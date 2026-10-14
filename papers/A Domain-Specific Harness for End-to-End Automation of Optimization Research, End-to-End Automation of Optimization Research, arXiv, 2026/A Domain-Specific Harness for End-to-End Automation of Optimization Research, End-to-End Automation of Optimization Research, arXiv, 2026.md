                                                          A Domain-Specific Harness for
                                                 End-to-End Automation of Optimization Research

                                                       Heechang Kim                     Ernest Ryu               Shuvomoy Das Gupta
                                                   Seoul National University              UCLA                       Rice University
                                                   heechang.kim@snu.ac.kr           eryu@math.ucla.edu              sd158@rice.edu




                                                                                          Abstract
arXiv:2608.07407v1 [math.OC] 7 Aug 2026




                                               We present AutoOPT, a domain-specific harness for end-to-end automation of optimization re-
                                               search. AutoOPT organizes the discovery of optimal first-order methods into four stages: numer-
                                               ical design through the BnB-PEP methodology; symbolic discovery of the analytic description
                                               and a convergence proof through frontier large language models (LLMs); formal verification in
                                               the Lean 4 proof assistant; and human interpretation and write-up. We demonstrate the frame-
                                               work on two case studies, each of independent interest. The first, lemniscate acceleration, is a
                                               new accelerated gradient method for minimizing the gradient norm of a smooth convex function:
                                               after N gradient steps it reduces the squared gradient norm at the optimal O(1/N 4 ) rate, with
                                               a constant governed by the lemniscate constant ϖ, a classical elliptic-integral constant. The
                                               second is the analytic description of ITEM-f, a method previously known only numerically: for
                                               L-smooth, µ-strongly convex minimization
                                                                                      p it contracts the function-value gap at an accelerated
                                               linear rate with a per-step factor (1 − µ/L)2 . The convergence theorems of both case studies
                                               are formalized and machine-checked in Lean 4.


                                          Preface
                                          In an era where frontier large language models (LLMs) provide remarkable mathematical intelli-
                                          gence, what role remains for human researchers? In this work, we (human experts) augment the
                                          general-purpose intelligence of LLMs with a technical domain-specific numerical methodology, and
                                          automate optimization research end-to-end, at a level not yet possible with LLMs alone. We hope
                                          this shows the community one way domain experts can productively contribute in an AI-driven
                                          research workflow: by augmenting the LLM’s general-purpose intelligence with a domain-specific
                                          harness derived from their expertise.


                                          1   Introduction
                                          Since the pioneering work of Nesterov on accelerated gradient methods [43] and of Nemirovsky and
                                          Yudin on information-based complexity [42], the design of eﬀicient and optimal first-order methods
                                          has been a central pursuit in the study of large-scale optimization. The performance estimation
                                          programming (PEP) framework [19, 65, 63] turned this pursuit into a computer-assisted discipline



                                                                                              1
by formulating the worst-case performance computation of a first-order method as a convex semidef-
inite program (SDP). Since its inception, PEP has produced many notable algorithms including
the optimized gradient method (OGM) [30, 17], its gradient-norm counterpart OGM-G [31], the
information-theoretic exact method (ITEM) [62, 18]. Designing an optimal method through the
PEP framework reduces to optimizing over the space of methods and branch-and-bound perfor-
mance estimation programming (BnB-PEP) [14] formulates this design process as a nonconvex
quadratically constrained quadratic program (QCQP) and solves it to global optimality using a
spatial branch-and-bound algorithm.
Yet, this computer-assisted methodology can be heavily labor-intensive: every stage from numer-
ically computing the method to coming up with the analytical form of the algorithm and its
convergence analysis demands deep domain expertise, and the rate of discovery is set by human
effort. While recent open-source packages such as PESTO [64] and PEPit [22] can help by solving
the worst-case SDP numerically, they come at the cost of a rigid, language-specific syntax and a
PEP derivation encoded in low-level library code that can be diﬀicult for newcomers to parse or
modify. Meanwhile, large language models (LLMs) and LLM-driven agents have begun to produce
genuine algorithmic and mathematical discoveries, which we review in Section 1.2. The natural
next step is to combine LLMs with these classical computer-assisted tools to further accelerate
research in optimization.
                       Numerically                      Candidate
   1
                        optimal
                                   2                    theorems 3                        Verified
                                                                                                     4
       Numerical        method                          & proofs                         theorems           Human
                                     Discovery of                        Formal
       design of                                                                                         interpretation
                                   analytical results                  verification
   optimal algorithm     human                           human                             human           & write-up
                        approval                        approval                          approval
  records &
   retrieves
                                                 Research workspace
                                         persistent memory of the research project
                              goals · sources · claims & evidence · experiments · next steps
    Figure 1: The researcher operates AutoOPT by conversing with an LLM agent in a research
    workspace in four stages. Stage 1 numerically designs an optimal first-order method for the problem
    class that the researcher specifies. Stage 2 consults a frontier LLM to propose an analytic form
    of the numerically designed method along with candidate convergence proofs. Stage 3 formally
    verifies the candidate theorems and proofs in the Lean proof assistant, ensuring every proof step is
    correct and explicit. In Stage 4, human authors interpret the verified results and write them up.


1.1 Contribution.
This work presents AutoOPT, a domain-specific harness that end-to-end automates optimization
research by combining the computer-assisted PEP methodology with LLMs and Lean formalization;
Figure 1 illustrates the pipeline.
We demonstrate AutoOPT on two case studies, each producing a result of independent interest.
The first case study, lemniscate acceleration (Section 4.1), is a new accelerated gradient method for
minimizing the gradient norm of an L-smooth convex function f with a minimizer x⋆ . From any
initial point x0 , its final iterate xN satisfies
                                                           ϖ4 L2 kx0 − x⋆ k2
                                        k∇f (xN )k2 ≤                        ,
                                                               (N + 1)4

                                                            2
where ϖ ≈ 2.622 is the lemniscate constant. This rate is optimal in its N -dependence [40, 41],
and its constant improves upon the previous best guarantee, obtained by concatenating OGM and
OGM-G, by a factor of about 1.35 (Section 4.1). To the best of our knowledge, this is the first time
the lemniscate constant and its associated elliptic functions have been connected to optimization
theory.
The second case study, analytic ITEM-f, (Section 4.2) is the optimal method for minimizing an
L-smooth, µ-strongly convex function f with minimizer x⋆ together with the accelerated linear rate
                                                 r 2N
                                                   µ
                        f (xN ) − f (x⋆ ) ≤ 4 1 −       (f (x0 ) − f (x⋆ )) ,
                                                   L
                                     p     2
whose per-step contraction factor 1 − µ/L matches the asymptotics of the complexity lower
bound [18]. ITEM-f was previously available only through numerical values [62, Appendix E]. We
formalize and machine-check the main convergence theorems of both lemniscate acceleration and
ITEM-f in Lean 4 with mathlib [16, 66].
More broadly, this work serves as a case study on how domain experts can contribute productively
to an AI-driven research workflow by designing and utilizing a domain-specific harness.

1.2 Prior work
AI-driven discovery and domain-specific harnesses. A rapidly growing body of work uses LLMs
and related search methods as discovery engines. Evolutionary symbolic search produced the Lion
optimizer [11]; AlphaTensor discovered faster matrix multiplication algorithms through reinforce-
ment learning [20]; and FunSearch and AlphaEvolve couple LLM code generation with automatic
evaluation to find new mathematical constructions and algorithmic improvements [55, 46]. At
the level of whole research programs, the AI Scientist pursues end-to-end automation of machine-
learning research [34, 35]; Aletheia reports research-level problem solving in mathematics [21]; an
internal version of OpenAI’s unreleased Astra model solved ten long-open problems in mathematics
and theoretical computer science, with each argument formalized in Lean [52]; and, with the Lean
4 proof assistant and its mathematical library mathlib [16, 66] now mature enough to formalize
research-level mathematics, AI-driven formal proof search has resolved open problems [67]. In the
natural sciences, AlphaFold and RoseTTAFold transformed protein-structure prediction [28, 8], and
the Virtual Lab coordinates a team of scientific agents that designed and experimentally validated
new nanobodies [61].
In the modern parlance of agentic AI, a harness is the scaffolding built around an LLM, includ-
ing the tools, prompts, workflows, and verification loops. We define a domain-specific harness to
be a harness designed with expert domain knowledge for the purpose of augmenting the general-
purpose intelligence of LLMs with the specialized methodology of a technical domain. Despite the
large body of work using LLMs to conduct mathematical research, most of it operates the models
through simple chat interfaces, and instances of domain-specific harnesses are not yet common.
Although their authors do not use the term, AlphaEvolve [46] and Aletheia [21] can be regarded
as domain-specific harnesses: AlphaEvolve targets scientific and algorithmic discovery across a
range of computational problems, whereas Aletheia targets mathematical research. Both systems,
however, remain broad in scope and were built in industry research labs with very large inference


                                                 3
compute budgets. In contrast, AutoOPT specializes further, to the domain of first-order optimiza-
tion research, and demonstrates this research principle at an academic scale of compute and token
usage.

Computer-assisted design of optimization methods. The performance estimation methodology
originates with Drori and Teboulle [19], who formulated the worst-case performance of a fixed-
step first-order method as an optimization problem and bounded it through an SDP relaxation;
Taylor, Hendrickx, and Glineur proved the relaxation exact through convex interpolation [65] and
then extended the framework to the composite setup in [63]. The methodology has since driven a
sequence of discoveries. Drori and Teboulle numerically constructed OGM [19], Kim and Fessler
found its analytic description [30], and Drori proved its exact optimality through a matching lower
bound [17]. Kim and Fessler constructed OGM-G, with the best known rate for reducing the
gradient norm of smooth convex functions [31]. Taylor and Drori constructed ITEM for reducing
the distance from the set of optimal solutions, whose exact optimality for smooth strongly convex
minimization follows from a matching lower bound [62, 18]. BnB-PEP [14] unified the design
side of this program by solving the underlying nonconvex QCQPs to certifiable global optimality,
constructing optimal methods in setups where the prior convexity-based reformulations do not
apply. Its methodology produced OptISTA, an optimal method for composite minimization [27].
Its numerical certificates also helped pave the way for the provably faster long-step gradient descent
of Grimmer [23] and the silver stepsize schedule of Altschuler and Parrilo [2, 3], a line of work
surveyed in [4]. In every one of these successes, the path from a numerically optimal solution to
a theorem that includes analytic coeﬀicients, a dual certificate, and a written proof was traversed
by hand. AutoOPT automates precisely this path while keeping the human researcher in control of
every decision boundary.

AI-assisted optimization theory. Very recently, frontier models have also begun proving research-
level results in optimization theory: an AI agent writing directly in Lean discovered an improved
last-iterate rate for anchored gradient descent ascent for minimax optimization [60], GPT 5.6 Sol
Pro closed a query-complexity gap open since 1996 in derivative-free convex optimization, with the
central lower bound subsequently formalized in Lean [29], and ChatGPT 5.5 produced the first
convergence proof for Bregman Douglas–Rachford splitting as a matrix scaling algorithm [37]. In
all three works the core workflow was that a human prompted a frontier model to solve a known
open question, the model supplied the mathematics, and correctness was secured afterward, by the
authors’ own checking or by a Lean formalization provided for that one result.
Two recent works [68, 59] combine PEP with LLM consultation for optimization research. In [68],
using ChatGPT and Codex for exploratory PEP computations, the authors discovered an optimal
proximal gradient method for minimizing the sum of a smooth and a nonsmooth convex function,
with the final Lyapunov proofs derived by the authors. Peppy [59] is an AI-assisted workflow
for tight convergence analysis of known algorithms: given a problem class, a known algorithm,
a performance measure, and an initial condition, it implements and solves the associated PEPs
through the deterministic PEPFlow package, extracts fixed-horizon proof certificates, assembles
Lyapunov partial sums, and simplifies them into closed-form analytic proofs, with symbolic checks
along the way.




                                                  4
1.3 Organization
This paper is organized as follows. In Section 2, we review conversational chatbots, agentic research
systems, coding and persistent agents, reusable agent skills, and the research practices on which
AutoOPT builds. In Section 3, we describe AutoOPT methodology consisting of numerical design,
symbolic discovery, formal verification, and human interpretation. In Section 4, we present lem-
niscate acceleration and analytic ITEM-f, respectively, together with their convergence analyses,
continuous-time interpretations, AutoOPT design histories, and Lean formalizations. In Section 5,
we discuss the applicability and limitations of AutoOPT and the broader role of domain-specific har-
nesses in AI-assisted research. Appendices A and B collect the deferred proofs, PEP formulations,
and technical details for the two case studies.

1.4 Computational setup
We open-source the portable agent skills and Lean verification projects associated with AutoOPT
at the link:
                            https://github.com/Shuvomoy/AutoOPT
Unless otherwise specified, we conducted the experiments from a laptop running macOS Tahoe
with an Apple M5 Max processor and 128 GB of memory. The agentic experiments used GPT-5.5
[51] and GPT-5.6 Sol [50] through the USD 200-per-month ChatGPT Pro tier [47]. No internal or
unreleased model was used for the agentic experiments in this paper. The Lean verification projects
use Lean 4.32.0 [16] and mathlib 4.32.0 [66].
Within Stage 1 of AutoOPT, we formulated the numerical design problems in JuMP 1.31.1 [36], a
domain-specific modeling language for mathematical optimization embedded in Julia 1.12.6 [9].
The reported BnB-PEP computations used MOSEK 11.2.2 [39] as the primary solver for the fixed-
method SDPs and KNITRO 16.0.0 [10] and Ipopt 3.14.19 [69] as the primary solvers for the local
QCQPs. Gurobi 13.0.2 [25] was used to perform spatial branch-and-bound. MOSEK and Gurobi
provide no-cost academic licenses [38, 24]. Ipopt is open source under the Eclipse Public License
2.0 [12], while KNITRO is commercial and offers academic and teaching programs [7].


2   Background on agentic research
In this section, we briefly review recent agentic research practice, with an emphasis on what each
class of tool can and cannot responsibly do in a mathematical research workflow.

From chatbots to agents. Conversational chatbots such as ChatGPT, Claude, and Gemini were
the first widely used form of LLM assistance in research. A researcher can ask for explanations,
brainstorming, proof debugging, literature orientation, or alternative formulations of a claim. This
is extremely valuable, but it has a structural limitation: a chat agent does not own a repository,
run the tests that would falsify its suggestions, or maintain a reproducible artifact trail. It can
offer advice, but it cannot execute research over a long time horizon.

Agentic research systems. Recent work on using LLMs for research has moved in a more agentic
direction, closing part of the propose-test-revise loop. Program-search systems such as FunSearch


                                                 5
and AlphaEvolve use LLMs to generate candidate programs and evaluate them automatically,
yielding new constructions and algorithmic improvements [55, 46]. Broader scientific-agent frame-
works, such as the AI Scientist, attempt larger portions of the open-ended research cycle [34], and
in mathematics, systems such as Aletheia point toward autonomous or semi-autonomous research-
level problem solving [21].

Coding agents. For individual academic research and mathematical software development, the
most practical setup beyond the conversational chatbot is the coding agent, such as Codex, Claude
Code, and OpenCode [49, 5, 54]. A coding agent can operate on an active repository: it can read
files, edit source code, run shell commands, inspect compiler or solver output, and iterate after
errors. The important shift from the conversational chatbot is that the agent can act on artifacts
the researcher will later inspect.
Persistent personal research agents extend this idea from a single coding session toward a more
persistent research workflow. OpenClaw can be viewed as a personal AI assistant that runs on the
user’s devices and replies on messaging surfaces such as WhatsApp, Telegram, Slack, Mattermost,
and Discord [53]. Hermes Agent is a self-improving agent with persistent memory, generated
workflow packages, scheduled automations, and support for similar messaging surfaces [45]. These
agents can support research progress by preserving state across repositories, files, commands, logs,
memories, scheduled tasks, and other inspectable artifacts; their ability to maintain context across
interactions and serve as standing research assistants is therefore highly valuable.

Agent skills. In the context of agentic LLMs, a skill is a reusable package of instructions and
supporting material that an agent can load for a specialized task. In the open Agent Skills format,
the minimal object is a folder containing a SKILL.md file with metadata and instructions; the folder
may also contain scripts, references, templates, and other resources [1]. OpenAI Codex and Claude
Code document skill mechanisms based on this principle [48, 6]. For an optimization workflow, the
point of a skill is to move recurring guidance out of a transient prompt and into an inspectable
artifact.

Agentic research practice. Across these tool classes, effective agentic research consistently de-
pends on persistent instructions, inspectable reports and artifacts, staged evaluation, explicit ver-
ification, and intermittent human steering [74]. Mathematical research tightens each requirement.
A claimed algorithm must have a precise statement; a computational run must record solver status,
tolerances, and enough environment information to be reproduced; a proof attempt must be labeled
theorem, conjecture, checked derivation, or failed approach; and a formal-verification claim requires
actual checker output. AutoOPT instantiates these requirements for optimization research: each
stage of the pipeline is packaged as a skill that any skill-loading agent can execute, every stage is
approved or revised by a human, and the research state lives in a versioned repository. We describe
the framework in Section 3.


3   Methodology
AutoOPT is an agentic framework for the end-to-end design, convergence analysis, and formal
verification of optimal first-order methods. The framework has four stages, illustrated in Figure 1


                                                 6
and detailed in the following subsections. Throughout this section, we describe AutoOPT at a high
level, focusing on how to use the methodology; readers interested in implementation details can
refer to the appendix and the accompanying skills.

Operating AutoOPT. AutoOPT is model- and agent-agnostic: a user can run it from any skill-
loading agent, e.g., Codex, Claude Code, or OpenCode, and can use any commercial or open-source
LLM supported by the agent. The user operates AutoOPT by conversing with the agent.
At the start, AutoOPT invokes the agent skill research-repo-manager, which creates a research
workspace in a directory of the user’s choice. The workspace serves as persistent memory for the
research project, keeping every source, claim, experiment, artifact, reproducibility note, deferred
goal, and potential next step explicit and inspectable. The workspace overcomes a key limitation
of single-session LLM workflows: as a conversation grows, the LLM’s context window becomes
crowded, compressed, or incomplete, making it harder to reliably recover earlier decisions, assump-
tions, and evidence. By storing the research state in versioned repository files rather than only
in the chat transcript, research-repo-manager lets a later session reload the current goals, findings,
artifacts, and next action directly from the workspace.

3.1 Stage 1: Numerical design of optimal first-order methods via bnb-pep-skill
The design problem. The research question AutoOPT addresses is finding the fastest gradient-
based method for a given problem class: minimizing a function f : R d → R from a known function
class F, such as smooth convex functions, smooth strongly convex functions, weakly convex func-
tions, or a nonsmooth class. Here, “fastest” means the best worst-case guarantee with respect to
a chosen performance measure E. For example, the goal may be to design an N -step algorithm
producing a final point xN such that E = f (xN )−inf f or E = k∇f (xN )k2 is guaranteed to be small,
subject to an initial condition C ≤ 0 normalizing the starting point, such as C = kx0 − x⋆ k2 − R2
for a given R > 0.
AutoOPT searches over the class of fixed-step first-order methods (FSFOMs): methods that form
each iterate from the starting point x0 ∈ R d and the first-order information observed so far via

                                          X
                                          i−1
                            xi = xi−1 −         hi,j f ′ (xj ),   i = 1, . . . , N,
                                          j=0

where f ′ (xj ) ∈ ∂f (xj ) is a subgradient of f at xj and {hi,j }0≤j<i≤N is a lower triangular array of
stepsizes; lower triangularity expresses that each update depends only on the first-order information
observed so far. The stepsizes {hi,j }0≤j<i≤N parameterize the FSFOM and are the main decision
variables we optimize over; we write MN for the class of all N -step FSFOMs. We write M =
{hi,j }0≤j<i≤N ∈ MN to denote an individual FSFOM.
Formally, the design problem becomes a minimax problem of the form

 R⋆ (MN ) ≜      min   max {E : f ∈ F , C ≤ 0, x1 , . . . , xN generated by M = {hi,j }0≤j<i≤N } . (1)
               M ∈MN   |                                     {z                                }
                                            R(M ), the worst-case performance of M




                                                       7
From function classes to finitely many inequalities. At first sight, the minimax problem above
may seem intractable as the inner maximization runs over all functions in F, an infinite-dimensional
class. The performance estimation methodology [19, 65] removes this obstacle in two steps. First,
for a fixed method M = {hi,j }0≤j<i≤N , the inner problem depends on f only through its values and
first-order information at the iterates x0 , x1 , . . . , xN and at a stationary point (minimizer for convex
setups) x⋆ , adjoined to encode stationarity (optimality for convex setups) through 0 ∈ ∂f (x⋆ );
collecting these indices in IN     ⋆ ≜ {0, 1, . . . , N, ⋆} and writing g ∈ ∂f (x ) and f ≜ f (x ), the
                                                                           i        i        i        i
trajectory data {(xi , gi , fi )}i∈IN⋆ carry everything the inner problem needs to know about f . Second,
the function classes the methodology covers are quadratically representable [13, 14]: membership in
F is described by inequalities of the form

                  c0 f (y) ≥ c1 f (x) + c2 kxk2 + c3 kyk2 + c4 kuk2 + c5 kvk2 + c6 hx, yi
                                                                                                        (2)
                             + c7 hx, ui + c8 hx, vi + c9 hy, ui + c10 hy, vi + c11 hu, vi

for all x, y ∈ R d , u ∈ ∂f (x), and v ∈ ∂f (y), where ∂f denotes the subdifferential, reducing to
∂f (x) = {∇f (x)} for the differentiable classes, and c0 , . . . , c11 are fixed coeﬀicients determined by
the class parameters; smooth convex, smooth strongly convex, and weakly convex functions are all
of this form.
Technically, replacing the constraint f ∈ F with the inequalities (2) imposed only on the finitely
many pairs in IN⋆ is, a priori, a relaxation. Establishing that this finite system is lossless requires

a separate theorem for each function class, and such characterizations are known as interpolation
conditions. We refer the reader to prior work for a detailed discussion of this issue; see, for example,
[65, 56, 57].

Gram lifting: Pa convex SDP for fixed stepsizes.
                                          Pi          It is convenient to reparameterize the FSFOM
                 i−1
as xi = x0 − j=0 αi,j gj , where αi,j ≜ k=j+1 hk,j ; this triangular map is invertible, so α is the
design variable. Collect the relevant trajectory vectors as columns of a matrix P and the sampled
function values in a row vector F , and form the Gram matrix G ≜ P ⊤ P  0. Since the iterates
are aﬀine in α, the sampled inequalities (2), the performance measure, and the initial condition are
aﬀine in (F, G), with Gram-side coeﬀicient matrices whose entries have degree at most two in α.
Writing tr for the trace, the inner worst-case problem becomes
                                                                                        
                      maximize F uE + tr GQE (α)
                    subject to                                                          
                                                                                        
                    F ui,j + tr GQi,j (α) ≤ 0, i, j ∈ I : i 6= j, ▷ dual var. λi,j ≥ 0 
                                                          ⋆
         R(M ) =                                        N                              ,      (3)
                      −G    0,   ▷ dual var. Z  0                                      
                                                                                        
                    F uC + tr GQC (α) ≤ r, ▷ dual var. ν ≥ 0                            
                      rank G ≤ d,

where the vectors uE , uC , ui,j , the symmetric matrices QE (α), QC (α), Qi,j (α), and the scalar r are
assembled mechanically from (2), E, and C; for instance, the initial condition C = kx0 − x⋆ k2 − R2
has uC = 0 and r = R2 . Under the large-scale assumption that d is at least the number of columns
of P , the constraint rank G ≤ d is vacuous. Dropping it makes (3) a convex semidefinite program
(SDP) in (F, G), free of the problem dimension d. This mechanical assembly is exactly what bnb-
pep-skill automates: it fixes the exact contents of P and F for the instance at hand, derives the


                                                      8
corresponding vectors u and matrices Q(α) symbolically, and records the resulting Gram dimension
together with the matching assumption on d. Appendix A.3 carries out this assembly explicitly for
lemniscate acceleration.

Dualization: from worst-case values to proofs. SDP duality turns the inner maximization (3)
into a minimization,
                                                                              
                           minimize νr
                          subject to                                          
                                       P                                      
                          u − νu −                                            
                          E       C           ⋆
                                                P
                                          i,j∈IN :i̸=j λ i,j u i,j = 0,        
                 R(M ) =                                                      ,       (4)
                          νQC (α) − QE (α) + i,j∈I ⋆ :i̸=j λi,j Qi,j (α) = Z, 
                                                         N                    
                          Z  0,                                              
                           ν ≥ 0, λi,j ≥ 0, i, j ∈ IN : i 6= j
                                                        ⋆

whose decision variables λ = {λi,j }i,j∈IN⋆ :i̸=j , ν, and the positive-semidefinite slack matrix Z we
call the inner-dual variables. By weak duality, R(M ) ≤ R(M ), and this inequality carries the
interpretive weight of the methodology: any feasible inner-dual point is a certificate, an explicit
nonnegative aggregation of the sampled inequalities proving that E ≤ νr for every function in
the class satisfying the initial condition, that is, a machine-checkable convergence proof. Strong
duality holds under mild conditions which implies R(M ) = R(M ) and is assumed in this paper.
Each derivation that bnb-pep-skill writes states this dual explicitly, with the sign conventions of
its multipliers fixed, and records whether the resulting bound invokes strong duality or only the
weak direction. The certificate view is what the later stages of AutoOPT use internally: Stage 2
(Section 3.2) fits analytic expressions to the numerically designed (α⋆ , λ⋆ , ν ⋆ , Z ⋆ ) and then converts
the fitted multipliers into the Lyapunov function based convergence proofs, and Stage 3 (Section 3.3)
formalizes those Lyapunov proofs in Lean.

Cholesky elimination and the BnB-PEP QCQP. Substituting the dual (4) for the inner maxi-
mization in (1) collapses the minimax into a single minimization, jointly over the stepsizes and the
inner-dual variables. In other words, the single minimization problem jointly optimizes over the
algorithm and its convergence proof.
However, this joint optimization is non-convex. The BnB-PEP methodology [14] eliminates the
semidefinite constraint Z  0 through the parameterization Z = V V ⊤ and, by introducing aux-
iliary variables to represent bilinear or quadratic terms when necessary, formulates the numerical
optimization problem as a nonconvex quadratically constrained quadratic program (QCQP)
                                                                                
                               minimize νr
                             subject to                                         
                                                                                
                             uE − νuC − P         ⋆ :i̸=j λi,j ui,j = 0,
                                                                                 
                                             i,j∈IN
                                                    P                            
                                                                                
                R⋆ (MN ) =  νQC (α) − QE (α) + i,j∈I ⋆ :i̸=j λi,j Qi,j (α) = Z, ,            (5)
                                                            N                   
                             V is lower triangular with nonnegative diagonals, 
                                                                                
                             Z = V V ⊤,                                         
                               ν ≥ 0, λi,j ≥ 0, i, j ∈ IN : i 6= j
                                                            ⋆

