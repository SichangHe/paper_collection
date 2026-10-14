                                                                   Sorries Are Not the Hard Part:
                                                  An Expert-Review Case Study of a Semi-Autonomous Formalization


                                                                                         Vasily Ilin * 1 Brian Nugent * 2


                                                                    Abstract                                    mension of X, then the n-th sheaf cohomology of any sheaf
                                                                                                                of abelian groups on X vanishes. The authors wrote the
                                               Large language models can often close proof gaps
                                                                                                                Lean statement by hand, supplied Claude Code with a PDF
arXiv:2606.13925v1 [cs.AI] 11 Jun 2026




                                               in interactive theorem provers, but a verified the-
                                                                                                                excerpt of Hartshorne’s proof, and instructed the agent to
                                               orem is not the same thing as a reusable library
                                                                                                                follow that proof. The statement uses only existing mathlib
                                               contribution. We study this distinction through a
                                                                                                                definitions:
                                               detailed case study: a semi-autonomous formal-
                                               ization of Grothendieck’s vanishing theorem. The                 theorem GrothendieckVanishing
                                               initial version compiles with no sorries, but an ex-                 (X : TopCat) [NoetherianSpace X]
                                               pert review found serious problems in definitions,                   (n : Nat) (h : n > topologicalKrullDim X)
                                                                                                                    (F : Sheaf AddCommGrpCat X) :
                                               theorem generality, file organization, and the API.
                                                                                                                    Subsingleton (Sheaf.H F n)
                                               We then ran a review-driven refactor and compres-
                                               sion process and obtained a second expert review.                That the statement uses only existing definitions matters: it
                                               The before-and-after comparison shows a sharp                    prevents the agent from making custom definitions to render
                                               split: agents adapted well to local, mechanically                the theorem trivially true.
                                               checkable feedback, but remained weak at choos-
                                               ing definitions and designing APIs. We argue that                Proof sketch. The formal proof follows Hartshorne’s
                                               autoformalization should be evaluated not only                   route by induction on topologicalKrullDim X. First
                                               by closed sorries, but by whether the resulting                  it reduces to the irreducible case using a closed-immersion
                                               formalization survives expert review.                            short exact sequence and the fact that Noetherian spaces
                                                                                                                have finitely many irreducible components. For an irre-
                                                                                                                ducible space of dimension zero, every open is simple
                                         1. Intro                                                               enough that any sheaf is flasque, and higher cohomology of
                                                                                                                any flasque sheaf vanishes. In the positive-dimensional irre-
                                         The default public story for semi-autonomous formalization
                                                                                                                ducible case, the proof chooses a proper irreducible closed
                                         is proof completion: given an informal or formal statement,
                                                                                                                Z ⊂ X, uses strict dimension drop on Z, and combines the
                                         can an agent produce code accepted by a proof assistant?
                                                                                                                induction hypothesis with closed-immersion cohomology,
                                         This is the right first question, but it is not the last. Modern
                                                                                                                extension by zero, and a finite-generation reduction through
                                         mathematics is highly interconnected, and a formal library
                                                                                                                filtered colimits. These reductions need supporting defini-
                                         that supports it must compose: definitions must combine,
                                                                                                                tions and API not currently in mathlib — for the closed-
                                         theorem statements must have the right generality, names-
                                                                                                                immersion short exact sequence, flasque vanishing, exten-
                                         paces must support search, and APIs must let future users
                                                                                                                sion by zero, finite-generation via filtered colimits, topologi-
                                         reason about properties rather than unfold implementations.
                                                                                                                cal Krull dimension, and sheaf cohomology — which serve
                                         This paper evaluates the quality of LLM-produced Lean                  as our tests for the agent’s ability to define new objects and
                                         code and asks what the current barriers are between it                 build around them.
                                         and a reusable library contribution. Our case study is a
                                         Lean formalization of Grothendieck’s vanishing theorem                 Before and After. We treat the project as a before-and-
                                         (Hartshorne, 1977, Ch. III, Thm. 2.7): if X is a Noetherian            after experiment. State A is the first verified version, in-
                                         topological space and n is above the topological Krull di-             spected by one of the authors, a Lean/mathlib expert. State
                                           *
                                                                                                                B is the version after an automated response to that review
                                            Equal contribution 1 University of Washington, Seattle, WA,         and a later mathlib-style cleanup, inspected by the same
                                         USA 2 University of Utah, Salt Lake City, UT, USA. Correspon-
                                         dence to: Vasily Ilin <vasilin97@gmail.com>.                           expert. The review exposes what proof-completion metrics
                                                                                                                miss: LLMs are much better at closing local goals than at
                                         Preprint. June 15, 2026.                                               deciding what objects should exist.

                                                                                                            1
                                                 Sorries Are Not the Hard Part

