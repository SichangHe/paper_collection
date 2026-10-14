                                         Security Tests as Executable Specifications for LLM Code
                                         Generation:
                                         Benefits, Trade-offs, and Coverage Limits
                                         YUNHAO LIANG, Chengdu Institute of Computer Applications, Chinese Academy of Sciences and
                                         University of Chinese Academy of Sciences, China
                                         CHENGGUANG GAN, Independent Researcher, Japan
                                         RUIXUAN YING, Institute of Multidisciplinary Research for Advanced Materials (IMRAM), Tohoku
                                         University, Japan
                                         HANJUN WEI, University of Chinese Academy of Sciences, China
                                         ZHE CUI, Chengdu Institute of Computer Applications, Chinese Academy of Sciences and University of
                                         Chinese Academy of Sciences, China
                                         SHIWEN NI, Artificial Intelligence Research Institute, Shenzhen University of Advanced Technology, China
arXiv:2608.09740v2 [cs.SE] 11 Aug 2026




                                         Large language models can generate functionally useful code that remains vulnerable, while security-oriented
                                         interventions can make code appear safe by breaking its intended behavior. We study a different intervention
                                         point: using security tests as executable specifications before generation and as feedback during repair. We
                                         develop SecTDD, a controlled test-feedback scaffold that separates three decisions often conflated in prior
                                         work: whether tests are shown upfront, whether failed executions trigger revision, and how failures are
                                         selected and represented. The evaluation uses behavior-partitioned visible and hidden tests and byte-identical
                                         initial candidates for repair comparisons.
                                            Across 2,705 trajectories, 31 task instances, three secure-code benchmarks, 16 CWE categories, and two
                                         model families, showing all visible tests upfront changes hidden functional-and-security joint success by
                                         +19.3 percentage points on average, but helps only 7 of nine benchmark–model conditions and hurts 2.
                                         In shared-candidate comparisons, structured feedback repairs 80 initially unsuccessful candidates with 0
                                         joint regressions; fixed raw feedback repairs 83 but regresses 3. Yet structured and raw feedback are nearly
                                         indistinguishable head-to-head (6 wins, 6 losses, 453 ties). Candidates that pass all visible tests still fail hidden
                                         behavior families under every common regime. These findings support a mechanism-level conclusion rather
                                         than a winner claim: executable feedback can repair secure-code generation across model families, but its
                                         opportunity is bounded by test coverage, and its effect depends on the model, task, and feedback entry point.
                                         We release prompts, partitioned oracles, sandbox runners, complete trajectories, and frozen analysis manifests.
                                         Additional Key Words and Phrases: secure code generation, large language models, test feedback, software
                                         testing, program repair, empirical study

                                         1   Introduction
                                         Code generation is useful only when the generated program both implements its requirement
                                         and resists the relevant attacks. These goals are not interchangeable. A candidate that omits
                                         dangerous behavior can look secure while being useless; a candidate that passes ordinary unit
                                         tests can still contain command injection, path traversal, or improper certificate validation. Recent
                                         secure-code benchmarks therefore advocate evaluating functionality and security on the same
                                         candidate [4, 8, 21]. Nevertheless, most defenses are still presented as model-training, constrained-
                                         decoding, static-analysis, or prompt-optimization techniques [9, 10, 17, 19]. Less is known about a

                                         Authors’ Contact Information: Yunhao Liang, Chengdu Institute of Computer Applications, Chinese Academy of Sciences
                                         and University of Chinese Academy of Sciences, China; Chengguang Gan, Independent Researcher, Japan; Ruixuan Ying,
                                         Institute of Multidisciplinary Research for Advanced Materials (IMRAM), Tohoku University, Japan; Hanjun Wei, University
                                         of Chinese Academy of Sciences, China; Zhe Cui, Chengdu Institute of Computer Applications, Chinese Academy of Sciences
                                         and University of Chinese Academy of Sciences, China; Shiwen Ni, Artificial Intelligence Research Institute, Shenzhen
                                         University of Advanced Technology, China.


                                                                                                           , Vol. 1, No. 1, Article . Publication date: August 2027.
2                                    Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


mechanism already familiar to developers: executing security tests during generation and returning
failures to the model.
   Tests can affect generation in at least three distinct ways. First, test code can be an upfront
executable specification, exposing examples and security properties before a candidate exists. Second,
test execution can create a feedback loop that revises an existing candidate. Third, an orchestrator
can select and represent failures—for example, sending all raw logs or prioritizing a compact security
failure. Prior studies of self-debugging and patch validation show that execution feedback can
improve functional generation and vulnerability repair [3, 13, 14]. However, a secure-generation
claim requires stricter controls. If two methods generate different initial programs, an observed
difference cannot be attributed to repair. If stopping uses hidden tests, the evaluation leaks its oracle.
If visible and hidden tests exercise the same inputs, a reported gain may be test memorization.
Finally, reporting security independently from functionality can reward empty or broken programs.
   This paper presents a controlled empirical study of security tests at generation time. We build
SecTDD, a test-feedback scaffold, not as another universally superior prompting recipe, but as an
instrument for separating the effects above. It runs candidate code in a sandbox, observes only
a visible behavior partition, and performs at most two revisions. Fixed raw, random raw, and
structured security-priority feedback reuse the exact initial response produced by the requirement-
only condition. A second feedback condition similarly reuses the candidate generated with all
visible tests upfront. Hidden functional and security tests run once, after stopping, and never enter
a prompt or decision.
   We evaluate SecTDD on audited subsets of CWEval [21], SALLM [26], and CodeGuard+ [8].
The primary evidence contains 2,705 trajectories over 31 benchmark task instances and 16 CWE
categories. It spans four local Qwen configurations from 7B to 32B and the remotely served
DeepSeek-V4-Flash model, with five repetitions per condition. For external tasks whose original
repositories did not provide the required partitioned dynamic oracle, we construct an overlay using
a secure implementation, a functionality-preserving vulnerable mutant, repeat execution, behavior-
family separation, and blinded machine semantic review. After the executable gates and three-repeat
stability checks passed, three software-engineering doctoral students manually reviewed the frozen
qualification packets. We therefore treat these external overlays as human-reviewed while retaining
machine-assisted construction as a limitation.
   The results complicate a simple “more tests are better” story. All tests upfront improve the
benchmark–model macro average by 19.3 percentage points, but the direction is negative on
Qwen2.5-Coder-7B-Instruct/SALLM and DeepSeek-V4-Flash/CodeGuard+. Shared-candidate feed-
back provides stronger causal evidence: structured feedback repairs 80 failures with no joint
regression, while fixed raw feedback repairs 83 with three. Yet the structured strategy does not
dominate raw feedback: across 465 paired cells, each wins six times. The breadth CodeGuard+
wave further shows why pilot effects can shrink. On 11 tasks selected without looking at baseline
outcomes, feedback triggers in only 21 of 110 B0 cells and produces four repairs; a strong candidate
that already passes visible tests offers no feedback opportunity even when it fails a hidden attack
family.
   This work makes four contributions:

• A controlled decomposition of upfront tests, executable feedback, and feedback representation
  for secure code generation, including shared-initial-candidate comparisons.
• A multi-benchmark, cross-family study comprising 2,705 trajectories, with functionality and
  dynamic security evaluated jointly on hidden behavior partitions.
• Mechanism-oriented measurements—repair/regression transitions and test-feedback overfitting—
  that explain when aggregate success rates rise or fall.

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                               3

• A reproducibility package containing frozen prompts, model/configuration manifests, qualified
  oracles, sandbox executions, raw model responses, and analysis scripts.
   Our conclusion is deliberately scoped: test feedback improves secure code generation by repairing
a subset of failed candidates and makes the security–functionality trade-off observable; no tested
feedback representation is best in all settings.

2     Background and Motivation
2.1 Joint secure-code evaluation
Let 𝐹 (𝑐) denote that candidate 𝑐 passes all functional tests and 𝑆 (𝑐) that it passes all security tests.
The useful outcome is 𝐽 (𝑐) = 𝐹 (𝑐) ∧ 𝑆 (𝑐). Reporting only 𝑆 is unsafe as an evaluation practice: a
program that returns a constant or deletes the requested operation may never reach a vulnerable
sink. Reporting only 𝐹 misses vulnerability-specific behavior. CodeGuard+ introduced metrics that
combine these dimensions [8]; CWEval uses outcome-driven functional and security oracles [21];
and Dai et al. show that several apparent security improvements disappear when both properties
are checked on the same output [4].
   The strict conjunction is appropriate for deployability but hides partial functional progress. We
therefore retain it as the primary outcome and report SAFE@1 as a sensitivity measure. SAFE
weights security by an exponential transform of the functional test-case pass fraction [4]. In our
adaptation, “secure” means passing all task-specific dynamic security tests rather than receiving
no warning from a collection of static analyzers. This difference matters and prevents a direct
numerical comparison with the original SAFE study.

2.2    Tests as specifications and feedback
Test-driven development treats executable examples as a way to clarify intended behavior before
implementation [1]. For an LLM, visible tests can likewise reduce ambiguity. Yet test source also
consumes context, can anchor a model on particular values, and can shift attention from the prose
contract. Upfront tests thus change the generation distribution; they do not demonstrate that a
particular candidate was repaired.
   Execution feedback is a different intervention. Self-debugging and CodeRL use test outcomes to
guide additional generation [3, 14]; vulnerability-repair systems return compiler, functional, and
sanitizer output [13]; secure-generation systems may loop over static analysis or fuzzing [17, 19].
The result depends on what the oracle exposes. A feedback loop cannot react when every visible
test passes, even if a hidden property fails. This creates a coverage-limited treatment opportunity
that aggregate final scores alone do not show.

2.3    The causal ambiguity of iterative generation
Suppose method 𝐴 prompts a model once and method 𝐵 prompts it with tests, executes the output,
and repairs it. If their initial outputs differ, the final contrast mixes prompt effects and repair effects.
We avoid this ambiguity for the principal feedback comparisons: B4, B5, and M load the serialized B0
response rather than regenerating it; B6 similarly loads B3. Model, task, repetition, initial code, and
initial usage accounting are therefore paired. Only the repair policy differs. B3 versus B0 remains
useful, but we interpret it as a benchmark–model condition contrast, not an edit-level causal effect.

3     SecTDD Experimental Scaffold
Figure 1 shows the workflow. A task provides a natural-language contract and a behavior-partitioned
oracle. The method controls what is placed in the first prompt. The candidate runs against visible
functional and security cases in a fresh sandbox. If the method permits feedback and a visible

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
4                                           Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


         Task
                                   Initial context                          LLM            Visible sandbox pass / stop     Freeze
      contract and
                                requirement ± visible tests             candidate                𝐹 vis , 𝑆 vis           final candidate
      visible oracle

                                                                                                   fail + budget                    run once


                   Shared round-0 response. B4/B5/M load the byte-                  Failure feedback                Hidden sandbox
                   identical B0 response; B6 loads B3 before the feedback            fixed raw / random
                                                                                       raw / structured              final evaluation only
                   branch.
                                                                                       replace candidate
                                                                                    at most two revisions

                                                                                                                   Hidden outcomes
                                                                                                                          𝐹 hid , 𝑆 hid , 𝐽



Fig. 1. Controlled SecTDD workflow. Generation and revision observe only the visible partition. Hidden tests
run once on the frozen candidate and never affect prompting, feedback, or stopping. The shared-response
pairing isolates repair effects from differences in initial generation.


case fails, the orchestrator constructs a bounded message and requests a complete replacement
module. Stopping depends only on visible results and frozen resource limits. The hidden partition
is mounted only for final evaluation.

3.1     Feedback policies
The structured policy first prioritizes failing security cases, then cases not previously selected, and
finally a stable case identifier. At most two failures are returned per round. Each block contains
the case identifier, marker (functional or security), an executable-property description, and the tail
of the observed failure. Fixed raw feedback returns all failing logs in stable order. Random raw
feedback returns one failure selected deterministically from the repetition identifier and round. All
policies request one complete Python module; none reveal hidden inputs or results.
   This design is intentionally modest. It tests whether selection and representation matter under a
small, auditable budget. It does not claim that the fixed priority is an optimal scheduler. Indeed,
the head-to-head results later show that representation effects are sparse relative to the effect of
receiving any executable failure.

3.2     Methods and controlled contrasts
Table 1 defines the method family. Not every benchmark includes every diagnostic baseline. B1
and B2 appear only in CWEval; B5 appears in CWEval and the CodeGuard+ breadth wave; B6
appears on the external benchmarks. In the final operational protocol, B6 means “B3 plus structured
feedback.” This supersedes an early living-protocol label that used B6 for a static-tool loop.
   The principal controlled contrasts are B4−B0 and M−B0 (does feedback repair a requirement-
only candidate?), B6−B3 (does feedback repair an upfront-test candidate?), and M−B4/B5 (does
structured selection outperform raw feedback?). B3−B0 addresses the separate question of upfront
specification.
   Comparison scope. Training-time defenses such as SVEN and SafeCoder and decoder-specific
