                                                  NormWorlds-CF: Solver-Verified Counterfactual Normative Reasoning
                                                                with Metamorphic-Relation GRPO

                                                                                                          Xinqi Zhang1
                                                                                                     1
                                                                                                         Tsinghua University




                                                                     Abstract                                           This problem is easy to understate if one imports the domi-
                                                                                                                     nant post-training template from mathematics. In math word
                                           Language models can reach the right normative verdict for
                                           the wrong reason. We introduce NormWorlds-CF, a solver-                   problems and contest-style reasoning, supervision and re-
                                           verified environment for counterfactual normative reasoning               ward often reduce to a sparse final answer: the boxed number
                                           in executable rule worlds. Its deterministic solver produces              or option is a strong proxy for correctness, and process re-
                                           final answers, proof and falsification certificates, argument             wards are valuable mainly because the answer space is vast
                                           statuses, support sets, and paired-world change labels, en-               and lucky guessing is rare (Cobbe et al. 2021; Lightman
arXiv:2607.03957v2 [cs.CL] 28 Jul 2026




                                           abling supervision and evaluation without LLM judges. The                 et al. 2024; Shao et al. 2024). Normative decision making
                                           benchmark contains staged SFT diagnostics and a compact                   is different in kind. The “answer” is typically drawn from
                                           paired-world task with 270 root families and 1080 canonical-              a small label set (permitted/forbidden/obligated/. . . ), so
                                           to-variant pairs. The SFT diagnostics show that final-answer              high answer accuracy can be achieved by shallow cues. What
                                           supervision can saturate verdict accuracy without inducing
                                                                                                                     matters is dialectical: which rule survives, which conflicting
                                           falsification competence: answer-only SFT reaches perfect
                                           answer accuracy but scores zero on joint falsification cer-               argument is defeated, and whether a proposed justification
                                           tificates, while full-mix training with targeted replay reaches           should be rejected. In that sense, our setting is closer to a
                                           strong all-task accuracy (0.99). For the structured-change task,          structured judgment task than to answer-sparse mathemati-
                                           we introduce metamorphic-relation GRPO (MR-GRPO), a                       cal derivation—and answer-only supervision is insufficient
                                           class-conditioned reward for GRPO that gives partial credit               and potentially misleading as a proxy for dialectical compe-
                                           for relation families and solver-visible change fields. In                tence.
                                           matched Qwen3-1.7B continuation experiments, MR-GRPO                         The empirical bottleneck is therefore attribution, not a
                                           improves held-out relation accuracy and relation-family cor-
                                           rectness, and reduces wrong-family error, compared to sparse
                                                                                                                     shortage of benchmarks. Legal evaluation suites and legal-
                                           and answer-only GRPO. In Qwen3-4B three-seed validation,                  domain LLMs are essential for external validity (Chalkidis
                                           sparse reward preserves coarse relation labels best, answer-              et al. 2022; Guha et al. 2023; Fei et al. 2024; Colombo et al.
                                           only reward improves answer-change but weakens relation-                  2024), but realistic legal tasks entangle knowledge, retrieval,
                                           family structure, and MR-GRPO leads on answer-, support-,                 drafting, and reasoning. Controlled reasoning benchmarks
                                           and status-change fields as well as class-conditioned MR and              isolate compositionality (Weston et al. 2015; Johnson et al.
                                           change-presence. These results show that verified counterfac-             2017; Clark, Tafjord, and Richardson 2020; Tafjord, Dalvi,
                                           tual structure can shape post-training beyond final answers,              and Clark 2021), yet rarely expose defeasible conflict, prior-
                                           while exact full change-record generation, invariant subtype              ity, and defeated-argument structure. Post-training research
                                           recognition, and out-of-distribution (OOD) transfer remain                needs environments that are rich enough to be interesting
                                           open problems.
                                                                                                                     and executable enough that supervision, reward, and evalua-
                                                                                                                     tion do not depend on LLM judges—whose own normative
                                                              1     Introduction                                     judgments would reintroduce the very attribution problem
                                         Normative reasoning exposes a failure mode that ordinary                    we aim to study.
                                         post-training metrics miss: a model can be right at the surface                We address this gap with NormWorlds-CF, a solver-
                                         and wrong in the structure. A useful reasoner in legal, insti-              verified laboratory for counterfactual normative reasoning
                                         tutional, or policy-like settings must track rules, exceptions,             (Figure 1). Each instance is generated from an executable
                                         priorities, defeated arguments, and counterfactual edits (von               rule world; deterministic solvers emit answers, proof and fal-
                                         Wright 1951; Nute 1994; Prakken and Sartor 2015; Guha                       sification certificates, argument statuses, minimal support,
                                         et al. 2023). Predicting permitted is useful only if the model              and root-level metamorphic relations. Errors become in-
                                         can name the decisive rule, explain why a plausible prohi-                  spectable: answer error, invalid proof, missing falsification,
                                         bition is defeated, and recognize when removing a priority                  relation-family confusion, schema failure, or counterfactual
                                         edge should flip the conclusion. Final-answer accuracy—                     generalization failure can be separated. The construction is
                                         and therefore final-answer reward—can hide exactly these                    motivated by a concrete design bet: if we want to study how
                                         failures.                                                                   post-training shapes normative structure, we must first make
that structure machine-checkable.                                                    2    NormWorlds-CF
   The study is staged by design. We first ask whether             NormWorlds-CF separates three objects often conflated in
