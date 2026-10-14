                                                          Data Verification is the Future of Quantum Computing Copilots
                                                       Junhao Song1 * , Ziqian Bi2 * , Xinliang Chia3 , William Knottenbelt1 , Yudong Cao4†
                                                                                  1
                                                                            Department of Computing, Imperial College London, UK
                                                                                 2
                                                                            Department of Computer Science, Purdue University, USA
                                                                3
                                                                  Department of Applied Mathematics, National Chung Hsing University, Taiwan
                                                                         4
                                                                           BCG X AI Science Institute, Boston Consulting Group, USA
                                                  junhao.song23@imperial.ac.uk, bi32@purdue.edu, marcus.chia@ai-agent-lab.com, w.knottenbelt@imperial.ac.uk,
                                                                                            cao.yudong@bcg.com
arXiv:2602.04072v1 [quant-ph] 3 Feb 2026




                                                                       Abstract                                         Only Inference              Reliable LLM with Closed Loop Verification

                                             Quantum program generation demands a level of precision
                                             that may not be compatible with the statistical reasoning car-
                                             ried out in the inference of large language models (LLMs).                                                                        Valid
                                                                                                                                                                              design       Reliable LLM
                                             Hallucinations are mathematically inevitable and not address-                 Prompt                      Prompt                 space
                                             able by scaling, which leads to infeasible solutions. We argue                                                                           Only Inference
                                                                                                                                                                             Possible     or RAG
                                             that architectures prioritizing verification are necessary for                                                                design space
                                             quantum copilots and AI automation in domains governed
                                             by constraints. Our position rests on three key points: ver-                                                                    Supervised Fine-
                                             ified training data enables models to internalize precise con-                                                                   Tuning (SFT)

                                             straints as learned structures rather than statistical approxima-
                                             tions; verification must constrain generation rather than filter     Quantum Computing Copilot    Quantum Computing Copilot
                                             outputs, as valid designs occupy exponentially shrinking sub-
                                             spaces; and domains where physical laws impose correctness
                                             criteria require verification embedded as architectural primi-
                                             tives. Early experiments showed LLMs without data verifica-
                                                                                                                                      ...                          ...
                                             tion could only achieve a maximum accuracy of 79% in cir-                                                                     Verification
                                             cuit optimization. Our positions are formulated as quantum                 Output designs              Output designs                        Data of verified
                                             computing and AI4Research community imperatives, calling                                                                                        designs
                                             for elevating verification from afterthought to architectural          Low success probability       100% correct outputs
                                                                                                                     (w/o data verification)      (w/ data verification)
                                             foundation in AI4Research.

                                                                                                                 Figure 1: Without data verification, outputs scatter across the
                                                                 1    Introduction                               exponentially low success probability space (red circle in
                                           The quantum computing stack requires tools for program                the top right corner). Even Retrieval-Augmented Gener-
                                           generation and program compilation for both near-term                 ation (RAG) is insufficient to guarantee correctness in this
                                           physical quantum devices (e.g., superconducting qubits (Lu            absence. When data verification is integrated into the train-
                                           et al. 2024), trapped-ion systems (Kreppel et al. 2024)               ing loop, only validated designs from the constrained vali-
                                           and neutral atoms arrays (Choi et al. 2023; Karuppasamy               dation space are used, ensuring 100% correct outputs. The
                                           et al. 2025)) and future fault-tolerant quantum comput-               snowflake symbol represents weights are frozen. The flame
                                           ers based on surface codes (Google 2023), qLDPC codes                 symbol represents that weights are trainable.
                                           (Breuckmann and Eberhardt 2021) and Bosonic codes
                                           (Cai et al. 2021). Concurrently, large language models
                                           (LLMs) assisted research is becoming increasingly prevalent
                                           across various disciplines, but their limitations are gradually       demand zero tolerance for errors, unlike the typical percent-
                                           emerging within the field of quantum computing. Such prob-            age error metrics used for testing LLMs.
                                           lems pose formidable challenges for AI automation with a                 Reflecting these challenges, synthesizing optimized quan-
                                           quantum computing copilot: (1) They cross multiple layers             tum circuits remains a labor-intensive process that demands
                                           of abstraction from high-level circuit descriptions to low-           manual insights and complex mathematical proofs. These
                                           level gate arrangements, and (2) have rigorous problem defi-          processes are inherently inefficient, difficult to formalize,
                                           nitions with precise verification methods. Critically, they (3)       and prone to errors across abstraction layers. Consequently,
                                              * These authors contributed equally.                               producing an end-to-end optimized design and compilation
                                              †
                                                Corresponding author.                                            of a quantum program can often be labor-intensive for a
                                           Copyright © 2026, Association for the Advancement of Artificial       complete algorithm, such as detailed resource estimations
                                           Intelligence (www.aaai.org). All rights reserved.                     for quantum factoring (Gidney and Ekerå 2021; Gidney
2025). The resulting complexity of such human-generated                                 2    Positions
program design and compilation makes these designs chal-         Definition. We define key terms used throughout this paper:
lenging for even trained experts to understand and replicate.      • Verification-aware model: An LLM that has been ex-
This difficulty motivated the creation of foundational tools         posed to formally verified training data where each ex-
including Qualtran (Harrigan et al. 2024), pyLIQTR (Oben-            ample satisfies domain-specific correctness constraints
land et al. 2025), Bench-Q (ZapataAI 2024), Stim (Gidney             (e.g., circuit unitarity, mathematical equivalence proofs).
2021), TQEC (Team 2024) and Pandora (Moflic and Paler                This is distinct from models trained on unverified code
2025). Such tools provide the foundational infrastructure            repositories.
for the development of quantum computing copilots. Re-
cent AI systems show promise: IBM’s Qiskit Code Assis-             • Data verification: The process of formally proving that
tant outperforms general models on quantum tasks (Dupuis             training examples satisfy domain constraints using auto-
et al. 2024), DeepMind’s AlphaTensor-Quantum achieved                mated theorem provers (Lean, Z3) before inclusion in the
37-47% T-gate reductions (Ruiz et al. 2025), and Google’s            training set.
AlphaEvolve generated circuit compilation functions for            • A priori constraints: Verification checks embedded
quantum simulation (Novikov et al. 2025). These successes            within the generation process that prevent invalid outputs
reveal LLMs potential to accelerate development cycles and           from being produced, as opposed to post-hoc filtering of
discover non-obvious optimization patterns that human de-            completed outputs.
signers might overlook or take longer to produce.                   A central issue concerning the limitation of the current
   However, fundamental limitations constrain these ap-          LLMs capabilities is infeasible solutions. Regardless of how
proaches. LLMs perform pattern matching over training dis-       the size of the model and training data set can be scaled
tributions rather than formal reasoning, leading to system-      up, infeasible solutions are known to be a fundamental bar-
atic failures when tasks require multi-step logical operations   rier (Karpowicz et al. 2025). For highly constrained applica-
(Dziri et al. 2023). Theoretical analysis establishes that in-   tions such as quantum program generation and compilation,
feasible solutions are mathematically inevitable in LLMs         where there is no tolerance for any error, does this mean that
without data verification, not transient bugs awaiting engi-     LLMs are doomed to fail them? In this paper, we present our
neering solutions (Karpowicz et al. 2025). For quantum cir-      positions that point to a possible way to systemically remove
cuits, where correctness requires satisfying rigid mathemat-     infeasible solutions by creating verified datasets. More con-
ical constraints across hundreds or thousands of interdepen-     cretely, we state the positions in this paper as follows:
dent gates, statistical improvements in average performance      P1 Data verification must be the minimum requirement
cannot substitute for guaranteed correctness (Limitation             for quantum copilots. This is largely driven by the na-
1). The insufficient training data problem compounds these           ture of the problem (Fig. 1). Any LLM that has a non-
quantum copilot issues (Limitation 2). The most compre-              zero chance of producing wrong answers will not be
hensive quantum dataset (QDataSet) (Perrier, Youssry, and            trusted as a viable component of a quantum copilot.
Ferrie 2022) required more than three months (2020-2021)         P2 Verification should provide a priori constraints, not
of HPC cluster time to generate 14TB of validated data               a posteriori filtering. As the number of design building
covering only one-qubit and two-qubits systems. Bench-               blocks e.g. qubits grows, the fraction of valid designs in
mark evaluations reveal that LLMs exhibit consistent er-             the space of all possible designs decreases exponentially
ror patterns on quantum tasks, with fine-tuning sometimes            (Fig. 1). Therefore, any strategy relying on a posteriori
underperforming few-shot learning (Yang et al. 2024). The            filtering will have an exponentially low likelihood of ran-
highly constrained search domain of valid quantum circuits           domly generating a valid design.
bounded by unitarity, hardware topology and gate fidelity
                                                                 P3 Verification-aware architecture required for highly
demands verification mechanisms that current LLM archi-
                                                                     constrained scientific domains. We advocate that ver-
tectures cannot provide internally (Limitation 3).
                                                                     ified datasets become a common practice in scientific
   Considering the three limitations mentioned above, this
                                                                     domains that, like quantum computing, can be revolu-
