                                           ProofSketcher: Hybrid LLM + Lightweight Proof
                                             Checker for Reliable Math/Logic Reasoning
                                                        Kranthi Kommuru                              Kunal Khanvilkar                            Gaurav Parekh
                                                 Automatic Data Processing, Inc               Automatic Data Processing, Inc               Amazon Web Services, Inc
                                                          Atlanta, USA                                Atlanta, USA                              Banglore, India
                                                   kranthi.kommuru@ieee.org                    khanvilkar.s.kunal@ieee.org                  gaurav.parekh4@ieee.org
                                                      0009-0008-7801-1558                         0009-0005-9646-1323                        0009-0000-8438-4678



                                           Abstract—The large language models (LLMs) might produce             other retrieval-augmented system like the LeanDojo/ReProver
arXiv:2604.06401v1 [cs.AI] 7 Apr 2026




                                        a persuasive argument within mathematical and logical fields,          is selective in retrieving premises: large libraries of premises
                                        although such argument often includes some minor missteps,             are chosen with the aim to boost success rates; this selection
                                        including the entire omission of side conditions, invalid infer-
                                        ence patterns, or appeals to a lemma that cannot be derived            uses another key punopuloetry activator (identity-switching)
                                        logically out of the context being discussed. These omissions          [8]. Other efforts address the problem of formalization of
                                        are infamously hard to notice solely out of the text, as even          informal inputs: ProofNet attempts auto-simultaneous auto-
                                        the misconstrued construction still may seem mostly accurate.          formalization and auto-generation of proofs [9], in theory, [10],
                                        Conversely, interactive theorem provers like Lean and Coq have         [11] are geometry solvers that combine systemic deduction
                                        rigorous reliability by ensuring that syntactic and semantic state-
                                        ments only accept statements that can pass all the syntactic and       with learning techniques.
                                        semantic steps in the program which is a small trusted kernel of          In spite of these developments, there is still a practical
                                        the language type-checks with. Despite the fact that this technique    challenge, that is, the average interface would like the model to
                                        provides strong guarantees, it comes at quite a heavy price: the       generate a full proof script or sequence of tactics in one search.
                                        evidence must be completely formalized, and the evidence user or       Where the resulting script fails to compile, the feedback is
                                        a auxiliary search program must provide an avalanche of low-
                                        level information. This paper presents ProofSketcher, a hybrid         too fine-grained (e.g., tactic state) or too coarse (e.g. generic
                                        pipeline where an LLM generates a typed proof sketch in a              timeout), and numerous expensive remedies have to be made.
                                        compact DSL and a lightweight trusted kernel expands the sketch        Furthermore, although external solvers prove handy, the level
                                        into explicit proof obligations.                                       of soundness can be determined only when they are supported
                                           Index Terms—LLM reasoning, proof sketching, lightweight             with verifiable certificates to their outputs [12]. This will
                                        proof checking, proof certificates, formal verification
                                                                                                               encourage reconsideration of the segregation of labor between
                                                                                                               the formal verification engine and the language model.
                                                               I. I NTRODUCTION
                                                                                                                  This paper proposes ProofSketcher, a hybrid design where
                                           Large language models (LLMs) can produce long math and              the LLM writes a typed proof sketch rather than a full formal
                                        logic arguments. But they often make a small invalid step,             proof. The sketch is a structured plan with explicit step types
                                        miss a side condition, or use a lemma that does not follow             (rewrite, case split, induction, contradiction) and typed holes.
                                        from the context. These errors are hard to spot because the            A lightweight kernel expands each sketch node into concrete
                                        text still looks correct. In contrast, interactive theorem provers     proof obligations. Obligations are discharged by (i) a small set
                                        such as Lean and Coq accept a statement only when every step           of trusted inference rules, or (ii) external tools that must return
                                        type-checks against a small trusted kernel [1], [2]. This gives        a proof certificate that a small checker can validate [12]. If any
                                        strong reliability, but it also raises the cost: the proof must be     node fails, the kernel returns structured, localized feedback
                                        fully formal, and the user (or a search tool) must supply many         (missing lemma, failed instantiation, violated precondition,
                                        low-level details.                                                     countermodel), and the LLM edits only the failing node. The
                                           The latest developments seek to close the performance of            key goal is fast repair with a small trusted computing base,
                                        big language models with formal characteristics of theorem             while keeping acceptance sound.
                                        provers. GPT -f [3] illustrates that a language model can                 Contributions of this research is as follows - (1) A typed
                                        produce Is a sequence of proven proofs that are successfully           sketch DSL that makes high-level proof intent explicit while
                                        validated by a checker with Metamath. Prover benchmarks                keeping low-level details checkable. (2) An obligation ex-
                                        have allowed systematic comparisons between various provers            tractor that turns sketch nodes into a fixed set of kernel-
                                        and problem sets [4]. Other directions of study include adding         checkable goals. (3) A certificate-gated solver interface so
                                        more training data: curriculum learning schemes exposing               that automation remains outside the trusted base. (4) An
                                        the model to more complicated statements [5], and synthetic            incremental edit-check loop with node-level caching and tar-
                                        corpora specialized to Lean 4 [6], [7]. One of the bottlenecks         geted repair prompts, designed to reduce repeated whole-proof
                                        still noted is the effective utilization of existing libraries. Some   regeneration.
   The remaining section of this paper is structured in the          structured programs [20], and Proverbot9001 applied learned
