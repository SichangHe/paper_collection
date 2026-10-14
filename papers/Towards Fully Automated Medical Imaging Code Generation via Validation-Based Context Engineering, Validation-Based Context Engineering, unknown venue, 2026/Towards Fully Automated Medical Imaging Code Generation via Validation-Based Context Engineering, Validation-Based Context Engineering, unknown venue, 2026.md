                                         Towards Fully Automated Medical Imaging Code Generation via
                                                     Validation-Based Context Engineering
                                                             Zixiao Zhao                                                  Jing Sun                                       Zhe Hou
                                                       University of Auckland                                    University of Auckland                             Griffith University
                                                      Auckland, New Zealand                                      Auckland, New Zealand                              Brisbane, Australia
                                                    zixiao.zhao@auckland.ac.nz                                  jing.sun@auckland.ac.nz                           z.hou@griffith.edu.au

                                                          Cheng-Hao Cai                                                   Qian Liu                                     Mengze Li
                                                 Suzhou Industrial Park Monash                                   University of Auckland                         University of Auckland
                                                Research Institute of Science and                               Auckland, New Zealand                           Auckland, New Zealand
arXiv:2608.29016v1 [cs.CV] 29 Aug 2026




                                                          Technology                                            liu.qian@auckland.ac.nz                        mli840@aucklanduni.ac.nz
                                                         Suzhou, China
                                                  chenghao.cai.cs@gmail.com

                                                                                         Zijian Zhang∗                                     Jin Song Dong
                                                                              Beijing Institute of Technology                     National University of Singapore
                                                                                       Beijing, China                                  Singapore, Singapore
                                                                                  zhangzijian@bit.edu.cn                                dcsdjs@nus.edu.sg

                                         Abstract                                                                                CCS Concepts
                                         Large language models (LLMs) have demonstrated considerable                             • Software and its engineering → Automatic programming; •
                                         promise in program generation for small-scale and conventional ap-                      Computing methodologies → Multi-agent systems; • Applied
                                         plication development; however, they remain limited when applied                        computing → Health care information systems.
                                         to complex, domain-specific tasks such as medical image process-
                                         ing. General-purpose models lack explicit domain knowledge and                          Keywords
                                         robust validation mechanisms to ensure correctness, often requir-                       Automatic Programming, Large Language Models, Medical Imaging
                                         ing substantial human intervention to produce reliable processing
                                         pipelines. To address these limitations, we propose AutoMedImg, a                       ACM Reference Format:
                                                                                                                                 Zixiao Zhao, Jing Sun, Zhe Hou, Cheng-Hao Cai, Qian Liu, Mengze Li,
                                         multi-agent framework for fully automated medical image process-
                                                                                                                                 Zijian Zhang, and Jin Song Dong. 2026. Towards Fully Automated Medical
                                         ing code generation. AutoMedImg orchestrates specialised agents
                                                                                                                                 Imaging Code Generation via Validation-Based Context Engineering. In
                                         across two phases: a Planning Phase that performs dataset analy-                        Proceedings of the 41st IEEE/ACM International Conference on Automated
                                         sis and architecture design with semantic and formal verification,                      Software Engineering (ASE ’26), October 12–16, 2026, Munich, Germany. ACM,
                                         and a Coding Phase that generates modules in parallel with static                       New York, NY, USA, 13 pages. https://doi.org/10.1145/3832783.3834399
                                         checking, execution testing, and assembly validation. This multi-
                                         stage validation mitigates error propagation throughout genera-                         1    Introduction
                                         tion, while comprehensive auto-context engineering combining
                                         domain-specific knowledge bases, shared memory, and validation                          The emergence of large language models (LLMs) has revolutionised
                                         feedback automates context construction without manual prompt-                          the field of software engineering [14, 19, 21]. Trained on mas-
                                         ing. A cross-project adaptive pipeline synthesis mechanism further                      sive code datasets, LLMs show impressive capabilities in natu-
                                         accumulates validated pipelines and retrieves proven components                         ral language requirements comprehension [2], relevant codebases
                                         for new tasks based on project similarity, enhancing generation effi-                   search [26], reasoning on software structures [34], and demonstrat-
                                         ciency through cross-project learning. Extensive evaluation across                      ing substantial code generation capabilities [7]. On function-level
                                         six diverse and well-established medical imaging datasets with five                     code generation benchmarks such as HumanEval [5] and MBPP [3],
                                         backbone LLMs demonstrates that AutoMedImg achieves zero hu-                            state-of-the-art LLMs have achieved accuracy rates of 97.6% and
                                         man intervention , with Dice scores of up to 0.90 for segmentation                      92.7%, respectively [44, 48]. On SWE-bench [20], a benchmark on
                                         tasks and 99% accuracy for classification.                                              solving real-world Github repository issues, LLMs have achieved a
                                                                                                                                 76.8% resolution rate [45]. These results highlight the significant
                                         ∗ Corresponding author
                                                                                                                                 potential of LLMs in software engineering.
                                                                                                                                    However, these benchmarks only demonstrate the capability of
                                                                                                                                 LLM systems in small-scale code generation or code repair within
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   existing repositories. When generating complex code from scratch,
                                         ASE ’26, Munich, Germany                                                                current LLMs face significant limitations: (1) For complex prob-
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2882-2/2026/10                                                      lems, users must provide highly detailed prompts encompassing
                                         https://doi.org/10.1145/3832783.3834399                                                 all task-relevant background information to achieve satisfactory
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                      Zhao et al.


results [27]; (2) Due to the hallucination problem inherent in LLMs           construct and maintain generation context, enabling error
and the lack of effective validation mechanisms, human interven-              detection and correction without manual prompting.
tion remains necessary during code generation [43]; (3) Without           (2) We develop an adaptive pipeline synthesis mechanism
built-in validation mechanisms, LLMs cannot maintain consistent               that transfers validated medical imaging pipeline compo-
context and memory across code generation projects, even when                 nents across projects, enabling efficient knowledge reuse
successfully generating complete code [46]. Medical image process-            while maintaining pipeline quality.
ing code generation significantly exemplifies these challenges. Med-      (3) We present AutoMedImg, a multi-agent framework for fully
ical images exhibit complex properties with multimodal data (CT,              automated medical image processing code generation,
MRI), 2D/3D volumetric structures, various intensity ranges, and              evaluated on six diverse datasets, achieving zero human
specialised formats (NIfTI, DICOM) [28, 36], demanding domain                 intervention with competitive model performance.
expertise that significantly exceeds what can be conveyed through         The remainder of this paper is organised as follows: Section 2
manual prompting. Domain reliability requirements mean that hal-       reviews related work on automated code generation and medical
lucinated preprocessing steps or incorrect architectural choices are   imaging automation. Section 3 presents the AutoMedImg frame-
unacceptable, necessitating rigorous validation throughout genera-     work, detailing the multi-agent architecture, systematic validation
tion. Complete pipelines span multiple interdependent stages from      mechanisms, and validation-guided context engineering. Section 4
data loading through inference, while recurring patterns across        evaluates existing state-of-the-art code generation approaches on
projects demand cross-project knowledge retention that standard        medical image processing to identify their limitations, and demon-
LLMs cannot exploit. Automating this process would enable practi-      strates how AutoMedImg’s validation-based design addresses these
tioners lacking deep learning expertise to deploy validated medical    limitations across six medical imaging datasets with ablation studies.
imaging pipelines, broadening access to AI-assisted diagnostics.       Section 5 presents a qualitative comparison with medical imaging
Moreover, established benchmarking datasets with ground truth          automation methods and discusses threats to validity. Section 6
annotations and standardised metrics enable objective assessment       concludes with a summary and future research directions.
of generated pipelines. Together, these properties make medical
image processing both a practically impactful and methodologi-         2   Related Work
cally rigorous domain for evaluating automated code generation in
                                                                          Automated code generation with LLMs. LLM-based code gener-
complex, real-world settings.
                                                                       ation has evolved from early models like InCoder [10] and Code-
   Although several approaches attempt to tackle these challenges,
                                                                       Gen [38] to proprietary models such as GPT [39], Claude [1], and
they remain insufficient. Existing code generation frameworks or
                                                                       Gemini [8] achieving state-of-the-art performance on benchmarks
tools [11, 15, 47, 52] lack domain-specific knowledge integration
                                                                       like HumanEval [5] and MBPP [3]. Self-debugging frameworks [6]
and systematic validation mechanisms, making human intervention
                                                                       and execution-feedback methods [37] enable refinement based on
indispensable for specialised domains. Recent AutoML and multi-
                                                                       runtime errors but rely on human-provided test cases. Multi-agent
agent approaches [9, 49] automate broader ML pipelines but remain
                                                                       frameworks such as ChatDev [40] and AgentCoder [17] introduced
confined or pre-defined datasets, requiring manual effort to extend
                                                                       dynamic test generation through agent collaboration, yet remain
to specialised domains or datasets. Medical imaging automation
                                                                       limited to function-level or module-level generation. Contempo-
methods [18, 31, 50] incorporate domain expertise but address only
                                                                       rary tools including GitHub Copilot [11], Cursor [47], and Anti-
partial pipeline components without achieving fully automated
                                                                       gravity [12] integrate LLMs into IDEs with execution capabilities
generation. No existing approach combines comprehensive domain
                                                                       but still require substantial human intervention across complex
knowledge, systematic validation, and consistent context manage-
                                                                       multi-stage tasks in specialised domains.
ment to enable fully automated generation of complete, validated
pipelines from scratch.                                                   Automation in medical image processing. In the field of medi-
   To address these limitations, we propose AutoMedImg, a multi-       cal imaging, numerous automated algorithm design and optimiza-
