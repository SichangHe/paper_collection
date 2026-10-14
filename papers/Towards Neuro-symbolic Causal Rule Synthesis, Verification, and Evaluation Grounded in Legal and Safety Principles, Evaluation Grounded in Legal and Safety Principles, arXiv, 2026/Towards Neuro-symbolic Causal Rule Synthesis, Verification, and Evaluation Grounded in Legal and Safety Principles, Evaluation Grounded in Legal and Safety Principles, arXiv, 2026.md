                                         Towards Neuro-symbolic Causal Rule Synthesis, Verification, and
                                              Evaluation Grounded in Legal and Safety Principles
                                                                          Zainab Rehan                                                        Christian Medeiros Adriano
                                                                   Hasso Plattner Institute                                                         Hasso Plattner Institute
                                                                    University of Potsdam                                                           University of Potsdam
                                                                     Potsdam, Germany                                                                 Potsdam, Germany
                                                                zainab.rehan@uni-potsdam.de                                                        christian.adriano@hpi.de

                                                                       Sona Ghahremani                                                                  Holger Giese∗
                                                                     Hasso Plattner Institute                                                       Hasso Plattner Institute
arXiv:2604.28087v2 [cs.LO] 11 May 2026




                                                                      University of Potsdam                                                         University of Potsdam
                                                                       Potsdam, Germany                                                               Potsdam, Germany
                                                                    sona.ghahremani@hpi.de                                                           holger.giese@hpi.de

                                         ABSTRACT                                                                                1    INTRODUCTION
                                         Rule-based systems remain central in safety-critical domains but                        Context – Rule-based systems [33] are specified and constructed
                                         often struggle with scalability, brittleness, and goal misspecifica-                    from existing domain knowledge about desired and undesired (for-
                                         tion. These limitations can lead to reward hacking and failures                         bidden, unsafe) behavior, often as logical if–then statements. Rule-
                                         in formal verification, as AI systems tend to optimize for narrow                       based approaches remain central in many safety- and mission-
                                         objectives. In previous research, we developed a neuro-symbolic                         critical contexts because rules make system behavior observable at
                                         causal framework that integrates first-order logic abduction trees,                     runtime and open to formal verification [22, 36].
                                         structural causal models, and deep reinforcement learning within a                         In self-adaptive and autonomic systems, the MAPE-K feedback
                                         MAPE-K loop to provide explainable adaptations under distribution                       loop [27] represents monitoring, analysis, planning, and execution
                                         shifts. In this paper, we extend that framework by introducing a                        as activities over a shared knowledge base (of rules and represen-
                                         meta-level layer designed to mitigate goal misspecification and sup-                    tation models). These systems often rely on runtime enforcement
                                         port scalable rule maintenance. This layer consists of a Goal/Rule                      components that supervise primary controllers and trigger prede-
                                         Synthesizer and a Rule Verification Engine, which iteratively refine                    fined mitigation actions when rules are violated [10, 36].
                                         a formal rule theory from high-level natural-language goals and                            Challenges – However, rule-based and expert systems are widely
                                         principles provided by human experts. The synthesis pipeline em-                        recognized for their brittleness and limited scalability. As new
                                         ploys large language models (LLMs) to: (1) decompose goals into                         requirements emerge, even minor changes can cause cascading
                                         candidate causes, (2) consolidate semantics to remove redundancies,                     revisions across numerous interdependent rules. Managing and
                                         (3) translate them into candidate first-order rules, and (4) compose                    tracking these evolving rules places a significant cognitive and or-
                                         necessary and sufficient causal sets. The verification pipeline then                    ganizational burden on human experts, often becoming a central
                                         performs (1) syntax and schema validation, (2) logical consistency                      bottleneck and increasing the risk of unexpected failures [20, 36].
                                         analysis, and (3) safety and invariant checks before integrating                        Classic analyses of earlier expert systems highlight the exponential
                                         verified rules into the knowledge base. We evaluated our approach                       increase in maintenance effort and the well-known “knowledge
                                         with a proof-of-concept implementation in two autonomous driving                        acquisition bottleneck.” In practice, large rule sets are inherently dif-
                                         scenarios. Results indicate that, given human-specified goals and                       ficult to extend or adapt without unintentionally disrupting existing
                                         principles, the pipeline can successfully derive minimal necessary                      behaviors [20, 36]. These issues were prominent in large, early AI
                                         and sufficient rule sets and formalize them as logical constraints.                     expert-system projects, which helped motivate later shifts toward
                                         These findings suggest that the pipeline supports incremental, mod-                     methods that combine statistical learning with more scalable forms
                                         ular, and traceable rule synthesis grounded in established legal and                    of knowledge representation [31, 36].
                                         safety principles.                                                                         Approach – We extend a prior neuro-symbolic causal frame-
                                                                                                                                 work for self-adaptive, learning-enabled systems[1, 2] with a meta-
                                         KEYWORDS                                                                                level synthesis and verification layer that incrementally refines
                                         Rule synthesis, Neuro-symbolic methods, Software verification,                          the governing rule theory. A Goal/Rule Synthesizer uses large lan-
                                         Causality, Goal specification                                                           guage models to decompose high-level, natural-language goals and
                                                                                                                                 principles into candidate causes, consolidate their semantics, and
                                                                                                                                 translate them into candidate first-order rules while identifying
                                         ∗ IEEE and ACM Member
                                                                                                                                 necessary and sufficient cause sets. A complementary Rule Verifi-
                                                                                                                                 cation Engine then enforces syntax and schema correctness, logical
                                                                                                                                 consistency, and safety and invariant constraints before integrating
                                         Proc. of the Neurosymbolic eXplainable Trustworthy Systems Workshop (NEXUS 2026),
                                         Bakirtzis, Fridovich-Keil , Kakas, Theodorou, Li, McKinlay (eds.), May 25 – 26, 2026,
                                         Paphos, Cyprus,https://nexus.telecom-paris.fr. 2026.
only verified rules into the knowledge base. Together, these compo-           Causal-Neuro-Symbolic Reasoning - Causal neuro-symbolic
nents realize an incremental, modular, and traceable pipeline from        AI combines the strengths of causal inference, symbolic reason-
human-specified legal and safety principles to formally verified          ing, and deep learning to produce models that are both adaptable
rule sets, demonstrated on autonomous driving scenarios.                  and explanatory [26]. In such hybrid frameworks, symbolic struc-
   Evaluation – We present an application in the domain of au-            tures (e.g., causal graphs or abduction trees) provide interpretable
