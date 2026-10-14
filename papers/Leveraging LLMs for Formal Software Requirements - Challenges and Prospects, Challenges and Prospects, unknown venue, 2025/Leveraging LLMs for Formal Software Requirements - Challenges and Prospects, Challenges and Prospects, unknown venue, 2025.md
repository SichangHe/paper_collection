Leveraging LLMs for Formal Software Requirements:
Challenges and Prospects
Arshad Beg1,*,† , Diarmuid O’Donoghue1,† and Rosemary Monahan1,†
1
    Maynooth University, Maynooth, Ireland.


              Abstract
               Software correctness is ensured mathematically through formal verification, which requires the generation of a
               formal requirement specification and an implementation that must be verified. Tools such as model-checkers and
               theorem provers ensure software correctness by verifying the implementation against the specification. Formal
               methods deployment is regularly enforced in the development of safety-critical systems e.g. aerospace, medical
               devices and autonomous systems. Generating these specifications from informal and ambiguous natural language
               requirements remains the key challenge. Our project, VERIFYAI 1 , aims to investigate automated and semi-
               automated approaches to bridge this gap, using techniques from Natural Language Processing (NLP), ontology-
               based domain modelling, artefact reuse, and large language models (LLMs). This position paper presents a
               preliminary synthesis of relevant literature to identify recurring challenges and prospective research directions in
               the generation of verifiable specifications from informal requirements.

               Keywords
              Large Language Models, Knowledge Representation and Reasoning, Formal Languages, Software Requirements-
              {Engineering, Specifications}, Formal Verification, Theorem Proving, Model Checking, Chain-of-Thought (CoT),
              Prompt-Engineering, {Zero, One, and Few}-shot prompting




1. Introduction
As software systems grow in complexity and criticality, so does the need for scalable verification methods
that ensure correctness and reliability. Formal verification is especially important in safety-critical systems
where minor software errors can lead to serious consequences, including loss of life, environmental
damage, or large-scale system failures. Under all circumstances, the software used in sectors like aviation,
healthcare, automotive, and nuclear control must behave exactly as intended. While testing can only
check specific scenarios, formal verification uses mathematical techniques to prove that a system meets
its specifications under every possible condition. This level of assurance is crucial when human safety
depends on software behaving reliably. The purpose of sound software engineering principles is to
catch flaws early in the design phase, ensuring consistency between requirements and implementation.
The mathematical techniques used in formal methods improve trust, and support compliance with
industry standards and regulations. However, their adoption in industry is consistently hindered by the
challenges of writing and maintaining formal specifications, which demand rigorous developer training
and significantly increase the software development cycle time by up to 30% [1]. This motivates research
1
  https://github.com/arshadbeg/OVERLAY2025_SupportingDocs.git
Overlay2025: 7th International Workshop on Artificial Intelligence and fOrmal VERification, Logic, Automata, and sYnthesis
*
  Corresponding author.
†
  These authors contributed equally.
$ arshad.beg@mu.ie (A. Beg); diarmuid.odonoghue@mu.ie (D. O’Donoghue); rosemary.monahan@mu.ie (R. Monahan)
 0009-0004-6939-0411 (A. Beg); 0000-0002-3680-4217 (D. O’Donoghue); 0000-0003-3886-4675 (R. Monahan)
              © 2022 Copyright for this paper by its authors. Use permitted under Creative Commons License Attribution 4.0 International (CC BY 4.0).
into automated and semi-automated approaches that can make formal verification more accessible to a
wider audience of software engineers.
   The VERIFYAI project [2] aims to address a central challenge of formal software engineering:
translating informal, natural-language requirements into formal, verifiable specifications. This paper
outlines the challenges and prospects in leveraging Large Language Models (LLMs) for formalising
software requirements. The project aims to integrate techniques from Natural Language Processing (NLP),
ontology-driven domain modelling, artefact reuse, and large language models (LLMs) to support the
automated generation and traceability of formal specifications. Like all other fields, the development of
large language models (LLMs) has opened a world of opportunities for the challenge of formalisation of
software requirements. We consolidate initial findings to highlight research gaps and recurring difficulties
in LLM-assisted formal specification generation. Noting firstly that the main body of the paper is
supported by several detailed Appendices available at https://github.com/arshadbeg/OVERLAY2025_
SupportingDocs.git.
The key contributions of this paper are as follows:
Identification of Core Challenges in Formalisation: We present a structured analysis of the barriers to
translating informal, natural language software requirements into formal specifications, such as ambiguity,
lack of domain models, and LLM instability.
VERIFYAI Research Framework: We propose our research framework, which integrates LLMs with
NLP, ontology-driven modelling, and artefact reuse to support the semi-automated generation of verifiable
formal specifications.
State-of-the-Art Synthesis: Through a focused literature review, we categorise and compare (Section
2, supported by Appendix A) recent LLM-based tools and techniques—such as Req2Spec, SpecGen,
AssertLLM, and nl2spec—highlighting their approaches, strengths, and limitations in requirement
formalisation.
Experimental Evaluation: We include empirical evaluations (Appendices B and C) comparing multiple
SMT solvers (Alt-Ergo, Z3, CVC4, CVC5) in terms of specification verification success and execution
time, using the Frama-C PathCrawler tool and standard program sets.
Highlighting Gaps and Future Directions: Based on our synthesis, we outline critical open problems
such as prompt instability, fragility of formal outputs, and the need for domain-specific context grounding
(Appendix D). These pave the way for developing more robust LLM-based formal specification pipelines.
Positioning for Long-Term Vision: As a position paper, our work serves as a foundational step toward a
longer-term vision of trustworthy, LLM-assisted formal methods tooling that bridges the expertise gap in
safety-critical software development.
   The structure of the paper is: Section 2 describes a focused state of the art. Section 3 outlines the
challenges and future directions for the research, supported by Appendix A that outlines the experiment
setup and analysis performed on an example of the PathCrawler tool of Frama-C where we have re-
simulated the methodology presented in [3]. This analysis is based on four provers available in Frama-C
i.e. Alt-Ergo, Z3, CVC4 and CVC5. Appendix B presents the execution time comparison for these
provers on the programs provided in [4]. Section 4 discusses our plans for future work and Section 5
concludes the paper.
2. State of the Art
This section synthesises what we found to be the state of the art. The main research questions for
conducting our systematic literature review on the topic were as follows:
RQ1: What methodologies leverage Large Language Models (LLMs) to transform natural language
software requirements into formal notations?
RQ2: What are the emerging trends and future research directions in using LLMs for formal requirements
formalisation?
   Here, we summarise our main findings. For a comprehensive overview of the literature survey, including
detailed comparisons and categorised insights, we encourage readers to consult the accompanying GitHub
repository, which presents the full set of supporting tables.
   GPT-3.5 has assisted requirement analysis for code verification [5], while Explanation-Refiner inte-
grates LLMs with theorem provers for NLI validation and iterative correction [6]. Evaluation of GPT-4o
with VeriFast shows generation of functional specifications, though verification remains limited due to
redundancy and failed assertions [7].
   The nl2spec tool supports interactive synthesis from unstructured requirements [8], while the SpecSyn
tool improves sequence-to-sequence contract generation with a 21% accuracy gain [9]. Req2Spec
converts 71% of BOSCH automotive requirements into formal specs [10], while SpecGen uses prompt
mutation and verification feedback to improve LLM-generated specifications, succeeding on 279 out of
384 benchmark programs [11]. In the hardware domain, AssertLLM synthesizes assertions with 89%
correctness via multi-phase prompting and validation [12], while VLSI applications leverage LLMs for
spec review and generation in SpecLLM [13]. Smart grid requirements have been formalised using
GPT-4o and Claude 3.5, achieving F1 scores between 79% and 94% [14]. The trend in F1-scores observed
by authors of [14] suggested that GPT-4o and Claude 3.5 not only maintain robustness but may actually
benefit from increased system specification complexity, highlighting a potential alignment between model
reasoning depth and specification richness. This aspect not mirrored in Gemini 1.5 or GPT-3.5-turbo
and warranting further investigation. NASA’s software verification effort surfaced requirement errors,
demonstrating practical utility of LLM-in-the-loop workflows [15].
   NL-to-LTL translation has seen progress via few-shot prompting and dynamic reasoning [16], achieving
