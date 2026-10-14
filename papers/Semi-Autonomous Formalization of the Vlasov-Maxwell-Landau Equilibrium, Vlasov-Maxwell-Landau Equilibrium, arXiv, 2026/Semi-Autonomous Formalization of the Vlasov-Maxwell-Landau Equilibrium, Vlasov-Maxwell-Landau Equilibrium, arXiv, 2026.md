                                                                Semi-Autonomous Formalization of the
                                                                 Vlasov-Maxwell-Landau Equilibrium
                                                                                          Vasily Ilin∗

                                                                                         March 2026
arXiv:2603.15929v2 [cs.AI] 31 Mar 2026




                                                                                           Abstract
                                                   We present a complete Lean 4 formalization of the equilibrium characterization in the
                                               Vlasov-Maxwell-Landau (VML) system, which describes the motion of charged plasma. The
                                               project demonstrates the full AI-assisted mathematical research loop: an AI reasoning model
                                               (Gemini DeepThink) generated the proof from a conjecture, an agentic coding tool (Claude
                                               Code) translated it into Lean from natural-language prompts, a specialized prover (Aristotle)
                                               closed 111 lemmas, and the Lean kernel verified the result. A single mathematician supervised
                                               the process over 10 days at a cost of $200, writing zero lines of code.
                                                   The entire development process is public: all 229 human prompts, and 213 git commits are
                                               archived in the repository. We report detailed lessons on AI failure modes – hypothesis creep,
                                               definition-alignment bugs, agent avoidance behaviors – and on what worked: the abstract/con-
                                               crete proof split, adversarial self-review, and the critical role of human review of key definitions
                                               and theorem statements. Notably, the formalization was completed before the final draft of the
                                               corresponding math paper was finished.



                                         1    Introduction
                                         Formal verification of mathematics in proof assistants like Lean 4 [de Moura and Ullrich, 2021,
                                         The mathlib Community, 2020] has traditionally required deep expertise in both the mathematics
                                         and the proof assistant itself. The learning curve is steep: even experienced mathematicians re-
                                         port months of effort to formalize results that take pages to prove on paper [Urban, 2026]. This
                                         bottleneck has limited formal verification to a small community of specialists.
                                             Recent advances in AI-assisted theorem proving are changing this landscape rapidly (Figure 1).
                                         Large language models can now generate Lean tactics [Chen et al., 2025], agentic coding tools can
                                         manage entire Lean projects [Liu et al., 2026], and cloud-based automated theorem provers can
                                         close individual lemmas without human intervention [Achim et al., 2025].
                                             Yet most published work on AI-assisted formalization focuses on competition mathematics
                                         (IMO, Putnam) or textbook results. Recent breakthroughs include AxiomProver autonomously
                                         generating a formal Lean proof of Fel’s open conjecture [Chen et al., 2026c] from a natural-
                                         language problem statement alone, GPT-5.2 generating informal proofs of open Erdős problems
                                         that were then auto-formalized in Lean by Aristotle [Sothanaphan, 2026], and Google DeepMind’s
                                         Aletheia agent [Feng et al., 2026b,a] autonomously producing research papers in natural language.
                                         Liu et al. [2026] formalized effective Brascamp-Lieb inequalities (∼8K lines) with human experts
                                            ∗
                                              University of Washington. Email: vilin@uw.edu. Repository: https://github.com/Vilin97/aristotle/tree/
                                         landau.


                                                                                                1
Project                          Prover   LOC New thm New defs Team     AI role      Logs     Domain
Gauss [Math, Inc., 2026]           Lean 4 181K‡   ✗       ✗     6+§    sorry elim.    ✗      Geometry
Bayer & David [Bayer et al., 2025] Isabelle 20K   ✓       ✓      15       none        ✗     Num. theory
This work                          Lean 4 10K     ✓       ✓      1      all code      ✓     Math. phys.
Numina [Liu et al., 2026]          Lean 4 ∼8K     ✓       ✓      13      collab.      ✗       Analysis
AxiomProver [Chen et al., 2026b] Lean 4 4.3K      ✓       ∼      21   fully auton.    ✗     Num. theory
AxiomProver [Chen et al., 2026c] Lean 4 2.7K      ✓       ∼      21   fully auton.    ✗       Algebra
2HDM [Tooby-Smith, 2026]           Lean 4 1.6K    ✗†      ✓      1      minimal       ✗       Physics
Aristotle [Sothanaphan, 2026]      Lean 4 1.4K    ✓       ✗      1    fully auton.    ✗       Combin.
AxiomProver [Chen et al., 2026a] Lean 4 0.2K      ✓       ∼       5   fully auton.    ✗      Alg. geom.

Table 1: Recent research-level formalizations with publicly available code, sorted by LOC. “New
thm” = theorem previously unpublished. “New defs” = required definitions or theory not in the
proof library (✓ = substantial, ∼ = lightweight, ✗ = none). “AI role”: sorry elim. = eliminated
sorry’s in human-written scaffold; all code = AI generated all proof-assistant code from NL prompts;
collab. = human-AI pair programming; fully auton. = AI from NL problem statement alone. “Logs”
= full development process public (all commits, prompts, and interaction logs). † Discovered an
error in the published proof. ‡ ∼22K lines (definitions, statements) written by human experts;
Gauss eliminated ∼160K lines of sorry’s in 3 weeks. § No paper; 6+ named contributors on blog
post.


collaborating on the Lean code, and Bayer et al. [2025] formalized their own new theorem in
Isabelle in parallel with the mathematical research, writing the proof assistant code themselves.
    Our work is distinguished not by full autonomy – AxiomProver’s Fel’s conjecture result is more
