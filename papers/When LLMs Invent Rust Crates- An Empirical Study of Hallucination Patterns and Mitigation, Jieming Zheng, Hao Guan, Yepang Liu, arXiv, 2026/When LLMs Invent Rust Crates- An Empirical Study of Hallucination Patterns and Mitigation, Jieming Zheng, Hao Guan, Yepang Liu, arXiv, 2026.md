                                                      When LLMs Invent Rust Crates: An Empirical Study of
                                                            Hallucination Patterns and Mitigation
                                                          Jieming Zheng                                              Hao Guan                                   Yepang Liu∗
                                              Southern University of Science and                               Nankai University                    Southern University of Science and
                                                        Technology                                               Tianjin, China                               Technology
                                                      Shenzhen, China                                       hao.guan@nankai.edu.cn                          Shenzhen, China
                                                12432728@mail.sustech.edu.cn                                                                             liuyp1@sustech.edu.cn

                                         Abstract                                                                            across various popular LLMs (e.g., ChatGPT, CodeRL, CodeGen).
                                         Large Language Models (LLMs) have become powerful tools for                         Such hallucinations can have important reliability and security im-
                                         code generation, yet they remain prone to hallucinations—producing                  plications: fabricated or misleading code, including incorrect APIs
                                         plausible but incorrect or fabricated outputs. Among these, pack-                   and dependency-related suggestions, may introduce build failures,
                                         age hallucination, where an LLM suggests non-existent dependen-                     vulnerable implementation choices, or downstream opportunities
                                         cies, poses an emerging security risk to the software supply chain.                 for adversarial exploitation. As a result, hallucination-driven at-
                                         While previous studies focus on popular languages like Python or                    tacks have emerged as a new and urgent topic in software supply
                                         JavaScript, in this work we present the first large-scale empirical                 chain security research [20, 39, 46].
arXiv:2606.08444v2 [cs.SE] 14 Aug 2026




                                         study on crate hallucination in LLM-generated Rust code. We con-                       A critical weakness of code-generating LLMs is package hal-
                                         struct a multi-source dataset combining coding tasks from Stack                     lucination: the model recommends or imports a dependency that
                                         Overflow, GitHub, and LLM-generated tasks, and evaluate both                        does not actually exist [39]. Spracklen et al. [39] proposed a threat
                                         commercial and open-source models under various decoding set-                       model based on package hallucination, in which an adversary can
                                         tings. Our analysis reveals that, unlike prior findings in Python and               pre-register a malicious package under a hallucinated identifier so
                                         JavaScript, hallucination behavior in Rust follows a distinct pattern:              that users who follow the LLM-generated recommendation may
                                         different models exhibit surprisingly consistent hallucination rates,               inadvertently introduce a supply-chain compromise.
                                         and these rates show minimal sensitivity to model parameters. Fur-                     In this paper, we also focus on studying package hallucination
                                         thermore, we investigate prompt engineering strategies to mitigate                  within the context of code generation. Existing research on package
                                         hallucinations without sacrificing code quality. This study provides                hallucination primarily focuses on the most popular languages (e.g.,
                                         new insights into the reliability and security implications of LLM-                 Python, JavaScript), while paying little attention to less popular
                                         assisted Rust development, offering guidance for future research                    languages like Rust [20, 39]. Rust is typically adopted for system-
                                         and safer model deployment in software engineering workflows.                       level programming, including operating systems, browsers, and
                                                                                                                             blockchain protocols, where security is of paramount importance.
                                         CCS Concepts                                                                           The threat model introduced by prior work [39] is compelling,
                                                                                                                             but it manifests differently in Rust. In Rust, downloading an external
                                         • Software and its engineering → Automatic programming;
                                                                                                                             crate requires an explicit dependency declaration in Cargo.toml.
                                         Empirical software validation; Software libraries and repositories.
                                                                                                                             Referencing that crate in .rs source files alone does not trigger its
                                         Keywords                                                                            download. Therefore, a hallucinated crate reference in Rust code
                                                                                                                             should not be interpreted as direct evidence that a malicious pack-
                                         Large language models, package hallucination, Rust crates, software                 age would be fetched or installed. Even so, it is still practically
                                         supply chain                                                                        important to study such hallucinated crate references. They are a
                                                                                                                             direct reliability problem, since invalid crate references can lead
                                         1    Introduction                                                                   to unresolved imports, incorrect namespace usage, and build fail-
                                         With the rapid rise of generative AI, Large Language Models (LLMs)                  ures. In addition, many LLM-assisted coding workflows generate
                                         have been widely adopted for code generation [12, 17, 38]. Program-                 source-code snippets, functions, or single-file examples rather than
                                         mers now rely on LLMs more than ever for coding. Automated                          complete Rust projects with fully specified Cargo.toml manifests.
                                         code generation powered by LLMs can boost developer productiv-                      As a result, source-level crate references often serve as the earliest
                                         ity and reduce avoidable human errors during software develop-                      observable signal and an upstream precursor of dependency-related
                                         ment [30, 32]. However, hallucination remains a critical drawback                   confusion, while dependency-resolution decisions occur only later
                                         of LLMs, resulting in outputs that appear plausible but are factually               through searches on crates.io, package-management tools, or man-
                                         incorrect, logically unsound, or entirely fabricated [13].                          ual crate additions. Motivated by this distinction, our study focuses
                                            In the specific context of code generation, Liu et al. [24] recently             on characterizing crate hallucinations at the source-code reference
                                         grouped hallucinations into three main categories: 1) intent conflict-              level in Rust.
                                         ing, 2) context deviation, and 3) knowledge conflicting. Their study                   The lack of research on LLM hallucinations in Rust code gen-
                                         further shows that code-generation hallucinations are widespread                    eration may lead to the following consequences: (1) we cannot
                                         ∗ Corresponding author. Jieming Zheng and Yepang Liu are affiliated with Research   determine whether the hallucination patterns observed in other
                                         Institute of Trustworthy Autonomous Systems and Department of Computer Science      language ecosystems also manifest in Rust; (2) we lack evidence
                                         and Engineering at SUSTech.
                                                                                                            Jieming Zheng, Hao Guan, and Yepang Liu


to discover new hallucination modes that may arise from Rust’s                In code generation scenarios, hallucinations manifest as syntac-
unique scenarios; and (3) we are unable to design or evaluate miti-       tically well-formed or semantically plausible code that relies on
gation tools that are truly effective for Rust developers.                fabricated, non-existent, or contextually misaligned elements, mak-
   To bridge this research gap, we present the first large-scale eval-    ing them difficult to detect through manual inspection alone [10, 44].
uation of crate hallucinations of Rust code generated by both com-        In programming, these hallucinations are often categorized as: (1)
mercial and open-source LLMs. In response to the lack of prior            intent conflicting, where the generated code deviates from the user’s
work on Rust, we propose the following research questions (RQs):          task requirements and shows low semantic relevance; (2) context
                                                                          deviation, where the code misaligns with the given context or the
     • RQ1 (Prevalence of Crate Hallucinations): How likely
                                                                          model’s own earlier outputs; and (3) knowledge conflicting, where
       are LLMs to hallucinate when recommending Rust crates?
                                                                          the output violates domain facts or programming conventions [24].
       How do model family, model size, and decoding parameters
                                                                          Recently, the growing popularity of “vibe coding” has encouraged
       affect this likelihood?
                                                                          more users to rely on LLMs to generate and iteratively refine code
     • RQ2 (Common Hallucination Patterns): What recur-
                                                                          from natural-language intents [35]. However, multiple empirical
       ring patterns can be observed in Rust crate hallucinations,
                                                                          studies have shown that even advanced coding assistants still hal-
       and what shared characteristics do these errors exhibit?
                                                                          lucinate [25, 48, 49]. As a result, this problem has attracted increas-
     • RQ3 (Mitigation of Crate Hallucinations): Can we lever-
                                                                          ing attention, motivating a rapidly expanding body of work on
       age common prompt engineering strategies to mitigate Rust
                                                                          systematically characterizing code hallucinations and developing
       crate hallucination?
                                                                          detection and mitigation techniques to improve the reliability of
   These questions aim to fill the gap in understanding crate hallu-      LLM-generated code [10].
