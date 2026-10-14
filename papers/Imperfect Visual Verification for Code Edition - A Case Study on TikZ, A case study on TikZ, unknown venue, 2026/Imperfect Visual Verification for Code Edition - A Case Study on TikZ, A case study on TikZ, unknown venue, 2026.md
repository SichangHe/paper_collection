                                                             Imperfect Visual Verification for Code Edition :
                                                                          A case study on TikZ
                                                         Charly Reux                                      Mathieu Acher                           Djamel Eddine Khelladi
                                               Univ Rennes, Inria, IRISA, INSA                Univ Rennes, Inria, CNRS, IUF, IRISA              Univ Rennes, Inria, CNRS, IRISA
                                                      Rennes, France                                   Rennes, France                                   Rennes, France
                                                    charly.reux@inria.fr                            mathieu.acher@irisa.fr                      djamel-eddine.khelladi@irisa.fr

                                                                               Clément Quinton                                  Olivier Barais
                                                                            Univ. Lille, CNRS, Inria                      Univ. Rennes, IRISA, Inria
                                                                                 Lille, France                                 Rennes, France
arXiv:2606.15693v1 [cs.SE] 9 Apr 2026




                                                                         clement.quinton@univ-lille.fr                     olivier.barais@irisa.fr

                                        ABSTRACT                                                                     KEYWORDS
                                        LLMs have significantly advanced code generation, enabling the syn-          AI-based code generation, Large Language Models (LLMs), Code
                                        thesis of functional programs. While recent systems achieve strong           customization, Visual intent alignment, Evaluation
                                        performance on many coding benchmarks, tasks involving programs
                                        such as TikZ that generate visual artifacts remain challenging, in
                                        particular on visual code customization. Unlike generation from              1    INTRODUCTION
                                        scratch, customization requires localized, semantics-preserving ed-          Large language models (LLMs) have significantly advanced auto-
                                        its: the model must locate relevant code, modify it according to the         mated code generation, enabling the synthesis of functional pro-
                                        instruction, and preserve the remaining structure and rendering.             grams from natural language descriptions [43]. While recent sys-
                                        Approaches based on post-hoc iterative refinement/correction where a         tems achieve strong performance on many coding benchmarks, a
                                        verifier provides feedback to guide corrections, have shown promise.         class of tasks remains challenging: programs that generate visual
                                        However, in the case of programs with a visual outcome such as               artifacts [23, 41, 45], such as TikZ, SVG, or interactive web visu-
                                        in TikZ, where correctness is harder or likely impossible to formal-         alizations (e.g., D3.js). In these settings, correctness is not solely
                                        ize and evaluate automatically, deterministic verifiers do not exist.        determined by syntactic or functional properties of the code, but
                                        Hence, developers can only rely on imperfect verifiers.                      by high-level visual properties such as geometric structure, spatial
                                            In this paper, we conduct an empirical study to answer: to what ex-      relationships, and layout semantics. However, such properties are
                                        tent can iterative refinement remain effective when the verifier itself is   difficult to infer or verify from code alone.
                                        unreliable? We use TikZ as a focused case study that isolates the core          A particularly challenging instance of this problem is visual code
                                        difficulties of the problem (weak code structure, fine-grained visual        customization, where an existing program must be modified accord-
                                        semantics, and difficult feature localization) in a controlled and chal-     ing to a high-level visual instruction (e.g., "reduce the size of the green
                                        lenging setting. We define visual code customization as an iterative         box on the left and put it parallel to the yellow one"). Unlike genera-
                                        editing problem with an imperfect oracle, and introduce a framework          tion from scratch, this customization requires localized, semantics-
                                        for analyzing such iterative refinements. We conduct a large-scale           preserving edits: the model must identify where in the code a visual
                                        study and evaluate multiple LLM-based and tool-augmented visual              element is defined, modify it according to the instruction, and pre-
                                        verifiers within iterative refinement pipelines, and perform exten-          serve the remaining structure and rendering. This problem arises in
                                        sive manual annotation of refinement trajectories to assess verifier         a wide range of domains, including web interfaces, SVG graphics, sci-
                                        behavior and feedback quality.                                               entific diagrams, games, and 3D modeling. Although prior work on
                                            Our findings show that even imperfect verifiers can determine            multimodal code generation (e.g., image-to-code or text-to-diagram
                                        with moderate accuracy whether visual instructions are applied to            synthesis) has shown promising results [12, 32, 40], recent studies
                                        code, achieving F1-scores up to 0.815. Feedback improves iterative           indicate that LLMs still struggle to reliably perform such targeted
                                        refinement, especially for weaker models, adding 11–20 perfect cus-          visual modifications [31]. Indeed, Reux et al. showed that GPT-4o
                                        tomizations for Qwen3-vl-30b-a3b-Instruct, while stronger models             successfully completed only 26% of TikZ customization tasks.
                                        like Gemini-3 gain fewer improvements (+5) but benefit more from                One promising paradigm for improving generation quality is post-
                                        accurate verification that prevents premature acceptance. Feedback           hoc iterative refinement/correction [13, 29], where an LLM proposes
                                        is effective only when it precisely identifies image issues, provides        candidate solutions and a verifier provides feedback to guide subse-
                                        actionable guidance, addresses all relevant problems, and remains            quent improvements (see fig. 2). This paradigm underlies a growing
                                        grounded in the original instruction.                                        class of systems, including coding agents and Reinforcement Learn-
                                                                                                                     ing with Verifiable Rewards (RLVR), where feedback signals are
                                                                                                                     typically deterministic, boolean, and highly reliable. Examples in-
                                        CCS CONCEPTS                                                                 clude unit test execution for code generation, constraint checking
                                        • Software and its engineering → Automatic programming;                      for structured outputs, or formal proof checkers in theorem-proving
                                        Software prototyping; Visual languages; • Computing method-                  environments. In such settings, refinement is effective because the
                                        ologies → Artificial intelligence.                                           verifier acts as a near-perfect oracle.
Conference’17, July 2017, Washington, DC, USA                         Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais


    However, many real-world generation tasks lack such determin-
istic verification signals, making it challenging to design reliable
refinement loops. When outputs are primarily visual, correctness is
difficult (if not impossible) to formalize and evaluate automatically.
For visual code such as TikZ, HTML/CSS, SVG, or SCAD, compi-
lation or execution only ensures syntactic validity, not semantic
correctness of the rendered image. As a result, refinement must rely
on imperfect verifiers, often implemented as LLM- or VLM-based
evaluators assessing visual similarity or instruction compliance. An
imperfect verifier can be characterized along three dimensions: (i)
false positives, where incorrect outputs are mistakenly accepted,
(ii) false negatives, where correct or partially correct outputs are
rejected, and (iii) feedback quality, defined as the extent to which
feedback is specific, actionable, and aligned with the underlying
error. Such imperfections make the refinement process challenging:                            Figure 1: Excerpt of a TikZ code.
false positives lead to premature termination, while poor feedback
prevents meaningful improvement. This motivates the core research
question of this work: To what extent can iterative refinement remain           • We derive a taxonomy of feedback behaviors and failure
effective when the verifier itself is unreliable?                                 modes of LLM-based visual verifiers through systematic man-
    This paper investigates this question through a focused and con-              ual analysis of refinement trajectories.
trolled case study on TikZ. As detailed in Section 2, TikZ amplifies            • We provide the dataset and a replication package of our ex-
three core software engineering challenges while controlling away                 periments.
confounding factors such as multi-file architectures or framework-
specific tooling: (i) weakly structured and highly compositional code,     2     BACKGROUND AND MOTIVATION
which complicates visual element localization; (ii) high sensitivity       This section introduces the necessary background and further moti-
to small edits, where minor code changes produce subtle but critical       vates our work.
visual differences; and (iii) abstract geometric constructs, which are
                                                                              Problem formalization. We formalize iterative code customization
difficult for current vision-language models to interpret reliably.
                                                                           as the problem of refining a code artifact 𝑐 through a sequence
    To address this problem, we frame visual code customization as an
                                                                           of updates guided by an imperfect verifier. At each iteration, the
iterative editing process under an imperfect oracle, and we introduce
                                                                           generator proposes edits to the code, the verifier provides potentially
a framework for analyzing such iterative refinements. Building on
                                                                           noisy feedback and a score, and the process repeats until a stopping
this framework, we conduct a large-scale empirical study using a
                                                                           criterion or refinement budget is reached. The goal is to produce a
refined version of the VTikZ dataset [31]. In particular, we evalu-
                                                                           final code artifact that best matches the intended visual outcome.
ate multiple LLM-based and tool-augmented visual verifiers within
                                                                              Let 𝑐 0 denote the initial code (a diagram). At iteration 𝑡, the gen-
iterative refinement pipelines, and we perform extensive manual
                                                                           erator produces the next code based on the current code, the verifier
annotation of refinement trajectories to assess verifier behavior and
                                                                           feedback, and the score:
feedback quality. We selected Qwen-vl-30b-a3b and Gemini-3-flash
as the backbone models for our evaluation.                                                                 𝑐𝑡 +1 = 𝐺 (𝑐𝑡 , 𝑓𝑡 ),
    The results yield three key insights. First, imperfect verifiers can   where 𝑓𝑡 = 𝑉 (𝑐𝑡 ) represents the feedback and score provided by the
correctly assess whether visual instructions are applied to code,          verifier.
achieving F1-scores up to 0.815. Second, feedback significantly im-           For a complete refinement loop:
proves refinement for weaker models, yielding gains of +11 to +20                                      𝐺       𝑉       𝐺           𝐺
perfect customizations for Qwen3-vl-30b-a3b-Instruct, whereas stronger                             𝑐 0 → 𝑐 1 → 𝑓1 → . . . → 𝑐𝑛 .
models (Gemini-3) benefit less from feedback and more from accurate        The quality of the final code 𝑐𝑛 is measured with respect to the
classification that prevents premature acceptance. Third, feedback is      intended visual goal 𝑣 ∗ :
effective only when it is actionable: it must precisely identify visual                                 𝑄 (𝑐𝑛 , 𝑣 ∗ ),
issues, provide concrete guidance, cover all relevant problems, and
                                                                           The iterative refinement protocol we formalize in section 4.2 provides
remain grounded in the original instruction.
                                                                           a concrete operational instance of this process, enabling empirical
    To summarize, this work makes the following contributions:
                                                                           evaluation with real LLM generators and verifiers.
                                                                              TikZ as a testbed. The following work focuses on the TikZ lan-
     • We frame the general problem of iterative code customization        guage, a LATEXPackage that allows the creation of graphic elements,
       with imperfect visual verifiers, TikZ being one challenging         mainly for scientific diagrams, though it can also be used for draw-
       instance.                                                           ings and cartoon characters. TikZ programs define visual elements
     • We construct a large-scale dataset of manually annotated            such as shapes, edges, and layouts through code, making them a
       customization within iterative refinement trajectories.             representative example of programs that generate visual artifacts.
     • We provide the first empirical analysis of feedback on LLM             We use TikZ as a focused and controlled case study for iterative
       refinement performance in the customization scenario.               refinement with imperfect verifiers. Unlike broader settings such
Imperfect Visual Verification for Code Edition :
A case study on TikZ                                                                                           Conference’17, July 2017, Washington, DC, USA


                                                                           3     STUDIED VERIFIERS
                                                                           The verifiers we evaluate fall into two categories: (1) basic verifiers,
                                                                           which are variations of multimodal LLM-based verifiers where either
                                                                           the input modality is changed (Text, Visual, or Text+Visual) or the
                                                                           prompting technique is modified (Property); and (2) complex verifiers,
                                                                           which follow a more elaborate code-based approach. All system
                                                                           prompts and settings are available in the Git repository1 Each veri-
                                                                           fier outputs a numeric score and textual feedback. For consistency,
                                                                           we map all scores to the interval [0, 1]. For most verifiers, during
                                                                           prompting, we ask models to produce an integer score from 0 to
              Figure 2: Post-hoc Iterative Refinement.                     100, then divide by 100, as manual testing showed that models are
                                                                           more likely to assign a perfect score when the range is [0, 1] rather
                                                                           than [0, 100]. We also define specific scoring thresholds (0–49, 50–79,
as web development, which involve multi-file structures, modular           80–99, 100), depending on the extent to which the customization is
architectures, and mature visual tooling, TikZ controls away these         applied.
confounding factors while amplifying the challenges central to our
study: the code is weakly structured and lacks modular boundaries,         3.1     Simple LLM-based Verifier
making feature localization difficult; visual outputs require fine-        These verifiers differ from each other in the modality provided to the
grained geometric reasoning; and small code changes can produce            multimodal model: 1) Text, where the initial and customized code
subtle yet critical visual differences. The code is often sufficiently     are given; 2) Visual, where the initial and customized images are fed
opaque that even advanced LLMs fail to interpret what it repre-            to the model; and 3) Text+Visual, where both modalities are provided
sents. For instance, given the code of Figure 1, GPT-4 misinterprets       (images and codes).
it as a “stylized abstract landscape” and Gemini-3 as a seagull, when
it in fact represents a shark. TikZ thus provides an idealized yet         3.2     Property-based Verifier
practically relevant setting that isolates the mechanism of interest
                                                                           This verifier follows a two-step procedure. First, given the instruction