94.4% accuracy. Likewise, NL-to-JML contract synthesis for Java programs has been explored with
promising results [17]. Historical systems like RSL [18], ARSENAL [19], and RML [20] demonstrated
early rule-based and logic-based extraction pipelines, while hybrid neuro-symbolic systems offer greater
reliability. SAT-LLM couples SMT solvers with LLMs to detect inconsistencies with F1 of 0.91 [21]
and LeanDojo, ReProver, and Thor enhance formal proving via retrieval-augmented generation and
LLM-guided reasoning [22, 23]. IDE-integrated efforts like those combining Copilot with PathCrawler
and EVA demonstrate semi-automated ACSL specification generation [24, 3].
   As we expected, assertion-level synthesis shows better reliability than full contract generation. For
example, Laurel generates assertions for Dafny with over 50% success [25], and AssertLLM exceeds
89% correctness when guided by contract type and context. Full specifications are more error-prone,
often requiring multiple prompt iterations or external validation [11].
   LLM selection and prompting strategies critically affect performance. While zero-shot prompting is
strong in base performance [26], one-shot [27] and few-shot [28] offer alternative trade-offs. Chain-of-
Thought (CoT) prompting improves logical flow via intermediate steps [29], and like Structured CoT
(SCoT) [30] it can suffer from context decay in long prompts (“lost-in-the-middle”) [31], yet zero-shot
often remains competitive [32].
   Advanced prompting methods like Automate-CoT generate CoT examples automatically [33], while
Reprompting uses Gibbs sampling to escape prompt local optima [34]. Structured prompting with graphs
and trees improves reasoning robustness and efficiency [35]. RAG (Retrieval-Augmented Generation)
improves grounding for knowledge-intensive synthesis [36]. [37] discusses a wider range of almost
30 prompting strategies, some of which seem not to have been explored in relation to formalising
specifications. Of course, this does not include related approaches such as fine-tuning LLM via LoRA
adaptation training [38], but this may only be applicable when there is access to the LLM’s architecture
and weights. Additionally, reinforcement learning (RL) may help with specific challenges, opening even
more avenues for exploration.
Key Observations:
   Based on our literature survey, we proceed with some key observations. We observed a significant
difference between the success rates of assertion generation and full contract synthesis using LLMs.
AssertLLM [12] and Laurel [25] achieved high accuracy in generating helper assertions for programs
written in Dafny language [39] and design-specific verification statements. These tools achieved an
accuracy of 89% and over 50%, operating at a local level on source code or isolated signals. On the
other hand, [17] reported that while generating formal specifications for Java Modelling Language (JML)
contracts or temporal logic formulas ended up in frequent verification failures by the SMT solvers
embedded in OpenJML [40]. This happened even if the output appeared semantically sound, leading
to the conclusion of disparity between human-readable correctness and automated formal verification,
especially when the source code was written for complex tasks.
   In general, we observed that tasks with small scope and well-defined semantics yield better results
where the limited context in these assertions helps in improving verification accuracy [11, 9]. LLMs
handle such tasks more reliably due to reduced ambiguity and fewer dependencies on broader system
knowledge. On the other hand, for larger program segments, end-to-end contract synthesis involves
multiple interacting components or function bodies. It demands a deeper understanding of program
semantics, logic, and behaviour over time. SpecGen [11] and SpecSyn [9] presented significant progress
in tackling such challenges. However, their outputs require post-processing steps, such as mutation
operators or human-in-the-loop (software testing experts were involved), before the generated outputs are
usable for formal verification.
   The effort accuracy is influenced by tool design and integration. For example, tools like nl2spec [8]
improve generated specification quality through step-by-step refinement, adopting iterative and user-
in-the-loop approach to help address some LLM limitations. Similarly, prompt engineering techniques
utilising guided templates or Chain-of-Thought (CoT) [7, 41, 42] promised improved output coherence
and correctness. These strategies work well in scenarios involving localised tasks, such as assertion
synthesis or narrow-scope descriptions. As the program size and complexity of the specification goal
increase, the chances of ambiguity, under-specification, and logical inconsistency increase. Therefore, we
conclude that the current LLM architectures excel in focused, declarative tasks but require augmentation
for broader specification goals. However, [43] showed that different versions of language models including
LLM, can vary greatly in their responses to the same queries, suggesting that much experimental work
might be required to achieve optimum results.
   We conclude from our synthesis of the current literature that the research trend is increasing in
combining the strength of LLMs, symbolic reasoning and iterative user interaction. At the moment,
assertion generation dominates in terms of accuracy and usability, but the parallel efforts of better prompt
design, domain-specific fine-tuning, and verifier-in-the-loop are closely matching the performance of the
process. The challenges of abstraction and consistency drive research efforts in this domain.
3. Challenges and Future Directions
Based on our finding, we summarise five key challenges that we have identified, as well as our research
goals with brief description given in Table 1. A detailed description of these is included in Appendix C.

 Challenges                                              Future Directions
 C1: Semantic Ambiguity                                  F1: Human-in-the-loop Formalisation
 Ambiguity in natural language due to context-           Combines LLM support with domain expert over-
 dependence and jargon affects requirement in-           sight to improve accuracy, reduce ambiguity, and
 terpretation. Needs structured knowledge and            increase trust via feedback and interactive refine-
 human-in-the-loop refinement.                           ments.
 C2: Lack of Ground Truth Datasets                       F3: Standardised Benchmarks
 Absence of standardised, annotated datasets lim-        Creation of high-quality, domain-diverse datasets
 its model training, reproducibility, and scalability.   will enable consistent evaluation and push the
                                                         field forward.
 C3: Tool Interoperability                               F4: Neuro-symbolic Reasoning
 Formal verification tools lack standard interfaces      Combines neural flexibility with symbolic preci-
 and integration capabilities, hampering automa-         sion to improve integration, consistency, and con-
 tion.                                                   straint enforcement.
 C4: Traceability Across Artefacts                       F5: Interactive Traceability Tools
 Difficult to maintain consistent trace links between    Tools that enable visual navigation, version track-
 text, models, code, and tests over lifecycle.           ing, and LLM-assisted trace linking improve us-
                                                         ability and compliance.
 C5: Explainability and User Trust                       F2: Multi-modal Artefact Alignment
 Limited transparency in LLM-generated outputs           Integrating diverse input types (text, diagrams, ta-
 reduces trust, especially in safety-critical do-        bles) through semantic matching increases clarity
 mains.                                                  and confidence in outputs.
Table 1
Challenges and Corresponding Future Directions for VERIFYAI Project

   Semantic ambiguity (C1) due to natural language remains a critical issue, needing structured domain
knowledge and improved human-in-the-loop interventions. The lack of publicly available, high-quality
datasets (C2) hinders model training, reproducibility, and scalability. Tool interoperability (C3) is impeded
by incompatible formats and absence of standardised interfaces, complicating automation. Ensuring
traceability across artefact lifecycles (C4) is essential but difficult without explainable and collaborative
processes. In addition, explainability and user trust (C5) are limited by opaque model behavior and
insufficient rationale in outputs. To address these, human-in-the-loop formalisation (F1) offers controlled
semi-automation and improved trust, while multi-modal artefact alignment (F2) enables contextual
completeness via diverse input formats. The creation of standardised benchmarks (F3) would mitigate
dataset-related limitations and promote progress. Neuro-symbolic reasoning (F4) blends LLM flexibility
with logic-based precision, enhancing model reliability. Finally, interactive traceability tools (F5) that
support collaboration, visual navigation, and auditability are crucial for regulated and complex software
domains.
4. Embedding LLMs in the Specification Generation
4.1. Planned Evaluation of Prompting Strategies
A systematic and quantitative evaluation of prompting strategies is the central part of our planned research.
In particular, we intend to compare zero-shot, one-shot, few-shot, and Chain-of-Thought (CoT) prompting
across both assertion-level and full-contract generation tasks. Prior work in the literature [26–35]
suggests that prompt type and articulation can significantly influence specification quality. However, a
comprehensive evaluation requires a larger and more diverse benchmark than we currently report.
   Future experiments will therefore assess prompt sensitivity using precision, recall, and F1-based
