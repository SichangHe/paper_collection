                                                   AkiraRust: Re-thinking LLM-aided Rust Repair Using a
                                                             Feedback-guided Thinking Switch
                                                             Renshuang Jiang† , Yichong Wang† , Pan Dong† , Xiaoxiang Fang† , Zhenling Duan† ,
                                                                              Tinglue Wang ¶ , Yuchen Hu ¶ , Jie Yu† , Zhe Jiang ¶
                                                             † National University of Defense Technology, China, ¶ Southeast University, China


                                         Abstract
                                            Eliminating undefined behaviors (UBs) in Rust programs requires
                                         a deep semantic understanding to enable accurate and reliable re-
                                         pair. While existing studies have demonstrated the potential of
                                         LLMs to support Rust code analysis and repair, most frameworks
arXiv:2602.21681v1 [cs.SE] 25 Feb 2026




                                         remain constrained by inflexible templates or lack grounding in
                                         executable semantics, resulting in limited contextual awareness
                                         and semantic incorrectness. Here, we present AkiraRust, an LLM-
                                         driven repair and verification framework that incorporates a finite-
                                         state machine to dynamically adapt its detection and repair flow
                                         to runtime semantic conditions. AkiraRust introduces a dual-mode
                                         reasoning strategy that coordinates fast and slow thinking across
                                         multiple agents. Each agent is mapped to an FSM state, and a
                                         waveform-driven transition controller manages state switching,            Figure 1. Existing Rust Repair Frameworks. (a) Template-Based:
                                         rollback decisions, and semantic check pointing, enabling context-        Rely on pattern matching; out-of-scope patterns lead to failed re-
                                         aware and runtime-adaptive repair. Experimental results show that         pairs. (b) LLM-Aided: Single-process with a fixed agent pipeline,
                                         AkiraRust achieves about 92% semantic correctness and delivers a          while multi-process dispatch agents by heuristic features. Unable
                                         2.2× average speedup compared to SOTA.                                    to traverse solution space and semantically inaccurate.

                                         1   Introduction
                                            Rust language [25] is designed for system-level programming            model in local code adjustments without performing the required
                                         with strong guarantees of memory safety, and has been widely              semantic fix. Multi-process frameworks (e.g., RustBrain [18], Re-
                                         adopted in critical domains such as operating systems and browsers        pairAgent [5]) attempted to consider more Rust features to provide
                                         [1, 21, 22]. However, for the flexibility and compatibility with low-     offline multi-process candidates, but they only based on initial code
                                         level operations, Unsafe Rust allows developers to bypass the com-        features (Fig. 1 (b)), also suffering from semantic incorrectness.
                                         piler’s safety checks, reintroducing potential undefined behaviors        Challenges. When we attempted to develop a framework to ad-
                                         (UBs). Rust’s safety mechanisms, while ensuring robustness, com-          dress Rust’s security and semantic correctness issues, we found
                                         plicate the semantic understanding and repair of UBs, even minor          that these frameworks commonly achieve high pass rates under
                                         changes must respect strict compiler checks. Studies show that re-        security detection tools (like Miri [26], Kani [33]), but their repairs
                                         pairing and verifying Rust’s safety properties have become critical       frequently deviate from the intended semantics, revealing a lack
                                         aspects of software development, accounting for over 40% of total         of dynamic adaptability in repair processes. From the reasoning
                                         debugging costs [4]. Therefore, how to achieve automated, reliable        perspective, current static and LLM-based frameworks either op-
                                         and semantically correctness repair of Rust has become a challenge.       erate within inflexible template constraints or lack grounding in
                                         Existing Works. Traditional static and dynamic methods, includ-           executable semantics. Due to Rust’s strong type system and own-
                                         ing formal, fuzzing, and symbolic execution (e.g., Thetis-Lathe [17],     ership semantics, the selection and coordination of repair agents
                                         RULF [15], and SafeNet [10]), remain template-based and rely on           significantly influence the reasoning path and repair accuracy (see
                                         rule-matching logic. When errors extend predefined patterns or            Sec. 2.1), restricted template schemes frequently cause reasoning
                                         involve complex semantics, these fail due to the lack of semantic         deadlocks or oscillations, preventing the model from discovering
                                         understanding (Fig. 1a). LLM-aided frameworks show promising              valid repair strategies in dynamic contexts. From the runtime per-
                                         capabilities in Rust repair [9, 18, 36], leveraging deeper semantic       spective, repair processes rarely incorporate runtime signals such as
                                         understanding and contextual reasoning ability. However, existing         execution traces, borrow-state transitions, or verification, resulting
                                         frameworks treat repair as an offline single-process, where agents        in limited semantic awareness and fragile validation of generated
                                         and their order are fixed before execution, even though the actual        fixes. All of these limitations hinder the dynamic adaptability and
                                         repair runs online (Fig. 1b), e.g., RustAssistant [9] and RustGen [36].   semantic correctness required for accurate and efficient Rust repair.
                                         While leveraging LLM capabilities allows them to handle a broader         Contributions. Here, we present AkiraRust, an LLM-driven Rust
                                         range of static template-based errors, inappropriate agent invoca-        repair framework that integrates finite state machine (FSM) to dy-
                                         tion can still lead to semantic violations. For instance, borrowing-      namically adapt its repair processes to runtime semantic variations.
                                         related Unsafe Rust errors cause template-based schemes (e.g., “as-       By leveraging FSM, (i) the states of AkiraRust are composed of
                                         sert–modify”) to repeatedly insert assertions, leading to deviation       a dual-mode multi-agents library, mapping multiple agents and
                                         and hallucination; switching to modification agents often traps the       thinking modes (fast and slow thinking) to distinct states, thereby
enabling dynamic strategy selection and improving repair accu-               levels (1–5) based on the LOC [35] and experienced engineers’ clas-
racy and efficiency. (ii) the state transition mechanism controls            sificationclassify. We then compared the semantic accuracy and
the selection of agent states and the construction of reasoning              efficiency of fast and slow thinking across these complexity levels,
sequences, combining runtime monitoring signals to track the re-             where efficiency is measured by the total time required to complete
pair process and validate semantic correctness, while guiding the            a repair.
LLM to self-correct or adjust hallucinated repair suggestions. As a
demonstration on the Miri dataset [26], AkiraRust achieves about                                                                                                                                                            Time Out
                                                                                                                                                            1.0




                                                                                                                                   Semantic Accuracy Rate




                                                                                                                                                                                                                                                   Total Executing Time(s)
92% semantic correctness and delivers a 2× speedup over SOTA.                                                                                                                                                                    702
                                                                                                                                                                                                                                             600
                                                                                                                                                            0.9

2     Background and Motivation                                                                                                                             0.8                                                                              450

                                                                                                                                                            0.7
2.1       Agent Selection for Adaptive Repair                                                                                                                           Fast Thinking Cost Time                                              300
                                                                                                                                                                        Slow Thinking Cost Time
                                                                                                                                                            0.6
    Due to Rust’s strict semantics, the repair process must maintain                                                                                                    Fast Thinking Semantic
                                                                                                                                                                                                                                             150
                                                                                                                                                                        Slow Thinking Semantic
