                                           Safety Verification of Declarative Smart Contracts
                                                            Haoxian Chen∗ , Lan Lu† , Brendan Massey† , Yuepeng Wang‡ and Boon Thau Loo†
                                                                  ∗ ShanghaiTech University, † University of Pennsylvania, ‡ Simon Fraser University

                                                            hxchen@shanghaitech.edu.cn, {lanlu,masseybr,boonloo}@seas.upenn.edu, yuepeng@sfu.ca


                                           Abstract—Smart contracts manage a large number of digital                 [16]? (2) Is the implementation consistent with the formal
                                        assets nowadays. Bugs in these contracts have led to significant             model [18]? While this verification approach is generally more
                                        financial loss. Verifying the correctness of smart contracts is,             efficient, as the formal model abstracts away implementation
                                        therefore, an important task. This paper presents an automated
                                        safety verification tool, DCV, that targets declarative smart                details that are irrelevant to the verification task, it does require
                                        contracts written in DeCon, a logic-based domain-specific lan-               additional effort from the user since they need to specify the
arXiv:2211.14585v3 [cs.SE] 2 Aug 2023




                                        guage for smart contract implementation and specification. DCV               formal model in addition to the implementation. Additionally,
                                        proves safety properties by mathematical induction and can                   the steep learning curves of formal specification languages
                                        automatically infer inductive invariants using heuristic patterns,           may limit the adoption of such verification approach.
                                        without annotations from the developer. Our evaluation on 20
                                        benchmark contracts shows that DCV is effective in verifying                    This paper proposes an alternative verification approach
                                        smart contracts adapted from public repositories, and can verify             based on an executable specification of smart contracts. In
                                        contracts not supported by other tools. Furthermore, DCV                     particular, we target smart contracts written in DeCon [17], a
                                        significantly outperforms baseline tools in verification time.               domain-specific language for smart contract specification and
                                                                 I. I NTRODUCTION                                    implementation. A DeCon contract is a declarative specifica-
                                                                                                                     tion for the smart contract by itself, making it more efficient
                                           Smart contracts are programs that process transactions on                 to reason about than the low-level implementation in Solidity.
                                        blockchains – a type of decentralized and distributed ledgers.               It is also executable, in that it can be automatically compiled
                                        The combination of smart contracts and blockchains has                       into a Solidity program which can be deployed and run on
                                        enabled a wide range of innovations in many fields including                 the Ethereum blockchain. Automatic code generation based on
                                        banking [12], trading [31], [13], and financing [37], etc.                   the verified specification can save developers the manual effort
                                           Nowadays, smart contracts are managing a massive amount                   of implementing the contract. The high-level abstraction and
                                        of digital assets 1 , but they also suffer from security vulner-             executability of DeCon make it an ideal target for verifying
                                        abilities [2], [3], [1], which have lead to significant financial            contract-level properties.
                                        loss. In addition, since smart contracts are stored and executed                We implement a prototype, DCV (DeCon Verifier), for
                                        on blockchains, once they are deployed, it is hard to terminate              verifying declarative smart contracts. Properties are specified
                                        execution and update the contracts when new vulnerabilities                  as declarative queries for safety violations in the DeCon
                                        are discovered.                                                              language. DCV verifies safety invariants using mathematical
                                           One way to reduce potential vulnerabilities, whose patterns               induction on the sequence of transactions. A typical challenge
                                        are unknown during development, is safety verification: a                    in induction is to infer inductive invariants that can help
                                        smart contract that is always safe is less likely to suffer from             prove the target property. Our key insight for addressing
                                        undiscovered vulnerabilities[25], [32]. Thus, this work focuses              this challenge is that the DeCon language exposes the exact
                                        on the problem of safety verification for smart contracts.                   logical predicates that are necessary for constructing inductive
                                           Most existing solutions directly verify the implementation                invariants, which makes inductive invariant inference tractable.
                                        of smart contracts [7], [23], [28], [25], [32]. These solutions                 Another benefit of using DeCon is that it provides uniform
                                        have worked very well on verifying properties concerning                     interfaces for both contract implementation and property spec-
                                        one single transaction, e.g., integer overflow. However, when                ification. Specifically, DeCon models the smart contract states
                                        it comes to properties that needs to hold across an infinite                 as relational databases, and properties as violation queries
                                        sequence of transactions, these approaches suffer from low                   against these databases. Thus, developers can specify both
                                        efficiency due to state explosion issues. Some solutions [21],               the contract logic and its properties in a declarative and
                                        [15] trade soundness for efficiency, verifying properties up to              succinct way, and finish the verification and implementation
                                        a certain number of transactions.                                            automatically.
                                           On the other hand, in model-based verification approaches, a                 This paper makes the following contributions.
                                        formal model of the smart contract is specified separately from                 • A verification method for smart contracts, targeting
                                        the implementation. Given such a formal model and the im-                          contract-level safety invariants based on a declarative
                                        plementation, two kinds of verification problems are studied:                      specification language and the induction proof strategy
                                        (1) Does the formal model satisfy the desired properties [29],                     (Sections IV, V).
                                          1 According to Etherscan, as of the writing of this paper, the top ERC20      • A domain-specific adaptation of the Houdini algo-
                                        tokens are managing billions of dollars worth of tokens.                           rithm [26] to infer inductive invariants for automated
    proof (Section V).                                                     1 /* Declare relations. */
  • An open-source verification tool for future study and                  2 .decl recv_vote(proposal: uint)
                                                                           3 .decl vote(p: address, proposal: uint)
    comparison.                                                            4 .decl isVoter(v: address, b: bool)[0]
  • Evaluation that compares DCV with state-of-the-art veri-               5 .decl votes(proposal: uint, c: uint)[0]
    fication tools, on 20 representative benchmark smart con-              6 .decl wins(proposal: uint, b: bool)[0]
                                                                           7 .decl voted(p: address, b: bool)[0]
    tracts. Specifically, DCV successfully verifies all bench-             8 .decl *winningProposal(proposal: uint)
    marks, including the ones not supported by other tools.                9 .decl *hasWinner(b: bool)
    Furthermore, it is significantly more efficient than other            10 .decl *quorumSize(q: uint)
                                                                          11
    tools in terms of verification time (Section VI).                     12 .init isVoter
                                                                          13
                 II. I LLUSTRATIVE E XAMPLE                               14 /* Transaction where voter v cast a vote to
                                                                                 proposal p. */
                                                                          15 vote(v,p) :- recv_vote(p), msgSender(v),
                                                                          16               hasWinner(false), voted(v, false),
                                                                          17               isVoter(v, true).
                                                                          18
                                                                          19 /* Count votes for each proposal p. */
                                                                          20 votes(p,c) :- vote(_,p), c = count: vote(_,p).
                                                                          21
                                                                          22 /* A proposal wins by reaching a quorum. */
                                                                          23 wins(p, true) :- votes(p,c), quorumSize(q),
                                                                          24                   c >= q.
                                                                          25 hasWinner(true) :- wins(_,b), b==true.
                                                                          26 winningProposal(p) :- wins(p,b), b==true.
                   Fig. 1: Overview of DCV.                               27
                                                                          28 voted(v,true) :- vote(v,_).
                                                                          29
   Figure 1 presents an overview of DCV. It takes a smart                 30 /*Safety invariant: at most one winning proposal.
contract and a property specification (in the form of a violation         31 */
query) as input, both of which are written in the DeCon                   32 .decl inconsistency(p1: uint, p2: uint)[0,1]
                                                                          33 .violation inconsistency