The contributions are:                                                formalization that uncovered a literature error (Tooby-Smith,
                                                                      2026), autonomous number-theory and algebra formaliza-
   • a case study of semi-autonomous formalization of a               tions (Chen et al., 2026b;a), Archon’s previously open
     graduate-level algebraic geometry theorem in Lean;               commutative-algebra conjecture in roughly 19,000 lines (Ju
                                                                      et al., 2026), LeanMarathon’s multi-agent construct–audit–
   • a qualitative before-and-after analysis of expert review
                                                                      prove–repair harness over four Erdős problems (Zhang et al.,
     feedback on definitions, theorem statements, proofs,
                                                                      2026), and AutoformBot’s thousands of agents formalizing
     and file/API structure.
                                                                      26 textbooks into over 45,000 declarations (Rammal et al.,
Why this theorem is a useful stress test. Grothendieck                2026). Closest to our setting, the Vlasov-Maxwell-Landau
vanishing is not a contest-style problem reducible to a single        case study (Ilin, 2026) also emphasizes full-process logs,
tactic script. The theorem is short only because it sits on           agent failure modes, and human review of key statements.
a tower of categorical and topological infrastructure: the            These reports show AI can produce substantial verified ar-
agent had to work simultaneously with presheaves, sheaves,            tifacts quickly and that process logs expose failures a final
stalks, exact sequences, filtered colimits, Krull dimension,          proof hides.
and the derived-category definition of cohomology. The
central claim is deliberately modest: we do not claim one             What the prior work leaves open. What none of this
formalization predicts all future work, only that kernel ac-          isolates is the gap between a verified artifact and a reusable
ceptance is an incomplete evaluation target, and that this            one. Proof-generation evaluations have an unambiguous
case shows why.                                                       terminal condition — the artifact checks or it does not —
                                                                      but for library construction the statement and its interme-
2. Related Work                                                       diate abstractions are themselves outputs, and a proof can
                                                                      pass the kernel while forcing future users through awkward
Formal libraries as shared interfaces. The case study                 coercions or duplicated definitions. Large-scale reports in-
builds on Lean (de Moura et al., 2015; de Moura & Ullrich,            clude rich process data, but their notion of quality is still
2021) and mathlib, a single shared library supporting mod-            dominated by completion. We instead make the expert re-
ern mathematics at scale (The mathlib Community, 2020).               view the object of study, letting us ask which complaints an
Evaluating a contribution to such a library is closer to code         automated loop fixes and which persist because they require
review than to grading a fixed benchmark theorem.                     judgment about future reuse rather than proof search.

LLMs for proof generation. Autoformalization and neu-                 3. Timeline
ral theorem proving have largely been framed as translation
(Wu et al., 2022), retrieval, and proof-search problems: Le-          Reconstructing the project. Figure 1 and Table 1 recon-
anDojo (Yang et al., 2023) and Baldur (First et al., 2023)            struct the project from its commit history, structured loop
target retrieval-augmented proving and whole-proof repair,            logs, telemetry summaries, and two expert reviews of the
APRIL (Wang et al., 2026) learns proof repair and iterative           same development.1 The mathematical statement and proof
refinement from compiler feedback, and recent systems—                outline were supplied by humans.
Seed-Prover (Chen et al., 2025), Aristotle (Achim et al.,
2025), Numina-Lean-Agent (Liu et al., 2026), and QED-                 The proving phase. The proving phase was fast because
Nano (LM-Provers et al., 2026)—scale proof search through             the route was fixed in advance. The sorry curve in Figure 1
formal feedback, agentic tool use, and distillation. A few ef-        is nonetheless jagged, because the agent scaffolded interme-
forts push past binary correctness: Petrov et al. (2026) score        diate claims, discharged some, and repeatedly changed the
whether a proof is clear, concise, and transferable, Xie et al.       proof decomposition. The clearest side quest is the heartbeat
(2026) test whether models can judge mathlib pull-request             episode (Mar. 28 – Apr. 1). Mathlib’s synthInstance
merge-readiness, and Klingner et al. (2026) evaluate formal-          budget for HasDerivedCategory kept colliding with
ization in realistic imported contexts (miniF2F, miniCTX).            proofs mentioning Ext or Sheaf.H, and the agent’s first
In all of these the unit of evaluation is the attempted theo-         instinct was to raise set_option maxHeartbeats,
rem; ours is the library delta that survives after it closes —        oscillating budgets between 200K and 12.8M across days
the duplicated definition or over-specific lemma a theorem
                                                                         1
benchmark has no reason to penalize.                                      The two expert reviews and the structured process
                                                                      logs analyzed in this paper are released as a public
Research-scale semi-autonomous formalization. Sev-                    dataset:      https://huggingface.co/datasets/
                                                                      uw-math-ai/grothendieck-vanishing-logs.