correctness metrics, and investigate robustness under small variations of prompt formulation. We
anticipate that assertion-level tasks will prove more stable under prompt rephrasing, whereas full-contract
synthesis may show higher variability — an observation that motivates deeper analysis in follow-up work.
Our current contribution is to highlight the importance of prompt design in our work and to outline how
this dimension will be systematically investigated going forward.

4.2. Human-in-the-Loop Integration and Interoperability Considerations
Our experiments currently implement the early stages of a human-in-the-loop process through manual
review. In both the Tritype baseline and PathCrawler-augmented workflows, every LLM-generated ACSL
specification was checked by at least one author with formal methods expertise. This review ensured
(i) semantic alignment with intended behavior, (ii) logical completeness, and (iii) iterative refinement
by feeding corrected fragments back into the prompts. Although active learning is not yet integrated,
our project approach anticipates it: revised specifications, along with their source code and verification
results, can be versioned and selectively reused for retraining or fine-tuning.
   Figure 1b shows our proposed workflow based on the state of the art and figured out challenges in
Sections 2 and 3. Natural language requirements and domain ontologies form the input, grounding the
LLM in the target context. Different prompt strategies (zero-shot, few-shot, and Chain-of-Thought) shape
how inputs are presented for specification generation. Outputs are stored in a tool-neutral intermediate
format (JSON-LD), which can be translated into the syntax required by verification tools. These tools
check the generated specifications, while symbolic reasoning provides constraint-based feedback that
helps refine them. Human reviewers remain part of the loop, validating results, focusing on manageable
units, and collecting useful examples for future adaptation. The design is modular, so new reasoning
engines, prompt methods, or domain adapters can be added without changing the overall pipeline.
   For interoperability, the pipeline currently uses custom scripts to convert LLM outputs to tool-specific
formats (e.g., ACSL for Frama-C, JML for OpenJML). While functional, this approach is not generalisable.
As part of VERIFYAI, we plan to design a lightweight JSON-LD-based schema that maps to multiple
formal languages. This would allow LLM outputs to be stored in a tool-agnostic format and exported to
different targets, potentially supporting Frama-C, OpenJML, Dafny, and others with minimal per-tool
changes.

4.3. Symbolic Reasoning, Traceability, and Scalability Outlook
In our initial Tritype experiments, symbolic solvers were used only for post-generation verification. We
see potential for tighter integration, where solver feedback—such as unsatisfiable path conditions—could
guide the LLM during generation, reducing logical errors before verification. Currently, traceability relies
                                                                                   Input:
                                                                       Natural Language Requirements
                 Input C Program                                            + Domain Ontologies

                                                                          Different Prompt Strategies
              PathCrawler Analysis                                        (zero-shot, few-shot, CoT)


        Symbolic Paths + I/O Examples                                          LLM Specification
                                                                                 Generation

         Prompt LLM for ACSL Specs                                         Tool-Neutral Intermediate
                                                                              Format (JSON-LD)
        Annotated C Code (with ACSL)
                                                                              Verification Tools
                                                                         + Symbolic Reasoning Output
          Frama-C WP + SMT Solvers
                                                                         Human-in-the-Loop Validation
         Verification Goals + Outcomes                                      + Example Collection

(a) Methodology of the initial experiments following       (b) Proposed Workflow for the VERIFYAI pipeline:
    the approach of [3], combining LLM with symbolic           Natural-language requirements and domain ontolo-
    analysis tools in the Frama-C ecosystem. The work-         gies are combined with prompt strategies to gen-
    flow integrates path-based I/O examples and veri-          erate formal specifications via LLMs. Outputs in
    fication outputs to guide the generation of context-       JSON-LD feed verification tools, with symbolic and
    aware ACSL specifications.                                 human feedback refining results.
Figure 1: Methodology adopted for initial and future experiments


on manual annotations linking specification fragments to source code and natural-language requirements.
We are exploring semi-automated approaches where the LLM proposes initial links for human validation.
These links could be stored in a graph database to support version-aware navigation and visual trace
maps, which would be particularly valuable in regulated settings.
  We aim to build datasets that combine real-world, diverse requirements with verified specifications and
execution traces. Currently, we are curating a small seed set from open-source safety-critical software,
supplemented with synthetic examples to cover edge cases. While synthetic data is useful, it lacks the
nuances of industrial requirements, so mixed datasets appear most promising. VERIFYAI’s prototype
handles single-module programs well, but multi-module systems pose memory and latency challenges.
To manage complexity, we plan to employ hierarchical specification synthesis, verifying each module
independently prior to integration. Additionally, we aim to release an annotated subset of the dataset to
support transparency and reproducibility.


5. Conclusions
This paper identifies clear and concise challenges and prospects in leveraging LLMs for formal software
requirements, based on our initial anaysis of the literature. Semantic ambiguity, lack of ground truth
data, tool interoperability, lifecycle traceability, and explainability all present significant barriers to full
automation. However, each challenge also points to fertile ground for innovation. Future directions
such as human-in-the-loop systems, multi-modal alignment, standardised benchmarks, neuro-symbolic
reasoning, and interactive traceability tools offer practical and scalable paths forward. As a final remark,
we can say that as AI and formal methods continue to converge, interdisciplinary collaboration will be
key to bridging the gaps and turning conceptual advances into robust, real-world solutions.


6. Acknowledgements
This work is partly funded by the ADAPT Research Centre for AI-Driven Digital Content Technology,
which is funded by Research Ireland through the Research Ireland Centres Programme and is co funded
under the European Regional Development Fund (ERDF) through Grant 13/RC/2106 P2. The submission
aligns with Digital Content Transformation (DCT) thread of the ADAPT research centre.


References
 [1] M. Huisman, D. Gurov, A. Malkis, Formal methods: From academia to industrial practice. a travel
     guide, 2024. URL: https://arxiv.org/abs/2002.07279. arXiv:2002.07279.
 [2] A. Beg, D. O’Donoghue, R. Monahan, Formalising software requirements using large language
     models (2025). URL: https://arxiv.org/abs/2506.10704. arXiv:2506.10704.
 [3] G. Granberry, W. Ahrendt, M. Johansson, Specify what? enhancing neural specification synthesis
     by symbolic methods, in: N. Kosmatov, L. Kovács (Eds.), Integrated Formal Methods, Springer
     Nature Switzerland, Cham, 2025, pp. 307–325.
 [4] V. Robles, N. Kosmatov, V. Prevosto, P. Le Gall, High-level program properties in frama-c:
     Definition, verification and deduction, in: Leveraging Applications of Formal Methods, Veri-
     fication and Validation. Specification and Verification: 12th International Symposium, ISoLA
     2024, Crete, Greece, October 27–31, 2024, Proceedings, Part III, Springer-Verlag, Berlin, Hei-
     delberg, 2024, p. 159–177. URL: https://doi.org/10.1007/978-3-031-75380-0_10. doi:10.1007/
     978-3-031-75380-0_10.
 [5] J. O. Couder, D. Gomez, O. Ochoa, Requirements verification through the analysis of source
     code by large language models, in: SoutheastCon 2024, 2024, pp. 75–80. doi:10.1109/
     SoutheastCon52093.2024.10500073.
 [6] X. Quan, M. Valentino, L. A. Dennis, A. Freitas, Verification and refinement of natural language
     explanations through llm-symbolic theorem proving, 2024. URL: https://arxiv.org/abs/2405.01379.
     arXiv:2405.01379.
 [7] W. Fan, M. Rego, X. Hu, S. Dod, Z. Ni, D. Xie, J. DiVincenzo, L. Tan, Evaluating the ability of
     large language models to generate verifiable specifications in verifast, 2025. URL: https://arxiv.org/
     abs/2411.02318. arXiv:2411.02318.
 [8] M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, C. Trippel, nl2spec: Interactively translating un-
     structured natural language to temporal logics with large language models, 2023. URL: https:
     //arxiv.org/abs/2303.04864. arXiv:2303.04864.
 [9] S. Mandal, A. Chethan, V. Janfaza, S. M. F. Mahmud, T. A. Anderson, J. Turek, J. J. Tithi,
     A. Muzahid, Large language models based automatic synthesis of software specifications, 2023.
     URL: https://arxiv.org/abs/2304.09181. arXiv:2304.09181.
