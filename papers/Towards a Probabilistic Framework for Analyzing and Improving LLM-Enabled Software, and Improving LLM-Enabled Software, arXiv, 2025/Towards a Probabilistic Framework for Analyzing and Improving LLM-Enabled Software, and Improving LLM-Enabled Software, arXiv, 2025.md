                                            Towards a Probabilistic Framework for Analyzing
                                                and Improving LLM-Enabled Software
                                                  Juan Manuel Baldonado                       Flavia Bonomo-Braberman                         Víctor A. Braberman
                                            ICC UBA/CONICET and DC, FCEN                 ICC UBA/CONICET and DC, FCEN                 ICC UBA/CONICET and DC, FCEN
                                                 Universidad de Buenos Aires                Universidad de Buenos Aires                  Universidad de Buenos Aires
                                                  Buenos Aires, Argentina                     Buenos Aires, Argentina                      Buenos Aires, Argentina
                                              juanmanuelbaldonado@gmail.com                     fbonomo@dc.uba.ar                             vbraber@dc.uba.ar
arXiv:2501.06370v2 [cs.SE] 13 Apr 2025




                                            Abstract—Ensuring the reliability and verifiability of large         source of non-determinism (e.g., flaky tests [6]). Instead,
                                         language model (LLM)-enabled systems remains a significant              we believe that a disciplined engineering of reliable LLM-
                                         challenge in software engineering. We propose a probabilistic           enabled applications should be based on both the identification
                                         framework for systematically analyzing and improving these
                                         systems by modeling and refining distributions over clusters of         of constituent “transference models” (TMs) –LLM-powered
                                         semantically equivalent outputs. This framework facilitates the         software components transforming inputs into outputs–, and
                                         evaluation and iterative improvement of Transference Models–            the modeling and analysis of the underlying distribution over
                                         key software components that utilize LLMs to transform inputs           classes that comprise (transference)-equivalent outputs (i.e.,
                                         into outputs for downstream tasks. To illustrate its utility, we        “meaning classes” [4]). In particular, we propose an evaluation
                                         apply the framework to the autoformalization problem, where
                                         natural language documentation is transformed into formal               and refinement framework based on the above insights and also
                                         program specifications. Our case illustrates how distribution-          on the belief that it is feasible and worthwhile to characterize
                                         aware analysis enables the identification of weaknesses and             in which extent and how distribution over meaning-classes
                                         guides focused alignment improvements, resulting in more reliable       satisfies or deviates from expected distribution characteristics.
                                         and interpretable outputs. This principled approach offers a            More concretely, we hypothesize that, for inputs in which
                                         foundation for addressing critical challenges in the development
                                         of robust LLM-enabled systems.                                          TM yields concentrated distributions on incorrect meaning-
                                            Index Terms—LLMs, prompt engineering, autoformalization              classes (adversarial cases), it is possible to verbalize into task-
                                                                                                                 specific terms the kind of misalignment, and that constitutes
                                                                 I. I NTRODUCTION                                a valuable input for re-engineering transference models (e.g.,
                                                                                                                 sub-task decomposition, replacement of underlying LLM, or
                                            In recent years, Large Language Models (LLMs), such as
                                                                                                                 other targeted adjustments informed by such analyses).
                                         GPT-4 [14] and Gemini [19], have demonstrated remarkable
                                                                                                                    To illustrate these ideas, we present a preliminary case study
                                         capabilities across diverse applications. These successes are
                                                                                                                 addressing the problem of autoformalization: translating doc-
                                         largely attributed to their instruction-following abilities and in-
                                                                                                                 strings that specify the intention of a code snippet into formal
                                         context learning. By conditioning on task-specific instructions
                                                                                                                 pre- and post-conditions (e.g., assertions written in Dafny [10]).
                                         (zero-shot) or a small set of examples (few-shot), LLMs have
                                                                                                                 This downstream task, which translates natural language into
                                         been shown to perform a wide array of tasks effectively [3].
                                                                                                                 formal languages, is particularly useful in software testing and
                                         This adaptability has led to a proliferation of applications
                                                                                                                 verification [17]. Our study demonstrates how probabilistic
                                         leveraging LLMs to elicit various downstream tasks via
                                                                                                                 analysis and meaning-class transformations can lead to focused
                                         prompting. The integration of LLMs into software systems is a
                                                                                                                 alignment improvements, offering a foundation for principled
                                         rapidly growing trend, but it presents numerous challenges [6].
                                                                                                                 advancements in LLM-enabled systems.
                                         Particularly, phenomena such as hallucination [8] impact what
                                         can be guaranteed about such applications. One basic aspect                                    II. P RELIMINARIES
                                         to disciplined engineering of complex systems is how to A. Large Language Models
                                         understand and analyze their behavior. While NLP research
                                                                                                                    These predictive models are parameterized functions, whose
                                         acknowledges and leverages at some extent the underlying
                                                                                                                 parameter sets are often initially found by optimizing an
                                         predictive model on next token distribution (e.g., [4], [20]),
                                                                                                                 objective or loss function for next-token prediction with
                                         research papers on software engineering of LLM-enabled
                                                                                                                 respect to a training corpus. Thus, at its core, an LLM
                                         applications typically pinpoint that aspect just as a troublesome
                                                                                                                 yields a probability distribution over the set of tokens or
                                           Partially supported by UBACyT Grants 20020220300079BA and vocabulary (i.e., P (tk |x), the probability of the k-th token
                                         20020190100126BA, CONICET PIP 11220200100084CO, and ANPCyT being tk given the context x). LLMs are typically used in
                                         PICT-2021-I-A-00755, A-1-2022-1-173516 IDRC-ANII, SWPERFI UFAM- its generative role by performing some particular decoding
                                         MOTOROLA RD&I Project “Técnicas de Inteligência Artificial para Análise
                                         e Otimização de Desempenho de Software”, and Amazon Research Award – approach using the next-token predictive model [13]. In general,
                                         Fall 2023 on Automated Reasoning.                                       LLM-enabled software leverages them by injecting prompts
