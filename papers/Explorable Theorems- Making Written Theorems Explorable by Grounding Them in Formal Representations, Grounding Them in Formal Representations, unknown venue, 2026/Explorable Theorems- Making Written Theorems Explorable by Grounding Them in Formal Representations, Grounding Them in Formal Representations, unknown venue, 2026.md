                                          Explorable Theorems: Making Written Theorems Explorable by
                                                   Grounding Them in Formal Representations
                                                     Hita Kambhamettu                                     Will Crichton                               Sean Welleck
                                                  hitakam@seas.upenn.edu                             will_crichton@brown.edu                   swelleck@andrew.cmu.edu
                                                  University of Pennsylvania                             Brown University                      Carnegie Mellon University
                                                    Philadelphia, PA, USA                               Providence, RI, USA                       Pittsburgh, PA, USA

                                                                             Harrison Goldstein                               Andrew Head
                                                                              hgoldste@buffalo.edu                        head@seas.upenn.edu
                                                                              University at Buffalo                     University of Pennsylvania
arXiv:2604.02598v2 [cs.HC] 10 Apr 2026




                                                                               Buffalo, SUNY, USA                         Philadelphia, PA, USA

                                                                                         2
                                                                                             Execute proof steps

                                                                 1                               [         ]
                                                                 Lean proof
                                                                                                 [         ]                             4
                                                                                                                                          Work out examples
                                                                                                 [         ]                x=

                                                                                             3
                                                                                             Dependency graph


                                                                                                                                                used by step E


                                                                                                                                  5
                                                                                                                                   See proof dependencies

                                         Figure 1: Explorable theorems enlivens a static written proof with explorability affordances derived by analyzing and executing
                                         a linked formal machine proof. Given a written proof, a corresponding machine-checkable Lean proof is generated (○).     1 Structural and
                                         semantic information is derived by executing steps of the Lean proof (○)  2 and extracting logical dependencies (○).
                                                                                                                                                            3 This information is
                                         plugged into the written proof, allowing readers to use it as an explorable text. They can ask questions about whether a theorem holds on
                                         one or another example, the bounds of applicability, how the math “works out” for individual examples, and where counterexamples fail (○).
                                                                                                                                                                                4
                                         They can also ask questions about why propositions matter and where they come from by tracing to their definitions and uses (○).5


                                         Abstract                                                                   potential advantages of this approach: in a proof-reading task, par-
                                         LLM-generated explanations can make technical content more ac-             ticipants who had access to the provided explorability features gave
                                         cessible, but there is a ceiling on what they can support interactively.   better, more correct, and more detailed answers to comprehension
                                         Because LLM outputs are static text, they cannot be executed or            questions, demonstrating a stronger overall understanding of the
                                         stepped through. We argue that grounding explanations in a formal-         underlying mathematics.
                                         ized representation enables interactive affordances beyond what
                                         static text supports. We instantiate this idea for mathematical proof      CCS Concepts
                                         comprehension with explorable theorems, a system that uses LLMs            • Human-centered computing → Interactive systems and tools.
                                         to translate a theorem and its written proof into Lean, a program-
                                         ming language for machine-checked proofs, and links the written            Keywords
                                         proof with the Lean code. Readers can work through the proof at a          explorable explanations, AI-augmented proof reading, formal rep-
                                         step-level granularity, test custom examples or counterexamples,           resentations
                                         and trace the logical dependencies bridging each step. Each worked-
                                         out step is produced by executing the Lean proof on that example           1   Introduction
                                         and extracting its intermediate state. A user study (𝑛 = 16) shows         Artifacts that require formal reasoning, such as mathematical proofs [46,
                                                                                                                    47], programs [28, 30], or logical arguments [24, 35], can be difficult
                                                                                                                                Kambhamettu et al.


to understand through reading alone. To illustrate this challenge          theorem and proof, our system first formalizes them by generating
within the domain of mathematics, consider this theorem:                   its corresponding Lean theorem and proof. Lean is a programming
        Let 𝑎, 𝑑 ∈ N with gcd(𝑎, 𝑑) = 1. Then there are                    language for writing machine-checked proofs [10]. While Lean
        infinitely many prime numbers 𝑝 such that                          proofs sometimes diverge from the structure of written proofs,
                                                                           they can be analogous in areas of math like algebra and in proof
                           𝑝 ≡𝑎      (mod 𝑑).
                                                                           structures relying on forward-based reasoning. These cases allow
   This theorem says: pick any two numbers 𝑎 and 𝑑 that share no           for a natural linking between written and Lean proofs, which we
common factors; then infinitely many primes will leave remainder           utilized in our running examples and study tasks.
𝑎 when divided by 𝑑. To get a feel for it, a reader might instantiate it       Because Lean proofs are executable, the system can run the
at 𝑎 = 1, 𝑑 = 4, where gcd(1, 4) = 1 holds, and check which primes         proof on any concrete input and extract its intermediate states, the
have remainder 1 when divided by 4, seeing enough primes that              formal record of what is known and what remains to be shown
they get a sense that they might go on forever:                            at each step of the proof. These intermediate states also convey
                 5, 13, 17, 29, 37, · · · ≡ 1   (mod 4).                   which propositions were used in each step of the proof, building
                                                                           up a dependency graph of it. These structures are what ground
    They might then ask: why is this condition necessary? At 𝑎 = 2,
                                                                           a reader’s explorations: a reader can choose any example, step
𝑑 = 4, where gcd(2, 4) ≠ 1, only 𝑝 = 2 satisfies 𝑝 ≡ 2 (mod 4). All
                                                                           through the proof as it applies to that example, and see how each
other numbers in this progression (6, 10, 14...) are multiples of 2 and
                                                                           proof step’s conclusion follows from the ones before it.
thus composite. This clarifies why gcd(𝑎, 𝑑) = 1 is necessary: if 𝑎
                                                                               We evaluate explorable theorems in a user study (𝑛 = 16) against
and 𝑑 share a common factor, all numbers in the sequence will share
                                                                           a chatbot baseline, an increasingly common way readers currently
that factor, limiting the sequence to at most one prime. Through this
                                                                           seek help with proofs [69]. Participants using explorable theorems
exercise, the reader is not just reading but exploring the theorem
                                                                           produced more correct answers to proof-comprehension questions,
and its bounds: choosing inputs, running the theorem against them,
                                                                           referenced more explicit proof steps, and demonstrated stronger
and using the results to build a working model of what the theorem’s
                                                                           understanding of the underlying mathematical concepts. An expert
bounds are, and why they exist. This kind of active engagement,
                                                                           judged their open-ended responses to be more correct and more
illustrating abstract assertions through concrete examples, is a well-
                                                                           reflective of the underlying mathematics.
documented strategy for effective proof reading [63].
                                                                               We conclude with discussing how by grounding content to an
    AI tools are being increasingly used for math education [37, 43].
                                                                           underlying formal representation, it becomes an inspectable arti-
While these tools have been shown to support general mathematical
                                                                           fact that users can probe directly by reviewing concrete instances,
understanding [26, 37], generated text outputs do not naturally
                                                                           tracing logical dependencies, and actively investigating boundary
support this kind of active interaction. This is because freeform text
                                                                           conditions made visible by the system. Mathematical proofs rep-
cannot be executed or queried, meaning the reader cannot tinker
                                                                           resent an instantiation of this principle, and we discuss how these
with AI outputs. While a user might try to simulate this exploration
                                                                           design implications extend to other structured domains.
by repeatedly prompting the AI, this just generates disconnected
                                                                               This paper contributes:
outputs. The reader is never interacting with the mathematical
structure, but rather reifying different copies of generated outputs.            • The idea of grounding LLM-generated explanations in for-
In this work we ask: how can we combine the convenience of AI                       mal representations to enable interactive affordances that
explanations with the exploration necessary for understanding a                     freeform text cannot support.
formal domain like math?                                                         • Explorable theorems, a system that instantiates this idea for
    We argue that grounding the written math in a formal repre-                     mathematical proofs, using Lean as the formal backing for
sentation can enable interactive affordances that text alone cannot                 reader-steerable, example-driven proof exploration.
support. This idea has precedent in explorable explanations [58],                • Results from a user study (𝑛 = 16) demonstrating that
digital mediums that integrate narrative with computational models                  formally grounded exploration leads to better proof com-
to let readers manipulate parameters and observe consequences.                      prehension than a chatbot baseline.
    Recent HCI research has sought to support active reading by
grounding unstructured text in a structured representation. For
                                                                           2 Background and Related Work
example, AbstractExplorer [14] organizes freeform text into struc-         2.1 ∀𝑥 ∈ {theorem, proof}, hard(𝑥)
tured relational schemas to help readers compare information across        Prior work states that proof comprehension is challenging for learn-
documents. DataTales [51] connects narrative text to datasets, cre-        ers [16, 49, 50]. Effective proof reading is said to be through active
ating interactive links between prose and visualizations. More re-         reconstruction, including working through examples and connect-
cently, VeriPlan [27] uses formal model checkers to verify natural         ing individual steps to the overall structure of the argument [63].
language plans. These systems demonstrate that using structured            The ability to move fluidly between these representations of math
representations unlocks richer interactive reading affordances. Yet,       is a critical difference between a math expert, who can look for the
the structures in these prior works largely operate post-hoc, serving      big picture [33, 62], seek out reusable methods [64], and strategi-
primarily to organize or verify static outputs.                            cally use examples to test assertions [62, 64], and a novice, who
    We extend this idea, both in terms of active interaction and strict    might reason through proofs in the abstract, failing to employ con-
formality, to the domain of mathematical proof comprehension,              crete examples that would help them develop intuition around the
instantiating it as explorable theorems. Given a natural-language          meanings of theorems and assertions [38].
Explorable Theorems


    This matters especially when AI tools are being increasingly          The value of explorable explanations for communicating complex
used for math education [48, 61]. While AI can support learning,       technical concepts is well-established, evidenced by the success of
it risks exacerbating the passivity that already hinders proof com-    science simulations like PhET [67] and interactive scientific journals
prehension: students may accept generated explanations without         like Distill [40]. More closely related to our approach, Augmented
evaluating arguments or reconstructing why a proof works [69].         Math and Augmented Physics [7, 15] make static mathematical
As Yoon et al. [69] argue, when students rely on AI as an authority    notation manipulable. While these systems scaffold the reading of
figure, it hinders their own critical thinking. We share this view.    formulas, they operate at the level of syntactic rewriting and do
Rather than generating explanations for readers to passively con-      not evaluate the underlying mathematical logic. They lack a global
sume, explorable theorems supports active exploration by providing     understanding of the mathematical argument’s structural integrity,
structured ways to inspect examples and trace logical steps. Our       especially the ability to verify the logical flow between multiple
user study demonstrates the impact of this engagement: compared        steps or check the validity of a long-form proof. Our work extends
to a chatbot baseline, participants using explorable theorems wrote    beyond this presentation-level manipulation. By grounding written
proofs with significantly more explicit mathematical steps, richer     proofs in a formal representation, we enable readers to verify the
detail, and a stronger grasp of the underlying concepts.               underlying semantic logic, explore concrete instances of abstract
                                                                       steps, and trace dependencies across the entire document.