fine-grained semantic correctness. Unsafe Rust, though limited in                                                                                           0.5

pattern variety [3, 16, 39], is highly sensitive, requiring precise rea-                                                                                    0.4                                                                              0
                                                                                                                                                                        1              2            3               4           5
soning over memory boundaries and cross-module. For LLM-aided                                                                                                       Defect Complexity（ 1=simple,5=complex)
repair, different agents are suited to different defect types. We use                                                                                   Figure 2. Fast vs. Slow Thinking in Rust Repair.
RustBrain [18], a SOTA repair tool, to generate ten solutions and
record multiple repair configurations with different agent combina-             In Fig. 2, for simple defects, fast thinking achieves a repair suc-
tions and execution orders to evaluate how these affect semantic             cess rate of 92% and completes repairs with minimal iterations,
correctness (Tab. 1). Here, 𝑁 is the total number of repair rounds,          demonstrating higher efficiency than slow thinking, which tends to
𝑞 total the overall semantic accuracy, and 𝑞 agt the effectiveness of        over-reason in certain cases, introducing redundant logic or halluci-
each RustBrain agent: 𝑞 assert for assertion insertion, 𝑞 modify for code    nated code. As defect complexity increases, however, slow thinking
modification, 𝑞 replace for Safe Rust replacement, and 𝑞 knowledge for       enhances accuracy and interpretability, surpassing fast thinking for
RAG querying. Higher 𝑞 agt indicates stronger agent specificity.             complex, context-dependent repairs. In these cases, fast thinking
                                                                             requires multiple iterations, leading to more than a 3× overhead.
          Table 1. Effectiveness of Agents in Unsafe Rust Cases.
    Index Case Feature      𝑁 𝑞𝑡𝑜𝑡𝑎𝑙 𝑞𝑎𝑠𝑠𝑒𝑟𝑡 𝑞𝑚𝑜𝑑𝑖 𝑓 𝑦 𝑞𝑟𝑒𝑝𝑙𝑎𝑐𝑒 𝑞𝑘𝑛𝑜𝑤𝑙𝑒𝑑𝑔𝑒
                                                                              Insight 2: Effective repair requires switching between fast and slow
                                                                              thinking based on Rust code features to balance efficiency and accuracy.
      1     size mismatch    14 0.50    0.286   0.286   0.429     0.286
      2     access violation 14 0.50    0.429   0.286   0.357     0.286
      3     write access     13 0.692   0.615   0.385   0.615     0.615      2.3                                               Hallucination Control for Adaptive Repair
      4     retag write      12 0.75    0.75    0.417   0.583     0.583
      5     dangling pointer 11 0.909   0.545   0.636   0.727     0.273         LLMs may produce incorrect or semantically inconsistent reason-
      6     atomic access    10 1.00    0.600   0.600   0.200     0.250      ing during the repair process, known as hallucination [13, 14, 38].
   In Tab. 1, cases 1, 2, 4, and 5 show that a properly selected sin-        Each reasoning step can be regarded as a decision under uncer-
gle agent nearly matches 𝑞𝑡𝑜𝑡𝑎𝑙 , indicating that an appropriately           tainty, we design a code-state evaluation method, using UBs num-
selected single-agent already captures the core structure, and addi-         ber, semantic consistency, and structural soundness, to measure
tional agents contribute little beyond redundant hypotheses. This            the code incorrectness (see details in Sec. 4.2). We then define the
is because unsafe Rust errors arise from a finite set of structured          hallucination score as the deviation between the maximum code
operations, e.g., size mismatches require semantic-preserving re-            incorrectness score and the initial code. Since temperature directly
placements, while access violations demand safety assertions, mak-           affects the stochasticity of model reasoning, we construct three
ing certain agents inherently better suited to specific defect types.        comparative pipelines: (i) low temperature w/o rollback1 ; (ii) high
Cases 3 and 6 show similar success rates across agents, as these de-         temperature w/o rollback; (iii) high temperature w/ rollback, to
fects require multi-agents coordination, but inappropriate actions           analyze how hallucination control influences repair quality.
(e.g., 𝑞𝑚𝑜𝑑𝑖 𝑓 𝑦 in case 3) can cause semantic inconsistencies.                                                                    Low-Temperature(= 0.1) High-Temperature(= 0.7) High-Temperature(= 0.7)
                                                                                                                                      without rollback        without rollback         with rollback
                                                                                                                               4
                                                                               Semantic Accuracy Rate % Incorrectness Score




 Insight 1: Aligning agent with defect features is crucial, as appropriate
 coordination markedly enhances repair and semantic accuracy.                                                                  3                                                                                              rollback

                                                                                                                               2
2.2       Reasoning Modes for Adaptive Repair                                                                                  1
   While LLMs possess strong capabilities in language understand-                                                                                                                 steps                         steps                                                    steps
                                                                                                                                   0 1 2 3 4 5 6                                           0 1 2 3 4 5 6                0    1 2         3    4               5
ing and pattern recognition, their effectiveness in repair tasks is                                                      100                                                                                                                                                 2.5
                                                                                                                                                                                                                             90%
                                                                                                                                                                                                                                                                              Hallucination Score




highly dependent on the underlying reasoning mode. LLMs ex-                                                                                                                                               1.8                                1.9                             2.0
                                                                                                                              75                            67%                               72%
hibit two distinct modes of thinking [8, 20, 30]: fast thinking and                                                                                                                                                                                                          1.5
                                                                                                                              50
slow thinking. Fast thinking is quick and intuitive, producing can-                                                                                                                                                                                                          1.0
                                                                                                                                                                            0.6
didate fixes with minimal computation. Slow thinking, in contrast,                                                            25                                                                                                                                             0.5
is more careful and step-by-step. It examines the code structure in                                                            0                                                                                                                                             0.0
                                                                                                                                                        Success Hallucination               Success Hallucination           Success Hallucination
more detail, checks ownership and lifetime rules more thoroughly,                                                                                        Rate       Score                    Rate       Score                Rate       Score
                                                                                                                                                                  (a)                               (b)                             (c)
and reasons across multiple steps before proposing a repair. By                                       Figure 3. Temperature and Rollback Effects on Rust Repair.
selecting 100 defect samples from the official Rust library and open-
source projects [31], we categorized Rust code by repair complexity          1 Rollback: the framework reverses back to the initial code when an anomaly is detected.
AkiraRust: Re-thinking LLM-aided Rust Repair Using a Feedback-guided Thinking Switch


   In Fig. 3, the line plot shows the evolution of incorrectness scores                                                                                          invokes specialized repair templates tailored to different unsafe
