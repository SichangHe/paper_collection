                                                           ITPE VAL: Benchmarking Formal Translation Across
                                                                      Interactive Theorem Provers


                                                                     Jiayi Wu 1 Robert Joseph George 2 Anima Anandkumar 2


                                                               Abstract                                       evaluation pipelines2 are publicly released.
                                            Formal theorem proving has emerged as a frontier
                                            challenge for machine learning, yet the ecosys-            1. Introduction
                                            tem is fragmented: proofs remain siloed across
                                            incompatible systems, limiting both training data          Formal mathematics has become an increasingly important
                                            for learning-based provers and the portability of          domain for AI research: large language models now achieve
                                            verified results. We present ITPE VAL, the first           strong results on automated theorem proving (Polu et al.,
                                            benchmark for evaluating automated formal proof            2022; Yang et al., 2023; First et al., 2023; Xin et al., 2024),
                                            translation across four major ITPs (Lean 4, Rocq,          autoformalization (Wu et al., 2022; Jiang et al., 2023b), and
arXiv:2607.19407v1 [cs.AI] 7 Jul 2026




                                            Isabelle, and HOL Light), spanning two distinct            mathematical reasoning more broadly. Yet while proving
                                            logical foundations. Our benchmark comprises               and autoformalization have been extensively researched and
                                            1,560 source files and 6,848 theorems organized            benchmarked, the formal ecosystem remains fragmented:
                                            into a controlled tier of axiomatized files that           each interactive theorem prover (ITP) implements its own
                                            isolates foundational translation difficulty, and          logical foundation, tactic language, and mathematical li-
                                            an ecosystem tier drawn from real libraries that           brary, and interoperability between systems has been largely
                                            exposes API and proof-style mismatches. We                 overlooked.
                                            release itpeval, a unified multi-ITP verifica-
                                                                                                       This fragmentation brings various consequences: a the-
                                            tion infrastructure with state-isolated warm back-
                                                                                                       orem proved in Lean’s Mathlib (mathlib Community,
                                            ends that preserve per-artifact native checking se-
                                                                                                       2020) cannot be invoked in Isabelle’s Archive of For-
                                            mantics. We evaluate both statement and proof
                                                                                                       mal Proofs (Archive of Formal Proofs, 2026), even when
                                            translation across five frontier and open-weight
                                                                                                       both encode the same mathematics. Cross-ITP transla-
                                            LLMs on 12 directed translation pairs: statement
                                                                                                       tion, the task of converting formal proofs between sys-
                                            translation peaks at 29.1% pass@1 and proof
                                                                                                       tems while preserving correctness, would address this in
                                            translation at 10.5%; controlled theorems reach
                                                                                                       two ways. First, it would let verified results transfer
                                            29.7% proof pass@1 versus 5.2% for ecosystem-
                                                                                                       across ITP ecosystems, reducing duplicate formalization
                                            level translations, indicating that library mis-
                                                                                                       effort and expanding the training data available to learning-
                                            match is the largest observed source of proof-
                                                                                                       based provers. Second, it would inform autoformaliza-
                                            translation failure. In addition to pass@k eval-
                                                                                                       tion and auto-informalization, since both settings require
                                            uation, a deterministic Lean 4 BEq check estab-
                                                                                                       preserving theorem meaning across different surface lan-
                                            lishes equivalence for 54.0% of verified source 7→
                                                                                                       guages and libraries. We therefore also evaluate a round-
                                            Lean 4 miniF2F statement translations, showing
                                                                                                       trip autoformalization/auto-informalization setting in which
                                            that native type-checking alone can substantially
                                                                                                       multi-ITP context is used during generation.
                                            overestimate semantic fidelity; an exploratory
                                            autoformalization/auto-informalization round-trip          Despite this importance, cross-ITP translation has received
                                            study suggests target-dependent verification pat-          little systematic study. While formalization tracking efforts
                                            terns and possible benefits from multi-ITP context.        such as Formalizing 100 Theorems (Wiedijk, 2008) and
                                            Our benchmark1 , verification infrastructure, and          the 1000+ Theorems project (1000+ Theorems Contribu-
                                        1
                                                                                                       tors, 2026) catalog which classical results have been proved
                                         Brown University 2 California Institute of Technology.
                                                                                                       in which provers, and interoperability frameworks such as
                                        Correspondence to: Jiayi Wu <jiayi wu4@brown.edu>.
                                        The 3 rd AI for Math Workshop at the 43 rd International
                                                                                                       Dedukti (Assaf et al., 2023; Dowek & Thiré, 2023) en-
                                        Conference on Machine Learning (ICML), 2026. Copyright         able proof exchange via shared intermediate representations,
                                        2026 by the author(s).                                         none of these provide evaluation benchmarks for measur-
                                         1
                                           Data: jiayi005/ITPEval.
                                                                                                          2
                                                                                                              Code: lean-dojo/ITPEval.

                                                                                                   1
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers




Figure 1. Overview of ITPEval. The figure summarizes the cross-ITP translation setting, natural-language round-trip tasks, and the
unified state-isolated verification infrastructure.


ing translation quality. Without standardized benchmarks,             tomation behavior, and proof-style differences. This tiered
it is difficult to measure whether LLM-based or symbolic              structure quantifies the additional cost of library and proof-
translation methods produce correct, idiomatic output, or to          engineering dependencies beyond foundation-level transla-
identify which system pairs and proof features remain out             tion. Our contributions are:
of reach.
Constructing such a benchmark is itself non-trivial: each             • A four-way aligned cross-ITP benchmark with 1,560
ITP community has developed its library largely indepen-                source files and 6,848 theorems and lemmas across Lean 4,
dently, so no large aligned corpus of proofs exists across              Rocq, Isabelle, and HOL Light. The benchmark yields
systems, and even theorems that have been formalized in                 12 directed translation pairs and is organized into a con-
multiple ITPs typically differ in proof structure, lemma de-            trolled tier (64 axiomatized files, 660 lemmas) and an
pendencies, and library APIs. The only existing benchmark               ecosystem tier (232 Formalizing 100 Theorems files and
is Babel-formal (Stoskopf et al., 2025), limited to 14 aligned          1,264 miniF2F statements).
files between Lean and Rocq. Evaluation methodology is                • A unified multi-ITP client and verification infrastruc-
itself an open problem: type-checking alone has a high false-           ture that exposes heterogeneous theorem provers through
positive rate for semantic correctness (Poiroux et al., 2025;           a common evaluation interface with environment-keyed
Liu et al., 2025b), and code translation benchmarks (Yan                scheduling, state-isolated warm backends, and per-artifact
et al., 2023; Zheng et al., 2024) usually apply only partially          diagnostics.
since ITP translation must navigate logical foundation dif-
ferences, not just syntactic ones. These gaps motivate a              • A systematic evaluation of closed-source and open-
benchmark that jointly addresses cross-system coverage and              weight LLMs on statement and proof translation. We
foundation-aware evaluation.                                            evaluate GPT-5.5, Claude Sonnet 4.6, Gemini 3.1 Pro,
                                                                        DeepSeek-V4-Pro, and Qwen3-235B-A22B, with every
We present ITPE VAL, a benchmark and unified multi-ITP
                                                                        output checked by the native target prover rather than by
verification infrastructure for studying formal translation
                                                                        surface-level heuristics.
across major theorem-prover ecosystems. ITPEval spans
Lean 4, Rocq, Isabelle, and HOL Light, covering both de-              • An exploratory autoformalization and auto-
pendent type theory and higher-order logic. Its design sep-             informalization round-trip study showing target-prover
arates two sources of difficulty: a controlled tier of self-            effects and suggesting that multi-ITP context can affect
contained, axiomatized files that isolates foundational trans-          downstream formalization success.
lation issues, and an ecosystem tier of real library formaliza-
tions that exposes API mismatches, naming conventions, au-            • A Bidirectional Extended Definitional Equivalence
                                                                        check (BEq) that tests whether verified translations pre-

                                                                  2
                                         ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 1. Positioning of ITPE VAL. A = aligned data, B = bench-                                     Evaluation interfaces. Target-prover checking is neces-
mark, N = target-prover checking, U = unified verifier. ● = central
or supported, ◆ = partial or limited, ❍ = not a focus.
                                                                                                   sary for formal translation, but type checking alone does not
                                                                                                   guarantee semantic fidelity (Poiroux et al., 2025; Liu et al.,
Work                             Systems                A   B   N   U   Role
                                                                                                   2025b). Existing interfaces such as LeanDojo, Pantograph,
Interoperability and overlap
Formalizing 100 Theorems /        Many ITPs             ◆   ❍   ❍   ❍   Overlap catalogues         PISA, and itp-interface support interaction with indi-
1000+ Theorems (Wiedijk, 2008;
1000+ Theorems Contributors,
2026)
                                                                                                   vidual provers or small prover sets (Yang et al., 2023; Aniva
Dedukti / Logipedia /
EuroProofNet (Assaf et al., 2023;
                                  Many logics           ◆   ❍   ◆   ◆   Proof exchange             et al., 2025; Jiang et al., 2021; Thakur et al., 2025b). ITPE-
Dowek & Thiré, 2023; Thiré,
2020)                                                                                              VAL instead contributes a unified, state-isolated multi-ITP
OpenTheory (Hurd, 2011)           HOL family            ◆   ❍   ◆   ◆   HOL packages
Formal translation and autoformalization
                                                                                                   verifier for benchmark-scale evaluation across Lean 4, Rocq,
Babel-formal (Stoskopf et al.,
2025)
                                 Lean, Rocq             ●   ●   ●   ❍   Two-prover benchmark       Isabelle, and HOL Light. Appendix D gives a more detailed
MiniF2F in Rocq (Viennot et al., Lean, Isabelle, Rocq
2025)
                                                        ◆   ◆   ●   ❍   Rocq statement port
                                                                                                   comparison.
MMA (Jiang et al., 2023a)        Lean, Isabelle         ◆   ❍   ◆   ❍   NL–formal data
ProofWala (Thakur et al., 2025a) Lean, Coq/Rocq         ◆   ❍   ●   ◆   Proof search
KELPS (Zhang et al., 2025)       Lean, Coq/Rocq,        ◆   ❍   ◆   ❍   Autoformalization


Interfaces and analogues
                                 Isabelle
                                                                                                   3. Benchmark Design
LeanDojo / Pantograph / PISA / One or two provers       ❍   ❍   ◆   ◆   Prover interfaces
itp-interface (Yang et al.,
2023; Aniva et al., 2025; Jiang
                                                                                                   A benchmark for cross ITP translation must separate several
et al., 2021; Thakur et al., 2025b)
CodeTransOcean / HumanEval-X Programming                ●   ●   ◆   ❍   Code translation           sources of difficulty. Some failures come from differences
/ CRUXEval-X (Yan et al., 2023; languages
Zheng et al., 2024; Xu et al.,                                                                     in logical foundations, such as dependent type theory versus
2025)
ITPE VAL                         Lean 4, Rocq,          ●   ●   ●   ●   Four-way benchmark +
                                                                                                   higher order logic. Others come from prover ecosystems:
                                 Isabelle, HOL Light                    verifier
                                                                                                   library APIs, naming conventions, automation, local helper
                                                                                                   lemmas, and proof idioms. ITPE VAL is designed to expose
                                                                                                   these effects separately, while evaluating both statement
   serve theorem meaning, implemented for Lean 4 targets.
                                                                                                   translation and full proof translation.
   Applied to miniF2F statement translations, 174 of 322
   verified source 7→ Lean 4 translations (54.0%) pass BEq;
   the remaining 46.0% expose either semantic drift or limi-                                       Tier A: controlled files. Tier A contains self-contained,
   tations of the restricted equivalence search.                                                   axiomatized files. These files include their own definitions
                                                                                                   and assumptions, and avoid dependence on prover-specific
                                                                                                   libraries. They are intended to isolate foundational and
2. Related Work                                                                                    language-level translation issues, such as type theory, quan-
                                                                                                   tification, implicit arguments, universe conventions, and
Formal systems. ITPE VAL spans two major proof-
                                                                                                   proof syntax.
assistant traditions. Lean 4 (Moura & Ullrich, 2021) and
Rocq (Bertot & Castran, 2004) are based on the Calculus
of Inductive Constructions (CIC), while Isabelle/HOL (Nip-                                         Tier B: ecosystem files. Tier B contains formalizations
kow et al., 2002) and HOL Light (Harrison, 2009) are based                                         drawn from existing libraries and community developments.
on Higher-Order Logic (HOL). Translation difficulty is not                                         These files reflect real proof engineering practice: they use
determined by foundation alone: tactic languages, proof id-                                        library lemmas, local helper definitions, tactic automation,
ioms, libraries, automation, and naming conventions differ                                         naming conventions, and prover-specific mathematical struc-
even within the same logical family.                                                               tures. They therefore test the combined difficulty of trans-
                                                                                                   lating both the mathematics and the surrounding ecosystem.
Prior work. Prior work has tracked theorem coverage                                                This two-tier design makes the main analysis interpretable.
across provers and built proof-exchange infrastructure, but                                        Performance on Tier A measures how well models handle
has not provided a balanced four-way benchmark for cross-                                          controlled cross-system translation, while the gap between
ITP translation. Formalization trackers record overlap                                             Tier A and Tier B measures the additional cost of real prover
across systems (Wiedijk, 2008; 1000+ Theorems Contribu-                                            ecosystems.
tors, 2026), while Dedukti, Logipedia, EuroProofNet, and
OpenTheory provide proof exchange infrastructure (Assaf                                            3.1. Data Sources and Selection
et al., 2023; Dowek & Thiré, 2023; Thiré, 2020; Hurd, 2011).
Babel-formal (Stoskopf et al., 2025) is the closest prior                                          A central design constraint is the four-way intersection
benchmark, but covers Lean and Rocq only. Recent multi-                                            requirement: every file in the benchmark must be formal-
lingual autoformalization and proof-search systems study                                           ized in all four ITPs. This ensures that every source–target
natural language to formal translation or two-prover proof                                         pair is evaluated on exactly the same theorems, enabling
search, rather than balanced formal-to-formal translation                                          clean directional and foundation-pair comparisons without
across four ITPs (Jiang et al., 2023a; Thakur et al., 2025a;                                       missing-data confounds. We exclude files where a formal-
Zhang et al., 2025).                                                                               ization is unavailable in any of the four ITPs, where the
                                                                                                   source fails to compile in its native prover, or where theo-

                                                                                               3
                       ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

rem identity is ambiguous across systems.                               more tractable and directly diagnostic of whether models
                                                                        can encode the same theorem across type-theoretic and def-
Babel-formal (Tier A, 16 aligned items; 64 files; 660
                                                                        initional boundaries, without confounding this with proof-
lemmas). We adopt and extend the Babel-formal bench-
                                                                        search difficulty.
