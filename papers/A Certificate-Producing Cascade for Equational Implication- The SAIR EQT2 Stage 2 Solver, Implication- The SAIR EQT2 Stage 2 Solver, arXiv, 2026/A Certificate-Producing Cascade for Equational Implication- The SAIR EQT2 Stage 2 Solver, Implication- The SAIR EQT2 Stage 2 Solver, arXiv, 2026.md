                                               A Certificate-Producing Cascade for Equational
                                                 Implication: The SAIR EQT2 Stage 2 Solver
                                                        Haobo Ma                                Wenlin Zhang                           Manuel Israel Cázares
                                                     ChronoAI Pte. Ltd.                 National University of Singapore                     Bytepro AI
                                                        Singapore                                 Singapore                                Mazatlán, Mexico

                                        Abstract                                                                 This contract changes the design objective. A classifier
                                        The SAIR Mathematics Distillation Challenge on Equational             may be useful while remaining difficult to audit, whereas
                                        Theories asks a solver to classify whether one magma iden-            a certificate producer must preserve enough structure to
                                        tity implies another and, for either verdict, to return a cer-        reconstruct a kernel-checkable witness. At the same time,
                                        tificate accepted by a deterministic Lean 4 judge. We present         the kernel boundary permits aggressive untrusted search. A
arXiv:2609.00706v1 [cs.CL] 1 Sep 2026




                                        a single-file solver organized as a cheapest-first cascade. Its       defect in our term ordering, unifier, model finder, or certifi-
                                        false branch combines coefficient tests over structured alge-         cate printer may increase resource use or prevent a solution
                                        bra families, bounded finite-model search, an explicit central-       from being found, but it cannot cause an invalid certificate
                                        groupoid witness, and several infinite-carrier witnesses. Its         to be accepted. The competition proxy records success only
                                        true branch is a proof-producing ordered unit superposition           after the official judge has compiled the submitted term and
                                        procedure with Knuth–Bendix ordering, bidirectional de-               checked its dependency policy.
                                        modulation, indexing, memoised substitution, and anytime                 Our system implements a deterministic-first cascade in
                                        size deepening. Search results remain outside the trusted             one Python file. The early stages recognize direct impli-
                                        base: successful derivations are replayed as small Lean 4             cations and search inexpensive countermodel families. A
                                        terms, and countermodels are rechecked by the competition             bounded irregular model finder and deeper structured fam-
                                        judge.                                                                ilies handle false residuals. An ordered unit-superposition
                                            The frozen solver is a 189,504-byte Python file with SHA-         engine handles true residuals and records a replayable deriva-
                                        256 f2392533c9f4c03b.... In local runs through official               tion rather than only a refutation bit. The same source dis-
                                        judge revision 2848228, it produced accepted certificates for         patches to the Solo protocol, in which one process handles
                                        all 1,889 rows of the six public sets with no language-model          one problem, or the Marathon protocol, in which one process
                                        calls. Separate measurements recorded full agreement on the           shares a global budget among a manifest of problems. Every
                                        800 published Stage 1 evaluation-distribution problems, 100           successful path ends in a Lean 4 certificate.
                                        accepted rows in the canonical Marathon manifest without                 The central empirical result is deliberately narrower than
                                        tokens, and 200 accepted rows in the hosted playground.               a completeness claim. The cascade covers every row in the
                                        These are regression and playground measurements, not a               measured public, distribution-drill, and hosted-playground
                                        leaderboard result and not evidence about a hidden set. All           corpora within the recorded budgets. Neither the counter-
                                        quantitative claims are tied to immutable result ledgers; the         model families nor the superposition implementation is proved
                                        paper makes no completeness or comparative-superiority                complete, and the deeper stages stop at wall-clock limits. We
                                        claim.                                                                therefore do not infer performance on the held-back evalua-
                                                                                                              tion set. The result is a system description and an auditable
                                                                                                              regression report, not a theorem about all single-identity
                                        1   Introduction
                                                                                                              implications.
                                        An equational theory of magmas has one binary opera-                     This paper makes four contributions.
                                        tion and no assumed associativity, identity, or cancellation
                                        law. Given equations 𝐸 1 and 𝐸 2 , the implication problem
                                        asks whether every magma satisfying 𝐸 1 also satisfies 𝐸 2 .             • We present a certificate-producing cascade that inte-
                                        The SAIR Mathematics Distillation Challenge, organized                     grates complementary algebraic model families and
                                        by Damek Davis and Terence Tao with the SAIR Founda-                       proof-producing superposition behind one competi-
                                        tion, turns that question into a certificate-production task               tion interface.
                                        grounded in the Equational Theories Project [3, 12]. A true              • We describe certificate encodings that satisfy the judge’s
                                        answer must contain a Lean 4 proof of the universal im-                    dependency policy, including encodings for finite car-
                                        plication. A false answer must exhibit a magma in which                    riers beyond the direct table helper’s single-digit range
                                        the hypothesis holds and the conclusion fails. The same                    and core-only proofs over infinite carriers.
                                        deterministic judge checks both forms. An accepted certifi-              • We analyze two consequential implementation fail-
                                        cate solves the row; a plausible label, proof sketch, or partly            ures: retention of tautologies in the active superposi-
                                        checked derivation receives no credit [11, 12].                            tion set and inconsistent handling of the two accepted
                                                                                                          1
Conference’17, July 2017, Washington, DC, USA                                            Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


        spellings of the magma operation. End-to-end certifi-           ask later stages merely to justify it. Each stage returns a self-
        cate runs, rather than label accuracy alone, exposed            contained candidate of one polarity, submits that candidate,
        both failures.                                                  and continues if checking fails. For example, an arithmetic
      • We provide a hash-bound claim ledger that connects              countermodel whose certificate exceeds an instance budget
        the solver bytes, judge revision, result files, and every       does not bias the proof branch toward false; it is discarded
        evaluation-table row to SHA-256 identifiers.                    as an unavailable witness. A superposition trace that cannot
                                                                        be replayed is likewise not evidence for a true output. This
   The rest of the paper follows the execution path. Sec-
                                                                        discipline prevents a search heuristic from escaping into the
tion 2 gives the single-file architecture. Sections 3 and 4
                                                                        externally visible result.
describe the countermodel and proof branches. Section 5
                                                                           At both protocol entry points we normalize the input op-
covers deployment constraints, and Section 7 reports mea-
                                                                        eration symbol. The official problem format permits either
surements. We then state the reproducibility boundary and
                                                                        an asterisk or a diamond, but the solver’s term parser has
place the system relative to equational-theory, superposition,
                                                                        one internal token. Mapping the asterisk to ⋄ before pars-
and proof-assistant work.
                                                                        ing preserves the semantics and is operationally necessary;
                                                                        Section 5.2 records the failure that revealed it.
2     Single-File Solver Architecture
2.1    Contract and trusted boundary                                    2.2   Cheapest-first cascade
The submission contract requires one solver.py file no                  The Solo cascade is ordered by expected cost and by which
larger than the competition limit. Solver v2.5 is 189,504 bytes,        branch benefits from remaining time.
and therefore remains below that limit while containing all
                                                                           Stage A: shallow countermodels. The solver first tries
search code and fixed data. In Solo mode the proxy sends
                                                                        tiny brute-force tables, scalar linear and affine operations,
one JSON problem and its budget to a fresh process; the
                                                                        vector-linear families, low-degree polynomial operations,
solver sends judge or language-model requests back over
                                                                        and recognized infinite-carrier Austin models [1]. The ex-
