                                                     FIMO: A Challenge Formal Dataset for Automated Theorem Proving
                                                 Chengwu Liu1 , Jianhao Shen2 , Huajian Xin3 , Zhengying Liu4 , Ye Yuan1 , Haiming Wang3 ,
                                                     Wei Ju1 , Chuanyang Zheng5 , Yichun Yin4 , Lin Li2 , Ming Zhang1 * , Qun Liu4 * ,
                                                                          1
                                                                         Peking University, 2 Huawei HiSilicon, 3 Sun Yat-sen University,
                                                                          4
                                                                        Huawei Noah’s Ark Lab, 5 The Chinese University of Hong Kong
                                                   {liuchengwu, yuanye pku, juwei, mzhang cs}@pku.edu.cn, {shenjianhao2, liuzhengying2, yinyichun, lilin29,
                                                        qun.liu}@huawei.com, {xinhuajian2000, cyzhengme}@gmail.com, wanghm39@mail2.sysu.edu.cn,


                                                                      Abstract                               • Low difficulty level of existing datasets. Existing for-
arXiv:2309.04295v2 [cs.AI] 5 Dec 2023




                                          We present FIMO, an innovative dataset comprising formal             mal datasets often lean towards lower levels of com-
                                          mathematical problem statements sourced from the Interna-            plexity, potentially hindering models from obtaining the
                                          tional Mathematical Olympiad (IMO) Shortlisted Problems.             requisite skills. For example, while miniF2F offers 488
                                          Designed to facilitate advanced automated theorem proving            Olympiad mathematical problems, only 40 of which are
                                          at the IMO level, FIMO is currently tailored for the Lean for-       from the IMO context. IMO-level challenges inherently
                                          mal language. It comprises 149 formal problem statements,            pose heightened difficulty, and it is worth noting that
                                          accompanied by both informal problem descriptions and their          few of them have been successfully solved by automatic
                                          corresponding LATEX-based informal proofs. Through initial           provers yet (Polu and Sutskever 2020; Zheng, Han, and
                                          experiments involving GPT-4, our findings underscore the             Polu 2022; Polu et al. 2023; Wang et al. 2023).
                                          existing limitations in current methodologies, indicating a
                                          substantial journey ahead before achieving satisfactory IMO-       • Incompleteness of data. Most formal mathematical
                                          level automated theorem proving outcomes. The dataset has            datasets offer formal statements solely, neglecting cor-
                                          been made available on GitHub1 under the terms of the                responding statements or proofs in natural languages.
                                          Apache License.                                                      This absence not only compromises the statements’ in-
                                                                                                               terpretability but also hinders neural provers to leverage
                                                                Introduction                                   natural language proofs, a valuable resource often avail-
                                                                                                               able for high-school Olympiad mathematical problems.
                                        Automated theorem proving is a challenging yet critical
                                        field, undergoing rapid evolution and garnering considerable          IMO stands as a reputable measure of human mathe-
                                        research attention in recent times. While significant progress     matical proficiency, often serving as an effective predic-
                                        has been taken since the advent of large language mod-             tor of individual capabilities. Inspired by this, we postu-
                                        els (LLMs), the challenge of tackling high-school mathe-           late that the mastery of IMO-level intricate mathematical
                                        matical problems of International Mathematical Olympiad            problems could also serve as an indicator of large language
                                        (IMO) level complexity, which demands profound mathe-              models’ (LLMs) problem-solving abilities. In response to
                                        matical reasoning and problem-solving capabilities, remains        the aforementioned challenges, we present FIMO, a formal-
                                        a pivotal open question. Current investigations reveal that        ized IMO-level mathematical problem dataset with informal
                                        LLM-based provers exhibit limited capabilities, managing           statements and proofs. To lower the cost of formalization,
                                        to address few IMO problems and leaving the majority un-           our approach entails the automated formalization (transla-
                                        explored. This phenomenon warrants the exploration of sev-         tion from natural language mathematics to formal languages
                                        eral potential factors:                                            like Lean) of the IMO Shortlisted Problems. These problems
                                                                                                           are thoughtfully curated by the IMO’s problem selection
                                          • High cost of formalization. The realm of formal math-
                                                                                                           committee, mirroring the complexity of IMO challenges.
                                            ematical data is marked by scarcity since crafting for-
                                                                                                           Leveraging the reflective capabilities inherent in LLMs, we
                                            mal mathematical data demands extensive effort from
                                                                                                           substantially enhance the subset of problems amenable to
                                            expert humans and consequently comes at a substantial
                                                                                                           auto-formalization. The proposed dataset, FIMO, consists of
                                            cost. For instance, even one of the most extensive for-
                                                                                                           149 formal statements in Lean as well as the corresponding
                                            mal mathematics repositories, mathlib, a collaborative
                                                                                                           informal statements and proofs in natural language. Each
                                            endeavor aimed at constructing a unified mathematical li-
                                                                                                           formal statement undergoes thorough manual examination
                                            brary in Lean, is only 45MB in size. In contrast, the GPT-
                                                                                                           to ensure a faithful alignment with the original informal ver-
                                            3 training process employs the expansive CommonCrawl
                                                                                                           sion. We conduct baseline experiments with GPT-4 and re-
                                            dataset(Brown et al. 2020), which, even after filtration,
                                                                                                           port the results with case studies to further explore the prob-
                                            spans a colossal 570GB, surpassing the size of mathlib
                                                                                                           lems solving ability of current LLMs. The collective find-
                                            by over 10,000 times.
                                                                                                           ings highlight GPT-4’s limited capacity to yield satisfactory
                                           * Corresponding authors.                                        results, underlining the enduring challenge of automating
                                           1
                                               https://github.com/liuchengwucn/FIMO                        theorem proving at an IMO level.
  The contributions of this work are presented as follows:      build an AI that can win a gold medal in the IMO compe-
 • We present FIMO which contains 149 IMO-level chal-           tition in a formal-to-formal (F2F) way. Note that as a part
   lenging formal statements in Lean as well as the corre-      of the challenge, there is also a collection of solutions to
   sponding informal statements and proofs in natural lan-      IMO problems stored in mathlib, containing both the for-
   guage.                                                       mal provable statements and the formal proofs. At the time
                                                                of writing, mathlib contains 32 formal IMO problems with
 • We propose an auto-formalization process with a dy-          their solutions.
   namic interplay of human and environmental feedback.
   The significance of allowing a large language model to       MATH MATH (Hendrycks et al. 2021) is a dataset of
   refine its outcomes through provided feedback emerges        12 500 challenging competition mathematics problems, with
   as a pivotal factor influencing the performance of auto-     each problem having a step-by-step solution. These prob-
   formalization.                                               lems are drawn from mathematics competitions including
 • We evaluate GPT-4 on our dataset and conduct case stud-      AMC 10, AMC 12, AIME, etc, and they are classified into
   ies to analyze the capacity of existing approaches for       5 levels. Both the problem and the step-by-step solution are
   IMO-level problem-solving. We find that current LLMs         written in natural language and formatted using LATEX, with-
   struggle to prove IMO-level mathematical statements.         out a formal version.
                                                                MiniF2F MiniF2F (Zheng, Han, and Polu 2022) is a
           Background and Related Work                          benchmark of 488 manually formalized statements of
