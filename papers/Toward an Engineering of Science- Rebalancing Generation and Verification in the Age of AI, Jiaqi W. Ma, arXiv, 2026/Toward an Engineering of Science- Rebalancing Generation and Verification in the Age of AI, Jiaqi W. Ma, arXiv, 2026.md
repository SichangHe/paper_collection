                                                T OWARD AN E NGINEERING OF S CIENCE : R EBALANCING
                                                  G ENERATION AND V ERIFICATION IN THE AGE OF AI

                                                                                            W ORKING PAPER


                                                                                              Jiaqi W. Ma
                                                                                University of Illinois Urbana-Champaign
                                                                                       jiaqima@illinois.edu
arXiv:2605.10425v1 [cs.CY] 11 May 2026




                                                                                              A BSTRACT
                                                  AI systems can now cheaply generate plausible scientific artifacts such as papers, reviews, and
                                                  surveys. This creates a risk of epistemic pollution in our scientific systems, where unreliable but
                                                  plausible-looking artifacts can accumulate faster than the system can filter them out. The problem
                                                  is structural: the epistemic infrastructure of science was calibrated to a world where producing a
                                                  plausible artifact required substantial expertise, labor, and time, so generation cost itself served as
                                                  a rough filter; AI weakens that filter without comparably lowering verification cost. We argue that
                                                  AI-era science should treat this as an engineering problem: redesigning epistemic infrastructure
                                                  to rebalance the costs of generation and verification. The current paper-centered system makes
                                                  verification expensive: papers compress long-context scientific logic into prose, forcing reviewers,
                                                  human or AI, to reconstruct underlying argument structure before they can evaluate it. As one
                                                  step in this direction, we propose blueprints as preliminary epistemic infrastructure: structured,
                                                  decomposed research artifacts that represent claims, evidence, assumptions, and definitions as typed
                                                  graph components. Blueprints are designed to trade an upfront generation cost for cheaper, more local,
                                                  more distributed verification downstream. We have instantiated the proposal in a proof-of-concept
                                                  prototype.


                                         1   Introduction

                                         AI is reshaping the cost structure of scientific work: papers, reviews, hypotheses, code, and literature surveys can
                                         now be generated at low cost [24, 34, 41]. But science is fundamentally the production of verifiable, reusable, and
                                         trustworthy knowledge. A central bottleneck of AI-era science is therefore shifting from generating plausible research
                                         artifacts toward verifying them to maintain a reliable scientific knowledge base. The existing epistemic infrastructure of
                                         science—the artifacts, workflows, and norms through which claims are produced, reviewed, and accepted [25, 11]—was
                                         developed for a world where producing a plausible scientific artifact demanded substantial expertise, labor, and time.
                                         Historically, high generation costs served as a rough filter for unreliable artifacts. AI dramatically lowers generation
                                         costs but has not proportionally reduced verification costs.
                                         This imbalance creates conditions for epistemic pollution: the contamination of scientific literature by plausible yet
                                         unreliable artifacts [9, 26, 27]. Examples include AI-generated surveys flooding preprint platforms, termed a “survey
                                         paper DDoS attack” [22], and AI-generated peer reviews at major venues [26]. Additionally, automated verification
                                         systems currently show limited effectiveness in identifying significant errors or reproducibility issues [32, 12]. Better
                                         frontier AI cannot be relied on to resolve this on its own: paper mills, citation farms, and low-effort actors can exploit
                                         any system that rewards plausible artifacts while making verification costly. We argue that addressing this challenge
                                         calls for an engineering view of science: deliberately redesigning epistemic infrastructure to rebalance the costs
                                         of generation and verification.
                                         Verification evaluates several dimensions of scientific claims, including novelty, significance, and validity. This paper
                                         focuses on validity—whether claims are actually supported by evidence, methods, assumptions, and reasoning—for
                                         two reasons. First, validity is often especially labor-intensive: reviewers can sometimes make preliminary judgments
                                         about novelty and significance from an abstract, a figure, and their knowledge of the field, but checking whether claims
                                              Toward an Engineering of Science                           W ORKING PAPER



hold requires tracing extended chains of reasoning through evidence, methods, and assumptions. Second, validity is the
dimension where artifact design has the clearest direct leverage, because it is fundamentally about the internal logic of
an argument, and how an argument is presented can either expose or hide that logic. Papers, the current dominant form
of research artifacts, often obscure logical dependencies: they compress multi-step reasoning into prose, and verifying
long, complex, prose-bound logic is hard for both human reviewers and AI systems.
To mitigate the cost of verifying validity, we propose restructuring scientific artifacts from prose-first narratives into
structured, decomposed representations of shorter local arguments. We take inspiration from leanblueprint1 for
Lean formalization [4, 42], where a long, complex theorem is decomposed into a graph of shorter, simpler claims
that can be worked on locally and verified with distributed collaboration, including from non-expert mathematicians.
We adapt this spirit to general research, while recognizing that science beyond mathematics admits no formal proof
obligation: the goal is not deductive certification but easier inspection.
We instantiate this idea in blueprints, a proof-of-concept prototype for representing a research project as a typed
argument graph2 . A blueprint decomposes a project into entities such as claims, evidence, assumptions, and definitions,
connected by relations such as supports, expands, and contradicts. Blueprints do not replace papers: the paper remains
the narrative interface, while the blueprint acts as the verification interface. Constructing a blueprint is not free—as
in leanblueprint, it requires expert judgment about how to decompose an argument, and good decompositions
vary across fields and standards of evidence—but the intended tradeoff is exactly the rebalancing we seek: the author
records the support structure once so that reviewers, readers, AI systems, and structural tools can inspect it more locally
downstream. Our prototype equips these typed argument graphs with lifecycle statuses and structural linting, and
exposes the same underlying document through both a browser canvas for human editing and a command-line interface
for AI-agent editing. We do not present blueprints as a new theory of argument or a new semantic-publishing ontology;
instead, they adapt existing structured-argument ideas [36, 18] into an author-facing artifact that makes support structure
explicit and locally inspectable in AI-era science.
This paper offers three key contributions.
           1. Epistemic pollution and the generation-verification imbalance. We argue that the cost imbalance between
              cheap AI generation and expensive verification creates conditions for epistemic pollution: the contamination
              of scientific knowledge systems by plausible but unreliable artifacts.
           2. Validity as the verification bottleneck. We distinguish novelty, significance, and validity, and argue that
              validity verification is often especially expensive because prose papers compress multi-step reasoning into
              narrative form.
           3. Blueprints as cost-rebalancing artifacts. We propose blueprints as structured, decomposed research artifacts
              designed to trade a generation cost of argument decomposition for cheaper downstream verification, and
              instantiate the concept in a working prototype.