line-delimited JSON. In Marathon mode the runner supplies
                                                                        panded structured families add about 0.8 seconds on a true
a JSONL manifest and an append-only output path. The same
                                                                        input in the recorded development measurement. No irregu-
source supports both modes, selected by the runner-owned
                                                                        lar finite-model search is performed yet.
Marathon environment variable [11].
   The trusted computing base for a verdict is not the Python              Stage B: direct true certificates. Syntactic singleton col-
implementation. The judge generates the problem statement               lapse and substitution-instance checks produce direct proofs.
and the verdict-specific Goal type. A true goal has the form            A specialized singleton-forced prover then receives an eight-
                                                                        second cap, although applicable cases normally close during
         ∀(𝐺 : Type) [Magma 𝐺],          𝐸 1 (𝐺) → 𝐸 2 (𝐺),             its initial search. The general superposition engine follows
                                                                        with a quick budget min(6, max(1,𝑇 /600)) seconds for a pro-
whereas a false goal existentially quantifies a carrier and             cess allowance 𝑇 ; this is six seconds under the recorded Solo
magma for which 𝐸 1 holds and 𝐸 2 does not. The solver sup-             allowance. Most provable public instances terminate within
plies a definition named submission; Lean 4 elaboration,                this cap.
kernel checking, and the dependency inspector determine
acceptance. Search is therefore an untrusted producer of                  Stage C: bounded irregular models. A finite-model search
candidate proof objects.                                                over carriers four through ten receives eight seconds. It prop-
   The interface creates three distinct obligations. First, a           agates the universal instances of the hypothesis and Latin-
candidate must have the right polarity: a universal implica-            square constraints rather than enumerating complete tables.
tion for a true verdict or an existential separating structure             Stage D: deep false search. Only residuals reach heavier
for a false verdict. Second, the term must inhabit the judge-           polynomial and vector families, capped at sixty seconds,
generated goal rather than a solver-reconstructed copy that             followed by another finite-model pass capped at one hundred
might differ in variable order or parsing. Third, all transitive        twenty seconds. Deep false search precedes the deepest proof
dependencies must satisfy the proof policy. The judge en-
                                                                        pass so that a difficult false row does not consume most of
forces the first two by type checking submission : Goal;
                                                                        its allowance in proof saturation.
its inspection pass enforces the third. The emitted source
never uses admitted terms. This separation is why a success-               Stage E: anytime proof search. The ordered-superposition
ful Python-side check is called a candidate throughout the              engine, in the tradition of completion-based equational provers [2,
implementation, while “accepted” is reserved for the judge              8], receives min(600, max(20,𝑇 /6)) seconds, which is six
status.                                                                 hundred seconds under the Solo allowance. The engine re-
   The polarity boundary also determines failure recovery.              peatedly raises term-size and variable caps. If no direct refu-
The solver does not cache an unverified Boolean verdict and             tation is returned, a small pool of derived equalities can
                                                                    2
A Certificate-Producing Cascade for Equational Implication: The SAIR EQT2 Stage 2 Solver          Conference’17, July 2017, Washington, DC, USA


be emitted as exact lemmas followed by a kernel-checked                       row. If the runner terminates the process, all complete ear-
closing tactic. A language-model feedback loop follows the                    lier lines remain scoreable. A process-level timer bounds
deterministic cascade, but none of the accepted rows in the                   legacy search loops that predate the batch driver. The batch
archived regression invoked it.                                               path issues no speculative language-model calls and leaves a
   Every stage independently verifies its candidate before                    residual unanswered rather than consuming tokens without
the solver stops. A rejected certificate proceeds to the next                 producing a certificate.
strategy; a successful search without a valid emitted term
is not counted as a solution. This control flow distinguishes
search coverage from certificate robustness.                                  2.5   Cascade invariants and failure isolation
                                                                             Stage ordering does not assert that either polarity is more
2.3 Representation and dispatch                                              likely. Instead, it minimizes expected certificate cost while
Both branches share a small non-associative term representa-                 reserving time for both branches. A structured false witness
tion. Parsing produces a binary tree with variables at leaves;               is attractive early because checking a closed operation is
no reassociation or commutative normalization is performed.                  usually cheaper than saturation. Direct true patterns are
Alpha-renaming maps variables to a canonical local order for                 equally attractive because they avoid both table construc-
cache keys and family matching, but emitted proofs retain                    tion and general proof search. Measurements showed that
a map back to the judge’s binder order. Operation count,                     most provable rows close near the start of saturation, which
variable support, depth, and tree size are computed once                     motivates placing the quick G3 pass before irregular model
and reused by scheduling, countermodel probes, and proof                     search. Deep false search precedes deep G3 only after every
search.                                                                      low-cost recognizer has failed.
   Dispatch relies on positive recognizers. A direct proof                      The implementation maintains a cascade invariant: before
stage returns only after constructing a substitution or equal-               entering a stage, the solver has no accepted certificate, and
ity chain. An Austin or central-groupoid stage returns only                  every earlier candidate has either been absent, failed local
when the hypothesis matches its stored schema and a con-                     construction, or been rejected by the judge. It does not main-
crete evaluation separates the goal. A family that is merely                 tain the stronger and generally invalid invariant that earlier
likely from equation identifiers is not selected: identifiers are            stages have ruled out their polarity. Failure to find a finite
useful for diagnostics, but the solver matches parsed laws.                  model does not support truth; failure to derive the goal does
This property supports independent replay and handles in-                    not support falsity. Each stage can therefore be analyzed
puts whose labels or variable names differ from those in the                 and tested as a partial certificate producer, and the composi-
public files.                                                                tion is sound whenever the judge is sound, regardless of the
   Candidate validation is stratified. Low-cost Python evalua-               producers’ coverage.
tion removes malformed tables, wrong witnesses, and printer                     Exceptions are contained at strategy boundaries in the
bugs before a judge call. Judge feedback then closes the se-                 Marathon path so that a malformed residual cannot discard
mantic and dependency obligations. The development har-                      previously completed rows. Solo has a fresh process per
ness records both outcomes: a “found” countermodel rejected                  row and can rely on the runner to record a crash. Within a
by Lean 4 indicates an emitter defect or an encoding mis-                    strategy, deadlines are checked at natural allocation points:
match, whereas the absence of a Python witness within a                      carrier changes, model-search decisions, deepening rounds,
deadline indicates a coverage limitation. This distinction in-               and given-clause iterations. The Marathon alarm provides
formed the large-carrier encoding correction in Section 3.5.                 a final outer bound for code paths whose internal checks
                                                                             are too sparse. Timeout returns “no candidate” rather than a
2.4   Solo and Marathon                                                      verdict.
Solo gives each row a fresh process and a fixed allowance.                      Caches follow the same lifetime discipline. Parser and
Marathon instead requires triage across a whole manifest.                    static-law data live for the process. A superposition run owns
The batch path stably sorts problems by a structural cost de-                its unifier, normalization, term, and clause caches, which are
rived from operation occurrences, variable count, and equa-                  cleared before another problem. Marathon could in princi-
tion length. It then runs two passes. The first gives every row              ple share more proof state across rows, but the current im-
the shallow stages before any residual receives deep work.                   plementation does not rely on cross-problem lemmas. This
The second revisits only residuals. A fair cap is recomputed                 keeps Solo and Marathon certificate semantics aligned and
from remaining wall-clock time divided by remaining rows                     limits memory growth under a long manifest.
and clamped to the documented per-row interval. At most                         The fallback model follows the complete deterministic
fifty-five percent of a residual’s current slice goes to the false           cascade in Solo and is not invoked in the archived accepted
branch; the proof branch receives the rest.                                  rows. Its proposals still pass through the same printer and
   Marathon outputs constitute durable state. Each answer                    judge, so adding the fallback does not enlarge the trusted
