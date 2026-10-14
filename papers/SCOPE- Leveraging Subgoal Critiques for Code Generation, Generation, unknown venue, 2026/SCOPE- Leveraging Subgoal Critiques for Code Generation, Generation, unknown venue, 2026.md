                                             SCOPE: Leveraging Subgoal Critiques for Code
                                                             Generation
                                                  Yueke Zhang∗ , Yifan Zhang∗ , Zihan Fang∗ , Kevin Leach∗ , Juan Zhai† , Wei Zhang‡ , Yu Huang∗
                                                                                                 ∗ Vanderbilt University

                                                                 {yueke.zhang, yifan.zhang.2, zihan.fang, kevin.leach, yu.huang}@vanderbilt.edu
                                                                                    † University of Massachusetts at Amherst

                                                                                               juanzhai@umass.edu
                                                                                                      ‡ IBM

                                                                                                weiz@us.ibm.com


                                           Abstract—Code generation with large language models (LLMs)          at exposing real defects [10], [11]. Thus, passing a limited
                                        remains unreliable because generated programs can appear cor-          test suite is useful evidence, but it is not the same as showing
                                        rect while still violating key semantic requirements in the natural-   that the generated code actually satisfies the intended behav-
                                        language specification. Existing feedback-based methods improve
                                        over coder-only generation, but they often rely on unstructured        ior [12].
                                        critique or execution signals that do not explicitly identify what
                                        the code is semantically missing. We present SCOPE, a prover-
arXiv:2607.05810v1 [cs.SE] 7 Jul 2026




                                        initialized subgoal critic for code generation. SCOPE adapts a
                                        Lean-oriented prover model to produce three parseable feedback
                                        fields for downstream code generation: subgoals, gap analysis,
                                        and a robustness checklist. Our approach combines supervised
                                        fine-tuning, process-aligned reinforcement learning (RL), and
                                        feedback-guided inference, with two complementary rewards
                                        during RL: a dense reward for structured critique quality and
                                        a sparse reward based on whether the critique improves the
                                        coder’s execution score.
                                           Experiments show that SCOPE improves over the compared
                                        feedback baselines. On LiveCodeBench V6, SCOPE achieves
                                        39.4% pass@1, compared with 36.6% for Reflexion and 20.6%
                                        for the coder-only baseline. On BigCodeBench (Hard), it reaches
                                        42.6%, surpassing Reflexion at 36.5% and coder-only generation
                                        at 34.5%. Further analysis shows that SCOPE’s gains are                Fig. 1. A natural-language task usually contains latent semantic requirements
                                        concentrated in tasks with concrete semantic constraints and that      that are difficult to recover from execution feedback alone. SCOPE fills this
                                        its localized code corrections than Reflexion’s.                       gap by asking a prover-initialized critic to expose those requirements as
                                           Index Terms—LLM for Coding, Code Generation                         explicit repair obligations before the coder revises the program.

                                                               I. I NTRODUCTION                                   A natural response to unreliable code generation is verifi-
                                           Large Language Models (LLMs) for coding are now main-               cation, but this is precisely where the difficulty deepens [13].
                                        stream [1], [2]. AI coding assistants have moved from early            Existing approaches based on contracts, symbolic reasoning,
                                        trials to routine practice across industry and open source:            and SMT solvers can verify well-specified properties, yet
                                        enterprises report broad adoption and measurable productivity          they rely on precise formal statements of behavior that are
                                        gains [3], [4]. Recent data highlights rapid growth in AI-             rarely available in open-ended natural-language programming
                                        assisted development, while field studies with large orga-             tasks [14], [15]. Recent work at the intersection of LLMs
                                        nizations document sustained usage and positive developer              and formal methods is encouraging: models can generate
                                        experience impacts [5].                                                and repair proofs in interactive theorem provers and pro-
                                           However, reliability remains the central obstacle for LLM-          duce verifier hints for formally checked programs [13], [16].
                                        based code generation [6]. Code LLMs often produce pro-                However, these successes largely assume that the task is
                                        grams that look plausible but violate the user’s actual intent:        already formalized, that the target language is verifier-native,
                                        they may hallucinate APIs, invent unsupported behaviors, or            or that rich proof state feedback is available during search.
                                        implement logic that passes superficial checks while failing on        When these assumptions are relaxed, end-to-end verified code
                                        edge cases [7], [8]. Testing helps, but it does not fully solve the    generation remains difficult even for the most advanced LLMs
                                        problem [9]. In realistic software settings, developers cannot         [16], [17]. Thus, the main bottleneck is not only discharging
                                        enumerate tests for every path, corner case, and semantic              formal obligations, but first deriving useful obligations from
                                        constraint, and recent studies show that LLM-generated tests           ambiguous natural-language intent. This leaves a gap between
                                        are themselves incomplete, sometimes invalid, and often weak           weak evidence from testing and the high cost of full manual
formalization.                                                             within 20 lines), and does so with more surgical repairs
   Recent progress in formal mathematics suggests a promising              (28.0 vs. 35.0 median changed lines).
direction for narrowing this gap [18], [19]. Proof assistants          The remainder of this paper is organized as follows. Sec-
such as Lean provide a reasoning environment in which in-           tion II introduces the background. Section III presents a mo-
termediate steps are explicit, modular, and machine-checkable       tivating example. Section IV reviews related work. Section V
under a small trusted kernel [20], [20]. Moreover, the Lean         describes the SCOPE methodology. Section VI presents the
ecosystem has matured substantially, with infrastructure such       evaluation protocol. Section VII reports the empirical results
as LeanDojo exposing proof states, premises, and benchmarks         and explains where SCOPE helps most and why. Section VIII
to learning-based systems [21], [22]. At the same time, Lean-       discusses implications and limitations. Finally, Section IX
oriented LLMs have shown that models can make progress              concludes the paper.
by decomposing difficult problems into intermediate subgoals
rather than relying on unconstrained text generation alone [23],    II. BACKGROUND : W HY P ROVER -S TYLE D ECOMPOSITION
[24]. These developments suggest a more limited and practical                    F ITS C ODE G ENERATION
use of prover-trained models for code generation. Rather than          Lean is an interactive theorem prover in which reasoning
treating Lean as a runtime verifier for Python, we ask whether      is expressed as a sequence of machine-checkable proof states.
the decomposition behavior learned by Lean-oriented prover          As illustrated in Figure 2A, a proof starts from a goal together
models can be repurposed as structured semantic feedback for        with local hypotheses, and tactics transform that state by
code repair [25].                                                   reducing one difficult goal into several smaller subgoals. A
   Motivated by this idea, we propose SCOPE, a prover-              proof is complete only when all subgoals are discharged. For
