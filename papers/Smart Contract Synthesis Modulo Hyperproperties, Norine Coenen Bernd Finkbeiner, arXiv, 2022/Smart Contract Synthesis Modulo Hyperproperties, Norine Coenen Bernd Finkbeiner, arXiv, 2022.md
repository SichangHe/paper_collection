                                          Smart Contract Synthesis Modulo Hyperproperties
                                                                             Norine Coenen                                                           Bernd Finkbeiner
                                                         CISPA Helmholtz Center for Information Security                             CISPA Helmholtz Center for Information Security
                                                                   Saarbrücken, Germany                                                       Saarbrücken, Germany
                                                                   norine.coenen@cispa.de                                                        finkbeiner@cispa.de

                                                              Jana Hofmann                                                               Julia Tillman
                                         CISPA Helmholtz Center for Information Security                                CISPA Helmholtz Center for Information Security
                                                   Saarbrücken, Germany                                                          Saarbrücken, Germany
                                                   jana.hofmann@cispa.de                                                           julia.tillman@cispa.de
arXiv:2208.07180v2 [cs.LO] 10 Jul 2023




                                            Abstract—Smart contracts are small but highly security-                      several execution traces of the system. Prominent hyperproper-
                                         critical programs that implement wallets, token systems, auc-                   ties are information flow policies like noninterference and ob-
                                         tions, crowd funding systems, elections, and other multi-party                  servational determinism. Existing work on hyperproperties in
                                         transactions on the blockchain. A broad range of methods has
                                         been developed to ensure that a smart contract is functionally                  smart contracts focuses on verifying concrete information flow
                                         correct. However, smart contracts often additionally need to                    policies such as integrity, which are enforced using language-
                                         satisfy certain hyperproperties, such as symmetry, determinism,                 based methods [1], [2]. Hyperproperties are not limited to
                                         or an information flow policy. In this paper, we show how a                     information flow policies, though. To establish the users’ trust
                                         synthesis method for smart contracts can ensure that the contract               in a contract, one has to additionally show that a contract
                                         satisfies its desired hyperproperties. We build on top of a recently
                                         developed synthesis approach from specifications in the temporal                satisfies hyperproperties such as robustness and symmetry. In
                                         logic TSL. We present HyperTSL, an extension of TSL for the                     a voting contract, for example, all candidates should be treated
                                         specification of hyperproperties of infinite-state software. As a               symmetrically, and a vote from the owner of the contract
                                         preprocessing step, we show how to detect if a hyperproperty has                should not count more than any other vote.
                                         an equivalent formulation as a (simpler) trace property. Finally,                  In this work, we develop a general-purpose temporal logic,
                                         we describe how to refine a synthesized contract to adhere to its
                                         HyperTSL specification.                                                         HyperTSL, to express the wide range of hyperproperties
                                            Index Terms—hyperproperties, smart contracts, reactive syn-                  relevant in the context of smart contracts. We then show how
                                         thesis, temporal logics                                                         to automatically construct the underlying state machine of
                                                                                                                         a smart contract directly from the logical specification of
                                                                                                                         the hyperproperties. We approach the task from two angles.
                                                                   I. I NTRODUCTION
                                                                                                                         First, we investigate the synthesis problem of the logic and
                                            Smart contracts are small programs which describe trans-                     show how to approximate the in general undecidable problem
                                         actions between multiple parties. Common smart contracts                        to obtain correct-by-design implementations. Second, we
                                         implement wallets, token systems, auctions, crowd funding                       propose a two-step approach to include HyperTSL properties
                                         systems, and elections. Smart contracts run on the blockchain                   in a recently proposed smart contract synthesis approach [3].
                                         and thus remove the need for a trusted third party. Bugs in
                                         smart contracts have led to huge monetary losses in the last                    HyperTSL. We develop two variants of the logic, HyperTSL
                                         decade, making the need for rigorous formal foundations for                     and HyperTSLrel , which are both based on temporal stream
                                         smart contracts obvious. In the absence of a trusted third party,               logic (TSL) [4]. TSL extends linear temporal logic (LTL) with
                                         it is especially important to ensure that a contract implements                 the concept of cells and uninterpreted functions and predicates.
                                         the agreed order of transactions. The large body of existing                    These mechanisms separate the temporal control flow from the
                                         work on the correctness of a contract’s control flow mainly                     concrete data in the system, which enables reasoning about
                                         consists of verification methods to ensure that a contract                      infinite-state systems. TSL has been applied successfully to
                                         exhibits a correct behavior with respect to trace properties.                   synthesize hardware [5], functional programs [6], and also to
                                            Smart contracts often additionally need to satisfy hyperprop-                describe the underlying state machines of smart contracts [3].
                                         erties, however. Hyperproperties describe the relation between                  As an example, we can state that the winner of an election
                                                                                                                         remains the same after the method close has been called.
                                            This work was partially supported by the German Research Foundation                     (close →         Jwinner ↢ winnerK)
                                         (DFG) as part of the Collaborative Research Center “Foundations of Perspicu-
                                         ous Software Systems” (TRR 248, 389792660), and by the European Research        The contract’s method close is modeled as a boolean and the
                                         Council (ERC) Grant OSARES (No. 683300). N. Coenen, J. Hofmann, and
                                         J. Tillman carried out this work as members of the Saarbrücken Graduate        field winner is modeled as a cell. We define HyperTSL as
                                         School of Computer Science.                                                     a conservative extension of TSL. It adds quantification over
multiple executions; predicates, functions, and updates then         • We show that the synthesis problem of ∀∗ HyperTSL can
refer to one of the quantified executions. In an election with         be over-approximated by ∀∗ HyperLTL synthesis and that
two candidates A and B, we can state that two traces have the          the synthesis problem of ∃∗ HyperTSL can be under-
same winner A if they agree on the votes for A.                        approximated by LTL satisfiability checking.
                                                                     • We describe a preprocessing step to detect if a HyperTSL
∀π∀π ′ . (voteAπ ↔ voteAπ′ )
                                                                       formula has an equivalent TSL formulation.
          →   (Jwinner ↢ A()Kπ ↔ Jwinner ↢ A()Kπ′ )                  • We describe and implement a repair-like pruning
The second hyperlogic HyperTSLrel allows to relate executions          algorithm that refines a smart contract synthesized from
within a predicate. Here, we can state that the winners on two         a TSL specification to satisfy a ∀∗ HyperTSL formula.
executions are always the same as long as the votes are always
the same.                                                          Structure of the paper. We first give the necessary prelimi-
      ′
∀π∀π . (voteπ = voteπ′ ) →          (winnerπ = winnerπ′ )          naries, including the definitions of HyperLTL and TSL. In Sec-
                                                                   tion III, we present HyperTSL and HyperTSLrel , and show how
Note that the = predicate ranges over two different execution      to specify hyperproperties in a voting contract. We proceed by
variables π and π ′ . In TSL, all functions and predicates         investigating the realizability problem of HyperTSL and argue
are uninterpreted, but = would probably be implemented as          why HyperTSL is more suited for synthesis than HyperTSLrel .
actual equality.                                                   In Section V, we recap the synthesis workflow based on
                                                                   TSL [3] and discuss the combination of the TSL specification
Smart contract synthesis from HyperTSL. Synthesis con-             of the voting contract with the HyperTSL specifications.
structs correct-by-design systems from a formal specification.     Section VI discusses the detection of pseudo hyperproperties.
It therefore shifts the development from software writing to       Section VII presents the pruning of a contract with respect to
specification writing. This idea fits especially well to smart     HyperTSL, including a prototype implementation.
contracts. Most contracts belong to one of the major classes
like token systems or election protocols, and their behavior can                          II. P RELIMINARIES
be characterized with similar specifications. This also extends
                                                                     We recap the definitions of HyperLTL and TSL.
to hyperproperties: the set of actually relevant hyperproperties
is often the same across different systems.                        A. HyperLTL
   We therefore investigate the synthesis problem of Hyper-
TSL. Inherited from TSL, the problem is undecidable already           Let AP be an infinite set of atomic propositions. A trace t is
for a single quantifier. We show, however, that the ∀∗ fragment    an element of (2AP )ω . We write t[i] for the ith element of t. A
of HyperTSL can be approximated in ∀∗ HyperLTL, for which          trace property P is a set of traces, a hyperproperty H is a set
there exists a bounded synthesis approach implemented in           of sets of traces. HyperLTL [8] describes hyperproperties by
HyperBoSy [7]. For the ∃∗ fragment of HyperTSL, we present         extending LTL with explicit trace quantification. It is defined
an approximation based on LTL satisfiability checking.             with respect to an infinite set of trace variables V.
   As a step towards actual smart contract synthesis, we build                    φ ::= ∀π. φ | ∃π. φ | ψ
on a recent workflow that implements the synthesis of a smart
contract control flow from TSL specifications [3]. We present                     ψ ::= aπ | ¬ψ | ψ ∧ ψ |     ψ | ψ U ψ,
a two-step approach to synthesize a contract that adheres to       where a ∈ AP and π ∈ V. In HyperLTL, atomic propositions
HyperTSL specifications. First, we check if the combination        are indexed with the trace variable they refer to. The semantics
of a given TSL specification with a ∀∗ HyperTSL specification      of HyperLTL is defined with respect to a set of traces T . Let
lets the hyperproperty “collapse” to a simple trace property.      Π : V → T be a trace assignment that maps trace variables
We show that the check is undecidable in general, but can          to traces in T . To update Π, we write Π[π 7→ t], where
to some extend be approximated in a decidable fragment of          π maps to t and all other trace variables are as in Π. The
with HyperLTL satisfiability checking. If this is not the case,    satisfaction relation of HyperLTL is defined with respect to a
we synthesize the most general solution (the winning region)       trace assignment Π, a set of traces T , and a point in time i.
for the TSL specification using the tool presented in [3]. We
then prune the system to find a strategy that implements a           Π, T, i |= aπ        iff a ∈ Π(π)[i]
∀∗ HyperTSL property. Our implementation of the approach             Π, T, i |= ¬ψ        iff Π, T, i ̸|= ψ
shows that we can automatically construct a voting contract
                                                                     Π, T, i |= ψ1 ∧ ψ2 iff Π, T, i |= ψ1 and Π, T, i |= ψ2
which satisfies several hyperproperties.
                                                                     Π, T, i |=    ψ      iff Π, T, i + 1 |= ψ
Contributions. We present the first solution to automatically        Π, T, i |= ψ1 U ψ2 iff ∃j ≥ i. Π, T, j |= ψ2
construct smart contracts with respect to hyperproperties.                                         and ∀i ≤ k < j. Π, T, k |= ψ1
  • We define HyperTSL and HyperTSLrel , two hyperlogics
                                                                     Π, T, i |= ∃π. φ     iff ∃t ∈ T. Π[π 7→ t], T, i |= φ
     based on TSL, and show how they can specify hyper-
     properties occurring in the context of smart contracts.         Π, T, i |= ∀π. φ     iff ∀t ∈ T. Π[π 7→ t], T, i |= φ