language (Section III). The smart contract is then translated             34 inconsistency(p1,p2) :- wins(p1,true),
into a state transition system, and the property is translated into       35                           wins(p2,true),p1!=p2.
a safety invariant on the system states. DCV then verifies the
transition system preserves the safety invariant by mathemat-             Listing 1: A smart contract for voting, written in DeCon [17].
ical induction. In our prototype, the verification is performed
by Z3 [11], an automated theorem prover.
   If the verification succeeds, DCV guarantees that the smart              1) Participants cast their votes by sending vote transac-
contract is safe by ensuring that the violation query result is                tions, and these transaction records are stored in the
always empty, and returns an inductive invariant as a proof.                   “Vote Txs” table (on the left), with the voter address
However, if the verification fails, DCV returns “unknown”,                     and proposal ID (“Prop.”) listed as columns.
indicating that the smart contract may not satisfy the specified            2) For each proposal p, the number of votes it receives
safety invariant.                                                              can be counted by grouping the entries in the “Vote
   In the rest of this section, we use a voting contract as an                 Txs” table by the “Prop.” column, and then counting
example to illustrate the workflow of DCV. This example is                     the number of entries within each group. The counting
adapted from the voting example in Solidity [8], simplified for                results are displayed in the “Vote counts” table (middle).
ease of exposition.                                                         3) The proposal that first reaches a quorum is declared
A. A Voting Contract                                                           as the winner. Suppose in this example there are 5
                                                                               participants and the quorum size is 3, proposal 2 is
                                                                               selected as the winner as it gets 3 votes.

                                                                          B. Smart contract written in DeCon language
                                                                             Listing 1 shows the implementation of this voting contract
                                                                          in DeCon [17], which consists of three major components:
                                                                          (1) Relation declaration and annotation. The relations
                                                                          shown in Figure 2, along with other auxiliary relations, are
                                                                          declared in lines 1 to 10 of Listing 1. These declarations define
                   Fig. 2: A voting contract                              the table schema in relational databases, where each schema
                                                                          consists of the table name followed by column names and
   Figure 2 illustrates a voting scenario in a declarative view           types in parentheses. Optionally, a square bracket annotates
(i.e., everything is represented as a relational table):                  the index of the primary key columns, indicating that these



                                                                      2
                                      Fig. 3: The voting contract as a state transition system.


columns uniquely identify a row. For example, the relation                to false upon receiving a transaction request, the transaction
votes(proposal: uint, c: uint)[0] on line 5 has the first                 request is rejected, and no updates are made to any of the
column, proposal ID, as the primary key because votes are                 affected relations.
counted for each unique proposal. If no primary keys are an-              (3) Properties as violation query. Line 32 specifies a safety
notated, all columns are interpreted as primary keys, meaning             property as another relation, which is further annotated as a
that the table is a set of tuples.                                        violation query in line 33. This relation is defined by the rule
   A special kind of relation is a singleton relation, anno-              in line 34. If the rule is evaluated to true, it means that there
tated by ∗. Singleton relations only have one row, such as                exists two different winning proposals, indicating a violation to
winningProposal in line 8.                                                the safety invariant that there is at most one winning proposal.
   By default all relational tables are initialized to be empty,          Such violation query rule is expected to be always false during
except relations annotated by the init keyword (line 12).                 the execution of a correct smart contract.
These relations are initialized by the constructor arguments
passed during deployment.                                                 C. Translating DeCon Contract to State Transition System
(2) Relation definition in inference rules. Each relation is                 In order to perform formal verification, DeCon contracts
defined in the form of a rule, head :- body. Similar to the               are encoded as state transition systems. The state space com-
rules used in Datalog programs, the body consists of a list of            prises all possible valuations of the relational tables, and each
relational literals, and is evaluated to true if and only if there        successful transaction triggers an atomic state transition step
exists a valuation of all variables such that each literal has the        (the transaction atomicity is guaranteed by the underlying
corresponding concrete entries in the table. If the body is true,         Ethereum blockchain). Such encoding naturally captures the
the head is inserted into the corresponding table.                        semantics of smart contracts: reactive programs that listen and
   For instance, the rule in line 15 specifies that a vote                respond to requests (transactions).
transaction can be committed if there is no winner yet, the                  Figure 3 illustrates part of the transition system translated
message sender is a registered voter, and the voter has not               from the voting contract in Listing 1. The middle portion
voted before. The literal recv_vote(p) represents a transaction           (labeled “States after i Txs”) shows a state that is reached
handler that evaluates to true upon receiving a vote transaction          after i transactions from one of the initial states. At this
request. Rules that contain such transaction handlers (literal            point in the execution, proposal p1 has received two votes,
with a recv_ prefix in the relation name) are referred to as              proposal p2 has one, and no winner has been declared yet.
transaction rules. Committing a transaction inserts a new entry           Two outgoing edges from this state are highlighted. The one
into the transaction table (“Vote Txs” in Figure 2).                      on top represents a vote(p1) transaction, where p1 receives an
   Inserting a new vote(v,p) literal also triggers updates to             additional vote, thereby achieving the quorum and becoming
all its direct dependent rules. A rule is considered directly             the winning proposal. This transaction can be executed only
dependent on a relation R if and only if a literal of relation R is       if certain conditions are met, which are annotated on the edge
in its body. In this case, relation votes and voted are updated           (only part of the conditions are shown due to space limit). The
next. The chain of dependent rule updates continues until no              edge is derived from the transaction rule r in Listing 1 line 15
further dependent rules can be triggered, and the transaction             (recv vote(p1 ) ∧ ¬hasW inner ∧ ...), and its dependent rules
handling is finished. Using this mechanism, the votes for each            from line 19 to 26 (votes[p1 ] ≥ Q ∧ ...). This edge leads to
proposal, as well as the winning proposal, are automatically              a new state in which the number of votes for proposal p1 is
updated when new votes are approved.                                      incremented by one, and it becomes the winner, which is also
   On the other hand, if the body of a transaction rule evaluates         translated from line 19 to 26.



                                                                      3
   Similarly, the bottom right shows another transaction where
proposal p2 gets a vote, but hasWinner remains F alse since                                    Decl     := .decl R
no proposal has reached the quorum.                                                          Annot      := .(init | violation | public) R
   Section IV-B formally describes the algorithm to translate                         (Relation) R      := SR | SG | T R
a DeCon smart contract into a state transition system.                                 (Simple) SR      := .decl Str(Schema)[K]
Property. The violation query rule (line 31) is translated into                     (Singleton) SG      := .decl ∗ Str(Schema)
the following safety invariant:                                                  (T ransaction) T R     := .decl ∗ recv Str(Schema)
                                                                                (P rimary keys) K       := [k1, k2, ...]
         ¬[∃p1 , p2 . wins(p1) ∧ wins(p2) ∧ p1 ̸= p2]              (1)                     Schema       := Str : T 1, Str : T 2, ...
It states that there do not exist proposals p1 and p2 such that                           (T ype) T     := address | uint | int | bool
the violation query is true, which means there is at most one
winning proposal.                                                             Fig. 4: Syntax of DeCon relation declaration and annotation.
D. Proof by Induction
   To prove safety invariants of a smart contract against an                  Relation declarations. As shown in Figure 4, there are three
