                                         FMC: Formalization of Natural Language Mathematical Competition Problems


                                                           Jiaxuan Xie 1 Chengwu Liu 1 Ye Yuan 1 Siqi Li 1 Zhiping Xiao 2 Ming Zhang 1


                                                                  Abstract                                      languages have been introduced into LLM mathematical
                                                                                                                reasoning.
                                              Efficient and accurate autoformalization methods,
                                              which leverages large-scale datasets of extensive                 A formal language is a logical system in which statements
                                              natural language mathematical problems to con-                    and derivations can be verified through an interactive the-
arXiv:2507.11275v1 [cs.CL] 15 Jul 2025




                                              struct formal language datasets, are key to advanc-               orem prover, thereby mitigating the hallucination problem.
                                              ing formal mathematical reasoning. In this paper,                 However, formal reasoning introduces a new challenge—an
                                              we propose an autoformalization pipeline based                    even greater scarcity of data. To address this challenge,
                                              on large language models with error feedback,                     research on formal mathematical reasoning has primarily
                                              achieving a fully automatic and training-free for-                followed two directions: automated theorem proving and
                                              malization approach. Using this pipeline, we cu-                  autoformalization, with the latter often serving as a source
                                              rate an Olympiad-level dataset aligning natural                   of training data for the former. This work focuses on the
                                              language problems with Lean formalizations. The                   autoformalization of mathematical problems presented in
                                              dataset comprises 3, 922 mathematical problems                    natural language.
                                              in natural language and 9, 787 in Lean, of which                  We propose an enhanced autoformalization pipeline with
                                              64.46% were assessed as at least above-average                    error feedback. Built upon the stages of formal translation –
                                              quality, making it suitable as a benchmark for au-                formal verification – back translation – consistency check,
                                              tomated theorem provers. Additionally, we inves-                  our pipeline collects error information from the verification
                                              tigate the formalization and reasoning capabilities               and consistency stages. These errors, along with the original
                                              of various LLMs and empirically demonstrate that                  natural language problem, are fed back into the formaliza-
                                              few-shot learning, error feedback, and increasing                 tion model for a second translation, enabling the model to
                                              sampling numbers enhance the autoformalization                    perform self-correction.
                                              process. Experiments of three automated theorem
                                              provers on the FMC dataset also highlights its                    Using this pipeline, we construct a dataset of aligned natural
                                              challenging nature and its value as a benchmark                   language–Lean pairs, focusing specifically on mathematical
                                              for formal reasoning tasks.                                       problems of Olympiad difficulty. The original natural lan-
                                                                                                                guage problems are sourced from IMOmath, which curates
                                                                                                                problems from various national and international Olympiad
                                                                                                                competitions. After preprocessing, the problems are passed
                                         1. Introduction
                                                                                                                through our formalization pipeline, yielding a dataset of
                                         Large language models (LLMs), due to their strong textual              3, 922 natural language problems aligned with 9, 787 for-
                                         reasoning capabilities, have been widely applied to mathe-             mal statements.
                                         matical problem reasoning. Initially developed for reason-
                                                                                                                In evaluating the pipeline, we adopt syntactic validity and
                                         ing within natural language, LLMs face challenges such
                                                                                                                semantic consistency as key metrics. Our method achieves
                                         as the scarcity of complex mathematical data and the oc-
                                                                                                                a syntactic validity of 93.39% and semantic consistency of
                                         currence of hallucinations. To address these issues, formal
                                                                                                                81.74%. Compared to a closely related recent work Lean
                                            The source code and dataset are available in https://               Workbook (Ying et al., 2024), our dataset is based on sig-
                                         github.com/JadeXie1205/FMC. 1 State Key Laboratory                     nificantly more challenging problems and outperforms it’s
                                         for Multimedia Information Processing, School of Computer Sci-         autoformalization pipeline, which achieved 62.5% syntac-
                                         ence, PKU-Anker LLM Lab, Peking University, Beijing, China
                                         2
                                           Paul G. Allen School of Computer Science and Engineering, Uni-       tic validity and 17.5% semantic consistency. Furthermore,
                                         versity of Washington, U.S.A.. Correspondence to: Zhiping Xiao         we evaluate each example using a large language model
                                         <patxiao@uw.edu>, Ming Zhang <mzhang cs@pku.edu.cn>.                   across five criteria: relevance to current research, complex-
                                                                                                                ity and depth, interdisciplinary potential, community needs
                                         The second AI for MATH Workshop at the 42 nd International             and gaps, and novelty. Overall, 64.46% of the examples are
                                         Conference on Machine Learning, Vancouver, Canada. Copyright
                                         2025 by the author(s).                                                 rated as above-average or above.

                                                                                                            1
                         FMC: Formalization of Natural Language Mathematical Competition Problems

The contributions are summarized as follows:                             mathematical reasoning—that is, they often generate plausi-
                                                                         ble but logically flawed proofs. These subtle errors are hard
  1. We propose an enhanced autoformalization pipeline                   to detect, significantly increasing the difficulty of evaluating
     using LLMs with error-feedback, enabling a fully au-                the correctness of mathematical reasoning. Some recent
     tomated, training-free formalization process.                       efforts have incorporated self-verification mechanisms to
                                                                         mitigate hallucinations (Huang et al., 2023), but the results
  2. Using this pipeline, we curate a dataset of 3, 922                  remain unsatisfactory.
     aligned natural language–Lean pairs, with problems
     sourced from national and international mathematics                 As a result, some researchers have turned to formal lan-
     Olympiads. The semantic consistency of the formaliza-               guages for mathematical reasoning. Although data for for-
     tion pipeline reaches 81.74%. Our quality assessment                mal languages are even more limited, their verifiability en-
     reveals that 64.46% of the examples are rated as above-             sures the correctness and reliability of reasoning. Formal
     average or higher quality, indicating the high quality              mathematical reasoning has thus become a research focus
     of our dataset.                                                     within the broader field of AI reasoning.

  3. We investigate the formalization and semantic align-                2.2. Formal Languages
     ment checking capabilities of different general-purpose
     LLMs and find that DeepSeek-R1 remains at the                       Formal languages express mathematics within formal sys-
     forefront. Experimental results further demonstrate                 tems. They impose strict syntactic rules, and operations
     that few-shot learning, error feedback, and increased               such as verification must adhere to logically sound infer-
     sampling per problem enhance autoformalization per-                 ence rules(Yang et al., 2024).
     formance.                                                           Currently, formal math languages such as Isabelle
                                                                         (1986) (Paulson, 1988), Coq (1989) (Paulin-Mohring, 1993),
2. Related Work                                                          and Lean (2015) (de Moura et al., 2015) have attracted
                                                                         significant attention from researchers. This study uses
2.1. Large Language Models                                               Lean (Moura & Ullrich, 2021), a modern open-source the-
Large Language Models (LLMs) represent a significant                     orem prover developed by Microsoft Research and CMU.
paradigm shift in the evolution of natural language process-             Lean combines interactive and automated theorem proving,
ing. Typically built upon the Transformer architecture and               and supports reasoning in both mathematics and complex
equipped with tens or hundreds of billions of parameters,                systems in computer engineering.
LLMs are trained on massive textual corpora. Representa-                 Mathlib is commonly used in formalizing mathemati-
tive models include PaLM(Chowdhery et al., 2023), GPT-                   cal theorems in Lean. It is a community-driven project
4(OpenAI, 2024), DeepSeek-V3(DeepSeek-AI, 2025b), and                    aimed at building a unified library of formalized mathemat-
Claude 3.7(Anthropic, 2025). Their unprecedented scale in                ics for the Lean prover. Mathlib4, the updated version
both model size and training data enables capabilities dis-              for Lean 4, includes many important mathematical objects,
tinct from smaller models—capabilities often referred to as              pre-formalized theorems, and automation strategies. Some
emergent abilities(Wei et al., 2022) These include in-context            of its metaprograms enable non-trivial proof automation.
learning, instruction following, and step-by-step reason-
ing(Zhao et al., 2025), allowing LLMs to handle complex                  2.3. Automformalization
tasks across diverse domains, including reasoning tasks.
                                                                         Autoformalization is a key research direction in formalized
Among various reasoning tasks, mathematical reasoning has
                                                                         mathematical reasoning. It is essentially a translation task:
attracted particular attention. Previous research (Yang et al.,
                                                                         converting natural language mathematical problems into
2024) has shown that using LLMs for mathematical reason-
                                                                         formal theorems or proofs using computational methods.
ing generally involves three stages: pretraining, fine-tuning
                                                                         The former can serve as benchmarks for automated theorem
