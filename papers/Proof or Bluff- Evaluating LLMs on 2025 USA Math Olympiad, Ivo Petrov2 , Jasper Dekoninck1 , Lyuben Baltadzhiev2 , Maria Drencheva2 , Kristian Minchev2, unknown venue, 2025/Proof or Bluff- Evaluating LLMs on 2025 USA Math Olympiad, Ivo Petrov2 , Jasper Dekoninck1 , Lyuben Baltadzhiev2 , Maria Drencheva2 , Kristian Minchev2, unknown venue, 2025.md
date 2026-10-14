                                        P ROOF OR B LUFF ? E VALUATING LLM S ON 2025 USA
                                        M ATH O LYMPIAD
                                         Ivo Petrov2 , Jasper Dekoninck1 , Lyuben Baltadzhiev2 , Maria Drencheva2 , Kristian Minchev2
                                          Mislav Balunović1,2 , Nikola Jovanović1 , Martin Vechev1,2
                                                   1                        2
                                                     ETH Zurich               INSAIT, Sofia University "St. Kliment Ohridski"
                                                                                https://matharena.ai/
                                                                       https://github.com/eth-sri/matharena

                                                                                     A BSTRACT
arXiv:2503.21934v5 [cs.CL] 4 Sep 2025




                                                 Recent math benchmarks for large language models (LLMs) such as MathArena
                                                 indicate that state-of-the-art reasoning models achieve impressive performance
                                                 on mathematical competitions like AIME, with the leading model, G EMINI -2.5-
                                                 P RO, achieving scores comparable to top human competitors. However, these
                                                 benchmarks evaluate models solely based on final numerical answers, neglect-
                                                 ing rigorous reasoning and proof generation which are essential for real-world
                                                 mathematical tasks. To address this, we introduce a comprehensive evaluation of
                                                 full-solution reasoning for challenging mathematical problems. Using expert hu-
                                                 man annotators, we evaluated several state-of-the-art reasoning models on the six
                                                 problems from the 2025 USAMO within hours of their release. Our results reveal
                                                 that all tested models struggled significantly: only G EMINI -2.5-P RO achieves a
                                                 non-trivial score of 25%, while all other models achieve less than 5%. Through
                                                 detailed analysis of reasoning traces, we identify the most common failure modes
                                                 and find several unwanted artifacts arising from the optimization strategies em-
                                                 ployed during model training. Overall, our results suggest that current LLMs are
                                                 inadequate for rigorous mathematical reasoning tasks, highlighting the need for
                                                 substantial improvements in reasoning and proof generation capabilities.


                                        1   I NTRODUCTION
                                        The advancement of reasoning models has significantly improved the mathematical capabilities of
                                        large language models (LLMs). Evaluation efforts like MathArena (Balunović et al., 2025) demon-
                                        strate that these models achieve impressive performance on mathematical competitions such as
                                        AIME and HMMT. However, these competitions only evaluate final numerical answers and do not
                                        require rigorous proof-based reasoning essential for most mathematical tasks.
                                        Current benchmarks that mitigate this issue either rely on formal verification tools like Lean (Zheng
                                        et al., 2022; Liu et al., 2023; Tsoukalas et al., 2024) or focus on the evaluation of constructive proofs
                                        (Balunovic et al., 2025). While these approaches are useful, the former does not take advantage of
                                        LLMs’ strong natural language generation capabilities, and the latter covers only a limited subset of
                                        proofs. Only Frieder et al. (2023) evaluate LLMs on full-solution reasoning, but their evaluation is
                                        focused on just two older non-reasoning models, therefore not presenting their analysis as a bench-
                                        mark, and contains problems where some could appear in the training data. Therefore, it remains
                                        uncertain whether current reasoning LLMs can reliably address complex mathematical questions
                                        requiring rigorous reasoning, which are crucial in real-world mathematical contexts.
                                        To overcome these limitations, we conduct the first evaluation of natural language proofs by LLMs
                                        on challenging problems from the 2025 USA Mathematical Olympiad (USAMO). The USAMO
                                        represents one of the highest tiers of high school mathematics competitions in the United States,
                                        demanding detailed proofs and explanations analogous to the International Mathematical Olympiad
                                        (IMO). Participants qualify through prior competitions, including the AIME, but USAMO problems
                                        require significantly more rigorous and well-explained solutions.
                                        Overall, we find that current LLMs struggle significantly on USAMO problems, with the best-
                                        performing model achieving an average score of less than 25%. Our evaluation reveals several
                                        critical failure modes, including flawed logic, unjustified assumptions, and a lack of creativity.


                                                                                           1
      Problem 1: Let k and d be positive in-            Problem 5: Determine, with proof, all
      tegers. Prove that there exists a positive        positive integers k such that
      integer N such that for every odd integer                               n  k
                                                                         1 X n
      n > N , the digits in the base-2n represen-
      tation of nk are all greater than d.                            n + 1 i=0 i

                                                        is an integer for all positive integers n.

        Figure 1: Two problems of USAMO 2025. The other problems are available in App. B
These findings underscore the substantial limitations of current LLMs in generating rigorous math-
ematical proofs. In this report, we first outline our methodology in §2, present detailed results and
identify critical weaknesses in §3, and discuss several qualitative observations in §4.

2      M ETHODOLOGY
This section outlines the methodology used for evaluating the mathematical reasoning capabilities of
the selected LLMs. Our approach prioritized accuracy, fairness, and transparency throughout each
step, involving careful preparation and grading procedures.

2.1     P ROBLEM S ELECTION AND P REPARATION
We selected the USAMO 2025, a highly prestigious mathematics competition comprising six proof-
based problems administered over two days, as our benchmark. This competition aligns perfectly
with our evaluation objectives, as the questions are challenging, require detailed proofs for full
credit, and are uncontaminated. In Fig. 1, we present two problems from the competition, with the
remaining four available in App. B.
For evaluation, we provided each model with the problems, prompting them explicitly to produce
comprehensive and detailed proofs formatted in LATEX. The full prompt instructions and details
of used hyperparameters are available in App. A.2. To reduce variance, each model solved every
problem four separate times. Solutions, excluding thought traces, were anonymized and converted
into PDF format for grading. Both G ROK 3 and G EMINI -2.5-P RO were evaluated after our initial
grading and were therefore not fully anonymous when presented to the judges.

