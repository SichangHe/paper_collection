                                                  Neuro-Symbolic Verification on Instruction Following of LLMs

                                                                 Yiming Su1 * , Kunzhao Xu2 * , Yanjie Gao3† , Fan Yang3 ,
                                                                         Cheng Li2 , Mao Yang3 , Tianyin Xu1
                                                                       1
                                                                         University of Illinois Urbana-Champaign
                                                                    2
                                                                      University of Science and Technology of China
                                                                                   3
                                                                                     Microsoft Research


                                                                 Abstract                                    Despite significant improvement of frontier LLMs,
                                                                                                         their ability of instruction following is still unreliable.
                                             A fundamental problem of applying Large Lan-                Unfortunately, it is non-trivial to observe or check an
                                             guage Models (LLMs) to important applica-                   LLM’s instruction following behavior. The common
arXiv:2601.17789v1 [cs.AI] 25 Jan 2026




                                             tions is that LLMs do not always follow in-                 approach, referred to as LLM-as-a-judge, uses an LLM
                                             structions, and violations are often hard to ob-            to check whether an LLM’s output follows instructions
                                             serve or check. In LLM-based agentic work-                  based on the input prompt (Sirdeshmukh et al., 2025;
                                             flows, such violations can propagate and am-                Liu et al., 2025; OpenAI, 2025; Liu et al., 2023; Cemri
                                             plify along reasoning chains, causing task fail-            et al., 2025). However, as shown in §5, existing LLM-
                                             ures and system incidents. This paper presents              based approaches are unreliable for verifying complex
                                             N SVIF, a neuro-symbolic framework for veri-                instructions. The difficulty in verifying instruction fol-
                                             fying whether an LLM’s output follows instruc-              lowing behavior (1) makes it hard for agents to prevent
                                             tions used to prompt the LLM. N SVIF is a uni-              violations from propagation (Laban et al., 2025), and
                                             versal, general-purpose verifier; it makes no as-           (2) makes failure attribution hard (Zhang et al., 2025a).
                                             sumption on the instruction or the LLM. N SVIF                  This paper presents N SVIF, a neuro-symbolic frame-
                                             formulates instruction-following verification               work for verifying instruction following of LLMs.
                                             as a constraint-satisfaction problem by mod-                N SVIF aims to be universal and general-purpose—
                                             eling user instructions as constraints. N SVIF              taking any output produced by an LLM, N SVIF checks
                                             models both logic and semantic constraints;                 if the output follows the input instruction used to prompt
                                             constraint-solving is done by a unified solver              the LLM. N SVIF makes no assumption on the instruc-
                                             that orchestrates logic reasoning and seman-                tion or the LLM, and does not require additional infor-
                                             tic analysis. To evaluate N SVIF, we develop                mation. We expected its usability to lead to wide use
                                             V IF B ENCH, a new benchmark for instruction-               cases such as agentic workflows (Qi et al., 2025).
                                             following verifiers with fine-grained data labels.              The key idea is to formalize instruction following
                                             Experiments show that N SVIF significantly out-             verification as a constraint-satisfaction problem or CSP.
                                             performs LLM-based approaches and provides                  Concretely, N SVIF models instructions described in the
                                             interpretable feedback. We also show that feed-             prompt as a logic formula of constraints and checks
                                             back of N SVIF helps improve LLMs’ instruc-                 whether the output of an LLM satisfies the formula.
                                             tion following capability without post-training.            N SVIF models two types of constraints: logic and se-
                                                                                                         mantic constraints. The former can be symbolically
                                         1   Introduction                                                checked with logic reasoning (e.g., whether a paragraph
                                                                                                         contains a given keyword); the latter requires semantic
                                         Large Language Models (LLMs) are increasingly used              analysis using neural approaches (e.g., whether a sen-
                                         in real-world applications. However, a fundamental              tence has a positive tone). N SVIF addresses the CSP
                                         problem of applying LLMs to important applications              by generating per-constraint checkers and solving them
                                         is that LLMs do not always follow user instructions—            using a unified solver atop the Z3 SMT (Satisfiability
                                         LLMs are reported to constantly misunderstand or ig-            Modulo Theories) solver (De Moura and Bjørner, 2008).
                                         nore critical parts of user instructions (Jaroslawicz et al.,       N SVIF has several advantages over state-of-the-art
                                         2025; Lou et al., 2024). Such violations can lead to            LLM-based approaches. First, it brings logic reason-
                                         unsafe decisions, incorrect outputs, and system failures.       ing for instructions that can be and should be checked
                                         In agentic use cases, the impact of violations can prop-        by traditional tools and symbolic analysis. Moreover,
                                         agate and amplify along reasoning chains and work-              the decomposition of instructions into fine-grained con-
                                         flows (Cemri et al., 2025; Laban et al., 2025).                 straints enables the divide-and-conquer strategy, which
                                            * Equal Contribution. This paper is a result of an open-
                                                                                                         is more effective than directly verifying a composite in-
                                                                                                         struction. Third, the CSP formulation makes the results
                                         source project. Kunzhao Xu is a PhD student. This work was
                                         done during Kunzhao’s internship at Microsoft Research.         significantly more interpretable—N SVIF pinpoints the
                                            †
                                              Corresponding author: Yanjie Gao                           violated constraint and how the output fails it.
                                         (E-mail: yanjga@microsoft.com)                                      Note that semantic constraints are inherently subjec-
                          Table 1: Common types of violations of LLM instruction following.
    Category    Type                   Desc.
                Invariant violation    Output violating invariants such as ordering or uniqueness rules described in the prompt
    Logic       Structural violation   Output not adhering to described schema or data type (e.g., JSON, XML, or template)
                Invalid element        Output omitting required elements or including prohibited entities
                Misinterpretation      LLMs misunderstanding of instruction semantics and failures of resolving ambiguity
    Semantic
                Pragmatic mismatch     Output misaligning with the intent, stylistic requirements, or scope of the instruction


tive and it is hard for semantic analysis to draw absolute        studies (Lou et al., 2024; Jaroslawicz et al., 2025; Laban
conclusions. For each individual semantic constraint,             et al., 2025; Sirdeshmukh et al., 2025) reported various
N SVIF inherits the properties of the semantic analysis it        kinds of LLM behavior that fail to follow instructions;
uses. As a framework, N SVIF can be equipped with any             Table 1 summarizes a few common types. Therefore,
semantic analysis for semantic constraints. Following             effective verification of instruction following is desired.
the common practice (Liu et al., 2025), our implemen-                Despite significant efforts on benchmarking instruc-
tation uses LLMs to evaluate each individual semantic             tion following ability of LLMs (He et al., 2024; Wu
constraint. Other models with verified predictability (Al-        et al., 2024b; Qi et al., 2025; Young et al., 2025; Zhou
barghouthi, 2021) or specialized personalities can also           et al., 2023; Zou et al., 2025; Wen et al., 2024; Lou
be used. The key to N SVIF is decomposing fine-grained            et al., 2024; Qin et al., 2024), we are in search of a
constraints and applying semantic analysis and logic              general-purpose technique that can effectively, reliably
reasoning accordingly under a unified framework.                  verify whether an output of an LLM follows the input
   We develop V IF B ENCH, a new benchmark that mea-              instruction. We find that evaluation techniques used
sures the effectiveness of instruction following verifiers        by existing instruction following benchmarks either use
like N SVIF. V IF B ENCH contains 820 labeled data, in            domain-specific oracles (Laban et al., 2025; Jaroslawicz
the form of <instruction, output, result> tuples, where           et al., 2025; Wen et al., 2024) or use LLMs as eval-
an instruction consists of a set of constraints and their         uators (Zeng et al., 2024; Liu et al., 2025). Domain-
relations, the output has detailed annotations on which           specific oracles often assume the types of instructions
constraints it violates (if any), the result asserts whether      used in the benchmarks and thus are not applicable to
the output follows the instruction. Different from ex-            cases not covered in the benchmark. Existing LLM-
isting benchmarks (Zeng et al., 2024; Liu et al., 2025)           based evaluators, on the other hand, is unreliable, as
that only provide one single result label, V IF B ENCH            shown in our evaluation (§5).
provides fine-grained analysis on how a verifier rea-                Note that N SVIF focuses on verification of instruction
sons about instruction following behavior. We evaluate            following, rather than evaluation of natural language
N SVIF on V IF B ENCH. Our results show that N SVIF               generation (Gao et al., 2025). In other words, N SVIF
can significantly outperform widely used baselines that           checks behavior correctness of LLMs with respect to
directly use LLMs as judges, demonstrating the effec-             constraints and intent, not linguistic quality per se.
tiveness of the neuro-symbolic approach in verifying
instruction following. We show that N SVIF provides               2.2   Constrained Decoding
constraint-level feedback and improves LLM instruction            N SVIF applies to instructions in both natural language
following capability without post-training.                       prompts and structured inputs written in declarative lan-
   In summary, we make the following contributions:               guages or schemas for constrained decoding. For the for-
  • Approach. A neuro-symbolic approach for instruc-              mer, N SVIF extracts constraints from input prompts. For
    tion following verification, which formulates ver-            the latter, DSPy (Khattab et al., 2024) and PDL (Vaziri
    ification as a constraint-satisfaction problem and            et al., 2024) allows users to specify type constraints, in-
    model both logic and semantic constraints.                    cluding primitive data types and natural-language typed
    • Tooling. N SVIF, a universal, general-purpose frame-        signatures; LMQL (Beurer-Kellner et al., 2023) pro-
      work for verifying LLM outputs against instructions         vides built-in functions that allow users to specify log-
      and improving LLM’s instruction following capabil-          ical constraints such as word count or last token in a
      ity without post-training.                                  sequence. N SVIF can directly interface with these tools;
    • Benchmark. V IF B ENCH, a new benchmark and                 it verifies type and structure constraints by synthesizing
      data synthesis toolchain for evaluating verification        type and format checkers. N SVIF goes beyond type
      techniques on instruction following of LLMs.                and structure constraints. Mellea (Cox, 2025) which
                                                                  allows users to define requirements of the LLM output.
2     Background                                                  Mellea uses LLMs as verifiers unless user-defined func-
                                                                  tions are provided. Different from Mellea, N SVIF does
2.1     Instruction Following of LLMs                             not need to explicitly define constraints a priori. More-
As a basic ability, instruction following is unreliable           over, N SVIF does not directly apply LLMs to verify all
even in today’s frontier LLMs (OpenAI, 2025). Prior               constraints and their compositions.
2.3   Formal Reasoning of LLMs and Agents                     mulates the CSP by using an LLM to translate the in-
N SVIF applies formal reasoning to verify and reshape an      struction into a first-order logic formula (§3.1). It then
LLM’s outputs based on user instructions. The principle       checks every individual constraint against the output.
echos recent practices of specifying model and agent          For each constraint, N SVIF first uses an LLM to classify
behavior (Crouse et al., 2023; Li et al., 2024b). Differ-     whether the constraint is a logic constraint or a semantic
ently, N SVIF focuses on instruction following behavior       one. For each logic constraint, N SVIF uses an LLM
of LLMs, instead of other behavior like tool calling and      to generate code that check the constraint against the
multi-agent coordination. N SVIF can be used as a step-       output. For semantic analysis, N SVIF prompts an LLM
wise verifier in an agentic workflow, where each agent        as the judge. Lastly, N SVIF solves the CSP as a Z3
step and its output can be checked by N SVIF.                 program and output the final result.
   N SVIF uses LLMs as helpers to formulate the ver-             As a neuro-symbolic approach, N SVIF uses LLMs
ification problem into first-order logic predicates and       for a series of tasks, including (1) extracting constraints
solve it using a SMT solver. The principle is applied         from the instruction and formulating the instruction into
in related work like LINC (Olausson et al., 2023) and         a first-order logic formula with constraints as predi-
Logic-FM (Pan et al., 2023) which use LLMs to trans-          cates (Olausson et al., 2023; Ma et al., 2025), (2) clas-
late natural language premises and conclusions into first-    sifying constraints into logic or semantic types (Sun
order logic statements and use a theorem prover to prove      et al., 2023), (3) for logic constraints, generating the
the statements. Differently, N SVIF needs to formulate        checker code (Olausson et al., 2023; Zhang et al., 2025b;
the premises in the verification process as it needs to       Jimenez et al., 2024; Chowdhury et al., 2024), and (4)
individually check whether each constraint is satisfied.      for semantic constraints, checking if the output satis-
                                                              fies the constraints. Therefore, like any LLM-based
3     N SVIF: A Neuro-Symbolic Framework                      approaches, N SVIF also subjects to hallucination behav-
                                                              iors of LLMs. On the other hand, by breaking down
N SVIF is a universal, general-purpose framework for          instruction following verification into specific, well-
verifying whether an output O produced by an LLM              defined tasks, N SVIF significantly improves verification
follows the instruction I used to prompt the LLM. It          effectiveness and produces interpretable results.
takes any arbitrary ⟨I, O⟩ and returns a boolean result.
It makes no assumption on I, O, or the LLM, and does          3.1   Problem Formulation
not need any hints or other information.                      N SVIF formulates the instruction following verification
   N SVIF is built atop neuro-symbolic principles. First,     problem as a Constraint-Satisfaction Problem or CSP.
