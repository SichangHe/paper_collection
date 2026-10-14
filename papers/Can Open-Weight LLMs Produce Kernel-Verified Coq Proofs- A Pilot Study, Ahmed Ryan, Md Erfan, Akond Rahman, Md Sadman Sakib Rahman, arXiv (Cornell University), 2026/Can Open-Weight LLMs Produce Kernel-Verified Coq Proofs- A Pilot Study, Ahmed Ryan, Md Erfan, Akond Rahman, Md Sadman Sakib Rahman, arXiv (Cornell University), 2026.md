                                           Can Open-Weight LLMs Produce Kernel-Verified
                                                    Coq Proofs? A Pilot Study
                                                        Ahmed Ryan∗ , Md Erfan∗ , Akond Ashfaque Ur Rahman† , and Md Rayhanur Rahman∗
                                                                                 ∗ University of Alabama, Tuscaloosa, Alabama, USA

                                                                               {aryan9, merfan}@crimson.ua.edu, mrahman87@ua.edu
                                                                                     † Auburn University, Auburn, Alabama, USA

                                                                                               azr0154@auburn.edu


                                           Abstract—Large Language Models (LLMs) can generate text                  The difference between a convincing-looking proof and a
                                        that resembles a mathematical proof, but resemblance does not            formally valid proof matters because an LLM can fail at
                                        establish correctness. A formal proof checker verifies correctness       several levels. LLMs may produce invalid syntax, invoke a
                                        by evaluating whether each proof step follows the logical rules.
                                        Coq bases these rules on the Calculus of Inductive Constructions,        tactic that does not exist, refer to a lemma that the project
                                        a logical framework that defines which proof steps the system            does not provide, or apply a valid theorem under the wrong
                                        may accept. This pilot study evaluated 6 open-weight LLMs on             assumptions. A Coq tactic transforms a proof goal into one or
                                        the same 100 theorems from CoqStoq, a benchmark derived from             more smaller goals. An LLM may also omit a required step,
arXiv:2608.05420v1 [cs.LO] 5 Aug 2026




                                        real Coq projects. Each LLM received one attempt per theorem             leave a proof incomplete, use definitions that differ from those
                                        with temperature set to 0, and Coq checked every proposed
                                        proof in the theorem’s original project environment. A proof             in the target project, or depend on a different library version.
                                        was counted as successful if Coq’s trusted kernel accepted it.           These failures show why a proof must be checked rather than
                                           G EMMA 4 verified 12 of 100 theorems, L LAMA 3.3 verified             judged by how convincing it sounds. Therefore, we count a
                                        8, and D EEP S EEK C ODER V2 L ITE verified 1. Q WEN 3.5,                proof as successful only when Coq’s kernel accepts it in the
                                        M ISTRAL S MALL 3.1, and GPT-OSS verified none. The 21                   theorem’s original project environment.
                                        successful proofs covered 15 distinct theorems, and the baseline
                                        of standard Coq tactics did not solve 11 of them. LLMs were                 Existing studies do not yet establish how reliably general-
                                        able to verify theorems that had only short or medium human              purpose open-weight LLMs produce verified proofs for the-
                                        reference proofs, and no LLMs were able to verify theorems with          orems collected from real Coq projects. The literature also
                                        long reference proofs. Because we explored proof length after            provides limited evidence about three related matters: which
                                        selecting the primary analysis, this pattern does not establish
                                                                                                                 sampled theorems these LLMs solve, whether their successes
                                        that proof length caused the difference.
                                           For the three LLMs with at least one success, the total               overlap with basic Coq automation, and how many compu-
                                        generation cost per verified proof ranged from 741 to 36,193             tational resources the LLMs consume. Coq automation uses
                                        output tokens, from 14.9 to 178.0 seconds, and from 0.0167 to            tactics to search for a proof with limited or no step-by-step
                                        0.2000 aggregate GPU hours. We did not calculate this ratio              direction from a user. We therefore use one fixed experimental
                                        for an LLM that produced no kernel-verified proof. Across                procedure to evaluate proof success, compare model and
                                        600 attempts, the six models produced 21 kernel-verified proofs
                                        (3.5%), which covered 15 distinct theorems. The pilot study              automation results, and measure resource use.
                                        reports descriptive differences among LLMs but did not directly             The goal of this study is to evaluate how well open-
                                        test whether the performance difference between any two LLMs             weight LLMs produce kernel-verified Coq proofs, identify the
                                        was statistically significant. Therefore, the results do not establish   theorems they prove and measure the resources they use, and
                                        a universal ranking of the six models.
                                           Index Terms—large language models, formal verification, au-
                                                                                                                 eventually provide empirical evidence of the capabilities of
                                        tomated theorem proving, Coq, proof generation                           LLMs to the researchers, tool developers, practitioners, and
                                                                                                                 educators. To achieve this goal, we investigate the following
                                                                I. I NTRODUCTION                                 research questions:

                                           Researchers increasingly use LLMs to generate formal                    • RQ1: How often do LLMs generate a Coq proof that the
                                        mathematical proofs. A formal proof states each reasoning                    kernel accepts?
                                                                                                                   • RQ2: Which sampled theorems do LLMs solve, and how
                                        step in a precise language that a computer program can check.
                                        Because an LLM predicts text based on probability rather than                do their success compare with basic Coq automation?
                                                                                                                   • RQ3: How much computational resource do LLMs use
                                        enforcing logical validity, its output requires independent ver-
                                        ification. Coq provides that verification. As a proof assistant,             while generating verified proofs?
                                        Coq helps users state theorems, construct proofs, and check                 For RQ1 , each of six LLMs attempts 100 theorems from
                                        results. Coq’s small trusted kernel determines whether each              real Coq projects, and we count only proofs accepted by
                                        proof step follows from the stated assumptions and logical               the Coq kernel. We report verification rates with confidence
                                        rules. The kernel accepts a proof only when every step follows           intervals to express statistical uncertainty. For RQ2 , we com-
                                        those rules and rejects a proof if it contains an invalid step.          pare verified theorems across projects, reference-proof lengths,