2.2     J UDGE S ELECTION AND T RAINING
Our grading team consisted of four experts, each having substantial mathematical problem-solving
experience as former national IMO team members or having participated in final-stage team se-
lection processes for their countries. Prior to the grading, judges received instructions detailing
evaluation goals and methodologies. These guidelines are accessible in our GitHub repository. A
trial run with three USAMO 2024 problems was conducted to familiarize evaluators with the grading
approach and resolve ambiguities. Small misunderstandings were clarified during this session.

2.3     G RADING P ROCEDURE
Each of the six problems from USAMO 2025 was independently evaluated by two evaluators, with
each judge responsible for grading three unique problems. This double grading method, modeled
after the IMO’s evaluation process, ensures consistency in our grading and decreases personal biases.
Since the official USAMO does not release standard solutions or grading schemes, we carefully de-
veloped a standardized grading scheme for each problem, drawing from reliable mathematical com-
munity resources, particularly the Art of Problem Solving (AoPS) forums. All solutions from these
sources were verified by our evaluators for accuracy before creating the grading scheme. Follow-
ing USAMO conventions, each solution was graded out of a maximum of seven points with partial
credit given for significant and meaningful progress. The finalized grading schemes are available in
our GitHub repository and displayed on our website. An example can be found in App. A.3.
Judges independently reviewed each assigned solution against the pre-established grading scheme.
When a solution did not perfectly align with the scheme, the approach was awarded points where
appropriate. Each judge documented their reasoning, including justification for each partial credit
awarded. These notes are also accessible on our website, with an example provided in App. A.3.


                                                    2
Table 1: Main results of our evaluation. Listed scores are averaged over four runs. We measure cost
in USD, and report the average score across all generations and graders for each problem.

    Model               P1 (/7)   P2 (/7)   P3 (/7)       P4 (/7)   P5 (/7)   P6 (/7)   Total (/42)   Cost
    G EMINI -2.5-P RO    6.5       0.0       0.1           3.5       0.0       0.0         10.1         N/A
    R1                   0.5       0.0       0.0           1.5       0.0       0.0          2.0         2.03
    G ROK 3              2.0       0.0       0.0           0.0       0.0       0.0          2.0         N/A
    F LASH -T HINKING    1.5       0.0       0.0           0.0       0.2       0.0          1.8         N/A
    C LAUDE 3.7          0.5       0.5       0.0           0.0       0.0       0.6          1.5         9.03
    QWQ                  1.2       0.0       0.0           0.0       0.0       0.0          1.2         0.42
    O 1- PRO             0.5       0.0       0.0           0.0       0.2       0.4          1.2       203.44
    O 3- MINI            0.5       0.1       0.0           0.0       0.0       0.2          0.9         1.11

Evaluators also documented prominent failure modes observed during grading, defined as the first
instance of incorrect or inadequately explained reasoning. Specifically, mistakes were categorized
into four classes:
      • Logic: Errors due to logical fallacies or unjustified leaps disrupting the reasoning.
      • Assumption: Errors coming from the introduction of unproven or incorrect assumptions that
        undermined subsequent steps.
      • Creativity: Errors resulting from fundamentally incorrect solution strategies due to the in-
        ability to identify the correct approach.
      • Algebra/Arithmetic: Errors arising from critical algebraic or arithmetic miscalculations.

We show examples of these errors in App. C.1.
Additionally, noteworthy behaviors or trends in model-generated solutions were systematically
logged for further analysis. These observations were used to identify common pitfalls and areas
for improvement in the models’ reasoning capabilities and are presented in §4.

3     R ESULTS
We now present the results of our evaluation. In §3.1, we detail our primary findings, demonstrating
that only G EMINI -2.5-P RO achieves a score above 5%. In §3.2, we analyze common failure patterns
in depth, identifying typical mistakes and trends in the models’ reasoning. Finally, in §3.3, we try
and fail to automatically grade the models’ solutions by giving a judge model the grading scheme
and a ground-truth solution.

3.1    M AIN R ESULTS
We evaluate eight state-of-the-art reasoning models on the 2025 USAMO problems. Specifically,
we chose Q W Q (Qwen, 2025), R1 (Guo et al., 2025), G EMINI -2.5-P RO (Google DeepMind, 2025),
F LASH -T HINKING (Reid et al., 2024), O 1- PRO (Jaech et al., 2024), O 3- MINI (OpenAI, 2025),
G ROK 3 (xAI, 2025) and C LAUDE 3.7 (Anthropic, 2025). For brevity, we use a shorthand nota-
tion for each model in the main text, and we refer to App. A.1 for the full model names. The chosen
hyperparameters and prompt can be found in App. A.2.
We provide a detailed, per-problem breakdown of model performance in Table 1, with average scores
computed across four evaluation runs. Each USAMO problem is scored out of 7 points, with a total
maximum score of 42 points per run. The table also includes the total cost of running each model
over all problems and evaluation runs. If the model is free, we indicate this with "N/A".
While current state-of-the-art LLMs achieve performance comparable to top human competitors
on numerical-answer-focused competitions such as AIME and HMMT, our evaluation uncovers a
significant gap in their ability to generate rigorous proofs. Only G EMINI -2.5-P RO managed to score
above 5%, achieving an average score of 24.4% across all problems. This model’s performance is
particularly noteworthy, as it can solve a problem correctly (scoring 6/7 or above) in six of its
24 attempts. The highest average score achieved by any other model falls below 5%, indicating
substantial limitations in handling the complexity and rigor of USAMO problems. Notably, among
nearly 175 evaluated solutions from all models except G EMINI -2.5-P RO, the only perfect 7/7 score
was a single G ROK 3 attempt on Problem 1.


                                                      3
                                                                                  Logic
                  0.5
                                                                                  Assumption
                                                                                  Creativity
                  0.4
      Frequency                                                                   Algebra/Arithmetics

                  0.3

                  0.2

                  0.1

                  0.0
                        Gemini-Pro    R1      o1-pro   Flash-Thinking   o3-mini   QwQ      Claude 3.7   Grok-3

                                 Figure 2: Distribution of first encountered failure mode.


