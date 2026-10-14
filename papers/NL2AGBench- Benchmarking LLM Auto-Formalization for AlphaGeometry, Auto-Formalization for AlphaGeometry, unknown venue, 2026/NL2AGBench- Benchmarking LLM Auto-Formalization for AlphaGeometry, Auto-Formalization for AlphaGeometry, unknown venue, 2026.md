                                                          NL2AGBench: Benchmarking LLM
                                                         Auto-Formalization for AlphaGeometry
                                                      Samuel Xiao                        Judy Song                  Rory Hu                     Ziliang Zong
                                              Valley Christian High School         Vandegrift High School        Groton School         Computer Science Department
                                                      Fremont, CA                       Austin, TX               Cupertino, CA            Texas State University



                                            Abstract—Recent advances in large language models (LLMs)         geometry problems often contain implicit spatial relationships,
                                         have demonstrated strong performance in natural language            diagram-dependent information, and complex geometric con-
                                         understanding and mathematical reasoning. However, their            straints that must be preserved exactly during translation. Even
arXiv:2608.28481v1 [cs.CL] 28 Aug 2026




                                         ability to translate informal mathematical problem statements
                                         into formal representations remains underexplored. This lim-        small translation errors can fundamentally alter a problem’s
                                         itation is particularly important for neuro-symbolic geometry       meaning and prevent downstream reasoning systems from
                                         systems such as AlphaGeometry, whose theorem-proving en-            producing valid proofs.
                                         gine requires inputs written in a specialized domain-specific          AlphaGeometry represents one of the most successful
                                         language (DSL). Although AlphaGeometry achieved near-IMO            neuro-symbolic systems for Olympiad-level geometry reason-
                                         gold-medalist performance on Olympiad geometry problems,
                                         the manual conversion of natural-language problems into its         ing [1]. By combining neural-guided auxiliary construction
                                         formal syntax remains a significant usability bottleneck. To        generation with symbolic deductive reasoning, AlphaGeom-
                                         address this gap, we introduce Natural Language to Alpha-           etry solved 25 of 30 historical International Mathematical
                                         Geometry Benchmark (NL2AGBench), which aims to evalu-               Olympiad (IMO) geometry problems and demonstrated per-
                                         ate the ability of LLMs to translate English geometry prob-         formance comparable to elite human competitors. However,
                                         lems into AlphaGeometry-compatible formal representations.
                                         NL2AGBench evaluates translation quality using execution-           AlphaGeometry requires all problems to be expressed in
                                         based verification within the AlphaGeometry framework rather        a specialized domain-specific language (DSL). As a result,
                                         than relying solely on textual similarity metrics. We evaluate      geometry problems written in standard mathematical English
                                         ten state-of-the-art open- and closed-source LLMs spanning          must first be manually translated into formal syntax before
                                         multiple parameter scales and analyze their performance in          theorem proving can begin. This translation requirement re-
                                         terms of executable translation accuracy, syntactic correctness,
                                         and error characteristics. Our experiments reveal a substantial     mains a major barrier to accessibility, scalability, and practical
                                         performance gap between frontier closed-source models and           deployment. Figure 1 illustrates this challenge. On the left is
                                         open-source alternatives. While leading closed-source models        a geometry problem written in natural mathematical language,
                                         achieve executable translation rates exceeding 80%, even the        similar to the format used in Olympiad competitions and
                                         largest open-source models struggle to consistently preserve        textbooks. On the right is the corresponding AlphaGeometry
                                         geometric constraints and produce valid formalizations. To better
                                         understand these failures, we introduce an error taxonomy           DSL representation required by the theorem prover. While the
                                         that categorizes AlphaGeometry execution failures into syntax       English description is concise and intuitive for human readers,
                                         and logic errors. We further investigate mitigation strategies,     the formal representation must explicitly encode geometric
                                         including few-shot prompting, fine-tuning, and human-guided         objects, constraints, incidences, and proof targets using a strict
                                         hinting, demonstrating measurable improvements across multiple      symbolic syntax. Minor omissions or incorrect constructions
                                         model families.
                                            Index Terms—AlphaGeometry, benchmark, translation, neuro-        can fundamentally change the problem semantics and prevent
                                         symbolic learning, prompt engineering.                              the theorem prover from generating a valid proof.
                                                                                                                The challenge of converting natural-language geometry
                                                              I. I NTRODUCTION                               problems into formal representations is closely related to
                                            Recent progress in large language models (LLMs) has              semantic parsing and mathematical auto-formalization. Prior
                                         significantly advanced natural language understanding, code         work has explored translating informal mathematics into
                                         generation, and mathematical reasoning. Despite these ad-           proof-assistant languages such as Lean, Isabelle, and Meta-
                                         vances, translating informal mathematical descriptions into         math, while recent studies have investigated the use of LLMs
                                         machine-verifiable formal representations remains a challeng-       to assist formal theorem proving [2], [3]. However, existing
                                         ing problem. This process, commonly referred to as auto-            benchmarks primarily evaluate proof generation, mathematical
                                         formalization, is a critical prerequisite for many theorem-         reasoning, or general auto-formalization. To the best of our
                                         proving and neuro-symbolic reasoning systems because formal         knowledge, no benchmark specifically evaluates the translation
                                         solvers require precise symbolic inputs rather than natural-        of natural-language geometry problems into AlphaGeometry-
                                         language descriptions.                                              compatible formal representations.
                                            Geometry theorem proving presents a particularly chal-              To address this gap, we introduce NL2AGBench, a bench-
                                         lenging auto-formalization setting. Unlike algebraic problems,      mark designed to evaluate the ability of LLMs to trans-