is one JSON line, flushed and synchronized before the next                   base. In Marathon it is disabled to preserve the global token
                                                                         3
Conference’17, July 2017, Washington, DC, USA                                              Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


budget; the result is a partial manifest containing only ver-              vectors agree and the goal vectors differ, a separating assign-
ified deterministic answers. These are scheduling choices,                 ment can be sought in the small module. Full evaluation is
not claims about the intrinsic capabilities of the configured              still applied before emission, which protects the certificate
model.                                                                     path from an error in this symbolic shortcut.
                                                                              Vector-linear families use exactly the same recursion with
3     Countermodel Construction                                            matrices acting on coordinates. They are useful because
For a false implication the solver must find an operation                  scalar coefficient coincidence may hold in every small mod-
satisfying all assignments of the hypothesis and at least one              ulus even when non-commuting linear actions distinguish
assignment falsifying the goal. It evaluates candidate families            the goal. Polynomial operations abandon the linear invariant
in Python, retains a concrete witness, and emits a certificate             and instead use compiled term evaluators over bounded carri-
in which the judge repeats the decisive checks.                            ers. The family ordering therefore progresses from symbolic
                                                                           coefficient equality to increasingly expensive full evaluation,
3.1   Coefficient matching over structured families                        while presenting a uniform result to the certificate printer: a
                                                                           carrier, a total binary operation, and a goal witness.
Represent a magma term by the formal coefficients induced
by a candidate operation. For                                              3.2   Irregular finite models
                  𝑥 ⋄ 𝑦 = 𝑎𝑥 + 𝑏𝑦      (mod 𝑛),                            Some countermodels have no low-degree algebraic descrip-
                                                                           tion. The finite-model stage treats the Cayley table as a con-
each leaf contributes a coefficient obtained by multiplying                straint problem. For a proposed carrier size, table cells begin
edge labels along its path. Equality of two terms for all assign-          unassigned. Ground instances of the hypothesis watch the
ments is therefore equality of their coefficient vectors mod-              cells on which their two terms depend. Assigning a cell may
ulo 𝑛. This gives an exact, inexpensive test for whether the               simplify a term, force another cell, or violate an instance.
hypothesis is an identity of the candidate magma. The same                 The search uses a minimum-remaining-values choice among
representation quickly locates an assignment on which the                  table positions and abandons partial tables as soon as a hy-
goal coefficients differ. The scan includes composite moduli               pothesis instance becomes unequal.
and its shallow range extends to the largest carrier admitted                 Many identities imply that rows, columns, or both must be
by the certificate-instance guard.                                         permutations. A law in which a variable occurs once on one
   Affine operations add a constant term, and matrix-linear                side and appears under the operation in a particular argu-
operations replace the scalar coefficients by matrices over                ment position can expose such a constraint. The solver infers
small finite fields. The latter searches include two-dimensional           the applicable Latin flags, rejects duplicate row or column
vectors over the three-element field and three-dimensional                 values, and forces naked singletons. For one residual requir-
vectors over the two-element field. Polynomial candidates                  ing an eight-element quasigroup, this propagation changed
are evaluated on full assignments when the carrier and hy-                 the outcome from no witness within a one-hundred-twenty-
pothesis arity make that feasible. The deep pass adds a qua-               second attempt to a witness in 0.3 seconds. The production
dratic grid, a two-dimensional family over the five-element                shallow search remains restricted to carriers four through
field, and sampled polynomials of degree at most three. An                 ten and an eight-second cap; the deep pass revisits the same
instance-count guard prevents a mathematically compact                     carrier interval with a longer cap.
operation from producing a certificate whose exhaustive                       Before emission, the completed table is checked by a sep-
hypothesis check exceeds the judge budget.                                 arate evaluator over all hypothesis assignments and a stored
   These families provide both search efficiency and struc-                goal-falsifying assignment. The Lean 4 certificate then re-
tured certificates. They find many witnesses faster than a                 constructs the table operation and invokes the judge’s finite-
generic table search while preserving semantic structure in                decision tactic. The duplicated checks reduce wasted judge
the emitted certificate. For example, a linear countermodel                calls, while only the latter determines acceptance.
can be represented by its arithmetic operation rather than by                 The partial-table solver maintains two invariants. Every
a large opaque table. The judge still evaluates the hypothesis             assigned cell agrees with all hypothesis instances that have
and the failing goal instance, so coefficient matching remains             become ground, and every inferred Latin constraint agrees
an untrusted search optimization rather than a proof rule.                 with the assigned portion of its row or column. A watch list
   Coefficient evaluation is implemented recursively. A vari-              connects a cell to the term instances whose evaluation may
able leaf maps to its basis vector. At an internal node, the               advance when that cell is filled. Propagation reaches a fixed
coefficient vector is 𝑎𝑢® + 𝑏® 𝑣 for child vectors 𝑢® and 𝑣®; affine       point before the next decision. At a complete table, the first
families carry one additional constant coordinate. Thus the                invariant implies that exhaustive reevaluation of the hypoth-
universal hypothesis test does not enumerate assignments. If               esis should succeed; the separate final evaluator checks this
the two sides have different vectors, the candidate is immedi-             implication and also searches the goal assignments. Search
ately rejected as a model of the hypothesis. If the hypothesis             backtracking may be unsound or incomplete as an algorithm
                                                                       4
A Certificate-Producing Cascade for Equational Implication: The SAIR EQT2 Stage 2 Solver           Conference’17, July 2017, Washington, DC, USA


without threatening an accepted answer, because the table is                  the direct constants of the submitted term; helpers inside
subsequently evaluated from scratch and then checked once                     the submission namespace are unrestricted, which the or-
more in Lean 4.                                                               ganizers document as intended for auxiliary definitions. The
   Carrier growth is likewise heuristic. The shallow and deep                 final theorem refers directly to the namespaced operation
passes enumerate the documented carrier interval, but the                     and core arithmetic. This route was accepted by the official
solver does not infer that absence of a model there implies                   judge for the recorded larger carrier sizes and avoids relying
truth. It passes the row to the next proof or model family. This              on the table parser.
behavior implements the paper’s no-completeness boundary.                        This distinction affects dependency enforcement but does
                                                                              not circumvent it. The helper definition is part of the sub-
3.3   Central groupoids and the E168 residual family                          mitted source, is compiled by Lean 4, and is traversed by the
The evaluation-distribution drill identified a family of twelve               kernel when its theorem is checked. The allow-list controls
residuals whose hypothesis is the central-groupoid law. Cen-                  dependencies, not the truth of definitions. As specified by
tral groupoids have a well-known combinatorial structure                      the documented proof interface, submission-local auxiliary
studied by Knuth [7]. The natural constructions tried by the                  definitions provide the intended mechanism for packaging
structured stages satisfy both the hypothesis and the relevant                operations and lemmas that are not global library dependen-
E168 conclusions, so they do not separate these equations.                    cies.
Increasing the generic finder budget did not reliably recover
the missing witnesses.
   The solver therefore includes one explicit non-natural                     4     Proof-Producing Ordered Superposition
central groupoid of order nine. The table was checked against
each relevant hypothesis and goal, then stored once as a fixed               The true branch operates in unit equational logic. It assumes
witness family. When the hypothesis matches up to variable                   one universally quantified identity and attempts to derive
renaming and a goal is separated by the table, the solver                    the goal identity. The engine is inspired by ordered superpo-
                                                                             sition and unfailing completion as implemented in first-order
