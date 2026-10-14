                                         A Survey of Safety and Trustworthiness of Large
                                             Language Models through the Lens of
                                                   Verification and Validation
arXiv:2305.11391v2 [cs.AI] 27 Aug 2023




                                         Xiaowei Huang1 , Wenjie Ruan1 , Wei Huang5,1 , Gaojie Jin1 , Yi Dong1 ,
                                          Changshun Wu2 , Saddek Bensalem2 , Ronghui Mu1 , Yi Qi1 , Xingyu
                                         Zhao1 , Kaiwen Cai1 , Yanghao Zhang1 , Sihao Wu1 , Peipei Xu1 , Dengyu
                                                    Wu1 , Andre Freitas3 , and Mustafa A. Mustafa3,4
                                                                     1 University of Liverpool, UK
                                                                2 Université Grenoble Alpes, France
                                                                3 The University of Manchester, UK
                                                                   4 COSIC, KU Leuven, Belgium
                                                              5 Purple Mountain Laboratories, China




                                                                                    Abstract
                                                   Large Language Models (LLMs) have exploded a new heatwave of AI for their
                                               ability to engage end-users in human-level conversations with detailed and articu-
                                               late answers across many knowledge domains. In response to their fast adoption in
                                               many industrial applications, this survey concerns their safety and trustworthiness.
                                               First, we review known vulnerabilities and limitations of the LLMs, categoris-
                                               ing them into inherent issues, attacks, and unintended bugs. Then, we consider
                                               if and how the Verification and Validation (V&V) techniques, which have been
                                               widely developed for traditional software and deep learning models such as convo-
                                               lutional neural networks as independent processes to check the alignment of their
                                               implementations against the specifications, can be integrated and further extended
                                               throughout the lifecycle of the LLMs to provide rigorous analysis to the safety
                                               and trustworthiness of LLMs and their applications. Specifically, we consider four
                                               complementary techniques: falsification and evaluation, verification, runtime mon-
                                               itoring, and regulations and ethical use. In total, 370+ references are considered to
                                               support the quick understanding of the safety and trustworthiness issues from the
                                               perspective of V&V. While intensive research has been conducted to identify the
                                               safety and trustworthiness issues, rigorous yet practical methods are called for to
                                               ensure the alignment of LLMs with safety and trustworthiness requirements.


                                         Contents
                                         1   Introduction                                                                              3


                                                                                        1
2   Large Language Models                                                             6
    2.1 Categories of Large Language Models . . . . . . . . . . . . . . . . .         6
        2.1.1 Text-based Conversational AI . . . . . . . . . . . . . . . . .          6
        2.1.2 Text-based Image Synthesis . . . . . . . . . . . . . . . . . .          7
    2.2 Lifecycle of LLMs . . . . . . . . . . . . . . . . . . . . . . . . . . .       8
    2.3 Key Techniques Relevant to Safety and Trustworthiness . . . . . . . .         9
        2.3.1 Reinforcement learning from human feedback (RLHF) . . . .               9
        2.3.2 Guardrails . . . . . . . . . . . . . . . . . . . . . . . . . . . .     10

3   Vulnerabilities, Attacks, and Limitations                                        10
    3.1 Inherent Issues . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    11
         3.1.1 Performance Issues . . . . . . . . . . . . . . . . . . . . . . .      11
                 3.1.1.1 Factual errors . . . . . . . . . . . . . . . . . . . .      12
                 3.1.1.2 Reasoning errors . . . . . . . . . . . . . . . . . . .      12
         3.1.2 Sustainability Issues . . . . . . . . . . . . . . . . . . . . . .     12
         3.1.3 Other Inherent Trustworthiness and Responsibility Issues . . .        13
    3.2 Attacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    15
         3.2.1 Unauthorised Disclosure and Privacy Concerns . . . . . . . .          15
         3.2.2 Robustness Gaps . . . . . . . . . . . . . . . . . . . . . . . .       15
         3.2.3 Backdoor Attacks . . . . . . . . . . . . . . . . . . . . . . . .      16
                 3.2.3.1 Design of Backdoor Trigger . . . . . . . . . . . . .        16
                 3.2.3.2 Backdoor Embedding Strategies . . . . . . . . . .           17
                 3.2.3.3 Expression of Backdoor . . . . . . . . . . . . . . .        17
         3.2.4 Poisoning and Disinformation . . . . . . . . . . . . . . . . .        18
    3.3 Unintended Bugs . . . . . . . . . . . . . . . . . . . . . . . . . . . .      19
         3.3.1 Incidental Exposure of User Information . . . . . . . . . . .         19
         3.3.2 Bias and Discrimination . . . . . . . . . . . . . . . . . . . .       19

4   General Verification Framework                                                   19

5   Falsification and Evaluation                                                     21
    5.1 Prompt Injection . . . . . . . . . . . . . . . . . . . . . . . . . . . .     21
    5.2 Comparison with Human Experts . . . . . . . . . . . . . . . . . . . .        22
    5.3 Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     23
    5.4 Testing and Statistical Evaluation . . . . . . . . . . . . . . . . . . . .   23

6   Verification                                                                     25
    6.1 Verification on Natural Language Processing Models . . . . . . . . .         25
          6.1.1 Verification via Interval Bound Propagation . . . . . . . . . .      25
          6.1.2 Verification via Abstract Interpretation . . . . . . . . . . . . .   26
          6.1.3 Verification via Randomised Smoothing . . . . . . . . . . . .        27
    6.2 Black-box Verification . . . . . . . . . . . . . . . . . . . . . . . . .     28
    6.3 Robustness Evaluation on LLMs . . . . . . . . . . . . . . . . . . . .        30
    6.4 Towards Smaller Models . . . . . . . . . . . . . . . . . . . . . . . .       30




                                           2
7   Runtime Monitor                                                                   31
    7.1 Monitoring Out-Of-Distribution . . . . . . . . . . . . . . . . . . . .        32
    7.2 Monitoring Attacks . . . . . . . . . . . . . . . . . . . . . . . . . . .      33
    7.3 Monitoring Output Failures . . . . . . . . . . . . . . . . . . . . . . .      34
    7.4 Perspective . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     35

8   Regulations and Ethical Use                                                       36
    8.1 Regulate or Ban? . . . . . . . . . . . . . . . . . . . . . . . . . . . .      36
    8.2 Responsible AI Principles . . . . . . . . . . . . . . . . . . . . . . . .     37
    8.3 Educational Challenges . . . . . . . . . . . . . . . . . . . . . . . . .      37
    8.4 Transparency and Explainability . . . . . . . . . . . . . . . . . . . .       38

9   Discussions                                                                       38

10 Conclusions                                                                        39


1    Introduction
A Large Language Model (LLM) is a deep learning model equipped with a massive
amount of learnable parameters (commonly reaching more than 10 billion). LLMs are
attention-based sequential models based on the transformer architecture [149], which
consistently demonstrated the ability to learn universal representations of language.
The universal representations of language can then be used in various Natural Lan-
guage Processing (NLP) task. The recent scale-up of these models, in terms of both
numbers of parameters and pre-trained corpora, has confirmed the universality of trans-
formers as mechanisms to encode language representations. At a specific scale, these
models started to exhibit in-context learning [230, 351], and the properties of learning
from few examples (zero/one/few-shot – without the need for fine-tuning) and from
natural language prompts (complex instructions which describe the behavioural intent
that the model needs to operate). Recent works on Reinforcement Learning via Human
Feedback (RLHF) [241] have further developed the ability of these models to align and
respond to increasingly complex prompts, leading to their popularisation in systems
such as ChatGPT [23] and their use in a large spectrum of applications. The ability
of LLMs to deliver sophisticated linguistic and reasoning behaviour, has pushed their
application beyond their intended operational envelope.
    While being consistently fluent, LLMs are prone to hallucinations [286], stating
factually incorrect statements [285], lacking necessary mechanisms of safety, lacking
transparency and control [299], among many others. Such vulnerabilities and limita-
tions have already led to bad consequences such as suicide case [28], lawyer submitted
fabricated cases as precedent to the court [24], leakage of private information [6], etc.
Therefore, research is urgently needed to understand the potential vulnerabilities and
how the LLMs’ behaviour can be assured to be safe and trustable. The goal of this
paper is to provide a review of known vulnerabilities and limitations of LLMs and,
more importantly, to investigate how the V&V techniques can be adapted to improve
the safety and trustworthiness of LLMs. While there are several surveys on LLMs


                                           3
[370, 365], as well as a categorical archive of ChatGPT failures [58], to the best of our
knowledge, this is the first work that provides a comprehensive discussion on the safety
and trustworthiness issues, from the perspective of the V&V.
    With the rising of LLMs and its wide applications, the need to ensure their safety
and trustworthiness become prominent. Considering the broader subject of deep learn-
ing systems, to support their safety and trustworthiness, a diverse set of technical so-
lutions have been developed by different research communities. For example, the ma-
chine learning community is focused on adversarial attacks [126, 224, 88, 339], outlier
detectors [243], adversarial training [298, 231, 328], and explainable AI [337, 138, 264,
366]. The human-computer interaction community is focused on engaging the learn-
ing systems in the interactions with end users to improve the end users’ confidence
[106]. Formal methods community treats ML models as yet another symbolic system
(evidenced by their consideration of neurons, layers, etc.) and adapts existing formal
methods tools to work on the new systems [160]. While research has been intense on
these individual methods, a synergy among them has not been addressed. Without a
synergy, it is hard, if not impossible, to rigorously understand the causality between
methods and how they might collectively support the safe and trusted autonomous sys-
tems at runtime. This survey is rooted in the field of AI assurance, aiming to apply a
collection of rigorous V&V methods throughout the lifecycle of ML models, to pro-
vide assurance on the safety and trustworthiness. An illustrative diagram is given in
Figure 1 for general ML models. To begin with, data collection and synthesis is re-
quired to obtain as many as possible the training data, including the synthesis of high
quality data through e.g., data argumentation or generative models. In the training
phase, other than the prediction accuracy, multiple activities are needed, including e.g.,
the analysis of the learned feature representations and the checking for unintended bias.
After the training, we apply offline V&V methods to the ML model, including tech-
niques to falsify, explain, and verify the ML models. During the deployment phase,
we must analyse the impact and hazard of the potential application environment. The
operational design domain and operational data will be recorded. A run-time moni-
tor is associated to the ML model to detect outliers, distribution shifts, and failures in
the application environment. We may further apply reliability assessment methods to
evaluate the reliability of the ML model and identify failure scenarios. Based on the
detection or assessment results, we can identify the gaps for improvement. Finally,
we outline the factors that affect the performance of the ML model, and optimise the
training algorithm to obtain an enhanced ML model.
    These V&V techniques have been successful in supporting the reliable and depend-
able development of software and hardware that are applied to safety-critical systems,
and have been adapted to work with machine learning models, mainly focusing on the
convolutional neural networks for image classification (see surveys such as [160, 213]
and textbooks such as [159]), but also extended to consider, for example, object detec-
tion, deep reinforcement learning, and recurrent neural networks. This paper discusses
how to extend further the V&V techniques to deal with the safety and trustworthiness
challenges of LLMs.
    V&V are independent procedures that are used together for checking that a system
(or product, service) meets requirements and specifications and that it fulfills its in-
tended purpose [10]. Among them, verification techniques check the system against a


                                            4
                                                                                               •   Impact analysis
•   Falsification                                                                              •   Hazard/risk analysis
                                                Verification
•   Explanation                                                    Deployment                  •   Record Operational Design
                                                & Validation
•   Verification                                                                                   Domain (ODD)
                                                                                               •   Record operational data

•   Load training data                                                           Runtime       •   Observe outliers, distributional
•   Check accuracy                  Training                                    Monitoring         drift, failures, etc.
•   Analyze features                                                                           •   Apply enforcement when
•   Bias analysis                                                                                  needed
                                                             AI
                                                          Assurance

•   Collect more data                 Data                                       Reliability   •   Statistical evaluate reliability
•   Synthesize high-quality         Synthesis                                   Assessment     •   Identify failure scenarios
    data for training.


•   Delineate factors that affect
                                                   Model                                       •   Analyze runtime data to
    performance and properties                                     Analysis
                                                Enhancement                                        identify gaps for
•   Optimize training algorithms
    and hyper-parameters                                                                           improvements



      Figure 1: Summarisation of lifecycle V&V methods to support AI Assurance.


set of design specifications, and validation techniques ensure that the system meets the
user’s operational needs. From software, convolutional neural networks to LLMs, the
scale of the systems grows significantly, which makes the usual V&V techniques less
capable due to their computational scalability issues. White-box V&V techniques that
take the learnable parameters as their algorithmic input will not work well in practice.
Instead, the research should focus on black-box techniques, on which some research
has started for convolutional neural networks. In addition, V&V techniques need to
consider the non-deterministic nature of LLMs (i.e., different outputs for two tests
with identical input), which is a noticeable difference with the usual neural networks,
such as convolutional neural networks and object detectors, that currently most V&V
techniques work on.
    Considering the fast development of LLMs, this survey does not intend to be com-
plete (although it includes 370+ references), especially when it comes to the applica-
tions of LLMs in various domains, but rather a collection of organised literature reviews
and discussions to support the understanding of the safety and trustworthiness issues
from the perspective of V&V. Through the survey, we noticed that the current research
are focused on identifying the vulnerabilities, with limited efforts on systematic ap-
proaches to evaluate and verify the safety and trustworthiness properties.
    The structure of the paper is as follows. In Section 2, we review the LLMs and
its categories, its lifecycle, and several techniques introduced to improve safety and
trustworthiness. Then, in Section 3, we present a review of existing vulnerabilities.
This is followed by a general verification framework in Section 4. The framework
includes V&V techniques such as falsification and evaluation (Section 5), verification
(Section 6), runtime monitor (Section 7), and ethical use (Section 8). We conclude the
paper in Section 10.




                                                               5
2       Large Language Models
This section summarises the categories of machine learning tasks based on LLMs, fol-
lowed by a discussion of the lifecycle of LLMs. We will also discuss a few fundamental
techniques relevant to the safety analysis.

2.1     Categories of Large Language Models
LLMs have been applied to many tasks, such as text generation [205], content summary
[362], conversational AI (i.e., chatbots) [321], and image synthesis [186]. Other LLMs
applications can be seen as their adaptations or further applications. In the following,
we discuss the two most notable categories of LLMs: text-based conversational AI and
image synthesis. While they might have slightly different concerns, this survey will
be more focused on issues related to the former, without touching some issues that are
specific to image synthesis such as the detection of fake images.

2.1.1    Text-based Conversational AI
LLMs are designed to understand natural language and generate human-like responses
to queries and prompts. Almost all NLP tasks (e.g., language translation [60], chat-
bots [212, 133] and virtual assistants [307]) have witnessed tremendous success with
Transformer-based pretrained language models (T-PTLMs), relying on Transformer [311],
self-supervised learning [166, 217] and transfer learning [148, 269] to process and un-
derstand the nuances of human language, including grammar, syntax, and context.
    The well-known text-based LLMs include GPT-1 [254], BERT [98], XLNet [347],
RoBERTa [219], ELECTRA [85], T5 [256], ALBERT [193], BART [201], and PEGA-
SUS [360]. These models can learn general language representations from large vol-
umes of unlabelled text data through self-supervised learning and subsequently transfer
this knowledge to specific tasks, which has been a major factor contributing to their
success in NLP [176]. Kaplan et al. [181] demonstrated that simply increasing the
size of T-PTLMs can lead to improved performance [176]. This finding has spurred
the development of LLMs such as GPT-3 [61], PANGU [355], GShard [200], Switch-
Transformers [113] and GPT-4 [240].
    With the advancement of the Transformer development [311], significant enhance-
ments were achieved in handling sequential data. Leveraging the Transformer archi-
tecture, LLMs have been created as potent models with the capacity to generate text
resembling human language. ChatGPT represents a distinct embodiment of an LLM,
characterised by its remarkable performance that yields groundbreaking outcomes. The
progression of LLMs, depicted in Figure 2, starts from the evolution of deep learning
and transformer-based frameworks, culminating in the latest explosion of LLMs. We
divide the LLMs into Encoder-only, Decoder-only, and Encoder-Decoder according to
[343]. In Encoder-only and Encoder-Decoder architectures, the model predicts masked
words in a sentence while taking into account the surrounding context. While Decoder-
only models are trained by generating the subsequent word in a sequence based on the
preceding words. GPT-style language model belongs to the Decoder-only type.



                                           6
         Evolution Roadmap                                              ALBERT             ELECTRA

                                                                           Encoder-Only
                                                               BERT
             MLP     CNN              FastText                                      ChatGPT       GPT-4

               Deep Learning          Transformer                          Decoder-Only

             RNN      GAN             Word2Vec             GPT-1       GPT-2     GPT-3      LLaMA    LLaMA2

                                                                         BART            Switch
                                                                         Encoder-Decoder

                                                                          T5
                               2017                     2018          Large Language Models
                                                                              (LLMs)


               Figure 2: Large Language Models: Evolution Roadmap.


    We also note that, there are advanced uses of LLMs (or advanced prompt engineer-
ing) by considering e.g., self-consistency [319], knowledge graph [242], generating
programs as the intermediate reasoning steps [122], generating both reasoning traces
and task-specific actions in an interleaved manner [348], etc.

2.1.2   Text-based Image Synthesis
The transformer model [310] has become the standard choice for Language Modelling
tasks, but it has also found widespread integration in text-to-image tasks. We present
a chronological overview of the advancements in text-to-image research. DALL-E
[259] is a representative approach that leverages Transformers for a text-to-image gen-
eration. The methodology involves training a dVAE [265] and subsequently train-
ing a 12B decoder-only sparse transformer supervised by image tokens from the pre-
trained dVAE. The transformer generates image tokens solely based on text tokens
during inference. The resulting image candidates are evaluated by a pretrained CLIP
model [253] to produce the final generated image. StableFusion [266] differs from
DALL-E [259] by using a diffusion model instead of a Transformer to generate la-
tent image tokens. To incorporate text input, StableFusion [266] first encodes the text
using a transformer then conditions the diffusion model on the resulting text tokens.
GLIDE [238] employs a transformer model [310] to encode the text input and then
trains a diffusion model to generate images that are conditioned on the text tokens di-
rectly. DALL-E2 [258] effectively leverages LLMs by following a three-step process.
First, a CLIP model is trained using text-image pairs. Next, using text tokens as input,
an autoregressive or diffusion model generates image tokens. Finally, based on these
image tokens, a diffusion model is trained to produce the final image. Imagen [273]
employs a pre-trained text encoder, such as BERT [97] or CLIP [253], to encode text.
It then uses multiple diffusion models to train a process that generates images that start
from low-resolution and gradually progress to high-resolution. Parti [353] demon-
strates that a VQGAN [111] and Transformer architecture can achieve superior image
synthesis outcomes compared to previous approaches, even without utilising a diffu-
sion model. The eDiff-I model [44] has recently achieved state-of-the-art performance
on the MS-COCO dataset [211] by leveraging a combination of CLIP and diffusion


                                                    7
models.
    In summary, text-to-image research commonly utilises transformer models [310]
for encoding text input and either the diffusion model or the decoder of an autoencoder
for generating images from latent text or image tokens.

2.2   Lifecycle of LLMs
Figure 3 illustrates the lifecycle stages and the vulnerabilities of LLMs. This section
will focus on the introduction of lifecycle stages, and the detailed discussions about
vulnerabilities will appear in Section 3. The offline model construction is formed of
three steps [365]: pre-training, adaptation tuning, and utilisation improvement, such
that each step includes several interleaving sub-steps. In general, the pre-training step
is similar to the usual machine learning training that goes through data collection, ar-
chitecture selection, and training. On adaptation tuning, it might conduct instruction
tuning [222] to learn from task instructions, and alignment tuning [241, 83] to make
sure LLMs are aligned with human values, e.g., fair, honest, and harmless. Beyond
this, to improve the interaction with the end users, utilisation improvements may be
conducted through, for example, in-context learning [61] and chain-of-thought learn-
ing [322].
     Once an LLM is trained, an evaluation is needed to ensure that its performance
matches the expectation. Usually, we consider the evaluation from three perspec-
tives: evaluation on basic performance, safety analysis to evaluate the consequence
of applying the LLM in an application, and the evaluation through publicly available
benchmark datasets. The basic performance evaluation considers several basic types of
abilities such as language generation and complex reasoning. Safety analysis is to un-
derstand the impacts of human alignment, interaction with external environment, and
incorporation of LLMs into broader applications such as search engines. On top of
these, benchmark datasets and publicly available tools are used as well to support the
evaluation. The evaluation will determine if the LLM is acceptable (for pre-specified
criteria), and if so, the process will move forward to the deployment stage. Otherwise,
at least one failure will be identified, and the process will move back to either of the
three training steps.
     On the deployment stage, we will determine how the LLM will be used. For exam-
ple, it could be available in a web platform for direct interaction with end users, such
as the ChatGPT1 . Alternatively, it may be embedded into a search engine, such as the
new Bing2 . Nevertheless, according to the common practice, a guardrail is imposed
on the conversations between LLMs and end users to ensure that the AI regulation is
maximally implemented.
     In Figure 2, within the LLMs lifecycle, three main issues run through: performance
issues, sustainability issues, and unintended bugs. These may be caused by one or more
stages in the lifecycle. The red block shows that vulnerabilities appear in the LLMs
lifecycle, and they may appear in the early stage of the whole period. For example,
backdoor attacks and poisoning can contaminate raw data. When LLMs are deployed,
  1 https://openai.com/blog/ChatGPT
  2 https://www.bing.com/new




                                           8
         Backdoor
                                                           LLMs Lifecycle
                                ⚠ Performance Issues     ⚠ Sustainability Issues      ⚠ Unintended Bugs



                               Adaptation          Utilisation                                                                   End
        Pre-Training                                                     Evaluation         Deployment            Guardrail
                                Tuning           Improvement                                                                    Users


                                                                                                                Unauthorised
           Data                Instruction                                 Basic                                 Disclosure
                                                  In-Context                                  Chatbot
         Collection              Tuning                                 Performance
                                                                                                                 Robustness
        Architecture           Alignment           Chain-of-               Safety            w/ Search              Gap
         Selection              Tuning             Thought                Analysis            Engine
                                                                                                                   Privacy
                                                                                                                  Leakage
          Training             Poisoning                                Benchmarks              …
                                                                                                               Disinformation


                       Pre-training stage        Offline stages             Online stages           Vulnerabilities



               Figure 3: Large Language Models: Lifecycle and Vulnerabilities.


problems such as a robustness gap may also arise.

2.3      Key Techniques Relevant to Safety and Trustworthiness
In the following, we discuss two fundamental techniques that are distinct from the
usual deep learning models and have been used by e.g., ChatGPT to improve safety
and trustworthiness: reinforcement learning from human feedback and guardrails.

