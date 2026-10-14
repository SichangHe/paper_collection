                                          E ARLY E VIDENCE OF V IBE -P ROVING WITH C ONSUMER LLM S :
                                           A C ASE S TUDY ON S PECTRAL R EGION C HARACTERIZATION
                                                        WITH C HAT GPT-5.2 (T HINKING )



                                                     Brecht Verbeken1,2,                      Brando Vagenende1                     Marie-Anne Guerry1
                                                      0000-0002-7506-3298                     0000-0002-0573-8093                   0000-0001-5842-8905
arXiv:2602.18918v1 [cs.AI] 21 Feb 2026




                                                                    Andres Algaba1,2                                     Vincent Ginis1,2,3
                                                                   0000-0002-0532-3066                                  0000-0003-0063-9608
                                                           1
                                                           Data Analytics Lab, Vrije Universiteit Brussel, Pleinlaan 5, 1050 Brussel, Belgium
                                                             2
                                                               imec-SMIT, Vrije Universiteit Brussel, Pleinlaan 9, 1050 Brussels, Belgium
                                              3
                                                School of Engineering and Applied Sciences, Harvard University, Cambridge, Massachusetts 02138, USA


                                                                                               February 24, 2026

                                                                                                 A BSTRACT
                                                  Large Language Models (LLMs) are increasingly used as scientific copilots, but evidence on their
                                                  role in research-level mathematics remains limited, especially for workflows accessible to individual
                                                  researchers. We present early evidence for vibe-proving with a consumer subscription LLM through
                                                  an auditable case study that resolves Conjecture 20 of Ran and Teng (2024) on the exact nonreal
                                                  spectral region of a 4-cycle row-stochastic nonnegative matrix family. We analyze seven shareable
                                                  ChatGPT-5.2 (Thinking) threads and four versioned proof drafts, documenting an iterative pipeline
                                                  of generate, referee, and repair. The model is most useful for high-level proof search, while human
                                                  experts remain essential for correctness-critical closure. The final theorem provides necessary and
                                                  sufficient region conditions and explicit boundary attainment constructions. Beyond the mathematical
                                                  result, we contribute a process-level characterization of where LLM assistance materially helps
                                                  and where verification bottlenecks persist, with implications for evaluation of AI-assisted research
                                                  workflows and for designing human-in-the-loop theorem proving systems.

                                         Keywords AI-assisted mathematics · Karpelevich region · large language models · stochastic matrices


                                         1    Introduction

                                         Vibe-coding, where programmers steer Large Language Models (LLMs) to generate software through high-level natural-
                                         language intent rather than line-by-line specification, has rapidly transformed code generation [1, 2, 3]. Underpinning
                                         this shift is the sustained capability growth of frontier LLMs across successive systems and evaluations [4, 5, 6, 7].
                                         As these models grow more capable, they are increasingly deployed as scientific collaborators: generating candidate
                                         research ideas in controlled studies [8, 9], acting as agentic research assistants that plan, search, and iterate over literature
                                         and experiments [10, 11, 12, 13, 14, 15, 16], and accelerating evidence synthesis and literature screening [17, 18, 19].
                                         At field scale, LLM tooling is associated with measurable shifts in scientific production and communication [20],
                                         but it remains unclear how reliably these systems support auditable, research-level mathematical workflows under
                                         consumer-access conditions [21, 22].

                                               Corresponding author: brecht.verbeken@vub.be




                                                                                                        1
Beyond collaboration, LLMs increasingly execute end-to-end scientific workflows across domains. In the social
sciences, models serve as simulated subjects and predictive surrogates [23, 24, 25]. In the natural sciences, agentic
systems couple LLM reasoning to domain tools, autonomously running chemistry campaigns, designing biomolecules,
and accelerating experimental protocols [26, 27, 28, 29, 30, 31, 32], alongside work on test-time discovery and
automated search [33, 34]. Mathematics provides an unusually crisp stress test for whether vibe-coding’s paradigm
can extend beyond software: correctness is, in principle, checkable, and performance on benchmark suites has
improved rapidly [35, 36, 37, 38, 39, 40, 41]. Recent systems reach gold-medalist-level performance on Olympiad
geometry [42, 43], and a gold-medal score on International Mathematical Olympiad (IMO) problems [44]. At the
research frontier, program search and large-scale exploration pipelines generate new mathematical artefacts [45, 46, 47],
case studies document substantive human–LLM co-working on active problems [21, 48], and community infrastructures
curate open problem sets and evaluation tasks [49, 50, 51], including initiatives that explicitly invite LLM attempts [52].
Semi-autonomous pipelines have even been applied at scale to open mathematics problems [22, 53]. Together, these
results indicate that end-to-end AI-assisted mathematical discovery is becoming practically feasible.
These Erdős-scale and benchmark-scale results show what “specialized” LLM systems can achieve, but they leave a
practical question unresolved: can individual researchers produce mathematically substantive progress with consumer-
access models and explicit human verification? This question is central for vibe-proving, i.e., sustained, iterative
theorem development through conversational interaction rather than one-shot outputs. Unlike vibe-coding, where
software has a runtime oracle, vibe-proving faces an intrinsic verification bottleneck because every logical step must be
checked and a single hidden gap can invalidate the argument.
Our case study began when we encountered Conjecture 20 of [54] on nonreal eigenvalue regions of a structured 4 × 4
row-stochastic family of matrices. The project did not start from a pre-registered protocol, but from “vibing” with
ChatGPT-5.1 (Thinking) on an active research problem. During that initial exploratory phase, we did not systematically
retain our earliest interactions. Only after recognizing that the reasoning approach suggested by the LLM was not only
interesting but also potentially viable, did we transition from informal experimentation to systematic documentation
and structured iteration. Consequently, we reconstructed these initial prompts using ChatGPT-5.2 (Thinking). All
subsequent documented interactions were conducted directly with ChatGPT-5.2 (Thinking). We therefore ground the
paper in auditable artefacts: seven share links (Transcript 1–Transcript 7) and four proof drafts (Appendix Versions
A–D), and we explicitly mark where early prompt content is reconstructed rather than preserved verbatim.
Within this artefact set, we show that a stable interaction pattern of iterating between generate, referee, and repair
resolves the conjecture into a complete characterization theorem with explicit boundary attainment. The model is
strongest at proposing global structure (reparameterization and extremal strategy), whereas human effort is concentrated
on correctness-critical verification (quadrant control, branch tracking, endpoint admissibility, and dense algebraic
expansions). This framing complements recent mathematics results obtained with specialized or (semi-)autonomous
stacks, including dedicated theorem-discovery pipelines [55, 22], as well as domain-specific outputs in arithmetic
geometry, combinatorics, and robust control [56, 57, 58, 59]. Our contribution is a subscription-level, conversation-
auditable account where the revision trajectory is inspectable end-to-end.
The remainder of the paper is organized as follows. Section 2 introduces the mathematical setting and Conjecture 20.
Section 3 analyzes the interaction workflow with ChatGPT and documents the iterative proof-development process. We
then discuss the division of labor between model and human verification, limitations, and implications for AI-assisted
research workflows, and finally provide transcript-linked appendices and versioned proof artefacts for full auditability.




2     Mathematical Background


2.1   Spectral Regions of Stochastic Matrices

A fundamental problem in matrix theory is to characterize which complex numbers can appear as eigenvalues of
matrices with specific structural constraints. For row-stochastic matrices (nonnegative matrices with row sums equal
to 1), the definitive result is the Karpelevich theorem (1951) [60], which characterizes the region Kn of possible
eigenvalues of n × n row-stochastic matrices. For subclasses, such characterizations remain largely open.
Karpelevich’s original proof is notoriously difficult [61]. This difficulty has motivated significant recent work revisiting
and demystifying the Karpelevich theorem [62], as well as the search for alternative approaches for subclasses of
stochastic matrices where simpler characterizations might exist [63, 64, 65].


                                                             II
2.2   Dimitriev and Dynkin’s Trigonometric Method

Before Karpelevich’s general theorem, Dmitriev and Dynkin (1946) [66] developed a geometric method for characteriz-
ing the eigenvalue regions Kn for small n. Their approach, which we call the “trigonometric method,” is particularly
elegant:

      1. For an eigenvalue λ with eigenvector v, derive a multiplicative constraint from the eigenvalue equations.
      2. Reparametrize using arguments (u = Arg(z + t)) to convert the constraint into a trigonometric optimization
         problem.
      3. Use convexity and majorization arguments to characterize the boundary.

Dmitriev and Dynkin successfully characterized K2 , K3 , K4 , and K5 using this approach. Their method has the
advantage of being more elementary than Karpelevich’s and more amenable to adaptation for matrix subclasses with
specific zero patterns.

2.3   Conjecture 20 of Ran and Teng

Recently, Ran and Teng (2024) [54] studied eigenvalue regions for matrices with prescribed zero patterns, obtaining
complete characterizations for the 3×3 case. They also posed two conjectures for dimension four, of which Conjecture 20
concerns what we will call the “4-cycle” pattern.
Consider the family of 4 × 4 row-stochastic matrices:
                                         α     1−α             0          0
                                                                            
                                      0          β           1−β         0 
                     A(α, β, γ, δ) =                                          ,     α, β, γ, δ ∈ (0, 1).                     (1)
                                          0       0            γ        1 − γ
                                       1−δ        0            0          δ

This matrix has a so called cyclic zero pattern: state 1 transitions to states 1 or 2; state 2 to 2 or 3; state 3 to 3 or 4; state
4 to 4 or 1. Such patterns arise naturally in the study of Markov chains with restricted transitions.
Ran and Teng (2024) [54] defined the region R as:
                                       R = {z = a + bi ∈ K4 : a > 0, G(a, b) > 0}                                             (2)
where K4 is the Karpelevich region for 4 × 4 matrices and
                                           G(a, b) = (b2 + a2 + a)2 + 2a2 − b2 .                                              (3)
Conjecture 20 (Ran and Teng, 2024 [54], Conjecture 20). For any irreducible matrix A of the form (1), the non-real
eigenvalues of A lie in the region R.

Ran and Teng (2024) [54] provided substantial numerical evidence for this conjecture and proved that the curve
G(a, b) = 0 is indeed attained by the one-parameter subfamily AL (α) where β = γ = δ = 0:
                                                      α 1−α 0 0
                                                                     
                                                    0     0     1 0
                                          AL (α) =                     .                                   (4)
                                                      0    0     0 1
                                                      1    0     0 0

They conjectured that this curve forms the left boundary of the non-real part of the spectral region.

2.4   Contribution

We observed that Ran and Teng’s (2024) [54] Conjecture 20 could be used to provide a complete characterization.
Using the Karpelevich theorem and results on realizing boundary arcs (specifically, that the right boundary of K4 is
already attained within our restricted class), we provided a target theorem statement and asked ChatGPT for a proof
strategy.
The collaboration produced a proof of a theorem characterizing all non-real eigenvalues of the matrix family (1):
necessary and sufficient conditions, plus explicit boundary attainment. The full proof, developed through extended
dialogue with ChatGPT, will soon be available on the ArXiv. For this paper, the goal is to describe the process, not the
final product.


                                                                3
3     The Conversations with ChatGPT
3.1   Casual testing of GPT’s capabilities

The interaction with ChatGPT did not begin with a research plan. We were “vibing” by casually testing the “thinking
extended” mode on problems from our research area. During these informal explorations, we observed that the reasoning
approach suggested by the model was not only interesting but also potentially viable. Because these initial tests were
exploratory, we did not systematically document our earliest interactions with ChatGPT-5.1 (Thinking). To compensate
for the missing conversations with ChatGPT-5.1 (Thinking), we reran the initial prompts with ChatGPT-5.2 (Thinking)
in Transcript 1 and Transcript 2. From this point onward, all formal testing and documented interactions were performed
exclusively using ChatGPT-5.2 (Thinking), starting from Transcript 3. What follows is a reconstruction with the
versioned drafts (Appendix Versions A–D).

3.2   Setting Up the Theorem

We provided the Ran and Teng paper [54] and explained our observation about the right boundary being already
characterized by Karpelevich [60]. This resulted in the characterization Theorem below. Afterwards we provided
ChatGPT with this theorem statement and prompted the model towards the direction of thinking in line with the
trigonometric method of Dimitriev and Dynkin [67], and asked for a proof strategy (see Transcript 1 for the exact
statement we used in the prompt):
Theorem (Spectral region for a 4-cycle row-stochastic matrix). Let
                                        α     1−α       0        0
                                                                   
                                     0         β     1−β        0 
                    A(α, β, γ, δ) =                                   ,    α, β, γ, δ ∈ [0, 1].
                                         0      0       γ      1 − γ
                                      1−δ       0       0        δ
Let λ = a + ib ∈ σ(A(α, β, γ, δ)) with b ̸= 0, and write b+ = |b|. Then:
      1. 0 ≤ a ≤ 1;
      2. a + b+ ≤ 1;
      3. with
                                           G(a, b+ ) := (b2+ + a2 + a)2 + 2a2 − b2+ ,
         we have G(a, b+ ) ≥ 0.
Conversely, if b > 0 and
                                       0 ≤ a ≤ 1,     a + b < 1,        G(a, b) ≥ 0,
then there exist α, β, γ, δ ∈ [0, 1] such that λ ∈ σ(A(α, β, γ, δ)). (The lower half-plane follows by conjugation.)
Moreover:
       • the segment CR : λ = 1 − x + ix (x ∈ [0, 1]) is attained by α = β = γ = δ = 1 − x;
       • the curve portion CL of G(a, b) = 0 in the upper half-plane joining i to 0 is attained by
                                                   α 1−α 0 0
                                                                   
                                                 0      0     1 0
                                      AL (α) =                        ,     α ∈ [0, 1];
                                                   0     0     0 1
                                                   1     0     0 0

       • every point strictly inside {b > 0, 0 ≤ a ≤ 1, a + b < 1, G(a, b) ≥ 0} is attained.

3.3   The Proof Strategy

ChatGPT then proposed a trigonometric roadmap (angle parametrization plus Jensen/Karamata) inspired by [67, 68]
for the remaining constraints (see Transcript 1). The next prompt drew on our knowledge of the classical literature
(see Transcript 1). The response outlined the trigonometric approach: the multiplicative constraint from the eigenvalue
equations, reparametrization by arguments u = Arg(z + t), the convex function F , and the use of Jensen’s inequality
and Karamata’s inequality for the optimization. We then requested a hypercritical review, which surfaced a fatal gap in
the constrained Karamata/majorization step (see Transcript 2).


                                                           4
3.4   The Iterations

Appendix Version A contained the right structure but had gaps (see Transcript 3): incorrect quadrant handling for
arctan, a flawed inequality in what became Lemma 2, and incomplete algebra connecting the optimization to the curve
G(a, b) = 0.
The first correctness-critical bug was a feasibility claim in what became Lemma 2: the model’s original construction
fails in the near-endpoint regime M ↓ π/2. The repair was to localize the argument near the endpoint configuration
u4 ↑ M , and to require only the strict interior condition needed for that regime (namely u1 < M ) rather than uniform
slack up to M . This “local feasibility by continuity” patch is documented in Appendix Version B and corroborated by
an independent referee pass (see Transcript 6).
ChatGPT helped simplify and confirm the factorization |λ|6 ≥ N (a, b) (see Transcript 5). After some manipulation, it
produced:
                                       |λ|6 − N (a, b) = |λ − 1|2 G(a, b).                                       (5)
A disproportionate share of the iteration time went into Lemma 4 (see Transcript 5), which forces the “tight regime”
3m + M > 2π from the algebraic condition G(a, b) ≤ 0. To close this step, we wrote a fully expanded Lamport-style
draft of Lemma 4 and ran a dedicated “referee” thread focused on finding silent branch/sign errors rather than proposing
new structure. This pass largely validated the backbone of the argument (quadratic-in-s = b2 analysis, the deduction
b2 > 3a2 locating m in the correct range, reduction of 3m + M > 2π to a tangent inequality, and the load-bearing
algebraic identity |λ|6 − N (a, b) = |λ − 1|2 G(a, b)), but it also surfaced several obligations that earlier drafts had
left implicit: (i) the discriminant condition for G as a quadratic in s is ∆ ≥ 0 ⇐⇒ − 12 ≤ a ≤ 61 , so the conclusion
a ≤ 16 must be explicitly combined with the already-established constraint a ≥ 0; (ii) the Arg / arctan / tan branch
conventions and the monotonicity interval for tan must be stated once to justify the conversion of 3m + M > 2π
into a tangent inequality; and (iii) every squaring/cross-multiplication step must be preceded by a one-line positivity
check (notably 1 − a > 0 and denominator signs). We incorporated these items as explicit guard lines and reorganized
Lemma 4 into a “sign-check → transform → square/cross-multiply” micro-step schedule, which made the lemma
locally checkable and prevented regressions in later rewrites.
Appendix Version C is the first draft where the correctness-critical obligations are made explicit and discharged
end-to-end (see Transcript 4). Appendix Version D then primarily improves auditability: it expands the load-bearing
algebraic derivations (notably the factorization |λ|6 − N (a, b) = |λ − 1|2 G(a, b); see Transcript 5) and rewrites the
argument in a Lamport-style dependency structure (see Transcript 7).

3.5   From chronology to workflow-level lessons

The remainder of the paper abstracts the above chronology into workflow-level observations about verification, patch
search, and division of labor. To keep Section 3 chronological, we consolidate those methodological takeaways in the
Discussion (Section 4), with explicit pointers to the corresponding transcripts and appendix versions.

4     Discussion
4.1   What This Case Suggests

In this case study, a conversational workflow with ChatGPT-5.2 (Thinking) produced a complete and checkable proof
of Ran and Teng (2024) [54] Conjecture 20. The LLM supplied a viable global architecture early (characterization
theorem + trigonometric strategy), while the main human work consisted of identifying and discharging correctness
obligations (quadrant/branch handling, endpoint cases, and long algebra).
Success in this case used the following features of the problem and workflow:
       1. Prior scaffolding: The target was an explicit region characterization with known boundary information
          (Karpelevich right boundary and the conjectured left boundary G(a, b) = 0), and a classical proof template
          existed via a Dmitriev–Dynkin-style trigonometric reduction.
       2. Two anchoring prompts: The interaction was organized around (i) providing the target characterization
          theorem statement and boundary context and (ii) deriving a trigonometric/majorization-based proof strategy
          specialized to the 4-cycle matrix family.
       3. Untrusted outputs: Early drafts contained correctness-critical errors (e.g., arctan quadrant handling and a
          false inequality regime in Lemma 2), so every model-generated step was treated as a candidate and checked
          before inclusion.


                                                           5
      4. Independent patch search: When a gap was identified, we queried multiple independent sessions and
         compared proposed fixes, adopting only patches that could be verified and rejecting incompatible derivations.

