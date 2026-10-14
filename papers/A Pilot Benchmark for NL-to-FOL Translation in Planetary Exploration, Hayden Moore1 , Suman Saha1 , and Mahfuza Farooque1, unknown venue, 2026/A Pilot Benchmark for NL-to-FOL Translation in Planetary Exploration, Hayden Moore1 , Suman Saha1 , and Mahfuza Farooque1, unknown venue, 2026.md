                                         A Pilot Benchmark for NL-to-FOL Translation in Planetary Exploration
                                                                              Hayden Moore1 , Suman Saha1 , and Mahfuza Farooque1


                                            Abstract— Future planetary exploration envisions au-
                                         tonomous robotic agents operating under severe communica-
                                         tion constraints, without global positioning, and with minimal
                                         human intervention. In such environments, agents must not
                                         only perceive and act, but also reason over mission objectives,
                                         operational constraints, and evolving environmental conditions.
                                         While prior work has largely focused on perception and control,
arXiv:2605.17911v1 [cs.CL] 18 May 2026




                                         the translation of high-level mission knowledge into structured,
                                         machine-interpretable representations remains underexplored.
                                            We introduce a pilot benchmark for translating natural
                                         language (NL) into First-Order Logic (FOL) within the domain
                                         of planetary exploration. The dataset is constructed from real
                                         mission documentation sourced from NASA’s Planetary Data
                                         System (PDS), spanning missions from 2003 to 2013. These                    Fig. 1.     Conceptual setting motivating this work. In long-duration,
                                         documents describe mission phases such as launch, boost,                    communication-constrained planetary exploration, an autonomous agent
                                         coast, cruise, and orbital operations in rich natural language.             cannot rely on continuous connectivity to Earth and must instead use
                                         We manually annotate these documents with corresponding                     onboard mission documents and internal reasoning to interpret mission
                                         FOL representations that capture temporal structure, agent                  phases, understand constraints, and make decisions while interacting with
                                         roles, and operational dependencies. In addition, we provide                its environment.
                                         structured predicate vocabularies and typed constants to
                                         enable controlled experimentation with varying levels of
                                         prior knowledge. This pilot benchmark provides a foundation                 mission knowledge is specified and how it can be consumed
                                         for research at the intersection of language understanding                  by autonomous systems.
                                         and formal reasoning, grounded in real-world, safety-critical
                                         mission data. The dataset is provided at: https://github.                      Bridging this gap requires transforming high-level natural
                                         com/HaydenMM/planetary-logic-benchmark/blob/                                language descriptions into structured, machine-interpretable
                                         main/pilot_benchmark.json.                                                  representations. First-Order Logic (FOL) provides a natural
                                                                                                                     candidate for this transformation, offering a formal frame-
                                                               I. INTRODUCTION                                       work for representing entities, relations, and temporal de-
                                                                                                                     pendencies. Despite its relevance, the problem of translating
                                            Autonomous robotic systems are expected to play a central                natural language mission descriptions into FOL has received
                                         role in the next generation of planetary exploration [1].                   limited attention, particularly in domains characterized by
                                         Unlike terrestrial systems, these agents must operate under                 long-horizon temporal reasoning and complex operational
                                         extreme constraints, including delayed or intermittent com-                 structure [3], [4], [5], [6], [7]. Figure 1 illustrates the
                                         munication with Earth [2], limited onboard computational                    motivating setting for this benchmark, where an autonomous
                                         resources, and the absence of global positioning systems. In                planetary agent must reason over onboard mission knowledge
                                         such conditions, autonomy is not merely a convenience but                   under communication constraints.
                                         a necessity. Agents must interpret mission objectives, reason                  In this work, we introduce a pilot benchmark designed
                                         about evolving environmental conditions, and make decisions                 to support research on this problem. Our goal is to provide
                                         that are both safe and effective without continuous human                   a dataset that captures the richness and complexity of real
                                         oversight.                                                                  planetary mission documentation while enabling systematic
                                            A key challenge in achieving this level of autonomy                      exploration of natural language to logical representation.
                                         lies in how mission knowledge is represented and utilized.                  Rather than focusing on evaluating specific models, we posi-
                                         In current practice, mission plans, operational procedures,                 tion this benchmark as a foundational resource for studying
                                         and system constraints are largely expressed in natural lan-                the interaction between language understanding and formal
                                         guage. These descriptions contain rich information about                    reasoning in safety-critical planetary exploration environ-
                                         temporal sequences, dependencies between subsystems, and                    ments. This complements prior work in autoformalization
                                         conditional behaviors. However, natural language lacks the                  and structured translation tasks [5], [6], [7].
                                         precision and structure required for reliable execution and
                                         formal reasoning. As a result, there is a gap between how                                 II. DATASET CONSTRUCTION

                                           1 Department of Computer Science and Engineering, College of Engi-
                                                                                                                        The dataset is constructed from publicly available mis-
                                         neering, The Pennsylvania State University, University Park, Pennsylvania   sion documentation provided by NASA’s Planetary Data
                                         16802, USA: hmm5731@psu.edu                                                 System (PDS) [8]. These documents are written for sci-
