                                               EquivSVA: A Formally Verified Dataset of Behavioral
                                                Assertions Across Equivalent RTL Implementations
                                                                                               FNU Aditi


                                         Abstract                                                            benchmark suites for formal-verification tasks [8, 12], and
                                                                                                             datasets for training assertion-generation models [10, 16].
                                         Large language models are increasingly used to generate
                                         SystemVerilog Assertions from natural-language specifica-           A recurring challenge is that RTL admits many implemen-
                                         tions and register-transfer-level designs. Existing datasets        tations of the same behavior. State encodings, conditional
                                         and benchmarks support important goals such as large-               structure, helper expressions, combinational factorization,
arXiv:2609.26751v1 [cs.LG] 22 Sep 2026




                                         scale training, formal evaluation, specification-to-assertion       and update style can all change while the external be-
                                         generation, and mutation-based testing. A complemen-                havior remains unchanged. A model that generates a
                                         tary need is to study whether a generated assertion cap-            correct assertion for one implementation may therefore
                                         tures externally observable behavior or depends on inci-            behave differently when presented with another semanti-
                                         dental details of one RTL implementation. We present                cally equivalent implementation. Prior work has examined
                                         EquivSVA, a formally verified dataset organized around              this issue through semantics-preserving RTL transforma-
                                         behavior families. Each family contains four structurally           tions [2]. That study motivates a reusable dataset in
                                         distinct RTL implementations of the same externally ob-             which behavioral equivalence is not an auxiliary pertur-
                                         servable behavior, shared interface-level gold properties,          bation applied after dataset construction, but a first-class
                                         three controlled mutants, and formal-validation evidence.           organizing principle.
                                         EquivSVA contains 120 behavior families across 12 cat-              We introduce EquivSVA, a dataset whose basic unit is
                                         egories, 480 reference RTL implementations, 914 gold                a behavior family. Each family begins from a machine-
                                         properties, and 360 mutants. Every final family passes              readable behavioral specification and contains four struc-
                                         a fixed 17-job validation suite covering RTL equivalence,           turally distinct reference RTL implementations intended
                                         gold-property proofs, property reachability, mutant dis-            to realize the same externally observable behavior. The
                                         tinguishability, and gold-property checks on mutants. We            family also includes shared interface-level gold proper-
                                         also provide fixed family-safe train, development, and              ties, three controlled behavior-changing mutants, and
                                         test splits. As a small demonstration of the analyses en-           formal evidence used to validate the final artifacts. This
                                         abled by the dataset, we evaluate the publicly released,            organization makes it possible to ask whether an assertion-
                                         Apache-2.0-licensed Qwen2.5-Coder-7B-Instruct model on              generation method responds consistently to different im-
                                         the held-out test split. Of 293 interface-only generated            plementations of the same behavior while holding the
                                         properties, 93 are formally sound, and the number of                intended semantics fixed.
                                         sound properties varies across equivalent implementations
                                         for 14 of 24 test families. These results illustrate how            The goal of EquivSVA is complementary to existing re-
                                         behavior-family organization can support controlled stud-           sources. VERT emphasizes large-scale RTL–SVA training
                                         ies of assertion-generation robustness without requiring            data [10]; FVEval organizes formal-verification tasks at
                                         changes in intended functionality. The dataset, generators,         multiple levels of abstraction [8]; AssertionBench provides
                                         validation scripts, and case-study artifacts are publicly           curated designs with formally verified assertions for model
                                         released at https://github.com/aditigupta96/EquivSVA.               evaluation [12]; CodeV-SVA develops RTL-grounded data
                                                                                                             synthesis for specialized NL-to-SVA models [16]; Veri2 or-
                                                                                                             ganizes formally filtered RTL–SVA pairs for fine-tuning [5];
                                                                                                             and AssertLLM2 provides real-world designs, structured
                                         1     Introduction                                                  specifications, golden RTL, and systematically mutated
                                         Assertion-based verification provides a concise way to              buggy RTL for realistic assertion-generation evaluation
                                         express design intent and to check temporal and safety              [15]. EquivSVA adds a behavior-family representation
                                         properties of digital hardware. In practice, writing useful         that places multiple formally equivalent RTL implemen-
                                         SystemVerilog Assertions (SVAs) requires both an under-             tations, shared gold properties, and controlled mutants
                                         standing of the intended behavior and careful attention             under one dataset unit.
                                         to clocking, reset semantics, signal relationships, and tem-        The main contributions are:
                                         poral structure. This has motivated substantial work
                                         on automatic assertion generation, including rule-based             • A public dataset of 120 behavior families across 12
                                         and learned translation from natural-language specifi-                hardware-control categories, containing 480 reference
                                         cations [3, 4], specification-driven LLM frameworks [1],              RTL implementations, 914 gold properties, and 360


                                                                                                         1
  controlled mutants.                                               fine-tuning of open-source language models [10]. FVE-