eral recent projects move beyond contest problems: rapid              The Lean source is available at https://github.
large-scale topology (Urban, 2026), parallel Diophantine for-         com/Vilin97/Clawristotle/tree/main/
malization in Isabelle (Bayer et al., 2025), a Lean/PhysLean          grothendieck-vanishing.

                                                                  2
                                                            Sorries Are Not the Hard Part

                                               Grothendieck-vanishing formalization timeline
                                                                                                                                   40
                                   Proving                  Review window                     Refactor         Compress + polish
                                                                                                                                   35
                   8000
                                                                                                                                   30
                                                                                                                                   25
    Raw Lean LOC




                   6000




                                                                                                                                    Sorry count
                                                                                                                                   20
                   4000                                                                                                            15
                                                                                                                                   10
                   2000
                                                                                                                   Raw Lean LOC 5
                                                                                                                   Sorry count
                      0   Mar 28       Apr 2        Apr 7         Apr 12          Apr 17       Apr 22       Apr 27       May 2 0
Figure 1. Project timeline reconstructed from the commit log. The blue curve is raw Lean lines of code and the red curve is the sorry
count. Background colors mark the process phases: green = proving, yellow = expert-review window, blue = review-driven refactor,
purple = compression and final mathlib-style polish. The proving phase produces the first sorry-free version by April 4; LOC then keeps
moving well after the sorry count reaches zero, as the project is rewritten in response to the expert review.


without producing a stable project. The episode only                            we still need to note that it is remarkable that it is able to
ended after one author told the agent to “keep optimiz-                         produce a proof this sophisticated with no human guidance
ing until the whole project compiles with default heart-                        other than the theorem statement and a standard textbook
beats”. Stripping the overrides regressed the sorry count                       proof – this was not possible one year ago.
from 3 to 24; recovery came from caching instances via
                                                                                Now that we have a formalized proof, the next question is:
inferInstanceAs and splitting large proofs into named
                                                                                what can be done with the 5,000 lines of code that were
sub-lemmas. The durable rule that came out of this is: never
                                                                                produced? Can the definitions and lemmas proved along the
raise maxHeartbeats above 200000. It is the first ap-
                                                                                way to this theorem be repurposed and built off of? These
pearance of a pattern that recurs throughout the project: a
                                                                                questions are the focus of our analysis.
proof too expensive to check is usually a proof that should
be decomposed.                                                                  Lean code, in the context of theorem proving, has three main
                                                                                components: definitions, theorem statements, and proofs.
                                                                                We report on how the agent did in both state A and state B
After the proof closed. As seen in Figure 1 and Table 1,                        for each of these.
the project did not end when the sorry count reached zero.
Instead, one of the authors performed a comprehensive re-
view of the initial formalization (one week), which was                         Definitions were the weakest point. Of the three main
converted into a checklist, and then the agent (Claude and                      components to Lean code, definitions are by far the most
Codex) iterated until the checklist was finished (two weeks).                   important to get right and are where the agent struggled the
Three additional views of the same project (Figures 2 to 4)                     most.
record commit counts by loop mode, token usage, and tool-
                                                                                Bad definitions create future transport costs. If a construc-
use mix; we refer to them where relevant below. We refer
                                                                                tion is placed at the wrong level of generality, later users
to the initial formalization as state A, and the formalization
                                                                                must compare it to the version they actually need and then
that followed the first review as state B.
                                                                                transport every relevant theorem across that comparison.
                                                                                This transport can often be harder than simply redoing ev-
4. Analysis                                                                     erything from scratch. When that is the case, it begs the
                                                                                question of whether there is any value in a formalization if
What state A got right. The initial state had the proof
                                                                                it cannot be built upon effectively in the future. A proof can
in the right mathematical shape. The overall structure of
                                                                                be ugly and still mostly function while a bad definition can
the proof was exactly as expected and followed the proof
                                                                                create serious problems down the line.
outline described above. While the goal of this article is to
provide analysis of the quality of LLM-produced Lean code,                      The finitely generated subsheaf construction is a represen-

                                                                            3
                                                    Sorries Are Not the Hard Part

                              Table 1. Project phases reconstructed from commits, loop logs, and reviews.

   Phase                    Duration                  What happened                             Main difficulty
   Formalization            Mar. 27–Apr. 4; nine      Claude Code followed the supplied         The agent could close local goals, but
                            active days               Hartshorne proof plan, with Aristotle     the emerging API was ad hoc. A
                                                      used for bounded lemmas. This             heartbeat detour also stopped the
                                                      produced state A, the first sorry-free    project from compiling cleanly until
                                                      version.                                  large proofs were decomposed.
   Expert review            Apr. 8–15; one week       The same expert read the first verified   The review judged the code after
                                                      tree as library code and wrote a          kernel success, so it found design
                                                      structured audit with large cross-file    failures that no proof-completion
                                                      changes and per-file comments.            metric could see.
   Review response          Apr. 17–May 1;            The main refactor loop ran Apr.           Local checklist items were tractable;
                            about two weeks           19–27.                                    open-ended requests such as building
                                                                                                a usable Sheaf.H API were much
                                                                                                harder.
   Compression and          Apr. 27–May 1             The compression loop ran Apr. 27–28,      The LOC gate found real redundancy,
   polish                                             followed by a mathlib-style cleanup       but short code was only a proxy for
                                                      pass for names, docstrings, lint, and     library quality.
                                                      stale comments.

