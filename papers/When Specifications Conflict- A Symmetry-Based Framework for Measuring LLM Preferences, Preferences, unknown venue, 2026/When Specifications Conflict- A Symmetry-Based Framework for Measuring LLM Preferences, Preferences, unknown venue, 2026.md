                                         When Specifications Conflict: A Symmetry-Based Framework for Measuring LLM
                                                                           Preferences
                                                                      Tairan Wang* , Liang Zhou, Zikang Zhan* , Pingchuan Yan
                                                                                          Department of Computer Science
                                                                                             University College London
                                                                                              London, United Kingdom
                                                                     {tairan.wang.22, liang.zhou.22, zikang.zhan.22, maestro.yan.22}@ucl.ac.uk
                                                                                              *
                                                                                                Corresponding authors.

                                                                     Abstract                                 support incompatible behaviors, the model must implicitly
                                                                                                              determine which specification governs its final response. Un-
                                           Large language models (LLMs) are increasingly required to
                                           integrate multiple sources of information that may be in-          derstanding this selection behavior is important because it
                                           consistent or even conflicting. However, there is still a lack     reveals the implicit hierarchy that models assign to different
                                           of controllable and attributable methods for systematically        forms of specification and is essential for designing reliable
                                           analyzing how models resolve conflicts between competing           LLM-based systems.
                                           specifications. We propose a controlled experimental frame-           Prior work has studied how LLMs detect, reconcile,
                                           work for studying model preferences under conflicting spec-        or respond to conflicting information in settings such as
arXiv:2607.28384v1 [cs.AI] 30 Jul 2026




                                           ifications. By constructing specifications with explicit con-      retrieval-augmented generation, fact-checking, and multi-
                                           flicts, the framework enables model choices between com-           context question answering (Ge et al. 2025; Li et al. 2025;
                                           peting specifications to be directly observed and analyzed.
                                           A symmetry-based experimental design further reduces the
                                                                                                              Zeng et al. 2025; Hou et al. 2024; Kurfalı 2025; Lee, Kang-
                                           influence of confounding factors, allowing preferences as-         min, and Kim 2025). Other studies have examined how
                                           sociated with different representation types to be compared        models select among competing evidence or information
                                           systematically.                                                    sources (Schuster, Gautam, and Markert 2026). However,
                                           We evaluate the framework on an executable mathemati-              existing studies have primarily focused on conflicts among
                                           cal benchmark consisting of 550 conflict instances span-           information sources, while how models prioritize different
                                           ning 11 function families, comparing four representation           forms of task specification remains less understood. In par-
                                           types: pure natural language, formal language, naturalized         ticular, it remains unclear whether LLMs exhibit system-
                                           formal language, and input–output examples. The results            atic preferences when the same underlying task is expressed
                                           show that model behavior under conflict is systematic rather       through different representations, how these preferences vary
                                           than random, exhibiting a consistent preference ordering of        across models, and whether they generalize beyond con-
                                           Formal ≈ Naturalized Formal > Pure Natural Language >
                                                                                                              trolled settings.
                                           Input–Output Examples. We further find that the influence of
                                           examples depends on both model capability and the underly-            To answer these questions, we introduce a controlled,
                                           ing function family.                                               symmetry-based framework for measuring model preference
                                           Furthermore, we extend the framework to heterogeneous spec-        under conflicting specifications. We represent a task through
                                           ification conflicts in Boolean algebra, code generation, and the   competing executable mappings that produce different out-
                                           clinical domain, demonstrating its applicability across differ-    puts on a discriminative query. Because each specification
                                           ent tasks and specification forms. These experiments show that     supports a distinct candidate output, the model’s response can
                                           the framework can characterize model preferences under di-         be directly attributed to one mapping, the other mapping, or
                                           verse conflict settings while preserving attributable preference   neither. We further construct symmetry-complete configura-
                                           measurement, providing a unified experimental framework for        tions that counterbalance presentation order and the assign-
                                           analyzing conflict resolution behavior in large language mod-      ment of representation types to candidate mappings. This
                                           els across different domains.
                                                                                                              turns conflict resolution into an attributable specification-
                                                                                                              selection problem while reducing the influence of non-target
                                                                 Introduction                                 factors.
                                         Large language models (LLMs) increasingly operate in set-               We instantiate the framework in a controlled mathematical
                                         tings where multiple pieces of contextual information jointly        benchmark containing 550 conflict instances across 11 func-
                                         specify how a task should be performed (Lewis et al. 2020;           tion families and compare four representation types: pure
                                         Yang et al. 2018; Feldman and El-Yaniv 2019). These speci-           natural language, formal language, naturalized formal lan-
                                         fications may take diverse forms, including natural language         guage, and input–output examples. Our experiments reveal
                                         instructions, examples, formal constraints, and executable           systematic representation preferences across models, with
                                         tests. In practice, such specifications may be incomplete, in-       Formal and Naturalized Formal specifications consistently
                                         consistent, or directly conflicting (Hou et al. 2024; Zhang          preferred over Pure Natural Language and Input–Output Ex-
                                         et al. 2025; Liu and Roth 2025). When two specifications             amples. We further show that naturalized formal specifica-
tions behave much more like formal specifications than like                                    Method
an intermediate representation, while the influence of exam-        We propose a framework for measuring model preference un-
ples varies across models and task families.                        der conflicting specifications. The framework represents con-
   Finally, we extend the framework to heterogeneous spec-          flicts as competing executable mappings and uses symmetry-
ification conflicts in Boolean algebra, code generation, and        complete counterbalancing to attribute model outputs while
clinical rule settings. These cases demonstrate that the frame-     reducing effects from non-target factors such as presentation
work can measure attributable specification preferences be-         order and mapping assignment.
yond the controlled mathematical benchmark. Overall, this
work establishes conflict resolution in LLMs as a con-              A Symmetry-Based Framework for Identifiable
trolled, executable, and symmetry-counterbalanced measure-          Preference Attribution
ment problem, enabling systematic analysis of how models
prioritize different forms of specification.                        To characterize LLM preferences under conflicting speci-
                                                                    fications, we formulate a framework that represents model
                                                                    behavior under multiple competing specifications as a selec-
          Background and Related Work                               tion process over candidate mappings.
                                                                       We begin by defining a set of conflicting specifications,
Prior studies have shown that conflicts are widespread across       each of which induces a different output for the same input.
different types of contextual information and can affect LLM        In this way, conflict is formalized as an inconsistency relation
reliability. Liu and Roth analyze conflicts in natural texts,       among candidate mappings.
human annotations, and model interactions, while Xu et al.             Model outputs are then interpreted as the outcomes of
provide a systematic categorization of knowledge conflicts          this selection process. Since each specification determines a
in LLMs. Zhou et al. further show that models may exhibit           concrete output for the queried input, the model prediction
preferences among competing information sources, suggest-           can be directly attributed to one specification, turning an
ing that conflict resolution depends on the properties of con-      implicit decision into an observable variable.
flicting contexts and sources (Liu and Roth 2025; Xu et al.            Building on this formulation, measuring model preference
2024; Zhou et al. 2024).                                            requires handling two types of interfering factors. The first
   Recent benchmarks have developed controlled evaluations          consists of factors that cannot be disentangled within a single
of conflict resolution. WikiContradict studies whether mod-         configuration, such as presentation order, whose influence is
els can recognize and synthesize contradictory but equally          coupled with other factors. To address this, we construct
credible Wikipedia evidence (Hou et al. 2024), while MAGIC          symmetric configurations so that the effect of such factors
introduces structured knowledge-graph-based conflicts for           appears with opposite directions across configurations and
analyzing conflict detection and localization (Lee, Kangmin,        cancels out in the aggregate.
and Kim 2025). These works primarily focus on whether                  The second consists of factors that cannot be precisely
models can identify, localize, or reconcile conflicting infor-      controlled, such as subtle differences in how content is ex-
mation.                                                             pressed across specifications. Prior work has shown that even
   Beyond conflict resolution, recent work has examined pref-       meaning-preserving changes in prompt formatting can sub-
erence among competing information sources. Wan et al.              stantially affect model behavior (Sclar et al. 2024). Such
show through the CONFLICTINGQA benchmark that LLM                   variation may introduce unintended asymmetries and thereby
decisions can be influenced by properties of competing evi-         affect selection behavior. To mitigate this source of bias, we
dence, which may not align with human judgments of cred-            construct specifications that are symmetric in structure and
ibility (Wan, Wallace, and Klein 2024). Schuster et al. fur-        matched in informational content, while avoiding fixed sur-
ther study source preferences under inter-context knowledge         face templates that could introduce systematic lexical cues.
conflicts and demonstrate systematic preferences toward dif-           Symmetry operates at both the configuration and specifica-
ferent source types (Schuster, Gautam, and Markert 2026).           tion levels, reducing uncontrolled asymmetries and enabling
   Complementary to these studies, Parasaram et al. show            preference estimation through aggregation over symmetry-
that different organizations and combinations of contextual         complete configurations.
information can lead to different LLM behaviors in software
engineering scenarios (Parasaram et al. 2024), suggesting           Problem Formulation
that the representation and organization of task-relevant in-       Let X denote the input space and Y the output space. A task
formation can influence model decisions.                            is defined by a mapping
   Our work studies a complementary but different dimension
of preference. Whereas previous studies mainly vary source                                    f : X → Y.
reliability, attribution, or context organization, we investigate
how models choose between incompatible task specifications          A specification s provides a description of the task and in-
expressed through different representation types. Each spec-        duces a candidate mapping
ification corresponds to an executable candidate mapping,                                    fs : X → Y.
enabling model responses to be directly attributed to com-
peting specifications and allowing preference to be measured          We consider a set of specifications {s1 , s2 , . . . , sk }, and
under controlled conflicts.                                         assume that the corresponding candidate mappings produce
distinct and attributable outputs for the query inputs under
consideration.
   Given a prompt containing a subset of these specifications
and a query input x, the model produces a prediction ŷ. Since
each specification defines a concrete output for the same
input, the model prediction can be interpreted as selecting
one of the candidate mappings.
   Our objective is to characterize the model’s selection
behavior under such conflicts, i.e., which specification the
model follows under different conditions.

Preference Attribution
Under a fixed configuration, attribution yields a conditional
quantity that depends on both the target factor and other
factors in the setup. Rather than interpreting this quan-
                                                                  Figure 1: Example conflict instance represented in four spec-
tity directly, we estimate preference by aggregating over a
                                                                  ification formats: pure natural language (NL), formal speci-
symmetry-complete set of configurations.
                                                                  fication (Form), naturalized formal specification (NatF), and
   Specifically, let U denote the set of configurations gener-
                                                                  input–output examples (Ex).
ated by symmetric transformations over non-target factors.
We define the preference for a target factor value t as
                                                                  structure while inducing different executable outputs. We
                                              
               P (t) = Eu∈U P select t | t, u .
                                                                  then generate a discriminative query q ⋆ satisfying