autonomous – but by the combination of several features that, to our knowledge, no single prior
project shares (Table 1):
  • Scale and depth. 34 files and 10K+ lines of Lean, in hard analysis: Coulomb singularity
    cancellation, Leibniz integral rule, energy methods on the torus.
  • New theory. The theorem cannot even be stated with existing Mathlib – the Landau
    operator, torus differential structure, and VML system had to be defined from scratch.
  • New result. The characterization of smooth steady states of the full VML system with
    Coulomb collisions and electromagnetic coupling does not appear in the prior literature in this
    precise form and is, to our knowledge, new as a stated and proved result.
  • Fully documented process. A single mathematician wrote zero code while actively steering
    the formalization over 10 days; every prompt, commit, and tool call is public.
   The contributions are:
 1. A demonstration of the full AI-assisted mathematical research loop: from an open conjecture,
    through AI-generated resolution and detailed proof (Gemini DeepThink, requiring no mathe-
    matical corrections), to a complete machine-verified formalization (Claude Code + Aristotle)
    – all with the human acting solely as supervisor. To our knowledge, this is the first project to
    close this entire pipeline on a research-level result in hard analysis.

 2. A complete Lean 4 formalization of a new theorem in mathematical physics (the VML steady-
    state characterization), verified with zero sorry’s.

 3. A detailed, fully transparent account of the process: every prompt, every commit, every tool
    call is public.

                                                  2
Figure 1: ArXiv papers using Lean for formalization, by year. Data from the arXiv metadata
snapshot (March 2026), filtered for references to the Lean theorem prover.


 4. Lessons learned about the capabilities and failure modes of current AI tools for formalization,
    including a definition-alignment bug caught by an expert reviewer post-completion.
 5. Evidence that research-level formalization is now accessible to mathematicians without deep
    Lean expertise, at minimal cost ($200 subscription + $0 for Aristotle and Gemini).


2     The Theorem
2.1   The Physical System
The Vlasov-Maxwell-Landau (VML) system is a system of PDEs modeling the dynamics of a
charged plasma. The full time-dependent system evolves a particle distribution function f (t, x, v),
an electric field E(t, x), and a magnetic field B(t, x) via the Vlasov equation coupled to Maxwell’s
equations with the Landau collision operator.
    We are interested in steady states: solutions with no time dependence. Setting all time deriva-
tives to zero, the unknowns reduce to f (x, v) > 0 on T3 × R3 , E(x), and B(x), and the system
becomes:
                          v · ∇x f + (E + v × B) · ∇v f = ν Q(f, f ),                            (1)
                                                              Z
                                               ∇×B =J =            v f dv,                       (2)
                                                          Z    R3

                                                 ∇·E =       f dv − ρion ,                       (3)
                                                           R3
                                                 ∇ · B = 0,                                      (4)
where Q(f, f ) is the Landau collision operator with the Coulomb kernel Ψ(r) = r−3 . Note that
Faraday’s law ∂t B = −∇ × E becomes ∇ × E = 0 at equilibrium; this is not listed as a hypothesis
because it is derived in the proof (it follows from the other equations).

2.2   Main Result
Theorem 1 (Informal; see Ilin and Hu [2026] for the complete proof). Let f > 0 be a smooth
steady-state solution of the VML system with Coulomb collisions on T3 = (R/Z)3 , with Schwartz-

                                                 3
  theorem CoulombConcreteTheorem42
      (f : Torus3 → (Fin 3 → R) → R)
      (E B : Torus3 → Fin 3 → R)
      (ν ρ_ion : R)
      (hν : 0 < ν)                                                 -- (1)
      (hρ_ion : 0 < ρ_ion)                                         -- (2)
      (hf_pos : ∀ x v, 0 < f x v)                                 -- (3)
      (hf_smooth_v : ∀ x, ContDiff R 3 (f x))                      -- (4)
      (hf_smooth_x : ∀ v, ContDiff R 2
        (periodicLift (fun x => f x v)))                            -- (5)
      (hB_smooth : ∀ i, ContDiff R 2
        (periodicLift (fun x => B x i)))                            -- (6)
      (hSchwartz : UniformSchwartzDecay f)                          -- (7)
      (hGradBound : ∃ (Cg : R) (Kg : N),
        ∀ (x : Torus3) (v : Fin 3 → R) (i : Fin 3),
        |fderiv R (f x) v (Pi.single i 1)|
          ≤ Cg * (1 + ∥v∥) ^ Kg * f x v)                          -- (8)
      (hVlasov : ∀ x v,
        dotProduct v (torusGradX (fun y => f y v) x) +
        dotProduct (E x + cross v (B x)) (vGrad (f x) v) =
        ν * LandauOperator coulombKernel (f x) v)                   -- (9)
      (hAmpere : ∀ x,             R
        torusCurlX B x = fun i =>   v, v i * f x v)               -- (10)
      (hGauss : ∀ x,     R
        torusDivX E x = ( v, f x v) - ρ_ion)                      -- (11)
      (hDivB : ∀ x, torusDivX B x = 0)                            -- (12)
      :
      ∃ (T_eq : R) (B0 : Fin 3 → R), 0 < T_eq ∧
      (∀ x v, f x v = equilibriumMaxwellian ρ_ion T_eq v) ∧
      (∀ x, E x = 0) ∧
      (∀ x, B x = B0 )


Figure 2: The formal Lean 4 statement of the main theorem (CoulombConcreteTheorem42). The
proof (omitted) is 80 lines of tactic invocations that assemble the seven-step argument described
in Section 2.3. Here Torus3 is Fin 3 → AddCircle 1, periodicLift lifts torus functions to R3 for
differentiation, and equilibriumMaxwellian is the Maxwellian ρion /(2πT )3/2 exp(−|v|2 /2T ).


class velocity decay and a polynomial log-growth bound. Then:
                                                                            2
                                                       ρion
                                                               exp − |v|
                                                                                
  1. f is a spatially uniform Maxwellian: f (x, v) = (2πT )3/2        2T            for some T > 0;

  2. the electric field vanishes: E(x) = 0;

  3. the magnetic field is constant: B(x) = B0 .

    The formal Lean statement is shown in Figure 2. It takes 12 hypotheses, all with clear physical
meaning: 2 physical parameters (ν > 0, ρion > 0), strict positivity of f , smoothness conditions (C 3
in velocity, C 2 in space via periodic lift, C 2 for B), Schwartz-class velocity decay, a polynomial score
bound (|∂vi f | ≤ C(1 + ∥v∥)K f ), and the four steady-state equations (1) – (4). The polynomial
score bound is a genuine assumption not derivable from Schwartz decay alone; it is satisfied by
Maxwellians and physically reasonable perturbations. A 13th hypothesis – a polynomial log-growth
bound (| log f (x, v)| ≤ C(1 + ∥v∥)K ) – is derived from the score bound and smoothness inside the
proof.


                                                    4