2.2 𝑥 ↦→ example(𝑥)
Prior HCI research has contributed ways to make mathematical           2.3    LLMs ∩ Lean
documents more accessible through visual augmentation. Early           A formal representation of mathematical logic helps us generate
probes envisioned dynamic interfaces with annotations and ad-          explorable explanations for explorable theorems. The formal repre-
justable tracing [12], while recent work has documented [19] and       sentation we use is Lean [11]. Lean is an interactive theorem prover
operationalized [54, 68] practices for styling and labeling typeset    and functional programming language. It works by allowing users
math. While these approaches help readers understand notation          to write tactics, commands that incrementally transform a math-
and derivations, they do not structurally ground abstract proofs       ematical goal into known premises, relying on correspondences
in concrete, executable instances. A second line of work makes         where propositions are treated as types and proofs as programs
mathematical documents interactive. Systems introduce reactive         [39]. Lean belongs to a broader family of proof assistants, such as
documents with scrubbable values [60], direct manipulation of alge-    Rocq and Isabelle, which provide computational frameworks for
braic notation through gesture-based interaction [65], interactive     formalizing mathematics and verifying logical correctness [17].
math notation in academic papers [8], and executable math pa-             Proof assistants can be useful for mathematics education because
pers [29]. Specific to theorems, Alcock and Wilkinson [2] make         they provide immediate feedback and demand a level of logical un-
hidden logical structures explicit by using visual annotations to      ambiguity from students. This direction has been explored by sys-
link individual statements to their premises. However, while these     tems like Verbose Lean [32] and Waterproof [66]. However, proof
manually authored “e-Proofs” were popular with students, they did      assistants may not be used as a de facto format for mathematical
not yield measurable improvements in proof comprehension [1],          communication due to their steep learning curve. Their highly spe-
highlighting the difficulty of designing effective augmented proofs.   cialized syntax, combined with the inherent rigidity and verbosity
This pattern of visual linkage has been carried forward by dedi-       of full formalization, makes them inaccessible to those who are not
cated practitioners. For instance, Rougeux and Byrne [45] developed    domain experts[36]. There are several efforts to make formalized
an interactive adaptation of Byrne’s Euclid that connects written      proofs more communicative, such as translating code into natural
geometric proof steps directly to color-coded diagrams, making         language [32], or using Alectryon [44] and Lean widgets [57] to
these diagrams sort of visual proofs. Yet, producing such deeply       expose the rich proof-state information that is often hidden in the
integrated artifacts is exceedingly labor-intensive.                   source text. These experiments have demonstrated that formalized
   While existing interactive documents make notation reactive         proofs contain a wealth of information that can be extracted and
and manipulable, they do not support a reader actively exploring       channeled back to the user. We build on this by piping that infor-
a proof on their own terms. This need for active exploration is        mation directly into a written mathematical proof. Additionally,
articulated by Bret Victor’s “explorable explanations” [58] and Kill   current interfaces are primarily built for authoring and verifying
Math projects [59], which use interactive simulations to shift math-   rather than exploring. We enable a more active exploration.
ematical understanding away from abstract symbols and toward              Towards this, we use LLMs to translate theorems and their writ-
more tangible, dynamic representations. While Victor advocates for     ten proofs into Lean. While recent advances show that LLMs are
bypassing conventional notation entirely, our approach serves as a     increasingly capable of generating valid Lean code [22, 31], the ma-
bridge, connecting tangible exploration back to the formal proof.      chine learning community has primarily treated formalization as a
This is conceptually similar to “concreteness fading,” an instruc-     benchmark [70] for automated reasoning, optimizing for whether
tional technique that transitions students from concrete manipula-     a proof successfully compiles, not whether it can be used to help
tives to formal mathematical representations [25]. In the domain       someone understand written argument. Designing pipelines that
of mathematics, these methods align with the “proceptual” model        reliably follow these human-centric structural properties remains
[13], which asserts that learners build understanding by connecting    largely underexplored. Our work proposes a generation pipeline
concrete processes to their abstract expressions.
                                                                                                                                                 Kambhamettu et al.


that incorporates these properties, presenting the first HCI sys-
tem that integrates LLMs and formal proof assistants to create
explorable explanations of theorems.
                                                                                                                              1   theorem input slider
3     System
Provided the right underlying formalism is found, features in ex-
plorable theorems could serve as a general design pattern for expla-                                                                 proof step dependencies    3

nations across other formal domains. We instantiate this approach
for the domain of mathematical proofs. This section first describes                                      2   worked out proof step
the design rationale for each interface affordance, then gives the
technical approach used to realize each one.1

3.1     Design
                                                                                                               4   inspecting proof logic
Formalism unlocks a rich set of desirable interactions. We detail
what they are in the case of making theorems explorable.
                                                                                        Figure 2: The explorable theorems interface for the theorem
   Checking bounds of a theorem. When first reading a theorem, a                        “For all integers 𝑥, if 𝑥 > 2, then 𝑥 2 − 1 is not prime”. The input
reader might naturally want to probe its limits: for what values                        slider ○
                                                                                               1 lets readers set a concrete value of 𝑥; color coding indicates
does it hold, and for what values does it not? The theorem input                        where the theorem’s assumption 𝑥 > 2 holds. Each proof step is
slider (see ○
            1 in Figure 2) lets readers evaluate the theorem on any                     instantiated with Lean-verified intermediate values ○:    2 for 𝑥 = 2,
input, giving them a sense of what the theorem is stating. Under the                    the expression 𝑛 = 𝑥 2 − 1 evaluates to 3. Clicking a variable such
hood, the system runs the Lean proof on each input and surfaces                         as 𝑛 reveals the downstream proof steps that depend on it ○.  3 When
whether the theorem holds or breaks down at that value.                                 the concrete value violates the theorem’s assumptions, the interface
   Following steps of a proof. Once a reader understands what the                       flags exactly where the proof breaks ○,  4 making the role of each
theorem claims, they may want to read its proof. For each step of                       assumption legible to the reader.
the written proof, the system displays a worked example (see ○  2
in Figure 2) that instantiates the step’s reasoning with concrete                       3.2    Components
values, helping the reader see exactly what each step amounts to.
To enable this, the system extracts intermediate values from the                        The guiding principle of our implementation is a tight coupling
Lean proof state on example values for the theorem’s parameters                         between a prose proof and its formal Lean representation: interac-
chosen from the slider, or for any example values provided by                           tions on the interface side, such as checking bounds of a theorem,
the user in a custom value input widget. The system then inserts                        following steps of a proof, or tracing provenance of a proposition,
the intermediate values into generated templates that mirrors the                       are grounded in the formal Lean theorem and proof. The pipeline
structure of the written step.                                                          that achieves this coupling consists of four broad components: (1)
                                                                                        aligned generation, in which a Lean proof is generated that is struc-
    Tracing provenance of a proposition. Proofs can be difficult to                     turally similar to the written proof; (2) link-making, in which an
follow, especially when a step references facts established much                        LLM maps Lean tactics and variables to their corresponding written
earlier. It can also be unclear, on a first read, why a particular step                 steps and symbols; (3) dependency recovery, in which proof state
is necessary. The proof step dependencies (see ○   3 in Figure 2) lets a                diffs expose which facts each tactic introduces and consumes; and
reader click a proposition in a proof step to see which earlier steps                   (4) execution, in which the proof is run on concrete inputs to extract
it depends on and which later steps build on it, making the logical                     intermediate values. Each component involves design decisions
structure of the proof navigable. This is enabled by constructing a                     oriented toward making the coupling as tight as possible, making
dependency graph over propositions in the Lean proof and mapping                        sure the formal representation and natural-language representation
it back to the corresponding propositions in the written proof.                         structurally aligned with one another.
   Understanding conditions of a theorem. It can be difficult to un-                       Aligned generation of Lean proof. Given a theorem and its prose
derstand why a theorem is stated the way it is, particularly why                        proof, we use a coding agent, Claude Opus 4.6, to generate a corre-
a particular assumption is necessary. By sliding to an input that                       sponding Lean proof (see ○   1 in Figure 3). In Lean, a proof is written
violates the theorem’s conditions, a reader can inspect the proof                       as a sequence of tactics, instructions that are applied to the current
logic (see ○
           4 in Figure 2) and see exactly which step breaks down,                       proof state (the set of known hypotheses and the remaining goal)
making the role of each assumption legible. Under the hood, the                         until nothing is left to prove. To attempt to align the generated
system evaluates the Lean proof state on the given input and flags                      Lean proof to the original one, we instruct the agent to follow three
steps at which the proof no longer holds.                                               rules. First, it should build up propositions in the same order as the
1 A more scenario-centric view of the interface can be accessed in the usage scenario   prose. Second, the proof must use have statements, which introduce
in the Appendix A.1.                                                                    named, inspectable intermediate propositions into the proof. Third,
                                                                                        each block of have statements should correspond to a step in the
                                                                                        written proof. The agent annotates each Lean step with a comment
Explorable Theorems


                                                                                                   1
identifying its corresponding prose step, and is instructed to use                                     Lean step
variable names that match values in the written proof.
                                                                                                       2           3
   Link-making. We pass the Lean and written proofs to an LLM                     Run proof on example                 Check for dependencies
(GPT-5.1), which outputs a mapping from Lean proof steps to writ-                                                              n_def
ten proof steps. The LLM extracts two levels of linkages: linking
                                                                                                                   n=r•s       n>s      n|s
written proof blocks to steps of the Lean proof and linking written                                            4   5
propositions to specific Lean variables. These linkages are used              Template for worked example          Map from Lean to wrien step
throughout the rest of the pipeline to connect the two representa-                                                          n_def        n
tions (see ○
           5 in Figure 3)                                                                                  6
                                                                                         Substitute value
   Dependency recovery. We construct a dependency graph from
the Lean proof (see ○    3 in Figure 3). We instruct Claude Code to
                                                                          Figure 3: The pipeline for grounding interaction affordances
