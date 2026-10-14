                                         Projectional Decoding: Towards Semantic-Aware LLM Generation
                                                               Boqi Chen                               José Antonio Hernández López                              Aren A. Babikian
                                                         University of Ottawa                                   University of Murcia                            University of Toronto
                                                           Ottawa, Canada                                          Murcia, Spain                                   Toronto, Canada
                                                        boqi.chen@uottawa.ca                               joseantonio.hernandez6@um.es                        babikian@cs.toronto.edu

                                         Abstract                                                                                and semantically valid to satisfy intended requirements. Such valid-
                                         Large language models (LLMs) are increasingly used to generate                          ity is essential for ensuring correct behavior [32, 40], compliance
                                         software artifacts across many software engineering (SE) tasks, yet                     with regulations [6, 30], and seamless integration with other compo-
                                         ensuring the semantic validity of these artifacts remains a funda-                      nents [8, 21]. However, LLMs often struggle to consistently produce
                                         mental challenge. Existing constrained decoding techniques can                          syntactically and semantically valid outputs [5, 30, 38]. As LLMs
arXiv:2605.30054v1 [cs.SE] 28 May 2026




                                         enforce syntactic correctness and, in some cases, specific semantic                     are increasingly used in critical SE applications [11], addressing
                                         rules, but lack a general representation that bridges LLM-generated                     their semantic validity becomes an immediate task.
                                         text with the reasoning required for semantic validation in SE. In                         Some approaches repair LLM-generated artifacts after complete
                                         this paper, we propose projectional decoding, a novel conceptual                        generation with iterative post processing [5, 13, 14]. Such post-hoc
                                         framework that integrates domain semantics directly into the gener-                     methods can be inefficient and may not guarantee validity, particu-
                                         ation process by maintaining, alongside text, a partial graph model                     larly when the repair process is LLM-based. Invalid outputs may
                                         as the primary artifact representation throughout generation. This                      also be non-interpretable, potentially preventing repair techniques
                                         abstract representation enables incremental semantic validation                         from being applied at all. These limitations suggest that semantic
                                         by explicitly capturing uncertainty and natively supporting error                       validity should also be addressed during generation, not only after.
                                         detection, while guiding generation toward semantically valid out-                         In this paper, we argue that semantic-aware LLM generation in SE
                                         puts with provable guarantees. We present preliminary results on a                      requires shifting from text-focused generation to methods that leverage
                                         program generation task which demonstrate the potential of this ap-                     representations capturing the SE-specific structure of artifacts. While
                                         proach to improve the semantic validity of LLM-generated artifacts.                     LLMs generate text, SE artifacts are inherently structural and often
                                         We also discuss how projectional decoding can enable verifiable                         represented using graph-based models [10, 24]. Moreover, many
                                         automation with LLMs across various SE activities.                                      semantic properties in SE are specified as constraints over such
                                                                                                                                 models [2, 27, 28]. Treating semantic properties at the text level
                                         CCS Concepts                                                                            therefore introduces a fundamental mismatch between how artifacts
                                                                                                                                 are generated and how their correctness is defined.
                                         • Software and its engineering → Model-driven software engi-
                                                                                                                                    Recent work on constrained decoding partially addresses this
                                         neering; • Computing methodologies → Artificial intelligence.
                                                                                                                                 gap by guiding LLM generation using syntactic constraints [4, 9, 12,
                                                                                                                                 35, 38], and in some cases lightweight semantic rules [22, 25, 26, 34].
                                         Keywords                                                                                However, most existing methods still treat LLM outputs primarily as
                                         Large Language Models, Constrained Decoding, Partial Models,                            text, resulting in insufficient structural expressiveness and limited
                                         Semantic Validity, Neuro-Symbolic AI                                                    generalization to a broader range of SE scenarios.
                                         ACM Reference Format:                                                                      We argue that bridging this representation gap requires main-
                                         Boqi Chen, José Antonio Hernández López, and Aren A. Babikian. 2026.                    taining an explicit abstract representation during LLM generation.
                                         Projectional Decoding: Towards Semantic-Aware LLM Generation. In 34th                   Thus, we propose projectional decoding, a model-based constrained
                                         ACM Joint European Software Engineering Conference and Symposium on                     decoding framework inspired by the concept of projectional edit-
                                         the Foundations of Software Engineering (FSE Companion ’26), July 05–09,                ing [1, 19, 37], where a primary model representation is maintained
                                         2026, Montreal, QC, Canada. ACM, New York, NY, USA, 5 pages. https:                     during editing to enable continuous validation and early error detec-
                                         //doi.org/10.1145/3803437.3805571                                                       tion. Similarly, projectional decoding maintains a partial model [10]
                                                                                                                                 of the artifact during generation that captures both already gener-
                                         1    Introduction                                                                       ated structures and the uncertainty of yet-to-be-generated elements.
                                         Large language models (LLMs) are applied across many software                              During generation, each new token refines the partial model.
                                         engineering (SE) tasks [41], including code generation [15, 30, 32],                    This refinement enables incremental semantic validation directly
                                         debugging [33], and software modeling [5, 8, 20]. Unlike tasks in                       at the model level and allows the integration of established model-
                                         many other domains, SE tasks typically require outputs that conform                     based reasoning techniques [7, 29], supporting generation strategies
                                         to strict specifications. Generated artifacts must be both syntactically                that better capture SE-specific nuances than text-first approaches.
                                                                                                                                    We introduce projectional decoding as guided generation ap-
                                                                                                                                 proach, using it to derive semantic guardrails for the LLM token
                                                                                                                                 sampling process. We present a preliminary feasibility evaluation
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         FSE Companion ’26, Montreal, QC, Canada                                                 on a CLEVR program generation task [17]. The results show that
                                         © 2026 Copyright held by the owner/author(s).                                           even a simple token-masking strategy informed by partial models
                                         ACM ISBN 979-8-4007-2636-1/2026/07
                                         https://doi.org/10.1145/3803437.3805571
