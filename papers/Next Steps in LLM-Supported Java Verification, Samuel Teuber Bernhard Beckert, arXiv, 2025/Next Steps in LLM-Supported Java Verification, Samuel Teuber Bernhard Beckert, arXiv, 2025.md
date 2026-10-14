                                             Next Steps in LLM-Supported Java Verification
                                                                       Samuel Teuber                                           Bernhard Beckert
                                                             Karlsruhe Institute of Technology                         Karlsruhe Institute of Technology
                                                                   Karlsruhe, Germany                                        Karlsruhe, Germany
                                                                     teuber@kit.edu                                            beckert@kit.edu




                                           Abstract—Recent work has shown that Large Language Mod-                Unfortunately, we are still far from reaching the golden age.
                                        els (LLMs) are not only a suitable tool for code generation but        One reason for this is a lack of techniques to reliably elicit an-
                                        also capable of generating annotation-based code specifications.       notations from an LLM. As the number of required annotations
                                        Scaling these methodologies may allow us to deduce provable
                                                                                                               grows with the size of the analyzed software system, a lack
arXiv:2502.01573v1 [cs.SE] 3 Feb 2025




                                        correctness guarantees for large-scale software systems. In com-
                                        parison to other LLM tasks, the application field of deductive         of reliability quickly hinders our ability to scale the approach.
                                        verification has the notable advantage of providing a rigorous              Contribution: In this work, we present early results
                                        toolset to check LLM-generated solutions. This short paper             on exploring different prompting paradigms for the reliable
                                        provides early results on how this rigorous toolset can be used to     generation of JML contracts via LLMs. In particular, we
                                        reliably elicit correct specification annotations from an unreliable
                                        LLM oracle.                                                            analyze to what degree feedback from the verifier is currently
                                           Index Terms—Large Language Models, Program Verification,            helping the specification generation. Finally, we discuss the
                                        Formal Specification, Java, JML                                        necessary next steps to scale our approach to larger-scale
                                                                                                               systems. The detailed prompts used for our experiments can
                                                               I. I NTRODUCTION
                                                                                                               be found in Appendix A.
                                           Along with the pervasive success of Large Language
                                        Models [4] (LLMs) across many application domains, a                    II. LLM S FOR AUXILIARY S PECIFICATION G ENERATION
                                        steadily growing body of research is exploring the usage of               This work considers the specification of Java programs
                                        LLMs for the synthesis of specification annotations based              using the Java Modelling Language (JML) [2]. JML allows
                                        on a program’s source code [3, 5, 7, 9, 11, 12, 14, 16, 17,            the contract-based specification of Java methods and classes
                                        18]. The appeal of using LLMs in this context comes from               via JavaDoc-like comments and is a supported specification
                                        the “NP-like” imbalance in the problem formulation: While              language of multiple Java verifiers [1, 2, 6]. In this work,
                                        it is, in general, arbitrarily difficult to generate a correct,        we made use of the KeY tool [1], which deductively verifies
                                        useful specification for a given piece of code, auto-active            that a Java program adheres to a given contract-based JML
                                        verifiers [13], in principle, allow us to verify the correctness       specification. KeY comes with a built-in proof search strategy
                                        of a given specification. The combination of LLM-based                 that allows automated verification and supports modular veri-
                                        specification synthesis and deductive specification verification       fication: Using the abstractions provided by method contracts,
                                        has now been validated in multiple case studies and has even           specifications of larger software systems can be decomposed
                                        been applied for real-world programming languages such as              into verification tasks for individual methods.
                                        Java and JML [10] using the verification tool KeY [1] (see [3]).             LLM-based synthesis of JML annotations: In prior
                                           In this light, LLM-based specification generation, as a             work [3], we proposed an architecture for combining
                                        canonical example of Intersymbolic AI [15], has the potential          (deductive) verification tools such as KeY [1] with LLM-
                                        to usher in a “golden age” of deductive verification in which          based specification generation and evaluated our approach on
                                        the average software engineer can finally apply rigorous pro-          a set of Java programs. In our approach, outlined in Figure 1,
                                        gram analysis techniques to their large-scale software systems         a partially annotated Java Program (1) is handed to an LLM
                                        and prove system correctness on their own. Generating a                with instructions to complete the annotation. Subsequently,
                                        method’s top-level specification still requires human interven-        the annotations generated by the LLM are added to the
                                        tion to ensure the specification matches the requirements, but         program code, and the Annotation Draft (2) is handed to
                                        it has the potential to ease the workload to achieve provable          a verification tool, e.g. the Java verification tool KeY. If
                                        correctness. This work focuses on the other promising applica-         KeY successfully verifies the correctness of the Annotation
                                        tion field, namely auxiliary specification generation. Here, the       Draft, we return the annotated file (3). If verification fails,
                                        top-level specification is still provided by a human and the           we obtain a description of the error (4) from the verifier and
                                        LLM works under the supervision of an automated verifier               now require a strategy to recover from this error – we will
                                        which checks whether the LLM’s annotations are sufficient to           further discuss this part of the approach below.
                                        prove the top-level specification.                                        Depending on the application context, the guarantees
                                           This work was supported by funding from the pilot program Core-     provided by our approach can vary: If the Java Program (1)
                                        Informatics of the Helmholtz Association (HGF).                        contains no prior annotations and the LLM extends the
                         Partially Annotated Java Program (1)                                                    Successful Instances (GPT-4O)
                                                                                                   0.8




                                                                                    Invariants
                                          LLM:
                                  Annotation Generation                                            0.6                          Feedback             Median
                                                                                                                                Sampling             Min/Max
                                             Annotation                                            0.4
                                                                                                         1   2   3    4     5    6       7      8      9       10
                  ?                          Draft (2)
                                                                                                   0.6




                                                                                    Subcontracts
      Error (4)
                                     Verifier (e.g. KeY)                                           0.4
                                                                                                   0.2
                                              Success
                                                                                                   0.0
                                     Annotated File (3)                                                  1   2   3    4     5     6      7      8      9       10
                                                                                                                             Steps
