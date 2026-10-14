                                                       Computers and Education: Arti cial Intelligence 9 (2025) 100490


                                                                    Contents lists available at ScienceDirect


                                        Computers and Education: Artificial Intelligence
                           journal homepage: www.sciencedirect.com/journal/computers-and-education-artificial-intelligence




The promise and limits of LLMs in constructing proofs and hints for logic
problems in intelligent tutoring systems
Sutapa Dey Tithi∗ iD, Arun Kumar Ramesh, Clara DiMarco, Xiaoyi Tian, Nazia Alam,
Kimia Fazeli, Tiffany Barnes
Department of Computer Science, North Carolina State University, Raleigh, NC, USA




ARTICLE INFO                                               ABSTRACT

Keywords:                                                  Intelligent tutoring systems have demonstrated effectiveness in teaching formal propositional logic proofs, but
Intelligent tutoring systems                               their reliance on template-based explanations limits their ability to provide personalized student feedback. While
Next-step hints                                            large language models (LLMs) offer promising capabilities for dynamic feedback generation, they risk producing
Symbolic logic                                             hallucinations or pedagogically unsound explanations. We evaluated the stepwise accuracy of LLMs in construct-
LLMs                                                       ing multi-step symbolic logic proofs, comparing six prompting techniques across four state-of-the-art LLMs on 358
Generative AI
                                                           propositional logic problems. Results show that DeepSeek-V3 achieved superior performance with upto 86.7 %
Data mining
DeepSeek-v3
                                                           accuracy on stepwise proof construction and excelled particularly in simpler rules. We further used the best-
GPT-4o                                                     performing LLM to generate explanatory hints for 1050 unique student problem-solving states from a logic ITS
                                                           and evaluated them on 4 criteria with both an LLM grader and human expert ratings on a 20 % sample. Our
                                                           analysis finds that LLM-generated hints were 75 % accurate and rated highly by human evaluators on consis-
                                                           tency and clarity, but did not perform as well in explaining why the hint was provided or its larger context. Our
                                                           results demonstrate that LLMs may be used to augment tutoring systems with logic tutoring hints, but those hints
                                                           require additional modifications to ensure accuracy and pedagogical appropriateness.




1. Introduction                                                                             (Aleven & Koedinger, 2002; Koedinger et al., 2012). Complicating mat-
                                                                                            ters for integrating LLM-based help in tutoring systems, novices may
    Intelligent tutoring systems (ITSs) serve as scalable alternatives to
                                                                                            lack metacognitive skills to identify what and when to ask for help (help
human tutoring (Kardan & Conati, 2015; Ueno & Miyazawa, 2017).
                                                                                            avoidance), and they could abuse the system by asking for direct an-
These systems automatically evaluate student solutions and provide
                                                                                            swers or overly frequent hints (help abuse) (Roll et al., 2011). Thus, the
adaptive feedback, including next-step hints and explanations. Such
                                                                                            quality of solutions, adherence to pedagogical principles, and adapta-
personalized assistance has been shown to enhance student learning out-
                                                                                            tion based on metacognitive needs are as crucial as accuracy for help in
comes (VanLehn, 2011). Although various data-driven methods have
                                                                                            learning environments (Holstein et al., 2019).
been shown to save time and resources by reducing the need for an
                                                                                                Formal logic proofs are essential in STEM education. Several studies
expert to construct hints, they rely on the quantity and quality of train-
                                                                                            have evaluated LLM performance in solving logic problems and handling
ing data. Moreover, the hints in these systems are often template-based
                                                                                            natural language logical reasoning tasks (Parmar et al., 2024; Saparov &
with limited adaptation (Stamper et al., 2024). In this context, large
                                                                                            He, 2022). However, LLMs’ ability to handle complex, multi-step sym-
language models (LLMs) can offer opportunities to augment ITS capabil-
                                                                                            bolic logic proofs within pedagogical contexts is largely unexplored. In
ities through scalable feedback generation (Tian et al., 2024). However,
                                                                                            this work, we evaluate how well LLMs construct multi-step symbolic
integrating LLMs into ITSs faces challenges: LLMs may hallucinate incor-
                                                                                            propositional logic proofs and next-step natural language hints in an in-
rect information (Wang et al., 2024), which risks misleading students
                                                                                            telligent logic tutor. We compared six prompting techniques across four
and reinforcing misconceptions (Nye et al., 2023). LLMs may also
                                                                                            state-of-the-art LLMs on 358 propositional logic problems, leveraging
generate correct answers without adhering to sound instructional prin-
                                                                                            advanced prompt engineering to incorporate learning science theories.
ciples, potentially limiting their effectiveness in fostering deep learning
                                                                                            The quality of hints and explanations from the best-performing LLM was


 ∗   Corresponding author.
     Email address: stithi@ncsu.edu (S.D. Tithi).


https://doi.org/10.1016/j.caeai.2025.100490
Received 16 June 2025; Received in revised form 17 October 2025; Accepted 18 October 2025
Available online 28 October 2025
2666-920X/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by-
nc-nd/4.0/).
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                              Computers and Education: Arti cial Intelligence 9 (2025) 100490


assessed by a rubric-based LLM grader and 20 % were also rated by hu-             performance can decrease for complex operations, with accuracy drop-
man experts on a 4-dimensional rubric. We investigated the following              ping below 45 % for proofs requiring three or more steps (Saparov et al.,
research questions:                                                               2023). Prompt engineering techniques like Chain-of-Thought (CoT) have
    RQ1 To what extent can LLMs construct accurate step-by-step solu-             improved LLMs’ reasoning capabilities, but ensuring the faithfulness of
tions for propositional logic (PL) proofs within a logic tutor?                   generated reasoning chains remains challenging (Liu, Xu et al., 2024).
                                                                                  Careful prompt engineering is also important in ensuring the effec-
  • RQ1a: How do prompting strategies influence proof construction                tive utilization of LLMs in educational contexts (Stamper et al., 2024).
    performance?                                                                  These approaches predominantly address LLM performance on natural
  • RQ1b: How does performance vary across a selection of four open-              language logic problems or isolated inference rules, with limited work
    source and proprietary LLM models?                                            exploring multi-step symbolic propositional logic proofs. Additionally,
                                                                                  these LLMs are evaluated using traditional metrics such as accuracy and
RQ2 How well does the most accurate LLM generate pedagogically                    coverage (Phung et al., 2023, 2024); they are rarely assessed for the suit-
viable hints and explanations?                                                    ability of their explanations for educational contexts. Our work bridges
                                                                                  these gaps by investigating LLMs’ capabilities in multi-step symbolic
  • RQ2a: How does hint correctness vary across logic rules of differing
                                                                                  logic proof construction and explanatory hint generation, with the goal
    complexity?
                                                                                  of combining the pedagogical rigor of traditional ITS with the natural
  • RQ2b: How do domain experts assess the pedagogical quality of LLM-
                                                                                  language capabilities of LLMs. We extend traditional evaluation metrics
    generated explanations in terms of consistency, clarity, justification,
                                                                                  to include consistency (the what), clarity (the readability), justification
    and subgoaling?
                                                                                  (the why), and subgoaling (describing the why within a larger con-
                                                                                  text), as described below, providing a more comprehensive assessment