across repair steps, while the bar plot reports the final repair suc-                                                                                            patterns and error categories to achieve semantically consistent
cess rate and average hallucination deviation. Results indicate that                                                                                             repairs (❶ in Fig. 4). From Insight 1, the multi-agent repair library
high-temperature reasoning is more divergent, yielding both higher                                                                                               provides targeted repair strategies for type-related defects, e.g.,
hallucination levels and higher repair success rate (Fig. 3 (a) and                                                                                              assertion agents are used for type-mismatch errors, and modifica-
(b)). Introducing rollback under high temperature, effectively sup-                                                                                              tion agents handle value-correction errors, thereby offering more
presses hallucination, improves the accuracy of repair semantics                                                                                                 appropriate agent choices, reducing the overhead caused by ran-
and reduces the number of agent invocations (Fig. 3 (b) and (c)).                                                                                                dom agent selection, and improving repair accuracy. Furthermore,
                                                                                                                                                                 from Insight 2, during code generation, the LLM’s fast and slow
 Insight 3: Hallucinations inherently have exploratory potential, and
                                                                                                                                                                 thinking modes significantly influence agents’ reasoning depth and
 the point is to harness and control them via verification mechanisms,
                                                                                                                                                                 repair path selection. For the same agent, different thinking modes
 enabling improved repair semantic accuracy and efficiency.
                                                                                                                                                                 may yield distinct repair strategies. To better accommodate this
3      AkiraRust: At a Glance                                                                                                                                    cognitive diversity, we construct a dual-mode multi-agent library
                                                                                                                                                                 (❷ in Fig. 4), which modularized fast-thinking agents (heuristic and
   AkiraRust systematically addresses the challenges by FSM-based                                                                                                lightweight repair) and slow-thinking agents (deep semantic re-
runtime adaptive reasoning and repair orchestration, enabling the                                                                                                pair). This design enables adaptive invocation of appropriate agents
framework to determine which agents or tools to select, how rea-                                                                                                 across reasoning stages, achieving more flexible and efficient repair.
soning mode to adopt, and what actions to halt or rollback during                                                                                                   To address the limitation of inflexible template constraints and
the repair process. Overall, according to Rust’s semantic features,                                                                                              lacking executable semantics (Sec. 1), We construct an FSM-based
AkiraRust is composed of multiple LLM-based agents that oper-                                                                                                    repair framework that allows each agent to adaptively explore re-
ate under fast and slow thinking modes, and generate candidate                                                                                                   pair paths at runtime and gradually correct them under guidance
repairs by diverse strategies. Then, AkiraRust constructs an FSM                                                                                                 from code-context semantic feedback. The dual-mode multi-agent
that formally describes each state with agents and thinking modes,                                                                                               library maps agents and modes to the corresponding states of the
and defines transition conditions for selection states. By perform-                                                                                              FSM to support adaptive selection (❸ in Fig. 4). The FSM’s state-
ing runtime analysis of code, AkiraRust dynamically constructs                                                                                                   transition mechanism captures the current repair context, including
waveform evolution, which is a code-incorrectness scores curve                                                                                                   the UBs number, semantic correctness, and code structural, and
that reflects how the repair quality changes over time, and uses it                                                                                              determines the next agent invocation and reasoning mode (❹ in
to guide rollback decisions and adjust the reasoning depth. Fig. 4(a)                                                                                            Fig. 4). However, each transition introduces a semantic checkpoint,
presentshows the workflow of AkiraRust framework, showing the                                                                                                    a significant evaluation overhead is inevitably incurred. From In-
process from Rust code by UB detection to the adaptive repair path.                                                                                              sight 3, we design a self-adaptive correction mechanism based on
                             AkiraRust Fixes Rust Code Example Framework                                                                                         hallucination-aware evaluation to enhance state transitions con-
           Rust code                                       Defect Detection Tool                               Adaptive Repair Path
                                                                                                                                                                 ditions (❺ in Fig. 4). It scores the incorrectness of each generated
    fn main() {                                      error: Undefined Behavior:
       let x = 42;                                   deallocating ALLOC, which is                              1                               Dynamic           code, treating semantic hallucinations as deviations from expected
       let bad_box =                                                                                  s0               a              c        Runtime
                                                     stack variable memory, using                                                              Flexible          behavior; whenever the incorrectness exceeds a defined thresh-
    unsafe {                                                                                                       2       4
    mem::transmute::<&i                              Rust heap deallocation operation                                            5
    32, Box<i32>>(&x)                                self.1.deallocate(From::from(ptr.
                                                                                                           3
                                                                                                                       b
                                                                                                                                      d
                                                                                                                                               6
                                                                                                                                                        Sq       old, it triggers rollback or semantic evaluation to prevent error
    };                                               cast()), layout);
       drop(bad_box);                                 ^^^^^UB occurred here                                                      Exploring
                                                                                                                                                                 propagation and maintain repair stability.
    }
       （a) AkiraRust Workflow: Rust code -> defect detection -> adaptive repair path.                                                                               Overall, AkiraRust abstracts the repair process as a form of
    Dual-Mode Multi-Agent                                      FSM-Based Adaptive Reasoning Mechanism                                                            human-like reasoning, where each state transition reflects a cogni-
            Library
                                                                     States           Rust code                                                                  tive shift between exploration and reflection. By embedding adapta-
     1 Rust Agents Library
                                                                   Initial State
                    a       AssertAgent                               Fast   Dual                s0
                                                                                                                       halluci
                                                                                                                       nation
                                                                                                                                                                 tion into the repair path, it breaks the rigidity of static processes and
                                                       3         a
                    b       ModifyAgent                              Slow    Mode            1                                                 Repaired          enables the exploration of a larger repair space. Besides, compared
                                                     Mapping
                    c                                            b    Fast   Agents                        Step_2                                code
                      ReplaceAgent                                                               a Execute
                                                                      Slow   States                                                                              to running all agents at every step, it avoids combinatorial search
                                                                 …




                    d  Knowledge
                          Agent                        3           Error State               2             4               5              6
                         ……                                          Final State                 b
                                                                                                                    c            d                  Sq           explosion and excessive overhead. AkiraRust thus enables context-
                    n TestGenAgent                                                       3                     Step_3            Step_N
                                                                                                               Monitor           Rollback                        aware and semantically consistent repair of Rust UBs, enhancing
                                                                 4        Detection
       2   Reasoning Modes                                                                                  E (T)                              Error             the correctness and safety of the repaired code.
       Fast     s       a        b           … n
                                                                          Semantic                          Risk                          S3   State
     Thinking                                                             Evaluator          Loop Level S0                       S2                S4
                                                                                                                           S1
                             c                                 Switch         ……             Step                                                       Sq
                        a                                      Agent     Kownledge                                         1          2             3        T
      Slow      s                                                                                                      5       Error Level
                             b           d     … n
    Thinking
                                                               States Switch Controller                            Adaptive Mechanism
                                     …




                        b
                                                                                                                                                                 4     Implementation of AkiraRust
（b) AkiraRust Framework: The Detail Design of Adaptive Control of States and Transitions
                                                                                                                                                                 4.1   FSM as the Backbone of Repair