agent framework for automated medical image processing code            tion methods have been developed. NAS [30, 42] automatically dis-
generation via validation-based context engineering. AutoMedImg        covers optimal network structures but requires predefined search
integrates domain knowledge bases eliminating exhaustive man-          spaces and manual pipeline implementation [50]. nnU-Net [18] au-
ual prompting, systematic multi-stage validation preventing error      tomates segmentation pipeline configuration but requires manual
propagation, and adaptive pipeline synthesis maintaining context       environment setup and is restricted to segmentation tasks. Foun-
across projects. Built on a multi-agent architecture, AutoMedImg       dation models like SAM [22, 41] and MedSAM [31] eliminate task-
orchestrates the pipeline from dataset analysis through architecture   specific training but require interactive prompts during inference
design, parallel module implementation, and final assembly. Evalu-     and address only segmentation. AutoML-Agent [49] automates full-
ation on six medical imaging datasets demonstrates that AutoMed-       pipeline ML across diverse tasks but requires manually provided
Img achieves fully automated code generation while maintaining         skeleton code for new task types and relies solely on prompt-based
competitive model performance.                                         rather than execution-grounded verification. DS-Agent [13] lever-
   The main contributions of this work are as follows:                 ages case-based reasoning for data science automation but lacks
                                                                       medical imaging knowledge for generating appropriate pipelines,
   (1) We propose a validation-based context engineering ap-           and its sole reliance on execution feedback can only guarantee
       proach integrating medical imaging domain knowledge,            runnable code without ensuring alignment with domain conven-
       shared memory, and multi-stage validation to automatically      tions. VoxelPrompt [16] integrates a jointly-trained vision-language
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                                                         ASE ’26, October 12–16, 2026, Munich, Germany


                                                  Planning Phase                                                                            Coding Phase
                          Medical image
                                                                                    Shared Memory                                                                      Shared Memory
                      processing requirement                                                                              Coding Orchestration
            User                                                                     Task requirement                                                                    Module scripts
                                                                                   Dataset analysis report            Coding
             Planning Orchestration                                                                                                                                    Syntax check report
                                                                                                                      router           Parallel
                                                                                    Architecture design
                                                                                                                                      allocation                        Execution result
                            Dataset metadata                                         CSP specification                                                                        ...
                              & Task type                                                  ...

           Planning                                                                                                                                                    Validation Layer
                                                                                   Validation Layer
            router                                        Exploratory
                                                        dataset analysis                                                                                       ...                  Tester
                                                             report         Dataset analysis                     Coder                                                              agent
                      Dataset analyser                                       semantic check                    subagent(s)
                         subagent
                                                                            Fail
                                                                            Fail                                Dataset       NN      Training     Inference
                                                        Heuristic-based                      Verification       module       module   module        module                                   Fail
                                                       pipeline synthesis                      agent                                                                    Pylint & Radon
                                                              plan                                                                                                       static check
                            Architect
                            subagent                                                                                                                                             Pass
                                                                                Planning
                                                                            semantic validation
                                                                                                                                       Assembly                             Pytest           Fail
             Input/output               Planning validation
                                                                                                                                         script                       execution validation
             Intermediate result        Coding validation
             Key information

              Generation
              Pass info                                                                                                                                                Adaptive pipeline
                                           Validated architecture design                                                       Complete medical image
              Skill                                                                                                                                                       synthesis
              Mem. Storage                      TO CODING PHASE                                                                  processing pipeline
              Fix loop
                                                                                                                                                                       knowledge base


                                                        Figure 1: AutoMedImg’s two-phase workflow: Planning and Coding


agent for end-to-end radiological analysis but focuses exclusively                                           propagate to the Coding Phase as validated pipeline designs. Cod-
on inference-time task execution without addressing automated                                                ing Phase. The Coding Router decomposes the validated pipeline
pipeline development or code generation. M3 Builder [9] automates                                            design and allocates multiple Coder subagents for parallel mod-
medical imaging ML workflows through multi-agent coordination                                                ule generation (Dataset, NN, Training, Inference modules). The
but restricts generation to pre-defined datasets with accompanying                                           Tester Agent validates each module through static checking (Pylint,
code templates, requiring manual preparation for new datasets.                                               Radon) and execution testing (Pytest); failures trigger code refine-
These approaches address only partial pipeline components, requir-                                           ment with diagnostic feedback. Validated modules are integrated
ing substantial expertise for deployment, and none achieves fully                                            into an assembly script, which is then subjected to final end-to-end
automated generation of complete pipelines from scratch.                                                     validation. Successfully validated pipelines that achieve satisfac-
                                                                                                             tory performance are entered into the Adaptive Pipeline Synthesis
3    Method: AutoMedImg Framework                                                                            Knowledge Base, along with their project characteristics and per-
                                                                                                             formance metrics, enabling future projects to retrieve and adapt
In this section, we present AutoMedImg workflow and framework
                                                                                                             proven components from similar tasks. This two-phase architec-
through 3 components: Section 3.1 details agent specifications and
                                                                                                             ture with systematic multi-stage validation enables fully automated
context integration mechanisms; Section 3.2 explains validation-
                                                                                                             generation of production-ready medical imaging pipelines.
based context engineering in the Planning and Coding phases;
Section 3.3 presents cross-project adaptive pipeline synthesis.
    Medical imaging pipelines require understanding the dataset                                              3.1      AutoMedImg agent specification
characteristics before implementation. AutoMedImg addresses this                                             3.1.1 Agent Coordination Structure. Complex medical image pro-
through a two-phase architecture, Planning and Coding, as illus-                                             cessing tasks require comprehensive expertise over multiple do-
trated in Figure 1. Planning Phase. Given a medical image pro-                                               mains, including medical image data analysis, library dependencies
cessing requirement, the Planning Router first invokes the Dataset                                           and APIs, data loading strategies, and neural network architecture
Analyser subagent to perform exploratory dataset analysis. The Ver-                                          design. A single-agent approach faces fundamental limitations: (1)
ification Agent validates this analysis through semantic checking,                                           simultaneously invoking knowledge across diverse domains creates
ensuring all required dataset features are extracted; failures trigger                                       confusion and inconsistent reasoning; (2) maintaining accurate con-
re-analysis with diagnostic feedback. Next, the Architect subagent                                           text becomes increasingly difficult as context accumulates through
synthesises a pipeline design based on validated dataset characteris-                                        planning, validation, and coding phases; (3) single-agent systems
tics. This design undergoes planning semantic validation at two lev-                                         cannot exploit parallel execution for efficiency improvement.
els: contextual validation checks architecture-dataset compatibility,                                           AutoMedImg addresses these limitations through a multi-agent
modularity requirements, and medical imaging conventions; formal                                             architecture organised as a router-subagent hierarchy with an in-
validation converts the architecture to CSP# specification for PAT-                                          dependent Validation Layer. To distribute domain expertise, Au-
based model checking, ensuring process correctness. Throughout                                               toMedImg employs specialised agents: the Planning Router invokes
this process, intermediate results (dataset analysis report, architec-                                       Dataset Analyser and Architect, while the Coding Router allocates
ture design, CSP specification) are stored in Shared Memory for                                              multiple Coder subagents in parallel for concurrent module gen-
agent coordination. Only architectures passing semantic validation                                           eration, each possessing focused knowledge rather than handling
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                        Zhao et al.


multiple domains simultaneously. Each agent maintains its own            the Testing Knowledge Base containing test case patterns and cov-
context window, with Shared Memory storing validated interme-            erage criteria, while utilising static analysis tools (Pylint, Radon)
diate results that agents retrieve as needed, preventing context         and dynamic testing frameworks (Pytest) through MCP. All agents
accumulation in a single window. Critically, the Verification Agent      share access to shared memory for validated intermediate results
and Tester Agent operate within an independent Validation Layer          and adaptive synthesis knowledge base for cross-project reference.
rather than embedded within generating agents, eliminating self-         Validation feedback from failed checks and tool execution results
validation bias. Routers coordinate workflow progression based on        is incorporated during the fix-loop, enabling targeted corrections.
validation outcomes: only verified results advance to subsequent         This comprehensive context integration enables each agent to au-
stages, while failures trigger automated correction loops with di-       tomatically construct domain-appropriate context without manual
agnostic feedback. This architecture addresses domain knowledge          prompting.
specialisation, phase-specific context management, and parallel
execution requirements.                                                  3.2    Validation-based context engineering
                                                                         Traditional LLM-based code generation operates through prompt-
          Task-specific prompt                  Adaptive synthesis       and-generate cycles, where agents produce outputs solely based
                                                knowledge base           on input prompts and pre-trained knowledge. This approach suf-
                   Agent Skill
                                     LLM                                 fers from three critical limitations: (1) without checking outputs,
                                                Validation feedback
               Shared memory         Core                                agents cannot assure output quality and reliability; (2) outputs prop-
                                                Tool execution results   agate unchecked, allowing errors to cascade through subsequent
       Domain knowledge base
                                                                         stages, and (3) without memory management through systematic
      Figure 2: AutoMedImg Agent Context Integration                     validation, high-quality patterns may not be reliably adapted or
                                                                         reused across projects. In medical image processing, these limita-
                                                                         tions manifest as misaligned preprocessing sequences, inconsistent
                                                                         architecture designs, and functionally incorrect implementations.
3.1.2 Agent Context Integration. AutoMedImg achieves compre-                AutoMedImg addresses these limitations through validation-
hensive agent context engineering through seven core components,         based context propagation: only outputs that satisfy validation
as illustrated in Figure 2. Task-specific prompts define each agent’s    criteria propagate to subsequent agents, while failures generate
objectives and expected outputs within the workflow. Agent Skills        diagnostic feedback, enabling targeted refinement. The mechanism
provide structured execution capabilities that guide agents in per-      operates across two phases: the Planning Phase validates dataset
forming specific tasks step-by-step with precise instructions. Do-       analyses and architecture designs through dataset analysis and
main knowledge bases supply agent-specific expertise for genera-         planning semantic validation; the Coding Phase validates module
tion and validation. Shared memory stores validated intermediate         implementations and system assembly through static and execution
results accessible across agents. Adaptive synthesis knowledge base      validation. We formalise this mechanism through the following
maintains validated pipelines from previous projects. Validation         definitions:
feedback provides diagnostic information guiding iterative correc-          Definition 1 (Agent Context). The context of agent 𝐴𝑖 is de-
tions. Tool execution results capture outputs from command-line          fined as:
or Model Context Protocol (MCP) tools invoked during execution.
   Specific resource assignments vary by agent role. Planning Router                        𝐶𝐴𝑖 = ⟨𝑃𝑖 , 𝑀, 𝐾𝐷𝑖 , 𝐾𝐴𝑑𝑎 , 𝐻𝑖 , 𝑉𝑖 ⟩           (1)