• A family-centered representation in which four struc-             val provides three formal-verification subtasks, spanning
  turally distinct RTL implementations are formally                 natural-language-to-SVA generation and assertion gen-
  checked for equivalent externally observable behavior.            eration directly from RTL, together with tool-backed
• A fixed validation protocol that checks RTL equiva-               evaluation [8]. AssertionBench contains 100 curated Ver-
  lence, gold-property correctness, property reachability,          ilog designs from OpenCores and formally verified asser-
  mutant distinguishability, and whether each mutant vi-            tions generated using GoldMine and HARM, enabling
  olates at least one property in the family gold-property          quantitative comparison of LLMs for assertion generation
  harness.                                                          [12]. CodeV-SVA uses RTL-grounded bidirectional data
• Family-safe, category-stratified train, development,              synthesis to create training data for specialized assertion-
  and test splits designed to prevent implementation                generation models [16].
  variants from the same behavior appearing across dif-
                                                                    Veri2 is a formally filtered RTL–SVA dataset that or-
  ferent splits.
                                                                    ganizes generated pairs into quality tiers and reports
• A held-out Qwen2.5-Coder-7B-Instruct case study
                                                                    2,954 modules and 18,494 assertions in its verified tier
  demonstrating syntax, formal soundness, mutation
                                                                    [5]. AssertLLM2 provides 83 real-world designs across 13
  sensitivity, and variation across equivalent RTL im-
                                                                    categories together with structured specifications, golden
  plementations.
                                                                    RTL, systematically mutated buggy RTL, and evalua-
The released artifact is available at https://github.               tion spanning syntax, formal provability, coverage, and
com/aditigupta96/EquivSVA, with the v2.0 snapshot                   mutation-based bug detection [15]. These resources ad-
at https://github.com/aditigupta96/EquivSVA/releases/               dress complementary questions about training data, re-
tag/v2.0.                                                           alistic specifications, tool-backed evaluation, and bug de-
                                                                    tection.

                                                                    A closely related motivation is robustness under semantics-
2     Related Work                                                  preserving RTL rewriting. Prior work demonstrated that
                                                                    LLM-generated assertions can change in quality when
2.1    Assertion generation from specifica-                         the same behavior is represented by transformed RTL
       tions                                                        [2]. EquivSVA turns that observation into a dataset-
Earlier work explored translating natural-language re-              level abstraction: multiple equivalent implementations
quirements into SVAs using hybrid rule-based and                    are stored directly in each family and can be reused across
machine-learning methods [3]. A later approach intro-               models, prompts, and evaluation protocols.
duced a validation loop that translated generated SVAs
back into natural-language statements and then regener-
ated assertions to assess consistency with the original spec-       3     Dataset Design
ification [4]. AssertLLM subsequently studied complete
specification documents and used multiple LLM stages                3.1    Behavior families
for structure extraction, signal mapping, and assertion
generation [1]. These works establish assertion generation          The core design decision in EquivSVA is to organize data
as a structured reasoning task spanning natural-language            around behavior rather than around isolated RTL files.
intent, hardware signals, and temporal logic.                       A family is represented conceptually as

More recent systems have expanded both the generation                              F = B, {Ri }4i=1 , P, M, E ,
                                                                                                             
                                                                                                                            (1)
methodology and the evaluation setting. SANGAM uses
multi-stage specification processing and Monte Carlo tree           where B is a machine-readable behavior specification, Ri
self-refinement for SVA generation [6]; Spec2Assertion tar-         are four reference RTL implementations, P is the shared
gets pre-RTL assertion generation with progressive regu-            set of gold behavioral properties, M is a set of three
larization [14]; and AssertGen connects specification-level         controlled mutants, and E is formal-validation evidence.
verification objectives to RTL signals before producing
assertions [9]. These approaches focus on improving the             The four reference implementations are intentionally differ-
generation process itself, whereas EquivSVA focuses on              ent in structure. Depending on the family type, variation
a reusable data representation for controlled evaluation            includes state encoding, case versus nested conditional
across implementation variants.                                     control, factorized flag logic, sequential versus ternary
                                                                    updates, and function-based update expressions. The
