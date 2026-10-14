                                         From Helpful to Trustworthy: LLM Agents for Pair Programming
                                                                                                              Ragib Shahariar Ayon∗
                                                                                                                  Texas State University
                                                                                                                  San Marcos, TX, USA
                                                                                                                    ipd21@txstate.edu

                                         Abstract                                                                                workflows that make intent explicit, enable systematic validation,
                                         LLM-based coding agents are increasingly used to generate code,                         and produce evolution-ready artifacts [9].
                                         tests, and documentation. Still, their outputs can be plausible yet                        We study a multi-agent system (MAS) in which a driver agent
                                         misaligned with developer intent and provide limited evidence for                       proposes artifacts and a navigator agent critiques them, each operat-
                                         review in evolving projects. This limits our understanding of how                       ing through role-specific prompts and separate interaction histories
                                                                                                                                 while sharing a persistent project context. Both roles are occupied
arXiv:2604.10300v1 [cs.SE] 11 Apr 2026




                                         to structure LLM pair-programming workflows so that artifacts
                                         remain reliable, auditable, and maintainable over time. To address                      by LLM agents, instantiated either as the same base model under
                                         this gap, this doctoral research proposes a systematic study of multi-                  different prompts or as models specialized for generation and re-
                                         agent LLM pair programming that externalizes intent and uses                            view. We choose this driver-navigator design over a single-agent
                                         development tools for iterative validation. The plan includes three                     setup because it provides a minimal and interpretable separation
                                         studies: translating informal problem statements into standards-                        between proposal and critique, and prior work suggests that such
                                         aligned requirements and formal specifications; refining tests and                      role specialization can improve code quality through structured,
                                         implementations using automated feedback, such as solver-backed                         iterative feedback [14]. A natural concern with this setup is that, if
                                         counterexamples; and supporting maintenance tasks, including                            the navigator is itself an LLM, the developer may simply be trading
                                         refactoring, API migrations, and documentation updates, while                           one auditability problem for another [7, 13]. We address this by
                                         preserving validated behavior. The expected outcome is a clearer                        constraining the navigator to produce machine-checkable contracts
                                         understanding of when multi-agent workflows increase trust, along                       and formal specifications rather than free-form judgments, which
                                         with practical guidance for building reliable programming assistants                    are then validated by deterministic verifiers that return proofs or
                                         for real-world development.                                                             counterexamples [3–5, 8]. Trust thus shifts away from one model’s
                                                                                                                                 assessment of another and toward externally verifiable evidence,
                                         CCS Concepts                                                                            leaving the developer with one concrete responsibility: confirming
                                                                                                                                 that the specification captures their intent.
                                         • Software and its engineering → Formal software verifica-
                                                                                                                                    Initial results show that verifier-guided LLM-based specifica-
                                         tion.
                                                                                                                                 tion synthesis, through iterative feedback, improves correctness
                                                                                                                                 and completeness. Building on this, we plan to investigate pair-
                                         Keywords
                                                                                                                                 programming LLM agents as an end-to-end, evidence-driven work-
                                         Agentic AI, Large Language Model, Pair Programming                                      flow that translates intent into standards-aligned requirements and
                                         ACM Reference Format:                                                                   formal specifications, refines code and tests via automated feedback
                                         Ragib Shahariar Ayon. 2026. From Helpful to Trustworthy: LLM Agents                     (e.g., SMT-based counterexamples), and sustains artifacts across
                                         for Pair Programming . In 34th ACM Joint European Software Engineering                  software evolution.
                                         Conference and Symposium on the Foundations of Software Engineering (FSE
                                         Companion ’26), July 5–9, 2026, Montreal, QC, Canada. ACM, New York, NY,
                                         USA, 2 pages. https://doi.org/10.1145/3803437.3804875
                                                                                                                                 2   Background and Related Work
                                         1    Introduction                                                                       Requirements and context generation: ArchCode extracts func-
                                         LLM-based coding agents are increasingly used for code genera-                          tional and non-functional requirements to guide code and test gen-
                                         tion, repair, and interactive assistance. Despite strong empirical                      eration [6], and SpecGen and AutoReSpec generate and refine veri-
                                         performance, developers may still be cautious about relying on                          fiable specifications using verifier feedback [3, 8]. These tools, how-
                                         these tools as fully autonomous collaborators in realistic projects,                    ever, target specification generation in isolation rather than embed-
                                         since their outputs can appear plausible while remaining misaligned                     ding requirement elicitation within a pair-programming workflow.
                                         with developer intent and therefore still require human scrutiny [7,                    Our preliminary work begins to address this [2, 3], but how a driver-
                                         10, 13, 15]. Improving trust in LLM-assisted development requires                       navigator pair can co-produce standards-aligned requirements and
                                                                                                                                 formal specifications remains an open question.
                                         ∗ Advisor: Shibbir Ahmed, Assistant Professor, Texas State University, TX, USA.
                                                                                                                                    Code and test generation with automated feedback: Au-
                                                                                                                                 toCodeRover and SpecRover couple iterative code search with patch
                                                                                                                                 generation and specification inference [10, 15], Tian et al. improve
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   equivalent mutant detection via code embeddings [11]. These ef-
                                         FSE Companion ’26, Montreal, QC, Canada                                                 forts operate in single-agent or single-stage settings and do not
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2636-1/26/07                                                        expose solver-backed counterexamples as auditable artifacts within
                                         https://doi.org/10.1145/3803437.3804875                                                 a driver–navigator loop. Our proposed TDD study will examine