Fig. 1. Translation gap between natural-language geometry problems and AlphaGeometry’s formal DSL. While AlphaGeometry has demonstrated strong
theorem-proving capabilities, the manual formalization step remains a major barrier to usability and large-scale deployment.



late English geometry problems into AlphaGeometry’s DSL.                     ures into syntax and logic errors. This taxonomy provides
NL2AGBench consists of geometry problems paired with                         practical insights into common failure modes and facili-
verified formal representations and evaluates model out-                     tates future research on geometry auto-formalization.
puts through direct execution within AlphaGeometry. This                   • We investigate multiple translation-improvement strate-
execution-based evaluation allows us to assess not only syntac-              gies, including few-shot prompting, fine-tuning, and
tic correctness but also whether generated translations preserve             human-guided hinting. Our experiments demonstrate that
the geometric semantics required for theorem proving.                        targeted prompting and guidance can significantly im-
   Using NL2AGBench, we evaluate a diverse collection of                     prove pass rates for Llama3.1:70b by 23%, GPT-4o-
open- and closed-source LLMs and analyze their ability to                    mini:8b by 8%, and Qwen3:235b by 33.3%.
bridge the gap between natural-language problem descriptions
and formal geometric reasoning systems. Our results reveal                                     II. R ELATED W ORK
a substantial performance disparity between frontier closed-            A. AlphaGeometry and its Applications
source models and open-source alternatives, highlighting the               AlphaGeometry is a neuro-symbolic AI system designed to
difficulty of geometry-specific auto-formalization. We further          solve Euclidean geometry proof problems [1]. It combines a
characterize common failure modes through a systematic error            symbolic deduction engine with a neural model that proposes
taxonomy and analyze mitigation strategies including few-shot           auxiliary constructions when direct deduction is insufficient.
prompting, fine-tuning, and human-guided hints.                         This builds on earlier symbolic geometry theorem-proving
   Our main contributions are summarized as follows:                    methods, such as automated geometry proof systems [4].
  • We introduce NL2AGBench, a benchmark for eval-                      Beyond pure mathematics, AlphaGeometry has potential appli-
    uating the translation of natural-language geome-                   cations in scientific reasoning, synthetic-data generation, and
    try problems into AlphaGeometry-compatible domain-                  operating systems verification. Other recent systems, such as
    specific language representations. The benchmark pro-               HAGeo and TongGeometry, have also explored improved aux-
    vides a standardized framework for studying geome-                  iliary construction strategies and guided search for Olympiad
    try auto-formalization and LLM-assisted theorem-proving             geometry [5], [6]. However, these systems still depended on
    pipelines.                                                          formal or semi-formal problem representations. Newclid ad-
  • We conduct a comprehensive evaluation of ten state-of-              dressed this usability issue by proposing a more user-friendly
    the-art LLMs, including both open-source and closed-                alternative to AlphaGeometry [7]. These works showed that
    source models spanning multiple parameter scales.                   while geometry theorem proving has advanced significantly,
    Our results reveal a substantial performance gap be-                translating natural-language problems into solver-compatible
    tween frontier proprietary models and currently available           syntax is still a key bottleneck.
    open-source alternatives. The largest open-source model
    achieves a score of under 46% with an optimized prompt-             B. Challenges in AlphaGeometry Translation
    ing technique, while closed-source large frontier models              The task of converting English geometry problems into
    have reached 85% and above.                                         AlphaGeometry syntax is closely related to auto-formalization.
  • We introduce a systematic error taxonomy for Alpha-                 Wu et al. showed that large language models can perform
    Geometry translation failures, categorizing execution fail-         part of this translation process for mathematical statements
