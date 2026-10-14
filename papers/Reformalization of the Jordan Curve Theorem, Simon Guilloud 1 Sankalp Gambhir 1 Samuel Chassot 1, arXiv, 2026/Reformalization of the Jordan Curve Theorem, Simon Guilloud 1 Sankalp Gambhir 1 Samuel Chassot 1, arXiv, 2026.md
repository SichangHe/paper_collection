                                                                  Reformalization of the Jordan Curve Theorem


                                                                        Simon Guilloud 1 Sankalp Gambhir 1 Samuel Chassot 1


                                                                Abstract                                     restricted to transfers between systems with very similar
                                                                                                             foundations, transfers from a simpler system to a more
                                             We present a case study in reformalization, a                   complex system (for example, (Blanqui, 2024; Keller &
                                             variant of autoformalization in which the input                 Werner, 2010)), or translations with large complexity and
                                             proof is not natural language but a formal de-                  proof-size overhead, as in (Guilloud et al., 2024).
arXiv:2607.01734v1 [cs.AI] 2 Jul 2026




                                             velopment in a different proof assistant. Con-
                                             cretely, we report three reformalizations of the                The second obstacle is that, even when technically feasi-
                                             Jordan Curve Theorem: from Mizar to Lean,                       ble, the resulting translation is unnatural. In particular, the
                                             from HOL Light to Lean, and from HOL Light                      translation of a concept often does not match the way that
                                             to Agda. We analyse the results and identify                    concept is defined in the target assistant. This is the problem
                                             pipeline design choices that matter for practi-                 of library alignment. For example, in a transfer of HOL
                                             cal reformalization tasks. The final formaliza-                 Light proofs into Lean, the natural numbers N as defined
                                             tions are available at https://github.com/                      in HOL Light and translated into Lean yield a definition
                                             epfl-lara/jordan-curve-theorem.                                 of N that is not only different from Lean’s inductive type
                                                                                                             N, but possibly not even provably equivalent to it in Lean.
                                                                                                             The usual solution is manual alignment of concepts, which
                                                                                                             restricts the use of each translated concept to a particular
                                        1. Introduction                                                      API1 .
                                        Much attention has been given to the problem of autoformal-          In mathematical research, however, and with the exception
                                        ization: given a mathematical text in natural language (such         of a few peculiar domains, it is widely understood that the
                                        as a paper or textbook), produce a corresponding formaliza-          particular choice of logical foundations matters little: in
                                        tion in a proof assistant. Much less attention has been given        principle, a mathematical proof can be carried out “natu-
                                        to the simpler but still highly useful question of formalizing       rally” in any proof system with sufficient background. In
                                        a mathematical theory not from an informal proof, but from           that regard, the two problems above are artefacts of trans-
                                        a development in a different proof assistant. We call this           lations that must be deterministic, complete, and correct
                                        task reformalization.                                                by construction, but that cannot preserve the spirit of the
                                        Automated proof transfer, which translates proofs across             original proof. LLM-based proof transfer is the opposite:
                                        proof systems, has long been a research topic in the ITP             it is not deterministic, complete, or correct by construc-
                                        community (Kohlhase & Rabe, 2021; Anonymous, 1994).                  tion, but it can preserve the proof idea and thereby largely
                                        Before recent progress by LLMs in formal mathematics, the            avoid the two obstacles above. This is the rationale behind
                                        main viable approach was low-level logical translation of            reformalization.
                                        statements and proofs. Many approaches were developed                In the present work, we show through a case study that
                                        over the years, but they face two fundamental obstacles.             suitable agentic pipelines combined with large language
                                        First, a mismatch between logical foundations (for example,          models can transfer large mathematical developments across
                                        dependent type theory, higher-order logic, or set theory) is         entirely different proof assistants. Concretely, we consider
                                        difficult to overcome. Even when the logical foundations             the Jordan Curve Theorem (JCT) as our main study. The
                                        are provably equivalent, existing approaches are typically           JCT states that any non-self-crossing closed curve separates
                                           All authors contributed equally.   1
                                                                                École Polytechnique         the plane R2 into two disjoint regions – a bounded interior
                                        Fédérale de Lausanne (EPFL), Lausanne, Switzerland. Cor-           and an unbounded exterior – and was proven by Camille
                                        respondence to: Simon Guilloud <simon.guilloud@epfl.ch>,                1
                                        Sankalp Gambhir <sankalp.gambhir@epfl.ch>, Samuel Chassot                For example, in set theory, 0 is often defined as the empty set
                                        <samuel.chassot@epfl.ch>.                                            ∅. But the theorem 0 = ∅ certainly cannot hold (or even be stated)
                                                                                                             about the number 0 as defined in, e.g., Lean. Such “accidental”
                                        Proceedings of the 43 rd International Conference on Machine         theorems cannot be used in a translation that maps the set N to the
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026         Lean type N.
                                        by the author(s).

                                                                                                         1
                                                      Autoreformalization

