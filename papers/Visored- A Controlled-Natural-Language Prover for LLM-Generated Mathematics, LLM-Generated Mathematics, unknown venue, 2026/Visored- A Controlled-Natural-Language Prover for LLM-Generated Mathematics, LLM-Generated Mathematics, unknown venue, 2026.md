                                                     Visored: A Controlled-Natural-Language Prover for
                                                               LLM-Generated Mathematics
                                                                          Xiyu Zhai∗ Xinyi Chen∗ Yiping Wang∗
                                                                         Runlong Zhou∗ Liao Zhang† Simon S. Du∗


                                                                                            Abstract
arXiv:2606.17581v1 [cs.PL] 16 Jun 2026




                                                    We present a dependent-type-based prover designed around the way LLMs (and humans) tend
                                                to write mathematics, complementing existing systems such as Lean and Rocq. Its core design
                                                choices are a surface that imitates mathematical natural language and a rule-driven automation
                                                layer that closes the routine steps a textbook would omit, so that an accepted proof can be re-
                                                emitted as a checked Lean file. Early experiments suggest that, even without any prover-specific
                                                training data, LLMs can learn to use it effectively on the miniF2F benchmark. Lean output
                                                excerpts: https://github.com/xiyuzhai-husky-lang/visored/


                                         1      Introduction
                                         Large language models (LLMs) have become increasingly capable mathematical reasoners, both on
                                         standard benchmarks and, more recently, at the level of competition and research-level mathematics.
                                         They nevertheless still suffer from hallucination [17, 15], so an AI-produced proof is only as trustwor-
                                         thy as the process that checks it, and the most striking recent results still relied on substantial human
                                         verification before they could be reported. As more mathematics is produced with AI assistance, the
                                         binding constraint shifts from generating ideas to verifying and organizing them at scale. Autofor-
                                         malization, the task of mapping informal mathematical writing into machine-checkable form, is one
                                         concrete instance of that bottleneck: if AI-generated proofs are to be absorbed by the mathematical
                                         community rather than accumulating as unverified candidates, the route from informal prose to a
                                         kernel-checked proof has to become much more reliable than it currently is. This paper presents one
                                         attempt in that direction.
                                             One line of work removes the human from the loop with a small, auditable kernel that returns
                                         a definite yes/no on a candidate proof, independent of the model that produced it (the de Bruijn
                                         criterion [31, 30]). Whole-proof theorem provers now drive miniF2F [50] pass rates close to saturation
                                         (Appendix A), but they take an already formalized statement as input. Turning informal prose into
                                         that statement and its proof, the autoformalization step itself, lags well behind [44] and is where most
                                         of the non-local surface-to-semantics decisions are made.
                                             The separation is not just a user-experience (UX) issue. Informal and formal mathematics are not
                                         identical artifacts: informal prose leans on shared background, controlled abuse of notation, implicit
                                         side conditions (“for x suﬀiciently large”, “WLOG x ̸= 0”), and implicit number-system and coercion
                                         choices (N vs. Z vs. R) that readers fill in automatically. A direct translation must therefore commit
                                         to many decisions with no surface trace in the prose: the right library lemma, subtype, edge-case
                                         convention (how a library defines 1/0 or 00 ), tactic, and integer/rational cast. Each is non-local, and
                                         getting one wrong rarely surfaces as a compiler error (those are quick to fix) but as a silent semantic
                                         drift: a statement that compiles yet no longer says what the prose claimed, or a goal that looks
                                         plausible but is unprovable for a reason several rewriting steps upstream.
                                             Our project Visored is a research prototype aimed at making autoformalization as easy and reliable
                                         as possible. Figure 1 states the design thesis. Visored is a semantically rich intermediate representation
                                         (IR) in which every decision that has no surface trace in the LaTeX, namely subtype, library lemma,
                                         edge-case convention, and cast, is made explicit. The downward maps Visored → LaTeX (keep the
                                             ∗ University of Washington. Correspondence to Xiyu Zhai: xiyuzhai@cs.washington.edu
                                             † University of Innsbruck




                                                                                                 1
                                                Visored




                                       ng
                                      rsi
                                   pa
                                 tic
                               an
                               m
                            se
                                            autoformalization

                       LaTeX                                              Lean


Figure 1: The Visored triangle. Visored carries the full syntactic, semantic, and logical content
of a proof; the maps Visored → LaTeX and Visored → Lean are straightforward projections. The
task we want to solve, the dashed LaTeX → Lean edge, is autoformalization. The proposed route
is the composition of the upward semantic parsing arrow (inverting the LaTeX projection) with the
deterministic Visored → Lean projection.


surface, drop the typing) and Visored → Lean (emit each construct as the corresponding Lean term)
are straightforward projections, so the hard part of autoformalization is the upward semantic parsing
arrow from LaTeX into Visored. That ascent is an ill-posed inverse problem: the projection to LaTeX
is lossy, many Visored expressions share the same surface, and choosing among them requires a prior
over what mathematicians (and LLMs) tend to mean. Supplying that prior is the role of the LLM
in the loop; Visored handles everything mechanical below the lift and surfaces failures as localized
diagnostics rather than a single accept/reject at the end of a Lean compilation.
    Two observations shape the design:

1. LLM math data is overwhelmingly informal. Most modern mathematics has not been
formalized: Mathlib, the Coq stdlib, and Isabelle developments together cover only a small fraction
of the field. Frontier LLMs accordingly see far more informal mathematics in training (textbooks,
papers, lecture notes) than formal. A natural-language surface stays close to the side the model is
already fluent on.

2. Bridging natural and formal reasoning is more tractable than full automated theorem
proving. Traditional automated theorem proving (ATP), namely SAT/SMT solvers and resolution
provers, targets fully automated proof discovery, which is NP-hard or undecidable. Visored targets a
different problem: with the LLM supplying the proof outline in controlled natural language (CNL),
the solver only has to close the small obvious steps that mathematicians routinely omit, a much more
tractable task that is well within reach of modern agentic engineering, as demonstrated by coding
agents such as Cursor [2], Claude Code [1], and OpenAI Codex [27].
    Concretely, Visored takes as input a controlled subset of mathematical English embedded
in LaTeX (Appendix B). The accepted subset, both the sentence templates (“Let …”, “Assume …”,
“Then …”) and the LaTeX commands they wrap, is defined by external spec files rather than hard-
coded into the parser, so widening or specializing the language is a matter of editing configuration.
The input is elaborated into a dependently-typed IR (Appendix C), and each “Then …” obligation is
decided by a cost-bounded rule-driven solver (Appendix E). Following PVS, the elaborator
                                                                                    √           enforces
well-definedness at typecheck time: 1/x is accepted only when x ̸= 0 is derivable, x requires x ≥ 0,
and log x requires x > 0. Accepted proofs can optionally be re-expressed as Lean 4 for kernel-level re-
verification, but Visored does not route its own verdict through Lean. Section 5 lays out the resulting
usage modes: inference-time verifier, autoformalizer loop, dense reward signal, and data generator.
    Two challenges sit underneath this design. On the ATP side, Visored needs a solver strong enough
to reliably close the small obvious steps that mathematicians omit across arithmetic, algebra, ordering,
set theory, and named-lemma applications; without it the workflow stalls in retry loops on steps a
human reader would skim past. On the ITP side, producing the dependent-type-checked proofs that


                                                   2
interactive theorem provers (ITP) such as Lean and Rocq require is hard, since type systems, coercions,
library naming, and partial-function side conditions must all be resolved before the kernel accepts the
proof; a recent Claude-Code case study found Lean proof emission to be “the most challenging aspect”
of building an SMT solver from scratch [16], and Naproche has listed ForTheL → Lean as a direction
since 2020 without yet making it a production path [8].
    Visored today is an early prototype around the miniF2F dataset, covering middle-school-level set
theory, algebra, and inequalities; we discuss the limits openly in Section 7. It draws together several
earlier schools of prover design, reviewed in Appendix A. What is genuinely new lives in the integration
details, namely implicit hypothesis arguments per user expression discharged by the solver, a spec-
driven extensible LaTeX surface, a localized per-stage diagnostic channel, and the data structures
connecting these into one pipeline, rather than in any individual layer. What we test is whether the
combination amounts to more than the sum of its parts when the user is an LLM.


2    Related Work
Visored draws together several earlier schools of prover design. It shares the controlled-natural-
language surface of Mizar and Naproche [38, 24], the typecheck-time well-definedness of PVS [28, 33],
the dependently-typed substrate of Lean and Rocq, and the cost-budgeted rule-driven solving of
ProofGrader [47], and it adopts the LLM-centric framing of the recent autoformalization litera-
ture [46, 18, 48]. We do not claim any individual ingredient is novel; what is new is their integration
into a single LLM-facing pipeline whose checkable intermediate representation makes failures localized
rather than a single accept/reject after a Lean compilation. Appendix A gives the full discussion: the
broader progress of AI for mathematics that motivates the autoformalization bottleneck, and a de-
tailed comparison with each prior school, namely direct LLM autoformalization and whole-proof Lean
models, CNL provers, natural-language tactic layers, rule-based proof checkers, and typecheck-time
well-definedness.


3    Architecture
Visored is itself a prover. Given a LaTeX document (proof content lives inside example environments)
plus a small set of config and spec files, it returns its own verdict — accepted, or a structured diagnostic
pointing at the specific source location where elaboration or the solver failed. The Lean emitter is
an optional downstream stage that re-expresses an accepted proof as a Lean file for users who need
external verification or interoperability with the Lean ecosystem; Visored’s correctness does not pass
through Lean.
   The pipeline (Figure 2) is a sequence of stages where each stage either lowers the previous stage’s
output into a more constrained form or refuses with a diagnostic. We describe each stage by what
data it produces and what an LLM gains from being able to inspect that data.

LaTeX source. The input is LaTeX. Visored accepts a controlled subset of mathematical English
written inside LaTeX — not arbitrary prose — but the subset is defined by an external, easily editable
spec rather than baked into the parser. The set of recognized sentence templates, LaTeX commands,
and LaTeX environments lives in .lpcsv configuration files, so extending the surface language is a
matter of adding entries (Appendix B), not modifying compiler code. In practice the vocabulary
covers what an LLM is likely to emit when asked to write a proof in LaTeX, but inputs outside that
vocabulary are rejected with a localized diagnostic, not silently coerced.

Syntax tree. The Syntax stage uses two parsing strategies depending on which mode the source is
in. Math mode (the contents of $...$ and \[...\]) is parsed with a precedence-aware stack-based
parser similar to a C expression parser: incomplete sub-expressions are pushed onto a stack with their
precedences, and the stack is reduced when a closing delimiter or lower-precedence operator arrives.
Text mode (CNL prose between math — “Let …”, “Assume …”, “Then …”) is parsed by trie-like
matching of the word/punctuation token stream against the sentence templates declared in spec files
(.lpcsv): shared-prefix templates are resolved by descending through the alternatives until exactly
one continues to match. Both strategies map each LaTeX command (\sin, \frac, \sum, \mathbb, …)


                                                     3
                                   LaTeX source (CNL inside example)

                                                        parse


                                              Syntax tree

                                                        types, kinds


                                           Typed AST (sem)

                                                        lower


                                              Visored MIR



                                      Elaboration + well-definedness

                                                        discharge “Then…”

                    localized
                                          Cost-bounded solver
                   diagnostic


                                                                       transcribe
                                         accept (Visored verdict)                   UVL MIR


                                                                                    Lean file
                                                                                    lake build



Figure 2: The Visored pipeline. Each stage lowers the previous stage’s output into a more constrained
form or refuses with a localized diagnostic that points at the offending source span (dashed; any stage
can refuse, not only the two drawn). Visored’s verdict, accept or diagnostic, is produced by the solver
and does not pass through Lean. Once a proof is accepted, the dotted branch optionally transcribes
it, together with the recorded derivation steps, to UVL MIR and then to a Lean file for external kernel
re-checking.


and each LaTeX environment (example, itemize, …) onto a typed syntactic node. The resulting tree
is untyped in the type-theoretic sense — it records what was written, not yet what it means. A LaTeX
command the spec does not declare (the user writes \foobar) is rejected at this stage with a structured
UnknownCommand error pointing at the offending token, which an LLM can patch by rephrasing or by
adding the command to the spec.

Typed syntax tree (sem AST). Names get resolved against the current scope (local definitions
first, then global symbols loaded from .lpcsv spec files), and each subexpression is assigned a type
and a kind. The kind layer is small and dependent-flavored — enough for analysis, set theory, basic
algebra, and number theory — and forms the substrate for the typed pattern matching used by later
stages.

MIR (mid-level IR). The sem AST (a typed abstract syntax tree) is lowered to Visored MIR,
the substrate the solver and elaborator operate on. A separate stage further translates MIR plus the
recorded derivation steps to UVL MIR, a target-neutral IR from which a Lean formatter emits proof
text. The split means improvements to the solver do not change emission, and adding a new prover
target is a new UVL formatter rather than a rewrite of elaboration.

Elaboration and solver. Each statement (“Let …”, “Assume …”, “Then …”) updates a prover state
of variables, hypotheses, and derivations. “Then …” clauses are the gaps the solver must discharge.


                                                    4
                                                                          √
Elaboration also enforces well-definedness: writing 1/x demands x ̸= 0, x demands x ≥ 0, log x
demands x > 0, with the demands flowing asymmetrically through boolean connectives so that a
guard like x ̸= 0 ∧ 1/x > 0 is accepted. These demands are routed to the same cost-bounded rule-
driven solver that closes “Then …” gaps; a statement whose obligations cannot be closed is rejected
with a localized diagnostic. The rule format, the runtime, the well-definedness mechanism, and the
asymmetric-context details all live in Appendix E.

Lean emission (optional). For users who want external verification or to feed downstream Lean
tooling, an accepted proof can be re-expressed as a Lean file. The formatter itself does no proof
search, but the emitted Lean code calls Lean-side tactics — obvious, simp, assumption, custom
rewrite tactics — on small per-step obligations, which lake build then closes. This stage is not
required for Visored to accept or reject a proof.

What an LLM sees. From the LLM’s perspective, Visored is a function LaTeX proof → {accepted,
or a diagnostic pointing at a specific source location}, with Lean output available as a side product
when wanted. Intermediate states are exposed as human-readable trace output rather than as a generic
serialized format, so an LLM can use Visored both as an end-to-end checker and as a generator of
training data; an obvious next step is to wire the diagnostic channel directly as an RL reward signal.


4     Worked Example
To make the value proposition concrete, the three examples below show the same kind of object
written two ways: a Visored CNL input (left column) and the kind of Lean source an existing LLM
autoformalization pipeline would have to produce directly (right column). The CNL stays close to
what an LLM is already fluent at producing; the Lean additionally requires the LLM to pick the right
Mathlib lemmas and tactics, which is the part of the pipeline where current direct-autoformalization
systems report the largest pass-rate gap. All three pairs are checked automatically by the artifact
Makefile: the CNL passes Visored and the Lean compiles against Mathlib.

Visored CNL input (typeset)                        Hand-written Lean 4 proof

Example 1. Let k ∈ R.
Let x ∈ R.                                         import Mathlib
                 √
Assume x = 13−4 131 .
Assume 2x2 − 13x + k = 0.                          namespace VisoredPaperExamples.Ex01
The goal is to prove k = 19
                          4 .                      example (k x : ℝ)
Then k = 13x − 2x2 .                                  (hx : x = (13 - Real.sqrt 131) / 4)
Then k = 194 .                                        (heq : 2 * x^2 - 13 * x + k = 0) :
                                                      k = 19 / 4 := by
                                                    have hsq : Real.sqrt 131 ^ 2 = 131 :=
                                                      Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 131)
                                                    subst hx
                                                    nlinarith [hsq, Real.sqrt_nonneg 131, heq,
                                                         sq_nonneg (Real.sqrt 131)]

                                                   end VisoredPaperExamples.Ex01

miniF2F mathd-algebra-116. A two-line CNL substitution. The Lean has to handle Real.sqrt 131, the
                                                                             √   2
squaring lemma Real.sq_sqrt, and a non-linear arithmetic discharge that needs 131 = 131 as an explicit
hint.




                                                  5
Visored CNL input (typeset)                                 Hand-written Lean 4 proof

Example 2. Let n ∈ N.
                      Pn−1                                  import Mathlib
                        k=0 (2k + 3) = (n + 1) − 1.
                                              2
The goal is to prove
         Pn−1                2
We have     k=0 (2k + 3) = n   + 2n.
                                                            namespace VisoredPaperExamples.Ex04
We have (n + 1)2 − 1 = n2 + 2n.
     Pn−1                                                   open Finset
        k=0 (2k + 3) = (n + 1) − 1.
                               2
Then
                                                            example (n : ℕ) :
                                                               ∑ k ∈ range n, (2 * k + 3) = (n + 1)^2 - 1 := by
                                                             induction n with
                                                             | zero => simp
                                                             | succ n ih =>
                                                               rw [sum_range_succ, ih]
                                                               have hexp : (n + 1 + 1)^2 = (n + 1)^2 + (2 * n +
                                                                     3) := by ring
                                                               have hge : 1 ≤ (n + 1)^2 := Nat.
                                                                    one_le_iff_ne_zero.mpr (by positivity)
                                                               omega

                                                            end VisoredPaperExamples.Ex04
                                      ∑n−1
                                        k=0 (2k + 3) = (n + 1) − 1. The CNL is three lines; the Lean side
                                                              2
miniF2F induction_sum2kp1npqsqm1.
does explicit induction, Finset.sum_range_succ, and omega for truncated N subtraction.

Visored CNL input (typeset)                                 Hand-written Lean 4 proof
                                              
Example 3. The goal is to prove 21 + 13    2 − 3
                                           1   1      5
                                                   = 36 .   import Mathlib
                        2  2
                 2 − 3           − 3 .
         1  1    1   1       1      1
We have 2 + 3            = 2
        2  2                                            namespace VisoredPaperExamples.Ex09
We have 21  − 13    = 14 − 91 .                             example : ((1 : ℚ) / 2 + 1 / 3) * (1 / 2 - 1 / 3) =
We have 14 − 19 = 36
                   5
                     .                                            5 / 36 := by
                    
       1
Then 2 + 3 1    1
                2 −  1
                     3
                            5
                         = 36 .                              norm_num

                                                            end VisoredPaperExamples.Ex09

miniF2F mathd-algebra-462. (1/2 + 1/3)(1/2 − 1/3) = 5/36. Closed by norm_num; an LLM that tries ring
will fail because the constants are rational.

   The full pipeline on the first input would proceed through the stages of Section 3: parse, type-check,
elaborate the assumption and the goal, dispatch the goal to the solver, accept. An accepted proof can
optionally be emitted as Lean source; the emitted Lean is more verbose than the hand-written version
(Section 7) but is structurally a sequence of named lemmas, each provable by a small targeted tactic.


5     Intended Usage
Visored is designed to be useful in four modes inside an LLM workflow. Each addresses a different
point at which an LLM workflow currently lacks reliable mathematical feedback. The four are design
intent rather than measured outcomes in this first paper: Section 6 reports a coverage study closest
to the autoformalizer mode, and Section 7 lists exercising the modes as future work. Throughout this
section we use low-level prover to mean a kernel-checked theorem prover with a code-like surface, such
as Lean, Rocq, or Isabelle.

Inference-time verifier. At deployment, Visored sits alongside the LLM as a real-time mathemat-
ical checker: the LLM emits a CNL draft, Visored either accepts it or returns a localized diagnostic,
and the user sees only formally-checked output while the interaction surface stays in natural language.
This is the deployment shape an end product would want — a math chatbot, tutoring system, or
research assistant that does not silently emit a hallucinated proof, without forcing the user to read
formal-prover syntax to know whether the answer is correct.

Autoformalizer loop. The LLM is prompted to write a LaTeX proof. Visored returns either
accepted or a localized diagnostic. The LLM rewrites the offending region and retries. Visored’s CNL
surface stays close to natural mathematical writing, so anyone who knows math can inspect both


                                                            6
the proof and the diagnostic. Compared to direct autoformalization targeting a low-level prover, the
human-in-the-loop barrier could be lower: a research mathematician who reads CNL fluently but not
the target prover can still sit in the loop and contribute to a formalization effort.

Dense reward for RL. Each elaboration step in Visored produces a check that can succeed or fail
independently. The per-step verdict can be exposed as a vector reward (one entry per step) rather than
a single scalar at the end of an attempt. Because Visored strips away low-level prover details and stays
hierarchical at the CNL level, the resulting signal is closer in spirit to a natural-language self-verifier
than to a low-level syntax checker, and the CNL hierarchy matches the mathematical decomposition
of the proof rather than the prover’s tactic substrate.

