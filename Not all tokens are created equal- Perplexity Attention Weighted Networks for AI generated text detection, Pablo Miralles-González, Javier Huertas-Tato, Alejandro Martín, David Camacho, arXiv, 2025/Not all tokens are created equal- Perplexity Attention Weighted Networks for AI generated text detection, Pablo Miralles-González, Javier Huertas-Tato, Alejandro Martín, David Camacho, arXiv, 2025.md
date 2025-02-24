# Not All Tokens Are Created Equal: Perplexity Attention Weighted Networks For Ai Generated Text Detection

Pablo Miralles-González, Javier Huertas-Tato, Alejandro Martín, David Camacho Department of Computer Systems Technical University of Madrid Madrid
{pablo.miralles, javier.huertas.tato, alejandro.martin, david.camacho}@upm.es

## A**Bstract**

The rapid advancement in large language models (LLMs) has significantly enhanced their ability to generate coherent and contextually relevant text, raising concerns about the misuse of AI-generated content and making it critical to detect it. However, the task remains challenging, particularly in unseen domains or with unfamiliar LLMs. Leveraging LLM next-token distribution outputs offers a theoretically appealing approach for detection, as they encapsulate insights from the models' extensive pre-training on diverse corpora. Despite its promise, zero-shot methods that attempt to operationalize these outputs have met with limited success. We hypothesize that one of the problems is that they use the mean to aggregate next-token distribution metrics across tokens, when some tokens are naturally easier or harder to predict and should be weighted differently. Based on this idea, we propose the Perplexity Attention Weighted Network (PAWN), which uses the last hidden states of the LLM and positions to weight the sum of a series of features based on metrics from the next-token distribution across the sequence length. Although not zero-shot, our method allows us to cache the last hidden states and next-token distribution metrics on disk, greatly reducing the training resource requirements.

PAWN shows competitive and even better performance in-distribution than the strongest baselines
(fine-tuned LMs) with a fraction of their trainable parameters. Our model also generalizes better to unseen domains and source models, with smaller variability in the decision boundary across distribution shifts. It is also more robust to adversarial attacks, and if the backbone has multilingual capabilities, it presents decent generalization to languages not seen during supervised training, with LLaMA3-1B reaching a mean macro-averaged F1 score of 81.46% in cross-validation with nine languages.

K**eywords** AI Generated Text Detection · Perplexity-based methods

## 1 Introduction

The proliferation of large language models (LLMs) has ushered in a new era of text generation, where artificial intelligence can produce coherent, contextually relevant content with remarkable fluency. These advancements hold transformative potential across industries, yet they also raise serious concerns about the misuse of AI-generated text.

The ability to massively produce misinformation or automatically solve school assignments underscore the urgent need for effective detection mechanisms. However, identifying AI-generated text is far from straightforward, particularly in scenarios involving unseen domains or unfamiliar generative models, or mixed texts produced by human-machine collaboration. The diversity in writing styles, prompt configurations, and the opaque nature of AI systems contribute to the complexity of this task. Recent research has explored various strategies for detecting AI-generated text, with approaches based on next-token distribution output emerging as promising. These outputs, which represent likelihood estimates calculated by LLMs during text generation, encapsulate knowledge derived from extensive pre-training on diverse corpora. They offer a theoretically grounded foundation for detection, leveraging the statistical properties of language encoded in LLMs.

Despite their appeal, zero-shot methods that directly utilize these next-token distribution outputs have shown limited effectiveness and performance.

One of the limitations of current methods is their reliance on simple aggregation techniques, such as averaging nexttoken metrics across all tokens. This uniform treatment of tokens disregards the intrinsic differences in predictive complexity. For instance, predicting the completion of a word is often straightforward, while initiating a sentence, with its broader range of possible continuations, is inherently more challenging. The beginning of a text, unconditioned due to the unavailability of the generating prompt, is also naturally more random. Recognizing these nuances is critical to improving detection performance.

To address this gap, we propose the Perplexity Attention Weighted Network (PAWN), a novel approach that assigns dynamic weights to tokens based on their semantic, contextual and positional significance. PAWN leverages the semantic information encoded in the last hidden states of the LLM and positional indices to modulate the contribution of each token to a specific feature based on the next-token distribution metrics. Our method refines the aggregation process, resulting in more accurate and robust detection. Unlike zero-shot approaches, PAWN involves lightweight training, but it mitigates resource constraints by enabling the caching of hidden states and next-token distribution metrics on disk.

Empirical evaluations demonstrate that PAWN achieves competitive, and often superior, performance compared to fine-tuned LLM baselines. Notably, our model generalizes better to unseen domains and generative models, exhibiting consistent decision boundaries across distribution shifts and enhanced resilience to adversarial attacks. Furthermore, if the backbone LLM presents multilingual capabilities, PAWN showcases decent generalization to languages not seen during supervised training. These results highlight the potential of PAWN as a practical and resource-efficient solution for detecting AI-generated text.

The main contributions of this work are summarized as follows:
- We propose a novel detection framework, **Perplexity Attention Weighted Network (PAWN)**, which dynamically weights next-token distribution metrics based on semantic information from the LLM's hidden states and positional information. This model:
- Despite not being zero-shot and requiring supervised training, has a very small number of training parameters (in the order of one million). The backbone is thus frozen and run in inference mode, and it also allows us to cache the hidden states and metrics on disk, significantly reducing resource requirements compared to fine-tuning large models.

- Demonstrated *competitive or superior performance* to the strongest baseline, that is, fine-tuned language models, in in-distribution detection.

- Showcased better generalization capabilities in *unseen domains and with unfamiliar generative models*,
exhibiting more stable decision boundaries.

- Although still vulnerable to paraphrasing attacks, it achieved better overall robustness to adversarial attacks, mitigating vulnerabilities in AI-generated text detection.

- If the backbone model has multilingual capabilities, PAWN achieves decent performance in languages not observed during supervised training.

- By performing ablation studies with the different branches of the PAWN model, we study the effect of using semantic information from hidden states and next-token distribution metrics. As one might expect, we find that the former results in better performance in-distribution but worse generalization. By limiting the role of semantic information to weighting the metric-based features, PAWN achieves both great in-distribution performance and good generalization.

## 2 Related Work

This section reviews the state-of-the-art in the field of AI-generated text detection, highlighting key advances and challenges. We begin the discussion with the main challenges that researchers have found in this field. These challenges have shaped the most advanced datasets and benchmarks, recently developed, which we discuss next. We end the section with a classification of the main detection methods found in the literature.

## 2.1 Challenges

The detection of AI-generated text has been shown to face numerous challenges, preventing current detectors from being used reliably in real-world scenarios. Some of these challenges are as follows.

(i) **Generalization to unseen domains and models.** It has been shown now in several works [1, 2] that trained detectors often suffer when applied to a domain or source generative model that is not seen during training.

This makes it very difficult to reliably apply the detectors in real-world scenarios, as in most cases we do not know the domain or source model beforehand.

This is especially challenging in the current **continuously changing landscape of generative models**, where new and improved LLMs are being developed and made available to the public at an incredible rate.

(ii) **Multilingual detection.** The problem of generalizing to new domains is taken one step further in multilingual detection. This is especially true for low-resource languages, where supervised data is scarce, and so is pre-training data for many of the backbone LMs used in detectors. These LMs also suffer from tokenization problems, as many tokens are required to encode texts of rare languages, especially in other alphabets.

These problems were illustrated in [2], where Wang et al. found a great degradation in performance in languages where the model was not fine-tuned, even with a multilingual backbone model such as XLM-RoBERTa [3].

(iii) **Adversarial attacks.** Users of generative models are constantly devising strategies to avoid detection. One common strategy is the use of paraphrasing attacks [4, 5, 6], where the generated text is automatically processed by the same model or another to paraphrase sentences in the text. Although simple, these attacks have been shown to greatly degrade performance [1]. Other very simple attacks are available [7], such as the insertion of invisible characters, of whitespace, the use of intentional misspelling, of homoglyphs, etc.

(iv) **Intercalated human and machine-generated text.** Many times, the texts are a product of human and machine collaboration. The users might create an initial template to work with, and then rewrite some part according to their need. This opens the way to a different and related problem: detecting AI-generated spans within a text [8]. We do not treat this problem in this work.

## 2.2 Datasets And Benchmarks

The foundation for effective AI-generated text detection lies in robust datasets and evaluation benchmarks. Although there is a wealth of work in this research line, it was not until very recent work that evaluation sets started to address the challenges detectors faced when applied in real-world scenarios. For example, the data from the Voight-Kampff Generative AI Authorship Verification Task at PAN and ELOQUENT 2024 [9] and the TuringBench benchmark [10]
does not include information on the domain. The Ghostbuster dataset [11], HC3 [12] and the GPT2 output dataset [13] only include texts from a single source model. In this work, we focus on three modern datasets that address generalization to both new domains and new source models, and that contain a large number of examples.

MAGE [1] contains almost half a million examples, with a focus on quality and diversity. At the time of writing, MAGE contains the most diverse set of domains and source generative models. In addition, they standardize a set of eight testbeds to evaluate the detectors in different settings and run several existing baselines on them. They even include on testbed with samples attacked with paraphrasing.

M4 [2, 8] is a slightly less diverse and smaller dataset of 122K examples. It also presents a decent range of domains and source generative models, but the best feature is the diversity of languages. M4 provides a multilingual set with examples from nine different languages.

RAID [7] is a massive dataset of 6 million examples from a wide range of domains and source generative models, although less varied than that of MAGE. Particularly interesting is their inclusion of multiple decoding strategies, as well as samples with and without repetition penalty. They also present examples with a large set of eleven adversarial attacks to evaluate the robustness of detectors.

## 2.3 Detection Methods

There is a large and growing body of work focused on detection methods for AI-generated text. We review some of the main methods that appear in the literature, breaking them into four main categories. Watermarking methods add hidden patterns to AI-generated text to make it identifiable. Zero-shot detectors rely on large language models (LLMs) pre-trained for next-token prediction to identify AI-generated content without additional training, using the next-token distributions of the text. Other approaches fine-tune language models, training them specifically for the task of detection. Finally, LLMs have also been prompted to detect whether a text is AI-generated, making it complete the given prompt with the answer.

## 2.3.1 Watermarking Technology

Watermarking technologies offer a proactive approach to text detection by embedding identifiable markers in AIgenerated outputs. These methods are not strictly comparable to other types of detector, as they require the cooperation of the LLM provider.

An example of these methods is given by Kirchenbauer et al. [4]. They proposed an algorithm that uses the hash of the last token and a random number generator to produce a list of red tokens that are banned or made unlikely to be selected.

Thus, a text that has been generated with this algorithm can be detected because most of the tokens will be in the green list, that is, not in the red list. However, human text is expected to result in half of the tokens in each list. To avoid reducing the quality of the generated text, they applied a positive bias to the logits of tokens in the green list. In this way, sampling from very sharp distributions with low entropy is not greatly altered, and only high-entropy distributions with many available options as the next token are substantially modified.

The authors found that this method can be effectively attacked by using another LLM to paraphrase spans of the text.

In fact, the robustness of the method to such attacks was studied by Kirchenbauer et al. in [14]. Other attacks have been pointed out in the literature. A simple example is to ask the LLM to produce an emoji after each generated token, removing them from the sequence afterwards. This effectively randomizes the red list on each token [6].

## 2.3.2 Fine-Tuned Lms

As in any other text classification problems, fine-tuning pre-trained language models (LMs) has emerged as a powerful alternative. Encoder-only pre-trained models such as BERT [15], RoBERTa [16] or XLM-RoBERTa [3] appear in a large body of work [17, 18, 19, 1, 8], with OpenAI [20] even releasing their own RoBERTa large fine-tuned detector.

Although simple, these methods very often provide the strongest detection baselines [1, 8]. Unfortunately, they also tend to suffer greatly in out-of-distribution domains and generative models [1, 8].

## 2.3.3 Zero-Shot Detectors

Many zero-shot detection methods have been proposed in prior work. These methods are attractive because they do not require fine-tuning of large language models, but only selecting a boundary between machine-generated and human-generated texts for some score or metric they produce. We review some of the main methods in this category, all of them employing the next-token distribution of some frozen LLM to calculate some metric for the text. Gehrmann, Strobelt, and Rush [21] proposed GLTR. They used the probability of the token that occurred next, the rank of that token, and the entropy of the next-token distribution to create a visualization tool for human detectors, showing different colors for each token depending on these metrics.

Mitchell et al. [22] proposed DetectGPT. They applied local perturbations to the text using a different model such as T5 [23]. They mask some of the tokens and apply the mask-filling model to create perturbed versions of the text. Then, they use the average log-probability of both the original text and the sampled perturbed versions, subtracting the former with the mean of the latter.

DetectGPT is very computationally expensive as it runs the paraphrasing model and detection LLM once per perturbed sample. To solve this, Bao et al. [24] presented FastDetectGPT. Their approach re-samples tokens independently of each other, using the same LLM as the one used for detection. In other words, after resampling one token, they do not regenerate the text that follows but keep all the following next-token distributions the same for sampling. This allows them to avoid multiple runs through the model. Despite the increased efficiency, they also seemed to increase the detection performance of the model.

Su et al. [25] proposed two methods, called DetectLLM-LRR and DetectLLM-NPR. The former leverages the ratio between the next-token log-probability and log-rank. The latter compares the average log-rank information with the mean across a range of perturbations of the text.

Hans et al. [26] proposed Binoculars. In their method, they use two very similar models (they must at least share the same tokenizer) called the observer and the performer, often the foundation and instruction-tuned versions of the same model. First, they used the observer model to calculate the average log-probability of the text. Next, they compute the average cross-entropy between the next-token distributions of the observer and performer models, which measures how surprising the output of one model is to the other. The final score is the ratio of these two metrics. This normalization is motivated by what they call the "capybara problem". Without the prompt available to condition the text, the models will naturally assign higher perplexities depending on factors such as topic or style.

Despite being very interesting ideas and not requiring supervised training, these detectors are often not the best performing ones (see e.g. [1, 8] or appendix A), falling behind fine-tuned LMs.

## 2.3.4 Llms As Detectors