tonomous driving, where safety goals are systematically decom-            scaffolding for interventions and counterfactual reasoning while
posed into subgoals and translated into corresponding rules. The          neural components supply flexible function approximation for per-
mapping between goals and rules is realized via simulated abduction       ception and policy learning. Complementary approaches investi-
that produces explanations of an effect from its causes, while rule re-   gate confidence-aware semantic mapping approaches that integrate
finement is performed through deductive reasoning, de-duplicating         uncertainty-aware perception with symbolic spatial representations
rules and combining them into necessary and sufficient sets. We           for autonomous navigation and reasoning under uncertain obser-
evaluated our approach with a proof-of-concept implementation             vations [29]. Recent work demonstrates how causal abstractions
in two autonomous driving scenarios, showing that, given human-           can be learned or exploited by agents to accelerate adaptation and
specified goals and principles, the pipeline can successfully derive      to ground symbolic recovery strategies in measurable causal ef-
minimal necessary and sufficient rule sets and formalize them as          fects [26, 30]. Applications in multi-agent reinforcement learning
logical constraints. These findings suggest that the pipeline sup-        show further promise: transferable macro-actions or recovery prim-
ports incremental, modular, and traceable rule synthesis grounded         itives can be represented as compact causal rules that capture cause
in established legal and safety principles.                               & effect pathways linking failures to corrective actions, enabling
   Contributions – By structuring rule maintenance as an incre-           agents to exchange and re-use causal knowledge across contexts
mental, meta-level synthesis-and-verification loop, the approach          [30, 44]. Integrating such transferable causal experiences into sym-
directly attacks the scalability and brittleness problems of classic      bolic abduction structures enriches the abductive search space with
rule-based systems. First, high-level goals are decomposed into           empirical, distributed evidence, thereby improving both the quality
modular sets of necessary and sufficient rules per goal, so exten-        of synthesized rules and their generalizability across agents and
sions localize to specific goal-linked modules instead of triggering      environments.
cascading revisions across a monolithic rule base. Second, semantic           Knowledge Representation in Rule-based Systems Rule-
consolidation, de-duplication, and explicit traceability from each        based systems and first-order logic support complex and common-
rule back to its originating goal and principles reduce redundancy        sense reasoning but often incur high computational costs [28, 35].
and make large rule sets easier to understand, audit, and evolve.         To improve scalability, global theories are partitioned into context-
Third, the Rule Verification Engine systematically filters new rules      specific modules, enabling local reasoning while maintaining over-
through syntax, consistency, and safety checks before reintegration,      all consistency [7, 12, 37]. Techniques such as monotonic and non-
preventing brittle, ad hoc patches and enabling controlled growth         monotonic reasoning, syntax splitting, modular answer set pro-
of the theory over time. Reproduction package is available at [6].        gramming, and context-oriented logics support efficient reasoning
                                                                          and inter-context communication [7, 12, 28, 35, 37]. Probabilistic
                                                                          graphical models and related network structures integrate local
                                                                          results into coherent global knowledge, balancing expressiveness
2   STATE OF THE ART                                                      with computational manageability [30].
Goal Decomposition with LLMs – LLMs can decompose com-
plex goals into structured subgoals for planning and assistance.
Multi-step plans are generated, refined, and evaluated [3]. SGA-
ACR [14] produces verifiable sub-goal chains for RL agents, while
DELTA [34] leverages scene graphs for efficient long-horizon task
decomposition. Hierarchical LLM agents improve tractability and           3   RESEARCH PROBLEMS
interpretability [23], and human-centered methods [42] learn de-          Humans often state goals imprecisely, while AI systems pursue
compositions that enhance non-expert performance on complex               them with strict literalism. This can lead to unintended outcomes,
programming tasks.                                                        because AI models may exploit loopholes to technically complete
   Abduction and Rule Synthesis – Abductive reasoning gener-              a task rather than follow the user’s true intent. Moreover, human
ates explanatory hypotheses and candidate symbolic rules [4], pro-        communication relies on shared context that AI systems typically
viding a principled path from observations to minimal assumptions         lacks. Therefore, vague instructions are particularly hazardous,
and compact rule-like hypotheses [39]. Statistical learning links,        because cannot be easily confirmed and disambiguated by external
via inductive logic programming and statistical relational learn-         sources.
ing, allow frequent patterns or abductive explanations to become             These issues manifest in concrete failure modes such as formal
human-interpretable if–then rules [24, 40]. Contemporary neuro-           proof cheating and reward hacking. Formal proof cheating occurs
symbolic approaches use abduction as structured prior knowledge           when an AI produces a proof that technically satisfies formal criteria
to guide neural learners, improving sample efficiency. Extracted          but does so by altering axioms or definitions, ignoring the genuine
hypotheses can be refined and pruned to produce robust, generaliz-        mathematical intent [8]. Reward hacking [41] occurs when an AI
able adaptation rules, bridging observed outcomes and formalized          system exploits imperfections in a proxy reward function, achieving
reusable knowledge for self-adaptive systems [4, 24, 40].                 high measured performance while violating the underlying goal.
                                                                                    New           Rule Verification




                                                                                                                                          Synthesis &
                                                                                                                                  SAT




                                                                                                                                          Verification
    Goal misspecification is therefore a central problem in AI safety [5],          Rules              Engine




                                                                                                                                             Level
                                                                                                                              SCM DRL
especially when formal objectives diverge from the informal in-
                                                                                       Goal /Rule
tent of system designers. Goodhart’s law in machine learning fur-                                        Verified             Theory
                                                                                       Synthesizer
ther predicts that proxy metrics tend to degrade when heavily                                             rules
optimized [32, 43], whether the goals are misspecified or merely
underspecified.                                                                                        Theory
    Even when designers choose the right high-level goals, they may                                                    Causal
                                                                                                  Knowledge                        Plan
still encode them in ways that are too narrow or incomplete, leading                 Analyze                          Reasoning




                                                                                                                                              NeSy Causal
                                                                                                                                              Framework
AI systems to optimize the measurable formal metric rather than the                                  DRL SAT           Engine
broader human objective it was meant to approximate. Essentially,                                      SCM
humans rely on vague, context-dependent, and partly unconscious                      Monitor                        Execute
goals [9, 15, 25]. Conversely, AI systems require precise, formal,
and loophole-free specifications to behave as intended [5].                                 Self-adaptive DRL agent
    Accordingly, humans need support tools that help them artic-