Jordan in 1887. It is a famous example of an apparently               tion of the theorem and a highly detailed, guaranteed-correct
obvious theorem whose proof is long and technical, and it             proof. The LLM-based agent uses this specification together
has important applications.                                           with the target assistant’s libraries, search tools, and a verifi-
                                                                      cation loop to construct a native development for the target
The first formalization of the JCT was finished in 2005 by
                                                                      proof system.
Hales (Hales, 2007) in the HOL Light proof assistant (Har-
rison, 2009), in a proof of roughly 60,000 lines. In the same
                                                                      Scope of the task. Our case study focuses on the Jordan
year, an international team finished another formalization of
                                                                      Curve Theorem and its supporting infrastructure. This is a
the theorem in the Mizar proof assistant (Korniłowicz, 2007).
                                                                      useful stress test for reformalization for three reasons. First,
The JCT proof effort in Mizar spread over 14 years and, be-
                                                                      the statement of the theorem only requires real numbers and
cause of the attraction of the problem and the tendency of
                                                                      continuous functions, and hence can be stated directly in all
those who undertake it to disappear, has been described as
                                                                      the assistants we consider. Second, the proof developments
a black hole into which formalizing mathematicians fall,
                                                                      are large and technically heterogeneous, mixing topology,
never to be seen again. Although Hales was faster, he still
                                                                      geometry, graph arguments, and analytic lemmas. Third,
describes his formalization effort as having taken “many
                                                                      mature source formalizations exist in more than one assis-
months of hard work”. With an existing formal proof as
                                                                      tant, allowing us to compare reformalization across different
baseline, manually porting the proof to a different proof
                                                                      source languages and libraries.
assistant would take less time, perhaps “a few” months of
hard work. In contrast, the reformalizations in the present           For each case study, the setup consists of:
case study produced JCT formalizations in about a week,
with no more than two days of active human involvement                   • a source formalization of the Jordan Curve Theorem,
and using commercially available LLMs. This demonstrates
that practical proof transfer is now feasible at scale.                  • a target assistant together with its standard library and
                                                                           existing ecosystem tools, and
In the rest of the paper, we present three reformalizations of
the JCT: from Mizar to Lean, from HOL Light to Lean, and                 • an agentic pipeline combining an LLM, tool use, and
from HOL Light to Agda. Lean (de Moura et al., 2015) was                   human-written prompts and directives.
chosen for its well-developed ecosystem of tooling and the
Mathlib (The mathlib Community, 2020) library, and Agda               Human role. No proof code was written by hand, and
(Norell, 2007) was chosen as an example of a proof assistant          no mathematical insight or proof guidance was given to
with similar foundations, but less developed tooling in com-          the agent. Human input was used to configure the work-
parison, to test the impact of the prover’s ecosystem. For            flow: prompts were revised, additional verification steps
each, we present the pipeline and report the design choices           were inserted, and observed failure patterns were used to im-
that affected the agent’s performance. We then compare the            prove the process. This is precisely the kind of engineering
three reformalizations to evaluate how much the source and            experience we want to surface in the paper.
target proof assistants, and in particular their foundations
and tooling, matter for practical reformalization.                    Evaluation goals. Our evaluation is designed to answer
The formalizations are available together under an Apache             three questions. First, can current LLM-based pipelines
2.0 licence at https://github.com/epfl-lara/                          transfer a large, nontrivial formalization across proof as-
jordan-curve-theorem.                                                 sistants while keeping human effort low? Second, which
                                                                      factors most affect practical success: the quality of the tool-
                                                                      ing of source and target assistants, the maturity of their