2. Related work
                                                                                  of LLM-generated hint quality in logic education.
    Intelligent Tutoring Systems and Automated Feedback. ITSs have
established their effectiveness in promoting student learning through
                                                                                  3. Methodology
personalization across multiple fields, including mathematics (Anderson
et al., 1995; Canfield, 2001; Koedinger et al., 1997; Ritter et al., 2007),           Proof Construction. We selected two datasets to evaluate LLMs’ per-
probability (Chi & VanLehn, 2010; Sedlmeier, 1997), logic (Maniktala              formance in proof construction: (1) The Symbolic Propositional Logic
& Barnes, 2020), and programming languages (Anderson et al., 1995;                (SPL) dataset contains 310 multi-step problems. These problems were
Holland et al., 2009; Price, Dong & Lipovac, 2017). The evolution of              originally in natural language form, then Gottlieb et al. systematically
these systems has led to various data-driven techniques for providing             translated them into symbolic PL representations (Gottlieb, 2024). (2)
adaptive support. Murray (2003) demonstrated that data-driven assis-              The Logic Tutor dataset (LT) contains 48 PL problems of varying diffi-
tance can efficiently generate hints while reducing expert involvement.           culty. These problems are designed specifically for educational purposes,
This approach was further advanced by Barnes et al. through the Hint              with each proof typically requiring 12–15 steps to complete. In both SPL
Factory, a method for generating next-step hints in propositional logic           and LT datasets, each problem contains the given premises and a conclu-
(Barnes et al., 2008). Further research has confirmed that both on-               sion, which are fed into LLMs using carefully engineered prompts. LLMs
demand and unsolicited hints can significantly enhance student learning           output the complete step-by-step proof along with a structured solution
when appropriately implemented (Barnes et al., 2008; Maniktala &                  in JSON format.
Barnes, 2020; Stamper et al., 2013). Despite the popularity and ben-                  Logic Tutor Problem Solving State (PSS) Dataset Extraction. To
efits of data-driven hints in ITSs, the current approaches have some              enable realistic testing of next-step hint generation, a dataset was ex-
limitations. Many systems provide immediate next-step hints without               tracted from interaction logs of all solution attempts to 18 problems
offering conceptual explanations (Price, Dong & Lipovac, 2017; Rivers             each by 30 students using the logic tutor for homework in Fall 2024.
& Koedinger, 2017). Marwan et al. showed that novices perceived hints             Students were randomly selected from all CS majors at a US public
with explanations as significantly more relevant and interpretable than           university, whose 2021–22 graduating class demographics comprised
those without explanations in a block-based programming environment,              83 % men and 17 % women; with 58 % white, 18.5 % Asian, 3 %
and hints without conceptual explanations can decrease students’ trust            Hispanic/Latin, 2 % Black/African American, 9 % other races with the
in their helpfulness (Marwan et al., 2019). While incorporating textual           remaining 9.5 % having international student status for whom race/eth-
explanations alongside procedural hints has been shown to be useful,              nicity information was not available. IRB approval was obtained, and
generating these explanations traditionally requires extensive manual             only authorized researchers could access participant data. We devel-
effort.                                                                           oped an automated pipeline to convert the interaction logs into a textual
    Large Language Models in Logic. Recent applications demonstrate               representation of student problem solving states (PSS) (snapshots of
LLMs’ effectiveness in providing conversational support and personal-             problem solving after each step) (Barnes & Stamper, 2008) (Fig. 1).
ized instruction across various educational contexts (Roest et al., 2024;         These PSS representations were fed into our final LLM framework us-
Taneja et al., 2024; Venugopalan et al., 2024). Aashish et al. showed             ing carefully engineered prompts to generate targeted next-step hints
that students in an introductory programming course utilized a cus-               along with conceptual explanations for each PSS (Fig. 1).
tom GPT-4 AI tool for assignment help, and students primarily asked                   Intelligent Logic Tutor. Our logic tutor presents propositional logic
AI assistance for conceptual understanding rather than complete so-               (PL) problems to students in a graphical representation. Each prob-
lutions (Ghimire & Edwards, 2024). Systems like HypoCompass have                  lem shows a set of given statements at the top of the workspace and
demonstrated that LLM-augmented ITS can generate high-quality train-              a conclusion to be derived at the bottom (Fig. 2). Students solve the
ing materials and significantly improve student performance (Ma et al.,           problems by iteratively deriving new logic statements until they arrive
2024). However, the application of LLMs to formal logic instruction               at the conclusion. The tutor divides the problems into three sections:
presents unique challenges. While foundational datasets like ProofWriter          pretest, training, and posttest. Students’ prior knowledge is measured in
(Tafjord et al., 2020) enable multi-hop proofs and FOLIO (Han et al.,             the pretest section. The training section consists of five ordered levels
2022) introduces complex first-order logic (FOL) expressions, existing            with increasing difficulty. This is the only section where students can
benchmarks remain narrowly scoped. ProntoQA (Saparov & He, 2022)                  request and receive hints. Finally, students complete a posttest section
focuses on just one FOL rule (modus ponens). LogicBench (Parmar et al.,           consisting of six problems without any tutor assistance. The tutor uses
2024) covers a larger set of inference rules, and it reveals critical per-        a data-driven method to generate next-step hints with template-based
formance gaps even in state-of-the-art models like GPT-4. Moreover,               explanations to guide students given their current progress.

                                                                              2
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                  Computers and Education: Arti cial Intelligence 9 (2025) 100490




Fig. 1. Example of a student problem-solving state and generated hints. The top box presents the student’s derivation steps, while the bottom two boxes present the
LLM- and tutor-generated hints.




Fig. 2. The full interface of the logic tutor, showing the given statements at the top of the workspace and a conclusion to be derived at the bottom. The middle pane
contains the rule buttons.


3.1. Model selection and prompt engineering                                                Thus, it relies on the model’s inherent reasoning and problem-
                                                                                           solving capabilities, testing its capacity to generalize with no prior
    We evaluated four state-of-the-art LLMs: Llama-3-70B-Instruct
                                                                                           guidance.
(AI@Meta, 2024), Gemini-Pro (Anil et al., 2023), GPT-4o (Achiam et al.,
                                                                                        2. Few Shot Plan and Solve (FS_PlanAndSolve) This technique in-
2023), and DeepSeek-V3 (Liu, Feng et al., 2024). We set the temperature
                                                                                           structs the LLM to decompose a problem into subgoals and address