and Coding Router employ orchestration Skills for workflow coordi-       where 𝑃𝑖 represents agent 𝐴𝑖 ’s task-specific prompt; 𝑀 denotes
nation: Planning Router sequentially invokes Dataset Analyser and        shared memory containing accumulated validated outputs from all
Architect subagents, while Coding Router concurrently allocates          predecessor agents; 𝐾𝐷𝑖 is agent 𝐴𝑖 ’s domain knowledge base; 𝐾𝐴𝑑𝑎
multiple Coder subagents for parallel module generation. Dataset         is the Adaptive Pipeline Synthesis Knowledge Base; 𝐻𝑖 is agent 𝐴𝑖 ’s
Analyser, Architect, and Coder each access specialised knowledge         tool or Skill execution history; and 𝑉𝑖 is the agent’s accumulated
bases: The Dataset Analyser’s knowledge base is derived from             validation feedback.
nnU-Net [18] dataset card specifications, capturing standardised             Definition 2 (Context Evolution). Agent 𝐴𝑖 generates output
medical imaging dataset properties; The Architect’s knowledge            𝑜𝑖 = 𝑔𝐴𝑖 (𝐶𝐴𝑖 ) from its context, which is then evaluated by valida-
base is manually curated from leading neural network architectures       tion function V : O → {pass, (fail, 𝑓 )}. On pass, 𝑜𝑖 is stored in
on Grand Challenge, providing validated pipeline design patterns         shared memory 𝑀 and the next agent 𝐴𝑖+1 proceeds with updated
across diverse medical imaging tasks, with CSP# modeling Skill           context; on fail, diagnostic feedback 𝑓𝑖 is appended to 𝑉𝑖 and 𝐴𝑖
for converting architecture designs to formal specifications; The        retries with enriched context, enabling targeted correction.
Coder’s knowledge base is extracted from official MONAI API doc-
umentation, supplying library-specific implementation templates.         3.2.1 Domain Knowledge and Shared Memory. Domain knowledge
The Verification Agent’s knowledge base comprises manually sum-          bases 𝐾𝐷𝑖 and shared memory 𝑀 serve as foundational context com-
marised ISO/IEC 25023 modularity standards and IEC 62304 medical         ponents enabling validation-based context engineering across both
device software conventions, providing structured validation crite-      Planning and Coding phases. Domain knowledge provides agent-
ria and scoring rubrics for semantic assessment, CSP# interpretation     specific expertise without requiring manual specification, while
knowledge base for understanding verification outputs, alongside         shared memory enables the propagation of validated information
Skills for invoking PAT tool for formal verification. Tester accesses    without redundant computation.
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                   ASE ’26, October 12–16, 2026, Munich, Germany


    Domain Knowledge for Expertise Provision. Each agent                             reported (e.g., -1000 to 3000), and case counts are consistent. A miss-
accesses a domain knowledge base 𝐾𝐷𝑖 tailored to its role, providing                 ing spacing value or inconsistent case count triggers re-analysis
specialised contextual knowledge during generation. Each agent’s                     with targeted diagnostic feedback. This check is conducted by the
𝐾𝐷𝑖 is constructed from general medical-domain standards and docu-                   Verification Agent through rule-based semantic assessment: the
mentation as a knowledge graph using the Cognee framework [35],                      agent queries its domain validation knowledge, which contains
enabling natural language querying via MCP tool invocation dur-                      structured validation criteria and scoring rubrics, systematically
ing generation, and covering the most common medical imaging                         evaluates each architectural decision against these specifications,
tasks (supervised/semi-supervised segmentation and classification,                   and generates detailed diagnostic reports that enable targeted re-
2D/3D), modalities (CT, MRI, X-ray), and architectures. For example,                 finement of failed components.
the Dataset Analyser’s 𝐾𝐷𝑖 encodes properties such as: "CT images                       Planning Semantic Validation. Contextual semantic valida-
require HU windowing in range [-1000, 3000]; voxel spacing must                      tion checks two criteria. compatible(·, 𝑀) verifies that the architec-
be extracted and preserved for physical scale consistency." The Ar-                  ture aligns with validated dataset characteristics in shared memory
chitect’s 𝐾𝐷𝑖 stores patterns such as: "3D anisotropic data requires                 — for instance, anisotropic volumetric data requires patch-based
physical spacing-aware resampling; multi-organ segmentation with                     strategies and voxel-space resampling to preserve physical scale,
class imbalance requires Dice + Cross-entropy combined loss." The                    while multi-organ segmentation requires loss functions that ad-
Verification Agent’s 𝐾𝐷𝑖 contains criteria such as: "Ensure patient-                 dress class imbalance from organ volume distributions. On the other
level splitting to prevent data leakage; Validate CT preprocessing in-               hand, valid_design(·, 𝐾𝐷𝐴𝑟𝑐ℎ ) ensures compliance with ISO/IEC
cludes orientation normalisation before resampling." Without domain                  modularity requirements and medical imaging conventions drawn
knowledge, the agent’s outputs lack domain-specific constraints,                     from the domain knowledge base, including HU windowing for
leading to inappropriate outputs.                                                    CT, z-score normalisation for MRI, and patient-level data splitting
    Shared Memory for Context Propagation. Shared memory 𝑀                           to prevent leakage. For example, proposing a 2D UNet for a 3D
is implemented via Eion MCP tool, a persistent key-value store for                   CT dataset, or applying generic resize instead of voxel-space re-
multi-agent coordination, where validated outputs are written after                  sampling, triggers a compatibility failure with diagnostic feedback
each successful validation and retrieved through natural language                    specifying the violated convention, enabling targeted architecture
queries, enabling flexible and precise access to verified information                revision. This validation is executed in the same procedure as V𝑠 .
without redundant derivation. For instance, after the Dataset Anal-                     Formal semantic validation converts the architecture to a CSP#
yser completes validated analysis, 𝑀 contains: modality (CT), di-                    specification via dedicated Skill and validates it via PAT tool:
mensions (512×512×196), voxel spacing (0.8×0.8×3.0mm), intensity
range (-1000 to 3000 HU), and task type (supervised segmentation).                                      V𝑓 𝑠 (𝑜 𝐴𝑟𝑐ℎ ) = PAT(CSP(𝑜 𝐴𝑟𝑐ℎ ))                   (3)
The Architect retrieves these directly to design a patch-based 3D
pipeline with HU windowing preprocessing. Similarly, validated                       verifying deadlock-freedom, race condition absence, and LTL prop-
module code propagates through 𝑀 to assembly, eliminating redun-                     erties such as □(𝑚𝑜𝑑𝑒𝑙_𝑖𝑛𝑖𝑡𝑖𝑎𝑙𝑖𝑧𝑒𝑑 → ♦𝑡𝑟𝑎𝑖𝑛𝑖𝑛𝑔_𝑓 𝑖𝑛𝑖𝑠ℎ𝑒𝑑) and
dant validation and ensuring consistency across workflow stages.                     □(𝑡𝑒𝑠𝑡_𝑑𝑎𝑡𝑎_𝑙𝑜𝑎𝑑𝑒𝑑 → ♦𝑖𝑛𝑓 𝑒𝑟𝑒𝑛𝑐𝑒_𝑐𝑜𝑚𝑝𝑙𝑒𝑡𝑒). Properties are de-
                                                                                     rived from manually verified templates that specify standard safety
3.2.2 Planning Phase Context Engineering. The Planning Phase                         and liveness requirements for medical imaging workflows. The
constructs validated architecture designs through sequential agent                   Verification Agent adapts these templates to the current project
invocation with validation-guided refinement. Dataset Analyser                       through regex-based Skill invocation, substituting project-specific
extracts medical imaging characteristics; Architect designs pipeline                 process names and parameters while preserving the verified safety
architectures grounded in validated dataset analysis; Verification                   and liveness properties. Since medical image processing pipelines
Agent ensures planning correctness through two-level semantic                        follow consistent algorithmic patterns (data loading, preprocess-
validation: dataset analysis semantic checking verifies complete-                    ing, training, inference), the templates comprehensively cover the
ness and domain compliance; planning semantic validation checks                      required properties across different tasks.
architecture correctness through contextual domain conventions                          Through two-level semantic validation on architecture design,
and formal CSP# model checking.                                                      the Planning Phase achieves validation-based context engineer-
   Dataset Analysis Semantic Check. Semantic validation V𝑠                           ing: each agent iteratively refines its outputs through validation
verifies structural completeness and domain compliance of the                        feedback, and only verified outputs enter shared memory 𝑀 for
dataset analysis:                                                                    subsequent agents, preventing error propagation while eliminating
                                                                                     manual specification requirements.
 V𝑠 (𝑜 𝐷𝐴 ) = pass ⇔ ∀𝑝 ∈ P𝐷𝐴 : 𝑝 ∈ 𝑜 𝐷𝐴 ∧ consistent(𝑜 𝐷𝐴 ) (2)
                                                                                     3.2.3 Coding Phase Context Engineering. The Coding Phase trans-
where P𝐷𝐴 = {𝑚𝑜𝑑𝑎𝑙𝑖𝑡𝑦, 𝑑𝑖𝑚𝑒𝑛𝑠𝑖𝑜𝑛𝑠, 𝑠𝑝𝑎𝑐𝑖𝑛𝑔, 𝑖𝑛𝑡𝑒𝑛𝑠𝑖𝑡𝑦, 𝑐𝑜𝑢𝑛𝑡 } de-                   lates the validated architecture design into executable code through
notes the required dataset properties. In practice, the Verification                 validation-guided synthesis. Upon receiving 𝑜 𝐴𝑟𝑐ℎ ∈ 𝑀 from the
Agent queries its domain validation knowledge base and evaluates                     Planning Phase, the Coding Router parses the JSON-structured
the dataset analysis JSON output, checking for the presence and                      architecture design, which explicitly specifies class definitions with
consistency of each required property in P𝐷𝐴 . For example, for a CT                 inheritance relationships, method signatures with type annotations,
dataset, validation checks that modality is correctly identified, voxel              attributes with pre-defined values (e.g., learning rate, patch size),
spacing is extracted (e.g., 0.8×0.8×3.0mm), HU intensity range is                    and inter-module dependencies. The Router then decomposes the
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                                        Zhao et al.


design into module specifications for parallel Coder agents to imple-     mismatches, dimension incompatibilities, and incorrect sequencing,
ment. This phase employs three validation mechanisms operating            triggering targeted refinement with diagnostic feedback.
at increasing scopes: static checking validates the quality of indi-         Through static, execution, and assembly validation, the Coding
vidual module code; execution validation verifies the functional          Phase achieves multi-scale validation-based context engineering:
correctness of modules through dynamic testing; and assembly              individual modules refine through validation feedback, validated
validation ensures the consistency of system-level integration.           modules propagate through 𝑀𝑐𝑜𝑑𝑒 , and only high-performing com-
   Static Checking on Module Code. Static checking V𝑠𝑡𝑎𝑡 veri-            plete pipelines enter 𝐾𝐴𝑑𝑎 for future adaptive synthesis, ensuring