initialized subgoal critic for code generation. As illustrated      SCOPE, this view is an analogy and a source of model prior,
in Figure 1, SCOPE is designed to fill the gap between              not a runtime verification procedure. Each emitted subgoal is a
ambiguous natural-language intent and actionable repair sig-        natural-language semantic obligation, such as a precondition,
nals. Given a task and a draft program, the critic emits            an invariant, an output constraint, or an edge case requirement.
three structured fields: subgoals that state what the solution         The useful property for code generation is not formal
should satisfy, gap analysis that compares the draft against        certification, but disciplined decomposition. In Lean, reasoning
those subgoals, and a robustness checklist that highlights          does not proceed as unconstrained text generation. At each
boundary conditions. The output is natural language, not a          step, the prover operates on an explicit proof state: a typed
machine-checked Lean proof, but it is constrained enough to         goal together with local hypotheses. This state rules out many
be parsed and fed back to the coder. SCOPE therefore provides       irrelevant directions, and tactics further narrow the search by
a practical middle ground between weak test-only feedback           transforming one hard goal into a small number of concrete
and expensive end-to-end formal verification. Concretely, our       subgoals. SCOPE borrows this decomposition pattern for feed-
approach has three stages: (1) supervised fine-tuning to adapt      back: the critic should not rewrite the program or produce a
a Lean-oriented prover model to the critic interface, (2)           long reflection, but should identify a compact set of obligations
process-aligned reinforcement learning with dense semantic          that a coder can inspect and repair.
rewards and sparse execution rewards, and (3) feedback-based           This is exactly the kind of structure that natural-language-to-
inference, where the critic’s structured output guides iterative    code generation lacks. A programming prompt usually bundles
code revision.                                                      together several requirements, such as functional behavior,
   We summarize the contributions of this paper as follows:         boundary conditions, interface constraints, and hidden invari-
   1) We present SCOPE, a prover-initialized LLM as a               ants, but standard code generation leaves these requirements
       subgoal critic in two model code generation framework.       implicit. As a result, a code model may produce a plausible
   2) We design a process-aligned reward framework for              program while missing one thin semantic condition that later
       training the critic in coding tasks. It combines a dense     causes failure. SCOPE uses a prover-initialized critic as an
       reward for producing structured, semantically useful         intermediate layer because it can turn mixed natural-language
       critiques and a sparse reward based on whether the           intent into explicit repair obligations. Once these obligations
       critique ultimately helps the coder generate a correct       are exposed, the search problem becomes smaller and better
       program under execution based evaluation.                    organized: instead of searching broadly for any revision that
   3) We show that SCOPE achieves stronger performance              might pass tests, the system can focus on edits that address a
       than competitive self-refinement baselines. On Live-         specific violated condition.
       CodeBench V6, SCOPE reaches 39.4% pass@1, outper-               DeepSeek-Prover-V2 is especially well matched to this
       forming Reflexion at 36.6%, Self-Refine at 33.1%. On         role because it is already trained to reason through recursive
       BigCodeBench, SCOPE achieves 42.6% pass@1, again             subgoal decomposition rather than free-form explanation [23].
       surpassing Reflexion 36.5%.                                  SCOPE uses this model in a limited way. We do not ask it
   4) We provide evidence for why SCOPE works better.               to synthesize Python, call Lean, or certify the entire program
       Our analysis shows that, SCOPE rescues more failed           end to end. We prompt and post-train it to recover a semantic
       solutions than Reflexion (19 vs. 16), achieves better bug-   view of the task, identify which obligations the current draft
       triggered localization (42.1% vs. 31.3% localized wins       appears to violate, and return those failures as structured
Fig. 2. Illustration of the subgoal-decomposition prior that motivates SCOPE. (A) In Lean, tactics transform one formal goal into smaller subgoals that must
all be discharged. (B) DeepSeek-Prover-V2 is trained for Lean proof construction and inherits this bias toward decomposing a problem into intermediate
obligations. SCOPE does not run this proof search on Python code; it reuses the model as a critic that emits natural-language obligations for repair.




Fig. 3. The figure contrasts Reflexion’s broad natural-language reasoning with SCOPE’s subgoal-guided analysis, which exposes the missing invariant and
maps failure to a precise local fix.



feedback. In this sense, the prover model acts as a semantic                   number such as 022 is counted as valid. Given the failing case
search controller: it makes intent explicit, prunes semantically               [0, 2, 2] → 2, the system knows only that the current output is
irrelevant revisions early, and converts vague failures into                   wrong. It generates a long natural-language critique, but the
localized repair targets.                                                      feedback does not isolate the violated constraint. As a result,
                                                                               the search remains broad: the model can revise many parts of
                    III. M OTIVATION E XAMPLE                                  the program without directly addressing the real issue, namely
   Figure 3 shows a real example from LiveCodeBench. The                       that a number with a leading zero is being treated as valid.
task is: count distinct 3-digit even numbers formed from a                        The right side of Figure 3 shows how SCOPE changes
multiset of digits, allowing reuse only when multiple copies                   this process. We keep the same coder, but replace free-form
exist. The prompt contains several constraints at once: the                    feedback with a structured critic initialized from DeepSeek-
number must be 3-digit, the first digit cannot be zero, the                    Prover-V2-7B. Instead of producing broad discussion, the
last digit must be even, each digit can be used only as often                  critic decomposes the prompt into explicit obligations and
as it appears in the input, and duplicate valid numbers should                 identifies that the validity condition is violated. This turns the
be counted once. Both R EFLEXION [26] and our approach                         error into a local repair problem: the revision only needs to
are feedback-based code generation methods: they improve an                    enforce that the first digit is non-zero. The resulting fix is
initial draft by feeding critique generated by feedback LLM                    small, targeted, and semantically grounded.
back to the coder for revision. The key difference is that                        This example captures the main motivation for SCOPE.
R EFLEXION relies mainly on natural-language feedback from                     The advantage comes from using structured semantic feedback
test traces, whereas SCOPE asks a prover-initialized critic                    emitted by the critic. By converting informal intent into
to produce structured semantic feedback that makes missing                     explicit obligations, SCOPE narrows the repair space and
obligations and likely failure points more explicit.                           makes code revision more precise.
   The left side of Figure 3 illustrates this failure mode with
a Reflexion setup. The coder is Qwen3-Coder-30B, and the                                                IV. R ELATED W ORK
feedback model is Qwen3-8B. The Reflexion fails because the
coder generates plausible counting logic but misses one hidden                   This section reviews prior work most relevant to our
semantic constraint: it allows a leading zero, so an invalid                   approach, including LLM-based code generation, feedback-
Fig. 4. SCOPE couples a coder with a prover-initialized critic that receives the problem and draft code, then emits structured subgoals, gap analysis, and
robustness checks. During training, the critic is aligned with dense semantic rewards and sparse execution-based rewards. During inference, its critique guides
iterative revision by the coder.
driven refinement, and formal reasoning for program repair                       can generate feedback on its own output and then repeatedly
and verification.                                                                revise it, while R EFLEXION extends this idea with verbal
                                                                                 reinforcement and episodic memory across attempts [33], [26].
A. LLMs for Code Generation and Hallucination                                    In the coding setting, S ELF -D EBUG further demonstrates that
   Code LLMs have rapidly advanced natural-language-to-                          execution results and natural-language explanations can help
code generation. Open models, including C ODE L LAMA and                         a model inspect and repair its own programs rather than
S TAR C ODER, further improved support for multi-language                        merely resample candidates [34]. These methods establish
generation and deployment in developer-facing tools [27],                        an important point: even without changing model weights,
[28].                                                                            test-time feedback can substantially improve code generation
   A growing body of work shows that the remaining relia-                        quality [35], [36].
bility gap is a hallucination problem. Recent studies develop                       A second line of work makes the feedback signal more
taxonomies of code hallucinations and show that these errors                     explicit or more structured. C ODE RL introduces a critic
include invented APIs, incorrect package names, resource                         trained to estimate functional correctness from unit-test out-
assumptions, mapping mistakes, and faulty program logic [29],                    comes, bringing feedback into the training loop rather than
[30], [6]. These failures are obvious from surface form alone:                   relying only on post-hoc prompting [37]. More recent frame-
a generated program can look polished while violating hidden                     works such as T EXT G RAD cast natural-language critique
constraints or relying on nonexistent dependencies. Package                      as a gradient-like optimization signal over compound LLM
hallucinations make this risk even more concrete by turning                      systems [38], while R EPAIR AGENT frames repair as an au-
generation errors into potential software-supply-chain expo-                     tonomous agentic loop that alternates among fault localization,
sure [31]. Several mitigation strategies have therefore been                     patch generation, and validation [39].
proposed. For example, D E -H ALLUCINATOR grounds gener-
ation with iteratively retrieved project-specific API context                    C. Lean, Formal Proof, and LLM-Based Provers
to reduce repository-level API hallucinations [32]. However,                        Lean is a modern interactive theorem prover with a small
most existing approaches still ground code using retrieved                       trusted kernel and dependent type theory, making proofs
context, execution feedback, or post-hoc detection, rather than                  explicit and machine-checkable [20]. Recent infrastructure
explicitly representing the semantic obligations implied by the                  such as L EAN D OJO has made Lean more accessible to
original natural-language task.                                                  learning-based systems by exposing proof states, premises, and
                                                                                 benchmarks, which helped turn formal proving into a more
B. Feedback-Based LLM Code Generation Systems                                    standard LLM setting [21]. Building on this ecosystem, spe-
   Feedback-based code generation systems improve on single-                     cialized provers such as D EEP S EEK -P ROVER and D EEP S EEK -
shot decoding by inserting an iterative critique, verification,                  P ROVER -V2 show that LLMs can learn premise use, proof
or repair loop around a base model. A first line of work                         search, and especially subgoal decomposition in Lean, rather
studies self-feedback: S ELF -R EFINE shows that the same LLM                    than relying only on free-form reasoning [40], [23].
   A related line studies LLMs for formal proof and verified        the code generation task. Given a problem description x and
programming more directly. BALDUR explores whole-proof              an initial draft program p0 , the critic is trained to generate a
generation and repair with LLMs, while benchmarks such              structured critique
as DAFNY B ENCH and CLEVER show both the promise                                             y = (s, g, c),                       (1)
and the difficulty of generating machine-checked proofs or
                                                                       where s denotes the subgoals, g the gap analysis, and c the
verified programs from natural-language tasks [13], [16], [17].
                                                                    robustness checklist. The target here is a compact semantic
However, most of this work assumes a verifier-native target
                                                                    decomposition of the draft that can guide later repair.
language, a pre-existing formal specification, or direct proof-
                                                                       We initialize from DeepSeek-Prover-V2-7B and fine-tune
state feedback.
                                                                    it on the critique traces constructed in Section V-A. These
                     V. M ETHODOLOGY                                targets are refined by a tutor model so that the supervision is
   Figure 4 summarizes our methodology. SCOPE has two               consistent in both structure and quality. As a result, SFT serves
runtime models: a frozen coder and a critic initialized             primarily as a role-alignment stage: it teaches the model to
from DeepSeek-Prover-V2-7B. The critic receives the natural-        act as a semantic critic in the code generation task instead of
language problem and the coder’s draft program. The method-         mathematical proving.
ology consists of three stages: data construction, where we            The supervised completion is the exact format used in the
build critique traces with a tutor LLM for code generation;         implementation:
supervised fine-tuning, where we warm-start the critic to emit           <subgoal> s </subgoal> <gap_analysis>
                                                                         g    </gap_analysis>  <checklist>   c
the exact tag format consumed by the coder; and process-                 </checklist>.
aligned reinforcement learning, where dense semantic re-
                                                                      Formally, for each training example (x, p0 , y ⋆ ), where
wards and sparse execution rewards further optimize the critic
to produce feedback that helps the coder generate correct code.                             y ⋆ = (s⋆ , g ⋆ , c⋆ ),                 (2)
A. Data Construction                                                we optimize the standard conditional language-model objec-
   We construct training data by replaying the same critique-       tive
                                                                                           |y ⋆ |
guided revision process used by SCOPE at inference. To avoid
                                                                                           X
                                                                             LSFT (θ) = −         log pθ (yt⋆ | x, p0 , y<t
                                                                                                                         ⋆
                                                                                                                            ). (3)
overfitting to our main evaluation benchmark, we build the                                     t=1
training set from LiveCodeBench V1–V3. Each task provides
                                                                       In implementation, the prompt tokens corresponding to
a natural-language problem statement, optional starter code,
                                                                    (x, p0 ) are masked out, so the loss is applied only to the
and test cases.
                                                                    completion tokens of the structured critique. Intuitively, SFT
   For each task, a coder first generates an initial draft p0 . A
                                                                    teaches the model what kind of critique to produce, while
tutor critic then analyzes the draft and produces a structured
                                                                    the later RL stage teaches it which critiques actually help the
critique y, including subgoals, gap analysis, and a checklist.
                                                                    coder. In this sense, SFT provides the structural prior that
Conditioned on this critique, the coder produces a revised
                                                                    makes process-aligned reinforcement learning feasible.
program p1 . This yields a process-level training tuple
                                                                    C. Process-Aligned Reinforcement Learning with Dense and
                         (x, p0 , y, p1 ),
                                                                    Sparse Rewards
where x is the original problem.                                       SFT alone does not guarantee that a critique is useful for
   In our pipeline, we use Qwen3-Coder-30B as the coder             downstream repair. A critic may produce well-formed subgoals
and DeepSeek-V3 to generate critique traces. We store the           and fluent gap analysis that look reasonable to a human reader,
task, draft, revision, and normalized critique fields for each      yet still fail to help the coder generate a correct program. We
example. We next use these critique-guided traces to warm-          therefore further optimize the critic with Group Relative Policy
start the critic with supervised fine-tuning, which provides a      Optimization (GRPO), using a reward that combines dense
smoother transition from data construction to the downstream        semantic guidance with sparse execution-based feedback.
RL stage. Across LiveCodeBench V1 to V3, this procedure                For a task x and draft program p0 , the critic policy πθ
yields 528 critique-guided training tuples. Each tuple contains     samples a structured critique y. This critique is then fed to the
the original task, the initial draft, the structured critique,      coder, which produces a revised program p(y). The revised
and the revised program. The reference critiques are teacher-       program is executed on benchmark tests, and the critic is
generated and therefore are not treated as ground truth proofs;     rewarded according to whether its critique actually improves
they provide dense format and content supervision, while            downstream correctness. This makes the RL signal process-
downstream execution reward later checks whether a critique         aligned: The critic is rewarded not for writing code, but for
actually helps repair.                                              producing feedback that helps another model repair code.
                                                                       We optimize the policy with GRPO:
B. Supervised Fine-Tuning of the Prover Critic
  We first warm-start the critic with supervised fine-tuning        max Ey∼πθ (·|x,p0 ) [R(y)]−β KL(πθ (· | x, p0 ) ∥ πref (· | x, p0 )) ,
                                                                     θ
(SFT) so that it learns the subgoal decomposition interface in                                                                      (4)
   where πref is the reference policy initialized from SFT, and      D. Inference: SCOPE as a Critique-Guided Revision Loop
β controls the strength of KL regularization.
                                                                       At inference time, SCOPE instantiates a two-model revision
     a) Dense reward.: The dense reward encourages the
                                                                     loop between a coder and a post-trained critic. Given a task x,
