                                                 Translator vs. Challenger: Adversarial Agentic
                                                       Learning for C-to-Rust Translation
                                                                         Chaofan Wang, Xiaodong Gu, Yuling Shi, Chao Hu, Beijun Shen*
                                                                                             Shanghai Jiao Tong University
                                                                             {chaofwang, xiaodong.gu, yuling.shi, ythere, bjshen}@sjtu.edu.cn


                                            Abstract—C-to-Rust translation remains challenging due to             Adversarial Agentic Learning
                                         the substantial semantic gap between the two languages. Recent
                                         experience-enhanced LLM translators improve translation qual-                         Translator                                          Challenger
                                                                                                                               C   Rust                                 Target       Test Protocol
                                         ity by learning reusable insights from prior failures and repairs.                                   Challenging problems                    Correctness
arXiv:2609.15381v1 [cs.SE] 14 Sep 2026




                                         Yet learned insights do not automatically constitute reusable                                                                                Performance
                                                                                                                                                                                      Memory Safety
                                         translation knowledge: because they are derived from sparse and                                                                              Edge Cases
                                                                                                                                                      Refiner                         Concurrency
                                         program-specific translation traces, they often contain missing                                                                              Extensibility
                                         conditions, narrow applicability boundaries, or overlooked corner
                                         cases. This limits their robustness and generalizability when
                                                                                                                                   Feedback
                                         applied to new translation scenarios. We present T RAIL, an ad-
                                         versarial agentic learning framework for robust C-to-Rust trans-                                                  Insight Refinement
                                         lation. T RAIL employs two collaborating agents: a Translator that
                                         derives candidate insights from translation failures and accepted        Translation Insight Bank

                                         repairs, and a Challenger that actively searches for weaknesses,
                                         gaps, and boundary cases through adversarial challenges. To
                                         improve the robustness of individual insights and the complete-
                                         ness of insight collections, T RAIL performs adversarial learning           Translation Insights         Robust Insights                Insight Network

                                         at two levels. Individual-insight adversarial learning repeatedly
                                         stress-tests each insight to refine its applicability conditions      Fig. 1. Illustration of adversarial agentic learning for robust and generalizable
                                         and constraints, while compositional insight adversarial learning     translation insights.
                                         strengthens groups of related insights by exposing conflicts, gaps,
                                         and uncovered corner cases. By repeatedly challenging learned
                                         insights and their compositions with executable counterexam-
                                         ples, T RAIL transforms trace-specific translation experience into    uncompilable or semantically incorrect Rust code, particularly
                                         robust, reusable, and generalizable translation knowledge. We         for complex, project-specific scenarios [4], [9]–[11]. These
                                         evaluate T RAIL on two project-level benchmarks, CRUST-Bench          challenges motivate translation systems that can continuously
                                         and SmartC2Rust-Bench. Compared with the strongest LLM-               acquire and refine reusable knowledge from prior translation
                                         based baseline, T RAIL achieves average relative improvements         attempts, enabling them to handle diverse coding patterns and
                                         of 23.1% in syntax accuracy and 15.9% in semantic accuracy.
                                         Furthermore, the adversarially refined insights transfer effec-       project-specific corner cases.
                                         tively across benchmarks, demonstrating strong generalizability          Existing approaches to C-to-Rust translation have increas-
                                         across diverse C-to-Rust translation tasks.                           ingly shifted from manually engineered knowledge toward
                                            Index Terms—C-to-Rust Translation, Adversarial Agentic             automatically learned translation experience. Early systems
                                         Learning, Translation Knowledge Refinement, Experience-
                                         Enhanced Agents.                                                      augment LLMs with handcrafted semantic mappings [10] and
                                                                                                               translation guidelines [11] to bridge the semantic gap between
                                                                   I. I NTRODUCTION                            C and Rust. While effective for recurring patterns, such
                                            The growing adoption of Rust has created increasing de-            manually authored knowledge is costly to construct, difficult to
                                         mand for automated migration [1], [2] of existing C code-             maintain, and inherently limited in its coverage of real-world
                                         bases [3], [4]. However, C-to-Rust translation remains chal-          C codebases. Motivated by recent advances in experience-
                                         lenging due to the substantial semantic gap between the two           enhanced agents [12]–[15], newer C-to-Rust translators auto-
                                         languages. While C relies heavily on raw pointers, manual             matically learn reusable insights from translation failures and
                                         memory management, and implicit type conversions, Rust                successful repairs [9], [11], [16]. However, existing approaches
                                         enforces strict ownership, borrowing, and compile-time safety         primarily focus on accumulating learned insights, implicitly
                                         guarantees. Bridging this gap requires more than syntax-              assuming that insights derived from past translation traces
                                         level translation: translators must infer and reconstruct safety-     are reusable. In practice, because such insights originate from
                                         related semantics [5]–[8] that are often implicit in C pro-           sparse and program-specific experiences, they often capture
                                         grams. Consequently, rule-based techniques and zero-shot              local heuristics rather than general translation knowledge, leav-
                                         Large Language Model (LLM) generation frequently produce              ing missing conditions, narrow applicability boundaries, and
                                                                                                               overlooked corner cases. Consequently, insights that appear
                                           * Beijun Shen is the corresponding author.                          effective for previously observed failures may not generalize to
      Single-Insight Adversarial Learning
                                                       𝐼 = 𝑇𝑟𝑖𝑔𝑔𝑒𝑟, 𝐺𝑜𝑎𝑙, 𝐶𝑜𝑛𝑠𝑡𝑟𝑎𝑖𝑛𝑡, 𝑅𝑖𝑠𝑘                 Analysis
         Refinement             Evolution                                                                   𝐼" , 𝐼#                  Composition
          evidence 𝑒!                                                                                  support / conflict /
                              ∆! + 𝑒!                                                                    independent                 +𝐶𝑜𝑣𝑒𝑟𝑎𝑔𝑒 𝑆
                                                                                                                                 max +𝜆' 𝑆𝑢𝑝𝑝𝑜𝑟𝑡 𝑆
                                                                                                                                 $⊆ℬ
                                                                                                                                     −𝜆( 𝐶𝑜𝑛𝑓𝑙𝑖𝑐𝑡 𝑆

         Translation           Challenging                                                                Refinement
                                                                                                         Refinement
           𝑞+𝐼 !                                                                                                                     selected set 𝑆
              ▽                 challenge                                                                joint challenge
                             𝑞 = < 𝐶, 𝑅, 𝐻, 𝑂 >                                                        translator execute
         Rust Code 𝑥!


                                                                           insight retrieval

                                                                                                  Insights !



                                                           C → Rust                 cargo utils                 insight mining

                                                            CR

Fig. 2. Overview of T RAIL. A Challenger, Translator, and Refiner form an adversarial challenge–translate–refine loop that transforms translation experience
into reusable knowledge. Adversarial refinement at both the individual-insight and compositional levels improves the robustness and completeness of learned
insights for project-level C-to-Rust translation.



unseen coding patterns, alternative APIs, or interactions with                      The main contributions of this work can be summarized as:
other translation constraints.                                                      • We propose T RAIL , the first adversarial agentic learning
   To address this challenge, we propose T RAIL, an adver-                            framework for C-to-Rust translation. Through adversar-
sarial agentic learning framework that continuously refines                           ial interaction between a Translator and a Challenger,
translation insights through interaction among a Translator, a                        T RAIL continuously refines learned insights and trans-
Challenger, and a Refiner. Unlike prior approaches that treat                         forms trace-specific translation experience into reusable
learned insights as static knowledge to be validated and stored,                      translation knowledge.
T RAIL formulates insight learning as a continual adversar-                         • We design a two-level adversarial learning mechanism
ial process: the Translator extracts candidate insights from                          that systematically refines learned translation insights.
failures and successful repairs, while the Challenger actively                        By challenging insights both individually and composi-
constructs executable counterexamples to expose missing con-                          tionally, the mechanism improves their robustness, com-
ditions, boundary cases, and incorrect assumptions. A Refiner                         pleteness, and reusability before deployment in future
then converts the resulting execution feedback into structured                        translations.
insight updates through iterative challenge–translate–refine                        • We evaluate T RAIL on 120 C-to-Rust translation projects
cycles, progressively turning trace-specific experiences into                         with multiple LLM backends. Results show that T RAIL
robust, reusable knowledge. Our adversarial learning operates                         consistently outperforms state-of-the-art baselines and
at two levels: at the individual level, it refines each insight to                    that adversarially refined insights transfer effectively
produce robust translation knowledge under diverse scenarios;                         across benchmarks, demonstrating strong generalizability.
at the compositional level, it jointly challenges groups of
related insights to surface conflicts, gaps, and interaction-                                            II. T RAIL F RAMEWORK
induced corner cases, organizing them into a coherent insight
network that improves both coverage and consistency. Figure 1                    A. Framework Overview
illustrates the overall idea of our framework.                                      The core premise of T RAIL is that C-to-Rust translation
   We evaluate T RAIL on 100 C-to-Rust translation projects                      experience does not directly yield reliable reusable knowledge.
using three backend LLMs. Results show that T RAIL con-                          Although failure-and-repair traces may expose useful heuris-
sistently outperforms LLM-based baselines, achieving aver-                       tics, the induced insights are often partial, over-specialized to
age relative improvements of 23.1% in syntax accuracy and                        specific programs, or invalid under unseen C idioms. Instead
15.9% in semantic accuracy. Furthermore, a transfer study                        of passively accumulating such insights in a static repository,
on 20 projects from an independent benchmark shows that                          T RAIL formulates translation as an online adversarial learn-
adversarially refined insights remain effective on unseen data,                  ing process, in which insights are continuously mined from
suggesting that T RAIL learns generalizable and reusable trans-                  translation traces, challenged through executable tests, and
lation knowledge.                                                                iteratively refined during project migration.
                              TABLE I                                             Algorithm 1: Adversarial Challenge–Translate–Refine loop
               A N E XAMPLE OF A T RANSLATION I NSIGHT
                                                                                Input: Initial refinement target Z (0) , maximum rounds K
                                                                                Output: Refined target Z ⋆
  Translation Insight: Pointer–Buffer Coupling                                1 for r ← 0 to K − 1 do

  [Trigger]                                                                   2     qr ← C HALLENGE(Z (r) ); // Challenger probes
  C code passes raw pointers, arrays, allocated buffers, string lengths,              a boundary
  capacities, or null terminators.                                            3     if ¬ S ANITY C HECK(qr , Z (r) ) then
  [Goal]                                                                      4         Z (r+1) ← Z (r) ;
  Translate the pointer–buffer relation into Rust slices, Vec, or String
  while preserving length, capacity, and terminator semantics.
                                                                              5         continue;
  [Constraint]                                                                6        xr ← T RANSLATE(qr , Z (r) ); // Translator uses
  Bounds-check every index derived from C pointer arithmetic and pre-
                                                                                        Z (r) as constraint(s)
  serve whether a terminator is included in the logical length.
  [Risk]                                                                      7        er ← E XECUTE(xr , qr );        // Compile and test
  Rust code may still compile while dropping trailing-NUL handling,                     the result
  overrunning slices, or allocating the wrong capacity.                       8        ∆r ← R EFINE(Z (r) , qr , xr , er );        // Refiner
  [Tags]                                                                                attributes failures
  pointer-buffer, ownership-transfer, nul-terminated-string.                  9        Z (r+1) ← E VIDENCE G ATE(Z (r) , ∆r , er ); // Accept
                                                                                        supported updates only
   Figure 2 illustrates the overall architecture of T RAIL. The              10    Z ⋆ ← Z (K) ;
framework is built around structured translation insights as                 11    return Z ⋆ ;
first-class, evolving knowledge units (Section II-B), and orga-
nized into three collaborating agents: a Challenger, a Transla-
tor, and a Refiner. The Challenger synthesizes executable C-                 the insight. In addition, each insight is annotated with a set
to-Rust challenges that expose missing conditions, boundary                  of lightweight semantic tags to facilitate retrieval and cross-
cases, or implicit assumptions in existing insights. Conditioned             insight composition. Table I presents a representative buffer-
on selected insights, the Translator generates Rust implemen-                related insight.
tations that satisfy the required interface while preserving the
observable behavior of the original C program. Execution                     C. Single-Insight Adversarial Learning
results, including compilation outcomes and test executions,
provide concrete feedback, which the Refiner uses to revise the                 T RAIL treats each learned translation insight as a falsifiable
corresponding insights. Together, these agents form a closed-                hypothesis and subjects it to iterative adversarial testing. The
loop challenge–translate–refine process for continuously im-                 objective of single-insight adversarial learning is to actively
proving translation knowledge.                                               construct counterexamples that expose the boundary condi-
   To enhance robustness and completeness, T RAIL performs                   tions and failure modes of an insight, thereby improving its
adversarial learning at two levels. At the individual-insight                robustness and generality.
level, executable challenges probe whether a single insight                     Given an insight I, T RAIL performs up to K rounds of
captures a specific C-to-Rust constraint, such as pointer–buffer             counterexample-driven refinement. In each round, the Chal-
coupling or ownership transfer semantics (Section II-C). At                  lenger generates an executable C-to-Rust challenge targeting
the compositional level, multiple related insights are jointly               the applicability boundary of I, the Translator solves it under
evaluated under coordinated challenges to expose inconsis-                   I and the required Rust interface, and the Refiner attributes
tencies, coverage gaps, and interaction-induced corner cases                 compiler or test evidence to insight deficiencies. An evidence
(Section II-D). The resulting insight bank evolves into a                    gate then determines whether the insight is updated or retained
structured, reusable knowledge base supporting project-level                 unchanged, and the resulting version is carried to the next
C-to-Rust translation and automated repair (Section II-E).                   round. After K rounds, the final refined version is admitted
                                                                             to the insight bank, while candidates lacking sufficient tool-
B. Translation Insight Representation                                        observed evidence are discarded. Algorithm 1 summarizes this
   To enable systematic adversarial refinement, T RAIL rep-                  Challenge–Translate–Refine loop.
resents each translation insight as a structured, executable                    Specifically, each adversarial refinement round proceeds
knowledge unit that captures recurring C-to-Rust translation                 through four steps:
patterns extracted from translation traces.                                     1) Challenge Generation: The goal of challenge genera-
   Formally, an insight is defined as a 4-tuple:                             tion is to construct test cases that maximize the likelihood
                                                                             of falsifying an incomplete insight. Given the current insight
           I = ⟨Trigger , Goal , Constraint, Risk ⟩                    (1)
                                                                             instance I (r) = ⟨TI , GI , ΦI , ρI ⟩, the Challenger first derives
