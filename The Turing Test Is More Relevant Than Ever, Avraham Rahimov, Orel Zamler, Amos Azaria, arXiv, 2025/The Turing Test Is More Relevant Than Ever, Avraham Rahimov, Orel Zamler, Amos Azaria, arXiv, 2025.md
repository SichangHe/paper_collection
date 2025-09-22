# The Turing Test is More Relevant Than Ever

Avraham Rahimov, Orel Zamler, and Amos Azaria

School of Computer Science Ariel University, Israel

*"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human."*

Alan Turing, 1950

# Abstract

The Turing Test, first proposed by Alan Turing in 1950, has historically served as a benchmark for evaluating artificial intelligence (AI). However, Since the release of ELIZA in 1966, and particularly with recent advancements in large language models (LLMs), AI has been claimed to pass the Turing Test. Furthermore, criticism argues that the Turing Test primarily assesses deceptive mimicry rather than genuine intelligence, prompting the continuous emergence of alternative benchmarks. This study argues against discarding the Turing Test, proposing instead using more refined versions of it, for example, by interacting simultaneously with both an AI and human candidate to determine who is who, allowing a longer interaction duration, access to the Internet and other AIs, using experienced people as evaluators, etc.

Through systematic experimentation using a web-based platform, we demonstrate that richer, contextually structured testing environments significantly enhance participants' ability to differentiate between AI and human interactions. Namely, we show that, while an off-the-shelf LLM can pass some version of a Turing Test, it fails to do so when faced with a more robust version. Our findings highlight that the Turing Test remains an important and effective method for evaluating AI, provided it continues to adapt as AI technology advances. Additionally, the structured data gathered from these improved interactions provides valuable insights into what humans expect from truly intelligent AI systems.

# 1 Introduction