with decision variables {αi,j }0≤j<i≤N , λ, ν, Z, and V . Any feasible point to this QCQP corresponds
to an algorithm and its convergence proof, while an optimal point gives the best algorithm along
with its convergence proof.

                                                     9
The three-stage solution strategy. Despite its nonconvexity, (5) can be solved to certifiable global
optimality, up to prescribed tolerances, by the three-stage BnB-PEP strategy of [14]: a fixed-
method dual SDP supplies a feasible point, an interior-point solver refines it to a local optimum,
and a customized spatial branch-and-bound solver performs the global certification. The final stage
is made practical by the QCQP-specific bounds and cuts developed in that work. Accordingly, bnb-
pep-skill runs the first two stages by default and invokes the global stage only at the user’s explicit
request. The BnB-PEP methodology can be laborious to implement and debug and the manual
coding is cumbersome and error-prone and requires substantial PEP expertise. This implementation
barrier has previously limited its use.

Automation with bnb-pep-skill. The methodology described above, including several technical
details omitted from the exposition, can be tedious to formulate and implement by hand. Our
bnb-pep-skill automates this process through an executable and auditable protocol.
A run of the bnb-pep-skill opens as a structured interview that assumes no PEP expertise on the
user’s part and produces a fully specified instance: the function class with its inequalities, the
method update equations, the performance measure, the initial condition, the constants, and the
horizon N . Whenever a required item is missing or ambiguous, the skill asks a targeted question
rather than guessing, and it accepts the instance only when another researcher could write down
every constraint and identify every decision variable without making further choices.

Code generation and guardrails. Once the user approves the mathematics, bnb-pep-skill writes
code. The generated Julia/JuMP [36] program builds the primal and dual SDPs of the instance
together with the design problem (5) and numerically solves the non-convex QCQP.
This protocol makes concrete the division of labor behind the domain-specific harness of Section 1:
the LLM agent interviews the user, instantiating the derivation, and writing code, while the harness
supplies the accumulated domain expertise, from exactness theorems for interpolation conditions
to warm-start numerics, that a general-purpose model cannot be relied upon to reproduce unaided.
The same division of labor recurs in Stages 2 and 3.

The agentic workflow. In the first stage, AutoOPT invokes bnb-pep-skill and interviews the user
about the problem setup for which an optimal first-order method is sought. The interview assumes
no PEP expertise on the user’s part. From the agreed setup, the skill writes out the complete
derivation, instantiating (2)–(5) for the user’s instance, and stops for the user’s approval of the
mathematics before any code is written.
Once the user approves the derivation, the skill generates and runs Julia/JuMP code to obtain
candidate stepsizes and associated inner-dual certificates. It stores the derivation, the code, the
numerical solution, the solver status, and the logs in the research workspace. Figure 2 summarizes
the workflow; the complete derivations produced this way for our two case studies appear, lightly
edited for presentation, in Appendices A.3 and B.3.




                                                  10
                                                           bnb-pep-skill


           Problem                                            Julia                               Store
                                                                                      Run
                                   BnB-PEP                                                    derivation &
          description                                        code                     Julia
                                   derivation                                                  numerical
            by user     approve/                approve/   generation      approve/   code
                          edit                    edit                       edit               solution
        Figure 2: Stage 1 of AutoOPT. Numerical design of the optimal method via bnb-pep-skill.


3.2 Stage 2: Symbolic discovery of analytic descriptions and convergence proofs via
    LLMs
Numerical to symbolic discovery. Once the numerically optimal stepsizes and the BnB-PEP
mathematical derivation are available from Stage 1, AutoOPT invokes the skill frontier-llm-consult
to discover analytic descriptions of the numerically designed methods and candidate convergence
proofs. Figure 3 summarizes the stage. The skill frontier-llm-consult supports two routes. The
external consultation route, chatgpt-pro-session, runs a persistent ChatGPT Pro session in a web
browser and is the default for ordinary Stage 2 work; the same route also covers bounded one-
shot reviews, each conducted as a single approved turn in a fresh session. For the consultation
route, the skill assembles a deliberately small context bundle containing a self-contained prompt,
the numerical findings from the previous stage, and the relevant mathematical background and
derivations. The skill then presents the bundle for user approval; the user may approve it as is or
edit it first, and only after approval is the bundle shared with the frontier model. The persistent
session enables symbolic discovery from numerical findings through several rounds of pattern search,
algebraic refinement, and follow-up questions from the user. The native route, solve-with-highest-
reasoning, runs only on explicit user invocation and is not an external consultation: the host agent
itself conducts a long native campaign on the problem, using the strongest currently available
Codex GPT model at its highest supported reasoning setting, with direct repository exploration,
local tools, and adversarial verification, over at least eight wall-clock hours. The user approves the
repository scope, no problem material is sent to any external model, and the full evidence trail is
archived in the research workspace. For the consultation route, the user can edit the underlying
SKILL.md file to substitute a different frontier model.
Whichever route is selected, discovery proceeds in three substeps. The frontier model first identifies
the analytic form of the numerically designed method, that is, an analytic parametrization of the
numerically optimal FSFOM stepsizes from Stage 1, together with an analytic feasible point of the
inner dual (4). By the certificate view of Section 3.1, feasibility of this point already proves the
worst-case bound, so the first substep yields a candidate convergence proof by dual feasibility. In the
second substep, the model recasts the method from this raw stepsize parametrization into a simple,
memory-eﬀicient algorithmic form, recursive or momentum-based, which is the form in which this
paper states each method. In the third substep, the frontier model derives a second argument from
the same certificate: reading coeﬀicients off the certificate’s multipliers, it constructs a Lyapunov
sequence of potentials that is nonincreasing along the iterates and whose endpoint values give the
claimed bound, with the potentials stated directly on the recast form of the second substep. Both
arguments are candidate proofs of the same theorem. This paper presents the Lyapunov proofs,
the form that a classical optimization audience reads most naturally; the dual-feasibility certificates
remain intermediate artifacts of the research workspace, and it is their multipliers that the printed
proofs are built from.


                                                           11
 Attached are the Stage 1 outputs of AutoOPT for the design of an N -step FSFOM that minimizes
 the worst-case squared gradient norm ∥∇f (xN )∥2 over L-smooth convex functions with ∥x0 − x⋆ ∥ ≤
 R: the BnB-PEP derivation (derivation.md), the Julia/JuMP code that solved it, and a CSV
 sweep (stepsize_certificate_sweep.csv) of the numerically optimal stepsizes h and inner-dual
 certificates (λ, ν, Z) for the horizons N = 1,...,25 with first 5 being globally optimal via
 spatial branch-and-bound and the last 20 being locally optimal.
 From these data, propose a candidate analytic parametrization of the stepsizes h valid for
 every horizon N , together with a candidate analytic feasible point (λ, ν, Z) of the inner dual
 SDP stated in the derivation. Feasibility of that point already certifies the worst-case
 bound, so also state the candidate rate it implies in closed form. Every proposed formula
 is a candidate, not a proof; report which entries of the sweep you checked it against and to
 what precision. Please ask me clarifying questions if anything is not clear to you.

 Your parametrization stores the full lower-triangular stepsize array h. Recast the method
 into an equivalent memory-efficient form, recursive or momentum-based, that reproduces the
 same iterates x0 , . . . , xN while carrying only a constant number of vectors, and give closed-form
 expressions for the coefficients of the recast update. Check the recast against the h-form on
 the sweep horizons and report the agreement.

 Reading the coefficients off the multipliers (λ, ν) of your candidate certificate, construct a
 candidate Lyapunov proof of the same bound: a sequence of potentials V0 , . . . , VN , stated directly
 on the recast form of your previous reply, that is nonincreasing along the iterates and whose
 endpoint values yield the claimed bound. Express each one-step decrement as a nonnegative
 combination of the interpolation inequalities from the derivation, and flag any step you cannot
 close.

    Figure 4: An illustrative Stage-2 prompt sequence for the lemniscate case study: one initial prompt
    followed by two follow-up prompts corresponding to the three substeps of Section 3.2.


Figure 4 makes the workflow concrete for the lemniscate acceleration case study of Section 4.1. It
shows an illustrative Stage-2 prompt sequence, consultation-shaped because both published runs
used the external chatgpt-pro-session route: one initial consultation prompt requesting the first
substep, followed by two short turns in the same session requesting the remaining two. Only the
author-written task text is printed; the consultation package that wraps it and the approve-before-
send gate are those described above.
                                                frontier-llm-consult
                                                                               Candidate
                                                      Selected
                   Context                                                    formula and
                                                   frontier-model
                   bundle                                                     convergence
                                 approve/edit           route
                                                                                analysis
    Figure 3: Stage 2 of AutoOPT. Symbolic discovery of analytic descriptions of the numerically
    designed methods and their candidate convergence proofs via frontier-llm-consult.



Preparation for machine verification. At the end of this stage, AutoOPT saves the outputs from
the frontier LLMs in the research workspace so that the reasoning trace is inspectable by the user.
AutoOPT marks the frontier LLM output as a “candidate” analytical solution: it may give the
researcher something concrete to test, simplify, formalize, or prove, but it still needs independent
validation, which is supplied, for the results advanced to the paper, by the Lean verification stage
described next.

                                                        12
3.3 Stage 3: Formal verification of candidate theorems via lean-verify
                                             lean-verify

                                                                                                          final human
             Candidate                                     Check 1:                  Check 2:             confirmation
                                Formalized
            theorems &                                   Lean verifies             independent
                                 in Lean
               proofs                                     every step              re-examination                   formally verified
            from Stage 2      every definition &    no unfinished, incomplete, exactly what was proved,
                           proof step made explicit     or incorrect steps     under which assumptions
    Figure 5: Formal verification via lean-verify: candidate theorems and proofs from Stage 2 are
    formalized in Lean, checked by Lean itself, and re-examined by an independent verifier; the result
    is recorded as formally verified only after the human authors confirm that the formal theorems
    faithfully express the paper’s claims.


From candidate to formalization. Stage 3 of AutoOPT is the formal verification stage. Here,
AutoOPT invokes the skill lean-verify, which uses machine verification in the open-source proof
assistant Lean to determine whether the chain of logic in the candidate theorems and proposed
proofs discovered in Stage 2 is correct. During machine verification, Lean records every definition,
theorem statement, and proof precisely, examines the logic of every step of a proof, and accepts a
proof only when each step is correct and explicit.
The lean-verify skill first formalizes in Lean the candidate theorems together with the proofs selected
for presentation in the paper, which for our case studies are the Lyapunov proofs derived in Stage 2,
and reconstructs the proof steps there in detail, so that any gap, hidden assumption, or algebraic slip
in the candidate argument is exposed rather than granted on trust. A proof is recorded as formally
verified only after two successive independent checks followed by a final human confirmation. The
first check is Lean’s own internal verification, which confirms that the accepted proof contains no
unfinished, incomplete, or incorrect steps. The second independent check is through a separate
verifier called the comparator that reexamines the finished formalization and confirms exactly
which statements have been proved and which assumptions the proofs were permitted to use, so
that what has been machine verified is pinned down without ambiguity. Once the two checks are
complete, the human authors confirm that the formal theorem statements in Lean faithfully express
the corresponding theorem statements in the paper, and only then record the result as formally
verified. Figure 5 summarizes the workflow of the skill lean-verify.
An illustrative Stage-3 prompt, the file structure of each resulting Lean project, and per-project
summary statistics are presented with the case studies, in Sections 4.1.5 and 4.2.4.

3.4 Stage 4: Human interpretation and write-up
The goal of this paper is to provide a new methodology for automating what used to be a highly
time-consuming and technical component of optimization research. As researchers, we value accel-
erating progress and solving harder and more interesting problems.
However, we hope that this pursuit of automation does not cause us to lose sight of the fact that
mathematical research is a human endeavor and that the value of research is realized when it is
conveyed and used by other researchers. Therefore, the final part of the pipeline is for the human



                                                         13
authors to interpret the results, frame why they are of interest to the community, and present
insights that go beyond the mere statement of the result.
In what follows, we briefly offer our personal views on the best practices for humans using such
methodologies.

Publication restraint. In this era of AI accelerating research, proofs of novel results are no longer
scarce. We therefore believe authors should now ask whether a novel and correct result is suﬀiciently
interesting to the research community, and exercise judgment and parsimony by forgoing publication
of results that do not meet this new higher bar.

Distilling generalizable insights. While optimization is an applied field, worst-case complexity
guarantees are theoretical analyses whose value lies in expanding our collective understanding of
algorithm design and eventually informing the optimization practice. Merely presenting a new
algorithm with a verifiable but opaque analysis delivers little of this value, especially when AI
assistance means the human authors themselves lack strong intuition about the result.
It is therefore essential that authors extract compact, generalizable insights from the formal dis-
covery and present them in a form that is maximally useful to human researchers. For example, a
machine-discovered optimization algorithm may first arrive in a dense stepsize-matrix representa-
tion. In our pipeline, Stage 2 already recasts such a method into an equivalent memory-eﬀicient,
recursive, or momentum-based formulation (Section 3.2); what remains a matter of human judg-
ment is which of the available forms serves readers best. The authors should make that choice
deliberately, potentially with further AI assistance, and present the formulation that a human
reader can most readily implement, interpret, and analyze.

A calibrated standard of evidence. In the final presentation, the authors should clearly assign
each claim an evidentiary status (human-verified, formally verified, LLM-verified, numerical evi-
dence, or conjecture), so that no intermediate object or computational observation is presented as
stronger evidence than it actually provides.
We also emphasize that human authors must exercise their own due diligence in verification. Even
a Lean formalization may fail to establish the intended result: the formal theorem statement may
encode a claim weaker than the paper’s natural-language statement, or the proof may remain
incomplete because it contains sorry placeholders. Even with thorough harnesses, AI systems still
make mistakes, and the human authors are ultimately accountable for the work they publish.


4   New algorithms discovered, analyzed, and verified using AutoOPT
In this section, we present two new first-order algorithms found using AutoOPT: lemniscate accel-
eration and analytic ITEM-f. We present these algorithms both as algorithmic advances in their
own right and as demonstrations of the strength of AutoOPT.
Note that the order of discovery via AutoOPT differs from the order of presentation of those results
in this paper. For each method, AutoOPT first solved the BnB-PEP design problem numerically,
next identified the method’s analytic form together with an analytic dual certificate of its worst-case
guarantee, then recast the method from the raw stepsize parametrization of the design problem

                                                  14
into the memory-eﬀicient form in which this paper states it, and finally converted the certificate’s
multipliers into a Lyapunov convergence proof for the presented form. The paper presents each
method in the order a reader expects: algorithm, convergence theorem, and proof. The printed
proofs are the Lyapunov proofs from Stage 2, with Lean formalization discussed in Sections 4.1.5
and 4.2.4; the subsections titled “AutoOPT design” recount how each method was found, and
Appendices A.3 and B.3 reproduce the Stage-1 PEP formulations.
We use the following notation and notions in the rest of the paper. Write R d for the underlying
Euclidean space and we write h·, ·i and k · k to denote the standard inner product and norm on
R d . Write R m×n for the set of m × n matrices, S n for the set of n × n symmetric matrices, and
S+
 n for the set of n × n positive-semidefinite matrices. We use the standard notation e ∈ R d for
                                                                                        i
the unit vector having a single 1 as its i-th component. Write (· ·) : R d × R d → R d×d to denote
the symmetric outer product, that is x y = (xy ⊺ + yx⊺ ) /2 for every x, y ∈ R d , and δi,j denotes
the Kronecker delta, equal to 1 if i = j and 0 otherwise. We write tr for the trace of a square
matrix. For 0 ≤ µ < L < ∞, we write Fµ,L for the class of L-smooth µ-strongly convex functions
f : R d → R, that is, differentiable functions for which ∇f is L-Lipschitz and f − (µ/2) k·k2 is
convex; the case µ = 0 gives the class F0,L of L-smooth convex functions. Every function f ∈ F0,L
satisfies
                                                          1
                       f (x) − f (y) − h∇f (y), x − yi −    k∇f (x) − ∇f (y)k2 ≥ 0              (6)
                                                         2L
for all x, y ∈ R d [15, Theorem A.1].
Throughout, x⋆ denotes a minimizer of the function f under consideration, f⋆ ≜ f (x⋆ ), and the
subscript ⋆ refers to this optimal point. For a method that runs for N iterations and produces the
iterates x0 , x1 , . . . , xN , we collect the iteration indices together with the optimal point in the index
     ⋆ ≜ {0, 1, . . . , N, ⋆}.
set IN

4.1 Lemniscate acceleration for eﬀicient gradient-norm minimization
Consider the unconstrained minimization problem
                                             minimize f (x),                                             (7)
                                                x∈R d

where f : R d → R is an L-smooth convex function. We seek an algorithm that uses N gradient
evaluations to produce an output xN with a small worst-case guarantee on k∇f (xN )k.
Throughout this section, we use the single-gradient-step notation
                                               1
                                    z+ ≜ z −     ∇f (z),      ∀ z ∈ Rd.
                                               L

Algorithm statement
The lemniscate accelerated gradient method (LemniAcc) is
                                                              !
                                            1 + ρ2k+1 1 + ρ2k 1
                           zk+1 = zk − ΩN            −             ∇f (xk )
                                              2ρk+1      2ρk     L
                                                              !                                (LemniAcc)
                                         1 + ρ 2     1 + ρ2
                                               k+1        k+2
                           xk+1 = x+
                                   k +             −            zk+1
                                         1 − ρ2k+1 1 − ρ2k+2

                                                        15
                N        ΩN        ρ1          ρ2           ρ3             ρ4           ρ5         ρ6       ρ7
                1    2.4142      0.4142
                2    4.1628      0.6126       0.2402
                3    6.2479      0.7241       0.4142       0.1601
                4    8.6645      0.7931       0.5380       0.3004     0.1154
                5   11.4075      0.8388       0.6277       0.4142     0.2287        0.0877
                6   14.4730      0.8707       0.6942       0.5052     0.3287        0.1805       0.0691
                7   17.8578      0.8939       0.7446       0.5780     0.4142        0.2675       0.1464   0.0560
        Table 1: Values of ΩN and ρ1 , . . . , ρN for N = 1, . . . , 7, computed by the bisection method.


