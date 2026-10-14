                                               Evaluating Research-Level Math Proofs via Strict Step-Level Verification
                                                                                                     Yifeng Sun
                                                                                               Independent Researcher
                                        Abstract                                                            tion systems operate on a paradigm of ultimate accountability,
                                                                                                            where the underlying infrastructure (e.g., Lean) or a human
                                        Large Language Models (LLMs) struggle to rigorously ver-            expert bears the responsibility of providing an absolute guar-
                                        ify complex mathematical proofs. Standard global evaluation         antee of correctness. In contrast, our objective is to equip the
                                        approaches suffer from “context poisoning,” in which superfi-       agent with an intrinsic capacity to distinguish sound reason-
                                        cially plausible statements mask subtle logical flaws, leading      ing from flawed logic during its exploratory and generative
                                        to hallucination or over-skepticism. To address this, we shift      phases. After all, agents will inevitably encounter scenarios
                                        from global evaluation to strict step-level verification: our       where they must rely entirely on pure natural language rea-
                                        framework maintains detailed context for each deduction step        soning to conceptualize and discover solutions. In the highly
                                        and strictly constrains the sources of applied theorems. We         unconstrained search space of mathematical discovery, en-
                                        evaluate on a carefully curated adversarial diagnostic suite of     abling an agent to recognize its own missteps is critical for
                                        research-level proofs drawn from the FirstProof challenge. A        pruning dead ends and drastically reducing the generation of
                                        systematic ablation study demonstrates that these deductive
arXiv:2606.10799v1 [cs.AI] 9 Jun 2026




                                                                                                            hallucinatory or structurally flawed proofs. Ultimately, we
                                        constraints are indispensable, as unconstrained global prompt-      aim to demonstrate a core principle of agentic reasoning: by
                                        ing consistently fails to localize subtle logical errors. Beyond    forcing a model to explicitly and exhaustively write out
                                        outperforming global evaluation, our approach fundamentally         the underlying details of an informal proof, we inherently
                                        alters the failure taxonomy. Error analysis reveals that, rather    amplify its ability to discover subtle logical errors that its
                                        than exhibiting severe logical hallucinations, remaining rejec-     standard reasoning would otherwise gloss over. It is impor-
                                        tions are primarily instances of “pedantic hyper-rigor” stem-       tant to emphasize that, to validate our approach, we merely
                                        ming from unstated domain conventions, effectively exposing         task the agent with the process of elaboration rather than de-
                                        implicit ambiguities within the expert benchmark itself. Our        manding a flawlessly exhaustive natural language proof as the
                                        findings suggest that prompting agents to organize their verifi-    final output. Consequently, our objective is not to reinvent de
                                        cation notes in a cautious, human-mathematician-like manner         Bruijn’s Mathematical Vernacular (MV). Rather, we aim to
                                        can substantially improve their ability to distinguish rigorous     demonstrate that agents—much like human mathematicians—
                                        proofs from flawed ones, with the potential to strengthen agen-     leverage the very act of detailed writing to ascertain which
                                        tic reasoning on frontier mathematical concepts that the base       conclusions are genuinely correct and rigorously proven.
                                        model does not already know well, and to lay a theoretical
                                        foundation for future automated proof-review systems. Code          To achieve this, we aim to design an agent framework that
                                        and prompts are available at GitHub.                                evaluates proofs with the strictness of a human mathematician
                                                                                                            reviewing a manuscript. Such a system must prioritize sound-
                                        1 Introduction                                                      ness (eliminating false acceptances of flawed proofs) over
                                                                                                            mere completeness, and effectively leverage inference-time
                                        The self-correction and reasoning capabilities of Large Lan-        compute to achieve greater clarity the longer it reasons. We in-
                                        guage Models (LLMs) and AI agents have improved signif-             troduce a crucial methodological shift: reframing verification
                                        icantly with scaling and reinforcement learning [1]. In the         from direct anomaly detection to constructive elaboration
                                        mathematical domain, agent frameworks have demonstrated             via strict step-level verification. Rather than directly query-
                                        impressive problem-solving results [2, 3]. However, when            ing an LLM to spot flaws within a global context—a task
                                        verifying research-level mathematical proofs, current models        highly susceptible to context poisoning and hallucination—
                                        frequently falter. Standard global evaluation approaches often      we test whether the proof can be rigorously and explicitly
                                        suffer from “context poisoning,” where superficially plausible      expanded. For a mathematical text S treated as a string, we de-
                                        statements mask subtle spurious justifications, leading agents      compose it into an ordered sequence of steps (s1 , s2 , . . . , sn ),
                                        to either hallucinate validity or exhibit over-skepticism.          isolating deduction steps that contain logical assertions. By
                                        While formal verification systems such as Lean [4] offer ab-        “elaborating a step,” we mean expanding a deduction step si
                                        solute guarantees, their application is bottlenecked by human-      into a finer-grained derivation string s′i in natural language
                                        built infrastructures and a heavy reliance on manually main-        that strictly preserves the original reasoning trajectory but ex-
                                        tained libraries (e.g., Mathlib [5]). This naturally constrains     plicitly unpacks the underlying logic. Consequently, anomaly
                                        the ability of current automated agents to formally verify ad-      detection emerges naturally from the generative process: if
                                        vanced mathematical concepts. Therefore, verifying proofs           an agent fails to construct a valid s′i , we suspect si harbors a
                                        in natural language remains an essential frontier. Generating       logical gap or unsound justification. By forcing the agent to
                                        fine-grained elaborations of informal proofs serves as a crucial    elaborate, we replace the LLM’s opaque internal judgments
                                        bridge: it not only aids human mathematicians in peer re-           with strict generation constraints [11, 12]. Every elaborated
                                        view but also assists agentic systems in eventually translating     step is required to explicitly ground its applied theorems and
                                        informal math into rigorous formal code [6–10].                     logical derivations, reducing superficial plausibility.
                                        Crucially, this focus on AI self-correction serves a fundamen-         To systematically enforce these constraints and ensure the
                                        tally different role than formalization itself. Formal verifica-       elaboration does not introduce hallucinations of its own, we


                                                                                                           1
ground our process in a formal descriptive framework. Specif-            specific vulnerability. In these specific cases, the flawed proofs
ically, we model the logical dependencies of any deduction               package incorrect mathematical knowledge—which the LLM
step using a rigorous tripartite architecture: internal context          is unfamiliar with—into structurally rigorous and plausible
(Γi , encompassing theorems, definitions, and hypotheses di-             formats. This empirical result highlights that proof verification
rectly originating from the proof text S), external knowledge            remains a highly challenging task, particularly for novel or
(Σi , comprising non-trivial statements drawn from outside               frontier mathematics where LLMs lack prior familiarity with
literature or established domain consensus), and background              the specific domain knowledge and can be easily deceived by
theory (Ti , representing trivial statements or rewrite rules            formal-sounding pseudoproofs.
necessary to syntactically derive the assertion).                        To address this limitation, we evaluated our step-level verifi-
Operationally, we implement this step-level verification as an           cation agent under a strict avg@3 setting, supplemented by
autonomous, state-driven agentic workflow guided by fixed                multi-pass experiments on these specific adversarial exam-
prompt files. By default, every deduction step si is initialized         ples. By explicitly grounding the reasoning process within
with a conservative local status. During each iteration, the             the (Γi , Σi , Ti ) constraints to trace external knowledge, our
agent attempts to elaborate the remaining open steps. Based              framework successfully isolated these camouflaged errors, suc-
on the strict (Γi , Σi , Ti ) constraints, the agent executes spe-       cessfully rejecting all invalid proofs. Furthermore, out of the
cific state transition actions: if an elaboration is successfully        valid proofs, our agent failed to verify only 3 cases. Para-
derived, the step transitions to verified; conversely, if the            doxically, these failures highlight the meticulousness of our
agent identifies a distinct logical error, it flags the step as          framework. The agent did not fail due to logical reasoning
flawed. To rigorously guard against false positives (i.e.,               deficits, but because the underlying base model lacked famil-
pedantic over-rejection), any flawed step triggers a fixed               iarity with highly specific domain conventions, where certain
confirmation phase: the agent attempts to confirm the error,             mathematical objects inherently possess implicit properties
potentially reverting the state back to open if the perceived            by default. Consequently, it failed to establish the necessary
flaw is resolved upon re-evaluation. This iterative process is           prerequisite statements for the local context.
governed by strict halting criteria: (1) Acceptance: the proof           For example, in Question 7 of the FirstProof dataset, a human
is deemed valid if and only if all steps reach the verified              expert naturally assumes that the subgroup Γ is explicitly linear
state; (2) Rejection: the process terminates immediately and             (since it is a subgroup of a real semi-simple Lie group, and by
rejects the proof if a flawed state is definitively confirmed            convention within this specific research domain, such groups
upon reflection; and (3) Exhaustion: to prevent infinite loops           are treated as linear) [15, 16]. While the standard baseline
on intractable gaps, the system globally halts and rejects the           simply ignored this subtle leap and glossed over the text, our
proof after five consecutive reasoning resumptions without an            agent rigorously noted that under the general definition, a
observed progress signal.                                                subgroup of a real semi-simple Lie group is not necessarily
To empirically validate our proof of concept and demonstrate             linear by default [17]. Because the base model was unfamiliar
its potential reward, we construct a highly curated diagnos-             with this established domain convention, it conservatively
tic suite of challenging mathematical proofs. We focus on a              refused to arbitrarily add the linearity assumption into the local
small-scale sample to ensure absolute clarity in our evaluation:         context, ultimately losing a fundamental condition required
every proof has been meticulously verified by human experts              to verify the proof. This contrast perfectly demonstrates that
to establish an unambiguous ground truth, classifying them               our framework enforces genuine deductive verification over
as either strictly valid or explicitly invalid. Specifically, our        superficial pattern matching, even if it halts when confronted
diagnostic suite is heavily anchored in the FirstProof chal-             with domain-specific conventions it has not yet mastered.
lenge [13–15]. To establish an unambiguous ground truth, we              In summary, our main contributions are threefold:
collected proofs that have undergone rigorous expert evalua-              • Methodological Paradigm Shift: We reframe natural lan-
tion, securing a highly curated collection of 21 research-grade             guage proof verification from direct, black-box anomaly
proofs definitively classified as either strictly valid or explic-          detection to constructive elaboration. By modeling the
itly invalid. These 21 samples are strategically drawn from                 logical dependencies of deduction steps through a novel
three authoritative sources: (1) official FirstProof releases, (2)          (Γi , Σi , Ti ) tripartite architecture, we force the model to
correct proofs generated by the Aletheia, and (3) generations               explicitly trace internal contexts, external knowledge, and
from OpenAI’s solutions. By anchoring our evaluation on this                background theories, thereby mitigating superficial pattern
precise, expert-verified suite, we can investigate how our step-            matching.
level verification effectively isolates subtle reasoning errors           • Autonomous Verification Workflow: We propose a state-
that standard global evaluators consistently miss.                          driven agentic framework governed by strict step-level con-
In our evaluation on the curated 21-proof suite, we observe                 straints. Equipped with a fixed confirmation phase and
that current large language models demonstrate strong ca-                   robust halting criteria, our system prioritizes logical sound-
pabilities in standard contexts: the standard global baseline               ness and effectively leverages inference-time compute to
successfully identified the logical errors in 8 out of the 10               prevent the “context poisoning” that plagues global evalua-
explicitly invalid proofs. However, a detailed analysis of the              tors.
remaining 2 cases where the global pipeline failed reveals a              • Empirical Insights via Micro-benchmarking: Our evalu-


                                                                     2
    ation demonstrates that while even highly capable standard             and elevate the agent’s evaluative accuracy.
    baselines can still be deceived by structurally rigorous pseu-
    doproofs, our framework achieves zero false acceptances                3     Methodology
    on the problem set. Furthermore, our qualitative analysis
                                                                           For a mathematical text S treated as a string, it can nat-
    reveals a critical bottleneck in current verification tasks: the
                                                                           urally be decomposed into an ordered sequence of steps
    vulnerability of base models to unstated, domain-specific
                                                                           (s1 , s2 , . . . , sn ). Unlike fully formalized proofs in systems
    hidden conventions.
                                                                           like Lean or Rocq [4, 5], natural language mathematical proofs
                                                                           inherently omit trivial algebraic manipulations and elementary