Fig. 1. Setup of our LLM integration for KeY: A partially JML-annotated
Java file is handed to an LLM that generates additional annotations for the         Fig. 2. Increase of Success Rate for invariant (top) resp. subcontract (bottom)
file. Subsequently, the file with extended annotation is handed to a verifier (in   synthesis using GPT 4O for increasing step rate: Shaded areas represent
this instance KeY) which attempts to verify the correctness of the code w.r.t.      minimal/maximal success rates over 5 runs, the solid line represents the
the given annotations. This work explores strategies to recover from errors         median.
when the verifier cannot prove the specification draft of the LLM.

                                                                                                                 III. E RROR R ECOVERY
program by a verifiable annotation for a top-level method,
                                                                                       In prior work [3], we used rudimentary error messages from
we do not have any guarantee beyond internal consistency
                                                                                    KeY to generate feedback for the LLM. Here, we can distin-
between the generated code and its specification. On the
                                                                                    guish two kinds of failures: syntactical errors in the generated
other hand, if the partially annotated Java Program contains
                                                                                    specification (e.g., missing semicolons, wrong use of variables,
a top-level specification and the LLM only complements
                                                                                    etc.) and semantical errors (e.g., a postcondition that is not
the annotation by auxiliary specifications such as loop
                                                                                    satisfied by the method’s implementation). For syntactical
invariants and/or method contracts for submethods, successful
                                                                                    errors, we provide the LLM with the parser’s error message;
verification guarantees that the (human-provided) top-level
                                                                                    for semantical errors, the LLM receives the (KeY-generated)
specification is satisfied by the implementation.
                                                                                    labels of open proof branches. These labels, describe which
   We believe the latter use case is particularly promising as
                                                                                    part of the proof failed, e.g., the part where KeY tried to
it only delegates work to the LLM that cannot compromise
                                                                                    prove that a loop invariant is initially valid (”Invariant Initially
soundness and is thus resistant to an LLM’s errors: If the gen-
                                                                                    Valid”) or that the post-condition holds when the value of an
erated annotations admit verification, we know that the user-
                                                                                    array is not null(”Normal Execution ( a != null)”).
given top-level specification is satisfied due to the rigorous
                                                                                       However, this raises the question of whether the provided
deduction inside KeY. Hence, we will focus on the generation
                                                                                    feedback is helpful for the LLM in correcting the specification.
of auxiliary annotations for a given top-level specification. To
                                                                                    As a simple baseline comparison, we can use a sampling-based
focus our study on the LLM’s capabilities, we consider the
                                                                                    approach: Instead of providing feedback to the LLM and con-