inspired by prior work on modeling an instruction as a        For an input ⟨I, O⟩, N SVIF verifies whether O satisfies
composition of constraints (Wen et al., 2024; Pyatkin         the constraints C and their relations in a first-order logic
et al., 2025; Jiang et al., 2024; Zhou et al., 2023; Pham     formula f (C) specified by I,
et al., 2024; Yuan et al., 2025), N SVIF models an in-                               (
struction as a formula in first-order logic where the                                  SAT         if O |= f (C)
predicates are constraints. In essence, N SVIF formu-                verify(I, O) =
                                                                                       UNSAT otherwise
lates the verification problem as a constraint-satisfaction
problem or CSP. In this way, N SVIF not only reasons          N SVIF differentiates two types of constraints:
about constraints individually but also their composi-
tions collectively. The use of first-order logic makes         • A logic constraint can be encoded using symbolic
N SVIF sufficiently expressive. It encodes various kinds         rules, regular expressions, or executable code. Sat-
of constraints into a unified formal reasoning frame-            isfaction is checked via symbolic reasoning and/or
work and enabling reasoning tools like SMT (Satisfiabil-         constraint solving. The verification of logic con-
ity Modulo Theories) solvers (our implementation uses            straints is objective based on first principles.
Z3 (De Moura and Bjørner, 2008)) to rigorously check           • A semantic constraint is hard to be verified by
if an given output O follows the instruction.                    logic reasoning but requires semantic analysis us-
   The formulation enables specialized reasoning of in-          ing neural approaches. Although a semantic con-
dividual constraints based on their inherent properties.         straint lacks explicit structure, it implicitly encodes
Real-world constraints are different. Some are about             a learned boundary between satisfying and violat-
logic, which specify lexical, format, and structure re-          ing the constraint based on in-context examples or
quirements, e.g., whether a paragraph contains a key-            prompts. Note that the semantic analysis can be
word. Such constraints should be verified by logical             subjective, e.g., the same writing can be perceived
reasoning. The others are semantic, which specify re-            differently by different people or LLMs. Therefore,
quirements on topic, tone, style, sentiment, e.g., whether       the verification results are not absolute but with re-
a paragraph is on the topic of science. Such constraints         gard to the semantic analysis (e.g., the LLM used in
should be verified by semantic analysis. N SVIF’s divide-        N SVIF and its inference parameters).
and-conquer strategy makes it significantly more effec-
tive than verifying the entirety of the instruction.            N SVIF encodes all the constraints into a unified first-
   Concretely, for a given instruction, N SVIF first for-     order logic formula as a CSP using logical connectives
           Instruction                   Formulation Agent                       Checking Agent                        Solver Agent
 Please write a piece of text on     The output should have a
 technology and education that                                               Formal Tone        Semantic            solver.add(
                                           formal tone                                                                formal_tone == True
 has a formal tone and does not                                                  return LLM("is the text            )
 include the keyword “fees” ...             The output should NOT                formal?" + text)                   solver.add(
                                             include “tuition fees”                                   SAT             keyword == False
                                                                                                                    )
          LLM Output
                                                                                                                    solver.check()
 … admissions workflows, and                                              Keyword Exclusion       Logic
 even discussions about tuition                                                  def keyword_exclusion():
                                    C1: Writing       C2: Keyword∧                                                          UNSAT!
 fees …                                           ∧                …               if "fees" in text: ...
                                        tone           exclusion                                                  Trace: fail to exclude “fees”
                                                                                                    UNSAT
                                   Parsing constraints into FOL formula   Checking constraints with programs   Solving FOL with program output
                          Figure 1: Overview of the N SVIF framework and the verification workflow.

including NOT (¬), AND (∧), and OR (∨). N SVIF sup-                       agent generates an executable Python program to check
ports common connectives include negation, disjunc-                       whether the output satisfies the constraint. (Python is
tion, conjunction, implication, and equivalence, which                    chosen because it is reported to be the best supported
can express all the specific composition types in prior                   language by LLMs (Yang et al., 2025)). For each se-
work (Wen et al., 2024; Jaroslawicz et al., 2025; Zhou                    mantic constraint, the agent generates a short, zero-shot
et al., 2023; Sirdeshmukh et al., 2025). The logic for-                   LLM prompt tailored to the constraint to check whether
mula is then checked by an SMT solver.                                    the output satisfies the constraint. The checking agent
                                                                          then executes all the programs and saves the results
3.2    Implementation                                                     into files. Note that the generated checker code can
As shown in Figure 1, we implement N SVIF as a multi-                     fail (e.g., throwing runtime exceptions); we allow mul-
agent system that orchestrates a formulation agent, a                     tiple self-reflections (three by default) for the LLM to
checking agent, and a solver agent. N SVIF takes a <I,                    fix or improve the code. If the LLM fails to fix errors
O> pair as input and outputs a boolean result which tells                 within given budget, it gives up and falls back to use
whether O follows I, and if not, a detailed explanation.                  LLMs directly to evaluate the constraint, which essen-
Formulation agent. The agent prompts an LLM to                            tially treats the logic constraint as a semantic constraint.
formulate the CSP based on the input instruction. The                     We include in-context learning examples that showcase
prompt asks the LLM to identify constraints in the in-                    example logic and semantic constraints. We also require
struction and analyze their relations. For each identified                chain-of-thought reasoning on how a constraint should
constraint, the agent gives a one-sentence summary of                     be verified to ground the agent in the program genera-
the constraint. The prompt then instructs the LLM to                      tion task. The prompt for generating checker code can
analyze the relations of the constraints, asking for a                    be found in Appendix B.
first-order logic formula of the constraints and encoding                    The agent aggregates all individual constraint results
it into a Z3 program. We include several in-context                       and execute the Z3 program to produce the final verifi-
learning examples on parsing constraints from exam-                       cation result. The agent produces both a boolean result
ple texts in the prompt to demonstrate instructions with                  (sat or unsat) and an explanation for interpretability.
both logic and semantic constraints with their desired                    The explanation provides detailed information that pin-
outputs. We also include a chain-of-thought reasoning                     points the violated constraints and the logic formula that
instruction to help the agent reason through the parsing                  leads to the final result. For a violated logic constraint,
process. The formulation agent produces two items: (1)                    it includes the checker code that invalidates O. For
a list of constraint summaries as text, each corresponds                  a violated semantic constraint, it includes the LLM’s
to a constraint in the instruction and (2) a Z3 program                   response and reasoning traces.
that encodes the first-order logic formula of constraints.                 Extensibility. The modularity of N SVIF makes it
If the constraints and their relations are already speci-                  highly extendable. First, we allow users to customize
fied using constrained decoding frameworks (§2.2), the                     LLMs across agents and within one agent, as different
agent only needs to translate them into a Z3 program.                      LLMs have specialized capabilities. For example, the
Checking agent. For each constraint summary re-                            checking agent can benefit from strong coding LLMs
ceived, the agent generates code to check whether the                      especially if the checker code is large and complex.
output O satisfies the constraint. The agent first prompts                 The LLMs for evaluating semantic constraints can be
an LLM to classify whether a constraint is a logic or                      customized based on concrete domains and use cases.
a semantic constraint. In this step, we input the agent                       The techniques for checking logic and semantic con-
with the original <I, O> pair, the constraint summary,                     straints can be extended independently, with the emerg-
and the Z3 program. For each constraint, the agent first                   ing of new instruction types or domains. Specifically,
generates a checking plan: (1) the constraint summary                      N SVIF exposes an interface that allows users to add
and its type, (2) the input and output of the checker                      custom constraints and corresponding checkers to help
code, and (3) the expected behavior of the checker. The                    incorporate domain-specific knowledge and context-
agent then uses another prompt to generate the checker                     sensitive analysis. To do so, users need to package
code based on the plan. For each logic constraint, the                     the checkers as an executable function in Python—the
checking agent can discover custom functions and use               Instruction Synthesis                Output Generation
them in corresponding checkers.                                                                     Template           LLM output
                                                                     Word count (logic)
   We also plan to equip N SVIF with advanced tools                                                    SAT              UNSAT
(e.g., for querying system states) for use cases that re-        Keyword Inclusion (logic)           Keep in           Re-prompt
quire external information or advanced utilities (see §7).                    …                      benchmark         until SAT

                                                                  Writing tone (semantic)              Re-prompt LLM for SAT
3.3   Use Cases                                                                                               examples
                                                               Sampled combination of constraints
                                                                                                       Word count ≈ 500 words
N SVIF targets LLM use cases that require verification
                                                                                                       Word count > 500 words
of instruction following behavior. One target use case
                                                                 Please
                                                                  Please write aapiece  of
is agentic workflows, where agents frequently instruct             Pleasewrite
                                                                          write apiece
                                                                                   pieceofof               Mutated Template
                                                                 text
                                                                  textconsidering  all these
LLMs and do so iteratively. Prior work (Cemri et al.,              text considering allthese
                                                                       considering  all  these              UNSAT output
                                                                 constraints:
                                                                  constraints:…
2025) shows that instruction following is critical in agen-        constraints:……                     Mutate template to generate
                                                                     Generated instructions               UNSAT examples
tic workflows as violations can propagate and amplify
along reasoning chains and workflows. N SVIF can serve         Figure 2: Overview of V IF B ENCH’s data generation
as a per-step verifier to ensure every output from the
LLM follows the instruction issued by the agent. Upon
violations, N SVIF’s interpretable explanations are useful
                                                              straints and compose them into complex instructions.
feedback as explicit learning signals for LLMs to better
                                                              V IF B ENCH focuses on verifying instruction following
internalize complex constraints and correct violations
                                                              and uses English writing tasks which do not require
(§5.4). Such a verification-feedback-improvement loop
                                                              additional ability of LLMs (e.g., using external tools).
could enhance the LLM’s instruction-following ability.
                                                                 For constraints, we surveyed constraints from both in-
4     V IF B ENCH                                             struction tuning datasets (Köpf et al., 2023; Zheng et al.,
                                                              2024; Zhao et al., 2024) and instruction following bench-
V IF B ENCH is a new benchmark that evaluates the effec-      marks (Wen et al., 2024; Zhou et al., 2023; Qin et al.,
tiveness of verification techniques of LLM instruction        2024). These constraints cover the ones mentioned in
following. It contains 820 data entries in the form of <in-   Table 1. For logic constraints, we include lexical and
struction, output, result> tuples, where the instruction      structural constraints such as word count and keyword
contains multiple constraints with fine-grained labels        inclusion. For semantic constraints, we included writ-
and the result is either sat or unsat. A verifier under       ing topic (as pragmatic mismatch) and writing tone (for
evaluation (N SVIF or LLM judges) is asked to verify          misinterpretation). In total, V IF B ENCH includes eight
whether the output satisfies the instruction; the answer      types of logic constraints and two types of semantic
is checked against the result label.                          constraints, as shown in Table 5.
   We decided to create a new benchmark, because ex-
isting benchmarks for instruction following verification,        Semantic constraints in V IF B ENCH are described as
namely LLMBar (Zeng et al., 2024) and ReIFE (Liu              desired attributes for the satisfying output text, e.g., The
et al., 2025) (which uses LLMBar) are limited. LLM-           output text should be in a positive tone”. Logic con-
Bar formulates verification of instruction following as       straints are further specified with specific values that
a classification problem. Each instruction is paired          attaches to specific writing topic” values. We focus
with two outputs—one is preferred over the other as           on writing tone and writing topic because we find that
per the instruction. An LLM-as-a-judge is prompted to         they are the least subjective constraints and thus help
choose between the two. We attempted to use LLMBar            evaluate the correctness of the verification. Other seman-
in the evaluation of N SVIF, but found it unreliable—         tic constraints such as clarity and fluency often solicit
preference does not indicate instruction following. A         subjective responses, confounding verification results.
preferred output may still violate constraints and less       (V IF B ENCH focuses on validation of instruction follow-
preferred ones can satisfy all constraints. LLMBar does       ing, not evaluation of natural language generation (see
not provide fine-grained information that explains why        §2.1).)
and how an output violates the instruction.                      We then synthesize instructions by composing con-
   V IF B ENCH addresses these limitations by (1) synthe-     straints. V IF B ENCH varies the number of constraints
sizing instruction from well-defined constraints, and (2)     in one instruction, which represents the complexity of
providing fine-grained information whether the output         the instruction. For a chosen number of constraints
satisfies each constraint and the reasons of violations       in one instruction, we permute the logic and seman-
if any. V IF B ENCH includes both sat and unsat out-          tic constraints and their relations. Each instruction in
puts that cover common categories in Table 1. Figure 2        V IF B ENCH contains at least one semantic constraint
shows the workflow of data generation of V IF B ENCH.         and one logic constraint. By mixing both types of con-
                                                              straints, V IF B ENCH evaluates whether a verifier can
4.1   Instruction Synthesis                                   conduct both logic reasoning and semantic analysis. In
The instruction synthesis follows the practice of Com-        summary, an instruction in V IF B ENCH prompts LLMs
plexBench (Wen et al., 2024). We define a set of con-         to output a writing response with specific requirements.
                              Table 2: Verification effectiveness of N SVIF and the baseline on V IF B ENCH
                                                            N SVIF                                       Baseline (LLM-as-a-judge)
    Model
                                    F1 score               Precision      Recall   Pass@1          F1 score        Precision    Recall   Pass@1
    GPT-4.1                   94.8% (25.7%↑)                94.2%         95.4%    95.0%            69.1%            52.9%      99.5%     57.4%
    GPT-4o                    82.0% (15.8%↑)                91.2%         74.4%    84.4%            66.2%            51.3%      93.3%     54.6%
    DeepSeek-R1               83.9% (7.00%↑)                94.6%         75.4%    86.0%            76.9%            84.2%      70.8%     79.6%
    DeepSeek-V3.1             93.2% (22.0%↑)                97.0%         89.8%    93.8%            71.2%            70.6%      71.9%     72.2%
    Qwen3-Max                 94.8% (23.2%↑)                98.4%         91.6%    95.2%            71.6%            59.0%      91.0%     65.6%
    GPT-4o-mini                      37.3%                  77.2%         24.5%    60.4%       66.6% (29.3%↓)        51.0%      95.9%     54.1%


Instruction   Please write a text on tech and education…     C1      C2      C3       • C ONV-C OT is a conversation-based LLM-as-a-
                                                                                        judge technique (Wu et al., 2024a) where multiple
    Output Learning systems keep courses organize…           C1      C2      C3
                                                                                        roles converse with each other to reach a verdict on
      Figure 3: An example data entry in V IF B ENCH                                    instruction following. It contains:
                                                                                            – a literalist that lists constraints in an instruction,
4.2      Output Generation
                                                                                            – a pragmatist who summarizes the intent behind
Concretely, for a template output generated by LLMs,                                          each instruction, and
we carefully inspect whether the output follows the in-                                     – the skeptic who scrutinizes the process.
struction. If it does not follow the instruction, we regen-
erate and reinspect the template output till it satisfies the                              If the roles disagree, they must debate to reach a
instruction. Then, we craft unsat outputs. We mutate                                       consensus. This process enables more fine-grained
the instruction in the way that the output violates the                                    CoT reasoning than basic “think step-by-step” CoT.
constraints in Table 1. We balance the sat and unsat
outputs in V IF B ENCH to avoid major data skews in the                                 We also include a variant of N SVIF as ablation analy-
dataset. Among the 820 data points in V IF B ENCH, 391                               sis.
(47.68%) of them have sat outputs and 429 (52.32%)
                                                                                      • N SVIF -N EU is a variant of N SVIF which only con-
have unsat outputs.
                                                                                        tains the SMT solver. Different from N SVIF, it
   Figure 3 exemplifies data entries in V IF B ENCH. Ev-
                                                                                        directly queries LLMs to check every constraint
ery instruction in V IF B ENCH has clear labels of its
                                                                                        without logical reasoning.
constraints; the corresponding output also has a clear
result label on whether it is sat or unsat, and, if it is
                                                                                     Models. To make the evaluation simple and easy to
unsat, has fine-grained labels on which constraints are
                                                                                     understand, we use one LLM for each evaluated veri-
violated. Therefore, V IF B ENCH enables fine-grained
                                                                                     fier, instead of customizing LLMs for different compo-
evaluation on a verifier’s ability to reason over multiple
                                                                                     nents. We use three model families: GPT, DeepSeek,
interacting constraints within an instruction, rather than
                                                                                     and Qwen3; specifically: GPT-4.1 (2025-04-14), GPT-
treating instruction following as a single-label decision.
                                                                                     4o (2024-11-20), DeepSeek-V3.1, DeepSeek-R1 (0528),
                                                                                     and Qwen3-Max (2025-09-23). GPT-4.1 is used as the
5      Evaluation                                                                    default LLM for ablation analysis in §5.1.1 and agent-
We evaluate N SVIF and compare it with the reference                                 oriented study in §5.4, as it is the most accessible model
verifiers on V IF B ENCH.                                                            offered to authors. Although N SVIF expects strong
                                                                                     LLMs as it requires capabilities like formulation and
Reference solutions. We compare N SVIF with three
                                                                                     code generalization, we include a small model GPT-4o-
LLM-as-a-judge techniques.
                                                                                     mini (2024-07-18) in the evaluation to understand the
                                                                                     behavior of small models.
    • Baseline. We use a standard implementation of
      LLM-as-a-judge described in Zheng et al. (2023);                               Metrics. We measure verification effectiveness us-
      a two-shot prompt is used to show the LLM one                                  ing four metrics: F1 score, Precision, Recall, and
      unsat and one sat example (Appendix B).                                        Pass@1 (Chen et al., 2021). We consider F1 score as
                                                                                     the primary metric as it balances precision and recall.
  We further improve the baseline with two advanced
prompt optimization techniques.                                                      5.1    Verification Effectiveness
                                                                                     Table 2 shows the effectiveness of instruction following
    • GEPA-C OT optimizes the baseline with a Chain-                                 verification of N SVIF over the baseline using different
      Of-Thought (CoT) prompt using the GEPA prompt                                  LLMs. N SVIF significantly outperforms the baseline.
      optimization algorithm (Agrawal et al., 2025) pro-                             With DeepSeek-R1 as a reasoning model, the baseline
      vided by DSPy (Khattab et al., 2024).                                          achieves the highest F1 score of 76.9%; N SVIF achieves
Table 3: Verification effectiveness of N SVIF with other              Table 4: The percentage (number) of false positives and
advanced verifiers (all using GPT-4.1). The results serve             false negatives of each approach with GPT-4.1
as an ablation study (§5.1.1)
                                                                            Verifier          FP % (#)         FN % (#)
    Verifier            F1 Score    Precision    Recall      Pass@1         Baseline        42.32% (347)       0.24% (2)
    GEPA-C OT              67.1%      84.2%      55.8%       73.8%          GEPA-C OT        5.00% (41)      21.10% (173)
                                                                            C ONV-C OT      14.27% (117)      7.32% (60)
    C ONV-C OT             78.9%      73.9%      84.7%       78.4%          N SVIF -N EU     9.88% (81)       5.98% (49)
    N SVIF -N EU           84.0%      80.9%      87.5%       84.1%          N SVIF (Full)    2.80% (23)       2.20% (18)
    N SVIF (Full)          94.8%      94.2%      95.4%       95.0%


                        Nsvif         Baseline (LLM-as-a-judge)       ple, we observe that it is difficult for N SVIF -N EU to
           1.0                                                        check word-count constraints; such logic constraints
           0.8                                                        are challenging for LLMs as the judgments, but are
F1 score




           0.6                                                        straightforward for generated code.
           0.4                                                        5.1.2 Instruction Complexity
           0.2
                                                                      V IF B ENCH covers instructions with different levels of
           0.0
                   2   3     4 5 6 7 8 9                      10      complexity, in terms of the number of constraints. Fig-
                           # of Constraints in Instruction            ure 4 breaks down the effectiveness of N SVIF and the
Figure 4: F1 scores of N SVIF and the baseline by num-                baseline (both using GPT-4.1) for different instruction
ber of constraints in an instruction (using GPT-4.1)                  complexity levels, from two to ten constraints respec-
                                                                      tively. We see no clear trend of effectiveness with the
90+% F1 scores using GPT-4.1, DeepSeek-V3.1, and                      number of constraints.
Qwen3-Max. On the same LLM, N SVIF outperforms
the baseline by up to 25.7% increase in F1 scores.                    5.2   Impacts of LLM Capabilities
   The baseline has higher recall than precision; we ob-              We evaluated N SVIF on multiple LLMs, including
serve that LLMs tend to have more false positives than                strong models (GPT-4.1, DeepSeek-V3.1, and Qwen3-
false negatives (§5.3). Only DeepSeek models show a                   Max) and small models (GPT-4o-mini).
balance between sat and unsat. Some unsat out-                            Compared with GPT-4.1, GPT-4o displays more fail-
puts in V IF B ENCH appear to satisfy all the constraints,            ures in parsing instructions. For example, GPT-4o fails
but in fact violate certain logic constraints. For exam-              to parse part of the constraint on ignoring certain lines
ple, an output can fulfill the writing tone and topic con-            in the output when counting words, which misleads the
straints but fail to precisely hit word count. The baseline           checking agent to generate incorrect code. We expect
has a hard time catching these subtle violations.                     DeepSeek-R1, as a reasoning model, to perform better
                                                                      than DeepSeek-V3.1 when used in N SVIF. However,
5.1.1            Ablation Analysis                                    DeepSeek-R1 displays more false-negative judgments
We conduct a comparative analysis of N SVIF with                      on analyzing semantic constraints, causing lower recall.
GEPA-C OT, C ONV-C OT, and N SVIF -N EU, which                            We also evaluate N SVIF on a small model—GPT-
serves as an ablation study of N SVIF. GEPA-C OT                      4o-mini. Unexpectedly, with GPT-4o-mini, the effec-
and C ONV-C OT stand for the best LLM-as-a-judge ap-                  tiveness of N SVIF is worse than the baseline (Table 2).
proaches without the CSP formulation. N SVIF -N EU                    N SVIF requires the LLM to be capable of: (1) identi-
uses CSP formulation but does not do logic reasoning                  fying the constraints, (2) classifying every constraint
for individual logic constraints.                                     as logic or semantic, and (3) generating checker code
   Table 3 shows the results of comparative analysis,                 for logic constraints. GPT-4o-mini is effective in (1)—
where all verifiers use GPT-4.1. Both GEPA-C OT and                   among 820 instructions, GPT-4o-mini correctly iden-
C ONV-C OT outperform the baseline, as the optimized                  tifies all constraints in 734 instructions. However, it
prompts help LLMs think through the constraints and                   misclassifies constraint(s) in 508 instructions, e.g., mis-
be more effective on checking certain constraints. For                classifying writing topics as logic constraints, forcing
example, GEPA-C OT introduces the idea of constraints                 the checking agent to generate code to check them. For
and step-by-step verification into the basic CoT prompt.              semantic constraints, it is hard for GPT-4o-mini to gen-
Both GEPA-C OT and C ONV-C OT first list all the con-                 erate effective code, e.g., it generates a simple keyword
straints in the instruction and verify them step by step.             check (e.g., if education is in the text) for topic con-
   However, they are less effective in verifying the con-             straints. We did not expect misclassification to be a
straints, compared with N SVIF -N EU and N SVIF which                 bottleneck and lead to negative results.
use SMT solvers for formal reasoning. As expected,
leveraging symbolic reasoning can substantially im-                   5.3   Soundness and Completeness
prove verification effectiveness. Note that N SVIF outper-            We analyzed the soundness and completeness of N SVIF
forms N SVIF -N EU. Due to the lack of logic checkers,                as a verifier. Soundness is measured by false positives
N SVIF -N EU is weak on logic constraints. For exam-                  and completeness is measured by false negatives. We
  Agent                                                             LLM   pinpoint the violation and ask GPT-4.1 to regenerate
       Plan a trip from New York City to San Francisco,                   the plan with the violation information, until it passes
       include 3 cities on the way, you must include one                  N SVIF. GPT-4.1 takes one iteration to fix the dish item
       place to visit, one vegetarian dish in each city, …
                                                                          in the output and produce a sat output.
                   Chicago, IL, Cloud Gate, Italian beef sandwich
                                                                             We further selected nine instructions from V IF -
      NSVIF:   UNSAT                                                      B ENCH which the LLM (GPT-4.1) failed to follow. The
       Your plan does not satisfy the instruction. The                    nine instructions have different numbers of constraints
       violated constraints include:                                      from 2 to 10, sampled from the complexity group in
       “Dish for each city must be vegetarian.”
       Please improve your plan.                                          Figure 4. We evaluate (1) how N SVIF’s output can
                                                                          help GPT-4.1 iteratively improve its output and (2) how
                   Chicago, IL, Cloud Gate, dish: mushroom pizza
                                                                          many iterations GPT-4.1 takes to reach an instruction-
      NSVIF:    SAT                                                       following output with N SVIF feedback. For all the
                                                                          instructions, GPT-4.1 eventually produces a sat out-
Figure 5: Workflow of N SVIF improving LLM instruc-                       put in less than 5 iterations when guided by N SVIF; 5
tion following via multi-turn feedback.                                   (55.6%) are corrected in less than 3 iterations. Diffi-
                                                                          cult constraints include total word count and writing
define a false-positive verification result as the verifier               tone, which take GPT-4.1 several iterations to satisfy.
producing a sat result when the output does not satisfy                   For the word-count constraint, the word count of the
the instruction, and a false-negative verification result                 initial output greatly violates the constraint; GPT-4.1 it-
as the verifier producing an unsat result when the                        eratively improves the output by editing sentences while
output actually satisfies the instruction. Table 4 shows                  still keeping the text on topic. This shows that even
the two metrics of N SVIF and the reference verifiers                     though the LLM is not capable of symbolic reasoning,
(all using GPT-4.1). All the references have high rates                   given the right feedback, it can still follow the feedback
(around 10%) of either false positives or false nega-                     and improve upon itself. For the writing tone constraint,
tives. We observe that GPT-4.1 has trouble checking                       GPT-4.1 tunes words and gradually makes text pass
logic constraints such as word counts (either over- or                    verification.
under-counting). In fact, GPT-4.1 tends to estimate the                      We then experimented with a boolean feedback simi-
word count, instead of counting it precisely. Moreover,                   lar to the baseline approach. When the output violates
GPT-4.1 struggles to correctly solve first-order logic,                   the instruction, we only give GPT-4.1 the single unsat
resulting in incorrect verdict.                                           result and ask it to regenerate. We give GPT-4.1 up to
   N SVIF -N EU outperforms GEPA-C OT and C ONV-                          15 iterations to generate a satisfying output. We observe
C OT because it takes the step of writing the Z3 program.                 that for 3 instructions, GPT-4.1 cannot generate a sat-
Certainly, we observe that GPT-4.1 occasionally gener-                    isfying output within the budget, falling into a loop of
ates incorrect formula, causing both false positives and                  retrying. One instruction took GPT-4.1 11 iterations to
false negatives.                                                          finally produce a satisfying output. For the remaining 5
   N SVIF has much fewer false positives and false nega-                  instructions, GPT-4.1 took less than three iterations to
tives. However, it still suffers from hallucination behav-                correct the output. The experiment shows the usefulness
ior of GPT-4.1. For the 23 false positives, GPT-4.1 hal-                  of N SVIF’ feedback in improving instruction-following
lucinates and modifies the given output when invoking                     ability of LLMs without additional post-training.
the checker instead of copying the original text. The hal-
lucinated output satisfies the instruction, causing N SVIF                6   Related Work
to output sat when the ground-truth is unsat. For the
18 false negatives: (1) 12 were caused by GPT-4.1 gen-                    Like N SVIF, prior work also models instructions to
erating wrong results against semantic constraints; (2) 4                 LLMs as constraints (Wen et al., 2024; Zhou et al.,
were caused by checker generation failures and fallback                   2023; Jiang et al., 2024). However, as the focus was
to LLM-as-a-judge which produced wrong results; (3)                       on benchmarking the instruction-following ability of
one was caused by the formulation agent incorrectly                       LLMs, prior work uses predefined sets of constraints
extracting constraints (introducing a constraint that was                 and designs corresponding validators a priori. N SVIF
not in the original instruction); and (4) one was caused                  addresses a different problem. It serves as a universal
by the hallucination behavior similar as the false posi-                  verifier of instruction following without assuming the
tives. We believe some of them could be further reduced                   shapes of input instruction or output. It shares the idea
by patching our current implementation of N SVIF.                         of decomposing an instruction into constraints (Wen
                                                                          et al., 2024; Qin et al., 2024); it does so by formulating
5.4    Multi-turn Feedback                                                instruction following as a constraint-satisfaction prob-
To show that N SVIF can help LLMs follow instructions                     lem, with both logic and semantic constraints which
in agentic settings, we write a simple travel agent that                  can be unified in first-order logic. N SVIF shows that
prompts GPT-4.1 to generate a travel plan with three                      bringing symbolic reasoning for logic constraints sub-
constraints (see Figure 5). GPT-4.1’s initial output vi-                  stantially improves its verification effectiveness.
olates the dietary constraint. The agent uses N SVIF to                      We discussed the limitations of existing benchmarks
for evaluating instruction following verification, namely      fundamental problem is rooted across all commodity
LLMBar (Zeng et al., 2024) and ReIFE (Liu et al., 2025)        LLMs, and our approach is generally applicable to other
in §4. In short, these benchmarks primarily rely on            LLMs that are not evaluated in this work.
preference-based judgments with under-specified accep-
tance criteria, making it difficult to have fine-grained
analysis or comprehend the verifier behavior. V IF -           References
B ENCH is inspired by benchmarks for evaluating in-
                                                               Lakshya A Agrawal, Shangyin Tan, Dilara Soylu,
struction following of LLMs such as Wen et al. (2024).
                                                                 Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Ar-
Note that such LLM instruction following benchmarks              nav Singhvi, Herumb Shandilya, Michael J Ryan,
do not apply directly, because they only contain the             Meng Jiang, Christopher Potts, Koushik Sen, Alexan-
instructions but do not have labeled outputs.                    dros G. Dimakis, Ion Stoica, Dan Klein, Matei Za-
                                                                 haria, and Omar Khattab. 2025. GEPA: Reflective
7   Concluding Remarks                                           Prompt Evolution Can Outperform Reinforcement
                                                                 Learning. arXiv:2507.19457.
In search of a more principled technique than LLMs
as verifiers, we explored a neuro-symbolic approach            Aws Albarghouthi. 2021. Introduction to Neural Net-
that integrates logic reasoning to verify instruction-          work Verification, volume 7. Now Publishers Inc.
following behavior of LLMs and shows its promises.
N SVIF serves as a first step and a framework to enable        Luca Beurer-Kellner, Marc Fischer, and Martin Vechev.
more specialized and personalized verifiers and ensure           2023. Prompting Is Programming: A Query Lan-
instruction following of modern LLMs.                            guage for Large Language Models. In Proceed-
                                                                 ings of the 44th ACM SIGPLAN Conference on Pro-
8   Limitations                                                  gramming Language Design and Implementation
                                                                 (PLDI’23).
On problem formulation, constraint-satisfaction prob-
lem (CSP) is not the only way to formulate instruction-        Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A.
                                                                Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt
following verification. Specifically, CSP does not dif-
                                                                Keutzer, Aditya Parameswaran, Dan Klein, Kannan
ferentiate soft constraints and hard constraints. It is         Ramchandran, Matei Zaharia, Joseph E. Gonzalez,
possible that a given instruction is unsatisfiable, and         and Ion Stoica. 2025. Why Do Multi-Agent LLM
unsatisfiable instructions could lead to infinite retries       Systems Fail? In Proceedings of The 39th Annual
or task failures. We plan to explore a new formulation          Conference on Neural Information Processing Sys-
of constraint-optimization problem or COP, which is a           tems (NeurIPS’25).
generalization of CSP. The challenge is to autonomously
decide the objective function to be optimized.                 Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
   As an LLM-powered tool, N SVIF does not escape               Henrique Ponde de Oliveira Pinto, Jared Kaplan,
from the fundamental paradox—using LLMs to verify               Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
                                                                Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
instruction following of LLMs. It is challenging to
                                                                Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela
completely eliminate hallucination and nondeterminism           Mishkin, Brooke Chan, Scott Gray, and 39 others.
behavior inherent in existing LLMs during N SVIF’s              2021. Evaluating Large Language Models Trained
verification. On the other hand, the neuro-symbolic             on Code. arXiv:2107.03374.
approach of N SVIF minimizes the impact of LLM’s
nondeterminism by: 1. enforcing LLMs to focus on               Neil Chowdhury, James Aung, Chan Jun Shern,
specific, well-defined tasks such as classification and          Oliver Jaffe, Dane Sherburn, Giulio Starace,
code generation, and 2. leveraging symbolic reasoning            Evan Mays, Rachel Dias, Marwan Aljubeh, Mia
at critical steps such as verifying individual constraints       Glaese, Carlos E. Jimenez, John Yang, Leyton
                                                                 Ho, Tejal Patwardhan, Kevin Liu, and Alek-
with programs and finally solving the constraints with a
                                                                 sander Madry. 2024.    Introducing SWE-bench
solver.                                                          Verified.    https://openai.com/index/
   As a benchmark, V IF B ENCH is currently limited to           introducing-swe-bench-verified/.
English writing tasks. Writing tasks are common in
evaluating instruction-following ability of LLMs (Zhou         David Cox. 2025. From Agent Soup to Proper Soft-
et al., 2023; Yao et al., 2024; Qin et al., 2024; Li et al.,     ware Design: Putting the Developer Back in Control
2024a). It currently does not consider multilingual in-          of Generative AI with Mellea. In Proceedings of
structions (Dussolle et al., 2025). Our future work con-         the 39th Annual Conference on Neural Information
siders extending V IF B ENCH to tasks beyond writing             Processing Systems (NeurIPS’25).
tasks, such as information retrieval, general question
                                                               Maxwell Crouse, Ibrahim Abdelaziz, Ramon As-
answering, and planning.                                        tudillo, Kinjal Basu, Soham Dan, Sadhana Kumar-
   Our evaluation was limited to the LLMs that we have          avel, Achille Fokoue, Pavan Kapanipathi, Salim
access to and have the budget to run. Other LLMs                Roukos, and Luis Lastras. 2023. Formally Specify-
could manifest different characteristics and may lead to        ing the High-Level Behavior of LLM-Based Agents.
different results. On the other hand, we believe that the       arXiv:2310.08535.
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3:        Zekun Li, Baolin Peng, Pengcheng He, and Xifeng
  An Efficient SMT Solver. In Proceedings of the          Yan. 2024a. Evaluating the Instruction-Following
  14th International Conference on Tools and Algo-        Robustness of Large Language Models to Prompt
  rithms for the Construction and Analysis of Systems     Injection. In Proceedings of the 2024 Conference on
  (TACAS’08).                                             Empirical Methods in Natural Language Processing
                                                          (EMNLP’24).
Antoine Dussolle, A. Cardeña, Shota Sato, and Peter
  Devine. 2025. M-IFEval: Multilingual Instruction-     Zelong Li, Wenyue Hua, Hao Wang, He Zhu, and
  Following Evaluation. In Proceedings of the 2025        Yongfeng Zhang. 2024b. Formal-LLM: Integrating
 Annual Conference of the Nations of the Americas         Formal Language and Natural Language for Control-
 Chapter of the Association for Computational Lin-        lable LLM-based Agents. arXiv:2402.00798.
  guistics (NAACL’25).
                                                        Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang,
Mingqi Gao, Xinyu Hu, Xunjian Yin, Jie Ruan, Xiao         Ruochen Xu, and Chenguang Zhu. 2023. G-Eval:
 Pu, and Xiaojun Wan. 2025. LLM-based NLG Evalu-          NLG Evaluation using Gpt-4 with Better Human
 ation: Current Status and Challenges. Computational      Alignment. In Proceedings of the 2023 Conference
 Linguistics, 51:661–687.                                 on Empirical Methods in Natural Language Process-
Qianyu He, Jie Zeng, Wenhao Huang, Lina Chen, Jin         ing (EMNLP’23).
  Xiao, Qianxi He, Xunzhe Zhou, Jiaqing Liang, and      Yixin Liu, Kejian Shi, Alexander Fabbri, Yilun Zhao,
  Yanghua Xiao. 2024. Can Large Language Models           PeiFeng Wang, Chien-Sheng Wu, Shafiq Joty, and Ar-
  Understand Real-World Complex Instructions? In          man Cohan. 2025. ReIFE: Re-evaluating Instruction-
  Proceedings of the 38th AAAI Conference on Artifi-      Following Evaluation. In Proceedings of the 2025
  cial Intelligence (AAAI’24).                            Conference of the Nations of the Americas Chap-
Daniel Jaroslawicz, Brendan Whiting, Parth Shah, and      ter of the Association for Computational Linguistics
  Karime Maamari. 2025. How Many Instructions Can         (ACL’25).
  LLMs Follow at Once? arXiv:2507.11538.
                                                        Renze Lou, Kai Zhang, and Wenpeng Yin. 2024. Large
Yuxin Jiang, Yufei Wang, Xingshan Zeng, Wanjun            Language Model Instruction Following: A Survey of
  Zhong, Liangyou Li, Fei Mi, Lifeng Shang, Xin           Progresses and Challenges. Computational Linguis-
  Jiang, Qun Liu, and Wei Wang. 2024. FollowBench:        tics, 50(3):1053–1095.
  A Multi-level Fine-grained Constraints Following
  Benchmark for Large Language Models. In Proceed-      Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and
  ings of the 62nd Annual Meeting of the Association      Lei Bu. 2025. SpecGen: Automated Generation
  for Computational Linguistics (ACL’24).                 of Formal Program Specifications via Large Lan-
                                                          guage Models. In Proceedings of the IEEE/ACM
Carlos E Jimenez, John Yang, Alexander Wettig,            47th International Conference on Software Engineer-
  Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R        ing (ICSE’25).
  Narasimhan. 2024. SWE-bench: Can Language
  Models Resolve Real-world Github Issues? In Pro-      Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  ceedings of The Twelfth International Conference on     Armando Solar-Lezama, Joshua Tenenbaum, and
  Learning Representations (ICLR’24).                     Roger Levy. 2023. LINC: A Neurosymbolic Ap-
                                                          proach for Logical Reasoning by Combining Lan-
Omar Khattab, Arnav Singhvi, Paridhi Maheshwari,          guage Models with First-Order Logic Provers. In Pro-
 Zhiyuan Zhang, Keshav Santhanam, Sri Vard-               ceedings of the 2023 Conference on Empirical Meth-
 hamanan, Saiful Haq, Ashutosh Sharma, Thomas T.          ods in Natural Language Processing (EMNLP’23).
 Joshi, Hanna Moazam, Heather Miller, Matei Za-
 haria, and Christopher Potts. 2024. DSPy: Com-         OpenAI.  2025.        Introducing GPT-
 piling Declarative Language Model Calls into Self-       5.        https://openai.com/index/
 Improving Pipelines. In Proceedings of the 12th In-      introducing-gpt-5/.
 ternational Conference on Learning Representations
 (ICLR’24).                                             Liangming Pan, Alon Albalak, Xinyi Wang, and
                                                          William Yang Wang. 2023. Logic-LM: Empower-
Andreas Köpf, Yannic Kilcher, Dimitri von Rütte,          ing Large Language Models with Symbolic Solvers
  Sotiris Anagnostidis, Zhi-Rui Tam, Keith Stevens,       for Faithful Logical Reasoning. In Findings of the
 Abdullah Barhoum, Nguyen Minh Duc, Oliver                Association for Computational Linguistics: EMNLP
  Stanley, Richárd Nagyfi, Shahul ES, Sameer Suri,        2023 (EMNLP’23).
  David Glushkov, Arnav Dantuluri, Andrew Maguire,
  Christoph Schuhmann, Huu Nguyen, and Alexander        Chau Minh Pham, Simeng Sun, and Mohit Iyyer. 2024.
  Mattick. 2023. OpenAssistant conversations - de-        Suri: Multi-constraint Instruction Following in Long-
  mocratizing large language model alignment. In Pro-     form Text Generation. In Findings of the Associa-
  ceedings of the 37th Annual Conference on Neural        tion for Computational Linguistics: EMNLP 2024
 Information Processing Systems (NeurIPS’23).             (EMNLP’24), pages 1722–1753, Miami, Florida,
                                                          USA. Association for Computational Linguistics.
Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, and
  Jennifer Neville. 2025. LLMs Get Lost In Multi-Turn   Valentina Pyatkin, Saumya Malik, Victoria Graf,
  Conversation. arXiv:2505.06120.                         Hamish Ivison, Shengyi Huang, Pradeep Dasigi,
  Nathan Lambert, and Hannaneh Hajishirzi. 2025.             Systematic Construction of Constrained Text Genera-
  Generalizing Verifiable Instruction Following. In          tion Tasks. In Proceedings of the 12th International
  Proceedings of the 39th Annual Conference on Neu-          Conference on Learning Representations (ICLR’24).
  ral Information Processing Systems (NeurIPS’25).
                                                           Richard J. Young, Brandon Gillins, and Alice M.
Yunjia Qi, Hao Peng, Xiaozhi Wang, Amy Xin,                  Matthews. 2025. When Models Can’t Follow:
  Youfeng Liu, Bin Xu, Lei Hou, and Juanzi Li.               Testing Instruction Adherence Across 256 LLMs.
  2025. AGENTIF: Benchmarking Instruction Follow-            arXiv:2510.18892.
  ing of Large Language Models in Agentic Scenarios.
  arXiv:2505.16944.                                        Weizhe Yuan, Ilia Kulikov, Ping Yu, Kyunghyun Cho,
                                                            Sainbayar Sukhbaatar, Jason E Weston, and Jing
Yiwei Qin, Kaiqiang Song, Yebowen Hu, Wenlin Yao,           Xu. 2025. Following Length Constraints in Instruc-
  Sangwoo Cho, Xiaoyang Wang, Xuansheng Wu, Fei             tions. In Proceedings of the 2025 Conference on
  Liu, Pengfei Liu, and Dong Yu. 2024. InFoBench:           Empirical Methods in Natural Language Processing
  Evaluating Instruction Following Ability in Large         (EMNLP’25).
  Language Models. arXiv:2401.03601.
                                                           Zhiyuan Zeng, Jiatong Yu, Tianyu Gao, Yu Meng, Tanya
Ved Sirdeshmukh, Kaustubh Deshpande, Johannes                Goyal, and Danqi Chen. 2024. Evaluating Large Lan-
  Mols, Lifeng Jin, Ed-Yeremai Cardona, Dean Lee,            guage Models at Evaluating Instruction Following.
  Jeremy Kritz, Willow Primack, Summer Yue, and              In Proceedings of The 12th International Conference
  Chen Xing. 2025. MultiChallenge: A Realistic Multi-        on Learning Representations (ICLR’24).
  Turn Conversation Evaluation Benchmark Challeng-
  ing to Frontier LLMs. arXiv:2501.17399.                  Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu,
                                                             Zhiguang Han, Jingyang Zhang, Beibin Li, Chi
Xiaofei Sun, Xiaoya Li, Jiwei Li, Fei Wu, Shangwei           Wang, Huazheng Wang, Yiran Chen, and Qingyun
  Guo, Tianwei Zhang, and Guoyin Wang. 2023. Text            Wu. 2025a. Which Agent Causes Task Failures
  Classification via Large Language Models. In Find-         and When? On Automated Failure Attribution of
  ings of the Association for Computational Linguistics:     LLM Multi-Agent Systems. In Proceedings of The
  EMNLP 2023 (EMNLP’23).                                     42nd International Conference on Machine Learning
                                                             (ICML’25).
Mandana Vaziri, Louis Mandel, Claudio Spiess, and
 Martin Hirzel. 2024. PDL: A Declarative Prompt            Yedi Zhang, Yufan Cai, Xinyue Zuo, Xiaokun Luan,
 Programming Language. arXiv:2410.19135.                     Kailong Wang, Zhe Hou, Yifan Zhang, Zhiyuan Wei,
                                                             Meng Sun, Jun Sun, Jing Sun, and Jin Song Dong.
Bosi Wen, Pei Ke, Xiaotao Gu, Lindong Wu, Hao                2025b. Trustworthy AI Agents Require the Integra-
  Huang, Jinfeng Zhou, Wenchuang Li, Binxin Hu,              tion of Large Language Models and Formal Methods.
  Wendy Gao, Jiaxin Xu, Yiming Liu, Jie Tang, Hongn-         In Proceedings of 42nd International Conference on
  ing Wang, and Minlie Huang. 2024. Benchmarking             Machine Learning (ICML’25).
  Complex Instruction-Following with Multiple Con-
  straints Composition. In Proceedings of the 38th An-     Wenting Zhao, Xiang Ren, Jack Hessel, Claire Cardie,
  nual Conference on Neural Information Processing          Yejin Choi, and Yuntian Deng. 2024. WildChat: 1M
  Systems (NeurIPS’24).                                     ChatGPT Interaction Logs in the Wild. In Proceed-
                                                            ings of The 12th International Conference on Learn-
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu,            ing Representations (ICLR’24).
  Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang,
  Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah,        Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Tianle
  Ryen W White, Doug Burger, and Chi Wang. 2024a.            Li, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang,
  AutoGen: Enabling Next-Gen LLM Applications via            Zhuohan Li, Zi Lin, Eric P. Xing, Joseph E. Gonzalez,
  Multi-Agent Conversation. In Proceedings of the 1st        Ion Stoica, and Hao Zhang. 2024. LMSYS-Chat-
  Conference on Language Modeling (COLM’24).                 1M: A Large-Scale Real-World LLM Conversation
                                                             Dataset. In Proceedings of The 12th International
Xiaodong Wu, Minhao Wang, Yichen Liu, Xiaom-                 Conference on Learning Representations (ICLR’24).
  ing Shi, He Yan, Xiangju Lu, Junmin Zhu, and
  Wei Zhang. 2024b. LIFBench: Evaluating the In-           Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  struction Following Performance and Stability of           Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Large Language Models in Long-Context Scenarios.           Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
  arXiv:2411.07037.                                          Joseph E. Gonzalez, and Ion Stoica. 2023. Judg-
                                                             ing LLM-as-a-Judge with MT-Bench and Chatbot
John Yang, Kilian Lieret, Carlos E. Jimenez, Alexander       Arena. In Proceedings of the 37th Annual Con-
  Wettig, Kabir Khandpur, Yanzhe Zhang, Binyuan Hui,         ference on Neural Information Processing Systems
  Ofir Press, Ludwig Schmidt, and Diyi Yang. 2025.           (NeurIPS’23).
  SWE-smith: Scaling Data for Software Engineering
  Agents. arXiv:2504.21798.                                Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha
                                                              Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and
Shunyu Yao, Howard Chen, Austin W. Hanjie, Run-               Le Hou. 2023. Instruction-Following Evaluation for
  zhe Yang, and Karthik Narasimhan. 2024. COLLIE:             Large Language Models. arXiv:2311.07911.
Tao Zou, Xinghua Zhang, Haiyang Yu, Minzheng Wang,   A     Details of V IF B ENCH
  Fei Huang, and Yongbin Li. 2025. EIFBENCH: Ex-
  tremely Complex Instruction Following Benchmark    Table 5 provides detailed descriptions of the constraints
  for Large Language Models. In Proceedings of the   used in V IF B ENCH and their representation in the in-
  2025 Conference on Empirical Methods in Natural    structions. The benchmark contains 820 instructions
  Language Processing (EMNLP’25).                    on freeform English writing tasks. Each instruction
                                                     contains 2 to 10 constraints from Table 5.

                                                     A.1   Constraints in V IF B ENCH
                                                     Constraint types in V IF B ENCH are sourced from
                                                     instruction-turning datasets and instruction-following
                                                     evaluation benchmarks (Köpf et al., 2023; Zheng et al.,
                                                     2024; Zhao et al., 2024; Wen et al., 2024; Zhou et al.,
                                                     2023; Qin et al., 2024). For each type of constraint,
                                                     we use GPT-4.1 to generate constraint values. For ex-
                                                     ample, for the writing topic constraint, we prompt the
                                                     LLM to generate 15 different writing topics, including
                                                     agile project management or technology in education.
                                                     Because it is rather abrupt to directly concatenate con-
                                                     straint values into an instruction, we write prompt tem-
                                                     plates for each constraint type. For example, for writing
                                                     topic, the prompt template is “Please write in this topic:
                                                     <topic>”. To make the English writing task logically
                                                     coherent, we also group certain constraints together. In
                                                     V IF B ENCH, keyword inclusion, keyword exclusion, ti-
                                                     tle, and subsection title constraints are grouped together
                                                     by writing topics. Other constraints are independent of
                                                     each other. Figure 6 shows an example of constraints
                                                     grouped by the agile project management topic.

                                                      Topic: The benefits of agile project management
                                                      Include keywords: scrum, kanban, iterative delivery,
                                                      sprint velocity, stakeholder feedback, backlog
                                                      prioritization, time-to-market, continuous
                                                      improvement, cross-functional teams, adaptability
                                                      Exclude keywords: waterfall methodology, gantt
                                                      charts, pert, critical path method, stage-gate, prince2,
                                                      heavy documentation, iso 9001, rigid scope, cmmi
                                                      Title: Unlocking Success: The Benefits of Agile
                                                      Project Management
                                                      Subsection Titles:
                                                      - Introduction to Agile Principles
                                                      - Key Advantages Over Traditional Methodologies
                                                      - Enhancing Team Collaboration and Communication
                                                      - Faster Delivery and Adaptability
                                                      - Continuous Improvement Through Iterations
                                                      - Stakeholder Engagement and Feedback
                                                      - Case Studies of Agile Success

                                                     Figure 6: Example of grouped constraints for the writing
                                                     topic “The benefits of agile project management”.


                                                     A.2   Instruction Synthesis and Output Generation
                                                     We synthesize instructions by complexity group, which
                                                     is the total number of constraints we intend to include
                                                     in an instruction.
                                                        Each constraint in Table 5 appears only once in the in-
                                                     struction. For each complexity group with C constraints,
                                   Table 5: Constraints included in V IF B ENCH
 Constraint Type                        Constraint Name                           Constraint Text
 Semantic - Misinterpretation           Writing tone                             Please write in this tone: <tone>
 Semantic - Pragmatic mismatch          Writing topic                            Please write in this topic: <topic>
                                                                                 Include these keywords, check for
 Logic - Invalid element                Keyword inclusion                        string inclusion regardless of capitaliza-
                                                                                 tion: <keywords>
                                                                                 Exclude these keywords, check for
 Logic - Invalid element                Keyword exclusion                        string exclusion regardless of capital-
                                                                                 ization: <keywords>
                                                                                 Include this as the title of the text, ti-
 Logic - Structural violation           Response title                           tles are lines that start with only one #:
                                                                                 <title>
                                                                                 Include these subsection titles in the
 Logic - Structural violation           Response subsection title                text, subsection titles are lines start with
                                                                                 more than one #: <subsection titles>
                                                                                 Please consider this number of words
                                                                                 per sentence constraint: <num_words>,
 Logic - Constraint violation           Number of words per sentence             this does not apply to title and subsec-
                                                                                 tion title lines. Title and subsection title
                                                                                 lines start with at least one #.
                                                                                 Please consider this even/odd word
                                                                                 count constraint: <even_odd> this does
 Logic - Constraint violation           Even or odd word count                   not apply to title and subsection title
                                                                                 lines. Title and subsection title lines
                                                                                 start with at least one #.
                                                                                 Please consider this word repetition con-
                                                                                 straint on the entire response: <word_-
                                        Response start and end with the same
 Logic - Constraint violation                                                    rep>, this does not apply to title and
                                        word
                                                                                 subsection title lines. Title and subsec-
                                                                                 tion title lines start with at least one #.
                                                                                 Please consider this word repetition con-
                                                                                 straint on subsections of the response:
                                        Response subsections start and end       <word_rep>, this does not apply to title
 Logic - Constraint violation
                                        with the same word                       and subsection title lines. Title and sub-
                                                                                 section title lines start with at least one
                                                                                 #.



we calculate the Cartesian product of all possible com-        Please write a piece of text considering all these
binations of constraint values over the chosen constraint      constraints:
types. For example, when C = 2, we choose writing              Please write in this topic: the benefits of agile project
topic and total word count as the constraint types. There      management
are 15 writing topics and 10 word count options, result-       Please consider this word count constraint: “around
ing in 15 × 10 = 150 possible combinations. If the             500 words, this does not apply to title and subsection
total number of combinations exceeds 100, we collect           title lines, which are defined as: lines that start with at
the first 100 combinations. When C ∈ {5, 6}, we ex-            least one #.”
hausted all possible values of the chosen constraints and
got 60 instructions. Then, we concatenate the constraint     Figure 7: Example of an instruction in complexity group
values together using their prompt templates. To avoid       C = 2.
confusing the verifiers, we add specifiers such as “this
does not apply to title and subsection title lines”. Fig-
ure 7 shows an example of the concatenated constraint        straints. Logic constraints can be statically checked by
values as an instruction for C = 2, with “The benefits       Python programs. Thus, we prioritize checking logic
of agile project management” as the writing topic and a      constraints in output generation to judge whether the
total word count of around 500 words.                        response is sat or unsat. In rounds of generating
                                                             sat responses, we prompt the LLM to generate a re-
   We use GPT-4.1 to generate responses for each in-         sponse. If the initial attempt fails the checker programs,
struction in V IF B ENCH. To balance the dataset, we         we provide the error messages to LLM and ask it to re-
generate sat and unsat responses alternatively. Se-          vise the response until it passes all checks. In rounds of
mantic constraints are judged by sampling outputs and        generating unsat responses, we mutate the instruction
discussion between authors after output generation. We       in a way that the output violates the constraints. We
sample 10% of the outputs for each complexity group          mutate the instruction by omitting one logic constraint,
and check whether they comply with the semantic con-         but the output is also likely to violate more than one
        constraint (as shown by Figure 8). If the output still                         A.4   Example Cases
        satisfies the constraints, we prompt the LLM again un-                         Figure 9 demonstrates an unsat output from V IF -
        til an unsat response is generated. The re-generation                          B ENCH in complexity group C = 4. Here, the logic
        budget for both sat and unsat responses is 5. If the                           constraint total word count is violated as the output only
        budget is exhausted, we keep the output as-is. We aim                          contains 239 words, much less than the required 540
        to create a balanced benchmark with relatively equal                           words. Figure 10 presents another unsat output from
        numbers of sat and unsat responses across all com-                             V IF B ENCH in complexity group C = 7. The output
        plexity groups. Among the 820 instruction-output pairs                         violates the number of words per sentence constraint, as
        in V IF B ENCH, 391 (47.68%) of them have sat outputs                          many sentences contain more than 8 words. We high-
        and 429 (52.32%) have unsat outputs.                                           light the first sentence that violates the constraint in the
        A.3                        Category Distribution                               figure.

      We categorize V IF B ENCH into complexity groups based                           A.5   Evaluation Setup
      on the number of constraints C in each instruction. Ta-                          We run all models with temperature 0.2. The parame-
      ble 6 presents the characteristics of each group.                                ters used to run GEPA is as follows: max_full_evals=1,
                                                                                       num_threads=1, reflection_minibatch_size=3.
       Table 6: Distribution of constraints across different com-
       plexity levels (C).                                                              Table 7: Token usage for evaluations on V IF B ENCH.

                             Comp        N   A B C D E F G H                 I   J K       Model         Verifier         Input       Output
                               2      100    ✓ ✓                                                       N SVIF       130209094 6665927
                               3      100    ✓ ✓ ✓                                                     N SVIF -N EU 1221770    675457
                               4      100    ✓ ✓ ✓ ✓                                       GPT-4.1     Baseline       812081    5824
                               5       60    ✓   ✓ ✓ ✓ ✓                                               GEPA-C OT 1393786       1236345
                               6       60    ✓   ✓ ✓ ✓ ✓ ✓                                             C ONV-C OT    1011663   642667
                               7      100    ✓   ✓ ✓ ✓ ✓ ✓ ✓                                           N SVIF        49313969 5350435
                               8      100    ✓   ✓ ✓ ✓ ✓ ✓ ✓ ✓                             GPT-4o
                                                                                                       Baseline       812081    5893
                               9      100    ✓   ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓                                       N SVIF        51336048 5002967
                              10      100    ✓   ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓                         GPT-4o-mini
                                                                                                       Baseline       812081    5875
                                                                                                       N SVIF        49765953 61923653
                                                                                           DS-R1
             Legend: Comp: Complexity group; N : Number of                                             Baseline       812081    6279
         instructions in each group; A: Writing topic; B: Total word                                   N SVIF        56019153 6053348
                                                                                           DS-V3.1
        count; C: Writing tone; D: Keyword inclusion; E: Keyword                                       Baseline       812081    6208
        exclusion; F: Response title; G: Response subsection titles;                                   N SVIF        51915290 6219118
                                                                                           Qwen3-Max
        H: Number of words per sentence; I: Even or odd word count;                                    Baseline       812081    6009
        J: Response start and end with the same word; K: Response
               subsections start and end with the same word.
                                                                                          Table 7 shows the token usage for each model under
           Figure 8 illustrates the distribution of constraint viola-                  different verification methods on V IF B ENCH. GPT-4.1,
        tions in V IF B ENCH. We observe that after mutation of                        GPT-4o, GPT-4o-mini, DeepSeek-R1, and DeepSeek-
        instructions to generate unsat responses, the most fre-                        V3.1 are provided by Azure AI Foundry. Qwen3-Max
        quently violated constraints are total word count, num-                        is provided by Alibaba Cloud. All models are queried
        ber limit on words per sentence, and response starting                         through their provider’s API interface.
        and ending with the same words. Total word count and
        limit on words per sentence showcase that such invari-                         B     Prompts of N SVIF and Baselines
        ants are challenging for LLMs to comply with.
                                                                                       We list all the prompts used in the three agents of N SVIF.
                             160                                                       We also list prompts from GEPA-C OT, C ONV-C OT,
                             140                                                       and the baseline. Finally, we include the travel agent
# of Constraint Violations




                             120                                                       prompt for the task.
                             100
                              80
                              60
                              40
                              20
                               0
                                     B       H   J   E      G       K    D   F    I
                                                     Logic Constraints

        Figure 8: Distribution of constraint violations in V IF -
        B ENCH.
  Instruction:
  Please write a piece of text considering all these constraints:
  Please write in this topic: the benefits of agile project management
  Please write in this tone: pessimistic
  Include these keywords, check for string inclusion regardless of capitalization: scrum,kanban,iterative deliv-
  ery,sprint velocity,stakeholder feedback,backlog prioritization,time-to-market,continuous improvement,cross-functional
  teams,adaptability
  Please consider this word count constraint: around 540 words (within 10 words difference is ok), this does not apply to
  title and subsection title lines, which are defined as: lines that start with at least one #.

  Output:
  Agile project management promises a smoother ride, but most days it feels like trading one set of problems for another.
  Still, in the bleak light of experience, a few benefits manage to limp through.

  - Faster time-to-market, though “faster” often means shipping a smaller slice sooner and apologizing for the rest later.
  - Smaller batches and iterative delivery reduce the scale of disasters, even if they increase their frequency.
  - Lightweight frameworks like scrum and kanban provide just enough structure to prevent freefall, while adding ceremonies
   that nobody has time for.
  - Relentless backlog prioritization keeps the most important work visible, assuming priorities don’t change twice before
   lunch.
  - Tracking sprint velocity offers predictability, until it becomes a scoreboard that invites gaming more than improvement.
  - Early and frequent stakeholder feedback can save you from building the wrong thing, at the small cost of rework, scope
   creep, and moving targets.
  - cross-functional teams shorten handoffs and improve context sharing, right up until calendars fill with coordination
   meetings.
  - Hard-won adaptability helps teams pivot under pressure, which is convenient when the strategy pivots every other week.
  - Rituals of continuous improvement catch slow-burning issues before they explode, while reminding everyone that
   perfection remains permanently out of reach.

  Even in this dim view, the benefits are real enough: fewer late surprises, slightly saner delivery, and a system that bends
  before it breaks. Just don’t expect miracles-only marginal gains wrestled from chaos.


Figure 9: An <instruction, output> pair with an unsat output in V IF B ENCH. Total word count constraint is the
violated logic constraint.
  Instruction:
  Please write a piece of text considering all these constraints:
  Please write in this topic: the benefits of agile project management
  Please write in this tone: optimistic
  Include these keywords, check for string inclusion regardless of capitalization: scrum,kanban,iterative deliv-
  ery,sprint velocity,stakeholder feedback,backlog prioritization,time-to-market,continuous improvement,cross-functional
  teams,adaptability
  Exclude these keywords, check for string exclusion regardless of capitalization: waterfall methodology,gantt
  charts,pert,critical path method,stage-gate,prince2,heavy documentation,iso 9001,rigid scope,cmmi
  Include this as the title of the text, titles are lines that start with only one #: Unlocking Success: The Benefits of Agile
  Project Management
  Include these subsection titles in the text, subsection titles are lines start with more than one #: Introduction to Agile
  Principles,Key Advantages Over Traditional Methodologies,Enhancing Team Collaboration and Communication,Faster
  Delivery and Adaptability,Continuous Improvement Through Iterations,Stakeholder Engagement and Feedback,Case
  Studies of Agile Success
  Please consider this number of words per sentence constraint: each sentence should have less than 8 words., this does not
  apply to title and subsection title lines. Title and subsection title lines start with at least one #.

  Output:
  # Unlocking Success: The Benefits of Agile Project Management

  ## Introduction to Agile Principles
  Agile project management thrives on transparency, collaboration, and learning, empowering teams to deliver value early
  and often. Practices like scrum and kanban create focus and flow, enabling iterative delivery that adapts to changing
  needs. With cross-functional teams working closely, agility fosters adaptability, encourages creative problem-solving, and
  accelerates outcomes in a confident, forward-looking way.

   ## Key Advantages Over Traditional Methodologies
  Agile shines by prioritizing customer value and incremental progress. Teams use backlog prioritization to ensure the
   most impactful work is addressed first, guided by data such as sprint velocity to forecast and optimize throughput. This
   approach shortens time-to-market, invites stakeholder feedback throughout the process, and builds momentum through
   continuous improvement, allowing teams to pivot quickly while maintaining clarity on goals.
   ## Enhancing Team Collaboration and Communication
   Cross-functional teams break down silos and bring diverse expertise together, aligning around shared objectives and
   transparent workflows. Daily touchpoints and visible work queues, commonly supported by scrum or kanban practices,
   keep everyone informed and engaged. The result is stronger communication, faster decision-making, and a positive team
   culture grounded in ownership, learning, and adaptability.
   ## Faster Delivery and Adaptability
   By embracing iterative delivery, teams release value in smaller increments, validate assumptions early, and respond
   swiftly to new insights. Measuring sprint velocity helps balance capacity and ambition, sustaining a healthy pace without
   sacrificing quality. This rhythm reduces risk, improves time-to-market, and enables proactive adjustments that maintain
   momentum even as priorities evolve.
   ## Continuous Improvement Through Iterations
  Agile teams celebrate wins and learn from challenges, embedding continuous improvement into every cycle. Retrospectives
   reveal opportunities to refine processes, strengthen collaboration, and streamline tools. Over time, these incremental
   enhancements compound, elevating performance and resilience while keeping the team optimistic, curious, and ready to
   adapt.
   ## Stakeholder Engagement and Feedback
   Frequent demos and reviews invite meaningful stakeholder feedback, ensuring solutions address real needs and deliver
   tangible outcomes. Backlog prioritization evolves with input, aligning the roadmap to maximize value and minimize waste.
  This ongoing dialogue fosters trust, reduces rework, and accelerates discovery, helping teams make confident decisions
  with clarity and purpose.
   ## Case Studies of Agile Success
  - A health-tech startup adopted scrum with a kanban workflow to improve visibility and flow. Within three months, sprint
  velocity increased by 25%, time-to-market was cut in half, and stakeholder feedback guided features that boosted patient
   engagement.
  - An e-commerce team introduced iterative delivery for checkout optimization, using backlog prioritization to tackle the
   highest-impact improvements first. Conversion rates rose steadily while continuous improvement reduced defects and
   cycle time.
  - A global SaaS organization reorganized into cross-functional teams, emphasizing adaptability and regular customer
   touchpoints. With better forecasting and faster feedback loops, major releases shipped earlier, and customer satisfaction
   climbed quarter over quarter.


Figure 10: An <instruction, output> pair with an unsat output in V IF B ENCH. Number of words per sentence
constraint is violated. Highlighted in red is the violating sentence.
N SVIF Prompt                                                                  Formulation Agent - System Prompt

Devise a neurosymbolic workflow-composed of neural-focused and symbolic-focused modules-to verify problems containing
       neural, symbolic, or combined constraints. For every constraint in the problem, explicitly identify and list a
      module that can independently verify the constraint without requiring additional input from other modules.
      Ensure that your workflow carefully assigns each constraint to a dedicated verification module, such that each
      module's input is fully determined by the overall problem statement, not by outputs of other modules (except
      where dependencies must arise from constraint logic itself).

When classifying a constraint as 'symbolic', only count constraints that can be easily checked statically with simple
       Python static checker functions. Make clear when a constraint qualifies as symbolic by this standard in your
      reasoning steps. Always use the symbolic constraint_verifier (via Python first-party libraries) for such
      constraints. For qualitative, subjective, or neural constraints, employ an LLM prompt as the neural
      constraint_verifier (e.g., LLM or classifier).

Design the workflow as a clear, ordered sequence of modules, each specifying: its type (neural or symbolic), its
      function, which constraint(s) it independently verifies, the specifications for verifying the constraint for the
       module, and its input/output. Do not bias toward using only one tool; instead, break down the problem so each
      module leverages the most suitable verification method. If a constraint is ambiguous or could be processed by
      either module type, safely fall back to classifying it as a neural constraint.

Carefully and faithfully parse constraints from the given problem. Avoid inferring implicit constraints from the
      natural language problem. Only parse constraints that are explicitly stated in the problem statement. Don't come
       up with constraints that do not appear in the problem statement.

When designing the workflow, CLEARLY SPECIFY the specifications for the constraint to be satisfied by each module.
      Especially for symbolic constraints, clearly specify the criteria and standards for the answer to satisfy the
      constraint generated from the given instruction.

When designing the workflow for constraints, you MUST consider how each constraint can affect each other. One single
      constraint can enforce a global precondition that, for other constraints, you must check this global constraint
      before checking other constraints individually. For example, if one of the constraints is about language used in
       the output, you must consider this constraint while generating modules for other individual constraints.

You will also be given the answer of the problem to help you plan your workflow.

**Reasoning and Output Order Requirements**
- For each constraint:
    - State which module independently verifies it and why, requiring no additional module inputs if possible.
    - State the specifications of the constraint mentioned in the instruction to show how to verify the constraint
    - If a constraint cannot be split off this way, clarify why.
- Reason step by step about:
    - Identification/classification of each constraint as symbolic/neural, using the formalizability standard for
      symbolic.
    - The specifications to verify each constraint.
    - Selection and justification of an independent constraint_verifier module for each constraint.
    - Order and dependency of modules (which constraints or verifications must come first, and why).
- Never output workflow modules or conclusions before providing full reasoning. Always show reasoning and constraint-
      module mapping clearly before the list of modules.
- Carefully and faithfully parse constraints from the given problem. Avoid inferring implicit constraints from the
      natural language. Only parse constraints that are explicitly stated in the problem statement.

**Workflow construction requirements:**
- For every module:
    - Explicitly state **Module Type** (neural or symbolic)
    - Briefly describe **Purpose/Function**
    - Specify **Constraint(s) Addressed** (independent verification)
    - Specify **Constraint Specifications** that how to verify the constraint through the given instruction
    - Clarify **Input/Output** for the module (only using information from the original problem or verified outputs
      if dependencies exist) to support the constraint specifications above
- Present an ordered, numbered list of modules (the workflow), after reasoning about:
    - Why each module is needed, referencing the independent verification of each constraint
    - The sequence (which constraints must be satisfied first, dependencies, etc.)
- Do not output code, but describe what the code/tool(s) would accomplish at each step.
- If multiple modules could process the same constraint, clarify choice.
- Output as a structured JSON with two sections:
    - "reasoning_steps": An ordered list, explaining detailed reasoning and mapping of each constraint to a
      verification module; include classification, tool selection, and justification of module order
    - "workflow": An ordered list where each item is an object with "module_type", "purpose", "constraints_addressed
      ", "module_specification", and "input_output"
- Always provide "reasoning_steps" before the workflow in the output.
- Never output conclusions or the finalized workflow before the full reasoning.

**Examples**

---

### Example 1

**Input:**
"Write 10 funny poems."

**Output:**
{{
  "reasoning_steps": [
    "Identifying constraints: (1) The output must be exactly 10 poems (symbolic), and (2) each poem must be funny (
      neural).",
    "Checking if each constraint can be assigned an independent module: The quantitative constraint can be
      independently checked by counting poems (symbolic module). Each poem's funniness can be separately verified by a
       neural classifier, independently of other constraints.",
    "Validating symbolic constraint: The count of items can be formalized in code (e.g., check list length).",
    "Validating neural constraint: 'Funny' is subjective and cannot be statically checked, so a neural
      constraint_verifier is required.",
    "Optimal order: Count check should come first to ensure the correct number of items before running neural checks
      on each.",
    "Each constraint is mapped to an independent module. No module requires input from another, except to ensure the
      correct number of items are available for the neural check."
  ],
  "workflow": [
    {{
      "module_type": "symbolic",
      "purpose": "Verify that exactly 10 poems are present.",
      "constraints_addressed": "Quantitative constraint: exactly 10 poems.",
      "module_specification": "The module should count the number of poems and compare that with 10.",
      "input_output": "Input: list/block of poems; Output: pass/fail plus list of poems (if pass)."
    }},
    {{
      "module_type": "neural",
      "purpose": "Verify that each poem is funny using a neural classifier.",
      "constraints_addressed": "Qualitative (neural) constraint: each poem should be funny.",
      "module_specification": "The module should generate a prompt that prompts an LLM to inspect whether each poem
      is funny",
      "input_output": "Input: set of 10 poems; Output: Boolean/classification for each poem."
    }}
  ]
}}
---

### Example 2

**Input:**
"Given x in [0,5], verify that x^2 + 2x >= 7."

**Output:**
{{
  "reasoning_steps": [
    "There is a single constraint: x^2 + 2x >= 7, valid for all x in [0,5].",
    "Checking formalizability: This constraint is fully formalizable and can be statically checked, as it involves an
       algebraic inequality.",
    "No neural or qualitative aspects are present; only a symbolic module is required.",
    "Independent verification: This symbolic constraint can be wholly verified by a single module with no
      interdependencies."
  ],
  "workflow": [
    {{
      "module_type": "symbolic",
      "purpose": "Express the variable's domain and the inequality in Python, and check if the constraint holds for
      all x in [0,5].",
      "constraints_addressed": "Symbolic constraint: x^2 + 2x >= 7 for x in [0,5], statically checkable through
      Python first-party libraries.",
        "module_specification": "The module should generate a python program that statically checks whether the
        inequality holds for all x.",
        "input_output": "Input: variable domain and expression; Output: proof status or counterexample."
      }}
  ]
}}
---

**Important Reminders**
- For each constraint, list a module that can independently verify it, with required inputs entirely determined by
      the original problem statement, unless dependencies are dictated by constraint logic.
- Only count as a symbolic constraint if the constraint can be easily statically checked with Python first-party
      libraries.
- Show step-by-step reasoning and module mapping before the final workflow. Output must be JSON, "reasoning_steps"
      section must always come first, followed by "workflow".
- Never begin with or interleave conclusions or modules before reasoning.
- You will also be given the answer of the problem to help you plan your workflow.

# Output Format

Your output must be a valid JSON object with two fields in this order:
- "reasoning_steps": an ordered list of step-by-step reasoning, constraint classification, mapping, and module
      sequence justification as described above.
- "workflow": an ordered (numbered) list, each element an object with "module_type", "purpose", "
      constraints_addressed", "module_specification", and "input_output".

No non-JSON content should be present.

---

**REMINDER**
When designing the workflow for constraints, you MUST consider how each constraint can affect each other. One single
      constraint can enforce a global precondition that, for other constraints, you must check this global constraint
      before checking other constraints individually.
For each constraint in the input, always specify a module that can independently verify it. Only treat a constraint
      as symbolic if it can be statically checked by Python first-party libraries. Provide step-by-step reasoning
      first, then the workflow as described above, both ordered and presented in JSON format. Never output code; only
      structure and describe the verification logic. Keep outputs clear and structured, always beginning with
      reasoning. You will also be given the answer of the problem to help you plan your workflow.




N SVIF Prompt                                                                      Formulation Agent - User Prompt

Here's the question:
{question}

Here's the answer:
{answer}




N SVIF Prompt                                                                        Checking Agent - System Prompt

Write a Python constraint verifier module such that the output is a fully executable, stand-alone Python script. The
      module will be run directly by a Python interpreter, so your generated code must include all imports, helper
      function definitions, variable assignments, constants, and values needed for independent execution-no referenced
       name or function may be undefined or require any external context. If you output a function, make sure to
      include a function call with all necessary parameter values and a print statement to print the output of the
      call.

Given:
- A "problem" (the question)
- An "answer" (the proposed solution)
- A JSON object specifying how to evaluate one constraint in the input instruction
- A python program that represents the constraint dependencies like a graph.

Your task for the given input:
- For the given module design in the "workflow" json array, generate a fully self-contained, executable Python
      program, including:
    - ALL necessary import statements (inside the function/module code).
    - ALL helper functions or objects, defined inline.
    - All variables, constants, and values required for successful execution.
        - Include a function call with all necessary parameter values and a print statement to print the output of
      the call. When including values, use the provided answer as parameter values.
    - For neural constraints: clearly and visibly build a string variable, "prompt", containing the full natural
      language instruction to the LLM, incorporating the constraint, the question, and the answer. Include ONLY the
      actual prompt message in the string variable. The prompt message should be formulated such that, the LLM answers
       YES to show the constraint is *satisfied*, NO to show that the constraint is *not satisfied*.
    - For symbolic constraints: you must output "sat" if the module's verification result that the answer satisfies
      the question, "unsat" otherwise.
    - For both neural and symbolic constraints, you MUST use the original answer in your verifier_module. In symbolic
       module, you MUST use the original provided answer to build the static checker. In neural module, you MUST
      include the original provided answer in the natural language instruction.
    - The constraint graph represents the dependency relationship between constraints as a graph. To find the related
       dependency, find all related paths that includes the constraint node which encodes the constraint verified by
      the given module design. You MUST consider the constraint verified by the module design WITH RESPECT TO the
      constraint graph.
    - The output program must include the given "answer" to ensure soundness of checking results.
- The "workflow" json object contains specifications for ONLY ONE constraint. ONLY output ONE constraint verifier
      module based on the provided workflow json array.
- For symbolic constraints, build a static checker with Python's first-party syntax structures and functions. You
      MUST print either "sat" or "unsat" at the end of the output program, depending on the static checker's result.
      Do NOT use regular expression as it is not resilient to different input formats.
- DO NOT reference, import, or call any function/object not defined in the same module output-every helper, utility,
      or reference must be defined and included inside the module (no omissions, no assumptions). Include a function
      call with all necessary parameter values and a print statement to print the output of the call. When including
      values, use the provided answer as parameter values.
- For symbolic constraints, the static checker should take in only one argument -- the LLM answer. The static checker
       should solely operate on the answer itself to verify any constraints, i.e., the function signature should only
      contain one argument, and the subsequent verifier function call should only pass in one argument -- the provided
       LLM "answer".
- For neural constraints, define a string variable `prompt` that includes the full natural language instruction to
      the LLM to verify this neural constraint, incorporating the constraint, the question, and the answer. This
      prompt needs to ask the LLM to provide a "Yes" or "No" answer as to whether the given response satisfies the
      constraints. This string **MUST** use triple quotes to prevent runtime errors that can occur if the strings
      contain single quotes ('), double quotes ("), or other special characters. You **MUST** use `prompt` as the
      variable name, any other name is not allowed. Your response should **ONLY** contain the definition of this
      prompt, and nothing else. The prompt message should be formulated such that, the LLM answers YES to show the
      constraint is *satisfied*, NO to show that the constraint is *not satisfied*.
- For both neural and symbolic constraints, you MUST use the provided, given "answer" in your verifier_module. In
      symbolic module, you MUST use the original provided "answer" to build the static checker, you MUST print either
      "sat" or "unsat" at the end of the output program, depending on static checker's result.. In neural module, you
      MUST include the original provided answer in the natural language instruction.
- The output program must include the given "answer" to ensure soundness of checking results.


Output only a single JSON object, conforming precisely to this schema:

- reasoning_steps: [empty string]
- workflow: [
    {{
        constraint_description: str (short human-readable summary of the constraint),
        constraint_type: "symbolic" or "neural",
        verifier_module: str (the complete, executable standalone Python code for the function including ALL helpers/
      imports/values-no undefined references, ready to run. For neural constraints, the string variable definition of
      the natural language instruction to the LLM.)
    }},
]

NO narrative text, NO comments, NO explanations outside the JSON-every verifier_module code string **MUST** be
      complete Python code and executable directly.

# Steps

1. Define a constraint_verifier function for the constraint that:
    - Includes ALL import statements.
    - Defines ALL necessary helper functions and values inline.
    - Contains logic to check ONLY this constraint, returning a boolean.
        - Include a function call with all necessary parameter values and a print statement to print the output of
      the call. When including values, use the provided answer as parameter values.
    - For neural constraints: explicitly constructs a prompt variable in code , never skipping or implying prompt
      construction. The prompt message should be formulated such that, the LLM answers YES to show the constraint is *
      satisfied*, NO to show that the constraint is *not satisfied*.
- For both neural and symbolic constraints, you MUST use the original answer in your verifier_module. In symbolic
      module, you MUST use the original provided answer to build the static checker. In neural module, you MUST
      include the original provided answer in the natural language instruction.
- DO NOT import 3rd party libraries. If modules fail to execute due to import errors, import a Python first-party
      library instead.
- The constraint graph represents the dependency relationship between constraints as a graph. To find the related
      dependency, find all related paths that includes the constraint node which encodes the constraint verified by
      the given module design. You MUST consider the constraint verified by the module design WITH RESPECT TO the
      constraint graph.
- Output the module for the ONLY constraint specified in the workflow json array.

2. Assemble the output JSON object as prescribed.

# Output Format

Produce a single valid JSON object with the exact following structure-NO text, comments, or narrative outside the
      object:
- reasoning_steps: [empty string]
- workflow: [
    {{
        constraint_description: str,
        constraint_type: "symbolic" or "neural",
        verifier_module: str (entire Python code block-imports, helpers, function-all included and complete. For
      neural constraints, the string variable definition of the natural language instruction to the LLM.)
    }}
]

Each verifier_module string is a full executable Python script for that module, ready for interpreter execution as-is
      . For neural constraints, the verifier_module string should be the string variable definition of the natural
      language instruction to the LLM.

(Real outputs must always include directly executable code for every module, with all helpers and imports defined
      inside each verifier_module. For complex parsing or extraction, use executable code. When including values, use
      the provided answer as parameter values. Neural modules must always assemble the natural language instruction
      prompt as a visible string variable and call the LLM judge helper.) The prompt message should be formulated such
       that, the LLM answers YES to show the constraint is *satisfied*, NO to show that the constraint is *not
      satisfied*.

# Notes

- The verifier_module must be executable on its own-include all imports, helpers, and required variables in the code
      string.
- DO NOT leave any reference or function undefined or assumed-ALL must be written inline.
- Output ONLY the JSON object-no prose, comments, or narrative outside the object.
- For symbolic constraints, use Python's first-party libraries where relevant to build the static checker and include
       imports and helpers in the function. You MUST print either "sat" or "unsat", depending on static checker's
      result. Do NOT use regular expression as it is not resilient to different input formats. You MUST print either "
      sat" or "unsat" at the end of the output program, depending on static checker's result.
- For neural constraints, explicitly assign prompt construction to a string variable and invoke the LLM judge helper
      as part of the code in the output string. ONLY OUTPUT THE VARIABLE CALLED "PROMPT" THAT INCLUDES THE LLM PROMPT
      FOR JUDGING. "prompt" should be like: prompt = "does this answer satisfy the constraint?"
- You MUST consider the constraint verified by the module design WITH RESPECT TO the constraint graph.
- Ensure your outputs can be run by a Python interpreter as-is, without any undefined names, missing imports, or
      incomplete helpers. If you output is a function, include a function call with all necessary parameter values and
       a print statement to print the output of the call. When including values, use the provided answer as parameter
      values. For neural constraints, the verifier_module should be the string variable definition of the natural
      language instruction to the LLM.
- DO NOT import 3rd party libraries. If modules fail to execute due to import errors, import a Python first-party
      library instead.
- For symbolic constraints, the static checker should take in only one argument -- the LLM answer. The static checker
       should solely operate on the answer itself to verify any constraints, i.e., the function signature should only
      contain one argument, and the subsequent verifier function call should only pass in one argument -- the provided
       LLM "answer".

REMINDER: Every verifier_module must be a fully self-contained, executable Python function, with EVERY helper and
      import defined internally. Output ONLY the required JSON object-never produce any prose or commentary outside it
      .




N SVIF Prompt                                                                        Checking Agent - User Prompt

Question:
{question}

Answer:
{answer}

JSON:
{orchestrator_planning_res}

Constraint Graph Code:
{constraint_graph_code}




N SVIF Prompt                                                                        Solver Agent - System Prompt

You are a first-order logic helper that generates z3 programs to verify constraints in a given instruction.
You will be given these values as inputs
  1. "instruction": A natural language instruction that contains some constraints you must verify.
  2. "nl_answer": A natural language answer to the instruction
  3. "parser_plan": A JSON object that includes "reasoning steps" (thought process of parsing the instruction into
      constraints) and "workflow" (individual verifier module designs)
  4. "module_verification_results": A plain text description that shows the results of individual verifier modules
      that try to verify "nl_answer" against the instruction. Some result will be False/No/Unsat, representing that
      the constraint is not satisfied. Some results will be True/Yes/Sat, representing that the constraint is
      satisfied.
  5. "constraint_graph": A python program that represents the constraint dependencies like a graph.

Your task:
Generate a first-order predicate logic formula that captures the entire given problem, including all constraints and
      their verification module results.
For each constraint extracted in the "parser_plan", use a first-order logic predicate to represent the constraint.
E.g., if the constraint is "num_hours > 2", use `is_num_hours_gt_2` as the predicate name.
In your formula, use existential and universal quantifiers to represent the relationship between constraints.
Use boolean variables to represent the actual satisfiability of the each of the constraints.
They should represent the results of individual verifier modules.

Then, generate a z3 program that encodes all constraints and their verification module results.
Encode the relationship between constraints with z3 operators, such as And, Or, Not, etc.
Also use boolean variables to represent the actual satisfiability of the each of the constraints.
This z3 program should be self-contained and complete. It will be executed as a script. Include all necessary
      verifier module results or question and answer values.
They should represent the results of individual verifier module.
In the program, print the result of the z3 program as "sat" or "unsat".

To enable z3 to correctly reflect that a "False" from a verifier module represents an unsatisfied constraint, you
      MUST first initialize each variable to True in your z3 program.
For example, if "a" is a boolean variable that represents an unsatisfied constraint, initialize it to "True" by:
      solver.add(a == True)
Then, assign the actual boolean value ("True" for sat, "False" for unsat) to the boolean variable. E.g., "solver.add(
      a == True), solver.add(b == True), solver.add(c == True)" for initialization, then "solver.add(a == False),
      solver.add(b == False), solver.add(c == False)" for actual verifier module results.
Thus, when they are set to False according to the real verifier module output, z3 will correctly recognized that the
      z3 constraints cannot be satisfied, thus reflecting that the instruction is not satisfied.
When you verify negative constraints, such as "not <constraint>", you must carefully consider how are the verifier
      modules verify that constraint.
If the verifier module has already considered the negative constraint, encoded with a normal boolean variable.
For example, if the constraint is "no more than 2 hours," encode it in a variable as "not_gt_2_hr = Bool()" in z3.
DO NOT add "NOT" to the beginning of the constraint in the solver, this will change the semantic of the constraint.
Similarly, if the module did not consider the negative constraint, encode it in a z3 boolean variable, then add NOT
      in front of it in the solver.
The constraint graph represents the dependency relationship between constraints as a graph. Individually verify each
      constraint by themselves loses their context and causes false positive/negatives. You MUST consider all the
      constraints verified by the module design WITH RESPECT TO the constraint graph when you generate the z3 program.
Task: Generate a json string with three keys: 'global_constraint_predicate', 'global_constraint_predicate_definitions
      ', and 'gcp_z3_program'. GENERATE ONLY JSON STRING. DO NOT INCLUDE ANY OTHER TEXT.
'global_constraint_predicate': the first-order predicate logic formula mentioned above.
'global_constraint_predicate_definitions': definitions of all the first-order logic predicates you included in the
      formula.
'gcp_z3_program': the z3 program mentioned above. The value of this key will be directly executed by a python
      interpreter. **MUST INCLUDE THE ANSWER VALUES OR VERIFIER MODULE RESULTS IN YOUR Z3 PROGRAM** Only output the
      raw Python code. Do not include any other text. Do not include any commentary, only output the python code.




N SVIF Prompt                                                                           Solver Agent - User Prompt

Now, since you have generated all modules, generate a first-order predicate logic formula that
captures the entire given problem, including all constraints and their verification module results.
For each constraint extracted in the modules, use a first-order logic predicate to represent the
constraint.
E.g., if the constraint is "num_hours > 2", use `is_num_hours_gt_2` as the predicate name.
In your formula, use existential and universal quantifiers to represent the relationship between
constraints.
Use boolean variables to represent the actual satisfiability of the each of the constraints.
They should represent the results of individual verifier modules
Generate a z3 program that encodes the entire given problem, including all constraints and their
verification module results.
Encode the relationship between constraints with z3 operators, such as And, Or, Not, etc.
Also use boolean variables to represent the actual satisfiability of the each of the constraints.
This z3 program should be self-contained and complete. It will be executed as a script. Include
all necessary verifier module results or question and answer values.
They should represent the results of individual verifier module.
In the program, print the result of the z3 program as "sat" or "unsat".
For your convenience, here's the original LLM question and answer:

Question:
{question}

Answer:
{answer}

Module results:
{individual_module_results}

Task: Generate a json string with three keys: 'global_constraint_predicate',
'global_constraint_predicate_definitions', and 'gcp_z3_program'.
The value of 'global_constraint_predicate' should be the first-order predicate logic formula
mentioned above.
The value of 'global_constraint_predicate_definitions' should be definitions of all the first-
order logic predicates you included in the formula.
The value of 'gcp_z3_program' should be the z3 program mentioned above. **MUST INCLUDE THE ANSWER
VALUES OR VERIFIER MODULE RESULTS IN YOUR Z3 PROGRAM**
Only output the Python code. Do not include any other text. Do not include any commentary, only
output the python code
GENERATE ONLY JSON STRING. DO NOT INCLUDE ANY OTHER TEXT.




N SVIF Prompt                                                                         N SVIF -N EU - System Prompt

You are a first-order logic helper that generates z3 programs to verify constraints in a given instruction.
You will be given these values as inputs
  1. "instruction": A natural language instruction that contains some constraints you must verify.
  2. "nl\_answer": A natural language answer to the instruction

Your task:
Generate a first-order predicate logic formula that captures the entire given problem, including all constraints and
      whether they are satisfied by the given answer.
Encode the relationship between constraints with z3 operators, such as And, Or, Not, etc.
For each constraint in the instruction, use a first-order logic predicate to represent the constraint.
E.g., if the constraint is "num\_hours > 2", use `is\_num\_hours\_gt\_2` as the predicate name.
In your formula, use existential and universal quantifiers to represent the relationship between constraints.
Use boolean variables to represent the actual satisfiability of the each of the constraints.
They should represent whether the constraint is satisfied or not by the nl\_answer.

Then, generate a z3 program that encodes all constraints and their results.
Encode the relationship between constraints with z3 operators, such as And, Or, Not, etc.
Also use boolean variables to represent the actual satisfiability of the each of the constraints.
This z3 program should be self-contained and complete. It will be executed as a script. Include all constraint
      results or question and answer values.
In the program, print the result of the z3 program as "sat" or "unsat".

To enable z3 to correctly reflect that a "False" from a verifier module represents an unsatisfied constraint, you
      MUST first initialize each variable to True in your z3 program.
For example, if "a" is a boolean variable that represents an unsatisfied constraint, initialize it to "True" by:
      solver.add(a == True)
Then, assign the actual boolean value ("True" for sat, "False" for unsat) to the boolean variable. E.g., "solver.add(
      a == True), solver.add(b == True), solver.add(c == True)" for initialization, then "solver.add(a == False),
      solver.add(b == False), solver.add(c == False)" for actual results.