FSE Companion ’26, July 05–09, 2026, Montreal, QC, Canada                                                                            Chen et al.


can substantially improve semantic validity and task accuracy com-
pared to standard decoding or syntax-only constrained decoding.

2    Background and Challenges
Semantics in SE artifacts. Semantics captures the meaning and
intended properties of software artifacts beyond their syntactic
structure. In SE applications, model-based methods are commonly
used to define graph-based semantics that capture the complex
interconnections within a domain. Engineers formalize semantics
by defining a domain metamodel together with well-formedness con-
straints. Such metamodel can be linked explicitly with the grammar              Figure 1: Architecture of projectional decoding
rules with existing tools [3, 16]. Constraints specify properties that
metamodel instances (representing software artifacts) must satisfy
and are often expressed using graph patterns [2, 28] or temporal
                                                                         the LLM generation process. Figure 1 illustrates the architecture
logic [27]. Prior work has considered various semantic constraints
                                                                         of our proposed projectional decoding framework when applied
for LLM-generated artifacts, including invariants [32], behavioral
                                                                         to guided LLM generation. In the figure, gray nodes denote user-
specifications [6, 30], and structural consistency [5, 20]. Existing
                                                                         provided inputs, orange represents the standard LLM generation
studies consistently show that LLMs are prone to violating such
                                                                         pipeline, red components correspond to syntax-guided genera-
constraints, even under explicit prompting [5, 6, 20].
                                                                         tion used in existing approaches, and blue denotes the proposed
Constrained decoding refers to a class of approaches for produc-
                                                                         semantic-guided generation enabled by projectional decoding.
ing structured outputs by modifying the LLM generation strategy.
                                                                             Inspired by projectional editing techniques, projectional decoding
Existing methods primarily focus on enforcing syntactic correct-
                                                                         maintains a partial model representation [10, 24] equivalent to the
ness according to predefined grammar rules, typically context-free
                                                                         text artifact throughout generation. This partial model serves as
grammars [4, 9, 12, 35, 38]. In general, these approaches guide
                                                                         the primary representation for continuously validating semantic
generation by masking invalid tokens during sampling from the
                                                                         constraints as decoding progresses, thereby addressing C1.
output distribution [4, 38]. With recent advances in optimization
                                                                             At each decoding step, the LLM produces a next token probability
techniques, the computational overhead of constrained decoding
                                                                         distribution over vocabulary based on the current output prefix. In
has been substantially reduced, even negligible in some cases [12].
                                                                         parallel, the vocabulary is filtered by two validation modules. First,
   More recently, some approaches extend constrained decoding be-
                                                                         syntactic validation removes tokens that violate the grammar. Next,
yond syntax to address semantic validity. However, these methods
                                                                         semantic validation evaluates each remaining token by refining a
typically target particular classes of semantic constraints [22, 25]
                                                                         partial model and checking for any constraint violations. This re-
and rely on checking generated text directly rather than reason-
                                                                         finement captures uncertainty in the generation by introducing or
