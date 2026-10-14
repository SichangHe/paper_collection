                                                   Aligning Requirement for Large Language Model’s Code
                                                                        Generation
                                                                              Zhao Tian                                                                    Junjie Chen∗
                                                                 College of Intelligence and                                                       College of Intelligence and
                                                                Computing, Tianjin University                                                     Computing, Tianjin University
                                                                       Tianjin, China                                                                    Tianjin, China
                                                                   tianzhao@tju.edu.cn                                                               junjiechen@tju.edu.cn
                                        Abstract                                                                                    1   Introduction
                                        Code generation refers to the automatic generation of source code                           Code generation refers to the automatic generation of source code
                                        based on a given programming specification, which has garnered                              from a given programming specification. In recent years, it has
arXiv:2509.01313v2 [cs.SE] 6 Sep 2025




                                        significant attention particularly with the advancement of large                            attracted significant attention from both academia and industry due
                                        language models (LLMs). However, due to the inherent complexity                             to its potential to reduce repetitive programming tasks and improve
                                        of real-world problems, the LLM-generated code often fails to fully                         software development productivity [16, 30, 44, 52]. Advancements
                                        align with the provided specification. While state-of-the-art agent-                        in LLMs, such as DeepSeek-Coder [20] and Gemini [47], have led to
                                        based techniques have been proposed to enhance LLM code gener-                              substantial improvements in code generation [57]. However, LLMs
                                        ation, they overlook the critical issue of specification perception,                        still face significant challenges, particularly when handling complex
                                        resulting in persistent misalignment issues. Given that accurate                            requirements [38, 51, 59]. For example, even advanced GPT-4 [1]
                                        perception of programming specifications serves as the foundation                           generates code passing all test cases for only 12.10% of real-world
                                        of the LLM-based code generation paradigm, ensuring specification                           competitive programming problems[27]. These performance issues
                                        alignment is particularly crucial. In this work, we draw on software                        impede the practical application of LLMs, potentially compromising
                                        requirements engineering to propose Specine, a novel specifica-                             software quality [48, 50]. Therefore, enhancing the code generation
                                        tion alignment technique for LLM code generation. Its key idea                              performance of LLMs is critical.
                                        is to identify misaligned input specifications, lift LLM-perceived                              Recently, various prompt-based [32, 41, 51] and agent-based [13,
                                        specifications, and align them to enhance the code generation per-                          24, 59] techniques have been proposed to enhance the code genera-
                                        formance of LLMs. Our comprehensive experiments on four state-                              tion performance of LLMs. In general, these techniques share four
                                        of-the-art LLMs across five challenging competitive benchmarks                              main steps: (1) Perception, where the LLM is provided with a re-
                                        by comparing with ten state-of-the-art baselines, demonstrate the                           quirement specification and perceives its intent; (2) Planning, where
                                        effectiveness of Specine. For example, Specine outperforms the most                         the LLM employs diverse planing strategies (e.g., task decomposi-
                                        effective baseline, achieving an average improvement of 29.60%                              tion or algorithm selection) based on its specification perception;
                                        across all subjects in terms of Pass@1.                                                     (3) Implementation, where the LLM generates code based on the
                                                                                                                                    devised plan; (4) Repair, where the LLM leverages feedback (e.g.,
                                        CCS Concepts                                                                                test execution messages) to fix incorrect code. Among them, agent-
                                        • Software and its engineering → Automatic programming;                                     based code generation has emerged as the state-of-the-art [25, 34],
                                        • Computing methodologies → Natural language processing;                                    which utilizes specialized LLM agents to simulate the human soft-
                                        Neural networks.                                                                            ware development workflow. For example, Self-collaboration [13]
                                                                                                                                    enables LLMs to take on different roles (e.g., analyst, coder, and
                                        Keywords                                                                                    tester), each responsible for a specific sub-task in the development
                                                                                                                                    process. PairCoder [59], the state-of-the-art agent-based technique,
                                        Code Generation, Large Language Model, Agent, Requirements
                                                                                                                                    employs a navigator agent to explore diverse solution plans and a
                                        Engineering
                                                                                                                                    driver agent to repair implementations using execution feedback.
                                        ACM Reference Format:                                                                           However, existing LLM-based code generation techniques [13,
                                        Zhao Tian and Junjie Chen. 2026. Aligning Requirement for Large Language                    24, 32, 41] mainly focus on the latter three stages (i.e., planning,
                                        Model’s Code Generation. In 2026 IEEE/ACM 48th International Conference
                                                                                                                                    implementation, and repair), while overlooking a fundamental issue
                                        on Software Engineering (ICSE ’26), April 12–18, 2026, Rio de Janeiro, Brazil.
                                                                                                                                    in the first stage: the perception bias of LLMs towards the origi-
                                        ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3744916.3764572
                                                                                                                                    nal input specification. Specifically, LLMs may implicitly ignore or
                                        ∗ Junjie Chen is the corresponding author.                                                  misperceive key ingredients within the input specification, leading
                                                                                                                                    to generated code that deviates from the intended requirement.
                                        Permission to make digital or hard copies of all or part of this work for personal or       The difference between the original input specification and the actual
                                        classroom use is granted without fee provided that copies are not made or distributed
                                        for profit or commercial advantage and that copies bear this notice and the full citation   LLM-perceived specification is referred to as specification misalign-
                                        on the first page. Copyrights for third-party components of this work must be honored.      ment. Actually, inaccurate perception can limit the capability of
                                        For all other uses, contact the owner/author(s).
                                                                                                                                    optimizing the subsequent three stages in improving LLM-based
                                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil
                                        © 2026 Copyright held by the owner/author(s).                                               code generation, since it may fundamentally produce inaccuracies
                                        ACM ISBN 979-8-4007-2025-3/26/04
                                        https://doi.org/10.1145/3744916.3764572
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                               Zhao Tian and Junjie Chen


in the three stages (such as inaccurate planning). In addition, soft-
                                                                           1. Description: You have an array of integers (initially     1. Problem Background: The code is designed ...
ware requirements engineering research [7, 36, 46, 58] emphasizes          empty). You have to perform q queries. Each query is         2. Functional Requirements: The code performs
                                                                           of one of two types:                                         tasks based on the given two types of queries:
that effective software development must be built upon an accurate         "1 x": add the element x to the end of the array;            - Type 1 (`1 x`): Appends the current mapped value
perception of fundamental specifications. Therefore, within the cur-       "2 x y": replace all occurrences of x in the array with y.   of `x` to `arr`. If `x` has been remapped via a Type 2
                                                                           Find the resulting array after performing all queries.       query, the mapped value is used.
rent LLM-driven automated code generation paradigm, ensuring               2. Input Requirements: The first line contains a single      - Type 2 (`2 x y`): Updates the mapping of `x` to `y`.
                                                                           integer q (1 ≤ q ≤ 5 · 10^5) - the number of queries.        If any other values in `value_map` were mapped to
specification alignment is particularly critical. That is, addressing      3. Output Requirements: In a single line, print k            `x`, they are updated to point to `y` as well.
                                                                           integers - the resulting array after performing all the      3. Input Requirements: The first input line ...
