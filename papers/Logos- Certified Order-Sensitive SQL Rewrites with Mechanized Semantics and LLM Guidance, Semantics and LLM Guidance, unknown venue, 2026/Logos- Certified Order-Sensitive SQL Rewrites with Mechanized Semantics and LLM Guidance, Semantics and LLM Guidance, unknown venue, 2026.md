                                         Logos: Certified Order-Sensitive SQL Rewrites with Mechanized
                                                          Semantics and LLM Guidance
                                                               Jingyu Ke                                               Jingyang Li                                 Guoqiang Li
                                                  Shanghai Jiao Tong University                            Shanghai Jiao Tong University                 Shanghai Jiao Tong University
                                                        Shanghai, China                                          Shanghai, China                               Shanghai, China
                                                    Windocotber@sjtu.edu.cn                                     lijjjjj@sjtu.edu.cn                            li.g@sjtu.edu.cn

                                         ABSTRACT                                                                               widely used open-source applications [27]. Deploying such rewrites
                                         SQL rewrite verification must account for duplicate rows, observ-                      requires establishing semantic equivalence between the original
                                         able row order, and typed value semantics. Existing verifiers have                     and rewritten queries. Specifically, the two queries must have the
                                         yet to combine proofs over database instances of arbitrary finite                      same observable behavior on every schema-conforming finite data-
                                         cardinality with an ordered-list semantics for nested, tie-sensitive                   base instance, without any preset bound on relation cardinality.
                                         top-𝑘. Unbounded systems reason primarily over bags or handle                          Testing can refute this obligation by finding a counterexample, but
                                         ordering through syntax-directed restrictions, whereas bounded                         it cannot establish it. This gap is increasingly consequential as
                                         systems either support only restricted top-𝑘 forms or impose a deter-                  optimizers combine hand-written rules, workload-derived transfor-
                                         ministic ordering rather than retain all legal tie-induced outcomes.                   mations, and LLM-generated rewrites; recent industrial evidence
arXiv:2608.15709v1 [cs.DB] 16 Aug 2026




                                         Support for typed expression and aggregate semantics, observable                       shows that realistic query pairs remain beyond the coverage of
                                         runtime errors, and integrity constraints also remains partial.                        current equivalence checkers [16].
                                            In Rocq, we mechanize a compositional logical semantics for a                          The central semantic challenge arises from the interaction be-
                                         typed SQL core with order-sensitive operators, capturing all possi-                    tween bag semantics and order-sensitive operators. Some relational
                                         ble ordered lists and observable SQL failures in the supported frag-                   arguments are permutation-invariant and admit concise multiplic-
                                         ment. To our knowledge, this is the first mechanized SQL semantics                     ity proofs. In contrast, ORDER BY establishes order, whereas slicing
                                         to combine nested, tie-sensitive top-𝑘 with a closure-based lifting                    and window operators can consume row positions. Globally quoti-
                                         from bag equivalence to ordered-list equivalence, enabling sound                       enting intermediate results by permutation therefore erases behav-
                                         reuse of bag-theoretic reasoning while preserving compositionality                     ior observable to nested, tie-sensitive top-𝑘, whereas assigning each
                                         across order-sensitive and correlated contexts. The formalization                      operator one fixed output list invents an execution order that SQL
                                         further provides executable semantics for PostgreSQL-oriented                          leaves unspecified. Retaining all legal ordered lists preserves this
                                         scalar and aggregate evaluation and an explicit account of integrity                   behavior, but introduces a substantial proof burden: even routine
                                         constraints. Building on this semantics, we present Logos, an LLM-                     query-specific equivalence arguments require nontrivial structural
                                         guided Rocq verifier for unbounded SQL rewrite equivalence. Its                        induction over lists, often coupled with explicit permutation reason-
                                         agent uses a verified SQL-specific lemma library to construct query-                   ing [7, 9]. Sound verification also requires concrete semantics for
                                         specific Rocq proofs. Our evaluation covers 389 query pairs from                       typed scalar and aggregate evaluation, including observable failures,
                                         Apache Calcite optimizer tests, TPC-H and TPC-DS rewrites, and                         together with a formal account of integrity constraints. Modeling
                                         WeTune’s real-application workloads. Logos solves 86.9% of them,                       scalar and aggregate operations as uninterpreted functions overap-
                                         compared with 64.0% for SQLSolver, the strongest baseline.                             proximates their behavior and can admit spurious counterexamples
                                                                                                                                that cannot arise under concrete SQL semantics.
                                         PVLDB Reference Format:                                                                   Existing unbounded verifiers obtain much of their power from
                                         Jingyu Ke, Jingyang Li, and Guoqiang Li. Logos: Certified Order-Sensitive              bag semantics and algebraic normalization [7, 9, 12, 26]. Support
                                         SQL Rewrites with Mechanized Semantics and LLM Guidance. PVLDB,                        for ordered fragments is typically syntax-directed, requiring syn-
                                         20(1): XXX-XXX, 2027.                                                                  tactic alignment of corresponding order-sensitive operators. Con-
                                         doi:XX.XX/XXX.XX                                                                       versely, list encodings can cover richer SQL but have so far provided
                                                                                                                                bounded guarantees for restricted order-sensitive fragments [13].
                                         1    INTRODUCTION                                                                      The missing connection is not another global choice between lists
                                         Query rewriting is a central technique for improving database per-                     and bags. A verifier needs a semantics that retains every possible
                                         formance [17]. Reported application cases include a 100× speedup                       result order, together with a checked criterion for using bag theory
                                         for an individual query and a 3.7× reduction in production workload                    at a particular subquery.
                                         latency [2, 22]. Recent rewriting systems have also uncovered hun-                        We present Logos, a proof-producing verifier that realizes this
                                         dreds of optimization opportunities missed by existing DBMSs in                        criterion. Its semantic foundation is FormalSQL, our order-sensitive
                                                                                                                                extension of SQLCoq [5], mechanized in Rocq. The extension pro-
                                         This work is licensed under the Creative Commons BY-NC-ND 4.0 International            vides a compositional logical semantics for a typed SQL core with
                                         License. Visit https://creativecommons.org/licenses/by-nc-nd/4.0/ to view a copy of    order-sensitive operators, together with executable, PostgreSQL-
                                         this license. For any use beyond those covered by this license, obtain permission by
                                         emailing info@vldb.org. Copyright is held by the owner/author(s). Publication rights   oriented value and error interpretations for the supported frag-
                                         licensed to the VLDB Endowment.                                                        ment. Rather than selecting one implementation-dependent result,
                                         Proceedings of the VLDB Endowment, Vol. 20, No. 1 ISSN 2150-8097.
                                         doi:XX.XX/XXX.XX
                                                                                                                                FormalSQL assigns each query a relation containing all possible
                                                                                                               ----- Source Query -----
ordered row lists and observable SQL failures in this fragment. Ap-           SELECT *
                                                                              FROM users
plying the order-forgetting map to every successful result yields             WHERE active IS TRUE
the query’s bag projection, which preserves multiplicities while                AND users.id IN (
                                                                                  SELECT user_id
discarding order. The projection may contain multiple distinct bags,              FROM group_users
for example when top-𝑘 cuts through a tie. We identify a semantic                 WHERE group_id = 8861)
                                                                              LIMIT 20;
closure condition under which two sets of legal ordered lists are
equivalent exactly when their bag projections are equal. At such a                                             ----- Target Query -----
                                                                              SELECT users.*
boundary, standard multiplicity arguments can be used locally and             FROM users
then lifted through the surrounding order-sensitive context.                  INNER JOIN group_users
                                                                                ON group_users.user_id = users.id
    Logos then performs LLM-guided counterexample search. If the              WHERE active IS TRUE
model predicts non-equivalence, it must propose a concrete, schema-             AND group_users.group_id = 8861
                                                                              LIMIT 20;
conforming database instance. A pair of differing executions on that
instance does not in general establish non-equivalence. When SQL
does not determine a unique order, an engine produces only one                Figure 1: A real-world Discourse rewrite from the WeTune
of several legal ordered lists; the observed choice may depend on             benchmark that replaces an IN membership test with a join.
optimizer-selected scan and join plans and physical storage order,
while the relative order of rows tied on every ordering expres-
sion remains implementation-dependent. Row-limiting operators
can turn this freedom into different selected subsets [18]. For a                     supported PostgreSQL fragment into fixed Rocq verification
proof-producing non-equivalence result, Logos therefore reifies                       goals and combines LLM-guided synthesis of equivalence
the candidate as a fixed, typed FormalSQL database instance and                       proofs and certified countermodels with a reusable SQL
requires the proof agent to establish a countermodel against the                      lemma library and domain-specific Rocq automation. Every
complete outcome relations. The proof exhibits a legal outcome on                     resulting certificate is checked in isolation by the Rocq
one side that no legal outcome on the other can match.                                kernel.
    Likewise, when the model predicts equivalence, Logos requires                   • We evaluate Logos against state-of-the-art SQL equiva-
the proof agent to establish the fixed Rocq equivalence theorem over                  lence verifiers on a diverse suite of optimizer, decision-
all schema-conforming database instances. Building on FormalSQL,                      support, and real-application benchmarks, including Cal-
we provide a library of verified lemmas covering general structural                   cite, the TPC decision-support suites, and WeTune. Lo-
properties and common operator interactions. The library keeps                        gos solves 86.9% of the query pairs, exceeding the best-
the agent from reproving these reusable facts and concentrates                        performing baseline, SQLSolver (64.0%), by 22.9 percentage
its effort on the semantic interactions and feature combinations                      points. These results show that mechanized SQL seman-
specific to each query pair.                                                          tics combined with LLM-guided proof search substantially
    We evaluate Logos on 389 query pairs spanning Calcite, the TPC                    broadens the practical coverage of proof-producing equiva-
decision-support suites, and WeTune. Logos solves 86.9% of the                        lence verification.
pairs, improving over the strongest baseline, SQLSolver (64.0%), by
22.9 percentage points. On the order-sensitive subset, it solves 73.1%,       2    OVERVIEW
compared with 41.3% for the strongest baseline on that subset. These
results show that explicit treatment of order and lemma-guided                    Figure 1 shows a real-world Discourse rewrite from the We-
proof synthesis extend proof-producing verification to substantially          Tune benchmark [27]. The source selects active users whose iden-
broader SQL feature combinations.                                             tifiers occur among the members of group 8861. The target re-
    This paper makes three contributions:                                     places this membership test with an inner join. The schema de-
                                                                              clares (group_id, user_id) unique in group_users, so a fixed group
     • We extend FormalSQL with a mechanized, compositional se-               contributes at most one matching membership row per user. Both
       mantics for a typed SQL core with order-sensitive operators.           queries then retain at most 20 rows without specifying an order.
       Each query denotes all possible ordered lists and observ-                  Consider a database in which the relevant rows are summarized
       able SQL failures in the supported fragment. The formaliza-            below. The symbols 𝑢 1, . . . , 𝑢 21 stand for distinct complete rows of
       tion provides executable Rocq semantics for PostgreSQL-                users.
       oriented scalar and aggregate evaluation. This includes                            User rows             active   Membership in group 8861
       NULL-sensitive evaluation and PostgreSQL numeric and
                                                                                          𝑢 1 , . . . , 𝑢 21    TRUE     one row per user
       temporal types (e.g., DECIMAL and TIMESTAMPTZ), with all                           𝑣                     FALSE    one row
       supported failures explicit. To our knowledge, this is the                         𝑤                     TRUE     none
       first mechanized SQL semantics to combine nested, tie-
       sensitive top-𝑘 with a closure-based lifting from bag equiv-           Before applying limit, the source core retains exactly 𝑢 1, . . . , 𝑢 21 :
       alence to ordered-list equivalence while preserving compo-             the inactive row 𝑣 fails the first predicate, and 𝑤 fails the member-
       sitionality across order-sensitive and correlated contexts.            ship test. The target core reaches the same rows through the join.
     • We implement Logos as a proof-producing prototype for                  Uniqueness is essential here; it ensures that the join emits each 𝑢𝑖
       SQL equivalence verification. It lowers query pairs in its             once rather than multiplying it by several matching membership
                                                                          2
