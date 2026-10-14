                                                                     Theory-Level Autoformalization:
                                                       From Isolated Statements to Unified Formal Knowledge Bases


                                        Marcus J. Min 1 Mike He 2 Zhaoyu Li 3 Zixuan Yi 1 Sharad Malik 2 Aarti Gupta 2 Xujie Si 3 Osbert Bastani 1


                                                                  Abstract
                                             Autoformalization translates informal natural lan-
                                             guage into formal, machine-verifiable languages.
                                             While most work focuses on individual state-
                                             ments, real formalization efforts are inherently
                                             theory-level: they require an entire web of ax-
                                             ioms, definitions, and lemmas before target the-
                                             orems can even be stated. In this position paper,
arXiv:2607.13292v2 [cs.AI] 5 Aug 2026




                                             we argue for theory-level autoformalization: for-
                                             malizing complete theories, including all their
                                             inter-dependencies, as structured libraries. We
                                             examine the significance of this shift, address
                                             alternative views, identify open challenges, and
                                             propose three promising paths forward. Our sur-
                                             vey of autoformalization is available at https:
                                             //github.com/marcusm117/Awesom
                                             e-Autoformalization.                                                 Figure 1. Overview of this position paper. We argue for theory-
                                                                                                                  level autoformalization by examining its significance (Section 2),
                                                                                                                  addressing alternative views (Section 3), identifying open chal-
                                                                                                                  lenges (Section 4), and proposing paths forward (Section 5).
                                        1. Introduction
                                        We define Theory-Level Autoformalization as the task                      mains not yet supported by such libraries, the main work is
                                        of automatically formalizing the entire theoretical context               precisely to construct those missing theoretical contexts.
                                        within a given scope, including axioms, definitions, nota-                The need for this shift is evident from real-world formaliza-
                                        tions, examples, lemmas, theorems, proofs, tactics, and all               tion efforts (Table 1). The Kepler conjecture is a single state-
                                        their inter-dependencies, as a coherent formal library.                   ment, yet its formalization required 11 years of constructing
                                        As depicted in the “Theory-Level Autoformalization                        an entire web of definitions and supporting lemmas (Hales
                                        Tower” (Figure 2), formalizing even a single target theorem               et al., 2015). AI-assisted approaches can largely accelerate
                                        like the Pythagorean theorem requires first constructing mul-             such efforts: the human formalization of the prime num-
                                        tiple layers of axiomatic primitives, derivative definitions,             ber theorem took 1.5 years (Avigad et al., 2006), while the
                                        and proof infrastructure. This contrasts with statement-level             AI-assisted formalization of its quantitative refinement took
                                        autoformalization, which translates individual theorems in                only 3 weeks (Math Inc., 2025a). Theory-level autoformal-
                                        isolation and implicitly relies on formal theoretical contexts            ization is necessary as statements implicitly require that the
                                        like Lean Mathlib (Mathlib Community, 2020). For do-                      surrounding theories are already formalized. Most impor-
                                                                                                                  tantly, transformative new results hinge on new abstractions
                                           1
                                             University of Pennsylvania 2 Princeton University 3 University       that reorganize and compress our entire knowledge base,
                                        of Toronto.      Correspondence to: Marcus J. Min <mar-                   enabling proofs that could not even be formulated.
                                        cmin@seas.upenn.edu>, Mike He <mikehe@princeton.edu>,
                                        Sharad Malik <sharad@princeton.edu>, Aarti Gupta <aar-                    As mapped out in Figure 1, we examine the significance of
                                        tig@cs.princeton.edu>, Xujie Si <six@cs.toronto.edu>, Osbert              theory-level autoformalization (Section 2) and address alter-
                                        Bastani <obastani@seas.upenn.edu>.                                        native views (Section 3). We then identify open challenges
                                        Proceedings of the 43 rd International Conference on Machine              in evaluation, decomposition, low-resource domain-specific
                                        Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026              languages, and multimodal inputs (Section 4), and propose
                                        by the author(s).                                                         paths forward (Section 5).

                                                                                                              1
                                                 Theory-Level Autoformalization

2. Significance: Why Do We Need                                        then checks the semantic alignment with the informal input.
   Theory-Level Autoformalization?                                     Empirically, model performance correlates strongly across
                                                                       mathematics, programming, and other reasoning bench-
2.1. Why Autoformalization?                                            marks (Emberson & Edelman, 2026), suggesting a shared
a. Synthesizing training data for neural theorem provers.              underlying capability. Training-wise, Pang et al. (2025)
Progress in neural theorem proving is tightly dependent on             demonstrates that a math-only initial RL stage with veri-
the availability of large, high-quality formal corpora (Xin            fiable rewards can elicit reasoning behaviors that transfer
et al., 2024; Lin et al., 2025a). Autoformalization is the most        across domains without specialized reward models, yielding
scalable way to synthesize high-quality informal–formal par-           consistent multi-domain gains.
allel data from the vast supply of informal statements and
proofs. It addresses two complementary bottlenecks: (i)
Statement Autoformalization turns natural-language theo-
rems and conjectures into formal declarations, expanding
coverage of interesting or challenging statements that are
not yet formalized; and (ii) Proof Autoformalization turns in-
formal proofs into machine-checkable proof scripts, directly
producing high-quality data for theorem proving.
b. Accelerating theoretical verification and discovery.
Formalization of important theorems and crucial engineer-
ing systems not only enables identifying potential mistakes,
but also facilitates certified extensions and future theoretical
discoveries. Table 1 surveys representative formalization
efforts across 4 domains: mathematics, science, software,
and hardware. The common bottleneck is that these projects
take years, some even decades (Leroy, 2009) of collabora-
tive effort by a team of domain experts. Autoformalization
thus becomes a promising way to accelerate such processes.
c. Grounding and guiding reasoning in natural language.
Natural-language reasoning by LLMs is prone to halluci-
nation and factual inconsistency (Ji et al., 2023). Auto-
formalization improves reliability by translating informal
arguments into formally checkable representations (Yang
et al., 2022; Zhou et al., 2024), which provides two comple-
mentary benefits: (i) Grounding rules out incorrect steps by
finding contradictions, ill-typed definitions, or non-existing
premises. (ii) Guiding provides checker feedback as a guid-
ance signal, enabling self-refinement loops. Autoformaliza-
tion also benefits human informal reasoning, where argu-
ments often omit routine steps, gloss over delicate cases, or
carry unnecessary assumptions (Autexier & Fiedler, 2006).
Autoformalization helps human researchers identify the
handwavy steps and redundant premises, leading to more
rigorous and elegant arguments. Furthermore, autoformal-
ization can lower the barrier to using proof assistants by
letting domain experts work closer to their natural mathe-
matical language, while the autoformalizer handles much of
the formal syntax and bookkeeping (Shulman, 2024).
d. Advancing AI with general reasoning capabilities.
Szegedy (2020) envisions a general reasoning AI system
powered by autoformalization: the autoformalizer gener-
ates candidate formalizations; the reasoner leverages for-             Figure 2. The “Theory-Level Autoformalization Tower” illus-
mal verifiers to keep only correctly proved statements and             trated with the formal SystemE (Avigad et al., 2009) of Euclidean
                                                                       geometry implemented by Murphy et al. (2024) in Lean.

                                                                   2
                                                     Theory-Level Autoformalization

        Table 1. Representative formalization projects across domains, which require substantial time and effort from human experts.

Domain              Formalization Project                                        Verification Tool                         Start    Duration
                                                                                     1
                    Four Color Theorem (Gonthier, 2007)                          Coq (Barras et al., 1997)                 2000       5 years
                    Kepler Conjecture (Hales et al., 2015)                       HOL Light2 (Harrison, 2025)               2003      11 years
Mathematics
                    Odd Order Theorem (Gonthier et al., 2013)                    Coq                                       2006       6 years
                    Liquid Tensor Experiment (Commelin et al., 2022)             Lean                                      2020      1.5 years
                    Chemical Physics (Bobbin et al., 2023)                       Lean                                      2022         1 year
Science
                    Applied PDEs (Deniz, 2024)                                   HOL Light                                 2022        Ongoing
                    CompCert (Leroy, 2009)                                       Coq                                       2005        Ongoing
Software            CertiKOS (Shao & Ford, 2010)                                 Coq                                       2010        Ongoing
                    Vellvm (Zhao et al., 2012)                                   Coq                                       2012        Ongoing
                    ISA-Formal (Reid et al., 2016)                               commercial model checkers                 2011        5 years
Hardware
                    CHERI-MIPS ISA (Nienhuis et al., 2020)                       Isabelle/HOL (Nipkow et al., 2002)        2014        6 years
1
    Coq has been renamed to Rocq since 2025, see https://rocq-prover.org/
2
    HOL Light was the main proof assistant; Isabelle was also used for the classification of tame graphs.