where Trigger specifies the applicability conditions under                   an activation predicate aI = P REDICATE(TI ) that identi-
which the insight is activated, Goal characterizes the intended              fies programs capable of triggering the targeted transforma-
translation effect, Constraint encodes semantic or structural re-            tion behavior, and extracts adversarial boundary conditions
quirements that must be preserved, and Risk describes potential              bI = B OUNDARY(ΦI , ρI ) that characterize critical edge cases
failure modes or unintended side effects induced by applying                 implied by the insight specification.
   Based on aI and bI , the Challenger instantiates a C-to-           cation. Given a proposed update ∆r , T RAIL applies it to
Rust challenge q = ⟨Cq , Rq , Hq , Oq ⟩, where Cq specifies           the current insight I (r) to obtain a candidate Iˆ(r+1) . The
the C program exercising the targeted idiom, Rq fixes the             Translator then re-executes the same challenge under Iˆ(r+1)
Rust-facing interface constraints, Hq defines the execution           as an active constraint.
harness for invoking the translated implementation, and Oq               If the replay succeeds, the update is accepted and Iˆ(r+1) be-
encodes the expected C semantics as executable assertions.            comes the insight for the next round. Otherwise, the proposal is
By combining activation conditions with boundary constraints          rejected and I (r) is retained. Insights remain unchanged when
under both source-language semantics and target-interface             (i) the original challenge already succeeds under I (r) , or (ii)
requirements, the generated challenge is designed to expose           no refinement proposal is generated by the Refiner. After the
missing preconditions, over-generalized assumptions, and un-          final round, the latest accepted version is taken as the refined
handled corner cases in the current insight.                          insight.
   Before execution, T RAIL applies three sanity checks to filter
generated challenges, ensuring execution budget is spent on           D. Compositional Insight Adversarial Learning
valid and diagnostic cases. L EAK removes duplicates and near-
duplicates, ACTIVATES verifies triggers and boundary condi-              Improving individual insights does not guarantee that they
tions, and T OOL C HECK ensures executability by checking that        form a complete and coherent body of translation knowledge.
the C snippet runs, the Rust harness type-checks against a stub       In project-level C-to-Rust translation, multiple insights are
for Rq , and the oracle passes under cargo test.                      often activated simultaneously along shared call chains or
   2) Insight-Constrained Translation: Each challenge is              data flows. Although each insight may be correct in isolation,