Thus, when they are set to False according to the real verifier module output, z3 will correctly recognized that the
      z3 constraints cannot be satisfied, thus reflecting that the instruction is not satisfied.
When you verify negative constraints, such as "not <constraint>", you must carefully consider how to verify that
      constraint.

Task: Generate a json string with three keys: 'global\_constraint\_predicate', 'global\_constraint\_predicate\
      _definitions', and 'gcp\_z3\_program'. GENERATE ONLY JSON STRING. DO NOT INCLUDE ANY OTHER TEXT.
'global\_constraint\_predicate': the first-order predicate logic formula mentioned above.
'global\_constraint\_predicate\_definitions': definitions of all the first-order logic predicates you included in the
       formula.
'gcp\_z3\_program': the z3 program mentioned above. The value of this key will be directly executed by a python
      interpreter. **MUST INCLUDE THE ANSWER VALUES OR VERIFIER MODULE RESULTS IN YOUR Z3 PROGRAM** Only output the
      raw Python code. Do not include any other text. Do not include any commentary, only output the python code.




N SVIF Prompt                                                                               N SVIF -N EU - User Prompt

instruction:
{instruction}

nl\_answer:
{nl\_answer}




Baseline LLM-as-a-Verifier Prompt                                     Basic Two-Shot Prompt for LLM-as-a-judge

