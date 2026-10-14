                                         IC3-Evolve: Proof-/Witness-Gated Offline LLM-Driven Heuristic Evolution for
                                                              IC3 Hardware Model Checking
                                                         Mingkai Miao1∗ , Guangyu Hu2∗ , Ziyi Yang1 , Hongce Zhang1,2†
                                            1
                                              Hong Kong University of Science and Technology (Guangzhou), Guangzhou, Guangdong, China
                                                    2
                                                      Hong Kong University of Science and Technology, Clear Water Bay, Hong Kong
                                          {mmiao815, zyang957}@connect.hkust-gz.edu.cn, ghuae@connect.ust.hk, hongcezh@hkust-gz.edu.cn

                                                                         Abstract                            For hardware safety model checking, IC3 [Bradley, 2011]
arXiv:2604.03232v1 [cs.AI] 18 Jan 2026




                                                                                                          (also known as property-directed reachability, PDR [Eén et
                                                 IC3, also known as property-directed reachability        al., 2011]) is a widely-used state-of-the-art algorithm. Im-
                                                 (PDR), is a commonly-used algorithm for hardware         portantly, IC3 is proof-producing: it either returns UNSAFE
                                                 safety model checking. It checks if a state transition   with a replayable counterexample trace, or returns SAFE with
                                                 system complies with a given safety property. IC3        a checkable inductive invariant that certifies the property.
                                                 either returns UNSAFE (indicating property viola-           While IC3 provides a strong algorithmic foundation, its
                                                 tion) with a counterexample trace, or SAFE with a        practical performance depends critically on numerous heuris-
                                                 checkable inductive invariant as the proof to safety.    tics and engineering decisions—including generalization,
                                                 In practice, the performance of IC3 is dominated by      clause propagation, and interactions with the underlying
                                                 a large web of interacting heuristics and implemen-      Boolean satisfiability (SAT) engines. As a result, improving
                                                 tation choices, making manual tuning costly, brit-       an IC3 checker is often more about heuristic engineering than
                                                 tle, and hard to reproduce.                              changing the core algorithmic framework. Unfortunately,
                                                 This paper presents IC3-Evolve, an automated             this engineering loop is costly and brittle [Le et al., 2021;
                                                 offline code-evolution framework that utilizes an        Hu et al., 2024]: even small heuristic changes typically re-
                                                 LLM to propose small, slot-restricted and auditable      quire re-running large benchmark suites to reach stable con-
                                                 patches to an IC3 implementation. Crucially, ev-         clusions; gains on one family of instances can easily induce
                                                 ery candidate patch is admitted only through proof-      regressions elsewhere. Manual tuning therefore demands
                                                 /witness-gated validation: SAFE runs must emit a         substantial domain expertise [Le et al., 2021; Hu et al., 2024],
                                                 certificate that is independently checked, and UN-       making it difficult to reliably discover robust heuristic com-
                                                 SAFE runs must emit a replayable counterexam-            binations.
                                                 ple trace, preventing unsound edits from being de-          Recent advances in machine learning have also begun to
                                                 ployed. Since the LLM is used only offline, the          influence Electronic Design Automation (EDA) and formal
                                                 deployed artifact is a standalone evolved checker        verification. In the context of IC3, prior work such as Neu-
                                                 with zero ML/LLM inference overhead and no run-          roPDR [Hu et al., 2023] and DeepIC3 [Hu et al., 2024]
                                                 time model dependency. We evolve on the public           explores learning-augmented solvers: a trained model pre-
                                                 hardware model checking competition (HWMCC)              dicts candidate clauses to guide IC3’s proof search, showing
                                                 benchmark and evaluate the generalizability on un-       promising results on selected benchmarks.
                                                 seen public and industrial model checking bench-            However, learning-augmented IC3 solvers often face prac-
                                                 marks, showing that IC3-Evolve can reliably              tical barriers to industrial deployment. Learned components
                                                 discover practical heuristic improvements under          introduce training and inference costs, and their benefits can
                                                 strict correctness gates.                                degrade on large-scale or heterogeneous workloads where ro-
                                                                                                          bustness and throughput are paramount. Moreover, placing
                                         1       Introduction                                             ML inference in the runtime loop adds latency and increases
                                         Formal property checking is a cornerstone of modern hard-        performance variance, prohibiting predictable behavior and
                                         ware verification. As integrated circuits grow in complexity,    integration into production flows. In recent HWMCC edi-
                                         their state spaces quickly exceed what simulation can effec-     tions, the strongest-performing entries remain predominantly
                                         tively explore, leaving deep corner-case behaviors untested,     conventional model checkers rather than learning-augmented
                                         causing severe economic loss, thus motivating formal analy-      solvers [hwm, 2024; hwm, 2025a].
                                         sis in hardware verification, exemplified by hardware safety        Another line of work uses LLMs in the verification loop
                                         model checking.                                                  to provide per-instance auxiliary hints (e.g., candidate invari-
                                                                                                          ants or guidance) to an existing checker [Janßen et al., 2024;
                                             ∗
                                                 Equal contribution.                                      Pirzada et al., 2024; Wu et al., 2024]. Such hints must be in-
                                             †
                                                 Corresponding author.                                    dependently validated before use; moreover, integrating on-
                                                                           flow that explores local refinements and cross-module
                                                                           changes, including the Compass & Jump strategy to
                                                                           guide search across the solver’s modification space.
                                                                         • We enforce correctness via proof-/witness-gated valida-
                                                                           tion: a proposed edit is accepted only if it passes hard
                                                                           checks with validation, preventing unsound changes
                                                                           from being deployed.
                                                                         • We evaluate IC3-Evolve by evolving on the public
                                                                           HWMCC suite and assessing generalization on unseen
                                                                           public and industrial verification benchmarks from pro-
                                                                           duction flows, demonstrating that IC3-Evolve can
                                                                           discover practical heuristic improvements under strict
                                                                           correctness gates.

                                                                     2     Background
                                                                     2.1    IC3 in a Nutshell
                                                                     IC3 is a proof-producing safety model checking algorithm: it
                                                                     tries to prove that no reachable execution can enter a “bad”
                                                                     state. Operationally, it alternates between (i) searching for
                                                                     counterexamples to the current proof attempt and (ii) learning
Figure 1: Comparison of learning-augmented IC3, LLM-in-the-loop      clauses that rule them out. It either returns UNSAFE with a re-
verification, and our approach. IC3-Evolve evolves IC3 code of-
fline and promotes edits only via proof-/witness-gated validation,
                                                                     playable counterexample trace, or returns SAFE with a check-