Together, these contributions frame one step toward an engineering of science under AI abundance: scientific artifacts
should be designed not only for effective communication, but also for robust verification.

2         Epistemic Pollution and Generation-Verification Imbalance
2.1        Epistemic Pollution

We use epistemic pollution to refer to the contamination of scientific literature and adjacent knowledge systems—
preprint repositories, peer review records, citation graphs, benchmark leaderboards, replication corpora, and AI training
data—by artifacts that look like legitimate scientific contributions but cannot be relied upon. The phrase is meant to
capture more than fraud, predatory publishing, or public misinformation, each of which is a distinct and longer-standing
concern. Pollution sits between these: it includes negligent and low-effort artifacts that are not strictly fraudulent,
reaches into mainstream venues rather than only the predatory fringe, and degrades the infrastructure scientists rely on
to do their own work rather than the channels through which science reaches the public.
The phenomenon is already visible across the surface area of the literature. Large-scale analyses now find substantial
LLM-associated changes in scientific writing and production patterns [21, 19]. In October 2025, arXiv’s computer
science category changed its moderation policy for survey articles, requiring them to have passed through a successful
peer review. This change is attributed to the fact that generative AIs have made papers without new research results
fast and easy to write [15]. Automated survey-writing systems make the same capability concrete [39]. A recent
      1
          https://github.com/PatrickMassot/leanblueprint
      2
          https://github.com/jiaqima/blueprint


                                                              2
                                            Toward an Engineering of Science                              W ORKING PAPER



commentary describes the resulting volume pressure in starker terms, framing the volume of AI-generated surveys
flooding preprint platforms as a “survey paper DDoS attack” [22].
Peer review itself is under similar pressure. A study in Nature reported that 21% of manuscript reviews for a major
AI conference were found to be generated by AI [26], raising the prospect of a feedback loop in which AI-generated
submissions are evaluated by AI-generated reviews [16, 40]. More broadly, LLMs are now being tested as part of the
review pipeline itself, including at scale and in randomized peer-review interventions [20, 35]. Adjacent infrastructure
is similarly affected. Large-scale evidence suggests that journal AI-use policies have not produced reliable disclosure or
restrained AI-assisted writing [10]. Paper-mill operations are also scaling with generative AI, and documented cases of
AI-generated articles falsely attributed to real researchers show that authorship metadata can itself be corrupted [33].
The authors of AI Scientist-v2 report that an end-to-end autonomous research system could formulate hypotheses, run
experiments, and author a manuscript that exceeded an ICLR workshop’s average human acceptance threshold for a fully
autonomous submission [41, 24]. This last result is often read as a milestone in AI capability. We read it differently: it
shows that candidate generation has become powerful enough that the surrounding verification infrastructure is now the
bottleneck.

2.2   A Shift in the Cost Ratio

The reason epistemic pollution is difficult to contain is not simply because AI introduces unreliable artifacts into science.
Unreliable artifacts existed long before AI, and the existing infrastructure of peer review, citation, and venue prestige
was built to filter them. What has changed is not the presence of unreliable artifacts but the cost of producing one—and
that cost was the implicit parameter on which all of these filters depended.
Producing a plausible paper, review, survey, or benchmark report used to require time, expertise, data, analysis,
and revision; authorship itself functioned as a costly signal of seriousness. AI can substantially lower much of that
production cost. The cost of verifying such an artifact has not fallen to a comparable degree. Automated verification,
the natural defensive response, is itself currently weak: recent benchmarks for detecting significant errors in scientific
manuscripts find recall far below what would be needed for meaningful filtering [32], and benchmarks for automated
reproducibility assessment in social science report similar gaps [12]. AI-generated artifacts have also introduced new
failure modes that verification must screen for—hallucinated citations [27, 29], unfaithful summaries, code that does
not match the described method, results not produced by the stated procedure. At this time, the cost ratio between
generating and checking a scientific artifact is sharply imbalanced.
Under such an imbalance, the existing filters do not break on their own terms—they simply lose the cost differential
that gave them their discriminating power. The diagnosis is therefore infrastructural rather than behavioral: not that
authors or reviewers have stopped doing their jobs, but that the infrastructure they operate within was calibrated to a
cost ratio that no longer holds.

2.3   Why Better AI Alone Is Not Enough

A natural response to the foregoing is to expect that better AI systems should be enough to resolve the problem: stronger
generators will produce fewer hallucinations, and stronger verifiers will catch more errors. We are skeptical of relying
on this alone for two reasons.
First, the problem is structural, not only capability-bound. Even if frontier AI systems become highly reliable scientific
collaborators, the infrastructure remains exploitable by anyone willing to use less reliable systems. Paper mills, citation
farms, low-effort authors, fake reviewers, automated submission systems, and institutions rewarded by publication
counts all benefit from artifacts that pass existing filters without improving knowledge. The infrastructure rewards
plausibility; as long as plausibility is cheap to produce, the most expensive part of the system—verification—bears the
load, and improvements in the best generators do little to relieve it.
Second, the asymmetry between generation and verification does not scale symmetrically with capability. A capability
improvement in generation lets one actor produce many more plausible artifacts at marginal cost. A capability
improvement in verification, by contrast, must be applied per artifact, and verification of a complex scientific claim does
not parallelize as readily as generation of a plausible-looking one. Even under optimistic assumptions about verifier
capability, the cost of producing and the cost of checking a scientific artifact remain on different scaling curves.
The redesign question that follows is therefore not only whether AI systems can be improved, but how the infrastructure
in which AI-generated and AI-assisted artifacts circulate should be redesigned to handle the cost structure AI has
produced. The next section opens up verification cost itself, asking what makes it expensive and where artifact design
has the most leverage.


                                                             3
                                            Toward an Engineering of Science                               W ORKING PAPER



3     Examining the Verification Cost

If the central problem is a cost imbalance between cheap generation and expensive verification, the natural next question
is what makes verification expensive in the first place. Section 2 treated verification cost as a single quantity contrasted
with generation cost. This section opens it up. We decompose verification into its components, locate where cost
concentrates, and identify the part of verification that artifact design can most directly affect.

