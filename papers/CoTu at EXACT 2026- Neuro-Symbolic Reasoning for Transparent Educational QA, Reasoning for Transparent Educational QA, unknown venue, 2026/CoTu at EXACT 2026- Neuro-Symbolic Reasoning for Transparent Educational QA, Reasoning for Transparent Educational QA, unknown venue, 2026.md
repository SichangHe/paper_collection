                                                 CoTu at EXACT 2026: Neuro-Symbolic
                                                Reasoning for Transparent Educational QA

                                         Quoc-Khang Tran ¹ 1⋆ , Minh-Thien Nguyen 1 , Phu-An Thai1 , Xuan-Tung
                                                Bui 1,2 , Truong-Thanh Ma1⋆ , and Nguyen-Khang Pham 1⋆
                                                              1
                                                                Can Tho University, Can Tho city, Vietnam
                                                               {tqkhang,mtthanh,pnkhang}@ctu.edu.vn,
                                                           {minhnguyent546,contact.thaiphuan}@gmail.com,
                                                                 tungp2425004@gstudent.ctu.edu.vn
                                                              2
                                                                Tay Do University, Can Tho city, Vietnam
                                                                         bxtung@tdu.edu.vn
arXiv:2607.14735v1 [cs.CL] 16 Jul 2026




                                                 Abstract. Transparent educational question answering asks for answers
                                                 that are not only correct but explainable, and doing so with small mod-
                                                 els rules out the reasoning power of the largest proprietary systems.
                                                 The EXACT 2026 competition poses this problem concretely: open-
                                                 weight language models of at most 8B parameters, self-hosted, with a
                                                 natural-language explanation for every answer. It pairs two tasks: log-
                                                 ical reasoning over university regulations, and multi-step physics prob-
                                                 lem solving. We describe the system that team CoTu developed to ad-
                                                 dress both, a neuro-symbolic Program-of-Thought pipeline in which a
                                                 4B backbone writes a program rather than stating an answer directly:
                                                 for regulation queries it emits a Z3 encoding whose entailment verdict
                                                 grounds the deduction, and for physics it emits numerical Python, both
                                                 wrapped in a shared self-correction loop and a unified explained-JSON
                                                 output. Answer-type routing, distillation-based task fine-tuning, and a
                                                 latency-aware serving stack—SGLang with speculative decoding—keep
                                                 the system within the 60-second per-query limit. The system achieved a
                                                 perfect score on the physics task in both automated selection rounds
                                                 and obtained the highest final-round technical score of any team—
                                                 13.44/15, combining automated answer evaluation with expert-judged
                                                 reasoning depth—with the equally weighted presentation score included,
                                                 CoTu placed 3rd overall. Grounding answers in a symbolic solver yields
                                                 correct, verifiable deductions at the 4B scale, and the residual difficulty
                                                 lies in premise selection rather than the deduction itself.


                                                             EXACT-2026-CoTu         cotulabs/cotu-exact-2026


                                                 Keywords: Educational QA · Neuro-Symbolic Reasoning · Z3 Solver ·
                                                 Explainable AI.

                                         ⋆
                                             Corresponding author. Email: {tqkhang,pnkhang,mtthanh}@ctu.edu.vn
   2      Quoc-Khang et al.

   1   Introduction
   Large Language Models (LLMs) [1,17,19,29,14,2] have advanced automated ques-
   tion answering, including educational and academic assistance [11,21]. Despite
   strong natural language capabilities, purely neural models remain limited in
   transparency, explainability, and reliability on complex reasoning tasks [16]. In
   academic settings, where factual accuracy is essential for student learning, con-
   cise but unsubstantiated answers or “hallucinations” [9,8] from black-box models
   can harm pedagogy and hinder practical adoption of AI in education.
       To address this challenge, Neuro-Symbolic (NeSy) [6,24] reasoning com-
   bines the pattern recognition and linguistic flexibility of neural networks with
   the deterministic guarantees of symbolic logic. This integration enables systems
   not only to produce accurate answers but also to expose intermediate reasoning
   in formal form, such as First-Order Logic (FOL), which can be checked with
   automated theorem provers like the Z3 Solver [15]. By making intermediate
   steps transparent and verifiable, neuro-symbolic systems offer a more trustwor-
   thy bridge between machine inference and human understanding.
       The EXACT 2026 challenge (The 2nd International XAI Challenge for Trans-
   parent Educational Question-Answering), organized as part of the IEEE Interna-
   tional Joint Conference on Neural Networks (IJCNN 2026), serves as a premier
   venue to foster such hybrid solutions. Building on EXACT 2025 [16], this year’s
   edition adds quantitative STEM problem-solving in physics alongside academic
   regulation queries, increasing demands on arithmetic precision and scientific in-
   terpretability. Furthermore, the organizers enforce strict technical constraints,
   including an 8-billion parameter ceiling for all LLM components and manda-
   tory self-hosting with OpenAI-compatible tools, so participants must focus on
   algorithmic design and tool integration rather than proprietary models.
       To guide the design and evaluation of our system, we formulate the following
   research questions:
RQ1: How can resource-constrained open-weight language models (≤ 8B param-
     eters) perform reliable and transparent reasoning on natural language aca-
     demic regulations without hallucinations?
RQ2: How can symbolic logic solvers and Program-of-Thought (PoT) execution
     complement neural models to deliver mathematically and logically sound
     answers for multi-step STEM problems?
RQ3: How do targeted Supervised Fine-Tuning (SFT) data curation and latency-
     aware serving stacks affect the inference quality and speed of a hybrid neuro-
     symbolic system under strict execution time budgets?
       This report presents the methodology of team CoTu, which placed 3rd over-
   all in EXACT 2026 while recording the highest final-round technical score
   (13.44/15), combining automated answer evaluation with expert assessment of
   structured reasoning depth. The main contributions of this work are summarized
   as follows:
 C1: Unified Neuro-Symbolic PoT Pipeline: We propose a unified, dual-task
     neuro-symbolic framework. For regulation queries, it translates premises to
                                                       CoTu at EXACT 2026         3

    FOL and verifies them via a Z3 solver; for physics problems, it generates
    numerical Python code evaluated directly in a sandboxed interpreter, both
    bound in a shared self-correction loop.
C2: Teacher-Distillation and Adapters: We develop a targeted data curation
    and SFT recipe. By distilling high-quality reasoning traces and Z3 solver code
    from offline teacher models, we train specialized adapters for a 4B parameter
    backbone to generate correct program structures and API calls.