Formal Mathematics                                              Olympiad-type mathematical competition problems. Each
                                                                of the statements is formalized by human experts in
As mentioned in (Koutsoukou-Argyraki 2021), formal math-
                                                                three different formal languages: Lean, Isabelle, and Coq.
ematics enables computers to verify the correctness of a
                                                                MiniF2F draws from Olympiad mathematical problems
proof. Formal mathematics can also help mathematicians
                                                                (AIME, AMC, and IMO) as well as high-school and under-
gain brand new insights even in already familiar topics as
                                                                graduate math classes. Despite having 488 problems in the
well as serve educational purposes. Formal mathematics re-
                                                                whole dataset, most of them are relatively trivial to solve,
lies heavily on interactive theorem provers (also referred to
                                                                and only 40 of them are drawn from authentic IMO prob-
as proof assistants). Popular choices include Lean, Isabelle,
                                                                lems. GPT-f, a fine-tuned version of GPT, is able to solve
Coq, and HOL Light. Mathematicians can enter statements
                                                                some problems, but none of the statements extracted from
and proofs written in a formal domain-specific language
                                                                IMO problems is successfully proved, as reported in (Zheng,
(DSL), and the interactive theorem prover could check the
                                                                Han, and Polu 2022). This emphasizes the challenge of
correctness of the proofs automatically.
                                                                IMO-level mathematical reasoning.
Auto-Formalization                                                 Note that the original version of the miniF2F dataset pre-
                                                                sented by OpenAI only contains formal statements. A de-
The task of formalization is to turn informal descriptions      rived version (Jiang et al. 2022b) is also available publicly
written in natural languages (human readable LATEX code)        with the addition of an informal statement and an informal
into formally correct and automatically checkable format        proof for each problem.
(Szegedy 2020). However, there is a vast logical gap be-
tween formal language and natural language, since every         Neural Theorem Provers
simple argument should be made explicit in formal lan-
guage. Therefore, formalization is a tedious task, and per-     Provers with Formal Language GPT-f (Polu and
forming formalization manually on a large scale is very         Sutskever 2020) is an automated prover for the Metamath
expensive and time-consuming. Auto-formalization with           formalization language. GPT-f generates original mathemat-
LLMs proposed in (Wu et al. 2022), is an attempt to per-        ical terms via generation from language models, which is
form formalization utilizing the few-shot learning ability of   based on GPT-3 and fine-tuned for theorem proving. Polu
the large language models by prompting them with several        et al. (Polu et al. 2023) follow GPT-f and use expert itera-
examples of informal and formal statement pairs. In their pa-   tion to generate more training data and successfully improve
per, they dealt with the auto-formalization of theorem state-   the pass rate of language models. DT-solver (Wang et al.
ments and claimed that LLMs are able to correctly translate     2023) proposes a dynamic tree sampling strategy to guide
a significant portion (25.3%) of mathematical competition       the search procedure with state confidence and proof-level
problems perfectly to formal specifications in Isabelle/HOL.    values.
                                                                Provers with Informal Language Draft, Sketch, and