with structured data, and invoking external tools. However,
                                                                         provers, while the latter can be used as training data. Early
reasoning within the scope of natural language using LLMs
                                                                         studies(Wu et al., 2022) indicate that general-purpose LLMs
still faces significant challenges, such as the scarcity of
                                                                         possess a degree of formalization ability, and training with
high-difficulty data and the problem of hallucination. First,
                                                                         formal proof data significantly improves the performance of
effective training of LLMs relies on large-scale, high-quality
                                                                         automated theorem provers.
corpora. Yet for domains like university-level mathematics,
mathematical competition problems, or research-level math-               Autoformalization is the central focus of this study. More
ematical reasoning, it is difficult to obtain sufficient data that       precisely, this work investigates how to construct a high-
include detailed reasoning processes. A more critical issue              quality, aligned dataset of natural language and formal lan-
is that LLMs are prone to hallucination when performing                  guage pairs via autoformalization, to serve as a benchmark

                                                                     2
                       FMC: Formalization of Natural Language Mathematical Competition Problems

for evaluating theorem provers.                                      ization pipeline that translates mathematical problems from
                                                                     natural language into Lean language with error feedback.
Constructing a Lean-based dataset via autoformalization
                                                                     The entire pipeline is shown in Figure 1. Each natural lan-
involves two primary steps: sourcing the original data and
                                                                     guage mathematical problem is first translated into Lean
conducting formalization. Data sources can be broadly
                                                                     language using a few-shot prompting approach and then
classified into three categories: manual curation, natural
                                                                     formally verified by Lean REPL, i.e., Lean’s syntax check.
language datasets, and automatic synthesis. Manual cura-
                                                                     Those that pass the formal verification are translated back
tion refers to the direct authoring of Lean theorems and
                                                                     into natural language and compared with the original prob-
proofs by mathematical experts. Most of the pre-proved the-
                                                                     lem to perform semantic consistency checks. Statements
orems in Mathlib fall into this category. Natural language
                                                                     that pass both the formal verification and semantic consis-
datasets such as the MATH dataset(Hendrycks et al., 2021),
                                                                     tency check are regarded as successfully formalized. In
GSM8K(Cobbe et al., 2021), and AQuA-RAT(Ling et al.,
                                                                     cases where a statement fails either check, the correspond-
2017) contain mathematical problems in natural language,
                                                                     ing error information is incorporated into a revised prompt
which can be formalized into formal language datasets. Au-
                                                                     and fed back to the translation model, enabling iterative
tomatic synthesis involves the computational generation of
                                                                     prompt refinement driven by error feedback.
new mathematical problems based on existing concepts and
theorems. Representative works include MUSTARD(Huang
et al., 2024), which first synthesizes problems in natural
language before formalizing them, and STP Lean(Dong
& Ma, 2025), which directly synthesizes problems in for-
mal language, among others (Liu et al., 2025a; Lu et al.,
2024). As for formalization methods, they can be roughly
divided into two types: manual annotation, as demonstrated
by works such as PutnamBench(Tsoukalas et al., 2024),
miniF2F(Zheng et al., 2021), and ProofNet(Azerbayev et al.,
2023); and autoformalization, which is now predominantly
powered by large language models. Our analysis of ex-
isting datasets reveals the following key observations: (1)
Datasets containing competition-level problems are usually
manually annotated and remain relatively small in scale.
(2) Extracting natural language problems from the web and
automatically formalizing them is still the dominant dataset
construction strategy. However, the difficulty levels of these                    Figure 1. Autoformalization Pipeline.
problems frequently exhibit considerable variability. (3)
Data synthesis allows for large-scale dataset generation, but
remains underexplored.                                               3.1. Translation

This study aims to construct high-quality datasets with min-         Within this autoformalization pipeline, the model is required
imal training costs. Manual annotation is labor-intensive            to translate natural language mathematical problems into for-
and prohibitively expensive, while typical data synthesis            mal language in two distinct scenarios: the first involves di-
requires substantial computational resources. Therefore, we          rect translation guided by few-shot prompting, while the sec-
adopt an approach based on autoformalization of natural              ond leverages error feedback incorporated into the prompt
language mathematical problems.                                      following a failed attempt.
Our autoformalization pipeline is inspired by the design of          The first case occurs during the initial translation of a math-
the Lean Workbook pipeline, with improvements to the base            ematical problem and is based on few-shot learning. In
translation model and the incorporation of error feedback            large language models, few-shot learning refers to solving
to enhance automation. For data selection, we focus on               tasks using prompts that include a task description and a few
Olympaid-level mathematical problems to ensure sufficient            examples, without gradient updates or fine-tuning—this
difficulty and quality in the resulting dataset.                     is known as in-context learning. Experiments on GPT-
                                                                     3(Brown et al., 2020) and related work have shown that
                                                                     few-shot learning can significantly improve performance
3. Autoformalization Pipeline Design                                 on tasks involving structured formatting or translation. In
Inspired by the formalization pipeline of the Lean Work-             this study, each translation prompt includes two fixed exam-
book(Ying et al., 2024), this paper proposes an autoformal-          ples—one from algebra and one from number theory—both
                                                                     correctly aligned in natural language and Lean. Since prob-

                                                                 3
                        FMC: Formalization of Natural Language Mathematical Competition Problems

lems in these two fields are common in math Olympiad                  the output records any compilation or type errors. This
contests, using such examples helps improve translation               approach confirms the syntactic correctness of the formal
accuracy.                                                             theorem and provides error messages for failed compila-
                                                                      tions, facilitating iterative prompt refinement based on error
Additionally, since large language models generate each
                                                                      feedback.
token by first computing a probability distribution and then
sampling from it, the output inherently contains stochastic-
ity. As a result, repeated formalization requests for the same        3.3. Backtranslation
input may yield different outputs. The temperature param-             Even when statements formalized by LLMs pass Lean’s
eter T controls the sharpness of this distribution, thereby           syntax checks, they sometimes differ semantically from the
influencing the creativity of the generated text. Since for-          original theorems—such as missing conditions, incorrect as-
malization tasks require syntactic correctness while still ben-       sumptions, or erroneous goals. These discrepancies clearly
efiting from some diversity to improve translation success,           indicate incorrect formalization. Therefore, semantic verifi-
this pipeline sets the temperature to 1.0 during formalization        cation is necessary to ensure that the formalized theorems
and samples each input five times.                                    correspond to the same mathematical problems described in
The second case arises when a theorem fails either for-               the original statements.
mal verification or semantic consistency check. In such               Although LLMs have limited formalization capabilities,
instances, the associated error information is incorporated           they are good at back translation—translating Lean-
into the prompt and fed back to the translation model. The            formalized mathematical problems back into natural lan-
model then attempts to retranslate the theorem, leveraging            guage. Comparing the consistency between two natural
the in-context learning capabilities of LLMs to produce a             language problem descriptions is a comparatively simple
valid formal representation. Experimental results demon-              task. Therefore, this autoformalization pipeline employs
strate that incorporating error feedback improves formaliza-          a “back translation—consistency check” approach to en-
tion accuracy, as detailed in the experimental section.               sure semantic equivalence. This stepwise process resembles
Additionally, since Lean focuses on theorem proving and               human reasoning and, despite introducing some noise, ef-
cannot resolve open problems lacking explicit solutions               fectively improves the overall accuracy of semantic verifica-
within the statements, it is necessary to address missing             tion. Similarly, this automated pipeline employs Deepseek-
solutions and proofs. For absent solutions, we depend on              R1(DeepSeek-AI, 2025a) as the back translation model.
the model’s reasoning capabilities, expecting it to generate
them during the formalization process. For missing proofs,            3.4. Consistency Check
the placeholder ”:= by sorry” is employed, enabling Lean              In consistency check, the goal is to verify whether the back-
to detect the omission and signal the missing proof without           translated natural language theorem is mathematically con-
triggering errors.                                                    sistent with the original theorem. The prompt sent to the
After comparing several frontier LLMs, this work directly             model explicitly emphasizes examining whether the two
employs the Deepseek-R1 (DeepSeek-AI, 2025a) as the                   problems share the same mathematical essence, aiming to
translation model. As one of the state-of-the-art large lan-          prevent incorrect judgments caused by differences in word-
guage models, Deepseek-R1 possesses strong reasoning and              ing or contextual information. Additionally, since some
in-context learning abilities, demonstrating promising per-           formalized theorems may superficially include all elements
formance in formalization. The comparison of formalization            of the original theorem but have confused conditions and
capabilities of different language models are presented in            goals, the prompt clearly instructs the model to verify the
the experimental section of this paper.                               consistency of both conditions and goals. To facilitate itera-
                                                                      tive prompt refinement based on error feedback, the model