[8], while Jiang et al. demonstrated that informal proof                angle bisectors, orthocenters, circumcenters, midpoints,
sketches can help guide formal theorem proving [9]. Bench-              reflections, and perpendicular constructions.
marks such as miniF2F have also evaluated IMO Olympiad               • Execution efficiency: Problems requiring excessive run-
mathematical reasoning in formal systems such as Lean,                  time or computational resources within AlphaGeometry
Isabelle, and Metamath [10]. More recent work on formal                 are excluded to ensure scalable evaluation across LLMs.
mathematical reasoning, such as research related to LeanDojo,        NL2AGBench contains problems (see sample problems 1
ProofBridge, and AlphaProof, further showed the growing            and 2 below) spanning varying levels of syntactic complexity
importance of connecting natural-language reasoning with           and geometric reasoning difficulty while maintaining practical
formal theorem-proving environments [11]–[13]. However,            evaluation costs. A visual diagram of 8 sample NL2AGBench
most of these works focused on general mathematical for-           problems is shown in Figure 2.
malization or proof generation. In contrast, we focus specifi-
                                                                   Problem 1:
cally on translating natural-language geometry problems into       Let ABC be a triangle with circumcenter O. Let H be
AlphaGeometry-compatible syntax, where readability, object         the midpoint of BC, and let lines OH and AB
definitions, givens, and target conclusions must all be correct.   intersect at D. Through C, draw the line
                                                                   perpendicular to CO, and through A, draw the line
                                                                   perpendicular to AO; let these two lines intersect
C. LLM Benchmarks and Prompting                                    at E. Prove that points A, O, E, and D lie on a
                                                                   circle.
   Existing LLM benchmarks evaluated mathematical reason-
ing or language translation, but not mathematical transla-         Translation:
tion. The MATH dataset and GSM8K benchmark evaluated               a b c = triangle a b c; o = circle o a b c; h =
                                                                   midpoint h c b; d = on_line d o h, on_line d a b; e
general mathematical problem solving, while OlympiadBench          = on_tline e c c o, on_tline e a a o
evaluated Olympiad-level scientific and mathematical rea-          ? cyclic a o e d
soning [14]–[16]. Model-specific work such as DeepSeek-
Math showed that training on mathematical data can improve         Problem 2:
competition-math performance, but stronger mathematical rea-       Let ABC be a triangle inscribed in a circle with
soning did not necessarily guarantee correct formal translation    center O. Let M be the midpoint of side BA. Let N be
                                                                   a point on line OM extended that also lies on the
[17]. For translation prompting, chain-of-thought prompting        circle with center O, so N is the second
and self-consistency prompting have shown that LLMs can            intersection of line OM with the circumscribed
improve reasoning performance when encouraged to generate          circle of triangle ABC. Draw line NC. Prove that the
                                                                   angle ACN is equal to the angle NCB, that is, prove
intermediate steps or sample multiple reasoning paths [18],        that CN bisects the angle ACB.
[19]. For AlphaGeometry translation, similar prompting strate-
gies can assist models with improving their translation. We ad-    Translation:
                                                                   a b c = triangle a b c; m = midpoint m b a; o =
dress a specific gap in mathematical reasoning and translation     circle o a b c; n = on_line n o m, on_circle n o a ?
by evaluating LLMs on natural-language-to-AlphaGeometry            eqangle c a c n c n c b
translation rather than only mathematical problem solving.
                                                                     3) Evaluation Objective: Given an English geometry prob-
                     III. NL2AGB ENCH                              lem (PN L ), the goal is to generate a corresponding Alpha-
                                                                   Geometry formalization (PAG ):
A. Benchmark Construction
   1) Sourcing Dataset: NL2AGBench is constructed from                                   fθ (PN L ) → PAG
geometry problems originally formalized for AlphaGeometry.
We begin with the Java Geometry Expert (JGEX) repository,            where fθ denotes an LLM.
an open-source geometry theorem-proving framework contain-           The generated translation must satisfy two requirements:
ing hundreds of Olympiad-style geometry problems. Among              • Syntactic correctness: the DSL must conform to Alpha-
these problems, the AlphaGeometry project manually formal-              Geometry grammar.
ized 231 instances into its domain-specific language. These          • Semantic correctness: the translation must preserve all
examples form the foundation of our benchmark because they              geometric objects, constraints, and target conclusions
enable direct evaluation of automatic translation from English          contained in the original problem statement.
geometry statements into AlphaGeometry-compatible syntax.            A translation is considered successful if and only if it can
Unlike general mathematical reasoning datasets, every prob-        be executed by AlphaGeometry without error and produces a
lem in NL2AGBench contains verified formal specifications          valid problem specification.
that can be executed directly by AlphaGeometry.
   2) Benchmark Selection: From the 231 formalized prob-           B. Prompting Strategy
