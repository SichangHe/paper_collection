A DbC Inspired Neurosymbolic Layer for Trustworthy Agent
Design
Claudiu Leoveanu-Condrei1
1
    ExtensityAI, 20 Stefan-Fadinger-Straße, Wels, 4600, Austria


                   Abstract
                   Generative models, particularly Large Language Models (LLMs), produce fluent outputs yet lack verifiable guarantees. We adapt Design
                   by Contract (DbC) and type-theoretic principles to introduce a contract layer that mediates every LLM call. Contracts stipulate semantic
                   and type requirements on inputs and outputs, coupled with probabilistic remediation to steer generation toward compliance. The layer
                   exposes the dual view of LLMs as semantic parsers and probabilistic black-box components. Contract satisfaction is probabilistic and
                   semantic validation is operationally defined through programmer-specified conditions on well-typed data structures. More broadly, this
                   work postulates that any two agents satisfying the same contracts are functionally equivalent with respect to those contracts.

                   Keywords
                   neurosymbolic AI, design-by-contract, probabilistic programming, large language models



1. Introduction                                                                                               ology extends classical Hoare logic assertions of the form
                                                                                                              {𝑃 }𝐶{𝑄} [15, 16]—which specify that if a pre-condition 𝑃
The increasing integration of generative models, especially                                                   holds before the execution of a computational unit 𝐶, then
Large Language Models (LLMs), into diverse applications                                                       a post-condition 𝑄 will hold upon its termination—by as-
necessitates formal approaches to ensure the dependability                                                    sociating the fulfillment of such a triple with a quantifiable
of their outputs [1, 2]. LLMs are susceptible to producing                                                    success probability, 𝑃𝑠𝑢𝑐𝑐 .
outputs that, despite being syntactically plausible, may be                                                     In the context of this work, an agent 𝒜 is a tuple of the
factually incorrect or semantically misaligned with user                                                      form
expectations [3, 4, 5].                                                                                                          𝒜 = ⟨ ℳ, Π, Θ, 𝒯 , 𝒞 ⟩
   Standard software engineering paradigms like Design by
Contract (DbC) [6] offer principles for constructing reliable                                                 where ℳ is a set of generative models (e.g., LLMs) the agent
systems by enforcing explicit specifications, termed con-                                                     controls, Π is the set of instructions the agent must execute,
tracts, that detail the mutual obligations between software                                                   Θ is the set of hyperparameters governing the agent’s be-
components. This research extends and adapts these princi-                                                    havior (e.g., temperature, iterations, etc.), 𝒯 is the set of of
ples to the inherently probabilistic and semantic operational                                                 types the agent can handle, and 𝒞 is the set of contracts the
domain of modern generative models.                                                                           agent must satisfy. The agent’s behavior is defined by its
   Dinu et al. [7] positions LLMs as components that func-                                                    ability to generate well-typed outputs according to 𝒯 , given
tion as semantic parsers. These parsers transform inputs                                                      inputs that are well-typed according to 𝒯 and instructions
(e.g., natural language prompts) into structured data repre-                                                  in Π, while respecting hyperparameters Θ and satisfying
sentations or perform operations guided by semantic intent—                                                   contracts 𝒞.
the specific meaning and purpose the user intends to convey                                                      Inspired by observational equivalence [17, 18, 19, 20],
or achieve.                                                                                                   agents satisfying the same probabilistic contracts are func-
   Type theory [8, 9, 10, 11], particularly through the lens                                                  tionally equivalent with respect to those contracts; they
of the Curry-Howard correspondence [12, 13], establishes                                                      differ only in (i) 𝑃𝑠𝑢𝑐𝑐 , (ii) operational costs, and (iii) poten-
an isomorphism where types in a formal system are analo-                                                      tial—i.e., the capacity of the agent to satisfy an ever more
gous to propositions in logic, and well-typed programs (or                                                    complex set of conditions, enabling principled comparison
terms inhabiting those types) correspond to constructive                                                      and selection.
proofs of those propositions [14]. A "well-typed" program                                                        In practice, guardrails and schema validators [21, 22],
or data structure, in this context, is one that conforms to the                                               function-calling and constitutional-style self-remediation
structural and constraint rules defined by its type. Conse-                                                   [23, 24, 25, 26], and ReAct/RAG correction loops [27, 28,
quently, defining contracts over such well-typed data struc-                                                  29, 30, 31] can all be expressed as pre/post predicates with
tures provides a rigorous theoretical basis for specifying                                                    bounded remediation under the contract layer. Our con-
and verifying semantic requirements; a model output satis-                                                    tribution is a unified, declarative DbC formalism and exe-
fying a contract can be seen as a constructive proof of the                                                   cution flow that subsumes these patterns while remaining
specification embodied by that contract.                                                                      implementation-agnostic.
   Contracts specify pre-conditions (𝑃 ) that must hold be-