Datasets                                                        Prove (DSP) is a method aimed at using informal proofs as
Lean Mathlib Mathlib is a community-maintained Lean             guides for automated theorem proving (Jiang et al. 2022b).
mathematical library aiming to build a unified library of       DSP maps informal proofs to formal proof sketches and lets
mathematics formalized in the Lean proof assistant (mathlib     the automated provers focus on easier sub-problems. Instead
Community 2020). It is the largest collection of mathematics    of having to figure out the whole formal proof from zero to
that has been formalized in Lean and contains programming       one, DSP takes advantage of the proofs written in natural
infrastructure, mathematics, and tactics. The IMO Grand         languages that are already existed. Besides, DSP allows in-
Challenge (Selsam et al. 2020) is a proposal that aims to       formal proofs either written by humans or generated by a
language model, which further extended the application of          Combinatorics, Geometry, and Number Theory. However,
DSP on problems without existing informal proofs.                  our focus for conversion purposes is directed solely toward
                                                                   problems falling under the Algebra and Number Theory do-
                      FIMO Dataset                                 mains, along with their corresponding solutions. This selec-
Dataset Construction                                               tive approach stems from insights outlined in (Zheng, Han,
                                                                   and Polu 2022), which highlights the formidable challenge
The process of constructing the dataset can be catego-             of formalization in the Combinatorics and Geometry cate-
rized into three main stages: Optical Character Recogni-           gories due to the nascent state of formalization efforts in
tion (OCR), Auto-Formalization with Feedback, and Man-             these areas, particularly within formal systems such as Lean.
ual Verification.Each stage is outlined in detail below. An        Importantly, it’s worth noting that not all Algebra and Num-
illustrative representation of the entire pipeline is provided     ber Theory problems inherently necessitate proof-oriented
in Figure 1.                                                       solutions. For instance, a problem may ask students to give
                                                                   some examples or to answer whether a statement is true or
           Start                                                   not. We follow the method described in (Wu et al. 2022)
                                                                   to address this variability. We apply a transformation to
           OCR                                                     reframe them as proof-oriented problems. Specifically, the
                                                                   solution for each problem is converted into an associated
   Auto-Formalization                                              proof. This procedure involves appending the answer to the
                                                                   end of the problem, effectively converting it into a proposi-
                                                                   tion open to formalized proof. An illustrative instance of this
          Lean             No      Error                           conversion process is depicted in Table 1.
                                  Messages       Reflection
          Check
                                                                     Original      Find all pairs (k, n) of positive integers for
         Yes                                                         Problem       which 7k − 3n divides k 4 + n2 .
                                                                                   Find all pairs (k, n) of positive integers for
                                                                    Provable
                            No                                                     which 7k − 3n divides k 4 + n2 . The final
          Manual                   Human                            Statement
                                                                                   answer is (2, 4).
          Check                   Feedback
                                                                   Table 1: Example of converting a non-proof problem into a
         Yes                                                       provable statement.
            End

Figure 1: Flowchart for the pipeline of our auto-                  Auto-Formalization with Feedback Next, our process
formalization with feedback.                                       employs the auto-formalization methodology introduced in
                                                                   (Wu et al. 2022), leveraging the few-shot learning capa-
                                                                   bilities inherent in large language models. The few-shot
OCR The IMO Shortlisted Problems are exclusively avail-            prompts detailed in (Wu et al. 2022) are written in Isabelle
able in PDF format. To make them amenable to further               notation, which isn’t directly compatible with our dataset
processing, we employ optical character recognition (OCR)          constructed for the Lean formal language. We manually
to convert them into LATEX code. Specifically, the Mathpix         rewrite the few-shot prompts and replace each Isabelle state-
snipping tool, an image-to-LATEX converter, is utilized. This      ment with the corresponding Lean statement. An example of
tool seamlessly translates pages of equations into format-         such a rewrite is shown in Table 2. This stage of the dataset
ted LATEX code while meticulously retaining all mathemati-         construction solidifies the transition from natural language-
cal equation details. In order to avoid minor errors that could    based problem statements to formalizable propositions, in-
potentially compromise mathematical semantics, we subject          strumental in furthering our aim of enhancing automated
the generated LATEX code to manual verification. Following         theorem proving capabilities.
the completion of the aforementioned OCR procedure, we                Bridging the vast logical gap between natural languages
assemble the problems alongside their corresponding solu-          and formal languages is no easy task. Analogous to hu-
tions. In instances where multiple distinct solutions are pro-     man comprehension, large language models (LLMs) may
vided, our approach is to retain the initial solution while dis-   initially produce outputs that encompass syntactic or seman-
carding the others. Furthermore, for problems that encom-          tic inaccuracies. To ameliorate this issue, we draw inspi-
pass multiple sub-questions, we opt for simplicity by treat-       ration from the concept expounded in (Shinn et al. 2023),
ing each sub-question as an independent problem. This com-         wherein verbal reinforcement is employed to facilitate the
prehensive transformation process ensures the conversion of        LLMs’ learning from previous inadequacies. The interactive
PDF-based IMO Shortlisted Problems into a coherent and             theorem prover Lean could act as the environment and point
structured format, poised for subsequent stages of dataset         out syntax errors directly with its error messages. This or-
construction.                                                      chestration enables the direct identification of syntax errors
   The IMO Shortlisted Problems are divided by the IMO             through Lean’s error messages, considerably simplifying the