where “select t” denotes selecting a specification with factor
value t.                                                                                f1 (q ⋆ ) ̸= f2 (q ⋆ ).
   By construction, symmetry operates at two levels:                 For each conflict pair, the dataset stores q ⋆ , the corre-
configuration-level symmetry offsets factors such as order        sponding outputs, and executable implementations of both
that cannot be independently isolated, while specification-       mappings, enabling automatic attribution during evaluation.
level symmetry reduces unintended asymmetries in infor-           For example-based representations, we additionally provide
mation content. The resulting P (t) provides a preference         input–output examples sampled from each mapping while
estimate after marginalizing over symmetry-controlled con-        excluding q ⋆ , ensuring that the discriminative query cannot
figurations, reducing sensitivity to configuration-specific ar-   be answered by direct retrieval.
tifacts.                                                             For each mapping, DeepSeek-V4-Pro (DeepSeek-AI 2026)
                                                                  generates three specification realizations: natural language,
                  Experimental Setup                              formal, and naturalized formal specifications. The model is
The framework constructs conflicts between two executable         used only for realizing predefined executable semantics; all
mappings, f1 and f2 , represented through four specification      mappings, queries, outputs, and labels are determined stati-
formats: pure natural language, formal specifications, nat-       cally.
uralized formal specifications, and input–output examples,
as shown in Figure 1. Specification order and mapping as-         Experimental Protocol
signment are counterbalanced, allowing model outputs to be        We evaluate how models resolve conflicts between four repre-
attributed to f1 , f2 , or other.                                 sentation types: pure natural-language specifications, formal
                                                                  specifications, naturalized formal specifications, and input–
Mathematical Conflict Benchmark                                   output examples. We consider all six unordered representa-
We construct a mathematical benchmark for measuring               tion pairs: pure natural language versus formal, pure natural
model behaviour under conflicting specifications. Mathemat-       language versus naturalized formal, pure natural language
ics provides executable semantic ground truth: each task is       versus examples, formal versus naturalized formal, formal
defined by a function, allowing model outputs to be directly      versus examples, and naturalized formal versus examples.
compared against competing candidate mappings.                       Each trial is constructed from one conflict instance con-
   The benchmark contains 550 conflict instances from 11          taining two conflicting executable mappings, f1 and f2 , and
parameterized function families, with 50 independently gen-       a discriminative query q ⋆ . The two presented specifications
erated instances per family. The families cover diverse exe-      describe different mappings: one realizes f1 , while the other
cutable mathematical tasks, including algebraic functions,        realizes f2 . For each representation pair A, B, where A and
conditional rules, sequences, polynomial queries, graph           B denote the two representation types being compared and
problems, and matrix operations, with parameters sampled          A(fi ) denotes mapping fi expressed using representation
from bounded ranges to avoid degenerate cases.                    type A, we generate four counterbalanced trials per conflict
   For every base mapping f1 , we construct a conflicting         instance:
mapping f2 through family-specific, schema-preserving per-                       (A(f1 ), B(f2 )) (B(f1 ), A(f2 ))
turbations. These perturbations maintain the original task                       (A(f2 ), B(f1 )) (B(f2 ), A(f1 ))
                                                                     models (RQ2), and finally examine heterogeneous specifica-
                                                                     tion conflicts beyond the controlled benchmark (RQ3).

                                                                     Pairwise Representation Preferences
                                                                     Models consistently favor specifications that retain explicit
                                                                     mathematical structure. As shown in Figure 3, formal spec-
                                                                     ifications are selected over pure natural-language specifica-
                                                                     tions in 87.45% of attributable responses, and naturalized
                                                                     formal specifications are selected over pure natural-language
                                                                     specifications in 86.77%. The gap is even larger when the
Figure 2: Example prompt construction and output attribu-
                                                                     alternative is a set of input–output examples: formal specifi-
tion procedure. Responses are attributed to f1 , f2 , or other by
                                                                     cations are selected over examples in 93.04% of responses,
comparing model outputs with the stored candidate outputs.
                                                                     while naturalized formal specifications are selected over ex-
                                                                     amples in 93.27%. Pure natural-language specifications also
                                                                     beat examples overall, but less decisively, with a selection
This design counterbalances both the presentation order of           rate of 77.80%.
the two specifications and the assignment of representation
                                                                        The main pattern is therefore clear:
types to the underlying mappings.
   Example-based sources contain coherent input–output ex-                       Formal ≈ Naturalized Formal
amples generated from their associated executable mapping.
                                                                                        > Pure Natural Language
Most instances provide ten examples per mapping; graph de-
gree queries provide four examples because of the smaller                               > Input–Output Examples.
graph representation. The examples do not include the dis-
                                                                     This ordering is broadly reflected across models, although
criminative query q ⋆ .
                                                                     the relative preference between pure natural language and
   In every trial, the model receives the two conflicting speci-
                                                                     examples varies across models.
fications and is asked to answer the query q ⋆ , as illustrated in
Figure 2. Models are instructed to provide a clearly identifi-          Formal and naturalized formal specifications are the only
able final answer, which is then extracted and normalized for        pair without a uniform direction. Overall, models select for-
attribution. We compare the extracted value against the stored       mal specifications in 59.67% of their direct comparisons.
executable outputs f1 (q ⋆ ) and f2 (q ⋆ ). A response matching      However, DeepSeek-V4-Flash (DeepSeek-AI 2026) favors
the first output is attributed to f1 , a response matching the       formal specifications strongly (69.67%), whereas GPT-5-
second is attributed to f2 , and a response matching neither         nano (OpenAI 2025a) instead favors naturalized formal spec-
is assigned to the other category.                                   ifications (55.24%). Thus, models agree much more strongly
                                                                     on the value of preserving mathematical structure than on
Generalizing the Framework to Heterogeneous                          whether that structure should be expressed as pure notation
                                                                     or embedded in natural language.
Specification Conflicts
We further evaluate the framework on Boolean algebra, code           When Do Examples Become Competitive?
generation, and clinical rule conflicts; construction and vali-
dation details are provided in the supplementary material.           Figure 4 summarizes example selection across models. The
                                                                     influence of coherent input–output examples varies substan-
Research Questions                                                   tially across models. This variation is most pronounced when
                                                                     examples compete with pure natural-language specifications.
To investigate this question, we study the following research        In this condition, GPT-5.4-nano (OpenAI 2026) selects the
questions:                                                           example-supported mapping in 55.64% of attributable re-
 • RQ1. When different representations of the same task              sponses, whereas Llama-3.3-70B (Dubey et al. 2024) selects
   support incompatible mappings, do language models ex-             it in only 2.98%. GPT-5-nano is approximately balanced in
   hibit systematic preferences for particular representation        this condition, selecting the example-supported mapping in
   types?                                                            49.63% of attributable responses. The remaining models fall
 • RQ2. How do representation preferences vary across dif-           between these extremes, with example-selection rates rang-
   ferent language models?                                           ing from 6.16% to 26.29%. Thus, example selection varies
                                                                     substantially across models when examples compete with
 • RQ3. How does the framework extend to heterogeneous               pure natural-language specifications.
   specification conflicts beyond the controlled mathemati-
                                                                         Examples are substantially less selected when the oppos-
   cal benchmark?
                                                                     ing specification preserves explicit mathematical structure.
                                                                     Against formal specifications, example selection ranges from
                           Results                                   1.00% for DeepSeek-V4-Flash to 26.00% for GPT-5.4-nano.
We organize the results around the three research questions.         The corresponding range against naturalized formal specifi-
We first evaluate representation preferences in the controlled       cations is 0.91% to 24.84%. These results show that model
mathematical benchmark (RQ1), analyze variation across               variation in example selection does not change the overall
                          DS-Flash                             DS-Pro                                GPT-4.1                             GPT-5.4
  Form > NL
   NatF > NL
   Form > Ex
   NatF > Ex
    NL > Ex
 Form > NatF
                              GPT-5                           Llama-3.3                              Llama-4                                Pooled
  Form > NL
   NatF > NL
   Form > Ex
   NatF > Ex
    NL > Ex
 Form > NatF

                        50%           75%     100%          50%        75%         100%            50%     75%       100%             50%            75%     100%
                                                         First-named representation selected (%)


Figure 3: Pairwise representation preferences across evaluated models. Each point shows the proportion of attributable responses
selecting the first-named representation in the comparison label. The dashed line marks 50%. Error bars show clustered-bootstrap
95% confidence intervals over conflict instances. The final panel aggregates results across models.

                                Ex vs NL                                         Ex vs Form                                        Ex vs NatF
  DS-Flash
   DS-Pro
   GPT-4.1
    GPT-5
   GPT-5.4
 Llama-3.3
   Llama-4

             0%   10%     20%     30%       40%   50%   60% 0%      10%      20%     30%     40%   50%    60% 0%      10%    20%      30%       40%    50%     60%
                                                        Example-supported mapping selected (%)


Figure 4: Selection of example-supported mappings across models. Each point shows the proportion of attributable responses
selecting the mapping specified by input–output examples under conflicts with different representation types.


preference pattern observed in the main benchmark: exam-                                   Model family        NL vs. Ex    Formal vs. Ex         NatF vs. Ex
ples are selected less frequently when the competing speci-                                DeepSeek             +8.10          +1.74                  +2.17
fication exposes explicit mathematical structure.                                          GPT                  +29.35         +17.75                 +16.52
   Within-family comparisons reveal systematic differences                                 Llama                +11.12         +1.83                  +2.54
between model variants. Table 1 summarizes the differ-
ences between model variants within the same model fam-                                Table 1: Maximum within-family differences in example se-
ily. Across all evaluated families, higher-capability variants                         lection. Values indicate percentage-point differences among
tend to select example-supported mappings more frequently,                             model variants with different capability levels within the
although the magnitude of the difference varies across rep-                            same model family.
resentation conflicts.

Robustness Checks
Presentation order has a secondary effect, but it does not ex-                         This suggests that position is more influential when compet-
plain the representation preferences reported above. Across                            ing specifications have similar overall strength. Additional
five of the six representation pairs, the pooled probability                           presentation-order analyses are provided in the supplemen-
of selecting the specification presented second ranges from                            tary material.
51.30% to 54.53%, which is small relative to the larger dif-                              We further examine whether the observed preferences
ferences associated with representation type. The main ex-                             could be affected by properties of the competing mappings
ception is the direct comparison between formal and nat-                               rather than their representation forms. Mapping identity is
uralized formal specifications, where the second-presented                             close to balanced: the minimum and maximum rates of at-
specification is selected in 67.86% of attributable responses.                         tributable responses selecting f2 across models are 50.64%
                                                                                                                                                                      MBPP Test Preference                     Claude-Opus-4.8-Thinking
                                   Form vs TT                                                            100%
  DS-Flash                                                                                                                                                        GPT-5-nano
                                                                                                                                                                                            DeepSeek-V4-Pro                      Kimi-K3
    DS-Pro                                                                                                                                                                                                            GPT-5.6-Luna
                                                                                                         80%




                                                                      Visible-test source selected (%)
                                                                                                                                                                                                     GPT-5.4-nano
   GPT-4.1
    GPT-5                                                                                                60%
                                                                                                                                                                                                                            GPT-5.6-Terra

   GPT-5.4
                                                                                                                                                                               DeepSeek-V4-Flash
 Llama-3.3                                                                                               40%                        Llama-3.3-70B-Instruct

                                                                                                                                         Llama-4-Scout

   Llama-4
                                                                                                         20%
             50%   60%       70%         80%        90%   100%
                             Formula selected (%)                                                                   Gemma-3-4B-IT
                                                                                                                                         GPT-4.1-nano


                                                                                                          0%
                                                                                                                0                   10                       20                   30                  40                   50               60
                                                                                                                                                                          Capability index