fore a component’s execution and post-conditions (𝑄) that                                                     2. Related Work
are guaranteed upon successful, type-conformant comple-
tion. The satisfaction of these contractual obligations by                                                    Program Correctness and DbC: The axiomatic approach
LLMs, which are inherently probabilistic, is therefore also                                                   [32, 15] and DbC [33] provide foundations for reasoning
probabilistic. The layer incorporates automated, model-                                                       about software behavior through explicit interface specifi-
driven remediation attempts to guide the component to-                                                        cations [16]. While runtime monitoring imposes overhead,
ward outputs that comply with the contract. This method-                                                      soft contract verification [34] enables static proofs via sym-
                                                                                                              bolic execution, and Hanus [35] combines static/dynamic
$ leo@extensity.ai (C. Leoveanu-Condrei)                                                                      checking for compile-time verification.
 https://futurisold.github.io/ (C. Leoveanu-Condrei)
               © 2025 Copyright for this paper by its authors. Use permitted under Creative Commons License
               Attribution 4.0 International (CC BY 4.0).
   Type Theory: From Church’s simple types [9] to Intu-                        are implemented as methods that either return True or
itionistic Type Theory [11, 10], type systems ensure well-                     raise descriptive exceptions. These exceptions serve a dual
structured data for contracts. The Curry-Howard correspon-                     purpose: they signal contract violations and provide se-
dence [12, 8] links types to logical propositions, making type                 mantic guidance to the LLM during the remediation phase.
conformance a prerequisite for semantic validation.                            Similarly, post-conditions validate the generated output’s
   Probabilistic Program Logics: Probabilistic Hoare Log-                      semantic properties beyond mere type conformance.
ics [36, 37] establish properties with probabilities, extended                    The contract execution flow proceeds through distinct
by loops [38] and union bounds [39]. eRHL [40] provides                        phases: (i) initial type validation of inputs against 𝒯 , (ii)
quantitative reasoning for probabilistic programs with com-                    pre-condition checking with optional remediation, (iii) an
pleteness results.                                                             optional act method for intermediate transformations, (iv)
   LLM Reliability: LLMs produce inconsistent outputs [1]                      LLM-driven output generation guided by the class’s prompt
despite code generation [3] and semantic parsing capabili-                     property and type specifications, and (v) post-condition vali-
ties [7, 41]. PEIRCE [42] unifies material/formal inference                    dation with remediation attempts. Type validation enforces
through neuro-symbolic conjecture-criticism, while con-                        structural well-formedness, while pre/post enforce seman-
tracts address DL API reliability [43]. Echoing Marcus [44],                   tic predicates on well-typed objects. When remediation
reliability may hinge on architectures that explicitly manip-                  is enabled for either pre- or post-conditions, both input
ulate symbols, providing the deterministic, compositional                      and output objects are "fixed"—guaranteed to be type-valid
substrate today’s LLMs lack.                                                   with all field conditions satisfied. This fixing process uses
                                                                               the LLM to populate or correct fields according to the type
                                                                               schema and semantic instructions, ensuring that each field
3. Implementation                                                              contains valid data (e.g., an extracted email or default value)
                                                                               that passes all specified constraints.
The contract layer is built entirely on the SymbolicAI frame-
                                                                                  Remediation is achieved through a component that it-
work [7] , extending its neurosymbolic capabilities with
                                                                               eratively refines outputs by incorporating validation error
DbC-inspired validation mechanisms1 . At its core, the im-
                                                                               messages into corrective prompts. The accumulation of er-
plementation leverages user-defined data models (Pydantic-
                                                                               ror history across retry attempts enables the LLM to learn
based [22] LLMDataModel subclasses) that serve as the con-
                                                                               from previous failures, avoiding cyclic errors. Each valida-
crete instantiation of the type system 𝒯 . These models de-
                                                                               tion function is parameterized by retry configurations in Θ,
fine not only structural requirements but also rich semantic
                                                                               controlling the maximum attempts (to preclude deep loops),
descriptions through field annotations, guiding both type
                                                                               delays, and backoff strategies.