for k = 0, 1, 2, . . . , N − 1, where N ≥ 1 is an integer-valued prespecified iteration budget, x0 ∈ R d
is the starting point, z0 = 0, and ΩN > 0 and 1 = ρ0 > ρ1 > · · · > ρN > ρN +1 = 0 are constants
that we define in Lemma 1.
We can also express (LemniAcc) equivalently in the so-called momentum form
                           (init) +
                x1 = x+
                      0 +α       (x0 − x0 ),
                                  (mom)                          (corr)
                                                                                                                         (8)
                xk+1 = x+                   k − xk−1 ) + αk
                                          (x+                               k − xk ),        k = 1, . . . , N − 1,
                                                 +
                        k + αk                                            (x+

where
                                                                          !
                        1 + ρ21 1 + ρ20        1 + ρ2N   1 + ρ2N −1
  α(init) = ΩN                 −                       −                        ,
                          2ρ1     2ρ0            2ρN       2ρN −1
          1+ρ2N −k   1+ρ2N −k−1
  (mom)    2ρ      −  2ρN −k−1
 αk     = 1+ρN2−k      1+ρ2N −k
                                ,
           2ρN −k+1 − 2ρN −k
              N −k+1

                                                                                                                       
                                               !                                         !
                1 + ρ2N −k   1 + ρ2N −k−1                   1 + ρ2k+1 1 + ρ2k                                           
   (corr)                                                                                                  1            
  αk        =              −                         ΩN              −                      −                           .
                  2ρN −k       2ρN −k−1                       2ρk+1     2ρk                     1 + ρ2N −k+1 1 + ρ2N −k 
                                                                                                             −
                                                                                                   2ρN −k+1     2ρN −k

The two forms are equivalent in the sense that they produce the same iterates x0 , . . . , xN ; a proof
is given in Appendix A.2.

Construction of the coeﬀicients
To fully define (LemniAcc), it remains to define the coeﬀicients ρ0 , ρ1 , . . . , ρN , ρN +1 and ΩN .
Lemma 1. Let N be a nonnegative integer. There exists a unique ΩN > 0 for which there is a
strictly decreasing nonnegative sequence 1 = ρ0 > ρ1 > . . . > ρN +1 = 0 satisfying the recurrence
equation                                                
                        ΩN (ρk − ρk+1 )2 = ρk 1 − ρk+1 2 , k = 0, . . . , N.                   (9)
Moreover, for this value of ΩN , the sequence ρ0 , ρ1 , . . . , ρN +1 is uniquely determined.



                                                              16
We can calculate the numerical values of {ρk }N
                                              k=0 and ΩN using bisection based on 1 ≤ ΩN ≤
                                                +1

(N + 1)2 . Appendix A.1 gives the exact shooting decision rule, its termination case, and its
correctness proof. Table 1 reports the values of ΩN and of the nontrivial entries ρ1 , . . . , ρN for
N = 1, . . . , 7.
We note that the sequence {ρk }N  k=0 has a symmetry: the map T (ρ) ≜ (1 − ρ)/(1 + ρ), which
                                    +1

satisfies T ◦ T = id, relates mirrored entries through ρN +1−k = T (ρk ) for 0 ≤ k ≤ N + 1. This
follows from the uniqueness in Lemma 1 together with the fact that (ρk , ρk+1 ) = (a, b) satisfies
the recurrence (9) if and only if (T (b), T (a)) does. In particular, for odd N , the middle index
k = (N + 1)/2 is its own mirror image, so ρ(N +1)/2 must be the point such that T (ρ) = ρ, namely
            √
ρ(N +1)/2 = 2 − 1 ≈ 0.4142.

Convergence theorem
Theorem 1. Let N ≥ 1 be an integer, and let f : R d → R be an L-smooth convex function with a
minimizer x⋆ . Then, the final iterate xN of (LemniAcc) satisfies

                                          L2 kx0 − x⋆ k2   ϖ4 L2 kx0 − x⋆ k2
                          k∇f (xN )k2 ≤                  ≤                   .
                                               Ω2N             (N + 1)4

               R1 √
Here, ϖ = 2 0 1/ 1 − x4 dx is the lemniscate constant, and the latter relaxation comes from
(N + 1)2 /ϖ2 < ΩN (Corollary 2 in Appendix A.1). We present a convergence proof soon in
Section 4.1.1.
(LemniAcc) is not the first method to attain an O(L2 kx0 − x⋆ k2 /N 4 ) rate on the squared gradient
norm k∇f (xN )k2 of L-smooth convex functions. Nesterov et al. [44, Remark 2.1] observed that
running Nesterov’s accelerated gradient method (AGM) [43] (or Kim–Fessler’s optimized gradient
method (OGM) [30]) for the first half of the iterations and OGM-G [31] for the second half achieves
this rate, which matches the Ω(L2 kx0 − x⋆ k2 /N 4 ) lower bound of [40, 41] and is therefore optimal
up to a constant factor.
Lemniscate acceleration improves upon this two-phase scheme in two ways. First, it attains the
optimal rate as a single method, with one coeﬀicient sequence and no switch between two algorithms.
Second, it improves the constant of the guarantee. For even N , chaining the standard guarantee of
OGM with that of OGM-G yields

                                                   64 L2 kx0 − x⋆ k2
                                   k∇f (xN )k2 ≤                     .
                                                       (N + 2)4

In comparison, Theorem 1 attains the constant ϖ4 ≈ 47.27, improving the leading asymptotic
constant by a factor of approximately 1.35.

4.1.1 Convergence proof
In this section, we prove Theorem 1. Throughout, f : R d → R is an L-smooth convex function
with a minimizer x⋆ , and xk and zk denote the iterates of (LemniAcc); in particular z0 = 0. The
argument has three steps. We first define the interpolation gaps and, from the multipliers of the
analytic dual certificate found in Stage 2 of the pipeline, a Lyapunov sequence V0 , V1 , . . . , VN along

                                                   17
the iterates. We then evaluate the two endpoints: V0 is at most (L/(2ΩN )) kx0 − x⋆ k2 , and the
terminal value VN dominates (ΩN /(2L)) k∇f (xN )k2 (Lemma 2). Finally, Lemma 3 shows that the
sequence is nonincreasing along the iterates, and chaining the three facts proves Theorem 1; the
same machinery yields a function-value guarantee (Corollary 1).
Write gi ≜ ∇f (xi ) and g⋆ = 0, so that x+
                                         ⋆ = x⋆ , and denote the interpolation gap by

                                                                1
                Di,j ≜ f (xi ) − f (xj ) − hgj , xi − xj i −      kgi − gj k2 ≥ 0,      i, j ∈ IN
                                                                                                ⋆
                                                                                                  ,
                                                               2L
which is nonnegative by (6). The three-point identity

                                    Di,⋆ − x+
                                            i − x⋆ , gj = Di,j − D⋆,j                                      (10)

follows from direct calculation. For notational simplicity, we also set D−1,0 ≜ 0, D−1,⋆ ≜ 0, and
x+−1 ≜ x0 . Evaluating the recurrence (9) at k = N , where ρN +1 = 0, and at k = 0, where ρ0 = 1,
gives the two boundary identities ρN = 1/ΩN and ΩN = (1 + ρ1 )/(1 − ρ1 ) > 1, which we use
repeatedly below.
For 0 ≤ k ≤ N , define the Lyapunov sequence
                                                                             2
      1 − ρ2k          (1 − ρk )2         L            1 + ρ2k+1                      L                2
 Vk ≜         Dk−1,⋆ −            DN,⋆ +     xk − x⋆ +           zk              −        N − x ⋆ + zk
                                                                                         x+              . (11)
        2ρk               2ρk            2ΩN           1 − ρ2k+1                     2ΩN

At k = 0, since D−1,⋆ = 0, ρ0 = 1, and z0 = 0, we get

                           L                 L          2    L
                   V0 =       kx0 − x⋆ k2 −      N − x⋆
                                                x+        ≤     kx0 − x⋆ k2 .
                          2ΩN               2ΩN             2ΩN

Next, we evaluate the terminal value VN .
Lemma 2 (Terminal decomposition). The terminal value of the Lyapunov sequence (11) satisfies

                ΩN                       1       Ω2 − 1           ΩN
         VN =      k∇f (xN )k2 + DN,⋆ +    D⋆,N + N     DN −1,N ≥    k∇f (xN )k2 .
                2L                      ΩN        2ΩN             2L

Proof of Lemma 2. Solving the x-update at k = N − 1, whose coeﬀicient evaluates to (1 + ρ2N )/(1 −
ρ2N ) − (1 + ρ2N +1 )/(1 − ρ2N +1 ) = 2/(Ω2N − 1), for zN and adding xN − x⋆ gives

                                           Ω2N − 1 +             Ω2 + 1
                    x N − x ⋆ + zN = −            (xN −1 − x⋆ ) + N     (xN − x⋆ ).                        (12)
                                              2                     2




                                                      18
Substituting ρN = 1/ΩN , ρN +1 = 0 into the Lyapunov sequence at k = N and expanding,

          Ω2N − 1           (ΩN − 1)2                 L                         L                 2
    VN =          DN −1,⋆ −              DN,⋆ +           kxN − x⋆ + zN k2 −         N − x ⋆ + zN
                                                                                    x+
           2ΩN                 2ΩN                   2ΩN                       2ΩN
          Ω −1
           2
                            (ΩN − 1)   2              1                           1
        = N       DN −1,⋆ −              DN,⋆ +          hxN − x⋆ + zN , gN i −      kgN k2
           2ΩN                 2ΩN                   ΩN                         2LΩN
          Ω2 − 1                                     (ΩN − 1)2
        = N        DN −1,⋆ − x+ N −1 −   x ⋆ , g N    −            DN,⋆
           2ΩN                                             2ΩN
             Ω2 + 1                         1
          + N        hxN − x⋆ , gN i −             kgN k2
              2ΩN                       2LΩN
          Ω2 − 1                         (ΩN − 1)2
        = N       (DN −1,N − D⋆,N ) −                   DN,⋆
           2ΩN                                 2ΩN
             Ω2 + 1 +                    ΩN
          + N         xN − x⋆ , g N +           kgN k2
              2ΩN                        2L
          ΩN                     1              Ω2 − 1
        =     kgN k2 + DN,⋆ +       D⋆,N + N             DN −1,N ,
          2L                    ΩN                2ΩN
where the second equality expands the difference of the two squared norms, the third substitutes
(12) and groups the terms by their coeﬀicients, the fourth applies (10) at (i, j) = (N − 1, N )
and substitutes xN = x+    N + (1/L) gN , and the last applies (10) at (i, j) = (N, N ) in the form
 x+
  N  − x ⋆ , g N = D N,⋆ + D⋆,N using DN,N = 0, and collects terms. The three interpolation gaps
are nonnegative and their multipliers are positive by ΩN = (1 + ρ1 )/(1 − ρ1 ) > 1, which gives the
second claim.
Lemma 3 (Monotonicity). The Lyapunov sequence (11), evaluated on the iterates of (LemniAcc),
satisfies for 0 ≤ k ≤ N − 1
                                                                             !
                       1 − ρ2k                             1 + ρ2k+1 1 + ρ2k
           Vk − Vk+1 =         Dk−1,k + (ρk − ρk+1 )D⋆,k +          −          DN,k ≥ 0. (13)
                         2ρk                                 2ρk+1     2ρk

Consequently, V0 ≥ V1 ≥ · · · ≥ VN .

Proof. We calculate the difference Vk − Vk+1 and group the resulting terms by the three-point
identity (10); we first prepare the supporting identities.
We use the following two scalar identities. Rearranging the recurrence (9) gives for 0 ≤ k ≤ N − 1,
                                       !                                          !
                    1 + ρ2k+1 1 + ρ2k 1 + ρ2k+1                1 − ρ2k+1 1 − ρ2k
               ΩN             −                      + 1 = ΩN            −           ,
                      2ρk+1       2ρk     1 − ρ2k+1             2ρk+1        2ρk
                  "                      !2                         !2 #                       (14)
               ΩN     1 − ρ2k+1 1 − ρ2k           1 + ρ2k+1 1 + ρ2k        1 − ρ2k+1
                                −            −             −             =           .
                2       2ρk+1       2ρk             2ρk+1     2ρk            2ρk+1




                                                  19
The update equations of (LemniAcc) give the two one-step relations
                                                                                               !
                  1 + ρ2k+2                     1 + ρ2k+1      ΩN          1 − ρ2k+1 1 − ρ2k
      xk+1 − x⋆ +           z k+1 = x k − x ⋆ +           zk −                      −              gk ,
                  1 − ρk+2
                        2                       1 − ρk+1
                                                     2          L            2ρk+1     2ρk
                                                                                    !                     (15)
                                                 ΩN               1 + ρ2k+1 1 + ρ2k
                  N − x⋆ + zk+1 = xN − x⋆ + zk −
                 x+                                                         −
                                   +
                                                                                      gk ,
                                                  L                 2ρk+1       2ρk

both for 0 ≤ k ≤ N − 1. For the first relation, the x-update gives

                                  1 + ρ2k+2                     1       1 + ρ2k+1
                    xk+1 − x⋆ +             z k+1 = x k − x ⋆ −   g k +           zk+1 ,
                                  1 − ρ2k+2                     L       1 − ρ2k+1

and substituting the z-update for zk+1 on the right-hand side and evaluating the resulting coeﬀicient
of gk by the first line of (14) proves it. The second relation of (15) follows by adding x+N − x⋆ to
both sides of the z-update.
We also state a useful vector identity: for 0 ≤ k ≤ N − 1,
                        !                           !                      !
    1 − ρ2k+1 1 − ρ2k                   1 + ρ2k+1        1 + ρ2k+1 1 + ρ2k                  
              −             xk − x⋆ +             zk −            −          x+N − x ⋆ + zk
      2ρk+1        2ρk                  1 − ρk+1
                                             2             2ρk+1     2ρk
                                                                         !                                (16)
          1 − ρ2k +             1 − ρ2k+1              1 + ρ2k+1 1 + ρ2k
     =−          (xk−1 − x⋆ ) +           (xk − x⋆ ) −           −           N − x⋆ ).
                                                                           (x+
           2ρk                    2ρk+1                  2ρk+1      2ρk
                                                                              
At k = 0, both sides equal (1 − ρ21 )/(2ρ1 ) (x0 − x⋆ ) − (1 + ρ21 )/(2ρ1 ) − 1 (x+  N − x⋆ ), by z0 = 0,
(1 − ρ0 )/(2ρ0 ) = 0, and x−1 = x0 . For 1 ≤ k ≤ N − 1, distribute the two products on the left-hand
      2                    +

side: the coeﬀicient of zk collects to
                           !                                 !                                    !
       1 − ρ2k+1 1 − ρ2k 1 + ρ2k+1         1 + ρ2k+1 1 + ρ2k       1 − ρ2k 1 + ρ2k     1 + ρ2k+1
                  −                    −            −          =                     −              ,
         2ρk+1        2ρk    1 − ρ2k+1       2ρk+1       2ρk         2ρk     1 − ρ2k   1 − ρ2k+1

and the x-update at index k − 1 gives
                                                       !
                       1 − ρ2k   1 + ρ2k   1 + ρ2k+1              1 − ρ2k           
                                         −                 zk =           xk − x+     .
                         2ρk     1 − ρ2k   1 − ρ2k+1                2ρk         k−1



                                      k−1 = (xk − x⋆ ) − (xk−1 − x⋆ ) verifies (16).
Substituting this and splitting xk − x+                    +




                                                    20
Fix 0 ≤ k ≤ N − 1. Expanding the difference Vk − Vk+1 using the one-step relations (15),
                                                                         !
            1 − ρ2k           1 − ρ2k+1          1 + ρ2k+1 1 + ρ2k
Vk − Vk+1 =         Dk−1,⋆ −            Dk,⋆ +                −             DN,⋆
              2ρk               2ρk+1              2ρk+1         2ρk
                                      ! *                                  +
                 1 − ρ2k+1 1 − ρ2k                     1 + ρ2k+1
             +             −            · xk − x⋆ +               zk , g k
                   2ρk+1        2ρk                    1 − ρ2k+1
                                      !
                 1 + ρ2k+1 1 + ρ2k
             −             −            · x+N − x ⋆ + zk , g k
                   2ρk+1        2ρk
                    "                       !2                              !2 #
               ΩN      1 − ρ2k+1 1 − ρ2k            1 + ρ2k+1 1 + ρ2k
             −                    −            −                −                kgk k2
               2L        2ρk+1        2ρk             2ρk+1         2ρk
               1 − ρ2k                             
           =            Dk−1,⋆ − x+ k−1 − x⋆ , g k
                 2ρk
                                                              
                  1 − ρ2k+1                           1      2
               −              Dk,⋆ − hxk − x⋆ , gk i + kgk k
                    2ρk+1                             L
                                        !
                          2
                    1 + ρk+1 1 + ρ2k                               
               +              −           DN,⋆ − x+   N − x⋆ , g k
                      2ρk+1       2ρk
                                                                                         !
             1 − ρ2k                    1 − ρ2k+1                    1 + ρ2k+1 1 + ρ2k
           =         (Dk−1,k − D⋆,k ) −           (Dk,k − D⋆,k ) +             −             (DN,k − D⋆,k )
               2ρk                        2ρk+1                        2ρk+1     2ρk
                                                                        !
               1 − ρ2k                                1 + ρ2k+1 1 + ρ2k
           =           Dk−1,k + (ρk − ρk+1 )D⋆,k +             −          DN,k ,
                 2ρk                                    2ρk+1     2ρk

where the second equality substitutes the vector identity (16) and the second line of (14), the third
applies (10) at j = k to each of the three groups, where at k = 0 the first group vanishes since its
factor (1 − ρ20 )/(2ρ0 ) is zero, and the fourth uses Dk,k = 0. This proves the equality in (13).
Finally, the right-hand side of (13) is nonnegative: the interpolation gaps are nonnegative, and the
three multipliers are nonnegative, since Lemma 1 gives 1 = ρ0 > ρ1 > · · · > ρN +1 = 0 and since the
map ρ 7→ (1+ρ2 )/(2ρ) is strictly decreasing for 0 < ρ ≤ 1, so that (1+ρ2k+1 )/(2ρk+1 ) > (1+ρ2k )/(2ρk )
for 0 ≤ k ≤ N − 1.

Combining Lemma 2 and Lemma 3, the proof of Theorem 1 is now immediate.

Proof of Theorem 1. Combining Lemma 2, the monotonicity of Lemma 3, and the evaluation of V0
gives
               ΩN                                                L
                   k∇f (xN )k2 ≤ VN ≤ VN −1 ≤ · · · ≤ V1 ≤ V0 ≤     kx0 − x⋆ k2 ,
               2L                                               2ΩN
and multiplying through by 2L/ΩN yields the first inequality; the second inequality then follows
from the lower bound ΩN > (N + 1)2 /ϖ2 of Corollary 2.

The Lyapunov sequence also yields a guarantee on the function value of the final iterate.



                                                     21
Corollary 1 (Function-value bound). Under the assumptions of Theorem 1, the final iterate xN
of (LemniAcc) satisfies

                                               L                ϖ2 L kx0 − x⋆ k2
                        f (xN ) − f (x⋆ ) ≤       kx0 − x⋆ k2 ≤                  .
                                              2ΩN                 2(N + 1)2
                                                                          
Proof. Dropping the two nonnegative terms (1/ΩN )D⋆,N and (Ω2N − 1)/(2ΩN ) DN −1,N in Lemma 2
and expanding DN,⋆ ,
                          ΩN
                    VN ≥      k∇f (xN )k2 + DN,⋆
                           2L
                                              ΩN − 1
                        = f (xN ) − f (x⋆ ) +        k∇f (xN )k2 ≥ f (xN ) − f (x⋆ ),
                                               2L
where the last inequality uses ΩN = (1 + ρ1 )/(1 − ρ1 ) > 1. Combining with VN ≤ V0 ≤
(L/(2ΩN )) kx0 − x⋆ k2 proves the first inequality; the second follows from (N + 1)2 /ϖ2 < ΩN
(Corollary 2), as in the proof of Theorem 1.

4.1.2 AutoOPT design: Optimal method for reducing the gradient magnitude from an initial-
      distance bound
The method (LemniAcc) was designed by AutoOPT as the optimal fixed-step first-order method
such that for all L-smooth convex functions f with minimizer x⋆ , the guarantee

                                      k∇f (xN )k2 ≤ CN kx0 − x⋆ k2

is optimal, i.e., CN is minimized. Specifically, among all N -step fixed-step first-order methods of
the form
                                      1X
                                        i−1
                          xi = xi−1 −        hi,j ∇f (xj ),  i = 1, . . . , N,
                                      L
                                              j=0

AutoOPT jointly searches over the coeﬀicients {hi,j }0≤j<i≤N and a convergence certificate to mini-
mize CN . In other words, AutoOPT jointly optimizes over the algorithm and its convergence proof
to find the algorithm with the optimal (smallest) convergence guarantee.
In Stage 1 of the pipeline, the skill bnb-pep-skill wrote out the BnB-PEP formulation of this design
problem. At a high level, performance estimation programming replaces the maximization over
the infinite-dimensional function class F0,L by a finite-dimensional semidefinite program involving
only the function values, gradients, and pairwise inner products observed along the trajectory;
dualizing this inner semidefinite program and jointly optimizing its dual variables and the method
coeﬀicients produces a nonconvex quadratically constrained quadratic program. Upon our approval
of the formulation, reproduced with light editing in Appendix A.3, the skill solved this program for
the horizons N = 1, 2, 3, . . . , 25, running spatial branch-and-bound at our request to certify global
optimality for N = 1, . . . , 5 and local optimality for N = 6, . . . , 25, and returned the corresponding
candidate stepsizes together with the candidate dual certificates.
These numerical solutions, together with the Stage-1 derivation, became the context for Stage 2,
in which the skill frontier-llm-consult placed them before a frontier LLM. The consultation first
identified an analytic description valid for arbitrary N ∈ N, the parametrization in terms of ΩN

                                                     22
and the sequence ρ0 , . . . , ρN +1 , together with an analytic feasible point of the dual certifying the
guarantee. At this point the method was still written as the dense stepsize array {hi,j }, its entries
now in closed form; the consultation next recast it into the memory-eﬀicient two-sequence form
(LemniAcc) in which Section 4.1 states the method. Continuing the same conversation, Stage 2
then converted the multipliers of this certificate into the Lyapunov proof of Theorem 1 presented in
Section 4.1.1, a proof stated directly on this two-sequence form; its Lean formalization is discussed
in Section 4.1.5.

4.1.3 Background: Lemniscate constant and lemniscate elliptic functions
The lemniscate constant ϖ ∈ R is a transcendental number [70] defined by
                                           Z 1
                                                       1
                                  ϖ=2            √          dx ≈ 2.62205755.
                                            0        1 − x4
It is also characterized as the ratio of perimeter to diameter of the unit lemniscate. See Figure 6.

                                                                 perimeter 2ϖ
                            (x2 + y 2 )2 = x2 − y 2      y



                                                                                x
                                      √                              √
                                   −1/ 2                           1/ 2



                                               diameter 2                  √
    Figure 6: The unit lemniscate (x2 + y 2 )2 = x2 − y 2 with foci at (±1/ 2, 0) and tips at (±1, 0). Its
    perimeter is 2ϖ, and its diameter is 2. Thus ϖ ≈ 2.62206 is its perimeter-to-diameter ratio.

The lemniscate elliptic functions are defined through the arc-length integral of the lemniscate.
Specifically, let                               Z u
                                                       dx
                                     arcsl(u) =     √        ,
                                                 0    1 − x4
for u ∈ [0, 1] and define the lemniscate sine sl(x) on [0, ϖ/2] as the inverse of arcsl. The lemniscate
cosine cl(x) is defined on [0, ϖ/2] by
                                                    ϖ      
                                         cl(x) = sl      −x .
                                                      2

Finally, we briefly note that while ΩN is an algebraic number, since a finite optimal value of
an QCQP with rational coeﬀicients, the limit N 2 /ΩN → ϖ2 (see Lemma 8 in Appendix A.1) is
transcendental.

4.1.4 Continuous-time analysis
In this section, we present the continuous time limit of lemniscate acceleration as an ODE, and
state an analogous convergence theorem. The details for this section can be found in Appendix A.4.


                                                         23
                               continuous ρ(t)      discrete ρk (N = 40)

                       1
                                                                                            σ(t)
                                                                           √
                                                                               2
                                                                               0
                                                                                   0   T /2        T
          ρ(t)


                 √                                                                      t
                     2−1

                                                                                       γ(t)

                                                                         3ϖ/T
                       0                                                    0
                           0                     T /2                T             0   T /2        T

                                        t                                      t
    Figure 7: Continuous-time coeﬀicient profiles. The left panel shows ρ(t) = cl2 (ϖt/(2T )) together
    with the discrete coeﬀicients ρk for N = 40, placed at tk = k T /(N + 1). We  p see that ρ(t) is
    the continuous limit of the discrete coeﬀicients. The right panels show σ(t) = 1/ρ(t) − ρ(t) and
    γ(t) = 3σ̇(t)/σ(t). The arrows indicate endpoint divergences to +∞.


Continuous-time ODE. For a finite time interval [0, T ], define ρ on [0, T ] and σ on [0, T ) by
                             
                           2 ϖt
                 ρ(t) ≜ cl       ,
                             2T
                        p                q
                 σ(t) ≜ 1/ρ(t) − ρ(t) = cl−2 (ϖt/(2T )) − cl2 (ϖt/(2T ))

where ϖ is the lemniscate constant. Figure 7 shows these profiles and the discrete coeﬀicients ρk
approaching the continuous curve ρ(t).
                                                                                    L = N 2 /T 2
Taking the small-stepsize limit of (LemniAcc) under the quantization t = k T /N and √
with N → ∞ suggests that the continuous-time counterparts X and Z of xk and N/( ΩN T ) zk ,
respectively, satisfy the ODE

                                                            σ(t)3
                                                   Ż(t) = −      ∇f (X(t)),
                                                               2
                                                             4
                                                   Ẋ(t) =       Z(t)
                                                           σ(t)3

for t ∈ (0, T ), with initial conditions X(0) = x0 and Ẋ(0) = 0. Eliminating Z(t) and defining the
friction coeﬀicient γ(t) ≜ 3σ̇(t)/σ(t) yields the second-order ODE

                                                  Ẍ + γ(t)Ẋ + 2∇f (X) = 0,

which, in terms of the lemniscate functions cl and sl, has the form
                                 "                #
                                      ϖt        ϖt
                              3ϖ cl 2T       sl 2T
                      Ẍ(t) +            
                                      ϖt +      ϖt
                                                    Ẋ(t) + 2∇f (X(t)) = 0
                              2T sl 2T       cl 2T
                              |         {z          }
                                                        =γ(t)



                                                                24
for t ∈ (0, T ). The endpoint expansions of γ give γ(t) ∼ 3/t as t ↓ 0 and γ(t) ∼ 3/(T − t) as t ↑ T
so near t = 0 the ODE asymptotically matches the continuous-time limit of OGM and near t = T
that of OGM-G [58].
We present an analogous Lyapunov analysis for the continuous-time ODE.
Theorem 2. Fix T > 0, and let f : R d → R be an L-smooth convex function with a minimizer x⋆ .
Any trajectory X ∈ C 2 ([0, T ]; R d ) satisfying Ẍ + γ(t)Ẋ + 2∇f (X) = 0 on (0, T ), with X(0) = x0
and Ẋ(0) = 0, has the following bounds on the endpoint X(T ):

                                                     ϖ4
                                 k∇f (X(T ))k2 ≤       4
                                                         kx0 − x⋆ k2 ,
                                                     T
                                                         ϖ2
                                 f (X(T )) − f (x⋆ ) ≤     2
                                                             kx0 − x⋆ k2 .
                                                        2T

Proof sketch. We denote xT ≜ X(T ), set Z(t) ≜ σ(t)3 Ẋ(t)/4 for t ∈ (0, T ), and define the
continuous-time Lyapunov function V(t) on (0, T ) by

                      1 − ρ2                        (1 − ρ)2
             V(t) ≜          (f (X(t)) − f (x⋆ )) −          (f (xT ) − f (x⋆ ))
                        2ρ                             2ρ
                                                               2
                                                                                        !
                                                                                    2
                        ϖ2                  1 + ρ2 T                          T
                      +         X(t) − x⋆ +          Z(t)          − xT − x⋆ + Z(t)         .
                        2T 2                1 − ρ2 ϖ                          ϖ

The derivative can be expressed as the following sum of Bregman divergences Df (x, y) ≜ f (x) −
f (y) − hx − y, ∇f (y)i, thus is nonpositive:
                                                                        
                      d           ϖ                     1 3
                        V(t) = −      σρDf (x⋆ , X(t)) + σ Df (xT , X(t)) ≤ 0.
                     dt           T                     2

The limits of the endpoints t ↓ 0, t ↑ T are

                                       ϖ2                2                2
                                                                             
                               V(0+) =       kx 0 −  x ⋆ k  − kx T − x ⋆ k     ,
                                       2T 2
                                        T2
                             V(T −) =       k∇f (xT )k2 + f (xT ) − f (x⋆ ),
                                       2ϖ2
                                                   
and the bounds follow by chaining ϖ2 /(2T 2 ) kx0 − x⋆ k2 ≥ V(0+) ≥ V(T −) and V(T −) ≥
            
 T 2 /(2ϖ2 ) k∇f (xT )k2 for the gradient bound and V(T −) ≥ f (xT ) − f (x⋆ ) for the function value
bound.

4.1.5 Lean formalization
The convergence theory of this section is machine-checked in Lean 4 with mathlib [16, 66] by
Stage 3 of AutoOPT (Section 3.3); Figure 8 shows an illustrative Stage-3 prompt. The resulting
Lean project proves ten public theorem declarations, stating the smooth convex inequality over the
Euclidean space R d and the algorithmic and continuous-time results over an arbitrary complete
real inner-product space, which subsumes the manuscript’s R d setting. The declaration Lemn
iAcc.gradient_rate is the Lean counterpart of Theorem 1, proving both displayed bounds;

                                                    25
 Using the lean-verify skill, formalize and verify the lemniscate acceleration results that
 are located in the ResearchLog folder. Targets for the verification are the coefficient
 construction, the Lyapunov identities, the convergence theorem, the function-value bound,
 the continuous-time theorem. State the results in the manuscript's Euclidean setting or a
 generalization of it. Constraints are Lean 4.32.0 with mathlib 4.32.0, pinned by commit; no
 sorry, axiom, admit, or unsafe anywhere in the development.
 Deliverables are a Lake project passing lake build and the hygiene scan; wrappers Challenge.le
 an, S o l u t i o n . l e a n, and c o n f i g . j s o n naming the agreed public theorem surface for comparator
 replay; build, axiom-audit, and replay logs under artifacts/.
 Please ask me clarifying questions if anything is not clear to you.

    Figure 8: An illustrative Stage-3 prompt for the formal verification of the lemniscate accelerated
    gradient method using the lean-verify skill.

  Public theorem declarations                                                    10
  Dependency nodes in the closure                                                22
  Lean source files                                                              22
  Lines of Lean                                                                7,384
  lake build jobs, native macOS                                                8,687
  Comparator replay time, native macOS                                         109 s
  Comparator replay time, WSL2 real Landrun                                    155 s
  Toolchain                                                 Lean 4.32.0, mathlib 4.32.0, commit-pinned
  Axioms used                                               propext, Quot.sound, Classical.choice
    Table 2: Summary statistics of the lemniscate acceleration Lean project: it formalizes a fixed
    22-node dependency closure of manuscript claims and their supporting steps through ten public
    theorem declarations, builds cleanly under the commit-pinned toolchain, and is accepted by the
    comparator replay under exactly the three standard axioms listed.


LemniAcc.functionValue_rate proves both bounds of Corollary 1; and LemniAcc.continu
ousTime_lyapunov proves both endpoint bounds of Theorem 2, with the C 2 trajectory of the
ODE supplied as a hypothesis exactly as stated there. The supporting declarations follow the
paper’s proofs: recurrence_existsUnique is Lemma 1; omega_bounds gives the strict bounds
(N + 1)2 /ϖ2 < ΩN < (N + 1)2 of Corollary 2; finite_interpolation establishes (6) that
the proofs use; iterates constructs the trajectory of (LemniAcc); lyapunov_terminal and
lyapunov_decrement are Lemmas 2 and 3; and Lemniscatic.sigma_identities combines the
lemniscatic calculus of Lemma 10 with the σ-identities of Lemma 11. As a representative statement,
LemniAcc.gradient_rate reads as follows, where E is an arbitrary complete real inner-product
space:




                                                       26
            LemniAcc/ Lean/Lake project for lemniscate acceleration
                 lakefile.toml, lean-toolchain build configuration; commit-pinned Lean and mathlib
                 config.json pins the ten theorem names and permitted axioms for the comparator
                 Challenge.lean comparator challenge wrapper over the stated development

                 Solution.lean comparator solution wrapper, replayed against it
                 AxiomAudit.lean runs the axiom audit over the ten declarations
                 LemniAcc.lean umbrella module importing the development
                 LemniAcc/ proof modules, organized in dependency layers:
                      Model, FiniteInterpolation problem class, oracle data, interpolation inequality

                      Discrete/Recurrence/ coeﬀicient existence and uniqueness by shooting
                      Discrete/ iterates, Lyapunov identities, discrete rate theorems
                      Lemniscatic/ the lemniscate integral and lemniscatic calculus
                      Continuous/ the continuous-time Lyapunov development
                 artifacts/ build, hygiene, axiom-audit, and comparator replay logs
    Figure 9: File structure of the Lean project for the lemniscate accelerated gradient method (module
    files grouped by folder). The wrappers Challenge.lean, Solution.lean, and config.json pin
    the ten public theorems and the permitted axioms for the comparator, and artifacts/ records the
    build, audit, and replay logs.

   theorem gradient_rate
       (N : Nat) (hN : 1 ≤ N)
       (M : SmoothConvexModel E) (x0 xStar : E)
       (hxStar : M.IsMinimizer xStar) :
       ∥M.grad (Discrete.canonicalX N M x0 N)∥ ^ 2 ≤
           ((M.L : R) ^ 2 / omega N ^ 2) * ∥x0 - xStar∥ ^ 2
         ∧
         ((M.L : R) ^ 2 / omega N ^ 2) * ∥x0 - xStar∥ ^ 2 ≤
           (Lemniscatic.varpi ^ 4 * (M.L : R) ^ 2 *
               ∥x0 - xStar∥ ^ 2) /
             (((N + 1 : Nat) : R) ^ 4)
Figure 9 shows the layout of the project, and Table 2 reports its summary statistics. The project
comprises 22 Lean source files and 7,384 lines of Lean, organized in dependency layers that parallel
the paper: the problem class and the interpolation inequality, the recurrence construction, the dis-
crete Lyapunov development, and the lemniscatic calculus supporting the continuous-time theorem.
It builds on mathlib’s theories of inner-product and Euclidean spaces, differentiability, and one-
variable calculus; in particular, the shooting argument of Appendix A.1 rests on the intermediate
value theorem, and the lemniscatic calculus of Appendix A.4 on interval integration.
The project passes lake build under the commit-pinned toolchain Lean 4.32.0 with mathlib 4.32.0
(8,687 build jobs on native macOS), a hygiene scan confirms that no sorry, axiom, admit, or unsafe
appears anywhere in the development, and an axiom audit reports that every public declaration
depends on exactly the three standard axioms propext, Quot.sound, and Classical.choice.
The comparator then independently certified the ten public theorems: the approved wrappers
Challenge.lean, Solution.lean, and config.json were replayed end to end, rebuilding both
wrappers, exporting their environments, and re-checking the solution with the Lean default kernel,


                                                    27
in 109 seconds; in this first project both wrappers import the proof development itself, and the
ITEM-f project of Section 4.2.4 strengthens the wrapper design with a proof-free statement layer.
Each project was certified twice, first replayed on native macOS, and then in a Linux environment
with Landlock isolation and systemd restrictions. The project was accepted by the Lean-kernel
of the sandboxed environment in 155 seconds, thus carries the evidence label Lean+comparato
rverified(WSL2realLandrun;systemdaddress-familyrestriction). The projects and their
verification artifacts accompany the paper.

4.2 ITEM-f for eﬀicient function-value ratio contraction
Consider the unconstrained minimization problem

                                             minimize f (x),                                             (P ′ )
                                                x∈R d

where f : R d → R is an L-smooth and µ-strongly convex function with 0 < µ < L. Strong convexity
guarantees that f has a unique minimizer x⋆ . Denote f⋆ ≜ f (x⋆ ).

Algorithm statement
The method (ITEM-f) is

                              ak ϕN −k−1                   ϕN −k−1 +
            xk+1 = x+
                    k +                      (x+ − x+   )+        (xk − xk ),                      (ITEM-f)
                           (1 − q)ak+1 ϕN −k   k    k−1     ϕN −k

for k = 0, 1, 2, . . . , N − 1, where N is a prespecified iteration count, x0 ∈ R d is the start-
                                                                                  √
ing point, x+ −1 = √    x0 by convention,
                                     √    x +
                                            k = x k − 1
                                                      L ∇f (x k ), q = µ/L, ϕ 0 =   1 − q, ϕN =
((1 − q)ΥN + aN ) / 1 − q, ϕk = 2ΥN ak − q for 1 ≤ k ≤ N − 1 and a0 , a1 , . . . , aN and ΥN
are positive constants that we define in Lemma 4.
Taylor and Drori [62, Appendix E] reported numerically optimized step sizes of ITEM-f for N =
1, . . . , 5 in the setting L = 1 and µ = 0.1, but did not assign a name to the resulting method. They
also derived a closed-form method with a convergence analysis, called the Information-Theoretic
Exact Method (ITEM), for a related performance criterion. We use the name ITEM-f to acknowl-
edge their numerical construction while distinguishing it from ITEM. The optimization objectives
underlying ITEM and ITEM-f are discussed further in Section 4.2.2.

Construction of the coeﬀicients
To fully define ITEM-f, it remains to specify the coeﬀicients a0 , a1 , . . . , aN and ΥN . Lemma 4
formally defines these coeﬀicients, and Figure 10 illustrates the underlying geometric construction.
Lemma 4. For any integer N ≥ 1 and 0 < q < 1, there exist a unique real ΥN > 1, unique reals

                              1/ΥN = a0 < a1 < · · · < aN < aN +1 = ΥN ,

and unique positive reals b0 , b1 , . . . , bN , bN +1 satisfying the following conditions. Write C = (ΥN , 0)




                                                        28
                                             P3       P4                                P3 P4 ∥ a-axis
                                                                                        O, P0 , P1 collinear
    2                                                                                   symmetry chords (through S)
                                      P2
                                                                                        tangent from S, touching at P2
                                                                                        P1 , P2 , P3 on circle
                                                                                        endpoints P0 , P4
                           P1
b
    1

                       P0

         S         O                                       C
    0
        −1             0             1            2   Υ3        3      4
                                                a
        Figure 10: The planar construction underlying Lemma 4, shown       p for N = 3, q = 0.1. The inter-
        mediate points P1 , . . . , PN (◦) lie on the circle of radius RN = Υ2N − 1 centered at C = (ΥN , 0);
        the endpoints P0 and PN +1 () lie strictly inside; successive points satisfy (Pk − C) · (Pk+1 − C) =
        RN2
            (1 − q ak+1 /ΥN ).
                             √ Shooting (red). The construction is run backward from the horizontal final
        edge bN = bN +1 = 1 − q RN (dashed); ΥN is the value for which O, P0 , P1 are collinear in this
        order (dotted). Symmetry (green). The map T (a, b) = (1/a, b/a) satisfies T (Pk ) = PN +1−k ; hence
        every chord Pk PN +1−k passes through S = (−1, 0). For odd N , the tangent from S touches the
        circle at the fixed point P(N +1)/2 .

               q
and RN =           Υ2N − 1 and write Pk = (ak , bk ) ∈ R 2 for 0 ≤ k ≤ N + 1. The requirements are:

                                kPk − Ck2 = RN
                                             2
                                               ,    1 ≤ k ≤ N,
                                                                      
                                                                 qa
                                (Pk − C) · (Pk+1 − C) = RN2
                                                              1 − Υk+1
                                                                    N
                                                                         ,   0 ≤ k ≤ N,
                                           √                                                                   (17)
                                P0 = Υ1N , 1−qΥN
                                                RN
                                                     ,
                                              p         
                                PN +1 = ΥN , 1 − q RN .

The proof of Lemma 4 is provided in Appendix B.1. To clarify, aN +1 is not used in the definition
of ITEM-f but we defined it for convenience. We can compute the numerical values of a0 , . . . , aN
and ΥN again by a one-dimensional bisection, as discussed in Appendix B.1.
The geometric construction carries a symmetry analogous to the lemniscate recurrence in Sec-
tion 4.1: the map T (a, b) ≜ (1/a, b/a), defined for a>0, maps the circle a2 + b2 − 2ΥN a + 1 = 0
to itself and reverses the construction, T (Pk ) = PN +1−k for 0 ≤ k ≤ N + 1, so that ak aN +1−k = 1
and ak bN +1−k = bk (Lemma 17 in Appendix B.1); in Figure 10 this symmetry is visible as the
chords Pk PN +1−k passing through the point S ≜ (−1, 0). This symmetry supplies the identities
ak+1 aN −k = 1 and a1 aN = 1 used in the convergence proof of Section 4.2.1.

Convergence theorem
Theorem 3. Let N ≥ 1 and d ≥ 1 be integers, and let f : R d → R be L-smooth and µ-strongly
convex with q = µ/L ∈ (0, 1), let ΥN and a0 , . . . , aN be as in Lemma 4, and let x⋆ = argmin f .
Then, for any starting point x0 ∈ R d , the final iterate xN of (ITEM-f) satisfies
                                  1                           √                 
                 f (xN ) − f⋆ ≤ 2 f (x0 ) − f⋆ ≤ 4(1 − q)2N f (x0 ) − f⋆ .                  (18)
                                 ΥN

                                                               29
We prove Theorem 3 in the following section.

4.2.1 Convergence proof
In this section, we prove Theorem 3. Throughout, f : R d → R is an L-smooth and µ-strongly
convex function with the minimizer x⋆ , q = µ/L, and xk denotes the iterates of (ITEM-f) with
the convention x+    −1 = x0 . The argument has three steps. We first define a Lyapunov sequence
V1 , . . . , VN along the iterates, whose coeﬀicients are read off from the multipliers of the analytic
dual certificate found in Stage 2 of the pipeline, and compress it into a compact form built from
transformed interpolation gaps and vectors Wk ∈ R 2d . We then compare the two endpoints: V1
is at most (f (x0 ) − f⋆ ) /ΥN , and VN dominates ΥN (f (xN ) − f⋆ ). Finally, Lemma 6 shows that
the sequence is nonincreasing, and chaining the three facts proves Theorem 3. The norm identities
that drive these computations (Lemma 5) are stated below and proved in Appendix B.2.
For 1 ≤ k ≤ N − 1, we define the Lyapunov sequence
                                                                                           
                                 µ              2       1                                 2
       Vk ≜ ak f (xk−1 ) − f⋆ − kxk−1 − x⋆ k −                k∇f (xk−1 ) − µ(xk−1 − x⋆ )k
                                 2                  2(L − µ)
              µ(1 − q)a2k+1
            +               kxk − x⋆ k2
                  2ΥN
                       µ                                                        2
            +                       (1 − q)ck ak+1 (xk − x⋆ ) − ak (x+
                                                                     k−1 − x⋆ )   ,
              2ΥN (1 − q)(1 − c2k )
and for the final iteration N , define
                                                                                              
                                    µ            2       1                                   2
     VN ≜ aN f (xN −1 ) − f⋆ − kxN −1 − x⋆ k −                 k∇f (xN −1 ) − µ(xN −1 − x⋆ )k
                                    2                2(L − µ)
               µΥN
           +         kxN − x⋆ k2
                 2
                    L                                                2
           +                                             N −1 − x⋆ )
                             (1 − q)ΥN (xN − x⋆ ) − aN (x+             ,
               2ΥN (1 − q)

where we define ck ≜ 1 − (qak+1 )/ΥN for 1 ≤ k ≤ N .
Following the approach of [62], we introduce the convex (L − µ)-smooth function and its gradient:
                                                       µ
                                  fe(x) ≜ f (x) − f⋆ − kx − x⋆ k2 ,
                                                       2
                                          e
                                  gek ≜ ∇f (xk ) = ∇f (xk ) − µ(xk − x⋆ ).

This makes ge⋆ = 0 and fe(x⋆ ) = 0. For i, j ∈ IN
                                                ⋆ , denote its interpolation gap by


                                                                       1
                   Gi,j ≜ fe(xi ) − fe(xj ) − he
                                               g j , x i − xj i −             gi − gej k2 ≥ 0,
                                                                             ke
                                                                    2(L − µ)

which is nonnegative by (6) applied to fe. From the relation x+                                 −1 e
                                                                 i − x⋆ = (1 − q)(xi − x⋆ ) − L g   i
                                −1
(which follows from xi = xi − L ∇f (xi ), ∇f (xi ) = gei + µ(xi − x⋆ ), and µ = qL), the three-point
                     +

identity follows:
                                     1
                             Gi,⋆ −        x+ − x⋆ , gej = Gi,j − G⋆,j .                        (19)
                                    1−q i

                                                        30
To simplify the analysis of (ITEM-f), for 1 ≤ k ≤ N , we define
                                                                     
                                               k−1 − x⋆ )
                                          ak (x+
                                                                     
                     Wk ≜  (1 − q)ak+1 (xk − x⋆ ) − ck ak (x+ − x⋆ )  ∈ R 2d ,               (20)
                                                             k−1
                                                sk
                     √
where we define sk ≜ q ak+1 ϕN −k /ΥN . At k = N , these definitions give the boundary values
                    p                                    √
cN = 1 − q and sN = q(1 − q), using aN +1 = ΥN and ϕ0 = 1 − q.
For 1 ≤ k ≤ N −1, the relation s2k +c2k = 1 can be proved using the symmetry identity ak+1 aN −k = 1
of the construction:
                                                                                        
            qa2k+1                          qak+1 2 qak+1                            qak+1 2
   2    2
  sk + ck =        (2ΥN aN −k − q) + 1 −             =        (2ΥN − qak+1 ) + 1 −             = 1.
             Υ2N                             ΥN          Υ2N                          ΥN

For 1 ≤ k ≤ N , define                              
                                        c k Id sk Id
                                  Ok ≜                 ∈ R 2d×2d .
                                       −sk Id ck Id
For 1 ≤ k ≤ N − 1, the identity s2k + c2k = 1 makes Ok orthogonal, and multiplying it by Wk gives
                                                                
                                  (1 − q)ak+1 (xk − x⋆ )
                                                                
             Ok Wk =  (1 − q)ck ak+1 (xk − x⋆ ) − ak (x+ − x⋆ )  , 1 ≤ k ≤ N − 1.          (21)
                                                         k−1
                                             sk
Since Ok is orthogonal for k < N , this gives the two quadratic terms in Vk . At k = N , where
s2N + c2N = 1 − q and the terminal block ON is not orthogonal, the quadratic terms in the final
VN follow instead from p
                       the direct expansion in the third identity of Lemma 5, using cN = 1 − q,
aN +1 = ΥN , and sN = q(1 − q). Thus the Lyapunov sequence has the compact form
                                                   µ
                         Vk = ak Gk−1,⋆ +                kWk k2 ,   1 ≤ k ≤ N,                 (22)
                                              2(1 − q)ΥN

where the norm is the Euclidean norm on R 2d .
Lemma 5 (Norm identities). The squared norms kWk k2 for the iterates of (ITEM-f) satisfy the
following identities:
                                       2ΥN                             Υ N a0
         kW1 k2 = (1 − q) kx0 − x⋆ k2 −                  0 − x⋆ , g
                                             (a1 − a0 ) x+        e0 +         g 0 k2 ,
                                                                              ke
                                         µ                              µL
                                            2
                2          ΥN (ck − 1)e  gk
         kWk+1 k = Wk −                         , 1 ≤ k ≤ N − 1,
                            µ     sk gek
                                             1                                           2
         kWN k2 = (1 − q)Υ2N kxN − x⋆ k2 +      (1 − q)ΥN (xN − x⋆ ) − aN (x+N −1 − x⋆ )   .
                                             q

The proof is tedious but straightforward algebra on the coordinate relations of the construction; it
is deferred to Appendix B.2.


                                                    31
Lemma 6 (Monotonicity). For 1 ≤ k ≤ N − 1,

                              Vk − Vk+1 = ak Gk−1,k + (ak+1 − ak )G⋆,k ≥ 0.

Consequently, V1 ≥ V2 ≥ · · · ≥ VN .

Proof. From the definition of Wk and ck = 1 − qak+1 /ΥN , we have
                             
          (ck − 1)e  gk
                          , Wk         = (1 − q)ak+1 (xk − x⋆ ) − ak (x+
                                                                       k−1 − x⋆ ), g ek ,
             sk gek               R 2d
                                  2
                    (ck − 1)e  gk                                                      2qak+1
                                                           gk k2 = 2(1 − ck ) ke
                                       = (1 − ck )2 + s2k ke                   g k k2 =         gk k2 .
                                                                                               ke
                        sk gek                                                            ΥN

Using the compact form (22) and expanding the second identity of Lemma 5, we obtain
                                                 µ                           
       Vk − Vk+1 = ak Gk−1,⋆ − ak+1 Gk,⋆ +                kWk k2 − kWk+1 k2
                                           2(1 − q)ΥN
                 = ak Gk−1,⋆ − ak+1 Gk,⋆
                           1                                                     ak+1
                      +         (1 − q)ak+1 (xk − x⋆ ) − ak (x+   − x⋆ ), gek −           g k k2
                                                                                         ke
                         1−q                                  k−1               L(1 − q)
                                                       
                                   1
                 = ak Gk−1,⋆ −           x+    − x  ,
                                                   ⋆ ke
                                                      g   + ak+1 G⋆,k
                                 1 − q k−1
                 = ak (Gk−1,k − G⋆,k ) + ak+1 G⋆,k
                    = ak Gk−1,k + (ak+1 − ak )G⋆,k ,

where the second equality uses the above two identities and the third and fourth use the three-point
identity (19) at (i, j) = (k, k) and (k − 1, k), respectively. Since ak+1 ≥ ak > 0 and Gi,j ≥ 0, the
last line is nonnegative.

We now provide the proof of Theorem 3.

Proof of Theorem 3. The relation a0 = 1/ΥN , the first identity in Lemma 5, and the compact form
(22) of V1 give
                                                                              
                   f (x0 ) − f⋆                       1
                                − V1 = (a1 − a0 )          x − x⋆ , ge0 − G0,⋆
                                                            +
                       ΥN                           1−q 0
                                     = (a1 − a0 )G⋆,0 ≥ 0,

where the last equality applies (19) at (i, j) = (0, 0).
The relation aN +1 = ΥN , the third identity in Lemma 5, and the compact form (22) of VN give
                                    
              VN − ΥN f (xN ) − f⋆
                                                                                     2
                             L                                                ΥN
                    −              (1 − q)ΥN (xN − x⋆ ) − aN (x+
                                                               N −1 − x ⋆ ) −    e
                                                                                 g N
                        2(1 − q)ΥN                                             L


                                                       32
                                                         
                                 1
               = aN       GN −1,⋆ −    x+ − x⋆ , geN          + ΥN G⋆,N
                               1 − q N −1
               = aN (GN −1,N − G⋆,N ) + ΥN G⋆,N
               = aN GN −1,N + (ΥN − aN )G⋆,N ≥ 0,

where the second equality applies (19) at (i, j) = (N − 1, N ). The completed square is nonnegative,
so VN ≥ ΥN (f (xN ) − f⋆ ); combining the two endpoint bounds with Lemma 6 gives

                            f (x0 ) − f⋆                                    
                                         ≥ V1 ≥ · · · ≥ VN ≥ ΥN f (xN ) − f⋆ .
                                ΥN
The explicit relaxation in the second inequality then follows from Lemma 18.

4.2.2 AutoOPT design: Optimal method for contracting function-value suboptimality
The method (ITEM-f) was designed by AutoOPT as the optimal fixed-step first-order method
for contracting the function-value suboptimality. Specifically, AutoOPT minimizes the contraction
factor CN in the guarantee
                                   f (xN ) − f⋆ ≤ CN (f (x0 ) − f⋆ )
and attains the optimal value CN = 1/Υ2N . The pipeline ran as for lemniscate acceleration (Sec-
tion 4.1.2): bnb-pep-skill wrote the BnB-PEP formulation of this design problem, reproduced with
light editing in Appendix B.3, and, upon our approval, solved the resulting QCQP numerically over
a range of horizons.
Taylor and Drori [62, Appendix E] previously considered the same optimization problem and nu-
merically obtained ITEM-f for N = 1, . . . , 5 in the setting L = 1 and µ = 0.1. From the Stage-1
formulation and its numerical solutions, frontier-llm-consult identified a closed-form expression for
the algorithm valid for arbitrary N , µ, and L, together with an analytic feasible point of the dual
certifying the contraction factor 1/Υ2N , and then rewrote the method, first obtained in the stepsize
variables of the design problem, as the momentum form (ITEM-f) in which this paper states it; con-
tinued consultation converted the certificate’s multipliers into the Lyapunov proof of Section 4.2.1,
stated on that momentum form, and Section 4.2.4 discusses its Lean formalization.

4.2.3 Continuous-time analysis
For a fixed finite horizon T > 0 √
                                 and strong convexity parameter µ > 0, let Υ > 1 be the unique
real number such that, with s ≜ 1 − Υ−2 ,
                                 p        Z arcsin s
                                                          dx
                                   2µ T =            √             .
                                            0          1 − s sin x

We note the continuous-time limit concerns L = N 2 /T 2 , and with qN = µT 2 /N 2 , we have
ΥN (qN ) → Υ as N → ∞. Define a, b : [0, T ] → R by
                                              r
                                                2µa(t)
                                 ȧ(t) = b(t)          ,
                                                  Υr
                                                       2µa(t)
                                 ḃ(t) = (Υ − a(t))           ,
                                                         Υ

                                                   33
  Public theorem declarations                                                 14
  Dependency nodes in the closure                                             20
  Lean source files                                                           38
  Lines of Lean                                                             7,985
  lake build jobs                                                           8,694
  Comparator replay time, native macOS                                      105 s
  Comparator replay time, WSL2 real Landrun                                 115 s
  Toolchain                                              Lean 4.32.0, mathlib 4.32.0, commit-pinned
  Axioms used                                            propext, Quot.sound, Classical.choice
    Table 3: Summary statistics of the ITEM-f Lean project: it formalizes a fixed 20-node dependency
    closure of manuscript claims and their supporting steps through fourteen public theorem declara-
    tions, builds cleanly under the commit-pinned toolchain, and is accepted by the comparator replay
    under exactly the three standard axioms listed.


                                              1
                                       a(0) =   ,
                                              Υ
                                              √
                                                Υ2 − 1
                                       b(0) =          .
                                                  Υ

Then the continuous-time ODE of ITEM-f is
                                    3ȧ(t)
                          Ẍ(t) +          Ẋ(t) + 2∇f (X(t)) = 0,   0 ≤ t ≤ T.
                                    2a(t)

Remark 1 (Continuous-time convergence of ITEM-f). For an L-smooth and µ-strongly convex
function f : R d → R, any solution X ∈ C 2 ([0, T ]; R d ) of the ODE above with X(0) = x0 and
Ẋ(0) = 0 satisfies
                                               1
                              f (X(T )) − f⋆ ≤ 2 (f (X(0)) − f⋆ ) .
                                              Υ
This can be shown with a continuous-time Lyapunov function
                          µ              µa(t)2                   1                                2
V(t) = a(t) f (X(t)) − f⋆ − kX(t) − x⋆ k2 +       kX(t) − x⋆ k2 +       ȧ(t)(X(t) − x⋆ ) + a(t)Ẋ(t) ,
                           2                2Υ                    4a(t)

by the monotonicity V̇(t) ≤ 0 and the endpoints V(0) = Υ−1 (f (X(0)) − f⋆ ) and V(T ) ≥ Υ (f (X(T )) − f⋆ ).
We do not pursue a detailed proof or Lean verification of this remark; both can be generated by
running the AutoOPT pipeline on this continuous-time claim.

4.2.4 Lean formalization
The convergence theory of ITEM-f is machine-checked in the same manner as that of lemniscate
acceleration (Section 4.1.5), by a second Lean project whose fourteen public declarations correspond
to the results of this section and its appendix. The root declaration ITEMf.convergence is the
Lean counterpart of Theorem 3, stated over the Euclidean space R d and proving both inequalities
of (18); it reads:



                                                    34
         ITEM-f/ Lean/Lake project for analytic ITEM-f
              lakefile.toml, lean-toolchain build configuration; commit-pinned Lean and mathlib
              config.json pins the fourteen theorem names and permitted axioms for the comparator
              Challenge.lean states the fourteen declarations, one approved placeholder each

              Solution.lean the same statements, closed by the proof development
              AxiomAudit.lean runs the axiom audit over the fourteen declarations
              ITEMf.lean umbrella module importing the development
              ITEMf/ proof modules, organized in dependency layers:
                   Spec/ proof-free statement interfaces; all that Challenge.lean imports
                   Model/ problem class, interpolation inequality, transformed objective
                   Construction/ the shooting argument: one-step map, orbit, target angle, symmetry, rate
                   Algorithm/ iterates, coeﬀicient identities, coordinate relations
                   Lyapunov/ norm identities, rotations, monotonicity
                   Convergence.lean the convergence theorem

              artifacts/ build, hygiene, axiom-audit, and comparator replay logs
    Figure 11: File structure of the ITEM-f Lean project (module files grouped by folder). The
    proof-free Spec/ layer is all that Challenge.lean imports, so the proofs reach the comparator
    only through Solution.lean; config.json pins the fourteen public theorems and the permitted
    axioms, and artifacts/ records the build, audit, and replay logs.

   theorem convergence
       {d N : Nat} (hd : 1 ≤ d) (hN : 1 ≤ N)
       (M : StronglyConvexSmoothModel (Euclidean d)) {xStar : Euclidean d}
       (hxStar : M.IsMinimizer xStar)
       (C : CoeffData N) (hC : ValidCoefficients M.q C)
       (x0 : Euclidean d) :
       M.f (itemfIterate M C x0 N) - M.f xStar ≤
             (1 / C.Upsilon ^ 2) * (M.f x0 - M.f xStar) ∧
         (1 / C.Upsilon ^ 2) * (M.f x0 - M.f xStar) ≤
             4 * (1 - Real.sqrt M.q) ^ (2 * N) *
               (M.f x0 - M.f xStar)
The supporting declarations follow the paper’s proofs. coefficientsExistUnique is the con-
struction Lemma 4, obtained through the shooting argument of Appendix B.1 via oneStepMap
(Lemma 13), orbitComparison (Lemma 14), targetAngle (Lemma 15), and shootingIffAdmis
sible (Lemma 16); involutionSymmetry is Lemma 17; explicitRate is Lemma 18; and finiteIn
terpolation is (6). The Lyapunov argument of Section 4.2.1 is formalized by transformedMemF0,
threePointIdentity, coordinateRelations (the identities (46)), normIdentities (Lemma 5),
and lyapunovMonotone (Lemma 6).
The project comprises 38 Lean source files and 7,985 lines of Lean, organized as in Figure 11 in a
layout parallel to the LemniAcc project, with one addition: a proof-free specification layer (ITEM
f/Spec) contains the definitions and statements of the fourteen declarations, and the comparator-
facing Challenge.lean, which restates each declaration with exactly one approved placeholder,
imports only this layer, so the proofs reach the comparator only through Solution.lean, which


                                                      35
closes every placeholder. The project passes lake build under the same commit-pinned toolchain
(8,694 build jobs); the hygiene scan confirms that no sorry, axiom, admit, or unsafe appears
anywhere in the proof development or in Solution.lean; and the axiom audit again reports ex-
actly propext, Quot.sound, and Classical.choice for every public declaration. The comparator
accepted the fourteen public theorems twice, under the two-platform protocol, evidence label, and
disclosures of Section 4.1.5: in 105 seconds on native macOS and in 115 seconds under the isolated
WSL2 real-Landrun replay; Table 3 summarizes the project.

4.3 Self-H-duality of LemniAcc and ITEM-f
The notion of H-duality was introduced in [32] and further developed in [33, 72, 73, 71]. Recall that
a fixed-step first-order method (FSFOM) with stepsizes {hi,j }0≤j<i≤N is a method of the form

                                        1X
                                          i−1
                          xi = xi−1 −      hi,j ∇f (xj ),    i = 1, . . . , N.
                                        L
                                          j=0


The H-dual of this method is the FSFOM with stepsizes hA      i,j ≜ hN −j,N −i for 0 ≤ j < i ≤ N .
Viewing the lower-triangular array {hi,j }0≤j<i≤N as an (N + 1) × (N + 1) matrix, taking the H-
dual corresponds to taking the anti-diagonal transpose, i.e., the entries are reflected across the
anti-diagonal rather than the usual diagonal. These prior works observe that H-duality exchanges
the type of guarantee while preserving its worst-case value: for example, OGM, which reduces the
function value under an initial-distance condition, maps to OGM-G, which reduces the squared
gradient norm under an initial function-gap condition, with exactly the same constant [32].
Remark 2 (Self-H-duality). In this work, we point out that (LemniAcc) and (ITEM-f) are self-H-
dual in the sense that each method is its own H-dual. Moreover, the corresponding continuous-time
ODEs are also self-H-dual in the sense of [32]: the ODEs have the form Ẍ(t) + γ(t)Ẋ(t) +
2∇f (X(t)) = 0, with the symmetry γ(t) = γ(T − t) for 0 < t < T . We record this observation
without a detailed proof or Lean verification; a reader who wants both can obtain them by running
the AutoOPT pipeline on this claim.


5   Conclusion
In this work, we present AutoOPT, a framework that automates much of the labor-intensive parts
in the design and analysis of optimal first-order methods. AutoOPT combines the domain-specific
methodology of performance estimation programming with the general-purpose intelligence of fron-
tier LLMs. We demonstrate the strength of this harness with two case studies, producing two opti-
mal algorithms of independent interest: lemniscate acceleration (Section 4.1) and analytic ITEM-f
(Section 4.2). More broadly, this work serves as a case study of how a domain-specific harness can
augment the general-purpose intelligence of LLMs.
AutoOPT has significant limitations. For example, it does not handle stochastic or second-order
optimization. We expect AutoOPT itself to be extensible to such settings, and we believe the general
principle of the domain-specific harness extends further still.
Finally, we offer this paper itself as one data point on what scholarship can look like in the era of
LLM intelligence. As stated in the Preface, we believe domain experts can contribute productively

                                                 36
in an AI-driven research workflow by augmenting the general-purpose intelligence of LLMs with
harnesses derived from their expertise. Automation lets us take on harder and more interesting
problems and elevate our scholarship, and it frees the researcher to concentrate on the parts of re-
search that are irreducibly human: choosing the problems, interpreting the answers, and conveying
the insight to others.


Acknowledgments
S. Das Gupta and E. K. Ryu acknowledge support by AFOSR Grant Number FA9550-25-1-0183.


References
 [1] Agent Skills. Agent Skills overview, 2026. URL: https://agentskills.io/home [cited
     2026-08-03].
 [2] Jason M. Altschuler and Pablo A. Parrilo. Acceleration by stepsize hedging: Multi-Step
     Descent and the Silver Stepsize Schedule. Journal of the ACM, 72(2):1–38, 2025. doi:
     10.1145/3708502.
 [3] Jason M. Altschuler and Pablo A. Parrilo. Acceleration by stepsize hedging: Silver Stepsize
     Schedule for smooth convex optimization. Mathematical Programming, 213(1–2):1105–1118,
     2025. doi:10.1007/s10107-024-02164-2.
 [4] Jason M. Altschuler and Pablo A. Parrilo. Stepsize Hedging: An alternative mechanism for
     accelerating gradient descent, 2026. To appear as an invited Research Highlight in the 2026
     INFORMS Computing Society Newsletter. arXiv:2605.31386.
 [5] Anthropic. Claude Code overview, 2026. URL: https://code.claude.com/docs/en/overvi
     ew [cited 2026-08-03].
 [6] Anthropic. Extend Claude with skills, 2026. URL: https://code.claude.com/docs/en/sk
     ills [cited 2026-08-03].
 [7] Artelys. Artelys Knitro, 2026. URL: https://www.artelys.com/solvers/knitro/ [cited
     2026-08-03].
 [8] Minkyung Baek, Frank DiMaio, Ivan Anishchenko, Justas Dauparas, Sergey Ovchinnikov,
     et al. Accurate prediction of protein structures and interactions using a three-track neural
     network. Science, 373(6557):871–876, 2021. doi:10.1126/science.abj8754.
 [9] Jeff Bezanson, Alan Edelman, Stefan Karpinski, and Viral B. Shah. Julia: A fresh approach
     to numerical computing. SIAM Review, 59(1):65–98, 2017. doi:10.1137/141000671.