(imperfect visual verification and fine-grained code localization), pro-
                                                                           and the original image, it generates a list of properties that the
viding analytical leverage for studying verifier–generator dynamics.
                                                                           customized image should satisfy. Then, each property is evaluated
Customizing TikZ code from high-level visual instructions requires
                                                                           independently by prompting the same model in a new context to
translating visual-level requests into localized code changes while
                                                                           determine whether the property holds, using a prompt similar to
preserving the overall diagram structure.
                                                                           that of the simple LLM-based verifiers. The final score is the average
   Iterative refinement approach. To address this challenge, we ex-        score of the per-property scores.
plore post-hoc iterative refinement, illustrated in Figure 2. In this
paradigm, a Generator attempts to modify the code according to             3.3     Agentic Vision Verifier
the visual instruction, while a Verifier evaluates whether the in-         This verifier is based on recent work by Google, which leverages
struction has been correctly applied, given the code and the rendered      code execution to ground the LLM’s reasoning2 . The approach gener-
image. The verifier returns a score and textual feedback, which can        ates Python code to manipulate and/or analyze an image in order to
be used to iteratively refine the generated solution.                      extract more fine-grained information. It is analogous to visual pro-
   For example, consider a simple customization such as removing a         gramming and agentic approaches, and serves as a solid code-based
specific feature in the TikZ drawing in Figure 1. A user instruction       baseline.
might ask that the teeth of the shark be removed. The Generator
may mistakenly identify the teeth and instead remove the fins. The         3.4     Segmentation and Tool-based Verifier
verifier can detect this discrepancy and guide the generator toward
the correct edit in subsequent iterations. Alternatively, the verifier     We implemented an approach that leverages the code-generation
may only deteriorate the code customization if incorrect feedback is       capabilities of LLMs to produce Python code. By prompting the model
further returned.                                                          with a precise specification, we ensure that the generated code uses a
                                                                           set of oracle (functions). Each oracle is designed to perform a specific
    Challenges and research gap. While iterative refinement has shown      visual verification on a change between two images (e.g., color, shape,
promising results in domains such as code optimization, readability        position).
improvement, constrained generation, and mathematical reason-
ing [26]. To the best of our knowledge, its effectiveness in visual        3.4.1 Code Generation and Score Computation. The first step of this
customization settings remains unclear. In our case, verifiers are         approach is to prompt the model to generate a verifier function that
inherently imperfect, as visual instructions may admit multiple valid      uses the available oracles. This function is then executed on the
solutions and cannot be evaluated through deterministic tests. As          customized image and returns a score between 0 and 1.
a result, it is uncertain whether LLM-based verifiers can reliably
detect whether a visual instruction has been correctly applied, and        1 https://github.com/CharlyReux/verifier_problem
whether their feedback can effectively guide refinement. Our work          2 https://blog.google/innovation-and-ai/technology/developers-tools/agentic-vision-
fills this gap.                                                            gemini-3-flash/
Conference’17, July 2017, Washington, DC, USA                              Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais


                                                                                 RQ 1.2 Do their scores correlate with human judgments?
                                                                                 RQ2 How does the feedback created and the score assigned by verifiers
                                                                                      relate to performance increases in the customization task?
                                                                                 RQ 2.1 Does the quality of feedback matter?
                                                                                 RQ 2.2 To what extent does the score matter to achieve better
                                                                                         solutions?
                                                                                 RQ3 How does feedback influence the interaction between the gener-
                                                                                      ator and the verifier?
                                                                                 RQ 3.1 Which types of feedback lead to errors, and which guide
                                                                                         the generator toward better solutions?
                                                                                 RQ 3.2 How do generator LLMs interpret and act upon the feedback
             Figure 3: Complete evaluation protocol.                                     they receive?
                                                                                 RQ 3.3 What makes a Generator create a perfect solution?

   For example, to verify that a circle is changed to blue and its width        4.1     Dataset
