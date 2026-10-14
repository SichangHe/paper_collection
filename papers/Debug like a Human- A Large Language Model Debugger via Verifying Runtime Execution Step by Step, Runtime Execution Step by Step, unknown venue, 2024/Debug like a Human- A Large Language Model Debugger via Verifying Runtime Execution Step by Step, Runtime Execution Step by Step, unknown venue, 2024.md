                                            Debug like a Human: A Large Language Model Debugger via Verifying
                                                             Runtime Execution Step by Step

                                                                          Li Zhong Zilong Wang† Jingbo Shang†
                                                                             University of California, San Diego
                                                                          {lizhong, zlwang, jshang}@ucsd.edu



                                                                  Abstract                                   Existing works: Post-Execution Information
                                                                                                              Test Case 1 Pass        Test Case 2       Error
                                             Large language models (LLMs) are leading sig-                    Test Case 3 Fail              …
                                             nificant progress in code generation. Beyond
                                                                                                 Generated
                                             one-pass code generation, recent works further      Program     LDB (ours): Runtime Execution Information
arXiv:2402.16906v6 [cs.SE] 6 Jun 2024




                                             integrate unit tests and program verifiers into                                                                           Debugging
                                                                                                                  1                                Task Desc.          w/ LLMs
                                             LLMs to iteratively refine the generated pro-                                                       Verify Step by Step
                                                                                                  Visible             2
                                             grams. However, these works consider the gen-       Test Case                                      v1=…, v2=…
                                             erated program as an indivisible entity, which                               3                     v2=…, v3=…
                                                                                                                  Control     Breakpoints         Runtime
                                             falls short for LLMs in debugging the programs,                    Flow Graph    in Program           States
                                             especially when the programs contain complex
                                             logic flows and data operations. In contrast,
                                             when human developers debug programs, they         Figure 1: Comparison of LDB and existing debugging
                                             typically set breakpoints and selectively exam-    works. Existing works treat the programs as an indivis-
                                             ine runtime execution information. The execu-      ible entity and depend on the post-execution feedback
                                             tion flow and the intermediate variables play a    for debugging, while LDB leverages the runtime exe-
                                             crucial role in the debugging process, yet they    cution information, tracking the values of intermediate
                                             are underutilized in the existing literature on    variables and verifying basic blocks against the task de-
                                             code generation. In this study, we introduce       scription step by step.
                                             Large Language Model Debugger (LDB), a
                                             novel debugging framework that enables LLMs
                                             to refine their generated programs with the run-   tion (Li et al., 2018; Raychev et al., 2014). Re-
                                             time execution information. Specifically, LDB      cent progress in large language models (LLMs) (Li
                                             segments programs into basic blocks and tracks     et al., 2023; Roziere et al., 2023; Achiam et al.,
                                             the values of intermediate variables after each    2023; Zhou et al., 2023a; Muennighoff et al., 2023)
                                             block throughout runtime execution. This al-
                                                                                                significantly boosts the performance of code gen-
                                             lows LLMs to concentrate on simpler code
                                             units within the overall execution flow, verify
                                                                                                eration and demonstrates a promising potential to
                                             their correctness against the task description     be generally applied in different requirements and
                                             block by block, and effectively pinpoint any       tasks (Shinn et al., 2023; Gu, 2023; Yuan et al.,
                                             potential errors. Experiments demonstrate that     2023). However, generating correct programs is
                                             LDB consistently enhances the baseline perfor-     not a one-time effort. Existing works suggest en-
                                             mance by up to 9.8% across the HumanEval,          hancing code generation through multiple sam-
                                             MBPP, and TransCoder benchmarks, archiv-           pling (Zhang et al., 2023b; Shinn et al., 2023), self-
                                             ing new state-of-the-art performance in code
                                                                                                consistency (Le et al., 2023; Huang et al., 2023a;
                                             debugging for various LLM selections.
                                                                                                Chen et al., 2022), and candidates ranking (Shi
                                                                                                et al., 2022; Ni et al., 2023; Zhang et al., 2023a).
                                        1    Introduction                                       Despite these advanced approaches, they still fall
                                                                                                short on basic programming questions from the Hu-
                                        Code generation is a critical yet challenging task
                                                                                                manEval and MBPP datasets. This underscores the
                                        that has various downstream applications, such
                                                                                                limitations of single-pass program generation.
                                        as text-to-code generation (Chen et al., 2021; Yin
                                                                                                   Recognizing this, a series of works have been
                                        and Neubig, 2017; Li et al., 2022), code transla-
                                                                                                proposed to refine the programs generated in a sin-
                                        tion (Roziere et al., 2020), and code autocomple-
                                                                                                gle pass, based on feedback from either human
                                             †
                                                 Corresponding authors.                         annotator (Chen et al., 2023a; Wu et al., 2023) or
                                                                                        Step 0
        Step 1                   Generated Program                                                                 Task Description                     Step 4
                                                                                     Generate seed
    (Profiling § 2.2)          def func(s):
                                                                                  programs w/ a LLM                                               (Regeneration § 2.4)
                                 cnt = 0                                                                          Count the number
       Run static                                                                                                                               Refine the program based
       analysis to
                                 if s != '':                                                                      of characters in a             on the task description
                                   for c in s: cnt += 2
       build CFG                 return cnt
                                                                                                                  string.                        and debugger response


  Control Flow Graph                         Visible        "LLM"                     Intermediate States                    Task          Debugger Response
  Ⓐ~Ⓓ are control blocks                     Test Cases                                                                      Description
  of the program                         input: "LLM"                             A      …                               Count the          A
                                                                                                                                                          This block is
                        A  cnt=0
                                         → output: 3                                                                     number of…
                                                                                                                                                          correct because…




                                                            Execution Trace
                                                                                       Before B, cnt=0
                         if s!='':                                                B    After B, cnt=0;c='L'                                 B
        B                                                                                                                                                 This block should
            for c in s
                                                                                       Before C, cnt=0;c='L'                                              add 1 to cnt
                                                                                  C    After C, cnt=2;c='L'
                                                                                                                                            C             instead of 2 when
                                                                                                                                                          encountering a
                                           Step 2                                 …         Variable Values
                                                                                                                           Step 3           …             new character in s
    C                                  (Profiling § 2.2)
                                                                                        Before/After Each Block
                                                                                                                      (Debugging § 2.3)
        cnt+=2                                                                                                                                             Verdicts and
                        D   return     Input visible test                         D      …                              Query LLMs to       D              Explanation
                                       cases & acquire                                                                 verify each block
                             cnt
                                        execution trace                       6                                        based on the task


Figure 2: Illustration of the debugging workflow of LDB. A code generator is prompted to generate the seed
programs (Step 0). Profiling (§ 2.2): LDB decomposes the seed program into basic blocks based on the control
flow graph (Step 1), and feeds in a failed visible test case to acquire the execution trace (Step 2). Debugging (§ 2.3):
LDB further inspects the runtime states of variables after each basic block during the runtime execution. Gathering
the runtime execution information, LDB queries a LLM for verdicts on the correctness of the blocks in the relation
to the task description (Step 3). Regeneration (§ 2.4): Finally, the LLM regenerates a refined program with the
debugging feedbacks by LDB (Step 4).


LLMs themselves (Tang et al., 2023; Chen et al.,                                                 basic blocks1 based on the control flow graph1 .
2023c). This refinement process is akin to debug-                                                LDB tracks the intermediate variables at the end of
ging in programming practices by human develop-                                                  each basic block, similar to the breakpoints set by
ers. Chen et al. (2023c); Jiang et al. (2023) intro-                                             developers. After gathering runtime execution in-
duce unit test results and error messages to LLMs.                                               formation, LDB queries LLMs for verdicts on each
These approaches allow LLMs to reflect on po-                                                    code block’s correctness and explanations of the
tential mistakes and generate corrected programs.                                                execution flow in relation to the coding task. This
Nevertheless, considering the debugging process                                                  approach allows language models to concentrate
by human developers, it is sub-optimal to solely de-                                             on simpler code units, verify intermediate states
pend on these post-execution information to debug                                                against the task description, and pinpoint potential
the program, especially in cases involving complex                                               bugs. Consequently, it effectively debugs the pro-
data structures and control flows. In fact, when hu-                                             gram and improves the quality of code generation.
man developers encounter a buggy program, they                                                      We validate LDB on three code generation
do more than just collect the program’s outputs.                                                 benchmarks, including HumanEval (Chen et al.,
They delve into the runtime execution to observe                                                 2021) and MBPP (Austin et al., 2021) for text-
the execution traces1 and examine the intermediate                                               to-code generation, and TransCoder (Roziere
variables by setting breakpoints. When the interme-                                              et al., 2020) for code translation. We conduct
diate execution states deviate from their intention,                                             experiments using the proprietary model, GPT-
developers pinpoint the bugs and make the correc-                                                3.5 (Achiam et al., 2023), and the open-sourced
tions. This is a common workflow for well-known                                                  models, StarCoder (Li et al., 2023) and CodeL-
interactive debuggers such as GDB (Stallman et al.,                                              lama (Roziere et al., 2023). Experiments demon-
1988) and PDB (Foundation, 2001).                                                                strate that LDB consistently improves code genera-
   To this end, we propose LDB, a large language                                                 tion accuracy across various LLM backbones and
model debugger that refines programs generated                                                   achieves state-of-the-art performance in debugging
by LLMs using runtime execution information, em-                                                 programs. Worth mentioning, even with the pro-
ulating the debugging practices of human devel-                                                  grams generated by more powerful code generators,
opers. As shown in Figure 1, feeding in a visible                                                such as GPT-4 (Achiam et al., 2023) and Reflex-
test case, LDB segments the execution trace into                                                 ion (Shinn et al., 2023), LDB can still detect errors
    1
      Refer to Appendix B for detailed introduction of execu-                                    overlooked by previous advanced methods, thereby
tion trace, control flow graph, and basic block.                                                 enhancing the capabilities of code generation even
further. We summarize our contribution as follows:      Considering the block-wise runtime execution and
• We propose a large language model debugger,           the task description, LDB queries the LLM again
  LDB, which takes the very first step on incorpo-      to detect buggy blocks and regenerate the program.
  rating runtime execution information into LLMs        LDB repeats these three steps iteratively until the
  to debug generated programs.                          new solution pass all the visible tests, or the maxi-