Large Language Models (LLMs) themselves can serve as detectors for AI-generated text, using their advanced understanding of linguistic patterns. In particular, we refer to methods that include the text in the prompt and ask the LLM whether it is machine-generated or human-generated. For example, Bhattacharjee and Liu [27] used ChatGPT as detector, although it did not prove to be a reliable detector. Koike, Kaneko, and Okazaki [28] further extend on this idea by using in-context learning (ICL), providing semantically similar labeled examples in the prompt. This methodology, together with their framework to produce adversarial examples, seems to improve the performance of the methods.

## 3 Methodology 3.1 Perplexity Attention Weighted Network (Pawn)

Like the zero-shot methods we reviewed in section 2.3.3, we use pretrained LLMs to obtain the next-token distributions from the given text. From these distributions, we generate five different metrics, measuring the likelihood of the next token and the randomness of the distribution.

However, zero-shot methods often use a simple mean to aggregate different metrics. Our main addition is the use of semantic and positional information to weigh the relevance of each token. The reason for this is that some of the tokens are naturally easier or harder to predict. Consider two examples. First, completions of words are expected to be very easy for the LLM, as the possibilities are very reduced, and patterns are not too difficult. Second, the beginning of a text is always very unconditioned, making the first few tokens naturally very random. Thus, applying a simple aggregation where every token is equally weighted will add a lot of unnecessary noise. To address this, we used both semantic information from the last hidden states of the LLM and positional information to perform some filtering.

Figure 1 shows the full diagram of our model. We explain it in four steps, both the computations and the rationale behind each design decision.

LLM run. The texts initially go through a selected decoder-only LLM pre-trained for next-token prediction. This returns both the last hidden states and the logits of the next-token distribution.

In this work, we use openai−community/gpt2 [29] and meta−llama/Llama−3.2−1B−Instruct [30], covering small and medium model sizes.

Computing metric features. From the output logits we generate five different metrics that measure some aspect of the distribution, instead of using only the probability or log-probability of the next token. All of these extra metrics serve one of two purposes. The first is to get a metric that is closer to the Top-P or Top-K decoding algorithms. The second is measuring the randomness of the distribution. This helps in contextualizing the log-probability of the token, as it is not the same to have a low probability in a very random distribution where the probability mass is very distributed, than in a very sharp distribution with a single very likely token. But it is also useful as a metric itself: we expect human text to take the LLM to uncharted territory more often. The five metrics are listed below. They are also mathematically formulated for a sequence of tokens t1*, . . . , t*N of length N, and an LLM next-token distribution probability matrix P ∈ MN×V, with V being the size of the vocabulary.

(i) **Log-probability of the token that occurred next in the sequence.** This metric is formulated as M
log-prob i = log Pi,ti+1 .

(ii) **Entropy of the distribution.** This metric measures the randomness in the distribution, that is, how spread the probability mass is across many tokens. In mathematical terms it is expressed as

$$M_{i}^{\mathrm{entropy}}=\sum_{j=1}^{V}P_{i,j}\log P_{i,j}.$$

(iii) **Maximum log-probability.** Another measure of randomness, useful to compare with the log-probability of the token that occurred. If they are close, then the token was one of the most probable ones. This can be interesting in distributions where the mass is spread across a few tokens. For example, in the phrase
"My favorite color is" the probability is distributed among the different colors. Mathematically:

$$\mathbb{M}$$
max-log-prob
i = max
$$=\operatorname*{max}_{j=1,\ldots,V}\log P_{i,j}.$$

(iv) **Rank of the token that occurred next in the sequence.** The quantile that the token that occurred next represented in the next-token distribution,. In other words, the minimum K parameter in Top-K decoding where the token could have been selected, divided by the size of the vocabulary. It can be expressed mathematically as Mrank i = rank (log Pi,:, ti+1) /V.

(v) **Sum of probabilities of tokens with higher or equal probability than the token that occurred**. In other words, the minimum P parameter in Top-P decoding where the actual token is covered with its full probability. It is formulated as follows:

$$M_{i}^{\mathrm{top-p}}=$$
i =X
$$P_{i,j}$$
$$\sum_{j=1,...,V;P_{i,j}\geq P_{i,t_{i}+1}}$$

These metrics are processed by an MLP network to generate F different *metric features*.

Computing weights. Next, the hidden states of the LLM and positional information are used to filter out and prioritize the different tokens. Instead of just using the corresponding hidden state, we also concatenate the hidden state of the next token. Both of these tokens are relevant when deciding which metrics to take into account and which to discard, and we found a slightly higher performance empirically. As positional information, we plug in the index of each token, divided by a fixed maximum length to avoid very large numbers. Again, the rationale behind it is that the first tokens of the sequence are very unconditioned and will likely have a low log-probability, so we want the model to be able to take this into account, even if no hidden state feature accounts for it.

All of these features are processed by an MLP network, generating G *feature logits*, where G divides F. These new *feature logits* are converted to *feature weights* by applying a softmax operation across the length of the sequence.

Aggregating metrics. The G *feature weights* are broadcasted up to the dimension F. They are then used to compute a weighted sum of the *metric features* across the length of the sequence, summarizing the full text into a single feature vector.

By using the softmax function, we restrict the role of the hidden states to weighting, and prevent hidden state and positional information from appearing in the summary vector, at least directly. This is because any component of the *metric features* that is independent of the metrics, such as bias parameters, will be summed up to itself after being aggregated with weights summing up to one.

Processing summary vector. The final summary vector goes through a final MLP network to produce the logit or probability of the text being generated by AI.

## 3.2 Data

As discussed in section 2, our choice of datasets was mainly motivated by whether they addressed the challenges that detectors face when applied in the real world. Thus, our choices include texts from a variety of domains and source generative models. In some of them we also find different languages, decoding hyperparameters and adversarial attacks. In this section, we describe the three datasets we use in more detail, elaborating on their selection of models, domains and other features.

## 3.2.1 Mage

The MAGE [1] dataset is a large (half a million samples), comprehensive, and diverse dataset and benchmark. This is our main choice for testing and performing ablation studies, given the large number of domains and models covered, the openness of their data splits, the pre-selection of a number of testbeds to compare different models and the number of baselines they provide.

Domain selection. A **main corpus** of data is provided, where human- and machine-generated texts are sourced from ten different domains: (i) opinion statements from the /r/ChangeMyView (CMV) Reddit subcommunity [31] (ii) and the Yelp dataset [32]; (iii) news articles from XSum [33] (iv) and TLDR_news (TLDR) [34]; (v) question answers from the ELI5 dataset [35]; (vi) stories from the Reddit WritingPrompts (WP) dataset [36] (vii) and the ROCStories Corpora
(ROC) [37]; (viii) common sense reasoning from the HellaSwag dataset [38]; (ix) question answering from the SQuAD
dataset [39]; (x) and scientific abstracts from SciXGen [40]. A **separate corpus** is also provided, containing samples from a complementary set of four domains: news CNN/DailyMail [41], dialogues from DialogSum [42], scientific answers from PubMedQA [43] and reviews from IMDb [44].

![6_image_0.png](6_image_0.png)

Figure 1: Diagram of the Perplexity Attention Weighted Network.
Model selection. The **main corpus** sources machine-generated texts from 27 generative models, grouped into seven families: (i) LLaMA [45]; (ii) OpenAI GPT [46] (up to *gpt-turbo-3.5*); (iii) FLAN-T5 [47]; (iv) BigScience [48];
(v) EleutherAI [49, 50]; (vi) OPT [51]; (vii) and GLM-130B [52]. The **separate corpus** contains texts generated by GPT-4 [53], a model that is not included in the main corpus.

Adversarial attacks. The authors also include a set with adversarially attacked texts by applying a paraphrasing model sentence-by-sentence.

## 3.2.2 M4/M4Gt-Bench

The next choice is M4 [2, 8], another modern dataset that covers several domains and models. They provide two separate sets, one with English texts only and one with texts from multiple languages. Although M4 is less varied in the English language and has fewer examples than MAGE (122K), we will be able to use it to test the ability to generalize to different datasets and languages.

Domain and language selection. We find six different English domains, a smaller set than that of MAGE:
(i) Wikipedia; (ii) Reddit ELI5 [35]; (iii) WikiHow [54]; (iv) PeerRead [55]; (v) arXiv abstract; (vi) and OUTFOX [28].

However, they include more domains from eight extra languages: (i) Arabic (Wikipedia and news); (ii) Bulgarian
(True & Fake News); (iii) Chinese (Baike/Web); (iv) Indonesian (id_newspapers_2018); (v) Russian (RuATD [56]);
(vi) German (Wikipedia and news); (vii) Italian (CHANTE-it news); (viii) and Urdu (Urdu-news [57]).

Model selection. The number of models included is also much smaller than in MAGE, with the monolingual set containing samples from (i) Davinci003; (ii) ChatGPT [58]; (iii) GPT4 [53]; (iv) Cohere [59]; (v) Dolly-v2 [60];
(vi) and BLOOMz [61]. The multilingual set includes samples from LLaMA-2 [62] and Jais [63] in Italian and Arabic, respectively.

## 3.2.3 Raid

Our last choice is RAID [7], another set with a variety of domains and source models. It contains a total of six million examples, being the largest of the sets we used, although the number of source texts to sample from is still limited
(13371). RAID is particularly interesting for their use of different decoding strategies and the inclusion of samples generated with repetition penalty. They also have a large selection of adversarial attacks. Unfortunately, the authors do not include results from baselines trained in the RAID training split. Instead, their baselines were trained on a different dataset each. The authors did not provide a testbed selection either. Model selection. The variety of selected models is somewhere between M4 and MAGE, as they include (i) Cohere [59]
(Foundation and Chat); (ii) MPT-30B [64] (Foundation and Chat); (iii) Mistral-7B [62] (Foundation and Chat);
(iv) ChatGPT [58]; (v) GPT-2 XL [29]; (vi) GPT-3 [65]; (vii) GPT-4 [53]; (viii) LLaMA 2 70B Chat [62]. The novelty of RAID is that they also use two different decoding strategies, greedy and sampling, as well as repetition penalty.

These features are included in the dataset, and we use them to test the generalization of our model in new decoding settings.

Domain selection. As for domains, they include factual knowledge from platforms like News [66] and Wikipedia [67],
generalization and reasoning seen in Abstracts [68] and Recipes [69], creative and conversational abilities found in Reddit [70] and Poetry [71], and familiarity with specific media such as Books [72] and Reviews [44].

Adversarial attacks. Finally, the authors provide examples attacked with a variety of adversarial strategies:
1. **Synonym**: Replace tokens with highly similar alternatives using BERT [15].

2. **Article Deletion**: Remove articles such as 'the', 'a', 'an'.

3. **Alternative Spelling**: Apply British spelling conventions.

4. **Add Paragraph**: Insert \n\n between individual sentences to separate them.

5. **Upper-Lower Case Swap**: Reverse the case of words (upper to lower and vice versa).

6. **Homoglyph**: Replace characters with visually similar alternatives (e.g., replace "e" with similar character U+0435).

7. **Number**: The digits are randomly shuffled in numbers. 8. **Paraphrase**: Rephrase using a fine-tuned T5-11B model [5]. 9. **Misspelling**: Introduce common misspellings of words.

10. **Whitespace**: Add extra spaces between characters.

11. **Zero-Width Space**: Insert the zero-width space character (U+200B) between every other character.

## 3.3 Experiments 3.3.1 In-Distribution Performance And Generalization To Unseen Domains And Models On Mage

Our main experiments are performed on the MAGE dataset [1]. The authors provide a fixed set of settings to evaluate detectors. They generate six different testbeds from the **main corpus**. In the first four, detectors are tested in-distribution, that is, on the same domains and source models they were trained on:
TB1: **One domain & one source model.** Training and testing are restricted to a single source model and domain.

This is done for each of the ten domains, and the results are averaged. This testbed will not be used because of its ease.

TB2: **One source model & all domains.** Training and testing are restricted to a single source model, but all domains are included. The results are obtained for each source model and averaged.

TB3: **All source model & one domain.** Training and testing are restricted to a single domain, but all source models are included. The results are obtained for each domain and averaged.

TB4: **All source model & all domains.** Training and testing are performed in all domains and source models.

Next, we find two testbeds that evaluate the detectors out-of-distribution, that is, on unseen domains or source models.

To do this, they proposed leave-one-out experiments across domains and source models.

TB5: **Unseen source model.** The samples are divided by model family, creating a split of seven sets in total. For each set, a model is trained on the samples that do not belong and tested on the samples that do. The results are averaged across families.

TB6: **Unseen domain.** Similarly, they divide the samples by domain and create a split of ten sets. The final results are the average of the results of all ten leave-one-out experiments.

Finally, the authors of MAGE generate two additional testbeds from the **separate corpus**. These testbeds go one step further in evaluating the detector's ability to generalize out-of-distribution.

TB7: **Unseen domain & source model.** Models trained on the main corpus are then evaluated on the separate one, which contains texts from unseen domains and an unseen generative model.

TB8: **Paraphrasing attacks.** To test the detector's robustness to paraphrasing attacks, which have been shown to be effective at avoiding detection, the separate corpus is transformed by paraphrasing the texts sentence by sentence. Both human and machine texts that are transformed get labeled as machine-generated.

We train PAWN with a openai−community/gpt2 [29] and meta−llama/Llama−3.2−1B−Instruct [30] backbone, and compare it with the rest of the baselines on each of the testbeds selected by the authors. These baselines include FastText [73], GLTR [21], DetectGPT [22] and a fine-tuned LM for classification with a Longformer [74] backbone. Li et al. report having tested RoBERTa-{base,large} [16], BERT-{base,large} [15] and GPT2-{small,medium,large} [29], but finding Longformer to be the best performing one.

We adopted their evaluation metrics to be able to compare PAWN with their baselines. As the set is imbalanced, the macro-averaged recall is used. The AUROC is also reported, as sometimes the detectors are able to distinguish between machine and human text, but the exact threshold has a lot of variability depending on the underlying text distribution.

All baselines in [1] are trained for five full epochs and we maintain their setting for a fair comparison.

## 3.3.2 Ablations

To study the importance of each element in the Perplexity Attention Weighted Network, we run the MAGE experiments with each of the branches of our networks in isolation. We consider the following two variations.

(i) **Hidden state branch.** We concatenate the consecutive hidden states and positional information, apply a single MLP element-wise, and average across tokens to produce the final prediction. We keep the number of hidden features in the MLPs and duplicate the depth of the network to match the maximum depth of computation.

