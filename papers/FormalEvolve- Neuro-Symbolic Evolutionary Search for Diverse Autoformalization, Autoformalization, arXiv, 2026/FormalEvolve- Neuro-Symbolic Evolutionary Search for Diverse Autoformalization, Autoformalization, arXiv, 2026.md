                                                FormalEvolve: Neuro-Symbolic Evolutionary Search for Diverse
                                                                    Autoformalization

                                                                    Haijian Lu1,2 Wei Wang2 * Jing Liu1
                                                          1
                                                          School of Artificial Intelligence, Xidian University, Xi’an, China
                                                 2
                                                   State Key Laboratory of General Artificial Intelligence, BIGAI, Beijing, China



                                                              Abstract                              From one candidate to diverse repertoire
                                                                                                                                                               ✦
                                             Autoformalization aims to produce formal                               A Single candidate
arXiv:2603.19828v4 [cs.AI] 2 Sep 2026




                                                                                                                                                                                                                          ×
                                                                                                                                                                        Fixed budget: 64 prover attempts
                                             statements that compile and faithfully preserve                         Formal statement    compile     semantic


                                                                                                                                                                        ×   ×    ×   ×   ×   ×   ×   ×         ...
                                                                                                                    Formal statement A      ✓           ✓
                                             the intended meaning of informal mathemat-                                                                                         0 / 64 solved
                                                                                                                                                                                                                     Only one Output
                                                                                                                                                                                                                          Fail !



                                             ics. Yet standard single-output evaluation                                                               Same prover, same budget,
                                                                                                                                                   different proof-search behavior.

                                             collapses this many-to-many structure into a        Informal
                                                                                                                    B Diverse repertoire
                                                                                                 Problem
                                             single prediction. For downstream proving,                              Formal statement    compile    semantic        ×   ×   ×    ×   ×   ×   ×   ×       ...
                                                                                                                                           ✓           ✓
                                                                                                 Natural-language



                                                                                                                                                                                                                          ✓
                                                                                                                                                                            × ✓ ✓ ✓ ×
                                                                                                                    Formal statement A
                                                                                                                                                                    ×   ×                        ×       ...
                                             this granularity is too coarse: a formal state-                        Formal statement B     ✓           ✓
                                                                                                                                                                    ✓   ✓   ✓   ✓    ✓   ✓   ✓   ✓       ...
                                                                                                                    Formal statement C     ✓           ✓
                                             ment is not merely a faithful translation end-                         Formal statement D     ✓           ✓            ✓   ✓   ✓   ✓    ✓   ×   ×   ×       ...          Higher chance
                                                                                                                                                                                                                        of provable
                                                                                                                                                                                                                       formulation
                                                                                                                    Formal statement E     ✓           ✓            ×   ×   ×    ×   × ✓ ✓ ×             ...
                                             point, but also a prover-facing interface whose                                                                                    32 / 64 solved

                                             structure can alter proof search under a fixed                         A semantically faithful repertoire hedges against prover sensitivity
                                                                                                                                        under a fixed proof budget.
                                             budget. We therefore recast autoformaliza-
                                             tion as budgeted test-time search: FormalE-
                                             volve maintains a compilation-feasible archive    Figure 1: Motivating illustration under a fixed prover
                                             for reuse and returns a deduplicated, seman-      and attempt budget (B=64). Even when candidate state-
                                             tically accepted repertoire for evaluation and    ments compile and are judged semantically consistent,
                                             downstream proving. It expands the archive        prover outcomes can vary substantially. Constructing
                                             with LLM-driven mutation, crossover, bounded      a diverse repertoire hedges against this sensitivity and
                                             patch repair, and symbolic abstract syntax tree   increases the chance that at least one provable statement
                                             (AST) rewrites for structural diversity. Under    is found within budget.
                                             a generator-call budget of T =100 with a fixed
                                             LLM semantic judge, FormalEvolve reaches          while semantic faithfulness remains a separate re-
                                             SH@100 of 58.0% on CombiBench and 84.9%           quirement. As large language model provers be-
                                             on ProofNet, improving over all no-archive con-   come more capable (Polu and Sutskever, 2020; Han
                                             trols while reducing the cross-problem concen-
                                             tration of semantic successes. Under a fixed
                                                                                               et al., 2022; Song et al., 2024), structural choices in
                                             B=64 prover budget, these repertoires improve     the statement itself increasingly affect downstream
                                             theorem-complete proving over the matched         proof search.
                                             no-archive control. Additional stronger-base         Autoformalization is naturally many-to-many:
                                             statement-generation experiments show that        the same theorem can often be encoded as multi-
                                             archive-search gains persist with stronger seed   ple faithful Lean statements. Semantic consistency
                                             and repair models.                                therefore does not imply prover equivalence: by
                                                                                               prover equivalence we informally mean compara-
                                        1    Introduction
                                                                                               ble proof-search behavior under the same prover
                                        Autoformalization translates informal mathemat-        and attempt budget. A formal statement that com-
                                        ics into Lean statements that compile and pre-         piles and preserves the intended claim is not nec-
                                        serve the intended mathematical claim. For down-       essarily a prover-friendly target; faithful variants
                                        stream proving, however, the formal statement is       can differ substantially in proof-search cost and
                                        not merely a translation endpoint: it is the prover-   success rate. Figure 1 illustrates this gap: candi-
                                        facing interface through which proof search is at-     dates that pass compilation and semantic checks
                                        tempted. Compilation requires successful elabora-      can still lead to different prover outcomes under the
                                        tion and type checking under the chosen context,       same prover protocol. A single generated statement
                                            * Corresponding author: wangwei@nlpr.ia.ac.cn.     therefore discards prover-relevant variation. This
Figure 2: Framework overview of FormalEvolve. A seed model produces an initial seedbank (debited as generator
calls) that initializes a compilation-feasible archive. Candidates are stored with semantic scores and selected with
usage penalties; a patch model proposes edits (full rewrite, diff patching, and cross patching) and triggers bounded
repair or EvolAST fallbacks on duplicate proposals and compilation failures. Semantic scoring filters the archive
into a diverse repertoire for downstream proving and evaluation.

motivates a repertoire view: the search procedure           biBench and 84.9% on ProofNet, improving over
should construct multiple faithful Lean statements          all no-archive controls on both benchmarks while
that expose different proof-search behavior under           reducing the cross-problem concentration of seman-
the same prover budget.                                     tic successes. Under a fixed B=64 prover budget,
   We formulate autoformalization as a budgeted             the resulting repertoires improve theorem-complete
test-time search problem. Under a generator-call            downstream proving over the matched no-archive
budget, the system must construct a repertoire of           control on both benchmarks. To separate repair-
candidate formalizations that are compilable, se-           model strength from archive search, we include a
mantically consistent, and useful for downstream            matched Hybrid control that uses the same stronger
proving. This requires preserving compilation fea-          repair model without an archive; FormalEvolve
sibility and semantic fidelity while distributing           still gains at the statement stage. The pattern also
search across distinct trajectories and avoiding near-      holds in a stronger-base statement-generation set-
duplicate candidates.                                       ting. Because semantic labels come from an LLM
   To address these requirements, we propose For-           judge, we also provide manual audits at both the
malEvolve, a compilation-gated neuro-symbolic               statement and theorem-complete stages to calibrate
evolutionary framework built around an archive              the evaluation.
search protocol.       FormalEvolve maintains a                More broadly, FormalEvolve illustrates a
compilation-feasible archive of candidate Lean              verifier-gated diversity-search pattern: when many
statements and expands it primarily through LLM-            valid formal artifacts can express the same informal
driven mutation, crossover, and bounded patch re-           intent, test-time compute can construct a repertoire
pair. In addition, conservative generator-call-free         of useful alternatives under hard checker feedback.
AST rewrites act as a structural diversification fall-         We make three primary contributions:
back when patching stalls, for example after re-
peated duplicates or compile failures. Usage penal-           1. Problem Modeling and Protocol: We formu-
ties and duplicate-aware selection encourage the                 late Lean 4 autoformalization as budgeted test-
search to cover more problems and statement forms.               time repertoire search and introduce budget-
Figure 2 gives a high-level overview.                            auditable metrics that connect statement-level
   Under a generator-call budget of T =100, For-                 coverage, cross-problem concentration, and
malEvolve reaches SH@100 of 58.0% on Com-                        downstream proving performance.
    2. Search Mechanism: We propose FormalE-             Test-time search and quality-diversity. Test-
       volve, a compilation-gated neuro-symbolic         time search and evolutionary optimization with
       evolutionary framework that combines              LLMs have been explored for sample-efficient
       archive-based LLM mutation and crossover,         program and algorithm improvement (Novikov
       bounded patch repair, and generator-call-free     et al., 2025; Lange et al., 2025; Liu et al.,
       symbolic AST rewrites.                            2024). Quality-diversity methods construct reper-
                                                         toires of high-quality solutions (Lehman and Stan-
    3. Empirical Evidence: We show that FormalE-         ley, 2011; Mouret and Clune, 2015), and multi-
       volve improves semantic hit rates and cross-      criteria evolutionary optimization provides a com-
       problem coverage uniformity under fixed           plementary perspective on multiple objectives
       generator-call budgets, improves theorem-         (Deb et al., 2002). EvolProver synthesizes of-
       complete downstream proving over a matched        fline prover-training data through symmetry, diffi-
       no-archive control by constructing diverse        culty, and semantics-preserving AST rewrites (Tian
       candidate repertoires, and preserves statement-   et al., 2025). FormalEvolve performs online, per-
       stage archive-search gains under a stronger-      problem test-time search and adapts conservative
       base setting.                                     AST rewrites as a targeted diversification fallback.
                                                         For Lean statement search, elaboration and type
2     Related Work
                                                         checking define the feasible set: a candidate must
Autoformalization and semantic evaluation.               compile before it can enter the archive or be reused
Large language models have enabled autoformal-           as a parent. For each informal problem, FormalE-
ization at scale, with systematic evaluation on cu-      volve builds a test-time repertoire of candidate
rated formal-mathematics benchmarks (Wu et al.,          statements used for that problem’s evaluation and
2022; Azerbayev et al., 2023; Zheng et al., 2022).       downstream proving.
Reliability remains a central bottleneck: compila-
tion checks syntax and elaboration, but is only a        3   Method
weak proxy for semantic consistency, motivating          FormalEvolve instantiates the shift from single-
dedicated semantic judges and alignment evalua-          output prediction to many-to-many repertoire con-
tors (Peng et al., 2025; Lu et al., 2024). Recent        struction as per-problem test-time search over
systems further improve semantic fidelity by in-         Lean 4 statement candidates under a generator-call
terleaving iteration, tool feedback, and grounding       budget T (Section 4). Given an informal state-
(Chen et al., 2025; Guo et al., 2025; Wang et al.,       ment x, the goal is to construct a deduplicated
2025b). These lines of work primarily improve            repertoire of candidates that compile and pass the
or assess individual formalizations within a single-     semantic judge within budget. The search starts
output view. We study fixed-budget construction          from a small compilation-feasible seedbank, stores
of semantically consistent and diverse candidate         unique compiled candidates in an archive, and ex-
repertoires.                                             pands it through LLM patching, bounded repair,
Statement variation and prover utility. For              and call-free EvolAST diversification. Because
downstream proving, a formal statement serves            Lean compilation defines a narrow feasible region,
both as a semantic target and as the object con-         archive entry is compilation-gated, near-feasible
sumed by a prover. Even among semantically con-          candidates are salvaged by bounded repair, and
sistent candidates, minor reformulations intended        lightweight diversity operators discourage repeated
to preserve semantics can substantially change           near-duplicate trajectories. Our reported output is
proof-search difficulty (Zhao et al., 2025). At the      the deduplicated semantically consistent repertoire
same time, semantic evaluation itself remains im-        generated within budget, i.e., candidates satisfy-
perfect (Chen et al., 2025). These observations mo-      ing Comp(c)=1 and Sem(c)=1, which we use for
tivate treating autoformalization as a fixed-budget      SH@T and downstream proving.
repertoire-construction problem, where multiple             Algorithm 1 summarizes the same loop and
faithful candidates expose different prover utilities.   makes the two domain gates explicit: Comp
Such a repertoire mitigates prover sensitivity by        checks whether a candidate passes Lean 4 com-
exposing several semantically aligned targets under      pilation, while Sem is the semantic-faithfulness
the same fixed budget.                                   judge against the informal theorem x. The counter
t tracks debited generator calls, AI is an island       Algorithm 1 FormalEvolve for Lean statement
archive, Z denotes sampled prompt context and           search
inspirations, B is the candidate batch produced by        Task: given informal theorem x, search Lean 4 statement
                                                          candidates c
proposal and bounded repair, and G is the persistent      Gates: Comp(c) checks whether c passes Lean 4 compila-
accepted repertoire returned at the end. Figure 2         tion; Sem(c) checks faithfulness to x
gives the visual overview, and Section E.1 gives          Input: budget T , models Mseed , Mpatch , islands K
                                                          Output: accepted repertoire G
the detailed pseudocode.                                  t ← 0; A ← empty K-island archive; G ← ∅
                                                          (A, t) ← S EEDA RCHIVE(x, Mseed , T, K)          (Seedbank
3.1   Search Procedure and State                          initialization)
                                                                       S
                                                          G ← {c ∈ I AIS: Comp(c) ∧ Sem(c)}
Basic objects and gates. We search over Lean 4            while t < T and I AI ̸= ∅ do
candidates of the form c = (ĥ, y), where ĥ is an           I ← S AMPLE I SLAND(A)            (Archive, islands, and
import/header context and y is the primary Lean 4            duplicates)
                                                             p ← S AMPLE PARENT(AI ); np ← np + 1 (Scoring;
statement or declaration target. Most candidates             Eq. 2)
are theorem/lemma-style files with placeholder               Z ← S AMPLE C ONTEXT(AI , p)
proofs, but benchmark contexts and model out-                c ← P ROPOSE(p, Z, x; Mpatch ); t ← t + 1 (Variation
                                                             operators)
puts can also contain def, abbrev, or example                (B, t) ← E XPANDA ND R EPAIR(c, p, x, t, T ) (Bounded
templates; for this reason, the prover-stage eval-           repair + EvolAST fallback)
                                                             AI ← E VALUATE A ND U PDATE(AI , B)
uation separately reports theorem-complete suc-              G ← G ∪ {b ∈ B : Comp(b) ∧ Sem(b)}
cess for explicit theorem/lemma completions. We           end while
evaluate candidates using a compilation predi-            return Dedup(G)
cate Comp(c) ∈ {0, 1} and a semantic predicate
Sem(c) ∈ {0, 1} (instantiated by an LLM judge           seed and patch roles: Mseed provides initial can-
in Section 4). Compilation is a hard feasibility        didates, while Mpatch performs edit-conditioned
gate: only candidates with Comp(c) = 1 are el-          proposals and bounded repairs. Concrete model
igible to enter the archive and be reused as par-       choices are specified in Section 4.
ents/inspirations. We treat compilation/elaboration
                                                        Archive, islands, and duplicates. We maintain
