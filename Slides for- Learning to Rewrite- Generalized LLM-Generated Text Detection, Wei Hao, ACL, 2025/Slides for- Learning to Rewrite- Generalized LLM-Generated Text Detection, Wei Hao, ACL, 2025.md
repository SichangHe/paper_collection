![](_page_0_Picture_0.jpeg)

![](_page_0_Picture_1.jpeg)

![](_page_0_Picture_2.jpeg)

# **Learning to Rewrite (L2R): Generalized LLM-Generated Text Detection**

**Wei Hao1\* , Ran Li1\* , Weiliang Zhao1 , Junfeng Yang1 , Chengzhi Mao2** 

**Columbia University1 Rutgers University2 Equal Contribution\***

### **LLM-Generated Texts Are Abused**

**A potential indicator of malicious activity**

### **LLM-Generated Texts Are Abused**

#### **A potential indicator of malicious activity**

• **Bad Academic Practice: 10%** of peer-reviews from a prestigious ML conference are LLM-generated (Liang et al. 2024)

![](_page_2_Picture_3.jpeg)

Figure 1. Lazy academic practice due to time constraints

### **LLM-Generated Texts Are Abused**

#### **A potential indicator of malicious activity**

• **Cyberattack:** Partnered with Barracuda Networks, we found that in Apr 2025, **>= 51%** (Spam) and **14%** (Phishing) attacks in real-world customers' inboxes were LLM-generated (Hao et al. 2025).

![](_page_3_Figure_3.jpeg)

![](_page_3_Picture_5.jpeg)

"Do Spammers Dream of Electric Sheep? Characterizing the Prevalence of LLM-Generated Malicious Emails", To appear in ACM IMC '25.

Figure 2. Study on AI-powered cybercrime by Forbes News

### **Various Detectors Have Been Proposed**

**Many require training a classification model**

### **Various Detectors Have Been Proposed**

#### **Many require training a classification model**

- Solaiman et al. (2019) trains a RoBERTa (or any LLM) and uses its logits for classification. (**Logits**)
- Verma et al. (2024) trains a model on the log probability output by an LLM, in addition to the unigram and bigram probability calculated on the input. (**Ghostbuster)**

### **Various Detectors Have Been Proposed**

#### **Many require training a classification model**

- Solaiman et al. (2019) trains a RoBERTa (or any LLM) and uses its logits for classification. (**Logits**)
- Verma et al. (2024) trains a model on the log probability output by an LLM, in addition to the unigram and bigram probability calculated on the input. (**Ghostbuster)**

| Method / Domians  | In-Distribution | Out-of-Distribution |
|-------------------|-----------------|---------------------|
| Logits (Llama-8b) | 0.98            | 0.14                |
| Ghostbuster       | 0.71            | 0.39                |

Overfits

Table 1. ID and OOD performance measured in AUROC scores. Delta of 0.32~0.84 indicates overfitting on the training domain.

### **Some Mitigations Have Been Proposed**

**Leverage domain-agnostic features**

## **Some Mitigations Have Been Proposed**

#### **Leverage domain-agnostic features**

• Mao et al. (2024) oberves that LLMs are reluctant to edit their own outputs. They then train a model on the edit distance between rewrite and the original input for classification. (**RAIDAR)**

![](_page_8_Figure_3.jpeg)

Figure 3. Rewrite on the LLM-generated text produces less edits, compared with rewrite on Human text.

## **Some Mitigations Have Been Proposed**

#### **Leverage domain-agnostic features**

• Mao et al. (2024) oberves that LLMs are reluctant to edit their own outputs. They then train a model on the edit distance between rewrite and the original input for classification. (**RAIDAR)**

![](_page_9_Figure_3.jpeg)

Figure 3. Rewrite on the LLM-generated text produces less edits, compared with rewrite on Human text.

AUROC ID: 0.80 - OOD: 0.69 (Not good enough)

### **Key Problem**

**Text Distributions Highly Vary across Domains**

### **Key Problem**

#### **Text Distributions Highly Vary across Domains**

- Caually written domains (e.g. product review) leave more room for rewrite for both human and LLM texts
- Formally written domains (e.g.environmental report) leave small room even for human

![](_page_11_Figure_4.jpeg)

Figure 4. Distributions of similarity scores of rewrites on LLM/Human input across different domains, can't use one threshold to separate.

### **Training on Highly Varying Rewrites Is Suboptimal**

**Need to produce even more/less rewrite on human/LLM input**

### **Training on Highly Varying Rewrites Is Suboptimal**

#### **Need to produce even more/less rewrite on human/LLM input**

• We need to reinforce the exsiting rewrite reluctance by l**earning to rewrite**

![](_page_13_Figure_3.jpeg)