Although the USAMO presents more difficult problems compared to previously tested competitions,
the complete failure of almost all models to successfully solve more than one problem underscores
that current LLMs remain inadequate for rigorous olympiad-level mathematical reasoning tasks.
Furthermore, while G EMINI -2.5-P RO achieved a non-trivial score, it still struggled significantly,
with an average score of only 24.4% across all problems. This limitation suggests that existing
optimization methods like GRPO (Shao et al., 2024) may currently be insufficient for tasks requiring
detailed logical precision.


3.2    FAILURE M ODES

The most frequent failure mode among human participants is the inability to find a correct solution.
Typically, human participants have a clear sense of whether they solved a problem correctly. In
contrast, all evaluated LLMs consistently claimed to have solved the problems. This discrepancy
poses a significant challenge for mathematical applications of LLMs as mathematical results derived
using these models cannot be trusted without rigorous human validation. To further investigate this
limitation, we conducted a thorough analysis of the errors identified during the grading process using
the categories defined in §2.
Figure 2 illustrates the distribution of these error categories as determined by our judges. The most
common errors were related to flawed logic, with solutions frequently using unjustified reasoning
steps, incorrect rationale, or misinterpretations of previous progress. Another significant issue was
the models’ tendency to treat certain critical proof steps as trivial or standard procedure without
proper justification. Notably, O 3- MINI, despite being one of the best reasoning models, frequently
skipped essential proof steps by labeling them as "trivial", even when their validity was crucial.
Another important observation is the lack of creativity in the models’ reasoning. Each model often
attempted the same (and wrong) solution strategy across all attempts, failing to explore alternative
approaches. One exception to this observation was F LASH -T HINKING, which attempted multiple
strategies in the same run, but as a consequence only shallowly explored each one, failing to reach a
valid conclusion. An example of this behavior is shown in App. C.2.
However, the models generally demonstrated strong performance in algebraic and arithmetic com-
putations, successfully performing symbolic manipulations without external computational support.
Still, R1 showed a notably higher frequency of algebraic or arithmetic errors, indicating a clear area
for targeted improvement in this model.


3.3    AUTOMATED G RADING

We explored the feasibility of replacing human graders with LLM-based evaluators, selecting O 3-
MINI and C LAUDE 3.7 as grading models. Both models were provided with a grading scheme
developed by our evaluators, along with a verified solution and an example evaluation for reference.
In App. A.2, we provide the full prompt used for this evaluation.


                                                                4
Table 2: Results of automated grading executed by O 3- MINI and R1. The table shows the average
total score which is at most 42.

                      Model                  Ours       O 3- MINI   C LAUDE 3.7
                      G EMINI -2.5-P RO      10.1         19.6         19.3
                      R1                      2.0         19.3         14.9
                      G ROK 3                 2.0         15.1          9.1
                      F LASH -T HINKING       1.8         10.5         14.1
                      C LAUDE 3.7             1.5         19.0         18.4
                      QWQ                     1.2         23.8         18.8
                      O 1- PRO                1.2         19.3         21.0
                      O 3- MINI               0.9         19.5         17.1


As detailed in Table 2, neither model accurately graded the solutions, consistently overestimating
their quality. Specifically, the models frequently awarded points for incorrect or unjustified reason-
ing, inflating the scores by a factor of up to 20.
Notably, F LASH -T HINKING and G ROK 3 received significantly lower scores from the automated
evaluation compared to other models. We hypothesize this discrepancy arises because both tend
to generate multiple solutions per attempt, or present the solutions in a chaotic manner, potentially
confusing the LLM-based judges and resulting in lower scores. Conversely, Q W Q achieved consid-
erably higher scores, likely because it often generates simpler solution attempts, which are easier for
the automated judges to interpret.

4   Q UALITATIVE D ISCUSSION
During the evaluation, judges also documented common issues and noteworthy behaviors exhibited
by the models. In this section, we discuss some of the most prominent issues that we observed.

Answer Boxing Current reinforcement learning optimization techniques rely on extracting re-
wards from a clearly identifiable final answer. To facilitate accurate reward extraction, models are
typically instructed to enclose their final answers within a \boxed{} environment. However, this
requirement often produces unintended artifacts in the solutions for the USAMO problems. Specifi-
cally, even though most of the evaluated problems do not require a final boxed answer, many models
consistently provided answers within a boxed environment. In a particularly notable instance from
problem 5, Q W Q confused itself by dismissing the possibility of a non-integer solution, despite
no such restriction existing in the problem statement. Consequently, it incorrectly insisted that the
final answer was 2, even though it had otherwise correctly deduced that all even numbers satisfy
the given conditions (see App. C.3). This behavior illustrates how alignment techniques like GRPO
(Shao et al., 2024) inadvertently encourage models to treat every mathematical problem as requiring
an explicitly boxed final answer, negatively affecting their overall reasoning.

Generalizing Patterns Models frequently exhibited a tendency to overgeneralize patterns ob-
served in smaller numerical cases to larger, untested cases. While this heuristic approach might
be effective for problems that only require a numerical answer, it is fundamentally flawed for prob-
lems that demand rigorous proof. Models often incorrectly asserted that these patterns observed for
small cases would hold generally, without providing a formal proof for such a claim (see App. C.4).