[10] Richard H. Byrd, Jorge Nocedal, and Richard A. Waltz. KNITRO: An integrated package
     for nonlinear optimization. In Gianni di Pillo and Massimo Roma, editors, Large-Scale Non-
     linear Optimization, volume 83 of Nonconvex Optimization and Its Applications, pages 35–59.
     Springer, Boston, MA, 2006. doi:10.1007/0-387-30065-1_4.
[11] Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Hieu Pham, Xuanyi
     Dong, Thang Luong, Cho-Jui Hsieh, Yifeng Lu, and Quoc V. Le. Symbolic discovery of

                                                37
    optimization algorithms. In Advances in Neural Information Processing Systems, volume 36,
    pages 49205–49233, 2023. doi:10.52202/075280-2140.
[12] COIN-OR. Ipopt license, 2026. URL: https://coin-or.github.io/Ipopt/LICENSE.html
     [cited 2026-08-03].
[13] Shuvomoy Das Gupta. Research highlight: A tutorial on branch-and-bound performance
     estimation programming. INFORMS Computing Society Newsletter, pages 15–28, May 2025.
     URL: https://higherlogicdownload.s3.amazonaws.com/INFORMS/a4f852dd-2bdc-46b
     c-98e7-47e7d7c12752/UploadedImages/ICSNews_May2025.pdf.