extract the proof state at each tactic step using lean_goal [41],
                                                                          in a formal representation. First, the Lean proof is generated (○).
                                                                                                                                          1
which allows the agent to connect to the Lean compiler. A proof
                                                                          The system executes this proof on concrete inputs and extract the
state is a list of active hypotheses (named facts currently in scope
                                                                          Lean proof state (○).
                                                                                             2 A language model then generates a template
of the proof) together with the current goal. We take the diff of
                                                                          for the proof step worked out on an example (○).4 Lean-computed
consecutive proof states to determine what each tactic introduces
                                                                          values are programmatically substituted into this template (○)6 to
and consumes. The result is a directed acyclic graph whose nodes
                                                                          produce the verified worked example shown to the reader. The
are the facts introduced throughout the proof and whose edges
                                                                          consecutive states of the proof are diffed to create a dependency
encode which earlier facts each new fact references.
                                                                          graph (○).
                                                                                   3 A mapping is created that links Lean statements to
   We also build a step-level dependency graph using the mapping
                                                                          natural-language propositions (○).
                                                                                                          5
from Section 3.2. Each fact node carries a proof step label, indicating
which step of the original written proof it belongs to. From this we
compute four maps: (1) which earlier steps this step relies on, and       to achieve worked examples that were brief, accurate, and infor-
which facts link them, (2) which later steps use facts established by     mative. This suggests the pipeline is tractable for well-structured
this step, (3) the specific facts this step consumes, and (4) the facts   undergraduate-level proofs. More complex proofs might surface
this step introduces.                                                     additional failure modes, which we discuss in future work.
                                                                             We also acknowledge some limitations to our approach. We
   Execution. To run the Lean proof on concrete values (see ○    2 in
                                                                          ground each limitation in examples drawn from a case-study evalu-
Figure 3), we first create a temporary copy of each have statement
                                                                          ation on two theorems in number theory from the ProofNet bench-
in the Lean proof, wrapped in a try block. Substituting a concrete
                                                                          mark [4], which is a set of undergraduate math theorem statements,
value (such as 𝑥 = 5) into a generalized proof would normally com-
                                                                          their natural language proofs, and the Lean formalization of the
plete the proof prematurely; the try block isolates execution so
                                                                          theorem statement (but not the proof): Theorem 1 (for all odd 𝑛,
that only the current step is evaluated against that value. We add an
                                                                          8 | 𝑛 2 − 1) and Theorem 2 (3𝑥 2 + 2 = 𝑦 2 has no integer solution).
extra hypothesis to the try statement fixing the input variable to a
concrete value, then use the subst tactic to substitute that value           Block-to-step mapping. We use an LLM to map natural-language
through the proof’s hypotheses, followed by simp and rfl, Lean’s          sentences to Lean code, which can be wrong when the prose and
built-in simplification and equality-checking tactics, to reduce in-      Lean proofs follow different proof strategies. In Theorem 1, for
termediate arithmetic. The resulting intermediate proof states, the       instance, the written proof factors 𝑛 2 − 1 as (𝑛 + 1)(𝑛 − 1) while
computed values of all intermediate expressions and sub-goals up          the Lean proof substitutes 𝑛 = 2𝑘 + 1; the LLM matches these
to that point, are saved to JSON. A language model (GPT-5.1) is           correctly, but the algebraic mismatch can still affect downstream
then prompted with this JSON state alongside the corresponding            components. However, our system works with any API-accessible
prose step and instructed to produce a template (see ○  4 in Figure 3),   language model and will improve as frontier models do.
a version of the prose in which abstract quantities are replaced by
                                                                             Dependency graph. Diffing consecutive proof states can make
template keys from the Lean state (for instance, generating xˆ2
                                                                          bookkeeping tactics like rfl appear as spurious nodes, and closing
= {{x}}ˆ2 = {{n_def}}). Concrete values from the Lean proof
                                                                          tactics like omega or contradiction leave no node despite dis-
state are substituted into these templates programmatically and
                                                                          charging the goal (as in Theorem 2, where the final step has no
displayed in the interface (see ○ 6 in Figure 3).
                                                                          incoming edges). Resolving these requires either reasoning about
3.2.1 Technical notes. Our pipeline performs well on the two proofs       the semantic importance of proof steps or deeper analysis of Lean
used in the user study. We characterize its performance on one of the     proof terms, neither straightforward.
proofs (also in Figure 2): dependency edges are correctly recovered
for seven of the eight proof steps, with one partial recovery, and        4   Study
worked example templates are correctly instantiated for all steps         To assess how these sorts of formally-backed explorable features
at 𝑥 = 2. Lean proof generation required two manual iterations            might support exploration and understanding, this study focused
before producing a proof that compiled and satisfied our struc-           on the comparison of explorable theorems to reasonable modern
tural constraints, and template generation required three iterations
                                                                                                                                             Kambhamettu et al.


alternative for explaining theorems, a written proof plus chatbot,      theorems tool, this included sliding the input slider, viewing the
with fixed theorem review tasks and success assessments.                proof worked out step by step, trying their own examples, and ex-
   We structured our study around the following questions:              ploring proof dependencies. Each tool was introduced immediately
     • RQ1: How does the addition of the explorability features         before the task in which it was used.
        affect understanding of the original written artifact?             Tasks. Participants completed two theorem-understanding tasks.
     • RQ2: Do readers use the explorability features and if so,        The theorems can be found in Appendix B. In each task, they were
        how do they shape the reading process?                          instructed to study a theorem and its proof well enough to answer
   Participants. We recruited participants who were comfortable         detailed questions from memory, “as if preparing for a short quiz.”
reading mathematical proofs at the undergraduate level. All 16 re-      Each task lasted 15 minutes. Participants began by reading the
cruited participants were bachelor’s students in computer science,      first theorem and its proof, then advanced to the second theorem
recruited from academic mailing lists at a university. 15 had com-      and proof when they felt ready. If they had not moved on by the
pleted an introductory proof course and 11 had taken advanced           10-minute mark, they were prompted to do so2 .
coursework requiring proofs (participants could select multiple op-        Following the theorem-understanding tasks, participants an-
tions here). After the study, 11 participants rated themselves very     swered five proof-comprehension questions per theorem, adapted
familiar with proofs of the complexity used in the study, 4 rated       from established proof assessment models [9, 34]. These questions
themselves familiar, and 1 somewhat familiar.                           can be found in Appendix B.2. The first required participants to
                                                                        summarize the proof in their own words; this was used for a com-
   Baseline. In this condition, participants were provided with the     parative judgement of proof summaries, a measure of student com-
exact same written theorem and proof text used in the explorable        prehension quality stated in prior literature [9]. The remaining four
theorems condition. We selected the Gemini [56] chatbot as our          questions followed from established dimensions of proof compre-
baseline. Participants were given access to a set of pre-written        hension [34]3 .
prompts that they could copy and paste directly into the Gemini            To assess recall of proof structure, participants completed a Par-
interface. These prompts were designed to support proof compre-         sons puzzle [42] after each theorem, reconstructing the proof from
hension in ways that explorable theorems does: (1) providing the        memory. Each puzzle presented the proof steps in scrambled order,
theorem and proof as context alone, and (2) prompting Gemini to         with ordering words such as “first” and “lastly” removed, alongside
explain how the proof applies to a specific value, given the the-       3–4 fabricated distractor steps. Participants arranged the steps into
orem statement and proof as context. Participants were also free        the correct order. Regardless of tool order, participants always com-
to ask Gemini any question of their choosing. This choice was           pleted the comprehension questions and corresponding puzzle for
motivated by two considerations. First, Gemini has demonstrated         the first theorem before moving on to the second.
strong performance on general-purpose mathematical reasoning
and zero-shot proof generation [21]. Second, using an AI chatbot           Questionnaires. Participants completed three sets of question-
as a baseline reflects a modern and increasingly tool used in math      naires during the session. After each theorem-understanding task,
education [37, 43], allowing us to directly compare two ways to         they completed a subset of the NASA-TLX workload assessment [18]
read proofs: interacting with a chatbot versus using the explorable     and reported the usefulness of the tool and its individual features
theorems system. In our pilot tests, Gemini yielded correct answers,    on 4-point usefulness scale (not at all useful, somewhat useful, use-
so any differences in comprehension outcomes are less likely attrib-    ful, very useful). After completing both the proof-comprehension
utable to the correctness of the mathematical content presented.        questions and the proof-ordering puzzle, participants filled out a
                                                                        final questionnaire about their experience using both tools.
   Procedure. Each participant completed a one-hour study session.
The study was conducted as a remote session. Participants accessed          Measurements and analysis. To optimize our evaluation resources,
the web-based study interfaces through their own computers, with        we split the grading process between two evaluators based on
remote access provided through a locally hosted deployment ex-          the nature of the assessment. A senior computer science faculty
posed via ngrok. Sessions included screen recording and either          member with experience teaching proof-based mathematics ranked
audio recording or researcher note-taking, depending on partici-        participants’ proof summary responses using a TrueSkill ranking
pant preference. To minimize demand characteristics, we referred        model [20]. Rather than requiring full pairwise comparisons across
to tools with neutral names (“Tool S” for explorable theorems and       all 16 responses, which would demand 120 judgments, we used an
“Tool R” for the baseline). We counterbalanced the order in which       adaptive design with a fixed budget of 40 comparisons per condition,
participants used the tools. After consenting and filling out a back-   yielding approximately 5 comparisons per response. Pair selection
ground questionnaire, participants completed a short tutorial, two      was adaptive: responses were initialized with equal ratings, and
proof understanding tasks, two sets of proof-comprehension ques-        at each step the algorithm selected the most closely matched pair
tions, and two proof-ordering puzzles.                                  2 This soft time limit ensured that participants had at least 5 minutes to study the second
                                                                        theorem, as one comprehension question required understanding both theorems and
   Tutorial. Before beginning the tasks, participants completed a       their proofs. Additionally, there was also a prototype feature for comparing proofs; it
guided tutorial. We introduced the features of each tool and had par-   appeared useful, but it was not the main focus of this analysis
                                                                        3 These included justifying internal dependencies (such as why a specific mechanism
ticipants complete short exercises practicing each afforded feature.    was used), tracing inferences through a concrete example to verify the necessity of
For example, for the baseline condition, this included copying and      premises, interrogating the theorem’s assumptions, and identifying shared strategies
pasting prompts and prompting Gemini freely. For the explorable         across both studied proofs.
Explorable Theorems


for comparison, updating quality estimates via TrueSkill after each
judgment. The expert was blind to which condition each summary
was written from.
   For the fine-grained response evaluation, a computer science