CNL data generator. A pipeline that prompts an LLM to write LaTeX proofs at scale and filters
with Visored is in effect an infinite generator of formally correct mathematical proofs in a natural-
language surface. The CNL vocabulary itself is configurable through spec files (Appendix B) and
can be tuned arbitrarily close to the conventions of any particular mathematical literature, so the
same pipeline can produce competition-math style, textbook style, or research-paper style proofs as
needed. The result is a free, unbounded corpus of formally checked yet naturally-reading mathematical
proofs — a renewable supply of clean math data that does not have to be curated by hand or scraped
from existing texts. Compared to scraping or auto-generating text from a low-level prover, CNL data
could give better transfer to natural-mathematical-writing tasks, because the surface stays close to the
distribution an LLM is already fluent on.


6    Experiments
We report a single, deliberately narrow result and do not oversell it. This first version of Visored is
meant as a prototype: its purpose is to work out the fundamental design issues across the four layers
it is built from — the CNL syntax, its semantics, the solver, and Lean transpilation — not to be
a finished, competitive prover. It is consequently an older system that has accumulated substantial
technical debt, and what follows is not an independent benchmark but a coverage study on one split
of miniF2F [50], conducted while the system was still being built. The number should be read as a
lower bound on what the design can already express, not as a tuned, competitive pass rate.

Setup. We work on miniF2F-valid (244 problems). A single LLM coding agent (Claude, driving
Visored through a documented skill that describes the CNL surface language and how to write and
verify proofs in it) is handed each problem’s formal statement as a CNL prefix and asked to finish the
proof. The loop is the ordinary agentic one: the agent drafts proof steps, runs the Visored CLI, reads
the diagnostic on failure, and revises. When a step exposed a gap — a deduction a mathematician
would consider routine but that Visored could not close — we recorded it and, where feasible, added
the corresponding rule to the library before continuing. The valid split therefore served as both our
development set and our evaluation set, and no bounded retry or sampling budget was imposed. This
is exactly the kind of co-development that makes the result a statement about expressivity, not about
held-out generalisation.

Coverage on miniF2F-valid. Under this protocol the agent produced Visored-checked proofs for
222 of 244 problems (91%). Table 1 breaks this down by problem source. Coverage is near-saturated
everywhere except the olympiad (IMO) problems, which are both the hardest mathematically and the
least supported by the current rule database.

Where it fails. Of the 22 unsolved problems, 13 are IMO problems. We want to be careful about
attribution: these are almost entirely Visored gaps, not the agent failing at the mathematics. In every
case the obstacle is a feature, rule, type, or piece of machinery that Visored does not yet have — a
missing AM–GM inequality, a sum of ⌊log⌋ terms, finite-field types Z/nZ that are unimplemented (two
problems), limit reasoning, trigonometric identities and sums, and, for the olympiad problems, more
substantial proof machinery (such as the inequality and descent techniques behind IMO 1988 P6 or
IMO 1978 P5). We have no evidence that the agent could not drive these proofs once the machinery is


                                                    7
                        Category                                     Solved / Total       Rate
                        Induction                                               8/8       100%
                        Algebra (mathd + custom)                              86 / 88      98%
                        Number theory (mathd + custom)                        66 / 68      97%
                        AMC                                                   42 / 45      93%
                        AIME                                                  13 / 15      87%
                        IMO                                                    7 / 20      35%
                        Total                                              222 / 244       91%

Table 1: miniF2F-valid coverage by problem source. “Solved” means the agent produced a proof that
Visored accepts; rules were added to the library as gaps were discovered, so these are coverage figures
on the development split rather than held-out pass rates.


in place — we simply have not added it yet. One further failure (IMO 1987 P4) is a plain regression —
an existential assertion that used to check and no longer does — which is the characteristic signature
of accumulated technical debt. Table 2 lists all 22 with the specific obstacle in each case; the broader
scope limitations are discussed in Section 7.

      Problem                                 Source     Why it remains unsolved
    (a) Needs substantial mathematical machinery Visored does not yet have
      imo-2006-p6                            IMO       Competition-level inequality.
      imo-1962-p4                            IMO       Nonlinear trigonometric equation.
      imo-1978-p5                            IMO       Rearrangement inequality.
      imo-1988-p6                            IMO       Vieta jumping; a famously hard olympiad problem.
      imo_1990_p3                            IMO       Long divisibility-chain argument.
    (b) Genuine prover gaps — a missing rule, capability, or type
      algebra-amgm-prod1toneq1-sum1tongeqn  Algebra     General AM–GM inequality is not in the rule library.
      mathd_algebra_31                      Algebra     Requires limit / fixed-point reasoning.
      aime-1994-p4                          AIME        Evaluating a sum of ⌊log⌋ terms.
      aime_1997_p12                         AIME        Closed form for a sum of sines and cosines.
      amc12b-2021-p21                       AMC         Transcendental equation (the agent also failed to find a
                                                        proof).
      amc12a_2003_p25                       AMC         Reasoning about a set fixed point S = f (S).
      amc12a_2003_p24                       AMC         Set maximisation / optimisation.
      mathd-numbertheory-232                NT          Finite-field type Z/31Z not supported.
      mathd_numbertheory_668                NT          Z/nZ constructor unimplemented.
      imo_1966_p4                           IMO         Needs trigonometric identities (tan = sin / cos not known).
      imo_1966_p5                           IMO         System of absolute-value equations.
      imo_1967_p3                           IMO         Product divisibility.
      imo_1977_p5                           IMO         Disjunction in the conclusion (division with remainder).
      imo_1979_p1                           IMO         Alternating harmonic sum / number theory.
      imo_1987_p6                           IMO         Prime-generating polynomial argument.
      imo_1993_p5                           IMO         Existence of a function (construction).
    (c) Regression
      imo-1987-p4                             IMO        A bare existential assertion that used to check no longer
                                                         does.


Table 2: The 22 miniF2F-valid problems Visored does not solve, grouped by what they need: (a)
substantial mathematical machinery not yet built, (b) a specific missing rule, capability, or type, (c)
a regression. All three are Visored-side gaps; none is attributed to the agent being unable to do the
mathematics.


The cost of Lean transpilation, and why we stopped here. The gaps above persist not
because they are conceptually hard to close but because of where this prototype spent its effort. The
dominant sink was Lean transpilation: we spent several months on it, largely because we had not yet
found the right way to organize the emitted proofs. The lasting consequences are a very large Lean
output1 — Section 7 reports a median of ≈ 250× the hand-written proof, with a tail to ∼ 25,000×
(see Appendix F) — and an incremental Lean recompilation far heavier than the design requires. The
effect is best stated comparatively: iterating on this codebase — add a rule, regenerate, recompile —
is much slower than the same loop in the successor prover we are now building with the design lessons
  1 Representative excerpts of this emitted Lean—the first chunks of one accepted proof per miniF2F subject, each

annotated with its full size—are public at https://github.com/xiyuzhai-husky-lang/visored.


                                                           8
this prototype taught us. So rather than keep grinding features into the old system, we stopped its
development once it had served its purpose: showing us how the four layers — syntax, semantics, the
solver, and Lean transpilation — should be organized. The unsolved problems are therefore a backlog
we chose not to clear on this codebase, not a frontier of what the design can express.

How to read these numbers. The honest claim is modest: Visored’s CNL surface and its current
rule library are already expressive enough that an LLM agent, in an ordinary verify-and-revise loop,
can drive 91% of miniF2F-valid to a checked proof. We do not claim competitive automated theorem
proving, we do not extrapolate to the test split, and we do not compare against systems run under
different protocols. We stop here deliberately.


7    Limitations and Future Work
We state current limitations honestly because they are concrete and addressable, not foundational.

Math scope. The current rule databases and prelude cover arithmetic, basic algebra, set theory,
elementary number theory, and parts of real analysis. Categories of miniF2F that require, e.g., heavy
combinatorial enumeration or sophisticated inequality manipulation are currently out of scope; sup-
porting them is a matter of adding rules, not changing the foundation.

Emitted-Lean verbosity. The current sparse emission scheme is extremely verbose — per-problem
line-count ratios on miniF2F-valid are heavy-tailed, with median ≈ 250× and a tail reaching ∼ 25,000×.
The full statistics and the design choices that drive them are in Appendix F.

Solver diagnostics. When the Miracle budget is exhausted without closing a goal, the diagnostic
reports the unclosed goal and source location but does not yet report which rule almost fired or how
close the best candidate was. Surfacing this would tighten the LLM-in-the-loop signal.

Type-system ceiling. The dependent-type system is intentionally lightweight. Mathematics whose
statement requires non-trivial dependent indexing or higher inductives is outside the current scope.
Visored’s role here is complementary: produce a usable formal corpus for elementary mathematics,
and hand off harder cases to the host prover.

Engineering maturity. Visored is research code. Rule organization, spec file layout, and IR bound-
aries are still moving; the system is a checkpoint of an evolving design rather than a stable platform.

Exercising the intended-usage modes. Each of the four modes in Section 5 is currently a design
intent rather than a measured outcome. A natural next step is to actually instantiate each: deploy
Visored as an inference-time verifier behind an LLM endpoint, drive an autoformalizer loop on miniF2F
with a frozen LLM, train an RL policy using Visored’s per-step verdict as a dense reward, and stand
up the CNL-data-generation pipeline at scale.

Richer CNL. The current CNL vocabulary covers the constructions needed for miniF2F-style proofs
but is still terse compared to textbook prose. Adding more idiomatic patterns — longer sentence
templates and standard shorthands like “for suﬀiciently large n”, “WLOG”, “passing to a subsequence”
— would make the CNL strictly more readable and closer to research-paper conventions.

Tactic mode through hints. The current solver runs autonomously: the user writes “Then …” and
Visored either closes the gap or fails. A tactic mode in which the user supplies optional hints (“by
induction on n”, “apply Cauchy-Schwarz”, “rewrite using lemma X”) would let an LLM (or a human)
steer the solver through hard steps without leaving the CNL surface.




                                                  9
References
 [1] Anthropic. Claude Code: An agentic coding tool that lives in your terminal. https://github.
     com/anthropics/claude-code, 2025.

 [2] Anysphere. Cursor: The AI code editor. https://cursor.com/, 2025.
 [3] Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Al-
     bert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck. Llemma: An open language model
     for mathematics. In International Conference on Learning Representations (ICLR), 2024.
 [4] Kevin Buzzard.Division by zero in type theory: a FAQ. Xena Project blog, https://
    xenaproject.wordpress.com/2020/07/05/division-by-zero-in-type-theory-a-faq/,
    2020.
 [5] Qinxiang Cao, Lihan Xie, and Junchi Yan. The LLM era demands natural-language-aligned theo-
     rem provers for mathematics. In Proc. 1st ACM SIGPLAN International Workshop on Language
     Models and Programming Languages (LMPL ’25), Singapore, 2025.
 [6] Luoxin Chen et al. Seed-Prover: Deep and broad reasoning for automated theorem proving. arXiv
     preprint arXiv:2507.23726, 2025. ByteDance Seed.
 [7] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
     Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
     Schulman. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168,
     2021.
 [8] Adrian De Lon, Peter Koepke, and Anton Lorenzen. Interpreting mathematical texts in Naproche-
     SAD. In Intelligent Computer Mathematics (CICM), 2020. Describes a generic parsing mechanism
     that generates Lean code from ForTheL statements; framed as “useful for writing readable ab-
     stracts” rather than as production-quality proof emission.
 [9] Kefan Dong and Tengyu Ma. STP: Self-play LLM theorem provers with iterative conjecturing
     and proving. arXiv preprint arXiv:2502.00212, 2025.
[10] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathematical
     exploration and discovery at scale. arXiv preprint arXiv:2511.02864, 2025.
[11] Google DeepMind. AI achieves silver-medal standard solving international mathematical olympiad
     problems. DeepMind Blog, 2024. AlphaProof and AlphaGeometry 2; full system paper later
     published in Nature (2025), https://www.nature.com/articles/s41586-025-09833-y.
[12] Google DeepMind.            Advanced version of         Gemini     with Deep      Think of-
     ficially    achieves   gold-medal   standard     at      the      international    mathemat-
     ical     olympiad.             DeepMind      Blog,
                                                    https://deepmind.google/blog/
    advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-int
    2025.
[13] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset.
     In NeurIPS Datasets and Benchmarks Track, 2021.
[14] Joseph Howlett.    AI just solved an 80-year-old ‘Erdős problem,’ and mathematicians
     are amazed.      Scientific American, https://www.scientificamerican.com/article/
     ai-just-solved-an-80-year-old-erdos-problem-and-mathematicians-are-amazed/,
     2026.       May 21,        2026. Gowers’s recommendation for Annals      of   Math-
     ematics     reported       by    Wells,    https://www.technology.org/2026/05/21/
     openai-erdos-unit-distance-proof-second-attempt/.

[15] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong
     Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large
     language models: Principles, taxonomy, challenges, and open questions. ACM Transactions on
     Information Systems, 2023.


                                                10
[16] Mikoláš Janota and Mirek Olšák. LLM2SMT: Building an SMT solver with zero human-written
     code. arXiv preprint arXiv:2603.06931, 2026. Conducted entirely inside Claude Code with the
     Claude Sonnet 4.6 model; reports that “proof generation was the most challenging aspect”, with
     Lean proof emission requiring significant human guidance and still failing on a number of problems.
[17] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang,
     Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM
     Computing Surveys, 55(12):Article 248, 2023.
[18] Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
     Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal theorem
     provers with informal proofs. In International Conference on Learning Representations (ICLR),
     2023.

[19] Yisi Ke, Tianyu Huang, Yankai Shu, Di He, Jingchu Gai, and Liwei Wang. Towards solving the
     Gilbert-Pollak conjecture via large language models. arXiv preprint arXiv:2601.22365, 2026.
[20] Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay
     Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam
     Neyshabur, Guy Gur-Ari, and Vedant Misra. Solving quantitative reasoning problems with lan-
     guage models. In Advances in Neural Information Processing Systems (NeurIPS), 2022.
[21] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
     Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover: A frontier model for open-source
     automated theorem proving. arXiv preprint arXiv:2502.07640, 2025.

[22] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
     Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
     Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover-V2: Scal-
     ing formal theorem proving with scaffolded data synthesis and self-correction. arXiv preprint
     arXiv:2508.03613, 2025.

[23] Adrian De Lon et al. Le Miz s’approche: Informalization and autoformalization with Mizar and
     Naproche. In Conference on Artificial Intelligence and Theorem Proving (AITP), 2025. Slides:
     http://aitp-conference.org/2025/slides/ADL.pdf.

[24] Adrian De Lon, Peter Koepke, Anton Lorenzen, Adrian Marti, Marcel Schütz, and Makarius
     Wenzel. The Isabelle/Naproche natural language proof assistant. In Conference on Automated
     Deduction (CADE), 2021.

[25] Patrick Massot. Verbose Lean 4: Tactics and commands for Lean in a controlled natural lan-
     guage. https://github.com/PatrickMassot/verbose-lean4, 2024. Software; ITP 2024 pa-
     per: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.27.
[26] Alexander Novikov et al. AlphaEvolve: A coding agent for scientific and algorithmic discovery.
     arXiv preprint arXiv:2506.13131, 2025. Google DeepMind.
[27] OpenAI. Codex CLI: A lightweight coding agent that runs in your terminal. https://github.
     com/openai/codex, 2025.

[28] Sam Owre, John M. Rushby, and Natarajan Shankar. PVS: A prototype verification system. In
     Conference on Automated Deduction (CADE), 1992.

[29] Shashank Pathak. GFLean: An autoformalisation framework for Lean via GF. arXiv preprint
     arXiv:2404.01234, 2024.
[30] Lawrence C. Paulson.       The de Bruijn criterion vs the LCF architecture.             https://
    lawrencecpaulson.github.io/2022/01/05/LCF.html, 2022.

[31] PLS Lab. The de Bruijn criterion. https://www.pls-lab.org/en/de_Bruijn_criterion,
     2023. Small, auditable kernels for proof assistants.



                                                  11
[32] Z. Z. Ren et al. DeepSeek-Prover-V2: Advancing formal mathematical reasoning via reinforcement
     learning for subgoal decomposition. arXiv preprint arXiv:2504.21801, 2025.
[33] John Rushby, Sam Owre, and Natarajan Shankar. Subtypes for specifications: Predicate subtyping
     in PVS. IEEE Transactions on Software Engineering, 24(9):709–720, 1998.
[34] SRI-CSL. PVS language reference: Types and TCC generation. https://github.com/SRI-CSL/
     PVS/blob/master/doc/language/types.tex, 2024. Documents context-propagation rules for
     TCCs through AND, OR, IMPLIES, and IF-THEN-ELSE.
[35] Terence Tao. Machine-assisted proof. Notices of the American Mathematical Society, 72(1):6–16,
     2025.
[36] Terence Tao. The story of Erdős problem #1026. Blog post on What’s new, https://terrytao.
     wordpress.com/2025/12/08/the-story-of-erdos-problem-126/, 2025. December 8, 2025.

[37] Terence Tao.   AI is ready for primetime in math and theoretical physics.  Ope-
     nAI    Academy    blog    interview,   https://academy.openai.com/public/blogs/
    terence-tao-ai-is-ready-for-primetime-in-math-and-theoretical-physics-2026-03-06,
    2026. March 6, 2026.
[38] Andrzej Trybulec et al. The Mizar mathematical library and its mathematical vernacular. Journal
     of Formalized Mathematics, 1990. Mizar system; project page: https://mizar.uwb.edu.pl/.
[39] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
     Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in Neural Information
     Processing Systems (NeurIPS), 2017.
[40] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, et al. Kimina-Prover
     preview: Towards large formal reasoning models with reinforcement learning. arXiv preprint
     arXiv:2504.11354, 2025.
[41] Yiping Wang. ScaleAutoResearch-Ramsey: Finding new Ramsey bounds through scaling au-
     toresearch. GitHub repository, https://github.com/ypwang61/ScaleAutoResearch-Ramsey,
     2026. Reports R(3, 17) ≥ 93 (first improvement since 1994) and R(4, 15) ≥ 160.
[42] Yiping Wang, Shao-Rong Su, Zhiyuan Zeng, Eva Xu, Liliang Ren, Xinyu Yang, Zeyi Huang,
     Xuehai He, Luyao Ma, Baolin Peng, Hao Cheng, Pengcheng He, Weizhu Chen, Shuohang Wang,
     Simon Shaolei Du, and Yelong Shen. ThetaEvolve: Test-time learning on open problems. arXiv
     preprint arXiv:2511.23473, 2025.
[43] Jelle Wemmenhove, Cosmin Manea, Jim Portegies, et al. Waterproof: A plugin for the Coq/Rocq
     proof assistant for writing proofs in a style resembling handwritten mathematics. https://
     github.com/impermeable/coq-waterproof, 2024. Software.

[44] Ke Weng, Lun Du, Sirui Li, Wangyue Lu, Haozhe Sun, Hengyu Liu, and Tiancheng Zhang.
     Autoformalization in the era of large language models: A survey. arXiv preprint arXiv:2505.23486,
     2025.
[45] EuroProofNet WG5. Integration of controlled natural language in formal mathematics systems.
     Deliverable 14, EuroProofNet, 2025.
[46] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik, and
     Christian Szegedy. Autoformalization with large language models. In Advances in Neural Infor-
     mation Processing Systems (NeurIPS), 2022.
[47] Lihan Xie, Zhicheng Hui, and Qinxiang Cao. A natural formalized proof language. In Con-
     ference on Automated Deduction (CADE), 2024. ProofGrader system; https://github.com/
     Laplace-Demon/ProofGrader.

[48] Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
     and Xiaodan Liang. DeepSeek-Prover: Advancing theorem proving in LLMs through large-scale
     synthetic data. arXiv preprint arXiv:2405.14333, 2024.


                                                 12
[49] Xiyu Zhai. On the Theory of Deep Learning. PhD thesis, Massachusetts Institute of Technol-
     ogy, 2024. Doctoral dissertation. The super-computation-graph machinery later carried over to
     Visored’s kernel originated here.
[50] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: a cross-system benchmark for
     formal Olympiad-level mathematics. In International Conference on Learning Representations
     (ICLR), 2022.




                                               13