[10] A. Nayak, H. P. Timmapathini, V. Murali, K. Ponnalagu, V. G. Venkoparao, A. Post, Req2spec:
     Transforming software requirements into formal specifications using natural language processing,
     in: Requirements Engineering: Foundation for Software Quality: 28th International Working
     Conference, REFSQ 2022, Birmingham, UK, March 21–24, 2022, Proceedings, Springer-Verlag,
     Berlin, Heidelberg, 2022, p. 87–95.
[11] L. Ma, S. Liu, Y. Li, X. Xie, L. Bu, Specgen: Automated generation of formal program specifications
     via large language models (2024). URL: https://arxiv.org/abs/2401.08807. arXiv:2401.08807.
[12] W. Fang, M. Li, M. Li, Z. Yan, S. Liu, H. Zhang, Z. Xie, Assertllm: Generating hardware verification
     assertions from design specifications via multi-llms, in: 2024 IEEE LLM Aided Design Workshop
     (LAD), 2024, pp. 1–1. doi:10.1109/LAD62341.2024.10691792.
[13] M. Li, W. Fang, Q. Zhang, Z. Xie, Specllm: Exploring generation and review of vlsi de-
     sign specification with large language model, 2024. URL: https://arxiv.org/abs/2401.13266.
     arXiv:2401.13266.
[14] L. M. Reinpold, M. Schieseck, L. P. Wagner, F. Gehlhoff, A. Fay, Exploring llms for verifying
     technical system specifications against requirements, 2024. URL: https://arxiv.org/abs/2411.11582.
     arXiv:2411.11582.
[15] V. Gervasi, B. Nuseibeh, Lightweight validation of natural language requirements, Softw. Pract.
     Exper. 32 (2002) 113–133. URL: https://doi.org/10.1002/spe.430. doi:10.1002/spe.430.
[16] Y. Xu, J. Feng, W. Miao, Learning from failures: Translation of natural language requirements into
     linear temporal logic with large language models, in: 2024 IEEE 24th International Conference on
     Software Quality, Reliability and Security (QRS), 2024, pp. 204–215. doi:10.1109/QRS62785.
     2024.00029.
[17] I. T. Leong, R. Barbosa, Translating natural language requirements to formal specifications: A study
     on gpt and symbolic nlp, in: 2023 53rd Annual IEEE/IFIP International Conference on Dependable
     Systems and Networks Workshops (DSN-W), 2023, pp. 259–262. doi:10.1109/DSN-W58399.
     2023.00065.
[18] W. Nowakowski, M. Śmiałek, A. Ambroziewicz, T. Straszak, Requirements-level language and
     tools for capturing software system essence, Computer Science and Information Systems 10 (2013)
     1499–1524.
[19] S. Ghosh, D. Elenius, W. Li, P. Lincoln, N. Shankar, W. Steiner, Arsenal: Automatic requirements
     specification extraction from natural language, in: S. Rayadurgam, O. Tkachuk (Eds.), NASA
     Formal Methods, Springer International Publishing, Cham, 2016, pp. 41–46.
[20] S. J. Greenspan, A. Borgida, J. Mylopoulos, A requirements modeling language and its logic,
     Information Systems 11 (1986) 9–23. URL: https://www.sciencedirect.com/science/article/pii/
     0306437986900207. doi:https://doi.org/10.1016/0306-4379(86)90020-7.
[21] M. Fazelnia, M. Mirakhorli, H. Bagheri, Translation titans, reasoning challenges: Satisfiability-aided
     language models for detecting conflicting requirements, in: Proceedings of the 39th IEEE/ACM
     International Conference on Automated Software Engineering, ASE ’24, Association for Computing
     Machinery, New York, NY, USA, 2024, p. 2294–2298. URL: https://doi.org/10.1145/3691620.
     3695302. doi:10.1145/3691620.3695302.
[22] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, A. Anandkumar,
     Leandojo: Theorem proving with retrieval-augmented language models, in: A. Oh, T. Naumann,
     A. Globerson, K. Saenko, M. Hardt, S. Levine (Eds.), Advances in Neural Information Processing
     Systems, volume 36, Curran Associates, Inc., 2023, pp. 21573–21612.
[23] A. Q. Jiang, W. Li, S. Tworkowski, K. Czechowski, T. Odrzygóźdź, P. Mił oś, Y. Wu, M. Jam-
     nik, Thor: Wielding hammers to integrate language models and automated theorem provers, in:
     S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural
     Information Processing Systems, volume 35, Curran Associates, Inc., 2022, pp. 8360–8373.
[24] G. Granberry, W. Ahrendt, M. Johansson, Towards integrating copiloting and formal methods,
     in: T. Margaria, B. Steffen (Eds.), Leveraging Applications of Formal Methods, Verification and
     Validation. Specification and Verification, Springer Nature Switzerland, Cham, 2025, pp. 144–158.
[25] E. Mugnier, E. A. Gonzalez, R. Jhala, N. Polikarpova, Y. Zhou, Laurel: Generating
     dafny assertions using large language models, 2024. URL: https://arxiv.org/abs/2405.16792.
     arXiv:2405.16792.
[26] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, Y. Iwasawa, Large language models are zero-shot reasoners,
     in: S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural
     Information Processing Systems, volume 35, Curran Associates, Inc., 2022, pp. 22199–22213.
[27] Y. Li, B. Hui, X. Xia, J. Yang, M. Yang, L. Zhang, S. Si, L.-H. Chen, J. Liu, T. Liu, F. Huang,
     Y. Li, One-shot learning as instruction data prospector for large language models (2024). URL:
     https://arxiv.org/abs/2312.10302. arXiv:2312.10302.
[28] H. Zhang, M. Cai, X. Zhang, C. J. Zhang, R. Mao, K. Wu, Self-convinced prompting: Few-shot
     question answering with repeated introspection (2023). URL: https://arxiv.org/abs/2310.05035.
     arXiv:2310.05035.
[29] J. Wei, X. Wang, D. Schuurmans, M. Bosma, b. ichter, F. Xia, E. Chi, Q. V. Le, D. Zhou, Chain-
     of-thought prompting elicits reasoning in large language models, in: S. Koyejo, S. Mohamed,
     A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural Information Processing
     Systems, volume 35, Curran Associates, Inc., 2022, pp. 24824–24837.
[30] J. Li, G. Li, Y. Li, Z. Jin, Structured chain-of-thought prompting for code generation, ACM
     Trans. Softw. Eng. Methodol. 34 (2025). URL: https://doi.org/10.1145/3690635. doi:10.1145/
     3690635.
[31] C. Hsieh, Y. Chuang, C. Li, Z. Wang, L. T. Le, A. Kumar, J. R. Glass, A. Ratner, C. Lee, R. Krishna,
     T. Pfister, Found in the middle: Calibrating positional attention bias improves long context
     utilization, in: L. Ku, A. Martins, V. Srikumar (Eds.), Findings of the Association for Computational
     Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, Association
     for Computational Linguistics, 2024, pp. 14982–14995. URL: https://doi.org/10.18653/v1/2024.
     findings-acl.890. doi:10.18653/V1/2024.FINDINGS-ACL.890.
[32] X. Ye, G. Durrett, The unreliability of explanations in few-shot prompting for textual reasoning,
     in: S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural
     Information Processing Systems, volume 35, Curran Associates, Inc., 2022, pp. 30378–30392.
[33] K. Shum, S. Diao, T. Zhang, Automatic prompt augmentation and selection with chain-of-thought
     from labeled data, in: H. Bouamor, J. Pino, K. Bali (Eds.), Findings of the Association for Computa-
     tional Linguistics: EMNLP 2023, Singapore, December 6-10, 2023, Association for Computational
     Linguistics, 2023, pp. 12113–12139. URL: https://doi.org/10.18653/v1/2023.findings-emnlp.811.
     doi:10.18653/V1/2023.FINDINGS-EMNLP.811.