2.2. Why Theory-Level Autoformalization?                                  reduce the dominant cost of expert labor.
As depicted in the “Theory-Level Autoformalization                        b. Statement formalization requires formal theories.
Tower” (Figure 2), to formalize our target theorems with                  Many existing statement autoformalization tasks appear
proofs, we must start from the axiomatic definitions in                   tractable because the heavy lifting is implicitly done by
Layer 0: primitive sorts like Points and primitive re-                    a mature formal environment of proof assistants and stan-
lations like sameSide governed by axioms. Based on the                    dard libraries. Modern proof assistants such as Lean (Moura
primitive definitions, we can construct more complex deriva-              & Ullrich, 2021) provide expressive foundations and power-
tive definitions in Layer 1 that involve inductive types like             ful metaprogramming support, and large human-formalized
Angle and composite relations such as formTriangle                        standard libraries like Mathlib (Mathlib Community, 2020)
that combine multiple primitive notions. On top of the                    already supply a vast collection of definitions, notation, and
definitions, Layer 2 provides the tooling infrastructure: no-             lemmas that can be reused directly. If we want to formalize
tations that make formal statements readable; lemmas and                  statements in areas not well-supported by Mathlib, for ex-
tactics that facilitate subsequent proofs. Only with all these            ample, numerical analysis, then the main work is precisely
layers in place can we state and prove the target theorems                to construct the missing formal theoretical context. Even
in Layer 3. The best current method achieves 71.4% on                     for standard undergraduate mathematics, there are still miss-
statements in Layer 3 (Min et al., 2026), assuming Layers                 ing sub-theories in Lean Mathlib (Lean Community, 2026).
0–2 already formalized by humans. Yet, no current method                  Therefore, extending statement autoformalization to new
even attempts to autoformalize these lower layers.                        domains necessitates theory-level capabilities.
Theory-level autoformalization is, therefore, a systems engi-             c. New theoretical discovery demands new abstractions.
neering endeavor to construct a coherent library of formal                Significant theoretical discoveries i.e. proofs of difficult the-
components that hinge on each other. It is necessary and                  orems typically require new abstractions that refactor and
imminent for the following 3 reasons:                                     compress our representation of knowledge, enabling argu-
                                                                          ments that could not even be stated before. Abstract algebra
a. Real formalization projects are by nature theory-level.
                                                                          introduced groups, rings, and fields that abstract away spe-
The real-world formalization efforts surveyed in Section 2.1,
                                                                          cific structures like the integers or polynomials, focusing on
from the Four Color Theorem to CertiKOS, are not isolated
                                                                          analyzing symmetries. This shift led to Galois’s proof that
statement translations but large-scale formal theory construc-
                                                                          the general quintic cannot be solved by radicals, a result that
tions. The Kepler conjecture is indeed a single statement,
                                                                          depends on recognizing that the symmetric group S5 is not
but it cost 11 years to formalize the entire web of definitions
                                                                          solvable. Category theory abstracted away internal structure
and supporting lemmas from scratch (Hales et al., 2015).
                                                                          to focus on morphisms between objects. Grothendieck’s
Similarly, the Liquid Tensor Experiment required formaliz-
                                                                          invention of étale cohomology (Milne, 2013)—defining a
ing substantial portions of condensed mathematics before
                                                                          richer cohomology theory for algebraic varieties over finite
the target theorem could even be stated (Commelin et al.,
                                                                          fields by replacing the category of open sets with the cate-
2022). Theory-level autoformalization is thus necessary to
                                                                          gory of étale mappings—ultimately enabled Deligne’s proof

                                                                      3
                                                Theory-Level Autoformalization

of the Weil conjectures (Deligne, 1980), resolving the num-           Counterargument. As analyzed in Section 2.1, autofor-
ber theory problem in a geometric way. These examples                 malization has value that extends well beyond training data
illustrate that theoretical progress hinges on the creation of        synthesis: it accelerates verification and discovery, grounds
new abstractions that compress knowledge and unlock more              natural-language reasoning, and advances general AI rea-
general results. After theory-level autoformalization from            soning capabilities. This is especially evident in hardware
all of mathematics, science, and engineering, we will have            verification, where the real bottleneck is formalizing speci-
an enormous codebase of formalized knowledge. Refac-                  fications rather than proving properties, as the latter is typ-
toring this codebase allows us to identify common struc-              ically handled by mature model checking tools. Even in
tures and patterns across various domains, abstract them out,         the context of interactive theorem proving, the prover pre-
compress our knowledge base, and eventually use these new             supposes a formal statement as the goal, but where does
abstractions to prove new results.                                    this statement come from? We do not care about proving
                                                                      arbitrary formal statements, but only the ones that matter to
To conclude, theory-level autoformalization is an inevitable
                                                                      human mathematicians or have significant downstream im-
step toward the vision of an AI system that can automate
                                                                      pact like the correctness of compilers and operating systems.
real-world verification and genuine theoretical discovery.
                                                                      Autoformalization is what produces these statements in the
                                                                      first place, making it the fuel of theorem proving. Moreover,
3. Alternative Views: Why Not Otherwise?                              even when both tasks target proofs, they differ in objective:
                                                                      theorem proving seeks any valid proof, while proof autofor-
3.1. View 1: Informal over Formal Reasoning.
                                                                      malization faithfully translates a specific informal argument
Informal natural-language reasoning has made remarkable               (see Appendix B for detailed discussions).
progress since the release of OpenAI o1 (OpenAI, 2024) and
DeepSeek-R1 (Guo et al., 2025). The IMO 2025 results (Lu-             3.3. View 3: Statement Autoformalization over
ong & Lockhart, 2025; Wei, 2025) further demonstrate that                  Theory-Level Autoformalization.
informal reasoning alone can tackle difficult competition
problems without formal verification. Practically, informal           Statement autoformalization is so far a more tractable prob-
reasoning is also more flexible: it requires no specialized           lem with various benchmarks and evaluation methods. Re-
syntax and is not restricted to domains, thus benefiting from         cent human-AI collaborations (Math Inc., 2025a;b; 2026)
massive training data compared to formal reasoning.                   demonstrate that complicated theorems like the strong prime
                                                                      number theorem can be autoformalized with the following
Counterargument. First, as discussed in Section 2.1, for-             pipeline: human experts first provide a “blueprint”—a well-
mal methods ground and guide informal reasoning for both              decomposed dependency graph of lemmas and definitions—
AI and humans by catching errors and providing verified               and an LLM-based agent follows this blueprint to autofor-
feedback. Second, formal proofs enable modular trustwor-              malize each lemma in topological order, essentially per-
thiness: proofs of difficult theorems are hard to read re-            forming a sequence of statement-level translations. The
gardless of whether they are written in natural or formal             agent then proves the lemmas, optionally guided by infor-
language, but formal proofs can be mechanically checked,              mal proofs. Given these positive signals, one might argue
allowing collaborators to trust each other’s contributions            that statement-level methods should be prioritized.
without inspecting every detail. This empowers large-scale
collaboration among human experts and AI systems. Third,              Counterargument. First, as explained in Section 2.2, state-
informal reasoning scales solely through learning from data,          ment autoformalization implicitly depends on theory-level
which may eventually plateau. In contrast, formal reason-             autoformalization. The strong prime number theorem for-
ing can scale through both learning and search—the only               malization by Math Inc. (2025a) was mostly built upon Lean
two methods that Sutton (2019) identifies to scale reliably           Mathlib, which already contains the foundational theories
with compute. Formal reasoning is thus complementary to               of complex analysis, harmonic analysis, and number theory;
informal reasoning with new results found via search.                 without these formal foundations, the theorem cannot even
                                                                      be stated. For domains not yet supported by mature libraries,
                                                                      theory-level autoformalization is the only path forward. Sec-
3.2. View 2: Theorem Proving over Autoformalization.
                                                                      ond, even for well-supported domains, the human-blueprint
Since the goal is to prove and discover new theorems, the-            approach does not scale. These blueprints are not natu-
orem proving, especially the generation of proof scripts              ral textbook prose, but fine-grained decompositions into
and verification conditions, directly addresses this objective.       minimal easy-to-prove lemmas, written in a style closer to
From this perspective, autoformalization appears secondary            formal language than to informal mathematical exposition.
and is merely one of several ways to synthesize training data         Creating such blueprints still requires substantial time and
for neural-based theorem proving.                                     effort from human experts. Finally, as argued in Section 2.2,
                                                                      theory-level autoformalization enables the discovery of new

                                                                  4
                                               Theory-Level Autoformalization

mathematical abstractions, which are essential tools for tack-       trary relations in other models. Definitional equivalence in
ling the most challenging open conjectures.                          proof assistants like Lean addresses this by unfolding defini-
                                                                     tions via δ-reduction (Bailey, 2025), but still cannot equate
4. Open Challenges: What’s Missing for                               m + 0 with 0 + m. This is because Nat.add is defined
                                                                     by recursion on the second argument: m + 0 reduces to
   Theory-Level Autoformalization                                    m immediately, but 0 + m gets stuck on the abstract vari-
4.1. Challenge 1: Equivalence Checking                               able m. Relating them requires propositional rewriting with
                                                                     lemmas like Nat.add comm, proved by induction.
Equivalence checking is the core of progress in autoformal-
ization: it enables meaningful benchmarking and provides             However, unrestricted propositional equivalence is not
reward signals for training. Yet unlike theorem proving,             sound: any two true statements in the background theory
where the underlying solver or type checker delivers defini-         T become equivalent, making 1 + 1 = 2 equivalent to
tive verdicts, autoformalization not only lacks reliable ora-        Fermat’s Last Theorem. The solution is to restrict the back-
cles, but even the very notion of equivalence is subjective.         ground theory to an admissible fragment. Liu et al. (2025)
                                                                     proposed “Extended Definitional Equivalence,” but their