emits the ordinary finite-table certificate. This stage is not a
                                                                             provers, but is specialized to one binary symbol, unit clauses,
classification of central groupoids and makes no claim about
minimal order. It provides a specific, auditable witness for a               and the need to reconstruct a small positive Lean 4 proof.
recurring algebraic family: the official runner accepted the
emitted certificates for the twelve drill residuals.
                                                                              4.1   Terms, ordering, and inference
3.4   Infinite carriers for Austin pairs                                     Terms are immutable trees over variables and the binary
Finite satisfiability can conceal false general implications.                magma symbol. A Knuth–Bendix ordering with unit symbol
Several pairs catalogued in the Equational Theories Project                  weights determines maximal equation sides and orients us-
are true over the finite magmas searched by standard meth-                   able rewrite rules. Superposition overlaps an oriented side
ods but false in general. For recognized Austin-pair hypothe-                with a non-variable subterm of another maximal side, com-
ses, the solver selects a fixed operation on N, or its opposite,             putes a most general unifier, and constructs the resulting
and a small tuple falsifying the goal. The certificate proves                equality. Ordering checks are repeated after unification, be-
the hypothesis through a fixed sequence of elementary lem-                   cause substitution can change comparisons. Equations that
mas and closes the negated goal with the concrete tuple.                     cannot be oriented remain available for symmetric infer-
   This is qualitatively different from finite decision. There               ences.
is no exhaustive tactic over N, so the complete mathematical                     The goal is represented internally as a negative unit clause
argument must be expressed in the certificate. The original                  𝑢 ≠ 𝑣 over fresh constants. Active equalities can superpose
certificates imported a broad tactic module; Section 5.1 de-                 into either side; ordinary demodulation simplifies the clause.
scribes why those imports became an operational problem                      If its sides unify, the negative clause is refuted. This internal
and how positive-form replay reduced their compile time.                     negative representation is convenient for search, but the
                                                                             emitted proof does not ask Lean 4 to validate a refutation
3.5   Certificate shapes and the allow-list                                  calculus. It instead reconstructs a positive equality chain
For carriers through ten, finOpTable embeds a JSON-like                      ending at the original goal.
Cayley table and decideFin! checks the finite existential                        Forward demodulation normalizes each generated equal-
goal. The helper extracts individual decimal characters, so                  ity by current rules. Backward demodulation revisits active
a table entry with multiple digits is not a faithful encoding.               equations when a new rule can simplify them. Symmetric
Larger carrier tables therefore cannot use that direct shape.                alpha-normalized keys remove variants. A given-clause loop
   The alternative is a definition such as submission.op                     interleaves a weight heap with an age queue; later deepening
whose body computes a linear, affine, polynomial, or packed-                 rounds alter the variable penalty and age ratio so that a proof
table lookup operation. The judge checks its allow-list on                   blocked by one selection policy is not permanently starved.
                                                                         5
Conference’17, July 2017, Washington, DC, USA                                          Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


4.2   The tautology-deletion failure                                   4.4   Anytime deepening
An early version of the prover did not resolve one public              A fixed size cap is sensitive to the selected bound: saturation
residual, hard3_0314. The official-runner attempt found no             at a small cap can terminate with time remaining even when
proof after 810 seconds even though an external derivation             one slightly larger intermediate would finish the proof. The
suggested that the necessary clauses were within the config-           deep pass therefore runs a schedule of increasing term-size
ured size bound. Instrumentation indicated that throughput             and variable caps. If a round saturates, its unused time moves
was not the primary cause. When demodulation transformed               forward. If the final configured round saturates, caps con-
an equation into 𝑠 = 𝑠, the step constructor returned no proof         tinue to grow within the overall deadline. The last strategies
node, and the caller retained the partially rewritten input            reduce the variable penalty and increase age pressure, ap-
equation. Backward simplification had the same behavior.               proximating a different prover configuration without main-
   Consequently, many small instances of the hypothesis                taining another implementation.
remained live. Their weights made them attractive to given-               The procedure remains budget-bounded and machine-load
clause selection, so they repeatedly displaced clauses on the          sensitive. It is not a new completeness result for ordered
useful derivation. The correct simplification rule is deletion:        superposition, nor a proof that the chosen ordering is fair
a demodulated tautology contributes nothing to saturation.             under every cap. The evaluation in Section 7 measures this
The fix retires the active clause before testing the rewritten         implementation on fixed corpora.
result and drops a new clause whose sides become equal.
   With that change, the prover found the residual proof in
                                                                       4.5   Replay into the Lean 4 kernel
0.6 seconds in its direct measurement, and the official-runner
path produced an accepted certificate in 14.6 seconds of               Every retained equation stores a derivation recipe. Replay
wall-clock time. These measurements illustrate the coupling            recursively reconstructs source equations, instantiates the
between simplification and selection rather than establishing          universally quantified hypothesis, and uses congruence to
a general speed ratio. Retaining a tautology as a live clause          place an equality inside the overlap context. A superposi-
changed the effective search strategy enough to prevent                tion step becomes a have binding assembled from congrArg,
the final public proof from being found within the earlier             symmetry, and transitivity. Goal simplifications become an-
attempt.                                                               other exact equality chain. The final proof is a sequence of
                                                                       have/rw/exact-style core terms in positive form.
                                                                          Positive replay isolates search from trust. The Python
4.3   Indexing and allocation control                                  engine can orient an equation incorrectly, use a stale cache,
Demodulation candidates are retrieved through a discrimina-            or reconstruct the wrong path; any of these produces a term
tion tree keyed by a term’s linear skeleton. The index returns         that fails to elaborate or has the wrong type. The judge
rules whose left sides may match a subterm; matching and               then rejects it, and the solver may retry robust emission
the ordering check filter false positives. Normal forms are            or continue to another stage. A prover defect can therefore
cached and versioned by the rewrite-rule set. Term sizes,              cause a missed proof or a slower run, but cannot cause a
variable multisets, preorder traversals, and eligible positions        wrong acceptance unless there is also a defect below the
are cached on immutable equations.                                     Lean 4 kernel boundary.
   The unifier returns a triangular substitution rather than ea-          Replay granularity and certificate size impose competing
gerly applying it to every binding. A memoised substitution            requirements. Emitting every normalization micro-step is
routine resolves chains while sharing unchanged subtrees.              easy to audit but repeats contexts and substitutions. Com-
Before constructing a superposition result, the engine esti-           pressing an entire derivation into a large tactic call reduces
mates instantiated size from static term sizes and per-variable        source size but reintroduces a dependency on tactic behavior
counts. Overlaps that cannot fit the current cap are rejected          and library imports. The solver uses one named equality
before allocating their terms. Unifier results are cached by           per selected inference, with normalization represented as
the renamed overlap pair. These changes preserve the in-               explicit transitivity where needed. Shared ancestors are emit-
ference trace at fixed bounds while reducing the work per              ted once in topological order. This keeps proof text close to
surviving clause.                                                      the saturation trace while allowing Lean 4 to elaborate each
   The passive set stores recipes—source equation, target              local equality without reconstructing the global search.
equation, direction, and overlap position—rather than full                Robust re-emission addresses elaboration rather than log-
instantiated proof objects. The selected recipe is materialized        ical inference. The first printer uses direct exact terms. If
when it becomes given. Under the hosted memory limit, this             the judge rejects that source, the solver can wrap individual
representation permits a large passive frontier without dupli-         equality steps in a small sequence of core closing alternatives
cating every term and ancestry chain. Caches and negative-             and resubmit the same derivation; it does not rerun super-
goal storage are bounded and cleared between prover invo-              position or change the claimed theorem. If search exhausts
cations.                                                               its deadline without a refutation, the lemma-pool path emits
                                                                   6