2    Related Work                                                          logical deductions to maintain readability. Because of these
Math Agents Agentic frameworks for mathematics have                        inherent omissions, evaluating a proof as a monolithic global
advanced rapidly and are producing more and more significant               text often obscures subtle flaws and logical gaps.
results in research-level mathematics. These agents may or                 To address this, we reframe verification from direct anomaly
may not utilize proof assistants and formal languages. Recent              detection to constructive elaboration. By “elaborating a
frontier breakthroughs have heavily favored second paradigm:               step”, we mean that for a given deduction step si with an
agents conduct exploration, reasoning, and proof construction              assertion (derived conclusion statement) ai , we provide an
entirely in pure natural language. For instance, R ETHLAS [3]              expanded derivation s′i that concludes with the identical as-
can operate as an informal reasoning agent that mimics human               sertion as si . Crucially, s′i must strictly preserve the original
mathematical workflows—exploring literature and proposing                  reasoning trajectory of si , but unpack the logic at a finer gran-
candidate natural-language proofs for advanced open prob-                  ularity. If we fail to come up with a valid expanded derivation,
lems. Similarly, A LETHEIA [2] functions as an end-to-end                  we suspect si to contain a logical gap or flaw.
natural language research agent capable of iteratively gener-
ating, verifying, and revising solutions from PhD-level exer-              3.1   The Tripartite Explanation Framework
cises to autonomous research papers. Most recently, O PE -                 To systematically investigate whether an elaboration s′i suc-
NAI’ S MODEL [18] achieved a historic milestone by disprov-                cessfully bridges a gap without demanding explicit syntactic
ing Erdős’s 80-year-old planar unit distance conjecture using             completeness (which misaligns with human communication),
highly complex, purely informal reasoning. However, despite                we introduce the formal concept of an explanation.
their immense generative power, a critical vulnerability of
                                                                           It is crucial to clarify that this theoretical framework is not
these pure natural language agents is their susceptibility to
                                                                           artificially engineered solely for AI agents; rather, it stems
hallucinations and subtle logical gaps, particularly when self-
                                                                           directly from a refinement of the routine cognitive actions hu-
evaluating long-horizon mathematical proofs. [19–21] Our
                                                                           man mathematicians employ when explaining and validating
work directly addresses this vulnerability. We demonstrate
                                                                           a proof. By adopting this stance, the framework is sufficiently
a structured pathway for pure natural language agents to in-
                                                                           descriptive to ensure universal applicability to human mathe-
dependently overcome these blind spots: by enforcing strict,
                                                                           matical discourse, while simultaneously providing a rigorous,
step-level detailed elaboration, agents can systematically un-
                                                                           prescriptive structure that conveniently facilitates systematical
pack their reasoning, rigorously detect anomalies, and elim-
                                                                           analysis and guides agentic workflows. [23] In our implemen-
inate hallucinations without needing to fall back on external
                                                                           tation, we explicitly prompt the agent to output its elaborations
formalization infrastructures.
                                                                           according to the (Γi , Σi , Ti ) tripartite structure. However, it
                                                                           is worth noting that we do not claim this explicit formatting
Mathematical Vernacular The conceptual ambition of                         is necessarily the optimal approach, given the additional gen-
bridging informal human mathematical discourse and strict                  eration overhead it imposes on the agent. Alternative imple-
mechanical logic dates back to de Bruijn’s Mathematical Ver-               mentations may achieve similar rigor by simply requiring the
nacular (MV) [22]. MV was proposed as an intermediate                      agent to maintain a detailed, distinct record of internal con-
representational language that obeys formal grammatical rules              texts versus external knowledge, without strictly enforcing the
while preserving the natural “resting points” (steps) of math-             tripartite syntax.
ematical reasoning, thus serving as a stepping stone toward                We model the logical dependencies of any deduction step (or
fully coded formal systems (e.g., Automath). Importantly,                  its elaboration) using this framework. We define an explana-
we do not intend to replicate MV or construct a rigid natural-             tion of the step si as a triple of sets (Γi , Σi , Ti ). A step si is
language proof assistant. Rather, we adopt its underlying                  considered valid if there exists an explanation such that:
philosophy to help autonomous agents systematically reduce
logical hallucinations. By structuring natural language proofs                                      Γi ∪ Σi ⊢Ti ai                          (1)
around the (Γi , Σi , Ti ) tuple extraction, our framework com-
putationally isolates these resting points, bringing rigor to              where ⊢ denotes rigorous informal entailment. The compo-
informal mathematical text. Crucially, in practice, we do not              nents reflect how mathematical justifications are sourced:
algorithmically verify whether the agent flawlessly executes                • Local Context (Γi ): This contains finitely many statements
this extraction; the mere attempt to engage in this highly struc-             (theorems, definitions, and hypotheses) directly originating
tured elaboration is sufficient to expose hidden logical flaws                from S. These statements may be explicit or implicit, but


                                                                       3
   they must be effective within the current scope (e.g., local           3. Flaw Confirmation (FLAWED → OPEN): To rigorously
   assumptions within a case analysis block expire once the                  guard against pedantic false positives, any preliminary
   block concludes).                                                         transition to FLAWED triggers an adversarial investigation.
 • Global Knowledge (Σi ): This comprises non-trivial state-                 The agent evaluates whether the proposed flaw witness rep-
   ments drawn from external literature or established domain                resents a genuine structural mathematical error or merely
   consensus (i.e., outside of S). To prevent the hallucination              a superficial textual nitpick (e.g., relying on an unstated
   of non-existent theorems, any statement invoked from Σi                   standard domain convention or a terminology-dependent
   must be critically examined.                                              edge case). If the perceived flaw is determined to be an
 • Background Theory (Ti ): This comprises trivial state-                    epistemic ambiguity rather than a logical breakdown, the
   ments, fundamental logical axioms (e.g., Modus Ponens),                   step is conservatively reverted to OPEN.
   and rewrite rules. By isolating Ti , we bypass the need for            4. Dynamic Decomposition (OPEN → {OPENa , OPENb }):
   rigid algebraic hierarchies (like those in Mathlib), allowing             If a deduction step si is deemed too coarse or encompasses
   the direct manipulation of sound statements over concrete                 multiple non-trivial logical leaps, the agent is permitted
   objects while safely decoupling structural type constraints               to dynamically decompose it into finer-grained sub-steps.
   from the core deductive logic.                                            The original si is replaced in the global sequence by these
                                                                             new sub-steps, which are individually initialized as OPEN
Crucially, an explanation (Γi , Σi , Ti ) should not be viewed as
                                                                             and evaluated independently.
the complete set of all contextually valid truths, but exclusively
as the minimal required set of statements necessary to validate          We emphasize a critical design choice: failure to close a diffi-
the natural language proof step rigorously. A comprehensive              cult theorem does not by itself count as a flaw. If an external
discussion of this framework and what constitutes a valid                burden remains unsupported, the step conservatively remains
explanation is provided in Appendix B.                                   OPEN.

3.2   State-Driven Verification Agent
                                                                         Global Halting Criteria The autonomous verification loop
While the tripartite framework intrinsically describes human             progressively updates the step states and their dependencies.
mathematical validation, it also serves as an ideal analytical           The process iterates until one of the following strict halting
scaffolding for AI systems. To explore the feasibility of highly         criteria is triggered, determining the final validity of the global
efficient natural language proof verification, we implement a            proof S:
lightweight, state-driven agent. The agent utilizes this frame-
work because it conveniently enforces traceable reasoning and             • Acceptance (Soundness): The global proof is deemed
provides a systematic taxonomy for isolating failure modes.                 valid and accepted if and only if the entire sequence suc-
The agent operates without relying on a formal proof assistant              cessfully reaches the terminal verified state: ∀i, ci =
or domain-specific theorem whitelists. Instead, it maintains a              VERIFIED. If the text contains several proofs, it is consid-
discrete cognitive state ci ∈ {OPEN, VERIFIED, FLAWED}                      ered valid if entire sequence of one of the proofs is valid.
for each step si .                                                        • Rejection via Flaw Confirmation: If any step enters the
                                                                            FLAWED state, it must undergo the aforementioned Flaw
                                                                            Confirmation investigation. If a flaw is explicitly confirmed