as verifier feedback: it both defines feasibility and
                                                        a per-problem archive A of unique compilation-
provides the primary error feedback for bounded
                                                        feasible candidates that serves both as a parent pool
compilation repair. During search, the archive
                                                        and as prompt context. We use an island model
stores unique compilation-feasible candidates re-
                                                        with K semi-isolated archive populations (default
gardless of Sem(c) (i.e., it may include semanti-
                                                        K = 2). When K = 1, FormalEvolve uses a
cally inconsistent stepping stones) and is used only
                                                        single archive population: it still retains archive-
for parent/context sampling. For reporting SH@T
                                                        based parent reuse, archive-conditioned context
and downstream proving, we define the semanti-
                                                        sampling, usage-penalized selection, and bounded
cally consistent repertoire as the deduplicated set
                                                        repair, but removes island partitioning and migra-
of candidates generated within budget that satisfy
                                                        tion. Each iteration samples one island and restricts
both Comp(c) = 1 and Sem(c) = 1. FormalE-
                                                        parent/context sampling to it. In the main config-
volve uses these two predicates during test-time
                                                        uration, migration occurs every 10 generations at
search and bounded repairs; downstream proving
                                                        rate 0.1 with the top candidate in each island pro-
is evaluated only when reporting proof utility. All
                                                        tected. Detailed hyperparameters are provided in
generator-side LLM calls (seeds, patches, and re-
                                                        Section E.3. Exact duplicates under canonicaliza-
pairs) are debited against the same per-problem
                                                        tion (whitespace/name normalization) are rejected
generator-call budget T (Section 4).
                                                        at archive insertion to reduce collapse. In Algo-
Seedbank initialization. We initialize the search       rithm 1, S AMPLE PARENT uses the scoring rule de-
by sampling a small seedbank with a seed model          fined below, and ni tracks how often ci has already
Mseed , evaluating each seed with the compiler          been selected as a parent.
and semantic judge, and inserting the compilation-
                                                        Scoring and usage-penalized selection. The se-
feasible subset into the archive. When a pre-
                                                        lection rule separates archive storage from parent
sampled seedbank is reused across methods, we
                                                        sampling. Storage is purely feasibility-gated: only
still debit each reused seed as one generator call
                                                        candidates with Comp(c) = 1 can enter the archive,
to preserve consistent accounting. We separate the
                                                        and the archive retains all unique compilation-
feasible candidates. This matters because differ-       Bounded compilation and semantic repair. We
ent faithful statements can expose different binder     compile the full Lean 4 file and treat successful
structures, imports, and theorem shapes to the          compilation as a hard feasibility gate. When compi-
downstream prover. Scores therefore bias reuse          lation fails, FormalEvolve invokes a repair prompt
as future parents; archive contents remain available    that proposes a minimal patch conditioned on com-
for later sampling, and proof utility is evaluated      piler feedback. Repair is bounded to a fixed cap of
downstream under the fixed prover protocol.             two repair attempts per proposal path in the main
   For an archived candidate ci ∈ AI , let ni be how    configuration; each attempt is debited as a gener-
many times it has already been selected as a parent.    ator call, and repair stops immediately when the
We assign each candidate a sampling weight wi           remaining budget is exhausted. Bounding repair
and sample proportionally:                              makes the search budget-auditable under hard cut-
                                    wi                  offs and prevents pathological cases where a single
          Pr(p = ci | AI ) = P             .      (1)   hard candidate consumes most of the call budget.
                                 cj ∈AI wj
                                                        For a compilable candidate that fails the semantic
The weight combines the gate score and a usage          judge (Comp(c) = 1 and Sem(c) = 0), we option-
discount:                                               ally invoke bounded semantic repair. Mpatch re-
      si = Comp(ci )(1 + Sem(ci )),                     vises the statement using the informal input and the
                                                        judge’s rationale (when available), after which the
      s̃I = mediancj ∈AI (sj ),
                                                        result is re-evaluated; every repair and semantic-
      dI = max(MAD({sj : cj ∈ AI }), ε),                repair attempt is debited. We view compilation
                                                 (2)
      zi = (si − s̃I )/dI ,                             repair and semantic repair as two instantiations of
      ui = [1 + (1 + β)ni ]−1 ,                         the same edit-conditioned patch mechanism, differ-
                                                        ing only in the feedback source (compiler errors vs.
      wi = σ(λzi )ui .
                                                        judge rationale).
Since archived candidates already compile, si = 1
                                                        Call-free diversity fallback (EvolAST).
for judge-negative archive members and si = 2 for
                                                        Archive-based search can suffer mode collapse,
judge-consistent members. ui is a usage discount:
                                                        with many candidates becoming near-duplicates
it equals 1 for a never-used parent and decreases
                                                        or exploiting superficial patterns. FormalEvolve
as the same parent is sampled repeatedly. We set
                                                        mitigates this primarily via the usage penalty
ε = 10−6 only to avoid division by zero when all
                                                        in parent sampling. We additionally apply a
scores are identical, and use λ = 10 and β = 0.05
                                                        conservative, generator-call-free AST rewrite
in the main runs.
                                                        fallback inspired by EvolProver (Tian et al., 2025)
3.2   Proposal, Repair, and Diversification             when patching stalls (e.g., repeated duplicates
                                                        or compile failures). In the reported runs, each
Variation operators. Given a selected parent,
                                                        triggering proposal contributes at most one
the patch model proposes a new candidate us-
                                                        EvolAST representative, and EvolAST outputs are
ing one of three prompt templates. Full patching
                                                        not recursively rewritten or sent into LLM repair.
rewrites the entire statement (and, when allowed,
                                                        EvolAST rewrites only within binder types and
its surrounding imports) conditioned on the infor-
                                                        the goal type (imports/preamble unchanged) to
mal input and parent context. Diff patching per-
                                                        produce symmetry/structure variants, which are
forms localized edits that make minimal changes
                                                        then filtered by the same compilation gate and
relative to the parent, guided by compiler/judge
                                                        semantic judge. EvolAST consumes no generator
feedback. Cross patching additionally conditions
                                                        calls; Section E.2 reports its compilation and judge
on one or more inspiration candidates sampled
                                                        overhead.
from the current archive. The model combines use-
ful elements (e.g., import context, binder structure,   4   Experiments
or type annotations) while preserving the informal
input’s meaning (see Section F for prompt details       Benchmarks. We evaluate on ProofNet (Azer-
and Section D for audited examples). All three tem-     bayev et al., 2023) (Lean 4 port; test split, N =186)
plates return a complete Lean 4 file (imports plus      and CombiBench (Liu et al., 2025) (N =100, do-
a single statement) and are budgeted identically as     main/style shift). The two benchmarks provide con-
generator calls.                                        trasting search regimes. ProofNet consists primar-
ily of standard undergraduate mathematics, and the      Metrics. CH@T and SH@T denote the fraction
public autoformalization SFT mixture used to ini-       of problems with at least one compilable candidate
tialize Kimina-Autoformalizer includes ProofNet         and at least one compilable, judge-consistent candi-
(Wang et al., 2025a), making it a high-prior set-       date, respectively, within T debited generator calls.
ting for the Kimina-based generation component.         Coverage alone leaves open whether additional se-
CombiBench instead focuses on specialized com-          mantic successes are broadly distributed or con-
binatorics and presents a substantially stronger do-    centrated on a small set of already-easy problems.
main/style shift, providing a lower-prior setting in    Let sj (T ) be the number of generated candidates
which exploration is more important.                    with Comp(c) = 1 and Sem(c) = 1 for problem j
                                                        within budget T ; we therefore report cross-problem
Environment. Candidates are compiled under a
                                                        concentration via the Gini coefficient
pinned Lean 4/Mathlib toolchain served by Kimina
                                                                        PN PN
Lean Server (Dos Santos et al., 2025); full details                        i=1   j=1 |si (T ) − sj (T )|
are in Section E.3.                                        Gini(T ) =           PN                       , (3)
                                                                             2N j=1 sj (T ) + ε
Budget. We use T = 100 generator calls per
problem. Each seed, proposal, compilation-repair,       with the same numerical stabilizer ε = 10−6 used
and semantic-repair LLM call debits one call. We        in parent-score normalization. We alsoPreport the
                                                                           P                    N
additionally record compilation checks, semantic-       Top-10% share                s
                                                                            j∈Top10% j  (T )/      s
                                                                                                j=1 j (T )
judge calls, and EvolAST-triggered candidate eval-      (where Top10% selects the problems with the
uations; Appendix E.2 reports this accounting, in-      largest sj (T )). We evaluate downstream proof
cluding EvolAST-attributed judge calls.                 utility under a fixed round-robin B = 64
                                                        prover-attempt protocol (pass@64 / complete@64
Baselines. Our sampling baselines instantiate a         / theorem-complete@64; Table 2); full definitions
memoryless, no-archive setting: budget-matched          are in Section A.1.
variants with fresh sampling/repair and no archive
state. They include Sample (no repair), Com-            Semantic judge and manual calibration. The
pile Repair (bounded compilation repair), and           semantic predicate Sem is implemented by
C+S Repair (Compile+Semantic Repair: compila-           CriticLean-Qwen3-14B with a fixed prompt and
tion repair plus one bounded semantic-repair call       serving configuration; the judge prompt and judge-
for compilable candidates failing the judge). To        call accounting are reported in Appendix F.4
separate archive-search effects from patch-model        and Appendix E.2. Our semantic metrics rely
strength, Table 1 also reports Hybrid control: the      on an LLM-as-judge implementation of Sem.
same Kimina-generation/Qwen3-repair stack under         We therefore include manual faithfulness audits
T =100, but with independently sampled trajecto-        for a statement-stage sample from judge-positive
ries and no archive state, parent reuse, archive con-   ProofNet outputs and a theorem-complete prover-
text, usage-penalized selection, or island migration.   stage sample produced under the fixed B = 64
                                                        prover protocol. We summarize both audits in Sec-
Models. In our main runs, the sampling base-            tion 5 and provide their protocols and tables in
lines use Kimina-Autoformalizer-7B for sam-             Appendix C.1.
pling/repair, while FormalEvolve uses Kimina-
Autoformalizer-7B for seeding and Qwen3-30B-            5     Results
A3B for patch/repair. For proof utility, we fix the
                                                        5.1    Coverage and Uniformity
prover to Goedel-Prover-V2-32B (Lin et al., 2025)
with a fixed prompt template (Section F.5).             Statement generation at T = 100. Table 1 re-
                                                        ports statement generation under the same T = 100
Search configuration. Unless stated otherwise,          generator-call budget, including coverage (CH/SH)
FormalEvolve uses K = 2 islands, archive capacity       and concentration (Gini/top-10% share). Against
40, parent-selection parameters λ = 10 and β =          the hybrid no-archive control, which uses Kimina
0.05, an operator mix of full/diff/cross patching       generation with the same Qwen3 repair model but
with probabilities 0.5/0.3/0.2, and migration every     no archive, FormalEvolve increases SH@100 from
10 generations at rate 0.1; Appendix E.3 gives the      0.530 to 0.580 on CombiBench (+0.050, paired
complete configuration.                                 95% CI [0.003, 0.130]) and from 0.828 to 0.849 on
                                                        ProofNet (+0.022, paired 95% CI [0.005, 0.048]).
Table 1: Statement generation at T = 100. CH/SH measure compile/semantic coverage; Gini and top-10% share
measure concentration of semantic-success counts (lower is better).
                                           ProofNet (test, N = 186)                    CombiBench (N = 100)
 Method                           CH@100      SH@100        Gini↓  Top-10%↓   CH@100     SH@100     Gini↓   Top-10%↓
 Baselines (Kimina; no archive)
 Sample                            0.903       0.715     0.537      0.243      1.000      0.440    0.816     0.637
 Compile Repair                    0.909       0.720     0.566      0.263      0.990      0.400    0.825     0.641
 C+S Repair                        0.909       0.780     0.555      0.264      0.990      0.460    0.813     0.609
 Baselines (Qwen3; no archive)
 Qwen3 Sample                      0.387       0.242     0.896      0.876      0.300      0.200    0.939     0.952
 Qwen3 + Compile Repair            0.371       0.237     0.912      0.911      0.900      0.260    0.740     0.385
 Qwen3 + C+S Repair                0.688       0.548     0.802      0.656      0.940      0.390    0.827     0.655
 Hybrid control (no archive)
 Hybrid control                    0.973       0.828     0.505      0.241      1.000      0.530    0.790     0.588
 FormalEvolve
 FormalEvolve                      0.973       0.849     0.443      0.229      1.000      0.580    0.759     0.531
 FormalEvolve (K=1)                0.984       0.866     0.362      0.198      1.000      0.550    0.726     0.442
 FormalEvolve w/o EvolAST          0.973       0.871     0.454      0.236      1.000      0.500    0.776     0.577
 FormalEvolve w/o patch repair     0.903       0.780     0.449      0.211      1.000      0.470    0.772     0.494


We therefore interpret coverage together with cross-             tural perturbation may instead spend the fixed bud-
problem concentration and downstream proof util-                 get away from that trajectory. This is consistent
ity.                                                             with the higher ProofNet SH@100 of K=1 (0.866)
                                                                 and no-EvolAST (0.871), compared with 0.849
Ablations and component effects. The strongest
                                                                 for the default. CombiBench (domain-shift ex-
Kimina-only baseline is C+S Repair. Adding the
                                                                 ploration). CombiBench presents a substantially
stronger Qwen3 repair model without an archive
                                                                 stronger domain/style shift, where model priors
already improves SH@100 from 0.460 to 0.530 on
                                                                 more often fail and standard patching can collapse
CombiBench and from 0.780 to 0.828 on ProofNet.
                                                                 into repeated, unhelpful edits. Here, isolated search
FormalEvolve then adds archive-based search on
                                                                 trajectories help prevent premature convergence,
top of this repair strength, so the hybrid row can be
                                                                 while EvolAST forces structural variation when
read as a matched no-archive ablation. Remov-
                                                                 LLM-driven repair stalls. Consequently, K=2 with
ing patch repair drops SH@100 from 0.580 to
                                                                 EvolAST reaches SH@100 of 0.580, compared
0.470 on CombiBench and from 0.849 to 0.780
                                                                 with 0.550 for K=1 and 0.500 without EvolAST.
on ProofNet, identifying bounded repair as the
                                                                 We therefore use K=2 with EvolAST as a robust
largest direct driver of SH@100. The archive
                                                                 default across different domain difficulties rather
then makes repaired candidates reusable as parents
                                                                 than as a configuration that is optimal for every
and prompt context, allowing local repair gains
                                                                 dataset and metric; the main controlled compari-
to propagate through later search steps while re-
                                                                 son remains archive-based search versus matched
ducing repeated edits of the same templates. The
                                                                 no-archive controls.