Table 2. Qualitative before-and-after summary from the expert reviews. The table separates review items that have a local syntactic target
from items that require global API judgment.

  Review theme                  State A criticism                                  State B outcome
  File structure                File names were confusing and unorganized.        Fixed. File names make sense and docstrings
                                                                                  became readable.
  Definitions                   Dozens of specific and often unnecessary          Still the weakest category, did not noticeably
                                definitions.                                      improve after the review.
  Theorem statements            Most intermediate results were not general        All specific changes requested in the review were
                                enough to be reusable. Agent proved exactly       done but the agent failed to identify further changes
                                what it needed and nothing more.                  on its own.
  API design                    Proofs worked by repeatedly unfolding             Partially fixed. Downstream files are now cleaner
                                definitions rather than building an interface.    but the API itself is noisy and bloated.
  Proof style                   Proofs have long walls of have statements         Better but uneven. Some files became maintainable.
                                and frequent misuse of definitional equality.     The filtered-colimit files are still quite bad.


tative example. The agent defined finitely generated sub-               writing n < topologicalKrullDim X. Not only do
sheaves of sheaves of abelian groups on a topological space.            useless definitions like this make code more confusing, but
That was enough for the Grothendieck-vanishing proof, but               they also hinder the ability of tactics like simp. These tac-
the construction is not inherently about abelian groups or              tics use the syntax of the goal to decide on their next step
even topological spaces. In the future, one may want finitely           so a useless definition like this will cause it to fail where it
generated subsheaves for sheaves of rings, or on sheaves                otherwise would have succeeded.
over a site. A human library designer would first design the
                                                                        In total the agent made 62 of its own definitions and there
general construction and then provide convenient special-
                                                                        was exactly one that was done the correct way, namely
izations. The agent created exactly what the current proof
                                                                        TopCat.closedIncl. This is a construction that exists
needed instead.
                                                                        in mathlib for open sets but was missing for closed sets.
The same pattern appears in smaller definitions. Some dec-              The agent was able to build a useful API, likely copying
larations merely name a bijection that is needed once in a              the one from open sets in mathlib. This is the kind of
proof; others wrap a standard library construction under a              definition a library can keep, the object is mathematically
name that mentions the current application rather than the              natural, the name describes the object correctly, and the
mathematical object. These choices are cheap in the mo-                 adjacent API lets later proofs use it without needing to
ment because they give the agent a handle to continue the               unfold its definition. The remaining 61 definitions were all
proof. They are expensive later because they create public              done poorly and are not very useful for future formalizations.
surface area whose intended use is unclear. In state A, there           We give more specific examples of the problems with its
was a definition that roughly stated “n is less than the Krull          definitions in a section below.
dimension of X”. This is mathematically identical to just
                                                                        The agent did not improve its ability to make good def-

                                                                    4
                                                     Sorries Are Not the Hard Part




Figure 2. Daily commit counts classified by loop mode (commit-message tag). Phase shading matches Figure 1. Interactive commits
dominate the proving phase (the formalization was not fully automated); the April 8–17 gap is the expert-review window; the refactor
loop (green) drives the April 17–26 activity; the compression loop (orange) and a final mathlib-style polish (red) close out the project.




Figure 3. Cumulative Claude token usage across 31,529 turns in 270 sessions. Output (blue), fresh input (purple), and cache-creation
(orange) are on the left axis (millions); cache reads (red) on the right axis (billions). Cache reads exceed output by roughly two orders of
magnitude: formalization is context-dominated because each step reloads Lean files, diagnostics, and nearby library code. At the posted
Opus API rates ($75/M output, $18.75/M cache write, $1.50/M cache read, $15/M fresh input), the captured Claude usage corresponds to
a total of roughly $13K, dominated by cache reads (about $10K). The authors used the $200 subscription.


initions between state A and state B. Definitions remain                 stream files. In state B, the agent did create a dedicated
the largest hurdle between the agent and writing usable,                 cohomology API file, and this did substantially improve the
extensible code.                                                         rest of the proof. While in state A, many files were littered
                                                                         with specific and ad hoc proofs about cohomology, in state
                                                                         B they were contained to one file and the proofs in later
The API improved but not by much. After one decides
                                                                         files became much cleaner. Unfortunately, the API itself
on the right definition for an object, the next step is to build
                                                                         was built very poorly. Whenever a later proof needed a
an API for interacting with it. A good test of the agent’s
                                                                         fact about Sheaf.H, the agent simply added a new lemma
ability to do this came with cohomology. The version of
                                                                         to the file. Most of these lemmas were highly specific to
mathlib that the agent had access to possessed a definition
                                                                         whatever proof the agent was writing at the time. In the end,
of sheaf cohomology (Sheaf.H) but there had yet to be
                                                                         the file totaled almost 800 lines of code with 24 lemmas in