2.2    Datasets and benchmarks                                      intended external behavior is held constant. Gold proper-
                                                                    ties are defined over module-interface signals rather than
VERT constructs augmented RTL–SVA training exam-                    implementation-specific internal state so that the same
ples from open-source HDL and is designed to support                behavioral specification can be applied across variants.


                                                                2
Table 1: Representative related datasets and benchmarks, described by how their examples are organized and what
they are designed to support. The table emphasizes complementary design goals rather than ranking the resources.
Work             Primary purpose                   How examples are organized              Tool-backed / formal role
VERT [10]      Training data for RTL-to-           Augmented open-source RTL–SVA Evaluates generated assertions and
               SVA generation                      training pairs                   downstream fine-tuned models
FVEval [8]     Benchmarking LLM capabili-          Task instances for NL2SVA-Human, Jasper-based evaluation framework
               ties in hardware formal verifi-     NL2SVA-Machine, and Design2SVA
               cation
AssertionBench Quantitative comparison of          100 curated Verilog designs with for- Formal verification is used to establish
[12]           LLM assertion generation            mally verified assertion sets           benchmark assertions
CodeV-SVA      Training specialized NL-to-         RTL-grounded synthetic NL–SVA Uses semantic filtering and benchmark
[16]           SVA models                          training pairs produced by bidirec- evaluation
                                                   tional synthesis
Veri2 [5]        Formally filtered RTL–SVA         RTL–SVA pairs organized into All, Syn- JasperGold filtering of syntax and for-
                 training data                     tax Pass, and Verified tiers            mal validity
AssertLLM2       Realistic assertion-generation    Real-world designs with specifications, Syntax, proof, coverage, and mutation-
[15]             benchmark                         golden RTL, and systematically mu- based evaluation
                                                   tated buggy RTL
EquivSVA         Behavior-centered dataset for     Behavior families with 4 equiva- Dataset-wide equivalence, proof,
                 implementation-robust asser-      lent RTLs, shared gold properties, cover, and mutant checks
                 tion research                     and 3 controlled mutants


                                                            Gold prop-                                     Formal val-
         Behavior               RTL family                                         Controlled
                                                               erties                                        idation
       specification            4 structurally                                       mutants
                                                         shared, interface-                                equivalence,
          machine-            distinct reference                                    3 behavior-
                                                          level behavioral                               proof, cover, and
       readable intent        implementations                                    changing variants
                                                             assertions                                   mutant checks
                                                      Behavior family artifact


                         120 families · 480 reference RTLs · 914 gold properties · 360 mutants


Figure 1: EquivSVA construction and validation pipeline. The family abstraction keeps intended behavior fixed while
exposing multiple implementation structures and controlled behavior-changing mutants.


3.2     Behavior categories and model types                          13, with a mean of 7.62. Properties are written to
                                                                     describe externally observable functionality and avoid
The dataset contains 12 categories chosen to cover recur-            implementation-specific internal state names. This con-
ring control and small-state behaviors: arbiter, counter,            straint is central to the family abstraction: a property
FIFO control, handshake, interrupt control, mode con-                should continue to represent the intended behavior even
troller, protocol controller, pulse/event, rate limiter, sat-        when the internal implementation changes.
urating arithmetic, sequence detector, and timer/watch-
dog. Each category contains exactly 10 families. The
final dataset includes 80 finite-state-machine families, 27          3.4      Concrete family example
register-rule families, and 13 multi-register-rule families.
                                                                     As a concrete example, timer_0007 is a three-bit count-
This category balance is deliberate. It makes category-              down timer. A load input sets the observable remaining
level comparisons straightforward and prevents the overall           value to seven; a tick decrements a nonzero count; oth-
metrics from being dominated by one frequently generated             erwise the count holds. The derived output expired
behavior class. It should not be interpreted as an estimate          is asserted exactly when remaining is zero. The fam-
of how often these structures appear in industrial RTL.              ily contains four reference implementations—canonical,
                                                                     sequential, ternary, and function-oriented update styles—
3.3     Gold properties                                              generated from the same rule-level specification. Its three
                                                                     controlled mutants respectively ignore load, ignore tick,
The dataset contains 914 gold behavioral properties. Of              and decrement without requiring tick. Thus, the family
these, 131 are invariants and 783 are next-cycle impli-              changes implementation structure while preserving one
cations. Family-level property counts range from 5 to                intended interface behavior, and changes behavior only


                                                                 3