Initialization and Iteration Upon initialization, the agent                 (i.e., it is verified as a genuine structural error and not
assigns an OPEN status to all deduction steps. During each                  reverted to OPEN), the system halts and the global proof is
iteration, the agent selects the most critical OPEN step and                immediately rejected.
attempts to write a thick elaboration s′i , explicitly extracting         • Rejection via Exhaustion: The agent may fail to give a
the corresponding (Γi , Σi , Ti ).                                          disproof of a flawed step. Thus to prevent looping on in-
                                                                            tractable gaps or missing foundational knowledge, the run-
State Transition Rules The agent’s transitions are governed                 ner monitors observed progress signals. If five consecutive
by strict auditing mechanisms to prevent both pedantic false                resume iterations produce neither an OPEN→VERIFIED
positives and dangerous false negatives:                                    transition nor an OPEN-step split, the system terminates the
                                                                            loop and conservatively rejects the proof.
 1. OPEN → VERIFIED: A step transitions to VERIFIED
    if and only if its written elaboration is logically closed
    and every external item used in Σi is explicitly supported           External Knowledge Retrieval In our pipeline, the external
    (either by a direct sub-proof generated within the step file         knowledge set Σi is primarily sourced through active internet
    or by a precise literature citation).                                retrieval. To ensure the reliability of this external knowledge,
 2. OPEN → FLAWED: A step is marked FLAWED only when                     our prompt files explicitly direct the agent to prioritize estab-
    the agent can exhibit an explicit flaw witness. This in-             lished mathematical textbooks and directly relevant research
    cludes an exact false statement, an invalid inference from           literature. While these instructions guide the agent’s search
    written premises, an explicit contradiction with the already         behavior, we do not computationally enforce strict constraints
    verified local context Γi , or a demonstrably misapplied             on the exact provenance or syntactic precision of the cited
    external theorem in Σi .                                             theorems. However, general open-ended retrieval introduces


                                                                     4
a broader theoretical challenge: unconstrained agents often              the diagnostic suite into two distinct subsets based on their
overlook the strict technical constraints or local assumptions           ground-truth validity:
required by retrieved theorems. This risks creating a “con-              Valid Proofs (11 cases) This subset consists of 9 proofs gener-
textual misapplication,” where a globally valid theorem is               ated by the Aletheia framework [2] and 2 proofs from OpenAI.
incorrectly applied to a local context (Γi ) because its under-          The Aletheia subset (comprising variants 2A, 2B, 5A, 7B,
lying prerequisites are not fully met. Specifically, without             8B, 9A, 9B, 10A, and 10B, where the suffixes denote outputs
the strict faithfulness constraints enforced by our framework,           from two distinct agent architectures) was rigorously vetted
an agent might invoke unmentioned external knowledge to                  and certified as mathematically sound by human domain ex-
artificially justify flawed steps during extended multi-turn exe-        perts in the original Aletheia study. The remaining two valid
cutions. Successfully navigating this latent risk underscores            cases are OpenAI’s proofs for problems 4 and 6, which have
the critical necessity of our framework’s strict adherence to the        reached a definitive consensus of correctness within the formal
original text. Consequently, a crucial direction for future math-        mathematics community (e.g., Zulip expert discussions).
ematical agents is the development of rigorous controls over
external knowledge integration. Future systems must move                 Invalid Proofs (10 cases) To systematically source authentic,
beyond basic search by explicitly verifying the authoritative            AI-generated flawed proofs, we analyzed the human expert
provenance of the literature and ensuring the complete, precise          critiques provided in the original FirstProof paper [13]. We
extraction of all prerequisite conditions before any external            specifically targeted problems where the baseline LLMs were
theorem is applied.                                                      explicitly evaluated as committing unambiguous logical break-
                                                                         downs, retrieving the corresponding raw proof texts directly
                                                                         from the official FirstProof repository. There are 8 proofs
Structured Auditing via the Theorem Ledger To rigor-                     collected in this way. To ensure the inclusion of deeply ad-
ously ground external mathematical dependencies (Σi ), our               versarial examples, we augmented this set with Aletheia’s
framework asks the agent to maintain a Theorem Ledger—a                  proof 7A and OpenAI’s proof 2, both of which are recog-
centralized registry tracking external claims invoked by the             nized flawed. In particular, some of the key mathematical
agent. During the (Γi , Σi , Ti ) tuple extraction (full schema in       source material for our analysis of the FirstProof Question
Appendix), the ledger records the Status of cited theorems               7 and Question 8 cases is documented in the official solu-
Σj ∈ Σi . A deduction is marked VERIFIED only if the agent               tions/comments document and in the associated mathematical
provides explicit support (a proof sketch or precise citation)           background references [15, 16, 24, 25].
and confirms its valid applicability within the local context            Baselines and Pipeline Configurations To isolate the source
Γi . If any dependency remains OPEN, downstream reason-                  of our framework’s performance, we compare our agent
ing is flagged as conditionally closed, preventing premature             against three distinct baselines, testing the limits of direct
validation based on unvetted assumptions. This tracking mech-            prompting and textual granularity:
anism transforms verification from a black-box judgment into
a transparent, auditable process.                                         1. Global GPT-5.4-xhigh: A standard zero-shot LLM-as-a-
                                                                             judge prompt, representing the state-of-the-art capability
4     Experiments                                                            of a generic frontier model directly evaluating the mono-
                                                                             lithic text.
We design our empirical evaluation to answer two core re-                 2. Global Codex 5.4-xhigh: The identical base model used
search questions: (1) How does our structured, agentic ap-                   by our agent, prompted to globally verify the proof by
proach compare against standard global evaluators and naive                  reading sentence by sentence. Also it is told to be strict.
granular prompting across diverse mathematical fallacies? (2)                This isolates the model capacity of retrieving flaws and
How does the agent utilize its state-driven logic to navigate                gaps.
and resolve highly adversarial, research-level proofs during              3. Codex 5.4-xhigh Sentence-by-Sentence (Ablation): To
extended inference?                                                          determine whether performance gains merely stem from
To address these, we first present a comprehensive evaluation                granular reading, we implement a baseline where the
across different verification pipelines on a curated 21-proof                proof is mechanically split into single sentences. The
suite (Section 4.1 and 4.2). Subsequently, we provide a deep                 model evaluates each sentence sequentially but lacks our
qualitative analysis of the agent’s cognitive trajectory on spe-             explicit (Γi , Σi , Ti ) constraints and state-driven memory.
cific intractable cases (Section 4.3).                                       The prompts are designed to be almost the same, except it
                                                                             does not have a strict constructive framework for depen-
4.1   Experimental Setup                                                     dencies and theorems.
                                                                          4. Constructive Verification Agent (Ours): The fully
Diagnostic Suite We evaluate our framework on a highly
                                                                             equipped state-machine agent operating under the tripar-
curated diagnostic suite of 21 research-grade mathematical
                                                                             tite explanation framework.
proofs derived from the FirstProof challenge [13, 15]. This
suite comprises both fundamentally valid proofs (which may               To ensure a fair comparison, the zero-shot baseline prompt
contain minor, fixable omissions) and invalid proofs contain-            was empirically optimized through preliminary experiments to
ing fatal mathematical flaws or gaps. Specifically, we structure         faithfully elicit the model’s peak reasoning capability. Quanti-


                                                                     5
tative results for suboptimal prompt variants are omitted for                 For instance, all three baseline pipelines confidently and re-
brevity.                                                                      peatedly verified invalid proofs such as [Aletheia 7A].
Evaluation Metrics A verification attempt is considered suc-                  Without a rigorous mechanism to audit external theorems,
cessful if and only if it satisfies a strict dual-criterion: it must          these models were systematically deceived by formally
accurately assign the correct global verdict (VERIFIED or                     rigorous but mathematically vacuous text.
FLAWED), and for flawed proofs, it must correctly isolate an                • False Positives (Rejecting Valid Proofs): Conversely, on
offending step without hallucinating false negatives elsewhere                the 11 valid proofs, the baselines generated pedantic false
in the proof.                                                                 positives. They systematically flagged valid proofs such as
                                                                              [Aletheia 7B, 8B, 9A] as FLAWED, hallucinating
Data Contamination Risk and Audit Protocol Since our di-
                                                                              non-existent logical gaps or consistently complaining about
agnostic suite is derived from the public FirstProof challenge,
                                                                              standard, unstated notational conventions regardless of the
data contamination remains a serious concern when evaluating
                                                                              sampling randomness.
frontier models. For completed runs, we audited the retrieval
and reasoning logs; if a log mentioned FirstProof-related terms
or otherwise indicated direct exposure to FirstProof source
                                                                           Agent Performance In stark contrast, our Constructive Ver-
material or discussions, we discarded that run and repeated
                                                                           ification Agent achieved robust structural isolation, signifi-
the experiment. Apart from such explicit exposure, the risk
                                                                           cantly outperforming all baselines while completely taming
is substantially mitigated by the structure of the protocol: a
                                                                           the inherent stochasticity of the high-temperature setting.
verdict is not accepted merely because the model recognizes
a global answer pattern, but must be supported by local step                • Reducing False Negatives: On the 10 invalid proofs, the
elaborations, explicit dependency tracking, and auditable uses                agent successfully identified and isolated the fatal deduc-
of external knowledge. As an additional sanity check, we                      tive flaw in 100% of the cases. By strictly enforcing the
found that prompting Gemini 3.1 Pro to “find any flaws or                     (Γi , Σi , Ti ) constraints, the agent inherently blocked the
nontrivial gaps” rather than asking whether a proof is correct                mathematically invalid steps that bypassed the baseline
can solve all 21 cases in our suite. We do not interpret this as              evaluators.
evidence that a one-shot prompt is superior to our method. A                • Robustness against False Positives: On the 11 valid
more plausible concern is that Gemini may have been tuned,                    proofs, the agent correctly verified 8 proofs. For the re-
directly or indirectly, on internet-visible FirstProof materials,             maining 3 valid proofs (Aletheia 7B, 10A, 10B),
creating a risk of benchmark leakage. In particular, when                     the agent halted in the FLAWED or OPEN state due to gen-
Gemini judges that a correct solution route is valid, it may be               uinely ambiguous, unstated domain conventions. The agent
recognizing an internet-exposed answer pattern without fully                  flagged the proof of problem 10 as flawed because it strictly
attending to the subtle technical assumptions that make the                   adhered to the mathematical definition of the stated pos-
argument sound. This observation reinforces the need to treat                 itive semi-definite condition—which permits zero diago-
public benchmark results for natural-language proof verifica-                 nal entries and invalidates direct element-wise inversion—
tion with caution, and motivates our emphasis on auditable                    without adopting the human expert’s unstated practical
step-level reasoning rather than opaque global verdicts.                      convention that typical RKHS kernels inherently possess
                                                                              strictly positive diagonals. Crucially, owing to its explicit