2.3   Proof Architecture
The proof follows a classical entropy method in seven steps (Figure 3):

 1. H-theorem: Entropy dissipation D(f ) ≤ 0; the Landau matrix is positive semi-definite.

 2. Nullspace: D(f ) = 0 implies f is a local Maxwellian: log f (x, v) = a(x) + b(x) · v + c(x)|v|2 .

 3. Transport: Substituting into the Vlasov equation yields a polynomial in v that must vanish
    identically.

 4. Polynomial matching: The O(|v|3 ) terms force ∇c = 0 (constant temperature); the O(|v|2 )
    terms yield Killing’s equation for b.

 5. Killing’s equation: On the flat torus, the only smooth Killing fields are constants, so b = b0 .

 6. Maximum principle: Ampère’s law forces b0 = 0; Gauss’s law forces E = 0 and uniform
    density.

 7. Harmonic analysis: With J = 0, curl B = 0 and div B = 0 imply B is harmonic on T3 ,
    hence constant.


3     Tools
The project used four AI systems, none of which required any Lean code to be written by hand.

Claude Code (Anthropic). An agentic coding tool that operates in the terminal, with access
to file reading/editing, shell commands, and MCP (Model Context Protocol) integrations. Claude
Code was the primary workhorse: it generated all Lean code, managed the project structure, ran
diagnostics via the Lean LSP, and orchestrated submissions to Aristotle. The subscription costs
$200/month (Claude Max plan).

Gemini DeepThink (Google DeepMind). A mathematical reasoning model accessed via MCP.
Gemini generated the initial natural-language proof of the theorem in a five-turn dialogue, identified
the relevant literature, and was consulted during the project for planning decisions (e.g., choosing
the torus representation).

Aristotle (Harmonic). A cloud-based automated theorem prover for Lean 4 [Achim et al., 2025].
Lemma statements were extracted from the project, submitted via a Python script, and results were
automatically integrated. Aristotle proved 111 lemmas, disproved 28 false conjectures, and returned
66 with sorry’s still present. The service was free during the project period.

Lean LSP tools. The Lean Language Server Protocol, accessed via MCP, provided real-time
compilation feedback, goal-state inspection, tactic suggestions, and library search (LeanSearch,
Loogle). These tools generated 3,194 calls over the project.




                                                  5
Figure 3: Proof dependency graph, generated with LeanBlueprint [Massot, 2020]. All nodes are
green (fully proved). The graph flows from primitive definitions (normSq, eucNorm, landauMatrix)
at the top through intermediate results (H theorem, D zero implies maxwellian, the field and con-
servation lemmas) down to theorem42 and its concrete Coulomb instantiation coulomb concrete
at the bottom. An interactive version is available in the repository.

4     Process
4.1   Timeline
The project unfolded over 10 days of active development (March 1 – 10, 2026), preceded by the
Gemini DeepThink session on February 28. Table 2 summarizes the key milestones.

4.2   Phase 1: Natural-Language Proof (Feb 28)
The project began with a question posed to Gemini DeepThink:
      “What is known about the equilibrium of the Vlasov-Maxwell-Landau equations with
      Coulomb collisions, and a single species? Does it have to be a global Maxwellian? With
      what covariance? How is it shown?”
    Gemini produced a detailed six-step proof, identified the relevant literature [Villani, 2002, Cer-
cignani et al., 1994, Guo, 2003, 2012, Desvillettes and Villani, 2005], and refined the argument over

                                                  6
          Date     Event                                                          Sorry count
          Feb 28   Gemini generates natural-language proof                        –
          Mar 1    First Lean code committed (monolithic file)                    ∼25
          Mar 2    First Aristotle submissions; hypothesis creep begins           25
          Mar 3    File split into main/ directory; Aristotle results arrive      25 → 7
          Mar 5    Concrete torus representation chosen (with Gemini)             7 + 22
          Mar 7    Abstract theorem reaches 0 sorry’s                             0
          Mar 7    /critique adversarial review introduced                        0
          Mar 8    /babysit automation loop created (1:09 AM)                     0
          Mar 8    Coulomb kernel instantiation begun; university server online   +35
          Mar 9    Coulomb theorem reaches 0 sorry’s (11:15 PM)                   0
          Mar 10   Cleanup (−3K lines); non-vacuousness theorem                   0

                      Table 2: Project timeline and sorry count evolution.


five turns. Crucially, the proof required no mathematical corrections: the mathematician verified
the argument by hand and found it complete and correct, needing only the identification of exact
supporting theorems from the cited papers. The final natural-language proof became the blueprint
for the formalization.

4.3   Phase 2: Scaffolding (Mar 1 – 2)
The formalization prompt was:

      “Look at H-theorem-formal.tex. I want to formalize that the steady state of the VML.”

    Claude Code generated a monolithic 1,000+ line Lean file within hours, with sorry’s marking
every gap. Claude estimated the full formalization would require “multiple months.” The math-
ematician’s role was to reject false paths and enforce design principles, particularly hypothesis
discipline:

      “You keep doing the same thing – adding hypotheses that are actually lemmas to be
      proven! Why do you do that?” (Mar 2)

   This became the project’s central methodological principle, codified in CLAUDE.md: a sorry (an
acknowledged gap) is preferable to an unnecessary hypothesis (which silently weakens the theorem).

4.4   Phase 3: Abstract Proof Chain (Mar 3 – 7)
The monolithic file was split into a main/ directory with separate files for each section of the
proof. A FlatTorus3 typeclass abstracted the spatial domain, specifying integration by parts,
curl/divergence identities, a maximum principle, and constancy of harmonic functions – without
fixing a particular manifold. The mathematical argument (Sections 2 – 8) was formalized against
this interface.
    A concrete TorusInstance module proved that T3 = (R/Z)3 satisfies all 22 fields of FlatTorus3,
using the Mathlib representation Fin 3 → AddCircle 1. The representation was chosen in consul-
tation with Gemini. Periodicity is automatic: functions on the torus factor through the quotient
map R → R/Z.
    By March 7, all sorry’s in the abstract proof chain were closed – the abstract theorem was
fully proved.

                                                  7