and a fixed Coq-automation baseline. This comparison shows            verified@1 indicates whether a LLM’s first and only proof
whether the models and baseline prove the same or different        attempt for a theorem passes all verification checks. It mea-
theorems. For RQ3 , we measure generated tokens, wall-             sures success from a single attempt and does not represent
clock time, and GPU time. Because every model attempts             performance when a LLM can generate multiple proofs or
each theorem once, these measurements support a consistent         revise a failed proof.
comparison of resource use.
                                                                                        III. R ELATED W ORK
  Contributions: We list our contributions as follows:
                                                                      Coq Proof-Generation Systems: Several systems learn to
  • A reproducible benchmarking protocol that runs each
                                                                   generate Coq proofs. CoqGym collects proofs from existing
    model in the theorem’s original Coq environment and            projects and supports ASTactic, which learns to generate
    accepts only proofs verified by the Coq kernel.                tactics from those proofs [1]. Proverbot9001 also learns to
  • An evaluation of six open-weight LLMs under the same
                                                                   generate Coq proofs and evaluates its method mainly on
    one-attempt proof-generation rule.                             CompCert, a project included in our sample [2]. Tactician
  • A comparison of the theorems solved by each LLM and
                                                                   learns from existing tactic scripts and can suggest the next
    a fixed Coq-automation baseline.                               tactic or attempt to complete a proof [3]. Rango provides the
  • A resource analysis based on generated tokens, elapsed
                                                                   closest comparison because it also evaluates proof generation
    time, and GPU time.                                            on CoqStoq [4]. However, Rango uses a fine-tuned model and
                                                                   retrieves relevant information before generation. In contrast,
                     II. K EY C ONCEPTS
                                                                   our pilot evaluates general-purpose chat models with one fixed
   We use the following concepts to define the study and           prompt, one attempt, and no fine-tuning, retrieval, repair, or
interpret its reported outcomes.                                   interactive feedback.
   Coq checks whether a proof follows its formal rules, which         Benchmarks and Automation Baselines: Benchmark studies
are based on a logical system called the Calculus of Inductive     show why an overall success rate is not sufficient. CoqS-
Constructions.                                                     toq contains theorems from real Coq projects and preserves
   A formal proof expresses each reasoning step using defined      differences in libraries, notation, and proof styles [4]. By
symbols, syntax, and logical rules that a computer program can     comparison, miniF2F contains competition-style mathemati-
interpret and verify.                                              cal problems for several proof assistants [5], and LeanDojo
   A theorem states a claim that follows from previously           supports proof search in Lean projects [6]. Because these
defined assumptions, definitions, and logical rules. In this       benchmarks use different theorem sources and proof assistants,
study, each theorem specifies the claim for which an LLM           their success rates cannot be compared directly. Existing Coq
must produce a proof that Coq can verify.                          automation provides another reference point. CoqHammer
   A proof goal states what needs to be proved at a particular     uses relevant prior results and external theorem provers to
stage of the proof. As the LLM applies valid proof steps, Coq      construct proofs that Coq can verify [7]. Our fixed baseline of
updates the goal until no unproved goals remain.                   auto, eauto, and intuition auto is more limited but
   A tactic script directs Coq through a sequence of commands      easier to inspect and apply consistently. Thus, an LLM-only
that reduce a proof goal to smaller goals until no goal remains.   success means that this fixed baseline failed, not that all Coq
Even after the script closes every goal, the complete proof        automation would fail.
must pass the kernel checks.                                          Computational Resource Measurement: Prior systems use
   An large language model (LLM) is a machine-learning             different models, search procedures, hardware, benchmarks,
model trained on large datasets to generate new content from       and stopping rules, which prevents direct comparisons of
a given prompt. In this study, an LLM receives a Coq theorem       computational cost. For example, systems that retrieve exam-
statement and the permitted project context, then generates a      ples, try multiple tactics, repair failures, or interact repeatedly
tactic script intended to prove the theorem.                       with Coq perform more work than a one-attempt system. We
   CoqStoq is a dataset of Coq theorems collected from real        therefore report generated tokens, generation time, and GPU
software projects. It provides each theorem with its project       time only for our protocol and hardware. For each model with
context, including the definitions, assumptions, libraries, and    at least one verified proof, we also divide its total resource
dependencies available when the theorem was written.               use by its number of verified proofs. This calculation includes
   A project environment provides the notation, earlier results,   failed attempts because they contribute to the total cost of
tactics, library paths, and software configuration that Coq        obtaining the successful proofs.
requires to compile a theorem. We verify each LLM-generated           Position of This Study: This paper presents a descriptive
proof in its theorem’s original project environment because        pilot evaluation of six general-purpose open-weight LLMs
each project uses different settings.                              on the same 100 CoqStoq theorems. Unlike Coq-specific
   A Reference Proof is the human-written solution provided        systems, it measures proof generation without task-specific