a. Lack of reliable formal ground truth. Since there is              implementation lacks soundness because an LLM generates
no sound automated way to directly check semantic equiv-             the equivalence proof, with restrictions only on allowed
alence between a generated formalization and its informal            tactics rather than the background theory itself. Poiroux
input, reliable evaluation requires comparing against human-         et al. (2025) implemented a deterministic checker (BEq+)
written formal ground truth. However, existing statement             that forbids global context and proof search, permitting only
autoformalization benchmarks contain substantial errors.             computational automation tactics like simp all arith!,
For example, Poiroux et al. (2025) identified and corrected          and noncomm ring. This achieves 98.0% precision and
118 human formalization mistakes in ProofNet (Azerbayev              48.3% recall, compared to 100% precision and 30.9% re-
et al., 2023), a 31.8% error rate among its 371 problems.            call for pure definitional equivalence. However, false pos-
For another, at least 58 errors have been found and fixed            itives remain possible when both statements are indepen-
in PutnamBench (Tsoukalas et al., 2024) since its publi-             dently easy-to-prove, such as n * 1 = n and n + 0 =
cation in November 2024, an 8.6% error rate among 672                n: since both are provably true by these tactics, the bi-
Lean formalizations. For definition formalization, the only          conditional n * 1 = n ↔ n + 0 = n can be proved
dedicated benchmark is proposed by Zhang et al. (2025a),             despite them being fundamentally different properties.
consisting of just 56 definitions from Wikipedia and 30 from
arXiv papers. For proof autoformalization, the only dedi-            c. The notion of formal-formal equivalence is subjective.
cated benchmark and metric is ProofFlowBench with Proof-             The fundamental bottleneck that has been overlooked in
Score (Cabral et al., 2025), containing 184 undergraduate-           previous autoformalization literature is that even for two for-
level statements with proofs. For theory-level autoformal-           mal statements, equivalence is inherently subjective. What
ization, no benchmarks currently exist yet.                          counts as “equivalent” depends on how much implicit com-
                                                                     putation the evaluator performs automatically.
b. No checker with soundness and practical coverage.                                                      R1
Even with reliable ground truth, there exists no checker             Consider a ground truth statement 0 2x3 ln(x2 +1) dx > 0
                                                                                       R1
that is both sound and has a high coverage of non-trivial            and a prediction 0 2x3 ln(1 + x2 ) dx > 0. To most readers,
equivalence cases. Most autoformalization evaluations rely           these appear identical because applying commutativity of
on LLM-as-a-judge: backtranslating the formalization to              addition is so effortless that it happens unconsciously. But
informal and comparing it with the input informal using              what if the prediction is instead 14 > 0? Most would judge
LLMs (Ying et al., 2025; Gao et al., 2025), training embed-          this as inequivalent, yet the integral does evaluate to exactly
ding models to predict similarity scores (Lu et al., 2024), or        1
                                                                      4 . For an expert who can perform this integration mentally,
building LLM-based scorer agents that evaluate component-            the two statements may seem just as obviously equivalent.
wise consistency (Xuejun et al., 2025; Wang et al., 2025b).          This subjectivity becomes even more apparent in boundary
                                                                                               R1
These methods provide no soundness guarantee.                        cases. The statement 0 2x3 ln[(x − 1)2 + 2x] dx > 0
Sound alternatives exist but are overly restrictive. Exact           is mathematically equivalent to the ground truth because
match cannot handle semantically equivalent transforma-              (x − 1)2 + 2x = x2 + 1. To someone fluent in algebraic
tions: ∀n : N, P (n) and ¬∃n : N, ¬P (n) are logically               manipulation, recognizing this identity is immediate; to
equivalent but syntactically different. Logical equivalence          others, it requires explicit expansion and simplification.
handles such cases but fails when background theory knowl-           The perceived “degree of equivalence” thus varies with the
edge is required: rectangle(a) ∧ rhombus(a) and                      evaluator’s background knowledge and computational flu-
square(a) are equivalent in Euclidean geometry but not               ency. Any equivalence checker must choose a threshold
logically equivalent, since they can be interpreted as arbi-

                                                                 5
                                               Theory-Level Autoformalization

for how much computation and reasoning to permit, and                However, these methods remain insufficient for theory-level
different such thresholds yield different judgments about            blueprint generation. The problems they handle are only
what constitutes a correct formalization.                            high school mathematics with shallow dependency graphs,
                                                                     and they decompose only one proof or statement at a time.
4.2. Challenge 2: Hierarchical Decomposition and                     Blueprint generation, by contrast, requires decomposing en-
     Abstraction Learning                                            tire textbooks into coherent dependency graphs with dozens
                                                                     of major theorems and deeply intertwined dependencies.
As discussed in Section 3.3, recent human-AI collabora-
tions (Math Inc., 2025a;b; 2026) have formalized substan-            b. Abstraction Learning. The goal is to discover reusable
tial theorems by following human-written blueprints. We              patterns from data that can be applied to new tasks. In pro-
consider these efforts “Semi-Theory-Level Autoformaliza-             gram synthesis, library learning identifies common subrou-
tion” because 2 critical gaps remain: (i) Hierarchical De-           tines across program corpora (Ellis et al., 2021; Wang et al.,
composition: blueprints are fine-grained dependency graphs           2024b). In theorem proving, systems build libraries of lem-
of minimal lemmas, not natural prose—creating them still             mas that streamline future proofs (Zhou et al., 2022; Wang
requires significant expert effort. (ii) Abstraction Learning:       et al., 2023). In LLM reasoning, tool learning allows mod-
these projects rely on Mathlib for definitions; for domains          els to construct reusable utilities for specific domains (Yuan
without mature libraries, definition autoformalization re-           et al., 2024; Qu et al., 2025). In autoformalization, the goal
mains unexplored and underrepresented in training data.              is to curate libraries of reusable mathematical definitions.
                                                                     Patel et al. (2024) first proposed the concept of definition
a. Hierarchical Decomposition. In neural theorem prov-               formalization so that they can be reused when formalizing
ing, decomposition has proven effective for breaking proof           theorems, and Zhang et al. (2024) first experimented with
goals into manageable subgoals. Early work explored dif-             the autoformalization of definitions extracted from IsarMath-
ferent decomposition strategies: LEGO-Prover (Wang et al.,           Lib (Kolodynski, 2019). Def Wiki and Def ArXiv (Zhang
2023) builds a growing library of reusable lemmas during             et al., 2025a) are the only dedicated definition formalization
proof search, Zhao et al. (2023) use diffusion models to             benchmarks so far with 56 and 30 definitions respectively.
select subgoal demonstrations, and POETRY (Wang et al.,
2024a) outlines proof structure with placeholders before re-         DNA (Min et al., 2026) is the first to apply abstraction learn-
cursively filling in subgoals. The latest systems have scaled        ing to statement autoformalization by extracting common
these ideas successfully. DeepSeek-Prover-V2 (Ren et al.,            concepts across a corpus, constructing a dependency graph
2025) uses reinforcement learning to train LLMs to do de-            of these concepts, and formalizing them as reusable defini-
composition, achieving 88.9% on miniF2F (Zheng et al.,               tions. Nonetheless, this framework handles only composite
2022). BFS-Prover-V2 (Xin et al., 2025) uses a planner               definitions of mathematical relations, which are built upon
agent for decomposition with multiple prover agents col-             other lower-level definitions already present in the library.
laborating via a shared proof cache, reaching 95.1% on               No existing work addresses axiomatic definitions or algo-
miniF2F. Hilbert (Varambally et al., 2025) combines a spe-           rithmic definitions. In general, both the scale and the scope
cialized prover with a general reasoning model, recursively          of current abstraction learning benchmarks and methods fall
decomposing into subgoals when both direct attempts fail,            well short of what theory-level autoformalization demands.
and tries them on the new subgoals until success.                    Abstraction learning serves 2 roles in theory-level autofor-
For statement autoformalization, decomposition has only              malization. (i) Definition Formalization: extracting and
begun to receive attention since 2025. Xuejun et al. (2025)          formalizing reusable definitions directly tackles derivative
first use decomposition for evaluation: an LLM judge de-             definitions in the Theory-Level Autoformalization Tower
composes both the informal statement and the predicted               (Figure 2). (ii) Knowledge Compression: as discussed in
formalization into premises and conclusions, then assesses           Section 2.2, significant discoveries rely on inventing new
their semantic alignment. DRIFT (Zhang et al., 2025b)                abstractions that refactor existing knowledge into more com-
decomposes informal statements into sub-queries, each pair-          pact representations, enabling results that could not be stated
ing a natural language phrase with a predicted formal rep-           before. The 2 roles correspond to complementary method-
resentation to guide dependency retrieval from Mathlib.              ologies: (i) Agent-driven, where an LLM summarizes recur-
Aria (Wang et al., 2025b) decomposes the informal state-             ring concepts from an informal corpus (Min et al., 2026),
ment into a dependency graph of concepts, and formalizes             are well-suited for definition formalization since no for-
each node bottom-up from leaf nodes grounded in Mathlib.             mal corpus yet exists for symbolic methods to operate on,
DNA (Min et al., 2026) recursively decomposes the informal           and mathematical concepts in natural language are already
statement into a nested structure of quantifiers, premises,          highly abstracted. (ii) Symbolic (Ellis et al., 2021; Zhou
and conclusions until each leaf is an atomic proposition,            et al., 2022), which identify common structures by analyz-
then translates and composes the formal outputs.                     ing a formal corpus directly, are a natural fit for knowledge


                                                                 6
                                                Theory-Level Autoformalization

compression once a formal library is available: they make
the library more compact and modular, revealing hidden
connections between seemingly distant domains.

4.3. Challenge 3: Beyond Lean - Real-World
     Applications Using Low-Resource DSLs