ing over the underlying structure [34]. ChopChop [26] reasons
                                                                         updating elements in the partial model according to the metamodel
over AST spaces to enable semantic pruning at the structural level.
                                                                         and constraints, addressing C2. Tokens whose refinements lead to
Projectional decoding targets more general SE artifacts whose se-
                                                                         semantic violations are discarded, while the remaining tokens are
mantics are defined over typed graphs rather than trees, explicitly
                                                                         used to mask the LLM output distribution for effective guidance, ad-
representing uncertainty through partial models to support incre-
                                                                         dressing C3. In practice, most tokens are discarded by the syntactic
mental validation on general constraints using graph patterns.
                                                                         validation, making semantic validaiton computationally tractable
Open challenges. We identify three key challenges in closing the
                                                                         even without additional caching or pruning. The selected token is
representation gap for semantic-aware LLM generation:
                                                                         then appended to the output prefix and is used to refine the partial
(C1) Abstract representation for semantic evaluation. Ensuring se-
                                                                         model. The process repeats until the generation is terminated.
mantic validity requires an expressive representation to enable
                                                                         Abstract representation. The construction and maintenance of a
automated error detection during the generation of SE artifacts.
                                                                         partial model enables automated violation detection through ex-
(C2) Capturing uncertainty. During generation, an LLM produces
                                                                         plicit support for error states during generation. This partial model
only an incomplete artifact, while the remaining is yet to be gen-
                                                                         serves as the primary enabler of semantic validation through its
erated. Evaluating semantic constraints over incomplete artifacts
                                                                         direct connection to the metamodel and constraints, which is not
requires explicit consideration of uncertainty.
                                                                         possible when text is used as the primary artifact.
(C3) Effective semantic guidance. LLM generation is a search process
                                                                             Partial models were originally introduced to capture uncertainty
over tokens. Efficiently guiding generation to a semantically valid
                                                                         during modeling processes [10] and can be represented with a spec-
solution with guarantees requires reasoning under uncertainty to
                                                                         ification language [24]. In projectional decoding, the partial model
enable effective exploration of the search space.
                                                                         represents an incomplete instance of a metamodel using a graph
                                                                         structure. Each element (node and edges) corresponds to a meta-
3    Towards Semantic-Aware LLM Generation                               model element and is associated with a four-valued logic [24]: certain
To address the challenges and enable semantic-aware LLM genera-          elements correspond to parts of the output that have already been
tion, we propose projectional decoding, a framework for constrained      completed, possible elements are still to be generated in subsequent
decoding that explicitly integrates structured representations into      steps, absent elements are ruled out during decoding according to
Projectional Decoding: Towards Semantic-Aware LLM Generation                                               FSE Companion ’26, July 05–09, 2026, Montreal, QC, Canada


                                                                             Task prompt:
the constraints, therefore excluded from the partial model, and error        Generate a Python function                     Entry
                                                                                                                                                                     max      0\n     x\n     return         ...
                                                                                                                 def sum_pos(xs:list[int])
elements indicating violations of semantic constraints.
                                                                             that returns the sum of all
                                                                                                                                                                            c) Syntactic Validation
                                                                             positive numbers in a list.

   While certain elements can be derived directly from the already           Semantic constraints:
                                                                                                                               Assign
                                                                                                                             total = 0
                                                                                                                                                                          max              0\n             x\n

generated output, absent and candidate possible elements are in-             Con1:                                                                                                        Expr
                                                                             return value is an interger                                                                   refine          refine          refine
                                                                                                                                 For
ferred from the syntactic and semantic constraints based on the
                                                                             ensure:type(return)=int                                                                     CallExpr
                                                                                                                                                                                      ConstExpr        VarRef
                                                                             Con2:                                         for x in xs:        Statement                  max            0               x
incomplete portions of the output. This inference process is anal-           total >= 0 for all paths




                                                                                                              def(total)
                                                                                                                                                                            param
                                                                             invariant:total>=0                                                                           Expr
                                                                                                                              AugAssign       +=
ogous to automatic code completion in projectional editors [37].              def sum_pos(
                                                                                 xs:list[int]                                   LHS            RHS                          d) Semantic Validation

Error elements may be introduced as a result of validation when               ):
                                                                                 total = 0
                                                                                                                            VarRef
                                                                                                                            total
                                                                                                                                             Expr
                                                                                                                                        VarRef CallExpr                    max      0\n                      ...