Non-Existent Citations One of the most frequent and concerning mistakes made by G EMINI -
2.5-P RO is the generation of citations to sources that do not exist. This issue is especially prevalent
in problems where the model struggles significantly and fails to produce a correct solution. In such
cases, it often fabricates references to theorems or lemmas that appear plausible but, to the best of
our knowledge, are not real. For example, in P6, all four generations include citations to works
that we were unable to verify or locate. We suspect this behavior stems from the model’s training
with internet access: when it is unable to use internet in thought process, it appears to generate a
convincing-sounding citation instead. An illustration of this phenomenon is provided in App. C.5.
This tendency is particularly troubling, as it can result in the spread of misinformation which seem
to use credible academic sources.

                                                    5
Solution Structure and Clarity There was significant variation in the clarity and structural coher-
ence of the solutions provided by different models. Models such as O 3- MINI and O 1- PRO generally
presented their solutions clearly, logically, and in an easily interpretable manner. Conversely, models
like F LASH -T HINKING and Q W Q frequently produced chaotic and barely interpretable responses,
sometimes confusing multiple unrelated ideas within a single solution. Further, G EMINI -2.5-P RO
also had signicant issues with the clear presentation of results, sometimes boxing entire proofs are
letting its thought process slip through in its final answer (App. C.6). The noticeable clarity in mod-
els trained by OpenAI suggests that additional training focused on solution coherence substantially
improved their readability, an aspect evidently less emphasized in other models.

5   C ONCLUSION
In this study, we comprehensively analyzed the performance of eight state-of-the-art LLMs on prob-
lems from the USAMO 2025 competition. Using a rigorous human evaluation setup, we found that
all evaluated models performed very poorly, with even the best-performing model achieving an av-
erage accuracy of less than 25%. Through detailed examination of the models’ reasoning traces, we
identified several critical failure modes, including significant artifacts arising from the optimization
strategies employed during model training. These findings underscore the substantial limitations
of current LLMs in the rigorous mathematical reasoning required for high-level olympiad competi-
tions, highlighting the need for substantial improvements in proof generation capabilities.

ACKNOWLEDGEMENTS
This work has received funding from the Swiss National Science Foundation (SNSF)
[200021_207967], the Ministry of Education and Science of Bulgaria (support for INSAIT, part
of the Bulgarian National Roadmap for Research Infrastructure), and the Swiss State Secretariat for
Education, Research and Innovation (SERI).

R EFERENCES
Anthropic. Claude 3.7 sonnet system card, March 2025. URL https://assets.anthropic.com/
  m/785e231869ea8b3b/original/claude-3-7-sonnet-system-card.pdf.

Mislav Balunovic, Jasper Dekoninck, Nikola Jovanovic, Ivo Petrov, and Martin T. Vechev. Math-
 construct: Challenging LLM reasoning with constructive proofs. CoRR, abs/2502.10197, 2025.
 doi: 10.48550/ARXIV.2502.10197. URL https://doi.org/10.48550/arXiv.2502.10197.
Mislav Balunović, Jasper Dekoninck, Ivo Petrov, Nikola Jovanović, and Martin Vechev. Math-
 arena: Evaluating llms on uncontaminated math competitions, February 2025. URL https:
 //matharena.ai/.

Simon Frieder, Luca Pinchetti, Alexis Chevalier, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas
  Lukasiewicz, Philipp Petersen, and Julius Berner. Mathematical capabilities of chatgpt. In Al-
  ice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine,
  editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neu-
  ral Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, Decem-
  ber 10 - 16, 2023, 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/
  58168e8a92994655d6da3939e7cc0918-Abstract-Datasets_and_Benchmarks.html.

Google DeepMind. Gemini Pro, March 2025. URL https://deepmind.google/technologies/
  gemini/pro/. Accessed: 2025-04-03.

Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
  Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
  via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec
  Helyar, Aleksander Madry, Alex Beutel, Alex Carney, Alex Iftimie, Alex Karpenko, Alex Tachard
  Passos, Alexander Neitz, Alexander Prokofiev, Alexander Wei, Allison Tam, Ally Bennett,


                                                   6
  Ananya Kumar, Andre Saraiva, Andrea Vallone, Andrew Duberstein, Andrew Kondrich, An-
  drey Mishchenko, Andy Applebaum, Angela Jiang, Ashvin Nair, Barret Zoph, Behrooz Ghor-
  bani, Ben Rossen, Benjamin Sokolowsky, Boaz Barak, Bob McGrew, Borys Minaiev, Botao
  Hao, Bowen Baker, Brandon Houghton, Brandon McKinzie, Brydon Eastman, Camillo Lu-
  garesi, Cary Bassin, Cary Hudson, Chak Ming Li, Charles de Bourcy, Chelsea Voss, Chen Shen,
  Chong Zhang, Chris Koch, Chris Orsinger, Christopher Hesse, Claudia Fischer, Clive Chan, Dan
  Roberts, Daniel Kappler, Daniel Levy, Daniel Selsam, David Dohan, David Farhi, David Mely,
  David Robinson, Dimitris Tsipras, Doug Li, Dragos Oprica, Eben Freeman, Eddie Zhang, Ed-
  mund Wong, Elizabeth Proehl, Enoch Cheung, Eric Mitchell, Eric Wallace, Erik Ritter, Evan
  Mays, Fan Wang, Felipe Petroski Such, Filippo Raso, Florencia Leoni, Foivos Tsimpourlas,
  Francis Song, Fred von Lohmann, Freddie Sulit, Geoff Salmon, Giambattista Parascandolo,
  Gildas Chabot, Grace Zhao, Greg Brockman, Guillaume Leclerc, Hadi Salman, Haiming Bao,
  Hao Sheng, Hart Andrin, Hessam Bagherinezhad, Hongyu Ren, Hunter Lightman, Hyung Won
  Chung, Ian Kivlichan, Ian O’Connell, Ian Osband, Ignasi Clavera Gilaberte, and Ilge Akkaya.
  Openai o1 system card. CoRR, abs/2412.16720, 2024. doi: 10.48550/ARXIV.2412.16720. URL
  https://doi.org/10.48550/arXiv.2412.16720.

Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
  Chuanyang Zheng, Yichun Yin, Lin Li, Ming Zhang, and Qun Liu. FIMO: A challenge formal
  dataset for automated theorem proving. CoRR, abs/2309.04295, 2023.