3.2. Formal Verification                                              is also required to provide a brief rationale for its judgment,
                                                                      enabling the use of error cases in subsequent iterations.
Each translated formal theorem must undergo formal ver-
ification to ensure its syntactic correctness. In this study,         Similarly, this automated pipeline employs Deepseek-
the formal verifier from DeepSeek-Prover(Xin et al., 2024)            R1(DeepSeek-AI, 2025a) as the consistency checking
is used to submit the Lean statement to Lean 4 REPL for               model. Notably, due to Deepseek-R1’s strong reasoning ca-
validation and parsing the returned results. Specifically, for-       pabilities, it often produces extensive analytical output. To
mal verification is performed by invoking Lean 4’s interac-           facilitate the extraction of relevant information, the prompt
tive Read-Eval-Print Loop (REPL) via a Python subprocess.             explicitly restricts the output format.
The formal theorem, including Mathlib import statements,
is passed through standard input in JSON format, while


                                                                  4
                       FMC: Formalization of Natural Language Mathematical Competition Problems

4. Dataset Construction
4.1. Data Collection
To enhance dataset difficulty and ensure quality, all math-
ematical problems in this dataset are all official Olympiad
problems on the IMOmath website(IMOmath, 2025). It
covers 11 international competitions including the Interna-
tional Mathematical Olympiad (IMO), as well as 42 national
and regional Olympiad contests. The dataset spans the years
1959 to 2011 and covers six continents: Europe, Asia, North
America, South America, Oceania, and Africa. These con-
tests are either the IMO and its regional selection rounds
or other major competitions of comparable difficulty. By
selecting these sources as the original natural language data,
the dataset guarantees the integrity, correctness, and chal-              Figure 2. A failed formalization example in geometry.
lenge of the mathematical theorems. The resulting aligned
natural language–Lean dataset will facilitate the evaluation
of automated theorem provers’ capabilities.                          segment lengths are specified to be positive, with accurate
                                                                     quantitative relationships given for la , lb , lc relative to the
To collect problems, this study employed web crawling                six known segments and the final goal stated, the essential
techniques to download PDF files from relevant websites,             triangle constraint is missing. For example, the condition
and used Optical Character Recognition (OCR) to extract              that the interior angles of △ABC sum to 180° is absent, and
problem statements from the PDFs. OCR is a technology                constraints involving angle bisectors, the circumcircle, and
that converts printed text and images into machine-editable          their intersections—although implicit in the original prob-
formats (Islam et al., 2017). In this work, we used Math-            lem—are not imposed. The LLM neglects these implicit
pix (Huang et al., 2023) as the OCR tool to convert PDF              constraints during formalization. Additionally, the Lean
content into markdown files. Mathpix specializes in OCR,             statement lacks the goal of proving the conditions under
with support for multiple languages and various export for-          which the equality holds.
mats. More importantly, it is optimized for the structured
recognition of mathematical expressions, such as fractions,          This geometric problem example clearly represents a failed
subscripts, superscripts, and summations, and accurately             formalization case, yet it still passed both the formal ver-
converts them into well-formed LATEX code. This capability           ification and consistency checks in the autoformalization
is particularly critical for extracting mathematical problems        pipeline. This indicates that LLMs have limited understand-
in our study. Finally, we used regular expressions to extract        ing of geometric problems. Although some prior work has
the problem texts from the markdown files and organized              attempted autoformalization of Euclidean geometry prob-
them into JSON format. After preprocessing, we obtained a            lems(Murphy et al., 2024), even with improvements, the
total of 6,980 natural language mathematical problems.               accuracy remains around 20%. Also the LeanEuclid dataset
                                                                     construction still relies heavily on manual annotation. Such
4.2. Data Preprocessing                                              formalization approaches are evidently unsuitable for build-
                                                                     ing high-quality datasets. Therefore, this study temporarily
To further improve the quality of the formalized data, this          excludes geometry problems from the original dataset.
study conducted additional filtering on the extracted 6, 980
                                                                     The dataset also contains some mathematical problems
natural language mathematical problems. Preliminary exper-
                                                                     where a single problem includes multiple subproblems.
iments revealed that LLMs encounter significant difficulties
                                                                     These subproblems may be unrelated, may share the same
when formalizing geometry problems into Lean.
                                                                     set of conditions, or may have a hierarchical relationship.
Figure 2 presents an incorrect formalization example. The            Although the Lean system can handle multi-goal problems,
original problem, described in natural language, involves            for simplicity, multiple subproblems under the same prob-
a mathematical proposition about the internal angle bisec-           lem number are split. Specifically, the original problem is
tors of a triangle, where ma , mb , mc denote the lengths of         divided into subproblems of the form “shared conditions +
the three angle bisectors, and Ma , Mb , Mc represent their          subgoal 1,” “shared conditions + subgoal 2,” and so forth.
extended lengths intersecting the circumcircle. The objec-
                                                                     The tasks of filtering out geometry problems and splitting
tive is to prove an inequality along with the conditions for
                                                                     subgoals are also performed by the Deepseek-R1 model.
equality. In the Lean formulation, although the angles ∠A
                                                                     After these processes, a total of 4, 798 natural language
, ∠B and ∠C are constrained between 0 and π, and all six
                                                                     mathematical problems were retained.

                                                                 5
                        FMC: Formalization of Natural Language Mathematical Competition Problems

                                                                      formance in interdisciplinary potential and innovativeness.
              Table 1. The result of formalization.
                                                                      This pattern closely relates to the original data selection, as
  C LASS                                 N UMBER       R ATIO
                                                                      Olympiad-level problems tend to be relatively challenging,
  T OTAL                                     4798       100%          and the Lean community currently lacks data of comparable
  F ORMAL VERIFICATION                       4481     93.39%
      PASS AT ONE GO                         4287     89.35%
                                                                      difficulty. Overall, 64.46% of the data received ratings of
      PASS WITH ERROR FEEDBACK                194      4.04%          above average or higher, suggesting a generally acceptable
  C ONSISTENCY CHECK                         3922     81.74%          dataset quality.
      PASS AT ONE GO                         3631     75.68%
      PASS WITH ERROR FEEDBACK                291      6.07%

4.3. Dataset Construction and Evaluation
The 4, 798 natural language mathematical problems were
processed through the autoformalization pipeline in this
study. After multiple sampling rounds and error feedback
iterations, 4, 481 formalized statements passed formal ver-
ification, achieving a pass rate of 93.39%. Subsequently,
after consistency check, a natural language–Lean aligned
dataset comprising 3, 922 entries was constructed, corre-
sponding to a formalization accuracy of 81.74%. Construct-
ing this dataset cost 161, 037, 099 tokens in total, including
22, 492, 280 for prompting and 138, 544, 819 for comple-                      Figure 3. Distribution of evaluation indicators.
tion.                                                                 5. Experiments
Among the 4,481 statements that passed formal verification,
                                                                      5.1. Autoformalization Capability of Different LLMs
4,287 were verified on the first attempt, while 194 were cor-
rected and passed after error feedback, improving the formal          This paper compares the formalization capabilities of
verification pass rate by 4.04%. Of the 3, 922 entries that           Deepseek-R1, GPT-4o-mini, and Claude 3.7 Sonnet. (1)
passed consistency check, 3, 631 passed initially, and 291            Deepseek-R1(DeepSeek-AI, 2025a): Released by the
were corrected and passed after error feedback, increasing            DeepSeek team in January 2025, it emphasizes high perfor-
the consistency check pass rate by 6.07%. Detailed data               mance with low resource consumption. It supports complex
are presented in Table 1. These results demonstrate that              logical deduction and long code generation, exhibiting “re-
automated error feedback is highly effective in improving             flective” reasoning behavior, and demonstrates strong per-
formalization accuracy.                                               formance in mathematics, coding, and reasoning tasks. (2)
                                                                      GPT-4o-mini(OpenAI, 2024): Released by OpenAI in July
This study further assesses dataset quality by evaluating
                                                                      2024, this smaller, more cost-effective model compared to
each mathematical theorem along five dimensions using a
                                                                      GPT-4o excels in text and visual reasoning, mathematics,
large language model: relevance to current research, com-
                                                                      coding, and multimodal inference, featuring high resource
plexity and depth, interdisciplinary potential, community
                                                                      efficiency and low inference latency. (3) Claude 3.7 Son-