Figure 5: Results on the Boolean Algebra dataset, showing
model preferences between Boolean formulas (Form) and
truth tables (TT).                                                   Figure 6: Test preference across models with different ca-
                                                                     pability scores. Model capability is measured using the Ar-
                                                                     tificial Analysis Intelligence Index v4.1 (Artificial Analysis
and 51.66%, respectively. Responses assigned to other ac-            2026a,b)
count for 0.67% to 5.10% of all trials and are concentrated in
the pure-natural-language versus examples condition, where
the pooled rate is 6.36%, compared with 1.34% to 2.02%                  Additional comparisons involving gate-netlist are reported
for the remaining comparisons. We therefore report pair-             in the supplementary material, showing that gate netlists are
wise specification-selection rates over attributable responses       similarly preferred over truth tables, while formula vs gate-
throughout.                                                          netlist comparisons remain model-dependent.
                                                                     Code Generation We next apply our framework to code
Heterogeneous Specification Conflicts                                generation, where natural-language documentation and ex-
We next evaluate the framework on three heterogeneous                ecutable tests specify incompatible behaviors. From MBPP
specification-conflict settings: boolean algebra, code gener-        (Austin et al. 2021), we construct 67 verified conflict pairs
ation, and clinical rule conflicts. These settings differ in their   that preserve the original function signature and input domain
specification forms and output spaces, allowing us to ex-            but differ in one semantic slot, with one behavior grounded in
amine whether attributable preference measurement can be             the original task and the other forming a minimal alternative.
maintained beyond the controlled mathematical benchmark.             For each pair, we combine documentation for one behavior
                                                                     with visible tests for the other in four counterbalanced trials.
Boolean Algebra We constructed boolean-algebra conflict              Generated implementations are evaluated against validated
instances, as in the main experiments, the detailed con-             oracle suites and attributed to the documentation-supported
struction is illustrated in the supplementary material. Each         behavior, the test-supported behavior, or other. Further de-
instance contained two boolean expressions that differed             tails are provided in the supplementary material.
through a localized modification. One expression was repre-             As shown in Figure 6, specification preference varies
sented by a symbolic boolean formula, while the other was            sharply across models. Test-selection rates range from 16.5%
represented by its truth table.                                      for Gemma-3-4B-IT (Gemma-Team 2025) and 17.4% for
   Across from selected models, as shown in Figure 5, mod-           GPT-4.1-nano (OpenAI 2025b) to 94.0% for Kimi-K3
els exhibited consistent preference for boolean formula:             (MoonshotAI 2026) and 97.1% for Claude Opus 4.8 (An-
the formula-selection rate was 87.96%. Also, for the non-            thropic 2026). Although test preference does not increase
Llama models, presentation order and mapping identity re-            monotonically with the external capability score, the mod-
mained approximately balanced. In contrast, the two Llama-           els exhibit a broad capability-associated separation: lower-
family models exhibited a marked second-position prefer-             scoring models generally favor documentation, whereas the
ence, 70.25% and 66.75% of responses, but still follows the          highest-scoring models strongly favor tests.
result observed in Robustness Checks section.
   This preference is particularly notable because the unam-         Clinical Rule Conflicts We extend the framework to au-
biguous, exhaustive truth table specification allowed direct         thentic clinical rules drawn from public-domain openFDA
lookup for discriminative queries, whereas the formula re-           labels (U.S. Food and Drug Administration 2026). We con-
quired evaluation. If models prioritized computational con-          struct 166 conflicts over renal dosing thresholds and pedi-
venience or explicit completeness, the truth table would be          atric minimum-age indications, pairing each genuine thresh-
highly competitive. However, result suggests that, under con-        old with a schema-preserving perturbation. Perturbations are
flict, models strongly favor compact and compositionally             applied in both directions, making the genuine rule more re-
structured symbolic representations over exhaustive tabular          strictive in roughly half of the instances and allowing restric-
ones. This finding extends the main benchmark result beyond          tiveness to be separated from correctness. Rendering both
the original representation types and shows that expression          rules in all four representation types under the symmetry de-
preference persists.                                                 sign yields 7,968 counterbalanced trials across nine models
                                                                     conflicts reveal additional domain-specific influences beyond
                                                                     representation form.
                                                                        In code generation, conflicting software artifacts require
                                                                     models to select among competing intended behaviors rather
                                                                     than simply synthesize programs from a single specification.
                                                                     This reflects a latent specification-selection policy whose ef-
                                                                     fects are not inherently desirable or undesirable. Tests may
                                                                     provide precise executable specifications, but they may also
                                                                     be incomplete, stale, or erroneous. Reliable systems should
                                                                     therefore resolve conflicts contextually rather than univer-
                                                                     sally prioritizing tests or documentation.
Figure 7: Clinical rule conflicts. (a) Example-selection rates          Our main experiments characterize conflict resolution
against each textual form; all clustered-bootstrap intervals         when models are required to produce a task answer, but speci-
lie below 50%. (b) Genuine-value selection conditioned on            fication selection is not the only possible response to conflict-
whether the genuine rule is stricter or more permissive.             ing specifications. In an additional diagnostic experiment, we
                                                                     minimally modified the original prompt to allow an explicit
                                                                     uncertain response while keeping the conflict instances and
from five families. Appendix details the construction, cover-        experimental conditions unchanged. We evaluated this set-
age, and attribution procedures. These rules are transcribed         ting on two representative models: DeepSeek-V4 and GPT-
solely to measure model selection behavior and do not con-           5-nano selected this option in approximately 6% and 17% of
stitute medical advice.                                              trials, respectively. These results show that explicit absten-
   Across all 27 model–text comparisons, examples are the            tion can constitute an additional conflict-handling strategy,
least competitive specification: selection rates range from          and suggest that the tendency to defer resolution may vary
0.4% to 38.5%, with every clustered-bootstrap interval ex-           across models. Full experimental details are provided in the
cluding 50% (Figure 7a). The three textual forms show no             supplementary material.
stable ordering, so the mathematical ordering does not trans-           Our controlled framework isolates representation prefer-
fer to this domain.                                                  ences in conflicting specifications, but several limitations
   All nine models prefer the more restrictive rule (52%–            remain. Real-world conflicts are often more complex and
87%). Genuine-value selection remains near chance overall            may involve incomplete, ambiguous, or partially overlapping
(51%–57%), but splits to 70%–91% when the genuine rule is            specifications. Moreover, different representations cannot be
stricter and 17%–43% when it is more permissive for models           fully separated from accompanying factors such as descrip-
with the conservative tilt (Figure 7b). Given the bidirectional      tion length, information density, and level of detail, which
perturbations, this split tracks restrictiveness rather than label   may jointly contribute to the observed preferences. Finally,
correctness, revealing a domain-specific selection bias rather       our framework relies on executable outputs to infer specifica-
than a representation preference.                                    tion selection by comparing model responses with candidate
                                                                     specifications. Therefore, it is most naturally applicable to
                         Discussion                                  tasks with explicit behavioral mappings.
Our results show that models exhibit systematic preferences
among representation forms under conflicting specifications.                                 Conclusion
Formal and naturalized formal specifications are selected            We introduced a symmetry-based framework that represents
more frequently than less structured alternatives, suggest-          conflicting specifications as competing executable mappings,
ing that explicit structure facilitates conflict resolution by       enabling model responses to be attributed under counterbal-
directly exposing key constraints of the underlying map-             anced configurations. Across the mathematical benchmark,
ping. This may also explain why naturalized formal spec-             models systematically favored formal and naturalized for-
ifications behave similarly to formal ones despite their more        mal specifications, while the influence of examples depended
natural-language style. Pure natural-language and example-           on model capability and task structure. The heterogeneous
based specifications require greater inference from descrip-         experiments further showed that this ordering is not uni-
tions or finite observations, but examples are not inher-            versal: preferences varied across software and clinical set-
ently weaker. Their influence depends on model capability            tings, where domain-specific factors also shaped selection.
and task structure: higher-capability variants select example-       Together, these results characterize LLM conflict resolution
supported mappings more often, and examples are more com-            as structured but context-dependent specification selection
petitive when the underlying rule is easier to recover from          and provide a controlled approach for measuring such be-
demonstrations, particularly against pure natural-language           havior across tasks.
specifications. This interpretation is consistent with Wei et
al. (Wei et al. 2023), who find that learning input–label map-
pings from semantically unrelated exemplars improves with
model scale. The heterogeneous settings further show that
these preferences are context-dependent: Boolean algebra
favors compact structured representations, whereas clinical
                        References                                OpenAI. 2025a. GPT-5 System Card. https://openai.com/