small models can learn solver-generated interfaces under           natural-language benchmarks: a symbolic world (source
SFT, comparing answer-only, answer-plus-proof (no falsi-           of truth), a textual rendering (prompt only), and solver-
fication), answer-plus-proof-plus-falsification, and targeted-     generated labels (never an LLM judge).
replay curricula. Only after structured outputs stabilize do
we move to RL; otherwise an RL failure would be unin-              2.1   Design Principles: Why Build It This Way
terpretable. For RL, we formulate a compact paired-world           The dataset is not a miniaturized legal corpus. It is built to
change task inspired by metamorphic testing (Chen, Che-            answer a post-training question that open-text legal bench-
ung, and Yiu 1998; Chen et al. 2018): each root family pairs       marks cannot cleanly ask: when a model improves, what
a canonical world with transformed variants that should pre-       improved? Three principles follow.
serve or change normative structure in named ways. The
model outputs a machine-scored change record over rela-            Executable worlds before fluent text Realistic statutes
tion, answer, support, status, and attack fields—harder than       mix doctrine, drafting conventions, and retrieval. We instead
final-answer prediction, but more focused than regenerating        start from ground facts, typed rules, and priorities whose con-
two full certificates.                                             sequences are computable. Templates may generate surface
   We compare answer-only reward, sparse exact/schema              wording, but ground truth never depends on that wording.
GRPO (Shao et al. 2024; Guo et al. 2025), and MR-GRPO,             This reverses a common pipeline that annotates natural text
a class-conditioned reward that gives partial credit for meta-     first and hopes structure can be recovered later.
morphic structure. The central empirical finding is a re-          No LLM judges by construction If labels or rewards were
ward geometry: different rewards induce different shortcuts        themselves produced by an LLM, evaluation would inherit
rather than a single winner. Answer-only reward repairs local      that model’s normative biases and its tendency to reward
answer-change fields while shifting the relation prior toward      fluent but structurally wrong justifications. Here every an-
change labels. Sparse reward preserves coarse relation la-         swer, certificate field, falsification error type, and metamor-
bels but often leaves many training groups with zero within-       phic change record is emitted by a deterministic solver over a
group reward variance, starving GRPO’s ranking signal. MR-         closed DSL. Scoring is likewise parser-based. The advantage
GRPO densifies that signal and improves answer-, support-,         is not only reproducibility: it makes reward design scientif-
and status-change fields together with class-conditioned soft      ically meaningful, because credit assignment refers to the
scores, while exact full-record generation, invariant subtype      same objects the evaluator checks.
recognition, and OOD transfer remain open.
                                                                   Dialectical targets, not answer-sparse math Math RL of-
Contributions     This paper makes three contributions:            ten treats a rare correct final answer as the learning signal.
                                                                   Our answers are dense and low-entropy; the scarce resource
1. We introduce NormWorlds-CF, a solver-verified environ-          is structural fidelity. Call this a scarcity inversion: in con-
   ment for counterfactual normative reasoning with exe-           test math, the bottleneck is finding the answer; in normative
   cutable worlds, deterministic certificates, compact paired-     judgment, the bottleneck is defending and attacking under
   world change records, family-level splits, and OOD struc-       conflict. That is why the task suite foregrounds proof (jus-
   tural probes—motivated by the need to separate norma-           tify the winner), falsification (reject a plausible loser), and
   tive structure from open-text legal confounding.                paired-world change (state what a transformation should al-
2. We show that final-answer supervision can saturate ver-         ter). These are judgment-style interfaces: the model must
   dict accuracy without inducing solver-verified falsifica-       accept or reject candidate structure under an executable ora-
   tion competence: proof and falsification expose different       cle, rather than search a vast answer space for a single token
   capabilities, and targeted replay repairs concrete failures     sequence.
   under deterministic scoring.
                                                                   2.2   Executable Worlds and Certificates
3. We formulate compact structured-change prediction as            A world is a finite rule program w = (F, R, P, q) with ground
   a reward-ready post-training task and introduce MR-             facts F , instantiated typed rules R, priority relation P ⊆ R×
   GRPO. Under matched protocols, answer-only, sparse,             R, and query q. Templates may be used during generation, but
   and MR-aware GRPO learn different slices of the same            the solver receives only ground rule objects: each rule has an
   structure and expose characteristic shortcuts.                  identifier, a kind, an action, and a finite set of preconditions.
   The organizing claim is broader than “MR-GRPO beats             A priority edge (ri , rj ) ∈ P means that ri overrides rj under
a baseline.” Outcome supervision cannot identify norma-            conflict. A deterministic solver S maps w to an answer a and
tive structure quality; solver-verified counterfactual structure   certificate C:
makes that quality measurable at three levels—supervision                                   S(w) = (a, C),                       (1)
targets, evaluation tasks, and reward design—especially            where C contains decisive rules, defeated alternatives,
when answers are low-entropy and structure is scarce. Scope        argument statuses, and minimal support. If no applica-
is controlled: NormWorlds-CF is a laboratory for verified          ble normative rule supports the query, the answer is
normative structure, not a substitute for open-ended legal         no_conclusion; if incompatible undefeated arguments re-
expertise.                                                         main, conflict_unresolved; otherwise the answer is read
Figure 1: Overview of NormWorlds-CF. Executable rule worlds are solved by deterministic procedures that produce verified
answers, certificates, and paired-world change records. These solver-generated structures support staged SFT diagnostics and a
matched GRPO comparison among answer-only, sparse exact/schema, and MR-aware change-field rewards—all evaluated by
deterministic scorers, without LLM judges.