evaluated by the Translator with the current insight I (r)            their composition can introduce conflicts, missing coordination
injected as an active constraint. Conditioned on I (r) , it synthe-   constraints, or corner cases that are not observable in single-
sizes Rust code that satisfies the required interface Rq while        insight refinement. For example, an insight preserving a C
preserving the observable behavior of Cq .                            terminator may conflict with another constructing a Rust slice
   The resulting implementation is validated via cargo                excluding it; similarly, ownership-transfer rules may interfere
check and cargo test. If both succeed, the challenge is               with insights treating the same buffer as a borrowed view.
marked as solved, and T RAIL records the implementation and           Thus, locally correct insights may lead to inconsistent global
passing trace as positive evidence that I (r) covers the targeted     behavior.
behavior. Otherwise, compilation or test failures are treated            To address this limitation, T RAIL performs adversarial
as counterexamples; the failed program, compiler diagnostics,         learning at the compositional level. It jointly challenges co-
interface mismatches, and assertion failures are forwarded to         activated insight sets within a module and evaluates their
the Refiner to update I (r) .                                         combined constraints. Through joint conflict detection and
   3) Failure-Driven Refinement: When a challenge reveals             coverage-aware set refinement, T RAIL determines safe com-
a failure, the Refiner performs failure attribution to establish      posability, required precedence or applicability constraints, and
a diagnostic link between observed errors and the targeted            interaction-induced translation principles.
insight. Insight updates are proposed only when grounded                 Specifically, compositional adversarial learning proceeds
in concrete evidence, including compiler diagnostics, failing         through three steps:
assertions, or execution traces.                                         1) Counterfactual Interaction Analysis: Starting from the
   Attributed failures are categorized into four insight-level        insight bank B, whose entries have passed single-insight adver-
deficiencies, each mapped to a field-level update. A Trigger          sarial learning, T RAIL analyzes pairwise interactions among
gap denotes missing applicability conditions (e.g., requiring         insights that may co-activate in the same C-to-Rust context.
a visible length or terminator for a pointer rule), refining the      For an insight pair (Ia , Ib ), T RAIL performs counterfactual
Trigger. A Goal mismatch indicates an incorrect or incom-             reasoning [17]–[19] over their Trigger, Goal, Constraint, Risk,
plete objective (e.g., preserving bytes but violating the Rust-       C-idiom tags, and Rust-facing obligations to classify their
facing API contract), revising the Goal. A Constraint violation       relation as support, independent, or conflict. The analysis
captures insufficient or overly permissive constraints (e.g.,         asks whether removing, weakening, or reordering one insight
unchecked slice construction or violated ownership assump-            would alter the Rust interface, ownership model, aliasing
tions), strengthening the Constraint. A Missing risk records          assumptions, or executable behavior required by the other,
unmodeled failure modes (e.g., passing cargo check while              yielding support and conflict scores sab , cab ∈ [0, 1] together
mishandling trailing NUL bytes, introducing unintended alias-         with explanations.
ing, or altering allocation capacity), extending the Risk with           Predicted conflicts are not immediately rejected. Instead,
explicit guards or failure conditions.                                they are flagged for adversarial testing to distinguish genuine
   Refinement is triggered only by actionable failures; transla-      inconsistencies from cases that require refined applicability
tor noise, invalid challenges, and successful executions do not       conditions, strengthened constraints, or explicit precedence
produce updates.                                                      rules. This is necessary because apparent conflicts often arise
   4) Evidence-Gated Insight Evolution: The evidence gate             from conflating internal C representation requirements (e.g.,
validates each refinement proposal via replay-based verifi-           preserving a terminator in an allocated buffer) with external
Rust API obligations (e.g., exposing only initialized data via                    exposes a non-representable pattern, the Refiner introduces a
a slice).                                                                         new candidate insight, which is re-entered into single-insight
   2) Coverage-Aware Insight Composition: Given the in-                           adversarial learning before entering the bank.
teraction graph, T RAIL constructs compact insight sets for                          Through iterative joint challenges and evidence-driven re-
joint adversarial testing. Each set is expected to repre-                         finement, T RAIL improves interaction coherence and the com-
sent a coherent C-to-Rust feature, and co-activate dur-                           pleteness of learned C-to-Rust translation knowledge.
ing module-level translation. Candidate sets are formed
from related triggers and overlapping language-idiom tags,                        E. Inference with Learned Insights
such as pointer-buffer, ownership-transfer,
                                                                                     Building on the adversarially refined insight bank, T RAIL
nul-terminated-string, and api-preservation.
                                                                                  performs project-level C-to-Rust translation as a closed-loop
   To balance coverage and compatibility, T RAIL selects an
                                                                                  inference process that interleaves insight utilization and online
insight set S ⊆ B by maximizing
                                                                                  continual learning. The inference pipeline is implemented
                                                                                  by three cooperating agents: the Translator, which generates
  max    Coverage(S) +λ1 Support(S) −λ2 Conflict(S)                         (2)   initial Rust implementations; the Repairer, which fixes cargo
  S⊆B
                                                                                  check and cargo test failures; and the Reflector, which
         |   {z    }     |   {z   }     |   {z    }
        C-to-Rust tag coverage   LLM support score     LLM conflict score
                                                                                  distills reusable translation insights from execution traces and
where Coverage(S) measures normalized coverage of                                 repair trajectories.
distinct C-to-Rust semantic tags, defined as | ∪I∈S                                  Given a C project, T RAIL first applies macro expansion and
tags(I)|/ min(B, |T |). Here B denotes the maximum number                         constructs a dependency graph to derive a topological order
of insights per joint challenge, and T is the tag vocabulary of                   over functions. For each function, context-relevant insights are
the candidate set. For |S| > 1, Support(S) and Conflict(S)                        retrieved to guide both translation and subsequent repair. The
are defined as average pairwise LLM scores:                                       generated Rust code is first validated and iteratively corrected
                                   2       X                                      using compilation feedback, then integrated into the project
             Support(S) =                      sab ,
                              |S|(|S| − 1)                                        and further improved based on test execution signals. To
                                           a<b
                                                            (3)                   close the learning loop, the Reflector mines reusable insights
                                   2       X
             Conflict(S) =                     cab .                              from translation and repair traces, continuously enriching the
                              |S|(|S| − 1)                                        insight bank with newly observed patterns and failure-driven
                                                     a<b

For singleton sets, both terms are zero.                                          refinements.
   In practice, T RAIL constructs compositions via greedy                            Specifically, the pipeline consists of five stages.
optimization of Eq. 2. This approximation suffices as the                            1) Project Structuring for Translation: T RAIL first con-
objective is interpretable adversarial evaluation rather than                     structs a translation-ready project representation and estab-
global subset optimality. The resulting set captures realistic                    lishes a dependency-aware translation order. It macro-expands
translation scenarios, such as helper chains that compute buffer                  the source code and performs whole-project analysis to iden-
lengths, enforce terminators, transfer ownership, and preserve                    tify translation targets, shared declarations, Rust interfaces,
stable Rust-facing APIs.                                                          and inter-function dependencies. The resulting dependency
   3) Compositional Adversarial Refinement: The selected                          graph is topologically sorted to determine the subsequent
composition S is refined via joint adversarial testing. The                       function translation order.
Challenger generates executable C-to-Rust challenges that                            2) Insight Retrieval: Before translating each function,
jointly activate all insights in S and force oracle dependence                    T RAIL retrieves context-relevant insights from the insight bank
on their interaction; sanity checks reject cases where insights                   using the target C function, Rust interface, macro-expanded
are exercised independently. Valid challenges combine mul-                        surrounding context, available Rust artifacts, and prior trans-
tiple interacting C-to-Rust concerns, requiring a unified Rust                    lation or repair feedback as the query.
solution satisfying all insights.                                                    Retrieval proceeds in two steps. Candidate insights are first
   The Translator attempts the challenge with full activation                     selected by matching their Trigger and tags against the
