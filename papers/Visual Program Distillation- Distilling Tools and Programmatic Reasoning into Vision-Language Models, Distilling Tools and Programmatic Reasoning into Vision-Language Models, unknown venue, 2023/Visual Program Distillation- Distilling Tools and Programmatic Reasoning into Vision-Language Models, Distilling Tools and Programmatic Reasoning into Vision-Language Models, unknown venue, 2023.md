                                                                    Visual Program Distillation:
                                            Distilling Tools and Programmatic Reasoning into Vision-Language Models

                                                      Yushi Hu1,2 * Otilia Stretcu1 Chun-Ta Lu1 Krishnamurthy Viswanathan1
                                                            Kenji Hata1 Enming Luo1 Ranjay Krishna2 Ariel Fuxman1
                                                                     1
                                                                       Google Research 2 University of Washington
                                                                            https://visual-program-distillation.github.io/
arXiv:2312.03052v2 [cs.CV] 5 Apr 2024




                                                                                                                                                                           TOOLS
                                                                    Abstract
                                                                                                                  Object Detection                          Depth Estimation
                                            Solving complex visual tasks such as “Who invented the
                                                                                                                      Captioning                               Knowledge
                                        musical instrument on the right?” involves a composition of
                                        skills: understanding space, recognizing instruments, and                         OCR
                                                                                                                                 ABC

                                                                                                                                                                     VQA
                                                                                                                                 ABC                            ?
                                        also retrieving prior knowledge. Recent work shows promise
                                        by decomposing such tasks using a large language model
                                        (LLM) into an executable program that invokes specialized vi-                        LLM-generated Programs
                                        sion models. However, generated programs are error-prone:
                                        they omit necessary steps, include spurious ones, and are
                                                                                                                                                      distillation
                                        unable to recover when the specialized models give incor-
                                        rect outputs. Moreover, they require loading multiple models,
                                        incurring high latency and computation costs. We propose                                  Vision-Language Model
                                        Visual Program Distillation (VPD), an instruction tuning
                                        framework that produces a vision-language model (VLM) ca-               Figure 1. We introduce Visual Program Distillation (VPD), a frame-
                                        pable of solving complex visual tasks with a single forward             work which leverages tools and LLM-generated programs to synthe-
                                        pass. VPD distills the reasoning ability of LLMs by using               size cross-modal reasoning data for vision-language model (VLM)
                                        them to sample multiple candidate programs, which are then              training. VPD distills the skills in specialist models (e.g., detec-
                                        executed and verified to identify a correct one. It translates          tion, depth estimation) and LLM reasoning ability into VLMs. Our
                                                                                                                generalist models trained with VPD, PaLI-X-VPD (55B), out-
                                        each correct program into a language description of the
                                                                                                                perform prior VLMs on a broad range of tasks, while producing
                                        reasoning steps, which are then distilled into a VLM. Exten-            human-interpretable and faithful reasoning steps.
                                        sive experiments show that VPD improves the VLM’s ability
                                        to count, understand spatial relations, and reason compo-               of competent vision models. Even state-of-the-art (SOTA)
                                        sitionally. Our VPD-trained PaLI-X outperforms all prior                proprietary vision-language models such as GPT-4V [49] do
                                        VLMs, achieving state-of-the-art performance across com-                not perform well on tasks that involve counting and spatial
                                        plex vision tasks, including MMBench, OK-VQA, A-OKVQA,                  reasoning [70]. They find it difficult to count (TallyQA [1]),
                                        TallyQA, POPE, and Hateful Memes. An evaluation with                    to compositionally reason (GQA [26]), and to reason with ex-
                                        human annotators also confirms that VPD improves model                  ternal knowledge (OK-VQA [44], A-OKVQA [53]). Many
                                        response factuality and consistency. Finally, experiments on            of these tasks require VLMs to conduct compositional rea-
                                        content moderation demonstrate that VPD is also helpful for             soning, which still remains an unsolved challenge. For in-
                                        adaptation to real-world applications with limited data.                stance, answering the question “Who invented the musical
                                                                                                                instrument on the right?” involves a composition of skills:
                                        1. Introduction                                                         identifying objects, applying spatial reasoning to locate the
                                                                                                                one on the right, recognizing the musical instrument, and
                                        Vision-language models (VLMs) have become the pre-                      accessing prior knowledge to retrieve the inventor.
                                        trained backbone for many computer vision tasks [2, 4, 7, 9–                In contrast, large language models (LLMs) have demon-
                                        11, 34, 39, 41, 60, 63, 73, 79]. Yet, all these models still fall       strated remarkable performance at generating code that
                                        short of solving numerous visual reasoning tasks expected               solves complex and compositional tasks [3, 8, 43, 49, 68].
                                           * Work done while interning at Google Research.                      Several recent papers [16, 20, 25, 57] capitalize on this by


                                                                                                            1
            Input Data                                Program Generation                                               VLM Fine-Tuning                        Output
                                                                                                                                           There are 3
                Q: How many                                                                                                         CoT:
                                                                                                                                           buses in the
                    buses are                                                                         I:                                   image.The
                                                                                                                                           bus at...
 I:                 not yellow?     LLM Code          Program         Program     Conversion
                                    Generation        Execution       Filtering     to CoT                                 VLM
                 A: 1                                                                                 Q: How  many buses
                                                                                                         are not yellow?            A:     1              VLM-VPD


                                                                                               Program                                                    Available Tools
           LLM Code Generation                  Program Execution with Visual Modules          Filtering               Convert to Chain-of-Thought
                                                   find("bus")
                                      Object       (469 124 726 351) bus                                           There are 3 buses in the
                                     Detector
                                                   (494 330 692 512) bus                                           image. The bus at 469 124              LLM         VLM
                                                   (494 464 710 667) bus
                                                                                                                   726 351 is not yellow. The
                                                         Q: Is this bus yellow?
                                                                                                           LLM
                                                         A: No                                                     buses at 494 330 692 512
                                                                                                                   and 494 464 710 667 are                 Object      Depth
                                      VQA                Q: Is this bus yellow?                                                                           Detector   Estimator
                                                         A: Yes                                                    yellow. Thus, there is 1
                                                    ...
                                                  Program Output: 1
                                                                                                                   bus that is not yellow.
                                                                                                                                                               VQA

Figure 2. Overview of Visual Program Distillation (VPD). VPD uses an LLM and specialized vision tools to generate faithful chain-of-
thought (CoT) training data for vision-language models (VLMs). Given a multimodal input, our 4-step data synthesis pipeline generates a
CoT that answers the query. In the example above, our synthesized CoT contains a series of reasoning steps: find all buses, check if each bus
is yellow, and aggregate the count into a final answer. The CoT also contains the grounding information given by object detection.

prompting LLMs to generate programs where each step cor-                                insights to deliver a training paradigm that surpasses the sum
responds to a reasoning step. The programs invoke spe-                                  of its parts: It relies on (1) advancements in visual programs
cialized “tools” (or specialized vision models) to explicitly                           that use tools [20] and (2) the recent breakthroughs in dis-
execute each reasoning step. For the question above, the                                tillation through chain-of-thought reasoning [21]. Given a
program would call an “object detector” tool to identify and                            labeled training dataset of complex visual tasks, VPD gener-
isolate all the objects, a “fine-grained object classification”                         ates a correct program, and then distills its reasoning steps
tool to recognize the musical instrument, and a “knowledge-                             into vision-language models. To avoid using programs that
based question answering” tool to retrieve its inventor.                                give the wrong answer, VPD prompts an LLM to generate
   Although innovative, generating explicit programs is com-                            multiple candidate programs, and executes every one of them.
putationally expensive in practice, prone to errors, and still                          When labeled data is available, it then filters for programs
underperforms end-to-end models. Programs require load-                                 that produce the correct answer upon execution. Therefore,
ing and executing multiple tools, leading to high latency                               our programs comprise multiple vision tools, are executable,
and computational cost. Moreover, generated programs may                                and yield the correct answer when executed. Next, VPD
omit necessary steps or include spurious ones. Even when                                rewrites the correct programs as natural language chain-of-
the program is correct, vision model invocations can produce                            thought instructions and uses step-by-step distillation [21]
incorrect outputs, from which the overall program cannot                                to inject the reasoning abilities into VLMs.
recover. Unfortunately, empirical results show that visual                                  Our best instruction-tuned model, PaLI-X-VPD
programs still fall short of end-to-end fine-tuned models [16].                         (55B), sets a new SOTA result on 8 classical VQA tasks
   Another line of work is visual instruction tuning [39],                              and 2 zero-shot multimodal benchmarks. Our models even
which tries to distill the instruction-following ability of                             outperform the recent SOTA established by PaLI-X [10].
LLMs into VLMs. They prompt LLMs with image captions                                    Importantly, we conduct a quality evaluation with human
and bounding box annotations in order to generate queries                               raters which shows that PaLI-X-VPD generates more con-
and answers that are used to fine-tune VLMs [7, 23, 39, 65].                            sistent and faithful rationales compared to its counterpart
However, this approach has important limitations: image                                 trained using instruction-tuning data. In addition, we experi-
captions can miss fine-grained visual information, and LLM                              ment with PaLI-3(5B), and show that VPD also improves
are prone to producing inconsistent outputs for custom vi-                              the performance of smaller-scale models. Finally, experi-
sion representations like bounding boxes [18]. As a result,                             ments on Hateful Memes [29] show that VPD is also helpful
existing instruction-tuned VLMs still struggle with tasks that                          for adapting to new tasks, even when no labels are available.
requires complex visual reasoning [7, 14, 38, 40].
   In this work, we present Visual Program Distillation                                 2. Related work
(VPD), a novel distillation method that induces complex
cross-modal reasoning capabilities into vision-language mod-                            VPD is a general method for improving any vision-language
els (Fig. 2). As the name suggests, VPD combines two key                                model, and includes automatic program generation and train-


                                                                                   2
ing with chain-of-thought data as steps of the proposed                   into a chain-of-thought c (§3.1).
framework. We discuss each of these research areas.                    2. Distilling step-by-step: The visual input i, textual query
                                                                          q, and chain-of-thought c produced by the previous step
Vision-language models (VLMs). Most recent generative
                                                                          are distilled into a vision-language model (VLM) (§3.2).
VLMs share a common structure: a pre-trained visual en-
coder, a pre-trained LLM, and a connector between the two              3.1. Program generation and verification
modalities [2, 4, 9, 34, 39, 41, 60, 63, 73, 79]. The mod-
els are trained on large-scale image-text pairs from various           Our training data synthesis pipeline is illustrated in the blue
tasks to adapt to both modalities. They are also tuned on              boxes of Fig. 2, and consists of four stages. Given a sample
LLM-generated visual instructions to enable models to fol-             (i, q, y) consisting of a visual input i and a textual query q
low versatile instructions from users [39]. Some models also           about its content and, when available, its ground truth answer
include bounding boxes in the pre-training data to improve             y, we perform the following sequence of steps:
the VLM on visually grounded tasks [6, 7, 10, 41, 50, 61, 78].         1. Program generation with LLM: Given q, we generate
The bounding boxes are usually retrieved from COCO [37]                    a list of k candidate programs π(q) = {z1 , z2 , ..., zk },
and Visual Genome [32]. Different from prior work, our                     where π represents a program generation function.
method does not rely on provided dense annotations. We use             2. Program execution with vision modules: We execute each
LLM-generated code and specialized vision tools to generate                program zi with an execution engine ϕ to obtain its final
our own visual instruction-tuning data.                                    result ϕ(i, zi ) = ŷi . However, during program execution,
                                                                           we maintain the execution trace ti recording all the in-
Visual programming and agents. With the advancement of                     termediate function calls and outputs. At the end of this
large language models (LLMs) [3, 5, 13, 49, 59], recent work               step, we produce a list of programs, results, and execution
has started using LLMs as an interface to solving complex                  traces {(z1 , ŷ1 , t1 ), ..., (zk , ŷk , tk )}.
reasoning tasks with tools [12, 42, 51, 54, 76], and also as an        3. Program filtering: Among the k candidate programs from
agent for vision tasks [23, 25, 69, 71]. From this line of work,           the previous step, we keep a single tuple (z, ŷ, t) with
the most relevant to us are VisProg [20] and ViperGPT [16],                correct answer.
which leverage LLMs to generate executable programs with               4. Converting program execution traces into chain-of-
a sequence of invocations to specialized vision tools. They                thought rationales: We rewrite t into a CoT c using an
achieve SOTA zero-shot performance on various vision tasks,                LLM.
while being versatile and interpretable.                               We now discuss in detail each of the steps above.
Training and inference with chain-of-thought. Chain-                   Program generation. We adopt a similar approach with
of-Thought (CoT) [66] has become a popular approach to                 recent work [16, 20] in our program generation step, and use
improving LLM performance. Recent work such as Program-                PaLM-2 [3] as LLM to generate candidate programs for a
of-Thoughts (PoT) [8] and Faithful CoT [43] further improve            given query q. We prompt PaLM-2 with the same kind of
this framework by splitting inference into two steps: first            text prompt as used by ViperGPT, which contains a detailed
generate a program with LLM, then execute the program.                 description of the available vision modules, followed by the
This approach achieves better accuracy and reduces halluci-            query q (prompt in Appendix §D). The LLM is expected
nations in the reasoning steps. Moreover, CoT is also used             to directly output a Python function definition that will be
to train language models. Distill step-by-step [21], PaD [80],         executed in the following steps. However, in our experi-
and SCOTT [62] train smaller language models with CoT                  ments, we find that the success rate of top-k programs is
generated by LLMs, showing that this can improve model                 much higher than the top-1 program. Therefore, in contrast
performance and reasoning consistency. Mammoth [75]                    to prior work, which only samples one program z, when the
trains an LLM with a hybrid of CoT and PoT rationales and              ground truth answer y is available, we set a temperature T
achieves a SOTA model for math problems.                               for LLM decoding and sample a list of top-k candidate pro-
                                                                       grams {z1 , z2 , ..., zk } from the LLM. Then, we filter out one
