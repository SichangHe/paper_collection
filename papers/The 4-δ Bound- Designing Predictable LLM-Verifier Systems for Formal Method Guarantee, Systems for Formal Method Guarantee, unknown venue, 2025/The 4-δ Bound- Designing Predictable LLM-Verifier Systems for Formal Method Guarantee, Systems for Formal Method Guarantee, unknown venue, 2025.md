                                               The 4/δ Bound: Designing Predictable LLM-Verifier
                                                     Systems for Formal Method Guarantee

                                             Pierre Dantas1,2*, Lucas Cordeiro1,2† , Youcheng Sun1† , Waldir Junior2†
                                                      Dept. of Computer Science, The University of Manchester, UK.
                                                     1*
                                         2
                                             Dept. of Electrical Engineering, Federal University of Amazonas (UFAM), Brazil.
arXiv:2512.02080v3 [cs.AI] 24 Jun 2026




                                               *Corresponding author(s): pierre.dantas@gmail.com, 0000-0001-6390-9340;
                                              Contributing authors: lucas.cordeiro@manchester.ac.uk, 0000-0002-6235-4272;
                                                techieyoucheng@gmail.com, 0000-0002-1893-6259; waldirjr@ufam.edu.br,
                                                                          0000-0003-3095-0042;
                                                            †
                                                              These authors contributed equally to this work.


                                                                                        Abstract
                                             The integration of Formal Verification tools with Large Language Models (LLMs) offers a path
                                             to scale software verification beyond manual workflows. However, current methods remain unre-
                                             liable: without a solid theoretical footing, the refinement process acts as a black box that may
                                             oscillate, loop, or diverge. This work bridges this critical gap by developing an LLM-Verifier
                                             Convergence Theorem, providing the first formal framework with provable guarantees for termi-
                                             nation in multi-stage verification pipelines. We model the interaction not as a generic loop, but
                                             as a sequential absorbing Markov Chain comprising four essential engineering stages: CodeGen,
                                             Compilation, InvariantSynth, and SMTSolving. We prove that for any non-zero stage success
                                             probability (δ > 0), the system reaches the Verified state almost surely. Furthermore, because
                                             of the sequential nature of the pipeline, we derive a precise latency bound of E[n] ≤ 4/δ. We
                                             stress-tested this prediction in an extensive empirical campaign comprising over 90,000 trials.
                                             The results match the theory with striking consistency: every run reached verification, and the
                                             empirical convergence factor clustered tightly around Cf ≈ 1.0, confirming that the 4/δ bound
                                             accurately mirrors system behavior rather than serving as a loose buffer. Based on this data,
                                             we identify three distinct operating zones – marginal, practical, and high-performance – and
                                             propose a dynamic calibration strategy to handle parameter drift in real-world environments.
                                             Together, these contributions replace heuristic guesswork with a rigorous architectural foun-
                                             dation, enabling predictable resource planning and performance budgeting for safety-critical
                                             software.

                                             Keywords: Formal Verification, Large Language Models, SMT Solvers, Bounded Model Checking,
                                             Automated Program Repair, Specification Synthesis, ESBMC




                                                                                            1
1 Introduction
Formal software verification is essential in areas such as aerospace [1], medical devices [2], and
autonomous systems [3]. It uses mathematical methods to check that systems work as intended. For
example, techniques such as Bounded Model Checking (BMC) [4] analyze software to detect hidden
problems, such as numerical errors and memory-safety issues. Regular testing often misses these
kinds of issues. Tools such as Efficient SMT-based Context-Bounded Model Checker (ESBMC) [5, 6]
help with this process [7]. However, a significant specification bottleneck limits widespread adoption:
the extensive manual effort required to formulate precise formal specifications from ambiguous
requirements [8].
    We now have a few solid ways to handle this problem, thanks to the recent arrival of large
language models (LLMs). These models are proving incredibly useful; for example, they can easily
generate formal specifications [9], construct tricky loop invariants [10], and significantly speed up
automated program repair [11]. Despite the promising results mentioned, a central problem remains:
the process that improves the use of LLMs and verifiers does not always guarantee precise and reli-
able outcomes [9–11]. Although researchers have developed strong theoretical foundations for both
LLMs [12, 13] and Formal Verification tools [4, 5, 7] individually, they have not yet mathematically
analyzed how these components behave when used together in an iterative process [14, 15]. This
gap causes the system to behave unpredictably, making it unsafe to use in critical areas.
    The Fundamental Gap addressed in this work: Unpredictable Artificial Intelligence (AI)-
Verifier Interactions. We cannot predict how AI and Verifiers will interact in multi-stage workflows.
Mixing statistical AI components with reliable, deterministic verification tools creates a core conflict
that current methods have not solved mathematically. Even though specific tests look promising [10,
16], we lack a reliable convergence theory for the repeated refinement cycles typical of modern
verification pipelines. Most existing approaches treat LLM refinement as a generic “black box” loop,
ignoring the sequential engineering dependencies required to build valid proofs. This missing piece
creates three problems that prevent the deployment of these systems in real-world applications:
 1. Unpredictable Termination: Without mathematical guarantees that the sequential process
    will converge, the refinement can get stuck in intermediate stages (e.g., oscillating between syn-
    tax errors and logical failures) or wander off track. This unpredictability makes it unreliable for
    safety-critical scenarios like flight control, where a guaranteed end to the process is mandatory.
 2. Unbounded Resource Consumption: The absence of a defined step limit precludes the con-
    figuration of reliable timeouts. In a multi-stage pipeline, costs accumulate; without a theoretical
    ceiling, the process could run out of control, consuming all available memory or processing
    time until the application crashes.
 3. Lack of Performance Predictability and Stability: It is currently a guessing game. Engi-
    neers have no systematic way to connect an LLM’s capability to its total verification latency.
    Furthermore, the assumption that LLM performance is constant (stationary) is often violated
    in practice, leaving engineers without strategies to detect or mitigate performance drift during
    operation.
   These limitations can lead to serious problems in the real world, making systems unsafe and
rendering resource planning impossible.
   Our Proposed Approach: A Convergence Theorem for Sequential LLM-Verification. We
tackle the problem of guarantees using a new Convergence Theorem based on a sequential absorb-
ing Markov Chain. We model the verification process not as a generic loop but as a structured
pipeline comprising four essential engineering stages: CodeGen , Compilation , InvariantSynth ,
and SMTSolving .
   Figure 1 illustrates our integrated LLM-Verifier Convergence Framework. The diagram depicts
the sequential flow from the initial Unverified state through four milestones – CodeGen (s1 ),
 Compilation (s2 ), InvariantSynth (s3 ), and SMTSolving (s4 ) – to the final Verified absorb-
ing state (s5 ). By modeling these dependencies as a sequential absorbing Markov Chain, where
δ governs the transition to the next stage (si → si+1 ), we derive rigorous theoretical guarantees
(E[n] ≤ 4/δ). A feedback loop links real-world testing to the theoretical model, supporting the


                                                   2
dynamic calibration strategy to handle parameter non-stationarity in deployment. By continuously
monitoring the empirical success rate (δ̂) against the theoretical stability regions, this mechanism
detects performance drift (e.g., when δ̂ drops into the marginal region) and triggers corrective
actions – such as context resets or temperature adjustments – to restore the system to the optimal
practical region.

Fig. 1 LLM-Verifier Convergence Framework. The model visualizes the sequential progression through four manda-
tory refinement stages (s1 → s4 ), where δ represents the probability of advancing to the next stage and 1 − δ
represents the probability of retrying the current stage. A feedback loop links real-world testing to the theoretical
model, supporting the dynamic calibration strategy to handle parameter non-stationarity in deployment. By con-
tinuously monitoring the empirical success rate (δ̂) against the theoretical stability regions, this mechanism detects
performance drift (e.g., when δ̂ drops into the marginal region) and triggers corrective actions – such as context resets
or temperature adjustments – to restore the system to the optimal practical region




    In this model, δ quantifies the LLM’s single-attempt success rate for progressing from one stage
to the next. A failure (probability 1 −δ) necessitates a retry of the current stage, while success moves
the artifact closer to the final Verified state. This structured view allows us to move beyond
uncertain guesses [17, 18] and prove that the system will definitely terminate.
    Section 4.2 contains the formal statement of our Theorem, which establishes that for any δ > 0:
   • Guaranteed Convergence: If the program terminates and all reachable states are checked,
     the process is guaranteed to eventually traverse all four stages and reach the Verified state
     almost surely.
   • Bounded Latency: The process is efficient. Because the system must pass through four
     distinct stages (s1 → s4 ), we prove that the expected number of iterations is the sum of the
     expected time for each stage. This yields a precise bound of E[n] ≤ 4/δ, providing a worst-case
     ceiling for resource planning.
   • Exponential Tail Bounds: The likelihood of the process needing more than k steps drops
     off exponentially. This sharp decline enables reliable timeouts with high confidence.
    To address the practical challenge of parameter non-stationarity (performance drift), our frame-
work explicitly supports dynamic calibration. By continuously monitoring the empirical success rate
against the theoretical δ regions, engineers can detect when an LLM drops into the marginal region
and trigger context resets. Together, these results provide a comprehensive architectural founda-
tion: our framework guarantees the process will finish, imposes a hard limit on computational costs
(4/δ), and provides a mechanism to maintain stability in dynamic environments.
    To confirm our framework, we conducted an extensive study involving more than 90,000 sim-
ulations spanning the range 0.1 to 0.9. Our experimental results strongly support our theoretical
predictions and show three distinct behavior patterns (see Table 1).


                                                           3
 Table 1 Performance regions based on δ

  Region                   Range          Description
  Marginal                 δ < 0.3        High variance; requires strict timeouts or dynamic calibration to pre-
                                          vent resource exhaustion.
  Practical             0.3 ≤ δ ≤ 0.6     Optimal for real-world verification tasks with balanced performance
                                          and predictable latency.
  High-Performance         δ > 0.6        Ideal for safety-critical systems requiring fast convergence and mini-
                                          mal variance.




   Paper Organization: This paper is structured as follows: Section 2 reviews related work.
Section 3 provides theoretical background. Section 4 presents our convergence theory. Section 5
details our validation methodology. Section 6 discusses experimental results. Section 7 interprets
these findings. Finally, Section 8 summarizes the work and outlines future directions.

2 Related Work
The integration of LLMs into Formal Verification is a rapidly developing field built upon decades
of foundational work in Formal Methods. This review examines current uses of LLMs, showing how
practitioners integrate them, how these systems are structured, and how they perform. It shows
how the field has developed over time, from traditional methods to modern systems that consider
available resources.
 1. Foundational and Classical Formal Methods (1999–2021): Early work centered on
    developing core verification technologies, such as BMC [4], and applying these techniques to
    safety-critical domains like medical devices [2], aerospace [1], and autonomous systems [3].
    However, the widespread adoption of these powerful methods stalled because the specification
    bottleneck forced practitioners to spend extensive manual effort translating ambiguous natural-
    language requirements into precise formal specifications [8]. The development of advanced tools,
    such as ESBMC [5], accelerated progress in the field; later updates expanded its capabilities,
    including support for C++ templates [19], and provided a strong software foundation. This
    foundation is essential for combining new statistical learning methods.
 2. LLM Integration and Pattern Convergence (2023–2024): The rise of strong LLMs has
    started a new phase in research. This research is quickly focusing on three main ways to use
    these models together:
    (a) Automated Specification and Invariant Generation: This method uses LLMs to
        create formal rules and guidelines from everyday language or code, helping practitioners
        address a longstanding challenge in Formal Methods. Initially, the focus was on producing
        SystemVerilog Assertions to verify the hardware, which significantly improved coverage of
        the checks [20]. Later work in 2024 also utilized LLM-generated invariants to improve the
        efficiency of BMC itself [10].
    (b) Proof Synthesis: This pattern involves employing LLMs to generate full or partial proofs
        for interactive theorem provers. Work in this field has progressed quickly. For example,
        systems like Baldur [21] have achieved high accuracy rates and improved performance in
        environments such as Isabelle/HOL. Subsequent research in 2024 further enhanced proof
        synthesis in languages such as Dafny [22] by using iterative feedback and Chain-of-Thought
        prompting [23, 24].
     (c) Dynamic, Feedback-Driven Approaches: These systems deploy LLMs in a closed
         loop with verifiers, using error feedback to refine artifacts like specifications or proofs
         iteratively. Researchers established this approach using models like Generative Pre-trained
         Transformer-4 (GPT-4) alongside deductive verifiers [14], and specialized frameworks such
         as Formal Verification with Evolutionary Learning (FVEL) later emerged to support fine-
         tuned theorem proving [16].



                                                        4
  3. Closed-Loop Systems (2025–Present): Recent studies are working on creating systems
     that can adjust and improve themselves automatically. A good example of this is the ESBMC-
     AI framework, which helps fix code written in C using BMC [11, 25, 26]. Concurrently, research
     advanced property generation for C code [27], retrieval-augmented generation (RAG) for smart
     contracts [9], automated function modeling [28], and Rust static analysis [29].
    The LLM-Verifier Convergence Theorem establishes the formal conditions under which a
sequence of LLM-generated approximations converges to a verifier-correct solution. It moves beyond
the empirical question of whether a specific prompt or fine-tuning technique works and provides a
theoretical basis for why and how these methods succeed. With this foundation, we can recast the
challenge of model compression not merely as preserving statistical fidelity, but as maintaining the
logical convergence properties defined by the Theorem.
    Table 2 summarizes the significant advancements in LLM-accelerated Formal Verification and
model compression.


