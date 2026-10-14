                                           Proceedings of Machine Learning Research vol:1–32, 2026 Learning for Dynamics & Control Conference (L4DC) 2026




                                            From Natural Language to Certified H-infinity Controllers:
                                               Integrating LLM Agents with LMI-Based Synthesis

                                           Shihao Li                                                                  shihaoli01301@utexas.edu
                                           Jiachen Li                                                                       jiachenli@utexas.edu
                                           Jiamin Xu                                                                        jiaminxu@utexas.edu
                                           Dongmei Chen                                                                    dmchen@me.utexas.edu
arXiv:2511.07894v1 [eess.SY] 11 Nov 2025




                                           Department of Mechanical Engineering, University of Texas at Austin




                                                                                           Abstract
                                                We present S2C (Specification-to-Certified-Controller), a multi-agent framework that maps
                                                natural-language requirements to certified H∞ state-feedback controllers via LMI synthesis.
                                                S2C coordinates five roles—SpecInt (spec extraction), Solv (bounded-real lemma (BRL)
                                                LMI), Tester (Monte Carlo and frequency-domain checks), Adapt (spec refinement), and
                                                CodeGen (deployable code). The loop is stabilized by a severity- and iteration-aware γ-floor
                                                guardrail and a decay-rate region constraint enforcing ℜλ(A+BK) < −α with α = 3.9/Ts
                                                derived from settling-time targets. For state feedback, verification reports disturbance re-
                                                jection C (sI − (A+BK))−1 E ∞ alongside time-domain statistics; discrete benchmarks
                                                are converted to continuous time via a Tustin (bilinear) transform when needed. On 14
                                                COMPleib problems, S2C attains 100% synthesis success and 100% convergence within
                                                six iterations, with strong decay-rate satisfaction and near-target certified H∞ levels; it
                                                improves robustness metrics relative to single-shot BRL and BRL+α baselines. An ab-
                                                lation over LLM backbones (GPT-5, GPT-5 mini, DeepSeek-V3, Qwen-2.5-72B, Llama-4
                                                Maverick) shows the pipeline is robust across models, while stronger models yield the high-
                                                est effectiveness. These results indicate that LLM agents can integrate certificate-bearing
                                                control synthesis from high-level intent, enabling rapid end-to-end prototyping without
                                                sacrificing formal guarantees.
                                                Keywords: LLM agents; robust control; H∞ synthesis; convex optimization; specification
                                                mining; automated design; formal guarantees


                                           1. Introduction
                                           Traditional control system design bridges two worlds: natural language specifications from
                                           users (”the system should respond quickly without overshooting”) and mathematical imple-
                                           mentations that satisfy these requirements with provable guaranties Kopetz et al. (1991);
                                           Sifakis (2015). This translation process requires expertise in both interpreting vague re-
                                           quirements and selecting appropriate synthesis methods—a combination that has resisted
                                           automation despite decades of research in computer-aided control design Sarma (1989);
                                           Bissell (2009); Boyd and Barratt (1991).
                                               The recent emergence of capable language models presents a new opportunity Zhao
                                           et al. (2023); Huang and Chang (2022); Jiang et al. (2024); Nijkamp et al. (2022); Nguyen
                                           and Nadi (2022); Xia et al. (2024); OpenAI (2023). These models demonstrate strong
                                           natural language understanding and can generate structured code, suggesting potential for

                                           © 2026 S. Li, J. Li, J. Xu & D. Chen.
                                      Li Li Xu Chen




automating the specification-to-implementation pipeline. However, control design poses
unique challenges beyond code generation: requirements are often ambiguous, multiple
design approaches may apply to the same problem, and correctness cannot be verified
through unit tests alone—formal mathematical properties like stability and robustness must
be certified Jin and Lavaei (2020); Huang et al. (2020); Loveland (2016).
    Existing automated control design tools fall into two categories. Classical computer-
aided design packages Lofberg (2004); Boyd and Vandenberghe (2004) provide powerful
synthesis algorithms but require users to formulate optimization problems with precise
mathematical specifications Denham (2005). Recent LLM-based approaches Guo et al.
(2024); Narimani and Emami (2025) can interpret natural language and iteratively adjust
controller parameters, but they treat synthesis tools as black boxes and lack mechanisms to
maintain formal guaranties throughout the design process Zhao et al. (2022); Doerr and Do-
err (2019). Neither approach achieves end-to-end automation from informal specifications
to certified implementations.
    We present S2C (Specification-to-Certified-Controller), a framework that automates for-
mal control synthesis through multi-agent LLM integration. The key insight is that different
aspects of the design process—parsing specifications, formulating optimization problems,
verifying solutions, and generating code—require different types of reasoning that can be
handled by specialized agents working collaboratively. Rather than using a single LLM to
perform all tasks or treating synthesis methods as opaque solvers, S2C agents construct
mathematical optimization problems, invoke formal synthesis tools with full transparency,
and validate results against rigorous criteria.




                          Figure 1: S2C multi-agent architecture.

    The general framework shown in Figure 1 employs five specialized agents: SpecIntA-
gent interprets natural language requirements and translates them into formal performance
specifications. SolvAgent formulates these specifications as convex optimization problems
and generates solver code. TesterAgent validates candidate designs through both simula-
tion and formal certificate checking. AdaptAgent analyzes failures and revises specifications
when requirements cannot be met. CodeGen produces implementation code with embedded
performance certificates. These agents share a structured memory containing design his-

                                             2
                          LLM Agents for H-infinity Control




tory and communicate through targeted feedback messages, enabling iterative refinement
without human intervention.
    We focus on robust state feedback synthesis as a concrete demonstration. When users
specify requirements like ”reject disturbances effectively” or ”limit actuator usage,” S2C
must map these phrases to mathematical objectives, select appropriate synthesis meth-
ods, formulate optimization problems, and verify that solutions satisfy all constraints. The
framework handles this by having agents reason about the relationship between informal re-
quirements and formal specifications, construct optimization problems using domain-specific
knowledge, and validate results against multiple criteria.
    Our main contributions are:
    Formal Synthesis Automation: We demonstrate that LLM agents can integrate
convex optimization-based synthesis methods while maintaining mathematical rigor. Unlike
parameter tuning approaches, agents formulate LMI optimization problems from scratch,
interface with numerical solvers, and validate formal guarantees throughout the process.
    Multi-Agent Architecture for Design Workflows: We develop a structured ap-
proach to decomposing control design into specialized agent roles with explicit memory and
feedback mechanisms. This architecture enables agents to handle the complexity of map-
ping between informal requirements, formal specifications, optimization formulations, and
verified implementations.
    Validation on Benchmark Tasks: We evaluate S2C on 14 problems from the COM-
Pleib benchmark library Leibfritz (2006), spanning academic test cases, aircraft, helicopter,
reactor, and decentralized control systems. The framework achieves 100% synthesis suc-
cess (all problems stabilized) within 6 iterations, producing controllers with certified H∞
bounds, enforced decay-rate constraints for settling time, and verified robustness margins.
To ensure reproducibility, we provide deterministic heuristic fallbacks for all LLM-driven
decision points.
    The framework is implemented in Python with interfaces to standard control toolboxes
and optimization solvers. We release the complete implementation to support future re-
search in LLM-based formal synthesis automation.
    The remainder of this paper is organized as follows: Section 2 reviews background on
robust control synthesis and multi-agent systems. Section 3 formalizes the automated syn-
thesis problem. Section 4 describes the S2C framework architecture and agent designs.
Section 5 presents experimental validation. Section 6 discusses limitations and future di-
rections.

2. Background and Related Work
2.1. Formal Control Synthesis
Modern control system design relies on optimization-based synthesis methods that provide
formal performance guarantees. Linear Matrix Inequality (LMI) approaches enable sys-
tematic synthesis for robust control problems, including H∞ , H2 , and mixed-sensitivity
design Boyd et al. (1993); Gahinet (1996). Convex optimization tools like CVX Boyd
and Vandenberghe (2004) and solvers such as MOSEK ApS (2019) and SDPT3 Toh et al.
(1999) have made these methods computationally tractable. Despite these advances, for-
mulating LMI problems from user specifications remains an expert-driven manual process.

                                             3
                                        Li Li Xu Chen




Engineers must translate informal requirements into mathematical objectives, select ap-
propriate synthesis methods, construct optimization problems with proper constraints, and
verify solutions—steps that require deep knowledge of both control theory and numerical
optimization. Existing computer-aided design tools automate the solver stage but assume
users can already formulate correct problems Gu et al. (2005).

2.2. LLM Agents for Engineering Design
The potential of LLMs for engineering automation has been explored across multiple do-
mains Ren et al. (2025). In control engineering, recent benchmarks evaluate LLM knowledge
of textbook-level concepts Kevian et al. (2024); Zahedifar et al. (2025), while ControlAgent
Guo et al. (2024) demonstrated end-to-end automation of classical control design through
iterative parameter tuning for PID controllers and loop shaping. Beyond controls, Analog-
Coder Lai et al. (2025) addresses analog circuit design, SPICED Chaudhuri et al. (2025)
detects bugs in circuit netlists, and AmpAgent Liu et al. (2024) automates amplifier design.
However, these systems focus on parameter adjustment or design verification rather than
formulating and solving optimization problems. A key limitation is that LLM agents typ-
ically treat synthesis tools as black boxes—they can call solvers with pre-defined problem
structures but cannot construct novel optimization formulations from informal specifications
while maintaining formal guarantees throughout the design process Nti et al. (2022).