A Certificate-Producing Cascade for Equational Implication: The SAIR EQT2 Stage 2 Solver           Conference’17, July 2017, Washington, DC, USA


a bounded selection of the smallest already proved conse-                     normalization must occur at the protocol boundary, before
quences. Any final tactic must still close the judge goal from                any dispatch or caching.
exact lemmas. Failure to do so leaves the row unanswered.
                                                                              5.3   Resource and filesystem constraints
5 Engineering for the Hosted Environment                                     The hosted-style sandbox has a read-only submission mount,
5.1   Core-only certificates                                                 a bounded process count, bounded memory, no direct net-
                                                                             work, and a small writable temporary filesystem. The solver
The public harness used Lean 4 4.30.0-rc2, while the an-                     consequently uses the Python standard library, keeps all
nounced hosted verifier used Lean 4 4.32.0 with the corre-                   static data in the single source file, does not spawn external
sponding Mathlib release. Most emitted certificates already                  provers, and does not assume repository access. Bounded
imported only judge modules and core definitions. The ex-                    passive queues and caches keep the superposition engine
ception was the infinite-carrier Austin family, whose tactic                 below the sandbox memory ceiling observed in long false
import made compilation sensitive to the larger library envi-                saturations. The process-level timer also prevents a deeply
ronment. In a compatibility run, one such certificate required               nested legacy loop from overrunning its Marathon slice.
about 330 seconds of compilation.                                               Marathon’s output file is the only durable mutable state
   Rather than increasing the solver-side timeout, we rewrote                supplied by the runner. Per-row flush and synchronization
the Austin certificate in positive form, replaced the broad tac-             are therefore required for correctness. An initial local fixture
tic dependency with explicit core lemmas, and re-emitted the                 run also showed that the official checkout’s default artifact
witness. Its Lean 4 4.32 compilation then completed within                   directory could be unwritable in a managed workspace; redi-
3.1 seconds. A stratified corpus of 120 accepted certificates,               recting judge artifacts to temporary storage resolved the
covering every emission family and all fourteen former v1                    environmental failure without changing judge sources.
residuals, compiled 119 of 120 under the exact announced
toolchain in an external harness with a 120-second per-phase                  6     End-to-End Certificate Production
limit; the one non-pass was the pre-rewrite Austin witness
itself, which passes under a 300-second per-phase configu-                   Search and replay together form a single transaction. This
ration matching the judge (phases of 184 and 145 seconds).                   section follows representative false and true candidates from
The corpus therefore characterizes the migration-era certifi-                a parsed equation pair to the theorem checked by the judge.
cate set rather than the frozen artifact’s current output: the               The examples show certificate shape rather than a particular
frozen solver’s own certificate for the same problem imports                 benchmark row; the concrete generated sources remain in
only the judge module and is accepted in under five seconds.                 the archived result ledgers.
The judge support modules compiled unchanged. That cor-
                                                                              6.1   Finite countermodel transaction
pus run executed outside the repository and is archived as
an operator attestation (results/lean432_corpus/). When                       Suppose coefficient matching or table search returns a carrier
the organizers subsequently upgraded the judge to Lean 4                      Fin 𝑛, an operation 𝑚, and an assignment 𝜌 that separates the
4.33.1 after the kernel-soundness review, the frozen artifact                 goal. Before printing Lean 4, the solver performs three checks.
was revalidated in full under the upgraded judge — official                   It confirms that every table entry or arithmetic result belongs
harness, all six public sets, the distribution drill, and the                 to the carrier. It enumerates every assignment required by
Marathon manifest — with the resulting ledgers commit-                        the hypothesis and checks equality of the evaluated sides.
ted and hash-bound (results/lean4331_revalidation/).                          Finally, it reevaluates the two goal terms at 𝜌 and checks
Neither measurement substitutes for hosted scoring.                           that their values differ. A failure at any point discards the
                                                                              candidate without a judge call.
5.2   Input encoding                                                             For a small table the emitted proof has the following
                                                                              schematic form:
The official judge normalizes the asterisk and diamond spellings
when it builds the Lean 4 problem. The runner, however,                       def submission : Goal := by
passes the original problem text to the contestant process.                     let m : Magma (Fin n) :=
An earlier solver normalized only along one internal path.                        { op := finOpTable "<table>" }
When the Stage 1 evaluation splits were supplied in their pub-                  refine <Fin n, m, ?_>
lished asterisk encoding, the solver crashed before certificate                 decideFin!
search and recorded zero accepted rows out of 800.                           The angle-bracket line is printed with Lean 4’s tuple notation
   Version v2.4 introduced, and v2.5 retains, normalization                  in the actual source. The judge’s decision tactic expands the
of both equations at both the Solo and Marathon intakes.                     finite universal hypothesis and the existential goal witness
The same drill then recorded 800 accepted certificates with                  under the supplied operation. Thus the stored Python assign-
full agreement against the published answers. Thus, verified                 ment is useful for prechecking, but the accepted theorem
output does not address failures in an unverified parser;                    does not rely on the Python evaluator.
                                                                         7
Conference’17, July 2017, Washington, DC, USA                                          Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


   For a larger structured carrier, the transaction changes               For an overlap, replay first obtains the equality used as a
only in how 𝑚 is defined. A helper inside the submission               rewrite. It lifts that equality through the surrounding term
namespace computes the operation using Nat and Fin prim-               context with congrArg, choosing symmetry if the search
itives. The theorem refers to that helper when constructing            used the reverse direction. It then composes the lifted equal-
the magma, and finite decision closes the same logical goal.           ity with the instantiated target equation by transitivity. The
Packed-table witnesses use a natural-number payload and an             generated source consequently resembles
indexing expression in the helper body. Arithmetic families            have eA (...) : lhsA = rhsA := by exact h ...
print their closed form directly. Both routes keep multi-digit         have eB (...) : lhsB = rhsB := by
entries away from finOpTable while leaving the operation                  have lifted := congrArg C (eA ...)
transparent to the kernel.                                                exact lifted.trans ...
   The certificate has two independent failure modes. The              ...
operation may not be a countermodel, in which case finite              exact finalEquality
decision fails with an ordinary proof error. Or the source
                                                                       where actual variable binders, contexts, and equation sides
may use a dependency outside the policy, in which case
                                                                       are printed from the replay graph. No saturation data struc-
inspection classifies it as incomplete. Development probes
                                                                       ture or KBO comparison is imported into Lean 4. The certifi-
must run through the complete official policy: an earlier
                                                                       cate states only the equational consequences needed for the
permissive harness omitted the declaration restriction and
                                                                       final chain.
made a rejected arithmetic shape appear usable. Only the
                                                                          This proof shape also supports robust recovery. If an exact
official runner result was retained as evidence.
                                                                       term is difficult for elaboration because an implicit argument
6.2   Infinite countermodel transaction                                is ambiguous, the robust printer adds local type information
                                                                       or a small closing alternative around that step. It never re-
An infinite witness cannot delegate universal checking to
                                                                       places a missing inference with an axiom. Because reachable
finite reflection. The Austin path first matches the parsed
                                                                       nodes are emitted once, a clause used by several descendants
hypothesis against a stored law up to renaming. It selects an
                                                                       is shared by name rather than duplicating its derivation.