graduate student with prior discrete math teaching experience
evaluated each response along three rubric dimensions adapted
from an established proof comprehension assessment model [34],
designed to capture different aspects of proof understanding: (1)
correctness, (2) whether the response referenced specific steps of
the proof (a proxy for evaluating rigor of the proof summary [55]),                         Figure 4: Instructor preferences by condition. Box plot shows
and (3) whether it illustrated reasoning with concrete examples.                            the distribution of TrueSkill ratings assigned to participant re-
The grader was blind to condition. The same grader then performed                           sponses through pairwise comparisons by a mathematics instruc-
a comparative ranking of all responses, pooled across tasks and                             tor, combined across both study tasks. The instructor preferred
conditions, along dimensions of mathematical understanding, level                           responses written with explorable theorems in 94.9% of pairwise
of detail, and clarity, assigning each response to one of five evenly                       comparisons.
distributed tiers. This forced distribution allows tier assignments
to serve as a relative measure of quality.                                                     Consider the following example. Participants were asked to de-
   We used non-parametric tests for our analyses. We used Mann–                             scribe the proof of this theorem, “For all integers 𝑛, 𝑛(𝑛 + 1) (𝑛 +
Whitney 𝑈 tests for between-subjects comparisons of correctness                             2)(𝑛 + 3) + 1 is a perfect square”, in their own words.
scores (0–3 ordinal scale), rubric dimension ratings, and TrueSkill
instructor ratings, reporting Cohen’s 𝑑 as the effect size. For binary                         Answer A (with explorable theorems).
outcomes (whether participants referenced specific proof steps or                                  𝑝 = the product of the first and last term 𝑛(𝑛 + 3),
included concrete examples), we used Fisher’s exact tests. When                                    (𝑛 + 1)(𝑛 + 2) becomes 𝑝 + 2. multiply the outer
pooling responses across both tasks, where each participant con-                                   numbers 𝑛 · (𝑛 + 3) = 𝑛 2 + 3𝑛 to be 𝑝 and inner
tributes data in both conditions, we used Wilcoxon signed-rank                                     numbers (𝑛+1) · (𝑛+2) = 𝑛 2 +3𝑛+2 to be 𝑞. note that
tests, reporting Cohen’s 𝑑𝑧 as the paired effect size.                                             𝑞 = 𝑝 + 2. so then 𝑝 ·𝑞 = 𝑝 · (𝑝 + 2) = 𝑝 2 + 2𝑝, add 1 =
   For the proof puzzle, we compared position accuracy, pairwise                                   𝑝 2 +2𝑝 +1 = (𝑝 +1) 2 . then 𝑝 = 𝑛 2 +3𝑛, substitute this,
accuracy, and behavioral metrics between conditions using paired                                   and you get the whole thing (𝑝 + 1) 2 = (𝑛 2 + 3𝑛 + 1) 2
𝑡-tests and Wilcoxon signed-rank tests, reporting Cohen’s 𝑑𝑧 , and                                 this is a perfect square.
applied McNemar’s test for perfect solve rate (a binary outcome).                              Answer B (with baseline).
For Likert-scale responses we used two-tailed Wilcoxon signed-
                                                                                                    We group the middle terms together and the outer
rank tests, and tool preference was evaluated with a binomial test
                                                                                                    terms together, forming 𝑝 and 𝑞. Then we write 𝑞
against chance (𝑝 = 0.5).
                                                                                                    in terms of 𝑝 and factor the remaining expression,
   We analyzed open-ended responses through thematic analy-
                                                                                                    which shows that it is a perfect square in terms of 𝑝.
sis [6]: one author performed open coding to identify recurring
                                                                                                    We then substitute the expression for 𝑝 back in to get
ideas, which were then refined into key themes. We also conducted
                                                                                                    a perfect square in terms of 𝑛.
video analysis of interaction patterns for the 12 participants who
consented to recording.4                                                                       When asked which answer was better in terms of answer quality,
                                                                                            the instructor chose Answer A and explained:
5     Explorable theorems...                                                                        I would give Answer A full points. Answer B is impre-
Here, we report the results from our usability study.                                               cise and can be interpreted the wrong way...students
                                                                                                    must learn to formulate math answers precisely, and
5.1      ...improves proof comprehension (RQ1)                                                      using math notation is necessary for that.
Our evaluation provides evidence that participants’ written restate-                           When another grader graded these proofs individually, we found
ments of proofs were judged by an instructor to better demonstrate                          that proof summaries written after using explorable theorems were
knowledge of the proof with explorable theorems than with the                               graded to be of higher quality in the following ways: they were
baseline. A mathematics instructor preferred responses written                              graded as including significantly more explicit proof steps for Task
with explorable theorems significantly more often than responses                            1 (100% vs 38%, p=.026) though not for Task 2 (100% vs 57%, p=.077),
written with the baseline (see Figure 4), and these responses also                          to demonstrate significantly more understanding of the underlying
received significantly higher grades across both study tasks (Task                          mathematical concepts, were significantly easier to follow, and were
1: ET preferred in 90.6% of pairwise comparisons, U=58.0, p=.005,                           significantly more detailed (Task 1: U=53.5, p=.025, d=1.41; Task
d=2.14; Task 2: ET preferred in 93.8% of pairwise comparisons,                              2: U=56.5, p=.010, d=1.78).5 Proof summaries were also graded to
U=60.0, p=.002, d=3.47).                                                                    be significantly more correct for Task 2 (U=46.0, p=.022, d=1.45)
                                                                                            though not for Task 1 (U=40.0, p=.129, d=0.66).
4 Four participants did not consent to video recording and are excluded from interaction-
                                                                                            5 The test statistics for understanding, clarity, and detail were identical across both
level analyses.
                                                                                            tasks, suggesting these dimensions were highly correlated in the grader’s assessments
                                                                                            and may reflect a single latent quality factor.
                                                                                                                                 Kambhamettu et al.


                                                                            5.2    ...does not affect ability to recall proof order
                                                                                   (RQ1)
                                                                            Participants performed similarly in both conditions on the proof-
                                                                            order recall task. Position accuracy, task duration, and number of
                                                                            moves did not differ significantly between conditions.
                                                                               Position accuracy was high in both conditions (ET: 𝑀 = 0.932,
                                                                            𝑆𝐷 = 0.112; Baseline: 𝑀 = 0.951, 𝑆𝐷 = 0.073) and did not differ
                                                                            significantly (paired 𝑡 (15) = −0.610, 𝑝 = 0.551, Cohen’s 𝑑𝑧 = −0.15).
                                                                            Task duration was also similar across conditions (ET: 𝑀 = 148.7s,
                                                                            𝑆𝐷 = 65.4; Baseline: 𝑀 = 157.7s, 𝑆𝐷 = 50.0; paired 𝑡 (15) = −0.559,
                                                                            𝑝 = 0.585, 𝑑𝑧 = −0.14). Likewise, the number of effective moves did
                                                                            not differ significantly (ET: 𝑀 = 33.4, 𝑆𝐷 = 7.5; Baseline: 𝑀 = 31.3,
                                                                            𝑆𝐷 = 8.9; paired 𝑡 (15) = 0.693, 𝑝 = 0.499, 𝑑𝑧 = 0.17). This null
Figure 5: Response quality by condition. Box plots show the dis-            result is informative: participants in both conditions understood
tribution of graded correctness scores and percentage of responses          the surface structure of the proof equally well, suggesting that the
referencing explicit proof steps, combined across both theorem              comprehension gains observed in the written responses between
tasks. Vertical lines within each box indicate the median. Responses        conditions reflect a deeper understanding of proof logic rather than
written after using explorable theorems were graded as significantly        surface-level familiarity of the proof steps.
more correct and referenced specific proof steps more frequently.
                                                                            5.3    ...enables useful interactions (RQ2)
     Beyond summarizing the proof, participants also answered other         Participants reported higher perceived success with explorable
proof comprehension questions. Responses in the explorable theo-            theorems (see Figure 7) (ET: 𝑀 = 6.12, 𝑆𝐷 = 0.72; Baseline: 𝑀 =
rems condition were graded as more correct and referenced specific          5.25, 𝑆𝐷 = 1.18 on a 1–7 scale; Mann–Whitney 𝑈 = 183.0, 𝑝 =
proof steps more often (see Figure 5) than responses in the base-           0.032; Wilcoxon signed-rank 𝑊 = 3.5, 𝑝 = 0.012) and felt less
line condition (correctness: ET 𝑀 = 2.58 vs. Baseline 𝑀 = 1.58;             rushed (ET: 𝑀 = 2.25, 𝑆𝐷 = 1.00; Baseline: 𝑀 = 3.12, 𝑆𝐷 = 1.31;
Wilcoxon signed-rank 𝑊 = 1.5, 𝑝 = .001, 𝑑𝑧 = 1.32; steps refer-             Wilcoxon signed-rank 𝑊 = 3.5, 𝑝 = 0.007). 13 of 16 participants
enced: ET 35% vs. Baseline 12%, 𝑊 = 14.0, 𝑝 = .024).                        (81%) preferred explorable theorems, and 3 of 16 (19%) preferred
     Consider the following examples of participants who received           the baseline (binomial test, 𝑝 = 0.021). There was no significant
the average scores in their respective conditions. In response to a         difference in which tool participants said they would use in the
question about how the theorem “For all integers 𝑛, 𝑛(𝑛 + 1)(𝑛 +            future for understanding math theorems (ET: 𝑀 = 5.62, 𝑆𝐷 = 1.45;
2)(𝑛 + 3) + 1 is a perfect square.” could be further generalized, one       Baseline: 𝑀 = 5.00, 𝑆𝐷 = 1.03; Wilcoxon signed-rank, 𝑝 = 0.114)
participant in the explorable theorems condition wrote:                     or in perceived mental demand (ET: 𝑀 = 3.06, 𝑆𝐷 = 1.65; Baseline:
         “Any case where you’re able to pair the outer terms                𝑀 = 3.56, 𝑆𝐷 = 1.41; Mann–Whitney 𝑝 = 0.281).
         and the inner terms, the second product changes from
                                                                               Feature usefulness. On the 4-point usefulness scale (1=“Not at
         the first by a constant. Then, if you add the right
                                                                            all useful” to 4=“Very useful”), the most useful feature was seeing
         constant to pad that expression, the whole expression
                                                                            mathematical expressions worked out on examples (𝑀 = 3.62,
         becomes a square. So the theorem can be generalized
                                                                            𝑆𝐷 = 0.89), followed by slider colors showing valid and invalid
         by changing the spacing and adjusting the added
                                                                            ranges (𝑀 = 3.56, 𝑆𝐷 = 0.73), and checking whether the theorem
         constant.”
                                                                            holds for a user-defined example (𝑀 = 3.44, 𝑆𝐷 = 0.63). Participants
     A participant in the baseline condition wrote:                         also valued looking up prior dependent steps (𝑀 = 3.31, 𝑆𝐷 =
         “Yes, as long as the pairs of terms have a difference of           0.87) and checking whether an individual proof step holds on an
         a constant there’s a +1 in the end.”                               example (𝑀 = 3.00, 𝑆𝐷 = 0.73). Overall, these ratings suggest that
     The response in explorable theorems identifies the structural          participants found the most value in example-based exploration,