Table 2 Chronological advancement in LLM-accelerated Formal Verification

 Advancement                       Description & Key Features               Impact / Results
                                   Foundations and Early Integration (2023)
 Automated Proof Generation        LLMs generate and repair whole           State-of-the-art proof synthesis; 65.7% of
 and Repair (Baldur) [21]          proofs for Formal Verification (e.g.,    theorems proved automatically with Bal-
                                   Isabelle/HOL)                            dur+Thor
 Safety and Trustworthiness        Verification & validation frameworks     Identifies gaps and proposes rigorous
 Verification [15]                 for LLMs, including runtime monitor-     methods for LLM safety and trustworthi-
                                   ing and regulatory compliance            ness
 Prompt Compression (LLM-          Coarse-to-fine prompt compression for    Up to 20× prompt compression with
 Lingua) [30]                      LLMs, maintaining semantic integrity     little performance loss, accelerating infer-
                                   at high compression ratios               ence
                                 Hybrid Systems and Early Optimization (2024)
 Model Compression      Tech-      Quantization, pruning, knowledge dis-    Enable LLM deployment in resource-
 niques [31–37]                    tillation, low-rank approximation, and   limited settings; up to 70%+ compression
                                   hybrid methods for LLMs                  with minimal loss
 LLM-Driven Invariant Gen-         LLMs generate loop invariants for        Improves verification coverage for pro-
 eration for BMC [10]              BMC, avoiding loop unrolling             grams with unbounded loops using
                                                                            ESBMC
 Fine-Tuning and Inference         Parameter-efficient fine-tuning (e.g.,   Reduces resource overhead for adapting
 Optimization [32, 34]             low-rank adaptation (LoRA)), and         and deploying LLMs
                                   inference optimization
                       Advanced Closed-Loop and Specialized Compression (2025)
 Hybrid Verification (LLMs +       Combines LLMs’ cognitive abilities       Hybrid systems address scalability and
 Formal Methods) [14, 38, 39]      with formal rigor for bug detection,     soundness, outperforming standalone
                                   invariant generation, and validation     methods
 ESBMC-AI:       LLM    +          Integrates LLMs with ESBMC for           High-accuracy repair of buffer overflows,
 Bounded      Model Check-         automated vulnerability detection and    pointer errors
 ing [11, 25]                      repair in C code
 Symbolic Compression      for     Formal symbolic compression frame-       Achieves 78.3% token compression and
 Interpretability [40]             work for code generation and logical     improves logical traceability by 62%
                                   reasoning tasks
 Efficient Self-Attention with     Pruning and matrix folding in trans-     70% overall model compression with sta-
 Smart Pruning [35]                former layers for sustainable LLMs       ble or improved performance




                                                          5
3 Theoretical Background
This section establishes the theoretical foundation for the LLM-Verifier Convergence Theorem. We
first detail the verification principles of the ESBMC framework, which provides the deterministic
foundation for our model (Section 3.2). We then characterize the integration of LLMs as genera-
tors of verification artifacts (Sections 3.3 and 3.4). The main idea of our theory is to explain the
refinement process using a model called an absorbing Markov Chain (see Section 3.1.3). The model
builds on a concept called the error-reduction probability (δ). It helps us show that the process will
eventually solve, and it allows us to determine that we need about 4/δ steps to do so. Our the-
ory explains the refinement loop using an absorbing Markov Chain (see Section 3.1.3). This model
builds on a concept called the error-reduction probability (δ). It helps us show that the process is
likely to improve over time and allows us to determine how many steps we need to take, namely 4/δ.

3.1 Mathematical Foundation
This subsection establishes the mathematical basis for simulating the convergence time, E[n], by
leveraging the properties of the Geometric distribution applied to the Markov Chain’s transient
states.

3.1.1 Modeling State Transitions with the Geometric Distribution
Our methodology models the LLM-Verifier system as a five-state absorbing Markov Chain with four
transient states (s1 , s2 , s3 , s4 ) and one absorbing state (s5 , Verified ). The simulation’s efficiency
relies on characterizing the time spent in each transient state.
  • Residence Time (Mj ): The duration of a single stay in a transient state j is measured in
    discrete steps, or iterations. The number of iterations required to exit state j, denoted Mj , is
    modeled by a Geometric random variable. This distribution counts the number of independent
    Bernoulli trials (in this case, iterations) required to achieve the first “success”. We define a
    success as a transition out of state j, and this transition occurs with probability δ in each
    iteration, as shown in (1).

                                P (Mj = k ) = (1 − δ )k−1 δ,       k ∈ {1, 2, 3, . . .}                (1)

  • Expected Single-State Time: The average number of interactions needed to exit a single
    state is the expected value of the Geometric distribution, as shown in Eq. (2).

                                                               1
                                                    E[Mj ] =                                           (2)
                                                               δ

3.1.2 The Vectorized Markov Chain and Total Convergence Time
The total time to reach the absorbing state, T , is the sum of the independent residence times spent
in the four transient states. This summation is the basis for the computational efficiency of the
Vectorized Monte Carlo (VMC) approach.
  • Vectorization Basis: Since the times M1 , M2 , M3 , M4 are random and do not affect each
    other, we can find the total time for the i-th test, which we call Ti , by simply adding these
    times together, instead of simulating each step one by one., as shown in Eq. (3).

                                       Ti = Mi,1 + Mi,2 + Mi,3 + Mi,4                                  (3)

  • Total Expected Convergence Time (E[n]): According to the property of expectation, the
    average total interaction, denoted as E[n], is equal to the sum of the average times spent in
    each of the four stages., as shown in Eq. (4).

                                           4
                                           X                1 1 1 1   4
                                  E[n] =         E[Mj ] =     + + + =                                  (4)
                                           j=1
                                                            δ  δ δ δ  δ


                                                      6
    This equation, E[n] ≤ 4/δ, provides the core theoretical bound and is the target for empirical
validation using the large-scale VMC simulation.

3.1.3 Markovian Properties of LLM-Verifier Interactions
The basis of our convergence theory is the description of how LLM verifiers interact using an
absorbing Markov Chain [41, 42]. In this system, there are specific states known as absorbing states
that, once reached, cannot be changed or left.
    In our framework, the system reaches the Verified state (s5 ) as its final absorbing goal. The
path to this goal involves traversing a sequence of distinct transient states representing engineering
milestones: CodeGen (s1 ), Compilation (s2 ), InvariantSynth (s3 ), and SMTSolving (s4 ).
Recent studies show that LLMs naturally follow these step-by-step reasoning patterns [17, 18],
which matches well with Formal Methods that describe “verification” as a process moving through
defined refinement stages [7, 43].
    Several lines of research support this Markovian characterization:
  • LLM Reasoning as State Transitions: Chain-of-Thought reasoning in LLMs naturally
    follows patterns of moving from one state to another. Each reasoning step depends only on the
    step before it, which matches the Markov property [17, 24, 44].
  • Verification Processes as State Machines: The modeling of verification workflows as state
    transition systems is well-established in Formal Methods literature [7, 8, 43]. Our work extends
    this foundation to incorporate the probabilistic nature of LLM interactions.
  • Probabilistic Program Analysis: Previous research on probabilistic programming [45] and
    probabilistic theorem proving [46] offers a strong theoretical foundation for studying systems
    with random components. These ideas apply directly to LLM-based refinement using Markov
    Chain models.
   In our framework, the Markov property manifests through:
  • State Dependence: The probability of generating a correct verification artifact depends only
    on the current verification state and the LLM’s capability parameter δ.
  • Memoryless Transitions: Each refinement attempt is independent of the specific history of
    previous attempts, conditioned on the current state.
  • Stationary Transition Probabilities: The error-reduction probability δ remains constant
    throughout the refinement process for a given LLM-verifier pair.

Absorbing Markov Chain Theory
Two conditions formally define an absorbing Markov Chain: (i) there exists at least one absorbing
state, and (ii) from every state it is possible to reach an absorbing state in finite steps. States that
are not absorbing are called transient states [41, 42].
    This formulation extends the classical Kripke structure M = (s, s0 , R, L) used in model checking
by introducing probabilistic transitions (see Section 3.2.3). The two frameworks connect clearly:
the set of states S contains both temporary and final states, the initial states s0 represent where
verification begins, and the transition relation R covers probabilistic moves between states.
    The transition matrix P for a chain with t transient states and r absorbing states has the
canonical form, as shown in Eq. (5), where Q is a t × t matrix describing transitions between
transient states, R is a t × r matrix describing transitions from transient to absorbing states, and
Ir is the r × r identity matrix.                          
                                                      Q R
                                              P =                                                    (5)
                                                      0 Ir
    The fundamental matrix N = (It − Q)−1 provides the expected number of visits to transient
states before absorption. The expected number of steps until absorption starting from transient
state i is given by the i-th entry of the vector, as shown in Eq. (6), where 1 is a vector of ones.

                                                t = N1                                              (6)




                                                   7
   For a specific chain structure analyzed in this paper, solving for the expected number of steps,
E[n], yields the exact result E[n] = (4 − 3δ )/δ. We use this expression to derive a conservative upper
bound for resource estimation, as shown in Eq. (7).

                                                4 − 3δ  4    4
                                       E[n] =          = −3≤                                            (7)
                                                   δ    δ    δ
     The probability of absorption in state j when starting from transient state i is given by the
(i, j )-entry of the matrix B = N R. For large k, P k approximates these absorption probabilities,
with limk→∞ P k revealing the long-term absorption behavior.
     We base our convergence analysis of LLM-verifier refinement loops on this theoretical framework.
In it, the Verified state is the final absorbing state, while the refinement states are temporary
(transient) states. This framework extends traditional verification by adding probabilistic elements
to capture the random behavior of LLM-based refinement.

3.2 ESBMC Formal Verification Principles
Formal Verification uses math to prove that software works correctly according to given rules,
checking all possible ways the software can run. Tools like ESBMC follow a straightforward process:
they first transform the code into simpler forms, then apply BMC using techniques such as loop
unrolling and Static Single Assignment (SSA), and finally turn the properties into verification
conditions. Satisfiability Modulo Theories (SMT) solvers check these conditions to give definite
answers or find errors.
   These principles underpin our work on reliable LLM-verifier integration. Figure 2 illustrates the
end-to-end verification pipeline of the ESBMC framework, showing the complete workflow from
source code input to final verification results.

Fig. 2 The ESBMC verification framework architecture, integrating BMC for finite-depth program analysis with
SMT solving for efficient logical reasoning to enable rigorous software verification




3.2.1 Program Representation Level
The verification tool begins by transforming the source code into a form it can formally analyze.
For C/C++ programs, this transformation involves several critical preprocessing steps. Common
approaches rely on intermediate representations that simplify complex language features while
preserving semantic behavior [47].
    The transformation pipeline starts with C/C++ source code that includes complex language
features such as preprocessor directives, pointers, dynamic memory allocation, and implementation-
defined behavior. The preprocessing phase includes macro expansions and conditional compilation,
producing a self-contained translation unit [48]. Next, the process converts the code into the Gen-
eralized Operational Three-Address Output (GOTO) intermediate representation, which simplifies
complex control flow structures into basic blocks connected by explicit jumps [49, 50].
    The GOTO representation provides the base for the following BMC steps. It removes many
complex language details while preserving the essential meaning of the original program. This
transformation separates language processing from Formal Verification, letting verification focus on
the main computational logic.


                                                     8
3.2.2 Logical Notations for BMC
Formal Verification employs different logics to specify system properties. Propositional logic provides
the basic connectives, while temporal logic introduces operators to reason about how truth values
evolve. In these expressions, lowercase letters like p and q denote atomic propositions representing
basic state conditions.
    Temporal logic divides into two main types: Linear Temporal Logic (LTL), which reasons about
linear sequences of states (single execution paths), and Computation Tree Logic (CTL), which
reasons about branching futures (all possible paths from a state). BMC primarily applies LTL to
formulate properties over finite execution paths.
    Table 3 summarizes the key operators, with a focus on those most relevant to BMC.

 Table 3 Common Formal Verification notation: propositional logic and temporal logic

   Symbol       Name                    Logic Type      Meaning / Use Case
   Propositional Logic
   ¬p or !p     Negation / NOT          Propositional   The statement p is false.
   p ∧ q        Conjunction / AND       Propositional   Both p and q are true.
   p ∨ q        Disjunction / OR        Propositional   At least one of p or q is true.
   p → q        Implication             Propositional   If p is true, then q must be true.
   p ↔ q        Equivalence / IFF       Propositional   p is true if and only if q is true.
   Linear Temporal Logic (LTL)
   Fp           Finally                 LTL             Eventually, p will become true.
   Gp           Globally                LTL             p is always true, now and forever.
   Xp           Next                    LTL             In the next state, p will be true.
   pUq          Until                   LTL             p remains true until q becomes true.




3.2.3 BMC Transformation
Model Checking is a formal, automated verification technique for determining whether a finite-
state system model satisfies a given temporal logic specification. The core principle involves three
fundamental components, which align with the initial stages of the BMC transformation process
depicted in the figure [51, 52]:
 1. System Model (M): The system under verification is formally modeled, typically as a Kripke
    structure or a transition system. This model M represents all possible states and transitions
    that the system can undergo during its execution. Formally, a Kripke structure, illustrated in
    Figure 3, is a tuple M = (s, s0 , R, L), where:
         • s = {s1 , s2 , s3 } is a finite set of states.
         • s0 ⊆ S = {s1 } is a set of initial states.
         • R ⊆ S × S = {(s1 , s2 ), (s2 , s1 )(s1 , s3 ), (s3 , s3 )} is a transition relation that must be total.
         • L : S → 2AP = {(s1 , {p, q}), (s2 , {p, r}), (s3 , {q})} is a labeling function that assigns to
           each state a set of atomic propositions from a set AP that are true in that state.

 2. Specification (φ): The desired properties of the system, such as safety
    ( nothing bad happens ) and liveness ( something good eventually happens ), are
    expressed as formulas in a temporal logic, such as LTL [53] or CTL [54]. For instance, the
    safety property the system never enters a deadlock state can be expressed in LTL as
    G(¬deadlock).
 3. Verification Algorithm: The algorithm checks whether the model M satisfies the specifi-
    cation φ, denoted M |= φ, by verifying that all possible execution paths in M satisfy the
    temporal logic formula φ. It then returns:
      • Yes, if the property holds for all reachable states.


                                                            9
Fig. 3 An example of a Kripke structure




       • No, with a counterexample, if the property is violated. This counterexample is a trace
         of states {s0 , s1 , . . . , sk } leading from an initial state s0 ∈ s0 to a state sk that violates φ.
         This debugging aid is one of the most significant advantages of model checking.
    The primary challenge in model checking is the state-space explosion problem, where the number