rows. Thus, immediately before limit, the two query cores pro-                    3.1    Notation and Typed Core Syntax
duce the same bag of 21 user rows with the same multiplicities and                Let 𝜏 range over the supported SQL types, V𝜏 over their non-NULL
modeled failures.                                                                 values, and V𝜏⊥ = V𝜏 ⊎{NULL𝜏 } over their nullable values. A typed
   At this boundary, neither core establishes an order. Every per-                attribute 𝑎 : 𝜏 associates the column identifier 𝑎 with its SQL type
mutation of the 21 rows is therefore a legal result, but all of these             𝜏. Write 𝑣 1 ≈𝜏 𝑣 2 when two nullable values agree in the typed SQL
ordered lists have the same underlying bag. The collection of possi-              value model; in particular, NULL𝜏 ≈𝜏 NULL𝜏 . An ordered relation
ble bags consequently has one member before limit.                                signature 𝜎 = (𝑎 1 : 𝜏1, . . . , 𝑎𝑚 : 𝜏𝑚 ) is a finite sequence of typed
   The limit makes the distinction observable. Because any 𝑢𝑖 may                 attributes with distinct identifiers and fixes both column order and
occur last, taking the first 20 rows can omit any one of the 21                   types, with
users. The complete query therefore has 21 possible result bags,                                         V𝜎 = V𝜏⊥1 × · · · × V𝜏⊥𝑚 .                     (1)
each containing a different 20-user subset. Logos records these
                                                                                  Thus, V𝜎 is the domain of well-typed row values conforming to
alternatives separately instead of selecting one engine-dependent
                                                                                  𝜎, and 𝑟 ∈ V𝜎 denotes a particular row value. The 𝑖th component
order or combining the alternatives into a single bag.
                                                                                  of 𝑟 is a nullable value of type 𝜏𝑖 ; for 𝑎𝑖 : 𝜏𝑖 ∈ 𝜎, write 𝑟 [𝑎𝑖 ] for
   Preserving this set of alternatives is necessary for equivalence
                                                                                  this component. Rows satisfy 𝑟 1 ≈𝜎 𝑟 2 when their corresponding
reasoning, especially when the query is embedded as a subquery.
                                                                                  components are related by the appropriate ≈𝜏 .
Replacing the 21 possible bags by one arbitrarily selected bag would
make the comparison depend on that choice: two equivalent queries                 Definition 1 (Finite bag). For a set 𝑋 , a finite bag over 𝑋 is a
could be assigned different 20-row bags even though they admit                    function 𝐵 : 𝑋 → N whose support {𝑥 ∈ 𝑋 | 𝐵(𝑥) > 0} is finite;
the same complete set of alternatives. The resulting loss of corre-               𝐵(𝑥) is the multiplicity of 𝑥. We write Bag(𝑋 ) for the set of finite
spondence could cause equivalent queries to be reported as non-                   bags over 𝑋 . When 𝑋 carries a semantic equivalence ≈𝑋 , let #𝐵 (𝑥)
equivalent, and the discrepancy could propagate through the en-                   count all occurrences in 𝐵 equivalent to 𝑥, and write 𝐵 1 =B 𝐵 2 when
closing query.                                                                    #𝐵1 (𝑥) = #𝐵2 (𝑥) for every 𝑥 ∈ 𝑋 .
   Logos makes these alternatives explicit. Write 𝐵 21 for the bag that
contains each of 𝑢 1, . . . , 𝑢 21 once. On the database above, its compact       Definition 2 (Finite list). For a set 𝑋 , the set of all finite lists over
summary of the possible bags at the two relevant boundaries is                    𝑋 is
                                                                                    List(𝑋 ) ≜ {[𝑥 1, . . . , 𝑥𝑛 ] | 𝑛 ∈ N ∧ ∀𝑖 ∈ {1, . . . , 𝑛}. 𝑥𝑖 ∈ 𝑋 }. (2)
    before limit: {𝐵 21 },    after limit: {𝐵 21 \ {𝑢𝑖 } | 1 ≤ 𝑖 ≤ 21},
                                                                                  The case 𝑛 = 0 is the empty list [ ]; equivalently, finite lists are
where subtraction removes the single occurrence of 𝑢𝑖 . The first set             generated by ℓ ::= [ ] | 𝑥 :: ℓ for 𝑥 ∈ 𝑋 . Positions and repeated
says that all legal core results share one bag; the second keeps the 21           occurrences are retained. A list ℓ = [𝑥 1, . . . , 𝑥𝑛 ] induces bag(ℓ) ∈
alternatives created when limit observes their positions. This bag                Bag(𝑋 ) by counting occurrences. Thus bag forgets order but retains
summary is not itself the query semantics. Logos retains ordered                  multiplicity; we write {{𝑥 1, . . . , 𝑥𝑛 }} for the resulting bag. For 𝐵 ∈
row sequences as its successful outcomes and keeps modeled SQL                    Bag(𝑋 ), write Rows(𝐵, ℓ) when bag(ℓ) =B 𝐵.
errors as separate outcomes. It forgets order only at a local proof
                                                                                  Definition 3 (Schema and schema contract). A schema Σ maps
boundary, without merging distinct possible bags.
                                                                                  each relation name 𝑅 to an ordered relation signature Σ(𝑅). A
   To verify the rewrite, Logos first proves that the two cores pro-
                                                                                  schema contract Γ is a finite set of integrity constraints over the
duce the same 𝐵 21 . It then establishes that both cores are bag closed:
                                                                                  relations and attributes declared by Σ.
every ordering of 𝐵 21 is legal. These facts allow the local bag proof
to recover equality of all ordered core outcomes, as formalized in                Definition 4 (Finite database). A finite database 𝐷 over Σ maps
Section 3.3. Semantic congruence then carries this equality through               each declared relation 𝑅 to 𝐷 (𝑅) ∈ Bag(VΣ(𝑅) ). We write 𝐷 |=
the common limit and, when present, through any enclosing query.                  (Σ, Γ) when 𝐷 satisfies every constraint in Γ.
Consequently, the complete queries preserve precisely the same 21
                                                                                      Figure 2 presents the typed core syntax used by Logos. It covers
possible bags above, while genuine errors remain visible throughout
                                                                                  the supported SQL query expressions, scalar expressions, predi-
the query context.
                                                                                  cates, and the integrity constraints admitted by schema contracts.
                                                                                  The metavariables 𝑓 and 𝜃 range over the supported typed scalar
3     FORMAL SEMANTICS AND SEMANTIC                                               and predicate operators, 𝑛 ∈ N, and 𝜑 row is a well-typed, subquery-
      DECOMPOSITION                                                               free predicate in the scope of its declared relation. The list 𝑊 =
The formal development of Logos is grounded in an ordered-list se-                [𝑤 1, . . . , 𝑤𝑢 ] contains typed window outputs 𝑤 = (𝑎 : 𝜏,𝜓 ), where
mantics of query execution, from which bag reasoning is derived as                𝜓 is row number, a cumulative aggregate over the current partition
a controlled abstraction. Section 3.1 fixes the notation used through-            prefix, or an aggregate over the complete partition. The correspond-
out the paper and presents the typed core syntax of our supported                 ing semantics supports common aggregate functions and typed
SQL fragment. Section 3.2 gives this syntax an error-aware exe-                   scalar operators over the modeled SQL types.
cution semantics and defines the resulting verification objective.                    The query-expression category 𝑄 begins with two constant rela-
Section 3.3 then establishes the closure conditions under which bag               tions. Empty(𝜎) denotes the empty relation of signature 𝜎, whereas
equivalence can be lifted to ordered outcome equivalence and com-                 Singleton denotes the relation of empty signature () whose sole row
posed with surrounding operators. Finally, Section 3.4 instantiates               is the empty tuple ⟨⟩. The latter supplies a unit input from which
the development on the running example from Section 2.                            extended projection can construct a concrete row. Since Project
                                                                              3
                                      Query Expressions                                                                                    Scalar Expressions
      𝑄 ::= Empty(𝜎 )                                     No rows of signature 𝜎                     𝑉 ::= 𝑐 : 𝜏 | 𝑎 : 𝜏                                     Typed literal or attribute
          | Singleton                                     One empty row of signature ()                  | 𝛼𝜔 (𝑉 ) : 𝜏                                       Aggregate application
          | Table(𝑅)                                      Base relation 𝑅                                | 𝑓 (𝑉1 , . . . , 𝑉𝑟 ) : 𝜏                          Scalar application
          | Set(OP set , 𝑄 1 , 𝑄 2 )                      Order-insensitive bag operation                | Case(𝑃, 𝑉1 , 𝑉2 ) : 𝜏                             Lazy case
          | CrossJoin(𝑄 1 , 𝑄 2 )                         Cartesian product                              | Subquery(𝑄 ) : 𝜏                                  Scalar subquery
          | Join(OP join , 𝑃, 𝑄 1 , 𝑄 2 )                 Outer/semi/anti join on 𝑃
          | Project(𝐿, 𝑄 )                                Order-preserving projection                𝛼 ::= Count | Sum | Avg | Min | Max | · · · Aggregate operator
          | Filter(𝑃, 𝑄 )                                 Three-valued selection                     𝜔 ::= All | Distinct                        Aggregate duplicate policy
          | Distinct(𝑄 )                                  Duplicate elimination                      𝑓 ::= + | − | × | ÷ | Cast | Concat | · · · Scalar operator
          | Group(𝐿, 𝐺, 𝑃, 𝑄 )                            Grouped aggregation with having                                                      Predicates
          | GroupingSets( G, 𝑄 )                          Shared-input grouping-set branches
                                                                                                      𝑃 ::= True                                             Truth constant
          | Rank(𝐾𝑝 , 𝐾, 𝑎 rank : BIGINT, 𝑄 )             rank window
                                                                                                          | 𝜃 (𝑉1 , . . . , 𝑉𝑟 )                             Scalar predicate
          | Window(𝐾𝑝 , 𝐾,𝑊 , 𝑄 )                         Shared window evaluation
                                                                                                          | Not(𝑃 )                                          Three-valued negation
          | OrderBy(𝐾, 𝑄 )                                Constrain output order
                                                                                                          | And( [𝑃1 , . . . , 𝑃ℎ ] )                        SQL conjunction
          | Offset(𝑛, 𝑄 )                                 Drop first 𝑛 rows
                                                                                                          | Or( [𝑃1 , . . . , 𝑃ℎ ] )                         SQL disjunction
          | Fetch(𝑛, 𝑄 )                                  Keep first 𝑛 rows
                                                                                                          | In( (𝑉1 , . . . , 𝑉𝑟 ), 𝑄 )                      Tuple membership
      𝜎 ::= (𝑎 1 :𝜏1 , . . . , 𝑎𝑚 :𝜏𝑚 )                   Ordered relation signature                      | Exists(𝑄 )                                       Query nonemptiness
      𝐿 ::= [ (𝑉1 , 𝑎 1 :𝜏1 ), . . . , (𝑉𝑘 , 𝑎𝑘 :𝜏𝑘 ) ]   Projection list
      𝐺 ::= [𝑉1 , . . . , 𝑉𝑔 ]                            Grouping expressions                                                            Integrity Constraints
      G ::= [ (𝐿1 , 𝐺 1 ), . . . , (𝐿𝑠 , 𝐺𝑠 ) ]           Nonempty grouping-set branch list          𝐶 ::= NotNull(𝑅, [𝑎 1 , . . . , 𝑎ℎ ] )                  Nullability constraint
 𝐾𝑝 , 𝐾 ::= [𝜅 1 , . . . , 𝜅𝑟 ]                           Partition/order specification                  | PrimaryKey(𝑅, [𝑎 1 , . . . , 𝑎ℎ ] )               Primary key
      𝜅 ::= (𝑎 :𝜏, 𝛿, 𝜈 )                                 Typed sort key                                 | Unique(𝑅, [𝑎 1 , . . . , 𝑎ℎ ] )                   Unique key
      𝛿 ::= Asc | Desc                                    Sort direction                                 | ForeignKey 𝑅, [𝑎 1 , . . . , 𝑎ℎ ],
       𝜈 ::= First | Last                                 NULL placement                                       𝑅 ′ , [𝑏 1 , . . . , 𝑏ℎ ]                     Foreign key
 OP set ::= Union | Intersect | Except                    ALL-mode bag-operation kind                    | Check(𝑅, 𝜑 row )                                 Row-local check
 OP join ::= Left | Right | Full | Semi | Anti            Join kind                                      | UniqueIndex 𝑅, [𝑉1 , . . . , 𝑉𝑢 ], 𝜑 row          Expression/partial unique index


                                                   Figure 2: Typed core syntax for queries and integrity constraints.