ulate more precise and robust specifications that reduce misinter-                                Environment
pretation or manipulative compliance by AI systems. This support
must go beyond traditional verification and validation. In this paper,
                                                                             Figure 1: Extending NeSy Causal Framework with Rule-
we propose a vision of goal-specification assistance centered on
                                                                             synthesis and Verification
explicit rules and their systematic composition. We explore these
fundamental challenges through two research questions.                       MAPE-K (Monitor-Analyze-Plan-Execute) feedback loop as the ref-
                                                                             erence model for self-adaptive systems [27]. The process begins
      • RP.1 – What are the current capabilities of generative AI            with monitoring execution traces from the DRL agent to detect
        to support the synthesis of rules in a principled way that           distribution shifts and safety-constraint violations. In the analysis
        minimizes redundancies and ambiguities while maintaining             and planning phases, FOL-based abductive reasoning identifies can-
        traceability to system goals? Our approach – Establish               didate explanations, while the causal model evaluates intervention
        operations that refine rules via deduction and explain their         effects and selects minimal, high-explanatory-power configuration
        effect via abduction.                                                changes. These interventions guide knowledge transfer and warm-
      • RP.2 – How can rule synthesis be automatically evaluated in          start retraining of the DRL agent, whose updated behavior produces
        incremental and modular ways? Our approach – Search for              new traces that refine both symbolic and causal knowledge. The
        sufficient and necessary rule sets that satisfy a given goal.        framework thus interleaves logical reasoning, causal inference, and
   General Insight – We consider goals and subgoals as effects               learning to enable explainable, constraint-aware adaptation rather
of rules (causes) and their preconditions (controls). Moreover, will         than reactive retraining.
rely on causal representations and fundamental domain laws to
constrain reasoning about rules and their effects with respect to            4.2    Synthesis & Verification Level
system adaptations that preserve performance and safety [2, 17].             The Synthesis & Verification Level extends the original NeSy frame-
                                                                             work by introducing a meta-self-aware synthesis and verification
4     APPROACH                                                               layer on top of the operational adaptation cycle. In contrast to
                                                                             the earlier framework, the outputs of causal explanation are no
The proposed approach builds on our previous work [2], which is
                                                                             longer used solely for policy adaptation. Instead, anomaly reports
a neuro-symbolic (NeSy) causal reasoning framework for learning-
                                                                             are forwarded to the higher synthesis & verification level. This
enabled self-adaptive systems [16, 19] in particular when operating
                                                                             level contains a Goal/Rule Synthesizer and a Rule Verification Engine
under distribution shifts [18] and under safety-critical goals [21]
                                                                             that collectively update the theory that comprises domain knowl-
—see Section 4.1. As depicted in Figure 1, the approach comprises a
                                                                             edge, system constraints, and adaptation rules. Verified rules are
Goal/Rule Synthesizer and a Rule Verification Engine on top of the
                                                                             reintegrated into the knowledge base, thereby modifying future
NeSy framework—see Section 4.2.
                                                                             analysis and planning steps. The architecture, therefore, introduces
                                                                             a closed meta-loop in which the system adapts not only its behavior
4.1     NeSy Causal Framework                                                but also its governing symbolic FOL theory, enabling progressive
The Neuro-Symbolic (NeSy) causal framework integrates three com-             self-improvement and increased explainability.
plementary representations: (1) Symbolic Abduction Trees (SAT)               Goal/Rule Synthesizer – The pipeline (see Figure 2) receives as in-
grounded in first-order logic (FOL) to formally encode domain                put the high-level goals and governing principles provided by a hu-
knowledge, system constraints, and adaptation rules, enabling logi-          man expert expressed in natural language (natural-language based,
cal abduction to explain observed violations; (2) a structural causal        NLB) rather than as formal constraints, following the detection of a
model (SCM) that represents dependencies between environment                 drift or anomaly. The first step uses a large language model (LLM)
and system variables and supports intervention and counterfac-               to decompose each high-level goal into a set of lower-level candi-
tual reasoning; and (3) a deep reinforcement learning (DRL) policy           date causes, representing concrete conditions, behaviors, or system
responsible for operational decision-making–see Figure 1 for a ref-          properties that collectively could realize or justify the intended
erence. The three representation spaces are embedded within the              goal. These generated causes are then reprocessed by the LLM in
                                                                             to Causes          Consolidation       Translation


                                                                                            New Unverified           Evaluate
                                                                                             Rules (FOL)          Necessary &
                                                                                                                Sufficient Causes

                                                                                    Necessary     Sufficient
                                                                                     Causes        Causes        Rule Verification
                                                                                                                      Engine




                                                                                                                     Rule Verification Engine
                                                                                          New Rules
                                           Goal / Rule Synthesizer                       (Unverified)
                                                                                                                                                                  New Rules
          Principles                                                                                                                                               (Verified)
                                                                                                                                       Logical        Safety
   High-level             Candidate            Unique Causes                                          Syntax & Schema                Consistency    Invariant
     Goal                  Causes                  (NLB)                                                 Verification                  Check       Verification


                Decomposition           Semantic            Symbolic
                  to Causes           Consolidation        Translation                          Figure 3: Pipeline for Rule verification Engine

                                 New Unverified
                                                                                        Decomposition to Causes - The high-level goal (effect) represents
                                                            Evaluate
                                  Rules (FOL)            Necessary &
                                                                                        a scenario derived from everyday driving tasks. The objective is to
                                                       Sufficient Causes                generate candidate causes that explain how the effect may occur.
                                                                                        For example, the effect “respond correctly to a sudden obstacle on the
                         Necessary    Sufficient
                          Causes       Causes             Rule Verification             road” may be explained by the cause “the driver applies emergency
                                                               Engine                   braking.” The LLM decomposes the effect into candidate causes
                                                                                        required to achieve it while ensuring safety and compliance with
                                                                                        traffic regulations. The synthesis process is strictly constrained to
          Figure 2: Pipeline for Goal/Rule Synthesizer                                  limit hallucinations and unrelated reasoning, resulting in causes
                                    New Rules                  Rule Verification Engine that are logically consistent
                                                                                                                 New Ruleswith the effect and with the defined
                                   (Unverified)                                         constraints.              (Verified)
a semantic consolidation step, where overlapping, redundant, or
                                             Syntax &and
                                                       Schema              Logical
                                                                                        Semantic       Consolidation        – Although the focus is restricted at
semantically equivalent causes are identified             merged. This       nor- Consistency          Safety Invariant
                                                Verification                      Check the first step,Verification
                                                                                                          there is still a need to merge causes that refer to