of states in M grows exponentially as the number of system components or variables increases. To
solve this problem, researchers developed advanced techniques such as Symbolic Model Checking
(SMC) [55] based on Binary Decision Diagrams (BDD) [56] and BMC [57]. The BMC method forms
the foundation of the ESBMC [58] platform. This method uses a specific transformation pipeline:
  1. Loop Unrolling and SSA Form: For BMC, loops are unrolled to depth k and the program is
     converted to SSA form, assigning unique versions to variables to simplify state representation
     for logical encoding.
  2. BMC and SMT Solving: To address state-space explosion [7, 59, 60], BMC verifies properties
     within finite bounds [4], generating verification conditions solved via SMT solvers.
  3. Property Encoding as Verification Conditions (VCs): The SSA model and specification
     φ are encoded into a VC whose satisfiability implies a property violation within bound k [61].
     An unsatisfiable result indicates correctness within the bound.
  4. From BMC to Verification: k -Induction: k-induction extends BMC to complete verifica-
     tion through base case checking (paths up to length k) and inductive step (if property holds
     for k states, it holds for the next) [62].
     (a) Base Case: A standard BMC check that verifies the property holds for all execution paths
         of length up to k.
     (b) Inductive Step: An inductive proof that demonstrates if the property holds for any k
         consecutive states, it must also hold for the next state.
    Studies have shown that this combined approach effectively balances bug-finding efficiency with
verification completeness in tools like ESBMC [5].

3.2.4 Satisfiability Modulo Theories (SMT)
The application of BMC to software verification requires reasoning about complex data types
beyond propositional logic. SMT solving extends Boolean Satisfiability Problem (SAT) by combin-
ing boolean satisfiability with decision procedures for background theories [63]. SMT solvers serve
as the computational engine that enables precise reasoning about program semantics – including
pointer arithmetic, memory operations, and concurrent execution – by efficiently solving complex
verification conditions generated from real-world software systems [64].
    The architecture of modern SMT solvers comprises several key components working in concert:
  1. SAT Solving Core: At its foundation, an SMT solver contains a modern SAT solver that
     handles the bBoolean structure of formulas. This component finds satisfying assignments to the
     propositional skeleton of the input formula by replacing theory atoms with boolean variables.
  2. Theory Reasoning: SMT solvers integrate decision procedures for multiple background theo-
     ries essential for software verification – including bit-vector theory for fixed-width integers and


                                                     10
     bit-level operations, array theory for memory operations and data structures, linear arithmetic
     for integer and real constraints, and uninterpreted functions for abstract function symbols
     – which work collaboratively to determine satisfiability of formulas involving complex data
     types [65–67].
 3. Integration Architecture: The SAT solver and theory solvers interact through a lazy inte-
    gration scheme where the SAT solver proposes boolean assignments and theory solvers check
    their consistency, with theory conflicts driving the search process.
 4. Counterexample Generation: When the SMT solver finds a satisfiable verification condi-
    tion, it produces a concrete counterexample – an execution trace showing the sequence of states
    leading to the property violation, which is invaluable for debugging.
   The integration of BMC, k-induction, and SMT solving forms a comprehensive verification
framework where SMT solving provides the mathematical foundation for precise program reasoning.

3.2.5 ESBMC Output and Reporting
The final stage of the ESBMC workflow produces clear, actionable output for users. This output
directly corresponds to the results obtained from the SMT solving phase and consists of two primary
components:
 1. Verification Result + Counterexamples: ESBMC provides definitive verification results
    and, when property violations are detected, generates detailed counterexamples comprising
    comprehensive execution traces that include the exact sequence of program statements, vari-
    able values at each step, thread interleavings for concurrent programs, and memory state
    information for pointer-related errors, which are invaluable for debugging and root cause
    analysis.
 2. Final Report: ESBMC compiles all verification results into a comprehensive final report
    providing a summary of all checked properties and their status ( success/failed ), total
    verification time and resource usage, statistical information, references to counterexamples for
    failed properties, and verification bounds and parameters, serving as complete documentation
    for quality assurance, certification, and regression testing.
    In summary, ESBMC implements the theoretical model-checking pipeline, demonstrating how
engineers effectively combine BMC, k-induction, and SMT solving to build a powerful tool for
automated software verification. The framework’s comprehensive output, including detailed coun-
terexamples and final reports, provides users with actionable insights into program correctness and
potential defects.

3.3 LLMs for Verification
LLMs based on the Transformer architecture [12] are trained on massive code and text corpora,
enabling pattern recognition capabilities applicable to Formal Verification in ESBMC. It is crucial
to emphasize that LLMs operate primarily through statistical pattern matching rather than logical
reasoning. That program verification is fundamentally undecidable – no algorithm can solve all
verification problems.
    Despite their limitations, LLMs show two important abilities. First, they can recognize patterns
that emerge, such as predicting code behavior and translating between natural language and formal
representations [13]. Second, they can learn in context, adapting to verification tasks using carefully
designed prompts without changing their parameters [68].
    In code analysis, LLMs use statistical patterns to generate candidate specifications, such as
pre-conditions and loop invariants [69, 70]. They also detect possible code problems by recognizing
patterns [71]. Their generative abilities produce verification artifacts, such as formal properties for
ESBMC [72] and boundary test cases [73]. This approach builds a complete environment in which
LLMs act as a statistical helper before specification generation and as an assistants after, explaining
counterexamples [44].




                                                  11
    For deployment in verification, LLMs require optimization via model compression and
parameter-efficient fine-tuning. Compression includes quantization [74, 75], pruning [76], and knowl-
edge distillation [77]. Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA enable domain
adaptation by injecting small trainable adapters while freezing most parameters [78], allowing
efficient specialization for verification tasks.
    These pattern-matching capabilities, when integrated within our principled convergence frame-
work, enable the development of predictable and reliable LLM-verifier systems. This integration
acknowledges both the statistical nature of LLMs and the undecidability of verification, while provid-
ing theoretical guarantees for the iterative refinement process, making them suitable for deployment
in safety-critical verification environments where both performance and predictable behavior are
required.
    Table 4 summarizes significant advancements in accelerating Formal Verification through com-
pressed language models, highlighting the key techniques and their impacts on verification efficiency
and capability.


Table 4 Major advancements in applying LLMs to Formal Verification

 Advancement         and     Description & Key Features                       Impact / Results
 Framework
 Model        Compres-       Quantization, pruning, knowledge distillation    Enable LLM deployment in resource-
 sion Techniques for         for efficient pattern matching in LLMs           limited settings; up to 70%+ compres-
 LLMs [31–37]                                                                 sion with minimal accuracy loss
 Prompt Compression          Coarse-to-fine prompt compression maintain-      Up to 20× prompt compression with lit-
 (LLMLingua) [30]            ing semantic integrity                           tle performance loss, accelerating infer-
                                                                              ence
 Symbolic Compression        Formal symbolic compression framework for        Achieves 78.3% token compression and
 for Interpretability [40]   code generation tasks                            improves traceability by 62%
 Automated Proof Gen-        LLMs generate and repair proofs for Formal       65.7% of theorems proved automatically
 eration and Repair          Verification systems                             with Baldur+Thor
 (Baldur) [21]
 LLM-Driven   Invari-        LLMs generate candidate loop invariants using    Improves verification coverage for pro-
 ant Generation for          pattern recognition                              grams with unbounded loops using
 BMC [10]                                                                     ESBMC
 Hybrid     Verification     Combines LLMs’ pattern recognition with for-     Hybrid systems address scalability
 (LLMs    +      Formal      mal rigor for bug detection                      while maintaining formal guarantees
 Methods) [14, 38, 39]
 ESBMC-AI: LLM +             Integrates LLMs with ESBMC for vulnerabil-       High-accuracy repair of buffer over-
 Bounded Model Check-        ity detection and repair                         flows; suitable for continuous inte-
 ing [11, 25]                                                                 gration and continuous deployment
                                                                              (CI/CD) integration
 Efficient Self-Attention    Pruning and matrix folding in transformer lay-   70% overall model compression with
 with     Smart    Prun-     ers                                              stable performance
 ing [35]
 Safety and Trustwor-        V&V frameworks for LLMs, including runtime       Identifies gaps and proposes methods
 thiness Verification [15]   monitoring                                       for LLM safety assurance
 Fine-Tuning and Infer-      Parameter-efficient fine-tuning and inference    Reduces resource overhead for adapting
 ence Optimization [32,      optimization                                     LLMs to verification tasks
 34]




3.4 Formal Verifiers and LLM Integration
This subsection examines modern verifier characteristics enabling LLM integration and emerging
collaboration patterns. Examples include industrial-strength model checkers like ESBMC for C/C++
programs [5, 19, 58] and theorem provers in environments like FVEL [16]


                                                         12
    Formal verifiers are crucial in the LLM-assisted verification ecosystem, acting as the ground truth
for validating LLM-generated artifacts [14, 15]. These automated tools use mathematical reasoning
to prove or disprove software correctness with respect to formal specifications [7, 8], employing
techniques such as model checking [4, 43], theorem proving, and abstract interpretation.
    Unlike traditional testing, formal verifiers provide comprehensive coverage and mathematical
certainty rather than probabilistic confidence [57]. In LLM integration, they serve as reliable oracles
to validate generated code [23, 25], specifications [9], invariants [10], and repairs [11, 26], creating
a powerful approach between statistical AI and formal reasoning [27, 39].
    Figure 4 illustrates the fundamental workflow of a formal verifier, depicting how it consumes a
program and its specifications to deliver a definitive, mathematically sound result – either a proof
of correctness or a precise counterexample that guides debugging.

Fig. 4 The workflow of a formal verifier. This diagram illustrates the operational pipeline of a Formal Verification
tool. The process begins with the software program and its formal specification being translated into a formal model.
The verifier engine then performs a mathematical analysis of this model




    Modern Formal Verification tools like ESBMC exhibit key characteristics enabling effective LLM
integration [27, 39], including deterministic output providing definitive answers with counterexam-
ples [57] for reliable LLM refinement [21, 25]. These tools support incremental verification through
bounded approaches [4, 6] and provide rich counterexamples for LLM learning [5, 79], while scalable
SMT integration enables practical verification of complex properties [58, 63, 80].
    LLM-verifier integration uses different design patterns, such as sequential pipelines [9, 10], iter-
ative refinement [21, 23], hybrid verification [38, 39], and verifier-as-oracle methods [22, 81]. These
patterns help with important verification tasks - such as specification generation, invariant synthe-
sis, program repair, and proof assistance - by clearly combining the strengths of statistical learning
and Formal Methods.
    ESBMC’s architecture is well-suited for these integration patterns [5, 58], featuring mod-
ular design for LLM assistance [19, 82], comprehensive counterexamples for learning [6, 79],
and extensible verification strategies [62, 83] that enable practical application to real-world
programs [19, 64].
    Despite these architectural advances, LLM-verifier integration faces challenges including seman-
tic gaps between statistical and formal reasoning [13], effective feedback utilization [21], scale
mismatches [59], and uncertainty quantification in deterministic frameworks [46] [14, 15]. To solve
these problems, researchers use some good methods. These include structured prompting [24, 44],
checking step-by-step (incremental verification) [57, 62], and improved feedback loops [5, 21], and
specialized fine-tuning [75, 78].
    This integration represents a fundamental shift toward collaborative systems leveraging sta-
tistical AI and Formal Methods [7, 8], providing mathematical guarantees for safety-critical
deployment [1, 3].


                                                         13
4 Proposed Work - LLM-Verifier Convergence Theorem
The main goal of combining LLMs with Formal Verification tools like ESBMC is simple: Can we
prove with math that repeated improvements will finally lead to a correct answer? To answer this,
we build upon the Markov Chain theory (detailed in Section 3.1.3) to develop a new Theorem
tailored for sequential LLM-verifier systems.

4.1 Theoretical Foundation and Markov Chain Modeling
Our convergence theory builds upon the rigorous framework of absorbing Markov Chains established
in Section 3.1.3. The classical theory guarantees that a Markov Chain with at least one absorbing
state – and where every state can eventually reach an absorbing state – will be absorbed almost
surely [41, 42].
    This approach is well-supported theoretically and practically. Since transformer-based LLMs
generate text token-by-token within limited context windows, they inherently display the properties
of a Markov process. At the same time, empirical studies of systems like ESBMC-AI [11] and
Baldur [21] confirm that transition probabilities mainly depend on the current verification state.
    This model uses a five-state Markov Chain with Verified as the absorbing state (s5 ). Crucially,
we replace generic refinement steps with four distinct transient states representing the essential
milestones of a formal verification pipeline:
 1. (s1 ) CodeGen : The LLM attempts to generate the initial code or specification.
 2. (s2 ) Compilation : The artifact is validated for syntax and compilation errors.
 3. (s3 ) InvariantSynth : The system attempts to synthesize necessary loop invariants.
 4. (s4 ) SMTSolving : The final formal check where the solver attempts to prove correctness.
     The logic here mimics a sequential engineering workflow. When the system is in a specific stage
si , it attempts to advance to the next milestone si+1 . The transition succeeds with probability δ.
If it fails (with probability 1 − δ), the system remains in the current loop (si ) to retry the specific
task (e.g., regenerate code or refine invariants). The process reaches the absorbing Verified state
only after successfully clearing the final stage s4 .
     The Error-Reduction Probability (δ): Central to our model is the error-reduction proba-
bility δ, which quantifies the LLM’s capability to successfully complete a single pipeline stage in
one attempt. Table 5 shows typical δ values (0.360 - 0.880) for LLM verification tasks, validating
its role in governing system convergence and providing the empirical foundation for our theory.

Table 5 Summary of LLM performance on code-related tasks

 Task                      Model/System           δ        Details
 Automated Code Repair     GPT-4              0.543 [84]   Single-attempt vulnerability repair on Evaluation
                                                           and Assessment in Software Engineering (EASE)
                                                           benchmark (SecurityEval dataset)
 Invariant Generation      LLMs (Inductive    0.780 [85]   First-attempt success rate in generating verified
                           Loop Synthesis)                 invariants
 Invariant Generation      CodeLlama-34b-     0.360 [86]   First-attempt loop invariant synthesis (15 candi-
                           Instruct                        dates, no Houdini pruning)
 Proof Synthesis           Baldur             0.479 [21]   Single-attempt   whole-proof    generation    on
                                                           Isabelle/HOL
 Proof Synthesis           Baldur + Thor      0.657 [21]   Single-attempt on Isabelle/HOL when combined
                                                           with Thor
 Specification Synthesis   AssertLLM          0.880 [87]   Syntax-valid and Formal Property Verification
                                                           (FPV)-verified assertion generation
 Specification Synthesis   AutoSpec           0.790 [88]   Generates usable specifications via LLM + static
                                                           analysis + validation




                                                   14