Figure 5. With L2R, the previously diverse similarity thresholds become the same across domains.

**Step 1: Defining the training objective**

#### **Step 1: Defining the training objective**

• The edit distance is quantified by the negation of Levenshtein score (1996) among two strings, a larger distance denotes lower similarity:

$$D(x,F(x)) = 1 - \frac{\text{Levenshtein}(x,F(x))}{\max(len(x),len(F(x)))}$$
  $F(.)$  is the rewriting LLM, and  $F(x)$  is the rewritten text.

• Given some human text , our objective becomes: *xh* <sup>∈</sup> *Xh* and LLM text *xllm* <sup>∈</sup> *Xllm*

$$\max[D(x_h, F(x_h)) - D(x_{llm}, F(x_{llm}))]$$

#### **Step 1: Defining the training objective**

• The edit distance is quantified by the negation of Levenshtein score (1996) among two strings, a larger distance denotes lower similarity:

$$D(x,F(x)) = 1 - \frac{\text{Levenshtein}(x,F(x))}{\max(len(x),len(F(x)))}$$
  $F(.)$  is the rewriting LLM, and  $F(x)$  is the rewritten text.

• Given some human text , our objective becomes: *xh* <sup>∈</sup> *Xh* and LLM text *xllm* <sup>∈</sup> *Xllm*

$$\max[D(x_h, F(x_h)) - D(x_{llm}, F(x_{llm}))]$$

• We use the **cross-entropy loss** *L(·)* assigned to the input *x* by *F(·)* as a proxy to the edit distance (non-differentiable), and our objective becomes:

$$\min\{L(x_{\text{train}}) \cdot y_{\text{train}}\}, \quad y_{\text{train}} = \begin{cases} 1 & \text{(LLM)} \\ -1 & \text{(human)} \end{cases}$$

#### **Step 2: Loss calibration/thresholding before and during training**

• We observe that a vanilla optimization suffers from corrupted rewrites, where the rewrite becomes verbose for both LLM and Human text, with a more severe degree on Human text.

![](_page_17_Figure_3.jpeg)

Figure 4. Training loss curves for the rewrite model with and without the loss calibration.

#### **Step 2: Loss calibration/thresholding before and during training**

• We observe that a vanilla optimization suffers from corrupted rewrites, where the rewrite becomes verbose for both LLM and Human text, with a more severe degree on Human text.

![](_page_18_Figure_3.jpeg)

Figure 4. Training loss curves for the rewrite model with and without the loss calibration.

**Test the baselines and L2R under ID/OOD/Adversarial attacks**

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

• ID data: 21 source domains (e.g. Code, Legal Record), 4 LLMs (i.e. GPT-4o, Llama-3-70B, Gemini 1.5 Pro), 200 prompts

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

- ID data: 21 source domains (e.g. Code, Legal Record), 4 LLMs (i.e. GPT-4o, Llama-3-70B, Gemini 1.5 Pro), 200 prompts
- OOD data: 5 source domains (e.g. WikiHow and Reddit ELI5), 5 LLMs (i.e. BLOOMz, ChatGPT, Davinci), 2-8 prompts

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

- ID data: 21 source domains (e.g. Code, Legal Record), 4 LLMs (i.e. GPT-4o, Llama-3-70B, Gemini 1.5 Pro), 200 prompts
- OOD data: 5 source domains (e.g. WikiHow and Reddit ELI5), 5 LLMs (i.e. BLOOMz, ChatGPT, Davinci), 2-8 prompts
- Adversarial Attacks: Rewrite and Decoherence attack, s.t the LLM-generated input is designed to produce more rewrites, thus bypassing the detector

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

![](_page_23_Figure_2.jpeg)

**Logits** uses the same amount of learnable parameters as **L2R**, just with different training objectives

Figure 5. L2R Performance measured in AUROC scores.

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

![](_page_24_Figure_2.jpeg)

**Logits** uses the same amount of learnable parameters as **L2R**, just with different training objectives

Figure 5. L2R Performance measured in AUROC scores.

• L2R achieves the best generalizability, with second highest ID AUROC.

#### **Test the baselines and L2R under ID/OOD/Adversarial attacks**

![](_page_25_Figure_2.jpeg)

**Logits** uses the same amount of learnable parameters as **L2R**, just with different training objectives

Figure 3. L2R Performance measured in AUROC scores.

• The number of learnable parameters provides trade-off between ID and OOD performance (see **Logits** and **L2R**). But L2R's ID performance is less affected due to its unique learning objective!

![](_page_26_Picture_0.jpeg)

![](_page_26_Picture_1.jpeg)

### **By Reinforcing The Right Training Objective, We Effectively Mitigate Overfitting and Train A Domain-Agnostic LLM-Generated Text Detector**

**mailto: wh2473@columbia.edu**