defenses such as CodeGuard+ cannot be applied uniformly to the local and API checkpoints in our
grid [8–10]. Reimplementing them for only a subset would mix model and intervention effects.
We therefore compare inference-time policies that operate through the same model interface and
explicitly do not claim to outperform those systems. Their published findings motivate our joint
evaluation; our question is orthogonal: under a fixed generator and executable oracle, what comes
from test availability and feedback?

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                               5

Table 1. Experimental methods. M denotes the structured SecTDD policy. Iterative methods permit at most
two revisions; “Reused from” identifies the condition supplying the byte-identical round-0 response.


         ID    Initial context                          Feedback                              Reused from
         B0 Requirement                     None                                              –
         B1 Requirement + reminder          None                                              –
         B2 Requirement + functional tests None                                               –
         B3 Requirement + all visible tests None                                              –
         B4 Requirement                     All raw failures, fixed order                     B0
         B5 Requirement                     One random raw failure                            B0
         M Requirement                      Structured security priority                      B0
         B6 Requirement + all visible tests Structured security priority                      B3


4     Study Design
We organize the study around five research questions:
RQ1     How do visible security tests used as upfront specifications affect hidden joint success?
RQ2     Can executable feedback repair failed initial candidates without regressing functionality
        or security?
RQ3     Does structured security-priority feedback improve over raw feedback under shared initial
        candidates?
RQ4     How often does visible joint success fail to transfer to hidden behavior families?
RQ5     Which findings reproduce across benchmarks and model families?

4.1    Benchmarks and task selection
   CWEval. CWEval provides multilingual security-critical generation tasks and outcome-driven
functional/security evaluation [21]. We use nine Python tasks spanning eight CWE categories.
These tasks participated in method development, so we label CWEval internal confirmatory evidence
rather than an untouched external test set.
  SALLM.. SALLM contains security-centric Python prompts derived from author examples, Stack
Overflow, and CodeQL patterns [26]. Eleven tasks, each from a different CWE category, pass our
executable-oracle qualification. SALLM is external to method development.
   CodeGuard+. CodeGuard+ was designed to evaluate correctness and security jointly [8]. Docker
was unavailable in our execution environment, so we built a Python-only, Bubblewrap-based [7]
oracle overlay. The primary breadth wave is the union of tasks accepted by four frozen semantic
panels: 11 tasks across eight CWE categories. Crucially, it does not require a baseline security
failure, a feedback trigger, or a pilot repair. This removes the outcome-selection filter present in an
earlier three-task technical pilot, which we exclude from primary aggregates.
   Across benchmarks there are 31 task instances and 16 distinct CWE identifiers from the MITRE
taxonomy [16]. Overlap in CWE number does not imply duplicate behavior: benchmark contracts
and implementations remain separate.

4.2    Oracle construction and qualification
Each task has visible and hidden functional and security partitions. We split by behavior family or
attack mechanism rather than randomly splitting individual assertions. A hidden case may preserve
the security property while changing delimiters, encodings, nesting, boundary values, or attack

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
6                                    Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


construction. The hidden source, concrete inputs, expected outputs, and logs are unavailable to the
generation process.
  For SALLM and CodeGuard+ overlays, qualification has six gates:

(1) A secure implementation must pass all functional and security cases.
(2) A vulnerability mutant must preserve functionality and fail at least one security case.
(3) Both subjects run three times in independent fresh sandboxes; every observation must be stable.
(4) Visible and hidden partitions must represent the declared behavior families without sharing
    concrete hidden material.
(5) Blinded semantic-review packets contain the contract, implementations, and partition descrip-
    tions but hide task provenance and construction labels. Two strong models review each packet;
    disagreements receive a third-model adjudication.
(6) After the executable and machine-review gates pass, three software-engineering doctoral
    students manually review each frozen packet for contract–oracle agreement, the semantics of
    the secure implementation and vulnerable mutant, attack realism, and visible/hidden partition
    separation.

   Strong models and the DeepSeek-V4-Flash API were also used to generate multiple candidate
secure implementations during oracle construction. Candidates were accepted only by executable
gates, not by model self-assertion. The use of generative AI in data/oracle construction is therefore
part of the research method and is disclosed here. Model review served as a qualification aid rather
than the sole semantic authority: after the executable gates and three-repeat stability checks, three
software-engineering doctoral students manually reviewed every frozen SALLM and CodeGuard+
qualification packet. We therefore describe these overlays as human-reviewed, while carrying the
limitations of machine-assisted construction through the paper.


4.3    Models and generation
Table 2 reports the exact model identifiers and complete primary grid. The local checkpoints are
Qwen2.5-Coder-7B-Instruct and Qwen2.5-Coder-14B-Instruct [12], Qwen3-32B [27], and Qwen3.6-
27B [23]. All run in BF16 with single-GPU inference. Thinking is disabled for Qwen3-32B and
Qwen3.6-27B to keep code emission within the common budget. The cross-family conditions use the
official API model DeepSeek-V4-Flash (provider identifier in Table 2); thinking is explicitly disabled
in every request. DeepSeek reports 284B total and 13B active parameters for V4-Flash, while the
provider-managed server revision is not exposed [5]. We therefore archive raw responses, request
dates, usage, the provider identifier, and request slots instead of claiming bitwise reproducibility
for the API condition.
   Temperature is 0.2. CWEval permits 2,048 completion tokens per call; external experiments
permit 3,072. Iterative methods make at most three calls, use at most 1,200 feedback tokens total
(600 per round), and stop when all visible tests pass or a call, token, execution, or timeout budget
is reached. CWEval has a 12,000-input/6,144-output-token total budget and at most 20 visible
executions; the external grids use 14,000/9,216 tokens and at most six visible executions. These
limits were frozen before each confirmatory wave.
   Local repetitions use five fixed generation seeds. The DeepSeek-V4-Flash endpoint did not
support deterministic seeds: its five identifiers denote independent request slots and pairing keys
and were not sent as provider seeds. B4/B5/M still reuse the exact B0 response, and B6 the exact B3
response, within each slot.


, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                               7