malization produces a consistent set of unique causes, ensuring
                                                                                        similar concepts to reduce general statements that overlap into a
that the emerging theory avoids duplication and ambiguity. In the
                                                                                        set of unique causes. The semantic consolidation step is carried
next step, the consolidated causes are again provided to the LLM for
                                                                                        out to combine causes that describe the same underlying condition.
symbolic translation, mapping natural-language concepts into can-
                                                                                        "Driver maintains control of the vehicle" and "Driver is aware of
didate logical predicates and relations and producing a set of new,
                                                                                        surrounding traffic" are combined into a cause as "Driver maintains
unverified rules (causes) expressed in FOL. The resulting logical
                                                                                        control of the vehicle and is aware of surrounding traffic".
rules enable formal reasoning during the Rule Verification pipeline,
                                                                                        Symbolic Translation – After generating unique causes, each
e.g., using a verification solver such as Z3 [11]. The goal/rule synthe-
                                                                                        cause is translated from natural language to formal symbolic (FOL)
sizer pipeline analyzes combinations of causes to determine subsets
                                                                                        form to enable structured reasoning and systematic subset evalua-
of necessary and sufficient conditions that adequately justify the
                                                                                        tion. Although this step follows semantic unification in Figure 2, it
original synthesized Goal (more details in Section 4.3). The output
                                                                                        can be applied at any stage without altering content. Subsequent
of this pipeline is a set of newly synthesized but still unverified
                                                                                        analysis uses the natural language causes for stronger LLM reason-
logical rules representing intended behavior derived jointly from
                                                                                        ing, with FOL forms used only in the rule verification pipeline Fig-
empirical evidence and human intent.
                                                                                        ure 3. This decision is based on the observation that LLMs demon-
Rule Verification Engine - The synthesized rule candidates are
                                                                                        strate stronger reasoning performance when operating on natural
forwarded to the Rule Verification Engine, where formal consis-
                                                                                        language inputs. To ensure consistency and avoid ambiguity, a for-
tency and safety validation are performed to ensure that synthesized
                                                                                        mal grammar is defined in the prompt, and the model is instructed
rules can be safely incorporated into the system theory–see Fig-
                                                                                        to strictly follow it. Each cause is thus mapped to a structured
ure 3. The layered pipeline consists of (1) syntactic and schema
                                                                                        logical form that preserves its meaning while remaining machine-
validation, ensuring that generated rules conform to the logical
                                                                                        interpretable.
language and domain ontology together with semantic ground-
                                                                                           Alongside the FOL rule, the LLM also provides a brief explanation
ing checks, confirming that predicates and variables correspond to
                                                                                        of its translation, detailing how the natural language condition was
valid system entities; (2) logical consistency analysis, where candi-
                                                                                        interpreted and which predicates and operators were chosen. This
date rules are evaluated against the existing FOL knowledge base
                                                                                        enhances transparency, verifies semantic alignment, and improves
to detect contradictions; and (3) safety and invariant verification,
                                                                                        interpretability of the symbolic mapping.
which formally checks whether the rules preserve required system
                                                                                        Evaluate Necessary & Sufficient Causes – After obtaining a set
properties. The pipeline employs an automated reasoning tool to
                                                                                        of unique causes, the next step involves assessing the necessity and
perform satisfiability and entailment checks. Only rules that satisfy
                                                                                        sufficiency of each cause with respect to the main goal (effect). We
all verification stages are promoted to a verified theory and commit-
                                                                                        break this down into three steps described below:
ted to the knowledge repository. This verified knowledge is then
fed back into the adaptive loop, ensuring that future adaptations                           (i) Individual Necessity Evaluation is concerned with whether
are guided by formally verified, explainable principles rather than                              each cause is essential and provides a justification, citing
purely data-driven updates.                                                                      specific legal or safety conditions that would be violated if
                                                                                                 absent. Each cause is assessed independently, and the output
                                                                                                 is a structured list recording the cause, its necessity, and the
4.3 Illustrative Scenario for Goal/Rule Synthesis                                                rationale.
        Pipeline                                                                           (ii) Subset Necessity Evaluation identifies causes that are essen-
We demonstrate the Goal/Rule Synthesis Pipeline based on an ap-                                  tial only in combination. Starting with the full set, causes
plication in the domain of autonomous driving.                                                   are removed one at a time, and the feasibility of the effect is
          confirmed. A cause is deemed necessary if after its removal,       as maintaining vehicle control, adhering to speed limits, and keep-
          the effect is judged unachievable. A removed cause or set          ing safe distances. We selected the most relevant laws from this
          of causes is recorded as a minimal necessary subset if no          formalized research [13]. To cover broader scenarios encountered
          smaller subset produces the same effect. To improve effi-          in everyday driving, we then extended the set using generative AI,
          ciency, the candidate subsets containing already identified        specifically ChatGPT. This ensures that the legal knowledge can
          minimal subsets are skipped, and the outcomes of previous          guide the model in a variety of realistic situations while remaining
          evaluations are cached. This bottom-up approach ensures            interpretable and precise.
          that all truly minimal necessary combinations are captured
          while reducing computational effort.                                  Safety Principles: The safety principles capture physical princi-
    (iii) Minimal Sufficient Set Evaluation aims at identifying the sub-     ples of vehicle motion. Initially, we developed a basic set of rules rep-
          sets of causes that are individually sufficient to produce a       resenting logical and physics-based constraints. Examples include
          given effect. We start with single causes and test their suffi-    limits on friction, constraints on braking distance, and conditions
          ciency, incrementally adding additional causes if the effect       that increase the risk of losing traction at high speeds. To expand
          does not occur. This process continues until a sufficient sub-     coverage, ChatGPT was used to generate additional rules represent-
          set is found, and is repeated across all relevant combinations.    ing general principles, e.g., as "collision_if_obstacles", which states
          To reduce computational effort, supersets of already identi-       that a vehicle may collide if obstacles are present. This expanded set
          fied sufficient subsets are skipped, as sufficiency is preserved   allows the model to account for a wider variety of practical driving
          under addition. Once all minimal sufficient sets are deter-        scenarios while remaining grounded in physical feasibility.
          mined, they can be combined into a necessary-and-sufficient           Grammar and Symbolic Rule Language: The symbolic grammar
          set, which guarantees the effect and is required for its oc-       used for translating natural language causes into formal rules is
          currence. This set unifies all alternative minimal sufficient      based on the same formalization framework presented in [13]. The
          causes, capturing every pathway to the effect within a single      original predicate set is extended to incorporate additional predi-
          comprehensive framework.                                           cates related to fundamental speed and friction properties in order
                                                                             to capture physics-based safety constraints. Moreover, the grammar