Anthropic. 2026. Claude Opus 4.8 System Card. Technical           index/gpt-5-system-card/. Accessed 2026-07-29.
report, Anthropic.                                                OpenAI. 2025b. Introducing GPT-4.1 in the API. https:
Artificial Analysis. 2026a.        Artificial Analysis Intel-     //openai.com/index/gpt-4-1/. Accessed 2026-07-29.
ligence Benchmarking Methodology.                Available at     OpenAI. 2026.           Introducing GPT-5.4 Mini and
https://artificialanalysis.ai/methodology/intelligence-           Nano. https://openai.com/index/introducing-gpt-5-4-mini-
benchmarking; accessed 2026-07-27.                                and-nano/. Accessed 2026-07-29.
Artificial Analysis. 2026b. Comparison of AI Models across        Parasaram, N.; Yan, H.; Yang, B.; Flahy, Z.; Qudsi, A.; Zi-
Intelligence, Performance, and Price. Model-level Intelli-        aber, D.; Barr, E.; and Mechtaev, S. 2024. The fact selec-
gence Index scores. Available at https://artificialanalysis.ai/   tion problem in llm-based program repair. arXiv preprint
models/; accessed 2026-07-27.                                     arXiv:2404.05520.
Austin, J.; Odena, A.; Nye, M.; Bosma, M.; Michalewski, H.;       Schuster, J.; Gautam, V.; and Markert, K. 2026. Whose Facts
Dohan, D.; Jiang, E.; Cai, C.; Terry, M.; Le, Q.; and Sutton,     Win? LLM Source Preferences under Knowledge Conflicts.
C. 2021. Program Synthesis with Large Language Models.            In Liakata, M.; Moreira, V. P.; Zhang, J.; and Jurgens, D.,
arXiv:2108.07732.                                                 eds., Proceedings of the 64th Annual Meeting of the Associa-
DeepSeek-AI. 2026. DeepSeek-V4: Towards Highly Efficient          tion for Computational Linguistics (Volume 1: Long Papers),
Million-Token Context Intelligence. arXiv:2606.19348.             29430–29459. San Diego, California, United States: Asso-
Dubey, A.; Jauhri, A.; Pandey, A.; Kadian, A.; and et al.         ciation for Computational Linguistics. ISBN 979-8-89176-
2024. The Llama 3 Herd of Models. arXiv:2407.21783.               390-6.
Feldman, Y.; and El-Yaniv, R. 2019. Multi-hop paragraph re-       Sclar, M.; Choi, Y.; Tsvetkov, Y.; and Suhr, A. 2024. Quan-
trieval for open-domain question answering. In Proceedings        tifying Language Models’ Sensitivity to Spurious Features
of the 57th Annual Meeting of the Association for Computa-        in Prompt Design or: How I learned to start worrying about
tional Linguistics, 2296–2309.                                    prompt formatting. In The Twelfth International Conference
Ge, Z.; Wu, Y.; Chin, D. W. K.; Lee, R. K.-W.; and Cao,           on Learning Representations.
R. 2025. Resolving conflicting evidence in automated fact-        U.S. Food and Drug Administration. 2026. openFDA Drug
checking: A study on retrieval-augmented llms.                    Product Labeling API. Available at https://open.fda.gov/
Gemma-Team. 2025. Gemma 3 Technical Report.                       apis/drug/label/; accessed 2026-07-29.
Hou, Y.; Pascale, A.; Carnerero-Cano, J.; Tchrakian, T.;          Wan, A.; Wallace, E.; and Klein, D. 2024. What evidence
Marinescu, R.; Daly, E.; Padhi, I.; and Sattigeri, P. 2024. Wi-   do language models find convincing? In Proceedings of the
kicontradict: A benchmark for evaluating llms on real-world       62nd Annual Meeting of the Association for Computational
knowledge conflicts from wikipedia. Advances in Neural            Linguistics (Volume 1: Long Papers), 7468–7484.
Information Processing Systems, 37: 109701–109747.                Wei, J.; Wei, J.; Tay, Y.; Tran, D.; Webson, A.; Lu, Y.;
Kurfalı, M. 2025. Conflicting needles in a haystack: How          Chen, X.; Liu, H.; Huang, D.; Zhou, D.; and Ma, T. 2023.
LLMs behave when faced with contradictory information. In         Larger language models do in-context learning differently.
Proceedings of the 2025 Conference on Empirical Methods           arXiv:2303.03846.
in Natural Language Processing, 34349–34364.                      Xu, R.; Qi, Z.; Guo, Z.; Wang, C.; Wang, H.; Zhang, Y.; and
Lee, J.; Kangmin, L.; and Kim, T. 2025. MAGIC: A Multi-           Xu, W. 2024. Knowledge conflicts for llms: A survey. In
Hop and Graph-Based Benchmark for Inter-Context Con-              Proceedings of the 2024 Conference on Empirical Methods
flicts in Retrieval-Augmented Generation. In Findings of the      in Natural Language Processing, 8541–8565.
Association for Computational Linguistics: EMNLP 2025,            Yang, Z.; Qi, P.; Zhang, S.; Bengio, Y.; Cohen, W.; Salakhut-
8783–8803. Association for Computational Linguistics.             dinov, R.; and Manning, C. D. 2018. HotpotQA: A dataset
Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.;     for diverse, explainable multi-hop question answering. In
Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.-t.; Rocktäschel, T.;   Proceedings of the 2018 conference on empirical methods in
et al. 2020. Retrieval-augmented generation for knowledge-        natural language processing, 2369–2380.
intensive nlp tasks. Advances in neural information process-      Zeng, S.; Zhang, J.; Li, B.; Lin, Y.; Zheng, T.; Everaert,
ing systems, 33: 9459–9474.                                       D.; Lu, H.; Liu, H.; Xing, Y.; Cheng, M. X.; et al. 2025.
Li, Y.; Xu, C.; Xu, J.; and Wen, J.-R. 2025. BordaRAG: Re-        Towards knowledge checking in retrieval-augmented gener-
solving Knowledge Conflict in Retrieval-Augmented Gener-          ation: A representation perspective. In Proceedings of the
ation via Borda Voting Process. In Proceedings of the 34th        2025 Conference of the Nations of the Americas Chapter of
ACM International Conference on Information and Knowl-            the Association for Computational Linguistics: Human Lan-
edge Management, 1737–1747.                                       guage Technologies (Volume 1: Long Papers), 2952–2969.
Liu, S.; and Roth, D. 2025. Conflicts in texts: Data, im-         Zhang, G.; Xu, Z.; Jin, Q.; Chen, F.; Fang, Y.; Liu, Y.;
plications and challenges. Findings of the Association for        Rousseau, J. F.; Xu, Z.; Lu, Z.; Weng, C.; et al. 2025. Lever-
Computational Linguistics: EMNLP, 2025: 10073–10091.              aging long context in retrieval augmented language models
MoonshotAI. 2026. Kimi K3: Open Frontier Intelligence.            for medical question answering. npj Digital Medicine, 8(1):
arXiv:2607.24653.                                                 239.
Zhou, S.; Li, S.; Meng, Y.; Jiao, Y.; Ji, H.; and Han, J. 2024.   final answer with the two stored outputs. Table 3 presents
Establishing Knowledge Preference in Language Models.             representative conflict instances from different families.

    Mathematical Benchmark Construction                                          Specification Generation
This appendix describes the construction of the mathemati-        We use DeepSeek-V4-Pro to generate surface realizations
cal conflict-specification benchmark. The current benchmark       of statically defined executable mappings. Each realization
contains 550 conflict instances from 11 function families,        corresponds to the same underlying mapping, while differing
with 50 independently generated instances per family. Each        only in representation style. The generator is not given source
instance consists of two executable candidate mappings, de-       code, structured metadata, discriminative queries, candidate
noted by f1 and f2 , that share the same task family and          outputs, or the opposing mapping. Instead, each call receives
input–output schema but differ in selected metadata fields.       only a rendered formula or task-description string corre-
   The benchmark covers algebra, calculus, graph reasoning,       sponding to one executable mapping.
conditional rules, sequence reasoning, and matrix computa-           For quality control, we developed an HTML-based vi-
tion. Rather than treating all conflicts as uniform numerical     sualization tool that displayed each generated specification
perturbations, we construct family-specific alternative map-      alongside its corresponding executable mapping and the as-
pings that preserve the natural structure of each underlying      sociated conflict instance. All authors participated in manual
task. The goal is to make the two candidate functions min-        spot-checking across the three representation styles and the
imally different while remaining meaningfully distinguish-        11 function families. The inspection focused on semantic
able: each pair retains the same function family, input–output    faithfulness to the assigned mapping and on whether the
schema, and overall mathematical form, but differs on at least    generated realization introduced any unintended semantic
one valid query. This design allows the benchmark to vary the     change beyond the predefined difference between the two
underlying mathematical content without creating artificial       mappings.
or malformed tasks, while preserving executable semantics            For every conflict instance, f1 and f2 are processed in-
and automatic output attribution.                                 dependently. For each mapping, we generate three specifi-
                                                                  cation styles: pure natural language, formal specification,
Function Families                                                 and naturalized formal specification. Thus, each conflict
                                                                  pair yields six independently generated specifications. Pure
Table 2 summarizes the function families, their input–output
                                                                  natural-language specifications prohibit notation and sym-
schemas, and the corresponding conflict constructions. Meta-
                                                                  bolic formulas; formal specifications request minimal LATEX
data are sampled from bounded ranges, subject to family-
                                                                  mathematical expressions without explanatory prose; and
specific validity constraints described below.
                                                                  naturalized formal specifications retain mathematical nota-
   Across all families, we reject instances that are undefined,
                                                                  tion where useful while expressing the mapping in natural
degenerate, or not distinguishable under the two candidate
                                                                  language and remaining close to the rendered input. The
mappings. In particular, linear functions require nonzero
                                                                  executable mappings, discriminative queries, candidate out-
slopes and quadratic functions require nonzero leading coef-
                                                                  puts, and attribution labels are generated statically and do
ficients; rational functions must have nonzero denominator
                                                                  not depend on the language model used for specification
parameters and remain defined on all query and example
                                                                  realization.
inputs; threshold- and divisibility-conditioned functions re-
                                                                     All specifications are generated with DeepSeek-V4-Pro
quire valid branch parameters and nonzero branch slopes;
                                                                  using temperature 1, with reasoning disabled through
recurrence queries use bounded indices and valid recurrence
                                                                  thinking.type = disabled. For reproducibility, we
coefficients; graph instances must remain connected, con-
                                                                  release the generation prompts, rendered inputs, generated
tain no self-loops, and yield different values for the selected
                                                                  specification texts, and generation code with the benchmark.
query; definite integrals require valid ordered bounds; and
matrix instances are retained only when their entries and de-     Pure natural language prompt.
terminant outputs remain bounded and easily representable.           Write a pure natural-language definition of the
For every family, we additionally require that the two candi-        {content_type} below. Do not use mathematical no-
date mappings differ on at least one valid query. The complete       tation, symbolic formulas, programming terminology, bul-
family-specific metadata schemas, sampling ranges, and gen-          let points, or variable assignments. Define the function be-
eration constraints are released with the benchmark.                 havior only; do not explain how standard mathematical op-
   For each retained conflict pair, we generate a discrimina-        erations are computed. Do not include introductory meta-
tive query q ⋆ such that                                             commentary such as ‘Here is a description’.

                        f1 (q ⋆ ) ̸= f2 (q ⋆ ).                      {content_label}:
                    ⋆                                   ⋆            {content}
The dataset stores q , the corresponding outputs f1 (q ) and
f2 (q ⋆ ), and executable implementations of both mappings. It    Formal specification prompt.
also stores up to ten input–output examples for each mapping         Write a minimal formal mathematical specification of the
where applicable; the discriminative query is excluded from          {content_type} below. Output only clean LATEX math,
these example sets. Thus, model responses can be attributed          preferably one or two displayed equations. Do not add ex-
automatically to f1 , f2 , or other by comparing the normalized      planatory prose, examples, boxes, bullet points, or repeated
   Function family                       Input / output                     Conflict construction
   Algebra
   Linear functions                      Integer → integer                  Perturb the slope, the intercept, or both.
   Quadratic functions                   Integer → integer                  Perturb the leading coefficient, the linear coefficient, or
                                                                            both; keep the constant term fixed.
   Rational functions                    Valid integer input → reduced      Perturb one or both numerator coefficients; keep the
                                         fraction                           denominator fixed.
   Conditional rules
   Threshold-conditioned functions       Integer → integer                  Perturb the threshold and both branch mappings;
                                                                            optionally change the comparison operator.
   Divisibility-conditioned functions    Integer → integer                  Perturb the divisor and both branch mappings.
   Sequences and calculus
   Linear recurrence sequences           Nonnegative integer index →        Perturb a nonempty subset of the initial value,
                                         integer                            multiplicative coefficient, and additive coefficient.
   Polynomial derivative queries         Integer → integer                  Perturb exactly one polynomial coefficient.
   Polynomial integral queries           Integer interval → integer or      Perturb exactly one polynomial coefficient.
                                         reduced fraction
   Graph reasoning
   Graph degree queries                  Vertex → integer                   Add or remove exactly one edge while preserving
                                                                            connectivity.
   Shortest-path queries                 Source–target pair → integer       Add or remove exactly one edge while preserving
                                         distance                           connectivity.
   Matrix computation
   Shifted matrix determinants           Integer matrix → integer           Perturb exactly one entry of the shift matrix.