mechanism, that the pairing produces expressions differing by a             though structures that related to proof structure were also useful.
constant, and that adjusting both the spacing and the constant pre-
                                                                               Emergent interactions. We detail how participants used Gemini
serves the perfect square property. The response in the baseline
                                                                            to reveal what kinds of proof understanding they were seeking.
gestures at the right idea (constant difference between pairs) but
                                                                            In the baseline, participants asked an average of 2.8 questions to
incorrectly claims the +1 stays fixed, missing that the added con-
                                                                            Gemini (𝑆𝐷 = 2.4, range 0–9). The 44 total queries fell into three
stant must also change with the spacing (it’s actually 𝑟 4 for spacing
                                                                            broad categories: requesting proof summaries or explanations (17
𝑟 ). Three participants even arrived at the exact generalization of
                                                                            queries, 38.6%), asking about specific numeric examples worked
𝑛(𝑛 + 𝑟 ) (𝑛 + 2𝑟 ) (𝑛 + 3𝑟 ) + 𝑟 4 in the explorable theorems condition.
                                                                            out on the proof (18 queries, 40.9%), and reasoning about proof
                                                                            structure such as individual steps, hypotheses, or conclusions (9
                                                                            queries, 20.5%). One participant (P10) engaged in markedly deeper
                                                                            proof reasoning, all 6 of their questions were about proof steps,
                                                                            hypotheses, and conclusions, asking, for instance, why a particular
Explorable Theorems




                                                                       Figure 7: Self-reported task load by condition. Box plots show
                                                                       the distribution of participant responses on a 1–7 agreement scale
                                                                       for four task load items, comparing explorable theorems to the base-
                                                                       line. Participants felt significantly less rushed and more successful
                                                                       with explorable theorems. No significant differences were found
                                                                       for mental demand or desire to use the tool in the future.

                                                                          A common action at the start of the session was an interaction
                                                                       we term stress testing: participants selected edge-case values to
                                                                       start reading the proof on. This included using the slider (𝑛 = 9)
                                                                       or typing out their own examples (𝑛 = 3). P10 described wanting
                                                                       to both “try some things where it’s an edge case [and] something
                                                                       that’s an intuitive value” and then “check out...values that are less
Figure 6: Timeline of proof-reading behavior for each partic-          intuitive and see whether [the theorem still held].” This might
ipant during session. The y-axis indicates which proof step (1–8)      suggest that the slider afforded testing about theorem scope.
the participant is engaging with. Blue circles and orange squares         Participants (𝑛 = 5) also would toggle between in-scope and out-
denote reading in the abstract and concrete (instantiation) views,     of-scope examples on the example inputs slider while reading the
respectively. Purple diamonds mark dependency link clicks.             proof. For example, in Task 1 (the same as in Figure 2), P4 read the
ordering constraint was necessary and whether the argument held        first four steps of the proof on the value 𝑥 = −2 and then read the
for negative numbers. One participant (P14) did not use Gemini         last four steps of the proof on the value 𝑥 = 2. The theorem did not
at all and opted to only read the written proof. That participants     hold on both of these values; when asked about this behavior, P4
largely sought these same behaviors through the baseline (such as      said they focused on these two example values where the theorem
working out examples, examining proof structure) perhaps validates     did not hold because “the thinking or reasoning is upon me and I
the design of explorable theorems’ affordances.                        have to draw the dots between the steps of the proof and follow
    Figure 6 shows participants’ proof reading behaviors when using    along.”
explorable theorems. We discuss other kinds of reading behaviors.         Participants made use of the flexibility afforded by explorable
    Participants made thorough use of example analysis. With ex-       theorems. 10 participants read proof steps out-of-order at least
plorable theorems, participants selected 10.8 examples (𝑆𝐷 = 8.1),     once, as demonstrated by lines in Figure 6 going up and down. P3,
filtering for examples that were sustained selections over five sec-   for example, repeatedly cycled between steps 2 and 6 across the
onds. Of these, 5.6 (𝑆𝐷 = 3.6) were examples where the theorem         session, while P2’s trajectory spans 17 step visits with 8 switches
hypotheses were met, 3.8 (𝑆𝐷 = 5.1) were examples where the            between abstract and concrete modes and 2 backward jumps. Ten
hypotheses were not met, and 1.4 (𝑆𝐷 = 1.1) were participants’         participants used the dependency links at least once, indicating
own custom inputs. The utility of examples is articulated by P2:       that dependency navigation is perhaps correlated with non-linear
“this helps me understand the value [of variable x]...and I know       traversal of the proof structure. P5 articulated dependency links
what we’re trying to show.”                                            as “the ability to track the history and future references of a proof
                                                                       or immediate step.” Participants valued this ability: P9 noted they
                                                                                                                             Kambhamettu et al.


could “easily track how the proof got certain variables by clicking         Stay close to the source. With explorable theorems, many inter-
on the [dependency link],” and P10 appreciated seeing “how each          actions are grounded in the formal proof object. Worked example
part of the proof interacted with the rest of it”.                       values are extracted from the Lean proof state; dependency edges
   Seven participants alternated between reading the abstract proof      are recovered by diffing Lean proof states; the worked example
text and examining concrete instantiations within the same ses-          template mirrors the structure of the written step. This closeness
sion, as visible in the interleaving of blue and orange markers in       to the source matters because distance introduces error: whenever
Figure 6. P2 switched modes 8 times across 17 step visits, while P3      AI is used to create a model or establish links, there is opportunity
switched 6 times across 14 visits. This interleaving suggests partici-   for mistranslation. We reduced this distance through several de-
pants used the worked examples not as a separate reading pass but        sign decisions: prompting the agent to generate a Lean proof that
as an integrated strategy, reading a proof step, then checking its       structurally mirrors the prose and performing linking in small in-
concrete instantiation (or vice versa) before proceeding. P2 echoed      crements that leverage structural bridges put in place during gener-
this sentiment of an integrated strategy, stating “the text is showing   ation. Reasoning about correctness and computation was delegated
the meat of the proof and the boxes are showing how it works out         to the formal model wherever possible. We believe similar strate-
on an example...I’m doing two things in parallel.”                       gies, minimizing the role of AI inference and maximizing the role of
                                                                         the formal artifact, could reduce distance in other formally-backed
6   Discussion                                                           explanation systems, such as tools for understanding programs,
Results from our study show that explorable theorems improved            circuit diagrams, or biological pathways.
proof comprehension, drove participants to use and value every
interaction affordance, and surfaced exploratory behaviors that          6.1    Limitations
affirm our design choices.                                               Our pipeline has some technical limitations. First, because the Lean
                                                                         proof is AI-generated, it is not guaranteed to follow the original
6.0.1 Why did explorable theorems have an effect? What mecha-
                                                                         prose’s logical path; agents sometimes produce structurally dif-
nisms might explain the comprehension gains we observed? Several
                                                                         ferent arguments, or fail to complete the proof. Second, parts of
are plausible and likely act in concert. The novelty of the interface
                                                                         our pipeline rely on LLMs which introduce the possibility of subtle
may have increased engagement. The speed with which participants
                                                                         errors through mistranslations from Lean to natural language. How-
could set up and switch between examples reduced the friction of
                                                                         ever, as AI tools for formal proof generation improve, agents will
exploration. The concision of worked examples, showing only the
                                                                         become better at producing Lean proofs that structurally mirror
values relevant to each step, may have made the proof easier to
                                                                         their prose counterparts.
parse than a chatbot’s verbose explanations. And dependency links
                                                                            Our study also has limitations. We focused on relatively short
may have helped participants build a more accurate mental model
                                                                         proofs with undergraduate mathematics students; the benefits of
of proof structure. Participants’ very frequent use of examples and
                                                                         explorable theorems may differ for longer proofs, more advanced
strong ratings of their utility suggest that example-based explo-
                                                                         students, or experts encountering unfamiliar material. Additionally,
ration played a central role.
                                                                         while our evaluation measured comprehension through reconstruc-
   An interesting latent pattern emerges from Figure 6: participants
                                                                         tion tasks, written explanations, and subjective ratings, it does not
appear to fall into two broad modes of engagement. Some partici-
                                                                         capture longer-term outcomes such as retention, transfer to new
pants heavily sampled examples across the slider, while others made
                                                                         problems, or the ability to independently construct related proofs.
comparatively less use of examples but engaged more with depen-
dency links. This observation tentatively suggests that explorable
                                                                         6.2    Future work
theorems may support different reader strategies, example-driven
and structure-driven, rather than only accommodating one single          Future work could explore three main directions. First, systems
reading path, and that both strategies can support comprehension.        could combine explorable interfaces with conversational interac-
                                                                         tion. Rather than replacing the formal backing, chat would operate
6.0.2 A starter kit for formally-backed explanation interfaces. While    over it, allowing users to ask what breaks if a hypothesis is removed
we validate formally-backed explanation interfaces in the context        or how a proof changes under different instantiations. Second, the
of mathematical proofs, the approach may generalize. We reflect          approach could be extended to broader mathematical content to
on the design decisions that we believe drove the effect, and distill    understand how it holds up in messier, realistic settings. This in-
them into principles for others building similar systems.                cludes handling research-level theorems lacking complete Lean
   Offload incidental difficulty. One might ask whether interactivity    proofs, complex structures that do not map cleanly to natural lan-
removes the productive struggle necessary for durable learning [5].      guage, and non-numeric inputs like graphs. Finally, the principle
Proof comprehension involves two distinct kinds of difficulty: es-       of formally-backed explorability could extend beyond mathematics.
sential difficulty (understanding why a step follows or is necessary)    As formal verification tools are applied to end-user plans [27] and
and incidental difficulty (tracking variables, mentally substituting     complex reasoning [23], future systems might pair everyday arti-
values, recalling which step a symbol came from). We designed            facts, like a travel itinerary or a tax document, with a formalized
explorable theorems to offload incidental difficulty to the interface    Lean counterpart to make them fully explorable.
while preserving the essential difficulty. We believe this is why
participants felt less rushed without a reduction in mental demand.
Explorable Theorems