following manner. Section II inspires the problem setting and        guidance and search to software verification proofs in Coq
puts the objectives of credible LLM-assisted reasoning into          [21]. Reinforcement learning was also explored for interactive
place. The architectural design of ProofSketcher is drawn in         proving, for example TacticZero in HOL4 [22]. These systems
Section III, and its trust boundary is outlined. Section IV          motivate our repair loop design: search needs feedback that is
elaborates out the proposed methodology, such as certificate-        local and actionable, not only “success/fail”.
directed discharge and localised repair loop and incremental
re-checking. Section V gives empirical findings and compares         D. LLM-based formal theorem proving and benchmarks
with formal reasoning datasets. Section VI addresses the topic          With LLMs, one direction is whole-proof generation in a
of trade-offs, reveals constraints, and makes a discussion           formal language. GPT-f showed that a language model can
about feasible considerations to sound deployment. And lastly,       generate Metamath proofs that pass a checker [23]. To evaluate
Section VII wraps up the paper and gives way forward on              systems in a comparable way, miniF2F introduced a cross-
future research.                                                     system benchmark of formal Olympiad-level problems [24].
                                                                     Training and data generation became a key focus: expert-
                     II. R ELATED W ORK                              iteration style loops improved performance on formal math
   This work sits between two lines of research: (i) formal          statements [25], and large synthetic proof corpora were used
proof assistants with small trusted kernels, and (ii) learned sys-   to train Lean-focused provers such as DeepSeek-Prover and
tems (now including LLMs) that propose proof steps. Below            DeepSeek-Prover-V2 [26], [27]. Another major bottleneck is
we review the main threads and explain how ProofSketcher             selecting relevant library lemmas; LeanDojo made premise
differs.                                                             annotations and a retrieval-augmented prover (ReProver) avail-
                                                                     able as an open benchmark and toolkit [28]. ProofSketcher is
A. Proof assistants and small trusted kernels                        compatible with these ideas (retrieval, fine-tuning, search), but
   Interactive theorem provers were designed to make proof           it targets a different proof artifact: a typed sketch that is easy
acceptance depend on a small trusted computing base (TCB),           to decompose into obligations and easy to repair locally.
often via an LCF-style kernel where only the kernel can
construct theorem objects [13]. Modern systems keep this idea        E. Autoformalization: from natural language to formal proofs
while improving automation and extensibility, for example               A separate but related problem is translating informal
Lean 4 and Coq [1], [2]. ProofSketcher follows the same trust        math into a formal statement and proof. ProofNet provides
model: the LLM is never trusted; only the kernel and certificate     paired natural language statements/proofs with Lean theorem
checkers are.                                                        statements, and serves as a benchmark for autoformalization
                                                                     plus formal proving [29]. ProofSketcher can be used after