an API built for it. The first review complained that the
                                                                         the documentation header. A human designing this would
agent did not build an API for cohomology at all and instead
                                                                         instead try and distill out the most important properties to
just repeatedly unfolded the definition. A specific change
                                                                         design a small principled interface. This not only results in
requested in the first review was for the agent to build an
                                                                         fewer lines of code, but more importantly, is much easier
API for Sheaf.H and to not unfold its definition in down-

                                                                     5
                                                    Sorries Are Not the Hard Part




Figure 4. Tool calls across the project (19,393 total). Left: top 20 tools by call count, dominated by shell/file operations (Bash, Read,
Edit, Grep) and Lean LSP queries. Right: daily tool calls grouped by category, phase shading as in Figure 1. Proof construction
leans on Lean LSP diagnostics, goal queries, and library search; the review response is dominated by repository edits, shell checks, and
grep-style audits — visibly different workflows on the same Lean tree.


for future users to build off of.                                      The review also prompted the agent to try and identify where
                                                                       these kinds of generalizations would make its code more
The reviewer also requested the agent build an API for
                                                                       useful and cleaner. Aside from a few artificial changes,
topologicalKrullDim. This was also defined in
                                                                       the agent was not able to identify and correct any of these
mathlib but did not have an API for it yet. This defini-
                                                                       generality mistakes without them being requested. Much
tion is much simpler than that of cohomology and the agent
                                                                       like with the definitions problems, the agent struggles to
did a much better job with it. It is still not at the level
                                                                       make decisions that have a global effect on the project and
of mathlib quality but it is much closer than the majority
                                                                       is much better suited for dealing with local problems.
of machine-generated code. This is a good sign that the
agent is capable of good design given sufficiently specific            Lean code of the type produced in this project, with an
prompting.                                                             excess of specific lemmas and definitions, can still be useful
                                                                       to a search-heavy repository of generated results. In such
                                                                       a repository, an agent can sift through excess statements
Theorem statements improved more reliably. The re-                     and find a useful fact. It is not useful to a human curated
sponse was much better at fixing local problems. The review            library like mathlib, where users need a smaller and more
had a number of specific requests for generalizations of the-          intentional theorem surface.
orems. In particular, state A had a number of theorems
that had the hypothesis “let S be a short exact sequence
                                                                       Proofs improved, but unevenly. The proof terms in state
coming from an injective presentation” while the statements
                                                                       B are better than in state A. There are fewer walls of inter-
were all true under the simpler hypothesis “let S be a short
                                                                       mediate have statements, less definitional-equality abuse,
exact sequence”. The agent had no problem making these
                                                                       more named intermediate lemmas replacing long unreadable
changes.
                                                                       proofs, and less direct unfolding of definitions. In general,
In state A, there were a number of cases where the agent               the proofs that only used objects defined in mathlib were
tried to prove “x = y”, then realized it would be easier to            much cleaner, as the agent was able to rely on the good API
just prove “if x = 0 then y = 0” since that turned out to be           built in mathlib. The proofs that used definitions made by
all it needed for the rest of the proof. This method of taking         the agent were extremely bad in state A and were notice-
the path of least resistance makes sense when generating               ably better in state B after the APIs for Krull dimension
sorry-free code is the only goal but does not lead to useful,          and cohomology were built. Some of the more technical
reusable code. This was pointed out in the review and it was           proofs remained bad, for example, the filtered-colimit files
fixed in state B. Even in cases where this change required a           remained hard to read because they contain a dozen hyper-
large refactor, the agent was able to fix them.                        specific definitions that are only useful in this one proof.

                                                                   6
                                                 Sorries Are Not the Hard Part

In some ways, the proof terms themselves are the least                In some cases, the agent made a choice that clearly went
important part, as they are erased at runtime. There are              against previous design decisions. Sheaf cohomology is de-
performance and maintainability concerns however. Long                fined as a type, as opposed to a term of AddCommGrpCat.
tactic blocks can create performance failures, and fragile            Both choices have their benefits, but choosing to go with
definitional-equality arguments are sensitive to breaks from          the former was a deliberate design decision informed by
changes upstream. The project history shows a recurring pat-          considering all future applications. The agent chose to
tern: when a proof became too expensive to check, progress            define sheafH_succ_map as a morphism between the
improved only after the goal was decomposed into named                AddCommGrpCat versions of cohomology. This is not a
sublemmas rather than pushed through a larger heartbeat               bad definition in principle but it clearly goes against a previ-
allowance. That lesson is not specific to this theorem. It is         ous design decision and working with both adds work that
the software-engineering version of a mathematical norm:              is not needed.
if a proof has a meaningful intermediate claim, name it and
                                                                      Some definitions, like familyMap and familyImage
make later maintenance depend on that claim.
                                                                      are just silly. The definition of familyMap f is just
                                                                      Sigma.desc f so this definition saves exactly one
