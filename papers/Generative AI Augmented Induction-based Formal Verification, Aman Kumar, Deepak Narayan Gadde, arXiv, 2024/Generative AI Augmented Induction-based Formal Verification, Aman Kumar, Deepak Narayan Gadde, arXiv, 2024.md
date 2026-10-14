                                             To appear at the 37th IEEE International System-on-Chip Conference, Sep 16-19 2024, Dresden, Germany


                                           Generative AI Augmented Induction-based Formal
                                                            Verification
                                                                        Aman Kumar                                          Deepak Narayan Gadde
                                                                  Infineon Technologies                                     Infineon Technologies
                                                                    Dresden, Germany                                          Dresden, Germany
                                                                Aman.Kumar@infineon.com                                  Deepak.Gadde@infineon.com


                                                                                                         Abstract
                                                  Generative Artificial Intelligence (GenAI) has demonstrated its capabilities in the present world that
arXiv:2407.18965v1 [cs.AI] 18 Jul 2024




                                              reduce human effort significantly. It utilizes deep learning techniques to create original and realistic content
                                              in terms of text, images, code, music, and video. Researchers have also shown the capabilities of modern
                                              Large Language Models (LLMs) used by GenAI models that can be used to aid hardware development.
                                              Formal verification is a mathematical-based proof method used to exhaustively verify the correctness of a
                                              design. In this paper, we demonstrate how GenAI can be used in induction-based formal verification to
                                              increase the verification throughput.
                                                                                                       Index Terms
                                                   Generative AI, k-Induction, Formal Verification

                                                                                                   I. I NTRODUCTION
                                            Formal verification-based hardware verification is a highly desirable but labour-intensive task. It is an exhaustive
                                         verification technique that uses mathematical proof methods to verify if the design implementation matches its
                                         specifications [1]. Although formal verification ensures the functional correctness of the design, achieving a full
                                         proof of properties written to verify the design could be challenging, especially for complex designs [1]. Modern
                                         formal verification tools use k-induction-based proof. This approach allows them to prove the design correctness
                                         for all time, rather than just the first few time steps [2]. To avoid inductive step failures, it is necessary to use helper
                                         assertions that act as assumptions or invariants once proven. These helper assertions are also known as lemma.
                                         Moreover, in case an assertion fails in its inductive step, it takes human effort to find the root cause from Counter
                                         Example (CEX) and write a helper assertion to fix the failure. To address this complexity of formal verification, we
                                         explore the potential of GenAI to automate assertion generation, which has proved in recent times to be a suitable
                                         tool [3] [4]. We demonstrate GenAI based flow that can generate helper assertions based on a given RTL design
                                         and generate lemmas in the event of an inductive step failure during formal verification.
                                                                                                   II. BACKGROUND
                                         A. Induction-based Formal Verification
                                            Bounded Model Checking (BMC) can find bugs in large designs. However, the correctness of a property is
                                         guaranteed only for the analysis bound. Induction-based proof must be applied to prove the design will work all
                                         the time rather than just the first S time steps. Induction is a method to check if the design is in a random good
                                         state (state of design that doesn’t produce a CEX) whether it will be in a good state at the next cycle [2]. Induction
                                         with increasing depth k, consists of two steps, base and k-step induction as described in [5]. The base case utilizes
                                         the initial-state constraint, whereas the inductive step does not. Consequently, the inductive step may encompass
                                         unreachable states. At the inductive stage, the formal tool unrolls the design into small pieces and is unaware of the
                                         unreachable states. It can start from any arbitrary (unreachable) state and end up in a state where the property fails
                                         [6]. In practice, this might prevent the induction proof from succeeding without incorporating additional constraints,
                                           This work has been developed in the project VE-VIDES (project label 16ME0243K) which is partly funded within the Research Programme
                                         ICT 2020 by the German Federal Ministry of Education and Research (BMBF).



                                         ©2024 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future
                                         media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or
                                                           redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
such as stronger induction invariants than the property itself [5]. These induction invariants or helper assertions
rule out the CEX by reducing the state-space during the inductive step.
B. Generative Artificial Intelligence (GenAI)
   GenAI is a type of AI technique that has the ability to produce original content across various formats, such as text,
images, audio, and other forms of media. Propelled by the progress in deep learning, Natural Language Processing
(NLP), and continuously improving data processing capabilities, LLMs stand at the forefront of GenAI. An LLM
is a type of GenAI that specializes in understanding and generating human language by predicting subsequent parts
of text based on the context provided in the input it receives. It is pre-trained on a large corpus of text and then
fine-tuned for specific tasks or to improve its performance in generating coherent and contextually relevant text
[7]. In hardware verification, GenAI can be utilized to aid the verification processes such as assertion generation,
failure debugging, testbench and stimulus generation [3].
                                             III. L EMMAS U SING G ENERATIVE AI



        Specification              Promt Template                      LLM                  Generated SVAs




                                                                                                  Formal                 Proof
                                           RTL
                                                                                                   Tool


                                         Fig. 1: Helper assertion generation using LLM

   Fig. 1 shows the flow to generate lemmas or helper assertions. There are two inputs to the LLM. The first input