B. Bridging interactive proving with ATP/SMT automation              autoformalization: once a formal goal is available, the sketch-
   A long-running approach is to connect an interactive prover       and-check loop can improve reliability and reduce repeated
to external automatic tools (first-order ATP and SMT) and            full-proof regeneration.
then reconstruct a proof inside the prover. Isabelle’s Sledge-
hammer is a well-known example and was studied in depth in           F. Neuro-symbolic geometry as a specialized success case
IJCAR 2010 [14]. Later work extended Sledgehammer to SMT                Geometry has strong symbolic structure, and recent systems
solvers and improved the overall pipeline while still producing      combine learning with symbolic deduction and search. Al-
replayable proof scripts in Isabelle/HOL [15]. In Coq, SMT-          phaGeometry (Nature 2024) showed strong results by synthe-
Coq integrates external SAT/SMT solvers by requiring proof           sizing large amounts of geometric theorems/proofs and using
witnesses (certificates) that are checked (and reconstructed)        a symbolic engine for deduction [30]. AlphaGeometry2 fur-
in Coq, preserving soundness [16]. ProofSketcher shares the          ther expanded coverage and improved search, reporting gold-
same principle, but it differs in the interface: instead of asking   medalist level performance on IMO geometry sets [31]. These
a model to output a full tactic script, it asks for a typed sketch   systems support our design choice: learned components can
that the kernel expands into obligations.                            propose useful structure, while a symbolic checker enforces
                                                                     correctness.
C. Learning-guided theorem proving before LLMs
  Before LLM-centric systems, machine learning was used              G. Proof certificates and independent checking
to guide premise selection and tactic search. HolStep pro-             In the application of external solvers, the general soundness
vided a large dataset of higher-order logic proof steps to           of the process is not only dependent upon the supposed
support learning-based guidance [17]. In HOL4, TacticToe             unsatisfied flag of the solver but upon verifiable evidence
used learned predictions inside a tactic-level search proce-         of such. An early example of this principle going on, was
dure [18]. HOList offered an environment and benchmark               theoretically, the use of proof-carrying code, showing that
around HOL Light and supported learning-driven proof search          there is a way to safely include untrusted producers, on the
(DeepHOL) [19]. For Coq, CoqGym released a large-scale               assumption that they can produce provable proof information
dataset and an approach (ASTactic) that generates tactics as         [32]. In the case of SMT the meta-framework of LFSC was
provided to enable the use of fast proceeds of solvers to
be effectively verified again with no trouble by the LFSC
meta-framework [33]. The DRATtrim format introduced an
effective representation of proofs and checker that can support
many inferences of SAT solvers in the SAT domain [34].
The ProofSketcher is no exception and adheres to the same
paradigm: a solver call has to provide a certificate which
gets verified by a small trusted checker and, thus, maintains a
minimal trusted computing base.
                III. S YSTEM A RCHITECTURE
  Fig. 1 shows ProofSketcher as a closed-loop pipeline with a       Fig. 1. ProofSketcher architecture: LLM proposes a typed sketch; a
                                                                    lightweight trusted kernel extracts obligations; external solvers are untrusted
small trusted core. The LLM is used only to propose structure       and must provide certificates checked by a trusted checker; failures yield
and hints. Soundness comes from the kernel and certificate          structured feedback for local repair; caching enables incremental re-checking.
checking, not from model outputs [13], [32].
A. Components                                                       only the failing node (e.g., add a missing lemma, refine
   (1) Input Layer. The system takes a target theorem T with        instantiation, add a precondition subgoal). This repair loop
context Γ in a logic L. L can be first-order logic with equality,   runs for at most R repair iterations; if no kernel-accepted proof
extended with linear integer arithmetic (LIA) for arithmetic        is obtained, the theorem is rejected with the final failure report.
obligations.                                                        B. Trusted Boundary
   (2) Premise Retrieval. The system retrieves a bounded set
of candidate lemmas and definitions for each goal node and             The trusted computing base (TCB) includes only: (i) the
passes them as non-trusted hints to sketch generation and           kernel, (ii) the certificate checker, and (iii) proof object
repair. [28].                                                       storage/replay. Retrieval, the LLM, and external solvers are
   (3) LLM Sketch Generator. The LLM produces a typed               outside the TCB. This separation mirrors the classic “untrusted