Real-world applications of autoformalization span domains
that use specialized, low-resource DSLs: from SMT-LIB
for constraint solving to Cedar for access control policies.
Organizations frequently adopt niche or even create private
DSLs tailored to their specific verification needs. While
formal codebases may exist in isolation, these DSLs lack
the large paired informal–formal corpora that Lean enjoys,            Figure 4. Informal-to-formal translation of a leader election proto-
making them difficult for data-driven approaches.                     col (Chang & Roberts, 1979).

                                                                      b. Protocol Verification Languages. Verification of dis-
                                                                      tributed protocols provides formal guarantees that a protocol
                                                                      design satisfies safety properties (e.g., mutual exclusion),
                                                                      by proving these properties hold across all reachable states.
                                                                      State-of-the-art techniques take as input the protocol de-
                                                                      sign written in domain-specific modeling languages such as
                                                                      Ivy (Padon et al., 2016) and PVerifier (Mora et al., 2023),
                                                                      along with inductive invariants that imply safety properties.
Figure 3. Informal-to-formal translation example (ATP). For-
mal statements are extracted from the Tons of Inductive Prob-         Autoformalization for this domain faces similar challenges.
lems (Claessen et al., 2015) benchmark.                               First, the domain is inherently low-resource: the number of
                                                                      widely-studied distributed protocols is small compared to
                                                                      mathematical theorems (Mathlib Community, 2020). The
a. Automated Theorem Prover (ATP) Languages. Au-
                                                                      most comprehensive benchmark to date, IvyBench (Goel
tomated theorem provers operate over DSLs for encoding
                                                                      & Sakallah, 2020), contains only 54 formalized proofs of
logical constraints. SMT solvers accept specifications in
                                                                      protocols. Second, formalization demands extensive do-
SMT-LIB (Barrett et al., 2010), while first-order theorem
                                                                      main knowledge about background theories. For example,
provers such as E Prover (Schulz, 2002) and Vampire (Ri-
                                                                      Figure 4 shows an informal-to-formal translation of the
azanov & Voronkov, 1999) use TPTP syntax (Sutcliffe,
                                                                      Chang-Roberts leader election protocol (Chang & Roberts,
2024). These tools have achieved remarkable success in
                                                                      1979). In this example, the ring topology and initial states
competitions such as SMT-COMP (Barrett et al., 2005) and
                                                                      are encoded logically with axioms, and the formal model
CASC (Sutcliffe, 2016). Figure 3 illustrates formalizing
                                                                      references atomic predicates introduced in this encoding.
an informal proof objective into SMT-LIB. The informal
                                                                      Theory-level datasets are needed to train LLMs on encoding
statement describes a property of the drop(x, L) function:
                                                                      such domain knowledge.
∀x, w, L. drop(w, drop(x, L)) = drop(x + w, L).
                                                                      c. Hardware Verification Languages. Hardware security
Autoformalization for this domain faces two key challenges.
                                                                      and correctness rely on formal verification to ensure de-
First, existing benchmarks (Claessen et al., 2015; Barrett
                                                                      signs behave as intended before fabrication. Engineers must
et al., 2005; Sutcliffe, 2016) contain only formal specifica-
                                                                      translate informal design documents into formal verification
tions without natural language descriptions—for instance,
                                                                      languages such as SystemVerilog Assertions (SVAs), which
the Tons of Inductive Problems benchmark (Claessen et al.,
                                                                      express temporal properties over signal behaviors. This
2015) provides the formal statements in Figure 3 but no
                                                                      translation is labor-intensive, making it a natural candidate
informal counterpart. Second, informal statements may ref-
                                                                      for autoformalization.
erence multiple theories (e.g., integers and lists in Figure 3)
without explicit context, requiring theory-level formaliza-           However, while datasets of hardware designs in Verilog ex-
tion to identify necessary axioms and lemmas (e.g., com-              ist (Thakur et al., 2024), designs with formal specifications
mutativity of addition). In general, the scarcity of aligned          remain scarce. Moreover, formalization is inherently chal-
natural–formal specification pairs and theory-level formal-           lenging because design documents may combine natural
ization datasets remains an open challenge in the autofor-            language and timing diagrams, each containing ambigu-
malization of ATP languages.                                          ity and implicit assumptions/assertions. For example, in

                                                                  7
                                                  Theory-Level Autoformalization




                                                                         Figure 6. Informal-to-formal translation example of Cedar policy
Figure 5. Informal-to-formal translation example from Shih et al..       that implements clauses in HIPAA regulations.
The protocol is from the AMBA AXI specifications (Arm, 2004).

                                                                         feedback and retrieval-augmented generation, the success
Figure 5, the property stated informally as control informa-             rate is only 53.4%.
tion from the source remains stable implicitly asserts that
it holds starting from the next cycle (captured by the ##1               Cedar, Amazon’s policy language for authorization (Cutler
operator in the SVA), which becomes apparent only when                   et al., 2024), presents a different challenge: the informal
cross-referencing the timing diagram with the text.                      inputs are enormous. Real-world policy documents like
                                                                         HIPAA regulations (U.S. Department of Health and Human
Accurate formalization thus requires cross-modal reasoning               Services, 2024) span hundreds of pages of legal prose with
to resolve inconsistencies and surface hidden assumptions.               nested conditions, exceptions, and cross-references. For
Developing autoformalization techniques capable of such                  example, Figure 6 shows how three separate HIPAA clauses
multi-modal reasoning for articulating formal properties                 about individual access rights, personal representatives, and
remains an essential yet largely unaddressed challenge.                  minors must be jointly formalized into Cedar policies that
d. Declarative Programming Languages. Declarative                        correctly encode their interactions through shared predicates
languages like SQL, Cypher, CodeQL, and Cedar let users                  like to patient and state rep access allowed.
specify what they want while delegating how to compute it                While researchers have attempted to formalize fragments
to an execution engine. Unlike imperative languages, declar-             of such documents into Cedar, no complete large-scale pol-
ative program synthesis is a semantics-preserving translation            icy corpus has been fully formalized. The gap between
from informal intent to formal, which is in the scope of aut-            paragraph-level demonstrations and document-level formal-
oformalization (see Appendix A for detailed discussions).                ization remains vast, requiring theory-level autoformaliza-
We highlight 3 representative cases:                                     tion that can maintain consistency across thousands of inter-
                                                                         dependent policy rules.
Cypher, the query language for graph databases like Neo4j,
exemplifies low-resource DSL challenges. The Text2Cypher
                                                                         4.4. Challenge 4: Beyond Text - Real-World
benchmark (Ozsoy et al., 2025) provides 44,387 natural
                                                                              Applications Requiring Multimodal Inputs
language–query pairs, yet LLM performance remains mod-
est: GPT-4o achieves only 33% exact match accuracy, im-                  Real-world formalization tasks often involve multimodal
proving marginally from 31% without fine-tuning. The                     inputs. We identify four main modalities: (i) Natural Lan-
difficulty stems from compositional semantics that require               guage, including descriptions and documentation; (ii) For-
multi-hop reasoning over graph structures—patterns rarely                mal Languages, such as mathematical notation or existing
seen in pretraining data and highly dependent on schema-                 specifications; (iii) Structured Diagrams, including timing
specific knowledge that varies across deployments.                       diagrams, schematics, and flowcharts; and (iv) Free-Form
                                                                         Images, such as geometric figures and UI mockups. These
CodeQL, GitHub’s query language for static security analy-
                                                                         scenarios demand systems that reason across modalities, a
sis, illustrates yet another dimension of difficulty: the appli-
                                                                         capability current text-centric approaches lack.
cation requires dual expertise in security vulnerabilities and
program analysis. As shown by Wang et al. (2025a), synthe-               In geometry, spatial relationships like betweenness and inter-
sizing CodeQL queries from CVE descriptions is extremely                 section are naturally conveyed by diagrams but cumbersome
challenging—Claude Code achieves only a 10% success                      to express in text. Similarly, hardware timing diagrams and
rate when generating queries that correctly detect vulnera-              protocol state machines are primary carriers of formal con-
bilities in 176 CVEs across 111 Java projects. Even with                 tent with implicit semantics (e.g., “starting from the next cy-
sophisticated agentic scaffolding including language server              cle”) that must be parsed and integrated with textual descrip-

                                                                     8
                                                 Theory-Level Autoformalization

                                                                       5.2. Proposal 2: General-Purpose Models over
                                                                            Fine-Tuned Specialists
                                                                       Specialized fine-tuned models suffer from severe overfitting:
                                                                       Goedel-Formalizer-V2-32B (Lin et al., 2025b) scores 0.0%
                                                                       on LeanEuclidPlus (a Lean benchmark outside Mathlib),
                                                                       while its base model Qwen3-32B achieves 20.6%—a pat-
                                                                       tern observed across all fine-tuned autoformalizers (Min
                                                                       et al., 2026). We therefore advocate building on general-
                                                                       purpose LLMs, enhanced through general training tech-
                                                                       niques like iterative SFT (Ying et al., 2025) and reinforce-
                                                                       ment learning with verifier feedback (Huang et al., 2025),
                                                                       combined with inference-time methods such as dependency
Figure 7. Our 3 proposals for theory-level autoformalization: a        retrieval (Zhang et al., 2025b; Wang et al., 2025b) and veri-
common intermediate representation, general-purpose LLM agents,
and benchmarks with sound equivalence checking.
                                                                       fier feedback loops (Poiroux et al., 2025; Min et al., 2026).
                                                                       This approach transfers across DSLs and automatically ben-
                                                                       efits from foundation model improvements.
                                                                       To be precise, this proposal is not about the training tech-
                                                                       niques themselves—SFT, RLVR, and test-time scaling are
