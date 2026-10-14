                                               Context-Aware Distillation and Ablation for
                                                              Text2DSL

                                                      Alexander V. Kozachok1 ⋆ , Alexander M. Nazimov2 , and
                                                                     Shamil G. Magomedov1
                                               1
                                                 MIREA – Russian Technological University, Moscow, Russian Federation
                                                              {kozachok_a, magomedov_sh}@mirea.ru
arXiv:2606.22578v1 [cs.CL] 21 Jun 2026




                                               2
                                                 Academy of the Federal Guard Service of the Russian Federation, Oryol,
                                                                         Russian Federation
                                                                         s-nazim@list.ru




                                                   Abstract. We extend our prior work on Text2DSL — automatic gen-
                                                   eration of domain-specific language (DSL) code from natural language
                                                   descriptions — along two complementary axes. First, we replace prompt-
                                                   only synthetic generation with context-aware distillation, in which a
                                                   teacher large language model (DeepSeek-V4-Flash) operates under an
                                                   explicitly defined structured context comprising a BNF grammar, an
                                                   API specification, and a closed identifier vocabulary; the resulting cor-
                                                   pus is verified by a two-tier pipeline combining AST validation through
                                                   esprima and runtime acceptance through the production polkitd dae-
                                                   mon and the pkcheck client. This scales the verified PolkitBench corpus
                                                   from 4,204 to 10,073 natural-language–to–Polkit-rule pairs at 100.0%
                                                   AST validity and 99.7% runtime pass rate. Second, we conduct the per-
                                                   component factorial ablation of structured context that was identified as
                                                   future work in the precursor study: eight conditions C0 –C7 are evaluated
                                                   on GigaChat-10B-A1.8B with the new corpus. Three findings emerge.
                                                   (i) The new harder corpus collapses the baseline mode (Syntax Valid
                                                   97.6 % → 58.5 %, Combined Score 0.482 → 0.252), whereas the context-
                                                   enhanced mode degrades only marginally (Syntax 98.6 % → 97.4 %, Com-
                                                   bined 0.801 → 0.750), confirming that structured context is not a cos-
                                                   metic improvement but a load-bearing mechanism. (ii) The best absolute
                                                   condition is the full context C7 across all metrics, while the strongest par-
                                                   tial conditions (C5 = BNF + Vocabulary, C6 = API + Vocabulary) both
                                                   contain the vocabulary. (iii) A Shapley-style decomposition assigns the
                                                   largest semantic-quality effect to the vocabulary (Combined +0.198), the
                                                   largest structural-validity effects to API (+24.7 pp) and BNF (+22.3 pp),
                                                   supporting the interpretation that the three components are complemen-
                                                   tary rather than substitutable.

                                                   Keywords: Text2DSL, large language models, code generation, knowl-
                                                   edge distillation, structured context, ablation, formal verification, Polkit

                                         ⋆
                                             Corresponding author
2       Kozachok, Nazimov, Magomedov

1   Introduction
Domain-specific languages (DSLs) describe security and configuration policy
across a broad swath of modern systems: SELinux type-enforcement rules [3],
AppArmor profiles, OPA Rego policies [5], Terraform HCL infrastructure-as-
code [6] and, in the Linux desktop and server stack, Polkit authorization rules [2].
These languages share a common shape: a compact grammar, a closed vocab-
ulary of permitted identifiers, and deterministic semantics. They also share a
common operational risk: empirical studies of infrastructure-as-code [7] report
13–31 security smells per thousand lines, with policy languages among the most
error-prone artefacts in DevOps pipelines.
    In recent work [1] we formalised the task of generating such artefacts from
natural language descriptions as a distinct problem class, Text2DSL, charac-
terised by (i) a fixed grammar G, (ii) a closed identifier vocabulary V , and (iii)
deterministic API semantics. On a verified benchmark of 4,204 natural-language–
to–Polkit-rule pairs — PolkitBench — we showed that supplying structured con-
text (BNF grammar, API specification, vocabulary V ) in the prompt of a small
language model produces large and consistent gains across two MoE models
(GigaChat-10B-A1.8B and Nemotron-3-Nano-30B-A3B), with structural valid-
ity rising by +9.7 to +35.5 pp and CodeBLEU by +60 to +95% relative.
    That study left three concrete open questions, which the present paper ad-
dresses.
Q1. The PolkitBench corpus was produced by direct prompt-based generation
on a single teacher (Grok-4.1-fast) with domain hints embedded into the prompt.
It did not formalise the contextual conditions of generation: each record carried
no provenance about the generating model, the API base, the context file or
the context sources it drew on. Can the dataset construction itself be lifted into
the same context-aware mode, with each record explicitly bound to a versioned
context package? And how does this mode scale: does a larger, more diverse
verified corpus remain useful, or does it merely reproduce the smaller one?
Q2. The previous validation pipeline was deterministic but static: it accepted a
rule if it parsed, conformed to the structural template, and used only identifiers
from the documented vocabulary V . It did not check that the rule is actually
accepted by the production Polkit daemon at runtime. Such an additional check
is non-trivial: it requires loading the rule into polkitd, exercising it via pkcheck,
and reasoning about the difference between syntactic acceptance and observable
runtime behaviour.
Q3. The previous work of the authors [1] compared full context vs. no context.
It deferred the per-component breakdown — BNF only, API only, vocabulary
only, and all pairwise combinations — to future work. Without that breakdown
the prescription “inject structured context” is not actionable for practitioners
who need to know which components are load-bearing and which are decorative,
and it is not falsifiable in the scientific sense: any one of BNF, API or V could
in principle account for most of the gain.

Contributions. This paper makes the following four contributions.
                     Context-Aware Distillation and Ablation for Text2DSL         3

 1. Context-aware distillation method. We formulate the construction
    of a verified Text2DSL corpus as a distillation procedure in which
    a teacher LLM operates under an explicitly defined structured con-
    text model CM = ⟨G, A, V ⟩ and each generated record carries prove-
    nance fields (generator_model, generator_api_base, context_file,
    context_sources). Applied with DeepSeek-V4-Flash as teacher, the proce-
    dure yields a verified corpus of 10,073 pairs — the second-generation Polkit-
    Bench, hereafter PolkitBench-v2.
 2. Two-tier validation pipeline. We complement deterministic AST vali-
    dation with a containerised runtime stage that loads every candidate rule
    into the actual polkitd daemon and queries it through pkcheck. On
    PolkitBench-v2 the AST pass rate is 10073/10073 (100.0%) and the runtime
    acceptance rate is 10043/10073 (99.7%), with the 30 failures attributable to
    edge cases in the action.id dictionary.
 3. Per-component factorial ablation. We evaluate eight conditions
    C0 . . . C7 corresponding to the 23 subsets of {BNF, API, Vocabulary} on
    the same evaluated model (GigaChat-10B-A1.8B) and the same corpus
    (PolkitBench-v2). C0 and C7 are reused from the dedicated baseline and
    full-context runs; C1 . . . C6 are obtained from a single factorial run. We re-
    port main effects, pairwise interactions and Shapley-style attributions for
    the five primary metrics.
 4. Empirical evidence for context as a load-bearing mechanism. On
    the harder PolkitBench-v2 the baseline mode collapses on every metric
    (Combined Score 0.482 → 0.252, −901 additional timeouts) while the full-
    context mode degrades only marginally (Combined 0.801 → 0.750). The
    per-component ablation shows that the full context is the unique best con-
    dition; the two strongest partial configurations both contain the vocabulary;
    the vocabulary is the largest semantic-quality driver while BNF and API are
    the largest syntactic and structural stabilisers.

    The remainder of the paper is organised as follows. Section 2 recalls the for-