A     Extended Related Work
A.1    Progress of AI for Mathematics
LLMs built on the Transformer [39] have become capable mathematical reasoners, with steady progress
on benchmarks such as GSM8K [7], MATH [13], and miniF2F [50], and further gains from math-
specialized pretraining as in Minerva [20] and Llemma [3]. At the top of competition mathematics,
two results from the same lab one year apart are telling: AlphaProof reached IMO 2024 silver by writing
formal (Lean) proofs via reinforcement learning (RL) [11], while a Gemini Deep Think configuration
reached IMO 2025 gold writing proofs in natural language, graded like human contestants [12]. That
the higher medal went to the informal-reasoning system is part of why we keep a prover’s surface close
to natural language.
    Beyond competition mathematics, AI has begun to contribute to research-level open problems.
AlphaEvolve improved or matched the state of the art on dozens of them, including Erdős’s minimum-
overlap conjecture and kissing-number bounds in dimension 11 [26]; three Erdős problems fell to
AI-assisted constructions in one week of late 2025, each verified by Terence Tao [36]; and an OpenAI
reasoning model beat the long-conjectured grid optimum for the 1946 Erdős planar unit-distance
problem [14]. Smaller academic efforts follow the same pattern: ThetaEvolve improves best-known
bounds on circle packing and an auto-correlation inequality with an 8B open model [42], a follow-on
autonomous-agent scaffold tightens the Ramsey number R(3, 17) for the first time in decades and lifts
R(4, 15) past the AlphaEvolve record [41], and LLM-generated geometric lemmas raise the certified
lower bound for the Steiner ratio, the Gilbert-Pollak conjecture [19]. Tao [10, 35, 37] reads this shift as
moving the binding constraint from generating mathematical ideas to verifying and organizing them
at scale. That is exactly what Visored targets: not another proof-search engine, but infrastructure for
checking and organizing AI-produced informal mathematics.

A.2    Prover Designs
We position Visored against four families of work an AI audience is likely to know: (i) direct LLM-
based autoformalization, (ii) controlled-natural-language (CNL) provers, (iii) human-friendly natural-
language tactic layers on top of existing provers, and (iv) rule-based proof checkers for structured
natural-language proofs.

Direct LLM autoformalization and whole-proof Lean models. The natural baseline is to fine-
tune or prompt an LLM to map an informal statement and/or proof directly to Lean or Isabelle source.
Wu et al. [46] establish the basic setup for Isabelle/HOL and report state-of-the-art on miniF2F at
the time. Draft, Sketch, and Prove [18] extends this by first drafting an informal proof, sketching a
formal skeleton, and letting an automated theorem prover fill the gaps. A fast-moving line of whole-
proof Lean models has since pushed pass rates much higher: DeepSeek-Prover and its V2 [48, 32] scale
synthetic data and reinforcement learning targeting Lean 4; STP [9] trains a conjecturer and a prover
against each other to escape the limited supply of formal data; Goedel-Prover and its V2 [21, 22] add
scaffolded data synthesis and verifier-guided self-correction; Kimina-Prover [40] trains a large formal
reasoning model with long-form reasoning; and Seed-Prover [6] adopts lemma-style proving, reporting
that it saturates miniF2F while solving most recent IMO problems. Two things separate this line
from Visored. First, these systems take an already formalized statement as input and produce a proof,
whereas Visored’s input is the informal LaTeX surface; the hard surface-to-semantics decisions sit
upstream of where these provers begin. Second, the natural checkpoint of an end-to-end pipeline is the
final Lean file as a whole, so per-attempt feedback to the LLM is typically a single accept/reject after
compilation. Visored instead keeps a checkable IR at every stage, so failures are localized to a specific
sub-expression and the per-stage diagnostic is itself usable as a denser reward signal. This is a design
difference, not a critique: end-to-end translation and stage-by-stage elaboration are complementary
points in the design space.

CNL provers. Mizar [38] has, since the 1970s, accepted proofs written in a mathematical vernacular
— a controlled English-like syntax compiled against the Mizar Mathematical Library; the longevity
of the project is evidence that mathematically structured natural language can carry a precise formal



                                                    14
semantics. Isabelle/Naproche [24] is the modern reference point: a ForTheL CNL frontend whose
obligations are discharged by automated theorem provers via TPTP. Differences with Visored:
• Surface coverage. Both Naproche and Visored accept a controlled subset of mathematical English,
    not unrestricted prose. The difference is in how the subset is defined and extended. ForTheL is a
    fixed, explicitly designed grammar that the writer learns; widening it means a Naproche release.
    Visored’s accepted subset is defined externally by .lpcsv spec files (Appendix B) and extended by
    adding entries rather than by modifying the parser. The default vocabulary aims to cover what a
    typical LLM emits when asked to write a proof in LaTeX, but inputs outside the configured subset
    are rejected, with a localized diagnostic, just as in Naproche.
• Foundation. Naproche translates ForTheL into first-order logic. Visored is dependently typed,
    which is what lets the same proof be re-expressed in a dependently typed target like Lean 4.
• Solver philosophy. Naproche calls out to general-purpose ATPs (E, Vampire) for each obligation.
    Visored’s solver is custom and rule-database-driven, with a non-deterministic cost-bounded runtime
    (Miracle); this trades general-purpose power for predictable per-step cost and per-step diagnostics,
    both of which matter for LLM-in-the-loop use.
GFLean [29] uses the Grammatical Framework as the parsing layer and emits Lean from a subset of
ForTheL (“Simplified ForTheL”). It shares the CNL flavor but, by design, accepts a smaller surface
language than Naproche or Visored, and is not aimed at an LLM-driven workflow.
     Recent work has begun to use these CNL systems as the translation interface for autoformalization
rather than the end target. De Lon et al. [23] present a bidirectional verifiability-preserving syntactic
translation between Mizar and a Naproche-ZF–style CNL, with the explicit motivation that LLMs
have seen far more natural-language mathematics in training than formal source. The EuroProofNet
WG5 white paper [45] surveys the integration of CNL in formal mathematics systems and articulates
the shared design space (informalization, synthetic-data pipelines, ATP back-ends). Both treat CNL
as a layer wrapped around an existing formal system. Visored shares the CNL premise but inverts the
role: CNL is the primary medium the prover operates on, and existing formal systems are reached —
if at all — as optional emission targets.

Natural-language tactic layers on top of existing provers. Verbose Lean [25] provides Lean
4 tactics whose surface syntax reads as controlled English (or French), targeted at teaching pen-and-
paper proof writing. Waterproof [43] plays the analogous role for Rocq/Coq, with English-language
tactic wrappers and an automation tactic (waterprove) over customizable hint databases, again aimed
at undergraduate teaching. Both are UX layers rather than independent provers: the user is still
writing in (a more readable form of) the host prover, and the type system, library, and verifier are all
the host’s. Visored sits earlier in the stack — the user writes mathematical English / LaTeX, and the
host prover is reached only as an emission step, if at all.

Proof checkers. ProofGrader [47] is a rule-based checker for natural-language-like proofs, with its
own formal semantics for each proof construct. The ProofGrader project’s focus, as we read it, was
not on building or targeting a minimal foundational kernel but on the surface syntax and solver design
that together give a natural API for textbook-style mathematical proofs — a design goal closely
aligned with Visored’s. The ProofGrader solver — a configurable solver manager with per-solver
cost budgets, dynamic priority scheduling, and hierarchical sub-proposition decomposition — fits the
structure of textbook mathematical proofs better than SAT/SMT, and is the closest design match to
Visored’s Miracle runtime. Visored complements this line of work with a dependently-typed IR, and
accepted proofs can be optionally re-emitted as Lean 4 source for users who want external kernel-level
re-verification.

Well-definedness at elaboration time. Whether 1/x should be accepted before x ̸= 0 has been
established splits the landscape. PVS [28, 33] attaches the side conditions to the types of partial
functions via predicate subtyping — division has signature [real, nonzero_real → real], square root
has [nnreal → nnreal], log has [posreal → real] — so applying any of them to a wider-typed argument
generates a type-correctness condition (TCC) at typecheck time. The dominant alternative — Lean,
Rocq, Mathlib, Mizar — makes the partial functions total by convention (1/0 ≡ 0 in Lean and Rocq [4];
Mizar follows the same convention) and surfaces the side condition only when a downstream lemma
needs it. The landscape factors along two axes:


                                                   15
                                  Surface                     Well-definedness mechanism
 PVS                              code-like (spec language)   predicate subtyping → TCCs at typecheck
 Lean / Rocq / Mizar / Mathlib    code-like                   totalization convention (1/0 ≡ 0)
 Visored                          CNL (LaTeX)                 implicit hypothesis arguments per expression

    Visored takes the upfront-discipline path of PVS, but realizes it by treating every user-written ex-
pression as possibly carrying implicit hypothesis arguments that the elaborator must discharge as proof
obligations, rather than by encoding them into a richer type system. The obligations are discharged
on the spot by the same solver that closes “Then …” gaps; see Appendix E for the mechanism. The
pay-off for an LLM workflow is a single uniform diagnostic stream covering both missing lemmas and
missing positivity / non-zero conditions, with no transition to a separate specification language.

Natural formalized languages. A recent position paper by Cao, Xie, and Yan [5] argues that the
LLM era calls for a new class of theorem provers whose surface is a natural formalized language — a
proof language with three required properties: (i) rigorous formal semantics, (ii) maximal approxima-
tion to how mathematicians actually write, and (iii) accurate representation of the proof structures
that conventional provers were not designed to express. The structures the paper highlights as out
of reach for traditional provers include instantiation indicated by identical variable names, the fluid
free-or-bound status of a variable across a proof, the gap between definite and indefinite binders in
integral notation, and the postulate–derive–verify pattern of problem-solving proofs. The paper does
not propose a specific implementation; it identifies these informal-proof features and calls for the de-
sign space to be explored. Visored is one concrete attempt at a prover in this class: the CNL surface
(Appendix B), the spec-driven extensible vocabulary, the implicit-hypothesis-argument treatment of
partial functions (Appendix C), the per-step diagnostic channel, and the rule-driven solver are all
attempts at the design moves the position paper sketches.

Visored as an attempted synthesis. Read together, the four families above describe a design space
that has been partially explored from four different directions. Each direction contributed something
distinct: Mizar and Naproche showed that mathematically structured natural language can carry a
precise formal semantics; PVS showed that partial-function side conditions belong at typecheck time,
with context flowing asymmetrically through boolean connectives; Lean / Rocq and their Mathlib-style
libraries showed that a dependently-typed kernel plus a large rule library is a workable foundation for
modern formal mathematics; ProofGrader and related rule-based checkers showed that cost-budgeted,
priority-scheduled search over a domain-specific rule database fits the structure of textbook proofs
better than SAT/SMT engines; and the recent LLM-autoformalization literature reframed the goal as
producing usable training and reward signal for foundation models rather than just verified artifacts.
    Visored is best understood as an early-prototype attempt to combine these into one stack: a
LaTeX/CNL surface (Mizar / Naproche tradition), a dependently-typed IR with predicate-subtyping-
style well-definedness (PVS), a rule-database-driven cost-bounded solver (the ProofGrader school),
optional emission to a dependently-typed host prover for kernel-level re-verification (Lean), and a
localized, structured diagnostic channel designed from the start to be consumed by an LLM in a retry
/ RL loop (the autoformalization literature). We do not claim any individual ingredient is novel; what
we are testing is whether the combination is more than the sum of its parts for an AI-driven workflow.
The experiments in Section 6 and the limitations in Section 7 report where the combination works
today and where it does not.


B     Syntax
This appendix describes the surface language and the parser that turns it into a Visored syntax tree.
The vocabulary — both the sentence templates and the LaTeX commands they wrap — lives in
external .lpcsv (lisp-csv) spec files. Extending Visored to recognize a new sentence form or a new
LaTeX command is a matter of adding entries to those files; the parser is not touched.




                                                   16
B.1     Sentence templates
Proof content lives inside example environments and is structured into sentences. The sentence-
template vocabulary maps natural-language patterns to abstract syntactic constructors. Representa-
tive entries:

      `Let {formula}`                                                   => let
      `Let {x: formula} be a function defined by {def}`                 => let_function_like_defined_by
      `Let {formula} be such that {prop}`                               => let_such
      `Assume {formula}`                                                => assume
      `Then {prop}`                                                     => have
      `Thus, {prop}`                                                    => have
      `Hence, {prop}`                                                   => have
      `Therefore, {prop}`                                               => have
      `We have {prop}`                                                  => have
      `Since {p}, {q}`                                                  => have_hinted q (since p)
      `Note that {prop}`                                                => have
      `The goal is to prove {prop}`                                     => goal
      `It is enough to prove {prop}`                                    => show
      `We prove {prop} by induction on {var}`                           => induction
      `We prove {prop} by contradiction`                                => apagoge
      `We prove {prop} by working through different cases`              => cases
      `We prove {prop} by arguing from both sides`                      => bilateral
      `Case {prop}`                                                     => case
      `Contradiction`                                                   => contradiction
      `Claim: {prop}`                                                   => claim

   Each constructor admits several natural-language variants, so common rewordings (“Thus”, “Hence”,
“Therefore”) reach the same parse without per-variant special cases. The pattern grammar supports
optional tokens, optional letters inside words (view[s] matches both view and views), and choice
(a|b).

B.2     Notional propositions
“X is P ” constructions are recognized as predicate applications, with positive and negated natural-
language forms declared together so that “X is non-empty”, “X is not empty”, and “X is nonempty”
all parse to ¬empty(X). The current vocabulary covers
      prime, even, odd, empty, finite, infinite, injective, surjective, bijective,

each in several surface variants (“is finite”, “is a finite set”, “is an injection”, “is an injective function”,
“is not an injection”, …).

B.3     Existential introductions
Existential introduction is one of the constructs where natural mathematical prose is the most varied.
The same constructor is reached by all of the following surface forms (and more):

      `There exists {x} such that {p}`                     => let_such
      `There exist {x} such that {p}`                      => let_such
      `Take {x} such that {p}`                             => let_such
      `Choose {x} such that {p}`                           => let_such
      `Assume there exists {x} so that {p}`                => let_such
      `There exists {ty} {x} such that {p}`                => let_indefinite_such
      `Let {x} be {ty} such that {p}`                      => let_definite_such

   Both “be so that” and “be such that” phrasings are accepted; both singular and plural existence
(“there exists / there exist”) reach the same constructor.




                                                      17
B.4    LaTeX math vocabulary
Inside the formula slot of any template, the user writes ordinary LaTeX math. Each LaTeX command
is matched against an entry in the math-vocabulary spec files, which pin down its arity, fixity, and
meaning. The base vocabulary covers:
• Number systems and propositional types: N, Z, Q, R, C, Prop, True, False.
• Constants: e, π, i.
• Comparison and equivalence: =, ̸=, <, ≤, >, ≥, ≡, ≈.         ∪ ∩
• Set relations and operations: ∈, ∈,       / ⊆, ⊇, ⊊, ∪, ∩, \, , .
• Logical connectives and quantifiers: ∧, ∨, ¬, →, ↔, ∀, ∃.
• Arithmetic: +, −, ·, ×, /, , ±, mod, ()     (mod ).
• Number theory:∑|,∏      ∤, gcd,
                              ∫   lcm,    .
• Big operators:         , , , lim, sup, inf, max, min.
                                                      √
• Common functions: sin, cos, tan, log, ln, exp, .
• Greek letters: all lowercase (including varepsilon, vartheta, varphi etc.) and uppercase
   (Γ, ∆, Θ, Λ, Ξ, Π, Σ, Υ, Φ, Ψ, Ω).
    Subject-specific commands (calculus, complex analysis, elementary number theory) live in sepa-
rate spec files and are loaded on demand. A LaTeX command the spec does not declare yields an
UnknownCommand diagnostic pointing at the offending token.


B.5    Environments
Document-structure environments are recognized but mostly transparent: example, proof, theorem,
lemma, corollary, proposition, equation, align, matrix, pmatrix, cases, itemize, enumerate,
figure, table. Proof content must live inside a proof-bearing environment such as example; struc-
tural environments outside that scope are ignored.

B.6    From source to syntax tree
Parsing produces a tree of Visored Syn nodes. Each node carries the source span it came from, the
resolved template or LaTeX command, and the (still untyped) sub-trees. This is the input to the Sem
stage (Appendix C). As described in Section 3, math mode and text mode are parsed with different
strategies — a precedence stack-based parser and a trie-like sentence-pattern matcher — and both
produce nodes in the same Syn tree.

B.7    Scope and disambiguation
Visored accepts a controlled subset of mathematical English embedded in LaTeX, not arbitrary prose.
Within that subset the parser is intentionally tolerant of surface variation — punctuation, whitespace,
common synonyms for the same construct — because these are cheap to enumerate in the spec. Inputs
outside the configured subset are rejected with a localized diagnostic; we do not silently coerce or
paper over them. The subset can be widened by adding spec entries; we have not had to modify the
parser to support a new sentence form. Disambiguation that requires types — e.g. deciding whether
\, in f(x) y is multiplication or function application — is deferred to the Sem stage (Appendix C)
rather than overloading the parser.


C     Semantics
This appendix describes how a Visored syntax tree is given meaning — the type and kind system,
name resolution, and where well-definedness obligations enter the pipeline.

Kinds and types. Every Visored expression carries a kind (the broad ontological category — Num,
Set, Prop, Function, …) and a type (the specific mathematical object — N, R, C, a function space,
a finite set). Kinds are coarse and decidable;
                                       √       types are finer, dependent-flavored, and admit predicate
subtyping (Appendix A). Atoms like x have a natural-domain type (nnreal for the principal real
square root) and the elaborator emits a well-definedness obligation when the argument’s type does not
already match.


                                                  18
Bottom-up typing vs ML-style top-down elaboration. A central design choice is that each
subexpression in Visored is typed at the least type it naturally lives in, rather than at whatever
ambient type the surrounding context dictates. Contrast this with ML-style top-down elaboration
(“ML” here is the typed functional-language tradition, such as Standard ML and OCaml, not machine
learning) as found in Lean / Rocq / Mathlib: when Lean elaborates a surface expression like (3 : N) · x
in an ambient type C with x : R, it inserts coercions wherever they are locally needed — on individual
atoms or in unification-driven positions — and the same mathematical expression can elaborate into
different ASTs depending on where annotations and context sit. Visored builds expressions bottom-
up from atoms: the multiplication 3 · x first lives in R (the least common type of N and R), and a
coercion into C appears only at the outermost point where the type genuinely changes. The AST
is canonical with respect to mathematical structure rather than annotation position, which is what
makes the typed pattern matching used by the rule databases (Appendix E) tractable. When an
accepted proof is re-expressed as Lean, a dedicated pull_cast_rewrite pass lifts the Lean-side ML-
style coercion arrangement back into Visored’s bottom-up canonical form before any Visored-derived
lemma is applied.

Name resolution. Each identifier is resolved against a stack of namespaces: the local proof con-
text first (variables introduced by “Let …”, “Assume …”), then any Set-builder or quantifier binders
currently in scope, then the global symbol table loaded from .lpcsv spec files. The resolver is con-
servative: an ambiguous identifier yields a diagnostic rather than a silent choice, so the LLM gets a
localized signal it can act on.

Signature dispatch tables. The semantic resolution of an operator application — which signature
to instantiate for 2 + x when 2 : N and x : R — is decided by a table lookup, not by a hand-written
dispatcher. For each base operator class (binary operators, prefix operators, fractions, powers, square
roots, etc.) a .lpcsv dispatch file declares rows of the form (lhs-type, operator, rhs-type) →
signature-ident, and a separate signature_table.lpcsv declares each signature’s instantiation
and the underlying signature-data variant. The .lpcsv format is a small Lisp dialect (lisp-csv) that
supports parenthesized compound atoms like (subset nat), which lets a single signature dispatch
row cover an entire family of types uniformly. Adding a new operator overload or a new pair of
numeric-type combinations is a matter of adding entries to these files; the elaborator source is not
touched.

Sem AST. The output of the Sem stage is a typed syntax tree (the sem AST). Each node has a
resolved type, a kind, the list of free variables it depends on, and the list of well-definedness obligations
its sub-expressions generated — these obligations are propagated upward with the context-flow rule
described in Appendix A (under a ∧ e the obligations of e are guarded by a; under if-then-else branches
are guarded by the test and its negation).

Substrate for later stages. The Sem AST is the substrate on which the MIR lowering, the solver,
and the optional Lean emitter all operate. Pattern matching used by the rule databases (Appendix E)
is typed pattern matching on this tree, not on raw text or the surface CNL.


