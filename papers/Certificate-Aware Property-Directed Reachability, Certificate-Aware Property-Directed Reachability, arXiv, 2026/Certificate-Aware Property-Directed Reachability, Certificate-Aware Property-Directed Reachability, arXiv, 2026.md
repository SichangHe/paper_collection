                                                                                                                                                                                 1




                                              Certificate-Aware Property-Directed Reachability
                                                                                   Arman Ferdowsi1 and Laura Kovács2
                                                         1
                                                           Faculty of Computer Science, University of Vienna 2 Faculty of Informatics, TU Wien
                                                                       Email: arman.ferdowsi@univie.ac.at, laura.kovacs@tuwien.ac.at



                                            Abstract—Property-Directed Reachability (PDR/IC3) is widely     size and checking cost is crucial, as it significantly lowers
                                         used for hardware safety verification. Most implementations opti-  workflow overhead.
                                         mize time-to-answer, but certified workflows also require compact,
                                         inexpensive-to-check, and reproducible certificates. We introduce     Once certificates become first-class artifacts, quality matters.
                                         CAPDR, whose ranker is fitted offline on a disjoint development    Two correct SAFE certificates for the same system may differ
                                         corpus, frozen, and used only to order PDR-generated proposals on  by orders of magnitude in size and checking cost. Oversized
                                         unseen instances to target solving time, certificate size, and checker
                                                                                                            invariants slow down or even prevent independent checking.
                                         time. The ranker remains outside the trusted computing base: it    They also complicate reuse in incremental verification and
                                         cannot bypass the SAT guards on blocker insertion and pushing;
                                         obligation scheduling remains fair, and every SAFE/UNSAFE          downstream reasoning. Moreover, modern PDR implementa-
                                         claim requires independent checker acceptance. CAPDR also          tions are heuristic-driven and may be nondeterministic, due
                                         defines certificate-centric metrics and replay logs for artifact-  for example to randomized SAT heuristics, clause database
arXiv:2605.16472v2 [cs.LO] 30 Jul 2026




                                         grade reproducibility. On the 2024 Hardware Model Checking         effects, and parallelism. As such, PDR may lead to certificates
                                         Competition bit-level safety benchmarks, CAPDR solves six more     that vary substantially across runs. This instability complicates
                                         instances than the same PDR engine with ranking disabled. Across
                                         each configuration’s checker-accepted solved set, the medians of   debugging, hinders regression bisection, and reduces confidence
                                         the certificate-size proxy and checker time decrease by 24.6% and  in certified workflows.
                                         49%, respectively. After the same post-hoc minimizer is applied       At the same time, the community has begun exploring
                                         to paired SAFE outputs, CAPDR certificates still contain 16.3%     machine learning to guide verification, including learning-
                                         fewer literals and have 38.5% lower checker time.
                                                                                                            guided PDR/IC3 variants [5] and learning-based algorithm
                                            Index Terms—Hardware model checking, property-directed selection for hardware model checking [6]. These directions
                                         reachability, proof-carrying verification, certificate checking, raise a practical requirement: learning should improve end-to-
                                         learning-guided heuristics
                                                                                                            end cost without enlarging the trusted computing base.
                                                                                                               In this work, we advocate certificate-aware PDR, in short
                                                                 I. I NTRODUCTION                           CAPDR, without changing what must be trusted. CAPDR
                                            Property-Directed Reachability (PDR), also known as IC3, is neither a new certificate format nor a new checker. It
                                         is one of the most effective SAT-based techniques for proving separates PDR-generated proposals, learned ranking, ordinary
                                         safety properties of finite-state hardware transition systems [1]. PDR control, and independent validation. The policy is trained
                                         A key attraction of PDR is that it naturally produces in- offline on prior instances, then frozen and reused without
                                         dependently checkable evidence (certificate): in the SAFE adaptation across unseen target instances, where it only orders
                                         case, an inductive invariant; in the UNSAFE case, a finite current proposals. This cross-instance deployment lets the one-
                                         counterexample trace. Historically, however, this evidence was time fitting cost be amortized over a recurring stream of related
                                         largely treated as a secondary artifact, while implementations bit-level verification tasks. Transfer quality is an empirical
                                         and benchmarks focused on wall-clock time and solved performance question rather than a soundness assumption.
                                         instances.                                                         A poorly transferred policy may waste search effort, but it
                                            This emphasis is shifting. The hardware model checking cannot bypass guards, remove the exact blocker fallback, alter
                                         competition (HWMCC) introduced mandatory certification for certificate semantics, or cause an unchecked claim.
                                         its bit-level safety track in 2024 and continued the workflow Our contributions are summarized below.
                                         in 2025 [2], [3]. In essence, certificate-based validation is         • Certificate-aware objective. We define a run-level cost
                                         now a standard mechanism for increasing the trust, repro-               model over runtime, certificate size, and independent
                                         ducibility, and interoperability of verification results, e.g., in      checker time, turning PDR into a controllable optimization
                                         software verification [4]. This reflects an underlying principle        process (Section IV-A–Section IV-E).
                                         in automated reasoning: heuristic search need not be trusted          • A soundness-transparent learning interface. We formalize
                                         when correctness is discharged by an independent checker that           ranking events, development-time pairwise preferences
                                         validates the emitted certificate. As a consequence, certificates       induced by the run-level objective, and frozen deployment.
                                         become persistent workflow artifacts rather than merely internal        The policy only orders verifier-generated proposals, while
                                         byproducts. They are archived, rechecked, compared across               ordinary PDR guards and the independent checker preserve
                                         versions, and reused downstream. Consequently, reducing their           correctness (Section IV-C–Section IV-F).
                                            This is an extended version of the paper published at the Formal Methods   • Replay logs for reproducibility. We propose a compact
                                         in Computer-Aided Design (FMCAD 2026) conference.                               replay log that records nondeterministic choices together
                                                                                                                                       2



     with the solver-derived artifacts needed to determinize          and reuse learned information, e.g., via searching for i-good
     re-execution (Section IV-F–Section IV-G).                        lemmas [15]. More recently, extended-resolution reasoning has
   • Soundness of CAPDR is established, in a policy-                  been integrated into PDR to improve proof power [16], and
     independent manner (Section V).                                  dedicated SAT-solver optimizations tailored to IC3 workloads
   • Experimental evaluation under a disjoint develop-                have been shown to yield substantial speedups [17]. Another
     ment/evaluation protocol. On certified hardware bench-           relevant line augments IC3 with internal signals, allowing
     marks, frozen-policy evaluation on held-out instances            invariants over an enlarged variable vocabulary when no
     reduces certificate size and checker time while improving        concise latch-only invariant exists [18]. This line is particularly
     solved coverage. We additionally apply one shared imple-         relevant to our optional auxiliary-variable modes: unlike such
     mentation of the post-hoc minimal safe inductive subset          approaches, CAPDR makes the checker-facing certificate
     (MSIS) method of [7] to paired baseline and CAPDR                interface explicit by requiring either an X-only certificate
     SAFE invariants, showing that the online-search advantage        accepted by the base checker or an extended certificate
     survives equal postprocessing (Section VI).                      accompanied by a conservative auxiliary-state relation. CAPDR
Paper organization: Section II reviews related work. Section III      can incorporate such techniques as optional guarded actions,
recalls PDR and certificate checking. Section IV presents             enabling controlled trade-offs between solver runtime and
CAPDR. Section V proves checker-relative soundness, and               certificate-centric metrics.
Section VI evaluates the approach.
                                                                      C. Learning-guided verification
                     II. R ELATED W ORK                                  DeepIC3 [5], learned lemma prediction [19], LeGend [20],
A. Certification in hardware model checking                           and A-IC3 [21] use learning to improve PDR/IC3 search. Btor2-
                                                                      Select [6] applies learning at the algorithm-selection level, while
   Certification in hardware model checking predates                  IC3-Evolve [22] evolves solver heuristics offline and admits
HWMCC’24, including witness-circuit certification and strati-         results through independently checked proofs or witnesses.
fied certification for k-induction [8], [9]. HWMCC’24 made            The cited evaluations principally target solving performance,
certificates mandatory for the bit-level safety track [2], and        lemma prediction, or strategy selection. They do not report
HWMCC’25 continued this workflow while requiring certifi-             the same combination of checker-accepted CNF-invariant size,
cates for satisfiable bit-level liveness results [3]. Certification   independently measured checker time, and replay fidelity under
is not limited to the core model checking algorithm: certifying       a common certificate interface. A-IC3 also updates a bandit
preprocessing has been developed for phase abstraction [10],          policy from online feedback, whereas CAPDR fits its ranker
and compositional certification frameworks show how to                only on the development corpus and freezes it for deployment.
combine certificates across decomposed problems [11]. CAPDR              Our headline baseline is our implementation of Bradley’s
is orthogonal to these efforts: rather than proposing a new           PDR algorithm [1]. Within the paired experiments, baseline
certificate format, we make the heuristic search inside PDR           PDR and CAPDR share the solver-facing core, preprocessing,
certificate-aware and explicitly optimize for downstream check-       resource limits, certificate emission, and checker. They differ
ing cost.                                                             only in the order of verifier-generated choices, together with the
   A closely related direction studies how to extract, certify,       separately labeled optional post-fixpoint pass. This controlled
or minimize invariants once they have been found, including           internal comparison isolates the effect of certificate-aware
minimal safe inductive subsets and proof-certificate extraction       guidance within our engine. We do not claim that the baseline
for model checkers [7], [12], [13]. Ivrii et al. [7] start from an    is the strongest available HWMCC PDR implementation. A
already obtained conjunctive normal form (CNF) invariant and          total-tool comparison with learning-guided systems remains
search for a subset-minimal safe inductive subset. In contrast,       informative for coverage, but it cannot isolate ranking because
CAPDR changes the online PDR search, so it can discover               preprocessing, SAT tuning, lemma synthesis, invariant emission,
different lemmas and reach a different fixed point before any         and checking infrastructure also differ.
post-fixpoint reduction is applied. The two approaches are
therefore orthogonal rather than substitutes. We evaluate both
                                                                      D. Proof formats and trustworthy checking
a lightweight checker-preserving greedy pass (INV- MIN) and a
fair paired comparison in which the same combined MSIS                   Trustworthy reasoning has a long history in SAT and
implementation of [7] is applied to baseline and CAPDR                satisfiability modulo theories (SMT). DRAT proofs and the
invariants.                                                           DRAT-trim checker [23] provided an expressive and practical
                                                                      proof format for SAT, and LRAT adds hints that enable efficient
                                                                      checking in trusted systems [24]. Efficient LRAT checking
B. Strengthening and optimizing PDR                                   integrated with modern SAT solvers is demonstrated in [25],
   Since the first version of IC3 [1], performance improvements       and formally verified checking has also been developed [26].
have been made both at the algorithm layer and at the SAT-               Recent work extends clausal-proof certification to Lean,
solver interface. For example, removing activation literals           importantly via a verified Lean checker [27] for substitution-
from single-clause assumptions can speed up PDR-style                 redundancy proofs; this yields a clausal proof system gen-
workloads [14]. Recent work has also investigated lemma-              eralizing propagation redundancy (PR) and resolution asym-
quality criteria and strategies that improve the ability to push      metric tautology (RAT). For SMT, Alethe [28] and tools
                                                                                                                                             3



like Carcara [29], as well as proof reconstruction into Is- C. Property-Directed Reachability (PDR/IC3)
abelle/HOL [30] and Lean [31], show how solver outputs can be
                                                                            PDR incrementally constructs a sequence of clause sets
independently validated. Extending DRAT-style proofs to SMT
                                                                         (“frames”) F0 , F1 , . . . such that: (i) F0 is initialized from Init,
further highlights the broader relevance of proof logging [32].
                                                                         (ii) each Fi over-approximates the states reachable within i