2. Reformalization Task and Evaluation Setup                          libraries, the nature and mismatch of their logical founda-
We use the term reformalization for the following task:               tions, the model used, or the design of the agentic pipeline?
given an existing formal development establishing a state-            Third, what are good agentic pipelines and guardrail designs
ment T , produce a new, independently checkable formal                for reformalization?
development in a different target proof assistant that estab-
lishes the corresponding claim T ′ . In contrast to correct-by-       Measured quantities and reported observations. A re-
construction proof translation, our goal is not to preserve           formalization counts as a verified success if the resulting
source syntax, proof terms, or definitional equality, but to          target development is fully verified in the target assistant
recover in the target assistant a proof development that is           (without sorry placeholders or additional axioms) and es-
mathematically faithful to the source and idiomatic with              tablishes the final Jordan Curve Theorem statement. For
respect to the target. Hence the source formalization is not          each reformalization, we first give a qualitative experience
treated as an object to be compiled, but as an exact specifica-       report centred on pipeline design. In particular, we empha-
                                                                      size the practically useful lessons we learned about how to

                                                                  2
                                                    Autoreformalization

structure the workflow, where agents fail, and which design         Step 3: Proof Filling. The agent was finally instructed
choices and guardrails make reformalization succeed.                to fill in the proof of each theorem, utilizing the metadata
                                                                    and Mizar sources. The Mizar source provided the proof
We then complement this experience report with quantitative
                                                                    sketch, while the metadata provided a closed set of lemmas
descriptors: estimated human involvement time, size of the
                                                                    that could be used in the proof. The agent was instructed
resulting development (number of theorems, number of
                                                                    to delegate to Mathlib whenever the closest match found in
lines, number of tactics), compilation time, the proportion
                                                                    the previous step was sufficient to close the goal.
of the original proof that was already present in the target
assistant’s library versus the part that had to be actively         Despite the metadata and source links, the agent sometimes
formalized, the number of active days needed to complete            diverged by attempting to write a proof sketch from scratch,
the project, and approximate LLM cost. These metrics are            particularly following a context-window summarization. In
admittedly imperfect – proof size is a mediocre proxy for           this case, the agent was manually steered to refer to the
complexity, and time and cost are largely vendor-dependent          Mizar sources. This occurred approximately 10 times over
– so they should not be understood as a definitive benchmark,       the course of the formalization, but otherwise no mathemat-
but rather as supporting context for the qualitative report.        ical guidance was provided.
                                                                    Progress was tracked through a status file auto-generated us-
3. JCT: Mizar to Lean                                               ing a script filtering the Lean build output, and a markdown
                                                                    file containing a human-readable formalization plan, which
The reformalization of JCT from the Mizar Mathematical
                                                                    the agent was instructed to update after each completed
Library (MML) was conducted in three distinct steps: (1)
                                                                    theorem.
extraction of dependency information, (2) construction of
a proof sketch and library alignment, and (3) proof fill-
ing. We used both the original Mizar tool (Naumowicz                3.1. Results
& Kornilowicz, 2009) and the mizar-rs proof checker                 The final Lean development contains 413 lemmas and the-
reimplementation (Carneiro, 2023).                                  orems, spanning approximately 474,000 characters (about
                                                                    11,000 lines). In comparison, the source Mizar development
                                                                    (restricted to JORDAN*, BROUWER*, and BORSUK*) spans