fies syntactic correctness, dependency consistency, and code quality      both correctness and quality throughout implementation.
before execution. The Tester Agent employs Pylint for syntax vali-
dation and Radon for complexity measurement:                              3.3      Cross-project adaptive pipeline synthesis
                                 Û
 V𝑠𝑡𝑎𝑡 (𝑐𝑜𝑑𝑒𝑖 ) = pass ⇔                  threshold(𝑚, 𝑐𝑜𝑑𝑒𝑖 , 𝜏𝑚 )
                               𝑚∈ {𝑃 𝑦𝑙𝑖𝑛𝑡,𝐶𝐶,𝑀𝐼 }                          Knowledge accumulation              Similarity-based retrieval          Cross-project adaptation
                                                                    (4)          Validated pipeline                    New medical image                  Characteristic
                                                                                                                     processing requirement                differences
where Pylint(·) measures syntactic correctness and dependency                   (Architecture design
                                                                                    + codebase)                  dataset modality,
validity, 𝐶𝐶 (·) denotes cyclomatic complexity, 𝑀𝐼 (·) represents                                                    task type,
                                                                                                                    constraints                             Adaptation
maintainability index, and 𝜏𝑚 denotes the quality threshold for                    Performance                            Semantic                      [number of classes,
                                                                                                                      similarity checking                   image size,
                                                                                      check
each metric 𝑚 gated by ISO/IEC 25023 standards. In practice, the                                        Not                              Generate         preprocessing...]
                                                                                                       stored
                                                                                                                       Similar
                                                                                                                                           from
                                                                                Dice/Acc >
Tester Agent invokes Pylint and Radon via MCP tool calls, collecting            Threshold                           project found         scratch

their structured outputs and evaluating CC and MI scores against                Adaptive pipeline                      Retrieved pipeline
                                                                                   synthesis                          (Architecture design               Adapted pipeline
predefined thresholds (𝜏𝐶𝐶 = 𝜏𝑀𝐼 = 80), while Pylint pass/fail is de-           knowledge base                            + codebase)

termined automatically by its built-in rule set. Static checking elim-
inates syntactic errors before execution, reducing the complexity
of runtime validation. Failed checks enrich 𝑉𝐶𝑜𝑑𝑒𝑟 with diagnostic        Figure 3: Cross-project Adaptive Pipeline Synthesis Work-
feedback including error locations, dependency conflicts, and API         flow
mismatches for targeted correction.
                                                                             A critical limitation of LLM-based code generation is the lack of
   Execution Validation on Module Code. Execution validation
                                                                          cross-project continuity: each generation session operates indepen-
V𝑒𝑥𝑒𝑐 verifies runtime correctness through dynamic testing via
                                                                          dently, without retaining knowledge from previous successful tasks.
Pytest. The Tester generates test cases covering three categories:
                                                                          In medical image processing, analogous scenarios frequently arise:
assumption tests validate input constraints (e.g., verifying input
                                                                          analysing different organs within the same modality, segmenting
tensor shape matches expected dimensions [𝐵, 𝐶, 𝐷, 𝐻,𝑊 ] for 3D
                                                                          tissues with similar features, or processing datasets with compara-
volumetric data); functional tests verify computational correctness
                                                                          ble structures. These recurring patterns necessitate cross-project
(e.g., checking that preprocessing output intensity range falls within
                                                                          learning that standard LLMs cannot exploit. Cross-project adap-
the expected HU window after normalisation); and integration tests
                                                                          tive pipeline synthesis addresses this by accumulating validated
check interface compatibility (e.g., confirming that preprocessed
                                                                          solutions in 𝐾𝐴𝑑𝑎 and leveraging them to guide future generations.
output shape matches NN module input expectations). Formally:
                         Û                                                This constrains the solution space from exhaustive assumption to
   V𝑒𝑥𝑒𝑐 (𝑐𝑜𝑑𝑒𝑖 ) =              execute(𝑡, 𝑐𝑜𝑑𝑒𝑖 ) = expected(𝑡)         synthesis within validated neighbourhoods, minimising error, and
                     𝑡 ∈𝑇 𝑒𝑠𝑡𝑠 (𝑐𝑜𝑑𝑒𝑖 )                                   enhancing generation efficiency. Figure 3 illustrates this three-stage
                                                                  (5)     process:
The Tester Agent generates 30–40 test cases per module via LLM               Knowledge Accumulation. Successfully validated pipelines
invocation, guided by testing rules and examples from its knowl-          achieving satisfactory performance enter 𝐾𝐴𝑑𝑎 for cross-project
edge base. Test cases are executed via MCP tool calls to Pytest, with     reference:
execution traces captured and appended to 𝑉𝐶𝑜𝑑𝑒𝑟 as diagnostic
                                                                            𝐾𝐴𝑑𝑎 ← 𝐾𝐴𝑑𝑎 ∪ {(𝑜 𝐴𝑟𝑐ℎ , 𝑐𝑜𝑑𝑒, 𝜉, 𝜌)}                             if V𝑎 = pass ∧ 𝜌 ≥ 𝜃 (6)
feedback for targeted correction. Failed tests trigger refinement
cycles where execution traces reveal runtime behaviour, enabling          where 𝑜 𝐴𝑟𝑐ℎ represents the validated architecture design, 𝑐𝑜𝑑𝑒 rep-
targeted debugging. Only modules satisfying both static and execu-        resents the complete pipeline codebase, 𝜉 captures project charac-
tion validation propagate to assembly.                                    teristics (dataset modality, task type, dimensionality, architectural
   Assembly Validation. Assembly validation V𝑎 verifies system-           constraints), 𝜌 denotes performance metrics (Dice score, accuracy),
level correctness after module integration by applying both static        and 𝜃 defines the quality threshold. In practice, validated pipeline
checking and execution validation to the assembled pipeline. While        entries are appended incrementally to the agent knowledge graph
individual modules may pass isolated validation with mocked in-           via Cognee, enabling retrieval through the same natural language
puts, module-level correctness does not guarantee system-level            querying mechanism as the domain knowledge base; each dataset
correctness when real data flows among modules. For example, the          can only reference pipelines validated from previously processed
Dataset module may correctly output a dictionary with key image           datasets, ensuring all retrieved components originate exclusively
that passes its own validation, while the NN module expects key           from prior evaluation datasets and avoid information leakage across
data, violating the interface contract that only manifests when both      projects. Each entry preserves the complete pipeline structure, val-
modules are assembled. Assembly validation detects such interface         idated components, and achieved performance, enabling future
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                  ASE ’26, October 12–16, 2026, Munich, Germany


projects to access proven solutions rather than generating them                      configurations and evaluation metrics. Section 4.3 reports experi-
from scratch.                                                                        mental results organised by research question, including compre-
   Similarity-based Retrieval. When processing a new project                         hensive ablation studies.
with requirements 𝜉𝑛𝑒𝑤 , AutoMedImg retrieves relevant pipelines
from 𝐾𝐴𝑑𝑎 based on characteristic similarity:                                        4.1     Benchmarking datasets
    R (𝜉𝑛𝑒𝑤 ) = {(𝑜 𝐴𝑟𝑐ℎ , 𝑐𝑜𝑑𝑒, 𝜉, 𝜌) ∈ 𝐾𝐴𝑑𝑎 | 𝑠𝑖𝑚(𝜉𝑛𝑒𝑤 , 𝜉) ≥ 𝜏𝑠𝑖𝑚 } (7)           To evaluate the performance of AutoMedImg and baseline methods
                                                                                     across different medical image processing sub-tasks, we selected
In practice, 𝑠𝑖𝑚(·, ·) is computed via LLM-based semantic matching,                  four task categories comprising six datasets in total:
where the Router evaluates characteristic alignment between the                      FLARE22 [33]: A semi-supervised 3D segmentation dataset for 13
new project and retrieved entries through natural language rea-                      abdominal organs in CT scans (50 labelled, 2000 unlabelled cases,
soning over project descriptors, applying hierarchical matching:                     512×512×196), challenging due to the large unlabelled pool with
hard constraints, including dataset modality and task type, must                     limited supervision.
match exactly, while soft constraints such as dimensionality and                     ACDC [4]: A supervised 3D segmentation dataset for three car-
architectural requirements are assessed by degree of similarity. 𝜏𝑠𝑖𝑚                diac structures in MRI (215×228×10), challenging due to significant
defines the minimum alignment threshold across both hard and                         anisotropic voxel spacing.
soft constraints, where any mismatch in hard constraints immedi-                     BTCV [24]: A supervised 3D segmentation dataset for 13 organs
ately disqualifies retrieval regardless of soft constraint similarity.               in CT scans (50 cases, 512×512×123), challenging due to limited
Retrieved pipelines serve as reference implementations, providing                    samples and imbalanced organ volumes.
validated architecture designs and codebases for adaptation.                         FLARE21 [32]: A supervised 3D segmentation dataset for 4 abdom-
   Cross-project Adaptation. For a retrieved entry (𝑜 𝐴𝑟𝑐ℎ , 𝑐𝑜𝑑𝑒,                   inal organs in CT scans (361 cases, 512×512×126), representing a
𝜉𝑜𝑙𝑑 , 𝜌) ∈ R (𝜉𝑛𝑒𝑤 ), agents extract components and adapt them                      relatively simpler segmentation task than FLARE22.
based on characteristic differences Δ(𝜉𝑜𝑙𝑑 , 𝜉𝑛𝑒𝑤 ) such as class num-               Promise12MSBench [23]: A supervised 2D segmentation dataset
bers, image size, and preprocessing requirements, and adapt the                      for binary prostate segmentation in MRI (512×512), derived from
retrieved pipeline accordingly. For example, when processing semi-                   PROMISE12 [29].
supervised 3D CT segmentation after a supervised 3D CT segmen-                       OrganMNIST3D [51]: A supervised 3D classification dataset for 11
tation task, AutoMedImg retrieves the segmentation pipeline as a                     organ categories in CT scans (1,742 samples, 64×64×64), the most
reference, adapts the same data loading strategy, adjusts the num-                   straightforward task in our benchmark.
ber of output classes, and adds the unlabelled data handling logic,                     These six datasets are selected because they cover the two most
while retaining the validated preprocessing pipeline and 3D UNet                     fundamental medical image processing tasks (segmentation and
architecture. All adapted outputs undergo validation in the main                     classification), are publicly available and widely adopted bench-
pipeline to ensure correctness for the target project.                               marks, and span a comprehensive difficulty gradient from simple
   Through 𝐾𝐴𝑑𝑎 , AutoMedImg achieves cross-project adaptation:                      supervised classification to complex 3D semi-supervised segmenta-
validated pipelines accumulate incrementally, relevant components                    tion, enabling robust evaluation across diverse scenarios.
are retrieved based on project similarity, and adaptations undergo
validation ensuring correctness. This mechanism enables knowl-                       4.2     Evaluation settings & criteria
edge reuse while maintaining quality standards, operating without
                                                                                     4.2.1 Baseline Prompt Design and Configuration. To evaluate the