yielding a standalone checker with no runtime model dependency.      able inductive invariant that certifies the property. Through-
                                                                     out the paper, we use proof to denote the SAFE certificate (in-
line LLM calls at verification time raises practical concerns        ductive invariant), and witness to denote the UNSAFE coun-
about latency, reproducibility, and deployment.                      terexample trace.
   These trends suggest both an opportunity and a bottle-               We consider a finite-state transition system with state vari-
neck: today’s strongest IC3 checkers remain largely heuristic-       ables x, input variables y, initial-state predicate I(x), transi-
engineered, yet manual tuning is labor-intensive and frag-           tion relation T (x, y, x′ ), and a safety property P (x), where
ile. Meanwhile, recent LLM-based “code evolution” systems            x′ denotes the next-state copy of x. IC3 [Bradley, 2011] de-
show that iterative propose–evaluate–refine loops can au-            cides whether all reachable states satisfy P .
tonomously improve nontrivial algorithmic code under eval-
                                                                        IC3 maintains a sequence of frames F0 , . . . , Fk , where
uation feedback. For example, AlphaEvolve [Novikov et al.,
                                                                     F0 = I and each Fi is represented as a formula over x.
2025] demonstrates evaluator-driven evolutionary search for
                                                                     Intuitively, Fi over-approximates the set of states reachable
algorithmic optimization, while AutoSAT [Sun et al., 2024]
                                                                     within i steps. The frames are monotone (Fi ⇒ Fi+1 ),
and SATLUTION [Yu et al., 2025] apply related ideas to
                                                                     and for i ≥ 1 they are constrained to satisfy the property
evolve SAT-solver heuristics under rigorous validation.
                                                                     (Fi ⇒ P ). Additionally, the sequence satisfies the step condi-
   Motivated by this trend of research, we present
                                                                     tion: for all 0 ≤ i < k, Fi (x)∧T (x, y, x′ ) ⇒ Fi+1 (x′ ). IC3
IC3-Evolve, an offline LLM-driven framework that treats
                                                                     strengthens this sequence by learning lemmas that exclude
IC3 heuristic engineering as controlled code evolution. As
                                                                     unreachable states while preserving all reachable behaviors.
shown in Figure 1, rather than placing ML/LLM inference
                                                                        Algorithm 1 sketches the main loop of IC3. We use a cube
in the verification-time loop, IC3-Evolve uses LLMs to
                                                                     to denote a conjunction of literals representing a (partial)
propose constrained, auditable code edits to an IC3 checker
                                                                     state assignment, and a clause to denote a disjunction of liter-
and promotes edits only after proof-/witness-gated validation.
                                                                     als used as a lemma. At a high level, IC3 alternates between
The resulted artifact is a standalone evolved checker: the
                                                                     two phases: (i) blocking, which finds a counterexample-to-
LLM is used only offline, so deployment incurs no ML/LLM
                                                                     induction (CTI) cube s by checking Fk ∧T ∧¬P ′ (an Fk -state
inference overhead and no runtime model dependency. Build-
                                                                     with a bad successor) for satisfiability and attempts to block
ing on this foundation, we introduce a workflow that explores
                                                                     s by learning a new lemma; and (ii) propagation, which tries
both local and cross-module heuristic choices and evaluate
                                                                     to push learned lemmas forward to higher frames. If blocking
the evolved engine on public and industrial benchmarks.
                                                                     a proof obligation reaches level 0, IC3 can construct a coun-
   We make the following contributions:
                                                                     terexample trace and returns UNSAFE. If two adjacent frames
    • We introduce IC3-Evolve, an offline LLM-driven                 become identical (Fi = Fi+1 ), that common frame is a 1-step
      framework for evolving IC3 heuristics through slot-            inductive invariant implying P , and IC3 returns SAFE.
      restricted, auditable code edits, compiling validated im-
      provements directly into the checker (with no inference-       2.2    Key Subroutines and Heuristic Touchpoints
      time overhead at deployment).                                  Key point. Most implementation choices in IC3 control
    • We design and implement a heuristic-evolution work-            search order and resource allocation (e.g., which obligation
 Algorithm 1: IC3 Algorithm Overview                               Algorithm 2: IC3 Key Subroutines
     Input : ⟨I(x), T (x, y, x′ ), P (x)⟩                              // s′ and c′ denote the primed versions
     Output: SAFE or UNSAFE                                               obtained by substituting x 7→ x′
     // x′ denotes the next-state copy of x;
                                                                   1 Function B L O C K P R O O F O B L I G A T I O N S (Q):
         P ′ abbreviates P (x′ )                                   2    while Q ̸= ∅ do
 1 F0 ← I; F1 ← P ; k ← 1; Q ← ∅;                                  3        (s, i) ← P OP(Q);
   // Q stores proof obligations (s, i)                            4        if Fi ∧ s is UNSAT then continue;
                                          ′                                 if i = 0 then
 2 if I ∧ ¬P is SAT or I ∧ T ∧ ¬P is SAT then                      5
 3      return UNSAFE                                              6             return false
 4 end                                                             7        end
 5 while true do                                                   8        if Fi−1 ∧ T ∧ s′ is SAT then
 6      while Fk ∧ T ∧ ¬P ′ is SAT with witness cube s do          9             p ← P R E D G E N (GetWitness(), i − 1, s);
 7           if not B L O C K O N E (s, k) then                   10             insert (s, i) into Q;
 8                 return UNSAFE                                  11             insert (p, i − 1) into Q;
 9           end                                                  12        end
10      end                                                       13        else
11      P U S H C L A U S E S (k);                                14             c ← I N D G E N (s, i);
12      if ∃i < k : Fi = Fi+1 then                                15             for j = 1 → i do
13           return SAFE                                          16                   Fj ← F j ∧ c
14      end                                                       17             end
15      k ← k + 1; Fk ← P ;                                       18        end
16 end                                                            19    end
17 Function B L O C K O N E (s, k):                               20    return true;
18    insert (s, k) into Q;                                       21 Function P R E D G E N (p, j, s):
      // internally calls P R E D G E N and                             // Drop literals from predecessor
           I N D G E N while discharging Q                                  cube p while preserving
19    return B L O C K P R O O F O B L I G A T I O N S (Q);                 reachability into s
                                                                  22    return M INIMIZE P RED(Fj , T, p, s);
                                                                  23 Function I N D G E N (s, i):
                                                                        // Return c ⊆ ¬s such that I ⇒ c and
to tackle next, how aggressively to generalize, and how much
                                                                            Fi−1 ∧ c ∧ T ⇒ c′
SAT effort to spend). They do not affect soundness as long as
                                                                  24    return R EL I NDUCTIVE M INIMIZE(I, Fi−1 , T, ¬s);