proof sketch in the ProofSketch DSL. The sketch contains            producer, trusted checker” pattern [32].
method tags (rewrite, split, induction, contradiction), explicit    C. End-to-End Dataflow
dependencies, and typed holes for missing subproofs.
                                                                       (1) T, Γ enter the system; retrieval adds a bounded set
   (4) Typed Sketch DSL. The DSL is the interface contract:
                                                                    of candidate lemmas (possibly empty) as non-trusted hints.
it is structured enough for reliable obligation extraction, but
                                                                    (2) The LLM drafts a typed sketch. (3) The kernel expands
lighter than a full tactic script. This reduces search space
                                                                    sketch nodes into obligations. (4) Obligations are discharged
compared to direct tactic generation and supports localized
                                                                    by kernel rules or certified solver calls. (5) Passed obligations
repair.
                                                                    produce proof objects and populate the cache. (6) Failures
   (5) Lightweight Kernel (Trusted). The kernel parses the
                                                                    produce localized feedback; the LLM edits only the failing
sketch and converts each node into a fixed set of obligations
                                                                    region; the kernel re-checks incrementally.
in a sequent form Γ ⊢ ϕ. The kernel has a small set of trusted
inference rules, aligned with the LCF-style trust model used                          IV. P ROPOSED M ETHODOLOGY
in interactive provers [13], [1].                                     ProofSketcher is a closed-loop pipeline that turns an LLM-
   (6) Obligation Queue. Extracted obligations are queued and       generated sketch into a kernel-checked proof. The method has
dispatched. Each obligation carries provenance: originating         four fixed phases.
sketch node id, local context, and required theory fragment.
   (7) Solver Bridge (Untrusted) + Certificate Checker              A. Phase 1: Typed Sketch Generation
(Trusted). For decidable fragments, the kernel can call external       Given a theorem T and context Γ in logic L, the LLM pro-
SMT/ATP tools, but it accepts results only when accompanied         duces a typed sketch S in the ProofSketch DSL. Each sketch
by checkable evidence. The certificate checker validates this       node includes: (i) goal formula, (ii) method tag (rewrite,
evidence before the kernel records a derived step [32]. This        split, induction, contradiction), (iii) referenced
keeps automation outside the trusted boundary.                      facts, and (iv) typed subgoals. Unproven subgoals are rep-
   (8) Proof Object Store + Node Cache (Trusted). Accepted          resented as typed holes, and each hole declares its required
obligations produce kernel-replayable proof objects. Each           formula type; acceptance requires that all holes are discharged.
sketch node is cached by a content hash of (goal, method,
inputs, hints). Unchanged nodes reuse cached results, enabling      B. Phase 2: Obligation Extraction
fast edit-check cycles.                                                A trusted kernel parses S and deterministically expands
   (9) Structured Feedback + Local Repair. When an obligation       each node into a finite set of obligations O = {(Γi ⊢ ϕi )}.
fails, the kernel returns a structured report (failed node, cause   The expansion rules depend only on the node tag and its typed
class, minimal local context). The LLM is prompted to edit          fields. For example, a split node generates two obligations
under Γ ∪ {c} and Γ ∪ {¬c}, and a rewrite node generates
obligations to justify the equality and the rewrite application
at the chosen term position.
C. Phase 3: Certificate-Gated Discharge
   Each obligation is discharged in one of two ways:
   1) Kernel proof: the kernel proves Γi ⊢ ϕi using its trusted
       inference rules (propositional rules, equality reasoning,
       and quantifiers with explicit instantiation).
   2) Certified external proof: an external solver is called on
       a translated form of (Γi , ϕi ) and must return a proof                     Fig. 2. Pass rate by benchmark and method.
       certificate. A trusted certificate checker validates the
       certificate, and the kernel records the result as a derived
       step.
If a certificate fails validation, the obligation is marked failed.
D. Phase 4: Local Repair and Incremental Re-check
   If any obligation fails, the kernel returns a structured failure