[34] W. Xu, A. Banburski-Fahey, N. Jojic, Reprompting: Automated chain-of-thought prompt inference
     through gibbs sampling, CoRR abs/2305.09993 (2023). URL: https://doi.org/10.48550/arXiv.2305.
     09993. doi:10.48550/ARXIV.2305.09993. arXiv:2305.09993.
[35] M. Besta, F. Memedi, Z. Zhang, R. Gerstenberger, N. Blach, P. Nyczyk, M. Copik,
     G. Kwasniewski, J. Müller, L. Gianinazzi, A. Kubicek, H. Niewiadomski, O. Mutlu,
     T. Hoefler, Topologies of reasoning: Demystifying chains, trees, and graphs of thoughts,
     CoRR abs/2401.14295 (2024). URL: https://doi.org/10.48550/arXiv.2401.14295. doi:10.48550/
     arXiv.2401.14295. arXiv:2401.14295.
[36] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih,
     T. Rocktäschel, S. Riedel, D. Kiela, Retrieval-augmented generation for knowledge-intensive NLP
     tasks, in: H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, H. Lin (Eds.), Advances in Neural
     Information Processing Systems 33: Annual Conference on Neural Information Processing Systems
     2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020. URL: https://proceedings.neurips.cc/
     paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html.
[37] P. Sahoo, A. K. Singh, S. Saha, V. Jain, S. Mondal, A. Chadha, A systematic survey of prompt
     engineering in large language models: Techniques and applications (2025). URL: https://arxiv.org/
     abs/2402.07927. arXiv:2402.07927.
[38] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, Lora: Low-
     rank adaptation of large language models, in: The Tenth International Conference on Learning
     Representations, ICLR 2022, Virtual Event, April 25-29, 2022, OpenReview.net, 2022. URL:
     https://openreview.net/forum?id=nZeVKeeFYf9.
[39] K. R. M. Leino, Dafny: An automatic program verifier for functional correctness, in: Proceedings of
     the 16th International Conference on Logic for Programming, Artificial Intelligence, and Reasoning
     (LPAR), volume 6355 of Lecture Notes in Computer Science, Springer, 2010, pp. 348–370. URL:
     https://doi.org/10.1007/978-3-642-17511-4_20. doi:10.1007/978-3-642-17511-4\_20.
[40] D. R. Cok, Openjml: Software verification for java 7 using jml, openjdk, and eclipse, in:
     NASA Formal Methods (NFM 2011), volume 6617 of Lecture Notes in Computer Science,
     Springer, 2011, pp. 472–479. URL: https://doi.org/10.1007/978-3-642-20398-5_35. doi:10.1007/
     978-3-642-20398-5\_35.
[41] M. R. H. Misu, C. V. Lopes, I. Ma, J. Noble, Towards ai-assisted synthesis of verified dafny
     methods, Proc. ACM Softw. Eng. 1 (2024). URL: https://doi.org/10.1145/3643763. doi:10.1145/
     3643763.
[42] J. Yao, Y. Liu, Z. Dong, M. Guo, H. Hu, K. Keutzer, L. Du, D. Zhou, S. Zhang, Promptcot: Align
     prompt distribution via adapted chain-of-thought, in: 2024 IEEE/CVF Conference on Computer Vi-
     sion and Pattern Recognition (CVPR), 2024, pp. 7027–7037. doi:10.1109/CVPR52733.2024.
     00671.
[43] A. Porshnev, et al., Modelling implicit bias in gender–career associations: A systematic comparison
     of language models, PsyArXiv (2025). doi:10.31234/osf.io/p7hvw\_v1, preprint, 22 May
     2025.
[44] T. Tahir, H. Jahankhani, K. Tasleem, B. Hassan, Cross-project multiclass classification of ears-
     based functional requirements utilizing natural language processing, machine learning, and deep
     learning, Systems 13 (2025). URL: https://www.mdpi.com/2079-8954/13/7/567. doi:10.3390/
     systems13070567.
[45] K. Gregory, A dataset describing data discovery and reuse practices in research, Sci-
     entific Data 7 (2020) 232. URL: https://doi.org/10.1038/s41597-020-0569-5. doi:10.1038/
     s41597-020-0569-5.
[46] G. Boetticher, T. Menzies, T. Ostrand, {PROMISE} repository of empirical software engineering
     data (2007).
[47] J. H. Hayes, J. Payne, A. Dekhtyar, The requirements tracing on target (retro).net dataset (2018).
     URL: https://arxiv.org/abs/1807.11344. arXiv:1807.11344.
A. Work in progress and initial experiment setup
As initial experiment setup, we re-simulated the methodology presented in [3] by applying it to TriType.c
program, which was selected from the online interface of the PathCrawler tool available in the Frama-C
ecosystem. The program was analysed using the original workflow – combining Large Language Models
(LLMs) with symbolic outputs from PathCrawler and EVA – to generate ACSL specifications. The use of
PathCrawler provided concrete path-based input/output examples that guided the LLM toward generating
more context-relevant and semantically aligned annotations. Figure 2 shows the output of the Pathcrawler
tool. Our plan is to conduct experiments with simple and complex programs, representing a diverse set
of procedural constructs and control flows, allowing us to evaluate the methodology across a realistic
and varied set of inputs. A repository of related resources is available at https://github.com/arshadbeg/
OVERLAY2025_SupportingDocs.git.




Figure 2: Output of the Pathcrawler for TriType Example



Analysis of Tritype Example
Note: We used OpenAI’s ChatGPT-4o to assist in generating descriptive analysis text based on the output
of the PathCrawler tool. All generated content was reviewed and verified by the authors. The function
Tritype is:
/* Should return the type of the triangle
   which has sides of these lengths.
   3 = not a triangle
   2 = equilateral triangle
   1 = isoceles triangle
   0 = other triangle
*/
int Tritype(double i, double j, double k){
  int trityp = 0;
  if (i < 0.0 || j < 0.0 || k < 0.0)          // line 10
    return 3;
  if (i + j <= k || j + k <= i || k + i <= j) // line 12
    return 3;
  if (i == j) trityp = trityp + 1;            // line 14
  if (i == k) trityp = trityp + 1;            // line 15
  if (j == k) trityp = trityp + 1;            // line 16
  if (trityp >= 2)                            // line 17
      trityp = 2;
  return trityp;
}


   PathCrawler successfully instrumented and analysed the Tritype function using the all-path coverage
criterion. While 100% branch coverage was achieved, none of the 11 generated test cases were categorised
as successful or failed, leaving all as "unknown." This implies that the tool executed all branches in the
code, yet could not conclusively determine the verdict for any specific path, possibly due to incomplete
post-condition specifications or ambiguity in return value interpretation. The test harness was properly
compiled, and the environment was initialised and cleaned up, suggesting that the tool functioned without
interruptions. However, the presence of infeasible paths (8 of 19) emphasises the complexity of the
control flow. The inability to evaluate paths conclusively indicates a need to refine input constraints or
further investigate symbolic execution limitations. Ultimately, this dataset offers deep insights into path
feasibility without final verdict certainty.
   The test generation summary reveals a comprehensive attempt by PathCrawler to traverse 19 total paths
within the Tritype function. Of these, 11 were covered and 8 marked as infeasible. The success of
achieving 100% branch coverage suggests an effective instrumentation and exploration of all conditional
branches in the function. However, none of the generated test cases resulted in a definitive "success"
or "failure" outcome, indicating that path postconditions or functional assertions may not have been
defined or interpreted robustly enough for classification. The discrepancy between path coverage and
test verdicts signals potential limitations in either the underlying test oracle or symbolic constraint
solving. Nevertheless, all test cases completed without runtime errors or crashes, which strengthens the
confidence in static path feasibility. This situation is common in symbolic execution where certain paths
are executable in theory but do not yield assertable functional correctness outcomes.
   Several test cases (such as 3, 4, and 7) represent crucial boundary classifications in triangle identification