2.3.1      Reinforcement learning from human feedback (RLHF)
RLHF can be conducted in any stage of the “Adapation Tuning”, “Utilisation Improve-
ment”, or “Evaluation” in the framework of Figure 3. RLHF [84, 241, 41, 42, 43,
240, 192, 374] plays a crucial role in the training of language models, as it allows
the model to learn from human guidance and avoid generating harmful content. In
essence, RLHF assists in aligning language models with safety considerations through
fine-tuning with human feedback. OpenAI initially introduced the concept of incorpo-
rating human feedback to tackle complex reinforcement learning tasks in [84], which
subsequently facilitated the development of more sophisticated LLMs, from Instruct-
GPT [241] to GPT4 [240]. According to InstructGPT [241], the RLHF training process
typically begins by learning a reward function intended to reflect what humans value in
the task, utilising human feedback on the model’s outputs. Subsequently, the language
model is optimised via an RL algorithm, such as PPO [277], using the learned reward
function. Reward model training and fine-tuning with RL can be iterated continuously.
More comparison data is collected on the current best policy, which is used to train a
new reward model and policy. The InstructGPT models demonstrated enhancements
in truthfulness and reductions in generating toxic outputs while maintaining minimal
performance regressions on public NLP datasets.
    Following InstructGPT, Red Teaming language models [42] introduces a harm-
lessness preference model to help RLHF to get less harmful agents. The comparison


                                                                    9
data from red team attacks is used as the training data to develop the harmlessness
preference model. The authors of [41] utilised the helpful and harmless datasets in
preference modelling and RLHF to fine-tune LLMs. They discovered that there was a
significant tension between helpfulness and harmlessness. Experiments showed help-
fulness and harmlessness model is significantly more harmless than the model trained
only on helpfulness data. They also found that alignment with RLHF has many bene-
fits and no cost to performance, like combining alignment training with programming
ability and summarisation. The authors of [120] found that LLMs trained with RLHF
have the capability for moral self-correction. They believe that the models can learn
intricate normative concepts such as stereotyping, bias, and discrimination that pertain
to harm. Constitutional AI [43] trains the preference model by relying solely on AI
feedback, without requiring human labels to identify harmful outputs. To push the pro-
cess of aligning LLMs with RLHF, an open-sourced modular library, RL4LMs, and
evaluation benchmark, GRUE, designed for optimising language generator with RL
are introduced in [257]. Inspired by the success of RLHF in language-related domains,
fine-tuning approaches that utilise human feedback to improve text-to-image models
[196, 340, 335] have gained popularity as well. To achieve human-robot coexistence,
the authors of [134] proposed a human-centred robot RL framework consisting of safe
exploration, safety value alignment, and safe collaboration. They discussed the im-
portance of interactive behaviours and four potential challenges within human-robot
interactive procedures. Although many works indicate that RLHF could decrease the
toxicity of generations from LLMs, the induced RLHF, like introducing malicious ex-
amples by annotators [68], may cause catastrophic performance and risks. We hope
better techniques that lead to transparency, safe and trustworthy RLHF will be devel-
oped in the coming future.

2.3.2    Guardrails
Considering that some LLMs are interacting directly with end-users, it is necessary to
put a layer of protection, called guardrail, when the end users ask for information about
violence, profanity, criminal behaviours, race, or other unsavoury topics. Guardrails are
deployed in most, if not all, LLMs, including ChatGPT, Claude, and LLaMA. In such
cases, a response is provided with the LLM refusing to provide information. While
this is a very thin layer of protection because there are many tricks (such as prompt
injections that will be reviewed in Section 5.1) to circumvent it, it enhances the social
responsibility of LLMs.


3       Vulnerabilities, Attacks, and Limitations
This section presents a review of the known types of vulnerabilities. The vulnerabili-
ties can be categorised into inherent issues, intended attacks, and unintended bugs, as
illustrated in Figure 4.
    Inherent issues are vulnerabilities that cannot be readily solved by the LLMs them-
selves. However, they can be gradually improved with, e.g., more data and novel
training methods. Inherent issues include performance weaknesses, which are those


                                           10
                        Figure 4: Taxonomy of Vulnerabilities.


aspects that LLMs have not reached the human-level intelligence, and sustainability is-
sues, which are because the size of LLMs is significantly larger than the usual machine
learning models. Their training and daily execution can have non-negligible sustain-
ability implications. Moreover, trustworthiness and responsibility issues are inherent
to the LLMs.
    Attacks are initiated by malicious attackers, which attempt to implement their goals
by attacking certain stages in the LLMs lifecycle. Known intended attacks include ro-
bustness gap, backdoor attack, poisoning, disinformation, privacy leakage, and unau-
thorised disclosure of information.
    Finally, with the integration of LLMs into broader applications, there will be more
and more unintended bugs that are made by the developers unconsciously but have
serious consequences, such as bias and discrimination (that are usually related to the
quality of training data), and the recently reported incidental exposure of user informa-
tion. We separate these from inherent issues, because they could be resolved with e.g.,
high quality training data, carefully designed API, and so on. They are “unintended”,
because they are not deliberately designed by the developers.
    Figure 3 suggests how the vulnerabilities may be exploited in the lifecycle of LLMs.
While inherent issues and unintended bugs may appear in any stage of the lifecycle,
the attacks usually appear in particular stages of the lifecycle. For example, a back-
door attack usually occurs in pre-training and adaptation tuning, in which the backdoor
trigger is embedded, and poisoning usually happens in training or alignment tuning,
when the LLMs acquires information/data from the environment. Besides, many at-
tacks occur upon the interaction between end users and the LLMs using specific, well-
designed prompts to retrieve information from the LLMs. We remark that, while there
are overlapping, LLMs and usual deep learning models (such as convolutional neural
networks or object detectors) have slightly different vulnerabilities, and while initia-
tives have been taken on developing specification languages for usual deep learning
models [51, 162], such efforts may need to be extended to LLMs.

3.1     Inherent Issues
3.1.1   Performance Issues
Unlike traditional software systems, which run according to the rules that can be de-
terministically verified, neural network-based deep learning systems, including large-


                                           11
scale LLMs, have their behaviours determined by the complex models learned from
data through optimisation algorithms. It is unlikely that an LLM performs 100% cor-
rectly. As a simple example shown in Table 1, it can be observed that similar errors
exist across different LLMs, where most of the existing LLMs are not able to provide
a correct answer. Performance issues related to the correctness of the outputs include
at least the following two categories: factual errors and reasoning errors.

Table 1: Performance error exists across different LLMs. Retrieved 24 August 2023.

  LLMs              Output for question: "Adam’s wife is Eve. Adam’s daughter is Alice. Who is Alice to Eve?"

  ChatGPT [23]                                    Alice is Eve’s granddaughter.
  ERNIE Bot [346]                                 Alice is Eve’s granddaughter.
  Llama2 [306]                                    Alice is Eve’s granddaughter.
  Bing Chat [229]                      Alice is Adam’s daughter and Eve’s granddaughter.
  GPT-4 [240]                                        Alice is Eve’s daughter.




3.1.1.1 Factual errors Factual errors refer to situations where the output of an
LLM contradicts the truth, where some literature refers this situation as hallucination
[240][365][203]. For example, when asked to provide information about the expertise
in the computer science department at the University of Liverpool, the ChatGPT refers
to people who were never affiliated with the department. Hence more serious errors
can be generated, including notably wrong medical advice. Additionally, it is interest-
ing to note that while LLMs can perform across different domains, their reliability may
vary across domains. For example, the authors of [282] show that ChatGPT signifi-
cantly under-performs in law and science questions. Investigating if this is related to
the training dataset or training mechanism will be interesting.

3.1.1.2 Reasoning errors It has been discovered that, when given calculation or
logic reasoning questions, ChatGPT may not always provide correct answers. This is
mainly because, instead of actual reasoning, LLMs fit the questions with prior experi-
ence learned from the training data. If the statements of the questions are close to those
in the training data, it will give correct answers with a higher probability. Otherwise,
with carefully crafted prompt sequence, wrong answers can be witnessed [214, 118].

3.1.2    Sustainability Issues
Sustainability issues, which are measured with, e.g., economic cost, energy consump-
tion, and carbon dioxide emission, are also inherent to the LLMs. While excellent
performance, LLMs require high costs and consumption in all the activities in its life-
cycle. Notably, ChatGPT was trained with 30k A100 GPUs (each one is priced at
around $10k), and every month’s energy consumption cost at around $1.5M.
     In Table 2, we summarise the hardware costs and energy consumption from the
literature for a set of LLMs with varied parameter sizes and training dataset sizes.


                                                    12
Moreover, the carbon dioxide emission can be estimated with the following formula:
            tCO2 eq “ 0.385 ˆ GPUh ˆ pGPU power consumptionq ˆ PUE                   (1)
where GPUh is the GPU hours, GPU power consumption is the energy consumption
as provided in Table 1, and PUE is the Power Usage Effectiveness (commonly set as a
constant 1.1). Precisely, it has been estimated that training a GPT-3 model consumed
1,287 MWh, which emitted 552 (“ 1287 ˆ 0.385 ˆ 1.114) tons of CO2 [245].
    In the realm of technological advancements, the energy implications of various in-
novations have become a focal point of discussion. Consider the energy footprint of
training large language models (LLMs) like GPT-4. The energy required to train such
a model ranges between 51,772 to 62,318 MWh [3, 2]. To put this into perspective,
this is roughly 0.05% of Bitcoin’s energy consumption in 2021, which was estimated
at a staggering 108 TWh [93, 1]. Two remarks on this comparison: (i) the energy cost
of training LLMs is minuscule when juxtaposed with the colossal energy demands of
other technologies such as cryptocurrency mining, and (ii) the energy consumption of
LLMs is primarily associated with their training phases (one-time cost), whereas their
inference is considerably more energy-efficient. In contrast, cryptocurrency mining
consumes energy both in the creation of new coins and the validation of transactions,
continuously, as long as the network is active. This continuous energy drain under-
scores the vast difference in the sustainability profiles of these two technologies.

3.1.3   Other Inherent Trustworthiness and Responsibility Issues
Some issues occur during the lifecycle that could lead to concerns about the trust-
worthiness and responsibilities of LLMs. Generally, these can be grouped into two
sub-classes concerning the training data and the final model.
    For the training data, there are issues around the copyright [184], quality, and pri-
vacy of the training data. There is a significant difference between LLMs and other
ML models regarding the data being used for training. In the latter case, specific (well-
known/-structured) datasets are usually used in the training process. Ideally, these
datasets are properly pre-processed, anonymised, etc.; if needed, users have also given
consent about using of their data. It is well known that ChatGPT crawls the internet and
uses the gathered data to train. On the other hand, for LLMs, the data used for training
needs to be more understood. In most cases, users have not provided any consent; most
likely they are even unaware that their data contain personal information and that their
data have been crawled and used in LLM training. This makes ChatGPT, and LLMs
in general, privacy-nightmare to deal with and opens the door to many privacy leakage
attacks. Even the model owners would need to determine the extent of private risk their
model could pose.
    For the final model, significant concerns include, e.g., LLMs’ capability of inde-
pendent and conscious thinking [144], LLMs’ ability to be used to mimic human output
including academic works [195], use of LLMs to engage scammers in automatised and
pointless communications for wasting time and resources [66], use of LLMs in gener-
ating malware [127, 236, 59], etc. Similar issues can also be seen in image synthesis
tools such as DALL-2, where inaccuracies, misleading information, unanticipated fea-
tures, and reproducibility have been witnessed when generating maps in cartography


                                           13
      Model                                    Parameter size (billions)              Dataset sizea                          Hardware                                Energy
      BERT-base [97]                                    0.11                           3.3B words                          16 TPU chips                                 -
      BERT-large [97]                                   0.34                           3.3B words                          64 TPU chips                                 -
      GPT-3 [62]                                         175                          499B tokens                      10,000 NVIDIA V100                          1287 MWh
      Megatron Turing NLG [289]                          530                         338.6B tokens                  4480 NVIDIA A100-80GB                          >900MWh
      ERNIE 3.0 [296]                                    260                       4 TB/ 375B tokens                 384 NVIDIA V100 GPU                                -
      GLaM [102]                                        1200                           1.6T tokens                     1,024 Cloud TPU-V4                           456MWh
      Gopher [255]                                       280                          300B tokens                          4096 TPUv3                              1066 MWh
      PanGu-α [356]                                      200                     1.1 TB/ 258.5B tokens            2048 Ascend 910 AI processors                         -
      LaMDA [304]                                        137                     1.56 TB/ 2.81T tokens                     1024 TPU-v3                              451MWh
      GPT-NeoX [56]                                       20                             825 GB                   96 NVIDIA A100-SXM4-40GB                         43.92MWh
      Chinchilla [145]                                    70                           1.4T tokens                        TPUv3/TPUv4                                   -
      PaLM [82]                                          540                          780B tokens                          6144 TPU v4                             „ 640MWh
      OPT [361]                                          175                          180B tokens                    992 NVIDIA A100-80GB                           324 MWh




14
      YaLM [342]                                         100                      1.7 TB/ 300B tokens                   800 NVIDIA A100                            „ 785MWh
      BLOOM [276]                                        176                     1.61 TB/ 350B tokens                384 NVIDIA A100 80GB                           433 MWh
      Galactica [301]                                    120                          450B tokens                    128 NVIDIA A100 80GB                               -
      AlexaTM [291]                                       20                            1T tokens                       128 NVIDIA A100                            „ 232MWh
      LLaMA [306]                                         65                           1.4T tokens                  2048 NVIDIA A100-80GB                           449 MWh
      GPT-4 [182, 107, 3, 2]                            1800                        1 PB/ 13T tokens                  „ 25000 NVIDIA A100                      „ 51772-62318 MWh
      Cerebras-GPT [100]                                  13                          260B tokens                        16 Cerebras CS-2                               -
      BloombergGPT [334]                                50.6                          569B tokens                    512 NVIDIA A100 40GB                          „ 325MWh
      PanGu-Σ [263]                                     1085                          329B tokens                  512 Ascend 910 accelerators                          -

                                                            Table 2: Costs of different large language models.
         a A “word" is a single distinct meaningful element of a sentence, e.g. “Hello world" has two words. A “token" can represent a whole word or a part of a word, depending

     on the tokenisation strategy used, e.g. “I’m fine" can be tokenised into three tokens: “I", “m" and “fine". File size(TB or GB) refers to the amount of storage space required
     to save the training data.
[180]. These call for not only the transparency of LLMs development but also the novel
technologies to verify and differentiate the real and LLMs’ works [308, 232]. The latter
is becoming a hot research topic with many (practical) initiatives such as [20, 17, 18]
whose effectiveness requires in-depth study [247]. These issues inherent to the LLMs,
as they are neither attacks nor unintended bugs.

3.2     Attacks
3.2.1   Unauthorised Disclosure and Privacy Concerns
For LLMs, it is known that by utilising, e.g., prompt injection [250] or prompt leak-
ing [21] (which will be discussed in Section 5.1), it is possible to disclose the sen-
sitive information of LLMs. For example, with a simple conversation [30], the new
Bing leaks its codename “Sydney” and enables the users to retrieve the prompt without
proper authentication.
     More importantly, privacy concerns also become a major issue for LLMs. First,
privacy attacks on convolutional neural networks, such as membership inference at-
tacks where the attacker can determine whether an input instance is in the training
dataset, have been adapted to work on diffusion models [105]. Second, an LLM may
store the conversations with the users, which already leads to concerns about privacy
leakage because users’ conversations may include sensitive information [32]. Chat-
GPT has mentioned in its privacy policy that the conversations will be used for training
unless the users explicitly opt out. Due to such concerns, Italy has reportedly banned
ChatGPT [4] in early 2023. Most recently, both articles [202] and [132] illustrate that
augmenting LLMs with retrieval and API calling capabilities (so-called Application-
Integrated LLMs) may induce even more severe privacy threats than ever before.

3.2.2   Robustness Gaps
An adversarial attack is an intentional effort to undermine the functionality of a DNN
by injecting distorted inputs that lead to the model’s failure. Multiple input pertur-
bations are proposed in NLP for adversarial attacks [262, 131], which can occur at
the character, word, or sentence level [79, 165, 67]. These perturbations may involve
deletion, insertion, swapping, flipping, substitution with synonyms, concatenation with
characters or words, or insertion of numeric or alphanumeric characters [209, 209, 108,
199]. For instance, in character level adversarial attacks, [49] introduces natural and
synthetic noise to input data, while [121, 204] identifies crucial words within a sen-
tence and perturbs them accordingly. Moreover, [147] demonstrates that inserting ad-
ditional periods or spaces between words can result in lower toxicity scores for the
perturbed words, as observed with the "Perspective" API developed by Google. For
word level adversarial attacks, they can be categorised into gradient-based [209, 274],
importance-based [164, 175], and replacement-based [39, 187, 249] strategies based on
the perturbation method employed. In addition, in sentence level adversarial attacks,
some attacks [171, 320] are created so that they do not impact the original label of the
input and can be incorporated as a concatenation in the original text. In such scenar-
ios, the expected behaviour from the model is to maintain the original output, and the


                                          15
attack can be deemed successful if the label/output of the model is altered. Another
approach [368] involves generating sentence-level adversaries using Generative Ad-
versarial Networks (GANs) [125], which produce outputs that are both grammatically
correct and semantically similar to the input text.
    As mentioned above, the robustness of small language models has been widely
studied. However, given the increasing popularity of LLMs in various applications,
evaluating their robustness has become paramount. For example, [282] suggests that
ChatGPT is vulnerable to adversarial examples, including the single-character change.
Moreover, [316] extensively evaluates the adversarial robustness of ChatGPT in natu-
ral language understanding tasks using the adversarial datasets AdvGLUE [313] and
ANLI [239]. The results indicate that ChatGPT surpasses all other models in all adver-
sarial classification tasks. However, despite its impressive performance, there is still
ample room for improvement, as its absolute performance is far from perfection. In
addition, when evaluating translation robustness, [174] finds ChatGPT does not per-
form as well as the commercial systems on translating biomedical abstracts or Reddit
comments but exhibits good results on spoken language translation. Moreover, [73]
finds that the ability of ChatGPT to provide reliable and robust cancer treatment rec-
ommendations falls short when compared to the guidelines set forth by the National
Comprehensive Cancer Network (NCCN). ChatGPT is a strong language model, but
there is still some space for robustness improvement, especially in certain areas.

3.2.3   Backdoor Attacks
The goal of a backdoor attack is to inject malicious knowledge into the LLMs through
either the training of poisoning data [75, 281, 89] or modification of model parameters
[189, 345]. Such injections should not compromise the model performance and must be
bypassed from the human inspection. The backdoor will be activated only when input
prompts to LLMs contain the trigger, and the compromised LLMs will behave mali-
ciously as the attacker expected. Backdoor attack on DL models is firstly introduced
on image classification tasks [136], in which the attacker can use a patch/watermark as
a trigger and train a backdoored model from scratch. However, LLMs are developed
for NLP tasks, and the approach of pre-training followed by fine-tuning has become a
prevalent method for constructing LLMs. This entails pre-training the models on vast
unannotated text corpora and fine-tuning them for particular downstream applications.
To consider the above characteristics of LLMs, the design of the backdoor trigger is
no longer a patch/watermark but a character, word or sentence. In addition, due to
the training cost of LLMs, a backdoor attack should consider a direct embedding of
the backdoor into pre-trained models, rather than relying on retraining. Finally, the
backdoor is not merely expressed to tie with a specific label due to the diversity of
downstream NLP applications.

3.2.3.1 Design of Backdoor Trigger Three categories of triggers are utilised to ex-
ecute the backdoor attack: BadChar (triggers at the character level), BadWord (triggers
at the word level), and BadSentence (triggers at the sentence level), with each con-
sisting of basic (non-semantic) and semantic-preserving patterns [75] . The BadChar
triggers are produced by modifying the spelling of words in various positions within


                                          16
the input and applying steganography techniques to ensure their invisibility. The Bad-
Word triggers involve selecting a word from the ML model’s dictionary, and increasing
their adaptability to different inputs. MixUp-based and Thesaurus-based triggers are
then proposed [75]. The BadSentence triggers are generated by inserting or substitut-
ing sub-sentences, with a fixed sentence chosen as the trigger. To preserve the original
content, Syntax-transfer [75] is employed to alter the underlying grammatical rules.
These three types of triggers allow the flexibility to tailor their attacks to different ap-
plications.
    Two new concealed backdoor attacks are introduced: the homograph and dynamic
sentence attacks [292]. The homograph attack uses a character-level trigger that em-
ploys visual spoofing homographs, effectively deceiving human inspectors. However,
for NLP systems that do not support Unicode homographs, the dynamic sentence back-
door attack is proposed [292], which employs language models to generate highly nat-
ural and fluent sentences to act as the backdoor trigger.

3.2.3.2 Backdoor Embedding Strategies [281] is the first to propose a backdoor
attack on pre-trained NLP models that do not require task-specific labels. Specifically,
they select a target token from the pre-trained model and define a target predefined out-
put representation (POR) for it. They then insert triggers into the clean text to generate
the poisoned text data. While mapping the triggers to the PORs using the poisoned
text data, they simultaneously use the clean pre-trained model as a reference, ensuring
that the backdoor target model maintains the normal usability of other token represen-
tations. After injecting the backdoor, all auxiliary structures are removed, resulting in
a backdoor model indistinguishable from a normal one in terms of model architecture
and outputs for clean inputs.
    A method called Restricted Inner Product Poison Learning (RIPPLe) [189] is in-
troduced to optimise the backdoor objective function in the presence of fine-tuning
dataset. They also propose an extension called Embedding Surgery to improve the
backdoor’s resilience to fine-tuning by replacing the embeddings of trigger keywords
with a new embedding associated with the target class. The authors validate their ap-
proach on several datasets and demonstrate that pre-trained models can be poisoned
even after fine-tuning on a clean dataset.

3.2.3.3 Expression of Backdoor In contrast to prior works that concentrate on
backdoor attacks in text classification tasks, the applicability of backdoor attacks is
investigated in more complex downstream NLP tasks such as toxic comment detec-
tion, Neural Machine Translation (NMT), and Question Answer (QA) [206] . By repli-
cating thoughtfully designed questions, users may receive a harmful response, such
as phishing or toxic content. In particular, a backdoored system can disregard toxic
comments by employing well-crafted triggers. Moreover, backdoored NMT systems
can be exploited by attackers to direct users towards unsafe actions such as redirection
to phishing pages. Additionally, Transformer-based QA systems, which aid in more
efficient information retrieval, can be susceptible to backdoor attacks.
    Considering the prevalence of LLMs in automatic code suggestion (i.e., GitHub
Copilot), the data poisoning based backdoor attack, called TROJANPUZZLE, is stud-


                                            17
ied for code-suggestion models [34]. TROJANPUZZLE produces poisoning data that
appears less suspicious by ensuring that certain potentially suspicious parts of the pay-
load are never present in the poisoned data. However, the induced model still proposes
the full payload when it completes code, especially outside of docstrings. This char-
acteristic makes TROJANPUZZLE resilient to dataset cleaning techniques that rely on
signatures to spot and remove suspicious patterns from the training data.
    The backdoor attack on LLMs for text-based image synthesis tasks is firstly in-
troduced in [292]. The authors employ a teacher-student approach to integrate the
backdoor into the pre-trained text encoder and demonstrate that when the input prompt
contains the backdoor trigger, e.g., the underlined Latin characters are replaced with the
Cyrillic trigger characters, the generation of images will follow a specific description
or include certain attributes.