CAPDR complements these efforts by focusing on certifying
                                                                         steps, and (iii) the sequence is monotone (Fi ⇒ Fi+1 ). The
model checking outcomes (invariants/traces) and by making the
                                                                         PDR algorithm searches for counterexamples to induction
search procedure certificate-aware while keeping the correctness
                                                                         (CTIs) at successive frames and blocks them by learning
argument entirely checker-based.
                                                                         clauses that exclude the offending state while remaining
                                                                         inductive relative to the previous frame. Clauses that satisfy
                          III. BACKGROUND                                the corresponding push condition can be propagated forward,
   We briefly recall the transition-system model, the strengthening later frames. When, after blocking and pushing,
SAFE/UNSAFE certificate view adopted in this paper, and two consecutive frames coincide, their common clause set
the PDR/IC3 and certificate notions used later.                          is an inductive invariant and therefore a SAFE certificate. If
                                                                         blocking reaches the initial frame, the predecessor chain yields
                                                                         a concrete counterexample trace; see [1], [33].
A. Transition systems and safety
                                                                            Modern PDR implementations differ primarily in how they
   We consider finite-state transition systems over Boolean state perform generalization, how they order proof obligations,
variables X (latches) and Boolean input variables U . A system which are pending blocking tasks, and how they manage
is specified by a triple (Init(X), Trans(X, U, X ′ ), Prop(X)), incremental SAT queries; a classic implementation-oriented
where Init characterizes initial states, Trans is the transition treatment is [34].
relation, and Prop is a safety property that must hold in all
reachable states.
                                                                                          IV. C ERTIFICATE -AWARE PDR
Definition 1 (Reachable state). A state x is reachable if
there exists a finite sequence of inputs u0 , . . . , uk−1 and              In this section, we present CAPDR as a certificate-aware
states x0 , . . . , xk such that Init(x0 ), Trans(xi , ui , xi+1 ) for   variant  of PDR/IC3 that, by adding an offline learning ranker,
all i < k, and xk = x. We denote the set of reachable states             jointly targets time-to-answer, certificate size, and checker cost
by Reach.                                                                without   adding   the learned ranker to the trusted computing
                                                                         base. It ranks PDR-generated choices at four choice points
Definition 2 (Safety). The system is safe if and only if every (CPs), namely blocker generalization (CP1), obligation ordering
reachable state satisfies
                            the safety property. Formally, ∀x. x ∈ (CP2), clause pushing (CP3), and optional guarded extensions
Reach ⇒ Prop(x) .                                                        (CP4), defined with their control conditions in Sections IV-C
                                                                         and IV-D. Fig. 1 shows the division between learned ranking,
B. Certificates                                                          guarded PDR control, and independent checking.
                                                                            Offline development uses guarded continuations and the
   A standard way to certify safety-verification outcomes is
                                                                         run-level objective over solving time, certificate size, and
via explicit, independently checkable artifacts: an inductive
                                                                         checker cost to derive pairwise preferences and fit a ranker
invariant in the SAFE case and a counterexample trace in the
                                                                         on prior instances. Replay metrics measure reproducibility
UNSAFE case.
                                                                         (Sections IV-E and IV-F). The fitted ranker is then frozen and
Definition 3 (Safe certificate). A safe certificate is a Boolean reused unchanged on unseen targets.
formula Inv (X) over the state variables satisfying:                        During deployment, at each choice point the verifier generates
                                                                         a finite proposal set, the frozen ranker orders it, and ordinary
                                    Init(X) ⇒ Inv (X)               (1)
                                                                         PDR control governs commitment. CP1 and CP3 change frames
                                              ′           ′
             Inv (X) ∧ Trans(X, U, X ) ⇒ Inv (X )                   (2) only after SAT guards succeed, CP2 selects the next obligation
                                    Inv (X) ⇒ Prop(X)               (3) subject to fairness, and CP4 retains conservative validation.
                                                                         Deployment performs only feature extraction, scoring, and
   In base mode, where the certificate uses only the original ordering, with no online objective evaluation, rollout, or per-
state variables X, checking Eq. (1)-Eq. (3) reduces to three SAT proposal checker call. SAFE/UNSAFE is reported only after
queries (unsatisfiability checks), and is typically much cheaper checker acceptance.
than re-running model checking from scratch. Competition-
grade certification frameworks often use more structured
encodings of invariants (e.g., witness circuits) and establish A. Separation and trust boundary
the certificate’s checkability and semantics in a dedicated
                                                                            In CAPDR, learning may affect search but never the correct-
checker [2].
                                                                         ness argument. The trusted computing base consists only of a
Definition 4 (Unsafe certificate). An unsafe certificate is a finite standalone certificate checker: its parsing layer, the SAT engine
trace x0 , . . . , xk with inputs u0 , . . . , uk−1 such that Init(x0 ), used for SAFE certificates, the trace-evaluation/simulation
each step satisfies Trans(xi , ui , xi+1 ), and ¬Prop(xk ). This routine used for UNSAFE certificates, and any validation
can be checked by simulation or by SAT.                                  routine for the auxiliary-variable extension mode defined in
                                                                                                                                                                                                                                              4



    Offline development only


                                  run PDR and log                    matched continuations
       development                                                                                                       within-event pairs               fit pairwise ranker
                               e = (r, φ, A), features,            from the same proof state
       corpus Bdev                                                                                                     Jbe (a+ ) < Jbe (a− )                gθ (x) = θ > x
                                   guard outcomes                       estimate Jbe (a)



                                                                                                                                       freeze θ ?
                                                                                                                                       no online update

   Deployment on a target instance, untrusted search                                                                                                                                                 Trusted checking




                                                                                                                                                                                    trust boundary
                                        PDR/IC3 core       proposals         frozen scorer                           ordinary PDR control                                                             independent checker         accepted
       target model                                                                                     ordered                                                 certificate π
                                 frames, CTIs, obligations                  features xe (a)                        CP1 and CP3 SAT guards                                                               validate invariant        SAFE or
   (Init, Trans, Prop)                                                                                                                                         and replay log
                                    finite proposal set A                 scores gθ? (xe (a))                      CP2 fairness, CP4 checks                                                                  or trace             UNSAFE

                                                          Policy orders. PDR control commits. The checker validates.




Fig. 1: CAPDR overview and trust boundary. The ranker is fitted offline on the development corpus, frozen once, and reused without adaptation on unseen
target instances. It only orders verifier-generated proposals. CP1 and CP3 remain SAT-guarded, CP2 remains subject to fairness, CP4 retains conservative
validation, and the independent checker validates the final artifact before SAFE/UNSAFE is reported.



Section IV-B. Everything else, including the possibly nondeter-                                                                  C. PDR core invariants and guard checks
ministic certificate-producing verifier, the learned policy, feature                                                                To specify the learning interface precisely, we restate the
extraction, training, and hyperparameter tuning, is untrusted.                                                                   frame invariants and SAT guard checks that determine when
   Accordingly, all correctness claims are conditioned solely                                                                    a proposed state-changing action may be committed in PDR.
on checker acceptance. The policy may rank only alternatives                                                                     Recall that a frame Fi is a CNF over X. At any time, the
already admitted by the underlying algorithm, and any state-                                                                     engine maintains a finite prefix of frames F0 , . . . , Fk+1 for
changing action, such as learning or pushing a clause, is                                                                        a current depth k ≥ 0. We call level k the current frontier.
committed only after the corresponding PDR-style satisfiability                                                                  New frames are created lazily and initialized to Prop. For the
guard succeeds, or its conservative auxiliary-variable variant                                                                   algorithmic presentation, we assume that Prop has been fixed
when auxiliaries are present. Thus, learning can change the                                                                      once in CNF (or via a fixed clausal encoding shared by the
search order and which valid lemmas are found, but it cannot                                                                     verifier and the checker); by abuse of notation, we write Prop
by itself make an invalid certificate cross the trust boundary.                                                                  for that clausal form.
                                                                                                                                    Since safety properties may be violated already in the initial
B. Formal certificate semantics
                                                                                                                                 states, CAPDR first checks whether Init(X) ∧ ¬Prop(X) is
   In base mode, Va safe certificate is emitted as a CNF invariant                                                               satisfiable. If it is, the system is immediately UNSAFE with
Inv (X) ≡           C∈Inv C(X), where each C is a clause (a                                                                      a length-0 trace, and the run terminates with an UNSAFE
disjunction of literals over X). Its semantics is exactly that                                                                   certificate accepted by the independent checker. Hence, for the
of Eqs. (1) to (3). An unsafe certificate is emitted as a finite                                                                 remainder we may assume Init ⇒ Prop.
trace π = (x0 , u0 , x1 , . . . , uk−1 , xk ) with xi ∈ {0, 1}|X| and                                                               We maintain the standard PDR frame invariants for all
ui ∈ {0, 1}|U | . Its semantics is exactly that of Definition 4.                                                                 currently allocated indices:
   Optional strengthening may introduce auxiliary state bits
Y . To preserve soundness for the original system over X,                                                                            F0 ≡ Init                                                                                               (6)
CAPDR supports either projection mode, which emits an X-                                                                             Fi ⇒ Fi+1                 ∀0≤i≤k                                                                        (7)
only candidate invariant later validated by the base SAFE                                                                            Fi ⇒ Prop                 ∀ 1 ≤ i ≤ k+1                                                                 (8)
checker, or extension mode, which emits (Def , Inv (X, Y )).                                                                                                                    ′                                  ′
                                                                                                                                     Fi (X) ∧ Trans(X, U, X ) ⇒ Fi+1 (X )                                                    ∀ 0 ≤ i < k. (9)
Writing Def ′ (X ′ , Y ′ ) for the primed copy of Def (X, Y ),
define                                                                  Eq. (9) holds at every closed level i < k, meaning that
          ext
   Init ≜ Init(X) ∧ Def (X, Y ),                                        consecution from Fi to Fi+1 has been established. At the
                                                                        frontier level k, ruling out frontier CTIs establishes Fk (X) ∧
 Trans ext ≜ Trans(X, U, X ′ ) ∧ Def (X, Y ) ∧ Def ′ (X ′ , Y ′ ). Trans(X, U, X ′ ) ⇒ Prop(X ′ ), and any strengthening of F
                                                                                                                                    k+1
We require Def to be conservative under projection to X:                is justified either by a blocker check relative to Fk or by
                                                                        a successful push check. Hence, when after the push phase
                               ∀x. Init(x) ⇒ ∃y. Def (x, y),
                                                                        Fk ≡ Fk+1 , the common frame is inductive and thus a SAFE
                                                                   (4)
                                                                        certificate.
 ∀x, u, x′ , y. Trans(x, u, x′ ) ∧ Def (x, y) ⇒ ∃y ′ . Def (x′ , y ′ ).
                                                                   (5) Definition 5 (SAT encodings). All implications are checked via
                                                                        unsatisfiability: A ⇒ B iff A ∧ ¬B is UNSAT. We define and
  In extension mode, the checker validates both Def and Inv
                                                                        write UNSAT(Φ) and SAT(Φ) for (un)satisfiability queries to
on the extended system. Acceptance then implies safety of
                                                                        the underlying SAT backend on a fixed equisatisfiable clausal
the original system (Proposition 2). Since the experiments in
                                                                        encoding of Φ; when Φ is already in CNF, this is just Φ itself.
Section VI use base mode, here we restrict our attention to
the X-only case. More details about auxiliary extensions are Definition 6 (State-cube convention). A state cube is a complete
deferred to Appendix B.                                                 cube over X, i.e., a conjunction containing exactly one literal
                                                                                                                                      5