case where the Java+JML file has one gap in the specification
                                                                                    tinuing the same conversation string, we can restart the (prob-
that the LLM has to complete (e.g. one missing loop invariant).
                                                                                    abilistic) process from scratch whenever an LLM-generated
//@ ensures \result == -2*x;                                                        specification cannot be verified. To this end, we reran the ex-
int f(int x) { return g(-x); }                                                      periments from prior work for the synthesis of loop invariants
int g(int x) { return x+x; }                                                        and subcontracts with the current version of GPT 4O and com-
               Listing 1. Callee method g lacks an annotation
                                                                                    pared the previous feedback-based approach to a sampling-
                                                                                    based approach, which does not provide KeY’s feedback to the
      Example: Consider the example in Listing 1: In this                           LLM. As a benchmark set, we used 27 tasks for JML invariant
instance, we have a JML annotation for the method f. The                            synthesis and 14 tasks for the specification of called methods.
ensures clause defines a contract for f stating that its return                     The benchmarks cover a wide range of JML features including
value should be -2*x. To prove this contract in a modular                           array usage, quantifiers, assignable clauses, reference to pre-
way, we require an additional contract for method g, which                          execution values, etc. (see [3, Table 1]). For each instance, we
is called by method f. This contract could be provided by                           sampled (i.e., restarted the process) up to 10 times. Figure 2
an LLM: If the LLM manages to synthesize a contract for                             provides a first overview of these results: Here, we see how the
g such that KeY can prove the correctness of both methods                           rate of success increases with the number of feedback steps
(w.r.t. the contract in Listing 1 resp. the contract generated                      resp. sampled solutions for invariant and subcontract synthesis.
by an LLM), we know that the top-level specification of f                              On the one hand, the results show that an iterative process
is satisfied. This methodology of annotation-based automated                        with feedback increases the likelihood of success. This is a
verification is sometimes called auto-active verification [13].                     positive result because it means we are not in a situation
where GPT 4O either is capable of generating a solution or                                          Successful Instances (GPT-4O)
                                                                                  0.9
consistently fails across all attempts. On the other hand, these
                                                                                  0.7




                                                                   Invariants
results indicate that the current feedback provided by KeY does
not significantly improve GPT 4O’s ability to generate correct                    0.5                                    Feedback         Median
JML contracts: Because, even without any feedback, GPT 4O                         0.3                                    Sampling         Min/Max
achieves similar success rates and sometimes even outperforms                              2           4       6          8      10       12        14
the feedback-based approach. We suspect the latter result                         0.6




                                                                   Subcontracts
can be partially explained by the observation that GPT 4O
sometimes gets “stuck” on a wrong solution and only performs                      0.4
marginal changes to the previous, wrong solution instead of                       0.2
pivoting to a correct solution that would require more changes.                   0.0
      Token Efficiency: Another perspective on the two                                     2           4       6          8      10       12        14
competing approaches (sampling and feedback) is token                                                              Token Ratio
efficiency: LLM text generation is typically priced in tokens,
                                                                   Fig. 3. Increase of Success Rate for invariant (top) resp. subcontract (bottom)
which are the elementary components of a text that an LLM          synthesis using GPT 4O for increasing token ratio: Shaded areas represent
processes to perform its predictions. For this evaluation, it      minimal/maximal success rates over 5 runs, the solid line represents the
is important to note that different problem instances require      median.
different amounts of tokens: For example, assuming fixed
output length, generating a specification for a method with                                               TABLE I
                                                                                  R ESULTS FOR MIXED APPROACH : 50 INDEPENDENT SAMPLES VS .
100 lines of code will necessarily require more tokens than                              SAMPLING 5 ROUNDS WITH 10- STEP FEEDBACK .
generating code for a method with 10 lines of code (the token
                                                                                        Category               Strategy          Success Rate
count comprises both read input tokens and output tokens
                                                                                        Invariant Generation   Pure Sampling     23/27
written by the LLM). Hence, we divide the number of tokens                                                     Mixed             24/27
used to find a solution by the number of tokens in the initial                          Subcontracts           Pure Sampling     7/14
input query to the LLM and call this metric the token ratio.                                                   Mixed             8/14
The success rate w.r.t. token ratio is plotted in Figure 3.
   As a first observation, we note that sampling and