of S, and execution produces compiler and test evidence                           query, and then re-ranked by contextual relevance, compatibil-
as in the single-insight setting. Success indicates safe co-                      ity, and conflict risk estimated from compositional adversarial
activation in shared contexts. Failures are attributed by the                     learning. The top-N compatible insights are retained, while
Refiner to conflicting constraints, missing coordination condi-                   high-conflict combinations are filtered out.
tions, incomplete precedence relations, or interaction-specific                      3) Knowledge-Guided Translation: For each function,
corner cases. The evidence gate admits only verdict-supported                     T RAIL combines dependency-aware project context with re-
updates, including field refinements, relation updates, co-                       trieved insights. The context includes the target Rust interface,
activation preconditions, or precedence rules. For instance,                      aligned macro-expanded C code, relevant declarations and
ownership transfer may override borrowed-view assumptions                         constants, validated Rust artifacts from previously translated
when the C caller releases the buffer, while slice construc-                      functions, and essential dependency information, while unre-
tion excludes a terminator preserved internally. If a failure                     lated files are omitted or abstracted to meet prompt constraints.
   Conditioned on this context, the Translator generates Rust          1) CRUST-Bench: CRUST-Bench [4] contains 100 real-
code that conforms to the target interface and preserves the        world C projects collected from GitHub, Linux, and Post-
observable behavior of the original C function. Retrieved           greSQL, covering domains such as data structures, cryptog-
insights provide structured guidance on semantic constraints,       raphy, encoding, parsing, and system utilities. Each project is
translation patterns, and potential risks.                          paired with an idiomatic Rust interface crate and executable
   4) Execution-Guided Repair: After translation, cargo             tests. We use CRUST-Bench as the primary benchmark for
check is used for validation. If it succeeds, the implemen-         effectiveness, ablation, and sensitivity studies.
tation is accepted and the pipeline proceeds; otherwise, the           2) SmartC2Rust-Bench: To evaluate cross-benchmark
Repairer is invoked. It performs localized fixes using compiler     generalization, we use the benchmark introduced by
diagnostics, the target Rust interface, relevant C context,         SmartC2Rust [11]. Of its 21 programs, 20 are publicly
previous Rust attempts, and retrieved insights. This repair loop    available and used in our experiments. These subjects
repeats until compilation succeeds or the budget is exhausted.      comprise small-to-medium command-line utilities and
   Once all functions compile, the integrated project is val-       library-style programs with build scripts, test scripts, and
idated using cargo test. If tests pass, the translation is          entry-point specifications. Unlike CRUST-Bench, which
accepted; otherwise, the Repairer localizes failures using test     relies on Rust interface crates, SmartC2Rust-Bench evaluates
outputs, panic traces, assertions, dependency context, and          translations through executable behavioral checks.
recently translated components, and performs further targeted       B. Models
repairs under the same constraints.
                                                                       We evaluate T RAIL with three representative LLM back-
   5) Trace Reflection for Insight Mining: T RAIL performs
                                                                    ends: GPT-5.4-mini, a compact model with strong code-
reflection over all execution traces. The Reflector first filters
                                                                    generation capabilities; Kimi-K2.5, a large-scale model with
out traces that are project-specific, non-recurring, or low-
                                                                    an extended context window; and DeepSeek-V4-Flash, a
signal traces. For the remaining traces, it analyzes C context,
                                                                    fast inference model optimized for coding tasks. All mod-
compiler diagnostics, test failures, generated candidates, and
                                                                    els are accessed through OpenAI-compatible APIs. Un-
final outcomes to extract underlying conditions, objectives,
                                                                    less otherwise specified, we use temperature = 1.0 and
constraints, or risks, which are summarized as candidate
                                                                    max_output_tokens = 128000 for all experiments.
insights in the form ⟨Trigger , Goal , Constraint, Risk ⟩.
   These candidates are then screened to remove duplicates,         C. Baselines
triggerless patterns, contradictions with existing insights, or        We compare T RAIL against five representative baselines
artifacts tied to project-specific structure. The remaining can-    spanning rule-based, hybrid, and LLM-based C-to-Rust trans-
didates are forwarded for adversarial learning before entering      lation systems. All baselines are evaluated using their default
the insight bank, completing the translation–learning loop.         configurations.
                                                                       • C2Rust [1] is a rule-based source-to-source translator
                 III. E XPERIMENTAL S ETUP                                that mechanically converts C code into Rust. It serves
                                                                          as a non-LLM baseline for transpilation-based migration.
   We conduct experiments to evaluate the effectiveness of             • C2SaferRust [20] is a hybrid approach that first trans-
T RAIL, aiming to answer the following research questions:                lates C into unsafe Rust using C2Rust and then employs
  • RQ1 (Overall Effectiveness): How does T RAIL perform                  an LLM to incrementally rewrite unsafe code into safer
    compared with state-of-the-art baselines on project-level             Rust while preserving behavior through test-based verifi-
    C-to-Rust translation?                                                cation.
  • RQ2 (Ablation of Key Components): What is the con-                 • Direct Prompting uses the backend LLM to translate

    tribution of insight mining and the two-level adversarial             each callable without learned insights or iterative repair,
    learning mechanism to translation performance?                        representing the model’s zero-experience translation ca-
  • RQ3 (Generalization of Learned Insights): How well                    pability.
    do insights learned from one set of C-to-Rust projects             • Self-Repair [4] augments direct translation with iterative

    transfer to unseen project collections in improving trans-            compilation-driven repair (up to five rounds) but does not
    lation performance?                                                   leverage learned insights, isolating the effect of repair-
  • RQ4 (Sensitivity Analysis): How do key hyperparame-                   based feedback.
    ters, including insight selection size and the number of           • SmartC2Rust [11] is an LLM-based translation frame-

    adversarial learning rounds, affect the performance and               work that performs translation and repair using compila-
    stability of T RAIL?                                                  tion and test feedback, but does not incorporate structured
                                                                          translation insights.
A. Datasets                                                            No public C-to-Rust baseline provides a reproducible
                                                                    structured-insight pipeline for comparison. Therefore, in RQ2
  We evaluate T RAIL on two C-to-Rust translation bench-            we include a variant with directly mined insights via trace
marks.                                                              reflection, serving as a non-adversarial baseline.
                                                              TABLE II
                              OVERALL C OMPARISON OF T RAIL AND BASELINES ON 100 CRUST-B ENCH P ROJECTS

                                                                                                           Idiomaticity
             Model                Method                CompRate       TestRate     SafeRate
                                                                                                  Lint Pass ↑   Idiom Penalty ↓
             Rule-based and hybrid baselines
             —                  C2Rust                     98%            98%         0.13%           98              49.06
             gpt-5.4-mini       C2SaferRust                98%            98%        12.28%           94              49.20
             LLM-based methods
                                  Direct Prompting         32%           24%         99.66%           34              11.98
                                  Self-Repair              56%           55%         99.67%           65               8.70
             gpt-5.4-mini
                                  SmartC2Rust              66%           40%         99.41%           67              4.77
                                  T RAIL (ours)            88%           69%         96.63%           88               3.95
                                  Direct Prompting         39%           25%         98.95%           41              13.27
                                  Self-Repair              76%           61%         99.03%           84               8.48
             kimi-k2.5
                                  SmartC2Rust              59%           37%         97.16%           60              5.21
                                  T RAIL (ours)            79%           67%         95.12%           89               4.47
                                  Direct Prompting         21%           14%         98.81%           25              11.89
                                  Self-Repair              56%           48%         99.08%           67               9.23
             deepseek-v4-flash
                                  SmartC2Rust              31%           26%         98.49%           15              7.22
                                  T RAIL (ours)            74%           54%         97.57%           88               4.22
             ∗ For LLM-based methods, results are grouped by backbone model, with best in bold.




D. Metrics                                                                λ2 = 1 and use a conflict threshold τc = 0.7. Candi-
   We assess translation quality from four perspectives: compi-           date insights are grouped by related triggers and overlapping
lation success, behavioral correctness, safety, and idiomaticity.         tags, and compositions are constructed greedily by iteratively
                                                                          adding the largest positive marginal gain until reaching B = 3,
   1) CompRate: The percentage of projects that successfully
                                                                          exhausting positive-gain candidates, or encountering only un-
pass cargo check, indicating successful project-level com-
                                                                          resolved conflicts.
pilation.
                                                                             Unless otherwise specified, each accepted insight under-
   2) TestRate: The percentage of projects that pass all cargo
                                                                          goes at most K = 5 adversarial refinement rounds. During
test cases, indicating preservation of observable program
                                                                          execution-guided repair, compilation-level fixes are limited
behavior.
                                                                          to five attempts per callable (following Self-Repair), and
   3) SafeRate: The percentage of translated callables that
                                                                          project-level test repair is capped at three attempts. A repair
contain no unsafe blocks, measuring the extent to which
                                                                          is accepted only if it succeeds or reduces the number of