needs and gaps, and innovativeness. “Relevance to current
                                                                      net(Anthropic, 2025): Released by Anthropic in February
research” examines whether the theorem addresses actively
                                                                      2025, this model combines general large language model
studied problems or concepts in mathematics or related
                                                                      and reasoning capabilities, with self-reflective abilities dur-
fields; “complexity and depth” considers if the theorem suf-
                                                                      ing deliberation, and performs excellently in mathematics,
ficiently challenges existing theories and methods or offers
                                                                      physics, instruction following, coding, and many other tasks.
significant insights or advances; “interdisciplinary potential”
assesses opportunities for cross-disciplinary research, such          The selection of these three models primarily considers
as linking mathematics with computer science, physics, or             their strengths in reasoning and their low resource consump-
biology; “community needs and gaps” evaluates whether                 tion. They are respectively applied as the formalization
the theorem fills identified demands or gaps within the Lean          model, backtranslation model, and consistency check model
community or the broader mathematical community; and                  within the autoformalization pipeline. Experiments were
“innovativeness” gauges whether the theorem introduces                conducted on a random sample of 100 original problems
new methods, concepts, or applications. Each dimension                (including geometry problems). The results, shown in Ta-
is rated as excellent, good, above average, fair, or poor,            ble 2, indicate that at the cost of higher resource use and
with an overall rating also provided. The results, shown in           time, Deepseek-R1 significantly outperforms the other two
Figure 3, indicate strong performance in complexity and               models in formalization capability, achieving a final formal-
depth as well as community needs and gaps, but weaker per-            ization accuracy of 43%. Although the theorems formalized

                                                                  6
                        FMC: Formalization of Natural Language Mathematical Competition Problems

by GPT-4o-mini and Claude 3.7 Sonnet exhibit comparable                translation examples. The results indicate that few-shot
pass rates in formal verification, the final number of theo-           learning indeed increased the one-shot formal verification
rems passing consistency check is substantially higher for             pass rate. However, it remains unclear whether this con-
Claude 3.7 Sonnet than for GPT-4o-mini.                                tributed to differences in overall formalization accuracy.
                                                                       Although the overall accuracy difference reached as high as
To further investigate the formalization capabilities of the
                                                                       8.76%, this increase mainly arose from the second formal-
three models and their ability to assess semantic consistency,
                                                                       ization of theorems that initially failed consistency checks.
cross-experiments were conducted. Specifically, the same
                                                                       At the time of the first consistency check, formalization
model was used for both formalization and back-translation,
                                                                       accuracies were comparable (44% vs. 45%). During second
while a different model was employed for consistency check-
                                                                       formalization, only error feedback was provided without
ing. The experimental results are presented in Table 3. In
                                                                       correct sample prompts. Whether the formal statements that
the table, the first metric denotes the formal verification pass
                                                                       passed verification but failed consistency checks also served
rate, and the second indicates the consistency check pass
                                                                       as few-shot learning data and contributed to accuracy im-
rate, representing the overall formalization accuracy.
                                                                       provement under few-shot learning warrants further study.
It is observed that when using the same consistency check-             Nonetheless, the data show that few-shot learning overall
ing model, Deepseek-R1 achieves significantly higher for-              improved formalization accuracy.
mal verification and consistency check pass rates. This
indicates that Deepseek-R1 is better at ensuring both syntac-          5.3. Effect of Error Feedback
tic and semantic correctness during formalization. Although
GPT-4o-mini’s formal verification pass rate is slightly higher         Table 6 demonstrates the improvement in formalization ac-
than that of Claude 3.7 Sonnet, its consistency check pass             curacy achieved through error feedback. To ensure that
rate is notably lower. This suggests that while GPT-4o-mini            formalization results were not influenced by the number
adheres to Lean’s syntax rules, it struggles to accurately             of sampling attempts, experiments without error feedback
capture the original mathematical problem’s intent.                    also retained the second translation attempt for theorems
                                                                       that failed the first formal verification or consistency check,
Furthermore, when the same model is used for both for-                 but no error information was provided. Analysis of the
malization and backtranslation, Claude 3.7 Sonnet achieves             results shows that error messages returned by the formal
the highest consistency check pass rate when employed as               verification had a limited effect on improving the formal ver-
the consistency checker, while the results for Deepseek-R1             ification pass rate; the number of second-time passes with
and GPT-4o-mini fluctuate slightly. Manual analysis of the             error feedback (4) was roughly the same as that without
formalized mathematical problems shows that Claude 3.7                 error feedback (3). This may be because the error messages
Sonnet tends to give affirmative answers during consistency            from formal verification are structured data that the transla-
checks, meaning it more often classifies mathematically mis-           tion model finds difficult to interpret, or because the initial
matched natural language–Lean pairs as correct formaliza-              formal verification pass rate was already high and those
tions. In contrast, GPT-4o-mini adopts a stricter consistency          failed formal verification were ill-defined problems. In con-
criterion, labeling more mathematically matched pairs as               trast, for the consistency check, error feedback significantly
incorrect formalizations. Compared to these, Deepseek-R1               increased the pass rate on the second attempt, thereby im-
delivers the best overall performance, balancing precision             proving the overall formalization accuracy by 10.52%. This
and recall effectively; detailed metrics are provided in Ta-           confirms the positive impact of error feedback on enhancing
ble 4. One notable exception is that when GPT-4o-mini is               formalization accuracy.
used for both formalization and back-translation, its consis-
tency check pass rate exceeds that of Deepseek-R1—likely               5.4. Effect of Increasing Sampling Number
due to an inflated accuracy from using the same model for
both formalization and consistency checking.                           Table 7 presents experiments on increasing the sampling
                                                                       number, where the sampling number refers to how many
5.2. Effect of Few-shot Learning                                       times the same statement is input into the autoformalization
                                                                       pipeline. Experimental data show that multiple samplings
The experiments were conducted on a subset of 57 data                  significantly improve the pass rates of both the first formal
points after excluding geometric problems; the following               verification and consistency check, resulting in an overall
two experiments also used this subset. Table 5 presents the            increase of 31.57% in formalization accuracy. This perfor-
results of few-shot learning experiments. These experiments            mance boost is mainly attributed to the randomness and
involved error feedback and five rounds of sampling. Few-              diversity of outputs generated by large language models.
shot learning was applied only during the first formalization
attempt of each natural language mathematical theorem;
subsequent prompts contained only error feedback without

                                                                   7
                             FMC: Formalization of Natural Language Mathematical Competition Problems

                   Table 2. Model performance comparison. The number of tokens and the time are both average values.
                                                       F ORMAL VERIFICATION                                           CONSISTENCY CHECK
         M ODEL
                                           T OKEN NUMBER             T IME ( S )   PASS RATE            T OKEN NUMBER                 T IME ( S )        PASS RATE

         D EEPSEEK -R1                       10 783.79                338.16           58%                   3357.41                    94.74               43%
         GPT-4 O - MINI                       1508.33                  17.00           34%                    737.20                     3.97               11%
         C LAUDE 3.7 S ONNET                  1721.87                  43.28           31%                    881.16                    25.10               27%


Table 3. Model cross-validation results. The cell format is: Formal                    Table 5. The effect of few-shot learning on formalization accuracy.
verification pass rate/consistency check pass rate.                                                      FORMAL VERIFICATION               CONSISTENCY CHECK
                                                                                           CLASS                                                                        PASS RATE
                                                                                                        FIRST PASS    SECOND PASS      FIRST PASS      SECOND PASS
                                    CONSISTENCY CHECK MODEL
 FORMALIZATION MODEL
                                                                                         FEW- SHOT         51                4              44              8            91.22%
                          D EEPSEEK -R1    GPT-4 O - MINI   C LAUDE 3.7 S ONNET
                                                                                         ZERO - SHOT       45                5              45              2            82.46%
 D EEPSEEK -R1             58% / 43%        58% / 31%           58% / 54%
 GPT-4 O - MINI            34% / 10%        34% / 11%           34% / 22%
 C LAUDE 3.7 S ONNET       31% / 22%        31% / 14%           31% / 27%              Table 6. The effect of error feedback on formalization accuracy.
Table 4. Evaluation matrix for consistency checks of different mod-                                              FORMAL VERIFICATION             CONSISTENCY CHECK
                                                                                                CLASS                                                                    PASS RATE