4.2 The Main Result: LLM-Verifier Convergence Theorem
Combining LLMs with verification tools, such as ESBMC, certainly helps automate invariant gen-
eration. However, a significant issue remains: most approaches lack theoretical backing. Without
this foundation, the system becomes unstable. It may get stuck in infinite loops or oscillate indef-
initely [14, 15]. Our work fills this gap by introducing the LLM-Verifier Convergence Theorem.
This Theorem offers the first formal proof of termination and convergence, which is essential for
deployment in safety-critical systems [1, 3]. Next, we present Theorem 1 and its proof.

Theorem 1 (LLM-Verifier Convergence Theorem) We model the LLM-verifier process using a discrete-
time Markov Chain, denoted as X = {Xn }n≥0 . The state space S consists of a sequential engineering
pipeline (S = T ∪ A). First, T = {s1 , s2 , s3 , s4 } represents the set of transient pipeline stages ( CodeGen ,
 Compilation , InvariantSynth , SMTSolving ). Second, A = {s5 } acts as the single absorbing state
( Verified ). Assuming a fixed success probability δ ∈ (0, 1] for passing any single stage, we construct the
transition matrix P = (Pi,j ). The individual entries Pi,j = P(Xn+1 = sj | Xn = si ) are arranged as follows:
  (i) Transient Pipeline States: For the transient states i ∈ {1, 2, 3, 4}, the transition probabilities are:
                                 
                                 δ
                                         if j = i + 1 (success: advance to next stage),
                        Pi,j = 1 − δ if j = i (failure: retry current stage),
                                 
                                   0      otherwise.
                                 

(ii) Absorbing State: State s5 is absorbing, meaning the verification is complete. Hence, P5,5 = 1.
    Let τ = inf{n ≥ 0 : Xn ∈ A} be the iteration count until verification. The following bounds hold:
  1. Almost Sure Convergence:
                                             P(τ < ∞ | X0 ∈ T ) = 1
  2. Expected Iteration Bound: The mean time to convergence is given by:
                                                                  4
                                                E[τ | X0 = s1 ] =
                                                                  δ
  3. Tail Bound: Consider constants α > 0 and λQ ∈ (0, 1), where λQ is the spectral radius of the transient
     submatrix Q. Then, for all k ≥ 0:
                                           P(τ > k | X0 = s1 ) ≤ αλkQ .
     Substituting λQ = 1 − δ results in the following exponential bound:
                                          P(τ > k | X0 = s1 ) ≤ α(1 − δ)k .


Proof We analyze the absorbing Markov Chain structure to establish the three guarantees.
Part 1: Almost Sure Convergence: Does the system converge? To answer this, we check two requirements
from Markov Chain theory. First, do we have an absorbing state? Yes, state s5 . Second, can every state
reach it? Yes. From any point si ∈ T , the probability of reaching the end is δ 5−i > 0. Meeting both criteria
guarantees almost sure convergence. Thus,
                                           P(τ < ∞ | X0 ∈ T ) = 1
Part 2: Expected Iteration Bound: We analyze the total iteration count τ by considering the sequential
time spent in each pipeline stage. Let Mj represent the number of steps the process remains in state sj
before advancing. Because the probability of exiting sj to sj+1 on any given step is δ, the sojourn time Mj
follows a geometric distribution, Mj ∼ Geom(δ), with an expected value of E[Mj ] = 1/δ. Since the process
is sequential, the total number of iterations is the sum of the time spent in all four stages, τ = 4j=1 Mj .
                                                                                                  P
The linearity of expectation immediately gives us:
                                                 4
                                               X            1    1   1   1    4
                             E[τ | X0 = s1 ] =     E[Mj ] = + + + =
                                                            δ    δ   δ   δ    δ
                                                j=1

Part 3: Tail Bound: The transient submatrix Q is upper triangular (not diagonal), as transitions only
occur from i to i or i + 1. Specifically, every diagonal entry is Pi,i = 1 − δ, and every super-diagonal entry
is Pi,i+1 = δ. For an upper triangular matrix, the eigenvalues are simply the diagonal entries. Thus, the
spectral radius is λQ = maxi |Pi,i | = 1 − δ. Using standard Markov Chain theory, we find:
                                    P(τ > k | X0 = s1 ) ≤ α∥Qk ∥ ≤ α(1 − δ)k
                     −1
Where α = ∥(I − Q)        ∥. This equation establishes exponential decay.                                      □


                                                       15
4.3 A Practical Framework for Convergence
The system’s behavior is governed by the error-reduction probability δ, a metric that quantifies
the LLM’s ability to complete a specific verification sub-task. Unlike simpler models that assume
a single “generate-and-verify” step, our framework acknowledges the engineering reality of a multi-
stage pipeline. From any transient pipeline stage si (e.g., Compilation or InvariantSynth ), the
process has a δ chance of successfully advancing to the next milestone si+1 . Conversely, with a
probability of 1 − δ, the specific stage fails, necessitating a retry (si → si ) within the refinement
loop before the system can proceed.
    Our theory represents an important advancement in bridging LLMs and Formal Methods. We
no longer have to depend on uncertain, black-box outcomes. Instead, we offer a straightforward and
dependable framework backed by mathematical evidence:
  • Resource Allocation: Provides precise guidelines, specifically the bound E[n] = 4/δ, to assist
    with setting timeout limits and planning computational budgets for the entire pipeline.
  • Capability Assessment: Introduces a clear metric (δ) to measure LLM performance on spe-
    cific verification tasks, allowing for modular benchmarking of different stages (e.g., measuring
    δ for invariant generation separately from code repair).
  • Deployment Guidelines: Establishes practical thresholds for use (δ > 0.3 for standard
    systems and δ > 0.6 for high-performance applications).
    Mathematically, we confirm that for any δ > 0, the system will reach the verified state almost
surely. We can then use the derived formula E[n] = 4/δ to plan system limits, converting a theoretical
measure into a usable engineering metric. Table 6 shows how to use this logic to distribute resources
effectively in various situations.

             Table 6 Expected total pipeline iterations for different LLM verification capabilities

              LLM Capability Level         Success Rate δ      Expected Total Iterations E[n]
              Moderate Capability                 0.3                         13.3
              Balanced Performance                0.5                         8.0
              High Performance                    0.8                          5.0




   Furthermore, the exponential tail bound P(n > k ) ≤ α(1 − δ )k ensures that the probability of
excessively long refinement loops decays exponentially. This enables engineers to configure reliable
timeouts for safety-critical systems, ensuring that the verification pipeline fails gracefully rather
than hanging indefinitely.

5 Methodology
Our methodology establishes a comprehensive framework for validating the convergence theory
through systematic simulation and analysis. We designed this approach to test the theoretical
bounds rigorously; it simultaneously characterizes the behavior of sequential LLM-verifier systems
across their full operational range.

5.1 Simulation Framework Design
We developed a specialized simulation framework that implements the sequential Markov Chain
model described in Section 4. The simulator implements probabilistic transitions through the
four distinct pipeline stages: CodeGen (s1 ), Compilation (s2 ), InvariantSynth (s3 ), and
 SMTSolving (s4 ), leading ultimately to Verified (s5 ). In this model, δ governs the success
probability of advancing from stage si to si+1 .
   We examine the success probability parameter δ across its entire range. We categorize the
resulting operational data into three key regions: marginal (0.1 ≤ δ < 0.3), practical (0.3 ≤ δ ≤ 0.6),
and high-performance (0.6 < δ ≤ 0.9). After generating the large-scale dataset, we proceed to the


                                                        16
data collection phase. In this stage, we record both the total convergence time (T ) and the sequence
traces. The final stage involves the experimental validation framework, which uses a three-pronged
analytical approach – theoretical, sensitivity, and statistical – to rigorously test the derived bound
E[n] ≤ 4/δ and to provide empirically validated engineering insights.
   We summarize the complete experimental workflow in Figure 5. The process begins with the
simulation core, which translates the sequential pipeline model (Section 4) into a highly efficient
VMC simulation (Section 5.2.2).

Fig. 5 Overview of the LLM-Verifier Convergence validation methodology. The process links the theoretical sequen-
tial Markov Chain model to the experimental framework. The simulation core uses a VMC approach with the
Geometric distribution (Geom(δ)) to efficiently generate N = 10, 000 trials across the three defined operational
regions. After data collection (generating convergence time T and computational metrics), the results are channeled
into the experimental validation framework, which employs three complementary analytical lenses to confirm theo-
retical alignment, assess framework robustness, and ensure statistical reliability (see Table 7)




    We use a structured method to carefully check the accuracy of our theory about how well
different verification methods for LLMs work. We test this across all available verification options
to make sure our findings are reliable.
  • Sample Size Justification: The selection of 10,000 trials for each δ value is a robust method-
    ological decision, ensuring high statistical power [89, 90] and narrow 99% binomial confidence
    intervals (width ≤ ±0.01) [91, 92]. This large sample size is also critical for accurately esti-
    mating tail probabilities [93, 94] and for precisely computing higher-order empirical moments,
    such as variance and skewness [95].



                                                        17
  • Operational Regions Definition: The parameter space δ ∈ [0.1, 0.9] is divided into three
    operational regions based on probabilistic analysis and empirical modeling.
      1. The marginal region (0.1 ≤ δ < 0.3) addresses small success probabilities where conver-
         gence is theoretically ensured by exponential tail bounds, P(n > k ) ≤ e−cδk [93, 94], but
         tests practical computational limits.
      2. The practical region where δ falls between 0.3 and 0.6 matches typical success rates seen
         in Bernoulli-type outcomes [96]. This range also demonstrates the capabilities of LLMs
         in verification tasks [21, 97]. Therefore, it is the most important range when using these
         models in real-world situations.
      3. Finally, the high-performance region (0.6 < δ ≤ 0.9) represents near-expert behavior,
         corresponding to the high-probability convergence regime in Monte Carlo and reliability
         theory [90, 95].
  • Experimental Scale: Is structured around 90,000 Monte Carlo trials (10,000 trials across nine
    δ values from 0.1 to 0.9) to ensure statistically rigorous coverage for convergence analysis [90,
    95]. This method of systematic sampling helps us explore the area of success probabilities in a
    consistent way [96]. It allows us to understand how changes in δ relate to the rate of convergence
    and makes it easier to compare different situations [98]. The scale we use helps us test the
    rule that says the average value of n is less than or equal to 4 divided by δ. It also helps us
    see sudden changes, which we call phase transitions [96]. Overall, this creates a unique dataset
    that will be useful for future studies.

5.2 Simulation Execution
The validation follows a systematic protocol:
 1. VMC Simulation: Our framework works differently than traditional simulations that run
    step-by-step. Instead, it uses a method called VMC to speed up and improve efficiency. With
    VMC, we can calculate the time for all 10,000 trials simultaneously, rather than one at a time.
    This approach treats groups of data as a single unit, which speeds up calculations.
 2. Geometric Distribution: The Geometric distribution, Geom(δ ), models the residence time
    spent in each of the four pipeline stages (s1 through s4 ). Its expected value, 1/δ, directly
    establishes the theoretical basis for the primary bound we are validating.
                                                                        P4 Since the process is
    sequential, the total expected time is the sum of the means: E[n] = j=1 E[Mj ] = 4/δ.
 3. Parameter Sweep: For each δ value in {0.1, 0.2, . . . , 0.9}, execute 10,000 independent trials.
      • Number of iterations until absorption: This acts as the main measurement used to
        check the important theory that states E[n] ≤ 4/δ. It directly shows how quickly things
        come together or reach a stable point.
      • Sequence of state transitions: Enables analysis of the convergence path, identifying
        bottlenecks in specific pipeline stages (e.g., verifying if Invariant Synthesis s3 consumes
        disproportionate resources).
      • Convergence success / failure : Provides binary outcomes to empirically verify the
        Theorem’s guarantee of almost sure convergence across all trials.
      • Computational metrics (execution time, memory usage): Look at how doable the
        plan is and how many resources it will need. Make sure to connect the ideas from theory
        with the actual challenges we face when putting them into practice.
 4. Statistical Configuration: The framework features seeded random number generation
    for reproducible outcomes, independent trial execution to prevent cross-contamination, and
    comprehensive logging of all experimental parameters and outcomes.

5.2.1 Experimental Validation Framework
Our experimental study combines multiple methods, numerical measures, and key visuals to evaluate
convergence theory from multiple angles carefully. The design of our experiment includes three


                                                 18
methods to confirm our findings, each with its own measures and visuals to help interpret the
results, as shown in Table 7.


Table 7 Experimental validation framework: approaches, metrics, and visualizations

 Validation     Methodological Focus                Metrics                                Visualization
 Approach
 Theoretical    Empirical-theoretical     align-    Conservative        Factor    (Cf ):   Theoretical vs. Empiri-
 Validation     ment through statistical tests      Ratio of theoretical bound to          cal Bounds plot compar-
                of     distribution   structure,    empirical mean (Cf = (4/δ)/µ).         ing E[n] ≤ 4/δ against
                direct     bound    comparison      Efficiency (η): Successful state       empirical means (Figure 6)
                (E[n] ≤ 4/δ), and success rate      transitions per iteration (η = 4/µ).
                verification across all δ set-      Success Rate: Proportion of tri-
                tings.                              als satisfying n ≤ 1000.
 Sensitivity    Framework robustness assess-        Distribution Shape: Variance           Operational       Regions
 Analysis       ment via systematic δ varia-        (σ 2 ), Skewness (γ1 ), and Kurtosis   Map            demarcating
                tion, boundary-condition test-      (κ). Spread: interquartile range       marginal (δ < 0.3), prac-
                ing (δ = 0.1, 0.9), and distribu-   (IQR) (P75 − P25 ). Tail Latency       tical (0.3 ≤ δ ≤ 0.6),
                tion characteristic analysis.       (P99 ): The 99th percentile of iter-   and       high-performance
                                                    ations to absorption.                  (δ     >     0.6) regions
                                                                                           (Figure 7)
 Statistical    Reliability assurance through       Precision (W99 ): Width of the         Tail Probability Anal-
 Validation     confidence interval calculation,    99%√ Confidence Interval (2.576 ·      ysis with bounds e−cδk
                hypothesis testing against the-     σ/ N ). Throughput: Simula-            (Figure 8). Iteration Dis-
                oretical predictions, and statis-   tion speed (trials/sec). Resource      tribution Characteriza-
                tical power analysis.               Cost: Peak memory allocation           tion violin plots (Figure 9)
                                                    (MB).




   This combined approach turns theoretical ideas into real-world engineering knowledge. It helps