More definitions as examples. As mentioned above, def-                character of typing and does nothing else. Similarly,
                                                                      TopologicalSpace.IrreducibleCloseds.height is just defined
initions are the most important thing to get right and are
where the agent struggled the most. We will give some                 to be Order.height. This one has some use, as it allows
specific examples of the kinds of mistakes the agent made             the dot notation when working with irreducible closeds.
that it was unable to correct even after being prompted.              However, because it chose to make it a def instead of
                                                                      an abbrev, all of the theorems in mathlib proven about
The      worst       offender      is      the       definition       Order.height will not be usable with it unless it is ex-
sheafH_filtered_colimit_h1_sectionsFunctor.          This defi-       plicitly unfolded, which is exactly what the agent does when
nition is equivalent to sheafSections, a definition                   it uses it.
available in mathlib, and has nothing to do with sheafH,
filtered colimits, or H1. The naming is likely because of the
                                                                      Why feedback adaptation is uneven. The successful re-
particular use case the agent had for this definition. Creating
                                                                      view items had crisp completion predicates: no remaining
superfluous definitions like this is not just unnecessary,
                                                                      uses of an old name, a file renamed, a theorem statement
it can be actively harmful to future development. For
                                                                      generalized, a wrapper deleted, or a stronger isomorphism
example, if an instance is put onto this definition, say
                                                                      available at a call site. The failed items required counter-
an instance of it being an additive functor, then even if
                                                                      factual judgment. A good definition is good because future
sheafH_filtered_colimit_h1_sectionsFunctor is shown to
                                                                      developments can use it without transport pain. A good
be equal to sheafSections (which it is), the instances
                                                                      API is good because it contains the right small set of lem-
will likely not be definitionally equal. This leads to some
                                                                      mas, including lemmas whose need has not yet appeared.
of the most confusing errors in Lean, where you can
                                                                      The agent optimized for the next compiling proof, but was
rewrite sheafH_filtered_colimit_h1_sectionsFunctor into
                                                                      unable to make good long-term decisions.
sheafSections but since the instances don’t agree
definitionally, everything will break.
                                                                      Prompts had to forbid escape hatches. A recurring fail-
Some other       bad examples         came from equiv-                ure mode during long autonomous runs was loop drift to-
alences the      agent defined.            The definitions            ward declaring a task “blocked” or pinning a failure on
extClass_postcompAddEquiv_of_subsingleton_middle,                     infrastructure (“genuine mathlib gap”). The drift was fast
sheafH_extClassAddEquiv_of_subsingleton_middle,           and         and consistent enough that the project’s slash-command
sheafH_succ_iso_of_subsingleton_middle are all roughly “in            prompts explicitly forbade both phrases — “You are NOT
this hyper-specific case, this function is bijective, so here         allowed to say that you are blocked. You MUST close the
it is as an Equiv”. The correct thing to do here is just              sorrys yourself!” and “A no-op cycle is never acceptable.”
prove the function is bijective and use that. Anytime an              When an agent has a verbal escape hatch, it will reach for
equiv is needed, Equiv.ofBijective can be inlined.                    it before it reaches for a decomposition; the gate partially
The problem with making them definitions is that this                 removes the escape hatch.
essentially creates a barrier between the user and the actual
function they should be working with, with no real upside.
                                                                      Human feedback as a specification. The review sup-
sheafH0EquivSections                                 and              plied the quality specification the automated loop otherwise
sheafH0NatIsoSections are essentially the                             lacked. “Build a useful cohomology API” reads like a pro-
same definition under different names, it should be clear             gramming task but is really a design task, and a loop can
why this is a bad thing.                                              satisfy every local complaint while still producing an inter-

                                                                  7
                                                Sorries Are Not the Hard Part

face that is too broad, too specific, or too hard to navigate.       dataset at https://huggingface.co/datasets/
The division of labor follows: expert reviewers should spend         uw-math-ai/grothendieck-vanishing-logs.
their scarce attention on definitions, theorem surfaces, and
global organization, and hand agents the narrow refactors            Acknowledgements
that carry an explicit completion predicate.
                                                                     This work used computational resources from the Hyak
Gates are only as good as their target. The two loops                high-performance computing cluster at the University of
shared the worker/evaluator structure but had different re-          Washington. The AI subscription was funded by the UW
ward signals. The compression loop reduced normalized                Math AI Lab. We thank the mathlib community, whose li-
LOC under a compilation gate: a clean mechanical signal,             brary and conventions defined the standard of quality against
which made the loop a reliable optimizer but only loosely            which this formalization was reviewed.
aligned with review intent. The refactor loop had to oper-
ationalize natural-language review items, and its evaluator
could report progress as strong, partial, or absent without
ever being sure a broad review item was truly satisfied. The
lesson is that a mechanical gate is powerful when it matches
the quality target and dangerous when it is only a proxy.
Compilation gates are correctness gates; LOC and dead-
code gates are maintenance proxies; review-item checklists
are alignment proxies. None of them measures whether the
public definitions are the ones a future formalizer would
choose — exactly the gap between state A and the first
review.