(ii) **Metrics branch.** We remove the filtering based on hidden states and aggregate the metrics using a simple mean.

For these ablations, we restrict ourselves to MAGE's testbeds 4-8, as they include the most difficult in-distribution setting and all out-of-distribution ones.

## 3.3.3 Evaluating Ensembles As A Way To Improve Generalization

One simple idea to improve the generalization in out-of-distribution settings is to ensemble different models. This is particularly fitting in PAWN, where we may train with a set of different backbones, each giving a different perspective from their unique tokenization and fine-tuning process. To evaluate this idea, we tested several simple ensembles, averaging the final logits, on MAGE's testbeds 4, 7 and 8.

## 3.3.4 Generalization And Multilingualism On M4

Next, we test the generalization and multilingual capabilities of PAWN on M4. We study two separate settings.

Generalization to a new dataset. We evaluated the ability to adapt from one dataset to another, again testing the generalization capabilities of the detectors. We compare models trained on the main corpus of MAGE, using the Longformer model provided in [1] and our own RoBERTa [16] base fine-tuned model as baselines. We also test the adaptability of the detectors by fine-tuning them for one epoch, first on English domains and then on all domains. All of these experiments are performed on the multilingual set.

We note that there are intersections between the source domains in MAGE and M4. Most evidently, Reddit ELI5 is present in both datasets, but there might be other less obvious intersections. However, all models are evaluated under the same conditions, new domains in novel languages are added, and the distribution of generative models differs as well. Thus, we believe these experiments will provide useful comparisons.

M4GT-Bench. Next, we evaluate the PAWN model in M4GT-Bench [8] settings, and compare with their XLMRoBERTa and RoBERTa baselines. These settings include leave-one-out experiments to test out-of-distribution performance, similar to the fifth and sixth testbeds in MAGE [1]. In particular, they divide the data by domain, generative model, or language, and evaluate detectors through cross-validation, as in MAGE's testbeds. We remark that their experiments across domains are performed as a multiclass problem, where the detector not only predicts whether the text is AI-generated, but also the source model. We maintain the binary classification setting and train our own RoBERTa [16] base model as baseline.

We adopted their 10-epoch training limit, using only five epochs ourselves. We adapt to their metrics choice of accuracy, F1-score of the machine-generated class, and macro-averaged F1-score, depending on the case. Note that the accuracy metric is acceptable because the datasets are decently balanced.

## 3.3.5 Generalization To New Decoding Strategies And Robustness To Attacks On Raid

Finally, we conduct another set of experiments on RAID [7]. First, we evaluate the ability of PAWN to generalize to a new domain and model selection, new decoding strategies, and the addition of repetition penalty. We do this by testing the PAWN models, the Longformer model from [1] and a RoBERTa [16] base model pre-trained on the main corpus of MAGE. We also included baselines provided in RAID [7], but we note that each baseline is trained on a different dataset, and only zero-shot methods can be directly compared. These baselines include RoBERTa base and large models trained on the GPT2 output dataset [13], another RoBERTa base model trained on the HC3 dataset [12], RADAR [75], GLTR [21], FastDetectGPT [24], Binoculars [76], and LLMDet [77]. They also included the closed-source commercial detectors GPTZero, Winston, Originality and ZeroGPT.

Second, we evaluate the model's ability to adapt to these new decoding settings and domain and model selection by fine-tuning it for one epoch on RAID's training set. Again, our main baselines are the Longformer and RoBERTa base models pre-trained on MAGE. In this setting, no other baselines are provided in [7]. Finally, we evaluate the performance drop when different adversarial attacks are applied. This is tested on models that were fine-tuned on RAID's training set, excluding attacked data.

For uniformity with other baselines, we adopt the same metric that they used, that is, the recall at 5% FPR. Like them, we also select a different classification threshold per domain. It must also be noted that we do not use their test set, which is hidden, but our own split of their data, which can be easily replicated from our code. We make sure to group texts that are generated from the same source title in the same sets of the split, avoiding any leakages.

## 3.4 Technical Details 3.4.1 Hyperparameters

In table 1 we show the hyperparameters we used for the PAWN model with both backbone models openai−community/gpt2 [29] and meta−llama/Llama−3.2−1B−Instruct [30]. The MLP hyperparameters are common to all MLP networks in PAWN, that is, the networks are similar except for the input and output dimensions. We note that we drop out 15% of tokens during training by setting their *gate logits* to −∞ as a form of regularization.

## 3.4.2 Parameter Counts

One question that arises is the fairness of the comparisons with fine-tuned LM baselines given the size of the backbone model. Table 2 shows the parameter count of the main LM baselines and of the PAWN models we used, separating the backbone and head counts. We find that the PAWN model with a openai−community/gpt2 backbone has the second fewest total parameters, and the number of trainable parameters is two orders of magnitude below that of the fine-tuned LMs. However, the meta−llama/Llama−3.2−1B−Instruct backbone greatly increases the number of total parameters, and this should be taken into account when comparing the results.

## 3.4.3 Caching

Even though our model requires supervised training, our backbone LLMs are frozen, greatly reducing training compute requirements. Further, we cache the last hidden states and metrics for each of the data samples in MAGE, reducing training time by a factor between 7 and 10 with our hardware and model selection. This is an important feature of our model, as it only needs one iteration of the LLM in inference mode over the dataset for training, massively reducing training resource requirements.

Table 1: Hyperparameters used to train the Perplexity Attention Weighted Network (PAWN). MLP hyperparameters are common to all three MLP networks in PAWN. Dropout tokens is the ratio of tokens that are masked during training by setting their *gate logit* to −∞. The weight for positive samples is only used to train on MAGE. The first value is used in all testbeds except for TB2, where the second one is applied. Models in M4 are fine-tuned for one epoch and fully trained for five epochs.

| LLM hyperparameters                  |               |       |       |
|--------------------------------------|---------------|-------|-------|
| Max Length                           | 512           |       |       |
| PAWN hyperparameters                 |               |       |       |
| Positional encoding                  | Indices       |       |       |
| Number of gates G                    | 256           |       |       |
| Number of features F                 | 256           |       |       |
| Dropout tokens                       | 0.15          |       |       |
| MLP hyperparameters                  |               |       |       |
| Num hidden layers                    | 3             |       |       |
| Num hidden features                  | 256           |       |       |
| Normalization                        | Layer         |       |       |
| Activation                           | GELU          |       |       |
| Optimization hyperparameters MAGE M4 | RAID          |       |       |
| Optimizer                            | AdamW         | AdamW | AdamW |
| Learning rate                        | 0.001         | 0.001 | 0.001 |
| Weight decay                         | 0.01          | 0.01  | 0.01  |
| Batch size                           | 128           | 32    | 128   |
| Gradient clip value                  | 1             | 1     | 1     |
| Positive samples weight              | 0.413 | 2.891 | 1     | 1     |
| Label Smoothing                      | 0.2           | 0.2   | 0.2   |
| Epochs                               | 5             | 1 | 5 | 1     |

| Module                           | Number of parameters   |
|----------------------------------|------------------------|
| FacebookAI/roberta-base          | 125M                   |
| FacebookAI/roberta-large         | 355M                   |
| FacebookAI/xlm-roberta-base      | 279M                   |
| Longformer                       | 149M                   |
| openai-community/gpt2            | 137M                   |
| meta-llama/Llama-3.2-1B-Instruct | 1.24B                  |
| PAWN-GPT2 head                   | 989K                   |
| PAWN-LLaMA head                  | 1.6M                   |

Table 2: Parameter counts of the LM baselines and backbones used in this work, together with the PAWN networks with backbones *openai-community/gpt2 meta-llama/Llama-3.2-1B-Instruct*.

## 3.4.4 Setup

All experiments were run on a single NVIDIA GeForce RTX 3090 GPU with 24GB of memory. For reference, caching metrics and hidden states on disk, training PAWN for a single epoch on the full training set of MAGE takes 5min 40sec with the GPT2 backbone and 11min with the LLaMA3-1b backbone. The source code is available at https:
//github.com/pablomiralles22/ai-gen-detection, together with the Conda environment file containing the library versions we use.

## 4 Results 4.1 In-Distribution Performance And Generalization To Unseen Domains And Models On Mage

Table 3 shows the results of our model on MAGE's testbeds, as well as those reported in [1]. We remind the reader that Longformer is the only fine-tuned LM shown in this table, as it is the best performing backbone found by the authors.

We now restrict our attention to the *Longformer* baseline, since it is the only competitive one.

In the in-distribution settings of testbeds two and three, our model appears to perform on par, but slightly worse than Longformer. This is more pronounced when restricted to one domain than when restricted to one model. Thus, in the rare setting where we know the source model or the domain, we might get better performance with a fine-tuned LM.

However, in the fourth test, without restrictions, both of our models outperform the baseline *Longformer* in terms of recall, by a good margin. The AUROC is slightly below for PAWN-GPT2, although the magnitude of the difference is hidden by the rounding. In any case, PAWN models find a boundary that generalizes better in test data. In out-of-distribution testbeds five and six, showing the ability to generalize to unseen domains and models, we find that both of our models outperform the baselines in the two metrics. Although the AUROC is again very close, there is a big gap in average recall, especially in unseen domains. This again suggests that there is less variability in the decision boundary across distribution changes for PAWN models.

PAWN models also outperform in test seven for both metrics, with a good margin in the case of PAWN-LLaMA.

Furthermore, the macro-averaged recall of Longformer with the naive threshold is much weaker, and Li et al. had to use a special procedure to select a better one. Finally, the results in the eighth test suggest that our models are also not robust to paraphrasing attacks. The performance of PAWN is greatly diminished and cannot be used reliably in this setting.

We see a general trend across the results. In more specific in-distribution settings, our model performs slightly worse, but as we get to more open settings and even out-of-distribution, PAWN performs better, with the gap growing bigger.

This is especially the case in terms of recall, which is dependent on the selected threshold, unlike AUROC. It appears that the PAWN detectors result in a more uniform decision boundary across domains and source models.

## 4.2 Ablations

Next, we evaluate the relevance of our addition by comparing the performance of PAWN with that of the hidden state branch (HSFF) and the metrics branch (MPN). Table 4 shows these results. With both backbones, the PAWN model outperforms the alternatives in all settings with two exceptions. First, in the presence of paraphrasing attacks, where all models suffer greatly. Second, MPN has a slightly higher recall with the GPT2 backbone, but a smaller AUROC.

An interesting pattern emerges in the performance of the models in different settings. We observe that the hidden state branch is clearly the better alternative in the in-distribution fourth test. In unseen models, they perform relatively on-par, with HSFF still slightly ahead in terms of recall. However, in unseen domains (tests six and seven), HSFF falls far behind MPN.

This phenomenon is more apparent in the last two columns of table 4, where we show the variation in performance between each out-of-distribution testbed and the fourth testbed. MPN is the model that suffers the least, showing great generalization in terms of both AUROC and recall. HSFF is the one that suffers the most out-of-distribution on average. PAWN also suffers a bit more than MPN in new domains, with recall taking a larger hit, suggesting greater threshold variance across domains.

We theorize that using the next-token distribution of LLMs generalizes greatly, as the backbones are pre-trained in a massive dataset and not overfitted to specific domains. Using semantic information as in HSFF seems to overfit the training distribution and generalize worse, as we might expect given that they fit semantic information. PAWN is somewhere in the middle, since semantic information is only used to aggregate across tokens. This provides a greater ability to fit the model to in-distribution data while maintaining good generalization.

| and averaging the best boundaries. All results except PAWN's are taken from [1]. Setting Method HumanRec MachineRec   | AvgRec      | AUROC   |        |        |      |
|-----------------------------------------------------------------------------------------------------------------------|-------------|---------|--------|--------|------|
| Testbed 2,3,4: In-distribution Detection                                                                              |             |         |        |        |      |
| One source model & all domains                                                                                        | FastText    | 88.96%  | 77.08% | 83.02% | 0.89 |
| GLTR                                                                                                                  | 75.61%      | 79.56%  | 77.58% | 0.84   |      |
| Longformer                                                                                                            | 95.25%      | 96.94%  | 96.10% | 0.99   |      |
| DetectGPT*                                                                                                            | 48.67%      | 75.95%  | 62.31% | 0.60   |      |
| PAWN (GPT2)                                                                                                           | 95.03%      | 95.07%  | 95.05% | 0.99   |      |
| PAWN (Llama3-1b)                                                                                                      | 95.54%      | 96.10%  | 95.82% | 0.99   |      |
| All source models & one domain                                                                                        | FastText    | 89.43%  | 73.91% | 81.67% | 0.89 |
| GLTR                                                                                                                  | 37.25%      | 88.90%  | 63.08% | 0.80   |      |
| Longformer                                                                                                            | 89.78%      | 97.24%  | 93.51% | 0.99   |      |
| DetectGPT*                                                                                                            | 86.92%      | 34.05%  | 60.48% | 0.57   |      |
| PAWN (GPT2)                                                                                                           | 92.76%      | 90.72%  | 91.74% | 0.98   |      |
| PAWN (Llama3-1b)                                                                                                      | 93.44%      | 90.90%  | 92.17% | 0.98   |      |
| All source models & all domains                                                                                       | FastText    | 86.34%  | 71.26% | 78.80% | 0.83 |
| GLTR                                                                                                                  | 12.42%      | 98.42%  | 55.42% | 0.74   |      |
| Longformer                                                                                                            | 82.80%      | 98.27%  | 90.53% | 0.99   |      |
| DetectGPT*                                                                                                            | 86.92%      | 34.05%  | 60.48% | 0.57   |      |
| PAWN (GPT2)                                                                                                           | 93.75%      | 91.97%  | 92.86% | 0.98   |      |
| PAWN (Llama3-1b)                                                                                                      | 90.68%      | 95.84%  | 93.26% | 0.99   |      |
| Testbed 5,6: Out-of-distribution Detection                                                                            |             |         |        |        |      |
| Unseen source model                                                                                                   | FastText    | 83.12%  | 54.09% | 68.61% | 0.74 |
| GLTR                                                                                                                  | 25.77%      | 89.21%  | 57.49% | 0.65   |      |
| Longformer                                                                                                            | 83.31%      | 89.90%  | 86.61% | 0.95   |      |
| DetectGPT*                                                                                                            | 48.67%      | 75.95%  | 62.31% | 0.60   |      |
| PAWN (GPT2)                                                                                                           | 93.97%      | 81.43%  | 87.70% | 0.96   |      |
| PAWN (Llama3-1b)                                                                                                      | 95.17%      | 85.68%  | 90.42% | 0.97   |      |
| Unseen domain                                                                                                         | FastText    | 54.29%  | 72.79% | 63.54% | 0.72 |
| GLTR                                                                                                                  | 15.84%      | 97.12%  | 56.48% | 0.72   |      |
| Longformer                                                                                                            | 38.05%      | 98.75%  | 68.40% | 0.93   |      |
| DetectGPT*                                                                                                            | 86.92%      | 34.05%  | 60.48% | 0.57   |      |
| PAWN (GPT2)                                                                                                           | 65.17%      | 95.45%  | 80.31% | 0.94   |      |
| PAWN (Llama3-1b)                                                                                                      | 67.24%      | 95.84%  | 81.54% | 0.95   |      |
| Testbed 7,8: Detection in the wilderness Longformer 52.50%                                                            | 99.14%      | 75.82%  | 0.94   |        |      |
| Longformer †                                                                                                          | 88.78%      | 84.12%  | 86.54% | 0.94   |      |
| Unseen Domains & Unseen Model                                                                                         | PAWN (GPT2) | 84.12%  | 89.50% | 86.81% | 0.94 |
| PAWN (Llama3-1b)                                                                                                      | 78.87%      | 96.75%  | 87.81% | 0.97   |      |
| Longformer                                                                                                            | 52.16%      | 81.73%  | 66.94% | 0.75   |      |
| Longformer †                                                                                                          | 88.78%      | 37.05%  | 62.92% | 0.75   |      |
| Paraphrasing attacks                                                                                                  | PAWN (GPT2) | 87.00%  | 39.13% | 63.06% | 0.75 |
| PAWN (Llama3-1b)                                                                                                      | 77.53%      | 55.87%  | 66.70% | 0.74   |      |