paper advances three positions:
                                                                     tionized by AI automation but at the same time involve
 • Data verification as minimum requirement. Verified                hard constraints such as laws of physics or mathematical
   datasets ensure copilots internalize constraints as learned       axioms. Examples of such scientific disciplines include
   structure, not statistical approximation.                         drug discovery (Masters, Mahmoud, and Lill 2025), ma-
 • A priori constraints over a posteriori filtering. Verifi-         terials identification (Ferguson et al. 2025) and engineer-
   cation must constrain generation; filtering exponentially         ing design with physical constraints (Wang et al. 2025).
   growing invalid outputs is prohibitive.
 • Verification-first paradigm for AI4Research. Domains                          3   Position Arguments
   with physical laws require verification as architectural      We first describe the formulation of the program generation
   primitives in training and generation.                        and compilation problem, using Cuccaro Adder (Cuccaro
The subsequent sections are structured as follows: Section       et al. 2004) as an example. The adder is an in-place quantum
2 introduces our positions, Section 3 elaborates on both the     program that performs the addition of two n-bit integers x
positions and their supporting arguments, and Section 4 dis-     and y. The transformation of the adder can be described as:
cusses future directions.”                                                      |c0 ⟩|x⟩|y⟩|0⟩ 7→ |c0 ⟩|x⟩|x + y⟩,         (1)
        (a) Level 1: module based circuit design                 (c) Modular substitution

        c0                                            c0
        y0     MAJ                           UMA      s0
        x0                                            x0                                                             Potential improvements
                                                                                                                     based on precise
        y1             MAJ          UMA               s1                                                             mathematical insights
                                                                                                                     about quantum circuits:
        x1                                            x1                                                             parallelized execution,
         z                                            z ⊕ s2                                                         gate position swap


        (b) Level 2: decomposition of individual modules
                                                               (d) Optimized circuit

                                                                 c0                                     c0
             MAJ      =                                           y0                                    s0           Applying the
                                                                                                                     improvements leads to
                                                                  x0                                    x0           an optimized circuit with
                                                                                                                     signi cantly lower depth
                                                                  y1                                    s1

             UMA      =                 =                         x1                                    x1
                                                                  z                                     z ⊕ s2
   fi
Figure 2: The key features of quantum program generation (step a) and compilation (steps b-d), using the Cuccaro Adder
as an example. (a) The first level of abstraction where circuit design is at a modular level. (b) The second level where each
module is further decomposed into elementary gates (NOT, CNOT and Toffoli). (c) Expanding the modules to reveal the overall
circuit design with only the elementary gates, and identifying opportunities for improvements. (d) Applying the improvements
(parallelized execution of gates and gate position swap due to commutativity) yields an optimized circuit with lower depth.


where c0 is an incoming carry bit and the extra ancilla in |0⟩           example in a different context (fault-tolerant quantum im-
captures the overflow in the addition process. Any adder de-             plementation), but also for the Cuccaro adder. As such, the
sign must exactly satisfy the requirement described in Equa-             task of quantum program generation and compilation is still
tion 1 or any equivalent statement. This places a constraint             a labor-intensive effort that highly depends on the artisanal
of precise mathematical specification that may not apply                 skills of human expert.
to other AI automation tasks.                                               Faced with the aforementioned key features of the pro-
   In Fig. 2a we show an example for n = 2, where the                    gram generation and compilation problem, namely precision
adder is constructed by a cascade of Majority (MAJ) mod-                 in the mathematical specification, leaky abstraction of the
ules followed by a cascade of UnMajority-and-Add (UMA)                   design space, and labor intensity of the design task, it is im-
modules. This is the program generation step. The generated              portant to be intentional in the design of any AI automation
problem can be further compiled by expanding the modules                 systems. To that end, we expand on the positions laid out in
with elementary gates (Fig. 2b), substituted into the origi-             Section 2 as the following.
nal circuit for further improvement (Fig. 2c) yield an op-                  (P1) Data verification must be the minimum require-
timized circuit (Fig. 2d) that breaks the modular design in              ment for quantum copilots, due to the limitation of cur-
the original iteration. Such a pattern of leaky abstraction is           rent LLMs in understanding the structure of quantum
common in quantum program generation and compilation,                    circuit compilations. The design of quantum circuits comes
where two levels of description (such as Level 1 in Fig. 2a              with exact constraints that need to be satisfied. In the case of
and Level 2 in Fig. 2b) need to be merged (“leaked”) into                arithmetic circuit design such as the quantum adder, unitar-
each other to produce an optimized implementation. A con-                ity of the circuit operation implies that the logical opera-
sequence of such leaky abstraction is non-decomposibility                tion implemented by the circuit needs to be reversible. How
of the design space, namely that suboptimal designs at a                 to ensure that the AI system internalizes such precise con-
certain level of abstraction (such as the highlighted design             straints? Our position is that verified training data ensures
on UMA in Fig. 2b, which is arguably less optimal than                   that the model observes only reversible, resource-annotated
the other alternative with only 3 gates) do not necessarily              circuits; without it the model cannot learn the precise mathe-
yield suboptimal designs when expanding into lower layers                matical constraints that underpins the quantum program gen-
of abstraction. The highlighted design of UMA in Fig. 2b                 eration and compilation task.
turns out to be more advantageous in the overall circuit op-                Training quantum copilots on unverified data from
timization by parallelizing gate executions (Cuccaro et al.              sources such as low quality or uncommented code consti-
2004). The improvements shown in Fig. 2 are but a subset                 tutes implicit data poisoning. Unlike natural language tasks
of improvements that can be made (Cuccaro et al. 2004).                  where massive data volumes average out noise to approxi-
However, finding those detailed improvements with leaky                  mate ground truth, quantum circuit constraints do not admit
abstraction is largely a task carried out by human experts.              this: a single invalid gate sequence violates unitarity regard-
In 2018, Craig Gidney (Gidney 2018) is another one such                  less of how many valid examples surround it in the solution
                                                                                
                                                                                                                                               J S W  R V V B    E
                                                                                                                                               J S W  R V V B   E
                                                                                                                                               J H P P D  B   E
 $ Y J   & R Q I L G H Q F H  R Q  & R U U H F W  $ Q V Z H U    


                                                                                                                                             J H P P D  B   E



                                                                                


                                                                                


                                                                                


                                                                                 
                                                                                                                                                           
                                                                                                      1 X P E H U  R I  % L W V

             Figure 3: Average confidence assigned to the correct answer
             for the top-5 performing models. Higher values indicate bet-
             ter calibration. GPT-OSS models show higher confidence
             on correct answers compared to Gemma3 models, suggest-                                                                                                      Figure 4: Average accuracy per LLMs. The dashed circle
             ing better uncertainty quantification. Note: qwen3:1.7b,                                                                                                    marks the 25% random baseline; verification-aware models
             despite ranking among the top-5 in accuracy, is omitted                                                                                                     clearly exceed it, while unconstrained checkpoints remain
             because it fails to produce valid token-level probabilities                                                                                                 inside.
             (outputting malformed responses that yield zero confidence
             scores).
                                                                                                                                                                         tokens corresponding to the four options (A, B, C, D) from
                                                                                                                                                                         the model’s output distribution. Since raw log-probabilities
             space. This creates an anti-scaling phenomenon where addi-                                                                                                  do not sum to a consistent value across the four options,
             tional unverified data amplifies rather than dilutes errors.                                                                                                we apply softmax normalization to obtain calibrated con-
                To substantiate our position we derived an evaluation suite                                                                                              fidence scores that form a proper probability distribution.
             directly from the verified MAJ/UMA corpus described ear-                                                                                                    GPT-OSS models consistently assign 60–80% confidence to
             lier.                                                                                                                                                       correct responses across all bit-widths, while Gemma3 mod-
                Experimental Setup. We evaluated 34 publicly available                                                                                                   els remain in the 20–35% range. This disparity suggests that
             LLMs spanning 270M to 120B parameters, deployed via Ol-                                                                                                     verification-aware training not only improves accuracy but
             lama with default parameters. Each model answered 70,000                                                                                                    also enhances uncertainty quantification: models exposed to
             multiple-choice questions (10,000 per bit-width from 2 to                                                                                                   verified data exhibit more appropriate confidence when pro-
             8 qubits). The evaluation harness includes a retry mecha-                                                                                                   ducing correct answers.
             nism (up to 3 attempts) for malformed responses, with unan-                                                                                                    Several models (e.g., mixtral:8x7b, deepseek-r1
             swered questions counted as incorrect.                                                                                                                      variants) scored below the 25% random baseline due to
                For every n ∈ {2, . . . , 8} we construct 10,000 multiple-                                                                                               malformed outputs—verbose explanations or refusals rather
             choice questions where four candidate circuits all satisfy                                                                                                  than single-letter answers. This failure mode reinforces our
             the adder specification but differ in gate count, depth, and                                                                                                position: models without verification-aware training cannot
             Toffoli usage. The ground-truth answer is the circuit with                                                                                                  reliably engage with formally constrained tasks.
             the minimum score which is a weighted combination of cir-                                                                                                      (P2) Verification should provide a priori constraints,
             cuit parameters 0.5 × Toffolin + 0.25 × Depthn + 0.25 ×                                                                                                     not a posteriori filtering, due to domain constraints in
             TotalGatesn , so that each decision compares equally valid                                                                                                  quantum circuit search spaces. Models that internalize ex-
             but differently optimized implementations. Models with                                                                                                      plicit penalties for depth and Toffoli count rarely emit dis-
             verification knowledge (gemma3:12b, gpt-oss:120b)                                                                                                           allowed options, whereas unconstrained models require ag-
             achieve 0.60-0.79 accuracy, while generic models hover near                                                                                                 gressive post-hoc rejection sampling that wastes compute
             a random baseline (0.21-0.29). The radar view in Figure 4                                                                                                   and still leaks invalid answers. Consider the adder design
             compresses these results by averaging each model across bit-                                                                                                space: with d gate choices per position and O(n) positions,
             widths: these verification-aware models dominate the outer                                                                                                  the total space grows as O(dn ). Constraints reduce valid
             ring, while unconstrained copilots cluster inside the dashed                                                                                                designs to O(δ n ) for δ < d, yielding a valid fraction of
             25% circle. This quantitative gap demonstrates that scaling                                                                                                 O((δ/d)n ) that decreases exponentially. Post-hoc filtering
             parameter counts alone cannot guarantee correctness with-                                                                                                   thus incurs exponential cost.
             out verified data and structural constraints.                                                                                                                  Concretely, to demonstrate our position, we have gen-
                Beyond accuracy, we examine model calibration (Fig-                                                                                                      erated a dataset of over 200,000 adder circuit designs all
             ure 3). For each question, we extract the log-probabilities of                                                                                              of which implement the transformation in Equation 1 for
