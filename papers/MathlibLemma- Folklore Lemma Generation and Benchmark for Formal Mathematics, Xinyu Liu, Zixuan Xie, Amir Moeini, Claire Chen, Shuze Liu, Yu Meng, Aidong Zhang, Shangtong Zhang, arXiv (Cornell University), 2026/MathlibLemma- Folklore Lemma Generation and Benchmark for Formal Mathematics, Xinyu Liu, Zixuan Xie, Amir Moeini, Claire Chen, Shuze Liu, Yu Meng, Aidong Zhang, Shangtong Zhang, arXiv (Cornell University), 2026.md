                                                    MathlibLemma: Folklore Lemma Generation and Benchmark for
                                                                       Formal Mathematics


                                             Xinyu Liu 1 Zixuan Xie 1 Amir Moeini 1 Claire Chen 2 Shuze Daniel Liu 3 4 Yu Meng 1 Aidong Zhang 1
                                                                                     Shangtong Zhang 1


                                                                    Abstract                                       1. Introduction
arXiv:2602.02561v3 [cs.LO] 27 May 2026




                                                                                                                   Fully formal proofs checked by proof assistants against a
                                                                                                                   small trusted kernel offer a principled route to making math-
                                              While the ecosystem of Lean and Mathlib has en-                      ematical verification reliable, scalable, and reproducible.
                                              joyed celebrated success in formal mathematical                      This promise becomes increasingly salient as proofs in mod-
                                              reasoning with the help of large language models                     ern mathematics and computer science grow longer and
                                              (LLMs), the absence of many folklore lemmas                          more intricate. A striking illustration is the ABC conjecture:
                                              in Mathlib remains a persistent barrier that limits                  formulated independently by Masser (1985) and Oesterlé
                                              Lean’s usability as an everyday tool for mathe-                      (1988), it is widely viewed as a master key in number theory.
                                              maticians like LATEX or Maple. To address this,                      Despite its deceptively simple statement, a proof would re-
                                              we introduce M ATHLIB L EMMA, a modular LLM-                         shape the landscape of number theory by unifying numerous
                                              based pipeline for automated folklore-lemma min-                     disparate results, streamlining long and intricate arguments,
                                              ing: the discovery, formalization, and proving of                    and clarifying what is fundamentally possible and impos-
                                              reusable intermediate facts that mathematicians                      sible. Mochizuki later announced a highly technical proof
                                              often take for granted but that are not always                       spanning hundreds of pages, as presented in (Mochizuki,
                                              present in formal libraries. At its core, M ATH -                    2021a;b;c;d). Yet, despite substantial effort by experts in the
                                              LIB L EMMA proactively mines the missing con-                        past 10 years, the community still has not reached a simple
                                              nective tissue of mathematics. The pipeline pro-                     shared understanding of the argument’s correctness (Tao,
                                              duces a verified library of folklore-style lemmas,                   2012; Scholze & Stix, 2018; Mochizuki, 2019; Rittberg,
                                              including 1,506 Lean-checked proofs that pass                        2021). This situation is not merely sociological trivia: it ex-
                                              a proof-bypass screen; a small curated pilot sub-                    poses a structural limit of an informal pipeline that relies on
                                              set has also been merged into Mathlib, providing                     human intuition, local norms, and bounded attention. For-
                                              external evidence that selected outputs can meet                     mal verification is designed precisely to turn such debates
                                              expert library standards. Leveraging this pipeline,                  from sociological uncertainty to automatic verification.
                                              we further construct the M ATHLIB L EMMA bench-
                                              mark, a suite of 4,028 non-trivial type-checked                      At the same time, many researchers remain reluctant to write
                                              Lean statements spanning a broad range of math-                      proofs in formal languages. Beyond the well-known high
                                              ematical domains. By transforming the role of                        barrier to entry, a particularly stubborn bottleneck is library
                                              LLMs from passive consumers to active contrib-                       coverage: even when a proof is conceptually straightfor-
                                              utors, this work takes a step toward AI-assisted                     ward, formalizing it can stall on the absence of small “obvi-
                                              expansion of formal mathematical libraries.                          ous” facts. In this paper we focus on Lean 4 (de Moura &
                                                                                                                   Ullrich, 2021) and its flagship library Mathlib (The mathlib
                                                                                                                   Community, 2020), which has become the de facto standard
                                                                                                                   ecosystem for Lean formalization. Despite Mathlib’s scale,
                                             1                                                                     users still encounter missing lemmas at exactly the wrong
                                               Department of Computer Science, University of Virginia 2 The
                                         Division of Physics, Mathematics and Astronomy, California Insti-         moment: in the middle of a proof whose mathematical ideas
                                         tute of Technology 3 Massachusetts Institute of Technology 4 Purdue       are clear but whose formal details require a long chain of
                                         University. Correspondence to:                                            routine rewrites, inequalities, or structural facts. We refer
                                         Xinyu Liu <xinyuliu@virginia.edu>,                                        to these missing pieces as folklore lemmas: facts that work-
                                         Shangtong Zhang <shangtong@virginia.edu>.
                                                                                                                   ing mathematicians routinely use without comment, often
                                         Proceedings of the 43 rd International Conference on Machine              learned implicitly from textbooks, lectures, or repeated prac-
                                         Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026              tice, but which are not necessarily present in the library in
                                         by the author(s).

                                                                                                               1
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

a readily reusable form. The resulting friction constitutes           Module that tries to fix syntax and type errors of the Lean
a last-mile barrier that limits proof assistants from becom-          statements by interacting with a Lean server. All retained
ing everyday tools, comparable in convenience to LATEX or             Lean statements after the Formalizer are type-checked. The
Maple.                                                                last is a Prover Module that tries to prove the Lean statement
                                                                      that passes the judge and type-checks after formalization.
This last-mile phenomenon is widely reported by practi-
                                                                      This modular design is essential for the novel task of folklore
tioners. For example, in Terence Tao’s Lean formalization
                                                                      mining: by decoupling semantic plausibility from syntac-
project on the polynomial Freiman–Ruzsa conjecture (Tao,
                                                                      tic correctness and proof search, it makes the main failure
2023), he notes that the mathematically interesting parts
                                                                      modes observable and separately addressable.
were comparatively easy to formalize, while “technical ob-
vious steps” took the longest, especially in the final stretch        This framework constitutes our primary contribution, pio-
involving properties of independent random variables. Sim-            neering the task of automated folklore mining. Its efficacy
ilarly, in a Lean formalization effort on foundational rein-          is demonstrated by the production of a type-checked library
forcement learning theory, a single line about conditional ex-        of folklore lemmas, a subset of which has already been for-
pectation expands into a large formal development (Zhang,             mally merged into Mathlib, providing external evidence
2026), illustrating that folklore steps may be simple to state        that selected outputs can meet expert library standards.
informally yet costly to reconstruct in a proof assistant.
                                                                      As a second artifact, we construct the M ATHLIB L EMMA
These last-mile gaps can also degrade LLM-based formal
                                                                      benchmark, a suite of 4,028 non-trivial type-checked state-
reasoning. When a necessary lemma is missing, an LLM
                                                                      ments. To assess statement quality, we audit a seed-stratified
cannot simply invoke it via a concise reference. Instead, it
                                                                      sample of unproven residuals across diverse topics; 78%
is forced to reconstruct the result from scratch, transforming
                                                                      of the audited instances are mathematically sound, sug-
a single inference step into a lengthy derivation. This can
                                                                      gesting that many benchmark instances left unsolved by
expand the search space and consume context tokens, mak-
                                                                      current provers are valid rather than hallucinated. We eval-
ing the overall proof attempt more prone to hallucination
                                                                      uated state-of-the-art models including GPT-5.1, GPT-5.1
and failure.
                                                                      with low reasoning (OpenAI, 2025a;b)1 , Goedel-Prover-
In parallel to these challenges, automated theorem proving            V2-32B (Lin et al., 2026), DeepSeek-R1-Distill-Qwen-
in Lean has advanced rapidly with large language models               32B, DeepSeek-R1-Distill-Llama-70B (Guo et al., 2025),
(LLMs) (Achim et al., 2025; Chen et al., 2025; Chervonyi              Kimina-Prover-72B (Wang et al., 2025), and Qwen3-235B-
et al., 2025; Lin et al., 2025; Math-Inc, 2025; Hubert et al.,        A22B-Thinking-2507 (Yang et al., 2025). Collectively, 37%
2026; Lin et al., 2026). However, many existing evaluations           of the 4,028 lemmas are proved, whereas each individual
of LLMs’ capability in formal reasoning emphasize fixed               model can prove about 19% at most.
problem sets (Zheng et al., 2022; Azerbayev et al., 2023;
                                                                      These artifacts highlight the key distinction of our work:
Tsoukalas et al., 2024; Yu et al., 2025) and are only a partial
                                                                      M ATHLIB L EMMA is both a benchmark and a library-
proxy for addressing the last-mile gap. Furthermore, those
                                                                      expansion pipeline. It requires limited manual annotation,
systems and evaluations largely consume Mathlib but do not
                                                                      can be refreshed across domains, and allows future prover
systematically contribute to Mathlib. This one-way pattern
                                                                      successes to be recycled into a verified folklore-lemma
leaves an important opportunity unexplored: using models
                                                                      repository rather than remaining only benchmark scores.
not only to consume formal libraries, but also to help expand
them.                                                                 Code and Data Availability. The source code and datasets
                                                                      are available at https://github.com/Sequentia
We argue that addressing the last-mile gap calls for a comple-
                                                                      l-Intelligence-Lab/MathlibLemma. The repos-
mentary direction: rather than waiting for users to encounter
                                                                      itory contains two primary artifacts: the complete bench-
gaps, we should proactively discover and formalize these
                                                                      mark suite of 4,028 non-trivial type-checked statements, and
folklore lemmas at scale. To that end, we introduce M ATHLI -
                                                                      the verified library of 1,506 Lean-checked generated proofs
B L EMMA, to our knowledge, the first LLM-based modu-
                                                                      that pass the proof-bypass screen.
lar pipeline designed specifically for automated folklore-
lemma mining from an existing formal library.                            1
                                                                           OpenAI’s GPT-5.1 API documentation lists four reasoning-
                                                                      effort settings: none, low, medium, and high. In this work, “GPT”