As for LTL, we can derive the usual boolean logical con-               where c ∈ C, τ p ∈ TP , and τ f ∈ TF . An update term Jc ↢
nectives and temporal operators “eventually” ψ = ⊤ U ψ,                τf K denotes that the value of function term τf is assigned to
“globally” ψ = ¬ ¬ψ, and “weak until” ψ1 W ψ2 =                        cell c. We denote the set of update terms with TU .
(ψ1 U ψ2 )∨ ψ1 . When specifying smart contracts, we assume               Function and predicate terms are syntactic objects, i.e. the
specifications to belong to the syntactic safety fragment, i.e.,       term p(f c) only becomes meaningful when we assign, for
that they only contain , , and W as temporal operators. For-           example, c to the value 3, f to the function f (x) = x + 1
mulas from the syntactic safety fragment can be equivalently           and p to p(x) = x > 0. To assign a semantic interpretation
expressed using past-time temporal operators, which reason             to function and predicate symbols, we use an interpretation
about the past instead of the future of a trace. “Yesterday”           ⟨·⟩ : ΣF → F. A cell assignment C → TF is a total function
is the past-time equivalent of , and “since” S corresponds to          assigning exactly one function term to each cell. The set of all
U. We say that a trace set T satisfies a HyperLTL formula φ,           assignments C → TF is denoted by C. A computation ς ∈ C ω
written as T |= φ, if ∅, T, 0 |= φ, where ∅ denotes the empty          describes the control flow of the cells, i.e., which function term
trace assignment.                                                      is associated with a cell at which point in time. For every cell
   We define the HyperLTL realizability problem as in [9]. We          c ∈ C, let init c be a designated value assigned initially to
assume AP to be a disjoint union of a set of input propositions        c. Input streams I ω are infinite sequences of assignments of
and a set of output propositions, i.e., AP = AP in ∪˙ AP out . A       inputs to values. Given a computation, an input stream, and a
strategy σ : (2AP in )+ → 2AP out maps finite sequences of input       point in time i, we can evaluate a function term. The evaluation
valuations to an output valuation. For an infinite word w =            function η⟨·⟩ : C ω × I ω × N × TF → V is defined as
w0 w1 w2 · · · ∈ (2AP in )ω , the trace generated by a strategy σ is
defined as σw = (w0 ∪ σ(w0 ))(w1 ∪ σ(w0 w1 )) . . . ∈ (2AP )ω .
                                                                                            
                                                                                            ι[i] s
                                                                                                                        s∈I
We write traces(σ) for the set {σw | w ∈ (2AP in )ω }. We               η⟨·⟩ (ς, ι, i, s) := init s                      s∈C∧i=0
say that a strategy σ satisfies a HyperLTL formula φ over                                   
                                                                                              η⟨·⟩ (ς, ι, i−1, ς[i−1] s) s ∈ C ∧ i > 0
                                                                                            
AP = AP in ∪˙ AP out if traces(σ) |= φ.
                                                                        η⟨·⟩ (ς, ι, i, f τ0 . . . τn ) :=
Definition II.1 (HyperLTL realizability). A HyperLTL for-
mula φ over AP = AP in ∪˙ AP out is realizable if there is a                                 ⟨f⟩ η⟨·⟩ (ς, ι, i, τ0 ) . . . η⟨·⟩ (ς, ι, i, τn )
strategy σ : (2AP in )+ → 2AP out that satisfies φ.
                                                                       Note that ι[i] s denotes the value that input stream ι assigns
                                                                       to input s at position i. Likewise, ς[i] s is the function term
B. TSL
                                                                       that ς assigns to cell s at point in time i. As an example,
   We introduce the syntax and semantics of TSL follow-                to compute the value of cell x in step i, we might obtain
ing [3], [4]. TSL extends LTL with the concept of cells,               from the computation that x is updated to f x in step i, so
which hold data from an arbitrary domain. To abstract from             we recursively evaluate x in step i − 1 and apply the function
concrete data points, TSL employs uninterpreted functions and          assigned to f to the result. We evaluate a TSL formula ψ with
predicates. A TSL formula describes a system that receives             respect to an assignment function ⟨·⟩, an input stream ι ∈ I ω ,
a stream of inputs, abstracts from the concrete values using           a computation ς ∈ C ω , and a time step i ∈ N.
predicates, and produces a stream of cell updates using func-
tion applications. We formally define values, functions, and           ς, ι, i |=⟨·⟩ ¬ψ                iff ς, ι, i ̸|=⟨·⟩ ψ
predicates. The set of all values is denoted by V, the Boolean         ς, ι, i |=⟨·⟩ ψ1 ∧ ψ2           iff ς, ι, i |=⟨·⟩ ψ1 and ς, ι, i |=⟨·⟩ ψ2
values by B ⊆ V. An n-ary function f : V n → V computes
                                                                       ς, ι, i |=⟨·⟩    ψ              iff ς, ι, i + 1 |=⟨·⟩ ψ
a value from n values. An n-ary predicate p : V n → B
assigns a boolean value to n values. The sets of all functions         ς, ι, i |=⟨·⟩ ψ1 U ψ2           iff    ∃j ≥ i. ς, ι, j |=⟨·⟩ ψ2
and predicates are denoted by F and P ⊆ F, respectively.                                                      and ∀i ≤ k < j. ς, ι, k |=⟨·⟩ ψ1
Constants are both 0-ary functions and values.                         ς, ι, i |=⟨·⟩ Jc ↢ τ K          iff    ς[i] c ≡ τ
   Let I and C be the set of inputs and cells, and let ΣF
                                                                       ς, ι, i |=⟨·⟩ p τ1 . . . τn     iff    η⟨·⟩ (ς, ι, i, p τ1 . . . τn )
and ΣP ⊆ ΣF be the set of function and predicate symbols.
Function terms τ f are recursively defined by
                                                                       We use ≡ to syntactically compare two terms. An execution
                      f               f
                    τ ::= s | f τ . . . τ    f                         (ς, ι) satisfies a TSL formula ψ if ς, ι, 0 |=⟨·⟩ ψ holds. In this
                                                                       case, we write ς, ι |=⟨·⟩ ψ. A TSL formula ψ is satisfiable iff
where s ∈ I ∪ C and f is an n-ary function symbol. Predicate           there exists an interpretation ⟨·⟩ and an execution (ς, ι) such
terms τ p are obtained by applying a predicate to function             that ς, ι |=⟨·⟩ ψ [10].
terms. The sets of all function and predicate terms are denoted        TSL realizability. The realizability problem of a TSL formula
by TF and TP ⊆ TF , respectively. TSL formulas are built               ψ asks whether there exists a strategy which reacts to predicate
according to the following grammar:                                    evaluations with cell updates according to ψ. Formally, a
                                                                       strategy is a function σ : (2TP )+ → C. Given a strategy σ
     ψ ::= ¬ψ | ψ ∧ ψ |        ψ | ψ U ψ | τ p | Jc ↢ τ f K            and an input stream ι, we can define the resulting computation
σ(ι). To compute the cell updates at point in time i, we require        where π ∈ V, c ∈ C, τ p ∈ TP , and τ f ∈ TF . We evaluate
the current inputs as well as the history of cell updates:              a HyperTSL formula φ with respect to a set of executions
                                                                        E ⊆ C ω × I ω , an execution assignment function Π, and a
       σ(ι)[i] := σ( {τ p ∈ TP | η⟨·⟩ (σ(ι), ι, 0, τ p )} · . . .       point in time i. We omit the cases for ¬, ∧, , and U, which
                       . . . · {τ p ∈ TP | η⟨·⟩ (σ(ι), ι, i, τ p )} )   follow closely the respective cases in TSL.
Note that in order to define σ(ι)[i], the definition uses σ(ι).          Π, E, i |=⟨·⟩ Jc ↢ τ f Kπ         iff #ς (Π(π)) i c ≡ τ f
This is well-defined since the evaluation function η⟨·⟩ (ς, ι, i, τ )
                                                                         Π, E, i |=⟨·⟩ (p τ1 . . . τn )π iff η⟨·⟩ (ς, ι, i, p τ1 . . . τn )
only uses ς[0] . . . ς[i − 1].
                                                                                                                  for ς = #ς (Π(π)) and
Definition II.2 (TSL realizability [4]). A TSL formula ψ is
                                                                                                                       ι = #ι (Π(π))
realizable iff there exists a strategy σ : (2TP )+ → C such that
for every input stream ι ∈ I ω and every assignment function             Π, E, i |=⟨·⟩ ∃π. φ               iff ∃e ∈ E. Π[π 7→ e], E, i |=⟨·⟩ φ
⟨·⟩ : ΣP → F, it holds that σ(ι), ι |=⟨·⟩ ψ.                             Π, E, i |=⟨·⟩ ∀π. φ               iff ∀e ∈ E. Π[π 7→ e], E, i |=⟨·⟩ φ

                          III. H YPERTSL                                Here, #ι (·) and #ς (·) are used to project an execution on
   We extend TSL with execution quantifiers to allow reason-            its input stream and its computation. Given an assignment