operation 𝑓 : N → N → N, instantiates a fixed proof that 𝑓
satisfies the law, and evaluates candidate tuples until the goal       6.4 Acceptance as the commit point
sides differ. Emission packages N, the magma instance, the
                                                                       In Solo mode the solver sends the complete source in a judge
hypothesis theorem, and a function that turns any assumed
                                                                       request. The proxy writes the judge-controlled problem mod-
goal equality at the chosen tuple into a contradiction.
                                                                       ule, compiles the candidate, runs dependency inspection, and
    The hypothesis theorem is the expensive part of the source.
                                                                       returns one of the documented statuses. Only the accepted
Its core-only version is a sequence of named local facts about
                                                                       status commits a solution row. All other statuses preserve
the operation followed by the target identity. The goal refuta-
                                                                       enough error text for robust re-emission or later fallback,
tion is intentionally concrete. It applies the universally quan-
                                                                       subject to the remaining wall-clock budget.
tified conclusion to the stored natural-number tuple and uses
                                                                          Marathon cannot make interactive judge calls. Its commit
computation to show that the resulting equality is impossible.
                                                                       point is therefore split: the solver durably appends a com-
This division makes the reusable part of the mathematical
                                                                       plete candidate row, and the runner checks the last complete
construction visible while keeping each problem-specific
                                                                       candidate for each identifier after process exit. The append-
separation small.
                                                                       and-synchronize protocol ensures that termination between
    As with finite models, recognizing the hypothesis is not
                                                                       problems cannot corrupt already emitted source. This differ-
itself trusted. A renaming bug would instantiate a lemma at
                                                                       ence changes scheduling but not trust: the same verifier and
the wrong law, and Lean 4 would reject the resulting type.
                                                                       proof policy decide both tracks.
A wrong tuple would fail to close the negation. The kernel
therefore checks both the reusable model theorem and its
                                                                       7     Evaluation
application to the current judge-generated equations.
                                                                       7.1   Method and provenance discipline
6.3   Superposition replay transaction                                 Unless marked hosted, measurements in this section are
A successful G3 search returns a refuted negative goal plus            local runs of the official runner and deterministic Lean 4
a directed acyclic graph of selected inference recipes. Replay         judge. The main regression used official repository revision
begins from the nodes reachable from the refutation and                2848228ff490...; the harness completed without errors
topologically orders them; irrelevant saturation clauses are           on the operator host. The tested solver is v2.5, SHA-256
omitted. Hypothesis leaves become applications of the input            f2392533c9f4..., with byte count given in the abstract.
identity with a substitution for its universally quantified            Each result file is bound by the repository’s PROVENANCE.json.
variables. Derived leaves created by symmetry or reflexivity           The short hashes in the tables are prefixes of the full SHA-256
become the corresponding core constructors.                            values in that file.
                                                                   8
A Certificate-Producing Cascade for Equational Implication: The SAIR EQT2 Stage 2 Solver           Conference’17, July 2017, Washington, DC, USA


   The reported wall-clock time is the sum of per-row run-                    7.4   Distribution drill, Marathon, and hosted
ner measurements, not elapsed parallel makespan and not a                           playground
hardware-independent cost model. Solver stages with dead-                    The official-distribution drill uses the four published Stage
lines may take different paths under heavier load. “LLM”                     1 evaluation splits that were named as Stage 2 scoring cate-
counts language-model calls attributed by the runner; a zero                 gories. Each split contains published ground truth and uses
means the deterministic cascade produced the accepted cer-                   the asterisk input encoding. Table 2 reports full local judge
tificate.                                                                    acceptance and full agreement with those labels. Stage 2 does
                                                                             not reuse these problems, so the drill measures format and
                                                                             distribution readiness rather than evaluation transfer.
7.2   Six public sets                                                           The canonical Marathon measurement used the official
Table 1 reports the final six-set regression. All rows were                  batch runner and its normal_100 manifest. All rows were
accepted, every accepted row had one judge call, and no row                  accepted without tokens. The hosted-playground row is dif-
used the fallback model. The sum of the set sizes is 1,889. The              ferent in kind: it was run through the official playground
earlier frozen v1 solver accepted 1,875 of those rows; v2 adds               interface on the hosted judge and is recorded as an exter-
the structured false stages and G3 proof engine described                    nal operator attestation, because the playground emits no
above. We report v1 only as development context, not as a                    repository-committable ledger. Across the four evaluation
comparison against another entrant.                                          categories the attested runs record acceptance of every at-
  The totals establish regression coverage of these public                   tempted problem with no rejected or errored rows and no
artifacts only. The private evaluation set is separate, and                  language-model calls. It is explicitly not an official leader-
public-set tuning is possible. We do not treat Table 1 as a                  board score.
hidden-set estimate.                                                            The hosted record further reports means by verdict: 2.69
                                                                             seconds for false rows and 7.08 seconds for true rows, with
                                                                             maxima 6.5 and 23.8 seconds, respectively. Those values
                                                                             include hosted orchestration and certificate checking as ex-
7.3   Component-level interpretation
                                                                             posed by the playground, and should not be compared di-
The superseded v1 baseline left fourteen public residuals:                   rectly to the local prover-only benchmark below.
eleven true implications without a deterministic proof inside
its budgets and three false implications without a model in                   7.5   Focused prover measurement
its available families and carriers. The v2 development was
organized around those failure classes. G3 plus the tautology-               To test the G3 search independently of the full cascade, de-
deletion correction supplies certificates for the true resid-                velopment used a corpus of 254 ETP pairs selected because
uals; the large-carrier, Latin-propagating, structured, and                  an existing Vampire derivation was available and the earlier
infinite-carrier paths supply witnesses for the false residuals.             prover found them difficult. Under a thirty-second per-pair
Replaying the residual set alone records fourteen accepted                   prover cap, the optimized engine found all 254 derivations;
certificates, whereas the six complete sets provide a regres-                maximum prover time was 2.7 seconds and the sum was
sion check that stage ordering and printers preserve the                     sixteen seconds. On all 819 public true problems under the
previously accepted cases.                                                   quick cap, the prover found all proofs with median one mil-
   This history is diagnostic, not a controlled ablation study.              lisecond and maximum 1.2 seconds. These are prover-only
Several changes were introduced together, and a row may                      measurements on the development machine, not judge wall-
now be solvable by more than one stage. The paper there-                     clock time and not a comparison claiming superiority over
fore attributes mechanisms only where the engineering notes                  Vampire. Vampire served as a source of hard instances and
contain a direct replay, such as hard3_0314 for tautology                    derivation guidance.
deletion and hard1_0062 for Latin propagation. It does not                      These focused results are recorded in docs/TRUE_SIDE_
assign an aggregate percentage gain to individual compo-                     G3_PROVER.md; they have no standalone hash-bound runner
nents.                                                                       ledger and are therefore not included in the ledger tables.
   The order of the cascade also affects the observed wall
totals. A true row may incur the shallow false-family cost                    7.6   Bounded language-model measurement
before receiving a quick proof; a false row may incur direct                  Before the v2 deterministic extensions, a fixed-configuration
proof checks before finite-model search. These costs are                      run exercised the organizer-pinned gpt-oss-120b fallback
intentional because the early stages reduce resource use                      on six unsolved sample_20 residuals. It solved zero of the
across both branches: inexpensive structured countermodels                    six. Pilot and canonical runs also produced different first
avoid proof saturation, while direct proof patterns avoid                     attempts despite the advertised zero temperature and fixed
table search. The six-set totals measure the integrated policy,               seed. The canonical run cost $0.1350 in total, measured from
not isolated engine speed.                                                    provider credits-balance deltas rather than runner logs —
                                                                         9