feedback-based approaches fundamentally differ in their            tion length. A logical step to scale our approach to even more
token efficiency: Feedback-based approaches input the entire       attempts is thus to mix the sampling-based approach with the
previous conversation back into the LLM for the generation of      feedback-based approach. To this end, we can use the data
the next answer. Thus, if we initially input I tokens, the LLM     gathered in our previous experiments to compare the success
generates O tokens on each turn and each feedback response         rate of 50 samples with the success rate of 5 samples each of
on our side comprises R tokens, then the first iteration costs     which has a 10-step feedback iteration. In both cases, up to
I + O tokens, the second iteration costs I + O + R + O             50 solutions are evaluated. The results of the mixed approach
tokens and the nth iteration costs I + (n − 1) (O + R) + O         can be observed in Table I. Importantly, there is an overlap
tokens. In contrast, due to the lack of feedback, each             between the unsolved cases: the mixed approach solves all
sampling iteration only consumes I + O tokens. In total for n      benchmarks solved by sampling and two additional ones. For
iterations, we have token costs of n(I + O) for sampling vs.       invariants, the additional solved benchmark is a loop invariant
n(I + O) + n(n−1) 2    (O + R) for feedback-based techniques.      for array reversal. This invariant is found by GPT 4O at the
Effectively, sampling grows linear in the number of steps          8th feedback step (in two out of five runs). For subcontracts,
while feedback-based techniques have a quadratic term.             the instance only found by the mixed approach is a contract
   Just as we previously plotted the success rate for a growing    for copying a range of an array. However, that contract was
number of feedback/sampling steps, we can now plot the             found in the first iteration, i.e., without any feedback.
success rate for a growing allocated token ratio. The results of         Results: As a positive result, our experiments provide evi-
this experiment are based on the same dataset as the previous      dence that iterative approaches (whether feedback or sampling-
experiment and consider 5 runs. We evaluated our data up to        based) improve the LLM’s success rate for annotation genera-
token ratio 14 and the results can be found in Figure 3. In        tion. This insight suggests that more refined, iterative strategies
this perspective, sampling early on has a significant advantage    could lead to even stronger results which warrants further
over the feedback-based approach for subcontract generation        exploration. Our observation also strengthens the case for an
and we also see a weak indication that sampling might be           intersymbolic approach that couples LLM generation with ver-
superior for invariant generation.                                 ification as humans cannot be expected to inspect the LLM’s
      A Mixed Approach: Based on the observations from             many solutions candidates. We also note that an approach solv-
Figure 2, we hypothesize that the feedback-based approach          ing approx. 85% of JML invariant synthesis problems and 57%
eventually stagnates. Moreover, the feedback-based approach        of submethod contract problems is unquestionably promising.
cannot be scaled to arbitrary step sizes due to the size of the          Limitations: The shaded areas in Figures 2 and 3 indicate
LLM’s context window which only admits limited conversa-           that our results are not yet statistically significant. Although
our benchmark contains a large number of relevant Java and                    2. Beckert, B., Kirsten, M., et al.: Modular Verification of JML Contracts
JML features [3, Table 1], we require a larger set of representa-                Using Bounded Model Checking. In: Margaria, T., Steffen, B. (eds.)
                                                                                 ISoLA 2020, Rhodes, Greece, October 20-30, 2020, Proceedings, Part
tive instances to validate our hypotheses. Moreover, our results                 I. LNCS, vol. 12476, pp. 60–80. Springer, Heidelberg (2020). https://doi.
only suggest that the current feedback approach is insufficient                  org/10.1007/978-3-030-61362-4 4
to improve efficiency over sampling-based approaches. This                    3. Beckert, B., Klamroth, J., et al.: Towards Combining the Cognitive
                                                                                 Abilities of Large Language Models with the Rigor of Deductive Progam
result could change through further prompt engineering which,                    Verification. In: Margaria, T., Steffen, B. (eds.) ISoLA 2024, Crete,
again, requires a larger benchmark set. Finally, further research                Greece, October 27-31, 2024, Proceedings, Part IV. LNCS, vol. 15222,
is necessary to extend our approach to larger gaps in the                        pp. 242–257. Springer, Heidelberg (2024). https://doi.org/10.1007/978-
                                                                                 3-031-75387-9 15
auxiliary specification (e.g. multiple missing loop invariants)               4. Brown, T.B., Mann, B., et al.: Language Models are Few-Shot Learners.
                                                                                 In: Larochelle, H., Ranzato, M. (eds.) Advances in Neural Informa-
                          IV. D ISCUSSION                                        tion Processing Systems 33: Annual Conference on Neural Information
   This work presents our current methodology for evaluating                     Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual
                                                                                 (2020)