els. Experiments were based on formalization model Deepseek-R1.                                                 FIRST PASS   SECOND PASS    FIRST PASS    SECOND PASS

                                                                                        WITH ERROR FEEDBACK          51           4               44            8         91.22%
                                                                                         NO ERROR FEEDBACK           52           3               46            0         80.70%
  MODEL NAME           ACCURACY     P RECISION        R ECALL      F1 SCORE
  D EEPSEEK -R1         74.1%             69.8%         93.8%        80.0%
  GPT-4 O - MINI        74.1%             77.4%         75.0%        76.2%
  C LAUDE -3-7          58.6%             57.4%         96.9%        72.1%             the Lean Workbook pipeline, which relies on expert anno-
                                                                                       tations and iterative refinement, our pipeline can automati-
                                                                                       cally generate error feedback and perform iterative prompt
5.5. Testing as a Benchmark for Automated Theorem
                                                                                       optimization based on this feedback. Moreover, all mod-
     Provers
                                                                                       els used in this pipeline are off-the-shelf general-purpose
To assess the relative difficulty of different formal mathe-                           large language models, further demonstrating the reason-
matical datasets, three state-of-the-art automated theorem                             ing and formalization capabilities of large language mod-
provers – Kimina-Prover, Goedel-Prover, and DeepSeek-                                  els while greatly reducing deployment costs. Using this
Prover-V1.5-RL – are benchmarked against established                                   autoformalization pipeline, we constructed a natural lan-
datasets MiniF2F, ProofNet, and FormalMATH(Yu et al.,                                  guage–Lean aligned dataset with a formalization semantic
2025) alongside this newly constructed formal language                                 accuracy of 81.74%, ultimately containing 3, 922 mathemat-
dataset.                                                                               ical problems in natural language and 9, 787 in Lean at the
                                                                                       difficulty level of the Olympiad mathematics competitions.
Each verification task was evaluated over 32 runs on
                                                                                       Our dataset strikes a balances bwtween scale and difficulty.
1, 000 randomly sampled problems from 9, 787 formal
                                                                                       According to quality assessments, 64.46% of the formal-
statements to improve the statistical reliability of for-
                                                                                       ized data received evaluations of at least “above average.”
mal validation, with consistent hyperparameters across
                                                                                       Furthermore, a series of ablation experiments confirmed
all provers. As shown in Table 8, our dataset achieved
                                                                                       the formalization advantages of the Deepseek-R1 model
intermediate pass rates of 15.7% (Goedel-Prover) and
                                                                                       over GPT-4o-mini and Claude 3.7 Sonnet, and verified the
13.0% (DeepSeek-Prover), positioning its difficulty between
                                                                                       positive effects of few-shot learning, error feedback, and
ProofNet (15.2% − 16.0%) and FormalMATH (10.2% −
                                                                                       increased per-problem sampling on improving formaliza-
16.5%). These results demonstrate that our dataset not only
                                                                                       tion accuracy. We evaluated three state-of-the-art automated
presents a meaningful level of challenge but also effectively
                                                                                       theorem provers on a subset of the FMC dataset, highlight-
differentiates the performance of provers on moderately
                                                                                       ing its challenging nature and its value as a benchmark for
complex formal reasoning tasks, highlighting its competi-
                                                                                       formal reasoning tasks.
tiveness as a benchmark.
                                                                                       Regarding the raw data, due to the expressive limitations
6. Conclusion                                                                          of the Lean language, this study excluded all geometric
                                                                                       mathematical problems. Geometric problems hold a crucial
This paper reviews existing natural language–Lean aligned                              position not only in the field of competitions but also across
mathematical problem datasets and points out that datasets                             the entire domain of mathematical research. Therefore, fur-
at competition-level difficulty tend to be relatively small,                           ther development of Lean in this area, or the emergence
while other automatically constructed formalization datasets                           of new formal languages with better support for geometric
often lack guaranteed difficulty. To address this, we propose                          mathematics, is highly anticipated. In terms of autoformal-
an autoformalization pipeline with error feedback inspired                             ization, due to constraints on computational resources and
by the Lean Workbook formalization framework. Unlike                                   time, this study only performed 5 samplings per problem.

                                                                                   8
                              FMC: Formalization of Natural Language Mathematical Competition Problems

Table 7. The effect of increasing sampling number on formaliza-                                  Gray, S., Chess, B., Clark, J., Berner, C., McCandlish,
tion accuracy.                                                                                   S., Radford, A., Sutskever, I., and Amodei, D. Lan-
    CLASS
                FORMAL VERIFICATION              CONSISTENCY CHECK
                                                                               PASS RATE
                                                                                                 guage models are few-shot learners. In Proceedings of
              FIRST PASS   SECOND PASS        FIRST PASS     SECOND PASS                         the 34th International Conference on Neural Informa-
  SAMPLE @1      36                5                28             6            59.65%           tion Processing Systems, NIPS ’20, Red Hook, NY, USA,
  SAMPLE @5      51                4                44             8            91.22%
                                                                                                 2020. Curran Associates Inc. ISBN 9781713829546.
Table 8. Test results of different automated theorem provers. Each
verification task was evaluated over 32 runs on 1, 000 randomly                                Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra,
sampled formal problems.                                                                         G., Roberts, A., Barham, P., Chung, H. W., Sutton,
                                                                                                 C., Gehrmann, S., Schuh, P., Shi, K., Tsvyashchenko,
 DATASET        K IMINA -P ROVER       G OEDEL -P ROVER    D EEP S EEK -P ROVER -V1.5-RL
 M INI F2F            63.1%                 57.6%                      50.0%
                                                                                                 S., Maynez, J., Rao, A., Barnes, P., Tay, Y., Shazeer,
 P ROOF N ET            -                   15.2%                      16.0%                     N., Prabhakaran, V., Reif, E., Du, N., Hutchinson, B.,
 F ORMAL MATH         16.5%                 13.5%                      10.2%
 FMC                  16.4%                 15.7%                      13.0%                     Pope, R., Bradbury, J., Austin, J., Isard, M., Gur-Ari,
                                                                                                 G., Yin, P., Duke, T., Levskaya, A., Ghemawat, S., Dev,
                                                                                                 S., Michalewski, H., Garcia, X., Misra, V., Robinson,
Under more favorable conditions, increasing the number of
                                                                                                 K., Fedus, L., Zhou, D., Ippolito, D., Luan, D., Lim,
samplings could potentially yield higher formalization accu-
                                                                                                 H., Zoph, B., Spiridonov, A., Sepassi, R., Dohan, D.,
racy. Additionally, manual inspection of the dataset revealed
                                                                                                 Agrawal, S., Omernick, M., Dai, A. M., Pillai, T. S., Pel-
that even when using the most capable Deepseek-R1 model,
                                                                                                 lat, M., Lewkowycz, A., Moreira, E., Child, R., Polozov,
misjudgments still occur during consistency checks. This
                                                                                                 O., Lee, K., Zhou, Z., Wang, X., Saeta, B., Diaz, M.,
indicates that the currently most advanced general-purpose
                                                                                                 Firat, O., Catasta, M., Wei, J., Meier-Hellstern, K., Eck,
large language models still have limitations in formaliza-
                                                                                                 D., Dean, J., Petrov, S., and Fiedel, N. Palm: scaling
tion and consistency verification, thereby demonstrating the
                                                                                                 language modeling with pathways. J. Mach. Learn. Res.,
inherent challenges associated with autoformalization.
                                                                                                 24(1), January 2023. ISSN 1532-4435.

Impact Statement                                                                               Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H.,
                                                                                                 Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano,
This paper presents work whose goal is to advance the field                                      R., Hesse, C., and Schulman, J. Training verifiers to solve
of Machine Learning. There are many potential societal                                           math word problems. arXiv preprint arXiv:2110.14168,
consequences of our work, none which we feel must be                                             2021.
specifically highlighted here.
                                                                                               de Moura, L., Kong, S., Avigad, J., van Doorn, F., and von
                                                                                                 Raumer, J. The lean theorem prover (system description).
Acknowledgments                                                                                  In 2015 Conference on Automated Deduction, pp. 378–
This paper is partially supported by grants from the Na-                                         388. Springer, Cham, July 2015.
tional Key Research and Development Program of China
                                                                                               DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capa-
with Grant No. 2023YFC3341203 and the National Nat-
                                                                                                 bility in llms via reinforcement learning, 2025a. URL
ural Science Foundation of China (NSFC Grant Number
                                                                                                 https://arxiv.org/abs/2501.12948.
62276002).
                                                                                               DeepSeek-AI. Deepseek-v3 technical report, 2025b. URL
References                                                                                       https://arxiv.org/abs/2412.19437.