record (node id, cause, Γi , ϕi ), where cause is one of: miss-
ing lemma, failed instantiation, invalid rewrite, or unsatisfied
precondition. The LLM edits only the failing node (and its
direct subgoals) to produce an updated sketch S ′ . The kernel
re-checks incrementally using node hashing; unchanged nodes
reuse cached proofs. The loop stops when all obligations are                   Fig. 3. Mean LLM calls per theorem (lower is better).
proven and the kernel emits a replayable proof object for T .
                          V. R ESULTS                                 to regenerate the entire proof script; the edit-check loop of
A. Benchmarks and Acceptance Criterion                                repair is stabilised by relying on iteration of the specific node
                                                                      repair.
   We evaluate ProofSketcher on three standard settings:
miniF2F (Lean4) [24], LeanDojo benchmark (mathlib) [28],                                      VI. D ISCUSSION
and ProofNet [29]. A problem is counted as solved only when
the kernel accepts a replayable proof.                                   ProofSketcher is based on one design idea: the LLM is
                                                                      expected to suggest high-level structure, and the correctness
B. Compared Methods                                                   is to be checked with the use of formal checking. This brings
   We compare against: ReProver from LeanDojo (retrieval-             about two viable benefits. The system is the first to refuse a
augmented proving) [28], DeepSeek-Prover [26], and                    proof due to an exact justification, exactly such as a mis writers
DeepSeek-Prover-V2 [27]. These are widely used baselines              rewrite target, a precondition violation or a poor instantiation
for Lean-based neural proving and large-scale synthetic-proof         instead of just spewing out a protracted tactic track because
training.                                                             of failure. Second, the repair is local: a single sketch node is
                                                                      edited by the model, and all obligations that are affected are
C. Main Results                                                       re-validated by the kernel with the help of caching to eliminate
   Table I reports pass rate and cost metrics across benchmarks.      unnecessary work.
Fig. 2 shows pass rate by benchmark. Fig. 3 reports the mean             One such trade-off between the system is the granularity
number of LLM calls per theorem, which reflects how often             of the sketch and the obligation discharge burden. When the
repair is needed. Fig. 4 shows mean runtime split into kernel         sketch is too abstract, the kernel will be required to create
time and solver time.                                                 huge, difficult obligations and hence make more solver calls.
                                                                      On the other hand, when the sketch is too detailed, it will be
D. Repair and Failure Analysis                                        close to that of a tactic script and the LLM will have to process
   In order to explicitly analyse the reliability benefits provided   numerous low-level proof engineering tasks. In practice, the
by ProofSketcher, we record the type of failure in a sketch at        best compromise is an explicit record of approximately why
a single node, the first sketch node to fail: missing lemma,          a step ought to succeed, one of the method tags on steps, and
failed instantiation, invalid rewrite and unsatisfied precondi-       the lemmas that they intend are to be certified and handed
tion. Mean number of repetitions of a repair before acceptance        over to the trusted kernel and certified automation.
is also recorded. Due to localisation of failures by means of            Certificate-gated automation is important for reliability but
node identifier, the repair prompt is only regenerated on a           adds overhead. Proof certificates can be large, and checking
single node, which eliminates repetitive eventual global search       them can dominate runtime for some goals. This suggests
                                                                 TABLE I
                                   K ERNEL -ACCEPTED PASS R ATE (%) ON F ORMAL R EASONING B ENCHMARKS

                    Method                       miniF2F-test (Pass %)   LeanDojo-test (Pass %)      ProofNet-test (Pass %)
                    ReProver (LeanDojo) [28]             26.64%                  51.20%                       13.98%
                    DeepSeek-Prover [26]                 50.00%                     –                            –
                    DeepSeek-Prover-V2 [27]              88.93%                     –                         37.10%
                    ProofSketcher (Ours)                 92.21%                  58.25%                       44.62%



                                                                         The system returns localized failure feedback and supports fast
                                                                         repair through node-level caching and targeted sketch edits.
                                                                            The main outcome is a practical bridge between informal
                                                                         LLM reasoning and formal reliability: proofs are accepted only
                                                                         by checking, while the LLM remains useful for proposing
                                                                         structure and guiding search. Future work should focus on
                                                                         (i) better obligation shaping to reduce certificate size, (ii)
                                                                         tighter integration with library search to reduce missing-lemma
                                                                         failures, and (iii) broader evaluation across proof domains and
                                                                         theory fragments while preserving a small trusted computing
         Fig. 4. Mean time per theorem: kernel vs solver time.           base.
                                                                                                      R EFERENCES