External proving as a bounded tool. Aristotle submis-
sions are local assistance, not an autonomous strategy en-
gine. Successful calls closed bounded lemmas; disproven
calls were informative because they falsified incorrect lem-
mas. But the hard project decisions — which intermediate
statements should exist, which definitions should be public
— were never theorem-prover queries.

5. Conclusion
Without a sophisticated harness, LLMs are very capable
of closing proofs and local changes, but cannot yet make
the global design decisions that a reusable formalization
requires. Choosing good definitions and building a good
API remain the biggest barriers. We suggest a practical
evaluation standard for AI-for-math systems: after the proof
checks, ask an expert to review the public definitions, theo-
rem statements, namespaces, and API surface, then measure
how well the system responds.

Code and Data Availability
The Lean 4 formalization is available at https:
//github.com/Vilin97/Clawristotle/tree/
main/grothendieck-vanishing. The two expert
reviews and the structured process logs analyzed in this
paper—per-turn token usage, the refactor and compression
loop histories, per-commit LOC and sorry counts, the
agent tool-use timeline, Aristotle proving jobs, the human
prompts, and the loop prompts—are released as a public

                                                                 8
                                                Sorries Are Not the Hard Part

References                                                             Foundations of Software Engineering. ACM, 2023. doi:
                                                                       10.1145/3611643.3616243.
Achim, T., Best, A., Der, K., Fédérico, M., Gukov, S.,
  Halpern-Leistner, D., Henningsgard, K., Kudryashov, Y.,            Hartshorne, R.    Algebraic Geometry, volume 52
  Meiburg, A., Michelsen, M., Patterson, R., Rodriguez, E.,            of Graduate Texts in Mathematics.        Springer,
  Scharff, L., Shanker, V., Sicca, V., Sowrirajan, H., Swope,         1977.     doi: 10.1007/978-1-4757-3849-0.     URL
  A., Tamas, M., Tenev, V., Thomm, J., Williams, H., and               https://link.springer.com/book/10.
 Wu, L. Aristotle: IMO-level automated theorem prov-                   1007/978-1-4757-3849-0.
  ing, 2025. URL https://arxiv.org/abs/2510.
  01346.                                                             Ilin, V. Semi-autonomous formalization of the Vlasov-
                                                                        Maxwell-Landau equilibrium, 2026. URL https://
Bayer, J., David, M., Hassler, M., Matiyasevich, Y., and                arxiv.org/abs/2603.15929.
  Schleicher, D. Diophantine equations over Z: Universal
  bounds and parallel formalization, 2025. URL https:                Ju, H., Gao, G., Jiang, J., Wu, B., Sun, Z., Chen, L., Wang,
  //arxiv.org/abs/2506.20909.                                          Y., Wang, Y., Wang, Z., He, W., Wu, P., Xiao, L., Liu, R.,
                                                                       Dai, B., and Dong, B. Automated conjecture resolution
Chen, E., Cummins, C., Eltschig, B., Grubisic, D., Haller, L.,         with formal verification, 2026. URL https://arxiv.
  Hong, L., Kurghinyan, A., Lau, K., Leather, H., Lee, S.,             org/abs/2604.03789.
  Markosyan, A., Ono, K., Patel, M., Pendharkar, G., Rathi,
  V., Schneidman, A., Seeker, V., Sengupta, S., Sinha, I.,           Klingner, T., Bladek, D., Crawford, E., Chen, B., Fu, A.,
  Xin, J., and Zhang, J. Almost all primes are partially               Nair, K., Alper, J., Inchiostro, G., and Ilin, V. Evaluation
  regular, 2026a. URL https://arxiv.org/abs/                           of LLMs for mathematical formalization in Lean, 2026.
  2602.05090.                                                          URL https://arxiv.org/abs/2606.05632.

Chen, E., Cummins, C., GSM, Grubisic, D., Haller, L.,                Liu, J., Zhou, Z., Zhu, Z., Dos Santos, M., He, W., Liu, J.,
  Hong, L., Kurghinyan, A., Lau, K., Leather, H., Lee, S.,             Wang, R., Xie, Y., Zhao, J., Wang, Q., Zhi, L., Li, J., and
  Markosyan, A., Ono, K., Patel, M., Pendharkar, G., Rathi,            Li, W. Numina-lean-agent: An open and general agentic
  V., Schneidman, A., Seeker, V., Sengupta, S., Sinha, I.,             reasoning system for formal mathematics, 2026. URL
  Xin, J., and Zhang, J. Fel’s conjecture on syzygies of               https://arxiv.org/abs/2601.14027.
  numerical semigroups, 2026b. URL https://arxiv.
                                                                     LM-Provers, Qu, Y., Setlur, A., Dekoninck, J., Beeching, E.,
  org/abs/2602.03716.
                                                                      Li, J., Wu, I., Tunstall, L., and Kumar, A. QED-Nano:
Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie,               Teaching a tiny model to prove hard theorems, 2026. URL
  A., Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J.,            https://arxiv.org/abs/2604.04898.
  Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang,               Petrov, I., Dekoninck, J., Dimitrov, D. I., and Vechev, M.
  Z., Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H.,              Not all proofs are equal: Evaluating LLM proof qual-
  and Yang, F. Seed-prover: Deep and broad reasoning                   ity beyond correctness, 2026. URL https://arxiv.
  for automated theorem proving, 2025. URL https:                      org/abs/2605.10379.
  //arxiv.org/abs/2507.23726.
                                                                     Rammal, A., Patel, N., Gloeckle, F., Hayat, A., Kempe, J.,