different LLM prompting strategies for error recovery and                     5. Chakraborty, S., Lahiri, S.K., et al.: Ranking LLM-Generated Loop
presents some first evaluation results on error recovery in                      Invariants for Program Verification. (2023). https : / / doi . org / 10 . 18653 /
LLM-based JML synthesis. We found that an iterative ap-                          V1/2023.FINDINGS-EMNLP.614
                                                                              6. Cok, D.R.: OpenJML: Software verification for Java 7 using JML,
proach indeed improves the success rate which strengthens the                    OpenJDK, and Eclipse. In: Dubois, C., Giannakopoulou, D., Méry, D.
argument for our verification-based intersymbolic approach.                      (eds.) Proceedings 1st Workshop on Formal Integrated Development
For future work, we hope to repeat and extend the experiments                    Environment, F-IDE 2014, Grenoble, France, April 6, 2014. EPTCS,
                                                                                 pp. 79–92 (2014). https://doi.org/10.4204/EPTCS.149.8
presented using larger benchmark datasets. More generally, we                 7. Granberry, G., Ahrendt, W., Johansson, M.: Specify What? A Case-Study
hope to extend our work in the following directions:                             using GPT-4 and Formal Methods For Specification Synthesis. In: AI for
      Sampling vs. Feedback: Unlike many other domains,                          Math Workshop @ ICML 2024 (2024). https://openreview.net/forum?id=
                                                                                 ZRTcPkNl7v
specification generation has the advantage of providing a vast                8. Greiner, S., Bühlmann, N., et al.: Automated Generation of Code Con-
set of tools to check the correctness of solutions. In principle,                tracts: Generative AI to the Rescue? In: Proceedings of the 23rd ACM
we could thus “simply” generate a large number of solutions                      SIGPLAN International Conference on Generative Programming: Con-
                                                                                 cepts and Experiences. GPCE ’24, pp. 1–14. Association for Computing
and find the needle in the haystack, i.e., the one specification                 Machinery, Pasadena, CA, USA (2024). https://doi.org/10.1145/3689484.
that is consistent with our partially annotated input file. There                3690738
are of course limitations to this approach: When our code                     9. Janßen, C., Richter, C., Wehrheim, H.: Can ChatGPT support software
                                                                                 verification? In: Beyer, D., Cavalcanti, A. (eds.) Fundamental Approaches
has multiple annotation gaps, it may be necessary to fill all                    to Software Engineering - 27th International Conference, FASE 2024,
of them before verification, which quickly becomes work-                         Luxembourg City, Luxembourg, April 6-11, 2024, Proceedings. LNCS,
intensive if an individual solution by the LLM has a low                         vol. 14573, pp. 266–279. Springer, Heidelberg (2024). https://doi.org/10.
                                                                                 1007/978-3-031-57259-3 13
chance of being correct. Hence, moving up the left end of                    10. Leavens, G.T., Poll, E., et al.: JML Reference Manual. Draft revision
the curve in Figures 2 and 3 is a highly desirable objective:                    2344. May 2013. http://www.eecs.ucf.edu/ ∼leavens/JML//OldReleases/
We want to obtain successful specifications within the first                     jmlrefman.pdf.
                                                                             11. Kamath, A., Senthilnathan, A., et al.: Finding Inductive Loop Invariants
attempts as often as possible. We hope that an evaluation w.r.t.                 using Large Language Models. CoRR abs/2311.07948 (2023). arXiv:
a recently released dataset [8] for JML annotation may help us                   2311.07948
better understand the advantages and drawbacks of different                  12. Lathouwers, S., Huisman, M.: Survey of annotation generators for de-
                                                                                 ductive verifiers. Journal of Systems and Software 211, 111972 (2024).
prompting techniques in this context.                                            https://doi.org/10.1016/j.jss.2024.111972
   Future work will also focus on deriving textual represen-                 13. Leino, K.R.M., Moskal, M.: Usable auto-active verification. In: Ball, T.,
tations of failed proof attempts that are more effective as                      Zuck, L., Shankar, N. (eds.) Usable Verification Workshop (2010). https:
                                                                                 //fm.csl.sri.com/UV10