that condition continuations/responses (i.e., LLM predicts next-           autoformalization problem, logically equivalent annotations)
tokens conditioned by the prompt), thus hopefully eliciting the            and share the same meaning when embedded into the abstract
desired downstream tasks. Task-agnostic prompting strategies               domain O. This is, in theory, the result of summing up the
are frequently used (e.g. [11], [21]).                                     probabilities assigned to strings in each of the equivalence
                                                                           classes.
B. Autoformalization
   As indicated, our illustration is based on the problem                  E. Computing Empirical Distributions of TMs
of autoformalization in software verification. This is the                    Given the potential richness of TMs and decoding strategies
transformation from natural language descriptions (docstrings,             plus the fact next-token probabilities are not always accessible,
typically available in development processes) into some for-               for a given input, we approximate the TM probability distri-
mally correct and automatically verifiable format [17], [18]               bution by the empirical categorical distribution on meaning-
which enables automated reasoning on program’s correctness.                classes that are identified and built on-the-fly by clustering
In our illustration, we choose Dafny [10] as the target formal             generated outputs (e.g., by checking annotations to be SMT-
language and particularly the pre- and post-condition sections.            equivalent). More concretely, re-execution of code of the
                                                                           transference model with the same input triggers the (many times
                                                                           stochastic) decoding adapters [13] of the involved LLMs and
                                                                           thus the entire TM behaves as a black box stochastic process
                                                                           (whose behavior depends on hyperparameters and settings of
                                                                           those adapters like temperature, etc.). Yielded outputs are then
                                                                           clustered according to the equivalence relation and empirical
                                                                           distribution on classes is computed (see similar discussion
                                                                           in [4]).
   Figure 1. Architecture of the illustrated baseline transference model                      III. T HE F RAMEWORK
                                                                           A. Assumptions, Hypothesis and Rationale
C. Transference Models
                                                                     Firstly, we assume that for most LLM-enabled applications,
   Following [17], we define “Transference Models” (TMs) as it is possible to understand their LLMs interactions as part