lems, we select 48 representative problems to construct              To provide models with sufficient knowledge of Alpha-
NL2AGBench. Problems were chosen based on two criteria:            Geometry syntax, we employ a prompting framework, which
   • Translation diversity: Problems cover a broad range of ge-    consists of:
     ometric concepts including circles, cyclic quadrilaterals,      • official AlphaGeometry syntax definitions
Fig. 2. Sample NL2AGBench problems. These selected problems encompass a wide range of geometry question types, while still being optimized for runtime
and usability efficiency.



  • handwritten rules describing clause usage and formatting                   This evaluation framework directly measures whether a
    constraints                                                             generated translation can function as an effective interface be-
  • the target geometry problem                                             tween natural-language geometry problems and AlphaGeom-
  The LLM is instructed to generate a single two-line output                etry’s symbolic reasoning engine.
containing the problem identifier and its corresponding DSL                                    IV. E RROR C LASSIFICATION
representation. No explanations or intermediate reasoning are
                                                                               A central challenge in evaluating AlphaGeometry formal-
requested. This setup mirrors a realistic auto-formalization sce-
                                                                            ization is the ambiguity of execution failures. AlphaGeometry
nario in which the model must map natural-language geometry
                                                                            frequently reports low-level runtime exceptions that provide
descriptions directly into executable symbolic representations.
                                                                            limited information regarding the underlying translation mis-
Using the files above, translate the following                              take. To better understand model behavior, we introduce an
geometry problem into the AlphaGeometry domain
language format. Keep the problem title exactly as:
                                                                            execution-based error taxonomy that maps AlphaGeometry
{problem_id}. Provide ONLY ONE translation. Do not                          failures to interpretable categories.
include explanations, commentary, or alternatives
---just the two-line problem definition (title line                         A. Syntax Errors
+ definition line).
                                                                               Syntax errors occur when a generated translation violates
                                                                            the structural requirements of the AlphaGeometry domain-
C. Translation Verification                                                 specific language. These errors prevent the symbolic engine
   Evaluating translation quality using string similarity alone             from parsing or constructing the geometric configuration.
is insufficient because multiple formalizations may be syn-                 Below are the three cases for syntax errors.
tactically different while remaining semantically equivalent.                  1) Assertion Error: The AssertionErrors occur
Therefore, NL2AGBench employs an execution-based eval-                      when a construction receives an invalid number of arguments.
uation protocol. For each generated translation, we execute                 Such errors typically arise when the model correctly identifies
the resulting DSL specification using AlphaGeometry. The                    the intended construction but fails to provide all required geo-
execution outcome is categorized into one of three classes:                 metric entities. Examples include incomplete reflection opera-
                                                                            tions, malformed circle constructions, or incorrectly specified
  • Successful Translation: The specification is accepted by
                                                                            auxiliary points. These errors indicate partial understanding of
    AlphaGeometry and executes successfully.
                                                                            the problem but incomplete knowledge of DSL syntax.
  • Syntax Error: The specification violates DSL grammar
    or construction rules.                                                  Example erroneous translation:
                                                                            a b = segment; c = midpoint b a; d = reflect c b; e
  • Logic Error: The specification is syntactically valid                   = on_circle c a, r_triangle e c d; f = on_tline b a
    but semantically inconsistent with the intended geometry                b, on_line a e; g = on_line b f, on_line d e ? cong
    problem.                                                                e g g f
   In this example, AssertionError is thrown at                      •   self-referential constructions
d = reflect c b     because the reflect construction requires        •   invalid proof predicates
three points: the point that will be reflected and another two        • incorrect parameter counts
points to define the line being reflected upon. Since only two        These errors indicate that the model generated syntactically
points are provided, the computation results in an error.          plausible structures that violate underlying geometric construc-
   2) Key Error: A KeyError occurs when clauses, delim-            tion rules. For example, the ValueError is triggered at