human supervision.
                                                                                     fundamental limitations of existing code generation approaches on
                                                                                     medical image processing tasks, all baseline methods receive care-
4     Evaluation                                                                     fully designed prompts that provide equivalent task structure and
To thoroughly investigate the effectiveness of AutoMedImg, we                        necessary tool access, enabling them to attempt the same four-stage
formulate the following research questions:                                          pipeline as AutoMedImg: Dataset Analysis: Generate scripts to
   RQ1: What are the fundamental limitations of existing                             examine dataset file structure, image dimensions, modality charac-
code generation approaches when applied to medical image                             teristics and intensity distributions. Architecture Design: Design
processing tasks?                                                                    the complete pipeline architecture based on dataset analysis re-
   RQ2: How does AutoMedImg address the fundamental                                  sults, including preprocessing and data-loading strategies, neural
limitations of existing code generation approaches compared                          network structure, training configurations, and inference work-
to advanced multi-agent and automated ML frameworks?                                 flow. Module Implementation: Implement individual modules
   RQ3: How do AutoMedImg’s individual validation and                                according to the architecture design. Pipeline Assembly: Gener-
context engineering components contribute to reducing LLM                            ate an assembly script integrating all modules into an executable
errors and ensuring code correctness?                                                end-to-end pipeline.
   RQ4: How does AutoMedImg’s multi-agent architecture                                   Baselines also receive command-line execution permissions and
improve code generation quality compared to applying the                             file system access where their architecture permits, enabling them
same context engineering techniques in a single-agent sys-                           to: (1) execute Python scripts for runtime debugging, (2) read/write
tem?                                                                                 files during code generation, (3) check and install required depen-
   This section proceeds as follows: Section 4.1 presents the bench-                 dencies, and (4) attempt to iteratively refine code based on execution
mark datasets and their features. Section 4.2 describes experimental                 feedback. This configuration allows us to identify what types of
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                           Zhao et al.



                                      Human Interventions (HI ↓)                                      Performance (Dice/Acc ↑)
                                                                                                                                                  1
                            Copilot       13          9    9      6     11         5   30           0.61       0.46   0.56   0.54   0.77   0.86

                            Cursor        17          7    13     7      9     12                   0.13       0.81   0.71   0.7    0.88   0.94
                                                                                                                                                  0.8
                       Antigravity         8          7    5      10     5         5                  0.8      0.81   0.71   0.84   0.64   0.99

                      Qwen3-coder         13          8    9      11     5         5                0.06       0.78   0.48   0.76   0.67   0.98   0.6
                                                                                       20
                          GPT-oss         25      31       17     8      7         7                0.01       0.01   0.02   0.15   0.81   0.96

                    DeepSeek-V3.2          8          7    11     10     7         5                0.57       0.78   0.37   0.84   0.88   0.91   0.4

                          GPT-5.2          7          7    5      6      7         7                0.78       0.79   0.51   0.83   0.94   0.98
                                                                                       10                                                         0.2
                      Gemini3-pro          9          6    8      9      9         6                  0.6      0.69   0.74   0.76   0.79   0.81

                  Claude-4.5-Opus          7          6    12     6      5         6                0.53       0.68   0.62   0.86   0.92   0.75
                                                                                                                                                  0
                                       2          C              1      12    ST                    2       C                 1      12    ST
                                      2       D         CV    E2    ise                          E2        D        CV     E2    ise
                                   RE      AC         BT                   NI                           AC       BT                     NI
                                LA                          AR    om anM                     LA
                                                                                                R                       AR     om anM
                              F                          FL    Pr    rg                     F                        FL     Pr    rg
                                                                   O                                                            O

                Figure 4: Performance of Code Generation Tools and Base LLMs on Medical Image Processing Tasks

errors and limitations emerge without AutoMedImg’s validation-                          evaluation of existing baseline coding tools and LLMs on bench-
based context engineering and multi-agent coordination.                                 marking medical image processing tasks.
                                                                                            Proprietary IDE tools require 5–17 human interventions across
4.2.2 Experiment Environmental Settings. The evaluation was per-                        all tasks, revealing a fundamental inability to autonomously handle
formed on an Ubuntu 22.04 server equipped with an AMD Ryzen                             domain-specific requirements. Interventions predominantly take
Threadripper PRO 3995WX CPU (64 cores), 252GB RAM, and 2                                the form of design guidance and preprocessing specification, such
NVIDIA RTX A6000 GPUs (48GB VRAM each). We provide a uni-                               as selecting appropriate architectures, applying correct preprocess-
fied Python environment with pre-installed medical imaging li-                          ing, and accounting for volumetric data properties, as well as error
braries and common dependencies. All methods can install addi-                          correction for frequent execution failures. While these tools can
tional dependencies as needed during code generation. Regarding                         generate syntactically correct code, they lack domain knowledge to
AutoMedImg’s domain knowledge, it’s constructed from general                            make appropriate design decisions, such as selecting appropriate
medical-domain standards independent of the evaluation datasets                         architectures, applying appropriate preprocessing, and account-
selected for this study, ensuring no dataset-specific knowledge is                      ing for volumetric data properties, leading to frequent failures that
embedded in the framework prior to evaluation.                                          require human correction. Notably, Antigravity performs most com-
                                                                                        petitively (0.6372–0.9938, fewer than 10 interventions) owing to
4.2.3 Evaluation Criteria. We evaluate methods across three di-                         its partial memory retention across sessions, indirectly suggesting
mensions. To measure autonomy, we count human interventions                             the value of cross-project knowledge accumulation. Open-source
(HI) — the number of times a human must intervene to correct                            LLMs exhibit severe limitations in both domain knowledge and au-
errors or provide guidance that the system cannot autonomously                          tonomous error correction. Interventions span the broadest range,
resolve, including error correction, design guidance, and work-                         including domain design guidance, preprocessing specification,
flow instructions. HI takes three forms: direct prompt interactions                     manual script execution, and error message relay. Without domain
(providing instructions, relaying error messages, or corrections),                      guidance, these models make critical preprocessing errors that break
passing templates or skeleton code, and, rarely, manual script or                       fundamental medical imaging properties. For example, GPT-oss ap-
configuration updates. For model performance, we use the Dice                           plies unrestricted Resize instead of voxel-space Resample, corrupt-
coefficient [53] for segmentation and accuracy for classification,                      ing physical scale information and causing near-zero segmentation
both measured on test sets using identical evaluation protocols.                        performance (0.0067 Dice on FLARE22), yet lacks the validation
For implementation quality, we analyse structural designs includ-                       mechanisms to detect and correct such errors autonomously. Pro-
ing preprocessing strategies, data augmentation techniques, neural                      prietary LLMs demonstrate stronger baseline capabilities but still
network architectures, and computational efficiency (GPU mem-                           require 5–12 interventions with inconsistent performance across
ory usage and training time). On selected datasets, we conduct                          datasets (0.5058–0.9752 Dice), revealing that general coding abil-
detailed comparisons to assess whether generated pipelines adhere                       ity alone is insufficient for full autonomy in specialised domains
to medical imaging practices and properly handle volumetric data                        even with state-of-the-art models. Interventions are more mixed,
properties. All experiments are conducted with Pass@3, running                          spanning both domain design guidance and workflow instruc-
each configuration three times and reporting the best-performing                        tions, reflecting stronger but still insufficient domain awareness.
trial.                                                                                   Answer to RQ1: Existing code generation tools and LLMs con-
                                                                                         sistently fail on medical imaging tasks due to lack of domain
4.3     Experimental results                                                             knowledge and validation, with Antigravity’s partial memory
                                                                                         retention suggesting cross-project knowledge accumulation as a
4.3.1 Limitations of Existing Code Generation Approaches. To iden-
                                                                                         promising direction.
tify the fundamental limitations of existing code generation ap-
proaches on medical imaging tasks (RQ1), Table 4 presents the
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                  ASE ’26, October 12–16, 2026, Munich, Germany


   Table 1: Comparison of AutoMedImg Against Multi-agent and AutoML Frameworks on Medical Image Processing Tasks

                                                 FLARE22    ACDC      BTCV     FLARE21 Promise12 OrganMNIST
                     Method                     HI↓ Dice↑ HI↓ Dice↑ HI↓ Dice↑ HI↓ Dice↑ HI↓ Dice↑ HI↓ Acc↑
                     Multi-agent frameworks
                     CAMEL with GPT5.2 [25]      6 0.6523 7 0.7234 9 0.6312 6 0.7018 6 0.8456 5 0.8923
                     MetaGPT X [15]              4 0.7132 3 0.7750 3 0.6845 4 0.7534 3 0.8821 3 0.9125
                     MaCTG [52]                  3 0.5104 4 0.6273 2 0.5205 3 0.8414 2 0.8719 1 0.8820
                     AutoML frameworks
                     AutoML-Agent [49]           5 0.7421 2 0.6907 4 0.6237 2 0.7428 1 0.8870 1 0.9752
                     M3 builder [9]              6 0.7568 5 0.7413 1 0.7392 3 0.7464 3 0.8437 4 0.8727
                     Ours
                     AutoMedImg-Qwen3-Coder      0 0.7309 0 0.7856 0 0.6423 0 0.8204 0 0.8696 0 0.9752
                     AutoMedImg-Deepseek-V3.2    0 0.8333 0 0.7943 0 0.7678 0 0.8518 0 0.9293 0 0.9565
                     AutoMedImg-GPT5.2           0 0.8090 0 0.7901 0 0.7669 0 0.8667 0 0.9396 0 0.9752
                     AutoMedImg-Gemini3-pro      0 0.8440 0 0.8936 0 0.7664 0 0.8945 0 0.9347 0 0.8509
                     AutoMedImg-Claude-4.5-Opus 0 0.8185 0 0.9041 0 0.7696 0 0.8789 0 0.9517 0 0.9938

4.3.2 Performance of AutoMedImg Against Advanced Multi-agent                         AutoMedImg achieves zero human interventions across all task
and AutoML Frameworks. To demonstrate how AutoMedImg ad-                             types including semi-supervised segmentation, while maintaining
dresses the limitations (RQ2), we compare AutoMedImg against                         competitive or superior performance compared to all frameworks.
multi-agent and AutoML frameworks under identical task con-                           Answer to RQ2: While multi-agent and AutoML frameworks
figurations, providing both quantitative performance evaluation                       partially address RQ1 limitations, they introduce their own con-
(Table 1) and qualitative pipeline design analysis on BTCV (Table 2).                 straints including manual input dependencies and fixed templates.
    Multi-agent frameworks demonstrate improved autonomy                              AutoMedImg overcomes these through domain-specific knowl-