Table 3: Results for MAGE's testbeds 2-8. Recalls for both classes and their macro-average are reported due to class imbalances, as well as the Area Under the ROC curve. The asterisk * denotes unsupervised models. The dagger
†denotes that the classification boundary has been adjusted by using a portion of training data in each of the TB6 models and averaging the best boundaries. All results except PAWN's are taken from [1].

Table 4: Ablations in MAGE's testbeds 4-8. Recalls for both classes and their macro average are reported due to

class imbalances, as well as the Area Under the ROC curve. We compare the performance of the Perplexity Attention

Weighted Network (PAWN), the hidden state branch (HSFF) and the metrics branch (MPN). The last two columns show

the variation of the macro-averaged recall and AUROC with respect to the in-distribution setting of testbed 4, calculated as the difference between the two values.

Setting Method HumanRec MachineRec AvgRec AUROC AvgRec var AUROC var

Testbed 4: In-distribution Detection

PAWN (GPT2) 93.75% 91.97% 92.86% 0.981

PAWN (Llama3-1b) 90.68% 95.84% **93.26% 0.986**

HSFF (GPT2) 89.05% 81.99% 85.52% 0.932

HSFF (Llama3-1b) 94.57% 83.18% 88.87% 0.960

MPN (GPT2) 83.02% 82.64% 82.83% 0.926

All source models & all domains

| as the difference between the two values. Setting Method   | HumanRec         | MachineRec   | AvgRec   | AUROC   | AvgRec var   | AUROC var   |        |
|------------------------------------------------------------|------------------|--------------|----------|---------|--------------|-------------|--------|
| Testbed 4: In-distribution Detection                       |                  |              |          |         |              |             |        |
| PAWN (GPT2)                                                | 93.75%           | 91.97%       | 92.86%   | 0.981   |              |             |        |
| PAWN (Llama3-1b)                                           | 90.68%           | 95.84%       | 93.26%   | 0.986   |              |             |        |
| HSFF (GPT2)                                                | 89.05%           | 81.99%       | 85.52%   | 0.932   |              |             |        |
| All source models & all domains                            | HSFF (Llama3-1b) | 94.57%       | 83.18%   | 88.87%  | 0.960        |             |        |
| MPN (GPT2)                                                 | 83.02%           | 82.64%       | 82.83%   | 0.926   |              |             |        |
| MPN (Llama3-1b)                                            | 85.49%           | 81.84%       | 83.67%   | 0.927   |              |             |        |
| Testbed 5,6: Out-of-distribution Detection                 |                  |              |          |         |              |             |        |
| PAWN (GPT2)                                                | 93.97%           | 81.43%       | 87.70%   | 0.957   | -5.16%       | -0.024      |        |
| PAWN (Llama3-1b)                                           | 95.17%           | 85.68%       | 90.42%   | 0.970   | -2.83%       | -0.016      |        |
| HSFF (GPT2)                                                | 89.77%           | 67.44%       | 78.60%   | 0.883   | -6.92%       | -0.049      |        |
| Unseen source model                                        | HSFF (Llama3-1b) | 94.60%       | 74.61%   | 84.60%  | 0.937        | -4.27%      | -0.023 |
| MPN (GPT2)                                                 | 86.00%           | 72.89%       | 79.45%   | 0.911   | -3.38%       | -0.015      |        |
| MPN (Llama3-1b)                                            | 88.25%           | 69.19%       | 78.72%   | 0.900   | -4.94%       | -0.027      |        |
| PAWN (GPT2)                                                | 65.17%           | 95.45%       | 80.31%   | 0.936   | -12.55%      | -0.045      |        |
| PAWN (Llama3-1b)                                           | 67.24%           | 95.84%       | 81.54%   | 0.946   | -11.71%      | -0.040      |        |
| HSFF (GPT2)                                                | 53.85%           | 88.12%       | 70.98%   | 0.829   | -14.54%      | -0.104      |        |
| Unseen domain                                              | HSFF (Llama3-1b) | 52.55%       | 90.10%   | 71.32%  | 0.829        | -17.55%     | -0.131 |
| MPN (GPT2)                                                 | 77.86%           | 83.11%       | 80.48%   | 0.917   | -2.34%       | -0.008      |        |
| MPN (Llama3-1b)                                            | 78.99%           | 82.14%       | 80.57%   | 0.906   | -3.10%       | -0.021      |        |
| Testbed 7,8: Detection in the wilderness                   |                  |              |          |         |              |             |        |
| PAWN (GPT2)                                                | 84.12%           | 89.50%       | 86.81%   | 0.942   | -6.05%       | -0.039      |        |
| PAWN (Llama3-1b)                                           | 78.87%           | 96.75%       | 87.81%   | 0.973   | -5.45%       | -0.013      |        |
| HSFF (GPT2)                                                | 66.14%           | 81.25%       | 73.70%   | 0.817   | -11.82%      | -0.116      |        |
| Unseen Domains & Unseen Model                              | HSFF (Llama3-1b) | 71.78%       | 88.88%   | 80.33%  | 0.871        | -8.54%      | -0.089 |
| MPN (GPT2)                                                 | 86.22%           | 75.63%       | 80.92%   | 0.884   | -1.91%       | -0.041      |        |
| MPN (Llama3-1b)                                            | 91.60%           | 77.25%       | 84.43%   | 0.938   | +0.76%       | +0.011      |        |
| PAWN (GPT2)                                                | 87.00%           | 39.13%       | 63.06%   | 0.755   | -29.80%      | -0.226      |        |
| PAWN (Llama3-1b)                                           | 77.53%           | 55.87%       | 66.70%   | 0.735   | -26.56%      | -0.251      |        |
| HSFF (GPT2)                                                | 65.75%           | 71.00%       | 68.37%   | 0.756   | -17.14%      | -0.177      |        |
| Paraphrasing attacks                                       | HSFF (Llama3-1b) | 64.08%       | 58.13%   | 61.10%  | 0.664        | -27.77%     | -0.296 |
| MPN (GPT2)                                                 | 90.97%           | 7.37%        | 49.17%   | 0.528   | -33.66%      | -0.398      |        |
| MPN (Llama3-1b)                                            | 94.05%           | 15.75%       | 54.90%   | 0.688   | -28.77%      | -0.239      |        |

## 4.3 Evaluating Ensembles As A Way To Improve Generalization

In table 5 we show the results from running several ensembles of PAWN models, simply averaging the final logits.

We obtain minor performance gains in the in-distribution setting, although more pronounced in terms of recall than in terms of AUROC. In the out-of-distribution setting with unseen domains and models we find no AUROC improvement, only macro-averaged recall ones. Ensembles do not appear to provide any meaningful improvement in the presence of paraphrasing attacks, which remain very challenging.

## 4.4 Generalization And Multilingualism On M4

As explained earlier, we evaluated the PAWN model in two different settings in the M4 dataset [2, 8]. First, we compare models that are pre-trained on the main corpus of MAGE [1]. Although M4 and MAGE may have some domains in common, all detectors are evaluated under the same conditions, and we still expect a difference in the data distributions.

Second, we performed the full battery of experiments proposed in M4GTBench [8], modifying the unseen domain experiments to retain the binary classification task nature.

## 4.4.1 Models Pre-Trained On Mage

Table 6 shows the M4 results for models pre-trained on the main corpus of MAGE. Let us discuss each section.

No fine-tuning. Consider first the English domains. In terms of AUROC, the best model is RoBERTa, with PAWNLLaMA being a very close second. Overall, all models achieved a good AUROC and seem to generalize nicely to

Table 5: Results from running several ensembles of our model, by simply averaging the final logits, on MAGE's testbeds four, seven and eight. Recalls for both classes and their macro average are reported due to class imbalances, as well as the Area Under the ROC curve.

| the Area Under the ROC curve. Setting    | Backbones   | HumanRec   | MachineRec   | AvgRec   | AUROC   |
|------------------------------------------|-------------|------------|--------------|----------|---------|
| Testbed 4: In-distribution Detection     |             |            |              |          |         |
| All source models & all domains          | GPT2        | 93.75%     | 91.97%       | 92.86%   | 0.981   |
| LLaMA3-1b                                | 90.68%      | 95.84%     | 93.26%       | 0.986    |         |
| 1 GPT2, 1 LLaMA3-1b                      | 94.59%      | 93.92%     | 94.26%       | 0.988    |         |
| 2 GPT2, 2 LLaMA3-1b                      | 95.86%      | 93.55%     | 94.71%       | 0.989    |         |
| 2 GPT2                                   | 93.89%      | 92.27%     | 93.08%       | 0.983    |         |
| 2 LLaMA3-1b                              | 94.41%      | 94.50%     | 94.46%       | 0.988    |         |
| 1 GPT2, 1 LLaMA3-1b, 1 QWEN              | 90.78%      | 96.13%     | 93.45%       | 0.987    |         |
| Testbed 7,8: Detection in the wilderness |             |            |              |          |         |
| Unseen Domains & Unseen Model            | GPT2        | 84.12%     | 89.50%       | 86.81%   | 0.942   |
| LLaMA3-1b                                | 78.87%      | 96.75%     | 87.81%       | 0.973    |         |
| 1 GPT2, 1 LLaMA3-1b                      | 84.78%      | 94.00%     | 89.39%       | 0.961    |         |
| 2 GPT2, 2 LLaMA3-1b                      | 85.70%      | 93.75%     | 89.72%       | 0.963    |         |
| 2 GPT2                                   | 83.33%      | 91.00%     | 87.17%       | 0.943    |         |
| 2 LLaMA3-1b                              | 82.28%      | 95.88%     | 89.08%       | 0.969    |         |
| 1 GPT2, 1 LLaMA3-1b, 1 QWEN              | 82.28%      | 94.50%     | 88.39%       | 0.954    |         |
| Paraphrasing attacks                     | GPT2        | 87.00%     | 39.13%       | 63.06%   | 0.755   |
| LLaMA3-1b                                | 77.53%      | 55.87%     | 66.70%       | 0.735    |         |
| 1 GPT2, 1 LLaMA3-1b                      | 86.49%      | 42.00%     | 64.25%       | 0.751    |         |
| 2 GPT2, 2 LLaMA3-1b                      | 86.62%      | 39.50%     | 63.06%       | 0.739    |         |
| 2 GPT2                                   | 85.21%      | 41.87%     | 63.54%       | 0.747    |         |
| 2 LLaMA3-1b                              | 82.27%      | 43.50%     | 62.88%       | 0.711    |         |
| 1 GPT2, 1 LLaMA3-1b, 1 QWEN              | 82.91%      | 49.25%     | 66.08%       | 0.742    |         |

English texts. When looking at the macro-averaged recall, we observe that PAWN-LLaMA is the best with quite a margin, and PAWN-GPT2 is very close to RoBERTa. As in MAGE, we seem to find that threshold selection is more robust for PAWN models, even with worse discrimination capabilities, as measured by the AUROC.

Considering now non-English domains. we see that the only reliable detector is PAWN-LLaMA, with fairly good average results. Only Bulgarian and Russian texts result in low AUROC and recall scores. Some of the other models also achieve high scores for specific languages, but not on average. These results suggest that with a large backbone LLM that has been trained in multiple languages, PAWN is capable of generalizing to languages not seen during supervised training.

One epoch fine-tune on English domains. After fine-tuning in the English domains, all detectors seem to be able to fit the data very well, with the PAWN models having the best recall. Performance on other languages takes a hit in all cases, with PAWN-LLaMA remaining the only one better than random chance.

One epoch fine-tune on all domains. All detectors are capable of fitting the entire data distribution, including other languages, when trained in all domains. The best overall model is PAWN-LLaMA, but PAWN-GPT2 and RoBERTa are fairly close.

## 4.4.2 M4Gtbench Results

Table 7 shows the results for each of the experiments based on the M4GTBench [8] benchmark. In the **out-ofdistribution domain tests** we find that the strongest model overall is PAWN-GPT2. Although in terms of AUROC
it is a close race, with RoBERTa surpassing PAWN-LLaMA, both PAWN models outperform in terms of accuracy and macro-averaged F1. Thus, we find again that decision boundaries seem to generalize better in PAWN. In the out-of-distribution language tests results are similar to those in the previous section, with PAWN-LLaMA generalizing nicely to other languages, although there is some performance degradation. PAWN-GPT2 does generalize to some of the languages, but still performs worse than XLM-RoBERTa. Finally, in **out-of-distribution model tests** the PAWN
detectors outperform the baselines greatly.

