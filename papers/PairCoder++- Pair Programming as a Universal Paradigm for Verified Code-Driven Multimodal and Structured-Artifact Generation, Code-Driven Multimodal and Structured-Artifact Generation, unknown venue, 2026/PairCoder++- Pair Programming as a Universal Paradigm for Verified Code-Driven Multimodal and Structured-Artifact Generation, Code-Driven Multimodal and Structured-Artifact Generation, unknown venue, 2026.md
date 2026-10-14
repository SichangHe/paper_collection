                                          PairCoder++: Pair Programming as a Universal Paradigm for Verified
                                              Code-Driven Multimodal and Structured-Artifact Generation
                                              Junhao Chen1 Xiang Li2 Mingjin Chen3 Boran Zhang4 Henghaofan Zhang5
                                                         Yibin Xu6 Yuehan Cui7 Fangsheng Weng8 Fei Ma9
                                                                 Qi Tian9 Ruqi Huang1 Hao Zhao1,10
                                               1
                                                   THU 2 PKU 3 PolyU, Hong Kong 4 USTC                                                           5
                                                                                                                                                     UESTC 6 Tongji University
                                                    7
                                                      Tianjin University 8 Independent Researcher                                                9
                                                                                                                                                     Guangming Lab 10 BAAI

                                                                       Project page: http://yisuanwang.github.io/PairCoder
                                                     a                                                                                               ChartMimic          PandasPlotBench
                                                                 Program synthesis                                           gain (pp)      b
                                                                                                                      0.92
                                             LiveCodeBench                                                                0.96   +4.1
                                                                                        0.43
                                              BigCodeBench                                                                         +1.7
arXiv:2607.01883v1 [cs.CL] 2 Jul 2026




                                                                                         0.45
                                                                                                      Single model
                                                                                0.28
                                                     DS-1000                     0.31                 PairCoder                    +2.5
                                                                 Multilingual
                                                                                         0.46
                                          HumanEval-X C++                                       0.57                              +11.0
                                                                                         0.45
                                          HumanEval-X Java                                    0.50                                 +4.9
                                                                                        0.45
                                            HumanEval-X JS                                    0.50                                 +5.5
                                                                                                                                                      DaTikZ               GenCAD-Code
                                                                 Web & Hardware
                                                                                                              0.79
                                                   WebApp1K                                                        0.84            +5.1
                                                                                                            0.74
                                                   VerilogEval                                                 0.83                +9.0
                                                                                       0.40
                                                         RTLLM                                       0.62                         +22.0
                                                                 Code-driven artifacts
                                                                                                        0.72
                                                       DaTikZ                                                              0.97 +25.0
                                                                                                                           0.96
                                                    Plot2Code                                                              0.98    +1.5
                                                                                                                           0.97
                                           PandasPlotBench                                                                  0.99 +2.8            3DCodeBench                 StarVector
                                                                                                                      0.92
                                                   ChartMimic                                                              0.98 +6.6
                                                                                                                     0.90
                                                   StarVector                                                               1.00+10.0
                                                                                                                    0.87
                                              GenCAD-Code                                                                  0.98 +11.6
                                                                                        0.43
                                              3DCodeBench                                                    0.78                 +35.0
                                                                                                        0.71
                                             P3D text-to-3D                                                                 0.99 +27.5

                                                             0.00        0.25           0.50           0.75            1.00
                                                      primary official metric (executable/compile/render/pass rate in [0, 1])



                                        Figure 1: PairCoder improves code generation across every artifact domain, not only Python program synthesis.
                                        (a) All 17 public benchmarks at gpt-5.4 (thinking off): the light bar is single-model, the dark bar (bold value) is
                                        PairCoder, coloured by benchmark family, with the absolute gain (pp) at right; each bar is the benchmark’s primary
                                        official metric, an executable/compile/render/pass rate in [0, 1]. P3D-Bench is shown on its text-to-3D track (400
                                        cases); its image-to-3D and assembly-3D tracks are reported as a 3-case demonstration in the appendix (Table 14).
                                        (b) Representative artifacts across six modalities: a chart (ChartMimic), a scientific figure (PandasPlotBench), a
                                        diagram (DaTikZ), a CAD model (GenCAD-Code), a 3D scene (3DCodeBench), and a vector graphic (StarVector).
                                                                    Abstract                                                              two switch roles when errors persist. Across
                                                                                                                                          17 public benchmarks and seven models from
                                            Code is the medium through which large lan-
                                                                                                                                          three vendors, PairCoder improves essentially
                                            guage models generate structured artifacts:
                                                                                                                                          every benchmark whose artifact is verifiable, on
                                            charts, scientific figures, vector graphics, CAD
                                                                                                                                          full official metric suites rather than execution
                                            models, 3D scenes, and hardware designs are
                                                                                                                                          alone (for example, Blender scene executabil-
                                            all produced by writing programs. In this
                                                                                                                                          ity 0.20 to 0.78; TikZ compile rate up 10 to
                                            regime single pass inference is brittle, because
                                                                                                                                          30 points on every model), at 2.9 to 9.2 times
                                            the compiler, renderer, or simulator that de-
                                                                                                                                          single model cost (about 7 times overall). The
                                            cides whether the artifact exists is invisible
                                                                                                                                          improvements concentrate where the toolchain
                                            to the model. We present PairCoder, which
                                                                                                                                          provides an informative oracle and the base-
                                            grounds review in the toolchain and realizes
                                                                                                                                          line leaves headroom, and the method ties or
                                            it as two agent pair programming: a Driver
                                                                                                                                          mildly regresses where the oracle is weak; we
                                            agent writes the program, a Navigator agent
                                                                                                                                          frame pair programming as a reliable recipe for
                                            reviews it against verification evidence (diag-
                                                                                                                                          verified code driven generation.
                                            nostics, execution results, and renderings of
                                            the current artifact beside the target), and the


                                                                                                                                    1
1   Introduction                                                 PairCoder instantiates this idea with three com-
                                                              ponents. (1) Driver and Navigator roles with Self-
Code generation for structured data and multimodal            Mirror prompting: the Driver generates and revises
content asks a model to write a program whose                 while the Navigator reviews, each under a role spe-
value lies in the artifact it renders: scientific fig-        cific system prompt over the shared task and mem-
ures as TikZ, charts as matplotlib, icons as SVG,             ory, preserving two genuinely different perspec-
mechanical parts as CAD programs, 3D scenes as                tives on the same code. (2) Verification grounded
Blender scripts, web applications as React projects,          review: each candidate is compiled, executed, or
and circuits as Verilog RTL (Belouadi et al., 2024a;          rendered by the benchmark’s own toolchain, and
Yang et al., 2024a; Wu et al., 2024; Galimzyanov              the evidence, including diagnostics, test outcomes,
et al., 2024; Rodriguez et al., 2025; Alam and                and a rendering of the current artifact beside the
Ahmed, 2024; Gao et al., 2026; Cui, 2024; Guo                 target, is attached to the review; the Navigator must
et al., 2025b; Liu et al., 2023b; Lu et al., 2024). The       cite a concrete error or accept with [NOERROR],
task is broadly useful and hard in a specific way:            which prevents churn on already correct programs.
the program must survive an external toolchain (a             (3) Error triggered role switching with a quality
compiler, renderer, or simulator) that the model              fallback: persistent errors swap the roles so the
cannot observe while writing, and the artifact must           agent that diagnosed the fault repairs it, and an ex-
then match the target in structure, semantics, and            hausted budget returns the candidate with the best
geometry. Even strong LLMs (OpenAI, 2023; Bai                 verified quality rather than the last one.
et al., 2023; Liu et al., 2024; Li et al., 2023b) rou-           Across 17 public benchmarks spanning program
tinely emit programs that do not compile, do not              synthesis, multilingual code, data science, web,
run, or render something far from the request (Li             hardware, and six artifact modalities, under seven
et al., 2023c; Zhang et al., 2025; Tian et al., 2025).        models from three vendors, PairCoder improves
   Existing remedies fall into two camps. One                 essentially every benchmark whose artifact is veri-
scales up collaboration: team style multi agent               fiable (Figure 1), on full official metric suites rather
frameworks (Hong et al., 2023; Qian et al., 2023; Li          than execution alone: Blender scene executability
et al., 2023a; Wu et al., 2023) and role specialized          rises from 0.20 to 0.78, TikZ compile rate gains
pipelines (Huang et al., 2023; Dong et al., 2024;             10 to 30 points on every model, and chart, SVG,
Islam et al., 2024; Chen et al., 2023c) improve               and CAD benchmarks improve in execution rate,
correctness but pay up to an order of magnitude               SSIM, and CLIP, while on classical synthesis Pair-
token overhead, and recent agentic creation sys-              Coder stays competitive and often improves further
tems show the same closed loop instinct in single             (e.g. LiveCodeBench pass@1 from 0.94 to 0.99
domains (Pfaff et al., 2026; Chen et al., 2025a).             at gpt-5.4-mini) at 2.9 to 9.2 times the single
The other camp keeps one model and adds self cor-             pass cost. A consistent pattern emerges: gains con-
rection from runtime feedback (Shinn et al., 2024;            centrate where the toolchain gives an informative
Chen et al., 2024; Madaan et al., 2023; Gou et al.,           oracle and the baseline leaves headroom, with ties
2024), which is cheap but inherits the blind spots of         at saturated oracles and mild regressions where the
a single perspective. Neither camp offers a domain            oracle is weak.
general mechanism that anchors an independent                    Our contributions are threefold: (1) PairCoder,
reviewer to the toolchain, which is exactly where             a two agent framework that grounds pair program-
code driven creation fails.                                   ming in toolchain verification, unifying verification
   We argue that this task needs the smallest collab-         grounded review and error triggered role switching
orative structure in which an independent reviewer            into one protocol across modalities; (2) the first sys-
is grounded in verification, and human software en-           tematic evidence that pair programming transfers
gineering already has it: pair programming (Uma-              from Python synthesis to structured data and multi-
pathy and Ritzhaupt, 2017; Lui and Chan, 2006;                modal artifact generation, improving executability,
Hannay et al., 2009). We propose PairCoder, a                 visual similarity (SSIM, CLIP, DINO, SigLIP-2),
two agent framework whose core idea is to turn                and geometry (Chamfer) across 17 benchmarks,
code driven generation into a toolchain verified di-          seven models, and three vendors; and (3) a quali-
alogue: one agent writes the program, the other               tative heuristic that gains scale with oracle infor-
reviews it against concrete verification evidence,            mativeness and baseline headroom, characterizing
and control of the keyboard follows the diagnosis.            when the collaboration helps, ties, or is wasted.

                                                          2
2     Related Work                                           tion (Weng et al., 2026b; Chen et al., 2026e; Sun
                                                             et al., 2025, 2026; Chen et al., 2026d,a); PairCoder
2.1    Large Language Models                                 instead keeps the program as the medium, which
LLMs (Achiam et al., 2023; Touvron et al., 2023;             makes the toolchain itself available as a verifier.
Bai et al., 2023; Hui et al., 2024; Yang et al., 2025;       PairCoder targets exactly this family of tasks and
Liu et al., 2024; Guo et al., 2025a) have made               improves the full official metric suites rather than
code one of their most impactful application do-             execution success alone; it is a concrete instance
mains (Chen et al., 2021; Liu et al., 2023a; Jiang           of the verification centered multimodal code intel-
et al., 2024), supported by code specialized model           ligence that recent surveys call for.
families (Nijkamp et al., 2023; Zheng et al., 2023;
Li et al., 2023b; Lozhkov et al., 2024; Roziere              2.3    Multi-Agent Collaboration
et al., 2023) and increasingly demanding bench-              Two strands of work attack the brittleness of sin-
marks (Jain et al., 2024; Zhuo et al., 2024; Lai             gle pass generation. Multi agent systems divide
et al., 2023; Jimenez et al., 2024; Zhang et al.,            labor across roles, from simulated teams and con-
2023; Chen et al., 2025b; Guo et al., 2025b). Foun-          versation scaffolds (Hong et al., 2023; Qian et al.,
dation models also reach into multimodal percep-             2023; Li et al., 2023a; Wu et al., 2023) to role
tion, multimodal generation, and robustness (Chen            specialized pipelines (Huang et al., 2023; Dong
et al., 2023b; Miao et al., 2026; Ye et al., 2024;           et al., 2024; Islam et al., 2024; Chen et al., 2023c)
Chen et al., 2023a, 2026c), yet single pass infer-           and domain specific agentic creation (Pfaff et al.,
ence remains prone to logical errors and halluci-            2026; Chen et al., 2025a); the other closes the
nations (Zhang et al., 2025; Tian et al., 2025; Ji           loop with external signals, through self correc-
et al., 2023). PairCoder is model agnostic: any of           tion and tool grounded critique (Shinn et al., 2024;
these models can play Driver or Navigator, and the           Chen et al., 2024; Madaan et al., 2023; Gou et al.,
collaboration adds reliability on top of whatever            2024), learned verifiers and repair loops (Ni et al.,
base capability the chosen model provides.                   2023; Tsai et al., 2024), and agentic software sys-
                                                             tems (Yang et al., 2024b; Wang et al., 2025). Team
2.2    Structured Data Generation
                                                             scale systems pay an order of magnitude token