Anthropic. Claude 3.7 Sonnet: Hybrid Reasoning Model                                           Dong, K. and Ma, T. Stp: Self-play llm theorem provers
  for Complex Task Automation. Technical Report,                                                with iterative conjecturing and proving, 2025. URL
  2 2025. URL https://www.anthropic.com/                                                         https://arxiv.org/abs/2502.00212.
  news/claude-3-7-sonnet.
                                                                                               Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart,
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,                                     S., Tang, E., Song, D., and Steinhardt, J. Measuring math-
  Radev, D., and Avigad, J. Proofnet: Autoformalizing and                                        ematical problem solving with the math dataset. NeurIPS,
  formally proving undergraduate-level mathematics, 2023.                                        2021.

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan,                                        Huang, J., Chen, X., Mishra, S., Zheng, H. S., Yu, A. W.,
  J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G.,                                      Song, X., and Zhou, D. Large language models can-
  Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G.,                                        not self-correct reasoning yet. ArXiv, abs/2310.01798,
  Henighan, T., Child, R., Ramesh, A., Ziegler, D. M., Wu,                                       2023. URL https://api.semanticscholar.
  J., Winter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M.,                                   org/CorpusID:263609132.

                                                                                           9
                        FMC: Formalization of Natural Language Mathematical Competition Problems

Huang, Y., Lin, X., Liu, Z., Cao, Q., Xin, H., Wang, H., Li,           OpenAI. Gpt-4 technical report, 2024. URL https://
  Z., Song, L., and Liang, X. MUSTARD: Mastering uni-                    arxiv.org/abs/2303.08774.
  form synthesis of theorem and proof data. In The Twelfth
  International Conference on Learning Representations,                Paulin-Mohring, C. Inductive definitions in the sys-
  2024. URL https://openreview.net/forum?                                tem coq - rules and properties. In International Con-
  id=8xliOUg9EW.                                                         ference on Typed Lambda Calculus and Applications,
                                                                         1993. URL https://api.semanticscholar.
IMOmath.      Problems from olympiads.               https:              org/CorpusID:27548688.
  //imomath.com/index.cgi?page=
  problemsFromOlympiads, 2025.                     Accessed:           Paulson, L. C. Experience with Isabelle : A generic the-
  2025-03-14.                                                            orem prover. Technical Report UCAM-CL-TR-143,
                                                                         University of Cambridge, Computer Laboratory, Au-
Islam, N., Islam, Z., and Noor, N. A Survey on Opti-
                                                                         gust 1988. URL https://www.cl.cam.ac.uk/
   cal Character Recognition System. arXiv e-prints, art.
                                                                         techreports/UCAM-CL-TR-143.pdf.
   arXiv:1710.05703, October 2017. doi: 10.48550/arXiv.
   1710.05703.                                                         Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M.,
Ling, W., Yogatama, D., Dyer, C., and Blunsom, P. Program                Jennings, M., Thakur, A., and Chaudhuri, S. Putnam-
  induction by rationale generation: Learning to solve and               bench: Evaluating neural theorem-provers on the put-
  explain algebraic word problems. ACL, 2017.                            nam mathematical competition, 2024. URL https:
                                                                         //arxiv.org/abs/2407.11214.
Liu, C., Shen, J., Xin, H., Liu, Z., Yuan, Y., Wang, H., Ju,
  W., Zheng, C., Yin, Y., Li, L., Zhang, M., and Liu, Q.               Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B.,
  Fimo: A challenge formal dataset for automated theorem                Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D.,
  proving, 2023. URL https://arxiv.org/abs/                             Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O.,
  2309.04295.                                                           Liang, P., Dean, J., and Fedus, W. Emergent abili-
Liu, C., Yuan, Y., Yin, Y., Xu, Y., Xu, X., Chen, Z., Wang,             ties of large language models, 2022. URL https:
  Y., Shang, L., Liu, Q., and Zhang, M. Safe: Enhancing                 //arxiv.org/abs/2206.07682.
  mathematical reasoning in large language models via                  Wu, Y., Jiang, A. Q., Li, W., Rabe, M. N., Staats, C., Jam-
  retrospective step-aware formal verification, 2025a. URL              nik, M., and Szegedy, C. Autoformalization with large
  https://arxiv.org/abs/2506.04592.                                     language models, 2022. URL https://arxiv.org/
Liu, J., Lin, X., Bayer, J., Dillies, Y., Jiang, W., Liang,             abs/2205.12615.
  X., Soletskyi, R., Wang, H., Xie, Y., Xiong, B., Yang,
  Z., Zhang, J., Zhi, L., Li, J., and Liu, Z. Combibench:              Xin, H., Ren, Z. Z., Song, J., Shao, Z., Zhao, W., Wang,
  Benchmarking llm capability for combinatorial mathe-                   H., Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhu,
  matics, 2025b. URL https://arxiv.org/abs/                              Q., Yang, D., Gou, Z., Wu, Z. F., Luo, F., and Ruan, C.
  2505.03171.                                                            Deepseek-prover-v1.5: Harnessing proof assistant feed-
                                                                         back for reinforcement learning and monte-carlo tree
Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C., Shen,           search. 2024. URL https://arxiv.org/abs/
  J., Jin, H., Zhang, J., Wang, H., et al. Process-driven auto-          2408.08152.
  formalization in lean 4. arXiv preprint arXiv:2406.01940,
  2024.                                                                Yang, K., Poesia, G., He, J., Li, W., Lauter, K., Chaudhuri,
                                                                         S., and Song, D. Formal mathematical reasoning: A
Moura, L. d. and Ullrich, S. The lean 4 theorem prover and
                                                                         new frontier in ai, 2024. URL https://arxiv.org/
 programming language. In Platzer, A. and Sutcliffe, G.
                                                                         abs/2412.16075.
 (eds.), Automated Deduction – CADE 28, pp. 625–635,
 Cham, 2021. Springer International Publishing. ISBN                   Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and
 978-3-030-79876-5.                                                      Chen, K. Lean workbook: A large-scale lean prob-
Murphy, L., Yang, K., Sun, J., Li, Z., Anandkumar, A.,                   lem set formalized from natural language math prob-
 and Si, X. Autoformalizing Euclidean geometry. In                       lems. In The Thirty-eight Conference on Neural Informa-
 International Conference on Machine Learning (ICML),                    tion Processing Systems Datasets and Benchmarks Track,
 2024.                                                                   2024. URL https://openreview.net/forum?
                                                                         id=Vcw3vzjHDb.
OpenAI. GPT-4o mini: Advancing Cost-Efficient Intel-
  ligence. Technical Report, 7 2024. URL https:                        Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M., Zhang,
 //openai.com/.                                                          Y., Yuan, Z., Xin, H., Huang, W., Wen, Y., Zhang, G.,

                                                                  10
                      FMC: Formalization of Natural Language Mathematical Competition Problems

  and Liu, W. Formalmath: Benchmarking formal mathe-
  matical reasoning of large language models, 2025. URL
  https://arxiv.org/abs/2505.02735.
Zhao, W. X., Zhou, K., Li, J., Tang, T., Wang, X., Hou, Y.,
  Min, Y., Zhang, B., Zhang, J., Dong, Z., Du, Y., Yang, C.,
  Chen, Y., Chen, Z., Jiang, J., Ren, R., Li, Y., Tang, X.,
  Liu, Z., Liu, P., Nie, J.-Y., and Wen, J.-R. A survey of
  large language models, 2025. URL https://arxiv.
  org/abs/2303.18223.
Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021.




                                                              11
                          FMC: Formalization of Natural Language Mathematical Competition Problems

A. Case study
In the process of translating mathematical problems into formal statements acceptable to theorem provers, we have identified
three main challenges: semantic gaps in problem representation, goal definition issues, and missing conditions. This section
analyzes these challenges through concrete case studies.

A.1. Semantic Gaps in Problem Representation
Semantic gaps occur when formalized statements fail to accurately capture the mathematical essence of original problems.
These issues are particularly prominent in combinatorial mathematics and recursive structure problems.


            Original problem: n children sit in a circle. A teacher distributes candies clockwise starting from
            one child: gives to first, skips one, gives to next, skips two, gives to next, and so on (increasing skips).
            Find n such that eventually every child receives at least one candy.
            Formalized output:
            theorem candy_distribution (n : N) :
              ∃ m : N, ∀ i : Fin n, ∃ k : N,
              k < m ∧ (k * (k + 3) / 2) % n = i := by sorry