translations leverage Rust’s safety guarantees.
                                                                          diagnostics or failing tests.
   4) Idiomaticity: Measured using two metrics. Lint Pass
counts the number of projects that pass cargo clippy, re-                                            IV. R ESULTS
flecting adherence to Rust coding conventions. Idiom Penalty
follows the non-idiomatic pattern penalty defined by Rus-                 A. RQ1: Overall Effectiveness
tine [21]. Higher Lint Pass and lower Idiom Penalty indicate                 We evaluate T RAIL against rule-based, LLM-based, and
more idiomatic Rust code.                                                 hybrid baselines on 100 CRUST-Bench projects. Table II
                                                                          summarizes the results.
E. Implementation Details
                                                                             Across all three backbone models, T RAIL achieves the
   The insight bank is stored as structured JSON records and              strongest LLM-based project-level correctness. With gpt-5.4-
indexed using FAISS. Each insight’s Trigger and tags are                  mini, it reaches 88% CompRate and 69% TestRate, surpassing
encoded with BAAI/bge-base-en-v1.5 for similarity-                        SmartC2Rust’s 66% CompRate and Self-Repair’s 55% Tes-
based retrieval, with a default retrieval budget of N = 5                 tRate by 22 and 14 percentage points, respectively. Similar
insights.                                                                 gains appear on kimi-k2.5 (79%/67% vs. 76%/61%) and
   All agents are implemented as structured LLM calls with                deepseek-v4-flash (74%/54% vs. 56%/48%), showing that the
fixed schemas, prompts, output formats, and acceptance crite-             effect is consistent across backbones.
ria, ensuring consistency across the full T RAIL pipeline and                The improvements over SmartC2Rust and Self-Repair sug-
all ablation variants. All prompts are released in our artifact           gest that proactive knowledge injection complements iterative
repository to support reproducibility.                                    repair. T RAIL mines and refines reusable insights from traces,
   For compositional adversarial learning, the backend LLM                helping prevent recurring failures rather than only fixing them
estimates support and conflict scores in Eq. 2. We set λ1 =               after they appear.
                                                               TABLE III
     A BLATION S TUDY OF THE P ROPOSED I NSIGHT L EARNING M ECHANISM , WITH C UMULATIVE R EMOVAL OF E ACH C OMPONENT FROM T RAIL

                                                                                                                  Idiomaticity
Model               Variant                                              CompRate TestRate SafeRate
                                                                                                         Lint Pass ↑ Idiom Penalty ↓
                    T RAIL                                                  88%        69%     96.63%        88             3.95
                        w/o Compositional Insight Adversarial Learning      86%        66%     96.22%        89             4.00
gpt-5.4-mini
                        w/o Single Insight Adversarial Learning             85%        63%     96.60%        91             4.07
                        w/o Insight Mining                                  75%        56%     93.87%        87             4.16
                    T RAIL                                                  79%        67%     95.12%        89             4.47
                        w/o Compositional Insight Adversarial Learning      76%        63%     94.76%        86             4.37
kimi-k2.5
                        w/o Single Insight Adversarial Learning             69%        54%     94.95%        89             4.28
                        w/o Insight Mining                                  70%        49%     94.98%        87             4.31
                  T RAIL                                                    74%        54%     97.57%        88             4.22
                      w/o Compositional Insight Adversarial Learning        75%        51%     97.74%        90             4.26
deepseek-v4-flash
                      w/o Single Insight Adversarial Learning               70%        49%     97.73%        87             4.22
                      w/o Insight Mining                                    68%        45%     96.85%        88             4.10
∗ Best results per model are in bold.




   Rule-based and hybrid baselines show a different trade-off.          Removing insight mining yields the largest drop, with
C2Rust and C2SaferRust reach up to 98% CompRate and                  TestRate falling to 56%, 49%, and 45% on gpt-5.4-mini, kimi-
TestRate, but rely on unsafe-first transpilation and therefore       k2.5, and deepseek-v4-flash. This suggests that even unrefined
suffer extremely low safety and poor idiomaticity. Thus,             trace-reflected insights provide useful semantic constraints
compile/test success alone does not characterize translation         beyond a standard translation-and-repair pipeline.
quality. Although T RAIL does not yet match their raw pass              Across variants, SafeRate remains stable (96.63%, 95.12%,
rates, it narrows the gap while avoiding their severe safety         97.57%), and idiomaticity changes marginally, indicating func-
and idiomaticity degradation.                                        tional gains do not compromise safety or code quality.

 Answer to RQ1. T RAIL achieves the best overall effec-                  Answer to RQ2. Failure-driven mined insights already pro-
 tiveness among LLM-based approaches across all three                    vide measurable benefits, while adversarial learning at both
 backend models, while preserving a better balance across                the single-insight and compositional levels further improves
 functional correctness, safety, and idiomaticity than the               the reliability of reusable constraints, mainly by boosting
 unsafe transpilation-first baselines.                                   TestRate without sacrificing SafeRate or idiomaticity.

B. RQ2: Ablation of Key Components
                                                                     C. RQ3: Generalization of Learned Insights
   To quantify each component’s contribution, we conduct a
stepwise ablation study on CRUST-Bench. Starting from the               To evaluate cross-benchmark generalization, we transfer the
full T RAIL framework, we progressively remove composi-              CRUST-Bench insight bank to SmartC2Rust-Bench. Table IV
tional insight adversarial learning, single-insight adversarial      compares Base without insight injection, Direct with target-
learning, and insight mining. Table III summarizes the results.      benchmark insights, and Transferred with CRUST-Bench in-
   All components are beneficial, with performance degrading         sights and no further adaptation.
under each removal. Removing compositional insight adver-               Transferred improves over Base across models. For gpt-5.4-
sarial learning reduces behavioral correctness across back-          mini, CompRate/TestRate rises from 80%/55% to 85%/70%;
bones, highlighting its role in coordinating related insights.       for kimi-k2.5, CompRate stays at 90% while TestRate im-
In the full system, it boosts TestRate to 69%, 67%, and 54%          proves from 65% to 70%; for deepseek-v4-flash, CompRate
on gpt-5.4-mini, kimi-k2.5, and deepseek-v4-flash while keep-        rises from 75% to 80% while TestRate remains 70%. These
ing CompRate stable. Without it, cross-insight inconsistency         gains indicate that the learned insights capture reusable C-to-
leads to TestRate drops and minor CompRate trade-offs (e.g.,         Rust constraints beyond the source benchmark.
75%→74% on deepseek-v4-flash).                                          However, Transferred remains below Direct, which learns
   Further removing single-insight adversarial learning causes       on SmartC2Rust-Bench itself. Compared with Transferred,
larger degradation: on kimi-k2.5, TestRate/CompRate de-              Direct improves CompRate by 5 points for all models and
crease from 63%/76% to 54%/69%; on deepseek-v4-flash,                boosts TestRate by 5, 10, and 10 points on gpt-5.4-mini,
from 51%/75% to 49%/70%; gpt-5.4-mini shows a smaller                kimi-k2.5, and deepseek-v4-flash. Thus, transferred insights
but consistent decline (66%/86%→63%/85%), indicating that            provide strong priors, but adversarial refinement is still needed
counterexample-driven refinement improves per-insight preci-         for benchmark-specific APIs, failure modes, and boundary
sion and robustness.                                                 conditions.
                            TABLE IV
  C ROSS - BENCHMARK G ENERALIZATION OF A DVERSARIALLY R EFINED
                            I NSIGHTS

                                                                 Idiomaticity
Model          Setting       CompRate TestRate SafeRate
                                                          Lint Pass ↑ Idiom Penalty ↓
               Base            80%      55%     98.57%      13/20          5.17
gpt-5.4-mini   Direct          90%      75%     98.44%      16/20          4.72
               Transferred     85%      70%     98.62%      13/20          5.28
               Base            90%      65%     97.62%      14/20          19.13
kimi-k2.5      Direct          95%      80%     97.71%      16/20          17.40        (a) Effect of insight selection size (N ). (b) Effect of adversarial rounds (K).
               Transferred     90%      70%     97.55%      15/20          18.86
                                                                                        Fig. 3. Hyperparameter sensitivity analysis of T RAIL on CRUST-Bench with
                  Base        75% 70%   98.63%    16/20        2.99
                                                                                        GPT-5.4-mini.
deepseek-v4-flash Direct      85% 80%   98.68%    17/20        2.84
                  Transferred 80% 70%   98.59%    17/20        3.08
 ∗ Insights are learned on CRUST-Bench and transferred to SmartC2Rust-