mark (Stoskopf et al., 2025) from its original 14-file Lean–
Rocq scope to all four ITPs, re-formalizing each item in                Statement translation (stmts). Given a source file with
Isabelle and HOL Light and adding 2 new items formal-                   all proof bodies replaced by placeholders (e.g., sorry),
ized in all four systems from inception. Alignment is exact:            produce the corresponding file in the target ITP, also with
we authored all four versions ourselves. Each item is a                 placeholder proofs. Verification checks that the generated
self-contained axiomatized theory (2–19 lemmas per prover-              file type-checks in the target system; for multi-lemma files
specific file) covering order theory, group theory, topology,           (Babel-formal, Formalizing 100 Theorems), all statements
and analysis. The axiomatized design isolates type-theoretic            in the file must type-check together.
translation difficulty (dependent types, universe levels, im-
                                                                        Proof translation (proofs). Given a complete proof file
plicit arguments) from library API mismatches.
                                                                        in the source ITP, produce a complete, compilable proof
Formalizing 100 Theorems (Tier B, 58 aligned items;                     file in the target ITP. Verification requires that the entire
232 files; 4,924 lemmas). From Wiedijk’s 100 classical the-             generated file compiles without errors and with no sorry
orems (Wiedijk, 2008), we retain the 58 with formalizations             placeholders; for multi-lemma modules, every lemma must
publicly available in all four ITPs, aligned by√canonical list          be fully proved.
number (e.g., Theorem 1 = irrationality of 2). Because
each prover’s formalization was developed independently                 3.3. Infrastructure
by its community, stylistic differences are genuine. Formal-
izations are sourced from Mathlib 4 for Lean 4 (mathlib                 A substantial part of building ITPE VAL was designing a
Community, 2020); the Rocq standard library, MathComp,                  scalable verification infrastructure, not merely collecting
and Rocq community libraries for Rocq (The Mathematical                 aligned formalizations. Cross ITP evaluation is only mean-
Components Team, 2015; CoRN Contributors, 2011; Madiot                  ingful if generated artifacts are checked by the target prover
& Chardard, 2026; Niqui & Bertot, 2004; Guilhot & Pham,                 itself under conditions that faithfully reflect standalone veri-
2016; Allais et al., 2020; Rocq Archive, 2016; de Rauglau-              fication. We refer to this as native target-prover checking.
dre, 2017; Loiko, 2022; Ekdohibs, 2014); Isabelle and the               For this reason, all labels in ITPE VAL are produced by the
Archive of Formal Proofs for Isabelle/HOL (Nipkow et al.,               actual target ITP. A translation is counted as verified only
2002; Archive of Formal Proofs, 2026); and HOL Light’s                  when the target prover accepts the entire generated file with
core theories for HOL Light (Harrison, 2009). Each transla-             exit code 0. Partial files, later declaration failures, and proof
tion unit is the entire source file, including the headline theo-       mode outputs containing placeholders are all counted as
rem plus supporting lemmas and auxiliary definitions (mean              failures. For every artifact, the verifier records the final
21 lemmas per file, range 1–95), reflecting realistic trans-            verdict, diagnostics, wall clock time, backend identity, and
lation scenarios where proofs depend on locally-defined                 environment metadata.
helpers.                                                                The main systems challenge is that the target provers have
MiniF2F (Tier B, 1,264 single-theorem files, state-                     very different execution models. Lean 4 and Rocq can be
ments only). The competition mathematics benchmark                      checked relatively directly, but Isabelle and HOL Light have
miniF2F (Zheng et al., 2022) provides formalized prob-                  much heavier startup and session costs. Isabelle verification
lem statements across Lean, Isabelle, and HOL Light;                    is organized around sessions and theory files, while HOL
we use the Rocq port of MiniF2F (Viennot et al., 2025)                  Light runs through an OCaml-based environment whose ini-
and retain the 316 problems formalized in all four sys-                 tialization can dominate small checks. Treating each prover
tems, aligned by standardized problem identifier (e.g.,                 as a separate script would make evaluation fragile, difficult
amc12a 2008 p25). Each file contains exactly one theo-                  to restart, and hard to compare across targets. We therefore
rem statement. MiniF2F complements Formalizing 100 The-                 release itpeval, a unified multi-ITP client and toolchain
orems: its single-statement files test pure statement trans-            manager. It installs and runs all four proof assistants behind
lation without multi-lemma structure, and its competition-              a common run itp() entry point: each target prover is
math provenance provides diverse content (algebra, number               materialized in its own task directory, while prover-specific
theory, combinatorics) at controlled complexity.                        details remain localized to adapters.
                                                                        The central invariant is state isolation: every accelerated
3.2. Translation Tasks                                                  check must be observationally equivalent to verifying the
                                                                        generated artifact on its own. Figure 2 summarizes the
We evaluate two translation tasks, with statement trans-
                                                                        verifier. Generated JSONL records pass through strict one-
lation as the primary task. Statement translation is both

                                                                    4
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers




Figure 2. ITPE VAL verification infrastructure. Generated artifacts are filtered, cached, scheduled by environment, and checked by
prover-specific warm backends while preserving native per-file checking semantics.


sided filters, content-addressed caching, environment keys,           tactic sequences from an LLM under a restricted primitive
and cost-aware scheduling before entering a transactional             set. We keep the same bidirectional criterion and restricted-
CheckRequest/CheckResult API. The API then dis-                       primitive design, but replace LLM-sampled transformations
patches to prover-specific backends: Lean 4 checks fresh              with a deterministic Lean tactic cascade. This makes the
synthetic files, Rocq resets persistent REPL workers with             metric reproducible and avoids adding a second model-
Reset Initial., Isabelle checks temporary theories                    dependent source of variance to the translation benchmark.
inside server sessions, and HOL Light uses collision-aware            Appendix F gives the full protocol and failure analysis.
resident workers or a forkserver. Adaptive bisection re-
covers per-artifact labels after batch failures, append-only          4. Evaluation and Results
checkpoints make runs restartable, and telemetry records
diagnostics, backend provenance, and timing. These mecha-             4.1. Evaluation Setup
nisms are part of the experimental protocol: without them,
                                                                      We evaluate five zero-shot, greedy-decoded models (T =
warm workers can leak declarations across files, batched
                                                                      0): GPT-5.5, Claude Sonnet 4.6, Gemini 3.1 Pro Preview,
checking can lose pass@1 labels, and target-prover effects
                                                                      DeepSeek-V4-Pro, and Qwen3-235B-A22B. This set covers
can be confounded with verifier behavior.
                                                                      closed-source frontier models and large open-weight models.
                                                                      Direct translation is the primary setting: given a source
3.4. Semantic Equivalence Checking
                                                                      file and a target ITP, the model must emit only raw target
Target-prover type checking is necessary for correctness but          ITP code, with no markdown fencing or explanation. We
not sufficient for semantic fidelity: a translated statement          report pass@1 results: pass@1 is the fraction of translation
can type-check while expressing a weaker or shifted theo-             instances for which the single generated candidate verifies
rem (Poiroux et al., 2025; Liu et al., 2025b). To quantify this       under the target prover; more generally, pass@k counts an
gap, we adapt Bidirectional Extended Definitional Equiv-              instance as solved if any of k generated candidates verifies.
alence (BEq), introduced by Liu et al. (2025a), to verified
Lean 4 target translations. Given a generated Lean statement          4.2. Verification Throughput
G and the reference Lean statement R, BEq checks both
                                                                      The unified verifier is necessary in practice because target
entailments G ⊢ R and R ⊢ G; a translation passes BEq iff
                                                                      provers differ sharply in startup and checking cost. Ta-
both directions succeed.
                                                                      ble 2 reports wall clock time on 16 Babel-formal statement
Each directional check constructs a fresh Lean file by renam-         files. Lean 4 and Rocq already have modest cold checking
ing the assumed theorem to stmt assumed, renaming the                 costs, but still benefit from pooled or persistent workers.
goal theorem to beq goal, replacing the goal proof with               The largest gains occur for Isabelle and HOL Light, where
restricted proof search, and running Lean. Liu et al.’s orig-         startup and environment initialization dominate naive check-
inal implementation first tries exact? and then samples

                                                                  5
                                        ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 2. State preserving verifier backends and observed through-                                       Table 3. Statement translation pass@1 by benchmark. The
put on 16 Babel-formal statement files. Times are wall clock                                            Tier A/B gap persists, but miniF2F outperforms Formalizing 100
seconds; lower is better.                                                                               Theorems despite containing competition mathematics.

    Prover             Backend          Reuse                        Isolation        Cold Warm                                            Formalizing 100
                                                                                                            Model          Babel (A, 192) Theorems (B, 696) miniF2F (B, 3792)
    Lean 4    pool/server compiler workers fresh file         15.1   3.7
    Rocq      REPL pool persistent proc.      Reset            4.3   0.5                                    GPT-5.5           91 (47.4%)       106 (15.2%)      1163 (30.7%)
    Isabelle  server batch persistent session temp. theories 472.2   6.9                                    Gemini 3.1        63 (32.8%)        97 (13.9%)       496 (13.1%)
    HOL Light forkserver preloaded OCaml child exit          527.4 149.0                                    Claude 4.6        21 (10.9%)         32 (4.6%)        134 (3.5%)
                                                                                                            DeepSeek-V4       33 (17.2%)         46 (6.6%)      1190 (31.4%)
                     GPT-5.5                                                                29.1%
                                                                                                            Qwen3-235B         18 (9.4%)         10 (1.4%)       424 (11.2%)
             DeepSeek-V4-Pro                                                          27.1%
               Gemini 3.1 Pro                                14.0%
                 Qwen3-235B                     9.7%
                                                                                                        Table 4. Proof translation pass@1 rates on 888 directed pairs.
         Claude Sonnet 4.6          4.0%
                                                                                                        Tier A is consistently much easier than Tier B.
                                0   5      10           15            20         25    30
                                            Statement translation pass@1 (%)
                                                                                                                                                           Formalizing 100
                                                                                                              Model          Overall (888) Babel (A, 192) Theorems (B, 696)
Figure 3. Statement translation pass@1 across all 4,680 directed
file pairs. GPT-5.5 and DeepSeek-V4-Pro are the strongest overall,                                            GPT-5.5         93 (10.5%)      57 (29.7%)          36 (5.2%)
but even the best model succeeds on fewer than one third of pairs.                                            Gemini 3.1       45 (5.1%)      35 (18.2%)          10 (1.4%)
                                                                                                              Claude 4.6       13 (1.5%)       11 (5.7%)           2 (0.3%)
                                                                                                              DeepSeek-V4       13 (1.5%)       9 (4.7%)           4 (0.6%)
                                                                                                              Qwen3-235B         5 (0.6%)       3 (1.6%)           2 (0.3%)
ing. Isabelle decreases from 472.2 s to 6.9 s using server
batch sessions, while HOL Light decreases from 527.4 s
to 149.0 s using resident or forkserver backends. These                                                 difficult. The gaps are large: Lean 4 7→ Isabelle reaches
measurements show that scalable cross ITP evaluation re-                                                17.6%, while Isabelle 7→ Lean 4 reaches only 4.3%; HOL
quires infrastructure that is both faster and preserves per-file                                        Light 7→ Isabelle reaches 25.8%. These effects are not ex-
checking semantics.                                                                                     plained by logical foundation alone. CIC 7→ CIC directions
                                                                                                        are not consistently easier than cross-foundation directions,
4.3. Statement Translation                                                                              indicating that library conventions, elaboration behavior,
Statement translation is the primary evaluation in ITPE VAL,                                            and syntax matter more than the underlying foundation in
assessed on all 4,680 directed pairs per model across the                                               many cases. Because every directed source-target pair is
three benchmarks.                                                                                       evaluated on the same mathematical content, these asym-
                                                                                                        metries reflect target-language generation difficulty rather
Figure 3 shows that statement translation remains challeng-                                             than theorem selection. Full directional heatmaps are in
ing even before proof search is required. GPT-5.5 achieves                                              Appendix A.
the highest overall statement pass rate (29.1%), followed
closely by DeepSeek-V4-Pro (27.1%). Gemini is lower at                                                  4.4. Proof Translation
14.0%, while Qwen3-235B-A22B and Claude Sonnet 4.6
remain below 10%. The gap between the two leading mod-                                                  We also evaluate proof translation on the 888 directed pairs
els and the rest suggests that statement translation depends                                            from Babel-formal and Formalizing 100 Theorems.
on both formal syntax control and target library familiarity.                                           Proof translation is much harder than statement translation.
Table 3 shows that the controlled tier is consistently easier                                           GPT-5.5 is the strongest model, but still solves only 10.5%
than the ecosystem tier. Babel-formal removes most library                                              of proof pairs overall. The tier gap is also sharper: GPT-5.5
dependence and isolates foundational translation, while For-                                            reaches 29.7% on the controlled Babel-formal files but only
malizing 100 Theorems requires real library APIs, local                                                 5.2% on Formalizing 100 Theorems. This indicates that
helper lemmas, naming conventions, and prover-specific                                                  proof failure is not just a matter of producing syntactically
mathematical structures. MiniF2F is often easier than For-                                              valid target code. Complete proof translation often requires
malizing 100 Theorems because it contains single theorem                                                recovering target library dependencies, local helper lemmas,
statements with fewer local dependencies. This suggests that                                            automation behavior, and prover-specific proof idioms.
ecosystem complexity, not mathematical difficulty alone, is
the dominant source of failure.                                                                         Direction reversal. Proof translation has a different target
                                                                                                        profile from statement translation. Isabelle has one of the
4.3.1. T RANSLATION D IRECTION A NALYSIS                                                                highest statement verification rates, but becomes the lowest
                                                                                                        proof target (1.9–3.2%). HOL Light remains comparatively
Translation direction reveals strong asymmetry. In statement                                            strong, with proof pass rates between 4.3% and 5.7%. This
translation, Isabelle and HOL Light have the highest target-                                            suggests that well-formed statement generation and com-
side verification rates, whereas Lean 4 and Rocq remain                                                 plete proof construction reward different target-language

                                                                                                    6
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

properties. One interpretation is that Isabelle’s structured         Table 5. Multi-ITP autoformalization/auto-informalization round
                                                                     trips by target prover. Entries are pooled over five models; denom-
Isar style helps models produce well-formed declarations,            inators exclude empty or skipped outputs.
while complete proofs require more precise intermediate
facts and automation control. Another possible interpreta-             Target          Step 1 pass         Step 3 pass     Both pass
tion is that HOL Light’s compact OCaml tactic style appears            Lean 4     53/491 (10.8%) 56/493 (11.4%)                36
more uniform for current models. Full per-model directional            Isabelle   42/489 (8.6%)   21/490 (4.3%)               10
results are in Appendix A.                                             Rocq      152/465 (32.7%) 146/460 (31.7%)              101
                                                                       HOL Light 144/460 (31.3%) 147/454 (32.4%)              103