Step 1: Extracting Metadata. The Mizar proof checker                approximately 775,000 characters (about 23,500 lines). The
is not a single tool, but rather a collection of tools that         difference in size can be largely attributed to lemmas be-
execute separately at different stages and exchange data            ing discharged by close matches in Mathlib. The project
through standardized intermediate text formats. Unlike a            compiles in 111s (wall-clock time for lake build), with
closed environment where proof data is stored entirely in           Mathlib cached.
memory, the text formats enable independent processing
                                                                    The full formalization took about 10 days to complete, using
and analysis of the proof data.
                                                                    Claude Opus 4.6 and GPT-5.4 via GitHub Copilot. We
We used the intermediate files generated by a successful run        estimate the human involvement, which consisted of setting
of the proof checker to extract dependency graphs between           up the project, monitoring progress, and steering the agent,
source files as well as theorems in the development leading         at about 20 hours.
to the final Jordan Curve Theorem statement.
                                                                    Divergence from Mizar. Because the pipeline prioritized
                                                                    existing Mathlib lemmas whenever they were sufficient,
Step 2: Proof Sketch and Library Alignment. The de-                 the resulting Lean development did not always reproduce
pendency graph and MML sources were provided to an                  Mizar’s internal proof machinery. The overall structure of
agent with instructions to produce one Lean file per Mizar          the Jordan Curve Theorem argument remained close to the
source file, translating Mizar theorems into Lean theorem           source, but several intermediate constructions were replaced
skeletons, and inserting comments with the original Mizar           by more idiomatic Mathlib-based reasoning. In particular,
source element, location, and the theorems and lemmas used          substantial parts of the Mizar Go-board proof engineering
in the current theorem’s proof.                                     were no longer needed, as equivalent topological results
                                                                    were already available in Mathlib.
In a second pass, the agent was instructed to augment the
metadata with the closest matching theorems existing in
Mathlib for each component imported from Mizar.                     4. JCT: HOL Light to Lean
The resulting statement of the Jordan Curve Theorem was             In contrast with the Mizar-to-Lean formalization, the formal-
then manually verified to be correct and to only rely on            ization from HOL Light to Lean was linear. The HOL Light
definitions from Mathlib.                                           proof of the Jordan Curve Theorem is split into 30 sections

                                                                3
                                                     Autoreformalization

(labelled A to DD). The agent was tasked with working                section because a theorem was missing or a key lemma had
section by section and theorem by theorem, without comput-           a weaker statement than its HOL Light counterpart.
ing a dependency graph or prereading future sections. The
                                                                     This motivated strict maintenance of the CSV catalogue,
agent’s workflow for each section was set up as follows:
                                                                     and the agent was given a strict directive to implement every
                                                                     theorem that was not in Mathlib or made trivial by Lean
 1. Populate a catalogue of HOL Light theorems and defi-             type checking.
    nitions with a dedicated script.
 2. Build a Lean skeleton of theorems and definitions, us-           Fill proofs. The agent is then tasked with filling proofs
    ing sorry placeholders for proofs.                               one by one, in order. It always has to first read the HOL
                                                                     Light proof to understand the strategy, and then implement
 3. Fill all sorries one by one, in order, building between          it using the already formalized theorems and definitions. It
    each.                                                            builds and verifies compilation before moving to the next
                                                                     sorry, and was explicitly forbidden to work on multiple
 4. Once the file is sorry-free and compiles cleanly, up-
                                                                     proofs at once.
    date the catalogue with the corresponding Lean theo-
    rem and update the status document.                              Longer proofs in HOL Light often triggered the agent to
                                                                     search for shortcuts: its visible behaviour suggested an aver-
 5. Read the instruction file again and move on to the next
                                                                     sion to long, complicated tasks. But the resulting search
    section.
                                                                     for a shorter proof typically took much longer than the time
                                                                     required to transport the proof as-is. Hence, the agent was