any sized input x and y. Each design in the dataset is for-        sibility; this motivates multidisciplinary design optimization
mally verified with Lean to show correctness for any n and         architectures that coordinate interacting subsystems under a
with Z3 to show correctness for modular level decomposi-           global objective and shared constraints (Martins and Lambe
tion of MAJ and UMA operations. Through a process that             2013).
combines exhaustive search and formal verification (with              At the ecosystem level, robustness and generalization
Lean and Z3), we discovered 540 MAJ circuit designs and            hinge on community agreed benchmarks, standardized eval-
529 UMA circuit designs by searching over circuit depths           uation metrics, curated archives with stable metadata/in-
3 through 6. The combination of the designs leads to over          terfaces and uncertainty quantification, such as verification
540 × 529 = 285660 distinct adder circuit designs. How-            practices elevated from individual labs to shared infrastruc-
ever, this number is still a negligible fraction of possible       ture, so that models are developed and assessed against
circuit designs. Each MAJ/UMA module is in a space of              domain-meaningful, reproducible criteria rather than ad-hoc
approximately 12.2 million gate arrangements across depths         proxies (Ferguson et al. 2025).
3-6. The combined design space exceeds 148 trillion config-
urations, yet formal verification identifies only over 200,000                      4    Future Directions
valid adders (a ratio on the order of 10−9 ). This exponen-        Two main research directions follow from our verification
tial gap between possible and valid designs renders post-hoc       first paradigm:
filtering computationally prohibitive.
    Recent systems adopt this principle: QCircuitNet pairs           • FD1 Quantum copilots architectures must integrate for-
tasks with executable oracles (Yang et al. 2024), AlphaTen-            mal verification directly into the LLMs token generation
sor builds correctness into search objectives (Fawzi et al.            loop rather than treating it as post-hoc validation (details
2022), and AlphaEvolve filters variants through machine-               below).
checkable specifications (Novikov et al. 2025), demonstrat-          • FD2 The community needs constraint rich benchmarks,
ing that embedding verification within generation loops en-            releasing such datasets under open licenses would estab-
ables scalable discovery.                                              lish reproducible standards for quantum copilot develop-
    (P3) Verification-aware architecture is required not               ment and enable rigorous cross system comparison.
only for quantum circuit design but also for other prob-              For the FD1, we suggest that each proposed circuit frag-
lems throughout science. The design of the adder circuit           ment should satisfy satisfiability modulo theories con-
in Fig. 2 is at the level of logical circuit design. It can be     straint or symbolic specifications before being committed
lowered into a more detailed compilation towards a specific        to the design. So that can transform verification from a bi-
architecture of fault tolerant quantum hardware, such as 2D        nary filter into a structured exploration guide that avoids in-
surface code (Gidney 2018). In this case, a similar leaky ab-      valid paths in quantum copilot’s real-time generation.
straction and non-decomposability apply between the log-              For the FD2, the constraint rich benchmarks that go be-
ical quantum circuit and its physical implementation on a          yond the quantum adder (this paper example) adder evalua-
fault tolerant quantum computer.                                   tion to encompass modular multiplication, quantum Fourier
    A general formulation of such leaky abstraction is a set-      transforms, hardware specific routing constraints and zero
ting where one chooses implementations for components              tolerance resource costs. Also, we suggest each benchmark
g1 , . . . , gm and then compose them into a system scored by      can paired to executable verification oracles that assess
a global objective f . Non-decomposability then manifests          both functional correctness and optimization quality.
even if each gk admits a well-defined notion of “locally opti-        While our arguments focus on quantum circuit opti-
mal” design, the composed objective f is not generally equal       mization, the underlying principles apply broadly: any do-
to a sum of independent per-module objectives over disjoint        main where (1) correctness is binary rather than approxi-
variable blocks, so independently maximizing (or minimiz-          mate, (2) valid solutions occupy an exponentially small sub-
ing) each gk does not guarantee optimality for f .                 space, and (3) formal verification methods exist, will benefit
    The same non-decomposability appears broadly: in drug          from verification-first AI architectures. Quantum computing
discovery, optimizing a single property (e.g., potency)            serves as an ideal testbed because mature verification tools
can worsen others (e.g., permeability, metabolic stability,        and well-defined correctness criteria (unitarity, gate equiva-
safety), motivating explicit multi-parameter optimization          lence) already exist.
scores that trade off multiple physicochemical attributes             More broadly, the data verification principles we demon-
rather than treating them independently (Wager et al. 2010).       strate: embedding domain constraints within objectives and
In combinatorial optimization, greedy heuristics that make         generation loops. Apply across scientific disciplines gov-
the best local choices can perform arbitrarily poorly on           erned by physical laws or mathematical axioms (not only
global objectives (e.g., for Traveling Salesperson Problem         the quantum area), from drug discovery’s biochemical plau-
(TSP) variants there are instances where greedy-type tour          sibility requirements to materials design’s thermodynamic
construction returns the worst tour), illustrating that “locally   stability constraints. Those different areas can build data
favorable” steps need not make up a globally good solution         verification with constraint specification and solution check-
(Gutin, Yeo, and Zverovich 2001). In engineering design,           ing would helps AI better understand the laws of the phys-
multidisciplinary systems couple aerodynamics, structures,         ical/real world, leveraging the formal methods each domain
controls, thermal behavior, etc., so improving one discipline      has developed over decades as foundations for reliable AI-
in isolation can degrade overall system performance or fea-        assisted discovery.
                        References                                Karpowicz, M.; et al. 2025. On the Fundamental Impossi-
Breuckmann, N. P.; and Eberhardt, J. N. 2021. Quan-               bility of Hallucination Control in Large Language Models.
tum low-density parity-check codes. PRX quantum, 2(4):            arXiv preprint arXiv:2506.06382.
040101.                                                           Karuppasamy, K.; Puram, V.; Johnson, S.; and Thomas, J. P.
                                                                  2025. A comprehensive review of quantum circuit optimiza-
Cai, W.; Ma, Y.; Wang, W.; Zou, C.-L.; and Sun, L. 2021.
                                                                  tion: Current trends and future directions. Quantum Rep.,
Bosonic quantum error correction codes in superconducting
                                                                  7(1): 2.
quantum circuits. Fundamental Research, 1(1): 50–67.
                                                                  Kreppel, F.; Melzer, C.; Wagner, J.; Hilder, J.; Poschinger,