by CoqStoq. We use this proof to confirm that each theorem         training, retrieval, repair, repeated attempts, or interactive feed-
has a valid solution and to group the theorems by proof length.    back. Kernel verification addresses RQ1 . Analyses by project,
The LLMs do not receive or see the reference proofs.               reference-proof length, and automation overlap address RQ2 .
                                                                                                 TABLE I
Resource measurements address RQ3 . The study therefore                           L ANGUAGE MODELS EVALUATED IN THE STUDY
provides an initial account of one-attempt proof generation
                                                                    Label        Full Model Name                     Developer        Params.     CW
under a fixed protocol rather than a universal ranking of
                                                                    Llama        Meta Llama 3.3 70B Instruct         Meta               70B      128K
models or a direct comparison with systems that use different       Qwen         Qwen 3.5 35B-A3B                    Alibaba/Qwen       35B      262K
forms of assistance.                                                Gemma        Gemma 4 31B IT                      Google             31B      256K
                                                                    Mistral      Mistral Small 3.1 24B Instruct      Mistral AI         24B      128K
                                                                    GPT-OSS      GPT-OSS 20B                         OpenAI             20B      128K
                    IV. M ETHODOLOGY                                DeepSeek     DeepSeek Coder V2 Lite Instruct     DeepSeek           16B      128K
                                                                   Note: Params. denotes the nominal total parameter count reported for each model; B =
   We conduct the pilot study in four phases. First, we fix        billion parameters; CW = context window; K = thousand tokens.

the study settings and construct the theorem sets. Second,
we prompt the six LLMs and collect their proposed proofs.             3) Construct the development and main sets: We use CoqS-
Third, Coq verifies every proposed proof, and we compare the       toq as the source repository. CoqStoq divides its theorems into
verified results with a fixed automation baseline. Finally, we     predefined validation and test splits. We select 20 theorems
audit the complete record and calculate the reported statistics.   from the validation split to form the development set, which
Because we fix the benchmark, prompts, and verification            we use to test the methodology. We select 100 theorems from
rules before observing the main results, those results cannot      the test split to form the main set, which we use to produce
influence the evaluation rules.                                    the reported results. Each theorem belongs to a Coq project.
                                                                   Each project defines notation, reusable results, automated
A. Study design and benchmark construction                         tactics, and library paths. Together, these components form
                                                                   the theorem’s project environment. Because a proof may work
   1) Fix the protocol and software versions: Before generat-      in one project and fail in another, we compile and verify
ing any study proof, we record every setting that can affect       every proof in its original project environment. This procedure
generation or verification. We record theorem-selection rules,     verifies each proof with the project-specific settings that Coq
model versions, prompts, software dependencies, generation         requires for that theorem.
options, and verification rules because changing any item may         We treat every theorem in the CoqStoq test split as a
change the outcome. We clone the official CoqStoq repository       candidate theorem, meaning that it may be selected for the
and its included dependencies. We then fix the copy to one Git     main evaluation set if it meets the selection requirements. We
commit SHA, which uniquely identifies an exact repository          assign each candidate a reproducible position based on its
version. We evaluate six LLMs shown in Table I. We fix each        split, a fixed study date, and its unique identifier. We then
LLM repository and its tokenizer to an unchangeable Hugging        sort and examine the candidates in that order. This procedure
Face commit SHA. We obtain each identifier through the             prevents manual selection and produces the same ordering
Application Programming Interface (API) of Hugging Face.           when researchers repeat the study. We include a candidate
   We compute cryptographic hashes for three types of content:     theorem only if it satisfies three conditions: (a) The theorem’s
the prompt template, the complete prompt sent to each LLM          project contributes fewer than 10 selected theorems. (b) The
after formatting, and the theorem context included in that         theorem’s statement differs from every selected statement. (c)
prompt. A cryptographic hash acts as a digital fingerprint         The theorem passes the eligibility checks described below.
because any change to the content changes the hash. We record         To determine eligibility, we test each theorem in a container
these hashes with the code commit, container-image digests,        that provides an isolated environment with fixed tools and
dependency-lock hashes, and all generation and verification        dependencies. We first build the theorem’s project. We then
settings. Before generating proofs, the system checks that         place its original human-written reference proof in a separate
the current LLM versions, prompts, dependencies, verification      copy of the source file and ask Coq to verify it. Using a copy
environment, and settings match the recorded configuration.        prevents the check from changing the original project. We
These checks prevent unrecorded changes from affecting the         exclude a theorem if its project cannot be built or Coq cannot
results and allows reproducibility of the experiment.              verify its reference proof. We use the reference proof only for
   2) LLM Selection: We select the six LLM using four              this eligibility check and the later proof-length analysis, we
criteria. First, each LLM provides downloadable weights and        never show it to an LLM.
supports local execution. Second, each LLM can follow in-             Because this is a pilot study, we limit each prompt to 24,000
structions and generate source code without task-specific fine-    tokens to balance the amount of project context with the
tuning. Third, each LLM fits within our available computa-         required memory, runtime, and GPU resources. We exclude
tional resources (192GB GPU Memory). Fourth, the selection         a theorem if its prompt exceeds this limit under any model’s
includes LLMs from different developers and parameter scales       tokenizer. Applying the same limit across all models keeps the
to represent a range of open-weight model families. We also        evaluation set identical and leaves space for proof generation.
include D EEP S EEK C ODER V2 L ITE I NSTRUCT as a code-           We also exclude a theorem if its prompt contains its own
specialized model to examine whether training focused on           reference proof or another selected theorem’s reference proof,
source code benefits Coq proof generation. These criteria yield    which prevents models from copying known solutions. We
the six LLMs in Table I.                                           continue the selection process until the main set contains
                                                 Fig. 1. Methodology of the pilot study.