Table 6: Results on the M4 multilingual dataset [2, 8] for models pre-trained on the main corpus of MAGE [1]. We report results for each of the English domains separately, and grouped by language for the other domains. Three settings are included: no fine-tuning, one epoch fine-tune on the English domains, and one epoch fine-tune on all domains. The AUROC, F1 and macro-averaged recall are reported. We also include the average of these metrics across English and non-English domains, as well as the mean of these two averages.

| non-English domains, as well as the mean of these two averages. PAWN (GPT2) PAWN (LLaMA3-1b)   | Longformer     | RoBERTa   |        |         |         |        |        |        |        |         |         |       |
|------------------------------------------------------------------------------------------------|----------------|-----------|--------|---------|---------|--------|--------|--------|--------|---------|---------|-------|
| AvgRec                                                                                         | F1             | AUROC     | AvgRec | F1      | AUROC   | AvgRec | F1     | AUROC  | AvgRec | F1      | AUROC   |       |
|                                                                                                | No fine-tuning |           |        |         |         |        |        |        |        |         |         |       |
| wikihow (en)                                                                                   | 72.96%         | 76.00%    | 0.898  | 83.52%  | 83.84%  | 0.928  | 58.36% | 68.41% | 0.884  | 80.57%  | 81.69%  | 0.921 |
| reddit (en)                                                                                    | 93.94%         | 93.71%    | 0.986  | 95.95%  | 95.81%  | 0.994  | 88.55% | 89.25% | 0.989  | 95.84%  | 95.78%  | 0.992 |
| arxiv (en)                                                                                     | 75.88%         | 73.51%    | 0.756  | 83.90%  | 82.31%  | 0.897  | 87.27% | 85.88% | 0.926  | 88.83%  | 87.47%  | 0.978 |
| wikipedia (en)                                                                                 | 83.59%         | 83.89%    | 0.938  | 87.97%  | 87.78%  | 0.962  | 50.79% | 63.70% | 0.868  | 70.50%  | 74.41%  | 0.934 |
| peerread (en)                                                                                  | 85.84%         | 93.39%    | 0.947  | 90.39%  | 96.44%  | 0.983  | 85.44% | 95.32% | 0.980  | 89.61%  | 96.11%  | 0.981 |
| outfox (en)                                                                                    | 95.13%         | 95.66%    | 0.993  | 98.01%  | 98.17%  | 0.998  | 75.00% | 81.59% | 0.949  | 86.18%  | 88.86%  | 0.994 |
| Bulgarian                                                                                      | 63.84%         | 70.69%    | 0.739  | 58.86%  | 63.32%  | 0.620  | 50.65% | 65.73% | 0.730  | 50.07%  | 65.39%  | 0.381 |
| Chinese                                                                                        | 50.34%         | 54.49%    | 0.530  | 74.47%  | 73.87%  | 0.809  | 50.44% | 65.00% | 0.472  | 52.20%  | 65.52%  | 0.464 |
| Indonesian                                                                                     | 44.76%         | 2.27%     | 0.271  | 71.83%  | 63.49%  | 0.879  | 68.75% | 74.47% | 0.758  | 53.13%  | 20.60%  | 0.736 |
| Urdu                                                                                           | 73.54%         | 77.79%    | 0.813  | 88.14%  | 88.34%  | 0.951  | 50.00% | 70.19% | 0.397  | 50.00%  | 70.19%  | 0.176 |
| Russian                                                                                        | 51.77%         | 65.80%    | 0.467  | 54.41%  | 53.77%  | 0.569  | 49.04% | 64.98% | 0.554  | 50.46%  | 66.25%  | 0.263 |
| German                                                                                         | 61.00%         | 62.34%    | 0.638  | 83.93%  | 82.35%  | 0.920  | 66.35% | 68.08% | 0.703  | 63.22%  | 46.98%  | 0.797 |
| Arabic                                                                                         | 52.67%         | 58.99%    | 0.543  | 77.27%  | 83.92%  | 0.913  | 50.00% | 71.31% | 0.422  | 50.00%  | 71.31%  | 0.649 |
| Italian                                                                                        | 46.42%         | 6.51%     | 0.353  | 74.37%  | 68.48%  | 0.881  | 83.24% | 85.54% | 0.956  | 87.47%  | 85.93%  | 0.983 |
| Avg (en)                                                                                       | 84.56%         | 86.03%    | 0.920  | 89.96%  | 90.73%  | 0.960  | 74.24% | 80.69% | 0.933  | 85.25%  | 87.39%  | 0.967 |
| Avg (non-en)                                                                                   | 55.54%         | 49.86%    | 0.544  | 72.91%  | 72.19%  | 0.818  | 58.56% | 70.66% | 0.624  | 57.07%  | 61.52%  | 0.556 |
| Macro Avg                                                                                      | 70.05%         | 67.94%    | 0.732  | 81.43%  | 81.46%  | 0.889  | 66.40% | 75.68% | 0.778  | 71.16%  | 74.45%  | 0.761 |
| 1 epoch fine-tune on english domains                                                           |                |           |        |         |         |        |        |        |        |         |         |       |
| wikihow (en)                                                                                   | 99.28%         | 99.27%    | 0.998  | 99.59%  | 99.57%  | 0.999  | 98.63% | 98.55% | 0.999  | 99.50%  | 99.47%  | 1.000 |
| reddit (en)                                                                                    | 99.27%         | 99.25%    | 0.999  | 99.33%  | 99.32%  | 0.999  | 92.66% | 92.91% | 0.987  | 96.91%  | 96.89%  | 0.999 |
| arxiv (en)                                                                                     | 99.76%         | 99.76%    | 1.000  | 100.00% | 100.00% | 1.000  | 99.41% | 99.39% | 1.000  | 99.90%  | 99.90%  | 1.000 |
| wikipedia (en)                                                                                 | 99.75%         | 99.75%    | 1.000  | 99.90%  | 99.89%  | 1.000  | 97.12% | 96.86% | 0.999  | 99.77%  | 99.75%  | 1.000 |
| peerread (en)                                                                                  | 98.28%         | 99.42%    | 0.999  | 99.10%  | 99.67%  | 0.998  | 87.73% | 96.81% | 0.994  | 99.38%  | 99.83%  | 1.000 |
| outfox (en)                                                                                    | 99.82%         | 99.83%    | 1.000  | 99.85%  | 99.86%  | 1.000  | 97.47% | 97.77% | 0.998  | 99.25%  | 99.32%  | 1.000 |
| Bulgarian                                                                                      | 50.00%         | 65.43%    | 0.197  | 50.48%  | 54.21%  | 0.514  | 49.57% | 65.05% | 0.404  | 20.27%  | 32.84%  | 0.044 |
| Chinese                                                                                        | 43.83%         | 54.11%    | 0.453  | 83.90%  | 84.67%  | 0.947  | 50.80% | 65.39% | 0.517  | 45.20%  | 45.84%  | 0.407 |
| Indonesian                                                                                     | 58.01%         | 70.76%    | 0.643  | 56.88%  | 69.93%  | 0.849  | 52.29% | 68.19% | 0.813  | 54.58%  | 69.25%  | 0.602 |
| Urdu                                                                                           | 50.00%         | 70.19%    | 0.076  | 68.61%  | 77.08%  | 0.778  | 50.00% | 70.19% | 0.373  | 29.79%  | 48.73%  | 0.020 |
| Russian                                                                                        | 50.00%         | 66.04%    | 0.511  | 49.74%  | 61.21%  | 0.553  | 50.00% | 66.04% | 0.242  | 35.84%  | 51.90%  | 0.124 |
| German                                                                                         | 46.36%         | 61.43%    | 0.207  | 50.85%  | 62.50%  | 0.636  | 47.69% | 61.17% | 0.320  | 7.88%   | 1.61%   | 0.048 |
| Arabic                                                                                         | 50.00%         | 71.31%    | 0.794  | 63.60%  | 73.45%  | 0.735  | 50.00% | 71.31% | 0.646  | 38.72%  | 59.28%  | 0.465 |
| Italian                                                                                        | 50.00%         | 67.50%    | 0.607  | 53.51%  | 69.08%  | 0.804  | 53.16% | 68.92% | 0.986  | 55.96%  | 70.23%  | 0.986 |
| Avg (en)                                                                                       | 99.36%         | 99.55%    | 0.999  | 99.63%  | 99.72%  | 0.999  | 95.50% | 97.05% | 0.996  | 99.12%  | 99.19%  | 1.000 |
| Avg (non-en)                                                                                   | 49.78%         | 65.85%    | 0.436  | 59.70%  | 69.02%  | 0.727  | 50.44% | 67.03% | 0.537  | 36.03%  | 47.46%  | 0.337 |
| Macro Avg                                                                                      | 74.57%         | 82.70%    | 0.718  | 79.66%  | 84.37%  | 0.863  | 72.97% | 82.04% | 0.767  | 67.57%  | 73.33%  | 0.668 |
| 1 epoch fine-tune on all domains                                                               |                |           |        |         |         |        |        |        |        |         |         |       |
| wikihow (en)                                                                                   | 98.91%         | 98.89%    | 1.000  | 99.11%  | 99.09%  | 1.000  | 97.75% | 97.62% | 0.997  | 99.91%  | 99.90%  | 1.000 |
| reddit (en)                                                                                    | 98.56%         | 98.53%    | 0.999  | 99.24%  | 99.22%  | 1.000  | 90.26% | 90.81% | 0.984  | 98.53%  | 98.50%  | 1.000 |
| arxiv (en)                                                                                     | 99.86%         | 99.86%    | 1.000  | 99.93%  | 99.93%  | 1.000  | 99.41% | 99.39% | 0.999  | 100.00% | 100.00% | 1.000 |
| wikipedia (en)                                                                                 | 99.47%         | 99.45%    | 1.000  | 99.51%  | 99.49%  | 1.000  | 95.36% | 95.04% | 0.997  | 99.34%  | 99.28%  | 1.000 |
| peerread (en)                                                                                  | 97.35%         | 99.17%    | 0.996  | 99.37%  | 99.71%  | 1.000  | 82.10% | 95.38% | 0.976  | 98.76%  | 99.67%  | 1.000 |
| outfox (en)                                                                                    | 99.89%         | 99.90%    | 1.000  | 99.70%  | 99.73%  | 1.000  | 95.35% | 95.97% | 0.996  | 99.66%  | 99.69%  | 1.000 |
| Bulgarian                                                                                      | 96.68%         | 96.58%    | 0.992  | 99.42%  | 99.40%  | 1.000  | 94.98% | 94.91% | 0.994  | 97.20%  | 97.12%  | 0.996 |
| Chinese                                                                                        | 94.89%         | 94.73%    | 0.989  | 97.29%  | 97.21%  | 0.997  | 80.44% | 82.59% | 0.974  | 94.21%  | 94.01%  | 0.986 |
| Indonesian                                                                                     | 96.90%         | 97.05%    | 0.992  | 97.60%  | 97.55%  | 0.999  | 93.95% | 94.42% | 0.993  | 98.86%  | 98.89%  | 0.998 |
| Urdu                                                                                           | 98.47%         | 98.51%    | 0.996  | 100.00% | 100.00% | 1.000  | 98.47% | 98.51% | 0.998  | 98.23%  | 98.20%  | 0.984 |
| Russian                                                                                        | 91.98%         | 91.28%    | 0.952  | 98.61%  | 98.59%  | 1.000  | 87.54% | 88.11% | 0.973  | 91.51%  | 90.72%  | 0.990 |
| German                                                                                         | 97.00%         | 96.88%    | 0.993  | 98.35%  | 98.28%  | 0.995  | 90.11% | 90.31% | 0.991  | 98.62%  | 98.58%  | 0.998 |
| Arabic                                                                                         | 93.54%         | 93.33%    | 0.987  | 97.13%  | 97.04%  | 1.000  | 89.29% | 92.06% | 0.992  | 92.68%  | 92.35%  | 0.988 |
| Italian                                                                                        | 97.03%         | 97.19%    | 0.998  | 98.82%  | 98.80%  | 1.000  | 92.63% | 93.38% | 0.999  | 98.95%  | 99.00%  | 1.000 |
| Avg (en)                                                                                       | 99.01%         | 99.30%    | 0.999  | 99.47%  | 99.53%  | 1.000  | 93.37% | 95.70% | 0.992  | 99.37%  | 99.51%  | 1.000 |
| Avg (non-en)                                                                                   | 95.81%         | 95.69%    | 0.987  | 98.40%  | 98.36%  | 0.999  | 90.93% | 91.79% | 0.989  | 96.28%  | 96.11%  | 0.992 |
| Macro Avg                                                                                      | 97.41%         | 97.50%    | 0.993  | 98.94%  | 98.94%  | 0.999  | 92.15% | 93.74% | 0.990  | 97.82%  | 97.81%  | 0.996 |