We unpack the concrete verification workflow and division of labor in Sections 4.2–4.3.

4.2   Workflow and Verification Strategy

Across the seven threads, we converged on a stable loop of generate, referee, repair: generate candidate steps and
proof skeletons; run referee-style passes to surface hidden obligations (branch conventions, positivity checks before
squaring/cross-multiplying, endpoint admissibility); and then repair targeted subclaims without rewriting unrelated
parts.
Three concrete practices materially improved reliability:
       • Parallel patch search. When a gap was identified, we opened multiple independent sessions with the same
         obligation and treated their outputs as competing patches. We adopted only patches that were independently
         checkable (or where independent sessions converged), and rejected fixes that relied on silent case splits or
         unverifiable algebraic compression.
       • Fresh-session referee passes (bounded). At checkpoints, we pasted the then-current draft into a fresh thread
         and asked for a gap list (missing assumptions, unjustified monotonicity/branch steps, unsafe squaring). Once
         major gaps were fixed, repeated “hypercritical” prompting showed diminishing returns (stylistic noise and
         occasional false positives), so we used it as a bounded diagnostic rather than an endless loop.
       • Regression control via versioning and dependency visibility. Proof rewrites sometimes reintroduced errors
         elsewhere (notation drift, dropped sign constraints). We therefore kept versioned drafts aligned with transcript
         excerpts and re-checked downstream dependencies after each patch. We also frequently requested Lamport-
         style claim decomposition [69] to make dependencies explicit and to localize verification (see Transcript
         7).

4.3   Division of labor and the verification bottleneck

In this project, the model’s highest leverage was proposing global structure (reparameterizations, extremal strategies,
candidate factorizations) and producing fast symbolic manipulations; human time was dominated by correctness-critical
closure (branch/quadrant tracking, sign checks before squaring, endpoint admissibility, and long expansions).
Two observations were consistent across iterations:
      1. The bottleneck is narrow but expensive. Most iteration time concentrated on a small number of obligations
         (notably the tight-regime step around Lemma 4 and a few load-bearing factorizations), where a single silent
         sign/branch error can invalidate the argument.
      2. Mechanization would directly target the slowest work. The dominant verification load was algebraic
         expansion/simplification and inequality-domain checking. These are well matched to CAS and certified
         inequality/interval checkers, suggesting a practical hybrid pipeline: LLMs propose patches for explicit
         obligations; mechanized tooling validates the algebra/inequality substeps.
For completeness, we summarize the division of contributions (with transcript anchors):

Human contributions (verification and orchestration).
       • Problem selection and target theorem specification (see Transcript 1).
       • Error detection and obligation listing (quadrant/branch handling, Lemma 2 feasibility, endpoint issues).
       • Orchestration of independent patch search and regression control via versioned drafts.
       • Final correctness closure on sign/branch conditions and expanded algebra (see Transcript 5 and Transcript 6).
ChatGPT contributions (structure and candidate derivations).
       • Early global roadmap (trigonometric reduction + extremal strategy; Transcript 1).
       • Algebraic manipulation support, including confirming the key factorization (Transcript 5).
       • Structured Lamport-style rewrite that made dependencies explicit (Transcript 7).
       • Targeted referee passes that surfaced missing guard conditions when prompted appropriately (Transcript 2).


                                                            6
4.4   Formal Proof Assistants: The Verification Alternative

A natural question is how vibe proving with LLMs compares to formal proof assistants such as Lean, Coq, or
Isabelle [70, 71]. These systems offer something LLMs cannot: mechanically verified correctness relative to a small
logical kernel. When a Lean proof checks, the result is certain (modulo trust in the kernel, which is small but not zero,
as bugs have been found in proof assistant kernels, and complete formal verification of the kernel itself remains an open
problem) [72].
We did not attempt a formalization of the present proof. A mechanically verified proof would require encoding the
trigonometric optimization, convexity/majorization steps, and the inequality-heavy algebra within a proof assistant’s
libraries. This would yield stronger guarantees, but it would also change the artefact (proof script rather than narrative
proof) and require additional engineering beyond the scope of this case study.
Our output is a conventional, human-checked proof accompanied by an auditable chat trail.

4.5   Limitations
      1. Novelty: The proof strategy stayed within a classical Dmitriev–Dynkin/Jensen–Karamata template. The
         model’s main contribution was assembling and adapting this template to the 4-cycle matrix family rather than
         introducing a fundamentally new method.
      2. Error modes: We observed recurrent correctness failures in early drafts, including inverse-trigonometric
         branch/quadrant mistakes, missing sign conditions before squaring, and “compressed” algebra that omitted
         required intermediate steps.
      3. Verification bottleneck: The slowest component was discharging a small set of technical obligations (no-
         tably Lemma 4’s inequality/expansion chain and endpoint admissibility), rather than generating candidate
         derivations.
      4. Scope: Evidence here is limited to one structured spectral-region characterization problem with strong prior
         scaffolding (known conjectured boundary and known trigonometric reduction). We do not test problems
         lacking such structure.

4.6   Recommendations for Practitioners

The workflow-level observations in Sections 4.2–4.3 suggest the following checklist for vibe proving:

      1. Start from scaffolding. Prefer problems where you can state a concrete target theorem and where a recogniz-
         able reduction/template exists.
      2. Turn critique into obligations. Convert “this seems wrong” into an explicit obligation list (domains, branch
         conventions, positivity checks before squaring, endpoints).
      3. Use parallel patch search. Treat independent sessions as competing patch generators; adopt only patches that
         you can verify locally.
      4. Control regressions. Keep versioned drafts and re-check downstream dependencies after each patch; prefer
         Lamport-style decomposition to expose dependencies.
      5. Mechanize the bottleneck. Offload expansions and inequality-domain checks to CAS / certified checkers;
         reserve human time for conceptual choices and boundary cases.




                                                            7
Acknowledgements
This research was supported by funding from the Flemish Government under the “Onderzoeksprogramma Artificiële
Intelligentie (AI) Vlaanderen” program. Andres Algaba acknowledges support from the Francqui Foundation (Belgium)
through a Francqui Start-Up Grant and a fellowship from the Research Foundation Flanders (FWO) under Grant
No.1286924N. Vincent Ginis acknowledges support from Research Foundation Flanders under Grant No.G032822N
and G0K9322N.

Author contributions
All authors collaboratively conceived the main idea of the study. Brecht Verbeken co-constructed the proof with
the assistance of ChatGPT-5.1 (Thinking) and ChatGPT-5.2 (Thinking). Brecht Verbeken, Brando Vagenende, and
Marie-Anne Guerry reviewed and validated the final proof. Andres Algaba and Brecht Verbeken drafted the manuscript.
All authors collaboratively revised the manuscript and provided critical feedback.

Data and code availability
Conversations
• Transcript 1 (rerun): setup prompt + roadmap; includes follow-up algebra sanity checks (via ChatGPT’s Python tool).
• Transcript 2 (rerun): hypercritical review; identifies the majorization/Karamata gap.
• Transcript 3:referee pass on the first full proof attempt (Appendix Version A) and early gap list (branch/quadrant
  handling; Lemma 2 feasibility near M ; missing algebra).
• Transcript 4 corresponds to the first essentially complete draft (Appendix Version C).
• Transcript 5: referee pass on Lemma 4 (tight-regime step); checks branch/sign conditions and validates the factoriza-
  tion |λ|6 − N (a, b) = |λ − 1|2 G(a, b).
• Transcript 6: independent fresh-session critique corroborating the branch/quadrant and Lemma 2 issues/fix.
• Transcript 7: Lamport-style rewrite used for the final exposition (Appendix Version D).
Note that the following link template can be used to inspect meta-data from each conversation: https://chatgpt.
com/backend-api/share/<share-id>.

• Transcript 1 (rerun): https://chatgpt.com/share/699464b2-c81c-8002-9ba2-bad952e6414a
• Transcript 2 (rerun): https://chatgpt.com/share/69946540-e684-8002-a8ca-feb45e4da7be
• Transcript 3: https://chatgpt.com/share/697bb2d1-0418-8007-8f2a-474e3e6430fa
• Transcript 4: https://chatgpt.com/share/697bb2bd-5450-8007-9115-92589d95e1ba
• Transcript 5: https://chatgpt.com/share/697bb29a-c190-8007-b37e-87b390e9d9ff
• Transcript 6: https://chatgpt.com/share/697bb288-010c-8007-972b-ec676e9a16f7
• Transcript 7: https://chatgpt.com/share/697bb2ab-f83c-8007-a8fc-9439dd3d7488




                                                          8
References
 [1] Advait Sarkar and Ian Drosos. Vibe coding: programming through conversation with artificial intelligence, 2025.
 [2] Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. The impact of AI on developer productivity:
     Evidence from GitHub Copilot, 2023.
 [3] Kevin Zheyuan Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, and Tobias Salz. The productivity
     effects of generative AI: Evidence from a field experiment with GitHub Copilot, March 2024. Working paper
     (PubPub: An MIT Exploration of Generative AI).
 [4] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee,
     Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al. Sparks of artificial general intelligence: Early experiments with
     gpt-4. arXiv preprint arXiv:2303.12712, 2023.
 [5] Yijia Dai, Zhaolin Gao, Yahya Sattar, Sarah Dean, and Jennifer J Sun. Pre-trained large language models learn
     hidden markov models in-context. arXiv preprint arXiv:2506.07298, 2025.
 [6] Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang,
     Chaofan Lin, Chen Dong, et al. Deepseek-v3. 2: Pushing the frontier of open large language models. arXiv
     preprint arXiv:2512.02556, 2025.
 [7] Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart, Adi Ganesh, Ahmed El-Kishky, Aidan McLaughlin,
     Aiden Low, AJ Ostrow, Akhila Ananthram, et al. Openai gpt-5 system card. arXiv preprint arXiv:2601.03267,
     2025.
 [8] Alfredo Guevara, Alexandru Lupsasca, David Skinner, Andrew Strominger, and Kevin Weil. Single-minus gluon
     tree amplitudes are nonzero. arXiv preprint arXiv:2602.12176, 2026.
 [9] Chenglei Si, Diyi Yang, and Tatsunori Hashimoto. Can llms generate novel research ideas? a large-scale human
     study with 100+ nlp researchers. arXiv preprint arXiv:2409.04109, 2024.
[10] Jinheon Baek, Sujay Kumar Jauhar, Silviu Cucerzan, and Sung Ju Hwang. Researchagent: Iterative research
     idea generation over scientific literature with large language models. In Proceedings of the 2025 Conference
     of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language
     Technologies (Volume 1: Long Papers), pages 6709–6738, 2025.
[11] Alireza Ghafarollahi and Markus J Buehler. Sciagents: automating scientific discovery through bioinspired
     multi-agent intelligent graph reasoning. Advanced Materials, 37(22):2413523, 2025.
[12] Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Petar Sirkovic, Artiom Myaskovsky, Fe-
     lix Weissenberger, Keran Rong, Ryutaro Tanno, et al. Towards an ai co-scientist. arXiv preprint arXiv:2502.18864,
     2025.
[13] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The ai scientist: Towards
     fully automated open-ended scientific discovery. arXiv preprint arXiv:2408.06292, 2024.
[14] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner, Sergey
     Shirobokov, Borislav Kozlovskii, Francisco JR Ruiz, Abbas Mehrabian, et al. Alphaevolve: A coding agent for
     scientific and algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.
[15] Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael Moor,
     Zicheng Liu, and Emad Barsoum. Agent laboratory: Using llm agents as research assistants. Findings of the
     Association for Computational Linguistics: EMNLP 2025, pages 5977–6043, 2025.
[16] Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David
     Ha. The ai scientist-v2: Workshop-level automated scientific discovery via agentic tree search. arXiv preprint
     arXiv:2504.08066, 2025.
[17] Fernando M Delgado-Chaves, Matthew J Jennings, Antonio Atalaia, Justus Wolff, Rita Horvath, Zeinab M
     Mamdouh, Jan Baumbach, and Linda Baumbach. Transforming literature screening: The emerging role of large
     language models in systematic reviews. Proceedings of the National Academy of Sciences, 122(2):e2411962122,
     2025.
[18] Steven A Lehr, Aylin Caliskan, Suneragiri Liyanage, and Mahzarin R Banaji. Chatgpt as research scientist:
     Probing gpt’s capabilities as a research librarian, research ethicist, data generator, and data predictor. Proceedings
     of the National Academy of Sciences, 121(35):e2404328121, 2024.
[19] Michael D Skarlinski, Sam Cox, Jon M Laurent, James D Braza, Michaela Hinks, Michael J Hammerling,
     Manvitha Ponnapati, Samuel G Rodriques, and Andrew D White. Language agents achieve superhuman synthesis
     of scientific knowledge. arXiv preprint arXiv:2409.13740, 2024.


                                                            9
[20] Keigo Kusumegi, Xinyu Yang, Paul Ginsparg, Mathijs de Vaan, Toby Stuart, and Yian Yin. Scientific production
     in the era of large language models. Science, 390(6779):1240–1243, 2025.
[21] Sébastien Bubeck, Christian Coester, Ronen Eldan, Timothy Gowers, Yin Tat Lee, Alexandru Lupsasca, Mehtaab
     Sawhney, Robert Scherrer, Mark Sellke, Brian K Spears, et al. Early science acceleration experiments with gpt-5.
     arXiv preprint arXiv:2511.16072, 2025.
[22] Tony Feng, Trieu Trinh, Garrett Bingham, Jiwon Kang, Shengtong Zhang, Sang hyun Kim, Kevin Barreto, Carl
     Schildkraut, Junehyuk Jung, Jaehyeon Seo, Carlo Pagano, Yuri Chervonyi, Dawsen Hwang, Kaiying Hou, Sergei
     Gukov, Cheng-Chiang Tsai, Hyunwoo Choi, Youngbeom Jin, Wei-Yuan Li, Hao-An Wu, Ruey-An Shiu, Yu-Sheng
     Shih, Quoc V. Le, and Thang Luong. Semi-autonomous mathematics discovery with gemini: A case study on the
     erdős problems, 2026.
[23] Luke Hewitt, Ashwini Ashokkumar, Isaias Ghezae, and Robb Willer. Predicting results of social science
     experiments using large language models. Preprint, 2024.
[24] Benjamin S Manning, Kehang Zhu, and John J Horton. Automated social science: Language models as scientist
     and subjects. Technical report, National Bureau of Economic Research, 2024.
[25] Caleb Ziems, William Held, Omar Shaikh, Jiaao Chen, Zhehao Zhang, and Diyi Yang. Can large language models
     transform computational social science? Computational Linguistics, 50(1):237–291, 2024.
[26] Daniil A Boiko, Robert MacKnight, Ben Kline, and Gabe Gomes. Autonomous chemical research with large
     language models. Nature, 624(7992):570–578, 2023.
[27] Andres M. Bran, Sam Cox, Oliver Schilter, Carlo Baldassari, Andrew D White, and Philippe Schwaller. Augment-
     ing large language models with chemistry tools. Nature Machine Intelligence, 6(5):525–535, 2024.
[28] Yizhen Zheng, Huan Yee Koh, Jiaxin Ju, Anh TN Nguyen, Lauren T May, Geoffrey I Webb, and Shirui Pan.
     Large language models for scientific discovery in molecular property prediction. Nature Machine Intelligence,
     7(3):437–447, 2025.
[29] Kyle Swanson, Wesley Wu, Nash L Bulaong, John E Pak, and James Zou. The virtual lab of ai agents designs new
     sars-cov-2 nanobodies. Nature, 646(8085):716–723, 2025.
[30] Syed Asad Rizvi, Daniel Levine, Aakash Patel, Shiyang Zhang, Eric Wang, Curtis Jamison Perry, Nicole Mayerli
     Constante, Sizhuang He, David Zhang, Cerise Tang, et al. Scaling large language models for next-generation
     single-cell analysis. BioRxiv, pages 2025–04, 2025.
[31] Alexus A. Smith, Edmund L. Wong, Ronan C. Donovan, Brad A. Chapman, Ryan Harry, Pooyan Tirandazi,
     Paulina Kanigowska, Elizabeth A. Gendreau, Robert H. Dahl, Michal Jastrzebski, Jose E. Cortez, Christopher J.
     Bremner, José C. Morales Hemuda, James Dooner, Ian Graves, Rahul Karandikar, Christopher Lionetti, Kevin
     Christopher, Andrew L. Consiglio, Alyssa Tran, William McCusker, Duy X. Nguyen, Isis Botelho Nunes da Silva,
     Alvaro R. Bautista-Ayala, Monica P. McNerney, Sean Atkins, Michael McDuffie, Will Serber, Bradley P. Barber,
     Trinh Thanongsinh, Andrew Nesson, Bibek Lama, Brandon Nichols, Cameron LaFrance, Tenzing Nyima, Alicia
     Byrn, Rashard Thornhill, Bryan Cai, Lizvette Ayala-Valdez, Alycia Wong, Austin J. Che, Walter Thavarajah,
     Daniel Smith, Thomas F. Knight, David W. Borhani, Jerry Tworek, Mostafa Rohaninejad, Ahmed El-Kishky,
     Nathan C. Tedford, Tejal Patwardhan, Yunxin Joy Jiao, and Reshma P. Shetty. Using a gpt-5-driven autonomous
     lab to optimize the cost and titer of cell-free protein synthesis. bioRxiv, 2026.
[32] David P Woodruff, Vincent Cohen-Addad, Lalit Jain, Jieming Mao, Song Zuo, MohammadHossein Bateni, Simina
     Branzei, Michael P Brenner, Lin Chen, Ying Feng, et al. Accelerating scientific research with gemini: Case
     studies and common techniques. arXiv preprint arXiv:2602.03837, 2026.
[33] Mert Yuksekgonul, Daniel Koceja, Xinhao Li, Federico Bianchi, Jed McCaleb, Xiaolong Wang, Jan Kautz, Yejin
     Choi, James Zou, Carlos Guestrin, et al. Learning to discover at test time. arXiv preprint arXiv:2601.16175, 2026.
[34] Alex Vitvitskyi, Michael Boratko, Matej Grcic, Razvan Pascanu, Deep Shah, and Petar Veličković. Mining
     generalizable activation functions, 2026.
[35] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob
     Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv preprint arXiv:2103.03874,
     2021.
[36] Marthe Ballon, Andres Algaba, Brecht Verbeken, and Vincent Ginis. Benchmarks saturate when the model gets
     smarter than the judge. arXiv preprint arXiv:2601.19532, 2026.
[37] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert,
     Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al. Training verifiers to solve math word problems. arXiv
     preprint arXiv:2110.14168, 2021.


                                                         10
[38] Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar.
     Gsm-symbolic: Understanding the limitations of mathematical reasoning in large language models. arXiv preprint
     arXiv:2410.05229, 2024.
