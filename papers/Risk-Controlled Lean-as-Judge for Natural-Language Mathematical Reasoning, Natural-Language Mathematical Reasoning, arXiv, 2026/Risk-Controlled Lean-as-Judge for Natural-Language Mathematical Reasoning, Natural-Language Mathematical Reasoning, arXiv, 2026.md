                                                                    Risk-Controlled Lean-as-Judge for
                                                                Natural-Language Mathematical Reasoning
                                               Pauline Bourigault                       Xiaotong Ji                    Matthieu Zimmer
                                             Imperial College London                Huawei Noah’s Ark Lab            Huawei Noah’s Ark Lab

                                                             Rasul Tutunov                               Haitham Bou-Ammar
                                                          Huawei Noah’s Ark Lab                          Huawei Noah’s Ark Lab
                                                                                                           UCL Centre for AI

                                                               Abstract                          incorrect answer, but it may also reflect an ill-typed
                                                                                                 formalization, missing library context, or a proof-
                                             Lean is increasingly used to judge natural-
arXiv:2605.28365v1 [cs.AI] 27 May 2026




                                             language mathematical answers, but its signal       search timeout. Treating proof failure as a negative
                                             is partial: many answers never formalize, and       correctness signal therefore risks conflating mathe-
                                             a failed proof may reflect an ill-typed state-      matical incorrectness with lack of formal coverage.
                                             ment or a missing library fact, not a wrong            In our pipeline, this asymmetry appears as a
                                             answer. On MATH-500 we show this signal             sharp reliability gap. When the answer classes hold-
                                             is (i) sharply coverage-dependent, that is the      ing most of the model’s sampled solutions are for-
                                             proof-winning answer is correct 96% of the
                                                                                                 mally proved, raw formal selection has a low error
                                             time at high proved coverage but 20% at low,
                                             and (ii) sparse and often unfaithful: a 7B auto-    rate; when few of those solutions land in a proved
                                             formalizer proves a class for only 28% of prob-     class, its error rate rises sharply. A second view
                                             lems, and a manual audit finds only ≈ 43% of        gives the same message: a proof is reliable when
                                             those proofs faithful. We propose C OV C AL, a      the proved answer clearly outweighs the highest-
                                             selector over Lean-trace diagnostics that certi-    weight unresolved rival, that is the most-sampled
                                             fies a finite-sample selective-risk bound on ac-    answer class Lean left unresolved, but becomes
                                             cepted answers or abstains, under two regimes       unsafe when a heavily sampled rival remains un-
                                             (a conservative Bonferroni bound and a tighter
                                                                                                 resolved. We refer to this empirical pattern as a
                                             dev-then-cal rule). Feasibility depends on auto-
                                             formalization coverage: with the 7B formalizer      coverage cliff : formal selection is accurate when
                                             the signal is too sparse and Bonferroni abstains    proofs cover most of the sampled answer mass and
                                             on all 20 bootstrap partitions, whereas a prover-   unreliable otherwise.
                                             specialized formalizer reaches 79% coverage            This motivates a partial-observation view of
                                             and flips it to feasible on 17 of 20, accepting     Lean-based answer selection (Figure 1). The sys-
                                             ≈ 48% of problems at 0.98 accepted accuracy.        tem does not observe the truth or falsity of every
                                             Since self-consistency alone is already 91% ac-
                                                                                                 candidate answer. It observes only which normal-
                                             curate, our contribution is a precise account
                                             of when, and with which formalizer, a partial       ized answer classes reach a usable Lean statement
                                             formal signal can be trusted under risk control.    and which of those are proved. An answer class is
                                                                                                 a group of candidate strings that denote the same
                                                                                                 final answer, such as 1/2, 0.5, and 2/4. Candi-
                                         1   Introduction
                                                                                                 date classes that are not formalized or not proved
                                         A Lean-kernel-checked proof is strong positive          are therefore unresolved, not automatically wrong.
                                         evidence for the formal statement that Lean has         C OV C AL uses simple diagnostics of this partial ob-
                                         checked. Recent NLP systems use this signal by          servation, that is typed coverage, proved coverage,
                                         translating natural-language question–answer pairs      unresolved rival mass, and formal margin, and ac-
                                         into Lean, attempting proof search, and preferring      cepts a formal answer only when a predeclared rule
                                         candidates whose formal proofs succeed (Yao et al.,     satisfies a finite-sample selective-risk certificate.
                                         2025; Liu et al., 2025). Our question is comple-           The threshold rule is chosen from a fixed finite
                                         mentary: when should a downstream system trust          grid, where each cell sets one cutoff for typed cov-
                                         this formal signal, and when should it treat the        erage, proved coverage, and the formal margin. We
                                         signal as out-of-coverage? The distinction matters      report two certification regimes. The Bonferroni
                                         because proof failure is not the same as mathe-         regime searches over the whole grid on the calibra-
                                         matical falsity. A failed attempt may reflect an        tion split and applies a union-bound correction for
Figure 1: C OV C AL treats Lean as a partial-observation judge: trust formal evidence when coverage is sufficient,
and abstain when coverage is too low. The method couples Lean-based formal traces with finite-sample selective
prediction.


this search. The dev-then-cal regime chooses the              splits), whereas a prover-specialized formalizer
threshold on an independent development split and             at 79% coverage flips it to feasible (17/20).
certifies that single threshold once on the calibra-
tion split. Both regimes certify only the accepted        2    Formal Verifiers as NLP Judges
formal predictions under their assumptions; neither
                                                          A general Lean-based judging pipeline has four
certifies fallback answers or unresolved candidates.
                                                          stages. First, a candidate final answer is extracted
Contributions.                                            from a natural-language solution. Second, the prob-
                                                          lem and candidate answer are translated into one
1. Coverage cliff. On MATH-500, the proof-                or more Lean statements. Third, Lean attempts
   winning answer—the highest-weight answer               to elaborate each statement. Fourth, proof search
   class with a Lean proof—is correct 96% of the          attempts to close the elaborated statement. A ver-
   time at high proved coverage but only 20% at           ified proof gives strong positive evidence for the
   low coverage. Hence, a Lean proof is reliable          formal statement, but any stage can fail for reasons
   only when coverage and margin are high.                unrelated to the truth of the original informal an-
                                                          swer. Autoformalization may change the semantics
2. A real but sparse and imperfect signal. The            of the problem. Elaboration may fail because of
   formal signal must be faithfulness-audited, not        syntax, type-class inference, missing imports, or
   read as correctness: Lean proves a class for only      library mismatch. Proof search may time out even
   28% of problems, and a manual audit finds only         for true statements. Hence, the absence of a proof
   ≈ 43% of those proofs faithful to the problem          is a heterogeneous event, not a mathematical label.
   (the rest are true-but-irrelevant or trivial X = X        Prior work demonstrates the usefulness of this
   identities).                                           pipeline. FANS uses Lean 4 to formalize question–
                                                          answer pairs and assist answer selection (Yao et al.,
3. Method. We consider formal answer selec-
                                                          2025). Safe uses Lean 4 for retrospective step-
   tion as a partial-observation selective-prediction
                                                          aware verification of natural-language mathemati-
   problem, propose C OV C AL, which is a risk-
                                                          cal reasoning (Liu et al., 2025). These works show
   controlled selector over coverage diagnos-
                                                          that formal proof can improve math reasoning sys-
   tics with finite-sample certificates under two
                                                          tems. Our question is complementary: how much
   regimes, and prove that unresolved inequivalent
                                                          of the candidate-answer space is visible to the for-
   answer classes cannot be certified from formal
                                                          mal pipeline, and when is that partial trace suffi-
   observations alone without abstention.
                                                          cient for answer selection?