iters, or construction arguments are used improperly, similar      d = on_circum a b c, on_circum a o d. Although point d
to AssertionError. Common causes include:                          is being defined, it is also used in the second on_circum clause.
   • misuse of special characters (e.g. semicolon, whitespace,     Because d has not yet been constrained, it cannot be used to
      proof-operator)                                              determine its own position, resulting in a ValueError.
   • invalid output-variable references                            Example erroneous translation:
   • malformed construction declarations                           a b c = triangle; o = circumcenter a b c; d =
                                                                   on_circum a b c, on_circum a o d; p = on_circum a
   • hallucinated DSL clauses
                                                                   b c, on_circum a o p; f = foot p a d; g = foot
                                                                   p a b; h = foot p b c; e = foot p c d; i = on_line
Example erroneous translation:
                                                                   f g, on_line h e ? cyclic p g i h
b c d a = quadrangle; o = circumcenter b c d a; q
= midpoint c b; s = midpoint a d; j = midpoint s q;
m = reflect o j; i = on_line a d, on_line b c ? perp                 Another case is when the final proof clause has an incorrect
s m b c                                                            amount of parameters.
                                                                   Example erroneous translation:
   AlphaGeometry’s DSL allows points to be repeated for            a b c = r_triangle; d = foot c a b ? eqangle c a c d
readability. For instance, a = midpoint a b c defines a new        a d a b b c b d
point a that is in the middle of segment bc. The point
                                                                      The eqangle clause only takes 8 arguments, the first four
a can be repeated to the right of the clause to show that
                                                                   defining the first angle and the last four defining the second
it is an output point. In the above example, KeyError
                                                                   angle. In this example, ValueError is thrown because there
is thrown at o = circumcenter b c d a. The circumcen-
                                                                   are 12 arguments passed into eqangle.
ter clause normally takes three points to define the circle
in which the circumcenter point is to be constructed. The          Example erroneous translation:
                                                                   a b d = triangle; c = on_tline c a b, on_tline c b a
correct usage including repetition of the output point is          ; d1 = on_line b c, angle_bisector d b c; e =
o = circumcenter o b c d. There is a maximum of four               midpoint a d1; f = on_line a c, on_line b d1 ? para
points including the repeat to the right of the clause. However,   c e b d1
if the output point does not match (o does not match b on the         Here, ValueError is thrown at the definition of point
other side in the original example) when the maximum of four       c: c = on_tline c a b, on_tline c b a. The construction
points is used, a KeyError is thrown.                              on_tline requires three argument points to establish a point
   A second source of KeyError is incorrect use of special         of tangency between a circle and a line.
characters, particularly semicolons and question marks. In
the example below, a KeyError occurs before the proof              B. Logic Errors
statement foot a d e; ? eqangle because semicolons may                Logic errors occur when the generated translation is syntac-
separate clauses but cannot immediately precede a proof            tically valid but semantically incorrect. Typical causes include:
clause marked by ?. Similar parsing issues, such as trailing          • omitted constraints
whitespaces, can also trigger KeyError.                               • incorrect geometric relations

Example erroneous translation:                                        • incorrect target predicates
a b = segment; c = midpoint b a; d = on_circle c a;                   • misinterpretation of geometric terminology
e = on_line a b, on_tline d c d; f =
foot a d e; ? eqangle f a d a d a b
                                                                      Logic errors are particularly important because they reveal
                                                                   limitations in mathematical understanding, rather than defi-
  The final observed case in which a KeyError occurs is            ciencies in syntax generation.
when clauses are misplaced.                                        Example erroneous translation:
                                                                   a b c = r_triangle a b c ? perp a b b c
Example erroneous translation:
a b c = triangle; d = foot b a c; e = foot a b c;
f = foot b d e ?
                                                                      In this example, r_triangle creates a right triangle with
eqangle a b a d d b d e = eqangle c b c f f b f d                  right angle CAB. Therefore, lines CA and AB are perpendicular,
                                                                   not AB and BC. Using the modified ag4masses [20] system,
   Here, an extra eqangle is hallucinated into the proof clause,   these logic errors are detected immediately and cause the
causing a KeyError.                                                terminal to freeze. In contrast, the official system continues
   3) Value Error: ValueErrors occur when geometric                attempting to solve the problem before eventually freezing
objects are defined inconsistently or recursively. Examples        as well. Therefore, we terminate any run that exceeds five
include:                                                           minutes without producing new output and classify it as a
   • circular point definitions                                    logic error.
I0529 12:26:07.656355 140703903308672 graph.py:498]                # Example 1
test_problem                                                       Let ABC be a triangle with AB < AC and circumcenter
I0529 12:26:07.656621 140703903308672 graph.py:499]                O. The angle bisector of angle BAC meets BC at D.
a b c = r_triangle a b c ? perp a b b c                            The line through D perpendicular to BC meets AO at
*terminal freezes beyond this point                                X. Y is the midpoint of AD. Prove that B, C, X, Y
                                                                   are concyclic.

                                                                   a b c = triangle; o = circumcenter a b c; d =