[39] Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Qingxiu Dong, Lei Li, Chenghao Ma, Liang Chen,
     Runxin Xu, et al. Omni-math: A universal olympiad level mathematic benchmark for large language models.
     arXiv preprint arXiv:2410.07985, 2024.
[40] Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego Chicharro, Evan Chen, Alex Gunning, Caroline Falkman Olsson,
     Jean-Stanislas Denain, Anson Ho, Emily de Oliveira Santos, et al. Frontiermath: A benchmark for evaluating
     advanced mathematical reasoning in ai. arXiv preprint arXiv:2411.04872, 2024.
[41] Center for AI Safety, Scale AI, and HLE Contributors Consortium. A benchmark of expert-level academic
     questions to assess ai capabilities. Nature, 649(8099):1139–1146, 2026.
[42] Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong. Solving olympiad geometry without human
     demonstrations. Nature, 625(7995):476–482, 2024.
[43] Yuri Chervonyi, Trieu H. Trinh, Miroslav Olšák, Xiaomeng Yang, Hoang H. Nguyen, Marcelo Menegali, Junehyuk
     Jung, Junsu Kim, Vikas Verma, Quoc V. Le, and Thang Luong. Gold-medalist performance in solving olympiad
     geometry with alphageometry2. Journal of Machine Learning Research, 26(241):1–39, 2025.
[44] Davide Castelvecchi. Ai models solve maths problems at level of top students. Nature, 644(7):1, 2025.
[45] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar,
     Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. Mathematical
     discoveries from program search with large language models. Nature, 625(7995):468–475, 2024.
[46] Grzegorz Swirszcz, Adam Zsolt Wagner, Geordie Williamson, Sam Blackwell, Bogdan Georgiev, Alex Davies, Ali
     Eslami, Sebastien Racaniere, Theophane Weber, and Pushmeet Kohli. Advancing geometry with ai: Multi-agent
     generation of polytopes. arXiv preprint arXiv:2502.05199, 2025.
[47] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathematical exploration and
     discovery at scale. arXiv preprint arXiv:2511.02864, 2025.
[48] Jim Bryan, Balázs Elek, Freddie Manners, George Salafatinos, and Ravi Vakil. The motivic class of the space of
     genus 0 maps to the flag variety. arXiv preprint arXiv:2601.07222, 2026.
[49] Damek Davis, Paata Ivanisvili, Terence Tao, and contributors. Optimization constants in mathematics. GitHub
     repository, 2026.
[50] P. Chojecki. Unsolvedmath: A curated collection of open mathematics problems. https://huggingface.co/
     datasets/ulamai/UnsolvedMath, 2026. Includes over 1000 open mathematical problems.
[51] T. F. Bloom. Erdős problems. https://www.erdosproblems.com, 2026. Forum.
[52] Mohammed Abouzaid, Andrew J. Blumberg, Martin Hairer, Joe Kileel, Tamara G. Kolda, Paul D. Nelson, Daniel
     Spielman, Nikhil Srivastava, Rachel Ward, Shmuel Weinberger, and Lauren Williams. First proof, 2026.
[53] Kevin Barreto, Jiwon Kang, Sang-hyun Kim, Vjekoslav Kovač, and Shengtong Zhang. Irrationality of rapidly
     converging series: a problem of erdős and graham. arXiv preprint arXiv:2601.21442, 2026.
[54] André CM Ran and Zhixuan Emily Teng. The nonnegative inverse eigenvalue problem with prescribed zero
     patterns in dimension three. The Electronic Journal of Linear Algebra, 40:506–537, 2024.
[55] Tony Feng, Trieu H Trinh, Garrett Bingham, Dawsen Hwang, Yuri Chervonyi, Junehyuk Jung, Joonkyung Lee,
     Carlo Pagano, Sang-hyun Kim, Federico Pasqualotto, et al. Towards autonomous mathematics research. arXiv
     preprint arXiv:2602.10177, 2026.
[56] Tony Feng. Eigenweights for arithmetic hirzebruch proportionality. arXiv preprint arXiv:2601.23245, 2026.
[57] Tony Feng, Zhiwei Yun, and Wei Zhang. Arithmetic volumes of moduli stacks of shtukas. arXiv preprint
     arXiv:2601.18557, 2026.
[58] Joonkyung Lee and Jaehyeon Seo. Lower bounds for multivariate independence polynomials and their generalisa-
     tions. arXiv preprint arXiv:2602.02450, 2026.
[59] Ali Asadi, Krishnendu Chatterjee, Ehsan Goharshady, Mehrdad Karrabi, Alipasha Montaseri, and Carlo Pagano.
     Strongly polynomial time complexity of policy iteration for l∞ robust mdps. arXiv preprint arXiv:2601.23229,
     2026.
[60] F. I. Karpelevych. On the characteristic roots of matrices with nonnegative elements. Izvestiya Akademii Nauk
     SSSR, Seriya Matematicheskaya, 15:361–383, 1951. In Russian.


                                                        11
[61] Charles R Johnson and Pietro Paparella. A matricial view of the karpelevič theorem. Linear Algebra and its
     Applications, 520:1–15, 2017.
[62] D. N. Munger, A. L. Nickerson, and P. Paparella. Demystifying the karpelevič theorem. Linear Algebra and its
     Applications, 690:10–36, 2024.
[63] Marie-Anne Guerry. On monotone markov chains and properties of monotone matrix roots. Special Matrices,
     11(1):20220172, 2022.
[64] Bara Kim and Jeongsim Kim. Conjectures about determining the regions of eigenvalues of stochastic and doubly
     stochastic matrices. Linear Algebra and its Applications, 637:157–174, 2022.
[65] Brando Vagenende, Brecht Verbeken, and Marie-Anne Guerry. Eigenvalue regions and realising monotone
     stochastic matrices. arXiv preprint arXiv:2502.01314, 2025.
[66] N. Dmitriev and E. Dynkin. On characteristic roots of stochastic matrices. Izvestija Akademii Nauk SSSR, Serija
     Matematicheskaja, 10:167–184, 1946. English translation in: J. Swift, The Location of Characteristic Roots of
     Stochastic Matrices, M.Sc. Thesis, McGill University, 1972, Appendix A.
[67] Nikolai Aleksandrovich Dmitriev and E Dynkin. On characteristic roots of stochastic matrices. Izvestiya Rossiiskoi
     Akademii Nauk. Seriya Matematicheskaya, 10(2):167–184, 1946.
[68] Joanne Swift. The location of characteristic roots of stochastic matrices. 1972.
[69] Leslie Lamport. How to write a proof. The American Mathematical Monthly, 102(7):600–608, 1995. Originally
     appeared as Technical Report 94, Digital Equipment Corporation, Systems Research Center, 1993.
[70] The Coq Development Team. The coq proof assistant, 2024. Software artifact (Zenodo); published June 10, 2024;
     version 8.19.
[71] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming language. In Automated
     Deduction – CADE 28, volume 12699 of Lecture Notes in Computer Science, pages 625–635. Springer, 2021.
[72] Azim Ospanov, Farzan Farnia, and Roozbeh Yousefzadeh. Apollo: Automated llm and lean collaboration for
     advanced formal reasoning. arXiv preprint arXiv:2505.05758, 2025.




                                                         12
Here, we show the subsequent versions of the proof.

A      Appendix

    First version
    Theorem 21 (Precise spectral region for a 4-cycle row-stochastic matrix). Let
                                          α     1−α       0        0
                                                                     
                                      0          β     1−β        0 
                    A(α, β, γ, δ) =                                     ,     α, β, γ, δ ∈ [0, 1).
                                          0       0       γ     1 − γ
                                       1−δ        0       0        δ
    Let λ = a + ib ∈ σ(A(α, β, γ, δ)) with b ̸= 0, and write b+ = |b|. Then:
          1. 0 ≤ a ≤ 1.
          2. a + b+ ≤ 1.
          3. with
                                              G(a, b+ ) := (b2+ + a2 + a)2 + 2a2 − b2+ ,
             we have G(a, b+ ) ≥ 0.
    Conversely, if b > 0 and
                                         0 ≤ a ≤ 1,       a + b < 1,      G(a, b) > 0,
    then there exist α, β, γ, δ ∈ [0, 1) such that λ ∈ σ(A(α, β, γ, δ)). (The lower half-plane follows by conjugation.)
    Moreover:
           • the segment CR : λ = 1 − x + ix (x ∈ [0, 1]) is attained by α = β = γ = δ = 1 − x;
           • the curve portion CL of G(a, b) = 0 in the upper half-plane joining i to 0 is attained by
                                                        α 1−α 0 0
                                                                        
                                                      0      0      1 0
                                           AL (α) =                        ,     α ∈ [0, 1);
                                                        0     0      0 1
                                                        1     0      0 0
           • every point strictly inside {b > 0, 0 ≤ a ≤ 1, a + b < 1, G(a, b) > 0} is attained.
    Proof. 1) Eigenvalue equation. Let v ̸= 0 satisfy Av = λv. Row-by-row,
       (λ − α)v1 = (1 − α)v2 ,      (λ − β)v2 = (1 − β)v3 ,         (λ − γ)v3 = (1 − γ)v4 ,   (λ − δ)v4 = (1 − δ)v1 .
    Since 1 − α, . . . , 1 − δ > 0, if any vk = 0 then all vj = 0, contradiction. Hence v1 v2 v3 v4 ̸= 0, and multiplying
    gives
                               (λ − α)(λ − β)(λ − γ)(λ − δ) = (1 − α)(1 − β)(1 − γ)(1 − δ).                            (1)
    Put t1 = 1 − α, . . . , t4 = 1 − δ ∈ (0, 1] and z = λ − 1. Then λ − (1 − tk ) = z + tk , so Equation 1 becomes
                                       (z + t1 )(z + t2 )(z + t3 )(z + t4 ) = t1 t2 t3 t4 .                             (2)

    2) Angle parametrization and the function F . Assume b > 0 (the case b < 0 follows by conjugation since A is
    real). Write
                                             z = x + iy,       x = a − 1, y = b.
    For t > 0, z + t lies in the upper half-plane, so define u(t) = arg(z + t) ∈ (0, π). Elementary trigonometry gives
    the inverse relation
                                     t = t(u) = y cot u − x,       |z + t(u)| = y csc u.                           (3)
    Define
                           F (u) := log |z + t(u)| − log t(u) = log(y csc u) − log(y cot u − x).                   (4)
    Let
                               m := arg(z + 1) = arg(λ),          M := arg(z) = arg(λ − 1).                        (5)
    As t ↓ 0, u(t) ↑ M ; as t ↑ 1, u(t) ↓ m. Thus
                                              t ∈ (0, 1]    ⇐⇒       u ∈ [m, M ).                                       (6)


                                                               13
Lemma 1 (Log-modulus/argument reformulation). A nonreal λ satisfies Equation 2 for some tk ∈ (0, 1] iff there
exist uk ∈ [m, M ) such that
                                              u1 + u2 + u3 + u4 = 2π,                                      (7)
                                      F (u1 ) + F (u2 ) + F (u3 ) + F (u4 ) = 0.                           (8)
Proof.PWrite z + tk = |z + tk |eiuP
                                                                                           P
                                   k
                                     with uk ∈ (0, π). Taking arguments in Equation 2 gives uk ≡ 0 (mod 2π);
since uk ∈ (0, 4π) this forces uk = 2π, i.e. Equation 7. Taking moduli and logs gives Equation 8. Condition
Equation 6 is exactly tk ∈ (0, 1]. Conversely, Equation 7 and Equation 8 give equality of arguments and moduli,
hence Equation 2.
Define
               n                                                    o                                    4
                                                                                                         X
           P := (u1 , . . . , u4 ) ∈ [m, M )4 : u1 + · · · + u4 = 2π ,          Ψ(u1 , . . . , u4 ) :=         F (uk ).
                                                                                                         k=1

Then λ is a nonreal eigenvalue of some A(α, β, γ, δ) iff P ̸= ∅ and 0 ∈ Ψ(P).
3) Necessarily 0 ≤ a ≤ 1 (indeed a < 1 if b ̸= 0). Every (u1 , . . . , u4 ) ∈ P has average π/2, so π/2 ∈ [m, M ),
i.e.
                                                     π
                                                m ≤ < M.                                                       (9)
                                                     2
For b > 0, m ≤ π/2 ⇐⇒ a ≥ 0. Also M > π/2 ⇐⇒ a < 1 because ℜ(λ − 1) = a − 1 < 0 iff a < 1. Thus
P ̸= ∅ implies
                                                 0 ≤ a < 1,                                                   (10)
hence in particular 0 ≤ a ≤ 1.
4) Strict convexity of F . Differentiate Equation 4 using Equation 3. A direct computation yields
                                                   x2 + y 2
                                F ′′ (u) =                         >0         (u ∈ (0, π)),                               (11)
                                             (x − y cot u)2 sin2 u
so F is strictly convex on (0, π), hence on [m, M ).
5) Right boundary: a + b ≤ 1, and attainment of CR . P is convex and connected; Ψ is continuous, hence Ψ(P)
is an interval. By Jensen and strict convexity,
                                                        u + · · · + u 
                                                          1           4
                                Ψ(u1 , . . . , u4 ) ≥ 4F                 = 4F (π/2).                         (12)
                                                              4
Thus 0 ∈ Ψ(P) forces F (π/2) ≤ 0. Now
                                                                          b 
                                   F (π/2) = log(y) − log(−x) = log             ,
                                                                          1−a
so F (π/2) ≤ 0 ⇐⇒ b ≤ 1 − a ⇐⇒ a + b ≤ 1. This proves item (2) (for b > 0; for b < 0 replace b by |b|).
Attainment of CR : if t1 = t2 = t3 = t4 = x ∈ (0, 1], then Equation 2 becomes (z + x)4 = x4 , i.e. λ = 1 − x ± ix,
attained by α = β = γ = δ = 1 − x.
6) A max principle on P. There are two regimes.
Lemma 2 (Unbounded supremum). If
                                                     3m + M ≤ 2π,                                                         (13)
then supP Ψ = +∞.
Proof. Take u4 ↑ M and u1 = u2 = u3 = (2π − u4 )/3. Condition Equation 13 ensures u1 ≥ m. Also
u4 < M and u1 ≤ (2π − M )/3 ≤ M since M ≥ π/2 ⇒ 2π ≤ 4M . Hence (u1 , . . . , u4 ) ∈ P. As u4 ↑ M ,
t(u4 ) = y cot u4 − x ↓ 0, so − log t(u4 ) → +∞ while log(y csc u4 ) stays bounded; thus F (u4 ) → +∞ and
Ψ → +∞.
Lemma 3 (Finite maximum in the tight regime). If
                                     3m + M > 2π,            U := 2π − 3m < M,                                            (14)
then
                                               max Ψ = 3F (m) + F (U ),                                                   (15)
                                                 P
and equality holds iff (u1 , . . . , u4 ) is a permutation of (U, m, m, m).


                                                            14
                                                                              P
Proof. Order uk decreasing: v1 ≥ v2 ≥ v3 ≥ v4 . Since each vj ≥ m and             vj = 2π,
                                    v1 = 2π − (v2 + v3 + v4 ) ≤ 2π − 3m = U.
                             4
Thus (v1 , . . . , v4 ) ∈ [m, U ] with sum 2π. The vector (U, m, m, m) majorizes (v1 , . . . , v4 ). By Karamata (convex
F ),
                                             X 4
                                                 F (vj ) ≤ F (U ) + 3F (m),
                                           j=1

with equality only at permutations of (U, m, m, m) since F is strictly convex.

7) The inequality G(a, b) ≥ 0. We prove necessity for every nonreal eigenvalue.
7.1 Geometry lemma: G(a, b) ≤ 0 ⇒ 3m + M > 2π
Lemma 4. Assume b > 0 and 0 ≤ a ≤ 1. If G(a, b) ≤ 0, then 3m + M > 2π.
Proof. Set s = b2 . Then
                               G(a, b) = s2 + s(2a2 + 2a − 1) + (a2 + a)2 + 2a2 .                                    (16)
This is quadratic in s with discriminant
                       ∆ = (2a2 + 2a − 1)2 − 4 (a2 + a)2 + 2a2 = −(2a + 1)(6a − 1).
                                                                

Thus G(a, b) ≤ 0 forces ∆ > 0, hence a < 1/6, and s lies between the two real roots; in particular
                                          1               1p
                            s ≥ s− (a) := − a − a2 −         (1 − 6a)(1 + 2a).                                       (17)
                                          2               2
Case 1: a = 0. Then m = arg(ib) = π/2, and M = arg(−1 + ib) = π − arctan(b). Hence
                                         3π                   5π
                            3m + M =        + π − arctan(b) =    − arctan(b) > 2π.
                                          2                    2
Case 2: a > 0. From Equation 17 we get s > s− (a) ≥ 3a2 , with strictness because
                                          1                1p
                           s− (a) − 3a2 = − a − 4a2 −          (1 − 6a)(1 + 2a)
                                          2                2
                                                                                                                √
satisfies (LHS)2 − (RHS)2 = 32a3 (2a + 1) > 0 for a > 0. Hence b2 > 3a2 , i.e. tan m = b/a >                        3, so
m > π/3 and 3m − π ∈ (0, π/2).
                    b
Write ϕ := arctan 1−a  ∈ (0, π/2), so M = π − ϕ. Then
                                                                                      b
                           3m + M > 2π ⇐⇒ 3m − π > ϕ ⇐⇒ tan(3m) >                        ,                           (18)
                                                                                     1−a
since tan is increasing on (0, π/2) and tan(3m − π) = tan(3m).
                                                                                     3t−t3
Let t = tan m = b/a (allowed since a > 0). The triple-angle identity gives tan(3m) = 1−3t2 , and a direct

simplification yields
                                             b      b (4a3 − 3a2 − 4ab2 + b2 )
                                tan(3m) −        =                             .                     (19)
                                            1−a         a(a − 1)(a2 − 3b2 )
Here a > 0, a − 1 < 0, and a2 − 3b2 < 0 (since b2 > 3a2 ), so the denominator in Equation 19 is positive. Hence
the sign equals the sign of
                         N (a, b) := 4a3 − 3a2 − 4ab2 + b2 = (1 − 4a)b2 + a2 (4a − 3).                               (20)
For a < 1/6, 1 − 4a > 0 and 4a − 3 < 0, so N (a, b) is strictly increasing in b2 and has a unique zero at
                                                            a2 (3 − 4a)
                                                 s0 (a) =               .                                            (21)
                                                              1 − 4a
One checks that s− (a) > s0 (a) for every a ∈ (0, 1/6): after multiplying by 1 − 4a > 0 and squaring, the
difference becomes 256a6 > 0. Therefore b2 ≥ s− (a) > s0 (a) implies N (a, b) > 0. By Equation 19–18, this
gives 3m + M > 2π.


                                                            15