Table 2: Function families in the mathematical conflict-specification benchmark. Each family contains 50 independently gen-
erated conflict instances. All instances are filtered to preserve family-specific validity constraints and to admit at least one
discriminative query.


   restatements. Do not expand standard operators such as de-            expressions are variables, optionally preceded by negation,
   terminants, sums, binomial coefficients, derivatives, inte-           and compound expressions are formed by combining two
   grals, powers, or matrix products. Do not output a com-               subexpressions with one of the binary operators ∧, ∨, or ⊕.
   plete LATEX document: do not include documentclass,                   Boolean outputs are encoded as binary values in {0, 1}.
   usepackage, begin document, or end document.                             For each instance, the generator first samples a boolean
   {content_label}:                                                      expression with maximum recursive depth three. Variables
   {content}                                                             are sampled from A, B, C, D, with negation inserted proba-
                                                                         bilistically, and binary compositions are sampled from AND,
Naturalized formal specification prompt.                                 OR, and XOR. To include cases where syntactic grouping is
   Write     a   natural-language     description    of    the           important, a subset of expressions is generated in explicitly
   {content_type} below. You may use mathemati-                          bracketed three-variable forms. A conflicting counterpart is
   cal notation when it makes the computation clearer; it does           then constructed by applying one of three perturbation types.
   not need to be pure natural language. Keep the description            In an operator flip, one binary operator is replaced by a
   close to the given specification; do not simplify, expand,            different binary operator. In a negation flip, a negation is ei-
   rearrange, or decompose expressions into step-by-step                 ther inserted into or removed from a selected subexpression.
   computation. Do not include examples.
                                                                         In a grouping shift, the parenthesization of a three-variable
   {content_label}:                                                      expression is changed. For example, from (a ◦1 b) ◦2 c to
   {content}                                                             a ◦1 (b ◦2 c), with distinct operators used so that the regroup-
                                                                         ing can alter the induced Boolean function.
     Boolean Algebra Dataset Construction                                   After constructing a candidate pair, the generator exhaus-
                                                                         tively evaluates both specifications on all possible truth as-
The boolean algebra dataset is designed to study how lan-                signments. Pairs that are semantically equivalent are rejected.
guage models resolve conflicts other than only mathemati-                For each accepted pair, one distinguishing input x∗ is selected
cal functions or natural languages. Each instance consists of            such that
two boolean specifications, denoted as spec1 and spec2,
                                                                                                 f1 (x∗ ) ̸= f2 (x∗ ),
which define two distinct boolean expressions over four bi-
nary variables A, B, C, D. Each expression is represented                and the two corresponding outputs are stored as well. This
as a recursively constructed symbolic expression. Atomic                 guarantees that every data instance contains an explicit con-
  Family                  Conflict pair                                     Query                     Outputs
  Linear                  a = 9, b = −23 → a = 9, b = −27                   x = −15                   −158 vs. −162
  Quadratic               (a, b, c) = (−4, −11, −15) → (−3, −2, −15)        x = −25                   −2240 vs. −1840
  Rational                (a, b, c, d) = (3, 11, 7, 10) → (7, 14, 7, 10)    x = −6                    7/32 vs. 7/8
  Degree query            Remove edge (0, 1)                                v=0                       2 vs. 1
  Shortest path           Add edge (0, 4)                                   (1, 0)                    3 vs. 2
  Derivative              Coefficients [4, −5, 3] → [4, −5, 1]              t=7                       37 vs. 9
  Definite integral       Coefficients
                                       [1, −4,
                                             −3] → [1, −4,
                                                            −1]            [−4,
                                                                                5]                  −198 vs. −72
                                    2   −3            2  −1                   −3 −3
  Matrix determinant      Shift               →                                                       10 vs. 6
                                  −1     0           −1  0                    3    2

Table 3: Representative conflict instances. Each row shows a base mapping and its schema-preserving alternative, together with
a query on which their executable outputs differ.


flict whose resolution determines the answer to the query.           pair then produced four counterbalanced target-model trials,
   Each boolean specification is rendered deterministically          for a total of 67 × 4 = 268 trials per model.
into multiple representation types. The formula representa-             The complete pipeline was:
tion gives a LaTeX Boolean formula using standard logical
                                                                     1. sample MBPP source records deterministically;
symbols. The truth-table representation enumerates all in-
put assignments together with the corresponding values. The          2. construct an original-grounded specification A and a min-
gate-netlist representation expresses the same computation as           imally changed counterfactual specification B;
a sequence of logic gates, using intermediate gate variables         3. apply host-side structural checks and an independent
and a final output assignment. Unlike the natural-language              model-evaluator call;
specifications used in some other domains, the boolean rep-          4. repair or restart rejected candidates, with at most three
resentations are generated directly from the symbolic expres-           semantic generation attempts per source task;
sion and do not require a language-model rewriting step.
   The final boolean algebra dataset contains 100 conflict           5. generate reference implementations for A and B, gener-
instances. The realized dataset includes 32 operator-flip con-          ate shared test inputs, and derive all expected outputs by
flicts, 33 negation-flip conflicts, and 35 grouping-shift con-          executing the reference implementations;
flicts. Each instance has a unique first specification, a dis-       6. retain only pairs that pass the complete deterministic
tinguishing input, both conflicting outputs, and deterministic          cross-suite verification matrix; and
renderings of both specifications in the supported represen-         7. cross source assignment with presentation order, query
tation formats.                                                         each target model once per trial, and attribute the returned
                                                                        implementation by hidden execution.
    Code-Generation Conflict Construction
                                                                     Every intermediate prompt is versioned. Dataset hashes,
This appendix describes the code-generation experiment               prompt versions, sampling settings, model identifiers, test
summarized in Section Heterogeneous Specification Con-               counts, and execution settings are included in configuration
flicts and Figure 6. It instantiates the same measurement            fingerprints so that incompatible artifacts are not silently
principle as the mathematical benchmark in a software set-           reused.
ting: two sources specify incompatible executable mappings,
a target model must produce one implementation, and the              Constructing a one-slot semantic conflict
implementation is attributed by executing it against indepen-
dently constructed oracles. Here the competing source types          For a sampled record, the original MBPP prompt, reference
are a natural-language requirements document and a finite            code, and tests jointly ground specification A. DeepSeek-V4-
set of visible unit tests.                                           Pro receives exactly this one record and proposes a specifica-
                                                                     tion B. The generator is not asked merely to paraphrase the
End-to-end construction pipeline                                     task or to invent arbitrary failing tests. It must identify one
                                                                     named semantic slot and change only the value of that slot.
The canonical source is the sanitized MBPP file, which con-
                                                                     Examples include strict versus inclusive thresholding, zero-
tains 427 Python tasks. Each record provides a task identifier,
                                                                     versus one-based indexing, first- versus last-occurrence re-
a natural-language prompt, a reference implementation, and
                                                                     tention, case-sensitive versus case-insensitive matching, and
public tests (with setup and challenge-test fields where avail-
                                                                     first- versus last-item tie breaking.
able). For the reported experiment, we sampled 200 source
tasks without replacement using a local pseudo-random gen-              The generation contract enforces the following design re-
erator with seed 42. The unit of sampling was an MBPP task,          quirements.
rather than a successfully generated pair: a rejected task was        • A must preserve the MBPP behavior and B must be the
not replaced by another draw. After semantic and execution-             smallest plausible counterfactual within the same task
based filtering, 67 tasks yielded verified conflict pairs. Each         family.
 • Both sides must use the same function name and exact              are equivalent, the conflict is not observable, or the declared
   Python signature. If the MBPP name reveals the disputed           cases are semantic no-ops. In that case, the previous B, se-
   rule, only the name is replaced by a neutral one on both          mantic slot, and both inputs are discarded; only the source
   sides.                                                            grounding and A are retained. The generator must propose
 • Input types and domain, output type and structure, order-         a genuinely new slot and two new inputs, rather than editing
   ing and duplicate behavior, mutation policy, error behav-         the claimed outputs. A source task is abandoned after three
   ior, and all non-disputed constraints must be shared.             malformed or rejected semantic candidates, or immediately
 • The two documentation strings must be parallel in length,         after an unsuitable response.
   detail, specificity, and modal strength. Neither side may
   include an extra example, edge case, or implementation            Executable oracles and pair verification
   hint.
 • The candidate must declare exactly two distinct, valid            An accepted semantic description is not yet an experimental
   positional input arrays. On each input, the independently         item. The pipeline next constructs executable oracles in two
   traced outputs must satisfy A(x) ̸= B(x).                         stages. First, DeepSeek-V4-Pro generates independent refer-
                                                                     ence implementations for A and B. This prompt requests
 • Tasks requiring files, network access, randomness, time,          code only and withholds test-generation duties. A reference
   external packages, unstable iteration order, uncontrolled         implementation must use the exact shared signature, imple-
   floating-point behavior, or subjective judgment are ex-           ment a general rule rather than hard-code the declared ex-
   cluded.                                                           amples, and reproduce its side of both discriminating cases.
The generator can instead return unsuitable when no                  Host-side AST validation restricts code to a small allowlist of
honest one-slot counterfactual exists. This option is impor-         standard-library functionality and rejects dynamic execution,
tant because forcing every MBPP record to yield a pair would         reflection, I/O, network or subprocess access, randomness,
favor artificial or multi-factor conflicts.                          and other unsafe or nondeterministic behavior.
   All construction roles used separate calls to                        Second, after both implementations pass their declared
deepseek-ai/DeepSeek-V4-Pro through Together.                        cases, the model proposes inputs only. Declared discriminat-
Thus, “separate evaluator” below means an independent call           ing case 0 is automatically placed in the visible set and case
and prompt role, not a different model family. For the artifact      1 in the hidden set. The model supplies two additional visi-
used in the reported experiment, construction calls used             ble inputs and five additional hidden inputs, producing three
temperature 0.1, seed 42, a maximum of 4,086 completion              visible and six hidden calls. It never supplies expected values
tokens, a 120-second API timeout, and reasoning disabled.            or assertion strings. The host executes each already validated
Network retries did not consume the three semantic attempts.         reference implementation on the shared inputs and uses the
                                                                     observed return values to form paired assertions for A and