cinations in Rust, offering insights into model behavior, parameter           Package Hallucination. Package hallucination is a type of
sensitivity, error classification, domain-specific variations, and mit-   knowledge-conflicting hallucination in code generation. It refers
igation strategies. To answer them, we studied crate hallucinations       to scenarios where an LLM recommends non-existent or incorrect
on 14 models from six model families using a multi-source Rust cod-       package names while generating code [39]. This issue is particu-
ing task dataset containing 2,794 coding tasks. Our study yielded         larly noteworthy because dependency suggestions often appear
interesting findings. Regarding prevalence (RQ1), we found that           plausible, leading users who trust LLM-generated code to directly
crate hallucinations remain consistent across model families, model       install the package if it becomes available. Recent studies have
sizes, and decoding parameters. From these crate hallucinations, we       shown that such hallucinated package names are highly prevalent
identified four recurring, Rust-specific hallucination patterns that      in LLM-generated code, and this phenomenon spans different model
suggest structured confusions (RQ2). Finally, we found that com-          types and programming languages [20, 39]. Beyond correctness,
mon mitigation strategies at the prompting stage, such as RAG and         package hallucination introduces a concrete supply chain threat:
self-refinement, cannot effectively reduce the likelihood of crate        attackers can register a package under a hallucinated name with ma-
hallucination (RQ3), suggesting the need for more sophisticated           licious code, turning an LLM’s fabricated recommendation into an
techniques to prevent crate hallucination.                                installation-time attack. Such an attack is called a package confusion
   In summary, we make the following contributions in this paper.         attack [28]. Given that many users may utilize LLM-generated code
                                                                          without careful review, this creates substantial opportunities for
     • To the best of our knowledge, we are the first to conduct a
                                                                          such attacks [2, 37]. Given its pervasiveness, cross-model impact,
       systematic empirical study on crate hallucination in LLM-
                                                                          and tangible supply chain risks amplified by developers’ unchecked
       generated Rust code.
                                                                          reliance on LLM outputs, package hallucination emerges as a criti-
     • We conducted our empirical study on a large-scale coding
                                                                          cal and understudied problem that demands systematic research to
       task dataset, with a wide range of large language models.
                                                                          mitigate its threats to software security and reliability.
     • We identified four recurring patterns of crate hallucination
                                                                              Rust. Rust is a systems programming language designed to
       and found common prompting-stage mitigations ineffec-
                                                                          provide strong memory-safety guarantees without relying on a
       tive.
                                                                          garbage collector, largely enabled by its ownership and borrowing
     • We constructed a dataset containing 2,794 Rust coding tasks.
                                                                          model [42]. These features have made Rust as a high-performance
       We release this dataset to the public to facilitate future
                                                                          substrate for modern developer tooling, leading to the emergence of
       research in this domain.
                                                                          various Rust-based alternatives within established ecosystems. For
                                                                          example, projects like Polars [33] and uv [5] for Python, as well as
2   Background                                                            Deno [8] and SWC [41] for JavaScript, have gained widespread pop-
Hallucinations in Code Generation by LLMs. LLM hallucina-                 ularity by delivering significantly higher performance than legacy
tion is the phenomenon where a model generates unfaithful or              implementations. This growing reliance on Rust-based infrastruc-
nonsensical content [16]. Hallucinations are commonly categorized         ture underscores the importance of the security and integrity of its
into three types: (1) input-conflicting hallucinations, which deviate     library ecosystem.
from the user-provided input; (2) context-conflicting hallucinations,         In practice, Rust development heavily relies on Cargo and the
which contradict the model’s own earlier outputs; and (3) fact-           crates.io ecosystem, where functionality reuse is commonly achieved
conflicting hallucinations, which are inconsistent with established       by adding third-party crates. At the language level, a crate is a
world knowledge or cannot be verified [48]. Moreover, this phe-           unit of compilation and distribution and contains a tree of nested
nomenon is typically driven by data, training, and inference [13].        module scopes. This crate–module structure and Rust’s path-based
When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation


                                                                                                   Rust Function
naming conventions interact closely with dependency-related hal-
                                                                                                   /// Return a SHA-256 hex digest of `input`.
lucinations. First, Rust distinguishes crates (external dependency                                 /// Use lowercase; no external state.
units) from modules (in-crate namespaces), yet both may appear
                                                                                                   pub fn sha256_hex(input: &str) -> String { /* ... */ }
in similar path-based forms in code, which can foster structured
confusions such as treating standard library modules as external
                                                                                                   Generated Coding Task
crates [42]. Second, adding a dependency is not purely declarative:
                                                                                                   Instruction: Complete the following Rust function.
Cargo compiles and executes build.rs as part of the build process,                                   Signature: pub fn sha256_hex(input: &str) -> String
and procedural macros run at compile time over Rust syntax, so                                            Task: Return a SHA-256 hex digest of input;
                                                                                                                Use lowercase; no external state.
adding an unintended crate can have security implications even
before the program runs [31]. More broadly, recent studies show
                                                                                            Figure 1: Converting a Rust Function into a Coding Task
that LLMs can hallucinate packages or crates during code genera-
tion and that adversaries may exploit hallucinated or confusingly
similar names to mount supply chain attacks. The Rust ecosystem
has also seen official reports of malicious crates [31], underscoring                  and ty [4], all of which are Rust-implemented, high-performance
the practical relevance of this security risk.                                         Python developer tools). To enrich the diversity of programming
                                                                                       tasks, we apply random sampling and manual inspection to en-
3     Data Collection                                                                  sure the selected projects span a range of functionalities. From this
                                                                                       curated pool, we sample 10 repositories for downstream processing.
In this section, we detail our approach to collecting and construct-
                                                                                           For each of these 10 repositories, we transform repository arti-
ing the datasets utilized in our study. Additionally, we discuss the
                                                                                       facts into coding tasks by extracting function-level documentation.
rationale for selecting the subject models.
                                                                                       Specifically, we extracted all the function definitions from .rs files
                                                                                       and selected those documented with RustDoc comments. To create
3.1     Collecting Coding Tasks                                                        each coding task, we pair the extracted brief instruction with its
To effectively evaluate package hallucinations in Rust code genera-                    corresponding function signature. Figure 1 illustrates the conver-
tion, we need a coding task dataset that offers broad coverage of                      sion from a Rust function into a coding task. For selected functions,
programming tasks, Rust-specific contexts, and scenarios where                         we extracted function definitions with RustDoc comments from
the use of external crates is natural or recommended. To this end,                     all Rust source files. Each function’s RustDoc summary and signa-
we constructed a large-scale task dataset from three different data                    ture form a coding task, ensuring tasks are grounded in real-world,
sources. Our dataset encompasses a wide range of programming sce-                      well-specified code. This yielded 1,011 coding tasks.
narios, capturing both real-world developer needs and synthetically                        To ensure the quality and generality of the coding tasks, we
generated tasks.                                                                       applied a second-pass, rule-based review to the comment-derived
   Stack Overflow Coding Tasks. Stack Overflow [40] is a                               tasks with the following rules.
prominent developer Q&A platform where questions are tagged                                Vague or underspecified task. These tasks lack sufficient detail,
and ranked by community feedback. We leverage this data source                         such as I/O behavior or clear semantics, making them unfit for
to obtain practical, user-driven Rust coding needs that reflect au-                    general-purpose evaluation. For example, RustDoc like “Create a
thentic developer inquiries and real-world challenges. Rust-related                    dummy node” is too vague to be an actionable coding task.
questions are collected by querying posts tagged with Rust and                             Compiler internals. Tasks that are only meaningful within the
ranking them according to community votes. Our objective is to                         compiler’s source-code context, often involving internal types, are
produce a global ranking of the most upvoted Rust questions. This                      excluded.
approach prioritizes widely validated, general-purpose questions                           FFI/ABI or OS-specific constraints. Tasks that require platform-
that are likely to translate into practical, model-ready tasks. To                     bound ABIs or system-specific behavior reduce portability and
ensure focus and stability, we retain only unique question entries                     evaluability.
and remove duplicates across pages. Applying this process yields                           Test directives (harness/build scripts). Tasks mixing compile
1,001 unique Rust questions, which constitute the Stack Over-                          flags or FileCheck-like directives do not represent implementable
flow component of our coding task dataset. We observe that not                         requirements. For example, functions with “CHECK-NEXT:” com-
all questions retrieved from Stack Overflow by this method are                         ments are unsuitable for general code-generation evaluation.
strictly coding tasks. Following Spracklen et al.’s work [39], we do                       Following these rules, we removed 218 items from the initial
not apply further filtering to these questions, but instead instruct                   1,011 coding tasks, leaving 793 for experiments.
the LLM to produce code wherever possible.                                                 LLM-generated Coding Tasks. Many third-party libraries are
   GitHub Coding Tasks. GitHub [11] hosts real-world open-                             created to solve a specific set of programming tasks, and their