validation and LLM generation.
                                                                                  A critical aspect of the implementation is the fallback
                                                                               mechanism, which embodies DbC’s invariant principle. The
                                                                               original forward method is always executed in a finally
                                                                               block, regardless of contract validation outcomes. If contract
                                                                               validation fails, the forward method can enable graceful
                                                                               falling, where contract or type mismatches do not raise—the
                                                                               raw forward output is returned as-is, or can return a safe,
                                                                               type-compliant default. This design guarantees that contract
                                                                               failures never prevent system operation, merely degrading
                                                                               from verified to best-effort behavior.
                                                                                  Lastly, the success of contract satisfaction for each in-
                                                                               vocation is a Bernoulli random variable. We compute the
                                                                               empirical success
                                                                                             ∑︀𝑁 probability over N independent runs as
                                                                               𝑃succ = 𝑁1       𝑡=1 1[all contract predicates pass]. To sim-
                                                                               plify evaluation and reporting, we approximate the over-
                                                                               all success probability by multiplying per-family success
                                                                               probabilities. For example, if a post-condition involves six
                                                                               individual checks (predicates), we can group them into fam-
                                                                               ilies—such as class existence, index validity, and cluster
                                                                               reduction—and treat these families as independent, even
                                                                               though dependencies may exist. Combined with perfor-
                                                                               mance metrics that track validation overhead and remedia-
                                                                               tion costs, this approximation enables runtime comparison
                                                                               of functionally equivalent agents that satisfy the same con-
                                                                               tracts 𝒞.
Figure 1: Contract execution flow.


  When an agent 𝒜 processes a request, the contract deco-
                                                                               4. Limitations and Future Work
rator wraps the underlying Expression class’s forward                          While our contract layer provides a robust framework for
method, establishing a validation pipeline. Pre-conditions                     ensuring type conformance and semantic validation, several
1
    The contract source code is available at this GitHub [link]; the docu-     limitations merit discussion, alongside promising avenues
    mentation is available at this GitBook [link]. For challenging practical   for future investigation.
    use cases involving contracts, see this codebase [link], which includes
    various types of contracts ranging from simple to complex (e.g., repair-
                                                                                 Model Constraints. Semantic validation remains bounded
    ing a broken ontology).
by LLM capabilities and stochasticity. While hyperparame-              ative Models and Solvers, in: Proceedings of the 3rd
ter control enables deterministic outputs, low-temperature             Conference on Lifelong Learning Agents (CoLLAs),
settings may prune valid solution paths. Recent work on                2024. ArXiv:2402.00854.
grammar-constrained generation offers promising mitiga-            [8] P. B. Andrews, An introduction to mathematical logic
tion strategies [45, 46, 47]. Libraries like Lark [48] and Par-        and type theory: to truth through proof, volume 27,
simonious [49] provide practical foundations for encoding              Springer Science & Business Media, 2013.
deterministic constraints within our semantic validation           [9] A. Church, A formulation of the simple theory of
framework.                                                             types, The journal of symbolic logic 5 (1940) 56–68.
   Design Trade-offs. Proactive contract design demands           [10] B. C. Pierce, Types and programming languages, MIT
upfront investment. Poorly specified contracts risk over-              press, 2002.
constraining agents, creating brittle systems that fail to        [11] T. Coquand, An analysis of Girard’s paradox, Ph.D.
generalize. Conversely, overly permissive contracts provide            thesis, INRIA, 1986.
weak guarantees. The challenge lies in systematically de-         [12] P. Wadler, Propositions as types, Communications of
signing constraints that guide generation toward intended              the ACM 58 (2015) 75–84.
outcomes without stifling valid solution paths.                   [13] M.-C. Dinu, Parameter Choice and Neuro-Symbolic
   Formal Verification. Current contracts lack formal guar-            Approaches for Deep Domain-Invariant Learning,
antees about type system correctness. Future work will                 arXiv preprint arXiv:2410.06235 (2024).
pursue Lean4 [50] formalization of the entire pipeline, pro-      [14] J.-Y. Girard, P. Taylor, Y. Lafont, Proofs and types, vol-
viding machine-checked proofs of type safety and contract              ume 7, Cambridge university press Cambridge, 1989.
satisfaction properties. This formalization will establish rig-   [15] C. A. R. Hoare, An axiomatic basis for computer pro-
orous foundations for trustworthy agent design, enabling               gramming, Communications of the ACM 12 (1969)
verification of contract consistency, type safety preserva-            576–580.
tion across agent compositions, and probabilistic bounds on       [16] H. Leung, Program Correctness, AMC 10 (2010) 12.
contract satisfaction under various operational conditions.       [17] J. H. Morris, Lambda calculus models of programming
The Lean4 effort is prospective; the runtime layer does not            languages (1968).
depend on it.                                                     [18] M. Hennessy, R. Milner, Algebraic laws for nondeter-
                                                                       minism and concurrency, Journal of the ACM (JACM)
                                                                       32 (1985) 137–161.