C. Significance of the Taxonomy                                    on_line b c, angle_bisector b a c; x = on_line a o,
                                                                   on_tline d b c; y = midpoint a d ? cyclic b c x y
   Our taxonomy provides a standardized framework for an-
alyzing failures in AlphaGeometry auto-formalization. Rather       # Example 2
than reporting only overall success rates, the taxonomy enables    Let ABC be a triangle with AB=AC and M the midpoint
                                                                   of BC. P is a point with PB<PC and PA parallel to BC.
fine-grained diagnosis of whether model failures arise from        X,Y are on lines PB,PC with B on PX, C on PY, and
syntax generation, geometric interpretation, or semantic rea-      angle PXM = angle PYM. Prove APXY is cyclic.
soning. This distinction is critical for not only understanding
                                                                   a b c = iso_triangle; m = midpoint b c; p = on_pline
the errors designing future mitigation strategies and improving    a b c; x = on_line p b; y = on_line p c, eqangle3 y
LLM-based mathematical formalization systems.                      p m x m p ? cyclic a p x y

D. Baseline Model Performance Results                                 Figure 3 shows that few-shot prompting improves transla-
                                                                   tion accuracy across nearly all models. Among closed-source
                                                                   models, Gemini-3.1 achieves the best performance, increasing
                            TABLE I
               M ODEL P ERFORMANCE (Z ERO -S HOT )
                                                                   from 62.5% accuracy in the zero-shot setting to 83.3% with
                                                                   few-shot prompting, a gain of about 21 percentage points.
       Model         Correct   Model                 Correct       Grok-3 improves from 52.1% to 62.5% (+10 points), while
       Closed Source           Open Source                         Sonnet-4.6 rises from 37.5% to 52.1% (+14 points). GPT-5.4
       GPT-5.4       75.00%    qwen3:235B            12.50%
       Gemini 3.1    62.50%    Llama3.1:70B            0%          starts at a relatively high 75.0% accuracy and reaches 79.2%
       Grok-3        52.08%    Llama3.2:3B             0%          with few-shot examples (+4 points). In contrast, GPT-4o:8B
       Sonnet 4.6    37.50%    Mistral:7B              0%          remains slightly improved, improving only from 4.2% to 8.3%.
       gpt-4o:8B      4.17%    nemotron-3-nano:4B      0%
                                                                      The largest relative gains are observed among open-source
                                                                   models. Qwen3:235B improves from 12.5% to 45.8% accu-
       V. I MPROVING T RANSLATION P ERFORMANCE                     racy, a gain of around 33 percentage points and more than
                                                                   a threefold increase. Llama3.1:70B rises from 0% to 23%,
   Our baseline evaluation reveals a substantial performance       while Mistral:7B, Nemotron-3 Nano:4B, and Llama3.2:3B
gap between frontier closed-source models and open-source          fail to produce any correct translations in either setting. The
alternatives. The hatched data in Figure 3 illustrates the per-    improvement is particularly pronounced for syntax-related
formance of these models in zero-shot circumstances and serve      errors, suggesting that a substantial fraction of translation
as a reference point. While large proprietary models frequently    failures arise from unfamiliarity with AlphaGeometry’s DSL
generate executable AlphaGeometry translations, open-source        rather than a complete lack of geometric understanding.
models often fail due to syntax violations, omitted constraints,      Overall, few-shot prompting is the most effective and scal-
or incorrect geometric interpretations. To better understand       able approach, consistently reducing error rates and improving
how translation performance can be improved, we investigate        accuracy across models without requiring retraining. However,
three mitigation strategies: few-shot prompting, human-guided      a substantial performance gap remained between the strongest
correction and supervised fine-tuning.                             closed-source models and most open-source alternatives.

A. Few-Shot Prompting                                              B. Human-Guided Hints
   Few-shot prompting serves as the primary intervention strat-      Our next strategy investigates whether targeted human guid-
egy. Each model receives 54 reference examples consisting          ance can help LLMs recover from translation failures. Unlike
of paired natural-language geometry problems and Alpha-            few-shot prompting and fine-tuning, which provide general
Geometry translations. These examples expose the model to          knowledge about AlphaGeometry syntax, this approach intro-
common geometric constructions, DSL syntax patterns, and           duces problem-specific information after an initial translation
proof predicates. Compared with zero-shot prompting, few-          has been generated.
shot prompting consistently improves executable translation          As illustrated in Figure 4, we employ a two-stage human-
rates across all evaluated models.                                 guided correction framework.
   Below are two samples of the multi-shot example trans-            1) Stage 1: Diagram-Based Hints: In the first stage, the