Populate the Catalogue. After reading a status file to               given the guideline to always strictly follow the HOL Light
confirm the project’s state and current section, the agent           proof and not to search for shortcuts. It was also told that
executes a dedicated Python script that extracts all theorems        the HOL Light proofs were already optimized and that the
and definitions from a given section of the HOL Light proof          important thing was to keep making progress. Limiting
and adds them to a CSV catalogue. Each entry contains the            the agent’s “creative freedom” and imposing formal, me-
theorem’s name, its section, its kind (definition or theorem),       chanical bookkeeping made the process much smoother and
its formal statement, and whether it is used beyond the              faster.
section itself or only locally. Columns for the corresponding
Lean statements are filled afterwards.                               Verify and advance. Finally, once the file compiles, con-
                                                                     tains no remaining sorry placeholders, and only uses stan-
Write the Skeleton. The agent must then write a skele-               dard axioms, the agent should update the CSV and the status
ton of the section in a Lean file, with sorry placeholders           file, then move on to the next section.
for each theorem. Every theorem or definition has to be
classified in one of the following three categories:                 After completion, we manually verified that the proven state-
                                                                     ment was indeed a correct formalization of the JCT and then
   • Exists in Mathlib. The theorem is covered by an ex-             had the agent proof-golf, refactor, and improve the quality of
     isting theorem from Mathlib. The agent must add the             the development. We used a second agent, a Lean reviewer
     theorem name in Mathlib to a dedicated column in the            given Mathlib’s guidelines for PR quality, and had the two
     CSV.                                                            agents engage in a few rounds of proof improvement.

   • Not applicable to Lean. Some theorems genuinely do              4.1. Results
     not apply in Lean, typically because they are immediate
     by type-checking. This must also be recorded in the             The final Lean formalization comprises close to 1,400,000
     CSV.                                                            characters (29,000 lines), against 1,709,000 characters
                                                                     (59,000 lines) in the HOL Light proof. It contains more
   • Must be implemented. The theorem or definition must             than 910 theorems and lemmas and 150 definitions. Of
     be implemented. The theorem name in Lean and its                these, 116 have no equivalent in HOL Light: they are helper
     file and line numbers must be updated in the CSV.               lemmas or formalize statements from the HOL Light library
                                                                     that did not exist in Mathlib. On the other hand, 258 state-
In early exploration, the agent was given less strict guide-         ments from the HOL Light proof were already in Mathlib,
lines. It sometimes decided that a theorem could be skipped,         and 213 are classified as “not applicable to Lean”. We ob-
for example because the proof was simple and could be                serve that, once corrected for the difference in theorems on
inlined, or because it had found a way to carry the proof            each side, the number of characters in each proof is quite
without using the theorem. However, on multiple occasions            similar, meaning that both proofs are similarly verbose in
this led the agent to become stuck on a theorem in a later           their respective languages. The project takes 206s to com-

                                                                 4
                                                     Autoreformalization

pile (wall-clock time for lake build).                               from the executable as successful type checking, while Agda
                                                                     had in fact been killed by the operating system for running
The full formalization took a week to complete, using
                                                                     out of memory (OOM). The human operator had to point this
Claude Opus 4.6 via GitHub Copilot. We estimate the total
                                                                     out before the agent understood the failure mode and took
active human involvement at about 10 hours; this consisted
                                                                     action. Fixing the proofs to type check within the available
of setting up the project and the agentic pipeline, as well as
                                                                     memory took days. The Agda type checker was running for
monitoring the agent’s progress. The pipeline first evolved
                                                                     5 to 10 minutes before being killed by the operating system,
according to observations of the walls the agent encountered.
                                                                     which prevented fast agent turnaround. The agent finally
However, from around the middle of the formalization (sec-
                                                                     succeeded by splitting the proofs into chunks small enough
tion N), no further modifications were needed, and the agent
                                                                     to type check within the available memory. During this
completed the second half entirely autonomously.
                                                                     process, we also updated the instructions to force the agent
                                                                     to use Agda’s cached interfaces to speed up type checking
5. JCT: HOL Light to Agda                                            of subsequent chunks. Using the cache was particularly
                                                                     critical given the runtime of the type checker on the most
To evaluate the importance of the target proof assistant
                                                                     demanding proof chunks.
in such agent-based proof translation, we apply the same
approach to port the Jordan Curve Theorem proof to
Agda (Norell, 2007) from HOL Light.                                  5.1. Takeaways