exactly 100 theorems from at least 10 projects. We select no          by which an LLM could copy a selected reference proof from
more than 10 theorems from any project to limit the influence         the prompt.
of large projects and represent a wider range of coding styles
and library environments.                                             B. Prompting and Proof Generation
   We apply the same procedure to CoqStoq’s validation                   1) Apply one prompt design to every LLM: We use the same
split to select 20 development theorems. We exclude projects          fixed prompt template for every LLM and theorem (see List-
represented in the main set so that the development and main          ing 1). For each theorem, we replace only source_prefix
sets contain different projects. The development and main             and theorem_statement with the relevant project context
sets contain different projects to prevent test-set leakage. This     and theorem statement. We provide no model-specific exam-
separation ensures that adjustments made during development           ples, hints, retrieval results, repair attempts, or other assistance.
are not tailored to the projects used for the final evaluation.
We record why we exclude each candidate theorem. If the                Complete the following Coq theorem. Return only the proof
                                                                       body: the commands that belong between ‘Proof.‘ and ‘Qed.‘
fixed selection rules cannot produce both sets, we stop the            Do not include Markdown fences, ‘Proof.‘, ‘Qed.‘,
experiment rather than change the rules after examining the            admissions, new axioms, or commentary.

candidates.                                                            Project-visible source: {{ source_prefix }}
   4) Prevent reference-proof leakage: We show each LLM                Theorem: {{ theorem_statement }}
only the part of the source file that appears before the selected
theorem. We call this material the source prefix. Because the             Listing 1. Fixed prompt template used for all models and theorems.
source prefix ends where the theorem begins, it excludes that            We then format the resulting message with each model’s
theorem’s reference proof and all later file content.                 official chat template. This formatting changes the model-
   Two selected theorems may come from the same file. The             specific control tokens and markup but not the instructions
proof of the earlier theorem may then appear in the later             or theorem content. The prompt also tells the LLM to omit
theorem’s source prefix. We call this event cross-theorem             Markdown fences, proof markers, unfinished-proof commands,
leakage, which means that one evaluated theorem’s reference           and new assumptions. These restrictions standardize the re-
proof becomes visible in another evaluated theorem’s prompt.          sponses and prevent the LLM from bypassing the intended
We remove the affected theorem, replace it with the next              task. We record hashes of the prompts to confirm that the
eligible theorem in the fixed order, and repeat the check until       protocol remains fixed.
no leakage remains.                                                      2) Generate one candidate for each theorem by each LLM:
   Before locking the protocol, we audit every final prompt for       Each LLM generates one candidate proof for each of the 100
reference-proof exposure. We refuse to lock the protocol if the       main theorems and 20 development theorems. Therefore, The
audit finds any exposure. These checks remove known routes            six LLMs produce 600 main candidates and 120 development
theorem. Each candidate proof lets us measure ‘verified@1‘,         syntax-aware scan, which follows Coq’s command structure
which records whether an LLM’s first and only candidate             instead of treating every period as a command boundary. This
passes verification. This design controls computational cost,       approach avoids misreading comments, notation, and qualified
but it does not estimate success under repeated sampling.           names. The scan rejects commands that could bypass the
   We set the generation temperature to 0. When generating          task: ‘Admitted‘, ‘admit‘, ‘Axiom‘, ‘Conjecture‘, ‘Parameter‘,
a response, an LLM considers several possible tokens for the        ‘Abort‘, and ‘Declare ML Module‘.
next position and assigns each token a probability based on the        Next, we compile the file with Coq 8.18 in the theorem’s
prompt and the tokens already generated. A temperature of 0         original project directory. We use the project’s library-path
directs the LLM to select the token with the highest estimated      mappings, which connect names in the proof to the required
probability instead of randomly sampling from the alternatives.     files and modules. We require Coq to finish compilation and
This setting reduces variation and makes repeated runs more         leave no open proof obligations. An open proof obligation
consistent, although differences in software or hardware may        is a remaining goal that still requires a proof. We then run
still affect exact reproducibility. We also limit each response     ‘Print Assumptions‘, which lists every assumption used by
to 4,096 generated tokens. This limit provides enough space         the completed theorem. We reject any assumption that the
for a substantial Coq proof while preventing unusually long         protocol does not allow. Finally, we run ‘coqchk‘, which
responses from consuming excessive runtime, memory, or              asks the Coq kernel to check the compiled library. Together,
GPU resources.                                                      these checks detect incomplete proofs, added assumptions, and
   We distribute each LLM’s fixed parameters across four            proofs verified under the wrong project setup.
