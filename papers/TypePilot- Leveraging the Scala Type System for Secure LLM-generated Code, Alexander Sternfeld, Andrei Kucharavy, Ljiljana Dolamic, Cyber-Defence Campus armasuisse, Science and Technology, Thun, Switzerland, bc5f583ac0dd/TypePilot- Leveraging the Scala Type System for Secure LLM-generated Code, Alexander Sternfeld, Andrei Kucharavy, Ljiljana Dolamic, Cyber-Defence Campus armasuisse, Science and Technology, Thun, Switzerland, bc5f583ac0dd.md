    TypePilot: Leveraging the Scala type system for secure LLM-generated
                                     code
           Alexander Sternfeld                                          Andrei Kucharavy
           Institute of Entrepreneurship & Management, HES-SO           Institute of Informatics, HES-SO
           Le Foyer, Techno-Pôle 1                                     Techno-Pôle 3
           Sierre, Switzerland                                          Sierre, Switzerland
           alexander.sternfeld@hevs.ch                                  andrei.kucharavy@hevs.ch

                                                 Ljiljana Dolamic
                                             Cyber-Defence Campus
                                        armasuisse, Science and Technology
                                                Thun, Switzerland
                                     ljiljana.dolamic@armasuisse.ch


                       Abstract                                real-world analyses have shown that LLMs can in-
     Large language models (LLMs) have shown re-               troduce subtle yet serious vulnerabilities (Pearce
     markable proficiency in code generation tasks             et al., 2025).
     across various programming languages. How-                   This issue becomes particularly acute in the do-
     ever, their outputs often contain subtle but              main of mission-critical systems—software sys-
     critical vulnerabilities, posing significant risks
                                                               tems whose failure can lead to catastrophic out-
     when deployed in security-sensitive or mission-
     critical systems. This paper introduces Type-
                                                               comes, including physical harm, financial loss, ma-
     Pilot, an agentic AI framework designed to                jor operational disruptions, or loss of life (Gabriel
     enhance the security and robustness of LLM-               et al., 2022). Such systems are often implemented
     generated code by leveraging strongly typed               in strongly typed, safety-oriented programming
     and verifiable languages, using Scala as a rep-           languages like Coq, Scala, or more recently Rust,
     resentative example. We evaluate the effective-           where the type system is a central mechanism for
     ness of our approach in two settings: formal              enforcing correctness and preventing classes of
     verification with the Stainless framework and
                                                               bugs at run time. Despite these safeguards, vulnera-
     general-purpose secure code generation. Our
     experiments with leading open-source LLMs                 bilities still surface, often due to logical oversights,
     reveal that while direct code generation of-              incorrect assumptions, or abstraction mismatches
     ten fails to enforce safety constraints, just as          at boundaries. A well-known example is the 1999
     naive prompting for more secure code, our type-           NASA Mars Climate Orbiter failure, where one
     focused agentic pipeline substantially mitigates          subsystem produced output in imperial units while
     input validation and injection vulnerabilities.           another expected metric, leading to the spacecraft’s
     The results demonstrate the potential of struc-
                                                               loss due to an undetected discrepancy at the in-
     tured, type-guided LLM workflows to improve
     the SotA of the trustworthiness of automated
                                                               terface between components (Harish, 2025). A
     code generation in high-assurance domains.                notable recent example of such a vulnerability in
                                                               action occurred in January 2023, when a critical
1    Introduction                                              FAA system failure, later traced to a corrupted con-
In recent years, large language models (LLMs)                  figuration file, led to the temporary grounding of
have become powerful tools for assisting in soft-              all flights across the United States (reuters, 2023).
ware development, from generating boilerplate                     While LLMs are increasingly capable of detect-
code to proposing non-trivial algorithmic imple-               ing potential code vulnerabilities, they often fall
mentations (Wang and Chen, 2023; Chen et al.,                  short in generating robust corrections (Kulsum
2021). Their fluency in natural and programming                et al., 2024; Pearce et al., 2022). Our work ad-
languages allows developers to interact with them              dresses this gap. By focusing on Scala - a widely
without disrupting their workflow, accelerating the            used language with extensive codebase on GitHub
development lifecycle. However, as LLMs are                    and documentation on StackOverflow (O’Grady,
increasingly used to write production code, con-               2025), we propose TypePilot, an agentic AI ap-
cerns have emerged about the reliability and secu-             proach that not only leverages the detection capa-
rity of the generated output. Multiple studies and             bilities of LLMs but actively guides them to ex-

                                                          95
               Proceedings of the First Interdisciplinary Workshop on OMMM associated with RANLP 2025,
                                      pages 95–103, Varna, Bulgaria, Sep 8-10, 2025.
                                     https://doi.org/10.26615/978-954-452-101-1-011