C3: High-Throughput Serving and Empirical Success: We deploy our sys-
    tem using SGLang with RadixAttention prefix caching and DFLASH spec-
    ulative decoding. Our approach achieves the highest final-round technical
    score (13.44/15) in EXACT 2026 and a perfect score on the physics task,
    demonstrating the viability of hybrid reasoning on small models.

     The remainder of this report is organized as follows: Section 2 reviews the EX-
 ACT 2026 challenge tasks and metrics. Section 3 describes the proposed neuro-
 symbolic methodology, dataset synthesis, and fine-tuning details. Section 4 out-
 lines the experimental settings and hyperparameter choices. Section 5 presents
 the evaluation results and ablation studies. Finally, Section 6 concludes the pa-
 per.


 2     Challenge Overview

 The EXACT 2026 challenge benchmarks educational QA systems that are trans-
 parent as well as correct: every answer must be accompanied by a verifiable, step-
 by-step rationale to be useful in learning environments. The dataset is split into
 two tasks representing two core aspects of academic reasoning: logical reasoning
 over academic regulations and quantitative STEM problem-solving.


 2.1   Task Overview

 Task 1 (Logic-Based Educational Queries). Task 1 evaluates logical reason-
 ing over actual university regulations and academic policies, such as grading
 schemes, enrollment prerequisites, scholarship criteria, and graduation require-
 ments. Questions are formulated as Multiple-Choice (MCQ), Yes/No/Uncertain
 (YNU), or short Open-Ended (OE) items. At evaluation time the system receives
 a question together with its corresponding natural language premises; the train-
 ing set additionally provides FOL translations and human-written explanations.
 The main difficulty lies in parsing nested rules, conditional clauses, and double
 negatives common in academic policies, which frequently cause standard LLMs
 to hallucinate. Systems must translate natural language into symbolic logic and
 defer to deterministic solvers for hallucination-free deduction.

 Task 2 (Physics Problems). Task 2 extends the challenge into STEM domains,
 requiring systems to solve text-based physics problems. The problems center
 on electric circuits and electrostatics—equivalent resistance, voltage, current,
4      Quoc-Khang et al.

electrical power, capacitance, electric fields, and energy—but are not limited to
them: the final round also draws on broader introductory-physics topics such
as mechanics, rotational dynamics, thermodynamics, and geometric optics. All
items are numerical, requiring multi-step computation. Unlike Task 1, the sys-
tem receives only the raw text of the question, with no premises or formula
sheet. It must recover the relevant physical laws from parametric memory or
external knowledge, construct the correct equations, perform sequential Chain-
of-Thought (CoT) [22,13] reasoning, and output the final numerical answer with
its unit where applicable. Combining qualitative physical reasoning with precise
arithmetic is difficult under strict model size limits, where small language models
are prone to computational errors.

2.2   Evaluation Metrics
Submissions are scored along three dimensions. P1 measures answer correctness.
For Task 2 the reference values are compared under a relative tolerance rather
than by exact match: a prediction ŷ is accepted when |ŷ − y|/|y| < τ against
the non-zero reference answer y, for a threshold τ fixed by the committee, and,
where the answer carries a unit, the unit must match as well. P2 measures
supporting-premise quality on Task 1, computed as the F1 between the premises
a system cites and the gold supporting-premise indices; Task 2 is answer-only and
carries no P2. P3 measures the depth of structured reasoning (FOL translations,
symbolic proofs, CoT traces) and is judged manually by domain experts.
    The two automated rounds add a time bonus B that rewards fast correct
answers on top of this base score; the final round applies no such bonus. Each
question has a hard time limit T = 60 seconds: a response that does not fin-
ish within T receives 0 points for that question. Summing over every question
answered correctly (P1i = 1), the bonus is
                                                     
                                X                  di
                         B=r          max 0, 1 −        ,                      (1)
                                                    T
                               i : P1i =1

where di is the response time for question i and r = 0.1 is the time-bonus rate
that converts each normalized time saving into score points; a quicker correct
answer therefore earns a larger bonus. The per-task scores combine these com-
ponents as
                  ST1 = 12 P1 + 21 P2 + B,     ST2 = P1 + B,                (2)
so Task 1 weights answer correctness and premise quality equally, while Task 2
is scored on answer correctness alone.
    The final round drops the time bonus and instead combines three compo-
nents: the automated API score SAPI (the P1/P2 base score of Equation (2)
without B, aggregated over the round’s items), the manually judged reasoning
depth P3, and a presentation score Spres . The technical score sums the first two,
and the overall final score adds presentation:

        Stech = SAPI + P3,      Sr3 = Stech + Spres = SAPI + P3 + Spres ,      (3)
                                                      CoTu at EXACT 2026         5

with SAPI scored out of 11—one point per item over the 6 Task 1 and 5 Task 2
questions of the final round—P3 out of 4 (so Stech out of 15), and Spres out of 15.
The concrete evaluation rounds and per-round scores are reported in Section 5.


3     Methodology

Our system addresses both EXACT 2026 tasks under the challenge constraints:
open-source LLMs within the 8-billion parameter ceiling, self-hosted inference,
and a natural language explanation accompanying every answer. We build one
dedicated solver per task—Task 1 compiles regulation queries into Z3 con-
straints, Task 2 solves physics problems with executable Python—over a shared
stack that both solvers draw on for orchestration, serving, code execution, and
output formatting. Figure 1 shows the full pipeline. The rest of this section cov-
ers the shared stack (Section 3.1), the two solvers (Sections 3.2 and 3.3), and
the data preparation and SFT behind the backbone (Section 3.4).


3.1    System Overview and Shared Stack

The design principle behind CoTu is neuro-symbolic: rather than have the back-
bone state an answer directly, we have it write a program, and the program pro-
duces the answer. Both branches follow this PoT pattern—Task 1 emits Z3 [15]
constraints discharged by a symbolic solver, Task 2 emits numerical Python eval-
uated directly—so the final answer is grounded in code execution rather than
free-form generation. The two branches share one orchestration, serving, and
execution stack and diverge only in what code they emit; Figure 1 shows where
they split and rejoin.

Orchestration and Backbone. Every stage is a DSPy [12] module, composing sig-
natures, CoT, and PoT steps into one declarative graph per task that we retune
without rewiring the pipeline. The backbone is GRM-2.53 , an open, Qwen3.5-
4B-based model fine-tuned for STEM and problem solving that fits the 8-billion
parameter ceiling; each branch loads its own SFT checkpoint (Section 3.4). A
single FastAPI endpoint routes each query to its branch by task type.

Rich Prompting. A 4B model has little headroom, so we front-load each branch’s
prompt with task-specific guidance that steers it toward well-formed code. Task 1
prompts carry general logic rules and common traps—double negatives, nested
conditions—alongside Z3 API usage; Task 2 prompts carry SI-unit conventions,
physical constants, unit-conversion rules, and reminders of common physics for-
mulas. This guidance is what lets a small model emit code that parses and runs
on the first attempt more often than not.
3
    https://huggingface.co/OrionLLM/GRM-2.5