D     Kernel: the Super Computation Graph
Visored’s expressions, hypotheses, and derivations are all built on top of a single underlying graph
structure — the super computation graph — carried over from the first author’s PhD thesis on deep
learning theory [49], where the same structure was developed to reason about computational depen-
dencies in deep networks. The proof-world analogue treats every object the elaborator manipulates as
a node in this graph, and the graph’s structure is what drives lemma parameter lists in Lean emis-
sion, hypothesis activation under quantifier and implication introduction, and the dispatch logic that
survives changes in the active context.




                                                     19
D.1    Reishi and reiatsu
A reishi (霊子, “spirit particle”) is a free node in the super computation graph. Each reishi carries
a unique ID, a data variant (universe, variable, hypothesis, …), and recursively the reiatsu of its own
upstream dependencies. Reishi are interned: the same logical dependency yields the same ID, which
gives reishi-DAGs structural equality and lets the elaborator deduplicate dependencies across the proof.
    A reiatsu (霊圧, “spiritual pressure”) is an ordered set of reishi: the transitive closure of a node’s
free-node dependencies. When a hypothesis or derivation is emitted as a Lean theorem or lemma,
its reiatsu becomes that theorem’s parameter list, and the reishi-DAG is walked in topological order
so that every dependency is defined before use. This is the source of the parameter packets one sees
on every emitted lemma (the “coercion-witness arguments” of Appendix F are concrete instances of
reishi).

D.2    Ascension
The super computation graph allows free nodes to be turned on and off: a downstream node is available
only when its upstream free reishi are active. We call the operation of activating a previously-inactive
free node and lifting a downstream proof through it ascension.
    Concretely, ascension lifts a node in the super computation graph — any node, not only a proof;
a term, a hypothesis, or a derivation step is equally a valid argument — over an ascension step: a Let
binder for a single variable, an Assume for a hypothesis, or a forall / implication introduction. Several
ascension steps can be chained.
    The non-trivial part is that ascension must respect type dependency. Given (a : A) and (b : B a)
with b’s type depending on a, ascending a in isolation is ill-formed — the downstream node b refers to
a, so a has to be ascended together with b, and with anything else downstream of a in the reishi-DAG.
In general, an ascension step lifts a node together with the entire forward cone of its dependants.
This is what lets the rest of the system manipulate proofs and terms uniformly at the level of bound
variables and free assumptions without re-running the underlying reasoning, and it is the kernel-level
operation behind the introduction of every universal quantifier and implication in an accepted Visored
proof.

D.3    Montage
Because free nodes can be turned on and off, a downstream construction may become temporarily
unavailable when an upstream free reishi is deactivated. A montage is a small data structure that
holds a list of objects each tagged with its reiatsu, and on query returns the first object whose reiatsu
is currently alive. Montage is what lets the solver dispatch over multiple possible witnesses without
crashing when some are temporarily out of scope — a routine occurrence when ascension steps move
proofs across activation boundaries.

D.4    What this buys
The super computation graph as the underlying object has three concrete payoffs in Visored. First,
hypothesis and derivation dependencies are tracked explicitly and globally, so a Lean lemma can be
emitted with exactly the parameters it needs — no more, no less — without per-emission analysis.
Second, ascension gives a uniform kernel-level account of quantifier and implication introduction, so
the higher-level mechanisms (Section E.8) that introduce phantom hypotheses do not have to reinvent
the bookkeeping each time. Third, montage gives the solver a robust way to keep multiple candidate
witnesses alive across context changes, which is essential to the cost-budgeted search style of the
Miracle runtime (Section E.3).


E     Solver Internals
This appendix gives a concrete description of the solver: the rule databases, the rule format, the
Miracle runtime that schedules everything under a cost budget, the well-definedness machinery that
hangs off of it, and the bestiary of named tactics it dispatches.



                                                   20
E.1    Rule databases
Auto rules are organised into two databases by their direction of application. Backward rules live in the
Tekken Tachikaze database: when a goal q comes up, the solver searches for a rule whose conclusion
unifies with q and recurses on the rule’s assumptions. Forward rules live in the Ashisogi Jizō database:
when a fresh hypothesis h is derived, the solver searches for a rule whose assumption matches h and
adds the rule’s conclusion as a new hypothesis. Each database is indexed by a discrimination tree over
the rule’s pattern shape, so lookup is sub-linear in the number of rules.

E.2    Rule format
Rules are written as LaTeX propositions in spec files (one file per rule database under the project’s
specs/ tree) using the same surface syntax as user input:
      \begin{proposition}
          [rule-name]
          \label{prop:rule_name}
          Let $x, y \in \mathbb{R}$.
          Assume <pattern>.
          Then <conclusion>.
      \end{proposition}

A rule is loaded into the appropriate database after the project’s specs are read, and is available to
the solver on every subsequent proof obligation. Adding a new rule does not require touching the
elaborator source.

E.3    The Miracle runtime
The solver runs inside a runtime we call Miracle, which evaluates a non-deterministic computation
under a global cost budget. Each candidate continuation (e.g. a different rule fired against the same
goal) is enqueued with a fee; the runtime explores in priority order and aborts a branch as soon
as its accumulated cost exceeds the budget. Hierarchical decomposition is natural: a sub-obligation
gets its own sub-budget. The budget bounds end-to-end work and rules out non-termination, while
the per-step fee scheme lets cheap and reliable rules fire first. This cost-budgeted, priority-scheduled
search is similar in spirit to the cost system in ProofGrader [47], which manages multiple sub-solvers
with per-solver cost budgets and dynamic priority scheduling over hierarchical proof obligations. The
name is not coincidence: the connotation is a deliberate, costly intervention — something the runtime
reaches for only when its narrower tactics have not closed the goal.

E.4    Diagnostic on failure
When the budget is exhausted without closing a goal, Miracle reports the goal that was being at-
tempted together with the source location it traces back to. This is the diagnostic an LLM sees in the
autoformalizer loop. (A current limitation is that the diagnostic does not yet report which rule almost
fired or how close the best candidate came; see Section 7.)

E.5    Well-definedness obligations
Every user-written expression might carry implicit hypothesis arguments — proof obligations the
elaborator must discharge before the expression is accepted. The elaborator carries a per-operator
description of what each partial-function application demands: field division demands that the divisor
be non-zero; integer powers of a possibly-negative base demand either that the base be non-zero
or that the exponent be non-negative; the real logarithm demands its argument be positive; the
inverse of a function-like object demands bijectivity; and the various ab regimes (real-to-real, real-to-
complex, non-negative-base-to-positive-real-exponent, real-to-integer, real-to-natural) each carry the
appropriate domain conditions. Function signatures themselves remain plain (division is R → R → R,
as in Lean / Rocq / Mathlib); the obligation set lives in the elaborator, not in the type. Each emitted
obligation is added to the current proof state and discharged by the same Miracle runtime that closes
“Then …” gaps; an application whose obligations cannot be closed is rejected with a diagnostic at the
offending sub-expression.


                                                   21
E.6    The normalisation system
Visored carries a unified normalisation pass on expressions that turns every accepted (well-defined)
expression into a canonical form. The pass is stronger than what a ring normaliser (ring_nf) or
field normaliser (field_nf) can do safely without help, because the elaborator has already discharged
the well-definedness obligations of every sub-expression: the normaliser is free to carry out deeper
reductions that would otherwise be unsound. For instance, once x ̸= 0 is in the hypothesis state,
x/x normalises to 1 unconditionally; comparable reductions fire across multiplication by an inverse,
exponentiation by zero or one, division by literals, log of a power, and so on. The implementation
is intricate — each operator class carries its own normalisation rules, and the system runs them to a
fixed point — and we do not document the full rule set in this paper.
    The normaliser is what makes the rule databases tractable. Without canonical forms, a discrimina-
tion tree over rules would have to anticipate every algebraically-equivalent shape of the same expression,
and the rule databases would grow combinatorially. With canonical forms, the discrimination tree only
needs to match the canonical shape. Normalisation is the system’s primary way of making algebraic
reasoning cheap.

Cost on the transpilation side. The same normalisation pass is the largest single source of ver-
bosity in emitted Lean (Appendix F). Normalisation is cheap on the Visored side — a single fixed-point
pass per expression — but Lean has no comparable normaliser available to call back into (ring_nf and
field_nf cannot use well-definedness facts to discharge their side conditions), so when an accepted
proof is transpiled, the emitter has to spell out the normalisation history one primitive rewrite at a
time. The emitted file ends up resembling an interpreter trace of the Visored normaliser running on
the input.

E.7    Asymmetric context propagation across boolean connectives
When the elaborator processes a ∧ b, the hypothesis stack is updated with a before b is processed, so b’s
well-definedness obligations are checked under the assumption a. Concretely, the conjunction-folding
ambush adds the left conjunct to the spotlight before processing the right one, so a fact derivable from
a — say x ̸= 0 from 1 < x — is available when b’s well-definedness is checked. The reverse direction
does not hold: writing a ∧ b does not let one assume b when checking a. The same asymmetric flow
holds for a → b (assume a when checking b’s well-definedness) and for if a then b else c (check b under
a, c under ¬a). This matches the rule PVS adopted in the early 1990s for its TCCs [34], arrived at
here independently from a CNL surface.

E.8    A bestiary of solver mechanisms
Internal solver mechanisms in Visored carry evocative rather than descriptive names. Every mechanism
has its own module, and the module’s docstring explains what the code actually does; the names
recurring below act as a navigational handle in the source tree. The mechanisms below call each other
recursively — a tactic on a goal will invoke other tactics on its sub-goals, and an ambush on a fresh
hypothesis can trigger further ambushes — with the Miracle runtime pruning unproductive branches
under its global cost budget. The overall solver behaviour emerges from the interaction of many such
mechanisms rather than from any single one.

Tekken Tachikaze 鐵拳断風 — lightweight backward sweep. Iron-Fist Wind-Cleaver. A large
database of cheap backward-reasoning rules, each firing fast on a goal. Collectively they cover most
common deductions; the runtime tries them first because their cost is negligible. One sweep, many
small things felled.

Mashiro Kikku マシロキック — non-recursive trivial close. White Kick. Like Tekken Tachikaze,
but its rule database fires trivially and without recursion: a single decisive pass that closes whatever
it can immediately, then stops.




                                                   22
Ashisogi Jizō 疋殺地蔵 and Konjiki Ashisogi Jizō 金色疋殺地蔵 — forward propagation.
Foot-Killer Jizō; Golden Foot-Killer Jizō. Forward propagation on a freshly derived fact: pattern-
match on its shape (logical folds, numeric or set chains, applications, quantified expressions) and add
every immediate consequence to the hypothesis stack. Once it fires, the consequences spread outward
and the affected proposition cannot escape them. The golden variant specialises in chaining-separated
lists with exactly two elements.

Hyōrinmaru 氷輪丸 — algebra. Ice-Ring Pinwheel. The algebra solver. It freezes continuous alge-
braic structure into discrete combinatorial witnesses: integer-interval saturation (cutsat1dx), modular
implications, GCD/LCM via prime-factor decomposition, and rationality / non-rationality assertions
for radicals.

Ryūjin Jakka 流刃若火 — analysis. Flowing-Blade Young-Flame. The analysis solver, paired with
Hyōrinmaru: where the ice freezes algebra into discrete combinatorial witnesses, the flame fuses scat-
tered analytic constraints into single sweeping ones. Currently it merges scattered interval constraints
into unified intervals, both for continuous real intervals and discrete integer intervals.

Sode no Shirayuki 袖白雪 and Zabimaru 蛇尾丸 — qualified hypothesis instantiation.
Sleeve of White Snow; Snake-Tail Pinwheel. A family that discharges the goal by drawing on qualified
hypotheses already in the proof context and instantiating them. Sode no Shirayuki operates at the
general expression level, pulling from the rukia inventory of explicit and implicit context-rules — the
visible patterns drawn out of the sleeve, and the hidden ones woven beneath. Zabimaru is the chain-
specialised counterpart: pulling from the renji inventory indexed by the chain’s left-hand side, then
bridging the remaining gap via the Kurapika link-prover — a segmented whip-blade each section of
which locks onto one link.

Zangetsu 斬 月 and Tensa Zangetsu 天 鎖 斬 月 — congruence reduction. Slaying Moon;
Heaven-Chain Slaying Moon. Equality reduction in the spirit of Lean’s congr / gcongr. Zangetsu
cuts both sides through a common structure: ln x = ln y ⇝ x = y, |x| = |y| ⇝ x = y ∨ x = −y. Tensa
Zangetsu is the asymmetric, sharper variant — it cuts only one side (log x = y ⇝ x = exp y) and can
fire only once per goal.

Senbonzakura 千本桜 and Senbonzakura Kageyoshi 千本桜景厳 — heavy library search.
Thousand Cherry Blossoms; Thousand Cherry Blossoms Vista. A thorough sweep through the library:
Senbonzakura tries each rule against the current target and keeps a match only when the result is
syntactically equivalent. The more powerful variant Kageyoshi extends the sweep further, accepting
matches via an additional implicational transformation rather than strict equivalence — a sprawling
field of petals where the smaller variant was already a dense one.

Kyōka Suigetsu 鏡花水月 — ephemeral conditional hypothesis. Mirror-Flower Water-Moon.
Proves ∀x. P (x), p → q, and the internal imb form by introducing a phantom hypothesis — the bound
variable, or the antecedent — that the system temporarily believes in while it proves the body. Once
the body is proved, ascension (Appendix D.2) is what lifts the result past the phantom hypothesis
to close the unconditional outer goal; the hypothesis dissolves in the act of ascending. Ascension is
critical to this mechanism, which is fitting — ascent is, in another setting, what this name’s wielder is
best known for pursuing.

Hōzukimaru 鬼灯丸 and Ryūmon Hōzukimaru 龍紋鬼灯丸 — two chains into one. Demon-
Lantern Pinwheel; Dragon-Crest Demon-Lantern. “Obtain one chain from two chains”: merges two
chaining-separated lists into a single chain by dispatching on the separator (numeric, propositional, or
set) and applying a joining rule. Ryūmon Hōzukimaru, the more powerful variant, runs the same merge
with try_apply_new instead of try_apply_new_trivially, allowing the join to fire on a non-trivial
rule application.




                                                   23
Kazeshini 風死 and Kazeshini Fushi no Kōjō 風死・不死の工場 — weaken existing hypoth-
esis. Wind-Death; Wind-Death Immortal Factory. Discharges the goal by weakening an existing
context hypothesis at wind-like speed: x > 5 weakens to x ≥ 5, x < y weakens to x ̸= y, and so
on, with sub-cases for propositions, numerics, sets, and modular equivalences. The Immortal Factory
variant restricts the weakening search to primary hypotheses — the first-principles materials of the
context — rather than the full assumption stack.

Nozarashi 野晒 — split the goal. Sun-Bleached. Cuts the goal into smaller goals when its shape
allows: a conjunction splits into both conjuncts, a disjunction into a side-choice, an implication or iff
splits via logic-arrow rules, and a roster subset goal splits into per-element memberships. A weather-
worn cleaver that hews the goal’s grain in two.

Sakanade 逆 撫 and Sakashima Yokoshima Happōfusagari 逆 様 邪 八 方 塞 が り — stroke
against the grain. Reverse-Stroke; Backwards-and-Crooked Eight-Direction-Sealed. Both reverse
rather than approach head-on. Sakanade is the ambush form: when a fresh hypothesis arrives, gen-
erate its reversed/contrapositive form as a new hypothesis. Sakashima Yokoshima Happōfusagari
is the tactic form: reverse the current goal into an equivalent reversed shape, prove the reversed shape,
and wrap the result in a Sakanade hypothesis construction. The longest name in the source tree evokes
the complete inversion — the goal turned about, every direction sealed off.

Benihime 紅姫 — extensible simp-style normalisation. Crimson Princess. On a fresh hypoth-
esis, Benihime applies a simp-style rule database to rewrite it into a canonical normal form before it
enters the hypothesis stack. The matching tactic Benihime serves as the gateway through which the
simp pass is invoked — a multifaceted entry point, extensible across many small refining disciplines.

Kage Bunshin no Jutsu 影分身の術 — unchecked-rule escape hatch. Shadow-Clone Tech-
nique. A hypothesis-side ambush that applies a rule Visored does not internally re-check but trusts a
downstream macro to re-verify, decohering a superposed proposition into a single concrete component.
The genuine consequence is kept; the clones are discarded.

The Kurapika クラピカ family — graph algorithms over chains. Named after an analytical
chain-master. Kurapika Chain uses graph algorithms to congregate sub-chains and prove a chain-
separated goal end-to-end. Kurapika Link proves individual links by saturating the hypothesis stash
and bridging gaps with transitivity. Kurapika Substitute reforges expressions by substituting along
active arrows in the chain graph. The Kurapika ambush splits a non-trivial chain into left and right
halves and stashes both for the others to assemble.


F     Transpilation
This appendix describes how an accepted Visored proof is re-expressed as Lean source: the interme-
diate representation, the two emission schemes, the coercion bookkeeping that drives the file size, the
discharge-primitive heuristic, and the supporting Lean library. The high-level picture is that transpila-
tion is a separate stage from elaboration and proof search, and the design choices here are independent
of Visored’s correctness as a checker.

F.1    UVL MIR: a target-neutral IR
Visored does not emit Lean directly. An accepted proof is first lowered into UVL MIR, a target-neutral
intermediate from which a target-specific formatter emits source text. The UVL representation carries
each derivation step as an abstract operation together with the types and witnesses it needs; the Lean
formatter realises each step as a Lean term or tactic call. The benefit of this split is that adding a new
prover target (Rocq, Isabelle, …) is a new formatter on top of UVL rather than a rewrite of elaboration.
In principle the diﬀiculty of transpiling to Rocq or Isabelle is comparable to transpiling to Lean: the
same coercion bookkeeping, the same discharge-primitive heuristic, and the same supporting-library
cost would reappear on each new target. Only the Lean target has been implemented so far. The cost


                                                   24
of the split is that the UVL layer carries information that no single target needs in its entirety, so the
formatter has to make small choices at each step about what to materialise and what to leave implicit.

F.2     Sparse versus dense emission
There are two emission schemes with opposite trade-offs.
    The sparse scheme, which is the current default, realises each Visored derivation step as its own
private lemma, with the step’s inputs and outputs spelled out explicitly. Every step is independently
re-checkable by Lean and a diagnostic can point at the exact failing lemma; the cost is the file-size
figures discussed below.
    The dense scheme bundles a contiguous run of steps inside a single by … tactic block. The emitted
source is much more compact and Lean compiles it faster, but the per-step diagnostic channel collapses
to whatever Lean reports for the block as a whole.
    We currently default to sparse; the choice is a debuggability-versus-size trade-off rather than a
permanent design commitment.

F.3     Replaying the normalisation history
The largest single contributor to emitted size is the cost of replaying Visored’s expression normalisation
system (Section E.6). On the Visored side normalisation is cheap: a single fixed-point pass reduces
every accepted expression to a canonical form, and the rule databases match against canonical shapes.
Lean has no comparable normaliser available to call back into — ring_nf and field_nf are weaker
because they cannot use the well-definedness facts the Visored elaborator has already discharged —
so when the emitter has to express “Visored normalised these two expressions to the same canonical
form”, it has to spell out the normalisation history one primitive rewrite at a time. Each rewrite
becomes its own named Lean lemma; the emitted file is essentially an interpreter trace of the Visored
normaliser running on the input. This single phenomenon is the root cause of the line-count ratios
reported below. Section F.8 below shows a small slice of an actual emitted file.2

F.4     Coercion bookkeeping
The secondary contributor is coercion bookkeeping between number systems. Visored expressions are
typed bottom-up at the least type the construction naturally lives in (Appendix C); Lean elaborates
top-down and inserts coercions at unification-driven positions. The two views are reconciled in two
places.
   On the Lean side, the pull_cast_rewrite pass rewrites ML-style Lean expressions into the
bottom-up canonical form before any Visored-derived lemma is applied.
   On the emission side, every Visored derivation kind that crosses numeric types (N ↔ Z ↔ Q ↔
R ↔ C) is realised as a generic lemma that takes explicit coercion-witness arguments at the call site —
witnesses like nat_int_int_coercion_triangle or num_eq_nat_to_int_coercion, each pinning
down one piece of the cast tower. This is correct and uniform across number-system combinations,
but it compounds with the per-rewrite emission of the normaliser trace: every replayed normalisation
step that crosses a numeric-type boundary additionally carries its own packet of coercion witnesses.