Choi, J.; Shaw, A. L.; Madjarov, I. S.; Xie, X.; Finkel-          U.; Schmidt-Kaler, F.; and Brinkmann, A. 2024. Shuttling
stein, R.; Covey, J. P.; Cotler, J. S.; Mark, D. K.; Huang,       Compiler for a Trapped-Ion Quantum Computer Architec-
H.-Y.; Kale, A.; et al. 2023. Preparing random states and         ture with Junctions. In 2024 IEEE International Conference
benchmarking with many-body quantum chaos. Nature,                on Quantum Computing and Engineering (QCE), volume 1,
613(7944): 468–473.                                               1065–1076. IEEE.
Cuccaro, S. A.; Draper, T. G.; Kutin, S. A.; and Moulton,         Lu, B.-H.; Wang, P.; Chen, Z.-Y.; Liu, H.-Y.; Sun, T.-P.;
D. P. 2004. A new quantum ripple-carry addition circuit.          Duan, P.; Wu, Y.-C.; and Guo, G.-P. 2024. CAMEL: Physi-
Dupuis, N.; Buratti, L.; Vishwakarma, S.; Forrat, A. V.; Kre-     cally Inspired Crosstalk-Aware Mapping and Gate Schedul-
mer, D.; Faro, I.; Puri, R.; and Cruz-Benito, J. 2024. Qiskit     ing for Frequency-Tunable Quantum Chips. IEEE Transac-
code assistant: Training llms for generating quantum com-         tions on Computer-Aided Design of Integrated Circuits and
puting code. In 2024 IEEE LLM Aided Design Workshop               Systems.
(LAD), 1–4. IEEE.                                                 Martins, J. R. R. A.; and Lambe, A. B. 2013. Multidis-
Dziri, N.; Lu, X.; Sclar, M.; Li, X. L.; Jiang, L.; Lin, B. Y.;   ciplinary Design Optimization: A Survey of Architectures.
Welleck, S.; West, P.; Bhagavatula, C.; Le Bras, R.; et al.       AIAA Journal, 51(9): 2049–2075.
2023. Faith and fate: Limits of transformers on composition-      Masters, M. R.; Mahmoud, A. H.; and Lill, M. A. 2025.
ality. Advances in Neural Information Processing Systems,         Investigating whether deep learning models for co-folding
36: 70293–70332.                                                  learn the physics of protein-ligand interactions. Nature
Fawzi, A.; Balog, M.; Huang, A.; Hubert, T.; Romera-              Communications, 16(1): 8854.
Paredes, B.; Barekatain, M.; Novikov, A.; R. Ruiz, F. J.;         Moflic, I.; and Paler, A. 2025. Ultra-Large-Scale Compila-
Schrittwieser, J.; Swirszcz, G.; et al. 2022. Discovering         tion and Manipulation of Quantum Circuits with Pandora.
faster matrix multiplication algorithms with reinforcement        Novikov, A.; Vũ, N.; Eisenberger, M.; Dupont, E.; Huang,
learning. Nature, 610(7930): 47–53.                               P.-S.; Wagner, A. Z.; Shirobokov, S.; Kozlovskii, B.; Ruiz,
Ferguson, A.; LaFleur, M.; Ruthotto, L.; Thaler, J.; Ting, Y.-    F. J.; Mehrabian, A.; et al. 2025. AlphaEvolve: A coding
S.; Tiwary, P.; Villar, S.; Alves, E. P.; Avigad, J.; Billinge,   agent for scientific and algorithmic discovery. arXiv preprint
S.; et al. 2025. The Future of Artificial Intelligence and        arXiv:2506.13131.
the Mathematical and Physical Sciences (AI+ MPS). arXiv           Obenland, K.; Elenewski, J.; Morrell, K.; Rempfer, B.; Kuk-
preprint arXiv:2509.02661.                                        linski, P.; Neumann, R. S.; Kurlej, A.; Rood, R.; Blue, J.; and
                                                                  Belarge, J. 2025. pyLIQTR.
Gidney, C. 2018. Halving the cost of quantum addition.
Quantum, 2: 74.                                                   Perrier, E.; Youssry, A.; and Ferrie, C. 2022. QDataSet,
                                                                  quantum datasets for machine learning. Scientific data, 9(1):
Gidney, C. 2021. Stim: a fast stabilizer circuit simulator.       582.
Quantum, 5: 497.
                                                                  Ruiz, F. J. R.; et al. 2025. Quantum circuit optimization with
Gidney, C. 2025. How to factor 2048 bit RSA inte-                 AlphaTensor. In Nature Machine Intelligence.
gers with less than a million noisy qubits. arXiv preprint        Team, T. 2024. TQEC: Design automation software tools
arXiv:2505.15917.                                                 for Topological Quantum Error Correction.
Gidney, C.; and Ekerå, M. 2021. How to factor 2048 bit RSA       Wager, T. T.; Hou, X.; Verhoest, P. R.; and Villalobos, A.
integers in 8 hours using 20 million noisy qubits. Quantum,       2010. Moving beyond rules: the development of a central
5: 433.                                                           nervous system multiparameter optimization (CNS MPO)
Google. 2023. Suppressing quantum errors by scaling a sur-        approach to enable alignment of druglike properties. ACS
face code logical qubit. Nature, 614(7949): 676–681.              Chemical Neuroscience, 1(6): 435–449.
Gutin, G.; Yeo, A.; and Zverovich, A. 2001. Traveling Sales-      Wang, C.; He, S.; Luo, S.; Huan, Y.; and Wu, S. 2025. Inte-
man Should not be Greedy: Domination Analysis of Greedy-          grating physical units into high-performance AI-driven sci-
Type Heuristics for the TSP. BRICS Report Series RS-01-           entific computing. Nature Communications, 16(1): 3609.
6, BRICS, Department of Computer Science, University of           Yang, R.; Gu, Y.; Wang, Z.; Liang, Y.; and Li, T. 2024. QCir-
Aarhus.                                                           cuitNet: A Large-Scale Hierarchical Dataset for Quantum
Harrigan, M. P.; Khattar, T.; Yuan, C.; Peduri, A.; Yosri, N.;    Algorithm Design. arXiv preprint arXiv:2410.07961.
Malone, F. D.; Babbush, R.; and Rubin, N. C. 2024. Express-       ZapataAI. 2024. Bench-Q: A Framework for Quantum Al-
ing and Analyzing Quantum Algorithms with Qualtran.               gorithm Benchmarking.
                      Data Verification is the Future of Quantum Computing Copilots
                                           Supplementary Material

                  Prompt Template                             Option A                       ✓ Ground Truth
                                                              CNOT(1,0) ◦ CNOT(2,1) ◦ CNOT(1,2) ◦
All experiments reuse the same prompt, implemented verba-     Toffoli(1,0,2) ◦ CNOT(1,0) ◦ CNOT(3,2) ◦
tim inside the evaluation harness. Angle-bracket placehold-   CNOT(4,3) ◦ CNOT(3,4) ◦ Toffoli(3,2,4)
ers are filled with the MAJ/UMA sequences for each option     ◦ CNOT(3,2) ◦ CNOT(4,5) ◦ CNOT(3,4) ◦
before the request is sent to LLMs.                           Toffoli(3,2,4) ◦ CNOT(3,4) ◦ CNOT(4,2) ◦
                                                              CNOT(2,3) ◦ CNOT(1,2) ◦ Toffoli(1,0,2) ◦
                                                              CNOT(1,2) ◦ CNOT(2,0) ◦ CNOT(0,1)
   Multiple-choice Problem Prompt
                                                              Option B
   Select the best quantum circuit implementation with        X(0) ◦ CNOT(2,0) ◦ CNOT(2,1) ◦ CNOT(1,2)
   the LOWEST computational cost for an n-bit adder.          ◦ Toffoli(1,0,2) ◦ X(0) ◦ X(2) ◦ CNOT(4,2)
   Background: This circuit implements an n-bit               ◦ CNOT(4,3) ◦ CNOT(3,4) ◦ Toffoli(3,2,4)
   Quantum Ripple-Carry Adder. The architecture is            ◦ X(2) ◦ CNOT(4,5) ◦ Toffoli(3,2,4) ◦
                                                              CNOT(2,3) ◦ CNOT(4,2) ◦ SWAP(4,3) ◦
   constructed by cascading multiple instances of these
                                                              CNOT(4,3) ◦ CNOT(3,4) ◦ Toffoli(1,0,2)
   two primary modules:                                       ◦ CNOT(0,1) ◦ CNOT(2,0) ◦ SWAP(2,1) ◦
    • MAJ (Majority): A gate sequence used to prop-           CNOT(2,1) ◦ CNOT(1,2)
      agate the carry bit. In an n-bit adder, MAJ blocks      Option C
      are cascaded from the least significant bit to the      CNOT(1,2) ◦ CNOT(2,1) ◦ SWAP(2,1) ◦
      most significant bit.                                   CNOT(2,0) ◦ Toffoli(0,1,2) ◦ CNOT(3,4)
    • UMA (UnMajority and Add): The inverse op-               ◦ CNOT(4,3) ◦ SWAP(4,3) ◦ CNOT(4,2) ◦
      eration of MAJ, combined with an addition step.         Toffoli(2,3,4) ◦ CNOT(4,5) ◦ CNOT(3,2) ◦
      These are cascaded in reverse order to compute          CNOT(2,4) ◦ Toffoli(3,2,4) ◦ CNOT(4,3)
      the sum and uncompute the carry bits.                   ◦ CNOT(3,2) ◦ SWAP(4,2) ◦ CNOT(1,0) ◦
                                                              CNOT(0,2) ◦ Toffoli(1,0,2) ◦ CNOT(2,1) ◦
   Evaluation Criteria:                                       CNOT(1,0) ◦ SWAP(2,0)
    • SCORE = 0.5 × TOFFOLI COUNT + 0.25 ×                    Option D
      CIRCUIT DEPTH + 0.25 × TOTAL GATES                      CNOT(2,0) ◦ SWAP(2,1) ◦ CNOT(2,1) ◦
    • Lower SCORE means better performance.                   Toffoli(0,1,2) ◦ CNOT(1,2) ◦ CNOT(4,2) ◦
                                                              SWAP(4,3) ◦ CNOT(4,3) ◦ Toffoli(2,3,4)
   Options:
                                                              ◦ CNOT(3,4) ◦ CNOT(4,5) ◦ CNOT(2,3) ◦
   Option A:                                                  X(3) ◦ Toffoli(3,2,4) ◦ X(3) ◦ CNOT(4,3)
   <gate sequence A >                                         ◦ CNOT(4,2) ◦ CNOT(0,1) ◦ X(1) ◦
   Option B:                                                  Toffoli(1,0,2) ◦ X(1) ◦ CNOT(2,1) ◦
   <gate sequence B >                                         CNOT(2,0)
   Option C:
   <gate sequence C >                                         Observed Failure Modes
   Option D:                                                  • Format failure: Models output verbose explanations in-
   <gate sequence D >                                           stead of a single letter.
                                                              • Reasoning error: Models select valid but suboptimal cir-
   IMPORTANT: Output ONLY the letter (A, B, C, or
                                                                cuits.
   D). Your answer must be exactly one letter without
   punctuation.                                               • Refusal: Models decline to answer domain-specific ques-
   If uncertain, select the option that appears most op-        tions.
   timal.
   Your answer:                                                            Details and Visualizations
                                                              Algorithm 1 outlines the robust evaluation harness, includ-
                                                              ing the input sanitization and retry logic. This pseudocode
                                                              details the core logic used to test each LLMs for our early
          Example Evaluation Instance                         experiments, including the MAX RETRIES loop to handle
                                                              generation failures and the S ANITIZE procedure used to nor-