generated critique to remain structurally valid, semantically
                                                                     the coder first produces an initial draft program p0 . The critic
aligned, and practically readable. We define
                                                                     then receives (x, p0 ) and returns a structured critique
        Rdense (y) = λemb Remb (y) + λqual Rqual (y).         (5)
                                                                                              y = (s, g, c),                      (9)
   The first term, Remb , measures semantic alignment between
the generated critique and the teacher-generated targets in the        where s, g, and c denote the subgoals, gap analysis, and
training trace. Concretely, it scores the generated subgoals, gap    robustness checklist, respectively. Conditioned on this critique,
analysis, and checklist against their target counterparts:           the coder produces a revised program

 Remb (y) = αs sim(s, s⋆ )+αg sim(g, g ⋆ )+αc sim(c, c⋆ ), (6)                              p1 = C(x, p0 , y),                   (10)

where sim() denotes an embedding-based similarity function              where C(·) denotes the frozen coder. In this way, inference
and αs + αg + αc = 1.                                                mirrors the same critic-guided repair process used during
   The second term, Rqual , scores critique quality. Its role is     training, ensuring that the critic is deployed in exactly the
to reward outputs that are concise, grounded in the current          role for which it was optimized. The subgoals define what
draft, parseable by the revision prompt, and structurally useful     the program must satisfy, the gap analysis explains where
for repair. In our main setting, this signal is provided by a        the current draft violates those obligations, and the checklist
frozen GPT-5.2 judge, which evaluates whether the critique is        highlights boundary conditions that are easy to miss during
actionable rather than merely fluent. The semantic similarity        revision. By packaging these three components into a single
alone is not enough: a critique can overlap with the target text     output, SCOPE gives the coder a unified repair target rather
yet still be vague or unhelpful.                                     than a set of loosely related suggestions.
     b) Sparse reward.: The sparse reward captures the actual           Formally, the inference objective is not to search directly