5. Conclusion                                                     [19] G. D. Plotkin, A structural approach to operational
                                                                       semantics, Aarhus university, 1981.
We have presented a DbC inspired layer for trustworthy
                                                                  [20] F. Q. Da Silva, Observational equivalence and compiler
agent design that bridges the gap between LLM capabil-
                                                                       correctness, University of Edinburgh, Department of
ities and formal verification requirements. By extending
                                                                       Computer Science, Laboratory for . . . , 1992.
classical DbC principles to the probabilistic domain of gen-
                                                                  [21] NVIDIA, NeMo Guardrails, https://github.com/
erative models, our approach provides verifiable guarantees
                                                                       NVIDIA/NeMo-Guardrails, 2023. Accessed: 2025-06-
through type-theoretic contracts while maintaining the flex-
                                                                       11.
ibility inherent in LLM-based systems.
                                                                  [22] S. Colvin, Pydantic: Data validation using python type
                                                                       hints, 2025-06-14. URL: https://github.com/pydantic/
References                                                             pydantic.
                                                                  [23] Q. Lin, M. Wen, Q. Peng, G. Nie, J. Liao, J. Wang, X. Mo,
 [1] J. Yan, C. Wang, J. Huang, W. Zhang, Do large lan-                J. Zhou, C. Cheng, Y. Zhao, et al., Hammer: Robust
     guage models understand logic or just mimick con-                 function-calling for on-device language models via
     text?, arXiv preprint arXiv:2402.12091 (2024).                    function masking, arXiv preprint arXiv:2410.04587
 [2] X. Huang, W. Ruan, W. Huang, G. Jin, Y. Dong, C. Wu,              (2024).
     S. Bensalem, R. Mu, Y. Qi, X. Zhao, et al., A survey of      [24] X. Chen, H. Wen, S. Nag, C. Luo, Q. Yin, R. Li,
     safety and trustworthiness of large language models               Z. Li, W. Wang, Iteralign: Iterative constitutional
     through the lens of verification and validation, Artifi-          alignment of large language models, arXiv preprint
     cial Intelligence Review 57 (2024) 175.                           arXiv:2403.18341 (2024).
 [3] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto,      [25] Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion,
     J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brock-             A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McK-
     man, et al., Evaluating large language models trained             innon, et al., Constitutional ai: Harmlessness from ai
     on code, arXiv preprint arXiv:2107.03374 (2021).                  feedback, arXiv preprint arXiv:2212.08073 (2022).
 [4] Y. Deng, Y. Zhao, M. Li, S.-K. Ng, T.-S. Chua, Don’t         [26] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao,
     Just Say" I don’t know"! Self-aligning Large Language             S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang,
     Models for Responding to Unknown Questions with                   et al., Self-refine: Iterative refinement with self-
     Explanations, arXiv preprint arXiv:2402.15062 (2024).             feedback, Advances in Neural Information Processing
 [5] Z. Zhang, L. Lei, L. Wu, R. Sun, Y. Huang, C. Long,               Systems 36 (2023) 46534–46594.
     X. Liu, X. Lei, J. Tang, M. Huang, Safetybench: Eval-        [27] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan,
     uating the safety of large language models, arXiv                 Y. Cao, React: Synergizing reasoning and acting in
     preprint arXiv:2309.07045 (2023).                                 language models, in: International Conference on
 [6] B. Meyer, Object-Oriented Software Construction, 2nd              Learning Representations (ICLR), 2023.
     ed., Prentice-Hall, Upper Saddle River, NJ, USA, 1997.       [28] A. Asai, Z. Wu, Y. Wang, A. Sil, H. Hajishirzi, Self-rag:
 [7] M.-C. Dinu, C. Leoveanu-Condrei, W. Zellinger,                    Learning to retrieve, generate, and critique through
     M. Holzleitner, S. Hochreiter, SymbolicAI: A Frame-               self-reflection (2024).
     work for Logic-Based Approaches Combining Gener-             [29] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan,
     S. Yao, Reflexion: Language agents with verbal rein-             constrained decoding for structured NLP tasks without
     forcement learning, Advances in Neural Information               finetuning, arXiv preprint arXiv:2305.13971 (2023).
     Processing Systems 36 (2023) 8634–8652.                     [47] K. Park, T. Zhou, L. D’Antoni, Flexible and Efficient