from surviving labels under a fixed reporting convention            hibition, obligation vs. prohibition); apply priorities by di-
(obligated before forbidden before permitted). That con-            rected graph reachability; then extract certificates and fal-
vention is only a serialization order, not a claim about legal or   sification error types (e.g., defeated rule cited as decisive,
ethical priority. Transformations τ are executable edits. Each      unresolved conflict ignored, missing precondition). Minimal
τ carries a family label rτ determined by its edit operator and     support searches subsets of decisive rules sufficient to sus-
validated against solver-computed pre- and postconditions;          tain the answer while defeating conflicting alternatives. Su-
fine-grained answer, support, status, and attack changes are        pervision therefore has three layers: a decision layer (final
obtained by differencing the two solver traces,                     answer), a certificate layer (proof, falsification, statuses, sup-
                                                                  port), and a counterfactual layer (paired-world relation and
           M (w, τ ) = rτ , D S(w), S(τ (w)) ,               (2)    change fields). In the archive example, predicting forbidden
not by inspecting free-form text after the fact. In partic-         is an answer error; predicting permitted while citing r1 is a
ular, rτ distinguishes relation subtypes that share similar         proof error; failing to reject candidate forbidden is a falsifi-
or empty field diffs (e.g., surface_invariant vs. distrac-          cation error; claiming that priority removal changes nothing
tor_invariant).                                                     is a counterfactual error. This typed failure taxonomy is it-
   Consider a toy archive-entry case: facts appren-                 self a contribution of the environment: it turns “the model is
tice(alice) and emergency_rescue(alice); rule r1 forbids            wrong” into a researchable diagnosis.
entry for apprentices; rule r2 permits entry under emergency
rescue; priority r2 > r1. Both rules apply and conflict; priority   2.3   Diagnostic Task Ladder
selects permitted, with decisive rule r2 and defeated rule r1.      The same worlds feed a staged interface suite (Table 1) rather
Removing the priority edge yields conflict_unresolved;              than a single monolithic benchmark. The result is a diagnos-
removing the emergency fact yields forbidden; adding an             tic ladder: a model may learn final answers before proofs,
irrelevant fact should leave the certificate invariant. These       proofs before falsification, and still fail when asked to com-
edits define the four root-level metamorphic families used          pare a root world with a transformed variant. Answer and
later. The same object also makes reward differences con-           certificate tasks establish whether solver structure is learn-
crete: an output that flips the answer-change field but invents     able under SFT. Early micro corpora make those interfaces
a change relation on an invariant edit can be credited by           measurable (sizes and task mixes in the supplementary mate-
answer-only reward, penalized by sparse exactness, and only         rial). Surface-varied micro data (1000 roots, 4000 instances)
partly credited by MR-GRPO through family and emptiness             then varies lexical forms, entity names, rule-id prefixes, and
terms.                                                              fact/rule order while preserving solver-equivalent structure,
   Label construction is a closed symbolic procedure over a         checking that models learn the rule pattern rather than a