Figure 4. AkiraRust Framework: (a) illustrates the AkiraRust work-                                                                                                  An FSM is composed of a finite set of states, a set of input sym-
flow. (b) presents the detailed design of AkiraRust. ❶ and ❷ inte-                                                                                               bols, transition functions, and output mappings that describe the
grate a dual-mode multi-agent library, mapping to the FSM states                                                                                                 evolution of the system over time [6, 24]. In our setting, each state
in ❸, while ❹ and ❺ guide state transitions.                                                                                                                     represents a distinct repair agent or thinking mode, reflecting dif-
   Detailed design in Fig. 4(b), existinging Rust researches show                                                                                                ferent cognition or operations during the repair process. State tran-
that [10, 18, 29] Rust repair method can be categorized into three                                                                                               sition conditions are determined by runtime semantic feedback
types: (i) replacements with Safe Rust equivalents, (ii) assertion-                                                                                              signals, including repair success, semantic correctness, and halluci-
based prevention, and (iii) semantic-level modifications. Based on                                                                                               nation likelihoods. Therefore, the FSM can be formally defined as a
these, we developed a multi-agent repair library, where each agent                                                                                               six-tuple 𝐹𝑆𝑀 = (Σ, 𝑆, 𝑠 0, 𝐹, 𝛿, 𝜆), where:
    • Input: Σ = {𝑟 | Rust Code}, representing the set of input
      programs or repair candidates evaluated during the process.
    • State Set: Each state corresponds to a specific phase: 𝑆 =
      {𝑞 0, 𝑞𝑎𝑠𝑠𝑒𝑟𝑡 , 𝑞𝑚𝑜𝑑𝑖 𝑓 𝑦 , 𝑞𝑟𝑒𝑝𝑙𝑎𝑐𝑒 , 𝑞𝑘𝑛𝑜𝑤𝑙𝑒𝑑𝑔𝑒 , 𝑞𝑟𝑜𝑙𝑙𝑏𝑎𝑐𝑘 , 𝑞𝐸𝑟𝑟 , 𝑞 𝐹 }. 𝑞 0
      and 𝑞 𝐹 are the initial and final states, 𝑞𝐸𝑟𝑟 terminates re-
      pair afteron repeated failures, and the others are defined in
      Sec. 2.1.
    • Initial State: 𝑠 0 = 𝑞 0
    • Final State Set: 𝐹 = {𝑞 𝐹 , 𝑞𝐸𝑟𝑟 }
    • State Transition Function: 𝛿 : 𝑆 × Σ → 𝑆, defines FSM                                   Figure 5. TestGenAgent: User-Intent–Guided Test Agent.
      transitions driven by code-context.                                                 Given a repaired candidate, TestGenAgent first summarizes key
    • Output: 𝜆 : 𝑆 → Σ, refers Rust repair code.                                         code features and infers potential modification points (❶ in Fig. 5),
     For a Rust program detected with UBs by static or dynamic tools                      such as mismatched allocation–deallocation pairs or alignment-
(e.g., Miri [26]), AkiraRust initializes it as the FSM’s initial state                    sensitive memory operations. It then analyzes these points to de-
𝑞 0 , with input symbols Σ determined by the error type and seman-                        rive intent-aligned semantic constraints and generate candidate
tic context. Under feedback-driven transition conditions, the FSM                         behavioral conditions (❷ in Fig. 5). Based on these constraints, the
dynamically invokes appropriate repair agents to generate repair                          agent produces repair-aware semantic variants and synthesizes
code. When the defect is successfully fixed and passes compilation                        unit tests that exercise the inferred behaviors; if at least one variant
and semantics checks, the FSM reaches the final state 𝑞 𝐹 ; otherwise,                    passes all generated tests, the repair is considered acceptable (❸
after exceeding the maximum transition limit, it enters the error                         in Fig. 5). This process enables exploring a wider range of repair
state 𝑞𝐸𝑟𝑟 , indicating repair failure. Next, we present the design of                    variations, improving test coverage while ensuring the repaired
the dual-mode multi-agent library is detailed, including its mapping                      code’s semantics remain within the intended behavioral bounds.
to the FSM state set and the corresponding transition mechanism.                          Accuracy. We discuss the false negative/positive [34] of TestGe-
                                                                                          nAgent to analyze its accuracy in semantic validation. The results
4.1.1 Dual-Mode Multi-Agents State. Existing Rust automated                               show semantic evaluation achieves 85% accuracy: 10% false nega-
frameworks rely on fixed templates and rigid orchestration, result-                       tive, where abnormal behaviors that may violate Rust’s safety or
ing in inflexible repair processes. Compared to C language unsafe                         intended semantics are mistakenly classified as normal, potentially
operations [11, 23], the finiteness of Unsafe Rust provides a well-                       compromising program correctness; and 5% false positive, where
defined opportunity to systematically categorize and manage repair                        normal behaviors are misclassified as abnormal, leading to extra
strategies. Firstly, the repair patterns are limited and can be classi-                   semantic checks or rollbacks and increased overhead (Tab. 2).
fied into three types: replacement with Safe Rust, assertion-based
                                                                                                 Table 2. Semantic evaluation results of TestGenAgent
prevention, and semantic modification [10, 18]. Then, LLM thinking
modes can be divided into two typical approaches: fast thinking                                                   Predicted Abnormal            Predicted Normal
performs rapid repairs based on heuristics and contextual match-                            Actual Abnormal          True Positive: 0.78        False Negative: 0.10
ing, whereas slow thinking conducts deep semantic reasoning and                             Actual Normal            False Positive: 0.05       True Negative: 0.07
contextual consistency analysis. We abstract the above repair pat-
terns and reasoning modes into a set of orthogonal basis vectors to                          Overall, this dual-mode multi-agent library efficiently reuses
construct a dual-mode multi-agent library.                                                existing agents and enables flexible composition of repair strategies,
   To fully leverage existing capabilities and reduce redundant im-                       allowing agents to adapt adaptively based on code-context. These
plementation, existing Rust repair tools and specialized agents are                       agents are further abstracted as distinct states within the FSM, with
integrated into the framework, including assertion, modification, re-                     each state corresponding to a specific repair intention.
placement, and knowledge agents. Besides, we introduce evaluation                         4.1.2 Transformation and Coordination among States. To
agents to perform semantic validation. Rust’s memory safety mech-                         capture the dynamic evolution of repair behaviors and enable coor-
anism makes semantic correctness challenging, even experienced                            dinated reasoning across multiple agents, AkiraRust introduces a
developers spend over 15% of their time writing unit tests [7, 40].                       state transformation mechanism, which uses runtime indicators to
While compiler tools detect memory and type errors, they do not                           represent the evolving repair context and adaptively select the most
capture higher-level semantic intent or behavioral correctness (e.g.,                     suitable next repair agent and modes from library states. Formally,
unsafe blocks that compile but violate aliasing). Existing LLM-aided                      the state transformation is expressed as:
semantic validation methods, like CodeJudge [32] rely on prompt
engineering with other LLMs to judge semantic; test generation                                                 𝛿 : (𝑆𝑡 , 𝛼𝑡 ) ↦−→ (𝑆𝑡 +1, 𝐴𝑡 +1 )
methods (e.g, RUG [7], Rust-twins [37]) focus on syntactic cor-                           where 𝑆𝑡 is the current FSM state and Σ𝑡 is the vector of runtime
rections or surface-level consistency, neglecting the underlying                          signals, the next state 𝑆𝑡 +1 and the agent action output 𝐴𝑡 +1 .
semantic. However, the correct repair ultimately depends on the                              The transformation mechanism operates in two complementary
developer’s intention. For instance, in cases of misaligned alloc and                     stages: (i) the front-end performs a fast, local evaluation of the
dealloc, the goal is to ensure memory alignment, but which variable                       current Rust code state, which a lightweight check derived directly
to adjust and how to align it requires understanding the intended be-                     from runtime signals, by inspecting the runtime signal vector 𝛼𝑡 , in-
havior. Therefore, we propose a TestGenAgent that leverages Rust’s                        cluding UB counts, types, and semantic context from TestGenAgent.
strong type system and the built-in testing pipeline (“cargo test”)                       When the UB count is zero, the current state is considered a “stable
to perform intent-guided test generation and semantic validation.                         candidate” for subsequent verification. Otherwise, the framework
AkiraRust: Re-thinking LLM-aided Rust Repair Using a Feedback-guided Thinking Switch