ensure the safe use of language model verifiers by providing different ways to analyze and understand
them.

5.2.2 Simulation Execution Engine
Unlike iterative state-machine simulations, our framework utilizes a vectorized Monte Carlo
approach to maximize computational throughput and statistical power.
  1. Vectorized State Generation: For each configuration δ ∈ {0.1, 0.2, . . . , 0.9}, the system
     instantiates a matrix M ∈ ZN ×4 where N = 10, 000 (the trial count). Each element Mi,j
     represents the residence time in stage j for trial i, sampled independently from a Geometric
     distribution, as defined in Eq. (8).

                                      Mi,j ∼ Geom(δ )          ∀i ∈ [1, N ], j ∈ [1, 4]                             (8)

  2. Iteration Aggregation:
                         P4 The total convergence time Ti for the i-th trial is computed via row-
     wise summation, Ti = j=1 Mi,j , eliminating loop overhead and ensuring memory contiguity.
  3. Resource Monitoring: To accurately capture computational metrics without observer effect,
     the simulation encapsulates the generation phase in a tracemalloc context, which records
     peak memory allocation (MB) and process time (central processing unit (CPU) seconds) for
     each δ batch.

5.2.3 Data Collection and Filtering
Our processing pipeline first extracts trial-level granularity from the raw data of each simulation
batch before performing aggregation:
  • Convergence Status: A trial is called a Success if it takes 1,000 units of time or less. This
    limit helps prevent the trial from running forever when the value is very low (less than 0.1).


                                                          19
    It is also much higher than what we usually expect, which is about 40 units of time when the
    value is 0.1.
  • Sequence Trace: Saving the complete list [Mi,1 , Mi,2 , Mi,3 , Mi,4 ] for each trial enables us to
    identify specific patterns where progress slows. For example, we can identify trials that clear the
    initial CodeGen and Compilation stages quickly but stall during the final SMT Solving stage.

5.2.4 Metric Computation Methodology
The quantitative metrics presented in Table 7 (p. 19) are derived from the raw simulation data T
using the following formulations:
 1. Conservative Factor (Cf ): Calculated as the ratio between the theoretical upper bound and
    the empirical mean µ, according to Eq. (9).

                                                       4/δ
                                                Cf =                                               (9)
                                                        µ

    Values of Cf ≥ 1.0 indicate that the theory successfully provides a safe upper bound.
 2. Statistical Significance (CI Width): We compute the width of the 99% confidence interval
    using the standard error of the mean, according to Eq. (10).
                                                          σ
                                           W99 = 2.576 × √                                        (10)
                                                           N

    Where σ is the empirical standard deviation and N = 10, 000.
 3. Iteration Efficiency (η): Defined as the ratio of successful state transitions to total iterations,
    according to Eq. (11).
                                               η = 4/µ                                             (11)

5.2.5 Visualization Logic
We created the visualizations using multiple data transformations to illustrate key concepts clearly:
  • Theoretical Alignment (Figure 6): To visualize distribution spread beyond simple error
    bars, we employed IQR shading and a smooth cubic spline through the empirical means. The
    shaded region (between the 25th percentile, P25 , and 75th percentile, P75 ) provides a robust
    visual indicator of where the central 50% of trials converge.
  • Operational Regions (Figure 7): Our analysis employed a dual-axis transformation to
    study the phase transition. This method creates a graph that shows variance (a measure of
    how much things differ) on a logarithmic scale on the left and iteration efficiency (how well
    something works) on a linear scale on the right. Using these dual axes helps us see the changes
    across three areas: the marginal area (where values are less than 0.3), the practical area, and
    the high-performance area.
  • Tail Probability (Figure 8): We compute the tail distribution by using the complementary
    cumulative distribution function. We plot this relationship as P (n > k ) = 1 − rank(k )/N on
    a log-linear scale. We display only the important points from our data, which show that the
    tails of the convergence time distribution follow an exponential pattern.
  • Iteration Distribution Characterization (Figure 9): We use violin plots to show the
    whole shape and spread of the time it takes to reach a goal for each value of δ. When we plot
    the number of tries on a logarithmic scale, it makes it easier to see the vast differences in times
    in the lower-performing area compared to the more grouped times in the high-performing area.




                                                 20
6 Experiments and Results
This part shows the testing we did to check our theory about how quickly things get better. We vali-
date our method’s correctness and robustness across diverse LLM applications. The implementation
of this work is available at https://github.com/pierredantas
    We followed the detailed steps explained in Section 5 to run our experiment. We used a fast
Python program that works well with NumPy, which helps with calculations. In our study, we tested
a range of values for δ, starting at 0.1 and increasing by 0.1 up to 0.9. For each δ, we ran 10, 000
separate tests, which means we did over 90, 000 tests in total to ensure our results were reliable.
    We designed our experiments to address four key research questions:
 1. RQ1: Convergence Reliability: Does the empirical convergence behavior match theoretical
    almost-sure convergence guarantees across the δ spectrum?
 2. RQ2: Bound Accuracy: How strict are the theoretical limits, expressed as E[n] ≤ 4/δ, when
    compared to actual results?
 3. RQ3: Practical Operating Regions: Can we identify distinct operational regions with clear
    design implications for real-world deployment?
 4. RQ4 Statistical Distribution Fit: Does the empirical distribution of convergence time
    conform to the assumed geometric (exponential tail) properties, and can the tail behavior be
    reliably characterized by a theoretical exponential bound?
 5. RQ5 Distribution Characterization and Predictability: How does the overall pattern of
    convergence time change in different operational areas? Can we identify the high-performance
    area by spotting a consistent and low-variance distribution?
 6. RQ6 (Computational Performance): What is the performance of the vectorized simulation
    framework, and how many trials can it run each second? Does the amount of memory it uses
    show that it is effective for large-scale Monte Carlo validation?

6.1 Experimental Results
6.1.1 RQ1: Convergence Reliability
Our experiments show that the results are very consistent across all tested values of δ. The findings
back up the theory that we can expect strong, almost inevitable convergence. In Table 8, you can
see the detailed metrics related to convergence for different δ values.

  Table 8 Empirical convergence results vs. theoretical bounds (10,000 trials per δ)

    δ     Theory     Mean (µ)     Std (σ)     Cons. Fact (Cf )     Tail Latcy (P99 )   Success Rate (%)
    0.1    40.000     39.876       18.836           1.0031               97.00              100.00
    0.2    20.000     19.914        8.855           1.0043               47.00              100.00
    0.3    13.333     13.316        5.513           1.0013               30.00              100.00
    0.4    10.000     10.058        3.933           0.9942               22.00              100.00
    0.5     8.000      8.012        2.823           0.9985               17.00              100.00
    0.6     6.667      6.678        2.094           0.9982               13.00              100.00
    0.7     5.714      5.723        1.585           0.9984               11.00              100.00
    0.8     5.000      4.981        1.112           1.0039                9.00              100.00
    0.9     4.444      4.443        0.705           1.0001                7.00              100.00




    The perfect success rate across all values tested for δ suggests that the process will usually
achieve the expected result. The data show that the average result (µ) closely matches the expected
value (E[n] = 4/δ). The conservative factor (Cf ) is approximately 1.0 across all configurations,
confirming that the empirical convergence rate closely matches the theoretical prediction. The tail
latency, shown as the 99th percentile of trials, indicates that even the worst cases have limits. The
maximum number of steps reached is 97 when the value is 0.1, and it decreases to 7 steps when the
value is 0.9.



                                                      21
6.1.2 RQ2: Bound Accuracy
The results we found show a strong connection between the expected limit on the number of steps,
represented as E[n] ≤ 4/δ, and what we actually observed in our experiments. The conservative
factor (Cf ), which helps us see this difference, is about 1.0 across all values of δ. This small range
indicates that our theoretical model is very accurate at predicting how quickly things will reach
their average, with only a little extra caution needed (Cf stays between 0.9942 and 1.0043).
    The analysis shows that there is a complex relationship between δ and the predictability of
outcomes. The empirical standard deviation (σ) shows a significant decrease, dropping from approx-
imately 18.84 at δ = 0.1 to 0.71 at δ = 0.9. This sharp decline in variability makes the results more
predictable as the parameter δ increases.
    The image labeled as Figure 6 clearly shows how closely the average curve follows the theoretical
curve. Additionally, the shaded area representing the interquartile range (IQR) highlights a large
amount of initial variation (about 18.84) in the marginal area where the value of delta is less than
0.3.

Fig. 6 Theoretical Bound Alignment and Empirical Convergence Rate. The figure compares the theoretical
expected bound (E[n] ≤ 4/δ) against the empirical mean (µ) across the δ spectrum. The extremely close tracking
between the empirical curve (blue) and the theoretical curve (red dashed) demonstrates the tight alignment (Cf ≈ 1.0)
of the model prediction. The blue shaded area represents the IQR (P25 − P75 ), which visually captures the dramatic
decrease in system variance (σ 2 ) when transitioning from the marginal region (δ < 0.3) to the high-performance
region (δ > 0.6)
                          50                                                                 Interquartile Range (IQR)
                                                                                             Theoretical Bound [n] 4/
                                                                                             Smoothed Empirical Mean Trend
                                                                                             Discrete Empirical Data (99% CI)

                          40



                          30
             Iterations




                          20



                          10




                               0.1   0.2   0.3   0.4             0.5             0.6   0.7             0.8            0.9
                                                       Success Probability ( )




6.1.3 RQ3: Practical Operating Regions
Based on the empirical convergence patterns, we identify three distinct operational regions with
clear design implications, as visualized in Figure 7, which explicitly show the relationships among
δ, convergence predictability (variance on a log scale), and iteration efficiency.
  • Marginal Region (δ < 0.3): This area shows the highest average number of attempts (µ up
    to 39.88) and an extensive range of results (σ up to 18.84). It highlights the system’s inherent
    risk and the need for long-term task limits. It is best for applications where time is not urgent.
  • Practical Region (0.3 ≤ δ ≤ 0.6): This region captures a critical phase transition where
    the variance (σ) drops significantly (from 5.51 down to 2.09), but the mean iteration count
    (µ) remains moderate (6.68 to 13.32). It is the optimal range for balancing moderate LLM
    capability with predictable performance, ideal for most standard real-world applications.
  • High-Performance Region (δ > 0.6): Defined by the lowest mean iteration counts (µ
    between 4.44 and 5.72) and highly suppressed variance (σ falling below 1.0 at δ = 0.8).



                                                             22
Fig. 7 Operational Regions Map: Performance and Stability Analysis. This dual-axis visualization maps
the framework’s behavior across the δ spectrum. The left axis (purple, log scale) tracks the empirical variance (σ 2 ),
demonstrating the system’s predictability. The right axis (green, linear scale) tracks iteration efficiency (η). The plot
clearly illustrates the sharp phase transition in stability: variance collapses rapidly upon entering the practical region
(δ ≥ 0.3), confirming the empirical boundaries for safe and efficient deployment
                                                             Efficiency                           Marginal Region                                            0.9
                                                                                                  Practical Region
                                                                                                  High-Performance
                                                                                                  Variance                                                   0.8
                                                                                                  Efficiency
                                                102
                                                                                                                                                             0.7

                                                                                                                                                             0.6




                                                                                                                                                               Efficiency
               Variance




                                                                                                                                                             0.5
                                                101
                                                                                                                                                             0.4

                                                                                                                                                             0.3


                                                100                                                                                                          0.2

                                                                                                                                                             0.1
                                                            0.1           0.2   0.3    0.4             0.5             0.6        0.7   0.8       0.9
                                                                                             Success Probability ( )



     Real-time systems and safety-critical applications require this region to ensure tight latency
     guarantees.

6.1.4 RQ4: Statistical Distribution Fit
The experimental analysis decisively affirms that the empirical distribution of convergence time con-
forms to the assumed geometric properties. The graphical evidence firmly validates the hypothesis
that a theoretical exponential bound can reliably characterize the tail behavior.
   The tail probability analysis (Figure 8) demonstrates that the probability of requiring k extra
steps decays exponentially across all tested δ values. The clear, approximately linear trends on
the log-linear scale confirm the fundamental assumption that the convergence time follows the
predicted exponential tail behavior, given by P(n > k ) ∝ e−cδk . This validation ensures that the sys-
tem’s worst-case performance, despite its wide variability in the marginal region, is mathematically
bounded and predictable.

Fig. 8 Tail Probability Analysis: Empirical Validation of Exponential Decay. The figure plots the Com-
plementary Cumulative Distribution Function (CCDF, P (n > k)) on a log-linear scale. The approximately linear
decay observed across all tested δ values confirms the fundamental assumption that the convergence time follows an
exponential tail behavior (P(n > k) ∝ e−cδk ). This validation ensures that the system’s worst-case convergence time
is reliably bounded and predictable, even in the marginal region
                  100                                                                     Configuration
                                                                                                                                              Empirical = 0.2
                                                                                                                                              Empirical = 0.4
                                                                                                                                              Empirical = 0.6
                                                                                                                                              Empirical = 0.8

                                                     10 1
              Tail Probability (n > k) (Log Scale)




                                                     10 2




                                                     10 3




                                                     10 4
                                                                          10      20         30                 40           50         60              70
                                                                                                     Iterations (k)




                                                                                                      23
6.1.5 RQ5: Distribution Characterization and Predictability
The experimental analysis of the complete convergence time distribution profile provides strong
evidence distinguishing the operational regions based on stability. As visualized in Figure 9, the
complete statistical distribution of convergence time evolves systematically across the δ spectrum,
confirming that a stable, low-variance distribution reliably identifies the high-performance regime.