FSE Companion ’26, July 5–9, 2026, Montreal, QC, Canada                                                                                 Ragib Shahariar Ayon


whether such a setup improves consistency with requirements and          to quantify when multi-agent collaboration improves reliability and
produces more trustworthy, reproducible feedback.                        trust signals relative to single-agent baselines. It will investigate
   Maintenance and repository-scale evolution: Tufano et al.             how agents can externalize intent as requirements, use tests and
translate natural-language review comments into code transforma-         solver-backed feedback as auditable evidence during iteration, and
tions [12], and Abreu et al. predict risky diffs to support stability-   maintain artifacts through refactoring, documentation, and evolv-
preserving gating at scale [1]. Neither uses pre-existing specifi-       ing features at scale. The goal is to develop a practical workflow
cations and test suites as behavioral constraints to confirm that        that produces reliable artifacts and trust signals to support safer
changes preserve validated behavior. Our proposed maintenance            adoption. in software engineering research and practice.
study will investigate whether anchoring refactoring, dependency
upgrades, and documentation updates to such constraints reduces          References
regressions and keeps generated artifacts trustworthy.                    [1] Rui Abreu, Vijayaraghavan Murali, Peter C Rigby, Chandra Maddila, Weiyan
                                                                              Sun, Jun Ge, Kaavya Chinniah, Audris Mockus, Megh Mehta, and Nachiappan
                                                                              Nagappan. 2025. Moving Faster and Reducing Risk: Using LLMs in Release
3    Research progress and plan                                               Deployment. In 2025 IEEE/ACM 47th International Conference on Software Engi-
                                                                              neering: Software Engineering in Practice (ICSE-SEIP). 448–457. doi:10.1109/ICSE-
   Research Progress. In our initial study on formal specification            SEIP66354.2025.00045
generation, we introduced AutoReSpec, a verifier-guided collabo-          [2] Ragib Shahariar Ayon. 2026. AutoJML: Generation and Verification of JML
rative LLM framework for JML synthesis that classifies programs               Specifications using LLM Agents. IEEE Pulse 17, 1. doi:10.1109/MPULS.2026.
                                                                              3659250 Manuscript Number: department-Ayon-01-27-2026.
by structural complexity, selects a pair of primary and fallback          [3] Ragib Shahariar Ayon and Shibbir Ahmed. 2026. AutoReSpec: A Framework
LLM pair, and iteratively refines specifications using verifier feed-         for Generating Specification using Large Language Models. In Proceedings of
back; when the primary model fails, a collaborative fallback model            the 2026 IEEE/ACM Third International Conference on AI Foundation Models and
                                                                              Software Engineering (FORGE ’26) (Rio de Janeiro, Brazil) (FORGE ’26). doi:10.
receives the last failed candidate and verifier errors for focused            1145/3793655.3793731 April 12–13, 2026.
recovery [3]. On a 72-program benchmark, AutoReSpec verified 67           [4] Ragib Shahariar Ayon and Shibbir Ahmed. 2026. SpecPylot: Python Specification
                                                                              Generation with Large Language Models. In Proceedings of the 31st ACM Joint
programs, achieving a 58.2% success probability and 69.2% complete-           European Software Engineering Conference and Symposium on the Foundations of
ness, while reducing the average evaluation time by 26.89% over               Software Engineering Companion (FSE Companion ’26) (Montreal, QC, Canada).
prior methods. Building on these results, we developed AutoJML                ACM. doi:10.1145/3803437.3806427
                                                                          [5] Madeline Endres, Sarah Fakhoury, Saikat Chakraborty, and Shuvendu K Lahiri.
to study the impact of ReAct-based LLM agents on specification                2024. Can large language models transform natural language intent into formal
generation. AutoJML automates JML specification synthesis via                 method postconditions? Proceedings of the ACM on Software Engineering 1, FSE
                                                                              (2024), 1889–1912.