no refinement of the partial model satisfies the input constraints.              for x in xs:
                                                                                   total +=
                                                                                                                                        ConstExpr   ...                    Semantically Valid Tokens

Capturing uncertainty. A key feature of partial models is their                a) Current output prefix                     b) Current partial model

ability to represent uncertainty. This features allows syntactic and
semantic constraints to be evaluated directly at each generation         Figure 2: An example of projectional decoding for code gen-
step, before and after refinement, which enables reasoning about         eration; some partial model elements are excluded for clarity
potential new elements or any resulting violations.
   Syntactic validation. Based on the grammar and output prefix,             Q: How many objects are to the right of the red object and left to the brown object?

various existing constrained decoding techniques [12, 38] can be
used to determine the set of syntactically valid tokens, which ensure                                                                     3
                                                                                                                                                                            1.scene


the syntactic correctness of the underlying partial model.                                                                 Executor                         2.filter_color_          5.filter_color_

   Refinement and semantic validation. For each syntactically valid                                                                                                red                    brown


token, the partial model is updated to reflect the revised state of                   Program graph
                                                                                a) Program execution of the Clevr dataset
                                                                                                                                                               3.unique                   6.unique

the generated artifact. This update consists of two main steps: (1)               1["scene"] --> 2["filter_color_red"]                                      4.relate_right           ?. relate/filter...

refining existing partial elements based on the newly generated                   2 --> 3["unique"]
                                                                                  3 --> 4["relate_right"]
                                                                                                                                                   ?. filter/unique...           ?. And/Or
token, analogous to updating auto-completion suggestions, and (2)                 1 --> 5["filter_color_brown"]
                                                                                  5 --> 6["uni

introducing new (partial) elements as required by the metamodel               b) A partial DSL from an LLM for the question                    c) the partial model corresponding to b)

and semantic constraints. This update process can be realized using
existing partial model refinement techniques [36].                                   Figure 3: An example of the CLEVR program
   During refinement, the status of existing elements may change
from possible to either certain or absent, depending on whether they
are consistent with the provided token. When the refinement of an        (e.g., abstract syntax, control flow, and data flow) and incremen-
element violates any constraint, the element will be labeled as error.   tally constructs a corresponding partial model, shown in Figure 2.b.
This consistency check can be implemented using existing graph           In this partial model, certain elements (in purple) correspond to
pattern matching techniques [2, 29] for structural constraints, or       already-generated program components, while possible elements
abstract interpretation techniques [7] for behavior constraints.         (in yellow) represent incomplete parts inferred from the metamodel
   Any model containing error elements is considered invalid and         and constraints. For example, the Expr element represents the in-
discarded. Tokens that do not introduce violations preserve local        complete right hand side of the AugAssign statement.
validity and ensure that a valid output may potentially be generated.        Given the output prefix, syntactic validation derives the set of
Effective guided generation. The partial model not only captures         syntactically valid tokens shown in Figure 2.c. For example, return
the uncertainty introduced during generation but also constrains         is invalid on the right hand side of the AugAssign and is excluded.
the search space by reasoning about possible future valid elements.      Each remaining token is then evaluated by semantic validation
This enables the integration of various guided generation strategies.    (Figure 2.d) through partial model refinement. Some tokens, such
A naïve approach is to sample the next token from the LLM’s distri-      as max, introduce new possible elements, while others, such as x\n
bution restricted to tokens that satisfy both syntactic and semantic     and 0\n, only refine existing ones. Abstract interpretation [7] on
constraints. The sampled token is then appended to the prefix and        the model can identify that x\n may cause the value of total to be
used to refine the partial model for the next generation step. Gener-    negative and therefore violates constraint Con2, leaving only max
ation proceeds until termination when either a termination token is      and 0\n as candidates for the final sampling step. These valid tokens
produced or no semantically valid refinements remain. We discuss         will then be used to mask the LLM-generated token distribution.
the potential of more advanced strategies in Section 5.
Example. Figure 2 shows an example of projectional decoding ap-          4    Preliminary Evaluation
plied to code generation. The task prompt specifies the intended be-     We conduct a preliminary evaluation on the CLEVR program gen-
havior of a Python function and includes two semantic constraints        eration task [17] to show the feasibility of projectional decoding,
(defined in a dedicated constraint language) specifying a postcondi-     involving generating programs based on a question description. It is
tion (Con1) and invariant (Con2). Such constraints commonly arise        originally designed for visual question answering but has also been
in SE settings such as contract-based code generation [32].              used as a challenging benchmark for LLM-based generation [5].
   The grammar rules define the Python syntax for parsing. In our           Figure 3 shows an example of CLEVR program generation. The