3.1   What Verification Costs

A reviewer, reader, or downstream user who wants to determine whether a scientific artifact is reliable cannot do so by
inspection of the artifact’s surface. Plausibility is what generation produces; reliability is what verification has to check.
The work involved typically includes some combination of the following: identifying the central claims the artifact
makes; locating the evidence offered in support of each claim; recovering the assumptions on which the argument
depends, including ones the author has not stated explicitly; checking that the claimed support relations actually hold,
rather than merely being asserted; evaluating whether the methods chosen are appropriate to the question; and tracking
the risks, limitations, contradictions, and open questions that qualify the central claims.
Two features of this list matter for the rest of the section. First, the components are not equally costly. Some can be done
quickly from a skim; others require deep engagement with the argument’s internal logic. Second, every component is
paid per verifier. The author bears the cost of structuring an argument once; each subsequent reader, reviewer, or AI
system that needs to verify it bears a reconstruction cost in turn. This asymmetry compounds: a small reduction in
per-artifact verification cost is paid forward to every downstream verifier, and a small increase compounds the same
way.
Verification cost, in other words, is not a flat tax on the scientific record. It is a distribution across components, paid
many times by many parties, and the question of where to intervene depends on where the cost concentrates.

3.2   Validity as the Cost Concentration

Scientific review is conventionally said to evaluate several dimensions, of which the most commonly cited are novelty
(does this contribute something the field did not already know?), significance (does the contribution matter, and to
whom?), and validity (are the claims actually supported by the evidence, methods, assumptions, and reasoning offered?).
These dimensions are not exhaustive—reviewers also evaluate clarity, scope, and fit—but they are the dimensions that
most directly determine whether an artifact enters the trusted knowledge base.
Novelty and significance, on close inspection, are partly social judgments. Whether a result is novel depends on what
the field has previously established, which a reviewer often knows independently of the artifact; whether it is significant
depends on what the field cares about, which is similarly external. In many cases, a reviewer can form an initial
judgment on both from an abstract, a figure, and a sense of the field, even if a final judgment may require deeper
engagement. Artifact design has more limited direct leverage here: a more structured artifact does not change whether a
result is genuinely new or important, only how clearly it is communicated.
Validity is different in two ways. First, it is often especially labor-intensive. Where novelty and significance can
sometimes be judged initially at the surface, validity requires tracing extended chains of reasoning through evidence,
methods, and assumptions—running through nearly every component listed in Section 3.1. Second, validity is
the component whose cost depends most directly on how the artifact is internally organized. A claim’s validity is
fundamentally a property of the argument structure connecting it to its evidence, and the artifact is what records (or
fails to record) that structure. Novelty and significance live partly in the field’s collective context; validity lives more
directly in the artifact itself.
This is the asymmetry that motivates the rest of the paper. Verification cost often concentrates in validity, and validity is
the component where artifact design has the clearest direct leverage. We do not claim to address novelty or significance
verification. Those problems are real, but they are not where the artifact-level intervention developed here is most likely
to pay off.

3.3   Why Validity Verification Is Expensive in Prose

Validity is not intrinsically expensive to verify. It is expensive to verify given the artifact form in which scientific
arguments are currently delivered. The dominant form is the prose paper, and prose has a specific structural property
that makes validity verification costly: it serializes an argument graph into a reading order designed for narrative flow
rather than for inspection.


                                                              4
                                           Toward an Engineering of Science                               W ORKING PAPER



When an author writes a paper, they hold something like a graph in mind: a set of claims, the evidence they have for
each, the assumptions they are making, the dependencies among the claims, and the risks and limitations they have
noticed. Writing the paper compresses that graph into a linear text optimized for clarity, persuasion, and conformity to a
venue’s expectations. The compression discards information. Implicit assumptions are not written down because they
would be tedious to enumerate. Dependencies between claims are signaled by transitional phrases rather than recorded
as edges. Limitations may be acknowledged in a paragraph and not propagated to the claims they qualify.
A reviewer who wants to verify the paper must reverse this compression. They identify the central claims, which may
be distributed across the abstract, introduction, results section, and conclusion, sometimes in slightly different forms.
They locate the evidence for each claim, which may be in the methods section, in figures, in appendices, or by reference
to prior work. They infer implicit assumptions, since the author rarely lists them explicitly. They check whether the
support relations the author asserts actually hold, which often requires recomputing or rereading. They track risks and
contradictions, which may be acknowledged briefly in one place and silently violated in another. Each of these is a
reconstruction of structure that existed in the author’s head but was not recorded in the artifact. The author paid the
structure cost once; or, increasingly, the author skipped it entirely, leaving an AI system to produce a serialization
without the underlying graph.
This is also why AI verification of prose papers is harder than the surface symmetry between AI generation and AI
verification might suggest. A long prose argument can exceed the context window or reasoning depth that current
models can reliably handle for non-trivial scientific work, and the linearization removes precisely the local structure
that an AI system could otherwise check piece by piece. The scientific claim-verification literature makes this point
at increasing scales. SciFact formulates verification as finding abstracts that support or refute an atomic scientific
claim and selecting rationale sentences; SciFact-Open shows that the same task becomes substantially harder when
evidence must be found in an open-domain corpus and when evidence only partially matches a claim’s scope [37, 38].
CLAIM-Bench moves the problem into full AI papers, where models must extract claims, locate dispersed evidence
spans, and validate the links between them, exposing precision–recall and computational-cost tradeoffs [14]. At the
manuscript and reproducibility levels the gap is larger still: SPOT-a reports low precision and recall for significant
errors in published manuscripts, while REPRO-Bench reports low accuracy when agents must compare a paper PDF
with its reproduction package [32, 12]. Execution-grounded evaluation systems make the same point constructively:
checking code, data, and execution traces alongside the paper surfaces failures that narrative-only review misses [1].
Taken together, these benchmarks suggest that the bottleneck is not only model capability; it is the need to reconstruct
from prose the claim–evidence and paper–code relations that the artifact did not make explicit. Better models will help,
but the artifact form is itself the constraint. A verifier—human or AI—cannot easily check what the artifact has not
recorded.

3.4        What This Implies for Artifact Design