5     PROOF OF CONCEPT                                                       specifies the allowed rule forms, comparison operators, and logical
Experimental Setup - We design a controlled experiment to show               operators that may be used in rule construction.
how Large Language Models (LLMs) can help automate parts of the                 All reasoning carried out by the LLM is grounded in these curated
Goal/Rule Synthesizer pipeline illustrated in Figure 2. The objective        laws, which serve as the primary reference for evaluating causes.
of this setup is to evaluate realistic driving scenarios in which an         External knowledge or assumptions beyond this curated set are not
intended effect (Goal) must be explained by a set of underlying              used. This guarantees that all cause & effect evaluations remain
causes (Rules). The intent is not to verify causality in a statistical       valid, consistent, and reproducible. A complete listing of all legal
sense, but to show how LLMs can be guided to perform structured              and safety laws used is provided in the Appendix [6].
abductive and deductive reasoning. The scope of the setup is con-
strained by a predefined set of legal and safety regulations that            5.3     Results
define the boundaries within which the synthesis and reasoning               We analyze two illustrative scenarios to demonstrate the outputs
process operates.                                                            of the pipeline. For each scenario, candidate causes were generated,
                                                                             semantically consolidated, individually evaluated for necessity, and
5.1      Implementation Overview                                             subsequently analyzed to identify minimal necessary subsets and
                                                                             sufficient subsets..
The pipeline is implemented by leveraging the OpenAI GPT-4o
Mini model [38] to perform all processing tasks. Step by step, the           5.3.1   Scenario 1: Successfully Merge into Heavy Traffic.
process transforms an human stated goal (effect) description into a
set of candidate causes. The process begins with cause generation,              Decomposition and Consolidation. Eight candidate causes were
followed by consolidation of overlapping causes, then individual             initially generated. After semantic de-duplication, four unique con-
evaluation, and finally, subset analysis for necessity and sufficiency.      solidated causes remained:
This iterative design ensures that the reasoning is incremental,                (1) Driver maintains control of the vehicle and is aware of sur-
traceable, and easy to interpret at every step. The legal and safety                rounding traffic.
regulations that guide the process are defined prior to the first               (2) Vehicle is traveling at a speed that allows for safe merging
stage. These regulations serve as the sole reference for the model                  and adheres to traffic laws regarding merging.
throughout the pipeline. For details on how these principles were               (3) Sufficient distance is kept from other vehicles to merge safely,
sourced and compiled–see Section 5.2.                                               and no vehicles are overtaking on the right.
                                                                                (4) Traffic conditions allow for merging without impeding flow,
                                                                                    and no sudden obstacles in the merging path.
5.2      Data Sources
   Legal Principles: The legal Principles used in this work are de-             Individual Necessity Evaluation. Each consolidated cause was
rived from a formalized set of German traffic regulations designed           evaluated independently against the relevant safety and legal con-
for machine interpretability. These regulations define rules such            straints. Only the first two were classified as individually necessary.
This approach makes its reasoning both interpretable and action-             • Driver control and attentiveness: Without stable control and
able, providing a clear understanding of the underlying dynamics.              responsiveness, maintaining constant speed violates vehicle
    • Driver control and awareness: Without maintaining control                control safety requirements.
      and awareness, safe merging is not possible, violating safety          • Vehicle speed within limits: Operating outside legal speed
      constraints related to vehicle stability and collision avoid-            bounds violates regulatory constraints and invalidates the
      ance.                                                                    effect.
    • Vehicle speed within safe limits: Appropriate speed is essen-          • Sufficient friction: Adequate tire–road friction is required to
      tial for lawful and safe merging. Deviations from safe speed             maintain speed safely and preserve traction.
      ranges can violate legal constraints and create unsafe condi-          Minimal Necessary Sets. Three minimal necessary sets were iden-
      tions.                                                             tified, corresponding to the causes that were also individually nec-
    Minimal Necessary Sets. Four minimal necessary sets were iden-       essary:
tified. Each set represents a core condition that cannot be removed           • Necessary Set 1: Driver maintains vehicle control and is at-
without rendering the effect impossible:                                         tentive and responsive to road conditions.
    • Necessary Set 1: Driver maintains control of the vehicle and            • Necessary Set 2: Vehicle speed is within legal limits and above
      is aware of surrounding traffic.                                           minimum required speed.
    • Necessary Set 2: Vehicle is traveling at a speed that allows for        • Necessary Set 3: Sufficient friction between tires and road.
      safe merging and adheres to traffic laws regarding merging.           Minimal Sufficient Sets. Two minimal sufficient sets were identi-
    • Necessary Set 3: Sufficient distance from other vehicles to        fied:
      merge safely and no vehicles are overtaking on the right.
                                                                               • Sufficient Set 1:
    • Necessary Set 4: Traffic conditions allow for merging without
                                                                                 – Driver maintains vehicle control and is attentive and re-
      impeding flow and no sudden obstacles in the merging path.
                                                                                   sponsive to road conditions.
   Minimal Sufficient Sets. Sufficient sets represent combinations of            – Vehicle speed is within legal limits and above minimum
causes that guarantee successful merging. One minimal sufficient                   required speed.
set was identified:                                                              – Sufficient friction between tires and road.
    • Sufficient Set 1:                                                          – No obstacles on the highway segment.
      – Driver maintains control of the vehicle and is aware of                • Sufficient Set 2:
        surrounding traffic.                                                     – Driver maintains vehicle control and is attentive and re-
      – Vehicle is traveling at a speed that allows for safe merging               sponsive to road conditions.
        and adheres to traffic laws regarding merging.                           – Vehicle speed is within legal limits and above minimum
      – Sufficient distance from other vehicles to merge safely and                required speed.
        no vehicles are overtaking on the right.                                 – Sufficient friction between tires and road.
      – Traffic conditions allow for merging without impeding                    – No sudden changes in traffic conditions.
        flow and no sudden obstacles in the merging path.                These results demonstrate that, while certain causes may not be
These findings highlight an important structural property: while         required on their own to produce the effect, they play a crucial role
some causes are not individually necessary, they become indis-           when combined with other factors. In these sufficient combinations,
pensable within certain minimal necessary sets. Moreover, every          their presence helps ensure that the effect reliably occurs. This
minimal necessary cause is included within sufficient sets that en-      highlights how individual causes can contribute indirectly, support-
sure the effect occurs, illustrating how necessary and sufficient        ing the overall outcome even if they are not strictly necessary in
conditions are systematically linked.                                    isolation.