mal Text2DSL setting and discusses related work in synthetic data distillation,
runtime policy validation and constrained code generation. Section 3 formalises
the context-aware distillation method and the two-tier validation pipeline. Sec-
tion 4 specifies the factorial ablation design. Section 5 describes the experimental
setup. Section 6 reports the corpus validation, the baseline/context comparison
across both PolkitBench generations and the per-component ablation. Section 7
discusses interpretation, limitations and threats to validity. Section 8 concludes.


2     Background and Related Work
2.1   The Text2DSL Task
Following [1], let Q denote the set of natural language queries, G the formal
grammar of the target DSL, and V the closed vocabulary of permitted identifiers
(API names, constants, enumerations). The Text2DSL task is the construction of
4       Kozachok, Nazimov, Magomedov

a mapping f : Q → PG , where PG is the set of programs admitted by grammar
G, such that for an arbitrary query q ∈ Q the generated program p = f (q)
satisfies:

 1. Syntactic correctness: parse(p, G) = OK;
 2. Semantic correctness: ids(p) ⊆ V .

This task differs from general NL → Code in three properties of the target
language: a fixed compact grammar (Polkit has ≈ 10 productions; the Python
grammar has > 300), a closed identifier vocabulary (|V | ≈ 65 for Polkit), and
deterministic API semantics (each polkit.Result.* has exactly one interpre-
tation defined by the specification). The general programme of domain-specific
language design, in which a compact target grammar is paired with a fixed se-
mantic interpretation, has been treated systematically by Mernik et al. [9].


2.2   Code Generation with Pre-trained Language Models

Early pre-trained encoders for code such as CodeBERT [16] and GraphCode-
BERT [17] established that the bidirectional Transformer pre-training paradigm
transfers well to source-code understanding, and CodeT5 [18] extended it with
identifier-aware encoder–decoder objectives. The shift to decoder-only generative
models is represented by CodeGen [20] and StarCoder [19], which target open-
ended program synthesis from natural language. None of these models were
designed for a small, closed-vocabulary DSL: the underlying training corpora
are dominated by Python, Java and JavaScript, and the generation surface they
expose is the open vocabulary of general-purpose programming.


2.3   LLM-Based Synthetic Data and Distillation

Knowledge distillation was originally introduced for model compression [22] and
developed into a broad family of teacher–student transfer methods [23]; a clas-
sical NLP instantiation is TinyBERT [24]. In the LLM era this idea has been
generalised to dataset distillation: a teacher model produces a synthetic corpus
that captures task-relevant behaviour for downstream training or benchmarking.
Self-Instruct [25] used a teacher LLM to bootstrap an instruction-tuning corpus
from a small seed; Evol-Instruct [26] extended this idea with controlled task
transformations; in the code domain, WizardCoder [27] synthesised instruction–
code pairs by similar means.
    These methods produce broad but largely unverified corpora: synthetic gen-
eration is followed at best by lightweight heuristics or self-consistency checks.
For policy and configuration languages, where any single uncaught error is op-
erationally meaningful, this is insufficient. Jigsaw [21] applies post-hoc test exe-
cution to filter Pandas API code, but neither it nor comparable code-generation
pipelines provide deterministic compile-time and runtime validation of every
synthesised record against a reference interpreter of the target language.
                      Context-Aware Distillation and Ablation for Text2DSL           5

2.4   Runtime Validation of Generated Policies

For policy DSLs, syntactic acceptance does not imply runtime acceptance. Load-
ing a rule into the production daemon and exercising it through the actual deci-
sion client surfaces a different error class: a syntactically valid rule may still fail
to load due to silent dependencies on the runtime environment, and a loadable
rule may yield an unexpected decision for the query it was designed for. Recent
work on SELinux module integration [4] and on automated security-smell de-
tection in infrastructure-as-code [8,7] argues for this stronger validation mode.
We adopt the same position for Polkit and report a containerised pipeline that
performs both polkitd load and pkcheck verification per record.


2.5   Context Injection, Retrieval and Component-Wise Analysis

The closest analogue to context injection in Text2DSL is schema linking in
Text-to-SQL, popularised by the Spider benchmark [10]: DIN-SQL [11] demon-
strated that injecting the database schema into the prompt substantially im-
proves accuracy; RESDSQL [12] separates schema linking from SQL genera-
tion. PICARD [13] and Synchromesh [14] take a complementary approach by
constraining the decoder at the token level, and grammar-constrained decod-
ing [15] generalises this to arbitrary CFGs. A neighbouring line of work supplies
external knowledge to a generative model via retrieval rather than verbatim
context injection: retrieval-augmented generation [28] formalises the retriever–
reader pipeline, and prompt-time techniques such as in-context learning [32] and
chain-of-thought [29] structure the generation step itself. The previous work of
the authors [1] adopted the context-injection branch and reported full-context
vs. no-context numbers for two models, but did not isolate the contribution of
the three context components (BNF, API, vocabulary).
    To our knowledge, no published study reports a 23 factorial ablation of struc-
tured context for a policy-language Text2DSL task. The ablation reported in
Section 6.3 fills this gap.


3     Context-Aware Distillation and Two-Tier Validation

3.1   Structured Context Model

A context model for a target DSL is a triple

                                  CM = ⟨G, A, V ⟩                                  (1)

where G is a BNF grammar of the DSL, A is an API specification (objec-
t/method/property signatures together with admissible return values), and V
is the closed vocabulary of permitted string-valued identifiers (action.id val-
ues, group names, well-known principals). The grammar G defines the syntactic
envelope, the specification A defines the legal call shape, and the vocabulary V
defines the semantic content the rule may reference.
6      Kozachok, Nazimov, Magomedov

    For Polkit, this instantiation is concrete. G is a 10-production BNF describing
the top-level call polkit.addRule(function(action, subject) { ...}). A
enumerates the admissible accesses action.id, subject.user, subject.local,
subject.active, subject.isInGroup(...) and the polkit.Result enumer-
ation. V enumerates approximately 65 action.id strings across ten subsys-
tems: systemd, login1, PackageKit, udisks2, NetworkManager, hostname1,
timedate1, bluez, cupspkhelper and policykit.
    Throughout this paper the context-enhanced mode denotes the use of an
LLM with CM supplied verbatim in the prompt, together with explicit response-
format constraints and a small set of reference patterns. The baseline mode
denotes the same LLM with the same query but without any component of CM.
Both modes share inference parameters; the only varied factor is the presence of
CM.