approach, the LLM incrementally generates a Python program. An           goal is to generate a program in a domain-specific language (DSL)
example of a partially syntactically valid Python program is shown       that computes the answer to a question with a scene graph. The gen-
in Figure 2.a. In parallel, our method extracts structural information   erated program can be evaluated by execution to obtain an answer
FSE Companion ’26, July 05–09, 2026, Montreal, QC, Canada                                                                             Chen et al.


Table 1: Preliminary evaluation results on CLEVR program                 the 8B LLM (40%), demonstrating the practical benefits of enforcing
generation with semantic constraints for Qwen3 (in %).                   semantic constraints during generation. The syntactic guidance
                                                                         only provides improvements on accuracy for the smallest 4B LLM,
           No Guidance     Syntactic      Semantic (Ours)                showing that syntactic correctness alone is insufficient to ensure
  Size
         Syn. Sem. Acc. Syn. Sem. Acc. Syn. Sem. Acc. T                  high-quality generation. Moreover, the time overhead introduced
  4b     9.00   4.33   2.33   100 48.67 28.00 99.33 73.67 36.00 1.1x     by semantic guidance is moderate, ranging from 1.11x to 1.50x
  8b     87.67 60.33 38.67    100 61.00 37.33 99.00 79.67 40.00 1.5x     across different LLMs compared to no guidance.
  14b    83.33 55.44 37.67 100 58.33 36.67 99.67 73.33 37.33 1.1x
                                                                         5   Applications and Research Directions
                                                                         Application. Projectional decoding can be used to guarantee se-
                                                                         mantic validity in many SE applications, particularly in design-by-
(Figure 3.a) and compare it with the ground truth answer. We reuse
                                                                         contract scenarios. As shown in Section 3 and Section 4, it can
existing semantic constrains [5] to ensure the generated program
                                                                         be applied to contract-based and DSL-based program generation
is executable, including (Con1) type consistency (e.g., the argument
                                                                         with invariants and structural constraints. This form of constraint-
of filter must be of type set), (Con2) number of inputs (e.g., And
                                                                         guided generation naturally extends to other settings, including
must have exactly two inputs), and (Con3) acyclic structure, etc.
                                                                         compliance with safety regulations in API calling [6, 30], enforcing
LLMs. We evaluate the approaches with three Qwen3 [39] variants,
                                                                         well-formedness constraints in software modeling [5], and main-
including 4B, 8B, and 14B parameters. Qwen3 is an open-source
                                                                         taining cross-artifact consistency in larger software projects [31].
LLM that has showed strong performance on various generation
                                                                            More broadly, by integrating a abstract semantic representation,
tasks. While our approach is agnostic to the LLM, closed-source
                                                                         projectional decoding supports decoding-time validation of several
LLMs are not evaluated due to the lack of access to their internal
                                                                         interdependent artifact generation at the same time, where genera-
token distribution required for constrained decoding. To ensure a
                                                                         tion of one artifact (e.g., tests, design, or safety cases) immediately
consistent evaluation, we use greedy sampling (temperature=0) for
                                                                         constrains and informs the generation of others (e.g., code). This co-
all approaches with a few-shot prompt containing four examples.
                                                                         generation capability shows its potential as a unifying framework
Compared approaches. We compare three approaches: (1) No
                                                                         for semantic-aware automation with LLMs across the SE lifecycle.
Guidance, where the LLM generates the program without any guid-
                                                                         Research directions. Realizing the broader vision with projec-
ance; (2) Syntactic, where syntactic constrained decoding is applied,
                                                                         tional decoding raises several research directions for investigation.
we use LLGuidance [12]; and (3) Semantic, where projectional de-
                                                                            Effectiveness. By maintaining a partial model, projectional de-
coding is used. Figure 3.b and c show a partial CLEVR DSL and
                                                                         coding enables more advanced search strategies than text-only
the maintained partial model. In this case, several partial elements
                                                                         decoding and supports both token-level [34] and model-level back-
(e.g., filter, And, and relate) are derived by reasoning using the
                                                                         tracking during the generation process. Uncertainty-aware heuris-
semantic constraints. For example, the unique operator must be
                                                                         tics, such as prioritizing models with fewer possible elements, could
followed by a filter operator according to the type constraint
                                                                         further improve the effectiveness of semantic guidance [18].