ploit the expressiveness of the Scala type system to         3     Methodology
add safety guarantees. By structuring interactions,
TypePilot guides LLMs to generate and refine code            We will now describe the methodology that is used
that adheres to strict safety and correctness proper-        in this research. First, the models that are used
ties.                                                        in this research are specified. Then, we consider
                                                             the ability of LLMs to generate code using the
   This paper is structured as follows: Section 2            formal verification framework Stainless. Last, we
describes the related literature, after which Sec-           consider the general case of type-system rooted
tion 3 outlines the methodology. Next, the results           vulnerabilities.
are presented in Section 4. Last, Section 6 con-
cludes the paper and provides directions for future          3.1    Model usage
research. The code and results related to this paper
                                                             Throughout this research, we use open-source
are publicly available in this Github Repository.
                                                             models, with a focus on specialized coding
                                                             models. Specifically, we used the coding models
2     Related work                                           Qwen/Qwen2.5-Coder-32B-Instruct,
                                                             deepseek-ai/deepseek-coder-33b-
                                                             instruct and codellama/CodeLlama-
2.1    LLMs for code generation                              70b-Instruct-hf.             Additionally, we
                                                             used the regular conversational models
The use of large language models for code genera-
                                                             meta-llama/Meta-Llama-3-70B,
tion has grown rapidly, with coding specific mod-
                                                             deepseek-ai/DeepSeek-R1-Distill-
els demonstrating impressive capabilities across a
                                                             Llama-70B and Qwen/Qwen3-32B.
wide range of programming languages and tasks.
However, several studies have pointed out that               3.2    Stainless
these models often produce code that is syntac-
                                                             We first aim to leverage the formal verification
tically correct but semantically flawed or inse-
                                                             framework Stainless (Lab for Automated Reason-
cure. For instance, Pearce et al. (2025) shows
                                                             ing and Analysis, 2025) to improve the robustness
that GitHub Copilot produces vulnerabilities in ap-
                                                             of LLM-generated code. Formal verification refers
proximately 40% of test cases based on the top 25
                                                             to the use of mathematical methods to prove that
Common Weakness Enumeration list from MITRE.
                                                             a program satisfies certain correctness properties.
Similarly, Khoury et al. (2023) show that Chat-
                                                             Stainless is one of the most widely used verifica-
GPT generates vulnerable code in 16 out of 21 test
                                                             tion frameworks in Scala, with extensive documen-
cases, using a variety of programming languages
                                                             tation. Stainless verifies whether Scala code meets
targeting a diverse set of vulnerabilities.
                                                             user-specified safety properties by attempting to
   There have been attempts to use separate LLMs             construct proofs over the code. To enable this, the
in combination with sophisticated prompting strate-          code must explicitly state what is to be proven, and
gies to patch such vulnerabilities. However, these           provide the necessary logical structure for the proof,
approaches remain brittle, with models often mis-            using a subset of Scala tailored for verification.
understanding the root cause or proposing fixes that            To this end, we use both zero-shot and two-shot
break functionality. Kulsum et al. (2024) show               prompting to have a LLM both generate the code
that LLMs have difficulty in patching vulnerabili-           and the conditions. Figure 2 displays the prompt
ties that are either complex or linked to the project        that is used in the two-shot prompting setting. The
design. Similarly, Pearce et al. (2022) show that            two examples that are given to the LLM are Stain-
LLMs are not yet able to autonomously patch code             less code for finding the maximum between two
vulnerabilities in real-world scenarios.                     values and for returning the size of a list. The exact
    Our work builds upon these findings by explor-           examples can be found in the Github Repository.
ing a different method for mitigating vulnerabilities           As displayed in Table 1, we use three simple
- leverage the properties of strongly typed coding           tasks for evaluating the LLMs in the context of
languages. We use agentic AI, where LLMs coop-               formal proofs: calculating Fibonacci number n,
eratively operate as autonomous agents, which has            calculating the factorial of an input and assessing
been shown to result in better generations (Kumar            whether list a is a sublist of list b. The main vulner-
et al., 2025; Wang et al., 2025).                            ability that the generated conditions should prevent

                                                        96