problem selection committee into 4 categories: Algebra,            process of validating syntactical correctness. Consequently,
  Natural      If 3a + b + c = −3, a + 3b + c = 9, a + b +           Logically, the aforementioned method of auto-
 Language      3c = 19, then find abc. The final answer is        formalization with feedback process is LLM-agnostic
  Version      -56                                                and any LLM with the ability of few-shot learning should
               theorem                                            be able to perform the task. Specifically, we use GPT-4 (to
                  fixes a b c :: real                             be specific, gpt-4-0314) to perform the auto-formalization
  Isabelle        assumes "3*a + b + c = -3"                      (OpenAI 2023).
  Version            and "a + 3*b + c = 9"
                     and "a + b + 3*c = 19"                       Manual Verification The training objective of GPT se-
                  shows "a * b * c = -56"                         ries models focused on maximizing the probability of the
               theorem                                            next word, which are prone to minor errors. While natural
                  (a b c : R)                                     languages are robust to such mistakes, those errors may be
   Lean           (h0 : 3*a + b + c = -3)                         extremely harmful to mathematics statements (Shen et al.
  Version         (h1 : a + 3*b + c = 9)                          2021). Mathematics statements are vulnerable to minor er-
                  (h2 : a + b + 3*c = 19) :                       rors, which often change the semantic result in the whole
                  a * b * c = -56 :=                              statement being wrong and unprovable. Hence, we introduce
                                                                  multiple manual checks to ensure the formal statements are
Table 2: Rewrite few-shot prompts for auto-formalization          semantically aligned with the informal ones. Specifically,
with Lean language manually.                                      we manually check the LATEX code generated by the OCR
                                                                  system (namely the Mathpix snipping tool) and each formal
                                                                  statement generated by the LLM that has passed the verifi-
the focus of human experts can be channeled toward iden-          cation of the proof assistant Lean, as shown in Figure 1.
tifying semantic errors, further enhancing the iterative re-
finement process. We prompt the LLM to refine its results         Statistics
several times, until it is verified by both the proof assistant
Lean and human experts or the maximum number of itera-            FIMO is a dataset of human-verified auto-formalized state-
tions (to be specific, 5) is reached. By this means, we enable    ments of IMO-level mathematical problems aligned in Lean
the LLMs to refine its result iteratively. An example of such     language, as well as the natural language version of the
refinement is shown in Table 3.                                   problems and solutions. It provides an IMO-level chal-
                                                                  lenge benchmark for mathematical reasoning in both for-
                Let X be a set of 10000 integers, none of         mal language and natural language. We follow the same
                them is divisible by 47 . Prove that there        naming convention as the miniF2F dataset. Each Problem
  Informal                                                        that has been successfully formalized is given a problem
                exists a 2007-element subset Y of X such
  Statement                                                       name “imosl_#year_#category_p#number”. For
                that a − b + c − d + e is not divisible by 47
                for any a, b, c, d, e ∈ Y .                       instance, “imosl_2007_number_theory_p6” refers
                theorem exists subset not divisible by 47 :       to the IMO Shortlisted Problems 2007 Number Theory
                ∃ (Y : finset N) (X : finset N),                  Problem 6 and “imosl_2008_algebra_p3_1” refers
                (finset.card X = 10000) ∧                         to the first sub-question of the IMO Shortlisted Problems
     First      (∀ x ∈ X, x % 47 ̸= 0) ∧                          2008 Algebra Problem 3.
     Try        (finset.card Y = 2007) ∧                             The IMO Shortlisted Problems are selected by the IMO
                (Y ⊆ X) ∧                                         problems selection committee from problems proposed by
                (∀ a b c d e ∈ Y,                                 each country, namely the long list. The IMO Shortlisted
                (a - b + c - d + e) % 47 ̸= 0) :=                 Problems are not released until the following year IMO. As
                                                                  of the time of our work, the IMO Shortlisted Problems with
  Reflective    X is the premise instead of the goal. Try
                                                                  Solutions from 2006 to 2021 are available on the IMO offi-
  Feedback      again.
                                                                  cial website2 . Each year, around 30 problems are selected by
                theorem exists subset not divisible by 47 :
                                                                  the problem selection committee of IMO, and nearly half of
                ∀ (X : finset N),
                                                                  them belong to Algebra and Number Theory categories. The
                (finset.card X = 10000) ∧
                (∀ x ∈ X, x % 47 ̸= 0) →
                                                                  total quantity of all shortlisted Algebra and Number The-
   Refined                                                        ory problems from 2006 to 2021 is 245, including 121 Al-
                ∃ (Y : finset N),
   Result                                                         gebra problems and 124 Number Theory problems (prob-
                (finset.card Y = 2007) ∧
                (Y ⊆ X) ∧                                         lems that have multiple sub-questions are treated as mul-
                (∀ a b c d e ∈ Y,                                 tiple independent problems). With auto-formalization with
                (a - b + c - d + e) % 47 ̸= 0) :=                 feedback described above, we successfully formalize over
                                                                  60% (149/245) of the problems. The statistics of the pro-
                                                                  posed FIMO dataset and the comparison with other datasets