fixed schema: forward-chain identity rules to a fixed point;        single template; all renderings of one root stay in the same
select applicable normative arguments whose preconditions           split.
hold; attack only incompatible labels (permission vs. pro-             The compact change-record task is the RL bridge. Re-
 Interface       What it tests                                           Split       Fam.    Cases    Pairs   Role
 Answer          Final decision on original or edited worlds             Train        120      600     480    Optimization
 Proof           Decisive/defeated rules and support facts               Dev           30      150     120    Diagnostics
 Falsification   Reject invalid answers/certificates with error          ID test       60      300     240    Held-out ID
                 type                                                    OOD test      60      300     240    Held-out types
 Arg. cert.      Accepted/defeated/undecided argument nodes
 Change rec.     Relation + answer/support/status/attack changes   Table 3: Root-level MR pilot scale (270 families, 1080 pairs).

Table 1: Task interfaces derived from the same solver-verified
worlds.                                                            the reward geometry. We report two complementary proto-
                                                                   cols: a Qwen3-1.7B continuation that starts from a shared
 Field               Scored content                                sparse-GRPO adapter, and a Qwen3-4B scale check that
                                                                   starts from a shared aligned-SFT adapter.
 relation            One of four MR labels
 answer change       Unchanged/changed; both answers
 support change      Added/removed rules, facts, priorities        3.1   SFT as Interface Substrate
 status change       Added/removed argument statuses               SFT is part of the method, not a disposable warmup. Because
 attack change       Added/removed attack edges                    the task is judgment-structured rather than answer-sparse, we
                                                                   treat interface competence as a scientific prerequisite: if a
  Table 2: Compact paired-world change-record schema.              model cannot emit proof or falsification fields under direct
                                                                   supervision, later RL comparisons would confound reward
                                                                   design with serialization failure.
generating two nested certificates proved too noisy in pi-            Answer-only training uses only original- and edited-
lot prompts—a failed output could reflect reasoning fail-          world answer targets. The answer-plus-proof condition keeps
ure, formatting failure, or excessive sequence length—so           those answer targets and adds decisive rules, defeated rules,
the model emits a five-field record (Table 2): relation plus       and support—but no falsification. Answer-plus-proof-plus-
answer/support/status/attack changes. This target is small         falsification keeps the answer and proof targets and fur-
enough to score repeatedly during GRPO, yet structured             ther adds falsification certificates (error type and counter-
enough to distinguish coarse relation recognition from fine-       evidence). Targeted replay keeps that full mix while oversam-
grained change description.                                        pling residual failure families (unresolved-vs-priority con-
   Root-level metamorphic families are the main counterfac-        flicts, identity-derived support, sibling counter-rule confu-
tual substrate (Table 3). Each family anchors one canonical        sions). A short root-level case warmup transfers argument-
world and four variants with distinct diagnostic roles: sur-       certificate competence to the MR family distribution before
face_invariant (reorder facts/rules/priorities only; identi-       RL.
fiers unchanged), support_delta (edit a decisive support
fact), priority_delta (edit priority edges), and distrac-          3.2   GRPO and Three Rewards
tor_invariant (add irrelevant facts/rules for an unrelated
action). The canonical world itself is an unscored anchor;         For prompt x, GRPO samples a group of G completions and
supervised examples are the four canonical-to-variant pairs.       normalizes rewards within the group (Shao et al. 2024):
Family types target residual failures seen in earlier stages—                                    1
                                                                                                   P
                                                                                           ri − G     j rj
partial priority conflicts, unresolved conflicts, multiple com-                      Ai =                  .               (3)
patible overrides, missing-precondition distractors—rather                                 std({rj }) + ϵ
than arbitrary noise. Splits are by root family, so variants       We compare three rewards that instantiate three post-training
never leak across train/dev/ID/OOD. OOD uses held-out              philosophies. Answer-only reward is the natural import of
structural family types (e.g., priority chains and distractor-     math-style outcome supervision:
conflict variants), not merely new roots of the same type mix.
Critically, the relation label names the mechanism of change,       Rans = ωans Aans + ωschema Sans + ωtop Stop + Rlen . (4)
not a fixed answer direction: in some families both support
and priority edits resolve an unresolved conflict into permit-     It scores answer-change correctness plus minimal format
ted, while in others they remove a conclusion or introduce         shaping, and ignores relation, support, status, and attack
a new one. That is the point of the construction—to force          structure. Sparse reward instead demands exact compact-
models to explain why two worlds differ, not only whether          record generation:
their final labels differ.
                                                                   Rsparse = λall Aall + λfull Sfull + λtop Stop + λopt Or + Rlen ,
                                                                                                                               (5)
                 3    Post-Training Method                         where Aall is strict all-fields correctness. It is a strong ex-
We use LoRA adapters throughout (Hu et al. 2022). SFT es-          actness baseline, but provides little signal when a com-
tablishes structured-output competence; RL then compares           pletion is structurally close yet inexact. MR-GRPO re-
rewards on the compact change-record task under matched            places both with a class-conditioned metamorphic re-
data, optimizer, and group size. The experimental variable is      ward. Relations are grouped into invariant relations I =
      Setting        Init        Reward           Steps          reward geometry reappear when change fields are more ex-
      Sparse         sparse60    exact/schema     +60
                                                                 pressible? Which failures remain?
      Answer-only    sparse60    answer-change    +60               All metrics use deterministic parsers and scorers—never
      MR-GRPO        sparse60    class-cond. MR   +60            an LLM judge. We treat relation, relation-family, wrong-
                                                                 family, and exact answer/support/status change as primary
Table 4: Qwen3-1.7B matched continuation from a shared           structural readouts. Soft scores (change-presence, class-
sparse60 adapter. Qwen3-4B uses a shared aligned-SFT start       conditioned MR) reuse solver-visible fields and can align
(three seeds, 40 steps).                                         with the MR-GRPO reward; they are secondary diagnos-
                                                                 tics, not substitutes for exact family checks. Formally: rela-
                                                                 tion is four-way exact accuracy; relation-family is invariant-
{surface_invariant, distractor_invariant} and change             vs-change correctness; wrong-family crosses that boundary;
relations C = {support_delta, priority_delta}:                   all-changes exact requires the four change fields to match,
                                                                 excluding the relation label; change-presence checks answer
        RMR = Rrel + Rschema + g∆ Rsem + Rlen ,                  kind and nonempty slots without exact item identities; class-
          g∆ = γ0 + γ∆ S∆ ,                                      conditioned MR is Aclass . Predicting priority_delta for
                                                                 gold support_delta is wrong on subtype but right on fam-
         Rrel = αr Ar + αfam Afam                                ily; predicting an invariant label for that case is a wrong-
                + αopt Or − αwrong Wfam .                 (6)    family error. Unless noted, the SFT surface ablations and
                                                                 the Qwen3-1.7B GRPO continuation are single runs; the
Here Ar is exact relation correctness, Afam is invariant-vs-     Qwen3-4B GRPO study averages three independent seeds
change family correctness, and Wfam penalizes crossing that      (seeds, hardware, and per-seed tables in the supplementary
boundary. Semantic terms give exact and partial credit on        material). Exact 0/1 metrics use McNemar tests on the 1.7B
answer/support/status/attack fields and on a softer change-      held-out pairs; soft scores are secondary means. OOD asks
presence score that checks nonempty change slots without         whether in-distribution gains leave the training relation mix.
requiring exact item identities. The class-conditioned term is
the design centerpiece:
                                                                 4.1   SFT Diagnostics
             I
              ηfam Afam + ηsame Asame + ηE, r⋆ ∈ I,
                                           P
  Aclass =                                                       Table 5 shows the surface-variation ablation. Mixes are in-
                C
              ηfam Afam + ηchg Achg + ηprs Aprs , r⋆ ∈ C,        dependent from-base runs (896 records, 280 steps); the last
                                                           (7)   row keeps the full mix with targeted failure-family over-
so invariant gold labels reward unchanged answers and empty      sampling. Answer-only SFT saturates Answer (original- and
change fields, while change gold labels reward changed-          edited-world single-world answers) but scores zero on joint
answer structure and appropriate change presence. Soft           falsification. The prompts already name the falsification task
scores reuse these solver-visible fields; exact relation and     and schema, and models emit partially correct fields (Answer
relation-family accuracy remain the hard structural checks       wrong-rule 0.56; Answer+Proof counter-rule 0.42) while the
that a dense reward need not win. Coefficients are fixed         joint certificate stays empty—so the result shows limited
before held-out evaluation (full weights in the supplemen-       zero-shot transfer from answer/proof supervision to exact fal-
tary material); controls are protocol-matched rather than        sification certificates under the current interface, not only a
coefficient-count matched, because answer-only must remain       formatting failure (field breakdown in the supplementary ma-
an outcome-only control. The intended experimental differ-       terial). Answer+Proof saturates proofs yet still scores zero on
ence is therefore reward geometry, not optimizer, data, ini-     joint falsification. Adding falsification yields the first strong
tialization, or budget.                                          all-task jump; full mix + targeted replay reaches 0.99 overall.
   Table 4 summarizes the Qwen3-1.7B continuation: all           On root-level MR cases, a strong initializer still scores only
three branches continue from the same sparse-GRPO adapter        0.075 all-fields correct before a 600-step argument-certificate
for +60 steps on relation-balanced change records, so the        warmup raises this to 0.775, leaving relation-sensitive errors
comparison isolates reward switching after a shared sparse       for RL.
phase. The Qwen3-4B validation (Yang et al. 2025) asks the
same three-way reward question from a shared aligned-SFT         4.2   Matched Qwen3-1.7B Continuation
initializer—three seeds, a matched 40-step budget, and only
                                                                 On the 240-example held-out ID test (60 per relation), con-
the reward differing within each seed—providing a cleaner
                                                                 tinuing with MR-GRPO improves relation accuracy from
from-SFT check at larger scale (seeds and hardware in the
                                                                 0.2417 to 0.3375, relation-family correctness from 0.2917
supplementary material).
                                                                 to 0.3750, and wrong-family error from 0.5750 to 0.4333
                                                                 over continuing with sparse reward (Table 6; McNemar
                    4       Experiments                          p = 6.06 × 10−4 , 4.53 × 10−3 , 8.22 × 10−6 on held-out
The experiments answer four questions. Does final-answer         items). Gains concentrate on change-family labels: prior-
supervision suffice for solver-generated normative structure?    ity_delta rises from 39/60 to 48/60 and support_delta
After a shared sparse phase, how do answer-only, sparse,         from 18/60 to 33/60, while both invariant subtypes remain
and MR-aware continuations diverge on Qwen3-1.7B? From           near floor. Exact full change-record metrics also remain near
a shared aligned-SFT start on Qwen3-4B, does the same            floor; at this scale we read the continuation as evidence about
 Targets                      All↑   Answer↑    Proof↑   Fals↑           Metric                Sparse     Ans-only   MR-GRPO
 None (prompt only)           0.02       0.04     0.00   0.00            Relation↑              0.608        0.540       0.594
 Answer                       0.53       1.00     0.10   0.00            Answer change↑         0.610        0.743       0.747
 Answer+Proof                 0.75       0.99     1.00   0.00            Support change↑        0.562        0.597       0.621
 Answer+Proof+Fals.           0.97       0.98     0.97   0.95            Status change↑         0.571        0.565       0.600
 Full mix + targeted replay   0.99       1.00     0.98   0.99            All changes exact↑     0.431        0.435       0.443
                                                                         Relation-family↑       0.790        0.703       0.781
Table 5: Surface-variation SFT diagnostics (896 / 280 from               Wrong-family↓          0.210        0.297       0.219
base). Rows 2–4 ablate the target mix; the last adds targeted            Class-cond. MR↑        0.768        0.759       0.800
                                                                         Change-presence↑       0.813        0.829       0.843
failure-family oversampling. Answer = mean of original- and
edited-world single-world answer accuracy (same schema,
different input worlds); Proof/Fals: certificate exactness; All:    Table 7: Qwen3-4B three-seed mean on held-out test240.
mean of those two answer tasks plus proof and falsification.
                                                                               Branch         Zero-std↓    Class-MR probe↑
      Metric             Sparse      Ans-only   MR-GRPO                        Sparse            0.442               0.674
                                                                               Answer-only       0.317               0.693
      Relation↑           0.242         0.221       0.338                      MR-GRPO           0.108               0.698
      Answer change↑      0.050         0.050       0.038
      Relation-family↑    0.292         0.267       0.375
      Wrong-family↓       0.575         0.625       0.433          Table 8: Qwen3-4B training diagnostics (three-seed mean).
      Class-cond. MR↑     0.302         0.326       0.335          Zero-std: fraction of logged groups with zero reward std.;
                                                                   Class-MR probe: mean Aclass on training completions.
Table 6: Held-out ID Qwen3-1.7B three-way reward com-
parison.
                                                                   highest training-batch class-conditioned MR probe, match-
                                                                   ing the held-out pattern of denser structural credit without
                                                                   collapsing to the most visible answer field.
relation-family learning after a shared sparse phase, not as ex-
act field generation. Answer-only continuation is not stronger     How to read the three-way comparison The claim is a ge-
than sparse here: it ties on answer-change (0.05) and is worse     ometry, not a ranking. Answer-only chases the most visible
on relation-family behavior. Dev checks (dev32 and strati-         local field and shifts the relation prior toward change la-
fied40) match the held-out direction.                              bels. Sparse preserves coarse relation labels but often yields
                                                                   no within-group ranking signal for near-miss structure. MR-
4.3   Qwen3-4B Scale Validation                                    GRPO densifies credit along the invariant/change boundary
From a shared aligned-SFT start, the same geometry reap-           and solver-visible change fields. Sparse winning exact rela-
pears more cleanly (Table 7; three-seed means on the shared        tion/family and answer-only winning answer-local fields are
240-example held-out set). On primary exact metrics, sparse        expected signatures of those regimes, not contradictions.
GRPO preserves coarse relation and relation-family best
                                                                   4.4       Boundaries and Negative Results
(0.608 / 0.790). Answer-only GRPO improves answer-change
from 0.610 to 0.743 over sparse, and also lifts secondary          OOD remains open: on Qwen3-1.7B OOD240, relation ac-
change-presence—but relation-family drops from 0.790 to            curacy ties at 0.258; MR-GRPO reduces wrong-family er-
0.703 and wrong-family rises from 0.210 to 0.297. Er-              ror (0.667→0.571) without improving overall OOD relation
ror slices show the shortcut: answer-only reward shifts the        or class-conditioned MR. Exact full-record generation and
relation prior toward change labels (e.g., predicting sup-         invariant subtype recognition (surface_invariant vs. dis-
port_delta far more often), helping changed-answer cases           tractor_invariant) stay weak even when models detect
while converting invariant examples into the change family—        that nothing substantive changed. Invariant-heavy reweight-
the risk of importing outcome-only supervision into a judg-        ing and family-pooled advantage normalization do not close
ment task. MR-GRPO leads on exact answer-, support-, and           these gaps. The positive claim is therefore in-distribution
status-change fields and on the secondary soft scores, while       structural attribution under matched rewards, not transfer or
staying close to sparse on relation-family and far above           full-record mastery.
answer-only; relative to answer-only, it improves mean re-
lation and relation-family in every seed.                                5    Discussion: Insights and Implications
   Training diagnostics explain the mechanism (Table 8).           Scarcity inversion relative to math post-training In
Sparse exact reward leaves about 44% of logged GRPO                contest-style math, a rare correct final answer is often in-
groups with zero within-group reward standard deviation,           formative (Cobbe et al. 2021; Lightman et al. 2024; Shao
starving the ranking signal—a failure mode familiar from           et al. 2024). In normative judgment the label set is tiny, so
sparse outcome rewards, but here induced by exact nested           scarcity moves from which answer to which structure. That is
structure rather than by a rare boxed answer. Answer-only          why answer-only SFT can look solved and why answer-only
densifies that signal by rewarding answer-change alone. MR-        GRPO can “improve” by biasing toward change labels while
GRPO drops zero-std groups to about 11% while keeping the          dialectical checks remain empty.
Proof supervision does not transfer to falsification Proof          Process supervision, metamorphic tests, and counterfac-
exhibits the winner; falsification rejects a plausible loser. Our   tuals Intermediate and verifiable supervision improve be-
ladder shows limited automatic transfer under deterministic         yond final answers in mathematics and preference learning
scoring: answer-plus-proof can saturate proofs while joint          (Cobbe et al. 2021; Lightman et al. 2024; Christiano et al.
falsification stays at zero. Scoring only the winning path          2017; Ouyang et al. 2022; Shao et al. 2024; Guo et al. 2025).
misses certificate-review errors—citing a defeated rule, ig-        Rubric-structured rewards provide multi-criterion partial
noring unresolved conflict, or accepting an invalid certificate.    credit when binary oracles are scarce, usually scored by an
                                                                    LLM judge (Gunjal et al. 2025); our rewards instead score
Interventions, partial credit, and attribution Root-level           solver-visible change fields without a judge. Metamorphic
MR pairs are interventions, not generic augmentations: sur-         testing and counterfactual/contrast sets expose local deci-
face/distractor edits should leave certificates fixed, while sup-   sion failures when oracles are hard (Chen, Cheung, and Yiu
port/priority edits should change them in solver-specified          1998; Chen et al. 2018; Kaushik, Hovy, and Lipton 2020;
ways. Compact change records are a practical RL inter-              Gardner et al. 2020); unlike generic augmentation aimed
face for naming the mechanism of change. Confusing sup-             only at invariance, our priority and support edits are sup-
port_delta with priority_delta is wrong on subtype yet              posed to change answers and certificates in precise ways,
right on the invariant/change boundary; class-conditioned           and those relations become RL targets. Persistent strict seri-
partial credit follows that diagnostic hierarchy, whereas           alization failures also motivate future constrained decoding
sparse exactness ignores it and often starves GRPO. Refusing        (sch 2021).
LLM judges keeps reward design an experimental variable,
and typed failures make competence-level attribution possi-                              7   Conclusion
ble. NormWorlds-CF complements LegalBench-style eval-
uation by asking whether verified structure can be taught           NormWorlds-CF makes counterfactual normative structure
under auditable oracles before asking how much transfers to         auditable: answers, certificates, and paired-world change la-
open legal text.                                                    bels are solver-generated rather than LLM-judged. SFT di-
                                                                    agnostics show that final-answer supervision—often a rea-
                                                                    sonable default in answer-sparse math—can saturate ver-
                    6    Related Work                               dicts without inducing falsification competence. On com-
We situate NormWorlds-CF in three nearby literatures be-            pact change records, matched answer-only, sparse, and MR-
low. For a short primer, Prakken and Sartor (2015) surveys          aware GRPO induce a clear geometry under a 1.7B contin-
defeasible legal argumentation, Tafjord, Dalvi, and Clark           uation protocol and a 4B from-SFT protocol: sparse leads
(2021) exemplifies proof-oriented synthetic reasoning, and          on coarse relation labels, answer-only trades family struc-
Shao et al. (2024) introduces the GRPO-style group updates          ture for answer-local gains, and MR-GRPO leads on an-
used in our RL stage (LoRA adapters follow (Hu et al. 2022)).       swer/support/status fields and secondary soft scores. Ex-
                                                                    act full-record generation, invariant subtype recognition, and
Synthetic and solver-verified reasoning Controlled                  OOD transfer remain open. The broader lesson is that out-
benchmarks isolate compositionality and rule following (We-         come supervision cannot identify normative structure qual-
ston et al. 2015; Johnson et al. 2017; Clark, Tafjord, and          ity, so post-training should use verified structure at three
Richardson 2020; Tafjord, Dalvi, and Clark 2021). Sanyal,           levels: supervision targets, counterfactual tasks, and reward
Liao, and Ren (2022) further test whether deductive models          design.
stay consistent under minimal logical edits to operators and
theories. NormWorlds-CF is complementary: rather than en-
tailment labels over fixed theories alone, it exposes proof, fal-
sification, and paired-world change under executable priori-
ties, with solver-checked certificates rather than LLM-judged
text.
Normative and legal evaluation Deontic and defeasible
logics emphasize why a conclusion follows under rules,
exceptions, and priorities (von Wright 1951; Nute 1994;
Prakken and Sartor 2015). Recent LLM evaluations probe
defeasible property inheritance at scale (Allaway and McK-
eown 2025), normative versus epistemic modal reasoning
patterns (Ozeki et al. 2025), and diagnostic legal tasks
with machine-computable statute encodings (Servantez et al.
2026). Legal evaluation suites and legal-domain LLMs
measure external validity on realistic texts and workflows
(Chalkidis et al. 2022; Guha et al. 2023; Fei et al. 2024;
Colombo et al. 2024). We ask a complementary post-training
question: can reward design teach verified normative struc-
ture under controlled transformations?
                       References                               Guha, N.; Nyarko, J.; Ho, D. E.; Ré, C.; Chilton, A.;
2021. PICARD: Parsing Incrementally for Constrained Auto-       Narayana, A.; Chohlas-Wood, A.; Peters, A.; Waldon, B.;
Regressive Decoding from Language Models. In Proceed-           Rockmore, D. N.; Zambrano, D.; et al. 2023. LegalBench: A
ings of the 2021 Conference on Empirical Methods in Natural     Collaboratively Built Benchmark for Measuring Legal Rea-
Language Processing, 9895–9901. Association for Compu-          soning in Large Language Models. In Advances in Neural
tational Linguistics.                                           Information Processing Systems, volume 36, 44123–44279.
Allaway, E.; and McKeown, K. 2025. Evaluating Defeasible        Gunjal, A.; Wang, A.; Lau, E.; Nath, V.; He, Y.; Liu, B.;
Reasoning in LLMs with DEFREASING. In Proceedings of            and Hendryx, S. 2025. Rubrics as Rewards: Reinforce-
the 2025 Conference of the Nations of the Americas Chapter      ment Learning Beyond Verifiable Domains. arXiv preprint
of the Association for Computational Linguistics: Human         arXiv:2507.17746.
Language Technologies (Volume 1: Long Papers), 10540–           Guo, D.; Yang, D.; Zhang, H.; Song, J.; Wang, P.; Zhu, Q.;
10558. Association for Computational Linguistics.               Xu, R.; Zhang, R.; Ma, S.; Bi, X.; et al. 2025. DeepSeek-
Chalkidis, I.; Jana, A.; Hartung, D.; Bommarito, M.; An-        R1 Incentivizes Reasoning in LLMs through Reinforcement
droutsopoulos, I.; Katz, D.; and Aletras, N. 2022. LexGLUE:     Learning. Nature, 645: 633–638.
A Benchmark Dataset for Legal Language Understanding            Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.;
in English. In Proceedings of the 60th Annual Meeting of        Wang, L.; and Chen, W. 2022. LoRA: Low-Rank Adaptation
the Association for Computational Linguistics (Volume 1:        of Large Language Models. In International Conference on
Long Papers), 4310–4330. Association for Computational          Learning Representations.
Linguistics.                                                    Johnson, J.; Hariharan, B.; van der Maaten, L.; Li, F.-F.;
Chen, T. Y.; Cheung, S.-C.; and Yiu, S.-M. 1998. Meta-          Zitnick, C. L.; and Girshick, R. 2017. CLEVR: A Diagnostic
morphic Testing: A New Approach for Generating Next Test        Dataset for Compositional Language and Elementary Visual
Cases. Technical Report HKUST-CS98-01, Department of            Reasoning. In 2017 IEEE Conference on Computer Vision
Computer Science, The Hong Kong University of Science           and Pattern Recognition (CVPR), 1988–1997.
and Technology.                                                 Kaushik, D.; Hovy, E.; and Lipton, Z. 2020. Learning The
Chen, T. Y.; Kuo, F.-C.; Liu, H.; Poon, P.-L.; Towey, D.;       Difference That Makes A Difference With Counterfactually-
Tse, T. H.; and Zhou, Z. Q. 2018. Metamorphic Testing: A        Augmented Data. In International Conference on Learning
Review of Challenges and Opportunities. ACM Computing           Representations.
Surveys, 51(1): 4:1–4:27.                                       Lightman, H.; Kosaraju, V.; Burda, Y.; Edwards, H.; Baker,
Christiano, P. F.; Leike, J.; Brown, T.; Martic, M.; Legg,      B.; Lee, T.; Leike, J.; Schulman, J.; Sutskever, I.; and Cobbe,
S.; and Amodei, D. 2017. Deep Reinforcement Learning            K. 2024. Let’s Verify Step by Step. In International Confer-
from Human Preferences. In Advances in Neural Information       ence on Learning Representations, 39578–39601.
Processing Systems, volume 30.                                  Nute, D. 1994. Defeasible Logic. In Gabbay, D. M.; Hogger,
Clark, P.; Tafjord, O.; and Richardson, K. 2020. Transformers   C. J.; Robinson, J. A.; and Nute, D., eds., Handbook of Logic
as Soft Reasoners over Language. In Proceedings of the          in Artificial Intelligence and Logic Programming, Volume 3:
Twenty-Ninth International Joint Conference on Artificial       Nonmonotonic Reasoning and Uncertain Reasoning, 353–
Intelligence, IJCAI-20, 3882–3890.                              395. Oxford University Press.
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;       Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright, C.;
Kaiser, L.; Plappert, M.; Tworek, J.; Hilton, J.; Nakano, R.;   Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray, A.;
Hesse, C.; and Schulman, J. 2021. Training Verifiers to Solve   Schulman, J.; Hilton, J.; Kelton, F.; Miller, L.; Simens, M.;
Math Word Problems. arXiv preprint arXiv:2110.14168.            Askell, A.; Welinder, P.; Christiano, P. F.; Leike, J.; and Lowe,
Colombo, P.; Pires, T. P.; Boudiaf, M.; Culver, D.; Melo, R.;   R. 2022. Training Language Models to Follow Instructions
Corro, C.; Martins, A. F. T.; Esposito, F.; Raposo, V. L.;      with Human Feedback. In Advances in Neural Information
Morgado, S.; and Desa, M. 2024. SaulLM-7B: A pio-               Processing Systems, volume 35, 27730–27744.
neering Large Language Model for Law. arXiv preprint            Ozeki, K.; Ando, R.; Morishita, T.; Abe, H.; Mineshima, K.;
arXiv:2403.03883.                                               and Okada, M. 2025. Normative Reasoning in Large Lan-
Fei, Z.; Shen, X.; Zhu, D.; Zhou, F.; Han, Z.; Huang, A.;       guage Models: A Comparative Benchmark from Logical and
Zhang, S.; Chen, K.; Yin, Z.; Shen, Z.; Ge, J.; and Ng, V.      Modal Perspectives. In Proceedings of the 8th BlackboxNLP
2024. LawBench: Benchmarking Legal Knowledge of Large           Workshop: Analyzing and Interpreting Neural Networks for
Language Models. In Proceedings of the 2024 Conference on       NLP, 276–294. Association for Computational Linguistics.
Empirical Methods in Natural Language Processing, 7933–         Prakken, H.; and Sartor, G. 2015. Law and Logic: A Review
7962. Association for Computational Linguistics.                from an Argumentation Perspective. Artificial Intelligence,
Gardner, M.; Artzi, Y.; Basmov, V.; Berant, J.; Bogin, B.;      227: 214–245.
Chen, S.; Dasigi, P.; Dua, D.; Elazar, Y.; Gottumukkala, A.;    Sanyal, S.; Liao, Z.; and Ren, X. 2022. RobustLR: A Di-
et al. 2020. Evaluating Models’ Local Decision Boundaries       agnostic Benchmark for Evaluating Logical Robustness of
via Contrast Sets. In Findings of the Association for Compu-    Deductive Reasoners. In Proceedings of the 2022 Confer-
tational Linguistics: EMNLP 2020, 1307–1323. Association        ence on Empirical Methods in Natural Language Processing,
for Computational Linguistics.                                  9614–9631. Association for Computational Linguistics.
Servantez, S.; Lawsky, S. B.; Jain, R.; Linna, D. W., Jr.; and
Hammond, K. J. 2026. OpenExempt: A Diagnostic Bench-
mark for Legal Reasoning and a Framework for Creating
Custom Benchmarks on Demand. In Findings of the Asso-
ciation for Computational Linguistics: ACL 2026, 26644–
26669. Association for Computational Linguistics.
Shao, Z.; Wang, P.; Zhu, Q.; Xu, R.; Song, J.; Bi, X.;
Zhang, H.; Zhang, M.; Li, Y. K.; Wu, Y.; and Guo, D.
2024. DeepSeekMath: Pushing the Limits of Mathemati-
cal Reasoning in Open Language Models. arXiv preprint
arXiv:2402.03300.
Tafjord, O.; Dalvi, B.; and Clark, P. 2021. ProofWriter:
Generating Implications, Proofs, and Abductive Statements
over Natural Language. In Findings of the Association for
Computational Linguistics: ACL-IJCNLP 2021, 3621–3634.
Association for Computational Linguistics.
von Wright, G. H. 1951. Deontic Logic. Mind, 60(237):
1–15.
Weston, J.; Bordes, A.; Chopra, S.; Rush, A. M.; van Mer-
riënboer, B.; Joulin, A.; and Mikolov, T. 2015. Towards AI-
Complete Question Answering: A Set of Prerequisite Toy
Tasks. arXiv preprint arXiv:1502.05698.
Yang, A.; Li, A.; Yang, B.; Zhang, B.; Hui, B.; Zheng, B.; Yu,
B.; Gao, C.; Huang, C.; Lv, C.; et al. 2025. Qwen3 Technical
Report. arXiv preprint arXiv:2505.09388.
