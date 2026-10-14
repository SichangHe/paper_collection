                                         IaC-Guard-V: A Verification Framework for LLM-Generated Infrastructure-as-Code
                                                                            Repairs

                                                                                                           Lokesh Chauhan1
                                                                                               1
                                                                                                   Independent Researcher, Dallas, USA
                                                                                                        lokesh0186@gmail.com



                                         Abstract—Infrastructure-as-Code (IaC) misconfigurations are                     enabling teams to define servers, networks, and security poli-
                                         a leading cause of cloud security incidents, and Large Lan-                     cies through machine-readable configuration files in formats
                                         guage Models (LLMs) are increasingly proposed as automated                      such as Terraform HCL and Kubernetes YAML. However, IaC
                                         repair agents. While recent work has established detect-repair-                 misconfigurations remain a leading cause of cloud security
arXiv:2609.28488v1 [cs.SE] 12 Aug 2026




                                         verify workflows for general-purpose code, the trustworthi-                     incidents: the 2025 Cloud Security Report found that 65%
                                         ness of LLM-generated repairs for IaC remains uninvesti-                        of organizations experienced a cloud-related security incident
                                         gated. IaC presents unique verification challenges: security                    in the past year, with misconfigurations ranking among the
                                         scanners may produce inconsistent results across tools and                      top causes [1], [2]. Static analysis tools such as Checkov,
                                         configurations, infrastructure semantics cannot be validated                    KICS, and Terrascan can detect these misconfigurations, but
                                         through unit tests, and provider-specific rules create a frag-                  remediation remains a manual, error-prone process that scales
                                         mented verification landscape. We present IaC-Guard-V, a                        poorly across large infrastructure codebases.
                                         verification-centered framework that evaluates AI-generated                     Large Language Models (LLMs) have emerged as promising
                                         IaC repairs through four verification gates: syntactic validity,                automated repair agents. In the broader domain of automated
                                         target-issue resolution, regression safety, and patch minimality.               program repair (APR), LLM-based systems now fix hundreds
                                         We construct a multi-technology benchmark of 70 real-world                      of real-world bugs at costs below $1 per fix [3], and recent
                                         misconfigured Terraform and Kubernetes artifacts spanning                       work has established detect–repair–verify (DRV) workflows
                                         70 unique scanner rules across eight violation classes. The                     that iteratively refine LLM-generated patches using test feed-
                                         evaluation spans three repair strategies across three LLM                       back [4]. Naturally, practitioners are increasingly exploring
                                         families in 630 experimental runs. Our results reveal that                      LLMs for IaC repair, prompting models to fix flagged miscon-
                                         while all models achieve 100% syntactic validity, only 32–50%                   figurations and deploying the generated patches with minimal
                                         of repairs pass full verification under single-shot prompting.                  review.
                                         Verification-guided iterative repair statistically significantly                This practice is dangerous. While LLM-generated IaC repairs
                                         improves verified-fix rates across all models, achieving 68–                    may appear syntactically correct, their actual trustworthiness—
                                         92% compared to 32–50% for baselines. Notably, an open-                         whether they resolve the target issue without introducing new
                                         source model with verification-guided repair outperforms the                    vulnerabilities—remains uninvestigated for IaC specifically.
                                         strongest commercial model without it at one-twelfth the                        Motivating example. Consider the Terraform configuration
                                         cost per verified fix. Cross-technology analysis reveals that                   in Listing 1, which triggers Checkov rule CKV AWS 8
                                         Kubernetes repairs achieve near-perfect rates for commercial                    (“Ensure that launch configuration EBS volumes are en-
                                         models but require verification-guided iteration for open-                      crypted”). When prompted to fix this misconfiguration,
                                         source models, demonstrating that technology complexity and                     Claude Sonnet 4.6 produces a syntactically valid repair that
                                         model capability jointly determine repair trustworthiness. We                   changes associate_public_ip_address from true
                                         further find that structured prompting consistently degrades                    to false—a plausible-looking security improvement, but one
                                         Terraform repair quality across all models, a counterintuitive                  that addresses the wrong attribute entirely. The actual fix re-
                                         result that challenges common assumptions about constrained                     quires adding encrypted = true to the root block device
                                         LLM output. All artifacts are released for reproducibility.                     configuration. Without automated verification, a practitioner
                                                                                                                         reviewing this repair might accept it, believing the security
                                         Keywords–Infrastructure-as-Code; large language models; au-
                                                                                                                         issue was resolved. Our verification harness catches this failure
                                         tomated program repair; verification; software reliability;
                                                                                                                         at gate V2 (target-issue resolution), and the verification-guided
                                         Terraform
                                                                                                                         repair loop feeds this feedback back to the model, which
                                                                                                                         produces the correct fix on the second attempt.
                                         1. I NTRODUCTION
                                                                                                                         General-purpose DRV workflows [4] rely on unit tests and
                                         Infrastructure-as-Code (IaC) has become the standard mech-                      functional test suites for verification, an approach that does
                                         anism for provisioning and managing cloud infrastructure,                       not transfer to IaC for three reasons. First, IaC artifacts lack
                                           0 This work was conducted independently and does not relate to the author’s
                                                                                                                         executable test suites; verification must rely on static security
                                         position at Amazon. No Amazon resources, data, or confidential information      scanners that may produce inconsistent results across tools and
                                         were used.                                                                      configurations. Second, IaC encodes provider-specific seman-
                                                                        Opus 4.6, Claude Sonnet 4.6, Llama 4 Maverick), three
      (a) Original — CKV AWS 8: EBS volumes not encrypted
                                                                        repair strategies (plain prompting, structured prompting,
resource "aws_launch_configuration" "lc" {
  image_id      = "ami-0c55b24b055c14ff6"                               verification-guided iterative repair), and two IaC technolo-
  instance_type = "t2.micro"                                            gies (Terraform, Kubernetes).
  associate_public_ip_address = true
  # Missing: root_block_device { encrypted = true }                 4) Key findings. (a) While all models achieve 100% syntactic
}                                                                       validity, only 32–50% of repairs pass full verification un-
                                                                        der single-shot prompting. (b) Verification-guided iterative
         (b) LLM “fix” — syntactically valid but WRONG
                                                                        repair achieves 68–92% VFR, statistically significantly
resource "aws_launch_configuration" "lc" {
  image_id      = "ami-0c55b24b055c14ff6"                               outperforming baselines. (c) An open-source model with
  instance_type = "t2.micro"                                            verification outperforms the strongest commercial model
  associate_public_ip_address = false # Changed wrong
  # attribute! EBS encryption still missing.                            without it at a fraction of the cost per verified fix.
}                                                                       (d) Structured prompting consistently degrades Terraform
                                                                        repair quality—a counterintuitive finding. (e) Kubernetes
         (c) Correct fix — found by verify-loop (attempt 2)
                                                                        repairs achieve near-perfect rates for commercial models