[14] Shuvomoy Das Gupta, Bart P. G. Van Parys, and Ernest K. Ryu. Branch-and-bound perfor-
     mance estimation programming: A unified methodology for constructing optimal optimization
     methods. Mathematical Programming, 204(1–2):567–639, 2024. doi:10.1007/s10107-023-0
     1973-1.
[15] Alexandre d’Aspremont, Damien Scieur, and Adrien B. Taylor. Acceleration methods. Foun-
     dations and Trends® in Optimization, 5(1–2):1–245, 2021. doi:10.1561/2400000036.
[16] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In Automated Deduction – CADE 28, volume 12699 of Lecture Notes in Computer
     Science, pages 625–635. Springer, 2021. doi:10.1007/978-3-030-79876-5_37.
[17] Yoel Drori. The exact information-based complexity of smooth convex minimization. Journal
     of Complexity, 39:1–16, 2017. doi:10.1016/j.jco.2016.11.001.
[18] Yoel Drori and Adrien B. Taylor. On the oracle complexity of smooth strongly convex mini-
     mization. Journal of Complexity, 68:101590, 2022. doi:10.1016/j.jco.2021.101590.
[19] Yoel Drori and Marc Teboulle. Performance of first-order methods for smooth convex min-
     imization: A novel approach. Mathematical Programming, 145(1–2):451–482, 2014. doi:
     10.1007/s10107-013-0653-0.
[20] Alhussein Fawzi, Matej Balog, Aja Huang, Thomas Hubert, Bernardino Romera-Paredes,
     Mohammadamin Barekatain, Alexander Novikov, Francisco J. R. Ruiz, Julian Schrittwieser,
     Grzegorz Swirszcz, David Silver, Demis Hassabis, and Pushmeet Kohli. Discovering faster
     matrix multiplication algorithms with reinforcement learning. Nature, 610(7930):47–53, 2022.
     doi:10.1038/s41586-022-05172-4.
[21] Tony Feng, Trieu H. Trinh, Garrett Bingham, Dawsen Hwang, Yuri Chervonyi, Junehyuk
     Jung, Joonkyung Lee, Carlo Pagano, Sang-hyun Kim, Federico Pasqualotto, Sergei Gukov,
     Jonathan N. Lee, Junsu Kim, Kaiying Hou, Golnaz Ghiasi, Yi Tay, YaGuang Li, Chenkai
     Kuang, Yuan Liu, Hanzhao Lin, Evan Zheran Liu, Nigamaa Nayakanti, Xiaomeng Yang, Heng-
     Tze Cheng, Demis Hassabis, Koray Kavukcuoglu, Quoc V. Le, and Thang Luong. Towards
     autonomous mathematics research, 2026. arXiv:2602.10177.
[22] Baptiste Goujaud, Céline Moucer, François Glineur, Julien M. Hendrickx, Adrien B. Taylor,
     and Aymeric Dieuleveut. PEPit: computer-assisted worst-case analyses of first-order opti-
     mization methods in Python. Mathematical Programming Computation, 16(3):337–367, 2024.
     doi:10.1007/s12532-024-00259-7.



                                               38
[23] Benjamin Grimmer. Provably faster gradient descent via long steps. SIAM Journal on Opti-
     mization, 34(3):2588–2608, 2024. doi:10.1137/23M1588408.
[24] Gurobi Optimization, LLC. Gurobi academic licenses, 2026. URL: https://www.gurobi.com
     /academics [cited 2026-08-03].
[25] Gurobi Optimization, LLC. Gurobi Optimizer Reference Manual, version 13.0, 2026. URL:
     https://docs.gurobi.com/projects/optimizer/en/current/ [cited 2026-08-03].
[26] Roger A. Horn and Charles R. Johnson. Matrix Analysis. Cambridge University Press, 2nd
     edition, 2012. doi:10.1017/CBO9781139020411.
[27] Uijeong Jang, Shuvomoy Das Gupta, and Ernest K. Ryu. Computer-assisted design of ac-
     celerated composite optimization methods: OptISTA. Mathematical Programming, 2025.
     doi:10.1007/s10107-025-02258-5.
[28] John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ron-
     neberger, et al. Highly accurate protein structure prediction with AlphaFold. Nature,
     596(7873):583–589, 2021. doi:10.1038/s41586-021-03819-2.
[29] Phillip Kerger. Closing the oracle-complexity gap in derivative-free convex optimization: A
     near-quadratic lower bound from exact function values, 2026. arXiv:2607.13335.
[30] Donghwan Kim and Jeffrey A. Fessler. Optimized first-order methods for smooth convex
     minimization. Mathematical Programming, 159(1-2):81–107, 2016. doi:10.1007/s10107-015
     -0949-3.
[31] Donghwan Kim and Jeffrey A. Fessler. Optimizing the eﬀiciency of first-order methods for
     decreasing the gradient of smooth convex functions. Journal of Optimization Theory and
     Applications, 188(1):192–219, 2021. doi:10.1007/s10957-020-01770-2.
[32] Jaeyeon Kim, Asuman Ozdaglar, Chanwoo Park, and Ernest K. Ryu. Time-reversed dissipation
     induces duality between minimizing gradient norm and function value. Advances in Neural
     Information Processing Systems, 36:23389–23440, 2023. doi:10.52202/075280-1014.
[33] Jaeyeon Kim, Chanwoo Park, Asuman Ozdaglar, Jelena Diakonikolas, and Ernest K. Ryu.
     Mirror duality in convex optimization, 2023. arXiv:2311.17296.
[34] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The AI
     scientist: Towards fully automated open-ended scientific discovery, 2024. arXiv:2408.06292.
[35] Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foer-
     ster, David Ha, and Jeff Clune. Towards end-to-end automation of AI research. Nature,
     651(8107):914–919, 2026. doi:10.1038/s41586-026-10265-5.
[36] Miles Lubin, Oscar Dowson, Joaquim Dias Garcia, Joey Huchette, Benoît Legat, and
     Juan Pablo Vielma. JuMP 1.0: Recent improvements to a modeling language for math-
     ematical optimization. Mathematical Programming Computation, 15:581–589, 2023. doi:
     10.1007/s12532-023-00239-3.




                                              39
[37] Shiqian Ma. Convergence of BDRS as a matrix scaling algorithm. Optimization Online
     preprint, 2026. URL: https://optimization-online.org/2026/05/convergence-o
     f-bdrs-as-a-matrix-scaling-algorithm/.
[38] MOSEK ApS. MOSEK academic licenses, 2026. URL: https://www.mosek.com/products
     /academic-licenses/ [cited 2026-08-03].
[39] MOSEK ApS. The MOSEK optimizer API for Julia 11.2.2, 2026. URL: https://docs.mos
     ek.com/latest/juliaapi/index.html [cited 2026-08-03].
[40] Arkadi S. Nemirovsky. On optimality of Krylov’s information when solving linear operator
     equations. Journal of Complexity, 7(2):121–130, 1991. doi:10.1016/0885-064X(91)90001-E.
[41] Arkadi S. Nemirovsky. Information-based complexity of linear operator equations. Journal of
     Complexity, 8(2):153–175, 1992. doi:10.1016/0885-064X(92)90013-2.
[42] Arkadi S. Nemirovsky and David B. Yudin. Problem Complexity and Method Eﬀiciency in
     Optimization. Wiley, 1983.
[43] Yurii Nesterov. A method of solving a convex programming problem with convergence rate
     O(1/k 2 ). Soviet Mathematics Doklady, 27(2):372–376, 1983.
[44] Yurii Nesterov, Alexander Gasnikov, Sergey Guminov, and Pavel Dvurechensky. Primal-dual
     accelerated gradient methods with small-dimensional relaxation oracle. Optimization Methods
     and Software, 36(4):773–810, 2021. doi:10.1080/10556788.2020.1731747.
[45] Nous Research. Hermes Agent, 2026. URL: https://hermes-agent.nousresearch.com/
     [cited 2026-08-03].
[46] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang,
     Adam Zsolt Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas
     Mehrabian, M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies,
     Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. AlphaEvolve: A coding agent for
     scientific and algorithmic discovery, 2025. arXiv:2506.13131.
[47] OpenAI. Introducing ChatGPT Pro, 2024. URL: https://openai.com/index/introducing
     -chatgpt-pro/ [cited 2026-08-03].
[48] OpenAI. Build skills, 2026. URL: https://learn.chatgpt.com/docs/build-skills [cited
     2026-08-03].
[49] OpenAI. Codex CLI, 2026. URL: https://developers.openai.com/codex/cli [cited
     2026-08-03].
[50] OpenAI. GPT-5.6: Frontier intelligence that scales with your ambition, 2026. URL: https:
     //openai.com/index/gpt-5-6/ [cited 2026-08-03].
[51] OpenAI. Introducing GPT-5.5, 2026. URL: https://openai.com/index/introducing-gpt
     -5-5/ [cited 2026-08-03].
[52] OpenAI. Ten advances in mathematics and theoretical computer science, 2026. URL: https:
     //cdn.openai.com/pdf/ten-proofs-oai.pdf [cited 2026-08-03].



                                              40
[53] OpenClaw Foundation. OpenClaw docs, 2026. URL: https://docs.openclaw.ai/ [cited
     2026-08-03].
[54] OpenCode. OpenCode: The open source AI coding agent, 2026. URL: https://opencode.ai/
     [cited 2026-08-03].
[55] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming
     Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from
     program search with large language models. Nature, 625(7995):468–475, 2024. doi:10.1038/
     s41586-023-06924-6.
[56] Anne Rubbens and Julien M. Hendrickx. A constraint-based approach to function interpola-
     tion, with application to performance estimation for weakly convex optimization. Mathematical
     Programming, 2026. doi:10.1007/s10107-026-02353-1.
[57] Anne Rubbens, Julien M. Hendrickx, and Adrien B. Taylor. A constructive approach to
     strengthen algebraic descriptions of function and operator classes, 2025. arXiv:2504.14377.
[58] Jaewook J. Suh, Gyumin Roh, and Ernest K. Ryu. Continuous-time analysis of accelerated
     gradient methods via conservation laws in dilated coordinate systems. In Proceedings of the
     39th International Conference on Machine Learning, volume 162 of Proceedings of Machine
     Learning Research, pages 20640–20667. PMLR, 2022. URL: https://proceedings.mlr.pr
     ess/v162/suh22a.html.
[59] Jaewook J. Suh, TaeHo Yoon, Edward D. H. Nguyen, Bicheng Ying, and Shiqian Ma. Peppy:
     An AI-assisted workflow for tight convergence analysis of optimization algorithms. In ICML
     2026 Workshop AI4Research, 2026. Seoul, South Korea. URL: https://openreview.net/f
     orum?id=q7TfzOgGnb.
[60] Anja Surina, Arun Suggala, George Tsoukalas, Anton Kovsharov, Sergey Shirobokov, Francisco
     J. R. Ruiz, Pushmeet Kohli, and Swarat Chaudhuri. An improved last-iterate convergence rate
     for anchored gradient descent ascent, 2026. arXiv:2604.03782.
[61] Kyle Swanson, Wesley Wu, Nash L. Bulaong, John E. Pak, and James Zou. The Virtual
     Lab of AI agents designs new SARS-CoV-2 nanobodies. Nature, 646(8085):716–723, 2025.
     doi:10.1038/s41586-025-09442-9.
[62] Adrien B. Taylor and Yoel Drori. An optimal gradient method for smooth strongly convex
     minimization. Mathematical Programming, 199(1–2):557–594, 2023. doi:10.1007/s10107-0
     22-01839-y.
[63] Adrien B. Taylor, Julien M. Hendrickx, and François Glineur. Exact worst-case performance
     of first-order methods for composite convex optimization. SIAM Journal on Optimization,
     27(3):1283–1313, 2017. doi:10.1137/16M108104X.
[64] Adrien B. Taylor, Julien M. Hendrickx, and François Glineur. Performance estimation toolbox
     (PESTO): automated worst-case analysis of first-order optimization methods. In 2017 IEEE
     56th Annual Conference on Decision and Control (CDC), pages 1278–1283. IEEE, 2017. doi:
     10.1109/CDC.2017.8263832.



                                               41
[65] Adrien B. Taylor, Julien M. Hendrickx, and François Glineur. Smooth strongly convex interpo-
     lation and exact worst-case performance of first-order methods. Mathematical Programming,
     161(1–2):307–345, 2017. doi:10.1007/s10107-016-1009-3.
[66] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIG-
     PLAN International Conference on Certified Programs and Proofs, pages 367–381. Association
     for Computing Machinery, 2020. doi:10.1145/3372885.3373824.
[67] George Tsoukalas, Anton Kovsharov, Sergey Shirobokov, Anja Surina, Moritz Firsching,
     Gergely Bérczi, et al. Advancing mathematics research with AI-driven formal proof search,
     2026. arXiv:2605.22763.
[68] Manu Upadhyaya, Daniel Berg Thomsen, Aymeric Dieuleveut, and Adrien B. Taylor. An
     optimal first-order method for smooth and strongly convex composite optimization and its
     stationary limit, 2026. arXiv:2605.22929.
[69] Andreas Wächter and Lorenz T. Biegler. On the implementation of an interior-point fil-
     ter line-search algorithm for large-scale nonlinear programming. Mathematical Programming,
     106(1):25–57, 2006. doi:10.1007/s10107-004-0559-y.
[70] Michel Waldschmidt. Elliptic functions and transcendence. In Krishnaswami Alladi, edi-
     tor, Surveys in Number Theory, volume 17 of Developments in Mathematics, pages 143–188.
     Springer, New York, 2008. doi:10.1007/978-0-387-78510-3_7.
[71] TaeHo Yoon and Benjamin Grimmer. A theory of composition and duality of extremal optimal
     fixed-point algorithms, 2026. arXiv:2605.02231.
[72] TaeHo Yoon, Jaeyeon Kim, Jaewook J. Suh, and Ernest K. Ryu. Optimal acceleration for
     minimax and fixed-point problems is not unique. In Proceedings of the 41st International
     Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research,
     pages 57244–57314. PMLR, 2024. URL: https://proceedings.mlr.press/v235/yoon24b.h
     tml.
[73] TaeHo Yoon, Ernest K. Ryu, and Benjamin Grimmer. H-invariance theory: A complete
     characterization of minimax optimal fixed-point algorithms, 2025. arXiv:2511.14915.
[74] Max Zimmer, Nico Pelleriti, Christophe Roux, and Sebastian Pokutta. The agentic researcher:
     A practical guide to AI-assisted research in mathematics and machine learning, 2026. arXiv:
     2603.15914.


A    Deferred proofs and details for lemniscate acceleration
A.1 Existence and uniqueness of the lemniscate recurrence
In this section we prove Lemma 1, establish the bounds on ΩN used in Theorem 1, and give a
complete bisection rule for computing ΩN .

The one-step map.    For Ω > 0 and ρ ∈ (0, 1], a pair of consecutive terms of (9) solves
                                                           
                                    Ω (ρ − t)2 = ρ 1 − t2                                   (23)


                                               42
in the unknown t, which rearranges to the quadratic equation (Ω + ρ) t2 − 2Ωρ t + Ωρ2 − ρ = 0. We
work on the admissible set A ≜ {(Ω, ρ) : Ω > 0, 0 < ρ ≤ 1, Ωρ ≥ 1}.
Lemma 7 (One-step map). For (Ω, ρ) ∈ A, equation (23) has exactly one solution t with 0 ≤ t < ρ,
namely                                          p
                                          Ωρ − ρ2 + Ωρ(1 − ρ2 )
                                 FΩ (ρ) ≜                           ,                          (24)
                                                    Ω+ρ
and the other solution is greater than or equal to ρ, with equality only when ρ = 1. Moreover:
  1. FΩ (ρ) = 0 if and only if Ωρ = 1;
  2. F is continuous on A and strictly increasing in each of Ω and ρ on the fibers of A (the other
     variable being fixed).

Proof. The quarter-discriminant of the quadratic equals Ω2 ρ2 −(Ω+ρ)(Ωρ2 −ρ) = ρ2 +Ωρ(1−ρ2 ) >
0, so (23) has the two real solutions
                                            p
                                        Ωρ ± ρ2 + Ωρ(1 − ρ2 )
                                   t± =                         .
                                                Ω+ρ
Since Ωρ(1 − ρ2 ) ≥ 0, the square root is at least ρ, hence
                                           Ωρ + ρ   Ωρ + ρ2
                                    t+ ≥          ≥         = ρ,
                                           Ω+ρ       Ω+ρ
and both inequalities hold with equality only when ρ = 1. On the other hand, t− < Ωρ/(Ω+ρ) < ρ.
The product of the two solutions is t+ t− = ρ(Ωρ − 1)/(Ω + ρ) ≥ 0 on A; since t+ ≥ ρ > 0, this
gives t− ≥ 0, with t− = 0 exactly when Ωρ = 1. Therefore FΩ (ρ) = t− is the unique solution in
[0, ρ), which proves the root dichotomy and claim 1.
For claim 2, continuity follows from (24) because the denominator is positive. For the strict
monotonicity, define
                               ψ(Ω, ρ, t) ≜ Ω(ρ − t)2 − ρ(1 − t2 ),
and fix a point in the interior of A with t = FΩ (ρ) ∈ [0, ρ). Substituting the root identity 1 − t2 =
Ω(ρ − t)2 /ρ into the partial derivatives of ψ and using 0 ≤ t < ρ ≤ 1, tedious but straightforward
algebra gives ψΩ > 0, ψρ > 0, and ψt < 0 at this point. By the implicit function theorem,
F is continuously differentiable in the interior of A with ∂F/∂Ω = −ψΩ /ψt > 0 and ∂F/∂ρ =
−ψρ /ψt > 0. Consequently, for fixed ρ ∈ (0, 1) the map Ω 7→ FΩ (ρ) is continuous on [1/ρ, ∞) and
strictly increasing on its interior, hence strictly increasing on [1/ρ, ∞); the same argument applies
to ρ 7→ FΩ (ρ) on [1/Ω, 1] for fixed Ω > 1; and on the remaining boundary segment ρ = 1 the
explicit formula FΩ (1) = (Ω − 1)/(Ω + 1) is strictly increasing in Ω.

Shooting orbits. For Ω ≥ 1 define the shooting iterates Φ0 (Ω) ≜ 1 and Φk+1 (Ω) ≜ FΩ (Φk (Ω))
defined for as long as (Ω, Φk (Ω)) ∈ A. Taking the positive square root in (23) gives the step identity
                                             r
                                                Φk (Ω) (1 − Φk+1 (Ω)2 )     1
                         Φk (Ω) − Φk+1 (Ω) =                            ≤√                         (25)
                                                           Ω                 Ω
whenever the left-hand side is defined; the final bound holds because
                                                                     the iterates satisfy 0 ≤
Φk+1 (Ω) < Φk (Ω) ≤ Φ0 (Ω) = 1 (Lemma 7), so Φk (Ω) 1 − Φk+1 (Ω)2 ≤ 1.

                                                  43
Proof of Lemma 1. Call a pair (Ω, {ρk }N  +1
                                        k=0 ) admissible for horizon N if it satisfies all requirements
of the lemma: 1 = ρ0 > ρ1 > · · · > ρN +1 = 0 and (9) for 0 ≤ k ≤ N .
Step 0: every admissible pair is a shooting orbit. Let (Ω, {ρk }) be admissible for horizon N . Strict
decrease gives ρk > ρN +1 = 0 for k ≤ N . The recurrence at k = N reads Ωρ2N = ρN , so ρN = 1/Ω,
and the decrease of the sequence gives Ωρk ≥ ΩρN = 1 for k ≤ N ; hence (Ω, ρk ) ∈ A for 0 ≤ k ≤ N .
In particular 1/Ω = ρN ≤ ρ0 = 1 forces Ω ≥ 1, and for N ≥ 1 the strict inequality ρN < ρ0 forces
Ω > 1. Finally, for 0 ≤ k ≤ N the term ρk+1 solves (23) with 0 ≤ ρk+1 < ρk , so Lemma 7 gives
ρk+1 = FΩ (ρk ). Therefore ρk = Φk (Ω) for all 0 ≤ k ≤ N + 1: the sequence is uniquely determined
by Ω, which is the final claim of the lemma.
Step 1: existence,
                  by induction on the horizon. We construct numbers 1 = Ω0 < Ω1 < Ω2 < · · ·
such that ΩN , {Φk (ΩN )}k=0 is admissible for horizon N . For N = 0 the requirements reduce to
                          N +1

Ω(ρ0 − ρ1 )2 = ρ0 (1 − ρ21 ) with ρ0 = 1 and ρ1 = 0, that is, Ω0 = 1; and indeed Φ1 (1) = F1 (1) = 0.
For the induction step, assume (ΩN , {Φk (ΩN )}) is admissible for horizon N . We first record, by
induction on k ∈ {1, . . . , N + 1}, that the maps Ω 7→ Φk (Ω) are well defined, continuous, and
strictly increasing on the ray [ΩN , ∞). For k = 1, Φ1 (Ω) = FΩ (1) = (Ω − 1)/(Ω + 1) has all three
properties. For the step from k to k + 1 (with k ≤ N ), the monotonicity of F and admissibility
at horizon N give the domain bound Ω Φk (Ω) ≥ ΩN Φk (ΩN ) ≥ ΩN ΦN (ΩN ) = ΩN /ΩN = 1, so
(Ω, Φk (Ω)) ∈ A and Φk+1 (Ω) = FΩ (Φk (Ω)) is well defined; it is continuous by Lemma 7 and
the induction hypothesis, and strictly increasing because, for ΩN ≤ Ω < Ω′ , we have Φk+1 (Ω) =
FΩ (Φk (Ω)) < FΩ′ (Φk (Ω)) < FΩ′ (Φk (Ω′ )) = Φk+1 (Ω′ ), with the middle application being legitimate
since Ω′ Φk (Ω) > Ω Φk (Ω) ≥ 1, and the second inequality being strict by the induction hypothesis
Φk (Ω) < Φk (Ω′ ).
Now consider h(Ω) ≜ Ω ΦN +1 (Ω) on [ΩN , ∞). It is continuous, and it is strictly increasing because
ΦN +1 is nonnegative and strictly increasing there: for ΩN ≤ Ω < Ω′ , Ω ΦN +1 (Ω) ≤ Ω ΦN +1 (Ω′ ) <
Ω′ ΦN +1 (Ω′ ). Moreover h(ΩN ) = ΩN · ΦN +1 (ΩN ) = 0, and telescoping
                                                                √           (25) over 0 ≤ k √
                                                                                            ≤ N , all
