                                        The Fusion of Large Language Models and Formal Methods
                                        for Trustworthy AI Agents: A Roadmap
                                        YEDI ZHANG†∗ , YUFAN CAI∗ , and XINYUE ZUO∗ , National University of Singapore, Singapore
                                        XIAOKUN LUAN∗ , Peking University, China
arXiv:2412.06512v1 [cs.AI] 9 Dec 2024




                                        KAILONG WANG∗ , Huazhong University of Science and Technology, China
                                        ZHÉ HÓU∗ , Griffith University, Australia
                                        YIFAN ZHANG, National University of Singapore, Singapore
                                        ZHIYUAN WEI, Beijing Institute of Technology, China
                                        MENG SUN, Peking University, China
                                        JUN SUN, Singapore Management University, Singapore
                                        JING SUN, University of Auckland, New Zealand
                                        JIN SONG DONG, National University of Singapore, Singapore
                                        Large Language Models (LLMs) have emerged as a transformative AI paradigm, profoundly influencing daily
                                        life through their exceptional language understanding and contextual generation capabilities. Despite their
                                        remarkable performance, LLMs face a critical challenge: the propensity to produce unreliable outputs due
                                        to the inherent limitations of their learning-based nature. Formal methods (FMs), on the other hand, are
                                        a well-established computation paradigm that provides mathematically rigorous techniques for modeling,
                                        specifying, and verifying the correctness of systems. FMs have been extensively applied in mission-critical
                                        software engineering, embedded systems, and cybersecurity. However, the primary challenge impeding the
                                        deployment of FMs in real-world settings lies in their steep learning curves, the absence of user-friendly
                                        interfaces, and issues with efficiency and adaptability.
                                            This position paper outlines a roadmap for advancing the next generation of trustworthy AI systems by
                                        leveraging the mutual enhancement of LLMs and FMs. First, we illustrate how FMs, including reasoning and
                                        certification techniques, can help LLMs generate more reliable and formally certified outputs. Subsequently,
                                        we highlight how the advanced learning capabilities and adaptability of LLMs can significantly enhance the
                                        usability, efficiency, and scalability of existing FM tools. Finally, we show that unifying these two computation
                                        paradigms—integrating the flexibility and intelligence of LLMs with the rigorous reasoning abilities of FMs—
                                        has transformative potential for the development of trustworthy AI software systems. We acknowledge that
                                        this integration has the potential to enhance both the trustworthiness and efficiency of software engineering
                                        practices while fostering the development of intelligent FM tools capable of addressing complex yet real-world
                                        challenges.
                                        Additional Key Words and Phrases: Large Language Models, Formal Methods, SMT Solver, Automated Reason-
                                        ing, Autoformalization, Theorem Proving, Testing and Verification, Model Checking, Program Synthesis

                                        1   INTRODUCTION
                                        The rapid advancement of modern AI techniques, particularly in the realm of Large Language
                                        Models (LLMs) like GPT [Achiam et al. 2023], Llama [Touvron et al. 2023], Claude [Claude 2024],
                                        Gemini [Gemini 2024], etc., has marked a significant evolution in human-level computational
                                        capabilities. These models are fundamentally reshaping tasks across a spectrum of applications,
                                        from natural language processing to automated content generation. Trained on vast text corpora,
                                        ∗ Equal contribution, † Corresponding author.

                                        Authors’ Contact Information: Yedi Zhang†∗ , yd.zhang@nus.edu.sg; Yufan Cai∗ ; Xinyue Zuo∗ , National University of
                                        Singapore, Singapore; Xiaokun Luan∗ , Peking University, China; Kailong Wang∗ , wangkl@hust.edu.cn, Huazhong University
                                        of Science and Technology, China; Zhé Hóu∗ , z.hou@griffith.edu.au, Griffith University, Australia; Yifan Zhang, National
                                        University of Singapore, Singapore; Zhiyuan Wei, Beijing Institute of Technology, China; Meng Sun, Peking University,
                                        China; Jun Sun, Singapore Management University, Singapore; Jing Sun, University of Auckland, New Zealand; Jin Song
                                        Dong, dcsdjs@nus.edu.sg, National University of Singapore, Singapore.
2                                                                                            Zhang et al.


LLMs excel in generating responses that are contextually accurate and stylistically appropriate.
However, their applicability in safety-critical or knowledge-critical settings remains limited due
to their inherent reliability issues—primarily, their propensity for generating outputs that, while
plausible, may be factually incorrect or contextually inappropriate [Agarwal et al. 2024; Jacovi and
Goldberg 2020; Wiegreffe and Marasovic 2020]. This limitation, known as “hallucination”, stems
from the probabilistic nature of learning-based AI, where the models optimize for likelihood rather
than truth or logical consistency.
   In a completely different thread of research, Formal Methods (FMs) have been established as rig-
orous tools for verification and validation (V&V) of critical systems where failure is intolerable, such
as aerospace (relevant areas including avionics) [Dragomir et al. 2022; Liu et al. 2019], autonomous
driving [Alves et al. 2021; Huang et al. 2022; König et al. 2024], and medical devices [Arcaini et al.
2018; Freitas et al. 2020; Jetley et al. 2006]. By performing appropriate mathematical analysis, these
methods are designed to ensure the correctness and safety of both hardware and/or software
systems. Despite their demonstrated benefits, the adoption of FMs remains limited, primarily due to
their significant computational complexity and the specialized expertise required for their effective
and efficient implementation.
   Although both computational paradigms encounter inherent challenges of their own—namely,
the unreliability stemming from the statistical nature of LLMs and the user-unfriendly interfaces
coupled with the computational complexity of formal methods—recent studies have highlighted
their potential for mutual benefits [He-Yueya et al. 2023; Pan et al. 2023; Song et al. 2024; Wu et al.
2022; Yang and Deng 2019; Yang et al. 2024; Zhou et al. 2024]. Efforts to bridge these two paradigms
aim to harness their respective strengths, with the ultimate objective of developing a neural-
symbolic AI seamlessly integrates LLMs and FMs into a unified solution. For instance, to enhance
the reliability of LLMs, various approaches [Ma et al. 2024a; Pan et al. 2023] have incorporated
solvers to facilitate reasoning tasks guided by specification rules or reasoning models derived
from LLMs’ inputs/outputs. Specifically, some efforts have been directed toward improving LLMs’
understanding of Lisp, enabling better integration with Lisp-based programming techniques [Li
et al. 2024b; Stengel-Eskin et al. 2024]. Conversely, within the formal methods community, there is a
growing trend to leverage LLMs to enhance the functionality and usability of automated verification
approaches [Wen et al. 2024; Wu et al. 2024]. Indeed, LLMs are increasingly utilized to automate
and simplify the generation of specifications and proofs, and by employing LLMs to analyze natural
language requirements or extract logical properties from complex systems, researchers aim to
bridge the gap between human-readable specifications and machine-executable formal models.
   In this paper, we aim to advance the research agenda of bi-directional enhancement by building on
insights from our prior investigations and providing a comprehensive discussion of its implications,
technical challenges, and potential future directions. More specifically, we first look into how
FMs can contribute to improving the trustworthiness of LLMs. In this context, we discuss how
symbolic solvers, such as SMT solvers, can be seamlessly integrated into LLMs to enable a complete
reasoning cycle, thereby enhancing their logical reasoning capabilities and ensuring more robust
and reliable responses. Additionally, we investigate methods for advancing the evaluation of LLMs
through logical reasoning frameworks and delve into rigorous behavior analysis of LLMs via formal
verification techniques. Next, we examine how LLMs can drive advancements in existing formal
methods and tools, focusing on three key areas: (i) utilizing LLMs for the automated formalization
of specifications to bridge natural language and formal representations, (ii) leveraging LLMs to
enhance theorem proving by automating proof generation and validation, and (iii) employing
LLMs to develop intelligent model checkers with improved adaptability and efficiency. Finally, we
recognize that the bi-directional interactions between LLMs and FMs open avenues for further
exploration, highlighting their potential to drive the development of next-generation AI systems
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap         3




                      Fig. 1. Towards Trustworthy LLM Agents with Formal Methods.


that seamlessly integrate these paradigms. We believe that such integration holds significant
promise for developing trustworthy AI agents across diverse application domains, as exemplified
by the widely applicable scenario of program synthesis.
   The remainder of this paper is structured as follows: Section 2 outlines a roadmap for building
trustworthy agents by combining the strengths of FMs and LLMs. Sections 3 and 4 explore their bi-
directional benefits, focusing on FMs for LLMs and LLMs for FMs, respectively. Section 5 highlights
our exploration of integrating LLMs and FMs as a unified computational paradigm. Finally, Section 6
concludes the paper.

2   A ROADMAP TO TRUSTWORTHY LLM: COMBINING LLM AND FM
This section gives a roadmap for the development of a trustworthy LLM agent, specifically tailored
to tasks involving FMs, emphasizing the integration of rigorous formal analysis techniques with
the adaptability and learning capabilities of language models.
   The proposed roadmap, depicted in Figure 1, adopts a twofold strategy. On the one hand, we
advocate for the integration of formal analysis principles throughout the development and V&V
phases. This aims to enhance the reasoning capabilities of LLM agents while ensuring their reliability
and compliance with stringent certification standards, a strategy direction we term FMs for LLMs.
On the other hand, we leverage the adaptability and learning capabilities of LLMs during the
functionality development phase of FM-based tools. This is aimed at enhancing the flexibility and
reasoning efficiency of established formal analysis methodologies, such as theorem proving and
model checking. In this paper, we refer to this strategic direction as LLMs for FMs. Ultimately, we
argue that the dynamic interplay between these two strategic directions will substantially advance
the development of trustworthy LLM agents, particularly in the domain of formal methods.
   Building on these foundations, we outline the envisioned characteristics of a trustworthy LLM
agent as follows. Firstly, an LLM agent tailored for formal analysis should be implemented directly
at the client’s premises, allowing them to learn from and adapt to the client’s specific data and
workflows, also allowing the client’s domain-specific experts to use formal methods through LLM
agents with a low entry bar. This localized learning approach should not only enable the agents
to enhance their performance over time but also ensure that the entire process safeguards the
client’s privacy. Based on this, LLM agents will significantly reduce both the human learning curve
and the requisite human resources needed to apply formal methods, thereby facilitating a more
efficient integration of these methodologies into the client’s operational framework. Secondly, each
output suggested by an LLM agent should be both faithful and rigorously certified, particularly
when the response is expected to be deterministic. This requirement ensures that the outputs not
only align closely with the rules defined within the formal methods framework but also meet
predefined accuracy and reliability standards. To achieve this, the outputs must undergo a thorough
certification process, possibly involving techniques such as testing or verification, to validate that
4                                                                                             Zhang et al.