the specification misalignment in LLM-based code generation is a           queries                                                      4. Output Requirements: A single line of ...
                                                                           4. Test Case Examples: {“Input”: “7\n1 3\n1 1\n2 1           5. Test Case Examples (Optional): {“Input”: ...
key direction.                                                             2\n1 2\n1 1\n1 2\n2 1 3\n”, “Output”: “3 2 2 3 2 \n”}        6. External APIs (Optional): The code uses ...
                                                                                                                                        7. Additional Explanation (Optional): The code ...
   In this paper, we propose Specine (Specification Alignment),                   ...
a novel specification alignment technique to enhance the code                 6
                                                                              7
                                                                                        if command == 1:
                                                                                            x = query[1]
                                                                              8             current_value= value_map.get(x, x)
generation performance of LLMs. Specifically, Specine automati-               9             arr.append(current_value)
                                                                              ...
cally identifies the misaligned specification, lifts the LLM-perceived     20 final_result = []
                                                                           21 for value in arr:
specification, and aligns it with the original input specification,        22 final_result.append(value_map.get(value, value))          [Input Specification]
                                                                              ...                                                       5. Aligned Specification Purpose: The problem...
thereby facilitating correct code generation. However, designing                                                                        The goal is to efficiently handle two types of queries:
                                                                                                                                        (1) Just add an element x to the end of the array.
an effective specification alignment technique presents the follow-        Example 1:
                                                                                                                                        (2) Replace all occurrences of element x with
                                                                                                                                        another element y immediately after each query.
                                                                           Test Input: “7\n1 3\n1 1\n2 1 2\n1 2\n1 1\n1 2\n2 1 3\n”
ing key challenges: (1) How to identify the misaligned ones from           Expected Output: “3 2 2 3 2 \n”
                                                                                                                                        The final task is to output the resulting array
                                                                                                                                        after all queries have been processed.
input specifications? Performing alignment on all cases can incur          Code Output: “3 3 2 2 2 \n”

unnecessary overhead, even may misprocess the originally-correct                                                                             ...
                                                                                  ...                                                    7         if parts[0] == 1:
                                                                            7           if parts[0] == '1':                              8             arr.append(parts[1])
cases. (2) How to obtain the actual LLM-perceived specification for         8               x = int(parts[1])                            9         elif parts[0] == 2:
                                                                            9               current_value=value_map.get(x, x)           10             x, y = parts[1], parts[2]
the misaligned one? Once a misaligned specification is identified,         10
                                                                              ...
                                                                                            arr.append(current_value)                   11             for i in range(len(arr)):
                                                                                                                                        12                if arr[i] == x:
explicitly extracting the actual LLM-perceived specification facili-       24 final_array = [value_map.get(val, val) for val in arr]
                                                                              ...
                                                                                                                                        13
                                                                                                                                             ...
                                                                                                                                                              arr[i] = y

tates the subsequent specification alignment. (3) How to align the
LLM-perceived specification to generate correct code? Designing com-       Figure 1: An example from Codeforces with GPT-4o-mini
prehensive and effective alignment rules is essential for aligning the
LLM-perceived specification with the original input specification,
thereby enhancing code generation performance.                            performance in terms of Pass@1 achieved by all the four LLMs with
   To address the first challenge, Specine implements a dual-agent        the 10 baselines is 55.67% (using the Gemini-1.5-Flash model with
component comprising a coder agent to generate the initial code           the TGen technique), but Specine achieves 65.33% based on the same
and a tester agent to estimate its correctness. The correctness of the    LLM. Also, we investigate the influence of the number of iterations,
generated code serves as an indicator of the LLM’s perception of the      a key hyper-parameter in the agent-based framework. Our results
input specification [22, 54]. If the specification is identified as po-   show that as the number of iterations increases, Specine consistently
tentially misaligned, Specine activates subsequent components for         outperforms all baselines. Furthermore, we construct five variants
specification alignment. To address the second challenge, Specine         of Specine for an ablation study, confirming the contribution of each
employs a novel specification lifting component that explicitly ex-       main component in Specine.
tracts the LLM-perceived specification for effective misalignment            The main contributions of this paper are summarized as follows:
analysis. This LLM-perceived specification is lifted from the low-
                                                                          • Novel Perspective: We propose a novel perspective for en-
level generated code using a domain-specific language (DSL) of
                                                                            hancing the code generation performance of LLMs through the
requirement specifications, providing a high-level standardized
                                                                            sophisticated specification alignment.
representation. To address the third challenge, Specine applies ten
                                                                          • Tool Implementation: We implement Specine following the
pre-defined alignment rules (derived from software requirements
                                                                            novel perspective, which consists of identifying misaligned input
engineering [11, 18, 19]) to systematically align different ingredi-
                                                                            specifications, lifting LLM-perceived specifications, and aligning
ents of the misaligned specification. In this way, Specine generates
                                                                            them to generate the correct code.
an aligned specification that is accurately perceived by the LLM,
                                                                          • Performance Evaluation: We conduct extensive experiments
ultimately enhancing its code generation performance.
                                                                            on four advanced LLMs across five challenging benchmarks by
   We conduct extensive experiments to evaluate Specine on four
                                                                            comparing with ten state-of-the-art baselines, demonstrating the
advanced LLMs (i.e., DeepSeek-Coder-1.5 [21], Qwen2.5-Coder [26],
                                                                            effectiveness of Specine in improving LLMs’ code generation.
GPT-4o-mini [42], and Gemini-1.5-Flash [47]) based on five chal-
                                                                          • Data Availability: We publicly release all accessible dataset and
lenging competitive program-solving benchmarks (i.e., APPS [23],
                                                                            our source code at the project homepage [40] to facilitate the
APPS-Eval [12], CodeContests-Raw [33], CodeContests [33], and
                                                                            experiment replication, future research, and practical adoption.
xCodeEval [31]). Our results demonstrate that Specine significantly
outperforms all 10 popular or state-of-the-art baselines across all
20 subjects (4 LLMs × 5 benchmarks), demonstrating our idea for           2              Motivating Example
enhancing LLM-based code generation by specification alignment.           To illustrate the key idea of specification alignment, we present
For example, the average improvement of Specine over all 10 base-         a real-world example to analyze the necessity of two key compo-
lines is 29.60%∼93.55% in terms of Pass@1 (measuring the ratio of         nents in Specine: specification lifting (Section 3.2) and specification
programming problems for which the generated code passes all test         alignment (Section 3.3). The necessity of identifying misaligned
cases) across all subjects. Particularly, on the APPS dataset, the best   specifications has been discussed in Section 1.
Aligning Requirement for Large Language Model’s Code Generation                                                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


   Start                                                                                                                                                         End


                                                                                                                                                         Yes
                                Tester                   Generated                Public                     Public Pass Ratio
                                                                                                                                               Passed?
                                Agent                    Test Cases             Test Cases                   Generated Pass Ratio
                                                                                                                                                                 Final
   Specification




                                                                                                                                                    No           Code
      Input




                                Coder                       Initial               Test                                           No
                                                                                                             Hierarchical
                                                                                                                                       # Iteration>N?
                                Agent                       Code                Execution                      Criteria                                    Yes

                                                                                                                                         #Iteration+=1




                               Aligned                      Aligner                            Lifted                                 Lifter
                             Specification                  Agent                           Specification                             Agent

                      Specification Background   Examples with Explanations
                      Specification Purpose      Edge/Corner Cases                     Initial Code                         Requirement
                      Key Concepts               APIs                                                                       Engineering
                      Input Requirement          Error Handling Requirements           Input Specification                     DSL
                      Output Requirement         Hints or Tips




                                                                Figure 2: Overview of Specine
   Figure 1 presents a real-world example from the Codeforces [9]                3     Approach
platform. In this example, we employ an advanced LLM (GPT-4o-                    In this paper, we present Specine, a novel specification alignment
mini [42]) with Zero-shot learning [6] to generate the initial code              technique designed to enhance the code generation performance
based on the input specification. However, due to the complexity                 of LLMs. Specifically, Specine automatically identifies misaligned
of this problem, the generated code is incorrect. Specifically, the              specifications, lifts LLM-perceived specifications, and aligns them
LLM fails to accurately perceive the “two query types” in the speci-             to generate correct code. Figure 2 provides an overview of Specine,
fication, leading to the corresponding error in the initial code. To             consisting of three main components: (1) Misaligned Specifica-
further investigate this issue, we applied the state-of-the-art Pair-            tion Identification (Section 3.1) employs a coder agent to gen-
Coder [59] to adjust diverse solution plans and repair the code using            erate initial code and a tester agent to estimate its correctness
execution feedback (shown in Figure 1). However, PairCoder’s code                to determine whether the LLM has correctly perceived the input
(shown in Figure 1) still exhibits the logical error. In contrast, by            specification. (2) Specification Lifting (Section 3.2) employs a
aligning the purpose behind the “two query types” (shown in the                  novel LLM-driven lifting strategy to explicitly extract high-level
aligned specification of Figure 1), the LLM successfully generates               perceived specifications from low-level generated code based on a
a correct implementation (i.e., final code in Figure 1). This moti-              pre-defined requirement DSL. (3) Specification Alignment (Sec-
vates the potential of improving LLM-based code generation through               tion 3.3) applies ten pre-defined alignment rules to systematically
specification alignment.                                                         align different ingredients of the misaligned specification, facilitat-
   Moreover, our natural attempt to directly instruct the LLM to                 ing the subsequent code generation. In the following, we provide a
align the specification is unsuccessful, still resulting in incorrect            detailed description of each component in Specine. Here, we reuse
code. In contrast, explicitly extracting the LLM-perceived specifi-              the real-world example introduced in Section 2 for illustration.
cation (i.e., lifted specification in Figure 1) enables the subsequent
generation of correct code. This is because Specine systematically               3.1    Misaligned Specification Identification
compares the lifted specification with the input specification, effec-
                                                                                 In Specine, identifying misaligned specifications is a critical step
tively analyzing specification misalignment for facilitating success
                                                                                 that evaluates whether the LLM correctly perceives the input spec-
alignment (i.e., the aligned specification in Figure 1). This motivates
                                                                                 ification. It is important to emphasize that the absence of this com-
the necessity of explicitly obtaining the LLM-perceived specification.
                                                                                 ponent would cause Specine to indiscriminately perform specifi-
   Although the specification lifting component effectively helps
                                                                                 cation alignment on all input specifications. This indiscriminate
analyze specification misalignment, mitigating this misalignment
                                                                                 processing could introduce significant drawbacks. First, for cor-
remains a significant challenge. To explore potential solutions,
                                                                                 rectly LLM-perceived input specifications, forced alignment may
we further instruct the LLM to generate ten candidate aligned
                                                                                 lead to erroneous modifications due to the inherent hallucination is-
specifications based on the lifted specification (as evaluated in
                                                                                 sues of LLMs, potentially transforming originally correct code into
the Specine𝑤𝑜𝐴𝑅 variant in RQ3). However, none of the generated
                                                                                 incorrect implementations. Second, such redundant alignment op-
specifications successfully address the misalignment, and thus the
                                                                                 erations impose unnecessary computational overhead, significantly
generated code remains incorrect. This motivates the necessity of
                                                                                 increasing both time and token consumption.
designing effective alignment rules for specification alignment, which
                                                                                     As shown in Figure 2, we design a dual-agent framework com-
can finally enhance LLM-based code generation.
                                                                                 prising a coder agent to generate the initial code (shown in Figure 1)
                                                                                 and a tester agent to generate test cases. The correctness of the
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                 Zhao Tian and Junjie Chen


                                                                                                               All Ingredients
                      Description:
                      Let's call a set of positive integers a_1, a_2, ..., a_k quadratic if the product of     Key Concepts
                                                                                                                                    Inspired by existing lifting research [3, 39, 61], we propose a
    Specification     the factorials of its elements is a square of an integer, i. e. ∏_{i=1}^{k} a_i! =           Rule
  Background Rule     m^2, for some integer m.                                                                                   novel lifter agent (illustrated in Figure 2) that lifts the generated
    Specification     You are given a positive integer n. Your task is to find a quadratic subset of a              APIs
    Purpose Rule      set 1, 2, ..., n of maximum size. If there are multiple answers, print any of them.           Rule         code into a DSL tailored for requirement specifications. Compared
                      Input Requirements:
        Input
  Requirements Rule
                      A single line contains a single integer n (1 ≤ n ≤ 10^6).                                Hints or Tips
                                                                                                                   Rule          to ordinary natural language descriptions, a requirement DSL pro-
                      Output Requirements:
       Output         In the first line, print a single integer - the size of the maximum subset. In the      Error Handling     vides a standardized representation of critical software require-
  Requirements Rule   second line, print the subset itself in an arbitrary order.                            Requirements Rule
                      Test Case Examples:                                                                                        ments, mitigating common issues such as ambiguity and incom-
   Examples with      {“Input”: [“1\n”, “4\n”,“7\n”,“9\n”], “Output”: [“1\n1”, “3\n1 3 4”,“4\n1 4 5            Edge/Corner
  Explanations Rule   6”,“7\n1 2 4 5 6 7 9”]}                                                                   Cases Rule       pleteness. Building on research in software requirements engineer-
                                                                                                                                 ing [3, 39, 61], we define a tailored requirement DSL for our task,
Figure 3: Correspondence between alignment rules and key                                                                         encompassing the following key attributes:
specification ingredients                                                                                                         {
                                                                                                                                      "Problem Background": "Describes the background and context of the code, providing the
generated code serves as an indicator of the LLM’s perception of                                                                       necessary background knowledge for understanding the code's functionality.",
                                                                                                                                      "Functional Requirements": "Summarizes the core functionality of the code, specifying its
the input specification [22, 54]. In particular, the tester agent in-                                                                  specific objectives or tasks, such as the problem being solved or the task being performed."
dependently generates test cases based on the input specification,                                                                    "Input Requirements": "Details the inputs required by the code, including input types,
                                                                                                                                       formats, and any constraints."
without relying on the initial code. This independence ensures the                                                                    "Output Requirements": "Specifies the outputs of the code, including output types, formats,
objectivity of test cases generation, mitigating any potential bias                                                                    and any constraints."
                                                                                                                                      "Test Case Examples": "Extracts the test cases included in the code, which are often used
introduced by erroneous initial code. Following the existing re-                                                                       to verify code correctness and serve as usage examples."
search [25], we carefully design a prompt to guide the tester agent                                                                   "External APIs": "Lists any external APIs or library functions used by the code and
                                                                                                                                       describes their purpose and interactions."
in generating effective test cases. The prompt details are as follows:                                                                "Additional Explanation": "Provides supplementary information, such as design intentions,
                                                                                                                                       potential limitations, or special considerations."
 [Input Specification]                                                                                                            }
 Instruction:Implement a representative set of test cases for the above specification, ensure
 that the generated test cases are correct:                                                                                      This highly standardized requirement DSL aligns with IEEE speci-
 (1) Basic Test Cases: To verify the fundamental functionality under normal conditions.
 (2) Edge Test Cases: To evaluate the function's behavior under extreme or unusual conditions.                                   fication standard [11], ensuring that the extracted lifted specifica-
 (3) Large-Scale Test Cases: To assess the function’s scalability with large data samples.                                       tion(shown in Figure 1) comprehensively and effectively represents
 Please provide additional test cases in a json format: ```json{"inputs": [], "outputs": []}```
                                                                                                                                 the LLM-perceived specification from the initial code. Furthermore,
    In practice, programming specifications commonly include pub-                                                                we discuss the scalability of the DSL design in Section 6.4, high-
lic test cases. To comprehensively assess the generated code, Specine                                                            lighting its potential to further enhance the generalizability and
combines these public test cases with the additional test cases gen-                                                             applicability of our approach.
erated by the tester agent. These test cases can help ensure the                                                                    Moreover, we design a prompt for the lifter agent that consists
reliability of this step for identifying misaligned specification. In                                                            of the initial code, the definition of requirement DSL, and a task
Section 5.3, we further explore the influence of public test cases and                                                           instruction (“Analyze the initial code exclusively and translate it
generated test cases on the effectiveness of Specine, respectively.                                                              as the lifted specification based on the defined requirement DSL.”).
Upon executing these test cases, Specine estimates the correctness                                                               Through LLM-driven specification lifting, the lifter agent gener-
of the initial code. If the code fails to pass all test cases, the in-                                                           ates the requirement DSL and parses it into a structured lifted
put specification is deemed misaligned, activating the subsequent                                                                specification template, thereby producing the final lifted specifica-
components for specification alignment. Conversely, if the code                                                                  tion. Particularly, our ablation results (in Section 5.3) demonstrate
successfully passes all test cases, it is considered the final output of                                                         that the specification lifting strategy significantly outperforms the
Specine. We acknowledge that the LLM-generated test cases may                                                                    commonly-used test execution feedback strategy in existing agent-
contain partial inaccuracies and cannot guarantee complete correct-                                                              based code generation techniques.
ness. Nevertheless, consistent with findings of prior studies [5, 34],
they still contribute to enhancing the overall performance of LLM                                                                3.3        Specification Alignment
code generation. A systematic discussion of this phenomenon will                                                                 The core idea of this component is to analyze potential misaligned
be presented in Section 6.3.                                                                                                     ingredients between the LLM-perceived specification (i.e., the lifted
                                                                                                                                 specification) and the input specification, and then mitigate these
3.2        Specification Lifting                                                                                                 misalignment using pre-defined alignment rules. Based on the ex-
After identifying misaligned input specifications based on the esti-                                                             isting studies in software requirements engineering [11, 18, 19], we
mated correctness of the generated code, it is essential to thoroughly                                                           define ten alignment rules that systematically align different kinds
analyze the detailed misalignment by comparing the generated code                                                                of ingredients in the misaligned specification (shown in Figure 3).
and the input specification, which can facilitate specification align-                                                           These alignment rules are detailed as follows:
ment (as discussed in Section 2). However, directly comparing and                                                                 • Specification Background: further explains the background,
analyzing the specification misalignment is inherently challenging                                                                   motivation, or domain-specific knowledge required by the speci-
due to the significant difference in abstraction levels between the                                                                  fication. This helps the LLM fully perceive the problem context
initial code (i.e., low-level programming language) and the input                                                                    for more accurate code generation.
specification (i.e., high-level requirement description). To effectively                                                          • Specification Purpose: emphasizes the detailed objective or
bridge this semantic gap, we design a specification lifting compo-                                                                   core tasks of the specification. This helps the LLM maintain focus
nent that explicitly extracts the LLM-perceived specification from                                                                   on the intended goal, reducing the likelihood of generating code
the generated code.                                                                                                                  that deviates from the required functionality.
Aligning Requirement for Large Language Model’s Code Generation                                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


• Key Concepts: identifies and explains the critical terminology            optimization process ensures stepwise improvements during speci-
  in the specification, ensuring that the LLM accurately perceives          fication alignment process. In the future, more sophisticated search
  the core terms and concepts, thereby minimizing code errors               algorithms could be integrated to further enhance this component.
  caused by conceptual misperception.                                          Besides, Specine terminates the alignment process once a pre-
• Input Requirements: emphasizes the input requirements of                  defined number of iterations (denoted as 𝑁 ) is reached, outputting
  the specification, including data types, formats, and constraints         the code with the highest hierarchical pass ratio. The number of
  (e.g., value ranges, size limits, or specific conditions). It helps the   iterations is a critical hyper-parameter for all agent-based tech-
  generated code correctly process input data.                              niques, and its impact will be discussed in Section 5.2. Through this
• Output Requirements: emphasizes the output requirements of                specification alignment component, Specine can effectively achieve
  the specification, including data types, formats, and constraints         specification alignment for generating correct code.
  (e.g., precision, delimiters, or sorting rules). It helps the generated
  code correctly produce the expected output.                               4     Evaluation Design
• Examples with Explanations: provides step-by-step analysis                Our study aims to addresses the following research questions (RQs):
  of test cases, illustrating the detailed logic from input to output.
  This enhances the LLM’s perception of the programming logic.              • RQ1: How does Specine perform in terms of effectiveness and
• Edge/Corner Cases: introduces three additional LLM-generated                efficiency compared to the state-of-the-art techniques?
  test cases covering extreme or boundary conditions to ensure              • RQ2: How do hyper-parameters affect Specine’s effectiveness?
  that the generated code handles unusual edge cases correctly.             • RQ3: How does each main component in Specine contribute to
• APIs: specifies external APIs or library functions relevant to the          the overall effectiveness?
  task, including their names and functionalities. This helps the
  LLM implement the required functions more effectively.                    4.1    Benchmarks
• Error Handling Requirements: defines the expected behav-                  To comprehensively evaluate Specine, we utilize five challenging
  ior when encountering invalid inputs, such as returning default           benchmarks in our study: APPS [23], APPS-Eval [12], CodeContests-
  values, raising exceptions, or applying special mechanisms. It en-        Raw [33], CodeContests [33], and xCodeEval [31]. These datasets
  sures the code behaves as expected in exceptional circumstances.          are commonly used in many existing LLM-based code generation
• Hints or Tips: provides optional implementation suggestions,              studies [27, 28, 51]. Notably, we do not include basic programming
  such as recommended algorithms or data structures. It serves as           datasets such as HumanEval [6] and MBPP [4], as LLMs already
  a supplementary guideline for addressing any remaining specifi-           achieve a Pass@1 exceeding 95% on these datasets with simple Zero-
  cation misalignment not covered by the preceding nine rules.              shot [15] setting. Instead, we select more challenging competition-
                                                                            level datasets to better assess the performance of Specine.
    Furthermore, Specine employs an LLM-based aligner agent to                 APPS consists of programming problems collected from various
facilitate specification alignment. Specifically, we design a prompt        competitive programming platforms (e.g., LeetCode [45]), including
for the aligner agent, which consists of the input specification,           5,000 training data and 5,000 test data. To balance the evaluation
the lifted specification, the ten pre-defined alignment rules, and          cost and conclusion generalizability, we randomly sample 300 prob-
a task instruction (“Analyze the input specification and the lifted         lems from test set based on the difficulty distribution, following
specification to identify misalignment or omissions. Select one             the existing work [41, 51]. Additionally, to improve the compre-
or more ingredients from the ten alignment rules to improve the             hensiveness of the evaluation, APPS is extended into APPS-Eval by
input specification.”). The aligner agent automatically generates the       constructing over 100 additional test cases for each problem.
aligned ingredients for the input specification, which collectively            CodeContests-Raw is proposed by Google DeepMind [10], con-
constitute the aligned specification (as shown in Figure 1).                sisting of 13,328 training data, 117 validation data, and 165 test
    In particular, the specification alignment is implemented as a          data. It is designed to evaluate the ability of LLMs to solve chal-
stepwise search process. In each iteration, Specine produces an             lenging programming problems. We also use the extended version,
aligned specification and subsequently uses it to generate new code.        CodeContests, which includes ∼190 additional test cases over the
To measure the quality of different versions of generated code,             raw version. Following existing studies [5, 62], we use all 165 test
we design a hierarchical criteria based on two pass ratios: (1) the         data from both CodeContests-Raw and CodeContests.
primary pass ratio, which measures the pass ratio of public test               xCodeEval is a competition-level multi-task benchmark, consist-
cases provided in the input specification, and (2) the secondary pass       ing of ∼7,500 programming problems and 25 million code examples
ratio, which measures the pass ratio of LLM-generated test cases.           collected from Codeforces [9]. To maintain consistency with APPS,
When comparing different code, the primary pass ratio is consid-            we randomly sample 300 problems from the code generation test
ered first; only if this ratio is identical is the secondary pass ratio     data based on the frequency distribution of difficulty levels.
considered. This hierarchical criterion prioritizes the primary pass           These datasets provide several public test cases (as part of the
ratio, as the correctness of public test cases is guaranteed, whereas       original specification), along with separate private test cases used
LLM-generated test cases may contain errors. Importantly, if the            for evaluating code correctness. Some studied baselines (including
new code generated from the current aligned specification achieves          Self-repair [41], 𝜇FiX [51], Self-collaboration [13], PairCoder [59],
a higher hierarchical pass ratio than the previous iteration (even          and TGen [37]) rely on the execution result of public test cases. How-
if it does not fully pass all test cases), Specine retains the current      ever, in APPS, public test cases are presented in natural language
aligned ingredients and proceeds to the next iteration. This greedy         within the original specification, rendering them non-executable.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                         Zhao Tian and Junjie Chen


Hence, for APPS, we randomly sample three test cases from private            provided by OpenAI [43] and Google AI [2]. These LLMs, which
test cases to serve as executable public test cases. To prevent result       have demonstrated excellent performance in code generation and
inflation due to potential test case leakage, we remove the three            are widely adopted [17, 53, 59], evaluate the generalizability of
cases from private test cases for performance evaluation.                    Specine to some extent. In our experiments, we set max tokens to
                                                                             1024 and temperature to 0.8 for all LLMs. The maximum number
4.2      Metrics                                                             of iterations 𝑁 is set to 10 for Specine and baselines. As LLMs often
Following existing studies [29, 51], we use Pass@𝑘 and AvgPassRatio          generate code that includes natural language text segments (e.g.,
to evaluate the effectiveness of Specine. Pass@𝑘 measures the func-          explanatory text), which can lead to compilation failures or execu-
tional correctness of the generated code. For a given programming            tion errors. Following existing studies [35, 51], we utilize a code
problem, the LLM generates 𝑘 code instances. If any of the instances         sanitizer tool [14] to preprocess the code generated by the LLMs. It
passes all the private test cases, the problem is considered solved.         can automatically detect and remove non-functional text segments
Pass@𝑘 is the percentage of problems solved out of the total num-            from the generated code.
ber of problems. As demonstrated by existing studies [8, 13, 38],
developers tend to consider the first code instance generated by             5 Results and Analysis
the LLM, and thus we set 𝑘 = 1 following existing work [34, 51, 59].         5.1 RQ1: Effectiveness and Efficiency
Note that Pass@1 is a stricter criterion, making improvements in
                                                                             5.1.1 Process: To answer RQ1, we apply Specine and 10 compared
this metric both challenging and practically meaningful. AvgPass-
                                                                             techniques to four studied LLMs. We then evaluate the effectiveness
Ratio measures the degree of correctness of the generated code on
                                                                             of each technique across five widely-used benchmarks in terms of
private test cases, and differs from Pass@𝑘 that evaluates whether
                                                                             Pass@1 and AvgPassRatio. In addition, we assess the efficiency of
the generated code is completely correct on private test cases. Avg-
                                                                             each technique in terms of time and token overhead.
PassRatio calculates the ratio of passing private test cases for each
problem, and then computes the average ratio across all problems.         5.1.2 Results: Table 1 shows the effectiveness and efficiency com-
Both metrics are largely complementary, higher Pass@𝑘 and Avg-            parison results of these techniques. First, we observe that, on aver-
PassRatio values indicate better effectiveness.                           age, agent-based code generation techniques outperform prompt-
   Additionally, we evaluate the efficiency of Specine by measur-         based code generation techniques in terms of Pass@1 and Avg-
ing both time overhead and token overhead (which includes prompt          PassRatio. This result confirms the effectiveness of the agent-based
token cost and generated token cost) following existing work [13,         framework and further motivates the design of our Specine.
24, 51]. Smaller values of time and token overhead indicate better            In particular, Specine achieves the best effectiveness among
efficiency in code generation.                                            all studied techniques, consistently demonstrating superior
                                                                          performance in both effectiveness metrics across all 20 sub-
4.3 Compared Techniques                                                   jects (4 LLMs × 5 benchmarks). Specifically, Specine significantly
To thoroughly evaluate Specine, we compare it with six representa-        improves all baselines by 29.60%∼93.55% and 27.95%∼79.12% in
tive or state-of-the-art agent-based techniques: Self-collaboration [13], terms of Pass@1 and AvgPassRatio on average across all subjects,
MetaGPT [24], AgentCoder [25], TGen [37], FlowGen [34], and               respectively. Furthermore, the Wilcoxon Signed-Rank Test [55] at a
PairCoder [59]. They share the same high-level insight, which             significance level of 0.05 confirms that all p-values are smaller than
simulates the software development process by designing diverse           2.40 × 10−7 , demonstrating the statistically significant superiority
agents. The primary difference among these techniques lies in the         of Specine over all baselines in terms of Pass@1 and AvgPassRatio.
roles assigned to agents and the distinct strategies to address cor-          In addition, prompt-based code generation techniques outper-
responding sub-tasks. Although our study focuses on agent-based           form agent-based techniques in terms of both efficiency metrics
techniques, for a more comprehensive evaluation of Specine, we            (i.e., time and token overhead). However, considering the significant
also compare it with four typical or state-of-the-art prompt-based        effectiveness of agent-based techniques, a certain degree of addi-
code generation techniques, including Zero-shot [6], SCoT [32],           tional cost is justified, illustrating their excellent balance of cost and
Self-repair [41], and 𝜇FiX [51]. Due to space limitations, more           effectiveness. Notably, our Specine achieves superior efficiency
details on these techniques can be found in their respective papers.      compared to all six agent-based baselines in terms of both
                                                                          efficiency metrics. Specifically, Specine improves all agent-based
4.4 Implementation Details                                                baselines by 22.44%∼39.14% and 9.69%∼46.89% in terms of time
                                                                          and token overhead on average across all subjects, respectively.
To evaluate the performance of Specine, we select a variety of
                                                                          Furthermore, the Wilcoxon Signed-Rank Test [55] at a significance
open-source and commercial LLMs for our study. For open-source
                                                                          level of 0.05 confirms that all p-values are smaller than 1.56 × 10−2 ,
LLMs, we chose two representative LLMs: Qwen-Coder [26] (ver-
                                                                          demonstrating the statistically significant superiority of Specine
sion qwen2.5-coder-7b-instruct) and DeepSeek-Coder [21] (version
                                                                          over all agent-based baselines in terms of time and token overhead.
deepseek-coder-7b-instruct-v1.5). Specifically, we download them
via the Huggingface [56] platform and deploy them in a local en-
vironment for our experiments. For commercial LLMs, we select             5.2 RQ2: Influence of Hyper-parameter
two widely-used and advanced LLMs: GPT-4o [42] (version gpt-4o-           5.2.1 Setup: The number of iterations is a key hyper-parameter in
mini-2024-07-18) and Gemini-1.5 [47] (version gemini-1.5-flash-002).      agent-based code generation techniques [25, 59]. In this research
We access these commercial LLMs through the respective APIs               question, we investigate the influence of the number of iterations
Aligning Requirement for Large Language Model’s Code Generation                                                   ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 1: Effectiveness and efficiency comparison in terms of Pass@1 (↑), AvgPassRatio (↑), Time Overhead (↓), and Token
Overhead (↓). APR is short for AvgPassRatio.
                                                  APPS             APPS-Eval        CodeContests-Raw CodeContests              xCodeEval          Time Token
 LLM                     Technique
                                                                                                                                                   (h)  (M)
                                              Pass@1    APR       Pass@1   APR      Pass@1     APR      Pass@1     APR      Pass@1       APR
                     Zero-shot                18.00%   34.25%      8.33%   33.35% 7.27%       14.78%     2.42%    13.02%     11.00%     24.77% 3.50         0.64
                     SCoT                     19.00%   35.95%      8.67%   34.82% 7.27%       16.75%     3.64%    14.25%     12.33%     25.21% 5.15         2.43
                     Self-repair              20.67%   38.38%      8.67%   36.23% 7.27%       17.33%     3.64%    14.73%     12.67%     26.65% 6.39         2.06
                     𝜇FiX                     23.00%   40.42%     10.67%   39.04% 9.70%       19.90%     4.24%    15.10%     13.33%     27.12% 18.94        6.29
                     Self-collaboration       23.00%   35.37%     10.33%   32.84% 9.70%       18.48%     4.24%    15.96%     13.33%     24.83% 87.21        18.48
 DeepSeek-Coder-v1.5 MetaGPT                  24.33%   38.27%     10.67%   34.84% 7.27%       13.79%     4.85%    12.52%     12.67%     20.88% 127.43       25.16
                     AgentCoder               21.67%   37.53%      9.33%   33.59% 9.09%       16.01%     4.24%    14.74%     12.00%     25.34% 108.80       15.67
                     TGen                     22.33%   36.34%     10.00%   33.37% 7.88%       17.41%     3.03%    13.79%     15.00%     27.88% 73.44        17.36
                     FlowGen                  23.67%   41.09%     10.67%   38.86% 9.70%       15.87%     4.24%    14.36%     15.33%     29.30% 110.95       20.43
                     PairCoder                23.67%   37.37%      9.67%   35.09% 10.30%      20.82%     4.24%    18.22%     13.33%     26.64% 75.99        16.93
                     Specine                  35.33%   59.62%     14.33%   50.99% 13.33%      28.67%     7.88%    30.16%     20.67%     45.58% 60.22        15.16
                         Zero-shot            19.67%   36.66%      9.33%   34.95%    7.88%    17.97%      5.45%   18.64%     10.67%     27.63% 3.23         0.54
                         SCoT                 21.67%   38.29%     10.00%   35.94%    8.48%    15.67%      6.06%   15.13%     11.33%     22.52% 6.62         2.37
                         Self-repair          21.67%   37.12%     10.00%   36.05%    8.48%    19.82%      6.06%   19.93%     12.00%     24.17% 5.54         1.54
                         𝜇FiX                 24.33%   39.34%     11.00%   41.43%   10.91%    22.57%      6.67%   20.97%     13.33%     27.92% 19.99        6.08
                         Self-collaboration   24.00%   35.88%     10.67%   33.24%    9.09%    20.82%      7.27%   22.21%     12.33%     27.08% 62.60        15.75
 Qwen2.5-Coder           MetaGPT              23.33%   36.04%     11.00%   33.78%    9.70%    18.17%      7.27%   19.38%     11.33%     23.92% 110.45       25.54
                         AgentCoder           24.33%   38.06%     11.33%   33.76%   12.12%    22.36%      9.09%   22.52%     14.33%     28.27% 139.57       16.90
                         TGen                 26.33%   37.10%     11.00%   31.75%    9.09%    13.62%      6.06%   12.11%     14.33%     22.21% 74.42        17.11
                         FlowGen              25.33%   38.61%     10.00%   34.60%    8.48%    15.60%      6.67%   14.87%     12.00%     24.72% 108.02       21.98
                         PairCoder            30.33%   50.20%     11.67%   42.18%   13.94%    29.07%      9.09%   25.53%     16.00%     37.33% 84.81        15.64
                         Specine              37.67%   60.63%     16.67%   51.53%   15.15%    32.44%     10.30%   34.11%     18.67%     42.09% 51.20        14.38
                         Zero-shot            33.67%   43.61%     13.33%   41.38%    8.48%    18.16%      4.85%   17.96%     23.67%     32.82%     1.67     0.61
                         SCoT                 35.33%   46.52%     14.33%   43.03%   11.52%    23.73%      6.06%   22.00%     25.00%     33.68%     1.43     2.46
                         Self-repair          36.67%   47.01%     14.67%   43.24%   10.30%    19.94%      6.67%   20.66%     25.67%     34.88%      1.97    1.63
                         𝜇FiX                 40.33%   49.31%     15.67%   46.15%   12.12%    25.53%      9.09%   23.21%     28.67%     38.95%      5.62    6.55
                         Self-collaboration   42.00%   55.19%     16.33%   48.25%   14.55%    27.04%     10.91%   25.72%     30.67%     45.48%     31.40    17.00
 GPT-4o-mini             MetaGPT              41.33%   49.90%     16.33%   45.83%   12.12%    25.69%      9.70%   25.78%     26.00%     35.14%     32.90    27.20
                         AgentCoder           41.33%   49.16%     16.67%   44.21%   15.76%    26.58%     10.30%   26.48%     26.00%     33.46%     28.71    16.84
                         TGen                 41.00%   47.16%     16.67%   42.62%    9.09%    13.17%      7.88%   12.82%     30.67%     37.58%     48.21    18.32
                         FlowGen              43.67%   52.32%     17.00%   45.43%   12.12%    21.43%      9.09%   19.35%     30.00%     38.00%     32.70    21.33
                         PairCoder            49.00%   63.68%     19.67%   56.02%   18.79%    34.14%     11.52%   31.88%     31.67%     46.06%     29.87    16.71
                         Specine              56.33%   72.98%     22.67%   63.55%   23.64%    40.65%     17.58%   42.10%     38.67%     57.34%     24.62    14.41
                         Zero-shot            47.67%   59.33%     19.67%   51.65%   29.09%    39.30%     23.64%   33.49%     27.00%     41.44%      1.10    0.50
                         SCoT                 48.67%   59.51%     20.67%   51.10%   30.30%    40.08%     25.45%   35.05%     28.00%     41.26%      1.13    2.22
                         Self-repair          49.33%   60.14%     21.33%   52.71%   32.33%    42.64%     25.45%   36.71%     29.33%     42.72%      1.50    0.99
                         𝜇FiX                 51.33%   62.05%     22.33%   56.69%   34.39%    44.22%     28.48%   40.93%     31.00%     44.10%      4.08    5.10
                         Self-collaboration   54.33%   66.28%     22.67%   54.89%   36.97%    49.11%     30.30%   43.13%     31.67%     46.19%     21.74    10.71
 Gemini-1.5-Flash        MetaGPT              55.00%   65.31%     22.67%   53.60%   35.76%    45.68%     28.48%   40.34%     29.00%     35.21%     21.74    22.79
                         AgentCoder           53.33%   60.51%     22.33%   51.23%   42.42%    50.90%     32.73%   47.17%     30.67%     37.55%     20.22    13.83
                         TGen                 55.67%   68.96%     23.33%   58.76%   36.97%    50.06%     26.67%   42.82%     34.00%     47.12%     42.36    10.43
                         FlowGen              53.33%   63.15%     21.67%   51.01%   40.00%    54.31%     31.52%   48.92%     29.67%     42.14%     22.22    13.89
                         PairCoder            55.00%   68.47%     23.00%   56.82%   43.03%    54.42%     30.91%   47.05%     32.33%     46.72%     21.70    10.46
                         Specine              65.33%   78.15%     29.33%   65.91%   44.85%    56.96%     36.36%   54.34%     38.67%     58.42%     17.61    9.77

(i.e., 𝑁 ) on the effectiveness of Specine. Specifically, for 1 ≤ 𝑁 ≤ 10,           in effectiveness for both Pass@1 and AvgPassRatio. However, across
we evaluate the performance of Specine alongside six agent-based                    all iteration settings, Specine consistently outperforms all baselines,
baselines across all 20 subjects (4 LLMs × 5 benchmarks) in terms                   achieving 27.29%∼42.86% higher Pass@1 and 25.86%∼68.22% higher
of Pass@1 and AvgPassRatio.                                                         AvgPassRatio on average across all subjects. This demonstrates
                                                                                    the stable superiority of Specine across different iteration settings.
5.2.2 Results: Figure 4 illustrates the variation in Pass@1 across                  Furthermore, the Wilcoxon Signed-Rank Test [55] at a significance
different agent-based techniques as the number of iterations in-                    level of 0.05 confirms that all p-values are smaller than 1.09 × 10−4 ,
creases. Due to space limitations, we put the results for AvgPassRa-                demonstrating the statistically significant superiority of Specine
tio on our homepage [40]. First, we observe that as the number of it-               under varying iteration settings.
erations increases, all agent-based techniques exhibit improvements
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                Zhao Tian and Junjie Chen


                                   Self-collaboration           MetaGPT         AgentCoder                TGen         FlowGen                  PairCoder           Specine
     40%   DeepSeek, APPS                 16%    DeepSeek, APPS-Eval      15%     DeepSeek, CodeContests-Raw     10%   DeepSeek, CodeContests               25%   DeepSeek, xCodeEval
     35%                                  14%                                                                     8%                                        20%
Pass@1




     30%
                                          12%                             10%                                     6%
     25%                                                                                                                                                    15%
     20%                                  10%                                                                     4%
     15%                                   8%                             5%                                      2%                                        10%
           1 2 3 4 5 6 7 8 9 10                 1 2 3 4 5 6 7 8 9 10             1 2 3 4 5 6 7 8 9 10                  1 2 3 4 5 6 7 8 9 10                       1 2 3 4 5 6 7 8 9 10
     40%   Qwen, APPS                     18%    Qwen, APPS-Eval          20%     Qwen, CodeContests-Raw         12%   Qwen, CodeContests                   20%   Qwen, xCodeEval
     35%                                  16%                                                                    10%
                                                                          15%
Pass@1




                                          14%
     30%                                                                                                          8%                                        15%
                                          12%                             10%
     25%                                  10%                                                                     6%
     20%                                   8%                             5%                                      4%                                        10%
         1 2 3 4 5 6 7 8 9 10     1 2 3 4 5 6 7 8 9 10                           1 2 3 4 5 6 7 8 9 10                  1 2 3 4 5 6 7 8 9 10                       1 2 3 4 5 6 7 8 9 10
     60% GPT, APPS            25% GPT, APPS-Eval                                  GPT, CodeContests-Raw          20%   GPT, CodeContests                          GPT, xCodeEval
     55%                                                                  25%                                                                               40%
     50%                      20%                                         20%                                    15%                                        35%
Pass@1




     45%                                                                  15%                                    10%                                        30%
     40%                      15%
     35%                                                                  10%                                     5%                                        25%
     30%                      10%                                          5%                                     0%                                        20%
         1 2 3 4 5 6 7 8 9 10     1 2 3 4 5 6 7 8 9 10                           1 2 3 4 5 6 7 8 9 10                  1 2 3 4 5 6 7 8 9 10                       1 2 3 4 5 6 7 8 9 10
     70% Gemini, APPS                                                                                            40%
     65%                      30% Gemini, APPS-Eval                       45%     Gemini, CodeContests-Raw             Gemini, CodeContests                 40%   Gemini, xCodeEval
                                                                          40%                                    35%
Pass@1




     60%                      25%                                                                                                                           35%
                                                                          35%                                    30%
     55%
     50%                      20%                                         30%                                    25%                                        30%
     45%                      15%                                         25%                                    20%                                        25%
         1 2 3 4 5 6 7 8 9 10     1 2 3 4 5 6 7 8 9 10                           1 2 3 4 5 6 7 8 9 10                  1 2 3 4 5 6 7 8 9 10                       1 2 3 4 5 6 7 8 9 10
                    # iterations                          # iterations                     # iterations                          # iterations                              # iterations

                                         Figure 4: Influence of the number of iterations (𝑁 ) in terms of Pass@1 (↑)
   In addition, the improvement achieved by increasing the number                                    For the specification lifting component, existing agent-based
of iterations in Specine surpasses that of all baselines. Specifically,                           code generation techniques typically rely on the coarse-grained
as 𝑁 increases from 1 to 10, Specine achieves an average improve-                                 execution results of test cases as feedback to repair incorrect code.
ment of 47.97% in terms of Pass@1 across all subjects, whereas                                    In contrast, Specine employs specification lifting to obtain finer-
other baselines show an average improvement of 13.27%∼45.40%.                                     grained feedback messages. To assess the effectiveness of this
Similarly, for the AvgPassRatio metric, Specine demonstrates an                                   component, we replace the specification lifting strategy with a
average improvement of 37.02%, while other baselines achieve an                                   test-execution feedback strategy (introduced in Self-repair [41]),
average improvement of 9.97%∼35.87%.                                                              resulting in a variant of Specine called Specine𝑤𝑇 𝐹 . Specifically,
   In particular, these baselines appear to reach an effectiveness                                Specine𝑤𝑇 𝐹 utilizes test-execution feedback messages as input for
plateau after a certain number of iterations, such as when 𝑁 ≥ 3                                  the subsequent aligner agent to align the specification.
on APPS with DeepSeek-Coder. In contrast, Specine consistently                                       For the specification alignment component, we evaluate the con-
exhibits an upward trajectory across all iterations on almost all sub-                            tributions of both the aligner agent and pre-defined alignment rules
jects, demonstrating its ability to leverage additional iterations for                            by constructing two additional variants of Specine: Specine𝑤𝑜𝐴
continuous improvement in effectiveness. This is because Specine’s                                and Specine𝑤𝑜𝐴𝑅 . In Specine𝑤𝑜𝐴 , we remove the aligner agent and
specification lifting component keeps improving alignment over                                    randomly select pre-defined alignment rules for specification align-
time. Even when early iterations do not achieve perfect alignment,                                ment. In Specine𝑤𝑜𝐴𝑅 , we eliminate the pre-defined alignment rules
Specine can extract detailed information from newly generated code                                and instead provide a task instruction that guides the aligner agent
to progressively refine the LLM-perceived specification. In contrast,                             to directly generate the aligned specification.
existing baselines rely primarily on coarse test feedback, which is
less informative and may even lead to regression issues. We hypoth-                               5.3.2 Results: Table 2 shows the comparison results between Specine
esize that increasing the number of iterations may further enhance                                and its five variants across all 20 subjects (4 LLMs × 5 benchmarks)
Specine’s performance; however, this entails a trade-off between                                  in terms of Pass@1 and AvgPassRatio. Firstly, Specine consistently
effectiveness and computational cost.                                                             outperforms both Specine𝑤𝑜𝑃𝑇𝐶 and Specine𝑤𝑜𝑇 in terms of both
                                                                                                  metrics. On average, Specine improves 17.59% and 12.41% higher
                                                                                                  Pass@1 than Specine𝑤𝑜𝑃𝑇𝐶 and Specine𝑤𝑜𝑇 , and 25.12% and 11.84%
                                                                                                  higher AvgPassRatio, respectively. These results confirm the effec-
5.3        RQ3: Contribution of Main Components                                                   tiveness of incorporating both public test cases and LLM-generated
5.3.1 Variants: Specine consists of three main components: mis-                                   test cases in Specine. Additionally, Specine𝑤𝑜𝑇 demonstrates supe-
aligned specification identification, specification lifting, and speci-                           rior effectiveness over Specine𝑤𝑜𝑃𝑇𝐶 , achieving average improve-
fication alignment. To investigate the contribution of each compo-                                ments of 4.27% and 10.20%, respectively. This underscores the ne-
nent, we construct five variants of Specine for evaluation.                                       cessity of our hierarchical criteria (introduced in Section 3.3), which
   For the misaligned specification identification component, we                                  confirms that while public test cases are typically more reliable,
utilize both public test cases and LLM-generated test cases to assess                             LLM-generated test cases may introduce errors. Moreover, prior
the correctness of the initial code. To investigate separately the                                studies [37, 51, 59] have suggested that including public test cases
contribution of these two types of test cases, we construct two                                   within specifications is a common practice. However, Specine𝑤𝑜𝑃𝑇𝐶
variants of Specine: namely Specine𝑤𝑜𝑃𝑇𝐶 and Specine𝑤𝑜𝑇 , where                                   addresses a more challenging scenario where no public test cases
public test cases and the tester agent are removed, respectively.                                 are available. The experimental results show that Specine𝑤𝑜𝑃𝑇𝐶 still
Aligning Requirement for Large Language Model’s Code Generation                                           ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 2: Comparison between Specine and its variants in terms of Pass@1 (↑) and AvgPassRatio (↑). APR is short for AvgPassRatio.
                                                    APPS             APPS-Eval       CodeContests-Raw       CodeContests                xCodeEval
  LLM                      Technique
                                              Pass@1       APR     Pass@1   APR      Pass@1      APR      Pass@1         APR        Pass@1         APR
                           Specine𝑤𝑜𝑃𝑇 𝐶      29.67%      46.70%   12.00%   41.41%   11.52%     22.10%      6.06%      18.89%        17.33%       32.52%
                           Specine𝑤𝑜𝑇         32.00%      54.82%   13.33%   48.42%   11.52%     23.47%      6.06%      25.04%        16.00%       36.93%
  DeepSeek-Coder-v1.5      Specine𝑤𝑇 𝐹        29.67%      53.25%   13.00%   48.03%   11.52%     24.80%      5.45%      24.44%        16.33%       36.63%
                           Specine𝑤𝑜𝐴         29.00%      52.02%   12.33%   45.93%   10.91%     22.15%      4.85%      23.83%        16.00%       35.71%
                           Specine𝑤𝑜𝐴𝑅        23.33%      40.80%   10.67%   38.65%    9.70%     18.85%      4.24%      16.62%        14.00%       29.27%
                           Specine            35.33%      59.62%   14.33%   50.99%   13.33%     28.67%      7.88%      30.16%        20.67%       45.58%
                           Specine𝑤𝑜𝑃𝑇 𝐶      31.33%      49.39%   13.33%   45.30%   12.73%     25.04%      9.09%      24.64%        16.00%       34.01%
                           Specine𝑤𝑜𝑇         33.33%      55.88%   15.00%   47.54%   13.94%     29.73%      9.09%      26.95%        15.67%       35.91%
  Qwen2.5-Coder            Specine𝑤𝑇 𝐹        32.67%      55.87%   14.67%   49.33%   13.94%     30.12%      8.48%      27.45%        15.00%       33.77%
                           Specine𝑤𝑜𝐴         32.00%      55.18%   13.67%   48.04%   13.33%     29.85%      7.88%      26.98%        14.33%       32.14%
                           Specine𝑤𝑜𝐴𝑅        24.00%      47.33%   11.33%   44.13%   13.33%     29.65%      7.27%      27.08%        13.67%       34.06%
                           Specine            37.67%      60.63%   16.67%   51.53%   15.15%     32.44%     10.30%      34.11%        18.67%       42.09%
                           Specine𝑤𝑜𝑃𝑇 𝐶      51.00%      62.31%   20.33%   56.34%   17.58%     28.58%     13.33%      30.02%        33.67%       46.98%
                           Specine𝑤𝑜𝑇         53.00%      68.74%   20.67%   59.95%   22.42%     39.00%     14.55%      34.27%        34.33%       49.37%
  GPT-4o-mini              Specine𝑤𝑇 𝐹        52.00%      67.76%   21.00%   60.07%   21.82%     38.56%     15.15%      37.07%        35.00%       49.33%
                           Specine𝑤𝑜𝐴         50.33%      65.24%   20.33%   57.46%   20.61%     37.29%     13.33%      35.19%        34.00%       48.07%
                           Specine𝑤𝑜𝐴𝑅        42.67%      56.53%   18.33%   52.06%   21.82%     38.44%     12.73%      34.28%        30.67%       46.18%
                           Specine            56.33%      72.98%   22.67%   63.55%   23.64%     40.65%     17.58%      42.10%        38.67%       57.34%
                           Specine𝑤𝑜𝑃𝑇 𝐶      59.67%      70.91%   24.67%   61.08%   41.21%     51.51%     33.33%      45.86%        37.00%       52.10%
                           Specine𝑤𝑜𝑇         61.67%      74.14%   27.67%   63.59%   43.03%     56.62%     34.55%      49.60%        34.00%       52.01%
  Gemini-1.5-Flash         Specine𝑤𝑇 𝐹        60.67%      71.72%   27.33%   60.78%   41.82%     53.93%     31.52%      43.64%        36.33%       52.32%
                           Specine𝑤𝑜𝐴         59.00%      70.22%   24.33%   59.35%   40.61%     53.71%     30.91%      43.08%        35.33%       51.93%
                           Specine𝑤𝑜𝐴𝑅        54.33%      66.91%   23.00%   57.93%   38.79%     49.37%     29.70%      42.11%        31.00%       46.78%
                           Specine            65.33%      78.15%   29.33%   65.91%   44.85%     56.96%     36.36%      54.34%        38.67%       58.42%

outperforms all 10 baselines, even those leveraging public test cases,        6 Discussion
with average improvements of 7.37%∼48.25% and 2.17%∼33.15% in
                                                                              6.1 Case Study
terms of Pass@1 and AvgPassRatio, respectively. This highlights
the generalizability of Specine, demonstrating its effectiveness even         During the alignment process, Specine outputs intermediate aligned
in practical settings where public test cases are unavailable.                specifications, enabling systematic analysis of its iterative align-
   Secondly, Specine demonstrates superior performance compared               ment process. We present a case study using CodeContests bench-
to Specine𝑤𝑇 𝐹 , achieving average improvements of 14.75% and                 mark and Gemini-1.5 (shown in Figure 5). The quality of the aligned
12.95% in terms of Pass@1 and AvgPassRatio, respectively. These               specification is quantitatively evaluated based on the code correct-
results validate the contribution of the specification lifting com-           ness with private test cases: (1) Initially, the LLM generates code
ponent and further confirm that it outperforms the test-execution             solely from the input specification, achieving a 0% pass ratio, in-
feedback strategy commonly employed by existing agent-based                   dicating that the LLM fails to correctly perceive the specification.
techniques. In the future, we aim to further explore the integration          (2) Specine leverages the specification purpose rule to generate an
of our specification lifting strategy to enhance the effectiveness of         aligned specification, improving the pass ratio to 77.56%, demon-
existing agent-based code generation techniques.                              strating that this alignment rule enhances the LLM’s perception.
   Thirdly, Specine outperforms both Specine𝑤𝑜𝐴 and Specine𝑤𝑜𝐴𝑅               Consequently, this alignment rule is retained. (3) In the next itera-
with average improvements of 20.94% and 34.57% in terms of Pass@1,            tion, Specine incorporates the input requirements rule, increasing
and 16.49% and 28.75% in terms of AvgPassRatio, respectively. These           the pass ratio to 80.00%, confirming its contribution. (4) Subsequent
results confirm the necessity of the specification alignment compo-           iterations yield no further improvements, leading to the removal
nent in Specine. Moreover, Specine𝑤𝑜𝐴𝑅 demonstrats the weakest                of ineffective alignment rules. (5) By the sixth iteration, Specine
performance among all variants, further underscoring the signif-              incorporates the hints or tips rule, achieving a 100.00% pass ratio,
icance of the ten alignment rules derived from software require-              indicating that the LLM fully perceives the final aligned specifica-
ments engineering, which contribute the most substantially to the             tion. This provides a clear illustration of how Specine’s iterative
overall effectiveness of Specine.                                             alignment mechanism enhances the LLM perception, ultimately
   Furthermore, the Wilcoxon Signed-Rank Test [55] at a significance          improving code generation performance.
level of 0.05 confirms that all p-values are smaller than 1.77 × 10−7 ,          To better understand the limitations of Specine, we conduct a
exhibiting the statistically significant advantage of Specine over            manual analysis of 60 representative failure cases, sampled across
all variants. Overall, each of the main components contributes                four LLMs and five benchmarks. The analysis reveals that most
substantially to the overall effectiveness of Specine.                        failures are attributed to (1) suboptimal test cases generated by the
                                                                              tester agent (23 cases) and (2) incorrect application of alignment
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                            Zhao Tian and Junjie Chen


                                                                                                             25%
      1. Description: Monocarp is playing yet another computer game. In this game, his character has ...     20%             13.54%      9.05% 11.59% 14.48% 8.42%
      2. Input Requirements: The first line contains a single integer t (1 ≤ t ≤ 1000) - the number of ...
      3. Output Requirements: For each test case, print a single integer - the minimum value of ...          15%
      4. Test Case Examples: {“Input”: “3\n2 5\n1 5\n3 10\n2 4 10\n5 3\1 2 4 5 7”, “Output”: “3\n4\n1”}                          6.70%                               6.46% 7.27%
                                                                                                             10%     5.64%                                                         5.56%
      [Input Specification]                                                                                   5%
      5. Aligned Specification Purpose: The program determines the minimum poison duration (`k`)
      needed to kill a dragon with `h` hit points. The player attacks the dragon at times `a_i` ...




                                                                                                                                    Is
                                                                                                                      Sp und n

                                                                                                                             ose ion




                                                                                                                      Ed tions ith

                                                                                                                                     r




                                                                                                                              nts g
                                                                                                                              Tip s
                                                                                                                           ses rne




                                                                                                                           me lin
                                                                                                                                   o




                                                                                                                          or Hint

                                                                                                                                AP
                                                                                                                  Re I s

                                                                                                                  Re O nts




                                                                                                                                  s
                                                                                                                  Ex xam ts
                                                                                                                          gro ati




                                                                                                                           nc y




                                                                                                                         na s w
                                                                                                                         rp at


                                                                                                                                 t



                                                                                                                        ire ut
                                                                                                                        Co Ke




                                                                                                                       ire nd
                                                                                                                              ep




                                                                                                                   E men
                                                                                                                        ire ut




                                                                                                                       Cae/Co
                                                                                                                      ck fic

                                                                                                                      Pu ific




                                                                                                                            me
                                                                                                                    qu utp

                                                                                                                     pla ple
                                                                                                                     qu np




                                                                                                                   qu Ha
                                                                                                                   Ba peci


                                                                                                                           c
      [Input Specification]




                                                                                                                         g
                                                                                                                         e




                                                                                                                 Re rror
                                                                                                                      S
      5. Aligned Specification Purpose: The program determines the minimum poison duration (`k`)




                                                                                                                  E
      needed to kill a dragon with `h` hit points. The player attacks the dragon at times `a_i` ...
      6. Aligned Input Requirements: The input consists of `t` cases. Each case begins with two
      integers: `n`(1 ≤ n ≤ 100), representing the number of attacks, and `h` (1 ≤ h ≤ 10^{18}) ...              Figure 6: Effectiveness of each alignment rule in Specine

      [Input Specification]
      5. Aligned Specification Purpose: The program determines the minimum poison duration (`k`)
                                                                                                             solution. Specifically, the accuracy of LLM-generated test cases is
      needed to kill a dragon with `h` hit points. The player attacks the dragon at times `a_i` ...          60.17%∼72.92% on average across different LLMs and benchmarks,
      6. Aligned Input Requirements: The input consists of `t` cases. Each case begins with two
      integers: `n` (1 ≤ n ≤ 100), representing the number of attacks, and `h` (1 ≤ h ≤ 10^{18}) ...         indicating that a non-negligible proportion of LLM-generated test
      7. Aligned Hints or Tips: Use binary search to find the minimum `k`. The search space for
      `k` is[1, h]. For a given `k`, calculate the total damage inflicted by summing the durations ...
                                                                                                             cases contain errors. We acknowledge that the presence of incor-
                                                                                                             rectly generated test cases is a general challenge for all LLM-based
                                                                                                             approaches, primarily due to inherent limitations in LLM perfor-
   Figure 5: Case study on CodeContests with Gemini-1.5
                                                                                                             mance. Moreover, the accuracy of the generated test cases exceeds
rules by the aligner agent (25 cases). A smaller subset (12 cases)                                           50%, with the proportion of correct test cases surpassing that of
involves inaccurate lifted specifications produced by the lifter agent.                                      incorrect ones. Therefore, this facilitates prioritization of correct
These findings highlight opportunities for further enhancement. In                                           code, as it exhibits a higher pass ratio on LLM-generated test cases
future work, we plan to enhance the robustness of the tester agent                                           than incorrect code, aligning with the voting principle. Our abla-
by incorporating specification alignment into the test generation                                            tion study on Specine𝑤𝑜𝑃𝑇𝐶 further confirms that LLM-generated
process and introducing test case validation mechanisms. For the                                             test cases significantly enhance the overall effectiveness of Specine,
aligner agent, we intend to develop more effective alignment rules                                           providing empirical evidence of their contribution. Similar findings
to mitigate specification misalignment.                                                                      have been reported in CodeT [5] and FlowGen [34]. To further
                                                                                                             relieve this challenge, we introduce a hierarchical pass ratio crite-
6.2       Influence of Alignment Rules                                                                       rion (in Section 3.3) that prioritizes the results of reliable public
                                                                                                             test cases. This helps mitigate the negative impact of erroneous
We further analyze the influence of each alignment rule (as defined
                                                                                                             LLM-generated test cases to some extent. In future work, we aim
in Section 3.3). Specifically, for each programming problem, if a
                                                                                                             to develop more advanced test case generation techniques, such as
specific alignment rule leads to an improvement in the test pass
                                                                                                             incorporating type checking and test coverage to guide LLM-based
ratio of generated code, it is considered an effective alignment rule
                                                                                                             test generation, further improving the effectiveness of Specine.
for that problem. Based on this criterion, we evaluate the contri-
bution of each alignment rule across all programming problems,
considering all four LLMs and five benchmarks (as illustrated Fig-                                           6.4     Scalability of DSL
ure 6). The results demonstrate that, on average, all alignment rules                                        While our current evaluation focuses on structured programming
contribute to aligning more than 5% of all programming problems,                                             tasks, the DSL design in our Specine is designed to be modular and
further strengthening their necessity. Additionally, we observe that                                         extensible. The core principle of Specine, which involves abstracting
the three most effective alignment rules are Examples with Ex-                                               LLM-generated code into a structured and semantically rich repre-
planations, Specification Purpose, and Output Requirements, which                                            sentation to improve alignment with user intent, is broadly applica-
successfully align an average of 14.48%, 13.54%, and 11.59% of all                                           ble beyond competitive programming. The current schema builds
programming problems, respectively. This finding suggests that                                               on established foundations in requirements engineering [18, 19] and
developers should focus on improving these three aspects when                                                aligns with IEEE specification standard [11], ensuring wide applica-
writing programming specifications for LLMs in code generation. In                                           bility across diverse code generation scenarios. It can be extended to
the future, we plan to design additional alignment rules (e.g., perfor-                                      incorporate domain-specific ingredients (e.g., UI layout constraints
mance, security, and deployment requirements) to further enhance                                             in front-end development, data schemas in analytics) without mod-
Specine’s effectiveness in handling more complex problems.                                                   ifying the overall alignment pipeline. In future work, we plan to
                                                                                                             investigate the use of advanced LLMs to generate DSL schemas
6.3       Quality of LLM-Generated Test Cases                                                                tailored to new domains, with refinement via expert knowledge.
The quality of LLM-generated test cases directly impacts the effec-
tiveness of Specine. To comprehensively evaluate test case quality,                                          7     Threats and Validity
we verify their correctness against the canonical solutions pro-                                             The threat to construct validity mainly lies in the inherent ran-
vided in the dataset follow existing research [25]. That is, an LLM-                                         domness involved in LLMs. On one hand, we conduct a large-scale
generated test case is considered correct if it passes the canonical                                         study, and the consistency of our findings across all subjects helps
Aligning Requirement for Large Language Model’s Code Generation                                             ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


mitigate this threat. On the other hand, we repeat Specine’s ex-         plan to explore the integration of Specine with existing techniques
periments three times across all 20 subjects (4 LLMs × 5 bench-          to further enhance their performance.
marks). Notably, the standard derivations are only 0.008 and 0.022
in terms of Pass@1 and AvgPassRatio, respectively, demonstrating         9    Conclusion
the robustness of our conclusions to a large extent. Furthermore,
                                                                         In this work, we draw inspiration from software requirements en-
a Wilcoxon Signed-Rank Test [55] at the significance level of 0.05
                                                                         gineering practices and propose a novel perspective for enhancing
confirms that all p-values exceed 0.55, indicating no statistically
                                                                         the code generation performance of LLMs through specification
significant differences across the three experimental results. This
                                                                         alignment. Based on this perspective, we design Specine, which
further strengthens the reliability of our results.
                                                                         consists of identifying misaligned input specifications, lifting LLM-
   The threat to external validity mainly lies in the used subjects.
                                                                         perceived specifications, and aligning them to further generate
To mitigate this, we carefully select a diverse set of benchmarks,
                                                                         the correct code solution. To evaluate the effectiveness of Specine,
metrics, baselines, and LLMs. Following prior studies [27, 29, 51],
                                                                         we conduct comprehensive experiments on four advanced LLMs
we utilize five widely-used benchmarks in code generation and
                                                                         and five challenging benchmarks. Experimental results demonstrate
employ two metrics to assess code correctness. Additionally, we
                                                                         that Specine consistently outperforms state-of-the-art prompt-based
compare Specine with ten popular or state-of-the-art baselines on
                                                                         and agent-based code generation techniques across multiple eval-
four advanced LLMs, ensuring a comprehensive evaluation. In the
                                                                         uation metrics, highlighting its superiority in enhancing the code
future, we will extend our evaluation to a broader set of benchmarks
                                                                         generation performance of LLMs.
and LLMs to further assess Specine’s generalizability.
                                                                         Acknowledgments
8    Related Work                                                        This work is supported by the National Natural Science Foundation
Code generation is a critical task in software engineering and has       of China (Grant No. 62322208).
garnered significant attention in recent years [9, 32, 49, 59]. Among
the various approaches, prompt-based and agent-based techniques          References
are the two most widely-adopted paradigms.                                [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-
   Prompt-based techniques enhance code generation perfor-                    cia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal
                                                                              Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774
mance of LLMs by designing carefully-crafted prompts that can be              (2023).
applied in a plug-and-play manner. Based on their design principles       [2] Google AI. 2025. Gemini Developer API. https://ai.google.dev/gemini-api/docs/.
                                                                          [3] Anil Altinay, Joseph Nash, Taddeus Kroes, Prabhu Rajasekaran, Dixin Zhou,
and application stages, these techniques can be categorized into              Adrian Dabrowski, David Gens, Yeoul Na, Stijn Volckaert, Cristiano Giuffrida,
three types: (1) Pre-generation techniques (e.g., Self-planning [29]          et al. 2020. BinRec: dynamic binary lifting and recompilation. In Proceedings of
and SCoT [32]) aim to guide LLMs in generating intermediate rea-              the Fifteenth European Conference on Computer Systems. 1–16.
                                                                          [4] Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk
soning steps, thereby improving the effectiveness of code genera-             Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le,
tion. (2) Post-generation techniques (e.g., Self-debugging [8], Self-         et al. 2021. Program synthesis with large language models. arXiv preprint
edit [60], and Self-repair [41]) leverage error messages from test            arXiv:2108.07732 (2021).
                                                                          [5] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou,
execution to enable LLMs to refine and correct erroneous code. (3)            and Weizhu Chen. 2022. CodeT: Code Generation with Generated Tests. In The
Hybrid techniques (e.g., 𝜇Fix [51]) integrate the advantages of both          Eleventh International Conference on Learning Representations.
                                                                          [6] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira
pre-generation and post-generation approaches, leveraging their               Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman,
synergy to further enhance code generation performance of LLMs.               et al. 2021. Evaluating large language models trained on code. arXiv preprint
   Agent-based techniques improve the code generation perfor-                 arXiv:2107.03374 (2021).
                                                                          [7] Xiangping Chen, Xing Hu, Yuan Huang, He Jiang, Weixing Ji, Yanjie Jiang, Yanyan
mance of LLMs by simulating human collaborative software devel-               Jiang, Bo Liu, Hui Liu, Xiaochen Li, et al. 2025. Deep learning-based software
opment processes, where multiple agents interact to accomplish                engineering: progress, challenges, and opportunities. Science China Information
tasks such as task planning, code generation, and testing. Each agent         Sciences 68, 1 (2025), 111102.
                                                                          [8] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2024. Teaching
is assigned a specialized role, and their collaborative interactions          Large Language Models to Self-Debug. In The Twelfth International Conference
optimize different stages of the code generation process. Repre-              on Learning Representations.
                                                                          [9] Codeforces. 2025. https://codeforces.com/.
sentative agent-based techniques, including Self-collaboration [13],     [10] Google DeepMind. 2025. https://deepmind.google/.
AgentCoder [25], and PairCoder [59] (introduced in Section 1 and 4.3),   [11] John Doe. 2011. Recommended practice for software requirements specifications
highlight the importance of role definition and multi-agent coordi-           (ieee). IEEE, New York (2011).
                                                                         [12] Yihong Dong, Jiazheng Ding, Xue Jiang, Ge Li, Zhuo Li, and Zhi Jin. 2024. Code-
nation in improving code generation performance of LLMs.                      Score: Evaluating Code Generation by Learning Code Execution. ACM Trans.
   Unlike existing techniques, Specine introduces a novel perspec-            Softw. Eng. Methodol. (2024).
tive to enhance the code generation performance of LLMs through          [13] Yihong Dong, Xue Jiang, Zhi Jin, and Ge Li. 2024. Self-collaboration code genera-
                                                                              tion via chatgpt. ACM Transactions on Software Engineering and Methodology 33,
specification alignment. Our experimental results demonstrate that            7 (2024), 1–38.
Specine significantly outperforms state-of-the-art prompt-based and      [14] EvalPlus. 2025. Code Sanitizer. https://github.com/evalplus/evalplus/blob/master/
                                                                              evalplus/sanitize.py.
agent-based code generation techniques in terms of effectiveness.        [15] EvalPlus. 2025. EvalPlus Leaderboard. https://evalplus.github.io/leaderboard.
Notably, Specine is orthogonal to existing prompt-based and agent-            html.
based techniques to some extent. Specifically, Specine can serve         [16] Pengfei Gao, Zhao Tian, Xiangxin Meng, Xinchen Wang, Ruida Hu, Yuanan
                                                                              Xiao, Yizhou Liu, Zhao Zhang, Junjie Chen, Cuiyun Gao, et al. 2025. Trae Agent:
as a pre-processing module, aligning requirement specifications               An LLM-based Agent for Software Engineering with Test-time Scaling. arXiv
before they are provided to other techniques. In future work, we              preprint arXiv:2507.23370 (2025).
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                Zhao Tian and Junjie Chen


[17] Shuzheng Gao, Cuiyun Gao, Wenchao Gu, and Michael Lyu. 2025. Search-based            [37] Noble Saji Mathews and Meiyappan Nagappan. 2024. Test-Driven Develop-
     llms for code optimization. In 2025 IEEE/ACM 47th International Conference on             ment and LLM-based Code Generation. In Proceedings of the 39th IEEE/ACM
     Software Engineering (ICSE). IEEE Computer Society, 254–266.                              International Conference on Automated Software Engineering. 1583–1594.
[18] Martin Glinz. 2000. Problems and deficiencies of UML as a requirements specifi-      [38] Fangwen Mu, Lin Shi, Song Wang, Zhuohao Yu, Binquan Zhang, ChenXue Wang,
     cation language. In Tenth International Workshop on Software Specification and            Shichao Liu, and Qing Wang. 2024. Clarifygpt: A framework for enhancing
     Design. IWSSD-10 2000. IEEE, 11–22.                                                       llm-based code generation via requirements clarification. Proceedings of the ACM
[19] Sol Greenspan, John Mylopoulos, and Alex Borgida. 1994. On formal requirements            on Software Engineering 1, FSE (2024), 2332–2354.
     modeling languages: RML revisited. In Proceedings of 16th International Conference   [39] Nico Naus, Freek Verbeek, Sagar Atla, and Binoy Ravindran. 2024. Poster: For-
     on Software Engineering. IEEE, 135–147.                                                   mally Verified Binary Lifting to P-Code. In Proceedings of the 2024 on ACM SIGSAC
[20] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin                    Conference on Computer and Communications Security. 4973–4975.
     Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1:            [40] Homepage of Specnie. 2025. https://github.com/tianzhaotju/Specine.
     Incentivizing reasoning capability in llms via reinforcement learning. arXiv         [41] Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and
     preprint arXiv:2501.12948 (2025).                                                         Armando Solar-Lezama. 2024. Is Self-Repair a Silver Bullet for Code Generation?.
[21] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang,                     In The Twelfth International Conference on Learning Representations.
     Guanting Chen, Xiao Bi, Yu Wu, YK Li, et al. 2024. DeepSeek-Coder: When the          [42] OpenAI. 2024. Introducing GPT-4o and more tools to ChatGPT free users. (2024).
     Large Language Model Meets Programming–The Rise of Code Intelligence. arXiv          [43] OpenAI. 2025. The most powerful platform for building AI products. https:
     preprint arXiv:2401.14196 (2024).                                                         //openai.com/api/.
[22] Qi Guo, Xiaofei Xie, Shangqing Liu, Ming Hu, Xiaohong Li, and Lei Bu. 2025.          [44] Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer. 2023. The impact
     Intention is All You Need: Refining Your Code from Your Intention. In 2025                of ai on developer productivity: Evidence from github copilot. arXiv preprint
     IEEE/ACM 47th International Conference on Software Engineering (ICSE). IEEE               arXiv:2302.06590 (2023).
     Computer Society.                                                                    [45] LeetCode The World’s Leading Online Programming Learning Platform. 2025.
[23] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora,                https://leetcode.com/.
     Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob              [46] Klaus Pohl. 1996. Requirements engineering: An overview. Citeseer.
     Steinhardt. 2021. Measuring Coding Challenge Competence With APPS. In                [47] Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol
     Thirty-fifth Conference on Neural Information Processing Systems Datasets and             Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. 2024.
     Benchmarks Track (Round 2). https://openreview.net/forum?id=sD93GOzH3i5                   Gemini 1.5: Unlocking multimodal understanding across millions of tokens of
[24] Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng Cheng, Jinlin Wang, Ceyao                  context. arXiv preprint arXiv:2403.05530 (2024).
     Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. 2023.         [48] Zhao Tian, Junjie Chen, and Zhi Jin. 2023. Code difference guided adversarial
     Metagpt: Meta programming for multi-agent collaborative framework. arXiv                  example generation for deep code models. In 2023 38th IEEE/ACM International
     preprint arXiv:2308.00352 (2023).                                                         Conference on Automated Software Engineering (ASE). IEEE, 850–862.
[25] Dong Huang, Qingwen Bu, Jie M Zhang, Michael Luck, and Heming Cui. 2023.             [49] Zhao Tian, Junjie Chen, Dong Wang, Qihao Zhu, Xingyu Fan, and Lingming
     Agentcoder: Multi-agent-based code generation with iterative testing and opti-            Zhang. [n. d.]. LEAM++: Learning for Selective Mutation Fault Construction.
     misation. arXiv preprint arXiv:2312.13010 (2023).                                         ACM Transactions on Software Engineering and Methodology ([n. d.]).
[26] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu        [50] Zhao Tian, Junjie Chen, and Xiangyu Zhang. 2023. On-the-fly improving perfor-
     Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al. 2024. Qwen2. 5-coder technical             mance of deep code models via input denoising. In 2023 38th IEEE/ACM Interna-
     report. arXiv preprint arXiv:2409.12186 (2024).                                           tional Conference on Automated Software Engineering (ASE). IEEE, 560–572.
[27] Md. Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. 2024. Map-             [51] Zhao Tian, Junjie Chen, and Xiangyu Zhang. 2025. Fixing Large Language Models’
     Coder: Multi-Agent Code Generation for Competitive Problem Solving. In Pro-               Specification Misunderstanding for Better Code Generation. In 2025 IEEE/ACM
     ceedings of the 62nd Annual Meeting of the Association for Computational Linguis-         46th International Conference on Software Engineering (ICSE).
     tics (Volume 1: Long Papers). 4912–4944.                                             [52] Zhao Tian, Junjie Chen, Qihao Zhu, Junjie Yang, and Lingming Zhang. 2022.
[28] Naman Jain, Tianjun Zhang, Wei-Lin Chiang, Joseph E Gonzalez, Koushik Sen,                Learning to construct better mutation faults. In Proceedings of the 37th IEEE/ACM
     and Ion Stoica. 2023. Improving code style for accurate code generation. In               International Conference on Automated Software Engineering. 1–13.
     NeurIPS 2023 Workshop on Synthetic Data Generation with Generative AI.               [53] Zhao Tian, Honglin Shu, Dong Wang, Xuejie Cao, Yasutaka Kamei, and Junjie
[29] Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi                 Chen. 2024. Large language models for equivalent mutant detection: How far
     Jin, and Wenpin Jiao. 2024. Self-planning code generation with large language             are we?. In Proceedings of the 33rd ACM SIGSOFT International Symposium on
     models. ACM Transactions on Software Engineering and Methodology 33, 7 (2024),            Software Testing and Analysis. 1733–1745.
     1–30.                                                                                [54] Bingyang Wei. 2024. Requirements are All You Need: From Requirements to
[30] Majeed Kazemitabaar, Justin Chow, Carl Ka To Ma, Barbara J Ericson, David                 Code with LLMs. arXiv preprint arXiv:2406.10101 (2024).
     Weintrop, and Tovi Grossman. 2023. Studying the effect of AI code generators         [55] Frank Wilcoxon, S Katti, Roberta A Wilcox, et al. 1970. Critical values and
     on supporting novice learners in introductory programming. In Proceedings of              probability levels for the Wilcoxon rank sum test and the Wilcoxon signed rank
     the 2023 CHI Conference on Human Factors in Computing Systems. 1–23.                      test. Selected tables in mathematical statistics 1 (1970), 171–259.
[31] Mohammad Abdullah Matin Khan, M Saiful Bari, Xuan Long Do, Weishi Wang,              [56] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue,
     Md Rizwan Parvez, and Shafiq Joty. 2024. XCodeEval: An Execution-based Large              Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, et al.
     Scale Multilingual Multitask Benchmark for Code Understanding, Generation,                2019. Huggingface’s transformers: State-of-the-art natural language processing.
     Translation and Retrieval. In Proceedings of the 62nd Annual Meeting of the As-           arXiv preprint arXiv:1910.03771 (2019).
     sociation for Computational Linguistics (Volume 1: Long Papers). Association for     [57] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     Computational Linguistics, 6766–6805.                                                     Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and unleashing the power
[32] Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2025. Structured chain-of-thought prompt-         of large language models in automated code translation. Proceedings of the ACM
     ing for code generation. ACM Transactions on Software Engineering and Method-             on Software Engineering 1, FSE (2024), 1585–1608.
     ology 34, 2 (2025), 1–23.                                                            [58] Pamela Zave and Michael Jackson. 1997. Four dark corners of requirements
[33] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi            engineering. ACM transactions on Software Engineering and Methodology (TOSEM)
     Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. 2022.          6, 1 (1997), 1–30.
     Competition-level code generation with alphacode. Science 378, 6624 (2022),          [59] Huan Zhang, Wei Cheng, Yuhan Wu, and Wei Hu. 2024. A Pair Programming
     1092–1097.                                                                                Framework for Code Generation via Multi-Plan Exploration and Feedback-Driven
[34] Feng Lin, Dong Jae Kim, and Tse-Hsun (Peter) Chen. 2025. SOEN-101: Code                   Refinement. In Proceedings of the 39th IEEE/ACM International Conference on
     Generation by Emulating Software Process Models Using Large Language Model                Automated Software Engineering. 1319–1331.
     Agents. In 2025 IEEE/ACM 46th International Conference on Software Engineering       [60] Kechi Zhang, Zhuo Li, Jia Li, Ge Li, and Zhi Jin. 2023. Self-Edit: Fault-Aware
     (ICSE).                                                                                   Code Editor for Code Generation. arXiv preprint arXiv:2305.04087 (2023).
[35] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. 2023. Is your        [61] Naifeng Zhang, Sanil Rao, Mike Franusich, and Franz Franchetti. 2025. Towards
     code generated by chatgpt really correct? rigorous evaluation of large language           Semantics Lifting for Scientific Computing: A Case Study on FFT. arXiv preprint
     models for code generation. Advances in Neural Information Processing Systems             arXiv:2501.09201 (2025).
     36 (2023), 21558–21572.                                                              [62] Shun Zhang, Zhenfang Chen, Yikang Shen, Mingyu Ding, Joshua B Tenenbaum,
[36] Linda A Macaulay. 2012. Requirements engineering. Springer Science & Business             and Chuang Gan. 2023. Planning with Large Language Models for Code Genera-
     Media.                                                                                    tion. In The Eleventh International Conference on Learning Representations.