3.2.4   Poisoning and Disinformation
Among various adversarial attacks against DNNs, poisoning attack is one of the most
significant and rising security concerns for technologies that rely on data, particularly
for models trained by enormous amounts of data acquired from diverse sources. Poi-
soning attacks attempt to manipulate some of the training data, which might lead the
model to generate wrong or biased outputs. As LLM are often fine-tuned based on
publicly accessible data [71, 63], which are from unreliable and un-trusted documents
or websites, the attacker can easily inject some adversaries into the training set of the
victim model. Microsoft released a chatbot called Tay on Twitter [198]. Still it was
forced to suspend activity after just one day because it was attacked by being taught to
express racist and hateful rhetoric. Gmail’s spam filter can be affected by simply in-
jecting corrupted data in the training mails set [65]. Consequently, some evil chatbots
might be designed to simulate people to spread disinformation or manipulate people,
resulting in a critical need to evaluate the robustness of LLMs against data poisoning.
    [235] demonstrates how the poisoning attack can render the spam filter useless. By
interfering with the training process, even if only 1% of the training dataset is manip-
ulated, the spam filter might be ineffective. The authors propose two attack methods,
one is an indiscriminate attack, and another is a targeted attack. The indiscriminate
attack sends spam emails that contain words commonly used in legitimate messages to
the victim, to force the victim to see more spam and more likely to mark a legitimate
email as spam. As for the target attack, the attacker will send training emails containing
words likely to be seen in the target email.
    With the increasing popularity of developing LLMs, researchers are becoming con-
cerned about using chatbots to spread information. Since these LLMs, such as Chat-
GPT, MidJourney, and Stable Diffusion, are trained on a vast amount of data collected
from the internet, monitoring the quality of data sources is challenging. A recent study
[68] introduced two poisoning attacks on various popular datasets acquired from web-
sites. The first attack involves manipulating the data viewed by the customer who
downloads the data to train the model. This takes advantage of the fact that the data ob-
served by the dataset administrator during collection can differ from the data retrieved
by the end user. Therefore, an attacker only needs to purchase a few domain names
to gain control of a small portion of the data in the overall data collection. Another


                                           18
attack involves modifying datasets containing periodic snapshots, such as Wikipedia.
The attacker can manipulate Wikipedia articles before they are included in the snap-
shot, resulting in the internet storing perturbed documents. Thus, a significant level of
uncertainty and risk is involved when people use these LLMs as search engines.

3.3     Unintended Bugs
3.3.1    Incidental Exposure of User Information
In addition to the above attacks that an attacker actively initiates, ChatGPT was re-
ported [6] to have a “chat history” bug that enabled the users to see from their Chat-
GPT sidebars previous chat histories from other users, and openAI recognised that this
chat history bug may have also potentially revealed personal data from the paid Chat-
GPT Plus subscribers. According to the official report from OpenAI [5], the same bug
may have caused inadvertent disclosure of payment-related information for 1.2% of
ChatGPT Plus subscribers. The bug was detected within the open-source Redis client
library, redis-py. This cannot be an isolated incident, and we are expecting to witness
more such “bugs” that could have severe security and privacy implications.

3.3.2    Bias and Discrimination
Similar to the usual machine learning algorithms, LLMs are trained from data, which
may include bias and discrimination. If not amplified, Such vulnerabilities will be
inherited by the LLMs. For example, Galactica, an LLM similar to ChatGPT trained
on 46 million text examples, was shut down by Meta after three days because it spewed
false and racist information [19]. A political compass test [271] reveals that ChatGPT
is biased towards progressive and libertarian views. In addition, ChatGPT has a self-
perception [271] of seeing itself as having the Myers-Briggs personality type ENFJ.


4       General Verification Framework
Figure 5 provides an illustration of the general verification framework that might work
with LLMs, by positioning the few categories of V&V techniques onto the lifecycle.
In the Evaluation stage, other than the activities that are currently conducted (as men-
tioned in Figure 3), we need to start with the falsification and evaluation techniques, in
parallel with the explanation techniques. Falsification and evaluation techniques pro-
vide diverse, yet non-exhaustive, methods to find failure cases and have a statistical
understanding about potential failures. Explanation techniques are to provide human-
understandable explanations to the output of a LLMs. While these two categories are in
parallel, they can interact, e.g., a failure case may require an explanation technique to
understand the root cause, and the explanation needs to differentiate between different
failure and non-failure cases. The verification techniques, which are usually high cost,
may be only required when the LLMs pass the first two categories.
    Finally, ethical principles and AI regulations are imposed throughout the lifecycle
to ensure the ethical use of LLMs.



                                           19
                                                          Ethical Use

                LLMs Lifecycle


                      Adaptation        Utilisation                                                                       End
 Pre-Training                                              Evaluation          Deployment            Guardrail
                       Tuning         Improvement                                                                        Users



                                                Falsification
                                                                      Explanation                Runtime Monitor
                                               and Evaluation


                                                           Verification


            Pre-training stage      Offline stages         Online stages            Verification and validation stages



        Figure 5: Large Language Models: Verification Framework in Lifecycle.




                                             Prompt Injection

  Falsification and                Comparison with Human Expert
     Evaluation                                 Benchmark

                                   Testing and Statistical Evaluation
                                                                                          Interval Bound Propagation

                                    White-box Verification of NLP                             Abstract Interpretation

                                          Blackbox Verification                              Randomised Smoothing
     Verification
                                        Robustness Evaluation

                                         Towards Small Models

                                     Monitoring Out-of-Distribution
      Runtime
                                            Monitoring Attacks
     Monitoring
                                      Monitoring Output Failures

                                              AI Regulations

  Regulation and                       Responsible AI Principles
   Ethical Use
                                        Educatioinal Challenges

                                   Transparency and Explainability


Figure 6: Taxonomy of Surveyed Verification and Validation Techniques for Large
Language Models.




                                                          20
    Figure 6 presents the taxonomy of verification and validation techniques we sur-
veyed in this paper that can be used for large language models. In the following sec-
tions, we will review these techniques in greater details.


5     Falsification and Evaluation
This section summarises the known methods for identifying and evaluating the vul-
nerabilities of LLM-based machine learning applications. Falsification and evaluation
requires a red team [64], which, instead of having annotators label pre-existing texts,
interacts with a model and actively finds examples that fail. The red team needs to be
consist of people of diverse backgrounds and concerning about different risks (benign
vs. malicious). We also discuss on how the methods can, and should, be adapted.

5.1   Prompt Injection
This section discusses using prompts to direct LLMs to generate outputs that do not
align with human values. This includes the generation of malware, violence instruction,
and so on. Conditional misdirection has been successfully applied which misdirects the
AI by creating a situation where a certain event needs to occur to avoid violence.
    Prompt injection for LLMs is not vastly distinct from other injection attacks com-
monly observed in information security. It arises from the concatenation of instructions
and data, rendering it arduous for the underlying engine to distinguish them. Conse-
quently, attackers can incorporate instructions into the data fields they manage and
compel the engine to carry out unforeseen actions. Within this comprehensive defi-
nition of injection attacks, prompt engineering work can be regarded as instructions
(analogous to a SQL query, for instance). At the same time, the input information
provided can be deemed as data.
    Several methods for mis-aligning LLMs via Prompt Injection (PI) attacks have been
successfully applied [8]. In these attacks, the adversary can prompt the LLM to gener-
ate malicious content or override the initial instructions and the filtering mechanisms.
Recent studies have demonstrated that these attacks are difficult to mitigate since cur-
rent state-of-the-art LLMs are programmed to follow instructions. Therefore, most
attacks were based on the assumption that the adversary can directly inject prompt
to the LLMs. For example, [250] reveals two kinds of threats by manipulating the
prompts. The first one is goal hijacking, aiming to divert the intended goal of the
original prompts towards a target goal, while prompt leaking endeavours to retrieve
information from private prompts.
    [179] explores the programmatic behaviour of LLMs, demonstrating that classical
security attacks such as obfuscation, code injection, and virtualisation can be used to
circumvent the defence mechanisms of LLMs. This further exhibits that instruction-
based LLMs can be misguided to generate natural and convincing personalised mali-
cious content by leveraging unnatural prompts. Moreover, [95] suggests that by assign-
ing ChatGPT a persona, say that of the boxer Muhammad Ali (with a prompt “Speak
like Muhammad Ali.”), the toxicity of generations can be significantly increased. [227]
develops a black-box framework for producing adversarial prompts for unstructured


                                          21
image and text generation. Employing a token space projection operator provides a
solution from mapping the continuous word embedding space into the discrete token
space, such that some black-box attacks method, like square attacks, can be applied to
explore adversarial prompts. Experimental results found that those adversarial prompts
encourage positive sentiments or increase the frequency of the targeted letter in the gen-
erated text. [327] also suggests the existence of a fundamental limitation on mitigating
such prompt injection to trigger undesirable behaviour, i.e., as long as the length of the
prompts can be increased, the behaviour has a positive probability to be exhibited.
     [202] claims that in the previous versions of ChatGPT, some personal private in-
formation could be successfully extracted via direct prompting. However, with the
improved guardrails, some behaviours have been well-protected in the March 2023
version of ChatGPT, where ChatGPT is aware of leaking privacy when direct prompts
are applied, it will tend to refuse to provide the answer that may contain private infor-
mation. Although some efforts have been conducted to prevent training data extraction
attacks with direct prompts, [202] illustrates that there is still a sideway to bypass
ChatGPT’s ethical modules. They propose a method named jailbreak to exploit tricky
prompts to set up user-created role plays to alter ChatGPT’s ego and programming re-
strictions, which allows it to answer users’ queries unethically. More recently, [132]
proposes a novel indirect prompt injection, which required the community to have
an urgent investigation and evaluation of current mitigation techniques against these
threats. When LLMs are integrated with other plugins or using its API calling, the
content retrieved from the Web (public source) may already be poisoned and contain
malicious prompts pre-injected and selected by adversaries, such that these prompts
can be indirectly used to control and direct the model. In other words, prompt injection
risks may occur not only in situations where adversaries explicitly prompt LLMs but
also among users, developers, and automated data processing systems.
     We also noticed that prompt injection, and techniques based on prompt injection to
work with the APIs of LLMs, have been used to generate malware [127, 236, 59].

5.2    Comparison with Human Experts
Another evaluation thread is to study how LLMs are compared with human experts.
For example, for ChatGPT, [139] conducts the comparison on questions from open-
domain, financial, medical, legal, and psychological areas, [112] compares on the bib-
liometric analysis, [225] evaluates on university education with a primary focus on
computer security-oriented specialisation, [170] considers the ranking of contents, and
[331] compares on the grammatical error correction (GEC) task. It is surprising to note
that, in all these comparisons, the conclusion is that, ChatGPT does not perform as
well as expected. One step further, to study collaboration rather than only focus on
comparisons, [252] explores how ChatGPT’s performance on safety analysis can be
compared with human experts, and concludes that the best results are from the close
collaboration between ChatGPT and the human experts. A similar conclusion was also
drawn by [167] when studying ChatGPT’s logically consistent behaviours.
    In some cases, LLMs can outperform human experts in specific tasks, like pro-
cessing enormous amounts of data or doing repeated activities with great accuracy.
For example, LLMs can be used to analyse massive numbers of medical records to


                                           22
uncover patterns and links between different illnesses, which can aid in medical di-
agnosis and therapy [221, 35]. On the other hand, human experts may outperform
LLMs in jobs requiring more complicated reasoning or comprehension of social and
cultural contexts. Human specialists, for example, may better interpret and respond
to delicate social signs in a conversation, which can be difficult for LLMs. It is im-
portant emphasising that LLMs are intended to supplement rather than replace human
competence [280]. LLMs can automate specific processes or help human professionals
accomplish things more efficiently and precisely [365]. For example, [252] studies how
ChatGPT’s performance on safety analysis can be compared with human experts and
concludes that the best results are from the close collaboration between ChatGPT and
the human experts. [146] also shows that huge language models have a lot of potential
as knowledgeable assistants collaborating with subject specialists.

5.3    Benchmarks
Benchmark datasets have been used to evaluate the performance of LLMs. For exam-
ple, in [316], AdvGLUE and ANLI benchmark datasets are used to assess adversarial
robustness, and Flipkart review and DDXPlus medical diagnosis datasets are used to
evaluate out-of-distribution evaluation. In [293], eight kinds of typical safety scenarios
and six types of more challenging instruction attacks are used to expose safety issues of
LLMs. In [118], the GHOSTS dataset is used to evaluate the mathematical capability
of ChatGPT.
    Regarding the LLMs as a software as a service, rather than previous deep learning
models, it becomes imperative to incorporate lifelong time assessment. In [70], they
evaluated the March 2023 and June 2023 versions of GPT-3.5 and GPT-4 on several di-
verse benchmarks. The LLM service’s behavior can undergo significant changes within
a fairly brief period, as evidenced by their findings. According to [109], it states that
while releasing the results of the benchmark, the providers should provide raw results,
not only high-level metrics. So that the inspector is capable of conducting a more thor-
ough examination of the model’s defects. Previous NLP works show that fine-tuning
pre-trained transformer-based language models such as BERT [97] is an unstable pro-
cess [101, 194]. During the continual updating of LLMs, it could go through multiple
iterations of finetune and RLHF, which even increases the risk of catastrophic forget-
ting. In [36], the challenge of ensuring fair model evaluation in the age of closed and
continuously trained models is discussed. Moreover, Low-Rank Adaptation (LoRA) is
proposed to reduce the trainable parameters and thus could avoid catastrophic forget-
ting [150].

5.4    Testing and Statistical Evaluation
As mentioned above, most existing techniques on the falsification and evaluation heav-
ily rely on human intelligence and therefore have a significant level of human involve-
ment. In red teaming, the red team must be creative in finding bad examples. In prompt
injection, the attacker needs to design specific (sequence of) prompts to retrieve the in-
formation they need. Unfortunately, human expertise and intelligence are expensive



                                           23
and scarce, which calls for automated techniques to have an intensive and fair evalu-
ation, and to find corner cases as exhaustive as possible. In the following, we discuss
how testing and statistical evaluation methods can be adapted for a fair evaluation of
LLMs.
    To simplify it, we assume an LLM is a system that generates an output given an
input. Let D be the space of nature data, an LLM is a function M : D Ñ D. In the
meantime, there is another function H : D Ñ D representing human’s response. For
an automated generation of test cases, we need to have an oracle O, a test coverage
metric C, and a test case generation method A. The oracle O determines if an input-
output pair px, yq is correct. The implementation of oracle is related to both M and
H, by checking whether given any input x their outputs Mpxq and Hpxq are similar
under certain criteria. We call an input-output pair a test case. Given a set of test cases
P “ tpxi , yi qui“1,...,n , an evaluation of the coverage metric C returns a probability value
representing the percentage of cases in P over the cases that should be tested. Finally,
the test case generation method A generates the set P of test cases. Usually, the design
of coverage metric C should be based on the property to be verified. Therefore, the
verification problem is reduced to determining of whether the percentage of test cases
in P that passes the oracle O is above a pre-specified threshold.
    Statistical evaluation applies statistical methods in order to gain insights into the
verification problem we are concerned about. In addition to the purpose of determining
the existence of failures (i.e., counterexamples to the satisfiability of desirable proper-
ties) in the deep learning model, statistical evaluation assesses the satisfiability of a
property in a probabilistic way, by, e.g., aggregating sampling results. The aggregated
evaluation result may have the probabilistic guarantee, e.g., the probability of failure
rate lower than a threshold l is greater than 1 ´ ε, for some small constant ε.
    While the study on LLMs is just started [260], statistical evaluation methods have
been proposed for the general machine learning models.
    Sampling methods and testing methods have been considered for convolutional
or recurrent neural networks. Sampling methods, such as [323], are to summarise
property-related statistics from the samples. There are many ways to determine how
the test cases are generated, including, e.g., fuzzing, coverage metrics [295, 155], sym-
bolic execution [128], concolic testing [297], etc. Testing methods, on the other hand,
generate a set of test cases and use the generated test cases to evaluate the reliabil-
ity (or other properties) of deep learning [294]. While sampling methods can have
probabilistic guarantees via, e.g., Chebyshev’s inequality, it is still under investigation
on associating test coverage metrics with probabilistic guarantees. Moreover, ensur-
ing that the generated or sampled test cases are realistic is necessary, i.e., on the data
distribution [156, 367].
    For LLMs, the key technical challenges are on the design of test coverage metrics
and the test case generation algorithms because (1) LLMs need to be considered in a
black-box manner, rather than white-box one; this is mainly due to the size of LLMs
that cannot be reasonably explored, and therefore an exploration on the input space will
become more practical; (2) LLMs are for natural language texts, and it is hard to define
the ordering between two texts; the ordering between two inputs are key to the design
of test case generation algorithms; and (3) LLMs are non-deterministic, i.e., different
outputs are expected in two tests with identical input.

                                             24
6       Verification
This section discusses if and how more rigorous verification can be extended to work
on LLM-based machine-learning tasks. So far, the verification or certification of LLMs
is still an emerging research area. This section will first provide a comprehensive
and systematic review of the verification techniques on various NLP models. Then,
we will discuss a few pioneering black-box verification methods that are workable on
large-scale language models. These are followed by a discussion on how to extend
these efforts towards LLMs and a review of the efforts to reduce the scale of LLMs to
increase the validity of verification techniques.
     We remark that, this section is focused on verifying LLMs. For the other direction
of utilising LLMs to support the verification, there are works related to e.g., spec-
ification autoformalisation [336], code generation [303], assertion generation [178],
zero-shot vulnerability repair [246].

6.1     Verification on Natural Language Processing Models
As discussed in previous sections, an attacker could generate millions of adversarial
examples by manipulating every word in a sentence. Adversarial examples have dif-
ferent safety and trustworthiness implications to the downstream tasks. For example,
a perturbed output text might include different emotions that will affect the sentiment
analysis, and it is possible that a perturbed text might have the same meaning but differ-
ent language style to affect the spam detection. However, such methods may still fail
to address numerous unseen cases arising from exponential combinations of different
words in a text input. To overcome these limitations, another class of techniques has
emerged, grounded in the concept of “certification” or “verification” [279, 161]. For
example, via certification or verification, these methods train the model to provide an
upper bound on the worst-case loss of perturbations, thereby offering a certificate of
robustness without necessitating the exploration of the adversarial space [287]. By util-
ising these certification-driven methods, we can better evaluate the model’s robustness
in the face of adversarial attacks [124].

6.1.1    Verification via Interval Bound Propagation
The first technique successfully adapted from the computer vision domain for verify-
ing NLP models is Interval Bound Propagation (IBP). It is a bounding technique that
has gained significant attention for its effectiveness in training large, robust, and verifi-
able neural networks [130]. By striving to minimise the upper bound on the maximum
difference between the classification boundary and input perturbation region, IBP al-
lows the incorporation of a loss term during training. This enables the minimisation
of the last layer of the perturbation region, ensuring it remains on one side of the clas-
sification boundary. As a result, the adversarial region becomes tighter and can be
considered certified robust. Notably, Jia et al. [172] proposed certified robust models
while providing maximum perturbations in text classification. The authors employed
interval bound propagation to optimise the upper bound over perturbations, providing
an upper bound over the discrete set of perturbations in the word vector space.


                                             25
                Figure 7: Pipeline for robustness verification in [350]


    Later on, Huang et al. [154] introduced a verification and verifiable training method
for neural networks in NLP, proposing a tighter over-approximation in the form of a
‘simplex’ in the embedding space for input perturbations. To make the network veri-
fiable, they defined the convex hull of all the original unperturbed inputs as a space of
delta perturbation. By employing the IBP algorithm, they generated robustness bounds
for each neural network layer. Furthermore, as shown in Figure 7, Ye et al. [350]
proposed structure-free certified robust models, which can be applied to any arbitrary
model, overcoming the limitations of IBP-based methods that are not applicable to
character-level and sub-word-level models. This work introduced a perturbation set of
words using synonym sets and top-K nearest neighbours under the cosine similarity
of GloVE vectors [249], which could subsequently generate sentence perturbations us-
ing word perturbations and train a provably robust classifier. Very recently, Wallace et
al. [312] highlighted the limitations of IBP-based methods in a broader range of NLP
tasks, demonstrating that IBP methods have poor generalisability. In this work, the
authors performed a systematic evaluation of various of sentiment analysis tasks. They
pointed out some insights regarding the promising improvements and adaptations for
IBP methods in the NLP domain.

6.1.2   Verification via Abstract Interpretation
Another popular verification technique applied to various NLP models is based on
abstract interpretation or functional over-approximation. The idea behind abstract in-
terpretation is to approximate the behaviour of a program by representing it using a
simpler model that is easier to analyse. Specifically, this technique can represent the
network using an abstract domain that captures the possible range of values the network
can output for a given input. This abstract domain can then be used to reason about
the network’s behaviour under different conditions, such as when the network is under
adversarial perturbation. One notable contribution in this area is POPQORN [185]. It
can find a certificate of robustness for RNN-based networks, which utilised 2D planes
to bound the cross-nonlinearity in Long Short-Term Memory (LSTM) networks so a
certificate within an l p ball can be located if the lower bound on the true label output
unit is larger than the upper bounds of all other output units. Later on, Cert-RNN [103]
introduced a robust certification framework for RNNs that overcomes the limitations
of POPQORN [185]. The framework maintains inter-variable correlation and accel-


                                           26
erates the non-linearities of RNNs for practical uses. This work utilised Zonotopes
[110] to encapsulate input perturbations. Cert-RNN can verify the properties of the
output Zonotopes to determine certifiable robustness. Using Zonotopes, as opposed to
boxes, allows improved precision and tighter bounds, leading to a significant speedup
compared to POPQORN.
    Recently, Abstractive Recursive Certification (ARC) was introduced to verify the
robustness of RNNs [363]. Using those transformations, ARC defined a set of pro-
grammatically perturbed string transformations and constructed a perturbation space.
By memorising the hidden states of strings in the perturbation space that share a com-
mon prefix, ARC can efficiently calculate an upper bound while avoiding redundant
hidden state computations. Roughly at the same time, Ryou et al. proposed a similar
method called Polyhedral Robustness Verifier (PROVER) [272]. PROVER can rep-
resent input perturbations as polyhedral to generate a certifiably verified network for
more general sequential data. To certify large transformers, DeepT was proposed by
Bonaert et al. [57]. It was specifically designed to verify the robustness of transformers
against synonym replacement-based attacks. DeepT employed multi-norm Zonotopes
to achieve larger robustness radii in the certification. For the transformers with self-
attention layers, Shi et al. [284] developed a verification algorithm that can provide a
lower bound to ensure the probability of the correct label is consistently higher than
that of the incorrect labels. This method can obtain a tighter bound than those obtained
from IBP-based methods.

6.1.3   Verification via Randomised Smoothing




Figure 8: Pipeline of wordDP for word-substitution attack and robustness verification
[318]

    Randomised smoothing (RS) [87] is another promising technique for verifying the
robustness of deep language models. Its basic idea is to leverage randomness during
inference to create a smoothed classifier that is more robust to small perturbations in
the input. This technique can also be used to give certified guarantees against adver-
sarial perturbations within a certain radius. Generally, randomized smoothing begins


                                           27