Figure 1: The full pipeline for the generation of code using TypePilot. After the initial generation of the code, the
vulnerabilities are detected by a separate instance of the LLM. Then, a final LLM is prompted to leverage the Scala
type system to improve the initial code, given the detected vulnerabilities.


are input variables that are invalid, such as a nega-                     Code generation in robust setting
tive input for a factorial function. Additionally, the
functions should also be robust to inputs that are                        You are a scala code generator. You will be given
                                                                          a task description and you will generate the code
too large and may cause an overflow error.                                for it. The code should start with “‘scala and end
                                                                          with “‘. Pay attention to the safety and robustness
      Generation of stainless code                                        of the code, and leverage the Scala type system - for
                                                                          example ADTs, refined types, traits, sealed traits -
                                                                          where needed to make the code safer. The task is:
      <question> Use the stainless framework to write
                                                                          user input
      verifiable scala code for fewshot example 1 </ques-
      tion>

      <answer> fewshot answer 1 </answer>
                                                                       Figure 3: Prompt used to generate the code in the robust
      <question> Use the stainless framework to write                  prompting setting.
      verifiable scala code for fewshot example 2 </ques-
      tion>

      <answer> fewshot answer 2 </answer>
                                                                       attacks. In particular, we examine HTML, Bash,
                                                                       and URL injections—common security risks in
      <question> Use the stainless framework to write                  back-end web development, especially when han-
      verifiable scala code for function description </ques-           dling user inputs through web forms. The specific
      tion>
                                                                       test cases are shown in Table 1. To assess the per-
                                                                       formance of LLMs on these tasks, we consider the
                                                                       following settings:
Figure 2: Prompt used to generate the Stainless code.
                                                                          • Baseline: directly prompting a LLM to gen-
                                                                            erate the code
3.3     General case: type-system rooted
        vulnerabilities                                                   • Robust prompting: directly prompting a
As Stainless targets a niche subset of Scala appli-                         LLM to generate the code, while emphasizing
cations, we also consider a more general setting.                           that the LLM should leverage the Scala type
Specifically, we focus on two vulnerability cate-                           system to make the code robust to potential
gories: insufficient input constraints and injection                        vulnerabilities.

                Stainless                                      General case: type-system rooted vulnerabilities
                                                        Input constraints                             Code injection
Calculating a fibonacci number               Calculating a fibonacci number               Greeting a user with HTML
Calculating the factorial of a number        Calculating the factorial of a number        Making a list of comments with HTML
Asserting if list a is a sublist of list b   Calculating a matrix multiplication          Searching a file using bash
                                             Calculating a matrix convolution             Pinging a host using bash
                                                                                          Creating a redirect URL with HTML

Table 1: The test cases used to evaluate the LLMs in each of the settings. The most left column shows the test cases
used to evaluate the performance of LLMs in generating code using the Stainless framework. The second and third
column show the test cases for the general case looking at type-system rooted vulnerabilities.

                                                                  97
    Code generation using TypePilot                                          After prompting a first LLM to generate the
                                                                             initial code, we ask a second LLM to detect
    Initial code generation                                                  the vulnerabilities in this code. We then ask
    You are a Scala code generator. You will be given a
    task description and you will generate the code for it.                  a third instance of the LLM to improve the
    The code should start with “‘scala and end with “‘.                      initial code using the Scala type system, to
    The task is: user input                                                  make it robust to the detected vulnerabilities.
    Vulnerability detection                                               The prompt that is used in the robust generation
    You will be given a task description and generated                 setting can be found in Figure 3. Similarly, Figure
    code. Your task is to find potential vulnerabilities in
    the code that could lead to security issues or unex-               4 shows the prompts that are used with TypePilot.
    pected behavior. Solely describe the vulnerabilities,              In the baseline setting, we use the same prompt that
    do not give me any code. Here is the task: user input              is used for the initial code generation in TypePilot.
    Here is the previous code: initial output
                                                                       For each of the models described in Section 3.1 we
    Final code generation                                              run each of the settings.
    You are a Scala code generator. You will be given a
    task description, generated code, and vulnerabilities              3.4   Comparison to existing work
    that should be addressed. Your task is to improve the
    code by using the Scala type system - for example                  Research on secure code generation using large
    ADTs, refined types, traits, sealed traits - to address            language models (LLMs) remains limited, despite
    the vulnerabilities. The code should start with “‘scala
    and end with “‘. Here is the task: user input. Here                growing concerns about vulnerabilities in automati-
    is the previous code: initial output Here are the                  cally generated code. A recent survey by Dai et al.
    vulnerabilities: vulnerabilities                                   (2025) highlights that most current approaches rely
                                                                       heavily on training data or static analysis tools, re-
                                                                       stricting their generalizability. Methods such as