4.5   Phase 4: Automation (Mar 7 – 8)
On March 7, an adversarial self-review process was introduced:

      “You are a hostile reviewer trying to REJECT this formalization. Your job is to find
      every weakness, gap, and dishonesty.”

    The output, critique.md, identified false hypotheses, unnecessary assumptions, and dead code.
On March 8 at 1:09 AM, the automation suite was created in a 20-minute session. The initial
/babysit loop combined four slash commands (/critique, /prove, /check-aristotle, /cleanup)
and was set to run on a 10-minute timer. Over the following days, the loop was iteratively expanded
to 11 steps – adding /plan, /simplify, /strengthen, /submit-aristotle, /log, /commit, and
/alert (Telegram notifications) – and executed 122 documented cycles over the project.

4.6   Phase 5: Coulomb Kernel (Mar 8 – 9)
With the abstract theorem proved, the final challenge was instantiating it for the physical Coulomb
kernel Ψ(r) = r−3 . This required proving that the Landau collision operator satisfies all 17 inte-
grability, differentiability, and continuity conditions in the VelocityDecayConditions bundle.
    The Coulomb singularity at r = 0 makes |Aij (z)| ∼ ∥z∥−1 , which is barely integrable in R3 .
Each integrability proof required decomposing the domain into a ball around the origin (handled
by local integrability of ∥z∥−1 ) and the complement (handled by Schwartz decay). This phase was
the hardest part of the formalization, producing ∼4,000 lines of analytical estimates.
    A university server was brought online on March 8 to run /babysit loops concurrently with
the local machine, enabling continuous progress. The sorry count dropped from 35 to 0 on March
9, with the last sorry closed at 11:15 PM.

4.7   Phase 6: Cleanup (Mar 10)
With zero sorry’s achieved, the /babysit loop shifted to code quality: removing dead code (−3K
lines), eliminating unnecessary maxHeartbeats overrides, and re-enabling linters. A separate non-
vacuousness theorem (CoulombConcreteTheorem42 nonvacuous) verified that the 12 hypotheses
are satisfiable – the equilibrium Maxwellian with E = 0, B = 0 witnesses all conditions. This
sanity check was suggested independently by expert reviewers on the Lean Zulip.


5     Statistics
Table 3 summarizes the project. The 2.8 billion input tokens are dominated by cache reads of
the Lean codebase and Mathlib context – the 254:1 input-to-output ratio reflects the read-
heavy nature of formal verification. At Opus 4 API pricing with prompt caching, this would cost
approximately $6,300: $4,071 in cache reads ($1.50/M), $1,401 in cache creation ($18.75/M), $826
in output ($75/M), and $6 in fresh input ($15/M). Without prompt caching, the same workload
would cost ∼$42,700 – caching saves 85%. The mathematician paid only $200 for the Claude Max
subscription, which provides generous usage.
    The development trajectory is shown in Figures 4 and 5: the sorry count follows a sawtooth
pattern as scaffolding and proving alternate, while the LOC history shows the four-phase structure
of the project. Figure 11 reveals that roughly half of the final codebase is supporting infrastructure
– definitions, the torus instance, Coulomb kernel integrability files, and decay helpers – rather than
the core proof chain. This reflects the substantial gap between Mathlib’s current coverage and the

                                                  8
                Metric                                                         Value
                Lean 4 files                                                       34
                Lines of code                                                 10,445
                Theorems                                                           39
                Lemmas                                                           186
                Definitions                                                        28
                sorry’s                                                             0
                Development period                                           10 days
                Git commits                                                      213
                Claude Code sessions                         32 (across 2 machines)
                Human prompts (excl. slash commands)                             229
                /babysit cycles                                                  122
                Assistant turns                                               27,186
                Tool calls                                                    17,334
                Tokens consumed (input)                                   2.8 billion
                Tokens consumed (output)                                  11 million
                Input-to-output ratio                                          254:1
                Aristotle submissions                                            220
                  Proved                                                  111 (50%)
                  Disproved                                                28 (13%)
                  Returned with sorry                                      66 (30%)
                  Failed                                                    15 (7%)

Table 3: Project statistics. The 229 human prompts exclude bare slash commands like /babysit;
all are archived with timestamps. The mathematician estimates ∼50 hours of active supervision
over 10 days.


background material needed for research-level mathematical physics: the Landau operator, torus
differential calculus, Schwartz decay machinery, and Coulomb singularity estimates all had to be
built from scratch. Figure 6 shows session activity across two machines, with near-round-the-clock
coverage during the final sprint. Figure 7 breaks down token consumption, revealing the 254:1
input-to-output ratio characteristic of formal verification. Figure 8 summarizes tool usage across
17,334 invocations, and Figure 9 shows the outcomes of 220 Aristotle submissions.


6     Lessons Learned
6.1   Hypothesis Discipline is Critical
The most persistent failure mode of Claude Code was hypothesis creep: when faced with a difficult
lemma, the agent’s default behavior was to assume it as a hypothesis of the main theorem rather
than prove it. By March 4, the main theorem had accumulated 42 hypotheses – most of which
should have been derived lemmas.
   This failure mode is insidious because it is syntactically valid: the Lean code compiles, the sorry
count stays low, and the proof “works.” But the theorem statement is progressively weakened. In
the extreme case, one could “prove” any theorem by assuming its conclusion as a hypothesis.
   The fix required persistent human intervention:



                                                  9
Figure 4: Sorry count in main/ over time (85 commits). The sawtooth pattern reflects alternating
phases of scaffolding (sorry’s accumulate) and proving campaigns (sorry’s eliminated). Key events:
peak 25 on Mar 2 (abstract proof chain stated); Aristotle drops count from 25→7 on Mar 3; first
0 sorry’s on Mar 7 (abstract theorem proved); +35 sorry’s on Mar 8 (Coulomb kernel instantia-
tion begun); 35→0 sprint on Mar 9; brief +1 on Mar 10 (non-vacuousness theorem, immediately
resolved).


      “I have told you time and again to keep the hypotheses to Theorem42 minimal. If you
      need a mathematical fact, it should be a lemma with a sorry, not a hypothesis!” (Mar
      3)

    This was codified in CLAUDE.md: “The goal is not to end up with 0 sorry’s! The goal is to