iterates being defined on this ray, gives ΦN +1 (Ω) ≥ 1−(N +1)/ Ω, so h(Ω) ≥ Ω−(N +1) Ω → ∞
as Ω → ∞. By the intermediate value theorem there is a unique ΩN +1 ∈ (ΩN , ∞) with h(ΩN +1 ) =
1, that is, ΦN +1 (ΩN +1 ) = 1/ΩN +1 . The sequence ρk ≜ Φk (ΩN +1 ) for 0 ≤ k ≤ N + 1, extended by
ρN +2 ≜ 0, is then admissible for horizon N +1: the recurrence holds for 0 ≤ k ≤ N by construction,
and at k = N + 1 it reads ΩN +1 (ρN +1 − 0)2 = 1/ΩN +1 = ρN +1 (1 − 02 ); the sequence is strictly
decreasing because FΩ (ρ) < ρ at every step and ρN +1 = 1/ΩN +1 > 0 = ρN +2 ; and it is nonnegative
because ρk ≥ ρN +1 > 0 for k ≤ N + 1. This completes the induction, so an admissible Ω exists for
every horizon.
Step 2: uniqueness of Ω. Suppose (Ω, {ρk }) and (Ω′ , {ρ′k }) are both admissible for horizon N
with Ω < Ω′ . By Step 0, both sequences are shooting orbits, every pair (Ω, ρk ) and (Ω′ , ρ′k ) with
k ≤ N lies in A, and Ω, Ω′ ≥ 1. For N = 0, Step 0 gives ρ1 = (Ω − 1)/(Ω + 1) = 0 and
ρ′1 = (Ω′ − 1)/(Ω′ + 1) = 0, forcing Ω = Ω′ = 1 and contradicting Ω < Ω′ ; so assume N ≥ 1. We
prove ρk < ρ′k for 1 ≤ k ≤ N + 1 by induction. For k = 1,
                                            Ω−1  Ω′ − 1
                                     ρ1 =       < ′     = ρ′1 .
                                            Ω+1  Ω +1
For the induction step, the strict monotonicity of F in both arguments (Lemma 7) gives ρk+1 =
FΩ (ρk ) < FΩ′ (ρk ) < FΩ′ (ρ′k ) = ρ′k+1 , where the middle steps are valid because Ω′ ρk > Ωρk ≥ 1,

                                                  44
and the second inequality is strict by the induction hypothesis ρk < ρ′k . Iterating the induction
through the final step k = N yields ρN +1 < ρ′N +1 , contradicting ρN +1 = ρ′N +1 = 0. Hence the
admissible Ω is unique, and Step 0 shows the sequence is uniquely determined by it.

The same machinery yields the quantitative bounds on ΩN quoted in Theorem 1 and a complete
bisection rule for computing ΩN .
Corollary 2 (Bounds on ΩN and bisection correctness). Let N ≥ 1, and let ΩN and {ρk }N +1
                                                                                     k=0 be
as in Lemma 1. Then:
     (N + 1)2
  1.            < ΩN < (N + 1)2 , where ϖ is the lemniscate constant defined in Theorem 1;
         ϖ2
     moreover 1 = Ω0 < Ω1 < Ω2 < · · · .
  2. Fix Ω ≥ 1 and generate the shooting iterates Φ0 (Ω), Φ1 (Ω), . . ., computing Φk+1 (Ω) =
     FΩ (Φk (Ω)) whenever Φk (Ω) ≥ 1/Ω. If Ω > ΩN , then Φk (Ω) > 1/Ω for all 0 ≤ k ≤ N
     and ΦN +1 (Ω) > 0. If Ω < ΩN , then there is an index k ≤ N with Φk (Ω) < 1/Ω. If Ω = ΩN ,
     the iterates realize the sequence of Lemma 1.
     Consequently, the following exact bisection is correct. Initialize [Ωl , Ωr ] = [1, (N +1)2 ]. Given
     the midpoint Ωm = (Ωl +Ωr )/2, generate the shooting iterates until either some k ≤ N satisfies
     Φk (Ωm ) < 1/Ωm , in which case set Ωl ← Ωm , or the iterates have been generated through
     ΦN +1 (Ωm ). In the latter case, set Ωr ← Ωm if ΦN +1 (Ωm ) > 0, and return Ωm = ΩN and the
     generated sequence if ΦN +1 (Ωm ) = 0. At every nonterminal step the invariant Ωl < ΩN ≤ Ωr
     is maintained, the bracket length is halved, and the midpoints converge to ΩN .

Proof. Part 1. At Ω = ΩN the step identity (25) holds for 0 ≤ k ≤ N , and telescoping gives
                                             s              
                                         XN
                                               ρk 1 − ρ2k+1     N +1
                       1 = ρ0 − ρN +1 =                       ≤ √      ,
                                                    ΩN            ΩN
                                         k=0
                                                                    √
and the term k = 1, present since N ≥ 1, is strictly smaller than 1/q ΩN because ρ1 < 1; hence
√
  ΩN < N + 1. For the lower bound, dividing the step identity by ρk (1 − ρ2k+1 ) and summing
gives
                           N Z ρk                                   N Z ρk                      Z 1
N +1 X                    X                                         X
        N
             ρk − ρk+1                             dt                              dt                     dt
√    =     q           =           q                          <              p            =         p            = ϖ,
  ΩN   k=0  ρ 1−ρk
                     2
                          k=0 ρ k+1  ρ         k   1 − ρ2k+1        k=0   ρk+1  t (1 − t2 )      0     t (1 − t2 )
                         k+1

where the strict inequality holds because on the interior of each interval the integrand on the right
strictly dominates the constant integrand                                             2
                                         R 1 on the
                                                √ left, and the substitution t = s identifies     the
comparison integral with the form ϖ = 2 0 ds/ 1 − s of Section 4.1.3. Hence ΩN > (N +1) /ϖ2 .
                                                       4                                       2

Strict monotonicity of N 7→ ΩN was established in Step 1 of the proof of Lemma 1 and is inherited
by the unique admissible values.
Part 2. If Ω > ΩN , the sub-induction in Step 1 (anchored at ΩN ) shows that Φk (Ω) is defined and
strictly increasing in Ω for 1 ≤ k ≤ N + 1; therefore, for 0 ≤ k ≤ N , using that the iterates decrease
in the index (FΩ (ρ) < ρ),
                                                                 1  1
                               Φk (Ω) ≥ ΦN (Ω) > ΦN (ΩN ) =        > ,
                                                                ΩN  Ω

                                                   45
and ΦN +1 (Ω) > ΦN +1 (ΩN ) = 0. If 1 ≤ Ω < ΩN , suppose toward a contradiction that Φk (Ω) ≥ 1/Ω
for all 0 ≤ k ≤ N ; then all iterates up to ΦN (Ω) are defined. The comparison induction of Step
2 does not use admissibility of the lower orbit at the terminal index: it only needs both shooting
orbits to be defined up to the index being compared, the domain of each step being guaranteed here
by the contradiction hypothesis and by ΩN Φk (Ω) > Ω Φk (Ω) ≥ 1. The same induction therefore
gives ΦN (Ω) < ΦN (ΩN ) = 1/ΩN < 1/Ω, a contradiction. The case Ω = ΩN is Lemma 1 itself.
For the bisection, Part 1 gives Ωl = 1 < ΩN < (N + 1)2 = Ωr at initialization. The sign charac-
terization just proved says that the left update occurs exactly when Ωm < ΩN , the right update
occurs exactly when Ωm > ΩN , and the remaining exact case is Ωm = ΩN , where Lemma 1 gives
ΦN +1 (Ωm ) = 0. Hence each nonterminal update preserves Ωl < ΩN ≤ Ωr while halving the bracket,
and the midpoints converge to ΩN .



The comparison with the integral in Part 1 in fact identifies the limit of ΩN /(N + 1)2 : the lower
bound of Corollary 2 is asymptotically tight.
Lemma 8. Let ΩN be as in Lemma 1. Then
                                               ΩN        1
                                         lim         2
                                                       = 2.
                                        N →∞ (N + 1)    ϖ

Proof. Write {ρk }N
                  k=0 for the sequence of Lemma 1 at ΩN , put ℓk ≜ ρk − ρk+1 > 0, and set
                    +1


                                             1
                                  g(x) ≜ p            ,     0 < x < 1,
                                          x (1 − x2 )
                                R1
so that the improper integral   0 g(x) dx = ϖ, as recorded in the proof of Corollary 2. As in Part
                                                                q
1 of that proof, dividing the step identity (25) at Ω = ΩN by ρk (1 − ρ2k+1 ) and summing over
0 ≤ k ≤ N gives
                                     N +1 X
                                               N
                                                           ℓk
                                     √    =     q                    .                            (26)
                                       ΩN
                                                        k 1 − ρk+1
                                                 ρ             2
                                            k=0
                                                                                     √
We claim that the right-hand side converges to ϖ; the lemma follows, since then          ΩN /(N + 1) →
1/ϖ.
The intervals [ρk+1 , ρk ], 0 ≤ k ≤ N , partition [0, 1], and by
                                                              √ the step identity and the lower bound of
Corollary 2 their lengths satisfy δN ≜ max0≤k≤N ℓk ≤ 1/ ΩN < ϖ/(N +1), so the mesh       q δN tends to
zero. For x ∈ [ρk+1 , ρk ]∩(0, 1) we have x ≤ ρk and 1−x2 ≤ 1−ρ2k+1 , hence g(x) ≥ 1/ ρk (1 − ρ2k+1 ),
                                                                    R1
so the right-hand side of (26) is a lower Riemann-type sum for 0 g(x) dx = ϖ.
                                             R ρk
In particular, each summand is at most ρk+1        g(x) dx, so the sum is at most ϖ for every N . For
the matching lower bound, fix ε ∈ (0, 1/4]. On (0, ε] we have 1 − x2 ≥ 3/4, and on [1 − ε, 1) we
have x ≥ 1/2 and 1 − x2 ≥ 1 − x, so the endpoint tails satisfy
                       Z ε                                 Z 1             √ √
                                       4 √
                           g(x) dx ≤ √ ε          and           g(x) dx ≤ 2 2 ε.
                        0               3                   1−ε


                                                   46
                            p [ρk+1 , ρk ] that meets [ε, 1 − ε] lies in [ε/2, 1 − ε/2], where the two-
Once δN < ε/2, every interval
variable kernel (x, y) 7→ 1/ x(1 − y 2 ) is quniformly continuous, with modulus of continuity ωε ;
since g(x) is this kernel at (x, x), we get 1/ ρk (1 − ρ2k+1 ) ≥ g(x) − ωε (δN ) for every x ∈ [ρk+1 , ρk ].
Discarding the remaining (positive) summands and summing over the intervals that meet [ε, 1 − ε],
whose union covers [ε, 1 − ε] and has total length at most 1,

         X                            Z 1−ε                                        
         N
                     ℓk                                                       4  √ √
               q             ≥               g(x) dx − ωε (δN ) ≥ ϖ −       √ +2 2   ε − ωε (δN ).
         k=0    ρk 1 − ρ2k+1           ε                                       3

Letting N → ∞ and then ε ↓ 0 shows that the sum converges to ϖ.
              √
Hence (N + 1)/ ΩN → ϖ.

A.2 Equivalence of the two forms of (LemniAcc)
Throughout this subsection, set ϕk ≜ (1 + ρ2k )/(2ρk ) for 0 ≤ k ≤ N , ∆k ≜ ϕk+1 − ϕk for 0 ≤ k ≤
N − 1, and ψk ≜ (1 + ρ2k )/(1 − ρ2k ) for 1 ≤ k ≤ N + 1 so that the update of xk+1 in (LemniAcc) reads
                                                                         (init) = Ω ∆ ∆        (mom)
xk+1 = x+k + (ψk+1 − ψk+2 ) zk+1 and the     coeﬀicients of (8) read α           N 0 N −1 , αk     =
                          (corr)
∆N −k−1 /∆N −k , and αk            = ∆N −k−1 ΩN ∆k − ∆N1−k . Since 1 = ρ0 > ρ1 > · · · > ρN > 0 and
the map ρ 7→ (1 + ρ2 )/(2ρ) is strictly decreasing on (0, 1], we have ∆k > 0 for 0 ≤ k ≤ N − 1.
Lemma 9. Fix N ≥ 1, and let ΩN and ρ0 , . . . , ρN +1 be as in Lemma 1. From any starting point
x0 ∈ R d , the iterates x0 , x1 , . . . , xN of (LemniAcc) coincide with those of the momentum form (8).

Proof. First, we claim that
                                        ψk = ϕN +1−k ,    1 ≤ k ≤ N + 1.                               (27)
Indeed, for 0 < ρ < 1, the map T (ρ) = (1 − ρ)/(1 + ρ) satisfies

                                   1 + T (ρ)2   (1 + ρ)2 + (1 − ρ)2   1 + ρ2
                                              =                     =        ,
                                     2T (ρ)       2(1 + ρ)(1 − ρ)     1 − ρ2

and combining this identity at ρ = ρk , which lies in (0, 1) for 1 ≤ k ≤ N , with the relation
ρN +1−k = T (ρk ) recorded after Lemma 1 in Section 4.1 gives ϕN +1−k = ψk for 1 ≤ k ≤ N . At the
endpoint k = N + 1, where ρN +1 = 0 and ρ0 = 1, direct evaluation gives ψN +1 = 1 = ϕ0 , which
completes (27). By (27), ψk+1 − ψk+2 = ϕN −k − ϕN −k−1 = ∆N −k−1 for 0 ≤ k ≤ N − 1, so the
x-update of (LemniAcc) is

                               xk+1 = x+
                                       k + ∆N −k−1 zk+1 ,       0 ≤ k ≤ N − 1.                         (28)

We now argue by induction that the two forms generate the same iterates. They start from the
same x0 , and whenever the iterates agree up to index k, both forms evaluate the gradient at the
                             j for 0 ≤ j ≤ k agree as well.
same points, so the vectors x+

At k = 0: since   z0 = 0 and −∇f (x0 )/L    0 − x0 , the z-update
                                          = x+                  of+ (LemniAcc)
                                                                         (init)
                                                                                   gives z1 =
ΩN ∆0 x0 − x0 , and (28) yields x1 = x0 + ΩN ∆0 ∆N −1 x0 − x0 = x0 + α
         +                              +                +
                                                                                x0 − x0 , the
                                                                                 +

first update of (8).

                                                         47
                                                                                             
For 1 ≤ k ≤ N −1: solving (28) at index k−1 for the auxiliary variable gives zk = xk − x+      /∆N −k ,
                                                                                        k−1
and the z-update gives zk+1 = zk + ΩN ∆k xk − xk . Substituting both into (28) and writing
                                                +

      k−1 = xk − xk−1 − xk − xk , we get
xk − x+       +     +         +

                                                                            
                        ∆N −k−1 +                                       1             
                   +
          xk+1 = xk +              xk − xk−1 + ∆N −k−1 ΩN ∆k −
                                         +
                                                                                x+
                                                                                 k − xk ,
                         ∆N −k                                        ∆N −k
                                                          (mom)        (corr)
which is the k-th update of (8) with the coeﬀicients αk           and αk        above. By induction, the
two forms produce the same iterates x0 , x1 , . . . , xN .

A.3 Computer-assisted algorithm design by PEP
PEP formulation of the problem. This subsection presents, lightly edited for presentation, the
Stage-1 derivation that bnb-pep-skill wrote for the design problem behind (LemniAcc). The skill
instantiates the Stage 1 design problem of Section 3.1 for problem (7), in the notation of Section 4:
the function class is F = F0,L , the performance measure is E = k∇f (xN )k2 , the initial condition
is C = kx0 − x⋆ k2 − R2 ≤ 0 for a given R > 0, and the method class is the class MN of fixed-step
first-order methods (FSFOMs) with N steps. Applied to f ∈ F0,L from a starting point x0 ∈ R d ,
an FSFOM produces its iterates with

                                                  1X
                                                    i−1
                                    xi = xi−1 −      hi,j ∇f (xj )
                                                  L
                                                    j=0

for 1 ≤ i ≤ N , where, relative to the generic form displayed in Section 3.1, the stepsizes hi,j are
normalized by L. We can equivalently express the FSFOM as

                                               1X
                                                  i−1
                                     xi = x0 −    αi,j ∇f (xj ),
                                               L
                                                  j=0

               Pi
where αi,j ≜      k=j+1 hk,j for 0 ≤ j < i ≤ N ; this triangular relationship between h and α is
invertible, so we can compute h given α and vice versa. The stepsizes h or α may depend on F0,L
and the value of N , but are otherwise predetermined.
Instantiated with these choices, the worst-case performance R(M ) of a method M ∈ MN in (1)
becomes
                                                                              
                      maximize k∇f (xN )k2
                    subject to                                                
                                                                              
                    f ∈ F0,L ,                                                
                                                                              
          R (M ) =  x⋆ is an optimal solution to (7) satisfying ∇f (x⋆ ) = 0, 
                   
                                                                               ,  (Oinner )
                    {xi }1≤i≤N is generated by M with initial point x0 ,      
                                                                              
                    kx − x k2 ≤ R2 ,                                          
                          0    ⋆
                       x⋆ = 0, f (x⋆ ) = 0

where f , x0 , . . . , xN , and x⋆ are the decision variables. We set x⋆ = 0 and f (x⋆ ) = 0 without any
loss of generality because the function class F0,L is closed and invariant under shifting variables
and function values.

                                                  48
                       ⋆ ∈ M
                             N for this setup solves the outer design problem R (MN ) =
The optimal FSFOM MN                                                           ⋆

minM ∈MN R(M ) of (1).
Following the BnB-PEP reformulation outlined in Section 3.1, the derivation reduces this design
problem to a finite-dimensional nonconvex QCQP in two steps: it first formulates the inner problem
(Oinner ) as a finite-dimensional convex SDP, and then optimizes the stepsizes against its dual [14].
As the first step, the derivation formulates the inner problem (Oinner ) as a finite-dimensional con-
vex SDP using the smooth-convex interpolation result of [65, Corollary 1]. This result exactly
characterizes the sampled function values and gradients that arise from a function in F0,L .
In other words, we impose the smooth-convex interpolation inequalities at the sampled points xi ,
i ∈ IN⋆ , using (6), with the notation g ≜ ∇f (x ) and f ≜ f (x ). This finite representation is
                                         i         i        i         i
lossless by [65, Corollary 1]. Thus, the derivation casts (Oinner ) as the following finite-dimensional
but nonconvex problem:

                                                                                                    
                    maximize            kgN k2
                   subject to          fi ≥ fj + hgj , xi − xj i + 2L 1
                                                                         kgi − gj k2 ,             ⋆, 
                                                                                           i, j ∈ IN
                                                                                                     
                                                                                                     
                                       g⋆ = 0,
                                                     P                                                
          R(M ) =                                                                                    ,    (29)
                                       xi = x0 − L1 i−1 j=0 αi,j gj ,   1 ≤ i ≤ N,                   
                                                                                                     
                                       kx0 − x⋆ k2 ≤ R2 ,                                            
                                        x⋆ = 0, f⋆ = 0

where the decision variables are {xi , gi , fi }i∈IN⋆ ⊆ R d × R d × R.

Next, (29) is formulated as a convex SDP. Let P ≜ [x0 | g0 | g1 | . . . | gN ] ∈ R d×(N +2) , G ≜ P ⊤ P ∈
S+
 N +2
      , and F ≜ [f0 | f1 | . . . | fN ] ∈ R 1×(N +1) . Note that rank G ≤ d. Define the following notation
for selecting columns and elements of P and F :

          g⋆ = 0 ∈ R N +2 , gi = ei+2 ∈ R N +2 ,              0 ≤ i ≤ N,
                                                                       1X
                                                                          i−1
          x0 = e1 ∈ R N +2 , x⋆ = 0 ∈ R N +2 , xi = x0 −                  αi,j gj ∈ R N +2 ,   1 ≤ i ≤ N,
                                                                       L
                                                                          j=0

          f⋆ = 0 ∈ R   N +1
                              , fi = ei+1 ∈ R   N +1
                                                       ,     0 ≤ i ≤ N.

This notation is defined so that xi = P xi , gi = P gi , fi = F fi for i ∈ IN
                                                                            ⋆ . Note that x depends on
                                                                                           i
{αi,j }0≤j≤i−1 linearly for 1 ≤ i ≤ N . For i, j ∈ IN , now define
                                                    ⋆


                                   Ai,j (α) = gj           (xi − xj ) ∈ S N +2 ,
                                   Bi,j (α) = (xi − xj )            (xi − xj ) ∈ S+
                                                                                  N +2
                                                                                       ,                    (30)
                                   Ci,j = (gi − gj )          (gi − gj ) ∈ S+
                                                                            N +2
                                                                                 .

Note that Ai,j (α) is aﬀine and Bi,j (α) is quadratic as functions of {αi,j }0≤j<i≤N . Under this
notation, hgj , xi − xj i = trGAi,j (α), kx0 − x⋆ k2 = trGB0,⋆ , and kgi − gj k2 = trGCi,j for i, j ∈ IN
                                                                                                       ⋆.

In these terms, (29) becomes a maximization over F and G = P ⊤ P , at the price of the rank
constraint rank G ≤ d: the equivalence relies on the fact that any G ∈ S+        N +2
                                                                                      with rank G ≤ d

                                                               49
factors as G = P ⊤ P with P ∈ R d×(N +2) ; see [65, §3.2]. The rank constraint is removed with the
following large-scale assumption.
Assumption 1. We have d ≥ N + 2.
Under this assumption, the constraint rank G ≤ d becomes vacuous, since G ∈ S+         N +2
                                                                                            . The bnb-
pep-skill derivation drops the rank constraint and formulates (O inner ) as a convex SDP
                                                                                                  
               maximize trG (CN,⋆ )
             subject to                                                                           
                               h                i                                                 
                                                                                                  
 R(M ) =  F (fj − fi ) + trG Ai,j (α) + 2L1
                                             Ci,j ≤ 0, i, j ∈ IN
                                                               ⋆ : i 6= j,    ▷ dual var. λi,j ≥ 0  ,
                                                                                                  
             −G  0, ▷ dual var. Z  0                                                            
               trGB0,⋆ ≤ R , ▷ dual var. ν ≥ 0
                            2

                                                                                                   (31)

where F ∈ R N +1 , G ∈ S N +2 are the decision variables. We denote the corresponding dual variables
on the right-hand side of the constraints for later use. Note that (31) is free from problem dimension
d.
Next the bnb-pep-skill derivation uses convex duality to formulate the SDP (31) in the previous
step, originally a maximization problem, as a minimization problem. Taking the dual of (31) gives
                                                                                  
                          minimize νR2
                        subject to                                                
                        P                                                         
                                 ⋆ :i̸=j λi,j (fj − fi ) = 0,
                                                                                   
                            i,j∈IN
                                                P                                
               R(M ) =                                                            ,        (32)
                        νB0,⋆ − CN,⋆ + i,j∈I ⋆ :i̸=j λi,j Ai,j (α) + 2L
                                                                       1
                                                                         Ci,j = Z, 
                                                       N                          
                        Z  0,                                                    
                          ν ≥ 0, λi,j ≥ 0, i, j ∈ IN       ⋆ : i 6= j


where ν ∈ R, λ = {λi,j }i,j∈IN⋆ :i̸=j , and Z ∈ S+
                                                 N +2
                                                      are the decision variables. We call λ, ν, and Z the
inner-dual variables. By weak duality of convex SDPs, we have R(M ) ≤ R(M ).
In convex SDPs, strong duality holds often but not always. For the sake of simplicity, we will
assume strong duality holds in our setup.
Assumption 2. Strong duality holds between (31) and (32), i.e., R(M ) = R(M ).
As the second step, with the inner problem (Oinner ) replaced by its dual minimization (32), the
outer design problem becomes a joint minimization over the stepsizes {αi,j }0≤j<i≤N and the inner-
dual variables. This joint problem is nonconvex, and, following [14], the derivation formulates it as
a QCQP by replacing the semidefinite constraint Z  0 with the Cholesky factorization Z = V V ⊤ ,
where V is lower triangular with nonnegative diagonals [26, Corollary 7.2.9]. The problem of finding




                                                   50
the optimal FSFOM then takes the QCQP form
                                                                                  
                         minimize νR2
                        subject to                                                
                        P                                                         
                               ⋆ :i̸=j λi,j (fj − fi ) = 0,
                                                                                   
                          i,j∈IN
                                              P                                  
                                                                                  
            R⋆ (MN ) =  νB0,⋆ − CN,⋆ + i,j∈I ⋆ :i̸=j λi,j Ai,j (α) + 2L
                                                                       1
                                                                         Ci,j = Z,  ,             (33)
                                                     N                            
                        V is lower triangular with nonnegative diagonals,         
                                                                                  
                        Z = V V ⊤,                                                
                         ν ≥ 0, λi,j ≥ 0, i, j ∈ IN : i 6= j
                                                         ⋆


where λ = {λi,j }i,j∈IN⋆ :i̸=j , ν, Z, V , {αi,j }0≤j<i≤N are the decision variables.
Upon user approval of the derivation above, bnb-pep-skill solves (33) numerically; the resultant
optimal α⋆ gives the optimal stepsizes h⋆ for any large-scale setup d ≥ N + 2. By the scale
invariance discussed in [65, §3.5], it suﬀices to solve the QCQP for L = 1 and R = 1: for any other
L > 0 and R > 0 the optimal stepsizes are unchanged, and the optimal worst-case value scales by
the factor L2 R2 .
In Stage 2 of the pipeline, the frontier-llm-consult skill fitted symbolic expressions to the numer-
ical solutions of (33), yielding an analytic parametrization of the numerically optimal stepsizes
in the design variables α, equivalently h, together with an analytic feasible point of the inner
dual (32), whose feasibility already certifies the worst-case bound by weak duality. From this
stepsize parametrization, the consultation then recast the method into the memory-eﬀicient form
(LemniAcc) presented in Section 4.1. In continued consultation, Stage 2 converted the multipliers
of this feasible point into the Lyapunov proof of Theorem 1 given in Section 4.1.1, the form in
which this paper presents the convergence analysis; the Lean coverage of the presented results is
described in Section 4.1.5.