for each variable in X. Such a cube represents exactly one            D. Learning-guided choice points
concrete state. For a state cube d, its primed copy d(X ′ ) is the       The guarded control above leaves four choice points, at which
same conjunction over X ′ , constraining the next-state variables     the verifier must order a finite set of candidates. Candidate-set
to that state, and ¬d is the clause excluding that state. In the      membership asserts only syntactic and algorithmic admissibility.
obligation mechanism below, d and dpred always denote state           It does not mean that a clause insertion or push has passed its
cubes extracted from SAT models.                                      commitment guard. The policy supplies only an order.
   A proof obligation is a pair (i, d) where i ≥ 0 and d is           CP1    Learning-guided blocker generalization. After an obli-
a state cube over X representing one concrete target state.           gation   (i, d) passes the initial-state check and its predecessor
                     ′
Equivalently, d(X ) fixes the next-state variables to that state.     query   is  UNSAT, the exact fallback blocker is C0 ≜ ¬d. The
Each non-root obligation also stores the successor cube and           verifier  may   also construct generalized blockers
input valuation by which it was generated. When an initial                        C(d, i) ⊆ {¬d⋆ | d⋆ ⊆ d},        C0 ∈ C(d, i),
cube is reached, following these links yields a concrete suffix                  ⋆
ending in a bad state.                                                where d is obtained by dropping literals from the complete
   To find a bad successor at depth i, the engine checks              target cube d. Because d ⇒ d⋆ , every candidate C = ¬d⋆
                                                                    automatically satisfies the blocking condition Eq. (12). A
      SAT Fi (X) ∧ Trans(X, U, X ′ ) ∧ ¬Prop(X ′ ) .            (10) smaller subcube yields a shorter and logically stronger clause,
                                                                      but it may require more SAT effort or fail initiation or relative
If Eq. (10) is satisfiable, a model yields a current-state valuation inductiveness. The implementation seeds the finite set with
on X and a bad successor valuation on X ′ . The engine an UNSAT-core-derived subcube when available and explores
unprimes the X ′ -literals to obtain the bad-successor state cube additional subcubes by deterministic budgeted literal deletion.
d over X and creates the obligation (i+1, d).                         The learned policy orders this set, and the verifier commits the
   If i = 0, blocking has reached the initial frame and the stored first candidate that satisfies Eqs. (13) and (14). If all proper
obligation chain is emitted as a candidate UNSAFE trace. More generalizations fail, C0 remains available.
generally, before learning any blocker for an obligation
                                                             (i, d),    As an illustrative example, consider why learned ranking
the engine checks whether SAT Init(X)∧d(X) . If this query is not reducible to shortest-first ordering. Let the target cube
is SAT, then, because d is a complete cube, the target state be d = x1 ∧ ¬x2 ∧ x3 . The verifier-generated menu may
represented by d is an initial state. The stored successor links contain the one-literal clause Cs = ¬x3 , the two-literal clause
therefore yield a candidate UNSAFE trace, and no blocker is C1 = x2 ∨ ¬x3 , and the exact fallback C0 = ¬d = ¬x1 ∨
learned for d. Only when i > 0 and UNSAT(Init(X) ∧ d(X)) x2 ∨ ¬x3 . All three block the target cube, and Cs ⇒ C1 ⇒ C0 .
does PDR attempt to block (i, d) by the predecessor query:            Thus, ordering candidates by increasing length always tests the
                                                                    strongest generalization Cs first, although it may fail initiation
         SAT Fi−1 (X) ∧ Trans(X, U, X ′ ) ∧ d(X ′ ) .           (11) or relative inductiveness in the current frame. CAPDR may
                                                                      instead test C1 first when the available context indicates that it
If Eq. (11) is SAT, the model yields a concrete predecessor
                                                                      is more likely to pass the guards. Such context includes frame
valuation on X together with a witness input valuation on U ;
                                                                      information, recency, blocker and push history, and SAT-side
let dpred be the corresponding predecessor state cube over X.
                                     u                                statistics. Even when a shorter candidate passes, length alone
We store the successor link dpred −  → d, requeue (i, d), and add
                                                                      does not determine subsequent obligation generation, push
(i−1, dpred ). If Eq. (11) is UNSAT, then no state satisfying Fi−1
                                                                      success, convergence, or final checker time. A candidate is
can reach the target cube d in one step. The fallback (base)
                                                                      inserted only after
PDR blocker is C0 ≜ ¬d, the clause excluding exactly the
concrete state represented by d. More generally, CAPDR may               UNSAT(Init ∧ ¬C),             UNSAT(Fi−1 ∧ Trans ∧ ¬C ′ )
try a generalized blocker, but any clause C(X) actually inserted succeed. If every proper generalization fails, C remains
                                                                                                                              0
for obligation (i, d) must satisfy the same guard conditions:         available by Proposition 1.
                                    d(X) ⇒ ¬C(X)              (12)      Clause length is one CP1 feature, not a replacement for
                                                                     the policy. CP2 ranks proof obligations and has no clause-
                                 Init(X) ⇒ C(X)               (13)
                                                                     length notion. A CP3 push opportunity contains a clause, but
                                        ′           ′
           Fi−1 (X) ∧ Trans(X, U, X ) ⇒ C(X ).                (14)   its usefulness also depends on the source and target frames,
These conditions express target blocking, initiation, and relative   previous push outcomes, and the effect on convergence. Hence
inductiveness, respectively. Condition (13) is equivalent to         no single shortest-formula rule covers the three learned choice
UNSAT(Init(X) ∧ ¬C(X)), and condition (14) is equivalent            points.
to UNSAT Fi−1 (X) ∧ Trans(X, U, X ′ ) ∧ ¬C(X ′ ) .                   Proposition 1 (Base blocker is admissible after the initial-state
                                                                     check). If i > 0, UNSAT(Init(X) ∧ d(X)), and the predeces-
Clause insertion: When Eqs. (12) to (14) hold, the verifier
                                                                     sor query Eq. (11) for an obligation (i, d) is UNSAT, then the
may conjoin C to F1 , . . . , Fi , never to F0 . This preserves
                                                                     base clause C0 ≜ ¬d satisfies Eqs. (12) to (14).
monotonicity, closed-level consecution, and Fj ⇒ Prop by the
standard guarded insertion argument given in Appendix A. Thus        Proof. Let C0 ≜ ¬d. Since d is a state cube over X,
the policy only chooses which candidate C to try; insertion          we have d(X) ⇒ ¬C0 (X), so C0 satisfies the blocking
itself remains SAT-guarded.                                          condition Eq. (12).
                                                                                                                                        6



   Since UNSAT(Init(X) ∧ d(X)), we have Init(X) ⇒ (x0 , u0 , x1 , . . . , uk−1 , xk ), let bits(π) ≜ (k+1) · |X| + k · |U |.