4.5. Statements vs. Proofs
On the 888 pairs where both modes are available, statement           while expressing a weaker or shifted theorem. To probe
translation is clearly easier. A McNemar test on matched             whether models preserve mathematical content through the
instances with the same theorem, direction, and model gives          natural-language interface, we evaluate round trips that al-
χ2 = 249.19 with p < 0.0001. The asymmetry is large: 417             ternate between autoformalization (NL 7→ formal) and auto-
instances pass only in statement mode, while 69 pass only in         informalization (formal 7→ NL). Each round trip has three
proof mode. The gap also varies by model. On the common              steps: formalize a natural-language theorem statement into
benchmarks, GPT-5.5 drops from 22.2% on statements to                ITP code, informalize the generated code back to natural
10.5% on proofs, Gemini from 18.0% to 5.1%, and Claude               language, and re-formalize the informalized description.
from 6.0% to 1.5%. At the theorem level, statement success           Verification at the first and third steps is a coarse executable
is a near necessary condition for proof success: 32 theorems         signal of whether the round trip preserves a formalizable
pass statements but never proofs, while no theorem passes            theorem.
proofs without any statement translation success. Thus,
statement translation is a useful diagnostic for cross-system        We evaluate two configurations on 100 miniF2F theorems
theorem encoding, but it is far from sufficient for full proof       across all five models:
transfer.
                                                                     • Single-ITP round trip: NL 7→ Lean 4 7→ NL 7→ Lean 4.
4.6. Aggregate Analysis                                              • Multi-ITP round trip: NL 7→ {Lean 4, Rocq, Isabelle,
We fit a logistic regression over all 27,840 evaluation                HOL Light} 7→ NL 7→ {Lean 4, Rocq, Isabelle, HOL
records with binary verification outcome as the response               Light}.
(pseudo-R2 = 0.25; full coefficients in Appendix B.6). The
strongest predictors are target prover and benchmark iden-           Table 5 shows a descriptive target effect in the round-trip set-
tity. HOL Light and Isabelle are strong statement targets,           ting: Rocq and HOL Light verify about one third of pooled
while Formalizing 100 Theorems and miniF2F are harder                outputs at both formalization steps, while Lean 4 stays near
than Babel-formal. Translation task is also important: proof         11% and Isabelle drops to 4.3% at step 3. The similar step-1
translation has a large negative effect (−1.05). By contrast,        and step-3 rates for Rocq and HOL Light suggest that target-
sharing a logical foundation has only a weak positive effect         side differences can persist after the natural-language inter-
(+0.19, p = 0.001). In proof translation, all four founda-           mediate step. The benefit of multi-ITP context is model- and
tion pairs cluster between 2.2% and 4.5%, consistent with            target-dependent: the strongest gains concentrate in a few
ecosystem-level dependencies being the strongest measured            model-target combinations, while other pairs show smaller
source of difficulty once downstream prover libraries are            or inconsistent changes. Thus, aligned multi-ITP context
involved.                                                            is promising evidence but not yet a uniform improvement
                                                                     across provers or models.
Source complexity is another significant predictor. Longer
source files are harder in proof mode (−0.54, p < 0.001),            For Lean 4 specifically, multi-ITP context improves pooled
and source files associated with failed proof translations are       verification relative to the single-ITP Lean cycle in this
longer than those associated with successful ones (median            subset, with step 1 rising from 4.8% to 10.6%. We treat
3,992 vs. 1,978 characters). This is consistent with models          this as a hypothesis-generating result: larger samples and
struggling to translate long proofs into the target prover’s         controlled ablations are needed before attributing the im-
local proof language, library names, and automation style.           provement to multi-ITP context rather than prompt, model,
                                                                     or theorem-selection effects.
4.7. Autoformalization and Auto-informalization
                                                                     4.8. Semantic Equivalence Checking
Type-checking confirms syntactic well-formedness but not
semantic fidelity: a generated statement can type-check              We apply the BEq check (Section 3.4) to all 322 verified
                                                                     source 7→ Lean 4 statement translations on miniF2F.

                                                                 7
                         ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 6. Semantic equivalence (BEq) of verified source 7→ Lean 4           similarity were the main factor, Lean 4↔Rocq would have
statement translations on miniF2F. Pass% is the fraction of verified
translations whose equivalence to the reference is established by
                                                                           uniformly high verification rates; instead, verification rates
BEq.                                                                       vary substantially by target prover: Isabelle and HOL Light
                                                                           are strong statement targets, Isabelle becomes the lowest-
         Model               Verified BEq Pass Pass% BEq Fail              verification proof target, and HOL Light remains relatively
         Claude Sonnet 4.6       74       62   83.8%      12               strong for proofs.
         DeepSeek-V4-Pro         84       37   44.0%      47
         Gemini 3.1 Pro           7        3   42.9%       4               Because miniF2F, Formalizing 100 Theorems, and Babel-
         GPT-5.5                 29       10   34.5%      19
         Qwen3-235B             128       62   48.4%      66               formal are public resources, absolute pass rates may be af-
         All models             322      174 54.0%       148               fected by training-data contamination; miniF2F also already
                                                                           has cross-ITP ports. We therefore emphasize controlled
                                                                           comparisons across targets, directions, tiers, and verification
Table 6 shows that 174 of 322 verified translations pass BEq               criteria under a fixed evaluation protocol; future private or
(54.0%). This changes the interpretation of native verifica-               newly authored splits would strengthen claims about out-of-
tion: a Lean-accepted generated statement is often syntac-                 distribution generalization.
tically valid but not established equivalent to the reference              Three evaluation limitations remain. BEq measures
by our restricted bidirectional check. Model differences are               statement fidelity for Lean 4 targets, but semantic fi-
large. Claude Sonnet 4.6 has the highest BEq rate among                    delity of proof strategies remains open: accepted proofs
verified translations (83.8%), while GPT-5.5, Gemini 3.1                   can establish equivalent statements while using differ-
Pro, DeepSeek-V4-Pro, and Qwen3-235B range from 34.5%                      ent intermediate lemmas, automation, proof terms, or
to 48.4%. BEq failures are mostly neither-direction failures               proof-engineering structure. The autoformalization/auto-
(132 of 322 verified translations), while all asymmetric fail-             informalization round-trip study is also exploratory and
ures are backward-only (16 of 322): the reference entails                  should be scaled up before drawing strong conclusions about
the generated statement, but not conversely. This pattern is               multi-ITP context effects. Finally, our experiments evaluate
consistent with semantic weakening, though BEq failures                    zero-shot pass@1 for LLMs rather than pass@k or agentic
should be read as not established equivalent rather than                   theorem-proving systems; agentic systems at the current
definitive semantic inequivalence because the deterministic                frontier may achieve different performance levels and ex-
cascade is incomplete.                                                     hibit distinct failure patterns.
Source direction has a smaller effect than model choice, but               Finally, the infrastructure is part of the benchmark itself.
the rates are not identical: Rocq 7→ Lean passes at 52.4%, Is-             Cross ITP results are only reliable when verifier state is iso-
abelle 7→ Lean at 47.5%, and HOL Light 7→ Lean at 61.5%.                   lated, labels are recovered per artifact, and backend prove-
HOL Light 7→ Lean has the highest BEq rate among veri-                     nance is recorded (Xin et al., 2026). The unified state-
fied translations, while Rocq 7→ Lean contributes the largest              isolated client therefore fixes the unit of measurement to one
number of verified translations. These results show that                   generated artifact while making large-scale target-prover
target-prover type checking is necessary but weak as a se-                 checking reproducible and auditable.
mantic metric. It remains the executable acceptance signal
for translation, but we need equivalence-aware evaluation
to measure whether verified statements preserve theorem                    5. Conclusion
meaning.                                                                   We presented ITPE VAL, a benchmark and unified verifi-
                                                                           cation infrastructure for formal translation across Lean 4,
4.9. Discussion                                                            Rocq, Isabelle, and HOL Light. Across 1,560 source files,
The largest performance gap is between controlled files and                6,848 theorems, and five LLMs, statement translation peaks
ecosystem files rather than between same-foundation and                    at 29.1% pass@1 and proof translation at 10.5%. The
cross-foundation translation pairs. Models perform much                    controlled-to-ecosystem drop identifies library dependen-
better on the controlled tier, where library dependence is                 cies as the strongest measured sources of translation diffi-
removed, and drop sharply on ecosystem files that require                  culty. A BEq check establishes that type-checking alone can
library APIs, naming conventions, automation, and local                    substantially overestimate semantic fidelity; the round-trip
helper lemmas. Future translation systems should therefore                 study suggests target-dependent autoformalization behavior
prioritize retrieval, library mapping, API alignment, and                  and possible benefits from multi-ITP context. Limitations
proof-style adaptation. This parallels findings in program-                include zero-shot pass@1 evaluation and BEq coverage of
ming language translation, where library-centric errors dom-               Lean 4 targets only; future work should add retrieval and re-
inate over core language failures (Xue et al., 2026). Direc-               pair, deploy BEq beyond Lean 4, and scale aligned corpora.
tional results reinforce this conclusion. If logical-foundation


                                                                       8
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Acknowledgments                                                      First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
                                                                       Whole-proof generation and repair with large language
Jiayi Wu is supported by Caltech SURF fellowship. Robert               models, 2023. URL https://arxiv.org/abs/
Joseph George is supported by DARPA expMath and                        2303.04910.
AA2.AIMING-1-NSF.2522494. Anima Anandkumar is sup-
ported in part by the Bren endowed chair, DARPA expMath,             Guilhot, F. and Pham, T.-M. High School Geome-
and the AI2050 Senior Fellowship program at Schmidt Sci-               try. https://github.com/rocq-community/
ences.                                                                 HighSchoolGeometry, 2016. Accessed: 2026-07-
                                                                       02.
References                                                           Harrison, J. Hol light: An overview. In Berghofer, S.,
1000+ Theorems Contributors. 1000+ theorems. https:                    Nipkow, T., Urban, C., and Wenzel, M. (eds.), Theo-
  //1000-plus.github.io/, 2026.                                        rem Proving in Higher Order Logics, pp. 60–66, Berlin,
                                                                       Heidelberg, 2009. Springer Berlin Heidelberg. ISBN
Allais, G., Dailler, S., Feree, H., Madiot, J.-M., Pedrot, P.-         978-3-642-03359-9. doi: 10.1007/978-3-642-03359-9 4.
  M., and Pouly, A. Coqtail. https://github.com/
  rocq-community/coqtail-math, 2020.                     Ac-         Hurd, J. The opentheory standard theory library. In Bo-
  cessed: 2026-07-02.                                                  baru, M., Havelund, K., Holzmann, G. J., and Joshi, R.
                                                                      (eds.), NASA Formal Methods, pp. 177–191, Berlin, Hei-
Aniva, L., Sun, C., Miranda, B., Barrett, C., and Koyejo, S.           delberg, 2011. Springer Berlin Heidelberg. ISBN 978-3-
  Pantograph: A machine-to-machine interaction interface               642-20398-5.
  for advanced theorem proving, high level reasoning, and
  data extraction in lean 4, 2025. URL https://arxiv.                Jiang, A. Q., Li, W., Han, J. M., and Wu, Y. LISA:
  org/abs/2410.16429.                                                   Language models of ISAbelle proofs. 6th Confer-
                                                                        ence on Artificial Intelligence and Theorem Proving,
Archive of Formal Proofs. Archive of formal proofs,                     2021. URL https://aitp-conference.org/
  2026. URL https://www.isa-afp.org/. Edited                            2021/abstract/paper_17.pdf.
  by Manuel Eberl, Gerwin Klein, Peter Lammich, An-
  dreas Lochbihler, Tobias Nipkow, Larry Paulson, René              Jiang, A. Q., Li, W., and Jamnik, M. Multilingual mathemat-
  Thiemann, and Dmitriy Traytel. Accessed: 2026-05-05.                  ical autoformalization, 2023a. URL https://arxiv.
                                                                        org/abs/2311.03755.
Assaf, A., Burel, G., Cauderlier, R., Delahaye, D., Dowek,
  G., Dubois, C., Gilbert, F., Halmagrand, P., Hermant, O.,          Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jam-
  and Saillard, R. Dedukti: a logical framework based                   nik, M., Lacroix, T., Wu, Y., and Lample, G. Draft,
  on the λπ-calculus modulo theory, 2023. URL https:                    sketch, and prove: Guiding formal theorem provers with
  //arxiv.org/abs/2311.07185.                                           informal proofs, 2023b. URL https://arxiv.org/
                                                                        abs/2210.12283.
Bertot, Y. and Castran, P. Interactive Theorem Proving
  and Program Development: Coq’Art The Calculus of                   Li, Z., Wu, Y., Li, Z., Wei, X., Zhang, X., Yang, F., and
  Inductive Constructions. Springer Publishing Company,                Ma, X. Autoformalize mathematical statements by sym-
  Incorporated, 1st edition, 2004. ISBN 3642058809. doi:               bolic equivalence and semantic consistency, 2024. URL
  10.1007/978-3-662-07964-5.                                           https://arxiv.org/abs/2410.20936.

CoRN Contributors. C-CoRN. https://github.com/                       Liu, Q., Zheng, X., Lu, X., Cao, Q., and Yan, J. Rethinking
  rocq-community/corn, 2011. Accessed: 2026-07-                        and improving autoformalization: Towards a faithful met-
  02.                                                                  ric and a dependency retrieval-based approach. In The
                                                                       Thirteenth International Conference on Learning Rep-
de Rauglaudre, D. Formal Proof in Coq of Cauchy–                       resentations, 2025a. URL https://openreview.
  Schwarz Inequality.   https://github.com/                            net/forum?id=hUb2At2DsQ.
  roglo/cauchy_schwarz, 2017.
                                                                     Liu, X., Zhu, T., Dong, Z., Liu, Y., Guo, Q., Liu, Z., Chen,
Dowek, G. and Thiré, F. Logipedia: a multi-system                     Y., and Luo, T. Assess: A semantic and structural eval-
  encyclopedia of formal proofs, 2023. URL https:                      uation framework for statement similarity, 2026. URL
 //arxiv.org/abs/2305.00064.                                           https://arxiv.org/abs/2509.22246.
Ekdohibs. Various Proofs in Coq. https://github.                     Liu, Y., Zhu, T., Liu, X., Chen, Y., Liu, Z., Guo, Q., Zhang,
  com/Ekdohibs/coq-proofs, 2014. Accessed:                             J., Bao, K., and Luo, T. Generalized tree edit distance
  2026-07-02.

                                                                 9
                     ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

  (gted): A faithful evaluation metric for statement auto-          Stoskopf, T., Cohen, C., and Tabareau, N. Babel-formal:
  formalization, 2025b. URL https://arxiv.org/                        Translation of proofs between lean and rocq. In The
  abs/2507.07399.                                                     5th Workshop on Mathematical Reasoning and AI at
                                                                      NeurIPS 2025, 2025. URL https://openreview.
Loiko, A.      Friendship Theorem                in    Coq.           net/forum?id=WBI1PL0hZ2.
  https://github.com/aleloi/
  coq-friendship-theorem, 2022.                                     Thakur, A., Tsoukalas, G., Durrett, G., and Chaudhuri, S.
                                                                      Proofwala: A framework for multilingual proof data