make an honest formalization of the main theorem, with only the genuinely needed mathemati-
cal/physical assumptions.” The 42 hypotheses were systematically reduced: velocity-space decay
conditions were bundled into a single VelocityDecayConditions structure (replacing 15 scattered
hypotheses), and regularity facts like continuity of the density ρ were derived inside the proof from
domination bounds. The final concrete theorem has 12 hypotheses, all physically meaningful.

6.2   Aristotle is Transformative
The cloud-based theorem prover Aristotle [Achim et al., 2025] was the single most impactful tool
after Claude Code itself. Of 220 submissions, 111 were proved outright (50%), and 28 were disproved
– Aristotle found counterexamples or proved the negation.
    The disproved statements were arguably more valuable than the proved ones. They caught false
conjectures early: missing measurability hypotheses, claims that fail on pathological counterexam-
ples (e.g., Vitali sets), and Schwartz decay estimates that are actually false for the Coulomb kernel.
The fix-and-resubmit cycle served as the primary mechanism for catching bugs in the formalization.
    Aristotle’s overall median turnaround was 19 minutes (Figure 10). Proved lemmas returned in
a median of 9 minutes; disproved statements took 29 minutes (counterexample construction); but
submissions returned with sorry had a median of 5.6 hours, as Aristotle exhausted its time budget
searching before giving up. We recommend decomposing proofs aggressively into small lemmas and
submitting each to an automated prover – even lemmas that seem hard.



                                                 10
Figure 5: Lean lines of code over time (all 213 commits). The project progressed in four phases:
(1) Abstract proof chain (Mar 3 – 6), formalized against an abstract FlatTorus3 typeclass. (2)
Coulomb kernel analysis (Mar 7 – 9), handling the singularity at r = 0 – the sharp LOC increase
reflects ∼4K lines of analytical estimates. (3) Cleanup (Mar 10, early): ∼3K lines of dead code,
redundant lemmas, and unnecessary heartbeat overrides removed. (4) Non-vacuousness (Mar 10,
late): satisfiability of the 12 hypotheses.


6.3   Definition Alignment Requires Expert Review
After the formalization was announced on the Lean Zulip, Sébastien Gouëzel (a Mathlib maintainer)
immediately identified a definition-alignment bug: the original theorem used ContDiff R ⊤, which
in Mathlib means analytic, not C ∞ as intended. Neither the AI agent nor the mathematician
caught this during 10 days of development. Gouëzel remarked: “I find it a little bit worrisome that
AI can overlook such discrepancies – if there is one in the only line I’ve checked, how many others
are there?”
    The fix was straightforward – replacing ⊤ with explicit finite smoothness (C 3 in velocity, C 2
in space) – and the resulting theorem is actually stronger, since it assumes less. But the episode
illustrates a fundamental risk of AI-generated formalizations: the code compiles and the proof
checks, yet the theorem does not state what was intended. Gouëzel also suggested formalizing that
the equilibrium Maxwellian satisfies all 12 hypotheses (the non-vacuousness theorem), which was
implemented as an additional sanity check.
    This lesson is perhaps the most important for the community: compilation is not correct-
ness. Expert review of definitions and theorem statements remains essential, and cannot yet be
delegated to the AI.

6.4   Automation Helps but is Not Strictly Necessary
The /babysit loop (Section 4) ran for 122 cycles over the project. It was valuable for overnight
progress and for maintaining momentum on tedious tasks (linter cleanup, dead code removal).
However, the most important breakthroughs (closing the abstract theorem, proving the Coulomb


                                                11
Figure 6: Claude Code activity across two machines (local + university server). Top: messages
per hour (red = interactive human, orange = automated, blue = assistant). Bottom: hour-of-
day heatmap. The 27,186 assistant turns versus 229 human prompts give a 119:1 ratio, reflecting
the high autonomy of each /babysit cycle (typically 20 – 50 tool calls per invocation). The
heatmap shows near-round-the-clock activity on Mar 9 – 10 when both machines ran /babysit
loops concurrently.


integrability estimates) happened during interactive sessions with direct human guidance.
    The automation was most effective for:

  • Maintaining code quality: The adversarial /critique step caught issues that would oth-
    erwise accumulate (unused imports, stale comments, false docstrings).

  • Aristotle polling: Checking for completed Aristotle jobs and integrating results.

  • Overnight progress: Running unattended on two machines while the mathematician slept
    or traveled.

   It was less effective for:

  • Novel proof strategies: The agent often got stuck in loops, retrying the same failing ap-
    proach rather than reconsidering the proof strategy.

  • Architectural decisions: Choosing representations, structuring typeclasses, and deciding
    what to abstract required human judgment.

                                               12
Figure 7: Token consumption across the project. Top: cumulative input tokens (blue, 2.8B) and
output tokens (red, 11M). The 254:1 input-to-output ratio reflects the read-heavy nature of formal
verification – Claude reads far more context than it writes. Bottom: per-turn context size, showing
a sawtooth pattern as the context window fills to ∼175K tokens and resets at each of the 164
autocompacts (red vertical lines). Dense compaction clusters on Mar 6 – 10 correspond to the
intensive Coulomb kernel analysis and /babysit loop periods.


6.5   Gemini for Mathematical Reasoning
Gemini DeepThink served two distinct roles: (1) generating the initial proof blueprint, and (2)
providing mathematical advice during the formalization. For the first role, it was excellent – the
proof it produced (Section 4) served as the complete blueprint for the 10K-line formalization. For
the second role, it was useful but not essential: Claude Code’s own mathematical reasoning was
often sufficient for tactical decisions. In the mathematician’s own assessment: “I did not find
Gemini to be that terribly useful [beyond the initial proof ]. It was mostly for experimental sake.”
    The key insight is that the full loop of mathematical research – from conjecture to resolution
to detailed proof – can now be completed by AI with the human acting as verifier rather than
creator. Proof generation and proof formalization are different skills, and a model that excels at
informal mathematical reasoning (Gemini) can be productively combined with a model that excels
at code generation (Claude), with each handling its strength. The Lean kernel then provides the
final guarantee of correctness that neither model can offer alone.




                                                13