and the two branches must be eventually joined by an And or Or
                                                                            Efficiency. Although the overhead observed in the preliminary
operator since there can only be a single output node.
                                                                         evaluation is modest, further optimizations are possible. For exam-
Metrics. We evaluate the approaches based on several metrics:
                                                                         ple, the validation could be parallelized with LLM inference, and
(1) Syntactic validity (Syn.), the percentage of syntactically correct
                                                                         incremental constraint evaluation techniques [2] could be explored
programs; (2) Semantic validity (Sem.), the percentage of programs
                                                                         to reduce redundant computations in decoding steps.
satisfying all semantic constraints; and (3) Accuracy (Acc.), the per-
                                                                            Generalization. Generalizing projectional decoding beyond spe-
centage of programs producing the correct answer when executed
                                                                         cific use cases requires systematic support for partial modeling
on a scene graph. All metrics are computed over all generated
                                                                         using a generalized framework. Existing work on partial model
results. For semantic guidance, we also measure the average gener-
                                                                         specification [24] and reasoning [23] provides a promising founda-
ation time per token (T ) relative to the no-guidance approach.
                                                                         tion for defining reusable abstractions and constraints that could
Results. As shown in Table 1, projectional decoding significantly
                                                                         enable projectional decoding across various SE domains.
improves semantic validity across all LLMs compared to both base-
lines. Notably, even the worst semantic validity achieved by projec-
tional decoding (73.33% with 14B LLM) substantially outperforms          6   Conclusion
the best semantic validity of other approaches (61.00% with syn-         This paper proposes projectional decoding, a novel conceptual frame-
tactic decoding on 8B LLM). However, none of the LLMs reach a            work for constrained decoding addressing the representation gap
perfect semantic validity even with semantic guidance. This result       for semantic evaluation by maintaining a partial model during gen-
may be caused by the limitation that LLM generation explored a           eration. Projectional decoding tackles key challenges by providing
decoding path where no semantically valid solutions are possible, in     an abstract representation for semantic evaluation, capturing uncer-
which case generation terminates early with a semantically invalid       tainty during generation, and enabling effective semantic guidance.
output. Future work can explore advanced search strategies such          To realize the vision of semantic-aware LLM generation, future
as backtracking to further improve the semantic validity.                work will explore advanced search strategies, optimizations, and
    The improvement for semantic validity also leads to better task      broader applications in SE tasks requiring semantic validity in com-
accuracy in 2 out of 3 cases, achieving the best overall accuracy on     parison with existing structured decoding approaches.
Projectional Decoding: Towards Semantic-Aware LLM Generation                                                       FSE Companion ’26, July 05–09, 2026, Montreal, QC, Canada