¬d(X). Because C0 = ¬d, this is exactly the initiation condi- We define
tion Eq. (13). For the relative-inductiveness guard, consider                (
                                                                              lit(Inv ), if π = Inv (SAFE),
     UNSAT Fi−1 (X) ∧ Trans(X, U, X ′ ) ∧ ¬C0 (X ′ ) .
                                                                  size(π) ≜
                                                                              bits(π), if π is a trace (UNSAFE).
Because C0 (X ′ ) = ¬d(X ′ ), this is equivalent to                     Literal count is a syntactic size proxy for the emitted base-
                                              ′        ′             mode CNF invariant, not the sole certificate-quality measure
                                               
       UNSAT Fi−1 (X) ∧ Trans(X, U, X ) ∧ d(X ) ,
                                                                     and not a claim of semantic minimality. Equivalent invariants
which is exactly the predecessor query Eq. (11), assumed             can have different CNF representations. Clause count, the
UNSAT. Hence C0 satisfies Eq. (14).                                  clause-width distribution, the size of the checker encoding,
  Finally, ¬d ∈ C(d, i) by construction, and the blocking            and witness-circuit size are also meaningful. We use literal
loop scans the finite ordered candidate list until it finds a        count because it is defined directly on the emitted CNF and is
candidate satisfying the initiation and relative-inductiveness       independent of the checker implementation once that artifact
guards. Since C0 satisfies both, the loop must accept some           is fixed. The primary downstream measure is nevertheless the
candidate regardless of the policy ranking.                          independently measured checker time tchk . The experimental
CP2 Obligation ordering. Here the candidate set comprises the        conclusions are supported by both quantities rather than by
pending obligations currently eligible for processing, which         literal count alone.
we call ready obligations. The policy selects which obligation       Definition 8 (Scalarized objective). When a single scalar is
(i, d) is processed next. This scheduling decision does not          needed, we combine the run-level vector (t, size(π), tchk ) as
by itself modify any frame, although it can change which
predecessors and blockers are discovered later. A fairness rule                   J = α · t + β · size(π) + γ · tchk ,               (16)
such as bounded starvation ensures that a low-scored obligation
                                                                     with user-chosen weights α, β, γ ≥ 0. Thus J is simply a
cannot be postponed forever. Useful features include the frame
                                                                     tunable scalarization of solving time, certificate bulk, and
index, recency, requeue count, predecessor-chain depth, and
                                                                     downstream checking effort.
SAT-side history.
CP3 Pushing schedule and clause selection. For a learned                In the evaluated prototype, reproducibility is not folded
clause C ∈ Fi with i ≥ 1, a push attempt checks                      into J. Cross-seed stability and replay fidelity are reported
                                                                     separately in Section IV-F.
             Fi (X) ∧ Trans(X, U, X ′ ) ⇒ C(X ′ ),            (15)
                                                                        The proxy size(π) intentionally mixes two outcome-specific
equivalently UNSAT(Fi ∧ Trans ∧ ¬C ′ ). CP3 ranks eligible           measures: literal count for SAFE certificates and trace
push attempts and does not synthesize new clauses. A clause          bit count for UNSAFE certificates. Accordingly, aggregate
is added to Fi+1 only when Eq. (15) holds. The order can             SAFE+UNSAFE summaries using size(π) (or a scalarization
affect convergence and the fixed-point frame because successful      that includes it) should be read only as coarse workflow-level
pushes change the frames seen by later scheduling decisions.         bookkeeping across outcome types. Our main certificate-quality
CP4 Optional guarded extensions. Optional strengthening              analysis is therefore outcome-homogeneous, focusing on SAFE
methods may be exposed as policy choices only when their             invariants in Table III and Figs. 2a to 2c.
clauses obey the appropriate commitment guards and any                  We still report the underlying vector metrics (t, size(π), tchk ).
auxiliary variables have explicit checker-facing semantics as in     The local scorer introduced in Section IV-F is used only as a
Section IV-B. CP4 is disabled in the base-mode experiments.          surrogate for the action values induced by this global objective.
   Thus every choice point follows the same interface. The
verifier generates proposals, the policy orders them, and the
                                                                     F. Policy learning, deployment, and reproducibility
appropriate guarded or fair control decides what is committed.
                                                                     Ranking events and features. At a choice point CPr , the current
                                                                     proof state ϕ induces a ranking event
E. Run-level cost metrics and objective
   Given the guard-checked choices above, we evaluate a run                                     e = (r, ϕ, A),
by the vector (t, size(π), tchk ), where t is solving time, π is the
                                                                      where A is the finite set of blocker proposals for CP1, ready
emitted certificate, and tchk is the time taken by an independent
                                                                      obligations for CP2, eligible push attempts for CP3, or guarded
checker on the emitted certificate. Since checking cost depends
                                                                      extension proposals for CP4. For each a ∈ A, the verifier
on the checker and SAT engine, we treat tchk as the ground-
                                                                      computes a deterministic feature vector xe (a) ≜ ψ(r, ϕ, a). In
truth downstream cost. For learning, one may additionally log
                                                                      the evaluated prototype, ψ uses verifier-available attributes
proxies such as the number of SAT calls and their sizes. Below,
                                                                      including frame index, candidate length where applicable,
we define the certificate-size component size(π), and then use
                                                                      recency, blocker or push history, and SAT-side statistics. The
a scalarization only when a single optimization target is needed
                                                                      scorer assigns gθ (xe (a)), with higher values placed earlier
for learning or end-to-end reporting.
                                                                      in the order. At CP1 and CP3, selecting a means trying that
Definition 7 (Certificate-size P    proxy).   For   a  CNF    invari- proposal first while preserving all guards. It never means forcing
ant Inv , let lit(Inv ) ≜          C∈Inv |C|.  For   a  trace  π  =   an invalid state change.
                                                                                                                                  7



Development-time pairwise supervision. The objective J is a mismatch signals divergence caused by nondeterminism or
delayed run-level quantity, so it cannot be read directly from implementation drift.
the local proof state. Development therefore estimates a con- Stability and replay-fidelity metrics. For SAFE certificates, let
tinuation cost Jbe (a) for selected alternatives at the same event. canon(Inv ) denote the clause set obtained by sorting literals
A continuation begins from the same saved proof state, places within each clause and deleting duplicates. We measure cross-
a first, and then follows a fixed continuation policy with the seed instability by the Jaccard distance between canonicalized
usual guards, fallback rules, and fairness constraints. Matched clause sets from two seeds, and replay fidelity by the same
alternatives use the same remaining time and memory budget, distance between an original run and its deterministic replay.
solver configuration and seed, and post-action tie-breaking. The Lower is better, and exact replay gives ∆replayInv (s) = 0. The
first proposal is the only intentional intervention. The estimate exact formulas are given in Appendix D.
may come from a measured development continuation or from
an explicit offline rollout. A pairwise label is formed only G. Operational summary
when two alternatives from the same event have comparable
estimates under this common protocol. Missing or censored              In base mode, CAPDR follows the standard PDR/IC3 loop
continuations are omitted unless they receive the explicit failure and changes only proposal order. After the length-0 check, it
penalty defined in Appendix C. This within-event construction searches for a frontier CTI and creates a proof obligation. CP2
avoids comparing action costs across unrelated proof states schedules pending obligations subject to fairness. Predecessor
or benchmark instances. Writing a+ ≻e a− for the preferred search either extends the counterexample chain or reaches
alternative, the label is                                           an UNSAT query, after which CP1 orders candidate blockers
                                                                    and only guard-valid clauses are inserted. When the frontier
            a+ ≻e a− ⇐⇒ Jbe (a+ ) < Jbe (a− ).                      closes, CP3 orders guarded push attempts. If Fk ≡ Fk+1 , the
                                                                    common frame is emitted as a candidate invariant. If enabled,
For the linear ranker used in Section VI, let x+ = xe (a+ ), post-fixpoint minimization retains only edits preserving the
x− = xe (a− ), and ∆x = x+ − x− . Then                              three SAFE-checker conditions. SAFE or UNSAFE is reported
                              ⊤
                   gθ (x) = θ x,                                    only after checker acceptance, and rejection is treated as FAIL.
                                                                    Full pseudocode is given in Algorithm 1.
             ℓθ (a+ , a− ) = log 1 + exp −θ⊤ ∆x .
                                                   
                                                                       It is worth noting that according to Proposition 1, the
Minimizing the sum of these losses with L2 regularization           blocking  loop in Algorithm 1 is guaranteed to accept some
makes a lower-cost alternative receive a higher score. The          guard-validated candidate independently of the policy’s ranking.
complete objective and failure-penalty convention are given in
Appendix C.                                                                          V. S OUNDNESS A RGUMENT
Frozen deployment. After fitting, the learned parameter vector         What follows makes the trust boundary from Section IV-A
θ is frozen and reused unchanged across target instances. For precise. We first fix the checker model and the assumptions on
every event on a target instance, CAPDR computes the current the trusted components. We then prove that checker acceptance
features, evaluates the scorer, and applies fixed tie-breaking implies semantic correctness of SAFE and UNSAFE certificates,
to obtain a deterministic total order. It does not compute and finally lift these certificate-level guarantees to CAPDR
J or Jbe . It performs no rollout, parameter update, or per- itself. Consequently, the learned policy may affect search, but
candidate checker call. CP1 and CP3 scan the score order until it does not participate in the correctness argument.
a guard-valid proposal is found. CP2 selects the highest-ranked
ready obligation subject to fairness. CP4 remains subject to its A. Checker model and assumptions
conservative validation conditions. The final checker is invoked
                                                                       This subsection fixes the checker-level objects used in the
only on the emitted invariant or trace.
                                                                    rest of Section V. The following assumptions A1-A2 are
Applicability and transfer. The features describe local PDR
                                                                    the only metatheoretic assumptions about the trusted checker
contexts and candidates rather than benchmark identities, so the
                                                                    from Section IV-A: they state that its low-level reasoning and
frozen ranker can be reused on previously unseen systems and
                                                                    evaluation are correct.
its one-time fitting cost can be amortized over repeated certified
verification. Effective transfer is plausible when development Assumption A1 (Checker-query correctness): Answers returned
and target runs induce similar local decision distributions, but by the SAT engine used inside the checker are correct: if
it is not guaranteed. Nevertheless, although distribution shift UNSAT, the queried formula is unsatisfiable; if SAT, any
may reduce efficiency or certificate quality, soundness is not returned assignment satisfies the queried formula.
affected because guards, fairness, the exact CP1 fallback, and Assumption A2 (Parsing and evaluation correctness):
checker acceptance remain unchanged.                                The checker faithfully parses and semantically encodes
Replay log. To support artifact-grade reproducibility, the engine (Init, Trans, Prop) and the certificate, treats primed and un-
records tool and SAT-solver versions, configurations, seeds, primed variables consistently, correctly evaluates trace steps for
solver-derived objects that affect control flow, the attempted UNSAFE certificates, and correctly implements any validation
actions and guard outcomes, and hashes of the relevant contexts. routine used for extension-mode definitional extensions.
A replay reuses the recorded objects directly, or checks them          Under assumptions A1-A2, we define the acceptance condi-
against a determinized recomputation. A hash or guard-outcome tions of the checkers used throughout the proofs.
                                                                                                                                                                       8



Algorithm 1 CAPDR core loop in base mode.                                                        (Def , Inv (X, Y )). The extension-mode checker accepts if and
 1: /* Trivial counterexample of length 0 */                                                     only if (i) it validates Def by a procedure whose correctness
 2: if SAT(Init(X) ∧ ¬Prop(X)) then
 3:     extract an initial bad state x0 from the model                                           guarantees Eqs. (4) and (5), and (ii) it accepts Inv on the
 4:     set π ← (x0 )                                                                            extended system (Init ext , Trans ext , Prop) using the SAFE
 5:     if the UNSAFE checker accepts π then
 6:          return UNSAFE with π                                                                checks Eq. (17)-Eq. (19) over state variables (X, Y ).
 7:     else                                                                                        The next certificate-soundness results are semantic conse-
 8:          return FAIL
 9: Initialize F0 ← Init; F1 ← Prop; set k ← 0                                                   quences of these acceptance conditions. Assumptions A1-A2
10: Create further frames lazily; when Fk+1 is first created, initialize it as Prop              are needed only when relating those mathematical conditions to
11: Initialize obligation multiset Q ← ∅
12: while true do                                                                                the behavior of an actual checker implementation in Theorem 3.
13:      if SAT(Fk (X) ∧ Trans(X, U, X ′ ) ∧ ¬Prop(X ′ )) then
14:           extract the bad-successor state cube d over X by unpriming the model’s X ′
    assignment                                                                                   B. SAFE and UNSAFE certificates
15:          insert obligation (k+1, d) into Q
16:          while Q ̸= ∅ do                                                                     Theorem 1 (SAFE certificate soundness in base mode). If the
17:              choose and remove an obligation (i, d) from Q ▷ policy-guided, fair             SAFE checker in base mode accepts an invariant Inv , then
18:              if i = 0 or SAT(Init(X) ∧ d(X)) then
19:                   reconstruct a trace π ending in ¬Prop using the stored successor           the transition system satisfies the safety property Prop.
    links and input witnesses
20:                   if the UNSAFE checker accepts π then                                       Proof. Assume the SAFE checker in base mode accepts
21:                        return UNSAFE with π                                                  Inv . Then, by definition of checker acceptance, the formulas
22:                   else
23:                        return FAIL                                                           Eqs. (17) to (19) are UNSAT. Equivalently,
24:              if SAT(Fi−1 (X) ∧ Trans(X, U, X ′ ) ∧ d(X ′ )) then
25:                   extract the predecessor state cube dpred over X from the model’s X         Init(X) ⇒ Inv (X),
    assignment
26:                   store the predecessor/input witness information                            Inv (X) ∧ Trans(X, U, X ′ ) ⇒ Inv (X ′ ),
27:                   reinsert (i, d) into Q and insert (i−1, dpred ) into Q
28:              else                                                                            Inv (X) ⇒ Prop(X).
29:                   construct candidate generalized blockers C(d, i), i.e., clauses C =
    ¬d⋆ for subcubes d⋆ ⊆ d, with ¬d ∈ C(d, i)
30:                   order C(d, i) by policy score          ▷ fallback to deterministic order
                                                                                                    Let x be any reachable state. By definition of reachability,
31:                   for candidates C in that order do                                          there exist k ≥ 0, states x0 , . . . , xk , and inputs u0 , . . . , uk−1
32:                        if UNSAT(Init(X) ∧ ¬C(X)) and UNSAT(Fi−1 (X) ∧
    Trans(X, U, X ′ ) ∧ ¬C(X ′ )) then
                                                                                                 such that Init(x0 ), Trans(xi , ui , xi+1 ) for all i < k, and
33:                            add C to frames F1 , . . . , Fi                                   xk = x. We prove by induction on i ∈ {0, . . . , k} that Inv (xi )
34:                            break ▷ guaranteed by C = ¬d after the initial-state check
                                                                                                 holds.
35:      else
36:          attempt pushing learned clauses across frames F1 , . . . , Fk using guard              Base case (i = 0): Since Init(x0 ) and Init ⇒ Inv , we have
    Eq. (15)                                                            ▷ policy-guided order    Inv (x0 ).
37:          if Fk ≡ Fk+1 (canon(Fk ) = canon(Fk+1 )) then
38:              extract Inv ← Fk                                                                   Inductive step: Assume Inv (xi ) holds for some i < k. Since
39:              optionally minimize Inv by keeping only edits that preserve the three
    SAFE-checker SAT conditions
                                                                                                 Trans(xi , ui , xi+1 ) holds and Inv (X) ∧ Trans(X, U, X ′ ) ⇒
40:              if the SAFE checker accepts Inv then                                            Inv (X ′ ), it follows that Inv (xi+1 ) holds.
41:                   return SAFE with Inv                                                         Thus Inv (xk ) holds. Since xk = x and Inv ⇒ Prop, we
42:              else
43:                   return FAIL                                                                obtain Prop(x). Because x was an arbitrary reachable state,
44:          else                                                                                every reachable state satisfies Prop. Therefore the system is
45:              increment k ← k+1 and initialize Fk+1 ← Prop if needed
                                                                                                 safe.

SAFE checker (base mode): Given a transition system Proposition 2 (Soundness under conservative exten-
(Init(X), Trans(X, U, X ′ ), Prop(X)) and a candidate invari- sion).ext Assumeext Def satisfies Eq. (4)-Eq. (5), and let
ant Inv (X), the SAFE checker accepts if and only if all of (Init , Trans , Prop) be the extended system from Sec-
the following are UNSAT:                                               tion IV-B. If the SAFE checker accepts an invariant Inv (X, Y )
                                                                       for the extended system, then the original transition system
              Init(X) ∧ ¬Inv (X)                                  (17) (Init(X), Trans(X, U, X ′ ), Prop(X)) is safe.
              Inv (X) ∧ Trans(X, U, X ′ ) ∧ ¬Inv (X ′ )           (18)
                                                                       Proof. Let x = xk be reachable in the original system. Then
              Inv (X) ∧ ¬Prop(X).                                 (19) there exist k ≥ 0 and a sequence x0 , u0 , x1 , . . . , uk−1 , xk such
These are exactly the negations of Eq. (1)-Eq. (3).                    that Init(x0 ) and Trans(xi , ui , xi+1 ) for all i < k.
UNSAFE checker: Given (Init, Trans, Prop) and a trace π =                 We prove by induction on the prefix length j ∈ {0, . . . , k}
(x0 , u0 , x1 , . . . , uk−1 , xk ), the UNSAFE checker accepts if and that there exist y0 , . . . , yj such that Init ext (x0 , y0 ) holds and
only if:                                                               Trans ext (xi , ui , yi , xi+1 , yi+1 ) holds for all i < j.
                                                                          For j = 0, Init(x0 ) and Eq. (4) yield some y0 with
   • Init(x0 ) evaluates to true,
                                                                       Def (x0 , y0 ), hence Init ext (x0 , y0 ).
   • for all i < k, Trans(xi , ui , xi+1 ) evaluates to true, and
                                                                          For the inductive step, assume the claim holds for some j <
   • ¬Prop(xk ) evaluates to true.
                                                                       k. In particular, we have Def (xj , yj ) and Trans(xj , uj , xj+1 ).
Equivalently, it checks that π is a valid finite execution ending By Eq. (5) there exists y
                                                                                                            j+1 with Def (xj+1 , yj+1 ). By
in a bad state.                                                        definition of Trans ext , this implies
SAFE checker (extension mode): When auxiliaries Y
are present, the emitted SAFE certificate is a pair                                      Trans ext (xj , uj , yj , xj+1 , yj+1 ).
                                                                                                                                         9



Thus the claim holds for j + 1.                                            If CAPDR returns UNSAFE, it does so only after the
  Therefore             there    exist  y0 , . . . , y k such that       UNSAFE checker accepts π. By Theorem 2, the original system
(x0 , y0 ), . . . , (xk , yk ) is an execution of the extended           violates Prop.
system. Since the SAFE checker accepts Inv (X, Y ) on the
extended system, checker acceptance gives                                Corollary 1. Under assumptions A1-A2, CAPDR is sound
                         ext                                             regardless of the learned policy.
                  Init         (X, Y ) ⇒ Inv (X, Y ),
                                                                         Proof. The learned policy is consulted only inside the untrusted
   Inv (X, Y ) ∧ Trans ext (X, U, Y, X ′ , Y ′ ) ⇒ Inv (X ′ , Y ′ ),     search procedure. Whatever ranking it returns, every clause
and                                                                      insertion, push, or optional extension is committed only through
                     Inv (X, Y ) ⇒ Prop(X).                              the verifier’s guarded control logic, and CAPDR reports
                                                                         SAFE or UNSAFE only after the corresponding independent
Hence, by induction along the lifted execution, Inv (xk , yk )           checker accepts the emitted artifact. Hence the certificate-level
holds, and therefore Prop(xk ) holds.                                    hypotheses used in Theorem 3 are unchanged by the choice
   Since xk = x was an arbitrary reachable original state,               of policy. Therefore every SAFE/UNSAFE result returned by
all reachable original states satisfy Prop. Thus the original            CAPDR is correct regardless of the learned policy.
transition system is safe.
                                                                         D. Remark: completeness and progress
Theorem 2 (UNSAFE certificate soundness). If the UNSAFE                     Soundness is independent of completeness. An adversar-
checker accepts a trace π, the transition system violates Prop.          ial policy can still delay progress by prioritizing unhelpful
Proof. Let π = (x0 , u0 , x1 , . . . , uk−1 , xk ) be a trace accepted   candidates. To recover the usual completeness argument
by the UNSAFE checker. By the checker’s definition: (i)                  of finite-state PDR, the implementation should ensure that
Init(x0 ) holds, (ii) for all i < k, Trans(xi , ui , xi+1 ) holds,       the underlying baseline search remains guard-complete: (i)
and (iii) ¬Prop(xk ) holds.                                              blocking candidate sets are nonempty, with ¬d always available
   Items (i) and (ii) together show that x0 , . . . , xk is a concrete   when Eq. (11) is UNSAT, (ii) if the scorer is unavailable, the
execution of the transition system. Item (iii) shows the final state     engine reverts to a deterministic baseline order, and (iii) the
violates the safety property. Therefore there exists a reachable         scheduler is fair in the sense that every pending obligation and
state violating Prop, so the system is unsafe.                           every pending push opportunity is eventually served by that
                                                                         baseline order (bounded starvation suffices).
C. Soundness of CAPDR as a certificate-producing procedure
                                                                                      VI. E XPERIMENTAL E VALUATION
   The previous theorems establish correctness of certificates
                                                                    CAPDR improves the checker-accepted artifact, not merely
independent of how they were found. We now connect this to
                                                                 the verifier’s time-to-answer. We separate five questions:
CAPDR. A CAPDR run outputs either SAFE (with a candidate
                                                                 whether online guidance improves the certified workflow
invariant Inv ), or UNSAFE (with a candidate trace π). In both
                                                                 objective, whether the raw SAFE invariants become smaller and
cases, CAPDR reports the claim as final output only after the
                                                                 faster to check, whether the online-search advantage survives
corresponding checker accepts the emitted artifact; otherwise
                                                                 the same strong post-hoc minimizer applied to both methods,
the run is treated as FAIL, not as a SAFE/UNSAFE result. This
                                                                 whether replay removes residual nondeterminism, and which
reporting discipline is stated in Section IV-G and made explicit
                                                                 guarded PDR choice points contribute most. The CAPDR
in the full pseudocode of Algorithm 1.
                                                                 (learned) configuration measures the online-search contribution.
Theorem 3 (CAPDR soundness). Assuming assumptions A1- The CAPDR +INV- MIN configuration is reported separately as
A2,                                                              lightweight safe post-fixpoint minimization, while the PDR+
   • If CAPDR returns SAFE with a certificate accepted by        [7] and CAPDR + [7] configurations use one shared MSIS
      the appropriate SAFE checker (base mode or extension implementation.
      mode), then the original transition system satisfies Prop. A. Benchmarks, tool configurations, and protocol
   • If CAPDR returns UNSAFE with a certificate accepted by
                                                                    1) Benchmarks: We evaluate on the bit-level safety bench-
      the UNSAFE checker, then the original transition system
                                                                 marks from the Hardware Model Checking Competition
      violates Prop.
                                                                 (HWMCC), which provides bit-level instances in the AIGER