7.2 Tight regime: max Ψ ≥ 0 ⇐⇒ G ≥ 0
Assume 3m + M > 2π, so Lemma 6.2 applies with U = 2π − 3m ∈ (0, π) and maximizer (U, m, m, m). Since
u(1) = arg(z + 1) = m, Equation 6 gives t(m) = 1, hence
                                     F (m) = log |z + 1| − log 1 = log |λ|.                                 (22)
Also t(U ) = b cot U − (a − 1) = b cot U + 1 − a and |z + t(U )| = b csc U , so by Equation 15
                                                                                   |λ|3 b csc U
                                                                                               
             max Ψ = 3 log |λ| + log(b csc U ) − log(b cot U + 1 − a) = log                       .         (23)
               P                                                                b cot U + 1 − a
Thus maxP Ψ ≥ 0 is equivalent to
                                 |λ|3 b csc U ≥ b cot U + 1 − a.                        (24)
                                                                  3          3    3     2
Now U = 2π − 3m, so sin U = − sin(3m) and cos U = cos(3m). Since λ = (a + ib) = (a − 3ab ) +
i(3a2 b − b3 ), we have
                              ℜ(λ3 )   a(a2 − 3b2 )                           ℑ(λ3 )   b(3a2 − b2 )
                  cos(3m) =       3
                                     =              ,            sin(3m) =           =              .       (25)
                               |λ|         |λ|3                                |λ| 3       |λ|3
Hence
                                         b(b2 − 3a2 )                      a(a2 − 3b2 )
                               sin U =                ,          cos U =                .                   (26)
                                             |λ|3                              |λ|3
In the tight regime, necessarily m > π/3 (since M ≤ π), hence b2 − 3a2 > 0, so sin U > 0 and
                                               |λ|3                        a(a2 − 3b2 )
                               b csc U =                ,     b cot U =                 .                   (27)
                                             b2 − 3a2                       b2 − 3a2
Substitute Equation 27 into Equation 24 and clear the positive denominator b2 − 3a2 :
                                   |λ|6 ≥ a(a2 − 3b2 ) + (1 − a)(b2 − 3a2 ).                                (28)
Using |λ|2 = a2 + b2 , a direct expansion and factorization yields
                                                               
                   |λ|6 − a(a2 − 3b2 ) + (1 − a)(b2 − 3a2 ) = (a − 1)2 + b2 G(a, b).
                                                                           
                                                                                                            (29)

Since (a − 1)2 + b2 = |λ − 1|2 > 0, Equation 28 is equivalent to G(a, b) ≥ 0. Therefore, in the tight regime,
                                      max Ψ ≥ 0             ⇐⇒     G(a, b) ≥ 0.                             (30)
                                         P

7.3 Necessity of G ≥ 0 for all nonreal eigenvalues
Let λ be a nonreal eigenvalue of some A(α, β, γ, δ). Then P ̸= ∅ and 0 ∈ Ψ(P), hence supP Ψ ≥ 0. If
3m + M ≤ 2π, the previous lemma (contrapositive) gives G(a, b) ≥ 0. If 3m + M > 2π, then sup Ψ = max Ψ
and Equation 30 gives G(a, b) ≥ 0. This proves item (3) in the theorem.
8) Boundary identification and sharpness.
8.1 Right boundary CR
Already established in §5.
8.2 Left boundary CL : attainment by AL (α), and G = 0
For
                                         α 1−α 0 0
                                                      
                                      0       0   1 0
                             AL (α) =                   ,                   α ∈ [0, 1),
                                         0     0   0 1
                                         1     0   0 0
we have β = γ = δ = 0, so Equation 1 reduces to
                                                λ3 (λ − α) = 1 − α.                                         (31)
Eliminate α:
                                                            λ4 − 1
                                                      α=           .                                        (32)
                                                            λ3 − 1


                                                            16
                   4
Thus α ∈ R iff ℑ λλ3 −1
                        
                     −1 = 0. Compute
                                                                 
                                              ℑ (λ4 − 1)(λ3 − 1)
                                    4    
                                     λ −1
                                 ℑ 3        =                      .
                                     λ −1          |λ3 − 1|2
A direct expansion and factorization in λ = a + ib gives, for b ̸= 0,
                                          4
                                                       b |λ − 1|2 G(a, b)
                                                 
                                           λ −1
                                       ℑ 3          =                     .                                   (33)
                                           λ −1             |λ3 − 1|2
Hence, for b ̸= 0,
                                         α ∈ R ⇐⇒ G(a, b) = 0.                                                (34)
So every nonreal eigenvalue of AL (α) lies on G = 0.
Moreover, AL (α) always has a nonreal conjugate pair: rewrite Equation 31 as
                                                                            
                λ4 − αλ3 − (1 − α) = 0 ⇐⇒ (λ − 1) λ3 + (1 − α)(λ2 + λ + 1) = 0.

Let c = 1 − α ∈ (0, 1] and f (λ) = λ3 + c(λ2 + λ + 1). Then
                                             f ′ (λ) = 3λ2 + 2cλ + c
has discriminant 4c(c − 3) < 0, so f is strictly increasing on R. Also f (0) = c > 0 and f (λ) → −∞ as λ → −∞,
hence f has exactly one real root. Therefore the remaining two roots of f form a nonreal conjugate pair, giving the
desired pair for AL (α).
Endpoints: at α = 0, Equation 31 becomes λ4 = 1, giving λ = i. As α ↑ 1, Equation 31 tends to λ3 (λ − 1) = 0;
the conjugate pair among the three non-1 roots tends to 0. Thus α ∈ [0, 1) traces a connected arc of G = 0 from i
to 0.
Finally, every point on that arc is attained as follows. Let λ = a + ib with b > 0, 0 ≤ a ≤ 1, a + b ≤ 1, and
G(a, b) = 0. By Lemma 7.1 (since G = 0 ≤ 0), we are in the tight regime 3m + M > 2π, so Lemma 6.2 applies
and the maximizer is (U, m, m, m) with U = 2π − 3m ∈ [m, M ). By §7.2, G = 0 implies maxP Ψ = 0, hence
Ψ(U, m, m, m) = 0. By Lemma 2.1 this produces t1 = t(U ) ∈ (0, 1] and t2 = t3 = t4 = t(m) = 1, satisfying
Equation 2. Therefore the corresponding parameters
                                   α = 1 − t(U ) ∈ [0, 1),      β=γ=δ=0
yield exactly AL (α) and give λ as an eigenvalue. This identifies CL and proves it is attained.
9) Existence for every strict interior point. Fix λ = a + ib with b > 0 such that
                                  0 ≤ a ≤ 1,       a + b < 1,         G(a, b) > 0.                            (35)
Define z, m, M, F, P, Ψ as above. Then P ̸= ∅ by §3.
We show 0 ∈ Ψ(P). By Jensen,
                                                                              b 
                            Ψ(π/2, π/2, π/2, π/2) = 4F (π/2) = 4 log               <0
                                                                              1−a
since a + b < 1 ⇐⇒ b < 1 − a.
To produce a positive value: if 3m + M ≤ 2π, Lemma 6.1 gives supP Ψ = +∞, so Ψ takes positive values. If
3m + M > 2π, Lemma 6.2 gives maxP Ψ = 3F (m) + F (U ); by §7.2, G(a, b) > 0 implies maxP Ψ > 0, so Ψ
takes positive values.
Since P is connected and Ψ is continuous, Ψ(P) is an interval containing both negative and positive values,
hence contains 0. Thus there exists (u1 , . . . , u4 ) ∈ P with Ψ(u1 , . . . , u4 ) = 0. By Lemma 2.1 this yields
tk = t(uk ) ∈ (0, 1] satisfying Equation 2. Set
                        α = 1 − t1 ,    β = 1 − t2 ,   γ = 1 − t3 ,     δ = 1 − t4 ∈ [0, 1),
and then Equation 1 holds, so λ ∈ σ(A(α, β, γ, δ)). Conjugation gives the lower half-plane.




                                                        17
B
    Second version
    Theorem 22 (Spectral region for a 4-cycle row-stochastic matrix). Let
                                         α      1−α       0       0
                                                                     
                                      0         β     1−β        0 
                    A(α, β, γ, δ) =                                    ,              α, β, γ, δ ∈ [0, 1).
                                          0      0        γ     1 − γ
                                        1−δ      0        0       δ
    Let λ = a + ib ∈ σ(A(α, β, γ, δ)) with b ̸= 0, and write b+ = |b|. Then:
          1. 0 ≤ a ≤ 1;
          2. a + b+ ≤ 1;
          3. with
                                               G(a, b+ ) := (b2+ + a2 + a)2 + 2a2 − b2+ ,
             we have G(a, b+ ) ≥ 0.
    Conversely, if b > 0 and
                                         0 ≤ a ≤ 1,       a + b < 1,      G(a, b) > 0,
    then there exist α, β, γ, δ ∈ [0, 1) such that λ ∈ σ(A(α, β, γ, δ)). (The lower half-plane follows by conjugation.)
    Moreover:
           • the segment CR : λ = 1 − x + ix (x ∈ [0, 1]) is attained by α = β = γ = δ = 1 − x;
           • the curve portion CL of G(a, b) = 0 in the upper half-plane joining i to 0 is attained by
                                                        α 1−α 0 0
                                                                        
                                                      0       0     1 0
                                           AL (α) =                        ,     α ∈ [0, 1);
                                                        0      0     0 1
                                                        1      0     0 0
           • every point strictly inside {b > 0, 0 ≤ a ≤ 1, a + b < 1, G(a, b) > 0} is attained.
    Proof. 1) Eigenvalue equation. Let v ̸= 0 satisfy Av = λv. Row-by-row,
       (λ − α)v1 = (1 − α)v2 ,      (λ − β)v2 = (1 − β)v3 ,         (λ − γ)v3 = (1 − γ)v4 ,      (λ − δ)v4 = (1 − δ)v1 .
    Since 1 − α, . . . , 1 − δ > 0, if any vk = 0 then all vj = 0, contradiction. Hence v1 v2 v3 v4 ̸= 0, and multiplying
    gives
                               (λ − α)(λ − β)(λ − γ)(λ − δ) = (1 − α)(1 − β)(1 − γ)(1 − δ).                            (1)
    Put t1 = 1 − α, . . . , t4 = 1 − δ ∈ (0, 1] and z = λ − 1. Then λ − (1 − tk ) = z + tk , so (1) becomes
                                       (z + t1 )(z + t2 )(z + t3 )(z + t4 ) = t1 t2 t3 t4 .                                (2)

    2) Angle parametrization and the function F . Assume b > 0 (the case b < 0 follows by conjugation since A is
    real). Write
                                             z = x + iy,       x = a − 1, y = b.
    For t > 0, z + t lies in the upper half-plane, so define u(t) = Arg(z + t) ∈ (0, π). Elementary trigonometry gives
    the inverse relation
                                     t = t(u) = y cot u − x,        |z + t(u)| = y csc u.                          (3)
    Define
                           F (u) := log |z + t(u)| − log t(u) = log(y csc u) − log(y cot u − x).                   (4)
    Let
                              m := Arg(z + 1) = Arg(λ),           M := Arg(z) = Arg(λ − 1).                        (5)
    As t ↓ 0, u(t) ↑ M ; as t ↑ 1, u(t) ↓ m. Thus
                                              t ∈ (0, 1]    ⇐⇒       u ∈ [m, M ).                                          (6)
    Lemma 5 (Log-modulus/argument reformulation). A nonreal λ satisfies (2) for some tk ∈ (0, 1] iff there exist
    uk ∈ [m, M ) such that
                                          u1 + u2 + u3 + u4 = 2π,                                            (7)
                                  F (u1 ) + F (u2 ) + F (u3 ) + F (u4 ) = 0.                                 (8)


                                                               18
                                   iuk
                                                                                      P
Proof.
P      Write z + tk = |z + tP k |e     with uk ∈ (0, π). Taking arguments in (2) gives uk ≡ 0 (mod 2π); since
   uk ∈ (0, 4π) this forces       uk = 2π, i.e. (7). Taking moduli and logs gives (8). Condition (6) is exactly
tk ∈ (0, 1]. Conversely, (7) and (8) give equality of arguments and moduli, hence (2).
Define
               n                                                    o                                       4
                                                                                                            X
           P := (u1 , . . . , u4 ) ∈ [m, M )4 : u1 + · · · + u4 = 2π ,             Ψ(u1 , . . . , u4 ) :=         F (uk ).    (9)
                                                                                                            k=1

Then λ is a nonreal eigenvalue of some A(α, β, γ, δ) iff P ̸= ∅ and 0 ∈ Ψ(P).
3) Necessarily 0 ≤ a ≤ 1 (indeed a < 1 if b ̸= 0). Every (u1 , . . . , u4 ) ∈ P has average π/2, so π/2 ∈ [m, M ),
i.e.
                                                     π
                                                m ≤ < M.                                                      (10)
                                                     2
For b > 0, m ≤ π/2 ⇐⇒ a ≥ 0. Also M > π/2 ⇐⇒ a < 1 because ℜ(λ − 1) = a − 1 < 0 iff a < 1. Thus
P ̸= ∅ implies
                                                 0 ≤ a < 1,                                                   (11)
hence in particular 0 ≤ a ≤ 1.
4) Strict convexity of F . Differentiate (4) using (3). A direct computation yields
                                                   x2 + y 2
                                F ′′ (u) =                         >0         (u ∈ (0, π)),                                  (12)
                                             (x − y cot u)2 sin2 u
so F is strictly convex on (0, π), hence on [m, M ).
5) Right boundary: a + b ≤ 1, and attainment of CR . P is convex and connected; Ψ is continuous, hence Ψ(P)
is an interval. By Jensen and strict convexity,
                                                        u + · · · + u 
                                                          1           4
                                Ψ(u1 , . . . , u4 ) ≥ 4F                 = 4F (π/2).                    (13)
                                                              4
Thus 0 ∈ Ψ(P) forces F (π/2) ≤ 0. Now
                                                                                  b 
                                    F (π/2) = log(y) − log(−x) = log                   ,
                                                                                  1−a
so F (π/2) ≤ 0 ⇐⇒ b ≤ 1 − a ⇐⇒ a + b ≤ 1. This proves item (2) in the theorem (for b > 0; for b < 0
replace b by |b|).
Attainment of CR : if t1 = t2 = t3 = t4 = x ∈ (0, 1], then (2) becomes (z + x)4 = x4 , i.e. λ = 1 − x ± ix,
attained by α = β = γ = δ = 1 − x.
6) A max principle on P. There are two regimes.
Lemma 6 (Unbounded supremum). If
                                                     3m + M ≤ 2π,                                                            (14)
then supP Ψ = +∞.
Proof. Take u4 ↑ M and u1 = u2 = u3 = (2π − u4 )/3. Condition (14) ensures u1 ≥ m. Also u4 < M
and u1 ≤ (2π − M )/3 ≤ M since M ≥ π/2 ⇒ 2π ≤ 4M . Hence (u1 , . . . , u4 ) ∈ P. As u4 ↑ M ,
t(u4 ) = y cot u4 − x ↓ 0, so − log t(u4 ) → +∞ while log(y csc u4 ) stays bounded; thus F (u4 ) → +∞ and
Ψ → +∞.
Lemma 7 (Finite maximum in the tight regime). If
                                     3m + M > 2π,            U := 2π − 3m < M,                                               (15)
then
                                               max Ψ = 3F (m) + F (U ),                                                      (16)
                                                 P
and equality holds iff (u1 , . . . , u4 ) is a permutation of (U, m, m, m).




                                                            19
                                                                              P
Proof. Order uk decreasing: v1 ≥ v2 ≥ v3 ≥ v4 . Since each vj ≥ m and             vj = 2π,
                                    v1 = 2π − (v2 + v3 + v4 ) ≤ 2π − 3m = U.
                             4
Thus (v1 , . . . , v4 ) ∈ [m, U ] with sum 2π. The vector (U, m, m, m) majorizes (v1 , . . . , v4 ). By Karamata (convex
F ),
                                             X 4
                                                 F (vj ) ≤ F (U ) + 3F (m),
                                           j=1

with equality only at permutations of (U, m, m, m) since F is strictly convex.

7) The inequality G(a, b) ≥ 0. We prove necessity for every nonreal eigenvalue.
7.1 Geometry lemma: G(a, b) ≤ 0 ⇒ 3m + M > 2π
Lemma 8. Assume b > 0 and 0 ≤ a ≤ 1. If G(a, b) ≤ 0, then 3m + M > 2π.
Proof. Set s = b2 . Then
                               G(a, b) = s2 + s(2a2 + 2a − 1) + (a2 + a)2 + 2a2 .                                    (17)
This is quadratic in s with discriminant
                       ∆ = (2a2 + 2a − 1)2 − 4 (a2 + a)2 + 2a2 = −(2a + 1)(6a − 1).
                                                                

Thus G(a, b) ≤ 0 forces ∆ > 0, hence a < 1/6, and s lies between the two real roots; in particular
                                          1               1p
                            s ≥ s− (a) := − a − a2 −         (1 − 6a)(1 + 2a).                                       (18)
                                          2               2
Case 1: a = 0. Then m = Arg(ib) = π/2 and M = Arg(−1 + ib) = π − arctan(b). Hence
                                         3π                   5π
                            3m + M =        + π − arctan(b) =    − arctan(b) > 2π.
                                          2                    2
Case 2: a > 0. From (18) one gets s > s− (a) ≥ 3a2 , with strictness because
                                            1                1p
                           s− (a) − 3a2 = − a − 4a2 −            (1 − 6a)(1 + 2a)
                                            2                2
                                                                                                                √
satisfies (LHS)2 − (RHS)2 = 32a3 (2a + 1) > 0 for a > 0. Hence b2 > 3a2 , i.e. tan m = b/a >                        3, so
m > π/3 and 3m − π ∈ (0, π/2).
                    b
Write ϕ := arctan 1−a  ∈ (0, π/2), so M = π − ϕ. Then
                                                                                      b
                           3m + M > 2π ⇐⇒ 3m − π > ϕ ⇐⇒ tan(3m) >                        ,                           (19)
                                                                                     1−a
since tan is increasing on (0, π/2) and tan(3m − π) = tan(3m).
                                                                                     3t−t3
Let t = tan m = b/a (allowed since a > 0). The triple-angle identity gives tan(3m) = 1−3t2 , and a direct

simplification yields
                                             b      b (4a3 − 3a2 − 4ab2 + b2 )
                                tan(3m) −        =                             .                     (20)
                                            1−a         a(a − 1)(a2 − 3b2 )
Here a > 0, a − 1 < 0, and a2 − 3b2 < 0 (since b2 > 3a2 ), so the denominator in (20) is positive. Hence the sign
equals the sign of
                       N (a, b) := 4a3 − 3a2 − 4ab2 + b2 = (1 − 4a)b2 + a2 (4a − 3).                         (21)
