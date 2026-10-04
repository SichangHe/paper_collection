## DetectLLM: Leveraging Log Rank Information for Zero-Shot Detection of Machine-Generated Text

Jinyan Su<sup>1</sup> , Terry Yue Zhuo<sup>2</sup> , Di Wang<sup>3</sup> , Preslav Nakov<sup>1</sup> <sup>1</sup>Mohamed bin Zayed University of Artificial Intelligence <sup>2</sup>Monash University and CSIRO's Data61, <sup>3</sup>King Abdullah University of Science and Technology {Jinyan.Su, preslav.nakov}@mbzuai.ac.ae terry.zhuo@monash.edu,di.wang@kaust.edu.sa

## Abstract

With the rapid progress of Large language models (LLMs) and the huge amount of text they generated, it becomes more and more impractical to manually distinguish whether a text is machine-generated. Given the growing use of LLMs in social media and education, it prompts us to develop methods to detect machine-generated text, preventing malicious usage such as plagiarism, misinformation, and propaganda. Previous work has studied several zero-shot methods, which require no training data. These methods achieve good performance, but there is still a lot of room for improvement. In this paper, we introduce two novel zero-shot methods for detecting machinegenerated text by leveraging the log rank information. One is called DetectLLM-LRR, which is fast and efficient, and the other is called DetectLLM-NPR, which is more accurate, but slower due to the need for perturbations. Our experiments on three datasets and seven language models show that our proposed methods improve over the state of the art by 3.9 and 1.75 AUROC points absolute. Moreover, DetectLLM-NPR needs fewer perturbations than previous work to achieve the same level of performance, which makes it more practical for real-world use. We also investigate the efficiency–performance trade-off based on users preference on these two measures and we provide intuition for using them in practice effectively. We release the data and the code of both methods in [https://github.com/](https://github.com/mbzuai-nlp/DetectLLM.) [mbzuai-nlp/DetectLLM.](https://github.com/mbzuai-nlp/DetectLLM.)

## 1 Introduction

Large language models (LLMs) have made rapid advancement in recent years, and are now able to generate text with significantly improved diversity, fluency, and quality. Models such as Chat-GPT [\(OpenAI,](#page-9-0) [2022\)](#page-9-0), GPT-3 [\(Brown et al.,](#page-9-1) [2020\)](#page-9-1), LLaMa [\(Touvron et al.,](#page-10-0) [2023\)](#page-10-0) and BLOOM [\(Scao](#page-10-1) [et al.,](#page-10-1) [2022\)](#page-10-1) demonstrate exceptional performance

in answering questions [\(Robinson et al.,](#page-10-2) [2022\)](#page-10-2), writing stories [\(Fan et al.,](#page-9-2) [2018;](#page-9-2) [Yuan et al.,](#page-10-3) [2022\)](#page-10-3), composing emails, analyzing program code, and thus facilitating daily life and improving work efficiency. However, LLMs can also be misused for generating plagiarized text, misinformation, and propaganda, which can lead to negative consequences. For instance, students might use LLMs to write their essays and assignments [\(Rosenblatt,](#page-10-4) [2023\)](#page-10-4), making fair evaluation difficult for teachers, and in the long run, undermining the integrity of the entire education system. Malicious actors might generate fake news articles to spread misinformation and propaganda or to manipulate the public opinion, which is dangerous, especially when it comes to politics [\(Floridi and Chiriatti,](#page-9-3) [2020;](#page-9-3) [Stokel-Walker,](#page-10-5) [2022\)](#page-10-5).

With the proliferation of LLMs and the increasing amount of texts it produced, it is challenging for humans to accurately identify machine-generated texts [\(Gehrmann et al.,](#page-9-4) [2019\)](#page-9-4). Moreover, it is unrealistic to hire humans to manually identify machinegenerated text at scale due to the prohibitively high costs and the efficiency requirements in real-time applications, e.g., in social media. Thus, it is essential to develop tools and strategies to automatically identify machine-generated text and to mitigate the potential negative impact of LLMs.

The problem of distinguishing machinegenerated from human-written text is commonly formulated as a binary classification task [\(Jawahar](#page-9-5) [et al.,](#page-9-5) [2020\)](#page-9-5). Most previous work has focused on the black-box scenario, where the detector has access to the output of the LLMs only and cannot make use of its internal representations and states. They train or fine-tune a supervised binary classification model using the output of the LLMs. Such methods lack flexibility since they need to be retrained from scratch to be able to recognize the output of a new LLM [\(Mitchell](#page-9-6) [et al.,](#page-9-6) [2023\)](#page-9-6). Given the speed at which new LLMs

are developed, black-box methods are becoming more and more expensive and impractical. In cases when the access to the LLM is via an API only, one possibility is for the LLM owner to record all content it has generated, or to watermark all texts it has generated [\(Kirchenbauer et al.,](#page-9-7) [2023;](#page-9-7) [Zhao et al.,](#page-10-6) [2023\)](#page-10-6). However, such solutions are not feasible for third-parties.

We therefore consider a white-box setting, where the detector has full access to the LLMs. More specifically, we focus on zero-shot methods, where we use the LLM itself, without additional training. Generally speaking, zero-shot methods uses the source LLM to extract statistics such as the average per-token log probability or the average rank of each token in the ranked list of possible choices, and then to make a prediction by comparing it to a threshold [\(Solaiman et al.,](#page-10-7) [2019;](#page-10-7) [Ippolito et al.,](#page-9-8) [2019;](#page-9-8) [Gehrmann et al.,](#page-9-4) [2019\)](#page-9-4). Recently, [Mitchell](#page-9-6) [et al.](#page-9-6) [\(2023\)](#page-9-6) observed that machine-generated text tends to lie in the negative curvature of the log likelihood of the text, proposing a perturbation-based zero-shot method called DetectGPT and achieving the best performance at the expense of efficiency.

Here, we introduce two novel zero-shot methods, which extensively exploit the potential of the log rank information. The first one is using Log-Likelihood Log-Rank ratio (LRR), which complements Log-Likelihood with Log-Rank to enhance the performance. The second one uses a Normalized perturbed log rank (NPR), which is based on the intuition that machine-generated texts are more sensitive to minor rewrites (or say, small perturbations). We called these two methods DetectLLM-LRR and DetectLLM-NPR respectively.

In summary, our contributions are as follows:

- We propose two novel zero-shot approaches based on log rank statistics, which improve over the state of the art. On average, the proposed two methods improved upon the previous best zero-shot methods by 3.9 and 1.75 AUROC points absolute.
- We investigate the efficacy of existing zeroshot methods and explore their boundaries and limits as the size of the LLMs increases from 1.5 to 20 billion.
- We conduct comprehensive experiments to better understand the efficiency–performance

<span id="page-1-0"></span>![](_page_1_Figure_7.jpeg)

Figure 1: Distribution of LRR and NPR visualized on 300 human-written texts (HG) from the WritingPrompts dataset [\(Fan et al.,](#page-9-2) [2018\)](#page-9-2) as well as 300 texts generated with GPT2-xl (MG) by prompting it with the first 30 tokens from human-written texts.

trade-offs in zero-shot methods, thereby providing interesting insights on how to choose among different categories of zero-shot methods based on users' preference on performance or efficiency.

## 2 Related Work

The detection of machine-generated text is commonly formulated as a classification task [\(Jawahar](#page-9-5) [et al.,](#page-9-5) [2020;](#page-9-5) [Fagni et al.,](#page-9-9) [2021;](#page-9-9) [Bakhtin et al.,](#page-9-10) [2019;](#page-9-10) [Sadasivan et al.,](#page-10-8) [2023\)](#page-10-8). One way of solving it is to use supervised learning, where a classification model is trained on a dataset containing both machine-generated and human-written texts. For example, GPT2 Detector [\(Solaiman et al.,](#page-10-7) [2019\)](#page-10-7) fine-tunes RoBERTa [\(Liu et al.,](#page-9-11) [2019\)](#page-9-11) on the output of GPT2, while the ChatGPT Detector [\(Guo et al.,](#page-9-12) [2023\)](#page-9-12) fine-tunes RoBERTa on the HC3 [\(Guo et al.,](#page-9-12) [2023\)](#page-9-12) dataset. However, models trained explicitly to detect machine-generated texts may overfit to their training distribution of the domains [\(Bakhtin](#page-9-10) [et al.,](#page-9-10) [2019;](#page-9-10) [Uchendu et al.,](#page-10-9) [2020\)](#page-10-9).

Another stream of work attempts to distinguish machine-generated from human-written texts based on statistical irregularities in the entropy [\(Lavergne](#page-9-13) [et al.,](#page-9-13) [2008\)](#page-9-13), perplexity [\(Beresneva,](#page-9-14) [2016\)](#page-9-14) or in the n-gram frequencies [\(Badaskar et al.,](#page-8-0) [2008\)](#page-8-0). [Gehrmann et al.](#page-9-4) [\(2019\)](#page-9-4) introduced hand-crafted statistical features to assist humans in detectingmachine generated texts. Moreover, [\(Solaiman](#page-10-7) [et al.,](#page-10-7) [2019\)](#page-10-7) noted the efficacy of simple zero-shot methods for detecting machine-generated text by evaluating the per-token log probability of texts and using thresholding. [Mitchell et al.](#page-9-6) [\(2023\)](#page-9-6) observed that machine-generated texts tend to lie in the local curvature of the log probability and proposed DetectGPT, whose prominent performance can only

<span id="page-2-1"></span>![](_page_2_Figure_0.jpeg)

Figure 2: Comparison of DetectGPT to NPR averaged across six models (in terms of AUROC). (The full results are given in Figure 6 in the Appendix).

be guaranteed by the large size of the perturbation function and by a large number of perturbations, and thus costs more computational resources.

Other work explored watermarking, which imprints specific patterns of the LLM output text that can be detected by an algorithm while being imperceptible to humans. Grinbaum and Adomaitis (2022) and Abdelnabi and Fritz (2021) watermarked machine-generated text using syntax tree manipulation, while Kirchenbauer et al. (2023) required access to the LLM's logits at each time step to add the watermark.

## 3 Improved Zero-Shot Approaches by Leveraging Log Rank Information

In this section, we introduce the Log-Likelihood Log-Rank Ratio (LRR) and the Normalized Perturbed log-Rank (NPR). LRR combines logrank and log-likelihood as they provide complimentary information about the evaluated text. NPR is based on the idea that the log rank of machinegenerated texts should be more sensitive to smaller perturbations.

#### 3.1 Log-Likelihood Log-Rank Ratio (LRR)

We define Log-Likelihood Log-Rank Ratio as

$$LRR = \left| \frac{\frac{1}{t} \sum_{i=1}^{t} \log p_{\theta}(x_{i}|x_{< i})}{\frac{1}{t} \sum_{i=1}^{t} \log r_{\theta}(x_{i}|x_{< i})} \right|$$
$$= -\frac{\sum_{i=1}^{t} \log p_{\theta}(x_{i}|x_{< i})}{\sum_{i=1}^{t} \log r_{\theta}(x_{i}|x_{< i})},$$

where  $r_{\theta}(x_i|x_{< i}) \ge 1$  is the rank of token  $x_i$  conditioned on the previous tokens.

The Log-Likelihood in the numerator represents the absolute confidence for the correct token, while the Log-Rank in the denominator accounts for the relative confidence, which reveals complimentary information about the texts. As illustrated in Figure 1, LRR is generally larger for machinegenerated text, which can be used for distinguish-

ing machine-generated from human-written text. One plausible reason might be that for machine-generated text, the log rank is more discernible than the log likelihood, so LRR illustrates this pattern for machine-generated text. In Sections 4 and 6, we experimentally show that LRR is a better discriminator than either the log likelihood or the log rank. We call the zero-shot method using LRR as a detection feature as DetectLLM-LRR, and use abbreviation LRR in the rest of the paper.

## 3.2 Normalized Log-Rank Perturbation (NPR)

We define the normalized perturbed log rank as

$$NPR = \frac{\frac{1}{n} \sum_{p=1}^{n} \log r_{\theta}(\tilde{x}_{p})}{\log r_{\theta}(x)},$$

where small perturbations are applied on the target text x to produce the perturbed text  $\tilde{x}_p$ . Here, perturbation means minor rewrites of the texts, such as replacing some of the words. We call the zeroshot method using NPR as a detection feature as DetectLLM-NPR, and use abbreviation NPR in the rest of the paper.

The motivation for NPR is that machine-generated and human-written texts are both negatively affected by small perturbations, i.e., the log rank score will increase after perturbations, but machine-generated text is more susceptible to perturbations and thus increasing more on log rank score after perturbation, which suggests higher NPR score for machine-generated texts. As shown in Figure 1, NPR can be a discernible signal for distinguishing machine-generated from human-written text. DetectGPT (Mitchell et al., 2023) uses a similar idea, but experimentally, we find NPR to be more efficient and to perform better. Details and comparisons are given in Section 4.

#### <span id="page-2-0"></span>4 Experimental Setup

In this section, we conduct comprehensive experiments to evaluate the performance of LRR and NPR in comparison to several methods previosuly proposed in the literatu. We experiment with LLMs sizes varying from 1.5B to 20B parameters, probing the boundary of zero-shot methods when LLMs continue to grow in size. We further study the impact of the perturbation function used, the number of perturbations (specially for NPR and Detect-GPT), the decoding strategy, and the temperature used.

#### 4.1 Data

Following [\(Mitchell et al.,](#page-9-6) [2023\)](#page-9-6), we use three datasets: XSum [\(Narayan et al.,](#page-9-16) [2018\)](#page-9-16), SQuAD [\(Rajpurkar et al.,](#page-10-10) [2016\)](#page-10-10), WritingPrompts [\(Fan](#page-9-2) [et al.,](#page-9-2) [2018\)](#page-9-2), containing news articles, Wikipedia paragraphs and prompted stories, respectively as human-written texts while attain machinegenerated texts using LLMs. These datasets are chosen to represent the areas where LLMs could have a negative impact. For each experiment, we evaluate 300 machine-generated and humanwritten texts pairs by prompting the LLMs with the first 30 tokens of the human-written text. The whole data-generation process is released with our codes.

#### 4.2 Evaluation Measure

Following previous work [\(Mitchell et al.,](#page-9-6) [2023;](#page-9-6) [He et al.,](#page-9-17) [2023;](#page-9-17) [Krishna et al.,](#page-9-18) [2023\)](#page-9-18), we measure the performance using the area under the receiver operating characteristic curve (AUROC), which is the probability that a classifier correctly ranks the machine-generated example higher than humanwritten example. Since for zero-shot methods, detection rates are heavily dependent on the threshold when using discriminative statistics, the AUROC metric is commonly used to measure zero-shot detector performance, which considers the range of all possible thresholds [\(Krishna et al.,](#page-9-18) [2023\)](#page-9-18).

## 4.3 Methods

## 4.3.1 Zero-Shot Methods

We compare the following zero-shot methods:

- log p(x): the idea is that a passage with a high average log probability is more likely to have been generated by the target LLM;
- Rank: the idea is that a passage with a higher average rank is more likely to have been generated by the target LLM;
- Log-Rank: passage with higher average observed log rank is more likely to have been generated by the target LLM;
- Entropy: machine-generated text has higher entropy;
- DetectGPT: machine-generated text has more negative log probability curvature.

More detail and exact definition of these methods can be found in Appendix [A.](#page-11-0)

These zero-shot baselines, along with our newly proposed LRR and NPR, can be categorized into two groups:

- Perturbation-free: log p(x), Rank, Log-Rank, Entropy, LRR. These methods only query the LLM for statistics about the target text x.
- Perturbation Based: DetectGPT and NPR. These methods query the LLM not only for the target text x, but also for perturbed versions thereof x˜1, · · · , x˜p.

Since perturbation-based methods generally perform better (but are also more time-consuming), for fair comparison, we compare them within their own group.

#### 4.3.2 Supervised Methods

We also experiment with two supervised detectors: RoBERTa-base and RoBERTa-Large. However, as these are not central for our narrative, we put the results and the analysis in Appendix [B.](#page-12-0)

#### 4.4 Experimental Details

For the perturbation-based methods (DetectGPT and NPR), we use T5-3B as the perturbation model and we perturb the input text 50 times for all the experiments, unless specified otherwise. For all zero-shot methods, we use sampling with a temperature of 1, unless specified otherwise. More details about the experiments are given in Appendix [A.](#page-11-0)

## 5 Evaluation Results

#### 5.1 Zero-Shot Results

Table [1](#page-4-0) shows a comparison of the five baseline zero-shot approaches to our proposed LRR and NPR, grouped as perturbation-based and perturbation-free. We can see that for the perturbation based methods, NPR consistently outperforms DetectGPT on all datasets and LLMs, except for one case, with an average improvement of 0.90, 2.03, 2.32 AUROC points absolute on XSum, SQuAD, and WritingPrompts, respectively, (using the same perturbation function and the same number of perturbations). For the experiments among perturbation-free methods, on average, our method achieves the best performance and improves by 2.15, 8.27, 1.28 AUROC points absolute

<span id="page-4-0"></span>

| Dataset  | PerturbationMethod |                  |       |       | GPT2-xl Neo-2.7 OPT-2.7 GPT-j |       | OPT-13 | Llama-13 NeoX |                                                                      | Avg.                                      |
|----------|--------------------|------------------|-------|-------|-------------------------------|-------|--------|---------------|----------------------------------------------------------------------|-------------------------------------------|
|          |                    | log<br>p         | 89.16 | 87.69 | 86.98                         | 83.10 | 83.90  | 56.89         | 78.16                                                                | 80.84                                     |
|          |                    | Rank             | 79.79 | 77.87 | 76.07                         | 76.28 | 74.10  | 48.81         | 72.44                                                                | 72.19                                     |
|          | w/o                | Log Rank         | 91.75 | 90.79 | 89.18                         | 86.42 | 85.88  | 61.33         | 81.44                                                                | 83.83                                     |
| XSum     |                    | Entropy          | 56.78 | 55.14 | 50.34                         | 55.51 | 50.98  | 69.43         | 60.84                                                                | 57.00                                     |
|          |                    | LRR (ours) 93.47 |       | 92.24 | 88.70                         | 88.68 | 83.79  | 71.07         | 83.89                                                                | 85.98                                     |
|          |                    | DetectGPT 98.80  |       | 99.11 | 96.02                         | 95.88 | 92.65  | 73.55         | 93.58                                                                | 92.80                                     |
|          | w/                 | NPR (ours) 99.40 |       | 99.46 | 97.09                         | 95.76 | 94.63  | 75.51         | 94.08                                                                | 93.70                                     |
|          |                    | log<br>p         | 90.72 | 84.18 | 87.84                         | 78.20 | 80.65  | 42.91         | 68.78                                                                | 76.18                                     |
|          |                    | Rank             | 83.46 | 79.77 | 81.85                         | 79.46 | 77.47  | 54.44         | 73.10                                                                | 75.65                                     |
|          | w/o                | Log Rank         | 94.33 | 89.52 | 91.76                         | 83.37 | 85.05  | 48.28         | 73.88<br>80.88                                                       |                                           |
| SQuAD    |                    | Entropy          | 57.97 | 58.48 | 53.29                         | 58.26 | 57.14  | 69.71         | 59.97                                                                | 59.26                                     |
|          |                    | LRR (ours) 97.42 |       | 95.74 | 95.89                         | 91.59 | 91.36  | 68.78         | 83.31                                                                | 89.15                                     |
|          |                    | DetectGPT 98.52  |       | 95.86 | 96.91                         | 88.66 | 90.60  | 47.03         | 76.84                                                                | 84.92                                     |
|          | w/                 | NPR (ours) 99.40 |       | 97.56 | 98.39                         | 91.88 | 93.04  | 48.67         | 79.73<br>93.27<br>81.64<br>95.14<br>37.89<br>96.56<br>92.94<br>96.72 | 86.95                                     |
|          |                    | log<br>p         | 96.71 | 95.63 | 95.05                         | 94.43 | 92.53  | 83.54         |                                                                      | 93.02                                     |
|          |                    | Rank             | 87.62 | 82.79 | 83.89                         | 83.21 | 83.52  | 77.64         |                                                                      | 82.90                                     |
|          | w/o                | Log Rank         | 98.02 | 97.15 | 96.32                         | 96.06 | 94.34  | 88.11         |                                                                      | 95.02<br>39.32<br>96.30<br>94.90<br>97.22 |
| WritingP |                    | Entropy          | 36.45 | 34.07 | 39.75                         | 36.93 | 42.49  | 47.64         |                                                                      |                                           |
|          |                    | LRR (ours) 98.34 |       | 98.02 | 96.45                         | 96.97 | 95.09  | 92.66         |                                                                      |                                           |
|          |                    | DetectGPT 99.30  |       | 98.71 | 98.33                         | 95.52 | 96.46  | 83.01         |                                                                      |                                           |
|          | w/                 | NPR (ours) 99.78 |       | 99.59 | 98.87                         | 98.07 | 98.14  | 89.39         |                                                                      |                                           |

Table 1: Zero-shot experiments. Comparison of the proposed LRR and NPR to other zero-shot methods in terms of AUROC. For fair comparison, we show in bold the best results, both with and without perturbations.

<span id="page-4-1"></span>

|          |          |          | w/ Perturbation |          |         |            |           |            |
|----------|----------|----------|-----------------|----------|---------|------------|-----------|------------|
| Decoding | Dataset  | log<br>p | Rank            | Log Rank | Entropy | LRR (ours) | DetectGPT | NPR (ours) |
|          | XSum     | 81.64    | 70.68           | 85.19    | 55.47   | 89.25      | 91.34     | 92.93      |
| top-k    | SQuAD    | 76.31    | 74.31           | 81.28    | 57.96   | 90.61      | 82.42     | 84.99      |
|          | WritingP | 93.80    | 82.15           | 95.72    | 37.26   | 97.10      | 93.89     | 96.33      |
|          | XSum     | 86.94    | 70.86           | 88.65    | 53.89   | 88.29      | 92.74     | 93.42      |
| top-p    | SQuAD    | 82.07    | 75.03           | 85.49    | 55.86   | 91.09      | 83.98     | 86.19      |
|          | WritingP | 96.51    | 82.48           | 97.44    | 33.92   | 97.25      | 94.20     | 96.55      |

Table 2: Decoding strategy analysis. Shown are the AUROC scores for methods with top-k (k = 40) and top-p (p = 0.96) sampling averaged across four LLMs: Neo-2.7, OPT-2.7, GPT-j, Llama-13.

over the second-best perturbation-free method (i.e., log rank) on XSum, SQuAD, and WritingPrompts, respectively. Moreover, we find that in some cases, LRR can even perform better than perturbation based methods, e.g., on SQuAD, LRR outperforms DetectGPT by 4.23 AUROC point absolute and outperforms NPR by 2.20 AUROC points.

#### <span id="page-4-2"></span>5.2 Comparing DetectGPT to NPR

Equipped with large perturbation functions and adequate amount of perturbations, perturbation-based methods generally outperform perturbation-free

ones, e.g., using T5-3b as the perturbation function and perturb 50 times as in Table [1.](#page-4-0) However, in practice, due to time and resource constraint, not all users can afford these models and large amount of perturbations. Thus, it is important to investigate how NPR and DetectGPT behave with smaller perturbation function size and fewer perturbations.

Different Number of Perturbations. Figure [2](#page-2-1) shows the averaged performance of DetectGPT and NPR with varying number of perturbations. We can see that NPR consistently performs better than DetectGPT when using the same number of pertur-

<span id="page-5-0"></span>

| Perturbation | l<br>Dataset | # (Perturbations) |       |       |       |  |  |  |
|--------------|--------------|-------------------|-------|-------|-------|--|--|--|
| Function     | Dataset      | 10                | 20    | 50    | 100   |  |  |  |
|              | T5-large     | 86.69             | 88.00 | 88.74 | 88.94 |  |  |  |
| NPR (ours)   | T5-3b        | 91.39             | 92.35 | 93.04 | 93.20 |  |  |  |
|              | Diff         | 4.70              | 4.35  | 4.30  | 4.26  |  |  |  |
|              | T5-large     | 77.94             | 81.12 | 83.90 | 84.54 |  |  |  |
| DetectGPT    | T5-3b        | 86.70             | 89.57 | 91.38 | 92.10 |  |  |  |
|              | Diff         | 8.76              | 8.45  | 7.48  | 7.56  |  |  |  |

Table 3: **Perturbation analysis.** Comparing DetectGPT to NPR using different perturbations (AUROC scores).

bations. In other words, NPR can achieve a comparable or better performance but with significantly fewer perturbations. For example, in SQuAD and WritingPrompts dataset, NPR achieves 85 points and 95 points using approximately 10 perturbations while DetectGPT requires around 100 perturbations, which highlights the effectiveness and efficiency of NPR. More complete results for each dataset and models can be found in Figure 6 and Figure 7 of Appendix C.

**Different Perturbation Functions.** In Table 3, we compare NPR with DetectGPT using smaller perturbation model T5-large, and the result is averaged over 6 LLMs and 3 datasets. We found that, not surprisingly, replacing T5-3b to smaller models harms the performance of both NPR and DetectGPT, and the performance degradation can't be mitigated by increasing the number of perturbations. For both NPR and DetectGPT, the average performance of 100 perturbations with T5-large is still worse than 10 perturbations with T5-3b (emphasized with gray box in Table 3). Moreover, one can observe that, NPR is less affected by the reduced perturbation function size: when replacing T5-3b to T5-large, the performance degradation averaged over 10, 20, 50, 100 perturbations for NPR is 4.40 point, much smaller compared to that of 8.06 point for DetectGPT. The complete results on 6 LLMs and 3 datasets can be found in Figure 8 of Appendix C.

# 5.3 Different Decoding Strategy and Temperature

In this subsection, we study different decoding strategy and temperature to see how these factors impact different zero-shot detectors.

**Alternative Decoding Strategies.** In line with prior work (Pagnoni et al., 2022), we experimented

with top-k sampling (Fan et al., 2018) and top-psampling (Holtzman et al., 2019). Top-k sampling generates from top-k most likely words according to the LLM. Top-p sampling (nucleus sampling) samples from the set of words that collectively accounts for a total mass probability p. The result (averaged across 4 LLMs) are shown in Table 2, and complete results can be found in Table 8 of Appendix D. We find that, although almost all the zero-shot methods performs better when using topk and top-p sampling than temperature sampling, Log Rank and Log Likelihood method are more in favor of top-p sampling, while LRR is stable in both top-p and top-k sampling. For top-k decoding, LRR improves 4.06, 9.33, 1.38 points over the second best zero-shot method baseline on three datasets, respectively. LRR performance also improves when using top-p decoding strategy, but due to the unstable performance surge of Log Rank method, LRR become slightly behind Log Rank method, with a minor difference of 0.36 and 0.19 points on XSum and WritingPrompts dataset, respectively. For perturbation based methods, their behavior is consistent with previous results, where NPR outperforms DetectGPT for both top-p and top-k sampling strategies.

**Different Temperature.** Temperature controls the degree of randomness of the generation process. Increasing the temperature leads to more randomness and creativity, while reducing it leads to more conservation and less novelty. In practice, people adjust temperature for their specific purposes. For example, students might set a high temperature to encourage more original and diverse output when writing a creative essay, whereas fake news producers might set lower temperatures to generate seemingly convincing news articles for their deceptive purposes. Based on our experiments in Table 4, we found that Log Likelihood ( $\log p$ ), Log Rank and LRR is highly sensitive to the temperature and can get even better results than perturbation based methods when the temperature is relatively low. In addition, the performance improvement of Rank method with the increased temperature is negligible compared to Log Likelihood, Log Rank and LRR, while the performance of entropy method seems to be positively correlated to the temperature. We conjure that the abnormal behavior of Entropy method might be because of the assumption "machine generated text has higher entropy" (Mitchell et al., 2023), which, from our experi-

<span id="page-6-1"></span>

|             |          |       | w/o Perturbation |         | w/ Perturbation |           |            |
|-------------|----------|-------|------------------|---------|-----------------|-----------|------------|
| Temperature | log<br>p | Rank  | Log Rank         | Entropy | LRR (ours)      | DetectGPT | NPR (ours) |
| 0.5         | 98.72    | 77.87 | 99.29            | 25.90   | 99.23           | 86.14     | 95.76      |
| 0.7         | 97.01    | 76.98 | 98.05            | 38.28   | 98.84           | 90.28     | 95.61      |
| 0.9         | 90.04    | 75.82 | 92.28            | 47.14   | 94.50           | 90.33     | 92.89      |
| 0.95        | 86.15    | 75.43 | 88.88            | 50.42   | 92.04           | 89.97     | 91.98      |
| 1           | 81.48    | 74.85 | 84.81            | 52.37   | 89.15           | 89.02     | 90.86      |

Table 4: Temperature experiments. Results of using different temperatures (AUROC scores).

ments, doesn't stand for high temperature. As for perturbation based method, the impact of temperature is not so clear as perturbation-free method. But in general, the results suggest the temperature has only minor effects on DetectGPT while it improves the performance of NPR. Another observation is that, perturbation-free method performs better than perturbation based method in low temperature, for example, for temperature is smaller than 0.95, perturbation based methods get better detection accuracy while being efficient.

## <span id="page-6-0"></span>6 Analysis of the Efficiency

Though in Table [1,](#page-4-0) perturbation based methods appear to be significantly better than perturbationfree methods, it is important to note that their superior performances can only be achieved with large perturbation functions and multiple number of perturbations, which leads to intensive demand for computational resources and longer computational time. Thus, while performance is an important factor, it is crucial to consider the efficiency of these zero-shot methods as well.

#### 6.1 Computational Cost Analysis

To get an idea of how costly different zero-shot methods are to achieve their performance in Table [1,](#page-4-0) we estimated the computational time (per sample) for each zero-shot method (Detailed results can be found in Table [9](#page-16-1) of Appendix [E\)](#page-16-2). For perturbation based methods, we used 50 perturbations with T5-3b as in the main experiment for the estimation. We observed that the computational time of Log Likelihood, Rank, Log Rank and Entropy are almost the same, while LRR runs approximately 2 times longer than these methods, since it requests both the Log Rank and Log Likelihood statistics. For perturbation based methods, the running time is at least 50 times longer compared to Log Likelihood, Rank, Log Rank, Entropy method, since they

calculate the Log Likelihood or Log Rank for not only the target text, but also perturbed samples.

Composition of the Computational Time. In general, for perturbation-free zero-shot methods, the computational time only depends on the size of LLM and the complexity of statistics. LRR is twice as complex as simple statistics such as Log Rank and Log Likelihood, so it takes approximately twice as long to compute. As for LLM size, intuitively, larger models usually takes more time to compute, which can also be observed in Table [9.](#page-16-1) The additional computational time of perturbation based methods comes from two folds: (1) The total time for perturbation, which depends on the perturbation function we use and the number of perturbations. (2) The total time for calculating statistics of the perturbed texts, which depends on the number of perturbations, the size of LLM and the complexity of statistics. To reduce the computational time of perturbation based method, we could either choose smaller size of perturbation function or reduce the number of perturbations.

## Formula for Estimating the Computational Time. Let t<sup>p</sup> be the time of perturbing 1 sample, t<sup>m</sup> be the time of calculating a simple statistics

(such as log likelihood) of one sample for a particular LLM and n be the number of perturbations. The computational time for log likelihood, rank, log rank, entropy is approximately tm, the estimated time for LRR is 2 · tm, while the estimated computational time for perturbation based method is n · t<sup>p</sup> + (n + 1) · tm. The estimated value of t<sup>p</sup> and t<sup>m</sup> are illustrated in Table [5,](#page-7-0) which can help us estimate the total running time (in seconds) of different zero-shot methods.

#### 6.2 Balancing Efficiency and Performance

In this subsection, we provide additional experiments on LRR (the best perturbation-free method) and NPR (the best perturbation based method, more

<span id="page-7-0"></span>

|       |          | tp(s)   |          |         |         |         | tm(s) |        |          |      |
|-------|----------|---------|----------|---------|---------|---------|-------|--------|----------|------|
| T5-3b | T5-large | T5-base | T5-small | GPT2-xl | Neo-2.7 | OPT-2.7 | GPT-j | OPT-13 | Llama-13 | NeoX |
| 0.10  | 0.08     | 0.04    | 0.03     | 0.06    | 0.09    | 0.10    | 0.04  | 0.07   | 0.07     | 0.60 |

Table 5: Computation time. Estimated computation time for one perturbation (tp) and for calculating the target statistics on the text (tm): shown in seconds.

time consuming than LRR but also rather satisfactory performance) to provide users some intuition on setting parameters of NPR and choosing among between these two methods according to user's preference of efficiency and performance.

First, we study the perturbation function used for NPR. Different from Section [5.2,](#page-4-2) where the focus is to illustrate the advanced performance of NPR compared with DetectGPT, here, we mainly focus on the efficiency performance trade-off perspective and provide some intuition on choosing perturbation functions.

T5-small and T5-base are not good candidates for perturbation functions. T5-small and T5 base are 2 or 3 times faster than larger models such as T5-large (as shown in Table [5\)](#page-7-0), one might wonder if it is possible to trade the saved time with more perturbations for a better performance? We give a negative answer to this. We observe in Figure [3](#page-8-2) that using T5-base and T5-small performs worse than LRR even with 50 to 100 perturbations, which suggests that LRR can be at least 50 to 100 times faster while outperform perturbation based methods. So, if the user can only afford T5-small or T5-base as perturbation function, they should choose LRR with no hesitation since it achieves both better efficiency and better performance.

Cost-Effectiveness on More Perturbations and Larger Perturbation Function. In Figure [4,](#page-8-3) we illustrate the effectiveness of LRR compared to NPR with T5-large and T5-3b as perturbation function respectively, from which, we find that (1) T5- 3b has a higher performance upper limits compared with T5-large. So, if resources are allowed (enough memory and adequate perturbation time), t5-3b would be a better choice, especially for users that prioritize performance. (2) To achieve the same performance as LRR, generally we only need less than 10 perturbations using T5-3b as perturbation function. This estimate could help us choose whether to use NPR or LRR on validation set: setting the number of perturbation to be 10, if LRR outperforms NPR, we would suggest use LRR, otherwise, NPR would be a better option. (3) To achieve the same performance, using T5-large takes more than 2 times perturbations than using T5-3b, while the perturbation time using T5-3b is less than twice of the time using T5-large, so using large perturbation functions such as T5-3b is much more efficient than using smaller ones such as T5-large. The only concern is the memory.

In summary, when parameterizing perturbation function and the number of perturbations, we suggest using the lager perturbation functions if memory permits, which is more cost-effective: less timeconsuming for achieving the same performance and has a high performance upper limit. In addition, setting the number of perturbation to be 10 would be a good threshold on the validation set to decide whether to use NPR or LRR.

## 7 Conclusion

In this paper, we proposed two simple but effective zero-shot machine generated text detection methods by leveraging the log rank information. The methods we proposed —LRR and NPR—, achieve state-of-the-art performance within their respective category. In addition, we explored different settings such as decoding strategy and temperatures, as well as different perturbation functions and number of perturbations to better understand the advantages and the disadvantages of different zero-shot methods. Then, we analyzed the computational costs of these methods, and we provided guidance on balancing efficiency and performance.

## 8 Limitations and Future Directions

One of the limitation of zero-shot methods is the white box assumption that we can have some statistics about the source model. This induces two problems: for close-source models (such as GPT-3), these statistics might not have been provided. Moreover, in practice, the detector might have to run the model locally to get the statistics for the purpose of detection, which requires that the detector have enough resources to use the LLM for inference.

<span id="page-8-2"></span>![](_page_8_Figure_0.jpeg)

Figure 3: Comparing LRR and NPR when T5-small and T5-base are used for perturbation in NPR (AUROC scores).

<span id="page-8-3"></span>![](_page_8_Figure_2.jpeg)

Figure 4: Comparing LRR and NPR when T5-3b and T5-large are used for the perturbation in NPR (AUROC scores).

Based on the limitations of zero-shot methods, we consider weak supervised learning [\(Ratner et al.,](#page-10-11) [2017\)](#page-10-11) as an important direction for future work. Though many papers in MGTD assume knowing the source LLM where the text is generated from, in realistic, the source LLM might be unknown, so it is worth combining weak supervised learning as well as weak supervision sources (other LLMs at hand that might not be the target LLM) to weakly train a classifier. With the flexibility of the weak supervision sources, the limitations of our work could possibly be addressed: (1) Since the weak supervision sources do not have to be from the same target model, there is no need to assume that the target LLM is known. (2) Since the weak supervision sources are classifiers, we could only use statistics that are within reach, or even statistics from other open-source LLMs. (3) The weak supervision sources can be from smaller LLMs, rather than the target LLM, this relaxes the requirement for running an extremely large LLM locally.

## References

<span id="page-8-1"></span>Sahar Abdelnabi and Mario Fritz. 2021. Adversarial watermarking transformer: Towards tracing text provenance with data hiding. In *2021 IEEE Symposium on Security and Privacy (SP)*, pages 121–140. IEEE.

<span id="page-8-0"></span>Sameer Badaskar, Sachin Agarwal, and Shilpa Arora. 2008. Identifying real or fake articles: Towards bet-

- ter language modeling. In *Proceedings of the Third International Joint Conference on Natural Language Processing: Volume-II*.
- <span id="page-9-10"></span>Anton Bakhtin, Sam Gross, Myle Ott, Yuntian Deng, Marc'Aurelio Ranzato, and Arthur Szlam. 2019. Real or fake? learning to discriminate machine from human generated text. *arXiv preprint arXiv:1906.03351*.
- <span id="page-9-14"></span>Daria Beresneva. 2016. Computer-generated text detection using machine learning: A systematic review. In *Natural Language Processing and Information Systems: 21st International Conference on Applications of Natural Language to Information Systems, NLDB 2016, Salford, UK, June 22-24, 2016, Proceedings 21*, pages 421–426. Springer.
- <span id="page-9-23"></span>Sid Black, Stella Biderman, Eric Hallahan, Quentin Anthony, Leo Gao, Laurence Golding, Horace He, Connor Leahy, Kyle McDonell, Jason Phang, Michael Pieler, USVSN Sai Prashanth, Shivanshu Purohit, Laria Reynolds, Jonathan Tow, Ben Wang, and Samuel Weinbach. 2022. [Gpt-neox-20b: An open](https://doi.org/10.48550/ARXIV.2204.06745)[source autoregressive language model.](https://doi.org/10.48550/ARXIV.2204.06745)
- <span id="page-9-21"></span>Sid Black, Gao Leo, Phil Wang, Connor Leahy, and Stella Biderman. 2021. [GPT-Neo: Large](https://doi.org/10.5281/zenodo.5297715) [Scale Autoregressive Language Modeling with Mesh-](https://doi.org/10.5281/zenodo.5297715)[Tensorflow.](https://doi.org/10.5281/zenodo.5297715) If you use this software, please cite it using these metadata.
- <span id="page-9-1"></span>Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. *Advances in neural information processing systems*, 33:1877–1901.
- <span id="page-9-9"></span>Tiziano Fagni, Fabrizio Falchi, Margherita Gambini, Antonio Martella, and Maurizio Tesconi. 2021. Tweepfake: About detecting deepfake tweets. *Plos one*, 16(5):e0251415.
- <span id="page-9-2"></span>Angela Fan, Mike Lewis, and Yann Dauphin. 2018. Hierarchical neural story generation. *arXiv preprint arXiv:1805.04833*.
- <span id="page-9-3"></span>Luciano Floridi and Massimo Chiriatti. 2020. Gpt-3: Its nature, scope, limits, and consequences. *Minds and Machines*, 30:681–694.
- <span id="page-9-22"></span>Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al. 2020. The pile: An 800gb dataset of diverse text for language modeling. *arXiv preprint arXiv:2101.00027*.
- <span id="page-9-4"></span>Sebastian Gehrmann, Hendrik Strobelt, and Alexander M Rush. 2019. Gltr: Statistical detection and visualization of generated text. *arXiv preprint arXiv:1906.04043*.
- <span id="page-9-15"></span>Alexei Grinbaum and Laurynas Adomaitis. 2022. The ethical need for watermarks in machine-generated language. *arXiv preprint arXiv:2209.03118*.

- <span id="page-9-12"></span>Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang, Jinran Nie, Yuxuan Ding, Jianwei Yue, and Yupeng Wu. 2023. How close is chatgpt to human experts? comparison corpus, evaluation, and detection. *arXiv preprint arXiv:2301.07597*.
- <span id="page-9-17"></span>Xinlei He, Xinyue Shen, Zeyuan Chen, Michael Backes, and Yang Zhang. 2023. Mgtbench: Benchmarking machine-generated text detection. *arXiv preprint arXiv:2303.14822*.
- <span id="page-9-20"></span>Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 2019. The curious case of neural text degeneration. *arXiv preprint arXiv:1904.09751*.
- <span id="page-9-8"></span>Daphne Ippolito, Daniel Duckworth, Chris Callison-Burch, and Douglas Eck. 2019. Automatic detection of generated text is easiest when humans are fooled. *arXiv preprint arXiv:1911.00650*.
- <span id="page-9-5"></span>Ganesh Jawahar, Muhammad Abdul-Mageed, and Laks VS Lakshmanan. 2020. Automatic detection of machine generated text: A critical survey. *arXiv preprint arXiv:2011.01314*.
- <span id="page-9-7"></span>John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, and Tom Goldstein. 2023. A watermark for large language models. *arXiv preprint arXiv:2301.10226*.
- <span id="page-9-18"></span>Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, and Mohit Iyyer. 2023. Paraphrasing evades detectors of ai-generated text, but retrieval is an effective defense. *arXiv preprint arXiv:2303.13408*.
- <span id="page-9-13"></span>Thomas Lavergne, Tanguy Urvoy, and François Yvon. 2008. Detecting fake content with relative entropy scoring. *PAN*, 8:27–31.
- <span id="page-9-11"></span>Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. Roberta: A robustly optimized bert pretraining approach. *arXiv preprint arXiv:1907.11692*.
- <span id="page-9-6"></span>Eric Mitchell, Yoonho Lee, Alexander Khazatsky, Christopher D Manning, and Chelsea Finn. 2023. Detectgpt: Zero-shot machine-generated text detection using probability curvature. *arXiv preprint arXiv:2301.11305*.
- <span id="page-9-16"></span>Shashi Narayan, Shay B Cohen, and Mirella Lapata. 2018. Don't give me the details, just the summary! topic-aware convolutional neural networks for extreme summarization. *arXiv preprint arXiv:1808.08745*.
- <span id="page-9-0"></span>OpenAI. 2022. *gpt: Optimizing language models for dialogue. http://web.archive.org/web/ 20230109000707/https://openai.com/ blog/chatgpt/.*
- <span id="page-9-19"></span>Artidoro Pagnoni, Martin Graciarena, and Yulia Tsvetkov. 2022. Threat scenarios and best practices to detect neural fake news. In *Proceedings of the 29th International Conference on Computational Linguistics*, pages 1233–1249.

- <span id="page-10-12"></span>Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language models are unsupervised multitask learners. *OpenAI blog*, 1(8):9.
- <span id="page-10-10"></span>Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. 2016. Squad: 100,000+ questions for machine comprehension of text. *arXiv preprint arXiv:1606.05250*.
- <span id="page-10-11"></span>Alexander Ratner, Stephen H Bach, Henry Ehrenberg, Jason Fries, Sen Wu, and Christopher Ré. 2017. Snorkel: Rapid training data creation with weak supervision. In *Proceedings of the VLDB Endowment. International Conference on Very Large Data Bases*, volume 11, page 269. NIH Public Access.
- <span id="page-10-2"></span>Joshua Robinson, Christopher Michael Rytting, and David Wingate. 2022. Leveraging large language models for multiple choice question answering. *arXiv preprint arXiv:2210.12353*.
- <span id="page-10-4"></span>Kalhan Rosenblatt. 2023. Chatgpt passes mba exam given by a wharton professor. *Retrieved Jan*, 25:2023.
- <span id="page-10-8"></span>Vinu Sankar Sadasivan, Aounon Kumar, Sriram Balasubramanian, Wenxiao Wang, and Soheil Feizi. 2023. Can ai-generated text be reliably detected? *arXiv preprint arXiv:2303.11156*.
- <span id="page-10-1"></span>Teven Le Scao, Angela Fan, Christopher Akiki, Ellie Pavlick, Suzana Ilic, Daniel Hesslow, Roman ´ Castagné, Alexandra Sasha Luccioni, François Yvon, Matthias Gallé, et al. 2022. Bloom: A 176bparameter open-access multilingual language model. *arXiv preprint arXiv:2211.05100*.
- <span id="page-10-7"></span>Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec Radford, Gretchen Krueger, Jong Wook Kim, Sarah Kreps, et al. 2019. Release strategies and the social impacts of language models. *arXiv preprint arXiv:1908.09203*.
- <span id="page-10-5"></span>Chris Stokel-Walker. 2022. Ai bot chatgpt writes smart essays-should academics worry? *Nature*.
- <span id="page-10-0"></span>Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023. Llama: Open and efficient foundation language models. *arXiv preprint arXiv:2302.13971*.
- <span id="page-10-9"></span>Adaku Uchendu, Thai Le, Kai Shu, and Dongwon Lee. 2020. Authorship attribution for neural text generation. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 8384–8395.
- <span id="page-10-14"></span>Ben Wang and Aran Komatsuzaki. 2021. GPT-J-6B: A 6 Billion Parameter Autoregressive Language Model. [https://github.com/](https://github.com/kingoflolz/mesh-transformer-jax) [kingoflolz/mesh-transformer-jax](https://github.com/kingoflolz/mesh-transformer-jax).

- <span id="page-10-3"></span>Ann Yuan, Andy Coenen, Emily Reif, and Daphne Ippolito. 2022. Wordcraft: story writing with large language models. In *27th International Conference on Intelligent User Interfaces*, pages 841–852.
- <span id="page-10-13"></span>Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke Zettlemoyer. 2022. [Opt: Open pre](http://arxiv.org/abs/2205.01068)[trained transformer language models.](http://arxiv.org/abs/2205.01068)
- <span id="page-10-6"></span>Xuandong Zhao, Yu-Xiang Wang, and Lei Li. 2023. Protecting language generation models via invisible watermarking. *arXiv preprint arXiv:2302.03162*.

## <span id="page-11-0"></span>A Experimental Details and Baselines

Details on Baselines. We mainly compare the proposed methods with zero-shots methods, which utilize the source model itself to extract distinguishable statistic features, including:

- Log Likelihood (log p) [\(Solaiman et al.,](#page-10-7) [2019\)](#page-10-7): This approach evaluates the average token-wise log probability of the text and classifies text with higher Log Likelihood to be machine generated.
- Rank [\(Gehrmann et al.,](#page-9-4) [2019\)](#page-9-4): This approach evaluates the average rank of each token of the text and classifies text with smaller average rank to be machine generated.
- Log Rank [\(Mitchell et al.,](#page-9-6) [2023\)](#page-9-6): Instead of using the Rank score directly, this approach evaluates the average Log Rank of each token of the text and classifies text with smaller average Log Rank to be machine generated.
- Entropy [\(Gehrmann et al.,](#page-9-4) [2019\)](#page-9-4): This approach is inspired by the hypothesis that machine generated texts are more likely to have over-confident (thus low entropy) predictive distributions. In practice, [\(Mitchell et al.,](#page-9-6) [2023\)](#page-9-6) discovered that entropy to be positively correlated with passage fakeness, therefore, following their convention, we use high average entropy as a signal of machine generated text.
- DetectGPT [\(Mitchell et al.,](#page-9-6) [2023\)](#page-9-6): DetectGPT is based on the hypothesis that when applying small perturbations to a passage x and produce the perturbed text x˜, the quantity log pθ(x) − log pθ(˜x) is relatively larger for machine generated samples than human written one. In practice, the performance of this approach depends heavily on the external perturbation function and the number of perturbations.

Details on LLMs used. We used 7 LLMs ranging from 1.5B parameters to 20B parameters in our main experiments.

- GPT2-xl [\(Radford et al.,](#page-10-12) [2019\)](#page-10-12) is the 1.5B parameter version of GPT2 trained on a dataset of 8 million web pages called WebText [\(Radford et al.,](#page-10-12) [2019\)](#page-10-12), whose objective is to predict the next word given previous words within the text. GPT2-xl surpasses many other language models trained on specific domain (such as books, news, Wikipedia) without using domain-specific training dataset.
- GPT-Neo-2.7B [\(Black et al.,](#page-9-21) [2021\)](#page-9-21) was trained as an autoregressive language model on Pile [\(Gao](#page-9-22) [et al.,](#page-9-22) [2020\)](#page-9-22) dataset with EleutherAI's replication of the GPT-3 architecture.
- OPT-2.7B and OPT-13B are two models among a collection of decoder-only pre-trained transformers introduced in [\(Zhang et al.,](#page-10-13) [2022\)](#page-10-13), with the performance roughly match GPT-3 of the same size.
- GPT-j-6B [\(Wang and Komatsuzaki,](#page-10-14) [2021\)](#page-10-14), which was also trained on Pile [\(Gao et al.,](#page-9-22) [2020\)](#page-9-22), exhibits zero-shot performance roughly comparable to GPT-3 of comparable size. In addition, the performance gap from GPT-3 of similar size is closer than the GPT-Neo models.
- Llama-13b is the 13B parameter model from Llama models [\(Touvron et al.,](#page-10-0) [2023\)](#page-10-0): a collection of models ranging from 7B to 65B parameters trained with publicly available dataset. Llama-13B outperforms GPT-3 (175B) on most benchmarks, and all the models are released to the research community.
- NeoX-20B [\(Black et al.,](#page-9-23) [2022\)](#page-9-23) is a 20B autoregressive model trained on Pile, whose weights have been released openly to the public.

Experimental Details. For small models such as GPT2-xl, Neo-2.7, OPT-2.7, GPT-j, we use 1 NVIDIA A100 GPU (with total memory 40G) in our experiments; for larger models such as OPT-13b and Llama-13, we use 3 A100 GPUs (total memory 120 G) while using 4 A100 GPUs (total memory 160 G) for the largest model NeoX-20.

<span id="page-12-2"></span>

|       |                       | GPT2-xl Neo-2.7 |       | OPT-2.7 GPT-j |       | OPT-13 | Llama-13 NeoX |       | Avg.  |
|-------|-----------------------|-----------------|-------|---------------|-------|--------|---------------|-------|-------|
| XSum  | roberta-base          | 97.57           | 96.82 | 94.86         | 90.37 | 88.62  | 79.18         | 88.96 | 90.91 |
|       | roberta-large         | 99.74           | 99.73 | 98.37         | 97.58 | 93.85  | 85.93         | 95.13 | 95.76 |
|       | roberta-base          | 97.65           | 94.42 | 92.56         | 87.57 | 88.96  | 76.98         | 84.37 | 88.93 |
| SQuAD | roberta-large         | 99.01           | 98.30 | 96.53         | 93.31 | 91.62  | 82.59         | 88.37 | 92.82 |
|       | WritingP roberta-base | 96.88           | 95.23 | 89.57         | 93.26 | 86.18  | 83.49         | 88.92 | 90.50 |
|       | roberta-large         | 98.75           | 98.80 | 94.98         | 97.11 | 88.75  | 88.32         | 93.72 | 94.35 |

Table 6: Complete results for the supervised methods (AUROC score).

<span id="page-12-3"></span>

|       |                       |         |         | top-k |                  | top-p |         |       |          |  |
|-------|-----------------------|---------|---------|-------|------------------|-------|---------|-------|----------|--|
|       |                       | Neo-2.7 | OPT-2.7 | GPT-j | Llama-13 Neo-2.7 |       | OPT-2.7 | GPT-j | Llama-13 |  |
|       | roberta-base          | 96.48   | 94.15   | 92.72 | 82.47            | 98.30 | 97.30   | 96.71 | 85.84    |  |
| XSum  | roberta-large 99.74   |         | 98.06   | 98.29 | 87.33            | 99.84 | 98.97   | 98.82 | 89.35    |  |
|       | roberta-base          | 93.55   | 93.27   | 87.60 | 76.79            | 96.34 | 97.65   | 92.26 | 84.05    |  |
| SQuAD | roberta-large 98.35   |         | 96.88   | 93.97 | 82.42            | 98.21 | 98.39   | 95.09 | 86.46    |  |
|       | WritingP roberta-base | 97.27   | 90.14   | 93.86 | 83.24            | 98.33 | 94.09   | 96.55 | 88.78    |  |
|       | roberta-large 99.34   |         | 96.34   | 97.12 | 87.05            | 99.68 | 96.06   | 97.94 | 89.59    |  |

Table 7: Complete results for the supervised methods using top-k (k = 40) and top-p (p = 0.96) sampling across four models (AUROC scores).

## <span id="page-12-0"></span>B Supervised Methods

Main results for supervised methods. Comparing Table [1](#page-4-0) with Table [6,](#page-12-2) we found that, on average, our best zero shot method (either LRR on SQuAD dataset or NPR on XSum and WritingPrompts dataset) can exceed supervised model fine-tuned on roberta-base. For larger model roberta-large, only on writing dataset, perturbation-based method DetectGPT and NPR outperforms roberta-large model, by a margin of 0.55% and 2.87% respectively.

Supervised Method with Different Decoding Strategy. We experimented the 4 models used in zeroshot methods with top-p and top-k decoding strategy for supervised method and found that using top-p decoding strategy performs better than using top-k. (See Table [7\)](#page-12-3). Compared to zero-shot methods, the best zero-shot method NPR can outperform roberta-base model while being comparable to roberta-large model.

Supervised Method with Different Temperature. Supervised methods also perform better with lower temperature, but zero-shot methods such as Log Rank and Log Likelihood methods might exceed supervised methods in low temperature. Moreover, we found that the performance gap of roberta-base and roberta-large would be narrowed with lower temperature. The results are illustrated in Figure [5.](#page-13-1)

## <span id="page-12-1"></span>C Comparing NPR and DetectGPT

Different Number of Perturbations. The results for models smaller than or equal to 13B parameters are shown in Figure [6.](#page-14-0) For NeoX-20b model, we don't have enough computation resources to perform 100 perturbations, so we show it separately in Figure [7](#page-14-1) with 1, 10, 20, and 50 perturbations. For XSum dataset, NPR and DetectGPT almost coverages with 100 perturbations, but for SQuAD and WritingPrompts dataset, NPR still outperforms DetectGPT even with 100 perturbations. For SQuAD dataset with Llama-13b model, DetectGPT exhibits abnormality while NPR maintains stably improved performance as the number of perturbations increases. In addition, in nearly all the dataset and models, NPR outperforms DetectGPT except GPT-j on XSum dataset, demonstrating the effectiveness of NPR compared to DetectGPT.

<span id="page-13-1"></span>![](_page_13_Figure_0.jpeg)

Figure 5: Comparing supervised methods with different temperature (AUROC score).

Using T5-large as Perturbation Function. We illustrate the performance of NPR and DetectGPT in Figure 8 with different combination of dataset and LLMs using T5-large as perturbation function. Compared to T5-3b illustrated in Figure 6, the superiority of NPR over DetectGPT becomes more distinct with T5-large being the perturbation function, where in almost all the LLMs, datasets and different number of perturbations (except with Llama-13b on SQuAD), NPR outperforms DetectGPT by a large margin. In addition, we could also observe that NPR achieves comparable or even better result with only 10 perturbations to that of DetectGPT with 100 perturbations, which indicates that NPR is more efficient and can achieve similar level of performance with significantly fewer number of perturbations.

#### <span id="page-13-0"></span>**D** Alternative Sampling Strategies and Temperature

**Different Sampling Strategy.** In Table 8, we illustrate the complete results with different zero-shot methods with four LLMs using top-p and top-k sampling. For perturbation based methods, even with different sampling strategy, NPR provides clearer signal for machine generated text detection than DetectGPT. Moreover, we find that although LRR is more stable than Log Rank and Log Likelihood methods: when replacing temperature sampling to top-p and top-k sampling, all the above-mentioned three zero-shot methods' performance improve, however, LRR improves approximately the same for both

<span id="page-14-0"></span>![](_page_14_Figure_0.jpeg)

Figure 6: Comparing DetectGPT and NPR (AUROC score).

<span id="page-14-1"></span>![](_page_14_Figure_2.jpeg)

Figure 7: Comparing DetectGPT and NPR on NeoX-20b (AUROC score).

top-k and top-p sampling while the other two is more in favor of top-p sampling.

**Different Temperature.** Here, we investigate how temperature used for machine generated texts affects detection accuracy of different zero-shot methods. From Figure 9, we find that, all the perturbation-free zero-shot methods improved their performance with the decreasing temperature. In particular, for Log Rank and Log Likelihood method, the performance can become extremely high when the temperature drops, even exceeding NPR and achieving approximately 100 points detection accuracy. For example, in Neo-2.7 and OPT-13 with temperature 0.5,  $\log p$  method and Log Rank method achieves an accuracy of 100 points on WritingPrompts dataset, this prevalent performance can be observed notably in smaller models with relatively high temperature (such as GPT2-xl and Neo-2.7 with high temperature such as 0.7) or in large models with relatively lower temperature such as OPT-13 with temperature 0.5 as we demonstrated in Figure 9. Though we omit entropy method because it gets an accuracy worse than random guessing, one of the observation from our experiments is that, using the assumption "machine generated text has higher entropy" suggested in (Mitchell et al., 2023), the performance of entropy method improve with the increasing temperature with absolute accuracy smaller than 50 points, which suggests that for low temperature, we should use the assumption "machine generated text has lower entropy" for detection machine generated text. In general, Entropy method performs worse than random and is not an implementable detection method.

For perturbation based methods (Figure 10), while DetectGPT does not exhibit a clear trend with respect to temperature, the performance of NPR improves with the decreasing temperature most of the time. However, this trend is not as clearly as Log Rank and log likelihood method, especially when the temperature becomes too low. This behavior suggests that perturbation based method is more suitable for high temperature, while perturbation-free method is more suitable for low temperature.

<span id="page-15-0"></span>

|          |                     | top-p            |         |                        |       |                  |       |               |       |          |
|----------|---------------------|------------------|---------|------------------------|-------|------------------|-------|---------------|-------|----------|
| Dataset  | Perturbation Method |                  | Neo-2.7 | top-k<br>OPT-2.7 GPT-j |       | Llama-13 Neo-2.7 |       | OPT-2.7 GPT-j |       | Llama-13 |
|          |                     | log<br>p         | 91.27   | 90.19                  | 85.95 | 59.14            | 95.52 | 93.27         | 91.13 | 67.86    |
|          |                     | Rank             | 78.79   | 76.75                  | 77.25 | 49.94            | 78.58 | 76.89         | 77.18 | 50.77    |
|          | w/o                 | Log Rank         | 94.20   | 92.30                  | 89.18 | 65.09            | 96.71 | 93.93         | 92.53 | 71.44    |
| XSum     |                     | Entropy          | 53.07   | 47.80                  | 53.23 | 67.76            | 49.05 | 46.41         | 52.16 | 67.94    |
|          |                     | LRR (ours) 95.50 |         | 92.35                  | 91.14 | 77.99            | 95.64 | 90.68         | 91.14 | 75.72    |
|          |                     | DetectGPT 98.94  |         | 96.63                  | 96.56 | 73.22            | 98.82 | 97.72         | 96.58 | 77.82    |
|          | w/                  | NPR (ours) 99.61 |         | 98.23                  | 96.41 | 77.48            | 99.27 | 98.40         | 97.35 | 78.67    |
|          | w/o                 | log<br>p         | 87.85   | 91.00                  | 81.32 | 45.06            | 91.20 | 94.24         | 86.69 | 56.16    |
|          |                     | Rank             | 80.10   | 82.14                  | 79.81 | 55.21            | 80.56 | 82.40         | 80.28 | 56.89    |
|          |                     | Log Rank         | 92.58   | 94.40                  | 86.94 | 51.21            | 94.48 | 96.37         | 90.44 | 60.66    |
| SQuAD    |                     | Entropy          | 54.62   | 50.83                  | 56.89 | 69.52            | 54.51 | 50.01         | 55.67 | 63.26    |
|          |                     | LRR (ours) 97.79 |         | 97.58                  | 94.55 | 72.52            | 97.48 | 98.11         | 94.38 | 74.38    |
|          |                     | DetectGPT 97.04  |         | 97.53                  | 87.59 | 47.52            | 97.50 | 97.48         | 88.90 | 52.06    |
|          | w/                  | NPR (ours) 98.56 |         | 99.35                  | 91.21 | 50.83            | 98.32 | 99.18         | 92.99 | 54.28    |
|          |                     | log<br>p         | 96.62   | 95.99                  | 95.67 | 86.93            | 98.16 | 98.10         | 97.11 | 92.68    |
|          |                     | Rank             | 82.67   | 83.96                  | 83.49 | 78.49            | 82.89 | 84.45         | 83.55 | 79.01    |
|          | w/o                 | Log Rank         | 97.90   | 97.23                  | 97.20 | 90.57            | 98.73 | 98.60         | 97.89 | 94.56    |
| WritingP |                     | Entropy          | 32.37   | 38.22                  | 34.37 | 44.09            | 27.08 | 36.77         | 32.82 | 39.03    |
|          |                     | LRR (ours) 98.58 |         | 97.97                  | 98.06 | 93.80            | 98.46 | 97.97         | 97.76 | 94.79    |
|          |                     | DetectGPT 99.05  |         | 98.65                  | 96.05 | 81.83            | 98.80 | 98.62         | 96.67 | 82.70    |
|          | w/                  | NPR (ours) 99.58 |         | 99.46                  | 98.27 | 87.99            | 99.36 | 99.04         | 97.85 | 89.96    |

Table 8: Complete result for the zero-shot methods using top-k and top-p sampling across four models (AUROC score).

<span id="page-16-0"></span>![](_page_16_Figure_0.jpeg)

Figure 8: Comparing DetectGPT and NPR using t5-large (AUROC score).

<span id="page-16-1"></span>

| Perturbation Method |            | GPT2-x1 | Neo-2.7 | OPT-2.7 | GPT-j | OPT-13 | Llama-13 | NeoX  |
|---------------------|------------|---------|---------|---------|-------|--------|----------|-------|
|                     | $\log p$   | 0.06    | 0.09    | 0.10    | 0.04  | 0.07   | 0.07     | 0.60  |
|                     | Rank       | 0.07    | 0.10    | 0.09    | 0.04  | 0.05   | 0.07     | 0.60  |
| w/o                 | Log Rank   | 0.06    | 0.09    | 0.10    | 0.04  | 0.05   | 0.06     | 0.60  |
|                     | Entropy    | 0.06    | 0.09    | 0.09    | 0.04  | 0.05   | 0.06     | 0.60  |
|                     | LRR (ours) | 0.12    | 0.19    | 0.18    | 0.08  | 0.10   | 0.14     | 1.20  |
| w/                  | DetectGPT  | 8.07    | 9.60    | 9.80    | 7.03  | 7.98   | 8.14     | 35.56 |
|                     | NPR (ours) | 8.15    | 9.69    | 9.90    | 7.12  | 7.83   | 7.98     | 35.67 |

Table 9: Computational time (seconds) for different zero-shot methods on different LLMs (averaged over 10 reruns).

#### <span id="page-16-2"></span>**E** Computational Time

The estimated computational time of different zero-shot methods is illustrated in Table 9. The time is estimated over the average of 10 samples. For perturbation based methods, since the time depends on the perturbation function and the number of perturbation, we used T5-3b as perturbation function and use 50 perturbations since this is the setting used for the main results in Table 1, we want to provide an idea of how much more it costs for perturbation based method to achieve exceptional performance in Table 1.

<span id="page-17-0"></span>![](_page_17_Figure_0.jpeg)

Figure 9: Comparison of perturbation-free methods using different temperature (AUROC score).

<span id="page-18-0"></span>![](_page_18_Figure_0.jpeg)

Figure 10: Comparison of perturbation methods using different temperature (AUROC score).