Figure 4: Prompts used to generate the initial code, the               SafeCoder (He et al., 2024) and SVEN (He and
vulnerabilities and the final code in TypePilot. The final             Vechev, 2023) fine-tune LLMs with curated secure
prompt guides the LLM to use the Scala type system to                  code datasets, and are thus inherently dependent
make the code more robust.                                             on the availability and quality of specialized train-
                                                                       ing corpora. Moreover, the fine-tuned LLMs do
                                                                       not generalize well to unseen vulnerabilities or pro-
   • TypePilot: use the agentic AI framework as                        gramming languages. Similarly, PromSec (Naz-
     displayed in Figure 1 to generate the code.                       zal et al., 2024) optimizes prompts through static

                                         Qwen-2.5-Coder (32B)                CodeLlama (70B)          Deepseek-coder (33B)
                                      Baseline Robust TypePilot        Baseline Robust TypePilot   Baseline Robust TypePilot
 Average age
 - Correct for regular input            ✓        ✓        ✓              ✓        ✓        ✓         ✓        ✓        ✓
 - Handle empty lists                   ✓        ✓        ✓              ✓        ✓        ✓         ✓        ✓        ✓
 - Handle negative ages                 ✗        ✗        ✓              ✗        ✗        ✓         ✗        ✗        ✗

 Fibonacci number N
 - Correct for regular input            ✓        ✓        ✓              ✓        ✓        ✓         ✓        ✓        ✓
 - Check for negative N                 ✗        ✓        ✓              ✗        ✗        ✗         ✗        ✗        ✓
 - Handles large values of N            ✗        ✓        ✓              ✗        ✗        ✗         ✗        ✓        ✓

 Matrix multiplication
 - Correct for regular input            ✓        ✓        ✓              ✓        ✓        ✓         ✓        ✓        ✓
 - Check for empty matrices             ✓        ✗        ✓              ✗        ✗        ✗         ✗        ✗        ✗
 - Check for dimension matching         ✓        ✓        ✓              ✓        ✗        ✓         ✗        ✓        ✓

 Matrix convolution
 - Correct for square matrix input      ✓        ✓        ✓              ✗        ✗        ✗         ✓        ✓        ✓
 - Correct for regular matrix input     ✓        ✓        ✓              ✗        ✗        ✗         ✓        ✓        ✓
 - Handles rectangular kernels          ✗        ✗        ✓              ✗        ✗        ✓         ✗        ✗        ✗
 - Checks for empty kernel              ✗        ✓        ✓              ✗        ✗        ✓         ✗        ✗        ✓
 - Checks for empty matrix              ✗        ✓        ✓              ✗        ✗        ✓         ✗        ✗        ✓
 - Handles even sized kernels           ✗        ✗        ✓              ✗        ✗        ✗         ✗        ✗        ✗

Table 2: Manual evaluation of the generated code regarding input constraints. For each case, ✓ indicates that the
code is robust to the vulnerability, whereas ✗ indicates that the code is not robust to the vulnerability.

                                                                  98
                                  Qwen-2.5-Coder (32B)            CodeLlama (70B)             Deepseek-coder (33B)
                               Baseline Robust TypePilot    Baseline Robust TypePilot      Baseline Robust TypePilot

 HTML greeting
 Correctness and compilation     ✓        ✓        ✓            ✓        ✓        ✓          ✓        ✓        ✗
 Robust to injection             ✗        ∼        ✓            ✗        ✓        ✓          ✗        ✓        ✓

 HTML comments
 Correctness and compilation     ✓        ∼        ✓            ✓        ✗        ∼          ✓        ✓        ✓
 Robust to injection             ✗        ✓        ✓            ✗        ✗        ✓          ✗        ∼        ✓

 Bash file search
 Correctness and compilation     ✓        ✓        ✓            ✓        ✓        ✓          ✓        ✓        ✓
 Robust to injection             ✗        ✗        ✓            ✗        ✗        ✓          ✗        ✗        ✓

 Bash host ping
 Correctness and compilation     ✓        ✓        ✓            ✓        ✗        ✓          ✓        ✓        ✓
 Robust to injection             ✓        ✓        ✓            ✗        ✗        ✓          ✗        ✓        ✓

 URL redirect
 Correctness and compilation     ✓        ✓        ✓            ✓        ✓        ✓          ✓        ✓        ✓
 Robust to injection             ✗        ∼        ∼            ✗        ✓        ✓          ✗        ✗        ✓