• We leverage basic blocks in the execution traces      mum debugging iteration is reached (Section 2.4).
  to properly segment the programs into smaller,
  simpler code units, allowing LLMs to verify them      2.2   Profiling
  step by step against users’ intention and effec-      In the step of profiling, LDB collects the runtime
  tively pinpoint the potential bugs.                   execution information when running the generated
• Extensive experiments on three code genera-           program over the failed visible test cases. It collects
  tion benchmarks demonstrate the effectiveness         the execution trace and then segments the trace into
  of LDB in debugging generated programs across         basic blocks to inspect intermediate variables.
  different LLM backbones.
Reproducibility. The code will be released on           Execution Traces. In static analysis, each pro-
Github2 .                                               gram corresponds to a unique control flow graph
                                                        (CFG) where each node in the graph is a code basic
2       Large Language Model Debugger                   block, as shown in Figure 2. Each basic block is a
                                                        straight-line sequence of code with only one entry
Problem Formulation. We follow the problem              point and one exit. The CFG represents all paths
formulation of program debugging in Chen et al.         might be traversed through a program during its
(2023c). In a code generation task, each sample         execution. After LDB feeding in a visible test case,
can be represented as a triplet (Q, Tv , Th ), where    the control flow goes through a sequence of basic
Q represents the task description, Tv and Th are        blocks and the path is denoted as the execution
visible and hidden test cases. In the text-to-code      trace, [B1 , B2 , . . . , Bn ], where Bi is a basic block
generation task, Q consists of a brief paragraph in     in the trace and n is the length of the trace.
natural language that outlines the intended goal of
the task. In the code translation task, Q represents    Intermediate States. Given an execution trace
a program written in a language other than the tar-     [B1 , B2 , B3 , . . . , Bn ], we execute the first i blocks
get language, and the objective is to translate this    and collect all the variables in the scope along with
program into the target language. A code generator      their runtime values.    S We denote the state set as
is first provided with Q and Tv to generate the seed    Vi = {v = v̂|v ∈ B≤i }, where v is a variable
program A0 . In the debugging stage, a debugger         used in the first i blocks and v̂ is its runtime value
further refines A0 and finally outputs a new pro-       after the i-th block. We define the intermediate
gram A∗ . A∗ will be tested using the hidden tests      state after the first i blocks as (Vi−1 , Bi , Vi ), where
Th to evaluate whether it is correct or not. Th is      Vi−1 represents the entry states of the block, Bi is
only used in the evaluation stage and not visible       the current code block to execute, and Vi provides
during the code generation or debugging stages.         the actual execution results after Bi .

2.1      Overview                                       2.3   Debugging
We show the workflow of LDB in Figure 2. We             The block-wise intermediate states determined by
prompt a LLM to generate seed programs. This            profiling provide a comprehensive illustration for
serves as the starting point of debugging if they       the runtime execution. In Debugging, we integrate
fail any of the visible test cases. During debug-       the intermediate states into prompts and query a
ging, LDB feeds in the failed visible test case to      LLM to verify whether the basic blocks align with
the seed program and collects the runtime execu-        the intended semantics in the task description Q.
tion information, including the execution trace and
                                                        Debugging Verdicts. For each intermediate state
the runtime variable values after each basic block
                                                        throughout the trace, (Vi−1 , Bi , Vi ), the LLM is
(Section 2.2). Then, LDB queries a LLM to verify
                                                        acquired to make a verdict on its correctness Di ∈
the correctness of basic blocks step by step via com-
                                                        {True, False}, and elaborate the explanation Ei .
paring them with the task description (Section 2.3).
                                                        If the LLM detects any buggy code block, LDB
    2
        https://github.com/FloridSleeves/LLMDebugger    includes the message in the debugging response.
Selective Debugging. Loops and recursion are              MBPP (Austin et al., 2021). HumanEval and
common in programming, potentially leading to ex-         MBPP are for text-to-code generation, where
tensive execution traces. If we include the lengthy       the task description is a brief passage outlines
traces directly in the prompt, it is highly likely to     the intended functionality of the program to be
exceed the maximum token limit of LLMs. This              generated. TransCoder is for code translation
is similar to what occurs with humans in program          which requires to translate a program from C++
development. When the execution is lengthy, devel-        into Python. The task description of TransCoder
opers may only examine a few blocks and skip the          consists of a C++ program to be translated. We
other long and tedious execution traces when de-          compute Pass@1 accuracy with hidden test cases
tecting bugs. Inspired by the human practice, LDB         for assesment. We conduct experiments with the
selectively samples Nb blocks from program traces         proprietary LLM, GPT-3.5 (turbo-0613) (Achiam
to ensure the total length of runtime information         et al., 2023), and the open-source LLMs, CodeL-
within the max token limit of LLMs.                       lama (34B-Instruct) (Roziere et al., 2023) and
                                                          StarCoder (∼15B) (Li et al., 2023) as backbones.
Batch Debugging In our proposed LDB, the in-
termediate states following each basic block are de-      3.1   Experiment Setup
termined during the execution of the seed program
with test cases. Thus, LDB can batch these states         We generate the seed programs following the same
together and query the LLM for debugging verdicts.        prompts and generation parameters used in our
This significantly improves the token efficiency of       compared method Chen et al. (2023c). We set
LDB and alleviates the pitfall of repeatedly sending      the maximum number of debugging iterations as
lengthy context to LLMs in iterative refinement (Ge       10. More detailed implementation details are re-
et al., 2023; Hu et al., 2023). Specifically, the batch   ported in Appendix C. To obtain visible test cases
debugging query process is as follows,                    for HumanEval, we extract the given visible test
                                                          cases from the task description. For MBPP, we
            {V0 , B1 , V1 , B2 , ..., Bn , Vn }           use the first test case of each problem as the visi-
           LLM                                            ble test case and use the rest as hidden test cases.
          −−−→{(D1 , E1 ), ..., (Dn , En )}               For TransCoder, we include all test cases from the
                                                          dataset as visible test cases3 . The experiment set-
where Vi is the set of variables and their runtime
                                                          tings on MBPP and TransCoder are the same as the
values after the i-th blocks, Bi is the i-th block
                                                          prior works (Chen et al., 2023c; Shi et al., 2022;
in the trace, Di is the debugging verdict from the
                                                          Ni et al., 2023). After finalizing the code solution,
LLM, and Ei is the corresponding explanation.
                                                          we compute the Pass@1 accuracy with hidden test
2.4    Regeneration                                       cases to evaluate the performance.
The runtime execution information helps accurately
                                                          3.2   Compared Methods
localize buggy code blocks, allowing LLMs to con-
centrate specifically on these areas during the re-       We evaluate the seed programs and label the perfor-
generation process. In Regeneration, LDB collects         mance as Baseline (w/o debugger). We compare
the debugging verdicts D and explanations E, and          LDB against two rubber duck debugging meth-
incorporate them along with the task description Q        ods from Chen et al. (2023c): Self-Debugging
into the prompt. Then, LDB queries the LLM again          (+Expl.) which prompts LLMs to explain gener-
to generate the refined program. LDB iteratively          ated programs line-by-line as feedback, and Self-
runs Profiling, Debugging, and Regeneration, until        Debugging (+Trace) which prompts LLMs to dry
the refined program passes all visible test cases, or     run generated programs as feedback.
the maximum debugging iteration is reached. We               We reproduce the Self-Debugging methods fol-
test the finalized solution A∗ using the hidden test      lowing the instructions in Chen et al. (2023c) due
cases Th to evaluate the performance.                     to the unavailability of open-source code. When
                                                          referring to “Self-Debugging”, we default to the