two controls: (i) use certified solvers only for obligations that         [1] L. de Moura and S. Ullrich, “The lean 4 theorem prover
fall in well-scoped fragments, and (ii) prefer kernel-native                  and programming language (system description),” in International
reasoning for small local steps (rewrites, propositional splits,              Conference on Automated Deduction (CADE), 2021. [Online]. Available:
                                                                              https://lean-lang.org/papers/lean4.pdf
simple quantifier instantiation). A second limitation is library          [2] The Coq Development Team, The Coq Proof Assistant: Reference
dependence. Many failures in formal proving are not due to                    Manual, INRIA / TypiCal Project, 2013, version 8.4pl2, April
hard logic, but due to missing the right lemma name or a                      4, 2013. [Online]. Available: https://flint.cs.yale.edu/cs430/coq/pdf/
                                                                              Reference-Manual.pdf
required side condition. ProofSketcher reduces the cost of such           [3] S. Polu and I. Sutskever, “Generative language modeling for automated
failures by producing a clear missing lemma signal, but it                    theorem proving,” 2020. [Online]. Available: https://arxiv.org/abs/2009.
does not remove the need for good library search and lemma                    03393
                                                                          [4] K. Zheng, J. M. Han, and S. Polu, “Minif2f: a cross-system
selection.                                                                    benchmark for formal olympiad-level mathematics,” in International
   Another issue is robustness across domains. miniF2F re-                    Conference on Learning Representations (ICLR), 2022. [Online].
wards clean mathematical structure, while ProofNet adds noise                 Available: https://openreview.net/forum?id=9ZPegFuFTFv
                                                                          [5] S. Polu, J. M. Han, K. Zheng, M. Baksys, I. Babuschkin, and
from informal-to-formal mismatch, and LeanDojo includes                       I. Sutskever, “Formal mathematics statement curriculum learning,”
large-library engineering effects. The same sketch policy may                 2022. [Online]. Available: https://arxiv.org/abs/2202.01344
not be optimal across all three. This motivates benchmark-                [6] H. Xin, D. Guo, Z. Shao, Z. Z. Ren, Q. Zhu, B. Liu, C. Ruan,
                                                                              W. Li, and X. Liang, “Deepseek-prover: Advancing theorem proving
specific tuning of sketch depth (more explicit instantiations for             in llms through large-scale synthetic data,” 2024. [Online]. Available:
ProofNet-style goals, more lemma-centric hints for LeanDojo,                  https://arxiv.org/abs/2405.14333
and more structured induction templates for miniF2F).                     [7] Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao,
                                                                              L. Zhang, Z. Fu, Q. Zhu, D. Yang, Z. F. Wu, Z. Gou, S. Ma,
   Finally, ProofSketcher is designed to keep the trusted base                H. Tang, Y. Liu, W. Gao, D. Guo, and C. Ruan, “Deepseek-
small. However, the trusted base still includes the kernel,                   prover-v2: Advancing formal mathematical reasoning via reinforcement
the certificate checker, and any translation layer that maps                  learning for subgoal decomposition,” 2025. [Online]. Available:
                                                                              https://arxiv.org/abs/2504.21801
obligations to the solver format. The translation must preserve           [8] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
meaning. In an implementation, this layer should be minimized                 S. Godil, R. Prenger, and A. Anandkumar, “Leandojo: Theorem
and tested heavily because it is a common source of subtle                    proving with retrieval-augmented language models,” 2023, presented
                                                                              at NeurIPS 2023 (paper version on arXiv). [Online]. Available:
unsoundness.                                                                  https://arxiv.org/abs/2306.15626
                                                                          [9] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev,
                       VII. C ONCLUSION                                       and J. Avigad, “Proofnet: Autoformalizing and formally proving
                                                                              undergraduate-level mathematics,” 2023. [Online]. Available: https:
   This paper introduced ProofSketcher, a hybrid LLM +                        //arxiv.org/abs/2302.12433