software components that use (typically, prompt-modulated) of the implementation of one or more TMs. TMs might
LLMs to elicit downstream tasks as the key (but not necessarily be implemented straightforwardly by zero-shot instruction
unique) means for transforming some input data into some prompting that includes some representation of the input.
output data. Those transformations have potentially stochastic However, TMs could also be much more sophisticated or
nature given the underlying predictive model and (sampling- even generated by automated prompt generation frameworks
based) decoding strategy of the LLMs. Thus, TMs behavior like [9]. As illustrated above, they could include statically or
can be formulated as a function of input-output pairs into dynamically orchestrated external tools (e.g., some feedback
reals, that is, T : I × O → R, where T (i, o) denotes the signal for corrective tasks), general reactive LLM-triggered
probability that i ∈ I is transferred to o ∈ O, and for external computation [23], the chaining of a series of lower-
i ∈ I, T (i, ·) is a probability distribution over O. As an level transference models [9], etc. TMs are the component
example, in autoformalization proposals, typically, the TM is a under analysis in our approach. Thus the second assumption is
stochastic process that links natural language with annotations that those input/output transformations can be recovered and
as the expected type of input-output pairs (e.g., [2], [17]). described as –human understandable– downstream tasks either
Figure 1 shows the architecture of the TM developed for by developers/testers (or LLMs, in the future) (e.g. [2]). This
illustration. Similarly to Clover’s “doc2anno” TM [17], it understanding should include the ability to assess and equate
elicits a formalization task and, if Dafny compiler detects that tasks results into conceptual classes. Our main hypothesis is
the generated annotation is syntactically incorrect, it instructs that to gain insight on the potential behavior of an LLM-based
a corrective version of the formalization task by including TM (e.g., when testing it, when evaluating it, when validating
compiler’s feedback a bounded number of times. We also it, when engineering it, when over-sighting it, etc.) it is key to
include RAG-like (few-shot) prompt generation [11] to get embrace the predictive nature of underlying model and thus
annotations for likely similar problems by querying a vector approximate and characterize the yielded underlying probability
database.                                                         distribution of TMs over concepts1 . More concretely, we believe
D. Distributions over Semantic Domains                            that concentrated and misaligned cases are the ones to be
                                                                  detected and reduced during development time. The rationale
   Given that Language Models are density estimation functions
                                                                  is manyfold: on the one hand, concentrated and misaligned
that assign probability to every possible string, we concur with
                                                                  cases pinpoint to (adversarial) inputs that lead to systematic