Table 2. Models and primary evidence grid. Panel A maps compact model keys to official identifiers and
execution modes; Panel B enumerates the primary evaluation grid. Meth. denotes methods, Rep. denotes fixed
seeds for local checkpoints and independent request slots for the remote API, and Traj. denotes trajectories.
Repeated benchmark tasks and task–repetition cells are not independent inference units.

      Panel A: Model registry
             Key            Official model or API identifier                 Execution
             Q2.5-C7B       Qwen/Qwen2.5-Coder-7B-Instruct                   Local, BF16
             Q2.5-C14B      Qwen/Qwen2.5-Coder-14B-Instruct                  Local, BF16
             Q3-32B         Qwen/Qwen3-32B                                   Local, BF16, no-thinking
             Q3.6-27B       Qwen/Qwen3.6-27B                                 Local, BF16, no-thinking
             DS-V4-F        DeepSeek-V4-Flash (deepseek-v4-flash)            API, no-thinking

      Panel B: Primary evaluation grid

       Benchmark                  Model key               Tasks         Meth.            Rep.          Traj.
       CWEval                     Q2.5-C7B                       9               7             5          315
       CWEval                     Q2.5-C14B                      9               7             5          315
       CWEval                     Q3-32B                         9               7             5          315
       SALLM                      Q2.5-C7B                      11               5             5          275
       SALLM                      Q2.5-C14B                     11               5             5          275
       SALLM                      Q3.6-27B                      11               5             5          275
       SALLM                      DS-V4-F                       11               5             5          275
       CodeGuard+                 Q2.5-C14B                     11               6             5          330
       CodeGuard+                 DS-V4-F                       11               6             5          330
                                                                                       Total           2,705


4.4    Outcomes
For task 𝑥, repetition 𝑟 , and final candidate 𝑐 𝑥𝑟 , the primary metric is
                                                𝑁 𝑅
                                            1 ∑︁ ∑︁  ℎ𝑖𝑑                          
                              HSP@1 =                   ⊮ 𝐹 (𝑐 𝑥𝑟 ) ∧ 𝑆 ℎ𝑖𝑑 (𝑐 𝑥𝑟 ) .                                 (1)
                                           𝑁 𝑅 𝑥=1 𝑟 =1

We call it Hidden Secure-Pass@1 in prose. We additionally report Hidden Func@1, Hidden Secure@1,
security-given-functional 𝑃 (𝑆 ℎ𝑖𝑑 = 1 | 𝐹 ℎ𝑖𝑑 = 1), SAFE@1, and the four states 𝐹 +𝑆 + , 𝐹 +𝑆 − , 𝐹 − 𝑆 + ,
and 𝐹 − 𝑆 − . Security alone is never used as the headline result.
   For feedback, we count a trigger when an iterative condition makes at least one revision, a joint
repair when its shared initial candidate fails hidden joint evaluation and its final candidate passes,
and a joint regression for the reverse transition. We separately count functionality regressions and
function-preserving security repairs (𝐹 +𝑆 − → 𝐹 +𝑆 + ).

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
8                                    Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