Lu, J., Wan, Y., Huang, Y., Xiong, J., Liu, Z., and Guo, Z.           synthesis and theorem-proving, 2025a. URL https:
  Formalalign: Automated alignment evaluation for aut-                //arxiv.org/abs/2502.04671.
  oformalization, 2024. URL https://arxiv.org/
  abs/2410.10135.                                                   Thakur, A., Tsoukalas, G., Durrett, G., and Chaudhuri,
                                                                      S. itp-interface: Generic interface for hooking up
Madiot, J.-M. and Chardard, F. Formalizing 100 theorems in            to any interactive theorem prover (itp) and collect-
 Rocq. https://madiot.fr/coq100/, 2026. Ac-                           ing data for training ml models for ai in formal theo-
 cessed: 2026-07-02.                                                  rem proving, 2025b. URL https://github.com/
mathlib Community, T. The lean mathematical library. In               trishullab/itp-interface.
 Proceedings of the 9th ACM SIGPLAN International Con-              The Mathematical Components Team. The Mathemati-
 ference on Certified Programs and Proofs, POPL ’20, pp.              cal Components Library. https://github.com/
 367–381. ACM, January 2020. doi: 10.1145/3372885.                    math-comp/math-comp, 2015. Accessed: 2026-07-
 3373824. URL http://dx.doi.org/10.1145/                              02.
 3372885.3373824.
                                                                    Thiré, F. Interoperability between proof systems using the
Mistral AI. Leanstral: Open-source foundation for trust-              logical framework Dedukti. PhD thesis, Université Paris-
 worthy vibe-coding, 2026. URL https://mistral.                       Saclay, December 2020. URL https://theses.fr/
 ai/news/leanstral.                                                   2020UPASG053.
Moura, L. d. and Ullrich, S. The lean 4 theorem prover and          Viennot, J., Baudart, G., Arias, E. J. G., and Lelarge, M.
 programming language. In Platzer, A. and Sutcliffe, G.               Minif2f in rocq: Automatic translation between proof
 (eds.), Automated Deduction – CADE 28, pp. 625–635,                  assistants – a case study, 2025. URL https://arxiv.
 Cham, 2021. Springer International Publishing. ISBN                  org/abs/2503.04763.
 978-3-030-79876-5.
                                                                    Wiedijk, F. Formalizing 100 theorems. https://www.
Nipkow, T., Wenzel, M., and Paulson, L. C. Isabelle/HOL:             cs.ru.nl/˜freek/100/, 2008.
  a proof assistant for higher-order logic. Springer-Verlag,
  Berlin, Heidelberg, 2002. ISBN 3540433767.                        Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
                                                                     nik, M., and Szegedy, C. Autoformalization with large
Niqui, M. and Bertot, Y. Qarith: Coq formalisation of                language models, 2022. URL https://arxiv.org/
  lazy rational arithmetic. In Berardi, S., Coppo, M.,               abs/2205.12615.
  and Damiani, F. (eds.), Types for Proofs and Programs,
  pp. 309–323, Berlin, Heidelberg, 2004. Springer Berlin            Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
  Heidelberg. ISBN 978-3-540-24849-1. doi: 10.1007/                   C., Li, W., and Liang, X. Deepseek-prover: Advancing
  978-3-540-24849-1 20.                                               theorem proving in llms through large-scale synthetic
                                                                      data, 2024. URL https://arxiv.org/abs/2405.
Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Re-             14333.
  liable evaluation and benchmarks for statement autofor-
  malization, 2025. URL https://arxiv.org/abs/                      Xin, H., Li, L., Jin, X., Fleuriot, J., and Li, W. Ape-bench:
  2406.07222.                                                         Evaluating automated proof engineering for formal math
                                                                      libraries, 2026. URL https://arxiv.org/abs/
Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin,              2504.19110.
  I., and Sutskever, I. Formal mathematics statement cur-
  riculum learning, 2022. URL https://arxiv.org/                    Xu, R., Cao, J., Lu, Y., Wen, M., Lin, H., Han, X., He, B.,
  abs/2202.01344.                                                     Cheung, S.-C., and Sun, L. Cruxeval-x: A benchmark for
                                                                      multilingual code reasoning, understanding and execu-
Rocq Archive. Finite Sets over Ordered Types. https://                tion, 2025. URL https://arxiv.org/abs/2408.
  github.com/rocq-archive/fsets, 2016. Ac-                           13001.
  cessed: 2026-07-02.

                                                               10
                     ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Xue, P., Zheng, K., Yang, Z., Pei, Y., Wu, L., Dong, J., Luo,
  X., Xiao, Y., Liu, F., Zhang, Y., Lyu, X., Li, X., Zhu, X.,
  and Wang, C. Translibeval: Demystify large language
  models’ capability in third-party library-targeted code
  translation, 2026. URL https://arxiv.org/abs/
  2509.12087.
Yan, W., Tian, Y., Li, Y., Chen, Q., and Wang, W. Code-
  transocean: A comprehensive multilingual benchmark for
  code translation, 2023. URL https://arxiv.org/
  abs/2310.04951.
Yang, K. and Deng, J. Learning to prove theorems via
  interacting with proof assistants, 2019. URL https:
  //arxiv.org/abs/1905.09381.
Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models, 2023. URL https://arxiv.org/
  abs/2306.15626.
Zhang, J., Zhong, C., Xu, H., Li, Q., and Zhou, Y. Kelps: A
  framework for verified multi-language autoformalization
  via semantic-syntactic alignment, 2025. URL https:
  //arxiv.org/abs/2507.08665.

Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics, 2022.
  URL https://arxiv.org/abs/2109.00110.
Zheng, Q., Xia, X., Zou, X., Dong, Y., Wang, S., Xue, Y.,
  Wang, Z., Shen, L., Wang, A., Li, Y., Su, T., Yang, Z., and
  Tang, J. Codegeex: A pre-trained model for code gen-
  eration with multilingual benchmarking on humaneval-
  x, 2024. URL https://arxiv.org/abs/2303.
  17568.




                                                                11
                                                                                 ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

 Appendix Overview                                                                                                                                                                                                   Figure 4. Proof translation pass@1 (%) by source–target direction,
                                                                                                                                                                                                                     per model. GPT-5.5 dominates across most directions; DeepSeek-
             Appendix guide                                                                                                                                                                                          V4-Pro and Qwen3-235B show near-zero rates in many cells.

              • Appendix A: Full per-model results. Proof, state-                                                                                                                                                     A.2. Statement Translation
                ment, HOL Light target behavior, and tier-gap break-
                                                                                                                                                                                                                      Figure 5 shows per-model statement translation pass@1 by
                downs by model.
                                                                                                                                                                                                                      source–target direction.
              • Appendix B: Statistical analysis. Confidence in-                                                                                                                                                                                                                           Statement Translation Pass@1 by Direction                           Per Model
                tervals, model agreement, directional asymmetry,                                                                                                                                                                                             GPT-5.5                                                   Gemini 3.1 Pro                                               Claude Sonnet 4.6
                target rankings, foundation-pair effects, and vari-                                                                                                                                                             Lean 4                  3.3          22.6          82.6            Lean 4                 5.4         31.0            6.2       Lean 4                  0.0        5.9          2.6
                                                                                                                                                                                                                                                                                                                                                                                                                      80

                ance decomposition.                                                                                                                                                                                               Rocq        7.2                    19.7          77.9             Rocq         2.8                  35.9            1.0         Rocq 11.0                        4.4          3.3
                                                                                                                                                                                                                                                                                                                                                                                                                      70




                                                                                                                                                                                                                     Source
                                                                                                                                                                                                                               Isabelle       3.3       3.3                        82.1           Isabelle       1.5      7.9                         4.4      Isabelle       0.8       1.8                     0.0
                                                                                                                                                                                                                                                                                                                                                                                                                      60
              • Appendix C: Dataset and complexity characteri-                                                                                                                                                                HOL Light       5.6       6.4          34.6                       HOL Light        3.6      8.2         60.3                    HOL Light       7.7       1.3        9.2
                                                                                                                                                                                                                                                                                                                                                                                                                      50
                zation. Corpus sizes, source lengths, long-context




                                                                                                                                                                                                                                                                                                                                                                                                                          Pass@1 (%)
                                                                                                                                                                                                                                              4          q            e               t                          4         q            e               t                     4          q            e          t
                                                                                                                                                                                                                                          n          Roc          bell        igh                            n         Roc         bell         igh                       n          Roc         bell        igh
                                                                                                                                                                                                                                      Lea                      Isa          LL                           Lea                    Isa           LL                      Lea                     Isa          LL
                                                                                                                                                                                                                                                                          HO                                                                HO                                                          HO            40
                                                                                                                                                                                                                                                    DeepSeek-V4-Pro                                                     Qwen3-235B                                                      All Models
                proof translation, theorem difficulty, and miniF2F
                                                                                                                                                                                                                                Lean 4                 44.4          24.6          22.1            Lean 4                22.8         4.1             1.5       Lean 4                 15.2        17.6        23.0   30
                categories.
                                                                                                                                                                                                                                  Rocq 11.0                          32.8          31.3             Rocq 14.9                         6.7             1.8         Rocq        9.4                  19.9        23.1   20




                                                                                                                                                                                                                     Source
                                                                                                                                                                                                                               Isabelle       4.9      55.1                        22.1           Isabelle 10.8          26.9                         1.3      Isabelle       4.3      19.0                    21.9   10
              • Appendix D: Extended related work. Formaliza-
                                                                                                                                                                                                                              HOL Light       7.4      46.2          23.6                       HOL Light        8.7     14.9         1.5                     HOL Light       6.6      15.4        25.8               0
                tion tracking, cross-ITP benchmarks, multilingual                                                                                                                                                                             4          q            e              ht                          4         q            e              ht                     4          q            e          t
                                                                                                                                                                                                                                          n          Roc          bell           Lig                         n         Roc         bell            Lig                    n          Roc         bell        igh
                                                                                                                                                                                                                                      Lea                      Isa           L                           Lea                    Isa            L                      Lea                     Isa          LL
                autoformalization, semantic fidelity, prover inter-                                                                                                                                                                                          Target
                                                                                                                                                                                                                                                                          HO
                                                                                                                                                                                                                                                                                                                               Target
                                                                                                                                                                                                                                                                                                                                            HO
                                                                                                                                                                                                                                                                                                                                                                                             Target
                                                                                                                                                                                                                                                                                                                                                                                                        HO


                faces, and code-translation analogues.
                                                                                                                                                                                                                     Figure 5. Statement translation pass@1 (%) by source–target
                                                                                                                                                                                                                     direction, per model. Directional trends are broadly consistent but
              • Appendix E: Experimental details. Round-trip                                                                                                                                                         magnitudes vary: DeepSeek-V4-Pro achieves the highest per-cell
                autoformalization results, prompt templates, and the                                                                                                                                                 rates while Claude Sonnet 4.6 is the weakest.
                Babel-formal formalization process.
                                                                                                                                                                                                                      A.3. HOL Light as a Statement Target
              • Appendix F: Semantic equivalence checking de-
                tails. BEq protocol, entailment asymmetries, and                                                                                                                                                      HOL Light-target statement verification is an order of mag-
                failure cases.                                                                                                                                                                                        nitude more expensive than other targets, and the results
                                                                                                                                                                                                                      are highly model-dependent. Table 7 shows that GPT-
              • Appendix G: Infrastructure details. State-                                                                                                                                                            5.5 achieves 80.9% on HOL Light-target statements and
                isolated verification architecture, telemetry, repro-                                                                                                                                                 DeepSeek-V4-Pro reaches 25.1%, while the remaining three
                ducibility, and released artifacts.                                                                                                                                                                   models stay below 4%. This gap suggests that HOL Light
                                                                                                                                                                                                                      statement generation is particularly sensitive to decoding
                                                                                                                                                                                                                      stability and syntax discipline, rather than exclusively to
 A. Full Per-Model Results                                                                                                                                                                                            mathematical content.
 A.1. Proof Translation                                                                                                                                                                                              Table 7. HOL Light-target statement translation by frontier model.
                                                                                                                                                                                                                     Each direction has 390 pairs; Total has 1,170.
 Figure 4 shows per-model proof translation pass@1 by
 source–target direction.                                                                                                                                                                                                                     Model                                       L4 7→ HL                   Rocq 7→ HL                             Isa 7→ HL                             Total
                                                                                                                                                                                                                                              GPT-5.5    322 (82.6%) 304 (77.9%) 320 (82.1%) 946 (80.9%)
                                                                         Proof Translation Pass@1 by Direction                        Per Model
                                                                                                                                                                                                                                              Gemini 3.1 24 (6.2%)     4 (1.0%)   17 (4.4%)   45 (3.8%)
                                        GPT-5.5                                                   Gemini 3.1 Pro                                             Claude Sonnet 4.6                                                                Claude 4.6 10 (2.6%)    13 (3.3%)   0 (0.0%)    23 (2.0%)
                                                                                                                                                                                               30
           Lean 4                 10.8          6.8               13.5        Lean 4                 2.7         0.0           9.5       Lean 4                  0.0         2.7         4.1

             Rocq        6.8                    4.1               14.9          Rocq        0.0                  4.1           2.7         Rocq        0.0                   2.7         1.4
                                                                                                                                                                                               25
                                                                                                                                                                                                                      For Claude Sonnet 4.6, Isabelle 7→ HOL Light yields 0/390
Source




          Isabelle 10.8           12.2                            17.6       Isabelle       4.1      9.5                       8.1      Isabelle       0.0       0.0                     1.4

         HOL Light 17.6            6.8          4.1                         HOL Light       4.1      9.5         6.8                   HOL Light       1.4       0.0         4.1
                                                                                                                                                                                               20                     passes, while Lean 4 7→ HOL Light (2.6%) and Rocq 7→
                                                                                                                                                                                                                      HOL Light (3.3%) produce a handful. The dominant failure
                                                                                                                                                                                                   Pass@1 (%)




                         4          q               e               t                       4         q           e               t                    4          q           e           t
                     n          Roc          bell                igh                    n         Roc         bell          igh                    n          Roc         bell         igh
                 Lea                      Isa            OL
                                                            L                       Lea                    Isa         OL
                                                                                                                          L                    Lea                     Isa          LL         15
                                                        H                                                             H                                                           HO
                               DeepSeek-V4-Pro                                                     Qwen3-235B                                                    All Models                                           mode is syntax errors in HOL Light’s OCaml-embedded
           Lean 4                  1.4          0.0               1.4         Lean 4                 0.0         0.0           0.0       Lean 4                  3.0         1.9         5.7   10
                                                                                                                                                                                                                      tactic language: models frequently generate pseudo-HOL-
             Rocq        0.0                    1.4               2.7           Rocq        0.0                  1.4           0.0         Rocq        1.4                   2.7         4.3
                                                                                                                                                                                                                      Light that is syntactically close but fails the OCaml parser.