logic. Test Case 3, returning 0, indicates that the input values do not form a valid triangle—corroborated
by the path predicate involving non-equal sides and valid sum conditions. Test Cases 4 to 7 exhibit values
returning 1 or 2, which correspond to isosceles and equilateral triangle scenarios. These variations affirm
the tool’s capability to explore distinct triangle classifications based on the input side lengths. However,
all cases have an "unknown" verdict. This suggests that while execution paths were valid, postconditions
or specification assertions did not yield sufficient evidence for a conclusive outcome. It is also possible
that comparison thresholds or floating-point equality checks introduced uncertainty. The tool’s symbolic
reasoning did cover a wide input range, showcasing strength in data diversity.
   This selection emphasises the diversity in input ranges—both positive and negative, and also includes
floating-point values. Negative and invalid inputs, such as in Case 1, correctly trace to a return of 3,
denoting an error or invalid triangle. Equilateral triangles like in Case 7 return 2, consistent with the
expected logic. The presence of precise floating values (e.g., 886.99) highlights the need for robust type
handling in symbolic execution and comparison logic. The return values indicate that, functionally, the
outputs align with expectations, even if PathCrawler’s analysis labels the verdict as unknown.
   Examining the path predicates reveals detailed symbolic constraints applied during test generation.
For example, Case 3 checks all triangle inequality constraints and non-equality of sides. Case 7’s
predicate confirms all sides are equal, ideal for verifying the equilateral branch of logic. These conditions
provide assurance that symbolic execution adheres to logical expectations derived from triangle properties.
However, predicates like those in Cases 1, 10, and 11 reflect invalid or boundary-breaking inputs—some
involving negative sides. While such inputs yield predictable output values, their classification remains
"unknown" due to a lack of explicit functional assertions. The predicates affirm that PathCrawler applies
comprehensive constraint exploration but might benefit from clearer postcondition verification to move
cases from “unknown” to “success” or “failure.”
   The analysis indicates high internal code coverage but limited external verdict classification due to
insufficient assertions or postcondition specifications. While symbolic execution succeeded in evaluating
feasible and infeasible paths and fully traversing conditional logic, the lack of verdicts suggests an
improvement opportunity in integrating output expectations with test oracles. PathCrawler’s utility in this
context lies more in code path analysis and constraint checking than in final correctness validation. Future
work may involve explicitly encoding expected behavior (e.g., via assertion annotations or return value
comparisons) to convert "unknown" results into definitive outcomes. Despite these limitations, the tool
has proven its capability in surfacing hidden paths and exercising diverse execution flows. Particularly in
legacy or critical systems like Tritype, such analysis can prevent unanticipated bugs or logic flaws
through exhaustive test path enumeration.


Analysis of Verification on baseline_Example1-Tritype.c
The baseline prompt is available on page 20-21, [3].                                The verification of
baseline_Example1-Tritype.c using Frama-C and four SMT solvers (Alt-Ergo, Z3,
CVC4, and CVC5) revealed a consistent pattern. With minimal ACSL specification, only two implicit
verification goals—termination and unreachability—were generated and successfully verified by all four
provers. This indicates that the function is syntactically well-formed and does not exhibit trivial issues
like infinite loops or unreachable code paths. However, due to the absence of user-defined postconditions
or preconditions, the analysis provides limited insight into functional correctness. The warning about
the missing assigns clause suggests that memory side-effects are not specified, potentially causing
inaccurate assumptions for callers. Similarly, the absence of RTE (Run-Time Error) guards indicates
that common runtime errors like overflows or division by zero are not being verified. While the results
demonstrate soundness at a structural level, the lack of deep specification significantly limits the utility of
the verification. All provers perform equally under these trivial conditions.


Comparison of Prover Results on
baseline_Example1-Tritype.c

Table 2
Prover Results for baseline_Example1-Tritype.c
                       Prover      Total Goals     Proved              Notes
                       Alt-Ergo         2             2       All default goals proved
                       Z3               2             2       All default goals proved
                       CVC4             2             2       All default goals proved
                       CVC5             2             2       All default goals proved



Analysis of Verification on pathcrawler_augmented_Example1-Tritype.c
The pathcrawler augmented prompt is available on page 21-22, [3] while EVA augmented prompt is
available on page 24, [3]. The pathcrawler_augmented_Example1-Tritype.c file, enriched
with detailed ACSL annotations, exhibits significantly different verification behavior. A total of 20
goals were generated, including 18 based on user-specified preconditions and postconditions, plus
the standard termination and unreachability checks. The analysis reveals a distinct divide in prover
effectiveness. While all provers verified termination and basic logic, their ability to handle complex
ensures clauses varied. Z3 and CVC5 each failed to prove seven goals—Z3 due to timeouts and CVC4
due to unknown statuses—highlighting their struggles with intricate logical paths and case distinctions.
Alt-Ergo and CVC5 fared slightly better, with only five unverified goals each. Notably, the most complex
properties, such as correct classification of triangle types (Scalene, Isosceles, Equilateral) and handling of
inequality rules, were consistently problematic across all provers. This reflects the challenges solvers
face when dealing with disjunction-heavy logic or subtle arithmetic constraints embedded in functional
specifications.

Comparison of Prover Results on pathcrawler_augmented_Example1-Tritype.c

Table 3
Prover Results for pathcrawler_augmented_Example1-Tritype.c
                          Prover       Total Goals          Proved    Failed Type      Failed Count
                          Z3                 20               13       Timeout               7
                          Alt-Ergo           20               15       Timeout               5
                          CVC4               20               13       Unknown               7
                          CVC5               20               15       Timeout               5




B. Performance of provers on 36 Examples of Frama-C Tutorial
RTE Tool Output Summary

  C File                             Goals    Proved          Qed    Timeout   Term.   Unreach.   Alt-   Assigns
                                                                                                  Ergo   Missing
  01-abs-0.c                           1           2/3         0       1         1       1         0      Yes
  01-abs-1.c                           2           3/4         1       1         1       1         0      Yes
  01-abs-2.c                           4           6/6         4       0         1       1         0      No
  01-abs-3.c                           5           7/7         5       0         1       1         0      No
  02-max-0.c                          2            4/4        2        0         1       1         0      Yes
  02-max-1.c                          5            5/7        3        2         1       1         0      Yes
  02-max-2.c                          1            3/3        0        0         1       1         1      Yes
  02-max-3.c                          6            7/8        4        1         1       1         1      Yes
  02-max-4.c                          8           10 / 10     7        0         1       1         1      Yes
  03-max_ptr-0.c                      4            4/6        2        2         1       1         0      Yes
  03-max_ptr-1.c                      6            6/8        4        2         1       1         0      Yes
  03-max_ptr-2.c                      6            8/8        4        0         1       1         2      Yes
  03-max_ptr-3.c                      4            6/6        3        0         1       1         1      Yes
  03-max_ptr-4.c                      8           10 / 10     6        0         1       1         2      No
  04-incr_a_by_b-0.c                   5           3/7         0       4         1       1         1      Yes
  04-incr_a_by_b-1.c                   7           9/9         4       0         1       1         3      No
  04-incr_a_by_b-fail.c                7           8/9         4       1         1       1         2      No
  04-swap-0.c                          6           4/8         2       4         1       1         0      Yes
  04-swap-1.c                         12          14 / 14      9       0         1       1         3      Yes
  05-abs-0.c                           1           2/3         0       1         1       1         0      Yes
  05-abs-1.c                           7           9/9         7       0         1       1         0      No
  05-abs-2.c                           6           8/8         6       0         1       1         0      No
  06-max_abs-0.c                       2           2/2         2       0         –       –         0      Yes
  06-max_abs-1.c                      13          11 / 13      9       2         –       –         2      Yes
  06-max_abs-2.c                      13          12 / 13     11       1         –       –         1      Yes
 C File                  Goals   Proved    Qed   Timeout   Term.   Unreach.   Alt-   Assigns
                                                                              Ergo   Missing
 06-max_abs-3.c           13     13 / 13   11      0         –       –          2     Yes
 07-reset_array-0.c        3      2/4       1      2         –       1          0     Yes
 07-reset_array-1.c       13     15 / 15    9      0         1       1          4     No
 08-binary_search-1.c     27     29 / 29   13      0         1       1         14     No
 09-sqrt-0.c               6      4/7       2      3         –       1          1     Yes