every learned lemma is validated by the corresponding SAT
checks and SAFE is returned only at a validated fixpoint; un-     25 Function P U S H C L A U S E S (k):
der resource limits they mainly affect practical completeness     26    for i = 1 → k − 1 do
via timeouts. This makes these choices prime targets for sys-     27         foreach c ∈ Fi \ Fi+1 do
                                                                  28             if Fi ∧ T ∧ ¬c′ is UNSAT then
tematic heuristic engineering (and for our offline code evolu-
                                                                                   Fi+1 ← Fi+1 ∧ c ;
tion later).
                                                                  29         end
   Algorithm 2 expands the key subroutines and makes ex-          30    end
plicit where heuristics dominate performance in practice. We
use the cube/clause terminology as defined above. Most of
IC3’s runtime is spent answering incremental SAT queries
of two types: (1) predecessor-search queries (for recursive       Predecessor generalization (P RED G EN). When a PO
blocking), and (2) relative-inductiveness queries (for gener-     (s, i) cannot be blocked directly, IC3 queries Fi−1 ∧ T ∧ s′ to
alization and pushing).                                           obtain a predecessor cube p and enqueues (p, i − 1). P RED -
                                                                  G EN attempts to generalize p (e.g., by dropping literals or
                                                                  using partial models) while preserving reachability into s.
Proof obligations (B LOCK P ROOF O BLIGATIONS). IC3               Stronger predecessor generalization can reduce search depth
maintains a worklist Q of proof obligations (POs) (s, i),         and the number of POs, but it typically requires extra SAT
where s is a cube to be blocked at frame i. The policy for        work and interacts heavily with the worklist strategy.
popping and re-inserting POs (e.g., depth-first vs. best-first,
priority rules, aging) can strongly influence convergence: it     Inductive generalization (I ND G EN). Given a CTI cube s
can bias the solver toward quickly refuting shallow CTIs          at level i, I ND G EN derives a blocking clause c ⊆ ¬s such that
(bug finding) or toward accumulating stronger lemmas for          c is relatively inductive w.r.t. Fi−1 and does not exclude any
deeper proofs. Practical implementations also rely on bud-        initial state: I ⇒ c and Fi−1 ∧ c ∧ T ∧ ¬c′ is UNSAT. Most
geting/backoff to avoid repeatedly spending SAT effort on         implementations start from ¬s and attempt to drop literals
“stuck” POs. Since frames are continuously strengthened,          while keeping relative inductiveness, yielding MIC-style gen-
queued POs can become stale and are typically skipped once        eralization and its extensions. They often leverage UNSAT
they are already blocked by the current target frame (i.e.,       cores/conflict clauses to guide minimization. Optimizations
Fi ∧ s becomes UNSAT).                                            here can substantially reduce SAT calls and improve lemma
quality, but they introduce trade-offs between generalization       Slot           Scope (examples)
strength and computational overhead [Su et al., 2024].
                                                                    PO handling B LOCK P ROOF O BLIGATIONS: worklist order;
Push and propagation (P USH C LAUSES). To accelerate                            stale-PO skip; requeue/budget / PO depth; SAT/PO;
convergence, IC3 tries to push lemmas forward: if a lemma                       requeue rate
c ∈ Fi is also inductive relative to Fi , it can be added to        Ind. gen.      I ND G EN: literal dropping; UNSAT cores; CTG/MIC
Fi+1 (equivalently, if Fi ∧ T ∧ ¬c′ is UNSAT). The effec-                          budgets / core size; lemma yield; generalization
tiveness of pushing depends on clause ordering, caching, and                       SAT calls
simplification/subsumption policies, as well as on budgeting        Pred. gen.     P RED G EN: assumption order; predecessor selection;
decisions that prevent spending too much effort on low-yield                       cooldown / chain length; predecessor SAT calls;
push attempts.                                                                     depth
                                                                    Push/prop.     P USH C LAUSES: push order; caching; subsumption /
3     Methodology                                                                  push success; redundancy; frame stabilization

3.1    IC3-Evolve Framework Overview                                Cross-slot     Small multi-slot changes and synergies / overall
                                                                                   PAR2 and bucketed regressions
Figure 2 summarizes IC3-Evolve, our offline framework
for evolving IC3 implementations via iterative, auditable                        Table 1: Heuristic slots for code evolution.
code changes. Starting from a champion solver, each iteration
selects a constrained modification scope (a set of heuristic        3.3    Two-Agent Closed-Loop Evolution
slots) and asks a programmer agent to propose a small patch         To operationalize heuristic engineering as a repeatable opti-
together with a hypothesis about its expected impact and a          mization process, IC3-Evolve runs a two-agent loop or-
fallback plan in case the change proves invalid. The candidate      chestrated by a lightweight Compass&Jump search policy.
is then built and evaluated by an evaluator agent. Crucially,       The framework maintains a current champion implementa-
we separate optimization from correctness: a patch is con-          tion and applies the promotion rule (promote or revert) for
sidered only if it passes proof-gated hard checks with inde-        each proposed challenger. Validation and benchmarking are
pendent witness validation—SAFE runs must emit a check-             executed by the evaluator agent, which also produces a diag-
able inductive invariant/certificate, and UNSAFE runs must          nostic MoveSet—a ranked list of structured recommendations
emit a counterexample trace that can be replayed by simula-         m = (slot, direction, conf, risk, cost) summarizing the di-
tion. Among the validated candidates, we retain improve-            agnosis and suggested next edits. Each iteration records full
ments based on benchmark performance (e.g., PAR2 and                provenance (patch diffs, logs, metrics, and witnesses) to keep
solved counts) and use the evaluator’s diagnosis to steer sub-      the process auditable and to support post-hoc diagnosis.
sequent iterations via the Compass&Jump policy.
                                                                    Iteration protocol. Given a champion solver, one evolution
                                                                    iteration proceeds as follows:
3.2    Slot-Restricted Patch Space
                                                                        (i) Select scope. The framework uses Compass&Jump to