Table 3: Manual evaluation of the generated code regarding code injection. For each case, ✓ indicates that the code
is robust to the vulnerability, whereas ✗ indicates that the code is not robust to the vulnerability.


analyzers, but also relies on labeled data and an               cepts that are present in Scala but not available
external code-specific vulnerability scanner.                   in Stainless. As Stainless is a verification frame-
   In contrast, our approach does not rely on task-             work targeting a restricted subset of Scala, many
specific training data or external static analyz-               features of full Scala—such as certain standard li-
ers. Instead, it leverages the expressive power                 brary functions—are unavailable. To illustrate, in
of strongly typed languages to enforce security                 the generated code from Qwen/Qwen3-32B for
constraints directly in the generated code. Be-                 the verification of a sublist relation, the function
cause most existing methods depend on curated                   List.sliding is used. However, the sliding
datasets or vulnerability scanners (as discussed                operation is not defined for Stainless List objects.
above), there are few established baselines tailored            Similarly, in a generated code snippet the opera-
to strongly typed languages like Scala or Rust.                 tion println was used, which is not available in
Given this gap, it is most appropriate to compare               Stainless. Second, the generated code often con-
our method against prompting-based baselines in                 tains syntax errors. Whereas syntax errors could
addition to the base model. Following Vero et al.               be resolved relatively easily by users, the usage
(2025), we include a baseline where the model is                of Scala components in Stainless is not trivially
given a general security reminder, which we call                repaired. We hypothesize that the lack of perfor-
robust prompting. We also evaluate against Self-                mance is caused by a lack of training data related
Planning, a coding-specific prompting strategy in-              to Stainless, given that it is a niche framework.
troduced by Jiang et al. (2024). Self-Planning is a             This observation is consistent with findings from
two-stage prompting framework in which the LLM                  other domains, for example, Fan et al. (2025) found
first generates a high-level plan for the coding task,          that LLMs struggle to generate verifiable specifi-
after which it implements the plan in code.                     cations using the VeriFast verification framework
                                                                for C, despite preserving functional behavior. In
4     Results                                                   appendix B, we provide a notable instance in which
                                                                the generation avoids formal verification by using
4.1    Stainless                                                @library annotations.
In general, we see that none of the models is ca-
pable of consistently generating Stainless code                 4.2   General setting
that correctly compiles. Upon manual inspection,                Given that LLMs are not able to write compilable
we found two main failure modes across all mod-                 Stainless code, we shift our attention to a more gen-
els. First, each of the LLMs regularly uses con-                eral Scala setting, as described in Section 3.3. We

                                                           99
consider two types of vulnerabilities: insufficient           vulnerable to injection, ✓ indicates that code is ro-
input constraints and code injection. The generated           bust to injection, and ∼ indicates that the code is
code is available in the anonymized repository.               partially robust to injection. The results show that
                                                              in the baseline setting virtually all generated code
4.2.1   Input constraints                                     is vulnerable to code injection. Robust prompt-
Table 2 shows the results for each of the test cases          ing improves the performance, resulting in fewer
for each of the models. For each of the models, ✗             vulnerabilities. As before, TypePilot achieves the
indicates that the resulting code was not robust to           best performance, with robust code generations in
the indicated vulnerability. The results show that            almost all settings.
in the baseline setting, the models are capable of
generating functions that provide the correct out-            4.2.3 Usage of the Scala type system
put in a normal setting. However, the models are              In the new framework, the Scala type system is
not capable of handling edge cases correctly. To              used as a central tool to guide the generation of
illustrate, none of the models can correctly handle           secure code. By prompting LLMs to leverage fea-
negative ages or a negative input to a Fibonacci              tures such as sealed traits, smart constructors, and
function. We see that in the robust setting, models           refined return types, we enable the generation of
perform slightly better, and tend to be robust to             programs that encode correctness directly into their
some of the vulnerabilities. However, for none of             type signatures. This stands in contrast to baseline
the models the code is fully robust. With TypePilot,          generations, which operate on unconstrained prim-
we obtain the best performance, with models gen-              itives and rely on ad hoc runtime logic to handle
erally being robust to most vulnerabilities related           edge cases and errors.
to input constraints.                                            Figures 5 shows an examples of code generated
   When comparing the models, we observe that                 in the baseline and in the agentic AI framework, for