| of comparable metrics are highlighted in bold.   | OOD Domain       |             |             |          |        |          |          |        |          |        |        |    |
|--------------------------------------------------|------------------|-------------|-------------|----------|--------|----------|----------|--------|----------|--------|--------|----|
| PAWN (GPT2)                                      | PAWN (LLaMA3-1b) | RoBERTa     |             |          |        |          |          |        |          |        |        |    |
| Accuracy                                         | F1-Macro         | AUROC       | Accuracy    | F1-Macro | AUROC  | Accuracy | F1-Macro | AUROC  |          |        |        |    |
| Arxiv                                            | 95.97%           | 95.96%      | 0.988       | 88.25%   | 88.17% | 0.995    | 99.23%   | 99.23% | 1.000    |        |        |    |
| Outfox                                           | 82.41%           | 81.35%      | 0.989       | 76.51%   | 74.22% | 0.890    | 85.63%   | 85.02% | 0.989    |        |        |    |
| PeerRead                                         | 95.02%           | 91.35%      | 0.948       | 94.27%   | 89.90% | 0.960    | 91.53%   | 83.79% | 0.940    |        |        |    |
| Reddit                                           | 92.11%           | 92.04%      | 0.982       | 91.97%   | 91.95% | 0.975    | 82.11%   | 81.92% | 0.958    |        |        |    |
| Wikihow                                          | 94.10%           | 94.08%      | 0.982       | 90.49%   | 90.49% | 0.965    | 86.17%   | 86.17% | 0.942    |        |        |    |
| Wikipedia                                        | 88.04%           | 87.97%      | 0.988       | 92.44%   | 92.43% | 0.989    | 76.23%   | 75.24% | 0.993    |        |        |    |
| Average                                          | 91.27%           | 90.46%      | 0.980       | 88.99%   | 87.86% | 0.962    | 86.82%   | 85.23% | 0.970    |        |        |    |
|                                                  | OOD Language     |             |             |          |        |          |          |        |          |        |        |    |
| PAWN (GPT2)                                      | PAWN (LLaMA3-1b) | XLM-RoBERTa |             |          |        |          |          |        |          |        |        |    |
| Accuracy                                         | F1-Macro         | AUROC       | Accuracy    | F1-Macro | AUROC  | Accuracy | F1-Macro | AUROC  |          |        |        |    |
| Arabic                                           | 75.41%           | 75.20%      | 0.855       | 80.76%   | 79.77% | 0.992    | 92.18%   | 92.12% | -        |        |        |    |
| Bulgarian                                        | 95.92%           | 95.92%      | 0.979       | 98.21%   | 98.21% | 0.998    | 52.74%   | 39.18% | -        |        |        |    |
| Chinese                                          | 63.78%           | 60.22%      | 0.844       | 68.54%   | 65.46% | 0.952    | 82.51%   | 81.93% | -        |        |        |    |
| English                                          | 59.11%           | 58.09%      | 0.695       | 76.71%   | 76.59% | 0.839    | 66.51%   | 64.55% | -        |        |        |    |
| German                                           | 29.86%           | 25.93%      | 0.162       | 73.74%   | 72.88% | 0.833    | 73.62%   | 71.58% | -        |        |        |    |
| Indonesian                                       | 53.74%           | 44.79%      | 0.726       | 83.34%   | 82.96% | 0.960    | 55.83%   | 45.00% | -        |        |        |    |
| Italian                                          | 62.37%           | 57.53%      | 0.783       | 96.43%   | 96.43% | 0.994    | 83.51%   | 83.04% | -        |        |        |    |
| Russian                                          | 89.40%           | 89.36%      | 0.926       | 80.45%   | 79.79% | 0.960    | 53.70%   | 47.60% | -        |        |        |    |
| Urdu                                             | 73.79%           | 72.32%      | 0.970       | 81.59%   | 81.06% | 0.999    | 94.39%   | 94.39% | -        |        |        |    |
| Average                                          | 67.04%           | 64.37%      | 0.771       | 82.20%   | 81.46% | 0.947    | 72.78%   | 68.82% | -        |        |        |    |
|                                                  | OOD Model        |             |             |          |        |          |          |        |          |        |        |    |
| PAWN (GPT2)                                      | PAWN (LLaMA3-1b) | RoBERTa     | XLM-RoBERTa |          |        |          |          |        |          |        |        |    |
| Accuracy                                         | F1               | AUROC       | Accuracy    | F1       | AUROC  | Accuracy | F1       | AUROC  | Accuracy | F1     | AUROC  |    |
| bloomz                                           | 88.36%           | 56.86%      | 0.847       | 87.32%   | 48.57% | 0.858    | 60.30%   | 60.22% | -        | 73.07% | 72.74% | -  |
| chatGPT                                          | 99.38%           | 98.52%      | 0.999       | 99.52%   | 98.87% | 1.000    | 82.99%   | 85.45% | -        | 85.62% | 87.57% | -  |
| cohere                                           | 99.01%           | 97.10%      | 0.999       | 99.09%   | 97.32% | 0.998    | 78.24%   | 81.91% | -        | 86.23% | 87.74% | -  |
| davinci                                          | 97.25%           | 92.33%      | 0.995       | 98.05%   | 94.29% | 0.992    | 79.21%   | 82.58% | -        | 84.32% | 85.23% | -  |
| dolly                                            | 96.72%           | 90.23%      | 0.990       | 96.25%   | 88.18% | 0.994    | 77.78%   | 81.44% | -        | 79.43% | 80.40% | -  |
| gpt4                                             | 99.46%           | 98.55%      | 1.000       | 99.67%   | 99.12% | 1.000    | 79.37%   | 82.90% | -        | 77.95% | 81.93% | -  |
| Average                                          | 96.70%           | 88.93%      | 0.972       | 96.65%   | 87.73% | 0.974    | 76.32%   | 79.08% | -        | 81.10% | 82.60% | -  |

Table 7: Results on the M4 dataset [2, 8] for leave-one-out experiments across English domains (multilingual set),
languages (multilingual set) and models (monolingual set). Results taken from [8] do not report AUROC. Best results of comparable metrics are highlighted in bold.

## 4.5 Generalization To New Decoding Strategies And Robustness To Attacks On Raid

Table 8 shows the main results on the RAID dataset. This table reports the recall at 5% FPR by different categories of examples, depending on whether the model is open-source and instruction-tuned, the decoding strategy, and whether repetition penalty is used. As explained in the methodology, we compare models pre-trained on MAGE, and also fine-tune those models for one epoch on the training set of our own split of RAID. To address each factor individually, we include table 9, where we group the values by each factor (e.g., all greedy decoding results vs. all sampling decoding results), take the median values, and compute the difference. We remark that closed-source models are not included in the results without repetition penalty, as no corresponding counterparts are available.

Without fine-tuning, our models generalize slightly better than RoBERTa, and a lot better than Longformer, especially PAWN-LLaMA. Interestingly, in table 9 we find that our models are much more susceptible to the use of repetition penalty, and less susceptible to whether the model is instruction-tuned or not. One explanation for the first remark is that using repetition penalty tends to produce missing punctuation and stopwords at the end of the text, which results in very unexpected tokens in sharp distributions. This could easily mislead our models, which are based on these metrics.

After a single epoch of fine-tuning, we see that all models score close to perfect, and are capable of adapting to the different factors without trouble. One thing to note about these results is that the metric is not sensitive to threshold choice. This threshold is dynamically calculated to achieve the 5% FPR, and moreover, a different threshold is used for each domain. This hides the weakness we have been observing for fine-tuned LMs in other datasets.

Next, we test the robustness of models trained in RAID to different types of adversarial attack proposed in RAID.

The results appear on table 10. We observe that on average, the PAWN models are the most robust (among models trained under the same conditions). PAWN-LLaMA seems particularly robust, with paraphrasing attacks being the

| on the hidden set.          | Open Source                                                      | Closed Source         |                |          |                             |          |        |          |        |        |        |        |
|-----------------------------|------------------------------------------------------------------|-----------------------|----------------|----------|-----------------------------|----------|--------|----------|--------|--------|--------|--------|
| Chat                        | No Chat                                                          | Chat                  | No Chat        |          |                             |          |        |          |        |        |        |        |
| (llama-c, mistral-c, mpt-c) | (mistral, mpt, gpt2)                                             | (c-gpt, gpt4, cohere) | (cohere, gpt3) |          |                             |          |        |          |        |        |        |        |
| Decoding strategy           | Greedy                                                           | Sampling              | Greedy         | Sampling | Greedy                      | Sampling | Greedy | Sampling |        |        |        |        |
| Repetition Penalty          | ✗                                                                | ✓                     | ✗              | ✓        | ✗                           | ✓        | ✗      | ✓        | ✗      | ✗      | ✗      | ✗      |
|                             | No training on RAID                                              | Avg                   |                |          |                             |          |        |          |        |        |        |        |
| R-B GPT2                    | 84.10% 52.30%                                                    | 77.90%                | 26.20%         | 98.60%   | 44.10% 60.50% 35.40% 70.90% | 41.70%   | 65.10% | 52.50%   | 59.11% |        |        |        |
| R-L GPT2                    | 79.70% 41.10%                                                    | 71.40%                | 19.50%         | 98.50%   | 43.00% 67.20% 53.40% 61.40% | 34.70%   | 61.10% | 48.60%   | 56.63% |        |        |        |
| R-B CGPT                    | 80.20% 63.30%                                                    | 75.50%                | 39.30%         | 53.30%   | 26.40% 14.90%               | 1.70%    | 59.10% | 38.10%   | 46.50% | 39.00% | 44.78% |        |
| RADAR                       | 88.80% 77.40%                                                    | 85.60%                | 66.40%         | 91.80%   | 63.80% 48.30% 31.80% 81.60% | 75.30%   | 72.20% | 67.70%   | 70.89% |        |        |        |
| GLTR                        | 89.80% 67.50%                                                    | 83.90%                | 38.30%         | 99.60%   | 56.90% 44.50%               | 0.50%    | 80.70% | 54.30%   | 75.60% | 63.70% | 62.94% |        |
| F-DetectGPT                 | 98.60% 74.50%                                                    | 96.20%                | 40.50%         | 97.80%   | 56.10% 79.70%               | 0.60%    | 96.00% | 74.10%   | 93.80% | 86.30% | 74.52% |        |
| LLMDet                      | 55.50% 30.20%                                                    | 47.50%                | 16.50%         | 74.80%   | 27.00% 38.40%               | 3.70%    | 35.80% | 18.50%   | 40.00% | 32.90% | 35.07% |        |
| Binoculars                  | 99.90% 86.60%                                                    | 99.70%                | 60.60%         | 99.90%   | 62.30% 72.40%               | 0.60%    | 99.20% | 92.10%   | 99.00% | 95.00% | 80.61% |        |
| GPTZero                     | 98.80% 93.70%                                                    | 98.40%                | 82.50%         | 74.70%   | 34.60%                      | 9.40%    | 4.80%  | 92.30%   | 88.50% | 60.60% | 53.40% | 65.98% |
| Originality                 | 98.60% 86.30%                                                    | 97.70%                | 72.50%         | 99.90%   | 64.10% 89.00% 51.20% 96.80% | 89.00%   | 91.70% | 85.40%   | 85.18% |        |        |        |
| Winston                     | 97.20% 90.10%                                                    | 96.60%                | 78.30%         | 68.20%   | 49.00% 29.50% 11.30% 96.10% | 93.70%   | 73.20% | 68.10%   | 70.94% |        |        |        |
| ZeroGPT*                    | 95.40% 80.70%                                                    | 90.50%                | 54.90%         | 85.10%   | 57.20% 16.00%               | 0.30%    | 92.10% | 65.80%   | 83.40% | 72.70% | 66.18% |        |
| PAWN (GPT2)                 | 96.56% 88.57%                                                    | 93.70%                | 79.30%         | 90.53%   | 84.03% 57.52% 81.56% 90.16% | 72.02%   | 84.34% | 75.37%   | 82.81% |        |        |        |
| PAWN (Llama3-1b)            | 98.33% 92.00%                                                    | 96.26%                | 81.61%         | 98.90%   | 86.85% 52.07% 82.44% 93.10% | 73.24%   | 83.15% | 75.04%   | 84.42% |        |        |        |
| Longformer                  | 87.89% 86.60%                                                    | 86.55%                | 83.43%         | 86.15%   | 83.78% 59.62% 83.63% 81.66% | 68.24%   | 64.13% | 54.11%   | 77.15% |        |        |        |
| RoBERTa                     | 89.89% 98.10%                                                    | 91.14%                | 90.26%         | 85.32%   | 95.55% 49.14% 89.24% 89.04% | 71.97%   | 68.53% | 66.02%   | 82.02% |        |        |        |
| 1 epoch fine-tune on RAID   |                                                                  |                       |                |          |                             |          |        |          |        |        |        |        |
| PAWN (GPT2)                 | 99.90% 99.65%                                                    | 99.85%                | 99.60%         | 99.98%   | 99.83% 98.23% 99.63% 99.08% | 97.73%   | 98.69% | 96.60%   | 99.06% |        |        |        |
| PAWN (Llama3-1b)            | 99.98% 99.98% 100.00% 99.93% 100.00% 99.95% 99.43% 99.93% 99.65% | 98.93%                | 99.63%         | 98.84%   | 99.69%                      |          |        |          |        |        |        |        |
| Longformer                  | 99.78% 99.75%                                                    | 99.65%                | 99.55%         | 99.90%   | 99.10% 97.88% 99.30% 99.15% | 98.53%   | 98.21% | 96.45%   | 98.94% |        |        |        |
| RoBERTa                     | 99.98% 99.95%                                                    | 99.93%                | 99.83%         | 99.93%   | 99.80% 98.88% 99.35% 99.43% | 99.20%   | 99.14% | 98.65%   | 99.50% |        |        |        |

only significantly damaging ones. Longformer, RoBERTa and PAWN-GPT2 are also susceptible to the addition of homoglyphs, the latter to a lesser extent. Zero-width spaces seem to affect only our fine-tuned LM selection, whereas the addition of extra whitespace only affects PAWN-GPT2 significantly.

## 5 Conclusions

In this work, we proposed the Perplexity Attention Weighted Network (PAWN) for AI-generated text detection. Zeroshot methods typically aggregate next-token distribution metrics using a simple mean. Based on the idea that some tokens are naturally easier (e.g. word completions) and harder (e.g. beginnings of texts without prompt conditioning) to predict, we use semantic information from the last hidden states and positional information to weight features based on next-token distribution metrics before aggregating them across the sequence length.

Although not a zero-shot method, our method employs a very small number of trainable parameters, in the order of one million. In addition, since the LLM is frozen, we can cache the hidden states and next-token distribution metrics of training texts on disk, greatly reducing the training resource requirements.

PAWN performs competitively or even better in-distribution than the best baselines, which are fine-tuned LMs. It also generalizes better overall to new models and domains, especially in terms of decision boundaries, as fine-tuned LMs tend to maintain a high AUROC out-of-distribution but drop recall performance due to variations in the optimal boundary.

PAWN shows very strong performance even with a small backbone such as openai−community/gpt2, but a medium backbone such as meta−llama/Llama−3.2−1B−Instruct is slightly stronger in general. It also has better capabilities in other languages, providing decent generalization in languages unseen during supervised training. Finally, we also studied the robustness of PAWN to many types of adversarial attacks. Despite being more robust than the fine-tuned LM baselines on average, paraphrasing attacks are still challenging for our models and further work is still required.

Table 9: Variation of recall at 5% FPR on the RAID dataset, by different factors. We report absolute differences between the median values of each group of results. Closed-source models are not taken into account in the no repetition penalty category, as no corresponding counterparts are available. PAWN models, Longformer and RoBERTa were evaluated on our data split, as the original test split is hidden. The results from other detectors are taken from [7]. These detectors were pre-trained on different training sets, as described in section 3.3.5, and they were tested on the hidden set.