island and EvolAST ablations expose a dataset-
dependent exploration–exploitation trade-off un-                 Cross-problem concentration. Coverage alone
der the fixed budget. ProofNet (high-prior ex-                   can hide a failure mode in which a method spends
ploitation). ProofNet consists of standard un-                   most of its successful calls on the same easy prob-
dergraduate mathematics, and the public autofor-                 lems. We therefore report Gini and top-10% share
malization SFT mixture used to initialize Kimina-                over per-problem semantic_ok counts. The de-
Autoformalizer includes ProofNet, together with                  fault FormalEvolve configuration lowers both con-
PutnamBench, miniF2F, and Compfiles (Wang                        centration metrics relative to the hybrid control:
et al., 2025a). The Kimina-based generation com-                 on CombiBench, Gini decreases from 0.790 to
ponent therefore starts with a particularly strong               0.759 and top-10% share from 0.588 to 0.531; on
prior on this benchmark. When the initial struc-                 ProofNet, the corresponding changes are 0.505 to
tures are already strong, centralizing the archive               0.443 and 0.241 to 0.229. Bootstrap intervals over
with K=1 or relying on LLM patch/repair with-                    problems show that the Gini reductions are stable
out EvolAST can exploit a productive trajectory                  for the matched hybrid comparison (+0.031 [0.010,
efficiently; additional island separation or struc-              0.055] on CombiBench; +0.062 [0.035, 0.090] on
                                                                             Sample                          C+S Repair                                       FormalEvolve w/o EvolAST
                                                                             Compile Repair                  FormalEvolve                                     FormalEvolve w/o patch repair

                                                                          CombiBench (N=100)                                                                         ProofNet test (N=186)
           Semantic coverage (# problems)
                                            56       @100: 58/100 vs 46/100 (Δ=+12)                                                             @100: 158/186 vs 145/186 (Δ=+13)
                                                     reach baseline @t=40 (2.5×)                                                   150          reach baseline @t=27 (3.7×)
                                            48
                                                                                                                                   135
                                            40
                                                                                       40
                                                                                                                                   120                                           140

                                            32
                                                                                       30                                                                                        120
                                                                                                                                   105
                                            24                                                                                                                                   100
                                                                                       20                                              90
                                                     t ≤ 16 seedbank ( ≡ Sample)                                                                t ≤ 16 seedbank ( ≡ Sample)
                                                                                                                                                                                  80
                                            16
                                                                                              5   10    15   20    25                                                                     5   10    15   20   25
                                                 1      10         25                50            75               100                     1      10         25                50             75             100
                                                              Generator-call budget (calls per problem)                                                  Generator-call budget (calls per problem)

Figure 3: Semantic coverage vs debited generator calls t on both benchmarks. The dotted line marks the nominal
seedbank boundary (t=16).




   Compile Repair                                                                                                   Compile Repair




      FormalEvolve                                                                                                      FormalEvolve




Figure 4: Per-problem semantic-success counts at T = 100 (semantic_ok; zeros shown as white). Columns are
ordered by the C+S Repair baseline, and only problems with a positive count for at least one method are shown.
The head/mid/tail regions are visualization bands induced by this baseline ordering, not predefined difficulty splits.

ProofNet), while top-10% reductions have the same                                                                                formal statement and bypasses both generator and
sign but wider intervals (Appendix B.1). Under                                                                                   semantic judge.
the C+S Repair ordering used in Figure 4, For-
                                                                                                                                 Theorem-complete gains and boundaries. On
malEvolve’s additional successes concentrate in
                                                                                                                                 CombiBench, FormalEvolve raises theorem-
the baseline-ranked mid and tail. In the tail seg-
                                                                                                                                 complete@64 from 9/100 for the matched Hybrid
ment, FormalEvolve has higher semantic-success
                                                                                                                                 control to 13/100, and from 8/100 for both Sam-
counts on 18 versus 2 lower-count problems on
                                                                                                                                 ple and Kimina C+S Repair. On ProofNet, For-
CombiBench, and on 49 versus 5 on ProofNet.
                                                                                                                                 malEvolve also improves over the matched Hy-
The head can still favor C+S Repair, especially
                                                                                                                                 brid control on theorem-complete@64 (45/186 vs.
on ProofNet, so the pattern reflects complemen-
                                                                                                                                 40/186), while remaining comparable to Kimina
tary problem-level coverage across the baseline-
                                                                                                                                 C+S Repair (45/186 vs. 46/186). These results are
induced bands. Figures 4 and 9 show the same
                                                                                                                                 consistent with the hedging motivation: diverse
pattern at the problem level and across budgets.
                                                                                                                                 repertoires can increase the chance of reaching a
5.2       Downstream Proof Utility                                                                                               prover-friendly accepted statement under a fixed
Prover protocol. For each non-empty dedupli-                                                                                     prover budget. Appendix A.2 and Appendix C.2
cated semantic repertoire, Goedel-Prover-V2-32B                                                                                  provide additional curves and audit details.
receives B = 64 attempts under a fixed round-                                                                                    5.3             Test-Time Cost and Efficiency
robin schedule; candidates are revisited when
                                                                                                                                 Under the same T =100 generator-call budget, For-
the repertoire contains fewer than 64 candidates.
                                                                                                                                 malEvolve improves both SH@100 and theorem-
Empty repertoires count as failures. The single-
                                                                                                                                 complete@64 over the matched Hybrid control,
reference GT control uses the dataset reference
                                                                                                                                 with end-to-end durations of 8.16 vs. 8.18 hours
statement and therefore retries that statement for
                                                                                                                                 on CombiBench and 17.29 vs. 20.77 hours on
all 64 attempts. Table 2 reports solved-problem
                                                                                                                                 ProofNet. Figure 5 presents this final-result com-
counts for pass@64, complete@64, and theorem-
                                                                                                                                 parison. Appendix E.2 reports the complete ac-
complete@64. The prover sees only candidates
                                                                                                                                 counting of generation, compilation-repair, and
with compile_ok= 1 and semantic_ok= 1, dedu-
                                                                                                                                 semantic-repair calls, semantic-judge calls, Lean
plicated under canonicalization. The GT reference
                                                                                                                                 evaluations, candidate records, and batch duration.
row runs the same prover on the dataset-provided
Table 2: Downstream proof utility at B = 64 prover attempts per problem. Theorem-complete counts complete
proofs of explicit theorem/lemma declarations.
                                                              CombiBench (N = 100)                                               ProofNet (test, N = 186)
 Method                                      pass@64           complete@64 thm-complete@64                        pass@64         complete@64 thm-complete@64
 FormalEvolve                                  44/100              27/100                       13/100                127/186            52/186                   45/186
 Hybrid control                                40/100              22/100                        9/100                110/186            49/186                   40/186
 Sample                                        41/100              23/100                        8/100                106/186            46/186                   41/186
 C+S Repair                                    40/100              23/100                        8/100                119/186            50/186                   46/186
 GT reference                                  96/100              68/100                       18/100                146/186            46/186                   34/186

                                                                    Sample            C+S Repair             Hybrid         FormalEvolve


                                         (a) CombiBench                                                                (b) ProofNet
      SH@100 (higher is better)




                                  0.60
                                                                                                               0.85

                                  0.55
                                                                                                               0.80

                                  0.50
                                                                                                               0.75

                                  0.45
                                                                                                               0.70
                                             6.5        7.0         7.5        8.0            8.5                      15       16      17     18      19       20      21
                                                    Batch duration (hours)                                                           Batch duration (hours)
                                           TC@64: S 8/100, C+S 8/100, H 9/100, FE 13/100                                 TC@64: S 41/186, C+S 46/186, H 40/186, FE 45/186

                                            FE vs H: SH 0.530 -> 0.580; time 8.18 -> 8.16 h                              FE vs H: SH 0.828 -> 0.849; time 20.77 -> 17.29 h

Figure 5: SH@100 versus batch duration under the same T =100 generator-call budget. The footer beneath each
panel reports theorem-complete@64 and the FormalEvolve–Hybrid comparison.

5.4     Stronger-Base and Manual Audits                                                                  fulness to the source statement (Appendix C.1).
Stronger-base statement-generation.             As a
                                                                                                         6     Conclusion
supplementary CombiBench statement-generation
check, we use Goedel-Formalizer-V2-8B seed-                                                              FormalEvolve is a compile-gated test-time search
ing and GPT-5.4 repair with the same judge and                                                           method for Lean 4 autoformalization under a fixed
T =100 accounting. FormalEvolve preserves the                                                            generator-call budget. The central lesson is that
pattern over the matched Hybrid control: SH@100                                                          autoformalization should be evaluated at the level
rises from 0.86 to 0.88, deduplicated SemOKtotal                                                         of budgeted, semantically filtered repertoires: faith-
rises from 1886 to 3238 (1.7×), and concentration                                                        ful variants of the same informal claim can ex-
drops in both Gini (0.4832 to 0.4383) and top-10%                                                        pose different prover-facing interfaces. FormalE-
share (0.3128 to 0.2202) (Appendix B.3).                                                                 volve operationalizes this view with a compilation-
Manual faithfulness calibration. Manual audits                                                           feasible archive that stores reusable candidates, ex-
calibrate selected statement-stage and theorem-                                                          pands them through repair and evolution, and fil-
complete slices. On a matched 50-problem                                                                 ters the resulting repertoire for downstream prov-
ProofNet statement-stage audit, FormalEvolve,                                                            ing. Across two benchmarks, this archive-based
Hybrid control, and Sample have similar Faith-                                                           organization improves semantic coverage, reduces
ful/Partial/Severe totals: 42/5/3, 43/4/3, and 43/3/4.                                                   cross-problem concentration, and yields theorem-
These similar profiles calibrate FormalEvolve’s                                                          complete gains over matched no-archive multi-
judge-positive outputs against the no-archive con-                                                       candidate controls under our fixed prover protocol.
trols in this slice. At the theorem-complete end,                                                        The same archive-and-filter pattern may also ex-
a 161-artifact audit over the original three-method                                                      tend to Coq, Isabelle, and related proof assistants,
pool shows that FormalEvolve yields the largest ab-                                                      where multiple faithful formalizations can likewise
solute count of faithful artifacts (41), while severe                                                    differ in downstream prover utility.
counts are numerically similar across methods (11,
10, and 12). Proof success establishes utility for the                                                   Limitations
encoded formal statement under the fixed prover                                                          Semantic consistency remains difficult to certify
protocol. Manual auditing separately assesses faith-                                                     automatically, which is a central challenge for
autoformalization. Our semantic metrics rely              Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W.
on an LLM-as-judge implementation of Sem,                    Ayers, and Stanislas Polu. 2022. Proof artifact co-
                                                             training for theorem proving with language models.
so results that use semantic labels–including se-
                                                             In The Tenth International Conference on Learning
mantic coverage, semantic-success counts, and                Representations (ICLR 2022). OpenReview.net.
concentration statistics–can depend on the judge
                                                          Robert Tjarko Lange, Yuki Imajuku, and Edoardo
model, prompt, and serving details. Compila-                Cetin. 2025. ShinkaEvolve: Towards open-ended
tion certifies Lean elaboration and type correct-           and sample-efficient program evolution. Preprint,
ness, while semantic equivalence to the informal            arXiv:2509.19349. ArXiv preprint.
problem remains outside the compiler’s guaran-            Joel Lehman and Kenneth O. Stanley. 2011. Aban-
tee. We therefore report manual faithfulness audits         doning objectives: Evolution through the search for
over outputs produced by our pipeline. On the               novelty alone. Evolutionary Computation, 19(2):189–
matched ProofNet statement-stage slice, FormalE-            223.
volve, Hybrid control, and Sample have similar            Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-
Faithful/Partial/Severe totals (42/5/3, 43/4/3, and         Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
43/3/4), suggesting that archive search does not vis-       Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing
                                                            Lu, David Acuna, Kaiyu Yang, Hongzhou Lin, Yejin
ibly amplify judge-positive semantic shift relative         Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. 2025.
to no-archive controls.                                     Goedel-Prover-V2: Scaling formal theorem proving
   Our pass@64, complete@64, and theorem-                   with scaffolded data synthesis and self-correction.
complete@64 results use one fixed prover configu-           Preprint, arXiv:2508.03613.
ration with B = 64 attempts.                              Fei Liu, Rui Zhang, Zhuoliang Xie, Rui Sun, Kai Li,
                                                            Qinglong Hu, Ping Guo, Xi Lin, Xialiang Tong,
Acknowledgments                                             Mingxuan Yuan, Zhenkun Wang, Zhichao Lu, and
                                                            Qingfu Zhang. 2024. LLM4AD: A platform for al-
This work was primarily conducted at the State              gorithm design with large language model. Preprint,
Key Laboratory of General Artificial Intelligence,          arXiv:2412.17287.
BIGAI.                                                    Junqi Liu, Xiaohan Lin, Jonas Bayer, Yael Dillies, Wei-
                                                            jie Jiang, Xiaodan Liang, Roman Soletskyi, Haiming
                                                            Wang, Yunzhou Xie, Beibei Xiong, Zhengfeng Yang,
References                                                  Jujian Zhang, Lihong Zhi, Jia Li, and Zhengying
                                                            Liu. 2025. CombiBench: Benchmarking LLM ca-
Zhangir Azerbayev, Bartosz Piotrowski, Hailey               pability for combinatorial mathematics. Preprint,
  Schoelkopf, Edward W. Ayers, Dragomir Radev, and          arXiv:2505.03171.
  Jeremy Avigad. 2023. ProofNet: Autoformalizing
  and formally proving undergraduate-level mathemat-      Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong,
  ics. Preprint, arXiv:2302.12433.                           Zhengying Liu, and Zhijiang Guo. 2024. For-
                                                             malAlign: Automated alignment evaluation for auto-
Guoxin Chen, Jing Wu, Xinjie Chen, Wayne Xin Zhao,           formalization. Preprint, arXiv:2410.10135.
  Ruihua Song, Chengxi Li, Kai Fan, Dayiheng Liu,
  and Minpeng Liao. 2025. ReForm: Reflective aut-         Jean-Baptiste Mouret and Jeff Clune. 2015. Illumi-
  oformalization with prospective bounded sequence           nating search spaces by mapping elites. Preprint,
  optimization. Preprint, arXiv:2510.24592. ArXiv            arXiv:1504.04909.
  preprint.
                                                          Alexander Novikov, Ngan Vu, Marvin Eisenberger, Em-
Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, and            ilien Dupont, Po-Sen Huang, Adam Zsolt Wagner,
  T. Meyarivan. 2002. A fast and elitist multiobjective     Sergey Shirobokov, Borislav Kozlovskii, Francisco
  genetic algorithm: NSGA-II. IEEE Transactions on          J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar, Abi-
  Evolutionary Computation, 6(2):182–197.                   gail See, Swarat Chaudhuri, George Holland, Alex
                                                            Davies, Sebastian Nowozin, Pushmeet Kohli, and
Marco Dos Santos, Hugues de Saxcé, Haiming Wang,            Matej Balog. 2025. AlphaEvolve: A coding agent
 Ran Wang, Mantas Baksys, Mert Unsal, Junqi Liu,            for scientific and algorithmic discovery. Preprint,
 Zhengying Liu, and Jia Li. 2025. Kimina lean server:       arXiv:2506.13131.
 A high-performance lean server for large-scale verifi-
 cation. Preprint, arXiv:2504.21230.                      Zhongyuan Peng, Yifan Yao, Kaijing Ma, Shuyue Guo,
                                                            Yizhe Li, Yichi Zhang, Chenchen Zhang, Yifan
Qi Guo, Jianing Wang, Jianfei Zhang, Deyang Kong,           Zhang, Zhouliang Yu, Luming Li, Minghao Liu,
  Xiangzhou Huang, Xiangyu Xi, Wei Wang, Jingang            Yihang Xia, Jiawei Shen, Yuchen Wu, Yixin Cao,
  Wang, Xunliang Cai, Shikun Zhang, and Wei Ye.             Zhaoxiang Zhang, Wenhao Huang, Jiaheng Liu, and
  2025. Autoformalizer with tool feedback. Preprint,        Ge Zhang. 2025. CriticLean: Critic-guided rein-
  arXiv:2510.06857.                                         forcement learning for mathematical formalization.
                                                            Preprint, arXiv:2507.06181.
Stanislas Polu and Ilya Sutskever. 2020. Generative
   language modeling for automated theorem proving.
  Preprint, arXiv:2009.03393.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar.
  2024. Lean copilot: Large language models as
  copilots for theorem proving in lean. Preprint,
  arXiv:2404.12534.
Yuchen Tian, Ruiyuan Huang, Xuanwu Wang, Jing
  Ma, Zengfeng Huang, Ziyang Luo, Hongzhan Lin,
  Da Zheng, and Lun Du. 2025. EvolProver: Advanc-
  ing automated theorem proving by evolving formal-
  ized problems via symmetry and difficulty. Preprint,
  arXiv:2510.00732.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jian-
  qiao Lu, Hugues de Saxcé, Bolton Bailey, Chen-
  dong Song, Chenjun Xiao, Dehao Zhang, Ebony
  Zhang, Frederick Pu, Han Zhu, and 21 others. 2025a.
  Kimina-Prover Preview: Towards large formal rea-
  soning models with reinforcement learning. Preprint,
  arXiv:2504.11354.

Hanyu Wang, Ruohan Xie, Yutong Wang, Guoxiong
  Gao, Xintao Yu, and Bin Dong. 2025b. Aria: An
  agent for retrieval and iterative auto-formalization
  via dependency graph. Preprint, arXiv:2510.04520.

Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N.
  Rabe, Charles Staats, Mateja Jamnik, and Christian
  Szegedy. 2022. Autoformalization with large lan-
  guage models. In Advances in Neural Information
  Processing Systems.

Haoyu Zhao, Yihan Geng, Shange Tang, Yong Lin, Bo-
  han Lyu, Hongzhou Lin, Chi Jin, and Sanjeev Arora.
  2025. Ineq-Comp: Benchmarking human-intuitive
  compositional reasoning in automated theorem prov-
  ing on inequalities. Preprint, arXiv:2505.12680.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  2022. miniF2F: a cross-system benchmark for for-
  mal olympiad-level mathematics. In The Tenth In-
  ternational Conference on Learning Representations
  (ICLR 2022). OpenReview.net.
A     Additional Results                                Table 3: Metric definitions under generator-call account-
                                                        ing.
We give the metric definitions used throughout the      Metric             Definition and interpretation
experiments, followed by statement-level decom-         FY(t)                1
                                                                                 P
                                                                           |Et |    c∈Et Comp(c); fraction of debited calls
positions, proof-utility decomposition, and budget-                        yielding compilable candidates.
                                                        CH(t)              I[∃c ∈ Et : Comp(c) = 1]; at least one compilable
sweep coverage gaps under the same generator-call                          candidate.
accounting.                                             SH(t)              I[∃c ∈ Et : Comp(c) = 1 ∧ Sem(c) = 1]; at least
                                                                           one compilable and judge-consistent candidate.
                                                                               1
                                                                                                 Sem(c), or 0 if Etfeas is empty;
                                                                                    P
                                                        SD(t)                 feas     c∈E feas
A.1    Metric definitions                                                   |Et
                                                                           semantic
                                                                                   |        t

                                                                               1
                                                                                  P density among compilable candidates.
                                                        SY(t)                       c∈Et Sem(c); semantic yield per call, treating
We provide definitions of all reporting metrics un-                         |Et |
                                                                           non-compilable candidates as Sem = 0.
der generator-call accounting. For a given prob-        Div(t)             |Dedup(Gt )|; deduplicated semantic successes.
                                                                                 PN
                                                                             1
lem, let Et denote the set of candidates evaluated      Cov(t)              N     j=1 I[sj (t) ≥ 1]; dataset-level semantic
                                                                           coverage.
up to debited call t, and let Etfeas = {c ∈ Et :
                                                                            P
                                                                                  |si (t)−sj (t)|
                                                                              i,j P
                                                        Gini(t)               2N
                                                                                                  ; concentration of semantic
                                                                                    j sj (t)+ε
Comp(c) = 1}. Let Gt = {c ∈ Et : Comp(c) =                                 successes
                                                                           P         (↓).
                                                                              j∈Top10% sj (t)
1 ∧ Sem(c) = 1}, and for dataset-level concentra-       Top-10%                 P
                                                                                  j sj (t)
                                                                                              ; success mass assigned to the
                                                                       easiest 10% problems (↓).
tion let sj (t) be the number of semantic-success       PU-pass@64     At least one RR64 prover attempt returns a
candidates for problem j at budget t. For proof util-                  Lean 4-accepted proof script.
                                                        PU-complete@64 At least one RR64 prover attempt returns a proof without
ity, let G̃t = Dedup(Gt ) be the deduplicated se-                      sorry.
                             (64)                       PU-theorem@64 At least one RR64 prover attempt returns a complete
mantic repertoire and let At = RR64(G̃t ) be its                       proof of an explicit theorem/lemma.
ordered sequence of B = 64 prover attempts. For          Each debited generator call yields one evaluated representative candidate;
                                                         repair and semantic-repair calls count as additional calls. Dedup uses
each problem with a non-empty repertoire, RR64           conservative whitespace/name canonicalization.
allocates 64 attempts in round-robin order over
the available candidates; if the repertoire contains    A.2       Proof utility decomposition
fewer than 64 candidates, candidates are revisited
                                                        Figure 6 decomposes theorem-complete@64 into
until the attempt budget is exhausted. The GT refer-
                                                        (i) whether a method produces a non-empty state-
ence contains one statement and is therefore retried
                                                        ment repertoire to attempt under the fixed prover
for all 64 attempts. Let Ppass (a) ∈ {0, 1} indicate
                                                        protocol, and (ii) whether at least one attempted
whether prover attempt a returns a Lean 4-accepted
                                                        statement is solved at theorem-complete level un-
proof script (warnings allowed; sorry permitted),
                                                        der the same attempt budget.
Pcomplete (a) ∈ {0, 1} indicate a complete proof
without sorry, and Ptheorem (a) ∈ {0, 1} indicate       A.3       Statement-level decompositions at
a complete proof of an explicit theorem/lemma.                    T = 100
                                                        Tables 4 and 5 decompose the fixed-budget
                                                        statement-level results. FY is compilation yield,
                                                        SD is semantic density conditional on compilation,
                                                        and SY is semantic yield per generator call (treating
                                                        compilation failures as semantic failures). Report-
                                                        ing FY/SH/SD/SY together separates gains from
                                                        (i) producing more compilable candidates, (ii) im-
                                                        proving semantic consistency among compilable
                                                        candidates, and (iii) reallocating budget between
                                                        proposal and repair.
                                                        Table 4: CombiBench statement-level results at T =
                                                        100.
                                                         Method                                  FY       SH         SD          SY
                                                         Sample                                 0.695    0.440     0.189        0.132
                                                         Compile Repair                         0.555    0.400     0.199        0.110
                                                         C+S Repair                             0.324    0.460     0.371        0.120
                                                         FormalEvolve                           0.407    0.580     0.326        0.133
                                                         FormalEvolve w/o EvolAST               0.346    0.500     0.313        0.108
                                                         FormalEvolve w/o patch repair          0.682    0.470     0.250        0.170
          Table 5: ProofNet statement-level results at T = 100.                                           protocol as the sampling baselines.
                         Method                                   FY           SH    SD      SY
                         Sample                                  0.702     0.715    0.599   0.421
                         Compile Repair                          0.625     0.720    0.622   0.389
                         C+S Repair                              0.509     0.780    0.760   0.387
                         FormalEvolve                            0.562     0.849    0.775   0.435
                         FormalEvolve w/o EvolAST                0.539     0.871    0.788   0.425
                         FormalEvolve w/o patch repair           0.694     0.780    0.684   0.475


 A.4                                Coverage gaps across the budget
Figure 7 reports the budget-sweep coverage gap
relative to the strongest Kimina sampling baseline.
The hybrid Kimina+Qwen3 baseline in Table 1
separates search effects from patch-model strength
under the same generator-call accounting and repair




                                          FormalEvolve

                                            C+S Repair



                                          GT reference




                                          FormalEvolve

                                            C+S Repair



                                          GT reference




 Figure 6: Decomposing theorem-complete@64 under a fixed prover and attempt budget (B=64). Each bar splits
 the benchmark denominator into problems with an empty statement repertoire for proving (zero prover attempts),
 problems with a non-empty repertoire but no theorem-complete success, and problems with at least one theorem-
 complete success.
                                                              Sample                        FormalEvolve                         FormalEvolve w/o patch repair
                                                              Compile Repair                FormalEvolve w/o EvolAST




                                                       CombiBench (N=100)                                                              ProofNet test (N=186)
Δ semantic cov. (# problems)




                               12   overtake @t=28; end +12                                                  16    overtake @t=20; end +13


                                8
                                                                                                               8

                                4
                                                                                                               0
                                0
                                                                                                             −8
                               −4

                                                                                                            −16
                               −8
                                             20           40              60         80           100                       20             40             60     80    100
                                            Generator-call budget (calls per problem)                                      Generator-call budget (calls per problem)

 Figure 7: Coverage gap vs debited calls, plotted as ∆ semantic coverage relative to the strongest Kimina sampling
 baseline (Compile+Semantic Repair). The zero line corresponds to the baseline; positive values indicate a method
 covers more problems at the same generator-call budget. The dotted vertical line marks the nominal seedbank
 boundary (t=16) used by evolution-based methods (pre-sampled seeds, debited calls); a small subset of problems
 can require additional debited seeds before evolution starts.
B     Analysis                                                                           Table 9: Prover-stage non-dominance at theorem-
                                                                                         complete@64 for FormalEvolve versus Com-
We provide additional measurements for the fixed-                                        pile+Semantic Repair (C+S Repair).
budget experiments: paired uncertainty, repair-call                                      Dataset          n both fail FormalEvolve only C+S Repair only both succeed
composition, prover-stage non-dominance, cross-                                          CombiBench 100            85                  7                    2                6
                                                                                         ProofNet   186           129                 11                   12               34
problem concentration, stronger-base behavior, and
component effects.
                                                                                         B.2        Cross-problem uniformity: coverage and
B.1       Paired uncertainty, call composition, and                                                 concentration
          prover non-dominance                                                           We assess whether semantic successes concen-
The measurements below are computed from the                                             trate on a small subset of easy problems under
same fixed-budget artifacts used for the main fig-                                       a fixed call budget. At T = 100, we summa-
ures and tables. They cover paired uncertainty (Ta-                                      rize the per-problem semantic_ok count distri-
ble 6), concentration uncertainty for the matched                                        bution using coverage (SH@100) and concentra-
hybrid comparison (Table 7), per-problem repair-                                         tion (Gini and top-10% share; Table 1). Figure 4
call composition (Table 8), and prover-stage non-                                        provides a compact per-problem view. For read-
dominance (Table 9).                                                                     ability, we filter to problems where at least one
                                                                                         method attains a positive semantic_ok count (oth-
Table 6: Paired uncertainty over problems for the
                                                                                         erwise the column is identically zero). We order
matched Hybrid no-archive comparison. Hybrid de-
notes the matched Kimina-generation/Qwen3-repair no-                                     columns by the strongest Kimina sampling baseline
archive control used in Table 1 and Table 2.                                             (Compile+Semantic Repair) using its per-problem
Dataset            Metric           mean(FE) mean(base)            ∆ [95% CI]
                                                                                         semantic_ok counts at T = 100, defining an x-
CombiBench SH@100 vs Hybrid           0.580       0.530        +0.050 [0.003, 0.130]
                                                                                         axis independent of FormalEvolve; Figure 8 uses
ProofNet   SH@100 vs Hybrid           0.849       0.828        +0.022 [0.005, 0.048]
                                                                                         the same ordering for the delta visualization. This
                                                                                         subsection uses Compile+Semantic Repair only
   We use paired bootstrap 95% confidence inter-                                         as a fixed ordering and visualization baseline; the
vals for the mean difference (FormalEvolve − base-                                       matched Hybrid comparisons are reported sepa-
line).                                                                                   rately in Table 6 and in the main results.
Table 7: Bootstrap uncertainty for concentration reduc-                                  Aggregate pattern under baseline ordering.
tions relative to the matched hybrid no-archive control.
                                                                                         Under this baseline ordering, gains concentrate
Positive ∆ means the hybrid control is more concen-
trated than FormalEvolve, so lower concentration is
                                                                                         in the baseline-ranked tail: on the filtered set,
better for FormalEvolve.                                                                 ∆ > 0 dominates in the tail segment, while the
Dataset          Metric        FE     Hybrid ∆ (Hybrid − FE)             95% CI
                                                                                         head segment can favor the baseline (especially
CombiBench      Gini          0.759    0.790          +0.031          [0.010, 0.055]
                                                                                         on ProofNet). We define head/mid/tail by split-
CombiBench Top-10% share
ProofNet        Gini
                              0.531
                              0.443
                                       0.588
                                       0.505
                                                      +0.057
                                                      +0.062
                                                                     [-0.009, 0.128]
                                                                      [0.035, 0.090]
                                                                                         ting the baseline-ordered problems into three
ProofNet   Top-10% share      0.229    0.241          +0.011         [-0.005, 0.032]     contiguous segments as evenly as possible within
                                                                                         each benchmark. The table below counts how
  We compute the intervals by resampling bench-                                          often ∆ = #semantic_ok(F ORMAL E VOLVE) −
mark problems with replacement and recomputing                                           #semantic_ok(C OMPILE +S EMANTIC R EPAIR)
each concentration metric on the resampled per-                                          is positive/negative/zero within each segment
problem semantic-success counts.                                                         (reported as +/ − /0).
Table 8: Debited repair-call composition under T =                                        Dataset                        head (+/ − /0)    mid (+/ − /0)        tail (+/ − /0)
100.                                                                                      CombiBench (filtered 64/100)       8/12/1            12/7/2              18/2/2
                                                                                          ProofNet (filtered 161/186)        6/41/6           35/19/0              49/5/0
Dataset      Method           CRep (median [q25,q75]) SRep (median [q25,q75])
CombiBench
CombiBench
             Sample
             Compile Repair
                                           0.0 [0.0, 0.0]
                                        29.0 [4.0, 52.0]
                                                                        0.0 [0.0, 0.0]
                                                                        0.0 [0.0, 0.0]
                                                                                         B.2.1   Representative early semantic hits and
CombiBench
CombiBench
             C+S Repair
             Hybrid control
                                        14.0 [4.0, 34.5]
                                        15.5 [2.8, 33.0]
                                                                    38.0 [26.0, 54.0]
                                                                    43.5 [25.8, 57.0]
                                                                                                 baseline-miss instances
CombiBench   FormalEvolve              30.5 [20.8, 39.0]            20.5 [14.0, 26.0]
ProofNet     Sample                       0.0 [0.0, 0.0]               0.0 [0.0, 0.0]
                                                                                         There are 16 such instances on each bench-
ProofNet     Compile Repair             16.0 [0.0, 53.0]               0.0 [0.0, 0.0]
ProofNet     C+S Repair                  9.0 [0.0, 39.8]             11.5 [0.0, 37.8]
                                                                                         mark, where Compile+Semantic Repair has zero
ProofNet
ProofNet
             Hybrid control
             FormalEvolve
                                         6.0 [0.0, 29.0]
                                        24.0 [8.0, 40.8]
                                                                     10.0 [0.0, 32.8]
                                                                      4.0 [0.0, 16.0]
                                                                                         semantic_ok at T =100 while FormalEvolve at-
                                                                                         tains a positive semantic_ok count. Conversely,
                                                                                         there are 4 such instances where the baseline hits
Table 10: Representative early semantic hits at a generator-call budget of T = 100. We include both directions
(FormalEvolve earlier / baseline no-hit, and baseline-hit / FormalEvolve no-hit). “> 100” indicates no semantic hit
within the call budget.
Benchmark             Problem id                              Short description                                                  FormalEvolve   C+S
                                                                                                                                    first hit Repair first
                                                                                                                                                 hit
 FormalEvolve hits earlier, or baseline has no hit within T = 100
CombiBench           0055_egmo_2022_p5                       Domino tilings: parity of f (n, 2k) for all k                            1          > 100
CombiBench           0063_usamo_2000_p4                      3 colored squares form an axis-aligned right triangle                    4          > 100
                                                                                              20102010
CombiBench            0077_imo_2010_p5                        Box/coin operations reach 2010             ?                             4         > 100
CombiBench            0035_brualdi_ch9_8                      Count SDRs for six 2-sets arranged in a cycle                           21         > 100
CombiBench            0011_brualdi_ch1_10                     No magic square of order 2                                              22          93
CombiBench            0047_brualdi_ch13_10                    Tournament: a vertex reaches all others within 2 steps                  27          95
CombiBench            0057_imosl_2015_c6                      Infinitely many integers without a unique odd-sum representation         2          31
CombiBench            0065_imo_2020_p3                        Split weighted colored pebbles into two equal piles                     27          52
ProofNet              0046_exercise_3_4_5b                    Quotients of solvable groups are solvable                               19         > 100
ProofNet              0124_exercise_26_12                     Perfect map: compact Y implies compact X                                21         > 100
ProofNet              0163_exercise_3_13                      Cauchy product of absolutely convergent series                          25         > 100
ProofNet              0119_exercise_23_3                      Connected union with shared intersection                                18          86
ProofNet              0095_exercise_5_6_14                    Distinct roots of xm − x in characteristic p                            24          91
ProofNet              0045_exercise_3_4_4                     Finite abelian groups have subgroups of each divisor order              12          62
ProofNet              0005_exercise_6_4_12                    No simple group of order 224                                             6          45
 Baseline hits, but FormalEvolve has no hit within T = 100
CombiBench             0037_brualdi_ch10_31                Difference set B = {0, 3, 4, 9, 11} in Z21                               > 100          22
CombiBench             0014_brualdi_ch2_36                 Counting combinations of multisets with bounded repetitions              > 100          39
CombiBench             0068_imo_2000_p4                    Distribute cards into 3 boxes so sums are equal                          > 100          50
CombiBench             0021_brualdi_ch4_9                  Max inversions in a permutation of {1, . . . , n}                        > 100          85
ProofNet              0185_exercise_5_1                       Blaschke condition for zeros of bounded holomorphic functions         > 100           3
ProofNet              0009_exercise_11_2_13                   Divisibility in Gaussian integers implies divisibility in Z           > 100          40
ProofNet              0094_exercise_5_4_3                     A root of a polynomial with radicals is algebraic                     > 100          49




Figure 8: Delta strips at T = 100 under fixed-budget accounting on the same filtered set and in the
same baseline ordering (sorted by Compile+Semantic Repair semantic_ok) as Figure 4, showing ∆ =
#semantic_ok(F ORMAL E VOLVE) − #semantic_ok(C OMPILE +S EMANTIC R EPAIR) per problem.

but FormalEvolve misses on CombiBench, and 3
on ProofNet. To ground the aggregate patterns
above and illustrate non-dominance, Table 10 lists
representative instances in both directions: where
FormalEvolve reaches a semantically consistent
compilable statement substantially earlier than the
baseline (or the baseline has no hit within T = 100
calls), and where the baseline hits but FormalE-
volve misses within the same call budget. These
examples are computed from the debited-call logs
under the same budget.
  Across both benchmarks, FormalEvolve im-
proves coverage and reduces concentration (see
Table 1 and Figures 4–9).
                                                                Sample                             C+S Repair                                                          FormalEvolve w/o EvolAST
                                                                Compile Repair                     FormalEvolve                                                        FormalEvolve w/o patch repair


                                                        CombiBench (N=100)                                                                                                               ProofNet test (N=186)
                                                                                                                                               0.60
Gini of semantic successes




                                                                                                                  Gini of semantic successes
                             0.84                                                                                                              0.58

                                                                                                                                               0.56
                             0.82
                                                                                                                                               0.54

                             0.80                                                                                                              0.52

                                                                                                                                               0.50
                             0.78
                                                                                                                                               0.48

                                                                                                                                               0.46
                             0.76
                                                                                                                                               0.44
                             0.74
                                          20              40              60               80              100                                                        20                    40                        60                    80                   100
                                               Generator-call budget (calls per problem)                                                                                   Generator-call budget (calls per problem)

 Figure 9: Cross-problem concentration of semantic successes vs generator-call budget, summarized by the Gini
 coefficient of per-problem semantic-success counts under fixed-budget accounting. Lower is more uniform (less
 concentrated on a small subset of problems). Table 1 reports the corresponding summary at T = 100.

 B.3                                Stronger-base statement-generation                                                                     10% share 0.3128 → 0.2202). The search layer
                                    evaluation on CombiBench                                                                               both expands the total pool of judge-accepted can-
                                                                                                                                           didates and makes that pool less concentrated.
Table 11: Stronger-base statement-generation evalua-
tion on CombiBench (N =100, T =100). SemOKtotal                                                                                                B.4        What drives gains: repair versus online
is the deduplicated aggregate count of judge-consistent                                                                                                   diversity
compiled candidates across problems.
                                                                                                                                               Under fixed budgets, bounded patch/repair calls
              Method                     CH@100 SH@100 SemOKtotal                Gini↓          Top-10%↓
                                                                                                                                               are the dominant contributor to semantic hit rate:
              Sample                       0.95          0.82         1478       0.5852          0.3410
              C+S Repair                   0.93          0.85         1443       0.5693          0.3389                                        removing patch repair reduces SH@100 by 11/100
              Hybrid control               0.98          0.86         1886       0.4832          0.3128                                        (CombiBench) and 13/186 (ProofNet) (Table 1).
              FormalEvolve                 0.95          0.88         3238       0.4383          0.2202
                                                                                                                                               EvolAST-style fallback has a smaller and non-
                                                                                                                                               monotonic effect: relative to the no-EvolAST ab-
Setup. The primary comparison uses a Kimina-
                                                                                                                                               lation, the run with EvolAST gains semantic hits
based stack to keep the core comparison controlled
                                                                                                                                               on 11 CombiBench problems and loses them on
under the same generator-call budget. To test
                                                                                                                                               3, while on ProofNet it gains 1 and loses 5. Be-
whether the search layer still helps once the base
                                                                                                                                               cause semantic_ok is assigned by the LLM-as-
stack is substantially stronger, we run a statement-
                                                                                                                                               judge implementation of Sem, these differences
generation evaluation on CombiBench under the
                                                                                                                                               should be read as changes in the distribution of
same T =100 accounting with Goedel-Formalizer-
                                                                                                                                               judge-accepted candidates rather than guaranteed
V2-8B as the seeder and GPT-5.4 as the repair
                                                                                                                                               semantic improvements.
model. We keep the semantic judge and statement-
stage reporting protocol unchanged.                                                                                                            Illustrative instances (EvolAST can help or
                                                                                                                                               hurt). The examples below show one instance
Compared methods. S AMPLE uses Goedel-
                                                                                                                                               where EvolAST enables a semantic hit and one
Formalizer-V2-8B alone, without repair or archive
                                                                                                                                               where it suppresses a hit under the same T =100
search. C OMPILE +S EMANTIC R EPAIR keeps the
                                                                                                                                               budget.
same stronger seeder and applies bounded compile
/ semantic repair without an archive. H YBRID CON -                                                                                            Problem                 Dataset    first hit call (w/ EvolAST / w/o)   semantic_ok (w/ EvolAST / w/o)   ∆ semantic_ok
                                                                                                                                               0011_brualdi_ch1_10   CombiBench             22 / no hit                           12 / 0                   +12
TROL keeps the same stronger seeder and stronger                                                                                               0014_brualdi_ch2_36   CombiBench             no hit / 48                           0/3                       -3


repair stack, with archive-based search disabled.                                                                                              B.5        Failure modes
F ORMAL E VOLVE then adds archive-based search
on top of this no-archive control.                                                                                                             We log (i) compilation failures, (ii) semantic drift
                                                                                                                                               (judge rejects), and (iii) judge/prover disagree-
 Interpretation. The stronger-base statement-                                                                                                  ments for qualitative inspection. The qualitative
 generation setting preserves the main qualitative                                                                                             cases in Appendix D show representative instances
 pattern. Relative to the matched no-archive hy-                                                                                               of these disagreements.
 brid control, archive-based search still improves
 SH@100 (0.86 → 0.88), increases deduplicated                                                                                                  Example (judge/prover mismatch). In Ap-
 SemOKtotal by 1.7× (1886 → 3238), and further                                                                                                 pendix D.1.3 (ProofNet 0004_exercise_6_4_2),
 reduces concentration (Gini 0.4832 → 0.4383; Top-
both baselines obtain theorem-complete prover out-         Multi-reader cross-check. On a multi-reader
puts under the same RR64 budget, while our best            cross-check subset drawn from the manually au-
judge-accepted statement is only pass-level. This          dited portion, the initial agreement rate on the Faith-
illustrates non-dominance between semantic judg-           ful / Partial / Severe labels is 92% before adjudi-
ing and prover utility: semantic acceptance and            cation. Disagreements were rechecked jointly, and
proof success provide different evidence under             uncertain cases were resolved conservatively.
fixed-budget evaluation.
                                                           Aggregate pattern. Within this audited theorem-
C     Human and Prover-Stage Audits                        complete pool, F ORMAL E VOLVE yields the largest
                                                           absolute count of Faithful artifacts (41), while Se-
C.1    Manual faithfulness audits                          vere counts are numerically similar across methods
Audit overview. We report two complementary                (11, 10, and 12). Proof success certifies the formal
manual audits with the same Faithful / Partial /           statement that was actually encoded and proved,
Severe label set. The first audit targets theorem-         but does not by itself establish faithfulness to the
complete artifacts from the three original generator-      source statement; all three audited methods still
based methods at the solved end of the pipeline.           contain severe mismatches at the solved end of
The second targets the main statement-stage setting        the pipeline. The audit therefore complements the
with a matched ProofNet audit over FormalEvolve,           main fixed-budget results with a direct theorem-
the hybrid no-archive control, and Sample.                 faithfulness view at the solved end of the pipeline.
Theorem-complete audit: scope and audit unit.              Matched statement-stage audit. Because the
We audit the theorem-complete end of the origi-            statement-stage semantic metrics rely on judge-
nal three-method comparison pool. The pool con-            positive outputs, we also audit matched judge-
tains 161 theorem-complete artifacts across S AM -         positive statement-stage outputs on ProofNet. We
PLE , C+S R EPAIR , and F ORMAL E VOLVE : 29               sample 50 problems for which FormalEvolve, the
from CombiBench and 132 from ProofNet. The                 hybrid no-archive control, and Sample each have a
audit unit is one solved benchmark × method                late-window compile+semantic judge-positive wit-
× problem cell. If a solved cell contains multi-           ness. For each method and sampled problem, the
ple theorem-complete attempts, we take the first           audit unit is the latest deduplicated judge-positive
theorem-complete attempt in per_problem.json               candidate with insertion rank in [20, 100]. This
order and trace it back to the corresponding source        design compares faithfulness profiles on a shared
statement in rr64_dataset.jsonl.                           judge-positive slice; coverage is reported separately
                                                           by SH@100.
Labels. Faithful means that the proved formal
statement matches the mathematical content of              Table 14: Matched manual statement-stage audit on late-
the informal target. Partial denotes a materially          window judge-positive ProofNet outputs. The same 50
                                                           problems are audited for all three methods.
narrowed, incomplete, or otherwise only partially
                                                                    Method            Faithful   Partial   Severe
aligned statement. Severe denotes wrong-object,
                                                                    F ORMAL E VOLVE     42         5         3
vacuous, or structurally broken cases that do not                   Hybrid control      43         4         3
preserve the intended mathematical claim.                           Sample              43         3         4


Table 12: Pool-level totals for the manual faithfulness    Interpretation. Under final adjudication, the
audit over theorem-complete artifacts in the original      matched statement-stage audit shows similar faith-
three-method comparison pool.                              fulness profiles across the three methods: FormalE-
         Pool              Faithful   Partial   Severe     volve has 42/50 Faithful candidates, Hybrid control
         CombiBench (29)     18          4        7        has 43/50, and Sample has 43/50. Severe counts
         ProofNet (132)      93         13       26
         Total (161)         111        17       33        are also close (3/50, 3/50, and 4/50 respectively).
                                                           In this slice, FormalEvolve’s judge-positive out-
Table 13: Method-level totals for the same manual faith-
                                                           puts have a faithfulness profile similar to the two
fulness audit.
                                                           no-archive controls, with no obvious additional se-
         Method            Faithful   Partial   Severe
                                                           mantic shift from archive search.
         F ORMAL E VOLVE     41         6        11
         S AMPLE             34         5        10
         C+S R EPAIR         36         6        12
C.2   Prover-stage audit: what proof success
      certifies
Scope and claim boundary. We audit the prover
stage on the subset of judge-accepted statements
produced within the generator-call budget (Sec-
tion 4). A prover-complete Lean file certifies that
the produced formal artifact is accepted by Lean
and contains no remaining sorry. Faithfulness
to the original informal statement is assessed by
the LLM-as-judge implementation of Sem and
checked with manual audits (Appendix C.1).
Prompt reference. The prover prompt template
is fixed (Appendix F.5); the case studies report the
proved formal statement and the prover response.
ASCII normalization. For compatibility with
pdfLaTeX, raw transcripts in PromptBox are dis-
played after ASCII-only normalization of common
Unicode math symbols (e.g., rendering quantifiers
and connectives in ASCII form). This affects pre-
sentation only.
Theorem-complete reporting. In addition to
standard pass@64 and complete@64, we re-
port theorem-complete@64: a problem counts
as theorem-complete@64 if at least one prover
attempt yields a Lean-accepted, sorry-free file
that contains an explicit theorem or lemma. This
guards against Lean-complete outputs that only
introduce auxiliary def/abbrev/example content
without proving a named proposition. All prover-
stage results below use the RR64 attempt schedule
defined in Section A.1.
Prompt categories. Table 15 also reports a
coarse prompt-type audit for the audited generator-
based methods over prover attempts (not over prob-
lems): the denominator is the number of prover
prompts actually issued under a fixed per-problem
attempt budget. We label an attempt as “Prompt
has theorem” if the candidate statement sent to the
prover contains an explicit theorem/lemma declara-
tion. We label an attempt as “Prompt abbrev-only”
if the candidate contains an abbrev declaration and
no theorem/lemma. Remaining attempts typically
correspond to def or example templates and are
omitted from this summary.
Table 15: Prover-stage audit statistics under B=64 prover attempts per problem for the audited generator-based
methods. Prompt-category counts are reported per prover attempt, not per problem. We report (i) whether the prover
prompt contains a theorem/lemma declaration vs. abbrev-only prompts, and (ii) pass@64/complete@64 together
with theorem-complete@64.
                                   Benchmark         Method                 Prompt has theorem              Prompt abbrev-only             pass@64        complete@64         theorem-complete@64
                                   CombiBench        FormalEvolve              2299/3648 (0.630)                 384/3648 (0.105)           44/100           27/100                    13/100
                                   CombiBench        C+S Repair                1813/2944 (0.616)                 384/2944 (0.130)           40/100           23/100                     8/100
                                   CombiBench        Sample                    1792/2816 (0.636)                 256/2816 (0.091)           41/100           23/100                     8/100
                                   ProofNet          FormalEvolve              9136/9536 (0.958)                 192/9536 (0.020)           127/186          52/186                    45/186
                                   ProofNet          C+S Repair                8938/9280 (0.963)                 128/9280 (0.014)           119/186          50/186                    46/186
                                   ProofNet          Sample                    8164/8512 (0.959)                 128/8512 (0.015)           106/186          46/186                    41/186

                                                                   FormalEvolve pass@k                    Sample pass@k                              C+S Repair complete@k
                                                                   C+S Repair pass@k                      FormalEvolve complete@k                    Sample complete@k



                                                       CombiBench (N=100)                                                                                    ProofNet test (N=186)
                                                                                                                                                                                                          114/186
                          70                                                                                                                                                                              (61.3%)
                          60
                                                                                                                                                                                                            127/186
                                                                                                                                                                                                            (68.3%)
  Success (%)




                          50                                                                           39/100
                                                                                                       (39.0%)                                                              66/186
                                                                         32/100                                                                                             (35.5%)
                          40                                             (32.0%)                                                                                                           89/186
                                                                                                          44/100                                                                           (47.8%)
                          30                                                                             (44.0%)
                                                                                        36/100
                          20                                                            (36.0%)

                          10

                           0



                                                                                                                                                                                                          p+16
                                   Δ = FormalEvolve − C+S Repair                                                                        Δ = FormalEvolve − C+S Repair                                     c+4
  Δ solved (# problems)




                          15
                                                                                                                                                                            p+11
                                                                                                                                                                            c+1            p+10
                                                                                                                                                                                           c+5                   p+8
                          10                                             p+7                                                                                                                                     c+2
                                                                         c+6            p+3
                                                                                        c+5            p+1 p+4
                           5                                                                           c+4 c+4



                           0

                               1            2          4             8             16             32               64               1            2           4          8             16             32                64
                                                     Prover attempt budget (k)                                                                             Prover attempt budget (k)

Figure 10: Proof utility as a function of prover attempts k on the judge-accepted repertoire produced within T = 100
calls. Solid: pass@k; dashed: complete@k; bottom row shows the gap relative to Kimina Compile+Semantic
Repair.

Takeaway. On ProofNet, most prover prompts
contain a theorem/lemma (around 0.96), so
theorem-complete filtering is close to the standard
metrics. On CombiBench, 9–13% of prompts are
abbrev-only; theorem-complete@64 is therefore a
stricter and more robust success signal.
      Δ                         CombiBench (N=100)                                             Δ                      ProofNet test (N=186)
                                                                                          1      0
  1   -21
                                                                                                -4
                                                                                               +1
      +1                                                                                         0
                                                                                               -12
      +19                                                                                 6      0                                                             64
                                                                                               -53
      +23                                                                                      -14
                                                                                               +4
      +11                                                                                        0
                                                                                         11    +6
      +1                                                                                       +4
  6
                                                                                               +4
                                                                                                -3
      -4
                                                                                               -11
                                                                                         16     -5
      -1
                                                                                                -2




                                                                                                                                                                    Theorem-complete proof count (≤ 64)
                                                                                               +3
      +64                                                                                       -3
                                                                                               +7
      +25                                                                                21    +8
                                                                                               -19
 11   +15                                                                                      +7
                                                                                               +2
      +12                                                                                      -16
                                                                                         26     -9
      +10                                                                                       -8
                                                                                               +17
                                                                                                -3
      +1
                                                                                                -2
                                                                                         31     -3                                                             32
      +1
                                                                                               +18
                                                                                                -4
 16    0                                                                                        -4
                                                                                                -2
       0                                                                                 36     -3
                                                                                                -3
       0                                                                                        -2
                                                                                                -2
       0                                                                                       +9
                                                                                         41    +1
       0                                                                                         0
                                                                                                -1                                                             16
                                                                                                -1
 21    0
                                                                                                -1
                                                                                         46     -1
       0
                                                                                               +48
                                                                                               +24
       0                                                                                       +13
                                                                                               +12
                                                                                                                                                               8
       0                                                                                 51    +7
                                                                                               +6
       0                                                                                       +3                                                              4
                                                                                               +2                                                              2
 26    0                                                                                       +2                                                              1
                                                                                         56    +1
       0                                                                                         0
                                                                                                 0
                                                                                                 0
 28    0
                                                                                         60      0


                                                    olv
                                                          e                    ce                                                        olv
                                                                                                                                            e            nce
                  ple              air         lEv                          ren                         ple          epa
                                                                                                                          ir
                                                                                                                                     lEv             fere
               Sam             Rep            a
                                                                  T re
                                                                       fe                            Sam           SR             ma               re
                           C+S           Form                 G                                                 C+             For              GT

Figure 11: Filtered per-problem theorem-complete attempt counts under RR64 (cell = number of attempts, out of
B=64, that yield a theorem/lemma without sorry). Rows show only problems where at least one method attains at
least one theorem-complete attempt (so the number of displayed problems is smaller than N ). Generator-based
methods only attempt statements that pass the semantic judge (semantic_ok= 1), whereas the Ground truth column
runs the prover on the dataset-provided ground-truth formal statement (one per problem), bypassing the judge.



            FormalEvolve




            GT reference



                                                                                    Prover attempt index (RR64)
                                                  theorem-complete hits within k=64: FormalEvolve=30 (hit=True) vs GT reference=0 (hit=False)

Figure 12: Data-driven motivating example under RR64 on ProofNet: even among judge-accepted candidates,
prover outcomes can vary substantially under a fixed prover and attempt budget. The single-reference GT control
uses one canonical statement (retried under RR64), while FormalEvolve provides a diverse judge-accepted repertoire,
increasing the chance that at least one provable formulation is found within budget.

D     Case Studies and EvolAST Ablation                                                       one counterexample that highlights non-dominance
                                                                                              and judge/prover mismatch. To contextualize these
We give representative statement/prover interac-
                                                                                              examples, Table 9 quantifies prover-stage non-
tions and an EvolAST ablation to illustrate where
                                                                                              dominance frequency at theorem-complete@64
archive search helps, where it is non-dominant, and
                                                                                              (FormalEvolve versus Compile+Semantic Repair)
how symbolic rewrites can change search trajecto-
                                                                                              under the same RR64 protocol.
ries under a fixed budget.
                                                                                              D.1.1  Theorem-complete proof:
D.1     Case studies: two successes and one                                                          FormalEvolve completes; baselines have
        non-dominance example                                                                        no pass
Scope. We include two short success cases that                                                Benchmark: proofnet.
illustrate prover-stage outcomes under the same                                               Problem id: 0088_exercise_4_3_1.
RR64 budget (one where baselines fail to produce                                              Informal statement:
any Lean 4-accepted proof output, and one where                                                       If R is a commutative ring and a ∈ R, let L(a) =
a baseline reaches only pass-level artifacts), plus                                                   {x ∈ R | xa = 0}. Prove that L(a) is an ideal
                                                                                                      of R.
Outcome under the same fixed B = 64 prover                                                         gen0 init
                                                                                                   0d4bccde
                                                                                                   C=1, S=0

budget. Our run attains a theorem-complete                                                         children=3




proof, while both sampling baselines fail to pro-                                 gen20 full
                                                                                  7d521d74
                                                                                                   gen1 diff
                                                                                                   b0a6df29
                                                                                                                      gen33 full
                                                                                                                      9dc02192
                                                                                  C=1, S=1         C=1, S=0           C=1, S=1
duce any Lean 4-accepted proof output within                                                       children=3



B = 64 attempts (no pass).                                                                     gen1 semantic repair
                                                                                               f63a25ca
                                                                                               C=1, S=1
                                                                                               children=4

Takeaway. This instance illustrates a practical
benefit of a repertoire: under a fixed prover attempt                         gen8 full
                                                                              2fdc680c
                                                                              C=1, S=1
                                                                                                    gen42 full
                                                                                                    68049b58
                                                                                                    C=1, S=1
                                                                                                                          gen53 diff
                                                                                                                          3ccb476a
                                                                                                                          C=1, S=1

budget, the ability to try multiple judge-accepted
statements can be the difference between reaching a
complete proof and having no Lean-accepted proof                 Figure 13: ProofNet 0000_exercise_2_3_2 statement
output at all.                                                   evolution trace (Comp=compile-ok, Sem=semantic-ok).
                                                                 The repair step removes an extra conjunction and intro-
Notation. Lean 4 admits both Unicode and                         duces the conjugation structure (the g −1 term).
ASCII forms. For pdfLaTeX compatibility, we
display prover transcripts in ASCII, where quanti-               Outcome under the same fixed B = 64 prover
fiers/connectives may appear as forall/-> and the                budget. Our run reaches a theorem-complete
constructor names And/Or, corresponding to ∀/ →                  proof (complete=True, sorries=0), while Com-
and ∧/∨.                                                         pile+Semantic Repair only reaches pass-level arti-
                                                                 facts with remaining sorry.
Abridged prover output excerpt (FormalEvolve;
theorem-complete).                                               Prover output excerpt (FormalEvolve; theorem-
                                                                 complete).
import Mathlib

open Fintype Set Real Ideal Polynomial                           import Mathlib
open scoped BigOperators
noncomputable section                                            theorem my_theorem_xxx {G : Type*} [Group G] (a b : G) :
                                                                   exists g : G, a * b = g * (b * a) * g^(-1) := by
theorem my_theorem_123 {R : Type*} [CommRing R] (a : R) :          refine Exists.intro a ?_
  forall x y : R, x * a = 0 -> y * a = 0 ->                        simp [mul_assoc, mul_left_inv, mul_right_inv]
    And ((x + y) * a = 0)
      (And ((-x) * a = 0)
         (forall r : R, And ((r * x) * a = 0) ((x * r) * a =
         0))) := by
                                                                 Statement evolution trace (mechanism note).
intro x y hx hy                                                  This instance illustrates why we separate compila-
have h1 : (x + y) * a = 0 := by
  calc (x + y) * a = x * a + y * a := by ring                    tion from semantic checking: an early candidate
       _ = 0 := by simp [hx, hy]
have h2 : (-x) * a = 0 := by                                     may compile yet express a non-standard (and gener-
  calc (-x) * a = - (x * a) := by ring
       _ = 0 := by simp [hx]
                                                                 ally stronger) variant of the target claim, which can
have h3 : forall r : R, And ((r * x) * a = 0) ((x * r) * a =     be judged inconsistent and/or harder for the prover
0) := by
  intro r                                                        to use under a fixed attempt budget. Here, the par-
  have h4 : (r * x) * a = 0 := by calc (r * x) * a = r * (x *
  a) := by ring; _ = 0 := by simp [hx]                           ent uses a conjunction of two equations, whereas
  have h5 : (x * r) * a = 0 := by calc (x * r) * a = (r * x) *   the informal goal is a single conjugacy statement of
  a := by ring; _ = 0 := h4
  exact And.intro h4 h5                                          the form a∗b = g ∗(b∗a)∗g −1 . Bounded semantic
exact And.intro h1 (And.intro h2 h3)
                                                                 repair removes the extra conjunct and rewrites the
FormalEvolve: pass=True,   complete=True,   sorries=0
                                                                 statement into this standard form while preserving
C+S Repair: pass=False
Sample: pass=False
                                                                 compilation feasibility (Figure 13).
                                                                 init (Comp=1, Sem=0): exists g, a*b = g*b*a /\ b*a = g*a*b
                                                                 repair (Comp=1, Sem=1): exists g, a*b = g*(b*a)*g^(-1)
D.1.2  Complete proof: FormalEvolve
       completes; baseline is pass-only
                                                                 D.1.3  Non-dominance case: baseline
Benchmark: proofnet.
                                                                        theorem-complete; FormalEvolve
Problem id: 0000_exercise_2_3_2.
                                                                        pass-only
Informal statement:
                                                                 Benchmark: proofnet.
     Prove that the products ab and ba are conjugate             Problem id: 0004_exercise_6_4_2.
     elements in a group.
                                                                 Informal statement:
                                                                      Prove that no group of order p q, where p and q
                                                                      are prime, is simple.
Outcomes under the same fixed B = 64 prover
budget. In this instance, our best judge-accepted
statement yields pass=True but not a complete
proof, while both sampling baselines obtain a
theorem-complete proof within the same prover
attempt budget.
Takeaway. This example highlights non-
dominance: even under the same prover budget,
different judge-accepted statements can differ
substantially in proof-search friendliness, so proof
utility and semantic faithfulness need separate
readouts.
Prover output excerpt (FormalEvolve; pass-
only). The excerpt below contains remaining
sorry; the baseline theorem-complete outputs
serve as the comparison point through the reported
outcome flags. FormalEvolve (pass-only):

import Mathlib

theorem my_theorem_12345 {G : Type*} [Group G] [Fintype G] (p
q : Nat)
  (hp : p.Prime) (hq : q.Prime) (hcard : Fintype.card G = p *
  q) :
    Not (IsSimpleGroup G) := by
  have h_main : Not (IsSimpleGroup G) := by sorry
  sorry


FormalEvolve: pass=True, complete=False, sorries=1
C+S Repair: pass=True, complete=True, sorries=0
Sample: pass=True, complete=True, sorries=0



D.2   Early proof successes under fixed prover
      budgets
Table 16 lists representative instances where For-
malEvolve reaches a successful proof substantially
earlier than Compile+Semantic Repair under the
same prover attempt budget, or succeeds when the
baseline fails within B = 64 attempts. We report
the first prover attempt index k (under the round-
robin schedule described in Section A.1) where
the prover returns (i) any proof script accepted
by Lean 4 (pass) or (ii) a complete proof without
sorry (complete).
Table 16: Representative early proof successes under a fixed per-problem prover attempt budget B = 64, computed
on the judge-accepted repertoire produced within T = 100 generator calls. We report the first prover attempt index
k where the prover succeeds; “> 64” indicates no success within the attempt budget.
Benchmark          Criterion      Problem (id + short description)                                                      FormalEvolve first k C+S Repair first k
 Both succeed, but FormalEvolve is much earlier
ProofNet            pass          0113_exercise_18_8a – order topology: {x | f (x) ≤ g(x)} is closed                               1                         58
ProofNet            complete      0113_exercise_18_8a – order topology: {x | f (x) ≤ g(x)} is closed                              12                         58
ProofNet            pass          0174_exercise_5_3 – f (x) = x + εg(x) is injective for small ε                                   2                         64
ProofNet            complete      0174_exercise_5_3 – f (x) = x + εg(x) is injective for small ε                                  13                         64
CombiBench          pass          0047_brualdi_ch13_10 – tournament radius-2 vertex exists                                         9                         27
CombiBench          complete      0047_brualdi_ch13_10 – tournament radius-2 vertex exists                                        21                         27
CombiBench          pass          0057_imosl_2015_c6 – infinitely many non-clean integers                                          1                          5
CombiBench          complete      0057_imosl_2015_c6 – infinitely many non-clean integers                                          3                         15
 FormalEvolve succeeds, baseline fails within B = 64
ProofNet          complete        0000_exercise_2_3_2 – ab and ba are conjugate in a group                                         2                        > 64
ProofNet          complete        0046_exercise_3_4_5b – solvable quotients are solvable                                           1                        > 64
CombiBench        complete        0007_hackmath_8 – ferry crossing: women in first group                                           1                        > 64
CombiBench        complete        0063_usamo_2000_p4 – 3 colored squares make a right triangle                                     1                        > 64


Table 17: ProofNet instances where the main run and the no-EvolAST ablation disagree on semantic hit@100 under
fixed-budget accounting. We report the first call index where a semantic success appears (when it does), computed
from the budget accounting logs.
  Problem id                   Short description                                                   Main (repair + EvolAST)             No EvolAST (repair only)
                                                         2
  0066_exercise_8_3_6b               √ is a field with q elements
                               Z[i]/(q)                     √      (for q ≡ 3 mod 4)                           no hit                          hit at call 42
  0070_exercise_9_4_9          x2 − 2 irreducible over Z[ 2]                                                   no hit                          hit at call 65
  0142_exercise_4_15a          Uniform continuity iff having a modulus of continuity                           no hit                          hit at call 49
  0151_exercise_1_8            No ordered-field structure
                                                   P on C                                                      no hit                          hit at call 39
  0185_exercise_5_1            Blaschke condition: n (1 − |zn |) < ∞ for bounded holomorphic                   no hit                          hit at call 66
                               f
  0123_exercise_25_9           Identity component is a normal subgroup                                     hit at call 87                          no hit



D.3     Ablation note: when EvolAST changes                                   candidates but no semantic success, whereas the
        outcomes on ProofNet                                                  no-EvolAST configuration eventually reaches a
On ProofNet, enabling EvolAST slightly decreases                              judge-accepted statement after semantic repair.
semantic hit@100 under fixed-budget accounting                                One characteristic we observe in the main run
(158/186 vs 162/186). The gap is small (4 prob-                               is that EvolAST fallback triggers repeatedly
lems), but it illustrates an important point for bud-                         on duplicates and compile failures, producing
geted search: a diversity operator can change the                             compilable but judge-rejected variants; in this
search trajectory and archive composition, and may                            problem, many candidates are explicitly tagged
not be universally beneficial across datasets.                                as EvolAST fallbacks, and all have Comp(c) = 1
                                                                              but Sem(c) = 0. This can bias the archive toward
Where the difference comes from. Under fixed-                                 structurally perturbed but semantically misaligned
budget accounting, there are 5 problems that                                  candidates under a fixed budget, which in turn
achieve at least one judge-accepted statement un-                             alters parent selection and patch contexts.
der the no-EvolAST configuration but not under                                   Concretely, the semantic judge flags a common
the main configuration, and 1 problem where the                               failure mode here: domain mismatch (e.g., proving
reverse holds. Because the generator and patch-                               uniform continuity on R with the intended [a, b]
ing process are stochastic, these disagreements                               restriction missing). The best candidate found by
reflect diverging search trajectories under nearly                            the main run (compilable but judge-rejected) has
identical protocols; attributing causality to any                             the unconstrained target:
single operator requires careful per-instance in-
                                                                                     (∃µ, · · · ∧ ∀s, t ∈ R, |f (s) − f (t)| ≤ µ(|s − t|)) ↔ UniformContinuous f
spection. Empirically, these disagreements are
consistent with a mixture of direct trigger effects                           whereas the successful no-EvolAST semantic-
(duplicates/compile-fail fallbacks), indirect trajec-                         repair output explicitly restricts the bound to s, t ∈
tory effects, and dataset-dependent operator behav-                           [a, b] and targets uniform continuity on the interval:
ior.                                                                                 (∃µ, · · · ∧ ∀s, t, s ∈ Icc a b → t ∈ Icc a b → |f (s) − f (t)| ≤ µ(|s − t|))
                                                                                     ↔ UniformContinuousOn f (Icc a b)
Representative         example        (problem
0142_exercise_4_15a). In        this   instance,                              This illustrates a fundamental limitation of a con-
the main configuration produced many compilable                               servative type-rewrite operator: our EvolAST rule
set is limited to the existing binder and goal AST,      both are evaluated. All metrics normalize by the
so new problem-specific binders (e.g., explicit a, b     fixed budget T per problem; any early termination
interval parameters) and new domain-restriction          or failed call is treated as a consumed call with
hypotheses require LLM repair. Therefore, when           Comp(c) = 0 and Sem(c) = 0.
the current parent trajectory has not yet reached a
                                                         Parent selection. Parent selection uses the usage-
semantically correct “skeleton”, applying EvolAST
                                                         penalized robust weighting described in Section 3.
tends to preserve the same semantic mistake, pro-
                                                         For completeness, each archived candidate ci has
ducing many feasible variants that remain judge-
                                                         gate score si = Comp(ci )(1+Sem(ci )) and parent-
rejected. This effect is amplified by our implemen-
                                                         usage count ni . Within the selected island, we set
tation choice that EvolAST candidates terminate
                                                         zi = (si − m)/d, where m = medianj (sj ) and
the fallback path to keep accounting bounded, leav-
                                                         d = max(MAD({sj }j ), 10−6 ). The quality factor
ing later semantic correction to subsequent LLM
                                                         is Qi = σ(λzi ), the reuse factor is Ri = [1 +
proposals.
                                                         (1 + β)ni ]−1 , and the
                                                                              P next parent is sampled with
Takeaway. Online diversity operators can have            probability Qi Ri / j Qj Rj . Here MAD(A) =
dataset-dependent effects on semantic hit rates un-      mediana∈A |a − median(A)|, 10−6 is a numerical
der a fixed budget. In practice, this motivates tun-     stabilizer, and Ri discourages repeatedly selecting
able EvolAST rule sets, tunable trigger conditions,      the same parent.
and transparent ablation reporting.
                                                         Algorithm E.1 FormalEvolve (per problem; de-
EvolAST rewrite surface. In our experiments,             tailed)
EvolAST is used in its rule-based mode: it applies
                                                           Input: informal statement x, generator-call budget T ,
a bounded sequence of conservative, semantics-             seed model Mseed , patch model Mpatch , predicates
intended AST rewrites to the theorem type (binder          Comp, Sem, islands K
                                                           Output: feasible archive ∪I AI partitioned into islands
types and goal type), keeping the proof body un-           t ← 0; A1:K ← (∅, . . . , ∅)
changed. The rewrite surface is intentionally con-         (A1:K , t) ← I NIT S EEDS(x, Mseed , T, K; Comp, Sem)
trolled and includes conservative hypothesis re-               (debits budget; compiles/judges seeds; inserts feasible
                                                           seeds into islands)S
ordering; commutativity/associativity/distributivity       while t < T and I AI ̸= ∅ do
for conjunction/disjunction (Lean: ∧/∨); symme-              I ← S AMPLE I SLAND({I : AI ̸= ∅}) (uniform over
try swaps (e.g., a = b to b = a, P ↔ Q to                    nonempty islands)
                                                             p ← S AMPLE PARENT(AI ); np ← np + 1
Q ↔ P ); and dual relations (e.g., a < b to b > a,           (Iarch , Itop ) ← S AMPLE C ONTEXT(AI , p)
a ≤ b to b ≥ a).                                             c ← P ROPOSE(p, Iarch , Itop , x; Mpatch )
                                                             t←t+1
E     Algorithm, Budget Accounting, and                      c ← E NFORCE(c, p)             (preamble/proof protocol)
                                                             if I S E XACT D UPLICATE(c, AI ) then
      Configuration                                             crep ← E VOL AST(p)               (generator-call-free
                                                                representative)
We give the detailed per-problem search proce-                  P ROCESS C ANDIDATE(crep , x, p, AI , t, false) (no
dure, generator-call accounting rules, semantic-                semantic repair)
judge overhead, and implementation configuration             else if C OMPILES(c) then
                                                                P ROCESS C ANDIDATE(c, x, p, AI , t, true)
used in the fixed-budget experiments.                        else
                                                                crep ← E VOL AST(p) (compile-fail representative;
E.1    Detailed Pseudocode                                      no call)
                                                                P ROCESS C ANDIDATE(crep , x, p, AI , t, false)
Accounting conventions. Under fixed-budget ac-                  if t < T then
counting, we debit only generator-side LLM calls                    cfix ← CR EPAIR(c, x; Mpatch ); t ← t + 1
(proposals and bounded repairs). EvolAST is a                       cfix ← E NFORCE(cfix , p)
                                                                    P ROCESS C ANDIDATE(cfix , x, p, AI , t, true)
symbolic fallback triggered on (i) exact duplicates             end if
after canonicalization and (ii) compilation failures;        end if
                                                             M AYBE M IGRATE(A1 , . . . , AK )        (periodic island
it does not consume generator-call budget and is             migration; see Section E.3)
evaluated as the representative candidate of the trig-     end while
gering call. Each compilation-repair or semantic-
repair attempt is itself a debited generator call
whose representative candidate is the repaired out-
put; semantic repair preserves the original compil-
able candidate and appends a repaired variant, and
Table 18: Strict generator-call budget audit (call currency). Budget is fixed to N × T with T = 100 per problem;
Gen/CRep/SRep partition the same budget.
                               Dataset       Method                          Budget    Gen    CRep   SRep
                               CombiBench    Sample                          10000    10000      0      0
                               CombiBench    Compile Repair                  10000     7031   2969      0
                               CombiBench    C+S Repair                      10000     4257   1991   3752
                               CombiBench    Hybrid control                  10000     4081   1855   4064
                               CombiBench    FormalEvolve                    10000     4895   3042   2063
                               CombiBench    FormalEvolve w/o EvolAST        10000     5139   3428   1433
                               CombiBench    FormalEvolve w/o patch repair   10000    10000      0      0
                               ProofNet      Sample                          18600    18600      0      0
                               ProofNet      Compile Repair                  18600    13881   4719      0
                               ProofNet      C+S Repair                      18600    10732   3987   3881
                               ProofNet      Hybrid control                  18600    10887   3700   4013
                               ProofNet      FormalEvolve                    18600    11872   4903   1825
                               ProofNet      FormalEvolve w/o EvolAST        18600    11984   4887   1729
                               ProofNet      FormalEvolve w/o patch repair   18600    18600      0      0


Algorithm E.2 P ROCESS C ANDIDATE (compile
gate, judge, and bounded semantic repair)
  Input: candidate c, informal statement x, parent p, current
  island archive AI , call counter t, allow semantic repair flag
  r ∈ {true, false}
  Effect: if c is feasible, evaluates Sem(c) and inserts into
  AI ; if Sem(c) = 0 and r = true, spends one additional
  generator call on bounded semantic repair and evaluates
  the repaired candidate
  if C OMPILES(c) then
     m ← E VALUATE(c, x)                      (semantic judge)
     AI ← I NSERT(AI , (c, m))            (Comp(c) = 1 only)
     if r ∧ Sem(c) = 0 ∧ t < T then
        c′ ← SR EPAIR(c, x; Mpatch ); t ← t + 1
        c′ ← E NFORCE(c′ , p)
        if C OMPILES(c′ ) then
           m′ ← E VALUATE(c′ , x)
           AI ← I NSERT(AI , (c′ , m′ ))
        end if
     end if
  end if


E.2   Budget Audit and Evaluation Overhead
Generator-side. We audit generator-call usage
under the budget currency (T = 100 calls per prob-
lem). We decompose the fixed budget N × T into
generation calls (Gen), compilation-repair calls
(CRep), and semantic-repair calls (SRep). Table 8
provides a complementary per-problem distribu-
tional view (median/IQR) of CRep/SRep under the
same accounting.
Evaluator-side (semantic judge). We report
evaluator overhead in terms of semantic LLM-
as-judge calls (CriticLean-Qwen3-14B). In this
pipeline, semantic judging is invoked only after
successful compilation, and EvolAST outputs are
judged under the same gate; EvolAST-Judge is
the subset of judge calls attributed to EvolAST-
labeled candidates (generator-call-free on the gen-
erator side).
Table 19: Semantic judge overhead (CriticLean-Qwen3-14B). JudgeCalls counts how many compilable candidates
reach semantic checking; EvolAST-Judge is the EvolAST-attributed subset and is included in JudgeCalls.
                        Dataset       Method                          Problems   JudgeCalls   EvolAST-Judge
                        CombiBench    Sample                              100         6953               0
                        CombiBench    Compile Repair                      100         5513               0
                        CombiBench    C+S Repair                          100         6109               0
                        CombiBench    FormalEvolve                        100         4970             863
                        CombiBench    FormalEvolve w/o EvolAST            100         3800               0
                        CombiBench    FormalEvolve w/o patch repair       100         9025            3797
                        ProofNet      Sample                              186        13062               0
                        ProofNet      Compile Repair                      186        11624               0
                        ProofNet      C+S Repair                          186        11904               0
                        ProofNet      FormalEvolve                        186        10536             331
                        ProofNet      FormalEvolve w/o EvolAST            186        10103               0
                        ProofNet      FormalEvolve w/o patch repair       186        13465            1008


Table 20: Complete test-time accounting for the methods in Figure 5. All methods use T =100 generator calls
per problem. G/C/S partitions generation, compilation-repair, and semantic-repair calls; Judge [E] gives total
semantic-judge calls with the EvolAST-attributed subset in brackets; TC@64 is theorem-complete@64. Batch h
reports the recorded end-to-end batch duration.
 Dataset      Method              SH@100       TC@64                     G/C/S         Judge [E]     Lean eval. Records    Batch h
 CombiBench   Sample                 0.440      8/100             10,000/0/0            6,953 [0]        10,000   10,000      6.57
 CombiBench   C+S Repair             0.460      8/100      4,257/1,991/3,752            6,109 [0]        10,000    7,790      7.22
 CombiBench   Hybrid control         0.530      9/100      4,081/1,855/4,064            3,881 [0]         6,679    6,701      8.18
 CombiBench   FormalEvolve           0.580     13/100      4,895/3,042/2,063         4,970 [863]          8,891    9,011      8.16
 ProofNet     Sample                 0.715     41/186         18,600/0/0   13,062 [0]                    18,600   18,600    15.53
 ProofNet     C+S Repair             0.780     46/186 10,732/3,987/3,881   11,904 [0]                    18,600   14,684    18.25
 ProofNet     Hybrid control         0.828     40/186 10,887/3,700/4,013   10,565 [0]                    14,167   14,538    20.77
 ProofNet     FormalEvolve           0.849     45/186 11,872/4,903/1,825 10,536 [331]                    14,376   14,568    17.29


E.3   Configuration and hyperparameters                                    between islands (rate 0.1), while protecting
Table 21 summarizes the key hyperparameters used                           the top-1 elite in each island.
in the main experiments.
Lean 4 toolchain and library. All candidates are
compiled under Lean 4.15.0 with Mathlib (import
Mathlib). We use Mathlib4 v4.15.0 (commit
9837ca9) as bundled by our Kimina Lean Server
installation. Compilation is served by Kimina Lean
Server (Dos Santos et al., 2025), which provides
a pinned Lean 4/Mathlib environment suitable for
large-scale batch checking.
Implementation notes: archive and island me-
chanics.

   • Global feasible archive. We maintain a
     global compilation-feasible archive (capacity
     40); selection is applied only within this feasi-
     ble set.

   • Island-local behavior. Parent selection and
     cross-patch inspirations are restricted to the
     sampled island (via island_idx); children
     inherit the parent island by default.

   • Migration. Every 10 generations, we mi-
     grate a small fraction of feasible candidates
                                  Table 21: Key hyperparameters used in FormalEvolve.
    Component                     Setting
    Models                        Seed: Kimina-Autoformalizer-7B; patch/repair: Qwen3-30B-A3B.
    Compilation                   Lean 4.15.0 + Mathlib via Kimina Lean Server (Dos Santos et al., 2025).
    Semantic judge                CriticLean-Qwen3-14B (LLM-based judge; proof ignored).
    Islands                       2
    Island separation             enabled; parent selection and inspirations restricted to the sampled island
    Archive invariant             compilation-feasible (compile_ok= 1)
    Archive size                  global capacity 40 (compilation-feasible)
    Migration policy              interval 10 gens, rate 0.1; moves feasible gen> 0 candidates; elitism (top-1 protected)
    Parent selection              weighted (λ = 10) with usage penalty β = 0.05
    Operator mix (default)        full/diff/cross with probs 0.5/0.3/0.2
    Patch attempts                max patch attempts 1 (per step)
    Inspiration pool              per step: 4 archive inspirations + 2 top-k inspirations (when available)
    Cross prompt inspirations     samples k = 1 inspirations uniformly from the pool
    Repair budget                 max attempts 2, temperature 0.7 (applies to compile + semantic repair)
    EvolAST fallback              enabled as a fallback for (i) exact-duplicate edits, and (ii) compilation failures (evaluated as
                                  a generator-call-free fallback alongside bounded compile repair)

                                    Table 22: Prompt components used in our pipeline.
Component                       Model                    Purpose / output constraints
Initial generation              Mseed              Produce one Lean 4 file with a single theorem statement (:= by sorry).
Operators (full/diff/cross)     Mpatch             Edit-conditioned rewrite of a parent; cross additionally conditions on
                                                   one inspiration from the archive.
Compile repair (bounded)        Mpatch             Minimal patch conditioned on compiler feedback; debited within the
                                                   same call budget.
Semantic repair (bounded)       Mpatch             Revision conditioned on the informal statement and judge feedback;
                                                   debited within the budget.
Semantic judge                  CriticLean-Qwen3-1 Binary verdict on statement faithfulness (proof ignored), returned as
                                4B                 JSON (Correct/Incorrect plus a short rationale).
Prover                          Goedel-Prover-V    Complete a Lean file by replacing the placeholder proof under a fixed
                                2-32B              prover prompt.


F     Prompting and Semantic-Judge
                                                                      You are an expert in Lean 4 theorem proving and Mathlib.
      Protocol
                                                                      Given a problem statement in natural language, write a
We report the prompt templates used for initial                       COMPLETE Lean 4 file (imports + theorem)
                                                                      that formalizes the mathematical content.
statement generation, evolution operators, bounded
                                                                      MANDATORY OUTPUT REQUIREMENTS:
repair, semantic judging, and downstream proof                        - Output EXACTLY ONE Lean 4 code block: ```lean ... ```.
                                                                      - The code MUST start with the following two lines (in this
completion. We show the full prompt skeletons be-                     order):
cause prompt details affect both reproducibility and                    import Mathlib
                                                                        import Aesop
the reliability of LLM-as-judge semantic labels.                      - You MAY add additional `import ...` / `open ...` /
                                                                      `set_option ...` lines after that if needed (unless a
                                                                      mode-specific prefix locks the header, e.g., diff mode).
Notation. Placeholders          include        {in-                   - Do NOT include any comments.
                                                                      - Include EXACTLY ONE `theorem` declaration.
formal}        (natural-language       statement),                    - The theorem MUST end with `:= by sorry` (do not provide a
{code_content} (current Lean file), {perfor-                          proof).
                                                                      - Use Lean 4 v4.15-compatible syntax and Mathlib definitions.
mance_metrics} (compile/semantic metrics),
                                                                      Natural language statement:
{text_feedback_section} (optional judge feedback),                    {informal}
{original_code} (candidate file for repair), {com-                    Return ONLY the Lean 4 code block.
pile_error_type}/{compile_error_msg} (compiler
feedback), {critic_feedback} (semantic-judge                         F.2    Evolution operators (full / diff / cross)
feedback), {inspiration_code_1} (cross inspira-
tion), and {lean_statement} (theorem statement                       Shared prompt skeleton.
for judging). For pdfLaTeX compatibility, we                          You are an expert in Lean 4 theorem proving and the Mathlib
                                                                      library.
render common Lean unicode symbols in ASCII                           Your task is to improve a Lean 4 formalization for a given
in verbatim displays.                                                 natural language mathematical claim.

                                                                      Hard requirements (must satisfy all):
F.1      Statement generation (initial)                               - Output a COMPLETE Lean 4 file (imports + exactly one
                                                                      theorem) in a single ```lean``` code block.
Prompt template.                                                      - The code MUST start with these two lines (in this order):
  import Mathlib                                              F.3   Bounded repair prompts
  import Aesop
- You MAY add additional `import ...` / `open ...` /          Repairs count toward the generator-call bud-
`set_option ...` lines after that if needed.
- Do NOT include any comments.                                get. Compilation repair triggers only when
- Include EXACTLY ONE `theorem` declaration.
- The theorem MUST end with `:= by sorry` (do not provide a   compile_ok=0; semantic repair triggers only when
proof).
                                                              compile_ok=1 and semantic_ok=0.
Quality goals:
- compile_ok: The file compiles without errors.               Compilation repair prompt.
- semantic_ok: The theorem statement matches the informal
mathematical meaning.
                                                              You are an expert in Lean 4 theorem proving and Mathlib.
Natural language statement:                                   You are doing SYNTAX / COMPILATION REPAIR.
{informal}
                                                              You will receive:
Current Lean 4 program:                                       - A natural language statement (the semantic target)
```lean                                                       - A Lean 4 file that fails to compile
{code_content}                                                - Compiler error feedback
```
                                                              Your job:
Evaluation results:                                           - Produce a corrected Lean 4 file that compiles.
{performance_metrics}{text_feedback_section}
                                                              IMPORTANT:
Return ONLY the Lean 4 code block.                            - Fix compilation only; do NOT change the intended
                                                              mathematical meaning.
                                                              - Keep changes minimal (types, identifiers, imports, binder
                                                              annotations, etc.).
Full-mode addenda (sampled variants; one per
                                                              Natural language statement:
call).                                                        {informal}

(i) Default rewrite: revise types/hypotheses/structure as     Current Lean 4 code (does NOT compile):
needed.                                                       <CURRENT_CODE>
(ii) Different interpretation: try a different reasonable     {original_code}
formalization of the same claim.                              </CURRENT_CODE>
(iii) Type optimization: improve binder structure and
type-class constraints.                                       Compiler feedback:
(iv) Mathlib alignment: prefer standard Mathlib names and     - Error type: {compile_error_type}
definitions.                                                  - Error message:
(v) Simplification: if possible, state a simpler claim        ```
without changing meaning.                                     {compile_error_msg}
                                                              ```

                                                              Return exactly one Lean 4 code block, starting with `import
   Diff mode prepends a short local-edit instruction          Mathlib` and `import Aesop`,
                                                              with exactly one theorem ending in `:= by sorry`.
(still returning a full file), while cross mode addi-
tionally provides one sampled inspiration candidate
from the archive/top-k pool as extra context.
Diff-mode prefix (local edit).
You are doing a LOCAL EDIT of a Lean 4 formalization file.
Header lock (diff mode only):
- Do NOT add/remove/reorder/modify any preamble lines
(imports/opens/options).
- Keep everything before the `theorem` declaration EXACTLY
unchanged.
Goal:
- Make the smallest possible change to improve compilation
and formalization quality.
- Keep changes minimal; do NOT change the intended
mathematical meaning.



Cross-mode prefix (inspiration-guided).
You are doing CROSS patching.
You are given one inspiration candidate from the
archive/top-k pool as extra context.
Your task is to improve the current formalization by
optionally borrowing useful structure from the inspiration.



Cross-mode extra context (one per call).
[Inspiration candidate]
```lean
{inspiration_code_1}
```
Semantic repair prompt.                                        5. If correct, explain why the elements match; if incorrect,
                                                               list mismatches and their effect on correctness.
You are an expert in mathematics and Lean 4 (Mathlib).
                                                               Output Format:
You are doing SEMANTIC REPAIR.
                                                               Return exactly one JSON object:
                                                               {
You will receive:
                                                                 "reasons": "<your detailed analysis as a single string>",
- A natural language statement (the semantic target)
                                                                 "is_assistant_correct": "Correct or Incorrect"
- A Lean 4 file that is intended to formalize it
                                                               }
- Critic feedback (Accuracy Confirmation) describing
mismatches
                                                               Input Data:
                                                               -- Start of Mathematical_Text --
Your job:
                                                               {informal}
- Modify the Lean 4 code so that the theorem statement
                                                               -- End of Mathematical_Text --
matches the natural language statement.                        -- Start of Lean4Code --
                                                               {lean_statement}
Rules:                                                         -- End of Lean4Code --
- You MAY change hypotheses and the conclusion if needed to
match the semantics.
- You MAY adjust/add imports/opens/options as needed to keep
the file compiling.                                            F.5   Prover prompt (Goedel-Prover-V2-32B)
- Do NOT "solve" the task by weakening it to `True` or a
tautology.                                                     We evaluate downstream proof utility using a fixed
- Do NOT include any comments.
- Output a complete Lean 4 file starting with:                 prover configuration (Goedel-Prover-V2-32B) and
  import Mathlib
  import Aesop                                                 a fixed prompt template. The prompt asks the
- Include exactly one theorem, ending with `:= by sorry`.
                                                               prover to complete a Lean file by replacing the
Natural language statement:                                    placeholder proof.
{informal}

Current Lean 4 code:                                           Complete the following Lean 4 code.
<CURRENT_CODE>                                                 Return ONLY a complete Lean 4 file inside a ```lean4``` code
{original_code}                                                fence (no explanations): {lean_file}
</CURRENT_CODE>

Critic feedback (Accuracy Confirmation):
{critic_feedback}

Goal:
- Modify the Lean 4 theorem so that the semantic judge would
accept it as an exact formalization of the natural-language
statement.
- Address every mismatch mentioned in the Critic feedback.

Return exactly one Lean 4 code block, starting with `import
Mathlib` and `import Aesop`,
with exactly one theorem ending in `:= by sorry`.


F.4   Semantic judge prompt
      (CriticLean-Qwen3-14B)
We use CriticLean-Qwen3-14B as the LLM-as-
judge implementation of Sem, judging semantic
consistency between the natural-language state-
ment and the Lean 4 theorem statement (proof ig-
nored). The prompt template below is used for
each semantic check.
Role: Lean 4 & Formal Verification Expert
Input:
- Mathematical_Text: A math problem and its answer (no
proof).
- Lean4Code: A Lean 4 theorem statement formalizing the
problem (proof intentionally omitted).
Goal:
Determine if the Lean 4 theorem statement is an exact and
faithful formalization of the mathematical problem.
Do not evaluate or consider the answer or the proof. Your
sole task is to verify the correctness of the formalization.

Evaluation stages:
1. Identify the mathematical claim: variables, types,
quantifiers, assumptions, constraints, logic structure, and
conclusion.
2. Extract the corresponding components from the Lean 4
statement, ignoring the proof.
3. Compare the two statements for semantic alignment,
quantifier correctness, preserved constraints/boundaries,
correct typing, syntactic validity, and absence of semantic
drift or unjustified additions.
4. Give the final judgment using only what is explicitly
expressed in the Lean statement, not the proof.