others (e.g. [4], [7]) that probability should be deemed assigned
to concepts, not strings: there are often many (or even infinite)   1We also hypothesize that consistent probability assignments for task’s
strings that represent a given idea equally well (e.g., in the equivalent results is likely an emergent behavior of LLMs.
misalignment in the prompt-modulated predictive model while            existing dataset of Dafny programs; the CloverBench dataset
they could potentially deceive certainty-based hallucination           consists of 62 small hand-written example programs similar
detection techniques [4] (i.e., false negatives that would need        to those found in standard computer science textbooks [17].
to be further identified or mitigated somehow in a safe way).          Each program in the dataset consists of a single method and
Also, it has been shown that assuming TMs to be aligned and            includes a Dafny implementation, annotations specifying pre-
concentrated with high probability may provide error-bounded           conditions and post-conditions, and a docstring that describes
performance guarantees (e.g. [17]). Thus, improvement is               program’s intention. We extract from those programs docstrings
defined to be akin refinement or behavioral subtyping used in          and method signatures and we use pre- and post-conditions
program verification settings (e.g. [12]): replacing a TM with an      as the groundtruth to assess alignment of the most probable
improved one will mean less false positives for a certainty-based      meaning class. We get the empirical approximation by re-
hallucination guardrail, if deployed, and a reduced likelihood of      execution of the transference model (30 times in this case) and
error. We also require (almost-sure) non-regression on aligned         clustering with the assistance of a SMT solver. For the sake of
cases.                                                                 simplicity, we treat each syntactically-invalid result as its own
   On the other hand, we also hypothesize that, when a meaning         class, rather than assigning probability mass to the edit-distance
class that gets the most of the probability mass does not              closest valid class. Compared to collapsing all invalid results
match TM’s expected result, the nature of failure can be,              into a single class, it may lead to less concentration in verdicts,
in general, stated in terms of mistakes humans have already            especially when the model assigns significant probability to
studied and categorized in the corresponding problem domain            diverse invalid outputs. We opted for the Gemini 1.5 Flash
and could lead to hints regarding improvement. That is, we             model with a context of 1000 tokens. Hyperparameters were
seek characterizing in task-specific terms the nature of failures.     the default ones for that LLM: topk with k = 40, topp with
For instance, for the autoformalization problem studied, “too          p = 0.95 and temperature 0.7. This means we work with a
weak/strong pre/post-conditions” are well-known concepts of            generative-process distribution that is more skewed (and tail-
formalization mistakes ontology. As we will show later, they           truncated) than the underlying prompt-modulated next-token
are also typically the perfect fit for characterizing TM’s failures.   prediction model distribution. Yet, this illustrates a plausible
                                                                       generative-process distribution of the LLM running at the core
B. Defining Improvement                                                of the TM whose stochastic behavior one wants to approximate
   For a given input, TM’s distribution over meaning classes is        under such decoding settings. More details and data can be
aligned when the class with the largest assigned probability is        found in [1].
a correct one, and misaligned otherwise. Concentration is used
here as a practical proxy of certainty on generated concepts                                       TABLE I
                                                                                A LIGNMENT AND C ONCENTRATION OF D ISTRIBUTIONS
(akin semantic entropy of the empirical distribution), and it
is defined here as a distribution characterized by the winning                Alignment/Concentration              Concentrated   Not Concentrated
meaning class having probability mass greater than or equal to                          Aligned                        46                3
                                                                        Correct class gen. but misaligned distr.        2                3
the sum of the rest of the masses. Other definitions are possible            Correct class not generated                4                4
(e.g., [17]). Given two alternative t, t′ TMs, we say that TM t′
pointwise improves over t for a test set when t′ extends the set          In Table I, we show a breakdown of the results obtained
of inputs which feature aligned and concentrated distributions         in terms of alignment and concentration. For a given input
and reduces the set of inputs that feature concentrated and            (e.g., docstring + signature), we say that a meaning class (i.e.,
misaligned distributions. The generalized and computable               set of equivalent pre/post specifications) is correct when it
definition of almost-sure improvement for the entire domain is         is made up of specs equivalent to groundtruth specification.
possible by assuming some probability distribution D over the          Firstly, 54 out of the 62 inputs, the empirical distribution
domain of inputs (or a set of possible distributions). Although        features a non-zero probability meaning-class which is the
its definition and study is out of scope, it can be informally         correct one (although not necessarily the winning one). For
stated as a) probability of an input sampled according D to            those 54 inputs, in 49 inputs the obtained empirical distribution
be related by t′ to a concentrated and aligned distribution is         is actually aligned. Moreover, in 46 cases, the distribution is
greater than sampling from D an input with such characteristics        both concentrated and aligned: a sunny day scenario. It is
in t, b) with probability close to one, an input drawn from D          worth noting that the baseline TM using zero-temp (almost)
that has a concentrated and aligned distribution in t also has an      deterministic single-output regime in the underlying LLM gets
aligned and concentrated distribution in t′ , and c) probability       47 aligned results. However, TM’s distributions on concepts
of an input sampled according D to be related by t′ to a               for some of those inputs are either misaligned or they are
concentrated and misaligned distribution is less or equal than         high-entropy distributions. Thus, zero-temp disguises potential
sampling from D an input with such characteristics in t.               issues of the underlying model’s probability assignment. On
                                                                       the other hand, there are also inputs in which the zero-temp
  IV. I LLUSTRATIVE RESULTS ON AUTOFORMALIZATION                       utterance is incorrect but TM’s distribution is actually aligned
   Next we show an anecdotal illustration in line with the             and concentrated. A similar phenomenon has been observed for