Bench. Base uses no insights, Direct uses target-benchmark insights, and                E. Qualitative Insight Evolution
Transferred uses CRUST-Bench insights.
                                                                                           We inspect two representative learning traces to understand
                                                                                        what the adversarially refined insights actually encode.
   Safety and idiomaticity remain stable under transfer: SafeR-                            1) Single-Insight Adversarial Learning: In libvcd, the
ate changes marginally, Lint Pass is unchanged or slightly                              initial pointer-buffer insight preserves buffer length and NUL
higher, and Idiom Penalty varies only modestly. Overall,                                termination but misses the boundary between internal storage
Transferred improves functional correctness without degrading                           and Rust-visible string semantics. The C code stores signals
code quality, while Direct achieves the best balance.                                   in fixed char[N] arrays with NUL-terminated content, while
                                                                                        Rust conversions such as String::from_utf8_lossy
  Answer to RQ3. Transferred insights consistently match or                             may expose zero-padded regions. The challenge reveals that
  improve the base pipeline in compilation and testing, with                            copying the full buffer is insufficient when downstream oper-
  broadly stable safety and idiomaticity, while the full T RAIL                         ations interpret it as a C string.
  pipeline remains strongest due to benchmark-specific adver-                              The refined insight fixed-c-string-visible-length
  sarial refinement.                                                                    strengthens the rule into a visibility-aware condition: fixed
                                                                                        C arrays may retain zero-padded storage internally, but any
D. RQ4: Sensitivity Analysis                                                            Rust-visible representation, comparison, or lookup must stop
   We study two key hyperparameters of T RAIL on CRUST-                                 at the first NUL unless the original program treats the buffer
Bench with gpt-5.4-mini: the insight retrieval size (N ) and                            as raw bytes. The insight thus evolves from a structural
the maximum number of adversarial refinement rounds (K).                                constraint into an observation-boundary rule.
To isolate their effects, we vary one parameter while fixing                               2) Compositional Insight Adversarial Learning: In
the other (K=5 for sweeping N , and N =5 for sweeping K).                               lib2bit, the twobitSequence pipeline involves
   Figure 3a shows that performance benefits from a moderate                            multiple cooperating insights: one preserves helper-call
retrieval budget. With N =1, T RAIL reaches 78% CompRate                                structure, and another enforces allocation size, decoding
and 56% TestRate, indicating insufficient coverage of interact-                         length, and NUL termination. Alone, they remain incomplete
ing C idioms. Increasing N to 3 improves results to 84%/65%,                            because one lacks the Rust-visible sequence length and the
and the default N =5 performs best (88%/69%). Larger bud-                               other does not specify when masking applies.
gets reduce TestRate (68% at N =7, 66% at N =10) without                                   The compositional challenge exposes this interaction gap
CompRate gains, suggesting interference from irrelevant or                              and aligns the insights into one policy: the Rust-visible length
weakly relevant constraints.                                                            is end - start, the C buffer allocates one extra byte for
   Figure 3b shows saturation in adversarial refinement. With-                          the terminator, masking applies only to valid decoded bases,
out refinement (K=0), performance is 85% CompRate and                                   and the terminator is excluded from the logical sequence. The
63% TestRate. One and two rounds improve results to                                     insights thus become a coordinated constraint set for the same
86%/66% and 87%/68%, while K≥3 already matches the best                                 abstraction.
observed performance (88%/69%). Larger K mainly stabilizes
the outcome.                                                                                                         V. D ISCUSSION

  Answer to RQ4. T RAIL performs best under moderate                                    A. Cost Analysis
  retrieval and bounded adversarial learning: N =5 achieves                                We analyze T RAIL’s cost in token usage and end-to-end run-
  the strongest CompRate and TestRate, while most gains                                 time. On CRUST-Bench with gpt-5.4-mini, the full configura-
  are realized within two to three refinement rounds, and                               tion consumes 21.43M tokens (214.3K per project), compared
  K=5 serves as a conservative upper bound with stable                                  with 19.51M tokens (195.1K per project) for the no-insight
  performance.                                                                          setting. The 1.92M-token increase, or 9.8% overhead, remains
                                                                                        modest because most tokens are still spent on translation,
compiler feedback, and test-driven repair, while the compact        ownership [7], aliasing [6], pointer safety [5], [23], API mi-
insight bank is injected selectively.                               gration [8], [24]–[29], and type migration [30], [31]. However,
   For runtime, T RAIL takes 15,326 seconds in total (153.3         these approaches rely on handcrafted analyses or transforma-
seconds per project), compared with 10,452 seconds (104.5           tion rules, limiting their generality.
seconds per project) for SmartC2Rust, a 1.47× slowdown                 LLM-based methods generate idiomatic Rust code without
mainly due to trace reflection and the adversarial challenge–       manually defined translation rules. Existing work improves
translate–refine loop.                                              translation via semantic guidance [32]–[34], retrieval [9],
   These results indicate moderate token and runtime overhead,      [35]–[37], execution-driven repair [11], [16], [38]–[41], and
amortized as refined insights guide later translation and repair.   project-level context [42]–[44]. Despite these advances, en-
T RAIL is therefore most suitable for project-level migration       suring reliable translation correctness remains challenging due
where slightly higher latency is acceptable for improved            to the substantial semantic and paradigm gap between C
correctness, safety, and idiomaticity, while latency-sensitive      and Rust. A line of work leverages LLMs to enhance rule-
settings may rely on seeded insight banks with limited online       based transpilers or static analysis, for example by refining
refinement.                                                         transpiler outputs [20], injecting semantic guidance [45], [46],
                                                                    or performing skeleton-guided repair [10].
B. Threats to Validity                                                 Empirical studies [47]–[50] and benchmarks [3], [4] further
   Internal Validity. T RAIL validates translations using           highlight persistent trade-offs among correctness, safety, and
cargo check and cargo test. While these provide ob-                 idiomaticity in C-to-Rust migration.
jective correctness signals, they do not establish full semantic       T RAIL belongs to the LLM-based category. Unlike prior
equivalence with the original C implementation. Future work         approaches that rely on manual rules, retrieval, or repair-driven
will complement them with fuzzing, differential testing, and        generation, T RAIL models reusable translation knowledge as
stronger API specifications.                                        executable insights and refines them through adversarial learn-
   Beyond execution-based validation, compositional insight         ing, improving the reliability of knowledge-guided project-
learning depends on LLM-estimated support and conflict              level translation while achieving a better balance among
scores in Eq. 2, which may vary across backend models or            correctness, safety, and idiomaticity.
decoding settings. We reduce this risk by using fixed schemas       B. Experience-Enhanced AI Agents
and prompts and by treating the scores only as a heuristic for          Experience enhancement equips LLM agents with reusable
prioritizing insight compositions before executable validation;     knowledge accumulated across prior tasks, enabling transfer
actual insight and relation updates are accepted only when          beyond the current context. A line of work learns such expe-
supported by compiler or test evidence.                             rience from agent trajectories. For example, Reflexion [12]
   Another threat is potential benchmark contamination during       transforms execution feedback into verbal reflections; Ex-
LLM pre-training. This risk is reduced because the bench-           peL [13] distills successful and failed trajectories into reusable
marks contain no Rust reference implementations, preventing         lessons; AutoGuide [51] synthesizes context-aware guidelines;
direct memorization of target translations. However, models         and Agent Workflow Memory [14] extracts reusable workflows
may still have seen the original C projects. Evaluating on          from past executions.
private or newly released projects would further mitigate this          This paradigm has also been adopted in software engi-
threat.                                                             neering. AgentRR abstracts interaction traces into structured
   External Validity. Our evaluation is limited to public           experiences for reuse across similar tasks [52]. Agent KB
user-level C projects. CRUST-Bench and SmartC2Rust-Bench            aggregates heterogeneous trajectories into a knowledge base
cover diverse application domains, supporting generalization        for cross-task retrieval [53], while SWE-Exp distills prior
across a broad range of C-to-Rust translation tasks. However,       issue-resolution traces into actionable repair experience [15].
they do not represent all migration scenarios, such as kernel or    These systems improve reuse by storing and retrieving past
device-driver code, highly concurrent systems, projects with        trajectories or repair patterns [54], often augmented with
complex native dependencies, or large industrial codebases.         lightweight controls such as verification [55], disagreement
Extending the evaluation to these settings remains future work.     filtering, or retrieval-based selection.
                                                                        However, such experience is typically derived from stochas-
                    VI. R ELATED W ORK                              tic agent executions, which may encode spurious decisions,