The Turing Test, proposed by Alan Turing in 1950 [\(Turing](#page-10-0) , [1950\)](#page-10-0), has historically served as

a foundational benchmark for assessing artificial intelligence (AI). Over the decades, several AI systems—most notably ELIZA [\(Weizenbaum](#page-10-1) , [1966\)](#page-10-1) and Eugene Goostman [\(Warwick and Shah](#page-10-2) , [2016\)](#page-10-2)—have claimed to pass variations of this test, often sparking debate over its adequacy as a measure of genuine intelligence. Recently, the consensus has shifted: modern large language models (LLMs) such as GPT-4 [\(Bubeck et al.](#page-9-0) , [2023\)](#page-9-0) convincingly pass traditional forms of the Turing Test, diminishing its perceived relevance. Critics argue that this benchmark is primarily focused on deception rather than meaningful intelligence, prompting researchers to continually propose new benchmarks which, though initially challenging, are often surpassed within months [\(Srivastava et al.,](#page-9-1) [2022\)](#page-9-1).

Despite such criticisms, this paper argues that dismissing the Turing Test as outdated overlooks its significant potential as an ultimate evaluation of general intelligence, provided it is adapted to contemporary AI advancements. Rather than abandoning it, we propose that the Turing Test can—and should—be updated. Modern adaptations could include extended interaction times, engagement with domain experts as evaluators, enabling real-world interactions (such as placing online orders, composing a presentation, building websites, and creating videos), or incorporating audio and video communication. Moreover, contemporary versions of the test might allow both AI and human participants to leverage the Internet and even collaborate with other AIs. The human responder could be an expert in their field, for example, an expert software programmer. Crucially, the test should strongly incentivize human testers to pose meaningful challenges and human responders to convincingly demonstrate their authenticity.

If an AI consistently remains indistinguishable from a human across diverse, extended, and complex interactions, this would provide robust evidence of achieving genuine human-level intelligence (albeit, in the virtual world). Furthermore, data collected from these enriched interactions would offer invaluable insights, accurately reflecting human expectations and standards for general intelligence.

To systematically explore these issues, we introduce a modern web-based platform designed to examine two different environment settings of the Turing test, which we refer to as simple and enhanced.

In the simple variant, which is based on the experiment conducted by [\(Biever,](#page-9-2) [2023\)](#page-9-2), a human interacts briefly with a single candidate and must determine if she was conversing with an AI or a human. However, in the enhanced variant, we take several measures to ensure a more robust test, with the most significant difference being that the participants interact using a dual-chat interface. That is, the human participants (testers) simultaneously interact with both a human (responder) and an AI chatbot without knowing who is who. This allows the tester to compare the responses obtained from both parties when deciding who is human and who is an AI chatbot.

The primary objectives of this research are threefold. First, we aim to establish a standardized and reproducible environment for conducting Turing Test experiments. Second, we investigate how environmental factors, such as participant selection, conversation duration, and interface design, influence the overall human-AI interaction, rather than just AI performance. Finally, we assess the impact of engagement strategies and incentives on user participation and decision-making, while also comparing the effectiveness of simple versus enhanced Turing Tests in differentiating between AI and human intelligence. To the best of our knowledge, this is the first work to compare the performance (with respect to passing the Turing test) of identical models, in two different environments.

By emphasizing the key differences between simple and enhanced Turing Tests, this study demonstrated the necessity of refining AI evaluation methodologies rather than abandoning the Turing Test altogether. The experimental environment, participant composition, and testing duration all play essential roles in determining evaluation outcomes. Our findings contribute to ongoing discussions in AI research by demonstrating that while AI may easily deceive users in simplistic settings, more comprehensive and structured tests reveal deeper

limitations, reinforcing the relevance of the Turing Test as an important benchmark for evaluating general intelligence. Indeed, now that modern LLMs excel at generating convincing language, achieving high performance on a well-designed Turing Test requires AI to demonstrate true human-level intelligence across diverse tasks, rather than merely mimicking human-like conversation.

# 2 Related Work

The Turing Test [\(Turing,](#page-10-0) [1950\)](#page-10-0) was designed as an operational criterion for machine intelligence. In its original formulation, commonly referred to as the "imitation game", a human judge (interrogator) engages in a text-based conversation with both a human and a machine simultaneously, without knowing which is which. If the judge cannot reliably distinguish between them, the machine is said to exhibit intelligent behavior. While Turing did not specify a strict numerical threshold for passing the test, later interpretations often cite a benchmark of around 66.7-70%, i.e., if only two-thirds or less, of human testers correctly identify the machine as non-human, the machine is considered to have passed the test. In addition, [\(Jones and Bergen,](#page-9-3) [2025\)](#page-9-3) propose that passing the Turing test requires that success rate will be non-statistically significant lower than 50%.

The Loebner Prize competition was a practical instantiation of Turing's original ideas [\(Bradeško](#page-9-4) [and Mladenic´,](#page-9-4) [2012\)](#page-9-4), held annually from 1991 until its discontinuation in 2019. A 2012 survey of chatbot systems developed for the competition highlights that, at the time, many chatbots were able to superficially mimic human conversation but largely relied on pre-scripted responses and heuristic rules rather than genuine contextual understanding. As a result, these systems often failed to maintain sustained coherence or handle open-ended or ambiguous queries. The competition has drawn substantial criticism over the years, including concerns that it prioritized deception over intelligence, encouraged superficial ELIZA-style gimmicks, and relied on untrained judges making quick decisions under overly constrained conditions. While such critiques were valid, especially given the technical limitations of the time, the discontinuation of the prize coincided with the emergence of LLMs, which are capable of generating contextually rich, coherent, context-sensitive responses across a wide range of topics. As a result, the key challenge for

AI is no longer simply producing human-like conversation, which current LLMs can achieve to some extent, but demonstrating deeper forms of intelligence, such as reasoning, abstraction, adaptability, and the ability to perform complex tasks, which the original Turing Test implicitly aimed to evaluate.

Indeed, several recent studies have attempted to evaluate LLMs through variations of the Turing Test. In [\(Jannai et al.,](#page-9-5) [2023\)](#page-9-5), Jannai et al. conducted a large-scale study, by introducing the online game *"Human or Not?"*. In this game, over 1.5 million participants engaged in short conversations with either a human or an AI model, after which they had to indicate whether they were interacting with another human or with an AI. When interacting with an AI, only 62% of the humans correctly identified it as an AI. Thus, Jannai et al. conclude that their prompt engineered LLM has passed the Turing test. However, despite its large-scale participation, the experimental design introduces several critical flaws.

First, the interaction was conducted with only a single chat, so one could not compare the behavior of the AI to that of a real human. In addition, the participants were not assigned specific roles, with one being a tester and the other being a responder, and instead, the humans and the AI also played the role of a tester and also of a responder. Furthermore, the participants were not provided clear instructions, so some participants took the role of an AI, and attempted to answer as an AI would answer instead of acting like a human. Additionally, each interaction lasted only two minutes, with an average of 4-5 messages per participant. Such brief exchanges fail to expose deeper cognitive limitations of AI, such as long-term coherence, contextual understanding, and abstract reasoning.

Finally, the conversation structure followed a rigid alternating messages format, with predefined message length limits and time gaps. This artificially equalized AI-human communication prevents AI from exhibiting more nuanced weaknesses that would arise in unrestricted conversation. Furthermore, the study incorporated predefined AI personalities, backstories, and deliberate behavioral modifications, such as intentional delays, slang usage, and humor injection. These artificial enhancements biased the test by assessing the effectiveness of deception strategies rather than the AI's raw ability to engage in human-like dialogue.

Therefore, the study does not indicate that AI is

capable of full human-like cognition, as suggested by the original Turing test, but only demonstrates that AI can be optimized for passing a very simple version of the Turing test, one in which humans do not perform well.

Jones and Bergen [\(Jones and Bergen,](#page-9-6) [2024\)](#page-9-6) show that by prompt engineering GPT-4, it can successfully passed the Turing Test. In their experiment, which was very similar to that of Jannai et al. [\(Jannai et al.,](#page-9-5) [2023\)](#page-9-5), humans correctly identified their AI opponent only 46% of the cases, i.e, human judges classified GPT-4 as human 54% of cases. Jones and Bergen's study suffers from all the aforementioned flaws (except experiment duration which was slightly longer at 5-minutes). Forthermore, we note that according to the logic of the Turing test, a machine should never "outperform" humans on this type of test, and the optimal performance of a machine should not exceed 50%. Obtaining human performance levels below 50% indicates that the experiment was not performed correctly.

Jones and Bergen [\(Jones and Bergen,](#page-9-3) [2025\)](#page-9-3) introduce a three-party chat interface—where a human tester simultaneously converses with a human responder and an AI system. In this implementation, each experimental round was limited to 5 minutes, and the observed median chat duration was approximately 4.2 minutes. The median number of messages per conversation was about 8 (roughly 4 from each participant), a figure notably lower than the 14 messages per conversation observed in our own experiments. Each participant completed 8 rounds, interacting with different AI models and interchangeably serving as a tester or as a responder. This raises the concern that repeated exposure may induce a bias in the tester's ability to detect the AI. For instance, a tester who correctly identifies the AI in one round, may expect a similar behavior of the AI in a following round and thus, may be more prone to misclassify it if using a different model. In addition, serving both as a tester and a responder may cause confusion, especially since the instructions for both roles were provided together. Indeed, as shown by the authors, the ability to detect the AI *decreases* over time, which is completely counter intuitive for a well performed Turing test. Furthermore, only 76% of the testers correctly identified the simple ELIZA bot, further indicating that the environment is problematic and unrepresentative. It is important to note that neither

a pre-quiz to check participant understanding nor any bonus mechanism for accurate identification was implemented in this study.

Temtsin et al. [\(Temtsin et al.,](#page-10-3) [2025\)](#page-10-3) present an investigation based on the Computer-Imitates-Human Game (CIHG), a variant of the classic threeparty imitation game. Their approach employs a third-party interface that allows for unconstrained chat durations, in contrast to the fixed 5-minute limit used by Jones and Bergen. With these settings, the study reports that GPT-4 Turbo was identified as a bot in 97% of the cases. The findings underscore that longer interaction durations provide interrogators with more conversational evidence, thereby improving their ability to correctly distinguish between human and machine interlocutors. Similar to the previous study, no pre-quiz or bonus mechanisms were incorporated.

In the study *ChatGPT-4 in the Turing Test* by Restrepo [\(Restrepo Echavarría,](#page-9-7) [2025\)](#page-9-7), the experiment was conducted using WhatsApp over approximately 7 minutes per session. In a series of 10 Turing Test experiments, interrogators correctly identified ChatGPT-4 as the machine in 9 out of 10 cases. Although a simple binomial calculation—assuming a 50% chance level—yields a probability of about 0.98% for achieving 9 correct identifications out of 10 by chance, the very small sample size (only 10 experiments) limits the statistical power and robustness of the conclusion. Thus, while the results are indicative, the limited number of experimental sessions precludes a definitive inference.

It should be noted that none of these studies implemented mechanisms such as a pre-test quiz to ensure participant engagement or a bonus system to motivate accurate identification. In contrast, the Enhanced Turing Test environment presented in our work incorporates both a pre-quiz and a bonus payment system. These additions are designed to motivate participants to engage in extended, naturalistic conversations and to filter out unserious participation. Our modifications aim to provide a more robust experimental setting by promoting longer chat durations, increasing the number of messages exchanged, and ensuring that clear instructions are given to all participants. Such enhancements are critical for obtaining more reliable and interpretable data regarding the human likeness of AI behavior. Furthermore, to the best of our knowledge, this is the first paper to evaluate the performance of AI models in different environmental

settings.

A broader perspective on AI evaluation challenges was provided by Biever in [\(Biever,](#page-9-2) [2023\)](#page-9-2). This paper argues that since current AI can pass the Turing test, and that AI agents are capable of convincingly acting like humans, the Turing test is no longer relevant. Therefore, the paper suggests that researchers should focus only on other benchmarks, such as ConceptARC [\(Moskvichev et al.,](#page-9-8) [2023\)](#page-9-8), which evaluate AI on abstract reasoning tasks.

While this paper correctly highlights the need for more rigorous testing, it underestimates the importance of refining the Turing Test itself. Instead of discarding it altogether, improving the test environment can yield more reliable evaluations. A more robust Turing Test should involve longer conversations to assess deep coherence, incorporate multimodal interactions such as text, voice, and video to expose deeper weaknesses and introduce real-time unpredictability to prevent AI from relying on pre-learned heuristics.

Thus, while the authors correctly identify current test weaknesses, their argument for disregarding the Turing Test may be premature. Instead of abandoning it, a more rigorous version should be designed to account for AI deception strategies.

# 3 Experimental Design

We conducted four experiments categorized into two Turing test variants: *Simple* and *Enhanced*. Each test was performed both with and without prompt engineering.

### 3.1 Simple Turing Test

The Simple Turing Test was designed as a streamlined interaction, where participants engaged in a conversation within a single chat window without knowing their conversation partner's true identity. Although the second participant was randomly assigned from the first participant's perspective, it was always an AI.

Each interaction lasted two minutes, after which participants were asked to determine whether they had been conversing with a human or an AI. This design closely follows the methodology outlined in [\(Jannai et al.,](#page-9-5) [2023\)](#page-9-5), with the key difference that human-human interactions were excluded, as they were not relevant to the objectives of this study.

Participants in the Simple Turing Test received a fixed compensation of \$0.50, with no opportunity for additional bonuses. The estimated total

duration, including the conversation and a postexperiment survey, was approximately 3 minutes and 24 seconds on average.

Figure [1](#page-4-0) shows the home page where participants are instructed to fill demographic information and to accept their participation in the experiment, and Figure [2](#page-4-1) presents the chat interface used in the Simple Turing Test, depicting a human participant interacting with a prompt-engineered AI.

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 1: Simple Turing Test - Home page (Demographic information)

#### 3.2 Enhanced Turing Test

The *Enhanced Turing Test* introduced a dual-chat format. Upon joining, participants were assigned one of two roles: *tester* or *responder*. The tester was presented with two chat windows—one connected to a human (the responder) and the other to an AI. However, the tester was not informed which was which. The responder's objective was to convince the tester of their human identity while assisting in identifying the AI. In essence, the tester and responder collaborated to detect the AI. To encourage both human participants (the tester and the responder) to adhere to their roles, we offered a bonus to both parties if the tester correctly identified the human and the AI. To avoid confusion, each participant received instructions related only to his or her own role; the instructions included the bonus information. After viewing the instructions, a simple quiz was used to filter out inattentive participants.

Each interaction lasted five minutes, after which

<span id="page-4-1"></span>![](_page_4_Figure_7.jpeg)

Figure 2: Simple Turing Test - Chat Interface. Participants interacted with a prompt-engineered AI in a single chat window.

the tester submitted their judgment regarding which chat contained the AI and which contained the human. Following their selection, testers completed a brief post-experiment survey.

To reduce potential biases, the positions of the chat windows were randomized for each participant. Additionally, an inactivity detection system was implemented to ensure active engagement.

The base compensation was \$0.50 and the bonus was set to \$0.50 as well, bringing the total possible payment to \$1.00. The estimated total duration, including the chat and the post-experiment survey, was approximately 8 minutes and 58 seconds on average.

Figure [3](#page-5-0) illustrates the home page of the Enhanced test, which is similar to the home page of the Simple test with the same demographic information gathered. Figures [4](#page-5-1) and [5](#page-5-2) illustrate the interfaces used in the Enhanced Turing Test, depicting the perspectives of testers and responders.

From a technical standpoint, the system was implemented using modern web technologies, featuring a React.js frontend, a Python Flask backend, and MongoDB for data storage. This architecture facilitated real-time communication, robust data collection, and scalable deployment. The system logged various interaction metrics, including response times, user engagement levels, and accuracy rates in distinguishing AI from human participants.

The experiments were conducted via Amazon

Mechanical Turk, a widely utilized platform for human-subject studies [\(Paolacci et al.,](#page-9-9) [2010\)](#page-9-9). To ensure data quality, participants were required to meet the following eligibility criteria: a task approval rate exceeding 99%, completion of more than 1,000 approved tasks, and verified residency in the USA.

<span id="page-5-0"></span>

| 9 _ E     | ome to the Turing Test Exper                                             | E E       |
|-----------|--------------------------------------------------------------------------|-----------|
| 🔆 Can a   | computer (bot) fool you and your human team                              | mate?     |
| QVQ       | It's two humans against one bot. Who will win?                           |           |
| A O A     | E & O & O & E & O & O & O                                                | E /2      |
|           | Please fill in the following fields to start the experiment:             | - 4ª      |
|           | Gender:                                                                  | 0 0       |
| * A )     | Select                                                                   | all.      |
| Q C       |                                                                          | An An     |
| a the     | Age:                                                                     | E R       |
| Ē         | Select ~                                                                 | 0 4       |
|           | Educational Degree:                                                      | (E _ @)   |
| × 6       | Select V                                                                 | 100       |
| Q Ž @     | Steer                                                                    | An<br>LA  |
| a Pa      | Employment Status:                                                       |           |
| ) D _     | Select ~                                                                 | 0         |
|           |                                                                          | Q. Q      |
| X B       | Country of Residence:                                                    | A Co      |
| Q Ž @     | Select                                                                   | An<br>FA  |
| a Ch      | Experience with AI:                                                      | E B       |
| . Ð _     | Select 🗸                                                                 | 0 4       |
| (no       |                                                                          | C. C      |
| × 3       |                                                                          | 00        |
| Q I agree | e to participate in the experiment, and agree for the data to be used in | research. |
| 1 ( ) A   | E B & A Start B & A &                                                    |           |

Figure 3: Enhanced Turing Test - Home page with Demographic information

<span id="page-5-1"></span>![](_page_5_Figure_3.jpeg)

Figure 4: Enhanced Turing Test - Tester Interface. The tester interacts with both an AI and a human in two separate chat windows.

### 3.3 Prompt Engineering Usage

For each of the Turing test variants, we evaluated two models, one with prompt engineering and one without.

The prompt instructed the chatbot to mimic a human persona and convincingly pose as a human participant (see Listing [1](#page-5-3) for the key prompt guidelines used to simulate human-like behavior).

<span id="page-5-2"></span>![](_page_5_Figure_8.jpeg)

Figure 5: Enhanced Turing Test - Responder Interface. The responder engages in a conversation with the tester, aiming to convince the tester of being human.

<span id="page-5-3"></span>Listing 1: Key Prompt Guidelines for Human-like Behavior.

```
Core_Persona :
- Mimics a real person with emotions ,
    sarcasm , and quirks .
Behavioral_Guidelines :
1. Natural_Imperfection :
   - Occasional typos , self - corrections ,
        and informal punctuation .
2. Human_Like_Responses :
   - Avoids robotic tone , shows
       hesitation , and changes mind
       occasionally .
3. Conversational_Style :
   - Varies response length , uses pauses
        (...) , and occasional emojis /
       slang .
4. Engagement :
   - References past messages , shares
       personal anecdotes , reacts
       contextually .
5. Avoidances :
   - Never admits being AI , avoids
       formal or repetitive responses .
```

All experiments used the Llama 3.2 1B model via OpenRouter's API [\(Touvron et al.,](#page-10-4) [2023;](#page-10-4) [Open-](#page-9-10)[Router,](#page-9-10) [2024\)](#page-9-10).

# 4 Experimental Results

We evaluate two versions of the LLM, one with prompt engineering, and one without.

We use a χ 2 test for independence [\(Pearson,](#page-9-11) [1900\)](#page-9-11) to determine whether participant performance differs significantly between the *Simple* and *Enhanced* Turing Test variants.

The null hypothesis (*H0*) assumes that the test type does not affect participant accuracy. The alternative hypothesis (*HA*) suggests a significant difference between the two test formats.

### 4.1 Comparison: No Prompt Engineering

We first evaluate whether participants performed differently in the Simple and Enhanced Turing Tests when no prompt engineering was applied. Table [1](#page-6-0) presents the observed results. The sample size was nSimple = 41 and nEnhanced = 29.

<span id="page-6-0"></span>Table 1: Correct and Incorrect Guesses in Simple vs. Enhanced Turing Test (No Prompt Engineering)

| Test Type            | Correct | Incorrect |
|----------------------|---------|-----------|
| Simple (No Prompt)   | 28      | 13        |
| Enhanced (No Prompt) | 27      | 2         |

A chi-squared test for independence yields χ 2 (1) = 4.97, p = 0.026. Since p < 0.05, we reject *H<sup>0</sup>* and conclude that the Enhanced Turing Test significantly improved participant accuracy, even without prompt engineering.

### 4.2 Comparison: Prompt Engineering

We next examine whether prompt engineering influenced participant accuracy under the two test formats. Table [2](#page-6-1) presents the observed results. The sample size was nSimple = 41 and nEnhanced = 31.

<span id="page-6-1"></span>Table 2: Correct and Incorrect Guesses in Simple vs. Enhanced Turing Test (Prompt Engineering)

| Test Type            | Correct | Incorrect |
|----------------------|---------|-----------|
| Simple (w/ Prompt)   | 18      | 23        |
| Enhanced (w/ Prompt) | 22      | 9         |

The chi-squared test yields χ 2 (1) = 6.21, p = 0.013. Again, since p < 0.05, we reject *H<sup>0</sup>* and find that prompt engineering has a significant effect, with the Enhanced test facilitating improved detection.

### 4.3 Summary of Findings

Table [3](#page-6-2) summarizes accuracy levels across all four experiments. Results indicate that the Enhanced Turing Test consistently led to higher accuracy, regardless of whether prompt engineering was applied.

Table 3: Overall Turing Test Results

<span id="page-6-2"></span>

| Test Type            | Correct | Accuracy |
|----------------------|---------|----------|
| Simple (No Prompt)   | 28      | 68.29%   |
| Enhanced (No Prompt) | 27      | 93.10%   |
| Simple (w/ Prompt)   | 18      | 43.90%   |
| Enhanced (w/ Prompt) | 22      | 70.97%   |

The largest discrepancy appears in the promptengineered condition, where accuracy increased from 43.9% in the Simple Test to 70.97% in the Enhanced Test. This suggests that the dual-chat setting plays a critical role in helping participants detect subtle AI behaviors that would otherwise go unnoticed in single-chat scenarios.

A statistical summary of chi-squared results is provided in Table [4.](#page-6-3)

<span id="page-6-3"></span>Table 4: Summary of Chi-Squared Tests Comparing Test Types

| Simple vs. Enhanced | 2<br>χ<br>(df=1) | p-Value |
|---------------------|------------------|---------|
| No Prompt           | 4.97             | 0.026   |
| With Prompt         | 6.21             | 0.013   |

# 5 Additional Analysis

We analyze participant-level factors—AI experience, gender, and age—and their impact on the ability to distinguish between human and AI interlocutors. All statistical analyses employ Pearson's χ 2 test [\(Pearson,](#page-9-11) [1900\)](#page-9-11).

### 5.1 AI Experience and Performance Trends

Figure [6](#page-6-4) shows accuracy across experience levels (basic, intermediate, advanced) for each test condition.

<span id="page-6-4"></span>![](_page_6_Figure_22.jpeg)

Figure 6: Accuracy by AI experience level in the Simple and Enhanced tests, with and without prompt engineering.

### Key Observations:

- Enhanced vs. Simple: Enhanced tests yielded higher accuracy across all experience levels.
- Advanced users: In the Simple test with prompts, advanced users performed worse than intermediates, possibly due to overconfidence or misaligned expectations.

• Prompt sensitivity: Prompt engineering amplified differences in user performance between test types.

### 5.2 Demographic Effects

### Simple Test – Gender and Age Effects

We analyzed gender and age influences within the Simple variants.

- Simple (No Prompt): Gender: χ 2 (1) < 0.01, p = 1.00; Age (excluding empty 70+ bin): χ 2 (4) = 1.92, p = 0.75.
- Simple (With Prompt): Gender: χ 2 (1) = 0.28, p = 0.60; Age: χ 2 (5) = 2.82, p = 0.73.
- Pooled Simple Variants: Gender: χ 2 (1) = 0.19, p = 0.66; Age: χ 2 (5) = 2.62, p = 0.76.

Across all Simple test settings, none of the gender or age comparisons reached statistical significance. This suggests that in these settings, participants' ability to distinguish AI from human responses did not differ meaningfully by demographic group.

#### Enhanced Test – Gender and Age Effects

We repeated the demographic analysis for the Enhanced test conditions:

- Enhanced (No Prompt): Gender: χ 2 (1) = 0.18, p = 0.67; Age: χ 2 (5) = 0.24, p = 0.999.
- Enhanced (With Prompt): Gender: χ 2 (1) < 0.01, p = 1.00; Age: χ 2 (4) = 0.25, p = 0.993.
- Pooled Enhanced Variants: Gender: χ 2 (1) = 0.05, p = 0.82; Age: χ 2 (5) = 2.15, p = 0.83.

As with the Simple test, no statistically significant demographic effects were observed in the Enhanced test. These results further support the conclusion that gender and age were not major drivers of performance in our task.

We now present the accuracy of the testers in the Enhanced-Test setting when interacting with the model with Prompt-Engineering by conversation category. To that end we categorize each conversation by topic using the cosine similarity between

Table 5: Accuracy (%) by Gender

| Condition              | Male | Female |
|------------------------|------|--------|
| Simple (No Prompt)     | 72%  | 65%    |
| Simple (With Prompt)   | 39%  | 53%    |
| Enhanced (No Prompt)   | 100% | 88%    |
| Enhanced (With Prompt) | 73%  | 69%    |

Table 6: Accuracy (%) by Aggregated Age Group (Ages 20–50 = mean of 20–30, 30–40, 40–50; Ages 50+ = mean of 50–60, 60–70, 70+)

| Condition              | 20–50 | 50+   |
|------------------------|-------|-------|
| Simple (No Prompt)     | 37.0% | 45.0% |
| Simple (With Prompt)   | 26.0% | 41.7% |
| Enhanced (No Prompt)   | 48.0% | 46.7% |
| Enhanced (With Prompt) | 45.7% | 31.7% |

the etire conversation and each category using the embeddings obtained from the *BERT all-MiniLM-L6-v2* model [\(Hugging Face,](#page-9-12) [2024\)](#page-9-12). We use the 15 topics that appear in [\(Jones and Bergen,](#page-9-3) [2025\)](#page-9-3) for the set of topics.

Figure [7](#page-7-0) presents the success rate of each topic of conversation and the number of conversations in each topic (omitting any topic with no conversations).

<span id="page-7-0"></span>![](_page_7_Figure_21.jpeg)

Figure 7: Accuracy by conversation topic

As depicted by the figure, the most frequent topic was *Weather*, with 11 conversations; this was followed by *Bot or Human* and *Daily Activities*, which is unsurprising given that participants were not constrained to any particular subject, making these general topics default choices. The success rate does not vary much among these three topics, with weather's success rate at 72.7% and daily activities slightly lower at 66.7% (below the overall success rate of 70.97%).

However, the next five topics had only one or

two conversations each, these topics include humor, logic & math, request for personal details, accusation, and human experience. Interestingly, these topics, which can be viewed as more creative and unique, obtained overall a success rate of 83.3%, which is higher than the three frequent topics.

# 6 Discussion

This study highlights the critical role of the testing environment in evaluating AI intelligence using the Turing Test. The results demonstrate that the Enhanced Turing Test presents a significantly greater challenge for AI models compared to the Simple Turing Test, reinforcing the importance of well-structured evaluations. Our results suggest that when a more rigorous and prolonged test is implemented, AI struggles to sustain the illusion of human-like intelligence over time.

Yet, intelligence extends beyond textual conversation. Humans exhibit cognitive abilities that include reasoning, perception, creativity, motor skills, and emotional awareness. If AI is to be meaningfully compared to human intelligence, it must be tested across multiple modalities, incorporating not only text-based interactions but also other aspects of cognitive function.

We propose the Ultimate Turing Test (or Turing Test 2.0) which builds upon the Turing Test by evaluating AI across multiple dimensions, ensuring a more comprehensive assessment. Unlike traditional tests that focus solely on language, this test would assess AI's competence in areas such as visual recognition, where the AI must interpret and analyze images and videos in a meaningful way; speech and emotional intelligence, requiring AI to understand tone, sarcasm, and nuanced communication; and multimodal creativity, where AI would need to demonstrate the ability to generate original content across different artistic and problemsolving domains. Additionally, it would involve more advanced reasoning and programming challenges, testing whether an AI can autonomously write and debug code or develop functional applications. The tester should have experience with detecting LLMs, and the responder can be an expert in some field (e.g, a software engineer). Indeed, A more nuanced Turing Test can focus on specific fields (e.g, software engineering, art designers, etc.).

A true test of intelligence should not be constrained by text-based interactions alone. Instead, it should extend to evaluating AI's ability to interact in physical environments, demonstrating adaptability, problem-solving, and learning in real-world scenarios. Such a test would not only provide a clearer measure of AI's cognitive depth but also help distinguish between mere linguistic mimicry and genuine comprehension.

# 7 Conclusion & Future Work

This study emphasizes the importance of the testing environment in evaluating AI conversational abilities through the Turing Test. The results show that the Enhanced Turing Test provides a more rigorous and revealing assessment than the Simple Turing Test. As demonstrated in this paper, when AI is tested under structured and demanding conditions, its performance declines significantly.

Another key finding is that human evaluators' ability to distinguish AI from humans is influenced by factors such as age and prior experience with AI. This highlights the need to consider both AI performance and human judgment biases when designing evaluation methodologies.

Rather than treating the Turing Test as a fixed benchmark, our findings suggest that it should evolve alongside advancements in AI. A more refined and structured approach to evaluation is essential to ensure a meaningful assessment of AI's conversational capabilities.

Building on these findings, several areas of future research can help improve AI evaluation methodologies.

Expanding AI evaluation to multimodal Turing Tests is an essential step. Current tests focus primarily on text-based interactions, but future studies should assess AI in voice and video-based conversations. Evaluating AI's ability to replicate human-like behaviors across different communication channels will provide a more comprehensive understanding of its strengths and limitations.

Long-term interactions are another critical challenge. AI models often struggle to maintain logical consistency and adaptability over extended conversations. Future research should explore whether AI can sustain coherent and contextually aware discussions over time, offering deeper insights into its conversational intelligence.

Additionally, cognitive biases among human evaluators can influence Turing Test results. Future studies should focus on developing standardized evaluation frameworks, participant training methods, and bias-mitigation techniques to improve the reliability and objectivity of AI assessments. Understanding how different demographic groups perceive AI interactions can help create fairer and more accurate testing methodologies.

# 8 Limitations

Despite the robustness of our experimental design, several limitations must be acknowledged.

Participant Compliance: Despite implementing a qualification quiz and warning system, some participants attempted to bypass the experiment for compensation. However, we applied data filtering techniques to remove unreliable responses and mitigate this issue.

Experiment Duration: The Enhanced Turing Test required extended engagement, which may have led to participant fatigue, affecting participant effort and accuracy.

Monetary Incentives: While financial compensation helped attract participants, it may have also encouraged strategic guessing rather than genuine effort in distinguishing AI from humans.

AI Model Selection: We tested the Llama 3.2 1B model, but results might vary with more advanced AI systems, limiting the generalizability of our findings.

Evaluation Scope: Our study focused solely on text-based interactions. Future research should explore multimodal Turing Tests incorporating voice, video, and real-time contextual engagement.

Addressing these limitations in future work will help refine AI evaluation methodologies and strengthen the reliability of Turing Test results.

# 9 Ethical Statement

This study was conducted following ethical research principles, ensuring participant privacy, informed consent, and data anonymity. All participants were recruited through Amazon Mechanical Turk and met predefined eligibility criteria. They were informed about the study's purpose, provided consent before participation, and were compensated fairly. No personally identifiable information was collected or stored.

Additionally, this research highlights the ethical implications of AI deception in human-AI interactions. The findings underscore the importance of designing robust evaluation methods to prevent misleading conclusions about AI capabilities. The authors advocate for responsible AI development, emphasizing transparency, fairness, and accuracy in AI assessments.

# References

- <span id="page-9-2"></span>Celeste Biever. 2023. Chatgpt broke the turing testthe race is on for new ways to assess ai. *Nature*, 619(7971):686–689.
- <span id="page-9-4"></span>Luka Bradeško and Dunja Mladenic. 2012. A survey of ´ chatbot systems through a loebner prize competition. In *Proceedings of Slovenian language technologies society eighth conference of language technologies*, volume 2, pages 34–37. sn.
- <span id="page-9-0"></span>Sébastien Bubeck, Varun Chadrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al. 2023. [Sparks of artificial general intelli](https://doi.org/10.48550/arXiv.2303.12712)[gence: Early experiments with gpt-4.](https://doi.org/10.48550/arXiv.2303.12712) *arXiv preprint arXiv:2303.12712*.
- <span id="page-9-12"></span>Hugging Face. 2024. sentence-transformers/allminilm-l6-v2. [https://huggingface.co/](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). Accessed: 2025-05-01.
- <span id="page-9-5"></span>Daniel Jannai, Amos Meron, Barak Lenz, Yoav Levine, and Yoav Shoham. 2023. [Human or not? a gam](https://doi.org/10.48550/arXiv.2305.20010)[ified approach to the turing test.](https://doi.org/10.48550/arXiv.2305.20010) *arXiv preprint arXiv:2305.20010*.
- <span id="page-9-6"></span>Cameron R. Jones and Benjamin K. Bergen. 2024. [Peo](https://doi.org/10.48550/arXiv.2405.08007)[ple cannot distinguish gpt-4 from a human in a turing](https://doi.org/10.48550/arXiv.2405.08007) [test.](https://doi.org/10.48550/arXiv.2405.08007) *arXiv preprint arXiv:2405.08007*.
- <span id="page-9-3"></span>Cameron R. Jones and Benjamin K. Bergen. 2025. [Large language models pass the turing test.](https://doi.org/10.48550/arXiv.2503.23674) *arXiv preprint arXiv:2503.23674*.
- <span id="page-9-8"></span>Arseny Moskvichev, Victor Vikram Odouard, and Melanie Mitchell. 2023. [The conceptarc benchmark:](https://doi.org/10.48550/arXiv.2305.07141) [Evaluating understanding and generalization in the](https://doi.org/10.48550/arXiv.2305.07141) [arc domain.](https://doi.org/10.48550/arXiv.2305.07141) *arXiv preprint arXiv:2305.07141*.
- <span id="page-9-10"></span>OpenRouter. 2024. Meta: Llama 3.2 1b instruct. [https://openrouter.ai/meta-llama/](https://openrouter.ai/meta-llama/llama-3.2-1b-instruct) [llama-3.2-1b-instruct](https://openrouter.ai/meta-llama/llama-3.2-1b-instruct).
- <span id="page-9-9"></span>Gabriele Paolacci, Jesse Chandler, and Panagiotis G. Ipeirotis. 2010. [Running experiments on amazon](https://doi.org/10.1017/S1930297500002205) [mechanical turk.](https://doi.org/10.1017/S1930297500002205) *Judgment and Decision Making*, 5(5):411–419.
- <span id="page-9-11"></span>Karl Pearson. 1900. [On the criterion that a given sys](https://doi.org/10.1080/14786440009463897)[tem of deviations from the probable...](https://doi.org/10.1080/14786440009463897) *Philosophical Magazine Series 5*, 50(302):157–175.
- <span id="page-9-7"></span>Ricardo Restrepo Echavarría. 2025. [Chatgpt-4 in the](https://doi.org/10.1007/s11023-025-09711-6) [turing test.](https://doi.org/10.1007/s11023-025-09711-6) *Minds and Machines*, 35(1):8.
- <span id="page-9-1"></span>Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R. Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-Alonso, et al. 2022. [Beyond the](https://doi.org/10.48550/arXiv.2206.04615)

[imitation game: Quantifying and extrapolating the](https://doi.org/10.48550/arXiv.2206.04615) [capabilities of language models.](https://doi.org/10.48550/arXiv.2206.04615) *arXiv preprint arXiv:2206.04615*.

- <span id="page-10-3"></span>Sharon Temtsin, Diane Proudfoot, David Kaber, and Christoph Bartneck. 2025. [The imitation game ac](https://doi.org/10.48550/arXiv.2501.17629)[cording to turing.](https://doi.org/10.48550/arXiv.2501.17629) *arXiv preprint arXiv:2501.17629*.
- <span id="page-10-4"></span>Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurélien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. 2023. Llama: Open and efficient foundation language models. [https:](https://arxiv.org/abs/2302.13971) [//arxiv.org/abs/2302.13971](https://arxiv.org/abs/2302.13971).
- <span id="page-10-0"></span>Alan M. Turing. 1950. [Computing machinery and intel](https://doi.org/10.1093/mind/LIX.236.433)[ligence.](https://doi.org/10.1093/mind/LIX.236.433) *Mind*, 59(236):433–460.
- <span id="page-10-2"></span>Kevin Warwick and Huma Shah. 2016. [Can machines](https://doi.org/10.1080/0952813X.2014.921734) [think? a report on turing test experiments at the](https://doi.org/10.1080/0952813X.2014.921734) [royal society.](https://doi.org/10.1080/0952813X.2014.921734) *Journal of Experimental & Theoretical Artificial Intelligence*, 28(6):989–1007.
- <span id="page-10-1"></span>Joseph Weizenbaum. 1966. [ELIZA—a computer pro](https://doi.org/10.1145/365153.365168)[gram for the study of natural language communica](https://doi.org/10.1145/365153.365168)[tion between man and machine.](https://doi.org/10.1145/365153.365168) *Communications of the ACM*, 9(1):36–45.