The diagnosis points to a specific design lever. If a major verification cost is reconstruction of argument structure that
the author had but did not record, the corresponding remedy is for the artifact to record that structure in the first place.
Two design desiderata follow. The first is to make the artifact structured rather than prose-first: the argument graph
is recorded explicitly as the primary representation, and prose, where it is needed, is generated from or attached to
the graph rather than serving as the graph’s only form. The second is to make the artifact decomposed rather than
monolithic: the graph is broken into shorter local arguments that can be inspected, doubted, or amended independently,
rather than being packaged as a single linear narrative whose components cannot be addressed in isolation.
Together, these two desiderata are designed to redistribute the structure work from many downstream verifiers to one
upstream author. The author pays an upfront cost—the cost of recording explicitly what would otherwise have been left
implicit—with the aim that every downstream verifier pays less. This is what rebalancing the costs of generation and
verification would look like at the artifact level. Section 4 develops what an artifact built around these two desiderata
actually looks like.

4         Blueprints
Blueprints build on a long line of work arguing that scholarly knowledge should be represented as structured, machine-
actionable claims rather than only as prose [30, 17, 3, 8]. The closest operational inspiration for our prototype is
leanblueprint3 in formal theorem proving [4], because it demonstrates how a long argument can be decomposed into
locally inspectable graph components. We begin by briefly introducing leanblueprint (Section 4.1), then specify the
structure of a blueprint (Section 4.2) and how it is built and reviewed in practice (Section 4.3).
      3
          https://github.com/PatrickMassot/leanblueprint


                                                             5
                                                       Toward an Engineering of Science                                                      W ORKING PAPER




                      ≡            ✦               ⊢            ⚠              ❖       Claim        n_xyz_4



                                                                               TYPE                                          STATUS

                                                                                   ❖    Claim                                      draft

                                           ∧
                                                                               LABEL

                                                                                AI can now cheaply generate plausible scientific artifacts


                                                                               BODY (MARKDOWN + KATEX)

                                   ❖




                                               ❖                                        Edge       n_xyz_5 → n_xyz_6


                                                                               TYPE

                                                                                        Supports

                                           ?                                   BODY (MARKDOWN + KATEX)




                 Figure 1: An illustration of the blueprint as a heterogeneous graph with typed nodes and edges.


4.1        Background: leanblueprint

leanblueprint is a tool used in the Lean theorem prover community [4] to plan, decompose, and track formalization
of long mathematical proofs. A “blueprint” in leanblueprint is a typed graph: nodes are mathematical statements
(definitions, lemmas, theorems), and edges record dependency—which lemmas a theorem rests on, or which definitions
a lemma uses. Each node carries a status flag indicating whether it has been formally checked by Lean. The canonical
demonstration of the use of leanblueprint is the Lean formalization of the proof of the Polynomial Freiman-Ruzsa
conjecture, where Tao and collaborators used a leanblueprint to coordinate a distributed effort across many contributors,
including non-experts who could pick up local lemmas without holding the full proof in mind4 .
Two features of leanblueprint matter for what follows. First, the artifact is the structure: the graph records the proof’s
logical skeleton directly, and the prose attached to each node is supplementary. A reviewer or contributor can inspect
a single lemma and its dependencies without reading a paper. Second, the structure makes verification distributable:
because each node is small and locally specified, contributors can work on individual lemmas in parallel, and the global
proof status is a function of the per-node statuses. These features instantiate the structured-and-decomposed desiderata
of Section 3.4 in concrete form.
leanblueprint works because Lean provides a formal proof obligation: a node is either machine-verified or it is not.
General research has no such criterion, so leanblueprint cannot be transplanted directly. Our proposal adapts this
kind of structured, decomposed argument graph to settings where verification is non-binary, where vocabularies vary by
field, and where human and AI agents are both first-class users.

4.2        The Design of Blueprints

4.2.1        The Data Model
A blueprint is a heterogeneous directed graph (see Figure 1 for an illustration). Nodes and edges are both typed. Each
node carries an ID, a type, a status, a label, and an optional Markdown body with mathematical notation. Each edge
carries an ID, a type and an optional body of the same form. Beyond the typing, no further structure is built into the data
model: a blueprint is one JSON document, and any blueprint can be inspected, edited, or transmitted as a single file.

4.2.2        Vocabulary
The built-in vocabulary consists of seven node types organized into four roles, five edge types, and a small collection of
node-type-specific status ladders.

Node types: argument core. Three node types carry the load-bearing content of an argument. This lightweight
vocabulary adapts Toulmin’s claim–data–warrant structure [36], while the surrounding graph vocabulary draws on
issue-based discourse models such as IBIS [18]. A claim is a proposition the author proposes to defend. An evidence
      4
          Tao’s PFR Lean blueprint tour.


                                                                      6
                                           Toward an Engineering of Science                              W ORKING PAPER



is a proposition reporting an observation, a measurement, or a citation that bears on a claim. An assumption is a
proposition taken as given.

Node types: construction handles. Two node types help the author build the graph without asserting propositions.
A definition pins a term so that the rest of the argument can refer to it precisely. A question marks an unresolved
direction.

Node types: review channel.       A risk node attaches a counter-argument or suspicion to a specific claim, in place.

Node types: flexibility valve. A synthesis node carries prose when a joint argument across several premises does
not fit on a single edge body.

Edge types. Five edge types connect nodes: SUPPORTS (an evidence, assumption, or supporting claim backs a
downstream claim), EXPANDS (a child node elaborates its parent), CONTRADICTS (a tension between two nodes),
ADDRESSES (a node responds to a risk or question), and RELATES (a non-committal association).

Statuses. Each node type carries a status from a short type-specific ladder. A claim moves through draft, stated,
and supported. An evidence moves through missing, cited, and verified. A definition is draft or stated.
A question is open or answered. An assumption is given or questioned. A risk is noted, addressed, or
accepted. A synthesis is draft or stated.

Extensibility. The vocabulary above is the built-in default. The blueprint format allows a per-document override
(encoded in the document itself), a per-workspace override (a single configuration file applying to every document in
the workspace), and the built-in default.

4.3     Using Blueprints

Given the design, we now walk through how blueprints will be used.

4.3.1    Two Interfaces over a Shared Document
The prototype exposes two first-class interfaces, respectively for human users and AI agents, over a shared blueprint
document.