Table 3: Refine the result with human feedback focusing on        are shown in Table 4 and Table 5.
semantic errors. The LLMs are able to understand the high-
level semantic error described in natural language and to fig-        2
                                                                        The IMO Shortlisted Problems with Solutions are available at
ure out a way to correct it.                                      https://www.imo-official.org/problems.aspx
                            Total     Success      Success                               Total       Success          Success
       Category                                                       Category
                           Quantity   Count         Rate                                Quantity     Count             Rate
       Algebra               124         89        71.8%              Algebra               124     52 (−37)    41.9% (−29.9%)
                                                                   Number Theory            121     28 (−32)    23.1% (−26.5%)
    Number Theory            121         60        49.6%
                                                                         Total              245     80 (−69)    32.6% (−28.2%)
          Total              245        149        60.8%
                                                                 Table 6: The success rate of GPT-4 auto-formalization with-
Table 4: The success rate of GPT-4 auto-formalization with       out reflective feedback.
reflective feedback. Success count refers to the number of
problems that are successfully formalized. Since problems
that have multiple sub-questions are treated as multiple in-
                                                                 The Lean Proof assistant will point out the syntax error in
dependent problems, the total quantities of problems are
                                                                 Lean language, and generate corresponding error messages.
slightly larger.
                                                                 The syntax error can be divided into 7 categories, as shown
                                                                 in Table 7.
               Problem       IMO-
  Dataset                             FS      FP    IS     IP
                Count        Level                                                                             Number
                                                                   Error Type                      Algebra                 Total
                                                                                                               Theory
  mathlib          N/A         32      ✓      ✓      –      –
  miniF2F          488         40      ✓      –     –*     –*      failed to synthesize type
                                                                                                      6           1             7
  MATH            12 500       0       –      –     ✓      ✓       class instance
    FIMO           149        149      ✓      –     ✓      ✓       type mismatch                      6          10             16

                                                                   unknown identifier                 9           8             17
Table 5: Comparison with other datasets. FS, FP, IS and IP
refer to formal statement, formal proof, informal statement,
                                                                   invalid field notation             1           0             1
and informal proof, respectively. IMO-Level refers to prob-
lems that are either authentic IMO problems or IMO Short-
                                                                   function expected                  1           1             2
listed Problems which are both selected by the problem se-
lection committee of the IMO. The asterisks mean that there
                                                                   unexpected token                   2           0             2
is a derived version that contains informal statements and in-
formal proofs, while the original version does not.                don’t know how to syn-
                                                                                                      0           4             4
                                                                   thesize placeholder
                                                                   invalid expression                 0           1             1
Dataset Analysis
Translating mathematical statements into formal language           Total                             25          25             50
manually is a tedious and time-consuming process. With the
few-shot learning ability of LLMs, we can prompt LLMs
with some examples and auto-formalize the statements.            Table 7: Statistics of the syntax error type extracted from the
However, only a little proportion (25.3%) of the statements      error messages generated by proof assistant Lean.
could be formalized successfully as reported in (Wu et al.
2022). To address this problem, we prompt the LLMs with             As shown in Table 7, the most common syntax errors
the feedback that comes from either the error messages gen-      are “type mismatch” and “unknown identifier”. These errors
erated by the proof assistant Lean or written by a human         may be due to the hallucination inside the large language
expert, as shown in Figure 1.                                    model. However, like compilers for other programming lan-
   We also report the success rate of the auto-formalization     guages, the error messages are not always very useful. For