lations that are supplied to LLMs. The first section of the        model is provided with a geometric diagram corresponding to
example depicts the English version of the problem, while the      the target problem and is asked to re-evaluate its translation.
second is the manually-verified DSL translation.                   The diagram supplies spatial information that may be difficult
                                      Fig. 3. Model performance for zero-shot and few-shot prompting.



to infer reliably from text alone, including collinearity rela-
tionships, circle memberships, and auxiliary constructions.
   Many Olympiad geometry problems implicitly assume in-
formation that is visually obvious from the accompanying
figure but only partially specified in the textual description. By
incorporating the diagram shown in Figure 4, the model gains
access to additional geometric context that can reduce ambi-
guity during formalization. This stage is effective when the
original translation omits geometric constraints or incorrectly
interprets relationships between points, lines, and circles.
   2) Stage 2: Error-Specific Hints: After examining the re-
vised translation, a second round of guidance is provided
when necessary. Rather than supplying additional geometric
context, these hints directly target observed translation errors.
As shown in the lower portion of Figure 3, the hint may
identify a specific issue such as an incorrect number of clause
parameters, misuse of a geometric predicate, or an invalid
construction. The model is then asked to revise its translation
while preserving the remaining structure. This stage functions
as a targeted correction mechanism. Instead of requiring the
model to rediscover the source of failure, the hint narrows the        Fig. 4. Two-stage human-guided correction framework. In Stage 1, the model
                                                                       is provided with a geometry diagram to supply additional structural context
search space and focuses attention on the problematic portion          and reduce ambiguity in the natural-language problem statement. In Stage
of the formalization.                                                  2, targeted error-specific hints are provided to correct localized translation
                                                                       mistakes identified in the generated AlphaGeometry formalization.
   3) Effectiveness and Limitations: Human-guided hints im-
prove translation quality for strong frontier models, particu-
larly when the initial translation is close to correct. In many
cases, the models demonstrate sufficient geometric understand-         addresses missing geometric information through diagram-
ing to generate an accurate formalization once a specific              based reasoning, while the second stage addresses localized
ambiguity or error has been identified. Figure 4 highlights            translation mistakes through targeted corrective feedback. To-
the complementary roles of the two stages. The first stage             gether, they form an refinement process that improves exe-
cutable translation rates without modifying model parameters.      hints. Among these approaches, few-shot prompting is the
Specifcially, the hint-based methodology improves translation      most scalable and consistently effective strategy, while human-
performance across all evaluated models: GPT-5.4 by 14.29%,        guided correction demonstrates that some translation failures
Gemini 3.1 by 14.63%, Claude Sonnet 4.6 by 26.47%, and             arise from localized ambiguities rather than a complete lack
Grok-3 by 32.14%. These gains show that targeted human             of geometric reasoning capability. These findings suggest
guidance can substantially improve translation rates, especially   that improvements in mathematical formalization may require
for cases involving recoverable formalization errors.              tighter integration between language understanding, geometric
   Despite their effectiveness, human-guided hints have limited    reasoning, and symbolic verification.
scalability. Diagram interpretation requires additional problem       Future work could extend NL2AGBench to additional
resources, and error-specific hints require manual inspection      theorem-proving systems, incorporate geometric diagrams
of model outputs. Consequently, this approach is best viewed       through multimodal formalization, develop specialized auto-
as a diagnostic and correction framework rather than a fully       formalization models, and integrate symbolic feedback for
automated solution for large-scale benchmark evaluation.           iterative self-correction.

C. Supervised Fine-Tuning                                                                        R EFERENCES
                                                                    [1] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving olympiad
   We additionally investigate whether fine-tuning can improve          geometry without human demonstrations,” Nature, vol. 625, pp. 476–
translation performance for smaller open-source models. For             482, 2024.
this experiment, we utilize HAGeo-409, a human-verified             [2] J. Berant, A. Chou, R. Frostig, and P. Liang, “Semantic parsing on
                                                                        freebase from question-answer pairs,” in Proceedings of the 2013
collection of geometry problems paired with AlphaGeometry               Conference on Empirical Methods in Natural Language Processing,
formalizations. Models are fine-tuned to generate DSL repre-            2013, pp. 1533–1544.
sentations directly from natural-language inputs. Fine-tuning       [3] L. Dong and M. Lapata, “Language to logical form with neural atten-
                                                                        tion,” in Proceedings of the 54th Annual Meeting of the Association for