Browser canvas for human users. The blueprint renders as an interactive mindmap on a browser canvas, where a
human user can intuitively edit the graph. See Figure 2 for a screenshot of the layout.

Command-line interface (CLI) for AI agents. The edits on a blueprint can also be done through a set of CLI
commands. The commands are designed to be issued by an AI agent rather than typed by a human; we have used
Claude Code and Codex as the primary test agents, each given a small skill description that explains when and how to
use the available commands.

Live synchronization. Both interfaces read and write the same JSON file storing the blueprint. A development server
watches the workspace directory and propagates edits between the two within roughly 200 milliseconds: when the
agent issues a CLI command that mutates the file, the human’s canvas updates live; when the human edits a node body
in the canvas, the agent’s next read reflects the change. The shared-substrate property is what makes a researcher and
their agent able to edit the same artifact in parallel rather than coordinating through a chat window.

4.3.2    Authoring a Blueprint
The authoring workflow is similar in spirit to leanblueprint’s, with adaptations forced by the move from formal
mathematics to general research. An author builds the graph by drafting propositional content, scaffolding it with
construction handles, tracking progress through statuses, and reaching for synthesis only as a flexibility valve. Authoring
can also be partly delegated to an AI agent operating through the CLI.

Drafting the argument core. The propositional content of an argument is built up using claim, evidence, and
assumption nodes connected by SUPPORTS edges. An author typically starts with a small number of central claim
nodes, then either decomposes each into supporting sub-claims or grounds it in evidence and assumption nodes.


                                                            7
                                                 Toward an Engineering of Science                                                                                    W ORKING PAPER


 (a) Browser canvas                                                                        (b) Dual editing interfaces


                                                                                                         used by humans                                                     used by AI agents


                                                                                                       Browser canvas                                                                CLI
                                                                                                    react-flow + dagre, KaTeX                                              bin/blueprint.ts
                                                                                                      visual editing, live sync                                      add / move / link / setbody / ...



                                                                                                                       HTTP request
                                                                                                                        + SSE event




                                                                                                          Sync server
                                                                                                                                                                                    direct
                                                                                                      Vite plugin (dev only)                                                     read / write
                                                                                                     HTTP API, SSE, fs.watch




                                                                                               read / write
                                                                                                + fs.watch




                                                                                                                                  blueprints/<name>.json
                                                                                                                                   single source of truth on disk;
                                                                                                                                   both interfaces converge here




Figure 2: Dual interfaces over a shared blueprint document. Left: the browser canvas, showing a blueprint as an
interactive typed mindmap. Right: the illustration diagram of the dual interfaces.


Edges may carry their own bodies that explain why the source backs the target. A useful authoring rule of thumb: if the
supporting premises do not interact—each supports the conclusion independently—use separate edges with bodies; if
they interact and the joint argument must be considered as a whole, use a synthesis node.


Scaffolding with construction handles. Two non-propositional node types help the author build the graph. A
definition pins a term so that the rest of the argument can refer to it precisely; pinning a definition early lets later claims
use the term without re-explaining it each time. A question marks an unresolved direction during authoring—a thread
the author has not yet decided how to resolve, or a sub-problem to come back to. The same node type doubles as a
future-work flag in a finished blueprint, which means questions don’t need to be deleted before sharing; they signal
what’s still open.


Tracking progress through statuses. Each node carries a status from a short type-specific ladder. During authoring,
statuses act as a progress tracker: a claim is draft while sketched, stated once precisely formulated, and supported
when the author asserts it is settled by its incoming support edges. An evidence moves through missing (node added
but without content), cited (linked to the source), and verified (independently checked). Authoring discipline
is to advance statuses bottom-up: an author should not mark a claim supported before its supporting evidence
and supporting claims have themselves been matured. Doing so triggers structural warnings (described in the next
subsection), which is the lint helping the author notice they have asserted completeness that the structure does not yet
warrant.


Synthesis as a flexibility valve. A synthesis node is used when several supporters establish a downstream claim
only by being considered together—an argument that does not cleanly distribute across separate edges. The valve is
genuinely needed: some arguments rest on premises that interact, and forcing such an argument onto independent edges
would mislead. But synthesis is also the type most easily misused. Its body hides structure inside prose, which is the
opposite of what the typed graph is for, and a blueprint that leans heavily on synthesis may signal that decomposition
has not been pushed hard enough.5 The artifact does not adjudicate. Lint warns about specific misuse patterns—empty
synthesis nodes, single-supporter synthesis—but the deeper question of whether a synthesis is genuinely irreducible is
left to the author.


Co-authoring with an AI agent. Because the CLI exposes the same operations as the canvas, an AI agent can be
given partial authoring tasks: populating evidence bodies from cited sources, suggesting decompositions of a sketched
claim, or extending a subgraph along a direction the author has indicated. Coordination between human and agent
currently happens at the prompt level—the author tells the agent which subgraph to work on—rather than through
ownership primitives in the artifact itself.

     5
         leanblueprint faces a similar tension: a poorly decomposed proof can hide all its difficulty inside one large lemma.


                                                                   8
                                           Toward an Engineering of Science                               W ORKING PAPER



4.3.3   Reviewing a Blueprint
A blueprint is reviewed—by the author themselves, by a human reviewer, or by an AI reviewer—through structural
inspection of local subgraphs and through the dialogue mechanism the type vocabulary supports.

The artifact as a dialogue. The blueprint represents an argument as it is being made, not as it has been proved.
Statuses are the author’s positions: a supported claim is one the author asserts is settled by its support graph. A
reviewer who challenges that assertion does so structurally, by attaching a risk node to the claim. The author responds
by adding nodes that ADDRESSES the risk, by revising the support graph, or by moving the claim’s status back to
stated while the contestation is unresolved. Statuses are revisable. The point of statuses is not to certify; it is to record
the author’s current position so that the review dialogue has somewhere concrete to start.
This is what leanblueprint does not need to do: in formal mathematics the kernel arbitrates, so a proved status is
a fact, not a claim. In general research no kernel exists, and the artifact has to make explicit that statuses are author
assertions, structurally tracked but contestable.