For a < 1/6, 1 − 4a > 0 and 4a − 3 < 0, so N (a, b) is strictly increasing in b2 and has a unique zero at
                                                            a2 (3 − 4a)
                                                 s0 (a) =               .                                            (22)
                                                              1 − 4a
One checks that s− (a) > s0 (a) for every a ∈ (0, 1/6): after multiplying by 1 − 4a > 0 and squaring, the
difference becomes 256a6 > 0. Therefore b2 ≥ s− (a) > s0 (a) implies N (a, b) > 0. By (20) and (19), this gives
3m + M > 2π.



                                                            20
7.2 Tight regime: max Ψ ≥ 0 ⇐⇒ G ≥ 0
Assume 3m + M > 2π, so Lemma 7 applies with U = 2π − 3m ∈ (0, π) and maximizer (U, m, m, m). Since
u(1) = Arg(z + 1) = m, (6) gives t(m) = 1, hence
                                      F (m) = log |z + 1| − log 1 = log |λ|.                             (23)
Also t(U ) = b cot U − (a − 1) = b cot U + 1 − a and |z + t(U )| = b csc U , so by (16)
                                                                                   |λ|3 b csc U
                                                                                               
             max Ψ = 3 log |λ| + log(b csc U ) − log(b cot U + 1 − a) = log                       .      (24)
               P                                                                b cot U + 1 − a
Thus maxP Ψ ≥ 0 is equivalent to
                                 |λ|3 b csc U ≥ b cot U + 1 − a.                        (25)
                                                                  3          3    3     2
Now U = 2π − 3m, so sin U = − sin(3m) and cos U = cos(3m). Since λ = (a + ib) = (a − 3ab ) +
i(3a2 b − b3 ), we have
                               ℜ(λ3 )   a(a2 − 3b2 )                           ℑ(λ3 )   b(3a2 − b2 )
                  cos(3m) =        3
                                      =              ,            sin(3m) =           =              .   (26)
                                |λ|         |λ|3                                |λ| 3       |λ|3
Hence
                                          b(b2 − 3a2 )                      a(a2 − 3b2 )
                                sin U =                ,          cos U =                .               (27)
                                              |λ|3                              |λ|3
In the tight regime one necessarily has m > π/3 (since M ≤ π), hence b2 − 3a2 > 0, so sin U > 0 and
                                                |λ|3                        a(a2 − 3b2 )
                                b csc U =                ,     b cot U =                 .               (28)
                                              b2 − 3a2                       b2 − 3a2
Substitute (28) into (25) and clear the positive denominator b2 − 3a2 :
                                   |λ|6 ≥ a(a2 − 3b2 ) + (1 − a)(b2 − 3a2 ).                             (29)
Using |λ|2 = a2 + b2 , a direct expansion and factorization yields
                                                               
                   |λ|6 − a(a2 − 3b2 ) + (1 − a)(b2 − 3a2 ) = (a − 1)2 + b2 G(a, b).
                                                                           
                                                                                                         (30)

Since (a − 1)2 + b2 = |λ − 1|2 > 0, (29) is equivalent to G(a, b) ≥ 0. Therefore, in the tight regime,
                                       max Ψ ≥ 0             ⇐⇒     G(a, b) ≥ 0.                         (31)
                                          P

7.3 Necessity of G ≥ 0 for all nonreal eigenvalues
Let λ be a nonreal eigenvalue of some A(α, β, γ, δ). Then P ̸= ∅ and 0 ∈ Ψ(P), hence supP Ψ ≥ 0. If
3m + M ≤ 2π, Lemma 8 (contrapositive) gives G(a, b) ≥ 0. If 3m + M > 2π, then sup Ψ = max Ψ and (31)
gives G(a, b) ≥ 0. This proves item (3) in the theorem.
8) Boundary identification and sharpness.
8.1 Right boundary CR
Already established in §5.
8.2 Left boundary CL : attainment by AL (α), and G = 0
For
                                         α 1−α 0 0
                                                      
                                      0       0   1 0
                             AL (α) =                   ,                    α ∈ [0, 1),
                                         0     0   0 1
                                         1     0   0 0
we have β = γ = δ = 0, so (1) reduces to
                                                 λ3 (λ − α) = 1 − α.                                     (32)
Eliminate α:
                                                             λ4 − 1
                                                       α=           .                                    (33)
                                                             λ3 − 1


                                                             21
                   4
Thus α ∈ R iff ℑ λλ3 −1
                        
                     −1 = 0. Compute
                                                                 
                                              ℑ (λ4 − 1)(λ3 − 1)
                                    4    
                                     λ −1
                                 ℑ 3        =                      .
                                     λ −1          |λ3 − 1|2
A direct expansion and factorization in λ = a + ib gives, for b ̸= 0,
                                          4
                                                       b |λ − 1|2 G(a, b)
                                                 
                                           λ −1
                                       ℑ 3          =                     .                               (34)
                                           λ −1             |λ3 − 1|2
Hence, for b ̸= 0,
                                         α ∈ R ⇐⇒ G(a, b) = 0.                                            (35)
So every nonreal eigenvalue of AL (α) lies on G = 0.
Moreover, AL (α) always has a nonreal conjugate pair: rewrite (32) as
                                                                         
                λ4 − αλ3 − (1 − α) = 0 ⇐⇒ (λ − 1) λ3 + (1 − α)(λ2 + λ + 1) = 0.

Let c = 1 − α ∈ (0, 1] and f (λ) = λ3 + c(λ2 + λ + 1). Then
                                             f ′ (λ) = 3λ2 + 2cλ + c
has discriminant 4c(c − 3) < 0, so f is strictly increasing on R. Also f (0) = c > 0 and f (λ) → −∞ as λ → −∞,
hence f has exactly one real root. Therefore the remaining two roots of f form a nonreal conjugate pair.
Endpoints: at α = 0, (32) becomes λ4 = 1, giving λ = i. As α ↑ 1, (32) tends to λ3 (λ − 1) = 0; the conjugate
pair among the three non-1 roots tends to 0. Thus α ∈ [0, 1) traces a connected arc of G = 0 from i to 0.
Finally, every point on that arc is attained as follows. Let λ = a + ib with b > 0, 0 ≤ a ≤ 1, a + b ≤ 1, and
G(a, b) = 0. By Lemma 8 (since G = 0 ≤ 0), we are in the tight regime 3m + M > 2π, so Lemma 7 applies
and the maximizer is (U, m, m, m) with U = 2π − 3m ∈ [m, M ). By (31), G = 0 implies maxP Ψ = 0, hence
Ψ(U, m, m, m) = 0. By Lemma 5 this produces t1 = t(U ) ∈ (0, 1] and t2 = t3 = t4 = t(m) = 1, satisfying (2).
Therefore the corresponding parameters
                                   α = 1 − t(U ) ∈ [0, 1),      β=γ=δ=0
yield exactly AL (α) and give λ as an eigenvalue. This identifies CL and proves it is attained.
9) Existence for every strict interior point. Fix λ = a + ib with b > 0 such that
                                  0 ≤ a ≤ 1,       a + b < 1,         G(a, b) > 0.                        (36)
Define z, m, M, F, P, Ψ as above. Then P ̸= ∅ by (10)–(11).
We show 0 ∈ Ψ(P). By Jensen (13),
                                                                              b 
                            Ψ(π/2, π/2, π/2, π/2) = 4F (π/2) = 4 log               <0
                                                                              1−a
since a + b < 1 ⇐⇒ b < 1 − a.
To produce a positive value: if 3m + M ≤ 2π, Lemma 6 gives supP Ψ = +∞, so Ψ takes positive values. If
3m + M > 2π, Lemma 7 gives maxP Ψ = 3F (m) + F (U ); by (31), G(a, b) > 0 implies maxP Ψ > 0, so Ψ
takes positive values.
Since P is connected and Ψ is continuous, Ψ(P) is an interval containing both negative and positive values,
hence contains 0. Thus there exists (u1 , . . . , u4 ) ∈ P with Ψ(u1 , . . . , u4 ) = 0. By Lemma 5 this yields
tk = t(uk ) ∈ (0, 1] satisfying (2). Set
                        α = 1 − t1 ,    β = 1 − t2 ,   γ = 1 − t3 ,     δ = 1 − t4 ∈ [0, 1),
and then (1) holds, so λ ∈ σ(A(α, β, γ, δ)). Conjugation gives the lower half-plane.




                                                        22
C




    Third version
    Throughout, fix
                                        α        1−α       0         0
                                                                       
                                       0         β       1−β        0 
                      A(α, β, γ, δ) =                                    ,      α, β, γ, δ ∈ [0, 1).
                                        0         0        γ       1 − γ
                                       1−δ        0        0         δ
    This is row-stochastic (row sums are 1) and real. We write λ = a + ib, and b+ = |b|.

    Theorem (Spectral region for a 4-cycle row-stochastic matrix)
    Let λ = a + ib ∈ σ(A(α, β, γ, δ)) with b ̸= 0. Then:
          1. 0 ≤ a ≤ 1.
          2. a + b+ ≤ 1.
          3. Define for b ≥ 0:
                                                G(a, b) := (b2 + a2 + a)2 + 2a2 − b2 .
             Then G(a, b+ ) ≥ 0.
    Conversely, if b > 0 and
                                         0 ≤ a ≤ 1,       a + b < 1,      G(a, b) > 0,
    then there exist α, β, γ, δ ∈ [0, 1) such that λ ∈ σ(A(α, β, γ, δ)). (The lower half-plane follows by conjugation.)
    Moreover:
           • The segment CR : λ = 1 − x + ix (x ∈ [0, 1]) is attained by α = β = γ = δ = 1 − x.
           • The curve portion CL in the upper half-plane joining i to 0 defined by G(a, b) = 0 is attained by
                                                        α 1−α 0 0
                                                                        
                                                      0      0      1 0
                                           AL (α) =                        ,     α ∈ [0, 1).
                                                        0     0      0 1
                                                        1     0      0 0

           • Every point strictly inside {b > 0, 0 ≤ a ≤ 1, a + b < 1, G(a, b) > 0} is attained.

    Proof
    Because A is real, λ ∈ σ(A) ⇒ λ ∈ σ(A). So it suffices to prove all necessary conditions for b > 0, and then
    replace b by |b| for the final statements. The constructive (“converse”) part will also be done for b > 0.
    1) Eigenvalue equation ⇒ multiplicative constraint
    Let v = (v1 , v2 , v3 , v4 )⊤ ̸= 0 satisfy Av = λv. Writing the eigenvalue equation row-by-row gives:
                                                αv1 + (1 − α)v2 = λv1 ,
                                                βv2 + (1 − β)v3 = λv2 ,
                                                γv3 + (1 − γ)v4 = λv3 ,
                                                 (1 − δ)v1 + δv4 = λv4 .
    Rearrange each:
                                                 (λ − α)v1 = (1 − α)v2 ,
                                                 (λ − β)v2 = (1 − β)v3 ,
                                                                                                                  (1.1)
                                                 (λ − γ)v3 = (1 − γ)v4 ,
                                                 (λ − δ)v4 = (1 − δ)v1 .


                                                            23
Claim: none of v1 , v2 , v3 , v4 is zero.
Because α, β, γ, δ ∈ [0, 1), we have 1 − α, 1 − β, 1 − γ, 1 − δ > 0. If v1 = 0, then from the first equation
(1 − α)v2 = 0 ⇒ v2 = 0. Then second gives v3 = 0, third gives v4 = 0, contradicting v ̸= 0. The same cyclically
holds for any vk = 0. Hence v1 v2 v3 v4 ̸= 0.
Now multiply the four equations in (1.1). The left-hand side is
                                    (λ − α)(λ − β)(λ − γ)(λ − δ) v1 v2 v3 v4 ,
and the right-hand side is
                                      (1 − α)(1 − β)(1 − γ)(1 − δ) v1 v2 v3 v4 .
Cancel v1 v2 v3 v4 ̸= 0 to obtain the necessary condition:
                        (λ − α)(λ − β)(λ − γ)(λ − δ) = (1 − α)(1 − β)(1 − γ)(1 − δ).                          (1.2)
Conversely, if (1.2) holds and additionally λ ̸= α, β, γ, δ, one can solve the relations in (1.1) recursively for v
and check the final equation closes exactly when (1.2) holds. In our nonreal case λ ∈ / R, while α, β, γ, δ ∈ R, so
automatically λ ̸= α, β, γ, δ. Thus (1.2) is equivalent to existence of a nonzero eigenvector for nonreal λ.
2) Substitute tk = 1 − parameter and shift z = λ − 1
Define
                                t1 = 1 − α, t2 = 1 − β, t3 = 1 − γ, t4 = 1 − δ.
Since each parameter lies in [0, 1), each tk ∈ (0, 1]. Let z = λ − 1. Then
                                       λ − (1 − tk ) = λ − 1 + tk = z + tk .
Also
                                    (1 − α)(1 − β)(1 − γ)(1 − δ) = t1 t2 t3 t4 .
So (1.2) becomes:
                              (z + t1 )(z + t2 )(z + t3 )(z + t4 ) = t1 t2 t3 t4 .                     (2.1)
Write z = x + iy with x = a − 1 and y = b. We assume b > 0 in the rest of the necessity direction; later we
replace by |b|.
3) Argument parametrization: t ↔ u = arg(z + t)
Fix z = x + iy with y > 0. For any t > 0, the complex number z + t = (x + t) + iy lies in the upper half-plane,
so its argument u(t) := arg(z + t) is well-defined in (0, π).
3.1 Inverse formulas t = t(u), |z + t(u)|
Let u ∈ (0, π). Consider z + t = (x + t) + iy with argument u. Then
                                                      ℑ(z + t)    y
                                           tan u =             =     .
                                                      ℜ(z + t)   x+t
Since y > 0, this determines x + t uniquely:
                                     x + t = y cot u    ⇒     t = y cot u − x.                                (3.1)
Also
                    |z + t|2 = (x + t)2 + y 2 = (y cot u)2 + y 2 = y 2 (cot2 u + 1) = y 2 csc2 u,
So
                                               |z + t(u)| = y csc u.                                          (3.2)
3.2 Endpoints m = arg(z + 1), M = arg(z), and monotone correspondence
Define
                         m := arg(z + 1) = arg(λ),       M := arg(z) = arg(λ − 1).                     (3.3)
                                                                      
                                                                    y                                  y
Claim: u(t) is strictly decreasing in t > 0. Indeed, u(t) = arctan x+t   , and for y > 0 the function x+t is
strictly decreasing in t, hence arctan of it is strictly decreasing. Therefore as t ↓ 0, u(t) ↑ u(0) = arg(z) = M ;
and as t ↑ 1, u(t) ↓ u(1) = arg(z + 1) = m. Hence the mapping t 7→ u(t) is a continuous strictly decreasing
bijection from (0, 1] onto [m, M ). Equivalently:
                                         t ∈ (0, 1]    ⇐⇒     u ∈ [m, M ).                                    (3.4)


                                                         24
4) The function F and reformulation in (uk )
Define for u ∈ [m, M ):
                                       F (u) := log |z + t(u)| − log t(u).
Using (3.1)–(3.2) this becomes explicitly
                                        F (u) = log(y csc u) − log(y cot u − x).                                         (4.1)
Note t(u) = y cot u − x > 0 on [m, M ) by construction.
5) Lemma 1 (exact equivalence of eigenvalue condition)
Lemma 9. A nonreal λ satisfies (2.1) for some t1 , t2 , t3 , t4 ∈ (0, 1] if and only if there exist u1 , u2 , u3 , u4 ∈ [m, M )
such that
                                            u1 + u2 + u3 + u4 = 2π,                                                       (5.1)
                                    F (u1 ) + F (u2 ) + F (u3 ) + F (u4 ) = 0.                                            (5.2)
Proof. (⇒) Suppose (2.1) holds with tk ∈ (0, 1]. For each k, let uk = arg(z + tk ) ∈ (0, π). Because tk ∈ (0, 1],
by (3.4) we have uk ∈ [m, M ). Write z + tk = |z + tk |eiuk . Then the left side of (2.1) has argument u1 + · · · + u4
(mod 2π), while the right side t1 t2 t3 t4 > 0 has argument 0 (mod 2π). Thus u1 +· · ·+u4 ≡ 0 (mod 2π). But each
uk ∈ (0, π), so the sum lies strictly in (0, 4π). The only multiple of 2π in (0, 4π) is 2π. Hence u1 + · · · + u4 = 2π,
proving (5.1). Taking moduli in (2.1): |z + t1 | · · · |z + t4 | = t1 t2 t3 t4 . Take log of both sides:
                        4
                        X                       4
                                                X                 4 
                                                                  X                           
                              log |z + tk | =         log tk ⇐⇒         log |z + tk | − log tk = 0.
                        k=1                     k=1               k=1

But log |z + tk | − log tk = F (uk ) by definition, so (5.2) holds.
(⇐) Conversely, suppose uk ∈ [m, M ) satisfy (5.1)–(5.2). Define tk = t(uk ). Then by (3.4), tk ∈ (0, 1]. Also
z + tk = |z + tk |eiuk . Multiply:
               4                 4
                                             !          4           4
                                                                               !       4
             Y                  Y                    X            Y                  Y
                  (z + tk ) =       |z + tk | exp i        uk =       |z + tk | ei2π =   |z + tk |.
              k=1                 k=1                      k=1           k=1                     k=1
              Q                                      Q                               P             P
So the product (z+tk ) is positive real, with modulus |z+tk |. Equation (5.2) implies log |z+tk | = log tk ,
       Q          Q                  Q4               Q4
hence |z + tk | = tk . Therefore k=1 (z + tk ) = k=1 tk , which is exactly (2.1).
6) The feasible set P , its convexity/connectedness, and Ψ(P ) is an interval
Let
                           P := (u1 , u2 , u3 , u4 ) ∈ [m, M )4 : u1 + u2 + u3 + u4 = 2π ,
                               
                            P4
and Ψ(u1 , u2 , u3 , u4 ) := k=1 F (uk ).
6.1 P is convex and connected
The set [m, M )4 ⊂ R4 is convex. The affine hyperplane H := {u ∈ R4 :
                                                                      P
                                                                        uk = 2π} is convex. An intersection
of convex sets is convex, so P = [m, M ) ∩ H is convex. Any convex subset of Rn is path-connected (connect
                                         4

points by line segment), hence connected.
6.2 Ψ(P ) ⊂ R is an interval
Ψ is continuous because F is continuous on [m, M ) (all terms in (4.1) are continuous there since t(u) > 0).
Continuous image of a connected set in R is connected; connected subsets of R are intervals. Hence Ψ(P ) is an
interval. By Lemma 1:
                     λ nonreal eigenvalue of some A(α, β, γ, δ) ⇐⇒ P ̸= ∅ and 0 ∈ Ψ(P ).                                 (6.1)