in the explicitly labeled mutant artifacts.                         4.3    Diversity audit
Two representative gold properties for this family illustrate       The final corpus contains no exact normalized behavioral
the property forms used in the corpus. The first is a               clones according to the released diversity audit. The
next-cycle implication associated with the load rule; the           audit also identifies a small number of parameter- or
second is an invariant relating the derived output to the           shape-similar groups, which are retained because they
observable count:                                                   remain distinct behavior families. Template metadata is
property p_load;                                                    diverse across categories, with one repeated FIFO meta-
  @(posedge clk) disable iff (rst)                                  data template. We therefore describe the corpus as 120
    load |=> (remaining == 3’d7);
endproperty                                                         behavior families, rather than claiming 120 unique behav-
                                                                    ioral archetypes.
a_load: assert property (p_load);

property p_expired;
  @(posedge clk) disable iff (rst)
    expired == (remaining == 3’d0);                                 5     Formal Validation
endproperty

a_expired: assert property (p_expired);
                                                                    Formal validation is used as a quality-control layer for
                                                                    the final dataset. The released flow uses Yosys and
These examples are interface-level: neither property de-            SymbiYosys-based infrastructure [13, 17], with SMT back-
pends on a particular state encoding, helper signal, or             ends including Bitwuzla [11]. Multi-register equivalence
internal register name that differs among the four reference        checks use ABC/PDR where that flow is more reliable for
implementations. Appendix A gives one representative                the generated design class.
behavior family from each of the 12 dataset categories.             Every final family passes a fixed 17-job validation suite.
                                                                    Three jobs compare alternate reference implementations
                                                                    against the canonical implementation. Four proof jobs
4     Dataset Construction                                          exercise the family gold-property set across the four ref-
                                                                    erence implementations, and four cover jobs check the
4.1    Specification-driven generation                              associated reachability witnesses. Three jobs establish
Families are generated from explicit machine-readable               that each controlled mutant is distinguishable from the
specifications rather than by independently sampling un-            reference behavior. The final three jobs run the family
related RTL files. Three generator paths are used: finite-          gold-property harness against each mutant in bounded
state machines, single-register rule systems, and multi-            model-checking mode and require an expected assertion
register rule systems. The generator emits multiple im-             failure. A mutant therefore passes this check only when
plementation styles from the same behavior description.             at least one gold property produces a counterexample.
Because variants share the same intended semantics but              A validation job can contain multiple assertions. In partic-
differ in control structure and coding form, they can be            ular, each of the four gold-property proof jobs instantiates
used to study implementation sensitivity without chang-             one reference implementation together with the complete
ing the target behavior.                                            property set for that family. The 480 proof jobs in table 3
For FSM families, implementation styles include canonical           therefore collectively prove every one of the 914 gold prop-
case statements, one-hot state encodings, nested condi-             erties on each of the four reference implementations in
tionals, and factored flag logic. Register-rule and multi-          its family; the job count should not be interpreted as the
register-rule families use canonical, sequential, ternary,          number of individual properties. The same distinction
and function-oriented update forms. The precise coding              applies to cover jobs, which contain the family reachability
differences vary by family so that the dataset does not             witnesses.
reduce to a single text-rewrite pattern.                            The 2,040 total in table 3 summarizes the final per-family
                                                                    validation records. During dataset development, failed or
4.2    Controlled mutants                                           malformed families were repaired and then revalidated.
                                                                    Accordingly, we use the precise statement that every fi-
Each family contains three mutants designed to change               nal family passed its 17-job validation suite, rather than
behavior in a controlled way. Mutation operators de-                implying that the entire corpus was accepted in a single
pend on the family structure and include dropped tran-              uninterrupted first-pass run.
sitions, forced exits, ignored control conditions, missing
updates, altered clear or enable behavior, incorrect satu-          The formal results are relative to the encoded synchronous
ration, and similar localized semantic changes. Mutants             clock and reset semantics. Validation traces begin with
are not intended to model the full distribution of indus-           the required reset condition, after which inputs are un-
trial hardware bugs. Their purpose is to provide known              constrained according to the family harness. Equivalence
behavior-changing alternatives against which assertions             therefore means equality of the defined externally observ-
can be tested.                                                      able outputs under the shared harness assumptions.


                                                                4