Proof. If CAPDR returns SAFE in base mode, it does so only format for and-inverter graphs together with a workflow based
after the base SAFE checker accepts Inv . By Theorem 1, the on independently checkable certificates. We use two disjoint
original system satisfies Prop.                                  benchmark corpora. The development corpus Bdev is the
   If CAPDR returns SAFE in extension mode, it does so only deduplicated bit-vector single-property AIGER subset of the
after the extension-mode SAFE checker accepts (Def , Inv ). HWMCC’20 benchmark archive [35], with all HWMCC’24
By definition of that checker, Inv is accepted on the extended benchmark names and canonical AIGER hashes removed (its
system and Def is validated against a criterion that guaran- SAFE subset contains 190 instances), and is used only for
tees Eqs. (4) and (5). Hence Proposition 2 applies, and the offline fitting, model selection, and ablation. This is a natural
original system satisfies Prop.                                  development source for HWMCC: it is competition-selected
                                                                                                                                   10



and bit-blasted to AIGER, matching the bit-level setting while         Training examples are within-event candidate pairs. A pair
remaining disjoint from the certificate-mandated HWMCC’24           is retained only when both alternatives have an observed
test corpus. The held-out evaluation corpus Beval is the full       development continuation cost or a rollout-estimated cost
319-instance HWMCC’24 bit-level safety archive. This archive        from the same checkpoint under the matched protocol in
is a natural target for CAPDR because HWMCC’24 made                 Section IV-F. The first proposal is the only intentionally
independently checkable certificates part of the bit-level safety   changed verifier choice. The alternative with lower scalarized
workflow [2]. No HWMCC’24 evaluation instance contributes           objective J is preferred. Timeouts, resource exits, and checker
training examples, tuning decisions, or online adaptation.          rejections receive the development-only failure treatment from
   2) Compared configurations: We distinguish configurations        Appendix C. The prototype uses the linear scorer and the
used for development ablations from the frozen configurations       L2 -regularized pairwise logistic loss from Section IV-F and
used for the held-out headline comparison. Development-             Appendix C. In ablations, events from disabled choice points
stage configurations are: PDR (baseline), CAPDR (random             are omitted and the remaining scorer is trained by the same
ranking), CAPDR (CP1 only), CAPDR (CP1+CP2), CAPDR                  procedure. The model is fitted once on Bdev , frozen, and
(CP1-CP3 full), CAPDR (CP1-CP3 full) + inv-min, and                 reused unchanged across every instance of Beval . No evaluation
deterministic CAPDR (CP1-CP3 full) + replay for replay-             benchmark contributes training examples, model selection,
fidelity evaluation only. Evaluation-stage configurations are       tuning decisions, or online adaptation. Regularization and
PDR (baseline), CAPDR (learned), and CAPDR (learned)                rollout-budget choices are made only on Bdev .
+ inv-min. The paired post-hoc experiment additionally uses            Each campaign records the split manifest, canonical hashes,
PDR+ [7] and CAPDR + [7] on the common SAFE subset;                 random seeds, replay logs, frozen-model identifiers, checker
these are not new solving configurations, but the same MSIS         outcomes, and per-instance logs used to regenerate Tables I
postprocessor applied to checker-accepted raw outputs. The          to III and Figs. 2a to 2c. Reported learned-policy runtimes
baseline is our implementation of [1]. All configurations use the   include feature extraction, scoring, and all guard checks, but
same preprocessing, incremental SAT backend and interface,          exclude the one-time offline fitting cost. For every configuration
resource limits, certificate emitter, and independent checker.      labeled +INV- MIN, the reported runtime t includes the post-
The learned configuration differs from the baseline only in         fixpoint minimization pass. We ran our experiments on a single
proposal ordering. The INV- MIN variant additionally removes        Windows 11 machine with an Intel Core i7-11800H CPU and
duplicate or subsumed clauses and greedily attempts clause          64 GB RAM, with a per-instance timeout of 1 hour and a
and literal deletions, retaining only edits for which Eqs. (17)     memory limit of 56 GB.
to (19) remain UNSAT; it makes no minimality claim.                    4) Metrics: We report the vector metrics (t, size(π), tchk )
   3) Implementation, training, and evaluation protocol: We         from Section IV-E and, when useful, the scalar objective
implement CAPDR as a prototype extension of a standard              J = αt + β size(π) + γtchk with (α, β, γ) = (1, 10−3 , 1).
incremental PDR/IC3 engine for AIGER bit-level safety. SAFE         The factor 10−3 weights 1000 certificate-size units as one
results are validated by a standalone SAT-based checker on the      second of scalar cost. The weights are fixed before evaluation,
discovered CNF invariant, and UNSAFE traces by independent          and the underlying vector metrics remain primary. For SAFE
simulation. All solved counts and medians include only checker-     instances, size(π) = lit(Inv ) and tchk is measured by the
accepted results. A verifier claim rejected by the checker is       standalone CNF-invariant checker. Since size(π) is outcome-
counted as FAIL, not as solved. UNSAFE traces receive no            specific, mixed SAFE/UNSAFE summaries in Table I are
special learning-based quality treatment. They are included to      workflow-level summaries. SAFE-only certificate quality is
maintain a uniform trust boundary in which every reported           reported in Tables II and III and Figs. 2a and 2b.
result is independently checked.                                       5) Stability protocol: Unless stated otherwise, solve counts
   These runs are controlled internal comparisons rather than       and the medians of t, size(π), and tchk are reported for the