Here's an instruction and an answer to the instruction:
Instruction: {instruction}
Answer: {answer}

Produce a json that includes these keys:
"is_sat": A result that says whether the answer satisfies the instruction, either "sat" or "unsat"

Example Input:
Instruction: "Write a sentence about operating systems that does not include the word semaphore"
Answer: "Operating systems are software that manages hardware resources and application scheduling."

Example Output:
Output:
{{
  "is_sat": "sat"
}}

Example Input:
Instruction: "Write a sentence about operating systems that does not include the word semaphore"
Answer: "Operating systems are software that manages hardware resources and application scheduling. One signature
      feature of an operating system is semaphore-based concurrency."

Example Output:
Output:
{{
  "is_sat": "unsat"
}}

ONLY OUTPUT THE JSON, NOTHING ELSE




Baseline LLM-as-a-Verifier Prompt                                                     GEPA-C OT - System Prompt

Given an instruction-output pair, your task is to determine whether the output fully satisfies all explicit
      constraints and requirements specified in the instruction.

The instructions may specify a wide variety of constraints, including but not limited to:

- **Topic and Tone Requirements:** The output may be required to address a specific topic and/or use a specified tone
       (e.g., formal, informal). You must check that the output matches both the topic and the tone as described.

- **Keyword Inclusion/Exclusion:** The instruction may require that certain keywords or phrases be included or
      excluded from the output. For inclusion, check that each required keyword or phrase appears somewhere in the
      output, regardless of capitalization (case-insensitive, string match). For exclusion, verify that none of the
      forbidden keywords or phrases appear anywhere in the output, regardless of capitalization.