F.5     Discharge primitives, stock and custom
For sub-goals that are not pure-symbolic — numeric inequalities, ring identities, polynomial equa-
tions, modular and divisibility constraints, small finite-case verifications — the emitter routes to a
discharge primitive. Some primitives are stock Lean / Mathlib tactics (norm_num, ring, decide,
native_decide, simp). For shapes that the stock primitives do not handle well, Visored introduces its
own Lean tactics: a custom cutsat1dx tactic for integer linear arithmetic with explicit cut certificates,
a polynomial-equation tactic for Hyōrinmaru-side derivations, and a strengthened norm_num_extra
for numeric comparisons the standard norm_num times out on. Choosing among these is a heuristic
on the emitter side: pick the lightest primitive observed to close this shape of goal. Wrong choices
typically produce a Lean file that still type-checks but takes an order of magnitude longer for lake
   2 Representative emitted-Lean excerpts—the first chunks of one accepted proof per miniF2F subject, each annotated

with the full emission size—are available at https://github.com/xiyuzhai-husky-lang/visored.


                                                        25
build to verify, or one that fails with a diagnostic far from the underlying mistake. Improving the
heuristic is one of the smaller but high-impact items on the transpilation roadmap.

F.6    The Visored Lean library
Emitted Lean source calls into a supporting Lean library of pre-proved lemmas, named tactics, and
macros. The current snapshot contains roughly 3,600 theorems and lemmas across about 280 files and
46,000 lines, plus roughly 170 custom tactic / syntax / macro declarations. The bulk breaks down
approximately as:
• ∼ 1,030 derivation-side lemmas — the per-rewrite primitives the normaliser-trace emitter calls into;
• ∼ 1,130 tactic-side lemmas, including the custom cutsat1dx, polynomial-equation, and norm_num_extra
   machinery;
• ∼ 660 coercion lemmas — the witness tower across N ↔ Z ↔ Q ↔ R ↔ C;
• ∼ 370 ambush-side lemmas;
• the remainder split among hypothesis manipulation, foundations, and prelude.
    A large fraction of these proofs were obtained by a deliberately simple pipeline: the Visored side
emits each needed Lean theorem with a sorry body, and Claude / Codex then fills in the sorrys with
actual proofs that lake build accepts. There is no clever search loop on top — the LLM is given the
theorem statement and asked to prove it, one lemma at a time. This is one of the load-bearing payoffs
of building the system at all. Each Visored CNL construct stands on top of many Lean-side proofs, but
those proofs are written once and shared across every accepted CNL example that uses the construct.
From the user’s perspective, the Visored surface is strictly higher-level than the corresponding Lean
surface — the cost paid once inside the library is what makes the upstream CNL succinct, even though
every accepted proof still bottoms out at the Lean kernel.
    Every new Visored derivation kind requires both an emitter case and a corresponding Lean-side
proof in this library, which is the main reason expanding Visored’s surface vocabulary remains a
two-sided engineering cost.

F.7    Verbosity in practice
The sparse scheme produces large files. On the miniF2F-valid set (244 problems, 32 emitting non-
trivial Lean in the current snapshot), per-problem line-count ratios are heavy-tailed: median ≈ 250×,
mean ≈ 1,170×, ranging from ∼ 5× on the smallest accepted proofs up to ∼ 24,800× on the largest
(a 6-line CNL input expanded to a 148,889-line Lean file containing 37,416 named lemmas). The
bulk ratio across all measured emissions is ∼ 1,100×; the mean emitted file contains roughly 2,000
named lemmas, and several typical files sit near 700 named lemmas each. This is the cost of the sparse
scheme’s per-step explicitness, and it is the headline reason a denser emission scheme is in progress.

F.8    Example slices of transpilation
To make the per-rewrite shape concrete, the snippets below are drawn directly from emitted Lean
files on miniF2F-valid. We show four flavours of lemma that recur throughout every emission: a
basic derivation step with the full coercion-witness packet, a commutative-ring rewrite, a numeric
discharge through Visored’s custom norm_num_extra, and a library-rule application that surfaces a
named Visored tactic (Senbonzakura, in this case) directly in the emitted Lean.

Basic derivation
          √        with coercion witnesses. From a problem whose CNL goal is the one-liner
3! · (23 + 9)/2 = 33 (Visored accepts it and emits 318 named lemmas):


      /-- `9 + -0 = 9` by `derivation.term.add_eq`. -/
      private lemma h1d5
       : (((9:ℕ) : ℤ) + (-((0:ℕ) : ℤ) : ℤ) : ℤ) = (9:ℕ)
       := Visored.Library.Derivation.Term.add_eq ℕ ℤ ℤ ℕ h1d2 h1d3 h1d4
           num_eq_nat_to_int_coercion nat_nat_int_coercion_triangle
           num_eq_identity_coercion nat_int_int_coercion_triangle
           num_eq_nat_to_int_coercion nat_nat_int_coercion_triangle
           comm_ring_add_nat_to_int_coercion nat_nat_int_coercion_triangle
           nat_nat_int_coercion_triangle



                                                  26
The conclusion is the trivial fact 9 + (−0) = 9, but the body carries a packet of nine coercion witnesses
pinning down every leg of the N → Z cast tower.

Commutative-ring rewrite.         A multiplication-side reforge in the same family, applied to a real-
valued expression:


     private lemma h3d5 (b : ℝ)
      : ((((4:ℕ) : ℝ) : ℝ) * (b ^ (2:ℕ) : ℝ) : ℝ) = (((4:ℕ) : ℝ) * (b ^ (2:ℕ) : ℝ) : ℝ)
      := Visored.Library.Derivation.ExprReforge.comm_ring_mul_reforge ℝ ℝ ℝ
          h3d3 (h3d4 b)
          num_eq_identity_coercion num_eq_identity_coercion
          nat_real_real_coercion_triangle real_real_real_coercion_triangle
          comm_ring_mul_identity_coercion
          nat_real_real_coercion_triangle real_real_real_coercion_triangle



Numeric discharge through Visored’s norm_num_extra. When a sub-goal reduces to a compar-
ison the stock norm_num cannot close, the emitter falls back to Visored’s custom norm_num_extra:


     /-- `9 ≥ 0 ↔ True` by `derivation.term.trivially_true_num_comparison`. -/
     private lemma h1d8 : (9:ℕ) ≥ (0:ℕ) ↔ True :=
      Visored.Library.Derivation.Term.trivially_true_num_comparison h1d7
        (by norm_num_extra)



A named Visored tactic surfacing in emitted Lean. The Visored-side dispatch machinery shows
up in the emitted code as library calls into the corresponding tactic namespace. For example, the Sen-
bonzakura library rule squared_pos_if_base_nonzero is invoked directly inside an apply_exact_rule:


     private lemma h2 (b : ℝ) (h0 : b > 0) : (b ^ (2:ℕ) : ℝ) > ((0:ℕ) : ℝ) :=
      Visored.Library.Derivation.ApplyRule.apply_exact_rule
        (Visored.Library.Tactics.Senbonzakura.«prop:squared_pos_if_base_nonzero» b h0)
        (h2d0 b)


A Tekken-Tachikaze-side rule appears in the same shape:


     private lemma h_ne : p ≠ ((0:ℕ) : ℤ) :=
      Visored.Library.Tactics.TekkenTachikaze.ne_if_gt ℤ h4


    These four shapes — elementary derivation, commutative-ring rewrite, custom numeric discharge,
and named-tactic library application — account for almost every line of a typical emitted file. The
shape is straightforward; what makes the line counts heavy is that each rewrite step in the normaliser’s
history produces one such lemma, and a goal of even modest complexity replays many hundreds of
them.

State of the transpilation system. The current transpilation layer is not yet clean. The sparse
emission scheme, the per-operator coercion-witness packets, the discharge-primitive heuristic, the sup-
porting Lean library, and the interaction between them have all evolved incrementally; they are not
yet organised in a way we would call clean. A simplification pass is in progress, with the primary
targets being denser emission (fewer named lemmas per Visored step), a smaller and more uniform
coercion-witness surface, and a re-organisation of the supporting library along the same lines as the
elaborator-side classification. We expect the published numbers to improve substantially over the next
iteration of the system, and the design described in this appendix to be the last verbose generation
rather than the steady state.




                                                   27
G         The Visored Agent Skill
This appendix reproduces, verbatim, the skill given to the LLM coding agent in the experiment of
Section 6: the top-level SKILLS.md in full, followed by a representative subfile from each of the skill’s
three documentation categories (tactics, syntax, workarounds).

SKILLS.md.
---
name: visored-prover
description: Prove math theorems using the Visored controlled natural language theorem prover. Use when working with .tex files containing \begin{example}...\end{
       example} blocks with math proofs.
---

# Visored Theorem Prover

Visored is a controlled natural language theorem prover. You extend problem prefixes to form complete proofs.

## Workflow

1. **Read the problem** from a `.tex` file (the prefix inside `\begin{example}...\end{example}`)
2. **Think through the proof** in natural language first
3. **Extend the prefix** with proof statements
4. **Verify** by running: `visored-core-cli <file_path> --specs-dir <specs_dir>`
5. **If error**, parse the error message and fix the text
6. **Repeat** until SUCCESS

## Harder Problems

For harder problems:

1. **Solve in natural language first** - Write out the complete proof in plain English/math before attempting CNL
2. **Convert to CNL** - Only after you have a working natural language proof, translate it step by step
3. **If you can't solve it in natural language** - That's YOUR problem, not visored's. Don't blame the prover for your inability to find the proof.

This ensures you distinguish between:
- **Your failure**: Can't find the proof strategy
- **Visored limitation**: Found the proof but visored can't verify a specific step

## Verification Command

**IMPORTANT: Always use `cargo run`, NOT the pre-built binary!**

```bash
# ALWAYS use this form:
cargo run --bin visored-core-cli -- <path_to_tex_file> --specs-dir /home/xiyuzhai/repos/husky2/specs --output-style llm

# Syntax check only (faster):
cargo run --bin visored-core-cli -- <path_to_tex_file> --specs-dir /home/xiyuzhai/repos/husky2/specs --stages syntax_only
```

**NEVER use the pre-built binary directly!**

- SUCCESS → proof is valid
- FAILED → fix the error shown and retry

## Error Format

Errors mark the exact location with `【】` brackets:
```
ERROR: missing embedded math right delimiter
Line 3: We have 【$】\left(...\right) = 36.
```

---

# Language Reference

## Formatting

One sentence per line, separated by blank lines:

```latex
Let $x\in\mathbb{R}$.

Assume $x > 0$.

The goal is to prove $x^2 > 0$.

We have $x^2 > 0$.
```

## Basic Constructs

| Construct | Example | Description |
|-----------|---------|-------------|
| Variable introduction | `Let $x \in \mathbb{R}$.` | Introduce a variable |
| Variable definition | `Let $x = 5$.` | Define a variable with value |
| Assumption | `Assume $x > 0$.` | Add an assumption |
| Goal statement | `The goal is to prove $x^2 \geq 0$.` | State what to prove |
| Assertion | `We have $x^2 \geq 0$.` | Assert a fact (auto-proved) |
| Conclusion | `Then $x^2 \geq 0$.` | Conclude from previous steps |
| Divisibility | `Then $a \mid b$.` | Assert a divides b |
| Divisor count | `$\numberOfDivisors{n}$` | Number of divisors of n (renders as τ(n)) |
| Informal comment | `\informal{explanation}` | Add readable comment (ignored by prover) |

## Universal Instantiation

When you have `∀x, p(x)` and want to prove `q(x_0)` where it follows from `p(x_0)`, **explicitly state `p(x_0)` first!**

```latex
% Given: ∀n∈ℕ, a(n+2) = a(n)·a(n+1)/(2a(n)-a(n+1))
% Want to use it for n=1

% WRONG - trying to use consequence directly:
We have $a(3) = \frac{3}{11}$. % Fails! Visored doesn't auto-instantiate




                                                                                28
% RIGHT - explicitly instantiate first:
We have $a(3) = \frac{a(1)\cdot a(2)}{2a(1)-a(2)}$. % Instantiate ∀ with n=1
We have $a(3) = \frac{3}{11}$. % Now compute the value
```

**Don't be lazy!** Always explicitly write out the instantiation before using its consequences.

## Bounded Variable Introduction

To prove a universal statement `∀k, P(k) → Q(k)`, use the "Let such that" pattern:

```latex
Let $k \in \mathbb{Z}$ such that $1 \le k \le n$.

<prove property for k>

Then $\forall k \in \mathbb{Z},\, 1 \le k \le n \implies <property>$.
```

Key points:
- `Let $k \in S$ such that <condition>` introduces k with the bound attached
- Prove the property for that generic k
- `Then $\forall k \in S,\, <condition> \implies <property>$` generalizes

**IMPORTANT:** This pattern works inside case branches where `Let`+`Assume` would fail.

## Chaining

Use chaining `A = B ≤ C` to improve readability and help Visored reasoning:

```latex
% Instead of separate steps:
We have $\sum_{k=1}^{10} f(k) = \sum_{k=1}^{5} f(k) + \sum_{k=6}^{10} f(k)$.
Then $\sum_{k=1}^{10} f(k) = 10 + \sum_{k=6}^{10} f(k)$.
Then $\sum_{k=1}^{10} f(k) \leq 10 + 20$.

% Use chaining:
Then $\sum_{k=1}^{10} f(k) = \sum_{k=1}^{5} f(k) + \sum_{k=6}^{10} f(k) \leq 10 + 20$.
```

Chaining works with `=`, `<`, `≤`, `>`, `≥` in any combination.

**For inequalities with variable bounds:** Break into steps - one for substitution, one for simplification:
```latex
% Instead of: Then $(n-1) \cdot n \cdot (n+1) \ge 990$.
% Use chaining with explicit substitution:
Then $(n-1) \cdot n \cdot (n+1) \ge (10-1) \cdot 10 \cdot (10+1) = 990$.
```

**For complex sums/products:** When substitution fails on nontrivial sum expressions, use chaining to combine the steps into one statement.

## Disjunction Elimination

When you have `P ∨ Q` and want to derive a result, use case analysis:

```latex
Assume $a = 2 \lor b = 2$.
Assume $a \neq 2$.
The goal is to prove $b = 2$.
We prove $b = 2$ by working through different cases :
\begin{itemize}
   \item Case $a = 2$. Contradiction.
   \item Case $b = 2$. Then $b = 2$.
\end{itemize}
```

Key: Use `Contradiction.` when a case is impossible given other assumptions.

**For factored equations:** When you have `(A)(B) = 0`, use case analysis on `A = 0 ∨ B = 0`:

```latex
Then $(2a + 1)(a - 1) = 0$.
Then $2a + 1 = 0 \lor a - 1 = 0$.
We prove $a = 1$ by working through different cases :
\begin{itemize}
   \item Case $2a + 1 = 0$. Then $a = -\frac{1}{2}$. Then $a < 0$. We have $a > 0$. Contradiction.
   \item Case $a - 1 = 0$. Then $a = 1$.
\end{itemize}
```

Use contradiction to eliminate impossible cases based on other constraints (e.g., `a > 0`).

**IMPORTANT:** Always use `Contradiction.` instead of `Then $\mathsf{False}$.` The contradiction must be explicit in the proof - write out the conflicting
       statements (e.g., `We have $n \ge 55$. We have $n < 55$.`) before `Contradiction.`

## Induction

Use `We prove $P(n)$ by induction on $n$ :` with `\begin{itemize}` cases. See `docs/tactics/induction.md`.

**IMPORTANT: Induction must start from 0.** If you need to prove something for `n ≥ k` where `k > 0`, use a substitution:

```latex
% If you need to prove P(n) for n ≥ 1:
Let $m \in \mathbb{N}$.
We prove $P(m+1)$ by induction on $m$ : % Now m starts from 0
\begin{itemize}
   \item Case $m = 0$. ... prove P(1) ...
   \item Case $m \ge 0$. Assume $P(m+1)$. ... prove P((m+1)+1) ...
\end{itemize}
```

This transforms `n = m + 1` so that when `m = 0, 1, 2, ...`, we get `n = 1, 2, 3, ...`

## Claim `∈ ℕ` Before Using Quotients in Auto Rules

**IMPORTANT:** When using a quotient like `n/k` in auto rules (e.g., `dvd-gcd-if-dvd-both`), you must first establish that `n/k ∈ ℕ`. Otherwise the auto rule
       matching will fail silently.

```latex
% WRONG - auto rule can't match n/5 without knowing it's in ℕ:
Assume $5 \mid n$.
Assume $n / 5 \mid 3628800$.




                                                                                29
Assume $n / 5 \mid n$.
Then $n / 5 \mid \gcd(3628800, n)$. % FAILS

% RIGHT - claim n/5 ∈ ℕ first:
Assume $5 \mid n$.
Then $n / 5 \in \mathbb{N}$.
Then $n / 5 \mid 3628800$.
Then $n / 5 \mid n$.
Then $n / 5 \mid \gcd(3628800, n)$. % WORKS
```

## Comma Precedence in Set Builder

**IMPORTANT:** `,` has higher precedence than `\mid` (divisibility), but `,\,` has lower precedence.

If you get a `todo!()` panic at `decohere`, it may be because you used `,` instead of `,\,` between propositions in set builder notation.

```latex
% WRONG - comma has higher precedence than \mid, causes parse error:
\{n \in \mathbb{N} \mid 3000 \mid n, n \mid 18144000\}

% RIGHT - use ,\, which has lower precedence:
\{n \in \mathbb{N} \mid 3000 \mid n,\, n \mid 18144000\}
```

## Conjunction in Universal Bodies

**IMPORTANT:** Within the body of `\forall`, use `\land` (not `,\,`) to conjoin conditions. Using `,\,` causes conditional well-definedness to fail — guards won't
       propagate to later terms.

```latex
% WRONG - guards don't propagate for well-definedness:
\forall n\in\mathbb{N},\, t(n)\neq 0,\, \frac{1}{25t(n)}=1

% RIGHT - \land lets guards propagate:
\forall n\in\mathbb{N},\, t(n)\neq 0 \land \frac{1}{25t(n)}=1
```

The first `,\,` after the quantifier domain (`\forall n\in\mathbb{N},\,`) is fine — it separates the binding from the body. But within the body itself, use `\land
       `.

## Syntax Rules

**IMPORTANT: `$...$` must enclose a complete syntax tree.** Never break math expressions across boundaries.

**Trigonometric function powers:** e.g., use `{(\sin x)}^n` instead of `\sin^n x`.

```latex
% WRONG - breaks syntax tree:
We have $a = 4 \rightarrow a$ is prime.

% RIGHT - complete expression:
We have $4$ is prime. % separate statement
```

**Avoid excessive implications.** Write conclusions directly. Use case analysis with `Contradiction.` instead of chaining implications.

## Linear Systems

**Visored does NOT solve linear systems automatically.** Use Gaussian elimination externally (e.g., Python) to find coefficients.

For a system of n equations, find a linear combination that yields the target expression:

```python
from fractions import Fraction
# Solve for coefficients c1, c2, ... such that
# c1*eq1 + c2*eq2 + ... = target_expression
# Use Gaussian elimination with exact Fraction arithmetic
```

Then write the proof showing the linear combination equals the target:

```latex
We have $c_1 \cdot (\text{eq1}) + c_2 \cdot (\text{eq2}) + \ldots = x^2 + y^2$.

We have $c_1 + c_2 + \ldots = 36$.

Then $x^2 + y^2 = 36$.
```

See `solutions/solution75.tex` for a complete example (AIME 1984 P15).

---

# Tactics Reference

See `docs/tactics/` for detailed tactics:

- `case_analysis.md` - Case analysis and contradiction
- `floor.md` - Floor function (Hermite's identity)
- `induction.md` - Induction proofs
- `modular.md` - Modular arithmetic (prefer `\pmod` for derivations, see below)
- `set.md` - Set minimality, forall statements, set equality

## Modular Arithmetic Pattern

**In derivations, prefer `\pmod` (congruence) over `\bmod` (remainder).**

When a problem uses `\bmod` syntax, derive using `\pmod` then convert back:

```latex
% Given: m \bmod 2 = 1
% Want to derive: (m+1) \bmod 2 = 0

% Step 1: Convert to pmod
We have $m \equiv 1 \pmod{2}$.

% Step 2: Derive using pmod (this is what Visored can do)
Then $m+1 \equiv 0 \pmod{2}$.

% Step 3: Convert back to bmod
Then $(m+1) \bmod 2 = 0$.




                                                                                  30
```

---

# Directory Structure

```
valid/
├── SKILLS.md # This file
├── progress.json # Tracks solved/stuck problems
├── docs/
│ ├── tactics/ # Proof tactics (case analysis, sets, etc.)
│ ├── syntax/ # Correct LaTeX syntax rules
│ └── workarounds/ # Current limitations needing manual handling
├── scripts/
│ └── update_progress.py # Progress tracking script
├── problems/ # Problem prefixes
└── solutions/ # Completed proofs
```

## When Stuck

1. Check `docs/tactics/` for proof strategies
2. Check `docs/syntax/` for LaTeX syntax rules
3. Check `docs/workarounds/` for known limitations
4. If new issue, report to maintainer and document

## Reference Examples

- `test-data/visored/elaborator/` - Extensive examples
 - `main/props/` - Basic propositions
 - `minif2f/valid/` - Competition math problems
 - `tactics/` - Various proof tactics




docs/tactics/set.md.
# Set Tactics

## Set Minimality (Smallest Element)

To prove `$x$ is the smallest element of $S$`:

1. Prove `$x \in S$`
2. Prove `$\forall y \in S,\, x \le y$`

### Example

```latex
Let $S\subseteq\mathbb{Q}$.
Let $x\in\mathbb{R}$.
Assume $x\in S$.
Assume $\forall y\in S,\,x\le y$.
Then $x$ is the smallest element of $S$.
```

## Second Smallest Element

To prove `$x_2$ is the second smallest element of $S$`:

1. Prove `$x_1 \in S$`
2. Prove `$x_1$ is the smallest element of $S$`
3. Prove `$x_2 \in S$`
4. Prove `$\forall y \in S,\, x_1 < y \rightarrow x_2 \le y$`

### Example

```latex
Let $S\subseteq\mathbb{Q}$.
Let $x_1, x_2\in\mathbb{R}$.
Assume $x_1\in S$.
Assume $x_1$ is the smallest element of $S$.
Assume $x_2\in S$.
Assume $\forall y\in S,\,x_1 < y \rightarrow x_2\le y$.
Then $x_2$ is the second smallest element of $S$.
```

Reference: `test-data/visored/elaborator/tactics/tekken_tachikaze/main.tex`

## Proving Forall Statements

To prove `$\forall y \in S,\, P(y)$` (where S must be nonempty):

```latex
Let $y \in S$.

... (proof steps) ...

Then $P(y)$.

Then $\forall y \in S,\, P(y)$.
```

To prove `$\forall y \in S,\, Q(y) \rightarrow P(y)$` (forall with implication):

```latex
Let $y \in S$ such that $Q(y)$.

... (proof steps) ...

Then $P(y)$.

Then $\forall y \in S,\, Q(y) \rightarrow P(y)$.
```

Use `Let $y \in S$ such that $Q(y)$` to introduce an element with an additional condition.

## Set Equality via Predicate Equivalence




                                                                                   31
To prove `{n ∈ S | P(n)} = {n ∈ S | Q(n)}`, first prove `∀n ∈ S, P(n) ↔ Q(n)`, then conclude set equality.

```latex
% Want: S = {n ∈ ℕ | Q(n)} where S = {n ∈ ℕ | P(n)}
Let $n \in \mathbb{N}$.

... (prove P(n) ↔ Q(n)) ...

Then $\forall n \in \mathbb{N},\, P(n) \iff Q(n)$.

Then $S = \{n \in \mathbb{N} \mid Q(n)\}$.
```

## Set Equality with Roster (Enumerated Set)

To prove $S = \{a, b, ...\}$ or $|S| = n$:

1. **Show each element is in S** (forward direction)
2. **Show all elements of S satisfy a characterization** (backward direction)
3. **Conclude the iff characterization**
4. **Derive set equality and cardinality**

```latex
% Show 1 ∈ S, 2 ∈ S
Then $1 \in S$.
Then $2 \in S$.

% Show ∀x ∈ S, x = 1 ∨ x = 2
Let $x \in S$.
Then ... (derive bounds on x)
We have $x \in \mathbb{N}$.
We have $x > 0$.
We have $x < 3$.
Then $x = 1 \lor x = 2$.

% Conclude
Then $\forall x \in S,\, x = 1 \lor x = 2$.
Then $\forall x \in \mathbb{N},\, x \in S \iff x = 1 \lor x = 2$.
Then $S = \{1, 2\}$.
Then $|S| = 2$.
```




docs/tactics/induction.md.
# Induction

For proving `∀n∈ℕ, P(n)` by induction:

```latex
We prove $\forall n\in\mathbb{N},\, P(n)$ by induction on $n$ :

\begin{itemize}

\item Case $n=0$.

<proof that P(0) holds>

\item Case $n \ge 0$.

Assume $P(n)$.

The goal is to prove $P(n+1)$.

<proof using inductive hypothesis>

\end{itemize}
```

## Example: Prove 3 | n³+2n

```latex
We prove $3\mid n^3+2n$ by induction on $n$ :

\begin{itemize}

\item Case $n=0$.

We have $3\mid 0$.

\item Case $n \ge 0$.

Assume $3\mid n^3+2n$.

The goal is to prove $3\mid {(n+1)}^3+2(n+1)$.

We have ${(n+1)}^3+2(n+1) = (n^3+2n) + 3(n^2+n+1)$.

We have $3\mid n^3+2n$.

We have $3\mid 3(n^2+n+1)$.

Then $3\mid {(n+1)}^3+2(n+1)$.

\end{itemize}
```

See `test-data/visored/core/lean4-ok/minif2f-maiden-voyage/los_lobos000193.tex` for more examples.




docs/syntax/exponent-with-parentheses.md.
# Exponent with Parenthesized Base

When raising a parenthesized expression to a power, wrap in braces.

## Error




                                                                                32
```
ERROR: right delimiter as base
```

## Wrong

```latex
$(x+3)^2$
$a(x+3)^2$
```

## Correct

```latex
${(x+3)}^2$
$a{(x+3)}^2$
```

## Why

LaTeX parsing requires braces to group the base when it ends with a delimiter like `)`.




docs/workarounds/quantified-equality-transitivity.md.
# Quantified Equality Transitivity

Visored doesn't auto-chain transitivity for quantified equalities.

## Symptom

```
ERROR: Unable to prove: \(\forall x, A = C\)
```

When you have `∀x, A = B` and `∀x, B = C` established.

## Note

**Non-quantified** equalities work automatically:
- `A = B`, `B = C` → visored derives `A = C`

**Quantified** equalities need explicit steps:
- `∀x, A = B`, `∀x, B = C` → must explicitly state `∀x, A = C`

## Fix

State each transitivity step explicitly:

```latex
We have $\forall x, A = B$.
We have $\forall x, B = C$.
We have $\forall x, A = C$. % explicit transitivity step
We have $\forall x, C = D$.
We have $\forall x, A = D$. % another explicit step
```

## Example (Problem 10)

```latex
We have $\forall x \in \mathbb{R},\,3x^2+7x+4 = a{(x+3)}^2 + b(x+3) + c$.
We have $\forall x \in \mathbb{R},\,a{(x+3)}^2 + b(x+3) + c = ax^2 + 6ax + 9a + bx + 3b + c$.
We have $\forall x \in \mathbb{R},\,3x^2+7x+4 = ax^2 + 6ax + 9a + bx + 3b + c$.
```




H          Additional Worked Examples
The examples in this appendix are paired Visored CNL / Lean 4 artifacts maintained alongside this
paper’s source. The CNL on the left is the exact text the Visored elaborator accepts; the Lean on
the right is a hand-written Lean 4 proof of the same statement. A Makefile re-runs both checks. All
examples are drawn from miniF2F. Within each subject category, examples are ordered roughly easy
to hard.




                                                                                33
H.1      Algebra
Visored CNL input (typeset)                                     Hand-written Lean 4 proof

Example 4. Let x ∈ R.
Let y ∈ R.                                                      import Mathlib
Assume x > 0.
Assume y > 0.                                                   namespace VisoredPaperExamples.Ex03
Assume y 3 = 1.                                                 example (x y : ℝ)
Assume 6x2 = 2(6y 2 ).     √                                       (hxp : x > 0) (hyp : y > 0)
The goal is to prove x3 = 2 2.
Then y = 1.                                                        (hy3 : y^3 = 1) (hxy : 6 * x^2 = 2 * (6 * y^2))
Then x2 =√2.                                                            :
Then x = 2.  √                                                     x^3 = 2 * Real.sqrt 2 := by
Then x3 = 2 2.                                                   have hy : y = 1 := by
                                                                   have h1 : (y - 1) * (y^2 + y + 1) = 0 := by
                                                                        nlinarith
                                                                   have h2 : y^2 + y + 1 > 0 := by nlinarith [
                                                                        sq_nonneg y]
                                                                   rcases mul_eq_zero.mp h1 with h | h
                                                                   ·linarith
                                                                   ·linarith
                                                                 have hx2 : x^2 = 2 := by rw [hy] at hxy; linarith
                                                                 have hsq2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (
                                                                       by norm_num : (0:ℝ) ≤ 2)
                                                                 have hs_nn : (0:ℝ) ≤ Real.sqrt 2 := Real.
                                                                       sqrt_nonneg _
                                                                 have hx_eq : x = Real.sqrt 2 := by
                                                                   nlinarith [sq_nonneg (x - Real.sqrt 2), hx2,
                                                                        hsq2]
                                                                 rw [hx_eq]
                                                                 have hcube : (Real.sqrt 2 : ℝ)^3 = Real.sqrt 2 ^
                                                                       2 * Real.sqrt 2 := by ring
                                                                 rw [hcube, hsq2]

                                                                end VisoredPaperExamples.Ex03
                                                                            √         √
miniF2F amc12a-2008-p8. A four-step algebraic chain ( y = 1 , x2 = 2, x = 2, x3 = 2 2). The CNL is four
                                                                                                  √
“Then…” lines. The Lean proof factors y 3 − 1 to extract y = 1, uses Real.sq_sqrt to bridge x2 = ( 2)2 , and
                     √ 2 √
expands the cube as ( 2) · 2.

Visored CNL input (typeset)                                     Hand-written Lean 4 proof

Example 5. Let a ∈ R.
                                                                import Mathlib
Let b ∈ R.
Assume ∀x ∈ R, (x ̸= 3∧x ̸= 5) → x2 −8x+15
                                      4x
                                             = x−3a      b
                                                      + x−5 .
                                                                namespace VisoredPaperExamples.Ex05
The goal is to prove a = −6 ∧ b = 10.                           theorem mathd_algebra_13
We have (1 ̸= 3 ∧ 1 ̸= 5) → 1−8+15
                              4        a
                                    = 1−3     b
                                           + 1−5  .                (a b : ℝ)
We have 1 ̸= 3.                                                    (h₀ : ∀ x, (x - 3 ≠ 0 ∧ x - 5 ≠ 0) →
We have 1 ̸= 5.                                                     4 * x / (x^2 - 8 * x + 15) = a / (x - 3) + b / (x -
Then 48 = −2a
              + −4b
                    .                                                     5)) :
Then 2a + b = −2.                                                  a = -6 ∧ b = 10 := by
We have (2 ̸= 3 ∧ 2 ̸= 5) → 4−16+15
                               8         a
                                     = 2−3      b
                                            + 2−5   .            have h1 : 4 * (1 : ℝ) / ((1 : ℝ) ^ 2 - 8 * 1 + 15) = a /
We have 2 ̸= 3.                                                         (1 - 3) + b / (1 - 5) := by
We have 2 ̸= 5.                                                    refine h₀ 1 ⟨?_, ?_⟩ <;> norm_num
Then 38 = −1a
              + −3b
                    .                                            have h2 : 4 * (2 : ℝ) / ((2 : ℝ) ^ 2 - 8 * 2 + 15) = a /
Then 3a + b = −8.                                                       (2 - 3) + b / (2 - 5) := by
Then a = (3a + b) − (2a + b) = −8 − (−2) = −6.                     refine h₀ 2 ⟨?_, ?_⟩ <;> norm_num
Then b = −2 − 2a = −2 − 2 · (−6) = 10.                           have e1 : 2 * a + b = -2 := by
Then a = −6 ∧ b = 10.                                              have hh := h1
                                                                   field_simp at hh
                                                                   ring_nf at hh
                                                                   linarith
                                                                 have e2 : 3 * a + b = -8 := by
                                                                   have hh := h2
                                                                   field_simp at hh
                                                                   ring_nf at hh
                                                                   linarith
                                                                 exact ⟨by linarith, by linarith⟩

                                                                end VisoredPaperExamples.Ex05

miniF2F mathd-algebra-13. Partial fractions: instantiate the universal hypothesis at x = 1 and x = 2, solve
the resulting 2 × 2 linear system. The Lean writer must specialize h, discharge the inequality side conditions


                                                                34
(norm_num), clear denominators with field_simp; ring_nf, and close with linarith.


H.2      Number theory

Visored CNL input (typeset)                                 Hand-written Lean 4 proof

Example 6. The goal is to prove gcd(20!, 200000) = 40000.
We have gcd(20!, 200000) = 40000.                           import Mathlib

                                                            namespace VisoredPaperExamples.Ex02
                                                            example : Nat.gcd (Nat.factorial 20) 200000 = 40000
                                                                  := by
                                                             native_decide

                                                            end VisoredPaperExamples.Ex02

miniF2F mathd-numbertheory-169. One-line CNL discharging a numeric identity gcd(20!, 200000) = 40000.
Lean uses native_decide; the writer must know decide times out at compile time.

Visored CNL input (typeset)                                 Hand-written Lean 4 proof

Example 7. The goal is to prove gcd(180, 168) = 12.
We have gcd(180, 168) = 12.                                 import Mathlib

                                                            namespace VisoredPaperExamples.Ex06
                                                            example : Nat.gcd 180 168 = 12 := by decide

                                                            end VisoredPaperExamples.Ex06

miniF2F mathd-numbertheory-188. Small numeric gcd; decide suﬀices. The Lean writer also has to pick
between decide and native_decide, a choice that depends on how the numeric kernel evaluates the goal and
is therefore an extra Lean-specific decision compared with the CNL version.

Visored CNL input (typeset)                                 Hand-written Lean 4 proof

Example 8. Let m ∈ N.
                                                            import Mathlib
Let x ∈ N.
Assume 10 ≤ m ≤ 99.
Assume (6x) mod m = 1.                                      namespace VisoredPaperExamples.Ex07
Assume (x − 62 ) mod m = 0.                                 theorem mathd_numbertheory_780
The goal is to prove m = 43.                                   (m x : ℤ)
We have x ≡ 36 (mod m).                                        (h₀ : 10 ≤ m)
We have 6x ≡ 6 · 36 (mod m).                                   (h₁ : m ≤ 99)
We have 6x ≡ 1 (mod m).                                        (h₂ : (6 * x) % m = 1)
We have 6 · 36 ≡ 1 (mod m).                                    (h₃ : (x - 6 ^ 2) % m = 0) :
We have 216 ≡ 1 (mod m).                                       m = 43 := by
We have m | 215.                                             have hdvd_x : m ∣ (x - 6 ^ 2) := Int.dvd_of_emod_eq_zero
We prove m = 43 by working through different cases :                h₃
• Case m = 1. Contradiction.
• Case m = 5. Contradiction.                                 have hdvd_6x : m ∣ (6 * x - 1) := by
• Case m = 43.                                                 have hone : (1 : ℤ) % m = 1 :=
   We have m = 43.                                              Int.emod_eq_of_lt (by norm_num) (by linarith)
• Case m = 215. Contradiction.                                 have hmod : (6 * x) ≡ 1 [ZMOD m] := by
                                                                show (6 * x) % m = 1 % m
                                                                rw [h₂, hone]
                                                               have h := Int.modEq_iff_dvd.mp hmod.symm
                                                               exact h
                                                             have hdvd_215 : m ∣ (215 : ℤ) := by
                                                               have h1 : m ∣ 6 * (x - 6 ^ 2) := dvd_mul_of_dvd_right
                                                                    hdvd_x 6
                                                               have h2 : m ∣ (6 * (x - 6 ^ 2) - (6 * x - 1)) :=
                                                                    dvd_sub h1 hdvd_6x
                                                               have heq : 6 * (x - 6 ^ 2) - (6 * x - 1) = (-215 : ℤ)
                                                                    := by ring
                                                               rw [heq] at h2
                                                               rwa [dvd_neg] at h2
                                                             interval_cases m <;> omega

                                                            end VisoredPaperExamples.Ex07

miniF2F mathd-numbertheory-780. Modular arithmetic with case analysis. The CNL stays in N, but Lean’s
truncated subtraction makes the literal N transliteration vacuously false (x - 6^2 = 0 whenever x < 36),



                                                            35
so the Lean writer must know to lift to Z — itself part of the lemma-vocabulary cost. The proof uses
Int.dvd_of_emod_eq_zero, Int.modEq_iff_dvd, and interval_cases.




                                                36
Visored CNL input (typeset)                                Hand-written Lean 4 proof

Example 9. Let a ∈ N.                                      import Mathlib
Let b ∈ N.
Assume 0 < a.                                              namespace VisoredPaperExamples.Ex08
Assume 0 < b.                                              example

Assume 7 ∤ a.                                                 (a b : ℕ)
                                                              (ha : 0 < a) (hb : 0 < b)
Assume 7 ∤ b.                                                 (h₁ : ¬7 ∣ a) (h₂ : ¬7 ∣ b) (h₃ : ¬7 ∣ (a + b))
Assume 7 ∤ (a + b).                                           (h₄ : 7 ^ 7 ∣ (a + b) ^ 7 - a ^ 7 - b ^ 7) :
Assume 77 | ((a + b)7 − a7 − b7 ).                            19 ≤ a + b := by
                                                            have hab_pow_le : a ^ 7 + b ^ 7 ≤ (a + b) ^ 7 := by
The goal is to prove a + b ≥ 19.                              have hexp : (a + b) ^ 7 =
                                                      2
We have (a + b)7 − a7 − b7 = 7ab(a + b)(a2 + ab + b2 ) .         a ^ 7 + b ^ 7 +
                                    2 2                            (7 * a^6 * b + 21 * a^5 * b^2 + 35 * a^4 * b^3 +
We have 7 | 7ab(a + b)(a + ab + b ) .
           7              2
                                                                    35 * a^3 * b^4 + 21 * a^2 * b^5 + 7 * a * b^6) := by ring
                                     2
We have 76 | ab(a + b)(a2 + ab + b2 ) .                       have h_nonneg :
                                                                 0 ≤ 7 * a^6 * b + 21 * a^5 * b^2 + 35 * a^4 * b^3 +
We have 7 ∤ ab.                                                      35 * a^3 * b^4 + 21 * a^2 * b^5 + 7 * a * b^6 := Nat.zero_le _
We have 7 ∤ ab(a + b).                                        omega
                            2
We have 76 | (a2 + ab + b2 ) .                              have h_a7_le : a ^ 7 ≤ (a + b) ^ 7 :=
                                                              (Nat.le_add_right _ _).trans hab_pow_le
We have 73 | a2 + ab + b2 .                                 have h_sub_le : b ^ 7 ≤ (a + b) ^ 7 - a ^ 7 := by omega
We have a ≥ 1.                                              have h_int_sub :
We have b ≥ 1.                                                 (((a + b) ^ 7 - a ^ 7 - b ^ 7 : ℕ) : ℤ)
                                                                 = ((a : ℤ) + b) ^ 7 - (a : ℤ) ^ 7 - (b : ℤ) ^ 7 := by
We have a2 ≥ 1.                                               rw [Nat.cast_sub h_sub_le, Nat.cast_sub h_a7_le]
We have a2 + ab + b2 ≥ 1.                                     push_cast
                                                              ring
We have a2 + ab + b2 ≥ 343.                                 have h₄' :
We have ab ≥ 0.                                                (7 ^ 7 : ℤ) ∣ ((a : ℤ) + b) ^ 7 - (a : ℤ) ^ 7 - (b : ℤ) ^ 7 := by
We have (a + b)2 = a2 + 2ab + b2 .                            have hcast : ((7 ^ 7 : ℕ) : ℤ) ∣ (((a + b) ^ 7 - a ^ 7 - b ^ 7 : ℕ) : ℤ) :=
                                                               Int.natCast_dvd_natCast.mpr h₄
We have (a + b)2 ≥ a2 + ab + b2 .                             rw [h_int_sub] at hcast
We have (a + b)2 ≥ 343.                                       simpa using hcast
                                                            have h_identity :
We have a + b > 0.                                             ((a : ℤ) + b) ^ 7 - (a : ℤ) ^ 7 - (b : ℤ) ^ 7
We have a + b ≥ 19.                                              = 7 * ((a : ℤ) * b * ((a : ℤ) + b) *
                                                                        ((a : ℤ) ^ 2 + (a : ℤ) * b + (b : ℤ) ^ 2) ^ 2) := by ring
                                                            rw [h_identity] at h₄'
                                                            set S : ℤ := (a : ℤ) ^ 2 + (a : ℤ) * b + (b : ℤ) ^ 2 with hS_def
                                                            have h_six : (7 ^ 6 : ℤ) ∣ (a : ℤ) * b * ((a : ℤ) + b) * S ^ 2 := by
                                                              have h7ne : (7 : ℤ) ≠ 0 := by norm_num
                                                              have hpow : (7 ^ 7 : ℤ) = 7 * 7 ^ 6 := by ring
                                                              rw [hpow] at h₄'
                                                              exact (mul_dvd_mul_iff_left h7ne).mp h₄'
                                                            have hp7 : Nat.Prime 7 := by decide
                                                            have h_ab_not : ¬7 ∣ a * b := fun hh =>
                                                              (hp7.dvd_mul.mp hh).elim h₁ h₂
                                                            have h_abab_not_nat : ¬7 ∣ a * b * (a + b) := fun hh =>
                                                              (hp7.dvd_mul.mp hh).elim h_ab_not h₃
                                                            have hp7_int : Prime (7 : ℤ) := by
                                                              have h : Prime ((7 : ℕ) : ℤ) := Nat.prime_iff_prime_int.mp hp7
                                                              simpa using h
                                                            have h_abab_not_int : ¬(7 : ℤ) ∣ (a : ℤ) * b * ((a : ℤ) + b) := by
                                                              intro hh
                                                              apply h_abab_not_nat
                                                              have hcast : ((7 : ℕ) : ℤ) ∣ ((a * b * (a + b) : ℕ) : ℤ) := by
                                                               push_cast
                                                               simpa using hh
                                                              exact Int.natCast_dvd_natCast.mp hcast
                                                            have h_S2 : (7 : ℤ) ^ 6 ∣ S ^ 2 :=
                                                              hp7_int.pow_dvd_of_dvd_mul_left 6 h_abab_not_int h_six
                                                            have h_S : (7 : ℤ) ^ 3 ∣ S := by
                                                              have h_pow_eq : ((7 : ℤ) ^ 3) ^ 2 = (7 : ℤ) ^ 6 := by ring
                                                              have h' : ((7 : ℤ) ^ 3) ^ 2 ∣ S ^ 2 := by rw [h_pow_eq]; exact h_S2
                                                              exact (IsIntegrallyClosed.pow_dvd_pow_iff (n := 2) (by norm_num)).mp h'
                                                            have hS_pos : 0 < S := by
                                                              have ha' : (1 : ℤ) ≤ (a : ℤ) := by exact_mod_cast ha
                                                              have hb' : (1 : ℤ) ≤ (b : ℤ) := by exact_mod_cast hb
                                                              have hsq_a : (1 : ℤ) ≤ (a : ℤ) ^ 2 := by nlinarith
                                                              have hsq_b : (0 : ℤ) ≤ (b : ℤ) ^ 2 := sq_nonneg _
                                                              have hab : (0 : ℤ) ≤ (a : ℤ) * b := by positivity
                                                              have hSeq : S = (a : ℤ) ^ 2 + (a : ℤ) * b + (b : ℤ) ^ 2 := hS_def
                                                              linarith
                                                            have hS_ge : (343 : ℤ) ≤ S := by
                                                              have h343 : (7 : ℤ) ^ 3 = 343 := by norm_num
                                                              rw [h343] at h_S
                                                              obtain ⟨k, hk⟩ := h_S
                                                              have hk_pos : 0 < k := by
                                                               rcases lt_or_ge 0 k with hk' | hk'
                                                               ·exact hk'
                                                               ·exfalso
                                                                 have : S ≤ 0 := by
                                                                   have : (343 : ℤ) * k ≤ 343 * 0 :=
                                                                     mul_le_mul_of_nonneg_left hk' (by norm_num)
                                                                   rw [hk]; simpa using this
                                                                 linarith
                                                              have : (343 : ℤ) * 1 ≤ 343 * k :=
                                                               mul_le_mul_of_nonneg_left hk_pos (by norm_num)
                                                              rw [hk]; linarith
                                                            have h_ab_sq_ge_int : (343 : ℤ) ≤ ((a : ℤ) + b) ^ 2 := by
                                                              have hab : (0 : ℤ) ≤ (a : ℤ) * b := by positivity
                                                              have hEq : ((a : ℤ) + b) ^ 2 = S + (a : ℤ) * b := by
                                                               rw [hS_def]; ring
                                                              linarith
                                                            have h_ab_sq_ge : (343 : ℕ) ≤ (a + b) ^ 2 := by
                                                              have : ((343 : ℕ) : ℤ) ≤ (((a + b) ^ 2 : ℕ) : ℤ) := by
                                                               push_cast
                                                               exact h_ab_sq_ge_int
                                                              exact_mod_cast this
                                                            have h_gt : 342 < (a + b) ^ 2 := by omega
                                                            have h_sqrt_lt : Nat.sqrt 342 < a + b := Nat.sqrt_lt'.mpr h_gt
                                                            have h_sqrt_eq : Nat.sqrt 342 = 18 := by native_decide
                                                            rw [h_sqrt_eq] at h_sqrt_lt
                                                            omega

                                                           end VisoredPaperExamples.Ex08




                                                           37
miniF2F imo-1984-p2. Polynomial identity over Z plus 77 divisibility plus square-root bound. Lean Math-
lib chain: Prime.pow_dvd_of_dvd_mul_left, IsIntegrallyClosed.pow_dvd_pow_iff, Nat.sqrt_lt'. Each
lemma has its own positivity / coprimality side conditions.


H.3      Inequalities

Visored CNL input (typeset)                                      Hand-written Lean 4 proof

Example 10. Let a, b ∈ R.
Assume a > 0.                                                    import Mathlib
Assume b > 0.
The goal is to prove (a + b)4 ≤ 8(a4 + b4 ).                     namespace VisoredPaperExamples.Ex10
We have (a + b)4 = a4 + 4a3 b + 6a2 b2 + 4ab3 + b4 .             example (a b : ℝ)
We have 8(a4 + b4 ) − (a + b)4 = 7a4 − 4a3 b − 6a2 b2 − 4ab3 +
                                                                    (ha : a > 0) (hb : b > 0) :
7b4 .
We have 7a4 − 4a3 b − 6a2 b2 − 4ab3 + 7b4 = (a − b)2 (7a2 +         (a + b)^4 ≤ 8 * (a^4 + b^4) := by
10ab + 7b2 ).                                                     nlinarith [sq_nonneg (a - b), sq_nonneg (a + b),
We have (a − b)2 ≥ 0.                                                      sq_nonneg (a^2 - b^2), sq_nonneg (a^2 + b
We have a2 > 0.                                                                 ^2),
We have b2 > 0.                                                            sq_nonneg a, sq_nonneg b,
We have ab > 0.                                                            mul_pos ha hb, mul_pos (mul_pos ha hb) (
We have 7a2 > 0.
We have 7b2 > 0.                                                                mul_pos ha hb),
We have 10ab > 0.                                                          mul_self_nonneg (a - b), mul_self_nonneg
We have 7a2 + 10ab + 7b2 > 0.                                                   (a + b),
We have (a − b)2 (7a2 + 10ab + 7b2 ) ≥ 0.
                                                                           ha.le, hb.le]
We have 8(a4 + b4 ) − (a + b)4 ≥ 0.
Then (a + b)4 ≤ 8(a4 + b4 ).
                                                                 end VisoredPaperExamples.Ex10

miniF2F algebra-apb4leq8ta4pb4. (a + b)4 ≤ 8(a4 + b4 ). The Lean writer must supply the right sq_nonneg
hints (e.g., sq_nonneg (a − b), sq_nonneg (a2 − b2 )) for nlinarith to close.

Visored CNL input (typeset)                                      Hand-written Lean 4 proof

Example 11. Let x ∈ R.
                                                                 import Mathlib
Assume x > 0.             √
The goal is to prove 2 − 2 ≥ 2 − x − 2x1
                                         .
                   √      √        2                           namespace VisoredPaperExamples.Ex11
We have x + 2x − 2 =
               1
                             x − √2x .
                                  1
                                                                 example (x : ℝ) (hxp : 0 < x) :
         √           2                                            2 - Real.sqrt 2 ≥ 2 - x - 1 / (2 * x) := by
We have      x − √12x    ≥ 0.                                     have hs_nn : (0:ℝ) ≤ Real.sqrt 2 := Real.sqrt_nonneg _
                   √
We have x + 2x 1
                 − 2 ≥ 0.                                         have hsq2 : Real.sqrt 2 ^ 2 = 2 :=
                    √                                               Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)