2.3. Multi-Agent LLM Systems
Multi-agent architectures have emerged as a powerful paradigm for complex task automa-
tion, enabling specialized agents to collaborate on problems requiring diverse expertise Li
et al. (2024). General frameworks like AutoGen Wu et al. (2024) and MetaGPT Hong et al.
(2023) provide infrastructure for agent coordination across domains including code genera-
tion, question answering, and mathematical reasoning Qian et al. (2023); Chen et al. (2023).
These systems demonstrate that decomposing complex workflows into specialized agent
roles improves both reliability and interpretability. However, applying multi-agent systems
to formal engineering design introduces unique challenges: agents must not only coordinate
workflows but also maintain mathematical rigor, interface with domain-specific tools, and
validate formal properties. S2C addresses these challenges by designing specialized agents
that construct optimization problems, maintain formal certificates, and iteratively refine
designs through structured feedback—going beyond general-purpose coordination to enable
reliable automation of formal synthesis methods Sunehag et al. (2017); Li et al. (2022).


3. Problem Formulation
Consider a continuous-time LTI plant ẋ = Ax + Bu + Ew, z = Cz x + Dz u where x ∈ Rnx ,
u ∈ Rnu , w ∈ Rnw , and z ∈ Rnz is the regulated output. We seek static state-feedback u = Kx
achieving closed-loop stability and robust disturbance rejection.
    SpecIntAgent extracts specifications S = {γtarget , γmin , Ts,target , Ms,target }: target H∞
level γtarget for Tzw , transient guardrail γmin , settling time Ts,target (2% criterion), and
optional Ms,target = ∥S∥∞ for output-feedback. State-feedback uses disturbance-rejection
norm instead.

                                               4
                           LLM Agents for H-infinity Control




   We minimize the induced L2 gain subject to stability and decay-rate constraints. The
bounded-real lemma with Y = KP yields

                            minimize     γ
                            P ≻0, Y, γ

                           subject to    Ψ(P, Y, γ) ≺ 0,                                     (1)
                                         sym(AP + BY ) + 2αP ≺ 0,
                                         γmin ≤ γ ≤ γtarget ,

where
                                                         (Cz P + Dz Y )⊤
                                                                        
                                sym(AP + BY ) E
                  Ψ(P, Y, γ) =       E⊤        −γI             0        ,
                                  Cz P + D z Y    0            −γI                           (2)
                                                  3.9
                   sym(X) = X + X ⊤ ,        α=           .
                                                Ts,target

    Feasibility of Ψ ≺ 0 certifies ∥Tzw ∥∞ < γ and yields K = Y P −1 . TesterAgent verifies
via Monte Carlo (settling time, overshoot) and frequency analysis: output-feedback reports
Ms , Mt , GM, P M ; state-feedback evaluates ∥Cz (sI − (A + BK))−1 E∥∞ . Violations trigger
AdaptAgent to adjust S (relaxing γtarget , raising γmin , etc.) before re-solving (1). Overshoot
is measured but not enforced.


4. S2C Framework
The S2C (Specification-to-Certified-Controller) framework employs five specialized LLM
agents in an iterative synthesis-verification-adaptation loop (Figure 2): SpecIntAgent parses
natural-language requirements into numeric specifications S; SolvAgent solves the H∞ LMI
(1) with decay-rate constraints; TesterAgent validates controllers via Monte Carlo simula-
tion and frequency analysis; AdaptAgent refines S based on violations using an LLM and
severity-aware guardrails; and CodeGen produces deployable Python code. Implementation
details and full agent prompts are provided in Appendix A.


4.1. SpecIntAgent
Parses natural-language requirements (e.g., “settling time under 3s with strong disturbance
rejection”) into structured specifications S = {γtarget , γmin , Ts,target , Ms,target } via LLM-
generated JSON. Deterministic fallbacks apply when parsing fails. Specifications are vali-
dated before synthesis.


4.2. SolvAgent
Solves the H∞ LMI (1) with decay-rate constraint α = 3.9/Ts,target to enforce settling time.
Uses MOSEK (SCS fallback) to recover K = Y P −1 and verifies closed-loop stability via
eigenvalue checks. On infeasibility, returns failure to trigger AdaptAgent relaxation.

                                                5
                                      Li Li Xu Chen




                          Figure 2: S2C multi-agent architecture.


4.3. TesterAgent

Validates synthesized controllers via: (i) Monte Carlo simulation (N = 50 unit-sphere initial
conditions, 20s horizon, 2% settling criterion) measuring settling time and overshoot; (ii)
frequency-domain analysis computing disturbance rejection ∥Cz (sI − (A + BK))−1 E∥∞ for
state-feedback or classical margins (Ms , Mt , GM, P M ) for output-feedback. Violations are
classified by severity (low/medium/high) and reported to AdaptAgent.



4.4. AdaptAgent

Refines specifications based on violations using an LLM to generate JSON updates to S.
When transient violations (settling time, overshoot) occur, automatically raises a gamma-
floor guardrail γmin based on violation severity and iteration count to prevent excessive γ
optimization that degrades time-domain performance. Heuristic fallbacks apply on LLM
failure. Formula details in Appendix D.

                                             6
                          LLM Agents for H-infinity Control




4.5. CodeGen
Generates deployable Python code (HInfController class implementing u = Kx) with the
synthesized gain matrix K and formal performance certificates.

4.6. Gamma-Floor Guardrails
To prevent excessive γ minimization from degrading transient response, S2C employs a
gamma-floor mechanism that raises γmin when settling-time or overshoot violations occur.
The floor update combines severity-based thresholds and iteration history:
                                                                                
           γmin ← min 0.9 γtarget , max γmin , γbase (severity), γhist (γlast , i) ,

ensuring monotonic increases capped below 0.9 γtarget for feasibility. Full formulas in Ap-
pendix D.

4.7. Iterative Loop
S2C iterates up to Nmax = 10 times. Each iteration: (i) SolvAgent solves (1) with decay rate
α = 3.9/Ts,target and current γmin ; (ii) TesterAgent runs Monte Carlo simulation (N = 50
trials, 20s horizon) and frequency analysis; (iii) if violations V = ∅, CodeGen emits Python
code and exits; (iv) otherwise, AdaptAgent updates S via LLM and raises γmin per §4.6. A
memory buffer retains the last 20 designs. Full pseudocode in Appendix D.

5. Experiment
We evaluate S2C on 14 COMPleib benchmarks (Leibfritz, 2006) varying in dimension (nx ∈
[2, 4], nu ∈ [1, 2]), time domain (10 continuous, 4 discrete), and stability (12 stable, 2
unstable). Discrete systems (NN2, AC5, NN8, DIS5) undergo Tustin conversion (Ts = 1.0)
before synthesis. SpecIntAgent/AdaptAgent use GPT-5 (temperature 0.0; ablations: GPT-5
mini, DeepSeek-V3, Qwen-2.5-72B, Llama-4 Maverick). SolvAgent uses MOSEK with SCS
fallback (tolerance 10−8 ). Parameters: α = 3.9/Ts,target , Nmax = 10 iterations, Monte Carlo
N = 50 trials (20s, 2% settling). Full details are summarized in Appendix F.
Baselines. All use identical D2C, seeds, and stability criterion maxi ℜλi (A+BK) < 0.
BRL: single-shot γ minimization. BRL+α: adds decay constraint α = 3.9/Ts,target . S2C
(no floor): iterative with α, no guardrail. S2C (full): our method with α and γ-floor.
LQR–H2 : CARE with Q = Cz⊤ Cz , R = I. PID: SISO ITAE tuning.

5.1. Metrics
We report five aggregate metrics aligned with Fig. (a–e). All values are medians across the
14 problems; decimals in percentages reflect the 1/14 resolution where applicable.

Success rate (%) Fraction of benchmarks for which a stabilizing controller is synthesized;
  stability requires maxi ℜλi (A+BK) < 0.

Converged within 6 iterations (%) Fraction that satisfies all enforced specifications by
  iteration k ≤ 6.

                                             7
                                      Li Li Xu Chen




Disturbance rejection (state feedback, lower is better)
                                                      −1
                          ∥Hcl ∥∞ =     Cz sI − (A+BK) E          ∞
                                                                      ,                   (3)

  reported as the median across problems; bar charts show percentages normalized to the
  BRL baseline.

Normalized certified level (lower is better) Median γ/γtarget (in %), where γ is the
  certified H∞ bound returned by synthesis.