Semantic validation and repair                                       B. Consequently, the expected outputs used for acceptance
Validation first checks facts that do not require model judg-        and later attribution are execution-derived, not copied from
ment. The returned object must have the exact schema; its            an LLM response.
copied prompt, source code, tests, and task identifier must             The host then enforces the following invariants:
match the selected MBPP record; its signature must parse as
one synchronous function definition with the declared name;           • all tests have the literal-only form                 assert
and each discriminating input must be a JSON array with an              function(literals) == literal;
arity compatible with the signature. The two inputs must be
distinct, and neither declared case may have equal A and B            • A and B suites use identical calls in identical order, while
outputs.                                                                visible and hidden calls are disjoint and contain no dupli-
   A second DeepSeek-V4-Pro call then evaluates the candi-              cates;
date on five dimensions, each scored from 1 to 5: same task           • at least one call in each visibility split distinguishes the
family, exactly-one-slot conflict, information balance, deter-          two specifications;
ministic testability, and clarity. The evaluator is instructed to
recompute both declared outputs, ask whether a single im-             • executions occur in fresh isolated python -I -S sub-
plementation could satisfy both documents, check that the               processes and temporary working directories, with a two-
function name is neutral, and reject any hidden second dif-             second timeout; and
ference. Acceptance requires a total score of at least 22, a          • every cell is stable across two fresh repetitions.
score of 5 for the single-slot criterion, and scores of at least 4
on every other dimension. These thresholds are rechecked by          Finally, all eight cells of the solution-by-suite matrix must
the host even if the evaluator’s textual verdict is inconsistent     have the expected outcome: Both solutions must also re-
with its scores.                                                     produce every declared discriminating output. Instability, a
   Rejected candidates follow one of two repair paths. A nor-        timeout, a safety violation, a cross-suite pass, or failure on a
mal repair returns the previous candidate and the complete           same-side suite invalidates the pair. Oracle diagnostics can
evaluator diagnostics to the generator, preserving valid con-        trigger targeted solution or input repair, but the accepted se-
tent while repairing local balance, clarity, schema, or output-      mantic candidate is immutable at this stage. Each oracle stage
tracing errors. A semantic restart is used when the rules            is limited to three rounds.
                          Table 4: Execution outcomes under the four counterbalanced configurations.

                                           Visible A              Hidden A          Visible B            Hidden B
             Reference solution A            Pass                 Pass          Assertion failure     Assertion failure
             Reference solution B      Assertion failure    Assertion failure         Pass                  Pass


Counterbalanced preference trials and exact target                     • fail both hidden suites but pass the displayed visible suite:
prompt                                                                   visible-test overfitting; and
For each verified pair, we construct the two genuinely con-            • fail both hidden suites and the displayed suite, or fail
flicting source assignments                                              extraction, safety, or execution: other/failure.
                                                                      An A or B attribution is finally mapped to documentation or
     (doc(A), tests(B))      and   (doc(B), tests(A)).
                                                                      tests using that trial’s source assignment. Thus the label does
Each assignment is rendered once with documentation first             not assume that A is always the documentation-supported
and once with tests first. This 2 × 2 crossing swaps both the         behavior. The test-preference rate in Figure 6 is
behavioral assignment and the presentation order, yielding                                       Ntests
four trials per pair. No condition labels, spec_A/spec_B                                                        ,
identifiers, reference implementations, or hidden tests are                             Ntests + Ndocumentation
exposed to the target model.                                          so both-compatible, visible-test-overfit, wrong-behavior, ex-
   Apart from substituting the documentation, the three visi-         traction, and execution outcomes are excluded from this con-
ble assertions, the shared signature, and the order of the two        ditional preference denominator but remain available in the
conflicting blocks, the target prompt is exactly: There are           released raw result records. Confidence intervals are obtained
deliberately no labels such as “authoritative documentation”          from 10,000 bootstrap resamples clustered by conflict-pair
or “tests take precedence.” The signature inside the answer           identifier, keeping all four counterbalanced trials from a sam-
scaffold is shared by both specifications and therefore does          pled pair together. The results are shown in Table 6.
not favor either behavior.
                                                                                       Clinical Rule Conflict
Target models and reasoning settings                                  This appendix describes the construction of the clinical rule
Each target model receives all 268 trials, with one comple-           conflict experiment summarized in Section Clinical Rule
tion request per trial. Table 5 lists the 12 models included in       Conflicts, and reports the cross-authority analysis and ro-
Figure 6. “No explicit effort” means that the request omitted         bustness checks that are not carried in the main text.
a provider-specific reasoning-effort field and used the end-
point default; it does not mean that the model performed no           Dataset construction
internal reasoning. Conversely, high and max are API-level            The conflict material is derived from public-domain drug
inference-budget controls, not a request to reveal a chain of         labelling retrieved through the openFDA drug label API.
thought. Kimi-K3 exposed max, rather than high, as its                For a candidate label, a language model proposes a dosing
supported mandatory-reasoning setting.                                or indication threshold together with a verbatim supporting
   A GPT-OSS-120B result directory is retained with the               quote; the proposal carries no authority of its own and is ac-
released experimental artifacts, but that model is not part of        cepted only if it passes a deterministic gate. The gate requires
the 12-model Figure 6 analysis and is not included in the             that the quoted span contain the metric, the numeric value,
reported correlation with model capability.                           and an explicit below-relation, and rejects dose-adjustment
                                                                      bands, wrong-direction statements, fragments of dosing ta-
Implementation extraction, attribution, and                           bles, and “not studied” prose. Its rejection rules were ex-
aggregation                                                           tended over three rounds in which sampled acceptances were
The evaluator first extracts the text between the requested im-       re-examined against the source text and each observed fail-
plementation tags (with conservative fallbacks for otherwise          ure mode was turned into an additional rule. Roughly 17%
valid Python), then checks that the code defines the required         of candidate labels survive the gate. Accepted thresholds
function with the exact signature and passes the same static          cover two clinical decision fields, renal dosing thresholds
safety policy used for the reference implementations. The             and pediatric minimum-age indications, yielding 166 con-
extracted implementation is run separately against visible A,         flict instances. Every accepted instance retains its quote and
hidden A, visible B, and hidden B suites. Hidden tests are            source identifier, so any threshold can be checked against the
used for the primary behavioral attribution:                          label it came from.
                                                                         Each instance pairs the genuine threshold with a schema-
 • pass hidden A and fail hidden B: follows A;
                                                                      preserving perturbation of its value, following the procedure
 • pass hidden B and fail hidden A: follows B;                        used to construct f2 in the mathematical benchmark, and a
 • pass both hidden suites: compatible with both on the or-           query is placed strictly between the two values so that the
   acle inputs;                                                       rules give opposite answers. The perturbation is applied in
Given the following information:
{documentation and visible tests, in the assigned order}

output the implementation code as a function.

Return your final answer in exactly this format:
<implementation_code>

{shared function signature}

</implementation_code>


                                   Figure 8: Prompt template for code-generation experiments.

Table 5: Target models and request settings for the Figure 8 result snapshot. All requests allowed at most 4,086 completion
tokens and used a 120-second API timeout. “Default” denotes no explicit reasoning-effort parameter.

        Model                         Endpoint model identifier          Reasoning effort    Sampling fields
        Claude Opus 4.8               anthropic/claude-opus-4.8          high                temperature and seed omitted
                                      (OpenRouter)
        DeepSeek-V4-Flash             deepseek/deepseek-v4-flash         default             temperature 0.1; seed 42
                                      (OpenRouter)
        DeepSeek-V4-Pro               deepseek/deepseek-v4-pro           default             temperature 0.1; seed 42
                                      (OpenRouter)
        Gemma-3-4B-IT                 google/gemma-3-4b-it (Open-        default             temperature 0.1; seed 42
                                      Router)
        GPT-4.1-nano                  gpt-4.1-nano (OpenAI)              default             temperature 0.1; seed 42
        GPT-5-nano                    gpt-5-nano (OpenAI)                default             temperature omitted; seed 42
        GPT-5.4-nano                  gpt-5.4-nano (OpenAI)              high                temperature omitted; seed 42
        GPT-5.6-Luna                  gpt-5.6-luna (OpenAI)              high                temperature omitted; seed 42
        GPT-5.6-Terra                 gpt-5.6-terra (OpenAI)             high                temperature omitted; seed 42
        Kimi-K3                       moonshotai/kimi-k3        (Open-   max                 temperature and seed omitted
                                      Router)
        Llama-3.3-70B-Instruct        meta-llama/llama-3.3-              default             temperature 0.1; seed 42
                                      70b-instruct (OpenRouter)
        Llama-4-Scout                 meta-llama/llama-4-scout           default             temperature 0.1; seed 42
                                      (OpenRouter)


both directions: the genuine label value is the more restrictive   Trials, models, and attribution
of the two competing rules in roughly half of the instances
and the more permissive one in the other half. This is what        Each conflict is evaluated on all six unordered representa-
allows a preference for restrictiveness to be distinguished        tion pairs, under both authority framings (“Source 1/2” ver-
from a preference for correctness in Section Clinical Rule         sus “Clinical guideline”/“Product label”), and under a com-
Conflicts; were the perturbation always to loosen the genuine      plete 2 × 2 symmetry: presentation order is reversed, and
threshold, “adopts the stricter rule” and “adopts the genuine      the assignment of representation type to underlying rule is
rule” would denote the same event.                                 swapped. Order and rule-identity effects therefore cancel in
   Each of the two rules is then rendered in all four repre-       the aggregate. The full design is 166 × 6 × 2 × 2 × 2 = 7,968
sentation types of the main study. Table 7 shows a complete        trials per model.
instance. The genuine label value is 12 years and the per-            The nine evaluated models span five families: Doubao
turbation is 17 years, so here the perturbed rule is the more      Seed 2.0 Lite and Pro, GPT-4.1-nano, GPT-5-nano, GPT-
restrictive one; the query at age 14 separates them.               5.4-nano, DeepSeek-V4-Flash and V4-Pro, Llama-3.3-70B,
   The example sets exclude the queried value, so the ex-          and Llama-4-Scout. We report only effects that hold in the