We have x + 2x 1
                 ≥ 2.
                            √                                     have h2x_pos : (0:ℝ) < 2 * x := by linarith
We have 2 − x − 2x1
                      ≤ 2 − 2.
          √                                                       have hkey : Real.sqrt 2 ≤ x + 1 / (2 * x) := by
Then 2 − 2 ≥ 2 − x − 2x . 1
                                                                    have hmul : (x + 1 / (2 * x) - Real.sqrt 2) * (2 * x) =
                                                                       (x * Real.sqrt 2 - 1) ^ 2 + (Real.sqrt 2 ^ 2 - 2) *
                                                                            x := by
                                                                     have hx_ne : (2 * x) ≠ 0 := ne_of_gt h2x_pos
                                                                     field_simp
                                                                     nlinarith [hsq2, sq_nonneg (x * Real.sqrt 2 - 1)]
                                                                    have hrhs_nn :
                                                                       (x * Real.sqrt 2 - 1) ^ 2 + (Real.sqrt 2 ^ 2 - 2) *
                                                                            x ≥ 0 := by
                                                                     rw [hsq2]
                                                                     nlinarith [sq_nonneg (x * Real.sqrt 2 - 1)]
                                                                    have hprod_nn :
                                                                       (x + 1 / (2 * x) - Real.sqrt 2) * (2 * x) ≥ 0 := by
                                                                     rw [hmul]; exact hrhs_nn
                                                                    nlinarith [hprod_nn, h2x_pos]
                                                                  linarith

                                                                 end VisoredPaperExamples.Ex11

                                                                       √
miniF2F algebra-amgm-faxinrrp2msqrt2geq2mxm1div2x. AM-GM with 2 and 1/(2x) on x > 0. The Lean
                                                √
writer needs Real.sq_sqrt, the hint sq_nonneg (x 2 − 1), and the field_simp; ring bridge to clear 1/(2x).




                                                                 38
H.4     Induction, sums, and products

Visored CNL input (typeset)                              Hand-written Lean 4 proof

Example 12. Let n ∈ N.
                     Pn−1     1         n                import Mathlib
The goal is to prove  k=0 (k+1)(k+2) = n+1 .
We have ∀k ∈ N, (k+1)(k+2)
                     1         1
                           = k+1  − k+2
                                      1
                                          .
        Pn−1                Pn−1  1                    namespace VisoredPaperExamples.Ex12
We have            1
          k=0 (k+1)(k+2)  =   k=0   k+1   −  1
                                            k+2 .        open Finset
        Pn−1  1           
                                                         example (n : ℕ) :
                k+1 − k+2    = 1 − n+1
                        1           1
We have   k=0                           .
     Pn−1                                                   ∑ k ∈ range n, (1 : ℝ) / ((k + 1) * (k + 2)) = n
       k=0 (k+1)(k+2) = 1 − n+1 .
                1             1
Then
                                                                  / (n + 1) := by
We have 1 − n+1
             1      n
                 = n+1 .                                  induction n with
     Pn−1       1         n
Then   k=0 (k+1)(k+2) =  n+1 .                            | zero => simp
                                                          | succ n ih =>
                                                            rw [sum_range_succ, ih]
                                                            have hn1 : (n : ℝ) + 1 > 0 := by positivity
                                                            have hn2 : (n : ℝ) + 2 > 0 := by positivity
                                                            have hn1' : (n : ℝ) + 1 ≠ 0 := ne_of_gt hn1
                                                            have hn2' : (n : ℝ) + 2 ≠ 0 := ne_of_gt hn2
                                                            push_cast
                                                            field_simp
                                                            ring

                                                         end VisoredPaperExamples.Ex12
                                                       ∑n−1      1         n
miniF2F induction_sum_1oktkp1. Telescoping sum           k=0 (k+1)(k+2) = n+1 . Lean induction on n, Finset.sum_range_succ,
field_simp, ring.

Visored CNL input (typeset)                              Hand-written Lean 4 proof
                                  Q501 4k+4
Example 13. The goal is to prove    k=1 4k  = 502.
                                                         import Mathlib
We have ∀k ∈ N, k > 0 → 4k+4   = k+1
                                     .
        Q501 4k+4     Q5014k k+1 k
We have             = k=1 k .                            namespace VisoredPaperExamples.Ex13
        Qk=1   4k
          501 k+1                                        open Finset
We have   k=1 k    = 502
                      1 .
                                                         theorem amc12a_2008_p4 :
We have 502 = 502.
     Q501 4k+4
         1                                                  ∏ k ∈ Finset.Icc (1 : ℕ) 501, ((4 : ℝ) * k + 4) / (4 *
Then   k=1 4k   = 502.                                           k) = 502 := by
                                                          have hfactor : ∀ k ∈ Finset.Icc (1 : ℕ) 501,
                                                             ((4 : ℝ) * k + 4) / (4 * k) = ((k : ℝ) + 1) / k := by
                                                            intro k hk
                                                            rcases Finset.mem_Icc.mp hk with ⟨hk1, _⟩
                                                            have hk0 : (k : ℝ) ≠ 0 := by
                                                             have : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk1
                                                             linarith
                                                            have h4 : (4 : ℝ) ≠ 0 := by norm_num
                                                            field_simp
                                                          rw [Finset.prod_congr rfl hfactor]
                                                          have htel : ∀ n : ℕ, 1 ≤ n →
                                                             ∏ k ∈ Finset.Icc (1 : ℕ) n, ((k : ℝ) + 1) / k = (n +
                                                                   1 : ℝ) / 1 := by
                                                            intro n hn
                                                            induction n, hn using Nat.le_induction with
                                                            | base =>
                                                             simp
                                                            | succ n hn ih =>
                                                             rw [show (n + 1 : ℕ) = n + 1 from rfl,
                                                                Finset.prod_Icc_succ_top (by exact Nat.
                                                                      le_succ_of_le hn)]
                                                             rw [ih]
                                                             have hnpos : (n : ℝ) + 1 ≠ 0 := by
                                                               have : (0 : ℝ) < (n : ℝ) + 1 := by
                                                                have : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
                                                                linarith
                                                               linarith
                                                             field_simp
                                                             push_cast
                                                             ring
                                                          have := htel 501 (by norm_num)
                                                          rw [this]
                                                          norm_num

                                                         end VisoredPaperExamples.Ex13

                                                     ∏501 4k+4
miniF2F amc12a-2008-p4. Telescoping product           k=1    4k
                                                                  = 502. Lean uses Finset.prod_Icc_succ_top


                                                        39
for the structural induction.


H.5      Functional equations

Visored CNL input (typeset)                                    Hand-written Lean 4 proof

Example 14. Let a ∈ R.
                                                               import Mathlib
Let b ∈ R.
Let c ∈ R.
Let f : R → R be a function.                                   namespace VisoredPaperExamples.Ex14
Assume ∀x ∈ R, f (x + 3) = 3x2 + 7x + 4.                       example (a b c : ℝ) (f : ℝ → ℝ)
                                                                  (h1 : ∀ x : ℝ, f (x + 3) = 3 * x^2 + 7 * x + 4)
Assume ∀x ∈ R, f (x) = ax2 + bx + c.
The goal is to prove a + b + c = 2.                               (h2 : ∀ x : ℝ, f x = a * x^2 + b * x + c) :
                                                                  a + b + c = 2 := by
We have ∀x ∈ R, f (x + 3) = a(x + 3)2 + b(x + 3) + c.
                                                                have hf1_shift : f ((-2 : ℝ) + 3) = 3 * (-2)^2 + 7 *
We have ∀x ∈ R, 3x2 + 7x + 4 = a(x + 3)2 + b(x + 3) + c.              (-2) + 4 := h1 (-2)
We have ∀x ∈ R, a(x + 3)2 + b(x + 3) + c = ax2 + 6ax +          have hf1 : f 1 = 2 := by
9a + bx + 3b + c.                                                 have : ((-2 : ℝ) + 3) = 1 := by norm_num
We have ∀x ∈ R, 3x2 + 7x + 4 = ax2 + 6ax + 9a + bx + 3b + c.
                                                                  rw [this] at hf1_shift
We have ∀x ∈ R, ax2 + 6ax + 9a + bx + 3b + c = ax2 + (6a +        linarith [hf1_shift]
b)x + (9a + 3b + c).
                                                                have hf1' : f 1 = a + b + c := by