feedback to the LLM. How this information can be extracted                   14. Pei, K., Bieber, D., et al.: Can Large Language Models Reason about
from KeY’s proof tree is a nontrivial question.                                  Program Invariants? In: Krause, A., Brunskill, E. (eds.) Proceedings of
      Beyond Verification: For the quick evaluation of specifi-                  the 40th International Conference on Machine Learning. Proceedings of
                                                                                 Machine Learning Research, pp. 27496–27520. PMLR (2023). https://
cation candidates, we plan to explore additional checks using,                   proceedings.mlr.press/v202/pei23a.html
e.g., testing/fuzzing before attempting verification. Counterex-             15. Platzer, A.: Intersymbolic AI - Interlinking Symbolic AI and Subsymbolic
amples could then also be used to devise feedback to the LLM.                    AI. In: Margaria, T., Steffen, B. (eds.) ISoLA 2024, Crete, Greece, Octo-
                                                                                 ber 27-31, 2024, Proceedings, Part IV. LNCS, vol. 15222, pp. 162–180.
      Beyond Filling Gaps: Our experiments evaluated the                         Springer, Heidelberg (2024). https://doi.org/10.1007/978-3-031-75387-
ability of LLMs to fill the one gap in a partially JML-annotated                 9 11
Java file. As a next step, we want to devise a strategy that                 16. Sun, C., Sheng, Y., et al.: Clover: Closed-Loop Verifiable Code Genera-
                                                                                 tion. In: Avni, G., Giacobbe, M. (eds.) AI Verification - First International
generates all specifications to prove a given top-level specifi-                 Symposium, SAIV 2024, Montreal, QC, Canada, July 22-23, 2024, Pro-
cation (as a first step, by generating all necessary submethod                   ceedings. LNCS, vol. 14846, pp. 134–155. Springer, Heidelberg (2024).
and loop-invariant specifications). This could greatly increase                  https://doi.org/10.1007/978-3-031-65112-0 7
                                                                             17. Wu, H., Barrett, C., Narodytska, N.: Lemur: Integrating Large Language
the practicability of the approach.                                              Models in Automated Program Verification. In: The Twelfth International
                                                                                 Conference on Learning Representations (2024). https://openreview.net/
                            R EFERENCES                                          forum?id=Q3YaCghZNt
 1. Ahrendt, W., Beckert, B. (eds.): Deductive Software Verification - The   18. Yao, J., Zhou, Z., et al.: Leveraging Large Language Models for Au-
    KeY Book - From Theory to Practice. Springer (2016)                          tomated Proof Synthesis in Rust. CoRR abs/2311.03739 (2023). arXiv:
                                                                                 2311.03739
                       A PPENDIX                               @ decreases ...;
A. LLM Prompts                                                 @ assignable ...;
                                                             @*/
  Below we provide examples for the prompts used to elicit
                                                             ‘‘‘
specifications from the LLM.
  1) Invariant Generation: We invoke GPT with the follow-    For feedback-based approaches, we distinguish between syn-
ing system message:                                          tactical and semantical errors. For syntactical errors, we use
                                                             the following prompt to continue the conversation:
You are an assistant for JML annotation.
In the first message of this conversation, you are           The provided code is not valid JML. Please try
     provided with a Java class with partial JML                 again and make sure to provide a valid JML
    annotation.                                                  loop invariant.
Additionally, you are provided with natural                  This might describe the reason why change is
    language instructions that describe the task                 required:
    to be completed.                                         Beware that the error message may contain variable
JML annotation is a complicated task, but you are                 names from inside the proof system that are
    very capable and a perfect fit for this job.                 not available in the original code.
First, think step by step: What does the code do?            Such variable names must not in your JML answer;
    What is the context in which the code is                     only use variable names from the original code
    executed? What variables are relevant?                       .
Draft a behavioral description in natural language           <parser error>
    .
                                                             An example for a parser error message could be:
Subsequently, translate this description into JML
    annotation.                                              Error during JML parsing: Failed to parse JML
You should only provide the JML annotation and not               fragment: Encountered unexpected token: \"(\"
     the Java code.                                              \"(\"
We will then use the KeY verification system to                  at line 3, column 7.
    check if the JML annotation is correct.
If the program verification fails, you will be               Was expecting one of: <list of possible options>
    provided with information about the failure
                                                               For semantical errors we use the following prompt:
    and asked to correct the JML annotation.
Always add the JML keyword ‘normal_behavior‘ to              The provided JML does not solve the task. The KeY
    the contract -- this guarantees that no                      verification told me that the JML is wrong
    exceptions are being thrown.                                 because some proof goals were not closed:
Your answers should always have the following                Beware that the error message may contain variable
    format where the the <X> is substituted by the                names from inside the proof system that are
     JML annotation suggested by you:                            not available in the original code.
<your natural language reasoning>                            Such variable names must not in your JML answer;
‘‘‘                                                              only use variable names from the original code
/*@ <X>                                                          .
*/                                                           During verification, the following proof branches
‘‘‘                                                              could not be closed:
                                                             <proof branch labels>
Subsequently, we prompt GPT with the following prompt to
                                                             Please fix the JML loop invariant.
generate a loop invariant:
                                                             Examples for a proof branch label could be:
Given the following Java class:
’’’                                                          Normal Execution (_a != null)
<partially annotated file>
’’’                                                          Body Preserves Invariant
Please provide a loop invariant for the loop
    construct with the comment ‘//Add invariant              Use Case
    here‘ of the method ’<method name>’
Beware this annotation has to be a loop invariant.
    A loop invariant typically has the following
    structure:
‘‘‘
/*@ loop_invariant ...;
   2) Submethod Contract Generation: We invoke GPT with      @ assignable ...; // Fields that are assignable
the following system message:                                  in the called method.
You are an assistant for JML annotation.                   @*/
In the first message of this conversation, you are         ‘‘‘
     provided with a Java class with partial JML             For feedback-based approaches, we distinguish between
    annotation.                                            syn- tactical and semantical errors. For syntactical errors, we
Additionally, you are provided with natural                use the following prompt to continue the conversation:
    language instructions that describe the task
    to be completed.                                       The provided code is not valid JML. Please try
JML annotation is a complicated task, but you are              again and make sure to provide a valid JML
    very capable and a perfect fit for this job.               contract.
First, think step by step: What does the code do?          This might describe the reason why change is
    What is the context in which the code is                   required:
    executed? What variables are relevant?                 Beware that the error message may contain variable
Draft a behavioral description in natural language              names from inside the proof system that are
    .                                                          not available in the original code.
Subsequently, translate this description into JML          Such variable names must not in your JML answer;
    annotation.                                                only use variable names from the original code
You should only provide the JML annotation and not             .
     the Java code.                                        <parser error>
We will then use the KeY verification system to
    check if the JML annotation is correct.                Was expecting one of: <list of possible options>
If the program verification fails, you will be
    provided with information about the failure            Always add the JML keyword ‘normal_behavior‘ to
    and asked to correct the JML annotation.                   the contract -- this guarantees that no
Always add the JML keyword ‘normal_behavior‘ to                exceptions are being thrown.
    the contract -- this guarantees that no                An example for a parser error message could be:
    exceptions are being thrown.
Your answers should always have the following              Error during JML parsing: Failed to parse JML
    format where the the <X> is substituted by the             fragment: Encountered unexpected token: \"
     JML annotation suggested by you:                          loop_invariant\" \"loop_invariant\"
<your natural language reasoning>                              at line 9, column 5.
‘‘‘                                                          For semantical errors we use the following prompt:
/*@ <X>
                                                           The provided JML does not solve the task for the
*/
‘‘‘                                                            method ’<violated contract method>’.
                                                           The KeY verification told me that the JML is wrong
Subsequently, we prompt GPT with the following prompt to        because some proof goals were not closed:
generate a contract:                                       Beware that the error message may contain variable
Given the following Java class:                                 names from inside the proof system that are
’’’                                                            not available in the original code.
<partially annotated file>                                 Such variable names must not in your JML answer;
’’’                                                            only use variable names from the original code
Please provide a JML annotation to the method ’<               .
    called method>’ such that the contract                 During verification, the following proof branches
    specified by ’<calling method>’ is satisfied.              could not be closed:
A contract for a submethod typically has the               <proof branch labels>
    following structure:                                   Please fix the JML contract.
‘‘‘                                                        Always add the JML keyword ‘normal_behavior‘ to
/*@ normal_behavior // Ensures that no exceptions              the contract -- this guarantees that no
    are thrown by submethod                                    exceptions are being thrown.
  @ requires ...; // Requirements for an
                                                             Examples for a proof branch label could be:
    invocation of the submethod, based on the
    calling method.                                        Post (<called method name>)
  @ ensures ...; // Guarantees that the submethod
    will satisfy after the invocation.