parameter to 0.1 for all LLMs to limit the randomness and variability of
                                                                                           each subgoal one by one. Two training examples are included in
responses and improve accuracy. We opted not to use the LLMs, such as
                                                                                           the prompt to demonstrate this approach, with the goal of help-
o1 or DeepSeek-Reasoner, as they currently require significant computa-
                                                                                           ing the model learn to break its problem-solving process into
tional resources and are not yet practical for deployment in a classroom
                                                                                           smaller intermediate subgoals. This problem decomposition–re-
setting. Each prompt is structured consistently (Fig. 3) and is designed to
                                                                                           composition strategy promotes logical consistency across complex
incorporate evidence-based learning science principles (Stamper et al.,
                                                                                           tasks.
2024). Our prompt engineering framework implements six increasingly
                                                                                        3. Few Shot Chain of Thought (FS_CoT) Chain-of-thought (CoT)
advanced techniques, building upon Zero-Shot (ZS) and Few-Shot (FS)
                                                                                           prompting provides the model with examples that demonstrate a
prompting (Brown et al., 2020) with Chain-of-Thought (CoT) reasoning
                                                                                           series of intermediate reasoning steps. Through these exemplars,
(Wei et al., 2022). The techniques are summarized in Table 1.
                                                                                           the model may learn to articulate its own reasoning more transpar-
                                                                                           ently. Previous studies have shown that CoT significantly improves
   1. Zero Shot (ZS) Zero-shot prompting elicits step-by-step solutions                    the reasoning abilities of LLMs (Wei et al., 2022).
      and output expectations without providing any training examples.

                                                                                 3
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                            Computers and Education: Arti cial Intelligence 9 (2025) 100490


                                                                                                  6. Few Shot Tree of Thoughts Chain of Thought (FS_ToT_CoT)
                                                                                                     In this approach, the solution path branches out across multiple
                                                                                                     reasoning “threads” or experts, each contributing a step-by-step
                                                                                                     proof. We added examples in the prompt where three experts
                                                                                                     collaboratively debated each step, acknowledged and corrected
                                                                                                     mistakes, and refined their step derivations. This collaborative in-
                                                                                                     terplay forms a tree-like structure of possible solution paths: if a
                                                                                                     line of reasoning fails, it is pruned when the expert acknowledges
                                                                                                     their mistake; successful lines continue to expand. This approach
                                                                                                     is intended to ensure that alternative proofs are considered and
                                                                                                     validated.



                                                                                               3.2. Data splits

                                                                                                   We used the first two examples that students see in the tutor (as
                                                                                               shown in Appendix A) for few-shot prompting of every LLM to provide
                                                                                               appropriate logic proof structures. We set the LLM temperature param-
                                                                                               eter to 0.1 to achieve consistency but allow for some randomness. For
                                                                                               each dataset, we split the data into validation (35 %) and test (65 %)
                                                                                               sets using a fixed random seed (42) to ensure reproducibility. To refine
                                                                                               the LLM prompts, we iteratively refined the prompt templates based
                                                                                               on the validation set performance guided by two primary criteria: (1)
                                                                                               maximizing accuracy, and (2) minimizing syntax errors detected by our
                                                                                               automated logic checker (i.e., solutions that could not be parsed). The
                                                                                               iteration process was stopped when accuracy plateaued and no further
                                                                                               improvements were observed across consecutive refinement attempts.
Fig. 3. Abstract prompt template incorporating context, instructions, output                   To mitigate the risk of overfitting to the validation set, we allocated the
expectations, examples, and user prompts.                                                      majority (65 %) of the data to the test set. Once the prompt template
                                                                                               was finalized, we ran the models only on the test set and reported the
                                                                                               final results.
Table 1
Summarized descriptions of six prompting techniques.                                           3.3. Evaluation framework
  Technique                 Title & description                                                    The built-in logic checker in the logic tutor automatically verified
  1. ZS                     Zero Shot: Demonstrates step-by-step solutions with-               the correctness of all LLM-generated proof steps and hints, ensuring rel-
                            out training examples, relying on the model’s inherent             evance within the tutor context. We conducted a qualitative evaluation
                            reasoning capabilities.
                                                                                               of LLM-generated hints and explanations by two experts with 2–4 years
  2. FS_PlanAndSolve        Few Shot Plan and Solve: Instructs the LLM to decompose
                            problems into subgoals, demonstrated through two training          of experience as teaching assistants and researchers in logic and ITS.
                            examples aiming for better logical consistency.                        The evaluation rubrics (Table 2) were comprised of four key met-
  3. FS_CoT                 Few Shot Chain of Thought: Provides examples demon-                rics: consistency, clarity, justification, and subgoaling. To ensure the
                            strating intermediate reasoning steps, enabling the model          suitability of the metrics for our tutor context, our two domain experts
                            to articulate transparent reasoning.
                                                                                               collaborated and iteratively refined them until a consensus was reached
  4. FS_L_DCoT              Few Shot Logical Dual CoT: Integrates both direct and
                            indirect proof strategies, demonstrating alternate logical         with a course instructor expert. These metrics capture essential quali-
                            paths and cross-verification.                                      ties of effective hint explanations proposed in previous work (Daheim
  5. FS_BL_DCoT             Few Shot Bidirectional Logical Dual CoT: Combines                  et al., 2024; Jeuring et al., 2022; Macina et al., 2023; Maurya et al.,
                            forward chaining (premises to conclusion) with backward
                                                                                               2024; Roest et al., 2024; Tack & Piech, 2022). First, high-quality hints
                            chaining (conclusion to premises) for additional validation.
  6. FS_ToT_CoT             Few Shot Tree of Thoughts CoT: Uses multiple reasoning
                                                                                               must maintain logical consistency with both the student’s current proof
                            “threads” where experts collaboratively debate, forming a          state and the domain rules permitted by the tutor (Macina et al., 2023).
                            tree-like structure that prunes failed reasoning paths and         Second, hints should provide clarity through clear, actionable guidance
                            validates successful ones.                                         without vagueness or extraneous details, enabling students to under-
                                                                                               stand their next steps (Daheim et al., 2024; Kotalwar et al., 2024).
                                                                                               Third, effective hints incorporate justification or rationale to deepen

   4. Few Shot Logical Dual Chain of Thought (FS_L_DCoT) Building
      on the CoT concept, this approach integrates both direct and
                                                                                               Table 2
      indirect proof strategies. This technique provides the LLM with
                                                                                               Evaluation Criteria for LLM-generated hint explanations.
      examples that demonstrate how to consider alternative logical
      paths and cross-verify them. By encouraging the exploration of                            Criteria                     Definition

      multiple reasoning paths, this approach reduces the likelihood of                         Consistency                  Does the hint follow the tutor’s domain rules and
      overlooking potential mistakes or alternative solutions.                                                               align with the student’s current proof state?
                                                                                                Clarity                      Is the hint clearly written and free of irrelevant or
   5. Few Shot Bidirectional Logical Dual Chain of Thought (FS_BL
                                                                                                                             excessive details?
      _DCoT) This strategy augments the Dual CoT by combining for-                              Justification                Does the hint provide a rationale or reasoning for
      ward chaining (from premises to conclusion) with backward                                                              why the next step was suggested?
      chaining (from conclusion back to premises). By working in both                           Subgoaling                   Does the hint provide a larger context (without
      directions, the model may gain an additional layer of validation                                                       giving away the full solution) explaining how the
                                                                                                                             step will help work on other statements?
      and error detection.

                                                                                           4
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                    Computers and Education: Arti cial Intelligence 9 (2025) 100490