Fig. 9 Iteration Distribution Characterization. The figure uses violin plots to display the complete probability
density function of convergence iterations for each δ value. The data is plotted on a logarithmic scale to highlight the
extreme variance difference between the marginal (wide, scattered density) and high-performance (tight, compressed
density) operational regions
                                                                                                              Operational Region
                                                                                                                 Marginal
                                                                                                                 Practical
                                    102                                                                          High-Performance
           Iterations (Log Scale)




                                    101




                                          0.1   0.2   0.3   0.4             0.5             0.6   0.7   0.8              0.9
                                                                  Success Probability ( )



    The visual data confirms that the boundaries are statistically meaningful:
   • Marginal Region (δ < 0.3): In this region, data spreads out a lot and is not easy to predict.
     There is a wide range of values, and the data shows high variability.
   • Practical Region (0.3 ≤ δ ≤ 0.6): In this range, the data exhibits significantly reduced
     variance. This increased consistency makes the system’s behavior easier to manage and predict.
   • High-Performance Region (δ > 0.6): Here, the data is tightly clustered with a distinct
     peak, indicating low variance and a consistent, high-performing mode. This combination of
     high predictability and rapid convergence is ideal for latency-sensitive applications.

6.1.6 RQ6: Computational Efficiency
The simulation framework demonstrates excellent scalability and computational efficiency, leverag-
ing NumPy’s vectorized operations:
   • Total Runtime: The complete validation, spanning 90,000 trials, required approximately 0.10
     seconds of total CPU time.
   • Throughput: The measured throughput was extremely high, exceeding 858, 000 trials per
     second (average), definitively confirming the efficiency of the vectorized implementation.
   • Vectorized Efficiency: The achieved iteration efficiency (η) increased monotonically from
     0.1003 (δ = 0.1) to 0.9001 (δ = 0.9). This proximity to the theoretical optimum (η ≤ 1.0)
     validates the effectiveness of the vectorized implementation.
   • Memory Efficiency: The peak memory footprint was minimal (< 1MB) as reported by
     tracemalloc , enabling extensive parameter exploration on resource-constrained hardware.
   The results conclusively validate the framework’s scalability for establishing benchmark-quality
datasets with minimal computational overhead.




                                                                        24
6.2 Threats to Validity
Before presenting the final summary, the following sections detail the threats to the experimen-
tal design’s validity. This critical analysis systematically identifies potential flaws in the model,
measurement, and generalization of the results (categorized into internal, external, and construct
validity), ensuring that readers interpret the conclusions with appropriate context regarding their
reliability and applicability to real-world LLM-verifier systems.

6.2.1 Internal Validity
Internal validity assesses whether the study accurately demonstrates a causal relationship between
the variables, ensuring that the observed results are attributable to the proposed theoretical
framework rather than artifacts of the experimental design.
 1. Modeling Assumptions: We use a simpler model (Markov Chain) to understand how LLMs
    behave. Our tests support this simpler approach, showing that it is a good fit.
 2. Parameter Stationarity: We assume the parameter δ remains constant throughout the
    refinement process to derive a closed-form bound. In reality, LLMs may exhibit non-stationary
    behavior (e.g., performance drift due to context window saturation). While this abstraction
    simplifies the model, it represents the “average effective capability” of the system. Future work
    (discussed in Section 7.5) will address dynamic calibration strategies to mitigate this drift in
    real-world deployments.
 3. State Space Limitation: Our model has five states, which captures the core engineering
    pipeline (s1 → s5 ) but may not capture granular sub-states within complex tasks (e.g., partial
    invariant synthesis).
 4. Convergence Definition Bias: Defining success by a 1,000-iteration cutoff introduces a slight
    bias. However, the consistent 100% success rate confirms this bias is negligible for our main
    convergence proof.

6.2.2 External Validity
External validity evaluates the generalizability of our findings beyond the controlled simulation
environment. This section assesses the extent to which the theoretical bounds and operational
regions derived from our model apply to real-world LLM deployments, diverse verification domains,
and varying engineering scales.
  • Simulation vs. Real Systems: Experiments use modeled behavior (sum of independent
    Geometric distributions); validation with real LLM and application programming interfaces
    (APIs) is future work.
  • Domain Generalization: Results based on synthetic Markov Chains; domain-specific δ
    calibration is needed for different verification tasks (e.g., SMT solving vs. proof synthesis).
  • Scale Considerations: While we tested 90, 000 Monte Carlo trials, real deployment may
    involve different scales and operational patterns.

6.2.3 Construct Validity
Construct validity examines whether the operational measures used in the study essentially represent
the theoretical constructs they are intended to measure. We analyze potential disconnects between
our mathematical metrics and the real-world engineering goals of LLM verification.
  • Metric Selection: Emphasis on iteration count (E[n]) rather than wall-clock time, though
    these are typically correlated. We introduced the computational metrics – throughput and
    memory – to address this correlation indirectly.
  • Success Definition: Binary success / failure provides a clear convergence signal but may
    not capture partial progress in complex refinements.




                                                 25
  • Parameter Range: The defined δ values of 0.1 to 0.9 cover the practical range of LLM
    verification capability, but extreme values (e.g., δ → 0 or δ → 1) require further theoretical
    analysis.

6.3 Summary of Key Findings
We conducted a thorough series of experiments with over 90,000 simulations, yielding important
discoveries for designing systems to verify language models. We have summarized these key findings
in Table 9. Our results strongly support our theoretical ideas: we found a 100% success rate across
all tested values, indicating that our theory of convergence is almost certainly correct.
    The theoretical limit shows that the average number of items, represented as E[n], should not
be more than 4/δ. This limit is very accurate, as the actual average µ stays very close to it.
Consequently, the adjustment factor Cf remains around 1.0. This proximity to 1.0 means we can use
the limit not just as a safety measure, but also as a valuable tool for planning engineering resources.
    We also identified three different operating levels: marginal, practical, and high-performance.
This framework helps system designers understand how to connect the capabilities of LLMs (denoted
δ) to expected performance results in a clear, measurable way.
    These results conclusively demonstrate that our convergence theory provides the missing math-
ematical foundation for predictable, reliable, and efficient integration of LLM-Formal Methods into
critical software systems.


Table 9 Key findings and practical implications from convergence experiments

 Category          Empirical Finding                   Practical Implication
 Convergence       100% success rate for δ ≥ 0.1,      System Reliability: LLM-verifier systems will virtually
 Reliability       confirming almost-sure conver-      always converge, validating deployment in production envi-
                   gence (µ ≈ 4/δ).                    ronments regardless of capability δ.
 Theoretical       Empirical Mean (µ) tracks the       Resource Planning: The theoretical bound is highly accu-
 Bound Accu-       Theoretical Bound (4/δ) with        rate, allowing engineers to use 4/δ as the reliable predicted
 racy              Cf ≈ 1.0 (minimal conser-           mean time, rather than a safety margin.
                   vatism).
 Performance       Standard deviation decreases        Predictability: High-δ systems exhibit exponentially con-
 Predictabil-      dramatically from σ ≈ 18.84         sistent performance, enabling reliable service-level agree-
 ity               (δ = 0.1) to σ ≈ 0.71 (δ = 0.9).    ments and low-variance real-time applications.
 Convergence       Mean iteration count (µ) ranges     Performance Optimization: The steepest performance
 Speed             from 39.88 (δ = 0.1) down to 4.44   improvements occur when moving from δ = 0.1 to δ =
                   (δ = 0.9).                          0.3. Focus improvement efforts on this marginal-to-practical
                                                       transition.
 Operating         Three distinct regions: marginal    System Design: Select LLMs based on target δ region: δ >
 Regions           (σ > 5.5), practical (0.3 ≤ δ ≤     0.3 for robust performance, δ > 0.8 for high predictability.
                   0.6), high-performance (σ < 1.0
                   at δ ≥ 0.8).
 Computational 0.10s total runtime for 90,000          Scalability: The vectorized framework efficiently handles
 Efficiency    trials; throughput exceeding            large-scale analysis, supporting rapid prototyping and con-
               858,000 trials/second.                  tinuous monitoring of LLM capability.




7 Discussion
This section interprets the empirical results presented in Section 6.1 against the theoretical model
and core objectives established in Section 6, providing actionable insights for the design of sequential
LLM-verifier systems.




                                                       26
7.1 Validation of Theoretical Bound and Alignment (RQ2)
The empirical validation decisively confirms the theoretical bound E[n] ≤ 4/δ as a predictable
ceiling for convergence time. The analysis of the conservative factor (Cf ) (RQ2) reveals a highly
tight alignment between theory and experiment, with Cf ranging narrowly from a maximum of
1.0043 to a minimum of 0.9942 (Table 8, p. 21).
    This closeness confirms that the total verification latency is indeed the sum of the latencies of
the four pipeline stages (s1 → s4 ). This finding provides a critical engineering guarantee: it elevates
the determination of resource allocation from empirical guesswork to a practice    P governed by the
robust additive logic of the sequential pipeline, where total cost is predictably     E[Mj ] = 4/δ.

7.2 Phase Transition and System Predictability (RQ3 & RQ5)
Looking at the variance (σ 2 ) helps us confirm the operational regions (RQ3) and shows how the
system stability evolves (RQ5). The rapid collapse of the standard deviation supports the existence
of a critical phase transition in system predictability.
  • The system transitions from the marginal region (δ = 0.2, σ ≈ 8.86) to the practical region
    (δ = 0.3, σ ≈ 5.51), resulting in a significant reduction in performance variability (Figure 7).
  • This validates the defined δ thresholds: systems entering the practical region mitigate the
    variance risk inherent to low-δ configurations. For engineers, this implies that optimization
    efforts should focus on pushing δ past the 0.3 threshold to secure reliable service-level adherence.
   This data demonstrates that improving LLM capability does not just reduce average time; it
fundamentally alters the stability of the pipeline. We especially identify the High-Performance region
(δ > 0.6) as the target for safety-critical systems requiring minimal variance.

7.3 Alignment with Theoretical Premises (RQ1 & RQ4)
The experimental results align perfectly with the study’s fundamental premises, mathematically
validating the structure of the pipeline.
  • Almost-Sure Convergence (RQ1): The 100% success rate provides strong evidence that
    the sequential LLM-verifier is statistically guaranteed to self-correct and terminate. This holds
    true provided that the probability of success for any single stage (δ) remains non-zero.
  • Statistical Distribution Fit (RQ4): The structure of the empirical data strongly confirms
    that the convergence time follows a Negative Binomial distribution with parameter r = 4. Since
    a Negative Binomial(r, p) distribution describes the sum of r independent Geometric variables,
    this empirical fit mathematically validates our modeling assumption that the process consists
    of exactly four independent, sequential refinement stages (s1 , s2 , s3 , s4 ).

7.4 Computational Feasibility and Framework Validity (RQ6)
The simulation framework’s performance validates its utility as a high-speed analytical tool for LLM
assessment (RQ6). A throughput exceeding 858,000 trials/second, achieved with minimal memory
overhead, demonstrates that the analytic approach is highly scalable. This performance validates
the framework’s ability to support continuous monitoring and dynamic testing of LLM capability
in production environments.

7.5 Handling Non-Stationary Environments (Dynamic Calibration)
A key threat to validity identified in Section 6.2 is parameter stationarity – the risk that δ may
drift over time due to LLM context saturation or fatigue. While our Theorem assumes a fixed δ, our
framework offers a practical mitigation strategy for real-world deployment: dynamic calibration.
    Because the system behavior is well-characterized by the operational regions (Table 1, p. 4),
engineers can implement a runtime monitor that calculates a sliding-window average of the success
rate (δ̂).



                                                  27
  • If δ̂ drops into the marginal region (δ̂ < 0.3), the system can automatically trigger a context
    reset or increase the sampling temperature to restore the error-reduction probability.
  • This approach effectively treats a non-stationary process as a sequence of piecewise-stationary
    segments, ensuring that the system dynamically adheres to the convergence guarantees
    provided by the Theorem.

8 Conclusion and Future Work
The experimental validation decisively confirms the theoretical premises and core objectives of
this work. The detailed simulation of the VMC and LLM-verifier system demonstrated a robust
alignment with the proposed sequential absorbing Markov Chain model. This proves that modeling
verification not as a generic loop, but as a structured pipeline of engineering stages (s1 → s4 ),
provides a solid mathematical basis for combining Formal Methods and AI.
    The results clearly showed that our initial hypothesis of almost-sure convergence was correct
(RQ1), with a 100% success rate across all 90,000 tests. Importantly, we confirmed that the cumula-
tive expected latency is governed by the sum of the individual stage latencies, validating the bound
E[n] ≤ 4/δ with high accuracy (RQ2). The average results closely matched our predictions, and the
conservative factor (Cf ) remained consistently within the range [0.9942, 1.0043]. This consistency
proves that the linear accumulation of time across the four pipeline stages is a valid predictor of
total system cost.
    The statistical analysis provided precise metrics to define three different operational regions
(RQ3). The variance in convergence time (σ 2 ) collapsed significantly, dropping from approximately
18.84 in the marginal region (δ = 0.1) to around 0.71 in the high-performance region (δ = 0.9).
This phase transition supports the architectural recommendation to treat these regions differently
in deployment.
    Looking at the complete statistical distribution (RQ5) and the tail probabilities (RQ4) confirmed
that the convergence process follows the predicted geometric decay, indicating that worst-case out-
liers are mathematically bounded. Finally, the analytical framework proved highly scalable (RQ6),
capable of running more than 858,000 trials per second.
    In summary, the experimental results provide direct, strong, and affirmative confirmation that
the convergence theory provides the mathematical foundation for the integration and reliable
deployment of sequential LLM verification pipelines.

8.1 Future Work
The theories and validation methods created in this research point to distinct opportunities for
future studies, particularly in addressing the complexities of real-world deployment.
  • Integration with Real LLM APIs: A critical next step is extending the simulation environ-
    ment to interface directly with LLM APIs. We aim to measure empirical δ values for specific
    stages (e.g., measuring δcode vs. δinvariant ) to validate if the success rate remains uniform across
    different phases of the pipeline.
  • Handling Non-Stationary Environments: As noted in our validity analysis, real-world
    LLMs may exhibit parameter drift (non-stationarity) due to context window saturation or
    fatigue. Future work will focus on developing dynamic calibration strategies. These adaptive
    systems will estimate δ in real-time using a sliding window; if performance drops below the
    practical region threshold, the system could dynamically trigger context resets or strategy
    shifts.
  • Advanced Probabilistic Modeling: We aim to refine the mathematical model by exploring
    continuous-time Markov Chains to capture nuanced timing effects beyond discrete steps. This
    includes modeling correlations between stages (e.g., where a weak success in s1 increases the
    failure probability in s2 ).




                                                  28