| were pre-trained on different training sets, as described in section 3.3.5, and they were t   | ested on the hidden set.   |                  |         |
|-----------------------------------------------------------------------------------------------|----------------------------|------------------|---------|
| Sampling vs. Greedy                                                                           | RP vs. No RP               | No Chat vs. Chat |         |
|                                                                                               | No training on RAID        |                  |         |
| R-B GPT2                                                                                      | -15.60%                    | -41.25%          | -5.10%  |
| R-L GPT2                                                                                      | -15.45%                    | -33.50%          | +6.00%  |
| R-B CGPT                                                                                      | -17.65%                    | -31.55%          | -28.50% |
| RADAR                                                                                         | -8.00%                     | -22.10%          | -13.75% |
| GLTR                                                                                          | -17.85%                    | -39.25%          | -13.80% |
| F-DetectGPT                                                                                   | -17.80%                    | -48.70%          | -2.25%  |
| LLMDet                                                                                        | -6.35%                     | -29.75%          | +2.65%  |
| Binoculars                                                                                    | -9.75%                     | -38.35%          | -11.95% |
| GPTZero                                                                                       | -12.55%                    | -28.00%          | -49.00% |
| Originality                                                                                   | -6.60%                     | -29.85%          | -5.70%  |
| Winston                                                                                       | -2.55%                     | -18.75%          | -36.35% |
| ZeroGPT*                                                                                      | -15.00%                    | -31.75%          | -20.65% |
| PAWN (GPT2)                                                                                   | -9.66%                     | -9.32%           | -6.56%  |
| PAWN (Llama3-1b)                                                                              | -11.61%                    | -12.66%          | -9.76%  |
| Longformer                                                                                    | -8.96%                     | -2.64%           | -11.11% |
| RoBERTa                                                                                       | -7.91%                     | +5.31%           | -13.15% |
| 1 epoch fine-tune on RAID                                                                     |                            |                  |         |
| PAWN (GPT2)                                                                                   | -0.87%                     | +0.19%           | -0.48%  |
| PAWN (Llama3-1b)                                                                              | -0.34%                     | +0.09%           | -0.11%  |
| Longformer                                                                                    | -0.75%                     | +0.12%           | -0.93%  |
| RoBERTa                                                                                       | -0.30%                     | +0.06%           | -0.43%  |

| R-L GPT2             | RADAR   | GLTR            | Binoculars   | GPTZero   | Originality   | PAWN (GPT2)   | PAWN (LLaMA)   | Longformer   | RoBERTa   |         |
|----------------------|---------|-----------------|--------------|-----------|---------------|---------------|----------------|--------------|-----------|---------|
| None                 | 56.70%  | 65.61%          | 59.69%       | 78.98%    | 66.50%        | 85.00%        | 99.15%         | 99.71%       | 99.03%    | 99.54%  |
| Whitespace           | -16.60% | -4.48%          | -16.64%      | -10.30%   | -0.30%        | -0.10%        | -5.39%         | -0.76%       | -1.59%    | -1.91%  |
| Upper-Lower          | -       | -0.47%          | -14.35%      | -6.14%    | -             | -             | -1.34%         | -0.85%       | -0.69%    | -0.29%  |
| Synonym              | +22.70% | -2.87%          | -30.95%      | -36.92%   | -5.50%        | +11.50%       | -1.37%         | -1.68%       | -0.85%    | -0.29%  |
| Misspelling          | -17.20% | -1.30%          | -2.70%       | -1.74%    | -1.40%        | -6.40%        | -0.58%         | -0.39%       | -0.43%    | -0.27%  |
| Paraphrase           | +16.20% | -3.26%          | -16.74%      | +1.32%    | -2.50%        | +11.70%       | -13.84%        | -13.91%      | -10.55%   | -12.09% |
| Number               | -       | +0.07%          | -2.41%       | -2.62%    | -             | -             | -0.03%         | -0.01%       | -0.02%    | -0.01%  |
| Add Paragraph        | -       | +2.56%          | -1.40%       | -8.32%    | -             | -             | +0.64%         | +0.22%       | +0.78%    | +0.44%  |
| Homoglyph            | -35.40% | -20.78%         | -39.38%      | -42.88%   | -0.30%        | -75.70%       | -9.56%         | -2.23%       | -32.14%   | -15.92% |
| Article Deletion     | -23.50% | -2.61%          | -10.75%      | -5.71%    | -5.50%        | -13.60%       | -0.55%         | -0.39%       | -1.01%    | -0.13%  |
| Alternative Spelling | -       | -0.12%          | -1.46%       | -1.42%    | -             | -             | -0.13%         | -0.07%       | -0.09%    | -0.05%  |
| Zero-Width Space     | -       | +12.79% +38.18% | +19.43%      | -         | -             | +0.85%        | -1.08%         | -7.08%       | -26.73%   |         |
| Avg attacks          | -8.97%  | -1.86%          | -8.96%       | -8.66%    | -2.58%        | -12.10%       | -2.85%         | -1.92%       | -4.88%    | -5.20%  |

Table 10: Recall at 5% FPR on the RAID dataset by adversarial attack. Results in the first box are from models trained on datasets other than RAID, and are evaluated on the official test set. Results in the second box are pre-trained on MAGE, fine-tuned for one epoch on RAID and tested on our own RAID data split. Further, underlined results are taken directly from [7], as the detectors's predictions and results were unavailable on their repository.

## Acknowledgments

This work has been supported by the project PCI2022-134990-2 (MARTINI) of the CHISTERA IV Cofund 2021 program; by European Comission under IBERIFIER Plus - Iberian Digital Media Observatory (DIGITAL-2023-
DEPLOY- 04-EDMO-HUBS 101158511), and by TUAI Project (HORIZON-MSCA-2023-DN-01-01, Proposal number:
101168344) projects; by EMIF managed by the Calouste Gulbenkian Foundation, in the project MuseAI; and by Comunidad Autonoma de Madrid, CIRMA-CM Project (TEC-2024/COM-404).

## References

[1] Y. Li et al. "MAGE: Machine-Generated Text Detection in the Wild". In: *Proceedings of the 62nd Annual Meeting* of the Association for Computational Linguistics (Volume 1: Long Papers). Bangkok, Thailand: Association for Computational Linguistics, 2024, pp. 36–53. DOI: 10.18653/v1/2024.acl-long.3. (Visited on 12/10/2024).

[2] Y. Wang et al. "M4: Multi-Generator, Multi-Domain, and Multi-Lingual Black-Box Machine-Generated Text Detection". In: Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers). Ed. by Y. Graham and M. Purver. St. Julian's, Malta: Association for Computational Linguistics, Mar. 2024, pp. 1369–1407.

[3] A. Conneau et al. "Unsupervised Cross-Lingual Representation Learning at Scale". In: *Proceedings of the* 58th Annual Meeting of the Association for Computational Linguistics. Online: Association for Computational Linguistics, 2020, pp. 8440–8451. DOI: 10.18653/v1/2020.acl-main.747. (Visited on 12/13/2024).

[4] J. Kirchenbauer et al. "A Watermark for Large Language Models". In: *Proceedings of the 40th International* Conference on Machine Learning. PMLR.

[5] K. Krishna et al. "Paraphrasing Evades Detectors of AI-Generated Text, but Retrieval Is an Effective Defense".

In: *Thirty-Seventh Conference on Neural Information Processing Systems*. 2023.

[6] S. S. Ghosal et al. *Towards Possibilities & Impossibilities of AI-Generated Text Detection: A Survey*. Oct. 2023.

arXiv: 2310.15264 [cs]. (Visited on 10/23/2024).

[7] L. Dugan et al. "RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors".

In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:
Long Papers). Bangkok, Thailand: Association for Computational Linguistics, 2024, pp. 12463–12492. DOI:
10.18653/v1/2024.acl-long.674. (Visited on 12/13/2024).

[8] Y. Wang et al. "M4GT-Bench: Evaluation Benchmark for Black-Box Machine-Generated Text Detection".

In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:
Long Papers). Bangkok, Thailand: Association for Computational Linguistics, 2024, pp. 3964–3992. DOI:
10.18653/v1/2024.acl-long.218. (Visited on 12/17/2024).

[9] J. Bevendorff et al. "Overview of the "Voight-Kampff" Generative AI Authorship Verification Task at PAN and ELOQUENT 2024". In: *Working Notes of CLEF 2024 - Conference and Labs of the Evaluation Forum*. Ed. by G. Faggioli et al. CEUR Workshop Proceedings. CEUR-WS.org, Sept. 2024.

[10] A. Uchendu et al. "TURINGBENCH: A Benchmark Environment for Turing Test in the Age of Neural Text Generation". In: *Findings of the Association for Computational Linguistics: EMNLP 2021*. Punta Cana, Dominican Republic: Association for Computational Linguistics, 2021, pp. 2001–2016. DOI: 10.18653/v1/2021.findingsemnlp.172. (Visited on 12/30/2024).

[11] V. Verma et al. "Ghostbuster: Detecting Text Ghostwritten by Large Language Models". In: Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics:
Human Language Technologies (Volume 1: Long Papers). Mexico City, Mexico: Association for Computational Linguistics, 2024, pp. 1702–1717. DOI: 10.18653/v1/2024.naacl-long.95. (Visited on 12/30/2024).

[12] B. Guo et al. *How Close Is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection*. Jan.

2023. DOI: 10.48550/arXiv.2301.07597. arXiv: 2301.07597 [cs]. (Visited on 12/26/2024).

[13] *Openai/Gpt-2-Output-Dataset*. OpenAI. Dec. 2024. (Visited on 12/26/2024).

[14] J. Kirchenbauer et al. "On the Reliability of Watermarks for Large Language Models". In: *The Twelfth International Conference on Learning Representations*. 2024.

[15] J. Devlin et al. "BERT: Pre-Training of Deep Bidirectional Transformers for Language Understanding". In:
Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers). Minneapolis, Minnesota:
Association for Computational Linguistics, June 2019, pp. 4171–4186. DOI: 10.18653/v1/N19-1423. (Visited on 09/25/2023).

[16] Y. Liu et al. *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. July 2019. arXiv: 1907.11692 [cs].

(Visited on 09/01/2023).

[17] A. Uchendu et al. "Authorship Attribution for Neural Text Generation". In: *Proceedings of the 2020 Conference* on Empirical Methods in Natural Language Processing (EMNLP). Online: Association for Computational Linguistics, 2020, pp. 8384–8395. DOI: 10.18653/v1/2020.emnlp-main.673. (Visited on 01/02/2025).

[18] A. Bakhtin et al. *Real or Fake? Learning to Discriminate Machine from Human Generated Text*. Nov. 2019. DOI:
10.48550/arXiv.1906.03351. arXiv: 1906.03351 [cs]. (Visited on 01/02/2025).

[19] W. Antoun et al. "Towards a Robust Detection of Language Model-Generated Text: Is ChatGPT That Easy to Detect?" In: *Actes de CORIA-TALN 2023. Actes de La 30e Conférence Sur Le Traitement Automatique Des* Langues Naturelles (TALN), Volume 1 : Travaux de Recherche Originaux - Articles Longs. Ed. by C. Servan and A. Vilnat. Paris, France: ATALA, June 2023, pp. 14–27.

[20] I. Solaiman et al. *Release Strategies and the Social Impacts of Language Models*. Nov. 2019. DOI: 10.48550/
arXiv.1908.09203. arXiv: 1908.09203 [cs]. (Visited on 01/02/2025).

[21] S. Gehrmann, H. Strobelt, and A. Rush. "GLTR: Statistical Detection and Visualization of Generated Text". In:
Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics: System Demonstrations.

Florence, Italy: Association for Computational Linguistics, 2019, pp. 111–116. DOI: 10.18653/v1/P19-3019.

(Visited on 12/26/2024).

[22] E. Mitchell et al. "DetectGPT: Zero-Shot Machine-Generated Text Detection Using Probability Curvature". In:
Proceedings of the 40th International Conference on Machine Learning. PMLR, July 2023, pp. 24950–24962.

(Visited on 03/21/2024).

[23] C. Raffel et al. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer". In: *Journal* of Machine Learning Research 21.140 (2020), pp. 1–67.

[24] G. Bao et al. "Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature". In: *The Twelfth International Conference on Learning Representations*. 2024.

[25] J. Su et al. "DetectLLM: Leveraging Log Rank Information for Zero-Shot Detection of Machine-Generated Text". In: *Findings of the Association for Computational Linguistics: EMNLP 2023*. Singapore: Association for Computational Linguistics, 2023, pp. 12395–12412. DOI: 10.18653/v1/2023.findings-emnlp.827.

(Visited on 12/31/2024).

[26] A. Hans et al. *Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text*. Jan. 2024. arXiv:
2401.12070 [cs]. (Visited on 05/04/2024).

[27] A. Bhattacharjee and H. Liu. "Fighting Fire with Fire: Can ChatGPT Detect AI-Generated Text?" In: ACM
SIGKDD Explorations Newsletter 25.2 (Mar. 2024), pp. 14–21. ISSN: 1931-0145, 1931-0153. DOI: 10.1145/
3655103.3655106. (Visited on 12/31/2024).

[28] R. Koike, M. Kaneko, and N. Okazaki. OUTFOX: LLM-Generated Essay Detection Through In-Context Learning with Adversarially Generated Examples. Feb. 2024. DOI: 10.48550/arXiv.2307.11729. arXiv: 2307.11729
[cs]. (Visited on 12/31/2024).

[29] A. Radford et al. "Language Models Are Unsupervised Multitask Learners". In: (2019).

[30] A. Grattafiori et al. *The Llama 3 Herd of Models*. Nov. 2024. DOI: 10.48550/arXiv.2407.21783. arXiv:
2407.21783 [cs]. (Visited on 12/10/2024).

[31] C. Tan et al. "Winning Arguments: Interaction Dynamics and Persuasion Strategies in Good-Faith Online Discussions". In: *Proceedings of the 25th International Conference on World Wide Web*. Montréal Québec Canada: International World Wide Web Conferences Steering Committee, Apr. 2016, pp. 613–624. ISBN: 978-1-4503-4143-1. DOI: 10.1145/2872427.2883081. (Visited on 12/10/2024).