Figure 8: Tool usage across 17,334 invocations. Left: totals by category. The core editing loop
dominates – Bash (3,975), Read (3,416), Edit (2,495), Grep (1,701), Write (900) – reflecting the
iterative nature of formal verification. Lean LSP tools (3,194 combined) provided real-time feed-
back. Right: daily breakdown showing the ramp-up from exploratory work (Feb 28 – Mar 2)
through peak activity (Mar 6 – 10) when both machines ran /babysit loops concurrently.


6.6   The Agent Gets “Lazy”
Beyond hypothesis creep, Claude Code exhibited several avoidance behaviors:

  • Premature sorry: Marking a goal as sorry and moving on, rather than attempting the
    proof.

  • Excessive heartbeats: Setting maxHeartbeats 800000 to suppress timeouts rather than
    simplifying the proof.

  • Dead code accumulation: Leaving unused lemmas, commented-out code, and stale helper
    definitions rather than cleaning up.

  • Over-engineering: Creating unnecessary abstraction layers, helper functions, and interme-
    diate definitions when a direct proof would suffice.

  • No-op cycles: During automated /babysit runs, the agent would sometimes complete a cycle
    with no meaningful changes despite open issues in critique.md, requiring prompt rewrites to
    enforce progress.

   These behaviors are not bugs per se – they are rational strategies for an agent optimizing for
compilation success rather than proof quality. The fix is explicit instructions (CLAUDE.md) and
persistent human supervision. The adversarial /critique step in the /babysit loop partially
automated this supervision.

6.7   The Abstract/Concrete Split Pays Off
Separating the proof into an abstract framework (FlatTorus3 typeclass) and a concrete instanti-
ation (TorusInstance) was an early design decision that paid dividends throughout. When the
torus proofs required rewrites – removing false hypotheses, changing the representation of spatial


                                               14
Figure 9: Outcomes of 220 Aristotle submissions. Aristotle proved 111 lemmas cleanly (50%),
disproved 28 false statements (13%), returned 66 with sorry’s still present (30%), and 15 failed
or were never started (7%). The disproved statements were particularly valuable – they caught
false conjectures early (e.g., missing measurability hypotheses, Vitali-set counterexamples, incorrect
Schwartz decay estimates for the Coulomb kernel). The stacked bar chart shows peak submission
activity on Mar 2 (57 jobs) and Mar 6 (45 jobs).

differentiability – the abstract proof chain (Sections 2 – 8) was completely unaffected. This sepa-
ration of concerns is standard software engineering practice, but it is not the default behavior of
the AI agent, which tends to produce monolithic proofs.

6.8   No Lean Code Required
The mathematician wrote zero lines of Lean code and zero lines of any other programming lan-
guage. All Lean code was generated by Claude Code from natural-language prompts. Of the 229
human prompts sent to Claude Code (excluding bare slash commands and context continuations),
most were short directives or confirmations. The mathematician estimates approximately 50 hours
of active supervision – an average of 5 hours per day watching Claude Code work in real time.
    The mathematician’s contributions were:
 1. Posing the conjecture.
 2. Checking the final theorem statement (12 hypotheses, each evaluated for physical correctness).
 3. Enforcing hypothesis discipline and architectural decisions.
 4. Providing mathematical intuition when the agent was stuck.
 5. Designing and iterating on the automation suite.
   The mathematician did read key definitions and theorem statements in Lean to verify alignment
with the intended mathematics, but did not debug proofs or lemma statements directly.


7     Related Work
Table 1 compares recent research-level formalizations with publicly available code.

                                                 15
Figure 10: Aristotle turnaround times for 214 submissions, colored by outcome. Left: histogram.
Proved lemmas (green) cluster in the first bins (median 9 minutes), while “returned with sorry”
(red) dominates the long tail. Right: median turnaround by category. The overall median was
19 minutes. Disproved statements took 29 minutes (counterexample construction); submissions
returned with sorry took a median of 5.6 hours – Aristotle exhausts its time budget before giving
up.


AI-assisted theorem proving. Seed-Prover [Chen et al., 2025] achieves state-of-the-art results
on competition mathematics using reinforcement learning with Lean feedback. Harmonic’s Aris-
totle [Achim et al., 2025] achieved gold-medal performance on the 2025 IMO and auto-formalized
GPT-5.2-generated proofs of open Erdős problems in Lean [Sothanaphan, 2026]. Google Deep-
Mind’s Aletheia agent [Feng et al., 2026b,a] autonomously produced research papers in natural
language, including solutions to four open Erdős conjectures. AxiomProver autonomously gener-
ated formal Lean proofs of Fel’s open conjecture [Chen et al., 2026c], a result on partial regu-
larity of primes [Chen et al., 2026b], and parity of k-differentials [Chen et al., 2026a] – all from
natural-language problem statements with zero human guidance. Unlike our work, these systems
are specialized for theorem proving, and the formalized results are typically short combinatorial
or algebraic arguments rather than large-scale formalizations requiring hard analysis (Coulomb
singularity estimates, PDE energy methods).

Agentic formalization. Numina-Lean-Agent [Liu et al., 2026] combines Claude Code with MCP
tools and formalized effective Brascamp-Lieb inequalities (∼8K lines) with two human experts
collaborating on the Lean code. Archon [FrenzyMath, 2025] uses a dual-agent architecture and
demonstrated full automation of FirstProof problems. Bayer et al. [2025] formalized their own
new theorem on Diophantine complexity bounds in 20,000 lines of Isabelle in parallel with the
mathematical research – an “in-situ formalization” – with 13 student collaborators writing the
proof assistant code by hand and no AI assistance. Our work differs in that a single mathematician
wrote zero code of any kind: the mathematical proof was generated by Gemini, and all Lean code
was generated by Claude Code from natural-language prompts.

Large-scale autoformalization. Math.Inc’s Gauss agent [Math, Inc., 2026] eliminated ∼160K
lines of sorry’s in the sphere packing formalization (Viazovska’s Fields Medal-winning result) in
three weeks, growing the codebase from ∼22K to 181K lines. The theorem statements and defini-

                                                16