6       Quoc-Khang et al.



                                                                                                                          DSPy orchestration layer




                                                           Input Question

                                                           task identifier + raw question text




                                                         Task-Specific Rich Prompting
                                   Task 1 · Logic
                                                                                 Task 2 · Physics
                                   NL→FOL pitfalls · translation
                                   rules · symbolic-error patterns ·             SI units · scientific constants · unit
                                   FOL syntax                                    conversions · formula reminders


       TASK 1 · LOGIC



                                       Router




             Y/N/U · MCQ · Open-ended

                                                                                                          TASK 2 · PHYSICS



                           PoT                                                                                             PoT
              generate symbolic program                                                                          generate Python code
                                                                             regenerate




                                                  fail                                             fail
           Python                                                                                                                  Python
           runs Z3                                                                                                                 eval



                                                                   Self-Correction
                                                                   execution retry
                    ∀ ∃ |=
                Z3 SMT Solver
                     SAT   UNSAT     UNK




                                                                   Refinement




                                                 Unified JSON Output                       shared schema
                                           {}    answer:str unit:str explanation:str
                                                 premises used:list[int] reasoning:obj




Fig. 1. The CoTu dual-task pipeline. A query, tagged with its task identifier, first re-
ceives task-specific rich prompting: translation and symbolic-error guidance for Task 1,
and units, constants, and formula guidance for Task 2. The Task 1 branch routes the
query by answer type, then generates a PoT that runs Z3 through Python, whereas the
Task 2 branch generates PoT Python that is evaluated directly. Both branches send
failed executions back through a shared self-correction loop that regenerates the code,
and both converge on an output-refinement stage that emits one unified JSON record.
The whole system is coordinated by a DSPy orchestration layer.
                                                      CoTu at EXACT 2026         7

High-throughput Serving. Serving is tuned for the challenge’s 60-second per-
query limit and its time-based scoring bonus, both of which reward fast correct
answers (Section 2.2). We self-host with SGLang [30], whose RadixAttention
reuses the key-value cache across the shared prefixes of our prompts, and pair
it with DFLASH speculative decoding [3], which drafts a block of tokens in one
parallel forward pass with a lightweight block-diffusion model—higher-quality
drafts than the autoregressive multi-token-prediction drafters commonly used
for speculation. Together they cut the latency of our multi-call reasoning chains,
earning time bonus without shortening the reasoning itself. We deliberately serve
the backbone in BF16 with no quantization: on long-thinking, hard problems the
reasoning quality this preserves is worth more than the extra speed quantization
would buy.

Shared Execution and Output. Two mechanisms close the loop for both branches.
Generated code runs in a common sandboxed interpreter—a fresh process with
a restricted set of builtins and a fixed timeout, exposing Z3 constructors on
the Task 1 side and plain numerical code on the Task 2 side—and any parse or
execution failure is fed back to the backbone to regenerate, within a fixed retry
budget (Section 4). Both branches then converge on a refinement stage that
populates the shared JSON schema with the fields ⟨ answer, unit, explanation,
premises_used, reasoning ⟩, so a single output contract serves both automated
scoring and manual reasoning assessment; the explanation is non-empty for
every answer, as the challenge requires. This shared self-correction loop and
output-refinement stage are where the branches rejoin in Figure 1.

3.2   Task 1: Logic-Based Educational Queries
Task 1 answers questions about university regulations. The branch receives a
question and its natural language premises (plus answer options for multiple-
choice items), encodes them as a Z3 program, and reads the answer off the
solver outcome, so the deduction is deterministic rather than free-form. The
paragraphs below detail the Task 1 branch of Figure 1, from answer-type routing
to the shared refinement stage.

Question Routing. A query first passes a lightweight classifier that infers its an-
swer type—MCQ, YNU, or OE—from the question text, applying MCQ only
when explicit option markers are present. The type selects one of three special-
ized PoT solvers, each pinned to its own answer format. A preceding clarity check
screens for malformed items, such as undefined symbols or missing options, and
short-circuits them to an Uncertain answer instead of forcing a spurious deduc-
tion.

Hybrid Few-shot Retrieval. To supply worked Z3 exemplars, we built a hybrid
retriever over a corpus of solved Task 1 items. For a query q and a candidate
solved item d in the corpus D, we compute dense similarity using a dense encoder
(Qwen3-Embedding-0.6B) and lexical similarity using a sparse BM25 index, both
8       Quoc-Khang et al.

served from a Qdrant store. The two ranked lists are merged using Reciprocal
Rank Fusion (RRF) [4], formalized as follows:

Definition 1 (Reciprocal Rank Fusion). Let Rdense (q) and Rsparse (q) be
the ranked lists of candidate items retrieved by the dense and sparse models,
respectively. For each candidate item d ∈ Rdense (q) ∪ Rsparse (q), let rdense (q, d)
and rsparse (q, d) denote the rank of d in the respective lists (with r(q, d) = ∞ if
d is not present in the list). The RRF score of d for query q is defined as:

                                       1                 1
                 RRF(q, d) =                     +                   ,               (4)
                                k + rdense (q, d) k + rsparse (q, d)

where k is a constant smoothing parameter (we set k = 60).

    Top candidates with the highest RRF(q, d) scores are filtered to drop near-
copies of the query and injected into the PoT prompt as style and API-usage
references, not logic to copy. The aim is narrow: showing the Z3 code of a sim-
ilar question lets the model pattern the unfamiliar solver API and emit fewer
malformed constraints. Task 2 does not use retrieval, as its Python is ordinary
physics arithmetic the backbone generates reliably without an exemplar. We
enabled retrieval only for the first evaluation round, so it is not part of the
submitted final-round system.

Program-of-Thought with Z3. The selected solver prompts the backbone to emit
a Python program that encodes the premises and query through a constrained set
of Z3 helper constructors rather than raw solver calls. The sandbox executes the
program, and an entailment routine applies a two-step unsatisfiability test using
Satisfiability Modulo Theories (SMT). We formalize this verification process as
follows:

Definition 2 (SMT-based Entailment and Contradiction). Let P =
{p1 , p2 , . . . , pN } be a set of FoL formulas representing the natural language premises,
and let C be the logical formula representing the query. Let Sat(Φ) denote a
boolean function that returns True if the logical formula Φ is satisfiable, and
False otherwise. The entailment status of C with respect to P is defined as:
                                                        V              
                                                            N
                                
                                
                                 Entailed,       if Sat    i=1 p i ∧ ¬C   = False,
                                                         V            
            Status(P, C) = Contradicted, if Sat             N                         (5)
                                                           i=1 pi ∧ C = False,
                                
                                  Uncertain,      otherwise.
                                


    Each solver maps this status to its respective format: a Yes/No/Uncertain
label for YNU, a per-option status for MCQ, and the set of entailed facts for
OE. Grounding the answer in the solver verdict rather than the model’s own
claim is what keeps the deduction hallucination-free. We state the correctness of
this symbolic grounding in the following proposition:
                                                            CoTu at EXACT 2026       9