[32] X. Zhang, J. Zhao, and Y. LeCun. "Character-Level Convolutional Networks for Text Classification". In: Advances in Neural Information Processing Systems. Ed. by C. Cortes et al. Vol. 28. Curran Associates, Inc., 2015.

[33] S. Narayan, S. B. Cohen, and M. Lapata. "Don't Give Me the Details, Just the Summary! Topic-Aware Convolutional Neural Networks for Extreme Summarization". In: *Proceedings of the 2018 Conference on Empirical* Methods in Natural Language Processing. Brussels, Belgium: Association for Computational Linguistics, 2018, pp. 1797–1807. DOI: 10.18653/v1/D18-1206. (Visited on 12/10/2024).

[34] JulesBelveze/Tldr_news · *Datasets at Hugging Face*. https://huggingface.co/datasets/JulesBelveze/tldr_news.

(Visited on 12/10/2024).

[35] A. Fan et al. "ELI5: Long Form Question Answering". In: *Proceedings of the 57th Annual Meeting of the* Association for Computational Linguistics. Florence, Italy: Association for Computational Linguistics, 2019, pp. 3558–3567. DOI: 10.18653/v1/P19-1346. (Visited on 12/10/2024).

[36] A. Fan, M. Lewis, and Y. Dauphin. "Hierarchical Neural Story Generation". In: Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). Melbourne, Australia:
Association for Computational Linguistics, 2018, pp. 889–898. DOI: 10.18653/v1/P18-1082. (Visited on 12/10/2024).

[37] N. Mostafazadeh et al. "A Corpus and Cloze Evaluation for Deeper Understanding of Commonsense Stories".

In: *Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational* Linguistics: Human Language Technologies. San Diego, California: Association for Computational Linguistics, 2016, pp. 839–849. DOI: 10.18653/v1/N16-1098. (Visited on 12/10/2024).

[38] R. Zellers et al. "HellaSwag: Can a Machine Really Finish Your Sentence?" In: *Proceedings of the 57th Annual* Meeting of the Association for Computational Linguistics. Florence, Italy: Association for Computational Linguistics, 2019, pp. 4791–4800. DOI: 10.18653/v1/P19-1472. (Visited on 12/10/2024).

[39] P. Rajpurkar et al. "SQuAD: 100,000+ Questions for Machine Comprehension of Text". In: *Proceedings of* the 2016 Conference on Empirical Methods in Natural Language Processing. Austin, Texas: Association for Computational Linguistics, 2016, pp. 2383–2392. DOI: 10.18653/v1/D16-1264. (Visited on 12/10/2024).

[40] H. Chen, H. Takamura, and H. Nakayama. "SciXGen: A Scientific Paper Dataset for Context-Aware Text Generation". In: *Findings of the Association for Computational Linguistics: EMNLP 2021*. Punta Cana, Dominican Republic: Association for Computational Linguistics, 2021, pp. 1483–1492. DOI: 10.18653/v1/2021.findingsemnlp.128. (Visited on 12/10/2024).

[41] A. See, P. J. Liu, and C. D. Manning. "Get To The Point: Summarization with Pointer-Generator Networks".

In: *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1:*
Long Papers). Vancouver, Canada: Association for Computational Linguistics, 2017, pp. 1073–1083. DOI:
10.18653/v1/P17-1099. (Visited on 12/10/2024).

[42] Y. Chen et al. "DialogSum: A Real-Life Scenario Dialogue Summarization Dataset". In: *Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021*. Online: Association for Computational Linguistics, 2021, pp. 5062–5074. DOI: 10.18653/v1/2021.findings-acl.449. (Visited on 12/10/2024).

[43] Q. Jin et al. "PubMedQA: A Dataset for Biomedical Research Question Answering". In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). Hong Kong, China: Association for Computational Linguistics, 2019, pp. 2567–2577. DOI: 10.18653/v1/D19-1259. (Visited on 12/10/2024).

[44] A. L. Maas et al. "Learning Word Vectors for Sentiment Analysis". In: *Proceedings of the 49th Annual Meeting* of the Association for Computational Linguistics: Human Language Technologies. Ed. by D. Lin, Y. Matsumoto, and R. Mihalcea. Portland, Oregon, USA: Association for Computational Linguistics, June 2011, pp. 142–150.

[45] H. Touvron et al. *LLaMA: Open and Efficient Foundation Language Models*. Feb. 2023. arXiv: 2302.13971
[cs]. (Visited on 01/20/2024).

[46] T. Brown et al. "Language Models Are Few-Shot Learners". In: *Advances in Neural Information Processing* Systems. Vol. 33. Curran Associates, Inc., 2020, pp. 1877–1901. (Visited on 09/25/2023).

[47] H. W. Chung et al. "Scaling Instruction-Finetuned Language Models". In: *Journal of Machine Learning Research* 25.70 (2024), pp. 1–53.

[48] V. Sanh et al. "Multitask Prompted Training Enables Zero-Shot Task Generalization". In: *International Conference on Learning Representations*. 2022.

[49] B. Wang. *Mesh-Transformer-JAX: Model-Parallel Implementation of Transformer Language Model with JAX*.

May 2021.

[50] S. Black et al. "GPT-NeoX-20B: An Open-Source Autoregressive Language Model". In: *Proceedings of BigScience Episode \#5 - Workshop on Challenges & Perspectives in Creating Large Language Models*. Ed.

by A. Fan et al. virtual+Dublin: Association for Computational Linguistics, May 2022, pp. 95–136. DOI:
10.18653/v1/2022.bigscience-1.9.

[51] S. Zhang et al. *OPT: Open Pre-Trained Transformer Language Models*. June 2022. DOI: 10.48550/arXiv.

2205.01068. arXiv: 2205.01068 [cs]. (Visited on 12/10/2024).

[52] A. Zeng et al. "GLM-130B: An Open Bilingual Pre-Trained Model". In: The Eleventh International Conference on Learning Representations. 2023.

[53] OpenAI et al. *GPT-4 Technical Report*. Mar. 2024. DOI: 10.48550/arXiv.2303.08774. arXiv: 2303.08774
[cs]. (Visited on 12/10/2024).

[54] M. Koupaee and W. Y. Wang. *WikiHow: A Large Scale Text Summarization Dataset*. Oct. 2018. DOI: 10.48550/
arXiv.1810.09305. arXiv: 1810.09305 [cs]. (Visited on 12/19/2024).

[55] D. Kang et al. "A Dataset of Peer Reviews (PeerRead): Collection, Insights and NLP Applications". In: Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics:
Human Language Technologies, Volume 1 (Long Papers). New Orleans, Louisiana: Association for Computational Linguistics, 2018, pp. 1647–1661. DOI: 10.18653/v1/N18-1149. (Visited on 12/19/2024).

[56] T. Shamardina et al. "Findings of the The RuATD Shared Task 2022 on Artificial Text Detection in Russian".

In: *Computational Linguistics and Intellectual Technologies*. June 2022, pp. 497–511. DOI: 10.28995/20757182-2022-21-497-511. arXiv: 2206.01583 [cs]. (Visited on 12/19/2024).

[57] S. Hassan. *Urdu News Dataset 1M*. Jan. 2021. DOI: 10.17632/834VSXNB99.3. (Visited on 12/19/2024).

[58] *Introducing ChatGPT*. https://openai.com/index/chatgpt/. (Visited on 12/19/2024).

[59] *Command Models: The AI-Powered Solution for the Enterprise*. https://cohere.com/command. (Visited on 12/19/2024).

[60] M. Conover et al. *Free Dolly: Introducing the World's First Truly Open Instruction-Tuned LLM*.

https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm. 2023.

(Visited on 06/30/2023).

[61] N. Muennighoff et al. "Crosslingual Generalization through Multitask Finetuning". In: arXiv preprint arXiv:2211.01786 (2022). arXiv: 2211.01786.

[62] H. Touvron et al. *Llama 2: Open Foundation and Fine-Tuned Chat Models*. July 2023. arXiv: 2307.09288 [cs].

(Visited on 01/20/2024).

[63] N. Sengupta et al. *Jais and Jais-Chat: Arabic-Centric Foundation and Instruction-Tuned Open Generative Large* Language Models. Sept. 2023. DOI: 10.48550/arXiv.2308.16149. arXiv: 2308.16149 [cs]. (Visited on 01/03/2025).

[64] M. N. Team. *Introducing MPT-30B: Raising the Bar for Open-Source Foundation Models*.

www.mosaicml.com/blog/mpt-30b. 2023. (Visited on 06/22/2023).

[65] L. Ouyang et al. "Training Language Models to Follow Instructions with Human Feedback". In: *Advances* in Neural Information Processing Systems. Ed. by S. Koyejo et al. Vol. 35. Curran Associates, Inc., 2022, pp. 27730–27744.

[66] D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering". In: *Proceedings of the 23rd International Conference on Machine Learning - ICML '06*. Pittsburgh, Pennsylvania: ACM Press, 2006, pp. 377–384. ISBN: 978-1-59593-383-6. DOI: 10.1145/1143844.1143892.

(Visited on 12/19/2024).

[67] Aaditya Bhat. *GPT-Wiki-Intro (Revision 0e458f5)*. 2023. DOI: 10.57967/hf/0326.

[68] S. Paul and S. Rakshit. *arXiv Paper Abstracts*. https://www.kaggle.com/datasets/spsayakpaul/arxiv-paperabstracts. (Visited on 12/19/2024).

[69] M. Bien et al. "RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation". In: ´ *Proceedings of the 13th International Conference on Natural Language Generation*. Dublin, Ireland: Association for Computational Linguistics, 2020, pp. 22–28. DOI: 10.18653/v1/2020.inlg-1.4. (Visited on 12/19/2024).

[70] M. Völske et al. "TL;DR: Mining Reddit to Learn Automatic Summarization". In: Proceedings of the Workshop on New Frontiers in Summarization. Copenhagen, Denmark: Association for Computational Linguistics, 2017, pp. 59–63. DOI: 10.18653/v1/W17-4508. (Visited on 12/19/2024).

[71] M. Arman. *Poems Dataset (NLP)*. https://www.kaggle.com/datasets/michaelarman/poemsdataset. (Visited on 12/19/2024).

[72] D. Bamman and N. A. Smith. *New Alignment Methods for Discriminative Book Summarization*. May 2013. DOI:
10.48550/arXiv.1305.1319. arXiv: 1305.1319 [cs]. (Visited on 12/19/2024).

[73] A. Joulin et al. "Bag of Tricks for Efficient Text Classification". In: Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers. Ed. by M. Lapata, P. Blunsom, and A. Koller. Valencia, Spain: Association for Computational Linguistics, Apr. 2017, pp. 427–431.

[74] I. Beltagy, M. E. Peters, and A. Cohan. *Longformer: The Long-Document Transformer*. Dec. 2020. arXiv:
2004.05150 [cs]. (Visited on 04/09/2024).

[75] X. Hu, P.-Y. Chen, and T.-Y. Ho. "RADAR: Robust AI-Text Detection via Adversarial Learning". In: *ThirtySeventh Conference on Neural Information Processing Systems*. 2023.

[76] A. Hans et al. "Spotting LLMs with Binoculars: Zero-Shot Detection of Machine-Generated Text". In: *Proceedings of the 41st International Conference on Machine Learning*. Ed. by R. Salakhutdinov et al. Vol. 235.

Proceedings of Machine Learning Research. PMLR, 2024-07-21/2024-07-27, pp. 17519–17537.

[77] K. Wu et al. "LLMDet: A Third Party Large Language Models Generated Text Detection Tool". In: Findings of the Association for Computational Linguistics: EMNLP 2023. Singapore: Association for Computational Linguistics, 2023, pp. 2113–2133. DOI: 10.18653/v1/2023.findings-emnlp.139. (Visited on 12/26/2024).

## A Binoculars Results

As Binoculars [26] was not a very strong baseline in MAGE [1] and M4 [2, 8], we include its results in both benchmarks in this appendix. They are shown in tables 11 and 12. We note that the important metric is the AUROC, as the threshold is not re-trained. Something interesting happens in MAGE, as in some testbeds machine-generated texts produce higher scores than human-generated ones, and in others the opposite is the case.

Table 11: Results of the Binoculars [26] model in MAGE [1], with the default models backbone *tiiuae/falcon-7b-instruct* and *tiiuae/falcon-7b*, and without re-training the threshold.

| Setting                             | HumanRec   | MachineRec   | AvgRec   | AUROC   |
|-------------------------------------|------------|--------------|----------|---------|
| TB4: All source model & all domains | 23.25%     | 14.57%       | 18.91%   | 0.3129  |
| TB7: Unseen Domains & Unseen Model  | 16.40%     | 18.00%       | 17.20%   | 0.2388  |
| TB8: Paraphrasing attacks           | 16.65%     | 26.88%       | 21.76%   | 0.7258  |

|                | Binoculars   |        |        |
|----------------|--------------|--------|--------|
| AvgRec         | F1           | AUROC  |        |
| wikihow (en)   | 16.42%       | 25.45% | 0.496  |
| reddit (en)    | 13.69%       | 22.62% | 0.212  |
| arxiv (en)     | 14.03%       | 22.61% | 0.421  |
| wikipedia (en) | 14.49%       | 23.37% | 0.354  |
| peerread (en)  | 16.58%       | 24.63% | 0.220  |
| outfox (en)    | 74.44%       | 80.43% | 0.787  |
| Bulgarian      | 0.83%        | 1.63%  | 0.705  |
| Chinese        | 18.83%       | 29.53% | 0.350  |
| Indonesian     | 22.24%       | 31.32% | 0.902  |
| Urdu           | 1.62%        | 3.14%  | 0.818  |
| Russian        | 13.33%       | 20.68% | 0.491  |
| German         | 52.28%       | 63.07% | 0.972  |
| Arabic         | 1.29%        | 2.51%  | 0.749  |
| Italian        | 24.37%       | 35.41% | 0.867  |
| Avg (en)       | 24.94%       | 33.18% | 41.49% |
| Avg (non-en)   | 16.85%       | 23.41% | 73.16% |
| Macro Avg      | 20.90%       | 28.30% | 57.32% |

Table 12: Results of the Binoculars [26] model in M4 [2, 8], with the default models backbone *tiiuae/falcon-7b-instruct* and *tiiuae/falcon-7b*, and without re-training the threshold.