A fast growing line of work, recently surveyed un-           overhead and the domain built ones are engineered
der the banner of multimodal code intelligence,              per task, while single model self correction inher-
treats programs as the medium for generating struc-          its its own blind spots. PairCoder occupies the
tured and multimodal content, where the value                intersection they leave open: the smallest collabo-
of the code lies in the artifact it renders: scien-          rative unit, two agents in the Driver and Navigator
tific figures (Belouadi et al., 2024a,b), charts and         pattern of human pair programming (Umapathy
plots (Yang et al., 2024a; Wu et al., 2024; Gal-             and Ritzhaupt, 2017; Lui and Chan, 2006; Hannay
imzyanov et al., 2024; Yang et al., 2024c; Zhao              et al., 2009; Williams et al., 2000), with toolchain
et al., 2025), vector graphics and animation (Ro-            grounded review and error triggered role switch-
driguez et al., 2025; Wu et al., 2025; Chen et al.,          ing, applied as one uniform protocol from program
2026b; Qiu et al., 2025), garment patterns (Weng             synthesis to code driven multimodal generation.
et al., 2026a), parametric CAD (Alam and Ahmed,
2024; Alrashedy et al., 2025), procedural 3D                 3     Methods
scenes (Hu et al., 2024; Sun et al., 2023; Gao et al.,
2026), front end code (Si et al., 2025; Cui, 2024),          3.1    Overview
and hardware RTL (Liu et al., 2023b; Lu et al.,              The PairCoder framework, illustrated in Fig. 2,
2024). These benchmarks score the rendered arti-             adapts pair programming to automated code gener-
fact with perceptual and geometric metrics (Wang             ation with Large Language Models (LLMs). Two
et al., 2004; Radford et al., 2021; Oquab et al.,            agents alternate between proposal and review. At
2024; Tschannen et al., 2025), yet the methods               each iteration, the Driver produces a candidate solu-
they evaluate are almost exclusively single pass             tion and the Navigator critiques it, after which the
generators. A parallel line of work synthesizes              Driver revises the code. This interaction continues
multimodal content directly with learned models              until the solution is accepted or the iteration budget
rather than programs, spanning 3D editing, texture,          is exhausted.
rigging, skeleton, and human centric video genera-              Formally, given a programming task q ∈ Q,

                                                         3
                  Perception                                                                               Perception

                  Question                                                                        Future Implications
                                                                                                  Errors       Efficiency
                  Code Correct
                                                       Environment                                Consistency
                  Code Errors                                                                     Syntax and Semantics
                                                   Code Generation
                                                       Prompt                                     Deep Optimization
                  Code Warnings          def has_close_elements(numbers: List[float],

                                                                                                  Dependencies
                                         threshold: float) -> bool:
                                             """ Check if in given list of numbers, are
                  Optimization           any two numbers closer to each other than given
                                         threshold.                                               Best Practices . . .
                                             """

                                         Generated Code
                                         def has_close_elements(numbers: List[float],
                                         threshold: float) -> bool:
                                             diff = None
                                             for i, num1 in enumerate(numbers):
                                                 for j, num2 in enumerate(numbers):
  Brain                                              if j > i:                                                              Brain
                             Driver                      diff = abs(num1 - num2)                   Navigator
                                                         if diff <= threshold:
                                                             return True
                                             return False
                       Generate
                                                                    Code Reviews                     Review Code
                        Code
                                         There is an error in the code. The function
                                         should return True if any pair of elements has a
                                         difference less than the threshold, not only the

                       End
                                         first pair found.

                                                               …                                      End Review
                    Generation


                    Action                                                                                  Action



Figure 2: The PairCoder framework: the Driver generates and revises code, the Navigator reviews it against
verification evidence, and persistent errors switch the roles.


PairCoder seeks to generate code c∗ ∈ C that maxi-                  where Idri denotes the driver instructions, Q is
mizes both correctness and quality:                                 the task description, Ct is the candidate code at
                                                                    iteration t, Ri is the review outcome at iteration i,
      c∗ = arg max P (c | q) · Quality(c, q)            (1)         and Mt−1 is the accumulated interaction history:
                 c∈C


3.2   Role Assignment                                                                      Mt = {(Ci , Ri ) | 1 ≤ i ≤ t}        (3)

At each time step, a role function ρ : A × T → R
                                                                      Concretely, on the first round the Driver is
assigns Driver and Navigator to the two agents,
                                                                    prompted with the task Q alone and emits C1 ; on
where A = {a1 , a2 } denotes the agents, T the
                                                                    every subsequent round it receives the previous
time steps, and R = {Driver, N avigator} the
                                                                    candidate Ct−1 , the Navigator’s review Rt−1 , and
available roles.
                                                                    the same verification evidence ψt−1 the Navigator
   The Driver is responsible for code construction
                                                                    saw, and is asked to return the full revised program.
and revision, whereas the Navigator checks correct-
                                                                    There is no auxiliary objective or fine tuning: the
ness, identifies deficiencies, and returns actionable
                                                                    Driver is a frozen LLM steered entirely through its
feedback. A REVISE verdict is itself an error signal,
                                                                    prompt and the role-specific system message.