A. C-to-Rust Translation                                            omit boundary conditions, or introduce inconsistencies across
                                                                    tasks, limiting reliability under distribution shifts. To address
   Existing C-to-Rust translation work can be broadly grouped
                                                                    this limitation, T RAIL treats translation experience as a hy-
into rule-based and LLM-based approaches.
                                                                    pothesis to be validated: it is adversarially challenged, refined,
   Rule-based methods mechanically translate C into Rust [1],       and compositionally verified before reuse.
[2], [22] while largely preserving the original program struc-
ture, often producing code that relies heavily on raw pointers                         VII. C ONCLUSION
and unsafe constructs. Subsequent work improves safety                This paper presents T RAIL, an adversarial agentic frame-
and idiomaticity through analyses and transformations for           work for C-to-Rust translation that continuously refines
reusable translation insights through Translator–Challenger                       [17] W. Zeng, Y. Wang, C. Hu, Y. Shi, C. Wan, H. Zhang, and X. Gu, “Prun-
interaction and evidence-based updates. By strengthening in-                           ing the unsurprising: Efficient llm reasoning via first-token surprisal,”
                                                                                       arXiv preprint arXiv:2508.05988, 2025.
sights at both individual and compositional levels, T RAIL                        [18] W. Zeng, X. Zhang, Y. Shi, C. Hu, Y. Chen, B. Shen, and X. Gu,
improves their robustness and coordination across diverse                              “Glimprouter: Efficient collaborative inference by glimpsing one token
translation scenarios. Experiments on two project-level bench-                         of thoughts,” in Findings of the Association for Computational
                                                                                       Linguistics, ACL 2026, San Diego, California, United States, July 2-7,
marks show that T RAIL consistently outperforms existing                               2026, M. Liakata, V. P. Moreira, J. Zhang, and D. Jurgens, Eds.
LLM-based approaches and learns insights that generalize                               Association for Computational Linguistics, 2026, pp. 17 850–17 864.
beyond their source programs, while maintaining stable safety                          [Online]. Available: https://doi.org/10.18653/v1/2026.findings-acl.885
                                                                                  [19] X. Zhang, W. Zeng, X. Gu, C. Hu, H. Lin, Y. Shi, M. Wang, and B. Shen,
and idiomaticity.                                                                      “Paratempo: Efficient parallel reasoning via temporal confidence,” arXiv
                                                                                       preprint arXiv:2608.16425, 2026.
                      DATA AVAILABILITY                                           [20] V. Nitin, R. Krishna, L. L. do Valle, and B. Ray, “C2 saferrust:
  To support reproducibility, all related scripts and data are                         Transforming c projects into safer rust with neurosymbolic techniques,”
                                                                                       IEEE Transactions on Software Engineering, 2025.
available at https://github.com/bbzswcf/TRAIL.                                    [21] S. Dehghan, T. Sun, T. Wu, Z. Li, and R. Jabbarvand, “Translating large-
                              R EFERENCES                                              scale c repositories to idiomatic rust,” arXiv preprint arXiv:2511.20617,
                                                                                       2025.
 [1] “C2Rust: Migrate C code to Rust,” https://github.com/immunant/c2rust,        [22] X. Han, B. Hua, Y. Wang, and Z. Zhang, “Rusty: Effective c to rust
     2025.                                                                             conversion via unstructured control specialization,” in 2022 IEEE 22nd
 [2] N. Shetty, N. Saldanha, and M. Thippeswamy, “Crust: Ac/c++ to rust                International Conference on Software Quality, Reliability, and Security
     transpiler using a “nano-parser methodology” to avoid c/c++ safety                Companion (QRS-C). IEEE, 2022, pp. 760–761.
     issues in legacy code,” in Emerging Research in Computing, Information,      [23] M. Ling, Y. Yu, H. Wu, Y. Wang, J. R. Cordy, and A. E. Hassan, “In
     Communication and Applications: ERCICA 2018, Volume 1. Springer,                  rust we trust: a transpiler from unsafe c to safer rust,” in Proceedings of
     2019, pp. 241–250.                                                                the ACM/IEEE 44th international conference on software engineering:
 [3] G. Ou, M. Liu, Y. Chen, Y. Wang, X. Peng, and Z. Zheng, “Rustre-                  companion proceedings, 2022, pp. 354–355.
     potrans: Repository-level context code translation benchmark targeting       [24] J. Hong and S. Ryu, “Concrat: An automatic C-to-Rust lock API trans-
     rust,” in 2025 40th IEEE/ACM International Conference on Automated                lator for concurrent programs,” in 2023 IEEE/ACM 45th International
     Software Engineering (ASE). IEEE, 2025, pp. 610–622.                              Conference on Software Engineering (ICSE). IEEE, 2023, pp. 716–728.
 [4] A. Khatry, R. Zhang, J. Pan, Z. Wang, Q. Chen, G. Durrett, and               [25] ——, “To tag, or not to tag: Translating C’s unions to Rust’s tagged
     I. Dillig, “CRUST-bench: A comprehensive benchmark for c-to-safe-                 unions,” in Proceedings of the 39th IEEE/ACM International Conference
     rust transpilation,” in Second Conference on Language Modeling, 2025.             on Automated Software Engineering, 2024, pp. 40–52.
     [Online]. Available: https://openreview.net/forum?id=8xofWL61S9              [26] ——, “Forcrat: Automatic I/O API translation from C to Rust via
 [5] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating c to              origin and capability analysis,” in 2025 40th IEEE/ACM International
     safer rust,” Proceedings of the ACM on Programming Languages, vol. 5,             Conference on Automated Software Engineering (ASE). IEEE, 2025,
     no. OOPSLA, pp. 1–29, 2021.                                                       pp. 1541–1552.
 [6] M. Emre, P. Boyland, A. Parekh, R. Schroeder, K. Dewey, and B. Hard-         [27] X. Wu and B. Demsky, “GenC2Rust: Towards generating generic Rust
     ekopf, “Aliasing limits on translating c to safe rust,” Proceedings of the        code from C,” in 2025 IEEE/ACM 47th International Conference on
     ACM on Programming Languages, vol. 7, no. OOPSLA1, pp. 551–579,                   Software Engineering (ICSE). IEEE, 2025, pp. 90–102.
     2023.                                                                        [28] V. Chen, A. Coughlin, and M. D. Bond, “&inator: Correct, precise c-
 [7] H. Zhang, C. David, Y. Yu, and M. Wang, “Ownership guided C                       to-rust interface translation,” Proceedings of the ACM on Programming
     to Rust translation,” in International Conference on Computer Aided               Languages, vol. 10, no. PLDI, pp. 580–603, 2026.
     Verification. Springer, 2023, pp. 459–482.                                   [29] H. Peng, B. Kasikci, G. L. Bernstein, and M. D. Ernst, “Hayroll: A
 [8] J. Hong and S. Ryu, “Don’t write, but return: Replacing output param-             modular wrapper for translating c macros and conditional compilation
     eters with algebraic data types in c-to-rust translation,” Proceedings of         to rust,” Proceedings of the ACM on Programming Languages, vol. 10,
     the ACM on Programming Languages, vol. 8, no. PLDI, pp. 716–740,                  no. PLDI, pp. 730–753, 2026.
     2024.                                                                        [30] J. Hong and S. Ryu, “Type-migrating c-to-rust translation using a large
 [9] X. Cai, J. Liu, X. Huang, Y. Yu, H. Wu, C. Li, B. Wang, I. N. B. Yusuf,           language model,” Empirical Software Engineering, vol. 30, no. 1, p. 3,
     and L. Jiang, “Rustmap: Towards project-scale c-to-rust migration via             2025.
     program analysis and llm,” in International Conference on Engineering        [31] Q. Xu and J. Huang, “Optimizing type migration for llm-based c-to-
     of Complex Computer Systems, 2025, pp. 283–302.                                   rust translation: A data flow graph approach,” in Proceedings of the
[10] C. Wang, T. Yu, B. Shen, J. Wang, D. Chen, W. Zhang, Y. Shi, C. Xie,              14th ACM SIGPLAN International Workshop on the State Of the Art in
     and X. Gu, “EvoC2Rust: A skeleton-guided framework for project-level              Program Analysis, 2025, pp. 8–14.
     C-to-Rust translation,” in IEEE/ACM International Conference on              [32] F. Luo, K. Ji, C. Gao, S. Gao, J. Feng, K. Liu, X. Xia, and M. R.
     Software Engineering: Software Engineering in Practice (ICSE-SEIP),               Lyu, “Integrating rules and semantics for llm-based c-to-rust translation,”
     2026. [Online]. Available: https://arxiv.org/abs/2508.04295                       in 2025 IEEE International Conference on Software Maintenance and