infinite sequence of transactions, DCV adopts the mathemati-                  kinds of relation declaration syntax:
cal induction approach. Given a state transition system, and a                   • Simple relations (SR) have a string for a relation name,
safety invariant, the proof consists of two steps:                                  followed by a schema in parenthesis, and optional pri-
   1) Base case: all initial states satisfy the safety invariant.                   mary key indices in a square bracket. The schema consists
   2) Induction step: if the safety invariant holds for some                        of a list of column names and types. When inserting a
       state s, then it also holds for all possible next states s′ .                new tuple to a table, if a row with the same primary keys
   One of the biggest challenges in automatic induction proof                       exists, then the row is replaced by the new tuple.
is finding inductive invariants. In some cases, a true safety                    • Singleton relations (SG) are relations annotated with a *
invariant may not be inductive, which means that although the                       symbol. These relations have only one row. Row insertion
safety invariant is true for all possible states, it can still fail the             is also an update for singleton relations.
induction proof step. To successfully complete the induction                     • Transaction relations (T R) are relations with prefix
step, an inductive invariant inv(s) needs to be found, such that                    recv , which are interpreted as an event trigger for
inv(s) ∧ prop(s) is inductive, where s is the state variable.                       incoming transaction requests. For example, in line 15
   For example, the safety invariant in Equation 1 cannot be                        of listing 1, the literal recv_vote(p) is triggered to be
proved inductively on its own. To make it inductive, it needs to                    true when the contract receives a vote transaction, with
be augmented by an inductive invariant, such as the following:                      parameter p being the proposal ID.
          ∀u ∈ Proposal . wins[u] =⇒ hasWinner                     (2)        In addition to these user-declared relations, there are reserved
                                                                              relations for built-in smart contract constructs that do not need
which asserts that if any proposal u ∈ Proposal is marked as                  to be declared. For example, relation *msgSender(p: address
the winner, the predicate hasW inner must also be true.                       ) is reserved for incoming message sender address. Similarly,
   Inductive invariants are typically inferred in a guess-and-                there are reserved relations for message values, current block
check manner [26], where a set of candidate invariants are                    number, contract constructors, etc.
enumerated until an inductive one is found. However, such                     Relation annotations. Three kinds of relation annotations are
approaches heavily rely on good heuristics to generate a set                  supported:
of candidate invariants. The insight of DCV is that, rules in                    • init indicates that the relation is initialized by a con-
DeCon contracts provide a concise and high-quality source of                        structor argument passed during deployment.
logical predicates for constructing inductive invariants. Since                  • violation means that the relation represents a safety
they only concern high-level logic and do not include imple-                        violation query.
mentation details, the extracted predicates are much smaller                     • public generates a public interface to read the contents
in size than those extracted from lower-level implementa-                           of the corresponding relational table.
tions, greatly speeding up the invariant search process. For
                                                                              Rules. Figure 5 shows the syntax of DeCon rules. A DeCon
instance, the predicates in Equation 2 (wins[u], hasWinner ),
                                                                              rule is of the form head : - body, which is interpreted from
are presented in the DeCon transaction rules in Listing 1.
                                                                              right to left: if the body is true, then it inserts the head tuple
We describe the details of predicate extraction and inductive
                                                                              into the corresponding relational table.
invariant generation in Section V.
                                                                                 A rule body is a conjunction of literals, and is evaluated
                  III. T HE D E C ON L ANGUAGE                                to true if there exists a valuation of variables π : V 7→ D
   A DeCon contract consists of three main blocks: (1) Rela-                  such that all literals are true. π maps a variable v ∈ V to
tion declarations, (2) Relation annotations, and (3) Rules.                   its concrete value in domain D. Given a variable valuation
                                                                              π, a relational literal is evaluated to true if and only if there
            (Contract) P := Decl | Annot | Rule                               exists a matching row in the corresponding relational table.



                                                                          4
                                                                             initialized to zero, or unconstrained if they are annotated
             Rule     := H(x̄) : - Body                                      to be initialized by constructor arguments.
             Body     := Join | R(x̄), y = Agg : R(ȳ)                     • E is the set of transaction types. Each element in E
             Join     := R(x̄) | P red, Join                                 corresponds to a type of transaction in DeCon (analogous
              Agg     := sum n | max n | min n | count                       to a transaction function definition in Solidity).
             P red    := R(x̄) | C(x̄) | y = F (x̄)                        • T r ⊆ S × E × S is the transition relation, generated from
   (Condition) C      :=> | < | ≥ | ≤ | =      ̸ | ==                        DeCon rules. T r(s, e, s′ ) means that state s can transit
    (F unction) F     := + | − | × | /                                       to state s′ via transaction e.
                                                                           In the rest of this section, we introduce the algorithm to
Fig. 5: Syntax of DeCon rules. H(x̄) and R(x̄) are relational            generate the transition relation from a DeCon smart contract.
literals, with H and R being the relation name, and x̄ is an
array of variables or constants. For the max, min, and sum               B. Transition Relation
aggregators, n is a variable in a numerical domain.                         The transition relation Tr is defined by a formula tr : S ×
                                                                         E × S 7→ Bool. Given s, s′ ∈ S, e ∈ E, s can transition to
                                                                         s′ in one step via transaction type e if and only if tr (s, e, s′ )
Other kinds of literals, including conditions, functions, and            is true. Equation 3 defines tr as a disjunction over the set of
aggregations, are interpreted as constraints on the variables.           formulas encoding each transaction rule. R is the set of rules
   In particular, DeCon supports three kinds of rules. Their             in the DeCon contract. T R is the set of transaction rules in
differences in syntax and semantics are described as follows:            R. Γ is a map from relation to its modeling variable, e.g.,
   • Join rules are rules that have a list of predicates in the          the relation vote(proposal:uint,c:uint)[0] is mapped to
     rule body, and contain at least one relational literal. A           votes : uint 7→ uint. Recall from Section III that transaction
     predicate can be either a relational literal, a condition, or       rules are rules that listen to the incoming transaction and is
     a function.                                                         only triggered by the incoming transaction request. Therefore,
   • Transaction rules are a special kind of join rules that             r.trigger is the literal with recv_ prefix in r’s body.
     have one special literal in the body: transaction han-
     dlers. A transaction handler literal has recv_ prefix in                   _
     its relation name, and is evaluated to true when the                tr ≜          [EncodeRule(r, R, Γ, r.trigger) ∧ e = r.T xN ame]
     corresponding transaction request is received. The rest                    r∈TR
                                                                                                                                        (3)
     of the rule body specifies the approving condition for the
     transaction.
                                                                         Algorithm 1 EncodeRule(r, R, Γ, τ ).
   • Aggregation rules are rules that contain a relational
                                                                              Input: (1) A DeCon rule r, (2) the set of all DeCon rules
     literal R(x̄) and an aggregator y = Agg n : R(ȳ),
                                                                         R, (3) a map from relation to its modeling variable Γ, (4) a
     where Agg can be either max, min, count, or sum. For
                                                                         trigger τ , the newly inserted literal that triggers r’s update.
     each valid valuation of variables in R(x̄), it computes
                                                                               Output: A formula over S × S, encoding r’s body
     the aggregate on the matching rows in R(ȳ). Take the
                                                                         condition, and all state updates triggered by inserting r’s head
     following rule from the voting contract as an example.
                                                                         literal.
     votes(p,c) :- vote (_,p), c = count: vote (_,p).
                                                                           1: Body ← EncodeRuleBody(Γ, τ, r)
     For each unique value p in the second column of table                 2: Dependent ← {EncodeRule(dr, R, Γ, τ ′ ) | (dr, τ ′ ) ∈
     vote, the aggregator c = count: vote (_,p), counts the                   DependentRules(r, R)}
     number of rows in table vote whose second column                      3: (H, H ′ ) ← GetStateVariable(Γ, r.head)
     equals p.                                                             4: Update ← H ′ = GetUpdate(H, r, τ )
                                                                                                                     V
   DeCon contracts are executable on the Ethereum                          5: TrueBranch ← Body ∧ Update ∧ ( d∈Dependent d)