evaluates its list once for each input row, Singleton makes that                                      An SQL program state is a pair
evaluation occur exactly once. For example,                                                                                                  Ω = (𝐷, 𝜌),                                  (3)
                                                         
         Project [(1 : INTEGER, 𝑥 : INTEGER)], Singleton                                           where 𝐷 is the finite database and 𝜌 = 𝛽 0 :: · · · :: 𝛽𝑘 :: 𝜖 is a list
                                                                                                   of visible row and group bindings, with the head 𝛽 0 denoting the
has signature (𝑥 : INTEGER) and contains the single row ⟨1⟩; it is the
                                                                                                   innermost scope. The top-level environment is 𝜖, and an extension
core representation of the single-row table constructor VALUES (1).
                                                                                                   prepends its new binding to 𝜌.
Bag union of such terms represents a multirow VALUES constructor.
   The remaining query constructors cover the relational and order-
                                                                                                      Binding resolution. For a well-scoped typed attribute 𝑎 : 𝜏, define
sensitive operators listed in Figure 2. Section 3.2 assigns them
                                                                                                   𝑖 = min{ 𝑗 | 𝑎 : 𝜏 ∈ 𝜎𝛽 𝑗 ∧ ℓ𝛽 𝑗 ≠ [ ]}. If ℓ𝛽𝑖 = 𝑟 :: ℓ ′ , then
ordered-list semantics and specifies how modeled errors propa-
                                                                                                   resolve𝜌 (𝑎) = 𝑟 [𝑎]. Thus, resolution searches from the list head
gate from demanded subterms. The core set operators are the all
                                                                                                   (the stack top) toward the outer bindings and returns the value
variants with bag multiplicities; surface distinct variants are nor-
                                                                                                   from the first row of the nearest nonempty binding in which the
malized into these operators and Distinct. Within this syntax, inner
                                                                                                   attribute is visible. Attribute evaluation is given by
joins are represented by filtering a cross join, because the separate
Join constructor is reserved for outer, semi, and anti joins.                                                              resolve𝜌 (𝑎) = 𝑣
                                                                                                                                                            (Attribute)
                                                                                                                         (𝐷, 𝜌) ⊢ 𝑎 : 𝜏 ⇓ ok(𝑣)
3.2      Error-Aware Execution Semantics and                                                       A row binding supplies values to scalar expressions and predicates;
         Equivalence                                                                               a group binding additionally supplies the rows consumed by ag-
Query execution depends on more than the database contents. A                                      gregate expressions. Subqueries inherit the current binding list, so
subquery may refer to row and group bindings supplied by its                                       an attribute not resolved by the innermost binding may refer to an
surrounding context, while unordered inputs and unresolved sort                                    enclosing one, as required for correlated subqueries.
ties may admit multiple ordered lists. We first formalize the SQL                                     Let B3 = {T, F, U} and let Err be the domain of modeled SQL
program state that makes these dependencies explicit.                                              failures. Lowercase 𝑞 ranges over well-typed terms generated by
                                                                                                   𝑄, while 𝑉 and 𝑃 range over the corresponding scalar and pred-
Definition 5 (SQL program state). An SQL binding is a triple                                       icate terms. We write Ω ⊢ 𝑞 ⇓ ok(ℓ) when executing query 𝑞 in
𝛽 = (𝜎𝛽 , 𝑚 𝛽 , ℓ𝛽 ), where 𝜎𝛽 is its row signature, 𝑚 𝛽 is either Row                             program state Ω may return the ordered row list ℓ ∈ List(V𝜎 ),
or Group(𝐺), and ℓ𝛽 ∈ List(V𝜎𝛽 ). A row binding induced by 𝑟 ∈                                     and write Ω ⊢ 𝑞 ⇓ err(𝑒) when it may instead fail with 𝑒 ∈ Err.
V𝜎 is row𝜎 (𝑟 ) = (𝜎, Row, [𝑟 ]); a group binding stores in ℓ𝛽 all                                 The symbol ⇓ is relational: the same query may derive multiple
rows consumed by aggregate expressions. For 𝑔 ∈ List(V𝜎 ), write                                   ordered-list outcomes. Analogously, Ω ⊢ 𝑉 ⇓ ok(𝑣) returns 𝑣 ∈ V𝜏⊥ ,
gbind𝜎,𝐺 (𝑔) = (𝜎, Group(𝐺), 𝑔).                                                                   and Ω ⊢ 𝑃 ⇓ ok(𝑏) returns 𝑏 ∈ B3 ; either judgment may instead
                                                                                               4
                      Ω ⊢ Empty(𝜎 ) ⇓ ok( [ ] )          ( Empty )                                                    Ω ⊢ 𝑞 ⇓ ok(ℓ0 )
                                                                                                                Rows(distinctB (bag(ℓ0 ) ), ℓ )
                                                                                                                                                           ( Distinct )
                   Ω ⊢ Singleton ⇓ ok( [ ⟨ ⟩ ] )       ( Singleton )                                              Ω ⊢ Distinct(𝑞) ⇓ ok(ℓ )

                           Rows(𝐷 (𝑅), ℓ )                                                                    Ω ⊢ 𝑞 1 ⇓ ok(ℓ1 )     Ω ⊢ 𝑞 2 ⇓ ok(ℓ2 )
                                                        ( Table )
                        Ω ⊢ Table(𝑅) ⇓ ok(ℓ )                                                                  Ω ⊢ joinB𝑗,𝑃 (bag(ℓ1 ), bag(ℓ2 ) ) ⇓ 𝑜
                                                                                                                                                                  ( Join )
                                                                                                                     Ω ⊢ Join( 𝑗, 𝑃, 𝑞 1 , 𝑞 2 ) ⇓ 𝑜
                 Ω ⊢ 𝑞 1 ⇓ ok(ℓ1 )   Ω ⊢ 𝑞 2 ⇓ ok(ℓ2 )
                  Rows(setBop (bag(ℓ1 ), bag(ℓ2 ) ), ℓ )                                                      Ω ⊢ 𝑞 1 ⇓ ok(ℓ1 )    Ω ⊢ 𝑞 2 ⇓ ok(ℓ2 )
                                                                     ( Set )
                      Ω ⊢ Set(op, 𝑞 1 , 𝑞 2 ) ⇓ ok(ℓ )                                                            Rows(bag(ℓ1 ) ⊗ bag(ℓ2 ), ℓ )
                                                                                                                                                                 ( Cross )
                                                                                                                 Ω ⊢ CrossJoin(𝑞 1 , 𝑞 2 ) ⇓ ok(ℓ )

             Ω ⊢ 𝑞 ⇓ ok(ℓ )    Ω ⊢ project𝐿 (ℓ ) ⇓ 𝑜                                                         Ω ⊢ 𝑞 ⇓ ok(ℓ )     Ω ⊢ filter𝑃 (ℓ ) ⇓ 𝑜
                                                                ( Project )                                                                                    ( Filter )
                     Ω ⊢ Project(𝐿, 𝑞) ⇓ 𝑜                                                                           Ω ⊢ Filter(𝑃, 𝑞) ⇓ 𝑜


                                                         ( Proj-Nil )                                                                                  ( Filter-Nil )
                   Ω ⊢ project𝐿 ( [ ] ) ⇓ ok( [ ] )                                                              Ω ⊢ filter𝑃 ( [ ] ) ⇓ ok( [ ] )

                       Ω[𝑟 ] ⊢ 𝐿 ⇓ err(𝑒 )                                                                          Ω[𝑟 ] ⊢ 𝑃 ⇓ err(𝑒 )
                                                          ( Proj-Err )                                                                                 ( Filter-Err )
                  Ω ⊢ project𝐿 (𝑟 :: ℓ ) ⇓ err(𝑒 )                                                              Ω ⊢ filter𝑃 (𝑟 :: ℓ ) ⇓ err(𝑒 )

          Ω[𝑟 ] ⊢ 𝐿 ⇓ ok(𝑟 ′ )     Ω ⊢ project𝐿 (ℓ ) ⇓ 𝑜                                                Ω[𝑟 ] ⊢ 𝑃 ⇓ ok(𝑏 )       Ω ⊢ filter𝑃 (ℓ ) ⇓ 𝑜
                                                                    ( Proj-Cons )                                                                             ( Filter-Cons )
               Ω ⊢ project𝐿 (𝑟 :: ℓ ) ⇓ cons(𝑟 ′ , 𝑜 )                                                     Ω ⊢ filter𝑃 (𝑟 :: ℓ ) ⇓ keep(𝑏, 𝑟, 𝑜 )

            Ω ⊢ 𝑞 ⇓ ok(ℓ0 )   GroupsΩ,𝐺 (bag(ℓ0 ), Π)                                                Ω ⊢ 𝑞 ⇓ ok(ℓ0 )   Rows(bag(ℓ0 ), ℓ )   sorted𝐾 (ℓ )
                                                                                                                                                                          ( Order )
                  Ω ⊢ groups𝐿,𝐺,𝑃 (Π) ⇓ ok(ℓ𝑔 )                                                                  Ω ⊢ OrderBy(𝐾, 𝑞) ⇓ ok(ℓ )
                        Rows(bag(ℓ𝑔 ), ℓ )
                                                                       ( Group )
                  Ω ⊢ Group(𝐿, 𝐺, 𝑃, 𝑞) ⇓ ok(ℓ )                                                                        Ω ⊢ 𝑞 ⇓ ok(ℓ )
                                                                                                                                                             ( Offset )
                                                                                                               Ω ⊢ Offset(𝑛, 𝑞) ⇓ ok(drop𝑛 (ℓ ) )
                        Ω ⊢ 𝑞 ⇓ err(𝑒 )
                                                    ( Unary-Err )
                      Ω ⊢ 𝑈 (𝑞) ⇓ err(𝑒 )                                                                               Ω ⊢ 𝑞 ⇓ ok(ℓ )
                                                                                                                                                             ( Fetch )
                                                                                                                Ω ⊢ Fetch(𝑛, 𝑞) ⇓ ok(take𝑛 (ℓ ) )
                        Ω ⊢ 𝑞 1 ⇓ err(𝑒 )
                                                      ( Left-Err )                                         Ω ⊢ 𝑞 1 ⇓ ok(ℓ1 )        Ω ⊢ 𝑞 2 ⇓ err(𝑒 )
                     Ω ⊢ 𝐵 (𝑞 1 , 𝑞 2 ) ⇓ err(𝑒 )                                                                                                            ( Right-Err )
                                                                                                                  Ω ⊢ 𝐵 (𝑞 1 , 𝑞 2 ) ⇓ err(𝑒 )

Figure 3: Big-step ordered-list semantic rules for part of the core query language. Here 𝑈 and 𝐵 range over well-typed unary
and left-to-right binary query constructors. All metavariables are implicitly quantified over well-typed objects; in Group, Π
ranges over lists of row groups and ℓ𝑔 over lists of rows produced from those groups. The auxiliary judgments are explained in
Section 3.2.


return err(𝑒). Scalar calls use their concrete typed interpretations,                             Auxiliary judgments. Figure 3 defines the big-step semantics for
predicates use SQL three-valued logic, and Case executes only its                             most of the well-typed SQL query expressions introduced in Fig-
selected branch. A scalar subquery returns its sole value, returns                            ure 2.1 We next explain the auxiliary judgments and relations used
a typed null on an empty result, and raises a cardinality error on                            in these rules. The superscript B marks an auxiliary relation that
multiple rows. The In judgment applies SQL three-valued existen-                              treats successful query inputs as bags: the enclosing rule replaces
tial comparison, while Exists observes nonemptiness and evaluates                             each child list ℓ by bag(ℓ), thereby discarding positions while re-
only the subterms needed to determine it; both preserve errors from                           taining multiplicities. The auxiliary relation operates on these bags
demanded subterms.                                                                            and produces a result bag 𝐵, which represents every ordered list
   Let 𝑄 𝜎 denote the well-typed query terms with output signature                            ℓ ′ satisfying Rows(𝐵, ℓ ′ ); errors are propagated unchanged. This