8.2 Concluding Remarks
This work has created a strong basis for understanding how LLMs can work together with Formal
Methods. By achieving our research goals, we have provided solid mathematical support for a
process that used to rely on heuristics. This change turns a trial-and-error approach into a verifiable
engineering discipline. The key findings directly reaffirm the objectives:
  • The empirical 100% success rate validated the almost-sure convergence proof for the sequential
    pipeline.
  • The theoretical bound E[n] ≤ 4/δ was confirmed to exhibit tight alignment (Cf ≈ 1.0),
    demonstrating that total latency is predictable based on the four-stage structure (RQ2).
  • The empirical data successfully defined three distinct operational regions, identifying a critical
    stability phase transition at δ ≈ 0.3 (RQ3/RQ5).
  • The framework demonstrated computational feasibility, achieving over 858,000 trials/second,
    validating its utility for high-speed analysis (RQ6).
    This framework establishes a new paradigm for human-AI collaboration in critical reasoning
tasks, seamlessly integrating the complementary strengths of probabilistic learning and sequential
logic to solve challenging problems in computer science.

Acknowledgement
The authors thank the Center for Electronic and Information Technology (CETELI) and the Depart-
ment of Electrical Engineering at the Federal University of Amazonas (UFAM), Brazil, for providing
the infrastructure, technical support, and access to state-of-the-art resources that were fundamental
to this research.
    The authors express their gratitude to the Department of Computer Science at the University of
Manchester (UoM) and the Systems and Software Security (S3) Research Group for their invaluable
support, collaborative environment, and access to cutting-edge resources, which were instrumental
in the success of this research.
    The authors acknowledge the Fundação de Amparo à Pesquisa do Estado do Amazonas
(FAPEAM), Brazil, for its financial support, essential for the development of this research.
    The work in this paper is partially funded by the Engineering and Physical Sciences Research
Council (EPSRC) grants EP/T026995/1, EP/V000497/1, EP/X037290/1, and Soteria project
awarded by the UK Research and Innovation for the Digital Security by Design (DSbD) Programme.




                                                  29
References
 [1] Cofer, D., Gacek, A., Backes, J., Whalen, M.W., Pike, L., Foltzer, A., Podhradsky, M.,
     Klein, G., Kuz, I., Andronick, J., Heiser, G., Stuart, D.: A Formal Approach to Construct-
     ing Secure Air Vehicle Software. Computer 51(11), 14–23 (2018) https://doi.org/10.1109/mc.
     2018.2876051

 [2] Hatcliff, J., King, A., Lee, I., Macdonald, A., Fernando, A., Robkin, M., Vasserman, E.,
     Weininger, S., Goldman, J.M.: Rationale and Architecture Principles for Medical Application
     Platforms. In: 2012 IEEE/ACM Third International Conference on Cyber-Physical Systems,
     pp. 3–12. IEEE, Beijing, China (2012). https://doi.org/10.1109/iccps.2012.9

 [3] Luckcuck, M., Farrell, M., Dennis, L.A., Dixon, C., Fisher, M.: Formal Specification and Ver-
     ification of Autonomous Robotic Systems: A Survey. ACM Computing Surveys 52(5), 1–41
     (2019) https://doi.org/10.1145/3342355

 [4] Biere, A., Cimatti, A., Clarke, E., Zhu, Y.: Symbolic Model Checking without BDDs, pp.
     193–207. Springer, Berlin, Heidelberg (1999). https://doi.org/10.1007/3-540-49059-0_14

 [5] Gadelha, M.R., Monteiro, F.R., Morse, J., Cordeiro, L.C., Fischer, B., Nicole, D.A.: ESBMC
     5.0: an Industrial-Strength C Model Checker. In: Proceedings of the 33rd ACM/IEEE
     International Conference on Automated Software Engineering. ASE’18, pp. 888–891. ACM,
     Manchester, UK (2018). https://doi.org/10.1145/3238147.3240481

 [6] Cordeiro, L., Fischer, B., Marques-Silva, J.: SMT-Based Bounded Model Checking for Embed-
     ded ANSI-C Software. IEEE Transactions on Software Engineering 38(4), 957–974 (2012)
     https://doi.org/10.1109/tse.2011.59

 [7] Clarke, E.M., Henzinger, T.A., Veith, H., Bloem, R.: Handbook of Model Checking. Springer,
     Cham, Switzerland (2018). https://doi.org/10.1007/978-3-319-10575-8

 [8] Woodcock, J., Larsen, P.G., Bicarregui, J., Fitzgerald, J.: Formal Methods: Practice and
     Experience. ACM Computing Surveys 41(4), 1–36 (2009) https://doi.org/10.1145/1592434.
     1592436

 [9] Liu, Y., Xue, Y., Wu, D., Sun, Y., Li, Y., Shi, M., Liu, Y.: PropertyGPT: LLM-driven
     Formal Verification of Smart Contracts through Retrieval-Augmented Property Generation.
     In: Proceedings 2025 Network and Distributed System Security Symposium (2025). https:
     //doi.org/10.14722/ndss.2025.241357 . Internet Society

[10] Pirzada, M.A.A., Reger, G., Bhayat, A., Cordeiro, L.C.: LLM-Generated Invariants for
     Bounded Model Checking Without Loop Unrolling. In: Proceedings of the 39th IEEE/ACM
     International Conference on Automated Software Engineering, pp. 1395–1407 (2024). https:
     //doi.org/10.1145/3691620.3695512 . ACM

[11] Tihanyi, N., Charalambous, Y., Jain, R., Ferrag, M.A., Cordeiro, L.C.: A New Era in Software
     Security: Towards Self-Healing Software via Large Language Models and Formal Verification.
     In: 2025 IEEE/ACM International Conference on Automation of Software Test (AST), pp.
     136–147 (2025). https://doi.org/10.1109/ast66626.2025.00020 . IEEE

[12] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L.,
     Polosukhin, I.: Attention Is All You Need. arxiv (2017). https://doi.org/10.48550/arxiv.1706.
     03762

[13] Wei, J., Tay, Y., Bommasani, R., Raffel, et al.: Emergent Abilities of Large Language Models.
     arxiv (2022). https://doi.org/10.48550/arxiv.2206.07682




                                               30
[14] Beckert, B., Klamroth, J., Pfeifer, W., Röper, P., Teuber, S.: Towards Combining the Cognitive
     Abilities of Large Language Models with the Rigor of Deductive Progam Verification, pp.
     242–257. Springer, Cham, Switzerland (2024). https://doi.org/10.1007/978-3-031-75387-9_15

[15] Huang, X., Ruan, W., Huang, W., Jin, G., Dong, et al.: A Survey of Safety and Trustworthiness
     of Large Language Models through the Lens of Verification and Validation. arxiv (2023). https:
     //doi.org/10.48550/arxiv.2305.11391

[16] Lin, X., Cao, Q., Huang, Y., Wang, H., Lu, J., Liu, Z., Song, L., Liang, X.: FVEL: Interactive
     Formal Verification Environment with Large Language Models via Theorem Proving. Neural
     Information Processing Systems (2024) https://doi.org/10.48550/arxiv.2406.14408

[17] Zekri, O., Odonnat, A., Benechehab, A., Bleistein, L., Boullé, N., Redko, I.: Large Language
     Models as Markov Chains (2024). https://doi.org/10.48550/arxiv.2410.02724

[18] Qi, J., Tang, H., Zhu, Z.: VerifierQ: Enhancing LLM Test Time Compute with Q-Learning-
     based Verifiers (2024). https://doi.org/10.48550/arxiv.2410.08048

[19] Monteiro, F.R., Gadelha, M.R., Cordeiro, L.C.: Model Checking C++ Programs. Software
     Testing, Verification and Reliability 32(1) (2021) https://doi.org/10.1002/stvr.1793

[20] Orenes-Vera, M., Martonosi, M., Wentzlaff, D.: Using LLMs to Facilitate Formal Verification
     of RTL. arxiv.org (2023) https://doi.org/10.48550/arxiv.2309.09437

[21] First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: Whole-Proof Generation and Repair with
     Large Language Models. In: Proceedings of the 31st ACM Joint European Software Engineering
     Conference and Symposium on the Foundations of Software Engineering, pp. 1229–1241 (2023).
     https://doi.org/10.1145/3611643.3616243 . ACM

[22] Loughridge, C., Sun, Q., Ahrenbach, S., Cassano, F., Sun, C., Sheng, Y., Mudide, A., Misu,
     M.R.H., Amin, N., Tegmark, M.: DafnyBench: A Benchmark for Formal Software Verification.
     arxiv (2024) https://doi.org/10.48550/arxiv.2406.08467

[23] Misu, M.R.H., Lopes, C.V., Ma, I., Noble, J.: Towards AI-Assisted Synthesis of Verified Dafny
     Methods. Proceedings of the ACM on Software Engineering 1, 812–835 (2024) https://doi.org/
     10.1145/3643763

[24] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., Zhou,
     D.: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (2022). https:
     //doi.org/10.48550/arxiv.2201.11903

[25] Charalambous, Y., Manino, E., Cordeiro, L.C.: Automated Repair of AI Code with Large
     Language Models and Formal Verification. arxiv (2024). https://doi.org/10.48550/arxiv.2405.
     08848

[26] Fakih, M., Dharmaji, R., Bouzidi, H., Araya, G.Q., Ogundare, O., Faruque, M.A.A.:
     LLM4CVE: Enabling Iterative Automated Vulnerability Repair with Large Language Models.
     arxiv (2025). https://doi.org/10.48550/arxiv.2501.03446

[27] Wang, W., Farrell, M., Cordeiro, L.C., Zhao, L.: Supporting Software Formal Verification with
     Large Language Models: An Experimental Study. arxiv.org (2025) https://doi.org/10.48550/
     arxiv.2507.04857

[28] Deng, L., Zhong, Q., Song, J., Lei, H., Li, W.: LLM-Based Unknown Function Automated
     Modeling in Sensor-Driven Systems for Multi-Language Software Security Verification. Sensors
     25(9), 2683 (2025) https://doi.org/10.3390/s25092683

[29] Yao, J., Zhou, Z., Chen, W., Cui, W.: Leveraging Large Language Models for Automated Proof


                                                31
    Synthesis in Rust. arxiv.org (2023) https://doi.org/10.48550/arxiv.2311.03739

[30] Jiang, H., Wu, Q., Lin, C.-Y., Yang, Y., Qiu, L.: LLMLingua: Compressing Prompts for Accel-
     erated Inference of Large Language Models. arxiv (2023). https://doi.org/10.48550/arxiv.2310.
     05736

[31] Zhu, X., Li, J., Liu, Y., Ma, C., Wang, W.: A Survey on Model Compression for Large Language
     Models. Transactions of the Association for Computational Linguistics 12, 1556–1577 (2024)
     https://doi.org/10.1162/tacl_a_00704

[32] Wang, W., Mao, Y., Dongdong, T., Hongchao, D., Guan, N., Xue, C.J.: When Compression
     Meets Model Compression: Memory-Efficient Double Compression for Large Language Models.
     In: Findings of the Association for Computational Linguistics: EMNLP 2024, pp. 16973–16983.
     Association for Computational Linguistics, Miami, Florida, USA (2024). https://doi.org/10.
     18653/v1/2024.findings-emnlp.988

[33] Dantas, P.V., Silva, W., Cordeiro, L.C., Carvalho, C.B.: A Comprehensive Review of Model
     Compression Techniques in Machine Learning. Applied Intelligence 54(22), 11804–11844 (2024)
     https://doi.org/10.1007/s10489-024-05747-w

[34] Kim, G.I., Hwang, S., Jang, B.: Efficient Compressing and Tuning Methods for Large Language
     Models: A Systematic Literature Review. ACM Computing Surveys 57(10), 1–39 (2025) https:
     //doi.org/10.1145/3728636

[35] Belhaouari, S.B., Kraidia, I.: Efficient Self-attention with Smart Pruning for Sustain-
     able Large Language Models. Scientific Reports 15(1) (2025) https://doi.org/10.1038/
     s41598-025-92586-5

[36] Li, D., Shen, T., Zhou, Y., Yang, B., Liu, Z., Yang, M., Ghanem, B., Yang, Y., Zhong, Y.,
     Yang, M.-H.: Optimizing Singular Spectrum for Large Language Model Compression (2025).
     https://doi.org/10.48550/arxiv.2502.15092

[37] Dantas, P.V., Cordeiro, L.C., Junior, W.S.S.: A Review of State-of-the-art Techniques for Large
     Language Model Compression. Complex & Intelligent Systems 11(9) (2025) https://doi.org/
     10.1007/s40747-025-02019-z

[38] Tihanyi, N., Bisztray, T., Ferrag, M.A., Cherif, B., Dubniczky, R.A., Jain, R., Cordeiro, L.C.:
     Vulnerability Detection: From Formal Verification to Large Language Models and Hybrid
     Approaches: A Comprehensive Overview. arxiv (2025). https://doi.org/10.48550/arxiv.2503.
     10784

[39] Wu, H., Barrett, C., Narodytska, N.: Lemur: Integrating Large Language Models in Automated
     Program Verification (2023). https://doi.org/10.48550/arxiv.2310.04870

[40] AI, L., School, T.N..M., Ji, S., Song, Z., Zhong, F., Jia, J., Wu, Z., Cao, Z., Xu, T.: Enhanc-
     ing Large Language Model Efficiencyvia Symbolic Compression: A Formal Approach Towards
     Interpretability (2025). https://doi.org/10.48550/arxiv.2501.18657

[41] Ermon, S., Gomes, C., Sabharwal, A., Selman, B.: Designing Fast Absorbing Markov Chains.
     Proceedings of the AAAI Conference on Artificial Intelligence 28(1) (2014) https://doi.org/
     10.1609/aaai.v28i1.8843

[42] Craig, B.A., Sendi, P.P.: Estimation of the Transition Matrix of a Discrete-Time Markov Chain.
     Health Economics 11(1), 33–42 (2002) https://doi.org/10.1002/hec.654

[43] Clarke, E.M.: Model Checking, pp. 54–56. Springer, Berlin, Heidelberg, Germany (1997). https:
     //doi.org/10.1007/bfb0058022



                                                32
[44] Zhou, D., Schärli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui, C., Bousquet,
     O., Le, Q., Chi, E.: Least-to-Most Prompting Enables Complex Reasoning in Large Language
     Models. arxiv (2022) https://doi.org/10.48550/arxiv.2205.10625