de Moura, L. and Ullrich, S. The lean 4 theorem                        Munos, R., Arnal, C., and Cabannes, V. Formalizing
  prover and programming language. In Automated De-                    mathematics at scale, 2026. URL https://arxiv.
  duction – CADE 28. Springer, 2021. doi: 10.1007/                     org/abs/2605.29955.
  978-3-030-79876-5 37. URL https://doi.org/
  10.1007/978-3-030-79876-5_37.                                      The mathlib Community. The lean mathematical library.
                                                                       In Proceedings of the 9th ACM SIGPLAN International
de Moura, L., Kong, S., Avigad, J., van Doorn, F.,                     Conference on Certified Programs and Proofs, pp. 367–
  and von Raumer, J. The lean theorem prover (sys-                     381, 2020. doi: 10.1145/3372885.3373824.
  tem description). In Automated Deduction – CADE-
  25, pp. 378–388. Springer, 2015. doi: 10.1007/                     Tooby-Smith, J. Formalizing the stability of the two Higgs
  978-3-319-21401-6 26. URL https://doi.org/                           doublet model potential into Lean: Identifying an error
  10.1007/978-3-319-21401-6_26.                                        in the literature, 2026. URL https://arxiv.org/
                                                                       abs/2603.08139.
First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:
  Whole-proof generation and repair with large language              Urban, J. 130k lines of formal topology in two weeks:
  models. In Proceedings of the 31st ACM Joint European                Simple and cheap autoformalization for everyone?, 2026.
  Software Engineering Conference and Symposium on the                 URL https://arxiv.org/abs/2601.03298.

                                                                 9
                                              Sorries Are Not the Hard Part

Wang, E., Chess, S., Lee, D., Ge, S., Mallavarapu, A.,
 Alper, J., and Ilin, V. Learning to repair Lean proofs
 from compiler feedback, 2026. URL https://arxiv.
 org/abs/2602.02990.
Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
 nik, M., and Szegedy, C. Autoformalization with large
 language models. In Advances in Neural Information
 Processing Systems, 2022.
Xie, Z., Liu, X., and Zhang, S. MathlibPR: Pull request
  merge-readiness benchmark for formal mathematical li-
  braries, 2026. URL https://arxiv.org/abs/
  2605.07147.

Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu,
  S., Godil, S., Prenger, R., and Anandkumar, A. Lean-
  Dojo: Theorem proving with retrieval-augmented lan-
  guage models. In Advances in Neural Information Pro-
  cessing Systems, 2023. URL https://arxiv.org/
  abs/2306.15626.
Zhang, Y., Sun, Y., Suzuki, T., Lee, J. D., and Liu, F.
  LeanMarathon: Toward reliable AI co-mathematicians
  through long-horizon Lean autoformalization, 2026. URL
  https://arxiv.org/abs/2606.05400.




                                                              10
                                                 Sorries Are Not the Hard Part

A. Additional Figures
This appendix collects diagnostic material that helps audit
the case study but is too detailed for the main argument: a
per-cycle view of loop effectiveness, and the final import
graph of the Lean development.

Loop effectiveness. The loop-effectiveness plot gives a
per-cycle view of the refactor and compression loops. Refac-
tor cycles are scored by progress and task-completion status,
compression cycles by LOC delta, which is why the two
loops should not be compared as if they shared an objective:
one was interpreting a natural-language code review, the
other optimizing a mechanical signal. The plot also shows
why the paper does not treat cycle count as evidence of
quality by itself — some stretches are productive, others are
repeated low-value attempts.




Figure 5. Per-cycle refactor and compression outcomes summariz-
ing loop behavior across the project.


Import graph. The import graph records the final or-
ganization of the Lean development. Many review com-
                                                                       Figure 6. Import graph for the Grothendieck-vanishing Lean files.
plaints were about where concepts lived rather than about
isolated proof terms, so the organization is itself a result.
The intended reading is bottom-up: dimension, zero-outside,
flasque, closed-immersion, filtered-colimit, and generated-
subsheaf infrastructure feed the irreducible step and then the
main theorem. A future user navigates this artifact through
imports and namespaces before reading any proof, which is
why file naming carried weight in the review.




                                                                  11