3.2   Context-Aware Distillation

We define context-aware distillation as the procedure summarised in Algo-
rithm 1. A teacher LLM T generates candidate rules under the context model
CM for a parameterised query stream Q; each candidate is then verified by the
AST validator AST(·) (Section 3.3); each surviving candidate is verified by the
runtime validator RT(·) (Section 3.4). Records that pass both stages are emitted
with provenance metadata that ties them to a specific context version.


Algorithm 1. Context-aware distillation for Text2DSL.
Input: teacher LLM T , context model CM = ⟨G, A, V ⟩, query stream Q.
Output: verified corpus D.
1. D ← ∅
2. for each query q ∈ Q do
   3. prompt ← render(CM, q)
   4. r ← T (prompt)
   5. if AST(r, G, A, V ) = OK and RT(r) = OK then
      6. emit (q, r, meta(T, CM)) into D
   7. end if
8. end for




    The key difference from classical synthetic-data generation pipelines is that
CM is treated as the single source of domain truth: the teacher is instructed
to use only the symbols and constructs declared in CM, and any record that
exits CM is rejected by AST validation. The teacher’s role is therefore not to
“know Polkit” but to compose admissible elements of CM in response to natural-
language queries.
                     Context-Aware Distillation and Ablation for Text2DSL         7

3.3   AST Validation

AST validation is performed by an esprima-based JavaScript parser aug-
mented with three structural checks: (i) the top-level call must be
polkit.addRule(...); (ii) the callback must be a function of two param-
eters (action, subject); (iii) every property access on action, subject
or polkit.Result must reference a name from the documented vocabulary.
Records failing any of these checks are rejected and the rejection mode is logged
for diagnostic purposes.


3.4   Runtime Validation

Runtime validation is performed in a containerised environment in which
a full Polkit installation is started and the candidate rule is dropped into
/etc/polkit-1/rules.d/. The procedure has two stages:

1. Load check. The daemon is signalled to re-read its rules directory. A rule
   fails the load check if the daemon logs a parse error or refuses the file. This
   catches a residual class of errors invisible to static analysis: rules that parse
   as JavaScript but are rejected by the SpiderMonkey engine bundled with the
   production polkitd, or by Polkit’s own rule loader.
2. Decision check. pkcheck is invoked with the action.id for which the
   rule was synthesised. A rule fails the decision check if pkcheck returns an
   outcome inconsistent with the rule’s declared polkit.Result.

   The output of runtime validation is a triple (Load OK, pkcheck PASS,
pkcheck FAIL), reported per-record and aggregated per-corpus.


4     Per-Component Ablation Design

To isolate the contribution of each component of CM we instantiate the 23
factorial design summarised in Table 1. Each condition Ci corresponds to a
subset Si ⊆ {BNF, API, Vocabulary} of context components included in the
prompt; the prompt header, the response-format constraints and the reference
patterns are held constant across conditions.

Run fusion. In practice we obtain C0 from the dedicated baseline run on
PolkitBench-v2, C7 from the dedicated full-context run, and C1 . . . C6 from a
single factorial run. This fusion is methodologically sound because C0 and C7 in
the fused matrix are operationally identical to the corner cells of the factorial
design: same evaluated model (GigaChat-10B-A1.8B), same corpus (the 10,073-
record PolkitBench-v2), same inference parameters, same context file. The fusion
uses pre-computed runs only to avoid re-paying inference cost for two cells that
are already available.
8      Kozachok, Nazimov, Magomedov

       Table 1. Factorial ablation design over the three components of CM.


                        Condition           BNF API Vocabulary
                        C0 (baseline)        —   —       —
                        C1                   ✓   —       —
                        C2                   —   ✓       —
                        C3                   —   —       ✓
                        C4                   ✓   ✓       —
                        C5                   ✓   —       ✓
                        C6                   —   ✓       ✓
                        C7 (full context)    ✓   ✓       ✓




Factor decomposition. For each metric m, the main effect of factor X ∈
{BNF, API, Vocabulary} is

                     (m)       1 X          1 X
                   EX      =       m(CS ) −     m(CS ),                        (2)
                               4            4
                                S:X∈S                S:X ∈S
                                                         /

that is, the average of conditions in which X is present minus the average of
                                                                            (m)
conditions in which X is absent. We additionally report Shapley values ϕX
                     3
computed over the 2 coalition lattice with m as the value function; for facto-
rial designs with three players, the Shapley value is equivalent to the average
marginal contribution across all orderings.


5     Experimental Setup

5.1   Models and Roles

The experiment uses two models in two strictly separated roles.

Teacher: DeepSeek-V4-Flash. The teacher LLM is used exclusively to generate
PolkitBench-v2 under the context model CM (Algorithm 1). It is not evaluated
as a downstream Text2DSL solver in this paper; its role is to produce a verified
corpus.

Evaluated model: GigaChat-10B-A1.8B. The evaluated model is the same MoE
small language model used in the previous work of the authors [1], served locally
via llama.cpp with Q4_K_M quantisation. It is used both for the baseline/con-
text comparison (Section 6.2) and for the per-component ablation (Section 6.3).
    This separation is essential to interpret the experimental results. The teacher
in Algorithm 1 can be a strong cloud model precisely because its output is
independently verified; the evaluated model is the small locally-deployable model
that a practitioner would actually run at inference time.
                      Context-Aware Distillation and Ablation for Text2DSL          9

5.2   Datasets

PolkitBench-v1. The original verified corpus from [1]: 4,204 natural-language–
to–Polkit-rule pairs filtered from 5,000 candidates by three-level AST validation.
It was generated by Grok-4.1-fast in a prompt-based mode with domain hints.
We use it here as a reference point for cross-corpus comparison.

PolkitBench-v2. The new context-aware verified corpus introduced in this pa-
per: 10,073 pairs, produced by the procedure of Section 3.2 with DeepSeek-
V4-Flash as teacher. Each record carries provenance fields (generator_model,
generator_api_base, context_file, context_sources) tying it to a specific
version of CM.
    Table 2 reports the empirical distribution of PolkitBench-v2 across the ten
subsystems covered by V , alongside the corresponding shares of the v1 corpus
reported in [1] for comparison; per-record counts can sum above 100% because
multi-action rules touch multiple subsystems. The v2 corpus differs from v1 along
three quantifiable axes that jointly populate the long tail of the query space and
account for the disproportionate degradation of the baseline mode observed in
Section 6.2: (i) the share of rules combining two or more distinct action.id val-
ues rises to 58.4% (mean 1.62 distinct identifiers per rule, maximum 6); (ii) 95.0%
of rules carry a compound condition with at least one && operator, and 82.0%
reference subject.isInGroup(...) group membership; (iii) the polkit.Result
distribution is dominated by YES (96.3%) with AUTH_SELF (3.7%) and NO (3.3%)
as the remaining outcomes. Compared with v1 the relative weight of PackageKit,
login1 and NetworkManager rises markedly, while timedate1 and udisks2 grow
by about ×2.