References                                                                                 [21] Michael R Lyu, Baishakhi Ray, Abhik Roychoudhury, Shin Hwei Tan, and Patana-
 [1] Thorsten Berger, Markus Völter, Hans Peter Jensen, Taweesap Dangprasert, and               mon Thongtanunam. 2025. Automatic programming: Large language models
     Janet Siegmund. 2016. Efficiency of projectional editing: A controlled experiment.         and beyond. ACM Transactions on Software Engineering and Methodology 34, 5
     In Proceedings of the 24th ACM SIGSOFT International Symposium on Foundations              (2025), 1–33.
     of Software Engineering. ACM, 763–774.                                                [22] Franklin Ma and Alan J Hu. 2025. Logically Constrained Decoding. In Proceedings
 [2] Gábor Bergmann, Ákos Horváth, István Ráth, Dániel Varró, András Balogh,                    of The 3rd Workshop on Mathematical Natural Language Processing. ACL, 150–167.
     Zoltán Balogh, and András Ökrös. 2010. Incremental evaluation of model queries        [23] Kristóf Marussy, Attila Ficsor, Oszkár Semeráth, and Dániel Varró. 2024. Refinery:
     over EMF models. In Model Driven Engineering Languages and Systems - 13th                  Graph solver as a service: Refinement-based generation and analysis of consistent
     International Conference. Springer, 76–90.                                                 models. In Proceedings of the 2024 IEEE/ACM 46th International Conference on
                                                                                                Software Engineering: Companion Proceedings. ACM, 64–68.
 [3] Lorenzo Bettini. 2016. Implementing domain-specific languages with Xtext and          [24] Kristóf Marussy, Oszkár Semeráth, Aren A. Babikian, and Dániel Varró. 2020. A
     Xtend. Packt Publishing Ltd.                                                               Specification Language for Consistent Model Generation based on Partial Models.
 [4] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2023. Prompting is pro-              Journal of Object Technology 19, 3 (2020), 3:1–22.
     gramming: A query language for large language models. Proceedings of the ACM          [25] Niels Mündler, Jingxuan He, Hao Wang, Koushik Sen, Dawn Song, and Mar-
     on Programming Languages 7, PLDI (2023), 1946–1969.                                        tin Vechev. 2025. Type-Constrained Code Generation with Language Models.
 [5] Boqi Chen, Ou Wei, Bingzhou Zheng, and Gunter Mussbacher. 2025. Accurate and               Proceedings of the ACM on Programming Languages 9, PLDI (2025), 601–626.
     Consistent Graph Model Generation from Text with Large Language Models. In            [26] Shaan Nagy, Timothy Zhou, Nadia Polikarpova, and Loris D’Antoni. 2026. Chop-
     28th ACM/IEEE International Conference on Model Driven Engineering Languages               Chop: A Programmable Framework for Semantically Constraining the Output of
     and Systems. IEEE, 130–141.                                                                Language Models. Proceedings of the ACM on Programming Languages 10, POPL
 [6] Zhaorun Chen, Mintong Kang, and Bo Li. 2025. ShieldAgent: Shielding Agents                 (2026), 1905–1932.
     via Verifiable Safety Policy Reasoning. In Forty-second International Conference      [27] Amir Pnueli. 1977. The temporal logic of programs. In 18th annual symposium
     on Machine Learning.                                                                       on foundations of computer science. ieee, 46–57.
 [7] Patrick Cousot and Radhia Cousot. 1977. Abstract interpretation: a unified            [28] Mark Richters and Martin Gogolla. 2002. OCL: Syntax, semantics, and tools.
     lattice model for static analysis of programs by construction or approximation             In Object Modeling with the OCL: The Rationale behind the Object Constraint
     of fixpoints. In Conference Record of the Fourth ACM Symposium on Principles of            Language. Lecture Notes in Computer Science, Vol. 2263. Springer, 42–68.
     Programming Languages. ACM, 238–252.                                                  [29] Oszkár Semeráth and Dániel Varró. 2017. Graph Constraint Evaluation over
 [8] Juri Di Rocco, Davide Di Ruscio, Claudio Di Sipio, Phuong T Nguyen, and Riccardo           Partial Models by Constraint Rewriting. In Theory and Practice of Model Trans-
     Rubei. 2025. On the use of large language models in model-driven engineering.              formation - 10th International Conference (Lecture Notes in Computer Science,
     Software and Systems Modeling 24, 3 (2025), 923–948.                                       Vol. 10374). Springer, 138–154.
 [9] Yixin Dong, Charlie F Ruan, Yaxing Cai, Ziyi Xu, Yilong Zhao, Ruihang Lai,            [30] Da Song, Yuheng Huang, Boqi Chen, Tianshuo Cong, Randy Goebel, Lei Ma, and
     and Tianqi Chen. 2025. XGrammar: Flexible and efficient structured generation              Foutse Khomh. 2026. Evaluating Implicit Regulatory Compliance in LLM Tool
     engine for large language models. Proceedings of Machine Learning and Systems              Invocation via Logic-Guided Synthesis. arXiv preprint arXiv:2601.08196 (2026).
     7 (2025).                                                                             [31] Bastien Sultan and Ludovic Apvrille. 2024. AI-driven consistency of SysML
[10] Michalis Famelis, Rick Salay, and Marsha Chechik. 2012. Partial models: Towards            diagrams. In Proceedings of the ACM/IEEE 27th International Conference on Model
     modeling and reasoning with uncertainty. In 34th International Conference on               Driven Engineering Languages and Systems. ACM, 149–159.
     Software Engineering. IEEE Computer Society, 573–583.                                 [32] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024. Clover: Closed-
[11] Usman Gohar, Michael C Hunter, Robyn R Lutz, and Myra B Cohen. 2024. Code-                 loop verifiable code generation. In AI Verification - First International Symposium.
     feater: Using LLMs to find defeaters in assurance cases. In Proceedings of the 39th        Springer, 134–155.
     IEEE/ACM International Conference on Automated Software Engineering. ACM,             [33] Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu,
     2262–2267.                                                                                 Hui Haotian, Liu Weichuan, Zhiyuan Liu, et al. 2024. Debugbench: Evaluating