without reflective feedback. The result shows that there will    instance, an unknown identifier may be indirectly caused by
be a significant drop in the success rate without feedback,      not importing a certain library, or by not declaring a vari-
demonstrating the effectiveness of our method. The result        able properly. We found that GPT-4 is able to figure out how
also shows that Algebra problems are generally easier to         to fix syntax errors under the guidance of high-level error
formalize than Number Theory problems. The success rate          messages in most cases.
of the auto-formalization process of Algebra problems also          We also found that instead of simply mapping natural
gains a greater boost with reflective feedback. With our         mathematics into formal mathematics, GPT-4 is able to ex-
method, GPT-4 is able to formalize a considerably larger         tract nontrivial latent semantic information. As shown in Ta-
proportion of problems (from 32.6% to 60.8%) while keep-         ble 8, the informal mathematics statement “Let a, b, c be the
ing the need for human intervention comparable.                  sides of a triangle.” indicates that a, b, c are all positive real
   In order to understand the reason why LLMs fail to for-       numbers. GPT-4 is aware of it and also notices the fact that
malize mathematical statements, we randomly sample 50            the sum of any two sides is greater than the third side. Such
auto-formalized statements that fail to pass the Lean Check.     auto-formalization requires the model to have both mathe-
matical reasoning ability and general knowledge of mathe-        of methods. Inspired by the DSP framework, we also lever-
matics.                                                          age the power of the existing informal proofs. The original
                                                                 version of the DSP framework exclusively targets the for-
               Let a, b, c be the sides of a triangle. Prove     mal language Isabelle with Sledgehammer, a proof automa-
               that                                              tion tool in Isabelle. Because it relies on Isabelle instead of
                      √                   √
                        b+c−a               c+a−b                Lean, we cannot directly apply it to our dataset. Our methods
 Informal           √     √     √ +√           √     √           are described below. We conducted error analyses of formal
 Statement            b+ c− a             c+ a− b                proofs generated by GPT-4 and analyzed possible reasons
                               √                                 for the failure of the IMO-level automated theorem proving.
                                 a+b−c
                          +√       √     √ ≤3                    We also analyzed the limitation of the FIMO dataset.
                               a+ b− c
                                                                 GPT-4 Guided by Informal Proofs
               theorem imosl_2006_algebra_p5
                 (a b c : R)                                     To guide the LLMs with informal proofs, our approach can
                 (h0 : a > 0 ∧ b > 0 ∧ c > 0)                    be divided into two phases: acquiring the informal proof and
                 (h1 : a + b > c ∧ a + c > b                     formal proof generation.
                 ∧ b + c > a) :                                     The first phase is to find informal proofs for a given prob-
                 (real.sqrt (b + c - a) /                        lem. In common scenarios, solutions to the Olympiad math-
                 (real.sqrt b + real.sqrt c                      ematical problems are available, as in our dataset. But some-
                 - real.sqrt a)) +                               times they can be missing or not suitable for formal expres-
  Formal                                                         sion. Therefore, we conduct experiments in two different
                 (real.sqrt (c + a - b) /
 Statement                                                       setups: with or without human informal proof. In the for-
                 (real.sqrt c + real.sqrt a
                 - real.sqrt b)) +                               mer setup, the informal proofs are written by a human. In
                 (real.sqrt (a + b - c) /                        the FIMO dataset, the informal proofs are extracted from
                 (real.sqrt a + real.sqrt b                      the solutions provided by the problem selection commit-
                 - real.sqrt c)) 3 :=                            tee of IMO. We treat the solution provided as a “ground-
               begin                                             truth” informal proof. Hopefully, the manually-written in-
                 sorry                                           formal proof would act as a guide for the process of formal
               end                                               proof generation. In the latter setup, the informal proofs are
                                                                 generated directly by a language model. We also use GPT-
                                                                 4 for the generation of informal proofs. We regenerate the
Table 8: Instead of simply mapping natural mathematics into      informal proof every time we generate the formal proof.
formal mathematics, LLMs can extract latent semantic infor-         The second phase of our approach is to write formally ver-
mation. The original problem is the IMO Shortlisted Prob-        ifiable proofs. We prompt the language model with formal
lems 2006 Algebra Problem 5.                                     and informal statements, as well as informal proof acquired
                                                                 in the former phase. In such a way, the language model
                                                                 could obtain the proof ideas from the informal proofs and
            Experiments and Discussion                           use them to guide the process of formal proof generation.