amples never state the answer outright and the model must          same direction for all nine.
recover the underlying threshold from the demonstrations.             Running the complete design on every model is prohibitive
All four renderings of a rule express identical semantics;         for verbose reasoners, so coverage is uneven and is stated
only the surface form differs. This is also the most plausi-       wherever results are reported. Doubao Seed 2.0 Lite was run
ble reason for the weakness of examples reported in Section        on the complete design; six models were run on a fixed 1,500-
Clinical Rule Conflicts: clinical rules involve compound con-      trial subsample (seed 42); DeepSeek-V4-Pro on a 700-trial
ditions, multiple thresholds, and exceptions, which a finite       subset nested inside that subsample; and Doubao Seed 2.0
set of demonstrations covers poorly.                               Pro on an earlier 2,147-trial sample that overlaps the com-
Table 6: Code-generation outcomes by target model. Documentation and Tests are conditional percentages among trials attributed
to exactly one of the two conflicting specifications. Overfit and Failure are percentages of all 268 trials per model. Overfit denotes
an implementation that passes the displayed visible-test suite but fails both hidden suites; Failure denotes an extraction, safety,
runtime, or API hard failure. GPT-OSS-120B is excluded to match the 12-model analysis.

                                 Model                        Documentation         Tests   Overfit   Failure
                                 Claude Opus 4.8                      2.9%         97.1%     5.6%      2.6%
                                 DeepSeek-V4-Flash                  42.4%          57.6%     3.0%      5.2%
                                 DeepSeek-V4-Pro                    21.6%          78.4%     1.5%      8.6%
                                 Gemma-3-4B-IT                      83.5%          16.5%     2.6%      1.9%
                                 GPT-4.1-nano                       82.6%          17.4%     1.5%      5.6%
                                 GPT-5-nano                         14.3%          85.7%     4.5%      8.6%
                                 GPT-5.4-nano                       32.1%          67.9%     6.0%      3.7%
                                 GPT-5.6-Luna                       25.7%          74.3%     5.2%      1.9%
                                 GPT-5.6-Terra                      30.7%          69.3%     3.0%      1.1%
                                 Kimi-K3                              6.0%         94.0%     2.6%     15.7%
                                 Llama-3.3-70B-Instruct             65.3%          34.7%     1.5%      4.5%
                                 Llama-4-Scout                      71.8%          28.2%     1.1%     18.3%