and the switch is taken before the repair so that the
agent that diagnosed the fault takes the keyboard                    Navigator Agent The Navigator evaluates the
and a different agent reviews the resulting fix. The                 current candidate against concrete verification evi-
default policy switches on each error (η = 1); we                    dence and returns structured feedback:
also study switching only after η consecutive errors,
a fixed interval every k rounds, and never switching                       Rt = Fnavigator (Inav , Q, Ct , Mt−1 , ψt )          (4)
(Sec. 4.6).
Driver Agent. The Driver generates code con-                        where Inav specifies navigator-specific review
ditioned on the task specification and interaction                  guidelines and ψt is the verification evidence at-
history. As illustrated in Fig. 3, its generation pro-              tached to Ct (defined below).
cess follows:                                                          The Navigator re-reads the requirements, traces
                                                                    the candidate on concrete inputs, checks that names
           Ct = Fdriver (Idri , Q, Mt−1 )               (2)         and interfaces match the specification, and weighs

                                                                4
                                                                                            𝐼!"#
           You are the driver in
           pair programming and
                                          Question                            𝐶$ …                       𝐶( …
           your task is to write
           code...                         def has_close_elements(
                                           numbers: List[float],
 System                         Driver     threshold: float                   𝑆( = 𝑄, {𝐶, 𝑅}, 𝜌( , 𝜏(
                                           ) -> bool:
                                               """ Check if in
                                                                                          …
                                                                               𝑅$ …
            You are the navigator
            in pair Programming            given list of numbers,                                        NOERROR
            and your task is to            are any two numbers
            review the code and            closer to each other
            provide feedback...            than given threshold.
                                                                                           𝐼%&'
  System                      Navigator        """
                                                                                    Flow of Events

Figure 3: PairCoder workflow: the Driver proposes and revises, the Navigator reviews against toolchain evidence,
and persistent errors trigger a role switch.


the evidence ψt , then issues one of two verdicts:           ponents. The query Q is the original task speci-
              (                                              fication. The memory Mt is the running interac-
                 [NOERROR]       accept                      tion history (candidates, reviews, and the attached
        Rt =                                     (5)
                 REVISE(∆t ) otherwise                       evidence), kept per role and bounded in practice
                                                             only by the model’s context window. The role as-
where ∆t quotes the offending line, the require-             signment ρt records the current mapping between
ment it violates, and the specific fix. The proto-           agents and roles, and the iteration counter τt tracks
col is deliberately conservative: when ψt already            collaboration progress.
passes and the Navigator cannot point to a definite
fault it must accept with [NOERROR] rather than              Prompt construction. Each agent is a frozen
churn working code on style or vague suspicion.              chat LLM accessed through an OpenAI compat-
The interaction history is then updated as:                  ible API and carries its own message history; the
                                                             two histories together realize the shared memory
           Mt = Mt−1 ∪ {(Ct , Rt , ψt )}           (6)       Mt . The role prompt is injected as a system mes-
                                                             sage, a one line Driver or Navigator instruction
Verification Evidence ψt . Before each review                plus an optional benchmark specific hint, and is
the candidate Ct is run through the benchmark’s              re-asserted whenever the roles switch, which is the
own toolchain and the result is attached to the Nav-         Self-Mirror mechanism in implementation terms.
igator’s prompt as evidence ψt . In our implemen-            The Driver’s user message is the task Q on the first
tation ψt combines up to three signals. (1) A com-           round and the previous program, the Navigator’s
pile or execute predicate from the renderer, inter-          review, and the evidence ψt−1 on every round after;
preter, or simulator (LATEX, CadQuery, matplotlib,           the Navigator’s user message is a review instruc-
the SVG rasterizer, Blender, or an RTL simulator),           tion, the candidate program, and ψt . For image
together with the captured diagnostic on failure.            conditioned benchmarks these messages are multi-
(2) For tasks that ship a specification, the outcome         modal: the Driver is shown the target image, and
of a test the Navigator authors before it reviews, a         the Navigator is additionally shown a rendering of
test-driven check of satisfy(Ct , spec(Q)). (3) For          the current candidate next to the target. The single
image conditioned tasks, a rendering of the current          model baseline is one direct generation with the
artifact placed beside the target, so the Navigator          same task prompt and no review.
can cite concrete visual differences. The Driver re-
ceives the same ψt when it revises. This grounding           Agent Brain. As depicted in Fig. 4, each agent
is what makes the second perspective informative             uses an LLM conditioned on a role specific prompt
rather than a paraphrase of the first, and it is the         and the current shared state:
only domain specific part of the loop; everything
else is identical across the seventeen benchmarks.                       Brainrole = LLM(Prole , St )           (7)

3.3   System Components                                      where Prole encodes the responsibilities of the cur-
Shared Environment. The framework maintains                  rent role and St provides the task context, dialogue
a shared state St = ⟨Q, Mt , ρt , τt ⟩ with four com-        history, and current role assignment.

                                                         5
                                                                      Algorithm 1 PairCoder Collaboration Protocol
                                  Brain                                1: Input:    Task Q, parameters Θ = {T, k, η}
                                                                          (budget, fixed interval, error threshold)
                       Role Responsibility
                                                                       2: Output: Optimized code C ∗
                         Memory      Knowledge                         3: Initialize S0 ← ⟨Q, ∅, ρ0 , 0⟩




                                                 Storage
                                                                       4: while τ < T and not terminated do
      Perception
                                                                       5:     Driver phase with self mirror
                                                                       6:     Pdri ← SelfMirror(Driver, Idri )
                                                                       7:     Cτ ← Fdriver (Pdri , Q, Mτ −1 )
                                                                              Navigator phase with self mirror




                                                 Decision
                         Planning                                      8:
                            &                                          9:     ψτ ← Verify(Cτ ) ▷ compile/execute, opt.
        Action
                         Reasoning
                                                                          test, opt. render
                                                                      10:     Pnav ← SelfMirror(Navigator, Inav )
                                                                      11:     Rτ ← Fnavigator (Pnav , Q, Cτ , Mτ −1 , ψτ )
Figure 4: Agent brain architecture: LLM-based decision                12:     if Rτ = [NOERROR] then
making with role-specific configuration.
                                                                      13:          return Cτ
                                                                      14:     end if
                      Feedback Loop
                                                                      15:     Update shared state
                        Feedback
                                                                      16:     Mτ ← Update(Mτ −1 , Cτ , Rτ )
                                                                      17:     ρτ +1 ← CheckSwitch(ρτ , Rτ , τ )
                                                                      18:     τ ←τ +1
      Initial      Generate       Review     Final                    19: end while
      Prompt         Code          Code      Code
                                                                      20: return arg maxCi ∈Mτ Quality(Ci )


      System        Driver     Navigator                              hausted, PairCoder does not return the last attempt
                      Switch Role
                                                                      but the best one seen, arg maxCi ∈Mτ Quality(Ci ),
                                                                      where Quality orders candidates first by whether
Figure 5: Collaboration mechanism with iterative feed-                the verification evidence ψ passes, then by the
back loop between Driver and Navigator agents.
                                                                      benchmark’s continuous score when one is avail-
                                                                      able (for example structural similarity to the target),
Action Space. Each agent operates within a dis-                       and finally by recency. This makes an unresolved
crete action space Arole :                                            review debate degrade to a safe fallback rather than
                                                                      a failure.
      Adriver = {G ENERATE, R EFINE, E ND} (8)
 Anavigator = {R EVIEW, ACCEPT}                             (9)       Self-Mirror Mechanism. To preserve role con-
                                                                      sistency, each agent receives an identity aware
3.4    Collaboration Protocol                                         prompt before generation or review:
The collaboration follows an iterative refinement
                                                                      SelfMirror(ρt , Q, Mt ) = concat(
process formalized in Algorithm 1. The feedback
loop, illustrated in Fig. 5, alternates between Navi-                                           RolePrompt(ρt ), Q, Mt )
gator review and Driver revision, yielding progres-                                                                  (11)
sive improvement over successive iterations.                          where RolePrompt(ρt ) explicitly states whether the
                                                                      agent should act as Driver or Navigator. This mech-
Termination Protocol. The system terminates                           anism keeps the Driver focused on code produc-
when condition Ω(St ) is satisfied:                                   tion and revision, and keeps the Navigator focused
                                                                      on diagnosis, verification, and targeted feedback
            true if Rt = [NOERROR]
            
                                                                      throughout the interaction.
            
   Ω(St ) = true if τ ≥ T              (10)
            
            
              false otherwise                                         Implementation. Both arms use identical
                                                                      prompts and the same per benchmark extractor,
If the loop stops on [NOERROR] the accepted can-                      which recovers the program from the raw reply
didate is returned. If instead the budget T is ex-                    only to run the verifier ψ; the dialogue itself keeps

                                                                  6
the raw text. Empty or failed API responses                et al., 2023b) and RTLLM (Lu et al., 2024) (simu-
are retried with exponential backoff and do not            lation against reference testbenches). Code driven
pollute the history. Reasoning is disabled for the         artifacts: DaTikZ (Belouadi et al., 2024a) (cap-
main grid (a thinking-enabled study is reported            tion to TikZ), Plot2Code (Wu et al., 2024), Pandas-
separately), and the loop uses at most three to            PlotBench (Galimzyanov et al., 2024), and Chart-
four review rounds in the main experiments (up to          Mimic (Yang et al., 2024a) (chart or data to mat-
eight in the role-switching study of Sec. 4.6). The        plotlib), StarVector (Rodriguez et al., 2025) (im-
verifier ψ is the only per benchmark component; it         age to SVG), GenCAD-Code (Alam and Ahmed,
wraps the benchmark’s official toolchain (compiler,        2024) (image to CadQuery), 3DCodeBench (Gao
interpreter, renderer, simulator, or unit tests). We       et al., 2026) (text to Blender script), and P3D-
log prompt and completion tokens separately                Bench (Yang et al., 2026) (text to parametric 3D
for each arm, which is the basis for the token             CAD, detailed in Sec. 4.4). Each benchmark is
accounting in Sec. 4.5.                                    scored with its official metric suite: pass@1 or
                                                           execution rate where unit tests or toolchains de-
Role Switching Strategies. Our framework sup-
                                                           fine correctness, plus SSIM (Wang et al., 2004),
ports heterogeneous agent configurations in which
                                                           CLIP (Radford et al., 2021), DINO (Oquab et al.,
different LLMs can serve as Driver and Naviga-
                                                           2024), SigLIP-2 (Tschannen et al., 2025), and
tor, allowing us to leverage complementary model
                                                           Chamfer distance for rendered artifacts; full per
strengths. To optimize collaboration dynamics in
                                                           benchmark scoring and reproducibility details are
this setting, we implement two switching policies
                                                           in Appendix E.
π : St → {0, 1}:
   Fixed interval switching.                               Models and protocol. We test seven models
                                                           from three vendors: gpt-5.4-mini, gpt-5.4,
           πfixed (St ) = (τ mod k = 0)        (12)        and gpt-5.5 (OpenAI); doubao-1.5-lite
                                                           and       doubao-seed-2.0-mini               (Doubao);
ensuring balanced participation every k iterations.
                                                           deepseek-v3.2          and      deepseek-v4-flash
  Error triggered switching.
                                                           (DeepSeek), all with thinking disabled. The
                   τ                                       baseline is a single direct generation (one call per
                                              !
                  X
  πerror (St ) =       I[Ri = REVISE] ≥ η                  problem). PairCoder runs the loop of Sec. 3.2 with
                 i=τ −w                                    at most three to four review rounds: the Driver
                                           (13)            generates, the verification predicate ψ compiles,
activating when error count exceeds threshold η            executes, or renders the candidate, the Navigator
within window w.                                           reviews the code together with this evidence (and,
                                                           for visually grounded tasks, a rendering of the
4     Experiments
                                                           current artifact next to the target) and either accepts
4.1    Experimental Setup                                  with [NOERROR] or requests a concrete revision,
Benchmarks. Systematic LLM evaluation has                  and roles switch when errors persist. Both arms
been studied across many domains, from Chi-                use identical prompts and extraction; image input
nese language understanding (Zhang et al., 2023)           benchmarks are restricted to the vision capable
and strategic reasoning (Chen et al., 2025b) to            models. We log every token in both arms.
web interface comprehension (Guo et al., 2025b).
                                                           4.2   Main Results
Following this tradition, we evaluate PairCoder
on 17 public benchmarks organized by the arti-             Table 1 reports the full grid: 17 benchmarks under
fact a program must produce. Program synthe-               all seven models. On the three OpenAI models
sis: LiveCodeBench (Jain et al., 2024) (recent             PairCoder improves 44 of the 48 cells; the four
contest problems), BigCodeBench (Zhuo et al.,              exceptions are three exact ties at saturated ora-
2024) (library intensive tasks), and DS-1000 (Lai          cles (ChartMimic execution at gpt-5.4-mini, Big-
et al., 2023) (data science). Multilingual code: the       CodeBench at gpt-5.5, and StarVector rendering
C++, Java, and JavaScript splits of HumanEval-             at gpt-5.5) and one small regression (Plot2Code
X (Zheng et al., 2023). Web applications: We-              execution at gpt-5.5, 0.985 to 0.977, where
bApp1K (Cui, 2024) (React user journeys scored             the baseline already runs near the ceiling and
by hidden Jest tests). Hardware: VerilogEval (Liu          SSIM still improves, see Sec. 5). Three pat-

                                                       7
Table 1: Main results: 17 benchmarks × seven models from three vendors (thinking off), each scored with its
official metric suite. Each cell is single model → PairCoder; bold marks the better arm (↓ metrics are better when
lower; visual metrics are aggregates that score non-rendering generations as 0), green marks improvements. † marks
image-input benchmarks under vision-less models (doubao-1.5-lite, deepseek-v3.2, deepseek-v4-flash).
P3D-Bench denotes its text-to-3D / minimal-JSON track (Sec. 4.4); image-to-3D and assembly-3D are reported as a
demonstration in Table 14.

                                  gpt-5.4-      gpt-5.4        gpt-5.5      doubao-      doubao-seed-    deepseek-     deepseek-
Benchmark           Metric          mini                                    1.5-lite       2.0-mini        v3.2        v4-flash
Program synthesis
LiveCodeBench       pass@1 ↑     0.942→0.992   0.917→0.958   0.933→0.975   0.500→0.533   0.825→0.867    0.950→0.908   0.933→0.975
BigCodeBench        pass@1 ↑     0.450→0.458   0.433→0.450   0.458→0.458   0.350→0.317   0.408→0.392    0.467→0.450   0.417→0.425
DS-1000             pass@1 ↑     0.250→0.255   0.285→0.310   0.385→0.425   0.075→0.075   0.100→0.085    0.155→0.080   0.170→0.110
Multilingual
HumanEval-X C++ pass@1 ↑         0.335→0.415   0.463→0.573   0.524→0.835   0.183→0.220   0.427→0.421    0.463→0.451   0.561→0.598
HumanEval-X Java pass@1 ↑        0.341→0.384   0.451→0.500   0.396→0.561   0.250→0.256   0.335→0.335    0.500→0.463   0.494→0.463
HumanEval-X JS      pass@1 ↑     0.323→0.341   0.445→0.500   0.384→0.543   0.256→0.250   0.293→0.305    0.463→0.482   0.317→0.366
Web & Hardware
WebApp1K            pass@1 ↑     0.700→0.838   0.787→0.838   0.787→0.887   0.013→0.013   0.525→0.750    0.575→0.750   0.650→0.675
VerilogEval         pass@1 ↑     0.763→0.808   0.737→0.827   0.821→0.897   0.429→0.436   0.647→0.699    0.596→0.724   0.692→0.705
RTLLM               pass@1 ↑     0.656→0.719   0.400→0.620   0.620→0.660   0.360→0.300   0.500→0.480    0.560→0.640   0.560→0.520
Code-driven artifacts
                    compile ↑    0.500→0.633   0.717→0.967   0.783→1.000   0.550→0.850   0.567→0.800    0.683→0.917   0.633→0.733
                    SSIM ↑       0.215→0.256   0.363→0.512   0.394→0.485   0.406→0.601   0.325→0.449    0.365→0.544   0.348→0.406
DaTikZ
                    CLIP ↑       0.327→0.384   0.566→0.770   0.602→0.767   0.391→0.621   0.441→0.606    0.508→0.702   0.505→0.578
                    DINO ↑       0.303→0.338   0.530→0.698   0.554→0.730   0.259→0.391   0.383→0.545    0.465→0.596   0.445→0.519
                    exec ↑       0.841→0.962   0.962→0.977   0.985→0.977        †        0.909→0.917         †             †
Plot2Code           SSIM ↑       0.412→0.474   0.476→0.495   0.487→0.496        †        0.410→0.443         †             †
                    CLIP ↑       0.802→0.912   0.916→0.920   0.943→0.931        †        0.835→0.823         †             †
                    exec ↑       0.789→0.851   0.966→0.994   0.960→0.977        †        0.909→0.989         †             †
PandasPlotBench     SSIM ↑       0.423→0.461   0.567→0.610   0.597→0.644        †        0.491→0.534         †             †
                    CLIP ↑       0.728→0.794   0.909→0.944   0.907→0.942        †        0.846→0.922         †             †
                    exec ↑       0.967→0.967   0.917→0.983   0.983→1.000        †        0.900→0.950         †             †
ChartMimic          SSIM ↑       0.578→0.578   0.533→0.582   0.593→0.613        †        0.443→0.476         †             †
                    CLIP ↑       0.871→0.861   0.820→0.848   0.874→0.887        †        0.770→0.808         †             †
                    render ↑     0.983→1.000   0.900→1.000   1.000→1.000        †        0.983→1.000         †             †
                    SSIM ↑       0.784→0.801   0.776→0.873   0.777→0.787        †        0.758→0.770         †             †
StarVector
                    CLIP ↑       0.929→0.944   0.859→0.954   0.961→0.960        †        0.883→0.915         †             †
                    DINO ↑       0.874→0.885   0.820→0.906   0.938→0.934        †        0.793→0.819         †             †
                    exec ↑       0.900→0.983   0.867→0.983   0.917→1.000        †        0.833→0.967         †             †
GenCAD-Code
                    Chamfer ↓    0.233→0.166   0.259→0.155   0.215→0.126        †        0.308→0.212         †             †
                    exec ↑       0.200→0.783   0.433→0.783   0.383→0.417   0.167→0.383   0.200→0.533    0.333→0.633   0.600→0.533
                    SigLIP-2 ↑   0.181→0.702   0.263→0.842   0.741→0.790   0.225→0.302   0.180→0.521    0.271→0.446   0.658→0.487
3DCodeBench
                    DINO ↑       0.101→0.376   0.129→0.512   0.362→0.420   0.138→0.132   0.097→0.300    0.175→0.261   0.372→0.290
                    Chamfer ↓    4.850→2.618   4.658→1.658   2.368→2.482   4.762→3.955   4.965→3.400    5.279→3.407   2.694→3.258
                    valid ↑      0.973→1.000   0.715→0.990   0.672→0.943   0.140→0.427   0.812→0.990    0.950→0.993   0.945→1.000
                    geometry ↑   0.600→0.618   0.347→0.483   0.321→0.438   0.073→0.218   0.419→0.497    0.549→0.576   0.581→0.611
P3D-Bench           F@0.05 ↑     0.746→0.767   0.443→0.619   0.419→0.570   0.094→0.275   0.537→0.633    0.682→0.714   0.727→0.764
text-to-3D          F@0.01 ↑     0.316→0.326   0.153→0.215   0.143→0.188   0.037→0.104   0.196→0.230    0.282→0.298   0.298→0.311
(minimal-JSON)      NC ↑         0.678→0.698   0.435→0.605   0.402→0.556   0.087→0.262   0.504→0.609    0.640→0.671   0.650→0.685
                    IoU ↑        0.486→0.501   0.226→0.334   0.207→0.288   0.054→0.157   0.302→0.360    0.434→0.460   0.474→0.498
                    topology ↑   0.968→0.995   0.708→0.983   0.669→0.938   0.136→0.416   0.808→0.985    0.946→0.989   0.943→0.998




                                                                  8
terns stand out. First, the largest gains concen-            Bench (Yang et al., 2026), a benchmark in which
trate where the toolchain provides the richest sig-          the model writes a parametric construction pro-
nal: 3DCodeBench executability rises by up to 58             gram that is compiled to a mesh and scored against
points, DaTikZ compile rate by 10 to 30 points, and          ground-truth geometry. P3D-Bench spans three
WebApp1K and RTLLM each by up to 22 points.                  tracks (text-to-3D, image-to-3D, and assembly-
Second, gains often grow with model capability               3D) across several program formats (minimal-
rather than shrink: HumanEval-X C++ improves                 JSON, OpenSCAD, CadQuery, Three.js). We eval-
by 8.0, 11.0, and 31.1 points on gpt-5.4-mini,               uate the text-to-3D track primarily in the minimal-
gpt-5.4, and gpt-5.5 respectively, because a                 JSON format, the one configuration whose ground
stronger Navigator reviews more accurately and a             truth is materializable from the openly licensed
stronger Driver exploits the feedback better. Third,         Text2CAD v1.1 corpus, and additionally report exe-
on benchmarks whose baseline is already near                 cutable validity for the OpenSCAD format. For the
the ceiling the loop terminates immediately via              image-to-3D and assembly-3D tracks, whose full
[NOERROR] and safely ties instead of regressing,             evaluation sets build on the licensed Fusion 360
which is the designed behavior of the conservative           Gallery, we report a three-case in-repo demon-
review protocol.                                             stration (Appendix D, Table 14), on which Pair-
                                                             Coder improves validity, geometry, and topology
4.3   Cross-Vendor Generality                                in the CadQuery format of both tracks and ties on
The four right columns of Table 1 repeat the study           Three.js, where the baseline already compiles all
on models from two further vendors. The headline             three cases.1 The Navigator’s verification predi-
largely transfers: artifact domains with a strong            cate ψ is simply the benchmark’s own compiler
toolchain signal improve on nearly every appli-              (“does the program build a valid solid?”), and we
cable model. DaTikZ gains 10 to 30 compile                   report the official metrics: executable validity, a
points on all four models, 3DCodeBench gains 22              geometry score (Chamfer distance, F-score, nor-
to 33 executability points on three of four, We-             mal consistency and volumetric IoU, combined
bApp1K gains 2.5 to 22.5 points wherever the                 as the worst-filled composite that zeroes invalid
model can write React at all, and the vision capa-           programs), and a topology score. We run the full
ble doubao-seed-2.0-mini improves every chart,               400-case text-to-3D split with thinking disabled.
SVG, and CAD metric. The same columns also                      The P3D-Bench rows of Table 1 show the
delimit the method honestly: on benchmarks where             same headroom-tracking pattern as the rest of
the verification signal is weak (DS-1000 signature           the grid: PairCoder improves every metric on
execution without functional tests, BigCodeBench             every model with no regressions. The weak-
library calls, RTLLM compile only evidence), the             est baseline (doubao-1.5-lite, 14.0% valid)
weaker or non GPT navigators occasionally churn              gains +28.7 points of validity, +0.145 geome-
working code and small regressions appear (for ex-           try and +0.280 topology, and gpt-5.4 (71.5%)
ample DS-1000 on the DeepSeek models). This                  gains +27.5/ + 0.136/ + 0.275, while near-
is exactly the boundary in the qualitative pattern           saturated models such as gpt-5.4-mini (97.3%)
above: where the toolchain cannot adjudicate, re-            and deepseek-v4-flash (94.5%) still improve
view quality becomes model bound; where it can,              rather than regress. Crucially, on programs the
gains appear across all vendors; Appendix C (Fig-            baseline already compiles the geometry is un-
ures 19–23) shows the same tasks rendered across             changed: PairCoder intervenes only when the ar-
these models side by side. As a negative control             tifact fails to build, so coverage rises without dis-
we also ran GeoCodeBench (Li et al., 2026), a PhD            turbing correct solids, the conservative-review be-
level 3D vision benchmark on which both arms                 havior of Sec. 4.2, now measured on 3D geom-
score at the floor (about 0.02), and PairCoder ties          etry and topology. Appendix D breaks the ge-
rather than regresses.                                       ometry and topology columns into their official
                                                             sub-metrics (capped Chamfer, F-score@0.05/0.01,
4.4   Generalization to Parametric 3D Code                   normal consistency, and volumetric IoU for geom-
      (P3D-Bench)                                            etry, Table 11; no-open-edge, inverted-normal, and
To test whether the verification-grounded loop                   1
                                                                   We report P3D-Bench’s official metrics: executable va-
transfers to a target where the artifact is a 3D solid       lidity, geometry (Chamfer, F-score, normal consistency, IoU),
rather than a program output, we evaluate on P3D-            and topology.


                                                         9
non-manifold ratios for topology, Table 12): Pair-
Coder improves every sub-metric on every model,
while on the programs the single model already
compiles PairCoder keeps that program unchanged,
so its geometry is identical there and the Cham-
fer distance on that common set matches the base-
line exactly. This makes the source of the gain
unambiguous: it is coverage of non-executable pro-
grams, not re-optimization of already-valid geome-
try: PairCoder repairs programs the single model
fails to build at all into valid solids. Appendix D
additionally illustrates a vision-grounded geometry-
refinement variant that improves already-valid but
inaccurate solids (Fig. 24), for example raising F-           Figure 6: Cost versus benefit at gpt-5.4-mini: per-
score@0.05 from 0.23 to 0.95. A second program                benchmark token multiplier against primary-metric
format tells the same story: with OpenSCAD in                 gain; colours follow the families of Fig. 1.
place of minimal-JSON, PairCoder drives valid-
ity to a perfect 1.000 on all three models tested,
though the gain is smaller because the baseline is            over immediately), switch after two consecutive
already more fluent in OpenSCAD (Appendix D,                  errors, and a fixed interval switch every two rounds
Table 13).                                                    regardless of the signal. Figure 7 reports the official
                                                              metric and the token cost for each policy.
4.5   Token Economics
We log every token in both arms. Across the full                              1.0
grid PairCoder consumes 2.9× to 9.2× the to-                                  0.9
kens of the single model baseline depending on
                                                                              0.8
                                                            official metric




the benchmark (for example 2.9× on GenCAD-
Code, 3.4× on StarVector, 4.0× on WebApp1K,                                   0.7      DaTikZ (compile)
                                                                                       Plot2Code (exec)
5.9× on ChartMimic, 6.9× on DaTikZ, 7.9× on                                   0.6      HumanEval-X C++ (pass@1)
RTLLM where simulation failures trigger the most                                       HumanEval-X Java (pass@1)
revision rounds, and 9.2× on Plot2Code), with an                              0.5
overall ratio of 7.4× over 138M logged tokens (the                            0.4
per benchmark breakdown is in Table 10). This                                 0.3
is the cost of the review rounds themselves: tasks
                                                                                                 3.45M
accepted in the first round cost roughly 2× a sin-                                                            3.07M     3.12M
                                                                               3     2.87M
                                                        PairCoder
                                                         tokens




gle pass (one generation plus one review), and the
multiplier grows only when the Navigator actually                              2
finds errors, that is, exactly when the additional                             1
spend converts into accuracy (Fig. 6). Team style                              0
multi agent frameworks reported in prior work con-                                  no switch each error     after 2     fixed
                                                                                                (ours)       errors    interval
sume an order of magnitude more than a single call;
while we do not re-run those systems on our bench-            Figure 7: Role-switching policy at gpt-5.4-mini: offi-
marks, PairCoder’s measured 3 to 9 times envelope             cial metric (top) and PairCoder token cost (bottom) for
is well below that order of magnitude overhead.               four policies; see Sec. 4.6.

4.6   Role Switching Analysis                                   Switching on each error is the best or tied-
The error triggered role switch is a design choice;          best policy on all four benchmarks, and never the
here we test it directly at gpt-5.4-mini on four             worst. The effect is small where the loop is short
benchmarks, against three alternatives at matched            (DaTikZ saturates near a perfect compile rate un-
budget: no switch (the Driver keeps the keyboard,            der every policy) but clear where iteration mat-
the Navigator always reviews), switch on each er-            ters: on HumanEval-X C++, switching immedi-
ror (the Navigator that just flagged an error takes          ately reaches 0.427 while delaying the switch to

                                                       10
two consecutive errors drops to 0.390, the same as            2024), ChartMimic (Yang et al., 2024a): image
never switching, because the agent that diagnosed             or data to matplotlib), vector graphics (StarVec-
the fault is the one best positioned to fix it, and           tor (Rodriguez et al., 2025): image to SVG), para-
keeping it in the reviewer seat wastes that diagno-           metric CAD (GenCAD-Code (Alam and Ahmed,
sis. No switch and the fixed interval are competitive         2024): image to CadQuery), and 3D scenes
but consistently a step behind. We therefore adopt            (3DCodeBench (Gao et al., 2026): text to Blender
switch on each error as the default in all other ex-          script). In each domain the Navigator’s review is
periments. This updates the earlier preference for            grounded in the same verification predicates ψi as
a two error threshold, which we had observed on               in Sec. 3.2: the candidate program is compiled,
Python only; on the broader benchmark set imme-               executed, or rendered, and the result (including
diate switching is the more reliable choice.                  the rendered image for multimodal tasks) is sup-
                                                              plied to the Navigator as review evidence before
4.7    Effect of Reasoning Effort                             it issues [NOERROR] or a concrete revision request.
The main results disable model thinking. We addi-             We report each benchmark’s official metric suite,
tionally test whether enabling reasoning changes              namely execution or compile rate plus visual simi-
the picture, on the three Python benchmarks                   larity (SSIM (Wang et al., 2004), CLIP (Radford
where the no-thinking gains are smallest, at                  et al., 2021), DINO (Oquab et al., 2024), SigLIP-
gpt-5.4-mini. Enabling high reasoning effort                  2 (Tschannen et al., 2025)) and geometric fidelity
raises both arms’ baselines, as expected, and Pair-           (Chamfer distance), rather than execution success
Coder still helps where the verification signal is in-        alone.
formative: on BigCodeBench the gain grows from                Table 2:    Multimodal code generation with
+0.8 points (no thinking, 0.450 to 0.458) to +5.0             gpt-5.4-mini (thinking off); each cell is single
points (high, 0.425 to 0.475), because a stronger             model → PairCoder (↓ better when lower).
Driver produces candidates whose remaining errors
                                                              Benchmark               Metric                          single → PairCoder
are more often caught by the Navigator’s doctest
                                                                                      compile rate ↑                      0.500 → 0.633
                                                              DaTikZ (60)
evidence. On DS-1000, whose only signal is that                                       SSIM / CLIP / DINO ↑       .215/.327/.303 → .256/.384/.338

a function executes on its signature (no functional           Plot2Code (132)
                                                                                      execution rate ↑
                                                                                      SSIM / CLIP ↑
                                                                                                                         0.841 → 0.962
                                                                                                                     .412/.802 → .474/.912
tests), thinking lifts the baseline from 0.250 to                                     execution rate ↑                   0.789 → 0.851
                                                              PandasPlotBench (175)
0.310 but PairCoder neither helps nor hurts beyond                                    SSIM / CLIP ↑                  .423/.728 → .461/.794
                                                                                      execution rate ↑                   0.967 → 0.967
noise (0.310 to 0.300), consistent with the quali-            ChartMimic (60)
                                                                                      SSIM / CLIP ↑                  .578/.871 → .578/.861
tative pattern above: where the toolchain cannot              StarVector (60)
                                                                                      render rate ↑                       0.983 → 1.000
                                                                                      SSIM / CLIP / DINO ↑       .784/.929/.874 → .801/.944/.885
adjudicate correctness, extra reasoning improves
                                                                                      execution rate ↑                   0.900 → 0.983
                                                              GenCAD-Code (60)
the Driver but gives the Navigator nothing new to                                     Chamfer (aggregate) ↓              0.233 → 0.166

verify. Reasoning roughly triples per-call token                                      executability ↑                    0.200 → 0.783
                                                              3DCodeBench (60)        SigLIP-2 / DINO (agg.) ↑       .181/.101 → .702/.376
cost, so we use it only for this analysis and report                                  Chamfer (aggregate) ↓               4.85 → 2.62

the main grid with thinking disabled. (We omit
hardware RTL from this comparison: at high effort
the small model spends most of its budget on rea-             Quantitative results. Table 2 summarizes the
soning and frequently truncates the actual Verilog            gpt-5.4-mini results. PairCoder improves every
module, an artifact of the model rather than of the           official metric on six of the seven benchmarks: not
collaboration.)                                               only are far more generated programs executable,
                                                              the artifacts they produce are also closer to the ref-
5     Code-Driven Multimodal Generation                       erence in pixel structure (SSIM), semantics (CLIP,
                                                              SigLIP-2, DINO), and geometry (Chamfer). The
The central claim of this work is that pair pro-              only exception is ChartMimic, where the baseline
gramming turns code driven creation, not just                 already executes near the ceiling (about 0.97 to 1.0)
program synthesis, into a verified process. We                and the loop ties; notably, at gpt-5.4 the same
test it on seven public benchmarks whose outputs              benchmark turns positive (execution 0.92 to 0.98,
are executable artifacts in other modalities: sci-            SSIM 0.53 to 0.58), confirming that the tie reflects
entific figures (DaTikZ (Belouadi et al., 2024a):             a saturated oracle rather than a limit of the collabo-
caption to TikZ/LATEX), charts (Plot2Code (Wu                 ration. These gains transfer across vendors: with
et al., 2024), PandasPlotBench (Galimzyanov et al.,           the volcano engine models, DaTikZ improves on

                                                         11
           (a) Plot2Code: image to matplotlib                          (b) PandasPlotBench: data to matplotlib




           (c) ChartMimic: chart to matplotlib                             (d) StarVector: image to SVG




         (e) GenCAD-Code: image to CadQuery                              (f) 3DCodeBench: text to Blender

Figure 8: Qualitative comparison across six artifact domains: target/reference (left), single model (middle),
PairCoder (right).


all four (doubao-1.5-lite +30.0, doubao-seed-2.0-              suites (Tables 3–9); Appendix A walks through
mini +23.3, deepseek-v3.2 +23.4, deepseek-v4-                  complete multi-round traces (Cases A.1–A.4).
flash +10.0 compile points), 3DCodeBench gains
                                                               Cost. The collaboration costs about 3 to 9 times
+21.6/+33.3/+30.0 executability points, and the
                                                               the tokens of single model inference in these do-
multimodal doubao-seed-2.0-mini improves nearly
                                                               mains (for example, 2.9× on GenCAD-Code, 3.4×
every chart, SVG, and CAD metric (for example,
                                                               on StarVector, 5.9× on ChartMimic, 6.9× on
PandasPlotBench execution 0.91 to 0.99).
                                                               DaTikZ, and 9.2× on Plot2Code, measured per
Qualitative comparison. Figure 8 illustrates the               arm), with an overall ratio of about 7× across
dominant failure repair pattern behind these num-              the full grid; review rounds terminate early via
bers. Single model generations in these domains                [NOERROR] on the majority of tasks that succeed
frequently die at the toolchain boundary: LATEX that           immediately.
does not compile, matplotlib scripts that raise ex-
                                                               6   Conclusion
ceptions, Blender scripts that produce no geometry.
PairCoder converts a large fraction of these hard              Code is increasingly how language models make
failures because the Navigator receives the concrete           things, from figures, charts, and vector graphics
compiler or runtime error (and, for image condi-               to CAD parts, 3D scenes, and circuits, and in this
tioned tasks, a rendering of the current candidate             regime the decisive failures occur at the bound-
next to the target) and returns an actionable critique;        ary between the program and the toolchain that
after the error triggered role switch, the agent that          renders it. We presented PairCoder, a minimal
diagnosed the fault repairs it directly. When the              two agent framework that closes this boundary: a
baseline already renders, the same visual review               Driver writes the program, a Navigator reviews
instead nudges layout, proportions, and styling to-            it with verdicts grounded in compiler, execution,
ward the target, which is reflected in the consistent          and rendering evidence, and error triggered role
SSIM, CLIP, and DINO gains. Appendix B ex-                     switching keeps the collaboration moving. Across
pands this into one page per benchmark, with gal-              17 public benchmarks, seven models, and three
leries (Figures 12–18) and the full measured metric            vendors, PairCoder improves essentially every ver-

                                                          12
ifiable benchmark on its entire official metric suite,           Huang, et al. 2023. Qwen technical report. arXiv
covering executability, visual similarity, and geo-              preprint arXiv:2309.16609.
metric fidelity alike, while remaining within 2.9 to           Jonas Belouadi, Anne Lauscher, and Steffen Eger.
9.2 times a single pass in cost (about 7 times over-             2024a. Automatikz: Text-guided synthesis of sci-
all), far below team simulation systems; on classi-              entific vector graphics with tikz. In The Twelfth Inter-
cal synthesis it remains competitive with and often              national Conference on Learning Representations.
improves strong single model inference (for exam-              Jonas Belouadi, Simone Paolo Ponzetto, and Steffen
ple LiveCodeBench pass@1 from 0.94 to 0.99).                     Eger. 2024b. Detikzify: Synthesizing graphics pro-
The broader lesson is a qualitative pattern for col-             grams for scientific figures and sketches with tikz. In
                                                                 Advances in Neural Information Processing Systems,
laborative generation: gains concentrate where the               volume 37, pages 85074–85108. Curran Associates,
artifact is verifiable and the baseline leaves head-             Inc.
room, and fade where the oracle is weak. Wherever
a trustworthy toolchain can be made to speak, and              Junhao Chen, Mingjin Chen, Jianjin Xu, Xiang Li, Junt-
                                                                 ing Dong, Mingze Sun, Puhua Jiang, Hongxiang Li,
in code driven creation it almost always can, pair               Yuhang Yang, Hao Zhao, Xiao-Xiao Long, and Ruqi
programming converts that signal into reliably bet-              Huang. 2026a. Dancetogether: Generating interac-
ter artifacts, making it a practical recipe for trust-           tive multi-person video without identity drifting. In
worthy code mediated generation of structured data               The Fourteenth International Conference on Learn-
                                                                 ing Representations.
and multimodal content wherever such an oracle
exists.                                                        Junhao Chen, Kejun Gao, Yuehan Cui, Mingze Sun,
                                                                 Mingjin Chen, Shaohui Wang, Xiaoxiao Long, Fei
Limitations                                                      Ma, Qi Tian, Hao Zhao, and Ruqi Huang. 2026b.
                                                                 Lottiegpt: Tokenizing vector animation for autore-
While PairCoder improves code generation accu-                   gressive generation. In Proceedings of the IEEE/CVF
                                                                 Conference on Computer Vision and Pattern Recog-
racy, it still requires substantially more tokens and            nition (CVPR), pages 31639–31651.
wall clock time than single model inference, with
about seven times the cost per task on average in              Junhao Chen, Xiang Li, Xiaojun Ye, Chao Li, Zhaoxin
                                                                 Fan, and Hao Zhao. 2025a. Idea23d: Collaborative
our experiments (2.9 to 9.2 times depending on
                                                                 lmm agents enable 3d model generation from inter-
the benchmark). Although one PairCoder run can                   leaved multimodal inputs. In Proceedings of the 31st
reach accuracy levels that otherwise require several             International Conference on Computational Linguis-
retries, the added latency and token budget still                tics, pages 4149–4166.
constrain practical deployment. Reducing this cost             Junhao Chen, Peng Rong, Jingbo Sun, Chao Li, Xi-
while preserving accuracy remains an important                   ang Li, and Hongwu Lv. 2023a. Soulstyler: Using
direction for future work.                                       large language model to guide image style transfer
                                                                 for target object. arXiv preprint arXiv:2311.13562.
                                                               Junhao Chen, Jingbo Sun, Xiang Li, Haidong Xin,
References                                                       Yuhao Xue, Yibin Xu, and Hao Zhao. 2025b.
                                                                 LLMsPark: A benchmark for evaluating large lan-
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama
                                                                 guage models in strategic gaming contexts. In Find-
  Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
                                                                 ings of the Association for Computational Linguis-
  Diogo Almeida, Janko Altenschmidt, Sam Altman,
                                                                 tics: EMNLP 2025, pages 182–194, Suzhou, China.
  Shyamal Anadkat, et al. 2023. Gpt-4 technical report.
                                                                 Association for Computational Linguistics.
  arXiv preprint arXiv:2303.08774.
                                                               Junhao Chen, Xiaojun Ye, Jingbo Sun, and Chao Li.
Md Ferdous Alam and Faez Ahmed. 2024. Gencad:                    2023b. Towards energy-efficient sentiment classifica-
 Image-conditioned computer-aided design generation              tion with spiking neural networks. In International
 with transformer-based contrastive representation and           Conference on Artificial Neural Networks, pages 518–
 diffusion priors. arXiv preprint arXiv:2409.16294.              529. Springer.
Kamel Alrashedy, Pradyumna Tambwekar, Zulfiqar                 Junhao Chen, Boran Zhang, Mingjin Chen, Henghaofan
  Zaidi, Megan Langwasser, Wei Xu, and Matthew                   Zhang, Saining Zhang, Congcong Zhu, Hao Zhao,
  Gombolay. 2025. Generating cad code with vision-               Ruqi Huang, Zhihao Li, and Yufei Wang. 2026c. One
  language models for 3d designs. In The Thirteenth              video, one world: Turning monocular video into phys-
  International Conference on Learning Representa-               ical 4d scenes. Preprint, arXiv:2606.31388.
  tions.
                                                               Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang,           Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-
   Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei              plan, Harri Edwards, Yuri Burda, Nicholas Joseph,


                                                          13
  Greg Brockman, et al. 2021. Evaluating large                     models for converting image-to-web. In Findings of
  language models trained on code. arXiv preprint                  the Association for Computational Linguistics: ACL
  arXiv:2107.03374.                                                2025, pages 6449–6466, Vienna, Austria. Associa-
                                                                   tion for Computational Linguistics.
Mingjin Chen, Junhao Chen, Zhaoxin Fan, Yujian Lee,
  Zichen Dang, Lili Wang, Yawen Cui, Lap-Pui Chau,               Jo E Hannay, Tore Dybå, Erik Arisholm, and Dag IK
  and Yi Wang. 2026d. Hvg-3d: Bridging real and                     Sjøberg. 2009. The effectiveness of pair program-
  simulation domains for 3d-conditional hand-object                 ming: A meta-analysis. Information and software
  interaction video synthesis. In Proceedings of the                technology, 51(7):1110–1122.
  IEEE/CVF Conference on Computer Vision and Pat-
  tern Recognition (CVPR), pages 15986–15997.                    Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng
Mingjin Chen, Junhao Chen, Huan-ang Gao, Xiaoxue                    Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven
  Chen, Zhaoxin Fan, and Hao Zhao. 2026e. Ultraman:                 Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. 2023.
  ultra-fast and high-resolution texture generation for             Metagpt: Meta programming for multi-agent collabo-
  3d human reconstruction from a single image. Ma-                  rative framework. arXiv preprint arXiv:2308.00352.
  chine Vision and Applications, 37(2):24.
                                                                 Ziniu Hu, Ahmet Iscen, Aashi Jain, Thomas Kipf,
Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang,                   Yisong Yue, David A. Ross, Cordelia Schmid, and
 Chenfei Yuan, Chi-Min Chan, Heyang Yu, Yaxi Lu,                   Alireza Fathi. 2024. Scenecraft: An llm agent for
 Yi-Hsin Hung, Chen Qian, et al. 2023c. Agentverse:                synthesizing 3d scenes as blender code. In Interna-
 Facilitating multi-agent collaboration and exploring              tional Conference on Machine Learning.
 emergent behaviors. In The Twelfth International
 Conference on Learning Representations.                         Dong Huang, Qingwen Bu, Jie M Zhang, Michael Luck,
                                                                   and Heming Cui. 2023. Agentcoder: Multi-agent-
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and                   based code generation with iterative testing and opti-
  Denny Zhou. 2024. Teaching large language models                 misation. arXiv preprint arXiv:2312.13010.
  to self-debug. In The Twelfth International Confer-
  ence on Learning Representations.                              Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Day-
                                                                   iheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
Yi Cui. 2024. Webapp1k: A practical code-generation                Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder
   benchmark for web app development. arXiv preprint               technical report. arXiv preprint arXiv:2409.12186.
   arXiv:2408.00019.

Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li. 2024.                Md Ashraful Islam, Mohammed Eunus Ali, and
  Self-collaboration code generation via chatgpt. ACM             Md Rizwan Parvez. 2024. Mapcoder: Multi-agent
  Transactions on Software Engineering and Method-                code generation for competitive problem solving. In
  ology, 33(7):1–38.                                              Proceedings of the 62nd Annual Meeting of the As-
                                                                  sociation for Computational Linguistics (Volume 1:
Timur Galimzyanov, Sergey Titov, Yaroslav Golubev,                Long Papers), pages 4912–4944.
  and Egor Bogomolov. 2024. Drawing pandas: A
  benchmark for llms in generating plotting code.                Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia
  arXiv preprint arXiv:2412.02764.                                 Yan, Tianjun Zhang, Sida Wang, Armando Solar-
                                                                   Lezama, Koushik Sen, and Ion Stoica. 2024. Live-
Yipeng Gao, Lei Shu, Genzhi Ye, Xi Xiong, Ameesh                   codebench: Holistic and contamination free eval-
  Makadia, Meiqi Guo, Laurent Itti, and Jindong                    uation of large language models for code. arXiv
  Chen. 2026. 3dcodebench: Benchmarking agentic                    preprint arXiv:2403.07974.
  procedural 3d modeling via code. arXiv preprint
  arXiv:2606.01057.                                              Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan
                                                                   Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea
Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,                 Madotto, and Pascale Fung. 2023. Survey of hal-
  Yujiu Yang, Nan Duan, and Weizhu Chen. 2024.                     lucination in natural language generation. ACM com-
  Critic: Large language models can self-correct with              puting surveys, 55(12):1–38.
  tool-interactive critiquing. In The Twelfth Interna-
  tional Conference on Learning Representations.
                                                                 Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim,
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song,                 and Sunghun Kim. 2024. A survey on large lan-
  Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma,                   guage models for code generation. arXiv preprint
  Peiyi Wang, Xiao Bi, et al. 2025a. Deepseek-r1: In-              arXiv:2406.00515.
  centivizing reasoning capability in llms via reinforce-
  ment learning. arXiv preprint arXiv:2501.12948.                Carlos E Jimenez, John Yang, Alexander Wettig,
                                                                   Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
Hongcheng Guo, Wei Zhang, Junhao Chen, Yaonan Gu,                  Narasimhan. 2024. Swe-bench: Can language mod-
  Jian Yang, Junjia Du, Shaosheng Cao, Binyuan Hui,                els resolve real-world github issues? In International
  Tianyu Liu, Jianxin Ma, Chang Zhou, and Zhoujun                  Conference on Learning Representations, volume
  Li. 2025b. IW-bench: Evaluating large multimodal                 2024, pages 54107–54157.


                                                            14
Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang,               International Journal of Human-computer studies,
  Ruiqi Zhong, Luke Zettlemoyer, Wen-tau Yih, Daniel             64(9):915–925.
  Fried, Sida Wang, and Tao Yu. 2023. Ds-1000: A
  natural and reliable benchmark for data science code         Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
  generation. In International Conference on Machine            Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
  Learning, pages 18319–18345.                                  Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
                                                                et al. 2023. Self-refine: Iterative refinement with
Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii                   self-feedback. In Advances in Neural Information
  Khizbullin, and Bernard Ghanem. 2023a. Camel:                 Processing Systems, volume 36.
  Communicative agents for “mind” exploration of
  large language model society. In Advances in Neural          Xingyu Miao, Junting Dong, Qin Zhao, Yuhang Yang,
  Information Processing Systems, volume 36.                     Junhao Chen, and Yang Long. 2026. From frames
                                                                 to sequences: Temporally consistent human-centric
Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas                dense prediction. Preprint, arXiv:2602.01661.
  Muennighoff, Denis Kocetkov, Chenghao Mou, Marc
  Marone, Christopher Akiki, Jia Li, Jenny Chim, et al.        Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoy-
  2023b. Starcoder: may the source be with you!                  anov, Wen-tau Yih, Sida Wang, and Xi Victoria Lin.
  arXiv preprint arXiv:2305.06161.                               2023. Lever: Learning to verify language-to-code
                                                                 generation with execution. In International Confer-
Wenyi Li, Renkai Luo, Yue Yu, Huan-ang Gao, Mingju               ence on Machine Learning, pages 26106–26128.
  Gao, Li Yuan, Chaoyou Fu, and Hao Zhao. 2026.
  Benchmarking phd-level coding in 3d geometric com-           Erik Nijkamp, Hiroaki Hayashi, Caiming Xiong, Sil-
  puter vision. In Proceedings of the IEEE/CVF Con-              vio Savarese, and Yingbo Zhou. 2023. Codegen2:
  ference on Computer Vision and Pattern Recognition,            Lessons for training llms on programming and natu-
  pages 30974–30985.                                             ral languages. arXiv preprint arXiv:2305.02309.

Zongjie Li, Chaozheng Wang, Zhibo Liu, Haoxuan                 OpenAI. 2023. GPT-3.5 documentation. https:
  Wang, Dong Chen, Shuai Wang, and Cuiyun Gao.                   //platform.openai.com/docs/models/gpt-3-5.
  2023c. Cctest: Testing and repairing code comple-              Accessed: October 21, 2023.
  tion systems. In 2023 IEEE/ACM 45th International
  Conference on Software Engineering (ICSE), pages             Maxime Oquab, Timothée Darcet, Théo Moutakanni,
  1238–1250. IEEE.                                              Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fer-
                                                                nandez, Daniel Haziza, Francisco Massa, Alaaeldin
Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang,                   El-Nouby, et al. 2024. Dinov2: Learning robust vi-
  Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi                sual features without supervision. Transactions on
  Deng, Chenyu Zhang, Chong Ruan, et al. 2024.                  Machine Learning Research.
  Deepseek-v3 technical report.   arXiv preprint
  arXiv:2412.19437.                                            Nicholas Pfaff, Thomas Cohn, Sergey Zakharov, Rick
                                                                 Cory, and Russ Tedrake. 2026. Scenesmith: Agentic
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and                  generation of simulation-ready indoor scenes. arXiv
   Lingming Zhang. 2023a. Is your code generated by              preprint arXiv:2602.09153.
   chatgpt really correct? rigorous evaluation of large
   language models for code generation. Advances in            Chen Qian, Xin Cong, Cheng Yang, Weize Chen,
   neural information processing systems, 36:21558–              Yusheng Su, Juyuan Xu, Zhiyuan Liu, and Maosong
   21572.                                                        Sun. 2023. Communicative agents for software de-
                                                                 velopment. arXiv preprint arXiv:2307.07924, 6.
Mingjie Liu, Nathaniel Pinckney, Brucek Khailany, and
  Haoxing Ren. 2023b. Verilogeval: Evaluating large            Zeju Qiu, Weiyang Liu, Haiwen Feng, Zhen Liu, Tim Z.
  language models for verilog code generation. In 2023           Xiao, Katherine M. Collins, Joshua B. Tenenbaum,
  IEEE/ACM International Conference on Computer                  Adrian Weller, Michael J. Black, and Bernhard
  Aided Design (ICCAD), pages 1–8.                               Schölkopf. 2025. Can large language models un-
                                                                 derstand symbolic graphics programs? In The Thir-
Anton Lozhkov, Raymond Li, Loubna Ben Allal, Fed-                teenth International Conference on Learning Repre-
  erico Cassano, Joel Lamy-Poirier, Nouamane Tazi,               sentations.
  Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei,
  et al. 2024. Starcoder 2 and the stack v2: The next          Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
  generation. arXiv preprint arXiv:2402.19173.                   Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sas-
                                                                 try, Amanda Askell, Pamela Mishkin, Jack Clark,
Yao Lu, Shang Liu, Qijun Zhang, and Zhiyao Xie. 2024.            et al. 2021. Learning transferable visual models from
  Rtllm: An open-source benchmark for design rtl gen-            natural language supervision. In International Con-
  eration with large language model. In 2024 29th Asia           ference on Machine Learning, pages 8748–8763.
  and South Pacific Design Automation Conference
  (ASP-DAC), pages 722–727.                                    Juan A Rodriguez, Abhay Puri, Shubham Agarwal, Is-
                                                                 sam H Laradji, Pau Rodriguez, Sai Rajeswar, David
Kim Man Lui and Keith CC Chan. 2006. Pair program-               Vazquez, Christopher Pal, and Marco Pedersoli. 2025.
  ming productivity: Novice–novice vs. expert–expert.            Starvector: Generating scalable vector graphics code


                                                          15
  from images and text. In Proceedings of the Com-             Michael Tschannen, Alexey Gritsenko, Xiao Wang,
  puter Vision and Pattern Recognition Conference,               Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin,
  pages 16175–16186.                                             Nikhil Parthasarathy, Talfan Evans, Lucas Beyer,
                                                                Ye Xia, Basil Mustafa, et al. 2025. Siglip 2: Multilin-
Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten           gual vision-language encoders with improved seman-
  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,               tic understanding, localization, and dense features.
  Jingyu Liu, Romain Sauvestre, Tal Remez, et al. 2023.          arXiv preprint arXiv:2502.14786.
  Code llama: Open foundation models for code. arXiv
  preprint arXiv:2308.12950.                                   Karthikeyan Umapathy and Albert D Ritzhaupt. 2017.
                                                                 A meta-analysis of pair-programming in computer
Noah Shinn, Federico Cassano, Ashwin Gopinath,                   programming courses: Implications for educational
  Karthik Narasimhan, and Shunyu Yao. 2024. Re-                  practice. ACM Transactions on Computing Educa-
  flexion: Language agents with verbal reinforcement             tion (TOCE), 17(4):1–13.
  learning. Advances in Neural Information Process-
  ing Systems, 36.                                             Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu,
                                                                 Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi
Chenglei Si, Yanzhe Zhang, Ryan Li, Zhengyuan Yang,              Song, Bowen Li, Jaskirat Singh, et al. 2025. Open-
  Ruibo Liu, and Diyi Yang. 2025. Design2code:                   hands: An open platform for ai software developers
  Benchmarking multimodal code generation for au-                as generalist agents. In The Thirteenth International
  tomated front-end engineering. In Proceedings of               Conference on Learning Representations.
  the 2025 Conference of the Nations of the Americas
  Chapter of the Association for Computational Lin-            Zhou Wang, Alan C. Bovik, Hamid R. Sheikh, and
  guistics: Human Language Technologies (Volume 1:               Eero P. Simoncelli. 2004. Image quality assessment:
  Long Papers), pages 3956–3974.                                 From error visibility to structural similarity. IEEE
                                                                 Transactions on Image Processing, 13(4):600–612.
Chunyi Sun, Junlin Han, Weijian Deng, Xinlong Wang,
  Zishan Qin, and Stephen Gould. 2023. 3d-gpt: Proce-          Fangsheng Weng, Junhao Chen, Xiang Li, Jie Qin,
  dural 3d modeling with large language models. arXiv            Hanzhong Guo, ShaochunHao, and Xiaoguang Han.
  preprint arXiv:2310.12945.                                     2026a. GarmentGPT: Compositional garment pat-
                                                                 tern generation via discrete latent tokenization. In
Mingze Sun, Junhao Chen, Junting Dong, Yurun Chen,               The Fourteenth International Conference on Learn-
  Xinyu Jiang, Shiwei Mao, Puhua Jiang, Jingbo                   ing Representations.
  Wang, Bo Dai, and Ruqi Huang. 2025. Drive:
                                                               Jiawei Weng, Saining Zhang, Zhenxin Diao, Peishuo
  Diffusion-based rigging empowers generation of ver-
                                                                  Li, Henghaofan Zhang, Junhao Chen, and Hao Zhao.
  satile and expressive characters. In Proceedings of
                                                                  2026b. Feedforward 3d editing learns from semantic-
  the IEEE/CVF Conference on Computer Vision and
                                                                  part transformation. Preprint, arXiv:2605.27351.
  Pattern Recognition (CVPR), pages 21170–21180.
                                                               Laurie Williams, Robert R Kessler, Ward Cunningham,
Mingze Sun, Cheng Zeng, Jiansong Pei, Junhao Chen,               and Ron Jeffries. 2000. Strengthening the case for
  Chaoyue Song, Shaohui Wang, Tianyuan Chang,                    pair programming. IEEE software, 17(4):19–25.
  Bin Huang, Zijiao Zeng, and Ruqi Huang. 2026.
  Animator-centric skeleton generation on objects with         Chengyue Wu, Yixiao Ge, Qiushan Guo, Jiahao Wang,
  fine-grained details. In Proceedings of the IEEE/CVF           Zhixuan Liang, Zeyu Lu, Ying Shan, and Ping Luo.
  Conference on Computer Vision and Pattern Recog-               2024. Plot2code: A comprehensive benchmark for
  nition (CVPR), pages 17336–17345.                              evaluating multi-modal large language models in
                                                                 code generation from scientific plots. arXiv preprint
Yuchen Tian, Weixiang Yan, Qian Yang, Xuandong                   arXiv:2405.07990.
  Zhao, Qian Chen, Wen Wang, Ziyang Luo, Lei Ma,
  and Dawn Song. 2025. Codehalu: Investigating code            Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu,
  hallucinations in llms via execution-based verifica-           Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang,
  tion. In Proceedings of the AAAI Conference on Arti-           Shaokun Zhang, Jiale Liu, et al. 2023. Autogen:
  ficial Intelligence, volume 39, pages 25300–25308.             Enabling next-gen llm applications via multi-agent
                                                                 conversation. arXiv preprint arXiv:2308.08155.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  bert, Amjad Almahairi, Yasmine Babaei, Nikolay               Ronghuan Wu, Wanchao Su, and Jing Liao. 2025.
  Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti             Chat2svg: Vector graphics generation with large lan-
  Bhosale, et al. 2023. Llama 2: Open founda-                    guage models and image diffusion models. In Pro-
  tion and fine-tuned chat models. arXiv preprint                ceedings of the IEEE/CVF Conference on Computer
  arXiv:2307.09288.                                              Vision and Pattern Recognition.

YunDa Tsai, Mingjie Liu, and Haoxing Ren. 2024. Rtl-           An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  fixer: Automatically fixing rtl syntax errors with             Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,
  large language model. In Proceedings of the 61st               Chengen Huang, Chenxu Lv, et al. 2025. Qwen3
  ACM/IEEE Design Automation Conference.                         technical report. arXiv preprint arXiv:2505.09388.


                                                          16
Cheng Yang, Chufan Shi, Yaxin Liu, Bo Shui, Jun-               Yusuf, Haolan Zhan, Junda He, Indraneil Paul, et al.
  jie Wang, Mohan Jing, Linran Xu, Xinyu Zhu, Si-              2024. Bigcodebench: Benchmarking code genera-
  heng Li, Yuxiang Zhang, et al. 2024a. Chartmimic:            tion with diverse function calls and complex instruc-
  Evaluating lmm’s cross-modal reasoning capabil-              tions. arXiv preprint arXiv:2406.15877.
  ity via chart-to-code generation. arXiv preprint
  arXiv:2406.09961.
John Yang, Carlos Jimenez, Alexander Wettig, Kilian
  Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir
  Press. 2024b. Swe-agent: Agent-computer interfaces
  enable automated software engineering. Advances in
  Neural Information Processing Systems, 37:50528–
  50652.
Yikang Yang, Zhanpeng Hu, Youtian Lin, Mengqi Zhou,
  Jingxi Xu, Feihu Zhang, Jiaheng Liu, and Yao Yao.
  2026. P3d-bench: Benchmarking mllms for para-
  metric 3d generation and structural reasoning. arXiv
  preprint arXiv:2606.11152.
Zhiyu Yang, Zihan Zhou, Shuo Wang, Xin Cong,
  Xu Han, Yukun Yan, Zhenghao Liu, Zhixing Tan,
  Pengyuan Liu, Dong Yu, et al. 2024c. Matplota-
  gent: Method and evaluation for llm-based agentic
  scientific data visualization. In Findings of the As-
  sociation for Computational Linguistics: ACL 2024,
  pages 11789–11804.
Xiaojun Ye, Junhao Chen, Xiang Li, Haidong Xin, Chao
  Li, Sheng Zhou, and Jiajun Bu. 2024. Mmad: Multi-
  modal movie audio description. In Proceedings of
  the 2024 Joint International Conference on Compu-
  tational Linguistics, Language Resources and Evalu-
  ation (LREC-COLING 2024), pages 11415–11428.
Baoli Zhang, Haining Xie, Pengfan Du, Junhao Chen,
  Pengfei Cao, Yubo Chen, Shengping Liu, Kang Liu,
  and Jun Zhao. 2023. Zhujiu: A multi-dimensional,
  multi-faceted chinese benchmark for large language
  models. In Proceedings of the 2023 Conference on
  Empirical Methods in Natural Language Processing:
  System Demonstrations, pages 479–494.
Ziyao Zhang, Chong Wang, Yanlin Wang, Ensheng Shi,
  Yuchi Ma, Wanjun Zhong, Jiachi Chen, Mingzhi Mao,
  and Zibin Zheng. 2025. Llm hallucinations in prac-
  tical code generation: Phenomena, mechanism, and
  mitigation. Proceedings of the ACM on Software
  Engineering, 2(ISSTA):481–503.
Xuanle Zhao, Xianzhen Luo, Qi Shi, Chi Chen, Shuo
  Wang, Wanxiang Che, Zhiyuan Liu, and Maosong
  Sun. 2025. Chartcoder: Advancing multimodal large
  language model for chart-to-code generation. arXiv
  preprint arXiv:2501.06598.
Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan
  Wang, Yufei Xue, Lei Shen, Zihan Wang, Andi Wang,
  Yang Li, et al. 2023. Codegeex: A pre-trained model
  for code generation with multilingual benchmarking
  on humaneval-x. In Proceedings of the 29th ACM
  SIGKDD Conference on Knowledge Discovery and
  Data Mining, pages 5673–5684.
Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu,
  Wenhao Yu, Ratnadira Widyasari, Imam Nur Bani


                                                          17
A     Multi-Round PairCoder Traces on                                 Verification evidence ψ shown to the Navi-
      Code-Driven Multimodal Benchmarks                               gator

                                                                  1   runs OK; structural similarity to
This appendix documents complete PairCoder ses-                   2   the target chart = 0.876
sions on the multimodal benchmarks of Sec. 5.
Each trace shows the Driver’s program, the ver-
ification evidence ψ attached to the Navigator’s re-
view (execution status and, for image conditioned                     Round 1, Navigator review (verbatim)
tasks, the structural similarity of the current render-
ing to the target), the Navigator’s verbatim verdict,             1   The code has a visual mismatch with
                                                                  2   the target figure:
and the error triggered role switches. Renders of                 3   - Line causing the mismatch:
the rounds accompany each trace so the effect of                  4     fig.suptitle("Errorbar subsampling",
each review can be inspected visually. Traces use                 5                  fontsize=14)
                                                                  6   - Why: the target image uses a larger,
gpt-5.4-mini unless stated otherwise; prompts                     7     more prominent figure title and
and the review protocol are identical to the main                 8     slightly different top spacing. With
experiments.                                                      9     fontsize=14 the title is too small
                                                              10        compared to the reference.
                                                              11      - Fix: increase the suptitle size and
A.1    Case 1 (Plot2Code): review, role switch,               12        adjust its vertical placement.
       and cross acceptance
The Driver reproduces a three panel errorbar chart
from the target image (Fig. 9). Its first program                     Round 2, after role switch: former Naviga-
already runs and is close to the target, but the Navi-                tor writes the fix (diff)
gator, looking at the current rendering next to the
                                                                  1   - fig.suptitle("Errorbar subsampling",
target, finds a concrete visual deviation and rejects             2   -     fontsize=14)
the round. After the role switch the former Nav-                  3   + fig.suptitle("Errorbar subsampling",
igator takes the keyboard and applies its own fix,                4   +     fontsize=18, y=0.98)
and the former Driver, now reviewing, accepts with
[NOERROR]. The session costs two generations and
two reviews.
                                                                      Round 2, former Driver now reviews

                                                                  1   [NOERROR]




Figure 9: Case 1 rendering progression: target (left), the
                                                                  A.2    Case 2 (Plot2Code): review oscillation
Driver’s first program (middle), the program after the                   and the quality fallback
role switch (right).

                                                                  A harder session on a two panel contour task.
    Round 1, Driver (initial program, excerpt)                    The pair improves the program over three revision
                                                                  rounds (contour levels, then colorbars), but the two
1   fig, axs = plt.subplots(1, 3,
2       figsize=(12, 6), sharex=True)                             reviewers disagree about whether the target con-
3   fig.suptitle("Errorbar subsampling",                          tains colorbars, so no round is accepted within the
4       fontsize=14)
5   axs[0].errorbar(x, y1, yerr=yerr, ...)
                                                                  budget. PairCoder then falls back to the quality
6   axs[1].errorbar(x, y1, yerr=yerr,                             criterion of Algorithm 1 and returns the round with
7       errorevery=6)                                             the highest verified similarity score, which is also
8   axs[2].errorbar(x, y1, yerr=yerr,
9       errorevery=(6, 3))                                        the visually closest rendering (Fig. 10). The fall-
                                                                  back turns an unresolved review debate into a safe
                                                                  outcome instead of a failure.

                                                             18
Figure 10: Case 2 rendering progression: target, rounds
1 and 2, and the round selected by the quality fallback
after budget exhaustion.                                       Figure 11:       Case 3 rendering progression on
                                                               doubao-1.5-lite: target (left), the Driver’s first (non-
                                                               compiling) program (middle), the repaired program after
    Round 1, Navigator review (verbatim,                       the role switch (right).
    trimmed)

1   The code has a definite mismatch:                              Verification evidence ψ shown to the Navi-
2   - Problem line:
3     levels = np.linspace(-0.48, 0.40, 15)                        gator
4   - Why: the prompt says the plots should
5     use 14 levels, and the target image's                    1   LaTeX compilation FAILED
6     contour/colorbar scaling does not
7     match this fixed custom range.
8   - Concrete fix: use 14 contour levels
9     directly in both plots.                                      Round 1, Navigator review (verbatim,
                                                                   trimmed)
    Round 2, former Driver now reviews (ver-                   1   The error is that the code uses
    batim, trimmed)                                            2   \cref{claim:paths} which is not defined
                                                               3   anywhere in the provided code. To fix
                                                               4   this, either define the claim:paths
1   Missing colorbars.
                                                               5   macro appropriately in the preamble or
2   - The target figure shows a colorbar
                                                               6   remove the reference from the caption.
3     beside each subplot, but the code
                                                               7   Specific fix: remove the
4     never adds one. The exact missing
                                                               8   \cref{claim:paths} part from the
5     lines are:
                                                               9   caption.
6     fig.colorbar(cf, ax=ax)
7     fig.colorbar(cf2, ax=ax)


                                                                   Round 2, former Driver now reviews
    Round 3, the other agent disagrees (verba-
    tim, trimmed)                                              1   [NOERROR]

1   The code still has a concrete mismatch:
2   - Problem lines: fig.colorbar(cf, ax=ax)
3     and fig.colorbar(cf2, ax=ax)
4   - Why: the target image shows NO                           A.4    Case 4 (DaTikZ): first round acceptance,
5     colorbars. Adding them changes the                              the cheap path
6     layout and shrinks the axes.
                                                               For completeness, the most common trace shape:
A.3    Case 3 (DaTikZ, doubao-1.5-lite):                       the Driver’s first program compiles, the Navigator
       compile error repair on a weak model                    receives the passing evidence, finds no concrete
                                                               error, and accepts immediately with [NOERROR].
The same protocol on the weakest model in our                  The session costs one generation plus one review,
pool, where PairCoder lifts the DaTikZ compile                 roughly twice a single pass, which is why the av-
rate from 0.550 to 0.850. The Driver’s first TikZ              erage token multiplier in Sec. 4.5 stays in the 3 to
program fails to compile because its caption ref-              9 range even though failing tasks iterate several
erences an undefined cross reference macro. The                times.
Navigator receives the compiler verdict as evidence,
identifies the exact offending construct, and pro-                 Verification evidence ψ
poses the minimal removal; after the role switch the
                                                               1   compiles and renders OK
repaired program compiles and the former Driver
accepts (Fig. 11).

                                                          19
    Round 1, Navigator                                         capped Chamfer score (CD) to the F-score, normal-
                                                               consistency (NC), and volumetric-IoU sub-metrics
1   [NOERROR]
                                                               already reported per model in Table 1. All are the
                                                               worst-filled mean over the 400-case text-to-3D split
B    Per-Benchmark Qualitative and                             (invalid programs score 0, so the metric jointly re-
                                                               wards executability and fidelity). PairCoder im-
     Quantitative Results
                                                               proves every sub-metric on every model. The
This appendix devotes one full page to each artifact           gains are largest exactly where the single-model
benchmark: a gallery of qualitative comparisons on             baseline leaves headroom: on gpt-5.4 (71.5%
top and that benchmark’s complete measured met-                valid) F-score@0.05 rises 0.443 → 0.619, NC
ric suite below. In every gallery triplet the target           0.435 → 0.605, and IoU 0.226 → 0.334, while
or ground truth rendering is on the left, the sin-             on the weak doubao-1.5-lite (14.0% valid) ev-
gle model baseline’s artifact is in the middle, and            ery sub-metric roughly triples. Two facts isolate
PairCoder’s artifact is on the right (copper border),          where the gain comes from. First, on the cases the
with the task id and input quoted beneath; each ex-            baseline already compiles, the mean raw Cham-
ample is a distinct task. For the chart, plot, and vec-        fer distance (unnormalized, lower better) is es-
tor benchmarks every example has both arms ren-                sentially unchanged (e.g. 0.0042 → 0.0042 on
dering with PairCoder quantitatively closer to the             doubao-seed-2.0-mini, 0.0029 → 0.0029 on
target, so the comparison isolates artifact quality.           gpt-5.4-mini): PairCoder does not perturb solids
For DaTikZ, GenCAD-Code, and 3DCodeBench,                      that already build. Second, the worst-filled sub-
where PairCoder’s measured advantage is concen-                metrics nonetheless rise sharply, because PairCoder
trated in executability, the galleries lead with fi-           converts a large fraction of non-executable pro-
delity gains and then show executability repairs,              grams into valid solids that recover the target’s
in which the baseline produces no artifact (gray               structure: the coverage gain, not a re-optimization
panel) and PairCoder renders successfully. Each                of already-valid geometry, drives the numbers, con-
table reports every metric we measured for that                sistent with the conservative-review design.
benchmark, as “single model → PairCoder,” with
                                                               Topology breakdown. Table 12 expands the
green cells marking improvements and aggregate
                                                               P3D-Bench topology column of Table 1 into its
scores counting non rendering generations as zero.
                                                               three official sub-metrics, again as worst-filled
                                                               means: the fraction of solids with no open edge
C    Cross-Model Qualitative Comparisons                       (NoOE), and one minus the inverted-normal (InvN)
                                                               and non-manifold-edge (NM) ratios; all lie in [0, 1]
The per-benchmark galleries above use                          with higher better. The pattern mirrors geome-
gpt-5.4-mini. To show that the improvement                     try: PairCoder improves every topology sub-metric
is not specific to one backbone, Figures 19–23                 on every model, most strongly where the baseline
hold the benchmark and the task fixed and vary                 leaves headroom (gpt-5.4 NoOE 0.695 → 0.970,
the base model: each page covers one benchmark                 doubao-1.5-lite NoOE 0.130 → 0.400). Be-
across four models (columns) and three shared                  cause a program must build a valid solid before it
tasks (stacked blocks, the shared target shown in              can be watertight or manifold, these gains are again
each strip), with the single model artifact above              driven by converting non-executable programs into
the PairCoder artifact for the same model and                  well-formed solids rather than by repairing already-
task. The chart, plot, and vector panels use tasks             valid meshes.
where both arms render, so the comparison isolates
                                                               Qualitative examples: geometry refinement.
quality; the 3DCodeBench panel uses tasks where
                                                               On P3D-Bench text-to-3D the compile-grounded
several backbones fail to render and PairCoder
                                                               PairCoder of Table 1 gains by coverage: it re-
repairs execution (gray “no render” marks the
                                                               pairs non-executable programs into valid solids and
failure).
                                                               leaves already-compiling programs unchanged, so
D    P3D-Bench: Detailed Results                               on the common set the two solids are identical. We
                                                               additionally evaluate a vision-grounded geometry-
Full geometry breakdown. Table 11 gives the                    refinement variant: when the single-model pro-
full P3D-Bench geometry breakdown, adding the                  gram compiles to a valid but geometrically poor

                                                          20
Figure 12: Plot2Code qualitative gallery (27 distinct examples); both arms render and PairCoder is quantitatively
closer to the target.

                             Model                     exec ↑           SSIM ↑          CLIP ↑

                             gpt-5.4-mini           0.841 → 0.962    0.412 → 0.474   0.802 → 0.912
                             gpt-5.4                0.962 → 0.977    0.476 → 0.495   0.916 → 0.920
                             gpt-5.5                0.985 → 0.977    0.487 → 0.496   0.943 → 0.931
                             doubao-seed-2.0-mini   0.909 → 0.917    0.410 → 0.443   0.835 → 0.823


    Table 3: Plot2Code: full measured metric suite for every applicable model (single model → PairCoder).




                                                                21
Figure 13: PandasPlotBench qualitative gallery (27 distinct examples); both arms render and PairCoder is quantita-
tively closer to the target.

                              Model                     exec ↑           SSIM ↑          CLIP ↑

                              gpt-5.4-mini           0.789 → 0.851    0.423 → 0.461   0.728 → 0.794
                              gpt-5.4                0.966 → 0.994    0.567 → 0.610   0.909 → 0.944
                              gpt-5.5                0.960 → 0.977    0.597 → 0.644   0.907 → 0.942
                              doubao-seed-2.0-mini   0.909 → 0.989    0.491 → 0.534   0.846 → 0.922


Table 4: PandasPlotBench: full measured metric suite for every applicable model (single model → PairCoder).




                                                                 22
solid, the Navigator renders the solid and reviews            the result. In CadQuery, PairCoder repairs the one
it against the specification, and the Driver refines          non-compiling image-to-3D case (0.667 → 1.000
the parametric program (kept only if it still com-            valid) and recovers a valid assembly-3D solid from
piles). Across a sample of 40 mid-quality valid               a baseline that builds none (0 → 0.333), via a
solids (0.2 < F@0.05 < 0.8) on gpt-5.4, this re-              sibling candidate. In Three.js, gpt-5.4 already
finement raises F-score@0.05 on 29 and regresses              compiles all three image-to-3D cases, so PairCoder
on 3 (the kept-if-compiles safeguard bounds re-               ties, consistent with the headroom pattern seen
gressions), for a mean gain of +0.26; it is thus a            across the grid. The three-case sample is illus-
genuine effect rather than a cherry-pick. Figure 24           trative rather than conclusive, but it shows the
shows cases where both the single model and this              compiler-grounded mechanism reaches the image-
variant build valid solids, but the refined one is            conditioned tracks and a web-rendering representa-
much closer to the target: each triplet renders the           tion, spanning all four P3D-Bench program formats
ground-truth solid (green), the single-model solid            together with text-to-3D.
(pink; valid but wrong), and the PairCoder-refined
solid (blue), with the per-case F-score@0.05 im-              E   Reproducibility Notes
provement annotated.                                          For every benchmark we use the official
A second Text-to-3D format: OpenSCAD. To                      task set and scorer where released (Chart-
test whether the P3D-Bench gain is specific to                Mimic, Plot2Code, PandasPlotBench, StarVec-
the minimal-JSON format, we repeat the 400-                   tor, DaTikZ, 3DCodeBench, GenCAD-Code, Ver-
case Text-to-3D experiment with OpenSCAD, a                   ilogEval, RTLLM, WebApp1K, LiveCodeBench,
constructive-solid scripting language, on the three           BigCodeBench, DS-1000, HumanEval-X), iden-
models for which both formats were run. Ta-                   tical prompts and code extraction in both arms,
ble 13 reports validity, the fraction of programs that        and provider default sampling with thinking dis-
compile to a valid solid, for both formats side by            abled. Visual metrics are computed with SSIM
side. Two observations stand out. First, PairCoder            at 256×256 and the public CLIP, DINOv2, and
drives OpenSCAD validity to a perfect 1.000 on                SigLIP-2 checkpoints; Chamfer distance is com-
all three models, repairing every non-compiling               puted on normalized surface samples, and aggre-
program. Second, the single-model baseline is                 gate variants assign non executing generations the
markedly more fluent in OpenSCAD than in the                  worst observed score so that executability cannot
minimal-JSON format (for example gpt-5.4 base-                be traded for similarity. Token counts are taken
line validity 0.715 → 0.932), so the coverage                 from provider usage fields and logged separately
headroom PairCoder recovers is correspondingly                for the baseline arm and the PairCoder arm.
smaller: its OpenSCAD validity gain is +6.8 points
on gpt-5.4 versus +27.5 points in minimal-JSON.
This is the same headroom-tracking pattern seen
across the rest of the grid. The gain concentrates
where the baseline leaves room; OpenSCAD’s
higher baseline fluency compresses it, while Pair-
Coder still closes the remaining gap to perfect exe-
cutability in both formats.
Image-to-3D and assembly-3D demonstration.
The other two P3D-Bench tracks, image-to-3D and
assembly-3D, condition on a rendered image of the
target (assembly-3D also on part annotations) and
require a vision-capable model; their full evalua-
tion sets build on the licensed Fusion 360 Gallery.
We run the three in-repo demo cases per track with
gpt-5.4 across the CadQuery and Three.js pro-
gram formats (OpenSCAD is already evaluated at
scale on text-to-3D, Table 13), scoring the same
non-VLM buckets as text-to-3D. Table 14 reports

                                                         23
Figure 14: ChartMimic qualitative gallery (23 distinct examples); both arms render and PairCoder is quantitatively
closer to the target.

                              Model                     exec ↑           SSIM ↑          CLIP ↑

                              gpt-5.4-mini           0.967 → 0.967    0.578 → 0.578   0.871 → 0.861
                              gpt-5.4                0.917 → 0.983    0.533 → 0.582   0.820 → 0.848
                              gpt-5.5                0.983 → 1.000    0.593 → 0.613   0.874 → 0.887
                              doubao-seed-2.0-mini   0.900 → 0.950    0.443 → 0.476   0.770 → 0.808


   Table 5: ChartMimic: full measured metric suite for every applicable model (single model → PairCoder).




                                                                 24
Figure 15: StarVector qualitative gallery (12 distinct examples); both arms render and PairCoder is quantitatively
closer to the target.

                       Model                   render rate ↑      SSIM ↑          CLIP ↑         DINO ↑

                       gpt-5.4-mini           0.983 → 1.000    0.784 → 0.801   0.929 → 0.944   0.874 → 0.885
                       gpt-5.4                0.900 → 1.000    0.776 → 0.873   0.859 → 0.954   0.820 → 0.906
                       gpt-5.5                1.000 → 1.000    0.777 → 0.787   0.961 → 0.960   0.938 → 0.934
                       doubao-seed-2.0-mini   0.983 → 1.000    0.758 → 0.770   0.883 → 0.915   0.793 → 0.819


    Table 6: StarVector: full measured metric suite for every applicable model (single model → PairCoder).




                                                                 25
Figure 16: GenCAD-Code qualitative gallery (12 distinct examples) demonstrating PairCoder’s advantage; gray
panels mark baselines that produce no artifact.

                          Model                     exec ↑        Chamfer (cond.) ↓   Chamfer (agg.) ↓

                          gpt-5.4-mini           0.900 → 0.983     0.148 → 0.152      0.233 → 0.166
                          gpt-5.4                0.867 → 0.983     0.145 → 0.140      0.259 → 0.155
                          doubao-seed-2.0-mini   0.833 → 0.967     0.169 → 0.185      0.308 → 0.212
                          gpt-5.5                0.917 → 1.000     0.143 → 0.126      0.215 → 0.126


 Table 7: GenCAD-Code: full measured metric suite for every applicable model (single model → PairCoder).




                                                             26
Figure 17: DaTikZ qualitative gallery (12 distinct examples) demonstrating PairCoder’s advantage; gray panels
mark baselines that produce no artifact.

                      Model                  compile rate ↑      SSIM ↑          CLIP ↑         DINO ↑

                      gpt-5.4-mini           0.500 → 0.633    0.215 → 0.256   0.327 → 0.384   0.303 → 0.338
                      gpt-5.4                0.717 → 0.967    0.363 → 0.512   0.566 → 0.770   0.530 → 0.698
                      gpt-5.5                0.783 → 1.000    0.394 → 0.485   0.602 → 0.767   0.554 → 0.730
                      doubao-1.5-lite        0.550 → 0.850    0.406 → 0.601   0.391 → 0.621   0.259 → 0.391
                      doubao-seed-2.0-mini   0.567 → 0.800    0.325 → 0.449   0.441 → 0.606   0.383 → 0.545
                      deepseek-v3.2          0.683 → 0.917    0.365 → 0.544   0.508 → 0.702   0.465 → 0.596
                      deepseek-v4-flash      0.633 → 0.733    0.348 → 0.406   0.505 → 0.578   0.445 → 0.519


     Table 8: DaTikZ: full measured metric suite for every applicable model (single model → PairCoder).




                                                                27
Figure 18: 3DCodeBench qualitative gallery (12 distinct examples) demonstrating PairCoder’s advantage; gray
panels mark baselines that produce no artifact.

                                Model                               executability ↑

                                gpt-5.4-mini                        0.200 → 0.783
                                gpt-5.4                             0.433 → 0.783
                                gpt-5.5                             0.383 → 0.417
                                doubao-1.5-lite                     0.167 → 0.383
                                doubao-seed-2.0-mini                0.200 → 0.533
                                deepseek-v3.2                       0.333 → 0.633
                                deepseek-v4-flash                   0.600 → 0.533

                                Visual / geometric fidelity at gpt-5.4-mini (aggregate, n=60):
                                SigLIP-2 / DINO ↑                 .181/.101 → .702/.376
                                Chamfer (aggregate) ↓                  4.85 → 2.62


  Table 9: 3DCodeBench: full measured metric suite for every applicable model (single model → PairCoder).



                                                             28
Table 10: Per-benchmark token accounting at gpt-5.4-mini: single model and PairCoder totals over the full task
set, with the cost multiplier; the final row aggregates all runs across all models.

                             Benchmark              single model tokens    PairCoder tokens   multiplier

                             RTLLM                             161,708           1,272,758        7.9×
                             BigCodeBench                      428,875           3,514,486        8.2×
                             DS-1000                           550,911           1,995,002        3.6×
                             HumanEval-X JS                    445,887           2,575,842        5.8×
                             WebApp1K                          310,709           1,234,990        4.0×
                             DaTikZ                            260,271           1,802,890        6.9×
                             StarVector                        212,628             717,238        3.4×
                             ChartMimic                        226,356           1,341,183        5.9×
                             GenCAD-Code                       205,964             597,230        2.9×
                             Plot2Code                         216,997           2,004,708        9.2×
                             PandasPlotBench                   227,343           1,439,613        6.3×

                             All runs, all models           16,373,001         121,722,770        7.4×



Table 11: P3D-Bench text-to-3D geometry sub-metrics (single → PairCoder, 400 cases, worst-filled means, higher
better). CD is the capped-normalized Chamfer score 1 − min(CD, τ )/τ (τ =0.01).

   Model                    Validity ↑              CD ↑          F@0.05 ↑            F@0.01 ↑               NC ↑          IoU ↑
   gpt-5.4-mini            0.973→1.000       0.760→0.782        0.746→0.767         0.316→0.326        0.678→0.698      0.486→0.501
   gpt-5.4                 0.715→0.990       0.453→0.623        0.443→0.619         0.153→0.215        0.435→0.605      0.226→0.334
   gpt-5.5                 0.672→0.943       0.415→0.564        0.419→0.570         0.143→0.188        0.402→0.556      0.207→0.288
   doubao-1.5-lite         0.140→0.427       0.086→0.269        0.094→0.275         0.037→0.104        0.087→0.262      0.054→0.157
   doubao-seed-2.0-mini    0.812→0.990       0.542→0.641        0.537→0.633         0.196→0.230        0.504→0.609      0.302→0.360
   deepseek-v3.2           0.950→0.993       0.693→0.724        0.682→0.714         0.282→0.298        0.640→0.671      0.434→0.460
   deepseek-v4-flash       0.945→1.000       0.740→0.780        0.727→0.764         0.298→0.311        0.650→0.685      0.474→0.498


Table 12: P3D-Bench text-to-3D topology sub-metrics (single → PairCoder, 400 cases, worst-filled means, higher
better): no-open-edge fraction (NoOE), and one minus the inverted-normal (InvN) and non-manifold-edge (NM)
ratios.

              Model                                   NoOE ↑                       InvN ↑                      NM ↑
              gpt-5.4-mini                          0.963→0.990                0.973→1.000                  0.968→0.996
              gpt-5.4                               0.695→0.970                0.715→0.990                  0.714→0.988
              gpt-5.5                               0.662→0.930                0.672→0.943                  0.672→0.940
              doubao-1.5-lite                       0.130→0.400                0.140→0.427                  0.139→0.419
              doubao-seed-2.0-mini                  0.800→0.978                0.812→0.990                  0.811→0.988
              deepseek-v3.2                         0.940→0.983                0.950→0.993                  0.949→0.992
              deepseek-v4-flash                     0.945→1.000                0.945→1.000                  0.939→0.994


Table 13: P3D-Bench text-to-3D validity across two program formats (single → PairCoder, 400 cases, thinking
off).

                                                                          Validity ↑ (single → PC)
                        Model                                  minimal-JSON                    OpenSCAD
                        gpt-5.4                                 0.715→0.990                   0.932→1.000
                        doubao-seed-2.0-mini                    0.812→0.990                   0.925→1.000
                        deepseek-v3.2                           0.950→0.993                   0.990→1.000


Table 14: P3D-Bench image-to-3D and assembly-3D three-case demonstration (single → PairCoder, gpt-5.4)
in the CadQuery and Three.js formats; full evaluation requires the licensed Fusion 360 Gallery.

                Track               Format                 Validity ↑           Geometry ↑                 Topology ↑
                Image-to-3D         CadQuery           0.667→1.000             0.100→0.320             0.667→1.000
                Image-to-3D         Three.js           1.000→1.000             0.417→0.417             0.778→0.778
                Assembly-3D         CadQuery           0.000→0.333             0.000→0.068             0.000→0.333



                                                                29
Figure 19: ChartMimic across four models and three shared tasks (single vs. PairCoder per cell).




                                              30
Figure 20: Plot2Code across four models and three shared tasks.




                              31
Figure 21: PandasPlotBench across four models and three shared tasks.




                                 32
Figure 22: StarVector across four models and three shared tasks.




                              33
Figure 23: 3DCodeBench across four models and three shared tasks; gray marks baselines that fail to render.




                                                    34
  F@.05 0.21 0.95                                      F@.05 0.28 1.00




  F@.05 0.29 0.99                                      F@.05 0.25 0.91




  F@.05 0.32 0.93                                      F@.05 0.23 0.84




  F@.05 0.21 0.81                                      F@.05 0.35 0.94




Figure 24: P3D-Bench geometry-refinement gallery (gpt-5.4): ground truth (green), single model (pink; valid but
geometrically poor), PairCoder (blue); per-case F-score@0.05 annotated.




                                                      35