Source




                                                                                                                                                                                               5
          Isabelle       1.4       5.4                            0.0        Isabelle       0.0      1.4                       0.0      Isabelle       3.2       5.7                     5.4

         HOL Light       0.0       4.1          0.0                         HOL Light       0.0      2.7         1.4                   HOL Light       4.6       4.6         3.2               0

                     n   4
                                Roc
                                    q
                                             bell
                                                    e            igh
                                                                    t                   n   4
                                                                                                  Roc
                                                                                                      q
                                                                                                              bell
                                                                                                                  e         igh
                                                                                                                                  t                n   4
                                                                                                                                                              Roc
                                                                                                                                                                  q
                                                                                                                                                                          bell
                                                                                                                                                                              e        igh
                                                                                                                                                                                          t                           A.4. Tier Gap by Model
                 Lea                      Isa               LL                      Lea                    Isa            LL                   Lea                     Isa          LL
                                                        HO                                                            HO                                                          HO
                                        Target                                                            Target                                                      Target
                                                                                                                                                                                                                     Figure 6 breaks down the Tier A (controlled) vs. Tier B
                                                                                                                                                                                                                     (ecosystem) pass@1 gap for each model individually. The

                                                                                                                                                                                                                12
                                                                                             ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

tier gap is consistent across all five models in both state-                                                                                                                                                                               κ = 0.108 for proofs (n = 888). Both indicate only slight
ment and proof translation, confirming that ecosystem                                                                                                                                                                                      agreement beyond chance. Models largely fail on different
complexity—library APIs, naming conventions, automa-                                                                                                                                                                                       theorems, suggesting that ensembling or best-of-k strategies
tion behavior, and local helper lemmas—is the dominant                                                                                                                                                                                     across models could yield higher pass rates than any single
source of difficulty beyond foundational translation issues.                                                                                                                                                                               model. The higher proof-mode agreement reflects floor
                                                                                                                                                                                                                                           effects: with most models below 2% pass rate, almost all
                                                   Statement Translation                                                                                                 Proof Translation
                                                                                              Tier A (Controlled)
                                                                                              Tier B (Ecosystem)                   35
                                                                                                                                                                                                                Tier A (Controlled)
                                                                                                                                                                                                                Tier B (Ecosystem)
                                                                                                                                                                                                                                           entries are failures.
             50
                                                                                                                                   30
             40
                                                                                                                                   25
                                                                                                                                                                                                                                           B.3. Directional Asymmetry
Pass@1 (%)




                                                                                                                      Pass@1 (%)
             30                                                                                                                    20

                                                                                                                                   15
             20
                                                                                                                                   10
                                                                                                                                                                                                                                           Table 10 reports the full set of directional asymmetries for
             10
                                                                                                                                    5                                                                                                      all six undirected ITP pairs. For each pair (A, B), we report
              0
                       T-5
                          .5                 Pro                 t 4.6                -Pro            -23
                                                                                                            5B
                                                                                                                                    0
                                                                                                                                          T-5
                                                                                                                                             .5
                                                                                                                                                          .1 P
                                                                                                                                                              ro                        4.6             4-P
                                                                                                                                                                                                           ro
                                                                                                                                                                                                                     -23
                                                                                                                                                                                                                        5B
                                                                                                                                                                                                                                           the pooled pass@1 in both directions and the absolute gap.
                  GP                    .1
                                                            onn
                                                                e                  -V4                                                  GP                                        net
                                  ini 3                  eS                   See
                                                                                  k
                                                                                              Qw
                                                                                                en3                                                  ini 3                  Son                     ek-V        Qw
                                                                                                                                                                                                                  en3
                                                                                                                                                                                                 pSe
                               Gem
                                                   Cla
                                                       ud                Dee
                                                                             p                                                                    Gem
                                                                                                                                                                   Cla
                                                                                                                                                                      ude                     Dee                                          Statement-mode asymmetries are large and systematic: the
Figure 6. Tier A (controlled) vs. Tier B (ecosystem) pass@1 rates                                                                                                                                                                          strongest is Lean 4 ↔ HOL Light (|∆| = 16.4 pp), driven
by model. Left: statement translation; right: proof translation. The                                                                                                                                                                       by higher verification rates for HOL Light targets. Proof-
tier gap is consistent across all models: controlled, self-contained                                                                                                                                                                       mode asymmetries are smaller, consistent with floor effects
theorems are 3–10× more tractable than ecosystem-level transla-                                                                                                                                                                            compressing differences.
tions with real library dependencies.
                                                                                                                                                                                                                                           Table 10. Directional asymmetry: A 7→ B vs. B 7→ A pass@1 (%),
                                                                                                                                                                                                                                           pooled across all models. Pairs are sorted by statement-mode gap.
B. Statistical Analysis
B.1. Confidence Intervals                                                                                                                                                                                                                                       Statements                 Proofs
                                                                                                                                                                                                                                              Pair         A 7→ B B 7→ A |∆|        A 7→ B B 7→ A |∆|
Tables 8 and 9 augment the main-text pass@1 tables with
                                                                                                                                                                                                                                              L4↔HL         23.0      6.6    16.4    5.7      4.6   1.1
95% Wilson confidence intervals. The narrow statement-
                                                                                                                                                                                                                                              L4↔Isa        17.6      4.3    13.4    1.9      3.2   1.4
mode intervals (±1–2 pp) reflect the large sample size (n =                                                                                                                                                                                   Rocq↔HL       23.1     15.4     7.7    4.3      4.6   0.3
4,680); proof-mode intervals are wider (±2–4 pp) due to the                                                                                                                                                                                   L4↔Rocq       15.2      9.4     5.8    3.0      1.4   1.6
smaller evaluation set (n = 888).                                                                                                                                                                                                             Isa↔HL        21.9     25.8     3.9    5.4      3.2   2.2
                                                                                                                                                                                                                                              Rocq↔Isa      19.9     19.0     0.9    2.7      5.7   3.0
Table 8. Statement translation pass@1 with 95% Wilson confi-
dence intervals (n = 4,680 per model).
                                                                                                                                                                                                                                           The most symmetric statement pair is Rocq ↔ Isabelle
                   Model                                                                                Passed                               Pass@1                                     95% CI                                             (|∆| = 0.9 pp), despite spanning different logical foun-
                                                                                                                                                                                                                                           dations. This suggests that the translation difficulty be-
                   GPT-5.5                                                                                   1,360                              29.1%                                   [27.8, 30.4]
                   DeepSeek-V4-Pro                                                                           1,269                              27.1%                                   [25.9, 28.4]                                       tween these two systems is roughly balanced: neither is
                   Gemini 3.1 Pro                                                                             656                               14.0%                                   [13.1, 15.0]                                       much easier to read from or generate into than the other.
                   Qwen3-235B-A22B                                                                            452                               9.7%                                    [ 8.8, 10.5]                                       In proof mode, the largest asymmetry is Rocq ↔ Isabelle
                   Claude Sonnet 4.6                                                                          187                                4.0%                                   [ 3.5, 4.6]                                        (|∆| = 3.0 pp), where Isabelle 7→ Rocq (5.7%) outperforms
                                                                                                                                                                                                                                           the reverse. Isabelle’s verbose Isar proofs may provide
Table 9. Proof translation pass@1 with 95% Wilson confidence
                                                                                                                                                                                                                                           richer structural cues for generating Rocq tactics.
intervals (n = 888 per model).
                                                                                                                                                                                                                                           B.4. Bradley-Terry Target Ranking
                   Model                                                                                Passed                               Pass@1                                     95% CI
                                                                                                                                                                                                                                           To obtain a principled ranking of ITPs as generation targets,
                   GPT-5.5                                                                                       93                             10.5%                                   [ 8.6, 12.7]
                   Gemini 3.1 Pro                                                                                45                              5.1%                                   [ 3.8, 6.7]
                                                                                                                                                                                                                                           we fit a Bradley-Terry model to pairwise “wins”: for each
                   DeepSeek-V4-Pro                                                                               13                              1.5%                                   [ 0.9, 2.5]                                        (theorem, model, source) triple, the target that the model
                   Claude Sonnet 4.6                                                                             13                              1.5%                                   [ 0.9, 2.5]                                        successfully translates to “beats” targets that fail. Table 11
                   Qwen3-235B-A22B                                                                               5                              0.6%                                    [ 0.2, 1.3]                                        reports the log-strength parameters (mean-centered).
                                                                                                                                                                                                                                           HOL Light is the strongest target in both modes. The
B.2. Inter-Model Agreement                                                                                                                                                                                                                 most striking shift is Isabelle: second-highest for statements
                                                                                                                                                                                                                                           (+0.35) but tied for lowest in proofs (−0.35). One possible
To assess whether models fail on the same theorems or on                                                                                                                                                                                   explanation is that Isabelle’s Isar language helps models gen-
complementary subsets, we compute Fleiss’ κ across all five                                                                                                                                                                                erate well-formed declarations but is harder for constructing
models for each (theorem, direction) pair. The kappa values                                                                                                                                                                                complete proofs. The gap between Lean 4 and the field
are very low: κ = 0.032 for statements (n = 4,680) and                                                                                                                                                                                     narrows in proof mode, suggesting that Lean 4’s difficulty

                                                                                                                                                                                                                                      13
                         ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 11. Bradley-Terry log-strength scores for ITPs as generation            Table 13. Logistic regression coefficients for verification outcome
targets. Higher scores indicate higher target-side verification rates.        (n = 27,840, pseudo-R2 = 0.25). Reference categories are
The ranking reverses between modes: Isabelle drops from the                   GPT-5.5, statements, Babel-formal, Lean 4 source, and Lean 4
second-highest statement target score to the lowest proof target              target.
score.
                                                                                  Predictor                  Coef.       95% CI     p    Note
            Target ITP      Stmts score    Proofs score                           Intercept                  +2.25    [1.6, 2.9] < .001
                                                                                  Tgt: HL (vs. L4)           +2.34    [2.2, 2.5] < .001 Strong tgt
            HOL Light            +0.51            +0.55                           Tgt: Isa (vs. L4)          +1.96    [1.8, 2.1] < .001 Strong tgt
            Isabelle             +0.35            −0.35                           Mod: DeepSeek (vs. GPT)       —             —    —
            Rocq                 +0.15            +0.16                           Mod: Qwen (vs. GPT)           —             —    —
            Lean 4               −1.01            −0.35                           Src: HL (vs. L4)           +0.24     [.09, .4] .002 Good src
                                                                                  Same foundation            +0.19     [.07, .3] .001 Weak
                                                                                  Src complexity (log len)   −0.42   [−.5, −.3] < .001 Harder
                                                                                  Mod: Gemini (vs. GPT)      −0.89 [−1.0, −.8] < .001
                                                                                  Mode: proofs (vs. stmts)   −1.05 [−1.3, −.8] < .001 Harder
as a statement target is partly driven by syntactic strictness                    Bench: F100 (vs. Babel)    −1.50 [−1.7, −1.3] < .001 Tier B
rather than proof-search hardness.                                                Bench: miniF2F (vs. Babel) −2.33 [−2.6, −2.1] < .001 Harder
                                                                                  Mod: Claude (vs. GPT)      −2.39 [−2.5, −2.2] < .001
                                                                                  Src: Rocq (vs. L4)       −0.06      [−.2, .06]   .30   n.s.
B.5. Logical Foundation Pairs                                                     Src: Isa (vs. L4)        −0.13      [−.3, .03]   .11   n.s.
                                                                                  Tgt: Rocq (vs. L4)       −0.15      [−.4, .05]   .13   n.s.
Table 12 breaks down pass rates by the logical foundation
of the source and target provers (CIC-based: Lean 4, Rocq;
HOL-based: Isabelle, HOL Light).                                              B.7. Statements vs. Proofs Correlation

Table 12. Pass@1 by logical foundation pair. In statement mode,               At the theorem level, statement and proof translation dif-
the high CIC 7→ HOL and HOL 7→ HOL rates are driven by target-                ficulty are strongly correlated. Across the 74 theorems
prover effects (Isabelle and HOL Light). In proof mode, all four              where both modes are evaluated (Babel-formal + Formal-
pairs cluster within 2 percentage points.
                                                                              izing 100 Theorems), the Pearson correlation between per-
                                Statements            Proofs                  theorem statement pass rate and proof pass rate is r = 0.74
                                                                              (p < 0.001). Crucially, the relationship is asymmetric: all
   Pair             Type      Pass/Total      % Pass/Total     %
                                                                              41 theorems with at least one proof pass also have at least
   CIC 7→ CIC within           479/3900 12.3         16/740 2.2               one statement pass, while 32 theorems pass statements but
   CIC 7→ HOL cross           1630/7800 20.9        54/1480 3.6               never proofs. No theorem passes proofs but fails all state-
   HOL 7→ CIC cross            883/7800 11.3        67/1480 4.5
   HOL 7→ HOL within           932/3900 23.9         32/740 4.3               ment translations. This confirms that statement translation
                                                                              success is a near-necessary condition for proof translation
   Within                     1411/7800 18.1 48/1480 3.2
                                                                              success.
   Cross                     2513/15600 16.1 121/2960 4.1


The statement-mode asymmetry between CIC 7→ HOL                               C. Dataset and Complexity Characterization
(20.9%) and HOL 7→ CIC (11.3%) is not a foundation effect                     C.1. Dataset Statistics
but a target-prover effect: the HOL targets are Isabelle and
HOL Light, while the CIC targets are Lean 4 and Rocq                          Table 14 reports corpus-level statistics for the benchmark
(both hard). In proof mode, the four foundation pairs cluster                 data. File lengths vary by orders of magnitude across bench-
tightly (2.2–4.5%), confirming that logical foundation is not                 marks and ITPs: miniF2F files are short single-theorem
a meaningful predictor of translation difficulty once other                   statements (median 202 chars), while Formalizing 100 The-
factors are controlled.                                                       orems proof files range from ∼1 KB to ∼750 KB, with
                                                                              HOL Light files being the longest due to its verbose OCaml-
B.6. Variance Decomposition                                                   embedded tactic style.

Table 13 reports the full logistic regression results from the                These proof-file lengths make Formalizing 100 Theorems an
main-effects model described in Section 4.6. Reference                        end-to-end long-context translation setting: we pass the full
categories are GPT-5.5 (model), statements (mode), Babel-                     source file to the model without chunking or retrieval. Thus,
formal (benchmark), and Lean 4 (source and target prover).                    proof translation on this tier reflects both formal translation
                                                                              ability and each model’s effective long-context retention;
An interaction model adding model×mode and                                    we do not normalize results by context-window size or per-
model×target interactions improves fit (pseudo-R2 = 0.26),                    session memory behavior.
confirming that models have different relative strengths
across modes and target provers.                                              Table 15 breaks down statement file lengths by ITP. Isabelle
                                                                              and HOL Light files are consistently longer than their Lean 4


                                                                         14
                                                       ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 14. Source file length statistics (characters) by benchmark                                                                                   C.3. Theorem-Level Difficulty Distributions