3. Visual Program Distillation (VPD)                                   correct program z in later steps. As shown in our ablation in
We introduce VPD, a general model-agnostic framework that              §4.2, this becomes crucial to our performance gain. We use
distills the reasoning power of LLM-generated programs                 T = 0.5 and k = 5 for all our experiments. For unlabeled
together with the low-level image understanding abilities of           data, k = 1 and the filtering step can be skipped.
vision tools into a single vision-language model (Fig. 2). At          Program execution with vision modules. We use the same
its core, VPD consists of two major steps:                             execution engine ϕ as ViperGPT [16]. An LLM-generated
1. Program generation and verification: Given a textual                program zi is a Python function that takes the visual input i
    query q and a visual input i, VPD first generates a pro-           as input. While the LLM outputs the program as a sequence
    gram that solves the query by making use of vision mod-            of text, the execution engine ϕ is able to interpret this as a
    ules and tools, then converts the program execution trace          Python program and execute it, to obtain its return result


                                                                   3
ŷi . Additionally, ϕ also records the execution trace ti of the                 simultaneously fine-tuned on data synthesized for multiple
program zi , which keeps a record of all the vision module                       types tasks (e.g., free-form VQA, multiple choice).
calls, their inputs, and outputs. We use the following tools for                     Let f represent our VLM model. While the same VLM ar-
the program: PaLI-X [10] for simple visual queries, PaLI-X                       chitecture could solve all these tasks, it needs to be prompted
detection (distilled from OWLv2 [47]) for object detection;                      differently to adapt to the task. Following prior work [39],
Google Cloud Depth API [17] for depth estimation, and                            we manually design instructions for each task. For exam-
PaLM-2 [3] for external knowledge.                                               ple, for free-form VQA queries, the instruction is “Answer
Program filtering. As we discussed in §1, visual programs                        with a single word or phrase”, while for multiple-choice
are error-prone for a variety of reasons. The program might                      queries we use “Answer with the option letter from the given
be wrong, and the execution process can introduce additional                     choices directly”. During fine-tuning, we combine the train-
errors. To overcome these issues, we employ a program filter-                    ing samples generated for all tasks into a single dataset, so
ing step. We start by sampling top-k programs and attempt                        to account for the different types of tasks, we augment each
to execute each one. During this process, any program that                       sample with its corresponding task-specific prompt p.
fails execution is instantly discarded. We further filter the re-                    Using these instructions along with the data gener-
maining programs, the strategy depending on the availability                     ated in §3.1, we put together the training dataset D =
of labeled data. For tasks where human labels are available,                     {(ij , qj , ŷj , cj , pj )}N
                                                                                                             j=1 , where N is the total number of sam-
we select a single program per input sample whose answer                         ples, ij is the visual input, qj is the textual query, ŷi is the
is correct—that is, when the program output ŷi matches the                      visual program output2 , and cj is the CoT rationale.
human label y. In this case our visual program pipeline acts                         We train f to minimize a loss for predicting both the label
like a CoT rationale annotator. One potential problem is that                    and the rationale. As shown in the red box of Fig. 2, similar
some task answers are ambiguous. For example, for a ques-                        to [21], we treat predicting the output label ŷj and the ratio-
tion like “Where are the horses?”, the answers “mountain”                        nale cj as two separate optimization goals. However, since
and “mountains” are both correct. We adopt the method in                         VLMs are open-ended text generation models, they need
[28] and use an LLM to determine if the program output                           additional prompting to indicate whether we want a short
is correct (details in §D). If there is more than one correct                    answer or a long answer that includes a rationale. There-
program per question, we select the top scoring one, ac-                         fore, we append the suffix sc =“Explain the rationale to
cording to the scores provided by the program-generating                         answer the question” at the end of the prompt for generating
LLM ϕ. If no programs pass the test, the rated sample is not                     a CoT, and use the task instruction pj for short answers. Our
wasted—we simply use the correct answer y as supervision                         optimization objective is:
in our fine-tuning stage, without an associated CoT. When
no human-rated answer is available, we directly use the top                          L = Llabel + Lrationale                                               (1)
scoring executable program1 .                                                               N
                                                                                            X
                                                                                        =         ℓ(f (ij , qj , pj ), ŷj ) + ℓ(f (ij , qj , sc ), cj )   (2)
Converting program execution traces into chain-of-
                                                                                            j=1
thought rationales. After the filtering step, for each visual
input i and query q, we will have selected at most one pro-                      Here ℓ is the cross entropy-loss normalized by sequence
gram z together with its execution result ŷ and trace t. Since                  length to ensure that the labels (typically short) and ratio-
most existing VLMs have been pre-trained with text in nat-                       nales (typically long) have similar weights. Lrationale both
ural language and not code, we use an LLM to rewrite the                         teaches the VLM to generate faithful reasoning steps similar
execution trace t into a natural language CoT c for our VLM                      to program execution traces, and carries more information
distillation. Some examples are shown in §A. Concretely,                         beyond the label ŷ that also helps the VLM in better predict-
similar to prior work [23, 24], we hand-craft 20 examples                        ing the label. During test time, the rationale generation is
of how an input (q, z, t) can be converted into a CoT, and                       not required. We can adjust the task instruction to directly
use these as few-shots for prompting PaLM-2 [3], which                           get the short output label using p, and using sc to get the
performs in-context learning and generates CoTs for new                          human-interpretable reasoning steps if needed.
examples. We include a concrete example in §D.
3.2. Distilling step-by-step                                                     4. Experiments
In this step, we fine-tune a backbone VLM with the training                      In this section, we demonstrate VPD’s effectiveness by using
data generated in §3.1, distilling the knowledge and reason-                     it to train a generalist VLM. We attempt this for two VLMs
ing steps of our generated programs into a single end-to-end                     with different scales, PaLI-3 (5B) [11] and PaLI-X
model. We do so in a multitask fashion, where the VLM is                         (55B) [10]. Detailed experimental setups are given in §4.1.
   1 Studying ways to approximate program correctness strategies for unla-          2When labeled data is available, this is equivalent to the ground truth

beled data is an interesting direction for future work.                          label y due to our filtering strategy.


                                                                             4
        Is the girl to the right or to the left of the
        woman that is wearing a shirt?                                             covers subsets of a wide variety of VQA tasks, including
                                                                                   general VQA (VQAv2 [19]), optical character recognition
   The woman at 170 0 927 256 is wearing a                                         (OCRVQA [48]), compositional questions and reasoning
   shirt. The girl is at 202 216 813 468. Thus,
   the girl is to the right of the woman.                                          (GQA [26]), counting (TallyQA [1]), and VQA that involves
                                              PaLI-X-VPD                           external knowledge (OK-VQA [45] and A-OKVQA [52]).
                                                                                   The tasks contain a textual query and a short expected label.
                                         How many green vases are there?
                                                                                   We use the pipeline in §3.1 to synthesize CoT reasoning
                                                                                   steps for these labels, and tune the PaLI model with these
                                The vases at 348 139 771 371, 207
                                409 410 549, and 286 613 659 792 are               the loss in Equation 1. Notice that sometimes the pipeline
                                green. Thus, there are 3 green vases.              fails to find a program that generates the correct answer. In
                                                                  PaLI-X-VPD       that case, we set Lrationale to 0 and only keep Llabel . §4.2
Figure 3. Outputs of PaLI-X trained with VPD. Training with                        shows how many programs are kept after the filtering stage.
execution traces of filtered programs improves the model’s ability                 More details of the training data mixture is in §B.
to count, understand spatial relations, and reason compositionally.
The images are from Visual Genome [32].
                                                                                   Data for specialist models. While fine-tuning the generalist
                                                                                   model with VPD, we only use a subset of each task’s training
Qualitatively, models fine-tuned with VPD exhibit the ability                      data. To evaluate our model’s ability on each individual task,
to reason step-by-step like a program, as illustrated in Fig. 3,                   we continue fine-tuning PaLI-3-VPD and PaLI-X-VPD
and supported by human evaluation results (§4.3). Quantita-                        on each individual task on the training splits.
tive results show that our PaLI-3-VPD and PaLI-X-VPD                               Training setup. Both PaLI-3 and PaLI-X follow an encoder-
achieve new SOTA on a broad range of tasks, on both gener-                         decoder architecture, where images are encoded into visual
alist and per-task fine-tuning settings (§4.2). We also conduct                    tokens via a visual encoder and then passed into a UL2
a detailed analysis of the source of performance gain (§4.2).                      model. Due to resource constraint, we use LoRA [22] to
Finally, we conduct human evaluation on the quality of the                         fine-tune both PaLI models. Specifically, we add LoRA
rationales generated by our models, and compare it with                            weights on each linear layer in the attention blocks and the
rationales generated by an instruction-tuned model trained                         MLP blocks for both the encoder and decoder in the UL2
without VPD (§4.3).                                                                transformer. More training details are in §B.
4.1. Experimental setup                                                            Evaluation setup. We evaluate our models on a wide range
                                                                                   of tasks, including various VQA tasks and recent zero-shot
Backbone models. We use two state-of-the-art VLMs,                                 VLM benchmarks. Noted that A-OKVQA contains two
PaLI-3 (5B) [11] and PaLI-X (55B) [10] as our base                                 kinds of questions, multiple-choice (MC) and direct answer
models. Both take images and text as input, and generate                           (DA). We report results on both. TallyQA [1] contains com-
text as output. For simplicity, we further refer to them as                        plex counting questions that involve object relationships, at-
“PaLI model” when we discuss steps performed with each of                          tribute identification, and reasoning to get the correct answer.
them individually.                                                                 It contains two evaluation partitions, simple and complex.
                                                                                   TextVQA [55] focuses reading texts. We include it to evalu-
Data for Generalist Models. We fine-tune the pre-trained
                                                                                   ate our models on zero-shot tasks. In addition to VQA tasks,
PaLI model on two types of datasets to make it a generalist
                                                                                   we also test our models on two popular VLM benchmarks.
VLM—that is, a model that performs relatively well on any
                                                                                   POPE [36] focuses on VLM hallucination, containing binary
task without further training on that specific task:
                                                                                   questions of whether or not an object exists in the image.
    (1) Multimodal Instruction-Tuning (MMIT) tasks, created
                                                                                   MMBench [40] is a robust and comprehensive VLM bench-
in the spirit of Self-Instruct [64]. An LLM is prompted with
                                                                                   mark testing a range of fine-grained abilities (e.g., object
image captions, and generates task inputs and the desired
                                                                                   localization, attribute recognition, spatial relationship). De-
outputs about the corresponding image. Details of MMIT
                                                                                   tails of the evaluation sets and metrics are in §B.
tasks are covered in [65]. Note that these tasks cover a wide
variety of common use cases, but do not include the specific                       Baselines. We refer to the two PaLI models fine-tuned with
in-domain tasks used in this work.                                                 VPD as PaLI-3-VPD and PaLI-X-VPD, and compare
    (2) Academic task-oriented VQA tasks. Since image cap-                         them with various baselines. To evaluate the effectiveness
tions contain only a coarse description of visual information                      of VPD, we experiment with removing the synthesized CoT
in the image, and may miss details that are important for                          from our data mixture, and train the PaLI models with the
solving the task. Additionaly, LLM are likely to halluci-                          exact same hyper-parameters and steps. We call these models
nate during this data curation process. To further boost the                       as PaLI-3 Instruct and PaLI-X Instruct. For a
accuracy of our VLMs, we also fine-tune the PaLI models                            fair comparison, these models are also trained with the same
with academic task-oriented VQA tasks. The data mixture                            supervised loss for predicting the ground truth answers, on


                                                                               5
 Generalist Models                        VQAv2     GQA     OK-VQA                    A-OKVQA             TallyQA           TextVQA        POPE   MMB
                                                                                      MC   DA          Simp. Comp.
 Prior generalist VLMs
 Flamingo (80B) [2]                       82.0      -       57.8*                     -       -        -         -          57.1            -       -
 MiniGPT-4 (Vicuna-13B) [79]              -         43.5    -                         67.2    -        -         -          -               -      42.3
 InstructBLIP (Vicuna-13B) [14]           -         49.5*   -                         -       -        75.2*     57.5*      50.7*          78.9    44.0
 Shikra (Vicuna-13B) [7]                  77.4      -       47.2                      -       -        -         -          -              84.7    58.8
 Qwen-VL (9.7B) [4]                       78.8      59.3    58.6                      -       -        82.6*     65.8*      63.8            -      38.2
 Qwen-VL-Chat (9.7B) [4]                  78.2      57.5    56.6                      -       -        81.1*     64.0*      61.5            -      60.6
 mPLUG-Owl2 (8.2B) [73]                   79.4      56.1    57.7                      -       -        -         -          54.3*          86.2    64.5
 LLaVA-1.5 (Vicuna-13B) [38]              80.0      63.3    -                         -       -        76.9*     65.4*      61.3*          85.9    67.7
 Our instruction-tuned baselines
 PaLI-3-Instruct (5B)                     79.9      59.7    56.7                      78.3    57.6     81.9      70.4       63.3*          87.7    68.6
 PaLI-X-Instruct (55B)                    83.6      63.3    64.3                      84.1    61.5     85.5      75.4       65.0*          88.9    75.0
 Our visual program distillation models
 PaLI-3-VPD (5B)                          80.4      61.3    57.5                      78.5    56.5     83.1      70.9       63.7*          88.6    69.0
 PaLI-X-VPD (55B)                         83.9      64.9    64.6                      84.5    62.7     86.2      76.6       65.4*          88.8    76.2