tions through cross-modal reasoning. Finally, formalization            all standard—but about the Data Mixture, Reward Design,
sometimes requires translation between formal languages                and Evaluation Scope. By “general-purpose,” we mean
(e.g., Coq to Lean), which is non-trivial due to differing             models trained on diverse formal corpora spanning multiple
foundational assumptions and tactic ecosystems (Stoskopf               domains and DSLs, with rewards that do not overfit to a
et al., 2025), and motivates the common intermediate repre-            single library’s conventions, and evaluated on benchmarks
sentation we propose in Section 5.3.                                   including real-world textbooks and important proofs beyond
                                                                       standard competition mathematics.
5. Call to Action: Proposals for Advancing
                                                                       5.3. Proposal 3: A Common Intermediate
   Theory-Level Autoformalization                                           Representation for Theoretical Discovery
5.1. Proposal 1: Theory-Level Benchmarks with Sound                    A common intermediate representation (IR) can address
     Equivalence Checking                                              multiple challenges simultaneously. First, as depicted in
Existing benchmarks only evaluate definitions, statements,             Figure 7, the IR provides a unified target for formalizing
and proofs in isolation. We need benchmarks that evaluate              multimodal inputs, enabling a complete and coherent speci-
entire theories as unified artifacts, including controlled tests       fication even when the source materials are heterogeneous.
of decomposition and abstraction learning (Section 4.2).               Second, as discussed in Section 4.3, our target DSLs include
Concretely, an ideal theory-level benchmark should satisfy             low-resource, evolving, and proprietary languages; training
3 criteria: (i) it should include formalization of background          LLMs to master each one individually is impractical. An IR
theories, not just isolated statements; (ii) it should use sound       reduces this combinatorial problem to a linear one. Third, a
equivalence checking with reported precision and recall                general IR combines the theorem-proving strengths of itself
compared against expert judgments (Section 4.1); and (iii)             and the target DSLs: the DSLs often integrate tightly with
it should enforce data leakage prevention to ensure the back-          specialized symbolic Automated Theorem Proving (ATP)
ground theories are not already in the model’s training data.          tools, while the IR benefits from richer training data and
                                                                       thus LLM-automated Interactive Theorem Proving (ITP).
We propose the following priority ordering for measuring
progress. Immediate: theory-level benchmarks satisfying                The design of such an IR is subject to 3 constraints: Expres-
the above criteria. Near-Term: end-to-end case studies mea-            siveness (represent diverse DSL semantics), Verifiability
suring the time and expert effort to formalize a new theory            (type checking and proof verification within the IR), and
with AI assistance versus without; additionally, the commu-            Embeddability (deep embeddings of target DSLs for verified
nity should maintain a tracking table of autoformalization             transpilation). Lean is a natural candidate: its dependent
performance across the DSLs surveyed in Section 4.3, so                type theory provides expressiveness, its built-in type checker
that progress in each domain can be monitored and com-                 provides verifiability, and its metaprogramming facilities
pared over time. Longer-Term: evaluating whether a com-                enable DSL-specific embeddings for verified transpilation
mon IR-based approach (Section 5.3) offers genuine advan-              within a single framework.
tages over direct formalization.

                                                                   9
                                              Theory-Level Autoformalization

6. Conclusion                                                       Bailey, C. Type checking in Lean 4. Online tutorial, 2025.
                                                                      URL https://ammkrn.github.io/type_ch
We have argued that autoformalization must move beyond                ecking_in_lean4/.
isolated statements to formalize entire theories as holistic
formal knowledge bases. We identified open challenges and           Barras, B., Boutin, S., Cornes, C., Courant, J., Filliâtre,
proposed paths forward, aiming to turn autoformalization              J.-C., Giménez, E., Herbelin, H., Huet, G., Muñoz, C.,
from a per-statement demonstration into a scalable tool for           Murthy, C., Parent, C., Paulin-Mohring, C., Saı̈bi, A., and
real-world verification and theoretical discovery.                    Werner, B. The Coq Proof Assistant Reference Manual
                                                                      : Version 6.1. Research Report RT-0203, INRIA, May
Acknowledgement                                                       1997. URL https://inria.hal.science/in
                                                                      ria-00069968. Projet COQ.
We would like to thank Noopur Bhatt, Yu-An Shih, Isil Dil-
lig, and Ziyang Li for valuable discussions. We also thank          Barrett, C., De Moura, L., and Stump, A. Smt-comp: Sat-
the anonymous reviewers for their constructive feedback.              isfiability modulo theories competition. In International
                                                                      Conference on Computer Aided Verification, pp. 20–23.
Marcus J. Min and Zixuan Yi are each supported by an                  Springer, 2005.
AWS ASSET Ph.D. Fellowship. Mike He, Sharad Malik,
and Aarti Gupta are supported by NSF Award CCF-2422053.             Barrett, C., Stump, A., Tinelli, C., et al. The smt-lib stan-
Zhaoyu Li and Xujie Si are supported by the ProML project,            dard: Version 2.0. In Proceedings of the 8th international
funded by the Canadian Natural Sciences and Engineering               workshop on satisfiability modulo theories (Edinburgh,
Research Council and the French National Research Agency,             UK), volume 13, pp. 14, 2010.
under the reference ANR-25-CE23-6715. Osbert Bastani is
supported by NSF Award CCF-2338777, Amazon Research                 Bobbin, M. P., Sharlin, S., Feyzishendi, P., Dang, A. H.,
Award Fall 2023, Amazon/ASSET Gift for Research in                    Wraback, C. M., and Josephson, T. R. Formalizing chem-
Trustworthy AI.                                                       ical physics using the lean theorem prover, 2023. URL
                                                                      https://arxiv.org/abs/2210.12150.
Any opinions, findings, conclusions, or recommendations
expressed herein are those of the authors and do not neces-         Cabral, R., Do, T. M., Yu, X., Tai, W. M., Feng, Z., and
sarily reflect the views of funding entities.                         Shen, X. Proofflow: A dependency graph approach to
                                                                      faithful proof autoformalization, 2025. URL https:
                                                                      //arxiv.org/abs/2510.15981.
References
Arm. Amba axi protocol specification, 2004. URL https:              Chang, E. and Roberts, R. An improved algorithm for
  //developer.arm.com/documentation/ih                                decentralized extrema-finding in circular configurations
  i0022/b/.                                                           of processes. Communications of the ACM, 22(5):281–
                                                                      283, 1979.
Autexier, S. and Fiedler, A. Textbook proofs meet formal
                                                                    Claessen, K., Johansson, M., Rosén, D., and Smallbone,
  logic – the problem of underspecification and granularity.
                                                                      N. Tip: Tons of inductive problems. In Kerber, M.,
  In Kohlhase, M. (ed.), Mathematical Knowledge Man-
                                                                      Carette, J., Kaliszyk, C., Rabe, F., and Sorge, V. (eds.),
  agement, pp. 96–110, Berlin, Heidelberg, 2006. Springer
                                                                      Intelligent Computer Mathematics, pp. 333–337, Cham,
  Berlin Heidelberg. ISBN 978-3-540-31431-8.
                                                                      2015. Springer International Publishing. ISBN 978-3-
                                                                      319-20615-8.
Avigad, J., Donnelly, K., Gray, D., and Raff, P. A formally
  verified proof of the prime number theorem, 2006. URL             Commelin, J., Topaz, A., Buzzard, K., Nuccio, F. A. E.,
  https://arxiv.org/abs/cs/0509025.                                   Brasca, R., et al. Liquid tensor experiment. GitHub
                                                                      repository, 2022. URL https://github.com/lea
Avigad, J., Dean, E., and Mumma, J. A formal system                   nprover-community/lean-liquid.
  for Euclid’s Elements. The Review of Symbolic Logic,
  2(4):700–768, December 2009. ISSN 1755-0211. doi:                 Cutler, J. W., Disselkoen, C., Eline, A., He, S., Headley,
  10.1017/s1755020309990098. URL http://dx.doi                        K., Hicks, M., Hietala, K., Ioannidis, E., Kastner, J.,
  .org/10.1017/S1755020309990098.                                     Mamat, A., McAdams, D., McCutchen, M., Rungta, N.,
                                                                      Torlak, E., and Wells, A. M. Cedar: A new language for
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,          expressive, fast, safe, and analyzable authorization. Proc.
  Radev, D., and Avigad, J. ProofNet: Autoformalizing and             ACM Program. Lang., 8(OOPSLA1), April 2024. doi:
  formally proving undergraduate-level mathematics, 2023.            10.1145/3649835. URL https://doi.org/10.1
  URL https://arxiv.org/abs/2302.12433.                               145/3649835.

                                                               10
                                             Theory-Level Autoformalization

Deligne, P. La conjecture de weil. ii. Publications                Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q.,
 Mathématiques de l’Institut des Hautes Études Scien-             Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu,
  tifiques, 52(1):137–252, Dec 1980. ISSN 1618-1913. doi:           Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A.,
 10.1007/BF02684780. URL https://doi.org/10                         Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C.,
  .1007/BF02684780.                                                  Deng, C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin,
                                                                     F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H.,