7) Necessarily 0 ≤ a ≤ 1 (and in fact a < 1 when b ̸= 0)
Assume b > 0 and P ̸= ∅. Pick (u1 , . . . , u4 ) ∈ P . Then their average is u1 +···+u
                                                                                  4
                                                                                       4
                                                                                         = 2π   π
                                                                                            4 = 2 . Since each
uk ∈ [m, M ), the interval [m, M ) must contain π/2. That is:
                                                       π
                                                 m ≤ < M.                                                 (7.1)
                                                       2



                                                             25
Now compute what m ≤ π/2 means. Recall m = arg(λ) = arg(a + ib), b > 0. For b > 0, arg(a + ib) ≤ π/2
holds exactly when a ≥ 0 (points in upper half-plane with angle at most π/2 are those with nonnegative real part).
Hence:
                                                   π
                                             m≤       ⇐⇒ a ≥ 0.                                             (7.2)
                                                   2
Next, M > π/2 where M = arg(z) = arg((a − 1) + ib). Since b > 0, we have arg((a − 1) + ib) > π/2 exactly
when a − 1 < 0, i.e., a < 1. Thus:
                                                   π
                                             M>       ⇐⇒ a < 1.                                             (7.3)
                                                   2
Combining (7.1)–(7.3), P ̸= ∅ ⇒ 0 ≤ a < 1. In particular 0 ≤ a ≤ 1. This proves item (1).
8) Strict convexity of F
We show F ′′ (u) > 0 on (0, π), hence F is strictly convex on [m, M ) ⊂ (0, π). Recall F (u) = log(y csc u) −
log(y cot u − x), y > 0. Differentiate. First term:
                               d                 d                        d
                                 log(y csc u) =    (log y + log csc u) =    log csc u.
                              du                du                       du
       d
Since du                                d
         csc u = − csc u cot u, we get du log csc u = − csc u cot u
                                                          csc u     = − cot u. So
                                                 d
                                                   log(y csc u) = − cot u.                                     (8.1)
                                                du
                                                                          ′
Second term: define g(u) = y cot u − x. Then du  d
                                                   log g(u) = gg(u)(u)          d
                                                                       . Since du cot u = − csc2 u, we have
g ′ (u) = −y csc2 u. Therefore
                                   d                        −y csc2 u
                                      log(y cot u − x) =                .                              (8.2)
                                  du                       y cot u − x
Thus
                                                           y csc2 u
                                    F ′ (u) = − cot u +               .                                (8.3)
                                                         y cot u − x
                                           2
Differentiate again. Write h(u) = yycot
                                     csc u          ′′        2     ′                   d                2
                                        u−x . Then F (u) = csc u + h (u) (8.4) because du (− cot u) = csc u.
                                                                                                           ′      ′
Compute h′ (u) via quotient rule. Let p(u) = y csc2 u, q(u) = y cot u − x. Then h = p/q, so h′ = p q−pq
                                                                                                    q2  .
         ′               2               ′             2
Compute p (u) = −2y csc u cot u. Also q (u) = −y csc u.
                                 (−2y csc2 u cot u)(y cot u − x) − (y csc2 u)(−y csc2 u)
                          h′ =                                                           .
                                                      (y cot u − x)2
                        y csc2 u[−2 cot u(y cot u−x)+y csc2 u]
Factor y csc2 u: h′ =                (y cot u−x)2              . Use csc2 u = 1 + cot2 u:

                        −2 cot u(y cot u − x) + y(1 + cot2 u) = y − y cot2 u + 2x cot u.
So
                                               y csc2 u(y − y cot2 u + 2x cot u)
                                       h′ =                                      .                             (8.5)
                                                         (y cot u − x)2
Now combine with F ′′ = csc2 u + h′ . Put over common denominator:
                                                 !
  ′′        2         y y − y cot2 u + 2x cot u          2     (y cot u − x)2 + y(y − y cot2 u + 2x cot u)
 F (u) = csc u 1 +                                  = csc  u ·                                             .
                             (y cot u − x)2                                   (y cot u − x)2

Expand the numerator: (y cot u − x)2 = y 2 cot2 u − 2xy cot u + x2 . And y(y − y cot2 u + 2x cot u) =
y 2 − y 2 cot2 u + 2xy cot u. Sum: (y 2 cot2 u − 2xy cot u + x2 ) + (y 2 − y 2 cot2 u + 2xy cot u) = x2 + y 2 .
Therefore
                                                  x2 + y 2             x2 + y 2
                           F ′′ (u) = csc2 u ·                =                       .                 (8.6)
                                               (y cot u − x)2
                                                                (y cot u − x)2 sin2 u
Since x2 + y 2 > 0 (because y > 0) and the denominator is positive on (0, π), we conclude F ′′ (u) > 0 for all
u ∈ (0, π). So F is strictly convex.



                                                            26
9) Right boundary: necessity of a + b ≤ 1, and attainment of CR
Assume b > 0, P ̸= ∅, and 0 ∈ Ψ(P ).
9.1 Jensen inequality step (fully justified)
Let (u1 , . . . , u4 ) ∈ P . Since F is convex on [m, M ), Jensen’s inequality gives 14                    1
                                                                                        P                      P     
                                                                                          F (uk ) ≥ F      4       uk .
Multiply by 4:
                                          4               
                                         X                2π          π
                                            F (uk ) ≥ 4F        = 4F       .                                   (9.1)
                                                           4            2
                                        k=1
If 0 ∈ Ψ(P ), then inf Ψ ≤ 0. But (9.1) shows Ψ ≥ 4F (π/2) on P. Therefore 4F (π/2) ≤ 0, i.e., F (π/2) ≤ 0.
                      P
                                                                                                               (9.2)
9.2 Compute F (π/2) and deduce a + b ≤ 1
                                    − log(y cot(π/2) − x) = log(y) − log(−x). Since y = b, x = a − 1, so
Using (4.1): F (π/2) = log(y csc(π/2))
                                           b                                       b
−x = 1 − a. Hence F (π/2) = log           1−a   . So F (π/2) ≤ 0 is equivalent to 1−a ≤ 1 ⇐⇒ b ≤ 1 − a ⇐⇒
a + b ≤ 1. This proves item (2) for b > 0. By conjugation symmetry, for b < 0 it becomes a + |b| ≤ 1.
9.3 Attainment of segment CR
                                                                                                          π
Let x ∈ (0, 1] and choose α = β = γ = δ = 1 − x ∈ [0, 1). Then (2.1) reads (z + x)4 = x4 . So z + x = xei 2 k .
The nonreal solutions correspond to k = 1, 3: z + x = ±ix ⇒ λ = 1 − x ± ix. Thus the segment λ = 1 − x + ix
for x ∈ [0, 1] is attained.
10) Two regimes for supP Ψ: Lemmas 2 and 3 proved in full
Lemma 10 (Unbounded supremum). If 3m + M ≤ 2π, then supP Ψ = +∞.
Proof. Fix u4 ∈ [m, M ). Define u1 = u2 = u3 = 2π−u 3
                                                      4
                                                        . For u4 sufficiently close to M , (u1 , u2 , u3 , u4 ) ∈ P .
As u4 ↑ M , t(u4 ) ↓ 0, so F (u4 ) → +∞. Meanwhile u1 → (2π − M )/3 ∈ (m, M ), so F (u1 ) is bounded. Thus
Ψ → +∞.
Lemma 11 (Finite maximum in the tight regime). If 3m + M > 2π and we define U := 2π − 3m, then U < M ,
and
                                        max Ψ = 3F (m) + F (U ),                                 (10.3)
                                                P
with equality iff (u1 , u2 , u3 , u4 ) is a permutation of (U, m, m, m).
Proof. 3m + M > 2π ⇒ 2π − 3m < M . So U ∈ [m, M ). By symmetry, we rearrange (uk ) to nonincreasing
v1 ≥ v2 ≥ v3 ≥ v4 . Then v1 ≤ 2π − 3m = U . Every feasible ordered vector lies in a compact set majorized
by x = (U, m, m, m). By Karamata’s inequality and strict convexity of F , the sum is maximized at x. Thus
maxP Ψ = 3F (m) + F (U ).
11) Necessity of G(a, b) ≥ 0
11.1 A geometry/algebra lemma: G ≤ 0 ⇒ 3m + M > 2π (Lemma 4)
Lemma 12. Assume b > 0 and 0 ≤ a ≤ 1. If G(a, b) ≤ 0, then 3m + M > 2π.
Proof. Let s = b2 . G(a, b) = s2 + s(2a2 + 2a − 1) + (a2 + a)2 + 2a2 (11.1). G ≤ 0 implies s lies between
roots of the quadratic. The discriminant ∆ = −(2a + 1)(6a − 1). So ∆ > 0 iff a < 1/6. Case a = 0:
3m + M = 3(π/2) + π − arctan(b) > 2π. Case a > 0: We show b2 > 3a2 , which implies m > π/3. Let
                                               b
tan m = b/a. We want to show tan(3m) > 1−a        . Using triple-angle identity and substituting t = b/a, we find
the sign of the difference depends on N (a, b) = 4a3 − 3a2 − 4ab2 + b2 . Using s ≥ s− (a), algebraic expansion
shows s− (a) > s0 (a) where s0 is the root of N . Hence N (a, b) > 0, which confirms 3m + M > 2π.
11.2 Tight regime: compute maxP Ψ explicitly and relate it to G
                                  3            
In the tight regime, maxP Ψ = log b|λ|  b csc U
                                    cot U +1−a (11.25). Substituting trigonometric identities for csc U, cot U
in terms of a, b yields |λ|6 ≥ a(a2 − 3b2 ) + (1 − a)(b2 − 3a2 ). This factors as |λ − 1|2 G(a, b) ≥ 0. Thus,
maxP Ψ ≥ 0 ⇐⇒ G(a, b) ≥ 0. (11.39).




                                                            27
11.3 Finish necessity of G(a, b) ≥ 0
If λ is a nonreal eigenvalue, then supP Ψ ≥ 0. If 3m + M ≤ 2π, Lemma 4 contraposition implies G(a, b) > 0. If
3m + M > 2π, the tight regime applies and G(a, b) ≥ 0. This proves item (3).
12) Left boundary CL: attainment by AL (α) and equivalence to G = 0
                                                                                   4
For AL (α), the characteristic equation is λ3 (λ − α) = 1 − α. For nonreal λ, α = λλ3 −1
                                                                                      −1 (12.2). The imaginary
                     2
part is ℑ( pq ) = b|λ−1|  G(a,b)
                     |λ3 −1|2    . Thus ℑ(α) = 0 ⇐⇒ G(a, b) = 0. Factoring the equation as (λ − 1)[λ3 + (1 −
      2
α)(λ + λ + 1)] = 0, one finds exactly one real root and a conjugate pair for α ∈ [0, 1). At α = 0, λ = i. As
α → 1, λ → 0.
13) Every strict interior point is attained (constructive existence)
Fix λ satisfying 0 ≤ a ≤ 1, a + b < 1, G(a, b) > 0. P is non-empty as π/2 ∈ [m, M ). Ψ(π/2, . . . , π/2) =
        b
4 log( 1−a ) < 0 since a + b < 1. Conversely, supP Ψ > 0 because G(a, b) > 0 (using either regime). By
the Intermediate Value Theorem on the convex set P , there exists a point where Ψ = 0, which corresponds to
parameters α, β, γ, δ ∈ [0, 1).

Summary
For any nonreal eigenvalue λ = a + ib of some 4-cycle row-stochastic matrix, we have proved 0 ≤ a ≤ 1,
a + |b| ≤ 1, and G(a, |b|) ≥ 0. Conversely, strict interior points are realized. The boundaries CR and CL are
attained by specific matrix families.




                                                     28
D

    Final version
    Theorem 23 (Spectral region for a 4-cycle row-stochastic matrix). Fix
                                         α      1−α       0       0
                                                                     
                                      0         β     1−β        0 
                    A(α, β, γ, δ) =                                    ,          α, β, γ, δ ∈ [0, 1).
                                          0      0        γ     1 − γ
                                        1−δ      0        0       δ
    Let λ = a + ib ∈ σ(A(α, β, γ, δ)) with b ̸= 0, and write b+ = |b|. Then:
          1. 0 ≤ a ≤ 1.
          2. a + b+ ≤ 1.
          3. For b ≥ 0 define
                                                G(a, b) := (b2 + a2 + a)2 + 2a2 − b2 .
             Then G(a, b+ ) ≥ 0.
    Conversely, if b > 0 and
                                         0 ≤ a ≤ 1,       a + b < 1,      G(a, b) > 0,
    then there exist α, β, γ, δ ∈ [0, 1) such that λ ∈ σ(A(α, β, γ, δ)). (The lower half-plane follows by conjugation.)
    Moreover:
           • The segment CR : λ = 1 − x + ix (x ∈ [0, 1]) is attained by α = β = γ = δ = 1 − x.
           • The curve portion CL in the upper half-plane joining i to 0 defined by G(a, b) = 0 is attained by the
             family
                                                        α 1−α 0 0
                                                                        
                                                      0      0      1 0
                                           AL (α) =                        ,     α ∈ [0, 1).
                                                        0     0      0 1
                                                        1     0      0 0
           • Every point strictly inside {b > 0, 0 ≤ a ≤ 1, a + b < 1, G(a, b) > 0} is attained.
    Proof. Because A is real, λ ∈ σ(A) ⇒ λ ∈ σ(A). Thus it suffices to prove the necessary conditions for b > 0 and
    then replace b by |b| in the final statements. The constructive (converse) direction will also be proved for b > 0.

1) Eigenvalue equation ⇒ a multiplicative constraint. Let v = (v1 , v2 , v3 , v4 )⊤ ̸= 0 satisfy Av = λv. Writing
the eigenvalue equation row-by-row:
                                                  αv1 + (1 − α)v2 = λv1 ,
                                                  βv2 + (1 − β)v3 = λv2 ,
                                                  γv3 + (1 − γ)v4 = λv3 ,
                                                   (1 − δ)v1 + δv4 = λv4 .
    Rearrange:
      (λ − α)v1 = (1 − α)v2 ,      (λ − β)v2 = (1 − β)v3 ,      (λ − γ)v3 = (1 − γ)v4 ,    (λ − δ)v4 = (1 − δ)v1 . (1)
    Claim 1. If λ ∈
                  / R and α, β, γ, δ ∈ [0, 1) then v1 v2 v3 v4 ̸= 0 for every eigenvector v ̸= 0.
    Proof. Because α, β, γ, δ ∈ [0, 1) we have 1 − α, 1 − β, 1 − γ, 1 − δ > 0. If v1 = 0 then the first equation in (1)
    gives (1 − α)v2 = 0 hence v2 = 0. Then the second gives v3 = 0, the third gives v4 = 0, contradicting v ̸= 0.
    Cyclically the same holds for any coordinate, so no vk can vanish.
    Multiply the four equalities in (1) and cancel v1 v2 v3 v4 ̸= 0 (Claim 1):
                            (λ − α)(λ − β)(λ − γ)(λ − δ) = (1 − α)(1 − β)(1 − γ)(1 − δ).                             (2)
    Conversely, if λ ∈/ R and (2) holds, then λ ̸= α, β, γ, δ (since α, β, γ, δ ∈ R), and one can solve (1) recursively:
                                                 λ−β            λ−γ
    choose v1 ̸= 0, set v2 = λ−α
                              1−α v1 , then v3 = 1−β v2 , v4 = 1−γ v3 ; the final equation closes exactly when (2) holds.
    Thus for nonreal λ, (2) is equivalent to λ ∈ σ(A) for some choice of parameters.



                                                              29
2) Substitute tk = 1 − parameter and shift z = λ − 1. Define
                             t1 = 1 − α, t2 = 1 − β, t3 = 1 − γ, t4 = 1 − δ.
Then each tk ∈ (0, 1]. Set z = λ − 1. Then
                     λ − (1 − tk ) = z + tk ,      (1 − α)(1 − β)(1 − γ)(1 − δ) = t1 t2 t3 t4 .
So (2) becomes
                                  (z + t1 )(z + t2 )(z + t3 )(z + t4 ) = t1 t2 t3 t4 .                            (3)
Write z = x + iy with
                                    x = Re(z) = a − 1,          y = Im(z) = b.
In the necessity direction we assume b = y > 0.
3) Argument parametrization: t ↔ u = Arg(z + t). Fix z = x + iy with y > 0. For any t > 0, the point
z + t = (x + t) + iy lies in the open upper half-plane, so its argument u(t) = Arg(z + t) is well-defined and
belongs to (0, π).
3.1) Inverse formulas. Given u ∈ (0, π) and z + t = (x + t) + iy with Arg(z + t) = u, we have
                               y
                   tan u =            =⇒ x + t = y cot u =⇒ t = t(u) := y cot u − x.
                             x+t
Also
                   |z + t|2 = (x + t)2 + y 2 = (y cot u)2 + y 2 = y 2 (cot2 u + 1) = y 2 csc2 u,
hence
                                               |z + t(u)| = y csc u.
3.2) Endpoints and monotonicity. Define
                         m := Arg(z + 1) = Arg(λ),            M := Arg(z) = Arg(λ − 1).
                            y          y
                               
Because u(t) = arctan x+t and x+t is strictly decreasing in t, the map t 7→ u(t) is continuous and strictly
decreasing on (0, ∞). In particular, on t ∈ (0, 1] it is a continuous strictly decreasing bijection onto u ∈ [m, M ):
                                         t ∈ (0, 1] ⇐⇒ u ∈ [m, M ).                                               (4)
(As t ↑ 1, u(t) ↓ m; as t ↓ 0, u(t) ↑ M .)
4) The function F and reformulation. For u ∈ [m, M ) define
                    F (u) := log |z + t(u)| − log t(u) = log(y csc u) − log(y cot u − x).
Note t(u) > 0 on [m, M ) by construction.
5) Exact equivalence of eigenvalue condition in terms of (uk ).
Lemma 13 (Exact equivalence). A nonreal λ satisfies (3) for some t1 , t2 , t3 , t4 ∈ (0, 1] if and only if there exist
u1 , u2 , u3 , u4 ∈ [m, M ) such that
                                                       u1 + u2 + u3 + u4 = 2π,                                     (5)
                                      F (u1 ) + F (u2 ) + F (u3 ) + F (u4 ) = 0.                                   (6)
Proof. (⇒) Assume (3) holds with tk ∈ (0, 1]. Let uk = Arg(z + tk ) ∈ (0, π). Because tk ∈ (0, 1], (4) gives
uk ∈ [m, M ). Write z + tk = |z + tk |eiuk . The left side of (3) has argument u1 + · · · + u4 modulo 2π; the right
side t1 t2 t3 t4 > 0 has argument 0 modulo 2π. Hence u1 + · · · + u4 ≡ 0 (mod 2π). Since each uk ∈ (0, π), the
sum lies in (0, 4π), so the only
                              Q possible multiple
                                            Q       of 2π is 2π, proving (5).