blockchain [17]. To execute, they are first compiled                       6: FalseBranch ← ¬Body ∧ (H ′ = H)
into Solidity [9], which is further compiled to bytecode for               7: return TrueBranch ⊕ FalseBranch
the Ethereum blockchain.
             IV. P ROGRAM T RANSFORMATION                                   The procedure EncodeRule is defined by Algorithm 1. We
                                                                         explain it using the voting contract in Listing 1 as an example.
A. Declarative Smart Contracts as Transition Systems                        It takes four inputs: (1) a DeCon rule r, (2) the set of
  This section introduces the algorithm to translate a DeCon             all DeCon rules R, (3) a map from relation to its modeling
smart contract into a state transition system ⟨S, I, E, T r⟩             variable Γ, (4) and a trigger τ , the newly inserted literal that
where                                                                    triggers r’s update. In particular, a trigger τ takes the form
  • S is the state space: the set of all possible valuations of          insert [literal] or delete [literal]. It is used to inform
    all relational tables in DeCon.                                      the subroutine EncodeRuleBody how a relation is updated, and
  • I ⊆ S is the set of initial states that satisfy the initial          that the rest of the rule body in r needs to be encoded as a
    constraints of the system. All relations are by default              logical formula. For example, when a new vote transaction



                                                                     5
                      Γ, τ ⊢ R(x̄) ⇝ ϕ               Γ, τ ⊢ P red ⇝ ϕ1 Γ, τ ⊢ H(ȳ) : - Join ,→ ϕ2
                                             (Join1)                                               (Join2)
                 Γ, τ ⊢ H(ȳ) : - R(x̄) ,→ ϕ              Γ, τ ⊢ H(ȳ) : - P red, Join ,→ ϕ1 ∧ ϕ2
      τ = insert s′ = Γ(H)[k̄].value + n                          τ = delete s′ = Γ(H)[k̄].value − n
                                                     (Sum+)                                                     (Sum−)
 Γ, τ ⊢ H(ȳ) : - R(x̄), s = sum n : R(z̄) ,→ s = s′        Γ, τ ⊢ H(ȳ) : - R(x̄), s = sum n : R(z̄) ,→ s = s′
      τ = insert ϕ := c = Γ(H)[k̄].value + 1                  τ = delete ϕ := c = Γ(H)[k̄].value − 1
                                                     (Count+)                                                (Count−)
      Γ, τ ⊢ H(ȳ) : - R(x̄), c = count : R(z̄) ,→ ϕ          Γ, τ ⊢ H(ȳ) : - R(x̄), c = count : R(z̄) ,→ ϕ
                      τ = insert       m′ = Γ(H)[k̄].value ϕ := (n > m′ ∧ m = n) ⊕ (n ≤ m′ )
                                                                                             (M ax)
                                      Γ, τ ⊢ H(ȳ) : - R(x̄), m = max n : R(z̄) ,→ ϕ
                      τ = insert       m′ = Γ(H)[k̄].value ϕ := (n < m′ ∧ m = n) ⊕ (n ≥ m′ )
                                                                                             (M in)
                                      Γ, τ ⊢ H(ȳ) : - R(x̄), m = min n : R(z̄) ,→ ϕ

                                   Fig. 6: Inference rules for the EncodeRuleBody procedure.


is received, the trigger τ is insert recv_vote(p), where p is            deleted as well. Otherwise, τ is an insertion, and the update
the transaction parameter.                                               for relation r.head is also an insertion. Suppose we are in the
   In step 1, r’s body is encoded as a boolean formula,                  recursion step for encoding the votes rule in line 19, its update
BodyConstraint, by calling a procedure EncodeRuleBody                    constraint is generated as: votes ′ = Store(votes, p, votes[p]+
(Section IV-C). Take the rule for vote transaction in line 15            1), where the number of votes for proposal p is incremented
of Listing 1 as an example. Its body is encoded as:                      by one.
                                                                            Step 5 generates the constraint where r’s body is true, in
        ¬hasWinner ∧ ¬hasVoted [v] ∧ isVoter [v]                         conjunction with the update constraint and all dependent rules’
     Step 2 first selects direct dependent rules of r from               constraints. Step 6, on the other hand, generates constraints
the set of all DeCon rules R, by calling a subroutine                    where r’s body is false, no dependent rule is triggered, and
DependentRules(r , R). It returns a set of tuple (dr, τ ′ ), where       the head relation remains the same. Step 7 returns the final
dr is a direct dependent rule of r, and τ ′ is the corresponding         formula as an exclusive-or of the true and false branches,
trigger for dr. A rule dr is directly dependent on rule r if and         which encodes r’s body and how its update affects other
only if r’s head relation appears in dr’s body. For example,             relations in the contract.
rules in line 19 and 26 of Listing 1 are directly dependent              C. Encoding Rule Bodies
on the vote transaction rule in line 15. For the next trigger
                                                                            The procedure EncodeRuleBody is defined by two sets of
τ ′ , literal insertion results from a new relational tuple being
                                                                         inference rules:
derived from one of the rules. For example, if the rule for
transaction vote is evaluated to true, the next trigger τ ′ is              • Γ, τ ⊢ r ,→ ϕ states that a DeCon rule r is encoded by

insert vote(v,p). Literal deletion happens when literals with                 a boolean formula ϕ under context Γ and τ .
primary keys are inserted: inserting such literals implicitly               • Γ, τ ⊢ Pred ⇝ ϕ states that a predicate Pred is encoded

deletes the literals with the same primary keys, if exist. Next,              by a formula ϕ under context Γ and τ .
for each direct dependent rule dr of r and trigger τ ′ , it gets         The contexts (Γ and τ ) of both judgments are defined in the
dr’s encoding by recursively calling itself on dr and τ ′ .              same way as the input of Algorithm 1.
     Step 3 generates state variables for the head relation, where          Figure 6 shows the inference rules that define the first
H is for the current step, and H ′ is for the next transition            judgment Γ, τ ⊢ r ,→ ϕ. They are interpreted as follows.
step. Step 4 generates the head relation update constraint:                 A Join rule is encoded as a conjunction of the predicates,
H ′ equals inserting or deleting r’s evaluation result from H.           each of which is encoded from a literal in the rule body.
GetUpdate(H , r , τ ) is defined as follows:                             The encoding of individual literals is introduced later in this
                                                                        section.
                           
                            H.insert(r.head),                              Unlike Join rules, aggregation rules (Sum and Count)
                           
                            if r is agg. rule ∨ τ = insert              have separate inference rules for tuple insertion (+) and
GetUpdate(H, r, τ ) =
                           
                            H.delete(r.head),                           deletion (−). Because the relation between new and old aggre-
                           
                           
                                 if r is join rule ∧ τ = delete          gation results needs to be encoded. In these reference rules, k̄
                                                                         represents the primary keys of relation H, extracted from the