Deniz, E. Formalization of Partial Differential Equations           Xu, H., Ding, H., Gao, H., Qu, H., Li, H., Guo, J., Li,
  using HOL Theorem Proving. PhD thesis, Concordia                  J., Chen, J., Yuan, J., Tu, J., Qiu, J., Li, J., Cai, J. L., Ni,
  University, September 2024. URL https://spectr                    J., Liang, J., Chen, J., Dong, K., Hu, K., You, K., Gao,
  um.library.concordia.ca/id/eprint/99                               K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,
  4873/. Unpublished.                                                Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,
                                                                     M., Zhang, M., Tang, M., Zhou, M., Li, M., Wang, M.,
Ellis, K., Wong, C., Nye, M., Sablé-Meyer, M., Morales,             Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen,
  L., Hewitt, L., Cary, L., Solar-Lezama, A., and Tenen-             Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R., Chen,
  baum, J. B. DreamCoder: bootstrapping inductive pro-               R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye,
  gram synthesis with wake-sleep library learning. In Pro-           S., Wang, S., Yu, S., Zhou, S., Pan, S., Li, S. S., Zhou, S.,
  ceedings of the 42nd ACM SIGPLAN International Con-               Wu, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Liu,
  ference on Programming Language Design and Imple-                 W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L.,
  mentation, PLDI 2021, pp. 835–850, New York, NY,                  An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X.,
  USA, 2021. Association for Computing Machinery. ISBN               Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su, X., Lin, X.,
  9781450383912. doi: 10.1145/3453483.3454080.                       Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X.,
                                                                     Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K., Wang,
Emberson, L. and Edelman, Y. Benchmark scores are well              Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun,
 correlated, even across domains, 2026. URL https:                  Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y.,
 //epoch.ai/data-insights/benchmark-c                                Piao, Y., Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou,
 orrelations. Accessed: 2026-01-26.                                 Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo,
                                                                    Y., You, Y., Liu, Y., Zhou, Y., Zhu, Y. X., Huang, Y., Li,
Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and         Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y.,
  Dong, B. Herald: A natural language annotated Lean 4               Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang,
  dataset. In The Thirteenth International Conference on             Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu,
  Learning Representations, 2025. URL https://open                   Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu,
  review.net/forum?id=Se6MgCtRhz.                                    Z., Zhang, Z., and Zhang, Z. Deepseek-r1 incentivizes
                                                                     reasoning in llms through reinforcement learning. Nature,
Goel, A. and Sakallah, K. A. Collection of distributed
                                                                     645(8081):633–638, September 2025. ISSN 1476-4687.
  protocol verification problems. https://github.c
                                                                     doi: 10.1038/s41586-025-09422-z. URL http://dx
  om/aman-goel/ivybench, 2020.
                                                                     .doi.org/10.1038/s41586-025-09422-z.
Gonthier, G. The four colour theorem: Engineering of a             Hales, T., Adams, M., Bauer, G., Dang, D. T., Harrison,
  formal proof. In Computer Mathematics: 8th Asian Sym-              J., Hoang, T. L., Kaliszyk, C., Magron, V., McLaughlin,
  posium, ASCM 2007, Singapore, December 15-17, 2007.                S., Nguyen, T. T., Nguyen, T. Q., Nipkow, T., Obua, S.,
 Revised and Invited Papers, pp. 333, Berlin, Heidelberg,            Pleso, J., Rute, J., Solovyev, A., Ta, A. H. T., Tran, T. N.,
  2007. Springer-Verlag. ISBN 978-3-540-87826-1. doi:                Trieu, D. T., Urban, J., Vu, K. K., and Zumkeller, R.
 10.1007/978-3-540-87827-8 28. URL https://doi.                      A formal proof of the Kepler conjecture, 2015. URL
  org/10.1007/978-3-540-87827-8_28.                                  https://arxiv.org/abs/1501.02155.
Gonthier, G., Asperti, A., Avigad, J., Bertot, Y., Cohen,          Harrison, J. The HOL Light System Reference, 2025. URL
  C., Garillot, F., Le Roux, S., Mahboubi, A., O’Connor,             https://hol-light.github.io/reference
  R., Biha, S. O., Pasca, I., Rideau, L., Solovyev, A.,              s/reference.pdf. Revision of 17th March 2025.
 Tassi, E., and Théry, L. A machine-checked proof of
  the odd order theorem. In Proceedings of the 4th In-             Hu, X., Zhou, Q., Grechuk, B., and Tyukin, I. Y. StepProof:
  ternational Conference on Interactive Theorem Proving,             Step-by-step verification of natural language mathemati-
  ITP’13, pp. 163–179, Berlin, Heidelberg, 2013. Springer-           cal proofs, 2025. URL https://arxiv.org/abs/
 Verlag. ISBN 9783642396335. doi: 10.1007/978-3-642                  2506.10558.
 -39634-2 14. URL https://doi.org/10.1007/
  978-3-642-39634-2_14.                                            Huang, Y., Jin, X., Liang, S., Li, P., and Liu, Y. Formarl:

                                                              11
                                                 Theory-Level Autoformalization

  Enhancing autoformalization with no labeled data, 2025.               Lu, J., Wan, Y., Huang, Y., Xiong, J., Liu, Z., and Guo,
  URL https://arxiv.org/abs/2508.18914.                                   Z. Formalalign: Automated alignment evaluation for
                                                                          autoformalization, 2024. URL https://arxiv.or
Jana, P., Kale, K., Tanriverdi, A. E., Song, C., Vishwanath,              g/abs/2410.10135.
  S., and Ganesh, V. Proofbridge: Auto-formalization of
  natural language proofs in lean via joint embeddings,                 Luong, T. and Lockhart, E. Advanced version of gemini
  2025. URL https://arxiv.org/abs/2510.1                                  with deep think officially achieves gold-medal standard at
  5681.                                                                   the international mathematical olympiad. Google Deep-
                                                                          Mind Blog, 2025. URL https://deepmind.goo
Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii,              gle/blog/advanced-version-of-gemini-w
   E., Bang, Y. J., Madotto, A., and Fung, P. Survey                      ith-deep-think-officially-achieves-g
   of hallucination in natural language generation. ACM                   old-medal-standard-at-the-internation
   Computing Surveys, 55(12):1–38, March 2023. ISSN                       al-mathematical-olympiad/. July 21, 2025.
   1557-7341. doi: 10.1145/3571730. URL http:                             Gemini Deep Think solved 5 of 6 IMO 2025 problems
   //dx.doi.org/10.1145/3571730.                                          (35/42 points) in natural language within the competition
                                                                          time limit.
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,
   M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,               Math Inc. The strong prime number theorem. GitHub repos-
   and prove: Guiding formal theorem provers with informal               itory, 2025a. URL https://github.com/mat
   proofs, 2023. URL https://arxiv.org/abs/22                            h-inc/strongpnt. This repository contains an AI-
   10.12283.                                                             generated Lean formalization of the strong Prime Number
                                                                         Theorem (PNT) and the complex-analysis infrastructure
Kolodynski, S. IsarMathLib, 2019. URL https://gith
                                                                         used in its proof.
  ub.com/SKolodynski/IsarMathLib. Accessed:
  2026-01-28.                                                           Math Inc. Certifying the fri protocol. GitHub repository,
                                                                         2025b. URL https://github.com/math-inc
Lean Community. Missing undergraduate mathematics in
                                                                         /ZkLinalg. An AI-assisted Lean 4 formalization of the
  mathlib. https://leanprover-community.g
                                                                         Fast Reed–Solomon Interactive Oracle Proof (FRI) pro-
  ithub.io/undergrad_todo.html, 2026. URL
                                                                         tocol, a core component of modern transparent, STARK-
  https://leanprover-community.github.
                                                                         style zero-knowledge proofs.
  io/undergrad_todo.html. Accessed January
  2026.                                                                 Math Inc. The riemann hypothesis for curves, autofor-
                                                                         malized. GitHub repository, 2026. URL https:
Leroy, X. Formal verification of a realistic compiler. Com-
                                                                         //github.com/math-inc/RiemannHypothes
  mun. ACM, 52(7):107–115, July 2009. ISSN 0001-0782.
                                                                         isCurves. This is a formal Lean proof of the Riemann
  doi: 10.1145/1538788.1538814. URL https:
                                                                         Hypothesis for hyperelliptic curves over finite fields. We
  //doi.org/10.1145/1538788.1538814.
                                                                         follow the argument laid out in Chapter 11 of Iwaniec-
Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J.,           Kowalski’s classic text Analytic Number Theory, based
  Xia, M., Chen, D., Arora, S., et al. Goedel-prover: A fron-            on the Bombieri-Stepanov polynomial method.
  tier model for open-source automated theorem proving.                 Mathlib Community. The Lean mathematical library. In
  arXiv preprint arXiv:2502.07640, 2025a.                                Proceedings of the 9th ACM SIGPLAN International Con-
Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao,                ference on Certified Programs and Proofs (CPP ’20), pp.
  H., Jiang, L., Geng, Y., Ge, J., Sun, J., Wu, J., Gesi, J.,            367–381. ACM, 2020. doi: 10.1145/3372885.3373824.
  Lu, X., Acuna, D., Yang, K., Lin, H., Choi, Y., Chen, D.,             Mensfelt, A., Cucala, D. T., Franco, S., Koutsoukou-
  Arora, S., and Jin, C. Goedel-prover-v2: Scaling formal                Argyraki, A., Trencsenyi, V., and Stathis, K. Towards a
  theorem proving with scaffolded data synthesis and self-               common framework for autoformalization, 2025. URL
  correction, 2025b. URL https://arxiv.org/ab                            https://arxiv.org/abs/2509.09810.
  s/2508.03613.
                                                                        Milne, J. S. Lectures on etale cohomology (v2.21), 2013.