by training a regular neural network on a given dataset. Then, given a trained base
classifier f and an input x, the smoothed classifier g is defined using randomness (e.g.,
Gaussian noise) as: gpxq “ argmaxc Pp f px ` εq “ cq, where ε is the noise sampled
from some distribution (e.g., a Gaussian distribution). During the inference phase, to
classify a new sample, noise is randomly sampled from the predetermined distribution
multiple times. These instances of noise are then injected into the input x, resulting in
noisy samples. Subsequently, the base classifier f pxq generates predictions for each of
these noisy samples. The final prediction is determined by the class with the highest
frequency of predictions, thereby shaping the smoothed classifier gpxq. To certify the
robustness of the smoothed classifier gpxq against adversarial perturbations within a
specific radius r centered around the input x, RS calculates the likelihood of agreement
between the base classifier f pxq and gpxq when noise is introduced to x. If this likeli-
hood exceeds a certain threshold (e.g., surpassing 0.5 ` τ, where τ represents a minor
positive constant), it indicates the certified robustness of gpxq within a radius r around
x.
    Figure 8 depicts one of the pioneering efforts of using RS for verifying the robust-
ness of NLP models. It is called WordDP developed by Wang et al. [318], the authors
introduced a novel approach to provide a certificate of robustness by leveraging the
concept of differential privacy. In this work, the researchers considered a sentence
as a database and the individual words within it as records. They demonstrated that
if a predictive model satisfies a specific threshold of epsilon-differential privacy for
a perturbed input, it can be inferred that the input is identical to the clean, unaltered
data. This methodology offers a certification of robustness against L-adversary word
substitution attacks. In another recent study, Zeng et al. [354] introduced RanMASK,
a certifiably robust defence method against text adversarial attacks, which employs
a novel randomised smoothing technique specifically tailored for NLP models. The
input text is manually perturbed in this approach and subsequently fed into a mask
language model. Random masks are then generated within the input text to create a
large set of masked copies, which are subsequently classified by a base classifier. A
"majority vote" mechanism determines the final robust classification. Furthermore, the
researchers utilised pre-trained models such as BERT and RoBERTa to generate and
train with the masked inputs, showcasing the practical applicability and effectiveness
of the RanMASK technique in some real-world NLP scenarios.

6.2    Black-box Verification
Many existing verification techniques impose specific requirements on DNNs, such as
targeting a specific network category or networks with particular activation functions
[161]. With the increasing complexity and scale of large language models (LLMs),
traditional verification methods based on layer-by-layer search, abstraction, and trans-
formation have become computationally impractical. Consequently, we envision that
black-box approaches have emerged as a more feasible alternative for verifying such
models [326, 333, 341].
    In the black-box setting, adversaries can only query the target classifier without
knowing the underlying model or the feature representations of inputs. Several studies
have explored more efficient methods for black-box settings, although most of current


                                           28
approaches focus on vision models [326, 333, 341]. For instance, DeepGO, a reach-
ability analysis tool, offers provable guarantees for neural networks with deep layers
and nonlinear activation functions [267]. Its extended version, DeepAgn, is compatible
with various networks, including feedforward and recurrent neural networks, as long
as they exhibit Lipschitz continuity [358].
     Subsequently, an anytime algorithm was developed to approximate global robust-
ness by iteratively computing lower and upper bounds [268]. This algorithm returns
intermediate bounds and robustness estimates that improve as computation proceeds.
For neural network control systems (NNCSs), the DeepNNC verification framework
utilises a black-box optimisation algorithm and demonstrates comparable efficiency
and accuracy across a wide range of neural network controllers [359]. GeoRobust, an-
other black-box analyser, efficiently verifies the robustness of large-scale DNNs against
geometric transformations [314]. This method can identify the worst-case manipula-
tion that minimises adversarial loss without knowledge of the target model’s internal
structures and has been employed to systematically benchmark the geometric robust-
ness of popular ImageNet classifiers.
     Recently, some researchers have attempted to develop black-box verification meth-
ods for NLP models, although these methods are not scalable to LLMs. For example,
one study introduced a framework for evaluating the robustness of NLP models against
word substitutions [190]. By computing a lower and upper bound for the maximal
safe radius for a given input text, this verification method can guarantee that the model
prediction does not change if a word is replaced with a plausible alternative, such as a
synonym.

                                                                               A1: John can read 4 books a day. There are 7
                                Forward Reasoning                              days in a week. So in 6 weeks, he can read 6       Candidate
                                                                               * 7 * 4 = 168 books. The answer is 168.            Conclusion
                 ......                                                       ...
                 Q: John can read 4 books a day. John reads
                                                                    LLM        AK: John reads 4 books a day. He reads every
                 every Monday and Tuesday. How many books
                                                                               Monday and Tuesday. So that is 2 days a
                 would John read in 6 weeks?                                   week. So he reads 4 x 2 = 8 books a week. In
                                                                               6 weeks, he will read 8 x 6 = 48 books. The
                                                                               answer is 48.
                                      Verifier




           Stage 1
           Stage 2
                               Backward Verification             Verified
                                                                 Conclusion
 Conditional    ......                                                         A: John can read X books a day. He reads           Verification Score

                                                                      A1       every Monday and Tuesday. So he reads 2                    0
 Mask
                Q: “John can read ‘X’ books a day. John reads
                                                                      LLM      days a week. 168 books in 6 weeks. 168 / 6
                every Monday and Tuesday. John would read 168
 Conclusion                                                                    = 28 books a week. X × 2 = 28 books a day. X
 As Conditional books in 6 weeks.” What is the answer of 'X'?
                                                                               = 14. The answer is 14.
               ...
                                                                                                                               Verification Score
                                                                               A: John can read X books a day. He reads
                 ......                                                        every Monday and Tuesday. So he reads 2
                                                                      AK                                                               4
                 Q: “John can read ‘X’ books a day. John reads                 days a week. He reads 48 books in 6 weeks.
                                                                      LLM
                 every Monday and Tuesday. John would read 48                  So 48 / 6 = 8 books a week. X × 2 = 8 books
                 books in 6 weeks.” What is the answer of 'X'?                 a week. X = 4. The answer is 4. ✔
                                                                                                                    ✔
                                                                                                                           Answer     AK: 48
                                                                                                                    ✔✔



Figure 9: Example of Self-Verification proposed in [324]. In Stage-1, LLM gener-
ates some candidate conclusions. Then LLM verifies these conclusions and counts the
number of masked conditions that reasoning is correct to as the verification score in
Stage-2.


                                                                   29
    We also notice another thread of works focusing on training verifiers, for the cor-
rectness of language-to-code generation [237] or solving math word problems [86].

6.3   Robustness Evaluation on LLMs
Given the prominence of large-scale language models such as GPT, LLaMA, and
BERT, some researchers have recently started exploring the robustness evaluation of
these models. One such investigation is the work of Cheng et al. [78], who developed
a seq2seq algorithm based on a projected gradient method combined with group lasso
and gradient regularisation. To address the challenges posed by the vast output space of
LLMs, the authors introduced innovative loss functions to conduct non-overlapping and
targeted keyword attacks. Through applications in machine translation and text sum-
marisation tasks, their seq2seq model demonstrated the capability to produce desired
outputs with high success rates by altering fewer than three words. The preservation
of semantic meanings in the generated adversarial examples was further verified using
an external sentiment classifier. Another notable contribution comes from Weng et al.
[324, 325], as shown in Figure 9. They proposed a self-verification method that lever-
ages the conclusion of the chain of thought (CoT) as a condition for constructing a new
sample. The LLM is then tasked with re-predicting the original conditions, which have
been masked. This approach allows for the calculation of an explainable verification
score based on accuracy, providing valuable insights into the performance of LLMs. Fi-
nally, Jiang et al. [173] introduced an approach that addresses both auto-formalisation
(the translation of informal mathematics into formal logical notation) and the proving
of "proof sketches" resulting from the auto-formalisation of informal proofs.
    To the best of our knowledge, there remains a conspicuous absence of research
on verifying large language models (LLMs). As such, we encourage the academic
community to prioritise this vital research domain by developing practical black-box
verification methods tailored specifically to LLMs.

6.4   Towards Smaller Models
The current LLMs are of large scale with billions or trillions of parameters. This will
make the verification hard, even with the above-mentioned verification techniques. An-
other possible thread of research to support the ultimate verification is to use smaller
LLMs.
     A prevailing strategy of developing a smaller LLM is to apply techniques that re-
duce the parameters of a pre-trained model. One typical method is model compres-
sion, such as quantisation [234, 220, 116]. However, directly applying quantisation
techniques on LLMs leads to performance degradation. To this end, ZeroQuant [349]
utilise kernel fusion [315] to compress weights and activations before data movement,
to maximise memory bandwidth utilisation and speed up inference. Similarly, [244] in-
troduces a new LUT-GEMM kernel that allows quantised matrix multiplications with
either uniform or non-uniform weight quantisation. Both [315, 244] require custom
CUDA kernels. In contrast, [96] improves predictive performance on billion-scale 8-bit
transformers. [117] further improves GPT model with near-zero performance drop on 3
or 4-bit precision by deploying Optimal Brain Quantisation [116], Lazy Batch-Updates


                                          30
and Cholesky Reformulation. Other than quantisation techniques, Low-rank adaptation
(LORA) [151] involves decomposing the weights into low-rank matrices, which has
been shown to reduce the number of parameters while maintaining model performance
significantly. Knowledge distillation refers to the methodology wherein a “student”
model is trained to approximate the predictive behavior of a more complex “teacher”
model [143, 129]. In LLMs, for efficient training, the small student model is often used
to assimilate information from the pre-trained teacher model [300, 80, 332, 248, 137].
The knowledge transfer allows the student model to augment its capabilities in lan-
guage understanding and generation, which particularly advantageous for deployment
in computational environments where resource efficiency is a critical consideration.
    It is worth noting that Spiking Neural Networks (SNNs), as the third generation
neural networks, offer a complementary approach to improve computing efficiency,
e.g., utilising sparse operation [270, 330, 329]. Recent research has introduced SpikeGPT
[373], the largest SNN-based model with 260 million parameters, to demonstrate the
performance of SNNs on GPT models, comparable to that of traditional neural net-
works. In contrast, SNNs require implementation on specialised hardware, such as
neuromorphic chips like TrueNorth [37] and Loihi [91], which have been designed to
mimic biological neurons at the circuit level. While the development of SNNs on LLM
is still in its early stages, it presents an alternative approach to achieving computing
efficiency that works parallel to compression techniques.


7    Runtime Monitor
Guardrails mentioned in Section 2.3.2 provide a safeguard for the LLMs to interact
with the end users while retaining its social responsibility. This section discusses a
V&V method, i.e., runtime monitor, that is somewhat similar to the guardrails in that,
it provides the safeguards on the behaviour of the LLMs against vulnerabilities such
as those discussed in Section 3. The key motivation for using runtime monitors, rather
than the verification, is two-fold. First, verification methods require significant com-
putation and hence can become impractical when dealing with large models such as
LLMs. Second, a deep learning model might be applied to scenarios different from
where the training data is collected. These suggest the need for a runtime monitor to
determine the satisfiability of a specification on the fly.
    Similar to evaluation and verification, there is no existing work on LLMs, but there
are proposals for e.g., the convolutional neural networks. Given the missing speci-
fications (although the attempts to formalise specifications started [51, 45, 162]), the
current runtime monitoring methods for deep learning start from constructing an ab-
straction of a property, followed by determining the failure of the property by checking
the distance between the abstraction and the original learning model. There are a few
existing methods for abstraction of deep learning. For example, in [76], a Boolean
abstraction on the ReLU activation pattern of some specific layer is considered and
monitored. Conversely of Boolean abstraction, [142] consider box abstractions. In
[54], a Bayesian network based abstraction, which abstracts hidden features as random
variables, is considered.
    The construction of a runtime monitor requires the specification of the failures.


                                          31
Other than direct specifications such as [162], which requires additional efforts to con-
vert the formulas into runtime monitors, this can usually be done by collecting a set of
failure data and then summarising (through either learning or symbolic reasoning or a
combination of them) the relation between failure data and the part of the LLMs to be
monitored, e.g., some critical layers of the LLMs or the output [208, 77].

7.1    Monitoring Out-Of-Distribution
In the following, we discuss how runtime monitoring techniques have been developed
for a specific type of failure, i.e., out of distribution, which suggests that the runtime
data is on a different distribution from the training data. It is commonly believed that
ML models cannot be reliable when working with data drifted from the training data.
Therefore the occurrence of out-of-distribution suggests the existence of risks.
     Neural networks, used in computer vision (CV) or natural language process (NLP)
tasks, are known to make overconfident predictions on out-of-distribution (OoD) sam-
ples that do not belong to any of the training classes, i.e., in-distribution (ID) data. For
security reasons, such inputs and their corresponding predictions must be monitored
at runtime, especially for networks deployed in safety-critical applications. Runtime
monitoring or detection of out-of-distribution (OoD) samples have been extensively
studied in CV [140, 99, 210, 261, 216, 344]. Recently, researchers have paid more
attention to this problem for NLP models [141], although large-scale language models
(ChatGPT) have shown continuous improvement on most adversarial and OoD clas-
sification tasks [317]. Generally, to monitor OoD samples, one has to devise an ID
confidence score function Spxq such that an input x is classified as OoD if the value
Spxq is less than a predefined threshold γ, as shown in Equation 2.
                                       "
                                           ID      if Spxq ě γ
                              Mpxq “                                                     (2)
                                           OoD otherwise

    According to what information is used to construct this confidence function Spxq,
the current OoD monitoring methods for NLP models [40, 153, 72, 81, 104, 74] can be
roughly divided into the following three categories.
    The first category includes input density estimation methods [261, 197, 119, 40].
These methods usually involve a density estimator, either directly in the input space or
in the latent space of the generative models for the ID data. The probability value of
the input given by such a density estimator can be used as the ID score. One of these
examples is [40] that uses the token perplexity [197], avoiding the bias of text length as
the ID confidence score.
    The second category includes feature or embedding space approximation methods
[338, 251, 357, 371, 72, 372]. These methods first approximate the seen features by
some distribution function, and then use the distance (e.g., Euclidean and Mahalanobis
distances) between this distribution and the input feature as the ID confidence score.
For instance, [72] extracts holistic sentence vector embeddings from all intermediate
layers and shadow states of all tokens to enhance the general semantics in sentence
vectors, thereby improving the performance of OoD text detection algorithms based on
feature space distance.


                                            32
    The third category includes output confidence calibration methods [141, 94, 90,
207, 283, 352]. These methods use the model’s prediction confidence (usually cali-
brated) as the ID score. The classic is the maximum softmax probability, often used as
a strong baseline for OoD detection.
    Despite a lot of work and effort, the current results can still be improved. Moreover,
no single method is better than the other at present, which is understandable, given the
infinity of OoD data and the ambiguous boundaries of ID data. In terms of perfor-
mance, the methods mentioned above do not entail significant overhead, as they all
involve a single computation of a function related to high-dimensional vectors, which
can be accomplished within a short timeframe. When compared to the time required
for a single inference of a neural network, this overhead can be considered negligible.
    Finally, we remark that OoD detection task in the field of NLP still requires greater
efforts in the following two aspects. First, the community ought to reach a consensus
on a fine-grained definition of the OoD problem for NLP models, by precisely con-
sidering the sources of OoD data and the tasks of NLP models. For example, existing
work is done on NLP classification tasks. How to define the OoD problem for the
generative NLP models, e.g., what kind of data should be called OoD data to these
generative models? Second, a fair evaluation method is needed, given the fact that the
training datasets for most large language models (LLM) are unavailable, i.e., it is un-
clear whether the used test dataset for evaluating OoD methods are OoD data to the
tested models or not.

7.2    Monitoring Attacks
In this subsection, we discuss how to detect adversarial and backdoor attacks in real-
time. It is possible to detect the backdoor input at runtime, given a set of clean reference
dataset. The runtime monitoring for backdoor attack is based on the observation that
although backdoor input and target samples from reference dataset are classified the
same by the compromised network, the rationale for this classification is different. The
network identifies input features that it has learnt correlate to the target class in the
case of clean samples from the target class. It identifies features associated with the
backdoor trigger in the case of backdoor samples, causing it to identify the input as the
target class.
    Based on the above idea, several detection strategies for backdoor input are devel-
oped. Activation Clustering (AC) approach is adopted to check the activation similarity
between the runtime input and reference dataset [69]. The activations of last convolu-
tional layer are obtained for reference dataset and input. They are grouped according
to the label and each group is clustered separately. To cluster the activations, the di-
mensionality reduction technique, Independent Component Analysis (ICA) is applied.
Then cluster analysis methods, like exclusionary reclassification, relative size compar-
ison and silhouette score can help users identify if the input contains the backdoor
trigger. In addition, the feature importance maps generated from XAI techniques can
be leveraged to help identify the backdoor input [158, 302]. Since the compromised
neural network relies on backdoor trigger to make decision, the backdoor trigger is
highlighted when generating the feature importance maps regarding the input. Then,
the backdoor input can be filtered out when simple and fixed decision logic is sum-


                                            33
marised from the explanations. While the runtime monitoring of backdoor for LLMs
is few, we believe the current techniques can be extended to LLMs once we can get the
hidden activation or explanations from LLMs.
     Adversarial examples are thought to exhibit distinguishable features that set them
apart from clean inputs [163]. Consequently, we can leverage this distinction to de-
velop a runtime robust detector. For example, uncertainty values are used as features
to build a binary classifier as a detector. Feinman et al. [114] introduced the Bayesian
Uncertainty metric, employing Monte Carlo dropout to estimate uncertainty, primar-
ily detecting adversarial examples situated near the class boundaries, while Smith et
al. [288] utilised a mutual information approach for the same purpose. Furthermore,
Hendrycks et al. [140] demonstrated that softmax prediction probabilities can be used
to identify adversarial examples. They appended a decoder to reconstruct clean inputs
from the softmax and jointly trained it with the baseline classifier. Following the hy-
pothesis that diverse models exhibit different mistakes when confronted with the same
attack inputs, Monteiro et al. [233] proposed a bimodel mismatch detection. More-
over, Feinman et al. [114] introduced kernel density estimation for each class within
the training data and subsequently trained a binary classifier as a detector, utilising the
density and uncertainty features associated with clean, noisy, and adversarial examples.
Although there are also few runtime monitoring methods for detecting adversarial ex-
amples in LLMs, we believe these current techniques can be extended to LLMs once
we can develop an LLM detection model.

7.3    Monitoring Output Failures
As we mentioned in previous sections, although LLMs have shown strong performance
in many domains [46, 218, 174, 290, 369], they are also found to be prone to vari-
ous types of failures after scrutiny and evaluation [58, 282, 364], such as factual er-
rors [364], coding [215, 183], math [118], and reasoning [214]. These failures can
spell fatal disaster for downstream tasks, especially in safety-critical applications. To
address these issues, one way is to devise a mechanism to generate constrained outputs
[152, 188, 223]. However, LLMs generate output by selecting appropriate words from
a vocabulary rather than grabbing corresponding snippets from sources of truth, or rea-
soning on them. This generative nature makes it challenging to control the output, and
even more challenging to ensure that the generated output is, in fact, consistent with
the information source. Another way is to monitor the output of the models and take
necessary actions. In the following, we first summarise the limited amount of existing
work on runtime monitoring of such failures and then discuss how to proceed from a
future perspective.
    In addition to the generative nature of LLMs, the diversity of downstream tasks also
makes it extremely difficult, if not impossible, to have a general monitoring framework
for such generative outputs. Such output failures need to be addressed in a targeted
manner, according to different application scenarios and the specific scientific knowl-
edge accumulated by humans in various fields such as science and technology. Regard-
ing factual errors, [305] proposed a testbed for fact verification. However, this remains
an unsolved challenge. Similar to fact-checking, we argue that for code generation
failures, the fruitful methods, techniques, and tools accumulated in the field of for-


                                            34
mal methods related to compilers design [191] and program verification [309] can be
adapted to check whether the generated code is executable or satisfies some specified
invariants [226, 53, 52], respectively. As for math-related failures, existing tools in au-
tomated theorem proving [115, 55] (e.g., Z3 [92] and Prover9 [228]) may help. If an
LLM is employed within safety-critical systems and its outputs are required to adhere
to specified system safety properties, then a combination of traditional runtime moni-
toring and enforcement techniques [48, 47], along with those [123, 38, 169, 168, 135]
specifically developed for safe reinforcement learning, can be put into action. This al-
lows to detect in real-time whether the model’s outputs violate predefined behavioural
specifications and enforce corrective actions on the model’s outputs to ensure the safe
operation of the system.
    In order to conduct runtime monitoring for the aforementioned output errors, sub-
stantial offline or online overheads are incurred. This is due to the requirement of estab-
lishing an auxiliary system aimed at efficiently detecting a range of output anomalies
in the model.
    Finally, we point out that the current research on the output failures of large-scale
language models is still blank. More research is needed, such as configuring a runtime
monitor for the output of a specific application, or combining symbolic reasoning and
causal reasoning with the model’s learning process to ensure that the output avoids
failures from the source.

7.4    Perspective
Since LLMs are still in their infancy and have many known vulnerabilities, monitor-
ing these models in real time is a longstanding challenge. In this section, we outline
topics for future work to call on more researchers to address this challenge from three
perspectives: why, what, and how.
    Why does a model need to be monitored? The first thing we want to highlight is
whether at some point the LLMs can be trained intelligent enough, so that there is no
need to design a separate runtime monitor for these models. For instance, the model is
endowed with abilities to automatically detect “illegal inputs” (e.g., out-of-distribution
inputs) and guarantee the correctness of its outputs. From our authors’ perspective,
achieving such level of intelligent models in the foreseeable future is very difficult,
if not impossible. The main reasons are as follows. Existing LLMs are still learned
from observations, i.e., a training dataset containing partial information. There is no
evidence that current learning methods can infer from parts to wholes, even in the case
of massive data, nor is there evidence that a training dateset captures all the information.
Furthermore, existing learning methods do not characterize their generalization bounds
but instead measure the so-called generalization error, which prevents the identification
of “illegal inputs”. Therefore, it is necessary to monitor the model in real-time.
    What should be monitored? One needs to overcome various vulnerabilities listed
in Section 3 to reliably use LLMs in safety-critical applications. Equipping the model
with a corresponding runtime monitor provides a possible solution complementary to
offline verification methods. For example, there have been some works on monitoring
whether the model’s prediction is made for out-of-distribution inputs and whether the
model’s output is consistent with some existing fact base. However, to our knowledge,


                                            35
there is no monitoring work on other output failures, e.g., reasoning and code errors;
on intended attacks, e.g., robustness, backdoor, and data poisoning. Thus, we call on
researchers and practitioners to investigate more in these topics.
    How to better design a monitor for a model? The state-of-the-art methods are based
on the uncertainty model’s predictions. Unfortunately, low uncertainty cannot assure
the model’s prediction is reliable, and vice versa. To better design monitors for LLMs,
we need the following efforts. First, some fundamental intrinsic issues of deep learning
models must be better addressed, such as model implicit generalisation and decision
boundaries and explainability of model decisions, which may provide more rigorous
and formal characterisation and specification for building monitors. Specific to LLMs,
some special issues need to be tackled, such as the unavailability of training datasets,
the non-transparency of models, the generative nature of multi-modality, etc. Regard-
ing specific tasks, such as the most studied problem of monitoring out-of-distribution
inputs, principled methods for system design and evaluation of monitors still needs
to be included, as current work is based on calibration of predictive confidence scores
and evaluation on one-sided test datasets. Last, we call for great attention to unexplored
topics, such as how to monitor other trustworthiness and responsibility issues, attacks,
and unintended bugs, along with the model’s social and ethical alignments with human
society.