The following presents a representative evaluation instance
                                                              malize and validate the raw LLM outputs.
for inputs of size n = 2 bits. The correct answer is deter-
                                                                Reproducibility Details.
mined by computing the weighted score for each option.
                                                               • Models: All 34 models are publicly available through Ol-
Question Instance (2-bit Adder)                                  lama (https://ollama.ai).
  • Inference: Default Ollama parameters with max tokens             gle figure. The color gradient enables immediate pattern
    sufficient for single-letter responses.                          recognition—dark regions cluster around verification-
  • Dataset: 70,000 multiple-choice questions generated              aware models while lighter bands expose models stuck
    from 2M+ formally verified circuit designs.                      near random chance. This visualization is essential
  • Verification: Circuits verified using Lean 4 for func-           for identifying systematic trends (e.g., whether cer-
    tional correctness and Z3 for modular decomposition.             tain model families consistently outperform others) that
                                                                     would require extensive cross-referencing across dozens
  • Evaluation: Each question has exactly one correct an-            of separate plots.
    swer determined by the scoring function.
                                                                   • Bit-width-grouped bar charts (Figures 6–9): Enable
  • Hardware: Experiments conducted on Apple M3 with
                                                                     horizontal cross-model comparison at each fixed circuit
    512GB unified memory.
                                                                     complexity level. By sorting all 34 models by accuracy
   This section also presents supplementary visualizations to        at a specific bit-width, readers can directly answer ques-
illustrate the results of our early experiments further, show-       tions such as “Which models perform best on 8-qubit cir-
ing LLMs’ performance to support our positions in this po-           cuits?” or “How many models exceed the random base-
sition paper.                                                        line at 5 qubits?” The heatmap cannot answer these rank-
                                                                     ing questions as precisely, since color perception is less
Algorithm 1: Evaluation Agent Pseudocode                             accurate than bar length comparison.
 1: procedure E VALUATE H ARNESS(Q, model)                         • Model-grouped line charts (Figures 10–20): Enable
 2:    MAX RETRIES ← 3                                               longitudinal scaling analysis by tracking how each indi-
 3:    results ← {}          ▷ Initialize results dictionary         vidual model’s performance evolves as circuit complex-
 4:    for each question q ∈ Q do                                    ity increases. These plots reveal critical insights invisi-
 5:        prompt ← R ENDER P ROMPT(q)             ▷ Render          ble in aggregate views: some models maintain stable ac-
    prompt with MAJ/UMA sequences                                    curacy across bit-widths (indicating robust verification
 6:         answered ← false                                         knowledge), while others exhibit sharp degradation be-
 7:         for attempt ← 1 to MAX RETRIES do                        yond certain thresholds (suggesting brittle pattern match-
 8:             raw ← C ALLVLLM(model, prompt)                       ing). Such trajectory information is essential for predict-
 9:             answer ← S ANITIZE(raw)                              ing model behavior on larger, unseen circuits.
10:             if answer ∈ {’A’, ’B’, ’C’, ’D’} then              • Radar chart (Figure 4 in main text): Provides a com-
11:                 R ECORD C ORRECTNESS(results, q, answer)         pact aggregate summary by averaging each model’s ac-
12:                 answered ← true                                  curacy across all bit-widths. While detailed breakdowns
13:                 break                    ▷ Exit retry loop       are informative, practitioners often need a single metric
14:             else                                                 for quick model selection. The radar format visually sep-
15:                 L OG F ORMAT E RROR(q, attempt, raw)             arates verification-aware models (outer ring) from con-
16:             end if                                               ventional copilots (clustered inside the 25% baseline cir-
17:         end for                                                  cle), enabling rapid identification of top performers.
18:         if not answered then
                                                                     In summary, these visualizations operate at different gran-
19:             M ARK A S U NANSWERED(results, q)            ▷
                                                                  ularities: the heatmap shows everything at once but sacri-
    Counts as incorrect
                                                                  fices precision; bar charts enable precise ranking but only at
20:         end if
                                                                  one bit-width per figure; line charts reveal temporal dynam-
21:    end for
                                                                  ics but only for one model per subplot; and the radar chart
22:    return results
                                                                  sacrifices detail for immediate comparative insight. Each vi-
23: end procedure
                                                                  sualization answers questions that the others cannot, making
               ▷ Helper function for sanitizing vLLM output
                                                                  them collectively necessary rather than redundant.
24: procedure S ANITIZE(raw)
25:    clean ← T RIM W HITESPACE(raw)
26:    clean ← S TRIP P UNCTUATION(clean)               ▷ e.g.,
    quotes, brackets
27:    clean ← U PPERCASE(clean)
28:    return clean            ▷ Return first token if needed
29: end procedure

   Rationale for Multiple Visualization Dimensions. We
provide complementary visualization types that each serve a
distinct and irreplaceable analytical purpose. No single visu-
alization can capture all aspects of model behavior; together
they form a comprehensive evaluation framework:
 • Heatmap (Figure 5): Provides a global bird’s-eye view
    of all 34 models across all seven bit-widths in a sin-
                 gpt-oss_120b                              79.00%                                 76.50%                                 78.50%                         68.00%                        61.50%                                 69.50%                                69.00%
                 gemma3_12b                                76.50%                                 71.50%                                 75.00%                         70.00%                        60.00%                                 66.50%                                68.00%
                 gemma3_27b                                67.00%                                 68.00%                                 71.50%                         64.50%                        57.00%                                 65.00%                                61.50%
                   qwen3_1.7b                              71.00%                                 70.50%                                 66.50%                         66.50%                        51.50%                                 64.00%                                59.50%                                                      0.7
                   gpt-oss_20b                             72.00%                                 66.50%                                 69.50%                         64.00%                        52.00%                                 64.00%                                60.00%
                 llama3.3_70b                              60.50%                                 67.50%                                 64.00%                         61.50%                        47.50%                                 63.50%                                58.00%
                 qwen2.5_32b                               61.00%                                 63.00%                                 60.50%                         60.50%                        46.50%                                 61.50%                                54.50%
                 qwen2.5_14b                               56.50%                                 55.50%                                 63.50%                         63.00%                        50.00%                                 61.50%                                54.00%
                                                                                                                                                                                                                                                                                                                                               0.6
                 qwen2.5_72b                               59.00%                                 59.50%                                 54.00%                         53.50%                        42.00%                                 60.50%                                53.00%
                   qwen2.5_7b                              54.00%                                 53.50%                                 48.00%                         48.00%                        46.00%                                 55.50%                                51.50%
                       phi4_14b                            48.00%                                 48.50%                                 46.50%                         44.50%                        36.50%                                 53.00%                                45.50%
             granite4_small-h                              46.50%                                 44.50%                                 40.50%                         46.50%                        35.50%                                 43.00%                                46.50%
                                                                                                                                                                                                                                                                                                                                               0.5
                   qwen3_0.6b                              46.50%                                 41.00%                                 45.00%                         43.50%                        34.50%                                 52.50%                                39.00%
                mixtral_8x22b                              44.00%                                 38.00%                                 43.50%                         39.00%                        41.00%                                 50.50%                                42.00%
               granite4_micro                              36.00%                                 39.00%                                 40.50%                         35.00%                        33.50%                                 40.50%                                42.50%
                   gemma3_4b                               39.00%                                 41.50%                                 34.50%                         34.50%                        31.00%                                 48.50%                                36.50%




                                                                                                                                                                                                                                                                                                                                                    Accuracy
 Models




                   llama3.2_3b                             33.00%                                 28.50%                                 30.00%                         36.50%                        29.50%                                 33.00%                                32.00%                                                      0.4
               granite4_tiny-h                             33.50%                                 30.00%                                 33.50%                         30.50%                        33.00%                                 31.50%                                28.50%
             granite4_micro-h                              29.50%                                 33.50%                                 30.50%                         25.50%                        24.50%                                 31.00%                                30.00%
                   qwen2.5_3b                              30.50%                                 27.50%                                 28.50%                         24.00%                        24.00%                                 27.50%                                24.50%
                     mistral_7b                            26.00%                                 23.00%                                 25.50%                         21.00%                        30.00%                                 25.00%                                22.50%                                                      0.3
                 qwen2.5_1.5b                              19.00%                                 25.50%                                 25.00%                         26.50%                        22.50%                                 27.50%                                26.50%
               gemma3_270m                                 26.00%                                 23.00%                                 25.50%                         21.00%                        29.00%                                 25.00%                                22.50%
                 qwen2.5_0.5b                              17.00%                                 18.00%                                 23.00%                         22.50%                        24.00%                                 23.00%                                27.50%
                   llama3.2_1b                             19.50%                                 17.00%                                 22.00%                         22.50%                        22.50%                                 20.00%                                29.00%                                                      0.2
                   gemma3_1b                               15.00%                                 21.00%                                 22.50%                         24.00%                        25.00%                                 20.00%                                19.50%
               deepseek-r1_8b                               5.50%                                  7.50%                                  6.00%                          5.50%                         8.00%                                  6.50%                                 5.50%
             deepseek-r1_1.5b                               1.00%                                  1.50%                                  1.00%                          0.50%                         1.00%                                  0.50%                                 2.00%
                 mixtral_8x7b                               0.00%                                  1.50%                                  1.00%                          0.50%                         1.00%                                  1.00%                                 0.50%                                                      0.1
               deepseek-r1_7b                               1.50%                                  0.50%                                  1.00%                          0.50%                         0.50%                                  1.50%                                 0.00%
                 llama4_scout                               0.00%                                  0.00%                                  0.00%                          0.00%                         0.00%                                  0.00%                                 0.00%
                      qwen3_4b                              0.00%                                  0.00%                                  0.00%                          0.00%                         0.00%                                  0.00%                                 0.00%
                      qwen3_8b                              0.00%                                  0.00%                                  0.00%                          0.00%                         0.00%                                  0.00%                                 0.00%
                                                                                                                                                                                                                                                                                                                                               0.0
                                                               2                                      3                                      4                              5                             6                                      7                                     8
                                                                                                                                                                        Qubits

 Figure 5: Accuracy heatmap across 34 models and seven bit-widths. Dark cells highlight specific (quantum) verification knowl-
 edge LLMs, while lighter bands reveal general-purpose models stuck near random (25%).

           1.0                                                                                                                                                                          1.0
                                                                                                                                     Random Guess (25%)                                                                                                                                                           Random Guess (25%)
                   79%
           0.8        76%                                                                                                                                                               0.8     76%
                         72%71%                                                                                                                                                                    72%70%
                               67%                                                                                                                                                                       68%68%66%
                                  61%60%59%                                                                                                                                                                       63%
                                                                                                                                                                                                                     60%
           0.6                             56%                                                                                                                                          0.6                             56%54%
Accuracy




                                                                                                                                                                             Accuracy




                                              54%
                                                 48%46%46%                                                                                                                                                                    48%
                                                          44%                                                                                                                                                                    44%
                                                                                                                                                                                                                                    42%41%
                                                             39%                                                                                                                                                                          39%38%
           0.4                                                  36%
                                                                   34%33%
                                                                                                                                                                                        0.4                                                     34%
                                                                         30%30%                                                                                                                                                                    30%28%
                                                                               26%26%                                                                                                                                                                    28%26%
                                                                                                                                                                                                                                                               23%23%21%
                                                                                                                      20%19%                                                                                                                                            18%17%
           0.2                                                                                                              17%15%                                                      0.2
                                                                                                                                        6%                                                                                                                                                                          8%
                                                                                                                                             2% 1% 0% 0% 0% 0%                                                                                                                                                           2% 2% 0% 0% 0% 0%
           0.0                                                                                                                                                                          0.0
                   0b 2b 0b .7b 7b 2b 0b 2b 4b 7b 4b .6b l-h 2b 4b ro -h 3b 3b -h 7b 0m 1b .5b .5b 1b 8b 7b .5b 7b ut 4b 8b                                                                    0b 2b .7b 7b 0b 0b 2b 2b 4b 7b 4b l-h 4b .6b ro 2b -h -h 3b 3b .5b 0m 7b 1b .5b 1b 8b 7b .5b 7b ut 4b 8b
                _12 3_1 s_2 _1 3_2 5_3 3_7 5_7 5_1 .5_ 4_1 _0 al 8x2 a3_ mictiny .2_ .5_ icro al_ 27 .2_ _1 _0 a3_ r1_ r1_ _1 _8x scon3_ n3_                                                _12 3_1 _1 3_2 3_7 s_2 5_3 5_7 5_1 .5_ 4_1 al a3_ _0 mic8x2 icrotiny .2_ .5_ _1 27 al_ a3_ _0 .2_ r1_ _8x _1 r1_ scon3_ n3_
        t - osms mapt-ows enm3 mwaen2m. aw3.enw2.en2w. en2phwi ente34_stmral_emmite4_ite4l_amaw3 ene24_mmistmr a3la_mae3n2.e5n2.e5mmseeks-eekee-k-rix1traml a4_qweqwe                t -osms mawenm3 mama3p. t-wosenw2.enw2.en2w. en2phtei4_semmmweni3te4_trale_4_mite4l_amaw3 ene2n2.m5 a3m_ istermmen2l.a5mas3eekix-treael k-rs1eekm- a4_qweqwe
      gp ge g q ge q lla q q q                             q ni ix g an an l q nit em l qw qw g eep eep ps m lla                                                                   gp ge q ge lla g q q q q rani g qgranmixanitgran l q qwgem                                                  g qw l eep m ps eep lla
                                                          gra m gr gr                       gra         g                     d d dee                                                                                             g                   gr                                                d dee d
                                                                                      Models                                                                                                                                                                       Models

 Figure 6: Accuracy rankings for the 2- and 3-qubit MAJ/UMA prompts; both panels sort all 34 copilots and highlight the
 25% random-guess baseline, showing that verification-conditioned checkpoints (e.g., gpt-oss:120b, gemma3:12b/27b,
 qwen2.5:14b and larger) already sustain 0.6–0.8 accuracy while conventional Gemma, Llama, DeepSeek, and Mixtral vari-
 ants remain clustered around chance.
           1.0                                                                                                                                                                       1.0
                                                                                                                                       Random Guess (25%)                                                                                                                                                           Random Guess (25%)
                   78%
           0.8        75%                                                                                                                                                            0.8
                         72%70%                                                                                                                                                              70%68%
                               66%                                                                                                                                                                 66%64%
                                  64%64%                                                                                                                                                                 64%63%
                                        60%                                                                                                                                                                    62%60%
           0.6                                                                                                                                                                       0.6
Accuracy




                                                                                                                                                                          Accuracy
                                                       54%                                                                                                                                                                         54%
                                                          48%46%                                                                                                                                                                      48%46%
                                                                45%44%                                                                                                                                                                      44%44%
                                                                      40%40%                                                                                                                                                                      39%
           0.4                                                              34%34%                                                                                                   0.4                                                             36%35%34%
                                                                                  30%30%28%                                                                                                                                                                   30%
                                                                                           26%26%25%                                                                                                                                                             26%26%
                                                                                                    23%22%22%                                                                                                                                                          24%24%22%22%
                                                                                                                                                                                                                                                                                   21%21%
           0.2                                                                                                                                                                       0.2
                                                                                                                                          6%                                                                                                                                                                           6%
                                                                                                                                               1% 1% 1% 0% 0% 0%                                                                                                                                                            0% 0% 0% 0% 0% 0%
           0.0                                                                                                                                                                       0.0
                    0b 2b 7b 0b .7b 0b 4b 2b 2b 7b 4b .6b 2b ro l-h 4b -h -h 3b 3b 7b 0m .5b .5b 1b 1b 8b 7b .5b 7b ut 4b 8b                                                                 2b 0b .7b 7b 0b 4b 0b 2b 2b 7b l-h 4b .6b 2b 3b ro 4b -h .5b -h 3b 1b 1b .5b 0m 7b 8b 7b .5b 7b ut 4b 8b
                _12 3_1 3_2 s_2 _1 3_7 5_1 5_3 5_7 .5_ 4_1 _0 8x2 mic al a3_ tinyicro .2_ .5_ al_ 27 _1 _0 a3_ .2_ r1_ _8x _1 r1_ scon3_ n3_                                            3_1 _12 _1 3_2 s_2 5_1 3_7 5_3 5_7 .5_ al 4_1 _0 8x2 .2_ mica3_ tiny _1 icro .5_ a3_ .2_ _0 27 al_ r1_ _8x _1 r1_ scon3_ n3_
        t - osms mma mapt-ows enm3 aw3.enw2.enw2.en2w. en2phwi ent3ral_ite4t_e4_semmmite4e_4_mlamaw3 enm2 istmr a3e_n2.e5n2.e5mmlamas3eekix-treael k-rs1eekm- a4_qweqwe           m mpat-oqsswenm3 mgapt-wosen2m. aw3.enw2.enq2w. ente24_smpqhwi ent3rall_amnai3te4e_mmite4_en2e.54_qmwene2mmlamae3n2.m5 a3m_ istsreekix-treael k-rs1eeakm- a4_qweqwe
      gp ge ge g q lla q q q q                             qmix ranani g ran nit l q em qw qw g l eep m ps eep lla
                                                                g gr            g gra                  g                       d dee d                                          ge g          ge q lla q q rani                               mix lgra ggran qgrwanit                   g l qw em eep m ps eep ll
                                                                                                                                                                                                                                                                                                g         d dee d
                                                                                                                                                                                                                            g
                                                                                       Models                                                                                                                                                                       Models

 Figure 7: Accuracy rankings for the 4- and 5-qubit settings; verification-aware checkpoints stay above 0.6 despite deeper
 circuits, whereas large yet unverified copilots plateau near 0.5 on the shallower cases.


           1.0                                                                                                                                                                       1.0
                                                                                                                                       Random Guess (25%)                                                                                                                                                           Random Guess (25%)

           0.8                                                                                                                                                                       0.8
                                                                                                                                                                                             70%
                                                                                                                                                                                                66%65%
                                                                                                                                                                                                      64%64%64%
                   62%60%                                                                                                                                                                                      62%62%60%
           0.6           57%                                                                                                                                                         0.6                                56%
Accuracy




                                                                                                                                                                          Accuracy
                            52%52%50%                                                                                                                                                                                      53%52%
                                                                                                                                                                                                                                 50%48%
                                     48%46%46%
                                              42%41%                                                                                                                                                                                                           43%
                                                                                                                                                                                                                                                                  40%
           0.4                                      36%36%34%
                                                             34%33%
                                                                                                                                                                                     0.4
                                                                   31%30%30%29%                                                                                                                                                                                         33%32%31%
                                                                                                                                                                                                                                                                                 28%28%
                                                                               25%24%24%24%                                                                                                                                                                                            25%25%23%
                                                                                           22%22%
                                                                                                                                                                                                                                                                                                20%20%
           0.2                                                                                                                                                                       0.2
                                                                                                                                          8%                                                                                                                                                                           6%
                                                                                                                                               1% 1% 0% 0% 0% 0%                                                                                                                                                            2% 1% 0% 0% 0% 0%
           0.0                                                                                                                                                                       0.0
                                                                                                                                                               t                                                                                                                                                                         t
                  20b 12b 27b 20b .7b 14b 70b 32b _7b 72b 22b 14b ll-h .6bicro y-h _4b _7b _3b 0m _1b o-h _3b .5b _1b .5b _8b x7b .5b _7b ou _4b _8b                                        20b 12b 27b 20b .7b 70b 14b 32b 72b _7b 14b .6b 22b _4b ll-hicro _3b y-h o-h _3b .5b 0m _7b .5b _1b _1b _8b _7b x7b .5b ou _4b _8b
               s_1 3_ 3_ ss_ 3_1 .5_ .3_ .5_ 2.5 .5_ 8x i4_ ma 3_0 m tin a3 ral 3.2 _27 a3 icr 2.5 5_0 3.2 5_1 -r1 l_8 1_1 -r1 _sc n3 n3                                                 s_1 3_ 3_ ss_ 3_1 .3_ .5_ .5_ .5_ 2.5 i4_ 3_0 8x a3 ma m 3.2 tin icr 2.5 5_1 _27 ral 5_0 a3 3.2 -r1 -r1 l_8 1_1 _sc n3 n3
       p t -oesmmema mgapt-qowewn ena2maw3 enq2wewn enx2tral_ pihte4_qswenniten4_ite4g_emmmilsltamamag3emtme4_qmwewnen2ll.amwaenp2.seekixtreaek-prseelakma4qweqwe                p t -oesmmema mgapt-qoweanmaw3 enw2 enw2 enq2wen pqhwexntragl_emimte4_nsitel4la_mnaite4te_4_qmwewnen2.ma3miwsten2g.emlmlampaseepkseekixtreaekl-arma4qweqwe
      g g g                   q ll q            q mi ran gra gra                               gem grani        q          q dee meepsdee l                                     g g g                   ll q q q                     mi gran gra grgarani                      q gem q                 dee dee dmeep l
                                                                                                                                                                                                                                                                                                                         s
                                                          g                                                                         d
                                                                                       Models                                                                                                                                                                       Models

 Figure 8: Accuracy rankings for the 6- and 7-qubit benchmarks; verification-aware checkpoints remain above 50% while unver-
 ified copilots (e.g., llama3.3:70b, mixtral:8x22b) slide into the mid-30% range with most smaller models collapsing
 outright.


           1.0
                                                                                                                                       Random Guess (25%)

           0.8
                   69%68%
                            62%60%60%
           0.6                       58%
                                        55%54%53%
Accuracy




                                                 52%
                                                                46%46%
                                                                      42%42%
                                                                            39%
           0.4                                                                 36%
                                                                                  32%30%
                                                                                        29%28%28%
                                                                                                 26%24%
                                                                                                       22%22%
                                                                                                             20%
           0.2
                                                                                                                                          6%
                                                                                                                                               2% 0% 0% 0% 0% 0%
           0.0
                                                                                                                                     t
               20b 12b 27b 20b .7b 70b 32b 14b 72b _7b ll-h 14bicro 22b .6b _4b _3b o-h _1b y-h .5b .5b _3b 0m _7b _1b _8b .5b x7b ou _4b _8b _7b
            s_1 3_ 3_ ss_ 3_1 .3_ .5_ .5_ .5_ 2.5 ma i4_ m 8x 3_0 a3 3.2 icr 3.2 tin 5_0 5_1 2.5 _27 ral a3 -r1 1_1 l_8 _sc n3 n3 -r1
         -os ma ma t-o en a3 en2 en2 en2 en 4_s ph te4_ral_ en mm ma _mma te4_ n2. n2. en a3 ist mmeek k-r tra a4qweqweeek
      gpt gemgem gp qwllamqw qw qw qrawnite granmi ixt qw ge llaanite4 lglarani qweqwe qgwemm m gdeeepespsee mix llam deeps
                                         g                           gr                                      de
                                                                                       Models

 Figure 9: Accuracy ranking for the 8-qubit benchmark. Only a handful of data-verified copilots (notably gpt-oss:120b,
 gemma3:27b, qwen2.5:32b/72b) stay above 60%, whereas the majority of general-purpose checkpoints fall below 30%
 or flatline at zero, underscoring how qubit scaling amplifies the need for external verification.
            1.0                                                                   1.0                                                                   1.0
                                                  Random Guess (25%)                                                    Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                   0.8
 Accuracy




                                                                       Accuracy




                                                                                                                                             Accuracy
            0.6                                                                   0.6                                                                   0.6
                                                                                                                                                                                                   48%
                                                                                                                                                                    42%
            0.4                              29%
                                                                                  0.4                                                                   0.4 39%           34%    34%     31%
                                                                                                                                                                                                             36%
                  26%   23%   26%                      25%       22%                                22%    24%     25%
                                     21%                                                      21%                            20%       20%
            0.2                                                                   0.2 15%                                                               0.2
            0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                                Qubits                                                                Qubits

Figure 10: Performance of the gemma3:270m, gemma3:1b, and gemma3:4b checkpoints trained only with generic instruc-
tion data. All three curves hug the 25% random baseline—gemma3:4b briefly reaches ∼40% on 2–3 qubits before decaying
toward chance beyond six—showing that parameter count alone does not recover MAJ/UMA reasoning.
            1.0                                                                   1.0                                                                   1.0
                                                  Random Guess (25%)                                                    Random Guess (25%)                                                    Random Guess (25%)
            0.8 76%     72%   75%
                                     70%                                          0.8               72%                                                 0.8 72%           70%
                                                       66%       68%                    67%   68%          64%               65%                                    66%          64%               64%
                                             60%                                                                   57%                 62%                                                                   60%
 Accuracy




                                                                       Accuracy




                                                                                                                                             Accuracy
            0.6                                                                   0.6                                                                   0.6                              52%
            0.4                                                                   0.4                                                                   0.4
            0.2                                                                   0.2                                                                   0.2
            0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                                Qubits                                                                Qubits

Figure 11: Verification-conditioned gemma3:12b, gemma3:27b, and gpt-oss:20b. These checkpoints hold 0.60–0.75
accuracy through all qubit counts (with gpt-oss:20b dipping only to 0.52 at 8 qubits), illustrating the large jump gained
from verified data compared with Figure 10.
            1.0                                                                   1.0                                                                   1.0
                                                  Random Guess (25%)                                                    Random Guess (25%)                                                    Random Guess (25%)
            0.8 79%     76%   78%
                                                       70%       69%
                                                                                  0.8                                                                   0.8
                                     68%
                                             62%
 Accuracy




                                                                       Accuracy




                                                                                                                                             Accuracy
            0.6                                                                   0.6                                                                   0.6
                                                                                              39%   40%                      40%       42%
            0.4                                                                   0.4 36%                  35%     34%                                  0.4 30%     34%   30%                      31%       30%
                                                                                                                                                                                 26%     24%
            0.2                                                                   0.2                                                                   0.2
            0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                                Qubits                                                                Qubits

Figure 12: Comparison between gpt-oss:120b and the compact granite4 copilots. The 120B model stays between 0.62
and 0.79 accuracy even at 8 qubits, whereas granite4:micro and granite4:micro-h fluctuate in the 0.30–0.42 band
and erode with circuit depth, highlighting the gap between verification-first and distilled instruction-tuning.
            1.0                                                                   1.0                                                                   1.0
                                                  Random Guess (25%)                                                    Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                   0.8
 Accuracy




                                                                       Accuracy




                                                                                                                                             Accuracy




            0.6                                                                   0.6                                                                   0.6
                                                                                        46%   44%          46%               43%       46%
                                                                                                    40%
            0.4 34%           34%            33%       32%                        0.4                              36%                                  0.4
                        30%          30%                         28%                                                                                                                                         29%
                                                                                                                                                              20%         22%    22%     22%       20%
            0.2                                                                   0.2                                                                   0.2         17%

            0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                                Qubits                                                                Qubits

Figure 13: Effect of lighter granite4 releases versus a 1B Llama. granite4:tiny-h and granite4:small-h hover
in the low 30–40% range without scaling benefits, and llama3.2:1b drops from 0.29 to ≈0.20 as qubit counts grow, rein-
forcing that lightweight copilots need explicit verification signals.
            1.0                                                                   1.0                                                                   1.0
                                                  Random Guess (25%)                                                    Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                   0.8
                                                                                              68%   64%                      64%
                                                                                        60%                62%                         58%
 Accuracy




                                                                       Accuracy




                                                                                                                                             Accuracy




            0.6                                                                   0.6                                                                   0.6
                                                                                                                   48%
            0.4 33%                  36%               33%       32%              0.4                                                                   0.4
                        28%   30%            30%
            0.2                                                                   0.2                                                                   0.2
                                                                                                                                                              0%    0%    0%     0%      0%         0%       0%
            0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                                Qubits                                                                Qubits

Figure 14: Llama family scaling. llama3.2:3b remains near 0.30 accuracy across qubits, llama3.3:70b peaks at 0.64–
0.68 on 2–5 qubits before tapering to 0.48 by 8 qubits, and the distilled llama4:scout agent fails to answer any instance
correctly, underscoring inconsistent gains from size alone.
            1.0                                                                   1.0                                                                  1.0
                                                  Random Guess (25%)                                                   Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                  0.8
 Accuracy




                                                                       Accuracy




                                                                                                                                            Accuracy
            0.6                                                                   0.6                                                                  0.6                                        50%
                                                                                                                                                             44%         44%            41%                 42%
                                                                                                                                                                   38%          39%
            0.4                              30%                                  0.4                                                                  0.4
                  26%   23%   26%                      25%       22%
                                     21%
            0.2                                                                   0.2                                                                  0.2
                                                                                        0%   2%    1%     0%      1%         1%       0%
            0.0 2        3     4      5       6          7        8               0.0 2       3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                               Qubits                                                                Qubits

Figure 15: Mistral and Mixtral checkpoints. The dense mistral:7b oscillates around 0.25 accuracy, the sparse
mixtral:8x7b sits at ≤2% on every qubit count, and mixtral:8x22b briefly reaches 0.44–0.50 before sliding back
toward the high-30% range, showing that mixture-of-experts routing without verification does not guarantee reliability.
            1.0                                                                   1.0                                                                  1.0
                                                  Random Guess (25%)                                                   Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                  0.8
 Accuracy




                                                                       Accuracy




                                                                                                                                            Accuracy
            0.6                                        53%                        0.6                                                                  0.6
                  48%   48%   46%    44%                         46%
            0.4                              36%                                  0.4                                                                  0.4
                                                                                                   23%            24%       23%       28%                          26%   25%    26%               28%       26%
                                                                                                          22%                                                                           22%
            0.2                                                                   0.2 17%    18%                                                       0.2 19%
            0.0 2        3     4      5       6          7        8               0.0 2       3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                               Qubits                                                                Qubits

Figure 16: Mid-sized phi4 and entry-level qwen2.5. phi4:14b sustains mid-40% accuracy with a single spike above 50%,
whereas the 0.5B and 1.5B qwen2.5 models fluctuate between 0.18 and 0.28 accuracy, barely clearing the random-guess
threshold.
            1.0                                                                   1.0                                                                  1.0
                                                  Random Guess (25%)                                                   Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                  0.8
                                                                                                                                                                         64%    63%               62%
 Accuracy




                                                                       Accuracy




                                                                                                                                            Accuracy
            0.6                                                                   0.6 54%    54%                            56%       52%              0.6 56%     56%
                                                                                                                                                                                        50%                 54%
                                                                                                   48%    48%     46%
            0.4 30%                                                               0.4                                                                  0.4
                        28%   28%    24%     24%       28%       24%
            0.2                                                                   0.2                                                                  0.2
            0.0 2        3     4      5       6          7        8               0.0 2       3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                               Qubits                                                                Qubits

Figure 17: Scaling within qwen2.5. Moving from 3B to 7B to 14B steadily lifts accuracy from ≈0.25 to 0.45–0.56 and
finally 0.50–0.64, demonstrating that successive parameter doublings under the same training recipe yield material gains on
MAJ/UMA verification.
            1.0                                                                   1.0                                                                  1.0
                                                  Random Guess (25%)                                                   Random Guess (25%)                                                    Random Guess (25%)
            0.8                                                                   0.8                                                                  0.8
                  61%   63%   60%    60%               62%                                   60%                            60%
                                                                                  0.6 59%
 Accuracy




                                                                       Accuracy




                                                                                                                                            Accuracy




            0.6                                                  55%                               54%    54%                         53%              0.6                                        52%
                                             46%                                                                  42%                                        46%         45%    44%
                                                                                                                                                                   41%                                      39%
            0.4                                                                   0.4                                                                  0.4                              34%

            0.2                                                                   0.2                                                                  0.2
            0.0 2        3     4      5       6          7        8               0.0 2       3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                               Qubits                                                                Qubits

Figure 18: Large qwen2.5 checkpoints versus the compact qwen3:0.6b. The 32B and 72B models remain above 0.53
accuracy even at 8 qubits, while the 0.6B baseline tops out near 0.52 on easy settings and falls to 0.34 on 8 qubits, emphasizing
the benefit of pairing scale with verification-aware data.
            1.0                                                                   1.0                                                                  1.0
                                                  Random Guess (25%)                                                   Random Guess (25%)                                                    Random Guess (25%)
            0.8 71%     70%                                                       0.8                                                                  0.8
                              66%    66%               64%       60%
 Accuracy




                                                                       Accuracy




                                                                                                                                            Accuracy




            0.6                              52%                                  0.6                                                                  0.6
            0.4                                                                   0.4                                                                  0.4
            0.2                                                                   0.2                                                                  0.2
                                                                                        0%   0%    0%     0%      0%         0%       0%                     0%    0%    0%     0%      0%         0%       0%
            0.0 2        3     4      5       6          7        8               0.0 2       3     4      5       6          7        8               0.0 2        3     4      5       6          7        8
                                    Qubits                                                               Qubits                                                                Qubits

Figure 19: qwen3 family. The 1.7B reasoning model maintains 0.52–0.71 accuracy across qubit counts, yet the larger 4B
and 8B general-purpose releases answer zero questions correctly, highlighting how differing alignment objectives can erase
MAJ/UMA skill despite added capacity.
            1.0                                                                1.0                                                                1.0
                                               Random Guess (25%)                                                 Random Guess (25%)                                                 Random Guess (25%)
            0.8                                                                0.8                                                                0.8
 Accuracy




                                                                    Accuracy




                                                                                                                                       Accuracy
            0.6                                                                0.6                                                                0.6
            0.4                                                                0.4                                                                0.4
            0.2                                                                0.2                                                                0.2
                                                                                                                                                        6%   8%   6%    6%      8%         6%       6%
                  1%   2%   1%    0%      1%         0%       2%                     2%   0%   1%    0%      0%         2%       0%
            0.0 2      3    4      5      6           7        8               0.0 2      3    4      5      6           7        8               0.0 2      3    4      5      6           7        8
                                 Qubits                                                             Qubits                                                             Qubits

Figure 20: deepseek-r1 models. Neither the 1.5B nor 7B variants exceeds 2% accuracy, and even the newer 8B release
plateaus at 6–8%, confirming that exhaustive chain-of-thought generation alone does not translate into verifiable MAJ/UMA
answers.