over baseline tools but still suffer from the identified fundamental                  edge, systematic multi-stage validation, and adaptive synthesis,
limitations. CAMEL lacks domain-specific guidance, resulting in                       achieving fully automated generation where existing frameworks
basic preprocessing and augmentation strategies. MetaGPT X still                      still require human preparation.
shows performance gaps on complex tasks (0.6845 Dice on BTCV,
0.7750 on ACDC), demonstrating that code generation quality alone                    4.3.3 Ablation Study. To quantify the contribution of each indi-
is insufficient without domain validation. MaCTG achieves the low-                   vidual validation and context-engineering component (RQ3), we
est intervention counts (1–4) through intra-agent validation, yet                    ablate each component individually while keeping all others intact,
without domain knowledge its validation fails on complex multi-                      measuring the impact on autonomy, performance, and generation
organ segmentation (0.5104 on FLARE22, 0.5205 on BTCV) despite                       efficiency across all six datasets with Claude-4.5-Opus as the back-
strong performance on simpler tasks, confirming that multi-agent                     bone (Table 5).
architecture alone is insufficient without domain-specific validation.                  Planning Phase Validations. Dataset analysis semantic check-
AutoML frameworks exhibit different but equally limiting con-                        ing removal increases interventions by 0.10 with 3.3% performance
straints. AutoML-Agent requires a manually provided code skeleton                    degradation, as missing critical properties such as voxel spacing
for each new task type, fundamentally constraining its applicability,                or intensity range lead to subtly incompatible downstream designs
and its retrieval mechanism fetches neural network architectures                     that only manifest as performance degradation rather than outright
while ignoring preprocessing requirements for complex medical                        failures. Planning semantic validation removal has a more severe
data formats, increasing interventions on specialised tasks (5 on                    impact (+0.57 HI, -4.7%), reflecting the central role of architecture
FLARE22, 4 on BTCV). M3 Builder relies on manually provided                          validation in the overall pipeline — without contextual validation,
dataset cards and fixed templates for segmentation and classifi-                     agents may select fundamentally incompatible architectures such
cation, lacking dynamic pipeline design capability. Its template-                    as 2D networks for 3D volumetric data. Without formal semantic
based approach causes hallucinations on task type selection and                      validation, occasional specification-level inconsistencies that con-
aborted executions on tasks outside template coverage, particularly                  textual checks cannot detect go unresolved. While medical imaging
semi-supervised segmentation (6 interventions on FLARE22). Its                       pipelines follow straightforward sequential structures that rarely
competitive BTCV performance (0.7392 Dice) stems from prede-                         violate process ordering properties, formal verification provides
fined template coverage and forced nnU-Net backbone rather than                      an additional correctness guarantee that catches edge cases before
adaptive design capability.                                                          implementation begins. Together, these two planning validation
    AutoMedImg addresses the identified limitations across both                      steps form a comprehensive correctness gate, preventing a com-
framework categories. Domain-specific knowledge bases eliminate                      bined +0.67 HI increase and significant performance degradation
the need for manually provided skeletons or dataset cards, enabling                  before implementation begins.
fully automated generation from arbitrary datasets. Multi-stage                         Coding Phase Validations. Code validations exhibit a strong
validation prevents error propagation and hallucinations that cause                  impact on autonomy. Syntax check removal adds 0.67 interventions
framework abortions. Adaptive pipeline synthesis enables cross-                      and increases generation time by 37.2 minutes, as downstream vali-
project knowledge reuse without the rigidity of fixed templates.                     dations eventually catch syntax errors after attempting to execute
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                                                                                          Zhao et al.


                                                     Table 2: Detailed Method Comparison on BTCV Dataset (Supervised 3D Segmentation)

                                           Method                                                                         Preprocessing                 Augmentation                     Model        GPU Time
                                           Multi-agent frameworks
                                           CAMEL-GPT-5.2                                                                  Res., Norm.                   Rot., Flip                      UNet3D         8.9   146
                                           MetaGPT X                                                                      Ori., Res., Norm.             Patch, Rot., Flip, Int.         UNet3D+RN      6.0   257
                                           MaCTG                                                                          Ori., Res., Norm.             Rot., Noise, Flip, Int., Smooth UNet3D        25.5   203
                                           AutoML frameworks
                                           AutoML-Agent                                                                   Ori., Res., Norm.             Patch                            UNet3D       14.4   106
                                           M3 builder                                                                     Norm., Pad                    Patch, Rot., Noise, Flip, Int.   nnUNet       15.8   235
                                           Ours
                                           AutoMedImg-Qwen3-coder                                                         Ori., Res., Norm.             Patch, Rot., Flip                UNet3D        9.2   318
                                           AutoMedImg-DeepSeek3.2                                                         Ori., Res., Norm.             Rot., Flip, Noise, Int.          UNet3D       16.6    63
                                           AutoMedImg-GPT-5.2                                                             Ori., Res., Norm.             Patch, Rot., Flip, Int.          UNet3D       12.5   382
                                           AutoMedImg-Gemini3-pro                                                         Ori., Res., Norm., Pad        Patch, Rot., Flip, Int.          SwinUNet3D   23.1   533
                                           AutoMedImg-Claude4.5-Opus                                                      Ori., Res., Norm., Pad        Patch, Rot., Noise, Flip, Int.   UNet3D       14.9   477
                                                                                    Abbreviations: Ori.=Orientation, Res.=Resample, Norm.=Normalize, Rot.=Rotate, Int.=Intensity, RN=ResNet.
                                                                                        GPU refers to VRAM consumption during training in GB; Time refers to training time in minutes.



                 Planning                             Coding                             Memory/Know.                                      Agent Mode        Without runtime verification, functional errors, such as tensor di-
                                                                                                                                                             mension mismatches or incorrect function calls, can propagate to
                                            ∆HI ↑ (interventions added)
                                                                                                                                                             later stages, requiring substantial human debugging. Assembly val-
       4
                                                                                                                                                             idation removal causes 2.50 additional interventions, confirming
       3                                                                                                                                                     its necessity for detecting integration issues between individually
       2
                                                                                                                                                             validated modules.
                                                                                                                                                                 Memory and Knowledge Components. Shared memory re-
       1
                                                                                                                                                             moval causes 2.4% performance degradation with a 16-minute
       0                                                                                                                                                     time increase, indicating its role in maintaining context consis-
                k
                              Va
                                l                k
                                                           Ts
                                                                t
                                                                          Va
                                                                             l
                                                                                            em              B                 n            nt
            Ch                             Ch                                                                           Sy             ge
      DA            Pl
                      an
                                    Sy
                                      n
                                                 Ex
                                                      ec
                                                                    As
                                                                      m
                                                                                  Sh
                                                                                     r
                                                                                         M
                                                                                                     no
                                                                                                       w
                                                                                                           K
                                                                                                                Ad
                                                                                                                    p
                                                                                                                                  M
                                                                                                                                   -A                        tency across agents. Removing the knowledge base results in the
                                                                                                 K
                                                                                                                                                             largest performance degradation (-13.7%) with minimal increase
                                               ∆Perf. ↓ (% performance drop)                                                                                 in HI (+0.33), indicating that domain-specific knowledge primarily
                                                                                                                                                             guides appropriate designs. Without medical imaging practices and
           15
                                                                                                                                                             conventions, agents generate syntactically correct but suboptimal
           10                                                                                                                                                pipelines, such as using torchvision transforms instead of MONAI
                                                                                                                                                             medical imaging transforms, or applying a generic resize operation
           5                                                                                                                                                 that breaks voxel spacing information. Adaptive synthesis removal
                                                                                                                                                             results in 8.4% performance degradation and an over 37-minute time
           0
                     k
                                   Va
                                      l               k
                                                                Ts
                                                                  t
                                                                                  Va
                                                                                     l
                                                                                                  em            B                  n            nt
                                                                                                                                                             overhead, confirming that cross-project learning enables agents to
                 Ch                              Ch                                             M              K              Sy            ge
                           an               n              ec              m                            w                 p             -A
           DA            Pl               Sy          Ex                 As            Sh
                                                                                          r
                                                                                                     K
                                                                                                      no             Ad                M                     adapt pipelines from previous projects rather than regenerate from
                                                                                                                                                             zero. Without it, agents must generate solutions independently,
                                                     ∆Time ↑ (minutes added)                                                                                 resulting in slow generation and suboptimal designs.
           40
                                                                                                                                                              Answer to RQ3: AutoMedImg’s validation-based context engi-
                                                                                                                                                              neering achieves automated generation through three integrated
                                                                                                                                                              mechanisms: multi-stage validation for systematic correction, do-
           20
                                                                                                                                                              main knowledge and shared memory for quality and efficiency,
                                                                                                                                                              and adaptive synthesis for cross-project learning, collectively
           0                                                                                                                                                  eliminating manual prompting throughout the coding process.
                     k
                                   Va
                                      l              k
                                                                Ts
                                                                     t
                                                                                  Va
                                                                                     l
                                                                                                 em        B         n         nt
                 Ch                              Ch                                                      K        Sy        ge
           DA            Pl
                              an
                                          Sy
                                             n
                                                      Ex
                                                        ec
                                                                         As
                                                                              m
                                                                                       Sh
                                                                                            r
                                                                                                M
                                                                                                     no
                                                                                                       w
                                                                                                             Ad
                                                                                                                p
                                                                                                                       M
                                                                                                                         -A                                      To isolate the architectural contribution of multi-agent design
                                                                                                   K
                                                                                                                                                             (RQ4), we compare multi-agent versus single-agent execution un-