Table 2: Composition of EquivSVA across the 12 behavior categories. Every family contains four reference RTL
implementations and three controlled mutants.
                            Category                         Families Reference RTLs Gold properties Mutants Props./family
                            Arbiter                                      10                            40                               103               30                        10.30
                            Counter                                      10                            40                                58               30                         5.80
                            FIFO control                                 10                            40                                63               30                         6.30
                            Handshake                                    10                            40                                74               30                         7.40
                            Interrupt control                            10                            40                                71               30                         7.10
                            Mode controller                              10                            40                                91               30                         9.10
                            Protocol controller                          10                            40                                78               30                         7.80
                            Pulse/event                                  10                            40                                70               30                         7.00
                            Rate limiter                                 10                            40                                62               30                         6.20
                            Saturating arithmetic                        10                            40                                64               30                         6.40
                            Sequence detector                            10                            40                               109               30                        10.90
                            Timer/watchdog                               10                            40                                71               30                         7.10
                            Total                                    120                            480                             914                  360                           7.62


                                                                                                                                                                                   109
                              103
                      100                                                                              91
    Gold properties




                                                                                                                          78
                                                                         74               71                                                                                                       71
                                                                                                                                    70
                                                         63                                                                                         62               64
                                              58

                       50




                        0
                               r             er                         e               t           e                    ol                                                        e            r
                              e                         FO            ak             up           od                oc            lse            te            rit
                                                                                                                                                                  h             nc            me
                          bit              nt      FI                h              r
                                                                                                               ot              Pu              Ra                              e
                                                                                                                                                                                          Ti
                       Ar               o u                       ds            ter              M
                                                                                                            Pr                                           Sa
                                                                                                                                                            tA              qu
                                    C                          n              In                                                                                          Se
                                                             Ha

Figure 2: Gold-property counts by behavior category. Category family counts are fixed at 10, so the variation reflects
the number of behavioral properties associated with each family set rather than category size.


Table 3: Formal-validation jobs associated with the final                                                   Table 4: Fixed EquivSVA v2.0 splits. Every category
dataset. Every final family passed its complete 17-job                                                      contributes 6 train, 2 development, and 2 test families.
suite.                                                                                                               Split Families RTLs Properties Mutants
Validation check                                                  Jobs/family                    Pass
                                                                                                                     Train                72          288                     544              216
RTL equivalence                                                                    3           360/360
                                                                                                                     Dev                  24           96                     178               72
Gold-property proofs                                                               4           480/480
Property reachability / cover                                                      4           480/480
                                                                                                                     Test                 24           96                     192               72
Mutant distinguishability                                                          3           360/360
Gold-property checks on mutants                                                    3           360/360
Total                                                                            17 2040/2040               the same behavior during evaluation.
                                                                                                            The split was generated deterministically. Expansion
                                                                                                            families are used for development and test, while legacy
6                     Splits and Release                                                                    pilot families are assigned to training where prior prompt
                                                                                                            or baseline work could have exposed them. This choice is
The v2.0 release provides fixed family-safe, category-                                                      conservative with respect to possible experiment leakage
stratified train, development, and test splits. All four                                                    from earlier prototype work.
RTL variants of a family remain in the same split. This
prevents a model from seeing one implementation of a                                                        The public release contains the dataset manifest, split
behavior during training and another implementation of                                                      file, generators, construction and validation scripts, task-


                                                                                                       5
export code, baseline inference code, syntax/formal/mu-
                                                                    Table 5: Held-out Qwen2.5-Coder-7B-Instruct case study
tant evaluators, and the v2 case-study result files. The
                                                                    on 24 test families (96 RTL inputs).
repository is licensed separately for code and dataset ar-
tifacts, with Apache-2.0 for source code and CC BY 4.0                  Metric                                      Result
for the dataset.                                                        Syntax-valid tasks                  68/96 (70.8%)
                                                                        Interface-only properties                     293
                                                                        Formally sound properties          93/293 (31.7%)
7    Case Study: Qwen2.5-Coder-7B                                       Tasks with ≥1 sound property        45/96 (46.9%)
                                                                        Families sound on all 4 RTLs         8/24 (33.3%)