Z3 Prover Output Summary

 C File                  Goals   Proved    Qed   Timeout   Term.   Unreach.    Z3    Assigns
                                                                                     Missing
 01-abs-0.c                0      2/2       1      1         0       0         0      Yes
 01-abs-1.c                1      3/3       1      1         1       0         0      Yes
 01-abs-2.c                3      5/5       1      1         3       0         0      No
 01-abs-3.c                4      6/6       1      1         4       0         0      No
 02-max-0.c               2       4/4       1      1        2        0         0      Yes
 02-max-1.c               5       5/7       1      1        3        0         2      Yes
 02-max-2.c               1       3/3       1      1        0        1         0      Yes
 02-max-3.c               6       7/8       1      1        4        1         1      Yes
 02-max-4.c               8      10 / 10    1      1        7        1         0      Yes
 03-max_ptr-0.c           0       2/2       1      1        0        0         0      Yes
 03-max_ptr-1.c           2       4/4       1      1        2        0         0      Yes
 03-max_ptr-2.c           2       4/4       1      1        2        0         0      Yes
 03-max_ptr-3.c           2       4/4       1      1        1        1         0      Yes
 03-max_ptr-4.c           4       6/6       1      1        4        0         0      No
 04-incr_a_by_b-0.c        0      2/2       1      1         0       0         0      Yes
 04-incr_a_by_b-1.c        2      4/4       1      1         1       1         0      No
 04-incr_a_by_b-fail.c     2      3/4       1      1         1       0         1      No
 04-swap-0.c               2      4/4       1      1         2       0         0      Yes
 04-swap-1.c               8     10 / 10    1      1         7       1         0      Yes
 05-abs-0.c                0      2/2       1      1         0       0         0      Yes
 05-abs-1.c                6      8/8       1      1         6       0         0      No
 05-abs-2.c                5      7/7       1      1         5       0         0      No
 06-max_abs-0.c            2      2/2       0      0         2       0         0      Yes
 06-max_abs-1.c           13     11 / 13    0      0         9       2         2      No
 06-max_abs-2.c           13     12 / 13    0      0        11       1         1      No
 06-max_abs-3.c           13     13 / 13    0      0        11       2         0      No
 07-reset_array-0.c        1      1/2       0      1         0       0         1      Yes
 07-reset_array-1.c       11     13 / 13    1      1         8       3         0      No
 08-binary_search-1.c     18     18 / 20    1      1        11       5         2      No


CVC4 Prover Output Summary

 C File                  Goals   Proved    Qed   Timeout   Term.   Unreach.   CVC4   Assigns
                                                                                     Missing
 01-abs-0.c               0       2/2       1      1         0       0         0      Yes
 01-abs-1.c               1       3/3       1      1         1       0         0      Yes
 01-abs-2.c               3       5/5       1      1         3       0         0      No
 01-abs-3.c               4       6/6       1      1         4       0         0      No
 02-max-0.c               2       4/4       1      1         2       0         0      Yes
 02-max-1.c               5       5/7       1      1         3       0         2      Yes
 02-max-2.c               1       3/3       1      1         0       1         0      Yes
 02-max-3.c               6       7/8       1      1         4       1         1      Yes
 02-max-4.c               8      10 / 10    1      1         7       1         0      Yes
 03-max_ptr-0.c           0       2/2       1      1         0       0         0      Yes
 03-max_ptr-1.c           2       4/4       1      1         2       0         0      Yes
 C File                  Goals   Proved    Qed   Timeout   Term.   Unreach.   CVC4   Assigns
                                                                                     Missing
 03-max_ptr-2.c           2       4/4       1      1        2        0         0      Yes
 03-max_ptr-3.c           2       4/4       1      1        1        1         0      Yes
 03-max_ptr-4.c           4       6/6       1      1        4        0         0      No
 04-incr_a_by_b-0.c        0      2/2       1      1         0       0         0      Yes
 04-incr_a_by_b-1.c        2      4/4       1      1         1       1         0      No
 04-incr_a_by_b-fail.c     2      3/4       1      1         1       0         1      No
 04-swap-0.c               2      4/4       1      1         2       0         0      Yes
 04-swap-1.c               8     10 / 10    1      1         7       1         0      Yes
 05-abs-0.c                0      2/2       1      1         0       0         0      Yes
 05-abs-1.c                6      8/8       1      1         6       0         0      No
 05-abs-2.c                5      7/7       1      1         5       0         0      No
 06-max_abs-0.c            2      2/2       0      0         2       0         0      Yes
 06-max_abs-1.c           13     11 / 13    0      0         9       2         2      No
 06-max_abs-2.c           13     12 / 13    0      0        11       1         1      No
 06-max_abs-3.c           13     13 / 13    0      0        11       2         0      No
 07-reset_array-0.c        1      1/2       0      1         0       0         1      Yes
 07-reset_array-1.c       11     13 / 13    1      1         8       3         0      No
 08-binary_search-1.c     18     16 / 20    1      1        11       3         4      No


CVC5 Prover Output Summary

 C File                  Goals   Proved    Qed   Timeout   Term.   Unreach.   CVC5   Assigns
                                                                                     Missing
 01-abs-0.c                0      2/2       1      1         0       0         0      Yes
 01-abs-1.c                1      3/3       1      1         1       0         0      Yes
 01-abs-2.c                3      5/5       1      1         3       0         0      No
 01-abs-3.c                4      6/6       1      1         4       0         0      No
 02-max-0.c               2       4/4       1      1        2        0         0      Yes
 02-max-1.c               5       5/7       1      1        3        0         2      Yes
 02-max-2.c               1       3/3       1      1        0        1         0      Yes
 02-max-3.c               6       7/8       1      1        4        1         1      Yes
 02-max-4.c               8      10 / 10    1      1        7        1         0      Yes
 03-max_ptr-0.c           0       2/2       1      1        0        0         0      Yes
 03-max_ptr-1.c           2       4/4       1      1        2        0         0      Yes
 03-max_ptr-2.c           2       4/4       1      1        2        0         0      Yes
 03-max_ptr-3.c           2       4/4       1      1        1        1         0      Yes
 03-max_ptr-4.c           4       6/6       1      1        4        0         0      No
 04-incr_a_by_b-0.c        0      2/2       1      1         0       0         0      Yes
 04-incr_a_by_b-1.c        2      4/4       1      1         1       1         0      No
 04-incr_a_by_b-fail.c     2      3/4       1      1         1       0         1      No
 04-swap-0.c               2      4/4       1      1         2       0         0      Yes
 04-swap-1.c               8     10 / 10    1      1         7       1         0      Yes
 05-abs-0.c                0      2/2       1      1         0       0         0      Yes
 05-abs-1.c                6      8/8       1      1         6       0         0      No
 05-abs-2.c                5      7/7       1      1         5       0         0      No
 06-max_abs-0.c            2      2/2       0      0         2       0         0      Yes
 06-max_abs-1.c           13     11 / 13    0      0         9       2         2      No
 06-max_abs-2.c           13     12 / 13    0      0        11       1         1      No
 06-max_abs-3.c           13     13 / 13    0      0        11       2         0      No
 07-reset_array-0.c        1      1/2       0      1         0       0         1      Yes
 07-reset_array-1.c       11     13 / 13    1      1         8       3         0      No
 08-binary_search-1.c     18     16 / 20    1      1        11       3         4      No