uses the LLM to extract potential UB keyword tags to reflect the                       a low-variance region, AkiraRust invokes TestGenAgent to evaluate
current semantic context. (ii) the back-end builds a FixAgent that                     the current code’s semantic correctness. When these two moni-
selects appropriate 𝑆𝑡 +1 (agent and mode) based on 𝛼𝑡 . Given Rust’s                  toring points are detected, AkiraRust evaluates the current state
strong typing and ownership rules, AkiraRust maintains a dynamic                       semantic or rollback to the lowest-incorrectness score.
knowledge base that accumulates prior repair experience, enabling                         Overall, this design enhances the FSM’s transition mechanism
the FixAgent to more accurately choose the next state 𝑆𝑡 +1 and                        in AkiraRust by lightweight monitoring repair dynamics, avoiding
generate the corresponding action 𝐴𝑡 +1 . Overall, this transforma-                    redundant semantic checks and unnecessary full rollbacks, reducing
tion guides adaptive adjustment of repair path, achieving stepwise                     runtime overhead while maintaining repair accuracy (Sec. 5).
agent/mode selection and context-aware repair orchestration.

4.2   Self-Adaptive Correction Mechanism                                               5   Evaluation
   We analyze the overhead of AkiraRust within the FSM frame-                             The evaluation of AkiraRust designed to answer the following
work: (i) semantic evaluation is required for each intermediate Rust                   research questions:
code, and (ii) hallucinations (reflected in the final code state) trigger
direct rollback to the initial state. From Insight 3, hallucination                        1. RQ1 (Accuracy): What extent is AkiraRust successful in
depends not only on the performance of final states but also on the                           fixing Rust UBs as measured by metrics of pass and exec?
overall judgment across the entire repair process, direct rollback                         2. RQ2 (Adaptive): How does AkiraRust’s adaptation affect
neglecting intermediate repair progress may increase semantic eval-                           repair semantic correctness?
uation overhead. Therefore, AkiraRust implements a self-adaptive                           3. RQ3 (Advancement): How does the efficiency and perfor-
correction mechanism driven by waveform feedback to strength the                              mance of AkiraRust in eliminating UBs compared to the
transformation mechanism. It continuously monitors the runtime                                SOTA method and human experts?
dynamics of the repair state and determines optimal evaluation or
rollback point, reducing semantic validation and rollback overhead.                       Firstly, we give a brief explanation of the datasets, large language
                                                                                       models, baselines and metrics used in this paper.
                                                                                       Datasets. We use Rust UBs dataset from the Miri compiler [26]. The
                                                                                       dataset covers 47 common UB types, including allocation errors,
                                                                                       concurrency, data races, and borrow violations, spanning diverse
                                                                                       scenarios such as multi-threading and cross-module conflicts.
                                                                                       LLMs. We use three LLMs: GPT-4 [27], GPT-5 [28], and Claude-
                                                                                       3.5 [2], each with a default temperature of 0.5.
                                                                                       Baselines. We select both template-based frameworks (Thetis-
                                                                                       lathe [17], TECS’25) and LLM-based Rust repair frameworks (e.g.,
                                                                                       RustAssistant [9], ICSE’25), which represent a single-process tool,
          Figure 6. Self-Adaptive Correction Mechanism.
                                                                                       while RustBrain [18] (DAC’25) serves as a multi-process tool.
   Specifically, AkiraRust first collects the runtime context gen-                     Metrics. All experiments report pass rate(%) and exec rate(%),
erated after each state transition, including UB reports, seman-                       among which pass rate refers to the percentage of code passing
tic, and structural information as logs, and maps them to a fixed-                     Miri, and exec rate refers to the percentage of code that passes
dimensional error-signal vector. Based on prior studies [10, 12,                       semantic correctness checks during evaluation by TestGenAgent.
17, 19], AkiraRust classifies various types of unsafe code into sev-                      Subsequently, we analyze the results to answer these questions.
eral typical classifications (❶ in Fig. 6), and constructs a fixed-                    RQ1 (Accuracy): We evaluated AkiraRust’s repair pass and exec
dimensional signal channel set: 𝑓 (𝑡) = [𝑈 (𝑡), 𝐺 (𝑡), 𝐼 (𝑡), 𝐿(𝑡), 𝐶 (𝑡)]             rate using various LLM configurations. In Fig. 7, using an LLM
, where each component corresponds to a specific category of run-                      alone, even GPT-5, only achieves a 75% pass rate, failing to handle
time errors, unchecked operations (𝑈 ), global objects (𝐺), inter-                     complex ownership, lifetime, and aliasing issues in dataset. Aki-
operability (𝐼 ), low-level control (𝐿), and concurrency objects (𝐶).                  raRust achieves a 100% pass rate, demonstrating that all generated
Then, by normalizing thees signals 𝑓 (𝑡) (❷ in Fig. 6), AkiraRust eval-                patches compile and satisfy basic functional constraints. We further
uates code repair scores, and constructs a unified defect-evolution                    validate semantic correctness. In Fig. 8, due to Rust’s strict compiler
waveform E(t) over time (❸ in Fig. 6). This waveform is a curve of                     rules, and the lack of sufficient domain-specific training data, di-
code-incorrectness scores that reflects how repair quality evolves:                    rectly using general-purpose LLMs (GPT-4, GPT-5, Claude 3.5) for
        Í