We include a small case study to demonstrate how the                    Variant-sensitive families          14/24 (58.3%)
family structure can be used in model evaluation. The                   Detected property–mutant pairs      16/279 (5.7%)
purpose is not to provide a comprehensive model rank-                   Unique controlled mutants detected 11/72 (15.3%)
ing. We evaluate Qwen2.5-Coder-7B-Instruct [7], whose
upstream release is distributed under the Apache Li-
cense 2.0, on the untouched test split: 24 families and 96
RTL inputs. Inference uses the public 4-bit MLX check-              one sound property. At the family level, eight of 24 fami-
point mlx-community/Qwen2.5-Coder-7B-Instruct-4bit;                 lies produce at least one sound property for all four equiv-
the exact checkpoint identifier is also stored in the re-           alent implementations, while eight families produce none
leased run metadata. Decoding is greedy. The prompt                 for any implementation. The remaining eight produce
requests interface-only behavioral SVAs and prohibits               sound properties for only a subset of implementations.
implementation-specific internal signals.
Generated outputs are evaluated in stages. First, syntax            A notable family-level observation is that the number of
is checked. Next, properties that reference only interface          sound properties changes across equivalent implementa-
signals and fall within the supported lowering subset are           tions for 14 of 24 families (58.3%). This does not by itself
translated into formal monitors. The run produced 371               identify the cause of the difference, nor does it imply that
extracted assertions; 357 were supported by the lowering            one coding style is globally more difficult. It demonstrates
pipeline, and 293 were both lowerable and interface-only.           the type of controlled analysis enabled by storing multiple
A property is counted as formally sound when the proof              equivalent implementations under the same family label.
succeeds on its source RTL. Sound properties are then
checked against the three family mutants. Finally, results          Mutation testing provides an additional view of usefulness.
are aggregated by behavior family to measure variation              Across 279 checks pairing a sound generated property with
across the four equivalent implementations.                         a family mutant, 16 checks detect the behavioral change.
                                                                    These detections cover 11 of the 72 unique mutants in
For transparency, strict raw prompt-format compliance               the test families. The detected mutants span multiple
was 0/96 because outputs did not exactly obey the re-               categories, including arbiter, FIFO control, handshake,
quested bare-declaration format. The evaluator therefore            pulse/event, sequence detector, and timer/watchdog. We
separates formatting adherence from syntactic validity of           treat this as a demonstration metric rather than a com-
the extracted SVA content. After the evaluator’s normal-            plete measure of assertion quality.
ization/extraction step, 68/96 tasks produced syntacti-
cally valid SVA.
Let Pint be the set of interface-only generated properties
and Ppass the subset formally proven on their source RTL.           8     Discussion
We report property soundness as
                                                                    8.1    What the family abstraction enables
                               |Ppass |
                   Soundness =          .                 (2)
                                |Pint |                             A conventional RTL-to-SVA example asks whether a prop-
                                                                    erty is correct for one implementation. A behavior family
                                                                    supports additional questions while keeping the intended
For family-level implementation sensitivity, let si denote
                                                                    semantics fixed. For example, researchers can measure
the number of sound properties produced from RTL vari-
                                                                    whether a model produces sound properties for all vari-
ant i. A family is counted as variant-sensitive when the
                                                                    ants, whether the number or type of properties changes
four values are not all equal:
                                                                    by implementation style, whether generated assertions
         Sensitive(F) = 1[|{s1 , s2 , s3 , s4 }| > 1] .   (3)       transfer across family members, and whether mutation
                                                                    sensitivity is stable across implementations. The same
                                                                    family structure can also support training objectives that
Of the 293 interface-only properties, 93 (31.7%) are for-           encourage representation invariance or contrastive reason-
mally sound. Forty-five of 96 RTL tasks produce at least            ing across equivalent designs.


                                                                6
8.2    Complementarity              with      prior      re-        guishable; they should not be interpreted as a statistically
       sources                                                      representative sample of hardware defects.

The contribution of EquivSVA is not that other datasets             Finally, the Qwen2.5-Coder-7B experiment is a single-
should be reorganized in the same way. Different resources          model case study. Its purpose is to demonstrate dataset
serve different needs. Large training corpora are useful for        usage and family-level metrics, not to establish a model
fine-tuning; real-world specification benchmarks are use-           leaderboard. Broader multi-model comparisons, prompt
ful for evaluating practical generation settings; mutation-         strategies, fine-tuning experiments, and deeper mutation
based resources test bug-detection behavior; and tool-              analyses are left for subsequent work.
backed benchmarks provide rigorous correctness signals.
EquivSVA contributes a controlled equivalence dimen-
sion that can be used alongside these existing directions.
                                                                    11      Conclusion
This is why table 1 describes each work by its organization         We presented EquivSVA, a formally verified dataset
and purpose rather than by a checklist of missing features.         organized around behavioral equivalence families. The
                                                                    v2.0 release contains 120 families across 12 categories,
                                                                    480 reference RTL implementations, 914 gold behavioral
9     Public Artifacts and Data Prove-                              properties, and 360 controlled mutants. Each family
      nance                                                         pairs four structurally distinct but formally equivalent
                                                                    implementations with shared interface-level properties and