[30] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao,        Grammar-Constrained Decoding, 2025. URL: https:
     K. Narasimhan, Tree of thoughts: Deliberate prob-                //arxiv.org/abs/2502.05111. arXiv:2502.05111.
     lem solving with large language models, Advances            [48] E. Shin, L. contributors, Lark: a parsing toolkit for
     in neural information processing systems 36 (2023)               python, 2024. URL: https://github.com/lark-parser/
     11809–11822.                                                     lark.
[31] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger,           [49] E. Rose, Parsimonious: the fastest pure-Python
     M. Podstawski, L. Gianinazzi, J. Gajda, T. Lehmann,              PEG parser, 2022. URL: https://github.com/erikrose/
     H. Niewiadomski, P. Nyczyk, et al., Graph of thoughts:           parsimonious.
     Solving elaborate problems with large language mod-         [50] L. d. Moura, S. Ullrich, The Lean 4 Theorem Prover and
     els, in: Proceedings of the AAAI conference on artifi-           Programming Language, in: International Conference
     cial intelligence, volume 38, 2024, pp. 17682–17690.             on Automated Deduction, Springer, 2021, pp. 625–635.
[32] R. W. Floyd, Assigning meanings to programs, in: Pro-
     gram Verification: Fundamental Issues in Computer
     Science, Springer, 1993, pp. 65–81.
[33] B. Meyer, Applying "Design by Contract", IEEE Com-
     puter 25 (1992) 40–51. doi:10.1109/2.161279.
[34] P. C. Nguyen, S. Tobin-Hochstadt, D. Van Horn, Soft
     contract verification, ACM SIGPLAN Notices 49 (2014)
     139–152.
[35] M. Hanus, Combining static and dynamic contract
     checking for Curry, Fundamenta Informaticae 173
     (2020) 285–314.
[36] D. Kozen, Semantics of probabilistic programs, in:
     20th Annual Symposium on Foundations of Computer
     Science (sfcs 1979), IEEE, 1979, pp. 101–114.
[37] J. Den Hartog, E. P. de Vink, Verifying probabilis-
     tic programs using a Hoare like logic, International
     journal of foundations of computer science 13 (2002)
     315–340.
[38] X. Sun, X. Su, X. Bian, A. Cui, On the Rela-
     tive Completeness of Satisfaction-based Probabilis-
     tic Hoare Logic With While Loop, arXiv preprint
     arXiv:2406.16054 (2024).
[39] G. Barthe, M. Gaboardi, B. Grégoire, J. Hsu, P.-Y. Strub,
     A program logic for union bounds, arXiv preprint
     arXiv:1602.05681 (2016).
[40] M. Avanzini, G. Barthe, D. Davoli, B. Grégoire, A
     quantitative probabilistic relational Hoare logic, Pro-
     ceedings of the ACM on Programming Languages 9
     (2025) 1167–1195.
[41] P. Schneider, M. Klettner, K. Jokinen, E. Simperl,
     F. Matthes, Evaluating large language models in
     semantic parsing for conversational question an-
     swering over knowledge graphs, arXiv preprint
     arXiv:2401.01711 (2024).
[42] X. Quan, M. Valentino, D. S. Carvalho, D. Dalal, A. Fre-
     itas, Peirce: Unifying material and formal reason-
     ing via llm-driven neuro-symbolic refinement, arXiv
     preprint arXiv:2504.04110 (2025).
[43] S. Ahmed, S. M. Imtiaz, S. S. Khairunnesa, B. D. Cruz,
     H. Rajan, Design by contract for deep learning apis,
     in: Proceedings of the 31st ACM joint European soft-
     ware engineering conference and symposium on the
     foundations of software engineering, 2023, pp. 94–106.
[44] G. F. Marcus, The Algebraic Mind: Integrating Connec-
     tionism and Cognitive Science, The MIT Press, Cam-
     bridge, MA, 2001. doi:10.7551/mitpress/1187.
     001.0001, bradford Books imprint.
[45] B. T. Willard, R. Louf, Efficient guided genera-
     tion for large language models, arXiv preprint
     arXiv:2307.09702 (2023).
[46] S. Geng, M. Josifoski, M. Peyrard, R. West, Grammar-