OpenAI.     Openai o3-mini system card, January 2025.         URL https://cdn.openai.com/
  o3-mini-system-card-feb10.pdf.

Qwen. Qwq-32b: Embracing the power of reinforcement learning, March 2025. URL https:
 //qwenlm.github.io/blog/qwq-32b/.

Machel Reid, Nikolay Savinov, Denis Teplyashin, Dmitry Lepikhin, Timothy P. Lillicrap, Jean-
 Baptiste Alayrac, Radu Soricut, Angeliki Lazaridou, Orhan Firat, Julian Schrittwieser, Ioannis
 Antonoglou, Rohan Anil, Sebastian Borgeaud, Andrew M. Dai, Katie Millican, Ethan Dyer,
 Mia Glaese, Thibault Sottiaux, Benjamin Lee, Fabio Viola, Malcolm Reynolds, Yuanzhong
 Xu, James Molloy, Jilin Chen, Michael Isard, Paul Barham, Tom Hennigan, Ross McIlroy,
 Melvin Johnson, Johan Schalkwyk, Eli Collins, Eliza Rutherford, Erica Moreira, Kareem Ay-
 oub, Megha Goel, Clemens Meyer, Gregory Thornton, Zhen Yang, Henryk Michalewski, Za-
 heer Abbas, Nathan Schucher, Ankesh Anand, Richard Ives, James Keeling, Karel Lenc, Salem
 Haykal, Siamak Shakeri, Pranav Shyam, Aakanksha Chowdhery, Roman Ring, Stephen Spencer,
 Eren Sezener, and et al. Gemini 1.5: Unlocking multimodal understanding across millions of
 tokens of context. CoRR, abs/2403.05530, 2024. doi: 10.48550/ARXIV.2403.05530. URL
 https://doi.org/10.48550/arXiv.2403.05530.

Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, Y. K. Li,
  Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open
  language models. CoRR, abs/2402.03300, 2024. doi: 10.48550/ARXIV.2402.03300. URL
  https://doi.org/10.48550/arXiv.2402.03300.

George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings, Ami-
  tayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers on the
  putnam mathematical competition. CoRR, abs/2407.11214, 2024.
xAI. Grok 3 beta — the age of reasoning agents, February 2025. URL https://x.ai/news/grok-3.
  Accessed: 2025-04-03.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. minif2f: a cross-system benchmark for
  formal olympiad-level mathematics. In ICLR. OpenReview.net, 2022.




                                              7
A        A DDITIONAL EXPERIMENTAL DETAILS
Here we describe any additional information related to our evaluation setup and details.

A.1       M ODEL NAMES

For brevity and visual clarity, we have shortened the model names as follows:

          • O 3- MINI ( HIGH ) as O 3- MINI
          • O 1- PRO ( HIGH ) as O 1- PRO
          • D EEP S EEK R1 as R1
          • Q W Q-32B as Q W Q
          • G EMINI -2.0-F LASH -T HINKING -E XP as F LASH -T HINKING
          • C LAUDE -3.7-S ONNET-T HINKING as C LAUDE 3.7
          • G ROK 3 B ETA (T HINK ) as G ROK 3
          • G EMINI -2.5-P RO -E XP -03-25 as G EMINI -2.5-P RO

A.2       H YPERPARAMETERS AND P ROMPT

Model Hyperparameters For O 3- MINI, O 1- PRO, C LAUDE 3.7, and F LASH -T HINKING, we used
the default hyperparameters provided by their official API. For O 3- MINI and O 1- PRO, we used the
high reasoning setting, which provides the highest available reasoning budget. For C LAUDE 3.7and
F LASH -T HINKING, we set the maximum reasoning token limit to 32000.
As recommended by the authors of R1 and Q W Q, we used a temperature of 0.6 and a top-p value
of 0.95. Additionally, for Q W Q, we set top-k to 40. These hyperparameters sets correspond to
the default hyperparameters used by the official HuggingFace models1 . The token limit was set to
32000. We use the TogetherAPI for both these models.

Prompt         Every problem was ran with the following user prompt:
 Prompt

        Give a thorough answer to the following question. Your answer will be graded by human judges based on
        accuracy, correctness, and your ability to prove the result. You should include all steps of the proof. Do
        not skip important steps, as this will reduce your grade. It does not suffice to merely state the result.
        Use LaTeX to format your answer.

        {problem}




Judge Prompt To judge model solutions, we used the same hyperparameters for generation as
before. Additionally, we use the following prompt:
 Judge Prompt

        # Instruction

        You are an expert mathematician that grades solutions of high-school olympiad-level problems. You will be
        given a mathematical problem, as well as a grading scheme that you should adhere to. Your task is to
        accurately grade a solution according to that grading scheme.

        # Problem and Scheme

        ##Problem statement

        {problem_statement}

        ## Grading scheme


    1
        See   https://huggingface.co/deepseek-ai/DeepSeek-R1                 and    https://huggingface.co/Qwen/
QwQ-32B



                                                            8
      {grading_scheme}

      # Example

      Here how an example grading can look like:

      ## Example solution:

      {correct_solution}

      ## Example grading

      {example_grading}

      # Evaluation

      Produce a scoring using the same format for the following solution. Reason carefully about the contents of
      the solution and make sure that all steps of the proof are included and rigorous.

      ## Formatting instructions

      Follow a JSON-style formatting as the above example, namely:

      - The categories should be in the same order
      - The awarded number of points for each category should follow after the 'points' key
      - The reasoning for each decision should be explained after the 'desc' key.
      - Output only the JSON response.

      Here is the solution you should grade:
      {solution}




Both the grading scheme and example grading are provided in json format. Examples of these can
be found in App. A.3.

A.3     E XAMPLE G RADING S CHEME AND G RADING