Graphics Processing Units (GPUs). Before timing the study              We classify a candidate as verified only if it compiles, closes
attempts, we run one non-study prompt as a warm-up. A               every proof obligation, uses no forbidden assumption, and
warm-up performs an initial generation so that one-time setup       passes ‘coqchk‘. The ‘verified@1‘ measure reports whether
work does not inflate the measured time for the first theorem.      the one candidate generated for a theorem satisfies all four
For each attempt, we record the prompt hash, raw response,          conditions. Thus, every reported success represents a complete
input and output token counts, stopping reason, timestamps,         proof accepted by Coq rather than a script that only ap-
and retry information. We run the six LLMs sequentially. Each       pears plausible. We assign each failed attempt one predefined
LLM completes the development set before any LLM begins             category, such as ‘syntax error‘, ‘tactic failure‘, ‘unautho-
the main set. We unload one LLM and confirm that the GPUs           rized assumption‘, or ‘infrastructure error‘. An infrastructure
have released its memory before we load the next LLM. This          error describes a failure in the evaluation system rather than
sequence prevents the LLMs from competing for the same              a failure in the proposed proof. We retry only infrastructure
hardware and keeps timing conditions more consistent.               errors, and we never change the candidate during a retry. This
   3) Confirm that the main run fits the time budget: During        rule prevents a verification problem from giving an LLM an
the development run, we measure each LLM’s throughput and           additional proof attempt.
loading overhead. Throughput measures how many theorems                2) Compare the LLMs with a fixed automation baseline:
an LLM processes per unit of time. Loading overhead mea-            We also evaluate a fixed automation baseline. An automation
sures the time required to prepare the LLM before generation.       baseline is a consistent procedure that provides a reference
We use only these timing measurements to estimate the               point for interpreting LLM performance. We apply the follow-
duration of the 600 main generations. We do not examine             ing LLM-independent tactic script to all 100 main theorems:
development-set success when making this decision, because
                                                                    first [ solve [ auto ] | solve [ eauto ] | solve [ intuition
early success results must not influence the final sample.               ,→ auto ] ].
   We start the main run only if the estimate fits within 40
hours of the 48-hour pilot budget. We reserve the remaining 8                    Listing 2. Automation Baseline Tactic Script
hours for repeat verification, auditing, analysis, and reporting.     The script asks three standard Coq tactics, in order, to solve
If the estimate exceeds 40 hours, we stop and produce a             the complete theorem. We run the script with the same timeout,
feasibility report. We do not reduce the fixed sample to fit the    assumption rules, project environment, and verification checks
budget, because that change would alter the evaluation plan.        used for the LLM candidates. This comparison identifies LLM
                                                                    successes that overlap with basic built-in proof search. It does
C. Verification and Automation Baseline
                                                                    not represent the strongest automation available for Coq.
   1) Verify every candidate with Coq: We first normalize
each LLM response. Normalization converts a small set of            D. Outcomes, Statistical Analysis, and Reproducibility
recognized output formats into the proof-body format expected          1) Reverify and audit every result: We check every ac-
by the verifier. We remove at most one surrounding Markdown         cepted proof again inside a fresh verification container that
code fence and reject any wrapper that we cannot inter-             did not perform the first check. Repeating verification in a
pret without guessing. These changes standardize presentation       newly created environment helps detect results that depended
without changing the proposed proof. We insert the normalized       on stale files, cached build products, or accidental state from
proof body between fixed ‘Proof.‘ and ‘Qed.‘ commands               an earlier run. Before calculating any statistic, we confirm all
in a copy of the theorem’s source file. We then apply a             of the following: (a) the benchmark contains exactly 100 main
theorems and 20 development theorems. (b) the records name             model-theorem successes passed fresh-container reverification.
exactly six fixed model versions. (c) all 600 model-theorem            Three of the six models produced at least one verified proof.
combinations appear exactly once. (d) every generation has a           The 21 accepted model-theorem results covered 15 distinct
final result that is not an infrastructure error. (e) every accepted   theorems, including 11 not solved by the fixed baseline. All
proof again passes the assumption and coqchk checks. (f)               model successes occurred in the short and medium reference-
every prompt and protocol hash matches the locked value, and           proof groups. Cost per observed success was defined for only
(g) the final leakage audit reports no reference-proof exposure.       three models. The sections below give the evidence behind
The analysis stops if any check fails. Requiring a complete and        each part of this summary, organized by research question.
internally consistent record prevents missing, duplicated, or
unresolved attempts from silently changing a model’s reported          A. Findings of RQ1
rate.                                                                     The observed verified@1 rate ranged from 0% to 12%. Each
   2) Calculate statistics only from audited records: For each         model’s two rates and their own paired interval are reported
model, we report its verified@1 count out of 100 theorems.             side by side, since the Wilson interval and the project-clustered
We present the theorem-level success rate with a Wilson 95%            bootstrap interval estimate two different quantities rather than
confidence interval. We also report the average success rate           offering two views of the same number.
across projects with a project-clustered bootstrap 95% interval                                      TABLE II
based on 10,000 resamples and seed 20260728. The bootstrap                   V ERIFICATION RATES AND CONFIDENCE INTERVALS BY MODEL .
resamples whole projects because theorems from the same
project may be related.                                                 Model           Verify         Theorem Rate                    Project Rate
   The theorem-level rate shows the percentage of all sampled           Llama     8/100 8.0% [4.1%, 15.0%] 8.2% [4.0%, 12.6%]
theorems that a model verifies, whereas the project-level rate          Qwen      0/100  0.0% [0.0%, 3.7%]   0.0% [0.0%, 0.0%]
gives each project equal weight. We treat the project-level             Gemma    12/100 12.0% [7.0%, 19.8%] 11.2% [6.7%, 15.4%]
result as secondary because the sample contains only 12                 Mistral   0/100  0.0% [0.0%, 3.7%]   0.0% [0.0%, 0.0%]
                                                                        GPT-OSS 0/100    0.0% [0.0%, 3.7%]   0.0% [0.0%, 0.0%]