Conference’17, July 2017, Washington, DC, USA                                                         Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


Table 1. Local official-runner regression for solver v2.5. “Wall” is the sum of per-row wall-clock seconds. Each row names its
immutable ledger and SHA-256 prefix.

Set            Accepted LLM Judge Wall (s) Ledger provenance
sample_20          20/20       0      20        67.53   results/v2_sample_20_official_2848228.json
                                                        b17eaff452d2...
sample_200       200/200       0     200    964.12      results/v2_sample_200_official_2848228.json
                                                        dcf830de6199...
hard1              69/69       0      69    559.81      results/v2_hard1_official_2848228.json
                                                        7724566d1ceb...
hard2            200/200       0     200 1250.67        results/v2_hard2_official_2848228.json
                                                        3e68548945d4...
hard3            400/400       0     400 2857.38        results/v2_hard3_official_2848228.json
                                                        c9f98750e018...
normal         1000/1000       0    1000    4128.3      results/v2_normal_official_2848228.json
                                                        27c756482d15...


Table 2. Additional measurements. Local drill and Marathon rows name their ledger files and SHA-256 prefixes. The hosted
row is an operator attestation recorded in the hosted_playground_measurement entry of PROVENANCE.json; the playground
interface did not emit a repository ledger file.

Measurement                                     Accepted LLM/tokens                      Wall statistic Ledger provenance
evaluation_order5                                 200/200            0 calls              sum 583.29 s   results/official_distribution_drill/evaluation_order5_
                                                                                                         results.json
                                                                                                         422ecdf5a856...
evaluation_extra_hard                             200/200            0 calls            sum 1735.26 s    results/official_distribution_drill/evaluation_extra_hard_
                                                                                                         results.json
                                                                                                         99d16aecd72f...
evaluation_hard                                   200/200            0 calls              sum 889.03 s   results/official_distribution_drill/evaluation_hard_
                                                                                                         results.json
                                                                                                         4505248a3531...
evaluation_normal                                 200/200            0 calls            sum 2288.06 s    results/official_distribution_drill/evaluation_normal_
                                                                                                         results.json
                                                                                                         2377747990d8...
Marathon normal_100                               100/100         0 tokens         full default budget   results/marathon/normal_100_summary.json
                                                                                                         28fc79269ede...
Hosted playground (evaluation_normal)             200/200            0 calls mean 4.89 s/problem         PROVENANCE.json:hosted_playground_measurement
                                                                                                         artifact 7916cbc2...



about $0.023 per residual item under the sixteen-round cap.                       8      Honest Boundary and Reproducibility
Per-call latency and token telemetry are recorded as unavail-                     8.1     Hosted result: PENDING
able in the run notes, so no per-call figures are reported here.
                                                                                  At the time of this draft there is no hosted leaderboard score
We report this bounded negative measurement of one model,
                                                                                  or rank. The hosted playground is a diagnostic service and is
provider route, solver version, prompt, and residual set. It
                                                                                  labeled as such. The six-set and distribution-drill results are
does not support a general statement that language models
                                                                                  local official-runner measurements. None of them establishes
are ineffective for theorem proving or for this competition.
                                                                                  transfer to the hidden evaluation distribution.
   The executed pre-fix solver is bound in docs/LIVE_RUN_
                                                                                     There is also no completeness theorem for either branch.
NOTES.md by SHA-256 prefix 22a0bc846288...; the canon-
                                                                                  Structured countermodels cover chosen families, the finite-
ical row data are in results/sample_20_live.json. Be-
                                                                                  model search has carrier and time bounds, and the superpo-
cause no ledger-file hash for this historical run appears in
                                                                                  sition implementation deepens only until its deadline. Deep-
the claims provenance, it is reported in prose rather than the
                                                                                  stage outcomes can vary with machine load even though the
hash-bound tables.
                                                                                  judge’s verdict on a fixed certificate is deterministic. We make
                                                                                  no performance-superiority claim over another solver or
                                                                                  prover. The empirical statement is exactly that the archived
                                                                                  certificates were accepted in the recorded runs.


                                                                             10
A Certificate-Producing Cascade for Equational Implication: The SAIR EQT2 Stage 2 Solver            Conference’17, July 2017, Washington, DC, USA


8.2   Threats to validity                                                     the frozen solver.py. For example, the public normal set
The public suites influenced solver development. The four-                    uses
teen v1 residuals motivated particular prover and counter-                    python3 -m pipeline.runner \
model changes, and the E168 drill motivated the fixed central                     --submission /path/to/submission \
groupoid. Full regression shows that those changes integrate                      --problems examples/problems/normal.jsonl \
without losing earlier rows; it does not measure performance                      --output /tmp/normal-results.json
on an independently sampled corpus. The distribution drill                    The Marathon replay uses scripts/run_marathon.py, the
is broader but is still published Stage 1 data, and its ground                canonical normal_100.jsonl manifest, and an output di-
truth may share construction patterns with the public suites.                 rectory outside a read-only checkout. Recomputed output
   Wall-clock totals combine Python search, process over-                     hashes should be recorded as a new run rather than over-
head, and Lean 4 checking under one operator-host environ-                    writing the archived ledgers.
ment. They are appropriate for detecting large regressions                        The Lean 4 4.32 compatibility corpus was run in an ex-
within that setup but should not be read as portable run-                     ternal directory and is described in the provenance record;
times. Parallel worker load affects time-budgeted deepening,                  it is not presently packaged as a one-command repository
and filesystem caching affects Lean 4 startup. The hosted-                    test. This is a reproducibility limitation. The official harness,
playground mean times partially address this environment                      freeze checker, ledger files, and public-runner commands
gap, but playground selection and daily interaction are not                   are available locally; hosted playground interaction and any
the same protocol as final evaluation.                                        future leaderboard submission require organizer infrastruc-
   Finally, kernel checking validates each emitted theorem                    ture.
relative to the judge’s imported environment and allowed ax-
ioms. It does not validate that the benchmark labels, competi-                   A measured outer boundary. Shortly before submis-
tion problem generator, or provenance narrative are correct.                  sion the organizers released two additional official sets. On
We mitigate the last concern with hashes and exact com-                       stage2_stress_test, announced as mirroring the final leader-
mands; benchmark construction and judge implementation                        board configuration, the frozen solver accepts 200 of 200
remain external assumptions.                                                  problems with no language-model calls; the set publishes
                                                                              no per-item reference labels, but the per-category verdict
                                                                              counts match the announced composition of twenty-five
8.3   Hash-bound evidence
                                                                              true and twenty-five false in all four categories, and ev-
PROVENANCE.json binds the frozen solver’s SHA-256 and                         ery accepted verdict is kernel-checked by the judge. On
byte count, the official repository and configuration revi-                   research_order5_hard — one hundred research-tier prob-
sions, each result-ledger hash, the Marathon outputs, the                     lems in which at least one side is an order-five Austin law,
compatibility corpus, and the hosted-playground record. The                   whose false direction provably admits no finite counter-
human-readable claims ledger states the maximum set of sup-                   model, and whose ground truth is in part unknown even
ported claims and separately lists prohibited inferences. The                 to the organizers — the frozen solver certifies none within its
repository script scripts/check_freeze.py recomputes                          budgets. Both ledgers are committed and hash-bound. The
the solver and ledger hashes, checks accepted-row metadata,                   pair delimits the system precisely: complete coverage of the
verifies the one-file submission layout, and fails closed on                  announced evaluation distribution, and a research frontier,
drift.                                                                        coinciding with open territory in the Equational Theories
   This structure is intended to prevent stale measurements                   Project, that finite methods do not reach.