𝜎, and write O𝜎 for the semantic domain of their results:                                     convention keeps the displayed judgments in the common result
                                                                                              domain O𝜎 .
        O𝜎 = {ok(ℓ) | ℓ ∈ List(V𝜎 )} ⊎ {err(𝑒) | 𝑒 ∈ Err}.                                        For Ω = (𝐷, 𝜌) and 𝑟 ∈ V𝜎 , define

For a fixed database 𝐷 and binding list 𝜌, query semantics is the                                                       Ω[𝑟 ] = (𝐷, row𝜎 (𝑟 ) :: 𝜌),
set-valued map E𝐷,𝜌 : 𝑄 𝜎 → P (O𝜎 ), defined by                                               which makes 𝑟 the innermost visible row. This extension is used
                                                                                              whenever an auxiliary judgment evaluates an expression against
                E𝐷,𝜌 (𝑞) = {𝑜 ∈ O𝜎 | (𝐷, 𝜌) ⊢ 𝑞 ⇓ 𝑜}.                               (4)       one input row.
Thus, a query denotes its complete relation of legal ordered lists                            1 The complete typing and semantic definitions, including the rules omitted from
and observable failures, rather than one execution selected by an                             Figure 3, are available in the FormalSQL mechanization at https://github.com/
engine.                                                                                       WindOctober/FormalSQL.
                                                                                          5
   Bag-level auxiliary relations. Recall that Rows(𝐵, ℓ) makes ℓ an                              Ω[𝑟 ] ⊢ 𝑉𝑗 ⇓ ok(𝑣 𝑗 ) (1 ≤ 𝑗 ≤ 𝑘)
                                                                                                                                              (List-Ok)
arbitrary ordered representative of the bag 𝐵. The operation setBop                             Ω[𝑟 ] ⊢ 𝐿 ⇓ ok(⟨𝑎 1 = 𝑣 1, . . . , 𝑎𝑘 = 𝑣𝑘 ⟩)
                                                                                                Ω[𝑟 ]⊢𝑉 𝑗 ⇓ok(𝑣 𝑗 )
applies the SQL bag operation designated by op; for example, the                                     1≤ 𝑗 <𝑖     Ω[𝑟 ] ⊢ 𝑉𝑖 ⇓ err(𝑒)
union all case adds multiplicities:                                                                                                  (List-Err)
                                                                                                       Ω[𝑟 ] ⊢ 𝐿 ⇓ err(𝑒)
                  #setB                   (𝑟 ) = #𝐵1 (𝑟 ) + #𝐵2 (𝑟 ).                 For 𝑟 ∈ V𝜎 and 𝑜 ∈ O𝜎 , projection and filtering use the following
                      Union (𝐵 1 ,𝐵 2 )
                                                                                      combinators:
The operator distinctB assigns multiplicity one to every semantic                                                 (
                                                                                                                    ok(𝑟 :: ℓ), 𝑜 = ok(ℓ),
row class occurring in its input bag. For rows 𝑟𝑖 ∈ V𝜎𝑖 with disjoint                               cons(𝑟, 𝑜) =
attributes, let 𝑟 1 ∥ 𝑟 2 be their concatenation, of signature 𝜎1 ∥ 𝜎2 .                                            err(𝑒),     𝑜 = err(𝑒),
                                                                                                                  (
The bag product satisfies                                                                                           cons(𝑟, 𝑜), 𝑏 = T,
                                                                                                  keep(𝑏, 𝑟, 𝑜) =
                    #𝐵1 ⊗𝐵2 (𝑟 1 ∥ 𝑟 2 ) = #𝐵1 (𝑟 1 )#𝐵2 (𝑟 2 ).                                                   𝑜,            𝑏 ∈ {F, U}.
   The auxiliary join judgment joinB𝑗,𝑃 (𝐵 1, 𝐵 2 ) first evaluates 𝑃 on              Projection consequently emits one row for each input position,
each candidate 𝑟 1 ∥ 𝑟 2 under the corresponding row binding. A                       whereas filtering returns a stable subsequence. Both judgments
pair matches exactly when this evaluation returns T; F and U do                       preserve the first error encountered in a demanded row.
not match, and an error is propagated. The join kind 𝑗 then de-                          A sort specification 𝐾 = [𝜅 1, . . . , 𝜅𝑠 ] is a lexicographic list of
termines the result: left, right, and full joins add their respective                 keys 𝜅 = (𝑎 : 𝜏, 𝛿, 𝜈), where 𝛿 chooses ascending or descending
null-extended unmatched rows, while semi and anti joins retain a                      comparison and 𝜈 places nulls first or last. Write 𝑟 ⪯𝐾 𝑟 ′ when the
left row according to whether a match exists. The auxiliary judg-                     first key on which 𝑟 and 𝑟 ′ differ orders 𝑟 before 𝑟 ′ (or all keys tie).
ment then admits every ordered representative of the resulting                        Then
bag.                                                                                          sorted𝐾 ([𝑟 1, . . . , 𝑟𝑚 ])   ⇐⇒    ∀𝑖 < 𝑚. 𝑟𝑖 ⪯𝐾 𝑟𝑖+1 .
   Grouping illustrates how a compound operator is defined at
                                                                                      Together, Rows(bag(ℓ0 ), ℓ) and sorted𝐾 (ℓ) state that ℓ is a 𝐾-sorted
this boundary. Recall from Figure 2 that 𝐺 = [𝑉1, . . . , 𝑉𝑠 ] is a well-
                                                                                      permutation of the input occurrences; no order is imposed between
typed list of scalar expressions. Let 𝜎𝐺 be its induced ordered result
                                                                                      rows that tie on all keys. For ℓ = [𝑟 1, . . . , 𝑟𝑚 ], the positional opera-
signature. Evaluating 𝐺 under Ω[𝑟 ] assembles a key row 𝑘 ∈ V𝜎𝐺 ,
                                                                                      tors are
written Ω[𝑟 ] ⊢ 𝐺 ⇓ ok(𝑘). The grouping relation has signature                                           take𝑛 (ℓ) = [𝑟 1, . . . , 𝑟 min(𝑛,𝑚) ],
               GroupsΩ,𝐺 ⊆ Bag(V𝜎 ) × List(List(V𝜎 )).                                                   drop𝑛 (ℓ) = [𝑟 min(𝑛,𝑚)+1, . . . , 𝑟𝑚 ].
To derive GroupsΩ,𝐺 (𝐵, Π), choose an ordered representative ℓ =                      Here an empty index interval denotes [ ].
[𝑟 1, . . . , 𝑟𝑛 ] of 𝐵 and evaluate one key row for each occurrence:                     The rules in Figure 3 expose the order boundary directly. Projec-
                                     Û                                                tion and filtering transform one selected child list without reorder-
                   Rows(𝐵, ℓ),           Ω[𝑟𝑖 ] ⊢ 𝐺 ⇓ ok(𝑘𝑖 ).                        ing it. Table scans, bag operations, and the auxiliary judgments for
                                          1≤𝑖 ≤𝑛                                      joins and grouping do not preserve child positions; they directly ad-
Rows whose key rows are related by ≈𝜎𝐺 belong to the same group.                      mit their legal ordered outputs. Sorting admits every bag-preserving
Taking the first occurrence of each key as its representative gives                   list satisfying 𝐾, so ties remain nondeterministic, whereas offset
                   h
                                         1≤𝑖 ≤𝑛,
                                                     i                                and fetch consume concrete positions.
             Π = [𝑟𝑡 | 𝑘𝑡 ≈𝜎𝐺 𝑘𝑖 ] ¬∃ℎ<𝑖. 𝑘ℎ ≈𝜎𝐺 𝑘𝑖 .                                     For any outcome relation 𝐸 ⊆ O𝜎 , define
Both comprehensions range over input positions in increasing order,                       Succ(𝐸) = {ℓ | ok(ℓ) ∈ 𝐸},          Errs(𝐸) = {𝑒 | err(𝑒) ∈ 𝐸}.
so duplicates are retained and first-occurrence order is preserved.
                                                                                      Definition 6 (Observation and outcome equivalence). Using the
The SQL global-group convention is GroupsΩ,[ ] (∅, [[ ]]).
                                                                                      typed value and row equivalences from Section 3.1, write ℓ1 ≈L
   For Ω = (𝐷, 𝜌) and 𝑔 ∈ List(V𝜎 ), write
                                                                                      ℓ2 when two lists have equal length and their rows are related
                    Ω⟨𝐺, 𝑔⟩ = (𝐷, gbind𝜎,𝐺 (𝑔) :: 𝜌).                                 positionwise by ≈𝜎 . Two sets of legal lists match in both directions
The judgment Ω ⊢ groups𝐿,𝐺,𝑃 (Π) ⇓ 𝑜 processes each 𝑔 ∈ Π under                       when
Ω⟨𝐺, 𝑔⟩. It first finalizes the aggregate applications required by 𝐿                          𝑂 1 ≡L 𝑂 2 ⇔ (∀ℓ1 ∈ 𝑂 1 . ∃ℓ2 ∈ 𝑂 2 . ℓ1 ≈L ℓ2 ) ∧
                                                                                                                                                         (5)
and 𝑃, then evaluates 𝑃 as having. On success it produces                                                       (∀ℓ2 ∈ 𝑂 2 . ∃ℓ1 ∈ 𝑂 1 . ℓ1 ≈L ℓ2 ).

 ℓ𝑔 = 𝑟𝑔 | 𝑔 ← Π, Ω⟨𝐺, 𝑔⟩ ⊢ 𝑃 ⇓ ok(T), Ω⟨𝐺, 𝑔⟩ ⊢ 𝐿 ⇓ ok(𝑟𝑔 ) .
                                                                                    For full outcome relations over one signature, define
                                                                                                    𝐸 1 ≡out 𝐸 2 ⇔ 𝐸 1 ≠ ∅ ∧ 𝐸 2 ≠ ∅
Thus F and U discard a group, while demanded failures are propa-
                                                                                                                   ∧ Succ(𝐸 1 ) ≡L Succ(𝐸 2 )                 (6)
gated.
                                                                                                                   ∧ Errs(𝐸 1 ) = Errs(𝐸 2 ).
   Order-aware list operations. The order-sensitive auxiliary op-                     An outcome relation is safe when it contains at least one successful
erations act on concrete list positions. Recall from Figure 2 that                    result and no failure:
𝐿 = [(𝑉1, 𝑎 1 : 𝜏1 ), . . . , (𝑉𝑘 , 𝑎𝑘 : 𝜏𝑘 )]. Its left-to-right evaluation is
specified by the following rule schemes:                                                            Safe(𝐸) ⇔ Succ(𝐸) ≠ ∅ ∧ Errs(𝐸) = ∅.
                                                                                      Safe outcome equivalence is therefore
                                                     (List-Nil)                               𝐸 1 ≡safe 𝐸 2 ⇔ 𝐸 1 ≡out 𝐸 2 ∧ Safe(𝐸 1 ) ∧ Safe(𝐸 2 ).
                     Ω[𝑟 ] ⊢ [ ] ⇓ ok(⟨⟩)                                                                                                                     (7)
                                                                                  6
The inhabitedness conditions exclude vacuous equivalence of mal-                     Indeed, the lists have the same length and pair equivalent rows at
formed relations; an equivalence certificate must establish at least                 every position, so each row-equivalence class has the same multi-
one legal outcome on each side. Successful results never match                       plicity.
errors, and distinct modeled failures remain distinguishable.                           For the forward direction, assume 𝐸 1 ≡out 𝐸 2 . Equation (6) im-
                                                                                     mediately gives
   Schema conformance is part of the semantic premise. Constraints
in Γ are interpreted over the same nullable values and three-valued                                  Errs(𝐸 1 ) = Errs(𝐸 2 ),      𝑂 1 ≡L 𝑂 2 .
predicates as query execution; row predicates and expression-index                   Let 𝐵 ∈ Bags(𝑂 1 ). By Equation (11),
terms must also evaluate without error when their constraint re-
quires them. The complete satisfaction relation is mechanized in                                             ∃ℓ1 ∈ 𝑂 1 . bag(ℓ1 ) =B 𝐵.
the FormalSQL development cited above.                                               Forward list matching then supplies an ℓ2 ∈ 𝑂 2 such that
Definition 7 (Query equivalence contracts). For query terms 𝑞 1                                        (∗)
                                                                                             ℓ1 ≈L ℓ2 =⇒ bag(ℓ1 ) =B bag(ℓ2 ) =⇒ 𝐵 ∈ Bags(𝑂 2 ),
and 𝑞 2 with the same output signature, the default verification
contract is unconditional, error-preserving equivalence:                             where the last implication also uses symmetry and transitivity of
                                                                                     =B . Thus Bags(𝑂 1 ) ⊆ Bags(𝑂 2 ). The backward matching clause
  (Σ, Γ) |= 𝑞 1 ≡ 𝑞 2 ⇔ ∀𝐷 |= (Σ, Γ). E𝐷,𝜖 (𝑞 1 ) ≡out E𝐷,𝜖 (𝑞 2 ).        (8)       gives the reverse inclusion, and hence Bags(𝑂 1 ) = Bags(𝑂 2 ).
Safe equivalence additionally requires both queries to have at least                    Conversely, assume equality of the two bag projections and of
one successful outcome and no error on any conforming database:                      the two error sets. For any ℓ1 ∈ 𝑂 1 , reflexivity of =B and equality
                                                                                     of the projections give
 (Σ, Γ) |= 𝑞 1 ≡safe 𝑞 2 ⇔ ∀𝐷 |= (Σ, Γ). E𝐷,𝜖 (𝑞 1 ) ≡safe E𝐷,𝜖 (𝑞 2 ).
                                                                           (9)                  ℓ1 ∈ 𝑂 1 =⇒ bag(ℓ1 ) ∈ Bags(𝑂 1 ) = Bags(𝑂 2 ).

   Conditional extension. A well-typed precondition Φ restricts ei-                  Since 𝑂 2 is closed, Definition 8 now supplies
ther contract to databases that satisfy it. For the default error-                                             ∃ℓ2 ∈ 𝑂 2 . ℓ1 ≈L ℓ2 .
preserving contract, this gives
                                                                                     Thus every observation in 𝑂 1 has a matching observation in 𝑂 2 .
           ∀𝐷 |= (Σ, Γ). Φ(𝐷) ⇒ E𝐷,𝜖 (𝑞 1 ) ≡out E𝐷,𝜖 (𝑞 2 ).             (10)       Applying the same argument with the sides reversed and using
The safe conditional variant replaces ≡out with ≡safe . In either case,              closure of 𝑂 1 gives
the certificate must establish that Φ either follows from the input                                               𝑂 1 ≡L 𝑂 2 .
contract or is jointly satisfiable with it. Every database quantifier                Finally, the assumed inhabitedness of 𝐸 1 and 𝐸 2 , together with
ranges over arbitrary finite cardinalities. Failed proof search reports              error-set equality, discharges all clauses of Equation (6).     □
unknown; it does not weaken any of these contracts.
   The outcome relation remains the specification at every query                        This closure property arises throughout the core query language.
boundary. The next section characterizes when its successful or-                     In fact, let
dered lists may be replaced locally by possible bags.                                               R = {Empty, Singleton, Table, Set,
                                                                                                         CrossJoin, Join, Distinct, Group,
3.3     Lifting Bag Equivalence to Ordered-List                                                          GroupingSets, Rank, Window}.
        Equivalence                                                                  We define the syntactic certificate as
Fix an output signature 𝜎 and let 𝑂 ⊆ List(V𝜎 ) be a relation of                                   (
                                                                                                     true, the outer constructor of 𝑞 is in R,
successful ordered observations. Its order-forgetting projection is                      cert(𝑞) =                                                       (14)
                                                                                                     false, otherwise.
               Bags(𝑂) = {𝐵 | ∃ℓ ∈ 𝑂. bag(ℓ) =B 𝐵}.                       (11)
                                                                                       Theorem 10 (Closure-certificate soundness). For every ad-
Definition 8 (Bag closure). 𝑂 is bag closed, written Closed(𝑂),                      mitted 𝑞,
when                                                                                                                                       
                                                                                             cert(𝑞) = true =⇒ ∀𝐷, 𝜌. Closed Succ(E𝐷,𝜌 (𝑞)) . (15)
      ∀ℓreq . bag(ℓreq ) ∈ Bags(𝑂) =⇒ ∃ℓobs ∈ 𝑂. ℓreq ≈L ℓobs .           (12)
                                                                                         Proof sketch. Inspect the execution rule for each constructor
  The following theorem is the central lifting result: at bag-closed                 in R. Its successful result does not fix the order of the returned row
boundaries, equality of possible bags and failures characterizes                     list: once one list represents the computed bag, every permutation of
outcome equivalence over ordered lists.                                              that list is also admitted. Hence its successful observations contain
  Theorem 9 (Bag-to-list lifting). Let 𝐸 1 and 𝐸 2 be inhabited                      every ordering of each possible result bag, which is precisely the
outcome relations over the same signature, and let 𝑂𝑖 = Succ(𝐸𝑖 ). If                closure property in Definition 8.                                    □
Closed(𝑂 1 ) and Closed(𝑂 2 ), then
                                                                                        In contrast, Project and Filter preserve the order selected by
 𝐸 1 ≡out 𝐸 2 ⇔ Bags(𝑂 1 ) = Bags(𝑂 2 ) ∧ Errs(𝐸 1 ) = Errs(𝐸 2 ). (13)              their child rather than reset it: applied to [𝑟 1, 𝑟 2 ], they retain the
                                                                                     corresponding projected or retained rows in that order, without
   Proof. First observe that position-wise list equivalence pre-
                                                                                     independently admitting the reverse order. Establishing closure
serves row multiplicities:
                                                                                     for either operator therefore requires additional premises about
                   ℓ1 ≈L ℓ2 =⇒ bag(ℓ1 ) =B bag(ℓ2 ).                       (∗)       its child and row-level expressions. A failed certificate leaves the
                                                                                 7
ordered-list semantics unchanged and does not authorize forgetting                 on their well-typed row bindings. Uniformly in 𝐷 and 𝜌, we obtain
order.                                                                                     Bags(Succ(E𝐷,𝜌 (𝐶 src ))) = Bags(Succ(E𝐷,𝜌 (𝐶 tgt ))),
   Once Theorem 9 recovers outcome equivalence at a bag-closed                                                                                       (19)
                                                                                                 Errs(E𝐷,𝜌 (𝐶 src )) = Errs(E𝐷,𝜌 (𝐶 tgt )) = ∅.
boundary, semantic congruence permits an outcome-equivalent
child to be replaced inside an enclosing operator. For Fetch, the                      The successful observations of both cores are bag closed. For
property used below is                                                             𝐶 src , the table scan admits every input permutation, the filters act
                                                                                   pointwise, and In depends on membership in 𝐼 rather than the order
        E𝐷,𝜌 (𝑞 1 ) ≡out E𝐷,𝜌 (𝑞 2 )                                               of its rows. For 𝐶 tgt , CrossJoin resets order, after which pointwise
          =⇒ E𝐷,𝜌 (Fetch(𝑛, 𝑞 1 )) ≡out E𝐷,𝜌 (Fetch(𝑛, 𝑞 2 )).                     filtering and projection commute with permutations. The closure
It follows because take𝑛 preserves position-wise list equivalence                  lemmas of Section 3.3 therefore give
and Fetch propagates child errors unchanged. FormalSQL mech-
                                                                                                                                                  
                                                                                      Closed Succ(E𝐷,𝜌 (𝐶 src )) ,       Closed Succ(E𝐷,𝜌 (𝐶 tgt )) . (20)
anizes the analogous congruence lemmas for query, scalar, and
predicate contexts.                                                                The outcome relations are inhabited, so Theorem 9, together with
                                                                                   Equations (19) and (20), yields
3.4    Formalizing the Running Example                                                                    E𝐷,𝜌 (𝐶 src ) ≡out E𝐷,𝜌 (𝐶 tgt ).          (21)
We now instantiate the preceding results for the rewrite in Figure 1.              Applying this Fetch property to Equation (21) gives outcome equiv-
Fix a schema Σ containing users and group_users. Let 𝐿𝑈 be the                     alence for 𝑆 and 𝑇 . On the 21-user instance from Section 2, this
complete typed projection list for users. The following well-typed                 gives the same 21 possible 20-row bags on both sides.
core predicates are obtained by lowering the corresponding SQL
conditions:                                                                           Theorem 11 (Rewrite eqivalence). Under the schema contract
                                                                                   (Σ, Γ) above,
      • 𝑃𝐴 := users.active IS TRUE;
                                                                                                          (Σ, Γ) |= 𝑆 ≡ 𝑇 .                 (22)
      • 𝑃𝐺 := group_users.group_id = 8861; and
      • 𝑃 𝐽 := users.id = group_users.user_id.                                       Proof. Fix 𝐷 |= (Σ, Γ). Instantiating Equation (21) at 𝜌 = 𝜖 and
The two query cores and their enclosing limits are                                 applying the Fetch property above gives
            𝑈 = Filter(𝑃𝐴 , Table(users)),                                                                   E𝐷,𝜖 (𝑆) ≡out E𝐷,𝜖 (𝑇 ).
            𝑀 = Filter(𝑃𝐺 , Table(group_users)),                                   The claim follows from Definition 7, since 𝐷 was arbitrary and 𝑆,𝑇
             𝐼 = Project([user_id], 𝑀),                                            have the same output signature.                                  □
                                                                        (16)
          𝐶 src = Filter(In((id), 𝐼 ), 𝑈 ),
                                                                                   4    IMPLEMENTATION
          𝐶 tgt = Project(𝐿𝑈 , Filter(𝑃 𝐽 , CrossJoin(𝑈 , 𝑀))),
                                                                                   Logos2 comprises a typed SQL frontend, the FormalSQL Rocq li-
             𝑆 = Fetch(20, 𝐶 src ),       𝑇 = Fetch(20, 𝐶 tgt ).                   brary, and an untrusted proof-search loop. SQLGlot translates the
Here LIMIT 20 lowers to Fetch(20, ·) without an OrderBy, and                       declared input dialect to Calcite-compatible SQL [15]; Calcite re-
hence consumes an unconstrained child order. Assume that Γ con-                    solves types and operators [4]; and the Rust frontend lowers Cal-
tains the benchmark’s NOT-NULL declarations, the primary key                       cite’s intermediate representation to the Rocq representation of the
on users.id, and a unique key on the group_users attribute pair                    typed core shown in Figure 2.
(group_id, user_id).                                                                  In Rocq, we refactor and extend SQLCoq [5] into FormalSQL,
   Fix 𝐷 |= (Σ, Γ) and a binding list 𝜌, and write Ω = (𝐷, 𝜌). For                 an order-sensitive semantic library. FormalSQL mechanizes the
each of 𝑈 , 𝑀, 𝐶 src , and 𝐶 tgt , all successful observations differ only         complete execution and error semantics underlying Figure 3 and
in order; write 𝐵𝑈 , 𝐵𝑀 , 𝐵 src , and 𝐵 tgt for their respective underly-          provides the bridge between bag and ordered-list equivalence devel-
ing result bags. For a user row 𝑢, define the number of matching                   oped in Section 3.3. Its library contains over 2,000 verified lemmas.
membership occurrences by                                                          They primarily support three parts of verification: compositional
                ∑︁                                                                 query rewrites, such as merging adjacent projections; reasoning
                          #𝐵𝑀 (𝑚) · 1 Ω[𝑢 ∥ 𝑚] ⊢ 𝑃 𝐽 ⇓ ok(T) . (17)
                                                                
   𝑁 (𝑢) =                                                                         about scalar and grouped expressions under schema constraints,
            𝑚∈supp(𝐵𝑀 )                                                            such as proving two scalar expressions equivalent in their respec-
                                                                                   tive typed theories; and semantic lifting, such as transporting local
The indicator is one exactly when 𝑃 𝐽 evaluates to T under the joined
                                                                                   equivalence proofs across query constructors and enclosing con-
row binding for 𝑢 and 𝑚, and zero otherwise. The source retains
                                                                                   texts while preserving errors and observable order.
each occurrence of 𝑢 iff 𝑁 (𝑢) > 0, whereas the target produces
                                                                                      For each input SQL query pair, Logos generates a Rocq veri-
one projected occurrence for every match. Their multiplicities are
                                                                                   fication task that formalizes its schema constraints, queries, and
therefore
                                                                                   equivalence statement under FormalSQL semantics. It then invokes
 #𝐵src (𝑢) = #𝐵𝑈 (𝑢)1[𝑁 (𝑢) > 0],             #𝐵tgt (𝑢) = #𝐵𝑈 (𝑢)𝑁 (𝑢). (18)       a proof agent, which determines whether to prove equivalence or
                                                                                   establish non-equivalence. To focus the agent on proof construc-
Since 𝑀 restricts group_id to 8861, the unique key gives 𝑁 (𝑢) ∈                   tion rather than repository navigation, Logos provides a compact
{0, 1}. Equation (18) thus establishes equal multiplicities for every
user row. Moreover, all scalar operations in 𝑃𝐴 , 𝑃𝐺 , and 𝑃 𝐽 are total           2 https://github.com/WindOctober/Logos

                                                                               8
                                   Table 1: Composition and input-query characteristics of the 389 benchmark pairs.

                        Corpus                                   Input-query structure (P50/P90)                                                  Pairs containing feature (%)
Benchmark                                    Schemas            Query                    Join                    Agg./            Subq.               Set         Outer        Order/
family                         Pairs          (tables)         operators              occurrences                dist.            (corr.)             ops          join         slice         Top-𝑘         Window
Literature [13]                   30         24 (1–4)             6/9                       1/2                  50%           13.3% (0%)           13.3%           0%            0%            0%              0%
Calcite [4, 13]                  236           1 (6)              6/10                      1/2                 42.4%          11% (2.5%)           10.2%         26.7%         7.6%            3%             0.8%
R-Bot TPC-H [22, 24]              22           1 (8)             12/18                      1/5                 100%          45.5% (27.3%)          0%           4.5%          100%          100%              0%
R-Bot DSB [11, 22]                37           1 (25)            22/50                     6/11                 97.3%         35.1% (21.6%)         18.9%         10.8%         94.6%         75.7%             0%
TPC-DS variants [25]              14           1 (25)           34.5/72                    5/15                 100%          28.6% (14.3%)         92.9%         28.6%         100%          100%            35.7%
WeTune [27]                       50        7 (22–332)          9.5/17                      1/3                  44%           72% (26%)             26%           28%           30%           20%              0%
Schemas (tables) reports distinct schemas and the range of table counts. The query operators metric counts projections, scans, joins, filters, aggregation or duplicate elimination, set operations, ordering/slicing,
windows, and VALUES. Nested queries are included, with each CTE definition counted once. The join occurrences metric counts explicit joins and comma-separated FROM items. Pair-level P50/P90 use the larger
query. Feature percentages count a pair when either query contains the feature; shading shows prevalence, and columns may overlap. Agg./dist. covers aggregation, grouping, and duplicate elimination;
parentheses under Subq. report correlated subqueries. Top-𝑘 counts LIMIT/FETCH, but not OFFSET alone.



FormalSQL semantic context together with semantic indexes for                                                   and the TPC-DS variants instead supply substantially larger analyt-
the lemma library.                                                                                              ical queries, with P90 operator counts of 50 and 72 and join counts
   Non-equivalence cannot in general be certified merely by gener-                                              of 11 and 15. TPC-DS also provides the broadest feature interac-
ating a database instance and executing it in a deterministic engine                                            tions: every pair combines aggregation, ordering, and top-𝑘, while
such as PostgreSQL [18]. FormalSQL may assign a query a set of                                                  92.9% contain set operations and 35.7% contain windows. Thus, the
possible ordered-list results, whereas one concrete execution ob-                                               corpus progresses from localized optimizer rewrites to feature-rich
serves only a single result. Logos therefore accepts non-equivalence                                            analytical workloads and tests order sensitivity in composition with
only through a countermodel checked against the complete For-                                                   other SQL operators.
malSQL semantics or an observable mismatch between the queries’
output signatures.                                                                                                Environment. We run all experiments on a Linux server with an
                                                                                                               AMD Ryzen 9 5950X CPU (16 cores and 32 hardware threads) and
                                                                                                               128 GB of memory. Every tool receives a 14,400-second wall-clock
5     EVALUATION                                                                                               budget and a 16 GB memory limit per query pair, and we report
We evaluate Logos on 389 query pairs from six benchmark families                                               per-case end-to-end time rather than campaign makespan. Logos
and compare it with three unbounded SQL verifiers. Our evaluation                                              uses the gpt-5.6-sol proof agent at medium reasoning effort and
addresses two questions:                                                                                       permits at most three counterexample rounds. Each proof-agent
                                                                                                               sandbox is limited to 6 GB of memory and 2 GB of writable storage;
       • RQ1 (Effectiveness): How does the verification coverage                                               proof search and trusted Rocq checking are capped at 14,100 and
         of Logos compare with existing verifiers?                                                             420 seconds, respectively.
       • RQ2 (Efficiency): What is the runtime of Logos, and where
         are its main performance bottlenecks?                                                                     Baselines. We compare Logos with three unbounded SQL equiv-
                                                                                                                alence verifiers using their original implementations:

5.1      Experimental Setup                                                                                              • Cosette uses Rosette, a solver-aided language embedded in
                                                                                                                           Racket [23], for bounded counterexample search, and Coq
    Benchmarks. Our corpus combines six complementary bench-                                                               for checked proofs over K-relations and UniNomials [8].
mark families. The Literature family contains 30 standard-SQL                                                            • SQLSolver reduces U-expressions with unbounded summa-
query pairs from VeriEQL’s Literature benchmark [13], while Cal-                                                           tions to an extension of linear integer arithmetic discharged
cite contains 236 pairs derived from Apache Calcite optimizer                                                              by SMT solvers [12].
tests [4, 13]. The R-Bot TPC-H and R-Bot DSB families contain                                                            • QED normalizes queries into a sum-product normal form
22 and 37 decision-support query pairs, respectively. For these fam-                                                       and proves equality through stabilization and recursive
ilies, we generate each target reproducibly by applying a single                                                           unification, using SMT solvers for first-order side condi-
rewrite with a pinned version of R-Bot’s Calcite rewrite engine [22].                                                      tions [26].
They are therefore deterministic rewrite workloads rather than un-
published LLM outputs from the R-Bot study. The TPC-DS variants                                                    Cosette requires its dedicated DSL, whereas SQLSolver and QED
family pairs 14 official base templates with their corresponding                                                accept Calcite-compatible SQL subsets. Since the benchmark fami-
variants. Finally, WeTune contributes 50 before/after rewrites taken                                            lies span several source dialects, we build tool-specific materializa-
from commits in seven open-source applications [27].                                                            tion adapters on SQLGlot to translate each case’s declared dialect
    Table 1 shows that corpus complexity is multidimensional. Litera-                                           into the corresponding schema and query pair. This lets every veri-
ture and Calcite account for 266 of the 389 pairs, but their individual                                         fier run through its intended frontend.
queries are relatively small: their P90 sizes are 9 and 10 operators,
respectively, with two join occurrences in both families. WeTune                                                5.2       RQ1: Comparison with Existing Verifiers
shifts the stress to application context: its seven schemas contain                                            Table 2 reports coverage by benchmark family. Across the full cor-
22–332 tables, and 72% of its pairs contain subqueries. R-Bot DSB                                              pus, Logos solves 338 pairs (86.9%), compared with 249 (64.0%) for
                                                                                                          9
                             Table 2: Comparison of automated SQL equivalence verifiers by benchmark family.

Benchmark family   Pairs                   Logos                                  SQLSolver                                                                      QED                                               Cosette

                             Solved      Timeout      Unsupported     Solved      Timeout           Unsupported                                    Solved      Timeout     Unsupported          Solved         Timeout          Unsupported

Literature           30    28 (93.3%)     2 (6.7%)      0 (0.0%)     23 (76.7%)    0 (0.0%)          7 (23.3%)                                    16 (53.3%)   0 (0.0%)      14 (46.7%)       14 (46.7%)       0 (0.0%)          16 (53.3%)
Calcite             236    227 (96.2%)    9 (3.8%)      0 (0.0%)    183 (77.5%)    1 (0.4%)          52 (22.0%)                                  156 (66.1%)   0 (0.0%)      80 (33.9%)       36 (15.3%)       0 (0.0%)         200 (84.7%)
R-Bot TPC-H          22    16 (72.7%)    6 (27.3%)      0 (0.0%)    16 (72.7%)     0 (0.0%)          6 (27.3%)                                    5 (22.7%)    0 (0.0%)      17 (77.3%)        0 (0.0%)        0 (0.0%)         22 (100.0%)
R-Bot DSB            37    24 (64.9%)    12 (32.4%)     1 (2.7%)     9 (24.3%)    14 (37.8%)         14 (37.8%)                                   19 (51.4%)   0 (0.0%)      18 (48.6%)        0 (0.0%)        0 (0.0%)         37 (100.0%)
TPC-DS variants      14     9 (64.3%)    5 (35.7%)      0 (0.0%)     3 (21.4%)    4 (28.6%)          7 (50.0%)                                    2 (14.3%)    0 (0.0%)      12 (85.7%)        0 (0.0%)        0 (0.0%)         14 (100.0%)
WeTune               50    34 (68.0%)    13 (26.0%)     3 (6.0%)     15 (30.0%)    3 (6.0%)          32 (64.0%)                                   15 (30.0%)   0 (0.0%)      35 (70.0%)        0 (0.0%)        0 (0.0%)         50 (100.0%)

Aggregate           389    338 (86.9%)   47 (12.1%)     4 (1.0%)    249 (64.0%)   22 (5.7%)         118 (30.3%)                                  213 (54.8%)   0 (0.0%)      176 (45.2%)      50 (12.9%)       0 (0.0%)         339 (87.1%)



                                                                                                                                                                Cumulative Runtime Across Solved Cases
SQLSolver, the strongest baseline—an improvement of 22.9 percent-
                                                                                                                                                   Logos
age points. Logos attains the highest solved count on every family,                                                                                SQLSolver
                                                                                                                                       96h         QED
tying SQLSolver only on R-Bot TPC-H. The advantage grows on                                                                            48h
                                                                                                                                                   Cosette




                                                                                                      Cumulative runtime (log scale)
                                                                                                                                       24h
the 104 order-sensitive pairs identified by Table 1: Logos solves 76
                                                                                                                                        4h
(73.1%), whereas SQLSolver solves 43 (41.3%), QED 35 (33.7%), and
                                                                                                                                        1h
Cosette 5 (4.8%). Thus the aggregate improvement is not obtained
solely from the predominantly unordered Calcite family.                                                                                10m


    Examining the solved-case intersections, Logos solves 72 cases                                                                     1m
that no other evaluated verifier solves, compared with 13 for SQL-
                                                                                                                                       10s
Solver, four for QED, and none for Cosette. The baseline portfolio
collectively covers another six cases through the overlap of SQL-                                                                       1s

Solver and QED, so its total contribution beyond Logos is 23 cases.                                                                          0           50        100          150          200             250          300          350
                                                                                                                                                                     Case rank, sorted by per-tool runtime
    Verification coverage also depends on whether a tool can carry
a case through its input and semantic interfaces. Table 2 uses Un-
supported for non-definite outcomes other than timeouts, including                                   Figure 4: Cumulative runtime on solved cases, sorted by each
syntax and lowering failures, model or prover limitations, and solver                                tool’s per-case wall-clock time.
errors. Only four Logos cases (1.0%) fall into this category, com-
pared with 118 (30.3%) for SQLSolver, 176 (45.2%) for QED, and 339
(87.1%) for Cosette. Thus, Logos carries 99.0% of the corpus either                                  arise from isolated frontend and formalization gaps; we analyze the
to a definite result or into proof search, even when that search                                     much larger set of timeouts, together with the resulting optimiza-
eventually exhausts its budget.                                                                      tion opportunities, in RQ2.
    The cross-tool intersections show that this broader support trans-
lates into verified results. Of the 118 pairs unsupported by SQL-                                                     Answer to RQ1. Logos provides the greatest coverage overall
Solver, Logos solves 94 (79.7%); another 20 reach proof search but                                                    and in every benchmark family, solving 22.9 percentage points
time out. Conversely, among the 108 pairs solved by Logos but not                                                     more pairs than the strongest unbounded baseline while leaving
by SQLSolver, 94 (87.0%) lie outside SQLSolver’s supported frag-                                                      only 1.0% of the corpus unsupported. Its advantage is particularly
ment, while only 14 are SQLSolver timeouts. The principal gain is                                                     pronounced for order-sensitive pairs, where it improves the
therefore semantic reach rather than merely a stronger decision                                                       solved rate from 41.3% to 73.1%.
procedure over the same fragment: a comparatively comprehensive
typed core, combined with agent-guided proof construction, makes                                     5.3                                     RQ2: Runtime and Bottlenecks
proof-producing verification effective on application-scale query                                    Figure 4 compares end-to-end wall-clock time only on the cases
pairs that existing models cannot represent.                                                         each tool solves. The baseline medians are 1.4 seconds for QED,
    This support gap is most visible in the 101 feature-rich cases                                   1.7 seconds for SQLSolver, and 8.5 seconds for Cosette. Logos is
from R-Bot DSB, TPC-DS variants, and WeTune: Logos solves 67,                                        substantially slower: its median is 3,632 seconds (60.5 minutes), and
compared with 36 for QED, 27 for SQLSolver, and none for Cosette.                                    its 338 solved cases accumulate 396.3 hours, compared with 1.70
QED is designed to establish equivalence rather than certify inequiv-                                hours for SQLSolver, 0.20 hours for QED, and 0.12 hours for Cosette.
alence, and its bag-semantics model leaves ordering and concrete                                     This gap is the tradeoff of Logos’s Rocq-plus-agent route: the same
aggregate behavior largely abstract. SQLSolver’s linear-arithmetic                                   general semantics that yields high solved and support rates also
reduction loses completeness on nonlinear expressions, supports                                      leaves proof construction to a comparatively expensive synthesis
only a restricted range of aggregate reasoning, and handles or-                                      loop.
dering when the two queries have compatible outer ordering and                                          We analyze all 332 cases that enter agent-guided verification,
slicing structures rather than compositionally nested top-𝑘. Cosette                                 including both completed proofs and timeouts. Their proof-agent
is further constrained by its DSL and integer-encoded, unordered                                     rounds consume 563.3 hours. Of this time, 493.2 hours (87.6%) occur
relational model. By contrast, Logos covers these features within                                    outside diagnostic Rocq invocations and cover model deliberation
one typed, order-sensitive semantics. Its four unsupported cases                                     and proof orchestration; 70.1 hours (12.4%) are spent compiling
                                                                                               10
candidate proofs. The bottleneck is therefore proof synthesis rather         across the corpus but does not eliminate dialect-specific discrepan-
than Rocq compilation alone.                                                 cies.
    The 338 solved cases comprise 243 equivalence results and 95                Agent-guided proof search is also not fully deterministic. Varia-
non-equivalence results. Every equivalence result has a Rocq cer-            tion in model serving, response latency, and proof-step selection
tificate; among these 243 certificate modules, 224 (92.2%) directly          can change both the route taken through the proof space and the
invoke the Logos-specific lemma library, while 58 (23.9%) use a              wall-clock time of an individual run. Consequently, the reported
bag-to-list bridge.                                                          runtime distribution and timeout boundary may vary under re-
    Each diagnostic request submits the current candidate Rocq               peated campaigns, even with fixed prompts and budgets.
module to the checker. Across all 332 agent cases, 53,565 such
submissions contain 20,834,738 lines of candidate Rocq source in
total, with a mean of 62,755 lines and a median of 32,002 lines per          6   RELATED WORK
case. Of these submissions, 50,841 do not compile, consuming 67.9            This section reviews order-aware query semantics and SQL equiv-
of the 70.1 diagnostic hours. The agent thus automates Rocq proof            alence verification. Table 3 compares representative foundations
development, but currently pays for that automation through many             and systems along five dimensions. Unbounded checking ranges
iterations over incomplete proof states. The lemma library and bag-          over databases of arbitrary finite cardinality. Alternative ordered
to-list bridges reduce this repeated work by packaging proof-term            lists records whether a model retains every order permitted by SQL,
combinations that would otherwise have to be reconstructed from              while compositional top-𝑘 further requires these alternatives to sur-
the execution semantics.                                                     vive slicing and remain visible to enclosing queries. Thus, although
    This cost is not an intended property of the semantics. Off-the-         [𝑎, 𝑏] and [𝑏, 𝑎] denote the same bag, fetch1 may yield either [𝑎]
shelf SMT theories do not natively provide the combination re-               or [𝑏]. Bag semantics denotes a multiplicity-based query mean-
quired here: a set of alternative legal row sequences together with          ing. Typed aggregate semantics distinguishes concrete, NULL- and
the type- and NULL-aware semantics of SQL aggregates such as                 type-aware aggregation from restricted encodings or uninterpreted
AVG, MIN, and MAX. cvc5 provides distinct finite-bag and sequence            aggregate operators.
theories [3], but their primitives define neither the correspondence
between a bag and all row orders admitted by SQL nor SQL-specific               Ordered relational semantics and order-aware optimization. Or-
aggregate behavior. An SMT encoding could represent result se-               dered relational models long predate modern SQL equivalence veri-
quences using arrays and explicit lengths, but equivalence proofs            fiers. Coburn and Weddell propose an ordered-list model for graph-
would then require auxiliary invariants relating indices, legal or-          based data in which a query denotes a nonempty set of tuple lists.
ders, and aggregate states, together with solver guidance to in-             Declarative operators can thus admit alternative legal orders, while
stantiate these invariants across operators. Rocq lets us define this        lower-level access plans select more specific results [10]. Their ob-
combination directly and kernel-check the result, while the mea-             jective is wide-spectrum plan refinement: an implementation is
surements identify deterministic proof templates, more selective             valid when its possible results are contained in those of the request.
lemma retrieval, and incremental diagnostics as the main avenues                Slivinskas, Jensen, and Snodgrass give each expression a list-
for reducing synthesis cost.                                                 valued semantics and classify plan equivalence as list, multiset, or
                                                                             set equality. The required equivalence propagates inward from the
 Answer to RQ2. The existing unbounded verifiers are much                    query root. Without an outermost ORDER BY, the root requires mul-
 faster on the cases they solve. Logos trades that speed for                 tiset equality; a sort clears OrderRequired for its child, permitting
 broader, proof-producing coverage; its principal bottleneck is              multiset-preserving rules below it. For ORDER BY 𝐴, two results
 LLM-guided proof construction: 87.6% of agent-round time lies               need only have the same multiset and the same sequence of pro-
 outside Rocq diagnostic compilation. Reusable lemmas and bag-               jected 𝐴-values, thereby identifying permutations within ties [21].
 to-list bridges already reduce repeated reasoning, while deter-             This treatment does not extend directly to top-𝑘 operators such as
 ministic fast paths, better retrieval, and incremental diagnostics          FETCH: a prefix can distinguish tied permutations, requiring either
 provide the main opportunities for narrowing the remaining                  full list equality or an explicit semantics of alternative lists rather
 gap.                                                                        than multiset equality.
                                                                                Chinaei reduces an ordered-bag SQL algebra to set algebra by
                                                                             adding interpreted multiplicity and order-priority columns [6]. This
                                                                             enables reuse of set-based containment techniques. An augmented
5.4    Threats to Validity                                                   relation, however, records one computed priority assignment, en-
Our benchmark families span several SQL dialects. Although the               coding order within ordinary set rows. Similarly, Amarilli et al. rep-
tool-specific materialization adapters use SQLGlot to normalize              resent order-incomplete data as partially ordered relations whose
each case, the transpiler cannot guarantee semantic preservation             linear extensions are possible output lists, but each po-relation fixes
across dialects. A small number of cases may therefore acquire               one underlying bag [1]. It therefore cannot represent grouping or
semantic differences during translation, leading to false positive or        tie-sensitive top-𝑘 when possible worlds induce different result
false negative benchmark outcomes. We mitigate this risk by design-          bags.
ing Logos around a broad common SQL language and, where the                     Mechanized bag semantics over lists imposes a known proof
SQL standard leaves behavior unspecified, adopting PostgreSQL’s              cost. Bag equality becomes equality modulo permutation, while
documented execution behavior. This choice improves consistency              set equality also requires duplicate elimination. Proofs therefore
                                                                        11
                                   Table 3: Comparison of order-aware query models and SQL equivalence systems.

System or framework                    Unbounded checking                 Alternative ordered lists             Compositional top-𝑘               Bag semantics              Typed aggregate semantics
Order-aware semantics and optimization
Coburn and Weddell [10]                            —                                                                       —
Slivinskas et al. [20, 21]                         —                                                                       —
Chinaei [6]                                        —
Amarilli et al. [1]                                —
SQL query-pair verification
Cosette/HoTTSQL [8, 9]
SQLSolver [12]
QED [26]
VeriEQL [13]
Logos
   supported;   partially supported;   unsupported; — outside scope. Ratings concern each published fragment; Logos’s ratings concern its stated typed SQL fragment, rather than all PostgreSQL or ISO SQL.



proceed by list induction while carrying permutation and duplicate-                                        syntax rather than a semantics for arbitrarily nested order-sensitive
elimination invariants through operators; HoTTSQL reports that                                             queries. VeriEQL instead gives bounded SMT verification over fi-
this bookkeeping makes even simple rewrite proofs lengthy and                                              nite tuple lists and uses bag equivalence for unordered outputs.
scales poorly to optimizer rules [9]. Logos instead retains all le-                                        Its five core aggregates have concrete encodings over an integer/-
gal ordered lists, including alternatives with different bags, while                                       Boolean/NULL value model. It encodes LIMIT, OFFSET, and FETCH,
recovering multiplicity-level reasoning through a closure-based lift-                                      including in combination with ORDER BY, but observes list order
ing from bag equivalence to ordered-list equivalence at bag-closed                                         only for an outermost ORDER BY. It therefore does not provide
boundaries.                                                                                                a compositional semantics of legal result orders in which every
                                                                                                           tie-induced top-𝑘 result remains visible to enclosing queries [13].
   SQL query equivalence, rewrite verification, and optimizer testing.                                        Earlier symbolic systems include SPES, which targets bag se-
SQL query equivalence has been studied through proof assistants,                                           mantics, and EQUITAS, which targets set semantics; both use SMT-
algebraic decision procedures, and solver-backed verification. Re-                                         backed symbolic representations to reason about concrete predi-
cent industrial evidence nevertheless shows that real-world rewrite                                        cates, but neither provides semantics for order-sensitive queries [29,
verification remains challenging [16].                                                                     30]. The U-semiring decision procedure (UDP) supplies unbounded
   One line of work uses mechanized semantics and proof-oriented                                           bag reasoning, while abstracting scalar and aggregate semantics and
SQL provers. Cosette and HoTTSQL are closely related systems                                               omitting order-sensitive operators [7]. Testing and fuzzing tools
from the same line of work: Cosette emphasizes an automated                                                such as NoREC expose optimizer bugs by constructing differential
prover pipeline that combines bounded counterexample search                                                or metamorphic test oracles [19]. Such techniques are effective at
with Coq-checked reasoning over K-relations and UniNomials for                                             finding concrete counterexamples, but they do not provide univer-
bag-semantics rewrites, while HoTTSQL develops the HoTT-based                                              sally quantified rewrite proofs.
denotational semantics in more depth [7–9]. Their reasoning is
primarily about relational structure and multiplicities; scalar predi-
cates and expressions are largely treated as uninterpreted functions.                                         LLM-assisted theorem proving. Recent theorem-proving agents
The semantics also does not give compositional meaning to alter-                                           use language models to retrieve relevant facts, predict proof steps,
native result orders, leaving order-sensitive operators outside the                                        or coordinate automated provers. LeanDojo studies retrieval-based
main model. In addition, the systems do not model the full behavior                                        theorem proving over Lean libraries [28], and Thor integrates lan-
of industrial SQL dialects, including null-sensitive three-valued                                          guage models with automated theorem provers for formal proof
logic and type coercions.                                                                                  search [14]. These advances are orthogonal to our SQL-specific
   A second line develops algebraic or solver-backed decision pro-                                         semantic development, but inform Logos’s use of language models
cedures. QED combines semiring normalization with first-order                                              to guide proof search while leaving certificate acceptance to Rocq.
reasoning and gives unbounded guarantees for its supported bag-
semantics fragment. It represents operators such as LIMIT abstractly
and can pass through matching instances by recursive congruence,
but does not model their order-sensitive behavior; casts remain ab-                                        7      CONCLUSION
stract, and aggregate functions are treated as uninterpreted higher-                                       We presented Logos, a proof-producing verifier for SQL rewrites
order operators [26]. SQLSolver reduces U-expressions to linear                                            over arbitrary finite databases. FormalSQL gives a mechanized,
integer arithmetic and adds a divide-and-conquer ordered-bag pro-                                          compositional semantics for possible ordered lists and observable
cedure. It gives concrete encodings for core aggregates, but its value                                     failures, while its closure-based bag-to-list lifting theorem enables
reasoning is restricted to the supported linear-integer-arithmetic                                         local multiplicity reasoning without erasing order. Logos combines
fragment. It simplifies ordering operators, matches two ORDER BY                                           typed lowering with LLM-guided Rocq proof construction. Across
nodes only when their keys and following LIMIT/OFFSET structures                                           389 query pairs, it solves 338 (86.9%), compared with 249 (64.0%)
agree, and recursively invokes its bag verifier below them [12]. Con-                                      for the strongest baseline. These results demonstrate the practical
sequently, its sound ordered reasoning is tied to compatible query                                         value of combining ordered-list semantics with local bag reasoning.
                                                                                                     12
REFERENCES                                                                                    [19] Manuel Rigger and Zhendong Su. 2020. Detecting Optimization Bugs in Database
 [1] Antoine Amarilli, Mouhamadou Lamine Ba, Daniel Deutch, and Pierre Senellart.                  Engines via Non-Optimizing Reference Engine Construction. In Proceedings
     2017. Possible and Certain Answers for Queries over Order-Incomplete Data. In                 of the 28th ACM Joint Meeting on European Software Engineering Conference
     24th International Symposium on Temporal Representation and Reasoning (Leib-                  and Symposium on the Foundations of Software Engineering. Association for
     niz International Proceedings in Informatics), Vol. 90. Schloss Dagstuhl–Leibniz-             Computing Machinery, 1140–1152. https://doi.org/10.1145/3368089.3409710
     Zentrum für Informatik, 4:1–4:19. https://doi.org/10.4230/LIPIcs.TIME.2017.4             [20] Giedrius Slivinskas and Christian S. Jensen. 2001. Enhancing an Extensible
 [2] Qiushi Bai, Sadeem Alsudais, and Chen Li. 2023. QueryBooster: Improving SQL                   Query Optimizer with Support for Multiple Equivalence Types. In Advances in
     Performance Using Middleware Services for Human-Centered Query Rewriting.                     Databases and Information Systems (Lecture Notes in Computer Science), Vol. 2151.
     Proceedings of the VLDB Endowment 16, 11 (2023), 2911–2924. https://doi.org/10.               Springer, 55–69. https://doi.org/10.1007/3-540-44803-9_6
     14778/3611479.3611497                                                                    [21] Giedrius Slivinskas, Christian S. Jensen, and Richard T. Snodgrass. 2001. A
 [3] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt,                Foundation for Conventional and Temporal Query Optimization Addressing
     Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed, Aina Niemetz, Andres                        Duplicates and Ordering. IEEE Transactions on Knowledge and Data Engineering
     Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng, Cesare                    13, 1 (2001), 21–49. https://doi.org/10.1109/69.908979
     Tinelli, and Yoni Zohar. 2022. cvc5: A Versatile and Industrial-Strength SMT             [22] Zhaoyan Sun, Xuanhe Zhou, Guoliang Li, Xiang Yu, Jianhua Feng, and Yong
     Solver. In Tools and Algorithms for the Construction and Analysis of Systems                  Zhang. 2025. R-Bot: An LLM-Based Query Rewrite System. Proceedings of the
     (Lecture Notes in Computer Science), Vol. 13243. Springer, 415–442. https://doi.              VLDB Endowment 18, 12 (2025), 5031–5044. https://doi.org/10.14778/3750601.
     org/10.1007/978-3-030-99524-9_24                                                              3750625
 [4] Edmon Begoli, Jesús Camacho-Rodríguez, Julian Hyde, Michael J. Mior, and                 [23] Emina Torlak and Rastislav Bodík. 2014. A Lightweight Symbolic Virtual Machine
     Daniel Lemire. 2018. Apache Calcite: A Foundational Framework for Optimized                   for Solver-Aided Host Languages. In Proceedings of the 35th ACM SIGPLAN
     Query Processing Over Heterogeneous Data Sources. In Proceedings of the 2018                  Conference on Programming Language Design and Implementation. Association
     International Conference on Management of Data. Association for Computing                     for Computing Machinery, 530–541. https://doi.org/10.1145/2594291.2594340
     Machinery, 221–230. https://doi.org/10.1145/3183713.3190662                              [24] Transaction Processing Performance Council. 2017. TPC Benchmark H (Deci-
 [5] Véronique Benzaken and Évelyne Contejean. 2019. A Coq Mechanised Formal                       sion Support): Standard Specification, Revision 2.17.3. https://www.tpc.org/tpc_
     Semantics for Realistic SQL Queries: Formally Reconciling SQL and Bag Rela-                   documents_current_versions/pdf/TPC-H_v2.17.3.pdf Accessed: 2026-07-31.
     tional Algebra. In Proceedings of the 8th ACM SIGPLAN International Conference           [25] Transaction Processing Performance Council. 2024. TPC Benchmark DS: Standard
     on Certified Programs and Proofs. Association for Computing Machinery, 249–261.               Specification, Version 4.0.0. https://www.tpc.org/TPC_Documents_Current_
     https://doi.org/10.1145/3293880.3294107                                                       Versions/pdf/TPC-DS_v4.0.0.pdf Accessed: 2026-07-31.
 [6] Hamid R. Chinaei. 2007. An Ordered Bag Semantics for SQL. Master’s thesis.               [26] Shuxian Wang, Sicheng Pan, and Alvin Cheung. 2024. QED: A Powerful Query
     University of Waterloo. https://hdl.handle.net/10012/3062                                     Equivalence Decider for SQL. Proceedings of the VLDB Endowment 17, 11 (2024),
 [7] Shumo Chu, Brendan Murphy, Jared Roesch, Alvin Cheung, and Dan Suciu. 2018.                   3602–3614. https://doi.org/10.14778/3681954.3682024
     Axiomatic Foundations and Algorithms for Deciding Semantic Equivalences                  [27] Zhaoguo Wang, Zhou Zhou, Yicun Yang, Haoran Ding, Gansen Hu, Ding Ding,
     of SQL Queries. Proceedings of the VLDB Endowment 11, 11 (2018), 1482–1495.                   Chuzhe Tang, Haibo Chen, and Jinyang Li. 2022. WeTune: Automatic Discovery
     https://doi.org/10.14778/3236187.3236200                                                      and Verification of Query Rewrite Rules. In Proceedings of the 2022 International
 [8] Shumo Chu, Chenglong Wang, Konstantin Weitz, and Alvin Cheung. 2017.                          Conference on Management of Data. Association for Computing Machinery, 94–
     Cosette: An Automated Prover for SQL. In 8th Biennial Conference on Innova-                   107. https://doi.org/10.1145/3514221.3526125
     tive Data Systems Research. www.cidrdb.org. https://www.cidrdb.org/cidr2017/             [28] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing
     papers/p51-chu-cidr17.pdf                                                                     Yu, Saad Godil, Ryan J. Prenger, and Animashree Anandkumar. 2023. LeanDojo:
 [9] Shumo Chu, Konstantin Weitz, Alvin Cheung, and Dan Suciu. 2017. HoTTSQL:                      Theorem Proving with Retrieval-Augmented Language Models. In Advances in
     Proving Query Rewrites with Univalent SQL Semantics. In Proceedings of the 38th               Neural Information Processing Systems 36. 21573–21612. https://doi.org/10.52202/
     ACM SIGPLAN Conference on Programming Language Design and Implementation.                     075280-0944
     Association for Computing Machinery, 510–524. https://doi.org/10.1145/3062341.           [29] Qi Zhou, Joy Arulraj, Shamkant B. Navathe, William Harris, and Jinpeng Wu.
     3062348                                                                                       2022. SPES: A Symbolic Approach to Proving Query Equivalence Under Bag
[10] Neil Coburn and Grant E. Weddell. 1993. A Logic for Rule-Based Query                          Semantics. In 2022 IEEE 38th International Conference on Data Engineering. IEEE,
     Optimization in Graph-Based Data Models. In Deductive and Object-Oriented                     2735–2748. https://doi.org/10.1109/ICDE53745.2022.00250
     Databases (Lecture Notes in Computer Science), Vol. 760. Springer, 120–145.              [30] Qi Zhou, Joy Arulraj, Shamkant B. Navathe, William Harris, and Dong Xu.
     https://doi.org/10.1007/3-540-57530-8_8                                                       2019. Automated Verification of Query Equivalence Using Satisfiability Modulo
[11] Bailu Ding, Surajit Chaudhuri, Johannes Gehrke, and Vivek Narasayya. 2021.                    Theories. Proceedings of the VLDB Endowment 12, 11 (2019), 1276–1288. https:
     DSB: A Decision Support Benchmark for Workload-Driven and Traditional                         //doi.org/10.14778/3342263.3342267
     Database Systems. Proceedings of the VLDB Endowment 14, 13 (2021), 3376–3388.
     https://doi.org/10.14778/3484224.3484234
[12] Haoran Ding, Zhaoguo Wang, Yicun Yang, Dexin Zhang, Zhenglin Xu, Haibo
     Chen, Ruzica Piskac, and Jinyang Li. 2023. Proving Query Equivalence Using
     Linear Integer Arithmetic. Proceedings of the ACM on Management of Data 1, 4,
     Article 227 (2023), 26 pages. https://doi.org/10.1145/3626768
[13] Yang He, Pinhan Zhao, Xinyu Wang, and Yuepeng Wang. 2024. VeriEQL: Bounded
     Equivalence Verification for Complex SQL Queries with Integrity Constraints.
     Proceedings of the ACM on Programming Languages 8, OOPSLA1 (2024), 1071–
     1099. https://doi.org/10.1145/3649849
[14] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski,
     Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022. Thor:
     Wielding Hammers to Integrate Language Models and Automated Theorem
     Provers. In Advances in Neural Information Processing Systems 35. 8360–8373.
     https://doi.org/10.52202/068431-0608
[15] Toby Mao and Contributors. 2026. SQLGlot: Python SQL Parser and Transpiler,
     Version 30.11.0. https://pypi.org/project/sqlglot/30.11.0/ Accessed: 2026-07-07.
[16] Vivek R. Narasayya and Surajit Chaudhuri. 2026. Leveraging Query Opti-
     mizers to Verify the Soundness of LLM-Based Query Rewrites for Real-World
     Workloads, and More!. In 16th Conference on Innovative Data Systems Research.
     www.cidrdb.org, Chaminade, CA, USA, 12. https://www.cidrdb.org/cidr2026/
     papers/p33-narasayya.pdf
[17] Hamid Pirahesh, Joseph M. Hellerstein, and Waqar Hasan. 1992. Extensible/Rule
     Based Query Rewrite Optimization in Starburst. In Proceedings of the 1992 ACM
     SIGMOD International Conference on Management of Data. Association for Com-
     puting Machinery, 39–48. https://doi.org/10.1145/130283.130294
[18] PostgreSQL Global Development Group. 2026. PostgreSQL 18.4: SELECT. https:
     //www.postgresql.org/docs/18/sql-select.html Accessed: 2026-07-28.


                                                                                         13