Table 1. Comparison with SOTA generalist VLMs. PaLI-X-VPD outperforms all prior models. VPD improves performance on 8/9 tasks
for both PaLI-3 and PaLI-X, and is particularly effective on counting questions (TallyQA), compostional questions (GQA), and the
comprehensive benchmark (MMBench). Underline indicates when PaLI-3-VPD outperforms the Instruct version. * marks tasks
unseen during training. POPE and MMBench are zero-shot benchmarks for all models.


the same images and textual queries as our VPD variant.                  for creating instruction-tuning data which enables VLMs
Moreover, we also compare with the most recent SOTA                      to improve their visual reasoning ability.
vision-language models. These VLMs are initialized with                 Per-task fine-tuning (specialist). The results for the spe-
pre-trained visual encoders and LLMs, and then trained with             cialist models are shown in Table 2. PaLI-X-VPD sets a
image-text pairs, LLM-generated data, and academic tasks.               new SOTA on all benchmarks. Note how the specialist
                                                                        models tend to have higher scores than the generalist one.
4.2. Quantitative results                                               We propose several hypotheses for this performance gain:
Generalist model. Table 1 compares VPD with the base-                   (1) As shown in Table 2, the score gap tends to be larger on
lines discussed in §4.1. We infer all answers by open-ended             free-form VQA tasks. This may be due the fact that human
generation with the prompt “Answer with a single word or                annotations on these datasets have ambiguities. For example,
phrase.”, using greedy decoding without any constraint on               for the question “Who is looking up?”, GQA [26] labels
the model’s output space. For multiple-choice questions, we             are “man” or “woman” while OK-VQA [45] have more
run inference with the prompt “Answer with the option letter            detailed labels, for example, “worker” or “cook”. Per-task
from the given choices directly.” and generate the option let-          fine-tuning alleviates this annotation ambiguity and lets the
ter. As Table 1 shows, PaLI-X-VPD sets the new state-of-                model focus on the annotation style of that task. For multiple-
the-art on all benchmarks. Compared with prior generalist               choice and counting tasks, the answer has less ambiguity, and
VLMs, it achieves significant improvement on MMBench                    the score gaps are much smaller. (2) The performance gap
(+8.5), TallyQA complex (+9.8), and A-OKVQA(+9.5                        between PaLI-3 (5B) specialist and generalist is larger
compared with specialist SOTA[14]). PaLI-3-VPD, de-                     than that of PaLI-X. We hypothesize that this shows models
spite its small architecture size (5B), outperforms all prior           with larger scale has more multi-task capacity; (3) Per-task
models on VQAv2, TallyQA, POPE, and MMBench, in-                        fine-tuning adds more in-domain training data, which gener-
cluding much larger models that use Vicuna-13B as back-                 ally improves performance.
bones [7, 14, 38]. However, its performance on knowledge-
based VQA tasks does not outperform the prior SOTA. Our                               75                             76.6
                                                                                                                                    68.7    63.4 69.7
                                                                       Success Rate




hypothesis for this is that its language model (3B UL2) is                            50
                                                                                                    63.7      57.2
too small to contain all the necessary knowledge needed for                                  43.7                            47.0
correctly solving these tasks.                                                        25
    When compared to their Instruct variants, both                                     0
PaLI-3-VPD and PaLI-X-VPD outperform on 11/12                                                  GQA             OK-VQA       A-OKVQA MC       TallyQA
tasks. Specifically, for PaLI-X, VPD obtains a +1.6 im-                                                    Success@1                Success@5
provement on GQA (which is heavily focused on composi-
tional questions, spatial relationship, and localization), +1.2          Figure 4. Success rate of top-1 program and top-5 programs on the
on TallyQA for complex questions, and +1.2 on MMBench.                   training set during our data synthesis process.
These results suggest that VPD is a more effective method


                                                                   6
                                                             GQA          OK-VQA              A-OKVQA                      TallyQA
                  Specialist Models                                                  Multi-choice Direct Answer     Simple Complex
                                                            test-dev        val      val     test  val     test       test        test
                  InstructBLIP (Vicuna-7B) [14]                -           62.1      75.7   73.4    64.0    62.1       -         -
                  PaLI-3 (5B) [11]                             -           60.1       -      -       -       -        83.3      70.5
                  PaLI (17B) [9]                               -           64.5       -      -       -       -        81.7      70.9
                  CogVLM (17B) [63]                           65.2         64.7       -      -       -       -         -         -
                  PaLI-X (55B) [10]                            -           66.1       -      -       -       -        86.0      75.6
                  PaLI-3-VPD (5B) generalist                  61.3         57.5      78.5    -      56.5     -        83.1      70.9
                  PaLI-3-VPD (5B) specialist                  64.7         60.3      79.7   76.5    65.5    63.6      83.3      70.8
                  PaLI-X-VPD (55B) generalist                 64.9         64.6      84.5    -      62.7     -        86.2      76.6
                  PaLI-X-VPD (55B) specialist                 67.3         66.8      85.2   80.4    71.1    68.2      86.2      76.4

                Table 2. Comparison of per-task fine-tuning results of specialist models. PaLI-X-VPD sets a new SOTA for all the tasks.



           75                                        84.5          82.4           single candidate. As supported by the results in Figure 4,
                                                                                  this greatly improves the accuracy of our visual programs as
                        64.9          64.6                  64.2
Accuracy




           50                  50.2           50.7                                the teacher, thus making them more helpful for distillation.
                 41.1
           25                                                                     4.3. Human evaluation on rationales
            0
                    GQA         OK-VQA       A-OKVQA MC       TallyQA             In this section, we focus on the quality of model outputs. We
                               Program           PaLI-X-VPD                       performed this analysis using human annotators, who are
                                                                                  asked to evaluate both the correctness of the final answer
 Figure 5. Accuracy of visual programs and PaLI-X-VPD on                          and the quality of the rationale behind it.
 validation sets.
                                                                                  Models. We compare PaLI-X-VPD with PaLI-X
                                                                                  Instruct. Among possible baselines, we chose PaLI-X
Analysis: sampling multiple programs is key to good data                          Instruct because it is trained to generate long-form
generation. Fig. 4 shows the success rate of finding at least                     answers [65], which allows us to assess if it is the qual-
one program that passes the filtering stage, when the LLM                         ity of PaLI-X-VPD’s answers that the annotators prefer,
generates the top-1 or top-5 programs, respectively. There                        rather than its length. Since PaLI-X Instruct is also
is a dramatic increase in success rate from 1 program to 5:                       instruction-tuned, it can be prompted to provide long an-
+45% on GQA and A-OKVQA, +33% on OK-VQA, and                                      swers to alleviate this confounder.
+10% on TallyQA. This design choice greatly improves our
data synthesis efficiency, and, as a consequence, adding more                     Annotation protocol. We run inference with each of the two
CoT data that requires complex reasoning in our training                          models on a combination of 600 samples from GQA (test-
set. We also conduct an analysis in §4.2 to compare the                           dev), A-OKVQA (val), and TallyQA (Simple and Complex)
performance of VPD models with that of the visual programs                        and record their answers and rationales. We then ask 3 hu-
they are distilled from.                                                          man annotators to evaluate each model answer. We use prior
                                                                                  work from natural language processing (NLP) as inspiration,
 Analysis: comparison with visual programs Figure 5                               and build upon it for selecting the evaluation criteria [74].
 does a side-by-side comparison of the accuracy of visual                         Given an image and a query, for each model-generated ratio-
 programs and that of PaLI-X-VPD on GQA, OK-VQA,                                  nale, we ask human annotators to score the model answers
 A-OKVQA (multiple choice), and TallyQA (simple and                               along the following criteria: (1) correctness—is the final an-
 complex combined). We report results on the validation                           swer correct? (2) explainability—does the model explain its
 sets, so PaLI-X-VPD was not distilled with these exact                           rationale for reaching the final answer? (3) factuality—is ev-
 visual programs, but with visual programs generated in a                         ery step in the rationale factually correct (with respect to the
 similar manner on the training set. The results indicate that                    image and external knowledge)? (4) consistency—does step
 PaLI-X-VPD has much higher accuracy than visual pro-                             and final answer logically follow from the previous ones?
 grams on all tasks. This raises an interesting question: why                     Note that a rationale may have the wrong answer while being
 is the student model more accurate than its teacher? One                         consistent. We also conduct a side-by-side comparison, and
 explanation is that our pipeline allows us to leverage labeled                   ask annotators which of the two answers—the one provided
 data to improve the quality of the visual programs. When                         by PaLI-X-VPD or by PaLI-X Instruct—they prefer
 ground truth labels are available, we can choose a correct                       in terms of quality of the answer and explanation. More
 program among 5 candidates, rather than only relying on a                        details about the annotation protocol are in §C.


                                                                              7
                            100                                                                    100                                                                 100                    2




                                                                                                                                             each model is preferred
                                                                      Percent of correct samples
                                                                                                                                   98                                        6
                                         88                                                                                  88




                                                                                                                                                Percent of times
                                                                                                                87
       Percent of samples

                             80                                                                     80                                                                  80   27              40
                                                                                                         73
                                                                                                                                                                                                          PaLI-X-Instruct
                                   72
                             60                                                                     60                                                                  60                                PaLI-X-VPD
                                                                                                                                                                                                          Both
                             40                               46                                    40                                                                       46                           Neither
                                                                                                                                                                        40                   35

                             20                        22                                           20                                                                  20
                                                                                                                                                                             21              23
                              0                                                                      0                                                                   0
                                  correctness         explanability                                      factuality         consistency                                      All         When Correct
                                                (a)                                                                   (b)                                                          (c)

Figure 6. Human evaluation results assessing answer and rational quality for PaLI-X Instruct and PaLI-X VPD: (a) percentage of
answers that are correct and have explanations; (b) rationale factuality and consistency for the answers that contain an explanation; (c)
preference between the two models, when aggregating across all samples (“All”) and across those with correct answers (“When correct”).


Human evaluation results. The results of the evaluation are                                                                               Memes [29], a content moderation dataset where the task
first averaged among the human raters per sample, then ag-                                                                                is to classify if a meme contains hateful content. The tar-
gregated across samples. Our PaLI-X-VPD model far out-                                                                                    get labels are “yes” or “no”, and models are evaluated in
performs PaLI-X Instruct along all criteria. Fig. 6                                                                                       terms of classification accuracy and AUC-ROC. We experi-
(a) shows the correctness of the final answer provided by                                                                                 ment with two settings: supervised, in which the models are
each model (i.e. accuracy), and the proportion of the sam-                                                                                trained on the provided training set with 8, 500 labels, and
ples where the model provides a CoT rationale to explain                                                                                  unsupervised, in which no human labels are provided. We
its answer. PaLI-X-VPD’s gain in accuracy of +16.7%                                                                                       provide qualitative examples of the rationales our models
is even more impressive than in evaluations in §4.2 based                                                                                 give in Figure 7.
on benchmark labels—this is because human annotators are
better able to assess correctness for ambiguous questions                                                                                             Model                                             Acc     AUC-ROC
with different possible interpretations (e.g., the model’s an-                                                                                        Unsupervised / Zero-Shot Methods
swer “In the living room.” to the question “Where is the                                                                                              Generated Programs (ours)                         69.7        70.1
couch located?” was considered correct by annotators, even                                                                                            Supervised Methods
                                                                                                                                                      VisualBERT [35]                                   69.5        75.4
when the benchmark answer was “On the right.”). More-                                                                                                 Flamingo (80B) [2]                                 -          86.6
over, the explainability results confirm that our model is                                                                                            Previous SOTA [46]                                78.8        86.7
able to explain its own answer on +24% more samples than                                                                                              PaLI-X-VPD (label-only FT)                        77.6        88.0
the instruction tuned model. Additionally, Fig. 6 (b) shows                                                                                           PaLI-X-VPD (specialist w/ CoT)                    80.8        89.2
                                                                                                                                                      Human [29]                                        84.7        82.7
impressive rationale quality: among the samples where
an explanation is provided, PaLI-X-VPD’s rationales are                                                                                   Table 3. Results on Hateful Memes [29] seen test set. We improve
factual 87.2% of times, and consistent 97.8% of times, a                                                                                  SOTA for both zero-shot and supervised settings. Unsupervised
gain of +14.6% and +10%, respectively, when compared to                                                                                   PaLI-X-VPD outperforms strong supervised baselines.
PaLI-X Instruct.
    We also asked the annotators which of the two answers
given by the two models they prefer. We aggregated these                                                                                  5.1. Supervised setting
results in two ways: (1) across all samples, (2) across the
                                                                                                                                          We first experiment with the supervised setting. We fine-tune
samples where both models answered the question correctly.
                                                                                                                                          the models on 8,500 labels in two ways:
The results in Fig. 6 (c) show that PaLI-X-VPD is preferred
on 25% more samples than PaLI-X Instruct in the “All”                                                                                     1. Label-only fine-tuning: To establish a strong baseline,
case, and on 12% more samples when both are correct. This                                                                                    we first experiment with the traditional supervised setting,
suggests that even when PaLI-X-VPD makes mistakes, it                                                                                        where we fine-tune the model to output “yes” or “no”.
still provides a better answer. Such examples are shown in                                                                                2. PaLI-X-VPD (specialist): We use the complete VPD
§C. These results confirm that a model fine-tuned with VPD                                                                                   pipeline to train this model. We select an execution trace
leads to more faithful and consistent answers.                                                                                               that leads to the correct label, and use it to tune our VLM.

5. Experiments on content moderation                                                                                                      Results. Our PaLI-X-VPD (specialist) sets a new
                                                                                                                                          SOTA for this task, with an accuracy of 80.8% and
Prior experiments focus on training generalist VLMs. Here,                                                                                AUC-ROC of 89.2%. It outperforms the label-only fine-
we explore the effectiveness of VPD at quickly adapting                                                                                   tuning baseline and significantly improves the SOTA met-
models to real-world applications from a different domain                                                                                 rics, achieving nearly human-level accuracy, and super-
than the training data [e.g., 56]. We experiment on Hateful                                                                               human AUC-ROC.


                                                                                                                                  8
5.2. Unsupervised setting                                              list the limitations below, along with future work that may
                                                                       address these challenges.
How would VPD perform if we do not have any human-
annotated labels? We experiment with three methods:                    Scaling-up VPD with LLM-generated questions and bet-
1. Generated Program: The program generated by PaLM-                   ter filtering strategies. Our current setting limits the data
   2 [3] for solving this task consists of following main steps:       source of VPD to existing VQA tasks. Future work can scale-
   (1) get image description with PaLI-X [10]; (2) use an              up and diversify the tasks using LLMs, as demonstrated in
   OCR tool to extract embedded texts; (3) given the image             Self-Instruct [64]. One challenge is that there lacks human-
   description and OCR texts, ask PaLM-2 to explain if this            annotated labels for LLM-generated tasks. Experiments in
   meme is hateful.                                                    §5 show that VPD works well even without labels. Neverthe-
2. PaLI-X-VPD (generalist): In a zero-shot setting, we di-             less, it would be better if we have some filtering strategies,
   rectly prompt our PaLI-X-VPD(generalist) with:                      as shown in §4.2. Since even the strongest VLMs like PaLI-
  “The text is <OCR text>. Is this a hateful meme?” We com-            X [10] and GPT-4V [49] cannot give reliable answers, fact-
   pute the probability of PaLI-X-VPD generating “yes”                 checking strategies for multimodal chain-of-thought data is
   or “no” and measure accuracy and AUC-ROC.                           a promising future direction.
3. PaLI-X-VPD (specialist with zero-shot CoT): We follow               Agents, rather than static programs. There exist complex
   our VPD pipeline and convert the execution traces of the            visual-language tasks that cannot be easily solved with one
   program into CoTs, and then fine-tune PaLI-X-VPD                    program. Recent work [67, 71, 72] have explored the idea
   to output these CoTs. Since no groundtruth labels are               of LLM agents, where LLMs interact with an environment
   available, no filtering is done during the process.                 and do planning interactively. We may be able to leverage
VPD significantly improves performance even when no                    this idea in our scenario, and have an LLM update its plans
labels are available. As shown in Table 3, PaLI-X-VPD                  given the new information gathered from vision tools.
(generalist) outperforms all other VLMs (61.4%). In-                   Adding fine-grained and dense labeling tools. We find that
terestingly, the generated programs themselves get much                programs struggles in complex scenarios when objects are
higher accuracy (69.7%) than on the previous datasets,                 occluded, or the scene contains too many objects. Adding
perhaps because PaLM-2 is better suited at analyzing a                 dense-labeling tools like Segment Anything [31] may ad-
meme than typical VQA datasets. As shown in Figure 7,                  dress this challenge. For example, recently LISA [33] have
PaLI-X-VPD (generalist) is relatively insensitive                      proposed combining segmentation with LLMs. Future work
to hateful content, while programs are better. Moreover,               can make dense labeling tools available in VPD in a similar
our PaLI-X-VPD (specialist) sets a new zero-shot                       way, which will further boost VLM performance.
SOTA on Hateful Memes, and even outperforms supervised
VisualBERT [35]. To understand this impressive gain, we                7. Conclusion
manually inspect the model outputs and find that the model
has learnt PaLM-2’s reasoning process via VPD, as seen in              We introduce VPD, a framework for distilling the reasoning
Figure 7. Besides, our model has better understanding of               abilities of LLMs along with the capabilities of vision tools
the image. As seen in Figure 7 (a), the program, despite               into VLMs. VPD synthesizes training data for VLMs by
giving the correct answer, has not mentioned anything about            generating programs that can leverage external tools. We use
“black people”, because it is not covered in the image cap-            this technique to fine-tune some of the best existing VLMs
tion. In comparison, our PaLI-X-VPD (specialist)                       (PaLI-3 and PaLI-X) and established new SOTA results on
includes it and gives a better explanation.                            8 classical VQA and 2 zero-shot multimodal benchmarks.
                                                                       According to human evaluations, VPD-tuned models provide
More qualitative analysis. We observe that PaLI-X-VPD                  more accurate answers and better rationales. Experiments on
(supervised specialist) is able to capture the nuances in the          the Hateful Memes show how VPD can also adapt models
meme, while unsupervised methods fail, as shown in Figure 7            to new real-world domains, even when no labeled data is
(c). Also, there are some failure cases like (d), in which even        available, also establishing new SOTAs. We also point out
our supervised model fails while the program succeeds on               directions to further improve VPD. We believe VPD will
hateful content detection.                                             grant future VLMs better multimodal reasoning abilities.

6. Limitations and Future Directions                                   8. Acknowledgements
We mainly identify two directions for improvement. First,              We thank Tanmaya Dabral, Jialin Wu, Radu Soricut, Aditya
VPD can be further scaled-up with more diverse tasks. Sec-             Avinash, Howard Zhou, Jiao Sun, Deqing Fu, Cyrus
ond, we find that there are some problems that our visual              Rashtchian, Andrew Tomkins, Tom Duerig, as well as the
program framework (ViperGPT [16]) cannot solve. Further                Agile Modeling team for helpful project discussions and
improving the programs will yield bigger gains for VPD. We             technical support in this project.


                                                                   9
                    (a)                                                                        (b)




                  PaLI-X-VPD (generalist):                                                    PaLI-X-VPD (generalist):
                  No, this is not a hateful meme. The meme is simply a joke
                  about the fact that black people are consistently treated worse             No, this is not a hateful meme. The meme is about thinking
                                                                                              before you act, which is a positive message.
                  than white people.


                 Program:                                                                    Program:

                  This meme is hateful because it stereotypes an entire group of
                  people as being criminals. It is also harmful because it                    The meme is not hateful because it is not targeting a specific
                  suggests that people who are treated poorly by society                      group of people. It is simply giving advice on how to be treated
                  deserve it because they are criminals.                                      better.


                 PaLI-X-VPD (specialist w/ zero-shot CoTs):                                  PaLI-X-VPD (specialist w/ zero-shot CoTs):

                  The meme is hateful because it suggests that black people are
                  consistently sources of crime. This is a harmful stereotype that            The meme is not hateful. It is a positive message about
                  can lead to discrimination and violence against black people.               thinking before you act.


                 PaLI-X-VPD (supervised specialist):                                         PaLI-X-VPD (supervised specialist):

                  This meme is hateful because it stereotypes black people as
                  criminals. It suggests that black people are not worthy of being            This meme is not hateful because it is not targeting a specific
                  treated well because they are criminals. This is a harmful                  group of people. It is simply suggesting that people should
                  stereotype that can lead to discrimination against black people.            think before they act.



                      (c)                                                                      (d)




                  PaLI-X-VPD (generalist):                                                    PaLI-X-VPD (generalist):

                   No, this is not a hateful meme. The meme is about a woman
                                                                                              No, this is not a hateful meme. It is a funny meme about
                   who is in a wheelchair and her husband is always pushing her
                                                                                              Thanksgiving in China.
                   around and talking behind her back.

                  Program:                                                                   Program:

                   This meme is about a husband pushing his wife around in a                  This is a hateful meme because it is making a joke about the
                   wheelchair. The meme is not hateful because it is not making               stereotype that Chinese people eat cats. This stereotype is
                   fun of the wife or the husband.                                            harmful because it dehumanizes Chinese people and makes
                                                                                              them seem like they are barbaric and uncivilized.


                  PaLI-X-VPD (specialist w/ zero-shot CoTs):                                 PaLI-X-VPD (specialist w/ zero-shot CoTs):

                   The meme is not hateful because it is not targeting a specific
                                                                                              The meme is not hateful because it does not contain any
                   group of people. It is simply making a joke about a couple's
                                                                                              hateful language or imagery.
                   relationship.

                  PaLI-X-VPD (supervised specialist):                                        PaLI-X-VPD (supervised specialist):

                                                                                              The meme is not hateful because it is not making fun of any
                    This meme is hateful because it is making fun of a woman who
                                                                                              particular group of people. It is simply a joke about the fact that
                    is in a wheelchair. It is also making light of domestic violence.
                                                                                              Thanksgiving is not celebrated in China.



Figure 7. Example outputs of different methods on Hateful Memes [29] dev set. Here we prompt our PaLI-X-VPD models with “Is this
a hateful meme? Explain the rationale to answer the question.” to get models’ long-form rationales. The unsupervised methods include
zero-shot PaLI-X-VPD (generalist), our generated program, and PaLI-X-VPD (specialist with zero-shot CoTs). We also include
our supervised method, i.e., PaLI-X-VPD (specialist). We mark whether their outputs match the gold answers.




                                                                                        10
References                                                                 [6] Jun Chen, Deyao Zhu, Xiaoqian Shen, Xiang Li, Zechun
                                                                               Liu, Pengchuan Zhang, Raghuraman Krishnamoorthi, Vikas
[1] Manoj Acharya, Kushal Kafle, and Christopher Kanan. Tal-                   Chandra, Yunyang Xiong, and Mohamed Elhoseiny. Minigpt-
    lyqa: Answering complex counting questions. In Proceedings                 v2: large language model as a unified interface for vision-
    of the AAAI conference on artificial intelligence, pages 8076–             language multi-task learning, 2023. 3
    8084, 2019. 1, 5, 16, 17
                                                                           [7] Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng
[2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine                  Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s
    Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Men-                     referential dialogue magic, 2023. 1, 2, 3, 6
    sch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza
                                                                           [8] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W.
    Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina
                                                                               Cohen. Program of thoughts prompting: Disentangling com-
    Samangooei, Marianne Monteiro, Jacob Menick, Sebastian
                                                                               putation from reasoning for numerical reasoning tasks, 2022.
    Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Shar-
                                                                               1, 3
    ifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals,
    Andrew Zisserman, and Karen Simonyan. Flamingo: a visual               [9] Xi Chen, Xiao Wang, Soravit Changpinyo, AJ Piergiovanni,
    language model for few-shot learning, 2022. 1, 3, 6, 8                     Piotr Padlewski, Daniel Salz, Sebastian Goodman, Adam
[3] Rohan Anil, Andrew M. Dai, Orhan Firat, Melvin John-                       Grycner, Basil Mustafa, Lucas Beyer, Alexander Kolesnikov,
    son, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri,                    Joan Puigcerver, Nan Ding, Keran Rong, Hassan Akbari,
    Emanuel Taropa, Paige Bailey, Zhifeng Chen, Eric Chu,                      Gaurav Mishra, Linting Xue, Ashish Thapliyal, James Brad-
    Jonathan H. Clark, Laurent El Shafey, Yanping Huang,                       bury, Weicheng Kuo, Mojtaba Seyedhosseini, Chao Jia,
    Kathy Meier-Hellstern, Gaurav Mishra, Erica Moreira, Mark                  Burcu Karagol Ayan, Carlos Riquelme, Andreas Steiner,
    Omernick, Kevin Robinson, Sebastian Ruder, Yi Tay, Ke-                     Anelia Angelova, Xiaohua Zhai, Neil Houlsby, and Radu
    fan Xiao, Yuanzhong Xu, Yujing Zhang, Gustavo Hernan-                      Soricut. Pali: A jointly-scaled multilingual language-image
    dez Abrego, Junwhan Ahn, Jacob Austin, Paul Barham, Jan                    model, 2022. 1, 3, 7
    Botha, James Bradbury, Siddhartha Brahma, Kevin Brooks,               [10] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, So-
    Michele Catasta, Yong Cheng, Colin Cherry, Christopher A.                  ravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian
    Choquette-Choo, Aakanksha Chowdhery, Clément Crepy,                        Goodman, Xiao Wang, Yi Tay, Siamak Shakeri, Mostafa De-
    Shachi Dave, Mostafa Dehghani, Sunipa Dev, Jacob Devlin,                   hghani, Daniel Salz, Mario Lucic, Michael Tschannen, Arsha
    Mark Díaz, Nan Du, Ethan Dyer, Vlad Feinberg, Fangxiaoyu                   Nagrani, Hexiang Hu, Mandar Joshi, Bo Pang, Ceslee Mont-
    Feng, Vlad Fienber, Markus Freitag, Xavier Garcia, Sebas-                  gomery, Paulina Pietrzyk, Marvin Ritter, AJ Piergiovanni,
    tian Gehrmann, Lucas Gonzalez, Guy Gur-Ari, Steven Hand,                   Matthias Minderer, Filip Pavetic, Austin Waters, Gang Li,
    Hadi Hashemi, Le Hou, Joshua Howland, Andrea Hu, Jef-                      Ibrahim Alabdulmohsin, Lucas Beyer, Julien Amelot, Kenton
    frey Hui, Jeremy Hurwitz, Michael Isard, Abe Ittycheriah,                  Lee, Andreas Peter Steiner, Yang Li, Daniel Keysers, Anurag
    Matthew Jagielski, Wenhao Jia, Kathleen Kenealy, Maxim                     Arnab, Yuanzhong Xu, Keran Rong, Alexander Kolesnikov,
    Krikun, Sneha Kudugunta, Chang Lan, Katherine Lee, Ben-                    Mojtaba Seyedhosseini, Anelia Angelova, Xiaohua Zhai, Neil
    jamin Lee, Eric Li, Music Li, Wei Li, YaGuang Li, Jian                     Houlsby, and Radu Soricut. Pali-x: On scaling up a multilin-
    Li, Hyeontaek Lim, Hanzhao Lin, Zhongtao Liu, Frederick                    gual vision and language model, 2023. 2, 3, 4, 5, 7, 9, 17,
    Liu, Marcello Maggioni, Aroma Mahendru, Joshua Maynez,                     18
    Vedant Misra, Maysam Moussalem, Zachary Nado, John                    [11] Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov,
    Nham, Eric Ni, Andrew Nystrom, Alicia Parrish, Marie Pel-                  Jialin Wu, Paul Voigtlaender, Basil Mustafa, Sebastian Good-
    lat, Martin Polacek, Alex Polozov, Reiner Pope, Siyuan Qiao,               man, Ibrahim Alabdulmohsin, Piotr Padlewski, Daniel Salz,
    Emily Reif, Bryan Richter, Parker Riley, Alex Castro Ros,                  Xi Xiong, Daniel Vlasic, Filip Pavetic, Keran Rong, Tianli
    Aurko Roy, Brennan Saeta, Rajkumar Samuel, Renee Shelby,                   Yu, Daniel Keysers, Xiaohua Zhai, and Radu Soricut. Pali-3
    Ambrose Slone, Daniel Smilkov, David R. So, Daniel Sohn,                   vision language models: Smaller, faster, stronger, 2023. 1, 4,
    Simon Tokumine, Dasha Valter, Vijay Vasudevan, Kiran Vo-                   5, 7, 17, 18
    drahalli, Xuezhi Wang, Pidong Wang, Zirui Wang, Tao Wang,             [12] Zhoujun Cheng, Tianbao Xie, Peng Shi, Chengzu Li, Rahul
    John Wieting, Yuhuai Wu, Kelvin Xu, Yunhan Xu, Linting                     Nadkarni, Yushi Hu, Caiming Xiong, Dragomir Radev, Mari
    Xue, Pengcheng Yin, Jiahui Yu, Qiao Zhang, Steven Zheng,                   Ostendorf, Luke Zettlemoyer, et al. Binding language models
    Ce Zheng, Weikang Zhou, Denny Zhou, Slav Petrov, and                       in symbolic languages. arXiv preprint arXiv:2210.02875,
    Yonghui Wu. Palm 2 technical report, 2023. 1, 3, 4, 9, 15                  2022. 3
[4] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan               [13] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
    Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren                       Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham,
    Zhou. Qwen-vl: A versatile vision-language model for under-                Hyung Won Chung, Charles Sutton, Sebastian Gehrmann,
    standing, localization, text reading, and beyond, 2023. 1, 3,              Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua
    6                                                                          Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam
[5] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Sub-                         Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben
    biah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan,               Hutchinson, Reiner Pope, James Bradbury, Jacob Austin,
    Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language                Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke,
    models are few-shot learners. Advances in neural information               Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk
    processing systems, 33:1877–1901, 2020. 3                                  Michalewski, Xavier Garcia, Vedant Misra, Kevin Robin-


                                                                     11
     son, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan,                 Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen.
     Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan                    Lora: Low-rank adaptation of large language models, 2021.
     Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, An-                 5, 18
     drew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie              [23] Yushi* Hu, Hang* Hua, Zhengyuan Yang, Weijia Shi, Noah A
     Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Olek-                Smith, and Jiebo Luo. Promptcap: Prompt-guided task-aware
     sandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang,                  image captioning. arXiv preprint arXiv:2211.09699, 2022. 2,
     Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta,                   3, 4
     Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean,            [24] Yushi Hu, Chia-Hsuan Lee, Tianbao Xie, Tao Yu, Noah A.
     Slav Petrov, and Noah Fiedel. Palm: Scaling language model-               Smith, and Mari Ostendorf. In-context learning for few-shot
     ing with pathways, 2022. 3                                                dialogue state tracking. In Findings of the Association for
[14] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat                     Computational Linguistics: EMNLP 2022, pages 2627–2643,
     Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung,                Abu Dhabi, United Arab Emirates, 2022. Association for
     and Steven Hoi. Instructblip: Towards general-purpose vision-             Computational Linguistics. 4
     language models with instruction tuning, 2023. 2, 6, 7               [25] Ziniu Hu, Ahmet Iscen, Chen Sun, Kai-Wei Chang, Yizhou
[15] Mostafa Dehghani, Josip Djolonga, Basil Mustafa, Piotr                    Sun, David A Ross, Cordelia Schmid, and Alireza Fathi. Avis:
     Padlewski, Jonathan Heek, Justin Gilmer, Andreas Steiner,                 Autonomous visual information seeking with large language
     Mathilde Caron, Robert Geirhos, Ibrahim Alabdulmohsin,                    model agent, 2023. 1, 3
     Rodolphe Jenatton, Lucas Beyer, Michael Tschannen, Anurag            [26] Drew A Hudson and Christopher D Manning. Gqa: A new
     Arnab, Xiao Wang, Carlos Riquelme, Matthias Minderer,                     dataset for real-world visual reasoning and compositional
     Joan Puigcerver, Utku Evci, Manoj Kumar, Sjoerd van                       question answering. In Proceedings of the IEEE/CVF con-
     Steenkiste, Gamaleldin F. Elsayed, Aravindh Mahendran,                    ference on computer vision and pattern recognition, pages
     Fisher Yu, Avital Oliver, Fantine Huot, Jasmijn Bastings,                 6700–6709, 2019. 1, 5, 6, 16, 17
     Mark Patrick Collier, Alexey Gritsenko, Vighnesh Birodkar,           [27] Norman P. Jouppi, Cliff Young, Nishant Patil, David Patter-
     Cristina Vasconcelos, Yi Tay, Thomas Mensink, Alexander                   son, Gaurav Agrawal, Raminder Bajwa, Sarah Bates, Suresh
     Kolesnikov, Filip Pavetić, Dustin Tran, Thomas Kipf, Mario               Bhatia, Nan Boden, Al Borchers, Rick Boyle, Pierre-luc
     Lučić, Xiaohua Zhai, Daniel Keysers, Jeremiah Harmsen,                  Cantin, Clifford Chao, Chris Clark, Jeremy Coriell, Mike
     and Neil Houlsby. Scaling vision transformers to 22 billion               Daley, Matt Dau, Jeffrey Dean, Ben Gelb, Tara Vazir Ghaem-
     parameters, 2023. 17                                                      maghami, Rajendra Gottipati, William Gulland, Robert Hag-
[16] Surís Dídac, Sachit Menon, and Carl Vondrick. Vipergpt:                   mann, C. Richard Ho, Doug Hogberg, John Hu, Robert
     Visual inference via python execution for reasoning. arXiv                Hundt, Dan Hurt, Julian Ibarz, Aaron Jaffey, Alek Ja-
     preprint arXiv:2303.08128, 2023. 1, 2, 3, 9, 20                           worski, Alexander Kaplan, Harshit Khaitan, Daniel Kille-
[17] Ruofei Du, Eric Turner, Maksym Dzitsiuk, Luca Prasso, Ivo                 brew, Andy Koch, Naveen Kumar, Steve Lacy, James Laudon,
     Duarte, Jason Dourgarian, Joao Afonso, Jose Pascoal, Josh                 James Law, Diemthu Le, Chris Leary, Zhuyuan Liu, Kyle
     Gladstone, Nuno Cruces, Shahram Izadi, Adarsh Kowdle,                     Lucke, Alan Lundin, Gordon MacKean, Adriana Mag-
     Konstantine Tsotsos, and David Kim. DepthLab: Real-Time                   giore, Maire Mahony, Kieran Miller, Rahul Nagarajan, Ravi
     3D Interaction With Depth Maps for Mobile Augmented Re-                   Narayanaswami, Ray Ni, Kathy Nix, Thomas Norrie, Mark
     ality. In Proceedings of the 33rd Annual ACM Symposium on                 Omernick, Narayana Penukonda, Andy Phelps, Jonathan
     User Interface Software and Technology. ACM, 2020. 4                      Ross, Matt Ross, Amir Salek, Emad Samadiani, Chris Sev-
[18] Weixi Feng, Wanrong Zhu, Tsu-Jui Fu, Varun Jampani, Ar-                   ern, Gregory Sizikov, Matthew Snelham, Jed Souter, Dan
     jun Reddy Akula, Xuehai He, Sugato Basu, Xin Eric Wang,                   Steinberg, Andy Swing, Mercedes Tan, Gregory Thorson, Bo
     and William Yang Wang. Layoutgpt: Compositional visual                    Tian, Horia Toma, Erick Tuttle, Vijay Vasudevan, Richard
     planning and generation with large language models. ArXiv,                Walter, Walter Wang, Eric Wilcox, and Doe Hyun Yoon. In-
     abs/2305.15393, 2023. 2                                                   datacenter performance analysis of a tensor processing unit.
[19] Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Ba-                   In Proceedings of the 44th Annual International Symposium
     tra, and Devi Parikh. Making the V in VQA matter: Ele-                    on Computer Architecture. ACM, 2017. 18
     vating the role of image understanding in Visual Question            [28] Ehsan Kamalloo, Nouha Dziri, Charles L. A. Clarke, and
     Answering. In Conference on Computer Vision and Pattern                   Davood Rafiei. Evaluating open-domain question answering
     Recognition (CVPR), 2017. 5, 17                                           in the era of large language models, 2023. 4, 23
[20] Tanmay Gupta and Aniruddha Kembhavi. Visual program-                 [29] Douwe Kiela, Hamed Firooz, Aravind Mohan, Vedanuj
     ming: Compositional visual reasoning without training. 2023               Goswami, Amanpreet Singh, Pratik Ringshia, and Davide
     IEEE/CVF Conference on Computer Vision and Pattern                        Testuggine. The Hateful Memes Challenge: Detecting Hate
     Recognition (CVPR), 2023. 1, 2, 3                                         Speech in Multimodal Memes, 2020. 2, 8, 10
[21] Cheng-Yu Hsieh, Chun-Liang Li, Chih-Kuan Yeh, Hootan                 [30] Diederik P. Kingma and Jimmy Ba. Adam: A method for
     Nakhost, Yasuhisa Fujii, Alexander Ratner, Ranjay Krishna,                stochastic optimization. CoRR, abs/1412.6980, 2015. 18
     Chen-Yu Lee, and Tomas Pfister. Distilling step-by-step!             [31] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao,
     outperforming larger language models with less training data              Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer White-
     and smaller model sizes, 2023. 2, 3, 4                                    head, Alexander C. Berg, Wan-Yen Lo, Piotr Dollár, and Ross
[22] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-                  Girshick. Segment anything, 2023. 9


                                                                     12
[32] Ranjay Krishna, Yuke Zhu, Oliver Groth, Justin Johnson,              [47] Matthias Minderer, Alexey Gritsenko, and Neil Houlsby. Scal-
     Kenji Hata, Joshua Kravitz, Stephanie Chen, Yannis Kalan-                 ing open-vocabulary object detection, 2023. 4
     tidis, Li-Jia Li, David A. Shamma, Michael S. Bernstein, and         [48] Anand Mishra, Shashank Shekhar, Ajeet Kumar Singh, and
     Fei-Fei Li. Visual genome: Connecting language and vision                 Anirban Chakraborty. Ocr-vqa: Visual question answering by
     using crowdsourced dense image annotations, 2016. 3, 5, 17                reading text in images. In ICDAR, 2019. 5, 17
[33] Xin Lai, Zhuotao Tian, Yukang Chen, Yanwei Li, Yuhui Yuan,           [49] OpenAI. Gpt-4 technical report, 2023. 1, 3, 9
     Shu Liu, and Jiaya Jia. Lisa: Reasoning segmentation via             [50] Zhiliang Peng, Wenhui Wang, Li Dong, Yaru Hao, Shaohan
     large language model, 2023. 9                                             Huang, Shuming Ma, and Furu Wei. Kosmos-2: Grounding
[34] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi.                    multimodal large language models to the world, 2023. 3
     Blip-2: Bootstrapping language-image pre-training with               [51] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta
     frozen image encoders and large language models. ArXiv,                   Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda,
     abs/2301.12597, 2023. 1, 3                                                and Thomas Scialom. Toolformer: Language models can
[35] Liunian Harold Li, Mark Yatskar, Da Yin, Cho-Jui Hsieh,                   teach themselves to use tools, 2023. 3
     and Kai-Wei Chang. VisualBERT: A Simple and Performant               [52] Dustin Schwenk, Apoorv Khandelwal, Christopher Clark,
     Baseline for Vision and Language. ArXiv, abs/1908.03557,                  Kenneth Marino, and Roozbeh Mottaghi. A-okvqa: A bench-
     2019. 8, 9                                                                mark for visual question answering using world knowledge,
[36] Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin                     2022. 5, 16, 17
     Zhao, and Ji-Rong Wen. Evaluating object hallucination in            [53] Dustin Schwenk, Apoorv Khandelwal, Christopher Clark,
     large vision-language models, 2023. 5, 17                                 Kenneth Marino, and Roozbeh Mottaghi. A-okvqa: A bench-
[37] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays,                  mark for visual question answering using world knowledge.
     Pietro Perona, Deva Ramanan, Piotr Dollár, and C Lawrence                 arXiv preprint arXiv:2206.01718, 2022. 1
     Zitnick. Microsoft coco: Common objects in context. In               [54] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weim-
     European conference on computer vision, pages 740–755.                    ing Lu, and Yueting Zhuang. Hugginggpt: Solving ai tasks
     Springer, 2014. 3                                                         with chatgpt and its friends in hugging face, 2023. 3
[38] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee.               [55] Amanpreet Singh, Vivek Natarjan, Meet Shah, Yu Jiang, Xin-
     Improved baselines with visual instruction tuning, 2023. 2, 6             lei Chen, Devi Parikh, and Marcus Rohrbach. Towards vqa
[39] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.                  models that can read. In Proceedings of the IEEE Confer-
     Visual instruction tuning. arXiv preprint arXiv:2304.08485,               ence on Computer Vision and Pattern Recognition, pages
     2023. 1, 2, 3, 4                                                          8317–8326, 2019. 5, 17
[40] Yuan Liu, Haodong Duan, Yuanhan Zhang, Bo Li, Songyang               [56] Otilia Stretcu, Edward Vendrow, Kenji Hata, Krishnamurthy
     Zhang, Wangbo Zhao, Yike Yuan, Jiaqi Wang, Conghui He,                    Viswanathan, Vittorio Ferrari, Sasan Tavakkol, Wenlei Zhou,
     Ziwei Liu, Kai Chen, and Dahua Lin. Mmbench: Is your                      Aditya Avinash, Emming Luo, Neil Gordon Alldrin, et al.
     multi-modal model an all-around player?, 2023. 2, 5, 17                   Agile modeling: From concept to classifier in minutes. In
[41] Jiasen Lu, Christopher Clark, Rowan Zellers, Roozbeh Mot-                 Proceedings of the IEEE/CVF International Conference on
     taghi, and Aniruddha Kembhavi. Unified-io: A unified                      Computer Vision, pages 22323–22334, 2023. 8
     model for vision, language, and multi-modal tasks. ArXiv,            [57] Sanjay Subramanian, Medhini Narasimhan, Kushal
     abs/2206.08916, 2022. 1, 3                                                Khangaonkar, Kevin Yang, Arsha Nagrani, Cordelia Schmid,
[42] Pan Lu, Baolin Peng, Hao Cheng, Michel Galley, Kai-Wei                    Andy Zeng, Trevor Darrell, and Dan Klein. Modular visual
     Chang, Ying Nian Wu, Song-Chun Zhu, and Jianfeng Gao.                     question answering via code generation, 2023. 1
     Chameleon: Plug-and-play compositional reasoning with                [58] Yi Tay, Mostafa Dehghani, Vinh Q. Tran, Xavier Garcia, Ja-
     large language models, 2023. 3                                            son Wei, Xuezhi Wang, Hyung Won Chung, Siamak Shakeri,
[43] Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang, Delip                    Dara Bahri, Tal Schuster, Huaixiu Steven Zheng, Denny Zhou,
     Rao, Eric Wong, Marianna Apidianaki, and Chris Callison-                  Neil Houlsby, and Donald Metzler. UL2: Unifying Language
     Burch. Faithful chain-of-thought reasoning, 2023. 1, 3                    Learning Paradigms, 2022. 17
[44] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and                 [59] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Am-
     Roozbeh Mottaghi. Ok-vqa: A visual question answering                     jad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya
     benchmark requiring external knowledge. In Proceedings                    Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas
     of the IEEE/cvf conference on computer vision and pattern                 Blecher, Cristian Canton Ferrer, Moya Chen, Guillem Cu-
     recognition, pages 3195–3204, 2019. 1                                     curull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin
[45] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and                      Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman
     Roozbeh Mottaghi. Ok-vqa: A visual question answering                     Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan
     benchmark requiring external knowledge. 2019 IEEE/CVF                     Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Is-
     Conference on Computer Vision and Pattern Recognition                     abel Kloumann, Artem Korenev, Punit Singh Koura, Marie-
     (CVPR), 2019. 5, 6, 17                                                    Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich,
[46] Jingbiao Mei, Jinghong Chen, Weizhe Lin, Bill Byrne,                      Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov,
     and Marcus Tomalin. Improving hateful memes detection                     Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton,
     via learning hatefulness-aware embedding space through                    Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schel-
     retrieval-guided contrastive learning, 2023. 8                            ten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian,


                                                                     13
     Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams,                   Zeng, and Lijuan Wang. Mm-react: Prompting chatgpt for
     Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen                    multimodal reasoning and action, 2023. 3, 9
     Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Au-                  [72] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran,
     relien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas                   Karthik Narasimhan, and Yuan Cao. React: Synergizing
     Scialom. Llama 2: Open foundation and fine-tuned chat mod-                    reasoning and acting in language models. arXiv preprint
     els, 2023. 3                                                                  arXiv:2210.03629, 2022. 9
[60] Jianfeng Wang, Zhengyuan Yang, Xiaowei Hu, Linjie Li,                    [73] Qinghao Ye, Haiyang Xu, Jiabo Ye, Ming Yan, Haowei Liu,
     Kevin Lin, Zhe Gan, Zicheng Liu, Ce Liu, and Lijuan Wang.                     Qi Qian, Ji Zhang, Fei Huang, and Jingren Zhou. mplug-
     Git: A generative image-to-text transformer for vision and                    owl2: Revolutionizing multi-modal large language model
     language. arXiv preprint arXiv:2205.14100, 2022. 1, 3                         with modality collaboration, 2023. 1, 3, 6
[61] Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai,                     [74] Xi Ye and Greg Durrett. The unreliability of explanations
     Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and                         in few-shot prompting for textual reasoning. In Advances in
     Hongxia Yang. Ofa: Unifying architectures, tasks, and modal-                  Neural Information Processing Systems, pages 30378–30392.
     ities through a simple sequence-to-sequence learning frame-                   Curran Associates, Inc., 2022. 7
     work. CoRR, abs/2202.03052, 2022. 3                                      [75] Xiang Yue, Xingwei Qu, Ge Zhang, Yao Fu, Wenhao Huang,
[62] Peifeng Wang, Zhengyang Wang, Zheng Li, Yifan Gao, Bing                       Huan Sun, Yu Su, and Wenhu Chen. Mammoth: Building
     Yin, and Xiang Ren. Scott: Self-consistent chain-of-thought                   math generalist models through hybrid instruction tuning.
     distillation, 2023. 3                                                         arXiv preprint arXiv:2309.05653, 2023. 3
[63] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji                     [76] Andy Zeng, Adrian Wong, Stefan Welker, Krzysztof Choro-
     Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan                        manski, Federico Tombari, Aveek Purohit, Michael Ryoo,
     Song, Jiazheng Xu, Bin Xu, Juanzi Li, Yuxiao Dong, Ming                       Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke, et al. So-
     Ding, and Jie Tang. Cogvlm: Visual expert for pretrained                      cratic models: Composing zero-shot multimodal reasoning
     language models, 2023. 1, 3, 7                                                with language. arXiv preprint arXiv:2204.00598, 2022. 3
[64] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu,                  [77] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and
     Noah A. Smith, Daniel Khashabi, and Hannaneh Hajishirzi.                      Lucas Beyer. Sigmoid loss for language image pre-training,
     Self-instruct: Aligning language models with self-generated                   2023. 17
     instructions, 2022. 5, 9                                                 [78] Haotian Zhang, Pengchuan Zhang, Xiaowei Hu, Yen-Chun
[65] Yaqing Wang, Jialin Wu, Tanmaya Dabral, Jiageng Zhang,                        Chen, Liunian Harold Li, Xiyang Dai, Lijuan Wang, Lu Yuan,
     Geoff Brown, Chun-Ta Lu, Frederick Liu, Yi Liang, Bo Pang,                    Jenq-Neng Hwang, and Jianfeng Gao. Glipv2: Unifying
     Michael Bendersky, and Radu Soricut. Non-intrusive adapta-                    localization and vision-language understanding, 2022. 3
     tion: Input-centric parameter-efficient fine-tuning for versatile        [79] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mo-
     multimodal modeling, 2023. 2, 5, 7                                            hamed Elhoseiny. Minigpt-4: Enhancing vision-language
                                                                                   understanding with advanced large language models, 2023. 1,
[66] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma,
                                                                                   3, 6
     Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou.
     Chain-of-thought prompting elicits reasoning in large lan-               [80] Xuekai Zhu, Biqing Qi, Kaiyan Zhang, Xingwei Long, and
     guage models, 2022. 3                                                         Bowen Zhou. Pad: Program-aided distillation specializes
                                                                                   large models in reasoning, 2023. 3
[67] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin
     Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang,
     Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug
     Burger, and Chi Wang. Autogen: Enabling next-gen llm
     applications via multi-agent conversation. 2023. 9
[68] Yiheng Xu, Hongjin Su, Chen Xing, Boyu Mi, Qian Liu,
     Weijia Shi, Binyuan Hui, Fan Zhou, Yitao Liu, Tianbao Xie,
     Zhoujun Cheng, Siheng Zhao, Lingpeng Kong, Bailin Wang,
     Caiming Xiong, and Tao Yu. Lemur: Harmonizing natural
     language and code for language agents, 2023. 1
[69] Zhengyuan Yang, Zhe Gan, Jianfeng Wang, Xiaowei Hu,
     Yumao Lu, Zicheng Liu, and Lijuan Wang. An empirical study
     of gpt-3 for few-shot knowledge-based vqa. In Proceedings
     of the AAAI Conference on Artificial Intelligence, pages 3081–
     3089, 2022. 3
[70] Zhengyuan Yang, Linjie Li, Kevin Lin, Jianfeng Wang,
     Chung-Ching Lin, Zicheng Liu, and Lijuan Wang. The dawn
     of lmms: Preliminary explorations with gpt-4v (ision). arXiv
     preprint arXiv:2309.17421, 9, 2023. 1
[71] Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin Lin, Ehsan
     Azarnasab, Faisal Ahmed, Zicheng Liu, Ce Liu, Michael


                                                                         14
A. Examples outputs of our data-synthesis pipeline
We first present step-by-step examples of our data-synthesis pipeline. As discussed in §3, the pipeline contains four steps:
program generation, program execution, program filtering, and converting execution traces into chains-of-thoughts. Here we
show three filtered examples from three datasets we use. As shown, LLMs like PaLM-2 [3] are able to generate complex
programs to solve compositional vision tasks. The synthesized CoTs are used to fine-tune our VLMs.

    (a)
                                         Is the bookshelf to the right or to the left of the chair that is to the left of the vase?

                                         PaLM-2 Generated Program




                                         Execution Trace




                                         Conversion to COT

                                          The vase is at 676 615 756 653. To its left, the chair is at 603 467 771 549. The
                                          bookshelf is at 505 244 714 359. Therefore, the bookshelf is to the left of the
                                          chair.




                                                              15
(b)
                                        How many cars have the brake lights on?

                                       PaLM-2 Generated Program




                                        Execution Trace




                                        Conversion to COT

                                          The cars at 669 103 779 286 and 669 468 769 664 have the brake lights on. Thus,
                                          there are 2 cars with the brake lights on.



(c)
                                      What is usually found in the same room as the word on the sign spelled backwards?

                                       PaLM-2 Generated Program




                                       Execution Trace




                                       Conversion to COT

                                        The word on the sign is “stop”. “Stop” spelled backwards is “pots”. Pans are
                                        usually found in the same room as pots.

 Figure 8. Examples of our data-synthesis pipeline. (a) is from GQA [26]; (b) is from TallyQA [1]; (c) is from A-OKVQA [52].




                                                             16
B. Experimental details
B.1. Model architecture details
For both PaLI models that we considered in our experiments, the architectures are similar: images are encoded into visual
tokens individually via a visual encoder. Then, the vision tokens along with the textual inputs are passed through an encoder-
decoder UL2 Transformer [58]. The PaLI models were then pre-trained with image-text pairs to perform multimodal tasks.
Specifically, PaLI-3 [11] uses a pre-trained 2B SigLIP [77] as visual encoder, and a 3B UL2. The image resolution is 812 × 812.
PaLI-X [10] uses a pre-trained VIT-22B [15] as visual encoder, and a 32B UL2. The image resolution is 756 × 756. Please
refer to the PaLI-3 [11] and PaLI-X [10] papers about more architecture details.

B.2. Datasets
The details of the data mixture of academic task-oriented VQA datasets used in VPD training are shown in Table 4. We only
use a subset of each dataset’s training set. # labels refers to the total number of examples (containing image, query, and answer)
we use. # CoTs refers to the number of examples that we have synthesized CoTs using our programs. In total, there are 89.6K
CoTs used during training.


                                       Dataset              Description      # labels    # COTs
                                       VQAv2 [19]           General           100.0K
                                       OCR-VQA [48]         OCR                50.0K
                                       GQA [26]             Compositional      86.0K      38.0K
                                       OK-VQA [45]          Knowledge           9.0K       6.7K
                                       A-OKVQA [52]         Knowledge          17.1K      11.2K
                                       TallyQA [1]          Counting           48.4K      33.7K
                                       Total                                  310.5K      89.6K

                        Table 4. Data mixture of academic task-oriented VQA datasets used in VPD training.


   Details of each evaluation benchmark we use are in Table 5. For free-form question answering, we run inference with the
prompt “Answer with a single word or phrase.”, using greedy decoding without any constraint on the model’s output space.
For multiple-choice questions, we run inference with the prompt “Answer with the option letter from the given choices directly.”
and generate the option letter.


 Dataset            Description                                                                             # split        # Metrics
 VQAv2 [19]         General VQA. General questions about entities, colors, materials, etc.                  test-dev       VQA Score
                    Compositional VQA. Built on the scene-graphs in Visual Genome [32].
 GQA [26]                                                                                                   test-dev       EM
                    More compositional questions and spatial relation questions.
 OK-VQA [45]        Knowledge-based VQA. Questions that need external knowledge to be answered.             val            VQA Score
 A-OKVQA [52]       An advanced version of OK-VQA that is more challenging.
                     – Multiple Choice (MC): choose 1 of the 4 options.                                     val, test      EM
                     – Direct Answer (DA): compare with 10 free-form human answers                          val, test      VQA Score
 TallyQA [1]        Counting questions.
                     – Simple: synthesized simple counting questions                                        test-simple    EM
                     – Complex: human-written complex counting questions                                    test-complex   EM
 TextVQA [55]       VQA on images that contain text                                                         val            VQA Score
                    Benchmark on VLM hallucination.
 POPE [36]                                                                                                  dev            EM
                    Binary questions of whether an object exists in the image.
                    Comprehensive benchmark on VLMs with multiple-choice questions.
 MMBench [40]       Covering 20 ability dimensions across 3 levels (e.g., coarse perception, fine-grained   dev            EM
                    perception, attribute reasoning, relation reasoning, logic reasoning, etc.)

                                               Table 5. Summary of evaluation benchmarks.



                                                                  17
B.3. Training details
We use LoRA [22] to fine-tune both PaLI-3 [11] and PaLI-X [10]. For generalist training, we add LoRA weights on each linear
layer in the attention blocks and multilayer perceptron (MLP) blocks for both the encoder and decoder in the UL2 transformer.
For both models, we use rank = 8. We use a cosine learning rate schedule, with warm-up ratio 1% and peak learning rate
1e − 4. For all models and all settings, we use a batch size of 128 and fine-tune the pre-trained model for 8, 000 steps. In terms
of training time, we train PaLI-X-VPD with 128 TPU-v3 [27] and it takes about 2 days to finish training. For PaLI-3-VPD,
we use 32 TPU-v4 and training takes about 20 hours. We still observe a steady loss drop when we terminate training, which
indicates that more computation may lead to even better performance. For per-task fine-tuning, to avoid overfitting, we reduce
the number of training parameters. For both models, we only add LoRA weights to encoder layers. We use LoRA rank = 4
for PaLI-X-VPD and rank = 8 for PaLI-3-VPD. The peak learning rate is 1e − 4 and we use a cosine learning schedule,
with warm-up ratio 1%. For all per-task fine-tuning experiments, we use a batch size of 64. We train for 1 epoch on GQA,
and 3 epochs on all other datasets. We use the AdamW [30] optimizer with β1 = 0.9 and β2 = 0.98, and bfloat16 for all
experiments.

B.4. Inference costs
We sampled 300 questions and measured the computation cost. Using 128 TPU v5, code generation takes on average 4.7s,
while program execution takes 4.2s. With the same resources, PaLI-X-VPD takes 0.8s per question. The cost gap (0.8s vs
8.9s) is very large with immense consequences for practical applications.

C. Human evaluation
We asked our human annotators to first evaluate each model’s answer, using the criteria described in §4.3. After rating each
model answer separately, we also asked them to choose a preferred answer between the two. However, we observed that there
are cases where one or both models have similar answers, or both answers are incorrect, in which case it would be difficult for
the annotators to choose a favorite, so we also provided the annotators with the options “Both” or “Neither”, giving them the
following instruction: “Please try to choose "Answer 1 is better" or "Answer 2 is better" whenever possible. We also give you
the option to choose "Both are equally good." or "Both are too bad to make a choice." for the cases when it is hard to make a
choice either because both answers are correct and similar, or because both answers are wrong so it makes no sense to choose
a favorite.”
    We show some examples from our human evaluation in Table 6. The table contains the images and corresponding
text queries (column 2), the answers provided by the two models we compared—PaLI-X Instruct (column 3) and
PaLI-X-VPD (column 4)—along with the corresponding annotations given by the human annotators. The human annotations
are aggregated across 3 raters per sample. Finally, column 5 shows which of the two answers was preferred by the human
raters. When a model’s answer includes a bounding box, we annotate it on the image for convenience. Examples are as follow:
   • Example #1 shows a common situation where PaLI-X-VPD succeeds where PaLI-X Instruct fails. By being
     trained with programs that include calls to an object detection tool, PaLI-X-VPD has learned to produce answers that
     localize the object in question in the image, which prods the model to correctly perform tasks such as counting.

  • Example #2 shows a type of question where neither model produces an explanation, where one is arguably not necessary.
    However, in spite the lack of explanation, PaLI-X-VPD’s answer is more accurate.

  • Example #3 shows an example where from Tally QA where PaLI-X-VPD is able to correctly localize and count the
    number of tennis balls in the image, as asked by the question, when PaLI-X Instruct counts incorrectly and also
    does not provide a rationale.

  • Example #4 shows a situation where PaLI-X-VPD produces an answer that is deemed both factual and consistent by
    the human raters, and yet the answer is incorrect. Indeed we can notice that everything that PaLI-X-VPD is accurate
    with respect to the context image, and yet it does not address the question as expected by the human raters.

  • Example #5 shows a case where both models are incorrect, but the annotators prefer PaLI-X-VPD’s answer, despite the
    fact that both models essentially give the same incorrect final count of 0 yellow busses. However, PaLI-X-VPD provides
    a consistent rationale, from which we can tell the reason for its mistake: it correctly identifies 2 out of the 3 buses in the
    image, missing the partially occluded yellow bus in the back. It seems the annotators prefer this kind of mistake over one
    without an explanation.


                                                               18
 Index               Image & Query                   PaLI-Instruct Answer                      PaLI-VPD Answer                  Annotator
                                                          & Human Eval                           & Human Eval                   Preference
   1.                                            The knife is on the left side of the   The knife is at 55 693 412 884,         PaLI-VPD
                                                 table.                                 which is on the right side of the
                                                                                        image.
                                                 • Correct: ✗
                                                 • Has Explanation: ✗                   • Correct: ✓
                                                 • Explanation Factuality: N/A          • Has Explanation: ✓
                                                 • Explanation Consistency: N/A         • Explanation Factuality: ✓
                                                                                        • Explanation Consistency: ✓



         On which side is the knife?
   2.                                            The fruits in the image are apples     The fruits are called apples.           PaLI-VPD
                                                 and broccoli.
                                                                                        • Correct: ✓
                                                 • Correct: ✗                           • Has Explanation: ✗
                                                 • Has Explanation: ✗                   • Explanation Factuality: N/A
                                                 • Explanation Factuality: N/A          • Explanation Consistency: N/A
                                                 • Explanation Consistency: N/A




         What are this fruits called?
   3.                                            There are two tennis balls in the      There is a tennis ball at 826 665 869   PaLI-VPD
                                                 photo.                                 721. Thus, there is 1 tennis ball.

                                                 • Correct: ✗                           • Correct: ✓
                                                 • Has Explanation: ✗                   • Has Explanation: ✓
                                                 • Explanation Factuality: N/A          • Explanation Factuality: ✓
                                                 • Explanation Consistency: N/A         • Explanation Consistency: ✓




           How many tennis balls are in the
           photo?
   4.                                            The player is wearing gloves           The player is wearing gloves to         PaLI-
                                                 because he is a batter. Batters wear   catch the ball.                         Instruct
                                                 gloves to protect their hands from
                                                 the ball.                              • Correct: ✗
                                                                                        • Has Explanation: ✓
                                                 • Correct: ✓                           • Explanation Factuality: ✓
                                                 • Has Explanation: ✗                   • Explanation Consistency: ✓
                                                 • Explanation Factuality: ✓
                                                 • Explanation Consistency: ✓
         Why is one player wearing gloves?
   5.                                            There are no yellow buses in the       There are 2 buses in the picture.       PaLI-VPD
                                                 picture.                               Neither of them is yellow. Thus,
                                                                                        there are 0 yellow buses in the
                                                 • Correct: ✗                           picture.
                                                 • Has Explanation: ✗
                                                 • Explanation Factuality: N/A          • Correct: ✗
                                                 • Explanation Consistency: N/A         • Has Explanation: ✓
                                                                                        • Explanation Factuality: ✗
                                                                                        • Explanation Consistency: ✓
         How many yellow buses are in the pic-
         ture?
Table 6. Human Annotation Examples. We show the answers provided by the two models, PaLI-X Instruct and PaLI-X-VPD, along
with the aggregated evaluation scores by human raters along the criteria introduced in §4.3.
                                                              19
     D. Prompts
     In this section we present the prompts used in our data synthesis pipeline. Refer to §A for step-by-step examples of the
     programs, execution traces, and the converted CoTs.

     D.1. Prompt for code generation
     For each image and query, we put the query and a model-generated image caption in the prompt. An LLM takes this prompt
     and generate the program to answer the query. We modify the original ViperGPT [16] prompt to adapt to the vision tools we
     use in this paper.
 1   class ImagePatch:
 2       # A Python class containing a crop of an image centered around a particular object , as well as relevant information .
 3       # Attributes
 4       # −−−−−−−−−−
 5       # cropped_image : array_like
 6       #      An array−like of the cropped image taken from the original image.
 7       # left , lower, right , upper : int
 8       #      An int describing the position of the ( left /lower/ right /upper) border of the crop’s bounding box in the original image.
 9       # Methods
10       # −−−−−−−
11       # find (object_name: str )−>List[ImagePatch]
12       #      Returns a list of new ImagePatch objects containing crops of the image centered around any objects found in the
13       #      image matching the object_name.
14       # visual_question_answering ( question : str =None)−>str
15       #      Returns the answer to a basic question asked about the image. If no question is provided , returns the answer to "What is this ?".
16       # image_caption()−>str
17       #      Returns a short description of the image crop .
18       # expand_patch_with_surrounding()−>ImagePatch
19       #      Returns a new ImagePatch object that contains the current ImagePatch and its surroundings .
20       # overlaps ( patch : ImagePatch)−>Bool
21       #      Returns True if the current ImagePatch overlaps with another patch and False otherwise
22       # compute_depth()−>float
23       #      Returns the median depth of the image patch . The bigger the depth , the further the patch is from the camera.
24
25      def __init__ ( self , image, left : int = None, lower: int = None, right : int = None, upper: int = None):
26          # Initializes an ImagePatch object by cropping the image at the given coordinates and stores the coordinates as
27          # attributes . If no coordinates are provided , the image is left unmodified, and the coordinates are set to the
28          # dimensions of the image.
29          # Parameters
30          # −−−−−−−
31          # image: PIL.Image
32          #      An array−like of the original image.
33          # left , lower, right , upper : int
34          #      An int describing the position of the ( left /lower/ right /upper) border of the crop’s bounding box in the original image.
35          #      The coordinates (y1,x1,y2,x2) are with respect to the upper left corner the original image.
36          #      To be closer with human perception , left , lower, right , upper are with respect to the lower left corner of the squared image.
37          #      Use left , lower, right , upper for downstream tasks .
38
39           self . original_image = image
40           size_x , size_y = image. size
41
42           if left is None and right is None and upper is None and lower is None:
43                self . x1 = 0
44                self . y1 = 0
45                self . x2 = 999
46                self . y2 = 999
47           else :
48                self . x1 = left
49                self . y1 = 999 − upper
50                self . x2 = right
51                self . y2 = 999 − lower
52
53           self . cropped_image = image.crop (( int ( self . x1/1000* self . sz) , int ( self . y1/1000* self . sz) ,
54                                              int ( self . x2/1000* self . sz) , int ( self . y2/1000* self . sz) ) )
55
56           self . width = self . x2 − self . x1
57           self . height = self . y2 − self . y1
58
59          # all coordinates use the upper left corner as the origin (0,0) .
60          # However, human perception uses the lower left corner as the origin .
61          # So, need to revert upper/lower for language model
62          self . left = self . x1
63          self . right = self . x2
64          self . upper = 999 − self . y1
65          self . lower = 999 − self . y2
66
67           self . horizontal_center = ( self . left + self . right ) / 2
68           self . vertical_center = ( self . lower + self . upper) / 2
69
70           self . patch_description_string = f"{ self . y1} { self . x1} { self . y2} { self . x2}"
71
72      def __str__ ( self ) :
73          return self . patch_description_string
74
75      def compute_depth(self ) :
76          # compute the depth map on the full image. Returns a np. array with size 192*192
77          # Parameters
78          # −−−−−−−−−−
79          # Returns
80          # −−−−−−−
81          # float
82          #     the median depth of the image crop
83
84          # Examples
85          # −−−−−−−−
86          # >>> return the image patch of the bar furthest away
87          # >>> def execute_command(image)−>ImagePatch:
88          # >>>     image_patch = ImagePatch(image)
89          # >>>     bar_patches = image_patch. find (" bar ")




                                                                                                                          20
 90      # >>>       bar_patches . sort (key=lambda bar: bar . compute_depth())
 91      # >>>       return bar_patches [−1]
 92
 93       return depth( self . cropped_image)
 94
 95   def find ( self , object_name: str ) :
 96       # Returns a list of ImagePatch objects matching object_name contained in the crop if any are found.
 97       # The object_name should be as simple as example, including only nouns
 98       # Otherwise, returns an empty list .
 99       # Note that the returned patches are not ordered
100       # Parameters
101       # −−−−−−−−−−
102       # object_name : str
103       #       the name of the object to be found
104
105      # Returns
106      # −−−−−−−
107      # List [ImagePatch]
108      #      a list of ImagePatch objects matching object_name contained in the crop
109
110      # Examples
111      # −−−−−−−−
112      # >>> # find all the kids in the images
113      # >>> def execute_command(image) −> List[ImagePatch]:
114      # >>>     image_patch = ImagePatch(image)
115      # >>>      kid_patches = image_patch. find (" kid ")
116      # >>>      return kid_patches
117
118       print ( f" Calling find function . Detect {object_name}.")
119       det_patches = detect ( self . cropped_image, object_name)
120       print ( f" Detection result : {’ and ’. join ([ str (d) + ’ ’ + object_name for d in det_patches ]) }")
121
122       return det_patches
123
124
125   def expand_patch_with_surrounding( self ) :
126       # Expand the image patch to include the surroundings . Now done by keeping the center of the patch
127       # and returns a patch with double width and height
128
129      # Examples
130      # −−−−−−−
131      # >>> # How many kids are not sitting under an umbrella?
132      # >>> def execute_command(image):
133      # >>>     image_patch = ImagePatch(image)
134      # >>>     kid_patches = image_patch. find (" kid ")
135
136      # >>>      # Find the kids that are under the umbrella .
137      # >>>      kids_not_under_umbrella = []
138
139      # >>>       for kid_patch in kid_patches :
140      # >>>           kid_with_surrounding = kid_patch . expand_patch_with_surrounding()
141      # >>>           if "yes" in kid_with_surrounding . visual_question_answering (" Is the kid under the umbrella ?") :
142      # >>>                print ( f"the kid at {kid_patch} is sitting under an umbrella .")
143      # >>>           else :
144      # >>>                print ( f"the kid at {kid_patch} is not sitting under an umbrella .")
145      # >>>                kids_not_under_umbrella . append(kid_patch)
146
147      # >>>      # Count the number of kids under the umbrella .
148      # >>>      num_kids_not_under_umbrella = len(kids_not_under_umbrella)
149
150      # >>>       return formatting_answer ( str (num_kids_not_under_umbrella))
151
152      new_left = max(self . left − self . width / 2, 0)
153      new_right = min( self . right + self . width / 2, 999)
154      new_lower = max(self . lower − self . height / 2,0)
155      new_upper = min(self . upper + self . height / 2, 999)
156
157       return ImagePatch( self . original_image , new_left , new_lower, new_right , new_upper)
158
159
160   def visual_question_answering ( self , question : str = None) −> str :
161       # Returns the answer to a basic question asked about the image.
162       # The questions are about basic perception , and are not meant to be used for complex reasoning
163       # or external knowledge.
164
165      # Parameters
166      # −−−−−−−
167      # question : str
168      #     A string describing the question to be asked.
169
170      # Examples
171      # −−−−−−−
172
173      # >>> # What is the name of the player in this picture ?
174      # >>> def execute_command(image) −> str:
175      # >>>     image_patch = ImagePatch(image)
176      # >>>      return formatting_answer (image_patch. visual_question_answering ("What is the name of the player ?") )
177
178      # >>> # What color is the foo?
179      # >>> def execute_command(image) −> str:
180      # >>>     image_patch = ImagePatch(image)
181      # >>>      return formatting_answer (foo_patch . visual_question_answering ("What color is the foo?") )
182
183      # >>> # What country serves this kind of food the most?
184      # >>> def execute_command(image) −> str:
185      # >>>     image_patch = ImagePatch(image)
186      # >>>     food_name = image_patch. visual_question_answering ("What kind of food is served ?")
187      # >>>     country = language_question_answering( f"What country serves {food_name} most?", long_answer=False)
188      # >>>      return formatting_answer ( country )
189
190      # >>> # Is the second bar from the left quuxy?
191      # >>> def execute_command(image) −> str:
192      # >>>     image_patch = ImagePatch(image)
193      # >>>     bar_patches = image_patch. find (" bar ")
194      # >>>     bar_patches . sort (key=lambda x: x. horizontal_center )
195      # >>>     bar_patch = bar_patches [1]
196      # >>>      return formatting_answer ( bar_patch . visual_question_answering (" Is the bar quuxy?"))




                                                                                                                    21
197
198           answer = vqa( self . cropped_image, question )
199
200           print ( f" Calling visual_question_answering function . ")
201           print ( f"Question: {question}")
202           print ( f"Answer: {answer}")
203
204           return answer
205
206       def image_caption( self ) −> str :
207           # Returns a short description of the image.
208            return image_caption( self . cropped_image)
209
210       def overlaps ( self , patch ) −> bool:
211           # check if another image patch overlaps with this image patch
212           # if patch overlaps with current patch , return True. Otherwise return False
213
214           if patch . right < self . left or self . right < patch . left :
215             return False
216           if patch . lower > self . upper or self . lower > patch . upper:
217             return False
218           return True
219
220
221   def language_question_answering( question : str , long_answer: bool = False ) −> str :
222       # Answers a text question using a lanugage model like PaLM and GPT−3. The input question is always a formatted string with a variable in it .
223       # Default is short −form answers, can be made long−form responses with the long_answer flag .
224
225      # Parameters
226      # −−−−−−−−−−
227      # question : str
228      #     the text question to ask . Language model cannot anderstand the image. Must not contain any reference to ’ the image’ or ’ the photo ’, etc .
229      # long_answer: bool
230      #     whether to return a short answer or a long answer. Short answers are one or at most two words, very concise .
231      #     Long answers are longer , and may be paragraphs and explanations . Defalt is False .
232
233      # Examples
234      # −−−−−−−−
235      # >>> # What is the city this building is in?
236      # >>> def execute_command(image) −> str:
237      # >>>     image_patch = ImagePatch(image)
238      # >>>     building_name = building_patch . visual_question_answering ("What is the name of the building ?")
239      # >>>      return formatting_answer (language_question_answering( f"What city is {building_name} in ?", long_answer=False))
240
241      # >>> # Who invented this object ?
242      # >>> def execute_command(image) −> str:
243      # >>>     image_patch = ImagePatch(image)
244      # >>>     object_name = object_patch . visual_question_answering ("What is this object ?")
245      # >>>      return formatting_answer (language_question_answering( f"Who invented {object_name}?", long_answer=False))
246
247      # >>> # Explain the history behind this object .
248      # >>> def execute_command(image) −> str:
249      # >>>       image_patch = ImagePatch(image)
250      # >>>       object_name = object_patch . visual_question_answering ("What is the object ?")
251      # >>>        return formatting_answer (. language_question_answering( f"What is the history behind {object_name}?", long_answer=True))
252      print ( f" Calling language_question_answering")
253      print ( f"Question: {question}")
254
255      answer = language_model_qa(question, long_answer).lower () . strip ()
256      print ( f"Answer: {answer}")
257      return answer
258
259
260   def distance (patch_a : Union[ImagePatch, float ], patch_b: Union[ImagePatch, float ]) −> float :
261       # Returns the distance between the edges of two ImagePatches, or between two floats .
262       # If the patches overlap , it returns a negative distance corresponding to the negative intersection over union.
263
264      # Parameters
265      # −−−−−−−−−−
266      # patch_a : ImagePatch
267      # patch_b : ImagePatch
268
269      # Examples
270      # −−−−−−−−
271      # # Return the qux that is closest to the foo
272      # >>> def execute_command(image):
273      # >>>     image_patch = ImagePatch(image)
274      # >>>     qux_patches = image_patch. find (’ qux’)
275      # >>>     foo_patches = image_patch. find (’ foo ’)
276      # >>>     foo_patch = foo_patches [0]
277      # >>>     qux_patches. sort (key=lambda x: distance (x, foo_patch) )
278      # >>>      return qux_patches[0]
279
280       return dist (patch_a , patch_b)
281
282
283   def formatting_answer (answer) −> str :
284       # Formatting the answer into a string that follows the task ’s requirement
285       # For example, it changes bool value to "yes" or "no", and clean up long answer into short ones.
286       # This function should be used at the end of each program
287
288       final_answer = ""
289       if isinstance (answer, str ) :
290          final_answer = answer. strip ()
291
292       elif isinstance (answer, bool) :
293         final_answer = "yes" if answer else "no"
294
295       elif isinstance (answer, list ) :
296         final_answer = " , " . join ([ str (x) for x in answer])
297
298       elif isinstance (answer, ImagePatch):
299         final_answer = answer.image_caption()
300
301       else :
302          final_answer = str (answer)
303




                                                                                                                     22
304       print ( f"Program output : { final_answer }")
305       return final_answer
306
307
308   Given an image and a query, write the function execute_command using Python and the ImagePatch class (above) , and the other functions above that could be executed to provide an answer to the query.
309   For reference , a model generated image description is also provided , so that the function can be customized for the given image. The image description is model−generated and may not be reliable , so do not trust it .
310
311   Consider the following guidelines :
312   − Use base Python (comparison, sorting ) for basic logical operations , left / right /up/down, math, etc .
313   − Use the language_question_answering function to access external information and answer informational questions NOT concerning the image.
314   − The program should print out the intermediate traces as it runs . So add print function in the program if needed.
315
316   For usual cases , follow the guidelines below:
317   − For simple visual queries , directly call visual_question_answering to get the answer.
318   − For queries that need world knowledge, commonsense knowledge, and language reasoning , use visual_question_answering , language_question_answering , and sometimes image_caption to get the answer.
319   − For queries that require counting and spatical relations , in addition to the above functions , use find function to help getting the answer.
320   − For queries involve "behind" and " front " , consider using compute_depth function .
321
322
323   Some examples:
324   Image description : a woman is walking several dogs
325   Query: how many dogs are to left of the person?
326   Function :
327   def execute_command(image):
328       image_patch = ImagePatch(image)
329       person_patch = image_patch. find ("person") [0]
330       dog_patches = image_patch. find ("dog")
331
332       # Count the number of dogs whose leftmost x−coordinate is less than the person .
333       num_dogs_left = 0
334       for dog_patch in dog_patches:
335           if dog_patch. left < person_patch . horizontal_center :
336               print ( f"dog at {dog_patch} is on the left of human.")
337               num_dogs_left += 1
338
339       return formatting_answer (num_dogs_left)
340
341   # [ other in−context examples]
342
343   Image description : INSERT_IMAGE_CAPTION_HERE
344   Query: INSERT_QUERY_HERE
345   Function :




      D.2. Prompt for result verification
      After running each program, we get an output. As discussed in §3.1, we adopt the method of [28] and use an LLM to determine
      if the program output matches human answers. The LLM takes the program output and reference answers as input. The
      prompt is as follows:
 1    Given a visual question , several human annotator answers, and a candidate answer, determine if the candidate is correct .
 2    The candidate is considered correct if is allowed to have formatting differences compared with the human answers.
 3    If the candidate is correct , return the gold answer it matches. Otherwise, return None.
 4
 5    Question: INSERT_QUESTION_HERE
 6    Answers: INSERT_ANSWERS_HERE
 7    Candidate: INSERT_CANDIDATE_HERE
 8    Is the candidate correct ?




      D.3. Prompt for CoT conversion
      Finally, once a program is filtered, we convert its execution trace into chain-of-thought using an LLM. The LLM takes the
      query, program, execution trace, program output as input, and summarizes the execution trace into a chain-of-thought rationale.
      The prompt we use as as follows:
 1    Given an image and a question , I wrote the function execute_command using Python and the ImagePatch class (above) , and the other functions above that could be executed to provide an answer to the query.
 2    As shown in the code, the code will print execution traces .
 3    I need you to rewrite the execution trace into a natural language rationale that leads to the answer.
 4
 5    Consider the following guidelines :
 6    − Use the bounding box information in the rationale .
 7    − Referencing the execution trace , write a reasoning chain that leads to the most common human answer. Notice that the output should be the same as the human answer, not necessarily the program output .
 8
 9
10    Some examples:
11    Question: How many wheels does the plane have?
12    Program:
13    def execute_command(image):
14        image_patch = ImagePatch(image)
15
16        # Find the plane in the image
17        plane_patch = image_patch. find (" plane ") [0]
18
19        # Count the number of wheels on the plane
20        num_wheels = 0
21        for wheel in plane_patch . find ("wheel"):
22            num_wheels += 1
23
24         return formatting_answer ( str (num_wheels))
25    Execution trace :
26    Calling find function . Detect plane
27    Detected plane at 153 25 647 972
28    Calling find function . Detect wheel
29    Detected wheel at 603 471 649 515
30    Detected wheel at 621 85 646 113
31    Detected wheel at 615 383 645 428
32    Program output : 3




                                                                                                                    23
33   Rationale : The plane at 153 25 647 972 has wheels at 603 471 649 515, 621 85 646 113, and 615 383 645 428.Thus, it has 3 wheels.
34
35   [Other demonstration examples]
36
37   Question: INSERT_QUESTION_HERE
38   INSERT_PROGRAM_HERE
39   Execution trace :
40   INSERT_EXECUTION_TRACE_HERE
41   Rationale :




                                                                                                                  24