Structural lint as an aid to review. The artifact ships with around a dozen structural rules grouped along three axes.
All rules are warnings, not blocks: the artifact does not refuse to save or share a blueprint that has unresolved warnings,
because lint can flag patterns but cannot adjudicate content. The reviewer is the arbiter; the lint surfaces what the
reviewer should look at.
The rules of the first axis check the soundness of the support graph. A SUPPORTS edge running the wrong way (for
instance from a claim into its own evidence) is almost always a typo or a confused edge. A SUPPORTS edge into a
matured claim from a node that is not itself grounded indicates the chain of support has a hole. The most informative
rule on this axis flags a claim marked supported with no incoming SUPPORTS edges at all. Structurally, such a node
is an assumption, not a claim: the author is asserting a proposition without offering anything to back it. The lint does
not insist the author convert it to an assumption—if the proposition really should be backed, the author needs to add
the supports—but the warning makes the type-vocabulary distinction operational. The difference between a claim and
an assumption is exactly what the support graph records.
The rules of the second axis check argument structure. Directed cycles in the SUPPORTS subgraph are flagged because
circular support is not support. Single-supporter synthesis nodes are flagged because synthesis is for joint support, and
a synthesis with one supporter is using the wrong type. The rules of the third axis check vocabulary integrity: nodes or
edges with type or status identifiers not in the active registry, or with empty labels, are flagged because they cannot be
reasoned about reliably.

Distributed and local review. The intended payoff of all this structure is that review can become more local. A
reviewer can pick a claim and inspect its supporters, evaluate the evidence bodies and assumption justifications
attached to that local subgraph, and form a judgment on that subgraph without first reconstructing the entire argument
from prose. Different subgraphs can in principle be reviewed by different reviewers, in parallel, with less coordination
overhead than dividing up a paper. An AI critic can be given a single matured-claim subgraph and asked to enumerate
plausible counter-arguments as new risk nodes; an expert can be given a single evidence node and asked to verify
the citation it points to; a generalist reader can navigate the graph following EXPANDS edges and form a sense of the
argument’s overall shape without having to extract the structure from prose. This is the property the rebalancing argument
of Section 3.4 ultimately rests on: an artifact that records structure is designed to make verification distributable.


5   Related Work

Structured scholarly artifacts and semantic publishing. Blueprints sit within a broader semantic-publishing
tradition that argues scientific communication should expose machine-actionable scholarly structure rather than leave
knowledge locked inside prose [30, 17]. Nanopublications proposed RDF-based packages for core scientific statements
and their provenance, while micropublications developed a richer semantic model for claims, evidence, arguments,
and annotations [8, 3]; later work has explored nanopublication-based reviewing workflows [2]. The Open Research
Knowledge Graph represents research contributions as structured scholarly knowledge [13], while CiTO and related
semantic-publishing ontologies make scholarly relations such as citation intent explicit [31]. Octopus similarly
decomposes research into typed, independently publishable components [6]. Blueprints therefore do not claim novelty
in representing claims, evidence, provenance, or scholarly relations as structured data. They build on this lineage but
focus on the AI-era problem of lowering downstream validity-verification cost through a lightweight, author-facing
artifact with local review statuses, soft structural lint, and shared human/agent interfaces.


                                                             9
                                           Toward an Engineering of Science                               W ORKING PAPER



Argumentation models and scientific claim verification. The blueprint vocabulary is not intended as a new theory
of argument. It is a pragmatic vocabulary for research artifacts, drawing from long-standing models of claims, grounds,
rebuttals, issues, positions, and arguments [36, 18]. In natural language processing, scientific claim-verification
benchmarks such as SciFact and SciFact-Open evaluate whether claims are supported or refuted by evidence in the
scientific literature [37, 38]. More recent work asks whether LLMs can validate claim–evidence relations in full
AI papers [14], while manuscript-level benchmarks test scientific error detection and social-science reproducibility
assessment [32, 12]. Execution-grounded evaluation extends this line by checking paper narratives against code, data,
and execution traces rather than against text alone [1]. The argumentation literature supplies vocabulary for making
support and contestation explicit; the NLP and execution-grounded verification literature mostly operates downstream
of already-written artifacts, recovering or assessing support relations, claim–evidence links, errors, reproducibility, or
narrative–execution consistency after the fact. Blueprints instead make a project’s support structure part of the artifact
before verification begins.

AI-era production pressure and peer review. Recent empirical work suggests that LLMs are already affecting
scientific writing at scale and may be changing scientific production patterns [21, 19]. Automated survey-writing
systems show that literature synthesis itself can be generated cheaply [39], and AI-generated survey volume has been
framed as a denial-of-service attack on research attention [22]. Related failure modes include GPT-fabricated papers,
false authorship, and hallucinated citations [9, 33, 27, 29]. Peer review is also being reshaped: AI-generated reviews
are already visible in major conferences [26], while LLM feedback has been evaluated at scale and in randomized
peer-review interventions [20, 35]. These lines of work motivate the same bottleneck: as plausible artifacts and reviews
become cheaper to produce, the value of making verification structurally easier increases.

Provenance, infrastructure, and agent-native artifacts. Another response to AI-era scientific risk is to improve
provenance and infrastructure. Recent work frames LLM-assisted scholarly writing as a provenance problem [5], while
broader proposals call for AI-era scientific infrastructure and renewed open-science systems [7, 28]. A very recent,
concurrent proposal for agent-native research artifacts makes a closely related claim: papers discard structure that
AI agents need in order to inspect, reproduce, and extend research [23]. Blueprints are complementary but narrower.
Provenance systems record attribution, lineage, and production history; agent-native artifacts package research for
execution, reproduction, and extension; blueprints target a lighter-weight layer for validity verification, recording how
claims, evidence, assumptions, risks, and definitions support one another. Their purpose is to make the verification
interface of a research project explicit.

6   Discussion
Engineering of science as a research program. The argument presented here exemplifies a broader principle:
scientific artifacts and infrastructure should be designed intentionally and evaluated systematically against criteria such
as verification costs, error rates, ease of adoption, and resilience against adversarial or low-effort use. The related work
discussed underscores that this principle is already implicitly recognized across areas like open science, reproducibility,
semantic publishing, and scholarly infrastructure. The cost imbalance introduced by AI highlights an urgent, specific
design question: Which elements of scientific artifacts require redesign now that plausible generation is inexpensive,
yet rigorous verification remains resource-intensive?