Liu, Q., Zheng, X., Lu, X., Cao, Q., and Yan, J. Rethinking              Available at www.jmilne.org/math/.
  and improving autoformalization: Towards a faithful met-
  ric and a dependency retrieval-based approach. In The                 Min, M. J., Gao, Y., Sy, W., Li, Z., Si, X., and Bastani, O. Di-
  Thirteenth International Conference on Learning Repre-                 vide and abstract: Autoformalization via decomposition
  sentations, 2025. URL https://openreview.net                           and abstraction learning. In The Fourteenth International
  /forum?id=hUb2At2DsQ.                                                  Conference on Learning Representations, 2026. URL

                                                                   12
                                              Theory-Level Autoformalization

  https://openreview.net/forum?id=Njga                               Poiroux, A., Weiss, G., Kunčak, V., and Bosselut, A. Re-
  eXNit3.                                                              liable evaluation and benchmarks for statement autofor-
                                                                       malization, 2025. URL https://arxiv.org/abs/
Mora, F., Desai, A., Polgreen, E., and Seshia, S. A. Message           2406.07222.
 chains for distributed system verification. Proc. ACM
 Program. Lang., 7(OOPSLA2), October 2023. doi: 10.1                 Polu, S. and Sutskever, I. Generative language modeling
 145/3622876. URL https://doi.org/10.1145/                             for automated theorem proving, 2020. URL https:
 3622876.                                                              //arxiv.org/abs/2009.03393.

Moura, L. d. and Ullrich, S. The Lean 4 theorem prover and           Qu, C., Dai, S., Wei, X., Cai, H., Wang, S., Yin, D., Xu, J.,
 programming language. In Platzer, A. and Sutcliffe, G.                and Wen, J.-r. Tool learning with large language models:
 (eds.), Automated Deduction – CADE 28, pp. 625–635,                   a survey. Front. Comput. Sci., 19(198343), 2025. ISSN
 Cham, 2021. Springer International Publishing. ISBN                   2095-2228, 2095-2236. doi: 10.1007/s11704-024-40678
 978-3-030-79876-5.                                                   -2.

Murphy, L., Yang, K., Sun, J., Li, Z., Anandkumar, A., and           Reid, A., Chen, R., Deligiannis, A., Gilday, D., Hoyes, D.,
 Si, X. Autoformalizing euclidean geometry, 2024. URL                  Keen, W., Pathirane, A., Shepherd, E., Vrabel, P., and
 https://arxiv.org/abs/2405.17216.                                     Zaidi, A. End-to-End Verification of Arm Processors
                                                                       with Isa-Formal. In Chaudhuri, S. and Farzan, A. (eds.),
Nienhuis, K., Joannou, A., Bauereiss, T., Fox, A., Roe,                Proceedings of the 2016 International Conference on
  M., Campbell, B., Naylor, M., Norton, R. M., Moore,                  Computer Aided Verification (CAV’16), volume 9780 of
  S. W., Neumann, P. G., Stark, I., Watson, R. N. M.,                  Lecture Notes in Computer Science, pp. 42–58. Springer
  and Sewell, P. Rigorous engineering for hardware se-                 Verlag, July 2016. ISBN 978-3-319-41539-0. doi: 10.1
  curity: Formal modelling and proof in the cheri design               007/978-3-319-41540-6\ 3.
  and implementation process. In 2020 IEEE Symposium
  on Security and Privacy (SP), pp. 1003–1020, 2020. doi:            Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,
  10.1109/SP40000.2020.00055.                                          W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F.,
                                                                       Gou, Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D.,
Nipkow, T., Wenzel, M., and Paulson, L. C. Isabelle/HOL:               and Ruan, C. Deepseek-prover-v2: Advancing formal
  a proof assistant for higher-order logic. Springer-Verlag,           mathematical reasoning via reinforcement learning for
  Berlin, Heidelberg, 2002. ISBN 3540433767.                           subgoal decomposition, 2025. URL https://arxiv.
                                                                       org/abs/2504.21801.
OpenAI. Learning to reason with LLMs. OpenAI Blog,
  2024. URL https://openai.com/index/l                               Riazanov, A. and Voronkov, A. Vampire. In Interna-
  earning-to-reason-with-llms/. September                              tional Conference on Automated Deduction, pp. 292–296.
 12, 2024. Introduces OpenAI o1, a model trained with                  Springer, 1999.
  reinforcement learning to perform complex reasoning.
                                                                     Schulz, S. E–a brainiac theorem prover. Ai Communications,
Ozsoy, M. G., Messallem, L., Besga, J., and Minneci,                   15(2-3):111–126, 2002.
  G. Text2cypher: Bridging natural language and graph
  databases. In Proceedings of the Workshop on Generative            Shao, Z. and Ford, B. Advanced development of certified
 AI and Knowledge Graphs (GenAIK), pp. 100–108, 2025.                  OS kernels. Technical report, Department of Computer
                                                                       Science, Yale University, 2010. URL https://www.
Padon, O., McMillan, K. L., Panda, A., Sagiv, M., and                  cs.yale.edu/publications/techreports
  Shoham, S. Ivy: safety verification by interactive general-          /tr1436.pdf.
  ization. SIGPLAN Not., 51(6):614–630, June 2016. ISSN
  0362-1340. doi: 10.1145/2980983.2908118. URL http                  Shih, Y.-A., Lin, A., Gupta, A., and Malik, S. Flag: Formal
  s://doi.org/10.1145/2980983.2908118.                                 and llm-assisted sva generation for formal specifications
                                                                       of on-chip communication protocols, 2025. URL https:
Pang, B., Kong, D., Savarese, S., Xiong, C., and Zhou, Y.              //arxiv.org/abs/2504.17226.
  Reasoning curriculum: Bootstrapping broad llm reason-
  ing from math, 2025. URL https://arxiv.org/                        Shulman, M. Strange new universes: Proof assistants and
  abs/2510.26143.                                                      synthetic foundations. Bull. Amer. Math. Soc. (N.S.), 61
                                                                       (2):257–270, 2024. doi: 10.1090/bull/1830. URL ht
Patel, N., Saha, R., and Flanigan, J. A new approach towards           tps://www.ams.org/journals/bull/2024
  autoformalization, 2024. URL https://arxiv.or                       -61-02/S0273-0979-2024-01830-8/. Article
  g/abs/2310.07957.                                                    electronically published February 15, 2024.

                                                                13
                                               Theory-Level Autoformalization

Stoskopf, T., Cohen, C., and Tabareau, N. Babel-formal:               Wang, C., Li, Z., Dutta, S., and Naik, M. QLCoder: A query
  Translation of proofs between lean and rocq. In The 5th              synthesizer for static analysis of security vulnerabilities,
  Workshop on Mathematical Reasoning and AI at NeurIPS                 2025a. URL https://arxiv.org/abs/2511.0
  2025, 2025. URL https://openreview.net/f                             8462.
  orum?id=WBI1PL0hZ2.
                                                                      Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q.,
Sutcliffe, G. The cade atp system competition—casc. AI                 Huang, Y., Xiong, J., Shi, H., Xie, E., Yin, J., Li, Z.,
  Magazine, 37(2):99–101, 2016.                                        Liao, H., and Liang, X. LEGO-Prover: Neural theorem
                                                                       proving with growing libraries, 2023. URL https:
Sutcliffe, G. Stepping Stones in the TPTP World. In                    //arxiv.org/abs/2310.00656.
  Benzmüller, C., Heule, M., and Schmidt, R. (eds.), Pro-            Wang, H., Xin, H., Liu, Z., Li, W., Huang, Y., Lu, J., Yang,
  ceedings of the 12th International Joint Conference on               Z., Tang, J., Yin, J., Li, Z., and Liang, X. Proving theo-
  Automated Reasoning, number 14739 in Lecture Notes in                rems recursively, 2024a. URL https://arxiv.or
  Artificial Intelligence, pp. 30–50, 2024.                            g/abs/2405.14414.

Sutton, R. The bitter lesson. Blog post, 2019. URL http:              Wang, H., Xie, R., Wang, Y., Gao, G., Yu, X., and
  //www.incompleteideas.net/IncIdeas/B                                 Dong, B. Aria: An agent for retrieval and iterative
  itterLesson.html. March 13, 2019.                                    auto-formalization via dependency graph, 2025b. URL
                                                                       https://arxiv.org/abs/2510.04520.
Szegedy, C. A promising path towards autoformalization
                                                                      Wang, Z., Yang, B., Li, C., Zhang, Y., Zhou, S., Dong,
  and general artificial intelligence. In Intelligent Computer
                                                                       B., and Wen, Z. Translating informal proofs into formal
  Mathematics: 13th International Conference, CICM
                                                                       proofs using a chain of states, 2025c. URL https:
  2020, Bertinoro, Italy, July 26–31, 2020, Proceedings, pp.
                                                                       //arxiv.org/abs/2512.10317.
  3–20, Berlin, Heidelberg, 2020. Springer-Verlag. ISBN
  978-3-030-53517-9. doi: 10.1007/978-3-030-53518-6 1.                Wang, Z. Z., Neubig, G., and Fried, D. TROVE: inducing
  URL https://doi.org/10.1007/978-3-030                                verifiable and efficient toolboxes for solving program-
 -53518-6_1.                                                           matic tasks. In Proceedings of the 41st International
                                                                       Conference on Machine Learning, ICML’24. JMLR.org,