If r is an aggregation rule, the update is directly encoded              array ȳ, and Γ(H)[k̄].value reads the current aggregate result.
as insertion since new aggregation results implicitly overwrite          Note that, unlike the Join rules, the literal R(x̄) here does not
the old ones. If r is a join rule, and the trigger τ is a tuple          join with the aggregation literal, because it is only introduced
deletion, then r’s join result with the deleted tuple needs to be        to obtain valid valuations for the rule variables (every row



                                                                     6
in table R is a valid valuation). For each valid valuation, the         passing. Unlike prior work checking for message handling
aggregator computes the aggregate summary for the matching              errors, DCV assumes that message delivery and handling
rows in table R (Section III).                                          are always successful, and instead focuses on the functional
   For M ax and M in aggregation rules, DCV only encodes                correctness. Note that such interactions are limited to func-
the their update for tuple insertions, based on the assumption          tions without mutual recursions. Mutual recursions are not
that they only apply to transaction relations (tables that stores       supported because it breaks the atomicity assumption of a
the transaction records), which are append only and has no              transaction. To illustrate, suppose contract A’s transaction calls
primary keys. In other words, they have no tuple deletion.              contract B’s transaction Foo, which in turn calls another
   This assumption is made for two reasons. First, updating             transaction of contract A. In this case, the execution of two
M ax and M in for tuple deletion is complicated, because                transactions of contract A overlap, breaking the atomicity of
if the current maximum or minimum is deleted, the second                transactions.
largest or smallest element needs to be fetched and become
                                                                        D. Safety Invariant Generation
the new aggregation result. Such update requires storing
the whole table and even maintaining sorted table entries.                 Each violation query rule qr in a DeCon contract is first
Second, Ethereum has strict limits on the computation and               encoded as a formula ϕ such that Γ, τ ⊢ qr ,→ ϕ. Note that
storage of each smart contract and its transactions. Maintaining        the context Γ is the same mapping used in the transition system
maximum and minimum for tables with delete operation is                 encoding process. The second context, trigger τ , is a reserved
very expensive to be executed on Ethereum. We survey smart              literal check(), which triggers the violation query rule after
contracts in public repositories and find no contract with              every transaction.
such logic. Therefore, DCV adds such assumption and greatly                Next, the safety invariant is generated from ϕ as follows:
simplify the rule encoding.                                                               P rop ≜ ¬(∃x ∈ X. ϕ(s, x))
Encoding individual literals. Following are the inference
rules for judgment: Γ, τ ⊢ Pred ⇝ ϕ, which encodes                      where X is the state space for the set of non-state variables
individual literals.                                                    in ϕ. The property states that there exists no valuations of
                       τ.rel = R                                        variables in X such that the violation query is non-empty. In
                                           (Lit1)                       other words, the system is safe from such violation.
               Γ, τ ⊢ R(x̄) ⇝ τ = R(x̄)
                     τ.rel ̸= R                                                           V. V ERIFICATION M ETHOD
                                          (Lit2)
             Γ, τ ⊢ R(x̄) ⇝ Γ(R)[k̄] = v̄                               A. Proof by Induction
where k̄ represents the primary keys in relational literal R(x̄),          Given the state transition system translated from the DeCon
extracted from x̄, and v̄ represents the remaining fields in x̄.        smart contract, the target property prop(s), which is translated
                                                                        from the violation query, is proven by mathematical induction.
                                 (Condition)                            In particular, let S be the set of states in the transition
                 Γ, τ ⊢ C ⇝ C
                                                                        system, and E be the set of transaction types (vote is the
                                          (F unction)                   only transaction type in the example in Listing 1). Given
         Γ, τ ⊢ y = F (x̄) ⇝ y = F (x̄)
                                                                        s, s′ ∈ S, e ∈ E, let init(s) indicate whether s is in the initial
Conditions and functions are directly encoded as they are, as           state, and tr (s, e, s′ ) indicate whether s can transition to s′ via
shown in the above rules.                                               transaction type e. The mathematical induction is as follows:
Rule derivation and recursion. DCV assumes that on every
new incoming transaction request, there is at most one new
tuple derived by each rule, and that there is no recursion in             ProofInd(init, tr, prop) ≜     Base(init, prop)
the rules.                                                                                               ∧Induction(tr, prop)
    Rule recursion means that a rule is dependent on itself.                      Base(init, prop) ≜ ∀s ∈ S. init(s)
A rule ra is dependent to another rule rb (ra → rb ) if                                                   =⇒ inv(s) ∧ prop(s)
rb ’s head relation appears in ra ’s body. This dependency                      Induction(tr, prop) ≜ ∀s, s′ ∈ S, e ∈ E.
relation is transitive: ra → rb ∧ rb → rc =⇒ ra → rc .                                                   inv(s) ∧ prop(s) ∧ tr(s, e, s′ )
Using this dependency annotation (→), rule recursion means                                                =⇒ inv(s′ ) ∧ prop(s′ )
ra → ... → ra .                                                                                                                       (4)
    This assumption keeps the size of the transition constraint         where inv(s) ∧ prop(s) is an inductive invariant inferred by
linear to the number of rules in the DeCon contract, thus mak-          DCV such that prop(s) is proved to be an invariant of the
ing the safety verification tractable. We find this assumption          transition system.
holds for most smart contracts in the financial domain, and is             Algorithm 2 presents the procedure to infer inductive in-
true for all of the ten benchmark contracts in our evaluation.          variants. It first extracts a set of predicates P from the set
Multi-contract Interactions. Multi-contract interaction is              of transaction rules R (Section V-B). Then it generates a set
specified implicitly by DeCon rules that join relations from dif-       of candidate invariants using predicates in P , following two
ferent contracts. Such interactions are performed via message           heuristic patterns (Section V-C). Finally, it invokes a recursive



                                                                    7
Algorithm 2 Procedure to find inductive invariants.                     of a column to a certain concrete value, and can thus be used
     Input: a transition system ts, a map from relation to its          directly in candidate invariant construction.
modeling variable Γ, and a set of DeCon transaction rules R.               Therefore, in the next step, each predicate p in P0
    Output: an inductive invariant of ts.                               is augmented by one of its matching predicates in
 1: function F IND I NDUCTIVE I NVARIANT (C,ts)                         matchingPredicates(p, r), which is the set of predicates in
 2:     for inv in C do:                                                rule r that share at least one variable with predicate p. This
 3:         if refuteInv(inv, C, ts) then                               set of augmented predicates is P1 . Finally, the union of P0
 4:             return FindInductiveInvariant(C \ inv, ts)              and P1 is returned.
 5:         end if
                                                                        C. Candidate Invariant Generation
 6:     end forV
 7:     return ci ∈C ci                                                    Given the set of predicates in P , DCV generates candidate
 8: end function                                                        invariants following two heuristic template patterns. Each
          S
 9: P ← r∈R ExtractPredicates(r, Γ)                                     pattern is a logical formula that consists of one or more
10: C ← GenerateCandidateInvariants(P)                                  placeholders. These placeholders are replaced by predicates
11: return FindInductiveInvariant(C, ts)                                extracted from transaction rules (P ) during template instanti-
                                                                        ation. DCV unions all possible template instantiations as the
                                                                        set of candidate invariants.
                                                                           The concrete forms of the two template patterns used in
subroutine F IND I NDUCTIVE I NVARIANT to find an inductive
                                                                        DCV are as follows:
invariant.
   The procedure F IND I NDUCTIVE I NVARIANTS is adopted                         {∀x ∈ X. ¬init(s) =⇒ ¬p(s, x) | p ∈ P }