At a high level, M ATHLIB L EMMA consists of four LLM-                refers to the none setting (which is the default configuration), and
backed modules. The first is a Discovery Module that iden-            “GPT-Reasoning” refers to the low setting. We excluded medium
tifies candidate missing folklore lemmas using existing files         and high levels as they were prohibitively slow and expensive for
from Mathlib as seeds. This Discovery Module outputs                  our large-scale evaluation. We note that previous baselines, such
                                                                      as Goedel or Kimina, typically did not include evaluations against
candidate lemmas in Lean directly. The second is a Judge
                                                                      these frontier reasoning APIs.
Module using LLM-as-a-judge to filter out Lean statements
that are mathematically wrong. The third is a Formalizer

                                                                  2
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

2. Related Work                                                      M ATHLIB L EMMA aligns with this feedback-rich paradigm
                                                                     but differs fundamentally in artifact reusability. Systems
Our work sits at the intersection of automated theorem prov-         like Delta Prover or Seed-Prover typically generate lemmas
ing, library evolution, and large language model (LLM)               as ad-hoc scaffolding customized to resolve specific hard
benchmarking. Unlike systems designed to solve individual            problems, often discarding them or leaving them dependent
Olympiad-level problems, M ATHLIB L EMMA focuses on the              on the problem context. In contrast, our pipeline is designed
structural last-mile challenge: constructing the dense lattice       to produce reusable, general-purpose statements derived
of folklore lemmas required for everyday formalization.              from library gaps. Our outputs are structurally designed not
                                                                     as transient steps in a proof search tree, but as permanent
2.1. Lemma Synthesis and Library Expansion                           candidates for the library.
The goal of automatically expanding formal libraries pre-
dates the recent progress in LLMs. Sivaraman et al. (2022)           2.3. Benchmarks and the Saturation of Olympiad Math
introduce data-driven methods to synthesize lemmas from              Finally, our work addresses a critical gap in evaluation. The
interactive proof traces in Coq. With the rise of LLMs,              landscape of formal reasoning benchmarks has historically
focus shifted to generative conjecturing to grow libraries           focused on Olympiad-level problem solving or undergradu-
of reusable skills (Wang et al., 2024). More recent works            ate autoformalization (Zheng et al., 2022; Azerbayev et al.,
employ LLMs to generate conjectures from existing library            2023; Tsoukalas et al., 2024; Achim et al., 2025). How-
seeds. LeanConjecturer (Onda et al., 2025) uses rule-based           ever, performance on these benchmarks is reaching satu-
context extraction and automated tactics (e.g., aesop, a pow-        ration. Recent empirical advancements demonstrate that
erful proof search tool) to filter and evaluate candidates in        success rates on MiniF2F have surged from 50% (Wang
Lean. In parallel, Lemmanaid (Alhessi et al., 2025) targets          et al., 2024) to near-saturation levels of 96% (Zhou et al.,
Isabelle/HOL, combining LLM-generated templates with                 2025). This rapid progress suggests that “depth” (solv-
a symbolic engine to enforce well-typedness and novelty              ing hard problems) has reached a high level of proficiency,
relative to the Archive of Formal Proofs (AFP).                      while “breadth” (knowledge coverage) remains unaddressed.
M ATHLIB L EMMA differentiates itself from recent library-           M ATHLIB L EMMA fills this void. Instead of testing ingenu-
centric works like LeanConjecturer by prioritizing folklore          ity on solved benchmarks, we evaluate a component’s ability
mining—the identification of missing structural gaps—over            to formalize and prove the vast quantity of routine back-
the general conjecturing of plausible facts. Rather than             ground facts that human mathematicians take for granted.
merely expanding the library with random valid statements,           This shift from isolated problem solving to foundational
our Discovery Module targets the missing connective tissue           library building is essential for the next stage of formal
that working mathematicians implicitly rely on but is absent         reasoning, ensuring that models can not only solve puzzles
from the library.                                                    but also contribute productively to formal ecosystems. A
                                                                     recent work Xie et al. (2026) also follows this direction by
2.2. Intermediate Lemmas and Feedback-Driven Repair                  benchmarking whether LLMs are able to judge whether a
                                                                     pull-request to Mathlib is ready to be merged.
A parallel line of research uses lemma generation as a mech-
anism for proof search, evolving rapidly from reinforce-
ment learning to agentic repair loops. Early LLM-based               3. The M ATHLIB L EMMA Framework
approaches like ProD-RL (Dong et al., 2024) use reinforce-           3.1. Task Formulation: Automated Folklore Mining
ment learning to reward the hierarchical decomposition of
proofs. More recently, the state-of-the-art shifted to agentic       We formalize the task of Automated Folklore Mining. Unlike
loops that actively exploit compiler feedback. Systems like          standard autoformalization (which translates informal text
Delta Prover (Zhou et al., 2025) and APOLLO (Ospanov                 to formal code) or Olympiad-level proving (which solves
et al., 2025) utilize Lean’s compiler error messages to iter-        closed problems), folklore mining aims to proactively ex-
atively refine subgoals. Meanwhile, ProofAug (Liu et al.,            pand the library by identifying and verifying missing in-
2025) analyzes proof structures in Isabelle, extracting and          termediate results.
refining “maximal compatible semi-proofs” to improve ro-             Formally, let L denote a background formal library (e.g.,
bustness. Similarly, Seed-Prover (Chen et al., 2025) and             Mathlib). Given a seed context C ⊂ L (represented by a
Hilbert (Varambally et al., 2026) utilize recursive decompo-         source file and its imports), our objective is to synthesize a
sition to generate intermediate scaffolding. Gödel’s Poetry         set of pairs {(S, P )}, where S is a lemma statement and P
(Davis, 2025) then extends this approach by integrating AST-         is its proof, satisfying three conditions:
based parsing to programmatically extract and recursively
prove subgoals.                                                      1. Semantic Novelty: The lemma S represents a “missing
                                                                     step” or generalization not explicitly present in L, avoiding

                                                                 3
                              M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

                                                                                                           Consequently, the Prover Module operates on a guaran-
   Mathlib context            Discovery Module                Candidate lemma        Legend
    (seed files)                 (Generation)                    pool (raw)                                teed well-formed proposition, focusing solely on proof
                                                                       normalize       Artifacts
                                                                                   (persistent sets)
                                                                                                           construction without being blocked by invalid definitions
      Rejected
                     reject     Judge Module        accept
                                                                 Accepted
                                                                                                           or imports. This separation allows for specialized feedback
     candidates                (Semantic Filter)              candidates (raw)      LLM modules
                                                                                      (stages)             loops that are impossible in monolithic generation.
                                Persistent
                                job queue
                                                                                   External verifier

                              Formalizer Module
                                                                                                           3.2.1. D ISCOVERY M ODULE : C ONTEXT-AWARE
                                                                Lean Server
                                (Repair Loop)
               success                                                                                            C ANDIDATE G ENERATION

    Type-checked                Prover Module       success       Verified
                                                                                                           Goal. Generate diverse candidate lemma statements con-
                              (Proof Search loop)
     statements                                                    proofs
                                                                                                           ditioned on Mathlib seed context C, without attempting
                                                                                                           proofs. Each candidate is emitted as Lean code containing
Figure 1. Overview of M ATHLIB L EMMA. A modular pipeline                                                  lemma/theorem declarations with sorry (a placeholder for
where the Discovery Module mines candidates from Mathlib seeds,                                            missing proofs).
followed by semantic filtering (Judge), syntactic repair (Formal-
izer), and proof generation (Prover), yielding a verified library and                                      Method. Given the full content of a seed Mathlib file, the
benchmark.                                                                                                 Discovery Module employs a structured prompt to brain-
                                                                                                           storm plausible missing folklore lemmas. This prompt is
                                                                                                           explicitly designed to encourage the identification of struc-
trivial restatements of existing facts.                                                                    tural gaps and cross-topic interactions (e.g., via high-
2. Mathematical Plausibility: The statement S corre-                                                       level planning) before generating the formal statements.
sponds to a true mathematical fact, free from hallucinations                                               Crucially, to ensure engineering robustness, the module
or false conjectures, ensuring it is worth attempting to prove.                                            enforces a normalized output format, which facilitates the
                                                                                                           reliable extraction and splitting of diverse candidates for
3. Syntactic Validity: The final output must be rigorously                                                 downstream verification.
verified by the kernel, i.e., the statement S is syntactically
well-formed in context C, and the proof P is valid for S                                                   3.2.2. J UDGE M ODULE : S EMANTIC F ILTERING
under this context. For proof artifacts used in the benchmark                                                     (LLM- AS - A -J UDGE )
and release, we additionally require the generated code to
pass the proof-bypass screen defined below.                                                                Goal. Filter out statements that are mathematically false or
                                                                                                           nonsensical before invoking kernel-validated checking or
This formulation shifts the challenge from purely solving a                                                proof search.
given statement to discovering what statements are worth
solving.                                                                                                   Method. For each single-lemma candidate, we ask an LLM
                                                                                                           to assess mathematical correctness while explicitly ignor-
3.2. High-Level Pipeline                                                                                   ing Lean well-formedness. This design ensures that valid
                                                                                                           mathematical insights are not prematurely discarded due to
Figure 1 provides a visual overview of this architecture. The                                              trivial, fixable syntax errors, which are effectively handled
detailed execution logic is provided in Algorithm 1 (Ap-                                                   by the subsequent Formalizer Module. The Judge Module
pendix A.1). In this section, we detail the specific goal                                                  outputs a binary verdict (correct vs. wrong); we discard
and method for each module. To ensure reproducibility,                                                     wrong candidates and forward only correct ones, pro-
we document the exact prompt templates, input specifica-                                                   viding a lightweight semantic filter before kernel-level repair
tions, and structured output extraction logic in Appendix B,                                               or proof search.
with detailed runtime configurations (e.g., temperature, max
tokens) provided in Appendix A.2.                                                                          3.2.3. F ORMALIZER M ODULE : K ERNEL -G UIDED T YPE
Design Rationale: Factorizing Failure Modes. Standard                                                             C HECKING AND R EPAIR
end-to-end synthesis entails a compounding risk of fail-                                                   Goal. Transform a semantically plausible candidate into a
ure, where mathematical hallucinations, syntax errors, and                                                 well-formed Lean statement S that is a valid proposition in
proof search failures are entangled. Our four-stage mod-                                                   context C (still with sorry).
ular pipeline is designed to factorize these distinct fail-
ure modes into orthogonal stages: (1) The Judge Mod-                                                       Method. For each judged lemma, we invoke kernel check-
ule eliminates semantic noise early, preventing the prover                                                 ing via Kimina Lean server (Dos Santos et al., 2025) to
from wasting compute on mathematically false premises;                                                     elaborate and type-check the statement and return structured
(2) The Formalizer Module bridges the syntax-semantics                                                     diagnostics. If errors occur, we iteratively prompt an LLM
mismatch, strictly separating the syntactic formalization                                                  to fix them using a transcript that includes (i) the current
of the statement from the logical burden of proving it; (3)                                                Lean code and (ii) diagnostic messages. The prompt forbids

                                                                                                       4
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