𝐸 (𝑡) = 𝑖 𝑤𝑖 · 𝑔𝑖 (𝑓𝑖 (𝑡)) . Here, 𝑤𝑖 denotes each error type’s weight,                repair achieves only modest semantic exec rates (typically 25–50%).
derived from historical repair frequency and severity, and 𝑔𝑖 (·) is                   In contrast, AkiraRust, across different underlying LLMs, maintains
a temporal smoothing function capturing error persistence over                         consistently high exec rates (≈ 85–95%), representing a 40–60%
time. Finally, based on the code-incorrectness scores, we define                       improvement over standalone LLM-based repair approaches. We
a set of monitoring rules and critical-point criteria to enhancing                     observe that although stronger LLMs (AkiraRust+GPT-5, compared
the state transition mechanism, from which two monitoring points                       with AkiraRust+GPT-4/Claude-3.5) yield slightly higher exec rates,
are derived (❹ in Fig. 6): (i) Rollback Points, triggered when the                     AkiraRust leverages FSM structure and waveform-guided adaptive
waveform sharply fluctuates or exceeds a threshold, indicating in-                     mechanism to select more suitable reasoning trajectories, narrow-
stability or semantic drift. When detected, AkiraRust stops further                    ing the performance gap between models. This makes to uniformly
modifications and rollback to the initial code state. (ii) Semantic                    high semantic repair accuracy and effectively decouples repair qual-
Evaluation Points, activated when the waveform stabilizes within                       ity from raw LLM reasoning capacity.
                                                                 Claude-3.5         GPT-4                    GPT-5         GPT-4+AkiraRust                                                                                             GPT-4+AkiraRust                                 GPT-5+AkiraRust                                          Claude-3.5+AkiraRust         Claude-3.5+RustBrian
                                                                         GPT-5+AkiraRust                       Claude-3.5+AkiraRust                                                                                                                                               GPT-4+RustBrian                                            RustAssisant        Thetis-lathe
                                 100                                                                                                                                                                      100
          Code pass by Miri(%)




                                 80




                                                                                                                                                                                    Execution(%)
                                                                                                                                                                                                          80
                                 60                                                                                                                                                                       60
                                 40
                                                                                                                                                                                                          40
                                 20
                                                                                                                                                                                                          20
                                  0
                                            c            r                    nce                                    ll        ter                       ity
                                                                  ic                       ow      race                                  rrow                            ned
                                                                                                               .ca                                                                                         0
                                       allo          inte      pan        ena         borr                               .poin                  vali
                                                                                                                                                     d
                                                                                                                                                                    alig
                                                 gpo                                          data        func                       kbo                                                                        allo
                                                                                                                                                                                                                     c        inte
                                                                                                                                                                                                                                   r
                                                                                                                                                                                                                                                                     pan
                                                                                                                                                                                                                                                                             ic                                nce          ow      race                                    .call         ter        rrow       dity          ed
                                            glin                     prov        both                                func        stac                          un
                                                                                                                                                                                                                          gpo                                                              ena                         borr    data                                  func           .poin        kbo        vali          lign
                                       dan                                                                                                                                                                           glin                                                    prov                                 both                                                         func         stac                       una
                                                                                                                                                                                                                dan
                                         Figure 7. AkiraRust Repairs UBs Pass Rate by Miri.                                                                                                                     Figure 10. Comparative of AkiraRust and Existing Tools.
                                                                 Claude-3.5         GPT-4                    GPT-5         GPT-4+AkiraRust
                                                                         GPT-5+AkiraRust                       Claude-3.5+AkiraRust
                                 100




                                                                                                                                                                                                                                                                                                                                             Agent inovking number
                                                                                                                                                                                                                                               Unchecked Operation




                                                                                                                                                                                                                                                                                                                                                                     40
          Execution(%)




                                 80
                                                                                                                                                                                                                                                                       107
                                                                                                                                                                                                                                                                                                                                     total



                                                                                                                                                                                                                                                                                                                                                                                                                   RustBrain
                                 60
                                                                                                                                                                                                                                                                                                                                                                                                                   AkiraRust
                                                                                                                                                                                                                                                                                                                                     exec




                                                                                                                                                                                                                                                                                                                                                                     30
                                 40

                                 20                                                                                                                                                  Concurrent objects
                                                                                                                                                                                                                                                                                                                     Global object
                                                                                                                                                                                                                                                                                                                                                                     20
                                                                                                                                                                                                                                          21




                                  0
                                                                                                                                                                                                                                                                                                                                                                     10
                                                                                                                                                                                                                                                                                  8




                                            c            r                   nce                              .call        ter                      dity
                                       allo          inte      pan
                                                                  ic
                                                                         ena         borr
                                                                                          ow      race               .poin           rrow       vali              lign
                                                                                                                                                                         ed
                                                 gpo                                         data         func                   kbo                           una
                                            glin                     prov       both                             func        stac
                                       dan
                                                                                                                                                                                                                                                                                                                                                                      0
                                 Figure 8. AkiraRust Repairs UBs Semantic Execution Rate.                                                                                                                                                                                             24




                                                                                                                                                                                                                                                                                                                                                                      ali
                                                                                                                                                                                                                                                                                                                                                                            as     ite
                                                                                                                                                                                                                                                                                                                                                                                 wr cce mat
                                                                                                                                                                                                                                                                                                                                                                                           ss   ch etag ters cess wice
                                                                                                                                                                                                                                                                                                                                                                                                    r      in          t
                                                                                                                                                                                                                                                                                                                                                                                       a     is          po ic ac lloc
                                                                                                                                                                                                                                                     57




                                 5                                                                                                                                                                                                                                                                                                                                                     siz
                                                                                                                                                                                                                                                                                                                                                                                          em
                                                                                                                                                                                                                                                                                                                                                                                                  ng
                                                                                                                                                                                                                                                                                                                                                                                                     ling atom dea
                                                  rollback                                                                        AkiraRust with Rollback                                                                                                                                                                                                                                       da
Incorrectness Score




                                                                                                                                  AkiraRust without Rollback
                                                                                                                                                                                                                                                                                            Interoperability
                                                                                                                                                                                                                   Low-level control




                                 4                                                                                                RustBrain with Direct Rollback                    Figure 11. AkiraRust Repair per- Figure 12. Comparison of Agent
                                                                                              rollback
                                 3                                                                                                       failure
                                                                                                                                                                                    formance across different Types. Invocation Counts.
                                 2                                                                                                                                     rollback
                                                    rollback
                                 1                                       success                                                                                          success   RustBrain [18], SOTA Rust repair tool). In Fig. 10, AkiraRust also
                                                      next solution                next solution           next solution                 next solution
                                                                                                                                                                                    achieves a semantic correctness of 92%, compared to RustAssistant
                                     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24                                                                               and RustBrain, the exec rate of AkiraRust increased by 15% and
                                                                                                   Steps
                                                                                                                                                                                    50%, respectively, while maintaining performance comparable to
Figure 9. Comparison of AkiraRust Adaptive Rollback, Non-                                                                                                                           Thetis-Lathe. However, Thetis-Lathe is restricted to template UB
Rollback, and RustBrain Direct Rollback in Repairing Rust UBs.                                                                                                                      patterns and fails to generalize beyond predefined rules, limiting
RQ2 (Adaptive): AkiraRust’s adaptive are primarily reflected in                                                                                                                     its applicability to real-world unsafe Rust defects.
three aspects: agent selection, LLM reasoning mode, and the oc-                                                                                                                         To evaluate AkiraRust’s effectiveness, we report the number of
currence of hallucinated code (Sec. 2). While the first two aspects                                                                                                                 agent invocations (Fig. 12) and the execution time (Tab. 3), reflecting
are validated by repair accuracy, we focus on the self-adaptive cor-                                                                                                                both repair process cost and runtime efficiency. AkiraRust reduces
rection mechanism. Here, we evaluate AkiraRust’s adaptability to                                                                                                                    overhead by 7× compared to human experts and shortens repair
different UB types and its ability to mitigate hallucination-driven                                                                                                                 time by about 2× relative to RustBrain (Fig. 12). This is because, for
deviations during the repair process.                                                                                                                                               complex errors (e.g., aliasing violations), RustBrain must enumerate
   First, we categorize the dataset samples by the Unsafe Rust error                                                                                                                and execute multiple solutions, resulting in about 2× the number