entific and operational purposes and contain detailed de-             StartsAfterMinutesApprox(b, e, 0)           ∧
scriptions of mission phases, system behaviors, and obser-            DurationMinutesApprox(b, 10))
vational activities. As such, they provide a realistic and            ∧∃c (CoastPhase(c) ∧ Agent(c, Spirit MER2) ∧
challenging source of natural language data for structured            InOrbit(c, ParkingOrbit)                    ∧
reasoning tasks. The full dataset is available for anonymous          StartsAfterMinutesApprox(c, b, 0)           ∧
review at: https://anonymous.4open.science/r/                         DurationMinutesApprox(c, 15) ∧ After(c, b))
PMR-BF96/mission.json.                                                ∧∃d (DespinEvent(d) ∧ Agent(d, Spirit MER2) ∧
   We collect mission documents spanning the period from              After(d, ThirdStageBurnout)                 ∧
2003 to 2013, covering a diverse set of planetary missions            Uses(d, YoYoDespinSystem)                   ∧
and operational contexts. Each document describes the pro-            ActsOn(d, UpperStageStack))
gression of a mission through multiple phases, including              ∧∃s               (ThirdStageSeparation(s)  ∧
launch, boost, coast, cruise, orbit insertion, and science            Agent(s, Spirit MER2)                       ∧
operations. These phases vary in duration from minutes to             AfterMinutesApprox(s, e, 36))
years and often involve nested temporal relationships and
                                                                    Beyond the paired natural language and FOL represen-
interdependent activities. The resulting dataset captures both
                                                                 tations, the dataset includes additional structure that sup-
short-duration procedural events and long-horizon mission
                                                                 ports controlled experimentation. Predicate vocabularies are
planning, providing a broad range of reasoning challenges.
                                                                 extracted and standardized across all documents, providing
   Each document is manually translated into a corresponding     a consistent set of logical primitives. Constants are sepa-
FOL representation. This annotation process is designed to       rated and typed according to their semantic roles, including
preserve the semantic content of the original text while         entities, temporal values, and numerical quantities. This
making its structure explicit. Temporal relationships are        separation allows the dataset to be used in settings with
encoded using predicates that capture ordering, duration, and    varying degrees of prior knowledge, such as scenarios where
dependency, allowing events to be composed into coherent         the logical vocabulary is fixed or where type information is
logical sequences. Agent roles are explicitly represented,       available to guide parsing.
distinguishing between spacecraft, subsystems, instruments,
and external entities such as ground stations. Operational ac-
tivities, such as maneuvers, observations, and system checks,                  III. BENCHMARK DESIGN
are modeled as predicates that relate agents, actions, and
outcomes.
                                                                    The pilot benchmark is defined as the task of translating
   An example from the dataset illustrates the level of detail
                                                                 natural language mission descriptions into First-Order Logic
captured in these annotations. The following excerpt shows a
                                                                 representations. This task requires capturing not only the
natural language description of a launch sequence alongside
                                                                 meaning of individual statements but also the composi-
its corresponding First-Order Logic representation:
                                                                 tional structure that arises from temporal dependencies and
Natural Language:
                                                                 operational constraints. Unlike traditional semantic parsing
                                                                 tasks, which often focus on short and relatively independent
     Spirit (MER-2 hardware) was launched June 10,               utterances, this benchmark involves longer documents with
     2003, at 1759 UTC (1359 EDT) from launch                    interconnected events and hierarchical structure.
     complex 17A at Cape Canaveral Air Force Station,               A central feature of the benchmark is its modular design.
     Florida. The launch azimuth was 93 degrees. The             By explicitly separating predicate vocabularies and typed
     boost portion of the launch vehicle trajectory took         constants from the core annotations, the dataset enables
     approximately 10 minutes, and was followed by a             researchers to explore different problem formulations. In
     short coast phase in a parking orbit for approxi-           one setting, models may be required to generate fully un-
     mately 15 minutes. After third stage burnout, the           constrained logical forms directly from natural language. In
     upper stage despun the stack using a yo-yo despin           another, models may operate within a predefined schema,
     system. Separation of the third stage occurred              leveraging known predicates and type constraints to guide
     approximately 36 minutes after launch.                      the translation process. These variations allow for systematic
First-Order Logic:                                               investigation of how structure and prior knowledge influence
                                                                 performance.
     ∃e (LaunchEvent(e) ∧ Agent(e, Spirit MER2) ∧                   The benchmark is intentionally agnostic to specific eval-
     DateUTC(e,′ 2003-06-10′ )                    ∧              uation protocols. Instead, it is designed to support a range
     TimeUTC(e,′ 17:59′ )                         ∧              of research directions, including symbolic methods that rely
     LocalTime(e,′ 13:59′ ) ∧ LocalTZ(e,′ EDT ′ ) ∧              on rule-based parsing, neural approaches that learn mappings
     From(e, LaunchComplex17A)                    ∧              from data, and hybrid methods that combine both paradigms
     At(e, CapeCanaveralAFS) ∧ In(e, Florida) ∧                  [9], [10]. By focusing on the dataset itself, we aim to
     AzimuthDeg(e, 93))                                          provide a flexible foundation that can be adapted to different
     ∧∃b (BoostPhase(b) ∧ Agent(b, Spirit MER2) ∧                experimental goals.
        IV. MOTIVATION AND APPLICATION                              numeric constants average 4.6, reflecting the prevalence of
   The motivation for this pilot benchmark is rooted in the         temporal durations, orbital parameters, and measurement
operational requirements of future autonomous planetary             values in mission descriptions.
systems. In scenarios where communication delays prevent               The dataset also exhibits significant variability in complex-
real-time human intervention, agents must rely on internal          ity. Natural language inputs range from short procedural de-
representations of mission knowledge to make decisions.             scriptions (84 words) to long, multi-phase mission narratives
These representations must be both expressive enough to             (over 400 words). Correspondingly, FOL representations
capture complex behaviors and structured enough to support          vary in both depth and breadth, with predicate vocabularies
reliable reasoning.                                                 ranging from 17 to 50 per example and predicate mentions
   First-Order Logic offers a formalism that satisfies these        ranging from 27 to 65. Quantifier counts range from 5 to
requirements. In the context of planetary rover autonomy,           25, further emphasizing differences in logical nesting and
this capability enables several concrete functions. Struc-          compositional depth across mission segments.
tured logical representations derived from natural language            An analysis of predicate usage reveals consistent struc-
mission descriptions can be used to define constraints for          tural patterns across examples. The most frequent predicates
semantic mapping, inform task planning and scheduling,              include During (42 occurrences), Agent (26), DateUTC
enforce safety conditions during navigation, and support            (13), and temporal relation predicates such as StartsAt,
verification and validation (V&V) of autonomous decisions.          EndsAt, and After. These distributions highlight the
By grounding high-level mission intent in formal repre-             central role of temporal reasoning and agent-centric event
sentations, autonomous systems can more reliably interpret          modeling in the dataset.
objectives, reason over constraints, and ensure that executed          Overall, these statistics indicate that the benchmark cap-
actions remain consistent with mission requirements.                tures both linguistic and logical complexity, combining long-
   The benchmark also has implications beyond planetary             form natural language descriptions with deeply structured
exploration. Many domains require the translation of natural        formal representations. The diversity in predicate vocab-
language into structured representations, including robotics,       ularies, temporal constructs, and entity types makes this
aerospace systems, and industrial automation. In these set-         dataset well-suited for studying compositional generaliza-
tings, the ability to bridge language and logic can enable          tion and structured reasoning in realistic, safety-critical and
more interpretable and reliable systems. By grounding this          planetary exploration domains. Table I summarizes the main
problem in real-world mission data, the benchmark provides          dataset-level statistics, including natural language length,
a realistic testbed for developing and evaluating such capa-        FOL length, predicate usage, quantifier count, and entity
bilities [11], [12].                                                constants.

             V. BENCHMARK STATISTICS                                        Statistic                      Mean     Range
   The pilot benchmark currently consists of 11 multi-phase                 NL Length (words)              257.6    84–412
mission segments in natural language (NL) and their cor-                    FOL Length (tokens)            286.9   174–434
responding First-Order Logic (FOL). These examples are                      Predicate Mentions              43.4    27–65
derived from 5 unique planetary mission sources spanning                    Unique Predicates / Example     30.3    17–50
                                                                            Quantifiers                     13.0     5–25
NASA Planetary Data System (PDS) documentation from
                                                                            Entity Constants                12.2     6–18
2003 to 2013. Across the dataset, we identify 251 unique
predicate signatures and 125 distinct entity constants, along                                  TABLE I
with 16 date literals, 13 time literals, and 51 numeric                 S UMMARY STATISTICS OF THE NL–FOL PILOT BENCHMARK .
values. This reflects both the semantic diversity of mission
descriptions and the structured variability required for formal
reasoning.
   The natural language inputs are moderately long and                            VI. PRELIMINARY RESULTS
descriptive, with an average length of 257.6 words (median            To provide an initial characterization of the pilot
249), ranging from 84 to 412 words. The corresponding FOL           benchmark, we conducted exploratory experiments
representations are similarly expressive, averaging 286.9           using a set of publicly available local language
tokens (median 288), with lengths ranging from 174 to 434           models, including Qwen/Qwen1.5-1.8B-Chat [13],
tokens. This near parity in NL and FOL length highlights            mistralai/Mistral-7B-Instruct-v0.3                   [14],
that the translation task preserves substantial structural detail   microsoft/Phi-3-mini-4k-instruct                     [15],
rather than compressing information into shallow forms.             meta-llama/Meta-Llama-3.1-8B-Instruct [16],
   At the logical level, each example contains an average           and google/gemma-2-9b-it [17]. For each model,
of 43.4 predicate mentions and 13.0 quantifiers, indicating         we provided the full natural language mission description
a high degree of compositional structure. The number of             as input and prompted the model to directly generate
unique predicates per example averages 30.3, suggesting that        a corresponding First-Order Logic (FOL) representation
each mission segment introduces a rich and varied set of            without additional explanation or intermediate steps. All
relations. Entity constants average 12.2 per example, while         model outputs were fixed to a maximum of 500 tokens.
   This setup represents a straightforward, unconstrained            representations deviate significantly from the ground truth in
translation task and is not intended to reflect optimized            both syntax and structure.
prompting or system design. Rather, it serves as a baseline             These preliminary results highlight the difficulty of direct,
to illustrate the challenges posed by long-form, structured          single-pass translation from long-form natural language into
mission descriptions.                                                structured logical representations. They suggest that more
   Across all models, we observe consistent failure modes.           effective approaches will likely require decomposition strate-
First, models struggle to maintain temporal and logical              gies, such as breaking mission descriptions into smaller units,
consistency over long sequences, often producing incomplete          as well as structured prompting techniques. Potential direc-
or incoherent event structures. Temporal relationships such          tions include few-shot prompting with schema constraints,
as ordering, duration, and dependency are frequently omitted,        guided decoding with formal grammars, and hybrid neuro-
misrepresented, or contradicted within the generated outputs.        symbolic pipelines that enforce logical consistency during
Second, models tend to miss critical components embedded             generation [18], [19], [20].
within the natural language descriptions, particularly when             We emphasize that these experiments are not
these components appear in later portions of the text or             intended as a comprehensive evaluation, but rather
are nested within complex sentences. Third, hallucination            as an initial demonstration of the challenges inherent
is prevalent, with models introducing predicates, entities, or       in this pilot benchmark. All raw model outputs are
relationships that are not grounded in the input description.        available     at:   https://github.com/HaydenMM/
These issues are amplified by the length and compositional           planetary-logic-benchmark/blob/main/
structure of the task, which requires sustained reasoning            pilot_benchmark_output.txt.
across multiple interconnected events.
   Some of the models demonstrate improved fluency and                                   VII. LIMITATIONS
partial structure, but still fail to reliably capture the full set      While this work introduces a curated pilot benchmark
of temporal dependencies and operational constraints present         for NL-to-FOL translation in planetary exploration, several
in the source text. Notably, even when local consistency is          limitations should be noted.
maintained within short segments, global coherence across               First, the dataset is small in scale, consisting of 11
the full mission sequence remains a challenge.                       mission segments derived from 5 unique sources. This work
   Model-specific behaviors further highlight these limita-          should therefore be viewed as a pilot benchmark intended
tions. Qwen [13] frequently fails to produce valid FOL               to motivate further data collection and expansion. Second,
representations and instead hallucinates by outputting natural       the annotations are manually constructed, which introduces
language instructions or step-by-step procedural descriptions.       potential subjectivity in how natural language descriptions
Mistral [14] and Meta-LLaMA-3.1 [16] demonstrate stronger            are mapped to logical representations. Third, the evaluation
alignment with the task and are more likely to attempt FOL-          presented in this work is preliminary and qualitative in
like structures, but still tend to generate ordered lists of         nature. Future work should explore quantitative evaluation
components that require additional processing to convert into        methods, including structural similarity, logical equivalence,
valid logical forms. Interestingly, while these enumerated           and execution-based validation. Finally, the experimental
outputs are incorrect with respect to the target format, they        setup relies on direct, single-pass generation with a fixed
often preserve temporal sequencing (e.g., step-wise progres-         output length constraint. This setting does not reflect more
sion), which partially maintains logical ordering despite not        advanced prompting strategies, decomposition methods, or
being explicitly requested.                                          constrained decoding approaches that may significantly im-
   Microsoft Phi-3 [15] exhibits severe hallucination behav-         prove performance.
ior, frequently introducing unrelated space or NASA con-                Despite these limitations, we believe this benchmark pro-
cepts not present in the input (e.g., references to the Hubble       vides a useful starting point for studying the intersection of
Space Telescope). In addition, it often repeats hallucinated         natural language understanding and formal reasoning in long-
temporal statements such as “Launch-40 min” and generates            horizon, structured environments.
redundant natural language outputs describing tasks rather
than producing FOL. These repetitions further degrade output                            VIII. CONCLUSION
quality and consistency.                                                We present a pilot benchmark for translating natural
   In addition, Google Gemma [17] occasionally failed to             language mission descriptions into First-Order Logic, con-
produce any output when given the full mission descriptions,         structed from real-world planetary mission documentation.
returning either empty responses or terminating generation           The dataset captures the complexity of mission phases,
prematurely. This behavior was observed more frequently for          temporal dependencies, and operational constraints, and aug-
longer inputs and suggests limitations in handling extended          ments these representations with structured predicate vocab-
context windows or internal decoding constraints under long-         ularies and typed constants. By focusing on the problem
form generation.                                                     of translating high-level mission knowledge into formal
   Among the evaluated models, Meta-LLaMA-3.1 show the               representations, this work highlights an important direction
strongest ability to produce structured FOL-like outputs in          for enabling interpretable and verifiable autonomy. We hope
some cases. However, even in these instances, the generated          this pilot benchmark will serve as a foundation for future
research at the intersection of language understanding and
formal reasoning in complex, real-world environments.
                            R EFERENCES
 [1] S. Chien et al., “The EO-1 Autonomous Science Agent,” in Proc. Int.
     Joint Conf. Autonomous Agents and Multiagent Systems (AAMAS),
     2004.
 [2] K. Fall, “A delay-tolerant network architecture for challenged inter-
     nets,” in Proc. ACM SIGCOMM, 2003.
 [3] L. S. Zettlemoyer and M. Collins, “Learning to map sentences to
     logical form,” in Proc. UAI, 2005.
 [4] A. Kamath and R. Das, “A survey on semantic parsing,” arXiv preprint
     arXiv:1812.00978, 2018.
 [5] H. Moore and A. Shah, “Evaluating Autoformalization Robustness
     via Semantically Similar Paraphrasing,” in AAAI 2026 Bridge LM-
     Reasoning Workshop.
 [6] M. Safarzadeh, A. Oroojlooyjadid, and D. Roth, “Evaluating NL2SQL
     via SQL2NL,” EMNLP, 2025.
 [7] S. Han, X. Guo, J. Chen, and X. Sun, “FOLIO: Natural Language
     Reasoning with First-Order Logic,” in Proc. EMNLP, 2024.
 [8] NASA Planetary Data System (PDS), “Planetary Data System,” 2024.
     [Online]. Available: https://pds.nasa.gov/
 [9] P. Yin and G. Neubig, “A syntactic neural model for general-purpose
     code generation,” in Proc. ACL, 2017.
[10] A. d’Avila Garcez et al., “Neural-symbolic computing: An effective
     methodology for principled integration of machine learning and rea-
     soning,” arXiv, 2019.
[11] P. Rajpurkar et al., “SQuAD: 100,000+ questions for machine com-
     prehension of text,” in Proc. EMNLP, 2016.
[12] S. W. Squyres et al., “The Opportunity Rover’s Athena science
     investigation at Meridiani Planum, Mars,” Science, 2004.
[13] Qwen Team, “Qwen1.5: Open foundation models,” 2024. [Online].
     Available: https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat
[14] A. Mistral AI, “Mistral-7B-Instruct-v0.3,” 2024. [Online]. Available:
     https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3
[15] Microsoft, “Phi-3: Technical report,” 2024. [Online]. Available:
     https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
[16] Meta AI, “LLaMA 3.1: Open and efficient foundation models,”
     2024. [Online]. Available: https://huggingface.co/meta-llama/Meta-
     Llama-3.1-8B-Instruct
[17] Google       DeepMind,       “Gemma:       Open      models     based
     on       Gemini      research,”     2024.     [Online].     Available:
     https://huggingface.co/google/gemma-2-9b-it
[18] J. Wei et al., “Chain-of-Thought prompting elicits reasoning in large
     language models,” in Proceedings of the 36th International Conference
     on Neural Information Processing Systems (NIPS), 2022.
[19] N. F. Liu et al., “Lost in the middle: How language models use long
     contexts,” Trans. ACL, 2024.
[20] Y. Bang et al., “A multitask, multilingual, multimodal evaluation of
     ChatGPT,” in Proceedings of the 13th International Joint Conference
     on Natural Language (IJCNLP), 2023