downstream value of the critique from testing. After sampling        over programs, but to improve the draft through critic-guided
y, we invoke the coder to revise p0 into p(y), then run the          revision. If S(·) denotes the hidden execution-based correct-
revised program on benchmark tests. Let S(·) denote the              ness signal, SCOPE aims to produce critiques such that
shaped execution score, which reflects not only binary pass/fail
but also partial test progress and lightweight penalties for                                 S(p1 ) > S(p0 ),                    (11)
runtime failures. We then define the sparse reward as
                                                                        and, more generally, such that the revised program moves
                Rsparse (y) = S(p(y)) − S(p0 ).               (7)    closer to satisfying the problem’s latent semantic constraints.
                                                                     This formulation reflects the central intuition of our method:
   It rewards the critic only for improvement over the original      the critic adds value not by replacing the coder, but by
draft. As a result, the critic is encouraged to generate critiques   exposing the obligations that the current draft has not yet made
that expose the draft’s missing semantic obligations and help        explicit.
the coder make targeted repairs.
      c) Final reward.: Our final reward combines the dense                                VI. E VALUATION
and sparse terms:
                                                                        We organize the evaluation around three questions:
       R(y) = wdense Rdense (y) + wsparse Rsparse (y),        (8)    RQ1: Does SCOPE improve end-to-end code generation ac-
                                                                     curacy over coder-only and iterative baselines?
   This combination reflects the two goals of SCOPE. The
                                                                     RQ2: Where are these gains concentrated: are they consistent
dense term keeps the critic anchored to the intended semantic
                                                                     across benchmarks, or do they appear mainly in particular
structure and prevents drift into unstructured free-form text.
                                                                     difficulty levels and problem categories?
The sparse term ensures that the critic is ultimately optimized
                                                                     RQ3: When SCOPE improves a failed baseline solution, does
for what matters most: whether its feedback helps the coder
                                                                     it do so through more precise repair behavior, such as localized
produce a correct program under execution-based evaluation.
                                                                     edits or specific types of semantic corrections?
   A useful way to interpret the two terms is as follows. The
dense reward teaches the critic to produce well-formed cri-
                                                                     A. Baselines
tiques; the sparse reward teaches it to produce useful critiques.
SCOPE needs both. Without the dense term, optimization                     a) Coder-Only: This is the coder-only baseline.Qwen3-
becomes unstable and the model may exploit noisy execution           Coder-30B receives the problem description and function
signals. Without the sparse term, the critic may learn to imitate    signature, generates a single solution, and that solution is
well-formed obligations that are linguistically plausible but do     evaluated directly. There is no critic model and no refinement
not improve code generation in practice.                             step.
     b) Self-Refine [33]: This baseline keeps Qwen3-Coder-         into four categories: crash-like failures, which include non-
30B as the coder and uses Qwen3-8B to generate a lightweight       AssertionError runtime failures; assertion-only failures,
natural language critique of the draft. The feedback points        where the program runs but does not satisfy the hidden tests;
out weaknesses in the current solution and suggests possible       mixed failures, where multiple failure types appear across
improvements in text, after which the coder revises the solution   attempts. This lets us examine not only whether SCOPE
once based on that critique. This baseline tests whether generic   improves final accuracy, but also whether it changes the kinds
textual self feedback is sufficient for code repair.               of errors the system tends to make.
     c) Reflexion [26]: This baseline also uses Qwen3-                   d) Difficulty and category breakdown.: To understand
Coder-30B as the coder and Qwen3-8B as the feedback                where the method helps most on LiveCodeBench, we join each
model. Unlike Self-Refine, the critic additionally observes        task’s official difficulty label with the corresponding binary
execution feedback, such as failing inputs, expected outputs,      pass/fail outcome and aggregate solved counts by difficulty
and runtime errors. It then produces natural language debug-       level. We report results for Easy, Medium, and Hard tasks sep-
ging feedback, which the coder uses for iterative revision.        arately. We also analyze performance by algorithmic category,
This setting represents a strong execution guided interactive      following the benchmark’s LeetCode style taxonomy, such as
baseline.                                                          array, string, hash table, math, greedy, dynamic programming,
     d) SCOPE (Untrained): This variant uses Qwen3-                graph, tree, binary search, and simulation. This breakdown
Coder-30B as the coder and a raw DeepSeek-Prover-V2-               helps show whether the gains are broadly distributed or
7B model as the critic. The critic is prompted to produce          concentrated in particular classes of problems.
structured subgoals, gap analysis, and a checklist, but it is            e) Repair localization and revision analysis.: We also
used without SFT or RL. This comparison isolates the value         study where successful repairs occur and what kinds of re-
of the prover-initialized critic before adaptation.                visions they make. For tasks where a coder-only approach
     e) SCOPE (SFT): This variant keeps the same coder,            fails but a target method succeeds, we perform a manual
Qwen3-Coder-30B, and replaces the critic with an SFT-              fault-localization check on the failing coder-only solution.
adapted DeepSeek-Prover-V2-7B. The goal of this compari-           Concretely, we inspect the failing program together with its
son is to measure how much role alignment alone helps, before      execution feedback, including traceback information, assertion
reinforcement learning is introduced.                              messages, and failing input & output behavior, and then
     f) SCOPE (Full).: Our full system again uses Qwen3-           mark the line, or smallest contiguous region, most directly
Coder-30B as the coder, but the critic is the fully post-          responsible for the failure. We refer to the center of this
trained DeepSeek-Prover-V2-7B after both SFT and GRPO.             marked region as the trigger line, denoted by ℓtrigger . We
The critic outputs structured semantic feedback in the form of     then compare the failing coder-only solution against the final
subgoals, gap analysis, and a robustness checklist, which the      successful solution and identify the main edited hunk; the
coder uses for revision.                                           center of that hunk is treated as the fix line, denoted by ℓfix . We
                                                                   summarize localization quality by the absolute line distance
B. Benchmarks, Metrics, and Analysis Protocol
                                                                                          d = |ℓfix − ℓtrigger | .                (12)
      a) Benchmarks.: We evaluate primarily on Python code
generation with LiveCodeBench V6, using the official execu-            Smaller d indicates that the successful repair stays closer
tion harness. This subset contains 175 tasks, each defined by a    to the inferred fault location. To quantify edit magnitude, we
natural-language problem description together with a Python        compute the changed-line count between the failing solution
function signature. Our setting is a controlled same-coder         and the final successful solution. Let Lbase and Lfinal be the
repair comparison. To test whether the method generalizes          sets of non-empty lines in the two versions after line based
beyond the benchmark used most heavily during development,         alignment. This yields a directly comparable trigger–fix view
we also evaluate on BigCodeBench-Complete (Hard), which            across methods under the same failure pool.
contains 148 Python tasks.                                             Under this protocol, we report several complementary repair
      b) Primary metric.: Our main metric is pass@1, defined       metrics. N Wins is the number of tasks where the coder-only