is doubled, the color and size oracles can be combined using the and            We base our evaluation on the existing VTikZ dataset [31]. We per-
operator.                                                                       formed a manual pass to correct typographical errors, resolve am-
def test_valid_customization() -> bool:                                         biguities, and improve clarity. Every instruction specifies a visual
 return color("circle", "blue")                                                 modification to be applied to an existing TikZ program. The cor-
    and size("circle", (2, 1))                                                  responding original code and rendered image serve as the starting
   Each oracle internally produces a probability, which are com-                point for the iterative refinement process.
bined to compute a final score, computed using probabilistic Boolean
combination.                                                                    4.2     Execution
3.4.2 Automatic Feedback Generation. Each oracle produces auto-                 We apply the iterative refinement to each customization. At every
matic feedback describing the detected discrepancy. When the gener-             iteration, the generated code, rendered image, and verifier’s score
ated verifier code combines multiple oracles using logical operators,           are recorded. This results in a sequence of refinement steps for
feedback is reported only when the corresponding combined proba-                each customization, which are later used for human annotation and
bility exceeds a predefined threshold of 0.9.                                   quantitative analysis.
                                                                                   Formalization of the Iterative Refinement Protocol. For a given
3.4.3 Oracle Catalog. Our oracle catalog includes checks for spatial            customization, we consider a Generator 𝐺 and a Verifier 𝑉 . The Gen-
relations (placement, position, alignment, mirrored), visual attributes         erator 𝐺 exposes two operations: generate and adjust. The generate
(color, size, shape), containment and quantity (within, present, count),        operation takes a code and an instruction as input and produces
rotation (angle), and complex visual properties (visual_property).              a modified code. The adjust operation takes feedback and a score
Each oracle leverages Gemini-2.5 segmentation to identify visual                and returns an updated code. The Verifier 𝑉 takes an instruction
elements from textual descriptions.With this type of method, com-               and a context as input, with the context containing the original
pleteness for an oracle catalog is difficult to achieve, and there is           and customized rendered images and/or their corresponding source
a risk of not covering every possible use case. This limitation is              codes. The verifier returns a score between 0 and 1 along with textual
inherent to the catalog-based approach.                                         feedback.
                                                                                   The process for a pair (𝐺, 𝑉 ) is outlined in Algorithm 1. Given an
4    EVALUATION METHODOLOGY                                                     initial code and instruction, the generator 𝐺 produces a customized
This section presents our evaluation methodology, summarized in                 code 𝑐 ′ (l.3). An iterative refinement loop is then performed (l.5). At
fig. 3. We first refine the VTikZ dataset by correcting and improving           each iteration, a context is constructed (l.7) that includes the initial
the existing instructions. Next, we run the iterative post-hoc refine-          and generated images and codes (𝑟, 𝑟 ′, 𝑐, 𝑐 ′ ). This context is provided
ment loop using selected verifier/generator pairs. At each iteration,           to the verifier 𝑉 (l.8), which outputs feedback and a score (𝑓 , 𝑠). If the
we collect the generated image (produced from the customized code)              score satisfies a predefined threshold (set to 1 in our experiments),
along with the score assigned by the verifier. The resulting images             the process terminates (l.11). Otherwise, 𝐺 uses (𝑓 , 𝑠) to produce
are then evaluated by human annotators, who are provided with                   an updated version of the code (l.13). The loop continues until the
the corresponding instruction and the original image, and asked to              threshold is met or the maximum number of iterations 𝑇 is reached.
rate them on a 1–5 scale. This yields pairs of human and verifier               At each iteration, the current code and image (𝑐 ′, 𝑟 ′ ), together with
scores, which form the basis of our subsequent analysis. We ana-                the score 𝑠, are recorded (l.9) and returned upon termination. This
lyze verifier performance along two dimensions: scoring accuracy                process is executed on all the customizations in the dataset, and
and feedback quality. Based on this distinction, we formulate the               returns code-image-score triplets.
following research questions:
RQ1 To what extent do verifiers correctly assess the application of a           4.3     Manual Annotation
     visual instruction to code?                                                The annotation process is conducted through a web interface in
RQ 1.1 Can they correctly detect whether a customization has been               which annotators evaluate individual refinement steps rather than
        applied or not?                                                         only the final output. Upon connection, each annotator is shown
Imperfect Visual Verification for Code Edition :
A case study on TikZ                                                                                        Conference’17, July 2017, Washington, DC, USA


    Input : Code 𝑐 and instruction 𝑖                                         and Segmentation Tool-Based) paired with both Qwen and Gemini.
    Output : List of (𝑐 ′, 𝑟 ′, 𝑠)                                           Finally, we introduce two additional verifiers: (1) SentenceVerifier, a
1 𝑠 ← 0; 𝜏 ← 1; 𝑇 ← 5;                                                       trivial verifier that always returns the message "The customization
2 𝑟 ← Renderer(c);                                                           is not applied, please apply it.", and (2) PreciseVerifier, a CLIP-based
3 𝑐
      ′ ← G.generate(c,i);                                                   verifier, executed last, which only returns a score measured using the
                                                                             maximum CLIP similarity between the customized image and the
4  𝐷 ← [];
                                                                             set of images annotated as perfect. Both of these new baselines allow
5  for 𝑗 ← 0 to 𝑇 − 1 do
                                                                             us to assess the usefulness of the feedback and the score, which we
 6    𝑟 ′ ← Renderer(c’);
                                                                             interpret in Sections 5.1 and 5.2
 7     context ← (𝑟, 𝑟 ′, 𝑐, 𝑐 ′ );                                             Overall, this results in 20 generator-verifier pairs. Each pair is
 8     (𝑓 , 𝑠) ← V(i,context);                                               evaluated on the 100 TikZ customizations, with three repeated runs
 9    𝐷.append(𝑐 ′, 𝑟 ′, 𝑠);                                                 per customization and up to five refinement iterations per run.
10     if 𝑠 ≥ 𝜏 then
11           return 𝐷                                                        Table 1: Human Annotation Statistics and Inter-Annotator
12     end                                                                   Agreement
13    𝑐 ′ ← G.adjust(f,s);
14 end
                                                                                    #Annotators                                         8
15 return 𝐷                                                                         Total number of distinct items                      3907
          Algorithm 1: Iterative Refinement Execution                               Total number of items                               15345
                                                                                    Total number of distinct annotated items            4289
                                                                                    Total number of annotated items                     17100
an image randomly sampled from all code-image-score triplets. The
                                                                                    Avg. annotations per Item                           1.11
corresponding original image and customization instruction are
also displayed. The annotator is then asked to rate how well the                    Avg. distinct #items per annotator                  536
instruction was applied on an ordinal scale from 1 to 5.                            Avg. #items per annotator                           2138
                                                                                    Krippendorff’s 𝛼                                    0.898
      • 1 - Not applied at all
      • 2 - Slightly applied
      • 3 - Moderately applied
      • 4 - Mostly applied                                                   5   EVALUATION RESULTS
      • 5 - Perfectly applied                                                This section now presents our observed results answering our RQs.
This gives us, for each step, triplets of image, verifier score, and human
score.                                                                       5.1 RQ1: Assessment of Visual Instruction
   Eight annotators participated in the manual annotation process.               Application on Code
Although the dataset contains many generated images, several cor-            For this evaluation, we first focus on the ability of verifiers to iden-
respond to identical or very similar code modifications produced             tify perfect customizations. We therefore cast the task as a binary
by the LLMs. As a result, the annotations cover 3907 distinct items,         classification problem, where items rated 5 (“Perfectly applied”) by
which correspond to a larger total of 15345 generated instances in           human annotators are treated as positive instances, and all others as
the dataset. This deduplication significantly reduced the amount of          negative. We then evaluate how well verifier scores can predict these
manual annotation required while still providing coverage of a larger        positives using F1-score. Figure 4 presents the precision-recall (PR)
set of generated outputs. More details about the human-annotated             curves for all evaluated generator-verifier pairs. Overall, simple LLM-
data are provided in Table 1. We measure inter-annotator agreement           based verifiers (Text, Text+Visual, Text-only) as well as AgenticVision
using Krippendorff’s 𝛼, obtaining a value of 0.898, indicating strong        tend to assign high scores to most candidate customizations. As a
agreement and supporting the reliability of the annotations.                 result, their PR curves are concentrated in the high recall region,
                                                                             with no operating point (except near 0) achieving both high precision