5.3.2 Scenario 2: Maintain a Constant Speed on a Highway Segment.        5.3.3 Symbolic Translation. To illustrate the formal translation
                                                                         step, each unique cause was converted into a symbolic rule for both
   Decomposition and Consolidation. Eight candidate causes were          scenarios using the predefined grammar. The following examples
initially generated. After deduplication, six unique causes remained:    show how natural language conditions are mapped into formally
   (1) Driver maintains vehicle control and is attentive and respon-     constrained logical representations.
       sive to road conditions.                                             "Driver maintains control of the vehicle"
   (2) Vehicle speed is within legal limits and above minimum            ∀𝑥 (¬𝑐𝑜𝑙𝑙𝑖𝑑𝑒 (𝑥) ← 𝑠𝑑_𝑓 𝑟𝑜𝑛𝑡 (𝑥) ∧ 𝑠𝑑_𝑟𝑒𝑎𝑟 (𝑥) ∧ ¬𝑙𝑎𝑛𝑒_𝑐ℎ𝑎𝑛𝑔𝑒 (𝑥))
       required speed.
   (3) Sufficient friction between tires and road.                       This rule formalizes vehicle control through safe longitudinal dis-
   (4) No obstacles on the highway segment.                              tances (sd) and the absence of destabilizing lane changes, ensuring
   (5) No sudden changes in traffic conditions.                          collision avoidance.
   (6) No emergency situations requiring sudden braking.                    "Sufficient distance from other vehicles to merge safely"
                                                                                   ∀𝑥 (𝑠𝑑_𝑓 𝑟𝑜𝑛𝑡 (𝑥) ∧ 𝑠𝑑_𝑟𝑒𝑎𝑟 (𝑥) ← ¬𝑑𝑒𝑛𝑠𝑒 (𝑥))
   Individual Necessity Evaluation. Each cause was evaluated indi-
vidually against safety and legal constraints. The first three were      Low traffic density implies that safe distances (sd) can be maintained
classified as individually necessary:                                    both in front of and behind the vehicle.
These examples demonstrate how rich driving conditions are sys-           the model’s responses. These factors constrain the completeness
tematically reduced to formally constrained logical rules within the      and robustness of the synthesized rule sets and their evaluations
reasoning framework. A key takeaway is that the LLM can inter-            and indicate that principled rule synthesis and modular evaluation
pret nuanced, context-dependent descriptions and convert them             still depend heavily on the quality and coverage of the underlying
into precise symbolic forms. It effectively bridges human-readable        knowledge base (RP.1, RP.2).
reasoning with formal, machine-interpretable logic, keeping both              However, these challenges point toward opportunities for im-
meaning and structure intact. For a comprehensive presentation            provement. Expanding the set of rules, introducing probabilistic
of the generated candidate causes, intermediate evaluation steps,         reasoning, or incorporating multiple model perspectives could en-
full subset analyses, and complete symbolic translations for both         hance robustness. Iterative refinement of prompts and providing
scenarios, refer to the Appendix [6], where detailed end-to-end           feedback to the model can further reduce errors. Such extensions
examples of the pipeline execution are provided.                          would not only broaden the domain coverage but also strengthen
                                                                          the principled nature of rule synthesis and the reliability of in-
                                                                          cremental, modular rule evaluation with respect to evolving goals
6   DISCUSSION                                                            (RP.1, RP.2). Overall, the pipeline demonstrates a form of abductive
The pipeline provides a structured way to analyze cause & effect          reasoning. It identifies likely causes, evaluates their necessity and
relationships in driving scenarios, directly informing how Genera-        sufficiency, and uncovers conditional dependencies. The structured,
tive AI can support the synthesis of rules in a principled, traceable     stepwise process makes the reasoning traceable and interpretable
manner (RP.1). Each stage contributes unique insights into the            while capturing complex interactions between factors, thereby pro-
reasoning process. The initial decomposition highlights the poten-        viding concrete evidence that LLM-based pipelines can support
tial factors that could lead to the effect, ensuring that no obvious      goal-based, legally and safety-informed rule synthesis (RP.1) and
candidate cause is missed and that high-level goals are system-           in a systematic, incremental, and modular way (RP.2).
atically unpacked into concrete rule candidates. De-duplication
then reduces redundancy, merging overlapping causes while pre-            7    CONCLUSION AND FUTURE WORK
serving meaning, which directly addressing the need to minimize           The proposed framework demonstrates how neuro-symbolic causal
ambiguities and redundancies in synthesized rules. This simplifies        reasoning, combined with large language models, can support in-
the reasoning and prevents inflated or repetitive outputs, thereby        cremental and modular rule synthesis grounded in legal and safety
improving the clarity and manageability of the rule space at scale.       principles. By decomposing high-level goals into candidate causes,
   Individual necessity evaluation assesses each cause in isolation       consolidating them semantically, translating them into formal rules,
and shows which factors are critical on their own, providing a first      and then analyzing necessary and sufficient cause sets, the pipeline
approximation of how candidate rules relate to system goals (RP.1).       yields traceable and interpretable rule sets that capture complex
However, this step alone cannot capture conditional relationships.        causal interactions in domains such as autonomous driving. The
Subset evaluation addresses this by considering combinations of           subsequent verification stages—covering syntax and schema checks,
causes. Interestingly, some causes initially marked as not necessary      logical consistency, and safety and invariant preservation—ensure
were required when combined with other factors. This demon-               that only rules compatible with an existing knowledge base and
strates the importance of examining interactions and conditional          domain constraints are integrated back into the system, thereby
dependencies rather than relying solely on isolated assessments           strengthening reliability and explainability across the MAPE-K loop.
and shows how rule evaluation must account for contextual depen-          Together, these elements illustrate how abductive and deductive
dencies to remain faithful to the desired specified goals (RP.2).         reasoning can be orchestrated to reduce brittleness, improve goal
   Sufficiency analysis further emphasizes flexible pathways to the       alignment, and provide a principled pathway from natural-language