student understanding of the underlying reasoning (Jeuring et al., 2022,               Table 3
Tack & Piech, 2022). Finally, hint explanations benefit from including                 Performance of different LLMs in different zero-shot and few-shot settings, mea-
subgoals as high-level guidance to help students develop an under-                     sured by accuracy on two datasets: LT and SPL. Boldface indicates the best
standing of the more general problem-solving skills beyond immediate                   accuracy score for each prompt technique.
procedural steps (Cucuiat & Waite, 2024; Morrison et al., 2016; Shabrina                Prompt Technique     Llama-3         Gemini-Pro      GPT-4o          DeepSeek-V3
et al., 2023; Tithi et al., 2025).
                                                                                                             LT     SPL      LT     SPL      LT       SPL    LT     SPL
    We used stratified random sampling, with stratification done by
                                                                                        1. ZS                24.4   34.1     37.7   40.5     67.9     68.3   75.7   72.2
problem to ensure problem diversity. For each problem, we sampled
                                                                                        2. FS_CoT            65.7   62.6     59.0   67.0     76.9     83.6   83.7   84.4
20 % from the set of unique solution states, using a fixed random seed                  3. FS_PlanAndSolve   56.7   60.2     49.8   50.3     75.5     79.9   79.0   83.0
(42) for reproducibility. The hints and explanations for the sampled solu-              4. FS_BL_DCoT        49.1   52.3     58.5   67.4     76.7     79.8   84.4   84.9
tion states were rated on each rubric on a scale from 1 to 4 (with 4 being              5. FS_L_DCoT         63.8   64.6     54.9   50.3     73.5     75.5   84.4   84.4
the best). We used Spearman correlation (𝜌) and Quadratic Weighted                      6. FS_ToT_CoT        59.1   56.1     51.7   60.4     72.7     82.4   85.0   86.7

Cohen’s Kappa (𝑄𝑊 𝐾) to obtain inter-rater agreement on the assess-
ment dimensions, which are common reliability measurements between                     Table 4
two raters (Naismith et al., 2023; Tian et al., 2024). We also used a                  Mean Parent length for Correct vs Incorrect steps across models and prompt tech-
rubric-based LLM grader to understand the potential of using it as an                  niques. Within each model, the shaded ‘C’ column reports the mean for correct
automated evaluator.                                                                   steps; the ‘Inc’ column reports the mean for incorrect steps.

                                                                                        Prompt Technique      Llama-3         Gemini-Pro      GPT-4o         DeepSeek-V3
4. Results
                                                                                                              C        Inc    C      Inc      C        Inc   C       Inc
4.1. RQ1: evaluating logic proof construction performance                               1. ZS                 2.3      6.0    2.8    7.0      3.9      6.5   4.0     8.7
                                                                                        2. FS_CoT             4.4      6.9    3.9    6.5      4.9      8.0   4.8     8.1
    We evaluated the performance of four LLMs (Llama-3, Gemini-
                                                                                        3. FS_PlanAndSolve    4.3      8.1    3.6    8.2      4.6      7.5   4.8     9.8
Pro, GPT-4o, and DeepSeek-V3) using six prompting techniques on the                     4. FS_BL_DCoT         4.1      8.7    4.1    7.1      4.8      6.3   4.7     7.4
two logic tutor (LT) and symbolic propositional logic (SPL) datasets.                   5. FS_L_DCoT          4.4      7.1    4.0    6.9      4.6      6.9   4.8     9.0
DeepSeek-V3 demonstrated superior accuracy in most prompt config-                       6. FS_ToT_CoT         4.3      6.5    3.6    6.0      4.6      6.9   4.8     7.5
urations, with the best FS_ToT_CoT prompts achieving 85.0 % and
86.7 % accuracy for the steps generated for full solutions of LT and SPL               Table 5
problems, respectively (Table 3). GPT-4o also exhibited strong perfor-                 Rule accuracy for comparison of DeepSeek-V3 and GPT-4o across all prompting
mance, particularly on SPL with FS_CoT prompts (83.6 %). Gemini-Pro                    techniques.
showed mixed results, while Llama-3 generally underperformed. All
zero-shot prompted models underperformed, indicating the importance
of in-context prompting in the integration of LLMs into ITSs.
    To differentiate the capabilities of the LLMs, we explored the com-
plexity of each problem, as measured by the lengths of the statements
combined to derive new steps. We hypothesized that longer parent state-
ments would be more likely to lead to reasoning errors (incorrect steps),
as they typically do for students. In Table 4, we show the mean lengths
of the parent statements for correct steps (in column ‘C’) and for incor-
rect steps (in column ‘Inc’) for four LLMs (Llama-3, Gemini-Pro, GPT-4o,
and DeepSeek-V3) in six prompting techniques on both LT and SPL
datasets combined.1 We compared the lengths of parent statements be-
tween correct and incorrect steps, and for each LLM, the lengths of the
parent statements were significantly longer for incorrect versus correct
steps with 𝑝 < 0.001 in each comparison. This suggests longer parent                   achieved comparable accuracy with simpler prompting, making it our
statements may introduce ambiguity, leading to more incorrect steps.                   preferred choice. Using DeepSeek-V3 with FS_CoT, we generated next-
    Rule-Specific Performance Analysis. For all the FS-based prompt-                   step hints and conceptual explanations for the LT PSS dataset containing
ing techniques and the GPT-4o and DeepSeek-V3 models, we calculated                    1050 unique student problem-solving states. Each state represents a
the average accuracy across different logical rules. As shown in Table 5,              snapshot of a student’s progress, containing all steps completed at that
DeepSeek-V3 and GPT-4o both achieved high accuracy on basic rules                      point, and transformed from a graphical into a natural language-based
(Com, Add, Conj, Simp) while DeepSeek-V3 maintained stronger perfor-                   form. DeepSeek-V3 with FS_CoT was used to generate the next best step
mance on the rules MP, DeM, MT, HS, DS and Contra. The performance                     hint for each state. A modified version of the LT logic checker was used
of GPT-4o declined with higher rule complexity (as measured by num-                    to evaluate correctness, with any hint considered to be incorrect if the
ber of operators including negations). The most challenging rules were                 step was logically incorrect, the suggested step was already present in
Contra, CP, DN, and Impl, although DeepSeek-V3 still outperformed                      the student solution, or if the parent steps were not yet derived. Overall,
GPT-4o.                                                                                75 % of the resulting hints were rated as correct/accurate. Accuracy
                                                                                       across the specific logical rules is shown in Fig. 4. The model struggled