projects. For models with no successes, the bootstrap interval          DeepSeek 1/100   1.0% [0.2%, 5.4%]   1.2% [0.0%, 3.6%]
is [0%, 0%] because every resampled project also contains no
                                                                       Note: “Verify” denotes the number of verified proofs out of 100 evaluated instances.
successes. This result does not prove that the model’s broader         Theorem Rate is weighted equally across theorems and uses Wilson 95% confidence
success probability is zero.                                           intervals. Project Rate is weighted equally across projects and uses cluster-bootstrap
                                                                       95% confidence intervals.
   We also report results by project, reference-proof length,
overlap with the automation baseline, and computational cost.             G EMMA produced 12 verified proofs, L LAMA produced 8,
We treat proof-length results as exploratory because reference-        and D EEP S EEK produced 1. Q WEN, M ISTRAL, and GPT-
proof length only roughly represents difficulty. Finally, we re-       OSS produced no verified proofs under this one-attempt
port results only after all 600 attempts produce valid outcomes,       protocol. A zero observed count does not establish that a
ensuring that every model retains a denominator of 100 and             model’s true success probability is exactly zero: the theorem-
that infrastructure failures are not counted as proof failures.        weighted Wilson interval still extends to 3.7%. The project-
   3) Reproducibility and analysis deviations: The results             weighted bootstrap collapses to [0%, 0%] for these three
cover verification rates and confidence intervals (RQ1 ), per-         models specifically because it resamples from twelve observed
formance by project, reference-proof length, and automation            project clusters that contain no success. We have explained in
overlap (RQ2 ), and computational cost (RQ3 ). We classify             Methodology for why we treat that interval as a secondary
theorems using their human-written reference proofs: short             sensitivity check rather than as evidence the true rate is zero.
proofs contain at most 3 nonblank lines, medium proofs                    This pilot does not statistically test whether one model
contain 4–10 lines, and long proofs contain more than 10               performs better than another. Although all six models attempt
lines. We fixed an earlier implementation error that used              the same 100 theorems, we calculate each model’s confidence
generated proof length and recalculated the results from the           interval separately. A future study could compare two models
audited raw data. For each model, we sum the generated                 by examining their results on each shared theorem and ac-
tokens, generation time, and estimated GPU time across all             counting for differences among projects. We do not compare
100 attempts. We then divide each total by the number of               confidence-interval overlap or use it to rank the models.
verified proofs. Thus, the cost per verified proof includes both
successful and unsuccessful attempts.                                  B. Findings of RQ2
                                                                          The 100 main theorems came from 12 projects. G EMMA
                          V. F INDINGS                                 verified at least one theorem in 9 projects, L LAMA in 7,
   All checks listed in the pilot report passed. The run con-          and D EEP S EEK in 1. Together, the models verified theorems
tained the planned 100 main theorems, 20 development theo-             in 10 of the 12 projects. None verified a theorem from
rems, six fixed model revisions, and 600 unique main model-            projects hoare-tut or reglang. Q WEN, M ISTRAL, and GPT-
theorem records. Every generation had a verification record,           OSS verified zero theorems in every project and every proof-
the protocol hashes matched, the leakage scan was clean, no            length category, so the tables below show only the three
accepted proof contained a forbidden construct, and all 21             models with at least one success, plus the fixed baseline.
                              TABLE III                                                      divide the total resource use by the number of verified proofs.
         N UMBER OF VERIFIED THEOREMS BY PROJECT AND MODEL .                                 We cannot calculate this value for models with no verified
                                                                                             proofs, and it may be unstable when a model has few suc-
  Project           Theorems        Llama       Gemma           DeepSeek     Baseline
                                                                                             cesses. Therefore, we report total resource use and resource
  buchberger                  10           1            2               0             3
  compcert                    10           2            2               0             0
                                                                                             use per verified proof in separate tables.
  dblib                        5           1            1               0             0                                   TABLE VI
  ext-lib                     10           0            1               0             3           T OTAL OUTPUT TOKENS , WALL - CLOCK TIME , AND GPU- HOURS .
  fourcolor                   10           0            1               0             0
  hoare-tut                    1           0            0               0             0
                                                                                               Model                               Output Tokens      Wall Time      GPU Hours
  huffman                     10           1            1               0             0
  math-classes                10           0            1               0             0        Llama 3.3 70B Instruct                        5,930        119.5 s          0.133
  poltac                       7           1            1               0             0        Qwen 3.5 35B-A3B                            407,025        261.7 s          0.300
  reglang                     10           0            0               0             0        Gemma 4 31B IT                               52,202        206.7 s          0.233
                                                                                               Mistral Small 3.1 24B Instruct              118,996        139.9 s          0.150
  zfc                          7           1            0               1             0
                                                                                               GPT-OSS 20B                                 307,349        103.6 s          0.117
  zorns-lemma                 10           1            2               0             1        DeepSeek Coder V2 Lite Instruct              36,193        178.0 s          0.200
                                                                                             Note: Output Tokens denotes the total number of generated tokens; Wall Time denotes
   The reference-proof-length analysis was exploratory. Of the                               the total elapsed inference time; and GPU Hours denotes the total GPU usage in hours.