7     Conclusion                                                                             [19] Andrew Head, Amber Xie, and Marti A. Hearst. 2022. Math Augmentation: How
                                                                                                  Authors Enhance the Readability of Formulas using Novel Visual Design Practices.
We introduce a technique for formally-based explanation systems                                   In Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems.
and instantiate it as explorable theorems, a system which makes                                   https://doi.org/10.1145/3491102.3501932
                                                                                             [20] Ralf Herbrich, Tom Minka, and Thore Graepel. 2006. TrueSkill: A Bayesian Skill
mathematical proofs interactively explorable. By linking a natural-                               Rating System. In Advances in Neural Information Processing Systems, Vol. 19.
language proof to its formal Lean counterpart, our system leverages                          [21] Thomas Hubert, Roshan Mehta, Laurent Sartran, et al. 2025. Olympiad-level
underlying proof states to let readers inspect steps worked out on                                formal mathematical reasoning with reinforcement learning. Nature (2025).
                                                                                                  https://doi.org/10.1038/s41586-025-09833-y
concrete examples and trace logical dependencies. Results from                               [22] Albert Qiaochu Jiang, Sean Welleck, Jue Ping Zhou, Timothée Lacroix, Jiacheng
a lab study show that explorable theorems improved proof com-                                     Liu, Guillaume Lample, Samuel Lewis, Yuhuai Wu, Xiaokai Hou, Christian Hutter,
prehension and led participants to use and value its interaction                                  et al. 2023. Draft, Sketch, and Prove: Guiding Formal Theorem Provers with
                                                                                                  Informal Proofs. In International Conference on Learning Representations (ICLR).
affordances.                                                                                 [23] Dongwei Jiang, Marcio Fonseca, and Shay B Cohen. 2024. Leanreasoner: Boosting
                                                                                                  complex logical reasoning with lean. In Proceedings of the 2024 Conference of the
References                                                                                        North American Chapter of the Association for Computational Linguistics: Human
                                                                                                  Language Technologies (Volume 1: Long Papers). 7497–7510.
 [1] Lara Alcock, Mark Hodds, Somali Roy, and Matthew Inglis. 2015. Investigating            [24] Philip N Johnson-Laird. 2005. Mental models and thought. The Cambridge
     and improving undergraduate proof comprehension. Notices of the AMS 62, 7                    handbook of thinking and reasoning (2005), 185–208.
     (2015), 742–752.                                                                        [25] Hee-jeong Kim. 2020. Concreteness fading strategy: A promising and sustainable
 [2] Lara Alcock and Nicola Wilkinson. 2011. e-Proofs: Design of a resource to                    instructional model in mathematics classrooms. Sustainability 12, 6 (2020), 2211.
     support proof comprehension in mathematics. Educational Designer 1, 4 (2011),           [26] Zeger-jan Kock, Ulises Salinas-Hernández, and Birgit Pepin. 2025. Engineering
     1–20.                                                                                        students’ initial use schemes of ChatGPT as an instrument for learning. Digital
 [3] Paul Ayres. 2001. Systematic mathematical errors and cognitive load. Contempo-               Experiences in Mathematics Education 11, 1 (2025), 192–218.
     rary educational psychology 26, 2 (2001), 227–248.                                      [27] Christine P Lee, David Porfirio, Xinyu Jessica Wang, Kevin Chenkai Zhao, and
 [4] Zhangir Azerbayev, Bartosz Piotrowski, and Jeremy Avigad. 2022. ProofNet:                    Bilge Mutlu. 2025. Veriplan: Integrating formal verification and llms into end-
     A benchmark for autoformalizing and formally proving undergraduate-level                     user planning. In Proceedings of the 2025 CHI Conference on Human Factors in
     mathematics problems. In Second MATH-AI Workshop.                                            Computing Systems. 1–19.
 [5] Elizabeth L Bjork, Robert A Bjork, et al. 2011. Making things hard on yourself,         [28] Stanley Letovsky. 1987. Cognitive processes in program comprehension. Journal
     but in a good way: Creating desirable difficulties to enhance learning. Psychology           of Systems and software 7, 4 (1987), 325–339.
     and the real world: Essays illustrating fundamental contributions to society 2, 59-68   [29] Yong Li, Shoaib Kamil, Alec Jacobson, and Yotam Gingold. 2022. Hé: Docu-
     (2011), 56–64.                                                                               ment Processor for Executable Linear Algebra Papers. In SIGGRAPH Asia 2022
 [6] Ann Blandford, Dominic Furniss, and Stephann Makri. 2016. Qualitative HCI                    Conference Papers. https://doi.org/10.1145/3550469.3555395
     research: Going behind the scenes. Morgan & Claypool Publishers.                        [30] Raymond Lister, Elizabeth S Adams, Sue Fitzgerald, William Fone, John Hamer,
 [7] Neil Chulpongsatorn, Mille Skovhus Lunding, Nishan Soni, and Ryo Suzuki. 2023.               Morten Lindholm, Robert McCartney, Jan Erik Moström, Kate Sanders, Otto
     Augmented Math: Authoring AR-Based Explorable Explanations by Augmenting                     Seppälä, et al. 2004. A multi-national study of reading and tracing skills in novice
     Static Math Textbooks. In Proceedings of the 36th Annual ACM Symposium on                    programmers. Acm sigcse bulletin 36, 4 (2004), 119–150.
     User Interface Software and Technology (UIST ’23). ACM, 1–16.                           [31] Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu,
 [8] Will Crichton. 2021. A New Medium for Communicating Research on Program-                     Ran Wang, Yunzhou Xie, Junqiao Zhao, Qiufeng Wang, et al. 2026. Numina-Lean-
     ming Languages. In Proceedings of the 1st Workshop on Human Aspects of Types                 Agent: An Open and General Agentic Reasoning System for Formal Mathematics.
     and Reasoning Assistants.                                                                    arXiv preprint arXiv:2601.14027 (2026).
 [9] Ben Davies, Lara Alcock, and Ian Jones. 2020. Comparative judgement, proof              [32] Patrick Massot. 2024. Teaching mathematics using lean and controlled natural
     summaries and proof comprehension. Educational Studies in Mathematics 105, 2                 language. In 15th International Conference on Interactive Theorem Proving (ITP
     (2020), 181–197.                                                                             2024). Schloss Dagstuhl–Leibniz-Zentrum für Informatik, 27–1.
[10] Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob              [33] Juan Pablo Mejía-Ramos, Evan Fuller, Keith Weber, Kathryn Rhoads, and Aron
     von Raumer. 2015. The Lean Theorem Prover (System Description). In Proceedings               Samkoff. 2012. An assessment model for proof comprehension in undergraduate
     of the 25th International Conference on Automated Deduction (CADE-25) (Lecture               mathematics. Educational Studies in Mathematics 79, 1 (2012), 3–18.
     Notes in Computer Science, Vol. 9195). Springer, 378–388. https://doi.org/10.1007/      [34] Juan P. Mejía-Ramos, Erika Fuller, Keith Weber, Kari Rhoads, and Alexis Samkoff.
     978-3-319-21401-6_26                                                                         2012. An Assessment Model for Proof Comprehension in Undergraduate Mathe-
[11] Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob                   matics. Educational Studies in Mathematics 79, 1 (2012), 3–18. https://doi.org/
     von Raumer. 2015. The Lean theorem prover (system description). In International             10.1007/s10649-011-9349-7
     Conference on Automated Deduction (CADE). Springer, 378–388.                            [35] Hugo Mercier and Dan Sperber. 2011. Why do humans reason? Arguments for
[12] Anton N. Dragunov and Jonathan L. Herlocker. 2003. Designing Intelligent and                 an argumentative theory. Behavioral and brain sciences 34, 2 (2011), 57–74.
     Dynamic Interfaces for Communicating Mathematics. In Proceedings of the 8th             [36] Frédéric Tran Minh, Laure Gonnord, and Julien Narboux. 2025. Proof Assis-
     International Conference on Intelligent User Interfaces. 154–161. https://doi.org/           tants for Teaching: a Survey. In ThEdu@CADE. https://api.semanticscholar.org/
     10.1145/604045.604085                                                                        CorpusID:278422822
[13] Eddie M Gray and David O Tall. 1994. Duality, ambiguity, and flexibility: A             [37] Nagham M Mohammad, Matthew Demers, Erin McCubbin, Mitchell Jackson, and
     “proceptual” view of simple arithmetic. Journal for research in Mathematics                  Sara M Fulmer. 2025. How college students use ChatGPT. Pedagogical Research
     Education 25, 2 (1994), 116–140.                                                             10, 4 (2025), em0250.
[14] Ziwei Gu, Joyce Zhou, Ning-Er Lei, Jonathan K Kummerfeld, Mahmood Jasim,                [38] Robert C Moore. 1994. Making the transition to formal proof. Educational Studies
     Narges Mahyar, and Elena L Glassman. 2025. AbstractExplorer: Leveraging                      in Mathematics 27, 3 (1994), 249–266.
     Structure-Mapping Theory to Enhance Comparative Close Reading at Scale. In              [39] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 theorem prover and
     Proceedings of the 38th Annual ACM Symposium on User Interface Software and                  programming language. In Automated Deduction–CADE 28: 28th International
     Technology. 1–25.                                                                            Conference on Automated Deduction. Springer, 625–635.
[15] Aditya Gunturu, Yi Wen, Nandi Zhang, Jarin Thundathil, Rubaiat Habib Kazi,              [40] Chris Olah and Shan Carter. 2017. Research Debt. Distill (2017). https://doi.org/
     and Ryo Suzuki. 2024. Augmented Physics: Creating Interactive and Embedded                   10.23915/distill.00005
     Physics Simulations from Static Textbook Diagrams. In Proceedings of the 37th           [41] oOo0oOo. 2024. lean-lsp-mcp: Lean Theorem Prover MCP. https://github.com/
     Annual ACM Symposium on User Interface Software and Technology (UIST ’24).                   oOo0oOo/lean-lsp-mcp MCP server that allows agentic interaction with the
     ACM, 1–12.                                                                                   Lean theorem prover via the Language Server Protocol. GitHub repository..
[16] Guershon Harel and Larry Sowder. 2007. Toward comprehensive perspectives on             [42] Dale Parsons and Patricia Haden. 2006. Parson’s programming puzzles: a fun
     the learning and teaching of proof. Second handbook of research on mathematics               and effective learning tool for first programming courses. In Proceedings of the
     teaching and learning 2 (2007), 805–842.                                                     8th Australasian Conference on Computing Education-Volume 52. 157–163.