[11] M. Shiraishi, Y. Cao, and T. Shinagawa, “SmartC2Rust: Iterative,                  Evolution (ICSME). IEEE, 2025, pp. 685–696.
     feedback-driven C-to-Rust translation via large language models for          [33] M. Farrukh, B. Coskun, T. Palit, and M. Polychronakis, “Safetrans: Llm-
     safety and equivalence,” in Proceedings of the ACM/IEEE 48th                      assisted transpilation from c to rust,” in Proceedings of the 1st Workshop
     International Conference on Software Engineering, 2026. [Online].                 on Code Translation, Transformation, and Modernization, 2026, pp. 30–
     Available: https://arxiv.org/abs/2409.10506                                       37.
[12] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Re-           [34] A. Z. Yang, Y. Takashima, B. Paulsen, J. Dodds, and D. Kroening, “Vert:
     flexion: Language agents with verbal reinforcement learning,” Advances            Polyglot verified equivalent rust transpilation with large language mod-
     in neural information processing systems, vol. 36, pp. 8634–8652, 2023.           els,” in 2025 40th IEEE/ACM International Conference on Automated
[13] A. Zhao, D. Huang, Q. Xu, M. Lin, Y.-J. Liu, and G. Huang, “Expel: Llm            Software Engineering (ASE). IEEE, 2025, pp. 1453–1463.
     agents are experiential learners,” in Proceedings of the AAAI Conference     [35] H. F. Eniser, H. Zhang, C. David, M. Wang, M. Christakis, B. Paulsen,
     on Artificial Intelligence, vol. 38, no. 17, 2024, pp. 19 632–19 642.             J. Dodds, and D. Kroening, “Towards translating real-world code with
[14] Z. Z. Wang, J. Mao, D. Fried, and G. Neubig, “Agent workflow memory,”             llms: A study of translating to rust,” arXiv preprint arXiv:2405.11514,
     arXiv preprint arXiv:2409.07429, 2024.                                            2024.
[15] S. Chen, S. Lin, Y. Shi, H. Lian, X. Gu, L. Yun, D. Chen, L. Cao, J. Liu,    [36] Z. Yuan, W. Mao, Z. Chen, X. Shang, C. Wang, Y. Lou, and X. Peng,
     N. Xia et al., “Swe-exp: Experience-driven software issue resolution,”            “Project-level c-to-rust translation via pointer knowledge graphs,” 2026.
     arXiv preprint arXiv:2507.23361, 2025.                                            [Online]. Available: https://arxiv.org/abs/2510.10956
[16] S. Wang, M. Liu, G. Ou, Y. Chen, Z. Li, Y. Wang, and Z. Zheng, “Build-
     aware incremental c-to-rust migration via skeleton-first translation and
     historical knowledge reuse,” arXiv preprint arXiv:2603.02617, 2026.
[37] J. Feng, W. Gan, C. Gao, C. Wang, F. Luo, X. Xia, G. Li, and                    translation with static analysis and ffi-based verification,” arXiv preprint
     K. Liu, “Dependency-guided repository-level c-to-rust translation with          arXiv:2503.12511, 2025.
     reinforcement alignment,” arXiv preprint arXiv:2604.02852, 2026.           [47] R. Li, B. Wang, T. Li, P. Saxena, and A. Kundu, “Translating c to rust:
[38] M. Shetty, N. Jain, A. Godbole, S. A. Seshia, and K. Sen, “Syzygy: Dual         Lessons from a user study,” arXiv preprint arXiv:2411.14174, 2024.
     code-test c to (safe) rust translation using llms and dynamic analysis,”   [48] A. Valenzuela, M. Gonzalez-Mallo, C. Gutierrez, D. Garcia-Gasulla,
     arXiv preprint arXiv:2412.14234, 2024.                                          G. Kestor, and S. Royuela, “From c to rust: Evaluating llm capabilities
[39] H. Zhou, Y. Luo, M. Zhang, and D. Xu, “C2rusttv: An llm-based frame-            in transpilation through compilation errors,” in International Conference
     work for c to rust translation and validation,” in 2025 IEEE 49th Annual        on High Performance Computing. Springer, 2025, pp. 311–324.
     Computers, Software, and Applications Conference (COMPSAC). IEEE,          [49] B. Tadesse, V. Nitin, M. Salah, B. Ray, M. d’Amorim, and W. Assunção,
     2025, pp. 1254–1259.                                                            “Code quality analysis of translations from c to rust,” arXiv preprint
[40] Y. Bai and T. Palit, “Rustassure: Differential symbolic testing for             arXiv:2602.00840, 2026.
     llm-transpiled c-to-rust code,” in 2025 40th IEEE/ACM International        [50] N. Rutherford and D. O’Keeffe, “An empirical study of c to rust trans-
     Conference on Automated Software Engineering (ASE). IEEE, 2025,                 lation using local large-language models,” in The Third International
     pp. 534–546.                                                                    Workshop on Large Language Models for Code, 2026.
[41] H. Sim, H. Cho, A. Shokri, Z. Fu, and B. Ravindran, “Encrust:              [51] Y. Fu, D.-K. Kim, J. Kim, S. Sohn, L. Logeswaran, K. Bae, and
     Encapsulated substitution and agentic refinement on a live scaffold for         H. Lee, “Autoguide: Automated generation and selection of context-
     safe c-to-rust translation,” arXiv preprint arXiv:2604.04527, 2026.             aware guidelines for large language model agents,” Advances in Neural
[42] M. Farrukh, B. Coskun, T. Palit, and M. Polychronakis, “Orbit: Guided           Information Processing Systems, vol. 37, pp. 119 919–119 948, 2024.
     agentic orchestration for autonomous c-to-rust transpilation,” 2026.       [52] E. Feng, W. Zhou, Z. Liu, L. Chen, Y. Dong, C. Zhang, Y. Zhao, D. Du,
     [Online]. Available: https://arxiv.org/abs/2604.12048                           Z. Hua, Y. Xia et al., “Get experience from practice: Llm agents with
[43] Y. Yan, Y. Feng, J. Liu, D. Liu, Z. Liu, H. Teng, and B. Xu, “C2rustxw:         record & replay,” arXiv preprint arXiv:2505.17716, 2025.
     Program-structure-aware c-to-rust translation via program analysis and     [53] X. Tang, T. Qin, T. Peng, Z. Zhou, D. Shao, T. Du, X. Wei, P. Xia,
     llm,” arXiv preprint arXiv:2603.28686, 2026.                                    F. Wu, H. Zhu et al., “Agent kb: Leveraging cross-domain experience
[44] C. Hu, W. Zeng, Y. Shi, B. Shen, and X. Gu, “In line with context:              for agentic problem solving,” arXiv preprint arXiv:2507.06229, 2025.
     Repository-level code generation via context inlining,” Proc. ACM          [54] S. Gao, W. Zeng, Z. Yu, J. Wangni, C. Wang, K. Cai, S. He,
     Softw. Eng., vol. 3, no. FSE, pp. 1469–1491, 2026. [Online]. Available:         and M. R. Lyu, “Swe-mem: Learning adaptive memory management
     https://doi.org/10.1145/3797094                                                 for long-horizon coding agents,” CoRR, vol. abs/2606.28434, 2026.
[45] Y. Gao, C. Wang, P. Huang, X. Liu, M. Zheng, and X. Zhang, “Raw                 [Online]. Available: https://doi.org/10.48550/arXiv.2606.28434
     pointer rewriting with llms for translating c to safer rust,” 2026.        [55] W. Zeng, Y. Shi, X. Gu, C. Hu, C. Wang, Y. Cui, H. Zhou, M. Qi,
     [Online]. Available: https://arxiv.org/abs/2505.04852                           J. Wangni, Z. Yu, S. Gao, K. Cai, and S. He, “Dockerless: Environment-
[46] T. Zhou, Z. Zhang, H. Lin, S. Jha, M. Christodorescu, K. Levchenko, and         free program verifier for coding agents,” CoRR, vol. abs/2606.28436,
     V. Chandrasekaran, “Sactor: Llm-driven correct and idiomatic c to rust          2026. [Online]. Available: https://doi.org/10.48550/arXiv.2606.28436