iterative verification and mutation-driven completeness feedback,         [6] Hojae Han, Jaejin Kim, Jaeseok Yoo, Youngwon Lee, and Seung-won Hwang. 2024.
and additionally leverages web-based context retrieval [2]. On a 120-         ArchCode: Incorporating Software Requirements in Code Generation with Large
program benchmark, AutoJML verified 109 programs, achieving                   Language Models. In Proceedings of the 62nd Annual Meeting of the Association for
                                                                              Computational Linguistics (Volume 1: Long Papers), Lun-Wei Ku, Andre Martins,
an average completeness of 79.3%, with significant improvements               and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok,
over state-of-the-art baselines on challenging control-flow patterns,         Thailand, 13520–13552. doi:10.18653/v1/2024.acl-long.730
including multi-path loops (81.48%) and nested loops (85.71%).            [7] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2026. A
                                                                              Survey on Large Language Models for Code Generation. ACM Trans. Softw. Eng.
                                                                              Methodol. 35, 2, Article 58 (Jan. 2026), 72 pages. doi:10.1145/3747588
   Future Plan. We want to investigate workflows in a pair pro-           [8] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Automated
gramming, multi-agent setting, where driver and navigator LLMs                Generation of Formal Program Specifications via Large Language Models. IEEE
use requirements and specifications to iteratively refine tests, im-          Press, 16–28. https://doi.org/10.1109/ICSE55347.2025.00129
                                                                          [9] Abhik Roychoudhury, Corina Pasareanu, Michael Pradel, and Baishakhi Ray.
plementations, and maintenance updates. Refinement is guided by               2025. Agentic ai software engineer: Programming with trust. arXiv preprint
automated feedback signals, including SMT-based counterexamples,              arXiv:2502.13767 (2025).
while tests and specifications constrain changes to preserve vali-       [10] Haifeng Ruan, Yuntong Zhang, and Abhik Roychoudhury. 2025. SpecRover: Code
                                                                              Intent Extraction via LLMs. In Proceedings of the IEEE/ACM 47th International
dated behavior across refactoring, documentation, and upgrades.               Conference on Software Engineering (Ottawa, Ontario, Canada) (ICSE ’25). IEEE
We study the following research question: How effective is the                Press, 963–974. doi:10.1109/ICSE55347.2025.00080
                                                                         [11] Zhao Tian, Junjie Chen, and Xiangyu Zhang. 2025. Fixing Large Language Models’
workflow at producing tests and implementations that are consis-              Specification Misunderstanding for Better Code Generation. In Proceedings of the
tent with requirements and specifications? How do solver-backed               IEEE/ACM 47th International Conference on Software Engineering (Ottawa, Ontario,
counterexamples and automated feedback influence refinement                   Canada) (ICSE ’25). IEEE Press, 1514–1526. doi:10.1109/ICSE55347.2025.00108
                                                                         [12] Rosalia Tufano, Luca Pascarella, Michele Tufano, Denys Poshyvanyk, and
behavior, and which types of programs benefit most? How does                  Gabriele Bavota. 2021. Towards Automating Code Review Activities. In 2021
feedback affect trustworthiness, measured by pass rates, inconclu-            IEEE/ACM 43rd International Conference on Software Engineering (ICSE). 163–174.
sive outcomes, and reproducibility of failures? How well can agents           doi:10.1109/ICSE43902.2021.00027
                                                                         [13] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao,
perform maintenance tasks while preserving existing behavior?                 Karthik Narasimhan, and Ofir Press. 2024. SWE-agent: agent-computer interfaces
How effective are test and specification constraints at preventing            enable automated software engineering. In Proceedings of the 38th International
regressions during iterative maintenance and migration? How ac-               Conference on Neural Information Processing Systems (Vancouver, BC, Canada)
                                                                              (NIPS ’24). Curran Associates Inc., Red Hook, NY, USA, Article 1601, 125 pages.
curate and useful are the generated documentation artifacts, and         [14] Huan Zhang, Wei Cheng, Yuhan Wu, and Wei Hu. 2024. A pair programming
do they introduce misleading or biased statements?                            framework for code generation via multi-plan exploration and feedback-driven
                                                                              refinement. In Proceedings of the 39th IEEE/ACM International Conference on
                                                                              Automated Software Engineering. 1319–1331.
4    Conclusion                                                          [15] Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, and Abhik Roychoudhury. 2024. Au-
                                                                              toCodeRover: Autonomous Program Improvement. In Proceedings of the 33rd
This doctoral research aims to shift multi-agent LLM pair program-            ACM SIGSOFT International Symposium on Software Testing and Analysis (Vienna,
ming from helpful assistance to trustworthy support in real-world             Austria) (ISSTA 2024). Association for Computing Machinery, New York, NY, USA,
software development. We will study a driver-and-navigator setup              1592–1604. doi:10.1145/3650212.3680384