as the fraction of tasks for which a method produces a             solution fails but the target method succeeds. Recovery Rate
final submission that passes all hidden tests. For the coder-      normalizes this count by the size of the coder-only non-pass
only baseline, pass@1 is computed from its single generated        pool. Localized Wins @20 is the fraction of all recovered
solution.                                                          tasks whose fix lies within 20 lines of the trigger, that is,
      c) Pairwise comparison and failure modes.: Beyond            |ℓfix − ℓtrigger | ≤ 20. Trigger+Fix Coverage is the fraction of
overall pass@1, we compare SCOPE against each baseline             recovered tasks for which localization can be evaluated under
on a per-task basis. For each pair, we count wins, where           our protocol. A task is counted as covered only when we can
SCOPE solves a task that the baseline fails, and regressions,      identify both (1) a trigger line in the coder-only failing solution
where the baseline solves a task that SCOPE fails. This            from its failure signal, and (2) a dominant fix line in the target
analysis shows whether SCOPE’s gains come from broad               successful solution from the main diff hunk. Localized Share
improvements across many tasks or only from a small number         Among Covered is the fraction of these covered tasks whose
of isolated cases. For unsolved tasks, we also group failures      fix lies within 20 lines of the trigger. This metric conditions on
                                                                 TABLE I
                     PASS @1 BY D IFFICULTY ON L IVE C ODE B ENCH V6 ACROSS SIX APPROACHES . B EST PER ROW IN BOLD .

     Difficulty     Coder-Only           Reflexion        Self-Refine    SCOPE (Untrained)        SCOPE (SFT)           SCOPE (Full)
     Easy          26/43 (60.5%)     39/43 (90.7%)     39/43 (90.7%)            41/43 (95.3%)      41/43 (95.3%)        42/43 (97.7%)
     Medium         8/52 (15.4%)     16/52 (30.8%)     16/52 (30.8%)            17/52 (32.7%)      16/52 (30.8%)        18/52 (34.6%)
     Hard           2/80 ( 2.5%)      9/80 (11.2%)      3/80 ( 3.8%)             6/80 ( 7.5%)       5/80 ( 6.2%)         9/80 (11.2%)
     Overall      36/175 (20.6%)    64/175 (36.6%)    58/175 (33.1%)           64/175 (36.6%)    62/175 (35.4%)        69/175 (39.4%)



the subset where a trigger-to-fix comparison is actually well         and +2.8 absolute pass@1 points; relative to the coder-only
defined. Median Changed Lines is the median line-diff size            baseline, the gain is 33 additional solved tasks and +18.8
between the coder-only solution and the target final solution.        points.
Median Changed Ratio further normalizes edit size by the                 We also evaluate on BigCodeBench (Hard) as a cross-
length of the coder-only program. Higher is better for recovery       benchmark generalization check. This second benchmark dif-
and localization metrics, while lower is better for edit-size         fers in composition and is evaluated with its own official
metrics.                                                              calibrated execution setting. The result is consistent with the
                                                                      main benchmark in table III: SCOPE (Full) achieves 63/148
C. Training settings
                                                                      solved tasks (42.6% pass@1), compared with 54/148 (36.5%)
   We train the critic in two stages: a supervised warm-              for Reflexion, 51/148 (34.5%) for coder-only generation,
start followed by GRPO-based reinforcement learning. All              and 62/148 (41.9%) for SCOPE (SFT). SCOPE remains the
training is conducted on 2× NVIDIA RTX A6000 GPUs using               strongest method even when evaluated on a second execution-
parameter-efficient fine-tuning. For both stages, we adopt            based benchmark with a different task distribution.
QLoRA with rank r = 16, α = 32, dropout 0.05, all-                       Overall, SCOPE delivers the strongest performance in our
linear target modules, and 4-bit NF4 quantization. In the SFT         main evaluation, and this advantage remains visible when we
stage, we fine-tune DeepSeek-Prover-V2-7B with optimizer              test on a second benchmark designed to reduce concern about
AdamW, gradient accumulation 8, learning rate 1 × 10−4 ,              benchmark-specific fitting.
warmup ratio 0.03, and 80 training steps. We then initialize
GRPO from the SFT checkpoint and continue training with the           B. RQ2: On Which Kinds of Tasks Does SCOPE Help Most,
same backbone and LoRA setting for 120 maximum steps. The             by Difficulty and Problem Category?
RL training mixture keeps broad regenerated LiveCodeBench
                                                                         In Table I, we demonstrate the difficulty breakdown per-
V1–V3 data and upweights focused hard-fail slices used for
                                                                      formance. On Easy tasks, SCOPE (Full) achieves the best
curriculum. We therefore interpret the LiveCodeBench V6
                                                                      result with 42/43 solved (97.7%), improving over Reflexion
result as an in-family repair evaluation and use BigCodeBench
                                                                      and Self-Refine, both at 39/43 (90.7%), and over the coder-
as the cleaner cross-benchmark generalization check.
                                                                      only baseline at 26/43 (60.5%). On Medium tasks, SCOPE
                        VII. R ESULTS                                 again obtains the strongest result with 18/52 solved (34.6%),
  We organize the results from overall effectiveness to deeper        compared with 16/52 (30.8%) for Reflexion and Self-Refine
analysis: we first compare SCOPE against baselines on bench-          and 8/52 (15.4%) for the baseline. On Hard tasks, SCOPE
mark performance, then study behavior across difficulty levels        reaches 9/80 (11.2%), matching Reflexion and clearly out-
and problem categories, and finally examine where the gains           performing Self-Refine at 3/80 (3.8%) and the baseline at
come from through a fine-grained error analysis.                      2/80 (2.5%). This pattern suggests that SCOPE consistently
                                                                      improves reliability up to the medium range and remains
A. RQ1: Does SCOPE Improve Overall Code Generation                    strong on hard tasks, while more exploratory feedback can
Accuracy Across Benchmarks?                                           still sometimes rescue especially difficult cases.
   In table I, the comparison isolates the effect of the feedback        In Table II, the category breakdown clarifies where
mechanism: no feedback for the Coder-Only, unconstrained              SCOPE’s gains come from. SCOPE (Full) is the strongest in
self-critique for Self-Refine, execution trace guided natural         most of the reported categories. On array tasks, the base-
language feedback for Reflexion, and prover-initialized sub-          line solves none of the tasks (0.000), whereas all feedback-
goal feedback for SCOPE. Under this setup, SCOPE (Full) is            based methods, including SCOPE, reach 0.455. On dynamic
the best-performing system overall. On LiveCodeBench V6,              programming, SCOPE reaches 0.250, exceeding Reflexion at
SCOPE (Full) solves 69/175 tasks, achieving 39.4% pass@1,             0.167 and both the baseline and Self-Refine at 0.000. It fits
compared with 64/175 (36.6%) for Reflexion, 58/175 (33.1%)            the intuition that dynamic programming requires preserving
for Self-Refine, 64/175 (36.6%) for SCOPE (Untrained),                intermediate invariants and state relationships that benefit from
62/175 (35.4%) for SCOPE (SFT), and 36/175 (20.6%) for                explicit subgoal decomposition.
the coder-only baseline. Relative to the strongest baseline,             SCOPE is also strong on categories where hidden con-
Reflexion, SCOPE improves by 5 additional solved tasks                straints are global rather than purely local. On hash-map
                                                            TABLE II
                  PASS @1 BY A LGORITHMIC C ATEGORY ON L IVE C ODE B ENCH V6. B EST PER CATEGORY COLUMN IN BOLD .

                       Approach              Array      DP     Graph     Hash Map      Math    Simulation    String
                       Coder-only            0.000    0.000     0.063          0.385   0.262        0.214    0.333
                       Reflexion             0.455    0.167     0.375          0.692   0.381        0.286    0.500
                       Self-Refine           0.455    0.000     0.313          0.615   0.333        0.214    0.500
                       SCOPE (Untrained)     0.455    0.250     0.250          0.692   0.405        0.214    0.500
                       SCOPE (SFT)           0.455    0.167     0.250          0.615   0.381        0.286    0.444
                       SCOPE (Full)          0.455    0.250     0.375          0.692   0.405        0.357    0.444


                                                             TABLE III