A.4 Details for continuous-time analysis of lemniscate ODE
In this section, we develop a leading-order continuous-time model of the lemniscate acceleration
algorithm and prove Theorem 2. For an Lf -smooth objective with Lf > 0, we apply the method
with the algorithmic smoothness upper bound L  b N = N 2 /T 2 and use the iterate grid t = kT /N .
                                         b
At fixed Lf and T , the condition Lf ≤ LN holds for all suﬀiciently large N . We retain only the
leading-order terms as N → ∞.
Recall the continuous-time coeﬀicients ρ(t) and σ(t) are given by
                                                   ϖ 
                                                      T
                                        ρ(t) = cl2      t ,
                                               s 2
                                                                                                   (34)
                                                  1 − ρ(t)2
                                       σ(t) =               ,
                                                    ρ(t)

where ϖT ≜ ϖ/T and cl(x) is the lemniscate cosine function in Section 4.1. We prove some
identities of ρ(t) and σ(t) used in the derivation of the ODE and the Lyapunov function.
We first collect the properties of theR lemniscate
                                            √      elliptic functions that these derivations use. Recall
                                        u
from Section 4.1.3 that arcsl(u) = 0 dx/ 1 − x4 , that sl is the inverse of arcsl, and that cl(x) =
sl(ϖ/2 − x).

                                                     51
Lemma 10 (Lemniscatic calculus). The following hold.
   1. sl is a continuous strictly increasing bijection of [0, ϖ/2] onto [0, 1] with sl(0) = 0 and
      sl(ϖ/2) = 1; consequently cl is a continuous strictly decreasing bijection of [0, ϖ/2] onto
                qsl(x), cl(x) ∈ (0, 1) for x ∈
      [0, 1], and                            q(0, ϖ/2).
   2. sl′ (x) = 1 − sl4 (x) and cl′ (x) = − 1 − cl4 (x) for x ∈ (0, ϖ/2).
   3. cl(ϖ/2 − x) = sl(x) for x ∈ [0, ϖ/2].
                1 − sl2 (x)
   4. cl2 (x) =       2     for x ∈ [0, ϖ/2]; equivalently, cl2 (x) + sl2 (x) + cl2 (x) sl2 (x) = 1.
                1 + sl (x)
   5. sl(x) = x + o(x) as x ↓ 0.
   6. For T > 0, the coeﬀicient (34) satisfies 0 < ρ(t) < 1 for t ∈ (0, T ). Its symmetry identity
      ρ(T − t) = (1 − ρ(t)) / (1 + ρ(t)) holds for t ∈ [0, T ].
                                              √
  √ Part 1. On [0, 1) the integrand 1/ 1 − x is positive, and near x = 1 it is bounded by
Proof.                                               4

1/ 1 − x, so arcsl is a continuous strictly increasing bijection of [0, 1] onto [0, ϖ/2]; here arcsl(1) =
ϖ/2 is the definition of ϖ. Its inverse sl inherits these properties, and cl(x) = sl(ϖ/2 − x) inherits
the rest.
                                                                                            q
                                                                 ′                ′
Part 2. For x ∈ (0, ϖ/2) the inverse function theorem gives sl (x) = 1/ arcsl (sl(x)) = 1 − sl4 (x),
                                                       q
and the chain rule gives cl′ (x) = − sl′ (ϖ/2 − x) = − 1 − cl4 (x).

Part 3. Substitute ϖ/2 − x for x in the definition cl(x) = sl(ϖ/2 − x).
                                      p                                              √
Part 4. For u ∈ [0, 1] set v(u) ≜
p                                        (1 − u2 )/(1 + u2 ), so that v(u)(1 + u2 ) = 1 − u4 and
  1 − v(u)4 = 2u/(1 + u2 ). For u ∈ (0, 1),

                              −2u                        v ′ (u)             −1            −1
             v ′ (u) =                    2,   so   p               =                  =√        .
                         v(u) (1 + u2 )                 1 − v(u)4       v(u) (1 + u2 )    1 − u4
        d
Hence du  [arcsl(u) + arcsl(v(u))] = 0 on (0, 1), and by continuity and the value arcsl(0) + arcsl(1) =
ϖ/2 at u = 0,
                                                        ϖ
                              arcsl(u) + arcsl (v(u)) = ,       u ∈ [0, 1].
                                                         2
Taking u = sl(x) for x ∈ [0, ϖ/2] gives arcsl(v(sl(x))) = ϖ/2 − x, that is, v(sl(x)) = sl(ϖ/2 − x) =
cl(x) by part 3. Squaring yields the first identity, and clearing denominators yields the second.
               1, sl(0) = 0, and by the mean value theorem sl(x) = sl′ (ξx ) x for some ξx ∈ (0, x),
Part 5. By partq
where sl′ (ξx ) =   1 − sl4 (ξx ) → 1 as x ↓ 0 by part 1 and continuity.

Part 6. For t ∈ (0, T ) we have ϖT t/2 ∈ (0, ϖ/2), so ρ(t) = cl2 (ϖT t/2) ∈ (0, 1) by part 1. For the
symmetry, parts 3 and 4 give
                                                   
                           2 ϖ     ϖT t        2 ϖT t      1 − cl2 (ϖT t/2)    1 − ρ(t)
             ρ(T − t) = cl      −         = sl          =         2         =           .
                              2      2             2       1 + cl (ϖT t/2)     1 + ρ(t)

Lemma 11. The following identities hold for t ∈ (0, T ):
                                   p
                      ρ̇(t) = −ϖT ρ(t)(1 − ρ(t)2 ) = −ϖT σ(t)ρ(t),

                                                    52
                                                   
                                  ϖT            1
                           σ̇(t) =      ρ(t) +        ,
                                   2           ρ(t)
                                  ϖ2
                           σ̈(t) = T σ(t)3 ,
                                   2
                           σ(t) σ(T − t) = 2.

Proof. Throughout the proof, 0 < ρ(t) < 1 and hence σ(t) > 0 onq(0, T ), by part 6 of Lemma 10, so
every division below is legitimate. By the derivative cl′ (x) = −    1 − cl4 (x) (part 2 of Lemma 10,
                                                                                    p
with cl ≥ 0 from part 1) and (34), ρ(t) satisfies the first identity: ρ̇(t) = −ϖT ρ(t)(1 − ρ(t)2 ) =
−ϖT σ(t)ρ(t). Differentiating σ(t)2 = 1/ρ(t) − ρ(t) and using the first identity gives
                                                                     
                                          1                         1
                    2σ(t)σ̇(t) = − 1 +          ρ̇(t) = ϖT 1 +            ρ(t)σ(t),
                                        ρ(t)2                     ρ(t)2

and dividing both sides by 2σ(t) gives the second identity. Differentiating the second identity and
using the first identity gives the third identity:
                                           
                            ϖT          1             ϖT2 (1 − ρ(t)2 )3/2   ϖT2
                    σ̈(t) =       1−          ρ̇(t) =                     =     σ(t)3 .
                             2        ρ(t)2            2     ρ(t)3/2         2

For the last identity, we use the symmetry ρ(T −t) = (1 − ρ(t)) / (1 + ρ(t)) from part 6 of Lemma 10.
Thus
                                        1 − ρ(T − t)2     4ρ(t)       4
                          σ(T − t)2 =                 =           =       ,
                                          ρ(T − t)      1 − ρ(t)2   σ(t)2

and since σ(t) > 0, this proves the last identity.

The continuous-time ODE. We sketch a derivation of the ODE by identifying the leading-order
behavior of (LemniAcc) as N √     → ∞ with  b      2   2                        x
                                          LN = N /T . On the iterate grid tk = k Tρ/N , we identify
X(tk ) ≈ xk and Z(tk ) ≈ N/( ΩN T ) zk . The coeﬀicient ρk is naturally placed at tk = k T /(N +1);
    x                x

for 0 ≤ k ≤ N , |txk − tρk | ≤ T /(N + 1) = O(1/N ), so we identify ρ(txk ) ≈ ρk at leading order. The
updates of (LemniAcc) are


                                           1 + ρ2            1 + ρ2k  1
                                                    k+1
                         zk+1 = zk − ΩN                   −               ∇f (xk ),
                                             2ρk+1              2ρk L  bN
                                    1
                          k = xk −
                         x+
                                   b
                                      ∇f (xk ),
                                   LN
                                      1 + ρ2      1 + ρ2k+2 
                                             k+1
                         xk+1 = x+ +             −             zk+1 .
                                 k
                                       1 − ρ2k+1 1 − ρ2k+2

                                             √
The z-update coeﬀicient, after division by       ΩN to account for the rescaling of Z, has the following
leading-order form:


                                                     53
   p                                                                    3/2
       1 + x2 k+1 p                         p
              ρ
                                   1 − ρ2k             1 − ρ2   1 1 − ρ2       1
    ΩN           ≈ ΩN (ρk − ρk+1 )     2   ≈ ρ(1 − ρ )
                                                    2
                                                           2
                                                              =               = σ3,
         2x ρk                       2ρk                2ρ      2   ρ          2

which follows from the mean value theorem, the continuity of ρ(t), and the recurrence (9). For the
x-update, define ϕk = (1 + ρ2k )/(2ρk ). The symmetry ρN +1−k = (1 − ρk )/(1 + ρk ) from Section 4.1
rewrites the coeﬀicient
               √        in the x-update as ϕN −k − ϕN −k−1 . Applying the preceding calculation
at T − t gives ΩN (ϕN −k − ϕN −k−1 ) ≈ σ(T − t)3 /2. Since 1/L  b N = T 2 /N 2 and ∆t = T /N , the
updates give ∆Z ≈ −(σ 3 /2)∇f (X) ∆t and ∆X ≈ (σ(T − t)3 /2)Z ∆t at leading order. The direct
                                                    b
gradient step x+k − xk carries the smaller factor 1/LN = O(∆t ) and hence does not contribute at
                                                              2

this order.
This development suggests the coupled ODE for X(t) and Z(t) on (0, T ):

                                           σ(t)3
                                  Ż(t) = −      ∇f (X(t)),
                                             2
                                          σ(T − t)3           4
                                  Ẋ(t) =           Z(t) =        Z(t).
                                              2             σ(t)3

Differentiating Z(t) = σ(t)3 Ẋ(t)/4 and using Ż(t) = −σ(t)3 ∇f (X(t))/2 gives the following second-
order ODE for X(t):

                          Ẍ(t) + γ(t)Ẋ(t) + 2∇f (X(t)) = 0,      0 < t < T,                   (35)

where γ(t) ≜ 3σ̇(t)/σ(t) is the coeﬀicient of the friction term.
Lemma 12. The ODE in (35) can be written as
                     "               #
                         ϖt        ϖt
                   3ϖ cl 2T     sl 2T
           Ẍ(t) +          
                         ϖt +      ϖt
                                       Ẋ(t) + 2∇f (X(t)) = 0,             0 < t < T.
                   2T sl 2T     cl 2T

Proof. We only need to calculate the friction term γ(t) = 3σ̇(t)/σ(t) in (35). By the second identity
of Lemma 11, we have
                            σ̇    ϖT ρ + ρ−1           ϖT     1 + ρ2
                               =      p              =    p             .
                            σ      2     (1 − ρ2 )/ρ    2    ρ(1 − ρ2 )
Substituting ρ(t) = cl2 (ϖT t/2) gives

                                  3ϖT          1 + cl4 (ϖT t/2)
                         γ(t) =                    q
                                   2
                                         cl(ϖT t/2) 1 − cl4 (ϖT t/2)
                                  3ϖT            1 + cl4 (ϖT t/2)
                              =                                             
                                   2 cl(ϖT t/2) sl(ϖT t/2) 1 + cl2 (ϖT t/2)
                                3ϖT cl2 (ϖT t/2) + sl2 (ϖT t/2)
                              =
                                 2     cl(ϖT t/2) sl(ϖT t/2)
                                                               
                                3ϖT cl(ϖT t/2) sl(ϖT t/2)
                              =                  +                .
                                 2    sl(ϖT t/2) cl(ϖT t/2)

                                                    54
                                                                                                    p
where we use cl2 (x) + sl2 (x) + cl2 (x)sl2 (x) = 1 (part 4 of Lemma 10, which also gives               1 − cl4 =
sl (1 + cl2 ) for the second equality) to simplify the form.

Proof of Theorem 2. Assume that X ∈ C 2 ([0, T ]; R d ). Denote xT ≜ X(T ) and ϖT ≜ ϖ/T , and
set Z(t) ≜ σ(t)3 Ẋ(t)/4 for t ∈ (0, T ). Then the second-order ODE and the definition of γ imply
Ż(t) = −σ(t)3 ∇f (X(t))/2. The Lyapunov function V(t) is defined for t ∈ (0, T ) as

                         1 − ρ2                         (1 − ρ)2
                V(t) ≜          (f (X(t)) − f (x⋆ )) −           (f (xT ) − f (x⋆ ))
                           2ρ                              2ρ
                         |                           {z                            }
                                                     A(t)
                                                                   2
                                                                                            !               (36)
                          ϖ2                     1 + ρ2 Z(t)                       Z(t) 2
                         + T         X(t) − x⋆ +                       − xT − x⋆ +              .
                            2                    1 − ρ2 ϖT                         ϖT
                          |                             {z                                  }
                                                            B(t)

Here and below, ρ, σ, X, Z, and their derivatives are evaluated at t when their arguments are
omitted. We calculate the derivative of function-value terms A(t) and squared-norm terms B(t)
separately. The function-value terms can be simplified as follows:

                             1 − ρ2                      (1 − ρ)2
                    A(t) =          (f (X) − f (x⋆ )) −           (f (xT ) − f (x⋆ ))
                               2ρ                           2ρ
                                                         (1 − ρ)2
                           = (1 − ρ) (f (X) − f (x⋆ )) +          (f (X) − f (xT )) .
                                                            2ρ

Using the identity ρ̇ = −ϖT σρ of Lemma 11 and σ 2 = ρ−1 − ρ, we have
                                               
                                     d (1 − ρ)2     ϖT σ 3
                                                  =        ,
                                    dt    2ρ           2

so the derivative of the function-value terms is
                                                   ϖT σ 3                    2
             Ȧ(t) = ϖT σρ (f (X) − f (x⋆ )) +            (f (X) − f (xT )) + hZ, ∇f (X)i .
                                                    2                        σ

For the squared-norm terms B(t), the identities of Lemma 11 give
                                                
                                    d 1 + ρ2          4ϖT
                                                   =− 3 .
                                    dt 1 − ρ   2       σ

Consequently,                                                
                                d                 1 + ρ2 Z             1 + ρ2 Ż
                                         X − x⋆ +                  =             ,
                                dt                1 − ρ2 ϖT            1 − ρ2 ϖT
where Ẋ = 4Z/σ 3 cancels −4Z/σ 3 . Differentiating the squared-norm terms B(t), substituting
Ż = −σ 3 ∇f (X)/2, and using σ 2 = ρ−1 − ρ gives

                                                    ϖT σ 3                    2
          Ḃ(t) = −ϖT σρ hX − x⋆ , ∇f (X)i −               hX − xT , ∇f (X)i − hZ, ∇f (X)i .
                                                     2                        σ

                                                      55
Adding the two derivatives Ȧ(t) and Ḃ(t), the terms involving hZ, ∇f (X)i cancel, and we obtain
V̇(t) = −ϖT σρDf (x⋆ , X)−(ϖT σ 3 /2)Df (xT , X) ≤ 0, where Df (y, x) ≜ f (y)−f (x)−hy −x, ∇f (x)i,
and the inequality follows from convexity of f , in the form Df (y, x) ≥ 0. Thus V(t) is non-increasing
on (0, T ).
For limits of the endpoints t ↓ 0 and t ↑ T , we substitute Z = σ 3 Ẋ/4 and expand the two squared
norms in (36) to expose the cancellation between potentially singular terms as t ↑ T . The expanded
form of (36) is:
                                                        (1 − ρ)2
                     V(t) = (1 − ρ) (f (X) − f (x⋆ )) +          (f (X) − f (xT ))
                                                           2ρ
                                ϖ2                             σ2         2
                                                                                                (37)
                             + T kX − x⋆ k2 − kxT − x⋆ k2 +             Ẋ
                                 2                                   8
                                ϖT σρ D             E ϖ σ3 D
                                                          T
                                                                           E
                             +          X − x⋆ , Ẋ +           X − xT , Ẋ .
                                   2                       4

For the limit t ↓ 0, ρ(t) → 1, σ(t) → 0, X(t) → x0 , and Ẋ(t) → 0, so V(t) has the limit:

                                         ϖT2                           
                            lim V(t) =         kx0 − x⋆ k2 − kxT − x⋆ k2 .                        (38)
                             t↓0          2

For the limit t ↑ T , denote δ = T − t and gT ≜ ∇f (xT ). The leading order terms of the coeﬀicients
ρ, σ, and γ as δ ↓ 0 are
                                                  ϖ2
                                      ρ(T − δ) = T δ 2 + o(δ 2 ),
                                                    4
                                                    2
                                      σ(T − δ) =       + o(δ −1 ),                              (39)
                                                  ϖT δ
                                                  3
                                      γ(T − δ) = + o(δ −1 ).
                                                  δ
Indeed, the relation cl (ϖT (T − δ)/2) = sl(ϖT δ/2) and sl(x) = x+o(x) (parts 3 and 5 of Lemma 10)
gives the expression for ρ; the other two follow from the definitions of σ and γ. Moreover, differ-
entiating the identity σ(t) σ(T − t) = 2 of Lemma 11 gives σ̇(t)/σ(t) = σ̇(T − t)/σ(T − t), so
γ(t) = γ(T − t); hence γ(t) = 3/t + o(t−1 ) as t ↓ 0 as well.
We next obtain the corresponding expansion of the trajectory. Since X ∈ C 2 ([0, T ]), the right-
hand side of γ(t)Ẋ(t) = −Ẍ(t) − 2∇f (X(t)) is bounded as t ↑ T . Because γ(t) → ∞, this forces
Ẋ(T ) = 0. Taylor expansion of Ẋ(t) gives Ẋ(T − δ) = −Ẍ(T )δ + o(δ). Hence the left-hand
side above converges to −3Ẍ(T ), whereas its right-hand side converges to −Ẍ(T ) − 2gT . Thus
Ẍ(T ) = gT , and further Taylor expansion gives

                            Ẋ(T − δ) = −gT δ + o(δ),
                                              1
                            X(T − δ) = xT + gT δ 2 + o(δ 2 ),                                     (40)
                                              2
                                                    1
                            f (X(T − δ)) − f (xT ) = kgT k2 δ 2 + o(δ 2 ).
                                                    2




                                                  56
Using (39) and (40), the limit of V(t) in (37) is calculated term by term:

                                                    kgT k2       kgT k2       kgT k2
                   lim V(t) = f (xT ) − f (x⋆ ) +          + 0 +        + 0 −
                   t↑T                               ϖT2          2ϖT2         ϖT2
                                                                                             (41)
                               1
                            =    2 k∇f (xT )k2 + f (xT ) − f (x⋆ ).
                              2ϖT

For any 0 < s < t < T , monotonicity gives V(s) ≥ V(t). Letting s ↓ 0 and then t ↑ T in this
inequality, (38) and (41) gives the stronger estimate

              k∇f (xT )k2 + 2ϖT2 (f (xT ) − f (x⋆ )) + ϖT4 kxT − x⋆ k2 ≤ ϖT4 kx0 − x⋆ k2 .

Dropping nonnegative terms and substituting ϖT = ϖ/T proves both stated bounds.


B    Deferred proofs and details for ITEM-f
B.1 Existence and uniqueness of the ITEM-f construction
We first derive the target angle and describe the shooting computation of the ITEM-f coeﬀicients,
then prove that it produces the unique construction of Lemma 4. Throughout, N ≥ 1 and q ∈ (0, 1)
are fixed, Υ > 1 denotes a candidate value of the constant, and we write
                                          p                        q R(Υ)    p
               C(Υ) ≜ (Υ, 0),    R(Υ) ≜    Υ2 − 1,        p(Υ) ≜          = q 1 − Υ−2 ,
                                                                      Υ
abbreviated to C, R, and p when the argument is clear. The map Υ 7→ 1 − Υ−2 is continuous and
strictly increasing on (1, ∞); hence so is p, with 0 < p(Υ) < q, p(Υ) → 0 as Υ ↓ 1, and p(Υ) → q
as Υ → ∞.

Target angle. For a prospective admissible configuration at a candidate Υ > 1, write P1 − C =   
                                                                                    √
R(cos θ1 , sin θ1 ) with θ1 ∈ (0, π). The endpoint formula gives P0 − C = −R2 /Υ, 1 − q R/Υ ,
so the inner-product condition at k = 0 evaluates on both sides; equating the two evaluations and
simplifying (tedious but straightforward algebra) gives
                                       p                      p
                              sin θ1 = 1 − q (Υ + R cos θ1 ) = 1 − q a1 .                     (42)
                                                              √
Since b1 = R sin θ1 , this says that P1 lies on the line b = 1 − q R a through the origin and
                                                                                             P0 .
Substitution into (a − Υ)2 + b2 = R2 , using Υ2 −R2 = 1, gives the quadratic 1 + (1 − q)R2 a2 −
                                             √
2Υa + 1 = 0, whose roots are a± = Υ ± q R / 1 + (1 − q)R2 . The quadratic is negative at
                                                                                 √
a0 = 1/Υ, so a− < a0 < a+ . Hence the ordering constraint selects the point (a+ , 1 − q R(Υ)a+ ).
Its angle about C(Υ) is the target angle ϑ(Υ) ∈ (0, π), where
                                                      √
                                           a+ − Υ       q − (1 − q)R Υ
                               cos ϑ(Υ) ≜          =                   .                     (43)
                                              R        1 + (1 − q)R2

We also define ϑ(Υ) for any Υ > 1 by this formula, even if the corresponding construction does not
exist.


                                                    57
Shooting computation.       For each candidate Υ > 1, define its backward shooting orbit by
                               √
              θN (Υ) ≜ arccos(− q),
                                                                                                       (44)
              θk (Υ) ≜ θk+1 (Υ) + arccos(1 − q − p(Υ) cos θk+1 (Υ)) ,      k = N − 1, . . . , 1.

Every admissible construction obeys this recurrence. Indeed, if a candidate Υ admits the required
points, then every intermediate point has a unique representation Pk − C(Υ) = R(Υ)(cos θk , sin θk )
with θk ∈ (0, π). The ordering of the abscissas gives θ1 > · · · > θN , while the inner-product
conditions give cos(θk − θk+1 ) = 1 − q − p(Υ) cos θk+1 for 1 ≤ k ≤ N − 1. At k = N , the same
                          √                                             √
condition gives sin θN = 1 − q, and aN < aN +1 selects cos θN = − q. Therefore admissible
constructions satisfy (44). Define the shooting residual by ΞN (Υ) ≜ θ1 (Υ) − ϑ(Υ) for Υ > 1.
Lemma 16 below shows that the candidate closes exactly when ΞN (Υ) = 0.
The numerical value of the root ΥN can be computed by bisection. Initialize Υl = 1 as an uneval-
uated sentinel, since ΞN is defined only on (1, ∞), and set Υr = 2. Double Υr until ΞN (Υr ) < 0.
Then bisect the interval [Υl , Υr ] by computing the midpoint Υm = (Υl + Υr )/2, replace Υl by Υm
when ΞN (Υm ) > 0, and replace Υr by Υm when ΞN (Υm ) < 0. For a prescribed tolerance ϵ > 0,
return Υm if ΞN (Υm ) = 0 or |Υr − Υl | < ϵ. Corollary 3 proves that the doubling terminates and
the bracket always contains ΥN . If the bisection is continued indefinitely, its midpoints converge
to ΥN ; if it stops with bracket width below ϵ, the returned value is within ϵ of ΥN .
Lemma 13 (One-step map). Fix q ∈ (0, 1) and p ∈ (0, q), and define Fp (θ) ≜ θ+arccos (1 − q − p cos θ).
Then:
  1. Fp is well defined on R: the argument of the arccos lies in (1 − 2q, 1) ⊂ (−1, 1), so Fp (θ) − θ ∈
     (0, π);
  2. Fp is strictly increasing in θ;
  3. for fixed θ with cos θ < 0, the map p 7→ Fp (θ) is strictly decreasing.

Proof. Write u ≜ 1 − q − p cos θ. Claim 1 follows from |p cos θ| ≤ p < q leading to −1 < 1 − 2q <
1 − q − p ≤ u ≤ 1 − q + p < 1.
                                                               √
For claim 2, differentiating in θ gives Fp′ (θ) = 1 − (p sin θ/ 1 − u2 ), so it suﬀices to prove p2 sin2 θ <
1 − u2 expanding u = 1 − q − p cos θ, tedious but straightforward algebra gives p2 sin2 θ + u2 ≤
(p + 1 − q)2 < 1, the last inequality because 0 < p + 1 − q < 1 by √     p < q. This proves claim 2. For
claim 3, differentiating in p gives for cos θ < 0, ∂Fp (θ)/∂p = cos θ/ 1 − u2 < 0.

By Lemma 13, the orbit in (44) which is written as θk (Υ) = Fp(Υ) (θk+1 (Υ)) is defined for every Υ >
                                                                                               √
1, each θk (Υ) is a continuous function of Υ, and θ1 (Υ) > θ2 (Υ) > · · · > θN (Υ) = arccos − q >
π/2.
Lemma 14 (Orbit comparison). Let N ≥ 2 and 1 < Υ < Υ′ . If θ1 (Υ) ≤ π, then θk (Υ′ ) < θk (Υ)
for 1 ≤ k ≤ N − 1.

Proof. The hypothesis gives θk (Υ) ∈ (π/2, π], hence cos θk (Υ) < 0, for every 1 ≤ k ≤ N . We induct
                                                                  √
downward on k. For the base case k = N − 1, since cos θN = − q < 0 and p(Υ′ ) > p(Υ), claim 3
of Lemma 13 gives θN −1 (Υ′ ) = Fp(Υ′ ) (θN ) < Fp(Υ) (θN ) = θN −1 (Υ). For the step from k + 1 to
k ≤ N − 2, claims 2 and 3 of Lemma 13 give θk (Υ′ ) = Fp(Υ′ ) (θk+1 (Υ′ )) < Fp(Υ′ ) (θk+1 (Υ)) <


                                                    58
Fp(Υ) (θk+1 (Υ)) = θk (Υ), where the first inequality uses the induction hypothesis and the second
uses cos θk+1 (Υ) < 0.
Lemma 15 (Target angle). The target angle (43) is well defined, continuous, and strictly increasing
                                                                 √ 
on (1, ∞), with ϑ(Υ) ∈ (0, π) for every Υ > 1, ϑ(Υ) → arccos q as Υ ↓ 1, and ϑ(Υ) → π as
Υ → ∞.