[12] Guidance AI. 2024. LLGuidance: Fast Structured Generation for Large Language               debugging capability of large language models. In Findings of the Association for
     Models. https://github.com/guidance-ai/llguidance.                                         Computational Linguistics. ACL, 4173–4198.
[13] Junda He, Christoph Treude, and David Lo. 2025. LLM-Based Multi-Agent Systems         [34] Shubham Ugare, Rohan Gumaste, Tarun Suresh, Gagandeep Singh, and Sasa
     for Software Engineering: Literature Review, Vision, and the Road Ahead. ACM               Misailovic. 2025. IterGen: Iterative Semantic-aware Structured LLM Genera-
     Transactions on Software Engineering and Methodology 34, 5 (2025), 124:1–124:30.           tion with Backtracking. In The Thirteenth International Conference on Learning
[14] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng,                      Representations.
     Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al.          [35] Shubham Ugare, Tarun Suresh, Hangoo Kang, Sasa Misailovic, and Gagandeep
     2023. MetaGPT: Meta programming for a multi-agent collaborative framework.                 Singh. 2025. SynCode: LLM Generation with Grammar Augmentation. Transac-
     In The Twelfth International Conference on Learning Representations.                       tions on Machine Learning Research (2025).
[15] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming
                                                                                           [36] Dániel Varró, Oszkár Semeráth, Gábor Szárnyas, and Ákos Horváth. 2018. To-
     Cui. 2023. Agentcoder: Multi-agent-based code generation with iterative testing
                                                                                                wards the automated generation of consistent, diverse, scalable and realistic
     and optimisation. arXiv preprint arXiv:2312.13010 (2023).
                                                                                                graph models. In Graph Transformation, Specifications, and Nets - In Memory of
[16] JetBrains. 2026. JetBrains MPS: The Meta Programming System. https://www.
                                                                                                Hartmut Ehrig (Lecture Notes in Computer Science, Vol. 10800). Springer, 285–312.
     jetbrains.com/mps/. Accessed: 2026-01-22.
                                                                                           [37] Markus Voelter, Tamás Szabó, Sascha Lisson, Bernd Kolb, Sebastian Erdweg, and
[17] Justin Johnson, Bharath Hariharan, Laurens Van Der Maaten, Li Fei-Fei, C
                                                                                                Thorsten Berger. 2016. Efficient development of consistent projectional editors
     Lawrence Zitnick, and Ross Girshick. 2017. CLEVR: A diagnostic dataset for
                                                                                                using grammar cells. In Proceedings of the 2016 ACM SIGPLAN International
     compositional language and elementary visual reasoning. In IEEE Conference on
                                                                                                Conference on Software Language Engineering. 28–40.
     Computer Vision and Pattern Recognition. IEEE Computer Society, 1988–1997.
                                                                                           [38] Brandon T Willard and Rémi Louf. 2023. Efficient guided generation for large
[18] Parv Kapoor, Akila Ganlath, Michael Clifford, Changliu Liu, Sebastian Scherer,
                                                                                                language models. arXiv preprint arXiv:2307.09702 (2023).
     and Eunsuk Kang. 2025. Constrained Decoding for Robotics Foundation Models.
                                                                                           [39] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng,
     arXiv preprint arXiv:2509.01728 (2025).
                                                                                                Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. 2025. Qwen3 technical
[19] Louis-Edouard Lafontant and Eugene Syriani. 2020. Gentleman: a light-weight
                                                                                                report. arXiv preprint arXiv:2505.09388 (2025).
     web-based projectional editor generator. In ACM/IEEE 23rd International Confer-
                                                                                           [40] Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kasriel, Kaiyu Yang, and Dawn
     ence on Model Driven Engineering Languages and Systems, Companion Proceedings.
                                                                                                Song. 2025. VERINA: Benchmarking Verifiable Code Generation. arXiv preprint
     ACM, 1:1–1:5.
                                                                                                arXiv:2505.23135 (2025).
[20] José Antonio Hernandez López, Máté Földiák, and Dániel Varró. 2024. Text2VQL:
                                                                                           [41] Quanjun Zhang, Chunrong Fang, Yang Xie, Yaxin Zhang, Yun Yang, Weisong Sun,
     teaching a model query language to open-source language models with ChatGPT.
                                                                                                Shengcheng Yu, and Zhenyu Chen. 2023. A survey on large language models for
     In Proceedings of the ACM/IEEE 27th International Conference on Model Driven
                                                                                                software engineering. arXiv preprint arXiv:2312.15223 (2023).
     Engineering Languages and Systems. 13–24.