To make code evolution controllable and reviewer-auditable,                 choose the next modification slot(s) and assembles slot-
our IC3-Evolve exposes a number of heuristic slots that                     relevant context (knowledge pack excerpts, code snip-
align with IC3’s dominant runtime subroutines (cf. Sec-                     pets, and the previous MoveSet if available).
tion 2.2). Each iteration restricts the programmer agent to            (ii) Propose. The programmer agent produces a slot-
one (Compass) or a small set (Jump) of slots, so that pro-                  restricted patch together with a hypothesis and a fall-
posed patches are localized, interpretable, and easy to revert.             back plan.
Table 1 summarizes the slots and representative optimization
knobs. Importantly, slots constrain where we edit, not what           (iii) Validate. The evaluator agent applies the patch, builds
constitutes correctness: soundness is enforced exclusively by               the challenger, and runs hard checks including proof-
the proof-gated validation described next.                                  /witness-gated validation.
                                                                      (iv) Test. The evaluator agent evaluates the challenger on
Slot-specific knowledge packs. A slot specifies a curated
                                                                            the evolution workload (a fixed HWMCC subset) under
set of files/functions (and optionally line ranges) that the pro-
                                                                            fixed timeouts, producing PAR2 and bucketed solved/-
grammer agent is allowed to modify in a given iteration. For
                                                                            timeout statistics.
each slot, we maintain a small, auditable knowledge pack that
collects the most relevant external and internal references, in-       (v) Diagnose & guide. The evaluator agent inspects
cluding solver code excerpts, open-source implementations,                  the patch diff and evaluation artifacts, confirms (or
and slot-specific papers and documentation. At each iteration,              refutes) the hypothesis, identifies bottlenecks, and
the Compass&Jump search policy retrieves and injects only                   returns a ranked MoveSet to guide the next slot and
the slot-relevant subset into the agents’ prompts to reduce                 edit direction.
context noise and constrain edits toward well-understood pat-       The challenger is promoted only if it passes hard gates and
terns. These knowledge packs only improve proposal qual-            improves the objective without unacceptable regressions; oth-
ity and interpretability; correctness is enforced solely by the     erwise, the framework rolls back to the champion and contin-
proof-/witness-gated validation.                                    ues with the next MoveSet.
Figure 2: Overview of IC3-Evolve. Compass&Jump selects slot(s); a programmer proposes a slot-restricted patch (with hypothesis and
fallback). A tool-using evaluator builds and witness-validates the challenger, benchmarks it (e.g., PAR2/solved), and returns a MoveSet.
Challengers are promoted only if they pass hard gates and improve under a regression budget. See agent prompt example in Section 6.1 in
Appendix.

 Algorithm 3: Compass & Jump search policy                            failure, or inconsistent return code) immediately rejects the
   Input : slots S; MoveSet M; progress history H; jump
                                                                      challenger regardless of its performance.
             prob. pJUMP ; jump size J ∈ {2, 3}
   Output: allowed slots A ⊆ S; guidance moves G; updated             Promotion and feedback on failures. Only challengers
             pJUMP                                                    that pass the hard gates are scored on performance metrics
 1 if M = ∅ then                                                      such as PAR2 and solved counts. When a challenger is
 2      sample s ∼ U NIFORM(S);                                       rejected—either by witness validation or by failing to im-
 3      return ({s}, ∅, pJUMP );                                      prove under the promotion rule—the evaluator inspects the
 4 end                                                                diff and logs to produce a diagnosis and a ranked MoveSet,
 5 pJUMP ← A DJUST J UMP (pJUMP , H);       // decrease if            which guides the programmer agent in the next iteration. This
     steady, increase if stagnant                                     proof-gated, witness-driven protocol ensures that evolution
 6 M ← R ANK B Y S CORE (M); // using the linear
                                                                      does not compromise the soundness of the underlying IC3
     score in Section 3.5
 7 if R AND () < pJUMP then
                                                                      proof logic.
 8      G ← T OP D ISTINCT S LOTS(M, J);
 9 end
      ⋆                                                               3.5    Search Policy: Compass&Jump
10 m ← S ELECT B EST (M, H);                  // optionally
     risk-averse when volatile
11 G ← {m };
             ⋆                                                        Compass&Jump is a lightweight search policy for choos-
12 A ← { m.slot | m ∈ G };
                                                                      ing the next editable slot(s) in the slot-restricted patch
13 return (A, G, pJUMP );                                             space.      After each iteration, the evaluator returns a
                                                                      MoveSet M, i.e., a ranked list of candidate moves m =
                                                                      (slot, direction, conf, risk, cost). We rank moves by a linear
                                                                      score score(m) = wc ·conf(m)−wr ·risk(m)−wk ·cost(m)