Decay-rate satisfaction (higher is better)

                              − max ℜλ(A+BK)                                3.9
                DecaySat =                   × 100%,            α =                   .   (4)
                                     α                                    Ts,target

    For state feedback we emphasize disturbance rejection (3), since loop-shaping sensitivity
metrics (Ms , Mt ) are not defined when K acts on the full state. If output-feedback con-
trollers are considered, we report Ms = ∥S∥∞ , Mt = ∥T ∥∞ , and classical margins computed
from L(s) = G(s)K(s).

5.2. Results
We evaluate six synthesis settings on 14 COMPleib plants using real LLM runs: BRL,
BRL+α, S2C (no floor), S2C (full), LQR–H2 , and PID loop shaping. Aggregated outcomes
are summarized in Fig. 3(a–e).
    Synthesis and convergence. S2C (full) achieves a 100% synthesis rate, compared
with 86% for S2C (no floor), 71% for BRL+α, 57% for BRL, 64% for LQR–H2 , and 50%
for PID (Fig. a). Convergence within six iterations is 100% for S2C (full), 92.9% for S2C (no
floor), 71.0% for BRL+α, 57.1% for LQR–H2 , 50.0% for BRL, and 35.7% for PID (Fig. e).
Fractional values arise from a 14-problem set (increments of 1/14 ≈ 7.1%).
    Robustness and γ certificates. Median disturbance rejection ∥Hcl ∥∞ (lower is better;
reported as a percentage of BRL) is 89.7% for S2C (no floor) and 92.5% for S2C (full),
improving upon BRL+α (96.8%) and BRL (100.0%), while LQR–H2 and PID are larger
(135.2%, 162.4%) (Fig. b). Median certified γ relative to the requested target is 88.0% for
S2C (no floor), 90.0% for S2C (full), 93.0% for BRL+α, and 96.0% for BRL; LQR–H2 and
PID trail at 130.0% and 160.0% (Fig. c).
    Decay-rate satisfaction. Using the normalized margin − max ℜλ(A+BK)/α (higher
is better), S2C (full) reaches 120.0% of the specified decay rate, S2C (no floor) 110.0%,
and BRL+α 105.0%. BRL (70.0%), LQR–H2 (80.0%), and PID (60.0%) lag (Fig. d),
highlighting the benefit of explicit decay constraints and the γ-floor mechanism.
    Summary. S2C (full) provides the most reliable synthesis (100%) and fastest conver-
gence (100% within six iterations) with strong decay-rate satisfaction. The S2C (no floor)
ablation yields tighter γ and disturbance rejection, reflecting a predictable trade-off when
guardrails are removed. BRL+α improves over single-shot BRL. Classical LQR/PID base-
lines underperform on H∞ -oriented metrics. Discrete-time plants are mapped to continuous
time via a Tustin transform prior to synthesis; all panels report medians across problems.

                                             8
                          LLM Agents for H-infinity Control




Figure 3: Aggregated experimental results across 14 COMPleib problems. Panels (a–e)
          report synthesis success, disturbance rejection, normalized certified γ, decay-rate
          satisfaction, and convergence within 6 iterations.



5.3. Ablation Study
We ablate the LLM used by SpecIntAgent and AdaptAgent while keeping all other com-
ponents, prompts, seeds, solver settings, and step budgets fixed. Models evaluated: GPT-
5 (baseline), GPT-5 mini, DeepSeek-V3, Qwen-2.5-72B-Instruct (served via vLLM), and
Llama-4 Maverick (via Together AI). Figure 4 reports five metrics: success rate, con-
vergence within 6 iterations, disturbance rejection ∥Hcl ∥∞ (lower is better; normalized
to BRL), normalized certified level γ/γtarget (lower is better), and decay-rate satisfaction
− max ℜλ(A+BK)/α (higher is better).
    Observations. GPT-5 attains the highest effectiveness, with 100% success and 100%
converged within ≤ 6 iterations, and strong certificates (low γ/γtarget , high decay-rate
satisfaction). GPT-5 mini is close on both success and convergence and shows only a
modest drop on robustness/certification metrics. DeepSeek-V3 and Qwen-2.5-72B remain
competitive (mid–high 80s for success; solid but weaker certificates). Llama-4 Maverick
trails on success and convergence and shows milder decay-rate satisfaction, but still reaches
feasible designs on most problems. Across models, disturbance rejection and normalized γ
degrade, indicating that the pipeline is robust to LLM quality and that the deterministic
synthesis/verification stages absorb variability. All values are medians across 14 problems.
    Efficiency. A complementary table with API usage (calls/tokens), median per-iteration
latency, and estimated cost is included in the appendix (Table 3). At a glance, GPT-5 mini
provides a favorable efficiency–effectiveness trade-off; Qwen-2.5-72B and DeepSeek-V3 are
moderate; Llama-4 Maverick tends to require more iterations and time.

                                             9
                                      Li Li Xu Chen




Figure 4: LLM backbone ablation across five metrics (higher is better for success, ≤ 6 iter-
          ations, and decay-rate satisfaction; lower is better for normalized γ and ∥Hcl ∥∞ ).
          Bars show medians across 14 problems.



6. Conclusion
We presented S2C, a multi-agent pipeline that translates natural-language specifications
into certified H∞ state-feedback controllers via convex synthesis. The system integrates a
SpecInt–Solv–Tester–Adapt loop with decay-rate constraints, severity-aware γ-floor guardrails,
and automatic discrete-to-continuous conversion. On 14 COMPleib benchmarks, S2C
achieved 100% synthesis success and 100% convergence within six iterations. LLM abla-
tions confirm robustness: GPT-5 attains highest effectiveness, GPT-5 mini offers favorable
efficiency.
     Key limitations include: state-feedback scope (no output-feedback or dynamic designs),
overshoot measured but not enforced, Tustin-based D2C (not native discrete synthesis),
and nominal LTI assumptions without parametric uncertainty or actuator limits. Future
work targets output-feedback, mixed H∞ /H2 synthesis, explicit transient shaping, robust
uncertainty handling, and improved adaptation strategies.
     Overall, S2C demonstrates that LLM agents can integrate certificate-bearing control
synthesis from high-level intent while retaining formal guarantees.


References
Mosek ApS. Mosek optimization toolbox for matlab. User’s Guide and Reference Manual,
 Version, 4(1):116, 2019.

Christopher Bissell. A history of automatic control. In Springer handbook of automation,
 pages 53–69. Springer, 2009.

                                             10
                        LLM Agents for H-infinity Control




Stephen P Boyd and Craig H Barratt. Linear controller design: limits of performance,
  volume 78. Prentice Hall Englewood Cliffs, NJ, 1991.

Stephen Boyd and Lieven Vandenberghe. Convex optimization. Cambridge university press,
  2004.

Stephen Boyd, Venkataramanan Balakrishnan, Eric Feron, and Laurent ElGhaoui. Control
  system analysis and synthesis via linear matrix inequalities. In 1993 American Control
  Conference, pages 2147–2154. IEEE, 1993.

Jayeeta Chaudhuri, Dhruv Thapar, Arjun Chaudhuri, Farshad Firouzi, and Krishnendu
  Chakrabarty. Spiced+: Syntactical bug pattern identification and correction of trojans
  in a/ms circuits using llm-enhanced detection. IEEE Transactions on Very Large Scale
  Integration (VLSI) Systems, 2025.

Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chi-Min Chan, Heyang
 Yu, Yaxi Lu, Yi-Hsin Hung, Chen Qian, et al. Agentverse: Facilitating multi-agent
 collaboration and exploring emergent behaviors. In The Twelfth International Conference
 on Learning Representations, 2023.

MICHAEL J Denham. Design issues for CACSD systems. Proceedings of the IEEE, 72(12):
 1714–1723, 2005.

Steven Diamond and Stephen Boyd. CVXPY: A Python-embedded modeling language for
  convex optimization. Journal of Machine Learning Research, 17(83):1–5, 2016.

Benjamin Doerr and Carola Doerr. Theory of parameter control for discrete black-box
  optimization: Provable performance gains through dynamic parameter choices. Theory
  of Evolutionary Computation: Recent Developments in Discrete Optimization, pages 271–
  321, 2019.

Pascal Gahinet. Explicit controller formulas for lmi-based H∞ synthesis. Automatica, 32
  (7):1007–1014, 1996.

Da-Wei Gu, Petko Hristov Petkov, and Mihail Mihaylov Konstantinov. Robust control
 design with MATLAB®. Springer, 2005.

Xingang Guo, Darioush Keivan, Usman Syed, Lianhui Qin, Huan Zhang, Geir Dullerud,
  Peter Seiler, and Bin Hu. Controlagent: Automating control system design via novel
  integration of llm agents and domain expertise. arXiv preprint arXiv:2410.19811, 2024.

Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang,
  Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. MetaGPT: Meta
  programming for a multi-agent collaborative framework. In The Twelfth International
  Conference on Learning Representations, 2023.

Jie Huang and Kevin Chen-Chuan Chang. Towards reasoning in large language models: A
  survey. arXiv preprint arXiv:2212.10403, 2022.

                                          11
                                     Li Li Xu Chen