Analysis: The formalization exhibits three fundamental discrepancies. Primarily, there exists a critical mismatch in the core
mathematical expression: the adopted quadratic form (k(k + 3)/2) fails to correspond with the actual skipping pattern,
where triangular numbers k(k + 1)/2 would be the correct characterization of the candy distribution rule. More critically,
the conclusion remains incomplete as the formalization merely proves the existence of qualifying n without characterizing
its essential property (specifically that n should be a power of two, n = 2k ), thereby depriving the result of practical
applicability.


            Original problem: Given triangle with sides a, b, c, construct new triangle with sides s − a, s − b, s − c
            where s is semiperimeter. Repeat until construction impossible. Find initial triangles allowing infinite
            iteration.

            Formalized output:
            theorem indefinite_semiperimeter_triangle (a b c : R) :
              (∀ s : R, s = (a + b + c) / 2 →
                ∃ a’ b’ c’ : R,
                  a’ = s - a ∧ b’ = s - b ∧ c’ = s - c ∧
                  a’ + b’ > c’ ∧ b’ + c’ > a’ ∧ c’ + a’ > b’ ∧
                  ∀ n : N,
                    ∃ a’’ b’’ c’’ : R,
                      a’’ = (a’ + b’ + c’) / 2 - a’ ∧
                      b’’ = (a’ + b’ + c’) / 2 - b’ ∧
                      c’’ = (a’ + b’ + c’) / 2 - c’ ∧
                      a’’ + b’’ > c’’ ∧
                      b’’ + c’’ > a’’ ∧
                      c’’ + a’’ > b’’) →
              a = b ∧ b = c := by sorry


Analysis: The formalization contains three critical flaws in recursive construction. Primarily, it demonstrates insufficient
recursion depth by explicitly building only two iteration levels (from (a, b, c) to (a′ , b′ , c′ ) to (a′′ , b′′ , c′′ )), failing to establish
a genuine infinite recursion structure. Secondly, there exists structural discontinuity between iteration levels - the inputs of
the second iteration (a′ , b′ , c′ ) lack proper mathematical connection to the outputs of the first iteration (a, b, c), creating an

                                                                      12
                        FMC: Formalization of Natural Language Mathematical Competition Problems

open-loop system that breaks recursive coherence.

A.2. Goal Definition Issues
Solving-oriented problems (”Find” type) often suffer from missing or misplaced goals, especially when requiring specific
values or function expressions.

           Original problem: Find all functions f : R → R satisfying: (i) f (x + y) ∈ [f (x) + f (y), f (x) +
           f (y) + 1] (ii) x ∈ [0, 1) ⇒ f (0) ≥ f (x) (iii) f (1) = 1 ∧ −f (−1) = 1

           Formalized output:
           theorem translated_theorem :
             ∃ f : R → R,
             (∀ x y : R, f x + f y + 1 ≥ f (x + y) ∧ f (x + y) ≥ f x + f y) ∧
             (∀ x : R, 0 ≤ x ∧ x < 1 → f 0 ≥ f x)
             ∧ f 1 = 1 ∧ -f (-1) = 1 := by sorry


Analysis: The primary issue is goal misalignment: while the original problem demands ”finding all satisfying functions”,
the formalized version merely proves the existence of such functions and omits the concrete solution set, representing a
substantial deviation from the original requirement.

           Original problem: Let {f (n)} be strictly increasing sequence of positive integers where the n-th
           missing positive integer is f (f (n)) + 1. Find f (240).

           Formalized output:
           theorem test
             (f : N → N)
             (h0 : ∀ n, 0 < f n)
             (h1 : ∀ n m, n < m → f n < f m)
             (h2 : ∀ n, ∃ m, m = f (f n) + 1 ∧ ∀ k < m, (∃ i, f i = k) → ∃ i
              ≤ k, f i = k) :
             f 240 = 38808 := by sorry


Analysis: The formalization exhibits two fundamental flaws. Firstly, it fails to properly characterize the ”n-th missing
positive integer” - while it expresses the relationship m = f (f (n)) + 1 using existential quantification, it lacks the necessary
cardinality constraints to ensure this indeed represents the n-th (rather than any arbitrary) missing number. More critically,
the formalized conclusion’s assertion that f (240) = 38808 is incorrect, revealing a serious validation failure.

A.3. Missing Conditions
Omission of critical conditions during formalization can lead to incorrect conclusions, particularly dangerous in number
theory problems.

           Original problem: Let k ≥ 14, pk the largest prime strictly less than k (given pk ≥ 3k/4). Let n be
           composite. Prove: (a) If n = 2pk , then n ∤ (n − k)! (b) If n > 2pk , then n | (n − k)!

           Formalized output:
           theorem part_a (k : N) (hk : k ≥ 14)
             (p_k : N) (hp_k : Nat.Prime p_k)



                                                               13
                       FMC: Formalization of Natural Language Mathematical Competition Problems


             (h : p_k < k) (h1 : p_k ≥ 3*k/4)
             (n : N) (hn : ¬Nat.Prime n)
             (hn_eq : n = 2 * p_k) :
             ¬n | (n - k).factorial := by sorry


Analysis: The formalization exhibits several critical limitations. Most notably, it fails to explicitly specify that pk must
be the largest prime strictly less than k. While the theorem states that pk is prime and satisfies pk < k, the absence of the
maximality condition introduces a fundamental flaw—the conclusion may become invalid if multiple primes satisfy pk < k.

B. Comparison with Other Datasets
To validate the reliability of our dataset, we selected some mathematical problems which overlap with FMC from FIMO(Liu
et al., 2023), CombiBench(Liu et al., 2025b), and FormalMATH(Yu et al., 2025), and compared their formalization accuracy
and stylistic differences. All three datasets adopt Lean as their formal language.

B.1. FIMO
The FIMO(Liu et al., 2023) dataset contains problems drawn from the International Mathematical Olympiad (IMO)
Shortlisted Problems. Below is an example that appears in both FMC and FIMO.

          Original problem: Prove that

                                             x2         y2         z2
                                                   +          +          ≥1
                                          (x − 1)2   (y − 1)2   (z − 1)2

          for all real numbers x, y, z, each different from 1, and satisfying xyz = 1.

          FMC:
          theorem test
            (x y z : R)
            (h0 : x ̸= 1)
            (h1 : y ̸= 1)
            (h2 : z ̸= 1)
            (h3 : x * y * z = 1) :
            xˆ2 / (x - 1)ˆ2 + yˆ2 / (y - 1)ˆ2 + zˆ2 / (z - 1)ˆ2 ≥ 1 := by
             sorry


          FIMO:
          theorem fimo_2008_algebra_p2_1
            (x y z : R)
            (h0 : x ̸= 1 ∧ y ̸= 1 ∧ z ̸= 1)
            (h1 : x * y * z = 1) :
            xˆ2 / (x - 1)ˆ2 + yˆ2 / (y - 1)ˆ2 + zˆ2 / (z - 1)ˆ2 ≥ 1 :=
          begin
            sorry
          end


This problem involves simple conditions and a clear goal so that both formal statements accurately capture the intended
meaning with only minor differences. Specifically, FMC lists the assumptions x ̸= 1, y ̸= 1 and z ̸= 1 separately, while
FIMO combines them into a single conjunctive premise. From a formal reasoning perspective, FMC’s formulation facilitates

                                                            14
                      FMC: Formalization of Natural Language Mathematical Competition Problems

usage of assumptions, whereas FIMO’s version offers improved readability. Additionally, the two statements’ placeholder
styles differ: by sorry versus begin...sorry...end, reflecting style discrepancy between Lean versions.

B.2. FormalMATH
The FormalMATH(Yu et al., 2025) dataset spans a wide range of topics, from high school Olympiad problems to
undergraduate-level theorems. Below are two examples found in both FMC and FormalMATH.

  • Case 1


          Original problem: Find all functions f : R → R such that for all real numbers x, y,

                                         f (f (x) + y) = f (x2 − y) + 4yf (x).


          FMC:
          theorem test
            (f : R → R)
            (h0 : ∀ x y, f (f x + y) = f (x ˆ 2 - y) + 4 * y * f x) :
            f = 0 ∨ f = fun x => x ˆ 2 := by sorry


          FormalMATH:
          theorem olymid_ref_base_11031 (f : R → R) :
            (∀ x y, f (f x + y) = f (x ˆ 2 - y) + 4 * y * f x) ↔
            ∀ x, f x = 0 ∨ f x = x ˆ 2 := by