Figure 11: LOC by file group over time. Red shades are the mathematical proof chain (Sec-
tions 2–8, Theorem42, VMLInputDerive, CoulombConcreteTheorem42); blue shades are supporting
infrastructure (definitions, torus instance, Coulomb kernel integrability files, decay helpers). At
completion, infrastructure accounts for roughly half of the codebase – reflecting the substantial
gap between Mathlib’s current coverage and the background material needed for research-level
mathematical physics. The sharp blue growth on Mar 7–8 is the Coulomb kernel analysis (∼4K
lines of analytical estimates for the singularity at r = 0). The cleanup phase (Mar 10) primarily
removed blue infrastructure code, while the red proof chain remained stable.


tions had been written by a team of 6+ human experts; Gauss’s role was sorry elimination – filling in
proofs where the goal was unambiguous. Urban [2026] formalized 130,000 lines of Munkres’ topol-
ogy textbook in two weeks for ∼$100, using ChatGPT/Claude Sonnet with a fast proof checker
(Megalodon). Both projects are larger in scale but formalize known results; our work targets a new
theorem requiring new definitions.

Formalization in physics. Tooby-Smith [2026] formalized the stability of the two-Higgs-doublet-
model potential in Lean/PhysLean (1.6K lines), discovering an error in a widely cited 2006 paper
– an example of formalization catching bugs in published proofs. Unlike our work, this formalized
existing results with minimal AI assistance.

Transparency. A distinguishing feature of our work is full transparency. Systems like Seed-
Prover [Chen et al., 2025] are closed-source, and even open systems like Numina-Lean-Agent [Liu
et al., 2026] do not publish the complete interaction logs. We publish all 229 human prompts (with
timestamps), all 213 commits, the full Gemini dialogue, and the complete development log of all
122 /babysit cycles.


8    Limitations
Mathematical novelty. The theorem – that every smooth positive steady state of the full VML
system with Coulomb collisions on the torus must be a global Maxwellian – does not appear in


                                                 17
Figure 12: Lines of Lean code added and deleted per day. Most days are net-positive (new content),
with two exceptions: Mar 3 (monolithic file split into main/ – same code reorganized) and Mar 9 –
10 (cleanup phase removed ∼3K lines of dead code, redundant lemmas, and unnecessary heartbeat
overrides). Total: +21,783 added, −13,478 deleted, net +8,305 lines.


the literature as a stated and proved result. Each proof technique is individually classical: the
H-theorem and null-space characterization of the Landau operator are standard [Villani, 2002, Cer-
cignani, 1988]; the polynomial-matching argument that forces constant temperature and Killing’s
equation on the bulk velocity appears in Cercignani [1988] and Desvillettes and Villani [2005];
and the maximum-principle argument for the nonlinear Poisson–Boltzmann equation is textbook.
However, prior work assembles these ingredients only for simpler systems. Desvillettes and Villani
[2005] prove steady-state uniqueness for the spatially inhomogeneous Boltzmann equation without
electromagnetic fields (E = B = 0). Guo [2003, 2012] study the full VML and Vlasov–Poisson–
Landau systems but prove dynamical stability of small perturbations near an assumed Maxwellian,
embedding the relevant macroscopic constraints inside linearized energy estimates rather than stat-
ing static uniqueness as a standalone result. What is new is the complete static characterization
for the electromagnetically coupled system: the observation that the Lorentz force contributes only
O(|v|1 ) terms to the Vlasov equation for a local Maxwellian (because (v × B) · v = 0), so the
O(|v|3 ) and O(|v|2 ) constraints of Cercignani [1988] and Desvillettes and Villani [2005] carry over
unchanged; the Ampère-law integration argument that forces the bulk velocity to vanish; and the
closure via Gauss’s law with a neutralizing background. These steps are individually straightfor-
ward, but their assembly into a single self-contained proof for the full VML system appears to be
new; the complete proof is given in Ilin and Hu [2026].

Definition alignment. As discussed in Section 6, the definition-alignment bug that survived the
entire development process illustrates a broader risk: similar undetected misalignments in other
definitions (e.g., torusCurlX, LandauOperator) cannot be ruled out without a thorough expert
audit.

Reproducibility. The process depends on the specific capabilities of Claude Opus 4 (March
2026), Aristotle (March 2026), and Gemini (February 2026). These models are updated frequently;
the same process may yield different results with future or past model versions.

                                                 18
Cost. While the subscription cost was $200, the API-equivalent cost was ∼$6,300 (with prompt
caching) or ∼$42,700 (without). The gap between the subscription and API cost reflects the Claude
Max plan’s unlimited usage model. At API pricing without caching, the project would not be as
accessible.

Human effort. Although no code was written, the process required significant mathematical
expertise and approximately 50 hours of active supervision (Table 3). It requires a mathematician
who understands the proof well enough to detect when the agent is weakening the theorem. As one
Zulip commenter noted, “the human verification process... is critical” and cannot yet be replaced
by another LLM.


9    Conclusion
We have demonstrated that the full loop of AI-assisted mathematical research can be closed in
a matter of days: starting from an open conjecture, an AI reasoning model (Gemini DeepThink)
correctly resolved the question and produced a detailed proof requiring no corrections; an agentic
coding tool (Claude Code) translated this proof into 10K+ lines of Lean 4 from natural-language
prompts alone; a cloud-based prover (Aristotle) closed individual lemmas and caught false conjec-
tures; and the Lean kernel verified the final result with guaranteed logical correctness. A single
mathematician supervised the entire process at a cost of $200, writing zero lines of code.
    The process is not yet fully autonomous – the human’s role in maintaining theorem integrity
is essential and cannot currently be delegated to the AI. But the barrier to entry has dropped
dramatically: from years of Lean expertise to the ability to supervise an AI agent and evaluate
theorem statements.
    A striking feature of this project is that the formalization was completed before the traditional
mathematics paper containing the informal proof. The 10-day formalization finished on March
10; the companion math paper, which requires cleaning up the natural-language arguments and
obtaining co-author sign-off, is still in preparation. This reversal of the usual order – where formal-
ization lags publication by months or years – suggests that AI-assisted formalization has reached a
point where it takes comparable effort to produce a machine-checked proof and to write a polished
mathematical manuscript.
    We believe this workflow – conjecture, generate proof, formalize, verify, review – will become a