Qwen-2.5-Coder (32B) performs the best,                       the same test case and model. Figure 5 shows that
passing all our checks when using TypePilot. In               in the baseline version, the averageAge function
contrast, CodeLlama (70B) does not perform                    takes a List[Int] and performs a division after
well, remaining vulnerable to a number of cases in            checking for emptiness. While this implementa-
each of the settings, highlighting the importance of          tion is syntactically valid, it permits semantically
study of specific code-generating LLM models.                 invalid inputs—such as negative ages or values far
                                                              outside a realistic human range—and silently de-
4.2.2   Code injection                                        faults to returning 0.0 when the input list is empty.
The second type of vulnerability we consider is               In contrast, the enhanced version defines a sealed
code injection. Table 3 displays the results for each         trait Age and a case class ValidAge, with a smart
of the models, where ✗ indicates that the code is             constructor in the Age companion object that en-


                (a) Baseline                                                  (b) TypePilot
object GeneratedFunctions {                       object GeneratedFunctions {
    def averageAge(ages: List[Int]): Double = {     sealed trait Age {
        if (ages.isEmpty) 0.0                         def value: Int
        else ages.sum.toDouble / ages.length        }
    }
}                                                     final case class ValidAge(value: Int) extends Age

                                                      object Age {
                                                        def apply(value: Int): Option[Age] = {
                                                          if (value >= 0 && value <= 120) Some(ValidAge(value))
                                                          else None
                                                        }
                                                      }

                                                      def averageAge(ages: List[Age]): Option[Double] = {
                                                        if (ages.isEmpty) None
                                                        else {
                                                            val (sum, count) = ages.foldLeft((0L, 0)) {
                                                            case ((accSum, accCount), age) =>
                                                            (accSum + age.value, accCount + 1)
                                                        }
                                                      }
                                                  }

Figure 5: Comparison of baseline and TypePilot average age function generations from Qwen-2.5-Coder
(32B)

                                                        100
forces domain-specific constraints: only values be-      (HTML injection, bash injection and path traver-
tween 0 and 120 are permitted. The averageAge            sal). For each method, we calculated the fraction
function now accepts a list of validated Age values      of secure outputs and averaged the results across
and returns an Option[Double], making both               the three LLMs, which is displayed in Figure 6.
the domain invariants and the possibility of unde-          For input constraints, robust prompting offered
fined results (e.g., empty lists) explicit at the type   limited improvements over the baseline, particu-
level. This design ensures that all inputs have been     larly for shape violations and null dereferences. It
prevalidated before the function executes, reducing      often inserted assertions but did not systematically
the likelihood of subtle logic bugs and enabling         enforce data structure correctness. TypePilot re-
safer composition in larger systems. A second ex-        duced these errors more effectively, as the presence
ample related to generating a function to search for     of type specifications led the models to generate
files using bash is discussed in appendix C.             code structured around expected data formats rather
   In TypePilot, the Scala type system is used not       than relying on runtime checks.
merely to enforce syntactic correctness but to en-          For code injection, TypePilot also lowered vul-
code domain abstractions rules, constrain behav-         nerability rates, especially for bash injections
ior, and make failure modes explicit. By doing           where robust prompting typically altered command
so, it transforms what would otherwise be runtime        structure without validating input. Results var-
checks and ad hoc validations into statically en-        ied between models: Qwen-2.5-Coder (32B) and
forced contracts. This shift leads to code that is       Deepseek-Coder (33B) generally applied the type
more robust, more predictable, and better aligned        system consistently, while CodeLlama (70B) some-
with the principles of secure and maintainable soft-     times attempted to handle vulnerabilities outside
ware design. In the context of LLM-generated code,       the type framework. In some cases, type constraints
these benefits are particularly important, as they       were only partially used, such as defining a type
offer a principled way to guard against common           for an output value but not for the input values.
pitfalls and encourage safer defaults during genera-        Appendix D analyzes attention weights across
tion.                                                    the three methods, showing that TypePilot places
                                                         greater emphasis on key safety terms during code
4.3   Vulnerability Analysis                             generation than robust prompting.
We performed a post-hoc vulnerability analysis by
                                                           4.4   Comparison to Self-Planning Code
categorizing the vulnerabilities observed in each
                                                                 Generation
test case. These categories include input con-
straint issues (shape violations, null dereferences      As an additional validation, we compared Type-
and boundary violations) and code injection risks        Pilot to the Self-Planning prompting framework,




Figure 6: Fraction of secure code generations across vulnerability categories for each of the methods (baseline
prompting, robust prompting, TypePilot). Results are averaged over all evaluated LLMs. Lower bars indicate a
higher frequency of vulnerabilities; higher bars indicate safer generations.