effect and operationalizes the search for sufficient and necessary        specifications to formally verified rule theories.
sets of rules that satisfy a given goal (RP.2). Minimal sufficient sets      In future work, we plan to deepen the integration between causal
include the necessary causes and may also incorporate additional          models and rule synthesis to derive more expressive sets of neces-
factors to guarantee the effect. This reflects real-world complexity,     sary and sufficient rules, and to broaden the coverage of domain
where multiple combinations of conditions can produce the same            principles beyond the current set of traffic regulations. We also plan
outcome similar to Scenario 2. Some causes that seemed irrelevant         to incorporate automated solvers to detect and resolve conflicts
individually were shown to be sufficient only in combination, high-       between newly synthesized rules and existing knowledge, enabling
lighting the subtlety of causal relationships. Together, the necessity    systematic management of inconsistencies at the theory level. This
and sufficiency analyses provide an incremental and modular way           will support the design of richer feedback loops that jointly ex-
to evaluate rules: incremental, because causes and subsets are as-        ploit formal verification, causal path analysis, and effect estimation,
sessed stepwise; modular, because minimal sets can be associated          with the goal of informing more robust synthesis, composition, and
with specific goals and reused as distinct rule components (RP.2).        adaptation strategies in safety-critical, learning-enabled systems.
   Despite its strengths in addressing RP.1 and RP.2, the approach
has limitations. The model functions as a black box, so the internal      REFERENCES
reasoning is not fully transparent. Moreover, there is a reliance on       [1] Christian Medeiros Adriano, Sona Ghahremani, and Holger Giese. 2024. Prin-
the predefined set of regulations, which may not cover all possible            cipled Transfer Learning for Autonomic Systems: A Neuro-Symbolic Vision. In
                                                                               2024 IEEE International Conference on Autonomic Computing and Self-Organizing
scenarios. Additionally, the outputs are highly sensitive to how the           Systems Companion (ACSOS-C). 79–84. https://doi.org/10.1109/ACSOS-
prompts are formulated, which can influence the adaptability of                C63493.2024.00035
 [2] Christian Medeiros Adriano, Sona Ghahremani, Finn Kaiser, and Holger Giese.            [24] P Hitzler, MK Sarker, TR Besold, AD Garcez, S Bader, H Bowman, P Domingos,
     2025. Neuro-symbolic causal reasoning for cautious self-adaptation under distri-            KU Kühnberger, LC Lamb, et al. 2022. Neural-symbolic learning and reasoning:
     bution shifts. In 2025 IEEE International Conference on Autonomic Computing and             A survey and interpretation. Frontiers in artificial intelligence and applications
     Self-Organizing Systems (ACSOS). IEEE, 88–99.                                               342 (2022), 1–51.
 [3] Mohamed Aghzal, Erion Plaku, Gregory J Stein, and Ziyu Yao. 2025. A survey on          [25] Yi-Fei Hu, Joseph Heffner, Apoorva Bhandari, and Oriel FeldmanHall. 2025. Goals
     large language models for automated planning. arXiv preprint arXiv:2502.12435               bias face perception. Journal of Experimental Psychology: General (2025).
     (2025).                                                                                [26] Utkarshani Jaimini, Cory Henson, and Amit Sheth. 2024. Causal neuro-symbolic
 [4] Alicia Aliseda. 2017. The Logic of Abduction: An Introduction. In Springer                  AI for root cause analysis in smart manufacturing. In International Semantic Web
     Handbook of Model-Based Science. Springer, Cham, 1–24. Chapter on abduction                 Conference.
     and hypothesis generation.                                                             [27] Jeffrey O. Kephart and David M. Chess. 2003. The Vision of Autonomic Computing.
 [5] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and             Computer 36, 1 (2003), 41–50.
     Dan Mané. 2016. Concrete Problems in AI Safety. arXiv preprint arXiv:1606.06565        [28] Gabriele Kern-Isberner, Christoph Beierle, and Gerhard Brewka. 2020. Syntax
     (2016).                                                                                     Splitting = Relevance + Independence: New Postulates for Nonmonotonic Rea-
 [6] HPI System Analysis and Modeling Group. 2026. Goal-Based Rule Synthesis.                    soning From Conditional Belief Bases. In Proceedings of the 17th International
     https://github.com/hpi-sam/goal-based-rule-synthesis. GitHub repository.                    Conference on Principles of Knowledge Representation and Reasoning. 560–571.
 [7] Christoph Beierle, Lars-Phillip Spiegel, Jonas Haldimann, Marco Wilhelm, Jesse              https://doi.org/10.24963/kr.2020/56
     Heyninck, and Gabriele Kern-Isberner. 2024. Conditional splittings of belief bases     [29] Jan-Niklas Klein, Sona Ghahremani, Christian Medeiros Adriano, and Holger
     and nonmonotonic inference with c-representations. In Proceedings of the 21st               Giese. 2026. CrossMaps: A Confidence-Aware Open-Vocabulary Semantic Map-
     International Conference on Principles of Knowledge Representation and Reasoning            ping for Rover Navigation. In ICRA-companion, International Workshop on Robotics
     (Hanoi, Vietnam) (KR ’24). Article 10, 11 pages. https://doi.org/10.24963/kr.2024           Software Engineering (ROSE). To apear.
     /10                                                                                    [30] Kathrin Korte, Christian Medeiros Adriano, Sona Ghahremani, and Holger Giese.
 [8] Sascha Brodsky. 2025. The mathematicians teaching AI to reason. IBM Think                   2025. Causal knowledge transfer for multi-agent reinforcement learning in
     (October 2025). https://www.ibm.com/think/news/mathematicians-teaching-ai-                  dynamic environments. In 2025 IEEE International Conference on Autonomic
     to-reason Published 13 October 2025, updated 23 October 2025.                               Computing and Self-Organizing Systems Companion (ACSOS-C). IEEE, 154–159.
 [9] Jaime J Castrellon, Jacob S Young, Linh C Dang, Christopher T Smith, Ronald L          [31] Douglas B Lenat, Mayank Prakash, and Mary Shepherd. 1990. CYC: Using
     Cowan, David H Zald, and Gregory R Samanez-Larkin. 2021. Dopamine biases                    common sense knowledge to overcome brittleness and knowledge acquisition
     sensitivity to personal goals and social influence in self-control over everyday            bottlenecks. AI Magazine 11, 2 (1990), 65–85.
     desires. bioRxiv (2021), 2021–09.                                                      [32] LessWrong Community. 2023. AI Safety 101: Reward Misspecification. https:
[10] Erika F. de Almeida, Marcio V. Vieira, and Rogério de Lemos. 2017. MAPE-                    //www.lesswrong.com/posts/mMBoPnFrFqQJKzDsZ/ai-safety-101-reward-
     K based guidelines for designing reactive and proactive self-adaptive systems.              misspecification. Accessed 2026-02-12.
     In Proceedings of the 12th International Symposium on Software Engineering for         [33] Hu Liu, Alexander Gegov, and Mihaela Cocea. 2016. Rule-based systems: a
     Adaptive and Self-Managing Systems. IEEE, 97–107.                                           granular computing perspective. Granular Computing 1, 4 (2016), 259–274.
[11] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In           [34] Yuchen Liu, Luigi Palmieri, Sebastian Koch, Ilche Georgievski, and Marco Aiello.
     International conference on Tools and Algorithms for the Construction and Analysis          2025. Delta: Decomposed efficient long-term robot task planning using large lan-
     of Systems. Springer, 337–340.                                                              guage models. In 2025 IEEE International Conference on Robotics and Automation
[12] Thomas Eiter, Michael Fink, Giovambattista Ianni, Thomas Krennwallner,                      (ICRA). IEEE, 10995–11001.
     Christoph Redl, and Peter Schüller. 2016. A model building framework for               [35] Adithya Murali, Lucas Peña, Christof Löding, and P. Madhusudan. 2023. A First-
     answer set programming with external computations. Theory and Practice of                   order Logic with Frames. ACM Trans. Program. Lang. Syst. 45, 2, Article 7 (May
     Logic Programming 16, 4 (2016), 418–464.                                                    2023), 44 pages. https://doi.org/10.1145/3583057
[13] Klemens Esterle, Luis Gressenbuch, and Alois Knoll. 2020. Formalizing Traffic          [36] Mark A Musen. 1989. Automating knowledge acquisition for expert systems.
     Rules for Machine Interpretability. In Proceedings of the 3rd IEEE Connected and            Methods of Information in Medicine 28, 4 (1989), 237–244.
     Automated Vehicles Symposium (CAVS). Institute of Electrical and Electronics           [37] Emilia Oikarinen. 2006. Modular Answer Set Programming. Technical Report
     Engineers (IEEE), Victoria, B.C., Canada. https://doi.org/10.1109/CAVS51000.20              Research Report A106. Helsinki University of Technology, Laboratory for Theo-
     20.9334599                                                                                  retical Computer Science.
[14] Shanwei Fan, Bin Zhang, Zhiwei Xu, Yingxuan Teng, Siqi Dai, Lin Cheng, and             [38] OpenAI. 2025. OpenAI developer platform. https://platform.openai.com/ Last
     Guoliang Fan. 2025. Subgoal Graph-Augmented Planning for LLM-Guided Open-                   visited 16.05.2025.
     World Reinforcement Learning. arXiv preprint arXiv:2511.20993 (2025).                  [39] Gabriele Paul. 1993. Approaches to abductive reasoning: an overview. Artificial
[15] Klaus Fiedler and Mandy Hütter. 2014. The Limits of Human Information Process-              intelligence review 7, 2 (1993), 109–152.
     ing in Goal Pursuit: Motivational Influences on Judgment and Decision Making.          [40] Luc De Raedt and Kristian Kersting. 2008. Statistical Relational Learning and
     Current Directions in Psychological Science 23, 3 (2014), 163–170.                          Inductive Logic Programming. Springer, Berlin. Bridging statistical learning and
[16] Sona Ghahremani, Christian Medeiros Adriano, and Holger Giese. 2018. Training               symbolic rule induction.
     Prediction Models for Rule-Based Self-Adaptive Systems. In International Confer-       [41] Joar Skalse, Nikolaus Howe, Dmitrii Krasheninnikov, and David Krueger. 2022.
     ence on Autonomic Computing (ICAC). 187–192. https://doi.org/10.1109/ICAC.2                 Defining and characterizing reward gaming. Advances in Neural Information
     018.00031                                                                                   Processing Systems 35 (2022), 9460–9471.
[17] Sona Ghahremani and Holger Giese. 2021. Hybrid planning with receding hori-            [42] Jiaxin Wen, Ruiqi Zhong, Pei Ke, Zhihong Shao, Hongning Wang, and Minlie
     zon: A case for meta-self-awareness. In 2021 IEEE International Conference on               Huang. 2024. Learning task decomposition to assist humans in competitive
     Autonomic Computing and Self-Organizing Systems Companion (ACSOS-C). IEEE,                  programming. arXiv preprint arXiv:2406.04604 (2024).
     131–138.                                                                               [43] Lilian Weng. 2024. Reward Hacking in Reinforcement Learning. https://lilianwe
[18] Omid Gheibi and Danny Weyns. 2024. Dealing with Drift of Adaptation Spaces                  ng.github.io/posts/2024-11-28-reward-hacking/. Accessed 2026-02-12.
     in Learning-based Self-Adaptive Systems Using Lifelong Self-Adaptation. ACM            [44] Fangkai Yang, Daoming Lyu, Bo Liu, and Steven Gustafson. 2018. Peorl: Inte-
     Trans. Auton. Adapt. Syst. 19, 1, Article 5 (feb 2024), 57 pages. https://doi.org/10        grating symbolic planning and hierarchical reinforcement learning for robust
     .1145/3636428                                                                               decision-making. arXiv preprint arXiv:1804.07779 (2018).
[19] Omid Gheibi, Danny Weyns, and Federico Quin. 2021. Applying machine learning
     in self-adaptive systems: A systematic literature review. ACM Transactions on
     Autonomous and Adaptive Systems (TAAS) 15, 3 (2021), 1–37.
[20] David Perry Greene. 1987. Automated knowledge acquisition: Overcoming the
     expert system bottleneck. In Proceedings of the Eighth International Conference on
     Information Systems (ICIS 1987). Association for Information Systems, 155–167.
[21] Joachim Haensel, Christian Medeiros Adriano, Johannes Dyck, and Holger Giese.
     2020. Collective risk minimization via a bayesian model for statistical software
     testing. In Proceedings of the IEEE/ACM 15th International Symposium on Software
     Engineering for Adaptive and Self-Managing Systems (Seoul, Republic of Korea)
     (SEAMS ’20). ACM, 45–56. https://doi.org/10.1145/3387939.3388616
[22] Frederick Hayes-Roth. 1983. Rule-based systems. Commun. ACM 26, 9 (1983),
     921–932.
[23] Brennen Hill. 2025. Generative World Models of Tasks: LLM-Driven Hierarchical
     Scaffolding for Embodied Agents. arXiv:2509.04731 [cs.AI] https://arxiv.org/ab
     s/2509.04731