8     Regulations and Ethical Use
V&V provides a set of technical means to support the alignment of LLMs with hu-
man interests. However, it has been argued that constructing LLMs that cannot be
abused can be impossible. This suggests that technical means are necessary, but can
be insufficient. To this end, it is needed to have ethical means, to supplement the tech-
nical means, in ensuring that the complete alignment of the use of LLMs with human
interests. In the following, we discuss several recent signs of progress.

8.1    Regulate or Ban?
A recent debate on “a 6-month suspension on the development [7] vs. a regulated de-
velopment” has shown the anxiety of, and the difference of opinions from, the commu-
nity upon the possibilities of AI development being misaligned with human interests.
More radical actions have also been taken. For example, Italy has reportedly banned
the ChatGPT [4]. In a US Senate Hearing on May 2023, OpenAI CEO Sam Altman
asked the government to regulate AI [278]. Actually, on AI regulations, major players
such as the EU, US, UK, and China all have their respective approaches and initiatives,
e.g., the EU’s GDPR [11], AI Act [26]. Data Act [27], the UK’s Data Protection Act
[12] and pro-innovative approach to regulate AI [29], the US’s Blueprint for an AI Bill
of Rights [22] and AI Risk Management Framework [15], and China’s regulations for
recommendation algorithms [16], deep synthesis [14], and algorithm registry [25]. It
is unclear (1) whether these regulations on the more general AI/ML, or other AI/ML
algorithms, can automatically work for LLMs without any changes, and (2) how the
regulations can be projected onto each other in a rigorous, yet operational, way. More


                                           36
importantly, even for general AI/ML, it still needs to be clarified how to sufficiently
and effectively address regulatory requirements (such as robustness and transparency)
with technical means. The V&V framework proposed in this survey will be one viable
solution.
    Nevertheless, significant issues raised by the LLMs, notably the ChatGPT, include
copyright and privacy. The ChatGPT developers reportedly use data from the internet,
and it is unclear if the copyrights of the training data have been carefully dealt with,
especially when the ChatGPT is eventually for commercial use. Moreover, as a con-
versational AI, the privacy of the end users, when engaged in a dialogue, is a serious
concern. The end-users should be informed on whether and how their dialogues will
be stored, used, and redistributed.

8.2    Responsible AI Principles
Responsible and accountable AI has been a topic of discussion for the past years (see
e.g., [13, 31, 33]), with a gradual convergence to include properties such as trans-
parency, explainability, fairness, robustness, security, privacy, etc. A governance frame-
work is called for to ensure that these properties are implemented, evaluated, and mon-
itored. A comprehensive discussion and comparison is out of the scope of this survey,
but we note that, many properties are required, consistent definitions to many of them
are still missing, and properties can be conflicting (i.e., the improvement of one prop-
erty may compromise others). It is therefore not surprising that it can still be a long
way to turn the principles into operational rules.
    Specific to LLMs, ChatGPT and the like have led to severe concerns on e.g., po-
tential misuse, unintended bias, and fair access. To this end, on the enterprise level,
ethical principles are needed to guide the development and use of LLMs, including
questioning whether something should be done rather than whether it can be done, as
requested in [9]. Moreover, systematic research is also called for to understand the
certain to which the misuse of LLMs can lead to bad consequence, as is done in [59]
on attackers generating malware with LLMs or in [275] which discusses the security
implication of using LLMs in generating codes.

8.3    Educational Challenges
Verification and validation of safe and trustworthy AI models are not central to the com-
puter science curriculum or data science curricula. When validation and verification of
models are taught at all, it is often part of an AI course that emphasizes tinkering with
testing data-set rather than as a systematic and rigorous discipline with a solid scien-
tific foundation. We need a curriculum beyond traditional education, covering formal
verification, statistics, and XAI.
     This need for adequately trained engineers impacts industrial practice, creating in-
efficiencies and difficulties in building AI systems with safety guarantees. Engineers
untrained in safety and trustworthy AI models are often asked to make AI models for
AI-critical applications.
     The need for a shared cultural background between AI and rigorous design commu-
nities results in fragmented research. They use different terminologies. For example,


                                           37
“trustworthiness” does not have the same meaning across communities. Conferences
are separate, no interaction between the two communities. The educational system will
take time to adapt to evolving industrial and cultural needs. At the least, we suggest in-
troducing AI students to the rigorous and systematic analysis of safety and trust and the
corresponding approaches to the design of AI-critical applications. Another short-term
objective should be to define and promote a reference curriculum in computer science
with an optional program for designing safe and trusted AI applications.

8.4     Transparency and Explainability
First, OpenAI’s decision to not open-source GPT-3 and beyond has already led to con-
cerns on the transparent development of AI. However, OpenAI said it plans to make
more technical details available to other third parties for them to advise on how to
weigh the competitive and safety considerations against the scientific value of further
transparency. Nevertheless, we have seen a trend of open-sourcing LLMs, with notably
Meta’s Llama 2 [306]. It is also important to note that, no technical details are available
on how the guardrail is designed and implemented. It will also be interesting to discuss
on whether the guardrail itself should undergo a verification process.
    Second, it has been hard to interpret and explain the decisions of the deep learning
models such as image classifiers. The situation becomes worsens when dealing with
LLMs [177], which have emergent and hard-to-explain behaviours. For example, it
has been observed that adding an incarnation, such as “Let’s think step by step”, to the
prompt can achieve improved responses from GPT-3. Techniques are needed to explain
such a phenomenon. This calls for extending explainable AI techniques to work with
LLMs. In particular, it is necessary to consider the explanations’ robustness to explain
why such incarnation can lead to improved, yet different, answers. To this end, some
prior works on image classifiers, such as [366, 157], can be considered.


9      Discussions
The safety and trustworthiness issues become more important with the wider adoption
of machine learning, especially for LLMs, with which a large number of end users
have direct interactions. Research has been significantly lagged behind, partly due to
the fact that some issues become more significant for LLMs than they are for the usual
machine learning models. The following are an incomplete list of research directions
that we believe require significant investments in the near future.
      • Data privacy. For usual machine learning models, their training data are obtained
        beforehand, with many of them being made available to the public. Notable
        examples include the ImageNet dataset. That is, the privacy and copyright issues
        for the training data were not as serious. However, LLMs’ training data come
        directly from the internet, many of which are private information and do not have
        the authorisations from the data owners. On top of this, various techniques, such
        as prompt injection and privacy attacks, are available to leak the information. It
        requires a multi-disciplinary approach to deal with the data privacy issue.


                                            38
     • Safety and trustworthiness implications. Currently, research is focused on trick-
       ing the LLMs to generate unexpected outcomes. There needs to be systematic
       approaches to study and measure the certain to which such unexpected outcomes
       might lead to bad consequences. This requires the modelling of the environment
       (e.g., an organisation) in which the LLMs are used, including how they are used
       and the consequences of all possible outcomes. A systematic study will enable
       the understanding of which aspects of alignments are needed and how to fine-
       tune the LLMs to different applications domains.
     • Rigorous engineering. The LLMs, in its current development, are mostly relying
       on the massive training data and the exceptional computational power owned by
       the large tech giants. Its performance currently is measured with various small
       scale benchmark datasets that are designed for the domain specific aspects of
       the abilities, for example, the mathematics, the reasoning, and so on. A rigorous
       engineering approach, by considering the entire development cycle including the
       evaluation, is needed to support the shifting of the development from extensive
       mode to intensive mode, and for the benefit of providing assurance cases for the
       applications of LLMs to safety critical domains.
     • Verification with provable guarantees. Empirical evaluation provides certain ev-
       idence about the performance, but cannot be regarded as a rigorous justifica-
       tion, especially in safety critical domains. A mathematically well-founded proof
       about the performance, e.g., in the form of statistical guarantees such as chain
       constraint [50], can be useful for improving the confidence of the users.
     • Regulations and standards. The necessity of regulations has been commonly
       agreed. However, the regulations do not provide workable measures that are
       usually recommended in industrial standards. Compliance with regulations and
       standards is an important part of an assurance case to justify the safety of a
       product. It is urgent for the community to come up with standards so as to
       release the full potential of LLMs and AI in general.


10      Conclusions
This paper provides an overview of the known vulnerabilities of LLMs, and discusses
how the V&V techniques might be adapted to work with them. Given the LLMs
are quickly adopted by applications that have direct or indirect interactions with end
users, it is imperative that the deployed LLMs undergoes sufficient verdict processes
to avoid any undesirable safety and trustworthy consequences. Novel V&V techniques
are called for, to deal with the special characteristics of the LLMs such as the nondeter-
ministic behaviours, the model sizes that are significantly larger than the usual machine
learning models, the training dataset that is obtained from internet rather than through
a careful collection process, etc. Multi-disciplinary development is needed to make
sure that all trustworthy issues are fully considered and tackled.




                                           39
Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research
and innovation programme under grant agreement No 956123. It is also financially
supported by the U.K. EPSRC through End-to-End Conceptual Guarding of Neural
Architectures [EP/T026995/1].


References
  [1] Bitcoin energy consumption index.                 https://digiconomist.net/
      bitcoin-energy-consumption. Accessed: 2023-08-17.
  [2] The carbon footprint of gpt-4.              https://towardsdatascience.com/
      the-carbon-footprint-of-gpt-4-d6c676eb21ae. Accessed: 2023-08-17.
  [3] Gpt-4’s details are leaked. https://archive.md/2RQ8X. Accessed: 2023-08-17.
  [4] Italy became the first western country to ban chatgpt. https://www.cnbc.com/
      2023/04/04/italy-has-banned-chatgpt-heres-what-other-countries-are-doing.
      html. Accessed: 2023-08-17.

  [5] March 20 chatgpt outage: Here’s what happened. https://openai.com/blog/
      march-20-chatgpt-outage. OpenAI. Accesses: 2023-08-20.
  [6] Openai         says       a        bug       leaked         sensitive     chat-
      gpt        user       data.                         https://www.engadget.com/
      chatgpt-briefly-went-offline-after-a-bug-revealed-user-chat-histories-115632504.
      html. engadget. Accessed:2023-8-20.
  [7] Pause giant ai experiments: An open letter. https://futureoflife.org/open-letter/
      pause-giant-ai-experiments/. Accesseed: 2023-08-20.
  [8] Prompt     engineering      guide.               https://github.com/dair-ai/
      Prompt-Engineering-Guide/tree/main/guides. Accessed: 2023-08-20.
  [9] Tools such as chatgpt threaten transparent science; here are our ground rules
      for their use. https://www.nature.com/articles/d41586-023-00191-1. Accessed:
      2023-08-20.

 [10] Quality management systems - process validation guidance.                  https:
      //www.imdrf.org/sites/default/files/docs/ghtf/final/sg3/technical-docs/
      ghtf-sg3-n99-10-2004-qms-process-guidance-04010.pdf, 2004.                GHTF.
      Accessed: 2023-08-20.
 [11] Eu gdpr. https://gdpr-info.eu, 2016. Accessed: 2023-08-20.

 [12] The data protection act. https://www.legislation.gov.uk/ukpga/2018/12/contents/
      enacted, 2018. Accessed: 2023-08-20.



                                          40
[13] Ethics guidelines for trustworthy ai.         https://ec.europa.eu/futurium/en/
     ai-alliance-consultation.1.html, 2018. European Commission. Accessed: 2023-
     08-20.
[14] China’s regulations on the administration of deep synthesis internet informa-
     tion services. https://www.chinalawtranslate.com/en/deep-synthesis/, 2021. Ac-
     cessed: 2023-08-20.
[15] Ai       risk   management       framework.       https://www.nist.gov/itl/
     ai-risk-management-framework, 2022. Accessed: 2023-08-20.
[16] China’s regulations on recommendation algorithms. http://www.cac.gov.cn/
     2022-01/04/c_1642894606258238.htm, 2022. Accessed: 2023-08-20.
[17] Content at scale, https://contentatscale.ai/ai-content-detector/, 2022. Accessed:
     2023-08-20.
[18] Copyleaks, https://copyleaks.com/ai-content-detector, 2022. Accessed: 2023-
     08-20.

[19] New meta ai demo writes racist and inaccurate scientific literature,
     gets      pulled.    https://arstechnica.com/information-technology/2022/11/
     after-controversy-meta-pulls-demo-of-ai-model-that-writes-scientific-papers/,
     2022. Accessed: 2023-08-20.

[20] Originality ai, https://originality.ai, 2022. Accessed: 2023-08-20.
[21] Prompt injection attacks against gpt-3. https://simonwillison.net/2022/Sep/12/
     prompt-injection/, 2022. Accessed: 2023-08-20.
[22] Blueprint for an ai bill of rights. https://www.whitehouse.gov/ostp/
     ai-bill-of-rights/, 2023. Accessed: 2023-08-20.

[23] Chatgpt: get instant answers, find creative inspiration, and learn something new.
     https://openai.com/chatgpt, 2023. Accessed: 2023-08-20.
[24] Chatgpt: Us lawyer admits using ai for case research, 2023. Accessed: 2023-
     08-23.

[25] China’s algorithm registry. https://beian.cac.gov.cn/#/index, 2023. Accessed:
     2023-08-20.
[26] Eu ai act. https://artificialintelligenceact.eu, 2023. Accessed: 2023-08-20.
[27] Eu data act. https://ec.europa.eu/commission/presscorner/detail/en/ip_22_1113,
     2023. Accessed: 2023-08-20.
[28] ’he would still be here’: Man dies by suicide after talking with ai chatbot, widow
     says, 2023. Accessed: 2023-08-23.




                                         41
[29] A pro-innovation approach to ai regulation. https://assets.publishing.service.
     gov.uk/government/uploads/system/uploads/attachment_data/file/1146542/a_
     pro-innovation_approach_to_AI_regulation.pdf, 2023. Accessed: 2023-08-20.
[30] Prompt leaking.     https://learnprompting.org/docs/prompt_hacking/leaking,
     2023. Accessed: 2023-08-20.
[31] Responsible ai priciples from microsoft. https://www.microsoft.com/en-us/ai/
     responsible-ai, 2023. Accessed: 2023-08-20.
[32] Three       samsung        employees       reportedly       leaked      sen-
     sitive       data       to        chatgpt.        https://www.engadget.com/
     three-samsung-employees-reportedly-leaked-sensitive-data-to-chatgpt-190221114.
     html, 2023. Accessed: 2023-08-20.
[33] Understanding artificial intelligence ethics and safety: A guide for the respon-
     sible design and implementation of ai systems in the public sector., 2023. Ac-
     cessed: 2023-08-20.
[34] H. Aghakhani, W. Dai, A. Manoel, X. Fernandes, A. Kharkar, C. Kruegel, G. Vi-
     gna, D. Evans, B. Zorn, and R. Sim. Trojanpuzzle: Covertly poisoning code-
     suggestion models. arXiv preprint arXiv:2301.02344, 2023.
[35] M. Agrawal, S. Hegselmann, H. Lang, Y. Kim, and D. Sontag. Large lan-
     guage models are zero-shot clinical information extractors. arXiv preprint
     arXiv:2205.12689, 2022.
[36] R. Aiyappa, J. An, H. Kwak, and Y.-Y. Ahn. Can we trust the evaluation on
     chatgpt? arXiv preprint arXiv:2303.12767, 2023.
[37] F. Akopyan, J. Sawada, A. Cassidy, R. Alvarez-Icaza, J. Arthur, P. Merolla,
     N. Imam, Y. Nakamura, P. Datta, G.-J. Nam, et al. Truenorth: Design and
     tool flow of a 65 mw 1 million neuron programmable neurosynaptic chip.
     IEEE transactions on computer-aided design of integrated circuits and systems,
     34(10):1537–1557, 2015.
[38] M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, and U. Topcu.
     Safe reinforcement learning via shielding. In Proceedings of the AAAI confer-
     ence on artificial intelligence, volume 32, 2018.
[39] M. Alzantot, Y. Sharma, A. Elgohary, B.-J. Ho, M. Srivastava, and K.-W.
     Chang. Generating natural language adversarial examples. arXiv preprint
     arXiv:1804.07998, 2018.
[40] U. Arora, W. Huang, and H. He. Types of out-of-distribution texts and how to
     detect them. arXiv preprint arXiv:2109.06827, 2021.
[41] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain,
     S. Fort, D. Ganguli, T. Henighan, et al. Training a helpful and harmless
     assistant with reinforcement learning from human feedback. arXiv preprint
     arXiv:2204.05862, 2022.


                                        42
[42] Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain,
     S. Fort, D. Ganguli, T. Henighan, et al. Training a helpful and harmless
     assistant with reinforcement learning from human feedback. arXiv preprint
     arXiv:2204.05862, 2022.
[43] Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen,
     A. Goldie, A. Mirhoseini, C. McKinnon, et al. Constitutional ai: Harmlessness
     from ai feedback. arXiv preprint arXiv:2212.08073, 2022.
[44] Y. Balaji, S. Nah, X. Huang, A. Vahdat, J. Song, K. Kreis, M. Aittala, T. Aila,
     S. Laine, B. Catanzaro, et al. ediffi: Text-to-image diffusion models with an
     ensemble of expert denoisers. arXiv preprint arXiv:2211.01324, 2022.
[45] A. Balakrishnan, A. G. Puranic, X. Qin, A. Dokhanchi, J. V. Deshmukh,
     H. Ben Amor, and G. Fainekos. Specifying and evaluating quality metrics for
     vision-based perception systems. In Design, Automation & Test in Europe Con-
     ference & Exhibition (DATE), pages 1433–1438, 2019.
[46] Y. Bang, S. Cahyawijaya, N. Lee, W. Dai, D. Su, B. Wilie, H. Lovenia,
     Z. Ji, T. Yu, W. Chung, et al. A multitask, multilingual, multimodal evalu-
     ation of chatgpt on reasoning, hallucination, and interactivity. arXiv preprint
     arXiv:2302.04023, 2023.
[47] E. Bartocci and Y. Falcone. Lectures on runtime verification. Springer, 2018.
[48] A. Bauer, M. Leucker, and C. Schallhart. Runtime verification for ltl and
     tltl. ACM Transactions on Software Engineering and Methodology (TOSEM),
     20(4):1–64, 2011.
[49] Y. Belinkov and Y. Bisk. Synthetic and natural noise both break neural machine
     translation. arXiv preprint arXiv:1711.02173, 2017.
[50] S. Bensalem, C.-H. Cheng, W. Huang, X. Huang, C. Wu, and X. Zhao. What,
     indeed, is an achievable provable guarantee for learning-enabled safety critical
     systems. In ISoLA 2023, 2023.
[51] S. Bensalem, C.-H. Cheng, X. Huang, P. Katsaros, A. Molin, D. Nickovic, and
     D. Peled. Formal specification for learning-enabled autonomous systems. In
     International Workshop on Numerical Software Verification, pages 131–143.
     Springer, 2022.
[52] S. Bensalem, Y. Lakhnech, and S. Owre. Invest: A tool for the verification
     of invariants. In Computer Aided Verification: 10th International Conference,
     CAV’98 Vancouver, BC, Canada, June 28–July 2, 1998 Proceedings 10, pages
     505–510. Springer, 1998.
[53] S. Bensalem, Y. Lakhnech, and H. Saidi. Powerful techniques for the automatic
     generation of invariants. In Computer Aided Verification: 8th International Con-
     ference, CAV’96 New Brunswick, NJ, USA, July 31–August 3, 1996 Proceedings
     8, pages 323–335. Springer, 1996.


                                        43
[54] N. Berthier, A. Alshareef, J. Sharp, S. Schewe, and X. Huang. Abstraction and
     symbolic execution of deep neural networks with bayesian approximation of
     hidden features. arXiv preprint arXiv:2103.03704, 2021.
[55] W. Bibel. Automated theorem proving. Springer Science & Business Media,
     2013.
[56] S. Black, S. Biderman, E. Hallahan, Q. Anthony, L. Gao, L. Golding, H. He,
     C. Leahy, K. McDonell, J. Phang, et al. Gpt-neox-20b: An open-source autore-
     gressive language model. arXiv preprint arXiv:2204.06745, 2022.
[57] G. Bonaert, D. I. Dimitrov, M. Baader, and M. Vechev. Fast and precise certifi-
     cation of transformers. In Proceedings of the 42nd ACM SIGPLAN International
     Conference on Programming Language Design and Implementation, pages 466–
     481, 2021.
[58] A. Borji. A categorical archive of chatgpt failures. CoRR, abs/2302.03494,
     2023.
[59] M. Botacin. Gpthreats-3: Is automatic malware generation a threat? In 2023
     IEEE Security and Privacy Workshops (SPW), pages 238–254, 2023.
[60] T. Brants, A. C. Popat, P. Xu, F. J. Och, and J. Dean. Large language models in
     machine translation. In J. Eisner, editor, EMNLP-CoNLL 2007, Proceedings of
     the 2007 Joint Conference on Empirical Methods in Natural Language Process-
     ing and Computational Natural Language Learning, June 28-30, 2007, Prague,
     Czech Republic, pages 858–867. ACL, 2007.
[61] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss,
     G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Winter,
     C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner,
     S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models
     are few-shot learners. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and
     H. Lin, editors, Advances in Neural Information Processing Systems, volume 33,
     pages 1877–1901. Curran Associates, Inc., 2020.
[62] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Nee-
     lakantan, P. Shyam, G. Sastry, A. Askell, et al. Language models are few-shot
     learners. Advances in neural information processing systems, 33:1877–1901,
     2020.
[63] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss,
     G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter,
     C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner,
     S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models
     are few-shot learners. In Proceedings of the 34th International Conference on
     Neural Information Processing Systems, NIPS’20, Red Hook, NY, USA, 2020.
     Curran Associates Inc.


                                        44
[64] M. Bullwinkle and E. Urban. Introduction to red teaming large language mod-
     els (llms). https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/
     red-teaming, 2023. Accessed: 2023-08-20.
[65] E. Bursztein. Attacks against machine learning — an overview. https://elie.net/
     blog/ai/attacks-against-machine-learning-an-overview/, 2018. Accessed: 2023-
     08-20.
[66] E. Cambiaso and L. Caviglione. Scamming the scammers: Using chatgpt to
     reply mails for wasting time and resources. arXiv preprint arXiv:2303.13521,
     2023.

[67] Y. Cao, D. Li, M. Fang, T. Zhou, J. Gao, Y. Zhan, and D. Tao. Tasa: Deceiving
     question answering models by twin answer sentences attack. arXiv preprint
     arXiv:2210.15221, 2022.
[68] N. Carlini, M. Jagielski, C. A. Choquette-Choo, D. Paleka, W. Pearce, H. Ander-
     son, A. Terzis, K. Thomas, and F. Tramèr. Poisoning web-scale training datasets
     is practical. arXiv preprint arXiv:2302.10149, 2023.
[69] B. Chen, W. Carvalho, N. Baracaldo, H. Ludwig, B. Edwards, T. Lee, I. Mol-
     loy, and B. Srivastava. Detecting backdoor attacks on deep neural networks by
     activation clustering. In SafeAI@ AAAI, 2019.
[70] L. Chen, M. Zaharia, and J. Zou. How is chatgpt’s behavior changing over time?
     arXiv preprint arXiv:2307.09009, 2023.
[71] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards,
     Y. Burda, N. Joseph, G. Brockman, et al. Evaluating large language models
     trained on code. arXiv preprint arXiv:2107.03374, 2021.