Linbin Huang, Huanhai Xin, and Florian Dörfler. H∞-control of grid-connected converters:
  Design, objectives and decentralized stability certificates. IEEE Transactions on Smart
  Grid, 11(5):3805–3816, 2020.
Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. A survey on large
  language models for code generation. arXiv preprint arXiv:2406.00515, 2024.
Ming Jin and Javad Lavaei. Stability-certified reinforcement learning: A control-theoretic
 perspective. IEEE Access, 8:229086–229100, 2020.
Darioush Kevian, Usman Syed, Xingang Guo, Aaron Havens, Geir Dullerud, Peter Seiler,
 Lianhui Qin, and Bin Hu. Capabilities of large language models in control engineer-
 ing: A benchmark study on gpt-4, claude 3 opus, and gemini 1.0 ultra. arXiv preprint
 arXiv:2404.03647, 2024.
Hermann Kopetz, Ralph Zainlinger, Gerhard Fohler, Heinz Kantz, P Puschner, and Werner
  Schütz. The design of real-time systems: From specification to implementation and
  verification. Software Engineering Journal, 6(3):72–82, 1991.
Yao Lai, Sungyoung Lee, Guojin Chen, Souradip Poddar, Mengkang Hu, David Z Pan,
  and Ping Luo. Analogcoder: Analog circuit design via training-free code generation. In
  Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 379–387,
  2025.
F Leibfritz. COMPleib: Constrained matrix optimization problem library. Online at
  http://www. compleib. de, 2006.
Maosen Li, Siheng Chen, Yanning Shen, Genjia Liu, Ivor W Tsang, and Ya Zhang. Online
 multi-agent forecasting with interpretable collaborative graph neural networks. IEEE
 Transactions on Neural Networks and Learning Systems, 35(4):4768–4782, 2022.
Xinyi Li, Sai Wang, Siqi Zeng, Yu Wu, and Yi Yang. A survey on LLM-based multi-agent
  systems: workflow, infrastructure, and challenges. Vicinagearth, 1(1):9, 2024.
Chengjie Liu, Weiyu Chen, Anlan Peng, Yuan Du, Li Du, and Jun Yang. Ampagent: An
 llm-based multi-agent system for multi-stage amplifier schematic design from literature
 for process and performance porting. arXiv preprint arXiv:2409.14739, 2024.
Johan Lofberg. YALMIP: A toolbox for modeling and optimization in MATLAB. In 2004
  IEEE international conference on robotics and automation (IEEE Cat. No. 04CH37508),
  pages 284–289. IEEE, 2004.
Donald W Loveland. Automated theorem proving: A logical basis. Elsevier, 2016.
Mohammad Narimani and Seyyed Ali Emami. AgenticControl: An Automated Control
 Design Framework Using Large Language Models. arXiv preprint arXiv:2506.19160,
 2025.
Nhan Nguyen and Sarah Nadi. An empirical evaluation of GitHub copilot’s code suggestions.
 In Proceedings of the 19th International Conference on Mining Software Repositories,
 pages 1–5, 2022.

                                           12
                         LLM Agents for H-infinity Control




Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio
  Savarese, and Caiming Xiong. Codegen: An open large language model for code with
  multi-turn program synthesis. arXiv preprint arXiv:2203.13474, 2022.

Isaac Kofi Nti, Adebayo Felix Adekoya, Benjamin Asubam Weyori, and Owusu Nyarko-
  Boateng. Applications of artificial intelligence in engineering and manufacturing: a sys-
  tematic review. Journal of Intelligent Manufacturing, 33(6):1581–1601, 2022.

R OpenAI. Gpt-4 technical report. arxiv 2303.08774. View in Article, 2(5):1, 2023.

Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang,
 Weize Chen, Yusheng Su, Xin Cong, et al. Chatdev: Communicative agents for software
 development. arXiv preprint arXiv:2307.07924, 2023.

Shuo Ren, Pu Jian, Zhenjiang Ren, Chunlin Leng, Can Xie, and Jiajun Zhang. To-
  wards scientific intelligence: A survey of llm-based scientific agents. arXiv preprint
  arXiv:2503.24047, 2025.

IG Sarma. Computer-aided Control System Design (CACSD): Some Perspectives. In Au-
  tomation and Instrumentation for Power Plants, pages 5–6. Elsevier, 1989.

Joseph Sifakis. System design automation: Challenges and limitations. Proceedings of the
  IEEE, 103(11):2093–2103, 2015.

Peter Sunehag, Guy Lever, Audrunas Gruslys, Wojciech Marian Czarnecki, Vinicius Zam-
  baldi, Max Jaderberg, Marc Lanctot, Nicolas Sonnerat, Joel Z Leibo, Karl Tuyls,
  et al. Value-decomposition networks for cooperative multi-agent learning. arXiv preprint
  arXiv:1706.05296, 2017.

Kim-Chuan Toh, Michael J Todd, and Reha H Tütüncü. SDPT3—a MATLAB software
  package for semidefinite programming, version 1.3. Optimization methods and software,
  11(1-4):545–581, 1999.

Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang,
  Xiaoyun Zhang, Shaokun Zhang, Jiale Liu, et al. Autogen: Enabling next-gen LLM
  applications via multi-agent conversations. In First Conference on Language Modeling,
  2024.

Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. Agentless: Demysti-
  fying llm-based software engineering agents. arXiv preprint arXiv:2407.01489, 2024.

Rasoul Zahedifar, Sayyed Ali Mirghasemi, Mahdieh Soleymani Baghshah, and Alireza
  Taheri. LLM-Agent-Controller: A Universal Multi-Agent Large Language Model Sys-
  tem as a Control Engineer. arXiv preprint arXiv:2505.19567, 2025.

Qingye Zhao, Xin Chen, Zhuoyu Zhao, Yifan Zhang, Enyi Tang, and Xuandong Li. Verifying
  neural network controlled systems using neural networks. In Proceedings of the 25th ACM
  International Conference on Hybrid Systems: Computation and Control, pages 1–11,
  2022.

                                            13
                                     Li Li Xu Chen




Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian
 Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models.
 arXiv preprint arXiv:2303.18223, 1(2), 2023.



Appendix A. Agent Prompts and System Instructions
This section provides implementation details and the exact system prompts used by S2C
agents to ensure reproducibility and transparency.

A.1. Implementation
The S2C framework is implemented in Python 3.10 with NumPy 1.24, SciPy 1.11, CVXPY
1.4 (Diamond and Boyd, 2016), and the Python Control Systems Library 0.9. LLM agents
interface with OpenAI API, DeepSeek API, Together AI API, and local vLLM servers for
open-source models. Experiments run on a desktop workstation (Intel i7-12700K, 32GB
RAM) running Windows 11. The discrete-to-continuous converter (d2c converter.py)
implements Tustin bilinear transformation with sampling period Ts = 1.0. The H∞ synthe-
sis LMI is solved via MOSEK when available, with automatic fallback to the open-source
SCS solver. Monte Carlo simulations use a fixed random seed (42) for reproducibility across
ablation studies.
    For the ablation study comparing LLM-based code-generation baselines, we freeze prompts,
random seeds, and step budgets (Nmax = 10) across all models. Each model receives identi-
cal natural language requirements, plant models, and verification feedback. We test GPT-5
(our baseline), GPT-5 mini, DeepSeek-V3, Qwen-2.5-72B-Instruct (served via vLLM), and
Llama-4 Maverick (via Together AI). All experiments log LLM call counts, iteration histo-
ries, and final controller performance for fair comparison.

A.2. SpecIntAgent (Discovery Agent)
The SpecIntAgent uses the following system prompt to extract numeric specifications from
natural language requirements:

You are an expert control engineer specializing in translating
natural language requirements into formal control specifications.

TASK: Parse natural language requirements and extract formal
control specifications.

OUTPUT FORMAT: JSON object containing specifications:
{
  "h_infinity_norm": {
    "target": <float>,
    "priority": "critical" | "high" | "medium" | "low",
    "slack": <float>
  },
  "settling_time": {
    "target": <float in seconds>,


                                           14
                         LLM Agents for H-infinity Control




      "priority": ...,
      "slack": <float>
    },
    "overshoot": {
      "target": <float as fraction, e.g., 0.10 for 10%>,
      "priority": ...,
      "slack": <float>
    }
}

INTERPRETATION RULES:
- "Fast" → settling_time: 2-3s
- "Smooth" → overshoot: 0.05-0.10
- "Strongly reject" → h_infinity_norm: 1.5-2.0
- Explicit requirements → HIGH or CRITICAL priority
- Strict requirements → 5-10% slack

IMPORTANT: Always include h_infinity_norm (required for synthesis)

A.3. AdaptAgent (Adaptation Agent)
The AdaptAgent refines specifications based on verification feedback:

You are an expert in iterative control design refinement and
specification adaptation.

TASK: Analyze verification feedback and violations, then refine
specifications to improve the design while maintaining feasibility.

ADAPTATION STRATEGY:

High Overshoot:
  - Relax settling_time by 15-20%
  - Tighten overshoot by 5-10%
  - Consider increasing gamma slightly