100 theorems, 34 had short reference proofs, 43 had medium-                                     1) Total resources across all 100 main attempts, all six
length reference proofs, and 23 had long reference proofs. No                                models: Models with no verified proofs still used substan-
model verified a theorem in the long category. This pattern                                  tial resources. For example, Qwen generated 407,025 to-
is consistent with shorter reference proofs being easier under                               kens, while GPT-OSS generated 307,349 tokens. However, we
this protocol, but it is not enough to establish that proof                                  cannot calculate tokens per verified proof for these models
length caused the difference. Reference-proof length is only an                              because they had no verified proofs. High token totals may
indirect measure of difficulty, and these groups were examined                               also reflect long, repeated, or truncated responses rather than
after generation. The fixed Coq automation baseline verified                                 useful proof generation.
7 of the 100 theorems. Its overlap with each of the successful
                                                                                                                           TABLE VII
models was as follows; Q WEN, M ISTRAL, and GPT-OSS                                                           R ESOURCE USAGE PER VERIFIED INSTANCE .
contribute 0 to every column here by construction, since none
produced a verified proof.                                                                    Model                              Verif. Tok./Verif. Time/Verif. GPU h/Verif.
                                       TABLE IV                                               Llama 3.3 70B Instruct                 8        741.2         14.9 s         0.0167
            V ERIFICATION PERFORMANCE BY PROBLEM LENGTH .                                     Gemma 4 31B IT                        12      4,350.2         17.2 s         0.0194
                                                                                              DeepSeek Coder V2 Lite Instruct        1     36,193.0        178.0 s         0.2000
    Model                Short (34)             Medium (43)              Long (23)           Note: “Verif.” denotes the number of verified instances. “Tok./Verif.” denotes the
                                                                                             average number of output tokens per verified instance. “Time/Verif.” denotes the
    Llama               5/34 (14.7%)             3/43 (7.0%)            0/23 (0.0%)          average wall-clock time per verified instance, and “GPU h/Verif.” denotes the average
    Gemma               8/34 (23.5%)             4/43 (9.3%)            0/23 (0.0%)          GPU usage in hours per verified instance.
    DeepSeek             1/34 (2.9%)             0/43 (0.0%)            0/23 (0.0%)
                                                                                                2) Total cost per verified proof, models with at least one
Note: Each cell reports the number of verified instances, the total number of instances,
and the corresponding verification rate in parentheses.                                      success: L LAMA used the fewest resources per verified proof,
                                                                                             followed by G EMMA. D EEP S EEK’s value is less reliable
   The six models produced 21 verified results across 15
                                                                                             because it verified only one proof, so its total cost across
distinct theorems because multiple models solved some of
                                                                                             100 attempts is divided by one. If D EEP S EEK had verified
the same theorems. The baseline also solved 4 of these 15
                                                                                             one more proof with the same total resource use, its cost per
theorems. The LLMs solved 11 theorems that the baseline
                                                                                             verified proof would be cut in half. These results describe
could not solve, while the baseline solved 3 theorems that none
                                                                                             this specific run on four GPUs and should not be treated as a
of the LLMs could solve. Thus, the LLMs and baseline solved
                                                                                             general efficiency ranking.
some different theorems. However, this result applies only to
our limited three-tactic baseline and does not show that the                                                               VI. D ISCUSSION
LLMs outperform stronger or project-specific Coq automation.
                                                                                                Under the strict one-attempt setting, verified proofs were
                           TABLE V
    C OMPARISON OF MODEL AND BASELINE VERIFICATION OUTCOMES .                                rare. Only three of the six models produced a verified proof,
                                                                                             and the highest success rate was 12%. However, these results
 Model                                 Both    Model Only       Baseline Only    Neither     show that open-weight models can generate complete proofs
 Llama 3.3 70B Instruct                    2                6                5         87    that pass all verification checks in real Coq projects.
 Gemma 4 31B IT                            4                8                3         85
 DeepSeek Coder V2 Lite Instruct           0                1                7         92
                                                                                                The failures show that models struggled with more than
Note: “Both” indicates that both the model and the baseline verified the instance;
                                                                                             logical reasoning. Q WEN produced 98 truncated responses.
“Model Only” indicates that only the model verified it; “Baseline Only” indicates that       GPT-OSS produced 59 truncated responses and 41 syntax
only the baseline verified it; and “Neither” indicates that neither verified the instance.   errors. M ISTRAL produced 60 syntax errors, 28 truncated
C. Findings of RQ3                                                                           responses, and 9 empty responses, while D EEP S EEK produced
   We report each model’s total resource use across all 100                                  93 syntax errors. L LAMA and G EMMA also had many project-
attempts. For models that verify at least one proof, we also                                 environment errors. Therefore, verified@1 measures the com-
plete proof-generation process, including correct syntax, out-       automation. Claims about LLM-only successes apply only to
put format, and compatibility with project libraries.                this fixed baseline.
   The LLMs and the fixed automation baseline solved differ-            Finally, this pilot does not statistically test whether one
ent theorems. The LLMs solved 11 theorems that the baseline          model outperforms another. A future study could compare the
could not solve, while the baseline solved 3 that none of the        models theorem by theorem while accounting for differences
LLMs could solve. This result suggests that LLMs and basic           among projects. The current results are descriptive and should
automation may work well together. However, it does not show         not be treated as a universal model ranking.
that LLMs outperform Coq automation because we did not test
                                                                                               VIII. C ONCLUSION