and mode. Per-ITP lengths are averaged across all four provers.
                                                                                                                                                    Table 16 reports the distribution of per-file pass rates (ag-
                  Benchmark                           Mode Files Mean Median                                                Max                     gregated across all models, directions, and modes) for each
                  Babel-formal    stmts                                   16                3674           2744        11662                        benchmark.
                  Babel-formal    proofs                                  16                6240           5118        21262
                  Formalizing 100                                                                                                                   Table 16. Distribution of file-level pass rates by benchmark. Pass
                  Theorems        stmts                                   58 16711                         6016 289797                              rate is computed per file across all models and translation direc-
                  Formalizing 100                                                                                                                   tions. No file exceeds 50% in any benchmark.
                  Theorems        proofs                              58 47543                           16663 753999
                  miniF2F         stmts                              316   213                             202   1499                                Benchmark                                             Files Mean             0%              0–10%          10–50%
                                                                                                                                                     Babel-formal                                           16 17.8% 0 (0%) 2 (12%)                              14 (88%)
                                                                                                                                                     Formalizing 100
and Rocq counterparts, reflecting more verbose surface syn-                                                                                          Theorems                                               58 5.0% 1 (2%) 52 (90%) 5 (9%)
                                                                                                                                                     miniF2F                                               316 18.0% 0 (0%) 49 (16%) 267 (84%)
tax. This length asymmetry is a surface-syntax confound
when comparing target difficulty across ITPs.
                                                                                                                                                    All 16 Babel-formal files are solved at least once, reflecting
Table 15. Median statement file length (characters) by ITP and                                                                                      the controlled tier’s tractability. In contrast, only 1 of 58
benchmark.                                                                                                                                          Formalizing 100 Theorems files has zero passes across all
                   Benchmark                           Lean 4 Rocq Isabelle HOL Light
                                                                                                                                                    models and directions, but 90% remain below 10% pass rate,
                                                                                                                                                    representing theorems where ecosystem dependencies make
                   Babel-formal                             2536 2593                          3254                   3434                          translation very difficult for current models. The miniF2F
                   Formalizing 100
                   Theorems                                 6467 4733                          8525                   4566                          distribution is more spread: most theorems have nonzero
                   miniF2F                                   207 192                            270                    129                          pass rates above 10%, consistent with the statement-only
                                                                                                                                                    evaluation being more tractable than full proof translation.
                                                                                                                                                                                                                Theorem Difficulty Distribution
 C.2. Source Complexity                                                                                                                                                                          1.0
                                                                                                                                                                  Cumulative fraction of files


                                                                                                                                                                                                 0.8
Source content length serves as a proxy for proof complexity.
                                                                                                                                                                                                 0.6
In proof mode, longer source proofs are significantly harder
                                                                                                                                                                                                 0.4
to translate (logistic regression coefficient = −0.54, p <
                                                                                                                                                                                                 0.2                                          Babel-formal
0.001). In statement mode, the effect is weaker but still                                                                                                                                                                                     Hundred Theorems
                                                                                                                                                                                                 0.0                                          miniF2F
negative (coefficient = −0.10, p < 0.001). Additionally,                                                                                                                                               0       10          20            30           40
                                                                                                                                                                                                                     Per-file pass rate (%)
failed proof translations are longer than successful ones
(median 3,992 vs. 1,978 characters), suggesting that models                                                                                         Figure 8. Empirical CDF of per-file pass rates by benchmark.
over-generate when unable to find a correct proof. This is                                                                                          Formalizing 100 Theorems files are concentrated near 0% (90%
consistent with the general finding that LLMs struggle with                                                                                         below 10% pass rate), while Babel-formal and miniF2F files spread
                                                                                                                                                    across a wider range, reflecting their greater tractability.
long-context generation tasks and tend to produce verbose,
incorrect outputs when the search space is large.
                                                                                                                                                    C.4. MiniF2F Competition Categories
                                Statement Translation                                                   Proof Translation
             70                                        Binned mean                                                          Binned mean             MiniF2F theorem titles encode their competition source or
             60                                                                        40                                                           mathematical topic. Table 17 reports statement translation
             50
                                                                                                                                                    pass rates by category (all models pooled, statement mode
Pass@1 (%)




                                                                          Pass@1 (%)




                                                                                       30
             40
             30                                                                        20                                                           only).
             20
             10
                                                                                       10                                                           Competition difficulty does not predict translation diffi-
              0                                                                         0                                                           culty. Table 18 groups categories by competition difficulty
                         2              3         4         5         6                             3             4          5             6
                    10             10        10        10        10                            10            10         10            10            level. The expected hierarchy AMC < AIME < IMO is not
                             Source length (chars, log scale)                                 Source length (chars, log scale)
                                                                                                                                                    reflected in translation pass rates. AIME problems (16.5%)
Figure 7. Per-file pass rate vs. source content length (log scale).                                                                                 are slightly easier to translate than AMC problems (14.8%),
Left: statement translation; right: proof translation. Dark markers
show binned means. The negative trend is stronger for proofs,
                                                                                                                                                    and IMO problems (10.0%) have only a modest gap. These
where each doubling of source length roughly halves the success                                                                                     differences should be read as translation statistics for the
probability.                                                                                                                                        four-ITP intersection, not as direct measures of mathemati-
                                                                                                                                                    cal difficulty.
                                                                                                                                                    Topic-labeled theorems (algebra, number theory, induc-
                                                                                                                                                    tion: 15.4% pooled) outperform competition-labeled ones

                                                                                                                                               15
                                   ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

Table 17. MiniF2F statement translation pass@1 by competition                                                   and has been used as a target for representing several logics
category (all models pooled).
                                                                                                                and proof systems. Logipedia (Dowek & Thiré, 2023) and
    Category                       Passed/Total                         %                   Type                EuroProofNet (Thiré, 2020) build on this line of work to
                                                                                                                support proof interoperability. OpenTheory (Hurd, 2011)
    MATH Dataset                   2,359/12,120                       19.5                  Math dataset
    Induction                        127/720                          17.6                  Topic
                                                                                                                provides a package format and standard library for the HOL
    AMC 12B                         252/1,440                         17.5                  Competition         family of provers. These projects make proof exchange pos-
    AIME                              99/600                          16.5                  Competition         sible in principle, but they do not evaluate LLM generated
    AMC                              103/660                          15.6                  Competition         translations across many directed prover pairs. ITPE VAL
    Number Theory                     54/360                          15.0                  Topic               is therefore complementary: it treats interoperability as an
    Algebra                         208/1,440                         14.4                  Topic
    AMC 12A                         199/1,560                         12.8                  Competition
                                                                                                                empirical benchmark problem, with target-prover checking
    IMO                                6/60                           10.0                  Competition         as the evaluation signal.

Table 18. MiniF2F pass rates by competition difficulty level. Math-                                             D.2. Cross ITP translation benchmarks and systems
ematical difficulty does not predict cross-ITP translation difficulty.
                                                                                                                Babel-formal (Stoskopf et al., 2025) is the closest prior
           Difficulty Level                                 Passed Total                           %            benchmark. It studies Lean and Rocq proof translation
           AMC 12 (incl. 12A/B)                                 554 3660 15.1
                                                                                                                using a small aligned corpus of 14 files and 117 lemmas,
           AIME                                                  99 600 16.5                                    and explores proof term translation as a bridge between the
           IMO / USAMO                                            6   60 10.0                                   two systems. ITPE VAL extends the scope from two systems
                                                                                                                to four, from one logical family comparison to CIC and
                                                                                                                HOL, and from 14 aligned files to 390 aligned items (1,560
(15.2%) only marginally in the 4-ITP intersection subset,                                                       source files across four ITPs).
suggesting that once theorems are formalized across all four
                                                                                                                Recent work on miniF2F in Rocq (Viennot et al., 2025) uses
systems, topic vs. competition provenance has little impact
                                                                                                                natural language, Lean, and Isabelle sources to produce
on translation difficulty.
                                                                                                                Rocq theorem statements. This shows that LLMs can help
                                         miniF2F by Competition Category                                        build new formal benchmark ports. However, the task is
                                                                                           n=202
                MATH Dataset
                     Induction                                                              n=12
                                                                                                                one target system and statement only. In contrast, ITPE VAL
                    AMC 12B                                                           n=24
                                                                                       n=10
                                                                                                                evaluates all 12 source target directions among Lean 4, Rocq,
                        AIME
                      AMC 12                                                        n=11                        Isabelle, and HOL Light, and includes both statement and
                Number Theory                                                        n=6
                      Algebra                                                n=24                               proof translation when aligned proofs exist.
                    AMC 12A                                           n=26
                         IMO                                                               n=1
                                                                                                                Recent prover agents also include cross system translation
                             0.0   2.5   5.0   7.5   10.0    12.5   15.0     17.5    20.0
                                               Statement Pass@1 (%)                                             as one capability. Leanstral (Mistral AI, 2026), for ex-
Figure 9. MiniF2F statement translation pass@1 by competition                                                   ample, is designed around Lean 4 and demonstrates Rocq
category (all models pooled). Mathematical difficulty level (AMC                                                to Lean translation as part of a broader proof engineering
vs. AIME vs. IMO) does not predict translation difficulty; the                                                  agent. Such systems motivate the need for a benchmark that
MATH Dataset category is easiest to translate despite covering                                                  can measure translation quality systematically rather than
diverse problem types.                                                                                          through isolated examples.

D. Extended Related Work                                                                                        D.3. Multilingual autoformalization
D.1. Formalization tracking and proof exchange                                                                  Multilingual autoformalization studies translation between
                                                                                                                informal mathematics and multiple formal languages.
Several projects study overlap among formal libraries
                                                                                                                MMA (Jiang et al., 2023a) constructs informal formal data
without providing a translation benchmark. Formalizing
                                                                                                                from Lean and Isabelle and shows that multilingual training
100 Theorems (Wiedijk, 2008) and the 1000+ Theorems
                                                                                                                can improve autoformalization. ProofWala (Thakur et al.,
project (1000+ Theorems Contributors, 2026) catalog which
                                                                                                                2025a) studies multilingual proof data synthesis and cross
mathematical results have been formalized in which proof
                                                                                                                language transfer between Lean and Rocq. KELPS (Zhang
assistants. These resources are valuable for identifying com-
                                                                                                                et al., 2025) introduces an intermediate representation for
mon mathematical content, but they do not provide aligned
                                                                                                                translating natural language into Lean, Rocq, and Isabelle.
source files, translation tasks, or target prover evaluation.
                                                                                                                These works are closely related to our autoformalization
Logical frameworks and proof exchange systems address
                                                                                                                and auto-informalization experiment, but differ in direction
a complementary problem: representing proofs from dif-
                                                                                                                and evaluation target. They primarily study natural lan-
ferent systems in a common foundation. Dedukti (Assaf
                                                                                                                guage to formal translation or multilingual training data.
et al., 2023) is based on the λΠ-calculus modulo theory

                                                                                                           16
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

ITPE VAL studies formal-to-formal translation directly and            D.6. Programming language translation benchmarks
uses natural-language round trips only as a diagnostic for
                                                                      Code translation benchmarks such as CodeTransOcean (Yan
multi-ITP generation context.
                                                                      et al., 2023), HumanEval-X (Zheng et al., 2024), and
                                                                      CRUXEval-X (Xu et al., 2025) evaluate translation between
D.4. Semantic fidelity and evaluation
                                                                      programming languages using tests or executable behavior.
A recurring issue in autoformalization is that type check-            They are useful analogues, but ITP translation is different
ing alone can overestimate correctness. Liu et al. (2025a)            in two ways. First, the target artifact must pass a proof
introduce BEq (Bidirectional Extended Definitional Equiva-            assistant kernel, elaborator, tactic engine, and library envi-
lence), a neuro-symbolic metric that extends definitional             ronment. Second, translation must preserve logical meaning
equality with tactic-based transformations to determine               across systems with different foundations and libraries, not
equivalence between formal statements; we adopt their bidi-           merely produce code with the same input output behav-
rectional entailment framework for cross-ITP translation              ior. These differences motivate a dedicated benchmark for
evaluation. Poiroux et al. (Poiroux et al., 2025) study reli-         formal translation.
able evaluation for statement autoformalization and intro-
duce stronger equivalence based metrics. Liu et al. (Liu              E. Experimental Details
et al., 2025b) propose tree edit based evaluation for for-
mal statements, and ASSESS/TransTED (Liu et al., 2026)                E.1. Autoformalization and Auto-informalization: Full
combines structural and semantic similarity for statement                  Results
comparison. FormalAlign (Lu et al., 2024) trains models
                                                                      Table 19 reports the full multi-ITP round-trip verification
to detect semantic alignment between informal and formal
                                                                      results by model and target prover. Rocq and HOL Light
statements, and symbolic equivalence or round trip evalua-
                                                                      account for most verified outputs, but the pattern is not
tion methods have also been explored (Li et al., 2024).
                                                                      target-independent: GPT-5.5 is strongest on HOL Light and
Cross-ITP translation adds another layer of difficulty. The           Rocq, Gemini is strongest on Rocq and relatively strong
source and target statements often live in different kernels,         on Isabelle, and the remaining models show smaller or in-
use different libraries, and expose different definitional            consistent gains. Table 20 compares the multi-ITP Lean 4
equalities. This makes direct structural comparison much              results against the single-ITP Lean cycle.
harder than in single-prover autoformalization. For this rea-
son, ITPE VAL uses target-prover checking as the primary              Table 19. Multi-ITP round-trip verification by model and target
                                                                      prover. Entries are pass/checked counts for step 1 and step 3;
executable signal and BEq as a complementary equivalence-             checked counts exclude empty or skipped outputs.
aware check for Lean 4 targets.
                                                                                       Lean 4        Isabelle           Rocq         HOL Light
D.5. Programmatic prover interfaces                                    Model         S1     S3       S1    S3      S1          S3    S1       S3
                                                                       GPT-5.5     16/100 17/100 2/100 1/100    61/100    62/100    91/100   92/100
Machine learning for theorem proving has produced sev-                 Claude 4.6  12/100 11/100 1/100 1/100    0/100     3/100     11/100   7/100
eral important prover interaction tools. CoqGym (Yang &                Gemini 3.1   8/99   9/98 30/97 17/96      61/75     57/67     26/70   28/61
                                                                       DeepSeek-V4 4/94    7/96 6/94 1/95        14/92     11/94     14/91    18/93
Deng, 2019) provides a dataset and learning environment for            Qwen3-235B 13/98 12/99 3/98 1/99          16/98     13/99      2/99    2/100
Rocq/Coq proof interaction. LeanDojo (Yang et al., 2023)
provides Lean data extraction, retrieval augmented proving,
and programmatic interaction with Lean. Pantograph (Aniva             Table 20. Lean 4 verification under single-ITP and multi-ITP round
                                                                      trips. Entries count all 100 selected miniF2F theorems per model,
et al., 2025) gives a machine to machine interface for Lean 4         treating missing or invalid generations as non-passing.
and supports proof search. PISA (Jiang et al., 2021) sup-
ports interaction with Isabelle. The itp-interface                                               Step 1 pass               Step 3 pass
project (Thakur et al., 2025b) provides a generic interface              Model            Single Multi          ∆ Single Multi                ∆
for Lean 4 and Rocq.
                                                                         GPT-5.5                 2        16 +14            4        17 +13