resource "aws_launch_configuration" "lc" {
  image_id      = "ami-0c55b24b055c14ff6"                               but require verification for open-source models, revealing
  instance_type = "t2.micro"                                            that technology complexity and model capability jointly
  associate_public_ip_address = true
  root_block_device {                                                   determine trustworthiness.
    encrypted = true # Actual fix for CKV_AWS_8
  }                                                                 All benchmark items, the verification harness, and experimen-
}                                                                   tal artifacts are released for reproducibility.1

Figure 1: Motivating example from benchmark item BM-0051.           2. BACKGROUND AND R ELATED W ORK
The LLM produces a syntactically valid repair (b) that changes      We organize related work into three areas: LLM-based auto-
the wrong attribute. The verification harness detects this at       mated program repair, IaC-specific repair and generation, and
gate V2 (target-issue resolution), and the iterative repair loop    IaC benchmarks and defect taxonomies. Table I positions our
produces the correct fix (c) on the second attempt.                 study against the most closely related work.

                                                                    2.1 LLM-Based Automated Program Repair
tics (e.g., AWS resource attributes, Kubernetes pod security        Large language models have transformed automated program
contexts) that vary across hundreds of resource types, making       repair (APR). Xia et al. [5] demonstrated that directly leverag-
correct repair far more context-dependent than fixing a Python      ing LLMs for program repair achieves competitive results, es-
function. Third, IaC files frequently contain multiple resources,   tablishing a practical baseline for the field. Zhang et al. [6] pro-
and a repair that fixes one misconfiguration may silently           vide the first systematic literature review of 189 LLM-based
introduce regressions in others—a failure mode that syntactic       APR papers, categorizing utilization strategies across semantic
validity alone cannot detect.                                       bugs, security vulnerabilities, and other repair scenarios. Yang
In this paper, we present IaC-Guard-V, a verification-centered      et al. [7] propose a unified taxonomy grouping 62 systems into
framework that evaluates LLM-generated IaC repairs through          four paradigms: fine-tuning, prompting, procedural pipelines,
four verification dimensions: three binary gates—(V1) syn-          and agentic frameworks.
tactic validity, (V2) target-issue resolution, (V3) regression      Among individual systems, ChatRepair [3] pioneered
safety—and one informational metric, (V4) patch minimality.         conversation-driven repair, interleaving patch generation with
We define the verified-fix rate (VFR) metric, which counts          test feedback to fix 162 of 337 Defects4J bugs at $0.42 each.
a repair as successful only when it passes all three binary         AlphaRepair [8] demonstrated that zero-shot LLM application
gates, and construct a multi-technology benchmark of 70 real-       can outperform supervised approaches. RepairLLaMA [9]
world misconfigured artifacts (50 Terraform, 20 Kubernetes)         demonstrated that parameter-efficient fine-tuning of open-
spanning 70 unique scanner rules and eight violation classes.       source models can match or exceed commercial models,
We make the following contributions:                                fixing 144 Defects4J v2 bugs. RepairAgent [10] introduced
1) Framework. IaC-Guard-V, a verification-centered frame-           autonomous agent-based repair using a finite state machine,
    work with four verification gates tailored to IaC-specific      repairing 164 bugs including 39 not fixed by prior techniques.
    challenges, including a verification-guided iterative repair    FLAMES [11] uses semantic-guided search to reduce memory
    loop that feeds scanner feedback back to the LLM.               consumption by 83% while maintaining repair effectiveness.
2) Benchmark. A multi-technology benchmark of 70 mis-               Most relevant to our work, Cheng [4] introduced the Detect–
    configured IaC artifacts drawn from Checkov’s test suite,       Repair–Verify (DRV) workflow for securing LLM-generated
    with stratified selection across 70 unique rules and eight      code, constructing a benchmark of runnable web applications
    violation classes, accompanied by baseline scanner outputs      and comparing single-pass and bounded iterative DRV vari-
    for reproducible evaluation.                                    ants. The iterative refinement paradigm has broader roots:
3) Empirical study. A comprehensive evaluation of 630
    experimental runs across three LLM families (Claude               1 Replication package: https://github.com/[redacted-for-review]
Chen et al. [12] showed that LLMs can self-debug by                 that tools like Checkov build upon. Sharma et al. [22] cata-
explaining and correcting their own code, and Madaan et             loged 24 configuration smells across 4,621 Puppet repositories,
al. [13] demonstrated that iterative self-feedback improves         while Steffens et al. [26] extended this work to Chef with
LLM outputs across diverse tasks. Tang et al. [29] formal-          17 technology-agnostic smells. Saavedra and Ferreira [23]
ized the exploration-exploitation tradeoff inherent in iterative    proposed GLITCH, a polyglot framework for cross-technology
code repair. While DRV establishes the iterative verification       security smell detection across Ansible, Chef, Puppet, and
paradigm we build upon, it targets general-purpose code (PHP,       Terraform. Dalla Palma et al. [24] developed ML-based defect
JavaScript, Python) and relies on unit tests and functional         prediction for IaC using product and process metrics. Verdet
test suites for verification—an approach that does not transfer     et al. [25] conducted the first large-scale empirical study of
to IaC, where infrastructure semantics cannot be validated          Terraform security practices using Checkov and tfsec across
through unit tests, security scanners may disagree on the           812 projects, finding significant variation in security policy
same artifact, and provider-specific rules create a fragmented      adoption across cloud providers. Hummer et al. [31] proposed
verification landscape. IaC-Guard-V addresses these gaps by         model-based testing for IaC idempotence.
defining four IaC-specific verification gates and evaluating        For benchmarking LLM capabilities, IaC-Eval [27] evaluates
repair across multiple IaC technologies and scanner rules.          Terraform code generation with formal verification, show-
                                                                    ing that GPT-4 achieves only 19.36% pass@1 accuracy—
2.2 IaC-Specific Repair and Generation                              far below its 86.6% on Python benchmarks—highlighting the
                                                                    difficulty gap between general code and IaC. Rahman et
Several recent works address IaC repair and generation di-
                                                                    al. [28] conducted a large-scale empirical study of security
rectly. TerraFormer [15] combines supervised fine-tuning with
                                                                    misconfigurations in open-source Kubernetes manifests, pro-
verifier-guided reinforcement learning (GRPO) for Terraform
                                                                    viding foundational data on defect prevalence.
generation and mutation, demonstrating that a 14B fine-tuned
                                                                    Gap. No prior work combines LLM-based repair, multi-
model can outperform 50× larger models on correctness
                                                                    dimensional verification (syntax, resolution, regression, min-
and security compliance. However, TerraFormer focuses on
                                                                    imality), and cross-technology IaC evaluation in a single
generation (NL-to-IaC) rather than repair of existing miscon-
                                                                    framework. IaC-Guard-V fills this gap.
figurations, and its verification is limited to policy compliance
scoring without regression analysis.                                3. I AC-G UARD -V F RAMEWORK
InfraFix [16] proposes the first technology-agnostic APR            This section presents IaC-Guard-V, a verification-centered
framework for IaC, using SMT-based repair guided by inferred        framework for evaluating LLM-generated IaC repairs. Figure 2
system states across Ansible, Puppet, Chef, and Terraform.          illustrates the end-to-end pipeline.
While InfraFix achieves 95.7% success across 254,288 repair
scenarios, it uses constraint solving rather than LLMs and does     3.1 Verification Gates
not evaluate the trustworthiness of LLM-generated repairs.          Given an original IaC artifact A, a repaired artifact A′ =
For Kubernetes specifically, GenKubeSec [17] fine-tunes a           f (A, v) produced by an LLM in response to a scanner finding
local LLM for misconfiguration detection and remediation            v, we define a repair as a verified fix if and only if it passes
across 169 misconfiguration types, achieving 0.990 precision        all three binary verification gates:
on ∼277,000 configurations. LLMSecConfig [18] combines
Checkov with LLMs and RAG for container misconfigura-                      VF (A, A′ , v) = V1 (A′ ) ∧ V2 (A′ , v) ∧ V3 (A, A′ )   (1)
tion repair, reporting 94.3% success with Mistral Large 2
                                                                    Patch minimality (V4 ) is measured but does not gate the
on 1,000 real-world configurations. Both focus on single-
                                                                    verdict, as there is no universally accepted threshold for
technology repair without cross-technology comparison or
                                                                    acceptable patch size.
multi-dimensional verification.
                                                                    V1: Syntactic Validity. The repaired artifact must be parseable
IaCGen [19] introduces a deployability-centric benchmark
                                                                    by the target technology’s parser (HCL for Terraform, YAML
(153 AWS scenarios) and an iterative feedback framework
                                                                    for Kubernetes). We use Checkov’s built-in parser as the
achieving 54.6–91.6% deployment success within 10 itera-
                                                                    syntax check: if Checkov can scan the file and produce
tions. Palavalli and Santolucito [20] study feedback loops
                                                                    structured output, the artifact is syntactically valid.
for CloudFormation generation, finding that effectiveness
                                                                    V2: Target-Issue Resolution. The specific scanner finding v
decreases exponentially and plateaus after approximately 5
                                                                    that triggered the repair must no longer appear in the Checkov
iterations—a finding our convergence analysis corroborates for
                                                                    output for A′ . We re-run Checkov on the repaired artifact and
repair (Section VI-E).
                                                                    verify that the target rule ID is absent from the failed-checks
                                                                    list. In multi-resource files, we check the rule at the file level;
2.3 IaC Benchmarks and Defect Taxonomies
                                                                    a limitation of this approach is discussed in Section VI-E.
The IaC research community has established several bench-           V3: Regression Safety. The repair must not introduce new
marks and taxonomies. Rahman et al. [21] identified seven           scanner findings. We compare the set of failed Checkov
categories of security smells in IaC scripts through analysis of    rule IDs on A′ against the baseline set on A. Any rule ID
1,726 Puppet scripts, establishing the foundational taxonomy        that appears in the repaired output but not in the baseline
                                      TABLE I: Positioning of This Study Against Related Work
         Study                      Focus                            IaC    LLM      Verification      Repair       Benchmark
         DRV [4]                    General code DRV                  No     Yes      Unit tests        Yes        Yes (web apps)
         ChatRepair [3]             Conversational APR                No     Yes      Unit tests        Yes          Defects4J
         TerraFormer [15]           IaC generation + RL              Yes     Yes     Policy score     No (gen)      Yes (152K)
         InfraFix [16]              IaC repair (SMT)                 Yes     No         Partial         Yes         Yes (254K)
         GenKubeSec [17]            K8s misconfig repair             Yes     Yes    Detection only      Yes         Yes (277K)
         LLMSecConfig [18]          Container repair                 Yes     Yes      Checkov           Yes           Yes (1K)
         IaC-Eval [27]              IaC generation bench             Yes     Yes       Formal           No           Yes (458)
         IaCGen [19]                IaC gen + feedback               Yes     Yes     Deploy test      No (gen)       Yes (153)
         This study                 IaC repair verif.                Yes     Yes       4 gates          Yes           Yes (70)




Figure 2: IaC-Guard-V pipeline. An IaC artifact with a scanner finding is repaired by an LLM using one of three strategies.
The verification harness evaluates the repair across four gates. In verify-loop mode, failed verification results are fed back to
the LLM for up to two retries.


constitutes a regression, regardless of which resource triggers             Structured prompting. The LLM receives the artifact along
it. A verified fix requires zero regressions.                               with the Checkov rule ID, rule description, violation class,
V4: Patch Minimality. We measure the size of the repair as                  affected resource name, and affected line range. The model is
the number of lines added, removed, or modified (computed                   instructed to return a JSON object containing the fixed artifact,
via unified diff). Unlike V1–V3, minimality is not a binary                 a patch summary, and lists of changed resources and attributes.
gate but an informational metric: excessively large patches                 This strategy tests whether providing structured context and
suggest the LLM rewrote unrelated sections rather than making               constraining output format improves repair quality.
a targeted fix. We report minimality statistics to characterize             Verification-guided iterative repair. The first attempt uses the
repair precision.                                                           structured prompt because it provides the LLM with maximum
                                                                            context about the target rule, even though single-shot struc-
3.2 Verified-Fix Rate
                                                                            tured prompting underperforms plain prompting (Section VI-
The primary evaluation metric is the verified-fix rate (VFR):               A). If verification fails, the harness constructs a retry prompt
                                                                            containing the original artifact, the failed attempt, and detailed
               |{i : V1 (A′i ) ∧ V2 (A′i , vi ) ∧ V3 (Ai , A′i )}|          verification feedback (which gates passed, which failed, and
      VFR =                                                           (2)
                                      N                                     the Checkov output on the failed repair). The LLM receives
where N is the total number of benchmark items. VFR is                      this feedback and produces a revised fix. We allow up to
strictly more conservative than metrics that count syntactically            two retries (three total attempts), chosen based on preliminary
valid or plausible-looking repairs, as it requires simultaneous             experiments showing diminishing returns beyond the second
satisfaction of syntax, resolution, and regression gates.                   retry (confirmed in Section VI-E). This strategy tests whether
                                                                            verification feedback enables the LLM to self-correct.
3.3 Repair Strategies                                                       Patch extraction. For plain prompting, we extract the re-
We evaluate three repair strategies of increasing sophistication:           sponse text, stripping any markdown code fences. For struc-
Plain prompting. The LLM receives the misconfigured arti-                   tured and verification-guided prompting, we parse the JSON
fact and a generic instruction to fix the security misconfigura-            response and extract the fixed_artifact field; if JSON
tion. No information about the specific rule, affected resource,            parsing fails, we fall back to regex extraction of the JSON
or expected fix is provided. The model returns raw IaC code.                object.
3.4 Implementation                                                               TABLE II: Benchmark Composition

The IaC-Guard-V framework is implemented in Python (ap-                 Violation Class                Terraform        Kubernetes
proximately 1,200 lines of code) and consists of four modules.          Missing encryption                 12               2
The prompt constructor generates method-specific prompts by             Over-permissive access              8               6
combining the original artifact with Checkov metadata (rule             Network hardening                   8               3
ID, description, affected resource, line range). The Bedrock            Public exposure                     6              —
caller handles API communication with AWS Bedrock, sup-                 Weak observability                  6               1
porting both Anthropic (Messages API) and Meta (Llama)                  Insecure defaults                   5               3
model families with automatic retry on transient errors.                Missing runtime safety             —                4
The verification harness orchestrates the four-gate evaluation          Other                               5               1
pipeline: it invokes Checkov as a subprocess, parses the JSON           Total                              50              20
output to extract failed rules, computes the diff between               Each item maps to a unique Checkov rule (70 total).
original and repaired artifacts, and renders a per-gate verdict.
The experiment runner coordinates the full evaluation loop,         4.2 Violation Taxonomy
managing the verify-loop retry logic and recording all inter-
                                                                    We classify benchmark items into eight violation classes based
mediate results (per-attempt verification, token counts, latency)
                                                                    on the misconfiguration’s security impact. Table II summarizes
to JSON files for post-hoc analysis.
                                                                    the benchmark composition.
The verification harness executes Checkov in quiet mode with
JSON output (checkov -f <file> --output json                        4.3 Baseline Establishment
--quiet --compact), parsing the structured results to               For each benchmark item, we run Checkov and record the
extract the list of failed rule IDs. For V2, we check whether       complete set of failed rules as the baseline. This baseline
the target rule ID appears in the failed-checks list of the         serves two purposes: (1) confirming that the target rule is
repaired file. For V3, we compute the set difference between        present in the scanner output (verified for all 70 items), and
the repaired file’s failed rules and the baseline’s failed rules;   (2) providing the reference set for regression detection (V3).
any new rule constitutes a regression. For V4, we compute           Baseline Checkov outputs, raw artifacts, and the selection
a unified diff and count added, removed, and modified lines,        manifest are included in the replication package.
reporting the diff ratio (changed lines divided by original file
                                                                    5. E XPERIMENTAL S ETUP
length) as the minimality metric.
                                                                    5.1 Models
4. B ENCHMARK C ONSTRUCTION                                         We evaluate three LLMs spanning two model families, ac-
                                                                    cessed via the AWS Bedrock API: Claude Opus 4.6 and
We construct a multi-technology benchmark of 70 misconfig-          Claude Sonnet 4.6 (Anthropic, commercial, undisclosed pa-
ured IaC artifacts designed to evaluate repair across diverse       rameter counts) and Llama 4 Maverick 17B (Meta, open-
violation types and technologies.                                   weight, 17B active parameters in a mixture-of-experts archi-
                                                                    tecture). This selection provides two commercial models of
                                                                    different capability levels (Opus, Sonnet) and one open-source
4.1 Source and Selection                                            model (Maverick), enabling analysis of how model capability
We source benchmark items from Checkov’s official test              and openness affect repair quality.
suite (v3.2.517), which contains IaC artifacts written by the       5.2 Configuration
tool’s maintainers to validate specific scanner rules. These
                                                                    All models use temperature 0 for deterministic outputs, ensur-
artifacts represent realistic misconfiguration patterns—each is
                                                                    ing reproducibility without repeated runs. Maximum output
a minimal, self-contained file that triggers one or more known
                                                                    length is set to 4,096 tokens. For verification-guided iterative
Checkov rules—while being publicly available and free of
                                                                    repair, we allow up to two retries (three total attempts). All
proprietary content.
                                                                    verification runs use Checkov v3.2.517. Prompts are provided
For Terraform, we scanned 287 AWS-specific test directories         in the replication package.
containing 1,081 individual rule violations across 369 unique
Checkov rules. We selected 50 items using stratified sampling:      5.3 Evaluation Protocol
one item per unique rule, with deliberate over-sampling of          Each of the 70 benchmark items is evaluated with each
minority violation classes (e.g., public exposure at 12% of         of the three repair strategies on each of the three models,
the benchmark vs. 4% of the corpus) to avoid inflating fix          yielding 70 × 3 × 3 = 630 experimental runs. For each
rates with easily repaired encryption misconfigurations, which      run, we record: the raw model response, the extracted patch,
dominate the corpus at 29%. For Kubernetes, we scanned              all four verification dimension results, token counts (input
98 test directories containing 2,400 violations across 215          and output), and wall-clock latency. For verification-guided
unique rules and selected 20 items using the same one-per-          runs, we additionally record per-attempt verification results to
rule strategy.                                                      enable convergence analysis.
5.4 Statistical Methods
We report 95% bootstrap confidence intervals (1,000 resamples
with fixed seed) for all verified-fix rates. We test for overall
method differences using Cochran’s Q test and perform six
pre-specified pairwise comparisons (verify-loop vs. plain and
verify-loop vs. structured, for each of the three models on
the Terraform benchmark) using McNemar’s exact test with
Bonferroni correction (α = 0.05/6 = 0.0083). We report
Cliff’s delta as the effect size measure alongside each p-
value. Kubernetes comparisons are reported descriptively, as
commercial models achieve ceiling performance (100%).
6. R ESULTS
We organize our results around five research questions. All        Figure 3: Verified-fix rate by model and repair strategy (Terra-
experiments use temperature 0 for deterministic outputs; each      form, n=50). Verify-loop substantially outperforms both base-
benchmark item is evaluated once per model-method combina-         lines for all models. Error bars show 95% bootstrap confidence
tion, yielding 630 total runs (450 Terraform, 180 Kubernetes).     intervals.
6.1 RQ1: Effectiveness of Verification-Guided Repair
                                                                       TABLE III: Terraform Repair Results (n=50 per cell)
Motivation. Our central claim is that verification-guided iter-
ative repair produces more trustworthy fixes than single-shot         Model      Method      V1     V2    V3      VFR      CI
prompting. We evaluate this on the Terraform benchmark (50                       Plain       100    46    100      46     32–60
items, 3 models, 3 methods).                                          Opus       Struct.     100    34     96      34     22–46
Approach. For each benchmark item, we run all three re-                          V-loop      100    92     98      92     84–98
pair strategies and measure the verified-fix rate (VFR): the                     Plain       100    44    100      44     30–58
proportion of repairs that pass all three binary verification         Sonnet     Struct.     100    34     90      32     20–44
gates. We report 95% bootstrap confidence intervals (1,000                       V-loop      100    76     92      68     54–80
resamples) and test significance using McNemar’s test with                       Plain       100    52     88      50     36–64
Bonferroni correction (α = 0.05/6 = 0.0083 for six pre-               Mav.       Struct.     100    42    100      42     28–56
specified comparisons).                                                          V-loop      100    74     94      70     56–82
Results. Table III and Figure 3 present the Terraform results.     V1=Syntax, V2=Resolved, V3=No Regression (%). CI=95% bootstrap. V4
Three findings emerge.                                                               (minimality) reported separately.
First, all models achieve 100% syntactic validity across all
methods, confirming that modern LLMs reliably generate
parseable HCL. However, syntactic validity alone is a poor         δ = 0.28, small). Verify-loop versus plain is significant
proxy for correctness: only 34–52% of syntactically valid          for Opus (p < 0.001, δ = 0.46, medium) and approaches
repairs resolve the target issue under single-shot prompting.      significance for Sonnet (p = 0.008, δ = 0.24) and Maverick
Second, verification-guided iterative repair (verify-loop) sub-    (p = 0.006, δ = 0.20); all three are significant under Holm-
stantially outperforms both baselines for every model. Opus        Bonferroni correction.
achieves 92% VFR (CI: 84–98%), Maverick 70% (CI: 56–
                                                                   6.2 RQ2: Variation by Violation Class
82%), and Sonnet 68% (CI: 54–80%), compared to 32–50%
for plain and structured prompting. The confidence intervals       Motivation. Not all misconfigurations are equally difficult to
for verify-loop do not overlap with those of structured prompt-    repair. We analyze whether verified-fix rates vary by violation
ing for any model.                                                 class.
Third, structured prompting consistently underperforms plain       Approach. We aggregate VFR across all three models for each
prompting (32–42% vs. 44–50%), a counterintuitive finding          violation class and compare plain versus verify-loop to identify
we discuss in Section VII. Structured prompting also intro-        where verification feedback provides the greatest benefit.
duces regressions in 4–10% of cases, while plain prompting         Results. Table IV presents verify-loop VFR by violation class,
on Opus and Sonnet introduces none.                                aggregated across all three models. Fix rates range from 47%
Statistical significance confirms these findings. Cochran’s Q      (insecure defaults) to 97% (missing encryption). Missing-
test rejects the null hypothesis of equal method performance       encryption violations are the easiest to repair because they
for all three models (p < 0.001). In pairwise McNemar’s            typically require adding a single attribute (e.g., encrypted
tests with Bonferroni correction (α = 0.0083), verify-loop         = true). Insecure-defaults and “other” violations are hardest
significantly outperforms structured prompting for all three       because they involve multi-resource files or provider-specific
models: Opus (p < 0.001, Cliff’s δ = 0.58, large), Sonnet          semantics that LLMs struggle to resolve. Public-exposure
(p < 0.001, δ = 0.36, medium), and Maverick (p < 0.001,            violations show the largest improvement from verify-loop over
TABLE IV: Verify-Loop VFR by Violation Class (Terraform)                    TABLE VI: Kubernetes Repair Results (n=20 per cell)
    Violation Class                 Plain     Verify-loop        ∆               Model       Method        V1      V2      V3      VFR
    Missing encryption               83           97            +14                          Plain         100     100     100     100
    Public exposure                  17           94            +78              Opus        Struct.       100     100     100     100
    Weak observability               56           83            +28                          V-loop        100     100     100     100
    Over-permissive access           46           71            +25                          Plain         100     100     100     100
    Network hardening                33           67            +33              Sonnet      Struct.       100     100     100     100
    Other                            20           53            +33                          V-loop        100     100     100     100
    Insecure defaults                33           47            +13                          Plain         100      70      55      45
    All values are percentages, aggregated across 3 models.                      Mav.        Struct.        95      95      95      95
                                                                                             V-loop        100     100     100     100
TABLE V: Verify-Loop VFR by Model and Violation Class                    All values are percentages. VFR requires passing all gates simultaneously.
(Terraform, %)
                                                                                 TABLE VII: Cost-Effectiveness (All 70 Items)
 Violation Class                     Opus       Sonnet        Maverick
 Missing encryption (12)              100        100             92             Model       Meth.      VFR       Tok.      Lat.       $/fix
 Public exposure (6)                  100         83            100             Mav.        Plain      48.6      1,027     1.7s       .001
 Weak observability (6)                83         83             83             Mav.        Verify     78.6      3,163     5.0s       .002
 Over-permissive access (8)            88         75             50             Sonnet      Plain      60.0      1,217     5.1s       .018
 Network hardening (8)                 88         63             50             Sonnet      Verify     77.1      4,188     17.6s      .044
 Other (5)                             80          0             80             Opus        Plain      61.4      1,214     6.4s       .029
 Insecure defaults (5)                100         20             20             Opus        Verify     94.3      3,320     15.2s      .047
                                                                         Tok.=avg tokens. Lat.=avg latency. $/fix=USD per verified fix. VFR across
 Overall (50)                          92         68             70
                                                                             50 TF + 20 K8s items. Structured omitted (underperforms plain).
 Numbers in parentheses indicate items per class.


                                                                         netes structured), suggesting that the JSON schema constraint