4.4     Evaluation Configurations                                            and low recall. This indicates a strong bias toward accepting outputs,
Because we evaluate verification methods rather than the models              yielding consistently high recall but limited precision.
themselves, we conduct experiments using two models: Qwen3-vl-                  Introducing more structured verification partially mitigates this
30b-a3b-instruct and Gemini-3-flash-preview, with the Gemini model           behavior. The VisualPropertyVerifier reduces the frequency of uni-
configured with minimal thinking effort. These models were chosen            formly maximal scores, leading to a more balanced score distribution.
for their strong coding and multimodal capabilities.Each model is            However, this comes at the cost of overall effectiveness, with both pre-
used both as a generator and as a verifier. Unless specified otherwise,      cision and recall decreasing relative to simple LLM-based approaches.
all models are run with a temperature of 0.5.                                A similar trade-off is observed for the Segmentation and Tool-based
    We first evaluate the four basic verifiers (Simple and Property)         approach, which performs similarly to VisualPropertyVerifier but
using Gemini-3 as the verifier model, paired with both Qwen and              yields overall underwhelming results.
Gemini as generators. We then repeat the same experiment using                  To further quantify these trends, the best achievable F1-score
Qwen as both the verifier and generator model. In addition to these          for each approach is computed over all decision thresholds. The
configurations, we evaluate the two complex verifiers (Agentic Vision        corresponding precision and recall values are reported in Table 2 and
Conference’17, July 2017, Washington, DC, USA                                                          Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais




                                                                           Figure 4: PR curves for each verifier.

                                         Table 2: Precision/Recall/F1 Scores for the best thresholds for llm verifiers

 Verifier    Generator                      Text                                         Text+Visual                                 Visual                                  Visual Property
 Model                      Threshold   Precision    Recall          F1   Threshold     Precision Recall        F1    Threshold   Precision Recall         F1    Threshold    Precision Recall       F1
 Gem.        Gem.               1.000       0.683        0.967    0.801       0.980           0.712   0.952   0.815       1.000      0.762    0.822      0.791       0.667        0.645   0.970    0.775
 Gem.        Qwen               1.000       0.533        0.937    0.680       1.000           0.691   0.857   0.765       1.000      0.674    0.919      0.778       0.875        0.484   0.715    0.578
 Qwen        Qwen               1.000       0.302        0.950   0.458        1.000           0.277   0.897   0.423       1.000      0.316    0.783      0.450       0.880        0.348   0.531    0.421



Table 3: Precision/Recall/F1 Scores for the best thresholds for                                                 Table 4: Kendall correlations for LLM and Fixed verifiers
fixed verifiers
                                                                                                               Verifier Model     Generator       Text     Text+Visual       Visual   Visual Property
 Generator              Agentic Vision                          Segmentation-Tool Verifier                     Gem.               Gem.           0.172            0.448      0.456                0.287
              Threshold Precision Recall            F1     Threshold Precision Recall            F1
                                                                                                               Gem.               Qwen           0.718            0.765      0.709                0.530
 Gem.               1.000       0.712   0.949   0.814            0.000     0.601      1.000   0.751
 Qwen               0.980       0.519   0.943   0.669            0.920     0.609      0.568   0.587            Qwen               Qwen           0.620            0.616       0.487               0.364

                                                                                                               Generator     Agentic Vision        Precise Score      Segmentation-Tool Verifier

Table 3. For readability, we abbreviate model names as follows: Gem.                                           Gem.                      0.441               0.534                                0.003
                                                                                                               Qwen                      0.718               0.373                                0.347
(Gemini-3-flash-preview) and Qwen (Qwen3-vl-30b-a3b-instruct).
For simple LLM-based Verifiers, optimal F1-scores are consistently
obtained at thresholds close to 1, confirming the tendency of these
models to assign high scores, leading to high recall but relatively
low precision.
                                                                                                              generators, relying solely on visual input (Visual) leads to better
   Across all approaches, performance improves when paired with
                                                                                                              alignment, indicating that textual signals may introduce noise once
stronger generator models, a trend observed for both LLM-based
                                                                                                              baseline output quality is high.
verifiers (Table 2) and fixed approaches (Table 3). Notably, AgenticVi-
sion achieves the highest overall F1-score when paired with Gemini
(0.814), but not with Qwen (0.669).                                                                              RQ1: Among the evaluated approaches, only Gemini-3-Flash
   Table 4 reports Kendall correlation coefficients between verifier                                          is reliable at detecting whether a customization has been applied,
scores and all human judgments. In contrast to F1-scores, an oppo-                                            achieving F1-scores up to 0.815. However, it tends to overestimate
site trend can be observed: correlation is higher when the generator                                          correctness, resulting in high recall but lower precision. Correlation
model is weaker, suggesting that stronger generators produce out-                                             with human judgments is moderate when paired with Gemini as the
puts that are harder to discriminate. Input modality also plays a                                             generator (0.456), but substantially higher with Qwen (0.765).
key role. When paired with weaker generators, combining textual                                                  More complex verification strategies—such as code generation
and visual inputs (Text+Visual) yields the strongest alignment with                                           (AgenticVision, Segmentation-Tool-based) or decomposition into
human judgments (correlation up to 0.765) However, with stronger
Imperfect Visual Verification for Code Edition :
A case study on TikZ                                                                                     Conference’17, July 2017, Washington, DC, USA




multiple verification steps (VisualProperty) - do not improve per-         that, at higher performance levels, accurate scoring and early stop-
formance and can even degrade both accuracy and alignment with             ping become more critical than exploratory feedback.
human judgments.                                                              Overall, feedback is beneficial for improving performance in the
   Overall, for TikZ code, LLM-based verifiers (particularly Gemini-       TikZ customization task, especially for weaker models. However, for
3-Flash) can be used to assess whether a visual instruction has been       stronger models, the precision and reliability of the verifier play a
applied. However, this comes with a significant rate of false positives,   more critical role than the feedback.
reflecting a systematic bias toward high recall at the expense of
precision.
                                                                           5.3 RQ3: Qualitative Feedback analysis
                                                                           To better understand LLM behavior during iterative refinement,
5.2     RQ2: Overall Performances                                          we conduct a manual analysis of verifier-generated feedback. We
Figure 5 reports the step-wise performance of all approaches, mea-         focus on feedback produced by TextVisualVerifier, PropertyVerifier,
sured as the number of customizations that achieve a perfect score         and AgenticVisionVerifier, as these approaches generate open-ended,
according to human annotators.                                             visually grounded, natural language feedback. In contrast, other
   For Qwen as the generator, performance improves when paired             approaches either constrain feedback to predefined properties (Visu-
with Gemini as the verifier, with gains of up to +16 and +17 of perfect    alPropertyVerifier) or rely on fixed oracle responses (Segmentation-
customizations. The largest gains occur when Gemini has access to          Tool-based approach).
the generated code (TextVerifier, TextVisualVerifier), although gains         We construct a characterization of feedback in customization
remain noticeable with visual-only input (VisualVerifier). Compared        trajectory steps. We consider three dimensions:
to the baseline where Qwen acts as both generator and verifier, using
Gemini leads to consistent gains, although they are more limited in            • (i) the quality of the initial customization (perfect vs. non-
the visual-only setting (+11). Pairing Qwen with the SentenceVerifier,           perfect)
which provides only coarse binary feedback (“customization not                 • (ii) the correctness of the feedback (correct vs. erroneous with
applied”), yields improvements comparable to being paired with                   respect to the instruction or image)
itself, suggesting that minimal feedback can be useful for weaker              • (iii) the quality of the subsequent customization (Worse, Un-
models.                                                                          changed, or Better)
   Improvements are more limited when Gemini is used as the gen-           For each output of a trajectory step, we analyze the feedback in
erator. When paired with itself, the VisualVerifier yields the best re-    terms of aspects (i.e., what the feedback contains) and interpreta-
sults, but only marginally (+2). Unlike Qwen, performance decreases        tions (i.e., how it is acted upon by the generator). The analysis is
when using the SentenceVerifier. This difference can be explained          conducted over 138 randomly sampled tuples of the form ⟨initial
by the higher initial performance of Gemini (around 75 correct cus-        customization, feedback, refined customization⟩. Sampling was con-
tomizations versus 20–24 for Qwen), which reduces the need for             tinued until no new feedback patterns or trajectory behaviors
additional exploration and increases the risk of degrading already         were observed, suggesting that the main trajectory patterns are ad-
correct outputs during refinement.                                         equately represented. This enables us to identify recurring feedback
   More complex verification strategies, such as AgenticVision and         patterns associated with improvement, stagnation, or degradation
the Segmentation-Tool-based approach, yield limited gains across           in customization quality.
both generators. Their performance remains comparable to, or slightly         We summarize this study in fig. 6, which depicts a decision tree
below, that of simpler LLM-based verifiers, indicating that added ar-      over customization trajectories. Starting from an initial customiza-
chitectural complexity does not translate into improved refinement.        tion, trajectories branch on the observed quality (Perfect vs. Non-
   The PreciseVerifier yields the largest performance improvements,        Perfect) and the correctness of the feedback, leading to subsequent
reaching up to 85 perfect customizations at step 4. By leveraging          customization steps. At each decision node, we report the frequency
similarity scores with known perfect outputs, it effectively halts         of transitions, and at the leaves, we detail the generators’ interpre-
successful trajectories early while allowing further exploration on        tations and resulting actions (e.g., rightly guided, partially applied,
unresolved cases. However, Qwen benefits less from this mechanism,         neglected, or wrongly guided).
with only marginal improvements (+2).                                         For incorrect feedback, the dominant failure modes are hallucina-
                                                                           tions on the visual content or instruction and misunderstandings of
   RQ2: Feedback can improve refinement performance, but its im-           the instruction.
pact strongly depends on the strength of the generator. For weaker            For correct feedback, we identify several aspects, specifically, it
models such as Qwen, informative feedback from stronger verifiers          may be imprecise, non-guiding, incomplete, or forgetful, which
(e.g., Gemini-based) leads to substantial gains (33–36 perfect cus-        can lead to partial, incorrect, or missing application in the next
tomizations), while coarse or indirect signals (e.g., PreciseVerifier,     customization.
SentenceVerifier) result in lower performance (28–30).                        We define these aspects as follows:
   For stronger models such as Gemini, the role of feedback differs:
coarse feedback degrades performance, whereas more informative                 • Precision: The feedback localizes and specifies issues clearly,
verifiers (TextVisualVerifier, VisualVerifier) yield modest improve-             rather than describing them in vague/abstract terms
ments. The best results are obtained with PreciseVerifier, indicating          • Guidance: The feedback goes beyond identifying errors and
                                                                                 provides actionable directions for correction.
Conference’17, July 2017, Washington, DC, USA                            Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais




                                     Figure 5: Total number of perfect customizations per step per verifier.




               Figure 6: Observed Customization Trajectories, and subsequent interpretation/actions by the generator.


     • Completeness: The feedback captures all necessary issues                  Finally, we select the behaviors that led to perfect customiza-
       required to correctly refine the customization.                        tion. For these we have observed most/all of the aspect described
     • Forgetfulness: The feedback "forgets" about the initial in-            above: the feedback is leverage-able and states what must be modi-
       struction, and only comments on the flaws of the diagram.              fied (guiding), it explicitly describes the what is right and what is
                                                                              wrong w.r.t the instruction (not forgetful) and it provides detailed
                                                                              information (Precise), and finally, it states all the points which are
   Independent of correctness, feedback may be interpreted and                to be fixed (Complete).
acted upon in different ways by the generator as it may be under-
stood or not, and either applied, partly applied, or ignored. We also
observe recurring behaviors such as invisible changes, stubborn-
ness, or neglect where the generator fails to modify the code despite            RQ3: Feedback that leads to errors is either (i) incorrect, due to
receiving feedback. This may stem either from an inability to opera-          hallucinations or misunderstandings, or (ii) correct but ineffec-
tionalize the feedback or from overconfidence in the current solution.        tive, due to being imprecise, non-guiding or forgetful. Generator
   Invisible changes are generally reformatting, adding comments,             LLMs exhibit diverse interpretation behaviors, ranging from correct
or shifting the entire picture. Together with neglect, these are the          understanding and application to failure modes such as misunder-
main reasons why the majority of the customizations happening                 standing, partial application, neglect, and stubbornness. Given
exhibit the same quality as the previous customizations, and are              that the generator LLM can operationalize the feedback, our study
mainly due to Qwen’s inability to correctly apply the feedback.
Imperfect Visual Verification for Code Edition :
A case study on TikZ                                                                                          Conference’17, July 2017, Washington, DC, USA


                                                                               6.2    Recommendations for imperfect visual
shows that perfect customization is achieved only when the feed-                      verifiers
back is guiding, not forgetful, Precise, and Complete. Overall,
the feedback influences the interactions in multiple ways, either              Although our empirical claims are carefully restricted to TikZ, the
negatively or positively, depending on its quality, and also on how            case study suggests broader recommendations for iterative refine-
LLM can interpret it.                                                          ment in domains where correctness cannot be checked through
                                                                               deterministic tests.
                                                                                  Separate decision quality from feedback quality. Two distinct ca-
                                                                               pabilities must be considered: (i) the ability to correctly accept or
                                                                               reject outputs, and (ii) the ability to provide guidance that improves
6     RECOMMENDATIONS                                                          them. A verifier can be a good scorer but a poor guide, or vice
We revisit the central question of this paper: To what extent can              versa. These dimensions should be evaluated independently.
iterative refinement remain effective when the verifier itself is un-             Evaluate verifiers within the refinement loop. Standalone verifica-
reliable? The TikZ case study suggests a positive but conditional              tion is insufficient. Our results show that the same verifier can
answer. Iterative refinement remains effective under imperfect                 help or hinder depending on the generator and the interaction
verification, but only when the verifier is reliable enough to                 dynamics. Evaluation should therefore consider final task success,
avoid premature acceptance and provides actionable feedback.                   stopping behavior, and the evolution of solutions across refinement
Building on this insight, we derive two sets of recommendations : (i)          steps.
practical guidelines for TikZ customization, grounded in our empiri-              Prioritize reducing false positives and improving actionability. False
cal results (Section 5), and (ii) broader implications for refinement          positives are harmful, as they prematurely terminate refinement. At
pipelines relying on imperfect visual verifiers.                               the same time, useful feedback is not merely correct: it must be
                                                                               precise, guiding, complete, and explicitly tied to the instruc-
                                                                               tion being executed. These properties constitute a more realistic
6.1     Recommendations for TikZ customization                                 target for imperfect visual verifiers than score agreement alone.
Prefer simple multimodal LLM-based verifiers as a strong baseline. As
                                                                               7     LIMITATIONS AND THREATS TO VALIDITY
shown in RQ1 (section 5.1), Gemini-based verifiers consistently
provide the strongest overall assessment results, whereas more                 Case study. Our study focuses on a single language, which limits
elaborate verification strategies based on decomposition, code gener-          generalization to other domains. While TikZ customization does
ation, or segmentation do not systematically improve either detection          not capture the scale and complexity of broader multimodal coding
quality or alignment with human judgments. Combined with the                   tasks (e.g., web development), it provides, as discussed in section 2, a
results of RQ2 and RQ3, this suggests that the advantage of multi-             focused and controlled setting that isolates the core difficulties of the
modal verifiers in TikZ is not only that they can assess whether a             problem while combining code generation, multimodal reasoning,
customization has been applied, but also that they provide feedback            and instruction understanding. Nonetheless, future replication on
that is easier for the generator to exploit during refinement.                 other languages and settings remains necessary.
   Do not treat these verifiers as reliable or near-perfect oracles. Despite       Evaluated models. We evaluate only two models, namely Qwen3-
strong recall, RQ1 highlights a persistent bias toward false positives.        VL-30B-A3B-Instruct and Gemini-3-Flash-Preview. This choice is
In an iterative loop, such errors are particularly harmful because             primarily driven by the high annotation cost: even with two models,
they terminate refinement too early. Stopping policies should                  the study required 8 annotators and 4,289 annotations. The selected
therefore be conservative, and verifier acceptance treated with                models represent different paradigms (instruct vs. thinking), which
caution.                                                                       may limit direct comparability. Nevertheless, both are suitable for
   Adapt the verifier’s role to the generator’s strength. RQ2 shows            the customization task and provide complementary baselines. Im-
that weaker generators benefit primarily from informative                      portantly, our focus is on imperfect verifiers rather than on the
feedback, whereas stronger generators benefit from accurate                    generative models themselves.
scoring and early stopping. In practice, the verifier should act as a              Limitation to 5 steps. We restrict evaluation trajectories to five
critic for weaker models, and a more selective stopping mechanism              steps. This represents a trade-off between capturing iterative refine-
for stronger ones.                                                             ment dynamics (e.g., classification quality, trajectory patterns, and
   Explicitly optimize for feedback quality. RQ3 shows that failures           feedback quality) and maintaining a manageable annotation effort.
stem not only from incorrect feedback, but also from correct yet inef-         Exploring longer trajectories could provide additional insights, but
fective feedback. Imprecise, non-actionable, incomplete, or forgetful          is left for future work.
feedback often leads to stagnation, partial application, or incorrect              Constrained feedback format. The system prompts we used en-
edits. For TikZ customization, effective feedback must localize                force a specific feedback format. This limits the diversity of possible
the problem, specify required changes, remain grounded in                      feedback. However, as shown in section 5.3, it is sufficient to assess
the original instruction, and cover all relevant corrections.                  the quality of LLMs’ feedback in an iterative refinement setting.
   Assess both requested change and preservation. Focusing solely
on whether the requested modification is present is not sufficient.            8     RELATED WORK
Successful customization must preserve the semantics and                       Visual code customization sits at the intersection of iterative re-
structure of the original artifact. Verifiers should therefore jointly         finement, critic models, visual question answering, and visual code
assess the applied change and the absence of unintended side-effects.          generation. While each area has seen substantial progress, none
Conference’17, July 2017, Washington, DC, USA                              Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais


directly addresses iterative refinement under an imperfect visual                  Refinement and Repair capability evaluation. Several works evalu-
verifier - where feedback may yield false positives, false negatives,           ate the refinement capabilities of LLMs, either by measuring their
or lack the actionability needed to guide meaningful improvement.               ability to improve their own outputs or by assessing the quality of
   Iterative refinement. It was initially introduced as a test-time com-        generated feedback. These studies typically focus on domains with
pute strategy to improve LLM outputs, notably with Self-Refine [26],            deterministic or easily verifiable answers, such as mathematics, algo-
and has since been extended in approaches such as CRITIC [8]. Prior             rithms, or multiple-choice reasoning. Notably, Huang et al. analyze
work has applied iterative refinement to code generation [5, 26, 33,            self-correction in LLMs and highlight both its potential and its limi-
42, 47] and, more recently, to multimodal tasks [2, 18, 20, 42]. How-           tations. Benchmarks such as RefineBench [19] evaluate refinement
ever, these studies do not explicitly consider iterative refinement for         using domain-specific checklists and consider both guided (exter-
structured diagram customization at inference time. Only Xu et al.              nal feedback) and self-refinement settings. Other works, including
and Li et al. explore both multimodal reasoning and code genera-                CriticBench [24], RealCritic [38], and CriticEval [16], focus on eval-
tion in the context of chart creation, but target full code generation          uating the quality of critics, again in domains where verification
from existing data, rather than customization from existing code.               can be reduced to clear, often binary outcomes. Closely related to
In code generation, Post-Hoc iterative refinement typically relies              editing, SR-Eval [44] evaluates the ability of LLMs to apply stepwise
on strong, programmatic feedback signals, similarly to RLVR-based               requirements in software engineering tasks, but considers cumula-
systems. For instance, Self-Debug [5] and Reflexion [33] leverage               tive sequences of different edits rather than iterative refinement from
multi-turn unit test execution to verify intermediate outputs, while            a single instruction. Similarly, Olausson et al. study self-repair in full
Self-Edit [46] applies a single-turn execution-based feedback strat-            code generation settings. Beyond deterministic domains, Sun et al.
egy. However, these approaches leverage deterministic verification,             investigate refinement in text summarization, where correctness is
which is unavailable when correctness depends on properties of                  less well-defined, but limit their analysis to single-turn prompting
rendered diagrams. Agents also exhibit similar behavior to iterative            strategies. In the multimodal domain, VF-EVAL [34] evaluates the
refinement [1], by using external tools and verification loops. In              ability of models to generate feedback on AI-generated videos, but
contrast to our context, the verifications are usually more reliable.           does not consider iterative refinement and is not related to code.
Other works investigate refinement strategies during training, us-                 To the best of our knowledge, no existing framework captures the
ing feedback loops to improve model parameters [4, 17, 22, 25], In              challenges of iterative refinement under imperfect visual verifiers.
contrast, our work focuses exclusively on refinement as a Post-Hoc              We provide the first novel empirical analysis of multi-step refinement
strategy, applied at inference time. Critic models are LLMs fine-tuned          in visual code customization, characterizing verifier behavior with
to evaluate or verify outputs [14, 15, 18, 21, 22, 28, 30, 39]. They are        regard to the quality of its classification and feedback.
often applied in single-turn generate-critique-refine pipelines, some-
times extending to multimodal domains (e.g., VIS-Shepherd, ReLook,              9     CONCLUSION
Volcano, IE-Critic-R1). While these critics demonstrate task-specific           In this paper, we explored the applicability and effectiveness of post-
evaluation, they operate in a single-turn fashion and do not explore            hoc iterative refinement with imperfect verifiers, using TikZ code
multi-step refinement loops.                                                    customization as a case study. We introduced an evaluation frame-
   Visual Question Answering and UI critique. The task of Visual                work to analyze LLM-based verifiers within an iterative refinement
Question Answering (VQA) is related to verification in our setting,             pipeline. Building on the VTikZ dataset, which we refined, we evalu-
as verification can be framed as asking: “Is the instruction <instruc-          ated 20 generator–verifier pairs on 100 TikZ customization tasks, for
tion> correctly applied to this image?”. However, unlike standard               up to five refinement steps, resulting in a total of 15,345 customized
VQA, our setting requires fine-grained spatial reasoning, instruc-              code instances. We conducted a large-scale manual evaluation of
tion grounding, and contextual comparison between an initial and                these customizations, enabling us to analyze both output quality and
an edited image. Visual Programming (VP) approaches [7, 35, 37]                 the impact of feedback in iterative refinement. In particular, we ex-
decompose tasks into sequences of tool calls. While conceptually                amined verifier performance in (i) assessing whether customization
similar, these methods are primarily designed for natural images                instructions are correctly applied to code, and (ii) understanding
and generic visual primitives, limiting their applicability to diagram-         how feedback and scoring influence subsequent refinements.
level edits. For completeness, we also evaluate VP-like verifiers(see              Our results show that verifiers are generally capable of deter-
sections 3.3 and 3.4). The task of UI critique, which consists of gener-        mining whether instructions are applied, but exhibit a bias toward
ating design comments from a UI screenshot and design guidelines,               classifying solutions as valid, leading to a high rate of false positives.
is also related. Duan et al. propose a pipeline that generates feed-            Feedback improves performance in post-hoc iterative refinement;
back and corresponding bounding boxes, and iteratively refines both             however, the reliability of scoring becomes more critical for stronger
using a validation model. This approach shares similarities with                models. We further derived a study of feedback by systematically
the segmentation-tool-based verifier (section 3.4), but operates on             analyzing 138 customization trajectories of ⟨initial customization,
different inputs.                                                               feedback, refined customization⟩, extracting fine-grained feedback
   Visual Code Generation. The intersection of code generation and              aspects and their interpretation by LLMs. Based on these findings,
visual inputs has been explored primarily through image-to-code                 we provide actionable recommendations not only for TikZ but also
approaches [3, 42, 48], and to a lesser extent in editing scenarios             for visual verification more broadly. These insights can support the
[9, 11]. However, these approaches focus on single-turn generation,             design of more effective and reliable verifiers for further research in
often in a single pass, without any feedback mechanism. Only Xu                 TikZ or other similar contexts.
et al. incorporate iterative refinement, but exclusively in the context            Finally, our results suggest several directions for future work. The
of image-to-code generation rather than editing.                                annotated trajectories collected in this study could be used to train a
Imperfect Visual Verification for Code Edition :
A case study on TikZ                                                                                                               Conference’17, July 2017, Washington, DC, USA


learned scorer for TikZ customization, reducing manual annotation                            [18] Seongyun Lee, Sue Hyun Park, Yongrae Jo, and Minjoon Seo. 2024. Volcano:
costs and potentially improving the verifier signal available during                              Mitigating Multimodal Hallucination through Self-Feedback Guided Revision. In
                                                                                                  Proceedings of the 2024 Conference of the North American Chapter of the Association
refinement. A second direction is to replicate the study on other                                 for Computational Linguistics: Human Language Technologies (Volume 1: Long
visual languages, such as SVG or P5.js, to determine which findings                               Papers), Kevin Duh, Helena Gomez, and Steven Bethard (Eds.). Association for
                                                                                                  Computational Linguistics, Mexico City, Mexico, 391–404. doi:10.18653/v1/2024.
transfer beyond TikZ. A third direction is to investigate imperfect                               naacl-long.23
visual verification in richer environments, including web interfaces,                        [19] Young-Jun Lee, Seungone Kim, Byung-Kwan Lee, Minkyeong Moon, Yechan
games, and 3D scenes, where the artifact to be evaluated is no longer                             Hwang, Jong Myoung Kim, Graham Neubig, Sean Welleck, and Ho-Jin Choi. 2025.
                                                                                                  RefineBench: Evaluating Refinement Capability of Language Models via Checklists.
a single rendered image but a more complex interactive environment.                               doi:10.48550/arXiv.2511.22173 arXiv:2511.22173 [cs].
                                                                                             [20] Bingxuan Li, Yiwei Wang, Jiuxiang Gu, Kai-Wei Chang, and Nanyun Peng. 2025.
                                                                                                  METAL: A Multi-Agent Framework for Chart Generation with Test-Time Scaling.
                                                                                                  In Proceedings of the 63rd Annual Meeting of the Association for Computational
ACKNOWLEDGEMENTS.                                                                                 Linguistics (Volume 1: Long Papers), Wanxiang Che, Joyce Nabende, Ekaterina
                                                                                                  Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Computational
This work is supported by the Inria Défi LLM4Code.                                                Linguistics, Vienna, Austria, 30054–30069. doi:10.18653/v1/2025.acl-long.1452
                                                                                             [21] Junlong Li, Shichao Sun, Weizhe Yuan, Run-Ze Fan, Hai Zhao, and Pengfei Liu.
                                                                                                  2023. Generative Judge for Evaluating Alignment. doi:10.48550/arXiv.2310.05470
REFERENCES                                                                                        arXiv:2310.05470 [cs].
 [1] Mohamad Abou Ali and Fadi Dornaika. 2025. Agentic AI: A Comprehensive Survey            [22] Yuhang Li, Chenchen Zhang, Ruilin Lv, Ao Liu, Ken Deng, Yuanxing Zhang, Jiaheng
     of Architectures, Applications, and Future Directions. Artificial Intelligence Review        Liu, Wiggin Zhou, and Bo Zhou. 2025. ReLook: Vision-Grounded RL with a
     59, 1 (Nov. 2025), 11. doi:10.1007/s10462-025-11422-4 arXiv:2510.25445 [cs].                 Multimodal LLM Critic for Agentic Web Coding. doi:10.48550/arXiv.2510.11498
 [2] Ruhana Azam, Tamer Abuelsaad, Aditya Vempaty, and Ashish Jagmohan. 2024.                     arXiv:2510.11498 [cs].
     Multimodal Auto Validation For Self-Refinement in Web Agents. doi:10.48550/             [23] Kevin Qinghong Lin, Yuhao Zheng, Hangyu Ran, Dantong Zhu, Dongxing Mao,
     arXiv.2410.00689 arXiv:2410.00689 [cs].                                                      Linjie Li, Philip Torr, and Alex Jinpeng Wang. 2025. VCode: a Multimodal Coding
 [3] Jonas Belouadi, Simone Paolo Ponzetto, and Steffen Eger. 2024. DeTikZify:                    Benchmark with SVG as Symbolic Visual Representation. doi:10.48550/arXiv.2511.
     Synthesizing Graphics Programs for Scientific Figures and Sketches with TikZ.                02778 arXiv:2511.02778 [cs].
     doi:10.48550/arXiv.2405.15306 arXiv:2405.15306 [cs].                                    [24] Zicheng Lin, Zhibin Gou, Tian Liang, Ruilin Luo, Haowei Liu, and Yujiu Yang. 2024.
 [4] Angelica Chen, Jérémy Scheurer, Tomasz Korbak, Jon Ander Campos, Jun Shern                   CriticBench: Benchmarking LLMs for Critique-Correct Reasoning. doi:10.48550/
     Chan, Samuel R. Bowman, Kyunghyun Cho, and Ethan Perez. 2024. Improving                      arXiv.2402.14809 arXiv:2402.14809 [cs].
     Code Generation by Training with Natural Language Feedback. doi:10.48550/arXiv.         [25] Jiaqi Liu, Kaiwen Xiong, Peng Xia, Yiyang Zhou, Haonian Ji, Lu Feng, Siwei Han,
     2303.16749 arXiv:2303.16749 [cs].                                                            Mingyu Ding, and Huaxiu Yao. 2025. Agent0-VL: Exploring Self-Evolving Agent
 [5] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2023. Teach-                    for Tool-Integrated Vision-Language Reasoning. doi:10.48550/arXiv.2511.19900
     ing Large Language Models to Self-Debug. doi:10.48550/arXiv.2304.05128                       arXiv:2511.19900 [cs].
     arXiv:2304.05128 [cs].                                                                  [26] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
 [6] Peitong Duan, Chin-Yi Cheng, Bjoern Hartmann, and Yang Li. 2025. Visual Prompt-              Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank
     ing with Iterative Refinement for Design Critique Generation. doi:10.48550/arXiv.            Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir
     2412.16829 arXiv:2412.16829 [cs].                                                            Yazdanbakhsh, and Peter Clark. 2023. Self-Refine: Iterative Refinement with
 [7] Jiaxin Ge, Sanjay Subramanian, Baifeng Shi, Roei Herzig, and Trevor Darrell. 2024.           Self-Feedback. Advances in Neural Information Processing Systems 36 (Dec.
     Recursive Visual Programming. doi:10.48550/arXiv.2312.02249 arXiv:2312.02249                 2023), 46534–46594. https://proceedings.neurips.cc/paper_files/paper/2023/hash/
     [cs].                                                                                        91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html
 [8] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan,                [27] Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and Ar-
     and Weizhu Chen. 2024. CRITIC: Large Language Models Can Self-Correct with                   mando Solar-Lezama. 2024. Is Self-Repair a Silver Bullet for Code Generation?
     Tool-Interactive Critiquing. doi:10.48550/arXiv.2305.11738 arXiv:2305.11738 [cs].            doi:10.48550/arXiv.2306.09896 arXiv:2306.09896 [cs].
 [9] Yucheng Han, Chi Zhang, Xin Chen, Xu Yang, Zhibin Wang, Gang Yu, Bin Fu, and            [28] Bo Pan, Yixiao Fu, Ke Wang, Junyu Lu, Lunke Pan, Ziyang Qian, Yuhan Chen,
     Hanwang Zhang. 2023. ChartLlama: A Multimodal LLM for Chart Understanding                    Guoliang Wang, Yitao Zhou, Li Zheng, Yinghao Tang, Zhen Wen, Yuchen Wu,
     and Generation. doi:10.48550/arXiv.2311.16483 arXiv:2311.16483 [cs].                         Junhua Lu, Biao Zhu, Minfeng Zhu, Bo Zhang, and Wei Chen. 2025. VIS-Shepherd:
[10] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu,                  Constructing Critic for LLM-based Data Visualization Generation. doi:10.48550/
     Xinying Song, and Denny Zhou. 2024. Large Language Models Cannot Self-Correct                arXiv.2506.13326 arXiv:2506.13326 [cs].
     Reasoning Yet. doi:10.48550/arXiv.2310.01798 arXiv:2310.01798 [cs].                     [29] Liangming Pan, Michael Saxon, Wenda Xu, Deepak Nathani, Xinyi Wang, and
[11] Lingjie Jiang, Shaohan Huang, Xun Wu, Yixia Li, Dongdong Zhang, and Furu Wei.                William Yang Wang. 2024. Automatically Correcting Large Language Models:
     2025. VisCodex: Unified Multimodal Code Generation via Merging Vision and                    Surveying the Landscape of Diverse Automated Correction Strategies. Transactions
     Coding Models. doi:10.48550/arXiv.2508.09945 arXiv:2508.09945 [cs].                          of the Association for Computational Linguistics 12 (2024), 484–506. doi:10.1162/
[12] Yilei Jiang, Yaozhi Zheng, Yuxuan Wan, Jiaming Han, Qunzhong Wang, Michael R.                tacl_a_00660
     Lyu, and Xiangyu Yue. 2025. ScreenCoder: Advancing Visual-to-Code Generation            [30] Bowen Qu, Shangkun Sun, Xiaoyu Liang, and Wei Gao. 2025. IE-Critic-R1: Ad-
     for Front-End Automation via Modular Multimodal Agents. doi:10.48550/arXiv.                  vancing the Explanatory Measurement of Text-Driven Image Editing for Human
     2507.22827 arXiv:2507.22827 [cs].                                                            Perception Alignment. doi:10.48550/arXiv.2511.18055 arXiv:2511.18055 [cs].
[13] Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, and Rui Zhang. 2024. When Can            [31] Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Olivier Barais, and Clément
     LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction               Quinton. 2025. LLM Code Customization with Visual Results: A Benchmark on
     of LLMs. doi:10.1162/tacl_a_00713/125177 arXiv:2406.01297 [cs].                              TikZ. doi:10.48550/arXiv.2505.04670 arXiv:2505.04670 [cs].
[14] Pei Ke, Bosi Wen, Andrew Feng, Xiao Liu, Xuanyu Lei, Jiale Cheng, Shengyuan             [32] Juan A. Rodriguez, Abhay Puri, Shubham Agarwal, Issam H. Laradji, Pau Ro-
     Wang, Aohan Zeng, Yuxiao Dong, Hongning Wang, Jie Tang, and Minlie Huang.                    driguez, Sai Rajeswar, David Vazquez, Christopher Pal, and Marco Pedersoli. 2025.
     2024. CritiqueLLM: Towards an Informative Critique Generation Model for Evalua-              StarVector: Generating Scalable Vector Graphics Code from Images and Text.
     tion of Large Language Model Generation. In Proceedings of the 62nd Annual Meet-             doi:10.48550/arXiv.2312.11556 arXiv:2312.11556 [cs].
     ing of the Association for Computational Linguistics (Volume 1: Long Papers), Lun-Wei   [33] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik
     Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational                  Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Verbal
     Linguistics, Bangkok, Thailand, 13034–13054. doi:10.18653/v1/2024.acl-long.704               Reinforcement Learning. doi:10.48550/arXiv.2303.11366 arXiv:2303.11366 [cs].
[15] Seungone Kim, Juyoung Suk, Shayne Longpre, Bill Yuchen Lin, Jamin Shin, Sean            [34] Tingyu Song, Tongyan Hu, Guo Gan, and Yilun Zhao. 2025. VF-Eval: Evaluating
     Welleck, Graham Neubig, Moontae Lee, Kyungjae Lee, and Minjoon Seo. 2024.                    Multimodal LLMs for Generating Feedback on AIGC Videos. doi:10.48550/arXiv.
     Prometheus 2: An Open Source Language Model Specialized in Evaluating Other                  2505.23693 arXiv:2505.23693 [cs] version: 1.
     Language Models. doi:10.48550/arXiv.2405.01535 arXiv:2405.01535 [cs].                   [35] Aleksandar Stanić, Sergi Caelles, and Michael Tschannen. 2024. Towards Truly
[16] Tian Lan, Wenwei Zhang, Chen Xu, Heyan Huang, Dahua Lin, Kai Chen, and                       Zero-shot Compositional Visual Reasoning with LLMs as Programmers. doi:10.
     Xian-ling Mao. 2024. CriticEval: Evaluating Large Language Model as Critic.                  48550/arXiv.2401.01974 arXiv:2401.01974 [cs].
     doi:10.48550/arXiv.2402.13764 arXiv:2402.13764 [cs].                                    [36] Shichao Sun, Ruifeng Yuan, Ziqiang Cao, Wenjie Li, and Pengfei Liu. 2024. Prompt
[17] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H.                Chaining or Stepwise Prompt? Refinement in Text Summarization. In Findings
     Hoi. 2022. CodeRL: Mastering Code Generation through Pretrained Models and                   of the Association for Computational Linguistics: ACL 2024, Lun-Wei Ku, Andre
     Deep Reinforcement Learning. doi:10.48550/arXiv.2207.01780 arXiv:2207.01780                  Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics,
     [cs].                                                                                        Bangkok, Thailand, 7551–7558. doi:10.18653/v1/2024.findings-acl.449
Conference’17, July 2017, Washington, DC, USA                                             Charly Reux, Mathieu Acher, Djamel Eddine Khelladi, Clément Quinton, and Olivier Barais


[37] Dídac Surís, Sachit Menon, and Carl Vondrick. 2023. ViperGPT: Visual Inference via        [43] Frank F. Xu, Uri Alon, Graham Neubig, and Vincent J. Hellendoorn. 2022. A
     Python Execution for Reasoning. doi:10.48550/arXiv.2303.08128 arXiv:2303.08128                 Systematic Evaluation of Large Language Models of Code. doi:10.48550/arXiv.2202.
     [cs].                                                                                          13169 arXiv:2202.13169 [cs].
[38] Zhengyang Tang, Ziniu Li, Zhenyang Xiao, Tian Ding, Ruoyu Sun, Benyou Wang,               [44] Zexun Zhan, Shuzheng Gao, Ruida Hu, and Cuiyun Gao. 2026. SR-Eval: Evaluating
     Dayiheng Liu, Fei Huang, Tianyu Liu, Bowen Yu, and Junyang Lin. 2025. RealCritic:              LLMs on Code Generation under Stepwise Requirement Refinement. doi:10.48550/
     Towards Effectiveness-Driven Evaluation of Language Model Critiques. doi:10.                   arXiv.2509.18808 arXiv:2509.18808 [cs].
     48550/arXiv.2501.14492 arXiv:2501.14492 [cs].                                             [45] Chenchen Zhang, Yuhang Li, Can Xu, Jiaheng Liu, Ao Liu, Changzhi Zhou, Ken
[39] Tianlu Wang, Ping Yu, Xiaoqing Ellen Tan, Sean O’Brien, Ramakanth Pasunuru,                    Deng, Dengpeng Wu, Guanhua Huang, Kejiao Li, Qi Yi, Ruibin Xiong, Shihui Hu,
     Jane Dwivedi-Yu, Olga Golovneva, Luke Zettlemoyer, Maryam Fazel-Zarandi,                       Yue Zhang, Yuhao Jiang, Zenan Xu, Yuanxing Zhang, Wiggin Zhou, Chayse Zhou,
     and Asli Celikyilmaz. 2023. Shepherd: A Critic for Language Model Generation.                  and Fengzong Lian. 2025. ArtifactsBench: Bridging the Visual-Interactive Gap in
     doi:10.48550/arXiv.2308.04592 arXiv:2308.04592 [cs].                                           LLM Code Generation Evaluation. doi:10.48550/arXiv.2507.04952 arXiv:2507.04952
[40] Jingxuan Wei, Cheng Tan, Qi Chen, Gaowei Wu, Siyuan Li, Zhangyang Gao,                         [cs].
     Linzhuang Sun, Bihui Yu, and Ruifeng Guo. 2024. From Words to Structured                  [46] Kechi Zhang, Zhuo Li, Jia Li, Ge Li, and Zhi Jin. 2023. Self-Edit: Fault-Aware Code
     Visuals: A Benchmark and Framework for Text-to-Diagram Generation and Editing.                 Editor for Code Generation. doi:10.48550/arXiv.2305.04087 arXiv:2305.04087 [cs].
     doi:10.48550/arXiv.2411.11916 arXiv:2411.11916 [cs].                                      [47] Kexun Zhang, Danqing Wang, Jingtao Xia, William Yang Wang, and Lei
[41] Chengyue Wu, Yixiao Ge, Qiushan Guo, Jiahao Wang, Zhixuan Liang, Zeyu Lu,                      Li. 2023. ALGO: Synthesizing Algorithmic Programs with Generated Ora-
     Ying Shan, and Ping Luo. 2024. Plot2Code: A Comprehensive Benchmark for                        cle Verifiers. Advances in Neural Information Processing Systems 36 (Dec.
     Evaluating Multi-modal Large Language Models in Code Generation from Scientific                2023), 54769–54784. https://proceedings.neurips.cc/paper_files/paper/2023/hash/
     Plots. doi:10.48550/arXiv.2405.07990 arXiv:2405.07990 [cs] version: 1.                         abe1eb21ceb046209c96a0f5e7544ccc-Abstract-Conference.html
[42] Chengzhi Xu, Yuyang Wang, Lai Wei, Lichao Sun, and Weiran Huang. 2025. Im-                [48] Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister, and Jinsung
     proved Iterative Refinement for Chart-to-Code Generation via Structured Instruc-               Yoon. 2026. PaperBanana: Automating Academic Illustration for AI Scientists.
     tion. doi:10.48550/arXiv.2506.14837 arXiv:2506.14837 [cs].                                     doi:10.48550/arXiv.2601.23265 arXiv:2601.23265 [cs].