Table 7: One complete conflict instance (acetazolamide extended-release, pediatric minimum age). Query: “For a 14-year-old
patient, is use of the medicine indicated? Answer yes or no.” The left column is the genuine labelled threshold, the right column
its perturbation; each row is one representation type. A trial presents one cell from each column.

                  Genuine rule (threshold 12; answers yes)                          Perturbed rule (threshold 17; answers no)
                           (                                                                 (
                            indicated         a ≥ 12                                           indicated        a ≥ 17
Formal            use(a) =                                                          use(a) =
                            not established a < 12                                             not established a < 17

Naturalized       Use is indicated for patients aged ≥ 12 years, and not es-        Use is indicated for patients aged ≥ 17 years, and not es-
formal            tablished for patients aged < 12 years.                           tablished for patients aged < 17 years.
Pure    natural   The medicine is indicated for patients who are at least twelve    The medicine is indicated for patients who are at least sev-
language          years old; for children younger than that, its use is not es-     enteen years old; for children younger than that, its use is
                  tablished.                                                        not established.
Input–output      age 16 years → indicated; age 8 years → not established;          age 21 years → indicated; age 13 years → not established;
examples          age 22 years → indicated.                                         age 27 years → indicated.


mon subsample only partially (413 trials), so it is reported               To examine conflicts between named authorities we assem-
alongside rather than as part of the matched comparison. Ev-               bled a separate set of 31 instances in which the U.S. FDA
ery model has the full 372 cross-authority trials. All models              and the European EMA issue operationally opposite guid-
were reached through a single endpoint with identical re-                  ance for the same drug and patient. Each instance carries,
quest settings (reasoning = medium where accepted,                         for both regulators, a one-line rule, a verbatim quote, and
temperature 0.1); no API errors occurred in any run.                       a resolvable citation—DailyMed or accessdata.fda.gov for
   Because the query is positively phrased and the two rules               the FDA, and EPAR product information or SmPC from the
answer it oppositely by construction, a clean yes or no maps               EMA medicines database. Candidates were collected and
deterministically to one rule. Attribution is recomputed from              then subjected to a refutation check: for each candidate, the
the stored responses at analysis time by a parser that tolerates           claimed conflict was challenged against the cited primary
verdicts wrapped in LATEX (\text{no}, \boxed{Yes})                         documents, and a candidate was retained only if the challenge
or preceded by prose. Responses the parser cannot resolve                  failed. Two candidates did not survive and were dropped. The
are resolved by a separate adjudication pass that classifies               check screens candidates for exclusion rather than warrant-
the stated position as following one rule, the other, both, or             ing the survivors—the quotes and citations it operated on
neither. The adjudication uses a model from a family not                   are released with the dataset, so every conflict can be ver-
among those evaluated, so that no model grades itself, and                 ified directly against the labelling. Because a rule cannot
every label is released with the response it was assigned to,              be truthfully re-attributed to the other authority, assignment
so the classification can be re-derived or replaced.                       symmetry is replaced by direction balance: 17 instances are
                                                                           FDA-more-permissive and 14 EMA-more-permissive. Each
Cross-authority conflicts                                                  conflict is presented under a labeled and an anonymized
                                                                           condition, with order counterbalanced and three repetitions,
The constructed conflicts use genuine values but an                        giving 372 trials per model.
anonymised generic rule, because attaching a real agency’s
name to a perturbed rule would fabricate a regulatory claim.                  Direction balance permits the analysis in Figure 9. In ag-
                           FDA vs EMA: tracks the stricter rule, not the authority                 Robustness
         Doubao-Pro
         Doubao-Lite                                                                               Dataset screening. Before any result was computed, all 31
    DeepSeek-V4-Pro                                                                                cross-authority instances were screened against five explicit
   DeepSeek-V4-Flash                                                                               criteria: whether each quote supports the rule attributed to it,
        GPT-5.4-nano
                                                                                                   whether the query is genuinely discriminative given the two
         GPT-5-nano
                                                                                                   rules, whether the stated answer polarity follows from the
        GPT-4.1-nano
       Llama-3.3-70B
                                                                                                   rule, whether the recorded direction matches the answers,
                                                                        EMA is more permissive     and whether the claim is consistent with known labelling.
       Llama-4-Scout                                                    FDA is more permissive
                       0      20             40              60             80               100   Two of these criteria—answer polarity and direction—are
                                              P(choose FDA) (%)
                                                                                                   mechanical, and were re-derived deterministically in code;
                                                                                                   both were consistent for all 31 instances. Of the remaining
Figure 9: Cross-authority conflicts. Probability of choosing
                                                                                                   checks, 28 instances passed cleanly and 3 were flagged, none
the FDA rule, split by which authority is the more permissive
                                                                                                   of them as a fabrication. In each flagged case the two sides
one. The gap is positive for all nine models, so the near-
                                                                                                   are not a perfect like-for-like pairing: an indication-specific
balanced aggregate reflects two opposing biases rather than
                                                                                                   sub-label set against an indication-general table, a route mis-
indifference.
                                                                                                   match between an oral and a parenteral product, and one
                                                                                                   regulatory action that could not be corroborated from the
                                                                                                   cited material alone. All three are retained, and a sensitiv-
Table 8: Hedging rate (reports both positions, commits to                                          ity check recomputes the headline contrasts without them.
neither) by condition. The effect of naming the authorities is                                     Screening identifies candidates for exclusion; it does not it-
confined to particular model families.                                                             self warrant correctness. The quote and citation underlying
                                                                                                   every rule are released with the dataset, so each instance can
           Model                               Anonymized               Labeled                    be checked against the primary document independently of
           Doubao Seed 2.0 Lite                             11%                  30%               this procedure.
           Doubao Seed 2.0 Pro                               4%                  32%
           DeepSeek-V4-Flash                                 4%                  24%
                                                                                                   Prompt contamination. Two defects were found in the
           DeepSeek-V4-Pro                                  19%                  25%               mined cross-authority instances and fixed before any num-
           GPT-4.1-nano                                      0%                   3%               ber was reported. First, three queries had the answer ap-
           GPT-5-nano                                        1%                   6%               pended by the mining process (“FDA answer: NO. EMA an-
           GPT-5.4-nano                                      0%                   1%               swer: YES”), which leaks the label into the prompt, includ-
           Llama-3.3-70B                                     1%                   1%               ing in the anonymized condition. Second, seven rules and
           Llama-4-Scout                                     0%                   0%               two queries identified their own regulator through incidental
                                                                                                   wording (“SmPC section 4.3”, “FDA-approved test”), which
                                                                                                   silently de-anonymizes the source in precisely the condition
                                                                                                   designed to hide it. The encoder now strips answer state-
gregate no model prefers one regulator (FDA-selection 46%–                                         ments and emits a scrubbed parallel rendering used only in
68%), but for every model this is the average of two oppos-                                        the anonymized condition, asserting that no regulator token
ing biases: the probability of choosing the FDA rule is lower                                      survives. The pre-fix run was discarded and every reported
when the FDA rule is the more permissive one and higher                                            result comes from the post-fix re-run.
when the EMA rule is. The direction-split swing is positive                                        Heterogeneity in the magnitude of the restrictiveness
for all nine models, ranging from +10 to +37 percentage                                            preference. The direction of the restrictiveness preference
points. Restrictive selection is 55%–68%. The restrictiveness                                      reported in Section Clinical Rule Conflicts is uniform across
preference reported in Section Clinical Rule Conflicts there-                                      all nine models, but its magnitude varies substantially across
fore also holds on real, dual-cited regulatory divergences                                         instances: the two clinical fields differ by 15 to 35 percentage
containing no fabricated values.                                                                   points, and this difference has the same sign for every model.
   Naming the authorities has a markedly model-specific ef-                                        We report this heterogeneity as an observation and do not
fect. Hedging—reporting both positions without committing                                          attribute it to a cause. The two fields differ simultaneously
to either—rises sharply for some families when the regulators                                      in rule type, in the wording of the restrictive outcome (con-
are named and not at all for others (Table 8). The Doubao                                          traindicated versus not established), and in the magnitude of
and DeepSeek families hedge considerably more once the                                             the perturbation, and a design with two fields cannot separate
sources are named, whereas the GPT and Llama families are                                          these factors. Identifying what modulates the strength of the
essentially unaffected and commit under either framing. We                                         preference requires a dedicated design and is left to future
therefore report this as a property of particular models rather                                    work.
than as a general effect of authority framing.
                                                                                                   Response truncation. Verbose reasoning models initially
  This analysis measures preference between sources, not                                           exhausted their token budget before emitting a verdict on
between representations. It is a complement to the main line                                       about 10% of trials, and the loss was not uniform across
of the paper rather than evidence for it, which is why it is                                       clinical fields. The budget was raised and the affected trials
reported here.                                                                                     rerun; residual unresolved trials are now 0–2% per model
and are excluded from rates rather than imputed.                  rule induction and execution capability, rather than ambigu-
                                                                  ity in the attribution procedure or the emergence of hybrid
                   Additional Results                             behaviors.

Example Selection across Function Families                        Boolean Algebra
Figure 10 shows that example use varies substantially across      Figure 13 compares Boolean formulas with gate netlists.
mathematical function families. Examples are most com-            Unlike the strong aggregate preference observed between
petitive against pure natural-language specifications for lin-    formulas and truth tables, this comparison does not reveal
ear functions, derivative queries, and recurrence sequences,      a consistent ordering across models. GPT-4.1 and GPT-5
where several pooled selection rates approach or exceed 50%.      strongly favor the gate-netlist-supported mapping, selecting
Their influence is much weaker for graph-degree queries, ma-      the formula-supported mapping in only approximately 19%
trix computation, shortest-path problems, and several condi-      and 14% of attributable responses, respectively. In contrast,
tional and rational-function families.                            DeepSeek-V4-Pro and GPT-5.4 favor formulas, with formula
   The same family-level ordering is broadly preserved when       selection rates of approximately 67% and 73%. DeepSeek-
examples compete with formal or naturalized-formal specifi-       V4-Flash, Llama-3.3, and Llama-4 remain closer to the 50%
cations, but the selection rates shift downward across nearly     indifference point, although Llama-3.3 exhibits a modest
all families. This shows that example use is determined           preference for gate netlists. These substantial cross-model
jointly by the underlying task structure and the representation   differences suggest that formulas and gate netlists occupy
of the competing specification. Examples become competi-          a more comparable level of representational strength: both
tive when finite demonstrations expose a recoverable map-         encode the Boolean function compositionally and support
ping, but they are consistently disadvantaged when the alter-     direct evaluation, leaving the preferred representation more
native presents the rule through explicit mathematical struc-     dependent on model-specific training or processing biases.
ture.                                                                Figure 14 shows a markedly different pattern when gate
                                                                  netlists are compared with truth tables. All DeepSeek and
Presentation-Order Effects                                        GPT models select the gate-netlist-supported mapping in
                                                                  more than 95% of attributable responses, with confidence
Figure 11 shows that presentation order has a measurable but      intervals well above the 50% indifference point. This indi-
generally secondary effect. For five of the six representation    cates a highly consistent preference for the gate-netlist rep-
comparisons, the pooled probability of selecting the second-      resentation over the truth table among these models. The
presented specification remains relatively close to 50%, and      two Llama models are exceptions, producing estimates close
these order effects are small compared with the correspond-       to chance with confidence intervals overlapping 50%, and
ing representation preferences.                                   therefore show no reliable preference between the two rep-
   The formal versus naturalized-formal comparison is the         resentations.
clear exception. These two representations have similar over-        Taken together, the two comparisons refine the broader or-
all selection strength, with neither exerting the large rep-      dering among Boolean representations. Gate netlists consis-
resentation advantage observed in comparisons involving           tently dominate truth tables for most evaluated models, but
pure natural language or examples. Consequently, when the         their relationship with formulas is model-dependent rather
representation-level preference is weak, secondary decision       than universal. One plausible interpretation is that both for-
factors become more influential, and the second-position          mulas and gate netlists provide compact, intensional descrip-
preference is amplified. This result suggests that presentation   tions of the underlying Boolean function, whereas truth tables
order plays the largest role when the competing specifications    present the function extensionally as a collection of input-
are otherwise similarly preferred.                                output assignments. The observed preference for gate netlists
                                                                  over truth tables may therefore reflect sensitivity to com-
Non-attributable Responses                                        positional structure, compactness, or ease of query-specific
                                                                  evaluation, rather than a general preference for any particular
Figure 12 shows that responses assigned to other are un-          surface syntax. However, because these properties are not in-
common in most representation comparisons. For formal,            dependently controlled in the present experiment, this inter-
naturalized-formal, and their comparisons with examples,          pretation should be treated as suggestive rather than causal.
the rate is generally below 5%, indicating that model outputs        These results further demonstrate that representational
can usually be attributed cleanly to one of the two executable    preference is not fully captured by a single global hierarchy:
mappings.                                                         robust ordering emerges between some representation pairs,
   The main exception is the pure-natural-language versus         while semantically equivalent structural representations can
examples condition, particularly for GPT-4.1-nano and the         produce pronounced model-specific reversals.
Llama-family models. Manual inspection of these responses
shows that they do not combine the two competing map-
pings. Instead, the model typically fails to infer the underly-       Abstention-Enabled Conflict Resolution
ing mapping from the finite input–output examples or applies      To examine whether models always resolve conflicting spec-
the inferred rule incorrectly to the discriminative query. The    ifications by committing to one of the competing sources, we
elevated other rate therefore reflects limited example-based      conduct an additional abstention-enabled experiment. We use
                                      Ex vs. NL                                                          Ex vs. Form                                Ex vs. NatF
         Linear

         Deriv.

       Recurr.

         Quad.

      Integral

     Rational

  Threshold

         Divis.

      Shortest

        Matrix

       Degree

               0%         25%           50%                    75%              100% 0%            25%      50%        75%    100% 0%       25%        50%        75%   100%

                                                                                 Example-supported mapping selected (%)


Figure 10: Example selection by function family across all three example-based comparisons. Light points show model-specific
estimates, and dark points show pooled estimates across models. Each estimate is the proportion of attributable responses
selecting the example-supported mapping. Error bars show conflict-instance clustered-bootstrap 95% confidence intervals.


   NL vs Ex
                                                                                                                  Thus, the model receives exactly the same conflicting spec-
 Form vs Ex
                                                                                                               ifications and query, but is additionally given an explicit op-
  NatF vs Ex
                                                                                                               tion to abstain from selecting either candidate behavior.
 NL vs Form                                                                                                       We evaluate DeepSeek-V4-Pro and GPT-5-nano under this
 NL vs NatF                                                                                                    setting. As in the main experiment, each model is evaluated
Form vs NatF                                                                                                   on all six representation pairs and four counterbalanced con-
                    40%         50%                      60%
                                         Second-presented source selected (%)
                                                                                70%          80%
                                                                                                               figurations for every conflict instance, resulting in 13,200
                                                                                                               trials per model. We define the abstention rate as the pro-
Figure 11: Presentation-order effects across representation                                                    portion of all trials in which the model returns the explicit
comparisons. Light gray points show model-specific esti-                                                       uncertain response:
mates, and black points show pooled estimates across mod-
                                                                                                                                                  Nuncertain
els. Each estimate is the proportion of attributable responses                                                                  P (abstain) =                 .
selecting the specification presented second. Horizontal er-                                                                                      Nall trials
ror bars show conflict-instance clustered-bootstrap 95% con-                                                      Table 9 reports abstention rates for each representation
fidence intervals for the pooled estimates, and the dashed line                                                pair. DeepSeek-V4-Pro abstains in approximately 6% of tri-
marks 50%.                                                                                                     als overall, with relatively moderate variation across condi-
                                                                                                               tions. GPT-5-nano exhibits a higher overall abstention rate
                                                                                                               of approximately 17%, but this behavior varies substantially
the same conflict instances, representation pairs, counterbal-                                                 across competing source types. In particular, GPT-5-nano
anced configurations, and evaluation setup as in the main                                                      abstains frequently when both sources are textual or formal-
mathematical experiments.                                                                                      ized representations, whereas abstention remains uncommon
   The only modification is to the final instruction in the                                                    in conditions involving input–output examples.
prompt. In the main experiment, the prompt ends with:                                                             These results indicate that explicit abstention can consti-
                                                                                                               tute an additional strategy for handling conflicting specifica-
      Compute the value: [query]. Please                                                                       tions rather than committing to either competing source. Im-
      give your final answer in the form                                                                       portantly, abstention does not appear to behave as a uniform
      \boxed{...}.                                                                                             model-level tendency. For GPT-5-nano, it varies sharply with
 For the abstention-enabled experiment, we minimally                                                           the types of specifications in conflict, whereas DeepSeek-
modify this instruction to:                                                                                    V4-Pro exhibits a more moderate pattern. This suggests that
                                                                                                               abstention may capture a distinct dimension of conflict-
      Compute the value: [query]. Please                                                                       handling behavior that is not reducible to source selection
      give your final answer in the form                                                                       alone.
      \boxed{...}, or answer "uncertain".
  DS-Flash                  2.6                               0.3                         0.5           0.2                            0.3                            0.2
                                                                                                                                                                                            14

    DS-Pro                  3.4                               0.5                         1.1           0.3                            0.7                            0.3                   12


   GPT-4.1                  12.0                              3.6                         3.8           2.8                            2.2                            2.2                   10




                                                                                                                                                                                                 Other (%)
                                                                                                                                                                                            8
   GPT-5.4                  1.2                               0.4                         0.5           1.1                            1.5                            0.8
                                                                                                                                                                                            6
     GPT-5                  2.1                               0.4                         0.5           0.2                            0.3                            1.9
                                                                                                                                                                                            4

  Llama-3.3                 14.5                              7.3                         5.9           4.8                            5.4                            4.2
                                                                                                                                                                                            2

   Llama-4                  11.7                              5.3                         4.3           3.7                            3.2                            2.5                   0


                                       x                              x                       x               orm                          atF                               atF
                                vs E                       mv
                                                                    sE
                                                                                          Fv
                                                                                            sE
                                                                                                        vs F                           vs N                             vs N
                           NL                           For                         Nat            NL                             NL                                m
                                                                                                                                                                For


Figure 12: Rates of responses assigned to other across models and representation comparisons. Each cell reports the percentage
of all trials whose normalized final answer matches neither executable candidate output. Non-attributable responses are generally
rare and are concentrated in the pure-natural-language versus examples condition.



                                                Form vs Gate
         DS-Flash
          DS-Pro
         GPT-4.1
              GPT-5
         GPT-5.4
        Llama-3.3
         Llama-4
                      0%               20%           40%                  60%       80%
                                             Formula selected (%)
                                                                                                                                                       Gate vs TT
                                                                                                               DS-Flash
Figure 13: Results on the Boolean Algebra dataset, show-                                                         DS-Pro

ing model preferences between Boolean formulas and gate                                                         GPT-4.1

netlists. Points indicate the proportion of attributable re-                                                        GPT-5
                                                                                                                GPT-5.4
sponses selecting the formula-supported mapping, with
                                                                                                               Llama-3.3
clustered-bootstrap 95% confidence intervals over conflict
                                                                                                                Llama-4
instances.
                                                                                                                            40%   50%        60%         70%        80%        90%   100%
                                                                                                                                                 Gate netlist selected (%)



                                                                                                  Figure 14: Results on the Boolean Algebra dataset, show-
   Conflict Pair                             DeepSeek-V4-Pro                    GPT-5-nano        ing model preferences between gate netlists and truth tables.
   Pure NL vs. Formal                                1.59%                       15.06%           Points indicate the proportion of attributable responses se-
   Pure NL vs. Examples                              6.91%                        1.59%           lecting the gate-netlist-supported mapping, with clustered-
   Formal vs. Examples                               9.41%                        1.05%           bootstrap 95% confidence intervals over conflict instances.
   NatF vs. Examples                                 4.64%                        0.82%
   Pure NL vs. NatF                                  3.14%                       21.92%
   Formal vs. NatF                                  10.00%                       64.18%
   Overall                                           5.95%                       17.45%

Table 9: Abstention rates when models are explicitly allowed
to answer uncertain. Rates are computed over all trials in
each representation pair.