4.2   General Verification Performance                                        Flaw Confirmation mechanism, the agent produced zero ar-
We evaluated the four pipelines on the 21-proof diagnostic                    bitrary FLAWED judgments on fundamentally sound proofs.
suite over 3 independent trials. While the standard direct                 When provided with the 7B model’s reference solution and the
prompt baseline (operating at a sampling temperature of 1.0)               initial problem conditions, our verifier successfully validated
exhibited slight outcome variance, ours framework demon-                   the proof (see Appendix C).
strated macro-level consistency, yielding identical final ver-
dicts across all runs. The aggregated results are presented in             5   Limitations and Future Works
Table 1.
This consistency reveals that the failures of standard LLMs in             While our framework demonstrates the immense potential of
mathematical verification are not artifacts of sampling noise,             LLM-based agents in verifying natural language mathematical
but stem from systemic deductive deficiencies.                             proofs, certain limitations provide clear avenues for future
                                                                           research.
                                                                           Implicit Conventions and Human-in-the-loop First, base
Baseline Performance and Failure Modes The baseline
                                                                           LLMs inherently struggle with unstated mathematical folklore,
models—Global GPT-5.4, Global Codex 5.4, and the Sentence-
                                                                           frequently mischaracterizing benign domain-specific notations
by-Sentence ablation—demonstrated severe systemic vulnera-
                                                                           as explicit flaws. To address this, a highly promising direction
bilities, consistently failing on both valid and invalid proofs
                                                                           is a human-in-the-loop (HITL) collaborative paradigm, where
across all trials.
                                                                           the agent autonomously prunes logical dependencies but dy-
 • False Negatives (Accepting Invalid Proofs): The base-                   namically queries human experts when confronting profound
   lines entirely failed to detect embedded flawed statements.             epistemic ambiguities.


                                                                       6
Table 1: Verification performance on the 21-proof diagnostic suite (avg@3 over three independent trials). We report the number
of correctly classified proofs and the specific error types (False Positives/Negatives). The agent significantly outperforms the
global baseline by systematically reducing hallucinated validations.
                                                  Valid Proofs (11 total)          Invalid Proofs (10 total)
              Pipeline                                                                                         Overall Acc.
                                               Correct (✓) False Positives Correct (✓) False Negatives

              Global GPT-5.4                       8.33             2.67            7.67            2.33          16/21
              Global Codex-5.4                     7.33             3.67              8               2          15.33/21
              Codex 5.4 Sentence-by-Sentence         9                2               9               1           18/21
              Agent (Ours)                          8                3               10              0            18/21



Residual Hallucinations vs. Formal Guarantees Second,                          D. Hwang, et al., “Aletheia tackles firstproof au-
unlike formal theorem provers that offer absolute mechanical                   tonomously,” arXiv preprint arXiv:2602.21201, 2026.
guarantees, our purely text-based agent remains susceptible to
subtle hallucinations. These can happen when the agent overly              [3] H. Ju, G. Gao, J. Jiang, B. Wu, Z. Sun, L. Chen, Y. Wang,
simplifies the application of complex, web-retrieved external                  Y. Wang, Z. Wang, W. He, et al., “Automated conjec-
theorems. While our current system mitigates this by enforc-                   ture resolution with formal verification,” arXiv preprint
ing strict (Γi , Σi , Ti ) constructive elaborations, it does not              arXiv:2604.03789, 2026.
currently employ a secondary adversarial pass to actively hunt
                                                                           [4] L. de Moura and S. Ullrich, “The lean 4 theorem prover
for flaws within its own accepted deductions. Future work will
                                                                               and programming language,” in Automated Deduction–
introduce an iterative, adversarial re-verification mechanism
                                                                               CADE 28: 28th International Conference on Automated
to critically audit steps that have already transitioned to the
                                                                               Deduction, Virtual Event, July 12–15, 2021, Proceedings
VERIFIED state, further minimizing false negatives.
                                                                               28, pp. 625–635, Springer, 2021.
Large-scale Evaluation Finally, while our curated 21-proof
diagnostic suite enables deep, qualitative dissection of the               [5] The mathlib Community, “The Lean mathematical li-
agent’s cognitive trajectory and failure modes, scaling this                   brary,” 2019.
evaluation to a massive, multi-domain benchmark of formal
                                                                           [6] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jam-
and informal mathematics remains an important next step to
                                                                               nik, and C. Szegedy, “Autoformalization with large lan-
fully chart the generalization bounds of our architecture.
                                                                               guage models,” 2022.
In conclusion, pure natural language mathematical agents are
poised to drive continued breakthroughs in the near future. Our            [7] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jam-
work demonstrates a fundamental cognitive parallel: much                       nik, T. Lacroix, Y. Wu, and G. Lample, “Draft, sketch,
like human mathematicians, autonomous agents can signifi-                      and prove: Guiding formal theorem provers with infor-
cantly elevate their ability to discern valid mathematical rea-                mal proofs,” 2022.
soning from flawed logic simply through the rigorous act of
detailed elaboration. Ultimately, our contribution extends be-             [8] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers,
yond a standalone verifier implementation. More crucially,                     D. Radev, and J. Avigad, “Proofnet: Autoformalizing
we present a generalizable verification paradigm that can                      and formally proving undergraduate-level mathematics,”
be seamlessly integrated into the internal reasoning pro-                      2023.
cesses of any future natural language mathematical agent.                  [9] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song,
                                                                               S. Yu, S. Godil, R. Prenger, and A. Anandkumar, “Le-
References                                                                     andojo: Theorem proving with retrieval-augmented lan-
 [1] DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song,                          guage models,” 2023.
     R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi,
                                                                        [10] K. Zheng, J. M. Han, and S. Polu, “Minif2f: a cross-
     X. Zhang, X. Yu, Y. Wu, Z. F. Wu, Z. Gou, Z. Shao,
                                                                             system benchmark for formal olympiad-level mathemat-
     Z. Li, Z. Gao, A. Liu, B. Xue, B. Wang, B. Wu, B. Feng,
                                                                             ics,” 2021.
     C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, D. Dai,
     D. Chen, D. Ji, E. Li, F. Lin, F. Dai, F. Luo, G. Hao,             [11] H. Lightman, V. Kosaraju, Y. Burda, H. Edwards,
     G. Chen, G. Li, et al., “Deepseek-R1: Incentivizing rea-                B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever,
     soning capability in LLMs via reinforcement learning,”                  and K. Cobbe, “Let’s verify step by step,” arXiv preprint
     2025.                                                                   arXiv:2305.20050, 2023.

 [2] T. Feng, J. Jung, S.-h. Kim, C. Pagano, S. Gukov,                  [12] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun,
     C.-C. Tsai, D. Woodruff, A. Javanmard, A. Mokhtari,                     L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano,


                                                                    7
     C. Hesse, and J. Schulman, “Training verifiers to solve          A.1   Instruction Prompts
     math word problems,” 2021.
                                                                            Prompt 1: Initialization
[13] M. Abouzaid, A. J. Blumberg, M. Hairer, J. Kileel, T. G.
     Kolda, P. D. Nelson, D. Spielman, N. Srivastava, R. Ward,          Run a fully automatic verifier in
     S. Weinberger, and L. Williams, “First proof,” 2026.               this folder. Read only README.md,
                                                                        STEP_TEMPLATE.txt, OUTPUT_FORMATS.txt,
[14] First Proof Project, “First batch | first proof project,”          and source/input.txt.
     2026. Project page for the first batch of First Proof              Split the proof into minimal logical
     problems.                                                          deduction units. Every original source
                                                                        sentence with mathematical content
[15] First Proof Project, “First proof solutions and comments,”         must appear verbatim in the Original
     2026. Official solutions and commentary PDF for the                step field of at least one step file.
     First Proof project.                                               Initialize steps/. Repeatedly work
                                                                        on the most critical untouched step,
[16] S. Weinberger, Variations on a Theme of Borel: An Es-              otherwise the most critical open step.
     say on the Role of the Fundamental Group in Rigidity.              Each step file must be a thick
     Cambridge University Press, 2022.                                  elaboration organized by (Γi , Σi , Ti ),
                                                                        with the full original step, the exact
[17] D. W. Morris, Introduction to arithmetic groups, vol. 2.           target assertion, a detailed deduction,
     Deductive Press Lieu de publication inconnu, 2015.                 and a diagnosis. Treat every step as
                                                                        requiring its own local closure analysis:
[18] OpenAI, “Planar point sets with many unit distances,”              never mark a step VERIFIED without
     2026. https://cdn.openai.com/pdf/74c24085-19b0-4534-               individually checking its own written
     9c90-465b8e29ad73/unit-distance-proof.pdf.                         Γi , Σi , Ti , Deduction, and every used
                                                                        item of Σi .
[19] J. Liu, Z. Sun, and J. Jiang, “Optimal bounds in bend-and-         For every used item of Σi , write the
     break for foliations,” arXiv preprint arXiv:2605.20754,            exact as-used statement and include
     2026.                                                              either a proof or a precise source,
                                                                        plus a brief applicability note. Be
[20] J. Liu and S. Qin, “Shokurov’s global index                        conservative: if a used item of Σi is
     conjecture for threefold foliations,” arXiv preprint               not closed by direct local reasoning, or
     arXiv:2605.22735, 2026.                                            by a proof or precise source that you
                                                                        can state concretely in the step file,