We used the same protocol as for the Lean target, explained          The Agda experiment suggests that the target assistant’s
in Section 4. We adapted the instructions to target Agda             operational characteristics matter as much as its founda-
instead of Lean and to use the appropriate terminology.              tions. The main technical mismatch with HOL Light was
We used Claude Opus 4.7 via Claude Code CLI for this                 not only the difference between higher-order logic and de-
instruction adaptation and for the formalization itself.             pendent type theory, but also the need to make HOL Light’s
                                                                     inhabited-type discipline explicit. The main tooling issue
At the time of writing, the Agda formalization is not com-           was turnaround time: once type checking required minutes
plete. Section 0 (i.e., the foundations), as well as Sections        and could fail by OOM without a clear diagnostic to the
A to D and around half of section E are ported and compile.          agent, progress slowed sharply. For Agda, robust refor-
This amounts to around 27,000 lines of Agda code. As the             malization pipelines should therefore make non-emptiness
main theorem is not ported yet, we cannot confidently assess         assumptions explicit, avoid unnecessary axiomatization
the correctness of the proof porting. We therefore report on         when possible, split developments aggressively, and enforce
the experience in setting up such experiments with Agda,             cached type-checking workflows from the beginning.
and lessons we learned while doing so.
                                                                     To make the most out of the LLM agents, the verifica-
                                                                     tion/compilation process should be as fast as possible.
Empty types. At the beginning of Section 0, the agent                This takeaway is not exclusive to LLM agents as human
asked the human operator multiple questions regarding                users also benefit from fast verification. However, LLM
empty types. In HOL Light, types are strictly inhabited,             agents tend to follow a trial-and-error approach with fast
while in Agda types can be empty. The main consequence,              turnaround to writing proofs.
as the agent pointed out, is that some total functions in the
HOL Light formalization are not total as-is in Agda. The             Caching verified results is crucial, especially with tools with
agent suggested different options, such as assuming that             slower verification. Indeed, almost instant verification is not
types are nonempty (which is unsound) or threading evi-              always possible, but the agent should not wait for already
dence of an inhabitant through the definitions that need it.         verified results, for the same turnaround reason. The human
We told the agent to use the latter.                                 operator should also ensure that instructions are clear on
                                                                     that matter.
Axiomatization. Also during the formalization of Section             The tool should also provide as much feedback as possible.
0, the agent asked the human operator whether it should              Again, this matter is not exclusive to LLM agents, but they
axiomatize some theories or build them from the founda-              tend to lack the intuition of experienced human users.
tions. We told the agent to build them from scratch for
                                                                     Finally, instructions should be clear about the fact that the
added robustness, at the expense of time.
                                                                     verification might fail for external reasons such as getting
                                                                     OOM killed by the OS. The agent must therefore take that
Memory pressure. During the port of Section 0, Agda                  possibility into account to avoid missing critical feedback.
type checking exceeded the memory available to the Docker
container where the agent was running (32GB). The agent
did not realize this and interpreted the absence of a reply

                                                                 5
                                                     Autoreformalization

6. Comparison to automated proof transfer                            rems in, for example, set theory, which is highly dependent
                                                                     on particular encodings, to be more difficult for agentic
The problem of translating proofs across different proof             systems. Hence, we expect that in the future reformaliza-
assistants has been studied in the ITP community. The                tion tools will integrate elements of systematic, logic-based
standard approach is to implement a general translation              approaches.
that transfers low-level proofs from one proof assistant and
checks them with another. The approach typically requires            Our case study also highlights important takeaways for re-
high engineering effort and matching logical foundations,            formalization pipelines. We highlight the importance of a
and the resulting translated proofs lack good library align-         well-defined workflow in the agent instructions, including
ment and are often not idiomatic with respect to the target          source-aware decomposition for a clear idea of progress,
system.                                                              strict bookkeeping for easy backtracking, alignment with
                                                                     the existing library, and guardrails that prevent the agent