These systems focus on proof search or data extraction                   Claude 4.6             13        12  -1           15        11  -4
within one prover, or a small subset of provers. ITPE VAL                Gemini 3.1              0         8 +8             0         9 +9
                                                                         DeepSeek-V4             4         4   0            5         7 +2
instead requires a verification service that can run four het-           Qwen3-235B              5        13 +8            15        12  -3
erogeneous target systems at benchmark scale. The main
systems challenge is not tactic search, but reproducible                 Pooled                 24        53 +29           39        56 +17
target-prover checking under state isolation. Our unified
client, filters, environment-keyed scheduling, checkpointed
                                                                      Worked example. We trace the full multi-ITP round trip
JSONL verification, and warm isolated backends are de-
                                                                      for AIME 1983 Problem 1 (Claude Sonnet 4.6) to illustrate
signed for this cross-prover evaluation setting.

                                                                 17
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

the process and a characteristic failure mode. The original            reference formalization: the original miniF2F Lean 4 state-
NL statement is:                                                       ment types x, y, z as N (natural numbers) with w : N, while
                                                                       the round-trip-generated versions use R (reals), yielding a
  Step 0: Reference NL
                                                                       strictly weaker statement. This information loss is intro-
  Let x, y and z all exceed 1 and let w                                duced at step 1, where the NL description does not specify
  be a positive number such that log x w                               integrality, and propagates unchanged through the rest of the
  = 24, log y w = 40 and log {xyz} w = 12.                             round trip. Such type-level semantic drift, invisible in the
  Find log z w. Show that it is 060.
                                                                       NL domain, is a characteristic failure mode of NL-mediated
                                                                       round-trips.
Step 1 (NL 7→ 4 ITPs) produces four formalizations. Two
representative outputs:
                                                                       E.2. Prompt Templates
  Step 1: NL 7→ Lean 4
                                                                       All evaluations use a two-message format (system + user)
  theorem log z w (x y z w : R) (hx : x                                with zero-shot prompting. Placeholders in {braces} are
  > 1) (hy : y > 1) (hz : z > 1) (hw :                                 filled per translation pair. The target-language header at
  w > 0)
  (h1 : Real.log w / Real.log x = 24)
                                                                       the end of each prompt primes generation with the correct
  (h2 : Real.log w / Real.log y = 40)                                  output format. System messages instruct the model to return
  (h3 : Real.log w / Real.log (x * y * z)                              only raw ITP code with no markdown fencing or explana-
  = 12) :                                                              tion.
  Real.log w / Real.log z = 60 := by sorry
                                                                         Statement translation
  Step 1: NL 7→ Isabelle                                                 Translate the following {src name}
                                                                         theorem statement of "{title}" into
  theorem log z w:
                                                                         {tgt name}. Do not prove the theorem;
  fixes x y z w :: real
                                                                         leave the proof body as sorry or the
  assumes hx: "x > 1" and hy: "y > 1"
                                                                         equivalent placeholder.
  and hz: "z > 1" and hw: "w > 0"
  assumes h1: "log x w = 24"                                             === {src name} statement ===
  assumes h2: "log y w = 40"                                             {source content}
  assumes h3: "log (x * y * z) w = 12"
  shows "log z w = 60"                                                   === {tgt name} statement ===
  sorry
                                                                         Proof translation
Step 2 (4 ITPs 7→ NL) produces an informalized description
                                                                         Translate the following {src name} proof
from all four formalizations:                                            of "{title}" into {tgt name}.
  Step 2: 4 ITPs 7→ NL                                                   === {src name} proof ===
                                                                         {source content}
  If x, y, z > 1 and w > 0, and log x(w) =
  24, log y(w) = 40, and log {xyz}(w) = 12,                              === {tgt name} translation ===
  then log z(w) = 60.
                                                                         Round-trip: NL 7→ Lean 4
Step 3 (NL 7→ 4 ITPs again) re-formalizes from the step-2
NL. The Lean 4 output:                                                   Translate the following natural language
                                                                         theorem statement into Lean 4. Do not
  Step 3: NL 7→ Lean 4 (second round)                                    prove the theorem; leave the proof body
                                                                         as sorry.
  theorem log problem (x y z w : R) (hx :
  x > 1) (hy : y > 1) (hz : z > 1) (hw :                                 === Natural language statement ===
  w > 0)                                                                 {nl}
  (h1 : Real.log w / Real.log x = 24)                                    === Lean 4 statement ===
  (h2 : Real.log w / Real.log y = 40)
  (h3 : Real.log w / Real.log (x * y * z)
                                                                         Round-trip: Lean 4 7→ NL
  = 12) :
  Real.log w / Real.log z = 60 := by sorry                               Describe the following Lean 4 theorem
                                                                         statement in natural language. Give a
The step-1 and step-3 Lean 4 outputs are syntactically close             concise mathematical statement of what
and express the same real-valued statement (modulo the                   the theorem claims.
theorem name), illustrating round-trip stability for this theo-
rem. However, a subtle semantic shift occurs relative to the

                                                                  18
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

  === Lean 4 statement ===                                             Illustrative example: comp commute. We show the
  {lean4}                                                              complete statement-mode file for comp commute (func-
  === Natural language description ===
                                                                       tion composition commutativity) in all four ITPs.3 This file
                                                                       defines composition and identity, then states seven lemmas
  Round-trip: NL 7→ 4 ITPs
                                                                       about commutativity with proof bodies replaced by place-
                                                                       holders, exactly the input an LLM receives during statement
  Translate the following natural language                             translation. The four versions illustrate how the same mathe-
  theorem statement into formal statements                             matical content is expressed differently across foundations:
  in all four ITPs. Leave proof bodies as
  sorry or the equivalent placeholder in                                 Lean 4
  each system.
                                                                         universe u v w
  === Natural language statement ===
  {nl}                                                                   namespace CompCommute

  === Lean 4 ===                                                         variable {a : Type u} {b : Type v} {c : Type w}
  === Isabelle ===                                                       def comp {a b c} (g : b -> c) (f : a -> b) : a -> c := fun
  === Rocq ===                                                           ,→ x => g (f x)
                                                                         def id {a} : a -> a := fun x => x
  === HOL Light ===
                                                                         axiom comp_assoc :
                                                                           forall {a b c d} (h : c -> d) (g : b -> c) (f : a -> b),
  Round-trip: 4 ITPs 7→ NL                                                 comp h (comp g f) = comp (comp h g) f
                                                                         axiom comp_id_l : forall {a b} (f : a -> b), comp (id) f = f
                                                                         axiom comp_id_r : forall {a b} (f : a -> b), comp f id = f
  The following formal theorem statements
  all describe the same mathematical                                     def commute {a} (f g : a -> a) : Prop := comp f g = comp g f
  theorem. Give a concise natural
                                                                         theorem commute_symm {a} (f g : a -> a) :
  language description of what the theorem                                 commute f g -> commute g f := by sorry
  claims.                                                                theorem commute_with_id_l {a} (f : a -> a) : commute f (id)
                                                                         ,→ := by sorry
                                                                         theorem commute_with_id_r {a} (f : a -> a) : commute (id) f
  === Lean 4 ===                                                         ,→ := by sorry
  {lean4}                                                                theorem commute_refl {a} (f : a -> a) : commute f f := by
  === Isabelle ===                                                       ,→ sorry
                                                                         theorem commute_congr {a} (f1 f2 g1 g2 : a -> a) :
  {isabelle}                                                               f1 = f2 -> g1 = g2 -> commute f1 g1 -> commute f2 g2 :=
  === Rocq ===                                                           ,→ by sorry
                                                                         theorem commute_transport_left_id {a} (f g : a -> a) :
  {rocq}                                                                   commute f g -> commute (comp (id) f) g := by sorry
  === HOL Light ===                                                      theorem commute_transport_right_id {a} (f g : a -> a) :
                                                                           commute f g -> commute f (comp (id) g) := by sorry
  {hol light}                                                            end CompCommute

  === Natural language description ===
                                                                         Rocq
E.3. Babel-formal Formalization Process
                                                                         Section CompCommute.
The 16 Babel-formal files originate in Lean 4 and Rocq                     Universes u v w.
                                                                           Definition comp {a b c : Type} (g : b -> c) (f : a -> b)
(adopted from the Babel-formal benchmark (Stoskopf et al.,                   : a -> c := fun x => g (f x).
                                                                           Definition id {a : Type} : a -> a := fun x => x.
2025), plus 2 new files). To complete the four-way align-
                                                                           Class FunProps := {
ment required by our benchmark design, we manually for-                      comp_assoc : forall {a b c d} (h : c -> d) (g : b -> c)
malized all 16 files in Isabelle and HOL Light. This section                   (f : a -> b),
                                                                               comp h (comp g f) = comp (comp h g) f;
describes the translation methodology, key design decisions,                 comp_id_l : forall {a b} (f : a -> b),
                                                                               comp (@id b) f = f;
and illustrative examples.                                                   comp_id_r : forall {a b} (f : a -> b),
                                                                               comp f (@id a) = f
                                                                           }.
Design principle: self-contained axiomatization. Every
                                                                           Definition commute {a : Type} (f g : a -> a) : Prop :=
Babel-formal file is designed to be self-contained: it carries               comp f g = comp g f.
                                                                           Context {FP : FunProps}.
its own definitions and axioms rather than depending on
any ITP-specific library. This property is inherited from                  Lemma commute_symm :
                                                                             forall {a} (f g : a -> a), commute f g -> commute g f.
the original Lean/Rocq sources and is preserved in the Is-                 Proof. Admitted.
                                                                           Lemma commute_with_id_l :
abelle and HOL Light translations. This axiomatized design                   forall {a} (f : a -> a), commute f (@id a).
serves two purposes: (1) it ensures that translation difficulty            Proof. Admitted.

reflects only foundational differences (type systems, proof
                                                                           3
languages, abstraction mechanisms) rather than library API                   The actual source files use Unicode Greek letters (α, β, γ)
mismatches, and (2) it makes the files independently verifi-           for type variables in Lean 4 and Rocq, and Unicode symbols (⇒,
                                                                       =⇒, ≡, λ) in Isabelle. We render these as ASCII equivalents for
able without installing large library ecosystems.                      typographic consistency.


                                                                  19
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

  Lemma commute_with_id_r :                                        ‘!f:A->A. commute myId f‘;;
    forall {a} (f : a -> a), commute (@id a) f.                  let commute_refl = ‘!f:A->A. commute f f‘;;
  Proof. Admitted.                                               let commute_congr =
  Lemma commute_refl :                                             ‘!f1 f2 g1 g2:A->A.
    forall {a} (f : a -> a), commute f f.                            f1 = f2 ==> g1 = g2 ==>
  Proof. Admitted.                                                   commute f1 g1 ==> commute f2 g2‘;;
  Lemma commute_congr :                                          let commute_transport_left_id =
    forall {a} (f1 f2 g1 g2 : a -> a),                             ‘!f g:A->A.
    f1 = f2 -> g1 = g2 ->                                            commute f g ==>
    commute f1 g1 -> commute f2 g2.                                  commute (myComp myId f) g‘;;
  Proof. Admitted.                                               let commute_transport_right_id =
  Lemma commute_transport_left_id :                                ‘!f g:A->A.
    forall {a} (f g : a -> a),                                       commute f g ==>
    commute f g -> commute (comp (@id a) f) g.                       commute f (myComp myId g)‘;;
  Proof. Admitted.
  Lemma commute_transport_right_id :
    forall {a} (f g : a -> a),
    commute f g -> commute f (comp (@id a) g).                 Several differences are visible even in this simple file.
  Proof. Admitted.
End CompCommute.                                               Lean 4 uses universe-polymorphic type variables ({α :
                                                               Type u}) with implicit arguments; Rocq bundles the func-
                                                               tion axioms into a typeclass (Class FunProps) and
Isabelle
                                                               threads the instance via Context; Isabelle redefines com-
theory comp_commute
                                                               position and identity as myComp/myId (avoiding name
  imports Main                                                 clashes with the standard library’s o and id); and HOL
begin
                                                               Light states lemmas as bare quoted terms (not wrapped
definition myComp ::
    "(’b => ’c) => (’a => ’b) => (’a => ’c)"                   in prove) since statement-mode files contain no proofs.
  where "myComp g f == (%x. g (f x))"
definition myId :: "’a => ’a"
                                                               The placeholder mechanisms also differ: sorry (Lean/Is-
  where "myId == (%x. x)"                                      abelle), Admitted (Rocq), and omission of prove (HOL
lemma comp_assoc:                                              Light).
  "myComp h (myComp g f) = myComp (myComp h g) f"
  by sorry
lemma comp_id_l: "myComp myId f = f" by sorry
                                                               For files with algebraic structure hierarchies (e.g.,
lemma comp_id_r: "myComp f myId = f" by sorry                  group, ideals, lattice like), the differences
definition commute ::                                          are more pronounced: Lean/Rocq typeclasses become
    "(’a => ’a) => (’a => ’a) => bool"
  where "commute f g == myComp f g = myComp g f"
                                                               Isabelle locales (e.g., locale group = fixes
                                                               mul ... assumes mul assoc ...)             and HOL
lemma commute_symm:
  "commute f g ==> commute g f" by sorry                       Light parameterized predicates (e.g., is group
lemma commute_with_id_l: "commute f myId" by sorry
lemma commute_with_id_r: "commute myId f" by sorry             (mul:A->A->A) (e:A) (ginv:A->A) <=>
lemma commute_refl: "commute f f" by sorry
lemma commute_congr:
                                                               ...). Lean/Rocq class inheritance (e.g., GroupComm
  "f1 = f2 ==> g1 = g2 ==>                                     extending Group) becomes locale composition (locale
    commute f1 g1 ==> commute f2 g2"
  by sorry                                                     group comm = group +) in Isabelle and predicate
lemma commute_transport_left_id:
  "commute f g ==>
                                                               conjunction in HOL Light.
    commute (myComp myId f) g"
  by sorry
lemma commute_transport_right_id:                              Proof translation strategies. Proof styles differ across
  "commute f g ==>
    commute f (myComp myId g)"                                 ITPs. Isabelle: We wrote all proofs as structured Isar
  by sorry
end
                                                               proofs, using calc chains for equational reasoning and
                                                               Isabelle’s automation (simp, metis, blast) for routine
                                                               steps. HOL Light: For simpler files (e.g., comp commute,
HOL Light                                                      group), we wrote complete tactic proofs. For the group
                                                               file, a key technique is the “babel group” bridge: we embed
let myComp = new_definition
  ‘myComp (g:B->C) (f:A->B) = (\x:A. g (f x))‘;;               the parameterized group into HOL Light’s native group