[72] S. Chen, X. Bi, R. Gao, and X. Sun. Holistic sentence embeddings for better
     out-of-distribution detection. In Findings of the Association for Computational
     Linguistics: EMNLP 2022, pages 6676–6686, Abu Dhabi, United Arab Emi-
     rates, Dec. 2022. Association for Computational Linguistics.
[73] S. Chen, B. H. Kann, M. B. Foote, H. J. Aerts, G. K. Savova, R. H. Mak,
     and D. S. Bitterman. The utility of chatgpt for cancer treatment information.
     medRxiv, pages 2023–03, 2023.
[74] S. Chen, W. Yang, X. Bi, and X. Sun. Fine-tuning deteriorates general textual
     out-of-distribution detection by distorting task-agnostic features. In Findings
     of the Association for Computational Linguistics: EACL 2023, pages 552–567,
     2023.

[75] X. Chen, A. Salem, D. Chen, M. Backes, S. Ma, Q. Shen, Z. Wu, and Y. Zhang.
     Badnl: Backdoor attacks against nlp models with semantic-preserving improve-
     ments. In Annual Computer Security Applications Conference, pages 554–569,
     2021.


                                        45
[76] C. Cheng, G. Nührenberg, and H. Yasuoka. Runtime monitoring neuron activa-
     tion patterns. In DATE2019, pages 300–303, 2019.
[77] C.-H. Cheng, C. Wu, E. Seferis, and S. Bensalem. Prioritizing corners in ood de-
     tectors via symbolic string manipulation. In A. Bouajjani, L. Holík, and Z. Wu,
     editors, Automated Technology for Verification and Analysis, pages 397–413,
     Cham, 2022. Springer International Publishing.
[78] M. Cheng, J. Yi, P.-Y. Chen, H. Zhang, and C.-J. Hsieh. Seq2sick: Evaluating
     the robustness of sequence-to-sequence models with adversarial examples. In
     Proceedings of the AAAI conference on artificial intelligence, volume 34, pages
     3601–3608, 2020.

[79] Y. Cheng, L. Jiang, and W. Macherey. Robust neural machine translation with
     doubly adversarial inputs. arXiv preprint arXiv:1906.02443, 2019.
[80] W.-L. Chiang, Z. Li, Z. Lin, Y. Sheng, Z. Wu, H. Zhang, L. Zheng, S. Zhuang,
     Y. Zhuang, J. E. Gonzalez, et al. Vicuna: An open-source chatbot impressing
     gpt-4 with 90%* chatgpt quality. See https://vicuna. lmsys. org (accessed 14
     April 2023), 2023.
[81] H. Cho, C. Park, J. Kang, K. M. Yoo, T. Kim, and S.-g. Lee. Enhancing out-
     of-distribution detection in natural language understanding via implicit layer en-
     semble. In Findings of the Association for Computational Linguistics: EMNLP
     2022, pages 783–798, Abu Dhabi, United Arab Emirates, Dec. 2022. Associa-
     tion for Computational Linguistics.
[82] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts,
     P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, et al. Palm: Scaling lan-
     guage modeling with pathways. arXiv preprint arXiv:2204.02311, 2022.

[83] P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei. Deep
     reinforcement learning from human preferences. In I. Guyon, U. V. Luxburg,
     S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors,
     Advances in Neural Information Processing Systems, volume 30. Curran Asso-
     ciates, Inc., 2017.

[84] P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei. Deep
     reinforcement learning from human preferences. Advances in neural informa-
     tion processing systems, 30, 2017.
[85] K. Clark, M.-T. Luong, Q. V. Le, and C. D. Manning. Electra: Pre-
     training text encoders as discriminators rather than generators. arXiv preprint
     arXiv:2003.10555, 2020.
[86] K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert,
     J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word
     problems. arXiv preprint arXiv:2110.14168, 2021.



                                         46
[87] J. Cohen, E. Rosenfeld, and Z. Kolter. Certified adversarial robustness via ran-
     domized smoothing. In international conference on machine learning, pages
     1310–1320. PMLR, 2019.
[88] F. Croce and M. Hein. Reliable evaluation of adversarial robustness with an
     ensemble of diverse parameter-free attacks. In International conference on ma-
     chine learning, pages 2206–2216. PMLR, 2020.
[89] J. Dai, C. Chen, and Y. Li. A backdoor attack against lstm-based text classifica-
     tion systems. IEEE Access, 7:138872–138878, 2019.
[90] S. Dan and D. Roth. On the effects of transformer size on in-and out-of-
     domain calibration. In Findings of the Association for Computational Linguis-
     tics: EMNLP 2021, pages 2096–2101, 2021.
[91] M. Davies, N. Srinivasa, T.-H. Lin, G. Chinya, Y. Cao, S. H. Choday, G. Dimou,
     P. Joshi, N. Imam, S. Jain, et al. Loihi: A neuromorphic manycore processor
     with on-chip learning. IEEE Micro, 38(1):82–99, 2018.
[92] L. De Moura and N. Bjørner. Z3: An efficient smt solver. In Tools and Algo-
     rithms for the Construction and Analysis of Systems: 14th International Confer-
     ence, TACAS 2008, Held as Part of the Joint European Conferences on Theory
     and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6,
     2008. Proceedings 14, pages 337–340. Springer, 2008.
[93] A. De Vries, U. Gallersdörfer, L. Klaaßen, and C. Stoll. Revisiting bitcoin’s
     carbon footprint. Joule, 6(3):498–502, 2022.
[94] S. Desai and G. Durrett. Calibration of pre-trained transformers. In Proceedings
     of the 2020 Conference on Empirical Methods in Natural Language Processing
     (EMNLP), pages 295–302, Online, Nov. 2020. Association for Computational
     Linguistics.
[95] A. Deshpande, V. Murahari, T. Rajpurohit, A. Kalyan, and K. Narasimhan. Tox-
     icity in chatgpt: Analyzing persona-assigned language models. arXiv preprint
     arXiv:2304.05335, 2023.
[96] T. Dettmers, M. Lewis, Y. Belkada, and L. Zettlemoyer. Gpt3. int8 (): 8-bit
     matrix multiplication for transformers at scale. Advances in Neural Information
     Processing Systems, 35:30318–30332, 2022.
[97] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. Bert: Pre-training of
     deep bidirectional transformers for language understanding. arXiv preprint
     arXiv:1810.04805, 2018.
[98] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. BERT: Pre-training of deep
     bidirectional transformers for language understanding. In Proceedings of the
     2019 Conference of the North American Chapter of the Association for Compu-
     tational Linguistics: Human Language Technologies, Volume 1 (Long and Short
     Papers), pages 4171–4186, Minneapolis, Minnesota, June 2019. Association for
     Computational Linguistics.


                                         47
 [99] T. DeVries and G. W. Taylor. Learning confidence for out-of-distribution detec-
      tion in neural networks. arXiv preprint 1802.04865, 2018.
[100] N. Dey.            Gpt:      A family of open,             compute-efficient,
      large     language      models.               https://www.cerebras.net/blog/
      cerebras-gpt-a-family-of-open-compute-efficient-large-language-models/,
      Apr 2023. Accessed: 2023-08-20.
[101] J. Dodge, G. Ilharco, R. Schwartz, A. Farhadi, H. Hajishirzi, and N. Smith. Fine-
      tuning pretrained language models: Weight initializations, data orders, and early
      stopping. arXiv preprint arXiv:2002.06305, 2020.

[102] N. Du, Y. Huang, A. M. Dai, S. Tong, D. Lepikhin, Y. Xu, M. Krikun, Y. Zhou,
      A. W. Yu, O. Firat, et al. Glam: Efficient scaling of language models with
      mixture-of-experts. In International Conference on Machine Learning, pages
      5547–5569. PMLR, 2022.
[103] T. Du, S. Ji, L. Shen, Y. Zhang, J. Li, J. Shi, C. Fang, J. Yin, R. Beyah, and
      T. Wang. Cert-rnn: Towards certifying the robustness of recurrent neural net-
      works. CCS, 21(2021):15–19, 2021.
[104] H. Duan, Y. Yang, A. Abbasi, and K. Y. Tam. BARLE: Background-aware rep-
      resentation learning for background shift out-of-distribution detection. In Find-
      ings of the Association for Computational Linguistics: EMNLP 2022, pages
      750–764, Abu Dhabi, United Arab Emirates, Dec. 2022. Association for Com-
      putational Linguistics.
[105] J. Duan, F. Kong, S. Wang, X. Shi, and K. Xu. Are diffusion models vulnerable
      to membership inference attacks? arXiv preprint arXiv:2302.01316, 2023.
[106] J. J. Dudley and P. O. Kristensson. A review of user interface design for inter-
      active machine learning. ACM Transactions on Interactive Intelligent Systems
      (TiiS), 8(2):1–37, 2018.
[107] E2Analyst.           Gpt-4:      Everything    you     want   to   know
      about openai’s new ai model.                  https://medium.com/predict/
      gpt-4-everything-you-want-to-know-about-openais-new-ai-model-a5977b42e495,
      Mar 2023. Accessed: 2023-08-20.
[108] J. Ebrahimi, A. Rao, D. Lowd, and D. Dou. Hotflip: White-box adversarial
      examples for text classification. arXiv preprint arXiv:1712.06751, 2017.
[109] B. EDWARDS. Study claims chatgpt is losing capability, but some experts
      aren’t convinced.     https://arstechnica.com/information-technology/2023/07/
      is-chatgpt-getting-worse-over-time-study-claims-yes-but-others-arent-sure/,
      2023. Accessed: 2023-08-20.
[110] D. Eppstein. Zonohedra and zonotopes. Mathematica in Education and Re-
      search, 5(4):15–21, 1996.


                                          48
[111] P. Esser, R. Rombach, and B. Ommer. Taming transformers for high-resolution
      image synthesis. In Proceedings of the IEEE/CVF conference on computer vi-
      sion and pattern recognition, pages 12873–12883, 2021.
[112] F. Farhat, S. Sohail, and D. Madsen. How trustworthy is chatgpt? the case of
      bibliometric analyses. Cogent Engineering, 10, 06 2023.

[113] W. Fedus, B. Zoph, and N. Shazeer. Switch transformers: Scaling to trillion
      parameter models with simple and efficient sparsity. J. Mach. Learn. Res, 23:1–
      40, 2021.
[114] R. Feinman, R. R. Curtin, S. Shintre, and A. B. Gardner. Detecting adversarial
      samples from artifacts. arXiv preprint arXiv:1703.00410, 2017.
[115] M. Fitting. First-Order Logic and Automated Theorem Proving, Second Edition.
      Graduate Texts in Computer Science. Springer, 1996.
[116] E. Frantar and D. Alistarh. Optimal brain compression: A framework for accu-
      rate post-training quantization and pruning. arXiv preprint arXiv:2208.11580,
      2022.
[117] E. Frantar, S. Ashkboos, T. Hoefler, and D. Alistarh. Gptq: Accurate quanti-
      zation for generative pre-trained transformers. In International Conference on
      Learning Representations, 2023.

[118] S. Frieder, L. Pinchetti, R.-R. Griffiths, T. Salvatori, T. Lukasiewicz, P. C. Pe-
      tersen, A. Chevalier, and J. Berner. Mathematical capabilities of chatgpt. arXiv
      preprint arXiv:2301.13867, 2023.
[119] V. Gangal, A. Arora, A. Einolghozati, and S. Gupta. Likelihood ratios and gen-
      erative classifiers for unsupervised out-of-domain detection in task oriented di-
      alog. In Proceedings of the AAAI Conference on Artificial Intelligence, vol-
      ume 34, pages 7764–7771, 2020.
[120] D. Ganguli, A. Askell, N. Schiefer, T. Liao, K. Lukošiūtė, A. Chen, A. Goldie,
      A. Mirhoseini, C. Olsson, D. Hernandez, et al. The capacity for moral self-
      correction in large language models. arXiv preprint arXiv:2302.07459, 2023.

[121] J. Gao, J. Lanchantin, M. L. Soffa, and Y. Qi. Black-box generation of adversar-
      ial text sequences to evade deep learning classifiers. In 2018 IEEE Security and
      Privacy Workshops (SPW), pages 50–56. IEEE, 2018.
[122] L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig.
      Pal: Program-aided language models, 2023.

[123] J. Garcıa and F. Fernández. A comprehensive survey on safe reinforcement
      learning. Journal of Machine Learning Research, 16(1):1437–1480, 2015.
[124] I. Goodfellow and N. Papernot. The challenge of verification and testing of
      machine learning. Cleverhans-blog, 2017.


                                          49
[125] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair,
      A. Courville, and Y. Bengio. Generative adversarial networks. Communications
      of the ACM, 63(11):139–144, 2020.
[126] I. J. Goodfellow, J. Shlens, and C. Szegedy. Explaining and harnessing adver-
      sarial examples. arXiv preprint arXiv:1412.6572, 2014.

[127] D. GOODIN. Hackers are selling a service that bypasses chatgpt restric-
      tions on malware. https://arstechnica.com/information-technology/2023/02/
      now-open-fee-based-telegram-service-that-uses-chatgpt-to-generate-malware/,
      2023. Accessed: 2023-08-20.

[128] D. Gopinath, K. Wang, M. Zhang, C. S. Pasareanu, and S. Khurshid. Symbolic
      execution for deep neural networks. arXiv preprint arXiv:1807.10439, 2018.
[129] J. Gou, B. Yu, S. J. Maybank, and D. Tao. Knowledge distillation: A survey.
      International Journal of Computer Vision, 129:1789–1819, 2021.
[130] S. Gowal, K. Dvijotham, R. Stanforth, R. Bunel, C. Qin, J. Uesato, R. Arand-
      jelovic, T. Mann, and P. Kohli. On the effectiveness of interval bound propa-
      gation for training verifiably robust models. arXiv preprint arXiv:1810.12715,
      2018.
[131] S. Goyal, S. Doddapaneni, M. M. Khapra, and B. Ravindran. A survey in adver-
      sarial defences and robustness in nlp. arXiv preprint arXiv:2203.06414, 2022.

[132] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M. Fritz.
      More than you’ve asked for: A comprehensive analysis of novel prompt in-
      jection threats to application-integrated large language models. arXiv preprint
      arXiv:2302.12173, 2023.

[133] J.-C. Gu, T. Li, Q. Liu, Z.-H. Ling, Z. Su, S. Wei, and X. Zhu. Speaker-aware
      bert for multi-turn response selection in retrieval-based chatbots. In Proceed-
      ings of the 29th ACM International Conference on Information &amp; Knowl-
      edge Management, CIKM ’20, page 2041–2044, New York, NY, USA, 2020.
      Association for Computing Machinery.
[134] S. Gu, A. Kshirsagar, Y. Du, G. Chen, Y. Yang, J. Peters, and A. Knoll. A
      human-centered safe robot reinforcement learning framework with interactive
      behaviors. arXiv preprint arXiv:2302.13137, 2023.
[135] S. Gu, L. Yang, Y. Du, G. Chen, F. Walter, J. Wang, Y. Yang, and A. Knoll. A
      review of safe reinforcement learning: Methods, theory and applications. arXiv
      preprint arXiv:2205.10330, 2022.

[136] T. Gu, K. Liu, B. Dolan-Gavitt, and S. Garg. Badnets: Evaluating backdooring
      attacks on deep neural networks. IEEE Access, 7:47230–47244, 2019.
[137] Y. Gu, L. Dong, F. Wei, and M. Huang. Knowledge distillation of large language
      models. arXiv preprint arXiv:2306.08543, 2023.


                                         50
[138] D. Gunning, M. Stefik, J. Choi, T. Miller, S. Stumpf, and G.-Z. Yang.
      Xai—explainable artificial intelligence. Science robotics, 4(37):eaay7120, 2019.
[139] B. Guo, X. Zhang, Z. Wang, M. Jiang, J. Nie, Y. Ding, J. Yue, and Y. Wu. How
      close is chatgpt to human experts? comparison corpus, evaluation, and detection.
      CoRR, abs/2301.07597, 2023.
[140] D. Hendrycks and K. Gimpel. A baseline for detecting misclassified and out-
      of-distribution examples in neural networks. In International Conference on
      Learning Representations, 2016.
[141] D. Hendrycks, X. Liu, E. Wallace, A. Dziedzic, R. Krishnan, and D. Song. Pre-
      trained transformers improve out-of-distribution robustness. In Proceedings of
      the 58th Annual Meeting of the Association for Computational Linguistics, pages
      2744–2751, 2020.
[142] T. A. Henzinger, A. Lukina, and C. Schilling. Outside the box: Abstraction-
      based monitoring of neural networks. In ECAI2020.
[143] G. Hinton, O. Vinyals, and J. Dean. Distilling the knowledge in a neural net-
      work. arXiv preprint arXiv:1503.02531, 2015.
[144] A. Hintze. Chatgpt believes it is conscious. arXiv preprint arXiv:2304.12898,
      2023.
[145] J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford,
      D. d. L. Casas, L. A. Hendricks, J. Welbl, A. Clark, et al. Training compute-
      optimal large language models. arXiv preprint arXiv:2203.15556, 2022.
[146] J. Holmes, Z. Liu, L. Zhang, Y. Ding, T. T. Sio, L. A. McGee, J. B. Ashman,
      X. Li, T. Liu, J. Shen, et al. Evaluating large language models on a highly-
      specialized topic, radiation oncology physics. arXiv preprint arXiv:2304.01938,
      2023.
[147] H. Hosseini, S. Kannan, B. Zhang, and R. Poovendran.             Deceiving
      google’s perspective api built for detecting toxic comments. arXiv preprint
      arXiv:1702.08138, 2017.
[148] N. Houlsby, A. Giurgiu, S. Jastrzebski, B. Morrone, Q. De Laroussilhe, A. Ges-
      mundo, M. Attariyan, and S. Gelly. Parameter-efficient transfer learning for nlp.
      In International Conference on Machine Learning, pages 2790–2799. PMLR,
      2019.
[149] O. Hrinchuk, M. Popova, and B. Ginsburg. Correction of automatic speech
      recognition with transformer sequence-to-sequence model. In Icassp 2020-
      2020 IEEE international conference on acoustics, speech and signal processing
      (icassp), pages 7074–7078. IEEE, 2020.
[150] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and
      W. Chen. Lora: Low-rank adaptation of large language models. arXiv preprint
      arXiv:2106.09685, 2021.


                                          51
[151] E. J. Hu, yelong shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and
      W. Chen. LoRA: Low-rank adaptation of large language models. In Interna-
      tional Conference on Learning Representations, 2022.
[152] Z. Hu, Z. Yang, X. Liang, R. Salakhutdinov, and E. P. Xing. Toward con-
      trolled generation of text. In International conference on machine learning,
      pages 1587–1596. PMLR, 2017.
[153] H. Huang, Z. Li, L. Wang, S. Chen, B. Dong, and X. Zhou. Feature space
      singularity for out-of-distribution detection. arXiv preprint arXiv:2011.14654,
      2020.

[154] P.-S. Huang, R. Stanforth, J. Welbl, C. Dyer, D. Yogatama, S. Gowal, K. Dvi-
      jotham, and P. Kohli. Achieving verified robustness to symbol substitutions via
      interval bound propagation. arXiv preprint arXiv:1909.01492, 2019.
[155] W. Huang, Y. Sun, X. Zhao, J. Sharp, W. Ruan, J. Meng, and X. Huang.
      Coverage-guided testing for recurrent neural networks. IEEE Transactions on
      Reliability, 71(3):1191–1206, 2021.
[156] W. Huang, X. Zhao, A. Banks, V. Cox, and X. Huang. Hierarchical distribution-
      aware testing of deep learning. arXiv preprint arXiv:2205.08589, 2022.
[157] W. Huang, X. Zhao, G. Jin, and X. Huang. Safari: Versatile and efficient evalua-
      tions for robustness of interpretability. arXiv preprint arXiv:2208.09418, 2022.

[158] X. Huang, M. Alzantot, and M. Srivastava. Neuroninspect: Detecting backdoors
      in neural networks via output explanations. arXiv preprint arXiv:1911.07399,
      2019.
[159] X. Huang, G. Jin, and W. Ruan. Machine learning basics. In Machine Learning
      Safety, pages 3–13. Springer, 2012.
[160] X. Huang, D. Kroening, W. Ruan, J. Sharp, Y. Sun, E. Thamo, M. Wu, and X. Yi.
      A survey of safety and trustworthiness of deep neural networks: Verification,
      testing, adversarial attack and defence, and interpretability. Computer Science
      Review, 37:100270, 2020.

[161] X. Huang, M. Kwiatkowska, S. Wang, and M. Wu. Safety verification of deep
      neural networks. In R. Majumdar and V. Kuncak, editors, Computer Aided Veri-
      fication - 29th International Conference, CAV 2017, Heidelberg, Germany, July
      24-28, 2017, Proceedings, Part I, volume 10426 of Lecture Notes in Computer
      Science, pages 3–29. Springer, 2017.

[162] X. Huang, W. Ruan, Q. Tang, and X. Zhao. Bridging formal methods
      and&nbsp;machine learning with&nbsp;global optimisation. In Formal Meth-
      ods and Software Engineering: 23rd International Conference on Formal Engi-
      neering Methods, ICFEM 2022, Madrid, Spain, October 24–27, 2022, Proceed-
      ings, page 1–19, Berlin, Heidelberg, 2022. Springer-Verlag.


                                         52
[163] A. Ilyas, S. Santurkar, D. Tsipras, L. Engstrom, B. Tran, and A. Madry. Adver-
      sarial examples are not bugs, they are features. Advances in neural information
      processing systems, 32, 2019.
[164] A. Ivankay, I. Girardi, C. Marchiori, and P. Frossard. Fooling explanations in
      text classifiers. arXiv preprint arXiv:2206.03178, 2022.
[165] M. Iyyer, J. Wieting, K. Gimpel, and L. Zettlemoyer. Adversarial example
      generation with syntactically controlled paraphrase networks. arXiv preprint
      arXiv:1804.06059, 2018.
[166] A. Jaiswal, A. R. Babu, M. Z. Zadeh, D. Banerjee, and F. Makedon. A survey
      on contrastive self-supervised learning. Technologies, 9(1):2, 2020.
[167] M. Jang and T. Lukasiewicz. Consistency analysis of chatgpt. arXiv preprint
      arXiv:2303.06273, 2023.
[168] N. Jansen, B. Könighofer, J. Junges, A. Serban, and R. Bloem. Safe reinforce-
      ment learning using probabilistic shields. Dagstuhl: Schloss Dagstuhl, 2020.
[169] N. Jansen, B. Könighofer, S. Junges, and R. Bloem. Shielded decision-making
      in mdps. arXiv preprint arXiv:1807.06096, 2018.
[170] Y. Ji, Y. Gong, Y. Peng, C. Ni, P. Sun, D. Pan, B. Ma, and X. Li. Exploring
      chatgpt’s ability to rank content: A preliminary study on consistency with human
      preferences, 2023.
[171] R. Jia and P. Liang. Adversarial examples for evaluating reading comprehension
      systems. arXiv preprint arXiv:1707.07328, 2017.
[172] R. Jia, A. Raghunathan, K. Göksel, and P. Liang. Certified robustness to adver-
      sarial word substitutions. arXiv preprint arXiv:1909.00986, 2019.
[173] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu,
      and G. Lample. Draft, sketch, and prove: Guiding formal theorem provers with
      informal proofs. arXiv preprint arXiv:2210.12283, 2022.