Figure 5: Ablation Study: Average Impact of Component Re-                                                                                                    der identical context-engineering settings, where the single-agent
moval on AutoMedImg with Claude-4.5-Opus                                                                                                                     mode receives the same domain knowledge, validation mechanisms,
malformed code. This result demonstrates that early-stage checks                                                                                             and shared memory as the full system. AutoMedImg employs a
prevent costly downstream failures. Execution testing removal dra-                                                                                           multi-agent architecture to address the fundamental limitations of
matically increases HI by 3.50 with 4.5% performance degradation,                                                                                            single-agent systems in complex code generation: domain speciali-
representing the most critical validation for automated generation.                                                                                          sation, context management across phases, and parallel execution.
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                             ASE ’26, October 12–16, 2026, Munich, Germany


                            Table 3: Comparison of AutoMedImg with Automated Medical Imaging Methods

                                        Complete       Task Specific       Multi-task Cross-project Multi-stage Production-ready       Fully
                         Method
                                        Pipeline          Design            Support    Reference    Validation Implementation        Automated
                                                              ✗                                                                            ✗
                                             ✗
                         NAS [50]                        (Depend on            ✓           ✗             ✗             ✗           (Predefined search
                                         (NN only)
                                                        search space)                                                                space needed)
                                                                                                                                           ✗
                                                                               ✗
                         nnU-Net [18]       ✓                ✓                             ✗             ✗             ✓             (Manual setup
                                                                           (Seg. only)
                                                                                                                                       needed)
                                             ✗                ✗                                                                            ✗
                                                                               ✗
                         MedSAM [31]     (Inference   (Fixed pre-trained                   ✗             ✗             ✓              (Interactive
                                                                           (Seg. only)
                                            only)           model)                                                                     inference)

                         AutoMedImg         ✓                ✓                 ✓           ✓            ✓              ✓                  ✓


The Multi-Agent (M-Agent) category in Figure 5 demonstrates that                               solutions to be retrieved and adapted for future tasks, a capability
removing this architecture significantly degrades performance, val-                            absent in all prior work.
idating the necessity of this design choice.                                                      Qualitative Comparison with Medical Imaging Automa-
   Experiments on AutoMedImg with Claude-4.5-Opus demon-                                       tion. Table 3 compares AutoMedImg with automated approaches
strate that single-agent mode reduces performance by 10.2%, re-                                in medical imaging and related domains. Medical imaging automa-
quires 1.33 additional interventions, and adds 10 minutes generation                           tion methods (NAS, nnU-Net, MedSAM) incorporate domain ex-
time, illustrating three critical limitations: (1) Self-validation bias oc-                    pertise but address only partial pipeline components, requiring
curs when a single agent possesses both generation and validation                              manual setup or interactive inference. AutoMedImg is the only
knowledge, occasionally applying validation criteria during gen-                               approach that achieves complete pipeline generation, task-specific
eration then merely confirming its own decisions, allowing errors                              design, multi-task support, cross-project knowledge reuse, system-
to propagate unchecked. (2) Context compaction forces the agent                                atic multi-stage validation and full automation.
to eliminate earlier validated planning outputs when exceeding                                    Threats to validity. Despite its advantages, AutoMedImg has
context limits, causing information loss. (3) Sequential processing                            certain limitations: 1) Generalisation: AutoMedImg is designed
adds overhead as modules must be generated sequentially. Multi-                                specifically for medical image processing, with domain-specific
agent architecture addresses these limitations through role-based                              knowledge bases and agent configurations tailored to this domain.
agent separation ensuring independent oversight, phase-separated                               The core framework (multi-agent coordination, validation-based
context management preserving workflow history, and concurrent                                 context propagation, shared memory, adaptive synthesis) is how-
execution exploiting implementation parallelism.                                               ever domain-independent and can be extended to other domains
 Answer to RQ4: Multi-agent architecture is essential for auto-                                requiring systematic dataset analysis and pipeline construction, by
 mated specialised-domain code generation. Distributed coordina-                               constructing domain-specific KBs from relevant standards, defin-
 tion enables specialised reasoning that prevents knowledge con-                               ing domain-appropriate semantic validation criteria, and adapting
 fusion, preserves context history across multi-stage workflows,                               formal verification templates. Adapting to broader general code gen-
 and exploits parallel execution to improve workflow efficiency.                               eration tasks beyond data analysis pipelines could also inherit the
                                                                                               framework, but would additionally require adapting agent prompts.
                                                                                               2) Generation Overhead: Multi-agent coordination with iterative
                                                                                               validation incurs higher API costs and generation time compared
5    Discussion                                                                                to direct generation. In our experiments, a complete pipeline gen-
Qualitative Comparison with Code Generation Baselines. IDE                                     eration costs approximately $20–40 with an average runtime of 32
tools and vanilla LLMs possess strong code generation capability but                           minutes, negligible compared to manual development requiring
lack domain-specific conventions and built-in validation, resulting                            4–8 hours at $200–600.
in suboptimal pipeline designs and substantial human correction
overhead. Multi-agent frameworks provide effective inter-agent                                 6   Conclusion
cooperation but lack systematic validation and domain ground-                                  In this work, we present AutoMedImg, a multi-agent code genera-
ing, limiting their effectiveness on complex domain-specific tasks.                            tion framework for medical image processing with validation-based
AutoML frameworks offer pipeline automation but require manu-                                  context engineering. By employing multi-agent coordination, multi-
ally provided scaffolds for each new task type, constraining their                             stage validation, and comprehensive context integration encompass-
applicability to predefined task coverage. AutoMedImg addresses                                ing domain knowledge, shared memory, validation feedback, and
these limitations by instantiating base models within a multi-agent                            adaptive pipeline synthesis, AutoMedImg achieves fully automated
architecture augmented with domain KBs and systematic step-wise                                code generation across diverse medical imaging tasks. Evaluation
validation, eliminating the need for manually provided scaffolds                               demonstrates that AutoMedImg achieves zero human interven-
through a planning-validation workflow that dynamically synthe-                                tion while maintaining competitive performance. Future work will
sises task-appropriate pipelines. Furthermore, AutoMedImg distin-                              extend AutoMedImg to additional tasks such as image denoising
guishes itself across all categories through cross-project knowledge                           and registration, and explore improving algorithmic performance
accumulation via adaptive pipeline synthesis, enabling validated                               beyond code generation.
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                                          Zhao et al.


7    Data Availability                                                                    [21] Haolin Jin, Linghan Huang, Haipeng Cai, Jun Yan, Bo Li, and Huaming Chen. 2024.
                                                                                               From llms to llm-based agents for software engineering: A survey of current,
The artifacts that support the results discussed in this paper are                             challenges and future. arXiv preprint arXiv:2408.02479 (2024). doi:10.48550/arXiv.
available at: https://github.com/SeanCho1996/AutoMedImg.                                       2408.02479
                                                                                          [22] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura
                                                                                               Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al.
                                                                                               2023. Segment anything. In Proceedings of the IEEE/CVF international conference
References                                                                                     on computer vision. 4015–4026. doi:10.48550/arXiv.2304.02643
 [1] Anthropic. 2025. Introducing Claude Opus 4.5. https://www.anthropic.com/             [23] Zeki Kuş and Musa Aydin. 2024. MedSegBench: A comprehensive benchmark
     news/claude-opus-4-5                                                                      for medical image segmentation in diverse data modalities. Scientific Data 11, 1
 [2] Chetan Arora, John Grundy, and Mohamed Abdelrazek. 2024. Advancing require-               (2024), 1283. doi:10.1038/s41597-024-04159-2
     ments engineering through generative ai: Assessing the role of llms. In Generative   [24] Bennett Landman, Zhoubing Xu, Juan Igelsias, Martin Styner, Thomas Langerak,
     AI for Effective Software Development. Springer, 129–148. doi:10.1007/978-3-031-          and Arno Klein. 2015. Miccai multi-atlas labeling beyond the cranial vault–
     55642-5_6                                                                                 workshop and challenge. In Proc. MICCAI multi-atlas labeling beyond cranial
 [3] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk                          vault—workshop challenge, Vol. 5. Munich, Germany, 12. doi:10.7303/syn3193805
     Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le,           [25] Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard
     et al. 2021. Program synthesis with large language models. arXiv preprint                 Ghanem. 2023. CAMEL: Communicative Agents for "Mind" Exploration of Large
     arXiv:2108.07732 (2021). doi:10.48550/arXiv.2108.07732                                    Language Model Society. In Advances in Neural Information Processing Systems,
 [4] Olivier Bernard, Alain Lalande, Clement Zotti, Frederick Cervenansky, Xin Yang,           A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.), Vol. 36.
     Pheng-Ann Heng, Irem Cetin, Karim Lekadir, Oscar Camara, Miguel Angel Gon-                Curran Associates, Inc., 51991–52008. https://proceedings.neurips.cc/paper_files/
     zalez Ballester, et al. 2018. Deep learning techniques for automatic MRI cardiac          paper/2023/file/a3621ee907def47c1b952ade25c67698-Paper-Conference.pdf
     multi-structures segmentation and diagnosis: is the problem solved? IEEE transac-    [26] Haochen Li, Xin Zhou, and Zhiqi Shen. 2024. Rewriting the code: A simple
     tions on medical imaging 37, 11 (2018), 2514–2525. doi:10.1109/TMI.2018.2837502           method for large language model augmented code search. In Proceedings of the
 [5] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira              62nd Annual Meeting of the Association for Computational Linguistics (Volume
     Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman,           1: Long Papers). Association for Computational Linguistics, 1371–1389. doi:10.
     et al. 2021. Evaluating large language models trained on code. arXiv preprint             18653/v1/2024.acl-long.75
     arXiv:2107.03374 (2021). doi:10.48550/arXiv.2107.03374                               [27] Jia Li, Yunfei Zhao, Yongmin Li, Ge Li, and Zhi Jin. 2024. Acecoder: An effec-
 [6] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2023. Teaching               tive prompting technique specialized in code generation. ACM Transactions on
     large language models to self-debug. arXiv preprint arXiv:2304.05128 (2023).              Software Engineering and Methodology 33, 8 (2024), 1–26. doi:10.1145/3675395
     doi:10.48550/arXiv.2304.05128                                                        [28] Xiangrui Li, Paul S Morgan, John Ashburner, Jolinda Smith, and Christopher
 [7] Tristan Coignion, Clément Quinton, and Romain Rouvoy. 2024. A performance                 Rorden. 2016. The first step for neuroimaging data analysis: DICOM to NIfTI
     study of llm-generated code on leetcode. In Proceedings of the 28th international         conversion. Journal of neuroscience methods 264 (2016), 47–56. doi:10.1016/j.
     conference on evaluation and assessment in software engineering. 79–89. doi:10.           jneumeth.2016.03.001
     1145/3661167.3661221                                                                 [29] Geert Litjens, Robert Toth, Wendy Van De Ven, Caroline Hoeks, Sjoerd Kerkstra,
 [8] Google Deepmind. 2025. Gemini 3 Pro. https://deepmind.google/models/gemini/               Bram Van Ginneken, Graham Vincent, Gwenael Guillard, Neil Birbeck, Jindang
     pro/                                                                                      Zhang, et al. 2014. Evaluation of prostate segmentation algorithms for MRI: the
 [9] Jinghao Feng, Qiaoyu Zheng, Chaoyi Wu, Ziheng Zhao, Ya Zhang, Yanfeng Wang,               PROMISE12 challenge. Medical image analysis 18, 2 (2014), 359–373. doi:10.1016/
     and Weidi Xie. 2025. M 3 builder: A multi-agent system for automated machine              j.media.2013.12.002
     learning in medical imaging. In International Workshop on Agentic AI for Medicine.   [30] Yuqiao Liu, Yanan Sun, Bing Xue, Mengjie Zhang, Gary G Yen, and Kay Chen Tan.
     Springer, 115–124. doi:10.1007/978-3-032-06004-4_12                                       2021. A survey on evolutionary neural architecture search. IEEE transactions on