3.4   Proof-/Witness-Gated Evaluation & Promotion                     (fixed weights). With probability pJUMP the policy enters Jump
Proof and witness hard gates. For each benchmark in-                  mode and enables edits to the top J ∈ {2, 3} moves from dis-
stance that a challenger solves within the timeout, we require        tinct slots, encouraging cross-slot synergies; otherwise it en-
it to emit an artifact that can be checked independently of the       ters Compass mode and enables only the single best move
evolved solver. If the solver reports UNSAFE, it must dump            (optionally preferring a lower-risk move when progress is
a counterexample trace that is replayed by AIGSIM [Biere,             volatile). The jump probability pJUMP is adapted from recent
2014] to confirm that the trace indeed reaches a bad state. If        progress (decrease under steady improvement; increase un-
the solver reports SAFE, it must dump a proof (inductive in-          der stagnation). Compass&Jump controls only search scope
variant) that is validated by CERTIFAIGER [Yu et al., 2021].          and guidance; correctness is guaranteed solely by the proof-
Any mismatch (missing proof/witness artifact, replay/check            /witness-gated validation in Section 3.4.
4     Experiments                                                    if pushedThisRound or
                                                                        periodicCheckpoint():
4.1    Experimental Setup                                                simplify()
Platform. All experiments are conducted on Ubuntu                    record pushSuccessRate()
20.04.6 LTS, equipped with dual Intel® Xeon® Plat-                   This reduces low-yield cleanup without changing IC3’s proof
inum 8375C CPUs at 2.90 GHz.                                         checks, and sets up later stall-aware scheduling.
LLM model. We use GPT-5-Codex [OpenAI, 2025] as the                  r004: skip repeatedly stalled frames. The next edit
underlying model for both the programmer and evaluator               makes propagation stall-aware by tracking per-frame stall
agents during offline evolution.                                     streaks and skipping push attempts on repeatedly unproduc-
                                                                     tive frames:
Benchmarks. We evolve on a workload of 100 public                    if stallStreak[i] >= limit: continue
HWMCC AIGER instances [hwm, 2025b], selected to cover                pushFrame(i)
a broad range of difficulty, including trivial, non-trivial, and     updateStallStreak(i) // reset
possibly timeout cases (spanning both SAFE and UNSAFE).                                    // else ++
To assess transferability to production settings, we evaluate        By redirecting effort to frames that still show improvement,
the final evolved engine on another 100 HWMCC instances              the solver reduces churn and drops timeouts (25→22) with a
(not used during evolution) and 302 industrial verification in-      clear PAR2 gain.
stances provided by industry.                                        r013: stall-aware adaptive budgets. Finally, evolution
Evolution configuration. We start from IC3ref [Bradley,              learns an adaptive budgeting rule: allocate more push at-
2013], a lightweight textbook-style IC3 implementation with          tempts to frames with recent successes, and cut budgets ag-
minimal built-in heuristics, which provides a clean and              gressively for deeply stalled frames with early termination:
lightweight starting point for controlled evolution. We run          budget <- adaptBudget(i)
200 offline evolution iterations in total. In the first 100 itera-   // stall/success history
                                                                     while clausesRemain(i) and budget>0:
tions, we use a structured slot sweep to ensure broad cover-             attemptPush(i)
age: edits are restricted to one slot at a time, and we move             budget--
to the next slot after several consecutive non-improving at-         if earlyCut(i): break
tempts. In the remaining 100 iterations, we enable the Com-
                                                                     Compared to the binary skip/try rule, adaptive budgets contin-
pass&Jump search policy to select slots based on the eval-
                                                                     uously reallocate work based on observed yield, further im-
uator’s MoveSet feedback and to occasionally allow multi-
                                                                     proving PAR2 to 943.07 s. A more detailed case-study inter-
slot edits for exploring cross-slot synergies. Context-window
                                                                     pretation is provided in Section 6.3 in Appendix.
management is described in Section 6.2 in Appendix.
Timeout and metrics. We use a timeout of 1800 s per in-              4.3   Comparison with Strong IC3 Baselines
stance and report PAR2 (the averaged solving time, where a           Table 2 compares IC3-Evolve against several well-known
timeout is penalized as taking 2× the time limit).                   IC3-based engines on public HWMCC benchmarks and an
                                                                     industrial benchmark suite. We report #Solved (split into
4.2    Evolution Trace and Case Study                                #UNSAFE/#SAFE) and PAR2 under the same timeout limit.
Figure 3 visualizes a typical offline evolution run. PAR2 im-        The baselines include the vanilla IC3ref [Bradley, 2013],
provements arrive as a sequence of punctuated “jumps” in the         IC3ref with a stronger SAT backend (IC3ref-CaDiCaL),
best-so-far line, interleaved with many non-improving (and           ABC [Brayton and Mishchenko, 2010] (whose IC3 engine
thus rejected) challengers. The shaded phases correspond             is a widely-used industrial-strength model checker), and rIC3
to different exposed heuristic slots, illustrating how the evo-      as a strong recent IC3 implementation.
lution process explores and composes improvements across                A key fairness consideration is that a practical model
solver subroutines while keeping correctness guarded by wit-         checker is a pipeline that couples preprocessing, the model
ness validation.                                                     checking algorithm, and the SAT backend. In particular,
Case study: Push propagation (P USH C LAUSES). We                    rIC3 [Su et al., 2025a] is the recent HWMCC winner
zoom into rounds r000–r013, where edits are restricted to the        (HWMCC’24 [hwm, 2024] and HWMCC’25 [hwm, 2025a],
P USH C LAUSES slot (all other code frozen). Across three ac-        in the bit-level safety tracks), making it a natural reference
cepted edits, PAR2 decreases from 1050.61 s to 943.07 s and          point for performance comparison. Since IC3-Evolve tar-
timeouts drop from 25 to 21. Overall, the edits follow a con-        gets IC3 heuristic/code evolution rather than SAT-solver engi-
sistent theme: avoid low-yield cleanup and reallocate effort         neering, we control for the SAT backend by uniformly using
toward frames with observed progress.                                CaDiCaL [Biere et al., 2024] in our evolved engine and com-
Milestones (green bars in Figure 3). We summarize best-              paring primarily against rIC3-CaDiCaL (rIC3 with CaDiCaL
so-far PAR2 (s) and timeouts (TO): r000 1050.61/25, r002             as the backend SAT solver, following the comparison setup
1050.42/25, r004 983.73/22, r013 943.07/21.                          in [Su et al., 2025b]). This setup accurately measures im-
r002: observe & gate simplification. Simplification inside           provements attributable to IC3-level implementation choices.
propagation can be expensive when few clauses are moving.
The edit adds lightweight progress observation and triggers          4.4   Ablation Study
simplification only after successful pushing or at periodic          No-gate counterfactual (why proof-/witness gating is
checkpoints:                                                         necessary). In rounds r093–r094, IC3-Evolve proposed
Figure 3: Representative evolution trace on the HWMCC optimization workload. Bars: attempted challengers; line: best-so-far PAR2 (lower
is better). Green bars: accepted new best; shading: editable slot(s) per phase.
                                HWMCC Set Aa                           HWMCC Set Ba                          Industry Benchmark
Solver
                         b
                   #S/#T #UNSAFE #SAFE PAR2(s) #S/#T #UNSAFE #SAFE PAR2(s)                         #S/#T     #UNSAFE #SAFE PAR2(s)
       c
IC3ref         75/100             21        54    1050.61 75/100        26         49     1068.33 187/302        39      148      1403.31
IC3ref-CaDiCaL 85/100             22        63     718.87 85/100        28         57      732.28 198/302        38      160      1302.13
ABC                86/100         22        64     665.59   88/100      26         62     618.59   185/302       36      149      1417.50
rIC3-CaDiCaL       86/100         21        65     639.61   89/100      27         62     524.35   182/302       36      146      1449.78
IC3-Evolve         92/100         24        68     490.67   94/100      28         66     464.56   225/302       36      189      1044.26
a
  HWMCC Set A is the offline evolution set; Set B is unseen and not used in evolution..
b
  #S/#T denotes #Solved/#Total (solved instances / total instances).
c
  IC3ref serves as the starting point for our offline code evolution.

                                  Table 2: Baseline comparison on public HWMCC and industrial benchmarks.

                       HWMCC Set A         HWMCC Set B
    Variant          (#Solved / PAR2(s)) (#Solved / PAR2(s))            tines remain frozen and only one “knob family” can be
                                                                        improved. As shown in Table 3, single-slot evolution yields
    Baseline             75 / 1050.61            75 / 1068.33           only marginal and often unstable gains: improvements are
    PO-only               78 / 995.35            75 / 1093.42           small and may fail to transfer across sets (e.g., PO-only
    PredGen-only          79 / 954.36             78 / 970.38           and Push-only improve little on Set B and can even regress
    IndGen-only           78 / 927.80             84 / 803.73           PAR2). Moreover, naively composing the best single-slot ed-
    Push-only            76 / 1016.05            75 / 1139.22           its (Naive-Compose) improves over the baseline but still falls
    Naive-Compose            78 / 944.86         85 / 775.19            far short of the full IC3-Evolve champion (e.g., Set B:
    IC3-Evolve               92 / 490.67         94 / 464.56
                                                                        85 vs. 94 solved, PAR2 775 vs. 465). These results suggest
                                                                        that IC3 heuristics are tightly coupled: effective optimization
                                                                        requires coordinated, feedback-driven cross-slot evolution
Table 3: Slot-isolated and naive-composition ablation. Single-slot-
only variants vs. Naive-Compose vs. full IC3-Evolve.                    with regression-aware promotion, rather than isolated slot
                                                                        tweaking or ad hoc “pick-and-mix” combinations.
a new clause-cleaning heuristic that would have increased
solved instances on the evolution workload by +9, and                   5    Conclusion and Future Work
would be promoted under performance-only selection. How-
ever, the challenger failed independent witness validation              We presented IC3-Evolve, an offline LLM-driven code-
(certificate checking / trace replay) and was rejected by our           evolution framework that proposes slot-restricted, auditable
proof-/witness gate. This counterfactual shows that witness             edits and admits them only through proof-/witness-gated val-
gating is essential: it prevents unsound “improvements” from            idation, producing a standalone evolved checker with zero
becoming champion and propagating into later rounds.                    runtime model dependency. Across public unseen/industrial
                                                                        workloads, IC3-Evolve delivers substantial performance
Slot-isolated evolution (IC3 optimization is not a                      gains, while our ablations indicate that improvements are not
low-hanging fruit). We run four ablations where                         a low-hanging fruit: isolated single-slot evolution and naive
IC3-Evolve is restricted to a single heuristic slot for                 composition fall far short of the full cross-slot champion.
the entire evolution budget, meaning that all other subrou-             More broadly, our results suggest that proof-producing ver-
ification offers a uniquely safe and reproducible setting for     [Le et al., 2021] Nham Le, Xujie Si, and Arie Gurfinkel.
evaluator-driven LLM code evolution. Future work will ex-            Data-driven optimization of inductive generalization. In
plore broader edit spaces beyond fixed slots, while maintain-        FMCAD, pages 86–95, 2021.
ing auditability and regression control.                          [Novikov et al., 2025] Alexander Novikov, Ngân Vũ, Mar-
                                                                     vin Eisenberger, Emilien Dupont, Po-Sen Huang,
References                                                           Adam Zsolt Wagner, Sergey Shirobokov, Borislav Ko-
[Biere et al., 2024] Armin Biere, Tobias Faller, Katalin             zlovskii, Francisco JR Ruiz, Abbas Mehrabian, et al. Al-
   Fazekas, Mathias Fleury, Nils Froleyks, and Florian Pol-          phaevolve: A coding agent for scientific and algorithmic
   litt. CaDiCaL 2.0. In Arie Gurfinkel and Vijay Ganesh,            discovery. arXiv preprint arXiv:2506.13131, 2025.
   editors, Computer Aided Verification - 36th International      [OpenAI, 2025] OpenAI. Addendum to gpt-5 system card:
   Conference, CAV 2024, Montreal, QC, Canada, July 24-              Gpt-5-codex, 2025.
   27, 2024, Proceedings, Part I, volume 14681 of Lec-
                                                                  [Pirzada et al., 2024] Muhammad AA Pirzada, Giles Reger,
   ture Notes in Computer Science, pages 133–152. Springer,
   2024.                                                             Ahmed Bhayat, and Lucas C Cordeiro. Llm-generated
                                                                     invariants for bounded model checking without loop un-
[Biere, 2014] Armin Biere. Aiger and-inverter-graph library          rolling. In Proceedings of the 39th IEEE/ACM Interna-
   and utilities (incl. aigsim). https://github.com/arminbiere/      tional Conference on Automated Software Engineering,
   aiger, 2014.                                                      pages 1395–1407, 2024.
[Bradley, 2011] Aaron R. Bradley. Sat-based model check-          [Su et al., 2024] Yuheng Su, Qiusong Yang, and Yiwei Ci.
   ing without unrolling. In Ranjit Jhala and David Schmidt,         Predicting lemmas in generalization of ic3. In Proceed-
   editors, Verification, Model Checking, and Abstract Inter-        ings of the 61st ACM/IEEE Design Automation Confer-
   pretation, pages 70–87, Berlin, Heidelberg, 2011. Springer        ence, DAC ’24, New York, NY, USA, 2024. Association
   Berlin Heidelberg.                                                for Computing Machinery.
[Bradley, 2013] Aaron R. Bradley. IC3ref: Ic3 reference im-       [Su et al., 2025a] Yuheng Su, Qiusong Yang, Yiwei Ci, Tian-
   plementation. https://github.com/arbrad/IC3ref, 2013.             jun Bu, and Ziyu Huang. The ric3 hardware model
[Brayton and Mishchenko, 2010] Robert Brayton and Alan               checker, 2025.
   Mishchenko. Abc: An academic industrial-strength ver-          [Su et al., 2025b] Yuheng Su, Qiusong Yang, Yiwei Ci,
   ification tool. In International Conference on Computer           Yingcheng Li, Tianjun Bu, and Ziyu Huang. Deeply opti-
   Aided Verification, pages 24–40. Springer, 2010.                  mizing the sat solver for the ic3 algorithm, 2025.
[Eén et al., 2011] Niklas Eén, Alan Mishchenko, and Robert      [Sun et al., 2024] Yiwen Sun, Furong Ye, Xianyin Zhang,
   Brayton. Efficient implementation of property directed            Shiyu Huang, Bingzhen Zhang, Ke Wei, and Shaowei Cai.
   reachability. In 2011 Formal Methods in Computer-Aided            Autosat: Automatically optimize sat solvers via large lan-
   Design (FMCAD), pages 125–134. IEEE, 2011.                        guage models. arXiv preprint arXiv:2402.10705, 2024.
[Hu et al., 2023] Guangyu Hu, Wei Zhang, and Hongce               [Wu et al., 2024] Guangyuan Wu, Weining Cao, Yuan Yao,
   Zhang. Neuropdr: Integrating neural networks in the               Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. Llm meets
   pdr algorithm for hardware model checking. In 2023                bounded model checking: Neuro-symbolic loop invariant
   ACM/IEEE 5th Workshop on Machine Learning for CAD                 inference. In Proceedings of the 39th IEEE/ACM Inter-
   (MLCAD), pages 1–6. IEEE, 2023.                                   national Conference on Automated Software Engineering,
[Hu et al., 2024] Guangyu Hu, Jianheng Tang, Changyuan               pages 406–417, 2024.
   Yu, Wei Zhang, and Hongce Zhang. Deepic3: Guiding              [Yu et al., 2021] Emily Yu, Armin Biere, and Keijo Hel-
   ic3 algorithms by graph neural network clause prediction.         janko. Progress in certifying hardware model checking
   In 2024 29th Asia and South Pacific Design Automation             results. In Alexandra Silva and K. Rustan M. Leino, edi-
   Conference (ASP-DAC), pages 262–268. IEEE, 2024.                  tors, Computer Aided Verification, pages 363–386, Cham,
[hwm, 2024] HWMCC 2024: Hardware model checking                      2021. Springer International Publishing.
   competition 2024 (results). https://hwmcc.github.io/2024/,     [Yu et al., 2025] Cunxi Yu, Rongjian Liang, Chia-Tung Ho,
   2024.                                                             and Haoxing Ren. Autonomous code evolution meets np-
[hwm, 2025a] HWMCC 2025: Hardware model checking                     completeness. arXiv preprint arXiv:2509.07367, 2025.
   competition 2025 (results). https://hwmcc.github.io/2025/,
   2025.
[hwm, 2025b] HWMCC: Hardware model checking compe-
   tition. https://hwmcc.github.io/, 2025.
[Janßen et al., 2024] Christian Janßen, Cedric Richter, and
   Heike Wehrheim. Can chatgpt support software veri-
   fication?     In International Conference on Fundamen-
   tal Approaches to Software Engineering, pages 266–279.
   Springer, 2024.
6     Appendix                                              - Edit only project sources (.c/.cc/.cpp/.h/.hpp). Do NOT
                                                                 touch: aiger/, minisat/, scorr_aig/, test/.
6.1    Prompt Templates                                     - Keep SAFE/UNSAFE semantics: in main.cpp, return 0 =
                                                                 SAFE, 1 = UNSAFE.
Evaluator Agent Prompt                                      - Prefer changes within IC3*/Model*/main.cpp unless
                                                                 explicitly justified.
             Listing 1: Evaluator Agent prompt.
                                                            Slot discipline:
You are the Evaluator Agent. Given (i) a patch diff and     - Primary slot must be declared in Hypothesis.json (see
     (ii) build/run logs + metrics, decide whether to            Listing˜\ref{lst:hypothesis_schema}); optional
     ACCEPT, REVERT, or RETRY.                                   cross-slot touches must be listed and kept surgical.
                                                            - If SLOT_FOCUS is set, stay within it unless strictly
Hard semantics / ground rules:                                   necessary.
- Treat metrics.runs[*].ok as the pass/fail truth
     (allowed return codes already reflected there).        Instrumentation (optional but encouraged):
- In main.cpp: return code 0 = SAFE, 1 = UNSAFE (not a      - Print one-line counters as: ‘. HYP <key>: <value>‘ for
     crash).                                                     parsing.
- Do not assume the suite is mixed SAFE/UNSAFE; uniform
     outcomes are valid if consistent with logs/metrics.    Required output:
- Do not infer expectations from filenames; use only the    - Edit the repository files directly AND create
     provided artifacts.                                         Hypothesis.json at repo root.
                                                            - Do NOT return a diff in the response.
Performance signals:
- Primary: metrics.par2.avg_sec (PAR2 uses 2*timeout for    Inputs (placeholders):
     timeouts; lower is better).                            REPO MAP: {{CODE_SNIPPET}}
- Secondary: solved/timeout counts; optional per-case IC3   KB: {{KB_SNIPPET}}
     stats to explain regressions/improvements.             LATEST DIAGNOSIS: {{DIAGNOSIS_SNIPPET}}
                                                            MOVESET: {{MOVES_PROMPT}}
Decision rubric:                                            CJ_PLAN: {{CJ_PLAN_SNIPPET}}
- ACCEPT iff build_ok=true AND all runs ok AND no           SLOT_FOCUS: {{SLOT_FOCUS}}
     witness/consistency failures AND performance
     improves under the regression budget.
- REVERT iff build fails OR any run ok=false OR witness
     validation fails OR the diff obviously breaks          6.2   Context Management for Prompt
     SAFE/UNSAFE semantics.                                       Construction
- RETRY iff results are inconclusive or the patch appears
     inert (no measurable change and no clear harm).        LLM-driven code evolution must operate under a finite
Output format (STRICT):                                     context window while handling repository-scale code, per-
- Return ONLY one fenced code block of type json,           instance logs, and retrieval-augmented notes. To keep
     matching the diagnosis_v1 schema in
     Listing˜\ref{lst:diagnosis_schema}.
                                                            IC3-Evolve robust across long runs, we use a hierarchi-
- Include: decision, 3-6 numeric reasons, evidence          cal truncation strategy that assigns an explicit budget to each
     summary, hypothesis evaluation (if provided), and a    prompt component and degrades gracefully when overflow is
     MoveSet for the next iteration.
                                                            detected.
MoveSet requirements (brief):
- Provide multiple candidate moves with scores              Hierarchical prompt budgeting. We prioritize high-signal
     (confidence/risk/cost) and expected metric             artifacts and cap every input by length (line/character) lim-
     directions.                                            its: (i) Selective code context: we provide a brief repository
- Compass: 2-3 single-slot moves. Jump: >=2 moves from
     distinct slots.                                        summary plus local snippets around the target functions and
- Prioritize SLOT_FOCUS if provided; only propose           a small diff excerpt, avoiding full-source injection; (ii) Log
     cross-slot moves when justified by evidence.
                                                            trimming: we include detailed logs only for the slowest top-
Inputs (placeholders):                                      k% cases and truncate each case by both a maximum number
KB: {{KB_SNIPPET}}                                          of lines and characters; build/run summaries are also clipped;
DIFF: {{DIFF_SNIPPET}}
LOGS: {{LOGS_SNIPPET}}                                      (iii) Slot-aware KB retrieval: knowledge-base snippets are re-
METRICS: {{METRICS_JSON}}                                   trieved by slot relevance (path/slot priority) with a hard length
BASELINE: {{BASELINE_JSON}}                                 cap (and can be disabled when needed); (iv) Structured stat-
STATS: {{STATS_JSON}}
HYPOTHESIS: {{HYPOTHESIS_JSON}}                             s/diffs: metrics, per-case statistics, and diffs are truncated to
PREV_MOVES: {{MOVES_PROMPT}}                                essential fields and subject to hard caps. Algorithm 4 sum-
CJ_PLAN: {{CJ_PLAN_SNIPPET}}
                                                            marizes the resulting prompt assembly, where KB denotes a
                                                            slot-specific knowledge base (curated notes/code excerpts/pa-
Programmer Agent Prompt                                     pers per slot) and slot focus specifies the currently editable
                                                            slot(s).
            Listing 2: Programmer Agent prompt.
You are the Programmer Agent evolving the IC3 repository.
                                                            Automatic slim-prompt fallback. If the framework
                                                            detects a context overflow (or missing/invalid agent
Goal:                                                       output), it automatically retries with a slim prompt
- Propose ONE minimal, safe improvement to IC3
     implementation heuristics (or instrumentation)
                                                            that omits KB snippets and aggressively shortens
     within the selected slot(s).                           logs/metrics/moveset/changed-file excerpts.      Importantly,
                                                            this truncation affects only the agent-facing diagnosis and
Hard constraints:
- Small patch: <=80 added lines, <=3 files; must compile    guidance; proof-/witness-gated validation and benchmarking
     with existing Makefile.                                are executed on the full, untruncated artifacts.
 Algorithm 4: Prompt assembly with bounded context                wasted cleanup on rounds with no movement. More impor-
  Input: diff, metrics, logs, KB, slot focus
                                                                  tantly, it creates a lightweight progress proxy (e.g., push suc-
  Output: prompt                                                  cess rate) that makes subsequent stall-aware policies imple-
1 Assemble core fields (slot focus, diff summary, key metrics);   mentable and auditable.
2 Attach local code snippets for target functions (budgeted);
3 Attach logs for top-k% slow cases (clip by lines/chars);        Stage 2 (r004): Skip Repeatedly Stalled Frames
4 Attach slot-relevant KB snippets (cap length);                  Motivation. Once progress can be observed, the next bot-
5 if prompt exceeds budget or agent output missing then
                                                                  tleneck is repeated work on frames that consistently fail to
6      Drop KB; shorten logs/metrics/moveset; retry (slim         push any clause forward. Treating repeated failure as a strong
        prompt);
                                                                  negative signal allows the solver to stop spending budget on
7 end
                                                                  “hopeless” frames within the current round.
                                                                  Auto-learned rule (diff-style, simplified).
6.3   Extended Case Study: Auto-Evolving Push                     if stallStreak[i] >= limit: continue
                                                                  pushFrame(i)
      Propagation                                                 updateStallStreak(i) // reset
Setup. We study how IC3-Evolve improves IC3’s push                                      // else ++
propagation loop when only the P USH C LAUSES slot is ed-         Why it helps. This change makes the loop explicitly stall-
itable. Specifically, we zoom into rounds r000–r013 of a rep-     aware: instead of uniform effort across frames, it redirects
resentative evolution run on the HWMCC optimization work-         attempts toward frames that still show movement. Empiri-
load (Set A). All other IC3 components are frozen, and every      cally, this corresponds to the first major jump in Table 4 (TO
candidate is subject to the same proof-/witness-gated valida-     25→22; PAR2 1050.42→983.73), consistent with reduced
tion as in the main paper.                                        churn in propagation.
Milestones. Table 4 summarizes the best-so-far solver vari-
ants (green bars in Figure 3). Even within a single slot,         Stage 3 (r013): Stall-Aware Adaptive Budgets
progress is punctuated: many proposals are rejected, while        Motivation. Stage 2 uses a binary decision (skip vs. try). A
a few accepted edits yield discrete drops in PAR2.                natural refinement is to turn this into a graded allocation pol-
                                                                  icy: give more attempts to promising frames and cut budgets
Table 4: Milestones during the push-propagation phase (Set A).    aggressively for deeply stalled frames, with early termination
PAR2 is in seconds (lower is better); TO denotes timeouts.        when marginal returns are low.
                                                                  Auto-learned rule (diff-style, simplified).
               Round              PAR2 (s)     TO                 budget <- adaptBudget(i)
               r000 (baseline)    1050.61      25                 // stall/success history
               r002 (Stage 1)     1050.42      25                 while clausesRemain(i) and budget>0:
               r004 (Stage 2)      983.73      22                     attemptPush(i)
               r013 (Stage 3)      943.07      21                     budget--
                                                                  if earlyCut(i): break
                                                                  Why it helps. Compared to the skip/try rule, adaptive bud-
High-level pattern. Across the three accepted edits, the          gets continuously reallocate effort based on observed yield.
evolution converges on a consistent scheduling principle:         This yields a further (smaller but consistent) improvement
avoid low-yield cleanup and reallocate effort toward frames       (PAR2 983.73→943.07; TO 22→21), suggesting that fine-
that show evidence of progress. Notably, the first ac-            grained budget control captures additional efficiencies be-
cepted change yields only a marginal PAR2 improvement             yond simple stall skipping.
(1050.61→1050.42), but it introduces a measurable signal
that later edits exploit to make more aggressive stall-aware      6.4   What This Reveals About Offline LLM-Driven
decisions.                                                              Code Evolution
                                                                  From measurement to control. The accepted edits follow
Stage 1 (r002): Observe & Gate Simplification                     a coherent progression: (i) introduce a measurable proxy of
Motivation. Simplification/cleanup inside propagation can         progress, (ii) use it to avoid repeated low-yield work, and
be expensive, and its benefit can be low when the propagation     (iii) refine the policy into a graded budget allocator. This
loop is not moving clauses. A natural first step is to instru-    “instrument → gate → adapt” pattern is typical in human
ment progress and gate expensive work on that signal.             heuristic engineering, yet here it is discovered through iter-
Auto-learned rule (simplified).                                   ative propose–evaluate–promote under strict gates.
if pushedThisRound or                                             Compositionality under constraints. All changes are slot-
   periodicCheckpoint():                                          restricted and easy to audit, and they compose cleanly be-
    simplify()                                                    cause each stage refines the same underlying scheduling ob-
record pushSuccessRate()                                          jective (yield-aware propagation) rather than introducing un-
Why it helps. This edit preserves IC3’s proof logic (no           related tweaks. This helps explain why the framework can
change to SAT checks or clause soundness), but reduces            accumulate gains without destabilizing the solver.
Takeaway. Even when only push propagation is editable,
IC3-Evolve discovers simple, readable rules that reduce
wasted work and reallocate effort toward productive frames,
achieving a measurable reduction in PAR2 and timeouts
while leaving IC3’s proof logic unchanged.