Poor Disturbance Rejection:
  - Tighten h_infinity_norm by 10-15%
  - May need to relax time-domain specs

Infeasible Synthesis:
  - Relax gamma by 20-30%
  - Identify and relax lowest priority specs

Progressive Refinement (Iterations 1-3):
  - Small adjustments (5-10%)
  - Focus on highest priority violations

Moderate Changes (Iterations 4-7):
  - Medium adjustments (10-20%)
  - Start trading off conflicting requirements


                                            15
                                      Li Li Xu Chen




Aggressive Relaxation (Iterations 8+):
  - Large adjustments (20-40%)
  - Consider feasibility over optimality


Appendix B. NN1 Showcase: Evolution of S2C Design
This section presents a detailed case study of S2C applied to the NN1 benchmark problem
using GPT-5 as the LLM backbone. We demonstrate how the multi-agent system iteratively
refines the controller design to satisfy performance specifications while maintaining formal
guarantees.

B.1. Discovery Phase
Natural Language Requirements:            The user provides the following informal require-
ments:

       “Design a robust H-infinity controller for the NN1 system with the following
       requirements: Minimize overshoot (target less than 10%, high priority); Fast
       settling time (target 16 seconds with 2s tolerance); Good disturbance rejection
       (H-infinity norm less than 20); Ensure adequate stability margins with decay
       rate α ≥ 0.25.”

SpecIntAgent Output: The SpecIntAgent (GPT-5) parses these requirements and ex-
tracts formal specifications:

{
    "settling_time": {"target": 16.0, "priority": "medium", "slack": 2.0},
    "overshoot": {"target": 0.1, "priority": "high", "slack": 0.05},
    "h_infinity_norm": {"target": 20.0, "priority": "high", "slack": 2.0},
    "decay_rate": {"target": 0.25, "priority": "medium"}
}

    The LLM identifies overshoot as high priority, assigns reasonable slack values (2s for
settling time, 5% for overshoot), and derives the decay-rate constraint α = 0.25 from the
stability requirement.

B.2. Evolution Across Iterations
Figure 5 illustrates how S2C’s performance evolves over 6 iterations. The design process
exhibits clear convergence patterns characteristic of effective multi-agent collaboration.
Key Observations from Figure 5: Measured Overshoot (Left Panel): Initially,
the measured overshoot is 93.9%, significantly exceeding the 10% target (shown as green
dashed line). This large overshoot is driven by aggressive bandwidth selection to meet
settling time. The AdaptAgent progressively adjusts the speed-damping trade-off, reducing
measured overshoot to 34.2% by iteration 5. While significant improvement occurs (64%
reduction in absolute overshoot), the target is not reached—a known limitation of state-
feedback H∞ synthesis without explicit time-domain shaping constraints (see §G).

                                             16
                           LLM Agents for H-infinity Control




Figure 5: Evolution of S2C design for NN1 benchmark (GPT-5 baseline). Left: Measured
          overshoot decreases from 93.9% to 34.2% (target: 10%, shown as green dashed
          line). Center: Settling time error reduces from +16% to -0.6% (specification met).
          Right: Decay rate satisfaction improves from 86% to 127% of target α.



    Settling Time Error (Center Panel): The settling time violation is minor initially
(+16.2%) and improves. By iteration 4, the error drops to +1.9%, and by iteration 5,
the specification is met with -0.6% error (15.9s vs 16.0s target). This demonstrates the
decay-rate constraint’s effectiveness in enforcing temporal specifications.
    Decay Rate Satisfaction (Right Panel): The decay-rate constraint ℜ(λ) < −α is
tightened. Initial synthesis achieves 86% of target α (maxℜλ = −0.21 vs −α = −0.244).
The gamma-floor guardrail mechanism (activated at iteration 1) stabilizes the design, and by
iteration 4, decay rate satisfaction reaches 135% (poles at −0.33, exceeding the requirement).
This over-achievement provides additional stability margin.

B.3. Detailed Iteration History
Table 1 provides comprehensive metrics for each iteration.


        Table 1: NN1 detailed design history across 6 iterations (GPT-5 baseline).
            Iter    γ      γmin   maxℜλ   ∥Hcl ∥∞   OS (%)   Ts (s)   Viol.   LLM
             0     14.64    –     −0.21    6.57      93.9     18.6     2      –
             1     18.00   18.0   −0.16    5.87      84.2     18.2     2      ✓
             2     18.00   18.0   −0.17    6.02      72.1     17.4     2      ✓
             3     18.00   18.0   −0.28    5.74      58.3     16.8     2      ✓
             4     18.00   18.0   −0.33    5.58      43.5     16.3     1      ✓
             5     18.00   18.0   −0.31    5.61      34.2     15.9     1      ✓



Iteration 0: Initial synthesis without guardrails achieves excellent certified bound (γ =
14.64, 73% of target) but exhibits severe overshoot (93.9%) and minor settling time violation
(18.6s vs 16.0s target). The open-loop NN1 system has an unstable pole at +3.606 (see
Figure 6); initial synthesis successfully stabilizes all poles to maxℜλ = −0.21.

                                             17
                                      Li Li Xu Chen




Figure 6: Pole migration for NN1 showing stabilization across iterations. Open-loop system
          has unstable pole at +3.606 (black X). S2C progressively moves closed-loop poles
          leftward: iteration 1 (purple) at maxℜλ = −0.16, iteration 2 (gray) at −0.17,
          and iteration 5 (yellow) at −0.31. All closed-loop poles remain stable throughout
          refinement, with final poles at {−0.310 ± 0.594j, −0.310}.


Iteration 1: AdaptAgent (GPT-5) diagnoses the overshoot-settling conflict and activates
the gamma-floor guardrail at γmin = 18.0 (90% of target). This forces synthesis to prioritize
transient quality over optimal disturbance rejection. Overshoot improves to 84.2%, settling
time to 18.2s. Note that poles move slightly rightward (−0.21 → −0.16) as the guardrail
trades decay rate for improved H∞ performance.
Iterations 2–3: Continued LLM-guided refinement progressively reduces both violations.
The decay rate improves significantly (−0.17 → −0.28), demonstrating the guardrail’s
effectiveness in stabilizing pole locations (visible in Figure 6 as leftward pole migration).
Iteration 4: Settling time violation resolves (16.3s, within tolerance). Decay rate reaches
135% of target (−0.33 vs −0.244). Only overshoot remains violated.
Iteration 5: Final design achieves settling time specification with margin (15.9s). Over-
shoot continues to improve but remains above 10% target. At this iteration, GPT-5 recog-
nizes the fundamental limitation and recommends accepting the design or switching syn-
thesis methods (see LLM recommendation below).

B.4. LLM Adaptation Quality and Limitations Recognition
Iteration 3 Example (GPT-5 Recognizes Trade-off ): The AdaptAgent receives
structured feedback indicating persistent overshoot (58.3%) and near-target settling time
(16.8s):
Violations:


                                             18
                          LLM Agents for H-infinity Control




  - overshoot: Measured 58.3%, target 10.0% [HIGH severity]
  - settling_time: Measured 16.8s, target 16.0s [LOW severity]

Feedback: "Overshoot remains 5.8x target despite improvements.
           Settling time nearly met. Recommend maintaining gamma
           floor to preserve transient quality gains."

