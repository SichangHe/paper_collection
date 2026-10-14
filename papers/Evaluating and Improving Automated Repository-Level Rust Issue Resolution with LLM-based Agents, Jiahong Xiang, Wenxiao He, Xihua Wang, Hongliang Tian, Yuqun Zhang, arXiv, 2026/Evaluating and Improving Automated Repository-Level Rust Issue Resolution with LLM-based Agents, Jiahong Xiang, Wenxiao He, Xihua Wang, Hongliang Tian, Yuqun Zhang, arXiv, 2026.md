                                              Evaluating and Improving Automated Repository-Level Rust
                                                       Issue Resolution with LLM-based Agents
                                                           Jiahong Xiang†                                              Wenxiao He                                     Xihua Wang
                                              Research Institute of Trustworthy                         Southern University of Science and                Southern University of Science and
                                               Autonomous Systems, Southern                                       Technology                                        Technology
                                             University of Science and Technology                               Shenzhen, China                                   Shenzhen, China
                                                       Shenzhen, China                                    12110818@mail.sustech.edu.cn                      12213006@mail.sustech.edu.cn
                                              xiangjh2022@mail.sustech.edu.cn

                                                                                       Hongliang Tian                                      Yuqun Zhang† *
arXiv:2602.22764v1 [cs.SE] 26 Feb 2026




                                                                                             Ant Group                            Research Institute of Trustworthy
                                                                                         Hangzhou, China                           Autonomous Systems, Southern
                                                                                      tate.thl@antgroup.com                      University of Science and Technology
                                                                                                                                           Shenzhen, China
                                                                                                                                      zhangyq@sustech.edu.cn

                                         Abstract                                                                                 CCS Concepts
                                         The Rust programming language presents a steep learning curve                            • Software and its engineering → Automatic programming;
                                         and significant coding challenges, making the automation of is-                          Software testing and debugging; • Computing methodologies
                                         sue resolution essential for its broader adoption. Recently, LLM-                        → Intelligent agents.
                                         powered code agents have shown remarkable success in resolving
                                         complex software engineering tasks, yet their application to Rust                        Keywords
                                         has been limited by the absence of a large-scale, repository-level                       Large Language Models, Automated Program Repair, Autonomous
                                         benchmark. To bridge this gap, we introduce Rust-SWE-bench, a                            Programming, Rust Benchmark
                                         benchmark comprising 500 real-world, repository-level software
                                                                                                                                  ACM Reference Format:
                                         engineering tasks from 34 diverse and popular Rust repositories. We
                                                                                                                                  Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun
                                         then perform a comprehensive study on Rust-SWE-bench with four
                                                                                                                                  Zhang† *. 2026. Evaluating and Improving Automated Repository-Level
                                         representative agents and four state-of-the-art LLMs to establish a                      Rust Issue Resolution with LLM-based Agents. In 2026 IEEE/ACM 48th
                                         foundational understanding of their capabilities and limitations in                      International Conference on Software Engineering (ICSE ’26), April 12–18,
                                         the Rust ecosystem.                                                                      2026, Rio de Janeiro, Brazil. ACM, New York, NY, USA, 13 pages. https:
                                            Our extensive study reveals that while ReAct-style agents are                         //doi.org/10.1145/3744916.3773108
                                         promising, i.e., resolving up to 21.2% of issues, they are limited
                                         by two primary challenges: comprehending repository-wide code                            1    Introduction
                                         structure and complying with Rust’s strict type and trait semantics.                     The Rust programming language has become increasingly popular
                                         We also find that issue reproduction is rather critical for task reso-                   by offering a compelling combination of performance and safety [20,
                                         lution. Inspired by these findings, we propose RustForger, a novel                       64, 77]. Through its strict type system and ownership model, it
                                         agentic approach that integrates an automated test environment                           provides compile-time guarantees against memory faults and data
                                         setup with a Rust metaprogramming-driven dynamic tracing strat-                          races [78], which has led to its wide adoption in critical domains
                                         egy to facilitate reliable issue reproduction and dynamic analysis.                      such as operating systems [43, 57, 61], cloud services [9], and web
                                         The evaluation shows that RustForger using Claude-Sonnet-3.7                             browsers [32, 49, 80]. However, its core strengths, i.e., memory
                                         significantly outperforms all baselines, resolving 28.6% of tasks                        and thread safety, also cause its steep learning curve and coding
                                         on Rust-SWE-bench, i.e., a 34.9% improvement over the strongest                          difficulty, posing significant challenges for developers, with 83% of
                                         baseline, and, in aggregate, uniquely solves 46 tasks that no other                      them finding it difficult to use [79] and 42% worrying about the long
                                         agent could solve across all adopted advanced LLMs.                                      "time to productivity" [27]. Therefore, automating the resolution
                                         * Yuqun Zhang is the corresponding author.                                               of the issues related to development in Rust is rather essential for
                                         † These authors are also affiliated with the Department of Computer Science and          unlocking Rust’s full potential and extending its adoption.
                                         Engineering, Southern University of Science and Technology, Shenzhen, China.                Recently, Large Language Models (LLMs) have demonstrated
                                                                                                                                  powers in addressing a wide range of software engineering chal-
                                                                                                                                  lenges [29, 33, 35, 45, 63, 66–69, 90]. Specifically, LLM code agents,
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.    which leverage LLMs’ coding abilities through tool adoption, com-
                                         ICSE ’26, Rio de Janeiro, Brazil                                                         mand execution, environmental feedback, and action planning,
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2025-3/2026/04                                                       have demonstrated superior performance in code-related tasks [13,
                                         https://doi.org/10.1145/3744916.3773108                                                  87, 92] and aided developers in coding efficiency [15, 70]. Their
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                            Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *


strengths are typically exemplified by their performance on pop-                To assess the capabilities of advanced LLMs and agents on this
ular benchmarks such as SWE-bench Verified [33], a version of               new benchmark, we conduct a comprehensive empirical study in-
SWE-bench crafted by OpenAI [54] for resolving real-world Python            volving four representative agentic approaches (i.e., SWE-agent [92],
issues. In this benchmark, an agent, given only an issue description        OpenHands+CodeAct v2.1 [87], Agentless [89], and AutoCodeRover
and a full repository codebase, is expected to autonomously gener-          v2.0 [63]) and four state-of-the-art LLMs (i.e., Claude-Sonnet-3.7 [11],
ate a single corrective patch to resolve the issue and pass all tests       GPT-4o [53], OpenAI o4-mini [55], and Qwen3 [10]). Specifically,
in one attempt. This task is highly demanding, requiring a suite of         these studied agents are selected for their general-purpose design,
capabilities including repository-level code understanding, targeted        i.e., having demonstrated capabilities across various programming
search, issue-reproducing test generation, and precise code edit-           languages [37, 60, 96]. The evaluation results demonstrate that the
ing. Surprisingly, the resolution rate on this benchmark has been           adoption of a ReAct-style [93] (‘thought-act-observe’ loop) archi-
improving dramatically, from a mere 1.2% achieved by approaches             tecture excels in solving tasks on Rust-SWE-bench. The associated
like RAG with SWE-Llama 13B in October 2023 [33] to a recent                agent OpenHands with Claude-Sonnet-3.7 [11] resolves a substan-
high 80.2% achieved by agents like Claude-Tools powered by the              tial 21.2% of real-world repository-level Rust issues, for which the
Claude 4 Opus model [13].                                                   manual resolution process averages 126 days and approximately 5.5
    The demand for automating Rust issue resolution and the demon-          rounds of discussion. Moreover, we find that top-performing agents
strated power of advanced LLMs and code agents altogether raise             distinguish themselves by their ability to generate large, complex
a compelling question: can agentic approaches effectively automate          patches, e.g., the leading agent OpenHands resolves significantly
the resolution of real-world Rust issues? To answer this question,          more issues than Agentless (105 vs. 57) when the required patch
it is essential for a large-scale, repository-level benchmark for           size exceeds 150 lines. We also find the compilation errors stem
real-world software engineering tasks for Rust and a comprehen-             from failures to model repository-wide code structure and to comply
sive study on how advanced LLMs and agents perform on such                  with Rust’s strict type and trait semantics. Interestingly, we observe
tasks upon the benchmark. However, existing benchmarks for                  that issue reproduction is critical for Rust issue resolution, e.g., the
Rust are deficient in two key aspects. First, while existing Rust           remaining 44.5% of tasks fail at the reproduction stage and thus
benchmarks focus on granular tasks such as C-to-Rust transpila-             could not be successfully resolved even under the top-performing
tion [14, 36, 56], function-level code synthesis [17, 50], or specific      agent-model configuration.
CVE analysis [52, 59, 91, 101], they are limited in involving general,          To mitigate the issues of repository-wide code analysis and issue
repository-level software engineering problems. Second, existing            reproduction in our study findings, we further introduce Rust-
large-scale SWE benchmarks predominantly feature Python and                 Forger, a novel agentic approach through automated test environ-
Java [33, 46, 98]. The few that incorporate Rust only offer a smaller       ment setup coupled with a cross-project dynamic tracing mecha-
corpus of tasks (e.g., 43 in SWE-bench Multilingual [37] and 239 in         nism. Specifically, RustForger first constructs an isolated testing
Multi-SWE-bench [96] compared with 500 Python issues in SWE-                workspace, managing Cargo dependencies [24] to create a reli-
bench Verified [54]). Consequently, the absence of a benchmark              able and sandboxed environment for issue reproduction. Within
that is both large-scale and dedicated to real-world Rust software          this controlled environment, the agent can invoke a novel Trace
engineering tasks prevents us from comprehensively assessing                command for cross-project dynamic analysis. This command auto-
the effectiveness of the LLMs and agents on resolving practical,            mates the entire dynamic analysis workflow by leveraging Rust’s
repository-level Rust issues.                                               metaprogramming capabilities—specifically procedural macros—to
    To bridge this gap, we introduce Rust-SWE-bench, a large-scale          automatically instrument target functions through Abstract Syn-
benchmark that contains 500 real-world, issue-resolving repository-         tax Tree (AST) modification. Such a decoupled strategy enables
level Rust tasks from 34 popular repositories. Specifically, we adopt       the agent to capture precise runtime control-flow information by
the well-established SWE-bench workflow [33] and adhere to the              executing tests from the clean workspace, thereby bypassing the
verification protocol established by the popular SWE-bench Ver-             complex build systems of the original project. Accordingly, Rust-
ified [54] to construct it. Our data collection process begins by           Forger equips the agent with the necessary runtime insights to
sourcing pull requests (PRs) from approximately 87 prominent                more effectively diagnose and resolve complex real-world Rust
open-source Rust repositories selected based on their popularity            issues. The evaluation results show RustForger solves 46 tasks
on GitHub (> 1,000 stars). We then identify candidate tasks with            that cannot be solved by any studied agent across all LLMs; its
PRs that are both merged and linked to a resolved GitHub issue              pairing with Claude-Sonnet-3.7 resolves 28.6% of tasks—a 34.9%
and that contain modifications to test files. Finally, to ensure that       improvement over the strongest baseline.
each task represents a verifiable fix, we validate whether each patch           In summary, this paper makes the following contributions:
induces a "fail-to-pass" transition (i.e., at least one test fails before
the patch and passes after the patch is applied), yielding a candidate
set of 1,040 Rust software engineering tasks. To mitigate issues
like underspecified problem descriptions [54, 89] which can lead            • Benchmark. We construct Rust-SWE-bench, the first large-scale,
to the underestimation of LLM capabilities and inefficient use of             repository-level benchmark dedicated to real-world Rust soft-
computational resources, we perform a final manual inspection of              ware engineering issues. Comprising 500 high-quality, verified
task candidates, following OpenAI’s construction principles [54].             tasks from 34 popular repositories, Rust-SWE-bench addresses
Eventually, we obtain 500 high-quality software engineering tasks             a critical gap in the field and enables systematic evaluation and
for Rust from 34 diverse GitHub repositories.                                 future research on automated Rust development.
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                    ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


• Study. We conduct a comprehensive empirical study on Rust-                                                        Requirements
  SWE-bench with four representative agents and four state-of-
  the-art LLMs. Our analysis reveals that while ReAct-style agents                                                        LLM
  show promising results, they are limited by two key challenges:
  comprehending repository-wide code structure and semantics,                                     Perception        Planning                    Action
  and successfully reproducing issues.
                                                                                                                     Memory
• RustForger. We propose RustForger, a novel agentic frame-
  work that addresses identified challenges by integrating an auto-
  mated testing workspace with a cross-project dynamic tracing                                                    Environment
  mechanism, powered by the distinctive programming features of                                   Exec Output      Codebase                     Tools
  Rust. Our evaluation shows that RustForger resolves 28.6% of
  tasks in the Rust-SWE-bench benchmark using Claude-Sonnet-
  3.7, significantly outperforming other baselines, and uniquely                             Figure 1: Basic Framework of LLM-based Agents
  resolves 46 tasks across all adopted LLMs.

2 Background & Related Work                                                          evaluated on this benchmark. In this benchmark, an agent, given
                                                                                     only an issue description and the repository codebase, is expected
2.1 Rust Programming Language                                                        to autonomously generate a single corrective patch to resolve the
Rust offers a modern solution for high-performance and secure soft-                  issue and pass all tests in one attempt. This task is highly demand-
ware that provides strong compile-time guarantees against memory                     ing, requiring a suite of capabilities including repository-level code
faults and data races without the overhead of a garbage collector.                   understanding, targeted search, issue-reproducing test generation,
This combination of safety and performance has spurred its adop-                     and precise code editing. Notably, reproducing an issue—whether
tion in critical domains, including operating systems such as Re-                    a bug, a missing feature, or an API behavior—is a critical step for
dox [62] and Tock [88], web browsers such as Servo [83], and cloud                   capturing dynamic execution information, which in turn facilitates
infrastructure like Firecracker [9]. Notably, Rust now constitutes                   more precise issue-related code localization and targeted patch gen-
21% of all new native code in the Android OS codebase [42].                          eration [41] and serves as a foundational stage in recent advanced
   While Rust’s safety guarantees are enforced by its unique type                    agents [19, 63, 87, 89, 92].
system (built on ownership, borrowing, and lifetimes), such a sys-                      To resolve the tasks mentioned above, a variety of paradigms
tem is notoriously difficult for newcomers to master, creating a                     have been proposed. ReAct [93] enables an agent to synergize rea-
steep learning curve and a significant barrier for adoption [22, 79].                soning and acting by interleaving a ‘thought-act-observe’ loop.
To address this high development overhead, researchers and de-                       For instance, SWE-agent [92] implements the ReAct loop with
velopers have proposed various approaches. RustAssistant [23]                        an Agent-Computer Interface (ACI) by equipping LLMs with high-
leverages LLMs to help developers automatically fix compilation                      level tools for file searching, editing, and navigation, instead of raw
errors. The LLM-driven Syzygy [65] aims to automate the migration                    terminal interaction. Similarly, the OpenHands agent [87], built
of legacy C codebases to Rust. Concrat [30] analyzes and replaces                    upon the ReAct-style CodeAct architecture [85], operates as a gen-
unsafe C lock APIs in concurrent programs with provably safe                         eralist platform where agents perform tasks by executing code or
Rust equivalents. Bronze [21] introduces an optional garbage col-                    conversing with humans for clarification. Another group of agents
lector to reduce the difficulty of complex memory management.                        employ more structured, multi-stage workflows. For instance, Au-
PanicKiller [52] provides the first automated tool for fixing panic                  toCodeRover v2.0 [63] utilizes a pipeline of specialized agents for
bugs in real-world Rust programs. However, despite these special-                    iterative context retrieval and specification inference to guide patch
ized solutions, a general-purpose agent capable of resolving diverse,                generation. Agentless [89] demonstrates the efficacy of a simpler,
real-world Rust issues remains an open challenge.                                    non-iterative workflow (e.g., localize, repair, and validate) that de-
                                                                                     liberately limits the LLM’s autonomy. While these agents show
2.2     Large Language Model-based Agents                                            promising results on Python-centric benchmarks like SWE-bench
LLM-based agents refer to autonomous systems that use an LLM                         Verified (e.g., OpenHands at 70.4% and Agentless at 50.8%), their
as a central controller to perceive and act upon an environment to                   effectiveness on real-world Rust issues remains underexplored.
achieve specific goals [34, 84]. These agents operate in an iterative
cycle, leveraging core components: planning for decomposing com-                      2.3     SWE-related Benchmarks
plex tasks, memory for learning from historical observations [99],                    SWE-bench [33] is a prominent benchmark for evaluating end-to-
and perception for processing environmental feedback, as shown in                     end software maintenance capabilities, comprising 2,294 real-world
Figure 1. Crucially, their action component enables them to utilize                   tasks derived from GitHub issues across 12 popular Python reposi-
external tools, allowing them to interact with and modify their                       tories. Specifically, the objective for each task is to automatically
environment in ways far beyond simple text generation [84].                           resolve the corresponding issue and submit a patch. The construc-
   Researchers have attempted to use agents to automatically re-                      tion of SWE-bench follows a three-stage pipeline to ensure task
solve real-world, repository-level software engineering tasks [26,                    quality: (1) scraping pull requests from well-maintained reposito-
33, 37, 60, 95–97]. Specifically, SWE-bench [33] has gained sig-                      ries, (2) filtering for those that resolve a specific issue and modify
nificant attention since its release, with numerous agents being                      corresponding tests, and (3) retaining only instances that pass a
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                         Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *


"fail-to-pass" execution cycle, confirming the tests’ relevance to                                       PRs from these repositories, along with the codebase state at each
the issue. In each task, an agent is provided with an issue descrip-                                     PR’s corresponding base commit.
tion and the entire repository as the codebase, and is challenged to
autonomously generate a corrective code patch. A submission is                                           3.1.2 Attribute-based filtering. We then apply an attribute-based
deemed successful only if the patch successfully applies and passes                                      filter to the scraped PRs, retaining only those that meet two criteria:
all unit and integration tests, which are hidden from the agent                                          being explicitly linked to a GitHub issue and introducing modifica-
during the resolution task. To facilitate more reliable evaluation                                       tions to the project’s test suite. Specifically, we conceptually divide
and reduce evaluation overhead [89], SWE-bench Verified provides                                         the changes within each pull request’s patch into two components:
a subset of 500 human-validated tasks with well-scoped tests and                                         a test patch, which modifies the test suite, and a fix patch, which
unambiguous issue descriptions [54].                                                                     resolves the corresponding issue.
   Recently, researchers have extended the repository-level issue-                                       3.1.3 Execution environment construction. To ensure build repro-
resolution tasks for SWE-bench in a multilingual manner. For in-                                         ducibility and mitigate dependency conflicts, we construct a snapshot-
stance, Multi-SWE-bench [96] introduces a large-scale, human-                                            based execution environment for each task by configuring Cargo [24]
annotated dataset of 1,632 tasks across seven languages, including                                       to use a crates.io index snapshot at the time of the original pull re-
Java, JavaScript, and Rust. SWE-bench Multilingual [37] offers a                                         quest. Next, we analyze and classify dependencies as either repository-
more compact set of 300 high-quality tasks across nine languages,                                        level or PR-specific to further minimize both storage overhead and
designed for rapid evaluation while maintaining full compatibility                                       the build time for each task’s Docker image and container.
with the original SWE-bench infrastructure. SWE-PolyBench [60]
focuses on languages like Java and TypeScript. These benchmarks                                          3.1.4 Execution-based filtering. Our validation process first identi-
collectively represent a significant step towards evaluating the gen-                                    fies the fail state of tests, i.e., we apply only the PR’s test patch
eralization capabilities of LLM-based agents across diverse software                                     to the base commit and execute the test suite. Next, we apply the
ecosystems. However, real-world Rust issues remain sparse in these                                       PR’s fix patch and re-execute the test suite to identify the pass
benchmarks, featuring a small corpus of tasks (43 in SWE-bench                                           state. A task is validated as a genuine fail-to-pass instance only
Multilingual and 239 in Multi-SWE-bench vs. 500 in SWE-bench                                             if it meets three conditions: (1) at least one test exhibits a clear
Verified). Hence, there is an urgent need to construct a large-scale                                     transition from fail to pass, (2) no previously passing tests (pass-
Rust real-world SWE benchmark to facilitate a rigorous and sys-                                          to-pass tests) regress, and (3) the complete patch (both test and
tematic evaluation of agent capabilities within the Rust ecosystem.                                      fix) introduces no new build failures, runtime errors, or test regres-
                                                                                                         sions. Specifically, unlike Python, to rigorously define a fail in
3        Rust-SWE-bench                                                                                  Rust’s compiled environment, we perceive compilation errors as
                                                                                                         test failures. This ensures that any non-compiling state, whether
                                                     1                                               3   after applying the test patch or the fix patch, is correctly categorized
     Repo Selection & Data Scraping                          Execution Env Construction
                                                                                                         as a failure. Accordingly, we obtain a pool of 1,040 candidate tasks.
                                                                        Repo Cargo.toml
                       GitHub Repos

            Filter by Stars      Rich PR history                                                         3.1.5 Manual verification. We perform a rigorous manual verifi-
                                                           Repo Dependencies      PR Dependencies        cation of each candidate task instance, inspired by SWE-bench
              High-quality Rust Repos
                                                                                      Docker Files       Verified [54] and Agentless [89]. We assess each task’s quality
                                                                    Cargo
                                                                    Snapshot        Env & Task Image     across three key dimensions: (1) issue quality, i.e., ensuring the
            Collecting PRs & CodeBase
                                                                                    Docker Container     problem description is sufficient and unambiguous; (2) fail-to-pass
                                                     2                                               4   integrity, i.e., confirming the fail-to-pass behavior is deterministic
           Attribute-based ltering                             Execution-based ltering                   and non-trivial; and (3) solution leakage, i.e., verifying that the
                              ✅ Resolve an issue             ✅ Pass-to-Pass      ❌ Fail-to-Pass
         Merged PRs                                            test-1   test-3         test-1
                                                                                                         issue does not contain explicit solutions. Our manual inspection
                              ✅ Test modi cation
                                                               test-2   test-4         test-2            details are provided on our GitHub page [3]. Notably, we label
                                                                                                     5
                                          Manually Veri cation                                           and classify each validated task by its primary type and challenge
                        Issue quality              Test integrity         Solution leakage               (as in Section 3.2). Eventually, our construction process yields the
    fi      fi   fi
                  fi
                                                                                                         Rust-SWE-bench dataset, which comprises 500 high-quality tasks
           Figure 2: Rust-SWE-bench Construction Process                                                 from 34 popular open-source Rust repositories, i.e., aligning with
                                                                                                         500 tasks in the established SWE-bench Verified [54] for Python,
                                                                                                         with each task representing a well-defined and realistic software
                                                                                                         engineering problem.
3.1         Benchmark Construction
Figure 2 shows a five-step construction process of Rust-SWE-bench,                                       3.2    Characteristics of Rust-SWE-bench
delineated as follows.
                                                                                                         Rust-SWE-bench provides 500 high-quality, manually reviewed
3.1.1 Repository selection and data scraping. We first select 87                                         task instances from 34 repositories, making it considerably larger
popular open-source Rust repositories that meet several criteria:                                        and more diverse than other existing Rust SWE benchmarks like
they must have over 1,000 GitHub stars, be well-maintained, feature                                      SWE-bench Multilingual [37] (43 instances from 7 repositories)
an extensive test suite, and possess a rich history of pull request (PR)                                 and Multi-SWE-bench [96] (239 instances from 10 repositories). To
discussions. Specifically, we scrape approximately 80,000 merged                                         ensure broad functional coverage, Rust-SWE-bench incorporates
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                       ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 1: Characteristics of Repositories in Rust-SWE-bench                                              1%
                                                                                                        1%
                                                                                                                                   Bug Fix
                                                                                                        5% 5%
                                                                                                                                   Feature Implementation
 Repository        #GitHub Stars                Functionality                #Instance                9%
                                                                                                                                   API Evolution
 ripgrep               53.6k               Command-line search tool                  7
                                                                                                                   52%             Error Handling Re nement
 ast-grep               9.2k             CLI for code structural search              6
 async-graphql          3.5k              GraphQL server-side library               14                                             Refactoring
                                                                                                      27%
 cargo-dist             1.7k            Application packaging for Rust              10                                             Performance Optimization
 aya                    3.7k                  eBPF library for Rust                  6                                             Others
 bevy                  40.5k               Data-driven game engine                  46
 bincode                3.1k                Binary encoder/decoder                   8
 biome                 19.9k              Web project toolchain/linter              53
 boa                    5.7k             Embeddable JavaScript engine               49   Figure 3: Distribution of Task Categories in Rust-SWE-bench
 cargo-generate         2.2k            Project template developer tool             12                   fi




 chrono                 3.6k                  Date and time library                 17
 clap                  15.3k           Command Line Argument Parser                 56
 async-trait             2k                 Async functions in traits                9   and 14.32 lines. This contrast implies Rust-SWE-bench potentially
 autocxx                2.4k              Safe C++ from Rust interop                 5
 bandwhich             10.6k            CLI network utilization display              2   better reflects real-world software engineering complexities.
 cargo-edit             3.2k              Manage cargo dependencies                 11       To characterize the nature of the tasks, we manually classified
 cbindgen               2.7k            Generates C bindings from Rust              14
 nushell               35.7k                   A new type of shell                   5   all 500 instances. Figure 3 shows their distribution where 52% of the
 rayon                 11.9k                Data parallelism library                 2   tasks are Bug Fix issues, followed by 27% Feature Implementation
 angle-grinder          3.6k             Command-line log slicing tool               3
 askama                 3.6k               Jinja-like template engine               25
                                                                                         issues, indicating that Rust-SWE-bench mainly focuses on practical
 cargo-fuzz             1.7k             Command-line fuzzer for Rust                6   software maintenance and evolution workflows. The high code
 cc-rs                  2.0k            Compile C/C++ in build scripts               8   churn detailed in Table 2 (averaging 139.9 lines edited vs. 14.3 in
 chalk                  1.9k                Rust trait system library                7
 cargo-make             2.8k              Task runner and build tool                 2   SWE-bench Verified) suggests that complex code modifications are
 serde                  9.8k              Serialization/deserialization              1   a common feature of routine maintenance in Rust. The benchmark
 bat                   53.3k            A ‘cat’ clone with highlighting             10
 fd                    38.6k           User-friendly alternative to ‘find’          12   also includes categories that are highly relevant to Rust’s ecosystem,
 cairo                  1.8k           Language for provable programs                9   e.g., API Evolution (9%) and Error Handling Refinement (5%), re-
 axum                  22.2k              Web application framework                 19
 bytes                  2.1k            Utilities for working with bytes            22
                                                                                         flecting the language’s evolving APIs and emphasis on explicit error
 tokio                 29.0k            Asynchronous runtime for Rust               17   management [44]. Note that their original manual resolution takes
 tracing                 6k                 Application-level tracing               13
 burn                  11.5k          Flexible Deep Learning Framework              14
                                                                                         on average 113 days from issue creation to PR merge and involves
                                                                                         approximately 7.2 rounds of developer discussion. We further an-
                                                                                         alyze the distribution of these resolution durations and find that
         Table 2: Overall Statistics of the Rust-SWE-bench                               14.0% of tasks are resolved within a day, 26.6% within a week, 21.6%
                                                                                         within a month, and 21.8% up to six months, while 16.0% exceed
 Component          Metric                     Mean            Median            Max     six months. This indicates that Rust-SWE-bench covers real-world
 Issue Text         Length (Tokens)             393.4             245.5          3,826   scenarios, spanning from quick fixes to long-standing issues.
                    # Files                    993.6                335         15,036
 Codebase
                    # Lines                  128,126             66,069        753,715   4 The Extensive Study
                    # Files edited                9.8                 4            148
 Fix Patch          # Hunks edited                9.9               4.5            148   4.1 Study Setup
                    # Lines edited              139.9              40.5         15,449   4.1.1 Study Subjects. We evaluate four representative SWE agents
                    # Fail to Pass               96.5                 5          1,733   including SWE-agent [92], OpenHands+CodeAct v2.1 [87], Agent-
 Tests
                    # Pass to Pass              219.6                14          1,780
                                                                                         less [89], and AutoCodeRover v2.0 [63] on our Rust-SWE-bench
                                                                                         benchmark with their details as follows.
                                                                                         • SWE-agent: SWE-agent designs an agent-computer interface
diverse project domains as shown in Table 1, including command-
                                                                                           which defines the possible actions taken by an agent to edit code,
line utilities (e.g., ripgrep [28], fd [58]), development tools (e.g.,
                                                                                           navigate the codebase, and execute tests.
cargo-edit [38], biome [16]), concurrency and parallelism libraries
                                                                                         • OpenHands+CodeAct v2.1: OpenHands utilizes the CodeAct [85]
(e.g., tokio [82], rayon [73]), web frameworks (e.g., axum [81]), and
                                                                                           architecture, enabling it to perform tasks by executing code-based
specialized engines (e.g., bevy [71], boa [72]).
                                                                                           actions.
   Table 2 presents the overall statistics of Rust-SWE-bench, high-
                                                                                         • Agentless: Agentless introduces a structured, multi-stage work-
lighting its scale and task complexity. Specifically, the Rust-SWE-
                                                                                           flow (e.g., localize, repair, and validate) that deliberately con-
bench demonstrates significant diversity in codebase size. On aver-
                                                                                           strains the LLM’s autonomy to a predefined sequence.
age, its projects contain 993.6 files and 128,126 lines of code, with
                                                                                         • AutoCodeRover v2.0: AutoCodeRover v2.0 employs an iter-
the largest repository reaching over 15,000 files and 750,000 lines.
                                                                                           ative process of context retrieval and specification inference to
This scale ensures that Rust-SWE-bench effectively represents a
                                                                                           progressively guide the generation of code patches.
wide spectrum of real-world software development scenarios. More-
over, a key characteristic of Rust-SWE-bench is the high complexity                      4.1.2 LLMs. We adopt four advanced LLMs including Claude-
of its tasks, requiring an average of 9.8 files, 9.9 hunks, and 139.9                    Sonnet-3.7 (claude-3-7-sonnet-20250219) [11], GPT-4o (gpt-4o-2024-
lines of code to resolve an issue, whereas a fix in Python-based                         11-20) [53], OpenAI o4-mini (o4-mini-2025-04-16) [55], and Qwen3
SWE-bench Verified [54] requires on average 1.25 files, 2.46 hunks,                      (qwen3-235b-a22b) [10]. We obtain the open-source model Qwen3
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                         Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *


from Hugging Face [1] and access Claude-Sonnet-3.7, GPT-4o, Ope-          • RQ2: What are the behavioral characteristics of agents resolving
nAI o4-mini through the APIs provided by Anthropic [12] and                 real-world Rust issues? For this RQ, we perform a detailed behav-
OpenAI [2]. Inference for the open-source model Qwen3 is con-               ioral analysis of the agents, which involves examining the scope
ducted on servers with 128-core 2.6GHz AMD EPYC™ ROME 7H12                  of code edits, the types of compilation errors they produce, and
CPU, 512 GiB RAM, and eight NVIDIA A100 80GB GPUs, running                  the tests they reproduce.
Ubuntu 20.04.6 LTS, utilizing vllm [40] inference framework.
                                                                          4.4    Result Analysis
4.1.3 Evaluation Metrics. Following prior works [31, 33, 48, 96],
our major evaluation metric is the Resolved Rate (%), reported            4.4.1 RQ1: performance of agents and models on Rust-SWE-bench.
as Pass@1 efficacy. An issue is considered resolved if a single           Table 3 presents the resolution rates for each agent-model con-
generated patch successfully applies to the codebase and passes all       figuration on Rust-SWE-bench. We find that agents built upon
developer-written acceptance tests. Crucially, these acceptance tests     the ReAct paradigm [93], such as OpenHands and SWE-agent,
are held out and not used by the agent during the patch generation        achieve the best performance on this benchmark. Specifically, the
process to ensure a fair evaluation. Moreover, we report the average      top-performing agent-model configuration, OpenHands paired
API inference cost ($ Avg. Cost) and token usage (# Avg. Token).          with Claude-Sonnet-3.7, resolves 106 (21.2%) tasks. When resolved
Note that to calculate the cost of the open-source LLM Qwen3, we          manually, these tasks typically require an average of 126 days from
adopt the pricing model from its official API webpage [10]. Further-      issue opening to PR merge and 5.5 rounds of discussion. Notably,
more, to specifically evaluate the issue reproduction stage adopted       this result largely outperforms not only the runner-up ReAct-based
by all our four studied agents in RQ2, we introduce an additional         agent SWE-agent (15.0% tasks), but also the runner-up LLM with
metric: Reproduction Success Rate (%), which measures the ratio           its own framework OpenAI o4-mini (6.8%). These results under-
of tasks where the agent-generated test successfully replicates the       score the decisive and compounding impact of both the ReAct-style
behavior described in the original issue.                                 agentic architecture and the choice of the underlying language
                                                                          model.
4.2      Implementations                                                   Finding 1: The adoption of a ReAct-style architecture achieves the
4.2.1 Agent Adaptation for Rust. Following the prior work [96], we         best performance on Rust-SWE-bench.
adapt the prompts of our four studied agents for the Rust language.
Moreover, agents like AutoCodeRover and Agentless include                    Moreover, we observe a significant cost disparity among the
an issue reproduction stage. However, reproducing issues in Rust          agent-model configurations. The top-performing agents, Open-
requires using shell commands to manage the environment and               Hands and SWE-agent, are also the most expensive, e.g., costing
dependencies of Cargo projects. Therefore, we develop custom shell        $3.81 and $3.48 on average when paired with Claude-Sonnet-3.7,
tools to enable this stage for these agents on Rust-SWE-bench. Fur-       respectively. This higher cost is potentially caused by their ReAct-
thermore, we adapt AutoCodeRover’s program structure-aware                based [93], iterative problem-solving frameworks, which lead to
APIs from Python to Rust, enabling the agent to gather relevant           a greater number of interaction rounds and consequently higher
code context. For other configurations, including decoding parame-        token consumption compared to the more structured, single-pass
ters (e.g., temperature and top-𝑝), we adhere to the original setups.     workflows of Agentless and AutoCodeRover.
The detailed implementations are shown in our GitHub page [3].
                                                                                            2%
4.2.2 Evaluation of the Agent’s Reproduction Stage. To assess the                          2%
                                                                                                                    Bug Fix
                                                                                          5% 3%
agents’ capabilities in reproducing issues, we extract the necessary                                                Feature Implementation
                                                                                        7%
commands and files from their issue-resolving trajectories and re-                                                  API Evolution
execute them within a sandboxed Docker container to capture the                                                     Error Handling Re nement
                                                                                                       57%          Performance Optimization
execution results. Specifically, we first run the reproduction test to                24%
                                                                                                                    Dependency Management
verify its syntactic validity [51, 86]. However, due to the complexity                                              Others
of Rust issues [18], we cannot analyze the reproduction results
directly via assertions as in prior work [51, 86]. Therefore, for tests
meeting this criterion, we then assess the reproduction results
                                                                           Figure 4: Distribution of All Resolved Tasks by Category.
                                                                                          fi




via manual analysis of the test execution output (including error
messages and exit codes) to determine if the observed behavior
corresponds to the problem described in the original issue.                  Figure 4 shows the distribution of the resolved task types by all
                                                                          studied agents which closely aligns with the overall benchmark’s
4.3      Research Questions                                               composition in Figure 3, e.g., bug fixes (57%) and feature implemen-
We investigate the following research questions to study the effec-       tations (24%) dominate the resolved tasks. This alignment demon-
tiveness of the agentic approaches and the factors that impact their      strates that the agents are effective in tackling common challenges
effectiveness on Rust-SWE-bench.                                          in the Rust ecosystem.
• RQ1: How do different agents perform on Rust-SWE-bench? For             4.4.2 RQ2: behavioral analysis of agents on Rust-SWE-bench. Ta-
  this RQ, we benchmark the selected agents-model configurations          ble 3 presents the edit scopes of patches generated by different
  on Rust-SWE-bench and report their overall effectiveness.               agents. We find that agents like SWE-agent and OpenHands
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                                     ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                                            Table 3: Evaluation Results of Different Models and Agents in Rust-SWE-bench

                                                                                                              #Edited                                Avg.                  Avg.
           Agent                                   LLM                          % Resolved
                                                                                              Line             Hunk                File             $ Cost             # Token
                                                   Claude-Sonnet-3.7            106(21.20%)   146.03            5.59               3.84               3.81             1,236,942
                                                   GPT-4o                        33 (6.60%)    66.59            3.19               2.50               1.85               729,393
           OpenHands
                                                   OpenAI o4-mini                34 (6.80%)   20.25             2.32               1.42               1.23             1,106,811
                                                   Qwen3                         25 (5.00%)    81.05            3.00               2.30               0.35               492,141
                                                   Claude-Sonnet-3.7             75(15.00%)   190.49            6.71               4.02               3.48             1,131,753
                                                   GPT-4o                         9 (1.80%)   172.84            5.28               3.45               1.92               755,343
           SWE-agent
                                                   OpenAI o4-mini                41 (8.20%)    77.13            3.81               2.32               2.13             1,708,013
                                                   Qwen3                          9 (1.80%)    83.47            2.33               1.72               0.33               417,091
                                                   Claude-Sonnet-3.7             36 (7.20%)   13.03             1.37               1.06               1.47               439,850
                                                   GPT-4o                        27 (5.40%)   16.45             1.93               1.24               0.89               331,373
           Agentless
                                                   OpenAI o4-mini                39 (7.80%)   13.10             1.43               1.06               0.61               441,949
                                                   Qwen3                         16 (3.20%)   13.41             1.30               1.07               0.35               460,175
                                                   Claude-Sonnet-3.7             46 (9.20%)   22.01             1.45               1.13               1.18               352,467
                                                   GPT-4o                        21 (4.20%)   15.01             1.53               1.24               1.09               369,833
           AutoCodeRover
                                                   OpenAI o4-mini                34 (6.80%)   17.38             1.51               1.09               0.46               343,247
                                                   Qwen3                         24 (4.80%)   12.09             1.37               1.14               0.32               359,351



cause substantially larger modifications, editing on average over                             Table 4: Statistics of Common Rust Compilation Errors En-
2 files and 70 lines of code per task, while Agentless and Au-                                countered During Agent Issue Resolution
toCodeRover typically edit 1.2 files on average and fewer than 20
lines.                                                                                           Error Code      Error Description                                          Rate (%)
                                                                                                      E0599      A method is used on a type which doesn’t implement it        18.06%
                             OpenHands      SWE-Agent         Agentless   AutoCodeRover               E0433      An undeclared crate, module, or type was used                16.21%
                       120
                                                                                                      E0432      An import was unresolved                                     12.08%
     # Task Resolved




                       90                                                                             E0425      An unresolved name was used                                   8.54%
                                                                                                      E0308      Expected type did not match the received type                 6.81%
                       60
                                                                                                      E0277      Type does not implement expected trait                        6.50%
                       30                                                                             E0412      A used type name is not in scope                              5.69%
                        0                                                                             E0753      An inner doc comment was used in an invalid context           3.07%
                                    50       100        150       200     250      300
                                                                                                                 The compiler could not infer a type and asked for a
                                         # Lines Edited per Fixed Patch                               E0282
                                                                                                                 type annotation
                                                                                                                                                                               1.75%

                                                                                                      E0609      Attempted to access a nonexistent field in a struct           1.48%
Figure 5: Cumulative Resolved Tasks by Edited Lines per                                                          An invalid number of arguments was passed when
                                                                                                      E0061                                                                    1.23%
Fixed Patch, Aggregated per Agent Across All LLMs.                                                               calling a function
                                                                                                      E0405      The code refers to a trait that is not in scope               1.21%
                                                                                                                A definition of a method not in the implemented trait
                                                                                                      E0407                                                                    1.18%
   We further analyze the capabilities of different agents on tasks                                             was given in a trait implementation
requiring varying edit scopes, with results aggregated across all
models for each agent, as shown in Figure 5. The result reveals
that all four agents perform similarly on tasks solvable with small
                                                                                              the overall distribution of common compilation errors produced
patches, e.g., OpenHands resolves 48 tasks and Agentless resolves
                                                                                              during their resolution process, detailed in Table 4. We find that
a comparable 43 within a 15-line edit scope. In contrast, a clear per-
                                                                                              the compilation errors originate from two major challenges. One
formance gap appears as the required patch size increases. Within
                                                                                              is the failure to comprehend repository-wide code organization
the 150-line scope, OpenHands resolves 105 tasks, while Agent-
                                                                                              (43.7%), leading to errors in naming, scoping, and path resolution
less resolves only 57. Such results indicate that powerful agents
                                                                                              (i.e., E0433, E0432, E0425, E0412, and E0405). This suggests that
like OpenHands and SWE-agent tend to explore a wider solution
                                                                                              agents struggle to correctly model the project’s structural con-
space by making more extensive changes.
                                                                                              text for linking different code modules, which is a prominent chal-
 Finding 2: While all agents are similarly effective on tasks requiring                       lenge during the issue reproduction stage. For instance, in the case
 small patches, top-performing agents are more powerful to generate                           of bevyengine-10627 [4] shown in Figure 6, OpenHands with
 large, complex patches for more challenging tasks.                                           Claude-Sonnet-3.7 attempts to construct a reproduction test to repli-
                                                                                              cate a panic [39] where cloning a reflected trait object (Box<dyn
   We find agents frequently encounter compilation errors when                                Reflect>) via the clone_value() method erases its type informa-
resolving real-world Rust issues, e.g., OpenHands encounters an                               tion, causing a subsequent call to insert_reflect to fail. However,
average of three compilation errors per task. We then examine                                 compilation errors arise from unresolved imports and undeclared
     ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                    Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *


     types, causing a failure to incorporate the necessary bevy crate                                   that this causes a 42% drop in its resolution rate, indicating that
     preludes [71] and dependencies into the test’s scope.                                              issue reproduction is a prominent bottleneck for Rust issue resolu-
                                                                                                        tion. To better understand these reproduction failures, we manually
                                                                               Reproduce Issue          inspect the failed instances and find that most cases stem from de-
                                        bevyengine-10627
                                                                          reflect_clone_issue.rs        pendency issues (52.5%; misconfigured Cargo.toml or workspace
                      insert_re ect panics when                           use bevy_app::prelude::*;     paths), followed by irrelevant tests (35.5%; tests that do not exercise
                                                                          use bevy_ecs::prelude::*;
                        inserting component                  OpenHands    use bevy_reflect::{…};
                                                                          use bevy_utils::default;
                                                                                                        the reported behavior) and non-compiling tests (12.0%; generated
                                                                          …             error[E0432]    tests that fail to build).
                                             Codebase
                                                             Read Src                   error[E0433]
                                                                                                         Finding 4: Issue reproduction is critical for Rust issue resolution.
               Figure 6: Compilation Error in bevyengine-10627 Task
                                                                                                        5     Approach
        Another major challenge for compilation errors (32.6%) arises                                   Inspired by Finding 4, we introduce RustForger, a novel agentic
     from Rust’s complex type and trait system. While agents often                                      approach to enhance Rust issue resolution through automated test
     generate syntactically plausible code, they fail to satisfy the strict                             environment setup coupled with a unique dynamic tracing strategy.
     semantic contracts of Rust (i.e., E0599, E0308, E0277, and E0407).
fl
     For example, in the case of askama-374 [5], SWE-agent’s syn-                                       5.1     RustForger Framework
     tactically valid attempt to call a method on an object consistently
                                                                                                        Figure 8 illustrates the framework of RustForger comprising two
     triggered an E0599 compilation error because the object’s type
                                                                                                        stages. In the first stage Setup Testing Workspace, the agent’s pri-
     failed to satisfy the necessary trait bounds, indicating the agent’s
                                                                                                        mary objective is to create a reliable, isolated environment for
     difficulty to comply with Rust’s strict semantics.
                                                                                                        issue reproduction. It begins by parsing the input issue description
      Finding 3: Agent-generated compilation errors primarily stem from                                 and performing an initial exploration of the target codebase to un-
      two key deficiencies: a failure to model repository-wide code struc-                              derstand its module structure and dependencies, adhering to the
      ture and an inability to comply with Rust’s strict type and trait                                 established practices of ReAct-style agents [87, 92]. Subsequently,
      semantics.                                                                                        the agent automatically executes three key steps: (1) it analyzes the
                                                                                                        project’s Cargo.toml to identify its structure and dependencies;
                                                                                                        (2) it initializes a new, clean Cargo project in a separate workspace;
       Reproduction Success Rate (%)




                                       0.6                                                              and (3) it imports the original, target project as a local path de-
                                                                          Claude-Sonnet-3.7    GPT-4o
                                                                          OpenAI o4-mini       Qwen-3   pendency into this new workspace. This ensures that any test will
                                  0.45
                                                                                                        run against the exact code under investigation. Finally, within this
                                                                                                        isolated workspace, the agent generates a test case to specifically
                                       0.3
                                                                                                        trigger and reproduce the failure described in the issue.
                                  0.15
                                                                                                           Once the issue is successfully reproduced, the agent launches the
                                                                                                        second stage, Code Analysis & Patch Generation, where it leverages
                                        0                                                               the controlled environment for dynamic analysis. After using the
                                               OpenHands   SWE-Agent     Agentless    AutoCodeRover     test outputs to locate potential issue-related code regions, it acti-
                                                                                                        vates its core cross-project dynamic tracing capability via the Trace
     Figure 7: Reproduction Success Rate by Agents and Models                                           command, a unified agent-computer interface that encapsulates
                                                                                                        the entire analysis workflow into a single, all-in-one function. This
        Motivated by Finding 3, we find that these compilation errors                                   process is highly automated, powered by Rust metaprogramming
     largely occur in the issue reproduction stage, e.g., 35% of them occur                             features [74–76]: RustForger first injects the necessary tracing
     during the reproduction stage for the top-performing OpenHands-                                    dependencies into the test environment. It then instruments tar-
     Claude-Sonnet-3.7 configuration, indicating that it is challenging                                 geted functions within the original codebase by injecting tracing
     for agents to reproduce issues. Figure 7 presents our evaluation                                   macros via Abstract Syntax Tree (AST) modification. Critically,
     of the issue reproduction stage, which involves re-executing tasks                                 the test execution and data collection are launched from the test-
     from Rust-SWE-bench and analyzing their outputs. OpenHands                                         ing workspace, as indicated by the dotted arrow in Figure 8. This
     paired with Claude-Sonnet-3.7 achieves the highest reproduction                                    decoupled strategy allows the agent to capture precise, runtime
     success rate at 55.5%, i.e., the remaining 44.5% of tasks fail at the                              control-flow information without being entangled in the original
     reproduction stage, i.e., a critical prerequisite for validating patches                           project’s complex build system or test suite. The collected trace
     and obtaining runtime information, and thus could not be success-                                  data provides the potential path to the issue’s origin, enabling the
     fully resolved even under the top-performing agent-model configu-                                  agent to propose a code modification. This patch is then iteratively
     ration. Specifically, we find that for each successfully reproduced                                verified against the reproduction test until the issue is resolved and
     issue, OpenHands with Claude-Sonnet-3.7 re-runs the reproduc-                                      the agent outputs the final patch. Notably, RustForger’s design is
     tion test on average 4.7 times for patch validation and dynamic                                    hybrid: it prioritizes the dynamic analysis powered by the Trace
     information gathering. Moreover, we also disable the reproduc-                                     command for reproducible issues, while utilizing the static analysis
     tion stage in OpenHands paired with Claude-Sonnet-3.7 and find                                     for all other cases, i.e., the agent bypasses dynamic analysis and
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                              ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil



                      Setup Testing Workspace                                                           Code Analysis & Patch Generation

                         Analyze Project Structure
                                                                                                                    Trace Command
       Explore                                                                                                                                              Modi cation &
                                                          Create                                          Setup Tracing          Macro Injection             Veri cation
      Codebase                                                                          Locate
                         Create Cargo Project                                                             Dependencies           based on AST
                                                      Reproduce Test                Related Code
  Issue Description      Import Dependency                                                               Execute & Collect
                                                                       Executed in Testing Workspace                             Auto Clean Up
                                                                                                           Tracing Data                                         Patch


                                                        Figure 8: The RustForger Framework


proceeds directly to the Code Analysis & Patch Generation stage, re-                                    Table 5: Evaluation Result of RustForger
lying solely on static analysis to locate and modify the code without
using the Trace command.                                                                      Agent             Claude-Sonnet-3.7 GPT-4o OpenAI o4-mini Qwen3
                                                                                              OpenHands             106(21.2%)       33(6.60%)     34(6.80%)       25(5.00%)
5.2     Trace Command                                                                         SWE-agent              75(15.0%)       9(1.80%)      41(8.20%)        9(1.80%)
                                                                                              Agentless               36(7.2%)       27(5.40%)     39(7.80%)       16(3.20%)
In this section, we introduce the Trace command for root cause                                AutoCodeRover          46(9.20%)       21(4.20%)     34(6.80%)       24(4.80%)
analysis in complex Rust projects. It provides a programmatic in-                             RustForger            143(28.6%)       42(8.4%)      82(16.4%)       33(6.60%)
terface to a cross-project tracing workflow, which automates code
instrumentation, test execution, and runtime data collection. Specif-
ically, the complete workflow of the Trace command integrates                                setup, AST-based macro injection, test execution, data collection,
three key components: a selective AST-based instrumentor, a robust                           and final cleanup (Figure 8), enabling the agent to focus on high-
tracing runtime with intelligent data serialization, and a unified                           level resolution strategies instead of implementation details.
agent-computer interface for seamless agent integration.
   Selective AST-based Instrumentation. To capture execution flow                            5.3       Evaluation
and ensure syntactic integrity, RustForger’s Trace command em-                               5.3.1 Evaluation Metrics and Baselines. To evaluate the perfor-
ploys a selective instrumentor that directly modifies the source                             mance of RustForger, we adopt metrics used in our extensive
code’s Abstract Syntax Tree (AST). It injects tracing macros at                              study (Section 4.1.3): Resolve Rate (%), $ Avg. Cost, and Reproduc-
specified target functions. Specifically, the process is decoupled                           tion Success Rate (%). Due to budget constraints, we follow the
from the build system, enabling instrumentation of the original                              SWE-agent setup [92] to set the budget per task to $4. We adopt
project code while running tests in a separate, isolated workspace.                          the same four studied agents and LLMs in our previous study as
To ensure robustness and manage complexity, our current imple-                               our baselines.
mentation of the Trace command focuses on instrumenting regular
functions, while automatically excluding more complex structures                             5.3.2 Implementation. RustForger is implemented as a ReAct-
like closures, other procedural macros, and test functions to prevent                        style agent [93] and follows the setup of baseline agents [63, 87, 92],
potential tracing conflicts and irrelevant overhead.                                         with its temperature set to 0 to ensure the model’s output is more
                                                                                             deterministic. Notably, our Trace’s instrumentation mechanism
   Robust Tracing Runtime. Our tracing runtime reconstructs the                              is designed as a purely observational wrapper to strictly preserve
dynamic call graph by capturing function input and output. How-                              original program semantics. To ensure identical trait resolution,
ever, this task is challenging due to Rust’s type system, in which the                       the injected macros retain original function signatures, including
non-serializability [25] of many types would otherwise cause com-                            all generics and where clauses. Furthermore, we adhere to Rust’s
pilation failures. To handle this, we adopt a hybrid tracing strategy                        borrow checker by exclusively utilizing temporary, strictly-scoped
that captures serializable types as JSON while recording descriptive                         immutable references to capture parameter values. This ensures
placeholders for others, thereby preserving crucial type information                         that variable lifetimes and drop timings remain unaffected, with all
without compromising build integrity. The resulting trace, encom-                            macro-generated variables isolated within private internal scopes.
passing the call hierarchy and captured data, is structured into a                           Specifically, Trace’s overhead is minimal: tokens generated for
single JSON object to facilitate programmatic analysis.                                      tracing account for only 1.65% of total usage, the shared isolated
                                                                                             workspace’s initial build takes about 40 seconds, and each Trace
   Unified Agent-Computer Interface. The Trace command encap-                                invocation adds only ∼12 seconds of incremental compilation. Due
sulates our entire tracing workflow into a unified agent-computer                            to page limits, implementation details like RustForger’s prompt,
interface, inspired by SWE-agent [92]. The agent invokes it with                             basic functions (e.g., string replacer) and Trace are shown in our
parameters defining the target instrumentation functions, execution                          GitHub page [3].
command, the testing workspace path, and the target codebase path.
To guarantee a non-destructive operation, the Trace command au-                              5.3.3 Result Analysis. Table 5 presents the evaluation results where
tomatically backs up the project state before instrumentation and                            RustForger, when paired with Claude-Sonnet-3.7, achieves the
restores it upon completion, usually within a second. This interface                         best performance on Rust-SWE-bench by successfully resolving 143
abstracts the underlying complexity, i.e., automating dependency                             out of 500 tasks (28.6%), outperforming the best-performing agent in
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                              Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *




                                                                                     Reproduction Success Rate (%)
                                                                                                                       0.7
our study OpenHands with Claude-Sonnet-3.7 by 34.9%. Notably,                                                                                                 Claude-Sonnet-3.7    GPT-4o
                                                                                                                                                              OpenAI o4-mini       Qwen-3
the Trace command is successfully leveraged in the resolution
                                                                                                                     0.525
process for 71.3% of these tasks. Moreover, we validate the statisti-
cal significance of this result using McNemar’s test [47], a widely                                                   0.35
adopted statistical method for comparing paired binary outcomes
in software engineering research. The test yields a 𝑝-value < 0.001                                                  0.175
when comparing RustForger with the runner-up OpenHands, in-
dicating that the performance gain is statistically significant. Rust-                                                  0
Forger also consistently outperforms each baseline agent across                                                              RustForger   OpenHands   SWE-Agent   Agentless AutoCodeRover
all four tested LLMs. This consistent superiority underscores the
robustness and general effectiveness of our proposed framework                                                       Figure 10: Comparison of Reproduction Success Rate
in tackling real-world Rust issues. Notably, RustForger with the
cost-effective OpenAI o4-mini achieves a 16.4% resolution rate (82
tasks), surpassing not only all baselines using the same model but                                                                           Trace Command
also the highly-regarded SWE-agent paired with the much more                                                         test_project:/workspace/test_workspace
                                                                                                                     target_project:/workspace/clap-rs
powerful Claude-Sonnet-3.7 (15.0%). Such a result indicates that by                                                  instrument:/workspace/test_workspace/src/main.rs:main
                                                                                                                     instrument:/workspace/clap-rs/src/output/usage.rs:\
effectively addressing the core challenges of issue reproduction and                                                             create_smart_usage,get_required_usage_from
runtime analysis, our approach enables even less powerful mod-                                                       output:/workspace/trace.json
                                                                                                                     exec:cd /workspace/test_workspace && cargo run
els to achieve highly competitive results on complex real-world
repository-level Rust tasks. At last, across all LLMs, RustForger
uniquely resolves 46 tasks that no baselines could.
                                                                                                                                                 Output
                                                                                                                     Thread ThreadId(1) (3 calls)
                    Claude-Sonnet-3.7       GPT-4o     OpenAI o4-mini   Qwen-3
                                                                                                                        ├─get_required_usage_from (usage.rs:316) [22:35:29]
                                                                                                                        ├─ in: {incl_last, incls, matcher}
OpenHands                                                                                                               ├─ out: […]
                                                                                                                        ├─get_required_usage_from (usage.rs:316) [22:35:29]
 SWE-Agent                                                                                                              ├─ in: {incl_last, incls, matcher}
                                                                                                                        ├─ out: [“—config <foo>”, “<input>”]
                                                                                                                        └─create_smart_usage (usage.rs:151) [22:35:29]
 RustForger                                                                                                             └─ in: {used}
                                                                                                                        └─ out: “test_workspace --config <foo> <input>"
               0                1                 2              3               4                                      └─ └─ get_required_usage_from (usage.rs:316)
                                            Avg. Cost ($)


         Figure 9: Comparison of Average Cost per Task                                           Figure 11: The Trace Command Used in clap-rs-2609 [6]


    In addition to its superior resolution rates, RustForger also                       Case Study. To illustrate RustForger’s practical advantages,
demonstrates significant advantages in cost efficiency. As shown in                  we analyze its unique resolution of issue clap-rs-2609 [6], a
Figure 9, RustForger consistently incurs lower average API costs                     task where all baseline agents fail. The issue involves the pop-
than the top-performing baselines, OpenHands and SWE-agent,                          ular clap library generating an incorrect usage string for argu-
across all LLMs. For instance, when paired with the most powerful                    ments with default values. RustForger first executes its automated
model Claude-Sonnet-3.7, RustForger’s average cost is $3.0, which                    setup strategy, creating an isolated testing workspace and link-
is 21.3% and 13.8% lower compared to OpenHands ($3.81) and SWE-                      ing the original project as a local dependency, while other agents
agent ($3.48), respectively. This gain is even more significant with                 consistently fail to reproduce the issue due to the complex build
more economical models–with OpenAI o4-mini, RustForger’s cost                        configurations. Subsequently, the agent invokes the Trace com-
($0.6) is less than half that of OpenHands ($1.23) and amounts to                    mand to perform cross-project dynamic analysis on the functions
only 28.2% of the cost of SWE-agent ($2.13).                                         responsible for usage generation as in Figure 11. Specifically, Trace
    Moreover, we examine how task complexity, approximated by                        automates the entire workflow by: (1) setting up dependencies
the original manual resolution duration, correlates with agent per-                  for both the test_workspace and the target codebase clap-rs;
formance. Our analysis shows that RustForger’s success rate is                       (2) instrumenting key functions, i.e., main in the test workspace,
42.9% on issues resolved within a day, 32.3% within a week, 31.5%                    and get_required_usage_from and create_smart_usage in the
within a month, 22.0% within six months, and 15.0% for issues open                   clap-rs source code, with a tracing macro; (3) executing the test
longer than six months, highlighting both RustForger’s strong                        via cargo run and collecting the resulting trace information; and
performance and the particular difficulty of long-standing issues.                   finally, (4) cleaning up all modifications. Interestingly, the trace
    Figure 10 shows that RustForger consistently outperforms all                     data precisely expose the root cause: a faulty interaction where
baselines in terms of reproduction success rate across all LLMs,                     one function get_required_usage_from passes an incorrect list
achieving a 67.3% rate with Claude-Sonnet-3.7 (vs. 55.5% for Open-                   of required arguments to create_smart_usage. This deep runtime
Hands) and a 45.4% rate with OpenAI o4-mini (vs. 32.6% for Open-                     insight enables the agent to correctly deduce a two-part patch
Hands).                                                                              modifying both functions. Finally, the agent iteratively validates
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                   ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                  Table 6: Ablation Study Results                                       To mitigate the inherent stochasticity of LLM-based agents, we
                                                                                     perform our evaluation across 500 diverse instances in Rust-SWE-
Configuration         Claude-Sonnet-3.7 GPT-4o OpenAI o4-mini Qwen3 Avg.             bench, ensuring the stability and generalizability of our findings.
RustForger𝑏𝑎𝑠𝑒               42           12           26           8    22.0        We set the temperature to 0 to mitigate the threat of randomness
RustForger𝑟𝑒𝑝𝑟𝑜𝑑𝑢𝑐𝑒          47           14           29          10    25.0        to the RustForger evaluation results. Potential bias in our manual
RustForger                   59           16           35          11    30.3
                                                                                     validation is mitigated through a strict protocol where three authors
                                                                                     independently verify each result before reaching a consensus.
                                                                                     Threats to external validity. The primary threat to external valid-
its solution within the isolated workspace, leveraging the rapid                     ity lies in the generalizability of our findings, which is closely tied
feedback loop to efficiently converge on the correct solution.                       to our evaluation dataset and the selection of compared agents. Cor-
                                                                                     respondingly, we construct Rust-SWE-bench with 500 real-world,
5.4     Ablation Study                                                               issue-resolving tasks sourced from 34 diverse and popular open-
                                                                                     source Rust repositories. Each task is grounded in an actual merged
We further perform an ablation study on 200 randomly selected                        pull request, ensuring the problems are authentic and representative
Rust-SWE-bench tasks, comparing the full RustForger against two                      of genuine software engineering challenges. Meanwhile, we select
variants: RustForger𝑟𝑒𝑝𝑟𝑜𝑑𝑢𝑐𝑒 , which disables the Trace command,                    four recent and representative agents that demonstrate state-of-the-
and RustForger𝑏𝑎𝑠𝑒 , which skips the isolated testing workspace                      art performance on the widely-recognized SWE-bench benchmark,
entirely and directly performs the reproduction in the target code-                  ensuring our analysis reflects the latest landscape of code agents.
base.                                                                                Threats to construct validity. A potential threat to construct
   Table 6 presents the results of our ablation study. First, compar-                validity lies in whether our evaluation metrics accurately capture
ing RustForger𝑏𝑎𝑠𝑒 with RustForger𝑟𝑒𝑝𝑟𝑜𝑑𝑢𝑐𝑒 , the introduction of                    the multifaceted nature of the issue resolution task. To mitigate this,
the isolated testing workspace alone improves the task resolution                    we adopt the Resolved Rate (Pass@1), a widely-accepted metric for
performance by resolving 3.0 more tasks on average. Furthermore,                     evaluating task completion in code generation benchmarks [31, 33,
the performance leap from RustForger𝑟𝑒𝑝𝑟𝑜𝑑𝑢𝑐𝑒 to the full Rust-                      48, 96]. To provide deeper diagnostic insights, we also measure the
Forger underscores the value of the cross-project dynamic tracing                    Reproduction Success Rate (%) [94, 100] to assess an agent’s ability
analysis where the Trace command enables the agent to resolve                        to replicate the original issues.
an additional 5.3 tasks on average. Such results reflect the effective-
ness of the issue reproduction and the dynamic tracing analysis of                    7    Conclusion
RustForger respectively.
                                                                                      In this paper, we introduce Rust-SWE-bench, the large-scale, repository-
   To better understand where Trace helps, we also examine two
                                                                                      level benchmark for real-world Rust software engineering issues,
representative issues. In bevyengine/bevy-16747 [7], RustForger
                                                                                      comprising 500 issue-resolving tasks from diverse and popular
must extend the animated_field! macro to support tuple structs
                                                                                      repositories. Our comprehensive study on Rust-SWE-bench reveals
(e.g., TextColor::0) while preserving the behavior for named fields.
                                                                                      that the performance of current LLM-based agents is primarily
By invoking Trace on the underlying implementation methods, the
                                                                                      hindered by challenges in repository-wide code comprehension
agent verifies at runtime that calls for named fields still go through
                                                                                      and issue reproduction. To address these limitations, we design
new_unchecked, whereas tuple indices are correctly dispatched to
                                                                                      RustForger, a novel agentic framework integrating an automated
new_tuple_unchecked, allowing it to validate the updated macro’s
                                                                                      testing workspace with a unique cross-project dynamic tracing
semantics beyond static inspection. In tokio-rs/tracing-1017 [8],
                                                                                      capability. Our evaluation demonstrates that RustForger achieves
RustForger uses Trace to validate a performance optimization
                                                                                      the best performance, resolving 28.6% of the tasks using Claude-
that skips Thread-Local Storage checks when no scoped dispatcher
                                                                                      Sonnet-3.7, i.e., a 34.9% improvement over the strongest baseline,
is active. By tracing set_global_default and with_default in
                                                                                      and uniquely resolving 46 issues across all adopted LLMs.
the reproduction test, it observes that the global dispatcher is initial-
ized before scoped guards, providing runtime evidence that the con-
ditional bypass does not compromise correctness or thread-safety.
                                                                                      Data Availability
These cases concretely illustrate how dynamic tracing contributes                    All study results, evaluation details, and source code of the Rust-
to the gains observed in the ablation study.                                         SWE-bench and RustForger are presented in the GitHub page [3].

6     Threats to Validity                                                             Acknowledgments
                                                                                     This work is partially supported by the National Natural Science
Threats to internal validity. We take several measures to ensure
                                                                                     Foundation of China (Grant No. 62372220). It is also partially sup-
the internal validity of our study. To guarantee reproducibility and
                                                                                     ported by Ant Group Research Fund.
mitigate system-level variations, we conduct each experimental
run in a dedicated Docker container that encapsulates the exact
repository state, toolchain, and dependencies. Furthermore, our
Trace command implements a meticulous cleanup mechanism to
remove all instrumentation artifacts after its execution, regardless
of the outcome, ensuring our analysis introduces no residual side
effects to the target codebase.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                          Jiahong Xiang† , Wenxiao He, Xihua Wang, Hongliang Tian, and Yuqun Zhang† *


References                                                                                 [29] Zuchen Gao, Zizheng Zhan, Xianming Li, Erxin Yu, Haotian Zhang, Bin Chen,
  [1] 2024-02-29. Hugging Face. https://huggingface.co.                                         Yuqun Zhang, and Jing Li. 2025. OASIS: Order-Augmented Strategy for Improved
  [2] 2024-02-29. OpenAI API. https://openai.com/api.                                           Code Search. arXiv preprint arXiv:2503.08161 (2025).
  [3] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench.                   [30] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An automatic C-to-Rust lock
  [4] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench/blob/                   API translator for concurrent programs. In 2023 IEEE/ACM 45th International
      main/material/MopenHands_claude_evyengine__bevy-10627.traj.                               Conference on Software Engineering (ICSE). IEEE, 716–728.
  [5] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench/blob/              [31] Xing Hu, Feifei Niu, Junkai Chen, Xin Zhou, Junwei Zhang, Junda He, Xin Xia,
      main/material/MSWE-agent_o4mini_rinja-rs__askama-374.traj.                                and David Lo. 2025. Assessing and Advancing Benchmarks for Evaluating Large
  [6] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench/blob/                   Language Models in Software Engineering Tasks. arXiv:2505.08903 [cs.SE]
      main/material/RustAgent_clap-rs__clap-2609.traj.                                          https://arxiv.org/abs/2505.08903
  [7] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench/blob/              [32] Dana Jansens. 2023.          Supporting the use of Rust in the Chromium
      main/material/rustforger_log_bevyengine__bevy-16747.traj.log.                             project. https://security.googleblog.com/2023/01/supporting-use-of-rust-in-
  [8] 2025. GitHub Repository. https://github.com/GhabiX/Rust-SWE-Bench/blob/                   chromium.html Google Security Blog.
      main/material/rustforger_log_tokio-rs__tracing-1017.traj.log.                        [33] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir
  [9] Alexandru Agache, Marc Brooker, Alexandra Iordache, Anthony Liguori, Rolf                 Press, and Karthik Narasimhan. 2023. Swe-bench: Can language models resolve
      Neugebauer, Phil Piwonka, and Diana-Maria Popa. 2020. Firecracker: Light-                 real-world github issues? arXiv preprint arXiv:2310.06770 (2023).
      weight virtualization for serverless applications. In 17th USENIX symposium on       [34] Haolin Jin, Linghan Huang, Haipeng Cai, Jun Yan, Bo Li, and Huaming Chen.
      networked systems design and implementation (NSDI 20). 419–434.                           2025. From LLMs to LLM-based Agents for Software Engineering: A Survey of
 [10] Alibaba Cloud. 2025. Qwen3 API Price. Online. https://www.alibabacloud.com/               Current, Challenges and Future. arXiv:2408.02479 [cs.SE] https://arxiv.org/abs/
      help/zh/model-studio/models#c5414da58bjgj Accessed: 2025-07-12.                           2408.02479
 [11] Anthropic. 2024. Introducing Claude 3.7 Sonnet. Online. https://www.anthropic.       [35] Sungmin Kang, Juyeon Yoon, and Shin Yoo. 2023. Large language models are few-
      com/news/claude-3-7-sonnet Accessed: 2025-07-15.                                          shot testers: Exploring llm-based general bug reproduction. In 2023 IEEE/ACM
 [12] Anthropic. 2025. Claude API Documentation. https://docs.anthropic.com/en/                 45th International Conference on Software Engineering (ICSE). IEEE, 2312–2323.
      home. Accessed: 2025-06-30.                                                          [36] Mohammad Abdullah Matin Khan, M Saiful Bari, Xuan Long Do, Weishi Wang,
 [13] Anthropic. 2025. Introducing the next generation of Claude. https://www.                  Md Rizwan Parvez, and Shafiq Joty. 2023. xcodeeval: A large scale multilin-
      anthropic.com/news/claude-3-family. Accessed: 2025-06-23.                                 gual multitask benchmark for code understanding, generation, translation and
 [14] Ben Athiwaratkun, Sanjay Krishna Gouda, Zijian Wang, Xiaopeng Li, Yuchen                  retrieval. arXiv preprint arXiv:2303.03004 (2023).
      Tian, Ming Tan, Wasi Uddin Ahmad, Shiqi Wang, Qing Sun, Mingyue Shang,               [37] Kabir Khandpur, Kilian Lieret, Carlos E. Jimenez, Ofir Press, and John Yang.
      et al. 2022. Multi-lingual evaluation of code generation models. arXiv preprint           2025. Multi-SWE-bench: 300 curated SWE-bench style tasks from 42 reposi-
      arXiv:2210.14868 (2022).                                                                  tories representing 9 programming languages. https://www.swebench.com/
 [15] Shraddha Barke, Michael B James, and Nadia Polikarpova. 2023. Grounded                    multilingual.html. Accessed: 2025-06-28.
      copilot: How programmers interact with code-generating models. Proceedings           [38] killercup. 2024. cargo-edit: A utility for managing Cargo.toml dependencies
      of the ACM on Programming Languages 7, OOPSLA1 (2023), 85–111.                            from the command line. https://github.com/killercup/cargo-edit.
 [16] BiomeJS. 2024. Biome: A toolchain for web projects, aimed to provide formatter,      [39] Steve Klabnik and Carol Nichols with contributions from the Rust Community.
      linter, and more. https://github.com/biomejs/biome.                                       2024. The Rust Programming Language (2024 ed.). The Rust Project Developers.
 [17] Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-                 https://doc.rust-lang.org/stable/book/ Accessed: 2025-07-17.
      Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson,            [40] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,
      Molly Q Feldman, et al. 2023. MultiPL-E: a scalable and polyglot approach to              Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
      benchmarking neural code generation. IEEE Transactions on Software Engineer-              Memory Management for Large Language Model Serving with PagedAtten-
      ing 49, 7 (2023), 3675–3691.                                                              tion. In Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems
 [18] Oscar Chaparro, Carlos Bernal-Cárdenas, Jing Lu, Kevin Moran, Andrian Marcus,             Principles.
      Massimiliano Di Penta, Denys Poshyvanyk, and Vincent Ng. 2019. Assessing the         [41] Tien-Duy B Le, Richard J Oentaryo, and David Lo. 2015. Information retrieval
      quality of the steps to reproduce in bug reports. In Proceedings of the 2019 27th         and spectrum based bug localization: Better together. In Proceedings of the 2015
      ACM Joint Meeting on European Software Engineering Conference and Symposium               10th Joint Meeting on Foundations of Software Engineering. 579–590.
      on the Foundations of Software Engineering (Tallinn, Estonia) (ESEC/FSE 2019).       [42] Abner Li. 2022. Google reports decline in Android memory safety vulnerabilities as
      Association for Computing Machinery, New York, NY, USA, 86–96. https:                     Rust usage grows. https://9to5google.com/2022/12/01/android-memory-safety-
      //doi.org/10.1145/3338906.3338947                                                         rust/
 [19] Dong Chen, Shaoxin Lin, Muhan Zeng, Daoguang Zan, Jian-Gang Wang, Anton              [43] Hongyu Li, Liwei Guo, Yexuan Yang, Shangguang Wang, and Mengwei Xu.
      Cheshkov, Jun Sun, Hao Yu, Guoliang Dong, Artem Aliev, Jie Wang, Xiao Cheng,              2024. An Empirical Study of { Rust-for-Linux } : The Success, Dissatisfaction,
      Guangtai Liang, Yuchi Ma, Pan Bian, Tao Xie, and Qianxiang Wang. 2024. CodeR:             and Compromise. In 2024 USENIX Annual Technical Conference (USENIX ATC
      Issue Resolving with Multi-Agent and Task Graphs. arXiv:arXiv:2406.01304                  24). 425–443.
 [20] Y. W. Chua. 2017. Appreciating Rust’s Memory Safety Guarantees. https://             [44] Linxi Liang, Jing Gong, Mingwei Liu, Chong Wang, Guangsheng Ou, Yanlin
      medium.com/singapore-gds/appreciating-rust-memory-safety-438301fee097                     Wang, Xin Peng, and Zibin Zheng. 2025. RustEvo2̂: An Evolving Benchmark
 [21] Michael Coblenz, Michelle L Mazurek, and Michael Hicks. 2022. Garbage col-                for API Evolution in LLM-based Rust Code Generation. arXiv:arXiv:2503.16922
      lection makes rust easier to use: A randomized controlled trial of the bronze        [45] Qingyuan Liang, Zhao Zhang, Zeyu Sun, Zheng Lin, Qi Luo, Xiao Yueyi, Yizhou
      garbage collector. In Proceedings of the 44th International Conference on Software        Chen, Yuqun Zhang, Haotian Zhang, Lu Zhang, et al. 2025. Grammar-based code
      Engineering. 1021–1032.                                                                   representation: Is it a worthy pursuit for llms?. In Findings of the Association for
 [22] Filipe Roseiro Cogo, Xin Xia, and Ahmed E. Hassan. 2023. Assessing the Align-             Computational Linguistics: ACL 2025. 15640–15653.
      ment between the Information Needs of Developers and the Documentation of            [46] Tianyang Liu, Canwen Xu, and Julian McAuley. 2023. Repobench: Benchmarking
      Programming Languages: A Case Study on Rust. 32, 2, Article 43 (April 2023),              repository-level code auto-completion systems. arXiv preprint arXiv:2306.03091
      48 pages. https://doi.org/10.1145/3546945                                                 (2023).
 [23] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi. 2023.           [47] Quinn McNemar. 1947. Note on the sampling error of the difference between
      Fixing rust compilation errors using llms. arXiv preprint arXiv:2308.05177 (2023).        correlated proportions or percentages. Psychometrika 12, 2 (1947), 153–157.
 [24] The Rust Project Developers. 2024. The Cargo Book. https://doc.rust-lang.org/        [48] Samuel Miserendino, Michele Wang, Tejal Patwardhan, and Johannes Heidecke.
      cargo/                                                                                    2025. SWE-Lancer: Can Frontier LLMs Earn 1 Million from Real-World Freelance
 [25] The Serde Developers. 2025. The Serialize trait - Serde. Online. https://docs.rs/         Software Engineering? arXiv:arXiv:2502.12115
      serde/latest/serde/ser/trait.Serialize.html Accessed: 2025-07-14.                    [49] Mozilla. 2021. Mozilla Welcomes the Rust Foundation. https://blog.mozilla.org/
 [26] Jia Feng, Jiachen Liu, Cuiyun Gao, Chun Yong Chong, Chaozheng Wang, Shan                  en/mozilla/mozilla-welcomes-the-rust-foundation/ The Mozilla Blog.
      Gao, and Xin Xia. 2024. Complexcodeeval: A benchmark for evaluating large            [50] Niklas Muennighoff, Qian Liu, Armel Zebaze, Qinkai Zheng, Binyuan Hui,
      code models on more complex code. In Proceedings of the 39th IEEE/ACM Inter-              Terry Yue Zhuo, Swayam Singh, Xiangru Tang, Leandro Von Werra, and Shayne
      national Conference on Automated Software Engineering. 1895–1906.                         Longpre. 2023. Octopack: Instruction tuning code large language models. In
 [27] Kelsey R Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and Michelle L                 NeurIPS 2023 Workshop on Instruction Tuning and Instruction Following.
      Mazurek. 2021. Benefits and drawbacks of adopting a secure programming               [51] Niels Mündler, Mark Niklas Müller, Jingxuan He, and Martin Vechev. 2025.
      language: Rust as a case study. In Seventeenth Symposium on Usable Privacy and            SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents.
      Security (SOUPS 2021). 597–616.                                                           arXiv:2406.12952 [cs.SE] https://arxiv.org/abs/2406.12952
 [28] Andrew Gallant. 2024. ripgrep: recursively searches directories for a regex
      pattern. https://github.com/BurntSushi/ripgrep.
Evaluating and Improving Automated Repository-Level Rust Issue Resolution with LLM-based Agents                              ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


 [52] Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu. 2024. Towards            [83] Arie van Deursen, Maurício Aniche, and Joop Aué. 2016. Delft Students on
      Fixing Panic Bugs for Real-world Rust Programs. arXiv e-prints (2024), arXiv–            Software Architecture: DESOSA 2016. Delft University of Technology (2016).
      2408.                                                                               [84] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang,
 [53] OpenAI. 2024. Hello GPT-4o. Online. https://openai.com/index/hello-gpt-4o/               Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei Wei,
      Accessed: 2025-07-15.                                                                    and Jirong Wen. 2024. A Survey on Large Language Model Based Autonomous
 [54] OpenAI. 2024. Introducing SWE-bench, verified. https://openai.com/index/                 Agents. Frontiers of Computer Science 18, 6 (2024), 186345. https://doi.org/10.
      introducing-swe-bench-verified/. Accessed on 2025-06-23.                                 1007/s11704-024-40231-1
 [55] OpenAI. 2025. Introducing OpenAI o3 and o4-mini. Online. https://openai.            [85] Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and
      com/index/introducing-o3-and-o4-mini/ Accessed: 2025-07-15.                              Heng Ji. 2024. Executable Code Actions Elicit Better LLM Agents. In International
 [56] Guangsheng Ou, Mingwei Liu, Yuxuan Chen, Xin Peng, and Zibin Zheng. 2024.                Conference on Machine Learning (ICML). https://arxiv.org/abs/2402.01030
      Repository-level code translation benchmark targeting rust. arXiv preprint          [86] Xinchen Wang, Pengfei Gao, Xiangxin Meng, Chao Peng, Ruida Hu, Yun Lin,
      arXiv:2411.13990 (2024).                                                                 and Cuiyun Gao. 2024. AEGIS: An Agent-based Framework for General Bug
 [57] Shane Panter and Nasir Eisty. 2024. Rusty Linux: Advances in Rust for Linux Ker-         Reproduction from Issue Descriptions. arXiv:2411.18015 [cs.SE] https://arxiv.
      nel Development. In Proceedings of the 18th ACM/IEEE International Symposium             org/abs/2411.18015
      on Empirical Software Engineering and Measurement. Association for Computing        [87] Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen
      Machinery, New York, NY, USA. https://doi.org/10.1145/3674805.3690756                    Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, et al. 2024. Openhands:
 [58] David Peter. 2024. fd: A simple, fast and user-friendly alternative to ’find’.           An open platform for ai software developers as generalist agents. arXiv preprint
      https://github.com/sharkdp/fd.                                                           arXiv:2407.16741 (2024).
 [59] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Un-          [88] Wikipedia contributors. 2024. Tock (operating system) — Wikipedia, The Free
      derstanding memory and thread safety practices and issues in real-world Rust             Encyclopedia. https://en.wikipedia.org/wiki/Tock_(operating_system) [Online;
      programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming               accessed 28-June-2024].
      Language Design and Implementation. 763–779.                                        [89] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2024.
 [60] Muhammad Shihab Rashid, Christian Bock, Yuan Zhuang, Alexander Buch-                     Agentless: Demystifying llm-based software engineering agents. arXiv preprint
      holz, Tim Esler, Simon Valentin, Luca Franceschi, Martin Wistuba, Prabhu Teja            arXiv:2407.01489 (2024).
      Sivaprasad, Woo Jung Kim, Anoop Deoras, Giovanni Zappella, and Laurent              [90] Jiahong Xiang, Xiaoyang Xu, Fanchu Kong, Mingyuan Wu, Zizheng Zhang,
      Callot. 2025. SWE-PolyBench: A multi-language benchmark for repository level             Haotian Zhang, and Yuqun Zhang. 2024. How far can we go with practical
      evaluation of coding agents. arXiv:arXiv:2504.08703                                      function-level program repair? arXiv preprint arXiv:2404.12833 (2024).
 [61] Redox OS. 2023. Redox OS. https://redox-os.org/                                     [91] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu.
 [62] Redox OS Foundation. [n. d.]. Redox OS - The Rust Operating System. https:               2021. Memory-safety challenge considered solved? An in-depth study with
      //www.redox-os.org/. Accessed: 2024-06-28.                                               all Rust CVEs. ACM Transactions on Software Engineering and Methodology
 [63] Haifeng Ruan, Yuntong Zhang, and Abhik Roychoudhury. 2024. Specrover:                    (TOSEM) 31, 1 (2021), 1–25.
      Code intent extraction via llms. arXiv preprint arXiv:2408.02232 (2024).            [92] John Yang, Carlos E Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao,
 [64] S. Shanker. 2018. Safe Concurrency with Rust. http://squidarth.com/rc/rust/              Karthik Narasimhan, and Ofir Press. 2024. Swe-agent: Agent-computer inter-
      2018/06/04/rust-concurrency.html                                                         faces enable automated software engineering. Advances in Neural Information
 [65] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A Seshia, and Koushik Sen.             Processing Systems 37 (2024), 50528–50652.
      2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and            [93] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
      Dynamic Analysis. arXiv preprint arXiv:2412.14234 (2024).                                and Yuan Cao. 2022. ReAct: Synergizing Reasoning and Acting in Language
 [66] Hanzhuo Tan, Weihao Li, Xiaolong Tian, Siyi Wang, Jiaming Liu, Jing Li, and              Models. arXiv:arXiv:2210.03629
      Yuqun Zhang. 2025. SK2Decompile: LLM-based Two-Phase Binary Decompila-              [94] Hongrong Yin, Jinhong Huang, Yao Li, Yunwei Dong, and Tao Zhang. 2025.
      tion from Skeleton to Skin. arXiv preprint arXiv:2509.22114 (2025).                      BugRepro: Enhancing Android Bug Reproduction with Domain-Specific Knowl-
 [67] Hanzhuo Tan, Qi Luo, Ling Jiang, Zizheng Zhan, Jing Li, Haotian Zhang, and               edge Integration. arXiv:2505.14528 [cs.SE] https://arxiv.org/abs/2505.14528
      Yuqun Zhang. 2024. Prompt-based code completion via multi-retrieval aug-            [95] Hao Yu, Bo Shen, Dezhi Ran, Jiaxin Zhang, Qi Zhang, Yuchi Ma, Guangtai
      mented generation. ACM Transactions on Software Engineering and Methodology              Liang, Ying Li, Qianxiang Wang, and Tao Xie. 2024. Codereval: A benchmark of
      (2024).                                                                                  pragmatic code generation with generative pre-trained models. In Proceedings
 [68] Hanzhuo Tan, Qi Luo, Jing Li, and Yuqun Zhang. 2024. Llm4decompile: Decom-               of the 46th IEEE/ACM International Conference on Software Engineering. 1–12.
      piling binary code with large language models. arXiv preprint arXiv:2403.05286      [96] Daoguang Zan, Zhirong Huang, Wei Liu, Hanwu Chen, Linhao Zhang, Shulin
      (2024).                                                                                  Xin, Lu Chen, Qi Liu, Xiaojian Zhong, Aoyan Li, Siyao Liu, Yongsheng Xiao,
 [69] Hanzhuo Tan, Xiaolong Tian, Hanrui Qi, Jiaming Liu, Zuchen Gao, Siyi Wang,               Liangqiang Chen, Yuyu Zhang, Jing Su, Tianyu Liu, Rui Long, Kai Shen, and
      Qi Luo, Jing Li, and Yuqun Zhang. 2025. Decompile-Bench: Million-Scale Binary-           Liang Xiang. 2025. Multi-SWE-bench: A Multilingual Benchmark for Issue
      Source Function Pairs for Real-World Binary Decompilation. arXiv preprint                Resolving. https://doi.org/10.48550/arXiv.2504.02605 arXiv:2504.02605 [cs.SE]
      arXiv:2505.12668 (2025).                                                            [97] Zhengran Zeng, Yidong Wang, Rui Xie, Wei Ye, and Shikun Zhang. 2024.
 [70] Ningzhi Tang, Meng Chen, Zheng Ning, Aakash Bansal, Yu Huang, Collin                     CoderUJB: An Executable and Unified Java Benchmark for Practical Program-
      McMillan, and Toby Jia-Jun Li. 2024. A Study on Developer Behaviors for                  ming Scenarios. arXiv:arXiv:2403.19287
      Validating and Repairing LLM-Generated Code Using Eye Tracking and IDE              [98] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung, Jin Liu, Daoguang Zan, Yi
      Actions. arXiv preprint arXiv:2405.16081 (2024).                                         Mao, Jian-Guang Lou, and Weizhu Chen. 2023. Repocoder: Repository-level
 [71] The Bevy Community. 2024. Bevy: A refreshingly simple data-driven game                   code completion through iterative retrieval and generation. arXiv preprint
      engine built in Rust. https://github.com/bevyengine/bevy.                                arXiv:2303.12570 (2023).
 [72] The Boa Developers. 2024. Boa: An embeddable and experimental Javascript            [99] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu,
      engine written in Rust. https://github.com/boa-dev/boa.                                  Zhenhua Dong, and Ji-Rong Wen. 2024. A Survey on the Memory Mechanism
 [73] The Rayon Developers. 2024. Rayon: A data parallelism library for Rust. https:           of Large Language Model Based Agents. arXiv preprint arXiv:2404.13501 (2024).
      //github.com/rayon-rs/rayon.                                                             arXiv:2404.13501 https://arxiv.org/abs/2404.13501
 [74] The Rust Project Developers. 2025. Macros. https://doc.rust-lang.org/book/ch19-    [100] Yu Zhao, Tingting Yu, Ting Su, Yang Liu, Wei Zheng, Jingzhi Zhang, and William
      06-macros.html. Accessed: 2025-07-15.                                                    G.J. Halfond. 2019. ReCDroid: Automatically Reproducing Android Application
 [75] The Rust Project Developers. 2025. Module ast. https://doc.rust-lang.org/beta/           Crashes from Bug Reports. In 2019 IEEE/ACM 41st International Conference on
      nightly-rustc/rustc_ast/ast/index.html. Accessed: 2025-07-15.                            Software Engineering (ICSE). 128–139. https://doi.org/10.1109/ICSE.2019.00030
 [76] The Rust Project Developers. 2025. The Rust Programming Language Repository.       [101] Xiaoye Zheng, Zhiyuan Wan, Yun Zhang, Rui Chang, and David Lo. 2023. A
      https://github.com/rust-lang/rust. Source code for the Rust compiler and                 closer look at the security risks in the rust ecosystem. ACM Transactions on
      standard library, including proc_macro and rustc_ast. Accessed: 2025-07-15.              Software Engineering and Methodology 33, 2 (2023), 1–30.
 [77] The Rust Team. 2019. Rust: Empowering everyone to build reliable and efficient
      software. https://www.rust-lang.org/
 [78] The Rust team. 2021. The Rust Programming Language. http://rust-lang.org/
 [79] The Rust Team. 2022. Rust Survey 2021 Results. https://blog.rust-lang.org/2022/
      02/15/Rust-Survey-2021.html
 [80] The Servo Project. 2019. The Servo Browser Engine. https://servo.org/
 [81] The Tokio Authors. 2024. Axum: Ergonomic and modular web framework built
      with Tokio, Tower, and Hyper. https://github.com/tokio-rs/axum.
 [82] The Tokio Authors. 2024. Tokio: A runtime for writing reliable asynchronous
      applications with Rust. https://github.com/tokio-rs/tokio.