Table 2. Subsystem distribution in PolkitBench-v1 (from [1]) and PolkitBench-v2 (this
work). v2 percentages are shares of records that reference the subsystem at least once
and sum above 100% due to multi-action rules.


                 Subsystem            v1 share (%)     v2 share (%)
                 PackageKit                      16             26.4
                 login1 (power)                  14             26.1
                 NetworkManager                  12             25.7
                 systemd                         12             17.2
                 timedate1                        7             16.4
                 udisks2                         10             16.1
                 hostname1                        6             11.7
                 cupspkhelper                     6             11.3
                 bluez / bluetooth                5              5.6
                 policykit / other               12              2.1
10      Kozachok, Nazimov, Magomedov

5.3   Metrics

We report the five primary metrics defined in [1]: Syntax Valid (SynVal), Struc-
ture Valid (StrVal), CodeBLEU — a code-oriented refinement of the classical
BLEU metric [30] for source-code outputs that better aligns with structural
equivalence than surface-level n-gram overlap, in the same spirit as Crystal-
BLEU [31] — string-literal Jaccard, and Combined Score = 0.7 · CodeBLEU +
0.3 · Jaccard. We additionally report the strict integrated indicator we name
Strict Success and the count of inference timeouts.

Strict Success. The evaluation code assigns Strict Success = 1 to a response
only if all of the following hold simultaneously: (i) a rule code block can be ex-
tracted from the response; (ii) the extracted code passes formal AST validation;
(iii) the structure of the rule is recognised as well-formed; (iv) the number of
hallucinated action.id values is exactly zero. Strict Success is therefore an in-
tegrated end-to-end indicator rather than a soft quality metric: a response that
is syntactically and structurally close to the reference but contains a single hal-
lucinated identifier scores Strict Success = 0. We report it for completeness and
use Syntax/Structure/CodeBLEU/Jaccard/Combined as the principal metrics
for cross-mode comparisons.


5.4   Inference Configuration

GigaChat-10B-A1.8B is served locally via llama.cpp with temperature 0.0
and a 120-second per-query timeout. The teacher DeepSeek-V4-Flash is ac-
cessed through its provider API with deterministic decoding for reproducibil-
ity. The full context CM used in C7 and in the distillation mode is the file
polkit_context.md version 2; the partial-context conditions C1 . . . C6 are con-
structed by removing the corresponding sections from the same file and leaving
the response-format header intact.


6     Results

6.1   Validation of PolkitBench-v2

Table 3 reports the validation results for PolkitBench-v2. All 10,073 candidates
pass AST validation; 10,043 pass the runtime decision check; 30 are rejected at
the runtime stage. Manual inspection of the failures shows that 23 of 30 are
caused by candidate rules referencing edge-case action.id strings that have
changed shape between Polkit versions (e.g., a deprecated string variant for a
NetworkManager action); the remaining 7 are decisions where the test pkcheck
returned AUTH_ADMIN where the reference rule declared AUTH_SELF. The 99.7%
runtime acceptance rate compares favourably with the validation throughput of
synthetic policy corpora that rely on static checks only.
                     Context-Aware Distillation and Ablation for Text2DSL        11

               Table 3. Validation of PolkitBench-v2 (N = 10,073).


      Stage                                           Pass count     Pass rate
      AST validation (esprima + structural checks) 10,073 / 10,073 100.0 %
      Runtime: polkitd load                        10,073 / 10,073 100.0 %
      Runtime: pkcheck decision                    10,043 / 10,073 99.7 %




6.2   Baseline vs. Context across Both PolkitBench Generations

Table 4 reports the cross-corpus comparison on GigaChat-10B. Four runs are
involved: PolkitBench-v1 in the baseline and context modes, and PolkitBench-
v2 in the baseline and context modes. All four use the same evaluated model
and identical inference parameters; only the corpus and the mode are varied.


Table 4. Baseline vs. Context on GigaChat-10B across PolkitBench-v1 (N = 4,204)
and PolkitBench-v2 (N = 10,073). Higher is better; bold marks the best value in each
column across the four conditions; TO is the count of inference timeouts.



Corpus / Mode          N Strict Syntax Struct. BLEU Jaccard Combined TO
v1 baseline        4,204 88.80 97.57 88.94 0.518             0.397        0.482 4
v1 context         4,204 77.05 98.60 98.64 0.829            0.736        0.801 2
v2 baseline       10,073 46.53 58.51 46.81 0.307             0.125        0.252 901
v2 context        10,073 60.03 97.37 97.32 0.788             0.660        0.750 161




Baseline collapses on the harder corpus. Moving from PolkitBench-v1 to
PolkitBench-v2 in the baseline mode, every metric degrades sharply: Syntax
Valid 97.6 → 58.5 % (−39.1 pp), Structure Valid 88.9 → 46.8 % (−42.1 pp),
CodeBLEU 0.518 → 0.307 (−0.211), Jaccard 0.397 → 0.125 (−0.272), Combined
0.482 → 0.252 (−0.230); the number of timeouts rises from 4 to 901. Qualitative
inspection of the failure modes on PolkitBench-v2 baseline shows three dominant
patterns: (i) absence of an extractable code block in the response, (ii) violations
of the top-level polkit.addRule(...) shape, and (iii) hallucinated action.id
values for the long tail of the new corpus’ wider query space.

Context is robust to corpus hardening. Moving from PolkitBench-v1 to
PolkitBench-v2 in the context mode, the same metrics degrade modestly: Syn-
tax 98.6 → 97.4 % (−1.2 pp), Structure 98.6 → 97.3 % (−1.3 pp), CodeBLEU
12                       Kozachok, Nazimov, Magomedov

                                                          GigaChat-10B on PolkitBench-v1 vs PolkitBench-v2
                        100   97.6                                    98.6     98.6                                                               97.4   97.3

                                     88.9

                                                                                      82.8
                                                                                                    80.1                                                        78.8
                         80
                                                                                             73.6                                                                             75.0


                                                                                                                                                                       66.0
     Score (% / x100)




                         60                                                                                   58.5

                                            51.8
                                                          48.2                                                       46.8

                                                   39.7
                         40

                                                                                                                            30.7
                                                                                                                                          25.2

                         20
                                                                                                                                   12.4




                          0
                                       v1 baseline                                v1 context                           v2 baseline                          v2 context

                                Syntax %                         Structure %                        CodeBLEU x100                  Jaccard x100             Combined x100




Fig. 1. GigaChat-10B on PolkitBench-v1 vs. PolkitBench-v2 in the baseline and con-
text modes. The harder PolkitBench-v2 collapses the baseline mode on every metric
while the context mode degrades only marginally.



0.829 → 0.788 (−0.041), Jaccard 0.736 → 0.660 (−0.076), Combined 0.801 →
0.750 (−0.051). The asymmetry of the two degradation profiles — catastrophic
for baseline, marginal for context — is the main quantitative finding of this pa-
per. Within the context mode the timeout count on the harder corpus is also
reduced by roughly an order of magnitude relative to baseline on the same corpus
(161 vs. 901).