[174] W. Jiao, W. Wang, J.-t. Huang, X. Wang, and Z. Tu. Is chatgpt a good translator?
      a preliminary study. arXiv preprint arXiv:2301.08745, 2023.
[175] D. Jin, Z. Jin, J. T. Zhou, and P. Szolovits. Is bert really robust? a strong baseline
      for natural language attack on text classification and entailment. In Proceedings
      of the AAAI conference on artificial intelligence, volume 34, pages 8018–8025,
      2020.
[176] K. S. Kalyan, A. Rajasekharan, and S. Sangeetha. Ammus: A survey of
      transformer-based pretrained models in natural language processing. arXiv
      preprint arXiv:2108.05542, 2021.
[177] S. Kambhampati. Changing the nature of ai research. Commun. ACM, 65(9):8–9,
      aug 2022.


                                            53
[178] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and J. Rajen-
      dran. Llm-assisted generation of hardware assertions. CoRR, abs/2306.14027,
      2023.
[179] D. Kang, X. Li, I. Stoica, C. Guestrin, M. Zaharia, and T. Hashimoto. Exploit-
      ing programmatic behavior of llms: Dual-use through standard security attacks.
      arXiv preprint arXiv:2302.05733, 2023.
[180] Y. Kang, Q. Zhang, and R. Roth. The ethics of ai-generated maps: A study
      of dalle 2 and implications for cartography. arXiv preprint arXiv:2304.10743,
      2023.

[181] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child,
      S. Gray, A. Radford, J. Wu, and D. Amodei. Scaling laws for neural language
      models. arXiv preprint arXiv:2001.08361, 2020.
[182] D. M. Katz, M. J. Bommarito, S. Gao, and P. Arredondo. Gpt-4 passes the bar
      exam. Available at SSRN 4389233, 2023.

[183] R. Khoury, A. R. Avila, J. Brunelle, and B. M. Camara. How secure is code
      generated by chatgpt? arXiv preprint arXiv:2304.09655, 2023.
[184] Y.-M. Kim. Data and fair use. Korea Copyright Commission, 141:5–53, 03
      2023.

[185] C.-Y. Ko, Z. Lyu, L. Weng, L. Daniel, N. Wong, and D. Lin. Popqorn: Quan-
      tifying robustness of recurrent neural networks. In International Conference on
      Machine Learning, pages 3468–3477. PMLR, 2019.
[186] J. Y. Koh, D. Fried, and R. Salakhutdinov. Generating images with multimodal
      language models. arXiv preprint arXiv:2305.17216, 2023.

[187] V. Kuleshov, S. Thakoor, T. Lau, and S. Ermon. Adversarial examples for natural
      language classification problems. arXiv preprint, 2018.
[188] A. Kumar, K. Ahuja, R. Vadapalli, and P. Talukdar. Syntax-guided controlled
      generation of paraphrases. Transactions of the Association for Computational
      Linguistics, 8:330–345, 2020.

[189] K. Kurita, P. Michel, and G. Neubig. Weight poisoning attacks on pretrained
      models. In Proceedings of the 58th Annual Meeting of the Association for Com-
      putational Linguistics, pages 2793–2806, 2020.
[190] E. La Malfa, M. Wu, L. Laurenti, B. Wang, A. Hartshorn, and M. Kwiatkowska.
      Assessing robustness of text classification through maximal safe radius compu-
      tation. arXiv preprint arXiv:2010.02004, 2020.
[191] M. Lam, R. Sethi, J. D. Ullman, and A. Aho. Compilers: principles, techniques,
      and tools. Pearson Education, 2006.



                                         54
[192] N. Lambert, L. Castricato, L. von Werra, and A. Havrilla. Illustrating rein-
      forcement learning from human feedback (rlhf). Hugging Face Blog, 2022.
      https://huggingface.co/blog/rlhf.
[193] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut. Albert: A
      lite bert for self-supervised learning of language representations. arXiv preprint
      arXiv:1909.11942, 2019.
[194] C. Lee, K. Cho, and W. Kang. Mixout: Effective regularization to finetune large-
      scale pretrained language models. arXiv preprint arXiv:1909.11299, 2019.
[195] J. Y. Lee. Can an artificial intelligence chatbot be the author of a scholarly
      article? journal of Educational Evaluation for Health Professions, 20, 2023.
[196] K. Lee, H. Liu, M. Ryu, O. Watkins, Y. Du, C. Boutilier, P. Abbeel,
      M. Ghavamzadeh, and S. S. Gu. Aligning text-to-image models using human
      feedback. arXiv preprint arXiv:2302.12192, 2023.
[197] N. Lee, Y. Bang, A. Madotto, and P. Fung. Misinformation has high perplexity.
      arXiv preprint arXiv:2006.04666, 2020.
[198] P.       Lee.                 Learning      from       tay’s     introduction.
      https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/,
      25,05.2016. Accessed: 2023-08-20.

[199] Y. Lei, Y. Cao, D. Li, T. Zhou, M. Fang, and M. Pechenizkiy. Phrase-level textual
      adversarial attack with label preservation. arXiv preprint arXiv:2205.10710,
      2022.
[200] D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer,
      and Z. Chen. Gshard: Scaling giant models with conditional computation and
      automatic sharding. arXiv preprint arXiv:2006.16668, 2020.
[201] M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy, V. Stoy-
      anov, and L. Zettlemoyer. BART: Denoising sequence-to-sequence pre-training
      for natural language generation, translation, and comprehension. In Proceedings
      of the 58th Annual Meeting of the Association for Computational Linguistics,
      pages 7871–7880, Online, July 2020. Association for Computational Linguis-
      tics.
[202] H. Li, D. Guo, W. Fan, M. Xu, and Y. Song. Multi-step jailbreaking privacy
      attacks on chatgpt. arXiv preprint arXiv:2304.05197, 2023.
[203] J. Li, X. Cheng, W. X. Zhao, J.-Y. Nie, and J.-R. Wen. Halueval: A large-scale
      hallucination evaluation benchmark for large language models. arXiv e-prints,
      pages arXiv–2305, 2023.
[204] J. Li, S. Ji, T. Du, B. Li, and T. Wang. Textbugger: Generating adversarial text
      against real-world applications. arXiv preprint arXiv:1812.05271, 2018.



                                          55
[205] J. Li, T. Tang, W. X. Zhao, J.-Y. Nie, and J.-R. Wen. Pretrained language models
      for text generation: A survey. arXiv preprint arXiv:2201.05273, 2022.
[206] S. Li, H. Liu, T. Dong, B. Z. H. Zhao, M. Xue, H. Zhu, and J. Lu. Hidden
      backdoors in human-centric language models. In CCS ’21: 2021 ACM SIGSAC
      Conference on Computer and Communications Security, Virtual Event, Republic
      of Korea, November 15 - 19, 2021, pages 3123–3140. ACM, 2021.
[207] X. Li, J. Li, X. Sun, C. Fan, T. Zhang, F. Wu, Y. Meng, and J. Zhang.
      kfolden: k-fold ensemble for out-of-distribution detection-fold ensemble for
      out-of-distribution detection. In Proceedings of the 2021 Conference on Em-
      pirical Methods in Natural Language Processing, pages 3102–3115, 2021.

[208] Y. Li, L. Ding, and X. Gao. On the decision boundary of deep neural networks.
      arXiv preprint arXiv:1808.05385, 2018.
[209] B. Liang, H. Li, M. Su, P. Bian, X. Li, and W. Shi. Deep text classification can
      be fooled. arXiv preprint arXiv:1704.08006, 2017.

[210] S. Liang, Y. Li, and R. Srikant. Enhancing the reliability of out-of-distribution
      image detection in neural networks. In 6th International Conference on Learn-
      ing Representations, ICLR 2018, 2018.
[211] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, and
      C. L. Zitnick. Microsoft coco: Common objects in context. In Computer Vision–
      ECCV 2014: 13th European Conference, Zurich, Switzerland, September 6-12,
      2014, Proceedings, Part V 13, pages 740–755. Springer, 2014.
[212] Z. Lin, P. Xu, G. I. Winata, F. B. Siddique, Z. Liu, J. Shin, and P. Fung. Caire:
      An empathetic neural chatbot. arXiv preprint arXiv:1907.12108, 2019.
[213] C. Liu, T. Arnon, C. Lazarus, C. Strong, C. Barrett, M. J. Kochenderfer, et al.
      Algorithms for verifying deep neural networks. Foundations and Trends® in
      Optimization, 4(3-4):244–404, 2021.
[214] H. Liu, R. Ning, Z. Teng, J. Liu, Q. Zhou, and Y. Zhang. Evaluating the logical
      reasoning ability of chatgpt and gpt-4. arXiv preprint arXiv:2304.03439, 2023.

[215] J. Liu, C. S. Xia, Y. Wang, and L. Zhang. Is your code generated by chatgpt
      really correct? rigorous evaluation of large language models for code generation.
      arXiv preprint arXiv:2305.01210, 2023.
[216] W. Liu, X. Wang, J. Owens, and Y. Li. Energy-based out-of-distribution de-
      tection. Advances in neural information processing systems, 33:21464–21475,
      2020.
[217] X. Liu, F. Zhang, Z. Hou, L. Mian, Z. Wang, J. Zhang, and J. Tang. Self-
      supervised learning: Generative or contrastive. IEEE Transactions on Knowl-
      edge and Data Engineering, 35(1):857–876, 2021.



                                          56
[218] Y. Liu, T. Han, S. Ma, J. Zhang, Y. Yang, J. Tian, H. He, A. Li, M. He, Z. Liu,
      et al. Summary of chatgpt/gpt-4 research and perspective towards the future of
      large language models. arXiv preprint arXiv:2304.01852, 2023.
[219] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettle-
      moyer, and V. Stoyanov. Roberta: A robustly optimized bert pretraining ap-
      proach. arXiv preprint arXiv:1907.11692, 2019.
[220] Z. Liu, Y. Wang, K. Han, W. Zhang, S. Ma, and W. Gao. Post-training quantiza-
      tion for vision transformer. Advances in Neural Information Processing Systems,
      34:28092–28103, 2021.

[221] Z. Liu, X. Yu, L. Zhang, Z. Wu, C. Cao, H. Dai, L. Zhao, W. Liu, D. Shen, Q. Li,
      et al. Deid-gpt: Zero-shot medical text de-identification by gpt-4. arXiv preprint
      arXiv:2303.11032, 2023.
[222] R. Lou, K. Zhang, and W. Yin. Is prompt all you need? no. a comprehensive and
      broader view of instruction learning. arXiv preprint arXiv:2303.10475, 2023.

[223] N. Madaan, I. Padhi, N. Panwar, and D. Saha. Generate your counterfactu-
      als: Towards controlled counterfactual generation for text. In Proceedings of
      the AAAI Conference on Artificial Intelligence, volume 35, pages 13516–13524,
      2021.
[224] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu.            To-
      wards deep learning models resistant to adversarial attacks. arXiv preprint
      arXiv:1706.06083, 2017.
[225] K. Malinka, M. Peresíni, A. Firc, O. Hujnák, and F. Janus. On the educational
      impact of chatgpt: Is artificial intelligence ready to obtain a university degree?
      In Proceedings of the 2023 Conference on Innovation and Technology in Com-
      puter Science Education V. 1, pages 47–53, 2023.
[226] Z. Manna and A. Pnueli. The temporal logic of reactive and concurrent systems:
      Specification. Springer Science & Business Media, 2012.
[227] N. Maus, P. Chao, E. Wong, and J. Gardner. Adversarial prompting for black
      box foundation models. arXiv preprint arXiv:2302.04237, 2023.

[228] W. McCune. Prover9 and mace4. https://www.cs.unm.edu/~mccune/prover9/,
      2005. Accessed: 2023-08-20.
[229] Y. Mehdi. Announcing the next wave of ai innovation with microsoft bing and
      edge, May 2023.

[230] S. Min, X. Lyu, A. Holtzman, M. Artetxe, M. Lewis, H. Hajishirzi, and L. Zettle-
      moyer. Rethinking the role of demonstrations: What makes in-context learning
      work? arXiv preprint arXiv:2202.12837, 2022.




                                          57
[231] M. Mirman, T. Gehr, and M. Vechev. Differentiable abstract interpretation for
      provably robust neural networks. In J. Dy and A. Krause, editors, Proceedings
      of the 35th International Conference on Machine Learning, volume 80 of Pro-
      ceedings of Machine Learning Research, pages 3578–3586. PMLR, 10–15 Jul
      2018.
[232] S. Mitrović, D. Andreoletti, and O. Ayoub. Chatgpt or human? detect and
      explain. explaining decisions of machine learning model for detecting short
      chatgpt-generated text, 2023.
[233] J. Monteiro, I. Albuquerque, Z. Akhtar, and T. H. Falk. Generalizable adver-
      sarial examples detection based on bi-model decision mismatch. In 2019 IEEE
      International Conference on Systems, Man and Cybernetics (SMC), pages 2839–
      2844. IEEE, 2019.
[234] M. Nagel, R. A. Amjad, M. Van Baalen, C. Louizos, and T. Blankevoort. Up
      or down? adaptive rounding for post-training quantization. In International
      Conference on Machine Learning, pages 7197–7206. PMLR, 2020.
[235] B. Nelson, M. Barreno, F. J. Chi, A. D. Joseph, B. I. P. Rubinstein, U. Saini,
      C. Sutton, J. D. Tygar, and K. Xia. Exploiting machine learning to subvert your
      spam filter. In Proceedings of the 1st Usenix Workshop on Large-Scale Exploits
      and Emergent Threats, LEET’08, USA, 2008. USENIX Association.
[236] T. H. News.         Wormgpt:    New ai tool allows cybercriminals to
      launch sophisticated cyber attacks.     https://thehackernews.com/2023/07/
      wormgpt-new-ai-tool-allows.html, 2023. Accessed: 2023-08-20.
[237] A. Ni, S. Iyer, D. Radev, V. Stoyanov, W.-t. Yih, S. Wang, and X. V. Lin. Lever:
      Learning to verify language-to-code generation with execution. In International
      Conference on Machine Learning, pages 26106–26128. PMLR, 2023.
[238] A. Nichol, P. Dhariwal, A. Ramesh, P. Shyam, P. Mishkin, B. McGrew,
      I. Sutskever, and M. Chen. Glide: Towards photorealistic image generation and
      editing with text-guided diffusion models. arXiv preprint arXiv:2112.10741,
      2021.
[239] Y. Nie, A. Williams, E. Dinan, M. Bansal, J. Weston, and D. Kiela. Adversar-
      ial nli: A new benchmark for natural language understanding. arXiv preprint
      arXiv:1910.14599, 2019.
[240] OpenAI. GPT-4 Technical Report. arXiv e-prints 2303.08774, 2023.
[241] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang,
      S. Agarwal, K. Slama, A. Ray, et al. Training language models to follow in-
      structions with human feedback. Advances in Neural Information Processing
      Systems, 35:27730–27744, 2022.
[242] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu. Unifying large language
      models and knowledge graphs: A roadmap, 2023.


                                         58
[243] G. Pang, C. Shen, L. Cao, and A. V. D. Hengel. Deep learning for anomaly
      detection: A review. ACM computing surveys (CSUR), 54(2):1–38, 2021.
[244] G. Park, B. Park, S. J. Kwon, B. Kim, Y. Lee, and D. Lee. nuqmm: Quantized
      matmul for efficient inference of large-scale generative language models. arXiv
      preprint arXiv:2206.09557, 2022.

[245] D. Patterson, J. Gonzalez, U. Holzle, Q. Le, C. Liang, L.-M. Munguia,
      D. Rothchild, D. R. So, M. Texier, and J. Dean. The carbon footprint of ma-
      chine learning training will plateau, then shrink. Computer, 55(7):18–28, 2022.
[246] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-Gavitt. Examining zero-
      shot vulnerability repair with large language models. In 2023 IEEE Symposium
      on Security and Privacy (SP), pages 2339–2356. IEEE, 2023.
[247] A. Pegoraro, K. Kumari, H. Fereidooni, and A.-R. Sadeghi. To chatgpt, or not
      to chatgpt: That is the question! arXiv preprint arXiv:2304.01487, 2023.
[248] B. Peng, C. Li, P. He, M. Galley, and J. Gao. Instruction tuning with gpt-4. arXiv
      preprint arXiv:2304.03277, 2023.
[249] J. Pennington, R. Socher, and C. D. Manning. Glove: Global vectors for word
      representation. In Proceedings of the 2014 conference on empirical methods in
      natural language processing (EMNLP), pages 1532–1543, 2014.

[250] F. Perez and I. Ribeiro. Ignore previous prompt: Attack techniques for language
      models. arXiv preprint arXiv:2211.09527, 2022.
[251] A. Podolskiy, D. Lipin, A. Bout, E. Artemova, and I. Piontkovskaya. Revisiting
      mahalanobis distance for transformer-based out-of-domain detection. In Pro-
      ceedings of the AAAI Conference on Artificial Intelligence, volume 35, pages
      13675–13682, 2021.
[252] Y. Qi, X. Zhao, and X. Huang. safety analysis in the era of large language
      models: a case study of stpa using chatgpt. arXiv preprint arXiv:2304.01246,
      2023.
[253] A. Radford, R. Jozefowicz, and I. Sutskever. Learning to generate reviews and
      discovering sentiment. arXiv preprint arXiv:1704.01444, 2017.
[254] A. Radford, K. Narasimhan, T. Salimans, I. Sutskever, et al. Improving language
      understanding by generative pre-training. OpenAI, 2018.
[255] J. W. Rae, S. Borgeaud, T. Cai, K. Millican, J. Hoffmann, F. Song, J. Aslanides,
      S. Henderson, R. Ring, S. Young, et al. Scaling language models: Methods,
      analysis & insights from training gopher. arXiv preprint arXiv:2112.11446,
      2021.




                                          59
[256] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li,
      and P. J. Liu. Exploring the limits of transfer learning with a unified text-to-
      text transformer. The Journal of Machine Learning Research, 21(1):5485–5551,
      2020.
[257] R. Ramamurthy, P. Ammanabrolu, K. Brantley, J. Hessel, R. Sifa, C. Bauckhage,
      H. Hajishirzi, and Y. Choi. Is reinforcement learning (not) for natural language
      processing?: Benchmarks, baselines, and building blocks for natural language
      policy optimization. arXiv preprint arXiv:2210.01241, 2022.
[258] A. Ramesh, P. Dhariwal, A. Nichol, C. Chu, and M. Chen.            Hierar-
      chical text-conditional image generation with clip latents. arXiv preprint
      arXiv:2204.06125, 2022.
[259] A. Ramesh, M. Pavlov, G. Goh, S. Gray, C. Voss, A. Radford, M. Chen, and
      I. Sutskever. Zero-shot text-to-image generation. In International Conference
      on Machine Learning, pages 8821–8831. PMLR, 2021.

[260] M. V. Reiss. Testing the reliability of chatgpt for text annotation and classifica-
      tion: A cautionary remark. arXiv preprint arXiv:2304.11085, 2023.
[261] J. Ren, P. J. Liu, E. Fertig, J. Snoek, R. Poplin, M. Depristo, J. Dillon, and
      B. Lakshminarayanan. Likelihood ratios for out-of-distribution detection. Ad-
      vances in neural information processing systems, 32, 2019.

[262] S. Ren, Y. Deng, K. He, and W. Che. Generating natural language adversar-
      ial examples through probability weighted word saliency. In Proceedings of
      the 57th annual meeting of the association for computational linguistics, pages
      1085–1097, 2019.
[263] X. Ren, P. Zhou, X. Meng, X. Huang, Y. Wang, W. Wang, P. Li, X. Zhang,
      A. Podolskiy, G. Arshinov, et al. Pangu-σ : Towards trillion parameter language
      model with sparse heterogeneous computing. arXiv preprint arXiv:2303.10845,
      2023.
[264] M. T. Ribeiro, S. Singh, and C. Guestrin. "why should I trust you?": Explaining
      the predictions of any classifier. In HLT-NAACL Demos, 2016.

[265] J. T. Rolfe. Discrete variational autoencoders. arXiv preprint arXiv:1609.02200,
      2016.
[266] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer. High-resolution
      image synthesis with latent diffusion models. In Proceedings of the IEEE/CVF
      Conference on Computer Vision and Pattern Recognition, pages 10684–10695,
      2022.
[267] W. Ruan, X. Huang, and M. Kwiatkowska. Reachability analysis of deep neural
      networks with provable guarantees. In IJCAI2018, pages 2651–2659, 2018.



                                           60
[268] W. Ruan, M. Wu, Y. Sun, X. Huang, D. Kroening, and M. Kwiatkowska. Global
      robustness evaluation of deep neural networks with provable guarantees for the
      hamming distance. In IJCAI2019, pages 5944–5952, 2019.
[269] S. Ruder, M. E. Peters, S. Swayamdipta, and T. Wolf. Transfer learning in
      natural language processing. In Proceedings of the 2019 Conference of the North
      American Chapter of the Association for Computational Linguistics: Tutorials,
      pages 15–18, 2019.
[270] B. Rueckauer, I.-A. Lungu, Y. Hu, M. Pfeiffer, and S.-C. Liu. Conversion of
      continuous-valued deep networks to efficient event-driven networks for image
      classification. Frontiers in neuroscience, 11:682, 2017.

[271] J. Rutinowski, S. Franke, J. Endendyk, I. Dormuth, and M. Pauly. The self-
      perception and political biases of chatgpt. arXiv preprint arXiv:2304.07333,
      2023.
[272] W. Ryou, J. Chen, M. Balunovic, G. Singh, A. Dan, and M. Vechev. Scalable
      polyhedral verification of recurrent neural networks. In International Confer-
      ence on Computer Aided Verification, pages 225–248. Springer, 2021.
[273] C. Saharia, W. Chan, S. Saxena, L. Li, J. Whang, E. L. Denton, K. Ghasemipour,
      R. Gontijo Lopes, B. Karagol Ayan, T. Salimans, et al. Photorealistic text-to-
      image diffusion models with deep language understanding. Advances in Neural
      Information Processing Systems, 35:36479–36494, 2022.

[274] S. Samanta and S. Mehta. Towards crafting text adversarial samples. arXiv
      preprint arXiv:1707.02812, 2017.
[275] G. Sandoval, H. Pearce, T. Nys, R. Karri, S. Garg, and B. Dolan-Gavitt. Lost
      at c: A user study on the security implications of large language model code
      assistants. arXiv preprint arXiv:2208.09727, 2023.
[276] T. L. Scao, A. Fan, C. Akiki, E. Pavlick, S. Ilić, D. Hesslow, R. Castagné, A. S.
      Luccioni, F. Yvon, M. Gallé, et al. Bloom: A 176b-parameter open-access
      multilingual language model. arXiv preprint arXiv:2211.05100, 2022.
[277] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal
      policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017.
[278] U.      Senate.               Senate     judiciary   subcommittee         hear-
      ing      on      oversight     of    ai.              https://techpolicy.press/
      transcript-senate-judiciary-subcommittee-hearing-on-oversight-of-ai/, 2023.
      Accessed: 2023-08-20.

[279] S. A. Seshia, D. Sadigh, and S. S. Sastry. Towards verified artificial intelligence.
      arXiv preprint arXiv:1606.08514, 2016.