stated hypothesis (no claim of generalization). We use an              close-ended selection tasks [7]. We argue that for reliability and
safety concerns one should focus on understanding and reducing have identified natural language utterances where the model’s
cases in which misalignment concurs with high concentration. assigned probabilities for formalizations are unsatisfactory.
In fact, Table II yields the in-depth analysis of winning meaning-
class in the misaligned cases. As mentioned earlier, how the                                           TABLE III
winning-class differs from the groundtruth can be many times              A LIGNMENT AND C ONCENTRATION FOR THE M ODIFIED TM.
defined naturally in task-specific terms. In fact, 11 out of 14            Alignment/Concentration             Concentrated Not Concentrated
misalignments were easily matchable to well-known bug types                          Aligned                        57              1
in formalization. When analyzing reasons for misalignment,           Correct class gen. but misaligned distr.        0              0
                                                                          Correct class not generated                2              2
weak post-condition is the more frequent characteristic of
winning meaning-classes. One of the 2 cases in “debugging”
focus (misaligned and concentrated) is LinearSearch. It is                                     V. R ELATED W ORK
supposed to return the index of the first appearance of an
element, but the winning meaning-class does not include into          Surface form competition for multiple-choice tasks is intro-
the post-condition that the returned index is indeed the first     duced    in [7] and later discussed in [22]. The hallucination
appearance. Moreover, that formula was actually generated in       detection     method of [4] works approximating entropy on
another context and that led to the idea that the model was        meaning-classes,       and equivalence checking for grouping results
not able to detect that part of the intention in the docstring     is done   by   means    of LLMs given the diversity of benchmarked
and formalize it in the same inference step. In general, this      tasks.   In   [17],   transference       model and similar notions of
phenomenon is known as the compositional gap [15] in which         alignment      and   concentration     are  introduced in their analytical
models can correctly answer all sub-problems but not generate      model    to  mathematically        describe    the hypothesis required to
the overall solution. This, in turn, suggested that a structured   bound    error  in  their program     synthesis   approach. In some sense,
docstring (i.e., NL pre-conditions followed by the NL post-        those   works     provide    evidence      on the  potential usefulness of
conditions, both marked with an identification) could constitute   such   concepts     but  do  not  elaborate    on  a framework to analyze
a better subdomain for getting better performance in terms         and   improve     transference     models.
of the proposed distribution analysis. This could trigger, for
                                                                                 VI. C ONCLUSIONS AND F UTURE W ORK