[17] John Harrison, Josef Urban, and Freek Wiedijk. 2014. History of interactive             [43] Birgit Pepin, Nils Buchholtz, and Ulises Salinas-Hernández. 2025. A scoping
     theorem proving. Computational Logic 9 (2014), 135–214.                                      survey of ChatGPT in mathematics education. Digital Experiences in Mathematics
[18] Sandra G Hart and Lowell E Staveland. 1988. Development of NASA-TLX (Task                    Education 11, 1 (2025), 9–41.
     Load Index): Results of empirical and theoretical research. In Advances in psy-         [44] Clément Pit-Claudel. 2020. Untangling mechanized proofs. In Proceedings of the
     chology. Vol. 52. Elsevier, 139–183.                                                         13th ACM SIGPLAN International Conference on Software Language Engineering.
                                                                                                                                                  Kambhamettu et al.


[45] Nicholas Rougeux and Oliver Byrne. 2018. Byrne’s Euclid: The First Six Books          A Appendix
     of the Elements of Euclid with Coloured Diagrams and Symbols. https://
     www.c82.net/euclid/ Online interactive reproduction.                                  A.1 Narrative Scenario
[46] Alan H Schoenfeld. 1988. When good teaching leads to bad results: The disasters
     of’well-taught’mathematics courses. Educational psychologist 23, 2 (1988), 145–       We demonstrate how the interaction patterns in explorable theo-
     166.                                                                                  rems can support productive inference over a longer period of use
[47] Annie Selden and John Selden. 2003. Validations of proofs considered as texts:
                                                                                           with an example of its usage in understanding a new proof. Ram is
     Can undergraduates tell whether an argument proves a theorem? Journal for
     Research in Mathematics Education 34, 1 (2003), 4–36.                                 a sophomore in a discrete mathematics class. He is trying to under-
[48] Derar Serhan and Natalie B. Welcome. 2024. Integrating ChatGPT in the Calculus        stand a theorem from the elementary number theory section that
     Classroom: Student Perceptions. International Journal of Technology in Education
     and Science (2024). https://api.semanticscholar.org/CorpusId:269835173
                                                                                           was introduced as an exercise in constructing direct proofs. Beyond
[49] Despina A Stylianou, Maria L Blanton, Eric J Knuth, and Despi Stylianou. 2009.        understanding this particular theorem, Ram wants to build intu-
     Teaching and learning proof across the grades. Routledge New York.                    ition for the overall proof structure so he can use it on an upcoming
[50] Despina A Stylianou, Maria L Blanton, and Ourania Rotou. 2015. Undergraduate
     students’ understanding of proof: Relationships between proof conceptions,            exam.
     beliefs, and classroom experiences with learning proof. International Journal of          Ram first reads the theorem statement:
     Research in Undergraduate Mathematics Education 1, 1 (2015), 91–134.
[51] Nicole Sultanum and Arjun Srinivasan. 2023. Datatales: Investigating the use of                  For all integers 𝑥 and odd integers 𝑛 > 1, if 𝑥 > 1,
     large language models for authoring data-driven articles. In 2023 IEEE Visualiza-                then 𝑥 𝑛 + 1 is not prime.
     tion and Visual Analytics (VIS). IEEE, 231–235.
[52] John Sweller. 1988. Cognitive load during problem solving: Effects on learning.           It is not immediately clear what this theorem is saying or why it
     Cognitive science 12, 2 (1988), 257–285.                                              should be true. Ram loads the theorem into the explorable theorems
[53] John Sweller, Paul Ayres, and Slava Kalyuga. 2011. Cognitive load theory. Springer    viewer to look into this.
     Science & Business Media.
[54] Jeffrey Tao, Litao Yan, Jessica Shi, Mia Ginsberg, and Andrew Head. 2025.
     FreeForm: Flexibly Augmenting Formulas with Synchronized Markup and Graph-
                                                                                               Seeing the boundaries of a theorem with the theorem input eval-
     ical Edits. In Proceedings of the 2025 CHI Conference on Human Factors in Com-        uator. Ram first uses the theorem input evaluator to see what the
     puting Systems. 1–12.                                                                 theorem actually says for a single concrete example. He sets 𝑥 = 2
[55] Oliver Tatton-Brown. 2019. Rigour and Intuition. Erkenntnis 86 (2019), 1757 –
     1781. https://api.semanticscholar.org/CorpusID:254465500                              and 𝑛 = 3, and the evaluator shows that the assumptions are satis-
[56] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui            fied. The tool displays the concrete computation directly beneath:
     Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican,          𝑥 𝑛 + 1 = 23 + 1 = 9, which is indeed not prime. Seeing a valid
     et al. 2023. Gemini: a family of highly capable multimodal models. arXiv preprint
     arXiv:2312.11805 (2023).                                                              example helps the theorem click, but Ram wonders why the strict
[57] The Lean Developers. 2024. Widgets: The user-widgets system. https://lean-            conditions, like 𝑛 > 1 and 𝑥 > 1, are necessary. He uses the evalu-
     lang.org/examples/1900-1-1-widgets/ Lean 4 Documentation.
[58] Bret Victor. 2011.       Explorable Explanations.       https://worrydream.com/
                                                                                           ator’s sliders to test these boundaries. Sliding down to 𝑥 = 1 and
     ExplorableExplanations/. Accessed 2026-03-01.                                         𝑛 = 1, the evaluator immediately flags that the assumptions are no
[59] Bret Victor. 2011. Kill Math. http://worrydream.com/KillMath/. Accessed:              longer met. The computation updates to show 11 + 1 = 2, which
     2024-05-24.
[60] Bret Victor. 2011. Tangle: a JavaScript Library for Reactive Documents. https://      is prime, breaking the theorem’s conclusion. Ram can now clearly
     worrydream.com/Tangle/. Accessed 2026-03-24.                                          see the theorem’s boundaries: the logic fails exactly when 𝑛 ≤ 1
[61] Yousef Wardat, Mohammad A. Tashtoush, Rommel Alali, and Adeeb M Jarrah.               or 𝑥 ≤ 1. He understands what the theorem claims and when it
     2023. ChatGPT: A revolutionary tool for teaching and learning mathematics.
     Eurasia Journal of Mathematics, Science and Technology Education (2023). https://     applies, but he still does not know why the valid cases always work.
     pdfs.semanticscholar.org/3174/39900cffedb7f18e623c1b0ab3fa8e54de21.pdf                He begins to read the proof.
[62] Keith Weber. 2008. How mathematicians determine if an argument is a valid
     proof. Journal for Research in Mathematics Education 39, 4 (2008), 431–459.              Seeing a worked example on each proof step. Ram really wants
[63] Keith Weber. 2015. Effective Proof Reading Strategies for Comprehending Math-
     ematical Proofs. International Journal of Research in Undergraduate Mathematics
                                                                                           to understand why the proof is true. The proof’s strategy is to
     Education 1, 3 (2015), 289–314. https://doi.org/10.1007/s40753-015-0011-0             show that 𝑁 = 𝑥 𝑛 + 1 is never prime by factoring it into two
[64] Keith Weber and Juan Pablo Mejia-Ramos. 2011. Why and how mathematicians              smaller integers, defined in the text as 𝑟 and 𝑠. To understand how
     read proofs: an exploratory study. Educational Studies in Mathematics 76, 3 (2011),
     329–344. https://doi.org/10.1007/s10649-010-9292-z                                    these factors are constructed, Ram clicks on their definitions. The
[65] Erik Weitnauer, David Landy, and Erin Ottmar. 2016. Graspable Math: Towards           proof step dependency inspector shows the definition of these terms:
     Dynamic Algebra Notations that Support Learners Better than Paper. In 2016            𝑟 = 𝑥 + 1 and 𝑠 is an alternating sum: 𝑠 = 𝑥 𝑛−1 − 𝑥 𝑛−2 + · · · − 𝑥 + 1.
     Future Technologies Conference. 406–414.
[66] Jelle Wemmenhove, Dick Arends, Thijs Beurskens, Maitreyee Bhaid, Sean Mc-             It is not immediately clear why multiplying these two specific
     Carren, Jan Moraal, Diego Rivera Garrido, David Tuin, Malcolm Vassallo, Pieter        expressions will always equal 𝑥 𝑛 +1. Looking at his running example
     Wils, et al. 2022. Waterproof: educational software for learning how to write
     mathematical proofs. arXiv preprint arXiv:2211.13513 (2022).
                                                                                           (𝑥 = 2, 𝑛 = 3), the worked example display beneath the step shows
[67] Carl E. Wieman, Wendy K. Adams, and Katherine K. Perkins. 2008. PhET:                 𝑟 = 2 + 1 = 3 and 𝑠 = 22 − 2 + 1 = 3. Since 3 × 3 = 9, the
     Simulations that enhance learning. Science 322, 5902 (2008), 682–683.                 factorization checks out for this specific case. But Ram wants to
[68] Michelle Wu, Aadil Gopal, and Andrew Head. 2023. FFL: A Language and Live
     Runtime for Styling and Labeling Typeset Math Formulas. In Proceedings of the         see the structural pattern. He slides the inputs to 𝑥 = 3, 𝑛 = 3 and
     36th Annual ACM Symposium on User Interface Software and Technology.                  sees 𝑁 = 28, with factors 𝑟 = 4 and 𝑠 = 7. The display shows
[69] Hyunkyoung Yoon, Jihye Hwang, Kyungwon Lee, Kyeong Hah Roh, and Oh Nam                the expanded form: 33 + 1 = (3 + 1)(32 − 3 + 1). He stares at this
     Kwon. 2024. Students’ use of generative artificial intelligence for proving mathe-
     matical statements. ZDM–Mathematics Education 56, 7 (2024), 1531–1551.                expansion. If he distributes the (3 + 1) across the (32 − 3 + 1), he gets
[70] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. 2022. MiniF2F: a cross-          33 −32 +3+32 −3+1. The −32 and +32 cancel. The +3 and −3 cancel.
     system benchmark for formal Olympiad-level mathematics. In International
     Conference on Learning Representations (ICLR).
                                                                                           All that is left is 33 +1. The concrete numbers make the abstract trick
                                                                                           obvious: the signs in 𝑠 alternate so that when multiplied by 𝑟 = 𝑥 +1,
                                                                                           every middle term cancels out. Ram keeps sliding the inputs and
                                                                                           watching the display update, and the cancellation pattern holds
                                                                                           every time.
Explorable Theorems


   Following a worked example to understand a key condition. Ram                Now, because 𝑥 > 2, we have 𝑟 = 𝑥 − 1 > 1. Moreover, we show