[280] M. Shanahan.     Talking about large language models.               arXiv preprint
      arXiv:2212.03551, 2022.


                                           61
[281] L. Shen, S. Ji, X. Zhang, J. Li, J. Chen, J. Shi, C. Fang, J. Yin, and T. Wang.
      Backdoor pre-trained models can transfer to all. In Proceedings of the 2021
      ACM SIGSAC Conference on Computer and Communications Security, pages
      3141–3158, 2021.
[282] X. Shen, Z. Chen, M. Backes, and Y. Zhang. In chatgpt we trust? measuring
      and characterizing the reliability of chatgpt. arXiv preprint arXiv:2304.08979,
      2023.
[283] Y. Shen, Y.-C. Hsu, A. Ray, and H. Jin. Enhancing the generalization for in-
      tent classification and out-of-domain detection in slu. In Proceedings of the
      59th Annual Meeting of the Association for Computational Linguistics and the
      11th International Joint Conference on Natural Language Processing (Volume
      1: Long Papers), pages 2443–2453, 2021.
[284] Z. Shi, H. Zhang, K.-W. Chang, M. Huang, and C.-J. Hsieh. Robustness verifica-
      tion for transformers. In International Conference on Learning Representations,
      2019.

[285] K. Shuster, M. Komeili, L. Adolphs, S. Roller, A. Szlam, and J. Weston. Lan-
      guage models that seek for knowledge: Modular search & generation for dia-
      logue and prompt completion. arXiv preprint arXiv:2203.13224, 2022.
[286] K. Shuster, S. Poff, M. Chen, D. Kiela, and J. Weston. Retrieval augmentation
      reduces hallucination in conversation. arXiv preprint arXiv:2104.07567, 2021.

[287] A. Sinha, H. Namkoong, R. Volpi, and J. Duchi. Certifying some dis-
      tributional robustness with principled adversarial training. arXiv preprint
      arXiv:1710.10571, 2017.
[288] L. Smith and Y. Gal. Understanding measures of uncertainty for adversarial
      example detection. arXiv preprint arXiv:1803.08533, 2018.
[289] S. Smith, M. Patwary, B. Norick, P. LeGresley, S. Rajbhandari, J. Casper, Z. Liu,
      S. Prabhumoye, G. Zerveas, V. Korthikanti, et al. Using deepspeed and mega-
      tron to train megatron-turing nlg 530b, a large-scale generative language model.
      arXiv preprint arXiv:2201.11990, 2022.

[290] D. Sobania, M. Briesch, C. Hanna, and J. Petke. An analysis of the automatic
      bug fixing performance of chatgpt. arXiv preprint arXiv:2301.08653, 2023.
[291] S. Soltan, S. Ananthakrishnan, J. FitzGerald, R. Gupta, W. Hamza, H. Khan,
      C. Peris, S. Rawls, A. Rosenbaum, A. Rumshisky, et al. Alexatm 20b: Few-
      shot learning using a large-scale multilingual seq2seq model. arXiv preprint
      arXiv:2208.01448, 2022.
[292] L. Struppek, D. Hintersdorf, and K. Kersting. Rickrolling the artist: Injecting
      invisible backdoors into text-guided image generation models. arXiv preprint
      arXiv:2211.02408, 2022.


                                          62
[293] H. Sun, Z. Zhang, J. Deng, J. Cheng, and M. Huang. Safety assessment of
      chinese large language models. arXiv preprint arXiv:2304.10436, 2023.
[294] Y. Sun, X. Huang, D. Kroening, J. Sharp, M. Hill, and R. Ashmore. Testing
      deep neural networks. arXiv preprint arXiv:1803.04792, 2018.
[295] Y. Sun, X. Huang, D. Kroening, J. Sharp, M. Hill, and R. Ashmore. Structural
      test coverage criteria for deep neural networks. ACM Trans. Embed. Comput.
      Syst., 18(5s), Oct. 2019.
[296] Y. Sun, S. Wang, S. Feng, S. Ding, C. Pang, J. Shang, J. Liu, X. Chen, Y. Zhao,
      Y. Lu, et al. Ernie 3.0: Large-scale knowledge enhanced pre-training for lan-
      guage understanding and generation. arXiv preprint arXiv:2107.02137, 2021.
[297] Y. Sun, M. Wu, W. Ruan, X. Huang, M. Kwiatkowska, and D. Kroening. Con-
      colic testing for deep neural networks. In ASE2018, 2018.
[298] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow,
      and R. Fergus. Intriguing properties of neural networks. arXiv preprint
      arXiv:1312.6199, 2013.
[299] L. Tanguy, N. Tulechki, A. Urieli, E. Hermann, and C. Raynal. Natural language
      processing for aviation safety reports: From classification to interactive analysis.
      Computers in Industry, 78:80–95, 2016.
[300] R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and
      T. B. Hashimoto. Stanford alpaca: An instruction-following llama model, 2023.
[301] R. Taylor, M. Kardas, G. Cucurull, T. Scialom, A. Hartshorn, E. Saravia,
      A. Poulton, V. Kerkez, and R. Stojnic. Galactica: A large language model for
      science. arXiv preprint arXiv:2211.09085, 2022.
[302] A. Tejankar, M. Sanjabi, Q. Wang, S. Wang, H. Firooz, H. Pirsiavash, and L. Tan.
      Defending against patch-based backdoor attacks on self-supervised learning.
      In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
      Recognition, pages 12239–12249, 2023.
[303] S. Thakur, B. Ahmad, Z. Fan, H. Pearce, B. Tan, R. Karri, B. Dolan-Gavitt,
      and S. Garg. Benchmarking large language models for automated verilog rtl
      code generation. In 2023 Design, Automation & Test in Europe Conference &
      Exhibition (DATE), pages 1–6. IEEE, 2023.
[304] R. Thoppilan, D. De Freitas, J. Hall, N. Shazeer, A. Kulshreshtha, H.-T. Cheng,
      A. Jin, T. Bos, L. Baker, Y. Du, et al. Lamda: Language models for dialog
      applications. arXiv preprint arXiv:2201.08239, 2022.
[305] J. Thorne, A. Vlachos, C. Christodoulopoulos, and A. Mittal. Fever: A large-
      scale dataset for fact extraction and verification. In 2018 Conference of the
      North American Chapter of the Association for Computational Linguistics: Hu-
      man Language Technologies, NAACL HLT 2018, pages 809–819. Association
      for Computational Linguistics (ACL), 2018.


                                           63
[306] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix,
      B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al. Llama: Open and efficient
      foundation language models. arXiv preprint arXiv:2302.13971, 2023.
[307] A. S. Tulshan and S. N. Dhage. Survey on virtual assistant: Google assistant,
      siri, cortana, alexa. In Advances in Signal Processing and Intelligent Recog-
      nition Systems: 4th International Symposium SIRS 2018, Bangalore, India,
      September 19–22, 2018, Revised Selected Papers 4, pages 190–201. Springer,
      2019.
[308] A. Uchendu, J. Lee, H. Shen, T. Le, T. K. Huang, and D. Lee. Understanding
      individual and team-based human factors in detecting deepfake texts. CoRR,
      abs/2304.01002, 2023.
[309] M. Y. Vardi and P. Wolper. An automata-theoretic approach to automatic pro-
      gram verification. In 1st Symposium in Logic in Computer Science (LICS). IEEE
      Computer Society, 1986.
[310] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
      Ł. Kaiser, and I. Polosukhin. Attention is all you need. Advances in neural
      information processing systems, 30, 2017.
[311] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. u.
      Kaiser, and I. Polosukhin. Attention is all you need. In I. Guyon, U. V. Luxburg,
      S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors,
      Advances in Neural Information Processing Systems, volume 30. Curran Asso-
      ciates, Inc., 2017.
[312] M. Wallace, R. Khandelwal, and B. Tang. Does ibp scale? arXiv preprint, 2022.
[313] B. Wang, C. Xu, S. Wang, Z. Gan, Y. Cheng, J. Gao, A. H. Awadallah, and B. Li.
      Adversarial glue: A multi-task benchmark for robustness evaluation of language
      models. arXiv preprint arXiv:2111.02840, 2021.
[314] F. Wang, P. Xu, W. Ruan, and X. Huang. Towards verifying the geometric
      robustness of large-scale neural networks. arXiv preprint arXiv:2301.12456,
      2023.
[315] G. Wang, Y. Lin, and W. Yi. Kernel fusion: An effective method for better
      power efficiency on multithreaded gpu. In 2010 IEEE/ACM Int’l Conference on
      Green Computing and Communications & Int’l Conference on Cyber, Physical
      and Social Computing, pages 344–350. IEEE, 2010.
[316] J. Wang, X. Hu, W. Hou, H. Chen, R. Zheng, Y. Wang, L. Yang, H. Huang,
      W. Ye, X. Geng, et al. On the robustness of chatgpt: An adversarial and out-of-
      distribution perspective. arXiv preprint arXiv:2302.12095, 2023.
[317] J. Wang, X. Hu, W. Hou, H. Chen, R. Zheng, Y. Wang, L. Yang, H. Huang,
      W. Ye, X. Geng, B. Jiao, Y. Zhang, and X. Xie. On the Robustness of Chat-
      GPT: An Adversarial and Out-of-distribution Perspective. arXiv e-prints, page
      arXiv:2302.12095, Feb. 2023.


                                          64
[318] W. Wang, P. Tang, J. Lou, and L. Xiong. Certified robustness to word substitu-
      tion attack with differential privacy. In Proceedings of the 2021 Conference of
      the North American Chapter of the Association for Computational Linguistics:
      Human Language Technologies, pages 1102–1112, 2021.
[319] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery,
      and D. Zhou. Self-consistency improves chain of thought reasoning in language
      models. In The Eleventh International Conference on Learning Representations,
      2023.
[320] Y. Wang and M. Bansal. Robust machine comprehension models via adversarial
      training. arXiv preprint arXiv:1804.06473, 2018.

[321] J. Wei, S. Kim, H. Jung, and Y.-H. Kim. Leveraging large language mod-
      els to power chatbots for collecting user self-reported data. arXiv preprint
      arXiv:2301.05843, 2023.
[322] J. Wei, X. Wang, D. Schuurmans, M. Bosma, brian ichter, F. Xia, E. H. Chi,
      Q. V. Le, and D. Zhou. Chain of thought prompting elicits reasoning in large
      language models. In A. H. Oh, A. Agarwal, D. Belgrave, and K. Cho, editors,
      Advances in Neural Information Processing Systems, 2022.
[323] T.-W. Weng, H. Zhang, P.-Y. Chen, J. Yi, D. Su, Y. Gao, C.-J. Hsieh, and
      L. Daniel. Evaluating the robustness of neural networks: An extreme value
      theory approach. arXiv preprint arXiv:1801.10578, 2018.

[324] Y. Weng, M. Zhu, S. He, K. Liu, and J. Zhao. Large language models are
      reasoners with self-verification. arXiv preprint arXiv:2212.09561, 2022.
[325] Y. Weng, M. Zhu, F. Xia, B. Li, S. He, K. Liu, and J. Zhao. Neural com-
      prehension: Language models with compiled neural networks. arXiv preprint
      arXiv:2304.01665, 2023.
[326] M. Wicker, X. Huang, and M. Kwiatkowska. Feature-guided black-box safety
      testing of deep neural networks. In Tools and Algorithms for the Construction
      and Analysis of Systems: 24th International Conference, TACAS 2018, Held as
      Part of the European Joint Conferences on Theory and Practice of Software,
      ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings, Part I 24,
      pages 408–426, 2018.
[327] Y. Wolf, N. Wies, Y. Levine, and A. Shashua. Fundamental limitations of align-
      ment in large language models. arXiv preprint arXiv:2304.11082, 2023.
[328] E. Wong, L. Rice, and J. Z. Kolter. Fast is better than free: Revisiting adversarial
      training. arXiv preprint arXiv:2001.03994, 2020.
[329] D. Wu, G. Jin, H. Yu, X. Yi, and X. Huang. Optimising event-driven spiking
      neural network with regularisation and cutoff. arXiv preprint arXiv:2301.09522,
      2023.


                                           65
[330] D. Wu, X. Yi, and X. Huang. A little energy goes a long way: Build an energy-
      efficient, accurate spiking neural network from convolutional neural network.
      Frontiers in neuroscience, 16, 2022.
[331] H. Wu, W. Wang, Y. Wan, W. Jiao, and M. Lyu. Chatgpt or grammarly?
      evaluating chatgpt on grammatical error correction benchmark. arXiv preprint
      arXiv:2303.13648, 2023.
[332] M. Wu, A. Waheed, C. Zhang, M. Abdul-Mageed, and A. F. Aji. Lamini-lm:
      A diverse herd of distilled models from large-scale instructions. arXiv preprint
      arXiv:2304.14402, 2023.

[333] M. Wu, M. Wicker, W. Ruan, X. Huang, and M. Kwiatkowska. A game-based
      approximate verification of deep neural networks with provable guarantees. The-
      oretical Computer Science, 807:298–329, 2020.
[334] S. Wu, O. Irsoy, S. Lu, V. Dabravolski, M. Dredze, S. Gehrmann, P. Kambadur,
      D. Rosenberg, and G. Mann. Bloomberggpt: A large language model for fi-
      nance. arXiv preprint arXiv:2303.17564, 2023.
[335] X. Wu, K. Sun, F. Zhu, R. Zhao, and H. Li. Better aligning text-to-image models
      with human preference. arXiv preprint arXiv:2303.14420, 2023.
[336] Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. E. Staats, M. Jamnik, and C. Szegedy.
      Autoformalization with large language models. In A. H. Oh, A. Agarwal, D. Bel-
      grave, and K. Cho, editors, Advances in Neural Information Processing Systems,
      2022.
[337] F. Xu, H. Uszkoreit, Y. Du, W. Fan, D. Zhao, and J. Zhu. Explainable ai: A brief
      survey on history, research areas, approaches and challenges. In Natural Lan-
      guage Processing and Chinese Computing: 8th CCF International Conference,
      NLPCC 2019, Dunhuang, China, October 9–14, 2019, Proceedings, Part II 8,
      pages 563–574. Springer, 2019.
[338] H. Xu, K. He, Y. Yan, S. Liu, Z. Liu, and W. Xu. A deep generative distance-
      based classifier for out-of-domain detection with mahalanobis space. In Pro-
      ceedings of the 28th International Conference on Computational Linguistics,
      pages 1452–1460, 2020.
[339] H. Xu, Y. Ma, H.-C. Liu, D. Deb, H. Liu, J.-L. Tang, and A. K. Jain. Adversarial
      attacks and defenses in images, graphs and text: A review. International Journal
      of Automation and Computing, 17:151–178, 2020.
[340] J. Xu, X. Liu, Y. Wu, Y. Tong, Q. Li, M. Ding, J. Tang, and Y. Dong. Imagere-
      ward: Learning and evaluating human preferences for text-to-image generation.
      arXiv preprint arXiv:2304.05977, 2023.
[341] P. Xu, W. Ruan, and X. Huang. Quantifying safety risks of deep neural networks.
      Complex & Intelligent Systems, pages 1–18, 2022.


                                         66
[342] Yandex. Yandex/yalm-100b: Pretrained language model with 100b parameters.
      https://github.com/yandex/YaLM-100B. Accessed: 2023-08-20.
[343] J. Yang, H. Jin, R. Tang, X. Han, Q. Feng, H. Jiang, B. Yin, and X. Hu. Har-
      nessing the power of llms in practice: A survey on chatgpt and beyond. arXiv
      preprint arXiv:2304.13712, 2023.

[344] J. Yang, K. Zhou, Y. Li, and Z. Liu. Generalized out-of-distribution detection:
      A survey. arXiv preprint arXiv:2110.11334, 2021.
[345] W. Yang, L. Li, Z. Zhang, X. Ren, X. Sun, and B. He. Be careful about poi-
      soned word embeddings: Exploring the vulnerability of the embedding layers
      in nlp models. In Proceedings of the 2021 Conference of the North American
      Chapter of the Association for Computational Linguistics: Human Language
      Technologies, pages 2048–2058, 2021.
[346] Z. Yang. Chinese tech giant baidu just released its answer to chatgpt, Mar 2023.
[347] Z. Yang, Z. Dai, Y. Yang, J. Carbonell, R. R. Salakhutdinov, and Q. V. Le. Xlnet:
      Generalized autoregressive pretraining for language understanding. Advances in
      Neural Information Processing Systems, 32, 2019.
[348] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao. React:
      Synergizing reasoning and acting in language models. In The Eleventh Interna-
      tional Conference on Learning Representations, 2023.

[349] Z. Yao, R. Yazdani Aminabadi, M. Zhang, X. Wu, C. Li, and Y. He. Zeroquant:
      Efficient and affordable post-training quantization for large-scale transformers.
      Advances in Neural Information Processing Systems, 35:27168–27183, 2022.
[350] M. Ye, C. Gong, and Q. Liu. Safer: A structure-free approach for certified
      robustness to adversarial word substitutions. arXiv preprint arXiv:2005.14424,
      2020.
[351] X. Ye, S. Iyer, A. Celikyilmaz, V. Stoyanov, G. Durrett, and R. Pasunuru.
      Complementary explanations for effective in-context learning. arXiv preprint
      arXiv:2211.13892, 2022.

[352] E. Yilmaz and C. Toraman. D2u: Distance-to-uniform learning for out-of-scope
      detection. In Proceedings of the 2022 Conference of the North American Chap-
      ter of the Association for Computational Linguistics: Human Language Tech-
      nologies, pages 2093–2108, 2022.
[353] J. Yu, Y. Xu, J. Y. Koh, T. Luong, G. Baid, Z. Wang, V. Vasudevan, A. Ku,
      Y. Yang, B. K. Ayan, et al. Scaling autoregressive models for content-rich text-
      to-image generation. arXiv preprint arXiv:2206.10789, 2022.
[354] J. Zeng, X. Zheng, J. Xu, L. Li, L. Yuan, and X. Huang. Certified ro-
      bustness to text adversarial attacks by randomized [mask]. arXiv preprint
      arXiv:2105.03743, 2021.


                                          67
[355] W. Zeng, X. Ren, T. Su, H. Wang, Y. Liao, Z. Wang, X. Jiang, Z. Yang, K. Wang,
      X. Zhang, et al. Pangu-α: Large-scale autoregressive pretrained chinese lan-
      guage models with auto-parallel computation. arXiv preprint arXiv:2104.12369,
      2021.
[356] W. Zeng, X. Ren, T. Su, H. Wang, Y. Liao, Z. Wang, X. Jiang, Z. Yang, K. Wang,
      X. Zhang, et al. Pangu-α: Large-scale autoregressive pretrained chinese lan-
      guage models with auto-parallel computation. arXiv preprint arXiv:2104.12369,
      2021.
[357] Z. Zeng, K. He, Y. Yan, Z. Liu, Y. Wu, H. Xu, H. Jiang, and W. Xu. Modeling
      discriminative representations for out-of-domain detection with supervised con-
      trastive learning. In Proceedings of the 59th Annual Meeting of the Association
      for Computational Linguistics and the 11th International Joint Conference on
      Natural Language Processing (Volume 2: Short Papers), pages 870–878, 2021.
[358] C. Zhang, W. Ruan, F. Wang, P. Xu, G. Min, and X. Huang. Model-agnostic
      reachability analysis on deep neural networks. arXiv preprint arXiv:2304.00813,
      2023.
[359] C. Zhang, W. Ruan, and P. Xu. Reachability analysis of neural network control
      systems. arXiv preprint arXiv:2301.12100, 2023.
[360] J. Zhang, Y. Zhao, M. Saleh, and P. Liu. PEGASUS: Pre-training with extracted
      gap-sentences for abstractive summarization. In H. D. III and A. Singh, editors,
      Proceedings of the 37th International Conference on Machine Learning, vol-
      ume 119 of Proceedings of Machine Learning Research, pages 11328–11339.
      PMLR, 13–18 Jul 2020.
[361] S. Zhang, S. Roller, N. Goyal, M. Artetxe, M. Chen, S. Chen, C. Dewan,
      M. Diab, X. Li, X. V. Lin, et al. Opt: Open pre-trained transformer language
      models. arXiv preprint arXiv:2205.01068, 2022.
[362] T. Zhang, F. Ladhak, E. Durmus, P. Liang, K. McKeown, and T. B. Hashimoto.
      Benchmarking large language models for news summarization. arXiv preprint
      arXiv:2301.13848, 2023.

[363] Y. Zhang, A. Albarghouthi, and L. D’Antoni. Certified robustness to pro-
      grammable transformations in lstms. arXiv preprint arXiv:2102.07818, 2021.
[364] R. Zhao, X. Li, Y. K. Chia, B. Ding, and L. Bing. Can chatgpt-like generative
      models guarantee factual accuracy? on the mistakes of new generation search
      engines. arXiv preprint arXiv:2304.11076, 2023.

[365] W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang,
      J. Zhang, Z. Dong, et al. A survey of large language models. arXiv preprint
      arXiv:2303.18223, 2023.




                                         68
[366] X. Zhao, W. Huang, X. Huang, V. Robu, and D. Flynn. Baylime: Bayesian
      local interpretable model-agnostic explanations. In C. de Campos and M. H.
      Maathuis, editors, Proceedings of the Thirty-Seventh Conference on Uncertainty
      in Artificial Intelligence, volume 161 of Proceedings of Machine Learning Re-
      search, pages 887–896. PMLR, 27–30 Jul 2021.

[367] X. Zhao, W. Huang, S. Schewe, Y. Dong, and X. Huang. Detecting operational
      adversarial examples for reliable deep learning. In 2021 51st Annual IEEE/IFIP
      International Conference on Dependable Systems and Networks - Supplemental
      Volume (DSN-S), pages 5–6, 2021.
[368] Z. Zhao, D. Dua, and S. Singh. Generating natural adversarial examples. arXiv
      preprint arXiv:1710.11342, 2017.
[369] Q. Zhong, L. Ding, J. Liu, B. Du, and D. Tao. Can chatgpt understand
      too? a comparative study on chatgpt and fine-tuned bert. arXiv preprint
      arXiv:2302.10198, 2023.

[370] C. Zhou, Q. Li, C. Li, J. Yu, Y. Liu, G. Wang, K. Zhang, C. Ji, Q. Yan, L. He,
      et al. A comprehensive survey on pretrained foundation models: A history from
      bert to chatgpt. arXiv preprint arXiv:2302.09419, 2023.
[371] W. Zhou, F. Liu, and M. Chen. Contrastive out-of-distribution detection for
      pretrained transformers. In Proceedings of the 2021 Conference on Empirical
      Methods in Natural Language Processing (EMNLP), 2021.

[372] Y. Zhou, P. Liu, and X. Qiu. Knn-contrastive learning for out-of-domain intent
      classification. In Proceedings of the 60th Annual Meeting of the Association for
      Computational Linguistics (Volume 1: Long Papers), pages 5129–5141, 2022.
[373] R.-J. Zhu, Q. Zhao, and J. K. Eshraghian. Spikegpt: Generative pre-trained
      language model with spiking neural networks. arXiv preprint arXiv:2302.13939,
      2023.
[374] D. M. Ziegler, N. Stiennon, J. Wu, T. B. Brown, A. Radford, D. Amodei,
      P. Christiano, and G. Irving. Fine-tuning language models from human pref-
      erences. arXiv preprint arXiv:1909.08593, 2019.




                                         69