                                                     101
                                                             One promising direction is the development of
                                                          a hybrid, object-aware prompting system. In this
                                                          approach, metadata about each relevant object, in-
                                                          cluding its types and invariants, is provided to the
                                                          LLM prior to generation. This structured context
                                                          could enable the model to reason more accurately
                                                          about type interactions and enforce security con-
                                                          straints across function boundaries. Additionally,
                                                          integrating lightweight symbolic reasoning or type
                                                          inference engines could help LLMs maintain global
Figure 7: Comparison of the secure code generation        consistency in larger projects, further reducing the
methods TypePilot (ours) and Self-Planning, as intro-     risk of injection attacks and logical errors.
duced by Jiang et al. (2024).
                                                          6   Conclusion
as discussed in Section 3.4. In the Self-Planning         In this work, we aim to improve the security of
framework, the model is first asked to outline a          LLM generated mission-critical code, focusing on
plan for solving the task. Afterwards, it is asked        the Scala strongly typed language. As Scala is
to write the code by executing the plan, and it is        routinely used in mission-critical software and en-
explicitly instructed to consider safety and security     gineers are increasingly often using LLMs to code,
aspects before writing code. Overall, TypePilot out-      it is essential to ensure that the generated code is
performs self-planning for both the input constraint      free of vulnerabilities. We first show that LLMs
and code injection tasks. The difference is largest       are not able to autonomously use the static veri-
for Qwen-2.5-Coder (32B), which more reliably ad-         fication tool Stainless. Therefore, we develop a
heres to the type system instructions in TypePilot,       more general agentic AI framework that structures
resulting in fewer shape and null-handling issues         multi-step interactions between LLMs for code gen-
compared to the Self-Planning setup.                      eration. By leveraging the Scala type system, we
   Manual inspection of the Self-Planning outputs         significantly improve the quality and safety of gen-
reveals that, despite explicit prompts to account for     erated code. Crucially, this approach transforms
vulnerabilities during the planning and implemen-         type systems from passive compile-time enforcers
tation stages, models frequently overlook or under-       into active agents of code safety. We study two dif-
address these concerns. The generated plans may           ferent classes of vulnerabilities, input constraints
mention security considerations in abstract terms         and code injection, and show that in both cases our
but rarely translate them into concrete, protective       framework improves code safety over a baseline
measures in the final code. These findings suggest        and zero-shot robust prompting setting. We use
that simply instructing the model to “think about         the rigidity of the Scala type system to compensate
safety” is insufficient: introducing a structured in-     for the inconsistencies picked up from the training
termediate step, such as TypePilot’s type-enforced        code by LLMs, which in turn allow an easier inter-
specification phase, is more effective in steering        face to access the power of the Scala type system.
the model toward safer code generation.
                                                              We conclude by suggesting two directions for
5   Scaling                                               future research. First, future work should test the
                                                          framework’s capabilities in more complex code-
The primary goal of this work is to show that lever-      bases. While this study provided a proof of concept
aging the type system in strongly typed languages         using simple test cases, real-world software tends
can substantially mitigate vulnerabilities in LLM-        to be more complex, so validating our approach in
generated code. While our experiments focus on            these environments is important to assess its effec-
relatively simple test cases, practical applications      tiveness. Second, deploying the framework in an
often involve larger, interconnected codebases with       active development setting would allow engineers
complex object hierarchies. Scaling our framework         to use it in their daily work and provide valuable
to such scenarios presents new challenges, primar-        feedback. This real-world input can guide further
ily related to context management and dependency          improvements and help tailor the framework to bet-
reasoning across multiple files and modules.              ter meet the needs of software teams.