[10] Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang, Eric Wallace, Freda Shi,            neural networks and learning systems 34, 2 (2021), 550–570. doi:10.1109/TNNLS.
     Ruiqi Zhong, Wen-tau Yih, Luke Zettlemoyer, and Mike Lewis. 2022. Incoder: A              2021.3100554
     generative model for code infilling and synthesis. arXiv preprint arXiv:2204.05999   [31] Jun Ma, Yuting He, Feifei Li, Lin Han, Chenyu You, and Bo Wang. 2024. Segment
     (2022). doi:10.48550/arXiv.2204.05999                                                     Anything in Medical Images. Nature Communications 15 (2024), 654. doi:10.1038/
[11] Github. 2025. GitHub Copilot · Your AI pair programmer. https://github.com/               s41467-024-44824-z
     features/copilot                                                                     [32] Jun Ma, Yao Zhang, Song Gu, Xingle An, Zhihe Wang, Cheng Ge, Congcong
[12] Google. 2025. Introducing Google Antigravity, a New Era in AI-Assisted Software           Wang, Fan Zhang, Yu Wang, Yinan Xu, et al. 2022. Fast and low-GPU-memory
     Development. https://antigravity.google/blog/introducing-google-antigravity               abdomen CT organ segmentation: the flare challenge. Medical Image Analysis 82
[13] Siyuan Guo, Cheng Deng, Ying Wen, Hechang Chen, Yi Chang, and Jun Wang.                   (2022), 102616. doi:10.1016/j.media.2022.102616
     2024. Ds-agent: Automated data science by empowering large language models           [33] Jun Ma, Yao Zhang, Song Gu, Cheng Ge, Shihao Mae, Adamo Young, Cheng
     with case-based reasoning. arXiv preprint arXiv:2402.17453 (2024). doi:10.48550/          Zhu, Xin Yang, Kangkang Meng, Ziyan Huang, et al. 2024. Unleashing the
     arXiv.2402.17453                                                                          strengths of unlabelled data in deep learning-assisted pan-cancer abdominal
[14] Junda He, Christoph Treude, and David Lo. 2025. LLM-Based Multi-Agent Systems             organ quantification: the FLARE22 challenge. The Lancet Digital Health 6, 11
     for Software Engineering: Literature Review, Vision, and the Road Ahead. ACM              (2024), e815–e826. doi:10.1016/S2589-7500(24)00154-7
     Transactions on Software Engineering and Methodology 34, 5 (2025), 1–30. doi:10.     [34] Wei Ma, Zhihao Lin, Shangqing Liu, Qiang Hu, Ye Liu, Wenhan Wang, Cen Zhang,
     1145/3712003                                                                              Liming Nie, Li Li, Yang Liu, et al. 2026. Exploring Code Analysis: Zero-Shot
[15] Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng Cheng, Jinlin Wang, Ceyao                  Insights on Syntax and Semantics with LLMs. ACM Transactions on Software
     Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. 2023.              Engineering and Methodology (2026). doi:10.1145/3818607
     Metagpt: Meta programming for multi-agent collaborative framework. arXiv             [35] Vasilije Markovic, Lazar Obradovic, Laszlo Hajdu, and Jovan Pavlovic. 2025. Opti-
     preprint arXiv:2308.00352 (2023). doi:10.48550/arXiv.2308.00352                           mizing the interface between knowledge graphs and llms for complex reasoning.
[16] Andrew Hoopes, Neel Dey, Victor Ion Butoi, John V Guttag, and Adrian V Dalca.             arXiv preprint arXiv:2505.24478 (2025). doi:10.48550/arXiv.2505.24478
     2024. VoxelPrompt: A Vision Agent for End-to-End Medical Image Analysis.             [36] Peter Mildenberger, Marco Eichelberg, and Eric Martin. 2002. Introduction to
     arXiv preprint arXiv:2410.08397 (2024). doi:10.48550/arXiv.2410.08397                     the DICOM standard. European radiology 12, 4 (2002), 920–927. doi:10.1007/
[17] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming                 s003300101100
     Cui. 2023. Agentcoder: Multi-agent-based code generation with iterative testing      [37] Ansong Ni, Miltiadis Allamanis, Arman Cohan, Yinlin Deng, Kensen Shi, Charles
     and optimisation. arXiv preprint arXiv:2312.13010 (2023). doi:10.48550/arXiv.2312.        Sutton, and Pengcheng Yin. 2024. Next: Teaching large language models to reason
     13010                                                                                     about code execution. arXiv preprint arXiv:2404.14662 (2024). doi:10.48550/arXiv.
[18] Fabian Isensee, Paul F Jaeger, Simon AA Kohl, Jens Petersen, and Klaus H                  2404.14662
     Maier-Hein. 2021. nnU-Net: a self-configuring method for deep learning-              [38] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou,
     based biomedical image segmentation. Nature methods 18, 2 (2021), 203–211.                Silvio Savarese, and Caiming Xiong. 2022. Codegen: An open large language
     doi:10.1038/s41592-020-01008-z                                                            model for code with multi-turn program synthesis. arXiv preprint arXiv:2203.13474
[19] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2026. A                  (2022). doi:10.48550/arXiv.2203.13474
     survey on large language models for code generation. ACM Transactions on             [39] OpenAI. 2025. Introducing GPT-5.2. https://openai.com/index/introducing-gpt-
     Software Engineering and Methodology 35, 2 (2026), 1–72. doi:10.1145/3747588              5-2/
[20] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,    [40] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng
     and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve                    Yang, Weize Chen, Yusheng Su, Xin Cong, et al. 2024. Chatdev: Communicative
     Real-world Github Issues?. In The Twelfth International Conference on Learning            agents for software development. In Proceedings of the 62nd Annual Meeting of the
     Representations. https://openreview.net/forum?id=VTF8yNQM66                               Association for Computational Linguistics (Volume 1: Long Papers). 15174–15186.
Towards Fully Automated Medical Imaging Code Generation via Validation-Based Context Engineering                            ASE ’26, October 12–16, 2026, Munich, Germany


     doi:10.18653/v1/2024.acl-long.810                                                       International Conference on Machine Learning (Proceedings of Machine Learning
[41] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali,              Research, Vol. 267), Aarti Singh, Maryam Fazel, Daniel Hsu, Simon Lacoste-Julien,
     Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson,                  Felix Berkenkamp, Tegan Maharaj, Kiri Wagstaff, and Jerry Zhu (Eds.). PMLR,
     et al. 2024. Sam 2: Segment anything in images and videos. arXiv preprint               60099–60146. https://proceedings.mlr.press/v267/trirat25a.html
     arXiv:2408.00714 (2024). doi:10.48550/arXiv.2408.00714                             [50] Yan Wang, Liangli Zhen, Jianwei Zhang, Miqing Li, Lei Zhang, Zizhou Wang,
[42] Pengzhen Ren, Yun Xiao, Xiaojun Chang, Po-Yao Huang, Zhihui Li, Xiaojiang               Yangqin Feng, Yu Xue, Xiao Wang, Zheng Chen, et al. 2024. Mednas: Multiscale
     Chen, and Xin Wang. 2021. A comprehensive survey of neural architecture                 training-free neural architecture search for medical image analysis. IEEE Trans-
     search: Challenges and solutions. ACM Computing Surveys (CSUR) 54, 4 (2021),            actions on Evolutionary Computation 28, 3 (2024), 668–681. doi:10.1109/TEVC.
     1–34. doi:10.1145/3447582                                                               2024.3352641
[43] Jiho Shin, Clark Tang, Tahmineh Mohati, Maleknaz Nayebi, Song Wang, and Hadi       [51] Jiancheng Yang, Rui Shi, Donglai Wei, Zequan Liu, Lin Zhao, Bilian Ke, Hanspeter
     Hemmati. 2025. Prompt Engineering or Fine-Tuning: An Empirical Assessment               Pfister, and Bingbing Ni. 2023. Medmnist v2-a large-scale lightweight benchmark
     of LLMs for Code. In 2025 IEEE/ACM 22nd International Conference on Mining              for 2d and 3d biomedical image classification. Scientific Data 10, 1 (2023), 41.
     Software Repositories (MSR). IEEE, 490–502. doi:10.1109/MSR66628.2025.00082             doi:10.1038/s41597-022-01721-8
[44] LLM Stats. 2026. MBPP Leaderboard. https://llm-stats.com/benchmarks/mbpp           [52] Zixiao Zhao, Jing Sun, Zhe Hou, Zhiyuan Wei, Cheng-Hao Cai, Miao Qiao, and
[45] SWE-bench. 2026. SWE-bench Leaderboard. https://www.swebench.com/                       Jin Song Dong. 2024. MaCTG: Multi-Agent Collaborative Thought Graph for
[46] Zhengwei Tao, Ting-En Lin, Xiancai Chen, Hangyu Li, Yuchuan Wu, Yongbin                 Automatic Programming. arXiv preprint arXiv:2410.19245 (2024). doi:10.48550/
     Li, Zhi Jin, Fei Huang, Dacheng Tao, and Jingren Zhou. 2024. A survey on                arXiv.2410.19245
     self-evolution of large language models. arXiv preprint arXiv:2404.14387 (2024).   [53] Alex P Zijdenbos, Benoit M Dawant, Richard A Margolin, and Andrew C Palmer.
     doi:10.48550/arXiv.2404.14387                                                           1994. Morphometric analysis of white matter lesions in MR images: method
[47] Cursor Team. 2024. Cursor Docs. https://cursor.com/docs                                 and validation. IEEE transactions on medical imaging 13, 4 (1994), 716–724.
[48] Price Per Token. 2026. HumanEval Leaderboard. https://pricepertoken.com/                doi:10.1109/42.363096
     leaderboards/benchmark/humaneval
[49] Patara Trirat, Wonyong Jeong, and Sung Ju Hwang. 2025. AutoML-Agent: A             Received 2026-03-26; accepted 2026-06-18
     Multi-Agent LLM Framework for Full-Pipeline AutoML. In Proceedings of the 42nd