The EquivSVA behavior specifications, generated RTL,                behavior-changing mutants. Every final family passes a
assertions, mutants, scripts, validation artifacts, and eval-       17-job validation suite, and fixed family-safe splits support
uation outputs used in this work are publicly released. The         reproducible training and evaluation.
model case study uses only Qwen2.5-Coder-7B-Instruct,
whose upstream release is distributed under the Apache              A held-out Qwen2.5-Coder-7B-Instruct case study illus-
License 2.0. The study does not use proprietary models,             trates the central use case: assertion quality can vary
non-public datasets, internal source code or infrastructure,        even when the intended behavior is unchanged. By mak-
customer data, or confidential information. The released            ing equivalent implementations a first-class dataset ele-
repository contains the artifacts needed to reproduce the           ment, EquivSVA provides a reusable basis for studying
reported dataset statistics and case-study evaluation.              whether assertion-generation systems capture behavioral
                                                                    intent rather than implementation-specific structure. The
                                                                    dataset and accompanying tools are publicly available at
10      Limitations                                                 https://github.com/aditigupta96/EquivSVA.

EquivSVA is intentionally controlled and therefore has
several limitations. First, the families are programmati-           A      Representative Families by Cat-
cally generated rather than mined directly from industrial                 egory
code bases. This provides precise semantics and repeat-
able formal validation, but it may not capture the full             The following examples give one representative behavior
structural complexity, naming conventions, long-range               family from each dataset category. They are illustrative
dependencies, or specification ambiguity present in pro-            rather than canonical definitions; the released dataset
duction RTL.                                                        contains ten families per category.
Second, the 12 categories emphasize control logic, small            • Arbiter (arbiter_0006, FSM): sticky two-client ar-
state machines, counters, handshakes, timers, and related             bitration in which an active grant is held until release.
behaviors. The dataset does not attempt comprehensive               • Counter (counter_0006, register rules): modulo-six
coverage of large datapaths, caches, coherent intercon-               counter with synchronous clear and enable control.
nects, deeply pipelined arithmetic units, or full protocol          • FIFO control (fifo_0006, multi-register rules): elas-
stacks. Third, the gold-property distribution is dominated            tic one-entry queue supporting same-cycle pop-and-
by next-cycle implications and invariants. Longer-horizon             replace behavior.
liveness and richer temporal sequences remain an impor-             • Handshake (handshake_0006, FSM): request re-
tant direction for future extensions.                                 mains active until acknowledgment, followed by request
Fourth, the equivalent variants are generated from com-               release.
mon machine-readable specifications and generator fami-             • Interrupt control (interrupt_0006, FSM): masked
lies. Formal equivalence establishes behavioral agreement             interrupt request is latched when enabled and cleared
under the harness assumptions, but generated variants                 by acknowledgment.
can still share stylistic regularities not representative of        • Mode controller (mode_controller_0006, FSM):
independently authored RTL. Fifth, controlled mutants                 locked, ready, and active operating modes with lock-
are designed to be behavior-changing and formally distin-             /unlock control.


                                                                7
• Protocol controller (protocol_controller_0002,         [5] Aarush Goradia. Veri2: A formally verified rtl–sva
  FSM): command/response protocol that waits for a           dataset for fine-tuning local language models. GitHub
  response before reporting completion.                      repository, 2026. Accessed September 2026.
• Pulse/event (pulse_event_0002, FSM): one-shot
                                                         [6] Adarsh Gupta, Bhabesh Mali, and Chandan Karfa.
  event pulse with rearming after the triggering level
                                                             Sangam: Systemverilog assertion generation via
  is released.
                                                             monte carlo tree self-refine, 2025.
• Rate limiter (rate_limiter_0002, register rules):
  token state with refill priority and bounded token ca- [7] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Day-
  pacity.                                                    iheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
• Saturating arithmetic (saturating_arithmetic_0002,         Bowen Yu, Keming Lu, Kai Dang, Yang Fan,
  register rules): incrementing value that saturates at      Yichang   Zhang, An Yang, Rui Men, Fei Huang,
  five and supports synchronous clear.                       Bo  Zheng,  Yibo Miao, Shanghaoran Quan, Yunlong
• Sequence detector (sequence_detector_0002,                 Feng, Xingzhang    Ren, Xuancheng Ren, Jingren Zhou,
  FSM): overlapping serial detector for the bit pattern      and  Junyang    Lin. Qwen2.5-coder technical report,
  110.                                                       2024.