In this section, in order to understand the performance of ex-   Our approach enjoys both the logical rigor provided by for-
isting LLMs, we conducted baseline experiments using the         mal systems and the flexibility of informal proofs. The ex-
cutting-edge GPT-4 (to be specific, gpt-4-0314) as our base-     periment’s result shows that our approach can achieve com-
line model. Current methods of automated theorem prov-           petitive results on the miniF2F benchmark, without sophis-
ing with LLMs can be divided into two classes in accor-          ticated search algorithms or further fine-tuning of LLMs.
dance with the usage of data. The first class of methods only
uses formal data in the process of the stage of model fine-      Result
tuning and inference. Well-known methods include PACT            We report the pass rate of GPT-4 guided by informal proofs
(Han et al. 2022) and Thor (Jiang et al. 2022a). PACT ex-        on our dataset and both the test set and the validation set of
tracts self-supervised data from formal proof terms for train-   the benchmark miniF2F. The results are reported in Table 9.
ing. Thor leverages the power of automated theorem provers       Pass rates are reported as Pass@N where N is the number of
instead of language models for premise selection. On the         attempts for generating the whole proof.
other hand, the second class of methods leverages both for-         GPT-4 achieved a Pass@8 of over 20% on miniF2F.
mal data and informal data and has potential to achieve bet-     Nonetheless, GPT-4 failed to prove any of the statements in
ter performance. These methods include GPT-f and DSP.            the FIMO dataset as expected, showing the difficulty of the
GPT-f uses the WebMath dataset, a mixture of formal data         IMO-level problem theorem proving. We also find that the
and informal data, in their pre-training process. The source     GPT-4 without using human informal proofs achieves better
of data involved in the WebMath dataset includes GitHub,         Pass@8. This phenomenon can be attributed to the increased
arXiv Math, and Math StackExchange. In the DSP, the for-         diversity and ability to explore various directions exhibited
mal proofs are generated under the guidance of the existing      in informal proofs generated by language models.
informal proofs. Since the FIMO dataset proposed contains           The results show that while GPT-4 is able to solve some
both formal data and informal data, it supports both classes     problems in the miniF2F dataset, it cannot solve any prob-
                                          miniF2F-valid                    miniF2F-test                    FIMO
                Method
                                     Pass@1 Pass@8 Length            Pass@1 Pass@8 Length             Pass@1 Pass@8
       GPT-4 w/ Human Proof           11.5%      16.0%      11.1      8.6%       14.3%       11.8      0.0%       0.0%
       GPT-4 w/o Human Proof          9.4%       21.3%      11.2      9.0%       20.9%       11.4      0.0%       0.0%

Table 9: Baseline performance of GPT-4 with/without human informal proofs. Pass rates are reported as Pass@N, where N is
the number of attempts for generating proofs. The length refers to the average number of lines of the generated proof.


lem in the FIMO dataset. We believe that this is because           an example emphasizing this kind of failure. The model
statements in our dataset are more difficult to prove and re-      managed to divide the whole problem into several sub-goals
quire advanced mathematical reasoning skills. In the follow-       according to the solution provided and explain the motiva-
ing section, we analyze the reason why GPT-4 fails in detail.      tion of each step in the comments. For instance, the formal
                                                                   proof generated defines a, b, c as in the informal solution,
Error Analysis                                                     and tries to show a2 + b2 + c2 ≥ 1. Unfortunately, the for-
We found that most of the informal proofs synthesized by the       mal proof fails to apply the tactic rw properly, as indicated
language model are mathematically incorrect. Therefore, the        by the red underline in the example. We also observed that
LLMs may be misled when generating formal proofs.                  although there are some errors, GPT-4 is able to generate
                                                                   much longer formal proofs (with an average length of over
                                                                   11) with the guidance of informal proofs. In contrast, the av-
                                                                   erage proof length is less than 3 for GPT-f on the miniF2F
                                                                   dataset as reported in (Zheng, Han, and Polu 2022).

                                                                                          Limitation
                                                                   Like manually formalized miniF2F, Combinatorics and Ge-
                                                                   ometry problems are not covered by the proposed FIMO
                                                                   dataset since they are less expressible in formal systems like
                                                                   Lean. The shift of the distribution of problem type may af-
                                                                   fect the evaluation of the reasoning ability of the models
                                                                   when the FIMO dataset serves as a metric. The dataset cov-
                                                                   ers the IMO Shortlisted Problems with Solutions only from
                                                                   2006 to 2021, which are publicly available on the official
                                                                   IMO website. At the time of writing, problems before 2006
                                                                   that can be acquired through other channels are not included.
                                                                   All of the formal statements are formalized automatically
                                                                   and checked by humans. Despite our best efforts, there may
                                                                   still be a very small number of errors.

                                                                                          Conclusion
                                                                   We presented FIMO, a dataset of formal IMO-level math-
                                                                   ematics problem statements, alongside informal statements
                                                                   and informal proofs in LATEX. This effort aims to enhance
                                                                   neural mathematical reasoning by bridging natural and for-
                                                                   mal languages. Through auto-formalization with feedback,
                                                                   we highlighted the significance of reflective feedback in im-
                                                                   proving the auto-formalization process. Employing GPT-4
                                                                   guided by informal proofs as our baseline model, we find
                                                                   that GPT-4 falls short of formally proving any statements
                                                                   in the dataset. This outcome emphasizes the enduring chal-
                                                                   lenge of achieving IMO-level automated theorem proving.
Figure 2: Informal solution provided and formal proof gen-         Our contribution, FIMO, along with our methodology and
erated. The original problem is the first sub-question of the      findings, enriches the landscape of neural mathematical rea-
IMO Shortlisted Problems 2008 Algebra Problem 2.                   soning. While current capabilities have limitations, they un-
                                                                   derscore the need for continued innovation and research to
   For GPT-4 with the guidance of human proofs, we ob-             advance the realm of AI-powered mathematical formaliza-