Per-corpus context gain. Within PolkitBench-v1 the context mode gains +0.319
on Combined relative to baseline; within PolkitBench-v2 the gain rises to +0.497
(Fig. 2). The same pattern holds for Structure (+9.7 pp vs. +50.5 pp), Jaccard
(+0.339 vs. +0.535) and CodeBLEU (+0.310 vs. +0.481). The larger gain on
the harder corpus is consistent with the interpretation that the context mode is
bounded by the model’s intrinsic Polkit knowledge plus what CM supplies, while
the baseline mode is bounded only by the former — and the former degrades
fast as queries leave the head of the distribution.


Strict Success interpretation. Strict Success does not follow the same mono-
tone pattern, because it is the conjunction of four binary tests rather than a
soft quality measure. On PolkitBench-v1 it decreases from 88.8 % (baseline) to
77.1 % (context); the context mode improves Structure, BLEU, Jaccard and
Combined but is penalised on Strict Success. On PolkitBench-v2 the pattern
reverses: 46.5 % (baseline) → 60.0 % (context). We therefore use Strict Success
as an auxiliary indicator and rely on Syntax/Structure/CodeBLEU/Jaccard/-
Combined for cross-mode conclusions, as recommended in Section 5.3.
                                                         Context-Aware Distillation and Ablation for Text2DSL                           13

                                                         Context-Induced Gain: PolkitBench-v1 vs PolkitBench-v2
                                   60

                                                                                                                   53.5
                                                                         50.5                                                    49.7
                                                                                           48.1
                                   48


       Absolute gain (pp / x100)                  38.9

                                   36                                                                       33.9
                                                                                    31.0                                  31.9



                                   24




                                   12                             9.70



                                           1.03
                                    0
                                            Syntax                 Structure       CodeBLEU                  Jaccard      Combined

                                        v1 gain                                                   v2 gain




Fig. 2. Context-induced gain on PolkitBench-v1 vs. PolkitBench-v2 (GigaChat-10B).
The gain is larger on the harder corpus on every metric.


    To pinpoint which of the four binary tests drives the v1 regression we decom-
pose the 11.7 pp drop. The first three tests — code extraction, syntactic validity
and structural validity — equal or exceed the baseline in the context mode:
Syntax rises from 97.57% to 98.60% and Structure from 88.94% to 98.64%. The
regression is therefore not caused by malformed output. The remaining test —
zero hallucinated action.id — is the dominant cause: the previous work [1]
reported 1,413 invalid action.id instances on the v1 context run, and the cor-
responding figure on the GigaChat run used here is 1,075 instances. With a
mean of ≈ 1.0 hallucinated identifier per affected record on v1, this accounts for
≈ 22% of the 4,204 records and almost exactly matches the 22.9% Strict Success
failure rate of the context mode. The v1 regression is therefore an artefact of the
strict conjunction with the hallucination test, not a regression in structural or
syntactic quality.

Residual hallucinations. Even with full context, the absolute count of hallu-
cinated action.id instances rises with corpus size: 1,075 on PolkitBench-v1 to
4,817 on PolkitBench-v2 in the context mode. Per-record this is comparable (0.26
vs. 0.48 per response on average); the absolute number nevertheless makes clear
that residual hallucinations persist and are not eliminated by context injection.
We discuss this in Section 7.3.

6.3   Per-Component Ablation on GigaChat-10B
Table 5 reports the full 23 matrix on PolkitBench-v2; Fig. 3 visualises the Strict
Success and Combined Score columns.

Finding 1: Full context is uniformly best. C7 achieves the best value of every
metric reported in Table 5. This contrasts with pilot results on different teacher
models discussed in our prior work [1], where full context occasionally lagged a
14                        Kozachok, Nazimov, Magomedov




Table 5. Per-component ablation C0 . . . C7 on GigaChat-10B and PolkitBench-v2
(N = 10,073). Bold marks the best value in each column. Values in brackets are
95% Wilson confidence intervals for the binary metrics (Strict, Syntax, Structure);
95% normal-theory CI half-widths for the continuous metrics (BLEU, Jaccard, Com-
bined) are uniformly ≤ 0.006 across all conditions and are omitted from the table for
compactness.



Cond. Components                                                        Strict [95% CI] Syntax [95% CI] Struct. [95% CI] BLEU Jaccard Comb.
C0                      —                  46.53 [45.6,47.5] 58.51 [57.5,59.5] 46.81 [45.8,47.8] 0.307                                                                                           0.125 0.252
C1                      BNF                15.73 [15.0,16.4] 93.11 [92.6,93.6] 92.77 [92.3,93.3] 0.549                                                                                           0.143 0.427
C2                      API                25.20 [24.4,26.1] 93.05 [92.5,93.5] 92.87 [92.4,93.4] 0.497                                                                                           0.189 0.404
C3                      Vocab              22.62 [21.8,23.4] 94.52 [94.1,95.0] 52.09 [51.1,53.1] 0.571                                                                                           0.365 0.509
C4                      BNF + API          13.72 [13.1,14.4] 92.47 [91.9,93.0] 91.91 [91.4,92.4] 0.552                                                                                           0.149 0.431
C5                      BNF + Vocab        50.49 [49.5,51.5] 91.25 [90.7,91.8] 90.42 [89.8,91.0] 0.613                                                                                           0.385 0.545
C6                      API + Vocab        38.09 [37.2,39.0] 95.80 [95.4,96.2] 94.97 [94.5,95.4] 0.568                                                                                           0.357 0.504
C7                      BNF + API + Vocab 60.03 [59.1,61.0] 97.37 [97.0,97.7] 97.32 [97.0,97.6] 0.788                                                                                           0.660 0.750




                                                        GigaChat-10B Per-Component Ablation on PolkitBench-v2
                         100                                                                                                                                                             97.4    97.3
                                                                                                     94.5                                                           95.8   95.0
                                                       93.1    92.8           93.0    92.9                                92.5   91.9          91.2   90.4



                          80
                                                                                                                                                                                                          75.0
     Score (% / x100)




                          60   58.5
                                                                                                                                                             54.5
                                                                                                            52.1   50.9                                                           50.4
                                       46.8
                                                                       42.7                                                             43.1
                                                                                              40.4
                          40


                                                25.2

                          20




                           0
                                      C0 base                 C1 BNF                 C2 API                 C3 V           C4 BNF+API            C5 BNF+V              C6 API+V                 C7 Full

                                       Syntax %                                                      Structure %                                             Combined x100




Fig. 3. Per-component ablation of structured context on GigaChat-10B and
PolkitBench-v2. The full context C7 is uniformly best; the strongest partial condi-
tions C5 and C6 both contain the vocabulary.
                     Context-Aware Distillation and Ablation for Text2DSL       15

strong partial configuration; on GigaChat-10B no such inversion is observed on
PolkitBench-v2.


Finding 2: Among partials, C5 and C6 dominate. Among the six partial condi-
tions, C5 (BNF + Vocabulary) is best on Strict Success (50.5 %), CodeBLEU
(0.613), Jaccard (0.385) and Combined (0.545). C6 (API + Vocabulary) is best
on Syntax Valid (95.8 %) and Structure Valid (95.0 %). Both top partial condi-
tions contain the vocabulary.