Taking moduli in (3) gives |z + tk | = tk . Take logs:
                     4
                     X                       4
                                             X                    4
                                                                  X                           
                           log |z + tk | =         log tk   ⇐⇒          log |z + tk | − log tk = 0.
                     k=1                     k=1                  k=1
But by definition F (uk ) = log |z + tk | − log tk , so (6) holds.
(⇐) Conversely, assume uk ∈ [m, M ) satisfy (5)–(6). Define tk = t(uk ). Then tk ∈ (0, 1] by (4). Also
z + tk = |z + tk |eiuk . Multiply:
                   Y4              Y 4             P         Y  4                 4
                                                                                      Y
                       (z + tk ) =        |z + tk | ei uk =          |z + tk | ei2π =   |z + tk |.
                   k=1                k=1                         k=1                   k=1
     Q                                                 Q                               P
Thus
P      (z + tk )Q
                is a positive real         Q modulus isQ |z + tk |. Equation (6) means
                              Q number whose                                             log |z + tk | =
  log tk , hence |z + tk | = tk . Therefore (z + tk ) = tk , i.e. (3) holds.



                                                             30
6) The feasible set P and the function Ψ. Let
           n                                                        o                                       4
                                                                                                            X
       P := (u1 , u2 , u3 , u4 ) ∈ [m, M )4 : u1 + u2 + u3 + u4 = 2π ,             Ψ(u1 , . . . , u4 ) :=         F (uk ).
                                                                                                            k=1

Then P is convex (intersection of a box with an affine hyperplane), hence path-connected, hence connected. Since
F is continuous on [m, M ), Ψ is continuous on P . The continuous image of a connected set in R is an interval, so
Ψ(P ) ⊂ R is an interval. By Lemma 13,
                 λ is a nonreal eigenvalue of some A(α, β, γ, δ)       ⇐⇒        P ̸= ∅ and 0 ∈ Ψ(P ).                       (7)

7) Necessarily 0 ≤ a ≤ 1 (indeed a < 1 if b ̸= 0). Assume b > 0 and P ̸= ∅. Choose (u1 , . . . , u4 ) ∈ P . Then
                                          u1 + u2 + u3 + u4   2π  π
                                                            =    = .
                                                  4            4  2
Since each uk ∈ [m, M ), the interval [m, M ) must contain π/2, i.e.
                                                      π
                                                m ≤ < M.                                                                     (8)
                                                      2
Now m = Arg(λ) = Arg(a + ib) with b > 0. In the open upper half-plane, Arg(a + ib) ≤ π/2 holds iff a ≥ 0.
Thus m ≤ π/2 ⇒ a ≥ 0.
Also M = Arg(λ − 1) = Arg((a − 1) + ib). Since b > 0, the argument is strictly bigger than π/2 iff
Re(λ − 1) = a − 1 < 0, i.e. a < 1. Thus π/2 < M ⇒ a < 1.
Therefore P ̸= ∅ ⇒ 0 ≤ a < 1, proving item (1) (and the sharper a < 1 for b ̸= 0).

8) Strict convexity of F . We show F ′′ (u) > 0 on (0, π). Recall
                               F (u) = log(y csc u) − log(y cot u − x),           y > 0.
Differentiate:
                                    d                 d
                                      log(y csc u) =    log csc u = − cot u.
                                   du                du
Let g(u) = y cot u − x. Then g ′ (u) = −y csc2 u and
                                   d                    g ′ (u)      y csc2 u
                                     log(y cot u − x) =         =−             .
                                  du                    g(u)       y cot u − x
Hence
                                                                   y csc2 u
                                         F ′ (u) = − cot u +                 .
                                                                 y cot u − x
A direct computation (as in the user’s draft) yields
                                                              x2 + y 2
                                          F ′′ (u) =                         .
                                                       (y cot u − x)2 sin2 u
Because y > 0 we have x2 + y 2 > 0, and the denominator is positive for u ∈ (0, π) (since t(u) = y cot u − x > 0).
Thus F ′′ (u) > 0 on (0, π), so F is strictly convex on [m, M ) ⊂ (0, π).

9) Right boundary: necessity of a + b ≤ 1, and attainment of CR. Assume b > 0, P ̸= ∅, and 0 ∈ Ψ(P ).
9.1) Jensen step. For any (u1 , . . . , u4 ) ∈ P , by convexity of F :
                                       4               4
                                     1X             1 X   
                                         F (uk ) ≥ F     uk = F (π/2).
                                     4               4
                                       k=1                   k=1

Thus
                            Ψ(u1 , . . . , u4 ) ≥ 4F (π/2)  for all (u1 , . . . , u4 ) ∈ P.                                  (9)
If 0 ∈ Ψ(P ), then inf P Ψ ≤ 0, but (9) implies inf P Ψ ≥ 4F (π/2), hence F (π/2) ≤ 0.



                                                           31
9.2) Compute F (π/2). Using the explicit F :
                     F (π/2) = log(y csc(π/2)) − log(y cot(π/2) − x) = log(y) − log(−x).
Because y = b and x = a − 1, we have −x = 1 − a, so
                                                                    b 
                                               F (π/2) = log             .
                                                                    1−a
                           b
Thus F (π/2) ≤ 0 ⇐⇒ 1−a       ≤ 1 ⇐⇒ b ≤ 1 − a ⇐⇒ a + b ≤ 1. This proves item (2) for b > 0; for b < 0
apply conjugation to obtain a + |b| ≤ 1.
9.3) Attainment of segment CR. Fix x ∈ (0, 1] and choose α = β = γ = δ = 1−x. Then t1 = t2 = t3 = t4 = x
and (3) becomes
                                               (z + x)4 = x4 .
Hence z + x = xeikπ/2 for k = 0, 1, 2, 3. The nonreal solutions correspond to k = 1, 3: z + x = ±ix, i.e.
λ = 1 − x ± ix. Thus the upper segment λ = 1 − x + ix, x ∈ [0, 1], is attained.

10) Two regimes for supP Ψ: Lemmas 2 and 3 with full details.
Lemma 14 (Unbounded supremum). If 3m + M ≤ 2π, then supP Ψ = +∞.
Proof. Fix u4 ∈ [m, M ) and define u1 = u2 = u3 = (2π − u4 )/3. Then u1 + u2 + u3 + u4 = 2π, so the
only requirement to have (u1 , . . . , u4 ) ∈ P is u1 ∈ [m, M ). If u4 is sufficiently close to M from below, then
u4 ∈ [m, M ) and
                                                    2π − u4    2π − M
                                              u1 =          >           .
                                                       3           3
The hypothesis 3m + M ≤ 2π implies (2π − M )/3 ≥ m, hence u1 ≥ m for all such u4 . Also u1 < M
because u4 > m implies u1 < (2π − m)/3 ≤ (2π − m)/3 < M (since M > π/2 and m > 0). Therefore
(u1 , u2 , u3 , u4 ) ∈ P for u4 close enough to M .
Now as u4 ↑ M , we have t(u4 ) ↓ 0 (because u(t) decreases and u(t) ↑ M corresponds to t ↓ 0), so
                           F (u4 ) = log |z + t(u4 )| − log t(u4 ) → +∞          (t(u4 ) ↓ 0).
Meanwhile u1 = (2π − u4 )/3 converges to (2π − M )/3 ∈ [m, M ), so F (u1 ) stays bounded. Thus Ψ =
3F (u1 ) + F (u4 ) → +∞, proving supP Ψ = +∞.
Lemma 15 (Finite maximum in the tight regime). Assume the tight regime 3m + M > 2π, and define
                                                    U := 2π − 3m.
Then U ∈ [m, M ) (indeed U < M ), and
                                              max Ψ = 3F (m) + F (U ),
                                               P

with equality if and only if (u1 , u2 , u3 , u4 ) is a permutation of (U, m, m, m).
Proof. Step 1: U ∈ [m, M ). Because 3m + M > 2π, we have U = 2π − 3m < M . Also m ≤ π/2 (since a ≥ 0
from Step 7), hence U = 2π − 3m ≥ 2π − 3(π/2) = π/2 ≥ m. Therefore U ∈ [m, M ).
Step 2: reduce to ordered vectors and a compact domain. Define the ordered feasible set
              P ↓ := {(v1 , v2 , v3 , v4 ) ∈ [m, M )4 : v1 ≥ v2 ≥ v3 ≥ v4 , v1 + v2 + v3 + v4 = 2π}.
Because Ψ(u1 , . . . , u4 ) is symmetric in the coordinates, we have
                                                   max Ψ = max Ψ,
                                                    P           P↓

since every point of P can be permuted into P ↓ without changing Ψ.
Next we prove that in the tight regime, every (v1 , . . . , v4 ) ∈ P ↓ actually lies in a closed box [m, U ]4 , so that
maxP ↓ Ψ is attained.
Indeed, for any (v1 , . . . , v4 ) ∈ P ↓ we have v2 , v3 , v4 ≥ m, so
                                    v1 = 2π − (v2 + v3 + v4 ) ≤ 2π − 3m = U.



                                                           32
Since v1 ≥ v2 ≥ v3 ≥ v4 , this implies vk ≤ v1 ≤ U for each k. Thus
                          P ↓ ⊂ [m, U ]4 ∩ {v1 + v2 + v3 + v4 = 2π, v1 ≥ v2 ≥ v3 ≥ v4 }.
Because U < M , the upper endpoint M (open) is avoided: [m, U ] is closed and bounded. Hence P ↓ is a closed
subset of a compact set, so P ↓ is compact. Since Ψ is continuous, Ψ attains its maximum on P ↓ .
Step 3: prove the majorization inequalities explicitly. Let
                                                       x := (U, m, m, m).
We claim that x majorizes every v = (v1 , v2 , v3 , v4 ) ∈ P ↓ , i.e.
                             k
                             X            k
                                          X                                   4
                                                                              X            4
                                                                                           X
                                   vj ≤         xj   (k = 1, 2, 3),                 vj =         xj = 2π.                (10)
                             j=1          j=1                                 j=1          j=1

We verify the partial sums:
       • For k = 1: as shown above, v1 ≤ U = x1 .
       • For k = 2: since v3 , v4 ≥ m,
                      v1 + v2 = 2π − (v3 + v4 ) ≤ 2π − 2m = (2π − 3m) + m = U + m = x1 + x2 .
       • For k = 3: since v4 ≥ m,
                   v1 + v2 + v3 = 2π − v4 ≤ 2π − m = (2π − 3m) + 2m = U + 2m = x1 + x2 + x3 .
       • For k = 4: both sums equal 2π by definition of P ↓ and U :
                                                                                                            4
                                                                                                            X
                             x1 + x2 + x3 + x4 = U + 3m = (2π − 3m) + 3m = 2π =                                   vj .
                                                                                                            j=1

Thus (10) holds, i.e. x majorizes v.
Step 4: apply Karamata P     (with strictness).
                                   P            Karamata’s inequality states: if f is convex on an interval and
x majorizes v, then      f (xi ) ≥    f (vi ). Here F is convex (indeed strictly convex) on [m, M ), hence on
[m, U ] ⊂ [m, M ). Therefore
                                                     4
                                                     X                 4
                                                                       X
                          Ψ(v1 , v2 , v3 , v4 ) =          F (vk ) ≤         F (xk ) = 3F (m) + F (U ).
                                                     k=1               k=1

So maxP ↓ Ψ ≤ 3F (m) + F (U ).
On the other hand, the point (U, m, m, m) itself belongs to P (since U ∈ [m, M ) and U + 3m = 2π), hence to
P ↓ (since U ≥ m). Thus
                                 max Ψ ≥ Ψ(U, m, m, m) = 3F (m) + F (U ).
                                      P↓
So equality holds and
                                           max Ψ = max Ψ = 3F (m) + F (U ).
                                            P              P↓
                                                                                                            P
Finally,
P         because F is strictly convex, the equality case in Karamata implies that if x majorizes v and F (xi ) =
    F (vi ), then v is a permutation of x. (Indeed, strict convexity forces equality only when the majorization is
trivial in the sense that the vectors agree up to permutation.) Hence equality occurs if and only if (u1 , u2 , u3 , u4 ) is
a permutation of (U, m, m, m).

11) Necessity of G(a, b) ≥ 0.
11.1) A geometry/algebra lemma: G ≤ 0 ⇒ tight regime.
Lemma 16. Assume b > 0 and 0 ≤ a ≤ 1. If G(a, b) ≤ 0 then 3m + M > 2π.




                                                                  33
Proof. Throughout, m = Arg(λ) = Arg(a+ib) ∈ (0, π/2] and M = Arg(λ−1) = Arg((a−1)+ib) ∈ (π/2, π).
Step 1: rewrite G as a quadratic in s = b2 . Let s = b2 ≥ 0. Expand:
               G(a, b) = (s + a2 + a)2 + 2a2 − s = s2 + s(2a2 + 2a − 1) + (a2 + a)2 + 2a2 .
Thus G(a, b) ≤ 0 means
                                 s2 + s(2a2 + 2a − 1) + (a2 + a)2 + 2a2 ≤ 0.                               (11)
Compute the discriminant:
                        ∆ = (2a2 + 2a − 1)2 − 4 (a2 + a)2 + 2a2
                                                                  

                          = (4a4 + 8a3 + 4a2 − 4a2 − 4a + 1) − 4(a4 + 2a3 + a2 + 2a2 )
                          = (4a4 + 8a3 − 4a + 1) − (4a4 + 8a3 + 12a2 )
                          = 1 − 4a − 12a2
                          = −(2a + 1)(6a − 1).
So ∆ > 0 iff a < 1/6 (since 2a + 1 > 0).
If a ≥ 1/6 then ∆ ≤ 0 and the quadratic (11) is everywhere > 0 (it is monic), so G(a, b) ≤ 0 is impossible.
Hence, under G(a, b) ≤ 0, we must have
                                                       1
                                               0≤a< .                                                 (12)
                                                       6
Step 2: handle a = 0 separately. If a = 0 then λ = ib with b > 0, so m = π/2. Also λ − 1 = −1 + ib so
M = π − arctan(b). Therefore
                                       3π                   5π
                           3m + M =       + π − arctan(b) =    − arctan(b) > 2π.
                                        2                    2
So the claim holds when a = 0.
Henceforth assume a > 0 (still with a < 1/6 by (12)).
Step 3: show b2 > 3a2 , hence m > π/3, hence 3m > π. Let s = b2 . Since G(a, b) ≤ 0 and the quadratic is
monic, s lies between its real roots. Let s− (a) be the smaller root:
                                                   √                    p
                             −(2a2 + 2a − 1) − ∆          1 − 2a − 2a2 − (2a + 1)(1 − 6a)
                  s− (a) =                              =                                 .
                                          2                              2
Then G(a, b) ≤ 0 implies
                                                  s = b2 ≥ s− (a).                                 (13)
We now prove the strict inequality
                                     s− (a) > 3a2      for all a ∈ (0, 1/6).                               (14)
Indeed, (14) is equivalent to
                            p
          1 − 2a − 2a2 − (2a + 1)(1 − 6a)                                         p
                                                  > 3a2 ⇐⇒ 1 − 2a − 8a2 > (2a + 1)(1 − 6a).
                              2
For a ∈ (0, 1/6), the left side is positive (check at a = 1/6: 1 − 1/3 − 8/36 = 4/9 > 0), so we can square both
sides without changing the inequality:
                                     (1 − 2a − 8a2 )2 > (2a + 1)(1 − 6a).
Expand the left side:
                               (1 − 2a − 8a2 )2 = 1 − 4a − 12a2 + 32a3 + 64a4 .
Expand the right side:
                                      (2a + 1)(1 − 6a) = 1 − 4a − 12a2 .
Thus the inequality becomes
                 1 − 4a − 12a2 + 32a3 + 64a4 > 1 − 4a − 12a2          ⇐⇒       32a3 + 64a4 > 0,
which holds strictly for all a > 0. This proves (14). Combining with (13) gives
                                                                     b    √
                                     b2 = s ≥ s− (a) > 3a2 =⇒          > 3.
                                                                     a


                                                       34
Since m = Arg(a + ib) = arctan(b/a) for a > 0, we get
                                                       √    π
                                            m > arctan( 3) = .
                                                            3
Therefore 3m > π. In particular 3m ∈ (π, 3π/2) because m < π/2.
Step 4: rewrite 3m + M > 2π as a tangent inequality. Because a < 1 and b > 0, the point λ − 1 = (a − 1) + ib
lies in quadrant II, so
                                                                  b 
                                   M = Arg(λ − 1) = π − arctan            .
                                                                   1−a
Thus
                                                                   b 
                             3m + M > 2π ⇐⇒ 3m + π − arctan                  > 2π
                                                                   1−a
                                                                   b 
                                             ⇐⇒ 3m > π + arctan             .                             (15)
                                                                   1−a
                      b
                        
Set θ := arctan 1−a       ∈ (0, π/2) (since b > 0 and a < 1). Then π + θ ∈ (π, 3π/2). We already know
3m ∈ (π, 3π/2) from Step 3. On (π, 3π/2) the tangent function is continuous and strictly increasing. Therefore
(15) is equivalent to
                                                                       b
                                   tan(3m) > tan(π + θ) = tan θ =         .                               (16)
                                                                    1−a
Step 5: express tan(3m) and reduce (16) to N (a, b) > 0. Since tan m = b/a (with a > 0), the triple-angle
identity gives
                                 3 tan m − tan3 m     3(b/a) − (b/a)3    3a2 b − b3
                      tan(3m) =              2     =               2
                                                                      =              .
                                    1 − 3 tan m         1 − 3(b/a)      a(a2 − 3b2 )
Equivalently (multiplying numerator and denominator by −1),
                                                        b(b2 − 3a2 )
                                           tan(3m) =                 .                                   (17)
                                                        a(3b2 − a2 )
By Step 3, b2 > 3a2 so all factors in (17) are positive, and tan(3m) > 0.
Plug (17) into (16) and cancel b > 0:
                                                b2 − 3a2         1
                                                             >      .
                                               a(3b2 − a2 )    1−a
All denominators are positive (since a ∈ (0, 1) and 3b2 − a2 > 0), so we can cross-multiply:
                                          (1 − a)(b2 − 3a2 ) > a(3b2 − a2 )
                                      b2 − ab2 − 3a2 + 3a3 > 3ab2 − a3
                                    b2 − 4ab2 + 4a3 − 3a2 > 0.
Define
                        N (a, b) := 4a3 − 3a2 − 4ab2 + b2 = (1 − 4a)b2 + (4a3 − 3a2 ).                   (18)