ing about hyperproperties for infinite-state systems. There is          function ⟨·⟩ : ΣF → F, a set of executions E satisfies a
not a single obvious way to lift TSL to a hyperlogic, so we             HyperTSL formula φ, written E |=⟨·⟩ φ, if ∅, E, 0 |=⟨·⟩ φ.
motivate in the following our choices for HyperTSL.                     B. HyperTSLrel
Function and predicate interpretations. There are two op-
tions to deal with function and predicate interpretations. The             In HyperTSLrel , predicate terms are defined with respect to
first is to interpret functions and predicates differently across       the set of executions variables V. If τ 1 , . . . , τ n are function
multiple executions. This would make sense, for example,                terms, π1 , . . . πn ∈ V, and p is an n-ary predicate symbol,
to model multiple components of a system. Most of the                   then p τπ11 . . . τπnn is a predicate term. The syntax of
hyperproperties, however, concern the behavior of the same              HyperTSLrel is that of HyperTSL with the exception that
system when executed several times. Functions and predicates            we denote predicate terms as τπp1 ,...,πn instead of τπp . The
like equality and addition mostly stay the same across several          semantics of HyperTSLrel is that of HyperTSL except for the
executions. We therefore decide to quantify the function and            semantics of the predicate, which we define as follows.
predicate interpretation before quantifying executions.                 Π, E, i |=⟨·⟩ p τπ11 . . . τπnn     iff ⟨p⟩ v1 . . . vn
Domain of updates and predicates. Another question is
                                                                        where vj = η⟨·⟩ (#ς (Π(πj )), #ι (Π(πj )), i, τ j ) for 1 ≤ j ≤ n
whether predicates, functions, and update terms may contain
terms evaluated on different executions. In the case of update          Satisfaction of a HyperTSLrel formula is defined as for Hy-
terms the answer should probably be no: an update of the form           perTSL.
Jcπ ↢ f(cπ′ )K would mean that the system could access the
value of a cell at the same point in time but on a different            C. HyperTSL for Smart Contracts
execution. This does not seem realistic for a real system,                 As for TSL, the strength of HyperTSL and HyperTSLrel is
which would have to store all possible values a cell c could            in their use of uninterpreted predicates and functions together
hold at some point in time. Additionally, the execution chosen          with a cell mechanism. That way, the logics can describe
for π ′ differs with every quantifier evaluation. Predicates            control flow properties like “if predicate p(c) evaluates to
ranging over multiple executions, on the other hand, would              true, cell c should be updated by applying function f to it”.
be useful. One could state a stronger version of observational          Since the concrete implementation of p and f is not relevant
determinism, namely “if two traces agree on the value of input          for the property, the synthesized system can be later completed
x, then also cell c is always updated to the same term”, written        to a concrete system by implementing p and f as needed.
as (xπ = xπ′ ) → (Jc ↢ f(x)Kπ ↔ Jc ↢ f(x)Kπ′ ).                            In this section, we showcase how the logics can express
We therefore define two logics: HyperTSL, in which we                   temporal hyperproperties of smart contracts. As a running
allow predicates to range only over the same execution, and             example, we use a simple voting contract. We informally
HyperTSLrel , which relates multiple executions using predi-            describe the contract and specify hyperproperties that should
cates.                                                                  hold in such a contract. This showcases the expressiveness
                                                                        of the logics and makes the differences in expressiveness
A. HyperTSL
                                                                        become clear. We postpone the formal specification of the trace
   We define HyperTSL as an extension of TSL. The definition            properties of the contract to Section V.
of function terms τ f and predicate terms τ p are the same as              For simplicity, we describe the core features of an ex-
in TSL. The syntax of HyperTSL is given as follows.                     emplary voting contract, which are enough to demonstrate
    φ ::= ∀π. φ | ∃π. φ | ψ                                             typical hyperproperties occurring in a voting scenario. The
                                                                        contract describes an election where users can vote for either
    ψ ::= ¬ψ | ψ ∧ ψ |          ψ | ψ U ψ | τπp | Jc ↢ τ f Kπ           candidate A or candidate B by calling methods voteA and
voteB. The contract can be closed by the owner, who can call        influence the winner field. This formulation of determinism
method close. voteA, voteB, and close are modeled                   additionally entails that the past of an execution cannot influ-
as booleans. We assume that in each step, exactly one of            ence the choice of the winner.
voteA, voteB, and close holds. The contract has two                    In HyperTSLrel , we can express determinism by relating
fields, votesA and votesB, to store the number of votes             executions with predicates. Instead of abstracting from the
recorded for the candidates. Both fields are modeled as cells       concrete number of votes using the > predicate, we could
in TSL. In the smart contract setting, we use the term field        state local determinism as follows. As before, the = predicate
and cell interchangeably. Furthermore, winner holds the             used in the formula is uninterpreted.
current winner chosen by the contract. The winner is updated
in every step where the contract receives a vote, so either           ∀π. ∀π ′ .
                                                                           
Jwinner ↢ A()K or Jwinner ↢ B()K holds globally.                            votesAπ = votesAπ′ ∧ votesBπ = votesBπ′
A() and B() are constants.                                                  → sameWinner (π, π ′ )
                                                                                                   
   The hyperproperties relevant in such a setting are typical
hyperproperties such as determinism and symmetry. Consider,         Symmetry. A prominent fairness condition in systems with
for example, the question which candidate is chosen as winner       multiple agents is symmetry, which requires that agents are
if there is a tie. One would expect a form of symmetry, e.g.,       treated symmetrically. In the voting case, this means, e.g., that
that the winner is not simply always candidate A. Similarly,        if two traces swap the votes for A and B, then the winner must
one typically requires some sort of determinism, i.e., that         also be swapped.
in similar situations the same winner is chosen. We use the
                                                                      ∀π. ∀π ′ . (Jwinner ↢ A()Kπ ↔ Jwinner ↢ B()Kπ′ )
                                                                                
following syntactic sugar.                                                                                                     
                                                                            ∧ (Jwinner ↢ B()Kπ ↔ Jwinner ↢ A()Kπ′ )
    sameWinner (π, π ′ ) :=                                                  
                                                                         W (voteAπ ↮ voteBπ′ ) ∨ (voteBπ ↮ voteAπ′ )
                                                                                                                                  
         (Jwinner ↢ A()Kπ ↔ Jwinner ↢ A()Kπ′ )                                                                                    (2)
       ∧ (Jwinner ↢ B()Kπ ↔ Jwinner ↢ B()Kπ′ )                      The fairness property implies that in case of a tie, the winner
The formula states that two executions π and π ′ choose the         cannot be brute-forced to always be candidate A or candidate
same winner.                                                        B.
Determinism. We state that the winner of the election is            No harm. A typical monotonicity criterion in elections states
determined by the sequence of votes received.                       that a vote for the currently leading candidate should not harm
                                                                    the candidate. Translated to our context this means that a vote
   ∀π. ∀π ′ . sameWinner (π, π ′ ) W                                for candidate A does not lead to B being the winner instead
                                              
      (voteAπ ↮ voteAπ′ ) ∨ (voteBπ ↮ voteBπ′ )                     of A. We formulate this condition as follows in HyperTSL.
                                                                                                    
The formula states that for any two executions, as long as they             ′
                                                                                 ^                          ^             
                                                                     ∀π. ∀π .         xπ ↔ xπ ′ U                xπ ↔ xπ ′
receive the exact same votes, they should agree on who is the
                                                                               x∈TP                        x∈TP
winner. Alternatively, we could have stated a local version of                                            ^                              
determinism using a greater predicate. Instead of writing
                                                                                                                                     
                                                                     ∧ voteAπ ∧ voteBπ′ ∧                                xπ ↔ xπ ′
greater votesA votesB, we use the better readable infix                                          x∈(TP )\{voteA,voteB}
notation with >. Note that the predicate is uninterpreted at this    →    (Jwinner ↢ A()Kπ′ → Jwinner ↢ A()Kπ )
stage altough we intend it to be implemented as expected. We                                                                         (3)
express that the choice of the winner is strictly determined by
the current evaluation of the > predicate on the votes and the      The formula describes two executions on which all predicate
last vote.                                                          terms evaluate to the same value except for one point in time
                                                                    at which the first execution receives a vote for A while the
 ∀π. ∀π ′ .
            
                                                                    second receives a vote for B. Then, A is the winner in the first
   ((votesA > votesB)π ↔ (votesA > votesB)π′ )                      trace whenever A is in the second one.
    ∧ ((votesB > votesA)π ↔ (votesB > votesA)π′ )                   Elections with multiple candidates. HyperTSLrel can specify
    ∧ (voteAπ ↔ voteAπ′ ) ∧ (voteBπ ↔ voteBπ′ )                     hyperproperties in contracts with an unknown number of
                                                                    candidates. Assume that instead of voteA and voteB, the
    → sameWinner (π, π ′ )
                          
                                                                    contract has a single method vote with a parameter cand
                                                             (1)
                                                                    indicating which candidate the caller is voting for. We model
This formula states that if A and B received the same number        vote and cand as inputs. Now, the winner field might
of votes, the winner must be the same on both executions.           range over a domain of unknown size. We express determinism
Note that the formula implicitly entails that any other predi-      as follows.
cate/input does not influence the winner. For example, if there
                                                                                ∀π. ∀π ′ . (winnerπ = winnerπ′ )
                                                                                           
is a predicate term sender = owner() testing whether the                                                               
caller of the method is the contract’s owner, this should not                                W (¬(candπ = candπ′ ))
                  ∅       ϵ     {p(x)}                              the case for synthesis, though, and as long as predicates and
                                                                    functions remain uninterpreted. If we considered HyperTSLrel
          σ(∅)                     σ({p(x)})                        synthesis with the theory of equality, much more meaningful
                                                                    strategies would be possible. HyperTSLrel might also be useful
      ∅          {p(x)}           ∅        {p(x)}
                                                                    when performing model checking, where formulas can contain
 σ(∅∅)           σ(∅{p(x)}) σ({p(x)}∅) σ({p(x)}{p(x)})              predicates that are not part of the system. TSL synthesis with
   ..               ..         ..         ..                        theories has only been studied in one work so far [11] and is
    .                .          .          .                        therefore out of the scope of this paper. TSL model checking
Fig. 1: The strategy tree for a HyperTSL strategy σ branching       has not been studied at all so far. Both directions will be
on a single predicate term TP = {p(x)}.                             exciting future work.
                                                                    A. Realizability of ∀∗ HyperTSL
       IV. H YPERTSL S YNTHESIS VIA R EDUCTIONS                        We show that the fact that TSL synthesis can by approx-
  In this section, we define the synthesis problem of Hyper-        imated by LTL synthesis [4] carries over to ∀∗ HyperTSL.
TSL and argue why HyperTSL is better suited for synthesis           To do so we recap the approximation of TSL in LTL [4].
than HyperTSLrel . HyperTSL inherits the undecidable realiz-        The main idea of the approximation is to forget the fact
ability problem from TSL. We therefore show that ∀∗ Hyper-          that predicates must evaluate to the same value if evaluated
TSL synthesis can be soundly approximated by HyperLTL, i.e,         on cells that hold the same value. Then, every predicate
a strategy for the HyperLTL approximation can be translated         τ p and update term Jx ↢ τ f K can be replaced with an
to a strategy in HyperTSL. The ∃∗ fragment of HyperTSL              atomic proposition aτ p and ax to τ f , respectively, which is
synthesis can be approximated by LTL satisfiability to prove        denoted by syntacticConversion(ψ) for a given TSL formula
unrealizability.                                                    ψ. For example, syntacticConversion( (p x → Jx ↢ f xK)
                                                                    translates to (ap x → ax to f x ). We call the set of atomic
Definition IV.1. A HyperTSL formula φ is realizable iff             propositions obtained in that translation AP ψ . Additionally,
there exists a strategy σ : (2TP )+ → C such that for every         we ensure that in each step, exactly one update proposition
interpretation ⟨·⟩ : ΣP → F the set constructed from all input      holds for each cell:
streams satisfies φ, i.e., {(σ(ι), ι) | ι ∈ I ω } |=⟨·⟩ φ.                                ^ _                   ^            
                                                                                                                                
                                                                        cellProps(φ) :=                 aτ ∧            ¬aτ ′
   The above definition defines the realizability problem of
                                                                                               c∈C τ ∈TUc             τ ′ ∈TUc \{τ }
HyperTSL by generalizing the TSL definition, similarly to how
HyperLTL generalizes LTL. The strategy has the same type            where TUc is the set of all update terms of c and aτ is the
as a TSL strategy, i.e., it generates an execution by reacting      atomic proposition associated with term τ . Now we define
to the predicate evaluations for the current input stream. The
                                                                        [ψ]atomic := syntacticConversion(ψ) ∧ cellProps(ψ)
resulting set of executions must satisfy the HyperTSL formula.
A visualization of the definition can be found in Figure 1.         Given an execution e = (ς, ι) ∈ C ω × I ω and an interpretation
   In HyperTSLrel , formulas contain predicates that relate                                                       ⟨·⟩
                                                                    ⟨·⟩, we define the corresponding LTL trace [e]atomic over AP ψ .
multiple executions. However, a system can still only react
                                                                                    ⟨·⟩
to the inputs it receives, i.e., it cannot include the evaluation                [e]atomic [i] :={aτ p | η⟨·⟩ (ς, ι, i, τ p )} ∪
of such predicates in its decision making. A definition of                                       {ax to τ f | ς i x ≡ τ f }
the realizability problem could therefore only contain pred-
icates not ranging over multiple executions. This makes many           Theorem 1 in [4] shows that for a TSL formula ψ, if [ψ]atomic
formulas unrealizable or only realizable by trivial strategies      is realizable, then ψ is realizable. Actually, their proof shows
most likely not intended by the developer. Consider the two         the following stronger result.
HyperTSLrel formulas from Section III-C again. In the first         Proposition IV.1 (Proof of Theorem 1 in [4]). Let ψ be a TSL
formula, the evaluation of the terms votesAπ = votesAπ′             formula. For any execution e, any interpretation ⟨·⟩, and any
and votesBπ = votesBπ′ depends on the chosen exe-                                                        ⟨·⟩
                                                                    point in time i, e, i |=⟨·⟩ ψ iff [e]atomic , i |= [ψ]atomic .
cutions π and π ′ and can therefore not be known by the
system. The predicate symbol = is uninterpreted and could              This results entails that realizability of [ψ]atomic implies
be implemented with any binary predicate. A strategy must           realizability of ψ; the opposite direction does not hold. This is
be winning for all interpretations. The only winning strategy       because the semantics of TSL forbids spurious behavior, which
is therefore the trivial strategy to set winner to either always    is not captured by the approximation in LTL. For example,
A() or always B(). We observe a similar phenomenon for              if we have Jx ↢ yK at some point in time, p(x) will be
the second formula. Since = is an uninterpreted predicate, the      equivalent to p(y) but ap x and ap y are different atomic
only winning strategy in this case is to always copy the value      propositions with possibly different truth values assigned to
of cand to winner.                                                  them. Therefore, every execution e can be mapped to a trace
                                                                       ⟨·⟩
   The above observations make HyperTSL the better candi-           [e]atomic , but there are traces t over AP ψ such that there is no
                                                                                            ⟨·⟩
date to extend TSL synthesis to hyperproperties. This is only       execution e with [e]atomic = t. The approximation is still very
valuable, because strategies found for the LTL approximations                is undecidable [7]. However, there exists an implementa-
carry over to strategies for the TSL specification. We show that             tion of bounded synthesis for ∀∗ HyperLTL in the tool
this result can be lifted to ∀∗ HyperTSL and ∀∗ HyperLTL.                    BoSyHyper [7]. This approach searches for smallest systems
                                                ⟨·⟩           ⟨·⟩
Given a set of executions E, we set [E]atomic = {[e]atomic |                 implementing the formula. The efficient reduction from ∀∗
e ∈ E} and also lift [·]atomic to HyperTSL formulas by setting               HyperTSL to HyperLTL opens the door to apply BoSyHyper
[τπ ]atomic = ([τ ]atomic )π with τ being either a predicate term or         to HyperTSL.
an update term.
Lemma IV.2. Let φ be a HyperTSL formula. For any set                         B. Realizability of ∃∗ HyperTSL
of executions E and any interpretation ⟨·⟩, E |=⟨·⟩ φ iff                       Theorem IV.3 uses the downwards closedness of ∀∗ Hy-
   ⟨·⟩
[E]atomic |= [φ]atomic .                                                     perLTL properties. This is necessary since a strategy for Hy-
Proof. Let φ = (∃∗ ∀∗ )k . ψ be a HyperTSL formula consisting                perTSL produces “fewer” traces than a strategy for the trans-
of k blocks of ∃∗ ∀∗ quantifiers. For the first direction, let               lation of the formula to HyperLTL does. Consequently, the
                             ⟨·⟩                                             proof does not extend to HyperTSL formulas with existential
E |=⟨·⟩ φ. We show [E]atomic |= [φ]atomic . Let φ[i] be the
                                                                             quantifiers. We show how to translate the synthesis problem of
subformula of φ starting from the ith quantifier block with 1 ≤
                                                                             ∃∗ HyperTSL formulas to a TSL satisfiability problem, which
i ≤ k. We keep the invariant to only construct trace assign-
                                                                             we can approximate by LTL satisfiability checking using the
ments Π such that there exists an execution assignment Π̂ with
                ⟨·⟩                                                          translation from TSL to LTL from [4]. In contrast to the case
Π(π) = [Π̂(π)]atomic and Π̂, E, 0 |=⟨·⟩ φ[i]. When choosing the
                                                                             of ∀∗ HyperTSL formulas, the approximation of existential
witness traces for the existential variables π1i+1 , . . . πni+1 of the
                                                                  ⟨·⟩        properties in LTL can be used to show unrealizability instead
(i + 1)th quantifier block, we choose Π(πji+1 ) = [ei+1       j ]atomic      of realizability.
where ei+1
        j   is assigned to πji+1 by the proof of satisfaction of
φ[i] with respect to the current execution assignment Π̂. Now,               Theorem IV.4. Given an ∃∗ HyperTSL formula φ, there exists
by Proposition IV.1 and a simple induction over the structure                a TSL formula ψTSL such that φ is realizable iff ψ is satisfiable.
                     ⟨·⟩
of ψ, we get Π, [E]atomic , 0 |= ψ. The argument is similar for              Proof. Let φ = ∃π1 . . . ∃πn . ψ. We encode the fact that all
                                                ⟨·⟩
the other direction since for every t ∈ [E]atomic , there exists             traces in a model of φ are producible by a strategy:
                         ⟨·⟩
an e ∈ E such that [e]atomic = t.                                                                   "             #  "                  #
                                                                                                      ^                 _            p
  Note that the above lemma does not extend to HyperTSLrel                     φstrat := ∀π. ∀π ′ .     τπu ↔ τπu′ W          τπp ↮ τπ′
as predicates over multiple executions cannot be mapped to                                         τ u ∈TU                  τ p ∈TP
HyperLTL. From the lemma we get the following theorem.
We will also reuse the lemma in Section V.                                   The formula states that while two executions have the same
                                                                             predicate evaluations, they have to perform the same updates.
Theorem IV.3. Let φ be a ∀∗ HyperTSL formula. If [φ]atomic                   Formula φ′ = ∃π1 . . . ∃πn . ψ ∧ φstrat ensures that the exe-
is realizable, then φ is realizable.                                         cutions chosen as witnesses for π1 , . . . , πn can be arranged
Proof. Let AP φ = AP in ∪˙ AP out be the atomic propositions                 in a strategy tree. Thus, φ and φ′ are equi-realizable. The
obtained in the translation [φ]atomic , where AP in are the                  additional conjunct also ensures that φ′ is satisfiable iff it is
propositions generated for predicate terms and AP out the                    realizable. Formula φ′ is satisfiable iff it is satisfiable by n
propositions for update terms, respectively. Let σHyperLTL :                 executions. The ∀ quantifiers in φ′ quantify from these n exe-
(2AP in )+ → 2AP out be the realizing strategy for [φ]atomic . We            cutions. We can therefore create an equi-satisfiable ∃n formula
claim that the following strategy σ realizes φ.                              by “unrolling” the ∀ quantifiers. Let φstrat = ∀π. ∀π ′ . ψstrat . We
                                                                             define:
  σ (P1 · . . . · Pi ) c := τ f                                                                              ^
  s.t. [Jc ↢ τ f K]atomic ∈ σHyperLTL ([P1 ]atomic · . . . · [Pi ]atomic )      φnew := ∃π1 . . . ∃πn . ψ ∧        ψstrat [π 7→ πi , π ′ 7→ πj ]
                                                                                                             1≤i,j≤n
Here, we lift [·]atomic to sets by [Pj ]atomic = {[τ p ]atomic | τ p ∈
Pj }. By definition of cellProps, the function term τ f is unique            Now we have that φ is realizable iff φnew is satisfiable.
for every i and every cell c. We show that σ realizes φ. Let ⟨·⟩             The above formula is satisfiable iff a TSL formula ψTSL is
be any interpretation. Let E = {(σ(ι), ι) | ι ∈ I ω } be the set             satisfiable, where we construct ψTSL by creating n copies of
of executions obtained from σ and T = traces(σ) be the set of                each input and each cell.
                                                 ⟨·⟩
traces obtained from σHyperLTL . Notice that [E]atomic ⊆ T , but T
                             ⟨·⟩
may not be a subset of [E]atomic . Since T |= [φ]atomic and since               It is an open question whether the two approximations for ∀∗
                                                             ⟨·⟩             HyperTSL and ∃∗ HyperTSL can be combined to approximate
universal properties are downwards-closed, also [E]atomic |=
                                                                             formulas with quantifier alternations. The challenge here is
[φ]atomic . Therefore, by Lemma IV.2 we have E |=⟨·⟩ φ.
                                                                             that universal properties are best over-approximated to obtain
 This theorem approximates ∀∗ HyperTSL synthesis by                          realizability results, whereas existential properties would need
 ∗
∀ HyperLTL synthesis. Even for HyperLTL, this problem                        an under-approximation.
V. H YPERPROPERTIES FOR S MART C ONTRACT S YNTHESIS                 specification            BDD-based    ✓     free   ✓/✘   translation
   We have shown that universal and existential HyperTSL             (pastTSL)                synthesis       choices?       to solidity
formulas can be approximated by HyperLTL synthesis and                                            ✘              ✓
LTL satisfiability. For the case of universal properties, this                      refine
                                                                                                                          implementation of
result is, as of now, mostly of theoretic interest. The realiz-                                                          predicates/functions
ability problem of ∀∗ HyperLTL is undecidable [7]. Bounded
hyperproperty synthesis is also still in its infancy.              Fig. 2: Workflow for the synthesis of a smart contract control
   In the following three sections, we therefore present a more    flow as developed in [3].
feasible approach to synthesize smart contract control flows.
We exploit the fact that we do not synthesize a system from
hyperproperties only, but in combination with trace properties     admissible strategy, the specification might be incomplete and
describing the temporal behavior of the contract. We build         should be refined. If not, or if either strategy is fine, a strategy
on a workflow recently developed for smart contract control        is extracted from the winning region. In the last step, the
flows from TSL specifications [3] and augment it with methods      developer provides an implementation of the functions and
for HyperTSL. In this section, we recap the TSL approach           predicates (such that the implementation respects the assump-
by showing how to specify some of the trace properties             tions stated in the specification), and SCS YNT generates a
expected of a voting protocol as described in Section III-C.       Solidity smart contract.
We also show how to include the hyperproperties discussed             SCS YNT specializes on a correct temporal control flow
in Section III-C. In the next section, we analyze whether the      and does not check if the provided function and predicate
combination of hyperproperties with trace properties leads to      implementations satisfy the stated assumptions. This can be
“pseudo” hyperproperties. In Section VII, we synthesize the        checked by specialized tools based on SMT solving. For recent
most general system from the trace properties and resolve free     approaches on how to combine TSL synthesis with reasoning
choices with a repair-like algorithm.                              over theories and syntax-guided synthesis, see [11], [12].
A. Recap: Smart Contract Synthesis from TSL Specifications         B. Voting Protocol
   It was recently demonstrated that the temporal behavior of         The part of the TSL voting specification that is relevant for
a smart contract can be extensively specified in the syntactic     this paper is depicted in Specification 1.        Specifications
safety fragment of TSL [3]. The idea of the approach is to         are divided into three parts. Assumptions describe properties
synthesize the underlying state machine of a smart contract        we can assume, e.g., that in each step only one method is
from a TSL specification. The state machine is then trans-         called. We also formulate assumptions on the predicates which
lated to Solidity code, which can then be augmented with           must be met by the user providing the implementation of
additional functionality to obtain the desired contract. TSL       the functions and predicates. Requirements state in which
is a convenient logic to not only describe the correct order       order and under which conditions methods can be called.
of method calls (method “vote should not be called after           Obligations describe how the contract’s fields must be updated.
close has been successfully called”) but also how fields need         The specification has four inputs. There is one input for
to be updated to ensure a correct control flow. This can be        each method indicating the called method. The sender input
achieved through TSL’s cells and uninterpreted functions and       contains the caller of the method (msg.sender in Solidity).
predicates. The TSL specification abstracts from the concrete      Cells describe the fields of the contract. We use a function
implementation of functions and predicates and instead states      addOne, which will be implemented as an increment. There
how fields have to be updated if certain predicates hold (“if      are two predicates > and =, which will be implemented as
method vote is called, update the winner field, depending          the actual “greater” and “equals” predicate. Lastly, we use
on whether votesA > votesB”).                                      three constants, one for each candidate A and B, and one
   While TSL synthesis is in general undecidable [4], correct      for the owner of the contract. Constants will be translated to
solutions can be found through approximation in LTL, which         immutable Solidity fields which are set in the constructor.
works very well in practice [4]–[6]. By restricting the TSL           Method calls are assumed to be atomic, i.e., exactly one
specification to the past-time fragment, synthesis can be solved   method is called at a time. This follows other work on
comparatively fast using a BDD-based implementation in a           modeling the control flow of smart contracts, e.g., [13], [14].
tool called SCS YNT [3].                                           Initially, neither candidate has more votes than the other,
   The synthesis is integrated in a feedback loop as shown         what can be achieved by setting votesA and votesB to
in Figure 2. The user provides a past-time TSL specification,      0. Lastly, keeping in mind that the > predicate will be
which is translated to LTL. If the LTL formula is unrealizable,    implemented as the actual “greater” predicate, we assume that
this might be either a specification error or is due to the        votesA > votesB and votesB > votesA cannot hold
LTL approximation (in most cases it’s the former). If the          true at the same time. The requirements ensure that close can
specification is realizable, SCS YNT returns the full winning      only be invoked by the owner of the contract and that no vote
region – a Mealy machine that implements the specification         can be cast after the voting is closed. The obligations describe
and includes all realizing strategies. If there is more than one   the updates of the fields. When voteA or voteB is invoked,
 1   Inputs: voteA, voteB, close, reveal, sender                     by summarizing multiple transitions between the same states
 2   Cells: votesA, votesB                                           with boolean formulas. For example, (¬(vA > vB) ∧ Jw ↢
 3   Functions: addOne                                               B()K) ∨ (¬(vB > vA) ∧ Jw ↢ A()K) expresses that A can
 4   Predicates: >, =
 5   Constants: owner(), A(), B()
                                                                     be chosen as winner as long as B does not have strictly more
 6
                                                                     votes.
 7   --- Assumptions ---                                                From the winning region we can see that the TSL specifica-
 8   // Mutex on methods                                             tion leaves the free choice which candidate is the winner when
 9    (voteA → ¬ voteB ∧ ¬ close);                                   neither one has the majority of votes. Strategies permitted by
10    (voteB → ¬ voteA ∧ ¬ close);
11    (close → ¬ voteA ∧ ¬ voteB);                                   the winning region are, for example, to always choose A as
12    (voteA ∨ voteB ∨ close);                                       winner, or go for the candidate who got the last vote. Which
13                                                                   strategies are considered to be suitable is described by the
14   // Arithmetic assumptions on > predicate                        HyperTSL formulations of local determinism (Formula 1 in
15     ¬(votesA > votesB ∧ votesB > votesA);                         Section III-C), symmetry (Formula 2 in Section III-C), and the
16   // Initial assumption on number of votes
17   ¬(votesA > votesB) ∧ ¬(votesB > votesA);                        no harm property (Formula 3 in Section III-C). Our goal is to
18                                                                   combine the TSL specification with the HyperTSL specifica-
19   --- Requirements ---                                            tions to obtain a satisfactory strategy. Since the specification
20    (close → sender = owner());                                    of the voting contract abstracts from the concrete number of
21    (close →      ¬voteA ∧ ¬voteB);                                votes cast with the > predicate, we need to add the following
22

23   --- Obligations ---                                             assumption to make the combination of the specifications
24    (voteA → JvotesA ↢ addOne votesAK);                            realizable.
25    (voteB → JvotesB ↢ addOne votesBK);
26                                                                   ∀π. ∀π ′ .
27    (¬ voteA → JvotesA ↢ votesAK);                                  
                                                                       ((votesA > votesB)π ↔ (votesA > votesB)π′ )
28    (¬ voteB → JvotesB ↢ votesBK);                                                                                 
29                                                                      ∧ ((votesB > votesA)π ↔ (votesB > votesA)π′ )
30    ((voteA ∨ voteB)                                                W (voteAπ ↮ voteAπ′ ∨ voteBπ ↮ voteBπ′ )
31       → Jwinner ↢ A()K∨Jwinner ↢ B()K);
32    ((voteA ∨ voteB) ∧ votesA > votesB
33       → Jwinner ↢ A()K);                                          The property states that the evaluation of the > predicate is
34    ((voteA ∨ voteB) ∧ votesB > votesA                             the same for every two executions as long as they receive
35       → Jwinner ↢ B()K);                                          the same sequence of votes. The property is satisfied when
36                                                                   implementing addOne as increment and > as “greater than”.
37    (close →       Jwinner ↢ winnerK);                                When combining the TSL specification of the voting con-
 Specification 1: Functional specification of the voting contract    tract with local determinism, symmetry, and the no harm
 in TSL.                                                             property, we observe that there is only one valid strategy left
                                                                     to resolve a tie. Local determinism states that the winner may
                                                                     only depend on the greater predicate on the votes and the vote
                                                                     cast in the current step. This forbids to take into account the
 the respective field counting the votes must be increased.
                                                                     past of the trace, e.g., by choosing the winner differently in
 Otherwise, the field must self-update, i.e., stay unchanged. If a
                                                                     the first and in the second step. Symmetry excludes to brute
 vote is cast, then the contract must update the winner to either
                                                                     force and always let the same candidate win in case of a tie.
 A() or B(). If votesA holds more votes than votesB,
                                                                     Together with local determinism, the winner must therefore
 the winner field is set to A() and correspondingly to B()
                                                                     truly depend on the current vote. In combination with local
 if there are more votes in votesB. Once close has been
                                                                     determinism and symmetry, the no harm property forbids to
 called, the winner cannot change anymore.
                                                                     let A win if the current vote is for B (and vice versa). This
    In this paper, we include in Specification 1 only the trace
                                                                     leaves as only option to resolve a tie to let the candidate win
 properties which interact with the hyperproperties we are
                                                                     who got the current vote. In this case, we could therefore
 interested in. To obtain a satisfactory voting protocol, one
                                                                     replace the hyperproperties with a trace property describing
 would, for example, also record the voters who already cast
                                                                     exactly this strategy, which leads to a much easier synthesis
 their vote and require that every person only votes once
                                                                     problem.
 by using a predicate. This could be achieved by using a
 field voters and guard calls to voteA and voteB with
                                                                                   VI. P SEUDO H YPERPROPERTIES
 an uninterpreted predicate inVoters voters sender,
 which is later implemented as expected.                                The previous section has shown that it can be hard to see the
    The winning region synthesized from the above specifica-         implications of combining several hyperproperties with trace
 tion is depicted in Figure 3. We write w instead of winner,         properties. It might be the case that the conjunction leaves
 and vA and vB instead of votesA and votesB, respectively.           only one strategy to resolve free choices. To recognize such
 We also use +1 instead of addOne. We simplify the system            situations is not easy for a human. We therefore propose to
                                          ner() ∧
                                nder = ow
                     close ∧ se ¬(vB > vA)
                                ∧
                     ¬(vA > vB)             K ∧ Jw ↢ wK           q3    close ∧ sender = owner() ∧ Jw ↢ wK
                               K ∧ JvB ↢ vB
                     ∧JvA ↢ vA
        q1                                                         close ∧ sender = owner() ∧ Jw ↢ wK
              ¬(v
                 A > vB) ∧
              ∧ (voteA ∧ ¬(vB > vA) ∧ (Jw ↢ A(                    q2
                                                                        
                                                                         (¬(vA > vB) ∧ Jw ↢ B()K) ∨ (¬(vB > vA) ∧ Jw ↢ A()K)
                                                                                                                                  
                                      K ∧ JvB ↢ vB ∨ Jw ↢ B()K)
                          JvA ↢ +1 vA             )K
                  ∨ (voteB ∧
                                                                          
                             JvB ↢ +1 vB           K)                   ∧ (voteA ∧JvA ↢ +1 vAK ∧ JvB ↢ vBK)
                                         K ∧ JvA ↢ vA                      ∨ (voteB ∧JvB ↢ +1 vBK ∧ JvA ↢ vAK)
                                                                                                                  
                                                      K)


                           Fig. 3: Winning region for Specification 1 as synthesized by SCS YNT [3].


preprocess the specification by checking whether the hyper-        Theorem VI.3. It is undecidable whether a HyperTSL formula
properties in conjunction with the trace properties effectively    φ describes a pseudo hyperproperty.
define a trace property. To do so, we introduce the notion
                                                                   Proof. The proof follows from undecidability of the satisfiabil-
of pseudo hyperproperties. We first investigate the problem
                                                                   ity problem of TSL [10]. The formula φ = ∀π. ∀π ′ .(p a)π ↔
for the general definition based on equivalence checking, and
                                                                   (p a)π′ is not a pseudo hyperproperty as there exists an
subsequently consider the special case of synthesis.
                                                                   interpretation of p such that E consists of executions for which
Definition VI.1. A hyperproperty H is a pseudo hyperprop-          p a always evaluates to true, and E ′ consists of executions
erty iff there is a trace property P such that                     for which p a always evaluates to false. E and E ′ are not
                                                                   closed under union for φ. Now, let a TSL formula ψ be given
             ∀T ⊆ (2AP )ω . T ∈ H iff ∀t ∈ T. t ∈ P                for which we assume w.l.o.g. that p is a fresh predicate and a
                                                                   a fresh input. Since ∀π. ∀π ′ . false is a pseudo hyperproperty,
   If H is a pseudo hyperproperty, H describes the trace
                S                                                  the formula ∀π. ∀π ′ . ((p a)π ↔ (p a)π′ ) ∧ ψπ is a pseudo
property P = T ∈H T . For proofs we will often use the
                                                                   hyperproperty iff ψ is unsatisfiable. Here, ψπ denotes the
following fact.
                                                                   formula obtained by lifting ψ to a HyperTSL formula by
Proposition VI.1. If H is a pseudo hyperproperty, then H is        annotating predicate and update terms with the trace variables
closed under union and subsets.                                    π.
   The downwards closure property in the above proposition            Fortunately, the above negative result comes with the rem-
implies that only hyperproperties expressible with ∀∗ formulas     edy that we can approximate the problem in HyperLTL, which
can be pseudo hyperproperties. The following proposition           is a result of Lemma IV.2.
establishes the convenient fact that if a ∀∗ HyperTSL formula
φ is a pseudo hyperproperty, then the formula obtained by          Theorem VI.4. Let φ be a HyperTSL formula. If [φ]atomic is
using only a single execution variable in the body of the          a pseudo hyperproperty, then so is φ.
formula is equivalent to φ. The proposition is close to the        Proof. Closedness under union and subsets follows from
corresponding result for HyperLTL, which has been observed         Lemma IV.2 and since for every set of executions E and in-
                                                                                           ⟨·⟩              ⟨·⟩                     ⟨·⟩
in context of using HyperLTL synthesis for the synthesis           terpretation ⟨·⟩, [E]atomic = e∈E [e]atomic , i.e., [E ∪ E ′ ]atomic =
                                                                                                   S
of linear distributed architectures [7]. Given a HyperTSL              ⟨·⟩           ⟨·⟩                         ⟨·⟩            ⟨·⟩
                                                                   [E]atomic ∪ [E ′ ]atomic , and E ⊆ E ′ iff [E]atomic ⊆ [E ′ ]atomic .
formula φ = ∀π1 . . . ∀πn . ψ, we define its ∀1 counterpart as
φ[π] := ∀π. ψ[π1 7→ π, . . . , πn 7→ π].                              Using the above result, we can translate a ∀∗ HyperTSL
                                                                   formula to HyperLTL and check its equivalence with the
Proposition VI.2. A ∀∗ HyperTSL formula φ describes a              corresponding ∀1 formula. For HyperLTL, this check is de-
pseudo hyperproperty iff φ ↔ φ[π].                                 cidable, because of the decidability of the ∃∗ ∀∗ fragment of
Proof. We observe that a hyperproperty H is a pseudo hyper-        HyperLTL [7]: a HyperLTL formula φ = ∀π1 . . . ∀πn . ψ is
property iff                                                       equivalent to its ∀1 counterpart φ[π] iff φ[π] → φ (because
                                                                   of the semantics of the ∀). By merging the quantifiers, this
         ∀T ⊆ (2AP )ω . T ∈ H iff ∀t ∈ T. {t} ∈ H                  implication is valid iff the formula
Thus, for any set of executions E and any interpretation ⟨·⟩,               ∃π1 . . . ∃πn . ∀π. ¬ψ ∧ ψ[π1 7→ π, . . . πn 7→ π]
we have E |=⟨·⟩ φ iff ∀e ∈ E. {e} |=⟨·⟩ φ iff E |=⟨·⟩ φ[π].
                                                                   is unsatisfiable. Thus, if the check returns UNSAT, the Hyper-
  The proposition describes how to check if a HyperTSL             TSL formula is guaranteed to describe a pseudo hyperproperty,
property is a pseudo hyperproperty, namely by checking if          so we can replace the hyperproperty with its TSL version.
φ is equivalent to φ[π]. If it is, the TSL formula φ[π] can be        So far, we described the check for pseudo hyperproperties
used for synthesis. The check is undecidable for HyperTSL,         in terms of satisfiability checking. This can be useful to
however.                                                           detect superfluous specifications or mistakes. For example, the
developer could have already specified in TSL that in case of        versions of local determinism, symmetry, and the no harm
a tie, the current vote determines the winner.                       property.

      (¬(votesA > votesB) ∧ ¬(votesB > votesA)                                     ∀π. ∀π ′ . (iπ ↔ iπ′ ) → (oπ ↔ oπ′ )
       → Jwinner ↢ A()K ↔ voteA)                                                   ∀π. ∀π ′ . (iπ ↮ iπ′ ) → (oπ ↮ oπ′ )
                                                                                   ∀π. ∀π ′ . iπ ∧ ¬iπ′ ∧ oπ′ → oπ
With this specification, the hyperproperties stated in Sec-
                                                                     The properties are not temporal, so they are realizable iff there
tion III-C are entailed by the specification. In the case of the
                                                                     are values o1 , o2 such that {{i, o1 }ω , {¬i, o2 }ω } satisfies the
“no harm” property, for example, the check with EAHyper
                                                                     three formulas. Let φ be their conjunction. There are only
reveals correctly within 0.003 seconds that the conjunction of
                                                                     four possible assignments of o1 , o2 to boolean values, each
the trace properties with the “no harm” property is a pseudo
                                                                     of which corresponds to a possible strategy. Indeed, for every
hyperproperty.
                                                                     possible strategy, φ is satisfied iff the trace property i ↔ o
   Without the above TSL specification however, the check
                                                                     is satisfied. However, the same does not hold for the trace
for the conjunction of local determinism, symmetry, and the
                                                                     property true, which is equivalent to φ[π]. Unfortunately, the
no harm property is labeled as a hyperproperty by EAHyper,
                                                                     general problem is undecidable already for HyperLTL, due
even though there is only one possible strategy. The reason for
                                                                     to the undecidability of the realizability problem of the ∀∗
that is the difference between realizability and satisfiability.
                                                                     fragment of HyperLTL.
Consider the following two traces.
                                                                     Theorem VI.5. Given a HyperLTL formula φ, it is in general
                                                  ω                  undecidable if there exists an LTL formula ψ such that for all
             (1) {voteA, Jwinner ↢ A()K}
             (2) {voteB, Jwinner ↢ A()K}ω                            strategies σ, traces(σ) |= φ iff ∀t ∈ traces(σ). t |= ψ.
                                                                     Proof. We show undecidability by a reduction from the ∀∗
In the first trace, neither votesA > votesB nor votesB >             HyperLTL realizability problem, which is undecidable [7]. Let
votesA, and there is always a vote for A, who is always              ρ be a ∀∗ HyperLTL formula over AP = AP in ∪˙ AP out .
the winner. The second trace is similar but there is always          We assume w.l.o.g. that AP in is non-empty. We define φ as
a vote for B. As single sets, both traces satisfy all three hy-      follows, where o is an output proposition that does not occur
perproperties. Together, they do not (because of the symmetry        in ρ.
requirement). Therefore, EAHyper returns that the conjunction                        φ := ρ ∧ ∀π. ∀π ′ . oπ ↔ oπ′
of the properties is not a pseudo hyperproperty (even in
combination with the full contract specification). When solving      We claim that ρ is unrealizable iff there exists an LTL
the realizability problem, however, we do not need to find an        formula ψ such that for all strategies σ, traces(σ) |= φ iff
equivalent trace property, it is enough to find a trace property     ∀t ∈ traces(σ). t |= ψ. If ρ is unrealizable, then we choose
which evaluates the same on all sets generated by strategies.        ψ := false. Since ρ is unrealizable, it holds for all σ that
We therefore adapt the notion of pseudo hyperproperties to           traces(σ) ̸|= φ iff ∀t ∈ traces(σ). t |= ψ. For the other
realizability. We give the definition for hyperproperties of         direction, assume that ρ is realizable and that there exists a
traces over AP in ∪˙ AP out , but the definition applies to traces   suitable LTL formula ψ. Let σ be the realizing strategy of ρ.
of any type, particularly also to hyperproperties over TSL-like      Since o is fresh for ρ, we can extend σ to σ1 and σ2 , where σ1
executions.                                                          adds o to the first output (for any input), and σ2 does not add
                                                                     o (also for any input). Both strategies realize φ, therefore, by
Definition VI.2. Let H be a hyperproperty over atomic propo-         our assumption, both strategies realize ψ. Now, let i ∈ AP in
sitions AP = AP in ∪˙ AP out . H is a pseudo hyperproperty in        be any input. We define σ3 as the strategy that adds o to the
the context of realizability if there is a trace property P such     first output exactly if i holds in the first position of the input
that                                                                 sequence. Since every trace generated by σ3 is either a trace
                                                                     of σ1 or σ2 , σ3 realizes ψ. However, it does not realize φ,
        ∀σ : (2AP in )+ → 2AP out .                                  which contradicts our assumption.
             traces(σ) ∈ H iff ∀t ∈ traces(σ). t ∈ P
                                                                        Lastly, we observe that we can decide if a HyperTSL
   The definition implies that a HyperTSL formula φ is a             formula is a pseudo hyperproperty if the formula contains
pseudo hyperproperty in the context of realizability iff there       as conjunct a local determinism formula like the one in our
is a TSL formula ψ such that a strategy σ realizes φ iff σ           running example. We define local determinism in the general
realizes ψ. In the context of realizability, however, ψ may          case as follows.
not be equivalent to φ[π]. To show why, we give an example              localDeterminism :=
in HyperLTL but the reasoning carries over to HyperTSL.                                    ^                  ^
Consider the example of the following HyperLTL formulas                      ∀π. ∀π ′ . ((   τπp ↔ τπp′ ) → (   τπc ↔ τπc′ ))
over input i and output o, which are abstract, simplified                                  τ p ∈TP                τ c ∈TU
Proposition VI.6. For every ∀∗ HyperTSL formula φ                      [TU ]atomic . S models φ if for every interpretation ⟨·⟩:
over predicate terms TP and update terms TU , if φ =                                                                 ⟨·⟩
localDeterminism ∧ φ′ , then deciding whether φ is a pseudo                   {(ς, ι) | ∃t ∈ traces(S). t = [(ς, ι)]atomic } |=⟨·⟩ φ
hyperproperty in the context of realizability is equivalent to a          The definition creates for each interpretation the set of
Boolean SAT problem.                                                   executions which have a trace through S and then checks if φ
   The above proposition follows from the observation that             is satisfied on these sets. We show that we cannot check the
localDeterminism ∧ φ is realizable iff there is a positional           satisfaction of a HyperTSL formula on such a system directly.
strategy that always assigns the same cell updates for the same        Lemma VII.1. Given a HyperTSL formula φ, it is undecidable
predicate evaluations, independently of the trace’s past. In this      whether a Mealy machine S over AP = [TP ]atomic ∪ [TU ]atomic
case, there are only finitely many combinations of predicate           models φ.
evaluations and the problem becomes finite.
                                                                       Proof. We show that the problem is already undecidable for
          VII. R ESOLVING C HOICES WITH R EPAIR                        TSL formulas expressed in HyperTSL as ∀π. ψπ , where ψπ is
                                                                       the π-indexed version of a TSL formula ψ . We proceed by
   If a hyperproperty is not a pseudo hyperproperty, we synthe-        reduction from the unsatisfiability problem of TSL. Let ψ be
size the winning region of the trace property and then check           a TSL property. ψ is unsatisfiable if for every ⟨·⟩ and every ς,
if free choices can be resolved such that the hyperproperty is         ι, it holds that ς, ι |=⟨·⟩ ¬ψ. Let S be the system that produces
satisfied. This is a repair algorithm additionally respecting the      every trace over AP = [TP ]atomic ∪ [TU ]atomic . Then, S models
distinction between inputs and outputs. We first give a formal         ∀π. ¬ψπ iff ψ is unsatisfiable.
definition of the problem we are interested in for HyperTSL
                                                                          However, owing to Lemma IV.2, for every ∀∗ HyperTSL
formulas. As observed several times, the formal problem is
                                                                       formula φ, if a Mealy machine S models [φ]atomic , then it also
undecidable for HyperTSL, but a sound approximation can
                                                                       models φ.
be achieved through HyperLTL. We then discuss how to
simplify the problem for ∀∗ formulas and present a prototype           Theorem VII.2. Let a ∀∗ HyperTSL formula and a Mealy
implementation, which successfully repairs the synthesized             machine S over AP = [TP ]atomic ∪ [TU ]atomic be given. If S
voting contract with respect to determinism, symmetry, and             models [φ]atomic , then S models φ.
the no harm property.
                                                                       Proof. For every ⟨·⟩, let S⟨·⟩ = {(ς, ι) | ∃t ∈ traces(S). t =
   The result of synthesizing the extended control flow of a                   ⟨·⟩                               ⟨·⟩
smart contract from TSL specifications is a Mealy machine as           [(ς, ι)]atomic }. By construction, [S⟨·⟩ ]atomic ⊆ traces(S). Since
depicted in Figure 3. A Mealy machine is a tuple (Q, Σ, δ, q0 ),       S |= [φ]atomic and since universal properties are downwards
                                                                                        ⟨·⟩
where Q is a set of states, Σ = 2AP with AP = AP in ∪AP  ˙             closed, [S⟨·⟩ ]atomic |= [φ]atomic and by Lemma IV.2 we have
                                                              out
is a labeling alphabet, δ : Q × Σ → Q is a transition function,        S⟨·⟩ |=⟨·⟩ φ.
and q0 is the initial state.                                              Based on this theorem, we repair the synthesized transition
Definition VII.1. A free choice in a Mealy machine                     system with respect to the corresponding HyperLTL formula.
(Q, Σ, δ, q0 ) consists of a state q ∈ Q and an input i ∈ 2AP in       To do so, we enumerate all refinements which leave exactly
such that there are at least two outputs o1 , o2 ∈ 2AP out with        one transition for each choice. Thereby, the refinement still
(q, i ∪ o1 , q1 ) ∈ δ and (q, i ∪ o2 , q2 ) ∈ δ for some q1 , q2 .     implements a strategy. Since the HyperLTL is a universal
                                                                       formula, this approach detects a correct refinement iff there
Definition VII.2. A Mealy machine Ŝ is a refinement of a              is one. Note that also with respect to HyperLTL, this cannot
Mealy machine S if Q̂ = Q, Σ̂ = Σ, qˆ0 = q0 and δ̂ ⊆ δ such            be a complete method, as ∀∗ HyperLTL synthesis is undecid-
that for every q ∈ Q, i ∈ 2AP in , if there are o ∈ 2AP out and        able [7]. The general problem of repairing HyperLTL formulas
q ′ ∈ Q such that δ(q, i ∪ o, q ′ ), then there are ô ∈ 2AP out and   has been discussed in [15], the problem is NP-complete for
qˆ′ ∈ Q̂ such that δ̂(q, i ∪ ô, qˆ′ ) and δ(q, i ∪ ô, qˆ′ ).         ∀∗ HyperLTL. An approach similar to our has been described
   The above definition ensures that if S defines a set of             for controller synthesis in [16], which distinguishes between
strategies for a TSL property ψ, then a refinement Ŝ still            controllable and uncontrollable inputs. Implementations have
describes at least one strategy for ψ. Our goal is to refine           not been developed yet.
S such that Ŝ models a HyperTSL property φ.                                   VIII. I MPLEMENTATION AND E XPERIMENTS
   The system S is produced from the LTL approximation,
                                                                          We implemented a prototype of the repair algorithm as a
it might therefore contain spurious traces which, for any
                                                                       Python script. Given a synthesized smart contract in form
interpretation, cannot be produced by a combination of an
                                                                       of a Mealy machine and a universal HyperLTL formula, the
input stream and a computation. We define when such a system
                                                                       script checks if the complete system satisfies the property. If
satisfies a HyperTSL formula.
                                                                       not, it searches for free choices, performs a self-composition,
Definition VII.3. Let φ be a HyperTSL formula over TP , TU             and checks if one of the possibilities to resolve the choices
and let S be a Mealy machine over AP = [TP ]atomic ∪                   satisfies the LTL body of the HyperLTL formula. For LTL
TABLE I: Results of the prototype implementation of the                      states symmetry with respect to the greater predicate as well as
repair algorithm. Times (t) are given in seconds. # refers to                the voteA and voteB inputs, similar to local determinism.
the number of nuXmv calls that were needed to find a repair.
                    only vote   + close      + owner            full         B. Blind Auction
Property              t     #     t   #      t     #        t           #
                                                                                As a second contract, we specified a blind auction in TSL,
Local determinism   0.170   1   0.475   1   2.577    1    7.049         1
                                                                             following [19]. Similar to the voting protocol, we had to
Local symmetry      0.229   2   1.251   6   64.90   86    308.1        120   restrict ourselves to a finite number of bidders, otherwise the
Global no harm      0.163   1   0.473   1   2.786    1    219.9        86    hyperproperties would not have been expressible in HyperTSL.
Determinism         0.147   1   0.612   1   27.63   35    6.825         1    The idea of a blind auction is that bidders send a hash of
Symmetry            0.254   2   1.630   6   29.03   35    6.571         1
                                                                             their actual bid and deposit a value which might be higher or
                                                                             lower than the actual bid. After the bidding is closed, bidders
No harm             0.170   1   0.704   1   2.993    1    90.81        35
                                                                             reveal their bids. If the hash fits the revealed bid and the
Determinism                                                                  deposited value is higher than the actual bid, the bid is valid.
+ Symmetry          0.274   3   2.105   6   217.7   256   760.4        256
+ No harm                                                                    The winner of the auction is the bidder with the highest valid
                                                                             bid. Bidders can also withdraw their deposits once a higher
                                                                             bid was revealed.
model checking we use the state-of-the-art model checker                        We specified the contract with two bidders. We use meth-
nuXmv [17]. Using our implementation, we conducted exper-                    ods bidA, bidB, closeBidding, revealA, revealB,
iments on different version of the voting contract and on a                  closeRevealing, and withdraw. One of the temporal
blinded auction contract.                                                    requirements is that bids can only be placed as long as the
                                                                             bidding has not been closed.
A. Voting Contract
   We repaired four variants of the voting protocol with respect                      (closeBidding →             ¬(bidA ∨ bidB))
to the hyperproperties described in this paper. The results
are depicted in Table I. None of the three systems initially                 The specification also reasons about fields bidsA, bidsB,
satisfies either of the properties, the number of calls given in             highestBidder, highestBid. One of the obligations on
the table therefore refers to the number of refinements tested               the fields is to update highestBid if bidder A reveals a
with nuXmv.                                                                  correct bid which is higher than all bids revealed so far.
   The first variant (“only vote”) reduces the contract to
                                                                                          (revealA ∧ valid bid secret
the core specification needed for the hyperproperties to make
sense. It has only a vote method and can be implemented as                                  ∧ bid > highestBid
a single-state system. It has two state-input combinations with                             → JhighestBid ↢ bidK)
a free choice, in each case there are two possible transitions.
The second variant (“+ close”) adds the close method and                     In the above specification, bid and secret are parameters
initial assumptions, resulting in a three-state system with four             of the method revealA. As for the voting specification, the
choices, again each with two options. The third variant (“+                  TSL specification describes the control flow of the contract,
owner”) is the contract as described in Specification 1. It has              i.e., in which order methods have to be called and how fields
eight choices. This results in 28 different combinations that                need to be updated. Other functionality like checking if a bid
might need to be checked.                                                    is valid needs to be implemented in the predicate validBid
   Lastly, we extended the voting contract with additional                   to obtain a working contract.
features following the voting example of the Solidity Docu-                     Similar to the
mentation [18]. The extended version additionally records the                voting case, we TABLE II: Repairing the blind auction
registered voters in a field voters and which addresses have                 left the free choice state machine. Times (t) are given in
voted in a field voted. The contract also has two additional                 which bid is stored seconds. # refers to the number of
methods: giveRightToVote may be called by the owner                          as highest bid if the nuXmv calls.
of the contract and adds addresses to voters; getWinner                      currently revealed
may be called after the voting has been closed to learn which                bid is the same is       Property                 t      #
candidate won. The synthesized state machine has again eight                 the current highest      Local determinism 11.13s 1
choices but is naturally larger than the state machine depicted              bid. The synthesized
in Figure 3.                                                                 state machine leaves     Local symmetry        17.42s 2
   Determinism, local determinism, symmetry, and the no harm                 free choices at two
property indicate the formulas given in Section III-C. For                   nodes. Using our implementation, we obtained strategies
symmetry, we included the necessary assumption described in                  to resolve a tie in a way that local determinism or local
Section V-B. The “global no harm” property formulates the no                 symmetry are satisfied. We report the running times and
harm property with a single instead of W . Local symmetry                    number of calls to nuXmv in Table II.
C. Evaluation                                                       range of logics have been developed for the specification of
   Our experiments show that the hyperproperties discussed in       hyperproperties. Examples are temporal logics like HyperLTL,
this paper are realizable on top of variants of a voting contract   HyperCTL∗ [8], and HyperPDL [26], first-order and second-
and a blinded auction. The evaluation shows that the runtime        order logics [27], [28], or asynchronous extensions mostly
mainly depends on the number of choice options that had to          based on HyperLTL [29]–[31]. All of the above logics are
be tested with NU X MV. The runtime also increases with larger      targeted to specify properties in the context of hardware and
formulas and larger state machines.                                 therefore assume a finite state space. Recently, the temporal
   This implementation is only a prototype to see if the idea to    logic of actions (TLA) has also been used to verify hy-
resolve free choices via repair works for relevant hyperprop-       perproperties via self-composition [32]. The synthesis from
erties. There are many options to improve performance. For          hyperproperties is known to be challenging. HyperLTL can ex-
example, one could switch to a model checker that is based on       press distributed architectures, which makes the synthesis from
Büchi or Parity automata (e.g., spot [20]). Like this, the LTL     ∀∗ properties already undecidable [7]. A simpler variant of
formula (which stays the same for every call) would have to         synthesis is controller synthesis, where the state space is given.
be translated to an automaton only once.                            Related to our approach, the resulting problem is similar to the
                                                                    repair problem and is therefore decidable for HyperLTL [16].
                    IX. R ELATED W ORK                              The classic program repair problem does not distinguish
   Our work brings together research on formal methods for          between inputs and outputs and has been studied for HyperLTL
smart contract control flows, reactive synthesis using TSL, and     as well [15]. The analysis of smart contract with respect
logics for hyperproperties.                                         to hyperproperties has not received enough attention yet. A
Formal methods for smart contract control flows. Most               recent approach uses type-checking to ensure information flow
closely related work is the recent approach to synthesize           policies such as integrity in smart contracts in the context of
the control and data flow of a smart contract from TSL              reentrancy attacks [1]. Other hyperproperties identified in the
specifications [3]. We build on the fact that they synthesize       context of smart contracts are integrity properties to prevent
the full winning region of the specification, which we refine to    reentrancy attacks [33], [34]
find a strategy that satisfies a HyperTSL specification. Another
approach to synthesize smart contract control flows is [21],                   X. C ONCLUSION AND F UTURE W ORK
which synthesizes the order of method calls from an LTL                We have presented two logics, HyperTSL and HyperTSLrel ,
specification. Formal guarantees have been also obtained by         which extend the temporal logic TSL to express hyperproper-
modeling the control flow of a contract directly with a finite      ties. Inherited from TSL, both logics express the control flow
state machine and transform the state machine to Solidity           of infinite-state systems by abstracting from concrete data with
code. In the FS OLID M framework [13] the state machine can         cells and uninterpreted functions and predicates. HyperTSLrel
be modeled in a graphical editor. A lot of work has been            predicates relate several executions, which makes the logic
invested to verify a contract against correctness properties        more expressive than HyperTSL. HyperTSL, on the other
instead of generating it automatically. The V ERI S OL [14], [22]   hand, is more suitable for synthesis tasks. We have demon-
framework checks a smart contract against properties defined        strated that both logics can express typical hyperproperties
with finite state machines. V ER X [23] and S MART P ULSE [24]      that occur in the context of smart contracts. The realizabil-
verify that a contract satisfies specifications given in LTL-like   ity problem of the universal fragment of HyperTSL can be
logics, where S MART P ULSE can handle not only safety but          approximated with HyperLTL realizability, the unrealizability
also liveness properties.                                           problem of the existential fragment can be approximated with
Temporal Stream Logic. TSL is a temporal logic that                 LTL satisfiability. As a step towards making synthesis from
has been developed to simplify reasoning about infinite-            hyperproperties reality, we have described two approaches to
state systems by separating control and data [4]. Due to its        integrate universal HyperTSL specifications in the synthesis
expressiveness, TSL synthesis is undecidable in general but         workflow of smart contracts specified with TSL. The first
sound CEGAR loops based on LTL synthesis work well in               approach checks for overly complicated specifications which
practice [4]. TSL has been successfully applied to specify and      have equivalent formulations in TSL. The second approach
synthesize an arcade shooter game running on an FPGA [5]            refines the winning region obtained from the TSL synthesis to
and functional reactive programs [6]. The TSL synthesis             resolve choices in a way that satisfy the hyperproperty.
approach has been extended with decidable theories like linear      Future work. This work has opened many interesting
integer arithmetic [11]. Here, counterexamples provided by          paths for future work. To profit from the expressiveness
the CEGAR loop are checked for consistency with the theory          of HyperTSLrel , one would have to include theories (e.g.,
using an SMT solver. TSL modulo first-order theories has also       the theory of equality) into the synthesis from HyperTSLrel
been studied with respect to its satisfiability problem [10].       specifications. Prior work has made steps in that direction for
Hyperproperties. The interest in hyperproperties, or relational     TSL [10], [11], one could extend these ideas to HyperTSLrel .
properties, stems from information flow policies like non-          Using theories, HyperTSLrel would also be interesting in the
interference and observational determinism. Since the term          context of model checking smart contracts or other infinite-
has been coined for the general class of properties [25], a         state systems. Another open question is how to approximate
the HyperTSL realizability problem for formulas with quanti-                         York City, NY, USA, July 13-14, 2019, Revised Selected Papers, ser.
fier alternations.                                                                   Lecture Notes in Computer Science, S. Chakraborty and J. A. Navas,
                                                                                     Eds., vol. 12031. Springer, 2019, pp. 87–106. [Online]. Available:
                                                                                     https://doi.org/10.1007/978-3-030-41600-3 7
                             R EFERENCES
                                                                                [15] B. Bonakdarpour and B. Finkbeiner, “Program repair for
 [1] E. Cecchetti, S. Yao, H. Ni, and A. C. Myers, “Compositional                    hyperproperties,” in Automated Technology for Verification and
     security for reentrant applications,” in 42nd IEEE Symposium on                 Analysis - 17th International Symposium, ATVA 2019, Taipei,
     Security and Privacy, SP 2021, San Francisco, CA, USA, 24-                      Taiwan, October 28-31, 2019, Proceedings, ser. Lecture Notes in
     27 May 2021. IEEE, 2021, pp. 1249–1267. [Online]. Available:                    Computer Science, Y. Chen, C. Cheng, and J. Esparza, Eds.,
     https://doi.org/10.1109/SP40001.2021.00084                                      vol. 11781. Springer, 2019, pp. 423–441. [Online]. Available:
 [2] ——, “Securing smart contracts with information flow,” in International          https://doi.org/10.1007/978-3-030-31784-3 25
     Symposium on Foundations and Applications of Blockchain, 2020.             [16] ——, “Controller synthesis for hyperproperties,” in 33rd IEEE
 [3] B. Finkbeiner, J. Hofmann, F. Kohn, and N. Passing, “Reactive                   Computer Security Foundations Symposium, CSF 2020, Boston, MA,
     synthesis of smart contract control flows,” 2022. [Online]. Available:          USA, June 22-26, 2020. IEEE, 2020, pp. 366–379. [Online]. Available:
     https://arxiv.org/abs/2205.06039                                                https://doi.org/10.1109/CSF49147.2020.00033
 [4] B. Finkbeiner, F. Klein, R. Piskac, and M. Santolucito, “Temporal          [17] R. Cavada, A. Cimatti, M. Dorigatti, A. Griggio, A. Mariotti, A. Micheli,
     Stream Logic: Synthesis Beyond the Bools,” in Computer Aided Ver-               S. Mover, M. Roveri, and S. Tonetta, “The nuxmv symbolic model
     ification - 31st International Conference, CAV 2019, New York City,             checker,” in CAV, 2014, pp. 334–342.
     NY, USA, July 15-18, 2019, Proceedings, Part I, ser. Lecture Notes in      [18] “Voting example from the solidity documentation,” https://docs.
     Computer Science, I. Dillig and S. Tasiran, Eds., vol. 11561. Springer,         soliditylang.org/en/v0.8.13/solidity-by-example.html#voting, 2022, ac-
     2019, pp. 609–629.                                                              cessed: 2022-05-12.
 [5] G. Geier, P. Heim, F. Klein, and B. Finkbeiner, “Syntroids: Synthesizing   [19] “Blind auction example from the solidity documentation,” https://docs.
     a game for fpgas using temporal logic specifications,” CoRR, vol.               soliditylang.org/en/v0.8.13/solidity-by-example.html#blind-auction,
     abs/2101.07232, 2021. [Online]. Available: https://arxiv.org/abs/2101.          2022, accessed: 2022-05-12.
     07232                                                                      [20] A. Duret-Lutz, A. Lewkowicz, A. Fauchille, T. Michaud, E. Renault, and
 [6] B. Finkbeiner, F. Klein, R. Piskac, and M. Santolucito, “Synthesizing           L. Xu, “Spot 2.0 — a framework for LTL and ω-automata manipulation,”
     functional reactive programs,” in Proceedings of the 12th ACM                   in Proceedings of the 14th International Symposium on Automated
     SIGPLAN International Symposium on Haskell, Haskell@ICFP 2019,                  Technology for Verification and Analysis (ATVA’16), ser. Lecture Notes
     Berlin, Germany, August 18-23, 2019, R. A. Eisenberg, Ed.                       in Computer Science, vol. 9938. Springer, Oct. 2016, pp. 122–129.
     ACM, 2019, pp. 162–175. [Online]. Available: https://doi.org/10.1145/      [21] D. Suvorov and V. Ulyantsev, “Smart contract design meets state
     3331545.3342601                                                                 machine synthesis: Case studies,” CoRR, vol. abs/1906.02906, 2019.
 [7] B. Finkbeiner, C. Hahn, P. Lukert, M. Stenger, and L. Tentrup,                  [Online]. Available: http://arxiv.org/abs/1906.02906
     “Synthesis from hyperproperties,” Acta Informatica, vol. 57, no.           [22] S. K. Lahiri, S. Chen, Y. Wang, and I. Dillig, “Formal specification
     1-2, pp. 137–163, 2020. [Online]. Available: https://doi.org/10.1007/           and verification of smart contracts for azure blockchain,” CoRR, vol.
     s00236-019-00358-2                                                              abs/1812.08829, 2018. [Online]. Available: http://arxiv.org/abs/1812.
 [8] M. R. Clarkson, B. Finkbeiner, M. Koleini, K. K. Micinski, M. N.                08829
     Rabe, and C. Sánchez, “Temporal logics for hyperproperties,” in
                                                                                [23] A. Permenev, D. K. Dimitrov, P. Tsankov, D. Drachsler-Cohen, and
     Principles of Security and Trust - Third International Conference,
                                                                                     M. T. Vechev, “Verx: Safety verification of smart contracts,” in 2020
     POST 2014, Held as Part of the European Joint Conferences on Theory
                                                                                     IEEE Symposium on Security and Privacy, S&P 2020, San Francisco,
     and Practice of Software, ETAPS 2014, Grenoble, France, April 5-13,
                                                                                     CA, USA, May 18-21, 2020. IEEE, 2020, pp. 1661–1677. [Online].
     2014, Proceedings, ser. Lecture Notes in Computer Science, M. Abadi
                                                                                     Available: https://doi.org/10.1109/SP40000.2020.00024
     and S. Kremer, Eds., vol. 8414. Springer, 2014, pp. 265–284. [Online].
     Available: https://doi.org/10.1007/978-3-642-54792-8 15                    [24] J. Stephens, K. Ferles, B. Mariano, S. K. Lahiri, and I. Dillig,
 [9] B. Finkbeiner, C. Hahn, P. Lukert, M. Stenger, and L. Tentrup, “Synthe-         “Smartpulse: Automated checking of temporal properties in smart
     sizing reactive systems from hyperproperties,” in Proceedings of CAV,           contracts,” in 42nd IEEE Symposium on Security and Privacy, SP 2021,
     ser. LNCS, vol. 10981. Springer, 2018, pp. 289–306.                             San Francisco, CA, USA, 24-27 May 2021. IEEE, 2021, pp. 555–571.
[10] B. Finkbeiner, P. Heim, and N. Passing, “Temporal stream logic                  [Online]. Available: https://doi.org/10.1109/SP40001.2021.00085
     modulo theories,” in Foundations of Software Science and Computation       [25] M. R. Clarkson and F. B. Schneider, “Hyperproperties,” in Proceedings
     Structures - 25th International Conference, FOSSACS 2022, Held as               of the 21st IEEE Computer Security Foundations Symposium, CSF
     Part of the European Joint Conferences on Theory and Practice of                2008, Pittsburgh, Pennsylvania, USA, 23-25 June 2008. IEEE
     Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings,            Computer Society, 2008, pp. 51–65. [Online]. Available: https:
     ser. Lecture Notes in Computer Science, P. Bouyer and L. Schröder,             //doi.org/10.1109/CSF.2008.7
     Eds., vol. 13242. Springer, 2022, pp. 325–346. [Online]. Available:        [26] J. O. Gutsfeld, M. Müller-Olm, and C. Ohrem, “Propositional
     https://doi.org/10.1007/978-3-030-99253-8 17                                    dynamic logic for hyperproperties,” in 31st International Conference
[11] B. Maderbacher and R. Bloem, “Reactive synthesis modulo theories                on Concurrency Theory, CONCUR 2020, September 1-4, 2020,
     using abstraction refinement,” CoRR, vol. abs/2108.00090, 2021.                 Vienna, Austria (Virtual Conference), ser. LIPIcs, I. Konnov and
     [Online]. Available: https://arxiv.org/abs/2108.00090                           L. Kovács, Eds., vol. 171. Schloss Dagstuhl - Leibniz-Zentrum
[12] W. Choi, B. Finkbeiner, R. Piskac, and M. Santolucito, “Can reactive            für Informatik, 2020, pp. 50:1–50:22. [Online]. Available: https:
     synthesis and syntax-guided synthesis be friends?” in PLDI ’22: 43rd            //doi.org/10.4230/LIPIcs.CONCUR.2020.50
     ACM SIGPLAN International Conference on Programming Language               [27] B. Finkbeiner and M. Zimmermann, “The first-order logic of
     Design and Implementation, San Diego, CA, USA, June 13 - 17, 2022,              hyperproperties,” CoRR, vol. abs/1610.04388, 2016. [Online]. Available:
     R. Jhala and I. Dillig, Eds. ACM, 2022, pp. 229–243. [Online].                  http://arxiv.org/abs/1610.04388
     Available: https://doi.org/10.1145/3519939.3523429                         [28] N. Coenen, B. Finkbeiner, C. Hahn, and J. Hofmann, “The
[13] A. Mavridou and A. Laszka, “Designing secure ethereum smart                     hierarchy of hyperlogics,” in 34th Annual ACM/IEEE Symposium on
     contracts: A finite state machine based approach,” in Financial                 Logic in Computer Science, LICS 2019, Vancouver, BC, Canada,
     Cryptography and Data Security - 22nd International Conference, FC              June 24-27, 2019. IEEE, 2019, pp. 1–13. [Online]. Available:
     2018, Nieuwpoort, Curaçao, February 26 - March 2, 2018, Revised                https://doi.org/10.1109/LICS.2019.8785713
     Selected Papers, ser. Lecture Notes in Computer Science, S. Meiklejohn     [29] J. Baumeister, N. Coenen, B. Bonakdarpour, B. Finkbeiner, and
     and K. Sako, Eds., vol. 10957. Springer, 2018, pp. 523–540. [Online].           C. Sánchez, “A temporal logic for asynchronous hyperproperties,” in
     Available: https://doi.org/10.1007/978-3-662-58387-6 28                         Computer Aided Verification - 33rd International Conference, CAV
[14] Y. Wang, S. K. Lahiri, S. Chen, R. Pan, I. Dillig, C. Born, I. Naseer,          2021, Virtual Event, July 20-23, 2021, Proceedings, Part I, ser.
     and K. Ferles, “Formal verification of workflow policies for smart              Lecture Notes in Computer Science, A. Silva and K. R. M. Leino,
     contracts in azure blockchain,” in Verified Software. Theories, Tools,          Eds., vol. 12759. Springer, 2021, pp. 694–717. [Online]. Available:
     and Experiments - 11th International Conference, VSTTE 2019, New                https://doi.org/10.1007/978-3-030-81685-8 33
[30] L. Bozzelli, A. Peron, and C. Sánchez, “Asynchronous extensions
     of hyperltl,” in 36th Annual ACM/IEEE Symposium on Logic
     in Computer Science, LICS 2021, Rome, Italy, June 29 - July
     2, 2021. IEEE, 2021, pp. 1–13. [Online]. Available: https:
     //doi.org/10.1109/LICS52264.2021.9470583
[31] J. O. Gutsfeld, M. Müller-Olm, and C. Ohrem, “Automata and
     fixpoints for asynchronous hyperproperties,” Proc. ACM Program.
     Lang., vol. 5, no. POPL, pp. 1–29, 2021. [Online]. Available:
     https://doi.org/10.1145/3434319
[32] L. Lamport and F. B. Schneider, “Verifying hyperproperties with
     TLA,” in 34th IEEE Computer Security Foundations Symposium, CSF
     2021, Dubrovnik, Croatia, June 21-25, 2021. IEEE, 2021, pp. 1–16.
     [Online]. Available: https://doi.org/10.1109/CSF51468.2021.00012
[33] I. Grishchenko, M. Maffei, and C. Schneidewind, “A semantic
     framework for the security analysis of ethereum smart contracts,” in
     Principles of Security and Trust - 7th International Conference, POST
     2018, Held as Part of the European Joint Conferences on Theory and
     Practice of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20,
     2018, Proceedings, ser. Lecture Notes in Computer Science, L. Bauer
     and R. Küsters, Eds., vol. 10804. Springer, 2018, pp. 243–269.
     [Online]. Available: https://doi.org/10.1007/978-3-319-89722-6 10
[34] E. Albert, S. Grossman, N. Rinetzky, C. Rodrı́guez-Núñez, A. Rubio,
     and M. Sagiv, “Taming callbacks for smart contract modularity,” Proc.
     ACM Program. Lang., vol. 4, no. OOPSLA, pp. 209:1–209:30, 2020.
     [Online]. Available: https://doi.org/10.1145/3428277