they are correct and adhere strictly to the operational and regulatory requirements. Note that, such
a certification process is critical, as it guarantees that the solutions provided by the LLM agents are
not only effective but also trustworthy and legally compliant, thereby increasing the confidence of
stakeholders in deploying these agents within sensitive or critical operational contexts.
   In the subsequent sections, we will adhere to the roadmap outlined in Figure 1 to present our
insights, document our work in progress, and outline our future visions regarding the two strategic
directions. Additionally, we will also discuss the synergistic outcomes derived from the integration
of these two computation paradigms. Specifically, we demonstrate how this integration can lead to
the development of programming refinement methodologies, exemplifying their applications in
more intelligent computational environments.

3     FM FOR LLM: TOWARDS RELIABILITY AND CERTIFICATION
In this section, we illustrate how formal methods can enhance the reliability and help certification
of LLMs. Specifically, we explore this integration direction from three perspectives: (i) trustworthy
LLMs with symbolic solvers, (ii) LLM Testing based on logical reasoning, and (iii) rigorous LLM
behavior analysis. We argue that incorporating these FM-based techniques enables AI systems to
become reliably secure, paving the way for developing trustworthy AI systems.
   Note that this section highlights the initial efforts to apply formal methods to enhance the reliabil-
ity of LLMs, acknowledging that these approaches are not exhaustive. While a fully comprehensive
methodology for integrating formal methods into LLMs remains elusive, we present our current
implementations and future visions as preliminary steps toward advancing this direction.

3.1    SMT Solvers for LLMs
Satisfiability Modulo Theories (SMT) solvers are specialized tools designed to determine the satisfi-
ability of logical formulas defined over some theories, such as arithmetic, bit-vectors, and arrays.
They play a pivotal role in formal verification, program analysis, and automated reasoning, serving
as essential components to ensure the correctness and reliability of complex software systems.
   Recent studies [Deng et al. 2024; Pan et al. 2023; Wang et al. 2024; Ye et al. 2024] have explored
the integration of SMT solvers to enhance the accuracy and reliability of LLMs in logic reasoning
tasks. These solver-powered LLM agents operate by translating task descriptions into formal
specifications, delegating reasoning tasks to specialized expert tools for precise analysis, and
subsequently converting the outputs back into natural language.
   We have identified three main challenges within this research line. Firstly, while LLMs are
capable of generating logical constraints or SMT formulas, they often produce suboptimal or overly
verbose constraints, which can place an additional computational burden on the solver. Secondly,
the outputs of LLMs lack guarantees of correctness or logical consistency, potentially introducing
subtle inaccuracies or ambiguities in the generated SMT constraints. It can lead to invalid results
or solutions that are challenging to interpret. Lastly, LLMs often lack domain-specific knowledge
and may struggle to generate outputs that conform to the precise formal syntax required by SMT
solvers. Consequently, they may generate formulas that are semantically sensible but syntactically
invalid formulas, rendering them unprocessable by the solvers.
3.1.1 Our Insights. We present our insights and proposed strategies to address the three key
challenges outlined above.
Strategy 1. Multiple LLMs Debating. To address the challenge of LLMs generating suboptimal or
overly verbose constraints, a potential strategy involves leveraging multiple LLMs in a collaborative
or adversarial framework to critique, validate, and refine each other’s outputs. In this approach, the
system employs one or more LLMs to generate SMT code from natural language inputs, while other
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap        5


LLMs function as “critics”, evaluating the generated SMT code for logical consistency, syntactic
correctness, and alignment with the problem description. By incorporating feedback loops among
these models, the system can iteratively refine the outputs and reduce ambiguity inherent in natural
language inputs.
Strategy 2. Test Generation. Test cases will be automatically generated to validate the correctness
and consistency of the LLM-generated SMT code against the expected behavior. Fuzzing techniques
may also be employed to generate adversarial inputs for testing. Additionally, mutation-based
approaches can be applied to both the SMT code and the natural language descriptions, with two
LLMs comparing the resulting solutions. The strategy helps check the consistency between the
natural language description and the SMT code produced by the LLMs.
Strategy 3. Self-Correction. Feedback from tests, critics, or the solver itself can be leveraged
to iteratively refine the SMT code. Errors identified via solvers can be categorized into syntax
issues (e.g., invalid SMT-LIB syntax), semantic misalignments (e.g., logical inconsistencies), or
performance bottlenecks (e.g., slow or incomplete solver responses). Based on this feedback, an
LLM can be employed to debug and regenerate problematic parts of the constraints, ensuring that
the refinements are both targeted and context-aware. This iterative refinement process, coupled
with validation through re-testing, facilitates the convergence of LLM-generated SMT codes toward
correctness and rigorousness.
3.1.2 Case Study on LLMs with Z3. To illustrate our perspective, we give our recent exploration of
the interaction between LLMs and Z3 in Python.
   Z3 [de Moura and Bjørner 2008], a widely used SMT solver, accepts inputs in the form of simple-
sorted formulas expressed in first-order logic (FOL). These formulas can include symbols with
predefined meanings, defined by the underlying theories supported by the solver, and these theories
encompass domains such as arithmetic, bit-vectors, arrays, etc., making Z3 particularly well-suited
for reasoning about a wide range of logical constraints.
  Example. Consider a scenario where a user requests the LLM agent to solve a scheduling problem:
      “Can you help plan a meeting for a team of three people—David, Emma, and Alex?
      David is free on Monday or Tuesday, Emma is free on Tuesday or Wednesday, and Alex
      is free only on Tuesday or Thursday. Find a common day when all three are available.”
  We now provide a detailed, step-by-step solution for this task:
  Formalization of Constraints. Given the above problem, the initial Z3 constraints in Python
generated by the LLM are given as follows:
     # Define days of the week
     days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
     David_free = [Bool(f"David_free_{day}") for day in days]
     Emma_free = [Bool(f"Emma_free_{day}") for day in days]
     Alex_free = [Bool(f"Alex_free_{day}") for day in days]
     # Create a solver
     solver = Solver()
     # Define constraints for each person's availability
     solver.add(Or(David_free[0], David_free[1]))
     solver.add(Or(Emma_free[1], Emma_free[2]))
     solver.add(Or(Alex_free[1], Alex_free[3]))
     # Add constraints that ensure a common day for all three
     common_day_constraints = [And(David_free[i],
     Emma_free[i], Alex_free[i]) for i in range(len(days))]
     solver.add(Or(common_day_constraints))
6                                                                                           Zhang et al.


  Self correction. If the Z3 code has issues (e.g., missing constraints or syntax errors) or generates
inconsistent results with the natural language description, the self-correction procedure will identify
and correct them. In this example, the previous Z3 code ignores the following constraints:

    # Constraints for David
    solver.add(And(Not(David_free[2]), Not(David_free[3])))
    # Constraints for Emma
    solver.add(And(Not(Emma_free[0]), Not(Emma_free[3])))
    # Constraints for Alex
    solver.add(And(Not(Alex_free[0]), Not(Alex_free[2])))



   Test Generation. The agent mutates the constraints and tweaks the availability of each individual
to create new conditions. For example, the new mutated constraints are David will be free on
Monday and Wednesday. Emma will be free on Tuesday and Thursday. Alex will be free on Monday
and Thursday. The updated Z3 code generated by the LLM is as follows:

    # Mutated constraints for David
    solver.add(And(David_free[0], David_free[2]))
    solver.add(And(Not(David_free[1]), Not(David_free[3])))
    # Mutated constraints for Emma
    solver.add(And(Emma_free[1], Emma_free[3]))
    solver.add(And(Not(Emma_free[0]), Not(Emma_free[2])))
    # Mutated constraints for Alex
    solver.add(And(Alex_free[0], Alex_free[3]))
    solver.add(And(Not(Alex_free[1]), Not(Alex_free[2])))


The agent systems will check the consistency between the results produced by Z3 and the reasoning
derived from natural language descriptions to further ensure the correctness of the Z3 codes.
   Multiple LLM Debating. Whenever it comes to a collision between the Z3 reasoning results and
the natural language reasoning results, the LLM debating will be activated to debate which part
is correct. For example, after LLM-A generates the initial constraints and gets the results of Z3
code. LLM-B will critique the constraints, identifying potential issues such as missing exclusivity
rules or improperly translated logic. LLM-C can suggest refinements, such as introducing mutual
exclusivity or expanding constraints to handle edge cases. The consensus will be the output with
the highest confidence score (e.g., most accurate or simplest) is selected for testing and execution.
   Problem Solving. The translated constraints are fed into the Z3 solver, which checks the satisfia-