Finding 3: BNF alone is structure-without-semantics. C1 (BNF only) lifts Syn-
tax from 58.5 % to 93.1 % and Structure from 46.8 % to 92.8 % — a large gain on
formal-correctness metrics. But it drops Strict Success to 15.7 % and yields Com-
bined 0.427, only marginally above C0 . The grammar alone teaches the model
to write formally-shaped rules but does not constrain the identifiers used inside
them, which is what Strict Success and Jaccard penalise.


Finding 4: API alone is weaker than vocabulary alone. C2 (API only) is similar
to C1 on Syntax/Structure but slightly behind on Jaccard (0.189); C3 (Vocabu-
lary only) is the strongest single-component condition on Combined (0.509, vs.
0.427 for C1 and 0.404 for C2 ). The Structure score in C3 collapses to 52.1 %,
however, because without BNF or API the model frequently emits rules outside
the expected callback shape.


Finding 5: BNF + API without vocabulary is the worst non-baseline partial. C4
scores 13.7 % Strict Success and Jaccard 0.149, both worse than several single-
component conditions. The interaction is negative on semantic metrics: grammar
and API jointly tighten the form of the rule while leaving the model free to invent
identifiers, which the strict and Jaccard tests both penalise.


Finding 6: Vocabulary alone collapses structural validity. C3 (Vocabulary only)
achieves Structure Valid 52.1% — far below all other contextual conditions and
only marginally above the baseline (46.8%) — despite having the second-best
partial Jaccard (0.365) and a competitive CodeBLEU (0.571). The interpreta-
tion is direct. The vocabulary V specifies the legal string-valued identifiers but
does not constrain the callback signature, the top-level polkit.addRule(...)
envelope or the use of polkit.Result.* return values. The model knows which
action.id values to use, but no longer how to wrap them, so it frequently emits
rules with correct identifiers in an incorrect structural envelope. This asymme-
try confirms that the three context components address different failure modes:
vocabulary fixes identifier choice, while BNF and API jointly fix structural cor-
rectness. It also explains the negative interaction observed in Finding 5 and
underpins the recommendation R1 of Section 7: any subset of CM that omits
BNF and API simultaneously is structurally fragile.
16       Kozachok, Nazimov, Magomedov

Finding 7: BNF and API have negative main effects on Strict Success. Table 6
          (Strict)              (Strict)
reports EBNF = −1.79 and EAPI            = −7.74, both negative. This is the same
mechanism that drives the v1 regression analysed in Section 6.2: supplying BNF
or API in isolation makes the model produce more structurally elaborate rules
with more identifier occurrences per response, while leaving identifier choice
unconstrained. The expanded surface area amplifies the probability of containing
at least one out-of-vocabulary identifier and consequently zeroes Strict Success.
Vocabulary has the opposite sign (+17.52) because it removes the very degree of
freedom that BNF and API would otherwise enlarge. The negative main effects
on Strict Success therefore do not contradict the positive main effects of the
same factors on syntactic and structural validity (+13.92 and +10.81, +22.33
and +24.66 respectively): each factor is helpful on the dimension it targets and
harmful on the dimension it does not, which is precisely why their joint use (C7 )
dominates.

Factor decomposition. Table 6 reports main effects (2) and Shapley values
per metric. The pattern is consistent across decompositions: Vocabulary has
the largest semantic effect (Combined +0.198, Jaccard +0.290, Strict Suc-
cess +17.5 pp); API and BNF have the largest structural effects (Shapley on
Structure: API +24.7, BNF +22.3, Vocabulary +3.5). The three components
are complementary rather than substitutable: their factorial sum on Combined
(0.198 + 0.111 + 0.066 = 0.375 in main-effect terms) is comparable to the C7 − C0
gap (0.498), with the residual accounted for by positive two-factor interactions,
principally BNF × Vocabulary and API × Vocabulary.


                         (m)                                 (m)
Table 6. Main effects EX (Eq. 2) and Shapley values ϕX on GigaChat-10B and
PolkitBench-v2. Main effect and Shapley value coincide for symmetric three-factor
designs.


      Factor        Strict     Syntax   Structure   BLEU      Jaccard   Combined
      BNF           −1.79      +13.92     +22.33    +0.072     −0.005     +0.066
      API           −7.74      +10.81     +24.66    +0.045     +0.018     +0.046
      Vocabulary   +17.52      + 9.21     + 3.52    +0.131     +0.290     +0.198




7     Discussion

7.1     Practical Implications

The combined evidence of Sections 6.2 and 6.3 translates into three actionable
recommendations for practitioners building a Text2DSL pipeline.
                      Context-Aware Distillation and Ablation for Text2DSL        17

(R1) Keep the full context. The unique uniformly-best condition is C7 . There
is no smaller subset of CM on GigaChat-10B that is competitive across all five
primary metrics. Pruning CM to “the one strongest piece” is not supported.
(R2) If the context must be reduced, retain the vocabulary. The two
best partial conditions (C5 , C6 ) both contain the vocabulary; the worst non-
baseline partial (C4 = BNF + API) lacks it. Vocabulary contributes the largest
semantic-quality effect and is the cheapest component to maintain (it is a flat
list rather than a grammar or a specification document).
(R3) Treat the distilled corpus as a renewable artefact, not a frozen
one. PolkitBench-v2 is bound to a specific version of CM via per-record prove-
nance. When CM is updated — a new action.id subsystem, a tightened gram-
mar, a revised polkit.Result interpretation — the procedure of Algorithm 1
can be re-run to produce an updated corpus that carries the new provenance,
without manual labelling.

7.2   Relation to Prior PolkitBench Results
The previous work [1] reported context-induced gains on PolkitBench-v1 with
GigaChat-10B of +18.9 pp Syntax, +35.5 pp Structure and +0.399 Combined;
the corresponding gains on PolkitBench-v2 reported here are +38.9 pp Syntax,
+50.5 pp Structure and +0.497 Combined. The two sets of numbers are consis-
tent in direction and consistent in the qualitative ordering of metric sensitivities.
The larger absolute gains on PolkitBench-v2 reflect the larger headroom on a
harder corpus rather than a change in the underlying effect: on every metric the
context mode sits in roughly the same band (Syntax ≈ 97 %, Structure ≈ 97 %,
Combined ≈ 0.75–0.80) on both corpora, while baseline drops markedly.
    The two corpora also serve different roles. PolkitBench-v1 remains useful as
a tighter, smaller, manually-reviewable benchmark; PolkitBench-v2 is the larger
and operationally more realistic corpus that exposes failure modes invisible on
the smaller one, in particular the timeout mode (183 → 24 for context in v1;
901 → 161 in v2) and the long-tail identifier hallucinations.