Proposition 1 (Soundness of Symbolic Grounding). Assuming that the
natural language premises and the query are faithfully translated into their re-
spective FoL formulas P and C, the solver verdict Status(P, C) is sound with
respect to classical first-order logic semantics:
                                        VN
 1. If Status(P, C) = Entailed, then i=1 pi |= C.
                                           VN
 2. If Status(P, C) = Contradicted, then i=1 pi |= ¬C.

   The shared refinement stage then writes the verdict into the JSON schema
and, for Task 1, emits the indices of the premises that support the answer; these
are scored as the automatic premise-F1 component (P2) and therefore matter
as much as the answer itself under the Task 1 metric.

Latency Fallback. The main solver runs the backbone with thinking enabled at
every generation step—code generation, self-correction, and output writing—
which drives its accuracy but also makes a single reasoning-heavy pass liable to
exceed the challenge’s per-query time limit. We therefore run this solver asyn-
chronously alongside a faster self-consistency runner that drops the thinking
budget. We formalize this dual-path routing and voting fallback mechanism as
follows:
    Let amain be the answer generated by the main thinking solver, and let d be
its execution time. Let tfallback denote the safety time limit (where tfallback < T =
60 seconds). The self-consistency runner samples M independent non-thinking
reasoning paths, yielding a set of candidate answers A = {a1 , a2 , . . . , aM }, where
each ai is a tuple consisting of the predicted answer value ŷi and the set of cited
premises Pi .
    The majority vote set Vmaj of the candidate answers is defined as:
                                              M
                                              X
                           Vmaj = arg max           I(ŷi = y),                    (6)
                                        y∈Y
                                              i=1

where Y is the space of all possible answers, and I(·) is the indicator function. If
there is a tie, i.e., |Vmaj | > 1, we break the tie by selecting the candidate citing
the minimum number of premises:

                             a∗ = arg min        min |Pi |.                        (7)
                                       y∈Vmaj i : ŷi =y