is the specification document that contains information about the functionality of the design. The second input is
the actual RTL code written in any Hardware Description Language (HDL). The LLM uses these two pieces of
information and analyzes them to come up with a set of helper assertions that can be used for formal verification.
In the next step, the generated assertions and the RTL design are provided to the formal tool and the tool proves
the correctness of the properties. Once proven, these assertions would be used as assumptions that help to prove
other complex assertions.
                            IV. I NDUCTION S TEP FAILURE A NALYSIS USING G ENERATIVE AI



         Inductive Step
            Failure                    Promt Template                     LLM                 Generated SVAs
             CEX


                                                                                                    Formal                Proof
                                              RTL
                                                                                                     Tool

                         Fig. 2: Helper assertion generation for induction step failure using LLM

  Fig. 2 shows the flow to analyze the induction step failure during formal verification and use the capabilities
of LLM to generate helper assertions. The LLM model requires two inputs. The first input is the CEX from the



©2024 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future
media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or
                  redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
inductive step failure. This is usually a waveform diagram that highlights the failure. The second input is the RTL
design that is used by the LLM to analyze the design and relate it to the counterexample. After analysis, the LLM
generates the necessary helper assertion that prevents inductive step failure during the next iteration of formal proof.
As an example, consider the simple design of two synchronized counters given in Listing 1.
 1   module s y n c c o u n t e r s ( i n p u t c l k , r s t , o u t p u t l o g i c [ 3 1 : 0 ] c o u n t 1 , c o u n t 2 ) ;
 2     a l w a y s @( p o s e d g e c l k o r p o s e d g e r s t ) b e g i n
 3         i f ( r s t ) begin
 4             c o u n t 1 <= 32 ’ b0 ;
 5             c o u n t 2 <= 32 ’ b0 ;
 6         end e l s e b e g i n
 7             c o u n t 1 ++;
 8             c o u n t 2 ++;
 9         end
10     end
11   endmodule
                                          Listing 1: Two synchronized counters design

  The following SVA property in Listing 2 should obviously hold true:
 1    property equal count ;
 2      &c o u n t 1 |−> &c o u n t 2 ;
 3    endproperty
                                          Listing 2: Two synchronized counters design

However, the induction step fails with the CEX in Fig. 3.




                               Fig. 3: Induction step failure (31st bit of count2 is not logic 1)

   Upon providing the RTL and the CEX, the LLM generated a helper assertion mentioned in Listing 3 that proved
the original assertion faster.
 1    property helper ;
 2      c o u n t 1 == c o u n t 2 ;
 3    endproperty
                       Listing 3: Helper assertion generated for the synchronized counters example

                                                              V. R ESULTS
   We used the helper assertion generation flow described in this paper for fairly complex designs. We utilized both
flows to generate general helper assertions as well as for induction step failure. The designs used were counters and
ECC. Usually, the flow was able to figure out necessary helper assertions that helped in faster proof for complex
properties. It was also observed that the quality of generated assertions was much better in the case of LLMs from
OpenAI such as GPT-4-Turbo and GPT-4o compared to Llama or Gemini. This could be due to the fact that the
LLMs from OpenAI are usually trained using relatively higher training data than the others.


©2024 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future
media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or
                  redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
                                                          VI. C ONCLUSION
   In this paper, we have demonstrated a flow to generate helper assertions or lemmas using GenAI to reduce
the efforts for induction-based formal verification. The flow aims at generating usual helper assertions that reduce
the proof time for complex properties as well as inductive invariants that help resolve induction step failures.
Although LLMs prove to be effective in generating assertions for our designs, one must be aware of the limitations
of using GenAI especially for artificial hallucinations that produce vulnerable results [8]. It is recommended to
analyze the output from the LLM before using it productively to avoid false positives and comprehend the so-called
human-in-the-loop AI.
                                                             R EFERENCES
[1]   A. Kumar, “Pragmatic Formal Verification of Sequential Error Detection and Correction Codes (ECCs) used
      in Safety-Critical Design,” DVCon US, 2023.
[2]   “JasperGold (JG) State-Space Tunneling (SST) Rapid Adoption Kit,” Cadence, Tech. Rep., Aug. 2017.
[3]   D. Yu et al., “Large Language Model For Verification: A Review And Its Application In Data Augmentation,”
      DVCon US, 2024.
[4]   W. Fang et al., Assertllm: Generating and evaluating hardware verification assertions from design specifica-
      tions via multi-llms, 2024. arXiv: 2402.00386 [cs.AR].
[5]   “Proof by induction,” in SAT-Based Scalable Formal Verification Solutions. Boston, MA: Springer US, 2007,
      pp. 175–183.
[6]   D. Gilday, “Human-guided proof closure,” Cadence Jasper User Group, 2021.
[7]   T. Amaratunga, Understanding Large Language Models: Learning Their Underlying Concepts and Technolo-
      gies. Apress, 2023, ISBN: 9798868800160.
[8]   D. N. Gadde et al., All artificial, less intelligence: Genai through the lens of formal verification, 2024. arXiv:
      2403.16750 [cs.AI].




©2024 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future
media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or
                  redistribution to servers or lists, or reuse of any copyrighted component of this work in other works.