7.3   Limitations and Threats to Validity
We list five limitations bounding the scope of the conclusions.
1. One evaluated model. The ablation is reported on a single evaluated model
(GigaChat-10B-A1.8B). The previous work [1] showed that the direction of the
full-context effect is consistent across two MoE models of different scale and
provenance; the per-component ranking reported here may shift on dense trans-
formers or on models substantially smaller or larger than 10B parameters. Repli-
cating the 23 matrix on Nemotron-3-Nano-30B-A3B and on additional dense
models is the natural next step.
2. One teacher. PolkitBench-v2 is distilled by a single teacher (DeepSeek-
V4-Flash). The corpus inherits whatever distributional biases that teacher has
under the supplied CM, even though every record is independently verified. A
multi-teacher distillation would lower this risk.
18      Kozachok, Nazimov, Magomedov

3. Residual identifier hallucinations. The context mode on PolkitBench-v2
still emits 4,817 instances of out-of-vocabulary action.id strings (≈ 0.48 per
response on average). This means Strict Success = 0 for roughly 40% of the
records where the hallucination test is the sole cause of failure. Two implemen-
tation paths for mitigation are immediate and compatible with the distillation
method of Section 3; a full mitigation experiment is reserved for a follow-up
paper.
     (a) Post-hoc identifier rewrite. Each emitted action.id candidate is matched
against V ; if absent, it is replaced by its nearest neighbour in V under Leven-
shtein distance, subject to a similarity threshold below which the response is left
unchanged rather than rewritten incorrectly. This mechanism is consistent with
the hallucination patterns reported in the previous work [1], where most fabri-
cated identifiers differ from the closest valid value by a small suffix substitution
(e.g. disable-net vs. disable-wifi, package-update vs. system-update) and
would therefore be recovered by edit-distance rewriting.
     (b) Grammar-constrained decoding restricted to V . Combining context injec-
tion with constrained decoding [14,15] so that the decoder accepts only members
of V in identifier positions provides a hard guarantee but requires decoder-level
integration with the local serving stack. We regard (a) as the cheaper first step
and (b) as the principled long-term solution.
4. Strict Success as a binary indicator. Strict Success is an integrated end-
to-end indicator and aggregates four binary tests. It is intentionally pessimistic
and should not be read as a soft quality metric; we use it as a deployment-
readiness signal.
5. Runtime validation in a containerised environment. The polkitd +
pkcheck pipeline models the production decision path but is not a substitute for
the full diversity of system configurations encountered in deployed Linux distri-
butions. Edge cases tied to specific D-Bus configurations or to the interaction of
Polkit with other authorisation layers are outside the scope of this evaluation.


8    Conclusion

We have presented a context-aware distillation method that produces verified
Text2DSL corpora bound to an explicit context model, and a two-tier validation
pipeline that combines AST parsing with runtime acceptance by the production
Polkit daemon. Applied to Polkit with DeepSeek-V4-Flash as teacher, the pro-
cedure yields PolkitBench-v2: 10,073 verified natural-language–to–rule pairs at
100.0 % AST validity and 99.7 % runtime acceptance. The per-component fac-
torial ablation of structured context on GigaChat-10B-A1.8B identifies the full
context as the unique uniformly-best condition, identifies the vocabulary as the
strongest semantic-quality driver, and identifies BNF and API as the strongest
syntactic and structural stabilisers. The cross-corpus comparison shows that the
context mode degrades only marginally on the harder PolkitBench-v2 (Com-
bined Score 0.801 → 0.750) while the baseline mode collapses on every metric
                       Context-Aware Distillation and Ablation for Text2DSL            19

(0.482 → 0.252), supporting the interpretation of structured context as a load-
bearing mechanism rather than a cosmetic improvement.
    Three directions for follow-up are immediate: replicating the 23 ablation
matrix on a dense transformer evaluated model; combining context injection
with grammar-constrained decoding to drive the residual identifier hallucina-
tion rate to zero; and extending the distillation procedure to a second policy
DSL (SELinux type enforcement or OPA Rego) to assess the portability of the
method.


Declaration of Generative AI Tools A teacher large language model
(DeepSeek-V4-Flash) was used to generate the synthetic candidate rules for
PolkitBench-v2 as described in Section 3.2. Every candidate was independently
validated by the AST and runtime pipeline of Section 3; no record was admit-
ted into the corpus on the strength of the teacher’s output alone. The authors
reviewed and edited the manuscript and take full responsibility for its content.


Declaration of Competing Interests The authors declare no competing
financial interests or personal relationships that could have appeared to influence
the work reported in this paper.


Data Availability The PolkitBench-v1 (4,204 pairs) and PolkitBench-v2
(10,073 pairs) corpora, the context model CM, the AST and runtime valida-
tors, the per-condition evaluation outputs and the factorial-ablation run logs
are released as part of the AI-Polkit research project.


References
 1. Kozachok, A.V., Nazimov, A.A., Magomedov, Sh.G.: Text2DSL: LLM-based code
    generation for domain-specific languages. In: Proc. 30th Int. Conf. Knowledge-
    Based and Intelligent Information & Engineering Systems (KES 2026). Procedia
    Computer Science (2026).
 2. freedesktop.org: Polkit reference manual. https://www.freedesktop.org/software/
    polkit/docs/latest/ (accessed 2026-05-12).
 3. Smalley, S., Vance, C., Salamon, W.: Implementing SELinux as a Linux security
    module. NAI Labs Report 01-043, NAI Labs, Network Associates Inc. (2001).
 4. Loscocco, P., Smalley, S.: Integrating flexible support for security policies into the
    Linux operating system. In: Proc. FREENIX Track, USENIX Annual Technical
    Conf., pp. 29–42 (2001).
 5. The Open Policy Agent Authors: OPA documentation. https://www.
    openpolicyagent.org/docs/latest/ (accessed 2026-05-12).
 6. HashiCorp: Terraform language documentation. https://developer.hashicorp.com/
    terraform/language (accessed 2026-05-12).
 7. Rahman, A., Parnin, C., Williams, L.: The seven sins: security smells in infrastruc-
    ture as code scripts. In: Proc. 41st Int. Conf. on Software Engineering (ICSE), pp.
    164–175 (2019). doi:10.1109/ICSE.2019.00033
20      Kozachok, Nazimov, Magomedov

 8. Saavedra, N., Ferreira, J.F.: GLITCH: Automated polyglot security smell detection
    in infrastructure as code. In: Proc. 37th IEEE/ACM Int. Conf. on Automated
    Software Engineering (ASE), Art. No. 19, pp. 1–12 (2022). doi:10.1145/3551349.
    3556945
 9. Mernik, M., Heering, J., Sloane, A.M.: When and how to develop domain-specific
    languages. ACM Computing Surveys 37(4), 316–344 (2005). doi:10.1145/1118890.
    1118892
10. Yu, T., Zhang, R., Yang, K., Yasunaga, M., Wang, D., Li, Z., Ma, J., Li, I., Yao,
    Q., Roman, S., Zhang, Z., Radev, D.: Spider: a large-scale human-labeled dataset
    for complex and cross-domain semantic parsing and Text-to-SQL task. In: Proc.
    2018 Conf. on Empirical Methods in Natural Language Processing (EMNLP), pp.
    3911–3921 (2018). doi:10.18653/v1/D18-1425