from the Houdini algorithm [26]. It iteratively refutes can-               {∀x ∈ X. ¬init(s) ∧ q(s, x) =⇒ ¬p(s, x) | p, q ∈ P }
didate invariants in C, until there is no candidate that can be
refuted, and returns the conjunction of all remaining invariants.       where X is the set of non-state variables in the body of the
The subroutine refuteInv is defined in Equation 5, which                formula. ¬init(s) is used as the implication premise so that
refutes a candidate invariant if it is not inductive:                   the whole formula can be trivially implied by the transition
                                                                        system’s initial constraints.
  refuteInv(inv, C, ts) ≜ ∨¬(ts.init      =⇒ inv)
                                                                           Having ¬p as the implication conclusion is based on the
                             ∨¬[( c∈C c) ∧ ts.tr =⇒ inv ′ ]
                                  V
                                                              (5)       observation that, in order to prove safety invariants, a lemma
where inv ′ is adopted by replacing all state variables in inv          is needed to prevent the system from unsafe transitions. Recall
with their corresponding variable in the next transition step.          from Section V-B that predicate p is one of the transaction
   A property of this algorithm is that, given a set of candidate       conditions, thus having ¬p in the invariant can prevent relevant
invariants C, it always returns the strongest inductive invariant       transactions from committing. In the second pattern, we add
that can be constructed in the form of conjunction of the               another predicate q ∈ P0 in the implication premise to make
candidates in C [26].                                                   the pattern more robust to different contracts and properties.
                                                                                              VI. E VALUATION
B. Predicate Extraction
                                                                               TABLE I: Benchmark properties for group one.
Algorithm 3 ExtractPredicate(r, Γ).
                                                                         Benchmarks          Properties
     Input: a transaction rule r, a map from relation to its
                                                                         wallet              No negative balance.
modeling variable Γ.
                                                                         crowFunding         No missing fund.
    Output: a set of predicates P .                                      ERC20               Account balances add up to totalSupply.
 1: τ ← r.trigger                                                        ERC721              All existing tokens have an owner.
 2: P0 ← {p | l ∈ r.body, Γ, τ ⊢ l ⇝ p}                                  ERC777              No default operator is approved for individual
 3: P1 ← {p ∧ q | p ∈ P0 , q ∈ MatchingPredicates(p, r)}                                     account.
 4: return P0 ∪ P1                                                       ERC1155             Each token’s account balances add up to that
                                                                                             token’s totalSupply.
                                                                         controllableToken   Account balances add up to totalSupply.
   Algorithm 3 presents the predicate extraction procedure.              partitionToken      Account balances add up to totalSupply in
It first transforms each literal in the transaction rule into a                              each partition.
predicate, and puts them into a set P0 . Some predicates in              paymentSplitter     No overpayment.
P0 do not contain enough information on their own, e.g.,                 vestingWallet       No early release.
predicates that contain only free variables. Because the logic           voting              At most one winning proposal.
of a rule is established on the relation among its literals (e.g.        auction             Each participant can withdraw at most once.
two literals sharing the same variable v means joining on
the corresponding columns). On the contrary, predicates that            Implementation. We implement the smart contract trans-
contain constants, e.g. hasWinner == true, convey the matching          formation and inductive invariant generation algorithms in



                                                                    8
TABLE II: Verification efficiency measured in time (seconds). TO stands for time-out after 1 hour. Unknown (?) means the
verifier cannot verify the contract property. Errors (×) from solc are caused by a known software issue [5]. Solc-verify also
returns errors on some benchmarks because it fails to analyze part of the OpenZeppelin libraries used in those benchmarks.
                Group             Name                #Rules   LOC           DCV               Solc          Solc-verify
                                                                           reference   DeCon     reference   DeCon
                Open standards    wallet                12       67             1        1            ?       17        ?
                and examples      crowFunding           14       85             2        1           ×         ?       38
                                  ERC20                 19      389             2        20          ×         ×       50
                                  ERC721                13      520             2       TO           ×         ×       50
                                  ERC777                31      562             2       TO            ?       74        ?
                                  ERC1155               18      645             2        12         TO        36       48
                                  paymentSplitter        6      166             1       TO           12       25        ?
                                  vestingWallet          7      113             1       TO            ?       55       14
                                  voting                 6       36             2        ×          TO         ?        ?
                                  auction               13      146            58        ×          TO         ?        ?
                                  controllableToken     23       55             2        29          2         ×       46
                                  partitionToken        16       70             2        1           1        14       30
                Top ERC20         bnb                   24      172             2        3           1         ?       55
                Tokens            link                  20      308             2        1           2        36       46
                                  ltcSwapAsset          25      655             2       TO           ×         ×       50
                                  matic                 25      510             2        2           ×        74       60
                                  shib                  22      508             2        1           ×        42       51
                                  tether                27      474             2        42          ×         ×       49
                                  theta                 21      213             2       270          1        45       49
                                  wbtc                  28      731             2       TO           ×         ×       67


Scala and use Z3 [11] to check the satisfiability of generated          of the voting contract contains recursion, which is not yet
formulas. Quantified formulas are handled by Z3’s default               supported by DeCon, and is thus dropped. In addition, solc and
heuristics.                                                             solc-verify do not support inline assembly analysis. Therefore,
Benchmarks. We collect 20 benchmark contacts in two                     inline assembly in the Solidity contracts are replaced with
groups. The first group consists of 12 contracts from open              native Solidity code. Minor syntax changes are also made to
libraries [6], [8] and examples from prior research [10]. Each          satisfy version requirements of the two baseline tools.
selected contract either has contract-level safety specifications          With these modifications, for each reference contract in
annotated, or has proper documentation from which we can                Solidity, we implement its counterpart in DeCon. Then we
come up with a contract-level safety specification. Table I             conduct verification tasks on three versions of benchmark con-
shows the contract names in group one and their target proper-          tracts: (1) DeCon contracts with DCV, (2) reference Solidity
ties. The second group consists of the most popular contracts:          contracts with solc and solc-verify, and (3) Solidity contracts
a list of top ERC20 contracts (based on circulating market              generated from DeCon with solc and solc-verify. For each set
cap) maintained by Etherscan [12]. Based on this list, we               of verification tasks, we measure the verification time and set
filter out the ones without source code or having unsupported           the time budget to be one hour. All experiments are performed
features (e.g., cryptographic algorithms) and obtain another 8          on a 2.4GHz core (single-threaded) and 4GB memory.
benchmark contracts. Since all of these contracts follow the            Results. Table II shows the evaluation results. DCV verifies
ERC20 standards, they are verified against the same property            all but one contract in two seconds, with auction taking 58
for the ERC20 token contract.                                           seconds. In particular, the properties for the voting and auction
Baselines. We use solc [9] and solc-verify [23] as the com-             contract are not inductive, and thus require inductive invariant
parison baselines. Solc is a Solidity compiler with a built-in          generation. Auction takes more time because it contains more
checker to verify assertions in source programs. It has been            rules and has a more complicated inductive invariant.
actively maintained by the Ethereum community, and version                 On the other hand, solc only successfully verifies 12 ref-
0.8.13 is used for this experiment. Solc-verify extends from            erence contracts, with one of them taking 270 seconds to
solc 0.7.6 and performs automated formal verification using             finish. It times out on six contracts, and reports SMT solver
strategies of specification annotation and modular program              invocation error on another two. This error has been an open
verification. We have also considered Verx [32] and Zeus [25],          issue according to the GitHub repository issue tracker [5],
but neither is publicly available.                                      which is sensitive to the operating system and the underlying
Experiment setup. We modify certain functionalities and syn-            library versions of Z3.
tax of the benchmark contracts so that they are compatible with            Similarly, solc-verify verifies 10 reference contracts, and
all comparison tools. In particular, the delegate vote function         reports unknown on four others. It also returns errors on



                                                                    9