Proof. Write c(Υ) for the fraction in (43), and note that its denominator is 1 + (1 − q)R2 =
                                                                    √
q + (1 − q)Υ2 . Then c(Υ) < 1, since the numerator is at most q < 1 < q + (1 − q)Υ2 . Moreover,
using Υ (Υ − R) = Υ/(Υ + R) (from Υ2 − R2 = 1), tedious but straightforward algebra writes
c(Υ) + 1 as a ratio of positive quantities, so c(Υ) > −1: hence ϑ(Υ) = arccos c(Υ) is well defined in
(0, π), and it is continuous. Differentiating the quotient and simplifying (tedious but straightforward
algebra) gives, for Υ > 1,
                                                                    √     
                               ′         (1 − q) (1 + q)Υ2 − q + 2 q ΥR
                              c (Υ) = −                                     ,
                                                 R (q + (1 − q)Υ2 )2
                                                 √
whose bracketed factor equals (1+q) Υ2 − 1 +2 q ΥR+1 > 1. Every remaining factor is positive,
so c′ (Υ) < 0 and c is strictly decreasing on (1, ∞), and composing with the strictly decreasing arccos
                                                                                                    √
shows that ϑ is strictly increasing. The limits follow by substitution: as Υ ↓ 1, R → 0 and c → q;
as Υ → ∞, dividing the numerator and denominator of c by (1 − q)Υ2 gives c → −1.

For Υ > 1, call a collection of points an admissible configuration at Υ if it satisfies the ordering,
positivity, and conditions of Lemma 4 with ΥN replaced by Υ (and hence with C = C(Υ) and
R = R(Υ)).
Lemma 16 (Shooting equivalence). An admissible configuration at Υ > 1 exists if and only if
ΞN (Υ) = 0. When it exists, it is unique.

Proof. Suppose an admissible    configuration exists at Υ. By the angle parametrization, its angles
                       √ 
satisfy θN = arccos − q and the backward recurrence (44), so they coincide with the orbit θk (Υ);
in particular θ1 (Υ) < π. Moreover, the shooting equation (42) together with a1 > a0 places P1
at the farther intersection, so cos θ1 (Υ) = cos ϑ(Υ); both angles lie in (0, π), hence θ1 (Υ) = ϑ(Υ).
Every coordinate is forced (P0 and PN +1 by their formulas, Pk by θk (Υ)), which is the uniqueness
claim.
Conversely, suppose θ1 (Υ) = ϑ(Υ). Define Pk ≜ C + R (cos θk (Υ), sin θk (Υ)) for 1 ≤ k ≤ N and
the endpoints by their formulas. Then all θk (Υ) lie in (0, π) because 0 < θN ≤ θk (Υ) ≤ θ1 (Υ) =
ϑ(Υ) < π, so bk = R sin θk (Υ) > 0; the angles decrease strictly in k, so a1 < · · · < aN ; and
            √
aN = Υ − q R < Υ = aN +1 . The norm condition holds by construction. For the inner-product
condition at 1 ≤ k ≤ N − 1, taking cosines in (44) gives cos (θk − θk+1 ) = 1 − q − p cos θk+1 =
1 − q ak+1 /Υ, and (Pk − C) · (Pk+1 − C) = R2 cos (θk − θk+1 ) since both points lie on the circle;
                                                  √                                    √
at k = N the condition holds because sin θN = 1 − q. At k = 0: the point a+ , 1 − q R a+
lies on the circle with positive ordinate, and P1 is the point of the circle with the same abscissa
                                                                                         √
a1 = Υ + R cos ϑ(Υ) = a+ and positive ordinate, so the two coincide; hence sin θ1 (Υ) = 1 − q a1 ,
which is (42) and, reversing the algebra that produced it, the inner-product condition at k = 0.
Finally a0 = 1/Υ < a+ = a1 .


                                                  59
Proof of Lemma 4. Existence. We first show ΞN (Υ) < 0 for all large Υ. Consider the boundary
parameter p = q: the map Fq (θ) = θ + arccos (1 − q(1 + cos θ)) is still well defined, since 1 − q(1 +
cos θ) ∈ [1 − 2q, 1]. For θ ∈ (0, π),

                           Fq (θ) < π ⇔ arccos (1 − q(1 + cos θ)) < π − θ
                                      ⇔ 1 − q(1 + cos θ) > − cos θ
                                      ⇔ (1 − q)(1 + cos θ) > 0,

which holds; so the orbit θN ≜ θN , θk ≜ Fq (θk+1 ) satisfies θ1 < π by induction. Each backward step
(p, θ) 7→ Fp (θ) is jointly continuous for p ∈ [0, q] because the arccos argument stays in [1 − 2q, 1];
at the endpoint p = 0 it reads F0 (θ) = θ + arccos (1 − q). Hence θ1 (Υ), which depends on Υ only
through p(Υ), converges to θ1 as p(Υ) → q, that is, as Υ → ∞. Combining with Lemma 15, we
have limΥ→∞ ΞN (Υ) = θ1 − π < 0, so ΞN (b) < 0 for some b > 1.
Next we produce a point where ΞN > 0. As Υ ↓ 1 we have p(Υ) → 0, so by the same joint continuity,
                                                                                         √ 
now at the endpoint p = 0, θ1 (Υ) → θN + (N − 1) arccos (1 − q), while ϑ(Υ) → arccos q by
Lemma 15. Therefore
                                                   √                   √
lim ΞN (Υ) = θN + (N − 1) arccos (1 − q) − arccos ( q) ≥ π − 2 arccos ( q) = arccos (1 − 2q) > 0,
Υ↓1

where the middle   inequality drops the nonnegative term (N − 1) arccos (1 − q) and uses θN =
         √                   √                                                            √
arccos − q = π − arccos q , and the last equality holds because cos π − 2 arccos q =
                                      √
− (2q − 1) = 1 − 2q and π − 2 arccos q ∈ (0, π). By continuity, ΞN (a) > 0 for some a > 1.
Hence ΞN (a) > 0 > ΞN (b) with a < b (enlarging b if necessary), so the intermediate value theorem
yields ΥN ∈ (a, b) with ΞN (ΥN ) = 0. By Lemma 16, an admissible configuration exists at ΥN .
Uniqueness. Suppose Υ < Υ′ both admit admissible points, so that θ1 (Υ) = ϑ(Υ) < π and
                                                                                √
θ1 (Υ′ ) = ϑ(Υ′ ) by Lemma 16. For N = 1 the orbit is the constant arccos − q , and the strict
monotonicity of ϑ makes the two equalities incompatible. For N ≥ 2, Lemma 14 applies at Υ (its
hypothesis θ1 (Υ) ≤ π holds) and gives, with Lemma 15, θ1 (Υ′ ) < θ1 (Υ) = ϑ(Υ) < ϑ(Υ′ ) = θ1 (Υ′ ), a
contradiction. Hence the admissible Υ is unique, and Lemma 16 shows that the points are uniquely
determined by it.

The same objects also give a sign characterization of the residual that makes the numerical evalu-
ation of ΥN straightforward.
Corollary 3 (Bisection correctness). Let ΥN be as in Lemma 4. Then the residual ΞN defined
above satisfies ΞN (Υ) > 0 for 1 < Υ < ΥN and ΞN (Υ) < 0 for Υ > ΥN . Consequently both update
rules of the bisection described above are correct, the doubling of the right endpoint terminates and
produces a bracket containing ΥN , the invariant Υl < ΥN < Υr is maintained, and, if the bisection
is continued indefinitely, the midpoints converge to ΥN . For any ϵ > 0, if it stops with bracket
width below ϵ, the returned value is within ϵ of ΥN .

Proof. By Lemma 16, θ1 (ΥN ) = ϑ (ΥN ) < π, so ΞN (ΥN ) = 0. For Υ > ΥN , Lemma 14 applies
at ΥN (its hypothesis θ1 (ΥN ) ≤ π holds) and gives, with the strictly increasing target angle of
Lemma 15, ΞN (Υ) = θ1 (Υ) − ϑ(Υ) < θ1 (ΥN ) − ϑ (ΥN ) = 0. For 1 < Υ < ΥN , either θ1 (Υ) ≥
π > ϑ(Υ) and ΞN (Υ) > 0 directly, or θ1 (Υ) < π and Lemma 14, now applied at Υ, gives in the


                                                  60
                                                                                      √ 
same way ΞN (Υ) > ΞN (ΥN ) = 0. (For N = 1 the orbit is the constant arccos − q and both
inequalities hold through the target angle alone.) For the bisection, the doubling terminates, since
ΞN < 0 once Υr exceeds ΥN , producing a bracket Υl = 1 < ΥN < Υr ; by the sign characterization
each update rule fires exactly on its side of ΥN , and the bisection bookkeeping is exactly parallel
to the argument of Appendix A.1, so the invariant Υl < ΥN < Υr is preserved. If the bisection is
continued indefinitely, its bracket width tends to zero, so the midpoints converge to ΥN . At finite
termination with |Υr − Υl | < ϵ, the bracket invariant puts the returned value within ϵ of ΥN .
Lemma 17 (Symmetry of the construction). For 0 ≤ k ≤ N + 1,

                                          ak aN +1−k = 1,
                                                                                                           (45)
                                           ak bN +1−k = bk .

Proof. The circle equation is equivalent to a2 + b2 − 2ΥN a + 1 = 0, and the map, defined for a > 0,
T (a, b) = (1/a, b/a), which satisfies T ◦ T = id, maps this circle to itself, with T (P0 ) = PN +1 .
Moreover, if P = (a, b) and P ′ = (a′ , b′ ) satisfy
                                                                   
                                                ′               qa′
                               (P − C) · (P − C) = RN 1 −
                                                       2
                                                                      ,
                                                               ΥN

then direct expansion gives
                                                                                               
             ′                       (P − C) · (P ′ − C) + RN
                                                            2 (aa′ − 1)
                                                                                          q
       (T (P ) − C) · (T (P ) − C) =                                       2
                                                                        = RN        1−              .
                                                     aa′                                 ΥN a

This is the recurrence for the reversed pair, since the first coordinate of T (P ) is 1/a. Hence
Pek ≜ T (PN +1−k ) satisfies the same endpoint conditions and recurrence as Pk . Its first coordinates
are strictly increasing and its second coordinates are positive, so uniqueness in Lemma 4 gives
T (Pk ) = PN +1−k . Comparing coordinates proves (45).

The construction also gives the explicit relaxation used in Theorem 3.
                                                                                                √
Lemma 18. Let ΥN be as in Lemma 4. Then, for every N ≥ 1, we have 1/Υ2N < 4(1 −                         q)2N .

Proof. For the construction angles θk , define tk ≜ cot (θk /2) for 1 ≤ k ≤ N . The half-angle formula
gives
                                         sin θk              bk
                                tk =              =                   .
                                       1 − cos θk    Υ N + RN − a k

By the symmetry of Lemma 17, a1 aN = 1 and b1 = a1 bN ; substituting these together with aN =
      √                √
ΥN − q RN and bN    = 1 −√q RN into the half-angle formula,    tedious
                                                                        but straightforward algebra
            √                                             √               √
gives t1 =    1 − q / (1 − q)(ΥN + RN ) and tN =            1 − q / 1 + q . For 1 ≤ k ≤ N − 1,
the inner-product condition, cos θk+1 < 0, and RN < ΥN give
                                                             
                                                RN
                   cos(θk − θk+1 ) = 1 − q 1 +       cos θk+1
                                                ΥN
                                                                              
                                                                          θk+1
                                   < 1 − q(1 + cos θk+1 ) = 1 − 2q cos2          ,
                                                                            2


                                                  61
and hence, taking half-angle sines, expanding sin((θk −θk+1 )/2), and dividing by sin(θk /2) sin(θk+1 /2)
                                                       √
(tedious but straightforward algebra), tk < (1 − q)tk+1 for 1 ≤ k ≤ N − 1, which gives
         √ N −1
t1 ≤ (1 − q)      tN .
Combining the contraction with these boundary values,
                                                                √
                      1        1                     √ N −1 (1 − q)N
                         <          = t1 tN ≤ tN (1 − q)
                                               2
                                                           =     √ .
                     2ΥN   Υ N + RN                           1+ q
                                   √ 2    √            √
It follows that 1/Υ2N < 2/(1 +      q) (1 − q)2N < 4(1 − q)2N , which completes the proof.

B.2 Norm identities for the ITEM-f Lyapunov sequence
This appendix proves Lemma 5 and shows how the update equation of (ITEM-f) enters the analysis.

Proof of Lemma 5. We use the coordinate relations

                             ck ak + sk bk = (1 − q)ak+1 ,   1 ≤ k ≤ N,
                                                                                                   (46)
                             ak = (ck + q)ak+1 − sk bk+1 ,    1 ≤ k ≤ N − 1.

For 1 ≤ k ≤ N − 1, these are the coordinate relations for the rotation from
                                                                        p Pk − C to Pk+1 − C and
its inverse. At k = N , the first identity follows from cN = 1 − q, sN = q(1 − q), aN +1 = ΥN , and
                           √                             √
the boundary facts bN = 1 − q RN and ΥN − aN = q RN of the construction (Appendix B.1).
First identity. Let g0 ≜ ∇f (x0 ). Since x+
                                          −1 = x0 , the first update (ITEM-f) and the definition of
ϕN with a1 aN = 1, a0 = 1/ΥN give
                                                      
                                 ϕN −1         a0         g0               ϕN −1 g0
           x1 − x⋆ = x0 − x⋆ −
                       +
                                         1+                     0 − x⋆ −
                                                             = x+           √         .
                                  ϕN        (1 − q)a1 L                  ΥN 1 − q L

The definition of s1 gives                                    r
                                    (1 − q)a2 ϕN −1               1−q
                                               √      =               .
                                        s1   ΥN 1 − q              q
Substituting this update into the definition (20) of W1 and using the first coordinate relation (46),
we have                                                             
                                                a1 (x+0 − x⋆ )
                                                         r
                                W1 =                       1 − q g0  .
                                         b1 (x0 − x⋆ ) −
                                              +
                                                               q L
                                                         √
The boundary relations in the construction give b1 = 1 − q RN a1 (the shooting relation (42)) and
              √
ΥN a1 − 1 = q RN a1 (equivalent to a1 aN = 1 from Lemma 17). Together with the circle equation
for P1 , these imply
                                            r
                                               1−q
                                     b1 =            (ΥN a1 − 1),
                                                q
                                     a21 + b21 = 2ΥN a1 − 1.




                                                    62
Expanding the squared norm and using µ = qL, ΥN a0 = 1, and (1 − q)g0 = ge0 + µ(x+
                                                                                 0 − x⋆ ), we
obtain
                                           1−q
                                             2          2(ΥN a1 − 1) +
       kW1 k2 = (2ΥN a1 − 1) x+
                              0 − x⋆           kg0 k2 −
                                                 +                     x0 − x⋆ , (1 − q)g0
                                           qL2                µ
                          2   1−q           2ΥN
              =    0 − x⋆
                  x+        +    2
                                   kg0 k2 −     (a1 − a0 ) x+
                                                            0 − x⋆ , g
                                                                     e0 .
                              qL             µ
                                                  −1
                              0 − x⋆ = x0 − x⋆ − L g0 and g
Finally, direct expansion of x+                           e0 = g0 − qL(x0 − x⋆ ) gives

                               2       1−q                                 1
                      0 − x⋆
                     x+            +      2
                                            kg0 k2 = (1 − q) kx0 − x⋆ k2 + 2 ke
                                                                              g 0 k2 .
                                       qL                                 qL

Since 1/(qL2 ) = ΥN a0 /(µL), substitution proves the first identity.
                                                         √
Second identity. For 1 ≤ k ≤ N − 1, the definition sk = q ak+1 ϕN −k /ΥN gives ϕN −k−1 /ϕN −k =
(ak+1 sk+1 )/(ak+2 sk ). Thus the update of (ITEM-f) becomes
                                      ak sk+1                   ak+1 sk+1 +
                  xk+1 = x+
                          k +                     (x+ − x+   )+          (xk − xk ).
                                   (1 − q)ak+2 sk   k    k−1     ak+2 sk

Substituting this into the definition (20) of Wk+1 and using the first coordinate relation (46) gives
                                                                                   
                                                      k − x⋆ )
                                               ak+1 (x+
               Wk+1 =                      ak +             (1 − q)ak+1 +          .
                                 k − x⋆ ) + s (xk − xk−1 ) +
                          bk+1 (x+                                       (xk − xk )
                                                      +
                                             k                    sk

Subtracting Ok Wk of (21), the first component of Wk+1 − Ok Wk is:
                                                                         ak+1
                               k − x⋆ ) − (1 − q)ak+1 (xk − x⋆ ) = −
                        ak+1 (x+
                                                                          L
                                                                              gek .

The second component is:

                                          ak +                (1 − q)ak+1 +
                            k − x⋆ ) +
                     bk+1 (x+
                                          sk
                                             (xk − x+k−1 )+
                                                                   sk
                                                                          (xk − xk )

                          (1 − q)ck ak+1 (xk − x⋆ ) − ak (x+   k−1 − x⋆ )
                        −
                                                  sk
                                                      
                                   ak      (1 − q)ak+1
                      = bk+1 +
                                   sk
                                        +
                                                sk
                                                         (x+ k − x⋆ )

                          (1 − q)ak+1 (1 + ck )
                        −                          (xk − x⋆ )
                                       sk
                        ak+1 (1 + ck ) +                                
                      =                   xk − x⋆ − (1 − q)(xk − x⋆ )
                              sk
                          ΥN sk
                      =−         gek ,
                            µ




                                                     63
where the second equality uses the second coordinate relation (46) and the last equality uses
ak+1 (1 + ck )/sk = ak+1 sk /(1 − ck ) = ΥN sk /q and x+                                 −1 e . Since
                                                           k − x⋆ = (1 − q)(xk − x⋆ ) − L g  k
1 − ck = qak+1 /ΥN , the two components give
                                                                                  
                                        ΥN (1 − ck )e  gk       ΥN      (ck − 1)e gk
                   Wk+1 − Ok Wk = −                         =−     Ok                  ,
                                         µ      sk gek           µ         sk gek

where the last equality uses c2k + s2k = 1. Rearrangement gives
                                                                  
                                                   ΥN (ck − 1)e  gk
                               Wk+1 = Ok Wk −                          .
                                                    µ     sk gek

Taking norms and using the orthogonality of Ok proves the second identity.
                                                                                    p
Third identity. At k = N , the definition (20) of WN and cN = 1 − q, sN =               q(1 − q), and
aN +1 = ΥN give
                                                                      
                                              N −1 − x⋆ )
                                         aN (x+
                            r
                    WN =  1 − q                                       .
                                     ΥN (xN − x⋆ ) − aN (x+
                                                          N −1 − x⋆ )
                                q
Expanding and regrouping its squared norm yields
                                      21−q                                     2
         kWN k2 = a2N x+
                       N −1 − x⋆          +                        N −1 − x⋆ )
                                              ΥN (xN − x⋆ ) − aN (x+
                                         q
                                            1                                          2
                 = (1 − q)Υ2N kxN − x⋆ k2 +                                N −1 − x⋆ )
                                               (1 − q)ΥN (xN − x⋆ ) − aN (x+             ,
                                            q
which is the third identity.

B.3 Computer-assisted algorithm design by PEP
PEP formulation of the problem. This subsection presents the Stage-1 derivation that bnb-pep-
skill wrote for the ITEM-f design problem, again lightly edited for presentation. The derivation
follows the PEP methodology of Section 3.1 [19, 65, 14], developed in detail for lemniscate acceler-
ation in Appendix A.3, whose notation (Section 4) it reuses. Below we spell out the case-specific
ingredients, namely the function class, the function-value performance measure with its normalized
initial condition, and the reduction to a transformed function, and refer to Appendix A.3 for the
steps that carry over unchanged.
The design problem is instantiated with the function class F = Fµ,L and the method class MN
of N -step FSFOMs. Applying a method in MN to f ∈ Fµ,L from a starting point x0 , with the
stepsizes normalized by L as in Appendix A.3, produces the iterates

                                           1X
                                              i−1
                               xi = xi−1 −    hi,j ∇f (xj ),   1 ≤ i ≤ N,                        (47)
                                           L
                                              j=0

with stepsizes {hi,j }0≤j<i≤N fixed in advance, independently of f . We rate a method by its worst-
case function-value suboptimality after N steps, relative to the initial suboptimality. Since Fµ,L
is invariant under translations of the variable and shifts of the function value, we set x⋆ = 0 and

                                                    64
f⋆ = 0. Optimality conditions give ∇f (x⋆ ) = 0, and we normalize the initial gap by f (x0 ) − f⋆ ≤ 1.
The worst-case performance of M ∈ MN is
                                                                               
                            maximize f (xN ) − f⋆
                          subject to f ∈ Fµ,L ,                                
                                                                               
                R(M ) =                {xi }1≤i≤N generated from x0 by M,                     (Ofin )
                                                                                ,
                                        f (x0 ) − f⋆ ≤ 1,                      
                                         x⋆ = 0, f⋆ = 0, ∇f (x⋆ ) = 0
where the decision variables are the function f and the iterates x0 , . . . , xN . The optimal FSFOM
  ⋆ ∈ M for this setup solves the outer design problem R⋆ (M ) = min
MN       N                                                       N              M ∈MN R(M ) of (1).

Following [62], the derivation passes to a transformed function. By scale invariance [65, §3.5] fix
L = 1, so µ = q. For f ∈ Fq,1 with x⋆ = 0, f⋆ = 0, the shifted function f˜ ≜ f − (q/2) k·k2 belongs
to F0,1−q , with gradients g̃i = ∇f (xi ) − q xi and g̃⋆ = 0; the original suboptimality is recovered
from the transformed values f˜i = f˜(xi ) through
                                         f (xi ) − f⋆ = f˜i + 2q kxi k2 .                                  (48)
Re-expressing (47) through g̃i , the iterates take the form
                                      X
                                       i−1          X
                                                     i−1
                            xi = 1 − q     αi,j x0 −     αi,j g̃j ,         1 ≤ i ≤ N,                     (49)
                                         j=0              j=0

where the transformed stepsizes {αi,j }0≤j<i≤N are defined from the original stepsizes {hi,j }0≤j<i≤N
through the triangular (hence invertible) system of equations [62, §3.2] αi,i−1 = hi,i−1 and αi,j =
                  X
                  i−1
hi,j + αi−1,j − q     hi,k αk,j , for 0 ≤ j ≤ i − 2. The transformed function obeys (6). We impose
                  k=j+1
these smooth-convex interpolation inequalities at the sampled iterates, with 1 − q in place of L.
Collect the data into P = [ x0 | g̃0 | · · · | g̃N ] ∈ R d×(N +2) , G = P ⊤ P ∈ S+N +2
                                                                                       , and F = [ f˜0 | · · · |
f˜N ]. With the selectors x0 = e1 , gi = ei+2 (so g̃i = P gi ), fi = ei+1 , x⋆ = g⋆ = 0, and f⋆ = 0, define
the iterate selectors by mirroring the coeﬀicients of (49),
                                     X
                                      i−1          X
                                                    i−1
                           xi ≜ 1 − q     αi,j x0 −     αi,j gj ,           1 ≤ i ≤ N,                     (50)
                                         j=0              j=0

so that xi = P xi by (49), and define Ai,j (α), Bi,j (α), and Ci,j for i, j ∈ IN
                                                                               ⋆ exactly as in (30).


By (50) xi is aﬀine in α, so Ai,j is aﬀine and Bi,j quadratic in α, while Ci,j is constant. By
(48) the objective is f (xN ) − f⋆ = F fN + (q/2)tr(GBN,⋆ ) and the initial gap is f (x0 ) − f⋆ =
F f0 + (q/2)tr(GB0,⋆ ). Under the large-scale assumption d ≥ N + 2 (Assumption 1) the rank
constraint on G is vacuous, and (Ofin ) relaxes to the convex SDP
                                                                                                 
          maximize F fN + 2q trGBN,⋆
         subject to                                                                              
                                                                                               
R(M ) =                                                                                          
         F (fj − fi ) + trG Ai,j (α) + 2(1−q) Ci,j ≤ 0, i, j ∈ IN : i 6= j, ▷ dual var. λi,j ≥ 0  ,
                                           1                     ⋆
         F f0 + q trGB0,⋆ ≤ 1, ▷ dual var. ν ≥ 0                                                 
                 2
          G  0, ▷ dual var. Z  0

                                                       65
with decision variables F ∈ R 1×(N +1) and G ∈ S N +2 , and the indicated dual variables. Taking the
dual gives
                                                                                       
                      minimize ν
                   subject to                                                          
                                                                                       
                   f −νf +P             ⋆ :i̸=j λi,j (fi − fj ) = 0,
                                                                                        
         R(M ) =  N         0      i,j∈IN     P                                     ,      (51)
                   q                                                                   
                   2 νB0,⋆ − BN,⋆ (α) + i,j∈I ⋆ :i̸=j λi,j Ai,j (α) + 2(1−q)
                                                                            1
                                                                              Ci,j = Z, 
                                                        N
                      Z  0, ν ≥ 0, λi,j ≥ 0 (i, j ∈ IN         ⋆ : i 6= j)


with decision variables ν ∈ R, λ = {λi,j }, and Z ∈ S N +2 . By weak duality, we have R(M ) ≤ R(M ).
The derivation then recasts the outer problem, in the design variable α, as a QCQP in exact parallel
with (33): it substitutes (51) for the inner problem, adjoins {αi,j }0≤j<i≤N to the decision variables
ν, λ, and Z, and replaces the constraint Z  0 with the Cholesky factorization Z = V V ⊤ , where
V is lower triangular with nonnegative diagonal again [26, Corollary 7.2.9]. Every constraint of the
resulting problem is at most quadratic in its decision variables; upon user approval of the derivation,
bnb-pep-skill solves the problem numerically. The reformulation presumes strong duality between
the inner SDP and its dual (51), the analogue of Assumption 2; weak duality alone already makes
its optimal value an upper bound on R⋆ (MN ).
In Stage 2 of the pipeline, the frontier-llm-consult skill fitted symbolic expressions to the numerical
solutions of this QCQP, yielding analytic formulas for the transformed stepsizes and an analytic
feasible point of the inner dual (51), expressed in terms of the geometric construction of Lemma 4 (at
L = 1, hence µ = q); dual feasibility alone already certifies the contraction bound. The consultation
then recast the method from the transformed-stepsize representation into the momentum form
(ITEM-f) in which Section 4.2 presents it. From the multipliers of this feasible point, continued
consultation produced the Lyapunov proof of Theorem 3 presented in Section 4.2.1, stated on the
momentum form, and Section 4.2.4 describes the Lean coverage of the presented results.




                                                  66