11. Pourreza, M., Rafiei, D.: DIN-SQL: decomposed in-context learning of Text-to-
    SQL with self-correction. In: Advances in Neural Information Processing Systems
    36 (NeurIPS 2023), pp. 36339–36348 (2023).
12. Li, H., Zhang, J., Li, C., Chen, H.: RESDSQL: decoupling schema linking and skele-
    ton parsing for Text-to-SQL. In: Proc. 37th AAAI Conf. on Artificial Intelligence,
    pp. 13067–13075 (2023). doi:10.1609/aaai.v37i11.26535
13. Scholak, T., Schucher, N., Bahdanau, D.: PICARD: parsing incrementally for con-
    strained auto-regressive decoding from language models. In: Proc. 2021 Conf. on
    Empirical Methods in Natural Language Processing (EMNLP), pp. 9895–9901
    (2021). doi:10.18653/v1/2021.emnlp-main.779
14. Poesia, G., Polozov, O., Le, V., Tiwari, A., Soares, G., Meek, C., Gulwani, S.:
    Synchromesh: reliable code generation from pre-trained language models. In: Proc.
    10th Int. Conf. on Learning Representations (ICLR) (2022).
15. Geng, S., Josifoski, M., Peyrard, M., West, R.: Grammar-constrained decoding
    for structured NLP tasks without finetuning. In: Findings of the Association for
    Computational Linguistics: EMNLP 2023, pp. 10932–10952 (2023). doi:10.18653/
    v1/2023.findings-emnlp.733
16. Feng, Z., Guo, D., Tang, D., Duan, N., Feng, X., Gong, M., Shou, L., Qin, B., Liu,
    T., Jiang, D., Zhou, M.: CodeBERT: a pre-trained model for programming and
    natural languages. In: Findings of the Association for Computational Linguistics:
    EMNLP 2020, pp. 1536–1547 (2020). doi:10.18653/v1/2020.findings-emnlp.139
17. Guo, D., Ren, S., Lu, S., Feng, Z., Tang, D., Liu, S., Zhou, L., Duan, N., Svy-
    atkovskiy, A., Fu, S., Tufano, M., Deng, S.K., Clement, C., Drain, D., Sundaresan,
    N., Yin, J., Jiang, D., Zhou, M.: GraphCodeBERT: pre-training code representa-
    tions with data flow. In: Proc. 9th Int. Conf. on Learning Representations (ICLR)
    (2021).
18. Wang, Y., Wang, W., Joty, S., Hoi, S.C.H.: CodeT5: identifier-aware unified pre-
    trained encoder-decoder models for code understanding and generation. In: Proc.
    2021 Conf. on Empirical Methods in Natural Language Processing (EMNLP), pp.
    8696–8708 (2021). doi:10.18653/v1/2021.emnlp-main.685
19. Li, R., Allal, L.B., Zi, Y., Muennighoff, N., Kocetkov, D., Mou, C., Marone, M.,
    et al.: StarCoder: may the source be with you! Transactions on Machine Learning
    Research (TMLR), 2023 (2023).
20. Nijkamp, E., Pang, B., Hayashi, H., Tu, L., Wang, H., Zhou, Y., Savarese, S., Xiong,
    C.: CodeGen: an open large language model for code with multi-turn program
    synthesis. In: Proc. 11th Int. Conf. on Learning Representations (ICLR) (2023).
21. Jain, N., Vaidyanath, S., Iyer, S., Natarajan, N., Parthasarathy, S., Rajamani, S.,
    Sharma, R.: Jigsaw: large language models meet program synthesis. In: Proc. 44th
                       Context-Aware Distillation and Ablation for Text2DSL            21

    Int. Conf. on Software Engineering (ICSE), pp. 1219–1231 (2022). doi:10.1145/
    3510003.3510203
22. Hinton, G., Vinyals, O., Dean, J.: Distilling the knowledge in a neural network. In:
    NeurIPS Deep Learning and Representation Learning Workshop (2014).
23. Gou, J., Yu, B., Maybank, S.J., Tao, D.: Knowledge distillation: a survey. In-
    ternational Journal of Computer Vision 129(6), 1789–1819 (2021). doi:10.1007/
    s11263-021-01453-z
24. Jiao, X., Yin, Y., Shang, L., Jiang, X., Chen, X., Li, L., Wang, F., Liu, Q.: Tiny-
    BERT: distilling BERT for natural language understanding. In: Findings of the
    Association for Computational Linguistics: EMNLP 2020, pp. 4163–4174 (2020).
    doi:10.18653/v1/2020.findings-emnlp.372
25. Wang, Y., Kordi, Y., Mishra, S., Liu, A., Smith, N.A., Khashabi, D., Hajishirzi, H.:
    Self-Instruct: aligning language models with self-generated instructions. In: Proc.
    61st Annual Meeting of the Association for Computational Linguistics (ACL), Vol.
    1: Long Papers, pp. 13484–13508 (2023). doi:10.18653/v1/2023.acl-long.754
26. Xu, C., Sun, Q., Zheng, K., Geng, X., Zhao, P., Feng, J., Tao, C., Lin, Q., Jiang,
    D.: WizardLM: empowering large pre-trained language models to follow complex
    instructions. In: Proc. 12th Int. Conf. on Learning Representations (ICLR) (2024).
27. Luo, Z., Xu, C., Zhao, P., Sun, Q., Geng, X., Hu, W., Tao, C., Ma, J., Lin, Q., Jiang,
    D.: WizardCoder: empowering code large language models with Evol-Instruct. In:
    Proc. 12th Int. Conf. on Learning Representations (ICLR) (2024).
28. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H.,
    Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., Kiela, D.: Retrieval-augmented
    generation for knowledge-intensive NLP tasks. In: Advances in Neural Information
    Processing Systems 33 (NeurIPS 2020), pp. 9459–9474 (2020).
29. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E.H., Le,
    Q.V., Zhou, D.: Chain-of-thought prompting elicits reasoning in large language
    models. In: Advances in Neural Information Processing Systems 35 (NeurIPS 2022),
    pp. 24824–24837 (2022).
30. Papineni, K., Roukos, S., Ward, T., Zhu, W.-J.: BLEU: a method for automatic
    evaluation of machine translation. In: Proc. 40th Annual Meeting of the Association
    for Computational Linguistics (ACL), pp. 311–318 (2002). doi:10.3115/1073083.
    1073135
31. Eghbali, A., Pradel, M.: CrystalBLEU: precisely and efficiently measuring the sim-
    ilarity of code. In: Proc. 37th IEEE/ACM Int. Conf. on Automated Software En-
    gineering (ASE), Art. No. 28, pp. 1–12 (2022). doi:10.1145/3551349.3556903
32. Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Nee-
    lakantan, A., Shyam, P., Sastry, G., Askell, A., et al.: Language models are few-
    shot learners. In: Advances in Neural Information Processing Systems 33 (NeurIPS
    2020), pp. 1877–1901 (2020).