Empirical validation of blueprints. This paper focuses on staking out a position and proposing a preliminary
prototype design. The claim that recording argument structure upstream can reduce the reconstruction burden paid by
downstream verifiers is a hypothesis that has yet to be fully tested. We see three natural starting points for empirical
validation: studies of blueprint authoring overhead and verification time on small case-study projects, comparison of
reviewer agreement and error-detection rates between prose papers and corresponding blueprints, and validation of
vocabulary extensions in disciplines outside our default.

Blueprints as harnesses for AI-assisted science. Blueprints may matter not only for verification, but eventually for
generation. In software, test suites do not merely check code after it is written; they also make code-generation agents
more useful by giving them local targets, structured feedback, and a way to iterate without holding the entire system in
context. Blueprints could play a similar role for scientific arguments. Because claims, evidence, assumptions, risks,
and support relations are explicit, an AI agent can be asked not only to inspect a finished argument, but also to extend
a subgraph, propose missing evidence, draft a synthesis node, identify unsupported claims, or generate alternative
decompositions against the current structure. The resulting additions would still be provisional and subject to human
judgment, but the artifact gives generation something to push against. In this sense, blueprints are a candidate harness
for AI-assisted science: they make verification more local now, and may make generation more disciplined later.


                                                            10
                                          Toward an Engineering of Science                             W ORKING PAPER



7   Conclusion
AI has made plausible scientific artifacts cheap to generate while leaving reliable verification comparatively expensive.
This is not only a model-capability problem, but an infrastructure problem: scientific systems built around papers, peer
review, and citation were calibrated to a world in which plausibility itself was expensive to produce.
We have suggested for one artifact-level response: blueprints, structured and decomposed argument graphs that make
support relations inspectable before a verifier has to reconstruct them from prose. Papers remain the narrative interface
of science; blueprints are proposed as a verification interface. The broader argument is that AI-era scientific artifacts
should be designed for verification as deliberately as they are designed for communication, so the infrastructure that
admits scientific claims can keep pace with the systems that generate them.

References
 [1] Xiaoyan Bai, Alexander Baumgartner, Haojia Sun, Ari Holtzman, and Chenhao Tan. The story is not the science:
     Execution-grounded evaluation of mechanistic interpretability research. arXiv preprint arXiv:2602.18458, 2026.
 [2] Cristina-Iulia Bucur, Tobias Kuhn, Davide Ceolin, and Jacco van Ossenbruggen. Nanopublication-based semantic
     publishing and reviewing: a field study with formalization papers. PeerJ Computer Science, 9:e1159, 2023.
 [3] Tim Clark, Paolo N Ciccarese, and Carole A Goble. Micropublications: a semantic model for claims, evidence,
     arguments and annotations in biomedical communications. Journal of biomedical semantics, 5(1):28, 2014.
 [4] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer. The lean theorem
     prover (system description). In International Conference on Automated Deduction, pages 378–388. Springer,
     2015.
 [5] Brian D Earp, Haotian Yuan, Julian Koplin, and Sebastian Porsdam Mann. Llm use in scholarly writing poses a
     provenance problem. Nature Machine Intelligence, pages 1–2, 2025.
 [6] Alexandra Freeman, Pen-Yuan Hsing, Mariia Tukanova, Jacqueline Thompson, and Marcus Munafo. Could
     octopus help researchers produce high quality, open research? Octopus, 2023. URL https://doi.org/10.
     57874/cyz8-es44. Rationale / Hypothesis, published 26 October 2023.
 [7] Satrajit Ghosh. An intelligent infrastructure as a foundation for modern science. ArXiv, 2025. URL https:
     //api.semanticscholar.org/CorpusID:280649886.
 [8] Paul Groth, Andrew Gibson, and Jan Velterop. The anatomy of a nanopublication. Information services and use,
     30(1-2):51–56, 2010.
 [9] Jutta Haider, Kristofer Rolf Söderström, Björn Ekström, and Malte Rödl. Gpt-fabricated scientific papers on
     google scholar: Key features, spread, and implications for preempting evidence manipulation. Harvard Kennedy
     School Misinformation Review, 5(5), 2024.
[10] Yongyuan He and Yi Bu. Academic journals’ ai policies fail to curb the surge in ai-assisted academic writing.
     Proceedings of the National Academy of Sciences, 123(9):e2526734123, 2026.
[11] Diana Hicks, Paul Wouters, Ludo Waltman, Sarah De Rijcke, and Ismael Rafols. Bibliometrics: the leiden
     manifesto for research metrics. Nature, 520(7548):429–431, 2015.
[12] Chuxuan Hu, Liyun Zhang, Yeji Lim, Aum Wadhwani, Austin Peters, and Daniel Kang. Repro-bench: Can agentic
     ai systems assess the reproducibility of social science research? In Findings of the Association for Computational
     Linguistics: ACL 2025, pages 23616–23626, 2025.
[13] Mohamad Yaser Jaradeh, Allard Oelen, Kheir Eddine Farfar, Manuel Prinz, Jennifer D’Souza, Gábor Kismihók,
     Markus Stocker, and Sören Auer. Open research knowledge graph: Next generation infrastructure for semantic
     scholarly knowledge. In Proceedings of the 10th international conference on knowledge capture, pages 243–246,
     2019.
[14] Shashidhar Reddy Javaji, Yupeng Cao, Haohang Li, Yangyang Yu, Nikhil Muralidhar, and Zining Zhu. Can
     ai validate science? benchmarking llms on claim–evidence reasoning in ai papers. In Proceedings of the 14th
     International Joint Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific
     Chapter of the Association for Computational Linguistics, pages 2355–2379, 2025.
[15] Nicola Jones. Leading preprint server clamps down on ’ai slop’. Science, 391 6784:432–433, 2026. URL
     https://api.semanticscholar.org/CorpusID:285174241.
[16] Jaeho Kim, Yunseok Lee, and Seulki Lee. Position: The ai conference peer review crisis demands author feedback
     and reviewer rewards. arXiv preprint arXiv:2505.04966, 2025.


                                                           11
                                         Toward an Engineering of Science                            W ORKING PAPER



[17] Tobias Kuhn and Michel Dumontier. Genuine semantic publishing. Data Science, 1(1-2):139–154, 2017.
[18] W. Kunz and H.W.J. Rittel. Issues as elements of information systems. Working paper 131, Institute of Urban
     and Regional Development, University of California, 1970. URL https://books.google.com/books?id=
     B-MaAQAAMAAJ.