proving the lemma and focuses solely on making the state-           4.1. Evaluation Protocol
ment compile (e.g., resolving namespaces, identifiers, and
                                                                    While our system’s goal is discovery (Section 3.1), the
implicit arguments). The loop terminates when the Lean
                                                                    benchmark evaluates a model’s capability for closed-book
server reports no error-level diagnostics or when a maximum
                                                                    automated proving on these discovered lemmas. Each
number of repair trials is reached. Successful results are
                                                                    benchmark instance is a pair (C, S), consisting of a well-
stored together with generation metadata (e.g., trial counts)
                                                                    typed Lean proposition S together with the sufficient self-
to facilitate downstream benchmarking and analysis.
                                                                    contained context C required to elaborate it (including nec-
                                                                    essary imports, open namespaces, and variable declarations).
3.2.4. P ROVER M ODULE : C LOSING THE L OOP WITH
                                                                    Importantly, we do not provide ground-truth proofs; the task
       V ERIFIED P ROOFS
                                                                    is to synthesize a proof P strictly from the given statement
Goal. Produce a valid proof term P for the type-checked             and context.
statement S such that the resulting artifact passes Lean
                                                                    Input and Output. The input provided to the model in-
checking and the proof-bypass screen.
                                                                    cludes both the context C and the statement S. Explicitly
Method. Given a type-checked lemma statement, we                    providing C ensures that the instance is self-contained and
prompt a prover LLM to (i) propose a proof plan and (ii)            compilable without requiring the model to retrieve external
output the full lemma-with-proof in Lean using a stage-             files. Given this input, a model must output Lean code that
specific marker. We validate each attempt by compiling the          proves the statement. A prediction is counted as successful
generated lemma-with-proof via the Lean server. A proof             only if the generated proof passes both Lean checking and
attempt is accepted only if it satisfies both Lean checking         the proof-bypass screen defined in Section 3.2.4.
and a proof-bypass screen. First, the self-contained Lean
                                                                    Closed-book Constraint. During evaluation, models are
file must elaborate with no error-level diagnostics. Sec-
                                                                    not allowed to use external retrieval tools (e.g., code search,
ond, the screen is applied to the extracted model-generated
                                                                    RAG, or browsing Mathlib sources). This design serves
proof code, not to the imported Mathlib environment. Af-
                                                                    three key purposes: 1. Isolating Model Capability: By
ter stripping Lean comments, it rejects incomplete-proof
                                                                    removing the dependency on external retrievers, we decou-
placeholders (sorry, admit, or Lean’s corresponding
                                                                    ple the model’s reasoning power from the quality of the
sorryAx) and model-introduced top-level declarations
                                                                    search stack, ensuring a fair “apples-to-apples” comparison
that could add new assumptions, primitive objects, or black-
                                                                    across diverse architectures. 2. Feasibility: It allows for
box facts (axiom, constant, or opaque). Fully proved
                                                                    scalable evaluation of expensive frontier reasoning models
auxiliary lemmas are allowed, but the model may not ex-
                                                                    (e.g., GPT-Reasoning), where multi-turn agentic retrieval
pand the trusted context with new assumptions or hidden
                                                                    for thousands of instances would be cost-prohibitive. 3.
declarations. On failure, we capture the compiler error
                                                                    Conservative Lower Bound: This setting acts as a stress
messages returned by the server. We then append the failed
                                                                    test for the models’ internalized mastery of Mathlib. While
code snippet combined with these error messages to the
                                                                    it conflates reasoning with recall, the resulting scores repre-
history buffer and prompt the model to repair the proof.
                                                                    sent a conservative lower bound on performance, measuring
This generate-verify-repair loop starts with an initial proof
                                                                    robust formalization ability rather than search efficiency.
attempt and then allows up to two repair rounds; we report
this setting as Success@2. Successful proofs are stored
persistently for downstream evaluation.                             4.2. Construction and Filtering
                                                                    We construct the M ATHLIB L EMMA benchmark by execut-
4. The M ATHLIB L EMMA Benchmark                                    ing the first three stages of our pipeline (Discovery, Judge,
                                                                    Formalizer) on seed contexts sampled from Mathlib. Specif-
Using the pipeline described in Section 3, we constructed           ically, we selected a diverse set of 109 source files spanning
M ATHLIB L EMMA, a benchmark of 4,028 non-trivial type-             the domains shown in Figure 2. For each instance, the entire
checked Lean 4 statements derived from diverse domains of           source file is used as the seed context. To ensure the high
Mathlib. Unlike previous datasets focused on high-school            quality of the benchmark statements, we employ a fron-
competitions (e.g., MiniF2F) or undergraduate text prob-            tier model (GPT-5.1) for all generation and filtering steps.
lems (e.g., ProofNet), our benchmark focuses on the missing         This process functions as a rigorous automated funnel: the
intermediate steps—the folklore lemmas—that bridge high-            system generates raw candidates, semantically filters hallu-
level intuition and formal verification.                            cinations via the Judge Module, and syntactically repairs
                                                                    them via the Formalizer Module. Only candidates that sur-
                                                                    vive this pipeline are admitted into the benchmark, ensuring
                                                                    high fidelity without the bottleneck of manual annotation.


                                                                5
                         M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics
                                 Complex & Functional Number Theory
                       Analysis
            (Lp, Series, Taylor)
                                 (Hahn-Banach)        (L-Series, Zeta)                          nations. To assess this filter, we audited a seed-stratified
                                                          Category Theory
                                                          (Galois, Fibered)                     sample of 53 candidates rejected by the Judge. We found
 Discrete & Matrix
                                                                                                that 54% were indeed mathematically false, while the re-
      (Finset, Int)                                               Algebra & Rep Thy
                                                                  (Group Homology)
                                                                                                maining 46% were valid statements erroneously rejected
                        Foundational
                                                 Abstract
                                                 Domain
                                                                                                (false negatives). Nevertheless, every seed context still con-
                          Domain

Special Functions
                                                                                                tributed surviving candidates after judging. While this in-
      (Exp, Pow)
                                                                     Geometry & Topology
                                                                     (Manifolds, Bundles)
                                                                                                dicates an imperfection in the Judge’s recall, it shows that
                                       Applied                                                  the Judge acts conservatively, discarding many questionable
                                       Domain
                                                                    Combinatorics &
        Probability                                                 Info Theory                 candidates before formalization. The quality of the retained
 (Basic Martingale)
                                                                  Linear Algebra
                                                                  (Matrix, Rank)
                                                                                                benchmark statements is assessed separately by the residual
             Adv. Probability
       (Martingales, Ergodic)               Calculus & Analysis                                 provability audit in Section 4.3. Subsequently, the Formal-
                                            (Fourier, Convex)
                                                                                                izer Module successfully compiles the majority (61%–77%)
Figure 2. M ATHLIB L EMMA taxonomy of seed-topic areas. The                                     of these judged candidates. Notably, the compilation rate
benchmark is partitioned into three distinct domains (inner ring):                              is highest in Foundational Domain (77.1%) and lowest in
Foundational, Applied, and Abstract. The outer ring shows topic
                                                                                                Abstract Domain (61.3%), reflecting the higher syntactic
areas used to source seed contexts, with representative examples
in parentheses.                                                                                 complexity of abstract mathematical structures.

                                                                                                Table 1. Pipeline Funnel Statistics. “Judge-accepted” denotes
                                                                                                statements labeled correct by the Judge Module; “Compilable”
                                                                                                denotes statements that passed the Lean kernel check. Percentages
Data Stratification. To facilitate fine-grained analysis, we                                    represent the pass rate relative to the count of the preceding stage
stratified the seed contexts into three distinct domains: Foun-                                 (e.g., Compilable % is calculated relative to the Judge-accepted
dational, Applied, and Abstract. This classification was                                        count).
performed manually by grouping Mathlib source files ac-
                                                                                                 Domain         Proposed   Judge-accepted (%)   Compilable (%)   Trivial (%)
cording to their primary mathematical subject matter and
                                                                                                 Foundational    3427         2447 (71.4%)       1887 (77.1%)       4.1%
directory location.                                                                              Applied         2591         1726 (66.6%)       1219 (70.6%)       6.6%
                                                                                                 Abstract        3130         1977 (63.2%)       1211 (61.3%)      10.8%
1. Foundational Domain. This domain covers the “bread
and butter” of formalized mathematics: real analysis, dis-
                                                                                                Lightweight Triviality Check. As a lightweight proxy for
crete structures (e.g., sets, matrices), basic probability, and
                                                                                                triviality and obvious redundancy, we flag instances solved
others. These lemmas often require high familiarity with
                                                                                                immediately by aesop as trivial. The low percentage of
Mathlib’s naming conventions and standard tactics, testing
                                                                                                trivial lemmas across domains (4.1% in Foundational Do-
a model’s internalized knowledge recall capabilities.
                                                                                                main, increasing to 10.8% in Abstract Domain) indicates
2. Applied Domain. This domain includes domains such                                            that the Discovery Module successfully targets non-trivial
as advanced probability (martingales), information theory,                                      gaps rather than trivial tautologies. Unless stated otherwise,
and convex analysis. While the mathematical concepts are                                        we exclude these trivial instances from the main proving re-
often intuitive to humans (e.g., “expected value is linear”),                                   sults. In total, this removes 289 aesop-trivial statements (78
they are notoriously difficult to formalize due to heavy type-                                  Foundational, 80 Applied, and 131 Abstract), leaving 4,028
class constraints (e.g., measurability proofs, integrability                                    non-trivial type-checked statements for the main bench-
conditions). This domain tests a model’s ability to handle                                      mark.
syntactic overhead and formalization gaps.
                                                                                                Generation-model dependence. Because GPT-5.1 is used