In particular, we compared our HOL Light to Lean refor-              from abandoning the source proof and designing its own ar-
malization against prior work on automated proof transfer            guments. In contrast with autoformalization, where natural
between HOL Light and Isabelle/HOL (Kaliszyk & Krauss,               language proofs often contain implicit arguments or gaps,
2013). The process patches HOL Light to generate proof               formal proofs are necessarily fully detailed and correct. This
trees in a serialized format. The outcome of the pipeline is         makes the process fully mechanical, so limiting the agent’s
an Isabelle theory file which loads the standard library ship-       freedom was key in improving performance. The compar-
ping with the translation, which matches some of the core            ison across Mizar, HOL Light, Lean, and Agda suggests
concepts from HOL Light to Isabelle/HOL. Then, the script            that libraries and tooling strongly affect success: Lacking
delegates to an OCaml program that reads the exported                libraries need to be completed first by the agent, and slow
proof trees and checks them within the Isabelle kernel. The          compilation processes can drastically slow progress. On
result is a verified translation of the Jordan Curve Theorem,        the other hand, foundational mismatch can often be handled
but one which cannot easily fit into Isabelle’s large existing       when the workflow makes the mismatch explicit and keeps
mathematical library, does not reuse any existing non-trivial        the target proof checker in the loop.
components, and does not produce a human-readable Is-
abelle theorem.
                                                                     Impact Statement
While this is logically sufficient to verify the theorem, it
significantly limits the usefulness of such a translation for        This paper presents work whose goal is to advance the state
real-world use. In contrast, LLM-based reformalization is            of the art in leveraging artificial intelligence for mathe-
not deterministic, complete, or correct by construction, but         matical research. There are many potential societal con-
it can preserve the original arguments rather than low-level         sequences of our work, none of which we feel must be
proof terms, leverage existing libraries, and tune the result-       specifically highlighted here.
ing definitions and proofs to be better integrated with the
target proof assistant’s ecosystem. Correctness is preserved         References
by utilizing the target assistant’s proof checker as the final
arbiter.                                                             Anonymous. The QED Manifesto. In Bundy, A. (ed.),
                                                                      Automated Deduction - CADE-12, 12th International
                                                                      Conference on Automated Deduction, Nancy, France,
7. Conclusion                                                         June 26 - July 1, 1994, Proceedings, Lecture Notes in
Our case study shows that LLM-based reformalization can                Computer Science, pp. 238–251. Springer, 1994. doi:
transfer large formal developments across proof assistants            10.5555/648231.752823.
at a scale that would be impractical for manual porting and
difficult for correct-by-construction proof translation. The         Blanqui, F. Translating HOL-Light proofs to Coq. In Pro-
development of mathematical libraries has always been a                ceedings of 25th Conference on Logic for Programming,
major bottleneck in the development of proof assistants, and           Artificial Intelligence and Reasoning, pp. 1–18, 2024. doi:
we believe that this will be radically improved by reformal-           10.29007/6k4x.
ization.
                                                                     Carneiro, M. Reimplementing Mizar in Rust. In
Nonetheless, LLM-based reformalization is not a silver bul-            Naumowicz, A. and Thiemann, R. (eds.), 14th
let, and it does not readily address heavy mismatches in               International Conference on Interactive Theorem
logical foundations. In all our case studies, proof assistants         Proving (ITP 2023), volume 268 of Leibniz Inter-
were already well developed, and, additionally, the Jordan             national Proceedings in Informatics (LIPIcs), pp.
Curve Theorem is largely independent of their particular               10:1–10:18, Dagstuhl, Germany, 2023. Schloss Dagstuhl
foundations. We would expect naturally translating theo-              – Leibniz-Zentrum für Informatik.       ISBN 978-3-

                                                                 6
                                                     Autoreformalization

  95977-284-6. doi: 10.4230/LIPIcs.ITP.2023.10. URL                  Naumowicz, A. and Kornilowicz, A. A Brief Overview of
  https://drops.dagstuhl.de/entities/                                  Mizar. In Proceedings of the 22nd International Con-
  document/10.4230/LIPIcs.ITP.2023.10.                                 ference on Theorem Proving in Higher Order Logics,
                                                                       volume 5674, pp. 67–72, August 2009. ISBN 978-3-642-