improves adherence to AlphaGeometry syntax and reduces                  Computational Linguistics, 2016, pp. 33–43.
several categories of grammar-related errors. However, im-          [4] S.-C. Chou, X.-S. Gao, and J.-Z. Zhang, “A deductive database approach
provements in executable translation accuracy remain limited.           to automated geometry theorem proving and discovering,” Journal of
                                                                        Automated Reasoning, vol. 25, pp. 219–246, 2000.
Qualitative inspection reveals that many fine-tuned models          [5] e. a. Duan, “Hageo,” 2025, geometry theorem proving and auxiliary-
learn surface-level DSL patterns without reliably capturing             construction research.
the geometric semantics required for correct formalization.         [6] e. a. Zhang, “Tonggeometry,” 2024, geometry theorem proving research.
                                                                    [7] e. a. Sicca, “Newclid,” 2024, open-source geometry theorem proving
In several cases, models generate syntactically plausible but           system.
semantically incorrect constructions, indicating that formaliza-    [8] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik,
tion requires deeper geometric reasoning than simple syntax             and C. Szegedy, “Autoformalization with large language models,” in
                                                                        Advances in Neural Information Processing Systems, 2022.
imitation. These findings suggest that the primary bottleneck       [9] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix,
for smaller models is not solely DSL familiarity but also               Y. Wu, and G. Lample, “Draft, sketch, and prove: Guiding formal
insufficient reasoning capacity.                                        theorem provers with informal proofs,” in International Conference on
                                                                        Learning Representations, 2023.
                                                                   [10] K. Zheng, J. M. Han, and S. Polu, “Minif2f: A cross-system benchmark
          VI. C ONCLUSION AND F UTURE W ORK                             for formal mathematical statement proving,” in International Conference
   This paper investigates a key bottleneck in automated geom-          on Learning Representations, 2022.
                                                                   [11] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil,
etry theorem proving: translating natural-language geometry             R. Prenger, and A. Anandkumar, “Leandojo: Theorem proving with
problems into the formal language required by AlphaGeome-               retrieval-augmented language models,” in Advances in Neural Informa-
try. To address this challenge, we introduce NL2AGBench, a              tion Processing Systems, 2023.
                                                                   [12] e. a. Jana, “Proofbridge,” 2025, formal mathematical reasoning research.
benchmark specifically designed to evaluate the ability of large   [13] e. a. Hubert, “Alphaproof,” 2025, formal mathematical theorem proving
language models to translate English geometry problems into             with reinforcement learning.
AlphaGeometry-compatible formal representations.                   [14] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang,
                                                                        D. Song, and J. Steinhardt, “Measuring mathematical problem solving
   We systematically assess both open-source and closed-                with the math dataset,” in Advances in Neural Information Processing
source LLMs across a diverse collection of geometry prob-               Systems, 2021.
lems. Our results reveal a substantial gap between frontier pro-   [15] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser,
                                                                        M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schul-
prietary models and current open-source alternatives, suggest-          man, “Training verifiers to solve math word problems,” arXiv preprint
ing that successful formalization requires not only syntactic           arXiv:2110.14168, 2021.
mastery of the target language but also accurate geometric         [16] C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han,
                                                                        Y. Huang, Y. Zhang et al., “Olympiadbench: A challenging benchmark
interpretation and constraint preservation. Through detailed            for promoting agi with olympiad-level bilingual multimodal scientific
error analysis, we construct a taxonomy of AlphaGeometry                problems,” 2024.
translation failures, categorizing them into syntax errors and     [17] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang,
                                                                        Y. K. Li, Y. Wu, and D. Guo, “Deepseekmath: Pushing the limits
logic errors. This taxonomy provides a practical framework              of mathematical reasoning in open language models,” arXiv preprint
for understanding model weaknesses and diagnosing failure               arXiv:2402.03300, 2024.
modes in future auto-formalization systems.                        [18] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,
                                                                        Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in
   We further explore multiple mitigation strategies, including         large language models,” in Advances in Neural Information Processing
few-shot prompting, supervised fine-tuning, and human-guided            Systems, vol. 35, 2022, pp. 24 824–24 837.
[19] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang,
     A. Chowdhery, and D. Zhou, “Self-consistency improves chain of
     thought reasoning in language models,” 2022.
[20] T. P. G. H., “Ag4masses,” 2024, modified AlphaGeometry system.
