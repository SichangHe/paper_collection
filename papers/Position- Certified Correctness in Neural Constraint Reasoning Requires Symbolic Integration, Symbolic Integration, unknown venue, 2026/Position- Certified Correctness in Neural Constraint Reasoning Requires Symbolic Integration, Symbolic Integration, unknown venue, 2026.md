                                                Position: Certified Correctness in Neural Constraint Reasoning Requires
                                                                          Symbolic Integration


                                                                            Shufeng Kong 1 2 Xiaochuan Zhang 1 Caihua Liu 3 2 4


                                                                    Abstract                                1. Introduction
                                                Neural solvers for constraint satisfaction prob-            A central debate in modern machine learning concerns the
                                                lems have achieved remarkable in-distribution               extent to which large-scale statistical learning can replace
                                                accuracy, yet they suffer from a fundamental lim-           explicit symbolic reasoning. While neural solvers have
                                                itation: persistent constraint violations occur un-         achieved remarkable in-distribution accuracy on constraint
                                                der distribution shifts even when the model re-             satisfaction problems (CSPs), they often lack the robust-
                                                ports high confidence. This position paper ar-              ness required for rigorous constraint enforcement. Con-
                                                gues that when hard constraints exist and the cost          sider the case of Sudoku: SATNet achieves 98.3% test
                                                of verification is relatively low, neural constraint
arXiv:2608.14569v1 [cs.AI] 2 Jun 2026




                                                                                                            accuracy on its in-distribution benchmark (Wang et al.,
                                                reasoning must prioritize symbolic integration              2019), but when the number of given digits shifts from
                                                over pure learning. We justify our focus on                 31–42 to 17–34 (out-of-distribution), accuracy collapses to
                                                Sudoku as a representative NP-complete testbed              3.2% (Miyato et al., 2025), representing a 95.1 percentage
                                                because it exhibits a sharp asymmetry between               point degradation. This is not an isolated failure. Even
                                                easy verification and hard solving: checking a              the leading neural-only solver without explicit certification,
                                                candidate solution requires only polynomial time            AKOrN (Miyato et al., 2025), achieves only 89.5±2.5%
                                                O(n2 ), while finding a solution may require ex-            OOD accuracy despite extensive test-time compute (128
                                                ponential search. Through a comprehensive sur-              Kuramoto steps and 4,096 samples with energy-based vot-
                                                vey of solving methods spanning deterministic               ing). By contrast, the neuro-symbolic system NeurASP
                                                algorithms, metaheuristic optimization, learning-           achieves 100% constraint satisfaction using only 25 train-
                                                based approaches, and language-conditioned rea-             ing examples (Yang et al., 2020), requiring orders of mag-
                                                soning, we demonstrate that neural-only meth-               nitude fewer samples than neural-only approaches such as
                                                ods without instance-level certification fail to            RRN (Palm et al., 2018). These empirical disparities indi-
                                                achieve the provable correctness that symbolic              cate that statistical approximation is fundamentally distinct
                                                and neuro-symbolic approaches provide. We ad-               from logical satisfaction, motivating the central position of
                                                vocate for a bidirectional integration in which             this paper.
                                                neural methods enhance symbolic solvers by
                                                learning heuristics and converting percepts into            Position. Neural constraint reasoning should priori-
                                                symbols, while symbolic methods verify neural               tize symbolic integration over pure learning when: (i)
                                                outputs to ensure their reliability. To operational-        hard constraints exist and are specifiable; (ii) verifica-
                                                ize this position, we propose a multi-agent certi-          tion costs are low relative to solving; and (iii) violation
                                                fied reasoning framework that demonstrates how              costs are high.
                                                this integration can achieve both computational             This paper focuses on domains where all three conditions
                                                efficiency and provable correctness.                        hold, including Sudoku and many industrial CSPs such as
                                                                                                            scheduling, configuration, and compliance checking. In
                                            1
                                              School of Software Engineering, Sun Yat-sen Univer-           these settings, cheap verification (O(n2 ) for Sudoku) can
                                        sity, Zhuhai, China 2 Department of Computer Science, Cor-          effectively certify expensive-to-produce solutions. We ad-
                                        nell University, Ithaca, NY, USA 3 School of Computer Science
                                        and Artificial Intelligence, Foshan University, Foshan, China       vocate for bidirectional integration: neural methods en-
                                        4
                                          Department of Ecology and Evolutionary Biology, Cornell           hance symbolic solvers by improving accessibility and
                                        University, Ithaca, NY, USA. Correspondence to: Caihua Liu          scalability, while symbolic methods certify neural outputs
                                        <cl2869@cornell.edu>.                                               to ensure trustworthiness.
                                        Proceedings of the 43 rd International Conference on Machine        Relationship to Prior Work. Our position shares with
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026        Kambhampati et al. (2024) the insight that neural systems
                                        by the author(s).

                                                                                                        1
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

require external symbolic verification, but diverges in a            modes attributable purely to neural approximation, with no
fundamental way. First, we focus on constraint satisfaction          confounding from shifting tasks or constraint sets. Such
problems, where polynomial-time verification (e.g., O(n2 )           control is difficult in messier domains (code, scheduling)
for Sudoku) contrasts sharply with NP-hard solving, en-              where many variables change simultaneously. The position
abling stronger certification claims than planning domains           generalizes to any domain satisfying (i)–(iii); Section 5.4
allow. Second, we survey four paradigms (deterministic,              confirms this for code generation, hard vehicle routing, and
metaheuristic, learning-based, and language-conditioned)             automated theorem proving.
to demonstrate that the certification gap persists across fun-
                                                                     Contributions. This paper makes four primary contribu-
damentally different architectures. Third, whereas LLM-
                                                                     tions. First, we provide a comprehensive taxonomy of
Modulo treats neural components as unidirectional gener-
                                                                     Sudoku solving methods across four paradigms: deter-
ators verified by symbolic critics, we advocate for bidi-
                                                                     ministic algorithms, metaheuristics, neural networks, and
rectional integration: neural methods enhance symbolic
                                                                     large language models (Section 2). Second, we advance
solvers (via learned heuristics and perception), while sym-
                                                                     three falsifiable empirical claims (Section 3): Claim 3.1
bolic methods certify neural outputs—a division of labor
                                                                     establishes that neural-only methods without explicit cer-
that exploits the strengths of both.
                                                                     tification exhibit >10% violation rates under distribu-
Operational Definition. To clarify our scope, we employ              tion shift; Claim 3.2 demonstrates that test-time scaling
a taxonomy distinguishing where constraint structure is in-          yields diminishing returns and fails to distinguish correct
jected and what guarantees it yields. We classify systems            from incorrect outputs; and Claim 3.3 shows that neuro-
into three categories: (i) Purely neural (data-implied):             symbolic approaches achieve dramatic sample efficiency
Systems that (a) invoke no external symbolic computation             gains. Third, we articulate strategies for bidirectional
(such as SAT/SMT/ASP solvers or constraint checkers) at              integration, demonstrating how neural methods can en-
inference time, and (b) do not encode constraints by archi-          hance symbolic solvers (via perception and heuristics) and
tectural construction. Constraint satisfaction in these mod-         how symbolic methods must certify neural outputs to en-
els is statistical rather than certified. (ii) Architecturally       sure trustworthiness (Section 4). Fourth, we propose the
constrained: Systems where constraints are enforced by               Proposer-Verifier-Solver (PVS) framework, a concrete
design via parameterization, projection, or normalization            multi-agent architecture that operationalizes these strate-
layers within the network. (iii) Symbolically integrated:            gies to achieve both computational efficiency and provable
Systems where constraint semantics are enforced via ex-              correctness (Section 5).
plicit symbolic verification or solving at inference time, en-
                                                                     Falsifiability. To ensure scientific rigor, we define a strict
abling instance-level certification.
                                                                     refutation criterion: If a purely neural (data-implied) sys-
Scope Note: Architectural vs. Symbolic Enforcement.                  tem achieves a <1% violation rate on a preregistered OOD
For continuous constraints (probability simplexes via Soft-          benchmark without (i) invoking symbolic solvers or ex-
max; linear inequalities via differentiable QPs (Amos                plicit constraint checkers at inference time, and without (ii)
& Kolter, 2017)), architectural enforcement is sufficient.           enforcing the task-defining constraints in C by architectural
Our position targets the complementary regime of dis-                construction, then this thesis is refuted.
crete combinatorial constraints with global structure (e.g.,
                                                                     Conflict of Interest Disclosure. The authors declare no fi-
all-different in Sudoku, sub-tour elimination in
                                                                     nancial conflicts of interest: no commercial product is eval-
TSP). Here, end-to-end neural solvers rely on continuous
                                                                     uated, and no author is employed by an organization that