We have ∀x ∈ R, 3x2 +7x+4 = ax2 +(6a+b)x+(9a+3b+c).               have := h2 1
We have a = 3.
We have 6a + b = 7.                                               simpa using this
We have b = −11.                                                linarith [hf1, hf1']
We have 9a + 3b + c = 4.
We have c = 10.                                                end VisoredPaperExamples.Ex14
We have a + b + c = 2.
miniF2F amc12a-2009-p9. Polynomial coeﬀicient identification: f (x+3) = 3x2 +7x+4 and f (x) = ax2 +bx+c,
find a + b + c. Lean specializes both hypotheses at x = −2 and x = 1, closes with linarith.

Visored CNL input (typeset)                                    Hand-written Lean 4 proof

Example 15. Let x ∈ R.
                                                               import Mathlib
Let σ : R → R be a function.
Assume σ is a bijection.
Assume ∀t ∈ R, σ(t) = 5t − 12.                                 namespace VisoredPaperExamples.Ex15
Assume σ(x + 1) = σ −1 (x).                                    open Function
                         47                                    example
The goal is to prove x = 24 .
                                                                  (x : ℝ)
We have σ(x + 1) = 5(x + 1) − 12.
                                                                  (σ σ_inv : ℝ → ℝ)
Then σ(x + 1) = 5x − 7.
                                                                  (hσ : Function.Bijective σ)
Then σ −1 (x) = 5x − 7.                                           (hLI : Function.LeftInverse σ_inv σ)
We have σ(5x − 7) = 5(5x − 7) − 12.
Then σ(5x − 7) = 25x − 47.                                        (h₀ : ∀ t : ℝ, σ t = 5 * t - 12)
                                                                  (h₁ : σ (x + 1) = σ_inv x) :
We have σ(σ −1 (x)) = x.
                                                                  x = 47 / 24 := by
Then 25x − 47 = x.
Then 24x = 47.                                                  have hSurj : Function.Surjective σ := hσ.surjective
Then x = 47/24.                                                 have hRI : Function.RightInverse σ_inv σ :=
                                                                  hLI.rightInverse_of_surjective hSurj
                                                                have hσx1 : σ (x + 1) = 5 * x - 7 := by
                                                                  have := h₀ (x + 1)
                                                                  linarith
                                                                have hInvFormula : σ_inv x = 5 * x - 7 := by
                                                                  have := h₁.symm.trans hσx1
                                                                  exact this
                                                                have hApplyσ : σ (σ_inv x) = σ (5 * x - 7) :=
                                                                  congrArg σ hInvFormula
                                                                have hLHS : σ (σ_inv x) = x := hRI x
                                                                have hRHS : σ (5 * x - 7) = 25 * x - 47 := by
                                                                  have := h₀ (5 * x - 7)
                                                                  linarith
                                                                have hChain : x = 25 * x - 47 := by
                                                                  calc x = σ (σ_inv x) := hLHS.symm
                                                                   _ = σ (5 * x - 7) := hApplyσ
                                                                   _ = 25 * x - 47 := hRHS
                                                                linarith

                                                               end VisoredPaperExamples.Ex15


miniF2F mathd-algebra-422. σ(σ −1 (x)) = x trick. Lean’s bijection layer requires Function.Bijective.surjective
and Function.LeftInverse.rightInverse_of_surjective to extract the cancellation; the algebraic close is
linarith.




                                                               40
H.6     Sequences and recurrences

Visored CNL input (typeset)                                Hand-written Lean 4 proof

Example 16. Let f : N → R be a function.
                                                           import Mathlib
Assume f (1) = 2.
Assume ∀n ∈ N, n > 1 ∧ n mod 2 = 0 =⇒ f (n) = f (n −
1) + 1.                                                    namespace VisoredPaperExamples.Ex17
Assume ∀n ∈ N, n > 1 ∧ n mod 2 = 1 =⇒ f (n) = f (n −       example
2) + 2.                                                       (f : ℕ → ℝ)
The goal is to prove f (2017) = 2018.                         (h1 : f 1 = 2)
Let k ∈ N.                                                    (heven : ∀ n : ℕ, n > 1 ∧ n % 2 = 0 → f n = f (n - 1) +
We prove f (2k + 1) = 2k + 2 by induction on k :                     1)
• Case k = 0.                                                 (hodd : ∀ n : ℕ, n > 1 ∧ n % 2 = 1 → f n = f (n - 2) +
   We have f (1) = 2.
                                                                    2) :
   We have 2 · 0 + 2 = 2.
   Then f (2 · 0 + 1) = 2 · 0 + 2.                            f 2017 = 2018 := by
• Case k ≥ 0.                                               have key : ∀ k : ℕ, f (2 * k + 1) = 2 * k + 2 := by
   Assume f (2k + 1) = 2k + 2.                                intro k
   The goal is to prove f (2(k + 1) + 1) = 2(k + 1) + 2.      induction k with
   We have 2(k + 1) + 1 = 2k + 3.                             | zero =>
   We have 2k + 3 > 1.                                           simpa using h1
   We have 2k + 3 ≡ 1 (mod 2).                                | succ k ih =>
   Then (2k + 3) mod 2 = 1.                                      have hindex : 2 * (k + 1) + 1 = 2 * k + 3 := by
   We have f (2k + 3) = f ((2k + 3) − 2) + 2.
                                                                   have hsucc : Nat.succ k = k + 1 := Nat.
   We have (2k + 3) − 2 = 2k + 1.
   Then f (2k + 3) = f (2k + 1) + 2.                                     succ_eq_add_one k
   We have f (2k + 1) = 2k + 2.                                    have hadd : k + 1 = Nat.succ k := (Nat.add_one k).
   Then f (2k + 3) = (2k + 2) + 2.                                       symm
   We have (2k + 2) + 2 = 2k + 4.                                  ring
   We have 2k + 4 = 2(k + 1) + 2.                                have hgt : 2 * k + 3 > 1 := by omega
   Then f (2(k + 1) + 1) = 2(k + 1) + 2.                         have hmod : (2 * k + 3) % 2 = 1 := by omega
We have 2017 = 2 · 1008 + 1.                                     have hrec : f (2 * k + 3) = f (2 * k + 3 - 2) + 2 :=
We have f (2 · 1008 + 1) = 2 · 1008 + 2.                           hodd (2 * k + 3) ⟨hgt, hmod⟩
We have 2 · 1008 + 2 = 2018.
                                                                 have hsub : 2 * k + 3 - 2 = 2 * k + 1 := by omega
Then f (2017) = 2018.
                                                                 calc f (2 * (k + 1) + 1)
                                                                     = f (2 * k + 3) := by rw [hindex]
                                                                   _ = f (2 * k + 3 - 2) + 2 := hrec
                                                                   _ = f (2 * k + 1) + 2 := by rw [hsub]
                                                                   _ = (2 * (k : ℝ) + 2) + 2 := by rw [ih]
                                                                   _ = 2 * ((k : ℝ) + 1) + 2 := by ring
                                                                   _ = 2 * ((k + 1 : ℕ) : ℝ) + 2 := by push_cast; ring
                                                            have h2017 : (2017 : ℕ) = 2 * 1008 + 1 := by norm_num
                                                            have happ := key 1008
                                                            have : f 2017 = (2 * (1008 : ℝ) + 2) := by
                                                              rw [h2017]; exact_mod_cast happ
                                                            linarith [this]

                                                           end VisoredPaperExamples.Ex17


miniF2F amc12a-2017-p7. Recurrence with parity, induct on odd indices f (2k + 1) = 2k + 2. Lean uses
Nat.succ_eq_add_one, push_cast, and omega.




                                                           41
H.7      Trigonometry

Visored CNL input (typeset)                         Hand-written Lean 4 proof

Example 17. Let x ∈ R.
                                                    import Mathlib
Assume 0 ≤ x ≤ 2π.
                 p              p             √
Assume 2 cos x ≤   1 + sin(2x) − 1 − sin(2x) ≤ 2.   namespace VisoredPaperExamples.Ex19
The goal is to prove π  ≤ x ≤ 7π
                               4 .
                                                    open Real
                   √ 4                              example (x : ℝ)
We have 2 cos x ≤√ 2.
                                                       (hx0 : 0 ≤ x) (hx2pi : x ≤ 2 * π)
We have cos x ≤ 22 .                                   (h : 2 * Real.cos x ≤ |Real.sqrt (1 + Real.sin (2 * x))
                   √
We have cos π     = 22 .                                      -
              4
                    √
                                                                        Real.sqrt (1 - Real.sin (2 * x))| ∧
We have cos 7π 4   = 22 .
                                                           |Real.sqrt (1 + Real.sin (2 * x)) -
Then π4 ≤ x ≤ 4 .
                7π
                                                            Real.sqrt (1 - Real.sin (2 * x))| ≤ Real.sqrt 2) :
                                                       π / 4 ≤ x ∧ x ≤ 7 * π / 4 := by
                                                     have hpi_pos : 0 < π := Real.pi_pos
                                                     have h2cos : 2 * Real.cos x ≤ Real.sqrt 2 := le_trans h
                                                           .1 h.2
                                                     have hcos_le : Real.cos x ≤ Real.sqrt 2 / 2 := by
                                                           linarith
                                                     have h_arccos_sqrt2_div_2 : Real.arccos (Real.sqrt 2 /
                                                           2) = π / 4 := by
                                                       have h1 : (0 : ℝ) ≤ π / 4 := by linarith
                                                       have h2 : π / 4 ≤ π := by linarith
                                                       have hcos_pi4 : Real.cos (π / 4) = Real.sqrt 2 / 2 :=
                                                             Real.cos_pi_div_four
                                                       have := Real.arccos_cos h1 h2
                                                       rw [hcos_pi4] at this
                                                       exact this
                                                     by_cases hxπ : x ≤ π
                                                         ·
                                                             have harccos_cos : Real.arccos (Real.cos x) = x := Real
                                                                  .arccos_cos hx0 hxπ
                                                             have hmono : Real.arccos (Real.sqrt 2 / 2) ≤ Real.
                                                                  arccos (Real.cos x) :=
                                                              Real.arccos_le_arccos hcos_le
                                                             have hlb : π / 4 ≤ x := by
                                                              have := hmono
                                                              rw [h_arccos_sqrt2_div_2, harccos_cos] at this
                                                              exact this
                                                             refine ⟨hlb, ?_⟩
                                                             linarith
                                                         ·
                                                             push_neg at hxπ
                                                             have hy0 : 0 ≤ 2 * π - x := by linarith
                                                             have hyπ : 2 * π - x ≤ π := by linarith
                                                             have hcosy_eq : Real.cos (2 * π - x) = Real.cos x :=
                                                                  Real.cos_two_pi_sub x
                                                             have hcosy_le : Real.cos (2 * π - x) ≤ Real.sqrt 2 / 2
                                                                  := by
                                                              rw [hcosy_eq]; exact hcos_le
                                                             have harccos_cos_y : Real.arccos (Real.cos (2 * π - x))
                                                                   = 2 * π - x :=
                                                              Real.arccos_cos hy0 hyπ
                                                             have hmono : Real.arccos (Real.sqrt 2 / 2) ≤ Real.
                                                                  arccos (Real.cos (2 * π - x)) :=
                                                              Real.arccos_le_arccos hcosy_le
                                                             have hyge : π / 4 ≤ 2 * π - x := by
                                                              have := hmono
                                                              rw [h_arccos_sqrt2_div_2, harccos_cos_y] at this
                                                              exact this
                                                             refine ⟨?_, ?_⟩
                                                             ·
                                                                 linarith
                                                             ·
                                                                 linarith

                                                    end VisoredPaperExamples.Ex19

miniF2F imo-1965-p1. Inverse-trig reasoning. Lean Mathlib names: Real.cos_pi_div_four, Real.arccos_cos,
Real.arccos_le_arccos. The interval [π/4, 7π/4] has to be the canonical range for arccos_cos to unfold.




                                                    42
H.8     Logarithm and exponential

Visored CNL input (typeset)                         Hand-written Lean 4 proof

Example 18. Let x ∈ R.
Assume x ̸= 0.                                      import Mathlib
                        
                     4 −1 3x3
                                2     
                                    1 −3
The goal is to prove x       x     2x    = 18x8 .
                3 2                             namespace VisoredPaperExamples.Ex20
           4 −1 3x       1 −3
We have x         x     2x     = 18x8 .             example (x : ℝ) (h₀ : x ≠ 0) :
                                                       (4 / x)⁻1 * ((3 * x^3) / x)^2 * ((1 / (2 * x))⁻1
                                                            )^3 = 18 * x^8 := by
                                                     field_simp
                                                     ring

                                                    end VisoredPaperExamples.Ex20

miniF2F mathd-algebra-245. Exponent simplification chain. Lean steps: inv_div, pow_succ, mul_pow,
pow_mul, one_div, inv_inv; one named lemma per CNL line.




                                                    43
Visored CNL input (typeset)                                     Hand-written Lean 4 proof

Example 19. Let a ∈ R.
                                                                import Mathlib
Let b ∈ R.
Assume a > 0.
Assume b > 0.                                                   namespace VisoredPaperExamples.Ex21
Assume log8 a + log4 (b2 ) = 5.                                 open Real
Assume log8 b + log4 (a2 ) = 7.                                 example (a b : ℝ) (ha : 0 < a) (hb : 0 < b)
The goal is to prove ab = 512.                                     (h1 : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5)
We have 31 log2 a + 12 log2 (b2 ) = 13 log2 a + 22 log2 b =        (h2 : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7) :
 1                                                                 a * b = 512 := by
 3 log2 a + log2 b = 5.                                          have ha_ne : a ≠ 0 := ne_of_gt ha
We have 13 log2 b + 21 log2 (a2 ) = 13 log2 b + 22 log2 a =      have hb_ne : b ≠ 0 := ne_of_gt hb
 1
 3 log2 b + log2 a = 7.                                          have hab_pos : 0 < a * b := mul_pos ha hb
We have 3( 13 log2 a + log2 b) = log2 a + 3 log2 b = log2 a +    have hlog2_pos : (0 : ℝ) < Real.log 2 :=
log2 (b3 ) = log2 (ab3 ) = 15.                                     Real.log_pos (by norm_num)
We have ab3 = 215 .                                              have hlog2_ne : Real.log 2 ≠ 0 := ne_of_gt hlog2_pos
We have 3( 13 log2 b + log2 a) = log2 b + 3 log2 a = log2 b +    have hlog8 : Real.log 8 = 3 * Real.log 2 := by
                                                                   have h8 : (8 : ℝ) = (2 : ℝ) ^ (3 : ℕ) := by norm_num
log2 (a3 ) = log2 (ba3 ) = 21.
                                                                   rw [h8, Real.log_pow]; push_cast; ring
We have ba3 = 221 .                                              have hlog4 : Real.log 4 = 2 * Real.log 2 := by
We have (ab3 )(ba3 ) = (ab)4 = 215 221 = 236 .
                                                                   have h4 : (4 : ℝ) = (2 : ℝ) ^ (2 : ℕ) := by norm_num
We have ab = 236/4 = 29 = 512.                                     rw [h4, Real.log_pow]; push_cast; ring
                                                                 have hloga2 : Real.log (a ^ 2) = 2 * Real.log a := by
                                                                   rw [Real.log_pow]; push_cast; ring
                                                                 have hlogb2 : Real.log (b ^ 2) = 2 * Real.log b := by
                                                                   rw [Real.log_pow]; push_cast; ring
                                                                 have h1d : Real.log a / (3 * Real.log 2)
                                                                           + 2 * Real.log b / (2 * Real.log 2) = 5 := by
                                                                   have htmp := h1
                                                                   unfold Real.logb at htmp
                                                                   rw [hlog8, hlog4, hlogb2] at htmp
                                                                   exact htmp
                                                                 have h2d : Real.log b / (3 * Real.log 2)
                                                                           + 2 * Real.log a / (2 * Real.log 2) = 7 := by
                                                                   have htmp := h2
                                                                   unfold Real.logb at htmp
                                                                   rw [hlog8, hlog4, hloga2] at htmp
                                                                   exact htmp
                                                                 have h3log2_ne : (3 : ℝ) * Real.log 2 ≠ 0 := mul_ne_zero
                                                                        (by norm_num) hlog2_ne
                                                                 have h2log2_ne : (2 : ℝ) * Real.log 2 ≠ 0 := mul_ne_zero
                                                                        (by norm_num) hlog2_ne
                                                                 have h1m : 2 * Real.log a + 6 * Real.log b = 30 * Real.
                                                                       log 2 := by
                                                                   have heq1 : (Real.log a / (3 * Real.log 2)
                                                                         + 2 * Real.log b / (2 * Real.log 2)) * (6 * Real.
                                                                               log 2)
                                                                         = 5 * (6 * Real.log 2) := by
                                                                    rw [h1d]
                                                                   have hexp : (Real.log a / (3 * Real.log 2)
                                                                            + 2 * Real.log b / (2 * Real.log 2)) * (6 *
                                                                                  Real.log 2)
                                                                            = 2 * Real.log a + 6 * Real.log b := by
                                                                    field_simp
                                                                    ring
                                                                   linarith [heq1, hexp]
                                                                 have h2m : 2 * Real.log b + 6 * Real.log a = 42 * Real.
                                                                       log 2 := by
                                                                   have heq2 : (Real.log b / (3 * Real.log 2)
                                                                         + 2 * Real.log a / (2 * Real.log 2)) * (6 * Real.
                                                                               log 2)
                                                                         = 7 * (6 * Real.log 2) := by
                                                                    rw [h2d]
                                                                   have hexp : (Real.log b / (3 * Real.log 2)
                                                                            + 2 * Real.log a / (2 * Real.log 2)) * (6 *
                                                                                  Real.log 2)
                                                                            = 2 * Real.log b + 6 * Real.log a := by
                                                                    field_simp
                                                                    ring
                                                                   linarith [heq2, hexp]
                                                                 have hsum : Real.log a + Real.log b = 9 * Real.log 2 :=
                                                                       by linarith
                                                                 have hlog_ab : Real.log (a * b) = Real.log 512 := by
                                                                   rw [Real.log_mul ha_ne hb_ne, hsum]
                                                                   have h512 : (512 : ℝ) = (2 : ℝ) ^ (9 : ℕ) := by
                                                                        norm_num
                                                                   rw [h512, Real.log_pow]
                                                                   push_cast
                                                                   ring
                                                                 have h512_pos : (0 : ℝ) < 512 := by norm_num
                                                                 exact Real.log_injOn_pos (Set.mem_Ioi.mpr hab_pos)
                                                                   (Set.mem_Ioi.mpr h512_pos) hlog_ab

                                                                end VisoredPaperExamples.Ex21


                                                                44
miniF2F aime-1984-p5. Log chain. The Lean version exercises a standard Mathlib path: Real.log_pow,
Real.log_mul (with ne_of_gt side conditions for each factor), Real.log_pos on 1 < 2, and Real.log_injOn_pos
to cancel the outer log. The CNL version is a chain of equalities; the Lean version makes every positivity hy-
pothesis explicit.


H.9      Set and membership

Visored CNL input (typeset)                                      Hand-written Lean 4 proof

Example 20. Let S = {x ∈ N | 0 < x < 1000 ∧ |{d ∈ N |
d | x}| = 3}.                                                    import Mathlib
The goal is to prove |S| = 11.
We have S = {4, 9, 25, 49, 121, 169, 289, 361, 529, 841, 961}.   namespace VisoredPaperExamples.Ex24
We have |S| = 11.
                                                                 open Finset
                                                                 theorem mathd_numbertheory_221
                                                                    (S : Finset ℕ)
                                                                    (h₀ : ∀ x : ℕ, x ∈ S ↔ 0 < x ∧ x < 1000 ∧ x.
                                                                         divisors.card = 3) :
                                                                    S.card = 11 := by
                                                                  have hS :
                                                                      S = (Finset.range 1000).filter (fun x => 0 < x
                                                                            ∧ x.divisors.card = 3) := by
                                                                    ext x
                                                                    rw [h₀ x, Finset.mem_filter, Finset.mem_range]
                                                                    constructor
                                                                    ·rintro ⟨hpos, hlt, hdiv⟩
                                                                      exact ⟨hlt, hpos, hdiv⟩
                                                                    ·rintro ⟨hlt, hpos, hdiv⟩
                                                                      exact ⟨hpos, hlt, hdiv⟩
                                                                  rw [hS]
                                                                  native_decide

                                                                 end VisoredPaperExamples.Ex24

miniF2F mathd-numbertheory-221. Set with divisor-count = 3 (squares of primes) cardinality. The Lean
writer rewrites the set as a Finset.filter over Finset.range 1000 and closes with native_decide; only
works because the bound is a concrete numeral.




                                                                 45
Visored CNL input (typeset)                       Hand-written Lean 4 proof
                               √     √
Example 21. Let S = {n ∈ N | n < 72 ∧ n > 2}.
                                                  import Mathlib
The goal is to prove |S| = 8.
      ∈ N.
Let n √
                                                  namespace VisoredPaperExamples.Ex23
Then √n > 2 ⇐⇒ n > 4.
                                                  lemma pred_equiv (n : ℕ) :
Then n < 72 ⇐⇒ n < 49     4 .                        (Real.sqrt n < 7 / 2 ∧ 2 < Real.sqrt n) ↔ (5 ≤ n ∧ n ≤
Then n > 4 ⇐⇒ n ≥ 5.
                                                          12) := by
We have 49          1
          4 = 12 + 4 .                             have h_lower :
Then n < 49   ⇐⇒ n ≤ 12.                              (2 : ℝ) < Real.sqrt n ↔ (4 : ℝ) < (n : ℝ) := by
      √    4     √
Then n < 72 ∧ n > 2 ⇐⇒ 5 ≤ n ≤ 12.                   have h2 : (0 : ℝ) ≤ 2 := by norm_num
Then S = {n ∈ N | 5 ≤ n ≤ 12}.                       have := Real.lt_sqrt (x := (2 : ℝ)) (y := (n : ℝ)) h2
We have |{n ∈ N | 5 ≤ n ≤ 12}| = 8.                  simpa [show ((2 : ℝ))^2 = 4 by norm_num] using this
Then |S| = 8.                                      have h_upper :
                                                      Real.sqrt n < (7 : ℝ) / 2 ↔ (n : ℝ) < (49 : ℝ) / 4 :=
                                                             by
                                                     have hpos : (0 : ℝ) < 7 / 2 := by norm_num
                                                     have := Real.sqrt_lt' (x := (n : ℝ)) (y := (7 : ℝ) / 2)
                                                           hpos
                                                     simpa [show ((7 : ℝ) / 2) ^ 2 = 49 / 4 by norm_num]
                                                          using this
                                                   rw [h_lower, h_upper]
                                                   constructor
                                                   ·rintro ⟨hup, hlo⟩
                                                     have hlo' : 4 < n := by exact_mod_cast hlo
                                                     have hup' : (n : ℝ) < 13 := by linarith
                                                     have hup'' : n < 13 := by exact_mod_cast hup'
                                                     exact ⟨hlo', Nat.lt_succ_iff.mp hup''⟩
                                                   ·rintro ⟨hlo, hup⟩
                                                     refine ⟨?_, ?_⟩
                                                     ·
                                                         have : (n : ℝ) ≤ 12 := by exact_mod_cast hup
                                                         linarith
                                                     ·
                                                      have : (5 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hlo
                                                      linarith
                                                  lemma set_eq :
                                                     {n : ℕ | Real.sqrt n < 7 / 2 ∧ 2 < Real.sqrt n}
                                                      = {n : ℕ | 5 ≤ n ∧ n ≤ 12} := by
                                                   apply Set.ext
                                                   intro n
                                                   rw [Set.mem_setOf_eq, Set.mem_setOf_eq]
                                                   exact pred_equiv n

                                             √
miniF2F mathd-algebra-224. Set-builder with n ∈ (2, 7/2) rewritten as n ∈ {5, . . . , 12}. Lean uses
Real.lt_sqrt, Real.sqrt_lt' to square out the radical, then Set.ext / Finset.ext / Nat.card_Icc for
the final cardinality.




                                                46