types 𝑓 (𝑡) (See Sec. 4.2) and evaluate AkiraRust’s repair perfor-                                                                                                                  of agent invocations compared to AkiraRust. For simpler repairs
mance within each types. In Fig. 11, AkiraRust maintains consis-                                                                                                                    (e.g., double dealloc), AkiraRust, due to its lightweight monitoring
tently high and close repair quality across all categories (about 86%-                                                                                                              (Sec. 6), invokes agents slightly more frequently than RustBrain,
92%), indicating that its adaptive mechanism adjusts the reasoning                                                                                                                  but the additional cost is minimal (green in Tab. 3). Furthermore, we
trajectory according to both the error type and context, rather than                                                                                                                compare AkiraRust under different LLMs, stronger models (GPT-5)
relying on error-specific. Then, we select a representative complex                                                                                                                 converge faster, yet all variants still outperform RustBrain.
UB case and evaluate it under AkiraRust and RustBrain across three                                                                                                                      Overall, AkiraRust provides a dynamically adaptive framework
strategies: adaptive rollback (AkiraRust), non-rollback (AkiraRust),                                                                                                                to repair Rust UBs, improving semantic repair correctness, adapt-
and direct rollback (RustBrain). In Fig. 9, for RustBrain, N solution                                                                                                               ing its reasoning trajectory to diverse UB types vian FSM-driven
processes are generated to perform repairs, and a direct rollback                                                                                                                   agent/mode selection, and reducing repair time and verification
occurs whenever a round fails. In this case, it takes four rounds (in-                                                                                                              overhead compared with SOTA methods and human experts.
voking 23 agents) to complete the repair. Without adaptive rollback,
AkiraRust would allow hallucinated code to persist unchecked, con-                                                                                                                  6                           Conclusion
tinuing to propagate until the maximum iteration limit is reached,                                                                                                                     We’ve introduced AkiraRust, a runtime and adaptive detection-
causing repair failure. In contrast, AkiraRust’s adaptive mechanism                                                                                                                 and-repair tool designed to eliminate UBs and improve repair cor-
identifies rollback points to select the most promising repair path,                                                                                                                rectness and semantic accuracy. Our approach involved leveraging
avoiding hallucination spread and completing the repair with only                                                                                                                   LLMs guided by FSMs to dynamically adapt detection and repair
7 agents invocations. Overall, this adaptive design maintains stable                                                                                                                strategies based on runtime semantic context. To bring this frame-
repair quality across various UB types, while reducing redundant                                                                                                                    work to life, we developed the dual-mode multi-agent system, en-
reasoning and preventing the accumulation of illusions.                                                                                                                             abling fast and slow reasoning modes to coordinate multiple agents
RQ3 (Advancement): To evaluate the effectiveness and efficiency                                                                                                                     performing diverse tasks, and designed a state transition mecha-
of AkiraRust, we compare it against a static template-based method                                                                                                                  nism to dynamically adjust agent strategies and task sequences,
(Thetis-Lathe [17]), LLM-aided methods (RustAssistant [9] and                                                                                                                       ensuring semantic consistency and stability throughout the repair
AkiraRust: Re-thinking LLM-aided Rust Repair Using a Feedback-guided Thinking Switch


Table 3. Execution Time of AkiraRust VS. Human and SOTA.                                      the Association for Computational Linguistics: EMNLP 2023. 1827–1843.
(Speepup: RustBrain Time (s)/ AkiraRust+GPT-5 Time (s))                                  [15] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2021. RULF: Rust library fuzzing via
                                                                                              API dependency graph traversal. In 2021 36th IEEE/ACM International Conference
                                  Average Time/s                                              on Automated Software Engineering (ASE). IEEE, 581–592.
       Types       Rust            AkiraRust                            Speedup          [16] Renshuang Jiang, Pan Dong, Yan Ding, Ran Wei, and Zhe Jiang. 2023. Thetis:
                                                            Human
                   Brain    GPT-5 GPT-4 Claude 3.5                                            A Booster for Building Safer Systems Using the Rust Programming Language.
    stack borrow    254     190.6    149     107.5             366         1.3x               Applied Sciences 13, 23 (2023), 12738.
                                                                                         [17] Renshuang Jiang, Pan Dong, Yan Ding, Ran Wei, and Zhe Jiang. 2025. Thetis-
      unaligned     207       90     138      94.5             222         2.3x
                                                                                              lathe: Guidance on Reducing Residual Safety Obstacle in System Software from
       validity     255       52     102      103              678         4.9x               Rust Source Codes. ACM Transactions on Embedded Computing Systems (2025).
         alloc      40       63      68       157              450        0.5x           [18] Renshuang Jiang, Pan Dong, Zhenling Duan, Yu Shi, Xiaoxiang Fang, Yan Ding,
    func_pointer    160       71      64      207              480         2.3x               Jun Ma, Shuai Zhao, and Zhe Jiang. 2025. Unlocking a New Rust Programming
     provenance     183      107     108      150              240        1.71x               Experience: Fast and Slow Thinking with LLMs to Conquer Undefined Behaviors.
         panic      309       89     182      145              336         3.5x               arXiv preprint arXiv:2503.02335 (2025).
                                                                                         [19] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2021.
      func_call     151      151     86       161             1176          1x
                                                                                              Safe systems programming in Rust. Commun. ACM 64, 4 (2021), 144–152.
       dangling      85       65      50      106              114         1.3x          [20] Daniel Kahneman. 2011. Fast and slow thinking. Allen Lane and Penguin Books,
        borrow      243      130     135      220              762         1.9x               New York (2011).
      data_race     294      147     231      173              336         2.0x          [21] Amit Levy, Michael P Andersen, Bradford Campbell, David Culler, Prabal Dutta,
       Average     218.4    101.4 114.6      147.3             442        2.2x                Branden Ghena, Philip Levis, and Pat Pannuto. 2015. Ownership is theft: Experi-
                                                                                              ences building an embedded OS in Rust. In Proceedings of the 8th Workshop on
                                                                                              Programming Languages and Operating Systems. 21–26.
process. Experimentally, AkiraRust exhibited a significant improve-                      [22] Amit Levy, Bradford Campbell, Branden Ghena, Pat Pannuto, Prabal Dutta, and
ment in UB detection and repair accuracy with less overhead.                                  Philip Levis. 2017. The case for writing a kernel in rust. In Proceedings of the 8th
                                                                                              Asia-Pacific Workshop on Systems. 1–7.
                                                                                         [23] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R Cordy, and Ahmed E
7     Acknowledgment                                                                          Hassan. 2022. In Rust we trust: a transpiler from unsafe C to safer Rust. In
                                                                                              Proceedings of the ACM/IEEE 44th international conference on software engineering:
   We appreciate the anonymous reviewers for their helpful feed-                              companion proceedings. 354–355.
back. This paper was written during a special moment in my life.                         [24] Peter Linz and Susan H Rodger. 2022. An introduction to formal languages and
                                                                                              automata. Jones & Bartlett Learning.
Renshuang Jiang sincerely thanks our sweetest little cat, Akira                          [25] Nicholas D Matsakis and Felix S Klock. 2014. The rust language. In Proceedings
Jiang, for joining our lives and filling them with love. Additionally,                        of the 2014 ACM SIGAda annual conference on High integrity language technology.
Shuang would extend her thanks to Zhe Jiang for his continuous                                103–104.
                                                                                         [26] Miri. 2012. Miri_Dataset. https://github.com/rust-lang/miri/tree/master/tests.
support and companionship throughout the years.                                               Accessed: 2025-08-26.
                                                                                         [27] OpenAI. 2023. GPT-4. https://platform.openai.com/docs/models/gpt-4. Accessed:
References                                                                                    2025-08-26.
                                                                                         [28] OpenAI. 2025. GPT-5 Mini. https://platform.openai.com/docs/models/gpt-5.
 [1] Brian Anderson, Lars Bergstrom, Manish Goregaokar, Josh Matthews, Keegan                 Accessed: 2025-08-26.
     McAllister, Jack Moffitt, and Simon Sapin. 2016. Engineering the servo web          [29] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Un-
     browser engine using Rust. In Proceedings of the 38th international conference on        derstanding memory and thread safety practices and issues in real-world Rust
     software engineering companion. 81–89.                                                   programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
 [2] Anthropic. 2025. Claude 3.5. https://www.anthropic.com/ai-research/claude-3.             Language Design and Implementation. 763–779.
     Accessed: 2025-08-26.                                                               [30] Xiaoye Qu, Yafu Li, Zhaochen Su, Weigao Sun, Jianhao Yan, Dongrui Liu, Ganqu
 [3] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexan-         Cui, Daizong Liu, Shuxian Liang, Junxian He, et al. 2025. A survey of efficient
     der J Summers. 2020. How do programmers use unsafe rust? Proceedings of the              reasoning for large reasoning models: Language, multimodality, and beyond.
     ACM on Programming Languages 4, OOPSLA (2020), 1–27.                                     arXiv preprint arXiv:2503.21614 (2025).
 [4] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J Summers. 2019.    [31] Rust. 2012. Rust example library. https://doc.rust-lang.org/std/. Accessed:
     Leveraging Rust types for modular specification and verification. Proceedings of         2025-08-26.
     the ACM on Programming Languages 3, OOPSLA (2019), 1–30.                            [32] Weixi Tong and Tianyi Zhang. 2024. Codejudge: Evaluating code generation
 [5] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2024. Repairagent: An             with large language models. arXiv preprint arXiv:2410.02184 (2024).
     autonomous, llm-based agent for program repair. arXiv preprint arXiv:2403.17134     [33] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Samp-
     (2024).                                                                                  son. 2022. Verifying dynamic trait objects in rust. In Proceedings of the 44th In-
 [6] Daniel Brand and Pitro Zafiropulo. 1983. On communicating finite-state ma-               ternational Conference on Software Engineering: Software Engineering in Practice.
     chines. Journal of the ACM (JACM) 30, 2 (1983), 323–342.                                 321–330.
 [7] Xiang Cheng, Fan Sang, Yizhuo Zhai, Xiaokuan Zhang, and Taesoo Kim. 2025.           [34] wIKIPEDIA. 2012. False positives and false negatives. https://en.wikipedia.org/
     RUG: Turbo LLM for Rust Unit Test Generation. In 2025 IEEE/ACM 47th In-                  wiki/False_positives_and_false_negatives. Accessed: 2025-08-26.
     ternational Conference on Software Engineering (ICSE). IEEE Computer Society,       [35] wIKIPEDIA. 2012. Source lines of code. https://en.wikipedia.org/wiki/Source_
     634–634.                                                                                 lines_of_code. Accessed: 2025-08-26.
 [8] Wim De Neys. 2023. Advancing theorizing about fast-and-slow thinking. Be-           [36] Xingbo Wu, Nathanaël Cheriere, Cheng Zhang, and Dushyanth Narayanan. 2023.
     havioral and Brain Sciences 46 (2023), e111.                                             Rustgen: An augmentation approach for generating compilable rust code with
 [9] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, Rishi Poddar, and Aseem                large language models. (2023).
     Rastogi. 2025. RustAssistant: Using LLMs to fix compilation errors in Rust code.    [37] Wenzhang Yang, Cuifeng Gao, Xiaoyuan Liu, Yuekang Li, and Yinxing Xue. 2024.
     In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE).           Rust-twins: Automatic rust compiler testing through program mutation and dual
     IEEE Computer Society, 3097–3109.                                                        macros generation. In Proceedings of the 39th IEEE/ACM International Conference