relaxations during training (e.g., SATNet’s differentiable
                                                                     produces the systems compared in this paper.
SDP of MAXSAT) (Wang et al., 2019): effective soft guid-
ance in-distribution, but the discrete rounding at inference
reintroduces violation risk, and this gap cannot be closed           2. A Taxonomy of Constraint Satisfaction
by architecture alone without resolving P vs. NP (Garey &               Paradigms
Johnson, 1979). Architectural and symbolic enforcement
are complementary, not competing.                                    To locate the precise failure mode of modern solvers, we
                                                                     categorize Sudoku solving methods into four paradigms:
Why Sudoku? A Controlled “Drosophila” Testbed. Su-                   deterministic algorithms, metaheuristic optimization, end-
doku is NP-complete (Yato & Seta, 2003) yet exhibits a               to-end neural learning, and language-conditioned reason-
sharp “easy verification, hard solving” asymmetry: check-            ing. We evaluate each paradigm against three criteria cen-
ing takes O(n2 ), finding a solution may require exponen-            tral to our position: flexibility (handling unstructured in-
tial search. More importantly, it is a controlled testbed: by        puts), efficiency (inference latency), and certified cor-
varying only the clue count ID [31−42] → OOD [17−34]                 rectness (guaranteed satisfaction). Table 1 summarizes
while holding all 324 constraints fixed, we isolate failure          these trade-offs, identifying a critical “Certification Gap”


                                                                 2
                 Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

in modern learning-based approaches.                                    to achieve 100% constraint satisfaction given perceived in-
                                                                        puts. The failure mode shifts from reasoning (solving the
2.1. Deterministic Algorithms: The Baseline of                          puzzle) to perception (reading the digits), proving that inte-
     Certifiability                                                     gration can preserve certification where pure learning fails.
                                                                        We treat NeurASP as a control baseline in this paper: its
Deterministic methods—including Dancing Links                           neural component performs only perception (mapping digit
(DLX) (Knuth, 2000), SAT solvers (Biere et al., 2020),                  images to label distributions), and the ASP solver con-
and constraint propagation (Norvig, 2006)—represent the                 structs the full solution. The neural network does not gen-
gold standard for correctness.                                          erate candidate solutions; the system therefore isolates the
Modern implementations such as Tdoku (Dillon, 2019)                     effect of explicit symbolic specification from any contribu-
leverage SIMD optimizations (AVX-512) to achieve                        tion of neural search. The Proposer-Verifier-Solver frame-
microsecond-level solve times (∼2.7 µs/puzzle). Crucially,              work introduced in Section 5 lies at the opposite end of the
these methods provide correctness by construction: they                 spectrum: the neural network actively proposes candidates
do not return a result unless it provably satisfies all con-            and the symbolic component certifies them.
straints. Their limitation is not reliability, but rigidity; they
cannot consume the unstructured inputs (images, natural                 2.4. Language-Conditioned Reasoning: The Illusion of
language) characteristic of real-world AI deployment.                        Logic
                                                                        Large Language Models (LLMs) represent the newest fron-
2.2. Metaheuristic Optimization: Search Without                         tier, attempting to solve CSPs via token-by-token reasoning
     Guarantees                                                         (Chain-of-Thought). Despite improvements in “System 2”
Metaheuristics—such as simulated annealing (Lewis,                      reasoning models (e.g., OpenAI’s o1), pure LLMs strug-
2007) and genetic algorithms (Mantere & Koljonen,                       gle with strict global constraints. On Sudoku-Bench (Seely
2007)—recast constraint satisfaction as an energy mini-                 et al., 2025), GPT-5 achieves only 33% accuracy on the
mization problem. While more flexible than exact solvers,               challenge 100 set.
they suffer from phase transitions. Lewis (2007) showed                 The core issue is that autoregressive generation is proba-
that on order-5 Sudokus (25 × 25), success rates can drop               bilistic; an LLM can “reason” its way to a constraint viola-
to 30% near the critical hardness threshold. Unlike deter-              tion with high confidence. However, when LLMs are aug-
ministic methods, metaheuristics provide no guarantee of                mented with tool use (LLM-Modulo (Kambhampati et al.,
convergence; they may stagnate in local optima where con-               2024)), effectively becoming neuro-symbolic controllers,
straints remain violated, making them unsuitable for safety-            they can regain correctness—but only if the symbolic tool
critical certification.                                                 is treated as the source of truth.

2.3. End-to-End Neural Learning: The Statistical Trap                   2.5. Summary: The Certification Gap
This paradigm attempts to learn constraint satisfaction from            This survey reveals a distinct “Certification Gap”. We have
data, treating logical necessities as statistical regularities.         methods that are fast and certified but rigid (Determinis-
Architectures range from Recurrent Relational Networks                  tic), and methods that are flexible and general but uncerti-
(RRN) (Palm et al., 2018) to differentiable solvers like                fied (Neural/LLM). Purely neural approaches—regardless
SATNet (Wang et al., 2019). While these models achieve                  of scale—cannot bridge this gap because they approximate
high in-distribution (ID) accuracy (e.g., 98.3% for SAT-                discrete validity with continuous probability. This neces-
Net), they exhibit a fundamental lack of robustness. Under              sitates the bidirectional integration proposed in this pa-
distribution shift (AKOrN split), SATNet’s accuracy col-                per: using neural models for flexible perception and heuris-
lapses to 3.2% (Miyato et al., 2025). Even AKOrN (Miy-                  tics, while retaining symbolic engines for the final, non-
ato et al., 2025), which integrates oscillator dynamics for             negotiable certification of correctness.
better stability, relies on energy-based voting to achieve
89.5% OOD accuracy. Because constraints are soft train-
ing signals rather than hard inference gates, these methods             3. Empirical Evidence: The Limits of
inevitably produce “almost correct” solutions that are logi-               Statistical Learning
cally invalid.
                                                                        Neural-only methods without explicit symbolic certifica-
The Neuro-Symbolic Exception(Control Baseline). Sys-                    tion can achieve near-perfect in-distribution accuracy but
tems like NeurASP (Yang et al., 2020) deviate from this                 degrade substantially under distribution shift. By contrast,
pattern by delegating the solving step to a symbolic ASP                neuro-symbolic methods maintain constraint satisfaction
backend. This isolation of responsibilities allows NeurASP              by delegating to symbolic solvers.

                                                                    3
                 Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

Table 1. The Certification Gap. While deterministic methods guarantee correctness, they lack the flexibility to handle raw perceptual
inputs. Neural and LLM approaches offer flexibility but sacrifice certification, leading to OOD failures. Neuro-symbolic integration (the
advocated position) bridges this gap.

            Paradigm                 Input Modality        Typical Speed                  Certified?                   Failure Mode
            Deterministic               Structured              µs–ms                          Yes           Rigid input requirements
            Metaheuristic               Structured              ms–s                           No            Local optima convergence
            End-to-End Neural        Raw/Structured             ms–s                           No               OOD Degradation
            Language-Cond.           Text/Multimodal            s–min                          No             Hallucinated reasoning


We advance three empirical claims supported by recent the-                                     98.3 96.8 99.8          99.4          100          100          100100
oretical findings:                                                                       100
                                                                                                                                                   89.5

                                                                                                                                      77.7




                                                                        Percentage (%)
                                                                                                                71.4
• Claim 1 (OOD Violations): State-of-the-art neural-only
                                                                                                                         62.1
  methods without explicit symbolic certification exhibit
  residual constraint violations under distribution shift that                           50
  further test-time compute cannot eliminate.                                                                                 37.9
                                                                                                             28.6
• Claim 2 (Compute ̸= Certificates): Test-time scaling                                                                                     22.3

  improves average accuracy but provides no mechanism                                                                                                   10.5
                                                                                                  3.2
  to distinguish correct from incorrect individual outputs,                                0
                                                                                                                                                                        0

  leaving a “validity gap” that compute alone cannot close.




                                                                                                          N
                                                                                              et




                                                                                                                       ED


                                                                                                                                      F


                                                                                                                                                   rN


                                                                                                                                                  SP
                                                                                                                                     ns
                                                                                                        RR
                                                                                            TN




                                                                                                                                              KO


                                                                                                                                                rA
                                                                                                                    IR


                                                                                                                                Co
                                                                                          SA
• Claim 3 (Integration Efficiency): Neuro-symbolic ap-




                                                                                                                                             eu
                                                                                                                                            A

                                                                                                                                           N
  proaches achieve orders-of-magnitude sample efficiency
  gains by removing constraint satisfaction from the hy-
                                                                                                          ID Accuracy                       OOD Accuracy
  pothesis space.
                                                                                                        OOD Violation Rate

3.1. Persistent OOD Violations                                         Figure 1. Performance degradation under distribution shift. All
                                                                       methods achieve near-perfect in-distribution (ID) accuracy, but