HWMCC standings. We do not claim that our baseline is               fixed primary evaluation seed. The 10-seed campaign is used
the strongest available PDR engine. The host, preprocessing         only for instability and replay-fidelity measurements. Each
pipeline, solver integration, certificate representation, and       configuration is run under 10 seeds while varying only low-
checker differ from competition tools. In base mode, the emitted    level solver randomness; verifier-level tie-breaking remains
artifact is already a CNF invariant whose semantics is exactly      fixed except in the random-ranking control. For each SAFE
the three SAT checks in Eqs. (17) to (19). Therefore tchk           benchmark, we aggregate all pairwise cross-seed distances
                                                                               ′
measures that artifact directly. Certifaiger checks competition     ∆seed
                                                                      Inv (s, s ) by the median. Replay is evaluated separately by
witness circuits [2]. Using it here would first require a           deterministic re-execution from the recorded log and measuring
CNF-to-witness-circuit conversion and would mix conversion          ∆replay
                                                                      Inv against the original artifact. Distances are computed only
engineering with the effect of online ranking. We leave a           for seed pairs in which both runs produce SAFE certificates for
common witness-circuit workflow to future work.                     the same benchmark. Benchmarks with fewer than two SAFE
   For CP1–CP3, the prototype uses the feature map described        certificates for a configuration are omitted from the distance
in Section IV-F. At CP1, an action means trying a blocker           distribution, while coverage is reported separately. Table III
C = ¬d⋆ first within C(d, i). At CP2, it means servicing one        reports the median of these per-benchmark values over eligible
ready obligation next. At CP3, it means attempting one eligible     benchmarks, whereas Fig. 2c shows their distribution.
push first. The model never proposes a clause outside the
verifier-generated CP1 set and never bypasses a guard.              B. Results
                                                                                                                                                                                                                    11



TABLE I: Held-out results on the 319 HWMCC’24 bit-level safety                                           paired, all medians in Table II are computed on the 178
benchmarks. Medians are over each configuration’s checker-accepted solved
set. The “Unsolved” column includes timeouts, resource exits, and checker                                instances completed by both. Every completed postprocessed
rejections. Lower is better for t, size(π), tchk , and J. The reported median J                          invariant is accepted by the independent checker.
is the median of per-run scalarized costs, not J evaluated on the displayed
component medians.                                                                                       TABLE II: Fair paired post-hoc minimization on the common HWMCC’24
Configuration     Solved (SAFE/UNSAFE)   Unsolved   Med. t [s]   Med. size(π)   Med. tchk [s]   Med. J   SAFE subset. The + [7] rows use the same combined BIG+NFN implementa-
PDR (baseline)                     287        32        109.7          19365            1.24     151.1   tion of [7]. “Completed” is over all 180 paired inputs; all medians are over
CAPDR (learned)                    293        26        115.2          14596            0.63     142.4   the 178 inputs completed by both. Raw lit. is measured before postprocessing;
CAPDR + inv-min                    293        26        117.5          12785            0.55     140.5
                                                                                                         the remaining size and checker columns are measured after it. Lower is better.

                                                                                                         Configuration Completed Raw lit. MSIS clauses MSIS lit. tmsis [s] tchk [s]
                                                                                                         PDR+ [7]                178/180       19,842                 3,274         14,026           11.4        0.78
   1) Overall end-to-end results: Table I reports certified end-                                         CAPDR + [7]             180/180       14,731                 2,807         11,741            7.6        0.48
to-end performance on the held-out evaluation benchmarks
under the disjoint development/evaluation protocol from Sec-                                                From the displayed paired medians, the shared minimizer
tion VI-A3. The key online-search comparison is the baseline                                             removes 29.3% of the baseline’s raw literals and 20.3%
row against CAPDR (learned): neither row uses post-fixpoint                                              of CAPDR’s. The larger proportional reduction for PDR
invariant minimization. Thus the certificate reduction in this                                           is consistent with greater removable redundancy in its raw
comparison comes from CP1–CP3 guidance during PDR search,                                                fixed points. Nevertheless, equal postprocessing does not erase
not from a final cleanup pass.                                                                           the online-search aability-protdvantage: relative to PDR+ [7],
   Under the primary evaluation seed, CAPDR reduces unsolved                                             CAPDR + [7] has 16.3% fewer literals and 14.3% fewer
instances from 32 to 26 (six additional checker-accepted                                                 clauses, with 38.5% lower checker time and 33.3% less
solutions), while improving the deliverable substantially: the                                           postprocessing time. Thus the common minimizer narrows,
median certificate proxy shrinks by 24.6% (19,365 → 14,596)                                              but does not close, the gap. This suggests that CAPDR often
and the median independent checker time drops by 49% (1.24 s                                             reaches a different useful clause core, rather than merely
→ 0.63 s, about 2× faster checking). The median solving time                                             producing an invariant with less removable redundancy.
increases by about 5% (109.7 s → 115.2 s), consistent with
spending additional SAT effort on lemma generalization and                                               TABLE III: Development-only SAFE-invariant ablation on Bdev . Medians
pushing. Under the fixed weights (α, β, γ) = (1, 10−3 , 1),                                              are over each row’s certified SAFE set. The complement of the certified count
                                                                                                         comprises timeouts, resource exits, and checker rejections, all treated as FAIL.
these certificate improvements yield a lower median objective                                            The last column lists cross-seed Jaccard distance, except for the replay row
(151.1 → 142.4).                                                                                         where replay distance is given. Lower is better. For the replay row, the runtime,
   Post-fixpoint minimization (CAPDR +INV- MIN) is comple-                                               invariant-size, and checker-time entries are those of the original full-policy
                                                                                                         runs; only the final column reports replay fidelity.
mentary: it further reduces the median certificate proxy to
                                                                                                         Configuration                        Certified SAFE   Med. t [s]   Med. lit(Inv )   Med. tchk [s]   Med. ∆Inv
12,785 (34.0% below baseline) and cuts median checking time
                                                                                                         PDR (baseline)                              176/190       123.2            16154            3.51         0.43
to 0.55 s (55.6% below baseline), with only a small additional                                           CAPDR (random ranking)
                                                                                                         CAPDR (CP1 only: blockers)
                                                                                                                                                     171/190
                                                                                                                                                     175/190
                                                                                                                                                                   135.4
                                                                                                                                                                   125.1
                                                                                                                                                                                    17917
                                                                                                                                                                                    11314
                                                                                                                                                                                                     3.75
                                                                                                                                                                                                     2.21
                                                                                                                                                                                                                  0.50
                                                                                                                                                                                                                  0.29
runtime overhead (117.5 s median) and unchanged coverage                                                 CAPDR (CP1+CP2: +obligation order)
                                                                                                         CAPDR (CP1-CP3 full)
                                                                                                                                                     178/190
                                                                                                                                                     179/190
                                                                                                                                                                   131.4
                                                                                                                                                                   125.3
                                                                                                                                                                                    10336
                                                                                                                                                                                     9620
                                                                                                                                                                                                     2.01
                                                                                                                                                                                                     1.61
                                                                                                                                                                                                                  0.25
                                                                                                                                                                                                                  0.20
(293 solved). Overall, CAPDR trades a small amount of solving                                            CAPDR (CP1-CP3 full) + inv-min
                                                                                                         CAPDR (CP1-CP3 full) + replay
                                                                                                                                                     179/190
                                                                                                                                                     179/190
                                                                                                                                                                   127.8
                                                                                                                                                                   125.3
                                                                                                                                                                                     7990
                                                                                                                                                                                     9620
                                                                                                                                                                                                     1.31
                                                                                                                                                                                                     1.61
                                                                                                                                                                                                                  0.20
                                                                                                                                                                                                                  0.00
time for substantially smaller and cheaper-to-check certificates.
   Because the solved sets differ across configurations, the                                                3) Ablation on choice points and stability: On the develop-
medians in Table I should be read as workflow-level summaries                                            ment split, Table III attributes the certificate gains on SAFE
over each configuration’s solved instances. The paired SAFE-                                             instances to specific PDR choice points and serves both as an
instance comparison in Fig. 2a controls for this by restricting                                          ablation study and as a characterization of the policy-design
to benchmarks solved by both baseline PDR and CAPDR.                                                     space used for offline fitting. A random ranking policy is a
   2) Fair post-hoc MSIS comparison: To isolate online                                                   useful negative control: it degrades solvability (171/190 vs.
search from post-fixpoint minimization, we apply one shared                                              176/190) and inflates both lit(Inv ) and tchk , confirming that
implementation of the combined BIG+NFN method defined                                                    CAPDR’s gains are not an artifact of nondeterminism but of
by [7] to the 180 SAFE benchmarks solved by both baseline                                                informed decisions. As in Table I, the medians in Table III are
PDR and CAPDR. In the terminology of [7], the pipeline runs                                              computed over each configuration’s own certified SAFE set
NEC, FEAS, a second NEC pass, and BigMSIS. It deletes                                                    and should therefore be interpreted jointly with the coverage
clauses only and returns a subset-minimal safe inductive subset,                                         column, rather than as paired common-subset comparisons.
without claiming minimum cardinality or literal count. Because                                              Guiding CP1 (blocker selection/generalization) provides
each evaluated AIGER job has one bad output, the fixed safety                                            most of the benefit: CP1 alone reduces the median invariant
clause ¬Bad , where Bad denotes that output, is used as the                                              literal count by 30% (16,154 → 11,314) and cuts median
initial necessary set. Every other fixed-point clause is a deletion                                      checker time by 37% (3.51 s → 2.21 s) with essentially
candidate. Both inputs use the same SAT backend, canonical                                               unchanged runtime. Adding guidance at CP2-CP3 yields further
clause order, one-hour postprocessing limit, and independent                                             improvements, reaching a 40% reduction in lit(Inv ) (16,154
checker. The original solving times are unchanged and are not                                            → 9,620) and a 54% reduction in checker time (3.51 s →
repeated; the reported tmsis is the additional postprocessing                                            1.61 s) for the full policy, while also solving three additional
time only. PDR+ [7] completes on 178 of the 180 inputs and                                               SAFE instances (179/190). Stability improves as well: the
CAPDR + [7] on all 180. To keep the quality comparison                                                   median cross-seed Jaccard distance drops from 0.43 to 0.20
                                                                                                                                                                                                                                                                                                                 12




                                                                                                                                                                     1
 Invariant literal ratio lit(InvCAPDR )/lit(InvPDR )


                                                                                                                                                                                                                                                                              1
                                                        100.6

                                                                                                                                                                    0.8                                                                                                      0.8
                                                        100.4




                                                                                                                                                                                                                                                          Instability ∆Inv
                                                                                                                                                    Empirical CDF
                                                        100.2                                                                                                       0.6
                                                                                                                                                                                                                                                                             0.6
                                                         100
                                                                                                                                                                    0.4
                                                       10−0.2                                                                                                                                                                                                                0.4

                                                       10−0.4                                                                                                       0.2                                                                 PDR
                                                                                                                                                                                                                                       CAPDR                                 0.2
                                                       10−0.6                                                                                                                                                                       CAPDR+inv-min
                                                                                                                                                                     0
                                                                10−0.6 10−0.5 10−0.4 10−0.3 10−0.2 10−0.1 100 100.1 100.2 100.3 100.4 100.5 100.6                    10−2   10−1                      100                     101                   102                       0
                                                                                              Runtime ratio tCAPDR /tPDR                                                           Checker time tchk on SAFE certificates [s]                                                      PDR   CAPDR   CAPDR+replay

                                                       (a) Per-instance tradeoff on SAFE benchmarks                                                 (b) Checker time distribution on SAFE certificates                                                          (c) Cross-seed instability and replay fidelity