[19] Keigo Kusumegi, Xinyu Yang, Paul Ginsparg, Mathijs de Vaan, Toby Stuart, and Yian Yin. Scientific production
     in the era of large language models. Science, 390(6779):1240–1243, 2025. doi: 10.1126/science.adw3000. URL
     https://www.science.org/doi/abs/10.1126/science.adw3000.
[20] Weixin Liang, Yuhui Zhang, Hancheng Cao, Binglu Wang, Daisy Yi Ding, Xinyu Yang, Kailas Vodrahalli, Siyu
     He, Daniel Scott Smith, Yian Yin, et al. Can large language models provide useful feedback on research papers? a
     large-scale empirical analysis. NEJM AI, 1(8):AIoa2400196, 2024.
[21] Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley Lepp, Wenlong Ji, Xuandong Zhao, Hancheng Cao, Sheng
     Liu, Siyu He, Zhi Huang, et al. Quantifying large language model usage in scientific papers. Nature Human
     Behaviour, pages 1–11, 2025.
[22] Jianghao Lin, Rong Shan, Jiachen Zhu, Yunjia Xi, Yong Yu, and Weinan Zhang. Stop ddos attacking the research
     community with ai-generated survey papers. arXiv preprint arXiv:2510.09686, 2025.
[23] Jiachen Liu, Jiaxin Pei, Jintao Huang, Chenglei Si, Ao Qu, Xiangru Tang, Runyu Lu, Lichang Chen, Xiaoyan
     Bai, Haizhong Zheng, Carl Chen, Zhiyang Chen, Haojie Ye, Yujuan Fu, Zexue He, Zijian Jin, Zhenyu Zhang,
     Shangquan Sun, Maestro Harmon, John Dianzhuo Wang, Jianqiao Zeng, Jiachen Sun, Mingyuan Wu, Baoyu
     Zhou, Chenyu You, Shijian Lu, Yiming Qiu, Fan Lai, Yuan Yuan, Yao Li, Junyuan Hong, Ruihao Zhu, Beidi Chen,
     Alex Pentland, Ang Chen, Mosharaf Chowdhury, and Zechen Zhang. The last human-written paper: Agent-native
     research artifacts. arXiv preprint arXiv:2604.24658, 2026.
[24] Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. The ai scientist:
     Towards fully automated open-ended scientific discovery. ArXiv, abs/2408.06292, 2024. URL https:
     //api.semanticscholar.org/CorpusID:271854887.
[25] Robert K Merton. The sociology of science: Theoretical and empirical investigations. University of Chicago
     press, 1973.
[26] Miryam Naddaf. Major ai conference flooded with peer reviews written fully by ai. Nature, 648(8093):256–257,
     2025.
[27] Miryam Naddaf and Elizabeth Quill. Hallucinated citations are polluting the scientific literature. what can be
     done? Nature, 652(8108):26–29, 2026.
[28] Guanxiong Pei and Huajian Huang. Open science falling behind in the era of artificial intelligence. Frontiers in
     Research Metrics and Analytics, 10:1595824, 2025.
[29] Yusuke Sakai, Hidetaka Kamigaito, and Taro Watanabe. Hallucitation matters: Revealing the impact of hallucinated
     references with 300 hallucinated papers in acl conferences. arXiv preprint arXiv:2601.18724, 2026.
[30] David Shotton. Semantic publishing: the coming revolution in scientific journal publishing. Learned Publishing,
     22(2):85–94, 2009.
[31] David Shotton. Cito, the citation typing ontology. Journal of biomedical semantics, 1(Suppl 1):S6, 2010.
[32] Guijin Son, Jiwoo Hong, Honglu Fan, Heejeong Nam, Hyunwoo Ko, Seungwon Lim, Jinyeop Song, Jinhang Choi,
     Gonccalo Paulo, Youngjae Yu, and Stella Biderman. When ai co-scientists fail: Spot-a benchmark for automated
     verification of scientific research. ArXiv, abs/2505.11855, 2025. URL https://api.semanticscholar.org/
     CorpusID:278740501.
[33] Diomidis Spinellis. False authorship: an explorative case study around an ai-generated article published under my
     name. Research Integrity and Peer Review, 10(1):8, 2025.
[34] Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao Huang. Ai-researcher: Autonomous scientific innovation.
     arXiv preprint arXiv:2505.18705, 2025.
[35] Nitya Thakkar, Mert Yuksekgonul, Jake Silberg, Animesh Garg, Nanyun Peng, Fei Sha, Rose Yu, Carl Vondrick,
     and James Zou. A large-scale randomized study of large language model feedback in peer review. Nature Machine
     Intelligence, pages 1–11, 2026.
[36] Stephen E Toulmin. The uses of argument. Cambridge university press, 2003.
[37] David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh
     Hajishirzi. Fact or fiction: Verifying scientific claims. In Proceedings of the 2020 Conference on Empirical
     Methods in Natural Language Processing (EMNLP), pages 7534–7550, 2020.


                                                         12
                                         Toward an Engineering of Science                            W ORKING PAPER



[38] David Wadden, Kyle Lo, Bailey Kuehl, Arman Cohan, Iz Beltagy, Lucy Lu Wang, and Hannaneh Hajishirzi.
     Scifact-open: Towards open-domain scientific claim verification. In Findings of the Association for Computational
     Linguistics: EMNLP 2022, pages 4719–4734, 2022.
[39] Yidong Wang, Qi Guo, Wenjin Yao, Hongbo Zhang, Xin Zhang, Zhen Wu, Meishan Zhang, Xinyu Dai, Min
     Zhang, Qingsong Wen, et al. Autosurvey: Large language models can automatically write surveys. Advances in
     neural information processing systems, 37:115119–115145, 2024.
[40] Qiyao Wei, Samuel Holt, Jing Yang, Markus Wulfmeier, and Mihaela van der Schaar. The ai imperative: Scaling
     high-quality peer review in machine learning. arXiv preprint arXiv:2506.08134, 2025.
[41] Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David Ha.
     The ai scientist-v2: Workshop-level automated scientific discovery via agentic tree search. ArXiv, abs/2504.08066,
     2025. URL https://api.semanticscholar.org/CorpusID:277741107.
[42] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger,
     and Animashree Anandkumar. Leandojo: Theorem proving with retrieval-augmented language models. Advances
     in Neural Information Processing Systems, 36:21573–21612, 2023.




                                                         13