reaches the most complex step of the proof, which states that 𝑠 > 1:         that 𝑠 > 1 by the following reasoning: 𝑥 > 2, so 𝑥 + 1 > 3, so 𝑠 > 1.
since 𝑛 is odd, the alternating sum 𝑠 = 𝑥 𝑛−1 − 𝑥 𝑛−2 + · · · − 𝑥 + 1           Finally, multiply both sides of 𝑟 > 1 with 𝑠. We get 𝑟 · 𝑠 > 𝑠.
has an even number of powers of 𝑥 followed by a final +1, so the             However 𝑟 · 𝑠 = 𝑛. Therefore we have derived 𝑛 > 𝑠. Since 𝑛 has a
terms can be grouped as 𝑠 = (𝑥 𝑛−1 − 𝑥 𝑛−2 ) + · · · + (𝑥 2 − 𝑥) + 1. Each   factor 𝑠 such that 1 < 𝑠 < 𝑛, 𝑛 is composite.                      □
grouped pair satisfies 𝑥 𝑚 − 𝑥 𝑚−1 = 𝑥 𝑚−1 (𝑥 − 1) > 0 because 𝑥 > 1,
                                                                                Theorem B.2. For all integers 𝑥 and odd integers 𝑛 > 1, if 𝑥 > 1,
so 𝑠 is a sum of positive terms plus 1, giving 𝑠 > 1. This is far too
                                                                             then 𝑥 𝑛 + 1 is not prime.
dense for Ram to make sense of.
   Ram uses the worked example display to follow along the proof                 Proof. Let 𝑥 be an arbitrary integer and 𝑛 be an odd integer
step on a concrete example. For 𝑛 = 3, 𝑥 = 2, he sees 𝑠 = (22 −2)+1 =        with 𝑛 > 1. Assume that 𝑥 > 1. Let us denote 𝑥 𝑛 + 1 by 𝑁 . We wish
2 + 1 = 3 > 1. He slides to 𝑛 = 5 and watches the display show four          to show that 𝑁 is not prime. We will do that by showing that 𝑁
powers of 𝑥 followed by +1: exactly the even number of powers                has a factor that is neither 1 nor equal to 𝑁 .
the step describes. He slides through 𝑛 = 5, 7, 9 and sees the same              First observe that for odd 𝑛 > 1, 𝑥 𝑛 + 1 = (𝑥 + 1)(𝑥 𝑛−1 − 𝑥 𝑛−2 +
pattern hold each time. The reason 𝑛 must be odd becomes clear:              𝑥 𝑛−3  − · · · + 1). Let us also denote 𝑥 + 1 by 𝑟 and the alternating
an odd 𝑛 guarantees an even number of powers of 𝑥, which is what             sum 𝑥 𝑛−1 − 𝑥 𝑛−2 + · · · + 1 by 𝑠. Note that both 𝑟 and 𝑠 are factors
makes the pairing argument work. If 𝑛 were even, the grouping                of 𝑁 , since 𝑁 = 𝑟 · 𝑠 = 𝑠 · 𝑟 .
would fail.                                                                      Now, because 𝑥 > 1, we have 𝑟 = 𝑥 + 1 > 2. Moreover, we show
   Ram then toggles to 𝑛 = 1 using the theorem input evaluator               that 𝑠 > 1 by the following reasoning: 𝑠 has 𝑛 terms alternating in
and sees the proof break at this step: with 𝑛 = 1, 𝑠 = 1, and the            sign, and since 𝑛 is odd, the last term is +1, and each positive term
condition 𝑠 > 1 no longer holds. The system flags that the proof             𝑥 𝑘 ≥ 1 for 𝑥 > 1, so 𝑠 ≥ 1, and since 𝑥 > 1 we get 𝑠 > 1.
breaks on this step. This makes clear why 𝑛 must be both odd and                 Finally, multiply both sides of 𝑟 > 1 with 𝑠. We get 𝑟 · 𝑠 > 𝑠.
greater than 1.                                                              However 𝑟 · 𝑠 = 𝑁 . Therefore we have derived 𝑁 > 𝑠. Since 𝑁 has
   Seeing the proof through to the end. The remaining steps show             a factor 𝑠 such that 1 < 𝑠 < 𝑁 , 𝑁 is composite.                      □
that 𝑁 > 𝑠 (since 𝑁 = 𝑟 · 𝑠 and 𝑟 > 1) and that 𝑠 > 1, together              B.1.2   Task 2: Arithmetic Progression Squares.
establishing that 𝑠 is a proper factor of 𝑁 , so 𝑁 is not prime. With
the worked example displayed right below each step of the proof                 Theorem B.3. For all integers 𝑛, 𝑛(𝑛 + 1)(𝑛 + 2)(𝑛 + 3) + 1 is a
(𝑁 = 9, 𝑟 = 3, 𝑠 = 3), Ram finds these steps straightforward.                perfect square.
   After his read of the proof, Ram understands not just the high-              Proof. Let 𝑛 be an arbitrary integer. Pair the outer terms: let
level proof strategy, find a proper factor to show 𝑁 is not prime,           𝑝 = 𝑛 · (𝑛 + 3). Expanding, 𝑝 = 𝑛 2 + 3𝑛. Pair the inner terms: let
but also the reasons each condition is required: 𝑥 > 1 ensures the           𝑞 = (𝑛 + 1) · (𝑛 + 2). Expanding, 𝑞 = 𝑛 2 + 3𝑛 + 2 = 𝑝 + 2.
grouped pairs are positive, 𝑛 must be odd to make the even-pairing              Rewrite the product: 𝑛(𝑛 + 1)(𝑛 + 2)(𝑛 + 3) = 𝑝 · 𝑞 = 𝑝 (𝑝 + 2).
argument work, and 𝑛 > 1 ensures 𝑠 > 1. He arrived at these                  Expand 𝑝 (𝑝 +2) = 𝑝 2 +2𝑝. Add 1 to both sides: 𝑝 2 +2𝑝 +1. Recognize
insights not by being told them, but by tinkering with the inputs            the perfect square: 𝑝 2 + 2𝑝 + 1 = (𝑝 + 1) 2 .
and inspecting the proof’s logic. Because explorable theorems is                Substitute back 𝑝 = 𝑛 2 + 3𝑛 to get 𝑝 + 1 = 𝑛 2 + 3𝑛 + 1. Therefore
backed by executable Lean code, Ram is seeing machine-checked                𝑛(𝑛 + 1)(𝑛 + 2)(𝑛 + 3) + 1 = (𝑛 2 + 3𝑛 + 1) 2 . Since 𝑛 2 + 3𝑛 + 1 is an
proof states that tell him how the math actually works out.                  integer, 𝑛(𝑛 + 1)(𝑛 + 2)(𝑛 + 3) + 1 is a perfect square.               □
   One might ask whether making the mathematics this interactive
removes the productive struggle necessary for durable learning [5].             Theorem B.4. For all integers 𝑛, 𝑛(𝑛 + 4)(𝑛 + 8)(𝑛 + 12) + 256 is
We argue that explorable theorems does not remove the difficulty             a perfect square.
of understanding the math; rather, it reduces unnecessary cogni-                 Proof. Let 𝑛 be an arbitrary integer. Pair the outer terms: let
tive load. Mentally tracking variable substitutions and expanding            𝑝 = 𝑛 · (𝑛 + 12). Expanding, 𝑝 = 𝑛 2 + 12𝑛. Pair the inner terms: let
algebraic terms requires significant working memory [3, 52, 53]. By          𝑞 = (𝑛 + 4) · (𝑛 + 8). Expanding, 𝑞 = 𝑛 2 + 12𝑛 + 32 = 𝑝 + 32.
offloading this computation to the interface, the system frees the               Rewrite the product: 𝑛(𝑛 + 4)(𝑛 + 8)(𝑛 + 12) = 𝑝 · 𝑞 = 𝑝 (𝑝 + 32).
reader to focus their efforts on the proof’s actual structure.               Expand 𝑝 (𝑝 + 32) = 𝑝 2 + 32𝑝. Add 256 to both sides: 𝑝 2 + 32𝑝 + 256.
                                                                             Recognize the perfect square: 𝑝 2 + 32𝑝 + 256 = (𝑝 + 16) 2 .
B Study Materials                                                                Substitute back 𝑝 = 𝑛 2 + 12𝑛 to get 𝑝 + 16 = 𝑛 2 + 12𝑛 + 16.
B.1 Theorems and Proofs                                                      Therefore 𝑛(𝑛 + 4)(𝑛 + 8)(𝑛 + 12) + 256 = (𝑛 2 + 12𝑛 + 16) 2 . Since
B.1.1   Task 1: Composite Numbers.                                           𝑛 2 + 12𝑛 + 16 is an integer, 𝑛(𝑛 + 4)(𝑛 + 8)(𝑛 + 12) + 256 is a perfect
                                                                             square.                                                               □
   Theorem B.1. For all integers 𝑥, if 𝑥 > 2, then 𝑥 2 − 1 is not prime.
   Proof. Let 𝑥 be an arbitrary integer. Assume that 𝑥 > 2. Let us           B.2     Study Questions
denote 𝑥 2 − 1 by 𝑛. We wish to show that 𝑛 is not prime. We will do         B.2.1 Task 1 Questions (Composite Numbers).
that by showing that 𝑛 has a factor that is neither 1 nor equal to 𝑛.            (1) Describe the proof of Theorem 1 in your own words.
   First observe that 𝑥 2 − 1 = (𝑥 − 1)(𝑥 + 1). Let us also denote 𝑥 − 1         (2) Why does the proof of Theorem 1 show 𝑥 − 1 > 1?
by 𝑟 and 𝑥 + 1 by 𝑠. Note that both 𝑟 and 𝑠 are factors of 𝑛, since              (3) Why does the theorem not hold for 𝑥 = 2?
𝑛 = 𝑟 · 𝑠 = 𝑠 · 𝑟.
                                                                                                                    Kambhamettu et al.


   (4) Can the assumption in Theorem 1 (𝑥 > 2) be weakened             (3) Why does this theorem hold for all integers?
       while keeping the conclusion true?                              (4) Can Theorem 1 be generalized by modifying the expres-
   (5) What are the similarities and differences between Theorem           sion?
       1 and 4 in their proofs?                                        (5) What are the similarities and differences between Theorem
                                                                           1 and 4 in their proofs?
B.2.2 Task 2 Questions (Arithmetic Progression Squares).
    (1) Describe the proof of Theorem 1 in your own words.          Revised 31 March 2026
    (2) Why does the proof pair outer terms and inner terms sepa-
        rately?