Example Grading Scheme The grading scheme for each problem was developed by our expert
judges. The grading scheme for Problem 1 is shown below:

 Grading Scheme

        {
            "id": "1",
            "points": 7,
            "scheme": [
               {
                  "title": "Initial closed form expression for each digit",
                  "points": 1,
                                                                               k
                     "desc": "Uses the base-2n representation of n                 to find a closed form expression of each digit
                                 nk
                            j           k
                     ai =                   mod (2n)"
                                (2n)i
                },
                {
                     "title": "Interchanging the floor and mod",
                     "points": 3,
                     "desc": "Transforms the digit expression into a easily boundable one by interchanging the floor
                      and modulo operations."
                },
                {
                     "title": "Bounding the expression",
                     "points": 2,
                     "desc": "Correctly bounds the aforementioned expression, usually by showing the numerator is
                                                        j        k
                                                            n
                     divisible by n, so that ai >=                   ∥."
                                                            2i
                },
                {
                     "title": "Finishing",
                     "points": 1,
                     "desc": "Chooses a provably sufficiently large N . The point is not awarded if it has not
                     proven that n^k has at most k digits."
                }
            ]
        }




                                                                           9
Example Grading An example grading for Problem 1 is shown below for a (human-generated)
completely correct solution:
 Example Grading

    {
        "points": 7,
        "details": [
           {
              "title": "Initial closed form expression for each digit",
              "points": 1,
              "desc": "Correctly uses the base-2n representation of n^k to find a closed form expression of each
                                   nk
                              j           k
                 digit ai =                   mod(2n)"
                                  (2n)i
            },
            {
                 "title": "Interchanging the floor and mod",
                 "points": 3,
                 "desc": "Transforms the digit expression into a easily boundable one by interchanging the floor
                 and modulo operations."
            },
            {
                 "title": "Bounding the expression",
                 "points": 2,
                 "desc": "Correctly bounds the aforementioned expression, usually by showing the numerator is
                                                         j        k
                                                             n
                 divisible by n, so that ai >=                        ."
                                                             2i
            },
            {
                 "title": "Finishing",
                 "points": 1,
                                                                                                k
                 "desc": "Chooses a provably sufficiently large N and has proven that n             has more than k digits."
            }
        ]
    }




B   USAMO P ROBLEMS
We show the six problems from the USAMO 2025 competition in this section.
 Problem 1
        Let k and d be positive integers. Prove that there exists a positive integer N such that for every odd
                                                                                k
        integer n > N , the digits in the base-2n representation of n               are all greater than d.




 Problem 2
        Let n and k be positive integers with k < n. Let P (x) be a polynomial of degree n with real
        coefficients, nonzero constant term, and no repeated roots. Suppose that for any real numbers
        a0 , a1 , . . . , ak such that the polynomial ak xk + · · · + a1 x + a0 divides P (x), the product a0 a1 · · · ak
        is zero. Prove that P (x) has a nonreal root.




 Problem 3
        Alice the architect and Bob the builder play a game. First, Alice chooses two points P and Q in the
        plane and a subset S of the plane, which are announced to Bob. Next, Bob marks infinitely many points in
         the plane, designating each a city. He may not place two cities within distance at most one unit of
        each other, and no three cities he places may be collinear. Finally, roads are constructed between the
        cities as follows: for each pair A, B of cities, they are connected with a road along the line segment
        AB if and only if the following condition holds:
        \begin{center}
        For every city C distinct from A and B , there exists R ∈ S such
        that △P QR is directly similar to either △ABC or △BAC .
        \end{center}
        Alice wins the game if (i) the resulting roads allow for travel between any pair of cities via a finite
        sequence of roads and (ii) no two roads cross. Otherwise, Bob wins. Determine, with proof, which player
        has a winning strategy.

        Note: △U V W is directly similar to △XY Z if there exists a sequence of rotations, translations,
        and dilations sending U to X , V to Y , and W to Z .




                                                                           10
 Problem 4
         Let H be the orthocenter of acute triangle ABC , let F be the foot of the altitude from C to AB ,
         and let P be the reflection of H across BC . Suppose that the circumcircle of triangle AF P
         intersects line BC at two distinct points X and Y . Prove that C is the midpoint of XY .




 Problem 5
      Determine, with proof, all positive integers k such that\frac{1}{n+1} \sum_{i=0}^n \binom{n}{i}^kis an
      integer for all positive integers n.




 Problem 6
         Let m and n be positive integers with m ≥ n. There are m cupcakes of different flavors arranged
         around a circle and n people who like cupcakes. Each person assigns a nonnegative real number score to
         each cupcake, depending on how much they like the cupcake. Suppose that for each person P , it is
         possible to partition the circle of m cupcakes into n groups of consecutive cupcakes so that the sum of
          P 's scores of the cupcakes in each group is at least 1. Prove that it is possible to distribute the m
          cupcakes to the n people so that each person P receives cupcakes of total score at least 1 with
         respect to P .




C     E XAMPLE TRACES
C.1     E XAMPLES OF DIFFERENT ERROR MODES

C.1.1     E XAMPLE OF LOGICAL ERROR
Here, C LAUDE 3.7 generalizes over all indices j, when it has proven it for a single one - a clear leap
in logic.

      C LAUDE 3.7
      ...
      Since P (x) has at least n distinct real roots and k < n, we have at least n − (k − 1) ≥ 2 choices for
      sk . If we choose sk = rm and then sk = rl (where rm , rl ̸∈ {s1 , s2 , . . . , sk−1 }), we get:

      For sk = rm : σj = Tj + rm · Tj−1
      For sk = rl : σj = Tj + rl · Tj−1

      If both of these result in σj = 0 for the same j , then:
      Tj + rm · Tj−1 = 0 and Tj + rl · Tj−1 = 0

      Subtracting, we get: (rm − rl ) · Tj−1 = 0

      Since rm ̸= rl (as the roots of P (x) are distinct), we must have Tj−1 = 0.

      Continuing this logic, we would find that all Tj = 0, which is impossible, especially since T0 = 1.

      Therefore, we can always find a choice of sk such that all σj ̸= 0 for j = 1, 2, . . . , k, which means all
      coefficients of our divisor are nonzero.
      ...