instance, a re-engineering of the TM by adding a sentence
close-ended classification task (pre-condition, post-condition,       We illustrate some principled engineering insights gained
none) to help structuring stripped docstring as a preprocessing when probability distributions over meaning-classes are re-
component added to the baseline TM.                                covered from the stochastic behavior of transference models.
                                                                   This paper pinpoints at concentrated misalignment as key
                               TABLE II                            failure for “debugging” but inputs leading to non-concentrated
     NATURE OF M ISALIGNMENT FOR THE O BTAINED D ISTRIBUTIONS .    distributions and their characterization might be also relevant.
  Formalization Mistakes Concentrated     Non-Concentrated Total   Sensitivity of distributions to input perturbations that are (or
  Weak post-condition            2                3           6    not) supposedly equivalent to the transformation under analysis
  Incorrect post-condition       1                2           4    could also be key to understand task-related limitations of
  Syntax error                   1                2           3
  Weak pre-condition             1                0           1
                                                                   the TM. Several RQs and experiments are necessary to claim
  Strong pre-condition           1                0           0    generalizability and impact of the approach (e.g., In which
  Total                          6                7          14    extent tasks characteristics impact effectiveness of analysis?,
                                                                   In which extent knowing input distribution is key to analysis?,
   In fact, in Table III we show how the modified TM safely that is, When does improvement on a test set translate into
improves over the baseline. Vast majority of inputs lead to generalized improvement?, Which is the impact of decoding
concentrated probability distributions and the concentration is strategy in the analysis?, How robust the framework is to
on the right meaning class. Moreover, the number of misaligned alternative practical distribution/equivalence approximation
and concentrated cases dropped from 6 to 2. Those two inputs methods?, etc.). There are also many possible conceptual
leading to concentrated misalignment (indeed, not even a and automation paths, including: approximation techniques for
correct output generated), modify_2d_array and on-line-max, computing concentration, the definition of a richer language
according to our proposal would be the focus of analysis for to predicate on inputs and resulting distributions, and notions
a new round of engineering efforts (out-of-scope). In fact, of compositionality of TMs. Also, we are aware that, for
relevance of those inputs in focus can also be backed by the some tasks/transference models, a more structured domain
fact that in the baseline TM the resulting distributions were of concepts might be needed (e.g., preference relation) and
misaligned and non-concentrated (one without generation of the improvement definitions might need to accommodate potential
correct result). Moreover, modify_2d_array was a paradigmatic trade-offs among lowering entropy and aligning distributions.
case of non-concentration in the baseline TM (20 different            Last but not least, it is foreseeable the help of AI-based solu-
meaning classes). On the other hand, both TMs were unable tions to characterize misalignments and troublesome/adversarial
to generate one of the constraints required for the concept of inputs and even the assistance in decomposition, prompt-
maximum in on-line-max. Through this guided analysis, we engineering and hyperparameter tuning.
A. The case of Agentic AI                                                         [5] Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, and Fabien Roger. AI
                                                                                      control: Improving safety despite intentional subversion. ICML 2024.
   A particular case of interest for safe AI is the analysis
                                                                                  [6] Ahmed E. Hassan, Dayi Lin, Gopi Krishnan Rajbahadur, Keheliya
of agentic goal-pursuing LLM-enabled software. For such                               Gallaba, Filipe Roseiro Côgo, Boyuan Chen, et al. Rethinking software
a case, we can naturally lift previously defined notions to                           engineering in the era of foundation models: A curated catalogue of
a setting inspired by Markov Decision Processes [16]. In                              challenges in the development of trustworthy FMware. FSE Comp. 2024.
                                                                                      doi:10.1145/3663529.3663849.
this vision, decisions of the MDP denote inputs from the                          [7] Ari Holtzman, Peter West, Vered Shwartz, Yejin Choi, and Luke
environment (e.g., user-stated goals, invoked tools results, etc.).                   Zettlemoyer. Surface form competition: Why the highest probability
The LLM then provides the probability of transitioning to states                      answer isn’t always right. EMNLP 2021.
                                                                                      doi:10.18653/V1/2021.EMNLP-MAIN.564.
that stand for external action invocations or internal thoughts
                                                                                  [8] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, et al.
generated by the agent. More precisely, LLM can be regarded as                        Survey of hallucination in natural language generation. ACM Comput.
implementing transference models that, given a representation                         Surv., 55(12):248:1–248:38, 2023.
of a history of interactions and thoughts, yields distributions                       doi:10.1145/3571730.
on meaning classes each of them representing conceptually                         [9] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang,
                                                                                      Keshav Santhanam, Sri Vardhamanan, et al. DSPy: Compiling declarative
the same action invocation or same thoughts. In essence, an                           language model calls into state-of-the-art pipelines. ICLR 2024.
agentic LLM-powered software behaves as incrementally and                        [10] K. Rustan M. Leino. Dafny: An automatic program verifier for functional
reactively enacting a policy of action invocation and thoughts                        correctness. LPAR 2010.
governed by the distributions over meaning-classes yielded by                         doi:10.1007/978-3-642-17511-4_20.
the LLM. Moreover, given an environmental policy or sequence                     [11] Patrick S. H. Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni,
                                                                                      Vladimir Karpukhin, Naman Goyal, et al. Retrieval-augmented generation