lightweight proof-checking approach for reliable math and                [10] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving
                                                                              olympiad geometry without human demonstrations,” Nature, vol.
logic reasoning. The LLM produces a typed proof sketch with                   625, no. 7995, pp. 476–482, 2024. [Online]. Available: https:
explicit step tags and typed holes. A trusted kernel expands the              //www.nature.com/articles/s41586-023-06747-5
sketch into proof obligations and accepts a theorem only when            [11] Y. Chervonyi, T. H. Trinh, M. Olšák, X. Yang, H. Nguyen, M. Menegali,
                                                                              J. Jung, V. Verma, Q. V. Le, and T. Luong, “Gold-medalist performance
all obligations are discharged by kernel rules or by externally               in solving olympiad geometry with alphageometry2,” 2025. [Online].
produced proof certificates that a trusted checker validates.                 Available: https://arxiv.org/abs/2502.03544
[12] G. C. Necula, “Proof-carrying code,” in Proceedings of the 24th            [29] Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev,
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming                       and J. Avigad, “Proofnet: Autoformalizing and formally proving
     Languages (POPL), 1997. [Online]. Available: https://dl.acm.org/doi/            undergraduate-level mathematics,” 2023. [Online]. Available: https:
     10.1145/263699.263712                                                           //arxiv.org/abs/2302.12433
[13] M. J. C. Gordon, A. J. Milner, and C. P. Wadsworth, Edinburgh              [30] T. H. Trinh, Y. Wu, Q. V. Le, and T. Luong, “Solving olympiad
     LCF: A Mechanized Logic of Computation, ser. Lecture Notes in                   geometry without human demonstrations,” Nature, vol. 625, no.
     Computer Science. Springer, 1979, vol. 78. [Online]. Available:                 7995, pp. 476–482, 2024. [Online]. Available: https://www.nature.com/
     https://link.springer.com/book/10.1007/3-540-09724-4                            articles/s41586-023-06747-5
[14] S. Böhme and T. Nipkow, “Sledgehammer: Judgement day,” in                 [31] Y. Chervonyi, T. H. Trinh, M. Olšák, X. Yang, H. Nguyen, M. Menegali,
     Automated Reasoning (IJCAR 2010), ser. Lecture Notes in Computer                J. Jung, V. Verma, Q. V. Le, and T. Luong, “Gold-medalist performance
     Science, vol. 6173. Springer, 2010, pp. 107–121. [Online]. Available:           in solving olympiad geometry with alphageometry2,” 2025. [Online].
     https://link.springer.com/chapter/10.1007/978-3-642-14203-1 9                   Available: https://arxiv.org/abs/2502.03544
[15] J. C. Blanchette, S. Böhme, and L. C. Paulson, “Extending                 [32] G. C. Necula, “Proof-carrying code,” in Proceedings of the 24th
     sledgehammer with smt solvers,” Journal of Automated Reasoning,                 ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     vol. 51, no. 1, pp. 109–128, 2013. [Online]. Available: https:                  Languages (POPL), 1997. [Online]. Available: https://dl.acm.org/doi/
     //link.springer.com/article/10.1007/s10817-013-9278-5                           10.1145/263699.263712
[16] B. Ekici, A. Mebsout, C. Tinelli, C. Keller, G. Katz, A. Reynolds,         [33] A. Stump, D. Oe, A. Reynolds, L. Hadarean, and C. Tinelli, “Smt
     and C. Barrett, “Smtcoq: A plug-in for integrating smt solvers                  proof checking using a logical framework,” Formal Methods in
     into coq,” in Computer Aided Verification (CAV 2017), ser. Lecture              System Design, vol. 42, no. 1, pp. 91–118, 2013. [Online]. Available:
     Notes in Computer Science. Springer, 2017. [Online]. Available:                 https://dl.acm.org/doi/10.1007/s10703-012-0163-3
     https://link.springer.com/chapter/10.1007/978-3-319-63390-9 7              [34] N. Wetzler, M. J. H. Heule, and W. A. Hunt, “Drat-trim: Efficient