C.1.2     E XAMPLE OF CREATIVITY ERROR
On problem 3, which is a game between 2 players - Alice and Bob, O 3- MINI (and most other
models) argued that Bob should win from the beginning while it can be proven that Alice has an
optimal strategy.

      O 3- MINI
                                                                                         2
      We will show that regardless of how Alice chooses the two fixed points P, Q ∈ R        and the "template-set"
      S ⊂ R2 , Bob can place his cities so that the resulting road network fails to meet at least one of the two
      winning conditions for Alice. (Alice wins only if the road network is both connected and drawn with no two
      roads crossing.) In other words, Bob has a winning strategy.
      ...




                                                            11
C.1.3       E XAMPLE OF ASSUMPTION ERROR
On problem 4, many assumption errors are made, like this one from O 3- MINI, where it assumes (not
explicitly) that C is external to the circumcircle of AF P , which is incorrect.

      O 3- MINI

      ...
      A key step is to prove the following claim:

      ----------------------------

       CA is tangent to ω = ⊙(AF P ).
      ----------------------------

      Once we have tangency, the radius drawn to the tangency point is perpendicular to the tangent line. Since
      that radius (from the center of ω ) lies on the perpendicular bisector of any chord, we will see that the
      perpendicular from the center of ω to BC must pass through C .

      ...




C.1.4       E XAMPLE OF ALGEBRAIC / ARITHMETIC ERROR
Here, R1 incorrectly computes a sum of combinations and arrives at the incorrect conclusion. The
correct value of the sum is 3,395,016, which is divisible by 8.

      R1
      ...
      4. **Case k = 4**:
      - Testing small values of n (up to n = 6) shows the expression is an integer. However, for n = 7:
                     P7   74
         - The sum    i=0 i   = 1, 894, 391.
                          1,894,391
         - The expression     8     = 236, 798.875 is not an integer.
      - Thus, k = 4 fails for n = 7.
      ...




C.2     F LASH -T HINKING STRUGGLING ON PROBLEM 6

Below, we see F LASH -T HINKING attempting multiple strategies in the same run, leading to a con-
fusing solution that fails to reach a valid conclusion.

      F LASH -T HINKING
      Consider a bipartite graph. People on one side, cupcakes on the other side.
      Let's consider a different network flow approach.
      Source S , Sink T . Nodes P1 , . . . , Pn . Nodes C1 , . . . , Cm .
      For each person Pi , consider the partitions. Let's fix one partition for each person Pi , say
      Gi,1 , . . . , Gi,n .
      Nodes Gi,k for i = 1, . . . , n, k = 1, . . . , n.
      Edge S → Pi capacity 1. Edge Pi → Gi,k capacity 1. Edge Gi,k → Cj if Cj ∈ Gi,k capacity 1. Edge
      Cj → T capacity 1.
      We want to show max flow is n.

      Assume for contradiction that it is impossible to distribute the cupcakes as required.
      We will use Hall's Marriage Theorem, but need to define the sets correctly.
      For each person Pi , let Gi be the set of all consecutive groups of cupcakes that give score at least 1 to
      person Pi . We need to select Ai ∈ Gi such that Ai ∩ Aj = ∅.

      Let's reconsider the network flow approach. Construct a network as follows:
      Source S , Sink T . Nodes for people P1 , . . . , Pn . Nodes for cupcakes C1 , . . . , Cm .
      For each person Pi and each cupcake Cj , create an edge from Pi to Cj .
      Edge S → Pi capacity 1 for i = 1, . . . , n. Edge Pi → Cj capacity 1 for i = 1, . . . , n, j = 1, . . . , m. Edge
      Cj → T capacity 1 for j = 1, . . . , m.
      Cost on edge (Pi , Cj ) is −sij . Cost on other edges is 0.
      We want to send flow of value n from S to T with minimum cost.
      If we can send flow of value n, then we have selected n paths from S to T . Each path is
      S → Pi → Cj →      T . Let xij be      flow on edge (Pi , Cj ). Then
                                         the P
      P m             Pn              Pn       m
        j=1 xij ≤ 1,     i=1 xij ≤ 1,    i=1   j=1 xij = n. This is not right.




                                                             12
      Consider a different graph. Bipartite graph with people P1 , . . . , Pn on one side, and cupcakes C1 , . . . , Cm
      P the other side. Edge between Pi and Cj . We want to select a matching M such that for each Pi ,
      on
         C ∈M and (P ,C )∈M sij ≥ 1. This is not matching.
            j            i   j


            use Hall's Theorem. For each person Pi , let Fi be the family of sets of consecutive cupcakes F such
      Let's P
       that   C ∈F sij ≥ 1. We want to choose Ai ∈ Fi for each i = 1, . . . , n such that Ai ∩ Aj = ∅ for i ̸= j .
                  j                                                           S
      For any subset of people X ⊆ {P1 , . . . , Pn }, let F (X) =    Pi ∈X Fi . We need to show that for any
      X ⊆ {P1 , . . . , Pn }, we can choose |X| disjoint sets from F (X). This is not Hall's theorem directly.

      We need to show that there exist disjoint sets A1 , . . . , An such that Ai is a consecutive group from some
      partition for Pi and score for Pi from Ai is at least 1.
      Since for each person Pi , there is a partition into n groups Gi,1 , . . . , Gi,n with score ≥ 1. Let's
      consider these groups as possible choices.
      For each person Pi , we have n choices Gi,1 , . . . , Gi,n . We need to select one choice Ai ∈ {Gi,1 , . . . , Gi,n }
       for each i such that Ai ∩ Aj = ∅ for i ̸= j .
                                                                                     2
      Consider a bipartite graph. People P1 , . . . , Pn on one side, and n groups Gi,j on the other side. Edge
      from Pi to Gij . We need to find a matching of size n such that each Pi is matched to some Gi,ji , and
      G1,j1 , . . . , Gn,jn are disjoint.

      Final Answer:
      We will prove this by contradiction. Suppose it is impossible to distribute the cupcakes such that each
      person Pi receives cupcakes of total score at least 1.
      For each person Pi , we are given that there exists a partition of the circle      P of m cupcakes into n
      consecutive groups Gi,1 , Gi,2 , . . . , Gi,n such that for each k = 1, . . . , n,  C ∈G    sij ≥ 1.
                                                                                                    j      i,k

                                                                                                    Sn
      Consider a bipartite graph B = (U ∪ V, E) where U = {P1 , . . . , Pn } and V =       i=1 {Gi,1 , Gi,2 , . . . , Gi,n }
      . We add an edge between Pi ∈ U and G ∈ V if and only if G ∈ {Gi,1 , Gi,2 , . . . , Gi,n }. We want to show
      that there exists a matching of size n in B . BySHall's Marriage Theorem, we need to show that for any
      subset X ⊆ U , |N (X)| ≥ |X|, where N (X) =      P ∈X {Gi,1 , Gi,2 , . . . , Gi,n }.
                                                                     i
      For any X ⊆SU ,                                            P                                         P
      |N (X)| = |       Pi ∈X {Gi,1 , Gi,2 , . . . , Gi,n }| ≤   Pi ∈X |{Gi,1 , Gi,2 , . . . , Gi,n }| =     Pi ∈X n = n|X|. This
      does not help.

      Let's consider a different approach using flows. Consider the network constructed earlier... Further
      investigation is needed to construct the correct argument.


      Final Answer: The final answer is          Y es