Then (16) is equivalent to
                                                 N (a, b) > 0.                                           (19)
                                                                            2
Step 6: show G(a, b) ≤ 0 ⇒ N (a, b) > 0 by comparing roots in s = b . Fix a ∈ (0, 1/6) and view N as an
affine function of s = b2 :
                                        N (a, b) = (1 − 4a)s + (4a3 − 3a2 ).
Because a < 1/6 < 1/4, we have 1 − 4a > 0, so N is strictly increasing in s. Therefore, under the constraint
s ≥ s− (a) from (13), it suffices to prove
                                                   s− (a) > s0 (a),                                     (20)
where s0 (a) is the unique root of N in s:
                                                                                  a2 (3 − 4a)
                 N (a, b) = 0 ⇐⇒ (1 − 4a)s = 3a2 − 4a3 ⇐⇒ s = s0 (a) :=                       .          (21)
                                                                                    1 − 4a



                                                       35
Indeed, if (20) holds then s ≥ s− (a) implies s > s0 (a),√and since N increases in s this implies N (a, b) > 0.
                                                   1−2a−2a2 −    (2a+1)(1−6a)
We now prove (20). Starting from s− (a) =                       2             , we compute:
                                                          p
                                      1 − 2a − 2a2 −                a2 (3 − 4a)
                                                              (2a + 1)(1 − 6a)
              s− (a) > s0 (a) ⇐⇒                                                 >
                                                  2                   1 − 4a
                                                        p
                               ⇐⇒ (1 − 4a) 1 − 2a − 2a − (2a + 1)(1 − 6a) > 2a2 (3 − 4a).
                                                      2
                                                                          

Expand (1 − 4a)(1 − 2a − 2a2 ):
                                   (1 − 4a)(1 − 2a − 2a2 ) = 1 − 6a + 6a2 + 8a3 .
So the inequality becomes
                                                      p
                         1 − 6a + 6a2 + 8a3 − (1 − 4a) (2a + 1)(1 − 6a) > 6a2 − 8a3 ,
i.e.                                                                 p
                                 1 − 6a + 16a3 > (1 − 4a)             (2a + 1)(1 − 6a).
For a ∈ (0, 1/6) both sides are positive, so we may square:
                                   (1 − 6a + 16a3 )2 > (1 − 4a)2 (2a + 1)(1 − 6a).                                (22)
                                                   2
Compute (2a + 1)(1 − 6a) = 1 − 4a − 12a . Then the right side is
                           (1 − 4a)2 (1 − 4a − 12a2 ) = (1 − 8a + 16a2 )(1 − 4a − 12a2 ).
Expand:
                        (1 − 8a + 16a2 )(1 − 4a − 12a2 ) = 1 − 12a + 36a2 + 32a3 − 192a4 .
Expand the left side:
                          (1 − 6a + 16a3 )2 = 1 − 12a + 36a2 + 32a3 − 192a4 + 256a6 .
Thus the left side equals the right side plus 256a6 , so (22) holds strictly for a > 0. Hence s− (a) > s0 (a), and
therefore N (a, b) > 0.
Step 7: conclude 3m + M > 2π. We have proved G(a, b) ≤ 0 ⇒ N (a, b) > 0 ⇒ (16) holds, which implies (15),
which is equivalent to 3m + M > 2π.

11.2) Tight regime: compute maxP Ψ explicitly and factor to G. Assume b > 0, 0 ≤ a < 1, and we are in the
tight regime 3m + M > 2π. Then by Lemma 15,
                                   max Ψ = 3F (m) + F (U ),              U = 2π − 3m.
                                     P

Step 1: compute F (m) exactly. By definition m = Arg(z + 1), so the associated t is t = 1. Equivalently, using
t(u) = y cot u − x and (x, y) = (a − 1, b):
                                            t(m) = b cot m − (a − 1) = 1.
Then
                                         F (m) = log |z + 1| − log 1 = log |λ|.
Step 2: compute F (U ) exactly. By definition,
            F (U ) = log(b csc U ) − log(b cot U − (a − 1)) = log(b csc U ) − log(b cot U + 1 − a).

Step 3: obtain the announced closed form. Combine:
                              max Ψ = 3 log |λ| + log(b csc U ) − log(b cot U + 1 − a)
                               P
                                                    |λ|3 b csc U 
                                      = log                         .                                             (23)
                                                  b cot U + 1 − a
This is the detailed derivation of the formula announced as (11.25) in the draft.



                                                                36
Step 4: rewrite csc U and cot U algebraically in terms of (a, b). We use U = 2π − 3m. Because U ∈ (0, π) in
the tight regime (indeed U < M < π), we have sin U > 0.
We have the trigonometric identities
                                  sin(2π − θ) = − sin θ,         cos(2π − θ) = cos θ,
hence
                                          cos U    cos(3m)                                        1
   sin U = − sin(3m),           cot U =         =           = − cot(3m),              csc U =         = − csc(3m).
                                          sin U   − sin(3m)                                     sin U
Now express sin m and cos m using λ = a + ib:
                                p                                  a                   b
                           |λ| = a2 + b2 ,              cos m =       ,     sin m =       .
                                                                  |λ|                 |λ|
Use triple-angle formulas:
                      sin(3m) = 3 sin m − 4 sin3 m,             cos(3m) = 4 cos3 m − 3 cos m.
Compute:
                          b      b 3    3b|λ|2 − 4b3   b(3(a2 + b2 ) − 4b2 )    b(3a2 − b2 )
             sin(3m) = 3     −4         =         3
                                                       =           3
                                                                               =               ,
                         |λ|     |λ|          |λ|               |λ|                   |λ|3
                         a 3       a    4a3 − 3a|λ|2   a(4a2 − 3(a2 + b2 ))      a(a2 − 3b2 )
             cos(3m) = 4        −3      =         3
                                                       =             3
                                                                                =                .
                           |λ|      |λ|       |λ|                |λ|                   |λ|3
Therefore
                                  1          |λ|3                           cos(3m)    a(a2 − 3b2 )
               csc U = −              =−              ,         cot U = −           =−              .            (24)
                              sin(3m)    b(3a2 − b2 )                       sin(3m)    b(3a2 − b2 )
Step 5: substitute into (23) and reduce to an algebraic inequality. First compute b csc U using (24):
                                                          |λ|3        |λ|3
                                          b csc U = −            =          .
                                                        3a2 − b2   b2 − 3a2
Next compute the denominator b cot U + 1 − a:
                                                            a(a2 − 3b2 )
                                     b cot U + 1 − a = −                 + 1 − a.
                                                             3a2 − b2
Put over the common denominator (3a2 − b2 ):
                                                −a(a2 − 3b2 ) (1 − a)(3a2 − b2 )
                              b cot U + 1 − a =              +
                                                  3a2 − b2          3a2 − b2
                                                −(a − 3ab ) + 3a − b2 − 3a3 + ab2
                                                   3       2     2
                                              =
                                                             3a2 − b2
                                                −4a3 + 3a2 + 4ab2 − b2
                                              =                        .
                                                       3a2 − b2
Define N (a, b) as in (18):
                                      N (a, b) = 4a3 − 3a2 − 4ab2 + b2 .
Then the last numerator is exactly −N (a, b), so
                                                          −N (a, b)   N (a, b)
                                      b cot U + 1 − a =     2     2
                                                                    = 2        .
                                                          3a − b     b − 3a2
Consequently, the positive quantity inside the logarithm in (23) is
                                                            3     |λ|3
                                        |λ|3 b csc U   |λ| · b2 −3a2    |λ|6
                                                     =    N (a,b)
                                                                     =          .                                (25)
                                     b cot U + 1 − a       2    2
                                                                       N (a, b)
                                                             b −3a




                                                           37
Thus                                                      |λ|6 
                                                 max Ψ = log         .                                       (26)
                                             P              N (a, b)
Since the left side is defined, the argument of the logarithm is positive; equivalently N (a, b) > 0 in the tight
regime.
From (26), we have
                                                  |λ|6
                          max Ψ ≥ 0 ⇐⇒                   ≥ 1 ⇐⇒ |λ|6 ≥ N (a, b).
                            P                   N (a, b)
Step 6: factor |λ|6 − N (a, b) as |λ − 1|2 G(a, b). Let r := |λ|2 = a2 + b2 . Then |λ|6 = r3 . Also |λ − 1|2 =
(a − 1)2 + b2 = r + 1 − 2a. Rewrite G in terms of r:
          G(a, b) = (b2 + a2 + a)2 + 2a2 − b2 = (r + a)2 + 2a2 − (r − a2 ) = r2 + (2a − 1)r + 4a2 .
Now multiply:
            |λ − 1|2 G(a, b) = (r + 1 − 2a) r2 + (2a − 1)r + 4a2
                                                                           

                                = r3 + (4a − 1)r + 4a2 − 8a3             (direct expansion; the r2 terms cancel)
                                = r3 − 4a3 − 3a2 − 4ab2 + b      2
                                                                   

                                = |λ|6 − N (a, b).
Therefore
                               |λ|6 ≥ N (a, b) ⇐⇒ |λ − 1|2 G(a, b) ≥ 0.                                            (27)
Because b > 0 implies |λ − 1|2 > 0, (27) is equivalent to
                                                       G(a, b) ≥ 0.
Combining with the previous equivalences yields the precise statement announced in the draft:
                                            max Ψ ≥ 0     ⇐⇒           G(a, b) ≥ 0.
                                             P


11.3) Finish necessity of G(a, b) ≥ 0. Assume λ is a nonreal eigenvalue of some A(α, β, γ, δ). By (7), we have
0 ∈ Ψ(P ), hence supP Ψ ≥ 0.
If 3m + M ≤ 2π, then Lemma 16 by contrapositive implies G(a, b) > 0.
If 3m + M > 2π, then we are in the tight regime and by the computation in §11.2, supP Ψ = maxP Ψ ≥ 0 ⇐⇒
G(a, b) ≥ 0. Thus always G(a, b) ≥ 0.
Finally, by conjugation symmetry, replace b by |b| to obtain item (3) for all b ̸= 0.

12) Left boundary CL: attainment by AL (α) and equivalence to G = 0.
12.1) Characteristic equation for AL (α). Let
                                                α 1−α 0 0
                                                              
                                               0   0    1 0
                                      AL (α) =                  .
                                                 0  0    0 1
                                                 1  0    0 0
Let v ̸= 0 satisfy AL v = λv. Row-by-row:
                             αv1 + (1 − α)v2 = λv1 ,     v3 = λv2 ,       v4 = λv3 ,    v1 = λv4 .
From the last three equalities,
                                          v3 = λv2 ,   v4 = λ2 v2 ,      v1 = λ3 v2 .
Substitute into the first:
                             α(λ3 v2 ) + (1 − α)v2 = λ(λ3 v2 )    ⇐⇒           αλ3 + (1 − α) = λ4 .
Equivalently,
                                             λ3 (λ − α) = 1 − α.                                                   (28)
For λ ∈
      / R this is equivalent to λ ∈ σ(AL (α)).



                                                            38
Solving (28) for α (and using λ3 ̸= 1 for nonreal λ) gives
                                                              λ4 − 1
                                                       α=            .                                    (29)
                                                              λ3 − 1
12.2) Compute ℑ(α) and show ℑ(α) = 0 ⇐⇒ G(a, b) = 0. Let p = λ4 − 1 and q = λ3 − 1. Then α = p/q.
For any complex numbers p, q with q ̸= 0,
                                          p    pq  ℑ(pq)
                                        ℑ     =ℑ      =      .
                                           q     |q|2   |q|2
Thus
                                                             3    
                                                ℑ (λ4 − 1)(λ − 1)
                                         ℑ(α) =                     .                                     (30)
                                                     |λ3 − 1|2
Expand the numerator:
                                               3                    3             3
                                     (λ4 − 1)(λ − 1) = λ4 λ − λ4 − λ + 1.
Take imaginary parts:
                                                       3                    3
                                           ℑ(λ4 λ ) − ℑ(λ4 ) − ℑ(λ ).
         3
Now λ4 λ = λ(λλ)3 = λ|λ|6 , hence
                                                   3
                                          ℑ(λ4 λ ) = ℑ(λ)|λ|6 = b|λ|6 .
         3
Also ℑ(λ ) = −ℑ(λ3 ), so the numerator of (30) equals
                                             b|λ|6 − ℑ(λ4 ) + ℑ(λ3 ).                                     (31)
              3          4
Compute ℑ(λ ) and ℑ(λ ) for λ = a + ib:
                        λ3 = (a3 − 3ab2 ) + i(3a2 b − b3 )           ⇒     ℑ(λ3 ) = b(3a2 − b2 ),
and
                   λ4 = (a4 − 6a2 b2 + b4 ) + i(4a3 b − 4ab3 ) ⇒ ℑ(λ4 ) = 4ab(a2 − b2 ).
Substitute into (31):
                                       3
                         ℑ (λ4 − 1)(λ − 1) = b|λ|6 − 4ab(a2 − b2 ) + b(3a2 − b2 )
                                              
                                                                                   
                                                = b |λ|6 − (4a3 − 3a2 − 4ab2 + b2 )
                                                = b |λ|6 − N (a, b) .
                                                                   

By the factorization proved in §11.2,
                                        |λ|6 − N (a, b) = |λ − 1|2 G(a, b).
Therefore
                                                           b |λ − 1|2 G(a, b)
                                           ℑ(α) =                             .                           (32)
                                                                |λ3 − 1|2
Since b > 0 and both |λ − 1|2 and |λ3 − 1|2 are strictly positive for nonreal λ, we conclude
                                        ℑ(α) = 0            ⇐⇒      G(a, b) = 0.
Thus the upper-half-plane boundary curve G(a, b) = 0 is exactly traced by the nonreal eigenvalues of AL (α).
12.3) Existence of a conjugate pair and endpoints i and 0. From (28) we have the characteristic polynomial
                                            λ4 − αλ3 − (1 − α) = 0.
One checks λ = 1 is always a root:
                                              1 − α − (1 − α) = 0.
Indeed the polynomial factors as
                                                                  
                                   (λ − 1) λ3 + (1 − α)(λ2 + λ + 1) = 0.                                  (33)



                                                              39
Let
                                fα (λ) := λ3 + (1 − α)(λ2 + λ + 1),           λ ∈ R.
Then
                                        fα′ (λ) = 3λ2 + 2(1 − α)λ + (1 − α).
The discriminant of this quadratic is
                 ∆α = 4(1 − α)2 − 12(1 − α) = 4(1 − α) (1 − α) − 3 < 0
                                                                  
                                                                                       (α ∈ [0, 1)),
so fα′ (λ) > 0 for all real λ. Hence fα is strictly increasing and has exactly one real root. Therefore the remaining
two roots of fα are nonreal and form a complex conjugate pair. One of them lies in the upper half-plane.
At α = 0, (28) becomes λ4 = 1, whose upper-half-plane nonreal root is λ = i. As α ↑ 1, the coefficients
in (33) vary continuously, so the roots vary continuously; and from fα (0) = (1 − α) > 0 and fα (−1) =
−1 + (1 − α)(1 − 1 + 1) = −α < 0, the unique real root of fα lies in (−1, 0), while the conjugate pair has
modulus tending to 0 as α ↑ 1. Thus the upper branch connects i (at α = 0) to 0 (as α → 1− ), as stated.

13) Every strict interior point is attained (constructive existence). Fix λ = a + ib with
                            b > 0,        0 ≤ a ≤ 1,      a + b < 1,       G(a, b) > 0.
We must construct α, β, γ, δ ∈ [0, 1) with λ ∈ σ(A(α, β, γ, δ)).
Step 1: P ̸= ∅ and exhibit a point with Ψ < 0. Because 0 ≤ a < 1 and b > 0, we have m ≤ π/2 < M as in
Step 7, hence π/2 ∈ [m, M ). Define                π π π π
                                           u(0) :=     , , ,      ∈ P.
                                                     2 2 2 2
Then                                                               b 
                                      Ψ(u(0) ) = 4F (π/2) = 4 log          .
                                                                    1−a
                                               b                  b
                                                                     
Since a + b < 1, we have b < 1 − a, hence 1−a     < 1, hence log 1−a   < 0. Thus

                                                   Ψ(u(0) ) < 0.                                                (34)

Step 2: produce a point with Ψ > 0 using G(a, b) > 0. We show
                                         ∃ u(1) ∈ P such that Ψ(u(1) ) > 0.                                     (35)
There are two cases:
Case 1: 3m + M ≤ 2π. Then Lemma 14 gives supP Ψ = +∞, so in particular there exists u(1) ∈ P with
Ψ(u(1) ) > 0.
Case 2: 3m + M > 2π (tight regime). Then Lemma 15 gives
                                                 sup Ψ = max Ψ,
                                                   P          P

and §11.2 gives maxP Ψ ≥ 0 ⇐⇒ G(a, b) ≥ 0. Since we assume G(a, b) > 0, we get maxP Ψ > 0, so there
exists u(1) ∈ P with Ψ(u(1) ) > 0. For example, take u(1) = (U, m, m, m) (in any order), which achieves the
maximum.
Thus (35) holds in all cases.
Step 3: apply IVT along a line segment in P (fully explicit). Because P is convex, for t ∈ [0, 1] the convex
combination
                                             u(t) := (1 − t)u(0) + t u(1)
lies in P . Define the scalar function
                                     ϕ(t) := Ψ(u(t)) = Ψ (1 − t)u(0) + t u(1) .
                                                                             

Because Ψ is continuous on P and u(t) is continuous in t, the composition ϕ is continuous on [0, 1]. We have
ϕ(0) = Ψ(u(0) ) < 0 by (34), and ϕ(1) = Ψ(u(1) ) > 0 by (35). By the Intermediate Value Theorem, there exists
t∗ ∈ (0, 1) such that ϕ(t∗ ) = 0. Set
                                         (u1 , u2 , u3 , u4 ) := u(t∗ ) ∈ P,
so
                              u1 + u2 + u3 + u4 = 2π,            Ψ(u1 , u2 , u3 , u4 ) = 0.



                                                         40
By Lemma 13, the corresponding tk = t(uk ) ∈ (0, 1] satisfy (3), hence λ is an eigenvalue of the original matrix
for parameters
                             α = 1 − t1 , β = 1 − t2 , γ = 1 − t3 , δ = 1 − t4 .
Because each tk ∈ (0, 1], each parameter lies in [0, 1). This constructs α, β, γ, δ with λ ∈ σ(A(α, β, γ, δ)),
proving the converse for strict interior points.

Combining Steps 7, 9, and 11 yields the necessary conditions 0 ≤ a ≤ 1, a + |b| ≤ 1, and G(a, |b|) ≥ 0 for all
nonreal eigenvalues. The explicit families in Steps 9.3 and 12 attain the boundary segments CR and CL. Finally
Step 13 proves every strict interior point is attained.




                                                      41