3     Experiments                                         method with higher accuracy among the two meth-
We evaluate LDB on three code genera-                     ods unless otherwise specified. Throughout the
tion benchmarks: HumanEval (Chen et al.,                    3
                                                              All test cases can be generated by running the original
2021), TransCoder (Roziere et al., 2020), and             C++ programs, which are visible to LLMs.
                                                                                  Dataset

  Model (# Param.)      Debugger                             HumanEval         TransCoder                  MBPP
                                                             Acc. ↑   ∆↑      Acc. ↑        ∆↑      Acc. ↑      ∆↑
                        Baseline (w/o debugger)               73.8             82.3                  67.6
                        SD (+Expl.) (Chen et al., 2023c)      81.1    +7.3     85.9         +3.6     74.4       +6.8
  GPT-3.5 (≥175B† )     SD (+Trace) (Chen et al., 2023c)      80.5    +6.7     86.1         +3.8     72.6       +5.0
                        LDB (ours)                            82.9    +9.1     87.7         +5.4     76.0       +8.4
                        Baseline (w/o debugger)               49.4             69.8                  51.2
                        SD (+Expl.) (Chen et al., 2023c)      53.0    +3.6     79.4         +9.6     55.6       +4.4
  CodeLlama (34B)       SD (+Trace) (Chen et al., 2023c)      54.3    +4.9     76.4         +6.6     57.2       +6.0
                        LDB (ours)                            55.5    +6.1     79.6         +9.8     57.4       +6.2
                        Baseline (w/o debugger)               39.0             61.8                  51.6
                        SD (+Expl.) (Chen et al., 2023c)      38.4    -0.6     68.9         +7.1     54.4       +2.8
  StarCoder (15B)       SD (+Trace) (Chen et al., 2023c)      39.0    +0.0     65.7         +3.9     54.8       +3.2
                        LDB (ours)                            39.6    +0.6     69.8         +8.0     55.4       +3.8

Table 1: Results of LDB and Self-Debugging (Chen et al., 2023c) (denoted as SD) on HumanEval, TransCoder,
and MBPP with GPT-3.5, CodeLlama, and StarCoder. Accuracy is calculated based on Pass@1. The improvement
(denoted as ∆) is measured against the baseline (w/o debugger). † We assume the parameter number in GPT-3.5 is
larger than that of GPT-3 (175B).


evaluation process, we ensure that all debugging                                        Code Generator
methods utilize the same LLM settings, visible test          Debugger
                                                                              GPT-3.5        GPT-4         Reflexion
cases, seed programs, and prompts formats. This
                                                             (w/o debugger)   73.8           87.2          91.5
ensures a fair comparison and eliminates potential           SD (GPT-3.5)     81.1 (+7.3)    88.4 (+1.2)   92.1 (+0.6)
disruptions caused by changes in prompt formats.             LDB (GPT-3.5)    82.9 (+9.1)    89.6 (+2.4)   95.1 (+3.6)

3.3   Main Results                                         Table 2: Results of LDB and Self-Debugging (denoted
                                                           as SD) on HumanEval with seed programs from GPT-
We compare LDB with the baseline debugging
                                                           3.5, GPT-4, and Reflexion. We use GPT-3.5 as the
methods on HumanEval, TransCoder, and MBPP,                debugging backbone. LDB can detect the subtle bugs
and present the result in Table 1. We observe that         overlooked by the powerful code generation method and
LDB consistently achieves improvements of up to            improve the performance even further.
9.8% on all datasets across different LLM back-
bones. Specifically, compared to Self-Debugging
which prompts LLMs to dry run or explain the
                                                           misguide the program debugging and refinement,
program, LDB achieves higher and more stable
                                                           which explains why Self-Debugging (+Expl.) and
performance gain over the baseline by introducing
                                                           Self-Debugging (+Trace) fail to improve the seed
the actual runtime execution information.
                                                           programs on HumanEval with StarCoder. On the
   We attribute the advantage of LDB to the fine-
                                                           contrary, LDB generates the debugging verdicts
grained debugging feedback and the runtime infor-
                                                           and explanations based on accurate intermediate
mation as external supplements to the LLM self-
                                                           values and execution flows, guiding the generated
correction. The detailed block-level debugging
                                                           programs towards the correct answer.
responses help LLMs concentrate on the buggy
areas in the program to better align the program             Worth mentioning, the visible test cases are also
with the task description. Moreover, as pointed            provided to the LLM during the initial seed pro-
out by Huang et al. (2023c), LLMs has limited              gram generation. However, their utility in code
self-correct reasoning abilities. Particularly in code     generation is limited, as evidenced by the sub-
generation, LLMs are prone to mistakes when re-            optimal performance of Baseline (w/o debugger).
flecting on program execution. This is due to their        This aligns with our assumption that actual runtime
inability to accurately calculate concrete variable        execution information significantly helps LLMs
values and predicting execution flow at branches or        ground their reasoning, thereby improving their
loops. The inaccurate feedback from LLMs could             ability to generate better semantically aligned code.
3.4    Results on Advanced Code Generators                                        LDB (ours)                        SD (+Expl.) (Chen et al., 2023c)
                                                                                  Repeated Sampling                 SD (+Trace) (Chen et al., 2023c)
To further demonstrate the effectiveness of LDB,                                                                                                   82.9
we apply LDB and Self-Debugging to debug                                         82                                               82.3 82.3 82.3
                                                                                                                      81.7 81.7




                                                        HumanEval Accuracy (%)
the seed programs from advanced code genera-                                                    81.1 81.1 81.1 81.1 81.1 81.1 81.1 81.1 81.1
                                                                                 80                         80.5                          80.5
tors, GPT-4 (Achiam et al., 2023) and Reflex-                                                     79.9 79.9 79.9 79.9 79.9 79.9 79.9 79.9
                                                                                            79.3       79.3
ion (Shinn et al., 2023). We conduct the analysis                                         78.7
                                                                                 78
on HumanEval as an example. We query GPT-
                                                                                                    76.8
4 (1106-preview) to generate seed programs in                                    76                                               76.2 76.2 76.2 76.2
                                                                                                           75.6 75.6 75.6 75.6
the same setting introduced in Section 3.1. As for                                           75.0 75.0
Reflexion, we utilize the corresponding generated                                74          74.4
                                                                                      73.8
programs published in the official Github reposi-
                                                                                      0             2           4           6          8           10
tory4 as the seed programs. GPT-4 and Reflexion                                                               # Iterations
are considered as more powerful code generators
                                                      Figure 3: Performance at each debugging iteration on
that already achieve superior performance without
                                                      HumanEval with LDB, Repeated Sampling, and Self-
any debuggers.                                        Debugging using GPT-3.5 as the backbone. SD stands
   The results are shown in Table 3. The LLM          for Self-Debugging. LDB exhibits a continuing growth
backbone of Self-Debugging and LDB is GPT-            potential with the increasing iterations and achieves the
3.5 (turbo-0613), which is weaker than the code       best performance in debugging after 10 iterations.
generators, GPT-4 and Reflexion. We list the per-
formance of GPT-3.5 in the table for reference.
                                                      Continuous Debugging Potential of LDB In
Despite the weaker LLM backbone, both Self-
                                                      Figure 3, with increasing debugging or resampling
Debugging and LDB can refine the programs in the
                                                      rounds, all methods refine the seed program and
debugging process. This highlights the advantage
                                                      improve the performance. Particularly, LDB con-
of introducing a debugging stage in code genera-
                                                      tinuously improves the performance across the de-
tion with LLMs. Furthermore, LDB surpasses Self-
                                                      bugging iterations and achieves the best debugging
Debugging in debugging and refining programs.
                                                      performance despite the slightly slow rising speed.
It can improve performance on HumanEval even
                                                      In contrast, Self-Debugging nearly stops improving
further and achieve a new state-of-the-art result
                                                      the performance after 2 iterations, as also observed
(95.1%) in code generation by debugging the seed
                                                      in Chen et al. (2023c).
programs from Reflexion. This indicates that LDB
is able to examine the runtime execution and cor-     Necessity of Runtime Information. From Fig-
rect bugs overlooked by the advanced code gen-        ure 3, we observe that the performance of Self-
erators, serving as an orthogonal supplement to       Debugging presents a similar trend to Repeated
current code generation techniques.                   Sampling after 3 rounds. They both stops effec-
                                                      tively improving the performance at an early stage
3.5    Performance vs. Debugging Iterations           (around 2 ∼ 3 iterations). This phenomenon re-
In Figure 3, we plot the performance of LDB, Re-      veals a fundamental difference between LDB and
peated Sampling, Self-Debugging (+Expl.), and         Self-Debugging. We attribute it to the limited self-
Self-Debugging (+Trace) across each iteration on      correcting ability of LLMs, as pointed out in Huang
HumanEval using GPT-3.5. We introduce Re-             et al. (2023c). The feedback mechanisms in Self-
peated Sampling as a straightforward comparison       Debugging (self-explaining and self-tracing) in fact
method, where we repeatedly sample coding solu-       enhance the initial understanding of coding tasks
tions from the program generator until the solution   but fail to align the task to the specific code. There-
passes the visible test. The performance at each      fore, the debugging performance of these methods
iteration is computed in the same way as LDB. We      quickly converges and then hardly improves even
run these methods up to 10 iterations to examine      given more rounds of debugging. In the contrast,
the performance tendency. We show the perfor-         LDB exhibits a continuing improvement with the
mance of LDB across 20 iterations in Appendix 7       growth of debugging iterations. The new infor-
to explore the continuous improvement trend.          mation from runtime execution keeps moving the
                                                      models towards correct programs, which closely
  4
      https://github.com/noahshinn/reflexion          resembles the human debugging process.
                         85.0                                                                                        w/o                  Self-Debugging                      LDB
HumanEval Accuracy (%)                                                                                               debugger             (Chen et al., 2023c)                (ours)
                         82.5             LDB: Block-level (ours)
                                                 (82.9%)                                                       100         (+1.2)(+1.2)




                                                                                     TransCoder Accuracy (%)
                                                                                                                      95.1 96.3 96.3
                         80.0                  Line-level                                                                                        (+4.0)(+4.8)
                                                (80.5%)             Function-level                              90                               86.8 87.6
                                                                       (79.9%)                                                                                                (+9.1)
                         77.5                                                                                                             82.8
                                                                                                                                                                       (+4.6) 82.4
                                                                                                                80                                                     77.9
                         75.0                         Baseline (73.8%)                                                                                          73.3
                                                                                                                70
                         72.5
                                21   22   23        24      25      26       27                                 60
                                                 # Token (K)                                                              Easy               Medium                    Hard
Figure 4: Performance vs. average token cost per pro-                                Figure 5: Performance of LDB on problems of differ-
gram of LDB in different decomposition levels on Hu-                                 ent difficulty levels in TransCoder using GPT-3.5 as
manEval with GPT-3.5. LDB (block-level) achieves                                     the backbone. LDB demonstrates the most improve-
the best accuracy with the least token cost compared to                              ment on Hard-level problems, indicating its capability
LDB (line-level) and LDB (function-level).                                           in understanding the program execution and detecting
                                                                                     non-trivial errors in program debugging.

3.6                        Different Decomposition Levels of LDB
                                                                                     LLMs struggles to fully understand the code units
In Profiling (Section 2.2), we segment the run-                                      and accurately identify bugs within the program.
time trace into basic blocks based on the control                                       LDB (function-level) provides the most coarse-
flow graph. A basic block only has one entry and                                     grained information which largely preserves the
one exit in the program execution, serving as an                                     complete programs. However, the intermediate
ideal basic unit in the runtime analysis (Sherwood                                   states in the function-level fail to provide de-
et al., 2001). To explore the effectiveness and effi-                                tailed runtime information. Consequently, LDB
ciency of block-level decomposition, we develop                                      (function-level) is less effective and requires ap-
two comparative methods, LDB (line-level) and                                        proximately 8.1 iterations on average to debug a
LDB (function-level), which segment the runtime                                      program which are much more than the other levels
trace in the granularity of lines and functions re-                                  (see Appendix E for statistics). This explains the
spectively. We denote the original block-level de-                                   highest token cost of LDB (function-level).
bugging method as LDB (block-level). LDB in
different decomposition levels share the same ar-                                    3.7 Performance of Different Difficulty Levels
chitecture. They collect runtime intermediate states                                 To evaluate the capability of LDB in debugging pro-
at the end of each code unit. The code unit can be                                   grams, we dive into the problems it successfully de-
a line in LDB (line-level), a block in LDB (block-                                   bugs in TransCoder and categorize them into three
level), or a function in LDB (function-level). Simi-                                 difficulty levels, Easy, Medium, and Hard. The
larly, we adopt Selective Debugging (Section 2.3)                                    difficulty annotation is automatically performed
to fit prompts into the token limits of LLMs. Please                                 by GPT-4 (1106-preview) based on the canonical
refer to Appendix E for implementation details.                                      solutions of each problem to avoid potential subjec-
   Figure 4 plots the performance and average to-                                    tiveness. Figure 5 shows the improved accuracy for
ken cost per program of LDB in different decom-                                      each difficulty level from TransCoder dataset. We
position levels on HumanEval using GPT-3.5. The                                      observe that the performance of GPT-3.5 in code
detailed statistics are listed in Table 6 in Appendix.                               generation decreases with the increasing problem
All three debugging methods manage to enhance                                        difficulty while the improvement from the debug-
the performance, demonstrating the benefits from                                     ger increases in harder problems. Particularly, LDB
runtime execution information. Particularly, among                                   shows the most improvement (9.1%) on the hard-
the three decomposition levels, LDB (block-level)                                    level problems, which indicates that LDB is able
achieves the highest improvement.                                                    to detect the non-trivial bugs and understand the
   LDB (line-level) performs worse than LDB                                          complex execution flows in the harder problems.
(block-level) even if the line-level information is
more fine-grained. This may arise because line-                                      3.8                         Case Study
level decomposition leads to incomplete semantics                                    Figure 6 presents an example on HumanEval with
in each code unit (i.e. a line of code). As a result,                                GPT-3.5. In the example, LDB successfully fix the
     Task Description                               Large Language Model Debugger (LDB)
      1. Given a list of numbers, return
      whether or not they are sorted in
                                                    Segment Program into Basic Blocks & Feed in Visible Test Case
      ascending order.                               [BLOCK-0]                               [BLOCK-1]                                      [BLOCK-5]
      2. If list has more than 1 duplicate of the     Before: lst=[1,2,2,3,3,4]
                                                                                                     Before: i=0,                                          Before: i=4,
      same number, return False.                                                                 lst=[1,2,2,3,3,4]                                     lst=[1,2,2,3,3,4]
                                                      for i in range(len(lst)-1):             for i in range(len(lst)-1):                     return not any(lst.count(x)>1
     Visible Test Cases                                 if lst[i] > lst[i + 1]:                 if lst[i] > lst[i + 1]:                                      for x in lst)

             Input: lst=[1,2,2,3,3,4]                         After: i=0,                              After: i=1,                             After: i=4,lst=[1,2,2,3,3,4],
              Expected Output: True                       lst=[1,2,2,3,3,4]                        lst=[1,2,2,3,3,4]                                     _ret=False


     Seed Program                                                             Inspect the runtime states and gather the runtime execution information
      def is_sorted(lst):                           Query LLM to Verify Correctness of Each Block Step by Step
        for i in range(len(lst)-1):
                                                     [Verdict-0]                        [Verdict-1]                            [Verdict-5]
          if lst[i]>lst[i + 1]:
            return False                                   The block is Correct              The block is Correct                                The block is Incorrect
        return not any(lst.count(x) > 1                                                                                    …
               for x in lst)                          Explanation: The block             Explanation: The block                 Explanation: The task requires …. To fix this issue, we
                                                      initializes the variable `lst`     correctly checks if the current        should change the condition to lst.count(x)>2
                                                                                                                                                                     lst.count(x)>2    to
                                                      and `i` correctly.                 element …                              consider the original occurrence of the number in the list.
              Actual Output: False




Figure 6: Debugging example of LDB on HumanEval with GPT-3.5. LDB accurately detects the bug in Block-5,
and suggests tha correct fix to align the program to the task description.


the program and enable it to pass the visible and                                      LDB enhances code generation without expanding
hidden test cases. This case requires the program                                      sampling numbers complementing existing meth-
to check two conditions: (1) numbers sorted in as-                                     ods, while these existing code generation methods
cending order. (2) list does not have more than                                        could provide better seeds for our debugger.
1 duplicate of the same number. In the seed pro-
                                                                                       Feedback-based Code Refinement                Generat-
gram, it checks the first condition, while mistakenly
                                                                                       ing correct solutions could require iterative refine-
presents the second condition as not having any
                                                                                       ment due to model limitations. Interactive methods
duplicates (lst.count(x) > 1). In BLOCK-0 to
                                                                                       like using human feedback (Chen et al., 2023a; Wu
BLOCK-4, LDB makes the verdicts that each block
                                                                                       et al., 2023) are effective but labor-intensive. Alter-
correctly checks the first condition. For BLOCK-
                                                                                       natively, code refinement techniques (Chen et al.,
5, LDB finds out the mistake in the condition and
                                                                                       2023c; Jiang et al., 2023; Hu et al., 2024) based
locates the program bugs exactly in this block. It
                                                                                       on language models have been proposed, utiliz-
proposes to fix this condition into lst.count(x)
                                                                                       ing interpreter outputs, self-generated explanation,
> 2 so that it aligns with the task description.
                                                                                       and other users’ submission in competition-level
                                                                                       programming (Zhang et al., 2022b). Some train ad-
4   Related Work                                                                       ditional models for bug fixing (Pearce et al., 2023;
                                                                                       Huang et al., 2023d; Gupta et al., 2023), while LDB
Augmented Code Language Models Recent
                                                                                       utilizes debugging capabilities of original large lan-
language models based on deep neural net-
                                                                                       guage models. LDB follow an similar iterative
works (Achiam et al., 2023; Roziere et al., 2023;
                                                                                       refinement paradigm as previous works (Madaan
Li et al., 2023; Nijkamp et al., 2022) demonstrate
                                                                                       et al., 2023; Zhou et al., 2023b). It leverages exe-
great potential for coding tasks. Despite their im-
                                                                                       cution results for debugging inspired by previous
pressive capabilities, these models face challenges
                                                                                       works on execution-guided code generation (Chen
such as syntax correctness (Jin et al., 2023; Chen
                                                                                       et al., 2018; Ni et al., 2022). Additionally, agent
et al., 2023b), semantic alignment (Ni et al., 2023;
                                                                                       frameworks using reinforcement learning for cod-
Fan et al., 2023), code reliability (Zhong and Wang,
                                                                                       ing tasks (Shinn et al., 2023; Zhou et al., 2023a;
2023), and conflict merging (Zhang et al., 2022c).
                                                                                       Hong et al., 2023; Rasheed et al., 2024; Le et al.,
To address these challenges, some focus on en-
                                                                                       2022) incorporate feedback from environments to
hancing initial code generation by leveraging mul-
                                                                                       guide actions. While these frameworks excel in
tiple candidates (Shinn et al., 2023; Zhou et al.,
                                                                                       searching code generation space, LDB focuses on
2023a; Gu, 2023) or refining solutions based on
                                                                                       code refinement and consistently improves perfor-
better test cases (Zhang et al., 2023a) and self-
                                                                                       mance across various initial code.
consistency (Chen et al., 2022; Le et al., 2023),
while others train verifiers on execution results to                                   Decomposition in Reasoning          Prompting
predict solution quality (Ni et al., 2023). In contrast,                               methods suggest that decomposing problems aids
large language models in reasoning tasks (Wei          or recommendations expressed herein are those of
et al., 2022; Zhou et al., 2022; Lightman et al.,      the authors and should not be interpreted as neces-
2023; Dhuliawala et al., 2023; Wang et al., 2024;      sarily representing the views, either expressed or
Cheng et al., 2022). (Zhang et al., 2022a) proposes    implied, of the U.S. Government. The U.S. Gov-
program trunking to improve the program fix rate.      ernment is authorized to reproduce and distribute
Inspired by this, LDB decomposes programs into         reprints for government purposes not withstanding
blocks, querying language models for debugging         any copyright annotation hereon.
verdicts and explanation. LDB further introduces
batch debugging to improve the efficiency.
                                                       References
5   Conclusion                                         Josh Achiam, Steven Adler, Sandhini Agarwal, Lama
                                                         Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
We present LDB, a debugging framework that help          Diogo Almeida, Janko Altenschmidt, Sam Altman,
LLMs refine generated programs with runtime exe-         Shyamal Anadkat, et al. 2023. Gpt-4 technical report.
cution information. We empirically show that LDB         arXiv preprint arXiv:2303.08774.
significantly improves code generation accuracy
                                                       Alfred V Aho and Ravi Sethi Jeffrey D Ullman. 2015.
and achieves state-of-the-art performance in pro-        ,“compilers-principles, techniques, and tools”, pear-
gram debugging, by segmenting the programs into          son education asia, 2007.
basic blocks and tracking the intermediate values.
                                                       Frances E Allen. 1970. Control flow analysis. ACM
Experiments also reveal its unique paradigm of
                                                         Sigplan Notices, 5(7):1–19.
program debugging by using runtime information.
                                                       Glenn Ammons and James R Larus. 1998. Improving
Limitation                                               data-flow analysis with path profiles. In Proceedings
                                                         of the ACM SIGPLAN 1998 conference on Program-
LDB is a program debugging framework using               ming language design and implementation, pages
large language models. Therefore, it is subjected to     72–84.
the limitation of existing debugging methods of hu-    Jacob Austin, Augustus Odena, Maxwell Nye, Maarten
man developers. The correct test cases are manda-         Bosma, Henryk Michalewski, David Dohan, Ellen
tory in LDB so that LDB can execute the program           Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. 2021.
and compare the execution flow against the task           Program synthesis with large language models. arXiv
                                                          preprint arXiv:2108.07732.
description. It remains an open question in future
study whether LLMs are able to do self-correct by      Thomas Ball and James R Larus. 1994. Optimally pro-
simply looking at its intermediate execution with-       filing and tracing programs. ACM Transactions on
out knowing whether the result is correct or not         Programming Languages and Systems (TOPLAS),
                                                         16(4):1319–1360.
(a.k.a. test-case-free debugging).
                                                       Thomas Ball and James R Larus. 1996. Efficient
Ethic Statements                                         path profiling. In Proceedings of the 29th Annual
                                                         IEEE/ACM International Symposium on Microarchi-
This paper focuses on debugging code generated by        tecture. MICRO 29, pages 46–57. IEEE.
large language models. The architecture are built
upon open-source models and publicly available         Angelica Chen, Jérémy Scheurer, Tomasz Korbak,
                                                         Jon Ander Campos, Jun Shern Chan, Samuel R Bow-
proprietary models. All the datasets in this paper       man, Kyunghyun Cho, and Ethan Perez. 2023a. Im-
are available online. We did not hire any human          proving code generation by training with natural lan-
annotators in our experiments. We will release           guage feedback. arXiv preprint arXiv:2303.16749.
the code and datasets on https://github.com/
                                                       Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan,
FloridSleeves/LLMDebugger. Therefore, we do              Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2022.
not anticipate any major ethical concerns.               Codet: Code generation with generated tests. In
                                                         The Eleventh International Conference on Learning
Acknowledgement                                          Representations.

Our work is sponsored in part by NSF CAREER            Hongqiao Chen, Kexun Zhang, Lei Li, and
                                                         William Yang Wang. 2023b. Tooldec: Syntax
Award 2239440, NSF Proto-OKN Award 2333790,              error-free and generalizable tool use for llms via
as well as generous gifts from Google, Adobe, and        finite-state decoding. In The 3rd Workshop on
Teradata. Any opinions, findings, and conclusions        Mathematical Reasoning and AI at NeurIPS’23.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming                Metagpt: Meta programming for multi-agent collabo-
 Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-         rative framework. arXiv preprint arXiv:2308.00352.
 plan, Harri Edwards, Yuri Burda, Nicholas Joseph,
 Greg Brockman, et al. 2021. Evaluating large            Mengkang Hu, Yao Mu, Xinmiao Yu, Mingyu Ding,
 language models trained on code. arXiv preprint          Shiguang Wu, Wenqi Shao, Qiguang Chen, Bin
 arXiv:2107.03374.                                        Wang, Yu Qiao, and Ping Luo. 2023. Tree-planner:
                                                          Efficient close-loop task planning with large language
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and          models. arXiv preprint arXiv:2310.08582.
  Denny Zhou. 2023c. Teaching large language models
  to self-debug. arXiv preprint arXiv:2304.05128.        Xueyu Hu, Kun Kuang, Jiankai Sun, Hongxia Yang,
                                                           and Fei Wu. 2024. Leveraging print debugging to
Xinyun Chen, Chang Liu, and Dawn Song. 2018.               improve code generation in large language models.
  Execution-guided neural program synthesis. In Inter-     arXiv preprint arXiv:2401.05319.
  national Conference on Learning Representations.
                                                         Baizhou Huang, Shuai Lu, Weizhu Chen, Xiaojun Wan,
Zhoujun Cheng, Tianbao Xie, Peng Shi, Chengzu
                                                           and Nan Duan. 2023a. Enhancing large language
  Li, Rahul Nadkarni, Yushi Hu, Caiming Xiong,
  Dragomir Radev, Mari Ostendorf, Luke Zettlemoyer,        models in coding through multi-perspective self-
  et al. 2022. Binding language models in symbolic         consistency. arXiv preprint arXiv:2309.17272.
  languages. In The Eleventh International Conference
                                                         Haochen Huang, Bingyu Shen, Li Zhong, and Yuanyuan
  on Learning Representations.
                                                           Zhou. 2023b. Protecting data integrity of web ap-
John Cocke. 1970. Global common subexpression elim-        plications with database constraints inferred from
  ination. In Proceedings of a symposium on Compiler       application code. In Proceedings of the 28th ACM
  optimization, pages 20–24.                               International Conference on Architectural Support
                                                           for Programming Languages and Operating Systems,
Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu,             Volume 2, pages 632–645.
  Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Ja-
  son Weston. 2023. Chain-of-verification reduces hal-   Haochen Huang, Chengcheng Xiang, Li Zhong, and
  lucination in large language models. arXiv preprint      Yuanyuan Zhou. 2021. {PYLIVE}:{On-the-Fly}
  arXiv:2309.11495.                                        code change for python-based online services.
                                                           In 2021 USENIX Annual Technical Conference
Zhiyu Fan, Xiang Gao, Martin Mirchev, Abhik Roy-           (USENIX ATC 21), pages 349–363.
  choudhury, and Shin Hwei Tan. 2023. Automated
  repair of programs from large language models.         Jie Huang, Xinyun Chen, Swaroop Mishra,
  In 2023 IEEE/ACM 45th International Conference            Huaixiu Steven Zheng, Adams Wei Yu, Xiny-
  on Software Engineering (ICSE), pages 1469–1481.          ing Song, and Denny Zhou. 2023c. Large language
  IEEE.                                                     models cannot self-correct reasoning yet. arXiv
                                                            preprint arXiv:2310.01798.
Python Software Foundation. 2001. pdb — the
  python debugger. https://docs.python.org/3/            Kai Huang, Xiangxin Meng, Jian Zhang, Yang Liu,
  library/pdb.html.                                        Wenjie Wang, Shuhao Li, and Yuqing Zhang. 2023d.
                                                           An empirical study on fine-tuning large language
Tao Ge, Jing Hu, Xun Wang, Si-Qing Chen, and Furu
                                                           models of code for automated program repair. In
  Wei. 2023. In-context autoencoder for context com-
                                                           2023 38th IEEE/ACM International Conference on
  pression in a large language model. arXiv preprint
                                                           Automated Software Engineering (ASE), pages 1162–
  arXiv:2307.06945.
                                                           1174. IEEE.
Qiuhan Gu. 2023. Llm-based code generation method
  for golang compiler testing. In Proceedings of the     Shuyang Jiang, Yuhao Wang, and Yu Wang. 2023. Self-
  31st ACM Joint European Software Engineering Con-        evolve: A code evolution framework via large lan-
  ference and Symposium on the Foundations of Soft-        guage models. arXiv preprint arXiv:2306.02907.
  ware Engineering, pages 2201–2203.
                                                         Matthew Jin, Syed Shahriar, Michele Tufano, Xin
Priyanshu Gupta, Avishree Khare, Yasharth Bajpai,         Shi, Shuai Lu, Neel Sundaresan, and Alexey Svy-
   Saikat Chakraborty, Sumit Gulwani, Aditya Kanade,      atkovskiy. 2023. Inferfix: End-to-end program repair
   Arjun Radhakrishna, Gustavo Soares, and Ashish Ti-     with llms. arXiv preprint arXiv:2303.07263.
   wari. 2023. Grace: Language models meet code edits.
   In Proceedings of the 31st ACM Joint European Soft-   James R Larus. 1999. Whole program paths. ACM
   ware Engineering Conference and Symposium on the        SIGPLAN Notices, 34(5):259–269.
  Foundations of Software Engineering, pages 1483–
  1495.                                                  Hung Le, Hailin Chen, Amrita Saha, Akash Gokul,
                                                           Doyen Sahoo, and Shafiq Joty. 2023. Codechain: To-
Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng             wards modular code generation through chain of self-
   Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven      revisions with representative sub-modules. arXiv
   Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. 2023.     preprint arXiv:2310.08992.
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio         Shishir G Patil, Tianjun Zhang, Xin Wang, and
  Savarese, and Steven Chu Hong Hoi. 2022. Coderl:           Joseph E Gonzalez. 2023. Gorilla: Large language
  Mastering code generation through pretrained models        model connected with massive apis. arXiv preprint
  and deep reinforcement learning. Advances in Neural        arXiv:2305.15334.
  Information Processing Systems, 35:21314–21328.
                                                           Hammond Pearce, Benjamin Tan, Baleegh Ahmad,
Jian Li, Yue Wang, Michael R. Lyu, and Irwin King.           Ramesh Karri, and Brendan Dolan-Gavitt. 2023. Ex-
   2018. Code completion with neural attention and           amining zero-shot vulnerability repair with large lan-
   pointer networks. In Proceedings of the 27th Inter-       guage models. In 2023 IEEE Symposium on Security
   national Joint Conference on Artificial Intelligence,     and Privacy (SP), pages 2339–2356. IEEE.
   IJCAI’18, page 4159–25. AAAI Press.
                                                           Reese T Prosser. 1959. Applications of boolean ma-
Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas            trices to the analysis of flow diagrams. In Papers
  Muennighoff, Denis Kocetkov, Chenghao Mou, Marc            presented at the December 1-3, 1959, eastern joint
  Marone, Christopher Akiki, Jia Li, Jenny Chim, et al.      IRE-AIEE-ACM computer conference, pages 133–
  2023. Starcoder: may the source be with you! arXiv         138.
  preprint arXiv:2305.06161.
                                                           Zeeshan Rasheed, Muhammad Waseem, Mika Saari,
Yujia Li, David Choi, Junyoung Chung, Nate Kushman,          Kari Systä, and Pekka Abrahamsson. 2024. Code-
  Julian Schrittwieser, Rémi Leblond, Tom Eccles,            pori: Large scale model for autonomous software
  James Keeling, Felix Gimeno, Agustin Dal Lago,             development by using multi-agents. arXiv preprint
  et al. 2022. Competition-level code generation with        arXiv:2402.01411.
  alphacode. Science, 378(6624):1092–1097.
                                                           Veselin Raychev, Martin Vechev, and Eran Yahav. 2014.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri          Code completion with statistical language models. In
  Edwards, Bowen Baker, Teddy Lee, Jan Leike,                Proceedings of the 35th ACM SIGPLAN conference
  John Schulman, Ilya Sutskever, and Karl Cobbe.             on programming language design and implementa-
  2023. Let’s verify step by step. arXiv preprint            tion, pages 419–428.
  arXiv:2305.20050.
                                                           Eric Rotenberg, Steve Bennett, and James E Smith.
                                                             1996. Trace cache: a low latency approach to high
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
                                                             bandwidth instruction fetching. In Proceedings of the
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,
                                                             29th Annual IEEE/ACM International Symposium on
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,
                                                             Microarchitecture. MICRO 29, pages 24–34. IEEE.
 et al. 2023. Self-refine: Iterative refinement with
 self-feedback. arXiv preprint arXiv:2303.17651.           Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten
                                                             Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,
Niklas Muennighoff, Qian Liu, Armel Zebaze, Qinkai           Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023.
  Zheng, Binyuan Hui, Terry Yue Zhuo, Swayam                 Code llama: Open foundation models for code. arXiv
  Singh, Xiangru Tang, Leandro Von Werra, and                preprint arXiv:2308.12950.
  Shayne Longpre. 2023. Octopack: Instruction tun-
  ing code large language models. In NeurIPS 2023          Baptiste Roziere, Marie-Anne Lachaux, Lowik Chanus-
  Workshop on Instruction Tuning and Instruction Fol-        sot, and Guillaume Lample. 2020. Unsupervised
  lowing.                                                    translation of programming languages. Advances in
                                                             Neural Information Processing Systems, 33:20601–
Ansong Ni, Jeevana Priya Inala, Chenglong Wang, Alex         20611.
  Polozov, Christopher Meek, Dragomir Radev, and
  Jianfeng Gao. 2022. Learning math reasoning from         Timothy Sherwood, Erez Perelman, and Brad Calder.
  self-sampled correct and partially-correct solutions.      2001. Basic block distribution analysis to find peri-
  In The Eleventh International Conference on Learn-         odic behavior and simulation points in applications.
  ing Representations.                                       In Proceedings 2001 International Conference on
                                                             Parallel Architectures and Compilation Techniques,
Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoy-         pages 3–14. IEEE.
  anov, Wen-tau Yih, Sida Wang, and Xi Victoria Lin.
  2023. Lever: Learning to verify language-to-code         Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke
  generation with execution. In International Con-           Zettlemoyer, and Sida I Wang. 2022. Natural lan-
  ference on Machine Learning, pages 26106–26128.            guage to code translation with execution. In Proceed-
  PMLR.                                                      ings of the 2022 Conference on Empirical Methods
                                                             in Natural Language Processing, pages 3533–3546.
Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan
  Wang, Yingbo Zhou, Silvio Savarese, and Caiming          Noah Shinn, Federico Cassano, Ashwin Gopinath,
  Xiong. 2022. Codegen: An open large language               Karthik R Narasimhan, and Shunyu Yao. 2023. Re-
   model for code with multi-turn program synthesis. In      flexion: Language agents with verbal reinforcement
  The Eleventh International Conference on Learning          learning. In Thirty-seventh Conference on Neural
   Representations.                                          Information Processing Systems.
Richard Stallman, Roland Pesch, Stan Shebs, et al. 1988.   Tianyi Zhang, Tao Yu, Tatsunori Hashimoto, Mike
  Debugging with gdb. Free Software Foundation, 675.         Lewis, Wen-tau Yih, Daniel Fried, and Sida Wang.
                                                             2023b. Coder reviewer reranking for code generation.
Zilu Tang, Mayank Agarwal, Alexander Shypula, Bailin         In International Conference on Machine Learning,
   Wang, Derry Wijaya, Jie Chen, and Yoon Kim. 2023.         pages 41832–41846. PMLR.
   Explain-then-translate: an analysis on improving pro-
   gram translation with self-generated explanations. In   Li Zhong. 2023.      A survey of prevent and de-
   Findings of the Association for Computational Lin-        tect access control vulnerabilities. arXiv preprint
   guistics: EMNLP 2023, pages 1741–1788.                    arXiv:2304.10600.
Zilong Wang, Hao Zhang, Chun-Liang Li, Julian Mar-         Li Zhong and Zilong Wang. 2023. A study on robust-
   tin Eisenschlos, Vincent Perot, Zifeng Wang, Lesly         ness and reliability of large language model code
   Miculicich, Yasuhisa Fujii, Jingbo Shang, Chen-Yu          generation. arXiv preprint arXiv:2308.10335.
   Lee, et al. 2024. Chain-of-table: Evolving tables in
   the reasoning chain for table understanding. arXiv      Li Zhong, Chengcheng Xiang, Haochen Huang, Bingyu
   preprint arXiv:2401.04398.                                 Shen, Eric Mugnier, and Yuanyuan Zhou. 2024. Ef-
                                                              fective bug detection with unused definitions. In
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten              Proceedings of the Nineteenth European Conference
   Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,             on Computer Systems, pages 720–735.
   et al. 2022. Chain-of-thought prompting elicits rea-
   soning in large language models. Advances in Neural     Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman,
   Information Processing Systems, 35:24824–24837.           Haohan Wang, and Yu-Xiong Wang. 2023a. Lan-
                                                             guage agent tree search unifies reasoning acting
Zeqiu Wu, Yushi Hu, Weijia Shi, Nouha Dziri,                 and planning in language models. arXiv preprint
  Alane Suhr, Prithviraj Ammanabrolu, Noah A                 arXiv:2310.04406.
  Smith, Mari Ostendorf, and Hannaneh Hajishirzi.
  2023. Fine-grained human feedback gives better           Aojun Zhou, Ke Wang, Zimu Lu, Weikang Shi, Sichun
  rewards for language model training. arXiv preprint        Luo, Zipeng Qin, Shaoqing Lu, Anya Jia, Linqi Song,
  arXiv:2306.01693.                                          Mingjie Zhan, et al. 2023b. Solving challenging
                                                             math word problems using gpt-4 code interpreter
Pengcheng Yin and Graham Neubig. 2017. A syntactic           with code-based self-verification. arXiv preprint
  neural model for general-purpose code generation.          arXiv:2308.07921.
  In Proceedings of the 55th Annual Meeting of the
  Association for Computational Linguistics (Volume        Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
  1: Long Papers), pages 440–450.                            Nathan Scales, Xuezhi Wang, Dale Schuurmans,
                                                             Claire Cui, Olivier Bousquet, Quoc V Le, et al. 2022.
Zhiqiang Yuan, Junwei Liu, Qiancheng Zi, Ming-               Least-to-most prompting enables complex reasoning
  wei Liu, Xin Peng, and Yiling Lou. 2023. Eval-             in large language models. In The Eleventh Interna-
  uating instruction-tuned large language models on          tional Conference on Learning Representations.
  code comprehension and generation. arXiv preprint
  arXiv:2308.01240.
Jialu Zhang, José Cambronero, Sumit Gulwani, Vu Le,
   Ruzica Piskac, Gustavo Soares, and Gust Ver-
   bruggen. 2022a. Repairing bugs in python assign-
   ments using large language models. arXiv preprint
   arXiv:2209.14876.
Jialu Zhang, De Li, John Charles Kolesar, Hanyuan Shi,
   and Ruzica Piskac. 2022b. Automated feedback gen-
   eration for competition-level code. In Proceedings
   of the 37th IEEE/ACM International Conference on
   Automated Software Engineering, pages 1–13.
Jialu Zhang, Todd Mytkowicz, Mike Kaufman, Ruz-
   ica Piskac, and Shuvendu K Lahiri. 2022c. Using
   pre-trained language models to resolve textual and
   semantic merge conflicts (experience paper). In Pro-
   ceedings of the 31st ACM SIGSOFT International
   Symposium on Software Testing and Analysis, pages
   77–88.
Kexun Zhang, Danqing Wang, Jingtao Xia,
  William Yang Wang, and Lei Li. 2023a. Algo:
  Synthesizing algorithmic programs with generated
  oracle verifiers. arXiv preprint arXiv:2305.14591.
Appendix                                                   entry block to the exit block (Ball and Larus, 1994,
                                                           1996; Ammons and Larus, 1998).
A    Performance with Better Reasoners
                                                           C    Implementation Details
We explore the relationship between performance
and the ability of debugging backbones. With better        In the debugging stage of LDB, we generate the
reasoners as debugging backbones, LDB achieves             debugging verdicts and explanation using greedy
higher performance, which can be up to 98.2% on            decoding with temperature T = 0 to improve the
HumanEval with Reflexion as the seed generators            reproducibility of our experiment. The maximum
and GPT-4o (2024-05-13) as the backbones.                  number of debugging iterations is 10. We set the
                                                           threshold for the number of sampled blocks and
 Reflexion +LDB (GPT-3.5) +LDB (GPT-4) +LDB (GPT-4o)       input tokens at 10 and 3,097, respectively.
 91.5       95.1(+3.6)     96.9(+5.4)   98.2 (+6.6)
                                                           D    Overhead Breakdown
Table 3: Accuracy of LDB on HumanEval with seed pro-
grams from Reflexion shows that LDB performs better        The time cost of LDB is comparable to other base-
with more advanced debugging backbones. We use GPT-        line methods and all debugging steps of LDB are
3.5 (turbo-0613), GPT-4 (1106-preview), and GPT-           fully automated without any human labor, as shown
4o (2024-05-13) as the debugging backbone. LDB             in Table 4. We summarize the standard paradigm
performs better when it is backboned with better reason-   of iterative refinement methods as follows: (1)
ers (GPT-4 and GPT-4o).                                    Execute the buggy program with a Python inter-
                                                           preter. (2) Query a LLM to generate debugging
                                                           feedback. (3) Query a LLM again to regenerate a
B    Programming Language Concepts
                                                           program based on the feedback. LDB, along with
Basic Block. A basic block is defined as a linear          the baseline methods Self-Debugging all follows
sequence of code containing a single entry point           this paradigm. We compare the time cost of LDB
and a single exit point (Allen, 1970; Aho and Ull-         and Self-Debugging in each stage on HumanEval
man, 2015). Upon executing the first instruction           with GPT-3.5. Compared with the baseline method,
within a basic block, all subsequent instructions are      the additional time cost of LDB comes from the
guaranteed to execute exactly once and in sequen-          profiling step (Section 2.2). This step is performed
tial order. A sequence of instructions is considered       by program analysis and only costs 0.09 seconds
a basic block if it satisfies two conditions: (1) each     on average for programs in HumanEval. The over-
instruction in the sequence always executes before         head turns out to be negligible under the fluctuation
all subsequent instructions, and (2) there are no in-      of other overhead while contributing to a signifi-
tervening instructions between any two instructions        cant improvement in the performance as shown in
in the sequence (Cocke, 1970; Allen, 1970).                Table 1 and Figure 3.

Control Flow Graph. The control-flow graph                 E   Tradeoffs in Debugging in Different
(CFG) (Allen, 1970; Prosser, 1959) serves as a                 Decomposition Levels
graphical depiction of all potential paths traversed
during the execution of a program. Each node               We conduct different level debugging following
within the CFG corresponds to a basic block, with          this design: (1) For LDB (line-level) debugging,
directed edges representing transitions in the con-        we collect the intermediate states before and af-
trol flow. Typically, two special blocks are identi-       ter each line execution. We sample the first 25
fied: the entry block, which signifies the initiation      lines and last 25 lines when the line number ex-
of control flow into the graph, and the exit block,        ceeds threshold Nb = 50, which is five times of the
where all control flow exits the graph.                    block-level threshold. We set this number based
                                                           on the previous research on the average number
Execution Traces. In this paper, execution                 of instructions in a basic block (Rotenberg et al.,
traces are control-flow traces of the whole pro-           1996). (2) For the original LDB (block-level) de-
gram (Larus, 1999). An control-flow trace of a             bugging, we sample the first 5 blocks and the last 5
program is a sequence of consecutively executed            blocks when the block number exceeds threshold
basic blocks within the program. It also corre-            Nb = 10. (3) For LDB (function-level) debug-
sponds to a path in the control flow graph from the        ging, we decompose the program on function-level,
    Debugging Stages                            LDB                                                                                                                     Self-Debugging
    Execute the buggy program                   0.01s                                                                                                                   0.01s
    Query a LLM to generate feedbacks           0.09s (profiling) + 9.25s (feedback generation)                                                                         9.84s
    Query a LLM to regenerate programs          7.83s                                                                                                                   7.17s
    Other minor overhead                        0.05s                                                                                                                   0.01s
    Total Time                                  17.23s                                                                                                                  17.08s

                           Table 4: Performance breakdown of LDB and Self-Debugging.


namely we only collect the intermediate states at                      HumanEval                                              GPT-3.5 Avg. Turn CodeLlama Avg. Turn
the entry and exit of the solution function. If the                    (w/o debugger)                                               73.8                   -                 49.4                      -
                                                                       LDB (line-level)                                             80.5                  6.4                53.7                     9.1
function trace exceeds the context length, we sam-                     LDB (block-level)                                            82.9                  6.2                55.5                     7.8
ple first 25 lines and last 25 lines to ensure same                    LDB (function-level)                                         79.9                  8.1                53.7                     9.3

amount of code trace information with block-level
                                                              Table 6: Accuracy vs debugging turns on HumanEval.
and line-level. These three level of decomposition            For both GPT-3.5 and CodeLlama, LDB with block-
expand from fine to coarse granularity.                       level debugging achieves the highest accuracy and
   We show the average token cost per program and             fewest debugging turns.
debugging turns of LDB with different granular-
ity debugging levels in Table 5 and Table 6. Us-                                   84                                                                                                                         84.1
                                                              HumanEval Accuracy (%)

                                                                                                                                                                                        83.5 83.5 83.5 83.5
ing GPT-3.5, LDB (line-level) has less token cost                                                                                                       82.9 82.9 82.9 82.9 82.9 82.9
                                                                                   82                                                  82.3 82.3 82.3
than LDB-Function due to less debugging turns.                                                                             81.7 81.7

                                                                                   80                               80.5
However, using CodeLlama, an open source model,
                                                                                                             79.3
LDB has higher token cost in the line-level debug-                                 78
ging than the function-level debugging. The de-                                                       76.8
                                                                                   76
bugging turns of line-level debugging is not signifi-
cantly lower than function-level debugging, which                                  74
                                                                                               75.0
                                                                                                                                                                          LDB (ours)
                                                                                        73.8
shows that CodeLlama has worse reasoning ability                                        0             2             4           6           8           10       12        14           16       18           20
                                                                                                                                                # Turns
for line-level debugging even with more runtime ex-
ecution information. Besides, line-level debugging            Figure 7: Performance of LDB on HumanEval with
has higher token costs for each debugging turns.              GPT-3.5 in 20 debugging iterations. The final perfor-
Therefore, it has the highest token cost. Both GPT-           mance after 20 iterations is 84.1%.
3.5 and CodeLlama demonstrate better efficiency
and accuracy in the block-level debugging. Based
on these observations, we choose block-level de-              token efficiency of LDB and alleviates the pitfall
bugging in LDB.                                               of repeatedly sending context to language models
                                                              in iterative refinement (Hu et al., 2023). Assume
 HumanEval           GPT-3.5     Token CodeLlama Token        the average token numbers is N for debugging
 (w/o debugger)       73.8        -     49.4          -       each block, average block number is B for debug-
 LDB (line-level)     80.5 (+6.7) 24K   53.7 (+4.3)   72K     ging, and average debugging iteration number is D.
 LDB (block-level)    82.9 (+9.1) 23K   55.5 (+6.1)   52K
 LDB (function-level) 79.9 (+6.1) 27K   53.7 (+4.3)   54K     Without batch debugging, for debugging i-th block,
                                                                                               Pi∗N
                                                              the context length for debugging is
                                                                                                  B
                                                                                                      . Therefore,
Table 5: Accuracy vs average token number per problem         debugging N blocks consumes i=0 (i ∗ N ), ap-
on HumanEval. For both GPT-3.5 and CodeLlama,                 proximately O(B 2 ∗ N ) tokens. As a comparison,
LDB with block-level debugging achieves the highest           batch debugging only send one debugging message
accuracy and least token cost.
                                                              in each turn, which has context length of O(B ∗ N )
                                                              tokens.
F    Complexity Analysis of Batch
     Debugging                                                G                         Debugging 10 More Iterations
LDB can batch runtime information of all selected             As LDB shows a different trend of performance
blocks together and query language models for de-             regarding debugging turns compared to the state-
bugging verdicts. This significantly improves the             of-the-art methods, it is interesting to see whether
                     HumanEval MBPP TransCoder          is that the syntax errors are less frequent given the
    Accuracy           93.7%   95.3%     86.7%          code generation ability of current LLMs, and LDB
    Syntax Error       18.8%   23.2%     20.0%          can better debug semantic errors by introducing the
    Semantic Error     81.2%   76.8%     80.0%          detailed runtime execution information.

Table 7: Debug correctness of LDB and detected pro-     I   Extendability of LDB
gram error types.
                                                        In this paper, we have chosen Python for LDB due
                                                        to its widespread popularity in software develop-
the performance continues growing after 10 debug-       ment (Huang et al., 2021). This aligns with previ-
ging turns. We conduct a experiment that continue       ous studies such as Self-Debugging (Chen et al.,
debugging until 20 debugging turns to explore the       2023c), Reflexion (Shinn et al., 2023), and Go-
characteristic of LDB, as shown in Figure 7. The        rilla (Patil et al., 2023), which also utilize Python
accuracy still grows after 10 debugging turns and       to showcase the effectiveness of their methodolo-
achieves 84.1%.                                         gies.
                                                           We further elaborated on LDB’s capability to
H     Error Analysis of LDB                             adapt to other programming languages. Impor-
We analyze the debugging feedback of LDB in two         tantly, LDB does not use features that are specific
perspectives, the bug localization accuracy and the     to Python. This makes it easy to adapt LDB for use
bug categorization. We evaluate the performance         with other programming languages by changing
of LDB in localizing the bug accurately and further     its program executors and analysis tools (Zhong,
specify the types of bugs detected by LDB. We use       2023; Huang et al., 2023b; Zhong et al., 2024). In
the results with GPT-3.5 as an example.                 the debugging process of LDB, the backbone LLM
                                                        debugs programs based on the detailed runtime ex-
Accuracy of Bug Localization. To evaluate the           ecution information, such as execution traces and
correctness of debugging verdicts made by LDB,          intermediate variables. This runtime execution in-
we collect the cases that LDB successfully de-          formation can be similarly obtained in all different
bugs and query GPT-4 (1106-Preview) to auto-            kinds of programming languages. We can use off-
matically verify whether LDB correctly identifies       the-shell program analysis tools to instrument the
the buggy basic block. In the prompt, we pro-           targeted language and acquire the runtime execu-
vide the task description, the seed program, the        tion information. Incorporating multilingual exper-
runtime information, debugging responses, and           iment settings, such as the HumanEval-X, remains
the final programs for GPT-4. Table 7 shows             as a future work.
the analysis results on HumanEval, MBPP and
TransCoder. We observe that LDB achieves an ac-         J   Prompt Example in LDB
curacy over 85% over all datasets. It has the highest   We list the prompts used in LDB in detail as follow,
accuracy on MBPP (95.5%) while performs worst           • The prompts used in the chat mode are shown in
on TransCoder (86.7%). This may arise because             Figure 8.
TransCoder consists of more complicated programs        • The prompts used in the text completion mode
where the original C++ programs outlines the in-          are shown in Figure 9.
tention implicitly.
Bug Categorization. We further categorize the
bugs detected and fixed by LDB into two categories:
Syntax Errors and Semantic Errors. Syntax errors
refer to the cases that violates the syntax rules of
its programming language. Semantic error occurs
when the code runs without producing any syn-
tax errors, but it does not behave as intended, thus
fails the test cases. We annotate the categories
through GPT-4 (1106-preview) to avoid subjec-
tiveness. Across three datasets, LDB fixes semantic
errors with around 80% of the time. The reason
==================================== System ====================================
You are an expert programming assistant .



===================================== User =====================================
Complete the following task in Python . Please respond with code only .
def is_sorted ( lst ):
    '''
    Given a list of numbers , return whether or not they
    are sorted in ascending order . If list has more than
    1 duplicate of the same number , return False .
    Assume no negative numbers and only integers .

    Examples
    is_sorted ([5]) =    True
    is_sorted ([1 , 2,   3, 4, 5]) = True
    is_sorted ([1 , 2,   3, 4, 5, 6, 7]) = True
    is_sorted ([1 , 2,   2, 2, 3, 4]) = False
    '''



=================================== Assistant ==================================
    for i in range ( len ( lst ) - 1) :
        if lst [i] > lst [i + 1]:
            return False
    return not any ( lst . count (x) > 1 for x in lst )



===================================== User =====================================
The code above fails the given unit test :
assert is_sorted ([1 , 2, 2, 3, 3, 4]) == True # Real Execution Output : False .
Help me debug this .

Here is the code execution trace block by block with the intermediate variable
values to debug your code . You need to answer FOR EACH BLOCK whether this code
block is correct or not . If not , give an explanation on what is wrong . Please
wrap your response into a JSON object that contains keys `block ` with the name of
 each block , key ` correct ` with value False or True , and key ` explanation ` with
an explanation on the bug .

Example Answers :
{" block ": " BLOCK -1" , " correct ": " True ", " explanation ": " The block initializes
variable `a ` and `b `."}
{" block ": " BLOCK -2" , " correct ": " False ", " explanation ": " The block is incorrect
because the code does not add the two integers together , but instead subtracts
the second integer from the first . To fix this issue , we should change the
operator from `-` to `+` in the return statement . This will ensure that the
function returns the correct output for the given input ."}

[ BLOCK -0]
     # lst =[1 , 2, 2, 3, 3, 4]
     for i in range ( len ( lst ) - 1) :
          if lst [i] > lst [i + 1]:
     # i =0        lst =[1 , 2, 2, 3, 3,   4]
[ BLOCK -1]
     # i =0        lst =[1 , 2, 2, 3, 3,   4]
     for i in range ( len ( lst ) - 1) :
          if lst [i] > lst [i + 1]:
     # i =1        lst =[1 , 2, 2, 3, 3,   4]
[ BLOCK -2]
     # i =1        lst =[1 , 2, 2, 3, 3,   4]
     for i in range ( len ( lst ) - 1) :
          if lst [i] > lst [i + 1]:
     # i =2        lst =[1 , 2, 2, 3, 3,   4]
[ BLOCK -3]
     # i =2        lst =[1 , 2, 2, 3, 3,   4]
     for i in range ( len ( lst ) - 1) :
          if lst [i] > lst [i + 1]:
     # i =3        lst =[1 , 2, 2, 3, 3,   4]
[ BLOCK -4]
     # i =3        lst =[1 , 2, 2, 3, 3,    4]
     for i in range ( len ( lst ) - 1) :
          if lst [i] > lst [i + 1]:
     # i =4        lst =[1 , 2, 2, 3, 3,    4]
[ BLOCK -5]
     # i =4        lst =[1 , 2, 2, 3, 3,    4]
     for i in range ( len ( lst ) - 1) :
     return not any ( lst . count (x) > 1   for x in lst )
     # i =4        lst =[1 , 2, 2, 3, 3,    4] _ret = False



=================================== Assistant ==================================
{" block ": " BLOCK -0" , " correct ": true , " explanation ": " The block initializes the
variable `lst ` correctly ."}
{" block ": " BLOCK -1" , " correct ": true , " explanation ": " The block correctly checks
if the current element is greater than the next element in the list ."}
{" block ": " BLOCK -2" , " correct ": true , " explanation ": " The block correctly checks
if the current element is greater than the next element in the list ."}
{" block ": " BLOCK -3" , " correct ": true , " explanation ": " The block correctly checks
if the current element is greater than the next element in the list ."}
{" block ": " BLOCK -4" , " correct ": true , " explanation ": " The block correctly checks
if the current element is greater than the next element in the list ."}
{" block ": " BLOCK -5" , " correct ": false , " explanation ": " The block is incorrect
because it returns the opposite of the condition `lst . count (x) > 1` for any
element `x ` in the list . This means that if any element has more than 1 duplicate
, the function will return False . However , the task requires that if there are
more than 1 duplicate of the same number , the function should return False . To
fix this issue , we should change the condition to `lst . count (x) > 2` to account
for the original occurrence of the number in the list ."}



===================================== User =====================================
Please fix the Python code .



=================================== Assistant ==================================
def is_sorted ( lst ):
    '''
    Given a list of numbers , return whether or not they
    are sorted in ascending order . If list has more than
    1 duplicate of the same number , return False .
    Assume no negative numbers and only integers .

    Examples
    is_sorted ([5]) = True
    is_sorted ([1 , 2, 3, 4, 5]) = True
    is_sorted ([1 , 2, 3, 4, 5, 6, 7]) = True
    is_sorted ([1 , 2, 2, 2, 3, 4]) = False
    '''
    for i in range ( len ( lst ) - 1) :
        if lst [i] > lst [i + 1]:
             return False
    return not any ( lst . count (x) > 2 for x in lst )



                                 Figure 8: Prompt for chat mode.
# Write Python function to complete the task and pass the assertion tests .
### Task Start ###
# These are the assertions for your function :
assert find_char_long ( ' Please move back to stream ') == [' Please ' , 'move ', 'back ',
 ' stream ']

def find_char_long ( text ):
    """
    Write a function to find all words which are at least 4 characters long in a
    string by using regex .
    """
    if text == "":
        return []
    pat = r "\ b\w {4}\ b"
    res = re . findall ( pat , text )
    return res

With the above function , the assertion is ` find_char_long (' Please move back to
stream ') == [' Please ', ' move ', ' back ' , ' stream '] ` but the real execution output
is `[' move ' , ' back '] `.
Debug the program trace block by block until find the incorrect block . Every
block should have different feedbacks :
[ BLOCK -0]
     # text =" Please move back to stream "
     if text == "":
[ BLOCK -1]
     # text =" Please move back to stream "
     pat = r "\ b\w {4}\ b"
     res = re . findall ( pat , text )
     # text =" Please move back to stream " pat ="\ b\w {4}\ b" res =[ ' move ' , ' back ']
[ debug ]
[ BLOCK -0]
Feedback : CORRECT . This block is correct . It checks if the input text is empty .
If the input text is empty , it returns an empty list without do regex match .
[ BLOCK -1]
Feedback : INCORRECT . This block defines a regular expression pattern `pat ` with
value r "\ b\w {4}\ b ". However , there ' s an issue with the regular expression pattern
. It only matches words that are exactly 4 characters long . Therefore , the return
  value `_ret ` is `[' move ' , ' back '] `. In the task description , it asks for words
which are at least 4 characters long . To fix the code , we should change ` pat =r "\ b\
w {4}\ b"` into `pat = r "\ b\w {4 ,}\ b " `.
[/ debug ]
Please fix the Python code .
[ python ]
import re
def find_char_long ( text ):
     """
     Write a function to find all words which are at least 4 characters long in a
     string by using regex .
     """
     if text == "":
           return []
     pat = r "\ b\w {4 ,}\ b"
     res = re . findall ( pat , text )
     return res
[/ python ]
### Task End ###

### Task Start ###
# These are the assertions for your function :
assert solution ([3 , 3, 3, 3, 3]) == 9

def solution ( lst ):
    """
    Given a non - empty list of integers , return the sum of all of the odd elements
     that are in even positions .
    Examples
    solution ([5 , 8, 7, 1]) == > 12
    solution ([3 , 3, 3, 3, 3]) == > 9
    solution ([30 , 13 , 24 , 321]) == >0
    """
    result = 0
    for i in range ( len ( lst )):
        if lst [i] % 2 == 0 and i % 2 == 0:
            result += lst [i]
    return result

With the above function , the assertion is ` assert solution ([3 , 3, 3, 3, 3]) == 9
` but the real execution output is ` 0 `.

Debug the program trace block by block until find the incorrect block . Every
block should have different feedbacks :
[ BLOCK -0]
     # lst =[3 , 3, 3, 3, 3]
     result = 0
     for i in range ( len ( lst )):
          if lst [i] % 2 == 0 and i % 2 == 0:
     # lst =[3 , 3, 3, 3, 3] result =0 i =0
[ BLOCK -1]
     # lst =[3 , 3, 3, 3, 3] result =0 i =0
     for i in range ( len ( lst )):
          if lst [i] % 2 == 0 and i % 2 == 0:
     # lst =[3 , 3, 3, 3, 3] result =0 i =1
[ BLOCK -2]
     # lst =[3 , 3, 3, 3, 3] result =0 i =1
     for i in range ( len ( lst )):
          if lst [i] % 2 == 0 and i % 2 == 0:
     # lst =[3 , 3, 3, 3, 3] result =0 i =2
[ BLOCK -3]
     # lst =[3 , 3, 3, 3, 3] result =0 i =2
     for i in range ( len ( lst )):
          if lst [i] % 2 == 0 and i % 2 == 0:
     # lst =[3 , 3, 3, 3, 3] result =0 i =3
[ BLOCK -4]
     # lst =[3 , 3, 3, 3, 3] result =0 i =3
     for i in range ( len ( lst )):
          if lst [i] % 2 == 0 and i % 2 == 0:
     # lst =[3 , 3, 3, 3, 3] result =0 i =4
[ BLOCK -5]
     # lst =[3 , 3, 3, 3, 3] result =0 i =4
     for i in range ( len ( lst )):
     return result
     # lst =[3 , 3, 3, 3, 3] result =0 i =4 _ret =0
[ debug ]
=================================== Completion ==================================
[ BLOCK -0]
Feedback : CORRECT . This block is correct . It initializes the result variable to
0.
[ BLOCK -1]
Feedback : INCORRECT . This block has an issue . It checks if the element at index `
i ` is even and if the index `i ` is even . However , the task description asks for
the sum of all of the odd elements that are in even positions . To fix the code ,
we should change the line `if lst [i] % 2 == 0 and i % 2 == 0: ` into `if lst [i] %
2 != 0 and i % 2 == 0: `.
[ BLOCK -2]
Feedback : INCORRECT . This block has an issue . It checks if the element at index `
i ` is even and if the index `i ` is even . However , the task description asks for
the sum of all of the odd elements that are in even positions . To fix the code ,
we should change the line `if lst [i] % 2 == 0 and i % 2 == 0: ` into `if lst [i] %
2 != 0 and i % 2 == 0: `.
[ BLOCK -3]
Feedback : INCORRECT . This block has an issue . It checks if the element at index `
i ` is even and if the index `i ` is even . However , the task description asks for
the sum of all of the odd elements that are in even positions . To fix the code ,
we should change the line `if lst [i] % 2 == 0 and i % 2 == 0: ` into `if lst [i] %
2 != 0 and i % 2 == 0: `.
[ BLOCK -4]
Feedback : INCORRECT . This block has an issue . It checks if the element at index `
i ` is even and if the index `i ` is even . However , the task description asks for
the sum of all of the odd elements that are in even positions . To fix the code ,
we should change the line `if lst [i] % 2 == 0 and i % 2 == 0: ` into `if lst [i] %
2 != 0 and i % 2 == 0: `.
[ BLOCK -5]
Feedback : CORRECT . This block is correct . It returns the result variable .
[/ debug ]
Please fix the Python code .
[ python ]
def solution ( lst ):
     """
     Given a non - empty list of integers , return the sum of all of the odd elements
      that are in even positions .

     Examples
     solution ([5 , 8, 7, 1]) == > 12
     solution ([3 , 3, 3, 3, 3]) == > 9
     solution ([30 , 13 , 24 , 321]) == >0
     """
     result = 0
     for i in range ( len ( lst )):
          if lst [i] % 2 != 0 and i % 2 == 0:
              result += lst [i]
     return result
[/ python ]
### Task End ###



                            Figure 9: Prompt for completion mode.