bility of the formula and computes a solution if possible.

    # Check for a solution
    if solver.check() == sat:
        model = solver.model()
        common_days = [days[i] for i in range(len(days))
        if model.evaluate(David_free[i])
           and model.evaluate(Emma_free[i])
           and model.evaluate(Alex_free[i])]
        print(f"Common day(s) when everyone is free:
        {common_days}")
    else:
        print("No common day when everyone is free.")
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap           7


   Solution Interpretation. The LLM agent receives the solution from the Z3 solver and translates
it back into natural language for the user. The only day when all three are free is Tuesday. The
output will be: Common day(s) when everyone is free: [‘Tuesday’].

3.2   Logical Reasoning for LLM on Test Case Generation
LLM Testing [Hendrycks et al. 2021; Huang et al. 2023; Zhong et al. 2024; Zhou et al. 2023] is primarily
focused on establishing a comprehensive benchmark to evaluate the overall performance of the
models, ensuring that they fulfill specific assessment criteria, such as accuracy, coherence, fairness,
and safety, in alignment with their intended applications. Among these criteria, the phenomenon of
“hallucination” is particularly noteworthy. This occurs when LLMs generate coherent but factually
or contextually inaccurate or irrelevant output during tasks such as problem-solving.
   Recent research has introduced a variety of methodologies for detection and evaluation to mitigate
hallucination issues in LLMs. A common and straightforward method is to create comprehensive
benchmarks specifically designed to assess LLM performance. However, these methods, which often
rely on simplistic or semi-automated techniques such as string matching, manual validation, or
cross-verification using another LLM, has significant shortcomings in automatically and effectively
testing Fact-conflicting hallucinations (FCH) [Li et al. 2024a]. This is largely due to the lack of
dedicated ground truth datasets and specific testing frameworks. We contend that unlike other
types of hallucinations, which can be identified through checks for semantic consistency, FCH
requires the verification of content’s factual accuracy against external, authoritative knowledge
sources or databases. Hence, it is crucial to automatically construct and update factual benchmarks,
and automatically validate the LLM outputs based on that.
   To this end, we propose to apply logical reasoning to design a reasoning-based test case generation
method aimed at developing an extensive and extensible FCH testing framework. Such a testing
framework leverages factual knowledge reasoning combined with metamorphic testing principles
to ensure a comprehensive and robust FCH evaluation of LLM outputs.

3.2.1 Overview. A reasoning-based test case generation framework for FCH in LLMs should
comprise the following four key modules working in sequential:
Module 1. Factual Knowledge Extraction. Utilizing extensive knowledge database dumps, the
essential information and factual triples of verified entities are systematically extracted.
Module 2. Logical Reasoning. This module enables employing reasoning rules for generating
valid and diverse facts and establishing new ground truth knowledge.
Module 3. Benchmark Construction. Focused on producing high-quality test case-oracle pairs
from the newly generated ground truth knowledge, this module uses a straightforward metamorphic
relation: Questions that align with the generated knowledge should receive a response of “YES”, while
questions that contradict it should be answered with “NO”. This module also includes methods for
generating or selecting effective prompts to facilitate reliable interaction with LLMs.
Module 4. Response Evaluation. In the final module, the responses from LLMs are evaluated to
detect factual consistency automatically. The module parses LLM outputs using NLP techniques
to construct semantic-aware representations and assesses semantic similarity with ground truth.
It then applies similarity-based oracles, using metamorphic testing to evaluate the consistency
between LLM responses and established ground truth.

3.2.2 Factual Knowledge Extraction. This process focuses on extracting essential factual information
from input knowledge data in the form of fact triples, which are then suitable for logical reasoning.
Existing knowledge databases [Auer et al. 2007; Bollacker et al. 2007; Miller 1995; Suchanek et al.
2007] serve as valuable resources due to their extensive repositories of structured data derived from
8                                                                                            Zhang et al.


documents and web pages. This structured data forms the foundation for constructing and enriching
factual knowledge, providing a robust basis for the test case framework. The approach leverages
the categorization of entities and relations defined in resources like Wikipedia, as demonstrated in
accompanying figures that illustrate entity categories, relation types, and example fact triples.
   The extraction process typically involves structuring facts as three-element predicates, nm (𝑠, 𝑜),
where “𝑠” (stands for subject) and “𝑜” (stands for object) are entities, and “nm” denotes the predicate.
This divide-and-conquer strategy extracts facts category by category, effectively organizing infor-
mation across various domains. The extraction processs iterates through predefined categories of
entities and relations, employing a database querying function to retrieve all relevant fact triples for
a given entity and predicate combination. This ensures comprehensive and systematic extraction
of factual knowledge, creating a well-structured dataset for reasoning and testing.
3.2.3 Logical Reasoning. This step focuses on deriving enriched information from previously
extracted factual knowledge by employing logical reasoning techniques. The approach utilizes
a logical programming-based processor to automatically generate new fact triples by applying
predefined inference rules, taking one or more input triples and producing derived outputs.
   In particular, to introduce variability in the generation of test cases, reasoning rules, commonly
utilized in existing literature [Abboud et al. 2020; Liang et al. 2022; Zhou et al. 2019] for knowledge
reasoning, are typically adopted, including negation, symmetric, inverse, transitive and composite.
These rules provide a systematic framework for generating new factual knowledge, ensuring
diverse and comprehensive test case preparation. The system applies all relevant reasoning rules
exhaustively to the appropriate fact triples, enabling the automated enrichment of the knowledge
base for further testing purposes.
3.2.4 Benchmark Construction. This process consists of two key steps: (i) generating question-
answer (Q&A) pairs and (ii) creating prompts from derived triples, which together can significantly
reduce manual effort in test oracle generation.
Step 1. Question Generation. This step uses entity-relation mappings to populate predefined Q&A
templates, aligning relation types with corresponding question structures based on the grammatical
and semantic characteristics of predicates. For predicates with unique characteristics, customized
templates are employed to generate valid Q&A pairs. To enhance natural language formulation,
LLM can be used to refine the Q&A structures. Answers are derived directly from factual triples,
with true/false judgments determined by the data. Mutated templates, leveraging synonyms or
antonyms, diversify questions with opposite semantics, yielding complementary answers.
Step 2. Prompt Construction. Prompts are designed to instruct LLMs to provide explicit judgments
(e.g., yes/no/I don’t know) and outline their reasoning in standardized formats. LLM analysts
can utilize predefined instructions to ensure clarity and enable LLMs to deliver assessable and
logically consistent responses. This method maximizes the model’s reasoning capabilities within
the structured framework of prompts and cues.
3.2.5 Response Evaluation. This step aims to enhance the factual evaluation in LLM outputs by
identifying discrepancies between LLM responses and the verified ground truth in Q&A pairs. Since
the “yes” or “no” answers from LLMs may be unreliable, the module emphasizes analyzing the
reasoning process to assess factual consistency. The approach uses semantic similarity between
parsed LLM responses and ground truth to detect inconsistencies systematically.
   The process begins with preliminary screening, where responses indicating the LLM’s inability
to answer (e.g., “I don’t know”) are classified as correct, as they align with the model’s honesty
principle. Suspicious responses proceed to response parsing and semantic structure construction,
where statements in the reasoning process are parsed into triples. These triples are used to construct
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap           9


a semantic graph for the response, which is compared with a similar graph constructed from ground
truth triples. Finally, similarity-based metamorphic testing and oracles evaluate consistency by
comparing the semantic structures of the response and ground truth, focusing on node similarity
(fact correctness) and edge similarity (reasoning correctness). Responses are categorized into
four classes: correct responses (both nodes and edges are similar), hallucinations from erroneous
inference (nodes are similar, edges are dissimilar), hallucinations from erroneous knowledge (edges
are similar, nodes are dissimilar), and overlaps with both issues (both nodes and edges are dissimilar).

3.3    Rigorous LLM Behavior Analysis
While LLM Testing techniques can effectively provide broad assessments and reveal edge cases that
may provoke unexpected responses, they are limited in their capability to give rigorous guarantees
on LLM behaviors. LLM Verification, on the other hand, serves as a complementary mechanism.
However, as LLMs grow more complex and tasks become increasingly sophisticated, traditional
neural network verifiers lose relevance due to their limitations in accommodating diverse model
architectures and their focus on single-application scenarios. Indeed, formal verification of LLMs
poses intrinsic challenges due to three key factors:
Factor 1. Non-Deterministic Responses. Responses from LLMs are non-deterministic, meaning
their outputs may vary even with the same input. This inherent variability presents substantial
challenges to providing deterministic guarantees regarding their behavior.
Factor 2. High Input Dimensions. The high dimensionality of inputs in LLMs leads to exponential
growth in the number of input tokens, rendering exhaustive verification across an infinite input
space highly impractical.
Factor 3. Lack of Formal Specification. While formal specifications are rigorous, they often
lack the expressive capability of natural language, which makes it extremely difficult to precisely
capture the nuanced and complex language behaviors expected from LLMs.
   Hence, we propose that a specialized verification paradigm tailored specifically for LLMs should
be considered to ensure reliable and rigorous certification for long-term applications.
   Given these challenges, we argue that monitoring might serve as a viable long-term solution
for reliable LLM behavior analysis. Positioned between testing and verification, monitoring of
formalized properties at runtime enables rigorous certification of system behavior with minimal
computation overhead by examining execution traces against predefined properties. This approach
has already inspired several efforts to monitor LLM responses at runtime [Besta et al. 2024; Chen
et al. 2024; Cohen et al. 2023; Manakul et al. 2023] (quite similar to another research line named
guardrails). However, the specifications used in these methods remain ambiguous and informal.
For example, they define the properties of low hallucination based on the stability of LLM outputs.
More recently, an approach [Cheng et al. 2024] has been introduced to monitor the conditional
fairness properties of LLM responses. The specifications in [Cheng et al. 2024] are informed by
linear temporal logic and its bounded metric interval temporal logic variant, reflecting a shift
toward formal methods for more precise and dependable monitoring of LLM behavior. Despite
these progresses, further efforts are needed to enable rigorous monitoring of a wider range of
properties to fit in more real-world settings, which will remain our primary focus in the future.

4     LLM FOR FM: SOLVING VERIFICATION TASKS INTELLIGENTLY
This section explores how LLMs can enhance formal methods by developing intelligent LLM
agents for tasks such as theorem proving and model checking. These agents bring adaptability
and efficiency to traditional formal verification processes, paving the way for more advanced and
effective formal methods.
10                                                                                            Zhang et al.


      Problem: Let 𝑢𝑛 a sequence defined by 𝑢 0 = 0 and ∀𝑛 ≥ 0, 𝑢𝑛+1 = 2𝑢𝑛 + (𝑛 + 1). Show
      that ∀𝑛 ≥ 0, 𝑢𝑛 = 2𝑛+1 − (𝑛 + 2).
      Informal Proof: The property is true for 𝑛 = 0, since 20+1 − (0 + 2) = 0. By induction,
      assuming the property holds for 𝑛 ≥ 0, we have:
                                                       
                𝑢𝑛+1 = 2𝑢𝑛 + (𝑛 + 1) = 2 2𝑛+1 − (𝑛 + 2) + 𝑛 + 1 = 2𝑛+2 − (𝑛 + 3),
      which shows the property holds for 𝑛 + 1.

                   Fig. 2. An example of an informal proof that needs to be formalized.


   Formal methods are foundational techniques for ensuring system correctness and reliability,
grounded in rigorous mathematical approaches such as theorem proving, model checking, and
constraint solving. Despite their rigorous and provable guarantees, these techniques face signif-
icant barriers to industry adoption, primarily due to the complexity of formalizing requirement
specifications, the limited scalability of algorithms for large systems, and the substantial manual
effort involved in proof generation and validation.
   Nevertheless, recent advances in LLMs present new opportunities to address these challenges.
With their ability to process and generate natural language, structured code, and symbolic rep-
resentations, LLMs can serve as intelligent assistants, automating tedious tasks and enhancing
the capabilities of existing formal methods algorithms. This section delves into these possibilities
through targeted case studies, demonstrating how LLMs can make formal methods more efficient
and effective.

4.1    LLM for Autoformalization
Autoformalization is the process of automatically translating natural language based specifications
or informal representations into formal specifications or proofs. This complex task demands a deep
understanding of both informal and formal languages, along with the ability to generate accurate,
machine-readable formal representations. The recent advances of LLMs have opened new avenues
for automating the formalization process, which is traditionally a manual task. Recent research has
demonstrated the effectiveness of LLMs in various autoformalization scenarios, including neural
theorem proving [Jiang et al. 2022b], temporal logic generation [Murphy et al. 2024], and program
specification generation based on source code [Ma et al. 2024b]. In this section, we explore the role
of LLM agents in facilitating proof autoformalization, focusing on the challenges and opportunities
in this line of research.
    Informal proofs, commonly found in textbooks, research papers, online forums, or even generated
by LLMs, often omit details that human consider trivial or self-evident. However, to ensure rigorous
verification by theorem provers, they need to be translated into formal proofs that adhere to a
specific syntax, where all the details are explicitly provided. The challenge lies in bridging the gap
between the informal proof sketches and the detailed rigor required in formal proofs.
    Specifically, Figure 2 gives a motivating example from the miniF2F benchmark [Zheng et al. 2022].
The problem and its human-written informal proof are given, and it demonstrates a concise and
correct inductive proof. However, some intermediate steps, particularly the algebraic manipulations,
are omitted in the informal proof. Although the equation can be easily verified by human experts,
it is challenging for LLMs to infer the missing details and generate a correct formal proof due to
their limited symbolic reasoning capabilities. The following Isabelle/HOL proof snippet illustrates
an attempt by ChatGPT-3.5-turbo to formalize the given informal proof. While the model correctly
identifies the required transformations, it fails during the simplification of the term 2∗ (𝑛+2) − (𝑛+1),
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap         11


mistakenly reducing it to 2𝑛 + 3 instead of 𝑛 + 3. This example highlights the limitations of LLMs in
handling detailed algebraic reasoning without explicit guidance.
  lemma induction_seq_mul2pnp1_forn :
    fixes n :: nat and u :: " nat ⇒ nat "
    assumes h0 : " u 0 = 0"
      and h1 : " ( n :: nat ) . u ( n +1) = 2 * u n + ( n +1) "
                   Ó

      and h2 : " u n = 2 ^ ( n +1) - ( n +2) "
    shows " u ( n +1) = 2 ^ ( n +2) - ( n +3) "
  proof -
    have " u ( n +1) = 2 * u n + ( n +1) " using h1 by simp
    also have "... = 2 * (2 ^ ( n +1) - ( n +2) ) + ( n +1) " using h2 by simp
    also have "... = 2 * 2 ^ ( n +1) - (2 * ( n +2) ) + ( n +1) "
      by ( simp add : right_diff_distrib ')
    also have "... = 2 ^ ( n +2) - (2 * ( n +2) - ( n +1) ) "
      sledgehammer
    (* an error in simplification *)
    also have "... = 2 ˆ (n+2) - (2*n + 3)" by auto
    also have "... = 2 ^ ( n +2) - ( n +3) " by auto
    finally show ? thesis by blast
  qed

   To address this, we propose the use of autoformalization agents equipped with enhanced capa-
bilities for symbolic reasoning. More specifically, autoformalization agents break down the process
into manageable steps: (i) generating proof outlines, (ii) filling intermediate steps using external
tools, and (iii) integrating and refining proofs. To elaborate, the agent first constructs a high-level
proof outline, capturing the main steps of the informal proof, while leaving placeholders for missing
intermediate steps. This outline aligns with the informal proof structure and serves as a blueprint
for the following formalization process. For the missing details, especially those involving symbolic
reasoning or algebraic manipulations, the agent delegates the task to external tools like computer
algebra systems (CAS). These tools can perform accurate transformations on the mathematical
expressions, ensuring the correctness of the derived intermediate steps. Once the intermediate
steps are derived, the agent integrates them into the proof outline, filling in the placeholders and
completing the formalization. In case the agent still encounters gaps in certain steps, it iteratively
refines the proof by revisiting the informal proof and consulting external tools. In this way, the
autoformalization agents can leverage the strong symbolic reasoning capabilities of external tools
to fill in the missing details in the informal proofs, thus bridging the gap between informal and
formal proofs and specifications.

4.2   LLM for Theorem Proving
Among all formal analysis techniques, theorem proving stands out for its capability to handle
complex state spaces, abstract specifications, and highly intricate systems. Unlike model checking
(we will discuss subsequently) which is primarily designed for finite models and faces challenges
with state space explosion, theorem proving excels in leveraging mathematical reasoning to establish
properties that hold universally. This capability has been successfully demonstrated in critical
systems, such as CompCert [Leroy 2009], a formally verified C compiler that guarantees the
correctness of compiled code, and seL4 [Klein et al. 2009], a microkernel with rigorous proofs
of memory safety, functional correctness, and security properties. These examples showcase the
unmatched flexibility theorem proving offers in system verification, making it a powerful tool for
ensuring system correctness. In this section, we explore how LLMs can augment each sub-task
12                                                                                           Zhang et al.


within the theorem-proving framework, improving efficiency and enhancing accessibility for novice
users throughout the entire proving process.

4.2.1 Premise Selection. Retrieving relevant facts from a large collection of lemmas is a critical
task in theorem proving, and this process is known as premise selection. This task is typically done
manually by explicitly specifying the used lemmas in the proof scripts, which often requires trial
and error and deep domain knowledge, making it time-consuming and error-prone. Some powerful
automation techniques in interactive theorem provers (ITPs) also need premise selection to first
filter out irrelevant lemmas from the large search space. For example, Sledgehammer [Böhme
and Nipkow 2010], an effective tool for Isabelle/HOL [Paulson 1994], collects relevant facts from
the background theories and sends them to external automatic theorem provers (ATPs) and SMT
solvers to find proofs. This process involves premise selection to identify the most relevant lemmas
that can help in proving the current goal. For example, Sledgehammer usually selects about 1,000
lemmas out of tens of thousands of premises. Some heuristics [Meng and Paulson 2009] and machine
learning techniques [Kühlwein et al. 2013] like naive Bayes are used in Sledgehammer for relevant
fact selection. A recent work [Mikuła et al. 2024] proposed using transformer models to learn the
relevance of lemmas for premise selection, which improved the success rate of Sledgehammer by
13% on the miniF2F benchmark [Zheng et al. 2022].
   Our insight is that LLM agents can further improve the premise selection process by leveraging
their code understanding capabilities. Premise selection is fundamentally different from other tasks
like code retrieval, where cosine similarity is often used to identify candidates with high syntactic
resemblance. While such approaches are effective in retrieval contexts, they fall short in theorem
proving. Lemmas with similar syntactic structures to the proof goal may not necessarily be the
most useful, and conversely, the most helpful facts may exhibit little syntactic similarity. This
highlights the need for a retrieval approach grounded in the semantic understanding of lemmas,
rather than relying solely on syntactic features as most current methods do.
   LLMs, with their strong code comprehension capabilities, offer a way to address this gap. They
can infer the meaning of a lemma from its name, its definition, and its contextual information,
mimicking the reasoning process of a human expert. For instance, a human expert can intuitively
assess whether a given lemma is likely to be helpful for a particular proof goal. However, the sheer
number of lemmas in large proof libraries makes it impossible for experts to manually evaluate
and rank all possible candidates. By contrast, LLM agents can efficiently scale this process. We
can first collect definitions and contextual information of lemmas and ask LLM agents to generate
semantic descriptions in natural language for each lemma, forming a knowledge base for premise
selection. Then, given a proof goal, LLM agents comprehend the goal and generate a semantic
representation, which is used to query the knowledge base for relevant lemmas. This approach
effectively simulates the expert’s intuition across a vast number of possibilities, fully leveraging
semantics information to guide the premise selection process.

4.2.2 Proof Generation. Proof step generation is the central task in theorem proving, where the
objective is to predict one or more proof steps to construct a valid proof for a given theorem.
Many pioneering works on LLM-based proof generation [Han et al. 2022; Polu et al. 2023; Polu and
Sutskever 2020] approach this problem as a language modeling task and train LLMs on large-scale
proof corpora to predict the next proof step. Various techniques have been developed to improve
the quality of generated proofs. For instance, learning to invoke ATPs to discharge subgoals [Jiang
et al. 2022a], repairing failed proof steps by querying LLMs with the error message [First et al. 2023],
and predicting auxiliary constructions to simplify proofs [Trinh et al. 2024] have all demonstrated
significant potential.
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap          13


   However, real-world verification scenarios present challenges that go beyond these methods.
Human experts, for instance, do not solely rely on immediate proof context or predefined strategies.
Instead, they first have a high-level proof plan in mind and frequently need to consult the definitions
of important concepts or theorems during the proof process. Additionally, experts often employ a
trial-and-error approach, iteratively refining their methods to construct a valid proof. This highlights
a limitation of current LLMs when used as standalone tools: while they excel at producing plausible
proof steps, they lack the broader strategic reasoning and adaptability. This gap makes it difficult
for LLMs to consistently surpass human performance in proof generation tasks.
   To address these limitations, we propose a shift toward LLM agents that more closely emulate
human experts in their proof strategies. In contrast to standalone LLMs, these agents integrate
multiple capabilities, allowing them to reason, adapt, and interact during the proof process. This
distinction can be articulated through the following two key features:
Feature 1. Explicit Proof Intentions. A defining feature of LLM agents is their ability to generate
both proof steps and explicit proof intentions—statements that explain the reasoning or goals
underlying each step. This additional layer of information is critical for improving both automated
and human-driven refinement. When a proof step fails, the agent can use the intention, along with
error feedback, to attempt a proof repair. Even if the repair is unsuccessful, the intention provides
valuable insights for human users, streamlining their efforts to identify and resolve the issue.
Feature 2. Dynamic Retrieval of Relevant Knowledge. LLM agents go beyond the immediate
context by incorporating mechanisms to retrieve definitions, lemmas, or related theorems from
knowledge bases. This mimics how human experts consult reference materials during the proof
process but with significantly greater efficiency and scale. By dynamically identifying and incorpo-
rating relevant information, the agent can address gaps in its internal knowledge, enabling it to
construct proofs that require broad or specialized domain understanding.
   Many existing methods, such as delegating specific tasks to automated tools like Sledgehammer,
and introducing auxiliary lemmas, can be seen as attempts to replicate human expert strategies.
LLM agents can unify these capabilities into a framework, allowing them to reason about when and
how to apply these techniques. By combining these methods with explicit intentions and dynamic
knowledge retrieval, LLM agents can achieve a level of adaptability and strategic reasoning that is
closer to human expertise.
4.2.3 Case Study on LLMs with Coq. To illustrate our perspective, we illustrate our recent explo-
ration of the interaction between LLMs and Coq. Coq [Huet et al. 1997] is a classic proof assistant
based on constructive type theory, supporting functional programming and formal specification.
The integration of Coq with an LLM agent involves several key steps:
Step 1. Natural Language Understanding. The LLM agent receives natural language input from
the user, typically in the form of a mathematical theorem, conjecture, or problem.
Step 2. Formalization of the Problem. The LLM agent translates the natural language problem
into Coq’s formal language. This includes defining types, propositions, and functions necessary for
the formulation of the theorem.
Step 3. Proof Construction. The LLM agent collaborates with Coq to construct proofs, utilizing
Coq’s interactive features to propose proof steps that are subsequently verified or refined.
Step 4. Proof Verification and Feedback. Once the proof is constructed, Coq verifies its cor-
rectness. The LLM agent translates the verified proof back into natural language, providing a
comprehensible explanation of the result to the user.
  Example. Consider the following natural language query posed to the LLM agent:
     “Prove that the sum of two even numbers is even.”
14                                                                                         Zhang et al.


     The LLM agent first translates this into a formal Coq language:
     Theorem sum_of_even_numbers : forall n m : nat ,
       even n -> even m -> even ( n + m ) .

  The user needs to check the correctness of the coq code to guarantee consistency between the
natural language and coq code. Then, the LLM agent will search the related theorems and lemmas,
and construct the proof as follows:
     Proof .
       intros n m Hn Hm .
       unfold even in *.
       destruct Hn as [ k Hk ].
       destruct Hm as [ l Hl ].
       exists ( k + l ) .
       rewrite Hk , Hl .
       ring .
     Qed .

     Coq verifies this proof, and the LLM agent explains and responds in natural language:
         “The proof shows that if two numbers are even, their sum is also even by using basic
         properties of addition and the definition of even numbers.”

4.3     LLM for Model Checking
Model checking is a formal verification technique that systematically explores a system’s state space
to check if the system satisfies specified properties, such as safety and liveness. It is particularly
effective for finite-state systems, providing automated detection of logical errors like deadlocks or
critical system property violations. However, traditional model checking faces great limitations,
including scalability challenges for large systems and the complexity involved in system modeling
and property formalization.
   In this section, we illustrate how model checking agents can alleviate above limitations by
combining the strengths of LLMs. Leveraging the respective advantages, a model checking agent
accepts a system description in natural language from the user, generates corresponding processes
using an LLM, and refines them iteratively based on feedback from the model checker. We note
that this refinement can be facilitated by an Automated Prompt Engineer (APE) [Cheng et al. 2023;
Zhou et al. 2022], which optimizes the interaction between the LLM and the model checker. This
synergy not only streamlines the model checking process but also enhances its accessibility for
users without extensive expertise in formal verification.
4.3.1 Overview. The overall workflow for building a model checking agent should include the
following steps:
Step 1. Natural Language Input. Users provide a description of a system in natural language,
specifying desired behaviors or properties. For instance, they might describe a mutual exclusion
protocol or outline expected system behaviors.
Step 2. LLM Planning. An LLM with strong reasoning capabilities translates the natural language
input into a detailed, structured plan. This plan breaks down the system description into specific
instructions, including a one-to-one mapping of logical steps, such as defining variables, specifying
state transitions, and drafting preliminary assertions.
Step 3. LLM Code (Assertion) Completion. Following the structured plan, a specialized LLM
trained in syntax and logic generates the code and assertions required to implement the system.
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap          15


This generation is treated as a completion task, where the model fills in the details based on the
planning phase rather than creating the code from scratch. The structured approach enhances
precision and reduces the likelihood of errors in the generated outputs.
Step 4. Verification. The generated code and assertions are submitted to an automated verification
tool. This tool evaluates the artifacts to ensure they comply with the logical properties and behaviors
specified in the initial input.
Step 5. Feedback Generation. Feedback from the formal verification tool highlights issues such
as syntax errors or logical inconsistencies. This feedback is processed by an APE, which refines the
LLM’s prompts and provides updated instructions.
Step 6. Iterative Improvement. The LLM iteratively refines the code and assertions based on
feedback until all formal verification checks are successfully passed. Through this iterative process,
the framework ensures that the final system model is logically sound, adheres to the desired
specifications, and is ready for deployment.
  In the following part, we demonstrate our model checking agent framework utilizing the widely
adopted model checker, Process Analysis Toolkit (PAT) [Liu et al. 2011; Sun et al. 2008]. This
demonstration highlights how the integration of formal methods and LLMs can be interactively
harnessed to develop the PAT Agent, showcasing the potential of this synergy in enhancing
verification processes.

4.3.2 PAT Agent. Process Analysis Toolkit (PAT) is a formal verification tool designed to model,
simulate, and verify concurrent and real-time systems. It supports the verification of key properties
such as deadlock-freeness, reachability, and refinement, addressing critical correctness and reliability
concerns in system design. With applications spanning domains such as vehicle and aircraft
safety, resource optimization, and complex system analysis, PAT provides a robust foundation for
developing a model checking agent.
   In the following motivating example, we illustrate how the PAT Agent can be used to derive
verified system constructs, starting from natural language instructions.

  Example. In the development of a car system, ensuring that the key is never locked inside the
car is a critical requirement. This safeguard is essential for user convenience and safety, as locking
the key inside could result in costly locksmith services, delays, or emergencies in dangerous areas.
The system must ensure logical consistency in different operations to avoid such consequences.
  We begin by asking an LLM (gpt-4o-2024-08-06) to directly generate a formal model based on a
high-level description. While the LLM has learned syntax rules and demonstrates effective planning
capabilities, the generated model contains a critical logic flaw: it allows the key to be locked inside
the car. This issue arises due to hallucination by GPT-4o, which incorrectly assumes that placing
the key into a currently locked car is a valid scenario, contradicting commonsense reasoning.

  [ key == i && owner [ i ] == near ] leavekey { key = incar ;}

   Consequently, the resulting system design deviates from the intended behavior, compromising
its reliability and safety.
   To address this issue, we use PAT to formally verify the generated system. PAT identifies an error
trace (i.e., a sequence of operations) that leads to the key being locked inside the car, providing
feedback that highlights flaws in the logic governing key and door operations. By analyzing this
error trace, the LLM identifies the aforementioned logical flaw and corrects it by imposing stricter
restrictions on when the key can be left inside the car. Additionally, it establishes clear conditions
for locking the door, ensuring alignment with the intended system behavior.
16                                                                                           Zhang et al.



     [ key == i && owner [ i ] == near && door == open ]
     leavekey { key = incar ;}


     [( owner [ i ] == near && key == i ) || owner [ i ] == in ]
     lockdoor . i { door = lock ;}

  The refined model, guided by PAT’s feedback, results in a system that can now be formally
verified to ensure the key will never be locked inside the car. This example highlights the powerful
synergy between formal verification and LLM-driven development. LLMs ease the process of
system development, while tools like PAT provide rigorous guarantees by identifying and rectifying
logical inconsistencies. Together, they create a robust and user-friendly approach to formal system
development, ensuring critical requirements are met with precision.
   Prototype. To implement the PAT model checking agent, we build it on the LangChain pipeline,
leveraging its streamlined implementation and modularized memory system to efficiently manage
intermediate states and iterative refinements during formal verification. This allows seamless
integration of LLM capabilities with formal verification tools. We illustrate the prototype in Figure 3.




                                      Fig. 3. PAT Agent Prototype.

   The PAT Agent prototype follows a structured workflow that seamlessly integrates formal
verification with LLM capabilities. Starting with natural language descriptions provided by the user,
the Planning LLM translates these into structured instructions, specifying logical components such
as state transitions and properties to verify. These instructions are passed to the Code Generation
LLM, which generates formal code with knowledge learned from the syntax and semantic datasets
as a completion task. The generated code is then verified with the PAT model checker, evaluating
key properties such as deadlock-freeness and reachability. If verification fails, the APE refines the
instructions based on feedback from PAT, iteratively improving the code until it meets the specified
properties. By uniting the strengths of LLMs and formal verification, the PAT Agent exemplifies
how model checking agents can enable reliable and accessible system development.
4.3.3 Other Model Checking Agents. We acknowledge that such an agent framework is highly
generalizable and can be adapted for tools like Alloy Analyzer [Jackson 2000], PRISM [Kwiatkowska
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap        17


et al. 2002], UPPAAL [Behrmann et al. 2004], etc. Its modular design enables the Planning LLM to
learn tool-specific semantics and the Code Generation LLM to produce corresponding formal code
and assertions. By tailoring feedback and refinement loops for each tool, the framework seamlessly
integrates LLM-driven development with diverse formal verification processes.

5     UNIFYING THE POWER OF FMS AND LLMS
This section highlights the synergy between FMs and LLMs, combining the rigor of formal methods
with the flexibility and intelligence of LLMs. By integrating these two approaches, we can create
robust systems that enhance both the trustworthiness and efficiency of software engineering
processes while adapting to complex and real-world problems. We demonstrate this idea through
an application: trustworthy code generation.
  We acknowledge that using an LLM for program synthesis involves leveraging its ability to
understand and generate code snippets, solve programming problems, and create software systems
based on high-level requirements. This integration aims to leverage the LLM agent’s ability to
understand natural language, translate program specifications and code into formal properties, and
assist in verifying correctness using automated verification tools.

5.1    Challenges of LLMs for Program Synthesis
LLMs have made rapid advancements in mathematics, reasoning, and programming [Romera-
Paredes et al. 2023; Zhao et al. 2023], significantly reshaping the landscape of software development
and computational problem-solving. Industrial-grade LLMs like GPT-4 [OpenAI and co. 2023]
and tools like GitHub Copilot [GitHub 2023] have emerged as powerful assistants for program-
mers, automating coding-related tasks and achieving performances exceeding the 50th percentile
in competitive programming contests [Pandey et al. 2024]. These achievements highlight the
transformative potential of LLMs in enhancing productivity and reducing manual effort in coding.
   However, despite these advancements, LLMs face significant challenges, notably the issue of
hallucination. This phenomenon undermines their reliability in critical contexts. User studies [Ding
et al. 2023; Vaithilingam et al. 2022] have revealed that programmers often struggle to trust and
debug LLM-generated code due to the opaqueness and lack of control over the generation process.
Alarmingly, empirical research indicates that over half of ChatGPT’s responses to programming-
related queries contain inaccuracies [Kabir et al. 2024], exacerbating concerns about their utility in
professional and high-stakes environments. Even worse, recently, mathematicians have proven
that hallucinations in LLMs are unavoidable [Xu et al. 2024].
   These challenges underscore the urgent need for strategies to mitigate hallucination and improve
the transparency and trustworthiness of LLM-generated code, paving the way for their broader
adoption in critical programming workflows.

5.2    Program Refinement
The task of program refinement has a rich history, dating back to foundational works such as [Dijk-
stra et al. 1976; Floyd 1993; Hoare 1969]. The related theories [Back and von Wright 1990; Morgan
1990] are based on Hoare logic and the calculus of weakest preconditions. Recent advancements
have extended these foundational ideas by formalizing the refinement calculus within interactive
theorem provers. Notable examples include the work in Isabelle [Foster et al. 2020] and Coq [Alpuim
and Swierstra 2018; Sall et al. 2019], leveraging the expressive power of these tools to mechanize
and verify program refinements. The Coq proof assistant, in particular, has been instrumental in
encoding and verifying complex refinement relations [Barras et al. 1999].
18                                                                                         Zhang et al.


  Formally, the refinement relation between programs is grounded in their weakest preconditions,
enabling precise definitions and automated verification [Butler and Långbacka 1996]. This formal-
ism ensures correctness and supports incremental development by iteratively refining abstract
specifications into concrete implementations while maintaining rigorous correctness guarantees.
These developments mark a significant step forward in the use of formal methods for program
synthesis and verification. For program 𝑆 and postcondition 𝑃, 𝑤𝑝 (𝑆, 𝑃) represents the weakest
precondition where S is guaranteed to terminate in a state satisfying 𝑃. Program 𝑆 0 is refined by 𝑆 1
denoted as 𝑆 0 ⊑ 𝑆 1 , iff
                                      ∀𝑃, 𝑤𝑝 (𝑆 0, 𝑃) → 𝑤𝑝 (𝑆 1, 𝑃)                                (1)
which states that 𝑆 1 will preserve the total correctness of program 𝑆 0 . The program refinement can
be established in a linear sequence:
                                      𝑆 0 ⊑ 𝑆 1 ⊑ 𝑆 2 ⊑ 𝑆 3 ... ⊑ 𝑆𝑛                               (2)
which shows the refinement 𝑆 0 ⊑ 𝑆𝑛 with the transitivity of the refinement relation.

5.3   Integrating Formal Program Refinement with LLMs
The refinement calculus [Back and von Wright 1990; Carrington et al. 1998; Morgan 1990; Sall
et al. 2019; Swierstra and Alpuim 2016] provides a rigorous framework for the stepwise refinement
method of program construction. This approach involves specifying a program’s required behavior
as an abstract, non-executable specification, which is systematically transformed into an executable
program through a series of correctness-preserving steps. By ensuring that each step maintains the
program’s intended semantics, the refinement calculus offers a sound methodology for constructing
reliable software.
5.3.1 Technical Challenges. Despite its strengths, the refinement process is traditionally performed
manually, making it a labor-intensive and error-prone task. The reliance on human effort to translate
abstract specifications into executable code not only slows down development but also increases
the risk of introducing subtle mistakes during transformation. This bottleneck has long been a
barrier to scaling the benefits of refinement calculus to larger, more complex software systems.
   Given the advancements in LLMs, integrating their powerful code-generation capabilities into
the refinement process presents an exciting opportunity. LLMs can assist in automating parts of the
transformation, bridging the gap between high-level specifications and executable implementations
while adhering to the principles of correctness-preserving refinement. This integration could
significantly reduce the manual effort required, streamline the refinement process, and open new
avenues for leveraging LLMs in formal methods and program synthesis.
5.3.2 Our Insights. Figure 4 shows an overview of our approach. Generally, it can be divided
into two parts: the formal and informal systems. We define the formal specification language and
program language in the formal system. The formal specification will first be transformed into
an abstract syntax tree. Then, with one specific law, it will formally transform the specification
into the new specification and build the proviso constraints of the law. Finally, after extracting the
generated code from LLM, it will automatically build the proof obligations and the verification
scripts for ATPs to verify. ATPs will try to verify the scripts automatically and output the success
or error message. If the code fails to verify, it will provide feedback to the LLM with possible
counterexamples.
   In the informal system, the user needs to first formalize the natural language specification into a
formal specification with the aid of the LLM. Secondly, it will build the prompt and describe the
refinement laws to the LLM. Then, the LLM selects one refinement law based on the specification’s
description and constraints and generates the associate code. The LLM will regenerate the code
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap       19




                Fig. 4. Overview of the tool that combines LLMs and program refinement.



based on the verification result. If multiple failures occur, our method will backtrack to the last
refinement step, interact with the LLM again to choose another refinement law, re-generate the
associated code, and then proceed as previously.

6   CONCLUSION AND DISCUSSION
This paper presents a roadmap for the fusion of Large Language Models and Formal Methods
to construct next-generation trustworthy AI agents/systems. By leveraging the complementary
strengths of LLMs (adaptability, natural language processing, and intelligence) and FMs (rigorous
reasoning, verification, and provable guarantees), we propose a synergistic framework to address the
limitations of both paradigms. Through case studies and conceptual explorations, we demonstrate
the transformative potential of integrating these technologies in applications such as program
synthesis. This convergence not only paves the way for robust AI systems capable of solving
complex real-world problems but also provides a foundational step toward bridging neural learning
and symbolic reasoning for enhanced trustworthiness in AI-driven systems.
   Indeed, the tight integration of LLMs and FMs raises several significant technical and practical
challenges. On the technical front, achieving seamless communication between these paradigms
demands a sophisticated mechanism for translating natural language based specifications into
formal representations and vice versa. This translation must be accurate, scalable, and contextually
adaptable to maintain the integrity of both paradigms. Additionally, LLMs’ inherent issues with
hallucinations and logical inconsistencies pose a barrier to their deployment in safety-critical
domains. Incorporating certification mechanisms is essential for mitigating these risks and ensuring
system reliability. From a practical perspective, the usability and accessibility of these integrated
systems require careful consideration. Specifically, the adaptability must be carefully balanced
with robust safeguards to address potential misuse or misinterpretation of outputs, particularly
in high-stakes scenarios. An equally critical concern is the protection of client privacy, as formal
verification tools and LLM agents often process sensitive or proprietary data. Ensuring privacy
requires implementing secure data-handling protocols, such as local deployment of tools, encrypted
communication, and adherence to strict data governance policies. Future research should focus
on developing user-friendly tools that not only retain the rigor of formal methods and simplify
interactions for users without formal engineering expertise but also incorporate robust privacy-
preserving mechanisms to safeguard client information.
20                                                                                                               Zhang et al.


REFERENCES
Ralph Abboud, Ismail Ceylan, Thomas Lukasiewicz, and Tommaso Salvatori. 2020. Boxe: A box embedding model for
    knowledge base completion. Advances in Neural Information Processing Systems 33 (2020), 9649–9661.
Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko
    Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. Gpt-4 technical report. arXiv preprint arXiv:2303.08774 (2023).
Chirag Agarwal, Sree Harsha Tanneru, and Himabindu Lakkaraju. 2024. Faithfulness vs. plausibility: On the (un) reliability
    of explanations from large language models. arXiv preprint arXiv:2402.04614 (2024).
João Alpuim and Wouter Swierstra. 2018. Embedding the refinement calculus in Coq. Science of Computer Programming 164
    (2018), 37–48. https://doi.org/10.1016/j.scico.2017.04.003 Special issue of selected papers from FLOPS 2016.
Gleifer Vaz Alves, Louise Dennis, and Michael Fisher. 2021. A double-level model checking approach for an agent-based
    autonomous vehicle and road junction regulations. Journal of Sensor and Actuator Networks 10, 3 (2021), 41.
Paolo Arcaini, Silvia Bonfanti, Angelo Gargantini, Atif Mashkoor, and Elvinia Riccobene. 2018. Integrating formal methods
    into medical software development: The ASM approach. Science of Computer Programming 158 (2018), 148–167.
Sören Auer, Christian Bizer, Georgi Kobilarov, Jens Lehmann, Richard Cyganiak, and Zachary Ives. 2007. DBpedia: A
    Nucleus for a Web of Open Data. In The Semantic Web, Karl Aberer, Key-Sun Choi, Natasha Noy, Dean Allemang, Kyung-Il
    Lee, Lyndon Nixon, Jennifer Golbeck, Peter Mika, Diana Maynard, Riichiro Mizoguchi, Guus Schreiber, and Philippe
    Cudré-Mauroux (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 722–735.
Ralph-Johan R Back and Joakim von Wright. 1990. Refinement concepts formalised in higher order logic. Formal Aspects of
    Computing 2 (1990), 247–272.
Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Yann Coscoy, David Delahaye, Daniel de Rauglaudre,
    Jean-Christophe Filliâtre, Eduardo Giménez, Hugo Herbelin, et al. 1999. The Coq proof assistant reference manual. INRIA,
    version 6, 11 (1999), 17–21.
Gerd Behrmann, Alexandre David, and Kim G Larsen. 2004. A tutorial on uppaal. Formal methods for the design of real-time
    systems (2004), 200–236.
Maciej Besta, Lorenzo Paleari, Ales Kubicek, Piotr Nyczyk, Robert Gerstenberger, Patrick Iff, Tomasz Lehmann, Hubert
    Niewiadomski, and Torsten Hoefler. 2024. CheckEmbed: Effective Verification of LLM Solutions to Open-Ended Tasks.
    arXiv preprint arXiv:2406.02524 (2024).
Sascha Böhme and Tobias Nipkow. 2010. Sledgehammer: Judgement Day. In Automated Reasoning, Jürgen Giesl and Reiner
    Hähnle (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 107–121.
Kurt Bollacker, Robert Cook, and Patrick Tufts. 2007. Freebase: A Shared Database of Structured General Human Knowledge.
    In Proceedings of the 22nd National Conference on Artificial Intelligence - Volume 2 (Vancouver, British Columbia, Canada)
    (AAAI’07). AAAI Press, 1962–1963.
Michael Butler and Thomas Långbacka. 1996. Program derivation using the refinement calculator. In Theorem Proving
    in Higher Order Logics, Gerhard Goos, Juris Hartmanis, Jan van Leeuwen, Joakim von Wright, Jim Grundy, and John
    Harrison (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 93–108.
DAVID Carrington, I Hayes, Ray Nickson, Geoffrey Watson, and Jim Welsh. 1998. A program refinement tool. Formal
    Aspects of Computing 10 (1998), 97–124.
Jifan Chen, Grace Kim, Aniruddh Sriram, Greg Durrett, and Eunsol Choi. 2024. Complex Claim Verification with Evidence
    Retrieved in the Wild. In Proceedings of the 2024 Conference of the North American Chapter of the Association for
    Computational Linguistics: Human Language Technologies (Volume 1: Long Papers). 3569–3587.
Chih-Hong Cheng, Changshun Wu, Harald Ruess, Xingyu Zhao, and Saddek Bensalem. 2024. Formal Specification,
    Assessment, and Enforcement of Fairness for Generative AIs. arXiv preprint arXiv:2404.16663 (2024).
Jiale Cheng, Xiao Liu, Kehan Zheng, Pei Ke, Hongning Wang, Yuxiao Dong, Jie Tang, and Minlie Huang. 2023. Black-box
    prompt optimization: Aligning large language models without model training. arXiv preprint arXiv:2311.04155 (2023).
Team Claude. 2024. The Claude 3 Model Family: Opus, Sonnet, Haiku. https://api.semanticscholar.org/CorpusID:268232499
Roi Cohen, May Hamri, Mor Geva, and Amir Globerson. 2023. LM vs LM: Detecting Factual Errors via Cross Examination.
    In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, Houda Bouamor, Juan Pino,
    and Kalika Bali (Eds.).
Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for the Construction and
    Analysis of Systems, C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 337–340.
Shujie Deng, Honghua Dong, and Xujie Si. 2024. Enhancing and Evaluating Logical Reasoning Abilities of Large Language
    Models. In ICLR 2024 Workshop on Secure and Trustworthy Large Language Models. https://openreview.net/forum?id=
    xw06d8NQAd
Edsger W Dijkstra, Edsger Wybe Dijkstra, Edsger Wybe Dijkstra, and Edsger Wybe Dijkstra. 1976. A discipline of programming.
    Vol. 613924118. prentice-hall Englewood Cliffs.
Hantian Ding, Varun Kumar, Yuchen Tian, Zijian Wang, Rob Kwiatkowski, Xiaopeng Li, Murali Krishna Ramanathan,
    Baishakhi Ray, Parminder Bhatia, Sudipta Sengupta, Dan Roth, and Bing Xiang. 2023. A Static Evaluation of Code
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap                               21


   Completion by Large Language Models. arXiv:2306.03203 [cs.CL]
Iulia Dragomir, Carlos Redondo, Tiago Jorge, Laura Gouveia, Iulian Ober, Ivan Kolesnikov, Marius Bozga, and Maxime
   Perrotin. 2022. Model-checking of space systems designed with TASTE/SDL. In Proceedings of the 25th International
   Conference on Model Driven Engineering Languages and Systems: Companion Proceedings. 237–246.
Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-proof generation and repair with large language
   models. In The 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software
   Engineering. 1229–1241.
Robert W Floyd. 1993. Assigning meanings to programs. In Program Verification: Fundamental Issues in Computer Science.
   Springer, 65–81.
Simon Foster, Jonathan Julián Huerta y Munive, and Georg Struth. 2020. Differential Hoare logics and refinement calculi for
   hybrid systems with Isabelle/HOL. In Relational and Algebraic Methods in Computer Science: 18th International Conference,
   RAMiCS 2020, Palaiseau, France, October 26–29, 2020, Proceedings 18. Springer, 169–186.
Leo Freitas, William E Scott III, and Patrick Degenaar. 2020. Medicine-by-wire: Practical considerations on formal techniques
   for dependable medical systems. Science of Computer Programming 200 (2020), 102545.
Team Gemini. 2024. Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805 [cs.CL] https://arxiv.org/
   abs/2312.11805
GitHub. 2023. GitHub Copilot. https://github.com/features/copilot
Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward Ayers, and Stanislas Polu. 2022. Proof Artifact Co-Training for Theorem
   Proving with Language Models. In International Conference on Learning Representations. https://openreview.net/forum?
   id=rpxJc9j04U
Joy He-Yueya, Gabriel Poesia, Rose E Wang, and Noah D Goodman. 2023. Solving math word problems by combining
   language models with symbolic solvers. arXiv preprint arXiv:2304.09102 (2023).
Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2021. Measuring
   Massive Multitask Language Understanding. In 9th International Conference on Learning Representations, ICLR 2021,
   Virtual Event, Austria, May 3-7, 2021.
Charles Antony Richard Hoare. 1969. An axiomatic basis for computer programming. Commun. ACM 12, 10 (1969), 576–580.
Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, Junteng Liu, Chuancheng Lv, Yikai
   Zhang, Jiayi Lei, Yao Fu, Maosong Sun, and Junxian He. 2023. C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation
   Suite for Foundation Models. In Advances in Neural Information Processing Systems 36: Annual Conference on Neural
   Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, Alice Oh, Tristan
   Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine (Eds.).
Zhen Huang, Bo Li, DeHui Du, and Qin Li. 2022. A Model Checking Based Approach to Detect Safety-Critical Adversarial
   Examples on Autonomous Driving Systems. In International Colloquium on Theoretical Aspects of Computing. Springer,
   238–254.
Gérard Huet, Gilles Kahn, and Christine Paulin-Mohring. 1997. The coq proof assistant a tutorial. Rapport Technique 178
   (1997).
Daniel Jackson. 2000. Automating first-order relational logic. In Proceedings of the 8th ACM SIGSOFT international symposium
   on Foundations of software engineering: twenty-first century applications. 130–139.
Alon Jacovi and Yoav Goldberg. 2020. Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate
   Faithfulness?. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. 4198–4205.
Raoul Jetley, S Purushothaman Iyer, and P Jones. 2006. A formal methods approach to medical device review. Computer 39,
   4 (2006), 61–67.
Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu,
   and Mateja Jamnik. 2022a. Thor: Wielding hammers to integrate language models and automated theorem provers.
   Advances in Neural Information Processing Systems 35 (2022), 8360–8373.
Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix, Yuhuai Wu, and
   Guillaume Lample. 2022b. Draft, sketch, and prove: Guiding formal theorem provers with informal proofs. arXiv preprint
   arXiv:2210.12283 (2022).
Samia Kabir, David N. Udo-Imeh, Bonan Kou, and Tianyi Zhang. 2024. Is Stack Overflow Obsolete? An Empirical Study of
   the Characteristics of ChatGPT Answers to Stack Overflow Questions. In Proceedings of the CHI Conference on Human
   Factors in Computing Systems (Honolulu, HI, USA) (CHI ’24). Association for Computing Machinery, New York, NY, USA,
   Article 935, 17 pages. https://doi.org/10.1145/3613904.3642596
Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dhammika Elkaduwe,
   Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. 2009. seL4:
   formal verification of an OS kernel. In Proceedings of the ACM SIGOPS 22nd Symposium on Operating Systems Principles
   (Big Sky, Montana, USA) (SOSP ’09). Association for Computing Machinery, New York, NY, USA, 207–220. https:
   //doi.org/10.1145/1629575.1629596
22                                                                                                                Zhang et al.


Lukas König, Christian Heinzemann, Alberto Griggio, Michaela Klauck, Alessandro Cimatti, Franziska Henze, Stefano
   Tonetta, Stefan Küperkoch, Dennis Fassbender, and Michael Hanselmann. 2024. Towards Safe Autonomous Driving:
    Model Checking a Behavior Planner during Development. In International Conference on Tools and Algorithms for the
    Construction and Analysis of Systems. Springer, 44–65.
Daniel Kühlwein, Jasmin Christian Blanchette, Cezary Kaliszyk, and Josef Urban. 2013. MaSh: Machine Learning for
    Sledgehammer. In Interactive Theorem Proving, Sandrine Blazy, Christine Paulin-Mohring, and David Pichardie (Eds.).
    Springer Berlin Heidelberg, Berlin, Heidelberg, 35–50.
Marta Kwiatkowska, Gethin Norman, and David Parker. 2002. PRISM: Probabilistic symbolic model checker. In International
    Conference on Modelling Techniques and Tools for Computer Performance Evaluation. Springer, 200–204.
Xavier Leroy. 2009. Formal verification of a realistic compiler. Commun. ACM 52, 7 (July 2009), 107–115. https://doi.org/10.
    1145/1538788.1538814
Ningke Li, Yuekang Li, Yi Liu, Ling Shi, Kailong Wang, and Haoyu Wang. 2024a. Drowzee: Metamorphic Testing for
    Fact-Conflicting Hallucination Detection in Large Language Models. Proc. ACM Program. Lang. 8, OOPSLA2, Article 336
   (Oct. 2024), 30 pages. https://doi.org/10.1145/3689776
Yixuan Li, Julian Parsert, and Elizabeth Polgreen. 2024b. Guiding enumerative program synthesis with large language
    models. In International Conference on Computer Aided Verification. Springer, 280–301.
Ke Liang, Lingyuan Meng, Meng Liu, Yue Liu, Wenxuan Tu, Siwei Wang, Sihang Zhou, Xinwang Liu, and Fuchun Sun. 2022.
    Reasoning over different types of knowledge graphs: Static, temporal and multi-modal. arXiv preprint arXiv:2212.05767
   (2022).
Jing Liu, Tengfei Li, Zuohua Ding, Yuqing Qian, Haiying Sun, and Jifeng He. 2019. AADL+: a simulation-based methodology
    for cyber-physical systems. Frontiers of Computer Science 13 (2019), 516–538.
Yang Liu, Jun Sun, and Jin Song Dong. 2011. PAT 3: An Extensible Architecture for Building Multi-domain Model
    Checkers. In IEEE 22nd International Symposium on Software Reliability Engineering, ISSRE 2011, Hiroshima, Japan,
    November 29 - December 2, 2011, Tadashi Dohi and Bojan Cukic (Eds.). IEEE Computer Society, 190–199. https:
   //doi.org/10.1109/ISSRE.2011.19
Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2024b. SpecGen: Automated Generation of Formal Program
    Specifications via Large Language Models. arXiv:2401.08807 [cs.SE] https://arxiv.org/abs/2401.08807
Yubo Ma, Zhibin Gou, Junheng Hao, Ruochen Xu, Shuohang Wang, Liangming Pan, Yujiu Yang, Yixin Cao, Aixin Sun, Hany
   Awadalla, et al. 2024a. Sciagent: Tool-augmented language models for scientific reasoning. arXiv preprint arXiv:2402.11451
   (2024).
Potsawee Manakul, Adian Liusie, and Mark Gales. 2023. SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection
    for Generative Large Language Models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language
    Processing. 9004–9017.
Jia Meng and Lawrence C. Paulson. 2009. Lightweight relevance filtering for machine-generated resolution problems.
    Journal of Applied Logic 7, 1 (2009), 41–57. https://doi.org/10.1016/j.jal.2007.07.004 Special Issue: Empirically Successful
    Computerized Reasoning.
Maciej Mikuła, Szymon Tworkowski, Szymon Antoniak, Bartosz Piotrowski, Albert Q. Jiang, Jin Peng Zhou, Christian Szegedy,
    Łukasz Kuciński, Piotr Miłoś, and Yuhuai Wu. 2024. Magnushammer: A Transformer-Based Approach to Premise Selection.
    In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=oYjPk8mqAV
George A. Miller. 1995. WordNet: A Lexical Database for English. Commun. ACM 38, 11 (nov 1995), 39–41. https:
   //doi.org/10.1145/219717.219748
Carroll Morgan. 1990. Programming from Specifications. Prentice-Hall, Inc., USA.
William Murphy, Nikolaus Holzer, Nathan Koenig, Leyi Cui, Raven Rothkopf, Feitong Qiao, and Mark Santolucito. 2024.
    Guiding LLM Temporal Logic Generation with Explicit Separation of Data and Control. arXiv:2406.07400 [cs.LG]
    https://arxiv.org/abs/2406.07400
OpenAI and co. 2023. GPT-4 Technical Report. arXiv:2303.08774 [cs.CL]
Liangming Pan, Alon Albalak, Xinyi Wang, and William Wang. 2023. Logic-LM: Empowering Large Language Models with
    Symbolic Solvers for Faithful Logical Reasoning. In Findings of the Association for Computational Linguistics: EMNLP 2023.
    3806–3824.
Ruchika Pandey, Prabhat Singh, Raymond Wei, and Shaila Shankar. 2024. Transforming Software Development: Evaluating
    the Efficiency and Challenges of GitHub Copilot in Real-World Projects. arXiv:2406.17910 [cs.SE] https://arxiv.org/abs/
    2406.17910
Lawrence C Paulson. 1994. Isabelle: A generic theorem prover. Springer.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya Sutskever. 2023. Formal
    Mathematics Statement Curriculum Learning. In The Eleventh International Conference on Learning Representations.
    https://openreview.net/forum?id=-P7G-8dmSh4
The Fusion of Large Language Models and Formal Methods for Trustworthy AI Agents: A Roadmap                              23


Stanislas Polu and Ilya Sutskever. 2020. Generative Language Modeling for Automated Theorem Proving. CoRR (2020).
   arXiv:2009.03393 [cs.LG] https://arxiv.org/abs/2009.03393
Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien
   Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al. 2023. Mathematical discoveries from
   program search with large language models. Nature (2023), 1–3.
Boubacar Demba Sall, Frédéric Peschanski, and Emmanuel Chailloux. 2019. A Mechanized Theory of Program Refinement.
   In Formal Methods and Software Engineering: 21st International Conference on Formal Engineering Methods, ICFEM 2019,
   Shenzhen, China, November 5–9, 2019, Proceedings (Shenzhen, China). Springer-Verlag, Berlin, Heidelberg, 305–321.
   https://doi.org/10.1007/978-3-030-32409-4_19
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. 2024. Towards large language models as copilots for theorem proving
   in lean. arXiv preprint arXiv:2404.12534 (2024).
Elias Stengel-Eskin, Archiki Prasad, and Mohit Bansal. 2024. ReGAL: Refactoring Programs to Discover Generalizable
   Abstractions. arXiv:2401.16467 [cs.SE] https://arxiv.org/abs/2401.16467
Fabian M. Suchanek, Gjergji Kasneci, and Gerhard Weikum. 2007. Yago: A Core of Semantic Knowledge. In Proceedings of
   the 16th International Conference on World Wide Web (Banff, Alberta, Canada) (WWW ’07). Association for Computing
   Machinery, New York, NY, USA, 697–706. https://doi.org/10.1145/1242572.1242667
Jun Sun, Yang Liu, and Jin Song Dong. 2008. Model checking CSP revisited: Introducing a process analysis toolkit. In
   International symposium on leveraging applications of formal methods, verification and validation. Springer, 307–322.
Wouter Swierstra and Joao Alpuim. 2016. From Proposition to Program: Embedding the Refinement Calculus in Coq. In
   Functional and Logic Programming: 13th International Symposium, FLOPS 2016, Kochi, Japan, March 4-6, 2016, Proceedings
   13. Springer, 29–44.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière,
   Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample.
   2023. LLaMA: Open and Efficient Foundation Language Models. arXiv:2302.13971 [cs.CL] https://arxiv.org/abs/2302.13971
Trieu Trinh, Yuhuai Tony Wu, Quoc Le, He He, and Thang Luong. 2024. Solving Olympiad geometry without human
   demonstrations. Nature 625 (2024), 476–482. https://www.nature.com/articles/s41586-023-06747-5
Priyan Vaithilingam, Tianyi Zhang, and Elena L Glassman. 2022. Expectation vs. experience: Evaluating the usability of code
   generation tools powered by large language models. In Chi conference on human factors in computing systems extended
   abstracts. 1–7.
Chengpeng Wang, Wuqi Zhang, Zian Su, Xiangzhe Xu, Xiaoheng Xie, and Xiangyu Zhang. 2024. When Dataflow Analysis
   Meets Large Language Models. arXiv preprint arXiv:2402.10754 (2024).
Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong Tian. 2024.
   Enchanting program specification synthesis by large language models using static analysis and program verification. In
   International Conference on Computer Aided Verification. Springer, 302–328.
Sarah Wiegreffe and Ana Marasovic. 2020. Teach Me to Explain: A Review of Datasets for Explainable Natural Language
   Processing. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 1).
Haoze Wu, Clark W. Barrett, and Nina Narodytska. 2024. Lemur: Integrating Large Language Models in Automated Program
   Verification. In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11,
   2024.
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and Christian Szegedy. 2022.
   Autoformalization with large language models. Advances in Neural Information Processing Systems 35 (2022), 32353–32368.
Ziwei Xu, Sanjay Jain, and Mohan Kankanhalli. 2024. Hallucination is Inevitable: An Innate Limitation of Large Language
   Models. arXiv:2401.11817 [cs.CL] https://arxiv.org/abs/2401.11817
Kaiyu Yang and Jia Deng. 2019. Learning to prove theorems via interacting with proof assistants. In International Conference
   on Machine Learning. PMLR, 6984–6994.
Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree
   Anandkumar. 2024. Leandojo: Theorem proving with retrieval-augmented language models. Advances in Neural
   Information Processing Systems 36 (2024).
Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett. 2024. Satlm: Satisfiability-aided language models using declarative
   prompting. Advances in Neural Information Processing Systems 36 (2024).
Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang,
   Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang
   Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. 2023. A Survey of Large Language Models. arXiv:2303.18223 [cs.CL]
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. 2022. miniF2F: a cross-system benchmark for formal Olympiad-level
   mathematics. In International Conference on Learning Representations. https://openreview.net/forum?id=9ZPegFuFTFv
Wanjun Zhong, Ruixiang Cui, Yiduo Guo, Yaobo Liang, Shuai Lu, Yanlin Wang, Amin Saied, Weizhu Chen, and Nan Duan.
   2024. AGIEval: A Human-Centric Benchmark for Evaluating Foundation Models. In Findings of the Association for
24                                                                                                           Zhang et al.


    Computational Linguistics: NAACL 2024. 2299–2314.
Jin Peng Zhou, Charles Staats, Wenda Li, Christian Szegedy, Kilian Q. Weinberger, and Yuhuai Wu. 2024. Don’t Trust: Verify
   - Grounding LLM Quantitative Reasoning with Autoformalization. In The Twelfth International Conference on Learning
    Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024.
Kun Zhou, Yutao Zhu, Zhipeng Chen, Wentong Chen, Wayne Xin Zhao, Xu Chen, Yankai Lin, Ji-Rong Wen, and Jiawei Han.
    2023. Don’t make your llm an evaluation benchmark cheater. arXiv preprint arXiv:2311.01964 (2023).
Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. 2022. Large
    language models are human-level prompt engineers. arXiv preprint arXiv:2211.01910 (2022).
Zili Zhou, Shaowu Liu, Guandong Xu, and Wu Zhang. 2019. On completing sparse knowledge base with transitive relation
    embedding. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 33. 3125–3132.