Fig. 2: SAFE-certificate quality and reproducibility. Panels (a) and (b) use the held-out HWMCC’24 evaluation corpus. (a) Common 180-instance SAFE
subset, with runtime and invariant-size ratios relative to baseline; parity is 1. (b) Empirical CDF of SAFE checker time on the same common subset, where left
is faster. (c) On Bdev , cross-seed instability for PDR and CAPDR, and replay-fidelity distance for CAPDR +REPLAY.



(roughly 80% clause-set overlap after canonicalization). Replay                                                                                                                                  different seeds often lead to meaningfully different resulting
addresses a different question: deterministic re-execution from                                                                                                                                  invariants. In contrast, CAPDR shifts the distribution downward
the recorded logs yields med ∆replayInv = 0 on the same SAFE                                                                                                                                     and tightens it, showing that certificate-aware guidance tends
runs, confirming exact artifact-grade reproducibility.                                                                                                                                           to produce more consistent invariants across runs. Finally,
   The CP1-only row is not a dedicated shortest-first control,                                                                                                                                   enforcing replay collapses the distribution to ∆Inv = 0,
so Table III does not establish a learned-versus-shortest CP1                                                                                                                                    demonstrating that the replay log fully determinizes the run
result. The additional gains from CP2 and CP3 show only that                                                                                                                                     and enables artifact-grade reproducibility.
a rule defined solely by CP1 clause length is not a complete
explanation of the full policy. A direct deterministic shortest-                                                                                                                                                                                     VII. C ONCLUSION
first ablation is not part of the present evaluation. The equality-
controlled comparison with the dedicated postprocessor of [7]                                                                                                                                       CAPDR separates offline learning from certified cross-
is reported separately in Section VI-B2.                                                                                                                                                         instance deployment and reuses one frozen ranker across
   4) External coverage sanity check: On the 200-instance                                                                                                                                        held-out target instances without adding it to the trusted
test list published with LeGend [20], a separate author run                                                                                                                                      computing base. At deployment, the frozen model only or-
of CAPDR solved 189 instances under a 7200 s per-instance                                                                                                                                        ders verifier-generated proposals, while PDR guards control
timeout. LeGend reports 181 solved with IC3ref and 182                                                                                                                                           clause insertion and pushing and the independent checker
with ABC [20]. This is a coverage-only sanity check, not                                                                                                                                         controls final acceptance. On held-out HWMCC’24 bit-level
a controlled tool comparison. Hosts, preprocessing, solver                                                                                                                                       safety benchmarks, this guidance reduces certificate bulk and
integration, lemma generation, certificate emission, and checker                                                                                                                                 checker time with modest solving overhead. Its advantage
interfaces differ, and coverage is not the objective optimized                                                                                                                                   also remains after applying the same MSIS postprocessor to
here. The result therefore supports only the limited conclusion                                                                                                                                  paired baseline and CAPDR SAFE outputs, while replay logs
that the certificate-oriented evaluation is not accompanied by                                                                                                                                   make runs artifact-reproducible. Transfer remains an empirical
an obvious loss of broad solved coverage on that list.                                                                                                                                           performance question, whereas soundness remains checker-
   5) Per-instance tradeoffs, checker cost, and stability: Fig. 2a                                                                                                                               relative and policy-independent.
provides a per-instance view on SAFE benchmarks solved by                                                                                                                                           Future work includes exporting witness circuits for a
both baseline PDR and CAPDR. Of the 180 paired SAFE                                                                                                                                              common Certifaiger workflow and studying certificate-aware
instances, 177 lie below y = 1 and three lie above it. The                                                                                                                                       choices for SMT-based infinite-state systems [12], liveness
concentration below parity while runtime remains near x = 1                                                                                                                                      certificates [13], and theorem-prover-based certification [36].
shows that the reductions are broad rather than driven by a few
                                                                                                                                                                                                Acknowledgements. The research of Arman Ferdowsi was
outliers. The three points above y = 1 are genuine checker-
                                                                                                                                                                                                funded in whole or in part by the Austrian Science Fund
accepted cases, not checker errors. A locally valid clause order
                                                                                                                                                                                                (FWF) 10.55776/ESP1705325. The research of Laura Kovács
can steer PDR toward a different proof trajectory and a larger
                                                                                                                                                                                                was funded in whole or in part by the ERC Consolida-
final fixed point. With only three such cases, we cannot identify
                                                                                                                                                                                                tor Grant ARTIST 101002685, the WWTF Grant ForSmart
a reliable benchmark pattern. This non-monotonicity motivates
                                                                                                                                                                                                10.47379/ICT22007, and the SBA Research COMET Center
the tunable objective in Eq. (16) rather than a claim that every
                                                                                                                                                                                                SBA-K1 NGC managed by the FFG.
local certificate-aware choice improves every instance.
   Fig. 2b shows the corresponding leftward shift in independent                                                                                                                                 Artifact availability. The source code is publicly available at
checker time, with CAPDR +INV- MIN improving further.                                                                                                                                            https://github.com/armanferdowsi/CAPDR.
   Fig. 2c quantifies how sensitive SAFE certificates are
to nondeterminism by plotting the distribution (over SAFE                                                                                                                                                                                                   R EFERENCES
benchmarks) of the invariant-instability metric ∆Inv across
10 seeds, where ∆Inv is the Jaccard distance between canoni-                                                                                                                                       [1] A. R. Bradley, “Sat-based model checking without unrolling,” in
                                                                                                                                                                                                       Verification, Model Checking, and Abstract Interpretation (VMCAI 2011),
calized clause sets (Section IV-F). The baseline PDR exhibits                                                                                                                                          ser. Lecture Notes in Computer Science, vol. 6538. Springer, 2011, pp.
substantial run-to-run variability (wide spread), indicating that                                                                                                                                      70–87.
                                                                                                                                                                   13



 [2] N. Froleyks, E. Yu, M. Preiner, A. Biere, and K. Heljanko, “Introducing         [20] M. Miao, G. Hu, W. Zhang, and H. Zhang, “Legend: A data-driven
     certificates to the hardware model checking competition,” in Computer                framework for lemma generation in hardware model checking,” arXiv
     Aided Verification (CAV 2025), Proceedings, Part I, ser. Lecture Notes               preprint arXiv:2602.24010, 2026.
     in Computer Science, vol. 15931. Springer Nature, 2025, pp. 281–295.            [21] X. Zhou, G. Hu, H. Zhang, and W. Zhang, “A-IC3: Learning-guided
 [3] A. Biere, N. Froleyks, and M. Preiner, “Hardware model checking                      adaptive inductive generalization for hardware model checking,” arXiv
     competition 2025,” in 2025 Formal Methods in Computer-Aided Design                   preprint arXiv:2604.21688, 2026.
     (FMCAD). IEEE, 2025, pp. 1–1.                                                   [22] M. Miao, G. Hu, Z. Yang, and H. Zhang, “Ic3-evolve: Proof-/witness-
 [4] D. Beyer and J. Strejček, “Improvements in software verification and                gated offline llm-driven heuristic evolution for ic3 hardware model
     witness validation: SV-COMP 2025,” in Tools and Algorithms for the                   checking,” arXiv preprint arXiv:2604.03232, 2026.
     Construction and Analysis of Systems (TACAS 2025), ser. Lecture Notes           [23] N. Wetzler, M. J. H. Heule, and J. Warren A. Hunt, “Drat-trim: Efficient
     in Computer Science, vol. 15698. Springer Nature, 2025, pp. 151–186.                 checking and trimming using expressive clausal proofs,” in Theory and
 [5] G. Hu, J. Tang, C. Yu, W. Zhang, and H. Zhang, “Deepic3: Guiding ic3                 Applications of Satisfiability Testing (SAT 2014), ser. Lecture Notes in
     algorithms by graph neural network clause prediction,” in 29th Asia and              Computer Science, vol. 8561. Springer, 2014, pp. 422–429.
     South Pacific Design Automation Conference (ASP-DAC 2024). IEEE,                [24] L. Cruz-Filipe, M. J. H. Heule, J. Warren A. Hunt, M. Kaufmann, and
     2024, pp. 262–268.                                                                   P. Schneider-Kamp, “Efficient certified rat verification,” in Automated
 [6] Z. Lu, P.-C. Chien, N.-Z. Lee, A. Gurfinkel, and V. Ganesh, “Btor2-                  Deduction (CADE 26), ser. Lecture Notes in Computer Science, vol.
     Select: Machine learning based algorithm selection for hardware model                10395. Springer, 2017, pp. 220–236.
     checking,” in Computer Aided Verification (CAV 2025), Proceedings,              [25] F. Pollitt, M. Fleury, and A. Biere, “Faster lrat checking than solving with
     Part I, ser. Lecture Notes in Computer Science, vol. 15931. Springer                 cadical,” in 26th International Conference on Theory and Applications of
     Nature, 2025, pp. 296–311.                                                           Satisfiability Testing (SAT 2023), ser. Leibniz International Proceedings in
 [7] A. Ivrii, A. Gurfinkel, and A. Belov, “Small inductive safe invariants,”             Informatics (LIPIcs). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
     in 2014 Formal Methods in Computer-Aided Design (FMCAD). IEEE,                       2023.
     2014, pp. 115–122.                                                              [26] P. Lammich, “Fast and verified unsat certificate checking,” in Automated
 [8] E. Yu, A. Biere, and K. Heljanko, “Progress in certifying hardware                   Reasoning (IJCAR 2024), Proceedings, Part I, ser. Lecture Notes in
     model checking results,” in International Conference on Computer Aided               Computer Science, vol. 14739. Springer Nature, 2024, pp. 439–457.
     Verification. Springer, 2021, pp. 363–386.                                      [27] C. R. Codel, J. Avigad, and M. J. Heule, “Verified substitution redundancy
 [9] E. Yu, N. Froleyks, A. Biere, and K. Heljanko, “Stratified certification             checking,” in 2024 Formal Methods in Computer-Aided Design (FMCAD).
     for k-induction,” in 2022 Formal Methods in Computer-Aided Design                    IEEE, 2024, pp. 186–196.
     (FMCAD). IEEE, 2022, pp. 59–64.                                                 [28] H.-J. Schurr, M. Fleury, H. Barbosa, and P. Fontaine, “Alethe: Towards
[10] N. Froleyks, E. Yu, A. Biere, and K. Heljanko, “Certifying phase                     a generic smt proof format,” arXiv preprint arXiv:2107.02354, 2021.
     abstraction,” in Automated Reasoning (IJCAR 2024), Proceedings, Part            [29] B. Andreotti, H. Lachnitt, and H. Barbosa, “Carcara: An efficient proof
     I, ser. Lecture Notes in Computer Science, vol. 14739. Springer Nature,              checker and elaborator for smt proofs in the alethe format,” in Tools and
     2024, pp. 284–303.                                                                   Algorithms for the Construction and Analysis of Systems (TACAS 2023),
[11] E. Yu, N. Froleyks, A. Biere, and K. Heljanko, “Towards compositional                Part I, ser. Lecture Notes in Computer Science, vol. 13993. Springer
     hardware model checking certification,” in Proceedings of the 23rd                   Nature, 2023, pp. 367–386.
     Conference on Formal Methods in Computer-Aided Design (FMCAD                    [30] H. Lachnitt, M. Fleury, H. Barbosa, J. Jakpor, B. Andreotti, A. Reynolds,
     2023). TU Wien Academic Press, 2023, pp. 44–54.                                      H.-J. Schurr, C. Barrett, and C. Tinelli, “Improving the smt proof