of inputs/decisions, the MDP can be conceptually casted into                          for knowledge-intensive NLP tasks. NeurIPS 2020.
a Markov Chain in which probability of a set of trajectories of                  [12] Barbara Liskov and Jeannette M. Wing. A behavioral notion of subtyping.
interest can be theoretically measured. This formulation would                        ACM Trans. Program. Lang. Syst., 16(6):1811–1841, 1994.
be able to address unintended and competent misalignments.                            doi:10.1145/197320.197383.
Firstly, the function from history to distributions on completions               [13] Clara Meister, Gian Wiher, and Ryan Cotterell. On decoding strategies
                                                                                      for neural text generators. Trans. Assoc. Comput. Linguistics, 10:997–
implemented by the LLM is deemed deterministic (there is                              1012, 2022.
no hidden scratchpad memory nor randomization available as                            doi:10.1162/TACL_A_00502.
mechanisms for implementing AI subversion strategies [5]).                       [14] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad,
                                                                                      Ilge Akkaya, et al. GPT-4 technical report, 2024. arXiv:2303.08774.
Thus, one would be interested in strategies “accidentally”
                                                                                 [15] Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A. Smith,
played by the environment in which trajectories that violate                          and Mike Lewis. Measuring and narrowing the compositionality gap in
key safety constraints (e.g., no requesting human authorization)                      language models. EMNLP 2023.
have a, higher than acceptable, chance to occur. Secondly,                            doi:10.18653/V1/2023.FINDINGS-EMNLP.378.
those inputs and feedback from the environment are not                           [16] Martin L. Puterman. Markov Decision Processes: Discrete Stochastic
                                                                                      Dynamic Programming, Wiley, 1994.
intentionally crafted (in the sense of jailbreaking) but they can                     doi:10.1002/9780470316887.
be naturally expected according to some sensible operational                     [17] Chuyue Sun, Ying Sheng, Oded Padon, and Clark W. Barrett. Clover:
profile governing external decisions. Thirdly, they are not                           Closed-loop verifiable code generation. SAIV 2024.
punctual or artificial: they can be grouped into a measurable                         doi:10.1007/978-3-031-65112-0_7.
human-characterizable fault-inducing input class. Last but                       [18] Christian Szegedy. A promising path towards autoformalization and
                                                                                      general artificial intelligence. CICM 2020.
not least, violating trajectories look like competent behavior:                       doi:10.1007/978-3-030-53518-6_1.
other safety (but less risky) constraints like environment                       [19] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac,
preconditions for action execution are satisfied.                                     Jiahui Yu, Radu Soricut, et al. Gemini: A family of highly capable
                                                                                      multimodal models, 2024. arXiv:2312.11805.
                             R EFERENCES
                                                                                 [20] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi,
 [1] Juan Baldonado. Source code for the experiments. https://github.                 Sharan Narang, et al. Self-consistency improves chain of thought
     com/jmbuba/llm-semantic-perf, 2024.                                              reasoning in language models. ICLR 2023.
 [2] Víctor A. Braberman, Flavia Bonomo-Braberman, Yiannis Charalambous,         [21] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian
     Juan G. Colonna, Lucas C. Cordeiro, and Rosiane de Freitas. Tasks                Ichter, Fei Xia, et al. Chain-of-thought prompting elicits reasoning in
     people prompt: A taxonomy of LLM downstream tasks in software                    large language models. NeurIPS 2022.
     verification and falsification approaches, 2024. arXiv:2404.09384.
 [3] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared             [22] Sarah Wiegreffe, Matthew Finlayson, Oyvind Tafjord, Peter Clark, and
     Kaplan, Prafulla Dhariwal, et al. Language models are few-shot learners.         Ashish Sabharwal. Increasing probability mass on answer choices does
     NeurIPS 2020.                                                                    not always improve accuracy. EMNLP 2023.
 [4] Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and Yarin Gal.                   doi:10.18653/V1/2023.EMNLP-MAIN.522.
     Detecting hallucinations in large language models using semantic entropy.   [23] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R.
     Nat., 630(8017):625–630, 2024.                                                   Narasimhan, et al. ReAct: Synergizing reasoning and acting in language
     doi:10.1038/S41586-024-07421-0.                                                  models. ICLR 2023.