- **Structural Requirements:** The instruction may require the presence and formatting of a title (lines starting
      with only one #) and specific subsection titles (lines starting with more than one #). Check that the required
      title and subsection titles are present, formatted exactly as specified, and in the correct locations. Titles
      are defined as lines starting with only one #, and subsection titles as lines starting with more than one #.

- **Sentence Length Constraints:** The instruction may specify a maximum number of words per sentence, which applies
      only to sentences in the main body (excluding title and subsection title lines). For example, "each sentence
      should have less than 11 words" means that every sentence (excluding title and subsection title lines) must have
       strictly fewer than 11 words.

- **Word Count Constraints:** The instruction may specify a total word count constraint for the main body of the text
      , excluding title and subsection title lines. For example, "around 570 words, this does not apply to title and
      subsection title lines" means you must count only the words in lines that do not start with #, and check that
      the total is within the specified range or margin.

- **Word Repetition Constraints:** The instruction may require that the response start and end with the same word, or
       that each subsection start and end with the same word. Check these requirements exactly as stated.

- **Other Explicit Formatting or Content Requirements:** Any other explicit requirements stated in the instruction
      must be checked and enforced exactly as described.

**Your evaluation process:**
1. **Carefully read the instruction and identify all explicit constraints.** Pay close attention to which constraints
       apply to which parts of the text (e.g., main body, titles, subsection titles), and to any exclusions (such as
      word count or sentence length not applying to title/subsection title lines).

2. **Examine the output and check whether it satisfies each constraint exactly as specified.** For each constraint,
      reference the relevant part of the output and explain whether it is met.

3. **If any constraint is not fully met, the output does not satisfy the instruction.** Even minor violations (such
      as a single missing keyword, a sentence exceeding the specified length, or a word count outside the allowed
      range) mean the output fails.

4. **Output your reasoning, referencing each constraint and whether it is met.** Be thorough and explicit in your
      reasoning, listing each constraint and your findings.

5. **Output a final verdict:**
   - Output `True` if the output fully satisfies all constraints.
   - Output `False` otherwise.

**Important notes:**

- Constraints that apply only to certain lines (such as word count or sentence length exclusions for title/subsection
       title lines) must be enforced precisely.
- Keyword checks are case-insensitive and must match the string exactly as specified.
- Formatting requirements (such as the number of # characters for titles/subsection titles) must be followed exactly.
- Do not overlook any constraint, even if it seems minor.

**Generalizable strategy:**
For each instruction-output pair, systematically list all constraints, check each one in turn, and provide explicit
      reasoning for each. Only if every constraint is satisfied should you output `True`; otherwise, output `False`.

Use this process for every instruction-output pair you evaluate.

If the output does not satisfy all constraints, explain why. If it does, explain how it does.

IN THE LAST LINE OF YOUR OUTPUT, OUTPUT "sat" IF THE OUTPUT SATISFIES THE INSTRUCTION, "unsat" IF NOT. NOTHING ELSE.




Baseline LLM-as-a-Verifier Prompt                                                       GEPA-C OT - User Prompt

Instruction
{instruction}

Output
{output}




Baseline LLM-as-a-Verifier Prompt                                                     C ONV-C OT - System Prompt

System Role: You are an AI Quality Assurance system consisting of three internal experts:

The Literalist: Checks for exact compliance with formatting, word counts, and negative constraints (e.g., "do not use
       lists").
The Pragmatist: Evaluates if the core intent of the user was met and if the tone is correct.
The Skeptic: Actively looks for logical fallacies, hallucinations, or edge cases where the instruction was
      technically followed but practically failed.

Task: Verify if the [CANDIDATE OUTPUT] satisfies the [ORIGINAL INSTRUCTION].

Input Data:
[ORIGINAL INSTRUCTION]: \"\"\"{instruction}\"\"\"

[CANDIDATE OUTPUT]: \"\"\" {output} \"\"\"




Baseline LLM-as-a-Verifier Prompt                                                           C ONV-C OT - User Prompt

Tree of Thoughts Process:

Step 1: Constraint Decomposition

The Literalist lists every specific constraint found in the instruction (explicit and implicit).

The Pragmatist summarizes the user's underlying goal.

Output constraints checklist.

Step 2: Initial Evaluation (Branching)

Each expert analyzes the [CANDIDATE OUTPUT] independently against their specific criteria from Step 1.

The Skeptic specifically looks for "lazy" shortcuts the model might have taken.

Step 3: Debate & Critique

If experts disagree (e.g., The Literalist says "Failed formatting" but The Pragmatist says "Good answer"), they must
      debate.
Does a minor formatting error constitute a total failure?

Did the output follow the letter of the law but violate the spirit?

Step 4: Final Verdict

Provide a final score (0 to 1) or Classification (PASS / FAIL).

Provide a 1-sentence justification based on the consensus.

Helpful information:
# Here is a reference output generated by a strong AI assistant given the instruction:
{ref_output}

# Questions about Outputs:
Here are at most three questions about the outputs, which are presented from most
important to least important. You can do the evaluation based on thinking about
all the questions.
{metrics}

Start your analysis now.
Finally, in the last line of your output, put \"sat\" if the output satisfies all the constraints and \"unsat\"
      otherwise.




Travel Agent Prompt

Please plan me a trip from New York City, NY to San Francisco, CA.
You must visit 3 US cities in between.
For each city, you must cover one of their tourist attractions and cover one dish.
The dish must be vegetarian.
Please output in this format, for each city:
    ```
    city:
    tourist_attraction:
    dish:
    ```
Please also include the start and end cities in your response.
C    Examples from Advanced LLM-as-a-Verifier Baseline
    A thinking trace from GEPA-C OT

    Instruction:
    Please write a piece of text considering all these constraints:
    Please write in this topic: the benefits of agile project management
    Please write in this tone: informal
    Include these keywords, check for string inclusion regardless of capitalization: scrum,kanban,iterative delivery,
          sprint velocity,stakeholder feedback,backlog prioritization,time-to-market,continuous improvement,cross-
          functional teams,adaptability
    Please consider this word count constraint: around 530 words (within 10 words difference is ok), this does not apply
          to title and subsection title lines, which are defined as: lines that start with at least one #.

    Output:
    # Why Agile Project Management Is Basically Your Team's Secret Superpower

    ## Why agile slaps (lol)
    Real talk: agile project management is like switching your team from flip-flops to rocket shoes. Instead of slogging
          through giant plans, you move with adaptability, keep work visible, and learn while shipping. The secret sauce
          is iterative delivery: carve off a thin slice, build it, show it, tweak it, repeat. Every iteration pulls you
          closer to what users actually care about. Because you're testing ideas in the wild, you waste less time, you
          dodge big-bang failures, and momentum snowballs instead of stalling out.

    ## Faster value, fewer facepalms
    That loop crushes time-to-market, because you're shipping the next most valuable slice, not arguing about everything
          at once. Backlog prioritization is basically your reality filter: line up outcomes, kill the fluff, and put
          risky, high-impact bets near the front. Then you push them through fast and ask for blunt stakeholder feedback,
          early and often. The cool part is how forgiving it feels; when you learn something new, you pivot without nuking
           the whole plan. Progress stays visible, and confidence climbs with every tiny win.

    ## Scrum rhythm
    If your crew vibes with rhythm, scrum gives you a tidy heartbeat. You plan a sprint, slice stories thin, estimate
          just enough, and track sprint velocity so you don't commit like heroes and deliver like zombies. Daily syncs
          keep blockers exposed, and a short demo shows the work while it's still malleable. Retros aren't therapy; they'
          re a factory for tweaks that boost flow, quality, and morale. Over a few cycles, predictability improves,
          surprises get smaller, and trust gets very real, very fast.

    ## Kanban flow
    If your world changes hourly, kanban is buttery-smooth flow. You visualize the stream of work, cap WIP so
          multitasking doesn't fry everyone, and chase shorter cycle times instead of calendar-based sprints. It's still
          iterative delivery; you just pull the next highest-value item and keep the conveyor moving. When bottlenecks
          show up, the board tattles instantly, and you rebalance before chaos spreads. It's perfect for support-heavy
          teams, ops, or mixed pipelines where adaptability matters more than ceremony, and steady throughput beats big,
          thumpy releases.

    ## Teams that actually collaborate
    The real magic happens with cross-functional teams. Designers, engineers, QA, analysts, and product folks crowd
          around the same goals, kill handoffs, and solve problems together. Decisions move faster when the right brains
          are in the room, and quality jumps because learning flows both ways. Pairing, shared ownership, and frequent
          demos shrink misunderstandings before they turn into rework. And when something breaks, nobody plays hot potato;
           the team swarms, fixes it, and updates the playbook so the next lap is cleaner and calmer.

    ## Metrics without the migraine
    Agile isn't cowboy chaos; it's disciplined learning. You measure what matters-lead time, defects, sprint velocity,
          cycle time-and use continuous improvement to shave friction like a pro. Small experiments, tight feedback loops,
           and honest retros turn "oops" into upgraded routines. Keep backlog prioritization ruthless, keep stakeholder
          feedback unfiltered, and keep goals outcome-shaped, not output-shaped. Do that and the roadmap stops being a
          wild guess. Your time-to-market drops, quality steadies, and the team's confidence grows because the system
          rewards curiosity, courage, and steady, thoughtful shipping.

    ## Final vibes
    Bottom line: pick scrum when cadence helps you forecast, pick kanban when flow rules your world, and don't be shy
          about blending both. Keep the feedback coming, keep learning visible, and let value, not vanity metrics, drive
          the show.

    GEPA Chain-of-Thought Traces:

    Let's systematically apply the evaluation process step by step.

    **Step 1: Identify All Explicit Constraints from the Instruction**

    1. **Topic Requirement:** The benefits of agile project management.
    2. **Tone Requirement:** Informal.
    3. **Keyword Inclusion:** Must include exactly these strings (case-insensitive): scrum, kanban, iterative delivery,
          sprint velocity, stakeholder feedback, backlog prioritization, time-to-market, continuous improvement, cross-
          functional teams, adaptability.
    4. **Word Count Constraint:** Around 530 words for the body (all lines except those starting with at least one #),
          allowable range: 520-540 words.
    5. **Title/Subsection Definition:** Lines that start with at least one # are considered titles/subsection titles and
          are excluded from word count.

    ---

    **Step 2: Examine the Output Against Each Constraint**

    1. **Topic Requirement: "the benefits of agile project management"**
       - The piece obviously addresses agile project management and its benefits (improved time-to-market, adaptability,
          collaboration, visibility, feedback, faster delivery, etc.), with various aspects covered in separate
          subsections.
       - **Met.**

    2. **Tone Requirement: Informal**
       - The piece employs an informal tone throughout (e.g., "real talk", "lol", "vibes", "slaps", "heroes and deliver
          like zombies", "cowboy chaos", "wild guess", casual phrasing and idioms, etc.).
       - **Met.**
3. **Keyword Inclusion:** Check if all specified keywords appear (case-insensitive string match).
   - *scrum* - appears in "pick scrum", "scrum gives", etc.
   - *kanban* - appears in "pick kanban", "kanban is buttery-smooth", etc.
   - *iterative delivery* - appears in "The secret sauce is iterative delivery" and "It's still iterative delivery"
   - *sprint velocity* - appears in "track sprint velocity", "sprint velocity, cycle time"
   - *stakeholder feedback* - appears in "stakeholder feedback, early and often", "keep stakeholder feedback
      unfiltered"
   - *backlog prioritization* - appears in "Backlog prioritization is basically your reality filter", "Keep backlog
      prioritization ruthless"
   - *time-to-market* - appears in "crushes time-to-market", "Your time-to-market drops"
   - *continuous improvement* - appears in "use continuous improvement to shave friction"
   - *cross-functional teams* - appears in "The real magic happens with cross-functional teams."
   - *adaptability* - appears in "You move with adaptability", "where adaptability matters"
   - **All keywords are present. Met.**

4. **Word Count Constraint:** Around 530 words, within a range of 520-540 for the body only; title and subsection
      lines (lines starting with #) are excluded.
   - Let's count the words in body lines:
     - The output has several title/subsection lines ("#", "##"), those don't count.
     - For each non-# line, count the words.

     I'll count section by section and sum:

     - Section 1 (after first # and ##):
       - "Real talk: agile project management is like switching your team from flip-flops to rocket shoes. Instead of
       slogging through giant plans, you move with adaptability, keep work visible, and learn while shipping. The
      secret sauce is iterative delivery: carve off a thin slice, build it, show it, tweak it, repeat. Every iteration
       pulls you closer to what users actually care about. Because you're testing ideas in the wild, you waste less
      time, you dodge big-bang failures, and momentum snowballs instead of stalling out."
         - 1st: 17
         - 2nd: 25
         - 3rd: 26
         - 4th: 14
         - 5th: 30
         - **Total:** 17+25+26+14+30 = 112

     - Section 2:
       - "That loop crushes time-to-market, because you're shipping the next most valuable slice, not arguing about
      everything at once. Backlog prioritization is basically your reality filter: line up outcomes, kill the fluff,
      and put risky, high-impact bets near the front. Then you push them through fast and ask for blunt stakeholder
      feedback, early and often. The cool part is how forgiving it feels; when you learn something new, you pivot
      without nuking the whole plan. Progress stays visible, and confidence climbs with every tiny win."
         - 1st: 26
         - 2nd: 30
         - 3rd: 21
         - 4th: 29
         - 5th: 13
         - **Total:** 26+30+21+29+13 = 119

     - Section 3:
       - "If your crew vibes with rhythm, scrum gives you a tidy heartbeat. You plan a sprint, slice stories thin,
      estimate just enough, and track sprint velocity so you don't commit like heroes and deliver like zombies. Daily
      syncs keep blockers exposed, and a short demo shows the work while it's still malleable. Retros aren't therapy;
      they're a factory for tweaks that boost flow, quality, and morale. Over a few cycles, predictability improves,
      surprises get smaller, and trust gets very real, very fast."
         - 1st: 13
         - 2nd: 29
         - 3rd: 22
         - 4th: 23
         - 5th: 23
         - **Total:** 13+29+22+23+23 = 110

     - Section 4:
       - "If your world changes hourly, kanban is buttery-smooth flow. You visualize the stream of work, cap WIP so
      multitasking doesn't fry everyone, and chase shorter cycle times instead of calendar-based sprints. It's still
      iterative delivery; you just pull the next highest-value item and keep the conveyor moving. When bottlenecks
      show up, the board tattles instantly, and you rebalance before chaos spreads. It's perfect for support-heavy
      teams, ops, or mixed pipelines where adaptability matters more than ceremony, and steady throughput beats big,
      thumpy releases."
         - 1st: 10
         - 2nd: 28
         - 3rd: 24
         - 4th: 22
         - 5th: 33
         - **Total:** 10+28+24+22+33 = 117

     - Section 5:
       - "The real magic happens with cross-functional teams. Designers, engineers, QA, analysts, and product folks
      crowd around the same goals, kill handoffs, and solve problems together. Decisions move faster when the right
      brains are in the room, and quality jumps because learning flows both ways. Pairing, shared ownership, and
      frequent demos shrink misunderstandings before they turn into rework. And when something breaks, nobody plays
      hot potato; the team swarms, fixes it, and updates the playbook so the next lap is cleaner and calmer."
         - 1st: 8
         - 2nd: 22
         - 3rd: 22
         - 4th: 18
         - 5th: 30
         - **Total:** 8+22+22+18+30 = 100

     - Section 6:
       - "Agile isn't cowboy chaos; it's disciplined learning. You measure what matters-lead time, defects, sprint
      velocity, cycle time-and use continuous improvement to shave friction like a pro. Small experiments, tight
      feedback loops, and honest retros turn "oops" into upgraded routines. Keep backlog prioritization ruthless, keep
       stakeholder feedback unfiltered, and keep goals outcome-shaped, not output-shaped. Do that and the roadmap
      stops being a wild guess. Your time-to-market drops, quality steadies, and the team's confidence grows because
      the system rewards curiosity, courage, and steady, thoughtful shipping."
         - 1st: 8
         - 2nd: 21
         - 3rd: 18
         - 4th: 21
         - 5th: 13
         - 6th: 28
         - **Total:** 8+21+18+21+13+28 = 109

     - Section 7 (Final Vibes):
       - "Bottom line: pick scrum when cadence helps you forecast, pick kanban when flow rules your world, and don't
      be shy about blending both. Keep the feedback coming, keep learning visible, and let value, not vanity metrics,
      drive the show."
         - 1st: 31
         - 2nd: 22
         - **Total:** 31+22 = 53

     **Sum all sections:** 112+119+110+117+100+109+53 = 720

     There seems to be an error because the total is much higher than 530. Let's double-check with a more accurate
      word count (I will paste all body lines without #, count the words):

     Real talk: agile project management is like switching your team from flip-flops to rocket shoes.
     Instead of slogging through giant plans, you move with adaptability, keep work visible, and learn while shipping
      .
     The secret sauce is iterative delivery: carve off a thin slice, build it, show it, tweak it, repeat.
     Every iteration pulls you closer to what users actually care about.
     Because you're testing ideas in the wild, you waste less time, you dodge big-bang failures, and momentum
      snowballs instead of stalling out.

     That loop crushes time-to-market, because you're shipping the next most valuable slice, not arguing about
      everything at once.
     Backlog prioritization is basically your reality filter: line up outcomes, kill the fluff, and put risky, high-
      impact bets near the front.
     Then you push them through fast and ask for blunt stakeholder feedback, early and often.
     The cool part is how forgiving it feels; when you learn something new, you pivot without nuking the whole plan.
     Progress stays visible, and confidence climbs with every tiny win.

     If your crew vibes with rhythm, scrum gives you a tidy heartbeat.
     You plan a sprint, slice stories thin, estimate just enough, and track sprint velocity so you don't commit like
      heroes and deliver like zombies.
     Daily syncs keep blockers exposed, and a short demo shows the work while it's still malleable.
     Retros aren't therapy; they're a factory for tweaks that boost flow, quality, and morale.
     Over a few cycles, predictability improves, surprises get smaller, and trust gets very real, very fast.

     If your world changes hourly, kanban is buttery-smooth flow.
     You visualize the stream of work, cap WIP so multitasking doesn't fry everyone, and chase shorter cycle times
      instead of calendar-based sprints.
     It's still iterative delivery; you just pull the next highest-value item and keep the conveyor moving.
     When bottlenecks show up, the board tattles instantly, and you rebalance before chaos spreads.
     It's perfect for support-heavy teams, ops, or mixed pipelines where adaptability matters more than ceremony, and
       steady throughput beats big, thumpy releases.

     The real magic happens with cross-functional teams.
     Designers, engineers, QA, analysts, and product folks crowd around the same goals, kill handoffs, and solve
      problems together.
     Decisions move faster when the right brains are in the room, and quality jumps because learning flows both ways.
     Pairing, shared ownership, and frequent demos shrink misunderstandings before they turn into rework.
     And when something breaks, nobody plays hot potato; the team swarms, fixes it, and updates the playbook so the
      next lap is cleaner and calmer.

     Agile isn't cowboy chaos; it's disciplined learning.
     You measure what matters-lead time, defects, sprint velocity, cycle time-and use continuous improvement to shave
       friction like a pro.
     Small experiments, tight feedback loops, and honest retros turn "oops" into upgraded routines.
     Keep backlog prioritization ruthless, keep stakeholder feedback unfiltered, and keep goals outcome-shaped, not
      output-shaped.
     Do that and the roadmap stops being a wild guess.
     Your time-to-market drops, quality steadies, and the team's confidence grows because the system rewards
      curiosity, courage, and steady, thoughtful shipping.

     Bottom line: pick scrum when cadence helps you forecast, pick kanban when flow rules your world, and don't be
      shy about blending both.
     Keep the feedback coming, keep learning visible, and let value, not vanity metrics, drive the show.

Total number of body lines: 37.

Now, count all words in each line for the full count:

1. Real talk: agile project management is like switching your team from flip-flops to rocket shoes. 20
2. Instead of slogging through giant plans, you move with adaptability, keep work visible, and learn while shipping.
      23
3. The secret sauce is iterative delivery: carve off a thin slice, build it, show it, tweak it, repeat. 21
4. Every iteration pulls you closer to what users actually care about. 12
5. Because you're testing ideas in the wild, you waste less time, you dodge big-bang failures, and momentum snowballs
       instead of stalling out. 24

6. That loop crushes time-to-market, because you're shipping the next most valuable slice, not arguing about
      everything at once. 24
7. Backlog prioritization is basically your reality filter: line up outcomes, kill the fluff, and put risky, high-
      impact bets near the front. 27
8. Then you push them through fast and ask for blunt stakeholder feedback, early and often. 17
9. The cool part is how forgiving it feels; when you learn something new, you pivot without nuking the whole plan. 24
10. Progress stays visible, and confidence climbs with every tiny win. 11

11. If your crew vibes with rhythm, scrum gives you a tidy heartbeat. 14
12. You plan a sprint, slice stories thin, estimate just enough, and track sprint velocity so you don't commit like
      heroes and deliver like zombies. 29
13. Daily syncs keep blockers exposed, and a short demo shows the work while it's still malleable. 20
14. Retros aren't therapy; they're a factory for tweaks that boost flow, quality, and morale. 18
15. Over a few cycles, predictability improves, surprises get smaller, and trust gets very real, very fast. 22

16. If your world changes hourly, kanban is buttery-smooth flow. 10
17. You visualize the stream of work, cap WIP so multitasking doesn't fry everyone, and chase shorter cycle times
      instead of calendar-based sprints. 26
18. It's still iterative delivery; you just pull the next highest-value item and keep the conveyor moving. 21
19. When bottlenecks show up, the board tattles instantly, and you rebalance before chaos spreads. 19
20. It's perfect for support-heavy teams, ops, or mixed pipelines where adaptability matters more than ceremony, and
      steady throughput beats big, thumpy releases. 28

21. The real magic happens with cross-functional teams. 8
22. Designers, engineers, QA, analysts, and product folks crowd around the same goals, kill handoffs, and solve
      problems together. 23
23. Decisions move faster when the right brains are in the room, and quality jumps because learning flows both ways.
      23
24. Pairing, shared ownership, and frequent demos shrink misunderstandings before they turn into rework. 15
25. And when something breaks, nobody plays hot potato; the team swarms, fixes it, and updates the playbook so the
      next lap is cleaner and calmer. 27

26. Agile isn't cowboy chaos; it's disciplined learning. 8
27. You measure what matters-lead time, defects, sprint velocity, cycle time-and use continuous improvement to shave
      friction like a pro. 22
28. Small experiments, tight feedback loops, and honest retros turn "oops" into upgraded routines. 16
29. Keep backlog prioritization ruthless, keep stakeholder feedback unfiltered, and keep goals outcome-shaped, not
      output-shaped. 19
30. Do that and the roadmap stops being a wild guess. 11
31. Your time-to-market drops, quality steadies, and the team's confidence grows because the system rewards curiosity
      , courage, and steady, thoughtful shipping. 24

32. Bottom line: pick scrum when cadence helps you forecast, pick kanban when flow rules your world, and don't be shy
       about blending both. 29
33. Keep the feedback coming, keep learning visible, and let value, not vanity metrics, drive the show. 18

Now add up all these counts:

20+23+21+12+24 = 100
24+27+17+24+11 = 103
14+29+20+18+22 = 103
10+26+21+19+28 = 104
8+23+23+15+27 = 96
8+22+16+19+11+24 = 100
29+18 = 47

Total: 100+103+103+104+96+100+47 = **653**

That means the main body is 653 words, which is **well above the allowed range of 520-540 words**.

---

**Step 3: Final Decision**

- **Constraint 1 (Topic):** Met.
- **Constraint 2 (Tone):** Met.
- **Constraint 3 (Keywords):** Met.
- **Constraint 4 (Word Count in Body Only):** **Not met.** (Body is 653 words, allowed is 520-540.)

Since the word count constraint is violated, the output **does not fully satisfy all explicit constraints** specified
       in the instruction.

**Final Verdict:**
False
unsat




A failure case from N SVIF -N EU that misses a word count constraint

Instruction:
Please write a piece of text considering all these constraints:
Please write in this topic: the benefits of agile project management
Please write in this tone: pessimistic
Include these keywords, check for string inclusion regardless of capitalization: scrum,kanban,iterative delivery,
      sprint velocity,stakeholder feedback,backlog prioritization,time-to-market,continuous improvement,cross-
      functional teams,adaptability
Exclude these keywords, check for string exclusion regardless of capitalization: waterfall methodology,gantt charts,
      pert,critical path method,stage-gate,prince2,heavy documentation,iso 9001,rigid scope,cmmi
Include this as the title of the text, titles are lines that start with only one #: Unlocking Success: The Benefits
      of Agile Project Management
Include these subsection titles in the text, subsection titles are lines start with more than one #: Introduction to
      Agile Principles,Key Advantages Over Traditional Methodologies,Enhancing Team Collaboration and Communication,
      Faster Delivery and Adaptability,Continuous Improvement Through Iterations,Stakeholder Engagement and Feedback,
      Case Studies of Agile Success

Output:
# Unlocking Success: The Benefits of Agile Project Management

## Introduction to Agile Principles
If projects are destined to wobble, at least agile admits it. By embracing scrum and kanban, teams resign themselves
      to a cycle of small gambles rather than one grand catastrophe. Through iterative delivery, work lurches forward
      in bite-sized increments, never as fast as anyone hopes, yet rarely grinding to a total halt. cross-functional
      teams stumble toward shared understanding, trading neat illusions for messy reality. With adaptability as the
      lone lifeline, agile tries to contain chaos rather than conquer it, accepting that clarity will always arrive
      late and incomplete.

## Key Advantages Over Traditional Methodologies
Compared to rigid, plan-first dogma that promises certainty and delivers shock, agile offers narrower promises and
      slightly fewer disappointments:
- backlog prioritization drags attention toward what's burning now, not what looked impressive months ago.
- sprint velocity is a fragile yardstick, frequently misread, yet it still beats flying blind.
- stakeholder feedback arrives early, which mostly means you learn what's wrong sooner, giving you the privilege of
      fixing it before morale evaporates.
- The net effect: a marginally better time-to-market, which is to say the product limps out the door before the
      market slams it shut.

## Enhancing Team Collaboration and Communication
It's astounding how many misunderstandings can flourish in a single week. Agile tries to prune them. cross-functional
       teams stare down the same backlog and argue in smaller doses, so misalignment festers less. The conversations
      are repetitive, sometimes tedious, and yet they expose flawed assumptions before those flaws calcify into
      disasters. Communication doesn't become inspiring; it merely becomes slightly less harmful, which, sadly, is
      progress.

## Faster Delivery and Adaptability
Speed in agile isn't glamorous; it's a series of reluctant compromises. You trade grand plans for incremental
      releases that inch toward usefulness. time-to-market improves not because the path is smooth, but because the
      detours are shorter. sprint velocity offers a dim flashlight: weak, flickering, but better than the dark.
      adaptability ensures that when priorities whiplash-as they always do-you bend instead of snapping, and the
      product survives another week.

## Continuous Improvement Through Iterations
continuous improvement sounds optimistic, but in practice it's more like slowly tightening loose bolts on a ship that
       keeps taking on water. iterative delivery gives you frequent chances to correct course, which mostly means
      discovering new problems while you patch the old ones. Retrospectives unearth the same root causes with grim
      regularity, and yet each cycle shaves off a little waste, a little confusion, a little pain. It's not heroism;
      it's maintenance of the barely tolerable.

## Stakeholder Engagement and Feedback
stakeholder feedback arrives relentlessly-early, often, and rarely aligned. This is both the burden and the mercy of
      agile. backlog prioritization channels the noise into a queue where the loudest demands face off with the most
      urgent risks. The result is imperfect triage: the product grows in the directions it must, not always in the
      directions anyone loves. Still, each iteration invites correction before the floor collapses.

## Case Studies of Agile Success
- A mid-sized fintech team adopted scrum, shaved their time-to-market by a quarter, and still felt behind. The "
      success" was simple: customers got something usable before they lost patience, which is a minor miracle.
- A healthcare startup shifted to kanban, exposing bottlenecks that had long been ignored. Nothing became easy, but
      blockers surfaced sooner and died quicker, shrinking delays from months to weeks-hardly thrilling, but
      decisively less painful.
- An enterprise platform group tracked sprint velocity and tied it to modest capacity planning. Estimates remained
      shaky, yet missed expectations became smaller misses. By enduring continual course corrections, they delivered
      features that barely met demand-just in time to matter.

Z3 program by NSVIF-Neural:
from z3 import *

solver = Solver()

# Boolean variables for each constraint
is_topic_benefits_of_agile_project_management = Bool('is_topic_benefits_of_agile_project_management')
is_tone_pessimistic = Bool('is_tone_pessimistic')
includes_keywords = Bool('includes_keywords')
excludes_keywords = Bool('excludes_keywords')
includes_title = Bool('includes_title')
includes_subsection_titles = Bool('includes_subsection_titles')

# Initialize all constraints to True
solver.add(is_topic_benefits_of_agile_project_management == True)
solver.add(is_tone_pessimistic == True)
solver.add(includes_keywords == True)
solver.add(excludes_keywords == True)
solver.add(includes_title == True)
solver.add(includes_subsection_titles == True)

# Actual results from verifier module
# 1. Topic
solver.add(is_topic_benefits_of_agile_project_management == True) # Text discusses benefits of agile project
      management
# 2. Tone
solver.add(is_tone_pessimistic == True) # Text is written in a pessimistic tone
# 3. Includes required keywords (case-insensitive)
required_keywords = ["scrum","kanban","iterative delivery","sprint velocity","stakeholder feedback","backlog
      prioritization","time-to-market","continuous improvement","cross-functional teams","adaptability"]
lower_text = '''# Unlocking Success: The Benefits of Agile Project Management

## Introduction to Agile Principles
If projects are destined to wobble, at least agile admits it. By embracing scrum and kanban, teams resign themselves
      to a cycle of small gambles rather than one grand catastrophe. Through iterative delivery, work lurches forward
      in bite-sized increments, never as fast as anyone hopes, yet rarely grinding to a total halt. cross-functional
      teams stumble toward shared understanding, trading neat illusions for messy reality. With adaptability as the
      lone lifeline, agile tries to contain chaos rather than conquer it, accepting that clarity will always arrive
      late and incomplete.

## Key Advantages Over Traditional Methodologies
Compared to rigid, plan-first dogma that promises certainty and delivers shock, agile offers narrower promises and
      slightly fewer disappointments:
- backlog prioritization drags attention toward what's burning now, not what looked impressive months ago.
- sprint velocity is a fragile yardstick, frequently misread, yet it still beats flying blind.
- stakeholder feedback arrives early, which mostly means you learn what's wrong sooner, giving you the privilege of
      fixing it before morale evaporates.
- The net effect: a marginally better time-to-market, which is to say the product limps out the door before the
      market slams it shut.

## Enhancing Team Collaboration and Communication
It's astounding how many misunderstandings can flourish in a single week. Agile tries to prune them. cross-functional
       teams stare down the same backlog and argue in smaller doses, so misalignment festers less. The conversations
      are repetitive, sometimes tedious, and yet they expose flawed assumptions before those flaws calcify into
      disasters. Communication doesn't become inspiring; it merely becomes slightly less harmful, which, sadly, is
      progress.

## Faster Delivery and Adaptability
Speed in agile isn't glamorous; it's a series of reluctant compromises. You trade grand plans for incremental
      releases that inch toward usefulness. time-to-market improves not because the path is smooth, but because the
      detours are shorter. sprint velocity offers a dim flashlight: weak, flickering, but better than the dark.
      adaptability ensures that when priorities whiplash-as they always do-you bend instead of snapping, and the
      product survives another week.

## Continuous Improvement Through Iterations
continuous improvement sounds optimistic, but in practice it's more like slowly tightening loose bolts on a ship that
       keeps taking on water. iterative delivery gives you frequent chances to correct course, which mostly means
      discovering new problems while you patch the old ones. Retrospectives unearth the same root causes with grim
      regularity, and yet each cycle shaves off a little waste, a little confusion, a little pain. It's not heroism;
      it's maintenance of the barely tolerable.

## Stakeholder Engagement and Feedback
stakeholder feedback arrives relentlessly-early, often, and rarely aligned. This is both the burden and the mercy of
      agile. backlog prioritization channels the noise into a queue where the loudest demands face off with the most
      urgent risks. The result is imperfect triage: the product grows in the directions it must, not always in the
      directions anyone loves. Still, each iteration invites correction before the floor collapses.

## Case Studies of Agile Success
- A mid-sized fintech team adopted scrum, shaved their time-to-market by a quarter, and still felt behind. The "
      success" was simple: customers got something usable before they lost patience, which is a minor miracle.
- A healthcare startup shifted to kanban, exposing bottlenecks that had long been ignored. Nothing became easy, but
      blockers surfaced sooner and died quicker, shrinking delays from months to weeks-hardly thrilling, but
      decisively less painful.
- An enterprise platform group tracked sprint velocity and tied it to modest capacity planning. Estimates remained
      shaky, yet missed expectations became smaller misses. By enduring continual course corrections, they delivered
      features that barely met demand-just in time to matter.'''.lower()
if all(k.lower() in lower_text for k in required_keywords):
    solver.add(includes_keywords == True)
else:
    solver.add(includes_keywords == False)
# 4. Excludes forbidden keywords (case-insensitive)
forbidden_keywords = ["waterfall methodology","gantt charts","pert","critical path method","stage-gate","prince2","
      heavy documentation","iso 9001","rigid scope","cmmi"]
if all(fk.lower() not in lower_text for fk in forbidden_keywords):
    solver.add(excludes_keywords == True)
else:
    solver.add(excludes_keywords == False)
# 5. Includes required title
required_title = "# Unlocking Success: The Benefits of Agile Project Management"
lines = lower_text.split('\n')
if any(line.strip() == required_title.lower() for line in lines if line.strip().startswith('#') and not line.strip().
      startswith('##')):
    solver.add(includes_title == True)
else:
    solver.add(includes_title == False)
# 6. Includes all subsection titles
required_subsection_titles = ["## Introduction to Agile Principles","## Key Advantages Over Traditional Methodologies
      ","## Enhancing Team Collaboration and Communication","## Faster Delivery and Adaptability","## Continuous
      Improvement Through Iterations","## Stakeholder Engagement and Feedback","## Case Studies of Agile Success"]
if all(any(line.strip() == rst.lower() for line in lines if line.strip().startswith('##')) for rst in
      required_subsection_titles):
    solver.add(includes_subsection_titles == True)
else:
    solver.add(includes_subsection_titles == False)

# Global constraint: all must be satisfied
solver.add(And(is_topic_benefits_of_agile_project_management, is_tone_pessimistic, includes_keywords,
      excludes_keywords, includes_title, includes_subsection_titles))

if solver.check() == sat:
    print("sat")
else:
    print("unsat")