3. Abstract Domain. This domain spans abstract fields                                           for candidate discovery, judging, and statement repair, the
including category theory, algebraic topology, and differ-                                      benchmark distribution partly reflects GPT-5.1’s view of
ential geometry. Proofs here rely less on calculation and                                       what folklore lemmas look like and how they should be
more on abstract structural reasoning (e.g., diagram chasing,                                   phrased. The subsequent proof evaluation is objective in the
functoriality). This tests a model’s capacity for deep logical                                  sense that success is determined by Lean checking together
reasoning.                                                                                      with the proof-bypass screen, but the set of evaluated state-
                                                                                                ments is shaped by the generation model. We therefore view
We use this partition to report construction statistics and
                                                                                                M ATHLIB L EMMA as a versioned benchmark generated by
evaluate model performance.
                                                                                                a specified pipeline, rather than as a model-independent
Pipeline Funnel Statistics. Table 1 reports the detailed                                        census of all missing Mathlib folklore. The current Discov-
statistics of this funnel across the three domains. Observe                                     ery stage is intentionally seed-file local and one-shot, with-
that the drop from ‘Proposed’ to ‘Judge-accepted’ is signifi-                                   out repository-wide retrieval, dependency-graph traversal,
cant (filtering out 30-37% of raw candidates), highlighting                                     or proof-attempt-driven gap detection; preliminary open-
the critical role of the Judge Module in removing halluci-                                      model discovery runs produced lower-quality candidates, so

                                                                                            6
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

we leave broader repository-aware discovery to future work.          Table 2. Human Provability Audit. We analyze a seed-stratified
                                                                     sample of model-unsolved instances to assess residual validity
                                                                     across diverse seed contexts. For each domain, we sampled lem-
4.3. Validity: Provability Audit                                     mas from diverse seed contexts (2 lemmas per seed). The high
                                                                     human success rate implies that the benchmark remains challeng-
Unlike benchmarks derived from existing libraries, M ATH -           ing but solvable, and that many failures are due to current prover
LIB L EMMA consists of novelly discovered conjectures.               limitations rather than false statements.
Consequently, these instances do not inherently possess
ground-truth proofs. An evaluation failure can therefore                  Domain           Sampled      Human-proved       Rate
have two different causes: the statement may be valid but                 Foundational        38               30           79%
beyond the prover’s current capabilities, or it may be un-                Applied             56               40           71%
provable as stated because of missing hypotheses or an over-              Abstract            44               37           84%
strong conclusion. To separate these factors, we conducted                Total               138             107           78%
an expert provability audit on up to two model-unsolved
instances from each audited seed context, a seed-stratified
sampling strategy that gives coverage across diverse Math-
lib contexts. We use this audit to assess the validity of the        MiniF2F) where ground-truth proofs are known, our bench-
sampled residuals and to diagnose common failure modes.              mark represents a dynamic discovery setting: instances
                                                                     are type-checked conjectures without pre-existing solutions.
Audit Protocol. The audit was performed by expert formal-            Consequently, success is defined strictly by independent
izers. Unlike the closed-book evaluation for models, the             Lean checking together with the proof-bypass screen. In
human experts operated in an open-book setting, allowed              this section, we primarily report the Sequential Success@2
to utilize the full Mathlib library, AI assistance, and ex-          (specifically Success@2: cumulative success within a bud-
ternal search tools. For each sampled instance, the expert           get of 2 repair turns) as the definitive measure of system ef-
attempted to construct a proof from scratch to determine             ficacy. Unlike standard Pass@k which aggregates paralleliz-
its mathematical truth and formal provability. This setup            able independent samples, Success@k measures sequential
ensures that we strictly measure the intrinsic validity of           self-correction. Since this repair loop is inherently serial,
the statements, independent of the closed-book constraints           we limit the budget to k = 2. Further experimental details
imposed on the models.                                               and performance analyses are provided in Appendix C.
Audit Results. Table 2 presents the results of this audit.
Across all domains, experts successfully proved 78% of the           5.1. Experimental Setup
sampled instances. This high validity rate primarily serves
                                                                     We evaluate a diverse set of models: the generalist GPT-
as evidence of our framework’s efficacy, suggesting that
                                                                     5.1 (“GPT”) and its reasoning variant (“GPT-Reasoning”);
the construction pipeline has reasonably high precision on
                                                                     the open-weight reasoning models DeepSeek-R1-Distill-
this sampled subset and produces mathematically sound tar-
                                                                     Qwen (“DS-32B”), DeepSeek-R1-Distill-Llama-70B (“DS-
gets. Since the audit sample is drawn from model-unsolved
                                                                     70B”) (collectively “DeepSeek”), and Qwen3-235B-A22B-
residuals, the human success rate shows that many residual
                                                                     Thinking-2507 (“Qwen”); the library specialist Goedel-
failures are not false statements; it highlights a gap between
                                                                     Prover-V2 (“Goedel”), a model pre-fine-tuned on Mathlib;
current closed-book provers and expert open-book formal-
                                                                     and Kimina-Prover-72B (“Kimina”), a model trained via
ization.
                                                                     RL on formal competitions (e.g., MiniF2F). We follow the
For the unproven minority (22%), qualitative analysis (Ap-           closed-book protocol defined in Section 4.1.
pendix D) reveals that the dominant failure mode is Missing
Hypotheses (e.g., omitting integrability or non-emptiness            5.2. Main Results
conditions), rather than fundamental mathematical errors.
This finding underscores a characteristic challenge of folk-         We summarize the aggregated performance in Table 3.
lore mining: while models effectively capture the core math-         1. The “Specialist vs. Generalist” Trade-off. The most
ematical intuitions, they occasionally overlook the implicit         striking result is the performance dichotomy between open-
boundary conditions that human mathematicians take for               weight specialists and frontier generalists. Goedel-Prover
granted but formal systems strictly require.                         achieves a remarkable 27.42% success rate in the Founda-
                                                                     tional Domain, significantly outperforming GPT-Reasoning