[10] Yan Dong, Zhicong Zhang, Mohan Cui, and Hui Xu. 2024. SafeNet: Towards                   on Automated Software Engineering. 631–642.
     mitigating replaceable unsafe Rust code via a recommendation-based approach.        [38] Jia-Yu Yao, Kun-Peng Ning, Zhen-Hui Liu, Mu-Nan Ning, Yu-Yang Liu, and Li
     Software Testing, Verification and Reliability 34, 5 (2024), e1875.                      Yuan. 2023. Llm lies: Hallucinations are not bugs, but features as adversarial
[11] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Trans-                 examples. arXiv preprint arXiv:2310.01469 (2023).
     lating C to safer Rust. Proceedings of the ACM on Programming Languages 5,          [39] Yuchen Zhang, Ashish Kundu, Georgios Portokalidis, and Jun Xu. 2023. On
     OOPSLA (2021), 1–29.                                                                     the dual nature of necessity in use of Rust unsafe code. In Proceedings of the
[12] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer.           31st ACM Joint European Software Engineering Conference and Symposium on the
     2024. Refinedrust: A type system for high-assurance verification of Rust pro-            Foundations of Software Engineering. 2032–2037.
     grams. Proceedings of the ACM on Programming Languages 8, PLDI (2024),              [40] Shuofei Zhu, Ziyi Zhang, Boqin Qin, Aiping Xiong, and Linhai Song. 2022. Learn-
     1115–1139.                                                                               ing and programming challenges of rust: A mixed-methods study. In Proceedings
[13] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii,           of the 44th International Conference on Software Engineering. 1269–1281.
     Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in
     natural language generation. ACM computing surveys 55, 12 (2023), 1–38.
[14] Ziwei Ji, Tiezheng Yu, Yan Xu, Nayeon Lee, Etsuko Ishii, and Pascale Fung.
     2023. Towards mitigating LLM hallucination via self reflection. In Findings of