Claim 1. Even state-of-the-art neural-only methods with-               neural-only methods without instance-level certification show
out explicit symbolic certification exhibit residual con-              substantial OOD degradation (red bars). NeurASP maintains 0%
straint violations under distribution shift that further test-         violation rate by delegating to a symbolic solver.
time compute cannot eliminate.

Figure 1 visualizes the performance gap between in-                    NeurASP achieves 100% constraint satisfaction (given per-
distribution and out-of-distribution settings. The pattern             ceived inputs) through a categorically different mecha-
is striking: neural solvers that appear near-perfect on in-            nism: it delegates constraint satisfaction entirely to an ASP
distribution data suffer severe degradation when the diffi-            solver. The neural component handles only perception
culty distribution shifts.                                             (digit recognition), while the symbolic component guaran-
                                                                       tees correctness. This architectural division of labor elimi-
This degradation is not merely an engineering failure but              nates the certification gap by construction.
a theoretical inevitability. As noted by Balestriero et al.
(2021), neural inference in high-dimensional spaces almost
                                                                       3.2. Compute Cannot Produce Certificates
always involves extrapolation beyond the training mani-
fold. Models like SATNet, even when incorporating dif-                 Claim 2. Test-time scaling yields diminishing returns and
ferentiable relaxations of constraint structure, fail to gener-        provides no mechanism to distinguish correct from incor-
alize these structures robustly. Increasing test-time com-             rect outputs.
pute, as seen in ConsFormer and AKOrN, partially mit-
igates the problem but cannot eliminate it. Concretely,                A natural response to OOD degradation is to increase test-
AKOrN plateaus at ∼10.5% violations on our preregistered               time compute. ConsFormer’s scaling curve illustrates the
Sudoku OOD protocol even at its maximum compute bud-                   limitations of this approach: moving from 2K to 10K itera-
get (128 Kuramoto steps, 4,096 samples, energy-based vot-              tions (a 5× increase in compute) yields only ∼12 percent-
ing). Even with extensive sampling and voting, neural-only             age points of improvement, plateauing well below 100%.
methods leave a persistent residual of constraint violations.          Similarly, AKOrN requires 4,096 forward passes per puz-

                                                                   4
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

zle, each involving 128 internal Kuramoto iteration steps,           of two specific learning algorithms; the independent vari-
yet still fails on ∼10.5% of instances. By contrast, Tdoku           able is the presence vs. absence of explicit symbolic spec-
solves the hardest puzzles in ∼42µs. The compute ratio ex-           ification. RRN tackles the same Sudoku task with con-
ceeds 108 , yet the neural approach provides no correctness          straints learned from data rather than specified: it con-
guarantee.                                                           sumes 216,000 training examples (∼8,640× NeurASP’s
                                                                     25) and still collapses under the same OOD shift. The
The deeper issue is epistemic rather than computational.
                                                                     certification gap is therefore architectural, not a matter of
Xu et al. (2024) prove that for any computable function ap-
                                                                     dataset size: a soft-regularizer architecture obtains its con-
proximated by a neural network, there exist inputs where
                                                                     straint signal from continuous relaxations of discrete con-
the model produces incorrect outputs with non-negligible
                                                                     straints, and those relaxations hold only in expectation—no
probability. Neural confidence scores are notoriously mis-
                                                                     amount of additional data converts them into the instance-
calibrated (Guo et al., 2017); thus, a high confidence score
                                                                     level guarantee that a symbolic verifier provides by con-
is not a certificate of correctness. A system that is “usually
                                                                     struction.
right” is categorically different from one that is “provably
right.”
                                                                     4. Strategies for Bidirectional Integration
The Aggregate-Instance Gap. Accuracy is an aggregate
                                                                     The case for bidirectional integration rests on a funda-
property measured over distributions, whereas certification
                                                                     mental computational asymmetry: for NP-complete prob-
is an instance property required for each output. Even
                                                                     lems, solving is hard (exponential), but verification is
99.9% expected accuracy leaves the question “is this spe-
                                                                     cheap (polynomial). A SAT formula may require expo-
cific output correct?” unanswerable from the model alone.
                                                                     nential search to satisfy, yet any proposed assignment can
Symbolic verification supplies exactly this missing per-
                                                                     be checked in linear time. This asymmetry suggests an op-
instance information: a binary signal (valid/invalid) that is
                                                                     timal division of labor: neural networks excel at efficient
perfectly calibrated by construction.
                                                                     generation through pattern recognition (System 1), while
                                                                     symbolic systems excel at rigorous verification through
3.3. Integration Enables Sample Efficiency                           constraint checking (System 2).
Claim 3. Neuro-symbolic approaches achieve substantial               We therefore advocate for a bidirectional strategy where
sample efficiency gains by delegating constraint satisfac-           each component compensates for the other’s deficits.
tion to symbolic solvers.

The resulting sample-efficiency gap is striking: NeurASP             4.1. Neural Methods Enhancing Symbolic Solvers
achieves 100% constraint satisfaction using only 25 train-           Symbolic solvers guarantee correctness but face two prac-
ing examples (Yang et al., 2020), whereas RRN requires               tical barriers: they struggle with unstructured inputs (the
216,000 examples to reach comparable in-distribution per-            symbol grounding problem), and generic heuristics may be
formance (Palm et al., 2018).                                        suboptimal for specific data distributions. Neural methods
This contrast follows directly from the “Learn vs. Spec-             address both.
ify” principle. In NeurASP, the neural component is tasked           Neural Perception (Symbol Grounding). Real-world
primarily with perception (mapping pixels to digits), while          constraints often operate on raw modalities like images or
constraint reasoning is enforced by predefined ASP rules.            text, which symbolic solvers cannot ingest. Neural en-
In RRN, the network must implicitly learn both the visual            coders bridge this gap by mapping raw perception to dis-
representation and the logical rules of Sudoku from data.            crete symbols. NeurASP (Yang et al., 2020) exemplifies
The orders-of-magnitude difference in sample efficiency is           this decomposition: a CNN grounds digit images to prob-
a predictable consequence of removing constraint satisfac-           ability distributions, while an ASP solver enforces Sudoku
tion from the hypothesis space.                                      constraints over these distributions. This separation allows
One might object that comparing NeurASP and RRN is                   the system to isolate perception errors (misreading a digit)
unfair because they do not instantiate identical learning            from reasoning errors (violating a constraint). Crucially,
problems. We view this mismatch not as a confounding                 while the neural component provides the specification, the
variable, but as the mechanism of action. The fact that              symbolic component ensures the satisfaction of that speci-
neuro-symbolic architectures allow us to simplify the learn-         fication.
ing problem—converting a reasoning task into a perception            Neural Heuristics (Learned Search). For hard instances,
task—is precisely why they are superior for constrained do-          the bottleneck is the search space. Deterministic solvers
mains.                                                               typically rely on generic heuristics (e.g., VSIDS). Neu-
Claim 3 measures paradigm cost, not the relative merit               ral networks can learn instance-specific distributions to

                                                                 5
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

guide this search, acting as a “learned intuition” that                Table 2. Three paradigms of neuro-symbolic integration; only
                                                                       Inversion of Control places a sound verifier on every output path.
prunes the search space without compromising soundness.
Approaches like Graph-Q-SAT (Kurin et al., 2020) and                     Paradigm       Examples              Failure / guarantee
AlphaGo’s MCTS (Silver et al., 2016) demonstrate that
                                                                         A. Soft sym- SATNet       (Wang ID 98.3%          →OOD
learned priors can speed up solving by orders of magni-                  bolic (regu- et al., 2019), Scal- 3.2% (Miyato et al.,
tude. The key property is that distribution shift degrades               larizer)     lop (Huang et al., 2025); silent failure, no
only efficiency, not correctness.                                                     2021)                fallback
                                                                         B. Ad-hoc LLM-                    Invocation hallucina-
4.2. Symbolic Methods Certifying Neural Outputs                          tool-use     Modulo      (Kamb- tion + output override
                                                                                      hampati et al., leave correctness prob-
The converse direction is the primary focus of this paper:                            2024),         Tool- abilistic
                                                                                      former      (Schick
ensuring trustworthiness. As Kambhampati et al. (2024)                                et al., 2023), Re-
argue, autoregressive models “cannot autonomously self-                               Act (Yao et al.,
verify” because they apply to verification the same learned                           2023b)
heuristics that produced the potentially flawed output. Self-            C. Inversion PVS (this paper), Every output traverses
verification is circular; external verification is foundational.         of Control ICF, BFS-Prover- V ; Prop. 5.1 gives a
                                                                                      V2                   structural guarantee
We formalize this strategy as Verification-Interposed Ex-
ecution. The system output ŷ is defined not as the direct
output of a neural function fθ , but as the conditional result
                                                                       (the model discards a correct symbolic result). PVS en-