4.2. RQ2a: evaluating next-step hint generation performance                            most with complex rules like DS, Impl, Add, DN, MT, DeM, CP. With
    Based on RQ1, DeepSeek-V3 performed better than all other LLMs.                    the exception of Addition, all of these rules handle negations, introduc-
While more complex prompting like bidirectional dual CoT and tree-                     ing complexity into the application of rules. Addition introduces a new
of-thoughts CoT improved accuracy, their lengthier and more complex                    variable into a proof, which adds another type of complexity.
prompts appeared difficult to adapt for the hint generation task. FS_CoT                   We compared the performance of DeepSeek-V3 to our logic tutor’s
                                                                                       data-driven hint mechanism, which utilizes historical data to identify
                                                                                       optimal next steps. DeepSeek-V3 generated a higher number of unique
  1
    We present the mean lengths of the parent statements for correct steps and         hints per problem on average (M=4.5) compared to the tutor (M=3.0).
incorrect steps for each technique after combining the two datasets, LT and SPL.       The overall hint accuracy of 75 % is promising. However, accuracy var-
The results for each dataset separately yielded similar results.                       ied across the tutor levels. While the LLM achieved 87.9 % accuracy in

                                                                                   5
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                            Computers and Education: Arti cial Intelligence 9 (2025) 100490




                                                  Fig. 4. The distribution of correct and incorrect LLM-generated hints for each rule.


                                Table 6
                                Inter-rater agreement metrics for evaluation of 210 LLM-generated explanations. (𝜌 = Spearman’s Correlation,
                                𝑄𝑊 𝐾 = Quadratic Cohen’s Kappa. † 𝑝 > Bonferronithreshold ).

                                  Dimension             Human-Human            Avg rating (Human)        Human-LLM                Avg Rating (LLM)
                                                        𝝆          𝑸𝑾 𝑲                                  𝝆           𝑸𝑾 𝑲

                                  Consistency           0.90       0.85        3.9                       0.59        0.30         3.81
                                  Clarity               0.93       0.92        3.09                      0.54        0.56         2.92
                                  Justification         0.92       0.92        2.24                      0.55        0.59         2.39
                                  Subgoaling            0.77       0.79        1.66                      0.08†       0.16†        2.47



the first training level, the number of unique hints increased, and accu-                      that combine both negation and implication increase the complexity
racy declined across the 5 training levels. Since difficulty and the number                    even more, such as Modus Tollens and Contrapositive ((𝑝 → 𝑞) ⟹
of logic rules needed increase at each level, the size of the potential so-                    (¬𝑞 → ¬𝑝)). Johnson et al. argued that rules involving negation require
lution space expands. This larger solution space may have led to lower                         working memory to track inverted truth values across multiple steps,
hint accuracy and the generation of more unique hints by DeepSeek-V3.                          thus increasing cognitive load (Johnson-Laird, 2001). Anderson et al. re-
                                                                                               ported that humans exhibit slower response times and higher error rates
4.3. RQ2b: evaluating next-step hint explanations                                              when processing negated statements like ¬(𝐴 ∧ 𝐵), due to the increased
                                                                                               cognitive load associated with maintaining dual truth states (Anderson,
    Two expert graders independently applied the evaluation rubrics
                                                                                               2013).
(Table 2) to a sample of 210 LLM-generated conceptual explanations.
                                                                                                   The challenge in tackling negation was also observed in the per-
Table 6 shows a strong inter-rater agreement for the expert human
                                                                                               formance of the involved LLM models in our study. In logic proof
graders across all dimensions. The Spearman correlation (𝜌) ranged from
                                                                                               construction, although DeepSeek-V3 (Table 3) achieved high accuracy
0.77 to 0.93, and the 𝑄𝑊 𝐾 values ranged from 0.79 to 0.92, suggesting
                                                                                               on basic rules (e.g., Commutative (Com): 99.23 %), the model struggled
near-perfect reliability (McHugh, 2012). These high agreement metrics
                                                                                               with more complex rules (e.g., CP: 64.07 %). Our results suggest that
suggest that our evaluation criteria were well-defined and consistently
                                                                                               LLMs encounter difficulties in propagating negation through inference
applied by the expert human raters. The sampled LLM explanations were
                                                                                               chains, often struggling with expressions like ¬(𝐴 ∧ 𝐵) and ¬𝐴 ∧ ¬𝐵. This
highly rated for consistency and clarity, with human-rater scores of 3.90
                                                                                               resembles a similar reasoning bottleneck found in human cognition.
and 3.09 out of 4, respectively. However, the system showed room for
                                                                                                   The length of parent logic statements being combined also intro-
improvement in other areas, with expert human rater scores of 2.24
                                                                                               duces complexity, usually via nested statements, which further intro-
for justification and 1.66 for subgoaling. We applied an LLM grader us-
                                                                                               duces more cognitive load and working memory demands for humans.
ing the same rubrics to the sample of explanations and compared their
                                                                                               Similarly, a strong negative correlation was found between parent state-
rubric scores with the expert human ratings. While the LLM grader as-
                                                                                               ment length and accuracy of LLMs. It may be that longer parent state-
signed consistency and clarity scores comparable to human scores, it
                                                                                               ments introduce ambiguities or combinatorial explosions that exceed
overestimated human scores in justification and subgoaling. However,
                                                                                               the contextual reasoning capacity of current LLM models. Preprocessing
the rubric-based LLM grader exhibited weaker agreement with human
                                                                                               inputs into simpler structures may improve the logical reasoning perfor-
graders, particularly in subgoaling, where the average LLM subgoaling
                                                                                               mance of current LLMs.
score was 2.47 as opposed to the human subgoaling score of 1.66.
                                                                                                   Overall, DeepSeek-V3 with FS_CoT achieved an average accuracy
                                                                                               of 75 % for hint generation, but its hint accuracy was higher for
5. Discussion
                                                                                               earlier training problems and declined across the training levels as
    Logic rules can be considered basic or complex based on their use                          difficulty increased (from 87.9 % to 63.2 %). These accuracy levels
of negation. Basic rules such as Simplification or Commutative involve                         are not high enough for integration into ITSs, as student trust can
direct and single-step operations (e.g., (𝑝 ∨ 𝑞) ⟹ (𝑞 ∨ 𝑝)). On the other                      shift quickly when encountering even one that is inaccurate or not
hand, the rules involving negation (e.g., DeMorgans) cause challenges                          aligned with student thinking, potentially leading to help avoidance
for people and for LLMs. The implication operator → inherently includes                        (Price, Zhi & Barnes, 2017). In our experiment, LLMs also sometimes
negation as part of its definition ((𝑝 → 𝑞) ⟺ (¬𝑝 ∨ 𝑞)). Statements                            generated sub-optimal hints based on the redundant statements derived

                                                                                           6
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                   Computers and Education: Arti cial Intelligence 9 (2025) 100490