plain (94% vs. 17%), suggesting that verification feedback is
                                                                         occasionally disrupts YAML generation for open-source mod-
most valuable for violations where the initial fix attempt is
                                                                         els. Structured prompting dramatically improves Maverick’s
likely to be incomplete.
                                                                         Kubernetes performance (45% → 95%), the opposite of its
Table V disaggregates verify-loop VFR by model and violation
                                                                         effect on Terraform where it consistently degrades quality.
class, revealing substantial model-dependent variation. Opus
                                                                         We attribute the overall technology gap to three structural
achieves 100% on missing encryption and insecure defaults,
                                                                         differences: (1) Kubernetes manifests are declarative YAML
while Sonnet and Maverick achieve only 20% on insecure
                                                                         with flat, well-documented schemas, whereas Terraform HCL
defaults—an 80 percentage point gap within the same violation
                                                                         encodes provider-specific semantics across hundreds of re-
class. The “other” category shows the most extreme diver-
                                                                         source types; (2) Terraform misconfigurations frequently in-
gence: Opus and Maverick achieve 80% while Sonnet achieves
                                                                         volve cross-resource dependencies absent in typical Kuber-
0%, suggesting that Sonnet’s repair strategy fails on miscon-
                                                                         netes manifests; (3) Terraform test files often contain multiple