4. Feasibility is formalizer-governed. Certificate           The answer requires separating three notions that
   feasibility is governed by autoformalization cov-      are often collapsed: (i) whether a candidate answer
   erage: a 7B formalizer is too sparse for any Bon-      is mathematically correct, (ii) whether its intended
   ferroni certificate (0/20 bootstrap dev/cal/test       formal statement is well represented in Lean, and
(iii) whether the current prover can decide it within     The five statuses are defined in Appendix F
budget. C OV C AL does not solve (i)–(iii). Instead,      (proved is a kernel-checked proof; typechecked
it measures the observable mass of candidates for         elaborates but is unproved; the rest are failures);
which (ii) and (iii) are available, then calibrates the   optional decisive negation/inequivalence statuses
risk of trusting the resulting formal selection.          are supported but not required.
                                                             For each answer class c, define class-level indi-
3   Problem Setup                                         cators
We first describe the objects used by the selector.
As a running example, suppose a model samples                 Pc (x) = I{∃j : ex (aj ) = c, sj = proved}, (4)
K = 32 solutions to the same problem. Sev-                    Tc (x) = I{∃j : ex (aj ) = c, sj ∈ Styp },
eral samples may end with surface forms such as                Styp = {proved, typechecked, timeout}.
1/2, 0.5, and 2/4; these should count as one final-                                                 (5)
answer class rather than three different answers.
Another group of samples may end with 3/4. C OV-          Styp is the elaborated-statement set; timeout qual-
C AL reasons over these normalized classes and            ifies since proof search runs only after elabora-
their total weights, not over raw strings.                tion. The formal observation O(x) consists of an-
   Let x ∈ X be a natural-language mathematical           swer classes, class weights, statuses, proof artifacts
problem with reference answer a⋆ (x). A gener-            when available, error logs, and the fixed prover
ator or ensemble produces K candidate answers             budget. A selector returns an answer class ĉ(x), a
a1 , . . . , aK with nonnegative weights qj (x) satis-    representative answer â(x), or abstains with ⊥.
fying K
          P
              j qj (x) = 1. The weights may be self-      4     Coverage Diagnostics
consistency frequencies (Wang et al., 2023), nor-
malized reranker scores, or a uniform distribution        The diagnostics answer three questions about the
over sampled candidates.                                  formal trace. How much candidate mass reached a
                                                          well-formed Lean statement? How much candidate
Answer classes. Raw candidate strings are a poor
                                                          mass was actually proved? And, if a class was
unit of selection: 1/2, 0.5, and 24 may be the same
                                                          proved, does it dominate the strongest unresolved
answer, while two candidates with the same surface
                                                          rival? These quantities are pipeline-agnostic and
form may correspond to different formalizations.
                                                          can be computed from answer-class weights and
We therefore map candidates to normalized answer
                                                          Lean status logs.
classes
                   ex (aj ) ∈ C(x),              (1)      Definition 1 (Typed coverage). The typed coverage
using answer extraction, algebraic simplification,        mass is
exact string normalization, or formal equivalence                               X
                                                                    Ctyp (x) =       Qc (x)Tc (x).       (6)
checks when available. The class weight is
              X                  X                                                c∈C(x)
 Qc (x) =          qj (x),            Qc (x) = 1.
           j:ex (aj )=c           c∈C(x)
                                                             Typed coverage measures how much candidate
                                                 (2)      probability reached a well-formed Lean statement.
All coverage, margin, and selection quantities are        Low typed coverage points to autoformalization,
computed over classes instead of raw candidates.          parsing, answer-normalization, or library-interface
This prevents an unresolved duplicate of an already       failure.
proved answer from being treated as a rival.              Definition 2 (Proved coverage). The proved cover-
                                                          age mass is
Formal observation. For each pair (x, aj ), a for-
malization module attempts to produce one or more                               X
                                                                    Cprf (x) =       Qc (x)Pc (x).      (7)
Lean artifacts. A verifier elaborates each artifact
                                                                                  c∈C(x)
and attempts proof search. We summarize the best
status for candidate aj by                                   Proved coverage measures how much answer-
    sj ∈ S,                                               class probability is positively decided by the for-
                                                          mal pipeline. It is distinct from proof existence:
    S = {proved, typechecked, illtyped,
                                                          proving a low-weight class may be much less infor-
            timeout, unformalized}.                (3)    mative than proving the dominant class.
Definition 3 (Unresolved rival mass and formal              Acceptance rule. For a threshold tuple τ =
margin). If at least one class is proved, let               (τtyp , τprf , τM ), define
           c+ (x) = arg max Qc (x)                    (8)      Aτ (x) = I{Ctyp (x) ≥ τtyp , Cprf (x) ≥ τprf ,
                          c:Pc (x)=1

be the highest-weight proved class. The unresolved                         M (x) ≥ τM , gF (x) ̸= ⊥,
rival mass is                                                              no conflict}.                       (12)
       Runres (x) =         max            Qc (x),    (9)   If Aτ (x) = 1, C OV C AL returns gF (x). If Aτ (x) =
                      c̸=c+ (x):Pc (x)=0
                                                            0, the selective version abstains. A full-coverage
with Runres (x) = 0 when every other class is also          system may instead call a fallback gN (x) such as
proved or no rival exists. The formal margin is             self-consistency or a learned natural-language veri-
        M (x) = Qc+ (x) (x) − Runres (x),            (10)   fier; the formal selective-risk certificate below ap-
                                                            plies only to the accepted formal predictions, not
and M (x) = −∞ if no class is proved.
                                                            to fallback outputs. Algorithm 1 (Appendix B)
   The margin captures the main reliability condi-          summarizes the instance-level decision rule.
tion: a proof of one answer is not decisive if a
higher-weight inequivalent answer class remains             Risk-controlled threshold selection. Given a tar-
unresolved.                                                 get selective-risk level ϵ and a finite grid T , C OV-
                                                            C AL chooses the least conservative rule whose cal-
Conflict indicators. If two inequivalent final-             ibration certificate is valid. We report two valid
answer classes are both proved for the same infor-          regimes; both produce a certificate of the form
mal problem, we mark a conflict and reject formal           “with probability ≥ 1 − δ, the selected τ̂ has pop-
selection by default. This should not be read as a          ulation selective risk at most ϵ,” but they differ in
Lean inconsistency. It usually indicates an answer-         sample efficiency.
normalization error, a semantic mismatch between               The default operational regime is Bonferroni:
generated formal statements, or incompatible auto-          optimize over the grid on the calibration split and
formalizations of the informal problem.                     pay a |T |-fold union-bound penalty. Formally,
Coverage cliffs. We use coverage cliff for the
empirical scenario in which the reliability of for-         τ̂Bonf = arg max mτ       s.t.   Uδ/|T | (kτ , mτ ) ≤ ϵ,
                                                                          τ ∈T
mal answer selection changes sharply as a func-                                                               (13)
tion of Ctyp , Cprf , Runres , or M . The hypoth-           where mτ and kτ are the number of accepted
esis is stronger than “hard examples have lower             calibration examples and accepted errors, and
proof rates”: below a coverage threshold, failed            Uα (k, m) is the one-sided Clopper–Pearson upper
or missing proofs become non-diagnostic because             bound with Uα (k, 0) = 1. If no threshold is fea-
unresolved classes may be false, unformalized, or           sible, the selective method returns reject-all. This
unproved.                                                   regime is conservative but makes no assumption
                                                            on the dependence structure between the |T | cell
5   Risk-Controlled Formal Selection                        statistics: they are jointly nested under the same
C OV C AL is a selective wrapper around a base Lean         calibration sample, so a generic union bound is the
selector. It does not require training a new theorem        safest valid statement.
prover or changing the formalizer. Its contribution            A tighter alternative is a dev-then-cal rule. First,
is to decide when the formal signal is sufficiently         a threshold τ̂DC is selected using only the devel-
covered to determine the answer.                            opment split, for example by choosing the highest-
                                                            coverage grid cell whose empirical dev error is at
Base formal selector. The base selector returns             most ϵ under a deterministic tie-break. If no such
the highest-weight proved answer class,                     cell exists, the procedure returns reject-all. Sec-
                  gF (x) = c+ (x),                   (11)   ond, the selected threshold is evaluated once on the
                                                            independent calibration split and is accepted only
with gF (x) = ⊥ if no class is proved or if a conflict
                                                            when
is detected. The returned natural-language answer
                                                                                            
                                                                           Uδ kτ̂cal , m cal
                                                                                         τ̂DC ≤ ϵ.            (14)
is a canonical representative of c+ (x). More so-                                 DC

phisticated formal selectors can be substituted, but        Because τ̂DC is a function only of the dev split, it
the coverage logic is unchanged.                            is independent of the calibration sample. Hence,
a single Clopper–Pearson bound at level δ is suffi-      and any example-level pipeline randomness, for all
cient. Theorem 2 gives the finite-sample guarantee       τ ∈T,
under i.i.d. dev/cal/deployment samples.                             R(τ ) ≤ Uδ/|T | (kτ , mτ ).      (17)
Practical choices. The default class weights are         Consequently, whenever Eq. 13 returns a feasible
self-consistency frequencies; a class is marked          threshold, the selected rule has selective risk at
proved if any of its artifacts is kernel-checked, and    most ϵ with probability at least 1 − δ.
two inequivalent proved classes trigger rejection        Accepted calibration errors at a fixed threshold are
rather than a choice. All implementation choices,        Bernoulli, so a one-sided Clopper–Pearson bound
and the quantities frozen before calibration labels      (Clopper and Pearson, 1934) controls its risk; the
are used, are listed in Appendix B.                      Bonferroni correction makes this simultaneous over
                                                         the grid, letting the threshold be chosen after seeing
6    Finite-Sample Guarantees                            calibration errors (proof in Appendix A).
The guarantee certifies the selective risk of the com-   Theorem 2 (Dev-then-cal selective-risk calibra-
plete frozen pipeline: candidate generation, answer      tion, no union bound). Partition i.i.d. samples
normalization, formalization, proof search, cover-       from the population P into an independent devel-
age computation, and formal selection. It does not       opment split Ddev and calibration split Dcal . Let
certify unresolved candidates and does not interpret     τ̂ = f (Ddev ) be any σ(Ddev )-measurable choice
failed Lean proofs as negative labels. The proba-        of threshold cell in T ∪{⊥}; in particular, τ̂ may be
bility in the guarantee is over the random draw of       the maximum-coverage dev-feasible cell with a de-
calibration and future deployment examples, in-          terministic tie-break. Let m = mτ̂cal and k = kτ̂cal
cluding any example-level randomness that is part        be the accept count and accepted-error count on
of the frozen pipeline. In the reported bootstrap        the calibration split. Define the certified output
summaries, candidate and formalization logs are          threshold
                                                                 (
fixed, so only the dev/cal/test partition varies.                   ⊥ τ̂ = ⊥, or m = 0, or Uδ (k, m) > ϵ,
                                                         τbout =
Selective risk. Let Dcal = {(Xi , Ci⋆ )}ni=1 be a                   τ̂ otherwise.
calibration set drawn i.i.d. from the same pop-          Then
ulation as future test examples, where Xi is the                                                   
problem and Ci⋆ is its normalized reference answer         Pr τbout ̸= ⊥ =⇒ R(b
                                                                              τout ) ≤ Uδ (k, m) ≤ ϵ
class. The pipeline outputs used by Aτ and gF are                                             ≥ 1 − δ. (18)
computed without inspecting Ci⋆ except for final
                                                         Because τ̂ is fixed on dev, the cal split sees a single
evaluation. For τ ∈ T , let
                                                         threshold, so the bound uses level δ rather than
             n
             X                                           δ/|T |; strict dev/cal separation is the load-bearing
     mτ =          Aτ (Xi ),                             assumption (proof in Appendix A).
             i=1
             Xn                                          dev-then-cal procedure. The selection rule, that
      kτ =         Aτ (Xi )I{gF (Xi ) ̸= Ci⋆ }.   (15)   is the highest-coverage dev-feasible cell then a
             i=1                                         single cal-side Clopper–Pearson check at level δ,
                                                         and the boundary cases it handles (empty splits,
The population selective risk is
                                                         zero accepts, all-errors, multiple ϵ targets, and the
    R(τ ) = Pr[gF (X) ̸= C ⋆ | Aτ (X) = 1],       (16)   i.i.d./measurability requirements) are given in Ap-
                                                         pendix B.
with the harmless convention R(τ ) = 0 when              Comparison of the two regimes. At our set-
Pr[Aτ (X) = 1] = 0.                                      tings (|T | = 125, δ = 0.05), Theorem 1 spends
Theorem 1 (Uniform selective-risk calibration un-        α = 4 × 10−4 per cell while Theorem 2 spends
der Bonferroni). Assume the threshold grid T is          α = 0.05 on a single cal-side bound, so the two
fixed before inspecting calibration labels, and the      regimes can disagree on feasibility for the same
pipeline used to compute Aτ and gF is fixed before       observations. The cliff (Section 8.1) is a property
calibration. If the calibration examples are i.i.d.      of the data and is identical under either regime;
from the deployment population, then with prob-          only the certificate’s verdict depends on the bound.
ability at least 1 − δ over the calibration sample       Section 8.3 reports both.
            Method                       Overall               Accepted               Acc. frac.     Test diag. UB
            Regime-independent selectors (ncal = 151, ϵ = 0.15)
            Self-consistency      0.910 [0.903, 0.916] 0.910 [0.903, 0.916] 1.000 [1.000, 1.000] 0.138 [0.131, 0.146]
            Confidence-only abst. 0.866 [0.857, 0.875] 0.969 [0.966, 0.973] 0.894 [0.884, 0.903] 0.068 [0.063, 0.072]
            Raw Lean + fallback 0.891 [0.884, 0.899] 0.891 [0.884, 0.899] 1.000 [1.000, 1.000] 0.159 [0.150, 0.168]
            Proof-existence abst. 0.193 [0.182, 0.203] 0.877 [0.857, 0.896] 0.220 [0.209, 0.231] 0.258 [0.234, 0.282]
            Calibrated formal selectors — Bonferroni regime
            C OV C AL                                         reject-all (0/20 partitions certify)
            Calibrated formal selectors — dev-then-cal regime (12/20 partitions certify)
            C OV C AL              0.194 [0.184, 0.205] 0.932 [0.914, 0.949] 0.209 [0.197, 0.220] 0.192 [0.168, 0.216]
            C OV C AL+fallback     0.905 [0.896, 0.913] 0.905 [0.896, 0.913] 1.000 [1.000, 1.000] 0.144 [0.135, 0.154]

Table 1: When C OV C AL accepts (≈ 21% of items) it is 0.93 accurate, but only dev-then-cal certifies this (12/20
partitions); Bonferroni rejects the sparse signal outright. As self-consistency alone is already 91% accurate, the
contribution is the certificate, not raw accuracy. Main MATH-500 run (Qwen2.5-Math-7B-Instruct, ncal = 151,
ϵ = 0.15; K = 20 bootstrap, seed-mean 95% interval). Test diag. UB is a held-out Clopper–Pearson bound computed
after rule selection—a diagnostic, not the certificate of Table 3; the top block is regime-independent.


No coverage, no verifier-only certificate. The                        is reliable. The main experiment uses a filtered
next proposition explains why coverage diagnostics                    MATH-500 short-answer subset (Hendrycks et al.,
are necessary.                                                        2021; Lightman et al., 2024): 378 of 500 exam-
                                                                      ples remain after excluding proof-only, diagram-
Proposition 1 (Unresolved answer classes are in-
                                                                      dependent, and non-normalizable references. The
distinguishable). Fix a problem x and a formal
                                                                      split is 76/151/151 development/calibration/test,
observation O(x). Suppose a verifier-only selector
                                                                      with ϵ = 0.15 and δ = 0.05. We also report a
h selects a proved class cs = h(O(x)), but there
                                                                      harder levels-4/5 subset of the same run, an aut-
is an unresolved answer class cu with Qcu (x) > 0,
                                                                      oformalizer ablation that swaps Qwen2.5-Coder
Pcu (x) = 0, and no formal evidence in O(x) prov-
                                                                      for Goedel-Prover-V2-8B/-32B with generation
ing, disproving, or identifying cu as equivalent to
                                                                      held fixed (Sec. 8.3), and an AMC/AIME out-of-
cs . Then there are two latent correctness assign-
                                                                      distribution set (Appendix H).
ments over the informal answer classes that are
both compatible with the same formal observation                         For each problem, Qwen2.5-Math-7B-Instruct
but disagree on whether cs is correct. Hence no                       generates K = 32 candidate solutions. We ex-
non-vacuous pointwise correctness certificate for                     tract final answers, normalize them into answer
h follows from O(x) alone unless the selector re-                     classes, and assign each class a self-consistency
solves cu , assumes it away, uses external semantic                   weight Qc . The pipeline then formalizes the
information or labels, or abstains.                                   top four answer classes and attempts Lean proof
   Intuitively, the formal log records what Lean                      search. The resulting class statuses, which are
could decide, not the truth values of classes it never                proved, typechecked, timeout, illtyped, and
resolved: an unresolved inequivalent rival leaves                     unformalized, are the only formal observations
the selected proved class and that rival equally com-                 used by C OV C AL.
patible with the same observation (proof in Ap-
                                                                        We compare self-consistency, confidence-only
pendix A). This is a certification statement, not
                                                                      abstention, raw Lean with fallback, proof-existence
an empirical claim that unresolved candidates are
                                                                      abstention, and C OV C AL with and without fall-
usually correct. Missing formal evidence is not evi-
                                                                      back. Thresholds are chosen on the calibration
dence of mathematical falsehood. Calibration turns
                                                                      split using either the Bonferroni grid certificate
the partial observation into a controlled selective
                                                                      or the dev-then-cal certificate from Sec. 6. The
problem, using Lean where coverage suffices and
                                                                      main target is ϵ = 0.15 with δ = 0.05; the
forcing abstention or fallback elsewhere.
                                                                      harder levels-4/5 subset uses the stricter ϵ = 0.10.
7   Experimental Protocol                § Code repository            Prompts (Appendix E), the candidate/formalization
                                                                      pipeline (Appendix C), the analysis log schema
We evaluate whether Lean-derived coverage di-                         (Appendix F), and filtering, hardware, and tactic-
agnostics predict when formal answer selection                        portfolio details (Appendix G) are in appendices.
       Bin                   #   Proof rate Winner acc.    only under the more sample-efficient dev-then-cal
       by proved coverage Cprf (all n = 378)               regime, and even then on only 12 of 20 partitions,
       Cprf < 0.25         283      0.035      0.20
       0.25 ≤ Cprf < 0.50 6         1.000      0.33
                                                           with the held-out test diagnostic (≈ 0.19) sitting
       0.50 ≤ Cprf < 0.75 4         1.000      1.00        above ϵ because the accepted set is small. The fall-
       Cprf ≥ 0.75          85      1.000      0.96        back variant recovers self-consistency-level overall
       by formal margin M (the 105 proved problems)        accuracy, but the certificate applies only to the for-
       M <0                 10    1.000        0.10
       0 ≤ M < 0.25          5    1.000        0.40        mal accepted predictions, not the fallback outputs.
       0.25 ≤ M < 0.5        5    1.000        0.80          The main diagnostic signal is not that hard ex-
       M ≥ 0.5              85    1.000        0.98
                                                           amples have fewer proofs. Low-margin examples
Table 2: The coverage/margin cliff on the main run. # is   can have proof existence but still be unreliable be-
problems per bin; Proof rate the fraction with a kernel-   cause a stronger unresolved rival answer remains.
proved class; Winner acc. the accuracy of the highest-     This is the empirical reason for treating unproved
weight proved class among problems with a proof. The       candidate mass as unresolved instead of false.
signal is sparse (most problems are in the lowest Cprf
bin with almost no proofs) but sharply reliable when       8.2   Faithfulness Audit and Qualitative
present: 96% at Cprf ≥ 0.75 vs 20% at Cprf < 0.25                Examples
(98% vs 10% by margin).
                                                           An automated rational-evaluation check classifies
                                                           the 314 proved artifacts as genuine (40.1%, a Q-
8     Results                                              true arithmetic identity), structural (33.4%, a true
                                                           gcd/divisor/quantified statement), trivial (22.9%,
The results support three main claims. First, the          an X = X identity), or spurious (2.5%, Q-false), so
formal signal is real but sparse: Lean proves              73.6% are non-trivial and correct. But non-trivial-
at least one answer class for only 28% of prob-            and-correct is not faithful: a true statement may
lems, and a manual audit finds only ≈ 43% of               not capture the problem. A manual audit of 45
proved statements faithful to the problem (versus          stratified examples (single annotator; diagnostic
the 74% an automated check labels non-trivial-and-         error analysis) makes the gap explicit: genuine
correct; Sec. 8.2). Second, the signal is sharply          proofs are faithful (6/6) and trivial ones are not,
coverage-dependent: the highest-weight proved              but structural statements almost never are (0/6).
class matches the reference answer 96% of the time         They assert a true side-fact or bare existence (e.g.
at high proved coverage but only 20% at low cover-         ∃n, n > 125 ∧ n = 129 for a problem whose an-
age, and 98% versus 10% binned by formal margin            swer is 129), omitting the problem’s actual condi-
(Tab. 2). Third, certifiability depends on autofor-        tion, while the audited spurious cases are classifier
malization coverage: with the 7B Qwen2.5-Coder             false-positives (e.g. (3:Q)/20 = 0.15), not real er-
formalizer the sparse signal forces Bonferroni to          rors. Reweighting the audited per-category rates
reject on all 20 bootstrap partitions (dev-then-cal        by population frequency, only ≈ 43% of proved
certifies 12/20), whereas the prover-specialized           statements are faithful, about half the 73.6% that
Goedel-Prover-V2-8B lifts coverage to 79% and              typecheck and hold. Faithful verification is thus
flips Bonferroni to feasible on 17/20 (Tab. 1 and 3).      rarer than proof success suggests, and the audited
Unless a column says calibration certificate, upper        failures are heterogeneous, including semantic drift,
bounds in answer-selection tables are held-out di-         proof-search failure on faithful statements, and ill-
agnostics computed after rule selection.                   typed statements, and supporting our treatment of
                                                           a missing proof as unresolved rather than negative.
8.1    Main Answer-Selection Results
                                                           Appendix I gives three worked examples (A)–(C):
On the main run, self-consistency is already 91%           a proof trusted when the proved class dominates the
accurate with no abstention. The formal signal             formally visible mass (A), a missing proof treated
is far sparser than the candidate signal: proof-           as unresolved rather than wrong (B), and a low-
existence and the calibrated formal selectors accept       weight or trivially formalized rival correctly dis-
only about 20–22% of test items, though their ac-          trusted by the margin (C).
cepted accuracy is high (0.88–0.93). Crucially, the
conservative Bonferroni certificate cannot use this        8.3   Ablations and Certification Regimes
sparse signal at all. It returns reject-all on every       The binding constraint on the main run is autofor-
partition. Thus, a nontrivial accepted set is certified    malization coverage: only 28% of problems reach
                                             Bonferroni (α = δ/|T |)       Dev-then-cal (α = δ)   UB ratio
         Autoformalizer (gen. fixed) ncal
                                            reject@K = 20 med cal UB reject@K = 20 med cal UB      (med)
         Qwen2.5-Coder-7B (main) 151           20/20           –            8/20          0.121       –
         Goedel-Prover-V2-8B     151           3/20          0.127          0/20          0.062    0.49×
         Goedel-Prover-V2-32B    151           7/20          0.143          3/20          0.115    0.81×

Table 3: The two certificate regimes on the main run (K = 20 bootstrap, ϵ = 0.15). Bonferroni applies α = δ/|T | =
4×10−4 over the 125-cell grid; dev-then-cal applies α = δ = 0.05 (Theorem 2). reject@K counts refusing seeds;
med cal UB is the median calibration-side bound over feasible seeds (– if none). Generation is held fixed; the
Goedel-Prover-V2 rows vary only the autoformalizer.


any proof (with the 7B Qwen2.5-Coder autoformal-             answer selection.
izer), which is what forces the conservative Bonfer-            Autoformalization and theorem proving.
roni certificate to reject and leaves the tighter dev-       LLM autoformalization and Lean/Isabelle theorem
then-cal regime feasible on only 12 of 20 partitions.        proving remain sensitive to domain, library context,
Table 3 compares the two regimes on the same                 and dependency retrieval (Wu et al., 2022; Jiang
frozen observations. Because coverage is the bot-            et al., 2023; Yang et al., 2023; Azerbayev et al.,
tleneck, we also vary the autoformalizer, holding            2023; Zheng et al., 2021; Yu et al., 2025; Patel
generation fixed. The prover-specialized Goedel-             et al., 2026; Lin et al., 2025). These works motivate
Prover-V2-8B raises proved coverage from 28%                 our treatment of proof failure as heterogeneous in-
to 79% at the same proof-winner precision (86%),             stead of as a negative label. We use Qwen2.5-Math
and this denser signal flips the certificate from in-        for generation and Qwen2.5-Coder for autoformal-
feasible to feasible: Bonferroni now certifies on 17         ization (Yang et al., 2024; Hui et al., 2024); our
of 20 partitions (versus 0 with Qwen2.5-Coder) and           contribution is the risk-controlled wrapper.
dev-then-cal on all 20, each accepting about 48%                Selective prediction and risk control. Selective
of test items at 0.98 accepted accuracy (Table 3).           classification trades coverage for risk (El-Yaniv and
Scaling the formalizer further to the 32B Goedel-            Wiener, 2010; Geifman and El-Yaniv, 2017). Risk-
Prover-V2 does not extend this gain: proved cov-             controlling prediction and conformal risk-control
erage is 64% (below the 8B’s 79%) and the certifi-           methods certify population risk for calibrated rules
cate is marginally less feasible (Bonferroni 13/20,          under distributional assumptions (Bates et al., 2021;
dev-then-cal 17/20), indicating that prover special-         Angelopoulos et al., 2024). C OV C AL adapts this
ization rather than raw model scale is what lifts            perspective to formal answer selection with partial
coverage past the feasibility threshold. The autofor-        observations: unresolved answer mass does not
malizer, not the certificate machinery, thus governs         become a larger prediction set, but instead forces
whether risk-controlled formal selection is possi-           abstention unless a coverage rule can be certified.
ble, though the faithfulness caveat of Sec. 8.2 still
applies to the underlying proofs. Additional per-            10        Conclusion
level breakdowns, ϵ-sensitivity, status-count, and           We documented a coverage cliff in Lean-as-judge
hard-subset details are reported in Appendix H.              for natural-language mathematical reasoning and
                                                             proposed C OV C AL, a selective wrapper that certi-
9   Related Work
                                                             fies risk only where enough formal evidence is visi-
Math reasoning and verifiers. Self-consistency,              ble, treating missing formal evidence as unresolved
outcome-reward models, and process-reward mod-               rather than negative. Whether its finite-sample cer-
els are common signals for natural-language math-            tificate (Bonferroni or dev-then-cal) holds depends
ematical reasoning (Wang et al., 2023; Cobbe et al.,         on autoformalization coverage: a 7B formalizer
2021; Uesato et al., 2022; Lightman et al., 2024;            leaves the signal too sparse for Bonferroni to cer-
Wang et al., 2024). Lean-based systems such as               tify any partition, whereas a prover-specialized for-
FANS and Safe instead use formal proof as a posi-            malizer at 79% coverage flips it to feasible on 17
tive correctness signal (Yao et al., 2025; Liu et al.,       of 20. C OV C AL is a conservative interface for us-
2025). Our focus is complementary: when the                  ing Lean as a judge; feasible when the formalizer
formal proof is absent, we ask whether the remain-           covers enough answer mass, but not a guarantee
ing formal trace is sufficiently covered to support          that all answers are verified.
Limitations                                             Faithfulness of proved statements. A kernel-
                                                        checked proof certifies the generated statement,
Scope of the certificate. The selective-risk guar-
                                                        not that the statement faithfully captures the infor-
antee covers only examples for which Aτ̂ (x) = 1
                                                        mal problem. An automated rational-evaluation
and a formal answer is returned. It does not certify
                                                        check of the 314 proved artifacts finds 73.6% non-
individual mathematical truth, does not assign a
                                                        trivial and correct, but our manual audit (45 strati-
label to unresolved answer classes, and does not ex-
                                                        fied examples) shows this overstates faithfulness:
tend to fallback predictions made when Aτ̂ (x) = 0.
                                                        many true structural statements assert a side-fact
Distributional assumptions. Both regimes re-            or bare existence, so only ≈ 43% of proved state-
quire exchangeability of the calibration sample         ments are faithful to the problem, and a wrong
with future test points. The dev-then-cal regime ad-    answer class is proved in 8% of problems. This
ditionally requires independence between the dev        audit is diagnostic error analysis, not benchmark-
and cal splits and that τ̂ be a function of dev only;   grade annotation (e.g., it uses a single annotator
leakage from the cal split into threshold selection     and small per-category samples) and the automated
would invalidate Theorem 2. Distribution shift be-      diagnostics alone do not flag a faithful-looking but
tween calibration and deployment also voids the         semantically drifted statement.
bound.
                                                        Ethical Considerations
Feasibility depends on the autoformalizer. The
certificate is only as good as the formal coverage      Formal verification can make mathematical reason-
it is given. With a 7B autoformalizer only about        ing systems more reliable, but overclaiming from
28% of problems are proved, and at ncal = 151 the       failed verification can mislabel correct reasoning
Bonferroni certificate returns reject-all on every      as incorrect or produce misleading training signals.
bootstrap partition (dev-then-cal certifies 12/20,      The proposed calibration framework is intended
with the held-out diagnostic sometimes exceeding        to make such limitations explicit. The work uses
ϵ on the small accepted set). A prover-specialized      public math datasets and local open models; no per-
formalizer raises coverage to 79% and makes Bon-        sonal data is involved. The main risk is that users
ferroni feasible on 17/20, so the limitation is not     may interpret calibrated acceptance as a guarantee
the certificate but the formalizer: the method is       for all examples rather than for the accepted subset
informative only when autoformalization covers          under the stated data assumptions.
enough answer mass, and the operator must supply
a sufficiently specialized formalizer. Raw scale is
                                                        References
not a substitute for specialization. The 32B Goedel-
Prover-V2 variant attains lower proved coverage         Anastasios N. Angelopoulos, Stephen Bates, Adam
                                                          Fisch, Lihua Lei, and Tal Schuster. 2024. Conformal
(64%) than the 8B (79%) and is marginally less
                                                          risk control. In International Conference on Learn-
feasible (Sec. 8.3).                                      ing Representations.
Single dataset and pipeline. The empirical evi-         Zhangir Azerbayev, Bartosz Piotrowski, Hailey
dence is from one dataset family (MATH-500), one          Schoelkopf, Edward W. Ayers, Dragomir Radev, and
candidate generator, and one proof style. We vary         Jeremy Avigad. 2023. ProofNet: Autoformalizing
                                                          and formally proving undergraduate-level mathemat-
the autoformalizer (up to a 32B prover) but cannot
                                                          ics. arXiv preprint arXiv:2302.12433.
claim the cliff or the coverage numbers transfer to
symbolic Olympiad problems, multi-step formal           Stephen Bates, Anastasios Angelopoulos, Lihua Lei,
proofs, other answer formats, or systems built on         Jitendra Malik, and Michael I. Jordan. 2021.
                                                           Distribution-free, risk-controlling prediction sets.
agentic provers with retrieval.
                                                          Journal of the ACM, 68(6):1–34.
Bootstrap and partition variability. The re-            Charles J. Clopper and Egon S. Pearson. 1934. The use
ported K = 20 bootstrap captures variance from the        of confidence or fiducial limits illustrated in the case
dev/cal/test partition but not from candidate sam-        of the binomial. Biometrika, 26(4):404–413.
pling or autoformalization stochasticity; the same
                                                        Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
observations are reused across seeds. A multi-seed        Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
re-run of generation and formalization would esti-        Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
mate the latter sources of variability.                   Nakano, Christopher Hesse, and John Schulman.
  2021. Training verifiers to solve math word prob-          Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-
  lems. arXiv preprint arXiv:2110.14168.                       cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,
                                                               Geoffrey Irving, and Irina Higgins. 2022. Solving
Ran El-Yaniv and Yair Wiener. 2010. On the founda-             math word problems with process- and outcome-
  tions of noise-free selective classification. Journal of     based feedback. arXiv preprint arXiv:2211.14275.
  Machine Learning Research, 11:1605–1641.
                                                             Peiyi Wang, Lei Li, Zhihong Shao, Runxin Xu, Damai
Yonatan Geifman and Ran El-Yaniv. 2017. Selective              Dai, Yifei Li, Deli Chen, Yu Wu, and Zhifang Sui.
  classification for deep neural networks. In Advances         2024. Math-Shepherd: Verify and reinforce LLMs
  in Neural Information Processing Systems.                    step-by-step without human annotations. In Proceed-
                                                               ings of the 62nd Annual Meeting of the Association
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul             for Computational Linguistics (Volume 1: Long Pa-
  Arora, Steven Basart, Eric Tang, Dawn Song, and              pers), pages 9426–9439.
  Jacob Steinhardt. 2021. Measuring mathematical
  problem solving with the MATH dataset. In Proceed-         Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le,
  ings of the Neural Information Processing Systems            Ed H. Chi, Sharan Narang, Aakanksha Chowdhery,
  Track on Datasets and Benchmarks.                            and Denny Zhou. 2023. Self-consistency improves
                                                               chain of thought reasoning in language models. In
Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Day-             International Conference on Learning Representa-
  iheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,              tions.
  Bowen Yu, Keming Lu, Kai Dang, Yang Fan,                   Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N.
  Yichang Zhang, An Yang, Rui Men, Fei Huang,                  Rabe, Charles Staats, Mateja Jamnik, and Christian
  Bo Zheng, Yibo Miao, Shanghaoran Quan, and 5 oth-            Szegedy. 2022. Autoformalization with large lan-
  ers. 2024. Qwen2.5-Coder technical report. arXiv             guage models. In Advances in Neural Information
  preprint arXiv:2409.12186.                                   Processing Systems.
Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda          An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao,
  Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix,           Bowen Yu, Chengpeng Li, Dayiheng Liu, Jian-
  Yuhuai Wu, and Guillaume Lample. 2023. Draft,                hong Tu, Jingren Zhou, Junyang Lin, Keming Lu,
  sketch, and prove: Guiding formal theorem provers            Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang
  with informal proofs. In International Conference on         Ren, and Zhenru Zhang. 2024. Qwen2.5-Math tech-
  Learning Representations.                                    nical report: Toward mathematical expert model via
                                                               self-improvement. arXiv preprint arXiv:2409.12122.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
  Edwards, Bowen Baker, Teddy Lee, Jan Leike, John           Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-
  Schulman, Ilya Sutskever, and Karl Cobbe. 2024.              mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
  Let’s verify step by step. In International Conference       Prenger, and Anima Anandkumar. 2023. LeanDojo:
  on Learning Representations.                                 Theorem proving with retrieval-augmented language
                                                               models. In Advances in Neural Information Process-
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-             ing Systems.
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,
  Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing       Jiarui Yao, Ruida Wang, and Tong Zhang. 2025. FANS:
  Lu, David Acuna, Kaiyu Yang, Hongzhou Lin, Yejin              Formal answer selection for LLM natural language
  Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. 2025.           math reasoning using Lean4. In Proceedings of the
  Goedel-Prover-V2: Scaling formal theorem proving              2025 Conference on Empirical Methods in Natural
  with scaffolded data synthesis and self-correction.           Language Processing, pages 3181–3200, Suzhou,
  arXiv preprint arXiv:2508.03613.                              China. Association for Computational Linguistics.

Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu,            Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li,
  Zaoyu Chen, Yasheng Wang, Lifeng Shang, Qun Liu,             Zhongyuan Peng, Minghao Liu, Yifan Zhang, Zheng
  and Ming Zhang. 2025. Safe: Enhancing mathemati-             Yuan, Huajian Xin, Wenhao Huang, Yandong Wen,
  cal reasoning in large language models via retrospec-        Ge Zhang, and Weiyang Liu. 2025. Formal-
  tive step-aware formal verification. In Proceedings          MATH: Benchmarking formal mathematical rea-
  of the 63rd Annual Meeting of the Association for            soning of large language models. arXiv preprint
  Computational Linguistics (Volume 1: Long Papers),           arXiv:2505.02735.
  pages 12171–12186, Vienna, Austria. Association
                                                             Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  for Computational Linguistics.
                                                               2021. MiniF2F: A cross-system benchmark for for-
                                                               mal Olympiad-level mathematics. arXiv preprint
Nilay Patel, Noah Arias, Davit Babayan, Victoria
                                                               arXiv:2109.00110.
  Cochran, Timothy Libman, Hafsah Mahmood, Liam
  McCarty, Soli Munoz, Laurel Willey, and Jef-
  frey Flanigan. 2026. MathAtlas: A benchmark
  for autoformalization in the wild. arXiv preprint
  arXiv:2605.14061.
Appendices                                               Algorithm 1 Coverage-calibrated formal selection
                                                         (C OV C AL). Lean is trusted only when the proved
A    Proofs                                              answer class dominates enough formally visible
Proof of Theorem 1. Fix a threshold τ ∈ T . Be-          answer-class mass.
cause Aτ and gF are computed without calibra-            Require: problem x, candidates a1:K , weights q1:K , statuses
                                                             s1:K , thresholds τ , fallback gN
tion labels, the accepted calibration examples are        1: Normalize candidates into answer classes C(x) and class
an i.i.d. sample from the conditional deployment             weights Qc (x).
distribution given Aτ (X) = 1, conditional on the         2: Aggregate formal statuses into class indicators Tc (x) and
                                                             Pc (x).
number mτ of accepted examples. Therefore, when           3: Compute Ctyp (x), Cprf (x), unresolved rival mass
mτ > 0, the accepted-error count satisfies                   Runres (x), and margin M (x).
                                                          4: if no class is proved or conflicting proved classes exist
                                                             then
        kτ | mτ ∼ Binomial(mτ , R(τ )).                   5:     return reject formal selection
                                                          6: if Ctyp (x) ≥ τtyp , Cprf (x) ≥ τprf , and M (x) ≥ τM
If mτ = 0, the convention Uα (k, 0) = 1 makes                then
the bound vacuous. For mτ > 0, the one-sided              7:     return the highest-weight proved class gF (x)
                                                          8: else
Clopper–Pearson construction gives                        9:     return ⊥ for selective evaluation, or gN (x) for full-
                                                           answer evaluation
     Pr R(τ ) > Uδ/|T | (kτ , mτ ) ≤ δ/|T |.

Taking a union bound over the finite predeclared         Proof of Proposition 1. Because O(x) contains no
grid yields                                              formal decision or equivalence relation for cu , con-
                                                       struct two possible latent interpretations that agree
   Pr ∃τ ∈ T : R(τ ) > Uδ/|T | (kτ , mτ ) ≤ δ.
                                                         on all observed generated artifacts, weights, sta-
On the complementary event, all grid cells are si-       tuses, proved classes, and error logs. In the first
multaneously valid. Since Eq. 13 selects τ̂ from         interpretation, the selected class cs is the intended
this same grid after calibration, the selected thresh-   correct answer class. In the second, the unresolved
old inherits the bound. If Eq. 13 is feasible, then      inequivalent class cu is the intended correct an-
Uδ/|T | (kτ̂ , mτ̂ ) ≤ ϵ, hence R(τ̂ ) ≤ ϵ on the        swer class, while the formal observation remains
simultaneous-validity event.                             unchanged because cu was not resolved and no
                                                         equivalence to cs was established. The verifier-only
Proof of Theorem 2. The map f depends only on            selector receives identical observations in both in-
the development split, so τ̂ is σ(Ddev )-measurable      terpretations and therefore returns the same class cs .
and independent of the calibration split. Condi-         It is correct in the first interpretation and incorrect
tional on the event τ̂ = τ ◦ and on m = mcal  τ◦ =       in the second. Thus the formal observation alone
   ◦
m > 0, the cal accepted-error count is binomial:         cannot yield a pointwise correctness certificate that
                                                         is valid across all latent interpretations compatible
 k | τ̂ = τ ◦ , m = m◦ ∼ Binomial(m◦ , R(τ ◦ )).         with the unresolved rival.
The one-sided Clopper–Pearson bound therefore
                                                         B    Method and Calibration Details
satisfies, for every fixed τ ◦ and m◦ > 0,
                                                         Instance-level decision rule.
Pr[R(τ ◦ ) > Uδ (k, m◦ ) | τ̂ = τ ◦ , m = m◦ ] ≤ δ.
                                                         dev-then-cal selection and certification. Define
The certificate outputs τbout ̸= ⊥ only when m > 0               n                                   o
and Uδ (k, m) ≤ ϵ. Thus, conditional on any se-           Tdev = τ ∈ T : mdev    > 0, kτdev /mdev  ≤ϵ .
                                                                              τ                 τ
lected τ̂ and cal accept count m > 0, the implica-
tion
                                                         If Tdev = ∅, the procedure returns reject-all. Other-
     τbout ̸= ⊥ =⇒ R(b
                     τout ) ≤ Uδ (k, m) ≤ ϵ              wise,
                                                                       τ̂DC = arg max mdev τ ,
                                                                                       τ ∈Tdev
fails with probability at most δ. The reject-all
branches make the implication true by convention.        with deterministic lexicographic tie-breaking. This
Marginalizing over τ̂ and m gives the stated proba-      dev-stage screen is not a certificate; it is only a
bility bound.                                            threshold-selection rule. The selected threshold is
then certified on the independent calibration split      1. Main dataset: all-levels MATH-500, 378 kept
and returned only if                                        after filtering (500 raw minus 122 excluded for
                                                          non-normalizable references, proof-only items,
    mτ̂cal
        DC
            > 0   and   U δ   k cal
                               τ̂DC , mcal
                                       τ̂DC ≤ ϵ.
                                                            and diagram-dependent geometry).
                                                         2. Hard subset: MATH-500 levels 4–5 only, 199
Otherwise the procedure returns reject-all. The             kept after the same filters.
requirement mτ̂cal
                 DC
                     > 0 is a practical convention: a
zero-coverage rule has vacuous selective risk, but it    3. Candidate generator: Qwen2.5-Math-7B-
is reported as reject-all because it accepts no formal      Instruct (bfloat16, vLLM 0.10.2), K = 32 sam-
predictions.                                                ples, temperature 0.7, top-p = 0.95, maximum
                                                            2048 new tokens, final answer in
Edge cases handled by Theorem 2. (i) Empty                  boxed{...}.
dev split: τ̂ = ⊥, reject-all (dev-then-cal is not
                                                         4. Class aggregation: normalize final answers and
applicable when the dev fraction is zero). (ii) No
                                                            compute Qc from self-consistency frequency.
dev-feasible cell: τ̂ = ⊥, reject-all. (iii) Empty
cal accept set: m = 0, reject-all (the Uδ (·, 0) = 1     5. Formalization: Qwen2.5-Coder-7B-Instruct
convention makes the formula consistent but the             (bfloat16) autoformalization with four artifacts
certificate explicitly refuses). (iv) All cal accepts       per top class and one error-feedback repair pass.
are errors: k = m, Uδ (m, m) = 1, certificate
                                                         6. Formalized classes: top four classes per prob-
refuses. (v) Multiple ϵ targets on the same data: se-
                                                            lem.
lect τ̂ once on dev and report the cal-side Uδ (k, m)
as a single number, then check against each ϵ sepa-      7. Lean proving: Lean 4.21.0 with Mathlib at
rately. Re-selecting per ϵ would re-introduce mul-          commit 308445d7; tactic portfolio norm_num,
tiplicity and break the guarantee. (vi) Dev/cal/test        ring_nf, omega, linarith, nlinarith, simp,
distribution mismatch: the theorem fails. The i.i.d.        aesop, decide, and short combinations; 20 sec-
assumption in the statement is necessary. (vii) τ̂          onds per tactic script.
depends on cal: the theorem fails. Strict σ(Ddev )-
                                                         8. Calibration:             20/40/40      develop-
measurability of τ̂ is the load-bearing assumption.
                                                            ment/calibration/test split with seed 0;
Practical choices. The method is deterministic              target selective risk ϵ = 0.15 on the all-levels
after candidate generation and formalization logs           run and ϵ = 0.10 on the hard subset; confidence
are fixed. In experiments, we use self-consistency          1 − δ = 0.95; Clopper–Pearson bounds with
frequency as the primary weight: if K sampled               Bonferroni correction over T (Appendix D;
solutions collapse to answer classes c, then Qc is          |T | = 125).
the fraction of samples in class c. Reranker-derived     9. Baselines reported:            self-consistency,
weights are reported only as an ablation. A class is        confidence-only abstention, raw Lean+fallback,
marked proved if any of its formal artifacts is kernel      proof-existence abstention, typed-coverage only,
checked; it is marked typed if any artifact elabo-          proved-coverage only, margin-only, C OV C AL,
rates or reaches proof search. If one artifact proves       and C OV C AL+fallback.
and another artifact for the same class fails, the
class remains proved but the failure is retained for     D   Threshold Grid Used in Experiments
diagnostics. If two proved classes are inequivalent
                                                         The grid used in all reported runs is
under answer normalization, the formal selector
rejects rather than choosing between them. The                    Ttyp = {0, 0.25, 0.5, 0.75, 0.9},
threshold grid, target risk ϵ, confidence level 1 − δ,            Tprf = {0, 0.1, 0.25, 0.5, 0.75},
normalization rules, Lean version, imports, and
proof budgets are fixed before calibration labels                 TM = {−0.5, 0, 0.1, 0.25, 0.5},
are used.                                                           T = Ttyp × Tprf × TM .              (19)

C    Implementation Details                              The grid must be fixed before inspecting calibra-
                                                         tion labels. Equation 13 then selects the accepted-
The following items document the protocol used in        fraction-maximizing rule whose risk upper bound
the reported runs:                                       is at most the target ϵ.
E   Prompt Templates                                         Per-status definitions. The best Lean status sj
                                                             of an artifact takes one of five values. proved
Candidate generation prompt.
                                                             means a Lean proof of the generated statement
     Solve the following math problem. Give a concise
     derivation and put the final answer in
                                                             was found and kernel checked. typechecked
     boxed{...}. Problem: [problem text]                     means the statement elaborated but no proof was
                                                             found. timeout means proof search began from
Lean autoformalization prompt.
                                                             a well-formed statement but exceeded the budget.
     You are formalizing a math contest answer in
     Lean 4 with Mathlib. Given the problem and pro-
                                                             illtyped and unformalized denote earlier fail-
     posed final answer, write a Lean theorem whose          ures. If a pipeline can also prove negations or in-
     proof would certify that the proposed answer is         equivalence, those outcomes can be added as op-
     correct for the problem. Requirements: (i) state
     the problem’s actual mathematical claim with the        tional decisive statuses; they are not required by
     proposed answer substituted in — do not write           our method.
     a trivial identity such as answer = answer; the
     theorem must be false if the answer is wrong; (ii)      Existing verified Lean proofs. Existing proof
     use Q or R (never N) for any division, fraction,
     or non-integer arithmetic so that division is exact     corpora can be used for supplementary analysis
     rather than floor division, annotating numeric liter-   of proof-search or proof-edit coverage, but they
     als with their type when needed, e.g. (125 : Q)         do not replace the main answer-selection experi-
     / 9; (iii) prefer simple statements and standard
     Mathlib notation. Return only Lean code. Prob-          ment. C OV C AL requires multiple candidate final-
     lem: [problem text] Proposed answer: [answer            answer classes with weights and correctness labels.
     class]
                                                             A corpus of already verified Lean proofs usually
Repair prompt.                                               supplies proof success but not alternative wrong
     The Lean code below failed with the following           answer classes, unresolved rival mass, or natural-
     error. Repair the theorem statement or proof while      language answer-selection labels.
     preserving the intended meaning of the problem
     and answer. Return only Lean code. Code: [code]
     Error: [Lean error]                                     G    Additional Experimental Details

F   What Is Generated and Analyzed                           Filtering and splits. We include problems whose
                                                             final answer can be extracted as a number, expres-
C OV C AL does not require generating a complete             sion, set, interval, finite tuple, or multiple-choice la-
formal proof for every problem. It requires a struc-         bel mapped to a mathematical answer. We exclude
tured log of candidate answers and Lean verifica-            diagram-dependent geometry, proof-only items,
tion attempts. The minimal unit is an answer class,          and examples whose official answer cannot be nor-
not a raw model sample. For each problem, the                malized. MATH-500 contributes 378 kept exam-
generated record contains:                                   ples after 122 exclusions; the hard levels-4/5 subset
1. Problem fields: problem id, dataset, topic la-            is the 199-example slice of these at levels 4 and
   bel, problem text, reference answer, normalized           5. Unless otherwise stated, examples are split af-
   reference class, and inclusion/exclusion status.          ter generation and formalization into development,
                                                             calibration, and test partitions. The seed-0 split is
2. Candidate fields: the K raw sampled solu-
                                                             preregistered; the bootstrap summaries resample
   tions, extracted final answers, normalized an-
                                                             the frozen observations over K = 20 dev/cal/test
   swer classes, and self-consistency weights Qc .
                                                             partitions.
3. Formalization fields: for each top answer class,
   the generated Lean code, repair-round index,              Generation and normalization. Qwen2.5-Math-
   imports, and theorem statement.                           7B-Instruct generates 32 solutions per problem
                                                             at temperature 0.7, top-p = 0.95, and maxi-
4. Lean fields: artifact-level status, class-level sta-      mum 2048 new tokens. The normalizer strips
   tus, tactic script or proof attempt, runtime, time-       admissible units and formatting, canonicalizes
   out flag, error message, Lean version, Mathlib            fractions/decimals/signs/whitespace, parses simple
   commit, and hardware.                                     symbolic expressions, tests numeric equivalence
5. Selection fields: self-consistency class, highest-        for rationals, decimals, radicals, and finite tuples,
   weight proved class, conflict flag, Ctyp , Cprf ,         and logs ambiguous cases. Class weights are self-
   Runres , M , C OV C AL accept/reject decision,            consistency frequencies over normalized answer
   fallback decision when used, and correctness.             classes.
Formalization and Lean proving. For each of               Selector                             Overall Accepted Acc. frac. Test UB
the top four answer classes, Qwen2.5-Coder-7B-            Self-consistency                      0.910   0.910      1.000      0.138
Instruct produces four Lean artifacts, followed           Confidence-only                       0.866   0.969      0.894      0.068
                                                          Raw Lean + fallback                   0.891   0.891      1.000      0.159
by one error-feedback repair pass when elabora-           Proof-existence                       0.193   0.877      0.220      0.258
tion fails. Lean proof search uses Lean 4.21.0            Typed-coverage only                   0.194   0.867      0.224      0.268
                                                          Proved-coverage only                  0.194   0.874      0.222      0.258
with Mathlib commit 308445d7; the tactic port-            Margin only                           0.194   0.932      0.209      0.192
folio is norm_num, ring_nf, omega, linarith,              C OV C AL                             0.194   0.932      0.209      0.192
                                                          C OV C AL+fallback                    0.905   0.905      1.000      0.144
nlinarith, simp, aesop, decide, and short com-
binations, with a 20-second per-script budget.            Table 4: All nine selectors on the main run, dev-then-
Main-run class-level statuses are 140 proved, 271         cal regime (K = 20 bootstrap, ncal = 151, ϵ =
typechecked, 251 illtyped, 0 timeout, and 741 un-         0.15; seed-means). Overall counts abstentions as er-
formalized over 1403 answer-class observations,           rors; Acc. frac. is the accepted fraction; Test UB is
indicating that autoformalization-tier coverage, not      the held-out diagnostic upper bound. The calibrated
prover timeout, dominates the negative trace.             rows (typed/proved/margin/C OV C AL) average over the
                                                          12/20 feasible seeds; the others are regime-independent.
Baselines. The reported baselines are self-               Margin-only and C OV C AL coincide, indicating the mar-
consistency, confidence-only abstention, raw Lean         gin threshold carries most of the selective signal here.
plus fallback, proof-existence abstention, typed-
coverage-only, proved-coverage-only, margin-only,                                   0.30                   Self-consistency
                                                                                                           Confidence-only
C OV C AL, and C OV C AL plus fallback. The fall-                                   0.25                   Proof-existence
back is self-consistency. Fallback predictions are              Selective-risk UB                          CovCal (dev-cal)
useful for overall accuracy but are not covered by
                                                                                    0.20
                                                                                             = 0.15
the selective-risk certificate unless separately cali-                              0.15
brated.                                                                             0.10
Compute and hardware. All experiments ran                                           0.05
on a single compute node with one NVIDIA H100
                                                                                    0.00
80GB HBM3 GPU and 8 allocated CPU cores;                                                   0.0 0.2 0.4 0.6 0.8 1.0
generation and autoformalization use vLLM on                                                     Accepted fraction
the GPU, while Lean proof search runs on the
                                                          Figure 2: Accepted fraction versus held-out selective-
CPU within the same job. The autoformalizer abla-
                                                          risk upper bound on the main run (dev-then-cal; K = 20
tions took approximately 5.5 (Goedel-Prover-V2-           bootstrap mean). The dashed line is ϵ = 0.15. The
8B) and 4.9 (Goedel-Prover-V2-32B) GPU-hours,             formal selectors accept ≈ 21% of items just above ϵ,
and the main MATH-500 and AMC/AIME runs                   while confidence-only abstention reaches 0.89 coverage
a few GPU-hours each (generation is replayed              at lower diagnostic risk; +fallback variants (full cover-
from cache across the ablations), for roughly 15–20       age) and the Bonferroni reject-all case are omitted.
GPU-hours in total across all reported runs.

H     Additional Results                                  formal margin carries most of the selective sig-
                                                          nal at this protocol. Figure 2 plots the accepted-
This appendix presents supporting evidence behind
                                                          fraction/risk tradeoff for the main selectors.
the results summary in Sec. 8. Tables 5–10 pro-
vide the corresponding per-level, sensitivity, failure-   H.2     Per-Level and Domain Breakdowns
status, and robustness details.
                                                          Table 2 bins the cliff coarsely; Table 5 aggregates
H.1    Full Answer-Selection Comparison                   the same main-run observations by MATH-500 dif-
Table 4 reports all nine selectors on the main run        ficulty level. Both coverage and reliability decline
under the dev-then-cal regime (under Bonferroni           monotonically with difficulty: mean proved cov-
the calibrated rows are reject-all; Table 3). The         erage falls from 0.44 at level 1 to 0.16 at level 5,
single-diagnostic selectors clarify which diagnostic      and proof-existence accuracy on the proved subset
carries the signal: margin-only matches the joint         falls from 1.00 to 0.74. The coverage drop is the
C OV C AL rule exactly (0.93 accepted accuracy at         steeper of the two (a 2.7× reduction versus 1.4×
0.21 accepted fraction), whereas typed- and proved-       for accuracy), so in this protocol increasing dif-
coverage alone are slightly less precise. Thus, the       ficulty primarily reduces visible formal coverage,
   Level    n    C̄typ    C̄prf PE acc. Cert. feas.                 Lean class-level status Count Share
      1     35 0.797 0.441         1.00          –                  unformalized               741    0.528
      2     64 0.733 0.328         0.91          –                  typechecked                271    0.193
      3     80 0.627 0.226         0.90          –                  illtyped                   251    0.179
      4     97 0.616 0.191         0.78          –                  proved                     140    0.100
      5    102 0.520 0.162         0.74          –                  timeout                     0     0.000

Table 5: Per-level breakdown on the main MATH-500           Table 7: Class-level Lean status distribution on the main
run. C̄typ and C̄prf are mean typed/proved coverage         run (1403 answer-class observations across 378 prob-
within each level. PE acc. is proof-existence accepted      lems; best status per class). The taxonomy is automatic
accuracy on examples where at least one answer class        and based on pipeline statuses. Most answer classes
is proved. Cert. feas. asks whether proof-existence         are never formalized or fail elaboration; only 10% are
alone certifies ϵ = 0.15 within that level using the same   proved, and no well-formed statement times out.
Bonferroni confidence budget; all individual levels are
too small for this single-bin stand-in to certify, which
is expected and should not be read as evidence of zero      manual semantic audit.
useful signal.
                                                            Why the 32B autoformalizer does not help
Domain              n     Typed Proved Acc. Top failure     (status-level view). Table 8 compares class-level
Algebra             241   0.663   0.234   0.89   illtyped   Lean statuses for the two Goedel-Prover-V2 aut-
Number theory       60    0.684   0.314   0.82   illtyped
Combinatorics        30   0.621   0.281   0.70   illtyped
                                                            oformalizers with generation held fixed, and ex-
Geometry            24    0.490   0.194   0.86   illtyped   plains the headline of Sec. 8.3, that scaling from
Calculus / analysis 23    0.281   0.053   1.00   illtyped   8B to 32B lowers proved coverage (79% → 64%).
                                                            The gap is not a proof-search timeout: timeout
Table 6: Domain-level formal coverage on the main run.
                                                            is 0 for both models. Both models also elabo-
Typed and Proved are mean Ctyp and Cprf per domain;
Acc. is the accuracy of the highest-weight proved class     rate statements at essentially the same rate. The
among problems where a proof exists; Top failure is         unformalized count is nearly identical (656 vs.
the modal class-level Lean status among unsuccessful        651 of 1380 classes). The entire difference is
artifacts. Coverage is markedly lower for geometry and      a proved→typechecked shift: 493 classes are
calculus/analysis (typed 0.49 and 0.28 versus 0.66 for      proved by the 8B but only 347 by the 32B, with
algebra); the Acc. column is over the small proved          the lost mass reappearing as typechecked (191 →
subset of each domain (e.g. only 2 proved problems in       323). The larger model writes statements that type-
calculus/analysis) and is noisy.
                                                            check just as often but that the fixed Mathlib tactic
                                                            portfolio closes less often, consistent with prover
while in-bin reliability degrades more slowly.              specialization (shared by both Goedel-Prover-V2
   Table 6 gives a domain-level view. Geome-                models), rather than raw parameter count, being
try and calculus/analysis have substantially lower          what lifts proved coverage past the certificate-
typed and proved coverage than algebra, number              feasibility threshold.
theory, and combinatorics (proved coverage 0.19                Table 9 reports the Bonferroni calibration certifi-
and 0.05 versus 0.23–0.31), so far fewer of their           cates on the seed-0 main split. This table is inten-
problems reach any formal verdict. This supports            tionally separated from held-out answer-selection
this work’s central interpretation that the reliability     diagnostics: it is the calibration-side certificate
of Lean-as-judge depends on how much answer-                used by the selection rule. On the sparse real signal
class mass becomes representable and decidable by           the main split returns reject-all through ϵ = 0.20
the formal pipeline.                                        and certifies only at ϵ ≳ 0.26; the smallest achiev-
                                                            able Bonferroni upper bound at the most permissive
H.3    Status Counts and ϵ-Sensitivity                      cell is 0.257, well above the preregistered target
Table 7 gives the automated Lean-status break-              ϵ = 0.15.
down. The dominant statuses are unformalized                   A coarse-grid sensitivity check gives the same
and illtyped; timeouts on well-formed statements            qualitative conclusion: a 3 × 3 × 3 grid lowers the
are absent in the main run. These status counts             most-permissive-cell upper bound only modestly
support the claim that the main bottleneck occurs           and does not bring it below ϵ = 0.15. Thus the
before proof search, but they remain coarser than a         reject-all verdict is driven by the sparsity of the
 Lean class-level status       Goedel-V2-8B Goedel-V2-32B    coverage-based rows reject because the calibration-
 proved                            493           347         side Bonferroni upper bound for proof-existence
 typechecked                       191           323
 illtyped                           40           59
                                                             alone is already above the target. This is the
 unformalized                      656           651         intended conservative behavior of the certificate
 timeout                             0            0          when formal coverage is too low for the specified
 Proved coverage (problems)       79.1%         63.5%        risk level.
Table 8: Class-level Lean status counts for the two          I   Worked Examples
autoformalizer ablations (1380 answer-class observa-
tions over the same 378 problems; best status per            The three cases of Section 8.2 are presented next.
class, generation held fixed). Scaling 8B→32B leaves
unformalized and timeout essentially unchanged but           (A) Accept — faithful proof, full coverage.
shifts mass from proved to typechecked: the larger           Problem: “What is the 2003rd term of the sequence
model’s statements elaborate as often but are closed by      of odd numbers 1, 3, 5, 7, . . . ?” Reference answer:
the fixed tactic portfolio less often, so proved coverage    4005. All K=32 samples collapse to the single
falls from 79% to 64%.                                       answer class 4005 (w=1.0), which is proved. The
                                                             kernel-checked statement is
         ϵ       Selected τ̂ (mτ̂ , kτ̂ ) Cal. UB
                                                                 2 · 2003 − 1 = 4005        (by norm_num),
         0.05     reject-all      n/a       n/a
         0.10     reject-all      n/a       n/a
                                                             a faithful closed form of “the nth odd number is
         0.15     reject-all      n/a       n/a
         0.20     reject-all      n/a       n/a              2n − 1.” Diagnostics: Ctyp =Cprf =1, margin 1.
         0.30    (0, 0.1, 0)    (35, 1)    0.257             C OV C AL accepts 4005 (correct). Lesson: a proof
                                                             is trusted when the proved class dominates the for-
Table 9: Bonferroni calibration-split certificates for the   mally visible mass with a clear margin.
seed-0 main run (ncal = 151, δ = 0.05, |T | = 125).
On the sparse real signal no grid cell certifies through     (B) Abstain — no formal signal, fallback correct.
ϵ = 0.20, so C OV C AL returns reject-all at the prereg-     Problem: “Simplify cos 2π        4π     8π     16π
                                                                                       15 cos 15 cos 15 cos 15 .”
                                                                                   1
istered target ϵ = 0.15; the most permissive cell first      Reference answer: 16    . The dominant class 1/16
certifies near ϵ = 0.26 with calibration upper bound         (w=0.84) and the minor classes 1/32 and 1/8 all
0.257. This is the conservative regime correctly refus-      fail Lean elaboration. The trigonometric product
ing when the proved signal is too sparse to pay the
                                                             identity does not autoformalize. So, Ctyp =Cprf =0
|T | = 125 union bound.
                                                             and no class is proved. C OV C AL abstains; the self-
                                                             consistency fallback returns 1/16 (correct). Lesson:
proved signal and the resulting accepted-set errors,         a missing proof is unresolved, not negative; absten-
not by the granularity of the threshold grid.                tion plus fallback preserves the correct answer.

H.4     Hard Subset and AMC/AIME                             (C) Abstain — margin distrusts a vacuous proof
                                                             of a wrong rival. Problem: “An equilateral trian-
Table 10 records two robustness settings. The hard
                                                             gle is inscribed in the parabola x2 = 8y, such that
MATH-500 levels 4–5 subset (n = 199, the hardest
                                                             one of the vertices of the triangle coincides with
slice of the main run) has an even sparser proved
                                                             the vertex of the parabola. Find the side length√of
signal than the full set and returns reject-all un-
der both regimes at the stricter target ϵ = 0.10.                                  √ Reference answer: 16 3.
                                                             this equilateral triangle.”
                                                             The correct class 16 3 (w=0.88) fails to autofor-
An AMC/AIME-style out-of-distribution set (n =
                                                             malize (illtyped); the only proved class is a low-
164), run on the same pipeline, confirms that the
                                                             weight rival 16 (w=0.03), whose “proof” is the
sparsity persists under a harder problem distribu-
                                                             vacuous identity
tion: self-consistency accuracy is far lower (0.40
versus 0.91 on MATH-500), the proved signal is                      (16 : Q) = 16       (by norm_num),
sparse (proof-existence accepts only ≈ 11% of test
items), and both certificate regimes return reject-all       which holds for any value and therefore pro-
at ϵ = 0.10.                                                 vides no evidence about the answer. Diagnostics:
   For the hard subset, confidence-only abstention           Cprf =0.03, margin −0.84. Because the proved
can produce a low held-out error bound, but that is          class carries far less weight than the unresolved
not a Lean-backed formal certificate. The formal             dominant class, the strongly negative margin makes
               Setting                     n    ncal    ϵ     SC    PE acc.       PE frac. / verdict
               Main MATH-500      378 151 0.15 0.910                  0.877    0.220 / dev-cal 12/20
               Hard MATH-500 L4–5 199 80 0.10 0.859                   0.761   0.231 / reject-all (both)
               AMC/AIME           164 66 0.10 0.400                   0.429   0.108 / reject-all (both)

Table 10: Robustness settings versus the full main run. SC is self-consistency test accuracy; PE acc. and PE frac.
are proof-existence accepted accuracy and accepted fraction; the last field gives the certificate verdict (ϵ as listed).
The hard subset is the level-4/5 slice of the main run (n = 199); its proved signal is even sparser, so both regimes
reject-all at the stricter ϵ = 0.10. The AMC/AIME row is an out-of-distribution check on the same pipeline; its
sparser signal and lower self-consistency accuracy likewise yield reject-all under both regimes at ϵ = 0.10.

                                             √
C OV C AL abstain; the fallback recovers 16 3 (cor-
rect). Lesson: proof existence on a low-weight or
trivially formalized rival is correctly distrusted by
the margin.