by the students and failed to reorient the students to an optimal solution        tool/service, the authors reviewed and edited the content as needed and
path.                                                                             take full responsibility for the content of the publication.
    Our LLM-generated hint explanations achieved higher scores on the
consistency and clarity dimensions (Table 6), indicating that our se-             Declaration of competing interest
lected LLM could follow specified rules and provide clear explanations.
                                                                                      The authors declare that they have no known competing financial
However, its justification and subgoaling scores were comparatively
                                                                                  interests or personal relationships that could have appeared to influence
lower, suggesting LLMs sometimes struggle to articulate why a partic-
                                                                                  the work reported in this paper.
ular step was suggested within the larger problem or subgoal context.
This limitation echoes critiques of LLMs as “stochastic parrots” (Bender          Acknowledgement
et al., 2021) in educational contexts—they replicate surface-level pat-
terns but lack intentional pedagogy, which is critical for learning (Aleven          The work is supported by the National Science Foundation (NSF)
et al., 2003). Together with inaccuracy and these explanation ratings,            grant 2013502.
our results highlight the need to build hybrid systems in which LLMs
propose candidate hints, but they are checked for domain validity (e.g.           Appendix A. Few-shot prompting examples
symbolic checkers in math (He-Yueya et al., 2023)) and for pedagogical               This section provides two example problems used in few-shot
appropriateness.                                                                  prompting in our logic proof generation tasks.

6. Conclusion                                                                     Example 1

    Our work provides insights into the potential and current limitations         Givens: (𝑅 ∗ 𝑁) > 𝑂, −𝑂 ∗ (−𝑊 > 𝐴), (𝑈 > 𝐾) + (𝑅 ∗ 𝑁), 𝐾 > −𝑊
of LLMs in logic tutoring systems, specifically examining their capabili-         Conclusion: 𝑈 > 𝐴
ties across proof construction, hint generation, and explanation quality.         Step-by-step Proof:
While models like DeepSeek-V3 and GPT-4o demonstrate promising per-
formance in generating step-by-step solutions (achieving up to 86.7 %                1. (𝑅 ∗ 𝑁) > 𝑂, Given
accuracy) and producing factually correct hints (75 % accuracy) with                 2. −𝑂 ∗ (−𝑊 > 𝐴), Given
clear and consistent conceptual explanations, significant challenges re-             3. (𝑈 > 𝐾) + (𝑅 ∗ 𝑁), Given
main in ensuring better pedagogical alignment. Our study also had                    4. 𝐾 > −𝑊 , Given
several limitations. Our evaluation was limited to single-step accuracy              5. −𝑂, Simp (2)
for problem-solving in one domain. Future work should evaluate the                   6. −𝑊 > 𝐴, Simp (2)
optimality of LLM-constructed full solutions. Additionally, our study                7. −(𝑅 ∗ 𝑁), MT (5, 1)
did not include reasoning models such as OpenAI’s o1 or DeepSeek’s                   8. 𝑈 > 𝐾, DS (7, 3)
reasoning models, which employ extended chain-of-thought processes                   9. 𝑈 > −𝑊 , HS (8, 4)
and may offer improved performance in logical reasoning tasks. In the               10. 𝑈 > 𝐴, HS (9, 6)
future, it can be investigated whether these reasoning models can pro-
vide more pedagogically sound explanations and proofs, as well as the             Example 2
feasibility of deploying such models at scale in classroom settings, con-
sidering their computational costs and response latencies. The human              Givens: 𝐴 > 𝐸, 𝐻 > (𝐾 ∗ 𝐴), −(𝐾 ∗ 𝐸)
evaluation of hint explanations covered only 20 % of the dataset, po-             Conclusion: −𝐻
tentially limiting generalizability; and although we evaluated 4 criteria         Step-by-step Proof:
for hint explanations, other pedagogical elements may be important for
human understanding and learning. Future work should focus on devel-                 1. 𝐴 > 𝐸, Given
oping hybrid architectures to combine LLM capabilities with learning                 2. 𝐻 > (𝐾 ∗ 𝐴), Given
science principles to bridge the gap between the potential of LLMs and               3. −(𝐾 ∗ 𝐸), Given
the nuanced demands of a pedagogical environment.                                    4. −𝐾 + −𝐸, DeM (3)
                                                                                     5. −𝐸 + −𝐾, Com (4)
CRediT authorship contribution statement                                             6. 𝐸 > −𝐾, Impl (5)
                                                                                     7. 𝐴 > −𝐾, HS (1, 6)
   Sutapa Dey Tithi: Writing – review & editing, Writing – original                  8. −𝐴 + −𝐾, Impl (7)
draft, Visualization, Validation, Project administration, Methodology,               9. −(𝐴 ∗ 𝐾), DeM (8)
Investigation, Formal analysis, Data curation, Conceptualization. Arun              10. −(𝐾 ∗ 𝐴), Com (9)
Kumar Ramesh: Writing – review & editing, Software, Resources,                      11. −𝐻, MT (10, 2)
Methodology, Conceptualization. Clara DiMarco: Writing – re-
view & editing, Writing – original draft, Validation, Methodology,                References
Conceptualization. Xiaoyi Tian: Writing – review & editing,
                                                                                  Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D.,
Visualization, Validation, Supervision, Methodology, Investigation,                  Altenschmidt, J., Altman, S., Anadkat, S., et al. (2023). Gpt-4 technical report. arXiv
Formal analysis, Conceptualization. Nazia Alam: Writing – review &                   preprint arXiv:2303.08774.
editing, Validation, Resources, Data curation. Kimia Fazeli: Writing –            AI@Meta. (2024). Llama 3 model card. https://github.com/meta-llama/llama3/blob/
                                                                                     main/MODEL_CARD.md.
review & editing, Validation, Resources, Data curation. Tiffany Barnes:           Aleven, V., Stahl, E., Schworm, S., Fischer, F., & Wallace, R. (2003). Help seeking and
Writing – review & editing, Validation, Supervision, Resources, Project              help design in interactive learning environments. Review of Educational Research, 73,
administration, Methodology, Investigation, Funding acquisition,                     277–320.
                                                                                  Aleven, V. A., & Koedinger, K. R. (2002). An effective metacognitive strategy: Learning
Conceptualization.
                                                                                     by doing and explaining with a computer-based cognitive tutor. Cognitive Science, 26,
                                                                                     147–179.
Declaration of generative AI and AI-assisted technologies in the                  Anderson, J. R. (2013). The adaptive character of thought. Psychology Press.
                                                                                  Anderson, J. R., Corbett, A. T., Koedinger, K. R., & Pelletier, R. (1995). Cognitive tutors:
writing process                                                                      Lessons learned. The Journal of the Learning Sciences, 4, 167–207.
                                                                                  Anil, R., Borgeaud, S., Wu, Y., Alayrac, J. B., Yu, J., Soricut, R., Schalkwyk, J., Dai, A. M.,
   During the preparation of this work, the authors used OpenAI                      Hauth, A., Millican, K., et al. (2023). Gemini: A family of highly capable multimodal
ChatGPT (GPT-4o) to improve language and readability. After using this               models. arXiv preprint arXiv:2312.11805 1.

                                                                              7
S.D. Tithi, A.K. Ramesh, C. DiMarco et al.                                                                                         Computers and Education: Arti cial Intelligence 9 (2025) 100490


Barnes, T., & Stamper, J. (2008). Toward automatic hint generation for logic proof tutoring            Murray, T. (2003). An overview of intelligent tutoring system authoring tools: Updated
    using historical student data. In International conference on intelligent tutoring systems             analysis of the state of the art. In Authoring tools for advanced technology learning en-
    (pp. 373–382). Springer.                                                                               vironments: Toward cost-effective adaptive, interactive and intelligent educational software
Barnes, T., Stamper, J. C., Lehmann, L., & Croy, M. J. (2008). A pilot study on logic proof                (pp. 491–544). Springer.
    tutoring using hints generated from historical student data. In EDM (pp. 197–201).                 Naismith, B., Mulcaire, P., & Burstein, J. (2023). Automated evaluation of written dis-
Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of                   course coherence using gpt-4. In Proceedings of the 18th workshop on innovative use of
    stochastic parrots: Can language models be too big? In Proceedings of the 2021 ACM                     NLP for building educational applications (BEA 2023) (pp. 394–403).
    conference on fairness, accountability, and transparency (pp. 610–623).                            Nye, B. D., Mee, D., & Core, M. G. (2023). Generative large language models for dialog-
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A.,                 based tutoring: An early consideration of opportunities and concerns. In LLM@ AIED
    Shyam, P., Sastry, G., Askell, A., et al. (2020). Language models are few-shot learners.               (pp. 78–88).
    Advances in Neural Information Processing Systems, 33, 1877–1901.                                  Parmar, M., Patel, N., Varshney, N., Nakamura, M., Luo, M.Mashetty, S., et al. (2024).
Canfield, W. (2001). Aleks: A web-based intelligent tutoring system. Mathematics and                       Logicbench: Towards systematic evaluation of logical reasoning ability of large
    Computer Education, 35, 152.                                                                           language models. In Proceedings of the 62nd annual meeting of the association for
Chi, M., & VanLehn, K. (2010). Meta-cognitive strategy instruction in intelligent tutoring                 computational linguistics (Volume 1: Long Papers) (pp. 13679–13707).
    systems: How, when, and why. Journal of Educational Technology & Society, 13, 25–39.               Phung, T., Cambronero, J., Gulwani, S., Kohn, T., Majumdar, R., Singla, A., & Soares, G.
Cucuiat, V., & Waite, J. (2024). Feedback literacy: Holistic analysis of secondary educators’              (2023). Generating high-precision feedback for programming syntax errors using large
    views of llm explanations of program error messages. In Proceedings of the 2024 on                     language models. arXiv preprint arXiv:2302.04662.
    innovation and technology in computer science education V.1 (pp. 192–198).                         Phung, T., Pădurean, V. A., Singh, A., Brooks, C., Cambronero, J.Gulwani, S., et al. (2024).
Daheim, N., Macina, J., Kapur, M., Gurevych, I., & Sachan, M. (2024). Stepwise verification                Automating human tutor-style programming feedback: Leveraging gpt-4 tutor model
    and remediation of student reasoning errors with large language model tutors. arXiv                    for hint generation and gpt-3.5 student model for hint validation. In Proceedings of the
    preprint arXiv:2407.09136.                                                                             14th learning analytics and knowledge conference (pp. 12–23).
Ghimire, A., & Edwards, J. (2024). Coding with ai: How are tools like chatgpt being used by            Price, T. W., Dong, Y., & Lipovac, D. (2017). Isnap: Towards intelligent tutoring in
    students in foundational programming courses. In International conference on artificial                novice programming environments. In Proceedings of the 2017 ACM SIGCSE technical
    intelligence in education (pp. 259–267). Springer.                                                     symposium on computer science education (pp. 483–488).
Gottlieb, E. (2024). Propositional-logic. https://doi.org/10.5281/zenodo.14567918.                     Price, T. W., Zhi, R., & Barnes, T. (2017). Hint generation under uncertainty: The effect
    https://huggingface.co/datasets/ergotts/propositional-logic.                                           of hint quality on help-seeking behavior. In Artificial Intelligence in Education: 18th
Han, S., Schoelkopf, H., Zhao, Y., Qi, Z., Riddell, M., Zhou, W., Coady, J., Peng, D., Qiao,               International Conference, AIED 2017, Wuhan, China, June 28–July 1, 2017, Proceedings
    Y., Benson, L., et al. (2022). Folio: Natural language reasoning with first-order logic.               18 (pp. 311–322). Springer.
    arXiv preprint arXiv:2209.00840.                                                                   Ritter, S., Anderson, J. R., Koedinger, K. R., & Corbett, A. (2007). Cognitive tutor: Applied
He-Yueya, J., Poesia, G., Wang, R. E., & Goodman, N. D. (2023). Solving math word                          research in mathematics education. Psychonomic Bulletin & Review, 14, 249–255.
    problems by combining language models with symbolic solvers. arXiv preprint                        Rivers, K., & Koedinger, K. R. (2017). Data-driven hint generation in vast solution spaces: A
    arXiv:2304.09102.                                                                                      self-improving python programming tutor. International Journal of Artificial Intelligence
Holland, J., Mitrovic, A., & Martin, B. (2009). J-latte: A constraint-based tutor for java.                in Education, 27, 37–64.
Holstein, K., McLaren, B. M., & Aleven, V. (2019). Designing for complementarity: Teacher              Roest, L., Keuning, H., & Jeuring, J. (2024). Next-step hint generation for introductory
    and student needs for orchestration support in ai-enhanced classrooms. In Artificial                   programming using large language models. In Proceedings of the 26th Australasian
    intelligence in education: 20th International conference, AIED 2019, Chicago, IL, USA, June            Computing Education Conference (pp. 144–153). https://arxiv.org/pdf/2312.10055.
    25–29, 2019, Proceedings, Part I 20 (pp. 157–171). Springer.                                       Roll, I., Aleven, V., McLaren, B. M., & Koedinger, K. R. (2011). Improving students’ help-