of a gatekeeping function:
                                                                       forces an Inversion of Control: the verifier is a system-
          (                                                            level gatekeeper, and the proposer is architecturally pre-
            fθ (x)     if V ERIFY(fθ (x), C) = True
     ŷ =                                                    (1)       cluded from bypassing or overriding it. Proposition 5.1
            gsym (x) otherwise                                         states the resulting structural—rather than probabilistic—
                                                                       zero-violation guarantee.
where gsym is a sound symbolic solver (the fallback). For
Sudoku, verification takes less than 1µs (O(n2 )), which is            5. The Proposer-Verifier-Solver (PVS)
negligible compared to the ∼10ms required for neural in-
                                                                          Framework
ference. With AKOrN’s 89.5% OOD accuracy, this strat-
egy allows 89.5% of queries to use the fast neural path,               To operationalize the strategies in Section 4, we propose the
while the remaining 10.5% trigger the solver—ensuring                  Proposer-Verifier-Solver (PVS) framework. This archi-
100% certification with minimal amortized overhead.                    tecture fulfills the “multi-agent” proposition of our abstract
                                                                       by modeling constraint satisfaction as a collaborative con-
4.3. The Certification Invariant and Inversion of                      trol loop between a neural agent (optimized for efficiency)
     Control                                                           and a symbolic environment (optimized for correctness).
These strategies culminate in a single architectural in-
                                                                       5.1. Architectural Components
variant. The Certification Invariant: A reasoning sys-
tem is certified if and only if no output reaches the user             The framework F decomposes reasoning into three func-
without passing a symbolic constraint check. When hard                 tional modules:
constraints exist, verification is cheap, and violations are
costly, this distinction is not a matter of degree—it is cate-         1. The Neural Proposer (Pθ ): A learnable statistical
gorical. It separates systems that are “usually correct” from             model (e.g., Transformer, GNN) mapping inputs x to
those that are “provably correct.”                                        candidate assignments ŷ. Functioning as the “System
Inversion of Control vs. Prior Paradigms. The novelty                     1” agent, it prioritizes high-throughput generation and
here is not combining neural and symbolic computation,                    handles unstructured modalities but offers no correct-
but the architectural insistence that the symbolic verifier               ness guarantees.
be a mandatory gatekeeper at the system level rather than              2. The Symbolic Verifier (V ):           A deterministic
an optional aid (Table 2). Paradigm A softens discrete con-               polynomial-time function that checks if ŷ |= C.
straints into differentiable surrogates that hold only in ex-             Crucially, V returns structured diagnostics D (e.g.,
pectation; discrete rounding at inference reintroduces vio-               specific constraint violations) rather than a simple
lation risk. Paradigm B is the dominant LLM-agent pattern,                boolean, enabling targeted refinement.
but Kambhampati et al. (2024) document two systematic
failure modes—invocation hallucination (the model emits                3. The Symbolic Solver (S): A complete solver (e.g.,
an answer instead of calling the tool) and output override                Tdoku, SAT, ASP) acting as the fallback mechanism.

                                                                   6
                 Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

                                                                          gradients, the diagnostics Dt returned by V provide seman-
                                                                          tic, spatially localized grounding (e.g., “cell (3,4) conflicts
                                                                          with row 3”).
                                                                          ConstructFeedback: a cross-space conditioning oper-
                                                                          ator. C ONSTRUCT F EEDBACK maps symbolic diagnos-
                                                                          tics into a conditioning signal in the proposer’s native
                                                                          representation space. Three canonical realizations span
                                                                          the dominant proposer families: (i) LLMs: diagnostics
                                                                          are prepended as execution context, and in-context learn-
                                                                          ing (Brown et al., 2020) reshapes attention so the model
                                                                          corrects its output from verifier feedback without fine-
                                                                          tuning (Olausson et al., 2024). (ii) GNNs / message-
                                                                          passing: diagnostics become edge masks or penalty flags
                                                                          on violating nodes, conditioning the next forward pass on
                                                                          a modified graph. (iii) Energy-based / oscillator dynam-
                                                                          ics: diagnostics enter an additive symbolic-energy term
                                                                          Esym (y) that steers inference-time sampling (Du & Mor-
                                                                          datch, 2019); AKOrN’s Kuramoto oscillator dynamics with
Figure 2. The Proposer-Verifier-Solver (PVS) Architecture. The            energy-based voting (Section 3) instantiates this family.
neural agent generates candidates; the symbolic verifier acts as
a gatekeeper. Failed candidates trigger diagnostic feedback for
                                                                          Spatially localized diagnostics, not global traces. PVS is
refinement. If refinement fails, the symbolic solver serves as the        not classical guess-and-check (which discards and restarts)
safety net, ensuring the Certification Invariant is never violated.       nor CEGAR (Clarke et al., 2000) (which refines a global
                                                                          abstraction system-wide). Diagnostics are scoped to the
                                                                          current candidate: “cells (3,4) and (3,7) share value 5; row-
   It guarantees that a valid solution y ∗ or a proof of unsat-           3 all-different violated” (Sudoku); “file, line, column, AST
   isfiability is always attainable.                                      node, violation type” (code); UNSAT cores (SMT). Itera-
                                                                          tive refinement decreases fallback rate across rounds (CaR
5.2. The Multi-Agent Reasoning Loop                                       drives TSPTW-100 infeasibility from 38.22% to 0.03%
                                                                          within TR =10 steps).
Standard neural inference is a feed-forward process. We re-
structure this as an agentic refinement loop (Algorithm 1):
                                                                          5.3. Theoretical Guarantee: Asymmetric Trust
the Verifier produces structured diagnostics on each failed
candidate, and an operator C ONSTRUCT F EEDBACK (de-                      The central property of this framework is Asymmetric
fined below) folds those diagnostics into the proposer’s                  Trust. We place zero trust in the neural component’s re-
conditioning input without updating any parameters.                       liability, yet the system achieves a provable guarantee of
                                                                          correctness.
Algorithm 1 The PVS Agentic Control Loop
                                                                          Proposition 5.1 (Certification Preservation). For any in-
 1: Input: Observation x, Constraints C, Budget T                         put x and constraint set C, if the PVS framework returns an
 2: c0 ← x; ŷ0 ← Pθ (c0 ) {Initial proposal (System 1)}                  output y, then y |= C (or y is a verified proof of unsatisfia-
 3: for t = 0 to T do                                                     bility).
 4:    valid, Dt ← V (ŷt , C) {Dt : localized diagnostics}
 5:    if valid then                                                      Algorithm 1 has exactly two exit paths: Line 5 returns ŷt
 6:       return ŷt {Certified Fast Path}                                only after V certifies it, and Line 10 falls back to the sound,
 7:    end if                                                             complete solver S. Since no execution path bypasses a
 8:    ct+1 ← C ONSTRUCT F EEDBACK(x, ŷt , Dt ) {inject                  sound symbolic check, the system’s violation rate is struc-
       Dt into conditioning}                                              turally 0%, independent of Pθ ’s reliability.
 9:   ŷt+1 ← Pθ (ct+1 ) {Refinement (System 2)}
10: end for                                                               5.4. Cross-Domain Generalization Beyond Sudoku
11: return S(x) {Certified Safe Path (Fallback)}
                                                                          Table 3 summarizes three high-stakes domains where the
                                                                          propose–verify–refine pattern is now the leading approach.
The loop implements Test-Time Adaptation: only the
conditioning input ct changes across iterations; the pro-                 Code generation (verifier: compiler / unit tests): on Hu-
poser’s parameters θ are never updated. Unlike scalar loss                manEval Python, Reflexion’s verbal-feedback loop with

                                                                      7
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

Table 3. Cross-domain evidence for PVS-style pipelines. “Final”       B ENCH (Seely et al., 2025), a benchmark explicitly de-
is the certified rate after fallback/refinement.
                                                                      signed to test creative constraint reasoning, even frontier
Domain     (veri- Neural-only    Fallback     /      Final            models like GPT-5 achieve only 33% accuracy on the chal-
fier)             failure        refine                               lenge set. Specialized neural solvers like AKOrN (Miyato
Sudoku        OOD 10.5%        10.5%     →   100%
                                                                      et al., 2025) and ConsFormer (Xu et al., 2025) plateau well
(checker; ours) (AKOrN,        solver                                 above the <1% violation threshold despite massive test-
                   max    com-                                        time compute. Scale improves average-case intuition but
                   pute)                                              does not appear to yield the worst-case guarantees required
Code gen, Hu- 20% (GPT-4 verbal critic 91% (Reflexion)                for certification.
manEval (com- zero-shot        + test feed-
piler / tests)     pass@1)     back                                   Second, theoretical limitations suggest this is a category
Hard          VRP, 38.22%      ∼38%      →  99.97%                    error. Balestriero et al. (2021) prove that test predictions
TSPTW-100          (POMO)      0.03%
(feas. check)
                                                                      in high dimensions are geometrically equivalent to extrap-
Thm. proving, ∼47%             failed → BFS 95.08%                    olation. Furthermore, Xu et al. (2024) establish that for
miniF2F (Lean) (best ∼53% backtrack                                   any computable function approximated by a neural net-
                   pass@1)                                            work, there exist inputs where the model produces incorrect
                                                                      outputs. “Self-verification” does not solve this; it merely
                                                                      applies the same approximate heuristics to the output that
                                                                      generated it (circular certification).
self-generated tests improves GPT-4 pass@1 from 80%
to 91% (Shinn et al., 2023); failed candidates trig-                  Third, the economic argument favors integration. Even if
ger a reflection-conditioned regeneration instead of be-              scaling could achieve 99.99% satisfaction, a symbolic ver-
ing silently accepted. Hard vehicle routing (feasibility              ifier (running in < 1µs) combined with a fallback solver
checker): on TSPTW-100, AM/POMO produces 38.22%                       achieves 100% correctness at a fraction of the inference
infeasible routes (Bi et al., 2026); PIP (Bi et al., 2024) re-        cost. Using a trillion-parameter model to emulate a linear-
duces this to 6.96% and CaR (Bi et al., 2026) to 0.03%                time consistency check is a massive allocation inefficiency.
within ten refinement steps. Automated theorem prov-
ing (Lean kernel): best single-pass Kimina-Prover (Wang               6.2. Objection 2: “Tool Use Is Sufficient”
et al., 2025) reaches ∼53% pass@1; with the Lean kernel               Steelman Argument. We do not need intimate neuro-
as mandatory verifier at every BFS node, BFS-Prover-V2                symbolic integration because LLMs can simply invoke ex-
reaches 95.08% (Xin et al., 2025). In all four settings, the          ternal tools (Schick et al., 2023). An LLM that generates
same architectural pattern—fixed neural proposer, manda-              Python code to call a Z3 solver achieves perfect accuracy
tory symbolic verifier with structured diagnostics, sym-              without modifying the model architecture. Therefore, flex-
bolic fallback—separates probabilistic from certified cor-            ible “agentic” tool use supersedes the need for the special-
rectness.                                                             ized PVS frameworks proposed here.
                                                                      Response. We partially agree: tool-augmented LLMs are
6. Alternative Views                                                  a valid instance of symbolic integration. However, cur-
6.1. Objection 1: “Scale Will Eventually Solve It”                    rent implementations are unprincipled. The gap between
                                                                      “merely calling tools” and “reliably calling correct tools
Steelman Argument. The history of deep learning is a                  with correct inputs” is substantial. As noted by Kambham-
graveyard of symbolic objections. Domains once thought                pati et al. (2024), frontier agents exhibit three systematic
to require hard-coded priors—from protein folding to code             failure modes: invocation hallucination (the model emits
generation—were revolutionized by general-purpose scal-               an answer instead of calling the tool), formulation errors
ing. Recent reasoning models demonstrate emergent capa-               (translating the problem incorrectly into the solver’s lan-
bilities like self-correction and long-horizon planning. It           guage), and output override (ignoring the solver’s result
is reasonable to hypothesize that a sufficiently large neural         when it contradicts the model’s prior). Our position is not
solver, trained on vast datasets of constraints (e.g., gener-         against tool use but against ad-hoc tool use. We advocate
ated by solvers), effectively internalizes the logic of verifi-       for architectural enforcement: the tool invocation must
cation, closing the certification gap through sheer capacity          be triggered by formal conditions, and the solver’s output
rather than architectural hybridization.                              must be treated as authoritativerather than as just another
Response. We regard this as the strongest objection, yet              context token. Moreover, the verifier is the trust boundary:
it fails on three grounds: empirical, theoretical, and eco-           every output crosses it, and the proposer can neither by-
nomic. First, empirical evidence contradicts the “emer-               pass nor override it—the Inversion of Control absent from
gence” hypothesis for strict constraints. On S UDOKU -                Paradigm B (Table 2).

                                                                  8
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

6.3. Objection 3: “Real-World Constraints Are Too                   6.4. Objection 4: “Autoformalization and Neural
     Messy”                                                              Verifiers Suffice”
Steelman Argument. Sudoku features perfectly specified,             Steelman Argument. A growing line of work uses LLMs
complete, and static constraints. Real-world CSPs (e.g.,            as verifiers or autoformalizers: in theorem proving, an
supply chain logistics, legal compliance) involve partially         LLM can translate a natural-language proposal into Lean
known constraints, soft constraints with violation costs, or        and check it, or judge the proof directly. If the autoformal-
logically infeasible instances. Focusing on “NP-complete”           izer or neural judge is strong enough, an explicit symbolic
exact satisfaction is an academic idealization that does not        verifier may be unnecessary.
transfer to the noisy reality of deployment.
                                                                    Response. Autoformalization is crucial for domains whose
Response. While Sudoku is an idealized proxy, the prin-             constraints are not yet machine-checkable, but it does not
ciple of symbolic integration degrades gracefully in messy          displace symbolic certification. First, when an autoformal-
environments:                                                       izer feeds a sound symbolic kernel (Lean, Z3, Tdoku), the
                                                                    system is an instance of PVS: the proposer becomes “LLM
• Partially Known Constraints: Integration allows for a             + autoformalizer,” but the gatekeeper is still a sound veri-
  hybrid state. In drug discovery, known physics (e.g., va-         fier; the Certification Invariant holds, and Xin et al. (2025)
  lence rules) are enforced symbolically, while unknown             reach 95.08% on miniF2F precisely because the Lean ker-
  properties (e.g., toxicity) are approximated neurally. This       nel certifies every accepted step. Second, when the verifier
  yields partial certification—strictly better than zero cer-       is itself a learned neural judge, soundness becomes prob-
  tification.                                                       abilistic and we are back in Paradigm B of Table 2; even
• Soft Constraints: The framework adapts by shifting                strong learned verifiers exhibit false-accept rates incompat-
  from “check validity” to “compute cost.” Symbolic                 ible with the <1% violation threshold we adopt. Third, aut-
  solvers can compute exact penalty values for soft con-            oformalization is itself consistent with our call for bidirec-
  straints, providing a principled loss signal rather than a        tional integration—neural translation into symbolic repre-
  learned approximation of the loss.                                sentations, followed by symbolic certification—and so ex-
                                                                    pands the set of domains for which PVS applies rather than
• Infeasible Instances: When a problem has no solution,             supplanting the soundness requirement on the final verifier.
  a neural model often hallucinates a “best guess.” A sym-
  bolic solver returns UNSAT with a proof or a Minimal              7. Conclusion
  Unsatisfiable Core. This diagnostic value is unique to            We have defended a falsifiable position: when hard con-
  symbolic reasoning and critical for human decision sup-           straints are explicit, verification is cheap, and violations are
  port.                                                             costly, neural constraint reasoning must prioritize symbolic
                                                                    integration over pure learning. Neural-only solvers exhibit
Tiered verification and amortized cost. Where indus-
                                                                    persistent OOD violations that further test-time compute
trial verification itself is expensive (e.g., SMT-based pro-
                                                                    does not eliminate; “usually right” is epistemically dis-
gram checking), our position rests on relative asymme-
                                                                    tinct from “provably right”; and neuro-symbolic systems
try, not absolute cheapness: for any NP problem, verifi-
                                                                    achieve orders-of-magnitude gains in sample efficiency by
cation is asymptotically cheaper than exhaustive solving.
                                                                    delegating logic to solvers. Section 5.4 confirms the same
Practice further amortizes cost via multi-tier verification—
                                                                    pattern across code generation, hard vehicle routing, and
syntax/type checks before bounded model checking be-
                                                                    theorem proving.
fore full SMT (Newcombe et al., 2015; Brooker & De-
sai, 2024). In our experiment, 89.5% of candidates pass             Call to Action. We invite benchmark designers to consider
the O(n2 ) checker before any solver call, giving amortized         reporting Violation Rate alongside accuracy, together with
cost 0.895 · O(n2 ) + 0.105 · O(solver) per query. When             per-instance certification metadata that records whether
verification times out, PVS falls back to a safe template;          each output was verified, produced by symbolic fallback, or
partial certification is strictly safer than zero.                  left uncertified. We encourage system designers to explore
                                                                    the PVS pattern and suggest that certification status be re-
Verifier complexity across NP and beyond. Sudoku’s
                                                                    garded as a meaningful disclosure for “reasoning” claims
O(n2 ) verifier is heavier than that of most canonical
                                                                    on CSPs. We would warmly welcome attempts to refute the
NP-complete problems (3-SAT: O(n); Hamiltonian cycle:
                                                                    criterion stated in Section 1; such a refutation would mark a
O(n); graph k-coloring: O(|E|)); the asymmetric regime
                                                                    genuine breakthrough in the capacity of statistical learning
PVS exploits is the norm, not a Sudoku artifact. Beyond NP
                                                                    to approximate logic. Until then, we hope the community
(PSPACE/EXPTIME) exact verification may not be poly-
                                                                    will continue building systems that are provably right, not
nomial, but PVS retains value via cheap falsification and
                                                                    merely usually so.
bounded partial verification.

                                                                9
               Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

Acknowledgements                                                    Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan,
                                                                      J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,
This work was supported by the National Natural Sci-                  Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,
ence Foundation of China (Grant No. 62506090) and                     Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu,
the National Key R&D Program of China (Grant No.                      J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin,
2025YFF0523900).                                                      M., Gray, S., Chess, B., Clark, J., Berner, C., McCan-
                                                                      dlish, S., Radford, A., Sutskever, I., and Amodei, D.
References                                                            Language models are few-shot learners. In Advances
                                                                      in Neural Information Processing Systems (NeurIPS),
Amos, B. and Kolter, J. Z. OptNet: Differentiable opti-
                                                                      2020.
 mization as a layer in neural networks. In International
 Conference on Machine Learning (ICML), 2017.                       Chang, O., Flokas, L., Lipson, H., and Spranger, M. As-
                                                                      sessing SATNet’s ability to solve the symbol grounding
Anthropic.   Introducing the model context proto-
                                                                      problem. In Advances in Neural Information Process-
  col. Online announcement, November 2024. URL
                                                                      ing Systems (NeurIPS 2020), volume 33, pp. 1428–1439,
  https://www.anthropic.com/news/model-
                                                                      2020. Critical analysis of SATNet’s symbol grounding
  context-protocol.
                                                                      capabilities.
Balestriero, R., Pesenti, J., and LeCun, Y. Learning in high
                                                                    Clarke, E., Grumberg, O., Jha, S., Lu, Y., and Veith, H.
  dimension always amounts to extrapolation, 2021. URL
                                                                      Counterexample-guided abstraction refinement. In Com-
  https://arxiv.org/abs/2110.09485.
                                                                      puter Aided Verification (CAV), 2000.
Besta, M., Blach, N., Kubicek, A., Gerstenberger, R., Pod-
                                                                    Crook, J. F. A pencil-and-paper algorithm for solving su-
  stawski, M., Gianinazzi, L., Gajda, J., Lehmann, T.,
                                                                      doku puzzles. Notices of the American Mathematical
  Niewiadomski, H., Nyczyk, P., and Hoefler, T. Graph
                                                                      Society, 56(4):460–468, 2009.
  of thoughts: Solving elaborate problems with large lan-
  guage models. In Proceedings of the AAAI Confer-                  Davis, L. and Ji, T. Evaluating SAT and SMT solvers on
  ence on Artificial Intelligence (AAAI 2024), pp. 17682–             large-scale Sudoku puzzles, January 2025.
  17690, 2024. doi: 10.1609/aaai.v38i16.29720.
                                                                    Dillon, T. Tdoku: A fast sudoku solver and gener-
Bi, J., Ma, Y., Zhou, J., Song, W., Cao, Z., Wu, Y., and              ator. GitHub repository, 2019. URL https://
  Zhang, J. Learning to handle complex constraints for                github.com/t-dillon/tdoku.
  vehicle routing problems. In Advances in Neural Infor-
  mation Processing Systems (NeurIPS), 2024.                        DiMasi, J. A., Grabowski, H. G., and Hansen,
                                                                      R. W.       Innovation in the pharmaceutical indus-
Bi, J., Cao, Z., Zhou, J., Song, W., Wu, Y., Zhang, J.,               try: New estimates of R&D costs.        Journal of
  Ma, Y., and Wu, C. Towards efficient constraint han-                Health Economics, 47:20–33, 2016. doi: 10.1016/
  dling in neural solvers for routing problems. In Interna-           j.jhealeco.2016.01.012. URL https://doi.org/
  tional Conference on Learning Representations (ICLR),               10.1016/j.jhealeco.2016.01.012.
  2026. URL https://iclr.cc/virtual/2026/
  poster/10007139.                                                  Du, Y. and Mordatch, I. Implicit generation and model-
                                                                      ing with energy-based models. In Advances in Neural
Biere, A., Fazekas, K., Fleury, M., and Heisinger, M. CaD-            Information Processing Systems (NeurIPS), 2019.
  iCaL, Kissat, Paracooba, Plingeling and Treengeling en-
  tering the SAT competition 2020. In Balyo, T., Froleyks,          Du, Y., Mao, J., and Tenenbaum, J. B. Learning it-
  N., Heule, M. J. H., Iser, M., Järvisalo, M., and Suda,            erative reasoning through energy diffusion. In Pro-
  M. (eds.), Proceedings of SAT Competition 2020: Solver              ceedings of the 41st International Conference on Ma-
  and Benchmark Descriptions, volume B-2020-1 of De-                  chine Learning, volume 235 of Proceedings of Machine
  partment of Computer Science Series of Publications B,              Learning Research, pp. 11764–11776. PMLR, July
  pp. 50–53. University of Helsinki, 2020. URL https:                 2024. URL https://proceedings.mlr.press/
  //researchportal.helsinki.fi/files/                                 v235/du24f.html.
  142452772/sc2020_proceedings.pdf. Han-
  dle: http://hdl.handle.net/10138/318450.                          Eén, N. and Sörensson, N. An extensible SAT-solver. In
                                                                       Giunchiglia, E. and Tacchella, A. (eds.), Theory and
Brooker, M. and Desai, A. Systems correctness practices                Applications of Satisfiability Testing (SAT 2003), Se-
  at AWS: Leveraging formal and semi-formal methods.                   lected Revised Papers, volume 2919 of Lecture Notes in
  ACM Queue, 22(6):79–96, 2024. doi: 10.1145/3712057.                  Computer Science, pp. 502–518. Springer, 2004. doi:

                                                               10
               Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

  10.1007/978-3-540-24605-3 37. Conference held in                 Conference on Programming Language Design and Im-
  2003; proceedings published by Springer in 2004.                 plementation (PLDI 2023), pp. 1463–1487, 2023. doi:
                                                                   10.1145/3591280.
Garey, M. R. and Johnson, D. S. Computers and In-
  tractability: A Guide to the Theory of NP-Completeness.        Liang, H. Sudoku solver MCP server. GitHub repository,
  W. H. Freeman, 1979.                                             2025. URL https://github.com/Skywalker-
                                                                   Harrison/mcp-soduku.
Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q.
  On calibration of modern neural networks. In Pro-              Lloyd, H. and Amos, M. Solving sudoku with ant colony
  ceedings of the 34th International Conference on Ma-             optimization. IEEE Transactions on Games, 12(3):302–
  chine Learning (ICML), volume 70 of Proceedings of               311, 2020. Also available as arXiv:1805.03545.
  Machine Learning Research, pp. 1321–1330. PMLR,                Long, J. Large language model guided tree-of-thought,
  2017. URL https://proceedings.mlr.press/                         2023. Independent work from Yao et al.; applies Tree-
  v70/guo17a.html.                                                 of-Thoughts to Sudoku solving.
Huang, J., Li, Z., Chen, B., Samel, K., Naik, M., Song,          Lynce, I. and Ouaknine, J. Sudoku as a SAT problem. In
  L., and Si, X. Scallop: From probabilistic deduc-                Proceedings of the 9th International Symposium on Arti-
  tive databases to scalable differentiable reasoning. In          ficial Intelligence and Mathematics (ISAIM), Fort Laud-
  Advances in Neural Information Processing Systems                erdale, Florida, 2006. URL https://dblp.org/
  (NeurIPS 2021), volume 34, pp. 25134–25145, 2021.                rec/conf/isaim/LynceO06.html.

Kambhampati, S., Valmeekam, K., Guan, L., Verma,                 Maiya, A., Alghamdi, R., Pacheco, M. L., Trivedi, A.,
  M., Stechly, K., Bhambri, S., Saldyt, L., and                   and Somenzi, F. Explaining puzzle solutions in nat-
  Murthy, A. Position: LLMs can’t plan, but can                   ural language: An exploratory study on 6x6 sudoku.
  help planning in LLM-modulo frameworks.       In                In Che, W., Nabende, J., Shutova, E., and Pilehvar,
  Proceedings of the 41st International Conference                M. T. (eds.), Findings of the Association for Compu-
  on Machine Learning, volume 235 of Proceedings                  tational Linguistics: ACL 2025, pp. 3002–3009, Vi-
  of Machine Learning Research, pp. 22895–22907,                  enna, Austria, July 2025. Association for Computa-
  2024. URL https://proceedings.mlr.press/                        tional Linguistics. doi: 10.18653/v1/2025.findings-
  v235/kambhampati24a.html.                                       acl.155.    URL https://aclanthology.org/
                                                                  2025.findings-acl.155/.
Knuth, D. E. Dancing Links. In Davies, J., Roscoe,
  B., and Woodcock, J. (eds.), Millennial Perspectives in        Mantere, T. and Koljonen, J. Solving, rating and gener-
  Computer Science: Proceedings of the 1999 Oxford-               ating sudoku puzzles with GA. In IEEE Congress on
  Microsoft Symposium in Honour of Sir Tony Hoare,                Evolutionary Computation (CEC 2007), pp. 1382–1389,
  pp. 187–214. Palgrave Macmillan, Houndmills, Bas-               2007.
  ingstoke, Hampshire, UK, 2000. Also available as               Miyato, T., Löwe, S., Geiger, A., and Welling, M.
  arXiv:cs/0011047.                                               Artificial kuramoto oscillatory neurons. In Interna-
                                                                  tional Conference on Learning Representations (ICLR
Knuth, D. E. The Art of Computer Programming, Volume
                                                                  2025), 2025. URL https://www.cvlibs.net/
  4, Fascicle 5: Mathematical Preliminaries Redux; In-
                                                                  publications/Miyato2025ICLR.pdf. Oral pre-
  troduction to Backtracking; Dancing Links. Addison-
                                                                  sentation; also available as arXiv:2410.13821.
  Wesley Professional, 2019. ISBN 978-0134671796.
                                                                 Model Context Protocol Contributors.     Model
Kurin, V., Godil, S., Whiteson, S., and Catanzaro, B. Can         context protocol specification (version 2025-
  Q-learning with graph networks learn a generalizable            03-26).    Online specification, 2025.   URL
  branching heuristic for a SAT solver? In Advances               https://modelcontextprotocol.io/
  in Neural Information Processing Systems (NeurIPS),             specification/2025-03-26.
  2020. arXiv:1909.11830.
                                                                 Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker,
Lewis, R. Metaheuristics can solve sudoku puzzles. Jour-           M., and Deardeuff, M. How Amazon Web Services uses
  nal of Heuristics, 13(4):387–401, 2007. doi: 10.1007/            formal methods. Communications of the ACM, 58(4):
  s10732-007-9012-8.                                               66–73, 2015.
Li, Z., Huang, J., and Naik, M. Scallop: A language              Norvig, P. Solving every sudoku puzzle. Online essay,
  for neurosymbolic programming. In ACM SIGPLAN                    2006. URL https://norvig.com/sudoku.html.

                                                            11
                Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

Olausson, T. X., Inala, J. P., Wang, C., Gao, J., and Solar-          Tekin, E., Garg, A., and Venkatesh, G. From zero to sudoku
  Lezama, A. Is self-repair a silver bullet for code gener-             hero: An RL adventure. Cerebras blog, August 2025.
  ation? In International Conference on Learning Repre-                 URL https://www.cerebras.ai/blog/from-
  sentations (ICLR), 2024.                                              zero-to-sudoku-hero-an-rl-adventure.

Palm, R. B., Paquet, U., and Winther, O. Recurrent rela-              Töenshoff, J., Ritzert, M., Wolf, H., and Grohe, M. Graph
  tional networks. In Advances in Neural Information Pro-                neural networks for maximum constraint satisfaction.
  cessing Systems (NeurIPS 2018), volume 31, pp. 3368–                   Frontiers in Artificial Intelligence, 3:580607, 2021. doi:
  3378, 2018.                                                            10.3389/frai.2020.580607. RUN-CSP evaluated on bi-
                                                                         nary CSPs (Max-2-SAT, Max-Cut, 3-Colorability), not
Régin, J.-C. A filtering algorithm for constraints of differ-           directly on Sudoku.
   ence in CSPs. In Proceedings of the Twelfth AAAI Na-
   tional Conference on Artificial Intelligence (AAAI-94),            Topan, S., Rolnick, D., and Si, X. Techniques for symbol
   pp. 362–367, Seattle, Washington, 1994.                              grounding with SATNet. In Advances in Neural Infor-
                                                                        mation Processing Systems (NeurIPS 2021), volume 34,
Sato, Y. and Inoue, H. Solving sudoku with genetic opera-               pp. 20733–20744, 2021.
  tions that preserve building blocks. In IEEE Conference
  on Computational Intelligence and Games (CIG 2010),                 United States Government Accountability Office. Air-
  pp. 23–29, Copenhagen, Denmark, 2010.                                 line passenger protections: More data and analysis
                                                                        needed to understand effects of flight delays. Techni-
Sato, Y., Hasegawa, N., and Sato, M. GPU acceleration                   cal Report GAO-11-733, GAO, 2011. URL https://
  for sudoku solution with genetic operations. In IEEE                  www.gao.gov/products/gao-11-733. Accessed
  Congress on Evolutionary Computation (CEC 2011), pp.                  2026-01-19.
  296–303, 2011.
                                                                      Wang, C., Sun, B., Du, K.-J., Li, J.-Y., Zhan, Z.-H., Jeon,
Schick, T., Dwivedi-Yu, J., Dessı̀, R., Raileanu, R.,                  S.-W., Wang, H., and Zhang, J. A novel evolutionary
  Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda,                   algorithm with column and sub-block local search for
  N., and Scialom, T. Toolformer: Language models can                  sudoku puzzles. IEEE Transactions on Games, 16(1):
  teach themselves to use tools. In Advances in Neu-                   162–172, March 2024. doi: 10.1109/TG.2023.3236490.
  ral Information Processing Systems (NeurIPS), 2023.                  Early access online January 2023; journal issue March
  arXiv:2302.04761.                                                    2024.
Seely, J., Imajuku, Y., Zhao, T., Cetin, E., and Jones, L.            Wang, H., Ünsal, M., Lin, X., Baksys, M., Liu, J., Dos San-
  Sudoku-bench: Evaluating creative reasoning with Su-                 tos, M., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., Lu, J.,
  doku variants, 2025. Sakana AI.                                      de Saxcé, H., Bailey, B., Song, C., Xiao, C., Ma, D.,
                                                                       Fan, Y., Guo, H., Zhou, Y., He, W., Wu, Y., Xing, Y.,
Shah, K., Dikkala, N., Wang, X., and Panigrahy, R. Causal              Wang, J., Chen, Y., Zheng, W., Wang, R., Zhang, Y.,
  language modeling can elicit search and reasoning ca-                Yao, Y., Huang, L., Zhu, M., Yan, J., Cheng, J., Liu, Y.,
  pabilities on logic puzzles. In Advances in Neural                   Liu, X., Mou, R., Du, L., Anthony, Q., Mao, Y., Chen,
  Information Processing Systems (NeurIPS 2024), vol-                  J., Wang, J., and Wang, L. Kimina-prover preview: To-
  ume 37, 2024. URL https://arxiv.org/abs/                             wards large formal reasoning models with reinforcement
  2409.10502.                                                          learning, 2025.
Shinn, N., Cassano, F., Berman, E., Gopinath, A.,                     Wang, P.-W., Donti, P. L., Wilder, B., and Kolter, J. Z.
  Narasimhan, K., and Yao, S. Reflexion: Language                      SATNet: Bridging deep learning and logical reasoning
  agents with verbal reinforcement learning. In Advances               using a differentiable satisfiability solver. In Interna-
  in Neural Information Processing Systems (NeurIPS),                  tional Conference on Machine Learning (ICML 2019),
  2023. arXiv:2303.11366.                                              volume 97 of PMLR, pp. 6545–6554, 2019.
Silver, D., Huang, A., Maddison, C. J., Guez, A., Sifre, L.,          Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
   Van Den Driessche, G., Schrittwieser, J., Antonoglou, I.,           Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
   Panneershelvam, V., Lanctot, M., Dieleman, S., Grewe,               prompting elicits reasoning in large language models.
   D., Nham, J., Kalchbrenner, N., Sutskever, I., Lillicrap,           In Advances in Neural Information Processing Systems
   T., Leach, M., Kavukcuoglu, K., Graepel, T., and Has-               (NeurIPS 2022), volume 35, pp. 24824–24837, 2022.
   sabis, D. Mastering the game of go with deep neural
   networks and tree search. Nature, 529(7587):484–489,               Wouters, O. J., McKee, M., and Luyten, J. Estimated re-
   2016.                                                               search and development investment needed to bring a

                                                                 12
               Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

  new medicine to market, 2009–2018. JAMA, 323(9):
  844–853, 2020. doi: 10.1001/jama.2020.1166. URL
  https://doi.org/10.1001/jama.2020.1166.
Xin, R., Zheng, Z., Nie, Y., Yuan, K., and Xiao, X. Scaling
  up multi-turn off-policy RL and multi-agent tree search
  for LLM step-provers, 2025. Introduces the BFS-Prover-
  V2 theorem-proving system.
Xu, Y., Li, W., Sanner, S., and Khalil, E. B. Self-
  supervised transformers as iterative solution improvers
  for constraint satisfaction. In International Conference
  on Machine Learning (ICML 2025), 2025. Also avail-
  able as arXiv:2502.15794.

Xu, Z., Jain, S., and Kankanhalli, M. Hallucination
  is inevitable: An innate limitation of large language
  models, 2024. URL https://arxiv.org/abs/
  2401.11817.

Yang, Z., Ishay, A., and Lee, J. NeurASP: Embracing neu-
  ral networks into answer set programming. In Proceed-
  ings of the Twenty-Ninth International Joint Conference
  on Artificial Intelligence (IJCAI 2020), pp. 1755–1762,
  2020. doi: 10.24963/ijcai.2020/243.

Yang, Z., Ishay, A., and Lee, J. Learning to solve con-
  straint satisfaction problems with recurrent transformer.
  In International Conference on Learning Representa-
  tions (ICLR 2023), 2023.
Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T. L.,
  Cao, Y., and Narasimhan, K. Tree of thoughts: De-
  liberate problem solving with large language models.
  In Advances in Neural Information Processing Systems
  (NeurIPS 2023), volume 36, 2023a.
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan,
  K., and Cao, Y. ReAct: Synergizing reasoning and act-
  ing in language models. In International Conference on
  Learning Representations (ICLR 2023), 2023b.
Yato, T. and Seta, T. Complexity and completeness of find-
  ing another solution and its application to puzzles. IE-
  ICE Transactions on Fundamentals of Electronics, Com-
  munications and Computer Sciences, E86-A(5):1052–
  1060, May 2003.




                                                              13
                                   Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

                                                                                                          Exact Cover and Dancing Links(Knuth, 2000; 2019)
                                                              Combinatorial Search and
                                                               Constraint Satisfaction
                                                                                                     Constraint Satisfaction Programming(Régin, 1994; Crook, 2009)

                                                                                                            Boolean Satisfiability (SAT)(Lynce & Ouaknine,
                                                                 Logic-Based Satisfi-                       2006; Eén & Sörensson, 2004; Biere et al., 2020)
                                         Deterministic           ability Approaches
                                                                                                         Satisfiability Modulo Theories (SMT)(Davis & Ji, 2025)


                                                                                                                 Norvig-style Propagation(Norvig, 2006)
                                                               High-Performance Hy-
                                                               brid Implementations
                                                                                                                          Tdoku(Dillon, 2019)



                                                                Simulated Annealing                                Simulated Annealing(Lewis, 2007)


                                                                                                          Genetic Algorithms(Mantere & Koljonen, 2007; Sato
                                         Metaheuristic           Genetic Algorithms
                                                                                                          & Inoue, 2010; Wang et al., 2024; Sato et al., 2011)
               Sudoku Solving Methods




                                                              Ant Colony Optimization                       Ant Colony Optimization(Lloyd & Amos, 2020)


                                                                                                        Recurrent Relational Networks (RRN)(Palm et al., 2018)
                                                          Graph Message Passing Networks
                                                                                                     RUN-CSP: Learning Without Solutions(Töenshoff et al., 2021)


                                                                                                                Recurrent Transformer(Yang et al., 2023)

                                                                  Transformer Ar-                   ConsFormer: Self-Supervised Constraint Learning(Xu et al., 2025)
                                                                 chitectures for CSP

                                                                                                           IRED: Energy-Based Optimization(Du et al., 2024)


                                        Learning-based     Advanced Neural Architectures                    AKOrN: Oscillatory Neurons(Miyato et al., 2025)

                                                                                                           SATNet and the Symbol Grounding Problem(Wang
                                                                Differentiable Solvers                     et al., 2019; Chang et al., 2020; Topan et al., 2021)

                                                                                                                       NeurASP(Yang et al., 2020)
                                                            Neuro-Symbolic Programming
                                                                                                               Scallop(Huang et al., 2021; Li et al., 2023)


                                                              Autoregressive Language
                                                                                                    Autoregressive Language Modeling for Sudoku(Shah et al., 2024)
                                                               Modeling for Sudoku

                                                                                                               Chain-of-Thought (CoT)(Wei et al., 2022)

                                           Language-          Structured Prompting and
                                                                                                         Tree-of-Thoughts (ToT)(Yao et al., 2023a; Long, 2023)
                                          Conditioned           Search over Thoughts

                                                                                                              Graph-of-Thoughts (GoT)(Besta et al., 2024)


                                                                                                                The ReAct Framework(Yao et al., 2023b)


                                                                                                     Hybrid LLM-Solver Systems(Liang, 2025; Model Context Pro-
                                                          AI Agents with Tools and Verifiers         tocol Contributors, 2025; Anthropic, 2024; Maiya et al., 2025)

                                                                                                    GRPO and Reinforcement Learning for Sudoku(Tekin et al., 2025)


Figure 3. Comprehensive taxonomy of Sudoku solving methods. Four paradigms are distinguished by color: Deterministic (green)
methods guarantee correctness by construction; Metaheuristic (yellow-green) methods use stochastic search; Learning-based (yellow)
methods learn from data; Language-conditioned (orange) methods leverage large language models. Only deterministic methods and
neuro-symbolic hybrids (which delegate to symbolic solvers) can certify constraint satisfaction.


A. Taxonomy of Sudoku Solving Methods
Figure 3 provides a comprehensive taxonomy of Sudoku solving methods across four paradigms.




                                                                                               14
               Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

Algorithm 2 Sudoku Solution Verification
 1: procedure V ERIFY S UDOKU(grid)
 2: n ← 9
 3: expected ← {1, 2, 3, 4, 5, 6, 7, 8, 9}
 4: // Check rows
 5: for r = 0 to n − 1 do
 6:    if set(grid[r]) ̸= expected then
 7:       return FALSE
 8:    end if
 9: end for
10: // Check columns
11: for c = 0 to n − 1 do
12:    column ← { grid[r][c] : r ∈ {0, . . . , n − 1} }
13:    if column ̸= expected then
14:       return FALSE
15:    end if
16: end for
17: // Check 3×3 boxes
18: for br = 0 to 2 do
19:    for bc = 0 to 2 do
20:       box ← { grid[3br + dr][3bc + dc] : dr, dc ∈ {0, 1, 2} }
21:       if box ̸= expected then
22:          return FALSE
23:       end if
24:    end for
25: end for
26: return T RUE
27: end procedure




B. Verification Algorithm
All paradigms ultimately require verifying candidate solutions. The following procedure checks whether a filled 9×9 grid
satisfies Sudoku constraints.
Complexity: O(n2 ) for an n × n grid.

C. Complexity Summary


                                  Table 4. Computational Complexity Summary (high level)

             Method                           Time (Worst)          Time (Typical)   Certificate
             Deterministic
             DLX / SAT / ASP                  exponential           µs–s             Yes (assignment / proof)
             Metaheuristic
             SA / GA / ACO                    –                     ms–s             No (needs verifier)
             Learning-based
             RRN / SATNet / ConsFormer        –                     ms–s             No (needs verifier)
             Hybrid
             NeurASP / Tool+Solver            solver-dependent      ms–s             Yes (via symbolic)




                                                            15
               Position: Certified Correctness in Neural Constraint Reasoning Requires Symbolic Integration

D. Additional Application Domains
The position generalizes beyond Sudoku whenever constraints are specifiable and checkable:

• Drug discovery: valence rules, PAINS filters, Lipinski constraints; violations can cost $1–2.6B per failed candidate (Di-
  Masi et al., 2016; Wouters et al., 2020).

• Flight scheduling: duty limits, rest requirements, maintenance windows; violations can trigger large passenger disruption
  costs (United States Government Accountability Office, 2011).
• Circuit design: timing, power, and design-rule checks; violations can cost millions per respin.

E. Theoretical Background
E.1. Why Neural Networks Cannot Guarantee Constraint Satisfaction
Proposition E.1 (Extrapolation Regime). In high-dimensional input spaces, neural network predictions on test data almost
always involve extrapolation beyond the training distribution (Balestriero et al., 2021).
Proposition E.2 (Hallucination Inevitability). For any computable function f , there exist inputs where a trained model M
produces M (x) ̸= f (x) with non-negligible probability (Xu et al., 2024).

Implication. Unconstrained, data-implied neural networks learn statistical regularities, not logical necessities. They
satisfy constraints often, not always; guarantees arise only when constraint structure is injected by design (architectural
constraints) or enforced by explicit symbolic verification/solving. Hence the need for symbolic certification when viola-
tions are costly and constraints are cheap to verify.




                                                            16