from being attributed to a revised solver. Historical v1 and
intermediate v2 artifacts remain named as superseded. The                     9    Related Work
tables in this paper use the current v2.4 bindings from                          Equational theories. The Equational Theories Project
PROVENANCE.json, even where an older narrative report con-                    builds a collaborative implication graph for single magma
tains timings from a previous rerun.                                          identities and supplies formal proofs, finite models, and cu-
                                                                              rated problem data [3]. The SAIR task derives its laws and im-
8.4   Replay procedure                                                        plication setting from this project but imposes a distinct on-
Reproduction requires two checkouts: this artifact and the                    line solver and certificate interface. Cazares analyzes Stage 1
official Stage 2 judge at the pinned revision. In the artifact                of the challenge and its prediction setting [4]. Stage 2 changes
checkout, first run                                                           the observable output from a label to a judge-accepted proof
                                                                              or countermodel.
python3 scripts/check_freeze.py
                                                                                 Knuth’s study of central groupoids is directly relevant to
to check immutable bindings. In the official checkout, run                    the E168 witness family [7]. Our use is narrower than the
bash scripts/setup.sh, source .env.judge, and invoke                          structural theory: we embed one checked non-natural finite
the Solo runner with a submission-only directory containing                   model because natural constructions did not separate the
                                                                         11
Conference’17, July 2017, Washington, DC, USA                                               Haobo Ma, Wenlin Zhang, and Manuel Israel Cázares


goals encountered in the drill. The infinite-carrier Austin             Author contributions (CRediT)
models similarly draw on constructions represented in the               Haobo Ma: conceptualization, methodology, software (solver
Equational Theories Project rather than proposing a general             architecture and the systems foundation), investigation, vali-
finite-model theorem.                                                   dation. Wenlin Zhang: conceptualization, methodology, soft-
                                                                        ware, investigation, validation, data curation, project admin-
                                                                        istration, writing (original draft). Manuel Israel Cázares: vali-
   Superposition provers. Vampire [9], E [13], and                      dation (solver freeze verification — hash, file size, and single-
Prover9 [10] are mature first-order theorem provers imple-
                                                                        file contract compliance; evidence-ledger auditing across the
menting variants of resolution, superposition, completion,
                                                                        reviewed freezes); methodology (review of experimental de-
simplification, and given-clause saturation [9, 10, 13]. Our            sign and the claims–evidence boundary); writing (review
engine borrows standard ideas—ordered inference, KBO,                   and editing — full manuscript review and critical review of
demodulation, discrimination-tree retrieval, and age/weight             the presentation and claims).
selection—but specializes them to unit equations over one
binary symbol. The system-level difference is the output                References
contract: the search trace is compiled into a positive Lean 4
                                                                         [1] A. K. Austin. 1965. A Note on Models of Identities. Proc. Amer. Math.
equality proof acceptable under the competition policy.                      Soc. 16 (1965), 522–523.
We do not compare throughput or coverage against these                   [2] Leo Bachmair and Harald Ganzinger. 1994. Rewrite-Based Equational
systems.                                                                     Theorem Proving with Selection and Simplification. Journal of Logic
                                                                             and Computation 4, 3 (1994), 217–247.
                                                                         [3] Matthew Bolan, Joachim Breitner, Jose Brox, Nicholas Carlini, Mario
                                                                             Carneiro, Floris van Doorn, et al. 2025. The Equational Theories
   Proof assistants and certificate checking. Lean 4 is                      Project: Advancing Collaborative Mathematical Research at Scale.
both the certificate language and the final trusted checker [5];             arXiv preprint arXiv:2512.07087. arXiv:2512.07087 Project reposi-
Mathlib supplies the surrounding library in the official judge               tory: https://github.com/teorth/equational_theories.
environment [14]. The solver follows the proof-producing                 [4] Manuel Israel Cázares. 2026. Less Is More: Cognitive Load and the
automation pattern in which a fast untrusted procedure re-                   Single-Prompt Ceiling in LLM Mathematical Reasoning. arXiv preprint
                                                                             arXiv:2604.18897. arXiv:2604.18897
turns an object reconstructed or checked by a small trusted              [5] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem
kernel. Finite countermodels are likewise proof objects: ex-                 Prover and Programming Language. In Automated Deduction – CADE
haustive reflection closes the concrete finite statement, while              28 (Lecture Notes in Computer Science, Vol. 12699). Springer, 625–635.
infinite witnesses use explicit lemmas.                                  [6] Ukyo Honda, Soichiro Murakami, and Peinan Zhang. 2025. Distilling
                                                                             Many-Shot In-Context Learning into a Cheat Sheet. arXiv preprint
                                                                             arXiv:2509.20820. arXiv:2509.20820
                                                                         [7] Donald E. Knuth. 1970. Notes on Central Groupoids. Journal of
   Distillation artifacts. The competition is motivated by
                                                                             Combinatorial Theory 8 (1970), 376–390.
work on distilling many-shot context into a compact cheat                [8] Donald E. Knuth and Peter B. Bendix. 1970. Simple Word Problems
sheet [6]. The artifact here is executable rather than a natural-            in Universal Algebras. In Computational Problems in Abstract Algebra
language sheet: algebraic families, search control, and proof                (Proc. Conf., Oxford, 1967). Pergamon, 263–297.
printers are distilled into one source file. The fixed-configuration     [9] Laura Kovács and Andrei Voronkov. 2013. First-Order Theorem Prov-
                                                                             ing and Vampire. In Computer Aided Verification (CAV 2013) (Lecture
language-model measurement is included to document the                       Notes in Computer Science, Vol. 8044). Springer, 1–35.
development path, not to argue that symbolic search and                 [10] William McCune. 2005–2010. Prover9 and Mace4. Automated reason-
language models are mutually exclusive.                                      ing systems. https://www.cs.unm.edu/~mccune/prover9/
                                                                        [11] SAIR Foundation. 2026. Equational Theories Stage 2: Evaluation Setup
                                                                             and Official Repository. Competition rules and reference implementa-
                                                                             tion. https://github.com/SAIRcompetition/equational-theories-lean-
10    Conclusion                                                             stage2
The SAIR EQT2 Stage 2 contract rewards an answer only                   [12] SAIR Foundation, Damek Davis, and Terence Tao. 2026. Mathematics
                                                                             Distillation Challenge: Equational Theories, Stage 2. Official competi-
when the same artifact also supplies a machine-checked rea-                  tion overview. https://competition.sair.foundation/
son. The solver described here meets that contract with a               [13] Stephan Schulz. 2002. E – A Brainiac Theorem Prover. AI Communi-
cheapest-first combination of structured and irregular coun-                 cations 15, 2–3 (2002), 111–126.
termodels, infinite witnesses, and ordered unit superposi-              [14] The mathlib Community. 2020. The Lean Mathematical Library. In Pro-
tion, followed by replay through the Lean 4 kernel. Hash-                    ceedings of the 9th ACM SIGPLAN International Conference on Certified
                                                                             Programs and Proofs (CPP 2020). ACM, 367–381.
bound local regressions account for all measured public and
distribution-drill rows, and a separately labeled hosted play-
ground measurement exercises the announced toolchain.
The remaining boundary is explicit: no leaderboard result,
hidden-set claim, completeness theorem, or comparative
claim is available at this draft stage.
                                                                   12