C OMPARISON OF CODER - ONLY, R EFLEXION , SCOPE-SFT, AND SCOPE ON B IG C ODE B ENCH . S OLVED AND PASS @1 REPORT OVERALL PERFORMANCE .
“SCOPE W INS ” AND “SCOPE R EGR .” ARE MEASURED RELATIVE TO SCOPE ( OURS ). FAILURE CATEGORIES SUMMARIZE THE REMAINING UNSOLVED
                                                              CASES .


       Method             Solved    pass@1    SCOPE Wins        SCOPE Regr.       Fail-Crash   Fail-AssertionOnly     Fail-Mixed
       Coder-only         51/148    0.3446                19                  7           30                   53            14
       Reflexion          54/148    0.3649                16                  7           33                   50            10
       SCOPE (SFT)        62/148    0.4189                 4                  3           23                   51            11
       SCOPE (Full)       63/148    0.4257                 –                  –           21                   52            11


                                                               TABLE IV
      C ODER - ONLY- ANCHORED LOCALIZATION COMPARISON ON B IG C ODE B ENCH -C OMPLETE (H ARD ). E ACH ROW USES THE SAME CODER - ONLY
  CODER - ONLY BASELINE AS THE ANCHOR . W E CONSIDER TASKS WHERE THE CODER - ONLY SOLUTION FAILS AND THE TARGET METHOD SUCCEEDS .
  H IGHER IS BETTER FOR RECOVERY AND LOCALIZATION METRICS ; LOWER IS BETTER FOR EDIT- SIZE METRICS . B EST VALUES ARE SHOWN IN BOLD .

          coder-only           N   Recovery Trigger+Fix Localized Localized Share Median Changed Median Changed
          → Target            Wins   Rate    Coverage Wins @20 Among Covered          Lines ↓        Ratio ↓
   Coder-only → Reflexion      16     16.5%          37.5%        31.3%           83.3%               35.0               0.703
   Coder-only → SCOPE          19     19.6%          47.4%        42.1%           88.9%               28.0               0.577



tasks, SCOPE reaches 0.692, tying Reflexion for the best                when a draft is close enough to repair and the missing behavior
result and improving over the baseline at 0.385. On math                can be expressed as a small number of explicit obligations.
tasks, SCOPE achieves the best score at 0.405, compared with
0.381 for Reflexion and 0.262 for the baseline. On simulation,
SCOPE attains 0.357, again the highest value in the table,              C. RQ3: What Explains SCOPE’s Advantage Over Baselines
improving over Reflexion at 0.286 and the baseline at 0.214.            in Localization and Revision Behavior?
These gains are consistent with the intended role of SCOPE:
                                                                           Table III combines three complementary views of per-
making latent semantic requirements explicit enough that the
                                                                        formance: overall pass@1, pairwise win/loss decomposition
coder can repair them systematically rather than relying only
                                                                        against each baseline, and failure-mode shift on the remain-
on free-form critique. On graph problems, SCOPE reaches
                                                                        ing unsolved tasks. Under this view, SCOPE achieves the
0.375, tying Reflexion for the best result and outperforming
                                                                        strongest overall result on BigCodeBench-Complete (Hard),
Self-Refine at 0.313 and the baseline at 0.063. Graph problems
                                                                        solving 63/148 tasks (42.6% pass@1), compared with 54/148
are often structurally complex. They can also admit multiple
                                                                        (36.5%) for Reflexion and 51/148 (34.5%) for coder-only
plausible solution paths. As a result, SCOPE’s advantage
                                                                        generation. Relative to Reflexion, this corresponds to a net
is smaller on these tasks. Success often depends more on
                                                                        gain of +9 tasks (16 SCOPE wins vs. 7 regressions); relative
exploring alternative strategies than on correcting a specific
                                                                        to coder-only generation, the gain is +12 tasks (19 wins vs. 7
semantic error.
                                                                        regressions). The same table also shows that SCOPE produces
   SCOPE improves over Reflexion on dynamic programming                 the fewest crash-like failures among the compared methods. In
(0.250 vs. 0.167), math (0.405 vs. 0.381), and simulation               particular, Fail-Crash cases decrease from 33 under Reflexion
(0.357 vs. 0.286), while tying Reflexion on graph and hash-             to 21 under SCOPE, and from 30 under coder-only generation
map tasks. These are categories where failures often come               to 21. Crash failures are qualitatively different from pure
from violating a recurrence, numeric invariant, uniqueness              assertion failures: they often indicate unresolved semantic
condition, or state-transition rule. The gains are smaller where        mismatches, such as incorrect exception behavior, wrong API
the main challenge is broad strategy exploration rather than            usage, or failure to satisfy hidden structural constraints in
fixing a specific violated obligation. SCOPE is most useful             the harness. SCOPE is more often repairing the semantic
conditions that prevent the program from executing correctly        code editing. Such a state can help determine which con-
in the first place.                                                 straint is violated, where the likely fault lies, and whether
   Table IV demonstrates the localization comparison on the         the next revision should be local or global. Our findings also
same coder-only baseline for both Reflexion and SCOPE.              provide evidence for role specialization in multi-agent code
Under this shared baseline, SCOPE rescues more coder-only           generation. In SCOPE, a smaller, specialized critic improves
failures than Reflexion, improving from 16 wins to 19 wins, or      a larger coder not by generating better code directly, but by
from 16.5% to 19.6% recovery on the 97 coder-only non-pass          providing a stronger semantic representation of what the draft
tasks. SCOPE also yields higher trigger+fix coverage (47.4%         is missing. This suggests that future agentic systems may be
vs. 37.5%), which means a larger fraction of its successful         most effective when large coders are paired with smaller expert
repairs can be aligned to a concrete bug trigger and a concrete     critics for semantics, localization, and repair planning.
fix location. The difference also appears in localized rescue
behavior. SCOPE achieves 8 localized wins within a 20-              B. Threats to Validity and Limitations
line neighborhood of the coder-only trigger, compared with             Our study has several limitations. First, the evaluation scope
5 for Reflexion; as a rate over all wins, this is 42.1% for         is still narrow. SCOPE is trained and tested only on Python
SCOPE versus 31.3% for Reflexion. Even after restricting to         code-generation benchmarks, and the tasks are closer to code
cases where both trigger and fix can be identified, SCOPE           snippet level programming problems than to full repository
remains better (88.9% vs. 83.3%). At the same time, SCOPE           scale software engineering workflows. To reduce the risk
is more surgical: its median changed-line count is smaller          of overfitting to a single benchmark, we evaluate not only
(28.0 vs. 35.0), and its median changed-line ratio is also          on LiveCodeBench V6 but also on BigCodeBench (Hard),
lower (0.577 vs. 0.703). Taken together, these results support      which differs in task composition and execution setup. Even
a clearer mechanistic claim: SCOPE does not only solve more         so, broader validation across languages, real repositories, and
coder-only failures than Reflexion; it also repairs them more       longer-horizon agentic coding tasks remains future work.
consistently near the same baseline bug signal, while requiring        Second, SCOPE is not a full formal verification system. We
smaller code changes.                                               do not prove that the final Python program satisfies a complete
   SCOPE helps apply compact repairs near the actual fault          formal specification, and the semantic obligations generated
location when revision is needed. These repairs concentrate         by the critic may themselves be incomplete, approximate, or
on semantic-contract regions rather than on broad structural        occasionally misaligned with the true intent of the task. Our
rewrites.                                                           goal is therefore more practical than end-to-end certification:
                                                                    we use a prover-initialized model as a structured semantic
                      VIII. D ISCUSSION                             critic that makes intent more explicit before revision. To reduce
  Our results show that the main value of SCOPE is introduc-        the risk that the critic produces merely plausible but unhelpful