                                                    102
References                                                    Mayank Kumar, Jiaqi Xue, Mengxin Zheng, and Qian
                                                               Lou. 2025. Tfhe-coder: Evaluating llm-agentic fully
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming                    homomorphic encryption code generation.
 Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-
 plan, Harri Edwards, Yuri Burda, Nicholas Joseph,            Lab for Automated Reasoning and Analysis. 2025.
 Greg Brockman, Alex Ray, Raul Puri, Gretchen                   Stainless: A verification framework for scala
 Krueger, Michael Petrov, Heidy Khlaaf, Girish Sas-             programs.   https://epfl-lara.github.io/
 try, Pamela Mishkin, Brooke Chan, Scott Gray,                  stainless/index.html.
 Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz
 Kaiser, Mohammad Bavarian, Clemens Winter,                   Mahmoud Nazzal, Issa Khalil, Abdallah Khreishah, and
 Philippe Tillet, Felipe Petroski Such, Dave Cum-               NhatHai Phan. 2024. Promsec: Prompt optimization
 mings, Matthias Plappert, Fotios Chantzis, Eliza-              for secure generation of functional source code with
 beth Barnes, Ariel Herbert-Voss, William Hebgen                large language models (llms). In Proceedings of the
 Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie             2024 on ACM SIGSAC Conference on Computer and
 Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,          Communications Security, CCS ’24, page 2266–2280.
 William Saunders, Christopher Hesse, Andrew N.                ACM.
 Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan
 Morikawa, Alec Radford, Matthew Knight, Miles                Stephen O’Grady. 2025. The redmonk programming
 Brundage, Mira Murati, Katie Mayer, Peter Welinder,             language rankings: January 2025. Accessed: July 8,
 Bob McGrew, Dario Amodei, Sam McCandlish, Ilya                  2025.
 Sutskever, and Wojciech Zaremba. 2021. Evaluating
 large language models trained on code.                       Hammond Pearce, Baleegh Ahmad, Benjamin Tan,
                                                                Brendan Dolan-Gavitt, and Ramesh Karri. 2025.
Shih-Chieh Dai, Jun Xu, and Guanhong Tao. 2025. A               Asleep at the keyboard? assessing the security of
  comprehensive study of llm secure code generation.            github copilot’s code contributions. Commun. ACM,
                                                                68(2):96–105.
Wen Fan, Marilyn Rego, Xin Hu, Sanya Dod, Zhaorui
 Ni, Danning Xie, Jenna DiVincenzo, and Lin Tan.              Hammond Pearce, Benjamin Tan, Baleegh Ahmad,
 2025. Evaluating the ability of large language models          Ramesh Karri, and Brendan Dolan-Gavitt. 2022. Ex-
 to generate verifiable specifications in verifast.             amining zero-shot vulnerability repair with large lan-
                                                                guage models.
Ellie Gabriel, Xenophon Papademetris, Ayesha N.
   Quraishi, and Gregory P. Licholai. 2022. Therac-           reuters. 2023. Explainer: Why u.s. flights were
   25: Software that Killed, page 263–267. Cambridge             grounded by a faa system outage. Accessed: July 8,
   University Press.                                             2025.
Ajay Harish. 2025. When nasa lost a spacecraft due to         Mark Vero, Niels Mündler, Victor Chibotaru, Veselin
  a metric math mistake. Accessed: July 8, 2025.               Raychev, Maximilian Baader, Nikola Jovanović,
Jingxuan He and Martin Vechev. 2023. Large language            Jingxuan He, and Martin Vechev. 2025. Baxbench:
   models for code: Security hardening and adversarial         Can llms generate correct and secure backends?
   testing. In Proceedings of the 2023 ACM SIGSAC
                                                              Haoran Wang, Zhenyu Hou, Yao Wei, Jie Tang, and
   Conference on Computer and Communications Secu-
                                                                Yuxiao Dong. 2025. Swe-dev: Building software en-
   rity, CCS ’23, page 1865–1879. ACM.
                                                                gineering agents with training and inference scaling.
Jingxuan He, Mark Vero, Gabriela Krasnopolska, and
   Martin Vechev. 2024. Instruction tuning for secure         Jianxun Wang and Yixiang Chen. 2023. A review on
   code generation.                                              code generation with llms: Application and evalu-
                                                                 ation. In 2023 IEEE International Conference on
Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang,                Medical Artificial Intelligence (MedAI), pages 284–
  Qiwei Shang, Ge Li, Zhi Jin, and Wenpin Jiao. 2024.            289.
  Self-planning code generation with large language
  models. ACM Trans. Softw. Eng. Methodol., 33(7).
Raphaël Khoury, Anderson R. Avila, Jacob Brunelle,
  and Baba Mamadou Camara. 2023. How secure is
  code generated by chatgpt? In 2023 IEEE Interna-
  tional Conference on Systems, Man, and Cybernetics
  (SMC), pages 2445–2451.
Ummay Kulsum, Haotian Zhu, Bowen Xu, and Marcelo
  d’Amorim. 2024. A case study of llm for automated
 vulnerability repair: Assessing impact of reasoning
  and patch validation feedback. In Proceedings of the
 1st ACM International Conference on AI-Powered
 Software, AIware 2024, page 103–111, New York,
  NY, USA. Association for Computing Machinery.

                                                        103