Jeuring, J., Keuning, H., Marwan, S., Bouvier, D., Izu, C.Kiesler, N., et al. (2022). Towards              seeking skills using metacognitive feedback in an intelligent tutoring system. Learning
    giving timely formative feedback and hints to novice programmers. In: Proceedings of                   and Instruction, 21, 267–280.
    the 2022 working group reports on innovation and technology in computer science education          Saparov, A., & He, H. (2022). Language models are greedy reasoners: A systematic formal
    (pp. 95–115).                                                                                          analysis of chain-of-thought. arXiv preprint arXiv:2210.01240.
Johnson-Laird, P. N. (2001). Mental models and deduction. Trends in Cognitive Sciences, 5,             Saparov, A., Pang, R. Y., Padmakumar, V., Joshi, N., Kazemi, M., Kim, N., & He, H. (2023).
    434–442.                                                                                               Testing the general deductive reasoning capacity of large language models using ood
Kardan, S., & Conati, C. (2015). Providing adaptive support in an interactive simulation for               examples. Advances in Neural Information Processing Systems, 36, 3083–3105.
    learning: An experimental evaluation. In Proceedings of the 33rd annual ACM conference             Sedlmeier, P. (1997). Basicbayes: A tutor system for simple bayesian inference. Behavior
    on human factors in computing systems (pp. 3671–3680).                                                 Research Methods, Instruments, & Computers, 29, 328–336.
Koedinger, K. R., Anderson, J. R., Hadley, W. H., Mark, M. A., et al. (1997). Intelligent              Shabrina, P., Mostafavi, B., Tithi, S. D., Chi, M., & Barnes, T. (2023). Learning problem
    tutoring goes to school in the big city. International Journal of Artificial Intelligence in           decomposition–recomposition with data-driven chunky parsons problems within an
    Education, 8, 30–43.                                                                                   intelligent logic tutor. In International educational data mining society.
Koedinger, K. R., Corbett, A. T., & Perfetti, C. (2012). The knowledge-learning-instruction            Stamper, J., Eagle, M., Barnes, T., & Croy, M. (2013). Experimental evaluation of auto-
    framework: Bridging the science-practice chasm to enhance robust student learning.                     matic hint generation for a logic tutor. International Journal of Artificial Intelligence in
    Cognitive Science, 36, 757–798.                                                                        Education, 22, 3–17.
Kotalwar, N., Gotovos, A., & Singla, A. (2024). Hints-in-browser: Benchmarking lan-                    Stamper, J., Xiao, R., & Hou, X. (2024). Enhancing llm-based feedback: Insights from
    guage models for programming feedback generation. Advances in Neural Information                       intelligent tutoring systems and the learning sciences. In International Conference on
    Processing Systems, 37, 29864–29877.                                                                   Artificial Intelligence in Education (pp. 32–43). Springer.
Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C.,         Tack, A., & Piech, C. (2022). The ai teacher test: Measuring the pedagogical ability of
    et al. (2024). Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437.                          blender and gpt-3 in educational dialogues. arXiv preprint arXiv:2205.07540.
Liu, T., Xu, W., Huang, W., Wang, X., Wang, J., Yang, H., & Li, J. (2024). Logic-of-thought:           Tafjord, O., Mishra, B. D., & Clark, P. (2020). Proofwriter: Generating implications, proofs,
    Injecting logic into contexts for full reasoning in large language models. arXiv preprint              and abductive statements over natural language. arXiv preprint arXiv:2012.13048.
    arXiv:2409.17539. https://arxiv.org/pdf/2409.17539.                                                Taneja, K., Maiti, P., Kakar, S., Guruprasad, P., Rao, S., & Goel, A. K. (2024). Jill watson: A
Ma, Q., Shen, H., Koedinger, K., & Wu, S. T. (2024). How to teach programming in the                       virtual teaching assistant powered by chatgpt. In International Conference on Artificial
    ai era? using llms as a teachable agent for debugging. In International conference on                  Intelligence in Education (pp. 324–337). Springer.
    artificial intelligence in education (pp. 265–279). Springer.                                      Tian, X., Mannekote, A., Solomon, C. E., Song, Y., Wise, C. F.Mcklin, T., et al. (2024).
Macina, J., Daheim, N., Chowdhury, S. P., Sinha, T., Kapur, M., Gurevych, I., & Sachan,                    Examining llm prompting strategies for automatic evaluation of learner-created com-
    M. (2023). Mathdial: A dialogue tutoring dataset with rich pedagogical properties                      putational artifacts. In Proceedings of the 17th international conference on educational
    grounded in math reasoning problems. arXiv preprint arXiv:2305.14536.                                  data mining (pp. 698–706).
Maniktala, M., & Barnes, T. (2020). Deep thought: An intelligent logic tutor for discrete              Tithi, S. D., Tian, X., Chi, M., & Barnes, T. (2025). Investigating the impact and student
    math. In Proceedings of the 51st ACM technical symposium on computer science education                 perceptions of guided Parsons problems for learning logic with subgoals. arXiv preprint
    (pp. 1418).                                                                                            arXiv:2505.04712.
Marwan, S., Lytle, N., Williams, J. J., & Price, T. (2019). The impact of adding textual               Ueno, M., & Miyazawa, Y. (2017). Irt-based adaptive hints to scaffold learning in
    explanations to next-step hints in a novice programming environment. In Proceedings                    programming. IEEE Transactions on Learning Technologies, 11, 415–428.
    of the 2019 ACM conference on innovation and technology in computer science education              VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring
    (pp. 520–526).                                                                                         systems, and other tutoring systems. Educational Psychologist, 46, 197–221.
Maurya, K. K., Srivatsa, K., Petukhova, K., & Kochmar, E. (2024). Unifying ai tutor eval-              Venugopalan, D., Yan, Z., Borchers, C., Lin, J., & Aleven, V. (2024). Combining large lan-
    uation: An evaluation taxonomy for pedagogical ability assessment of llm-powered ai                    guage models with tutoring system intelligence: A case study in caregiver homework
    tutors. arXiv preprint arXiv:2412.09416.                                                               support. arXiv preprint arXiv:2412.11995. https://arxiv.org/pdf/2412.11995.
McHugh, M. L. (2012). Interrater reliability: The kappa statistic. Biochemia Medica, 22,               Wang, S., Xu, T., Li, H., Zhang, C., Liang, J.Tang, J., et al. (2024). Large language models
    276–282.                                                                                               for education: A survey and outlook. arXiv preprint arXiv:2403.18105.
Morrison, B. B., Margulieux, L. E., Ericson, B., & Guzdial, M. (2016). Subgoals help stu-              Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q. V., Zhou, D.,
    dents solve parsons problems. In Proceedings of the 47th ACM technical symposium on                    et al. (2022). Chain-of-thought prompting elicits reasoning in large language models.
    computing science education (pp. 42–47).                                                               Advances in Neural Information Processing Systems, 35, 24824–24837.




                                                                                                   8