common mode of computer-assisted mathematical research. Each stage of the pipeline is now within
reach of current AI systems: reasoning models can resolve conjectures and produce detailed proofs,
coding agents can translate these proofs into formal languages, automated provers can close gaps
and catch errors, and proof kernels provide the final guarantee of correctness. The mathematician’s
role shifts from writing proofs to posing questions and evaluating claims – a supervisor of an AI-
driven research pipeline rather than its sole executor.


References
Tudor Achim, Alex Best, Alberto Bietti, Kevin Der, Mathı̈s Fédérico, Sergei Gukov, Daniel
  Halpern-Leistner, Kirsten Henningsgard, Yury Kudryashov, Alexander Meiburg, Martin
  Michelsen, Riley Patterson, Eric Rodriguez, Laura Scharff, Vikram Shanker, Vladmir Sicca,
  Hari Sowrirajan, Aidan Swope, Matyas Tamas, Vlad Tenev, Jonathan Thomm, Harold
  Williams, and Lawrence Wu. Aristotle: IMO-level automated theorem proving. arXiv preprint
  arXiv:2510.01346, 2025.


                                                  19
Jonas Bayer, Marco David, Malte Hassler, Yuri Matiyasevich, and Dierk Schleicher. Diophantine
  equations over Z: Universal bounds and parallel formalization. arXiv preprint arXiv:2506.20909,
  2025.

Carlo Cercignani. The Boltzmann Equation and Its Applications, volume 67 of Applied Mathematical
  Sciences. Springer, 1988. doi: 10.1007/978-1-4612-1039-9.

Carlo Cercignani, Reinhard Illner, and Mario Pulvirenti. The Mathematical Theory of Dilute Gases,
  volume 106 of Applied Mathematical Sciences. Springer, 1994.

Dawei Chen, Evan Chen, Kenny Lau, Ken Ono, and Jujian Zhang. Parity of k-differentials in genus
  zero and one. arXiv preprint arXiv:2602.03722, 2026a.

Evan Chen, Chris Cummins, Ben Eltschig, Dejan Grubisic, Leopold Haller, Letong Hong, Andranik
  Kurghinyan, Kenny Lau, Hugh Leather, Seewoo Lee, Aram Markosyan, Ken Ono, Manooshree
  Patel, Gaurang Pendharkar, Vedant Rathi, Alex Schneidman, Volker Seeker, Shubho Sengupta,
  Ishan Sinha, Jimmy Xin, and Jujian Zhang. Almost all primes are partially regular. arXiv
  preprint arXiv:2602.05090, 2026b.

Evan Chen, Chris Cummins, GSM, Dejan Grubisic, Leopold Haller, Letong Hong, Andranik
  Kurghinyan, Kenny Lau, Hugh Leather, Seewoo Lee, Aram Markosyan, Ken Ono, Manooshree
  Patel, Gaurang Pendharkar, Vedant Rathi, Alex Schneidman, Volker Seeker, Shubho Sengupta,
  Ishan Sinha, Jimmy Xin, and Jujian Zhang. Fel’s conjecture on syzygies of numerical semigroups.
  arXiv preprint arXiv:2602.03716, 2026c.

Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun,
  Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu,
  Yihang Xia, Huajian Xin, and Fan Yang. Seed-prover: Deep and broad reasoning for automated
  theorem proving. arXiv preprint arXiv:2507.23726, 2025.

Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language.
  In Automated Deduction – CADE 28. Springer, 2021. doi: 10.1007/978-3-030-79876-5 37.

Laurent Desvillettes and Cédric Villani. On the trend to global equilibrium for spatially inhomoge-
  neous kinetic systems: The Boltzmann equation. Inventiones mathematicae, 159:245–316, 2005.
  doi: 10.1007/s00222-004-0389-9.

Tony Feng, Trieu Trinh, Garrett Bingham, et al. Semi-autonomous mathematics discovery with
  Gemini: A case study on the Erdős problems. arXiv preprint arXiv:2601.22401, 2026a.

Tony Feng, Trieu H. Trinh, Garrett Bingham, et al. Towards autonomous mathematics research.
  arXiv preprint arXiv:2602.10177, 2026b.

FrenzyMath. Archon: AI-assisted mathematical formalization. https://frenzymath.com/blog/
  archon-firstproof/, 2025. Blog post.

Yan Guo. The Vlasov–Maxwell–Boltzmann system near Maxwellians. Inventiones mathematicae,
  153:593–630, 2003. doi: 10.1007/s00222-003-0301-z.

Yan Guo. The Vlasov–Poisson–Landau system in a periodic box. Journal of the American Mathe-
  matical Society, 25(3):759–812, 2012. doi: 10.1090/S0894-0347-2011-00722-4.


                                                20
Vasily Ilin and Jingwei Hu. A neural score-based particle method for the Vlasov–Maxwell–Landau
  system. arXiv preprint arXiv:2603.25832, 2026. Presented at ICLR AI&PDE workshop.

Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang, Yun-
  zhou Xie, Junqiao Zhao, Qiufeng Wang, Lihong Zhi, Jia Li, and Wenda Li. Numina-lean-
  agent: An open and general agentic reasoning system for formal mathematics. arXiv preprint
  arXiv:2601.14027, 2026.

Patrick Massot. LeanBlueprint: A plasTeX plugin to build formalization blueprints. https:
  //github.com/PatrickMassot/leanblueprint, 2020. Software.

Math, Inc. Completing the formal proof of higher-dimensional sphere packing. https://www.math.
 inc/sphere-packing, 2026. Blog post.

Nat Sothanaphan. Resolution of Erdős problem #728: a writeup of Aristotle’s Lean proof. arXiv
 preprint arXiv:2601.07421, 2026.

The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
 International Conference on Certified Programs and Proofs (CPP 2020), 2020. doi: 10.1145/
 3372885.3373824.

Joseph Tooby-Smith. Formalizing the stability of the two Higgs doublet model potential into Lean:
  Identifying an error in the literature. arXiv preprint arXiv:2603.08139, 2026.

Josef Urban. 130k lines of formal topology in two weeks: Simple and cheap autoformalization for
  everyone? arXiv preprint arXiv:2601.03298, 2026.

Cédric Villani. A review of mathematical topics in collisional kinetic theory. In Susan Friedlander
  and Denis Serre, editors, Handbook of Mathematical Fluid Dynamics, volume 1, pages 71–305.
  North-Holland, 2002.




                                                21