figuration types that fall outside well-defined categories. These
                                                                         intentionally misconfigured resources, requiring selective re-
per-model differences underscore the importance of evaluating
                                                                         pair without disturbing others.
across multiple models rather than drawing conclusions from
a single LLM.
                                                                         6.4 RQ4: Cost-Effectiveness
6.3 RQ3: Cross-Technology Generalization                                 Motivation. Verification-guided repair requires multiple LLM
Motivation. To evaluate whether our findings generalize be-              invocations, increasing cost and latency. We quantify this
yond Terraform, we extend the benchmark with 20 Kubernetes               tradeoff using actual token counts and AWS Bedrock pricing
manifest items spanning 20 unique Checkov rules across six               (April 2026).
violation classes.                                                       Results. Table VII presents cost-effectiveness metrics. Mav-
Results. Table VI presents the Kubernetes results. Both com-             erick with verify-loop achieves 78.6% VFR at $0.002 per
mercial models (Sonnet and Opus) achieve 100% VFR across                 verified fix and 5.0s average latency. Opus without verification
all three methods, while Maverick achieves only 45% with                 achieves 61.4% at $0.029 per verified fix—nearly 12× more
plain prompting before verification-guided iteration rescues it          expensive per successful repair. This demonstrates that an
to 100%.                                                                 open-source model with verification produces more verified
This model-dependent disparity reveals that technology sim-              fixes per dollar than any commercial model configuration.
plicity alone does not guarantee repair success; model capa-             Sonnet verify-loop achieves comparable quality to Maverick
bility remains a factor. Notably, Maverick is the only model             (77.1% vs. 78.6%) but at 18× higher cost per fix ($0.044 vs.
to produce syntactically invalid output (V1=95% on Kuber-                $0.002) and 3.5× higher latency (17.6s vs. 5.0s).
TABLE VIII: Patch Minimality: Median Diff Ratio (Terra-
form)
    Model           Plain      Structured           Verify-loop
    Opus 4.6        0.227         0.067               0.152
    Sonnet 4.6      0.162         0.073               0.108
    Maverick        0.478         0.086               0.144
    Diff ratio = changed lines / original lines. Lower is more minimal.



6.5 RQ4b: Patch Minimality (V4)
Motivation. A correct repair that rewrites the entire file is less
desirable than a targeted, minimal patch. We analyze patch
minimality across methods and models using the diff ratio
(changed lines / original lines).                                         Figure 4: Terraform verify-loop: distribution of fixes by at-
Results. Table VIII presents median diff ratios for Terraform             tempt number. Most fixes occur in attempts 1–2; a third retry
repairs. Three patterns emerge. First, structured prompting               adds only 2 percentage points on average.
produces the most minimal patches (median 0.067–0.086)
across all models, likely because the JSON schema constraint
forces the model to articulate specific changes rather than               (CKV2 AWS 33) that checks cross-resource dependencies,
regenerating the entire file. Second, Maverick produces sub-              which no model resolves; (3) the remaining failures are model
stantially larger patches than the Claude models under plain              limitations where the LLM fails to produce a correct fix despite
prompting (median 0.478 vs. 0.162–0.227), suggesting that                 retries.
the open-source model is more prone to rewriting unrelated                Convergence. Figure 4 shows the distribution of fixes by
sections. Third, verify-loop patches are slightly larger than             attempt number for verify-loop on Terraform. Opus fixes 17
plain patches for Claude models (0.108–0.152 vs. 0.162–                   items on attempt 1 and 28 on attempt 2, with only 1 additional
0.227) because retry attempts sometimes modify additional                 fix on attempt 3. Sonnet and Maverick show similar patterns.
resources to satisfy verification. However, Maverick’s verify-            This suggests that two retries capture nearly all recoverable
loop patches (0.144) are substantially smaller than its plain             failures; a third retry adds only 2 percentage points on average.
patches (0.478), indicating that verification feedback helps the          Cases where plain outperforms verify-loop. Three Terraform
open-source model focus its repairs.                                      items are fixed by Sonnet’s plain prompting but not by its
This reveals a tradeoff: structured prompting optimizes for               verify-loop. In each case, the verification feedback from a
minimality but sacrifices correctness (32–42% VFR), while                 failed first attempt causes the model to overcorrect, producing
verify-loop optimizes for correctness (68–92% VFR) at the                 a different but still incorrect fix. This “retry confusion” effect is
cost of slightly larger patches. For practical deployment, cor-           a known limitation of iterative repair and occurs in 3/50 (6%)
rectness should take priority, but the minimality data suggests           of Sonnet’s items. The net effect remains strongly positive:
that combining structured output constraints with verification            verify-loop fixes 15 items that plain cannot, yielding a net
feedback could yield both minimal and correct repairs—a                   gain of +12 items.
direction for future work.                                                Cross-model agreement. Table IX presents the cross-model
                                                                          agreement analysis for verify-loop on Terraform. Of the 50
6.6 RQ5: Failure Analysis
                                                                          benchmark items, 30 (60%) are fixed by all three models
Motivation. Understanding where and why repairs fail is                   and 4 (8%) are fixed by none, yielding a full agreement rate
essential for improving both models and verification harnesses.           of 68%. The 7 items fixed exclusively by Opus represent
Results. We analyze failures across all Terraform verify-loop             its unique capability on harder items—these are not items
runs. Of the 50 benchmark items, 30 are fixed by all three                that Sonnet or Maverick fix with other methods, confirming
models, 4 are fixed by none, and 16 show model-dependent                  that Opus’s advantage is genuine rather than an artifact of
outcomes. The 16 model-dependent items produce 35 indi-                   method selection. Notably, zero items are fixed exclusively by
vidual model-item failures across the three models, which we              Sonnet or Maverick, indicating that the weaker models do not
categorize into three types:                                              possess unique repair capabilities absent in the stronger model.
Failure categorization. The author manually inspected all                 This asymmetry suggests that model capability determines the
35 verify-loop failures, examining the original artifact, the             ceiling of fixable items, while the verification loop determines
LLM’s repair attempts, and the Checkov output for each                    how close each model gets to its ceiling.
attempt. We identify three categories: (1) two items (BM-
0276, BM-0449) where the verification harness cannot isolate              7. D ISCUSSION
the target resource from pre-existing failures in multi-resource          We discuss four implications of our results.
files—these are harness limitations, not model failures; (2)              Verification matters more than model capability. The most
one item (BM-0040) involving a graph-based Checkov rule                   striking finding is that an open-source model with verification-
TABLE IX: Cross-Model Agreement on Verify-Loop (Terra-             as there are no other resources to miss. This technology-
form)                                                              dependent effect means that prompt engineering strategies
              Agreement Category         Items                     cannot be selected a priori without empirical verification—a
              All 3 models fix          30 (60%)                   conclusion enabled by the verification framework itself.
              2 of 3 models fix         9 (18%)                    Retry convergence and practical limits. Our convergence
              Opus only                 7 (14%)                    analysis shows that most verify-loop fixes occur on attempts
              Sonnet only                0 (0%)                    1–2, with a third attempt adding only 2 percentage points
              Maverick only              0 (0%)                    on average. Opus exhibits a distinctive pattern: 17 fixes on
              No model fixes             4 (8%)                    attempt 1 and 28 on attempt 2, suggesting that verification
              Full agreement rate         68%                      feedback is most valuable for the strongest model. Three items
                                                                   where Sonnet’s plain prompting succeeds but its verify-loop
                                                                   fails reveal a “retry confusion” effect: verification feedback
                                                                   from a failed first attempt occasionally causes the model to
guided repair (Maverick, 70% VFR) outperforms the strongest
                                                                   overcorrect. The net effect remains strongly positive (+12
commercial model without it (Opus plain, 46% VFR) at
                                                                   items for Sonnet), but practitioners should be aware that
roughly 8% of the cost per verified fix ($0.0024 vs. $0.0287).
                                                                   iterative repair is not universally superior on every individual
Even within the same model family, Opus plain (46%) barely
                                                                   item. Our convergence finding—diminishing returns after two
exceeds Sonnet plain (44%), while Opus verify-loop (92%)
                                                                   retries—corroborates Palavalli and Santolucito’s observation
dramatically outperforms Opus plain (46%)—a gap far larger
                                                                   that feedback effectiveness plateaus after approximately five
than the difference between models at the same method.
                                                                   iterations for CloudFormation generation [20], suggesting this
This suggests that for IaC repair, investing in verification
                                                                   is a general property of LLM feedback loops rather than an
infrastructure yields greater returns than upgrading to a more
                                                                   artifact of our framework.
capable model. For budget-constrained deployments, verify-
                                                                   Practical recommendations. Based on our results, we offer
loop enables smaller models to approach the quality of larger
                                                                   three deployment guidelines. (1) For Kubernetes with com-
models. For quality-critical deployments, verify-loop pushes
                                                                   mercial models, plain prompting with post-hoc verification is
top-tier models to 92% verified-fix rate.
                                                                   sufficient (100% VFR in our benchmark). (2) For Terraform
The structured prompting paradox. Contrary to the common           or open-source models, verification-guided iterative repair is
assumption that constraining LLM output to a structured            essential, as single-shot methods leave 50–68% of repairs
schema improves reliability [14], structured prompting consis-     unverified. (3) Two retries is the cost-effective sweet spot;
tently underperforms plain prompting on Terraform (32–42%          additional retries yield diminishing returns. In all cases, the
vs. 44–50%) and introduces regressions in 4–10% of cases.          verification harness should be integrated into CI/CD pipelines
We attribute this to two mechanisms. First, the JSON schema        as a mandatory gate before deploying LLM-generated repairs.
constraint forces the model to serialize the entire repaired       Our framework currently relies on a single scanner (Checkov);
file as a string value, increasing the likelihood of escaping      extending to multi-scanner consensus verification is a natural
errors and truncation. Second, providing the specific rule ID      next step that could further improve regression detection and
and affected resource causes the model to focus narrowly           reduce harness-specific false negatives.
on the target resource, missing other instances of the same
misconfiguration in multi-resource files.                          8. T HREATS TO VALIDITY
The minimality analysis (Section VI-D) adds nuance to this         Internal validity. Our verification harness relies on Checkov
finding: structured prompting produces the most minimal            as the sole scanner. Two benchmark items (BM-0276, BM-
patches (median diff ratio 0.067–0.086), suggesting that the       0449) produce false negatives in V2 because Checkov reports
JSON constraint successfully focuses the model’s edits but         the target rule as failed due to other resources in the same
at the cost of missing necessary changes elsewhere in the          file, not the repaired resource. Sensitivity analysis shows
file. This creates a correctness-minimality tradeoff: structured   that excluding these items raises Opus verify-loop from 92%
prompting is the best strategy for producing small, targeted       to 98%, confirming that our main findings are robust to
patches, but the worst for producing correct patches. Plain        this limitation. Additionally, one benchmark item (BM-0040)
prompting, unconstrained by output format, allows the model        involves a graph-based Checkov rule (CKV2 *) that checks
to make broader changes that are more likely to resolve the        cross-resource dependencies; no model resolves it, suggesting
target issue—even if the resulting patch is larger.                a fundamental limitation of single-resource repair prompting.
Notably, this effect reverses on Kubernetes: structured prompt-    Our results may also be sensitive to prompt wording; we use a
ing improves Maverick’s K8s performance from 45% to                single prompt template per strategy, and alternative phrasings
95%. We attribute this reversal to Kubernetes manifests’           could yield different fix rates.
simpler structure (flat YAML, single workload per file), which     Construct validity. The verified-fix rate treats V1–V3 as
eliminates the multi-resource problem that plagues Terraform       binary gates, which may not capture all dimensions of repair
repairs. In single-resource files, the narrow focus induced by     quality. In particular, V4 (minimality) is informational only—
structured prompting is not a liability—it is an advantage,        we do not penalize large patches that are otherwise correct. A
repair that rewrites an entire file to fix one attribute passes our   Three directions merit future investigation. First, extending the
gates but would be undesirable in practice. Human evaluation          verification harness to multi-scanner consensus (e.g., Checkov,
of repair intent preservation would complement our automated          KICS, and Terrascan jointly) could reduce scanner-specific
metrics and is a priority for future work.                            biases and improve regression detection. Second, human evalu-
External validity. Our benchmark of 70 items covers 70                ation of repair intent preservation would complement our auto-
unique Checkov rules across eight violation classes and two           mated metrics. Third, scaling the benchmark to additional IaC
technologies. The 630 total experimental runs across three            technologies (CloudFormation, Pulumi, Ansible) and sourcing
models, three methods, and two technologies provide sufficient        items from production repositories would strengthen external
statistical power to detect the observed effects (Cochran’s           validity.
Q p < 0.001 for all Terraform models). The benchmark                  The benchmark, verification harness, and all experimental arti-
is sourced from Checkov’s test suite rather than production           facts are available at https://github.com/[redacted-for-review].
repositories; while these artifacts represent realistic misconfig-
uration patterns [30], they may not capture the full complexity       ACKNOWLEDGMENT
of production IaC codebases. Our results are specific to
the model versions evaluated (April 2026); LLM capabilities           Portions of this work used AI-assisted tools (Anthropic
evolve rapidly, and future models may exhibit different repair        Claude, OpenAI ChatGPT) for grammar checking and La-
patterns. Extending the benchmark to additional technologies          TeX formatting during manuscript preparation. All framework
(CloudFormation, Pulumi, Ansible), sourcing items from pro-           design, Python implementation (approximately 1,200 lines),
duction repositories, and extending to multi-scanner verifica-        benchmark construction, experimental execution across 630
tion to reduce scanner-specific biases (Section VII) are planned      runs, statistical analysis, failure categorization, and engineer-
as future work.                                                       ing interpretations are solely the author’s work. No framework
Conclusion validity. We use temperature 0 for deterministic           code or experimental scripts were AI-generated. The author
outputs, making single runs per item sufficient for repro-            manually verified all results against raw experimental logs and
ducibility. All statistical comparisons use McNemar’s exact           takes full responsibility for the final content.
test with Bonferroni correction to control family-wise error
rate. Five of six pre-specified comparisons are significant           R EFERENCES
at the corrected threshold (α = 0.0083); the sixth (Sonnet
verify-loop vs. plain, p = 0.008) narrowly misses the strict           [1] Check Point Software Technologies, “2025 Cloud
Bonferroni threshold but is significant under the less conser-             Security    Report,”     2025.     [Online].    Available:
vative Holm-Bonferroni correction. All six comparisons are                 https://www.checkpoint.com/downloads/products/2025-
significant at uncorrected α = 0.05. Bootstrap confidence                  cloud-security-report.pdf
intervals are computed with a fixed seed for reproducibility.          [2] Palo Alto Networks, Unit 42, “Cloud Threat
                                                                           Report, Volume 7: Navigating the Expanding
                                                                           Attack     Surface,”     2024.     [Online].    Available:
9. C ONCLUSION
                                                                           https://www.paloaltonetworks.com/resources/research/unit-
We presented IaC-Guard-V, a verification-centered framework                42-cloud-threat-report-volume-7
for evaluating LLM-generated Infrastructure-as-Code repairs            [3] C. S. Xia and L. Zhang, “Keep the Conversation Going:
through three binary verification gates (syntactic validity,               Fixing 162 out of 337 Bugs for $0.42 Each using
target-issue resolution, regression safety) and one informa-               ChatGPT,” in Proc. ISSTA, 2024.
tional metric (patch minimality). We constructed a multi-              [4] C. Cheng, “Detect–Repair–Verify for LLM-Generated
technology benchmark of 70 misconfigured Terraform and                     Code: A Multi-Language, Multi-Granularity Empirical
Kubernetes artifacts spanning 70 unique scanner rules and                  Study,” arXiv:2603.23633, 2026.
eight violation classes, and conducted 630 experimental runs           [5] C. S. Xia, Y. Wei, and L. Zhang, “Practical Program Re-
across three LLM families and three repair strategies.                     pair in the Era of Large Pre-trained Language Models,”
Our results demonstrate that syntactic validity—the only di-               in Proc. ICSE, 2023.
mension visible without a verification harness—is a poor               [6] Q. Zhang, C. Fang, Y. Xie, Y. Ma, W. Sun, Y. Yang,
proxy for repair correctness: all models achieve 100% syntax               and Z. Chen, “A Systematic Literature Review on Large
validity, yet only 32–50% of repairs pass full verification                Language Models for Automated Program Repair,” ACM
under single-shot prompting. Verification-guided iterative re-             Trans. Softw. Eng. Methodol., 2026.
pair statistically significantly improves verified-fix rates to        [7] B. Yang, Z. Cai, F. Liu, B. Le, L. Zhang, T. F. Bissyandé,
68–92%, with the strongest configuration (Opus verify-loop)                Y. Liu, and H. Tian, “A Survey of LLM-based Automated
achieving 92% (95% CI: 84–98%). An open-source model                       Program Repair: Taxonomies, Design Paradigms, and
with verification outperforms the strongest commercial model               Applications,” arXiv:2506.23749, 2025.
without it at a fraction of the cost, establishing that verifi-        [8] C. S. Xia and L. Zhang, “Less Training, More Repairing
cation infrastructure matters more than model capability for               Please: Revisiting Automated Program Repair via Zero-
trustworthy IaC repair.                                                    shot Learning,” in Proc. ESEC/FSE, 2022.
 [9] A. Silva, S. Fang, and M. Monperrus, “RepairLLaMA:          [27] D. Kon, F. Zyuzin, N. Butakov, and A. Poddubny,
     Efficient Representations and Fine-Tuned Adapters for            “IaC-Eval: A Code Generation Benchmark for Cloud
     Program Repair,” IEEE Trans. Softw. Eng., 2025.                  Infrastructure-as-Code Programs,” in NeurIPS Datasets
[10] I. Bouzenia, P. Devanbu, and M. Pradel, “RepairAgent:            and Benchmarks, 2024.
     An Autonomous, LLM-Based Agent for Program Re-              [28] A. Rahman, S. I. Shamim, D. B. Bose, and R. Pandita,
     pair,” arXiv:2403.17134, 2024.                                   “Security Misconfigurations in Open Source Kubernetes
[11] T. Le-Cong, B. Le, and T. Murray, “Memory-Efficient              Manifests: An Empirical Study,” ACM Trans. Softw. Eng.
     Large Language Models for Program Repair with                    Methodol., 2023.
     Semantic-Guided Patch Generation,” in Proc. ICSE,           [29] H. Tang, K. Hu, J. P. Zhou, S. Zhong, W.-L. Zheng,
     2026.                                                            X. Si, and K. Ellis, “Code Repair with LLMs gives
[12] X. Chen, M. Lin, N. Schärli, and D. Zhou, “Teaching             an Exploration-Exploitation Tradeoff,” in Proc. NeurIPS,
     Large Language Models to Self-Debug,” in Proc. ICLR,             2024.
     2024.                                                       [30] Datadog, “State of Cloud Security 2025,” 2025. [On-
[13] A. Madaan et al., “Self-Refine: Iterative Refinement with        line]. Available: https://www.datadoghq.com/blog/cloud-
     Self-Feedback,” in Proc. NeurIPS, 2023.                          security-study-learnings-2025/
[14] J. Wei et al., “Chain-of-Thought Prompting Elicits Rea-     [31] W. Hummer, F. Rosenberg, F. Oliveira, and T. Eilam,
     soning in Large Language Models,” in Proc. NeurIPS,              “Testing Idempotence for Infrastructure as Code,” in
     2022.                                                            Proc. Middleware, 2013.
[15] P. Jana, S. Davidson, B. Bhasker, A. Kan, A. Deoras, and
     L. Callot, “TerraFormer: Automated Infrastructure-as-
     Code with LLMs Fine-Tuned via Policy-Guided Verifier
     Feedback,” in Proc. ICSE-SEIP, 2026.
[16] N. Saavedra, J. F. Ferreira, and A. Mendes, “InfraFix:
     Technology-Agnostic Repair of Infrastructure as Code,”
     in Proc. ISSTA, 2025.
[17] E. Malul, Y. Meidan, D. Mimran, Y. Elovici, and A.
     Shabtai, “GenKubeSec: LLM-Based Kubernetes Mis-
     configuration Detection, Localization, Reasoning, and
     Remediation,” in Proc. ACSAC, 2024.
[18] Z. Ye, T. H. M. Le, and M. A. Babar, “LLMSecConfig:
     An LLM-Based Approach for Fixing Software Container
     Misconfigurations,” arXiv:2502.02009, 2025.
[19] T. Sun et al., “Fail, Learn, Refine, and Suc-
     ceed through LLM-Empowered DevOps Simulation,”
     arXiv:2506.05623, 2025.
[20] M. A. Palavalli and M. Santolucito, “Using a Feedback
     Loop for LLM-based Infrastructure as Code Generation,”
     arXiv:2411.19043, 2024.
[21] A. Rahman, C. Parnin, and L. Williams, “The Seven
     Sins: Security Smells in Infrastructure as Code Scripts,”
     in Proc. ICSE, 2019.
[22] T. Sharma, M. Fragkoulis, and D. Spinellis, “Does Your
     Configuration Code Smell?,” in Proc. MSR, 2016.
[23] N. Saavedra and J. F. Ferreira, “GLITCH: Automated
     Polyglot Security Smell Detection in Infrastructure as
     Code,” in Proc. ASE, 2022.
[24] S. Dalla Palma, D. Di Nucci, F. Palomba, and D.
     A. Tamburri, “Within-Project Defect Prediction of
     Infrastructure-as-Code Using Product and Process Met-
     rics,” IEEE Trans. Softw. Eng., vol. 48, no. 6, 2022.
[25] A. Verdet, M. Hamdaqa, L. Da Silva, and F. Khomh,
     “Assessing the Adoption of Security Policies by Devel-
     opers in Terraform Across Different Cloud Providers,”
     Empirical Softw. Eng., 2025.
[26] A. Steffens, J. Schwarz, and H. Lichter, “Code Smells in
     Infrastructure as Code,” in Proc. QUATIC, 2018.