six contracts because it cannot analyze certain parts of the             code) implements the formal semantics specified in KEVM.
included OpenZepplin libraries, although the libraries are               This verification is also sound, but it focuses on the functional
written in compatible Solidity version.                                  correctness of each Solidity function, instead of the state
   For Solidity contracts generated from DeCon, solc verifies            invariants across multiple transactions.
six and solc-verify verifies 15. The performance difference                 Formal semantics of EVM bytecode have also been for-
between the reference version and the DeCon-generated ver-               malized in F* [22] and Isabelle/HOL [14]. Scilla [33] is a
sion is potentially caused by the fact that DeCon generates              type-safe intermediate language for smart contracts that also
stand-alone contracts that implement all functionalities without         provides formal semantics. They offer precise models of the
external libraries. On the other hand, DeCon implements                  smart contract behaviors, and support deductive verification
contract states (relations) as mappings from primary keys to             via proof assistants. However, working with a proof assistant
tuples, which may incur extra analysis complexity compared               requires non-trivial manual effort. On the contrary, DCV
to the reference version.                                                provides fully automatic verification.
   In summary, DCV is highly efficient in verifying contract-            Vulnerability detection. Securify [36] encodes smart contract
level safety invariants, and can handle a wider range of smart           semantic information into relational facts, and uses Datalog
contracts compared to other tools. By taking advantage of the            solver to search for property compliance and violation pat-
high-level abstractions of the DeCon language, it achieves sig-          terns in these facts. Oyente [27] uses symbolic execution
nificant speedup over the baseline tools. In several instances,          to check generic security vulnerabilities, including reentrancy
baseline tools timeout after an hour or report an error, while           attack, transaction order dependency, etc. Maian [30] detects
DeCon is able to complete verification successfully.                     vulnerabilities by analyzing transaction traces. Unlike the
                                                                         sound verification tools, which require some amount of formal
                    VII. R ELATED WORK
                                                                         specification from the users, these work require no formal
Smart contract verification. Solc [28], Solc-verify [23],                specification and can be directly applied to any existing smart
Zeus [25], Verisol [38], and Verx [32] perform safety verifica-          contracts without modification, offering a quick and light-
tion for Solidity smart contracts. Similar to DCV, they infer in-        weight alternative to sound verification, although may suffer
ductive invariants to perform sound verification of safety prop-         from false positives or negatives.
erties. They also generate counter-examples as a sequence of             Fuzzing and testing. Fuzzing and testing techniques have
transactions to disprove the safety properties. SmartACE [39]            also been widely applied to smart contract verification. They
is a safety verification framework that incorporates a wide              complement deductive verification tools by presenting con-
variety of verification techniques, including fuzzing, bounded           crete counter-examples. ContractFuzzer [24] instruments EVM
model checking, symbolic execution, etc. In addition to safety           bytecodes to log run-time contract behaviors, and uncov-
properties, SmartPulse [35] supports liveness verification. It           ers security vulnerabilities from these run-time logs. Smar-
leverages the counterexample-guided abstraction refinement               tisan [19] uses static analysis to predict effective transaction
(CEGAR) paradigm to perform efficient model checking, and                sequences, and uses this information to guide fuzzing process.
can generate attacks given an environment model.                         SmartTest [34] introduces a language model for vulnerable
   DCV differs from these work in that it uses a high-level              transaction sequences, and uses this model to guide the search
executable specification, DeCon, as the verification target.             path in the fuzzing phase.
Such high-level modeling improves verification efficiency, but
it also means that DCV can only apply to smart contracts                                       VIII. C ONCLUSION
written in DeCon, while the other tools can work on most
existing smart contracts in Solidity or Move.                               We present DCV, an automatic safety verification tool for
   The Move Prover [20] (MVP) is a formal verifier for                   declarative smart contracts written in the DeCon language.