• Timer/watchdog (timer_0007, register rules):           [8] Minwoo Kang, Mingjie Liu, Ghaith Bany Hamad,
  countdown timer loaded to seven and decremented            Syed Suhaib, and Haoxing Ren. Fveval: Understand-
  on tick until expiration.                                  ing language model capabilities in formal verification
                                                                     of digital hardware, 2024.
Artifact Availability                                             [9] Hongqin Lyu, Yonghao Wang, Yunlin Du, Mingyu
                                                                      Shi, Zhiteng Chao, Wenxing Li, Tiancheng Wang,
The public dataset, generators, validation scripts, eval-             and Huawei Li. Assertgen: Enhancement of llm-
uation code, and case-study artifacts are available at                aided assertion generation through cross-layer signal
https://github.com/aditigupta96/EquivSVA. The frozen                  bridging, 2025.
v2.0 snapshot used for this paper is available at https://
github.com/aditigupta96/EquivSVA/releases/tag/v2.0.              [10] Anand Menon, Samit S. Miftah, Shamik Kundu,
                                                                      Souvik Kundu, Amisha Srivastava, Arnab Raha,
                                                                      Gabriel Theodor Sonnenschein, Suvadeep Banerjee,
AI Use Disclosure                                                     Deepak Mathaikutty, and Kanad Basu. Enhancing
                                                                      large language models for hardware verification: A
Generative AI tools were used to assist with software                 novel systemverilog assertion dataset, 2025.
development and manuscript preparation. All technical
content and results were reviewed and validated by the           [11] Aina Niemetz and Mathias Preiner. Bitwuzla. In
author.                                                               Computer Aided Verification – 35th International
                                                                      Conference, CAV 2023, Proceedings, Part II, volume
                                                                      13965 of Lecture Notes in Computer Science, pages
References                                                            3–17. Springer, 2023.

 [1] Wenji Fang, Mengming Li, Min Li, Zhiyuan Yan,               [12] Vaishnavi Pulavarthi, Deeksha Nandal, Soham Dan,
     Shang Liu, Zhiyao Xie, and Hongce Zhang. Assertllm:              and Debjit Pal. Assertionbench: A benchmark to
     Generating and evaluating hardware verification as-              evaluate large-language models for assertion gener-
     sertions from design specifications via multi-llms,              ation. In Findings of the Association for Computa-
     2024.                                                            tional Linguistics: NAACL 2025, pages 8073–8080.
                                                                      Association for Computational Linguistics, 2025.
 [2] FNU Aditi. Robustness of llm-generated systemver-
     ilog assertions to semantics-preserving rtl transfor-       [13] Clifford Wolf and Johann Glaser. Yosys – a free
     mations, 2026.                                                   verilog synthesis suite. In Austrochip Workshop on
                                                                      Microelectronics 2013, pages 47–52, 2013.
 [3] FNU Aditi and Michael S. Hsiao. Hybrid rule-based
     and machine learning system for assertion generation        [14] Fenghua Wu, Evan Pan, Rahul Kande, Michael
     from natural language specifications. In 2022 IEEE               Quinn, Aakash Tyagi, David Kebo, Jeyavijayan Ra-
     31st Asian Test Symposium (ATS), pages 126–131.                  jendran, and Jiang Hu. Spec2assertion: Automatic
     IEEE, 2022.                                                      pre-rtl assertion generation using large language mod-
                                                                      els with progressive regularization, 2025.
 [4] FNU Aditi and Michael S. Hsiao. Validatable gener-
     ation of system verilog assertions from natural lan-        [15] Yuchao Wu, Wenji Fang, Jing Wang, Wenkai Li,
     guage specifications. In 2023 Fifth International                Ziyan Guo, and Zhiyao Xie. Assertllm2: A compre-
     Conference on Transdisciplinary AI (TransAI), pages              hensive llm benchmark for assertion generation from
     102–109. IEEE, 2023.                                             design specifications, 2026.


                                                             8
[16] Yutong Wu, Chenrui Cao, Pengwei Jin, Di Huang,
     Rui Zhang, Xishan Zhang, Zidong Du, Qi Guo,
     and Xing Hu. Qimeng-codev-sva: Training special-
     ized llms for hardware assertion generation via rtl-
     grounded bidirectional data synthesis, 2026.
[17] YosysHQ. Symbiyosys (sby): Front-end for yosys-
     based formal verification flows. Software documenta-
     tion and repository. Accessed September 2026.




                                                            9