[45] Staton, S., Yang, H., Wood, F., Heunen, C., Kammar, O.: Semantics for Probabilistic Program-
     ming: Higher-order Functions, Continuous Distributions, and Soft Constraints. In: Proceedings
     of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science. LICS’16, pp.
     525–534. ACM, New York, NY, USA (2016). https://doi.org/10.1145/2933575.2935313

[46] Gogate, V., Domingos, P.: Probabilistic theorem proving. Communications of the ACM 59(7),
     107–115 (2016) https://doi.org/10.1145/2936726

[47] Kroening, D., Strichman, O.: Decision Procedures. Springer, Berlin, Heidelberg, Germany
     (2016). https://doi.org/10.1007/978-3-662-50497-0

[48] Clarke, E., Kroening, D., Lerda, F.: A Tool for Checking ANSI-C Programs, pp. 168–176.
     Springer, Berlin, Heidelberg, Germany (2004). https://doi.org/10.1007/978-3-540-24730-2_15

[49] Böhm, C., Jacopini, G.: Flow Diagrams, Turing Machines and Languages with Only Two
     Formation Rules. Communications of the ACM 9(5), 366–371 (1966) https://doi.org/10.1145/
     355592.365646

[50] Rozier, K.Y., Dureja, R., Irfan, A., Johannsen, C., Nukala, K., Shankar, N., Tinelli, C., Vardi,
     M.Y.: MoXI: An Intermediate Language for Symbolic Model Checking, pp. 26–46. Springer,
     Cham, Switzerland (2024). https://doi.org/10.1007/978-3-031-66149-5_2

[51] Clarke, E.M., Emerson, E.A.: Design and Synthesis of Synchronization Skeletons Using Branch-
     ing Time Temporal Logic, pp. 52–71. Springer, Berlin, Heidelberg, Germany (1982). https:
     //doi.org/10.1007/bfb0025774

[52] Clarke, E.M.: The Birth of Model Checking, pp. 1–26. Springer, Berlin, Heidelberg, Germany
     (2008). https://doi.org/10.1007/978-3-540-69850-0_1

[53] Pnueli, A.: The Temporal Logic of Programs. In: 18th Annual Symposium on Foundations of
     Computer Science (sfcs 1977), pp. 46–57. IEEE, Providence, RI, USA (1977). https://doi.org/
     10.1109/sfcs.1977.32

[54] Emerson, E.A., Halpern, J.Y.: “Sometimes” and “Not Never” Revisited: on Branching versus
     Linear Time (Preliminary Report). In: Proceedings of the 10th ACM SIGACT-SIGPLAN Sym-
     posium on Principles of Programming Languages - POPL’83. POPL’83, pp. 127–140. ACM
     Press, New York, NY, United States (1983). https://doi.org/10.1145/567067.567081

[55] Vizel, Y., Weissenbacher, G., Malik, S.: Boolean Satisfiability Solvers and Their Applications
     in Model Checking. Proceedings of the IEEE 103(11), 2021–2035 (2015) https://doi.org/10.
     1109/jproc.2015.2455034

[56] Bryant: Graph-Based Algorithms for Boolean Function Manipulation. IEEE Transactions on
     Computers C–35(8), 677–691 (1986) https://doi.org/10.1109/tc.1986.1676819

[57] Clarke, E., Biere, A., Raimi, R., Zhu, Y.: Bounded Model Checking Using Satisfiability
     Solving. Formal Methods in System Design 19(1), 7–34 (2001) https://doi.org/10.1023/a:
     1011276507260

[58] Menezes, R.S., Aldughaim, M., Farias, et al.: ESBMC v7.4: Harnessing the Power of Intervals:
     (Competition Contribution), pp. 376–380. Springer, Luxembourg City, Luxembourg (2024).
     https://doi.org/10.1007/978-3-031-57256-2_24

[59] Clarke, E.M., Klieber, W., Nováček, M., Zuliani, P.: Model Checking and the State Explosion


                                                 33
    Problem, pp. 1–30. Springer, Berlin, Heidelberg, Germany (2012). https://doi.org/10.1007/
    978-3-642-35746-6_1

[60] Dhaussy, P., Roger, J.-C., Boniol, F.: Reducing State Explosion with Context Modeling for
     Model-Checking. In: 2011 IEEE 13th International Symposium on High-Assurance Systems
     Engineering, pp. 130–137. IEEE, Boca Raton, FL, USA (2011). https://doi.org/10.1109/hase.
     2011.24

[61] Mukherjee, R., Tautschnig, M., Kroening, D.: v2c – A Verilog to C Translator, pp. 580–586.
     Springer, Berlin, Heidelberg (2016). https://doi.org/10.1007/978-3-662-49674-9_38

[62] Donaldson, A.F., Haller, L., Kroening, D., Rümmer, P.: Software Verification Using
     k-Induction, pp. 351–368. Springer, Berlin, Heidelberg (2011). https://doi.org/10.1007/
     978-3-642-23702-7_26

[63] Barrett, C., Tinelli, C.: Satisfiability Modulo Theories, pp. 305–343. Springer, Cham, Switzer-
     land (2018). https://doi.org/10.1007/978-3-319-10575-8_11

[64] Barreto, R., Cordeiro, L., Fischer, B.: Verifying Embedded C Software with Timing Constraints
     Using an Untimed Bounded Model Checker. In: 2011 Brazilian Symposium on Computing
     System Engineering, pp. 46–52. IEEE, Los Alamitos, CA, USA (2011). https://doi.org/10.
     1109/sbesc.2011.19

[65] Brummayer, R., Biere, A.: Boolector: An Efficient SMT Solver for Bit-Vectors and
     Arrays, pp. 174–177. Springer, Berlin, Heidelberg, Germany (2009). https://doi.org/10.1007/
     978-3-642-00768-2_16

[66] Ho, Y.-S., Chauhan, P., Roy, P., Mishchenko, A., Brayton, R.: Efficient Uninterpreted Function
     Abstraction and Refinement for Word-Level Model Checking. In: 2016 Formal Methods in
     Computer-Aided Design (FMCAD), pp. 65–72. IEEE, Mountain View, CA, USA (2016). https:
     //doi.org/10.1109/fmcad.2016.7886662

[67] Tabuchi, N., Sumii, E., Yonezawa, A.: Regular Expression Types for Strings in a Text
     Processing Language. Electronic Notes in Theoretical Computer Science 75, 95–113 (2003)
     https://doi.org/10.1016/s1571-0661(04)80781-3

[68] Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, et al.: Language Models are Few-Shot
     Learners. arxiv (2020) https://doi.org/10.48550/arxiv.2005.14165

[69] Pearce, H., Ahmad, B., Tan, B., Dolan-Gavitt, B., Karri, R.: Asleep at the Keyboard? Assess-
     ing the Security of GitHub Copilot’s Code Contributions, vol. 68, pp. 96–105. Association
     for Computing Machinery (ACM), San Francisco, CA, USA (2025). https://doi.org/10.1145/
     3610721

[70] Zheng, S., Huang, C., Yu, F., Yao, J., Ye, J., Chen, T., Luo, Y., Ding, N., BAI, L., Cui, G., Ye,
     P.: SCI-Verifier: Scientific Verifier with Thinking (2025) https://doi.org/10.48550/arxiv.2509.
     24285

[71] Allamanis, M., Barr, E.T., Devanbu, P., Sutton, C.: A Survey of Machine Learning for Big
     Code and Naturalness. ACM Computing Surveys 51(4), 1–37 (2018) https://doi.org/10.1145/
     3212695

[72] Rozière, B., Gehring, J., Gloeckle, et al.: Code Llama: Open Foundation Models for Code.
     arxiv (2023) https://doi.org/10.48550/arxiv.2308.12950

[73] Lemieux, C., Inala, J.P., Lahiri, S.K., Sen, S.: CodaMosa: Escaping Coverage Plateaus in Test
     Generation with Pre-trained Large Language Models. In: 2023 IEEE/ACM 45th International



                                                 34
    Conference on Software Engineering (ICSE), pp. 919–931. IEEE, Melbourne, VIC, Australia
    (2023). https://doi.org/10.1109/icse48619.2023.00085

[74] Frantar, E., Ashkboos, S., Hoefler, T., Alistarh, D.: GPTQ: Accurate Post-Training Quanti-
     zation for Generative Pre-trained Transformers. arxiv (2022) https://doi.org/10.48550/arxiv.
     2210.17323

[75] Dettmers, T., Pagnoni, A., Holtzman, A., Zettlemoyer, L.: QLoRA: Efficient Finetuning of
     Quantized LLMs. arxiv (2023) https://doi.org/10.48550/arxiv.2305.14314

[76] Frantar, E., Alistarh, D.: SparseGPT: Massive Language Models Can Be Accurately Pruned
     in One-Shot. arxiv (2023) https://doi.org/10.48550/arxiv.2301.00774

[77] Hinton, G., Vinyals, O., Dean, J.: Distilling the Knowledge in a Neural Network. arxiv (2015)
     https://doi.org/10.48550/arxiv.1503.02531

[78] Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.: LoRA:
     Low-Rank Adaptation of Large Language Models. arxiv (2021) https://doi.org/10.48550/arxiv.
     2106.09685

[79] Brauße, F., Shmarov, F., Menezes, R., Gadelha, M.R., Korovin, K., Reger, G., Cordeiro, L.C.:
     ESBMC-CHERI: Towards Verification of C programs for CHERI Platforms with ESBMC. In:
     Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and
     Analysis. ISSTA’22, pp. 773–776. ACM, Seoul, South Korea (2022). https://doi.org/10.1145/
     3533767.3543289

[80] Moura, L., Bjørner, N.: Z3: An Efficient SMT Solver, pp. 337–340. Springer, Berlin, Heidelberg
     (2008). https://doi.org/10.1007/978-3-540-78800-3_24

[81] Tihanyi, N., Bisztray, T., Jain, R., Ferrag, M.A., Cordeiro, L., Mavroeidis, V.: The For-
     mAI Dataset: Generative AI in Software Security through the Lens of Formal Verification.
     In: International Conference on Predictive Models in Software Engineering (2023). https:
     //doi.org/10.1145/3617555.3617874

[82] Song, K., Gadelha, M.R., Brauße, F., Menezes, R.S., Cordeiro, L.C.: ESBMC v7.3: Model
     Checking C++ Programs using Clang AST (2023). https://doi.org/10.48550/arxiv.2308.05649

[83] Gadelha, M.R., Menezes, R.S., Cordeiro, L.C.: ESBMC 6.1: Automated Test Case Genera-
     tion Using Bounded Model Checking. International Journal on Software Tools for Technology
     Transfer 23(6), 857–861 (2020) https://doi.org/10.1007/s10009-020-00571-2

[84] Gong, J., Duan, N., Tao, Z., Gong, Z., Yuan, Y., Huang, M.: How Well Do Large Language Mod-
     els Serve as End-to-End Secure Code Agents for Python? (2024). https://doi.org/10.48550/
     arxiv.2408.10495

[85] Akhond, M.R., Chakraborty, S., Uddin, G.: LLM For Loop Invariant Generation and Fixing:
     How Far Are We? (2025). https://doi.org/10.48550/arxiv.2511.06552

[86] Kamath, A., Senthilnathan, A., Chakraborty, S., Deligiannis, P., Lahiri, S.K., Lal, A., Rastogi,
     A., Roy, S., Sharma, R.: Finding Inductive Loop Invariants using Large Language Models
     (2023). https://doi.org/10.48550/arxiv.2311.07948

[87] Yan, Z., Fang, W., Li, M., Li, M., Liu, S., Xie, Z., Zhang, H.: AssertLLM: Generating Hard-
     ware Verification Assertions from Design Specifications via Multi-LLMs. In: Proceedings of the
     30th Asia and South Pacific Design Automation Conference. ASPDAC’25, pp. 614–621. ACM,
     Tokyo, Japan (2025). https://doi.org/10.1145/3658617.3697756

[88] Wen, C., Cao, J., Su, J., Xu, Z., Qin, S., He, M., Li, H., Cheung, S.-C., Tian, C.: Enchanting


                                                 35
    Program Specification Synthesis by Large Language Models Using Static Analysis and Pro-
    gram Verification, pp. 302–328. Springer, Cham, Switzerland (2024). https://doi.org/10.1007/
    978-3-031-65630-9_16

[89] Cohen, J.: Statistical Power Analysis for the Behavioral Sciences. Routledge, New York, NY
     (2013). https://doi.org/10.4324/9780203771587

[90] Robert, C., Casella, G.: Introducing Monte Carlo Methods with R. Springer, New York, NY
     (2010). https://doi.org/10.1007/978-1-4419-1576-4

[91] Agresti, A., Coull, B.A.: Approximate is Better than “Exact” for Interval Estimation of Bino-
     mial Proportions. The American Statistician 52(2), 119–126 (1998) https://doi.org/10.1080/
     00031305.1998.10480550

[92] Brown, L.D., Cai, T.T., DasGupta, A.: Interval Estimation for a Binomial Proportion.
     Statistical Science 16(2) (2001) https://doi.org/10.1214/ss/1009213286

[93] Boucheron, S., Lugosi, G., Massart, P.: Concentration Inequalities: A Nonasymptotic Theory
     of Independence. Oxford University Press, Oxford, UK (2013). https://doi.org/10.1093/acprof:
     oso/9780199535255.001.0001

[94] Papaspiliopoulos, O.: High-Dimensional Probability: An Introduction with Applications
     in Data Science. Quantitative Finance 20(10), 1591–1594 (2020) https://doi.org/10.1080/
     14697688.2020.1813475

[95] Wasserstein, R.L.: Monte Carlo: Concepts, Algorithms, and Applications. Technometrics 39(3),
     338–338 (1997) https://doi.org/10.1080/00401706.1997.10485133

[96] Durrett, R.: Probability: Theory and Examples. Cambridge University Press, Cambridge, UK
     (2019). https://doi.org/10.1017/9781108591034

[97] Rozière, B., Gehring, J., Gloeckle, et al.: Code Llama: Open Foundation Models for Code
     (2023). https://doi.org/10.48550/ARXIV.2308.12950

[98] Montenegro, R., Tetali, P.: Mathematical Aspects of Mixing Times in Markov Chains. Foun-
     dations and Trends® in Theoretical Computer Science 1(3), 237–354 (2006) https://doi.org/
     10.1561/0400000003




                                               36