let myId = new_definition
  ‘myId = (\x:A. x)‘;;
                                                               type via a definitional bridge, allowing reuse of the standard
                                                               grouptheory.ml library lemmas while maintaining the
let comp_assoc =
  ‘!h g f. myComp h (myComp g f)                               axiomatized interface.
           = myComp (myComp h g) f‘;;
let comp_id_l = ‘!f:A->B. myComp myId f = f‘;;
let comp_id_r = ‘!f:A->B. myComp f myId = f‘;;
                                                               For the most complex files (notably polynomial), we
                                                               adopted an axiomatic strategy in HOL Light: benchmark
let commute = new_definition
  ‘commute (f:A->A) (g:A->A) <=>                               lemmas are stated as axioms (new axiom) rather than de-
   myComp f g = myComp g f‘;;
                                                               rived. This is a benchmark engineering choice rather than
let commute_symm =                                             a proof-exchange claim: (1) the corresponding mathemati-
  ‘!f g. commute f g ==> commute g f‘;;
let commute_with_id_l =                                        cal development is checked in Lean 4, Rocq, and Isabelle;
  ‘!f:A->A. commute f myId‘;;
let commute_with_id_r =                                        (2) HOL Light’s lack of locale/typeclass abstractions makes
                                                               certain proof structures (e.g., nested ring–polynomial locale

                                                          20
                      ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

contexts with 30+ parameters) prohibitively verbose to repli-          2. Extract the generated theorem block from the verified
cate; and (3) the axioms still serve the benchmark’s purpose              model output.
since the HOL Light file is used only as a source or target for
LLM translation, not as a trust root. Definitions and helper           3. Rename the assumed theorem to stmt assumed.
predicates (e.g., is poly context, which bundles 30+                   4. Rename the goal theorem to beq goal.
ring and polynomial axioms into a single predicate) are still
fully specified, ensuring that name resolution, type checking,         5. Replace the goal proof with a restricted proof search and
and file structure are exercised by the verifier.                         run Lean.

Summary statistics. Across the 16 files (2,902 lines                   Deterministic restricted search. Liu et al. (2025a) define
in Lean 4; 2,725 in Rocq), the Isabelle translations to-               BEq through a restricted transformation function: first try
tal 2,966 lines, nearly isomorphic to the originals, with              Lean’s exact?, then sample tactic sequences from an LLM
the slight increase due to locale declaration syntax and               under a restricted primitive set. Their ablations show that
explicit imports headers. The HOL Light translations                   bidirectionality is important and that restricting the prim-
total 2,407 lines. Although they are shorter overall, indi-            itive set controls false positives. We preserve this design
vidual lemma signatures are longer because they use ex-                principle but make the transformation search deterministic.
plicit universal quantification over structure parameters and          The check first runs exact?; the attempt is accepted only
the is poly context bundled-predicate pattern; the ax-                 if Lean’s suggestion explicitly references stmt assumed.
iomatic strategy used for the most complex files reduces               If this fails, the checker tries tactics corresponding to the
proof-side line count. All 16 Isabelle and HOL Light files             normal primitive set: exact, apply, rw, reverse rewrit-
compile cleanly in Isabelle 2024 and HOL Light (latest git),           ing, intro/intros, constructor, ext, local have,
respectively.                                                          case splitting, and existential use. Each tactic is instanti-
                                                                       ated so that a successful proof must use stmt assumed,
F. Semantic Equivalence Checking Details                               preventing standalone automation from proving the goal
                                                                       independently of the assumed statement.
This appendix describes the BEq protocol, provides per-
model directional breakdowns, documents entailment asym-               Interpretation. BEq is a Lean-checked but incomplete
metry, and gives examples of verified-but-semantically-                equivalence test. A pass is witnessed by Lean proofs of
incorrect translations.                                                both entailments. A failure means only that the determinis-
                                                                       tic restricted search did not establish equivalence; logically
F.1. BEq Protocol                                                      equivalent statements can still fail when they require trans-
                                                                       formations outside the implemented cascade, exceed Lean’s
The BEq check tests whether a verified translation preserves           search limits, or are not extracted into the expected theorem
the mathematical meaning of the reference theorem. In this             shape.
paper, BEq is applied to verified Lean 4 target translations.
Given a generated Lean statement G and the reference Lean
                                                                       F.2. Per-Model Directional Breakdown
statement R, BEq constructs two entailment problems:
                                                                       Table 21 reports BEq pass rates broken down by model and
• Forward (G ⊢ R): Assume G as an axiom; attempt to                    source prover.
  prove R.
                                                                       Table 21. BEq pass rate by model and source 7→ Lean 4 direction
• Backward (R ⊢ G): Assume R as an axiom; attempt to                   (pass/verified).
  prove G.                                                                Model            Rocq 7→ Lean    Isa 7→ Lean   HOL 7→ Lean             Total

                                                                          Claude Sonnet 4.6 36/43 (83.7%) 1/3 (33.3%) 25/28 (89.3%)      62/74 (83.8%)
                                                                          DeepSeek-V4-Pro 16/42 (38.1%) 7/18 (38.9%) 14/24 (58.3%)       37/84 (44.0%)
A translation passes BEq iff both directions succeed.                     Gemini 3.1 Pro     3/7 (42.9%)       —              —            3/7 (42.9%)
                                                                          GPT-5.5           5/20 (25.0%)       —         5/9 (55.6%)     10/29 (34.5%)
Forward-only means the generated statement is stronger                    Qwen3-235B        29/58 (50.0%) 21/40 (52.5%) 12/30 (40.0%)   62/128 (48.4%)
than the reference; backward-only means it is weaker.                     All models       89/170 (52.4%) 29/61 (47.5%) 56/91 (61.5%) 174/322 (54.0%)


Lean construction. Each directional check is compiled                  BEq pass rates vary by model and source direction.
as an independent Lean file:                                           Claude Sonnet 4.6 is strongest overall, while GPT-5.5 and
                                                                       DeepSeek-V4-Pro have low BEq rates despite producing
1. Split the reference file into a header and theorem block;           verified Lean statements. Across directions, HOL Light 7→
   the reference header supplies the Lean imports, open                Lean has the highest aggregate BEq rate (61.5%), followed
   commands, and options used for the check.                           by Rocq 7→ Lean (52.4%) and Isabelle 7→ Lean (47.5%).

                                                                  21
                          ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

F.3. Forward vs. Backward Entailment                                   the forward direction. This is another false negative from
                                                                       tactic limitations.
Table 22 reports the breakdown of entailment directions
among verified translations.
                                                                       Limitations. The tactic cascade is deliberately conserva-
Table 22. Entailment direction breakdown for verified source 7→        tive: it uses only standard Lean 4 automation and does not at-
Lean 4 translations. “Both” = BEq pass; “BwdOnly” = reference          tempt custom proof search. This means that some backward-
entails generated but not vice versa (weaker translation).             only and neither-direction cases may be logically equivalent
                                                                       to the reference but beyond the cascade’s reach. Prototype
     Model               Checked Both Neither FwdOnly BwdOnly
                                                                       extensions to Rocq (using auto, eauto, lia, etc.), Is-
     Claude Sonnet 4.6       74    62    10        0        2
     DeepSeek-V4-Pro         84    37    40        0        7
                                                                       abelle (using auto, blast, sledgehammer, etc.), and
     Gemini 3.1 Pro           7     3     4        0        0          HOL Light (using MESON TAC, ARITH TAC, etc.) exist,
     GPT-5.5                 29    10    18        0        1
     Qwen3-235B             128    62    60        0        6
                                                                       but this paper reports only the Lean 4 deployment; evaluat-
                                                                       ing non-Lean BEq at scale remains future work.
     All models             322   174   132        0       16


All 16 asymmetric cases are backward-only; no model pro-               G. Infrastructure Details
duces any forward-only cases (translations stronger than               Section 3.3 rests on one invariant: every accelerated backend
the reference). This pattern is consistent with weakening:             must be observationally equivalent to checking the gener-
dropping hypotheses, loosening types, or shifting to a more            ated artifact in isolation. Concatenating generated files into
general formulation that the reference can still imply. Most           one prover session is unsound for this benchmark because
failures, however, fail in both directions (132 cases). Addi-          later artifacts could depend on earlier declarations and top-
tionally, 26 verified records have extraction errors and are           level-name collisions could turn otherwise valid artifacts
counted as BEq failures in the aggregate results.                      into failures.

F.4. Failure Examples                                                  Toolchain manager. The released itpeval CLI installs
We illustrate three classes of BEq failures from DeepSeek-             and runs proof assistants under a common prefix. Each
V4-Pro’s backward-only cases.                                          prover adapter exposes installation and checking entry
                                                                       points, and run itp() materializes a prover-specific task
Genuine          semantic         weakening. Theorem                   directory before invoking the native binary. The adapter
amc12a 2021 p3 asks to show x − y = 14238                              returns a structured result containing exit status, wall-clock
given constraints on x, y. The reference uses integer                  time, captured logs, and backend metadata. Adding a new
coercion (↑x - ↑y = (14238:Z)), while DeepSeek                         prover requires only an adapter that maps generated source
generates natural-number subtraction (x - y = 14238).                  text to a native check task and returns this result object.
Since N subtraction truncates at zero, the generated
statement is strictly weaker. The reference entails the                State-isolated resident verification. Cold checking is
generated (backward), but not vice versa (forward).                    simple but too slow for large cross-ITP evaluation. The
                                                                       resident layer therefore amortizes startup while preserving
Definitional equivalence beyond the cascade. Theorem                   per-file semantics. Lean requests are fresh synthetic files,
amc12a 2003 p5 encodes digit constraints. The refer-                   Rocq requests are followed by Reset Initial, Isabelle
ence uses Nat.ofDigits 10 [0,1,C,M,A], while                           requests are temporary theories in server sessions, and HOL
DeepSeek inlines the arithmetic as 10000*A + 1000*M                    Light requests use either collision-aware worker packing or
+ 100*C + 10*1 + 0. These are definitionally equal                     a forkserver whose child exits after each request.
in Lean 4, but the tactic cascade cannot close the forward di-         Table 23. Resident backend semantics. Each backend amortizes
rection. This is a false negative: the statements are logically        setup cost while preserving one generated artifact as the evaluation
equivalent, but BEq reports backward-only.                             unit.

                                                                               Prover   Backend    Reuse            Isolation
Structural reformulation. Theorem amc12 2000 p1
                                                                               Lean 4 pool/server compiler workers fresh file
has the reference state hypotheses as separate binder argu-                    Rocq     REPL pool persistent proc.      Reset Initial.
ments ((h0 : i ̸= m ∧ ...) (h1 : i*m*o                                         Isabelle server-batch persistent session temp. theories
                                                                               HL       resident pool preloaded OCaml collision packing
= 2001)), while DeepSeek bundles everything into a                             HL       forkserver    preloaded parent child exit
single implication ((i ̸= m ∧ ... ∧ i*m*o =
2001) → ...). The two formulations are logically
equivalent, but the cascade hits a recursion depth limit on            Scheduling, caching, and bisection. Each generated
                                                                       record is assigned an environment key consisting of the

                                                                  22
                                                  ITPE VAL: Benchmarking Formal Translation Across Interactive Theorem Provers

target prover, benchmark mode, imports, and backend con-                                                                                     new benchmark data by appending records to the data files
straints. The scheduler groups compatible records, orders                                                                                    (every theorem must have all four ITP variants).
groups by estimated cost, and dispatches them to the fastest
backend that preserves per-file semantics. Strict filters are                                                                                Compute resources. All LLM generation was performed
deliberately one-sided: they can reject invalid artifacts, such                                                                              through provider APIs (OpenAI, Anthropic, Google, Open-
as proof-mode outputs containing placeholders, but they                                                                                      Router); no local GPU compute was required. ITP verifi-
can never turn an artifact into a success. For batch-capable                                                                                 cation is CPU-only and runs on any machine with the four
backends, failures are localized by adaptive bisection until                                                                                 toolchains installed. Per-record verification telemetry (wall-
per-record labels are recovered.                                                                                                             clock time, backend provenance, cache status) is included
                                                                                                                                             in the released JSONL checkpoints.
Checkpointing and telemetry. Verification writes
                                                                                                                                             The autoformalization round-trip experiment uses a cu-
append-only JSONL checkpoints keyed by stable record
                                                                                                                                             rated 100-record subset of miniF2F, selected to avoid the
identifiers, so interrupted runs resume without losing
                                                                                                                                             test split’s ∼62% mathd dominance (all 60 non-mathd
completed labels. Each checked record stores the original
                                                                                                                                             test records plus 40 randomly sampled mathd records,
generated text, pass/fail label, first diagnostic, wall-clock
                                                                                                                                             seed=42). Both single-ITP (NL 7→ Lean 4 7→ NL 7→ Lean 4)
time, backend name, environment key, scheduling metadata,
                                                                                                                                             and multi-ITP (NL 7→ 4 ITPs 7→ NL 7→ 4 ITPs) cycles are
and cache status. This telemetry distinguishes model
                                                                                                                                             included.
failures from verifier or toolchain failures and enables
cold-equivalence audits of resident backends.
                                               negative cache                                          batch bisection
                                                 reject only                                            recover labels


 Generated artifacts         Safe preflight                Multi-level cache            Environment key          Cost-aware scheduler
   JSONL shards               strict filters              exact + normalized            prover + imports            group by env




                                                        Transactional verification API
                                               begin_transaction / check / diagnose / rollback




           Lean 4                     Rocq                        Isabelle/HOL                HOL Light                  HOL Light
     pool / lean –server          REPL / pool                      server-batch              resident pool               forkserver
          fresh file              Reset Initial                 temporary theories         collision packing             child exits

                                                   diagnostics                  provenance
                                                phase + first error          backend + env key

                       Cold-equivalence audit                     CheckResult                    Verifier daemon
                         same native labels              pass/fail + logs + telemetry          shared warm sessions




Figure 10. Expanded infrastructure view for the state-isolated
verification service. The same architecture is summarized in the
main text.

G.1. Reproducibility
All code, data, and evaluation artifacts are available in the
public itpeval release. The repository includes: (1) the
complete benchmark data in structured JSON format (1,560
statement files and 296 proof files across four ITPs), (2) the
evaluation pipeline with both batch and synchronous execu-
tion modes supporting all five models, (3) bootstrap scripts
that install all four ITP toolchains on macOS and Linux,
(4) all raw model outputs and native ITP verification results,
and (5) scripts to reproduce all tables and figures in this
paper.
The evaluation pipeline is designed for end-to-end repro-
ducibility. LLM translation and ITP verification are decou-
pled: translations can be generated on any machine with
API keys, while verification requires the ITP toolchains and
can run separately on the same pre-generated outputs. All
runs produce checkpointed JSONL files that support safe
interruption and resumption. The pipeline is also extensible:
new models can be added with a single configuration line,
new providers by implementing a dispatch function, and

                                                                                                                                        23