5. Experiments                                                       (22.44%). However, its performance collapses in the Ab-
                                                                     stract Domain, dropping to 8.24% (roughly half of GPT-
We evaluate state-of-the-art LLM provers on M ATHLI -                Reasoning’s 18.61%). Qualitative inspection suggests dis-
B L EMMA benchmark to measure their ability to bridge the            tinct failure modes: we found that GPT’s primary weak-
last-mile formalization gap. Unlike static datasets (e.g.,           ness is hallucination—it frequently attempts to invoke non-

                                                                 7
                      M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Table 3. Main Results (Success@2). Comparison of cumulative              that future formal reasoning systems should prioritize en-
success rates (%) across the three domains. While GPT-Reasoning
performs consistently well, specialized models like Goedel show
                                                                         sembling diverse architectures (e.g., mixing specialized
strong performance on foundational tasks but degrade significantly       small models with reasoning-heavy frontier models) rather
on abstract math.                                                        than relying on a single monolithic prover.

 Model                 Foundational   Applied   Abstract   Total         5. The Remaining Folklore Gap. The union of all models
 GPT                      18.91        12.03     14.17     15.69         solves 37.39%, while applying the 78% human success rate
 GPT-Reasoning            22.44        15.28     18.61     19.39         from our seed-stratified residual audit suggests an indicative
 Kimina                   13.93        7.64       8.52     10.70         solvable fraction near 86%. Although this extrapolation is
 Goedel                   27.42        11.24      8.24     17.70
 DeepSeek-32B             11.00        3.60       3.80      6.98         diagnostic rather than a precise benchmark-level estimate,
 DeepSeek-70B             10.89        3.60       2.87      6.68         the gap shows that M ATHLIB L EMMA remains far from sat-
 Qwen                      1.93        2.63       3.15      2.46         urated and continues to expose limitations of current neural
 Union (All Models)       47.48        27.48     30.93     37.39         provers.

                                                                         6. Practical Impact: The Verified Library
existent APIs or lemmas, reflecting a lack of precise library
knowledge. In contrast, Goedel, having been fine-tuned on                Beyond benchmarking model capabilities, M ATHLI -
                                                                         B L EMMA fulfills a more fundamental scientific goal: the
Mathlib, rarely hallucinates syntax but suffers from logical
failures in abstract settings, unable to construct the deep              automated expansion of formal knowledge. Our pipeline
structural arguments required when “memorized” patterns                  produces a large-scale repository of Lean-checked proofs
do not apply. DeepSeek, despite its strong reputation in in-             that pass the proof-bypass screen, which constitutes a
formal math reasoning, achieves only 6.98% success. This                 durable and reusable asset for the community. This verified
suggests that general mathematical reasoning ability does                library serves two distinct practical functions: first, it acts as
not automatically transfer to formal proving without explicit            an immediately usable reference database for human for-
training on the target library’s syntax and conventions (as              malizers, offering valid proofs for over a thousand missing
seen in Goedel). Meanwhile, Kimina (10.70%), trained on                  folklore facts; second, it functions as a high-quality staging
competition problems (MiniF2F), underperforms Goedel                     area for Mathlib, supplying candidates that can be selec-
(17.70%) on our folklore task. This suggests that library-               tively curated for upstreaming when they are non-redundant,
centric fine-tuning (Goedel) is more effective for folklore              stated at the right level of generality, named consistently
mining than competition-centric RL (Kimina), as folklore                 with the surrounding API, placed appropriately, and written
lemmas resemble standard library code more than tricky                   in a maintainable proof style.
olympiad puzzles.
                                                                         6.1. The Proved Subset
2. Universal Benefit of Test-Time Compute. Test-time
compute yields universal gains. Comparing GPT and GPT-                   Using the Prover module (Section 3.2.4), we successfully
Reasoning, we observe a consistent performance gain of 3.3–              synthesized 1,506 verified proofs from 4,028 non-trivial
4.4 percentage points across domains. Unlike specialized                 type-checked statements. A released proof is counted only
models which exhibit high variance, this uniform improve-                if the self-contained Lean file elaborates without error-
ment suggests that reasoning budget effectively facilitates              level diagnostics and the generated proof code passes our
self-correction regardless of domain specificity.                        proof-bypass screen. This screen strips Lean comments
                                                                         and rejects two classes of bypass artifacts: incomplete-
3. Efficiency of Reasoning Distillation. Comparing                       proof placeholders (sorry, admit, or Lean’s correspond-
open-weight models reveals that scale is not all you need.               ing sorryAx) and model-introduced top-level declara-
DeepSeek-32B (6.98%) substantially outperforms Qwen                      tions that could supply new assumptions or black-box facts
(2.46%), while remaining close to the 70B variant (6.68%).               (axiom, constant, or opaque). Thus the proof must
This suggests that reasoning distillation and Lean-specific              be constructed from the supplied Mathlib context and Lean-
proof behavior may matter more than parameter scale alone                checked generated proof terms, rather than from incomplete
in this setting.                                                         placeholders, newly introduced assumptions, or black-box
4. Diversity is More Valuable than Scale. Perhaps the                    declarations.
most critical observation is the massive gap between the                 We release these proofs as a comprehensive repository of
best individual model (19.39%) and the Union performance                 machine-checked folklore, organized by domain and topic.
(37.39%). The fact that the union coverage is nearly twice               By covering a diverse range of folklore-style statements,
that of the strongest single model implies that these models             this repository can serve as a searchable auxiliary layer for
are highly orthogonal: Goedel solves problems that GPT                   downstream projects.
misses, and vice versa. This diversity gain strongly suggests

                                                                     8
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

6.2. Upstreaming to Mathlib                                         lib curation and therefore are plausible components of the
                                                                    auxiliary folklore layer such an ablation would use.
To evaluate whether the generated lemmas can meet the stan-
dards of a real formal-mathematics library, we conducted
                                                                    6.3. Cost and Practicality
a small pilot upstreaming effort to Mathlib. We selected
six generated, Lean-verified lemmas across several areas of         We also tracked approximate paid API cost. Discovery,
analysis, measure theory, and probability, manually cleaned         Judge, and Formalizer cost about $200 for 4,028 non-trivial
their names and proof style, and submitted them as Math-            type-checked statements, or roughly $0.05 per statement.
lib pull requests. At the time of writing, three of these six       Proving cost about $500; after the proof-bypass screen,
lemmas have been merged into Mathlib, one was rejected as           it yielded 1,506 released Lean proofs, or roughly $0.33
redundant with existing library material, and two were not          per proof for proving alone and $0.46 when amortizing
pursued further within the paper timeline.                          the full $700 pipeline cost. These figures exclude author
We emphasize that this pilot was intentionally small. Al-           curation, local serving costs for open-weight models, and
though our pipeline produced 1,506 Lean-checked proofs              Mathlib maintainer review. Because the upstreaming pilot
that pass the proof-bypass screen, submitting all of them           deliberately submitted only six curated lemmas, the three
directly to Mathlib would not be an appropriate integration         merged PRs are a high-standard validation signal rather than
strategy. Mathlib is maintained by a volunteer community,           a denominator for cost-per-merged-lemma.
and bulk submission of AI-generated lemmas would impose
substantial review burden without prior coordination. More-         7. Conclusion
over, Lean checking and proof-bypass screening establish
formal validity of the generated proof artifacts in a fixed         We introduced M ATHLIB L EMMA, to our knowledge, the
Lean environment, but Mathlib upstreaming additionally              first LLM-based modular pipeline capable of proactively
requires curation: a lemma should be non-redundant, stated          discovering and formalizing mathematical folklore. By sys-
at the right level of generality, named consistently with the       tematically mining the “connective tissue” of mathematics,
surrounding API, placed in the appropriate file, and written        our work establishes a constructive methodology toward
in an acceptable proof style. We therefore use selective            addressing the last-mile gap in formal libraries. The effi-
upstreaming as a high-standard validation signal rather than        cacy of this framework is validated by two critical pieces
as a bulk-ingestion mechanism.                                      of evidence: first, the successful selective upstreaming
                                                                    of generated proofs into Mathlib provides external evi-
The three merged examples illustrate the kind of reusable           dence that selected outputs can meet expert library stan-
folklore facts surfaced by the pipeline:                            dards; second, a rigorous human audit reveals that 78% of
Analysis. A monotonicity lemma for the Grönwall bound,             a seed-stratified sample of model-unsolved residuals are
stating that the Grönwall time-bound function is monotone          nonetheless provable, providing evidence that many gener-
in time under nonnegativity assumptions on its parameters.          ated model-unsolved challenges are mathematically sound.
Such facts are routinely used when propagating differential-        Complementing the framework, we released the M ATH -
                                                                    LIB L EMMA benchmark, which quantifies the distinct gap
inequality bounds.
                                                                    between human mathematical intuition and current formal
Measure theory. A compatibility lemma for kernels, stating          reasoning capabilities.
that restricting a constant kernel to a measurable set agrees
with the constant kernel associated with the restricted mea-        We acknowledge four limitations and corresponding direc-
sure. This is a small but useful API lemma connecting               tions for future work. First, our novelty filters rely mainly on
kernel restriction and measure restriction.                         syntactic uniqueness and lightweight automation, so seman-
                                                                    tically equivalent restatements of existing Mathlib facts may
Probability. An almost-everywhere congruence lemma for              remain; stronger checks should combine library retrieval,
central moments, stating that two real-valued random vari-          semantic search, and proof-based equivalence tests. Second,
ables that are equal almost everywhere have the same central        kernel elaboration verifies that a repaired statement is well
moment with respect to the same measure and moment order.           formed, but not that it preserves the original mathematical
This captures the standard principle that such probabilistic        intent; future repair loops could add semantic-consistency
quantities depend only on the almost-everywhere equiva-             checks, in the spirit of autoformalization alignment meth-
lence class of the random variable.                                 ods (Gao et al., 2025). Third, M ATHLIB L EMMA is tied to
These examples are given in Appendix E. A controlled                a fixed Lean/Mathlib snapshot and should be periodically
retrieval-augmented downstream ablation remains a valu-             rechecked as APIs evolve, with additional normalization for
able next step. The present pilot serves a different purpose:       implicit type, universe, and typeclass choices. Finally, Lean-
it shows that selected generated lemmas can survive Math-           checked proofs still require curation for naming, placement,
                                                                    generality, documentation, and proof style.

                                                                9
                   M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Impact Statement                                                        Dong, K., Mahankali, A., and Ma, T. Formal theorem
                                                                          proving by rewarding LLMs to decompose proofs hierar-
This paper presents work whose goal is to advance the field               chically. arXiv Preprint, 2024.
of Machine Learning. A potential risk is that automatically
generated lemmas could impose review burden or intro-                   Dos Santos, M., de Saxcé, H., Wang, H., Wang, R., Bakšys,
duce misleading artifacts if used without curation. We miti-              M., Ünsal, M., Liu, J., Liu, Z., and Li, J. Kimina Lean
gate this by requiring Lean kernel checking, a proof-bypass               Server: A high-performance Lean server for large-scale
screen, and selective human review before upstreaming. We                 verification. Mathematical Reasoning and AI Workshop
do not advocate bulk submission of generated lemmas to                    at NeurIPS, 2025.
Mathlib without coordination with maintainers.
                                                                        Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and
                                                                          Dong, B. Herald: A natural language annotated Lean 4
Acknowledgements
                                                                          dataset. In Proceedings of the International Conference
This work is supported in part by the US National Science                 on Learning Representations, 2025.
Foundation under the awards III-2128019, SLES-2331904,
and CAREER-2442098, the Commonwealth Cyber Initia-                      Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q.,
tive’s Central Virginia Node under the award VV-1Q26-001,                Xu, R., Zhang, R., Ma, S., Bi, X., et al. DeepSeek-R1
a Cisco Faculty Research Award, and an Nvidia academic                    incentivizes reasoning in LLMs through reinforcement
grant program award.                                                      learning. Nature, 2025.

                                                                        Hubert, T., Mehta, R., Sartran, L., Horváth, M. Z., Žužić, G.,
References                                                                Wieser, E., Huang, A., Schrittwieser, J., Schroecker, Y.,
                                                                          Masoom, H., et al. Olympiad-level formal mathematical
Achim, T., Best, A., Bietti, A., Der, K., Fédérico, M., Gukov,
                                                                          reasoning with reinforcement learning. Nature, 2026.
  S., Halpern-Leistner, D., Henningsgard, K., Kudryashov,
  Y., Meiburg, A., et al. Aristotle: IMO-level automated                Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J.,
  theorem proving. arXiv Preprint, 2025.                                  Xia, M., Chen, D., Arora, S., et al. Goedel-Prover: A fron-
                                                                          tier model for open-source automated theorem proving.
Alhessi, Y., Einarsdóttir, S. H., Granberry, G., First, E., Jo-
                                                                          In Proceedings of the Conference on Language Modeling,
  hansson, M., Lerner, S., and Smallbone, N. Lemmanaid:
                                                                          2025.
  Neuro-symbolic lemma conjecturing. arXiv Preprint,
  2025.                                                                 Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao, H.,
                                                                          Jiang, L., Geng, Y., Ge, J., Sun, J., et al. Goedel-Prover-
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,              V2: Scaling formal theorem proving with scaffolded data
  Radev, D., and Avigad, J. ProofNet: Autoformalizing                     synthesis and self-correction. In Proceedings of the Inter-
  and formally proving undergraduate-level mathematics.                   national Conference on Learning Representations, 2026.
  arXiv Preprint, 2023.
                                                                        Liu, H., Sun, J., Li, Z., and Yao, A. C. ProofAug: Efficient
Borkar, V. S. Stochastic Approximation: A Dynamical                       neural theorem proving via fine-grained proof structure
  Systems Viewpoint. Hindustan Book Agency, 2009.                         analysis. In Proceedings of the International Conference
                                                                          on Machine Learning, 2025.
Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie, A., Jin,
  X., Jin, X., Li, C., Ma, K., et al. Seed-Prover: Deep and             Masser, D. W. Open problems. In Proceedings of the
  broad reasoning for automated theorem proving. arXiv                   Symposium on Analytic Number Theory, 1985.
  Preprint, 2025.
                                                                        Math-Inc. Introducing Gauss, an agent for autoformaliza-
Chervonyi, Y., Trinh, T. H., Olšák, M., Yang, X., Nguyen,              tion. https://www.math.inc/gauss, 2025.
  H. H., Menegali, M., Jung, J., Kim, J., Verma, V., Le,
  Q. V., and Luong, T. Gold-medalist performance in solv-               Mochizuki, S. Report on discussions, held during the pe-
  ing Olympiad geometry with AlphaGeometry2. Journal                     riod March 15–20, 2018, concerning Inter-universal Te-
  of Machine Learning Research, 2025.                                    ichmüller Theory (IUTch). https://ww w.kurims
                                                                         .kyoto-u.ac.jp/˜ motizuki/Rpt2018.pdf,
Davis, K. J. Gödel’s Poetry. arXiv Preprint, 2025.                      2019.

de Moura, L. and Ullrich, S. The Lean 4 theorem prover                  Mochizuki, S. Inter-universal Teichmüller Theory I: Con-
  and programming language. In International Conference                  struction of Hodge Theaters. Publications of the Research
  on Automated Deduction, 2021.                                          Institute for Mathematical Sciences, 2021a.

                                                                   10
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Mochizuki, S. Inter-universal Teichmüller Theory II: Hodge–           ommunity .github.io/archive/stream/41
 Arakelov-theoretic evaluation. Publications of the Re-                2902-Polynomial-Freiman-Ruzsa-conje
 search Institute for Mathematical Sciences, 2021b.                    cture/topic/Project.20completed%21.2
                                                                       0.20Thoughts.20and.20reflections.3F.
Mochizuki, S. Inter-universal Teichmüller Theory III:                 html, 2023.
 Canonical splittings of the Log-theta-lattice. Publica-
 tions of the Research Institute for Mathematical Sciences,          The mathlib Community. The Lean mathematical library.
 2021c.                                                                In Proceedings of the ACM SIGPLAN International Con-
                                                                       ference on Certified Programs and Proofs, 2020.
Mochizuki, S. Inter-universal Teichmüller Theory IV: Log-
 volume computations and Set-theoretic foundations. Pub-             Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jen-
 lications of the Research Institute for Mathematical Sci-             nings, M., Thakur, A., and Chaudhuri, S. PutnamBench:
 ences, 2021d.                                                         Evaluating neural theorem-provers on the Putnam mathe-
                                                                       matical competition. In Advances in Neural Information
Oesterlé, J. Nouvelles approches du “théorème” de Fermat.           Processing Systems, 2024.
  Séminaire Bourbaki, 1988.
                                                                     Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and Ye,
Onda, N., Kasaura, K., Oriike, Y., Taniguchi, M., Sannai, A.,          K. HILBERT: Recursively building formal proofs with
  and Sonoda, S. LeanConjecturer: Automatic generation                 informal reasoning. In Proceedings of the International
  of mathematical conjectures for theorem proving. arXiv               Conference on Learning Representations, 2026.
  Preprint, 2025.
                                                                     Wang, H., Xin, H., Zheng, C., Liu, Z., Cao, Q., Huang,
OpenAI. Introducing GPT-5.1 for Developers. https:                    Y., Xiong, J., Shi, H., Xie, E., Yin, J., Li, Z., and Liang,
 //openai.com/index/gpt-5-1-for-devel                                 X. LEGO-Prover: Neural theorem proving with growing
  opers/, 2025a.                                                      libraries. In Proceedings of the International Conference
                                                                      on Learning Representations, 2024.
OpenAI. GPT-5.1 Instant and GPT-5.1 Thinking System
  Card Addendum. https://openai.com/index                            Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Dos San-
 /gpt-5-system-card-addendum-gpt-5-1/,                                tos, M., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
  2025b.                                                              Kimina-Prover preview: Towards large formal reason-
                                                                      ing models with reinforcement learning. arXiv Preprint,
Ospanov, A., Farnia, F., and Yousefzadeh, R. APOLLO:                  2025.
  Automated LLM and Lean collaboration for advanced
                                                                     Xie, Z., Liu, X., and Zhang, S. MathlibPR: Pull request
  formal reasoning. In Advances in Neural Information
                                                                       merge-readiness benchmark for formal mathematical li-
  Processing Systems, 2025.
                                                                       braries. arXiv Preprint, 2026.
Rittberg, C. J. Intellectual humility in mathematics. Syn-           Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
  these, 2021.                                                         Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical
Scholze, P. and Stix, J. Why ABC is still a conjecture.                report. arXiv Preprint, 2025.
  https://ww w.math.uni-bonn.de/people/                              Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M., Zhang,
  scholze/WhyABCisStillaConjecture.pdf,                                Y., Yuan, Z., Xin, H., Huang, W., et al. FormalMATH:
  2018.                                                                Benchmarking formal mathematical reasoning of large
                                                                       language models. arXiv Preprint, 2025.
Sivaraman, A., Sanchez-Stern, A., Chen, B., Lerner, S., and
  Millstein, T. Data-driven lemma synthesis for interac-             Zhang, S. Towards formalizing reinforcement learning the-
  tive proofs. Proceedings of the ACM on Programming                   ory: A Robbins-Siegmund approach. In Proceedings of
  Languages, 2022.                                                     the Reinforcement Learning Conference, 2026.
Tao, T. The probabilistic heuristic justification of the ABC         Zheng, K., Han, J. M., and Polu, S. miniF2F: A cross-system
  conjecture. https://terrytao.w ordpress.c                            benchmark for formal Olympiad-level mathematics. In
  om/2012/09/18/the-probabilistic-heuri                                Proceedings of the International Conference on Learning
  stic-justification-of-the-abc-conject                                Representations, 2022.
  ure/, 2012.
                                                                     Zhou, Y., Zhao, J., Zhang, Y., Wang, B., Wang, S., Chen,
Tao, T. Comment in “Project completed! Thoughts and                    L., Wang, J., Chen, H., Jie, A., Zhang, X., et al. Solving
  reflections?”. Lean Zulip archive, Polynomial Freiman–               formal math problems by decomposition and iterative
  Ruzsa conjecture stream. https://leanprover-c                        reflection. arXiv Preprint, 2025.

                                                                11
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Algorithm 1 Four-Stage Modular Lemma Generation Pipeline
Input :Set of seed contexts T (Mathlib files)
Output :Set of verified pairs {(S, P )}
// Stage 1: Discovery (Context-Aware Generation)
foreach context C ∈ T do
    R ← LLM(C) ;                                                                    // Brainstorm raw candidates
    Split R into individual raw statements {r1 , r2 , . . . , rn } based on markers
    // Each ri preserves imports and namespaces from C

// Stage 2: Judge (Semantic Filtering)
foreach raw statement ri do
    y ← LLM(ri ) ;                                                                 // Ignore syntax, judge math
    if y predicts correct then
         Add ri to queue Qformalize

// Stage 3: Formalizer (Syntax Repair)
foreach candidate sraw ∈ Qformalize do
    S ← sraw ;
    H ←∅;                                                                                     // Initialize history
    for t = 1 to Trepair do
        E ← L EAN S ERVER .C HECK(S) ;                                                     // Check S with imports
        if E is empty then
            Add S to Qprover ;                                                                   // S is well-formed
            break
        H ← Append(H, S, E) ;                                                         // Record failure & errors
        S ← LLM(H) ;                                                                            // Repair syntax

// Stage 4: Prover (Proof Generation & Repair)
foreach statement S ∈ Qprover do
    H ←∅;
    for k = 0 to Krepair do
        P ← LLM(S, H) ;                                          // Generate full lemma w/ proof
        E ← L EAN S ERVER .C HECK(P ) ;       // Check if P is a valid proof of S (with imports)
        if E is empty and P ROOF B YPASS S CREEN(P ) then
            Yield verified pair (S, P ) break
        H ← Append(H, P, E) ;                                    // Feedback: Code + Error Msgs




A. Implementation Details and Pseudocode
This appendix provides the precise execution logic of our pipeline (Algorithm 1) and documents the runtime configurations
used in our experiments to ensure reproducibility.

A.1. Pipeline Pseudocode
Algorithm 1 details the interaction logic between the four modules, the persistent queues, and the Lean server.

A.2. Experimental Configurations
Methodological Constraints. We do not fine-tune or update the parameters of any model. All adaptations are performed
at inference time via (i) stage-specific prompts, (ii) marker-based structured output extraction, (iii) decoding controls (e.g.,
temperature/top-p), and (iv) Lean-in-the-loop generate–verify–repair using compiler diagnostics. Crucially, we use Lean
solely for verification and error feedback; no external retrieval (e.g., RAG or code search) is used during evaluation.
This setting strictly evaluates the model’s internalized mathematical knowledge and reasoning capabilities.

                                                              12
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Overview and Environment. Our pipeline is implemented in Python, utilizing standard libraries for asynchronous
job management and LLM interaction. Key dependencies include weave (0.52.17) and wandb (0.23.0) for experiment
tracking, persist-queue (1.1.0) for robust inter-module message passing, and vllm for serving open-weight models.
The Lean 4 verification backend consists of a customized Lean server wrapper exposing an HTTP endpoint, running on
Lean v4.25.0-rc2. All candidates are validated by the Lean 4 kernel: statements must type-check, and proofs (when
present) must pass kernel proof checking. We interact with the Lean server in a stateless manner to ensure reproducibility.
For each verification request, we construct a self-contained Lean file (including necessary imports and open namespaces)
and send the full context to the server. This isolates the verification of each candidate, preventing state pollution from
previous failed attempts or other lemmas. For statement-only candidates, acceptance requires no error-level diagnostics
during elaboration/checking. For proof artifacts, acceptance additionally requires passing the proof-bypass screen defined in
Section 3.2.4. To accommodate complex elaboration and compilation tasks, we configure the Lean client with a generous
timeout (timeout=6000 seconds) to prevent premature termination of valid proofs.
The released artifact is version-pinned by the Lean toolchain and Mathlib manifest: all checks are performed under Lean
v4.25.0-rc2 and a fixed Mathlib revision. The repository is configured with relaxedAutoImplicit = false and
Mathlib’s standard linter set, and the benchmark/proof files are organized as standalone topic slices rather than as a dense
custom import graph, allowing future refreshes to be rechecked locally as Lean/Mathlib evolves.

LLM Inference Configuration. We utilize OpenAI-compatible chat completion endpoints for all LLM-backed modules.
Unless otherwise specified, we employ the following default settings to ensure sufficient capacity for mathematical reasoning:

   • Token budget: We set max completion tokens to 50,000 across all stages to allow for long intermediate
     reasoning and proof generation.
   • Sampling parameters: For the Discovery stage, we use exploratory sampling (temperature=1.0, top p=1.0).
     For the Prover stage, we adopt more conservative settings for open-weight models (e.g., temperature=0.6,
     top p=0.95) to reduce hallucinations, while relying on default parameters for frontier models (e.g., GPT-5.1) unless
     specific reasoning efforts are required (e.g., reasoning effort="low").

Stage-Specific Hyperparameters.       We detail the exact logic and runtime configurations for each stage below.

   • Discovery (Generation): We input the full text of the seed Mathlib file into the model context without truncation.
     We typically run this stage with high concurrency (e.g., 64 threads) using GPT-5.1. The extraction logic relies on the
     marker "brainstormed mathlib lemmas".
   • Splitting: Raw generations are split into individual lemma snippets using regex matching on lemma or theorem
     keywords. Critical context, including module-level imports and open namespaces, is preserved for each snippet to
     maintain compilation validity.
   • Judge (Semantic Filtering): We utilize GPT-5.1 with default sampling parameters and max tokens=50,000. This
     module runs with high concurrency (up to 100 threads). We use a precise parsing rule: a candidate is accepted if and
     only if the last non-empty line of the model’s response starts with "correct" (case-insensitive).
   • Formalizer (Repair Loop): We employ GPT-5.1 (default sampling, max tokens=50,000) to perform syntax
     repair. The repair loop runs for a maximum of T = 10 trials with a concurrency of 30 workers. In each iteration,
     the prompt receives the full history of the failed code combined with compiler error messages. We enforce a strict
     filter: candidates are rejected if the Lean server returns any diagnostics with severity="error" or if the error
     message indicates a duplicate declaration (e.g., containing “has already been declared”). The extraction marker is set to
     "error-free code".
   • Prover (Proof Search): For our main benchmarks, we allow up to Krepair = 2 repair rounds after the initial proof
     attempt. The extraction marker is "### Complete Lean 4 Proof". To ensure fair evaluation across different
     backends (e.g., Goedel, DeepSeek), we inject necessary environment configurations (such as import Aesop, open
     BigOperators, and set option maxHeartbeats 0) when required by specific models. We also employ a
     triviality filter using aesop: lemmas that can be solved immediately by replacing sorry with the aesop tactic
     (using default configuration and rule sets) are flagged as trivial.

                                                             13
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

Artifacts and Data Management. We use file-based persistent queues to manage state, ensuring that the pipeline can
resume from interruptions without data loss. The artifact directory structure follows the pipeline stages: MathlibLemma
(raw candidates), MathlibLemmaCorrect (judged), MathlibLemmaCompilable (type-checked statements), and
MathlibLemmaProved (verified proofs).

B. Prompt Templates and Extraction Logic
This appendix documents the exact prompt templates used by the Discovery, Judge, Formalizer, and Prover modules. To
ensure reproducibility, we detail not only the prompt text but also the runtime variable instantiation and the extraction logic.

B.1. Discovery Module (Generation)
Input Specification:

   • {LEAN FILE}: A single Mathlib source file corresponding to a specific topic. It typically contains the core definitions
     and existing lemmas for that topic.
   • {MARKER}: The extraction marker, set to brainstormed mathlib lemmas.

{LEAN_FILE}
The lean file above contains many basic lemmas, but not all of them. Many are still
missing. I am frequently surprised that some very obvious lemmas are not formalized yet.
Try to figure out those lemmas. You can guess based on the names of existing ones or try
to make analogues of existing ones. When you brainstorm the lemmas, think not only about
the topic of the file itself but also about how it may interact with topics from other
files. You will write the statements of the lemmas in Lean. Do not try to prove the
lemmas at all; just put a sorry. Generate at least 100 lemmas. Make sure the lemmas you
generate are diverse and not just repeating each other. Make sure they are not merely
renamings of existing lemmas in Mathlib. Make sure they cannot be trivially proved by
just using simp, trivial, or aesop. You can sketch your plan for brainstorming lemmas
first in natural language. After your thinking process, start a new line and write down
"{MARKER}". You will then start with "import Mathlib" and do not add any other imports.
Do not add a namespace or section. Then write down the lemmas you figure out.

Post-processing: We strip any non-code preamble and extract the Lean snippet appearing after the marker line; if code
fences are present, we keep the last fenced Lean block.

B.2. Judge Module (Semantic Correctness)
Input Specification: {LEAN STATEMENT} is instantiated with a single-lemma Lean snippet. The snippet usually contains
sorry and may not yet be compilable.
{LEAN_STATEMENT}
You are given a statement in Lean. Use your best judgement to decide whether this
statement is mathematically correct. You do not need to care whether the Lean syntax is
correct or whether you can prove it in Lean. Outline your rationale. After your thinking
process, at the end of your response, start a new line and use ’correct’ or ’wrong’ to
indicate your assessment.

Decision Rule: The candidate is accepted if and only if the last non-empty line of the response starts with correct
(case-insensitive).

B.3. Formalizer Module (Iterative Repair)
Input Specification:

   • {HISTORY}: A running transcript accumulating pairs of (previous code, compiler diagnostics).
   • {MARKER}: The extraction marker, set to error-free code.

                                                              14
                 M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics


{HISTORY}
Try your best to fix the errors. You are using Lean 4. Do not overthink. Try to add
missing stuff first in the errors. Never try to prove the lemma. There is no need to
prove it; just put a sorry. Focus on making the lemma statement compilable. Do not make
any assumption on the environment variables. Make sure the lemma statement is
self-contained. You can assume every related file is already imported, so do not add any
new import. However, the namespace may not be opened properly. At the end of your
response, start a new line with "{MARKER}" and then write down the error-free lean code.

Loop Protocol: We extract the code following {MARKER}. If compilation fails, the error messages are appended to
{HISTORY} for the next turn (t ← t + 1). The loop terminates on success (zero errors) or upon reaching budget T .

B.4. Prover Module (Proof Generation)
Input Specification:

  • {LEMMA WITH SORRY}: The type-checked lemma statement.

  • {HISTORY}: Transcript of previous failed proof attempts and errors.
  • {MARKER}: The extraction marker, set to ### Complete Lean 4 Proof.

{LEMMA_WITH_SORRY}
Complete the proof in Lean. Below is your previous failed trials and the corresponding
errors.
{HISTORY}
You are using Lean 4. Make sure you use correct API and make sure the solution you
generate can compile. You can assume every related file is already imported, so do not
add any new import. However, the namespace may not be opened properly.
Before producing the Lean 4 code to formally prove the given theorem, provide a detailed
proof plan outlining the main proof steps and strategies. The plan should highlight key
ideas, intermediate lemmas, and proof structures that will guide the construction of the
final formal proof. At the end of your response, start a new line with "{MARKER}" and
then write down the error-free lean code with complete proof.
Write the complete lemma with proof including everything you see at the beginning of this
message. Do not just write the proof.

Verification Rule: A proof is accepted if and only if the self-contained Lean file returns no diagnostics of severity error
and the extracted model-generated proof code passes the proof-bypass screen. The screen strips Lean comments and
rejects incomplete-proof placeholders (sorry, admit, sorryAx) and model-introduced top-level axiom, constant,
or opaque declarations.

B.5. Robust Output Extraction
To handle the stochastic nature of LLM outputs, we enforce a deterministic extraction pipeline:

 1. Marker splitting: We locate the last occurrence of the stage-specific marker (case-insensitive) to ignore any preliminary
    “chain-of-thought” or conversational filler.
 2. Code block parsing: From the text following the marker, we look for fenced code blocks (‘‘‘lean ...                ‘‘‘).
    If found, we extract the content of the last code block. If no fences are found, we take the raw text.

This ensures that the system reliably captures the final “clean” code intended by the model.




                                                            15
                   M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

C. Benchmark Statistics and Detailed Results
C.1. Evaluation Metrics
We report the Success@t metric, defined as the cumulative percentage of instances solved using at most t repair turns
(where t ∈ {0, 1, 2}):

   • Success@0 (One-shot): Success in the initial generation (0 repairs).
   • Success@1: Cumulative success after up to 1 repair round.
   • Success@2 (Total): Cumulative success after up to 2 repair rounds. This corresponds to the total system performance
     reported in our figures.

C.2. Performance Breakdown by Domain
We provide the fine-grained performance breakdown for each domain in Figures 3, 4, and 5. These figures detail the success
rates at each stage of the repair loop (Success@0, Success@1, Success@2), highlighting the impact of iterative refinement.

                                                                                         Foundational Domain

                                                                                                                                                                 Success@0 (One-shot)
                                                                                                                                                                 Success@1
                                       30                                                                                                                        Success@2 (Total)
                                                                                                                         27.4


                                       25                                                                         24.0
                                                                                22.4
                    Success Rate (%)




                                       20                 18.9           19.1
                                                                                                           17.7

                                                   15.9
                                       15                         13.8                              13.9


                                            11.4                                             11.1                                            11.0                10.9
                                                                                                                                      10.3                10.3
                                       10                                                                                       9.2
                                                                                                                                                    8.7
                                                                                       7.1


                                       5

                                                                                                                                                                              1.6 1.9
                                                                                                                                                                        1.1

                                       0
                                               GPT               GPT-Reasoning          Kimina               Goedel              DS-32B              DS-70B               Qwen


Figure 3. Performance on Foundational Domain. This domain comprises standard mathematical structures (e.g., lists, real analysis
basics) that are well-represented in the training data. Here, “GPT” denotes GPT-5.1, “GPT-Reasoning” denotes GPT-5.1 with low
reasoning, “DS-32B” denotes DeepSeek-R1-Distill-Qwen-32B, and “DS-70B” denotes DeepSeek-R1-Distill-Llama-70B. Goedel-Prover
shows the strongest Foundational-domain performance, with Success@2 above 27%. The significant contribution of “0-trial” (One-shot)
success indicates that frontier models have internalized many foundational definitions, and general-purpose open-weight models (e.g.,
DeepSeek) struggle with basic formalization, with scaling from 32B to 70B yielding no performance gain.




                                                                                                           16
                   M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

                                                                                                      Applied Domain

                                                                                                                                                              Success@0 (One-shot)
                                       17.5                                                                                                                   Success@1
                                                                                                                                                              Success@2 (Total)
                                                                                   15.3
                                       15.0

                                                                            13.3

                                       12.5                 12.0
                    Success Rate (%)


                                                                                                                           11.2
                                                     10.4
                                       10.0                           9.7

                                                                                                                     8.6
                                               8.3
                                                                                                       7.6
                                        7.5
                                                                                                 6.8

                                                                                                              5.5

                                        5.0
                                                                                           4.1
                                                                                                                                        3.4 3.6         3.4 3.6
                                                                                                                                  2.7             2.9
                                                                                                                                                                                 2.6
                                        2.5
                                                                                                                                                                           1.7
                                                                                                                                                                     1.1


                                        0.0
                                                     GPT            GPT-Reasoning           Kimina             Goedel               DS-32B         DS-70B              Qwen


Figure 4. Performance on Applied Domain. This domain includes fields like probability and information theory, where intuitive concepts
often require complex type-class constraints. This domain generally depresses success rates relative to the Foundational domain and
remains challenging across models, but models with stronger reasoning, most notably GPT-Reasoning, perform comparatively better.



                                                                                                  Abstract Domain

                                                                                                                                                              Success@0 (One-shot)
                                                                                                                                                              Success@1
                                       20                                                                                                                     Success@2 (Total)
                                                                                  18.6



                                                                           16.1

                                       15
                    Success Rate (%)




                                                           14.2

                                                    12.6

                                                                    11.0

                                       10     9.3
                                                                                                      8.5                  8.2


                                                                                                6.3                 6.5


                                        5
                                                                                          3.7                3.9                        3.7 3.8
                                                                                                                                  3.2                                            3.1
                                                                                                                                                              2.9          2.7
                                                                                                                                                        2.5
                                                                                                                                                  2.0               1.9



                                        0
                                                    GPT            GPT-Reasoning           Kimina             Goedel               DS-32B          DS-70B              Qwen


Figure 5. Performance on Abstract Domain. This domain covers category theory and differential geometry. Specialized library models
such as Goedel degrade sharply relative to the Foundational domain, while GPT-5.1 and GPT-Reasoning remain the strongest models in
this domain.


C.3. Pass@16 Evaluation for a Small Lean Prover
To complement the sequential Success@K evaluation in the main text, we additionally evaluate Goedel-Prover-V2-8B under
a standard Pass@16 protocol. These Pass@16 numbers should be interpreted as a small-model independent-sampling stress
test, not as a direct comparison with Table 3. Table 3 reports sequential repair-loop Success@2 for Goedel-Prover-V2-32B
and other models, whereas this appendix uses the much smaller 8B variant with 16 independent attempts and no repair
feedback. Thus, the experiment asks whether repeated parallel sampling from a small Lean-specialized prover already
closes a substantial part of the benchmark. For consistency with the main benchmark, we apply the same triviality filter used
in Section A.2, excluding statements that are solved immediately by aesop. The resulting evaluation set contains 4,028
non-trivial type-checked statements.

                                                                                                             17
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

                Table 4. Pass@16 results for Goedel-Prover-V2-8B on the non-trivial M ATHLIB L EMMA benchmark.

                                          Domain          Solved     Total   Pass@16
                                          Foundational      1        1809     0.06%
                                          Applied           7        1139     0.61%
                                          Abstract          5        1080     0.46%
                                          Overall           13       4028     0.32%



The results remain uniformly low, suggesting that the benchmark is challenging even when a small Lean-specialized prover
is allowed multiple independent proof attempts per statement. Together with the main Success@2 results, this supports the
same qualitative conclusion: M ATHLIB L EMMA is not saturated either by short sequential repair from stronger provers or by
independent sampling from a small specialist prover.

D. Supplementary Details for the Validity Audit
Failure modes among model-unsolved residuals. In Section 4.3, we reported that a minority of the audited instances
remained unproven even by human experts. To understand the root causes of these failures, we conducted a deep-dive
analysis on all 31 audited instances that remained unproven by human experts. Our analysis reveals that failures typically
fall into three distinct categories, with Missing Hypotheses being the dominant factor (accounting for 81% of failures).


  1. Missing hypotheses or underspecification (25/31, 81%). These statements capture a plausible mathematical intuition
     but omit necessary preconditions or dependencies. Common omissions include non-emptiness, non-degeneracy, integra-
     bility, measurability, continuity, finite-dimensionality, or explicit relationships between objects that are mathematically
     linked but introduced as independent Lean parameters.

  2. False as stated (5/31, 16%). These statements appear to be genuinely false under Lean’s precise interpretation, often
     because of degenerate default cases, incompatible typeclass assumptions, or an overgeneralization of a fact that only
     holds under additional structure.

  3. Hard technical formalization gap (1/31, 3%). One instance appears to express a plausibly true mathematical fact, but
     the required formal proof would require substantial auxiliary development or a more careful reformulation beyond the
     scope of the audit.


This breakdown highlights that the primary challenge for LLMs is not “imagining false math”, but rather mastering the
strict accounting of conditions and dependencies required by formal systems.

Held-out residual provability check. The 138-instance audit in Section 4.3 is our main manual estimate of residual
validity. To check that this estimate was not an artifact of that particular seed-stratified sample, we performed an additional
held-out audit on five seed files. From each seed file, we selected up to 20 non-trivial type-checked statements that compiled
but were not proved by any evaluated prover under the Success@2 protocol. Expert formalizers then attempted to prove
these statements in the same open-book setting as Section 4.3. They proved 79 of 94 statements (84.0%). The mean per-seed
success rate was 83.7%, with sample standard deviation 4.6%; a Wilson 95% confidence interval for the pooled rate is
75.3–90.1%. This held-out check is not pooled with Table 2, since it uses a different seed-level sampling design. Instead, it
serves as a robustness check: it is statistically compatible with the main residual audit and supports the conclusion that many
model-unsolved, type-checked statements are provable rather than hallucinated.

E. Merged Contributions
This appendix presents the three generated lemmas that were merged into Mathlib after human curation. Table 5 gives
the upstream pull-request identifiers, merge commits, and Mathlib file locations. Each example below is shown with its
mathematical role and the corresponding Lean statement/proof, modulo the surrounding Mathlib imports and namespace
context.

                                                                18
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

  Table 5. Merged Mathlib contributions. The three generated lemmas that were curated by the authors and merged into Mathlib.

 Area              Declaration                       PR         Merge commit     Mathlib file
 Probability       centralMoment congr ae            #31985     d7c53e9          Mathlib/Probability/Moments/Basic.lean
 Measure theory    Kernel.restrict const             #32167     f157c2c          Mathlib/Probability/Kernel/Basic.lean
 Analysis          gronwallBound mono                #32170     1608899          Mathlib/Analysis/ODE/Gronwall.lean


Analysis (gronwallBound mono). This lemma states that the Gronwall-bound expression used in the surrounding
Mathlib development is monotone in the time argument, under nonnegativity assumptions on its parameters. The result
is mathematically routine, but it packages a step that would otherwise require unfolding the definition of the bound and
re-proving monotonicity from the exponential expression. Such monotonicity facts are standard in Gronwall-based estimates,
including stochastic approximation arguments; closely related reasoning appears, for example, in Borkar (2009).
                                               Listing 1. gronwallBound mono.
/-- The Gronwall bound is monotone in time. -/
lemma gronwallBound_mono {δ K ε : R} (hδ : 0 ≤ δ) (hε : 0 ≤ ε) (hK : 0 ≤ K) :
     Monotone (gronwallBound δ K ε) := by
  intro x1 x2 hx
  unfold gronwallBound
  split_ifs with hK0
  · gcongr
  · have hK_pos : 0 < K := by positivity
     gcongr


Measure theory (restrict const). This lemma states a compatibility property between constant kernels and target-
set restriction. A constant kernel ignores its input and always returns the same target measure. After restricting such a kernel
to a measurable target set, the result is still a constant kernel, with the original target measure restricted to that set. This is
a small API bridge between constant kernels and measure restriction, allowing later proofs to rewrite kernel expressions
directly rather than unfold the definitions.
                                                  Listing 2. restrict const.
/-- The restriction of a constant kernel to a measurable set is equal
to the constant kernel of the restricted measure. -/
theorem restrict_const {µ : Measure β} (hs : MeasurableSet s) :
    (Kernel.const α µ).restrict hs = Kernel.const α (µ.restrict s) := by
  ext a
  simp [Kernel.restrict_apply, Kernel.const_apply]


Probability (centralMoment congr ae). This lemma states that central moments are invariant under almost-
everywhere equality. More precisely, if two real-valued random variables X and Y are equal µ-almost everywhere,
then their central moments of the same order with respect to µ are equal. This is a standard probabilistic congruence
principle: quantities defined by integration should depend only on the almost-everywhere equivalence class of the random
variable, not on its values on a null set.
                                            Listing 3. centralMoment congr ae.
/-- Central moments are equal for almost-everywhere equal random variables. -/
lemma centralMoment_congr_ae {X Y : Ω → R} (hXY : X =m [µ] Y) :
  centralMoment X p µ = centralMoment Y p µ := by
simp only [centralMoment, integral_congr_ae hXY]
refine integral_congr_ae ?_
filter_upwards [hXY] with x hx using by simp [hx]



F. Prompt Ablation: Explicit Necessary Conditions
Motivated by the missing-hypotheses failure mode, we ran a small prompt ablation in which the Discovery module was
instructed to explicitly list the necessary hypotheses before producing each formal statement. In this pilot, 123/160 generated

                                                               19
                  M ATHLIB L EMMA: Folklore Lemma Generation and Benchmark for Formal Mathematics

statements compiled. Manual review of all 123 compilable statements found that 117 were provable as stated; among the six
residual failures, only two appeared to be genuine missing-hypothesis cases. For comparison, an old-prompt run on the same
scale also produced 123/160 compilable statements; manual review found seven residual unresolved cases, of which two
appeared to be genuine missing-hypothesis cases. Thus, explicitly prompting for necessary conditions is reasonable and may
slightly improve precision on this pilot, but among compilable statements it did not substantially reduce missing-hypothesis
failures in this small pilot. We therefore leave a systematic prompt redesign to future work.




                                                            20