The final returned answer Ŷ is chosen according to the fallback decision rule:
                              (
                                amain , if d ≤ tfallback ,
                        Ŷ =                                                  (8)
                                a∗ ,    otherwise.

    By employing this fallback mechanism, a slow query degrades gracefully to
a faster consensus answer rather than causing a timeout. The two runners thus
trade accuracy for speed along a single axis—thinking versus non-thinking on the
same model—and the concrete timeouts and sample count are given in Section 4.
10      Quoc-Khang et al.

3.3   Task 2: Physics Problems

Task 2 solves text-based physics problems, centered on electric circuits and elec-
trostatics but extending to broader introductory-physics topics such as mechan-
ics, thermodynamics, and optics. Every item calls for a numerical answer, with
a physical unit where the quantity carries one. At evaluation the branch receives
only the question, with no premises or formula sheet, so it must recover the
governing laws from parametric memory and turn them into a computation. As
the Task 2 branch of Figure 1 shows, it reuses the same PoT, sandbox, and self-
correction machinery as Task 1, but generates plain numerical Python that is
evaluated directly instead of Z3 constraints, and uses no retrieval, since ordinary
physics arithmetic is code the backbone produces reliably without an exemplar.

Program-of-Thought Solver. The solver prompts the backbone to emit a Python
program that sets up the relevant equations and computes the result through
multi-step arithmetic. We formalize the Program-of-Thought (PoT) computation
process for physics problems as follows:

Definition 3 (Physics Computation). Let Q be a physics problem query
containing a set of known input physical variables Vin = {v1 , v2 , . . . , vm } and a
target quantity y. A PoT program π is defined as a sequence of L assignment
steps:
               vj ← ϕj ({vi }i<j , Cphys ) , j = m + 1, . . . , m + L,             (9)
where Cphys is a set of standard physical constants, ϕj is a physical formula or
numerical operation, and the final assignment yields the predicted target value
ŷ = vm+L .

    The sandbox executes the program π with numerical Python, exposing SciPy [20]
so the program can pull physical constants Cphys , such as the vacuum permittiv-
ity ε0 and the elementary charge e, from its scipy.constants tables. This avoids
hard-coding rounded values whose accumulated error could push the predicted
value ŷ outside the challenge’s relative-tolerance band. A failure to parse or ex-
ecute the sequence of assignments in Equation (9) is fed back for regeneration
under the same fixed retry budget as Task 1 (Section 4). Where an answer carries
a unit, the challenge scores it as part of answer correctness, so the solver emits
the unit alongside the value and the shared refinement stage keeps the two to-
gether. The premises_used field, which carries gold supporting-premise indices
in Task 1, here records the physical laws and formulas the solution invoked; it is
not scored, as the Task 2 metric is answer-only (Section 2.2).


3.4   Data Preparation and Supervised Fine-Tuning

The two SFT checkpoints behind the backbone (Section 3.1) share a recipe: we
clean and augment the official EXACT 2026 release into a task-specific set, re-
annotate it with reasoning traces from a stronger offline teacher, and fine-tune
GRM-2.5 to reproduce those traces. Two teacher models are used, both strictly
                                                      CoTu at EXACT 2026         11

Table 1. Data preparation for the two SFT sets. Task 1 is filtered by the live clar-
ity check (Section 3.2) and rebalanced with Z3-verified open-ended items; Task 2 is
augmented with synthesized multiple-choice items. Synthesis teachers are offline and
non-competing.

Task Data stage                                                              Items
Task 1    Official logic-query release                                          808
          After clarity filter (403 YNU / 314 MCQ / 5 OE)                       722
            + synthesized OE (Z3-verified)                                      333
          Total Task 1                                                        1,055
Task 2    Official physics set                                                1,352
            + synthesized MCQs (Qwen3.6-27B)                                    100
          Total Task 2                                                       1,452



offline for data preparation and never on the live solver path: DeepSeek-V4-Pro
for reasoning-trace re-annotation and Qwen3.6-27B 4 for Task 2 item synthesis.
We disclose both as non-competing, per the challenge rules.

Task 1 Data. We start from the official logic-query release and pass each item
through the same clarity check the live solver uses (Section 3.2), keeping only the
items it labels well-formed and dropping those with missing symbol definitions
or unresolved references. The clean set is skewed by answer type toward YNU
and MCQ, with only five open-ended items, so we synthesize additional open-
ended items with the teacher, discharging each candidate through Z3 and keeping
only those whose synthesized answer the solver confirms, so the augmentation
inherits the same symbolic grounding as the solver itself. Table 1 summarizes
the resulting item counts at each stage.

Task 2 Data. We start from the official physics set and add multiple-choice
items synthesized from existing questions with Qwen3.6-27B, broadening answer-
format coverage beyond the numerical-only originals (Table 1).

Re-annotation and Fine-tuning. For both tasks we re-annotate every item with
DeepSeek-V4-Pro, recording its thinking trace alongside the answer, explana-
tion, and generated program, and keep the executable trace as the fine-tuning
target. We then run separate Task 1 and Task 2 SFT of GRM-2.5 on these traces
with LoRA [7], computing loss only over the assistant’s reasoning and code so the
model learns to produce the structured PoT output the pipeline consumes; the
trained adapters are merged back into the backbone and released as standalone
checkpoints. The goal is narrow: a 4B backbone follows the pipeline’s CoT/PoT
instructions and per-task output formats far more reliably after distilling the
4
    https://huggingface.co/Qwen/Qwen3.6-27B
12     Quoc-Khang et al.

teacher’s traces than the base model does. The two checkpoints are released
as CoTuGRM-2.5.T1-SFT5 and CoTuGRM-2.5.T2-SFT6 . The exact training
hyperparameters, including LoRA settings, learning rates, and epochs, are de-
tailed in Section A. Replacing the base backbone with these checkpoints between
Round 1 and Round 2 raises accuracy and cuts response time, as Sections 5.1
and 5.2 report.


4     Experimental Setup
We now detail the runtime configuration under which CoTu produced the scores
in Section 5: the compliance-relevant model sizes (Section 4.1), the serving and
decoding setup together with the self-correction and latency-fallback budgets
deferred from the methodology (Section 4.2), and the structure of the evaluation
rounds (Section 4.3).

4.1   Compliance and Model Configuration
All competition-eligible runs use only open-weight models within the challenge’s
8-billion parameter ceiling, served on our own hardware. The ceiling applies
to the generation LLMs; non-generative LLMs, such as the embedding model
used for retrieval, do not count against it. Table 2 lists every model on the
live inference path with its size, role, and the rounds in which it ran. Every
generation model derives from the 4B backbone GRM-2.5: Round 1 runs the
base backbone on both tasks, while Rounds 2 and 3 run the two task-specific
SFT checkpoints, which are LoRA fine-tunes merged back into the 4B backbone
and so stay within the ceiling. The dense retriever Qwen3-Embedding-0.6B is
active on the Task 1 branch for the first round only. The two offline teachers used
for data preparation, DeepSeek-V4-Pro and Qwen3.6-27B, exceed the ceiling but
never run on the live path; we disclose them as non-competing and omit them
from the table. We serve the generation models in BF16 and enable thinking on
the reasoning-heavy steps, such as code generation7 , preserving the reasoning
quality that long-thinking, hard problems demand.

4.2   Serving and Inference
We serve the backbone with SGLang and DFLASH speculative decoding on a
single NVIDIA B200 GPU for all rounds. The self-correction loop shared by
both branches regenerates code on any parse or execution failure for at most
two iterations before the branch returns its best available result. On Task 1, the
latency fallback runs the self-consistency runner in non-thinking mode with three
5
  TODO: insert link to the model
6
  TODO: insert link to the model
7
  Code generation is the hardest step on Task 1: the model must encode every natural
  language premise as a correct first-order-logic statement in the Z3 program, so a
  single mis-encoded premise can change the solver verdict.
                                                         CoTu at EXACT 2026             13

Table 2. Models on the live inference path and their compliance with the EXACT
2026 8B open-weight ceiling. The base backbone runs in Round 1; the two task-specific
SFT checkpoints (Section 3.4), LoRA fine-tunes merged into the same 4B backbone,
run in Rounds 2–3. Offline data-preparation teachers are non-competing and omitted;
the non-generative retriever, active in Round 1 only, does not count against the ceiling.

Role                       Model                                   Size Rounds ≤ 8B
Backbone (both tasks)      OrionLLM/GRM-2.5                        4B       1       ✓
Task 1 solver              CoTuGRM-2.5.T1-SFT                      4B      2–3      ✓
Task 2 solver              CoTuGRM-2.5.T2-SFT                      4B      2–3      ✓
Retriever (Task 1)         Qwen3-Embedding-0.6B                    0.6B     1       ✓



sampled paths and supplies the answer when the main solver—which generates
with thinking enabled—does not respond within 54 s, well inside the T = 60 s
per-query hard limit.

4.3    Evaluation Rounds
The challenge ran three rounds. The two automated rounds (Round 1 and Round
2) score P1 and P2 with the time bonus of Equation (1) and select teams for
the final round; each covers 25 Task 1 and 25 Task 2 items. Round 2 evaluates
a refined submission over the same task structure as Round 1. The final round
(Round 3) is a live evaluation among the top teams: its automated API score
SAPI combines P1 and P2 without the time bonus over 6 Task 1 and 5 Task 2
items, and it adds the manually judged reasoning-depth score P3 and a presenta-
tion score, aggregated as Equation (3). We report Rounds 1 and 2 as automated
selection rounds and Round 3 as the scored final.


5     Results
We report CoTu’s official scores across the three evaluation rounds, then char-
acterize response time and the latency fallback (Section 5.2) and analyze the
remaining failures (Section 5.3). All numbers are official leaderboard scores un-
der the metrics of Section 2.2.

5.1    Official Leaderboard Results
Table 3 reports the two automated selection rounds. CoTu scores a perfect Task 2
(25/25) in both Round 1 and Round 2, so its answer-only physics solver answers
all 50 items correctly under the P1 metric. Task 1 accounts for the improvement:
its combined P1+P2 score rises from 21.24/25 in Round 1 to 23.10/25 in Round
2. The principal change between the two rounds is the model: Round 1 runs the
base GRM-2.5 backbone, while Round 2 swaps in the task-specific SFT check-
points, alongside a refined surrounding pipeline, and the score rises with them.
14      Quoc-Khang et al.

Table 3. Automated selection rounds. Task 1 is scored on answer correctness (P1)
and premise F1 (P2), combined as 21 P1 + 21 P2; Task 2 on answer correctness (P1). The
time bonus score B (Equation (1)) is added on top (Equation (2)). Each round covers
25 Task 1 and 25 Task 2 items, so every column is out of 25.

Round                                      Task 1           Task 2 Bonus          Total
                                     P1    P2     P1+P2       P1      B         (Rank)
Round 1 Selection round 1           21.00 21.48   21.24      25.00   2.78   49.02 (4/50)
Round 2 Selection round 2           22.00 24.20   23.10      25.00   4.10   52.20 (6/35)

Table 4. Final round (Round 3) score breakdown, over 6 Task 1 and 5 Task 2 items.
The technical score Stech sums the automated API score and the manual reasoning
score P3; the overall score adds presentation (Equation (3)). CoTu’s Stech is the highest
among all teams.

Component                                                                          CoTu
Automated API                                         SAPI (max. 11 pts)           10.24
Reasoning depth                                       P3 (max. 4 pts)               3.20
Technical                                             Stech (max. 15 pts)         13.44
  runner-up technical                                 (max. 15 pts)                12.51
Presentation                                          Spres (max. 15 pts)           8.80
Overall                                               Sr3                   22.24 (3rd)



The P1/P2 split in Table 3 locates the gain: premise F1 (P2) rises from 21.48
to 24.20 while answer correctness (P1) improves more modestly from 21.00 to
22.00, so the fine-tuning helped mainly in premise selection rather than deduc-
tion. The time bonus also improves, from 2.78 to 4.10, as the SFT checkpoints
return correct answers faster than the base backbone (Section 5.2). Both rounds
place CoTu well inside the qualifying band for the final round.
    The final round (Round 3) drops the time bonus and adds manual reasoning
and presentation scoring. Table 4 breaks down CoTu’s result. The automated
API score is 10.24/11, which with a reasoning-depth score of 3.20/4 gives a
technical score Stech = 13.44/15—the highest of any team, ahead of the runner-
up’s 12.51/15. The presentation score of 8.80/15 brings the overall final score to
22.24, placing CoTu 3rd overall. The technical lead and the 3rd-place finish are
therefore separate facts: CoTu produced the strongest system on the automated
and expert-judged reasoning metrics, while the presentation component, which
weighs equally with the full technical score, moved the overall ranking.

5.2   Response Time and Latency Fallback
The EXACT time bonus rewards answering quickly, but only on items answered
correctly, and the serving stack (Section 4.2) was built to stay well inside the
                                                        CoTu at EXACT 2026          15

Table 5. Per-query response time and latency-fallback usage across the three rounds,
from the official run logs. Mean time is over the 25 Task 1 and 25 Task 2 items in each
automated round and the 6 Task 1 and 5 Task 2 items in the final round. “Fallback”
counts Task 1 queries whose result came from the self-consistency fast runner after the
main solver exceeded the 54 s budget; it is Task 1-only by design and never fired on
Task 2. The time bonus score B is not awarded in the final round.

Round                                              Mean time (s) Fallback Bonus
                                                   Task 1 Task 2      Task 1        B
Round 1 Base backbone                               32.51    17.20     5/25       2.78
Round 2 SFT checkpoints                             12.05     4.21     0/25       4.10
Round 3 SFT checkpoints                             18.00    10.63     0/6          —



T = 60 s per-query limit. Table 5 reports mean per-query response time from
the official run logs, alongside how often the Task 1 latency fallback emitted the
self-consistency runner’s result in place of the main solver.
    Three patterns stand out. First, mean response time drops sharply from
Round 1 to Round 2 on both tasks: Task 1 from 32.51 s to 12.05 s and Task 2
from 17.20 s to 4.21 s. Round 1 ran the base GRM-2.5 backbone while Round 2
ran the task-specific SFT checkpoints, so the drop is consistent with the SFT
checkpoints being faster. A plausible mechanism is that fine-tuning on reasoning
traces distilled from the stronger DeepSeek-V4-Pro teacher steers the model
onto shorter, more direct solution trajectories, so it settles on an answer with
less intermediate reasoning. The two rounds use different item sets and Round
2 also refined the surrounding pipeline, so we read this as supporting evidence
rather than a controlled measurement, which would require holding pipeline and
items fixed while swapping only the model. Second, response time rises again in
the final round (18.00 s on Task 1 and 10.63 s on Task 2) even though Round 3
runs the same SFT checkpoints as Round 2. The final round is a smaller, harder
live evaluation, and the accuracy drop reported in Section 5.3 is consistent with
this, so the longer times point to items that require more reasoning effort to solve
rather than a regression in the solver. Third, the latency fallback was needed
only in Round 1, where it fired on 5 of 25 Task 1 items (20%). In Rounds 2 and 3
no query reached the 54 s fallback threshold—the slowest Task 1 item in Round
2 finished in 18.4 s—so the fallback went from a regularly exercised safety net to
an inactive one. It is a Task 1-only mechanism by design and never triggered on
Task 2. The faster responses also lifted the time bonus, from 2.78 to 4.10, since
it rewards correct answers returned quickly.


5.3   Error Analysis

We inspect the per-query logs from all three rounds to characterize where CoTu
still fails. Across every round, all incorrect items fall on Task 1: the Task 2 solver
is correct on every automated- and final-round item. The failures are therefore
16     Quoc-Khang et al.

confined to Task 1, and they split into two modes matching the Task 1 metric:
wrong answer, where the deduction itself is incorrect, and wrong premises, where
the answer is correct but the cited supporting premises miss the gold set and
lose P2.
    In Round 1, 36 of 50 items are fully correct; of the 14 Task 1 misses, 10 are
premise-selection errors and 4 are wrong answers, so most of the lost Task 1 score
is premise F1 (P2) rather than deduction. Round 2 shows the effect of the refined
submission: 45 of 50 correct, with only 2 premise errors and 3 wrong answers
on Task 1. In the final round, the 6 Task 1 items break down into 2 correct, 3
premise-selection errors, and 1 wrong answer, so premise selection remains the
dominant Task 1 failure mode into the final round.
    That the leading error mode is premise selection rather than deduction is
consistent with the design: grounding the answer in the Z3 solver verdict (Sec-
tion 3.2) keeps deductions largely correct, while identifying the exact supporting
premises—scored as P2 and weighted equally with answer correctness under
ST1 —remains the harder subproblem.


6    Conclusion

In this work, we presented team CoTu’s submission to EXACT 2026, a neuro-
symbolic system for transparent educational QA under the challenge’s open-
weight, 8B-parameter ceiling. Instead of answering directly, the GRM-2.5 back-
bone writes a program that is executed to obtain the answer: a Z3 encoding
whose entailment verdict grounds each regulation query in Task 1, and numer-
ical Python for the physics problems in Task 2, with both branches sharing a
self-correction loop and a unified explained-JSON output. The system achieved
a perfect Task 2 score in both automated rounds and obtained the highest final-
round technical score of any team (Stech = 13.44/15); with the equally weighted
presentation score included, CoTu placed 3rd overall. Grounding deduction in
a symbolic solver kept answers correct and verifiable at the 4B scale, leaving
premise selection, rather than the deductions themselves, as the main remaining
source of error.

Limitations. The main residual error mode is premise selection (P2) rather
than answer correctness: the Z3 verdict keeps Task 1 deductions largely cor-
rect, but identifying the exact supporting premises, weighted equally with the
answer, remains the harder subproblem. Our data pipeline also depends on two
offline teacher models—DeepSeek-V4-Pro for reasoning-trace re-annotation and
Qwen3.6-27B for Task 2 item synthesis—that exceed the 8B ceiling. Both are dis-
closed as non-competing and never enter the live inference path, yet the quality
of the fine-tuned checkpoints still rests on this distillation.

Future work. The most immediate priority is premise selection. Tighter attribu-
tion between the Z3 encoding and the cited premise indices, or joint optimiza-
tion of deduction and citation, would target the error mode that accounts for
                                                         CoTu at EXACT 2026           17

most of our lost P2. A second direction is to reduce the reliance on large of-
fline teachers by generating reasoning traces on-policy from the backbone itself
and retaining only the Z3 and Python programs whose executions verify. Our
pipeline already runs the solver that provides this correctness signal, the same
signal that three lines of recent work build a training loop around: rejection-
sampling and self-taught fine-tuning, which keep model-generated solutions that
pass a check [27,18,26]; execution-feedback self-training for programs, which fil-
ters candidates by running them against synthesized tests [23]; and reinforcement
learning with verifiable rewards, which optimizes the policy directly against a
deterministic correctness signal rather than distilling filtered traces [5,28,25].
Finally, extending symbolic grounding to Task 2, through dimensional and unit
checking or verification of retrieved formulas, would carry the deterministic guar-
antees that anchor Task 1 to the physics branch as its domain widens.


References
 1. Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Nee-
    lakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A.,
    Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D.M., Wu, J., Win-
    ter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark,
    J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D.: Language
    models are few-shot learners. In: Advances in Neural Information Processing Sys-
    tems 33: Annual Conference on Neural Information Processing Systems 2020,
    NeurIPS 2020. pp. 1877–1901 (2020), https://proceedings.neurips.cc/paper/2020/
    hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html
 2. Chang, Y., Wang, X., Wang, J., Wu, Y., Yang, L., Zhu, K., Chen, H., Yi, X., Wang,
    C., Wang, Y., Ye, W., Zhang, Y., Chang, Y., Yu, P.S., Yang, Q., Xie, X.: A survey
    on evaluation of large language models. ACM Transactions on Intelligent Systems
    and Technology 15(3), 1–45 (2024). https://doi.org/10.1145/3641289
 3. Chen, J., Liang, Y., Liu, Z.: DFlash: Block diffusion for flash speculative decoding.
    arXiv preprint arXiv:2602.06036 (2026), https://arxiv.org/abs/2602.06036
 4. Cormack, G.V., Clarke, C.L.A., Buettcher, S.: Reciprocal rank fusion outper-
    forms condorcet and individual rank learning methods. In: Proceedings of the
    32nd International ACM SIGIR Conference on Research and Development in
    Information Retrieval. p. 758–759. SIGIR ’09, Association for Computing Ma-
    chinery, New York, NY, USA (2009). https://doi.org/10.1145/1571941.1572114,
    https://doi.org/10.1145/1571941.1572114
 5. DeepSeek-AI: DeepSeek-R1: Incentivizing reasoning capability in LLMs via
    reinforcement learning. Nature 645, 633–638 (2025). https://doi.org/10.1038/
    s41586-025-09422-z, https://arxiv.org/abs/2501.12948
 6. d’Avila Garcez, A., Lamb, L.C.: Neurosymbolic AI: the 3rd wave. Arti-
    ficial Intelligence Review 56, 12387–12406 (2023). https://doi.org/10.1007/
    s10462-023-10448-w
 7. Hu, E.J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W.:
    LoRA: Low-rank adaptation of large language models. In: International Conference
    on Learning Representations (ICLR) (2022)
 8. Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng,
    W., Feng, X., Qin, B., Liu, T.: A survey on hallucination in large language mod-
18      Quoc-Khang et al.

    els: Principles, taxonomy, challenges, and open questions. ACM Transactions on
    Information Systems 43(2), 1–55 (2025). https://doi.org/10.1145/3703155
 9. Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A.,
    Fung, P.: Survey of hallucination in natural language generation. ACM Computing
    Surveys 55(12), 1–38 (2023). https://doi.org/10.1145/3571730
10. Kalajdzievski, D.: A rank stabilization scaling factor for fine-tuning with LoRA.
    arXiv preprint arXiv:2312.03732 (2023)
11. Kamalloo, E., Dziri, N., Clarke, C., Rafiei, D.: Evaluating open-domain question
    answering in the era of large language models. In: Proceedings of the 61st Annual
    Meeting of the Association for Computational Linguistics (Volume 1: Long Pa-
    pers). pp. 5591–5606. Association for Computational Linguistics, Toronto, Canada
    (Jul 2023). https://doi.org/10.18653/v1/2023.acl-long.307, https://aclanthology.
    org/2023.acl-long.307/
12. Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vard-
    hamanan, S., Haq, S., Sharma, A., Joshi, T.T., Moazam, H., Miller, H., Za-
    haria, M., Potts, C.: DSPy: Compiling declarative language model calls into self-
    improving pipelines. arXiv preprint arXiv:2310.03714 (2023), https://arxiv.org/
    abs/2310.03714
13. Kojima, T., Gu, S.S., Reid, M., Matsuo, Y., Iwasawa, Y.: Large language models
    are zero-shot reasoners. In: Advances in Neural Information Processing Systems
    35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS
    2022. pp. 22199–22213 (2022), https://proceedings.neurips.cc/paper_files/paper/
    2022/hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html
14. Minaee, S., Mikolov, T., Nikzad, N., Chenaghlu, M., Socher, R., Amatriain, X.,
    Gao, J.: Large language models: A survey. arXiv preprint arXiv:2402.06196 (2024),
    https://arxiv.org/abs/2402.06196
15. de Moura, L., Bjørner, N.: Z3: an efficient smt solver. In: Tools and Algorithms
    for Construction and Analysis of Systems. pp. 337–340. Springer, Berlin, Hei-
    delberg (March 2008), https://www.microsoft.com/en-us/research/publication/
    z3-an-efficient-smt-solver/
16. Nguyen, L.S.T., Vo, K.H.N., Nguyen, T.H.A., Bui, T.C., Nguyen, D.Q., Tran, T.T.,
    Nguyen, A.D., Nguyen, M.L., Baldacci, F., Bui, T.H., Nardo, E.D., Ciaramella, A.,
    Le, S.H., Ullah, I., Rocco, L.D., Quan, T.T.: Bridging llms and symbolic reason-
    ing in educational qa systems: Insights from the xai challenge at ijcnn 2025. In:
    ITADATA (2025), https://ceur-ws.org/Vol-4152/paper98.pdf
17. Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C.L., Mishkin,
    P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J.,
    Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano,
    P.F., Leike, J., Lowe, R.: Training language models to follow instructions
    with human feedback. In: Advances in Neural Information Processing Sys-
    tems 35: Annual Conference on Neural Information Processing Systems 2022,
    NeurIPS 2022 (2022), https://proceedings.neurips.cc/paper_files/paper/2022/
    hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html
18. Singh, A., Co-Reyes, J.D., Agarwal, R., Anand, A., Patil, P., Garcia, X., Liu,
    P.J., Harrison, J., Lee, J., Xu, K., Parisi, A., Kumar, A., Alemi, A., Rizkowsky,
    A., Nova, A., et al.: Beyond human data: Scaling self-training for problem-solving
    with language models. Transactions on Machine Learning Research (2024), https:
    //arxiv.org/abs/2312.06585
19. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.A., Lacroix, T.,
    Rozière, B., Goyal, N., Hambro, E., Azhar, F., Rodriguez, A., Joulin, A., Grave,
                                                          CoTu at EXACT 2026           19

    E., Lample, G.: LLaMA: Open and efficient foundation language models. arXiv
    preprint arXiv:2302.13971 (2023), https://arxiv.org/abs/2302.13971
20. Virtanen, P., Gommers, R., Oliphant, T.E., Haberland, M., Reddy, T., Courna-
    peau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S.J.,
    Brett, M., Wilson, J., Millman, K.J., Mayorov, N., Nelson, A.R.J., Jones, E., Kern,
    R., Larson, E., Carey, C.J., Polat, İ., Feng, Y., Moore, E.W., VanderPlas, J., Lax-
    alde, D., Perktold, J., Cimrman, R., Henriksen, I., Quintero, E.A., Harris, C.R.,
    Archibald, A.M., Ribeiro, A.H., Pedregosa, F., van Mulbregt, P., SciPy 1.0 Con-
    tributors: SciPy 1.0: fundamental algorithms for scientific computing in Python.
    Nature Methods 17, 261–272 (2020). https://doi.org/10.1038/s41592-019-0686-2
21. Wang, S., Xu, T., Li, H., Zhang, C., Liang, J., Tang, J., Yu, P.S., Wen, Q.: Large
    language models for education: A survey and outlook. IEEE Signal Processing
    Magazine 42(6), 51–63 (2025). https://doi.org/10.1109/MSP.2025.3594309, https:
    //doi.org/10.1109/MSP.2025.3594309
22. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V., Zhou,
    D., et al.: Chain-of-thought prompting elicits reasoning in large language models.
    Advances in neural information processing systems 35, 24824–24837 (2022)
23. Wei, Y., Cassano, F., Liu, J., Ding, Y., Jain, N., Mueller, Z., de Vries, H., von
    Werra, L., Guha, A., Zhang, L.: SelfCodeAlign: Self-alignment for code generation.
    In: Advances in Neural Information Processing Systems 37: Annual Conference on
    Neural Information Processing Systems 2024, NeurIPS 2024 (2024), https://arxiv.
    org/abs/2410.24198
24. Yang, X.W., Shao, J.J., Guo, L.Z., Zhang, B.W., Zhou, Z., Jia, L.H., Dai, W.Z.,
    Li, Y.F.: Neuro-symbolic artificial intelligence: Towards improving the reasoning
    abilities of large language models. In: Proceedings of the Thirty-Fourth Inter-
    national Joint Conference on Artificial Intelligence, IJCAI-25. pp. 10770–10778.
    International Joint Conferences on Artificial Intelligence Organization (2025).
    https://doi.org/10.24963/ijcai.2025/1195, survey Track
25. Yu, Q., Zhang, Z., Zhu, R., Yuan, Y., Zuo, X., Yue, Y., Fan, T., Liu, G., Liu,
    L., Liu, X., Lin, H., Lin, Z., Ma, B., Sheng, G., Tong, Y., Zhang, C., Zhang, M.,
    Zhang, W., Zhu, H., Chen, J., Chen, J., Wang, C., Yu, H., Song, Y., Wei, X.,
    Zhou, H., Liu, J., Ma, W.Y., Zhang, Y.Q., Yan, L., Qiao, M., Wu, Y., Wang,
    M.: DAPO: An open-source LLM reinforcement learning system at scale. arXiv
    preprint arXiv:2503.14476 (2025), https://arxiv.org/abs/2503.14476
26. Yuan, Z., Yuan, H., Li, C., Dong, G., Lu, K., Tan, C., Zhou, C., Zhou, J.: Scaling
    relationship on learning mathematical reasoning with large language models. arXiv
    preprint arXiv:2308.01825 (2023), https://arxiv.org/abs/2308.01825
27. Zelikman, E., Wu, Y., Mu, J., Goodman, N.D.: STaR: Bootstrapping rea-
    soning with reasoning. In: Advances in Neural Information Processing Sys-
    tems 35: Annual Conference on Neural Information Processing Systems 2022,
    NeurIPS 2022 (2022), https://proceedings.neurips.cc/paper_files/paper/2022/
    hash/639a9a172c044fbb64175b5fad42e9a5-Abstract-Conference.html
28. Zeng, H., Jiang, D., Wang, H., Nie, P., Chen, X., Chen, W.: AceCoder: Acing coder
    RL via automated test-case synthesis. In: Proceedings of the 63rd Annual Meeting
    of the Association for Computational Linguistics (Volume 1: Long Papers). Asso-
    ciation for Computational Linguistics (2025), https://arxiv.org/abs/2502.01718
29. Zhao, W.X., Zhou, K., Li, J., Tang, T., Wang, X., Hou, Y., Min, Y., Zhang, B.,
    Zhang, J., Dong, Z., Du, Y., Yang, C., Chen, Y., Chen, Z., Jiang, J., Ren, R., Li, Y.,
    Tang, X., Liu, Z., Liu, P., Nie, J.Y., Wen, J.R.: A survey of large language models.
    arXiv preprint arXiv:2303.18223 (2023), https://arxiv.org/abs/2303.18223
20      Quoc-Khang et al.

30. Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C.H., Cao, S., Kozyrakis,
    C., Stoica, I., Gonzalez, J.E., Barrett, C., Sheng, Y.: SGLang: Efficient execution
    of structured language model programs. arXiv preprint arXiv:2312.07104 (2024),
    https://arxiv.org/abs/2312.07104
                                                     CoTu at EXACT 2026        21

Table 6. LoRA configuration used to produce the Task 1 and Task 2 CoTu checkpoints
described in Section 3.4.

         Hyperparameter        Task 1 (T1-SFT)      Task 2 (T2-SFT)
         Base model           OrionLLM/GRM-2.5 OrionLLM/GRM-2.5
         Method               LoRA               LoRA
         LoRA rank r          16                 16
         LoRA α               32                 32
         LoRA dropout         0.0                0.0
         Rank-stabilized LoRA True               True
         LoRA target modules q_proj, k_proj, v_proj, o_proj,
                              gate_proj, up_proj, down_proj
         Learning rate        2 × 10−4           1 × 10−4
         LR schedule          cosine             cosine
         Warmup               0.03               0.03
         Batch size / device  1                  2
         Grad. accumulation 4                    4
         Epochs               1                  1
         Weight decay         0.01               0.01
         Optimizer            adamw_torch_fused adamw_torch_fused



A    Supervised Fine-Tuning Hyperparameters
We fine-tune a separate OrionLLM/GRM-2.5 checkpoint for each task with
LoRA [7]. Adapters are applied to all attention and MLP projection matri-
ces (Table 6) √
              and use the rank-stabilized parameterization, which rescales the
update by α/ r [10] to keep the effective learning rate stable. The loss is com-
puted only over the model’s reasoning trace (⟨think⟩ . . . ⟨/think⟩) and its final
response, with the prompt tokens masked out. After training, the LoRA adapters
are merged into the base weights and released as standalone checkpoints. The
two tasks share the configuration in Table 6 and differ only in learning rate and
per-device batch size.