[12] A. Mebsout and C. Tinelli, “Proof certificates for smt-based model                   reconstruction pipeline in isabelle/hol,” in 16th International Conference
     checkers for infinite-state systems,” in 2016 Formal Methods in Computer-            on Interactive Theorem Proving (ITP 2025), ser. Leibniz International
     Aided Design (FMCAD). IEEE, 2016, pp. 117–124.                                       Proceedings in Informatics (LIPIcs), vol. 352. Schloss Dagstuhl –
[13] A. Griggio, M. Roveri, and S. Tonetta, “Certifying proofs for sat-based              Leibniz-Zentrum für Informatik, 2025, pp. 26:1–26:22.
     model checking,” Formal Methods in System Design, vol. 57, no. 2, pp.           [31] A. Mohamed, T. Mascarenhas, H. Khan, H. Barbosa, A. Reynolds,
     178–210, 2021.                                                                       Y. Qian, C. Tinelli, and C. Barrett, “Lean-smt: An smt tactic for
[14] N. Froleyks and A. Biere, “Single clause assumption without activation               discharging proof goals in lean,” in International Conference on Computer
     literals to speed-up ic3,” in Proceedings of the 21st Conference on                  Aided Verification. Springer, 2025, pp. 197–212.
     Formal Methods in Computer-Aided Design (FMCAD 2021). TU Wien                   [32] S. Hitarth, C. R. Codel, H. Lachnitt, and B. Dutertre, “Extending drat
     Academic Press, 2021, pp. 72–76.                                                     to smt,” in Proceedings of the 24th Conference on Formal Methods in
[15] Y. Xia, A. Becchi, A. Cimatti, A. Griggio, J. Li, and G. Pu, “Searching              Computer-Aided Design (FMCAD 2024). TU Wien Academic Press,
     for i-good lemmas to accelerate safety model checking,” in Computer                  2024, pp. 18–28.
     Aided Verification (CAV 2023), Proceedings, Part II, ser. Lecture Notes         [33] A. R. Bradley, “Understanding ic3,” in International Conference on
     in Computer Science, vol. 13965. Springer Nature, 2023, pp. 288–308.                 Theory and Applications of Satisfiability Testing. Springer, 2012, pp.
[16] A. Luka and Y. Vizel, “Property directed reachability with extended                  1–14.
     resolution,” in Computer Aided Verification (CAV 2025), Proceedings,            [34] N. Eén, A. Mishchenko, and R. Brayton, “Efficient implementation of
     Part I, ser. Lecture Notes in Computer Science, vol. 15931. Springer                 property directed reachability,” in 2011 Formal Methods in Computer-
     Nature, 2025, pp. 258–280.                                                           Aided Design (FMCAD). IEEE, 2011, pp. 125–134.
[17] Y. Su, Q. Yang, Y. Ci, Y. Li, T. Bu, and Z. Huang, “Deeply optimizing           [35] A. Biere, N. Froleyks, and M. Preiner, “Hardware Model Checking Com-
     the SAT solver for the IC3 algorithm,” in Computer Aided Verification                petition 2020,” https://fmv.jku.at/hwmcc20/, 2020, benchmark archive
     (CAV 2025), Proceedings, Part I, ser. Lecture Notes in Computer Science,             and results.
     vol. 15931. Springer Nature, 2025, pp. 237–257.                                 [36] G. Sindoni, P. Pasini, G. Cabodi, P. E. Camurati, A. Griggio, M. Palena,
[18] R. Dureja, A. Gurfinkel, A. Ivrii, and Y. Vizel, “Ic3 with internal signals,”        M. Roveri, and S. Tonetta, “A theorem prover based approach for SAT-
     in 2021 Formal Methods in Computer Aided Design (FMCAD). IEEE,                       based model checking certification,” in Automated Deduction – CADE 30,
     2021, pp. 63–71.                                                                     ser. Lecture Notes in Computer Science, vol. 15943. Springer Nature,
[19] Y. Su, Q. Yang, and Y. Ci, “Predicting lemmas in generalization of IC3,”             2025, pp. 449–467.
     in Proceedings of the 61st ACM/IEEE Design Automation Conference
     (DAC 2024). ACM, 2024, pp. 208:1–208:6.
                                                                                                                                          14



                   A PPENDIX A                                         acceptance of an extended certificate implies safety of the
 F RAME PRESERVATION BY GUARDED CLAUSE INSERTION                       original system. We formalize this projection argument in
   Suppose C satisfies Eqs. (12) to (14) for an obligation (i, d),     Proposition 2.
and let Fbj = Fj ∧ C for 1 ≤ j ≤ i, while Fbj = Fj otherwise.             Projection mode emits an X-only candidate invariant and
The boundary F0 ⇒ F1 is preserved by Init ⇒ C. Boundaries              validates it with the base SAFE checker. Extension mode uses
1 ≤ j < i are strengthened on both sides, and later boundaries         the auxiliary-aware checker above.
are either strengthened only in the antecedent or unchanged;
hence monotonicity is preserved.                                                           A PPENDIX C
   For any closed consecution index j < k, if j + 1 ≤ i, the             D EFERRED F ORMALIZATION OF THE L OCAL O BJECTIVE
consequent frame is strengthened by C. Old consecution gives
                                                                          Fix a ranking event e = (r, ϕ, A) and a continuation control
Fj+1 (X ′ ), and monotonicity gives Fj ⇒ Fi−1 , so Eq. (14)
                                                                       law µ for the remainder of the run. The law µ includes the
gives C(X ′ ). If j + 1 > i, the consequent is unchanged
                                                                       frozen scorer, fixed tie-breaking, deterministic fallback behavior,
and the antecedent is only strengthened or unchanged, so old
                                                                       and the fairness rule. For CP1 and CP3, selecting a first means
consecution suffices. Finally, Fj ⇒ Prop is preserved because
                                                                       trying a first while leaving its SAT guard active. If the guard
strengthening frames cannot introduce new states.
                                                                       fails, execution continues according to µ. For CP2, selecting a
   Push preservation: If C           ∈     Fi and Fi (X) ∧
                                                                       first means servicing that obligation next.
Trans(X, U, X ′ ) ⇒ C(X ′ ), then adding C to Fi+1
                                                                          The global objective in Eq. (16) induces the ideal local
preserves monotonicity because Fi ⇒ C, and it preserves
                                                                       action value
consecution at level i by the push guard. Other closed
consecution obligations are unchanged or only strengthened in
                                                                                           
                                                                          QJ (e, a) ≜ −E J |e, a is selected first,
the antecedent.                                                                                                     
                                                                                                µ is used thereafter ,      a ∈ A. (22)

                     A PPENDIX B                                        where the expectation is over the remaining solver and system
         AUXILIARY-VARIABLE E XTENSION M ODE                            nondeterminism. Larger QJ (e, a) means lower expected final
   Some strengthening techniques (e.g., extended-resolution- cost.
style reasoning) introduce auxiliary Boolean state variables Y .            Development does not need to compute this expectation
To keep certificates unambiguous while preserving soundness             exactly.  For selected alternatives, it obtains a sample or estimate
for the original transition system over X, we support two               Jbe (a) from a measured continuation or a checkpointed rollout
conservative modes:                                                     beginning at the same proof state. Only alternatives from
                                                                        the same event and continuation protocol are compared. The
   • Projection mode: emit an X-only candidate invariant
                                                                        pairwise data set is
      Inv X (X) obtained from the internal auxiliary-rich repre-
      sentation by some elimination procedure; correctness is
                                                                                            n                                  o
                                                                                     D = (e, a+ , a− ) Jbe (a+ ) < Jbe (a− ) .
      not assumed from that elimination step itself, but solely
      from subsequent acceptance by the base SAFE checker. A continuation that times out, exits because of a resource
   • Extension mode: emit an invariant Inv (X, Y ) together             limit, or produces a checker-rejected artifact is assigned Jfail =
      with an auxiliary-state relation Def (X, Y ).                     ⟨actual value⟩, chosen above the largest completed checker-
   In extension mode, let Def ′ (X ′ , Y ′ ) denote the primed copy accepted development cost. This convention is used only for
of Def (X, Y ), and define                                              training labels. Reported solved-set medians in Section VI
         ext                                                            contain only checker-accepted runs.
    Init ≜ Init(X) ∧ Def (X, Y ),
                                                                            For each (e, a+ , a− ) ∈ D, let ∆xe = xe (a+ ) − xe (a− ).
 Trans ext ≜ Trans(X, U, X ′ ) ∧ Def (X, Y ) ∧ Def ′ (X ′ , Y ′ ).      For the linear scorer gθ (x) = θ⊤ x, the evaluated prototype
                                                                        minimizes
We require Def to be a conservative extension of the original
dynamics under projection to X:                                                           X                                 λreg
                                                                                                   log 1 + exp −θ⊤ ∆xe +             ∥θ∥22 .
                                                                                                                
                                                                           L(θ) =
                                                                                                                                  2
                                ∀x. Init(x) ⇒ ∃y. Def (x, y),                        (e,a+ ,a− )∈D
                                                                 (20)                                                                    (23)
                                                                        The   loss is small   when  the lower-cost alternative has the larger
 ∀x, u, x′ , y. Trans(x, u, x′ ) ∧ Def (x, y) ⇒ ∃y ′ . Def (x′ , y ′ ).
                                                                        score. Thus gθ is trained as an order-consistent surrogate for
                                                                 (21)
                                                                        QJ , not as a proof oracle.
   In extension mode, the emitted SAFE certificate is the                   During deployment, CAPDR computes only gθ (xe (a)) and
pair (Def , Inv (X, Y )). The independent checker must val- sorts the finite set A. It does not compute QJ , Jbe , or J online.
idate both components: (i) it checks Inv on the extended For CP1 and CP3, candidates are scanned in deterministic
system (Init ext , Trans ext , Prop), and (ii) it validates that Def score order until a guard-valid action is committed or the list is
witnesses a conservative auxiliary-variable extension of the exhausted. For CP2, the highest-ranked obligation is selected
original system by a dedicated procedure whose correctness subject to fairness. CP1 cannot deadlock after the initial-state
guarantees Eqs. (4) and (5). Only after both checks succeed check because ¬d ∈ C(d, i) satisfies Eqs. (13) and (14) under
may the checker accept the certificate. Under these conditions, the hypotheses of Proposition 1.
                                                                       15



                     A PPENDIX D
 E XACT I NSTABILITY AND R EPLAY-F IDELITY F ORMULAS
   For SAFE certificates, let canon(Inv ) be the clause set
obtained by sorting literals within each clause, deleting repeated
literals within a clause, and deleting duplicate clauses.
   For seeds s, s′ , let As = canon(Inv s ) and As′ =
canon(Inv s′ ). The cross-seed instability is
                      
                      0,
                                         As ∪ As′ = ∅,
                ′
     ∆seed
       Inv (s, s  ) ≜      |As ∩ As′ |                        (24)
                      1 −
                                      , otherwise.
                           |As ∪ As′ |
This is the Jaccard distance on canonicalized clause sets and
measures run-to-run certificate instability across seeds.
   For a run executed with seed s, let Inv replay
                                           s      be the certificate
produced by deterministic re-execution from that run’s replay
log, and set Rs = canon(Inv replay
                             s     ). The replay-fidelity distance
is
                   
                   0,
                                       As ∪ Rs = ∅,
        replay
      ∆Inv (s) ≜         |As ∩ Rs |                             (25)
                   1 −
                                    , otherwise.
                         |As ∪ Rs |
Exact replay corresponds to ∆replay
                                  Inv (s) = 0. We use ∆Inv
                                                          seed
                              replay
for stability evaluation and ∆Inv for replay validation. They
measure different phenomena and are reported separately.