source projects with rich code, comments, and usage context. We                        package descriptions explicitly summarize the provided functional-
leverage this platform to collect project-grounded tasks that reflect                  ity and typical use cases. Therefore, package descriptions offer a
realistic developer needs and implementation details observed in                       practical source for constructing dependency-related coding tasks.
production code. To construct our dataset, we first query GitHub                       In particular, a crate description summarizes the capability the li-
for Rust repositories and rank the results by the number of stars, se-                 brary provides and the scenarios it targets, which can be naturally
lecting the top 100 projects. However, we observe that many highly                     rewritten into an implementation request. This makes crate de-
starred repositories are functionally similar (e.g., uv [5], ruff [3],                 scriptions a scalable and consistent way to construct tasks where
                                                                                                           Jieming Zheng, Hao Guan, and Yepang Liu


           Table 1: Information of Evaluated Models                       Open-source Models. Based on the EvalPlus leaderboards,
                                                                        we choose Qwen2.5-Coder, DeepSeek-Coder-V2, and OpenCoder,
                                                            Open-       which are among the top-performing open-source code models
   Model                Vendor             Model Size       Source      under this evaluation.
   GPT-5                OpenAI              Unknown           ×
   Gemini 2.5 Pro       Google              Unknown           ×         4     RQ1: Prevalence of Crate Hallucinations
   Claude 4 Opus        Anthropic           Unknown           ×
   Qwen2.5-coder        Alibaba           0.5B, 1.5B, 3B,     ✓         In this section, we first describe how we detect crate hallucinations
                                           7B, 14B, 32B                 in LLM-generated Rust code, followed by the experimental setup
   DeepSeek-Coder-V2    High-Flyer          16B, 236B         ✓         and evaluation environment. We then report the results for RQ1 and
   OpenCoder            INF Technology       1.5B, 8B         ✓         provide an analysis of how model family, model size, and decoding
                                                                        parameters relate to the likelihood of crate hallucinations.

                                                                        4.1     The Approach of RQ1
the expected solution requires introducing external dependencies.
Moreover, sampling crates from registries allows us to cover a          RQ1 aims to measure how often LLMs hallucinate when recom-
broader range of different domains and dependency names. Mo-            mending Rust crates and to compare hallucination rates across
tivated by these considerations, we construct an LLM-generated          models. Specifically, we evaluate the six models listed in Section 3.2
coding task set by transforming the descriptions of selected crates     on three datasets. All models are run with their default configu-
into implementation-oriented tasks.                                     rations. For open-source models, we select the largest available
    Inspired by the approach of Spracklen et al. [39], which rewrites   parameter count. To answer RQ1, for each model’s generated code,
popular package descriptions into tasks, we construct a Rust LLM-       we apply the following hallucination-detection procedure.
generated coding task set as follows. To better reflect real-world         Detection of Crate Hallucinations. To ensure accurate de-
usage, we select the popular crates from the popularity ranking on      tection of crate hallucinations, we constructed a comprehensive
lib.rs. However, since the popularity ranking on lib.rs exposes only    inventory of existing Rust crates following the steps listed below.
the top 250 crates, we adopt a mixed collection strategy: we take the          • We first scraped the complete list of crate names available
top 250 crates from lib.rs (Popular) and supplement them with 750                on crates.io, which is the official Rust package registry.
crates from crates.io, which are ranked by recent downloads (dedu-             • Second, the Rust Standard library [43] consists of five built-
plicating overlaps). Subsequently, we employed the Qwen2.5:32B                   in crates (alloc, core, proc_macro, std, and test) that
model to transform each crate description into exactly one coding                are not distributed via crates.io. We supplement the crate
task: an English sentence beginning with the fixed prefix “Gen-                  name list crawled in the first step with those five names
erate Rust code that . . . ”. This procedure helped us produce 1,000             obtained from the documentation.
LLM-generated coding tasks.                                                    • Next, we collected the set of rustc compiler crates (e.g.
                                                                                 mdman, rustc_abi) from the Rust compiler documenta-
3.2    Model Selection                                                           tion [36], as these crates can also be used in Rust program-
We evaluate crate hallucinations across multiple LLMs to under-                  ming.
stand whether the phenomenon is model-dependent and to im-                     • A further complication in the Rust ecosystem is that a pack-
prove the generalizability of our findings. To cover both widely                 age’s published name on crates.io may differ from the crate
used proprietary assistants and reproducible open-source alterna-                name used in Rust programs. Such aliases should be de-
tives, we select models from two categories: commercial LLMs and                 clared in the Cargo.toml file of a Rust project’s repository.
open-source code LLMs.                                                           To address this issue, we mined all repositories of our col-
   We select models using public code-generation leaderboards as                 lected crates to extract those alternative names and merged
a practical criterion, aiming to evaluate crate hallucinations on                them into our crate name list. Because a small subset of
strong coding models rather than on weak baselines. Specifically,                packages either do not provide a valid GitHub repository
we rely on two widely used benchmarks for model selection: SWE-                  link or the provided link does not work, our alias coverage
bench Verified [18] for commercial assistants and EvalPlus [25] for              may not be fully complete. Consequently, in our study, the
open-source code LLMs.                                                           true hallucination rate of the LLM-generated Rust code is
   SWE-bench Verified is a widely used benchmark for software-                   likely slightly lower than the reported rate.
engineering tasks with verification-based scoring, and it is com-
                                                                          To extract crate names from LLM-generated Rust code, we rely
monly used to compare mainstream proprietary assistants. EvalPlus
                                                                        on three reference patterns:
extends HumanEval-style evaluations with stronger test suites and
stricter checking, and it has been widely adopted in recent work              (1) Use declarations (use crate_name::*;)
for comparing open-source code models [14, 15, 26, 39].                           Example: use serde::Serialize;
   Commercial Models. Based on the SWE-bench Verified leader-                 (2) Direct path prefixes (crate_name::module::item)
board, we choose Claude 4 Opus, GPT-5, and Gemini 2.5 Pro, which                  Example: tokio::spawn;
represent top-performing proprietary assistants from Anthropic,               (3) External crate declarations (extern crate crate_name;)
OpenAI, and Google, respectively.                                                 Example: extern crate regex;
When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation


                                                                                       Table 2: Hallucination Rate by Model Size Across Different
                                                                                       Model Families

                                                                                       Model Family                  Model Size           Hallucination Rate
                                                                                                                            16B                          18.46%
                                                                                       DeepSeek-Coder-V2
                                                                                                                           236B                          21.92%
                                                                                                                            1.5B                         19.54%
                                                                                       OpenCoder
                                                                                                                              8B                         19.28%
                                                                                                                            0.5B                         20.41%
                                                                                                                            1.5B                         21.62%
                                                                                                                              3B                         18.78%
                                                                                       Qwen2.5-Coder
                                                                                                                              7B                         20.83%
                                                                                                                            14B                          21.36%
                                                                                                                            32B                          20.07%
Figure 2: Crate Hallucination Rates of the Evaluated Models

                                                                                           The effect of model size. In the second experiment, our goal
We then compare the crates extracted by our parser with the list                       is to quantify, within each LLM family, the relationship between
we constructed following the approach described above.                                 model size (i.e., parameter count) and the crate hallucination rate,
  Metrics. We introduce the following metric to quantify the                           testing whether larger models would demonstrate lower CHRs.
degree of hallucination in a consistent and comparable way across                      Specifically, we evaluate the three open-source models listed in
prompts and models. Our idea is straightforward. Any extracted                         Section 3.2, along with all of their size variants available on Ollama
name that is absent from the crate name list built following the                       (DeepSeek-Coder-V2: 16B/236B; OpenCoder: 1.5B/8B; Qwen2.5-
above process is labeled as a hallucinated crate. Thus, the crate                      Coder: 0.5B/1.5B/3B/7B/14B/32B).
hallucination rate (CHR) for a model can be computed as follows.                           As shown in Table 2, our experimental results indicate that model
                     Number of hallucinated crates                                     size does not correlate with reduced hallucination rates across
               CHR =                                                                   the evaluated model families. Since Qwen2.5-Coder is the only
                    Total number of extracted crates
   Environment. All the experiments are carried out on a Linux                         evaluated family with more than two size variants, we further
server equipped with an AMD EPYC 9654 96-Core Processor, along                         conduct an ANOVA-style F-test [9] under a linear model on this
with 8 NVIDIA RTX 6000 Ada GPUs and 768 GB of system memory.                           family to assess whether model size explains the observed CHR
                                                                                       variation. The result shows no statistically significant effect of
4.2     Empirical Study Results                                                        model size with 𝐹 (1, 4) = 0.0138, 𝑝 = 0.912. The corresponding
                                                                                       effect size is also negligible, with 𝑅 2 = 0.0034. These results indicate
In the experiment, we generated a total of 16,764 code snippets and
                                                                                       that, within the Qwen2.5-Coder family, parameter count explains
extracted 48,494 crate recommendations. Of these recommended
                                                                                       almost none of the variation in CHR.
crates, 10,779 were identified as hallucinations, yielding an overall
                                                                                           We hypothesized that larger models would demonstrate lower
hallucination rate (CHR) of 22.23%.
                                                                                       CHRs; however, the result does not support this hypothesis. Within
   Overall, we observe that cross-model differences in CHR are not
                                                                                       the three families considered, model size is not a reliable predictor of
significant, though a few models achieve markedly lower CHR. As
                                                                                       hallucination rate in crate recommendation. The effect of model size
shown in Fig. 2, Gemini-2.5-Pro achieves an CHR of 16.18% (the
                                                                                       is small and statistically insignificant. One plausible explanation is
best) and Claude-4-opus’s CHR is 26.90% (the worst). The ratio of
                                                                                       insufficient Rust coverage in pretraining or instruction data, which
worst to best is about 1.66, indicating that model choice is a very
                                                                                       would limit the marginal benefit of additional parameters.
important factor. Selecting suitable models can significantly boost
the trustworthiness of the generated Rust code.                                         Finding 2. For our tested open-source models, there is no sta-
   In the comparison between commercial and open-source models,                         tistically significant correlation between model size and crate
the average overall CHR for commercial models is 23.34% and that                        hallucination rate.
for open-source models is 20.79%, indicating a slight advantage
for open-source models. Also, we found that Gemini-2.5-Pro is an                          The effect of temperature. We next investigate whether the
outlier and excluding it yields a commercial macro-averaged CHR                        sampling temperature parameter influences hallucination rate in
of 25.23%, making the higher CHR of commercial models more                             Rust-crate recommendation. Temperature controls how random the
apparent compared to open-source models.                                               model’s output is: lower values give more deterministic, repeatable
                                                                                       answers, while higher values encourage more diverse and creative
 Finding 1. Crate hallucinations are widespread and observed                           generations. Here, we hypothesize that increasing the decoding
 across all the six selected LLMs. When generating Rust code, the                      temperature will raise the CHR. However, we observed that for
 overall differences in CHR between commercial and open-source                         Rust code generation, both open-source and commercial models
 models are not large; however, certain commercial models achieve                      show only marginal sensitivity to temperature. As shown in Fig.
 notably lower CHRs.                                                                   3, the CHRs of all four models remain within a narrow range of
                                                                                                               Jieming Zheng, Hao Guan, and Yepang Liu


16.2%–26.1%, exhibiting small, inconsistent fluctuations rather than          Table 3: Top-10 Hallucinated Crate Names by All Models
a clear upward trend. For example, the CHR of Qwen2.5-Coder:32B
fluctuates mildly between 20.65% and 21.10% as the temperature               Crate               Frequency         Crate                 Frequency
increases from 0 to 5, exhibiting no monotonic trend. Among all
                                                                             thread                    1,086       trefcell                       296
models, Gemini-2.5-Pro shows a slightly wider fluctuation range,             duration                    828       tu32                           282
but the change is still modest and not statistically significant.            tokenstream                 505       ttcplistener                   277
   To formally examine the effect of temperature, we conduct an              ordering                    418       thashset                       257
ANOVA test using the temperature settings shared by all four eval-           vecdeque                    323       tpoll                          236
uated models, i.e., 0, 0.5, 1, 1.5, and 2. Since different models exhibit
different baseline CHRs, we include model identity as a blocking
factor and test the effect of temperature under the model CHR
∼ Model + Temperature. The ANOVA result shows that temper-                   helping explain how cross-ecosystem priors may shape erroneous
ature does not have a statistically significant effect on CHR with           Rust dependency suggestions.
𝐹 (4, 12) = 0.9159, 𝑝 = 0.4859. In contrast, the model factor is statisti-
cally significant with 𝐹 (3, 12) = 5.0425, 𝑝 = 0.0173, which suggests
                                                                             5.1     General Hallucination
that the observed variation is better explained by model differences
than by temperature settings. These results indicate that changing           Our analysis reveals a critical finding: over half of the hallucinated
decoding temperature leads only to small and inconsistent fluctu-            crates are actually valid Rust modules that exist in the standard
ations rather than a systematic effect on crate hallucination rate.          library or third-party crates, but are being misused or referenced
This observed stability contrasts with prior findings in Python and          in an unqualified way. This suggests that the primary issue is not
JavaScript [39], where higher temperature often leads to increased           the generation of completely non-existent packages, but rather the
hallucination rates.                                                         improper usage of existing modules. A module in Rust provides
                                                                             a hierarchical namespace that organizes and encapsulates code
 Finding 3. Unlike the findings in Python and JavaScript reported            within a crate. For example, ubiquitous data structures HashMap and
 in previous work, for Rust, the correlation between temperature             LinkedList are encapsulated within the std::collections mod-
 and crate hallucination rate is statistically weak.                         ule. The LLM-generated code may directly call HashMap::new with-
                                                                             out declaring use std::collections::HashMap in advance. This
   Answer to RQ1. In summary, crate hallucination is prevalent               issue of incorrect reference extends to numerous other standard
in LLM-generated Rust code. Across our experiments, the overall              library modules, including std::io, std::thread, and std::net.
crate hallucination rate stays around 20%, and all evaluated models
exhibit non-trivial hallucinations. Although the rate varies across           Finding 4. Many hallucinated crate names are actually valid
models, we do not observe a consistent trend by model family or               Rust modules that exist in the standard library, but are being
by whether the model is commercial or open-source. Within the                 incorrectly referenced.
open-source models we tested, increasing parameter count does
not substantially reduce hallucination. Moreover, changing decod-               Table 3 identifies the top ten hallucinated crates, ranked by their
ing temperature only leads to small and inconsistent differences.            aggregate frequency of appearance within the generation for the
Overall, crate hallucinations in Rust appear relatively stable under         coding tasks. Notably, the majority of these names correspond to
model size and decoding-time adjustments.                                    legitimate modules within the Rust standard library. This indicates
                                                                             that nearly half of all hallucinations (45.47%) are not entirely fabri-
5    RQ2: Recurring Hallucination Patterns                                   cated identifiers but rather cases where the model incorrectly treats
RQ2 aims to characterize recurring patterns in Rust crate halluci-           an internal module as an external crate dependency. Such errors
nations and to examine the shared characteristics of these errors.           suggest that the model partially recognizes semantically valid Rust
We conduct four complementary analyses that together reveal how              entities, yet fails to represent their hierarchical position within the
these hallucinations are structured in practice:                             language’s namespace system.
   General analysis. We separate broad classes of hallucinated                  This pattern suggests that LLMs may overgeneralize import
references to obtain an overall picture of what kinds of errors              conventions from languages such as Python, where modules and
occur, especially whether the model is fabricating external crates           packages share similar import syntax, into Rust, which enforces a
or misusing existing Rust modules.                                           stricter separation between crates and modules. This implication is
   Cross-model analysis. We measure how much hallucinated                    consistent with our previous findings that many hallucinated crate
crate names overlap across different models, which helps distin-             names correspond to valid standard-library modules, indicating
guish systematic weaknesses from model-specific mistakes.                    that the model captures their semantics but misrepresents their
   Name similarity analysis. We examine lexical similarity be-               scope within the import hierarchy.
tween hallucinated names and real crates to test whether hallucina-             From a software supply chain perspective, although module-level
tions tend to be near-miss variants, which is relevant for practical         hallucinations are less likely to result in malicious packages, they
risk and mitigation design.                                                  still pose challenges for automatic dependency management and
   Cross-domain analysis. We inspect frequent hallucinations for             build reliability. Recent work also [34] showed that LLM-generated
plausible transfer from other language ecosystems or platform APIs,          code often faces compilation errors and dependency issues.
When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation


                                                        Gemini 2.5 Pro                                                              GPT-5                                         DeepSeek-Coder-V2                                            Qwen2.5-Coder
      27.0                                                                                                 24.0                                                19.5                                                   21.3




      24.0                                                                                                 23.6                                                19.2                                                   21.0
CHR (%)




                                                                                                     CHR (%)




                                                                                                                                                         CHR (%)




                                                                                                                                                                                                                CHR (%)
      21.0                                                                                                 23.2                                                18.9                                                   20.7




      18.0                                                                                                 22.8                                                18.6                                                   20.4



      15.0                                                                                                 22.4                                                18.3                                                   20.1
          0                                      0.5           1                1.5              2                0        0.5        1        1.5   2             0   0.5    1   1.5    2      3     4     5             0    0.5   1   1.5     2      3      4   5
                                                        Temperature                                                              Temperature                                            Temperature                                            Temperature



                                                                   Figure 3: Hallucination Rates of Evaluated Models Across Different Temperature Settings

                                                        3062
                                         3K                                                                                                                        5.3        Name Similarity of Hallucination
                                                            2756
                                                                                                                                                                   To investigate the relationship between hallucinated crates and real
              No. of Hallucinated Packages




                                                     2375
                                                                                                                                                                   crates in the Rust ecosystem, we employed the Levenshtein distance
                                                               2015                                                                                                [22] as a quantitative measure of string similarity.
                                         2K
                                                                                                                                                                      As shown in Fig. 4, the results of the Levenshtein distance analy-
                                                                   1322
                                                                                                                                                                   sis indicate that hallucinated crate names in Rust are predominantly
                                                                                                                                                                   close variants of existing crates rather than entirely novel inven-
                                         1K                                                                                                                        tions. Among all 5,647 unique hallucinated names remaining after
                                                                          617                                                                                      excluding module-confusion cases (occurring 13,332 times in total),
                                                                                388
                                                                                      220263                                                                       the weighted mean distance to the nearest valid crate is 3.42. About
                                                                                               117
                                             0
                                                                                                                                                                   40.78% of hallucination occurrences differ by only one or two char-
                                                 0                    5                        10                     15                  20
                                                                                 Levenshtein Distance                                                              acters, and another 45.70% fall within a distance of three to five.
                                                                                                                                                                   Only 2.36% have a distance of ten or above, suggesting that most
Figure 4: Distribution of Levenshtein Distance Between Hal-                                                                                                        hallucinated crate names are minor variations involving limited
lucinated and Real Crate Names                                                                                                                                     character substitutions or omissions. In total, 86.48% of hallucina-
                                                                                                                                                                   tion occurrences are within five edits of an existing crate, reflecting
                                                                                                                                                                   a high concentration of near-miss cases.
                                                                                                                                                                      Further, we conducted a morphological analysis of these halluci-
                                                                                                                                                                   nations to understand the underlying patterns and mechanisms of
5.2                     Hallucination Across Models
                                                                                                                                                                   hallucination generation in the Rust ecosystem. The most promi-
Based on our prior analysis in Section 5.1, we conducted a cross-                                                                                                  nent finding is the systematic inconsistency in hyphen usage. Among
model analysis separating hallucinations into module and non-                                                                                                      13,332 total cases, we observe that 32.96% of hallucinated crates lack
module categories. We compute pairwise Jaccard similarities be-                                                                                                    hyphens while their corresponding real packages contain hyphens.
tween models for each category and quantify uniqueness by count-                                                                                                   This pattern suggests that the model tends to generate camelCase
ing how many models produce each hallucination item.                                                                                                               names, whereas the Rust ecosystem strongly favors kebab-case
   We found that module hallucinations exhibit substantially higher                                                                                                naming conventions. Representative examples include:
cross-model overlap: average Jaccard ≈ 0.44 (max ≈ 0.50). Consis-
tent with this, 55.05% of module hallucinations are shared across                                                                                                                         httpresponse          →             http-response
models, while 44.95% are unique. In contrast, non-module halluci-                                                                                                                            tokentree          →             token-tree
nations show much lower overlap—average Jaccard ≈ 0.16 (max                                                                                                                             servicebuilder          →             service-builder
≈ 0.21)—and most cases are not shared: only 25.42% are shared and                                                                                                                         genericarray          →             generic-array
74.58% are unique.                                                                                                                                                    Another finding is that among close matches (edit distance ≤
   These results indicate that module-related errors are more con-                                                                                                 3, 8,193 occurrences), 4,879 cases (59.6%) share common prefixes
sistent across models. A likely reason is that such errors may origi-                                                                                              with their nearest legitimate counterparts, while 5,697 cases (69.5%)
nate from the incompleteness of pre-training data. Thus, different                                                                                                 exhibit suffix similarity. This high degree of morphological over-
models tend to make similar confusions. Conversely, non-module                                                                                                     lap indicates that hallucinations are not randomly generated, but
hallucinations are more context-dependent and model-specific.                                                                                                      systematically constructed as variations of existing crate names.
                                                                                                                                                                   Examples demonstrating this pattern include:
   Finding 5. We found a moderate degree of overlap in crate hal-                                                                                                            downcast-ref             →   downcast-rs (prefix similarity),
   lucinations among models, with about half of module hallucina-                                                                                                            myenum                   →   tyenum (suffix similarity).
   tions being shared. This suggests that some hallucination patterns
   are common across different LLMs, though many remain model-                                                                                                        Our findings contrast sharply with prior studies for Python and
   specific.                                                                                                                                                       JavaScript [39], which report that nearly half of hallucinations have
                                                                                                                                                                   edit distances of six or more, while our Rust analysis shows that
                                                                                                                                                                   86.48% of hallucinations fall within five edits of legitimate packages.
                                                                                                          Jieming Zheng, Hao Guan, and Yepang Liu


This discrepancy suggests that Rust hallucinations are more tightly         Pre-processing strategies can generally be divided into two broad
clustered around existing names, potentially reflecting the more         categories: Prompt Engineering and Model Development [45]. In
standardized naming conventions in the Rust ecosystem and the            this work, we concentrate on the former because it is deployment-
model’s deeper internalization of Rust-specific patterns.                friendly (no weight updates, no extra training cost). Specifically,
                                                                         we employ two important methods of prompt engineering: Self-
 Finding 6. Unlike prior findings for Python and JavaScript, for         Refinement and Retrieval-Augmented Generation (RAG).
 Rust, most hallucinated crate names are minor variations of real           We chose RAG and self-refinement for the following reasons.
 crates (with a few character edits). A prominent pattern is the         First, in a relatively less popular ecosystem like Rust, models may
 misuse or omission of hyphens, with models often generating             not reliably remember real crates and their intended usage. RAG
 camel-case names instead of following the kebab-case convention         addresses this by incorporating an external source of crate names
 used in Rust.                                                           and descriptions and retrieving relevant evidence before generation,
                                                                         providing the model with grounded hints about existing crates
                                                                         rather than relying solely on its memory. Second, code outputs in
5.4    Hallucination Across Domains
                                                                         practice often go through review and iterative fixes. Self-refinement
To identify common patterns among frequently occurring halluci-          automates this process by asking the model to audit its own output
nations, we analyze non-module hallucinations that occurred more         after generation and to revise the solution when issues are found.
than 10 times using a fine-grained cross-domain criterion: a halluci-    Third, both approaches are training-free and require only standard
nated crate is considered “cross-domain” if its name clearly appears     inference access, without modifying model weights or accessing
in other programming language ecosystems or system/platform              internal parameters. This makes them portable across different
ecosystems (e.g., Windows API, Android SDK).                             models and convenient for controlled comparisons under the same
   Across the analyzed high-frequency hallucinated crates, we            evaluation metric.
found that 38.9% of them exhibit clear cross-domain character-              Self-Refinement. Self-Refinement is a prompt-level, inference-
istics. For instance, “queryparser” is from the Python ecosystem         time procedure in which an LLM first produces an initial plan/answer,
and “winuser” is from Windows API. This suggests that repeated           then re-evaluates it by running a second “review” prompt that asks
hallucinations are not purely random, but often stem from exposure       the model to check for issues. The model then revises the out-
to overlapping semantics across ecosystems, indicating structured        put based on this self-review, and this process can be repeated if
yet misaligned knowledge transfer.                                       needed [27]. We implement a verification-first, prompt-level self-
                                                                         refinement routine. At generation time, the prompt instructs the
 Finding 7. A substantial fraction of hallucinated crates reuse
                                                                         model to detect standard-library functionality and explicitly qual-
 names from other ecosystems.
                                                                         ify it via std::/core:: modules. When the model introduces an
   Answer to RQ2. Crate hallucinations in Rust exhibit clear recur-      external crate, it is asked to perform a self-check on the exact crate
ring patterns. A large portion of errors are Rust-specific confusions    name. If the model determines that the crate is a hallucination, it
where models generate unqualified references. Hallucinated crate         will regenerate the response with the instruction not to generate
names also show systematic reuse and structure: many recur across        the crate again, repeating this process up to 3 times.
different models, and a noticeable fraction appear as near-miss             Retrieval-Augmented Generation (RAG). RAG is a paradigm
variants of real crates, indicating that models often drift toward       that augments a parametric generator with a non-parametric re-
plausible-looking names instead of fabricating arbitrarily. Moreover,    triever to fetch task-relevant documents at inference time and
we observe an cross-ecosystem effect, where some hallucinated            generate conditions on the retrieved evidence, thereby improving
names resemble packages from other language ecosystems.                  factuality and mitigating hallucinations [23]. Considering the bal-
                                                                         ance between effectiveness and token cost, we construct a dataset
                                                                         from crates.io consisting of the top 10,000 crates ranked by recent
6     RQ3: Mitigation of Crate Hallucinations
                                                                         downloads. For each crate, we retain its canonical name and the
In RQ3, we evaluate two lightweight, language-sensitive interven-        description text provided on its crates.io page. When generating
tions to mitigate hallucinations. We keep the datasets and the de-       code, the database returns the top-five most relevant crates for the
tection pipeline unchanged and assess effectiveness solely by the        given task. In parallel, we inject a fixed “STD list” that grounds
change in CHR under controlled ablations, ensuring any improve-          common capabilities in the Rust standard library. The list is seeded
ment is attributable to the intervention rather than evaluation drift.   by the top-ten misused module names identified in RQ2, and it
                                                                         is used to discourage unqualified references in generation. When
6.1    Mitigation Strategies                                             generating code, this list is appended to the prompt alongside the
Our strategies focus on pre-processing rather than post-processing,      retrieved crate names, with an explicit policy that whenever the
which is fragile in adversarial settings. Attackers can obtain the       target capability is covered by the list, the model must use std and
name of a hallucinated package in advance, inject malicious code         refrain from adding an external crate.
into the package, and publish it to code repositories, which makes          We implemented these mitigation strategies using the open-
post-processing methods ineffective [39]. RQ2 also showed that           source models mentioned in Section 3.2, since they performed bet-
hallucinations cluster around (i) standard-library modules miscast       ter than the commercial models during the experiments in RQ1.
as external crates and (ii) near-miss names, suggesting that con-        Evaluation for commercial models is an important direction for
straining dependency choices during generation is more promising.
When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation


      Table 4: Performance of the Mitigation Strategies                                model capability across languages: when training follows a natu-
                                                                                       ral distribution, LLMs perform worse on low-resource languages.
Mitigation                DeepSeek          OpenCoder                Qwen2.5           Consistent with this, our RQ1 results suggest that decoding-time
                                                                                       parameter adjustments have limited impact on crate hallucination
No Mitigation                 21.92%               19.28%               20.07%
                                                                                       rates. We further conjecture that model performance on Rust is
RAG                   20.0% (-1.92%)      18.32% (-0.96%)      20.41% (+0.34%)         driven more by training-data coverage than by model architecture
Self-Refinement      18.66% (-3.26%)      17.06% (-2.22%)      17.76% (-2.31%)         or parameter settings, which helps explain why Rust can differ
                                                                                       from high-resource languages such as Python and JavaScript in
                                                                                       code generation behavior.
future work, but proprietary APIs may introduce additional cost,                          Structure of Rust Crate Hallucinations. Our empirical re-
access, and reproducibility constraints.                                               sults give the following key implications for understanding and
                                                                                       mitigating crate hallucinations in Rust. Crate hallucinations appear
6.2     Results                                                                        highly structured rather than purely arbitrary: many errors are tied
                                                                                       to Rust-specific ecosystem and namespace conventions, such as
Overall, both strategies reduce hallucinations for most evaluated
                                                                                       mistaking standard-library or module paths as external crates, or
models, but their effectiveness differs substantially. As shown in
                                                                                       producing near-miss crate names that resemble existing ones.
Table 4, self-refinement is consistently more effective than RAG, re-
                                                                                          Limited Impact of Decoding and Prompting. As mentioned
ducing crate hallucinations across all evaluated models. On average,
                                                                                       above, changing decoding settings during generation is unlikely
it lowers crate hallucinations by 2–3 percentage points, represent-
                                                                                       to substantially reduce hallucinations by itself, which motivates
ing a 10–15% relative reduction compared to each model’s original
                                                                                       mitigation strategies that incorporate stronger training-time or ex-
baseline. In contrast, RAG provides only limited and less consistent
                                                                                       ternal grounding mechanisms. While lightweight prompt-based
improvements across the evaluated models. This indicates that, un-
                                                                                       strategies can reduce hallucination rates for most models, the im-
der our current retrieval setup, RAG does not reliably suppress crate
                                                                                       provements are modest and not always consistent, indicating that
hallucinations and may be sensitive to retrieval quality and how
                                                                                       package hallucination may not be substantially alleviated by simple
well the retrieved evidence aligns with the model’s generation. The
                                                                                       prompting or pre-processing alone. More reliable mitigation likely
results of the two lightweight strategies suggest that, while both
                                                                                       requires tighter integration with toolchain-level verification.
approaches can help reduce hallucination rates for most models to
                                                                                          Directions for Rust-specific Mitigation. The modest improve-
some extent, crate hallucinations remain difficult to mitigate with
                                                                                       ments in RQ3 suggest that generic prompt-level methods are in-
simple, surface-level prompt interventions. This observation is con-
                                                                                       sufficient for fully mitigating crate hallucinations. We therefore
sistent with a prior study, which also reports that straightforward
                                                                                       view RAG and self-refinement as lightweight baselines rather than
prompting or lightweight pre-processing alone is often insufficient
                                                                                       complete Rust-specific defenses. A more effective mitigation strat-
to substantially eliminate package hallucinations [39].
                                                                                       egy should explicitly incorporate Rust’s crate/module namespace
 Finding 8. Both self-refinement and RAG reduce hallucination                          structure and Cargo-based dependency model.
 rates, but improvements are modest. Self-refinement is more ef-                          Based on our findings in RQ2, a Rust-aware guardrail can be de-
 fective, while RAG’s gains are limited.                                               signed around three components. First, it should perform namespace-
                                                                                       aware validation by distinguishing external crates from standard-
   Answer to RQ3. Both mitigation strategies reduce crate halluci-                     library modules, in-crate modules, and rustc crates. This directly
nations, but self-refinement is more consistently effective than RAG                   targets module-crate confusion, where valid Rust modules are in-
under our setup. Overall, lightweight prompting helps, but substan-                    correctly treated as external dependencies. Second, it should per-
tially mitigating Rust crate hallucinations likely requires stronger                   form registry-aware and near-miss checking against crates.io and
verification or tooling support beyond simple pre-processing.                          known aliases. Since many hallucinated names are close variants
                                                                                       of real crates, suspicious names can be flagged or corrected us-
7 Discussion                                                                           ing edit-distance and naming-convention checks. Third, it should
                                                                                       be Cargo-aware: source-level references should be cross-checked
7.1 Implications                                                                       with Cargo.toml, because Rust dependencies are resolved through
Training Data Richness Drives Model Performance. Cassano                               the manifest rather than by source imports alone. Overall, effec-
et al. [6] categorize programming languages in LLM-based code                          tive crate-hallucination mitigation should combine LLM generation
generation into high-resource and low-resource, based on how much                      with Rust-aware verification. Instead of relying only on retrieved
training data is available for each language. Public statistics sup-                   context, future coding assistants should validate whether a gener-
port this distinction: Rust is typically much smaller in scale than                    ated identifier is a crate, module, alias, or invalid dependency, and
mainstream languages such as Python and JavaScript. For example,                       then provide feedback for correction or regeneration.
the per-language statistics reported for The Stack dataset [19] show
that Rust accounts for a substantially smaller amount of data (on
the order of 40 GB) than Python (around 190 GB) and JavaScript                         7.2    Threats to Validity
(around 480 GB). Under this categorization, Rust is therefore a typi-                  The LLM evolves rapidly, so hallucination rates and model differ-
cal low-resource language. Prior work [29] also discussed how the                      ences observed within our evaluation window may not directly
distribution of programming languages in training data can affect                      generalize to newer models or more tool-integrated assistants. In
                                                                                                                  Jieming Zheng, Hao Guan, and Yepang Liu


addition, our results are based on a fixed set of models and a Rust-     et al. [39] and Krishna et al. [20] provided foundational empirical
specific prompt dataset constructed from selected sources. While         studies, focusing on mainstream languages such as Python and
these sources provide complementary coverage, they may not fully         JavaScript. They identified package hallucination as a prevalent
represent all Rust development contexts. To mitigate this threat, we     phenomenon, analyzed behavioral traits, and evaluated mitigation
evaluate multiple model families with different sizes, which adds        strategies. Both studies found that hallucination rates and patterns
confidence to our generalizability. For the synthetic task subset, it    depend on the model, its size, and language, but left open questions
is built by Qwen2.5-32B. This may introduce distribution bias for        regarding less-studied ecosystems. Beyond empirical studies, Zhao
model families related to the generator. However, in our aggregate       et al. designed HFuzzer [50], a fuzzing technique for systematically
results, we did not observe an obvious favorable outlier pattern for     testing LLMs for Python package hallucinations. This approach
the Qwen family. Our metric labels an extracted crate name as hal-       triggered more unique hallucinations and generated more diverse
lucinated if it is absent from the reference list. This may introduce    coding tasks than previous methods such as GPTFuzzer-A [47].
false positives when a model mentions an alias, an outdated name,           Together, these studies established a clear research trajectory,
or a non-crate identifier that is incorrectly parsed as a crate. False   from characterizing package hallucinations to advancing testing
positives may also occur when a model refers to private crates that      techniques. Extending this line of work, we investigate package
are not indexed by public registries. To reduce these risks, we use      hallucination in Rust, conduct a comprehensive evaluation, charac-
a consistent extraction pipeline and apply the same detection rule       terize its Rust-specific properties, and compare our findings with
across all settings. Although this does not eliminate mislabeling, it    those from more widely studied mainstream languages.
ensures that comparisons across models and mitigation settings are
made under the same operational definition and data-processing           9    Conclusion
procedure. Our study does not directly measure downstream con-
                                                                         In this work, we study crate hallucinations in LLM-generated Rust
sequences such as build failure rates, developer repair effort, or the
                                                                         code. We constructed a multi-source coding task dataset combining
exploitability of hallucinated crate names. Therefore, CHR should
                                                                         data from Stack Overflow, GitHub, and LLM-generated tasks,
be interpreted as a source-level indicator of dependency confusion
                                                                         which allowed us to cover a wide range of Rust coding tasks and
rather than direct evidence that a hallucinated reference will nec-
                                                                         dependency scenarios. We then evaluated Rust crate hallucinations
essarily lead to package installation or supply-chain compromise.
                                                                         across six LLM models to assess the impact of model family, model
                                                                         size, and decoding parameters. We found that crate hallucinations
                                                                         remain consistent across those parameters mentioned above. Our
8     Related Work                                                       results show that Rust crate hallucinations are highly structured
Our work draws inspiration from two lines of related work. We            rather than random, with many errors arising from Rust-specific
discuss them in this section.                                            conventions. While lightweight mitigation strategies such as self-
                                                                         refinement and RAG were found to reduce hallucination rates, the
8.1    Hallucination in Code Generation                                  improvements were modest and not always consistent. We hope our
Recent studies have begun to systematically characterize hallucina-      findings can provide insights for future research on package hallu-
tions in LLM-based code generation. Liu et al. [24] provide an early     cinations, enabling follow-up work to propose effective mitigation
taxonomy by sampling tasks from HumanEval [7] and DS-1000 [21].          strategies specifically tailored to the Rust language.
They categorize code hallucinations into three major types: intent-
conflicting, context deviation, and knowledge-conflicting. Extend-       10     Data Availability
ing beyond function-level tasks, Zhang et al. [49] argue that practi-    The task datasets, prompt templates, crate extraction scripts, eval-
cal development settings introduce richer failure modes and pro-         uation scripts, mitigation scripts, and result files in this study are
pose a taxonomy for repository-level generation that emphasizes          available via this link: https://doi.org/10.6084/m9.figshare.32233767.
requirement, factual, and project-context conflicts. Complementary
perspectives define hallucinations via execution outcomes: Tian et
al. [44] summarize runtime-oriented error categories (e.g., mapping,
                                                                         Acknowledgments
naming, resource, and logic failures) and introduce CodeHaluEval.        This work is supported by the National Natural Science Foundation
Agarwal et al. [1] organize hallucinations by defect types and con-      of China (Grant No. 62372219) and the Fundamental Research Funds
struct CodeMirage. Finally, a systematic review by Gao et al. [10]       for the Central Universities (No. 63261089).
synthesizes definitions and proposes a unified framework that high-
lights knowledge, functional, and environment/dependency-related         References
hallucinations, offering a consolidated view of the field.                [1] Vibhor Agarwal, Yulong Pei, Salwa Alamir, and Xiaomo Liu. 2025. CodeMirage:
    Overall, taxonomy-driven studies provide a shared vocabulary              Hallucinations in Code Generated by Large Language Models (2024). arXiv
                                                                              preprint arXiv:2408.08333 (2025).
and evaluation basis for systematically characterizing code halluci-      [2] Wadhah Al-Zofi. 2025. AI-Induced Supply-Chain Compromise: A Systematic
nations across tasks and models.                                              Review of Package Hallucinations and Slopsquatting Attacks. (2025).
                                                                          [3] Astral. n.d.. astral-sh/ruff: An extremely fast Python linter and code formatter.
                                                                              https://github.com/astral-sh/ruff. Accessed: 2026-01-22.
8.2    Package Hallucination                                              [4] Astral. n.d.. astral-sh/ty: An extremely fast Python type checker and language
                                                                              server. https://github.com/astral-sh/ty. Accessed: 2026-01-22.
Recent work has formalized package hallucination as a supply-             [5] Astral. n.d.. astral-sh/uv: An extremely fast Python package and project manager.
chain–relevant phenomenon in LLM-assisted coding. Spracklen                   https://github.com/astral-sh/uv. Accessed: 2026-01-22.
When LLMs Invent Rust Crates: An Empirical Study of Hallucination Patterns and Mitigation


 [6] Federico Cassano, John Gouwar, Francesca Lucchetti, Claire Schlesinger, Anders           Measuring the impact of programming language distribution. In International
     Freeman, Carolyn Jane Anderson, Molly Q Feldman, Michael Greenberg, Abhinav              Conference on Machine Learning. PMLR, 26619–26645.
     Jangda, and Arjun Guha. 2024. Knowledge transfer from high-resource to low-         [30] Ruchika Pandey, Prabhat Singh, Raymond Wei, and Shaila Shankar. 2024. Trans-
     resource programming languages for code llms. Proceedings of the ACM on                  forming software development: Evaluating the efficiency and challenges of github
     Programming Languages 8, OOPSLA2 (2024), 677–708.                                        copilot in real-world projects. arXiv preprint arXiv:2406.17910 (2024).
 [7] Mark Chen. 2021. Evaluating large language models trained on code. arXiv            [31] Walter Pearce. 2025. crates.io: Malicious crates faster_log and async_println.
     preprint arXiv:2107.03374 (2021).                                                        https://blog.rust-lang.org/2025/09/24/crates.io-malicious-crates-fasterlog-and-
 [8] Deno Land Inc. and Contributors. n.d.. denoland/deno: A modern runtime                   asyncprintln/ Rust Blog. Walter Pearce on behalf of the crates.io team. Updated
     for JavaScript and TypeScript. https://github.com/denoland/deno. Accessed:               Sept. 24, 2025.
     2026-01-22.                                                                         [32] Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. 2023. The impact
 [9] Ronald Aylmer Fisher. 1970. Statistical methods for research workers. In Break-          of ai on developer productivity: Evidence from github copilot. arXiv preprint
     throughs in statistics: Methodology and distribution. Springer, 66–70.                   arXiv:2302.06590 (2023).
[10] Cuiyun Gao, Guodong Fan, Chun Yong Chong, Shizhan Chen, Chao Liu, David             [33] Polars Contributors. n.d.. Polars User Guide. https://docs.pola.rs/. Accessed:
     Lo, Zibin Zheng, and Qing Liao. 2025. A Systematic Literature Review of Code             2026-01-22.
     Hallucinations in LLMs: Characterization, Mitigation Methods, Challenges, and       [34] Ravin Ravi, Dylan Bradshaw, Stefano Ruberto, Gunel Jahangirova, and Valerio
     Future Directions for Reliable AI. arXiv preprint arXiv:2511.00776 (2025).               Terragni. 2025. LLMLOOP: Improving LLM-Generated Code and Tests through
[11] GitHub, Inc. n.d.. GitHub. https://github.com/. Accessed: 2026-01-23.                    Automated Iterative Feedback Loops. ICSME. IEEE (2025).
[12] Roberto Gozalo-Brizuela and Eduardo C Garrido-Merchan. 2023. ChatGPT is             [35] Partha Pratim Ray. 2025. A Review on Vibe Coding: Fundamentals, State-of-the-
     not all you need. A State of the Art Review of large Generative AI models. arXiv         art, Challenges and Future Directions. Authorea Preprints (2025).
     preprint arXiv:2301.04655 (2023).                                                   [36] Rust Project. n.d.. Crate rustc_middle (nightly-rustc). https://doc.rust-lang.org/
[13] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian                 stable/nightly-rustc. Accessed: 2026-01-22.
     Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, et al. 2025. A         [37] Adrian Ryser, Florian Allwein, and Tim Schlippe. 2025. Calibrated Trust in Deal-
     survey on hallucination in large language models: Principles, taxonomy, chal-            ing with LLM Hallucinations: A Qualitative Study. arXiv preprint arXiv:2512.09088
     lenges, and open questions. ACM Transactions on Information Systems 43, 2                (2025).
     (2025), 1–55.                                                                       [38] Sandeep Singh Sengar, Affan Bin Hasan, Sanjay Kumar, and Fiona Carroll. 2025.
[14] Siming Huang, Tianhao Cheng, Jason Klein Liu, Jiaran Hao, Liuyihan Song, Yang            Generative artificial intelligence: a systematic review and applications. Multime-
     Xu, J Yang, Jiaheng Liu, Chenchen Zhang, Linzheng Chai, et al. 2024. Opencoder:          dia Tools and Applications 84, 21 (2025), 23661–23700.
     The open cookbook for top-tier code large language models. arXiv preprint           [39] Joseph Spracklen, Raveen Wijewickrama, AHM Nazmus Sakib, Anindya Maiti,
     arXiv:2411.04905 (2024).                                                                 and Bimal Viswanath. 2025. We have a package for you! a comprehensive analysis
[15] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu            of package hallucinations by code generating { LLMs } . In 34th USENIX Security
     Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical            Symposium (USENIX Security 25). 3687–3706.
     report. arXiv preprint arXiv:2409.12186 (2024).                                     [40] Stack Exchange, Inc. n.d.. Stack Overflow. https://stackoverflow.com/. Accessed:
[16] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii,           2026-01-23.
     Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in     [41] SWC Contributors. n.d.. swc-project/swc: Rust-based platform for the Web.
     natural language generation. ACM computing surveys 55, 12 (2023), 1–38.                  https://github.com/swc-project/swc. Accessed: 2026-01-22.
[17] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024. A sur-       [42] The Rust Project Developers. 2026. The Rust Programming Language. https:
     vey on large language models for code generation. arXiv preprint arXiv:2406.00515        //doc.rust-lang.org/stable/book/
     (2024).                                                                             [43] The Rust Project Developers. n.d.. The Rust Standard Library. https://doc.rust-
[18] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir               lang.org/std/. Accessed: 2026-01-22.
     Press, and Karthik Narasimhan. 2023. Swe-bench: Can language models resolve         [44] Yuchen Tian, Weixiang Yan, Qian Yang, Xuandong Zhao, Qian Chen, Wen Wang,
     real-world github issues? arXiv preprint arXiv:2310.06770 (2023).                        Ziyang Luo, Lei Ma, and Dawn Song. 2025. Codehalu: Investigating code hal-
[19] Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Car-                 lucinations in llms via execution-based verification. In Proceedings of the AAAI
     los Muñoz Ferrandis, Yacine Jernite, Margaret Mitchell, Sean Hughes, Thomas              Conference on Artificial Intelligence, Vol. 39. 25300–25308.
     Wolf, et al. 2022. The stack: 3 tb of permissively licensed source code. arXiv      [45] SMTI Tonmoy, SM Zaman, Vinija Jain, Anku Rani, Vipula Rawte, Aman Chadha,
     preprint arXiv:2211.15533 (2022).                                                        and Amitava Das. 2024. A comprehensive survey of hallucination mitigation
[20] Arjun Krishna, Erick Galinkin, Leon Derczynski, and Jeffrey Martin. 2025. Im-            techniques in large language models. arXiv preprint arXiv:2401.01313 6 (2024).
     porting Phantoms: Measuring LLM Package Hallucination Vulnerabilities. arXiv        [46] Trend Micro Research. 2025. Slopsquatting: When AI Agents Hallucinate
     preprint arXiv:2501.19012 (2025).                                                        Malicious Packages. https://www.trendmicro.com/vinfo/us/security/news/
[21] Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettle-             cybercrime-and-digital-threats/slopsquatting-when-ai-agents-hallucinate-
     moyer, Wen-tau Yih, Daniel Fried, Sida Wang, and Tao Yu. 2023. DS-1000: A                malicious-packages. Accessed: 2025-08-20.
     natural and reliable benchmark for data science code generation. In International   [47] Jiahao Yu, Xingwei Lin, Zheng Yu, and Xinyu Xing. 2024. Gptfuzzer: Red teaming
     Conference on Machine Learning. PMLR, 18319–18345.                                       large language models with auto-generated jailbreak prompts, 2024. ArXiv,
[22] VI Lcvenshtcin. 1966. Binary coors capable or ‘correcting deletions, insertions,         abs/2309.10253 (2024).
     and reversals. In Soviet physics-doklady, Vol. 10.                                  [48] Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu, Tingchen Fu, Xinting
[23] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir                   Huang, Enbo Zhao, Yu Zhang, Yulong Chen, et al. 2025. Siren’s Song in the AI
     Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rock-             Ocean: A Survey on Hallucination in Large Language Models. Computational
     täschel, et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp         Linguistics (2025), 1–46.
     tasks. Advances in neural information processing systems 33 (2020), 9459–9474.      [49] Ziyao Zhang, Chong Wang, Yanlin Wang, Ensheng Shi, Yuchi Ma, Wanjun Zhong,
[24] Fang Liu, Yang Liu, Lin Shi, Houkun Huang, Ruifeng Wang, Zhen Yang, Li Zhang,            Jiachi Chen, Mingzhi Mao, and Zibin Zheng. 2025. Llm hallucinations in practical
     Zhongqi Li, and Yuchi Ma. 2024. Exploring and evaluating hallucinations in               code generation: Phenomena, mechanism, and mitigation. Proceedings of the
     llm-powered code generation. arXiv preprint arXiv:2404.00971 (2024).                     ACM on Software Engineering 2, ISSTA (2025), 481–503.
[25] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is your       [50] Yukai Zhao, Menghan Wu, Xing Hu, and Xin Xia. 2025. HFuzzer: Testing Large
     code generated by chatgpt really correct? rigorous evaluation of large language          Language Models for Package Hallucinations via Phrase-based Fuzzing. arXiv
     models for code generation. Advances in Neural Information Processing Systems            preprint arXiv:2509.23835 (2025).
     36 (2023), 21558–21572.
[26] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-
     Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,
     et al. 2024. Starcoder 2 and the stack v2: The next generation. arXiv preprint
     arXiv:2402.19173 (2024).
[27] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
     Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al.
     2023. Self-refine: Iterative refinement with self-feedback. Advances in Neural
     Information Processing Systems 36 (2023), 46534–46594.
[28] Shradha Neupane, Grant Holmes, Elizabeth Wyss, Drew Davidson, and Lorenzo
     De Carli. 2023. Beyond typosquatting: an in-depth look at package confusion. In
     32nd USENIX Security Symposium (USENIX Security 23). 3439–3456.
[29] Gabriel Orlanski, Kefan Xiao, Xavier Garcia, Jeffrey Hui, Joshua Howland,
     Jonathan Malmaud, Jacob Austin, Rishabh Singh, and Michele Catasta. 2023.