Similar to the FIMO example, both formalizations are largely consistent and accurate with respect to the natural language
description.

  • Case 2

                                                                                          1
          Original problem: Show that for any integer n ≥ 2 the sum of the fractions ab     , where a and b are
                                                                                       1
          relatively prime positive integers such that a < b ≤ n and a + b > n, equals 2 . (Integers a and b are
          called relatively prime if the greatest common divisor of a and b is 1.)

          FMC:
          theorem test
            (n : N)
            (h0 : 2 ≤ n) :
            Finset.sum (Finset.filter (\lambda ab : N × N => ab.1 < ab.2 ∧
             ab.2 ≤ n ∧ ab.1 + ab.2 > n ∧ Nat.gcd ab.1 ab.2 = 1)
             (Finset.product (Finset.Icc 1 n) (Finset.Icc 1 n))) (\lambda
             ab => 1 / (ab.1 * ab.2 : Q)) = 1 / 2 := by sorry

          FormalMATH:
          theorem olymid_ref_base_11032 {n : N} (hn : 2 ≤ n) :
            Σ’ a : N, Σ’ b : N,
            (if (a < b ∧ b ≤ n ∧ Nat.Coprime a b ∧ a + b > n) then (1 / ((a
             * b) : Q)) else 0) =


                                                           15
                      FMC: Formalization of Natural Language Mathematical Competition Problems


             1 / 2 := by


From a mathematical perspective, both versions express the same content rigorously. The key difference lies in stylistic
preference: FMC uses Finset to denote finite sets in Lean, aligning with Lean’s programming idioms, while FormalMATH
opts for summation notation and if...then logic, which more closely resembles traditional mathematical expressions
and improves human readability.

B.3. CombiBench
The CombiBench(Liu et al., 2025b) dataset contains 100 carefully selected combinatorial problems formalized by mathe-
matical experts, including all combinatorial IMO problems since 2000. Below is an overlapping example found in both
FMC and CombiBench.

          Original problem: A magician has one hundred cards numbered 1 to 100 . He puts them into three
          boxes, a red one, a white one, and a blue one, so that each box contains at least one card. A member
          of the audience draws two cards from two different boxes and announces the sum of numbers on
          those cards. Given this information, the magician locates the box from which no card has been drawn.
          How many ways are there to put the cards in the three boxes so that the trick works? (Two ways are
          considered different if at least one card is put into a different box.)

          FMC:
          theorem test :
            let cards : Finset N := Finset.range 100
            let boxes : Finset (Finset N) := {∅, ∅, ∅} -- Placeholder for
             actual box definitions
            Finset.card (Finset.filter (fun b : Finset N => Finset.Nonempty
             b) boxes) = 3 ∧
            (∀ b1 b2 : Finset N, b1 ∈ boxes → b2 ∈ boxes → b1 ̸= b2 → ∀ x y
             : N, x ∈ b1 → y ∈ b2 →
            ∀ b3 b4 : Finset N, b3 ∈ boxes → b4 ∈ boxes → b3 ̸= b4 → ∀ z w :
             N, z ∈ b3 → w ∈ b4 →
            x + y ̸= z + w) := by sorry

          CombiBench:
          abbrev Cards := Finset.Icc 1 100
          abbrev Boxes := Fin 3
          abbrev Trick := N → Boxes

          def trick_works (f : Cards → Boxes) (t : Trick) : Prop :=
            ∀ c1 c2 : Cards,
            -- given the sum of two cards from box 0 and box 1 then the
             trick gives the result of box 2
            (f c1 = 0 → f c2 = 1 → t (c1 .1 + c2 .1) = 2) ∧
            -- given the sum of two cards from box 0 and box 2 then the
             trick gives the result of box 1
            (f c1 = 0 → f c2 = 2 → t (c1 .1 + c2 .1) = 1) ∧
            -- given the sum of two cards from box 1 and box 2 then the
             trick gives the result of box 0
            (f c1 = 1 → f c2 = 2 → t (c1 .1 + c2 .1) = 0)




                                                          16
                        FMC: Formalization of Natural Language Mathematical Competition Problems


           theorem imo_2000_p4 (good_allocations : Finset (Cards → Boxes))
               (h : ∀ f, f ∈ good_allocations ↔ Function.Surjective f ∧ ∃ (t
              : Trick), trick_works f t) :
               good_allocations.card = imo_2000_p4_solution := by sorry


In this case, the formal statement in FMC does not precisely align with the original natural language description. The
problem specifies that, given the sum of two cards drawn from two different boxes, the magician can uniquely identify the
box from which no card was drawn. This implies that the set of such pairwise sums for each pair of boxes must be disjoint,
effectively serving as a signature for the third box.
However, the FMC version fails to explicitly ensure that (b1 , b2 ) and (b3 , b4 ) refer to two distinct pairs of boxes, violating
the original problem constraints. Moreover, the formal statement does not specify the desired conclusion (i.e., the number of
valid configurations), resulting in a missing goal. The approach also relies on explicit enumeration rather than set-based
abstractions, making the expression unnecessarily verbose.
In contrast, the CombiBench version resolves these issues by introducing explicit box indices and counting mechanisms,
leading to a clearer and more faithful formalization. This comparison suggests that, for combinatorial problems, LLM-
generated formalizations still fall short, and statements formalized by mathematical experts retain a significant advantage.

C. Prompts
C.1. Formal Translation Prompts
There are two different stages of formal translation, the first goes with few-shot prompting and the second goes with error
feedback. Following is the prompt for translation with few-shot learning.

           A math theorem in natural language will be provided and please translate it into a Lean4 theorem.
           Please only return the translation (Lean4 code) and no analysis, no mathlib4 import, no comments,
           no proof, no reasoning. Use ”:= by sorry” as a placeholder for proof. Here are some examples for it:
           {few shot}. Following the examples above, translate the next problem into Lean4: {problem}

Following is the prompt for translation with error feedback.

           A math theorem in natural language will be provided and please translate it into a Lean4 theorem.
           Please only return the translation (Lean4 code) and no analysis, no mathlib4 import, no comments,
           no proof, no reasoning. Use ”:= by sorry” as a placeholder for proof. Here is the theorem in natural
           language: {problem}. Before your translation, note that this problem has been mistranslated as the
           following. Concrete errors have been listed and please avoid similar mistakes when translating it again.
           Mistranslation: {failed info}


C.2. Backtranslation Prompts
Following is the prompt for backtranslation.

           Convert the formal statement into natural language:\n```lean\n{prompt}\n```
           Please only return the translation and no analysis.


C.3. Consistency Check Prompts
Following is the prompt for consistency check.


                                                               17
                     FMC: Formalization of Natural Language Mathematical Competition Problems


         Please check whether the following two math problems is same or different in their mathematical
         essence:
         Problem 1: {origin}
         Problem 2: {back}
         Please consider each statement in two problems, they are different if any condition or any goal is
         different. Return in the following format:
         ”’{”Same”: true/false, ”Analysis”: ”Summarize their consistency and difference in brief”}”’


C.4. Dataset Evaluation Prompts
Our rating prompt is adapted from the paper DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale
Synthetic Data. Following is the prompt.

         To evaluate whether a formal Lean4 statement will be of interest to the community:
         \n‘‘‘lean\n{prompt}\n‘‘‘

         Please consider the following criteria:
         1. Relevance to Current Research: Does the statement address a problem or concept that is actively
         being researched in mathematics or related fields? Higher relevance scores indicate greater potential
         interest.

         2. Complexity and Depth: Is the statement complex enough to challenge existing theories and
         methodologies, yet deep enough to provide significant insights or advancements? Complexity and
         depth showcase Lean4’s capabilities and attract interest.

         3. Interdisciplinary Potential: Does the statement offer opportunities for interdisciplinary
         research, connecting mathematics with other fields such as computer science, physics, or biology?
         Interdisciplinary projects often garner wide interest.

         4. Community Needs and Gaps: Does the statement fill an identified need or gap within the Lean4
         community or the broader mathematical community? Addressing these needs directly correlates with
         interest.

         5. Innovativeness: How innovative is the statement? Does it propose new methods, concepts, or
         applications? Innovation drives interest and engagement.

         Customize your evaluation for each problem accordingly, assessing it as ’excellent’, ’good’,
         ’above average’, ’fair’ or ’poor’.

         You should respond in the following JSON format for each statement:

         {"Analysis ": (Provide a brief justification for each score,
         highlighting why the statement scored as it did across the
         criteria. Rate the statement as ’excellent’, ’good’, ’above
         average’, ’fair’ or ’poor’ for all aspects respectively. Format
         {"Relevance to Current Research ": {"rating ": (rating), "reason
         ": (reason)},"Complexity and Depth ": {"rating ": (rating),
         "reason ": (reason)}, ...}), "Assessment ": (Based on the
         criteria, rate the statement as ’excellent’, ’good’, ’above
         average’, ’fair’ or ’poor’.)}




                                                          18