Table 3. Hidden Secure-Pass@1 (%) by benchmark, model key, and method. Model keys are defined in Table 2;
dashes denote methods not run on that benchmark.


    Benchmark             Model key              B0         B1          B2      B3           B4   B5    M      B6
    CWEval                Q2.5-C7B             15.6 22.2               33.3   40.0      48.9 46.7      48.9      –
    CWEval                Q2.5-C14B            28.9 44.4               37.8   57.8      57.8 48.9      53.3      –
    CWEval                Q3-32B               22.2 11.1               33.3   73.3      62.2 57.8      62.2      –
    SALLM                 Q2.5-C7B             45.5    –                  –   41.8      60.0    –      63.6   58.2
    SALLM                 Q2.5-C14B            54.5    –                  –   63.6      70.9    –      70.9   72.7
    SALLM                 Q3.6-27B             60.0    –                  –   90.9      69.1    –      69.1   90.9
    SALLM                 DS-V4-F              52.7    –                  –   81.8      67.3    –      67.3   87.3
    CodeGuard+            Q2.5-C14B            76.4    –                  –   87.3      78.2 78.2      78.2   89.1
    CodeGuard+            DS-V4-F              89.1    –                  –   81.8      94.5 94.5      94.5   81.8


    To quantify coverage-limited stopping, we define the test-feedback overfitting rate:
                                                  Í           𝑣𝑖𝑠 (𝑐
                                                                   𝑥𝑟 ) ∧ ¬𝐽
                                                                               ℎ𝑖𝑑 (𝑐 )]
                                                    𝑥,𝑟 ⊮[𝐽                          𝑥𝑟
                                      TFOR =                Í         𝑣𝑖𝑠 (𝑐 )]
                                                                                         .                       (2)
                                                              𝑥,𝑟 ⊮[𝐽       𝑥𝑟

TFOR is an operational diagnostic for this study, not a claim that no equivalent generalization
metric exists. We report its numerator and denominator because a small denominator makes the
rate unstable.

4.5    Statistical analysis and integrity checks
The task is the inference unit; the 2,705 trajectories are repeated observations, not independent
samples. We compute method rates over task–repetition cells and 95% confidence intervals using
10,000 task-cluster bootstrap resamples [6]. Confirmatory method differences use exact sign-
flip permutation tests over task-level mean differences and Holm correction within each frozen
comparison family [11]. Given the small task sets, we emphasize effect sizes and paired events. The
smallest adjusted 𝑝 in component reports is 0.125; no comparison reaches 0.05.
   Every run manifest records task, model, method, repetition, budgets, prompt and oracle hashes,
candidate hashes, token usage, and execution results. Analysis aborts on a missing grid cell, model
mismatch, hash drift, or unexpected trajectory count. A hidden-leak audit scans prompts and
feedback for hidden identifiers, descriptions, and non-public string literals. Code runs without
network access in a fresh minimal mount with per-test and wall-clock timeouts.

5     Results
Table 3 gives the principal outcome for every condition. Percentages are deliberately not pooled
across heterogeneous benchmark grids.

5.1    RQ1: Upfront tests are helpful, but not monotonic
B3 exceeds B0 in seven of nine benchmark–model conditions and is worse in two. The unweighted
benchmark–model macro difference is +19.3 percentage points. The largest improvements occur on

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                               9

Table 4. Paired feedback transitions over shared initial candidates. Task–rep. cells are repeated observations,
not independent inference units. Repair denotes hidden joint failure → success; Trig. denotes at least one
revision; J.Reg./F.Reg. denote hidden joint/function regression; Sec.-only denotes 𝐹 +𝑆 − → 𝐹 +𝑆 + .


                Comparison        Task–rep.      Trig.    Repair       J.Reg.   F.Reg.    Sec.-only
                B4 − B0                   465      252         83          3        15             45
                M − B0                    465      252         80          0         8             40
                B6 − B3                   330       47         18          0         0              2
                M − B4                    465      252          6          6         8              0



CWEval/Qwen3-32B (22.2% to 73.3%), SALLM/Qwen3.6-27B (60.0% to 90.9%), and SALLM/DeepSeek-
V4-Flash (52.7% to 81.8%). These results support the idea that visible tests can convey security-
relevant semantics more concretely than prose alone.
   The exceptions reveal the risk. On SALLM/Qwen2.5-Coder-7B-Instruct, B3 falls from 45.5%
to 41.8%, driven by a secure-rate reduction from 74.5% to 56.4% even as functionality rises. On
CodeGuard+/DeepSeek-V4-Flash, B3 falls from 89.1% to 81.8%. In the latter condition, the all-tests
prompt produces five 𝐹 +𝑆 − cells and a TFOR of 18.2%, versus two 𝐹 +𝑆 − cells and 0% TFOR for
B0. A post-hoc CWE-89 example is especially instructive: the B3 candidate passes the complete
visible partition but fails the hidden data-integrity behavior, while the same-slot B0 candidate
passes hidden joint evaluation. Because the candidates are independently generated, this example
illustrates a prompt-distribution effect rather than a code edit.
   B1 and B2 on CWEval further argue against a universal prompt heuristic. A generic security
reminder improves Qwen2.5-Coder-14B-Instruct from 28.9% to 44.4% but harms Qwen3-32B from
22.2% to 11.1%. Functional tests alone improve all three CWEval models over B0, yet remain below
all-tests B3. Thus, executable security examples often add useful information, but model capacity
and attention allocation determine whether that information is used safely.
 Answer to RQ1. Upfront visible tests usually improve hidden joint success (7/9 conditions;
 +19.3 points macro), but can reduce it. They are a model-dependent specification mechanism,
 not a monotonic safety intervention.

5.2   RQ2: Feedback repairs shared candidates
Table 4 aggregates only comparisons with shared initial responses. M triggers on 252 of 465 B0
cells and turns 80 hidden joint failures into successes, with no joint regression. Forty of those
are function-preserving security repairs. Fixed raw feedback produces 83 repairs and three joint
regressions. B6 triggers less often—47 of 330 B3 cells—but repairs 18 and has no joint regression. It
does incur one security regression that does not cross from joint success to joint failure because
the B3 reference was not jointly successful.
   The opportunity differs sharply by benchmark. On internal CWEval, M triggers 113/135 cells and
repairs 44, including 38 security-only failures, but also causes eight functionality regressions relative
to B0. Because none of the regressed B0 candidates were hidden joint successes, the aggregate
joint-regression count remains zero; the four-state decomposition is what exposes the trade-off.
On SALLM, M triggers 118/220 and repairs 32 without a functionality regression. On outcome-
unfiltered CodeGuard+, it triggers only 21/110 and repairs four. This shrinkage from internal to
breadth evidence is not a contradiction: many CodeGuard+ candidates already pass the visible
partition, so the feedback treatment is never delivered.

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
10                                   Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


   A representative CWEval CWE-79 trajectory begins at 𝐹 +𝑆 − : the code implements the required
rendering but fails hidden HTML entity and attribute-delimiter behaviors. One structured visible
failure causes a second candidate that retains functionality and passes all hidden security cases.
A cross-family SALLM CWE-327 trajectory begins at 𝐹 − 𝑆 − and fails rejection of MD5 and a
mismatching SHA-256 digest; one B6 revision reaches 𝐹 +𝑆 + . Hidden behavior labels are used only
in this post-hoc explanation, not in feedback.
   Costs track treatment delivery. Relative to their shared reference, B4 uses 0.81 additional calls
and about 178 feedback tokens per eligible cell on average; M uses 0.80 calls and 202 tokens; B6
uses 0.24 calls and 49 tokens because B3 more often passes visibly. Feedback therefore buys repairs
at non-trivial but bounded inference cost.
 Answer to RQ2. Executable feedback can causally repair a subset of failed shared candidates
 across all three benchmarks and both model families. It also exposes lower-level functional-
 ity/security regressions that a single joint score can hide.


5.3    RQ3: Structure does not universally beat raw logs
M and B4 share 465 initial candidates and differ only in failure selection/representation. M wins
six cells, B4 wins six, and 453 tie. The wins and losses concentrate in CWEval and SALLM; all 110
CodeGuard+ cells tie. Aggregate repair counts slightly favor raw feedback (83 versus 80), while
joint regressions favor structured feedback (zero versus three). These differences are too sparse to
support a universal ranking.
   The qualitative failures explain why. In one SALLM CWE-22 slot, fixed raw feedback reaches
𝐹 +𝑆 + after one revision. Structured feedback continues to a third round and ends at 𝐹 − 𝑆 + , failing
hidden nested-file deletion. Prioritizing security reduced the immediate vulnerability signal but
did not preserve the complete functional contract. Conversely, structured selection can avoid
overwhelming the prompt when many raw failures are redundant. Which behavior dominates
depends on the failure set and model.
   In the CodeGuard+ breadth wave, B4, B5, and M have identical joint outcomes for both models:
78.2% on Qwen2.5-Coder-14B-Instruct and 94.5% on DeepSeek-V4-Flash. They also make the same
repair transitions. This equality is substantive: a complex representation policy has no room to
differentiate when few failures trigger and the selected messages lead to the same code-level
correction.
 Answer to RQ3. We find no outcome-level superiority for structured feedback over raw
 feedback. The robust effect belongs to receiving executable feedback; representation effects are
 conditional and sparse.


5.4    RQ4: Visible success leaves a coverage gap
Table 5 computes TFOR for the four methods available on every primary benchmark grid. Between
5.6% and 18.8% of visible-joint candidates fail hidden joint evaluation. B3 has the largest pooled rate
despite strong final success in several conditions. This does not mean B3 is always worse: TFOR is
conditional on visible success and should be read beside overall Hidden Secure-Pass@1.
   The failure occurs under every common regime. For example, a CWEval URL-validation candidate
passes all visible checks but fails hidden deep-subdomain, authority-userinfo, and encoded-delimiter
families. More importantly for iteration, DeepSeek-V4-Flash/CodeGuard+ B6 makes no revision in
any of 55 cells: its B3 candidates all pass the visible partition, yet five fail hidden joint evaluation.
This is not a failure of message formatting; no message exists. Increasing revision budget would
not help unless the visible oracle exposes a distinguishing behavior.

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                              11

Table 5. Visible-to-hidden generalization for methods available on all benchmark grids. Hidden-joint failures
are counted among visible-joint passes. Counts pool heterogeneous tasks for diagnosis, not significance
testing.


               Method      Visible-joint passes (𝑛)      Hidden-joint failures (𝑛)         TFOR (%)
               B0                                 213                                12             5.6
               B3                                 389                                73            18.8
               B4                                 360                                49            13.6
               M                                  360                                50            13.9



   Feedback can also increase visible confidence without proportionally improving hidden success.
On Qwen2.5-Coder-14B-Instruct/CodeGuard+, B4/M move from B0’s 9.8% TFOR to 15.6% while
producing a small +1.8-point joint improvement over their shared candidates. Some repaired visible
failures remain outside the hidden acceptance region. The correct engineering response is stronger
and more diverse tests, not merely more rounds.
 Answer to RQ4. Passing all visible functional and security tests is not a reliable safety certificate.
 Feedback is coverage-limited: it cannot repair a hidden property that produces no visible failure.

5.5    RQ5: Effects reproduce qualitatively, not uniformly
Table 6 focuses on the untouched, outcome-unfiltered CodeGuard+ breadth wave. Qwen2.5-Coder-
14B-Instruct benefits from B3 over B0 (+10.9 points) and B6 over B3 (+1.8), while B4/M improve
their shared B0 candidates by only +1.8. DeepSeek-V4-Flash shows the opposite entry-point pattern:
B3 is 7.3 points below B0, B6 never triggers, and B4/M repair three B0 cells to gain 5.5 points. The
same test-feedback mechanism exists in both families, but the useful starting point differs.
   SALLM provides another cross-family check. For DeepSeek-V4-Flash, B6 improves B3 from 81.8%
to 87.3%; for Qwen2.5-Coder-14B-Instruct it improves 63.6% to 72.7%. For Qwen3.6-27B, however,
both are already 90.9%, and for Qwen2.5-Coder-7B-Instruct B6 ends below M. Across Qwen and
DeepSeek, feedback can repair failures; across model/benchmark cells, neither its magnitude nor
the best entry condition is stable.
   The outcome-unfiltered breadth result also changes the interpretation of the earlier selected
pilot. A three-task CodeGuard+ pilot, selected after a preflight requiring a failure or feedback
opportunity, showed large feedback gains. When all 11 semantically qualified tasks are included
without looking at outcomes, triggers and gains shrink. We exclude the selected pilot from the
2,705 primary trajectories and use it only as evidence that preflight selection can inflate apparent
treatment opportunity.
 Answer to RQ5. The qualitative repair mechanism reproduces across Qwen and DeepSeek
 and across three benchmarks. Effect size, direction of upfront prompting, and the best feedback
 entry point do not.

6     Discussion
6.1    What the study establishes
The strongest evidence is paired and mechanistic. When a visible failure exists, executing tests
and returning the failure can change the same initial candidate from hidden failure to hidden joint
success. We observe 80 such changes for structured B0 feedback and 18 for structured B3 feedback.
The result appears on internal and external benchmarks and both model families.

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
12                                   Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


Table 6. Outcome-unfiltered CodeGuard+ breadth results. Func., Secure, Joint, and TFOR are hidden-
evaluation percentages; Calls is the mean number of model calls per task–repetition cell. Model keys are
defined in Table 2. This wave contains 11 human-reviewed overlay tasks and applies no baseline-failure or
feedback-trigger filter.


       Model key               Method             Func.     Secure Joint TFOR                      Calls
       Q2.5-C14B               B0                    80.0        80.0       76.4          9.8        1.00
       Q2.5-C14B               B3                    89.1        90.9       87.3          8.5        1.00
       Q2.5-C14B               B4                    87.3        89.1       78.2         15.6        1.44
       Q2.5-C14B               B5                    87.3        83.6       78.2         15.6        1.44
       Q2.5-C14B               M                     87.3        90.9       78.2         15.6        1.44
       Q2.5-C14B               B6                    90.9        92.7       89.1          8.3        1.27
       DS-V4-F                 B0                    92.7       89.1        89.1          0.0        1.00
       DS-V4-F                 B3                    90.9       90.9        81.8         18.2        1.00
       DS-V4-F                 B4                    94.5      100.0        94.5          5.5        1.13
       DS-V4-F                 B5                    94.5      100.0        94.5          5.5        1.13
       DS-V4-F                 M                     94.5      100.0        94.5          5.5        1.13
       DS-V4-F                 B6                    90.9       90.9        81.8         18.2        1.00

   The study does not establish that M is a new state-of-the-art method. Raw and structured
feedback are essentially tied head-to-head, and no adjusted test is significant. Treating the study as
an algorithm leaderboard would discard its main contribution: separating specification, feedback
availability, representation, and coverage reveals why secure-generation interventions sometimes
help and sometimes harm.

6.2    Implications for tool builders
   Preserve the joint contract. An orchestrator should track both functional and security properties
after every edit. Security-first selection can produce 𝐹 − 𝑆 + , while functionality-first correction can
reintroduce a vulnerability. Reporting only the dimension targeted by the latest feedback creates
false progress.
   Measure treatment opportunity. A high final score may arise from a strong initial model rather
than a feedback policy; a low feedback gain may arise because tests never fail. Tools should report
trigger count, repairs per trigger, and the initial four-state distribution alongside final pass rates.
   Invest in behavior diversity before more rounds. When visible tests pass and hidden attacks
fail, extra iterations are inert. Mutation testing, metamorphic variants, boundary generation, and
independent fuzzing can expand the visible signal. Care is needed to prevent the new tests from
becoming near-duplicates of the hidden evaluation.
  Use structured feedback for control, not assumed accuracy. Compact typed feedback has engineering
advantages: predictable token use, explicit property labels, and prioritization. Our evidence does not

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                              13

show that it is inherently more effective than raw logs. A practical system could choose adaptively:
structured summaries for redundant failure sets, raw context for subtle functional traces, and
regression tests retained across rounds.

6.3    Implications for secure-code evaluation
First, function and security must be evaluated on the same candidate. Second, hidden tests must be
isolated from generation and stopping. Third, iterative methods need shared-candidate analysis;
otherwise initial prompt differences masquerade as repair. Fourth, task-level inference matters.
Thousands of trajectories cannot compensate for a small number of security tasks. Finally, bench-
mark qualification should be separated from outcome selection. Our CodeGuard+ breadth wave
demonstrates how a semantically valid but outcome-unfiltered set can yield a smaller, more credible
effect.

6.4    A research agenda
The next step is not another fixed priority rule. A stronger line of work would learn or search
feedback policies while evaluating on held-out tasks and behavior families; estimate the value of a
test before spending a model call; generate new tests when the visible suite reaches a ceiling; and
extend joint evaluation to repository-level changes, multiple languages, build systems, and stateful
vulnerabilities. Human studies are also needed: SAFE@1 assumes partially functional secure code
has developer value, but the actual effort to complete such code remains unmeasured in our study.

7     Threats to Validity
   Construct validity. Passing dynamic tests does not prove absence of vulnerabilities. We cover
specified CWE behaviors, not arbitrary attacks. Conversely, a security test may reject a safe
but semantically different implementation. Secure implementations, vulnerable mutants, repeat
executions, and semantic review reduce this risk but do not eliminate it. SAFE@1 often collapses to
the joint outcome on external tasks because they contain one hidden functional case; we therefore
treat SAFE as sensitivity analysis, not independent corroboration. TFOR depends on the strength
and granularity of both partitions.
  Internal validity. Shared initial candidates make B4/B5/M versus B0 and B6 versus B3 edit-level
comparisons. B3 versus B0 is not shared and cannot identify a repair effect. Local generation seeds
improve repeatability but do not remove stochastic inference variation. Remote request slots are
not deterministic seeds, and the provider may revise its backend. Token accounting for DeepSeek-
V4-Flash uses a frozen local proxy tokenizer for budget enforcement; raw provider usage is retained
separately. Different benchmarks have slightly different completion and execution budgets, so we
do not pool them as a single leaderboard.
  Oracle and researcher bias. Generative models proposed secure implementations and served as
preliminary semantic reviewers. Executable mutation gates prevent accepting candidates on model
opinion alone, and review packets are blinded, but correlated model errors remain possible. After
the executable gates and three-repeat stability checks, three software-engineering doctoral students
manually reviewed every frozen SALLM and CodeGuard+ qualification packet. This human review
reduces, but does not eliminate, construct and researcher bias: reviewers may share interpretation
assumptions, and passing a finite dynamic oracle cannot establish security against arbitrary attacks.
  External validity. The study covers two model families, four local size/configuration points, a
remote API, three benchmarks, and 16 CWE categories. All tasks are Python functions or small
components. Findings may not transfer to Java/C/C++, repository-level agents, multi-file state,

                                                                 , Vol. 1, No. 1, Article . Publication date: August 2027.
14                                   Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


concurrency, dependency vulnerabilities, or production deployment. Public benchmark prompts
may occur in pretraining. Behavior-family splits reduce direct input memorization but cannot
establish contamination-free evaluation.

   Statistical conclusion validity. There are 31 benchmark task instances, not 2,705 independent
samples. Cluster intervals are wide, and no Holm-adjusted comparison is below 0.05. The nine-
condition RQ1 macro treats benchmark–model cells equally and is descriptive. Repair counts
establish observed transitions, not a population-wide effect size. We avoid universal superiority
language and expose denominators throughout.

  Reliability and safety. Generated code is untrusted. Bubblewrap restricts filesystem mounts,
process environment, and network access, with fresh sandboxes and timeouts, but an unprivileged
sandbox is not equivalent to a hardened VM. The artifact should run only on an isolated research
host. Local checkpoint hashes and all prompts/oracles are frozen; remote API outputs are archived
because they may not be reproducible.

8     Related Work
8.1 Secure code generation
Early empirical work showed that code assistants can emit CWE-relevant vulnerabilities and that
access to an AI assistant can worsen security outcomes while increasing users’ confidence in
their solutions [20, 22]. SVEN steers pretrained code models with property-specific continuous
vectors [9]; SafeCoder jointly tunes instruction following and secure generation [10]; CodeGuard+
studies constrained decoding and introduces joint correctness/security evaluation [8]; and PromSec
iteratively optimizes prompts using vulnerability-analysis feedback [17]. AutoSafeCoder combines
coding, static-analysis, and fuzzing agents [19]. These approaches differ in whether intervention
occurs during training, decoding, prompting, or tool use. Our work intervenes only at inference
and holds initial candidates fixed to isolate executable-feedback effects.
   Dai et al. reevaluate secure-generation methods with multiple analyzers and functionality on
the same code, showing that apparent safety can come from broken output [4]. Our dynamic
joint outcome follows the same principle and adds longitudinal state transitions. Their SAFE@k
motivates our partial-functionality sensitivity analysis, while hidden dynamic security cases remain
our primary oracle.

8.2    Secure-code benchmarks
SecurityEval established a CWE-mapped prompt set for security assessment of generated code [25];
SALLM supplies security-centric Python prompts and configurable assessment [26]. SecCodePLT
argues for executable security evaluation in realistic environments [28]. CWEval provides outcome-
driven functional and security oracles [21], and CodeGuard+ explicitly measures secure and correct
code [8]. On functional generation, EvalPlus demonstrates that weak test suites can accept incorrect
programs and even mis-rank models [15]. We do not propose a replacement benchmark. We adapt
three complementary sources into a common visible/hidden protocol and document the semantic
qualification needed when original execution environments are unavailable.

8.3    Execution feedback and repair
CodeT generates tests to select among candidate programs, while LEVER learns to rank candidates
from their execution results [2, 18]. CodeRL incorporates unit-test feedback in training and infer-
ence [14]; self-debugging revises generated programs using execution results [3]; and Reflexion

, Vol. 1, No. 1, Article . Publication date: August 2027.
Security Tests as Executable Specifications for LLM Code Generation:
Benefits, Trade-offs, and Coverage Limits                                                                                15

and OpenCodeInterpreter broaden iterative linguistic or execution feedback to agentic code re-
finement [24, 29]. VRpilot returns compiler, functional, and sanitizer feedback for vulnerability
repair [13]. Our focus differs in three respects: generated secure code rather than a known vulnera-
ble program, a hidden joint functional/security endpoint, and exact sharing of initial candidates
across feedback policies. The visible-to-hidden design also exposes the point at which iterative
debugging cannot proceed because its oracle is silent.

9   Conclusion
Security tests can serve as more than a final benchmark. Used upfront, they often improve generation
but sometimes harm it. Used as feedback, they repair a measurable subset of the same failed
candidates across benchmarks and model families. The benefit is neither free nor universal: feedback
can shift functionality and security in different directions, structured summaries do not consistently
beat raw logs, and no loop can repair a hidden behavior that visible tests fail to expose. Secure-code
generation should therefore be evaluated as a joint, budgeted, coverage-dependent process. The
empirical claim supported by our data is not that one method wins everywhere; it is that executable
feedback makes security repair possible and its limits measurable.

Data Availability
An anonymized replication package is available to reviewers at https://anonymous.4open.science/
r/sectdd-FBDB/. It contains the living and frozen protocols, benchmark manifests and repository
commits, visible/hidden oracle projections, secure and vulnerable oracle subjects, sandbox runners,
exact prompts, local checkpoint/configuration hashes, raw responses, the 2,705 trajectory records
analyzed in this manuscript, analysis scripts, generated tables, and result freezes. Hidden tests
are included in the reviewer package but are never mounted during generation. API credentials,
absolute user paths, and identity-bearing metadata are excluded. Upon acceptance, the authors
intend to publish the curated package under the licenses of the component benchmarks.

References
 [1] Kent Beck. 2002. Test Driven Development: By Example. Addison-Wesley Professional.
 [2] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2023. CodeT:
     Code Generation with Generated Tests. In The Eleventh International Conference on Learning Representations. https:
     //openreview.net/forum?id=ktrw68Cmu9c
 [3] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2023. Teaching Large Language Models to Self-Debug.
     arXiv preprint arXiv:2304.05128 (2023). https://arxiv.org/abs/2304.05128
 [4] Shih-Chieh Dai, Jun Xu, and Guanhong Tao. 2026. Rethinking the Evaluation of Secure Code Generation. In Proceedings
     of the 48th IEEE/ACM International Conference on Software Engineering. doi:10.1145/3744916.3773217
 [5] DeepSeek-AI. 2026. DeepSeek V4 Preview Release. https://api-docs.deepseek.com/news/news260424/
 [6] Bradley Efron and Robert J. Tibshirani. 1993. An Introduction to the Bootstrap. Chapman and Hall/CRC. doi:10.1201/
     9780429246593
 [7] Flatpak Project. 2026. bubblewrap: Unprivileged Sandbox Tool. Accessed 2026-08-06. https://github.com/containers/
     bubblewrap
 [8] Yanjun Fu, Ethan Baker, Yu Ding, and Yizheng Chen. 2024. Constrained Decoding for Secure Code Generation. arXiv
     preprint arXiv:2405.00218 (2024). https://arxiv.org/abs/2405.00218
 [9] Jingxuan He and Martin Vechev. 2023. Large Language Models for Code: Security Hardening and Adversarial
     Testing. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 1865–1879.
     doi:10.1145/3576915.3623175
[10] Jingxuan He, Mark Vero, Gabriela Krasnopolska, and Martin Vechev. 2024. Instruction Tuning for Secure Code
     Generation. In Proceedings of the 41st International Conference on Machine Learning (Proceedings of Machine Learning
     Research, Vol. 235). 18043–18062. https://proceedings.mlr.press/v235/he24k.html
[11] Sture Holm. 1979. A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics 6, 2
     (1979), 65–70. https://www.jstor.org/stable/4615733


                                                                   , Vol. 1, No. 1, Article . Publication date: August 2027.
16                                   Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, and Shiwen Ni


[12] Binyuan Hui et al. 2024. Qwen2.5-Coder Technical Report. arXiv preprint arXiv:2409.12186 (2024). https://arxiv.org/
     abs/2409.12186
[13] Ummay Kulsum, Haotian Zhu, Bowen Xu, and Marcelo d’Amorim. 2024. A Case Study of LLM for Automated
     Vulnerability Repair: Assessing Impact of Reasoning and Patch Validation Feedback. In Proceedings of the 1st ACM
     International Conference on AI-Powered Software. doi:10.1145/3664646.3664770
[14] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi. 2022. CodeRL: Mastering Code
     Generation through Pretrained Models and Deep Reinforcement Learning. arXiv preprint arXiv:2207.01780 (2022).
     https://arxiv.org/abs/2207.01780
[15] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is Your Code Generated by ChatGPT Really
     Correct? Rigorous Evaluation of Large Language Models for Code Generation. In Advances in Neural Information
     Processing Systems, Vol. 36. doi:10.52202/075280-0943
[16] MITRE. 2026. Common Weakness Enumeration. Accessed 2026-08-06. https://cwe.mitre.org/
[17] Mahmoud Nazzal, Issa Khalil, Abdallah Khreishah, and NhatHai Phan. 2024. PromSec: Prompt Optimization for
     Secure Generation of Functional Source Code with Large Language Models. arXiv preprint arXiv:2409.12699 (2024).
     https://arxiv.org/abs/2409.12699
[18] Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-Tau Yih, Sida Wang, and Xi Victoria Lin. 2023. LEVER:
     Learning to Verify Language-to-Code Generation with Execution. In Proceedings of the 40th International Conference
     on Machine Learning (Proceedings of Machine Learning Research, Vol. 202). 26106–26128. https://proceedings.mlr.press/
     v202/ni23b.html
[19] Ana Nunez, Nafis Tanveer Islam, Sumit Kumar Jha, and Peyman Najafirad. 2024. AutoSafeCoder: A Multi-Agent
     Framework for Securing LLM Code Generation through Static Analysis and Fuzz Testing. arXiv preprint arXiv:2409.10737
     (2024). https://arxiv.org/abs/2409.10737
[20] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. 2022. Asleep at the
     Keyboard? Assessing the Security of GitHub Copilot’s Code Contributions. In 2022 IEEE Symposium on Security and
     Privacy. 754–768. doi:10.1109/SP46214.2022.9833571
[21] Jinjun Peng, Leyi Cui, Kele Huang, Junfeng Yang, and Baishakhi Ray. 2025. CWEval: Outcome-driven Evaluation on
     Functionality and Security of LLM Code Generation. arXiv preprint arXiv:2501.08200 (2025). https://arxiv.org/abs/
     2501.08200
[22] Neil Perry, Megha Srivastava, Deepak Kumar, and Dan Boneh. 2023. Do Users Write More Insecure Code with AI
     Assistants?. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 2785–2799.
     doi:10.1145/3576915.3623157
[23] Qwen Team. 2026. Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model. https://qwen.ai/blog?id=qwen3.6-27b
[24] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language
     Agents with Verbal Reinforcement Learning. In Advances in Neural Information Processing Systems, Vol. 36. doi:10.
     52202/075280-0377
[25] Mohammed Latif Siddiq and Joanna C. S. Santos. 2022. SecurityEval Dataset: Mining Vulnerability Examples to
     Evaluate Machine Learning-Based Code Generation Techniques. In Proceedings of the 1st International Workshop on
     Mining Software Repositories Applications for Privacy and Security. doi:10.1145/3549035.3561184
[26] Mohammed Latif Siddiq, Joanna C. S. Santos, Sajith Devareddy, and Anna Muller. 2024. SALLM: Security Assessment
     of Generated Code. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering
     Workshops. 54–65. doi:10.1145/3691621.3694934
[27] An Yang et al. 2025. Qwen3 Technical Report. arXiv preprint arXiv:2505.09388 (2025). https://arxiv.org/abs/2505.09388
[28] Yu Yang, Yuzhou Nie, Zhun Wang, Yuheng Tang, Wenbo Guo, Bo Li, and Dawn Song. 2024. SecCodePLT: A Unified
     Platform for Evaluating the Security of Code GenAI. arXiv preprint arXiv:2410.11096 (2024). https://arxiv.org/abs/2410.
     11096
[29] Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue. 2024.
     OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement. In Findings of the Association for
     Computational Linguistics: ACL 2024. 12834–12859. doi:10.18653/v1/2024.findings-acl.762




, Vol. 1, No. 1, Article . Publication date: August 2027.