smart contracts written in the Move language [4]. Similar                It leverages the high-level abstraction of DeCon to gener-
to DCV, MVP also verifies safety properties. However, they               ate succinct models of the smart contracts, performs sound
target different languages and blockchain platforms. DCV is              verification via mathematical induction, and applies domain-
based on DeCon, which is declarative and more abstract, while            specific adaptations of the Houdini algorithm to infer inductive
Move is imperative. In addition, Move contracts work on the              invariants. Evaluation shows that it is highly efficient, verifying
Diem blockchain, while DeCon currently supports Ethereum                 all 20 benchmark smart contracts, with significant speedup
and Solidity. Despite the differences, we believe DCV could              over the baseline tools.
also benefit Move. An interesting future direction would be to              Our experience with DCV has also inspired interesting
implement a Move compiler for DeCon, so that DeCon can                   directions for future research. First, although DCV can verify
serve as a declarative specification for smart contracts on the          a wide range of contracts in the financial domain, we find
Diem blockchain, while Move as the implementation language               certain interesting applications that require non-trivial exten-
can provide better support for other verification tasks.                 sions to the modeling language, including contract inheritance,
Formal semantics of smart contracts. KEVM [18] intro-                    interaction between contracts, and functions that lie outside
duces formal semantics for smart contracts, and can automat-             relational logic. Second, since DCV verifies on the contract
ically verify that a Solidity program (its compiled EVM byte-            logic-level, we would also like to verify translation correctness



                                                                    10
for the DeCon-to-Solidity compiler, to ensure the end-to-end                          [26] Shuvendu K Lahiri and Shaz Qadeer. Complexity and algorithms for
soundness of DCV’s verification results.                                                   monomial and clausal predicate abstraction. In International Conference
                                                                                           on Automated Deduction, pages 214–229. Springer, 2009.
                                                                                      [27] Loi Luu, Duc-Hiep Chu, Hrishi Olickel, Prateek Saxena, and Aquinas
                              R EFERENCES                                                  Hobor. Making smart contracts smarter. In Proceedings of the 2016
                                                                                           ACM SIGSAC conference on computer and communications security,
 [1] King of the ether throne — post-mortem investigation. https://www.                    pages 254–269, 2016.
     kingoftheether.com/postmortem.html, 2016.                                        [28] Matteo Marescotti, Rodrigo Otoni, Leonardo Alt, Patrick Eugster,
 [2] Understanding the dao attack. https://www.coindesk.com/learn/2016/06/                 Antti EJ Hyvärinen, and Natasha Sharygina. Accurate smart contract
     25/understanding-the-dao-attack/, 2016.                                               verification through direct modelling. In International Symposium on
 [3] Not a fair game – fairness analysis of dice2win. https://blogs.360.net/               Leveraging Applications of Formal Methods, pages 178–194. Springer,
     post/Fairness Analysis of Dice2win EN.html, 2018.                                     2020.
 [4] The move team: The move programming language. https://diem.github.               [29] Zeinab Nehai, Pierre-Yves Piriou, and Frederic Daumas. Model-
     io/move/, 2020.                                                                       checking of smart contracts. In 2018 IEEE International Conference on
 [5] Cannot replicate smtchecker example output.           https://github.com/             Internet of Things (iThings) and IEEE Green Computing and Commu-
     ethereum/solidity/issues/13073, 2022.                                                 nications (GreenCom) and IEEE Cyber, Physical and Social Computing
                                                                                           (CPSCom) and IEEE Smart Data (SmartData), pages 980–987. IEEE,
 [6] Openzeppelin. https://github.com/OpenZeppelin/openzeppelin-contracts,
                                                                                           2018.
     2022.
                                                                                      [30] Ivica Nikolić, Aashish Kolluri, Ilya Sergey, Prateek Saxena, and Aquinas
 [7] Smtchecker and formal verification. https://docs.soliditylang.org/en/v0.
                                                                                           Hobor. Finding the greedy, prodigal, and suicidal contracts at scale.
     8.17/smtchecker.html, 2022.
                                                                                           In Proceedings of the 34th Annual Computer Security Applications
 [8] Solidity by example. https://docs.soliditylang.org/en/v0.8.17/solidity-               Conference, ACSAC ’18, page 653–663, New York, NY, USA, 2018.
     by-example.html, 2022.                                                                Association for Computing Machinery.
 [9] The solidity contract-oriented programming language. https://github.             [31] Benedikt Notheisen, Magnus Gödde, and Christof Weinhardt. Trading
     com/ethereum/solidity, 2022.                                                          stocks on blocks-engineering decentralized markets. In International
[10] Verx smart contract verification benchmarks. https://github.com/eth-sri/              Conference on Design Science Research in Information System and
     verx-benchmarks, 2022.                                                                Technology, pages 474–478. Springer, 2017.
[11] Z3. https://github.com/Z3Prover/z3, 2022.                                        [32] Anton Permenev, Dimitar Dimitrov, Petar Tsankov, Dana Drachsler-
[12] Erc-20 top tokens. https://etherscan.io/tokens, 2023.                                 Cohen, and Martin Vechev. Verx: Safety verification of smart contracts.
[13] Non-fungible tokens (nft). https://etherscan.io/tokens-nft, 2023.                     In 2020 IEEE symposium on security and privacy (SP), pages 1661–
[14] Sidney Amani, Myriam Bégel, Maksym Bortin, and Mark Staples.                         1677. IEEE, 2020.
     Towards verifying ethereum smart contract bytecode in isabelle/hol. In           [33] Ilya Sergey, Vaivaswatha Nagaraj, Jacob Johannsen, Amrit Kumar, An-
     Proceedings of the 7th ACM SIGPLAN International Conference on                        ton Trunov, and Ken Chan Guan Hao. Safer smart contract programming
     Certified Programs and Proofs, pages 66–77, 2018.                                     with scilla. Proceedings of the ACM on Programming Languages,
[15] Pedro Antonino and AW Roscoe. Formalising and verifying smart                         3(OOPSLA):1–30, 2019.
     contracts with solidifier: a bounded model checker for solidity. arXiv           [34] Sunbeom So, Seongjoon Hong, and Hakjoo Oh. {SmarTest}: Effectively
     preprint arXiv:2002.02710, 2020.                                                      hunting vulnerable transaction sequences in smart contracts through lan-
[16] Franck Cassez, Joanne Fuller, and Horacio Mijail Antón Quiles. De-                   guage {Model-Guided} symbolic execution. In 30th USENIX Security
     ductive verification of smart contracts with dafny. In International                  Symposium (USENIX Security 21), pages 1361–1378, 2021.
     Conference on Formal Methods for Industrial Critical Systems, pages              [35] Jon Stephens, Kostas Ferles, Benjamin Mariano, Shuvendu Lahiri, and
     50–66. Springer, 2022.                                                                Isil Dillig. Smartpulse: automated checking of temporal properties in
[17] Haoxian Chen, Gerald Whitters, Mohammad Javad Amiri, Yuepeng                          smart contracts. In 2021 IEEE Symposium on Security and Privacy (SP),
     Wang, and Boon Thau Loo. Declarative smart contracts. In ESEC/FSE                     pages 555–571. IEEE, 2021.
     ’22, 2022.                                                                       [36] Petar Tsankov, Andrei Dan, Dana Drachsler-Cohen, Arthur Gervais,
[18] Xiaohong Chen, Daejun Park, and Grigore Roşu.              A language-               Florian Buenzli, and Martin Vechev. Securify: Practical security analysis
     independent approach to smart contract verification. In International                 of smart contracts. In Proceedings of the 2018 ACM SIGSAC Conference
     Symposium on Leveraging Applications of Formal Methods, pages 405–                    on Computer and Communications Security, pages 67–82, 2018.
     413. Springer, 2018.                                                             [37] Shuai Wang, Yong Yuan, Xiao Wang, Juanjuan Li, Rui Qin, and Fei-
[19] Jaeseung Choi, Doyeon Kim, Soomin Kim, Gustavo Grieco, Alex                           Yue Wang. An overview of smart contract: architecture, applications,
     Groce, and Sang Kil Cha. Smartian: Enhancing smart contract fuzzing                   and future trends. In 2018 IEEE Intelligent Vehicles Symposium (IV),
     with static and dynamic data-flow analyses. In 2021 36th IEEE/ACM                     pages 108–113. IEEE, 2018.
     International Conference on Automated Software Engineering (ASE),                [38] Yuepeng Wang, Shuvendu K Lahiri, Shuo Chen, Rong Pan, Isil Dillig,
     pages 227–239. IEEE, 2021.                                                            Cody Born, Immad Naseer, and Kostas Ferles. Formal verification of
[20] David Dill, Wolfgang Grieskamp, Junkil Park, Shaz Qadeer, Meng                        workflow policies for smart contracts in azure blockchain. In Working
     Xu, and Emma Zhong. Fast and reliable formal verification of smart                    Conference on Verified Software: Theories, Tools, and Experiments,
     contracts with the move prover. In International Conference on Tools                  pages 87–106. Springer, 2019.
     and Algorithms for the Construction and Analysis of Systems, pages               [39] Scott Wesley, Maria Christakis, Jorge A Navas, Richard Trefler, Valentin
     183–200. Springer, 2022.                                                              Wüstholz, and Arie Gurfinkel. Verifying solidity smart contracts via
[21] Joel Frank, Cornelius Aschermann, and Thorsten Holz. {ETHBMC}: A                      communication abstraction in smartace. In International Conference on
     bounded model checker for smart contracts. In 29th USENIX Security                    Verification, Model Checking, and Abstract Interpretation, pages 425–
     Symposium (USENIX Security 20), pages 2757–2774, 2020.                                449. Springer, 2022.
[22] Ilya Grishchenko, Matteo Maffei, and Clara Schneidewind. A semantic
     framework for the security analysis of ethereum smart contracts. In
     International Conference on Principles of Security and Trust, pages 243–
     269. Springer, 2018.
[23] Ákos Hajdu and Dejan Jovanović. solc-verify: A modular verifier for
     solidity smart contracts. In Working conference on verified software:
     theories, tools, and experiments, pages 161–179. Springer, 2019.
[24] Bo Jiang, Ye Liu, and Wing Kwong Chan. Contractfuzzer: Fuzzing
     smart contracts for vulnerability detection. In 2018 33rd IEEE/ACM
     International Conference on Automated Software Engineering (ASE),
     pages 259–269. IEEE, 2018.
[25] Sukrit Kalra, Seep Goel, Mohan Dhawan, and Subodh Sharma. Zeus:
     analyzing safety of smart contracts. In Ndss, pages 1–12, 2018.




                                                                                 11