ing a prover-initialized critic that makes semantic obligations     obligations, we train it with both dense rewards for structured
explicit for revision. This suggests that feedback-based code       semantic quality and sparse rewards based on downstream
generation can benefit from structured intermediate reasoning,      execution improvement.
especially when the main errors are semantic.
                                                                                          IX. C ONCLUSION
A. Implications and Future Work                                        We present SCOPE, a prover-initialized subgoal critic
   Reduction of Search Space. A key implication of SCOPE            for Python code generation. By translating natural-language
is that structured obligations reduce the repair search space.      tasks into explicit repair obligations and comparing them
The implementation does not execute Lean tactics, but it            against draft programs, SCOPE provides structured feedback
borrows the prover-style habit of decomposing a large goal          that guides targeted repair. Through a three-stage design:
into smaller obligations. Once a programming task is rewritten      execution-grounded data construction, supervised fine-tuning,
as concrete obligations, many semantically irrelevant revisions     and process-aligned reinforcement learning with dense seman-
can be ruled out early. The coder is therefore not searching        tic reward and sparse execution reward, we show that prover-
broadly for any program that might pass hidden tests, but           style subgoal decomposition can be adapted from formal
revising within a smaller space of edits consistent with the        reasoning to practical code generation without claiming full
identified obligations. This helps explain why SCOPE tends to       formal verification.
produce compact, localized repairs rather than broad rewriting.        Through evaluation on LiveCodeBench and BigCodeBench,
As future work, this perspective suggests promising directions.     SCOPE achieves the strongest overall performance among the
One is to integrate subgoal-guided search more directly into        compared baselines, improving over coder-only generation and
decoding, allowing the coder to plan revisions around partially     feedback-based methods such as Reflexion and Self-Refine
satisfied obligations instead of relying only on post hoc repair.   under the same coder setting. Our analysis further shows that
   Implications for Agentic Coding Systems. Our results also        SCOPE helps most on tasks with stronger semantic structure,
suggest a broader implication for agentic software engineering      reduces crash-like failures, and produces more localized re-
systems. Future coding agents may benefit from maintaining          pairs rather than broad rewriting. These findings suggest that
an explicit obligation state between task understanding and         the main value of the prover-initialized critic in this setting is
not end-to-end verification, but making natural-language intent                  [17] A. Thakur, J. C. H. Lee, G. Tsoukalas, M. Sistla, M. Zhao, S. Zetzsche,
explicit enough to guide reliable revision.                                           G. Durrett, Y. Yue, and S. Chaudhuri, “CLEVER: A curated benchmark
                                                                                      for formally verified code generation,” in Advances in Neural
                                                                                      Information Processing Systems, vol. 38, 2025, datasets and Benchmarks
                                                                                      Track. [Online]. Available: https://papers.nips.cc/paper files/paper/
                              R EFERENCES                                             2025/hash/a7f67788f7b4d77fa7cd6887de3dcbe7-Abstract-Datasets
                                                                                      and Benchmarks Track.html
 [1] D. Nam, A. Macvean, V. Hellendoorn, B. Vasilescu, and B. Myers,             [18] R. Wang, J. Zhang, Y. Jia, R. Pan, S. Diao, R. Pi, and T. Zhang, “Theo-
     “Using an LLM to help with code understanding,” in Proceedings of                remLlama: Transforming general-purpose LLMs into Lean4 experts,” in
     the IEEE/ACM 46th International Conference on Software Engineering.              Proceedings of the 2024 Conference on Empirical Methods in Natural
     ACM, 2024, pp. 1–13.                                                             Language Processing. Association for Computational Linguistics, 2024,
 [2] S. Joel, J. Wu, and F. Fard, “A survey on LLM-based code generation              pp. 11 953–11 974.
     for low-resource and domain-specific programming languages,” ACM            [19] J. Zhang, Q. Wang, X. Ji, Y. Liu, Y. Yue, F. Zhang, D. Zhang,
     Transactions on Software Engineering and Methodology, 2025.                      G. Zhou, and K. Gai, “Leanabell-Prover: Posttraining scaling in formal
 [3] M. Kazemitabaar, X. Hou, A. Henley, B. J. Ericson, D. Weintrop, and              reasoning,” 2025. [Online]. Available: https://arxiv.org/abs/2504.06122
     T. Grossman, “How novices use LLM-based code generators to solve            [20] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and program-
     CS1 coding tasks in a self-paced learning environment,” in Proceed-              ming language,” in Automated Deduction – CADE 28. Springer, 2021,
     ings of the 23rd Koli Calling International Conference on Computing              pp. 625–635.
     Education Research. ACM, 2023, pp. 1–12.                                    [21] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
 [4] S. Zhao, A. Zhu, H. Mozannar, D. Sontag, A. Talwalkar, and V. Chen,              S. Godil, R. J. Prenger, and A. Anandkumar, “LeanDojo:
     “CodingGenie: A proactive LLM-powered programming assistant,” in                 Theorem proving with retrieval-augmented language models,” in
     Proceedings of the 33rd ACM International Conference on the Founda-              Advances in Neural Information Processing Systems, vol. 36,
     tions of Software Engineering. ACM, 2025, pp. 1168–1172.                         2023, pp. 21 573–21 612, datasets and Benchmarks Track.
 [5] A. S. Shethiya, “AI-assisted code generation and optimization in .NET            [Online]. Available: https://proceedings.neurips.cc/paper files/paper/
     web development,” Annals of Applied Sciences, vol. 6, no. 1, pp.                 2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets
     1–7, 2025, short article; verify venue suitability before submission.            and Benchmarks.html
     [Online]. Available: https://annalsofappliedsciences.com/index.php/aas/     [22] T. Hubert, R. Mehta, L. Sartran, M. Z. Horváth, G. Žužić, E. Wieser,
     article/view/15                                                                  A. Huang, J. Schrittwieser, Y. Schroecker, H. Masoom et al., “Olympiad-
 [6] Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen,                    level formal mathematical reasoning with reinforcement learning,” Na-
     M. Mao, and Z. Zheng, “LLM hallucinations in practical code gen-                 ture, vol. 651, no. 8106, pp. 607–613, 2025.
     eration: Phenomena, mechanism, and mitigation,” Proceedings of the          [23] Z. Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao,
     ACM on Software Engineering, vol. 2, no. ISSTA, pp. 481–503, 2025.               L. Zhang, Z. Fu, Q. Zhu, D. Yang et al., “DeepSeek-Prover-
 [7] X. Chen, C. Gao, C. Chen, G. Zhang, and Y. Liu, “An empirical study              V2: Advancing formal mathematical reasoning via reinforcement
     on challenges for LLM application developers,” ACM Transactions on               learning for subgoal decomposition,” 2025. [Online]. Available:
     Software Engineering and Methodology, vol. 34, no. 7, pp. 1–37, 2025.            https://arxiv.org/abs/2504.21801
 [8] C. Wang, K. Huang, J. Zhang, Y. Feng, L. Zhang, Y. Liu, and X. Peng,        [24] Y. Lin, S. Tang, B. Lyu, Z. Yang, J.-H. Chung, H. Zhao, L. Jiang,
     “LLMs meet library evolution: Evaluating deprecated API usage in                 Y. Geng, J. Ge, J. Sun et al., “Goedel-prover-v2: Scaling formal
     LLM-based code completion,” in 2025 IEEE/ACM 47th International                  theorem proving with scaffolded data synthesis and self-correction,”
     Conference on Software Engineering (ICSE). IEEE, 2025, pp. 885–                  2025. [Online]. Available: https://arxiv.org/abs/2508.03613
     897.                                                                        [25] K. Yang, G. Poesia, J. He, W. Li, K. E. Lauter, S. Chaudhuri, and
 [9] M. Sch”afer, S. Nadi, A. Eghbali, and F. Tip, “An empirical evaluation of        D. Song, “Position: Formal mathematical reasoning—a new frontier
     using large language models for automated unit test generation,” IEEE            in AI,” in Proceedings of the 42nd International Conference on
     Transactions on Software Engineering, vol. 50, no. 1, pp. 85–105, 2024.          Machine Learning, ser. Proceedings of Machine Learning Research,