stronger or project-specific automation.
   Total resource use remains meaningful for every model,               Under a strict one-shot, no-repair protocol, open-weight
including models with no verified proofs. For example, Q WEN         LLMs occasionally produced fully kernel-verified Coq proofs
generated 407,025 tokens and used 0.300 GPU hours without            in real projects, including proofs a minimal fixed tactic base-
verifying any proof. In contrast, resource use per verified proof    line could not find. Their low yield and frequent formatting,
is unstable when there are few successes. D EEP S EEK verified       truncation, and project-interface failures, however, make them
only one proof, so one additional success with the same total        unreliable as standalone proof automation under this protocol.
cost would reduce its cost per verified proof by half. So, these     Three of the six models (Q WEN, M ISTRAL, and GPT-OSS)
values should not be treated as a general efficiency ranking.        never produced a single verified proof, and success for the
   Success also varied across projects and proof lengths.            other three was concentrated in short and medium-length
G EMMA verified proofs from nine projects, L LAMA from               reference proofs. Models that verified no proofs still used
seven, and D EEP S EEK only from zfc project. Every verified         substantial tokens and GPU time. For successful models, the
theorem had a short or medium reference proof. However, the          cost per verified proof is uncertain because it is based on only
small number of successes and the exploratory proof-length           a few successes—and on just one success for D EEP S EEK.
analysis do not establish which project or theorem features             Future studies should compare LLMs with stronger and
cause success.                                                       project-specific Coq automation. They should separate syn-
                                                                     tax and project-environment failures from failures in logical
                 VII. T HREATS TO VALIDITY                           reasoning. They should also test whether repair, retrieval, and
                                                                     repeated attempts improve performance. Because every model
   This study evaluates six fixed model versions on 100              evaluates the same theorems, future model comparisons should
theorems using one prompt and one attempt per theorem.               compare their results theorem by theorem. These studies
The results apply only to this setup and do not represent            should continue using Coq kernel verification and independent
performance on all formal proofs. Different prompts, repeated        reverification to ensure that every accepted proof is valid.
attempts, retrieval, repair, tool access, or additional context
could change the results.                                                                           R EFERENCES
   The 100 theorems come from 12 projects, with no more              [1] K. Yang and J. Deng, “Learning to prove theorems via interacting
                                                                         with proof assistants,” in Proceedings of the 36th International
than 10 from each project. This limit increases project diver-           Conference on Machine Learning, ser. Proceedings of Machine Learning
sity but makes the sample different from the full CoqStoq                Research, vol. 97. PMLR, 2019, pp. 6984–6994. [Online]. Available:
dataset. Because some projects and proof-length groups con-              https://proceedings.mlr.press/v97/yang19a.html
                                                                     [2] A. Sanchez-Stern, Y. Alhessi, L. K. Saul, and S. Lerner, “Generating
tain few theorems, their results have substantial uncertainty.           correctness proofs with neural networks,” in Proceedings of the 4th ACM
The project-level confidence intervals are also limited by the           SIGPLAN International Workshop on Machine Learning and Program-
small number of projects.                                                ming Languages. Association for Computing Machinery, 2020, pp. 1–10.
                                                                     [3] L. Blaauwbroek, J. Urban, and H. Geuvers, “The tactician: A seamless,
   Reference-proof length is only a rough measure of difficulty.         interactive tactic learner and prover for Coq,” in Intelligent Computer
A long human proof may have a short automated solution,                  Mathematics, ser. Lecture Notes in Computer Science, vol. 12236.
while a short proof may require specialized knowledge. We                Springer, 2020, pp. 271–277.
                                                                     [4] K. Thompson, N. Saavedra, P. Carrott, K. Fisher, A. Sanchez-Stern,
therefore treat the proof-length analysis as exploratory.                Y. Brun, J. F. Ferreira, S. Lerner, and E. First, “Rango: Adaptive retrieval-
   The resource measurements depend on the hardware and                  augmented proving for automated software verification,” in Proceedings
software used in this study. GPU use was recorded every 15               of the 47th IEEE/ACM International Conference on Software Engineering.
                                                                         IEEE, 2025, pp. 347–359.
seconds, so the reported GPU time may be slightly higher or          [5] K. Zheng, J. M. Han, and S. Polu, “miniF2F: A cross-system
lower than the actual value.                                             benchmark for formal olympiad-level mathematics,” in International
   Many L LAMA and G EMMA failures were labeled                          Conference on Learning Representations, 2022. [Online]. Available:
                                                                         https://iclr.cc/virtual/2022/poster/6258
project_environment_error. This label indicates dif-                 [6] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,
ficulty producing a proof that works with the project’s libraries,       R. Prenger, and A. Anandkumar, “LeanDojo: Theorem proving with
notation, or configuration. Therefore, these failures do not             retrieval-augmented language models,” in Advances in Neural Information
                                                                         Processing Systems 36, 2023, datasets and Benchmarks Track.
measure logical reasoning alone.                                     [7] Ł. Czajka and C. Kaliszyk, “Hammer for Coq: Automation for dependent
   The automation baseline uses only auto, eauto, and                    type theory,” Journal of Automated Reasoning, vol. 61, no. 1–4, pp. 423–
                                                                         453, 2018.
intuition auto. It provides a basic comparison but does
not represent stronger, specialized, or expert-designed Coq