Execution Times
   File Name                    Alt-ergo Time(s)   Z3 Time(s)     CVC4 Time(s)      CVC5 Time(s)
   01-abs-0.c                         0.01            0.02            0.02               0.01
   01-abs-1.c                         0.02            0.04            0.02              0.001
   01-abs-2.c                         0.05            0.06            0.05              0.003
   01-abs-3.c                         0.04            0.03            0.03              0.004
   02-max-0.c                         0.02            0.02            0.01              0.002
   02-max-1.c                         0.07            0.06            0.05              0.004
   02-max-2.c                         0.08            0.07            0.05              0.002
   02-max-3.c                         0.12            0.14            0.13              0.004
   02-max-4.c                         0.05            0.06            0.05              0.007
   03-max_ptr-0.c                     0.02            0.03            0.02              0.001
   03-max_ptr-1.c                     0.03            0.04            0.03              0.002
   03-max_ptr-2.c                     0.06            0.06            0.06              0.002
   03-max_ptr-3.c                     0.09            0.09            0.07              0.003
   03-max_ptr-4.c                     0.07            0.07            0.08              0.004
   04-incr_a_by_b-0.c                 0.03            0.04            0.04              0.002
   04-incr_a_by_b-1.c                 0.02            0.03            0.01              0.003
   04-incr_a_by_b-fail.c              0.03            0.04            0.04              0.002
   04-swap-0.c                        0.01            0.02            0.02              0.002
   04-swap-1.c                        0.04            0.05            0.03              0.004
   05-abs-0.c                         0.05            0.07            0.06              0.004
   05-abs-1.c                         0.07            0.08            0.07              0.006
   05-abs-2.c                         0.09            0.10            0.09              0.005
   06-max_abs-0.c                     0.03            0.04            0.03              0.002
   06-max_abs-1.c                     0.11            0.12            0.11              0.009
   06-max_abs-2.c                     0.14            0.15            0.14              0.011
   06-max_abs-3.c                     0.13            0.14            0.13              0.011
   07-reset_array-0.c                 0.02            0.03            0.02              0.002
   07-reset_array-1.c                 0.08            0.10            0.09              0.008
   08-binary_search-1.c               0.25            0.28            0.30              0.064

                   Table 8: Execution times of Alt-Ergo, Z3, CVC4 and CVC5 on C files




Figure 3: Graph of Execution Times of Alt-Ergo, Z3, CVC4 and CVC5
C. Description of Challenges and Future Directions
C1: Semantic Ambiguity in Natural Language - The ambiguity introduced in software requirements
through the use of natural language is evident. The context-dependent terms, implicit references, and
domain-specific jargon complicate accurate interpretation of requirements for automatic specification
generation. The use of LLMs helps address this challenge but mis-interpretation of user intent still leads
to incorrect outputs. Removing ambiguity requires structured domain knowledge aligned with external
ontologies. As the literature synthesis suggests, improved models and effective human-in-the- loop
strategies increase the accuracy in generating correct and verifiable specifications.
C2: Lack of Ground Truth Datasets - public datasets involving industry based software is difficult to
locate, arguably due to the sensitivity of software pieces and underlying IP rights. This scarcity of standard
datasets comprising of natural language requirements together with formal logic poses an obstacle in the
much required steps of model training, evaluation, and reproducibility (core components of achieving
better accuracy in mainstream NLP tasks). It also involves a scalability challenge. Advancing the field
requires high-quality, and annotated datasets that span varied industries and requirement types. The
synthesised datasets partially solve the problem. The availability of high- quality, curated and annotated
standardised formal specification datasets involving varied industries and requirement types would push
the boundary in this domain. These datasets should capture real-world software complexity and domain
diversity.
C3: Tool Interoperability - There is a significant interest in developing tool-chains to integrate formal
verification tools for verifying critical software from the last two decades. Formal verification process
rely on diverse tools with incompatible formats and limited integration capabilities, which makes end-
to-end automation difficult. The process of integrating formal verification tools involves manual or
semi-automatic intervention. The process becomes difficult in the absence of shared standards or modular
pipelines. Achieving seamless and low-effort tool interoperability requires standardised interfaces and
ontologies.
C4: Traceability Across Artefact Lifecycles - A typical software development life-cycle involves
multiple phases. Maintaining traceability and alignment throughout the development cycle is the core
requirement. Achieving traceability manually can compromise system integrity. Effective traceability
links rationale, changes and dependencies across software artefacts i.e. text, models, code, and tests.
LLMs can assist in impact analysis to maintain traceability, but imposes a challenge of collaborative,
explainable, and context-aware evolution process.
C5: Explainability and User Trust - For LLM-generated formal specifications to be trusted, users
must understand how outputs were derived and whether they reflect intended meaning. Current models
offer limited transparency, often lacking rationale or input attribution. Addressing this involves adding
annotations in the implementation and can potentially be resolved through use of LLMs. But LLM
generated annotations can be under-developed or involve quality check using a human-in-the-loop,
especially ensuring trust in safety-critical systems and impose the challenge of deploying inspection,
refinement, and human oversight.
F1: Human-in-the-loop Formalisation - In this approach, the formalisation is semi-automated and
guided by a domain expert. LLMs can assist in proposing logic, trace links, or suggest refinements which
can be approved or revised by the users. The process ensures less ambiguity, improved accuracy and
increased user trust. It enhances learning as well because improvement in model outputs is ensured
through interaction. This process can be facilitated by better visualisation, iteration, and feedback support.
This approach facilitates adopting new methodologies as human judgment remains central to critical
                 C1: Semantic Ambiguity                   F1: Human-in-the-loop Formalisation



                 C2: Lack of Ground Truth Datasets        F2: Multi-modal Artefact Alignment



                 C3: Tool Interoperability                F3: Standardised Benchmarks


                 C4: Traceability Across Artefact Life-
                                                          F4: Neuro-symbolic Reasoning
                 cycles



                 C5: Explainability and User Trust        F5: Interactive Traceability Tools


Figure 4: Mapping between challenges (C1 – C5) and future research (F1- F5) directions in LLM-based
formalisation


decisions.
F2: Multi-modal Artefact Alignment - Software requirements can be documented through a combina-
tion of raised through text, diagrams, tables, and spreedsheets, depending on the methodology adopted by
the developers. Alignment between these can reduce ambiguity and lead to better formal specifications.
Multi-modal support in the tools should be available and can be achieved through representation learning
and semantic matching. LLMs having structural and visual modalities can improve context interpretation,
resulting in more comprehensive models. Formalisation pipelines and redundant artefact types can model
real-world complexity, impacting the correctness and reliability of generated specifications.
F3: Standardised Benchmarks - The future direction of developing standardised benchmark has one-
to-one mapping to identified challenge C2. Having standardised benchmarks to simulate and compare
performance is a well-established research area e.g. [44, 45, 46, 47]. Advancing the field requires
high-quality, and annotated datasets that span varied industries and requirement types. Though the
synthesised datasets have partially solved the problem, the availability of high-quality and annotated
standardised formal specifications datasets remains limited. However, such datasets involving varied
industries and requirement types can push the boundary in this domain. These datasets should capture
real-world software complexity and domain diversity. As the field matures, such resources will become
an essential component for progress.
F4: Neuro-symbolic Reasoning - Neuro-symbolic systems combine the adaptability of LLMs with
the precision of symbolic reasoning. In these setups, neural networks suggest possible specifications
While logic-based tools check or refine them. This helps improve consistency, enforce constraints, and
verify correctness. Symbolic features like type rules or domain-specific logic can also guide the learning
process. While building such systems is complex, the hybrid method offers the potential of lowering
hallucinations and boosting clarity. Ongoing research could lead to reliable, interpretable models that
merge statistical learning with formal methods.
F5: Interactive Traceability Tools - Improving traceability of software requirements through interactive
user-friendly tools is a well-established area of requirements engineering. Traceability needs to be
built into the formalisation process from the start and interactive tools can link requirements to models,
tests, and verification results. This supports debugging, system updates, and audits. Features like
visual navigation, filtering, and tagging help teams track changes and spot dependencies. LLMs can
help by proposing trace links, flagging inconsistencies, or explaining revisions but users must stay in
control of key decisions. These tools should work within development environments and support team
collaboration. When traceability is clear and usable, it boosts system transparency and helps ensure
compliance—especially in regulated fields like aerospace and healthcare. Traceability tools like EARS,
FRET and DOORS are industry-proven. Industry-based case studies are a valuable avenue for future
work in this field.