[10] J. Wang, Y. Huang, C. Chen, Z. Liu, S. Wang, and Q. Wang, “Software              vol. 267. PMLR, 2025, pp. 82 384–82 398. [Online]. Available:
     testing with large language models: Survey, landscape, and vision,” IEEE         https://proceedings.mlr.press/v267/yang25az.html
     Transactions on Software Engineering, vol. 50, no. 4, pp. 911–936, 2024.    [26] N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan,
[11] J. Liu, K. Wang, Y. Chen, X. Peng, Z. Chen, L. Zhang,                            and S. Yao, “Reflexion: Language agents with verbal
     and Y. Lou, “Large language model-based agents for software                      reinforcement learning,” in Advances in Neural Information
     engineering: A survey,” 2024, the previously claimed TOSEM                       Processing Systems, vol. 36, 2023, pp. 8634–8652. [Online].
     publication could not be verified as of 2026-06-30. [Online]. Available:         Available: https://proceedings.neurips.cc/paper files/paper/2023/hash/
     https://arxiv.org/abs/2409.02977                                                 1b44b878bb782e6954cd888628510e90-Abstract-Conference.html
[12] L. Yang, C. Yang, S. Gao, W. Wang, B. Wang, Q. Zhu, X. Chu, J. Zhou,        [27] B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E.
     G. Liang, Q. Wang, and J. Chen, “On the evaluation of large language             Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez et al., “Code
     models in unit test generation,” in Proceedings of the 39th IEEE/ACM             Llama: Open foundation models for code,” 2023. [Online]. Available:
     International Conference on Automated Software Engineering. ACM,                 https://arxiv.org/abs/2308.12950
     2024, pp. 1607–1619.                                                        [28] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou,
[13] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof               M. Marone, C. Akiki, J. Li, J. Chim et al., “StarCoder: May the source
     generation and repair with large language models,” in Proceedings of             be with you!” Transactions on Machine Learning Research, 2023.
     the 31st ACM Joint European Software Engineering Conference and                  [Online]. Available: https://openreview.net/forum?id=KoFOg41haE
     Symposium on the Foundations of Software Engineering. ACM, 2023,            [29] F. Liu, Y. Liu, L. Shi, Z. Yang, L. Zhang, X. Lian, Z. Li, and
     pp. 1229–1241.                                                                   Y. Ma, “Beyond functional correctness: Exploring hallucinations in
[14] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock, P. Derrin,           LLM-generated code,” IEEE Transactions on Software Engineering,
     D. Elkaduwe, K. Engelhardt, R. Kolanski, M. Norrish, T. Sewell,                  vol. 52, no. 3, pp. 1037–1055, 2026.
     H. Tuch, and S. Winwood, “seL4: Formal verification of an OS kernel,”       [30] Y. Tian, W. Yan, Q. Yang, X. Zhao, Q. Chen, W. Wang, Z. Luo, L. Ma,
     in Proceedings of the ACM SIGOPS 22nd Symposium on Operating                     and D. Song, “CodeHalu: Investigating code hallucinations in LLMs via
     Systems Principles. ACM, 2009, pp. 207–220.                                      execution-based verification,” Proceedings of the AAAI Conference on
[15] L. de Moura and N. Bjørner, “Z3: An efficient SMT solver,” in Tools              Artificial Intelligence, vol. 39, no. 24, pp. 25 300–25 308, 2025.
     and Algorithms for the Construction and Analysis of Systems. Springer,      [31] J. Spracklen, R. Wijewickrama, A. H. M. N. Sakib, A. Maiti,
     2008, pp. 337–340.                                                               B. Viswanath, and M. Jadliwala, “We have a package for you! a
[16] C. Loughridge, Q. Sun, S. Ahrenbach, F. Cassano, C. Sun, Y. Sheng,               comprehensive analysis of package hallucinations by code-generating
     A. Mudide, M. R. H. Misu, N. Amin, and M. Tegmark, “DafnyBench: A                LLMs,” in 34th USENIX Security Symposium (USENIX Security 25).
     benchmark for formal software verification,” 2024. [Online]. Available:          USENIX Association, 2025, pp. 3687–3706. [Online]. Available: https:
     https://arxiv.org/abs/2406.08467                                                 //www.usenix.org/conference/usenixsecurity25/presentation/spracklen
[32] A. Eghbali and M. Pradel, “De-hallucinator: Mitigating LLM
     hallucinations in code generation tasks via iterative grounding,” 2024.
     [Online]. Available: https://arxiv.org/abs/2401.01701
[33] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe,
     U. Alon, N. Dziri, S. Prabhumoye, Y. Yang et al., “Self-refine: Iterative
     refinement with self-feedback,” in Advances in Neural Information
     Processing Systems, vol. 36, 2023, pp. 46 534–46 594. [Online].
     Available: https://proceedings.neurips.cc/paper files/paper/2023/hash/
     91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html
[34] X. Chen, M. Lin, N. Sch”arli, and D. Zhou, “Teaching large
     language models to self-debug,” in The Twelfth International
     Conference on Learning Representations, 2024. [Online]. Available:
     https://openreview.net/forum?id=KuPixIqPiq
[35] Z. Liu, X. Bai, K. Chen, X. Chen, X. Li, Y. Xiang, J. Liu, H.-D. Li,
     Y. Wang, L. Nie et al., “A survey on the feedback mechanism of llm-
     based ai agents,” in Proceedings of the Thirty-Fourth International Joint
     Conference on Artificial Intelligence. International Joint Conferences
     on Artificial Intelligence, 2025, pp. 10 582–10 592.
[36] J. Stamper, R. Xiao, and X. Hou, “Enhancing llm-based feedback:
     Insights from intelligent tutoring systems and the learning sciences,”
     in International Conference on Artificial Intelligence in Education.
     Springer, 2024, pp. 32–43.
[37] H. Le, Y. Wang, A. D. Gotmare, S. Savarese, and S. C. H.
     Hoi, “CodeRL: Mastering code generation through pretrained
     models and deep reinforcement learning,” in Advances in
     Neural Information Processing Systems, vol. 35, 2022. [Online].
     Available: https://proceedings.neurips.cc/paper files/paper/2022/hash/
     8636419dea1aa9fbd25fc4248e702da4-Abstract-Conference.html
[38] M. Yuksekgonul, F. Bianchi, J. Boen, S. Liu, P. Lu, Z. Huang,
     C. Guestrin, and J. Zou, “Optimizing generative AI by backpropagating
     language model feedback,” Nature, vol. 639, no. 8055, pp. 609–616,
     2025.
[39] I. Bouzenia, P. Devanbu, and M. Pradel, “Repairagent: An autonomous,
     LLM-based agent for program repair,” in 2025 IEEE/ACM 47th Inter-
     national Conference on Software Engineering (ICSE). IEEE, 2025, pp.
     2188–2200.
[40] H. Xin, D. Guo, Z. Shao, Z. Ren, Q. Zhu, B. Liu, C. Ruan,
     W. Li, and X. Liang, “DeepSeek-Prover: Advancing theorem proving
     in LLMs through large-scale synthetic data,” 2024. [Online]. Available:
     https://arxiv.org/abs/2405.14333