[21] J. Liu, R. Hu, and S. Qin, “Boundedness of total cartier           keep it OPEN rather than VERIFIED. Do
     indices for rational singularities in families,” arXiv             not treat a statement as ‘confirmed’
     preprint arXiv:2605.22782, 2026.                                   merely because it looks standard or
                                                                        plausible.
[22] N. de Bruijn, “The mathematical vernacular, a language             A step is VERIFIED only if every used
     for mathematics with typed sets,” in Selected Papers on            item of Σi is ‘confirmed’; otherwise it
     Automath (R. Nederpelt, J. Geuvers, and R. de Vrijer,              is OPEN, unless there is an explicit
     eds.), vol. 133 of Studies in Logic and the Foundations            flaw witness, in which case it is
     of Mathematics, pp. 865–935, Elsevier, 1994.                       FLAWED. Initialize the verifier now:
                                                                        split the proof into detailed minimal
[23] M. Ganesalingam, “The language of mathematics,” in                 proof-obligation steps, splitting
     The Language of Mathematics: A Linguistic and Philo-               explicit intermediate assertions before
     sophical Investigation, pp. 17–38, Springer, 2013.                 downstream consequences. Maintain only
                                                                        steps/, dependency.txt, stepsprocess.txt,
[24] A. Alfieri and C. Novak, “Research report: some con-               and answer.txt. Stop only when every
     structions in polyhedral symplectic topology suggested             step has been judged as VERIFIED, OPEN,
     by ai,” 2026.                                                      or FLAWED.

[25] J. Fowler, “Finiteness properties for some rational
     Poincaré duality groups,” Illinois Journal of Mathemat-                Prompt 2: Resume
     ics, vol. 56, no. 2, pp. 281–299, 2012.
                                                                        Resume the verifier in this folder.
                                                                        Read README.md, STEP_TEMPLATE.txt,
A    Prompts for the Verification Agent                                 OUTPUT_FORMATS.txt, dependency.txt,
                                                                        stepsprocess.txt, answer.txt, and all
In this appendix, we present the prompts used to drive our              unresolved files in steps/.
state-based verification agent. The prompts are administered            If there is a step that is too coarse,
to the Codex agent as fixed instruction prompts.                        resplit the unresolved file that is



                                                                  8
still too coarse to be one minimal                 If yes, keep FLAWED. If not, change
logical deduction unit. Every original             it to OPEN and explain exactly why the
source sentence with mathematical                  witness fails.
content must appear verbatim in the
Original step field of at least one step
file. Then continue the main loop.
                                                A.2   File Formats and Step Templates
If a step has remained OPEN since the           To enforce strict state tracking and prevent the LLM from
first pass and still resists closure,           generating unstructured text, the agent is required to output
consider whether it has an explicit             its intermediate reasoning and global status into highly con-
flaw witness and should be FLAWED. For
                                                strained text files. The formats for these ledgers and templates
any current OPEN step hard to resolve,
                                                are defined below.