C.3        Q W Q BOXES AN INTEGER

Here, we show Q W Q confusing itself by requiring an integer answer, even though the solution is the
set of all even integers.

      QWQ

      ...
      ### Conclusion:
      The expression is an integer for all n if and only if k is even. Therefore, the solution is all positive
      even integers.

      ### Final Answer:

      The positive integers k are all even numbers. Thus, the solution is                2m for any positive integer m.
      However, since the problem requires a boxed answer and the minimal solution is typically expected, the

      answer is       2 . But strictly speaking, the correct answer is all even positive integers. Given the problem's
       requirements, the boxed answer is:


       2




C.4        OVERGENERALIZING PATTERNS

Here, F LASH -T HINKING chooses an explicit polynomial to test out on problem 2, but then decides
to generalize its conclusion to all polynomials.



                                                                         13
      F LASH -T HINKING
        Now, let us choose specific real roots for P (x). Let ri = i for i = 1, 2, . . . , n. Let
        P (x) = c(x − 1)(x − 2) · · · (x − n) for some nonzero real number c. Then P (x) is a polynomial of degree
         n with real coefficients, nonzero constant term, and no repeated roots.
                                                                            Pk         i
        Consider the divisor Q(x) = (x − 1)(x − 2) · · · (x − k) =             i=0 ai x .
                                                                               k−i
        Then r1 = 1, r2 = 2, . . . , rk = k . For this choice, ai = (−1)           ek−i (1, 2, . . . , k).
        Since 1, 2, . . . , k are all positive, ej (1, 2, . . . , k) > 0 for j = 1, 2, . . . , k . Also e0 (1, 2, . . . , k) = 1 > 0
        .
                                                   k−i
        Thus, for i = 0, 1, . . . , k, ai = (−1)         ek−i (1, 2, . . . , k) ̸= 0.
                                                       k
        Therefore, for this divisor Q(x) = ak x + · · · + a0 , the product a0 a1 · · · ak ̸= 0.
        However, the given condition states that for any real numbers a0 , a1 , . . . , ak such that
        ak xk + · · · + a1 x + a0 divides P (x), the product a0 a1 · · · ak is zero.
        This is a contradiction.
        Hence, our assumption that P (x) has only real roots must be false.
        Therefore, P (x) has a nonreal root.


        Final Answer: The final answer is        P (x) has a nonreal root




C.5     H ALLUCINATING C ITATIONS

A common failure mode of G EMINI -2.5-P RO was its tendency to generate fake citations to support
its points. One of the best examples is the case below, where the model hallucinates a paper with an
emoji in the title.
      G EMINI -2.5-P RO
        We will use the following lemma, which is a known result in fair division theory. This result can be
        found, for example, as Lemma 7 in "Fair partitioning of   " by Cardinal, Langerman, Palvolgyi (2021), or
         Theorem 2 in "Fair division of a discrete item" by Algaba et al. (2019). These papers attribute the
        proof technique to Gale (1993) and Scarf (1967).

                                                               n
        **Fair Partition Lemma:** Let v1 , . . . , vm ∈ R≥0 . Suppose that for each i ∈ {1, . . . , n}, there exists a
                                                                                        P
        partition of {1, . . . , m} into n sets Ji,1 , . . . , Ji,n such that (         j∈Ji,k vj )i ≥ 1 for all
         ∈ {1, . . . , n}. Then there exists a partition of {1, . . . , m} into n sets K1 , . . . , Kn such that
        kP
        ( j∈K vj )i ≥ 1 for all i ∈ {1, . . . , n}.
                 i




C.6     B OXING SOLUTIONS

The majority of models also struggled with presenting clear and structured solutions, making evalu-
ation and understanding significantly more difficult. In the instance below, G EMINI -2.5-P RO boxed
an entire solution at the end of its generation.
      G EMINI -2.5-P RO
      ...
      The representation is (2, 16, 11)22 . The digits are a0 = 11, a1 = 16, a2 = 2. All are greater than d = 1.
      The proof holds.

      Final Answer: The final answer is

       Let B = 2n.   We want to show that there exists a positive integer N such that for every odd ...

                                                                                                                      k
       ...   As shown above, this implies ai > d for all digits ai in the base-2n representation of n .

       This completes the proof.




                                                                   14