[17] C. Kaliszyk, F. Chollet, and C. Szegedy, “Holstep: A machine learning           checking and trimming using expressive clausal proofs,” in Theory
     dataset for higher-order logic theorem proving,” in International               and Applications of Satisfiability Testing – SAT 2014, ser. Lecture
     Conference on Learning Representations (ICLR), 2017. [Online].                  Notes in Computer Science, vol. 8561. Springer, 2014, pp.
     Available: https://openreview.net/forum?id=ryuxYmvel                            422–429. [Online]. Available: https://link.springer.com/chapter/10.1007/
[18] T. Gauthier, C. Kaliszyk, J. Urban, R. Kumar, and M. Norrish,                   978-3-319-09284-3 31
     “Tactictoe: Learning to prove with tactics,” Journal of Automated
     Reasoning, vol. 65, pp. 257–286, 2021. [Online]. Available: https:
     //dl.acm.org/doi/10.1007/s10817-020-09580-x
[19] K. Bansal, S. Loos, M. Rabe, C. Szegedy, and S. Wilcox, “HOList:
     An environment for machine learning of higher order logic theorem
     proving,” in Proceedings of the 36th International Conference on
     Machine Learning (ICML), ser. Proceedings of Machine Learning
     Research, vol. 97. PMLR, 2019, pp. 454–463. [Online]. Available:
     https://proceedings.mlr.press/v97/bansal19a.html
[20] K. Yang and J. Deng, “Learning to prove theorems via interacting with
     proof assistants,” in Proceedings of the 36th International Conference
     on Machine Learning (ICML), ser. Proceedings of Machine Learning
     Research, vol. 97. PMLR, 2019, pp. 6984–6994. [Online]. Available:
     https://proceedings.mlr.press/v97/yang19a.html
[21] A. Sanchez-Stern, Y. Alhessi, L. Saul, and S. Lerner, “Generating
     correctness proofs with neural networks,” in Proceedings of the
     4th ACM SIGPLAN International Workshop on Machine Learning
     and Programming Languages (MAPL), 2020. [Online]. Available:
     https://dl.acm.org/doi/10.1145/3394450.3397466
[22] M. Wu, M. Norrish, C. Walder, and A. Dezfouli, “Tacticzero: Learning
     to prove theorems from scratch with deep reinforcement learning,”
     in Advances in Neural Information Processing Systems (NeurIPS),
     2021. [Online]. Available: https://proceedings.neurips.cc/paper/2021/
     hash/4dea382d82666332fb564f2e711cbc71-Abstract.html
[23] S. Polu and I. Sutskever, “Generative language modeling for automated
     theorem proving,” 2020. [Online]. Available: https://arxiv.org/abs/2009.
     03393
[24] K. Zheng, J. M. Han, and S. Polu, “Minif2f: a cross-system
     benchmark for formal olympiad-level mathematics,” in International
     Conference on Learning Representations (ICLR), 2022. [Online].
     Available: https://arxiv.org/abs/2109.00110
[25] S. Polu, J. M. Han, K. Zheng, M. Baksys, I. Babuschkin, and
     I. Sutskever, “Formal mathematics statement curriculum learning,”
     2022. [Online]. Available: https://arxiv.org/abs/2202.01344
[26] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan,
     W. Li, and X. Liang, “Deepseek-prover: Advancing theorem proving
     in llms through large-scale synthetic data,” 2024. [Online]. Available:
     https://arxiv.org/abs/2405.14333
[27] Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao,
     L. Zhang, Z. Fu, Q. Zhu, D. Yang, Z. F. Wu, Z. Gou, S. Ma,
     H. Tang, Y. Liu, W. Gao, D. Guo, and C. Ruan, “Deepseek-
     prover-v2: Advancing formal mathematical reasoning via reinforcement
     learning for subgoal decomposition,” 2025. [Online]. Available:
     https://arxiv.org/abs/2504.21801
[28] K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
     S. Godil, R. Prenger, and A. Anandkumar, “Leandojo: Theorem proving
     with retrieval-augmented language models,” 2023. [Online]. Available:
     https://arxiv.org/abs/2306.15626