consult the local reference/* materials
or search online for relevant detailed                Prompt 4: Global Ledgers (OUTPUT_FORMATS.txt)
information, exact statements, or
precise sources. *If search online, you            [dependency.txt]
should only look for standard text book            List only external statements that are
or references that DIRECTLY CONNECT to             still OPEN or already FALSE.
the specific problem. DO NOT accept                Format:
randomly retrieved papers merely to                D1
force a proof to work.*                           - step(s):
Before changing any unresolved step to            - exact as-used statement:
VERIFIED, recheck that every used item            - status: OPEN / FALSE
of Σi has an exact as-used statement              - why:
together with either a proof or a                 - offending point if false:
precise source. Do not mark a step
                                                   [stepsprocess.txt]
VERIFIED by replacing the original
                                                   For each step:
inference with a different proof or
                                                   Step:
alternative argument. Default negative
                                                  - status: UNTOUCHED / OPEN / VERIFIED /
verdict is OPEN. Use FLAWED only with an
                                                   FLAWED
explicit flaw witness.
                                                  - minimal unit: yes / no
                                                  - criticality:
                                                  - main blocker:
                                                  - all used sigma closed: yes / no
 Prompt 3: Flaw Confirm                           - flaw witness:
                                                  - next action:
Investigate whether the FLAWED step                [answer.txt]
in this folder is actually FLAWED.                 Format:
Read README.md, STEP_TEMPLATE.txt,                 Overall verdict: RUNNING / VERIFIED /
OUTPUT_FORMATS.txt, dependency.txt,                FLAWED
stepsprocess.txt, answer.txt, the                  Current key step:
unresolved files in steps/, and                    If FLAWED:
reference/* if present.                           - offending step:
Choose exactly one currently FLAWED step,         - exact false statement or invalid
preferably the most critical one. Keep             inference:
the Original step verbatim and keep the           - flaw witness:
same final assertion. First investigate            If still running:
the step: expand the relevant concepts,           - remaining open steps:
exact statements, hypotheses, scope, and          - active dependencies:
nearby lemmas in the local reference/*             Per-step summary:
materials and online source, and use              - step:
this to judge whether the recorded flaw           - status:
witness shows that the original sentence          - one-line reason:
or exact as-used inference is false or             Rule:
invalid as written.                                Do not use FLAWED unless an explicit
Do not treat a mere wording, naming,               flaw witness has been written.
or terminology imprecision as a                    Do not use VERIFIED unless all used
flaw witness unless it changes the                 external statements are marked
mathematical claim, breaks the local              ‘confirmed’.
inference, or materially threatens the
validity of the proof.



                                            9
     Prompt 5: Logical Unit Template (STEP_TEMPLATE.txt)                    Let si be a deduction step of S. Let the statement ai be the
                                                                            assertion of si . Unlike fully formalized proofs in systems
   Step ID:
                                                                            like Lean or Rocq, natural language mathematical proofs
  Why this is one minimal logical
                                                                            inherently omit trivial algebraic manipulations and elementary
   deduction unit:
   Original step:                                                           logical deductions to maintain readability. In this paper,
   [paste the full original step string                                     we do not require the LLM to elaborate proofs down to
  verbatim]                                                                 atomic axiomatic steps, as this would lead to an unnatural
  Target assertion ai :                                                     combinatorial explosion of reasoning length and degrade
   Original route:                                                          model performance. When defining the assertion ai extracted
   Explanation:                                                             from a natural language proof, we adopt a stance of founda-
   [write a thick natural-language                                          tional agnosticism. Modern informal mathematics—ranging
   elaboration that preserves the same                                      from elementary calculus to advanced subjects like Topos
   assertion and route]                                                     theory or Wiles’ proof of Fermat’s Last Theorem—is rarely
   Statement Extraction (Γi , Σi , Ti ):
                                                                            written with a strict, singular axiomatic foundation (e.g.,
  Assertion:
                                                                            pure ZFC) in mind. Therefore, we do not restrict ai to a
   Local Context Γi :
  - γ1 :                                                                    specific foundational axiomatic system. Rather, we assume
  - γ2 :                                                                    the existence of a sufficient, implicit foundational theory that
   Global Knowledge Σi :                                                    is universally accepted for the specific domain of the proof.
  - σ1 :
      exact as-used statement:                                              We must also address the validity of natural language
      proof or precise source:                                              statements that appear underspecified in isolation, such as
      why it applies here:                                                  the simple assertion a = b. In strict formal systems, an
      status: confirmed / OPEN / false
                                                                            equality requires explicit type alignment (e.g., verifying
  - σ2 :
   Sigma Support:
                                                                            that both sides belong to the same algebraic structure). In
   [for each used σj , include either a                                     well-formed (which we may assume) natural mathematical
   proof or a precise source]                                               discourse, however, such type constraints are rarely restated
   Background Theory Ti :                                                   at every step; instead, they are implicitly inherited from the
  - t1 :                                                                    ambient context (captured by Γi in our framework). As long
  - t2 :                                                                    as a statement is semantically well-posed within this context,
   Deduction:                                                               it operates as a valid deductive step. Demanding explicit
   [derive the assertion from Γi , confirmed                                syntactic completeness for every variable introduces an
  Σi , and Ti ; if some used σj is still                                    unnatural overhead that misaligns with human communication.
   OPEN, state that the route is only                                       Ultimately, if we accept a natural language proof as a
   conditionally closed]
                                                                            valid logical artifact, we must recognize that its constituent
   Diagnosis:
  - conclusion preserved:
                                                                            statements—though syntactically incomplete in isolation—are
  - route preserved:                                                        rigorously well-defined when situated in the proof’s narrative
  - exact offending dependence, if any:                                     flow. Crucially, this approach does not imply an omission of
  - flaw witness, if any:                                                   type verification. Rather, by isolating type-related statements,
   Step Result:                                                             we can safely and cleanly decouple the structural type
  - status: UNTOUCHED / OPEN / VERIFIED /                                   constraints from the core deductive logic, making the natural
   FLAWED                                                                   language step significantly easier to evaluate.
  - main blocker:
  - flaw witness:
                                                                            For a practical way to formalize the elaboration process,
  - dependencies:
  - last update:
                                                                            we define an explanation of the step si as a triple of sets
                                                                            (Γi , Σi , Ti ), which encompasses all the necessary statements
                                                                            required to logically derive the assertion ai . Thus for any
B Extended Discussion on the (Γi , Σi , Ti )                                elaboration s′i (in natural language), there exists a explanation
  Framework and Explanation Validity                                        (Γi , Σi , Ti ) that explain s′i . In this context, we say the
                                                                            triple explains the elaboration if every critical mathematical
Consider a natural language proof text S and its ordered                    assertion articulated within the natural language elaboration
sequence of steps (substrings) (s1 , s2 , . . . , sn ). Without loss        and the step is subsumed either directly by the sets of the
of generality (by carefully choosing the substrings for steps               triple or by the intermediate statements deduced during the
and using conjunction) , we restrict that a step contains                   derivation process. Moreover, the derivation logically entailed
at most one new mathematical statement. Throughout the                      by this triple must strictly adhere to the specific computational
paper, we consider assumptions and declarations both as                     or deductive methodology dictated by the natural language
mathematical statements.                                                    text. Γi contains finitely many statements (theorems, lemmas,
                                                                            definitions, and hypothesis) from S. The statements within


                                                                       10
Γi may either be explicitly stated in S or left implicit. Σi             ity of the local context in eliminating ambiguity, we can omit
comprises a finite set of statements drawn from external                 type declarations for the assertions and the other statements.
literature or established domain consensus, that is, outside
                                                                                                                         √
of S. Here statements from Σi are considered non-trivial.                   Case Study: Deconstructing the Proof of          2∈
                                                                                                                              /Q
Within an explanation of s′i , there may exist statements
from Σi that are implicitly assumed rather than explicitly                  Background   √ Proof Context:
articulated in s′i . Ti comprises a finite set of what are often            Theorem: 2 is an irrational number.
considered trivial statements (or rewrite rules) representing               Step
                                                                            √ 1 (s1 ): Assume for the sake of contradiction that
the background theory. It assists Γi and Σi in syntactically                   2 is a rational number.
deriving the assertion ai . Fundamentally, our framework                    Step 2 (s2 ): By the definition of rational numbers,
aims to model any detailed elaboration of a proof step.                     there
                                                                            √      exist integers a and b (where b ̸= 0) such that
Consequently, any mathematical statement invoked in such an                    2 = ab .
expanded derivation must necessarily originate from this triple.            Step 3 (s3 ): We can further assume that a and b are
                                                                            coprime (i.e., the fraction ab is in its simplest form,
When we say a step si is valid, we usually mean there exists                sharing no common factors other than 1).
an explanation (Γi , Σi , Ti ) of si such that:                             Step 4 (s4 ): Squaring both sides of the equation gives
                                                                                   2
                                                                            2 = ab2 .
                        Γi , Σi , Ti ⊢ ai                                   Step 5 (s5 ): Multiplying both sides by b2 yields 2b2 =
                                                                            a2 .
Here ⊢ denotes a rigorous informal entailment. Also, all                    Step 6 (s6 ): Since b is an integer, b2 is an integer,
Γi , Σi , Ti are valid. For Γi to be valid, all the statements it           making 2b2 an even number. Therefore, a2 must be an
contains should first be effective in the step si . Statements in           even number.
S has their scope of effectiveness. A context statement (an                 Step 7 (s7 ): If the square of an integer is even, then
assumption or a declaration) has its scope: assumptions and                 the integer itself must be even. Thus, a is an even
variables are no longer valid from a certain point onwards.                 integer.
Consequently, si may also fall outside the scope of other                   Step 8 (s8 ): Since a is even, there exists an integer k
preceding mathematical statements, including lemmas                         such that a = 2k.
and theorems. For example, if the proof contains a case                     Step 9 (s9 ): Substituting a = 2k into the equation
analysis, then for every case the proof establishes a block                 from Step 5 (2b2 = a2 ) gives 2b2 = (2k)2 = 4k 2 .
with the corresponding assumption. The assumption’s scope                   Step 10 (s10 ): Dividing both sides by 2 yields b2 =
terminates once the discussion for the case is over. The                    2k 2 .
theorems and lemmas proved in the case may also be invalid                  Step 11 (s11 ): Following the same logic as before, this
for the next case, if local assumptions and declarations                    implies that b2 is an even number.
are used. Second, any implicit statements within Γi must                    Step 12 (s12 ): Consequently, b must also be an even
be validly inferred from the context. The admissibility of                  number.
such implicit elements is highly sensitive to both the active               Step 13 (s13 ): Since both a and b are even numbers,
discourse and the established consensus of the mathematical                 they share a common factor of at least 2.
community. Consequently, LLMs should be able to correctly                   Step 14 (s14 ): This directly contradicts our assump-
identify valid implicit statements based on the context. Finally,           tion in Step 3 that a and b are coprime.
since Γi contains deductions and theorems from the context,                 Step 15 (s15 ): Therefore, our initial√assumption in
the statements of Γi should all be valid. For Σi to be valid, all           Step 1 must be false, concluding that 2 is irrational.
statements within it must be drawn from universally accepted
mathematical facts or sound external literature.
                                                                            Step 7 (s7 ):
                                                                             • Assertion (a7 ): a is an even integer.
We now explain the validity of Ti . Since Ti captures the rou-
tine background steps skipped by human writers, it provides                  • Local Context (Γ7 ): {a2 is even}∪{a ∈ Z} (Note:
a practical interface between informal mathematical text and                   a ∈ Z is an implicit statement)
formal axioms. There is an immediate problem of what is                      • Global Knowledge (Σ7 ):                {∀n    ∈
considered as a nontrivial statement and has to be written                     Z, n2 is even =⇒ n is even}
explicitly. Since the explanation here actually corresponds                  • Background Theory (T7 ): ∅ (Direct application
to expanded derivations of si , the threshold for non-triviality               of Modus Ponens)
can be carefully calibrated. Also, for Ti to be valid, all the
statements it contains should be logically sound. Throughout                Step 9 (s9 ):
this framework, we operate under the standard assumption of                  • Assertion (a9 ): 2b2 = (2k)2 = 4k 2 .
soundness for the underlying mathematical foundation. Let us                 • Local Context (Γ9 ): {a = 2k, 2b2 = a2 }
now consider a simple example of a proof and two possible                    • Global Knowledge (Σ9 ): ∅ (No external lemmas
explanation of different steps. Note that by admitting the valid-


                                                                    11
                                                                         Case Study: Extraction Of Statements
       invoked)
     • Background Theory (T9 ): Equivalence proper-                      Problem and Proof Sketch
       ties of equality (e.g., symmetry, transitivity, and               Problem: Suppose that Γ is a uniform lattice in a real semi-
       substitution/congruence) combined with fundamen-                  simple group, and that Γ contains some 2-torsion. Is it possible
       tal properties of integer arithmetic (e.g., commuta-              for Γ to be the fundamental group of a compact manifold with-
       tivity, associativity, and evaluation of ground con-              out boundary whose universal cover is acyclic over the rational
       stants such as 2 × 2 = 4).                                        numbers Q?
                                                                         Proof: The generated proof constructs a logical contradiction
                                                                         centered around the compactly supported Lefschetz number,
                                                                         Lc (γ, X). The model computes this topological invariant
We now analyze the benefits of not restricting Ti to rigid, hard-        through two divergent pathways. Algebraically, it correctly
coded rules, primarily regarding its interface with foundational         applies Poincaré duality alongside the Q-acyclicity of X to
axioms. Although we do not specify a definitive axiomatic sys-           deduce that Hc∗ (X; Q) is concentrated exclusively in the top
tem, our framework inherently assumes universally permitted              degree, cleanly evaluating to Lc (γ, X) = ±1 ̸= 0. Topo-
operations like Modus Ponens. This universal compatibility               logically, the model evaluates the 2-sheeted regular covering
                                                                         X → Y = X/⟨γ⟩ using the transfer map, arriving at the
affords us considerable flexibility in formally specifying
                                                                         valid relation χc (Y ) = 12 (χc (X) + Lc (γ, X)). However, to
Ti . Furthermore, the flexibility in specifying Ti drastically           mathematically force a contradiction, the model introduces a
reduces the deductive overhead within ⊢ and minimizes the                critical hallucination: it erroneously asserts that the compactly
total number of explicit statements required. For example,               supported Euler characteristic is strictly multiplicative (i.e.,
in formal libraries like Lean’s Mathlib, performing basic                χc (X) = 2χc (Y )) for infinite cell complexes. By substituting
integer arithmetic typically necessitates instantiating deep             this flawed generalization into the transfer equation, the gener-
algebraic hierarchies, such as commutative rings. In contrast,           ated proof strictly forces Lc (γ, X) = 0, resulting in the false
allowing all kinds of sound statements bypasses this formal              algebraic contradiction 0 = ±1.
complexity, enabling the system to directly reason with sound
statements over Z. Furthermore, since the operations within
Ti are inherently routine, we can leverage this flexibility              Step si (Flawed)
                                                                         "However, for any finite k-sheeted unbranched covering of
to formulate statements directly about the concrete objects,
                                                                         locally compact ENRs with finite Betti numbers, the compactly
bypassing the need for explicit variable substitution. This
                                                                         supported Euler characteristic is strictly multiplicative. Thus,
also mirrors human conventions in mathematical discourse:                χc (X) = 2χc (Y )."
when executing elementary transformations, we naturally
manipulate the expressions directly. Consequently, the ele-
ments within T9 are concrete statements like (2k)2 = 2k · 2k,            Explanation generated by LLM
rather than abstract, uninstantiated schemas such as x2 = x·x.           The author introduces a general rule regarding covering spaces.
                                                                         They assert:
                                                                              “for any finite k-sheeted unbranched covering... the
Note that the explicit type declaration a2 ∈ Z is omitted from                compactly supported Euler characteristic is strictly
Γ7 for the same reason we bypass redundant variable bindings.                 multiplicative.”
By the ambient context, we establishes a ∈ Z. And since                  Expressed as a mathematical formula, the author is asserting
{∀n ∈ Z, n2 is even =⇒ n is even} is an unambiguous                      that for any total space E and base space B connected by a
well-established statement under the current context, we don’t           k-sheeted covering map, the relationship is:
need to write a2 ∈ Z here. Consequently, an explanation
(Γi , Σi , Ti ) should not be viewed as the complete set of all                               χc (E) = k · χc (B)
contextually valid truths, but exclusively as the minimal                To use this general formula, the author must establish the spe-
required set of statements necessary to validate the natural             cific values for E, B, and k based on the geometry of the spaces
language proof step rigorously.                                          in the proof.
                                                                          • The Total Space (E): The author is using X (the universal
                                                                             cover of the manifold M ) as the total space.
In the example above, we directly structured an elaboration               • The Base Space (B): The author defines the base space Y
using the (Γi , Σi , Ti ) format. In what follows, we demonstrate            as the quotient X/⟨γ⟩.
that given an elaboration s′i of a proof step, we can extract its         • The Sheet Count (k): The author establishes that γ is a
constituent statements and systematically categorize them into               torsion element of order 2 (γ 2 = id). Because γ generates
this triple framework. Then, find an explanation that explains               a strictly free action of Z/2Z on X, the projection map
s′i , though the explanation may not be valid. Consider the                  from X down to the quotient Y is a regular covering map.
following example from Firstproof generated by Aletheia.                     Because the group acting on it has exactly 2 elements, the
                                                                             number of “sheets” (the size of the fiber over any point in
                                                                             Y ) is exactly 2. Therefore, k = 2.
                                                                         The author takes the specific parameters established in Step 2:



                                                                    12
                                                                            highlighted statement corresponds to t1 . The blue highlighted
   • E→X
                                                                            statement corresponds to γ1 . Notice a few things here. First,
   • B→Y
                                                                            we ignore the statements “γ generates a strictly free action
   • k→2
                                                                            of Z/2Z on X,” and “the group acting on it has exactly 2
  And substitutes them directly into the general formula from
                                                                            elements.” But we still consider our (Γi , Σi , Ti ) explains the
  Step 1 (χc (E) = k · χc (B)).
  This direct application of the parameters to the multiplicative           elaboration. By definition, the explanation should contain
  rule yields the final assertion:                                          every critical mathematical assertion articulated within the
                                                                            natural language text. Thus, by considering the above two
                         χc (X) = 2χc (Y )                                  statements to be not critical (which is reasonable), we can
                                                                            simplify our (Γi , Σi , Ti ). Given the inherent linguistic vari-
  That is the entirety of the deduction for that specific step. The
                                                                            ations and rhetorical scaffolding present in human-authored
  author simply proves the covering is 2-sheeted and plugs k = 2
  into their (flawed) multiplicative formula.                               proofs, the extraction of critical statements from natural lan-
                                                                            guage inherently demands a degree of flexibility. Second, we
                                                                            did not take arguments like E is X into account. This is also
  Statement Extraction (Γi , Σi , Ti )                                      for simplification. By the same manner of the first example,
  Assertion (ai ): χc (X) = 2χc (Y ).                                       we omit the detail of Modus Ponen. The generated elaboration
  Local Context (Γi ):                                                      doesn’t verify all required conditions (for example, finite Betti
  γ1 : The projection X → Y is a 2-sheeted regular covering                 number) for the flawed theorem, thus we can fill them up in the
  map, generated by a strictly free group action.                           explanation. Though the deduction process ⊢ of the explana-
  γ2 : Hc∗ (X; Q) and Hc∗ (Y ; Q) are finite-dimensional.                   tion is sound, the statements it contains are not valid, making
  γ3 : X is an n-dimensional topological manifold. Y is a topo-             the explanation itself not valid. For certain steps, the logi-
  logical manifold.
                                                                            cal deduction is sufficiently explicit that it requires almost no
  All of them are explicit.
  Global Knowledge (Σi ):
                                                                            hidden calculations, rendering the corresponding elaboration
  σ1 : [Flawed lemma] For any finite k-sheeted unbranched cov-              essentially deterministic in practice.
  ering of locally compact ENRs with finite Betti numbers, the              In summary, this work seeks to analyze the rigor of natural
  compactly supported Euler characteristic is strictly multiplica-          language mathematical proofs. We do not attempt to enforce
  tive.                                                                     the absolute strictness required by systems like the Mathemat-
  σ2 : Every finite-dimensional topological manifold is a locally           ical Vernacular (MV) or formal proof assistants. Empirically,
  compact ENR.
                                                                            however, we demonstrate that subtle logical errors can be suc-
  σ3 : A topological manifold has finite compactly supported
                                                                            cessfully localized simply by writing out the proof in granular
  Betti numbers if its compactly supported rational cohomology
  is finite-dimensional.                                                    detail. The critical factor in this approach is maintaining strict
  σ4 : If X → Y is a covering map between manifolds, then                   faithfulness to the author’s original intent. Ultimately, our the-
  dim(Y ) = dim(X).                                                         oretical framework serves primarily as philosophical guidance
  Background Theory (Ti ):                                                  for the agent’s reasoning, rather than a rigid requirement to
  t1 : The property of ’the Euler characteristic being strictly mul-        perfectly instantiate every formal explanation. As our experi-
  tiplicative’ is defined by the following equation under algebraic         ments confirm, the mere act of forcing the agent to elaborate
  rewrite rules: χ(total space) = k · χ(base space), where k is             in detail intrinsically elevates its verification performance.
  the number of sheets of the covering.
  t2 : A regular covering map generated by a strictly free group            C    Case Study: The Boundary of Implicit Con-
  action is an unbranched covering.
  t3 : A k-sheeted covering is finite.                                           ventions (Aletheia 7A & 7B)
                                                                            To gain deeper insights into the agent’s cognitive trajectory,
                                                                            we present a detailed comparative case study on the proofs
  Deduction ⊢
  Since γ1 establishes a covering map X → Y and γ3 identifies
                                                                            Aletheia 7A (invalid) and Aletheia 7B (valid).
  both as manifolds, σ4 confirms they share the same dimen-                 The original text of 7A actually consists of two separate proofs:
  sion n, which by σ2 ensures both are locally compact ENRs.                the first is an invalid pseudoproof containing a highly con-
  Concurrently, because γ2 confirms their compactly supported               cealed, fatal error concerning “multiplicity”, while the second
  rational cohomology is finite-dimensional, σ3 guarantees both             fundamentally relies on the first. For GPT-5.4, formulating a
  possess finite compactly supported Betti numbers. Given that              precise disproof for this specific error is difficult, as explicit
  γ1 specifies the action is strictly free, t2 classifies it as un-
                                                                            counterexamples are scarcely available via web retrieval and
  branched, and since it is a 2-sheeted covering, t3 confirms it is
                                                                            fall outside the model’s internal parametric knowledge. Fur-
  finite k-sheeted (k = 2). With all prerequisites of the flawed
  lemma σ1 met (a finite k-sheeted unbranched covering of lo-               thermore, within the specific scope of FirstProof Problem 7, it
  cally compact ENRs with finite Betti numbers), we apply t1                is an accepted academic convention to assume that semisimple
  with k = 2 to yield the final assertion ai : χc (X) = 2χc (Y ).           Lie groups are linear—an assumption that does not strictly
                                                                            hold in general mathematical contexts. Consequently, an un-
                                                                            guided agent is highly susceptible to being distracted by this
The green highlighted part corresponds to σ1 . The yellow                   linearity assumption (generating a false flaw witness) or by


                                                                       13
downstream errors in the second proof.                                    mathematical communication.
To stress-test our agent’s ability to identify the true structural
error, we manually truncated 7A to include only the first proof           D    Prompts for the Sentence-by-Sentence Abla-
and explicitly appended the linearity condition. Across 10 in-                 tion Baseline
dependent runs, the agent yielded one false negative (marking
the flawed step as VALID during initialization rather checking            In this section, we present the prompts used for the Sentence-
it carefully) and successfully rejects the proof 9 times, marking         by-Sentence ablation baseline discussed in Section 4.1.
the specific step OPEN or FLAWED. However, a closer inspec-               Unlike our main Constructive Verification Agent, which
tion reveals a critical logical subtlety: the agent justified its         strictly enforces the (Γi , Σi , Ti ) tripartite structure and main-
FLAWED verdict by pointing out that the multiplicity claim ex-            tains an explicit external theorem ledger, this ablation base-
plicitly contradicted the local context. While this contradiction         line is designed to test the effect of mere textual granularity.
genuinely exists, penalizing the step strictly on these grounds           Specifically, it instructs the agent to break the proof down into
is mathematically unreasonable here, as the step resides within           sentence-level steps but only requests a “plain naive analysis
a proof by contradiction (reductio ad absurdum)—where de-                 in prose” without rigid dependency tracking. This isolates
riving absurdities is the expected trajectory. This highlights            the performance gains achieved by our structured deductive
the profound difficulty in distinguishing between an invalid              constraints from the gains naturally occurring when LLMs
inference rule and a valid derivation of a contradiction.                 process text at a granular level. To ensure a fair and controlled
Conversely, our experiments on the fundamentally valid proof              ablation, the overall execution pipeline—including the reflec-
Aletheia 7B perfectly illuminate the agent’s underlying                   tion and flaw confirmation prompts—remains identical to our
verification power and its dynamic self-correcting capabili-              primary version.
ties. Though the agent fail to validate the proof in the 3 runs,
when we evaluated 7B by explicitly providing the linearity                     Ablation Prompt 1: Initialization
assumption and the reference solution sketch, the agent did not
simply rubber-stamp the text. Instead, it exhibited a rigorous,               Run the verifier in this folder. Read
non-linear cognitive trajectory.                                              only README.md and source/input.txt.
                                                                              Split the proof into small steps.
During the verification process, the agent initially proposed
                                                                              Create one .txt file in steps/ for
two potential flaw witnesses that threatened to invalidate the                each step. Every original source
proof. In one of them, the agent’s web retrieval module re-                   sentence with mathematical content must
turned an alternative formulation of a specific series expansion.             appear verbatim in at least one step
Detecting a difference from the retrieved literature, the agent               file. Initialize or refresh steps/,
instinctively marked the author’s step as FLAWED. The action                  stepsprocess.txt, and answer.txt.
is then rejected by our Flaw Confirmation mechanism. En-                      On the first pass, do not read
gaged in adversarial self-reflection, the agent re-evaluated the              source/theory.txt, source/example.txt,
discrepancy and recognized that the mere existence of a dif-                  source/standards.txt, or reference/*.
ferent formalization online does not mathematically invalidate                Work step by step. In each step file,
                                                                              keep the original text and then write
the author’s specific local derivation. Consequently, the agent
                                                                              a plain naive analysis in prose of
correctly dismissed its own false alarm, averting a premature
                                                                              whether the step closes, what is missing,
false positive.                                                               or whether there is an explicit flaw
After overriding these superficial discrepancies and conduct-                 witness. Be conservative: if the step
ing further targeted retrieval, the agent meticulously verified               is not convincingly closed, keep it OPEN.
the highly non-trivial claims regarding KO-theory (real topo-                 Use FLAWED only with an explicit flaw
logical K-theory) and successfully closed the proof.                          witness.
                                                                              Maintain only steps/, stepsprocess.txt,
This juxtaposition offers a more grounded observation: when                   and answer.txt. Stop only when every
explicit premises are provided, the agent is capable of                       step has been marked VERIFIED, OPEN, or
processing complex mathematical concepts like K-theory.                       FLAWED.
More importantly, this iterative pattern—searching for ex-
ternal literature, raising potential issues, and self-correcting—
demonstrates a practical pathway for scaling test-time compute
in mathematical verification. By allocating more inference                     Ablation Prompt 2: Resume
steps to information gathering and adversarial reflection, the                Resume the verifier in this folder.
system can progressively resolve textual ambiguities. How-                    Read README.md, stepsprocess.txt,
ever, the agent’s frequent stalling on implicit human conven-                 answer.txt, and all unresolved files in
tions serves as a humbling reminder. It indicates that while                  steps/. If a step is still too coarse,
deductive logic and external retrieval are necessary, they are                split it smaller. Every original source
not yet sufficient to fully bridge the gap between strict formal-             sentence with mathematical content must
ization and the nuanced, context-dependent nature of human


                                                                     14
    appear verbatim in at least one step                                 Table 2: Complete hyperparameter configurations applied
    file.                                                                directly to the GPT-5.4-xhigh API endpoints across all verifi-
    Continue step by step. If a step has                                 cation pipelines.
    remained OPEN since the first pass,
                                                                                            Hyperparameter       Value
    consider whether there is an explicit
    flaw witness and it should be FLAWED.                                                   Temperature           1.0
    For a hard OPEN step, you may consult                                                   Top-p                 1.0
    reference/* or search online for
                                                                                            Top-k                  0
    relevant details. Before changing any
    unresolved step to VERIFIED, recheck                                                    Min-p                 0.0
    that the step really closes.                                                            Top-a                 0.0
    Default negative verdict is OPEN.                                                       Frequency Penalty     0.0
    Use FLAWED only with an explicit                                                        Presence Penalty      0.0
    flaw witness. Maintain only steps/,
                                                                                            Repetition Penalty    1.0
    stepsprocess.txt, and answer.txt.


E Implementation Details and Hyperparame-                                The successful portion of the run is the segment in which the
  ters                                                                   global status eventually changes to Overall verdict:
                                                                         VERIFIED. Within that segment, the agent’s behavior is best
To ensure full reproducibility of our empirical results, we              understood as a sequence of state transitions over a ledger of
detail the exact execution environment and API parameter                 proof obligations, rather than as a single forward derivation.
configurations utilized for our framework.
                                                                         F.1   Initial Reduction of the Open Proof State

Execution Environment. All experimental evaluations were                 At the beginning of the successful segment, the proof is
conducted within the codex framework (version 0.124.0).                  not globally closed. The agent first strengthens the veri-
We strictly utilized the framework’s default configuration pro-          fication of the real assembly injectivity step, recorded as
file for environmental setup. Beyond this basic scaffolding,             step_15a_real_assembly_injectivity. The key
all complex agentic behaviors, formatting rules, and state-              effect of this move is structural: it eliminates one major up-
machine constraints were injected directly into the GPT-5.4-             stream dependency and reduces the remaining unresolved part
xhigh engine via natural language system prompts. This design            of the proof to the signature-package portion.
avoids overfitting to specialized framework configurations and           The agent then observes that the existing step
explicitly demonstrates the out-of-the-box generalizability of           step_15b1_signature_equals_assembly                          is
our verification approach.                                               too coarse. In its own diagnosis, this step mixes two logically
                                                                         different bridges:

LLM Generation Hyperparameters. To maintain a rigor-                      (i) the assembly/index bridge, namely that the analytic sym-
ously fair comparison, identical generation parameters were                   metric signature is the assembly image of a signature class;
applied to the GPT-5.4-xhigh API calls across all baselines and               and
our agentic pipeline. We deliberately operated at a standard             (ii) the characteristic-class bridge, namely that this signature
temperature of 1.0 to simulate natural generation variance.                   class corresponds rationally to the Poincaré dual of the
The fact that our agent yields deterministic, monotonic conver-               Hirzebruch L-class.
gence under these high-entropy sampling conditions further               Instead of keeping this as one unresolved block, the agent
corroborates the robustness of our prompt-driven constraints.            explicitly resplits it into smaller units:
The complete parameter suite governing the LLM API requests
is summarized in Table 2.                                                 • step_15b1a_signature_class_to_assembly
                                                                          • step_15b1b_signature_class_to_lclass
F    A Worked Trace of a Successful Verification                          • step_15b1c_signature_equals_assembly
     Run for Problem 7b                                                  It also rewires the downstream chain so that each later step
                                                                         depends on the newly separated obligations rather than on one
This appendix records a representative successful verification           monolithic unresolved assertion:
trace for Problem 7b, based on the segment of the execution
log that culminates in a fully verified proof state. The point of               step_15b2_m0_pushforward_formula →
this example is not that the agent generated a correct proof in                     step_15c_lclass_equality →
one shot. Rather, the log shows a staged verification process                          step_16_degree_pm1 →
in which the agent repeatedly refines the proof graph, isolates                     step_17_final_contradiction
unresolved dependencies, revises an incorrect intermediate
diagnosis, and only then closes the remaining steps.                     This resplitting is the first decisive move in the successful run.


                                                                    15
It turns a vague unresolved block into a small dependency                 theorem is used to construct the real KO-homology signature
graph with identifiable root causes.                                      class and to identify its assembly image with the symmetric
                                                                          signature. Once this step is marked VERIFIED, the remain-
F.2   Compression to Two Genuine External Gaps                            ing active dependency set shrinks from {D6b1a, D6b1b} to
After the split, the proof still contains several OPEN steps,             just {D6b1b}.
but the agent recognizes that these are largely downstream
consequences of only two genuine external gaps, recorded in               2. Closing D6b1b. The agent closes this gap by rewriting
the dependency ledger as D6b1a and D6b1b. Informally:                     step_15b1b_signature_class_to_lclass. Here
 • D6b1a: the real KO-theoretic assembly/index bridge.                    the successful move is not simply to cite a missing theorem
 • D6b1b: the real KO-homological L-class bridge.                         verbatim. Instead, the agent builds a local bridge:

This is an important feature of the trace. The raw number of              (1) identify the real signature class in KO-homology;
open files is not itself the right complexity measure. Once               (2) complexify it to the standard complex signature class;
the proof has been resplit correctly, the open graph becomes              (3) invoke the known complex K-homological L-class for-
shallow: many open steps are merely inherited consequences                    mula;
of a very small number of unresolved inputs.                              (4) use rational real/complex comparison to recover the re-
                                                                              quired real KO-homology coordinates.
F.3   An Incorrect Flaw Diagnosis and Its Retraction
                                                                          This is the step at which the open graph finally collapses.
The      run    then     exhibits     a     nontrivial   self-            Once step_15b1b_signature_class_to_lclass
correction.           The     agent     temporarily     marks             is       verified,       the        recombination     step
step_15b1c_signature_equals_assembly                       as             step_15b1c_signature_equals_assembly
FLAWED. The reason given is a purported contradiction with a              also becomes verifiable, since its two incoming components
Rosenberg–Weinberger normalization theorem, which seemed                  are now both closed.
to show that the exact real KO-theoretic formula written in
the step could not hold with coefficient 1 and the Hirzebruch             F.5   Propagation to the Final Contradiction
L-class exactly as written.                                               After the two root dependencies are closed, the rest of the
This is not the final diagnosis. A separate follow-up phase is            proof is discharged by dependency propagation rather than by
launched specifically to determine whether the recorded flaw              new conceptual discoveries.
witness really implies that the original step is false as used.            • step_15b1c_... is verified by recombining the now-
This matters because the verification protocol distinguishes                 verified assembly/index bridge with the L-class bridge.
sharply between:
                                                                           • step_15b2_... is verified by specializing the base
 • a statement that is genuinely false;                                      formula to M0 and X0 .
 • a statement that may still be true, but whose current justifi-          • step_15c_... is verified by using injectivity of the real
   cation is incomplete or misaligned with the cited source.                 assembly map to pull back the signature equality.
Upon re-reading the relevant source, the agent concludes that              • step_16_... is verified by reading off the top-degree
the previous witness targeted the signature-operator transfor-               consequence, namely that D = ±1.
mation sn , whereas the proof step under inspection was using              • step_17_... is finally verified by combining this con-
a symmetric-signature route. Therefore the witness did not                   clusion with the already verified evenness statement for
actually refute the exact as-used inference. The result is a                 D.
rollback from FLAWED to OPEN.                                             (Note: Long file names are abbreviated here for narrative flow,
This retraction is one of the most informative parts of the trace.        while remaining rigorously tracked in the system ledgers.)
It shows that the agent is not merely searching for counterex-            At that point, the global ledger is updated to remaining
amples, but is also checking whether a counterexample hits the            open steps: none              and     Overall verdict:
correct formal target. In other words, the system distinguishes           VERIFIED. The run concludes with a consistency pass over
a failed proof route from a failed theorem statement.                     the step files, the dependency ledger, the process summary,
                                                                          and the final answer file to ensure that no stale OPEN or
F.4   Closure of the Two Remaining Root Dependencies
                                                                          FLAWED status remains.
After retracting the incorrect flaw diagnosis, the agent returns
to the two root gaps.                                                     F.6   Interpretation
                                                                          This trace is useful because it illustrates what a successful
1.           Closing      D6b1a. The          agent    verifies           agentic proof-verification run actually looks like in practice.
step_15b1a_signature_class_to_assembly.                                   It is not a single-pass proof synthesis. Instead, it has four
The successful route here is to replace an indirect complex-K-            characteristic ingredients:
theoretic justification with a more exact real KO-theoretic               Phase 1: State Decomposition: A coarse unresolved claim
source: Rosenberg and Weinberger’s Lipschitz-signature                             is split into minimal logical units.


                                                                     16
Phase 2: Dependency Localization: Many apparent open
         steps are reduced to a very small set of root gaps.
Phase 3: Error Correction: An intermediate FLAWED diag-
         nosis is explicitly re-examined and retracted when
         the witness is found to miss the exact target state-
         ment.
Phase 4: Closure by Propagation: Once the root gaps
         are closed, the remaining steps verify in sequence
         through the dependency graph.
For this reason, the 7B example should not be described as
a case where the agent simply “found the proof.” A more
accurate description is that it executed a ledger-guided verifi-
cation procedure: it refined the proof graph, isolated the true
bottlenecks, corrected a mistaken local refutation, and only
then propagated the repaired information to a fully verified
final contradiction.




                                                                   17