de Moura, L., Kong, S., Avigad, J., van Doorn, F., and von             03358-2. doi: 10.1007/978-3-642-03359-9 5.
  Raumer, J. The Lean Theorem Prover (System Descrip-
  tion). In Felty, A. P. and Middeldorp, A. (eds.), Auto-            Norell, U. Towards a Practical Programming Language
  mated Deduction - CADE-25, volume 9195, pp. 378–388.                Based on Dependent Type Theory. PhD thesis, Depart-
  Springer International Publishing, Cham, 2015. ISBN                  ment of Computer Science and Engineering, Chalmers
  978-3-319-21400-9 978-3-319-21401-6. doi: 10.1007/                   University of Technology, Göteborg, Sweden, 2007. URL
  978-3-319-21401-6 26.                                                https://chalmers.se.
                                                                     The mathlib Community. The Lean Mathematical Library.
Guilloud, S., Gambhir, S., Gilot, A., and Kunčak, V. Mech-
                                                                       In Proceedings of the 9th ACM SIGPLAN International
  anized HOL Reasoning in Set Theory. In Bertot, Y.,
                                                                       Conference on Certified Programs and Proofs, CPP 2020,
  Kutsia, T., and Norrish, M. (eds.), 15th International
                                                                       New Orleans, LA, USA, January 2020. ACM. doi: 10.
  Conference on Interactive Theorem Proving (ITP 2024),
                                                                       1145/3372885.3373824. URL https://doi.org/
  volume 309 of Leibniz International Proceedings in In-
                                                                       10.1145/3372885.3373824.
  formatics (LIPIcs), pp. 18:1–18:18, Dagstuhl, Germany,
  2024. Schloss Dagstuhl – Leibniz-Zentrum für Informatik.
  ISBN 978-3-95977-337-9. doi: 10.4230/LIPIcs.ITP.2024.
 18.

Hales, T. C. The jordan curve theorem, formally and infor-
  mally. The American Mathematical Monthly, 114(10):
  882–894, 2007.

Harrison, J. HOL Light: An Overview. In Berghofer, S.,
  Nipkow, T., Urban, C., and Wenzel, M. (eds.), Theorem
  Proving in Higher Order Logics, volume 5674, pp. 60–
  66. Springer Berlin Heidelberg, Berlin, Heidelberg, 2009.
  ISBN 978-3-642-03358-2 978-3-642-03359-9. doi: 10.
 1007/978-3-642-03359-9 4.

Kaliszyk, C. and Krauss, A. Scalable lcf-style proof transla-
  tion. In International Conference on Interactive Theorem
  Proving, pp. 51–66. Springer, 2013.

Keller, C. and Werner, B. Importing HOL Light into Coq.
  In Hutchison, D., Kanade, T., Kittler, J., Kleinberg, J. M.,
  Mattern, F., Mitchell, J. C., Naor, M., Nierstrasz, O.,
  Pandu Rangan, C., Steffen, B., Sudan, M., Terzopoulos,
  D., Tygar, D., Vardi, M. Y., Weikum, G., Kaufmann, M.,
  and Paulson, L. C. (eds.), Interactive Theorem Proving,
  volume 6172, pp. 307–322. Springer Berlin Heidelberg,
  Berlin, Heidelberg, 2010. ISBN 978-3-642-14051-8 978-
  3-642-14052-5. doi: 10.1007/978-3-642-14052-5 22.

Kohlhase, M. and Rabe, F. Experiences from Exporting
  Major Proof Assistant Libraries. Journal of Automated
  Reasoning, 65(8):1265–1298, December 2021. ISSN
 1573-0670. doi: 10.1007/s10817-021-09604-0.

Korniłowicz, A. A proof of the jordan curve theorem via
  the brouwer fixed point theorem. Mech. Math. Appl. Spe.
  Issue Jordan Curve Theorem, 6(1):33–40, 2007.

                                                                 7