GPT-5 Output:
{
  "diagnosis": {
    "root_causes": ["Insufficient damping despite slower response",
                    "State feedback cannot directly constrain overshoot"],
    "severity": "major",
    "pattern": "Consistent overshoot, improving settling time"
  },
  "updates": {
    "settling_time": {"target": 17.0, "rationale": "Relax further
                       to allow more damping"},
    "h_infinity_norm": {"min": 18.0, "rationale": "Maintain floor"}
  },
  "strategy": {"approach": "trade_off", "confidence": "medium"}
}

    The LLM identifies the fundamental trade-off, proposes gradual settling time relaxation,
and maintains the gamma-floor guardrail. This demonstrates sophisticated understanding
of control design trade-offs.
Iteration 5 Example (GPT-5 Recognizes Fundamental Limitation): By iteration
5, with overshoot still at 34.2% despite 6 iterations of refinement, GPT-5 provides diagnostic
analysis:

Violations:
  - overshoot: Measured 34.2%, target 10.0% [MEDIUM severity]
  - settling_time: Measured 15.9s, target 16.0s [NONE - MET]

GPT-5 Diagnostic Output:
{
  "diagnosis": {
    "root_causes": [
       "State-feedback H-infinity synthesis optimizes worst-case
        disturbance rejection, not transient overshoot",
       "LMI formulation lacks explicit time-domain shaping constraints",
       "Decay-rate constraint ensures exponential stability but
        does not bound overshoot for arbitrary initial conditions"
    ],
    "assessment": "Overshoot has improved 64% (93.9% -> 34.2%) but
                    cannot reach 10% target with current synthesis method",
    "limitation_identified": true
  },
  "recommendations": [
    {


                                             19
                                      Li Li Xu Chen




          "option": "Accept current design",
          "rationale": "Settling time and decay rate specifications met.
                        Overshoot improved significantly. Further iteration
                        unlikely to yield major gains within state-feedback
                        H-infinity framework."
     },
     {
          "option": "Switch synthesis approach [REQUIRES FRAMEWORK EXTENSION]",
          "suggestions": [
             "Output-feedback with integral action for better tracking",
             "Mixed H-infinity/H-2 to balance robustness and transient performance",
             "Pole-placement overlay with explicit damping ratio constraints",
             "Model-reference adaptive control for transient shaping"
          ],
          "note": "These methods not available in current S2C framework"
      }
    ],
    "final_decision": {
      "action": "terminate_iteration",
      "rationale": "Best achievable design within constraints.
                    2 of 3 hard specs met (settling time, decay rate).
                    Overshoot improved but limited by synthesis method.",
      "confidence": "high"
    }
}

     Key insight: GPT-5 diagnoses that the overshoot violation is not due to poor spec-
ification tuning, but rather a fundamental limitation of the synthesis method. The LLM
recognizes that:
    • Further spec relaxation would not resolve overshoot (already relaxed settling time)
    • The H∞ bounded-real lemma minimizes ∥Tzw ∥∞ , which does not constrain time-
       domain overshoot
    • Alternative synthesis methods (output feedback, mixed H∞ /H2 , pole placement)
       would be needed
    • The current S2C framework only supports state-feedback H∞ synthesis
     This demonstrates sophisticated LLM reasoning: GPT-5 not only adapts specifi-
cations but also recognizes when the problem lies outside the scope of available tools, and
recommends accepting the best achievable solution or extending the framework. This is
analogous to a human control engineer concluding that “we’ve pushed state-feedback H∞
as far as it can go; we need a different approach for overshoot.”

B.5. Generated Controller
Final controller (iteration 5):
                                                       
                              K = −3.612 −25.184 −4.597

     Closed-loop poles: {−0.310 ± 0.594j, −0.310} (all stable, maxℜλ = −0.31).
     Performance certificates:

                                            20
                          LLM Agents for H-infinity Control




   • H∞ certified bound: γ = 18.00 (90% of target 20.0)
   • Disturbance rejection: ∥C(sI − Acl )−1 E∥∞ = 5.61
   • Decay rate: − maxℜλ = 0.31 > α = 0.244 (127% of target)
   • Settling time: 15.9s < 16.0s (specification met)
   • Overshoot: 34.2% (violation persists, see discussion in §G)
Summary: The NN1 showcase demonstrates both the strengths and limitations of LLM-
guided control synthesis:
    Strengths demonstrated:
    • GPT-5 successfully navigates design trade-offs through iterative refinement
    • Settling time and decay rate specifications met with certified guarantees
    • LLM recognizes fundamental synthesis method limitations (not just parameter tuning)
    • Sophisticated diagnostic reasoning about when to stop iterating
    • Appropriate recommendations for framework extensions
    Limitations revealed:
    • State-feedback H∞ synthesis cannot constrain overshoot
    • LLM bounded by tools available in framework (cannot synthesize outside H∞ state-
      feedback)
    • Overshoot improved but target not achievable with current method
    • Framework extension needed for time-domain shaping (output feedback, mixed syn-
      thesis, etc.)
    Key takeaway: The LLM’s ability to recognize and articulate that the overshoot lim-
itation is methodological (not parametric) demonstrates genuine understanding of control
theory. A less sophisticated agent would continue iterating indefinitely, whereas GPT-5
diagnoses the need for alternative synthesis approaches and recommends terminating iter-
ation with the best achievable design. This honest recognition of limitations is crucial for
trustworthy autonomous design systems.

Appendix C. Mathematical Formulation Details
C.1. Discrete-to-Continuous Conversion (Tustin)
Discrete-time systems are converted to continuous-time via the bilinear (Tustin) transfor-
mation with sampling period Ts = 1.0:

                                     2
                                Ac =    (Ad − I)(Ad + I)−1 ,                              (5)
                                     Ts
                                     2
                                Bc = (Ad + I)−1 Bd ,                                      (6)
                                     Ts
                                Cc = Cd (Ad + I)−1 ,                                      (7)
                                                       −1
                                Dc = Dd − Cd (Ad + I)       Bd .                          (8)

    This transformation preserves stability (maps unit circle to left-half plane) and approxi-
mately preserves frequency response near the Nyquist frequency. Energy-consistent scaling
is applied by matching steady-state gains. Validation is performed by checking eigenvalue
migration: |λd | < 1 ⇒ ℜ(λc ) < 0.

                                             21
                                          Li Li Xu Chen




C.2. Matrix Aliases
To unify nomenclature across COMPleib and standard H∞ formulations, we use:

                               E ≡ B1      (disturbance input),
                              Cz ≡ C1      (regulated output),
                              Dz ≡ D12        (control feedthrough).

C.3. Bounded-Real Lemma LMI
The H∞ synthesis problem is formulated as a convex optimization:

                             minimize     γ
                             P ≻0, Y, γ

                            subject to    Ψ(P, Y, γ) ≺ 0,                                (9)
                                          P ⪰ 0.1I     (conditioning),
                                          γmin ≤ γ ≤ γtarget ,

where
                                                   (Cz P + Dz Y )⊤
                                                                  
                                sym(AP + BY ) E
                  Ψ(P, Y, γ) =       E⊤       −γI        0        ,                   (10)
                                  Cz P + D z Y  0        −γI

with sym(X) = X + X ⊤ .
    Feasibility of Ψ ≺ 0 certifies ∥Tzw ∥∞ < γ via the bounded-real lemma. The controller
is recovered as K = Y P −1 .

C.4. Decay-Rate Constraint
For settling-time specifications Ts,target , we enforce a pole-region constraint:

                                                                   3.9
                         sym(AP + BY ) + 2αP ≺ 0,           α=               .          (11)
                                                                 Ts,target

    This ensures all closed-loop poles satisfy ℜ(λi (A+BK)) < −α, guaranteeing exponential
decay rate e−αt and approximate settling time Ts ≈ 3.9/α (2% criterion).
    The factor 3.9 is derived from the step response of a first-order system: 1 − e−αt = 0.98
at t = 3.9/α.

C.5. Numerical Safeguards
To ensure well-conditioned solutions, we enforce:
   • P ⪰ 0.1I (strong positive definiteness)
   • Solver tolerance: ϵ = 10−8
   • Maximum iterations: 5000 (SCS), 2500 (MOSEK)
   • Eigenvalue check: maxi ℜ(λi (A + BK)) < 0 (stability verification)

                                                 22
                         LLM Agents for H-infinity Control




Appendix D. Extended Algorithms


D.1. Main S2C Iterative Loop


Algorithm 1 provides the complete pseudocode for the S2C iterative synthesis-verification-
adaptation loop.


Algorithm 1 S2C Iterative Design Pipeline (Complete)
Require: Plant P = (A, B, C, Bd , . . .), requirements r, max iterations Nmax
Ensure: Controller K, generated code
 1: S ← SpecInt.parse requirements(r, P )
 2: Initialize Memory ← ∅
 3: for i = 1 to Nmax do
 4:   // Synthesis
 5:   (ok, K, γ) ← SolvAgent.solve hinf lmi(P, S.hinf.target, S.hinf.min, α=3.9/S.Ts )

 6:    if ¬ok then
 7:       S ← AdaptAgent.relax specs(S)
 8:       continue
 9:    end if
10:    // Verification
11:    mc ← TesterAgent.monte carlo(A, B, K) {50 trials, 20s horizon}
12:    fd ← TesterAgent.freq domain(A, B, K, C, Bd )
13:    if fd.controller type = state fb then
14:       fd.disturbance rejection ← ∥C(sI − (A + BK))−1 Bd ∥∞
15:    end if
16:    V ← TesterAgent.check(mc, fd, S) {Compute violations}
17:    Memory.add(i, K, γ, mc, fd, V, S)
18:    if V = ∅ then
19:       break {All specs satisfied}
20:    end if
21:    // Adaptation
22:    f b ← FeedbackGen.generate(V )
23:    S ← AdaptAgent.refine specs(S, f b, Memory, i) {LLM update}
24:    S.hinf.min ← UpdateGammaFloor(S, V, γ, i) {See Alg. 2}
25: end for
26: if V ̸= ∅ then
27:    (K, γ) ← SelectBestDesign(Memory) {Fallback: fewest violations, then lowest γ}
28: end if
29: code ← CodeGen.generate(K, P, python)
30: return K, code




                                           23
                                        Li Li Xu Chen




D.2. Gamma-Floor Guardrail Formulation
The gamma-floor guardrail prevents excessive γ minimization from degrading transient
performance by dynamically raising γmin when settling-time or overshoot violations occur.
The update mechanism combines two components:
Severity-Based Base Floor. The base floor is determined by violation severity:
                       
                       0.05 × γtarget if severity = low
                       
                γbase = 0.10 × γtarget if severity = medium                                 (12)
                       
                        0.20 × γtarget if severity ∈ {high, critical}
                       

History-Based Candidate Floor. The history-based component accounts for recent
synthesis performance and iteration count:
                                                                        
                   γhist = γlast × m(severity) × 1 + 0.1 · min(i − 1, 5)  (13)

where γlast is the most recently achieved γ value, iteration i ∈ [1, Nmax ], and the multiplier
m is:                                  
                                       
                                       
                                        1.2   if severity = low
                                       
                                       2.0    if severity = medium
                        m(severity) =                                                     (14)
                                       
                                       
                                        5.0   if severity = high
                                       
                                       10.0 if severity = critical

The iteration factor (1 + 0.1 · min(i − 1, 5)) increases the floor progressively over iterations,
capped at 1.5× by iteration 6 to prevent overly conservative bounds.
Floor Update Rule.       The new floor is computed as:
                                                                     
                     γmin ← min 0.9 γtarget , max γmin , γbase , γhist                      (15)

This ensures: (i) monotonic (nondecreasing) floor values across iterations; (ii) feasibility by
capping strictly below 0.9 γtarget ; (iii) adaptation to both severity and synthesis history.
   Algorithm 2 provides the complete procedural implementation.




                                               24
                         LLM Agents for H-infinity Control




Algorithm 2 Gamma-Floor Guardrail Update
Require: Current specs S, violations V , last achieved γlast , iteration i
Ensure: Updated S.hinf.min
 1: severity ← max{sev(v) : v ∈ V } where sev ∈ {low, medium, high, critical}
 2: // Base floor by severity
 3: if severity = low then
 4:    γbase ← 0.05 × S.hinf.target
 5: else if severity = medium then
 6:    γbase ← 0.10 × S.hinf.target
 7: else
 8:    γbase ← 0.20 × S.hinf.target {high or critical}
 9: end if
10: // History-based candidate
11: if severity = low then
12:    m ← 1.2
13: else if severity = medium then
14:    m ← 2.0
15: else if severity = high then
16:    m ← 5.0
17: else
18:    m ← 10.0 {critical}
19: end if
                                               
20: γhist ← γlast × m × 1 + 0.1 · min(i − 1, 5)
21: // Update floor (monotonic, capped)
                  
22: γnew ← max S.hinf.min, γbase , γhist
                                                   
23: S.hinf.min ← min 0.9 × S.hinf.target, γnew
24: return S.hinf.min


D.3. State-Feedback Frequency Analysis
Algorithm 3 shows the branching logic for frequency-domain verification.




                                           25
                                      Li Li Xu Chen




Algorithm 3 Frequency-Domain Analysis (State vs Output Feedback)
Require: Plant (A, B, C), controller K, disturbance matrix Bdist
Ensure: Frequency-domain metrics
 1: nx ← size(A, 1), ny ← size(C, 1)
 2: if size(K, 2) = nx then
 3:    Acl ← A + BK {State feedback: u = Kx}
 4:    Hcl ← C(sI − Acl )−1 Bdist
 5:    dist rej ← ∥Hcl ∥∞
 6:    return {controller type: state fb, disturbance rejection: dist rej}
 7: else
 8:    G ← C(sI − A)−1 B {Output feedback: u = Ky}
 9:    L ← GK
10:    S ← (I + L)−1 , T ← L(I + L)−1
11:    Ms ← ∥S∥∞ , Mt ← ∥T ∥∞
12:    Compute gain margin GM , phase margin P M from L(jω)
13:    return {controller type: output fb, Ms , Mt , GM, P M }
14: end if


Appendix E. Extended Results Tables
E.1. Benchmark Characteristics (Full Table)
Table 2 provides complete characteristics for all 18 COMPleib problems (14 evaluated in
main experiments + 4 heat-flow problems).

E.2. LLM Ablation: Efficiency Metrics
Table 3 reports API usage, latency, and estimated costs for the LLM ablation study.
Observations:
  • GPT-5 mini offers the best cost-effectiveness: 92% of GPT-5’s success rate at 19% of
    the cost.
  • Qwen-2.5-72B requires local deployment but eliminates API costs.
  • Llama-4 Maverick requires 30% more iterations, increasing both latency and cost.

Appendix F. Experimental Configuration and Reproducibility
F.1. Software Environment
   • Language: Python 3.10.12
   • Core libraries:
       – NumPy 1.24.3 (numerical arrays)
       – SciPy 1.11.2 (matrix computations)
       – CVXPY 1.4.1 (convex optimization)
       – Python Control Systems Library 0.9.4 (LTI analysis)
   • Solvers:
       – MOSEK 10.0.43 (primary, commercial)

                                             26
                         LLM Agents for H-infinity Control




Table 2: COMPleib benchmark characteristics.     Problem types:    AC=Aircraft,
         HE=Helicopter, REA=Reactor, DIS=Decentralized, NN=Academic. Stability de-
         termined by max Re(λ(A)).

               Problem    nx     nu   ny     nw         Time      Stable     Type
               NN2        2      1     1     2         Discrete    Yes       Academic
               AC5        4      2     2     2         Discrete    Yes       Aircraft
               REA2       4      2     2     2          Cont.      Yes       Reactor
               NN1        3      1     2     3          Cont.      No        Academic
               NN3        3      2     1     3          Cont.      No        Academic
               NN4        4      1     1     4          Cont.      Yes       Academic
               NN8        3      2     1     3         Discrete    Yes       Academic
               HE1        4      2     2     2          Cont.      Yes       Helicopter
               HE2        4      2     2     2          Cont.      Yes       Helicopter
               DIS2       2      2     2     2          Cont.      Yes       Decentral.
               DIS5       2      2     2     2         Discrete    Yes       Decentral.
               AC4        4      2     2     2          Cont.      Yes       Aircraft
               AC15       4      1     1     4          Cont.      Yes       Aircraft
               AC17       4      1     1     4          Cont.      Yes       Aircraft
                  Additional heat-flow problems (not in main experiments)
               HF2D12     5      2     4     2          Cont.      Yes       Heat Flow
               HF2D13     5      2     4     2          Cont.      Yes       Heat Flow
               HF2D14     5      2     4     2          Cont.      No        Heat Flow
               HF2D18     5      2     4     2          Cont.      Yes       Heat Flow


     Table 3: LLM ablation study: efficiency metrics (medians across 14 problems).
      Model              Calls    Tokens (k)       Latency (s/iter)        Est. Cost ($/problem)
      GPT-5              12.5         18.2                  2.8                     0.42
      GPT-5 mini         11.0         16.5                  1.9                     0.08
      DeepSeek-V3        13.5         19.1                  3.2                     0.12
      Qwen-2.5-72B       14.0         20.3                  4.1                     0.001
      Llama-4 Maverick   16.5         24.7                  5.3                     0.18


       – SCS 3.2.3 (fallback, open-source)
   • LLM APIs:
       – OpenAI API (GPT-5, GPT-5 mini)
       – DeepSeek API (DeepSeek-V3)
       – Together AI API (Llama-4 Maverick)
       – vLLM 0.4.2 (Qwen-2.5-72B local deployment)


F.2. Hardware and Operating System
   • CPU: Intel Core i7-12700K (12 cores, 3.6 GHz base, 5.0 GHz boost)
   • RAM: 32 GB DDR4-3200

                                                  27
                                    Li Li Xu Chen




   • OS: Windows 11 Pro (Build 22621)
   • Storage: NVMe SSD (PCIe 4.0)

F.3. Monte Carlo Verification Settings
   • Trials: N = 50 per controller
   • Initial conditions: Sampled uniformly from unit sphere (unit-norm Gaussian ran-
     dom vectors)
   • Simulation horizon: T = 20 seconds
   • Time steps: 2000 (dt = 0.01s)
   • Settling criterion: 2% of peak state norm
   • Random seed: 42 (fixed for reproducibility)

F.4. Running the Full Pipeline
To reproduce the complete S2C pipeline on a benchmark problem:

cd s2c_agent
export OPENAI_API_KEY="sk-..."       # Set your API key

# Run single problem
python -c "
from llm_ablation_study import AblationStudyRunner
from gpt5 import ExtendedLLMInterface

runner = AblationStudyRunner(problem_name=’NN1’,
                              max_iterations=10,
                              random_seed=42)
llm = ExtendedLLMInterface(model=’gpt-5’, provider=’openai’)
results = runner.run_single_model(’GPT-5’, llm)
"

# Run full ablation study
python llm_ablation_study.py

Appendix G. Additional Discussions
G.1. Overshoot Persistence
Despite achieving 100% synthesis success and convergence, several problems (notably NN1,
NN3) exhibit persistent overshoot violations even after meeting settling time and distur-
bance rejection targets. This is a fundamental limitation of H∞ synthesis with decay-rate
constraints:
   • The decay-rate constraint ℜ(λ) < −α enforces exponential decay but does not limit
      overshoot.
   • State-feedback H∞ synthesis optimizes worst-case disturbance rejection, not time-
      domain transient shaping.

                                           28
                        LLM Agents for H-infinity Control




   • Overshoot depends on pole-zero locations and initial condition directions, which are
     not constrained by LMI formulations.

Future work directions:
   • Incorporate time-domain templates (e.g., reference model matching, transient bounds)
   • Use mixed H∞ /H2 synthesis to balance disturbance rejection and transient perfor-
     mance
   • Add explicit pole placement constraints in addition to decay-rate regions
   • Employ output feedback with integral action for improved tracking/regulation

G.2. Numerical Conditioning
Several benchmarks (AC5, HF2D14) exhibited numerical sensitivity during D2C conversion
or LMI solving:
   • D2C near-singularity: When Ad + I is ill-conditioned, Tustin transform magnifies
     errors. We mitigate this with explicit condition number checks and zero-order hold
     fallback.
   • LMI solver failures: Some problems require tighter tolerances (10−8 vs 10−6 ) or
     stronger conditioning (P ≻ 0.1I vs P ≻ 0).
   • Guardrail impact: The gamma-floor mechanism improved convergence for these
     problems by preventing numerically unstable low-gamma solutions.

G.3. LLM Adaptation Quality
Analysis of LLM-generated adaptation decisions reveals:
   • GPT-5/GPT-5 mini: Identify root causes and propose appropriate spec relax-
      ations. Rarely require heuristic fallback.
   • DeepSeek-V3/Qwen-2.5-72B: Good understanding of trade-offs but occasionally
      propose overly conservative relaxations. Fallback rate 15%.
   • Llama-4 Maverick: Struggles with conflicting requirements; fallback rate 35%.
      Benefits significantly from deterministic guardrails.
   The deterministic fallback heuristics ensure that even with weaker LLMs, the pipeline
maintains a success rate of over 85%—demonstrating the robustness of the multi-agent
architecture.


Appendix H. Detailed Limitations and Future Work
This section expands on the limitations and future directions briefly summarized in the
main paper.

H.1. Current Limitations
Controller Architecture. Our current scope is limited to static state-feedback con-
trollers of the form u = Kx. Output-feedback and dynamic architectures (e.g., PID,
lead/lag compensators, observers) are not synthesized within the present loop. This re-
striction affects:

                                           29
                                      Li Li Xu Chen




   • Frequency-domain metrics: For state feedback, classical loop-shaping metrics
     (Ms , Mt ) are undefined, so we emphasize a disturbance-rejection proxy ∥Cz (sI − (A +
     BK))−1 E∥∞ instead.
   • Practical deployment: State-feedback assumes full-state measurement or observer
     availability, which may not be realistic for all plants.
   • Performance trade-offs: Dynamic compensators can offer additional design free-
     dom for shaping closed-loop response beyond what static gains provide.

Transient Shaping. Overshoot is measured during Monte Carlo verification but not
enforced as a hard constraint in the LMI synthesis. The decay-rate constraint ℜ(λ) < −α
enforces exponential stability but does not bound overshoot for arbitrary initial conditions.
Consequently:
   • The simple adaptation heuristics can permit large overshoot on certain plants even
      when settling time and disturbance rejection specifications are satisfied.
   • State-feedback H∞ synthesis optimizes worst-case disturbance rejection, not time-
      domain transient shaping.
   • Alternative synthesis methods (output feedback, mixed H∞ /H2 , pole-placement over-
      lays) would be needed for explicit overshoot constraints.

Discrete-Time Handling. Discrete-time systems are converted to continuous-time via
Tustin bilinear transformation prior to synthesis. While this approach is standard and
works well for most benchmarks:
   • Native discrete-time LMIs may exhibit different performance trade-offs and avoid
     potential numerical issues from bilinear mapping.
   • The Tustin transform can introduce conditioning problems when Ad + I is nearly
     singular.
   • Sampling effects and aliasing are not explicitly modeled in the continuous-time ab-
     straction.

Modeling Assumptions. Experiments rely on nominal linear time-invariant (LTI) plants
without:
   • Parametric uncertainty: Polytopic or norm-bounded uncertainty descriptions are
     not currently handled.
   • Nonlinearities: The framework assumes linearized dynamics; nonlinear plants re-
     quire external linearization.
   • Actuator saturation: Control effort limits and anti-windup are not incorporated in
     synthesis.
   • Stochastic disturbances: Monte Carlo verification uses deterministic initial condi-
     tions; measurement noise and process disturbances are not modeled.

Verification Scope. Monte Carlo verification uses fixed simulation horizons (20s) and
deterministic seeds (42). While this provides reproducible validation:
   • Reachability analysis or formal barrier certificates would provide stronger guarantees.
   • Hardware-in-the-loop trials are not included in the evaluation pipeline.
   • Long-term stability beyond the simulation horizon is inferred from eigenvalue checks
     but not explicitly verified.

                                             30
                         LLM Agents for H-infinity Control




Computational and Cost Considerations. Practicality and cost depend on the LLM
backbone and provider:
   • API latency and token usage vary across models (GPT-5: $0.85/problem, GPT-5
     mini: $0.16/problem).
   • Numerical reliability can be sensitive to solver availability (MOSEK vs SCS) and
     problem conditioning.
   • The current implementation does not cache or distill LLM responses, leading to re-
     dundant API calls for similar problems.

H.2. Future Work Directions
Extended Controller Classes. We aim to extend the synthesis layer to support:
  • Output-feedback designs: Full-order and reduced-order observers, enabling de-
    ployment without full-state measurement.
  • Dynamic compensators: PID, lead/lag, notch filters, and observer-based architec-
    tures.
  • Mixed formulations: H∞ /H2 synthesis to balance robustness and transient perfor-
    mance, incorporating explicit (Ms , Mt ) targets.
  • Actuator limits: Anti-windup compensation and control effort constraints inte-
    grated into LMI formulations.

Native Discrete-Time Synthesis. Transition from Tustin-based discrete-to-continuous
conversion to native discrete-time LMIs:
   • Direct discrete H∞ synthesis via discrete bounded-real lemma.
   • Discrete decay-rate constraints formulated as LMI regions in the z-plane.
   • Elimination of numerical artifacts from bilinear transformation.

Robust and Uncertain Systems. Introduce uncertainty descriptions and robustness
analysis:
   • Polytopic uncertainty: LPV-style synthesis with vertex-based LMIs.
   • Norm-bounded uncertainty: Structured singular value (µ) surrogates and D-K
     iteration.
   • Stochastic disturbances: H2 covariance bounds and LQG-style formulations.

Advanced Adaptation Strategies. Replace heuristic specification updates with learned
or programmatic multi-objective strategies:
    • Goal programming: Lexicographic optimization jointly shaping γ, settling time,
      overshoot, and control effort.
    • Composite convex costs: Pareto-optimal trade-offs with adaptive weighting based
      on violation severity.
    • Convergence guarantees: Lyapunov-based adaptation rules with provable conver-
      gence to feasible specifications.
    • Learning-augmented guardrails: Train meta-models on past designs to predict
      effective γ-floor values and relaxation magnitudes.

Stronger Verification.    Integrate formal verification methods beyond Monte Carlo sim-
ulation:

                                          31
                                     Li Li Xu Chen




   • Reachability analysis: Hamilton-Jacobi methods or zonotope-based over-approximations
     to certify safety over infinite horizons.
   • Lyapunov/barrier certificates: SOS programming to synthesize certificates of sta-
     bility and constraint satisfaction.
   • Hardware-in-the-loop: Deploy controllers on real-time simulation platforms and
     physical testbeds.
Efficiency and Reproducibility. Improve computational efficiency and facilitate com-
munity adoption:
   • Token reduction: Distilled parsers for specification extraction, caching of LLM
      responses for similar problems.
   • Solver diversity: Plug-ins for additional solvers (SDPT3, YALMIP, CVXPY back-
      ends).
   • Reproducibility: Release scripts to regenerate all figures, tables, and benchmark
      results; provide Docker containers with pre-configured environments.
   • Benchmark expansion: Integrate additional problem suites (COMPleib heat-flow
      problems, aerospace benchmarks, power system models).
   • Provider flexibility: Support for additional LLM providers (Anthropic Claude,
      Google Gemini, local models via Ollama).
Deployment and Usability. Transition from research prototype to deployable tool:
  • Web interface: Browser-based GUI for natural-language specification and interac-
    tive design refinement.
  • Model upload: Support for importing plants from Simulink, MATLAB, Python
    Control, and CasADi.
  • Code generation: Extend to C/C++, Simulink blocks, and embedded targets
    (STM32, Arduino).
  • Certification reports: Automated generation of compliance documentation with
    formal performance certificates for safety-critical applications.

H.3. Broader Vision
Long-term, we envision S2C evolving into a multi-synthesis framework supporting diverse
control paradigms (model-predictive control, sliding mode, adaptive control) integrated by
LLM agents that reason about problem structure, performance requirements, and compu-
tational constraints. By combining formal synthesis, LLM-guided adaptation, and rigorous
verification, such systems could democratize certified controller design—enabling domain
experts without control theory expertise to specify requirements in natural language and
receive provably correct implementations.




                                           32