Tarrach, G., Jiang, A. Q., Raggi, D., Li, W., and Jamnik, M.           2024b.
  More details, please: Improving autoformalization with
                                                                      Wei, A. Openai imo 2025 proofs. GitHub repository, 2025.
  more detailed proofs. In AI for Math Workshop @ ICML
                                                                       URL https://github.com/aw31/openai-i
  2024, 2024. URL https://openreview.net/f
                                                                       mo-2025-proofs. This repository hosts the proofs
  orum?id=AkJvzpYMvK.
                                                                       produced by our experimental reasoning LLM during its
Thakur, S., Ahmad, B., Pearce, H., Tan, B., Dolan-Gavitt,              evaluation on the 2025 International Math Olympiad.
  B., Karri, R., and Garg, S. Verigen: A large language               Xin, H., Guo, D., Shao, Z., Ren, Z., Zhu, Q., Liu, B., Ruan,
  model for verilog code generation. ACM Transactions                   C., Li, W., and Liang, X. DeepSeek-Prover: Advancing
  on Design Automation of Electronic Systems, 29(3):1–31,               theorem proving in LLMs through large-scale synthetic
  2024.                                                                 data, 2024. URL https://arxiv.org/abs/2405
                                                                        .14333.
Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M.,
  Jennings, M., Thakur, A., and Chaudhuri, S. Putnam-                 Xin, R., Zheng, Z., Nie, Y., Yuan, K., and Xiao, X. Scaling
  bench: Evaluating neural theorem-provers on the put-                  up multi-turn off-policy rl and multi-agent tree search for
  nam mathematical competition, 2024. URL https:                        llm step-provers, 2025. URL https://arxiv.org/
  //arxiv.org/abs/2407.11214.                                           abs/2509.06493.
                                                                      Xuejun, Y., Zhong, J., Feng, Z., Zhai, P., Yousefzadeh, R.,
U.S. Department of Health and Human Services. HIPAA                     Ng, W. C., Liu, H., Shou, Z., Xiong, J., Zhou, Y., Ong,
  privacy rule, 2024. URL https://www.hhs.gov/                          C. B., Sugiarto, A. J., Zhang, Y., Tai, W. M., Cao, H., Lu,
  hipaa/for-professionals/privacy/index                                 D., Sun, J., Xu, Q., Xin, S., and Li, Z. Mathesis: Towards
  .html. Accessed: 2025-01-29.                                          formal theorem proving from natural languages, 2025.
                                                                        URL https://arxiv.org/abs/2506.07047.
Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and
  Ye, K. Hilbert: Recursively building formal proofs with             Yang, K., Deng, J., and Chen, D. Generating natural lan-
  informal reasoning, 2025. URL https://arxiv.or                        guage proofs with verifier-guided search, 2022. URL
  g/abs/2509.22819.                                                     https://arxiv.org/abs/2205.12443.

                                                                 14
                                              Theory-Level Autoformalization

Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,                 Zhou, J. P., Wu, Y., Li, Q., and Grosse, R. B. REFACTOR:
  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.               Learning to extract theorems from proofs, 2022. URL
  Leandojo: Theorem proving with retrieval-augmented                   https://openreview.net/forum?id=827j
  language models, 2023. URL https://arxiv.org/                        G3ahxL.
  abs/2306.15626.
                                                                     Zhou, J. P., Staats, C., Li, W., Szegedy, C., Weinberger,
Ying, H., Wu, Z., Geng, Y., Yuan, Z., Lin, D., and Chen, K.            K. Q., and Wu, Y. Don’t trust: Verify – grounding llm
  Lean workbook: A large-scale lean problem set formal-                quantitative reasoning with autoformalization, 2024. URL
  ized from natural language math problems, 2025. URL                  https://arxiv.org/abs/2403.18120.
  https://arxiv.org/abs/2406.03847.

Yuan, L., Chen, Y., Wang, X., Fung, Y., Peng, H., and Ji, H.
  CRAFT: Customizing LLMs by creating and retrieving
  from specialized toolsets. In The Twelfth International
  Conference on Learning Representations, 2024. URL
  https://openreview.net/forum?id=G0vd
  DSt9XM.

Zhang, L., Quan, X., and Freitas, A. Consistent autofor-
  malization for constructing mathematical libraries. In
  Proceedings of the 2024 Conference on Empirical Meth-
  ods in Natural Language Processing, pp. 4020–4033.
  Association for Computational Linguistics, 2024. doi:
  10.18653/v1/2024.emnlp- main.233. URL http:
  //dx.doi.org/10.18653/v1/2024.emnlp-m
  ain.233.

Zhang, L., Valentino, M., and Freitas, A. Autoformalization
  in the wild: Assessing llms on real-world mathematical
  definitions, 2025a. URL https://arxiv.org/ab
  s/2502.12065.

Zhang, M., Borchert, P., Gritta, M., and Lampouras, G.
  Drift: Decompose, retrieve, illustrate, then formalize the-
  orems, 2025b. URL https://arxiv.org/abs/25
  10.10815.

Zhao, J., Nagarakatte, S., Martin, M. M., and Zdancewic,
  S. Formalizing the LLVM intermediate representation
  for verified program transformations. In Proceedings
  of the 39th Annual ACM SIGPLAN-SIGACT Symposium
  on Principles of Programming Languages, POPL ’12,
  pp. 427–440, New York, NY, USA, 2012. Association
  for Computing Machinery. ISBN 9781450310833. doi:
  10.1145/2103656.2103709. URL https://doi.or
  g/10.1145/2103656.2103709.

Zhao, X., Li, W., and Kong, L. Decomposing the enigma:
  Subgoal-based demonstration learning for formal theo-
  rem proving, 2023. URL https://arxiv.org/ab
  s/2305.16366.

Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics, 2022.
  URL https://arxiv.org/abs/2109.00110.

                                                                15
                                              Theory-Level Autoformalization

A. Declarative Program Synthesis vs. Imperative Program Synthesis
Autoformalization is, by definition, the semantics-preserving translation from informal natural language to a formal language:
the informal input and the formal output should carry the same semantic content.
Declarative Program Synthesis satisfies this criterion. Declarative languages such as Prolog, SQL, Cedar, and CodeQL
specify what should hold rather than how to compute it. Translating natural language into these languages encodes the
information content of the informal input into a formally scoped specification, preserving its semantics. For example,
translating “every nurse may read a patient’s record only if assigned to that patient” into a Cedar policy produces a formal
artifact whose meaning is precisely the informal statement; no implementation details are introduced.
Imperative Program Synthesis, by contrast, does not satisfy this criterion. Translating a natural-language task description
into procedural or object-oriented code (e.g., Python, C++) introduces implementation details (control flow, data structures,
algorithmic choices, security constraints, etc.) that are absent from the informal input. The output contains strictly more
information than the input, making this a generative task rather than a semantics-preserving translation.
This distinction justifies our inclusion of declarative DSLs in Section 4.3 as autoformalization challenges. This view is
shared by Mensfelt et al. (2025), who similarly consider declarative programming languages (Prolog, PDDL, OWL) as
autoformalization tasks within a common framework. We advocate an inclusive view of autoformalization that recognizes
these shared challenges and enables transfer of methods across domains: progress in mathematical autoformalization directly
benefits declarative program synthesis, and vice versa.

B. Proof Autoformalization vs. Formal Theorem Proving
Proof Autoformalization and Formal Theorem Proving have related but distinct goals:
Formal Theorem Proving aims to produce a formal proof that a given formal statement is true. The goal is to find any proof
that passes the type checker or proof assistant, regardless of how it relates to existing informal arguments. Methods range
from automated tactic search (Polu & Sutskever, 2020; Yang et al., 2023) to reinforcement learning over proof steps (Xin
et al., 2024; Ren et al., 2025).
Proof Autoformalization aims to faithfully translate a specific informal proof into a formal one. The goal is not merely to
verify that a statement is true, but to produce a formal proof whose logical structure corresponds to the reasoning in the
original informal argument. This distinction is critical: two correct formal proofs of the same theorem may follow entirely
different proof strategies, but only one of them may faithfully represent the informal proof being autoformalized.
Early work on proof autoformalization used the informal proof to guide formal proof construction: DSP (Jiang et al.,
2023) translates the informal proof into a formal proof sketch of intermediate conjectures, then uses the sketch to guide
an automated prover toward smaller subgoals; SPADeR (Tarrach et al., 2024) iteratively fills in missing implicit steps by
attempting verification, identifying where the proof fails, and using an LLM to add the needed detail.
More recent work has focused explicitly on structural faithfulness: Step-Proof (Hu et al., 2025) decomposes a natural-
language proof into sentence-level subproofs that can be verified individually; ProofFlow (Cabral et al., 2025) models the
proof structure as a dependency DAG and formalizes each step as an intermediate lemma so the final Lean proof preserves
the original logical flow; ProofBridge (Jana et al., 2025) uses a joint embedding model that aligns NL–FL theorem/proof
pairs for cross-modal retrieval, combined with iterative proof repair via Lean feedback; and Chain of States (Wang et al.,
2025c) extracts a sequence of intermediate formal proof states aligned to the informal reasoning steps, then generates tactics
to move between adjacent states.
On the theory-level, it is not required to prove everything provable in a domain. The goal is to translate existing informal
knowledge (axioms, definitions, notations, theorems, and their proofs) into a coherent formal library. If a true statement
currently has no known informal proof, we would not expect autoformalization to produce a formal proof of it; that is the
job of theorem proving. Theory-level autoformalization produces the formal foundation upon which theorem provers can
then operate to discover genuinely new results.




                                                             16