served that the language model is able to follow the solution      tion, thereby narrowing the gap between human expertise
provided, but fails to apply tactics properly. Figure 2 shows      and machine capabilities.
                        References                                Shinn, N.; Cassano, F.; Labash, B.; Gopinath, A.;
                                                                  Narasimhan, K.; and Yao, S. 2023.            Reflexion: Lan-
Brown, T.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J. D.;
                                                                  guage Agents with Verbal Reinforcement Learning.
Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell,
                                                                  arXiv:2303.11366.
A.; Agarwal, S.; Herbert-Voss, A.; Krueger, G.; Henighan,
T.; Child, R.; Ramesh, A.; Ziegler, D.; Wu, J.; Winter,           Szegedy, C. 2020. A Promising Path Towards Autoformal-
C.; Hesse, C.; Chen, M.; Sigler, E.; Litwin, M.; Gray, S.;        ization and General Artificial Intelligence. In Benzmüller,
Chess, B.; Clark, J.; Berner, C.; McCandlish, S.; Radford,        C.; and Miller, B., eds., Intelligent Computer Mathematics,
A.; Sutskever, I.; and Amodei, D. 2020. Language Mod-             3–20. Cham: Springer International Publishing. ISBN 978-
els are Few-Shot Learners. In Larochelle, H.; Ranzato, M.;        3-030-53518-6.
Hadsell, R.; Balcan, M.; and Lin, H., eds., Advances in Neu-      Wang, H.; Yuan, Y.; Liu, Z.; Shen, J.; Yin, Y.; Xiong, J.;
ral Information Processing Systems, volume 33, 1877–1901.         Xie, E.; Shi, H.; Li, Y.; Li, L.; Yin, J.; Li, Z.; and Liang,
Curran Associates, Inc.                                           X. 2023. DT-Solver: Automated Theorem Proving with
Han, J. M.; Rute, J.; Wu, Y.; Ayers, E. W.; and Polu, S. 2022.    Dynamic-Tree Sampling Guided by Proof-level Value Func-
Proof Artifact Co-training for Theorem Proving with Lan-          tion. In Proceedings of the 61st Annual Meeting of the As-
guage Models. arXiv:2102.06203.                                   sociation for Computational Linguistics (Volume 1: Long
                                                                  Papers), 12632–12646. Toronto, Canada: Association for
Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart,        Computational Linguistics.
S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measur-          Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M. N.; Staats, C.; Jamnik,
ing Mathematical Problem Solving With the MATH Dataset.           M.; and Szegedy, C. 2022. Autoformalization with Large
NeurIPS.                                                          Language Models. arXiv:2205.12615.
Jiang, A.; Czechowski, K.; Jamnik, M.; Milos, P.;                 Zheng, K.; Han, J. M.; and Polu, S. 2022. MiniF2F: a cross-
Tworkowski, S.; Li, W.; and Wu, Y. T. 2022a. Thor: Wield-         system benchmark for formal Olympiad-level mathematics.
ing Hammers to Integrate Language Models and Automated            arXiv:2109.00110.
Theorem Provers. In NeurIPS.
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Li, W.; Liu, J.; Jam-
nik, M.; Lacroix, T.; Wu, Y.; and Lample, G. 2022b. Draft,
Sketch, and Prove: Guiding Formal Theorem Provers with
Informal Proofs. In Submitted to The Eleventh International
Conference on Learning Representations.
Koutsoukou-Argyraki, A. 2021. Formalising Mathemat-
ics – in Praxis; A Mathematician’s First Experiences with
Isabelle/HOL and the Why and How of Getting Started.
Jahresbericht der Deutschen Mathematiker-Vereinigung,
123(1): 3–26.
mathlib Community, T. 2020. The Lean Mathematical Li-
brary. In Proceedings of the 9th ACM SIGPLAN Interna-
tional Conference on Certified Programs and Proofs, CPP
2020, 367–381. New York, NY, USA: Association for Com-
puting Machinery. ISBN 9781450370974.
OpenAI. 2023. GPT-4 Technical Report. arXiv:2303.08774.
Polu, S.; Han, J. M.; Zheng, K.; Baksys, M.; Babuschkin, I.;
and Sutskever, I. 2023. Formal Mathematics Statement Cur-
riculum Learning. In The Eleventh International Conference
on Learning Representations, ICLR 2023, Kigali, Rwanda,
May 1-5, 2023. OpenReview.net.
Polu, S.; and Sutskever, I. 2020. Generative Language Mod-
eling for Automated Theorem Proving. arXiv:2009.03393.
Selsam, D.; Buzzard, K.; Barton, R.; Liang, P.; Loss, S.; and
Wiedijk, F. 2020. IMO Grand Challenge.
Shen, J.; Yin, Y.; Li, L.; Shang, L.; Jiang, X.; Zhang, M.; and
Liu, Q. 2021. Generate & Rank: A Multi-task Framework
for Math Word Problems. In Findings of the Association
for Computational Linguistics: EMNLP 2021, 2269–2279.
Punta Cana, Dominican Republic: Association for Compu-
tational Linguistics.
