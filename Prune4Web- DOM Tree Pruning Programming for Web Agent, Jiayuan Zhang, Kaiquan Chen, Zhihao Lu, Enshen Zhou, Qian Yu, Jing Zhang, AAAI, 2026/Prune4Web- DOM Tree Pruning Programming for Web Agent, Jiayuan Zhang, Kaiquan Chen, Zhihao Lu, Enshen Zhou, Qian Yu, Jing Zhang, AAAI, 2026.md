# Prune4Web: DOM Tree Pruning Programming for Web Agent

## Jiayuan Zhang\*, Kaiquan Chen\*, Zhihao Lu, Enshen Zhou, Qian Yu, Jing Zhang<sup>†</sup>

School of Software & QRI, Beihang University, Beijing, China {zhangjiayuan42, zhang\_jing}@buaa.edu.cn

### Abstract

Web automation uses intelligent agents to perform high-level tasks by mimicking human interactions with webpages. Despite recent advances in LLM-based web agents, efficiently navigating complex, real-world webpages remains challenging due to massive DOM structures (10,000~100,000 tokens). Current approaches either truncate DOMs—losing vital information-or use inefficient heuristics and separate ranking models, failing to balance precision and scalability. We introduce Prune4Web, a novel paradigm that transforms DOM processing from LLM-based filtering to programmatic pruning. Our key innovation is DOM Tree Pruning Programming, where an LLM generates executable Python scoring programs to dynamically filter DOM elements based on semantic clues from decomposed sub-tasks. This approach eliminates the need for LLMs to process full DOMs, instead delegating traversal and scoring to lightweight, interpretable programs. The result is a 25~50 times reduction in candidate elements for grounding, enabling precise action localization without attention dilution. Additionally, we propose a data annotation method and a two-turn dialogue training strategy that jointly optimizes Planner, Programmatic Filter, and Grounder in a unified framework. Experiments demonstrate state-of-the-art performance. On our low-level task grounding task, our approach dramatically increases grounding accuracy from 46.8% to 88.28%, highlighting its effectiveness.

## 1 Introduction

Web automation enables the completion of high-level tasks, such as booking flights or shopping online, through intelligent agents that mimic human interaction on webpages. These agents achieve this by interpreting high-level tasks, breaking them down into low-level sub-tasks, and seamlessly interacting with web elements. Recently, large language models (LLMs) have demonstrated impressive capabilities in autonomous web navigation through their strong reasoning and decision-making abilities (Yao et al. 2022; Deng et al. 2023a). Current web agents approaches fall into three main categories: 1) Textual HTML/DOM-based (Yao et al. 2022; Song et al. 2025), 2) Visual Screenshotbased (Lin et al. 2024; Cheng et al. 2024a), and 3) Multimodal-based (He et al. 2024a; Zheng et al. 2024a). Visual

![](_page_0_Figure_10.jpeg)

Figure 1: Comparison between existing multi-modal web agents and our Prune4Web paradim. Compared to existing multi-modal web agent paradigms, we propose a programmatic pruning strategy that efficiently removes redundant DOM elements. Our Prune4Web approach relaxes the token limits of LLMs and increases accuracy on low-level sub-task grounding from 46.80% to 88.28%.

screenshots provide an intuitive, human-like understanding of webpage state, making them effective for reasoning about low-level sub-tasks. However, they contain limited semantic information, especially for special icons, and are sensitive to variations in resolution and overlapping elements. In contrast, HTML/DOMs offer precise and stable semantic and structural information that enables accurate element selection with minimal ambiguity.

In this paper, we leverage the complementary advantages of text and visual multi-modal information and design a multi-stage framework: A **planner** model takes the high-level task (e.g., "Book a flight to New York") and a **screenshot**, then decomposes it into a low-level sub-task (e.g., "Find the destination field and Type NYC"). Based on the sub-task, an **action grounder** model processes the **DOMs** to precisely localize and execute the required operations (e.g., selecting <input id="destination">to type "NYC"). However, modern webpage DOMs typically contain 10,000–100,000 tokens—far exceeding the context ca-

<sup>\*</sup>These authors contributed equally.

<sup>&</sup>lt;sup>†</sup>Corresponding author: Jing Zhang

pacity of most LLMs. This results in token truncation and attention dilution, leading to critical information loss and significant processing delays (Gou et al. 2024a; Deng et al. 2023a). Existing HTML pruning methods fall short, either relying on overly simplistic heuristic filtering (He et al. 2024a; Pan et al. 2024) or requiring separate language models for element-ranking (Deng et al. 2023a). Neither approach effectively addresses the core issue. The fundamental challenge remains: *how to efficiently and accurately navigate task-relevant elements from complete DOM structures.*

To this end, we propose a Prune4Web pipeline through a novel paradigm: DOM Tree Pruning Programming. We observe that the low-level sub-tasks (e.g.,"Find the destination field") output by the planner contain extensive semantic clues about potentially relevant DOM elements. This insight motivates us to shift the LLM's role from directly locating elements in lengthy DOMs to generating a locator program based solely on the low-level sub-tasks, thereby avoiding the need to feed long DOM sources into the LLMs (Jiang et al. 2024a; Zhang et al. 2023b). Specifically, we implement this concept through our Programmatic Element Filter model. This filter receives a specific low-level sub-task from the upstream Planner and prompts the LLM to generate a concise, task-specific Python *scoring program*. We design a heuristic-based scoring program template, requiring the LLM to generate only key parameters for better controllability and flexibility. The generated program runs independently outside the LLM, efficiently traversing the complete DOM tree to score and rank all elements. This approach reduces candidate elements by 25∼50 times, enabling precise action localization without attention dilution. A downstream LLM-based Action Grounder then selects the final element from this refined shortlist, completing the grounding task.

To train the models within Prune4Web, we create an automated data synthesis pipeline that annotates structured intermediate outputs from raw data with minimal human intervention. These include low-level sub-tasks for the Planner and key parameters for the Programmatic Element Filter. For optimization, we develop a novel two-turn dialogue training strategy that jointly trains the Planner, Filter, and Grounder as a unified model. We initially use Supervised Fine-Tuning (SFT) with our annotated data to train a base model (Zheng et al. 2024b). Subsequently, we apply Reinforcement Fine-Tuning (RFT) to enhance the Planner's long-term planning capabilities while integrating the programmatic filtering process into this optimization framework. Extensive experiments on benchmark datasets (Deng et al. 2023a; Pan et al. 2024) demonstrate the effectiveness of the proposed Prune4Web. Notably, on our low-level sub-task grounding benchmark, our approach greatly boosts grounding accuracy from 46.8% to 88.28%, showing its core advantage. Our contributions are summarized as follows:

- We design a multimodal web agent framework that seamlessly combines the intuitive reasoning of visual inputs with the semantic precision of HTML/DOM.
- We introduce Prune4Web with a Programmatic Element Filter that generates task-specific Python scoring programs to efficiently filter and rank elements to address

- the DOM scalability bottleneck.
- We present a data annotation method and a two-turn dialogue training strategy that jointly optimize the planner, filter, and grounder. We use SFT and RFT to enhance planning and programmatic filtering. Strong empirical evidence validates our method on standard benchmarks.

# 2 Related Work

Multimodal-based Web Agents. To achieve higher precision in web interaction, directly processing HTML source code has recently become a significant research direction for LLM-based agents (Lai et al. 2024; Song et al. 2025), leading to notable advancements. Researchers have leveraged the rich semantic and structural information within the DOM by developing multimodal fusion techniques (Zheng et al. 2024a; Furuta et al. 2023) or more powerful endto-end models (Lin et al. 2024; Cheng et al. 2024; Hong et al. 2024; Xu et al. 2025) for precise element localization and operation. However, these efforts toward precision inevitably face the challenge of information overload (Gou et al. 2024a; Deng et al. 2023a; Xue et al. 2025). Modern webpage HTML sources typically contain vast amounts of irrelevant information. Feeding this directly into an LLM wastes computational resources and dilutes the model's focus across lengthy context (Gur et al. 2023). Balancing HTML's precision with efficient information processing remains a critical, unsolved challenge.

DOM Tree Pruning Strategies. DOM tree pruning is a key technique for addressing information overload challenge. Existing methods fall into two categories. The first is rulebased filtering, which relies on fixed heuristics like converting the DOM to a simplified accessibility tree (He et al. 2024a; Zhou et al. 2023). The second is LLM-based ranking, where the model is prompted to score and select from a large number of element candidates (Deng et al. 2023a; Lu,` Kasner, and Reddy 2024; Kerboua et al. 2025). Rule-based approaches are too rigid and generalize poorly. LLM-based ranking fails to reduce the burden of processing long contexts. In contrast, our work introduces DOM Tree Pruning Programming, a new paradigm that addresses both limitations by having the LLM generate a lightweight locator program (Qiao et al. 2024; Jiang et al. 2024b).

Programmatic Thinking for Agents. Our method is rooted in programmatic thinking—a paradigm that enhances LLM abilities by prompting them to generate intermediate code or plans to solve complex problems. This approach has shown effective for general reasoning and planning (Jiang et al. 2024a; Zhang et al. 2023b; Wei et al. 2022; Gupta and Kembhavi 2023; Zhou et al. 2025b; Qin et al. 2024). In the agent field, programmatic thinking typically generates high-level action sequences that control agent behavior on the web (Ma et al. 2023), mobile devices (Wen et al. 2024; Zhang et al. 2023a), or general computer operations (Zhang et al. 2024; Tan et al. 2024; Wu et al. 2024; Xie et al. 2025). Our work innovatively applies this paradigm to the lower-level problem of DOM filtering by generating an executable scoring function that actively reshapes the model's input.

Reinforcement Fine-Tuning for Agents. To enable agents

to learn complex policies beyond static datasets, Reinforcement Fine-Tuning (RFT) is increasingly used to optimize LLM agents for sequential decision-making in dynamic environments (Lu et al. 2025; Qi et al. 2024; Bai et al. 2025a; Guo et al. 2025). RFT allows agents to learn from outcomes via a reward mechanism, enabling them to master complex strategies. In Prune4Web, we not only employ RFT to optimize the Planner's capabilities but also innovatively use the success or failure of our DTPP process to provide rich intermediate reward signals (Zhou et al. 2025a), facilitating more efficient policy learning.

# 3 Method

# 3.1 Prune4Web Framework and Workflow

We introduce Prune4Web, a multi-stage framework for complex web automation tasks. The complete workflow is shown in Figure 2. The framework consists of three stages: task planning, element filtering, and action grounding.

Planning Stage. The workflow begins with the Planner model, which decomposes a high-level task T into low-level sub-tasks S<sup>t</sup> based on the current webpage screenshot Sc<sup>t</sup> and operational history Ht. This process is formally expressed as: S<sup>t</sup> = Planner(T, Sct, Ht). For example, given the high-level task "Book a flight to New York," the Planner might generate low-level sub-tasks like "Find the destination field" and "Type NYC", as well as current states. The Planner intentionally does not access the HTML source code, keeping its focus on high-level strategic decomposition.

Filtering Stage. If a low-level sub-task S<sup>t</sup> requires interaction with a specific element, the workflow proceeds to the filtering stage managed by the Programmatic Element Filter model. This model implements our core method, DOM Tree Pruning Programming, to generate a refined list of candidate elements C<sup>t</sup> from the complete HTML source code: C<sup>t</sup> = ProgrammaticElementFilter(St, HTMLt). The resulting list C<sup>t</sup> then serves as the sole input for the subsequent Action Grounder.

Action Grounding Stage. The Action Grounder completes the workflow by generating the final executable action At. It takes two inputs: the low-level sub-task S<sup>t</sup> from the Planner and the pruned candidate list C<sup>t</sup> from the Programmatic Element Filter. This is formally expressed as A<sup>t</sup> = ActionGrounder(St, [Ct]), where the brackets indicate that [Ct] is conditional. This is because [Ct] is only required for element-specific actions (e.g., 'click'), whereas abstract actions (e.g., 'task complete') are grounded directly from St. In summary, the Prune4Web framework offers a dual advantage. It uses the structured, precise information from the DOM to avoid the pitfalls of visual-based localization in complex scenarios. At the same time, its innovative filtering stage distills verbose HTML into a concise list of candidates. This effectively mitigates information overload and significantly reduces the difficulty and error rate of the grounding task for the Action Grounder.

# 3.2 DOM Tree Pruning Programming

DOM Tree Pruning Programming is the technical core of Prune4Web. It offloads the heavy task of element filtering from the LLM itself to a lightweight, dynamically generated program.

Step 1: Initial Rule-based Filtering. The process begins with a rule-based preliminary filtering of the raw HTMLt. The core principle is to retain elements with clear interactive features based on their tags (e.g., <a>, <button>, <input>) or 'role' attributes (e.g., 'checkbox'). For noninteractive elements, we extract key textual information (from 'text', 'aria-label', etc.) and attach it to the nearest interactive element as supplementary context. This step yields a pre-processed DOM tree containing only context-enriched interactive elements, serving as a more structured and less noisy initial candidate set.

Step 2: Scoring Function Generation. The core task of the Programmatic Element Filter is to generate a Python scoring function fscore <sup>t</sup> for the current step. We design a heuristic-based Scoring Function Template, where the LLM only needs to generate key parameters for this template. This approach significantly improves the stability and controllability of the generated code while maintaining flexibility. Algorithm 1 shows the pseudo-code of the template. The template mimics human intuition when searching for elements using keywords. It assumes that a target element contains identifiable textual features within the HTML. The template performs tiered, weighted matching across different attributes: Tier 1 includes visible 'text'; Tier 2 includes non-visible but high-semantic attributes like 'aria-label' and 'placeholder'; and Tier 3 includes other attributes like 'class' or 'id' that may contain semantic cues. The template also integrates multiple matching types (e.g., exact, substring, fuzzy) and assigns weights based on match quality. With this design, the Programmatic Element Filter simply generates a set of keywords and their corresponding base weights based on the low-level sub-task St, enabling multi-faceted relevance scoring for each element.

Step 3: Pruning Execution and Output Formatting. The generated scoring function fscore <sup>t</sup> is immediately executed to compute a score s for each element e in the pre-processed DOM tree. The system then selects the Top-N highestscoring elements, where N defaults to 20. The impact of varying N from 1 to 20 on pruning efficiency is visualized and analyzed in the Experiments section.

Discussion. The primary advantage of DOM Tree Pruning Programming lies in its combination of flexibility and structure. The LLM provides high-level, context-aware intelligence by generating keywords and weights, while the hardcoded function template ensures robust, efficient, and interpretable scoring and execution. By generating a lightweight function instead of directly processing lengthy raw HTML, this paradigm avoids attention dilution from long contexts and significantly reduces inference latency.

## 3.3 Data Synthesis

To effectively train our multi-stage architecture and rigorously evaluate DOM Tree Pruning Programming, we reconstructed and re-annotated the public Multimodal-Mind2Web (MM2W) dataset (Deng et al. 2023a). The original MM2W dataset contains only high-level tasks, per-step source code, and final target elements and actions, lacking the intermedi-

![](_page_3_Figure_0.jpeg)

Figure 2: The Prune4Web framework pipeline. (A) The input observations include high-level task, history, screenshot, and DOM tree. (B) The Planner generates low-level subtasks based on user instruction, history, and screenshot. (C) Guided by the plan, the Programmatic Element Filter produces a scoring program that is applied to the DOM tree elements to yield a pruned DOM tree. (D) This pruned DOM forms the refined input for the Action Grounder, which then selects an executable action.

ate reasoning steps our framework requires. To address this, we used GPT-4o (Hurst et al. 2024) as an annotation tool to add rich intermediate labels for each step. These labels include: (1) low-level sub-tasks for the Planner; (2) keywords and their weights for the Programmatic Element Filter; and (3) pruned DOM trees and thought processes for the Action Grounder. After annotation, we performed secondary cleaning and manual verification to ensure high data quality while strictly adhering to MM2W's original train/test splits. Using this annotated data, we constructed a new evaluation set that treats generated low-level sub-tasks as direct input to evaluate the grounding performance of subsequent models, directly validating the effectiveness of DOM Tree Pruning Programming. Our final dataset contains approximately 5,000 high-quality interaction steps, divided into training and test sets.

# 3.4 Training Strategy

Our training strategy involves two core stages: Supervised Fine-Tuning (SFT) and Reinforcement Fine-Tuning (RFT), both conducted on the Qwen2.5VL-3B-Instruct model.

Supervised Fine-Tuning (SFT). The goal of SFT is to teach the base model to perform three distinct roles: Planner, Programmatic Element Filter, and Action Grounder. We explored two SFT paradigms: Separate Models and Unified Model. In the Separate Models approach, we fine-tune three independent models, each specialized for one task. The Planner maps high-level tasks and screenshots to lowlevel sub-tasks. The Programmatic Element Filter maps lowlevel sub-tasks to scoring program parameters. The Action Grounder maps low-level sub-tasks and pruned lists to final actions. In the Unified Model approach, we designed an innovative two-turn dialogue template to optimize a single model. In the first turn, the model acts as both Planner and Programmatic Element Filter, generating the low-level subtask and scoring parameters simultaneously. In the second turn, after receiving the pruned list from the executed program, the model acts as the Action Grounder to output the final action. Experiments show the unified model is better suited for highly-coupled web automation tasks.

Reinforcement Fine-Tuning (RFT). As SFT is insufficient for teaching complex, long-horizon planning and task decomposition, we employ Group Relative Policy Optimization (GRPO) (Shao et al. 2024) for targeted RFT of the Planner (or the first turn of the unified model). We apply RFT selectively to the Planner because the Programmatic Element Filter and Action Grounder handle more deterministic tasks that can be effectively learned through SFT. The success of RFT depends on our Hierarchical Reward Mechanism, which provides timely feedback to the Planner based on downstream model performance. The Planner's reward Rtotal at each step combines format and accuracy components: Rtotal = Rformat + Rf iltering + Rgrounding. Here, Rformat ensures the generated low-level sub-task follows the correct format, Rf iltering provides critical intermediate feedback by verifying whether the Programmatic Element Filter's program successfully retains the ground-truth element in the pruned list, and Rgrounding measures final subtask success based on the Action Grounder's output. In our design, these rewards are binary rewards (1 for success, 0 for failure).

## Algorithm 1: Scoring Function Template

```
Input: E: Pre-processed list of candidate elements;
   W: Keywords with base weights ({k : wbase}) gener-
   ated by LLM
Output: S: Final relevance scores for ranking;
   P: Scoring justifications (paths)
Hyperparameters: α1 > α2 > α3 > α4 // Match
   Quality: Exact > Phrase > Word > Fuzzy
      β1 > β2 > β3 // Attribute Priority: Visual Text >
   Trusted Attribute > Other Attribute
 1: for each element e in E do
 2: S[e] ← 0; P[e] ← ∅
 3: for each attribute pair (text, type) in e do
 4: if type is Visual Text (e.g., text content) then
 5: β ← β1
 6: else if type is Trusted Attribute (e.g., name) then
 7: β ← β2
 8: else if type is Other Attribute (e.g., class, id) then
 9: β ← β3
10: end if
11: tokens ← Split(text)
12: for each keyword k in W do
13: α ← 0
14: if text = k then
15: α ← α1 // full exact match
16: else if (k has spaces) and (k is substring of text)
         then
17: α ← α2 // phrase match (on raw text)
18: else if (not k has spaces) and (k ∈ tokens)
         then
19: α ← α3 // word match (on token list)
20: else if FuzzyScore(k, text, tokens) > θ then
21: α ← α4 × FuzzyScore(k, text, tokens) //
           fuzzy match
22: end if
23: if α > 0 then
24: S[e] ← S[e] + (W[k] × α × β)
25: P[e].add(Path(k, type, α))
26: end if
27: end for
28: end for
29: end for
30: return (S, P)
```

# 4 Experiments

## 4.1 Experimental Setup

Benchmarks, Datasets, and Metrics. We conduct our primary offline evaluation on the standard Multimodal-Mind2Web benchmark (Deng et al. 2023a), following its official evaluation metrics (Element Accuracy, Operation F1, and Step Success Rate). For model fine-tuning, we use a custom dataset of approximately 5,000 interaction steps created by re-annotating and cleaning the Multimodal-Mind2Web training and development sets (detailed in Section 4.2). To assess the effectiveness of DOM Tree Pruning Programming, we build a new evaluation set from our re-annotated data. This benchmark uses ground-truth low-level sub-tasks as direct input to evaluate the grounding performance of the Programmatic Element Filter and Action Grounder models. We measure low-level sub-task grounding results using grounding accuracy. Additionally, we conduct targeted ablation studies on a curated set of online, dynamic websites, using LLM-Verified Task Completion Rate as the primary metric in Section 4.3.

Implementation Details. Our evaluation focuses on two versions of Prune4Web: a Two-turn Dialogue Unified version and a Separate Models version, both fine-tuned from Qwen2.5VL-3B-Instruct (Bai et al. 2023). To assess lowlevel sub-task grounding performance, we also trained a lighter Qwen2.5-0.5B-Instruct (Bai et al. 2023) model, demonstrating that our Programmatic Element Filter and Action Grounder operate effectively with lightweight LLMs. We developed all Prune4Web models using the two-stage SFT+RFT training approach described in Section 4.3.

Baselines. We compare our method with proprietary models such as GPT-4 (Achiam et al. 2023), GPT-4o (Hurst et al. 2024), and SeeAct (Zheng et al. 2024a), as well as state-ofthe-art fine-tuning methods based on open-source models, including SeeClick-9.6B (Cheng et al. 2024), MiniCPM-3.1B (Hu et al. 2024), ScribeAgent-32B (Shen et al. 2024), GPT-4o UGround (Gou et al. 2024b), EDGE-9.6B (Chen et al. 2024), and MindAct Flan-T5XL (Deng et al. 2023b).

## 4.2 Main Results

Performance on Standard Web Benchmarks. On the official Multimodal-Mind2Web test splits (results in Table 1), our proposed Prune4Web, particularly the Two-turn Dialogue unified model, demonstrates strong performance and significantly outperforms several baselines. Notably, our model achieves this competitive performance on a moderately sized training set of only ∼5,000 trajectories while directly processing raw, complex HTML. This demonstrates our method's excellent data efficiency and significant potential for improvement.

Performance on Low-Level Sub-Task Grounding. To precisely and isolatingly evaluate the effectiveness of DOM Tree Pruning Programming, we use a ground-truth lowlevel sub-task as direct input to evaluate the grounding performance of the Programmatic Element Filter and Action Grounder models. Since the unified Two-turn Dialogue model cannot be easily dissected for this purpose, we evaluate the Programmatic Element Filter and Action Grounder models trained using the Separate Models strategy. We report results for: 1) fine-tuning the Qwen2.5VL-3B-Instruct model using original HTML without pruning, 2) oracle pruning (GT elements guaranteed in top candidates), 3) direct pruning and decision with LLMs, and 4) our Prune4Web pruning and decision. The results (Table 2) show that, given a perfect low-level sub-task, our full Programmatic Element Filter–Action Grounder pipeline achieves a grounding accuracy of 88.28%. This performance far surpasses the baseline without pruning (46.8%) and significantly outperforms using the more powerful GPT-4o as the Action Grounder (80.65%). Additionally, even with the much lighter Qwen2.5-0.5B-Instruct, our method shows superior performance on both pruning results and grounding

| Method                                   | Cross-Task |                    | Cross-Website |                                                                         | Cross-Domain |      |      |      |      |
|------------------------------------------|------------|--------------------|---------------|-------------------------------------------------------------------------|--------------|------|------|------|------|
|                                          |            |                    |               | Ele. Acc Op. F1 Step SR Ele. Acc Op. F1 Step SR Ele. Acc Op. F1 Step SR |              |      |      |      |      |
|                                          |            | Proprietary Models |               |                                                                         |              |      |      |      |      |
| GPT-4 (Achiam et al. 2023)               | 40.8       | 63.1               | 32.3          | 30.2                                                                    | 61.0         | 27.0 | 35.4 | 61.9 | 29.7 |
| GPT-4o (Hurst et al. 2024)               | 5.7        | 77.2               | 4.3           | 5.7                                                                     | 79.0         | 3.9  | 5.5  | 86.4 | 4.5  |
| SeeAct (Zheng et al. 2024a)              | 46.4       | 73.4               | 40.2          | 38.0                                                                    | 67.8         | 32.4 | 42.4 | 69.3 | 36.8 |
|                                          |            | Open-Source Models |               |                                                                         |              |      |      |      |      |
| SeeClick-9.6B (Cheng et al. 2024)        | 26.3       | 86.2               | 23.7          | 21.9                                                                    | 82.9         | 18.8 | 22.1 | 84.1 | 20.2 |
| MiniCPM-3.1B (Hu et al. 2024)            | 23.8       | 86.8               | 20.8          | 20.3                                                                    | 81.7         | 17.3 | 17.9 | 74.5 | 14.6 |
| ScribeAgent-32B (Shen et al. 2024)       | 38.0       | 52.9               | 35.6          | 34.1                                                                    | 52.7         | 32.5 | 39.4 | 54.7 | 37.3 |
| GPT-4o UGround (Gou et al. 2024b)        | 47.7       | –                  | –             | 46.0                                                                    | –            | –    | 46.6 | –    | –    |
| EDGE-9.6B (Chen et al. 2024)             | –          | –                  | 30.0          | –                                                                       | –            | 21.1 | –    | –    | 22.4 |
| MindAct Flan-T5XL (Deng et al. 2023b)    | 55.1       | 75.7               | 52.0          | 42.0                                                                    | 65.2         | 38.9 | 42.1 | 66.5 | 39.6 |
|                                          |            | Prune4Web Variants |               |                                                                         |              |      |      |      |      |
| Prune4Web-3B (Separate Models)           | 46.0       | 83.4               | 42.2          | 43.0                                                                    | 77.3         | 37.8 | 42.2 | 84.4 | 40.6 |
| Prune4Web-3B (Two-turn Dialogue Unified) | 58.4       | 84.1               | 52.4          | 50.2                                                                    | 81.2         | 44.9 | 49.2 | 84.4 | 46.1 |

Table 1: Performance on the *Multimodal-Mind2Web* benchmarks across different methods. (Ele. Acc: Element Accuracy; Op. F1: Operation F1; Step SR: Step Success Rate). Two variants of our Prune4Web are evaluated. The Separate Models approach uses three independent models for the planner, filter, and grounder. The Unified Model approach uses an innovative two-turn dialogue training strategy to optimize three stages as a single model. Top-1 accuracy is represented using bold text.

accuracy. This experiment demonstrates that our DOM Tree Pruning Programming method achieves state-of-the-art performance in precise element localization and operation.

## 4.3 Ablation Studies and Further Analyses

To meticulously validate the contributions of our key design choices, we conduct ablation studies and further analyses. These experiments investigate the precision of our filtering mechanism, the effectiveness of programmatic filtering compared to simpler baselines, the contribution of our multistage architecture, and the efficacy of our training strategies. We also evaluate the framework's robustness in dynamic online environments to demonstrate its practical applicability. Performance in Dynamic Online Environments. The effectiveness of Prune4Web in dynamic online environments is demonstrated through our ablation studies in Table 3 and Table 4. Component analysis on a curated set of 30 online tasks shows consistent performance improvements. Our programmatic filtering significantly enhances task completion rates for smaller models like GPT-4o-mini, while the complete three-stage architecture achieves the best overall results. These findings confirm the framework's generalization capability and practical applicability in real-world settings. Effectiveness of Programmatic DOM Filtering. We compared our programmatic filtering against a baseline where the LLM directly performs Top-N selection in Table 3. The results show that for the powerful GPT-4o, our method maintains a high level of performance. However, its true value is demonstrated on smaller models. For GPT-4o-mini, Prune4Web's filtering boosts the task completion rate by over 5 percentage points (from 26.3% to 31.6%). For our fine-tuned Qwen2.5VL-3B, the baseline fails completely (0.0%), while our structured method achieves a functional

score (5.2%). This highlights that the programmatic ap-

proach is essential for enabling smaller or specialized models to handle complex filtering tasks. filtering tasks.

Contribution of the Multi-Stage Architecture. We evaluated the necessity of our three-stage Planning-Filtering-Action Grounding architecture. As shown in Table 4, each stage provides a clear benefit. For GPT-4o-mini, starting with only an Action Grounder yields 21.1% task completion. Adding the Planner boosts this to 26.3%, and further adding our Programmatic Element Filter brings the final performance to 31.6%. This steady improvement validates each component's contribution and confirms the rationality of our complete multi-stage design.

Efficacy of Training Strategies. We also assessed the impact of the RFT in Table 5. The results show that adding RFT on top of SFT consistently and significantly improves the Planner's capabilities. For the Separate Models framework, RFT boosts the Step Success Rate (Step SR) from 37.9% to 42.2%. For the Two-turn Dialogue Unified model, RFT provides an even larger boost, from 46.5% to 52.4%. These results confirm that our synergistic RFT approach, which uses filtering success as a reward, effectively optimize the Planner's policy for both training paradigms.

Filtering Recall Analysis. To evaluate the effectiveness of the scoring programs generated by the Programmatic Element Filter, we measured the Recall@N performance across various backbone models, as shown in Figure 3. The results clearly indicate that our fine-tuned models significantly outperform the zero-shot GPT models at all values of N. Specifically, both our fine-tuned Qwen2.5-0.5B and 3B models achieve a recall rate of over 90% when considering just the top 3 candidates (N = 3), and approach 95% at N = 5. In contrast, the powerful GPT-4o model only reaches approximately 72% recall at N = 3 and ends at around 86% at N = 20. A particularly noteworthy finding

| Method                                                    | Recall@20 | Grounding<br>Accuracy (%) |  |  |  |
|-----------------------------------------------------------|-----------|---------------------------|--|--|--|
| GT Task + Original HTML (No Pruning)                      |           |                           |  |  |  |
| Qwen2.5VL-3B-instruct (FT)                                | –         | 46.80                     |  |  |  |
| Oracle Pruning (GT guaranteed in top 20 candidates)       |           |                           |  |  |  |
| GPT-4o                                                    | –         | 82.83                     |  |  |  |
| GPT-4o-mini                                               | –         | 75.39                     |  |  |  |
| Qwen2.5VL-3B-instruct (ZS)                                | –         | 11.99                     |  |  |  |
| Qwen2.5VL-7B-instruct (ZS)                                | –         | 12.08                     |  |  |  |
| Qwen2.5VL-3B-instruct (FT)                                | –         | 90.28                     |  |  |  |
| GT Task + End-to-End LLM Pruning & Decision               |           |                           |  |  |  |
| GPT-4o                                                    | 85.56     | 70.84                     |  |  |  |
| GPT-4o-mini                                               | 89.19     | 67.57                     |  |  |  |
| GT Task + Prune4Web's Programmatic Element Filter Pruning |           |                           |  |  |  |
| GPT-4o                                                    | 85.56     | 80.65                     |  |  |  |
| GPT-4o-mini                                               | 89.19     | 73.75                     |  |  |  |
| Qwen2.5-0.5B-instruct (FT)                                | 97.64     | 88.28                     |  |  |  |
| Qwen2.5VL-3B-instruct (FT)                                | 97.46     | 88.28                     |  |  |  |

Table 2: Performance with Ground-truth (GT) low-level subtasks on our custom grounding benchmark (1101 trajectories), evaluating Programmatic Element Filter and Action Grounder capabilities under various conditions. Recall@20 indicates the percentage of times the ground-truth element is successfully included within the top 20 candidates after the filtering stage. ZS denotes zero-shot, and FT denotes finetuning. Top-1 accuracy is indicated by bold text.

| Filtering Method    | GPT-4o | GPT-4o-mini | Qwen2.5<br>VL-3B |
|---------------------|--------|-------------|------------------|
| LLM Top-N Selection | 42.1   | 26.3        | 0.0              |
| Prune4Web Filtering | 42.1   | 31.6        | 5.2              |

Table 3: Ablation on Programmatic DOM Filtering (LLM-Verified Task Completion Rate %).

is that our fine-tuned 0.5B model performs almost identically to the 3B model. This demonstrates that our DOM Tree Pruning Programming paradigm effectively distills the complex filtering task into a simple program generation problem that can be mastered even by smaller, more efficient models. This high recall with a small N is crucial, as it provides the downstream Action Grounder with a small, high-quality set of candidates, significantly reducing the difficulty of the final grounding step.

# 5 Conclusion

This paper addressed the significant challenge of information overload for LLM-based web agents by introducing Prune4Web, a multi-stage architecture based on a Planning → Programmatic Filtering → Action Grounding workflow and the core method of DOM Tree Pruning Programming. Our key innovation leverages LLMs to generate lightweight, interpretable Python programs that dynamically score and prune DOM elements based on semantic clues from de-

| Architecture                                            | GPT-4o       | GPT-4o-mini  |
|---------------------------------------------------------|--------------|--------------|
| Action Grounder Only                                    | 36.8         | 21.1         |
| Planner + Action Grounder<br>Full Framework (Prune4Web) | 42.1<br>42.1 | 26.3<br>31.6 |

Table 4: Ablation on multi-stage framework (LLM-Verified Task Completion Rate %).

| Training Strategy | Framework         | Step SR (%) |
|-------------------|-------------------|-------------|
| SFT Only          | Separate Models   | 37.9        |
| SFT + RFT         | Separate Models   | 42.2        |
| SFT Only          | Two-turn Dialogue | 46.5        |
| SFT + RFT         | Two-turn Dialogue | 52.4        |

Table 5: Ablation on training strategies (Step SR: Step Success Rate %) with Qwen2.5VL-3B-instruct on offline Multimodal-Mind2Web Cross-Task subset.

![](_page_6_Figure_11.jpeg)

Figure 3: Recall@N performance of our programmatic filtering stage with different backbone models. The y-axis represents the percentage of times the ground-truth element was successfully included in the Top-N candidates.

composed sub-tasks. This approach eliminates the need for LLMs to process massive DOMs, reducing candidate elements by 25∼50 times while maintaining high accuracy. Our automated data annotation pipeline provides supporting data for training our model. Additionally, our two-turn dialogue training strategy jointly trains the Planner, Filter and Grounder as a unified model. This training approach combines SFT with a targeted RFT that uses intermediate filtering results as reward signals for the upstream Planner, significantly improving the model's strategic task decomposition capabilities. In conclusion, Prune4Web offers an effective and efficient solution to information overload through its innovative programmatic pruning paradigm and synergistic training strategy, laying a solid foundation for more accurate and reliable next-generation web automation systems.

# 6 Acknowledgments

This work was supported in part by National Natural Science Foundation of China (No.62461160331, No.62132001, No.62572039), in part by Huawei-BUAA Joint Lab, in part by the Fundamental Research Funds for the Central Universities, and in part by the Young Elite Scientists Sponsorship Program by CAST.

# References

- Achiam, J.; Adler, S.; Agarwal, S.; Ahmad, L.; Akkaya, I.; Aleman, F. L.; Almeida, D.; Altenschmidt, J.; Altman, S.; Anadkat, S.; et al. 2023. Gpt-4 technical report. *arXiv preprint arXiv:2303.08774*.
- Bai, H.; Zhou, Y.; Pan, J.; Cemri, M.; Suhr, A.; Levine, S.; and Kumar, A. 2025a. Digirl: Training in-the-wild device-control agents with autonomous reinforcement learning. *Advances in Neural Information Processing Systems*, 37: 12461–12495.
- Bai, J.; Bai, S.; Yang, S.; Wang, S.; Tan, S.; Wang, P.; Lin, J.; Zhou, C.; and Zhou, J. 2023. Qwen-vl: A frontier large vision-language model with versatile abilities. *arXiv preprint arXiv:2308.12966*, 1(2): 3.
- Bai, S.; Chen, K.; Liu, X.; Wang, J.; Ge, W.; Song, S.; Dang, K.; Wang, P.; Wang, S.; Tang, J.; et al. 2025b. Qwen2. 5-vl technical report. *arXiv preprint arXiv:2502.13923*.
- Chen, X.; Li, H.; Liang, J.; Jiang, S.; and Yang, D. 2024. Edge: Enhanced grounded gui understanding with enriched multi-granularity synthetic data. *arXiv preprint arXiv:2410.19461*.
- Cheng, K.; Sun, Q.; Chu, Y.; Xu, F.; Li, Y.; Zhang, J.; and Wu, Z. 2024. Seeclick: Harnessing gui grounding for advanced visual gui agents. *arXiv preprint arXiv:2401.10935*.
- Deng, X.; Gu, Y.; Zheng, B.; Chen, S.; Stevens, S.; Wang, B.; Sun, H.; and Su, Y. 2023a. Mind2web: Towards a generalist agent for the web. *Advances in Neural Information Processing Systems*, 36: 28091–28114.
- Deng, X.; Gu, Y.; Zheng, B.; Chen, S.; Stevens, S.; Wang, B.; Sun, H.; and Su, Y. 2023b. Mind2Web: Towards a Generalist Agent for the Web. In *Proceedings of NeurIPS*.
- Furuta, H.; Lee, K.-H.; Nachum, O.; Matsuo, Y.; Faust, A.; Gu, S. S.; and Gur, I. 2023. Multimodal web navigation with instruction-finetuned foundation models. *arXiv preprint arXiv:2305.11854*.
- Gou, B.; Wang, R.; Zheng, B.; Xie, Y.; Chang, C.; Shu, Y.; Sun, H.; and Su, Y. 2024a. Navigating the digital world as humans do: Universal visual grounding for gui agents. *arXiv preprint arXiv:2410.05243*.
- Gou, B.; Wang, R.; Zheng, B.; Xie, Y.; Chang, C.; Shu, Y.; Sun, H.; and Su, Y. 2024b. Navigating the digital world as humans do: Universal visual grounding for gui agents. *arXiv preprint arXiv:2410.05243*.
- Guo, D.; Yang, D.; Zhang, H.; Song, J.; Zhang, R.; Xu, R.; Zhu, Q.; Ma, S.; Wang, P.; Bi, X.; et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*.

- Gupta, T.; and Kembhavi, A. 2023. Visual programming: Compositional visual reasoning without training. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 14953–14962.
- Gur, I.; Furuta, H.; Huang, A.; Safdari, M.; Matsuo, Y.; Eck, D.; and Faust, A. 2023. A real-world webagent with planning, long context understanding, and program synthesis. *arXiv preprint arXiv:2307.12856*.
- He, H.; Yao, W.; Ma, K.; Yu, W.; Dai, Y.; Zhang, H.; Lan, Z.; and Yu, D. 2024a. WebVoyager: Building an end-to-end web agent with large multimodal models. *arXiv preprint arXiv:2401.13919*.
- He, H.; Yao, W.; Ma, K.; Yu, W.; Zhang, H.; Fang, T.; Lan, Z.; and Yu, D. 2024b. Openwebvoyager: Building multimodal web agents via iterative real-world exploration, feedback and optimization. *arXiv preprint arXiv:2410.19609*.
- Hong, W.; Wang, W.; Lv, Q.; Xu, J.; Yu, W.; Ji, J.; Wang, Y.; Wang, Z.; Dong, Y.; Ding, M.; et al. 2024. Cogagent: A visual language model for gui agents. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 14281–14290.
- Hu, S.; Tu, Y.; Han, X.; He, C.; Cui, G.; Long, X.; Zheng, Z.; Fang, Y.; Huang, Y.; Zhao, W.; et al. 2024. Minicpm: Unveiling the potential of small language models with scalable training strategies. *arXiv preprint arXiv:2404.06395*.
- Hurst, A.; Lerer, A.; Goucher, A. P.; Perelman, A.; Ramesh, A.; Clark, A.; Ostrow, A.; Welihinda, A.; Hayes, A.; Radford, A.; et al. 2024. Gpt-4o system card. *arXiv preprint arXiv:2410.21276*.
- Jiang, J.; Wang, F.; Shen, J.; Kim, S.; and Kim, S. 2024a. A survey on large language models for code generation. *arXiv preprint arXiv:2406.00515*.
- Jiang, X.; Dong, Y.; Wang, L.; Fang, Z.; Shang, Q.; Li, G.; Jin, Z.; and Jiao, W. 2024b. Self-planning code generation with large language models. *ACM Transactions on Software Engineering and Methodology*, 33(7): 1–30.
- Kerboua, I.; Shayegan, S. O.; Thakkar, M.; Lu, X. H.; Cac- ` cia, M.; Eglin, V.; Aussem, A.; Espinas, J.; and Lacoste, A. 2025. LineRetriever: Planning-Aware Observation Reduction for Web Agents. *arXiv preprint arXiv:2507.00210*.
- Lai, H.; Liu, X.; Iong, I. L.; Yao, S.; Chen, Y.; Shen, P.; Yu, H.; Zhang, H.; Zhang, X.; Dong, Y.; et al. 2024. AutoWebGLM: A Large Language Model-based Web Navigating Agent. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 5295– 5306.
- Lin, K. Q.; Li, L.; Gao, D.; Yang, Z.; Wu, S.; Bai, Z.; Lei, W.; Wang, L.; and Shou, M. Z. 2024. Showui: One visionlanguage-action model for gui visual agent. *arXiv preprint arXiv:2411.17465*.
- Lu, X. H.; Kasner, Z.; and Reddy, S. 2024. Weblinx: Real- ` world website navigation with multi-turn dialogue. *arXiv preprint arXiv:2402.05930*.
- Lu, Z.; Chai, Y.; Guo, Y.; Yin, X.; Liu, L.; Wang, H.; Xiao, H.; Ren, S.; Xiong, G.; and Li, H. 2025. Ui-r1: Enhancing action prediction of gui agents by reinforcement learning. *arXiv preprint arXiv:2503.21620*.

- Ma, K.; Zhang, H.; Wang, H.; Pan, X.; Yu, W.; and Yu, D. 2023. Laser: Llm agent with state-space exploration for web navigation. *arXiv preprint arXiv:2309.08172*.
- Pan, Y.; Kong, D.; Zhou, S.; Cui, C.; Leng, Y.; Jiang, B.; Liu, H.; Shang, Y.; Zhou, S.; Wu, T.; et al. 2024. Webcanvas: Benchmarking web agents in online environments. *arXiv preprint arXiv:2406.12373*.
- Qi, Z.; Liu, X.; Iong, I. L.; Lai, H.; Sun, X.; Zhao, W.; Yang, Y.; Yang, X.; Sun, J.; Yao, S.; et al. 2024. WebRL: Training LLM Web Agents via Self-Evolving Online Curriculum Reinforcement Learning. *arXiv preprint arXiv:2411.02337*.
- Qiao, S.; Zhang, N.; Fang, R.; Luo, Y.; Zhou, W.; Jiang, Y. E.; Lv, C.; and Chen, H. 2024. AutoAct: Automatic agent learning from scratch for QA via self-planning. *arXiv preprint arXiv:2401.05268*.
- Qin, Y.; Ye, Y.; Fang, J.; Wang, H.; Liang, S.; Tian, S.; Zhang, J.; Li, J.; Li, Y.; Huang, S.; et al. 2025. UI-TARS: Pioneering Automated GUI Interaction with Native Agents. *arXiv preprint arXiv:2501.12326*.
- Qin, Y.; Zhou, E.; Liu, Q.; Yin, Z.; Sheng, L.; Zhang, R.; Qiao, Y.; and Shao, J. 2024. Mp5: A multi-modal openended embodied system in minecraft via active perception. In *2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 16307–16316. IEEE.
- Shao, Z.; Wang, P.; Li, S.; Zhang, Z.; Jin, P.; Liu, Z.; Chen, R.-Z.; Tu, Y.; Liu, S.; Wang, C.; et al. 2024. DeepSeek-Math: Pushing the Limits of Mathematical Reasoning in Open Language Models. *arXiv preprint arXiv:2402.01339*.
- Shen, H.; Liu, P.; Li, J.; Fang, C.; Ma, Y.; Liao, J.; Shen, Q.; Zhang, Z.; Zhao, K.; Zhang, Q.; Xu, R.; and Zhao, T. 2025. Vlm-r1: A stable and generalizable r1-style large vision-language model. *arXiv preprint arXiv:2504.07615*.
- Shen, J.; Jain, A.; Xiao, Z.; Amlekar, I.; Hadji, M.; Podolny, A.; and Talwalkar, A. 2024. ScribeAgent: Towards Specialized Web Agents Using Production-Scale Workflow Data. *arXiv preprint arXiv:2411.15004*.
- Song, Y.; Xu, F. F.; Zhou, S.; and Neubig, G. 2025. Beyond Browsing: API-Based Web Agents. In Che, W.; Nabende, J.; Shutova, E.; and Pilehvar, M. T., eds., *Findings of the Association for Computational Linguistics: ACL 2025*, 11066– 11085. Vienna, Austria: Association for Computational Linguistics. ISBN 979-8-89176-256-5.
- Tan, W.; Zhang, W.; Xu, X.; Xia, H.; Ding, Z.; Li, B.; Zhou, B.; Yue, J.; Jiang, J.; Li, Y.; et al. 2024. Cradle: Empowering foundation agents towards general computer control. *arXiv preprint arXiv:2403.03186*.
- Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; Xia, F.; Chi, E.; Le, Q. V.; Zhou, D.; et al. 2022. Chain-ofthought prompting elicits reasoning in large language models. *Advances in neural information processing systems*, 35: 24824–24837.
- Wen, H.; Li, Y.; Liu, G.; Zhao, S.; Yu, T.; Li, T. J.-J.; Jiang, S.; Liu, Y.; Zhang, Y.; and Liu, Y. 2024. Autodroid: Llmpowered task automation in android. In *Proceedings of the 30th Annual International Conference on Mobile Computing and Networking*, 543–557.

- Wu, Z.; Han, C.; Ding, Z.; Weng, Z.; Liu, Z.; Yao, S.; Yu, T.; and Kong, L. 2024. Os-copilot: Towards generalist computer agents with self-improvement. *arXiv preprint arXiv:2402.07456*.
- Xie, T.; Zhang, D.; Chen, J.; Li, X.; Zhao, S.; Cao, R.; Toh, J. H.; Cheng, Z.; Shin, D.; Lei, F.; et al. 2025. Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments. *Advances in Neural Information Processing Systems*, 37: 52040–52094.
- Xu, Y.; Wang, Z.; Wang, J.; Lu, D.; Xie, T.; Saha, A.; Sahoo, D.; Yu, T.; and Xiong, C. 2025. Aguvis: Unified Pure Vision Agents for Autonomous GUI Interaction. In *Proceedings of ICML*.
- Xue, T.; Qi, W.; Shi, T.; Song, C. H.; Gou, B.; Song, D.; Sun, H.; and Su, Y. 2025. An illusion of progress? assessing the current state of web agents. *arXiv preprint arXiv:2504.01382*.
- Yao, S.; Chen, H.; Yang, J.; and Narasimhan, K. 2022. Webshop: Towards scalable real-world web interaction with grounded language agents. *Advances in Neural Information Processing Systems*, 35: 20744–20757.
- Zhang, C.; Li, L.; He, S.; Zhang, X.; Qiao, B.; Qin, S.; Ma, M.; Kang, Y.; Lin, Q.; Rajmohan, S.; et al. 2024. Ufo: A ui-focused agent for windows os interaction. *arXiv preprint arXiv:2402.07939*.
- Zhang, C.; Yang, Z.; Liu, J.; Han, Y.; Chen, X.; Huang, Z.; Fu, B.; and Yu, G. 2023a. Appagent: Multimodal agents as smartphone users. *arXiv preprint arXiv:2312.13771*.
- Zhang, S.; Chen, Z.; Shen, Y.; Ding, M.; Tenenbaum, J. B.; and Gan, C. 2023b. Planning with large language models for code generation. *arXiv preprint arXiv:2303.05510*.
- Zheng, B.; Gou, B.; Kil, J.; Sun, H.; and Su, Y. 2024a. Gpt-4v (ision) is a generalist web agent, if grounded. *arXiv preprint arXiv:2401.01614*.
- Zheng, Y.; Zhang, R.; Zhang, J.; Ye, Y.; Luo, Z.; Feng, Z.; and Ma, Y. 2024b. LlamaFactory: Unified Efficient Fine-Tuning of 100+ Language Models. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 3: System Demonstrations)*. Bangkok, Thailand: Association for Computational Linguistics.
- Zhou, E.; An, J.; Chi, C.; Han, Y.; Rong, S.; Zhang, C.; Wang, P.; Wang, Z.; Huang, T.; Sheng, L.; et al. 2025a. RoboRefer: Towards Spatial Referring with Reasoning in Vision-Language Models for Robotics. *arXiv preprint arXiv:2506.04308*.
- Zhou, E.; Su, Q.; Chi, C.; Zhang, Z.; Wang, Z.; Huang, T.; Sheng, L.; and Wang, H. 2025b. Code-as-monitor: Constraint-aware visual programming for reactive and proactive robotic failure detection. In *Proceedings of the Computer Vision and Pattern Recognition Conference*, 6919–6929.
- Zhou, S.; Xu, F. F.; Zhu, H.; Zhou, X.; Lo, R.; Sridhar, A.; Cheng, X.; Ou, T.; Bisk, Y.; Fried, D.; et al. 2023. Webarena: A realistic web environment for building autonomous agents. *arXiv preprint arXiv:2307.13854*.

# Appendices

This supplementary material provides additional details omitted in the main text to facilitate a deeper understanding of our methodology and for reproducibility. The appendices are organized as follows:

- Appendix A: Framework Implementation Details. This section elaborates on the technical implementation of the Prune4Web framework, including the internal data flow, the detailed logic of DOM Tree Pruning Programming, the complete prompts used for all models, and the definition of the agent's action space.
- Appendix B: Dataset Construction and Annotation. This section provides a comprehensive overview of our data creation process. It details the selection and preprocessing of the source dataset, the annotation pipeline using GPT-4o, the multi-stage quality control measures, and the construction of our specialized benchmark for low-level sub-task grounding.
- Appendix C: Experimental Setup. This section outlines all configurations required to reproduce our experiments. It covers the benchmarks and datasets used, the precise definitions of all evaluation metrics, the hardware and software environment, and the final hyperparameter settings for both SFT and RFT stages.
- Appendix D: Training Strategy Details. This section offers an in-depth explanation of our training strategies. It describes the implementation of both the Separated Models and the Unified Model (Two-turn Dialogue) paradigms for SFT, and details the GRPO algorithm and the hierarchical reward mechanism used for RFT.
- Appendix E: Additional Experiments and Analyses. This section presents supplementary experiments to further validate our method's efficiency and modularity. It includes a detailed analysis of filtering precision, a performance comparison using smaller-parameter models, and an experiment verifying the plug-and-play capability of our framework.
- Appendix F: Case Studies and Discussion. This section provides an intuitive understanding of the framework's behavior through concrete examples. It includes a stepby-step walkthrough of a success case and an analysis of three distinct failure cases, followed by a systematic discussion of the method's limitations and directions for future work.

# A Framework Implementation Details

This section provides the necessary technical details and specific parameters to supplement the main paper. Our goal is to ensure the complete reproducibility of the Prune4Web framework.

## A.1 Framework Overview

As described in the main paper, the Prune4Web framework decomposes complex web tasks into a three-stage pipeline. The three stages are Planning, Filtering, and Action Grounding.

This section further clarifies the strong dependencies between these stages. The output of the Planning stage directly determines the goal for the Filtering stage. Correspondingly, the quality of the Filtering stage critically impacts the success of the Action Grounding stage.

This carefully designed structure of decoupled yet dependent components is key to the framework's ability to efficiently handle complex webpages. Its core philosophy is the separation of responsibilities. Each component focuses on the task it performs best. For example, the Planner is responsible for high-level strategic planning, while the Filtering and Grounding components handle low-level perception and execution.

To further clarify the system's interaction protocols and operational logic from an implementation perspective, we will now detail the internal data flow. Key data passed between models has explicit types. For instance, the low-level sub-task output by the Planner is a structured JSON object, while the parameters generated by the Programmatic Element Filter are passed to a Python function. The full DOM tree is provided as input only to the Filtering stage. In contrast, the Planner and Action Grounder process shorter, structured information. For example, the Planner receives a screenshot and a high-level task, while the Action Grounder receives a pruned list of candidate elements.

The workflow also contains explicit conditional logic. For example, the Filtering stage is activated only when the Planner's sub-task requires interaction with a page element. Otherwise, the workflow might proceed directly to an action that does not require element grounding, such as declaring the task complete in its final step. These implementation-level details are a necessary supplement to the framework diagram in the main text, ensuring that readers can understand the system's internal operating mechanics.

## A.2 DOM Tree Pruning Programming

The main paper identifies DOM Tree Pruning Programming as our core technique to address the performance degradation of Large Language Models (LLMs) when processing long contexts. This section details its core implementation idea: we transform a complex, semantics-based filtering task into a simple code generation task based on a domainspecific language. Specifically, the LLM no longer parses the DOM directly. Instead, it generates a Python dictionary as a parameter, which is then passed to a fixed, lightweight scoring function that is subsequently executed in an external environment.

Initial DOM Processing Script. Before executing the Python scoring function, we first run a JavaScript script, buildDomTree.js, in the browser environment to preprocess the live DOM. The core function of this script is to traverse the entire DOM tree and construct a simplified JSON object that contains only the elements potentially valuable for the current task. This JSON object then serves as the interactive elements input for the Python scoring function.

Interactivity Judgment. The isInteractiveElement function within the script defines what constitutes an interactive element. This is a complex boolean logic that considers multiple dimensions. These dimensions include HTML tags such as <a> and <button>, ARIA roles like button and link, specific attributes such as onclick and tabindex, CSS styles like cursor: pointer, and event listeners detected via window.getEventListeners. The function also includes special handling for common web components like cookie consent banners to improve robustness in real-world web environments.

Visibility and Hierarchy Judgment. In addition to interactivity, the script uses helper functions like isElementVisible and isTopElement to filter out elements that are invisible or obscured by other elements. This series of preprocessing steps ensures that the elements ultimately scored are those the user can currently see and interact with. It thus transforms a large, complex live DOM into a structured, prefiltered, and smaller-scale JSON object, laying the foundation for efficient subsequent scoring.

Scoring Function Template. The core of our method is a fixed, heuristic-based Python scoring function, the full implementation of which is provided in the supplementary code. Under this design, the LLM's task is significantly simplified. It only needs to generate a Python dictionary named keyword weights, where the keys are keyword strings and the values are their corresponding base weights, which are integers ranging from 1 to 50. The function relies on the rapidfuzz library for efficient fuzzy string matching and uses nltk.stem.PorterStemmer to normalize keywords and text through stemming.

Complex Scoring Logic. The function employs a sophisticated, multi-layered weighted scoring mechanism to calculate the relevance score for each element. This includes base score bonuses for the highest-weighted keywords and for keywords matched in the text content, as well as matchtype weighting for different match types like exact equality or phrase containment. It also uses the rapidfuzz library for fuzzy matching with defined thresholds and applies an attribute bonus for keywords matched in a predefined list of trusted attributes. This design hard-codes the complex and error-prone matching and scoring logic into the function template, ensuring the robustness and interpretability of the filtering process. At the same time, it constrains the LLM's task to a simple and well-defined generation problem.

## A.3 Model Prompt Engineering

In the Prune4Web framework, the behavior of each LLM component is precisely guided by highly structured prompts. These prompts act as the bridge between our abstract methodology and the concrete behavior of the models. Their quality directly determines the framework's overall performance. To meet the highest standards of reproducibility, we provide the verbatim prompt templates used to generate the results reported in this paper in the following paragraphs.

Planner Prompt. This prompt guides the model to act as a high-level planner. It requires the model to analyze the current situation based on the user's high-level task and a screenshot, and then generate a concise and clear low-level sub-task. The prompt includes strict output formatting requirements in JSON. It also contains specific instructions on how to handle common web interferences, such as pop-up dialogs.

Programmatic Element Filter Prompt. This prompt configures the model as a keyword extraction expert. It receives the low-level sub-task from the Planner as input and is required to output a keyword weights dictionary containing keywords and their weights. The prompt provides strategic advice on weight assignment, such as assigning higher weights to key nouns, to guide the model toward generating high-quality scoring parameters.

Action Grounder Prompt. This prompt requires the model to act as a precise executor. It receives the low-level sub-task and the pruned list of candidate elements as input. Its task is to select the single correct element from the list and decide on the action to be performed. The prompt emphasizes the need for logical reasoning during the thought process and to output the final decision in a specified format.

"Two-turn Dialogue" Unified Model Prompt. This prompt has a more complex structure and is used to train the unified model. In the first turn of the dialogue, the model acts as both the Planner and the Filter, generating the lowlevel sub-task and scoring parameters at once. After receiving the results from the externally executed filtering process, the dialogue proceeds to the second turn. In this second turn, the model then acts as the Action Grounder to make the final decision. This design aims to enhance the model's ability for continuous reasoning within the task's context.

## A.4 Action Space Definition

To ensure the deterministic nature of the agent's decision outputs and the reliability of downstream execution, we define a discrete and strict action space. This action space can be considered the API protocol between the Action Grounder model and the browser interaction engine, which is based on Playwright. The actions, including their names, parameters, and functional descriptions, will be detailed in a table, as referenced in Table 6.

Execution Details. The element index parameter is an abstract integer index. Upon receiving this index, the execution engine looks up the corresponding element's details, such as its XPath and CSS selectors, in the element hash map generated by buildDomTree.js. Subsequently, the engine employs a multi-strategy interaction method. It first attempts to perform a standard click or type operation using the retrieved selectors. If this fails, it falls back to dispatching JavaScript events, such as element.dispatchEvent(new MouseEvent('click', ...)), to simulate user interaction. This fallback mechanism is designed to improve the success rate of interactions on websites with complex front-end frameworks like React or Vue. Any model output that does not conform to the defined action space is considered an invalid action by the execution engine, thereby ensuring robust interaction.

# B Dataset Construction and Annotation

This section details the entire construction process for the custom dataset used to train and evaluate the Prune4Web framework. We aim to provide sufficient detail for other re-

Table 6: Definition of Action Space in the Prune4Web Framework

| Action                                             | Description                                                        | Parameters                                    |  |
|----------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------|--|
| CLICK(element_id)                                  | Clicks on a specified element on the page.                         | element_id: unique identifier from list $C_t$ |  |
| TYPE(element_id, text_to_input)                    | Types the provided text into the specified input field.            | element_id, text_to_input                     |  |
| SCROLL(direction)                                  | Scrolls the page vertically.                                       | direction: "up" or "down"                     |  |
| <pre>SELECT_OPTION(element_id, option_value)</pre> | Selects a specified option from a dropdown menu.                   | element_id,option_value                       |  |
| NAVIGATE(url)                                      | Navigates to a new webpage. Used to start tasks or load new pages. | url                                           |  |
| DONE ()                                            | Signals task/sub-task completion.                                  | None                                          |  |
| FAIL()                                             | Indicates inability to complete the current task.                  | None                                          |  |

searchers to understand and reproduce our data preparation work.

### **B.1** Data Source Selection and Preprocessing

The effectiveness of the Prune4Web framework relies heavily on high-quality training data annotated with intermediate reasoning steps. Existing web automation datasets generally lack the fine-grained intermediate labels required by our three-stage model, necessitating that we construct our own.

**Primary Data Source**. The foundation for all our training and evaluation data is the public Multimodal-Mind2Web (Deng et al. 2023a) (MM2W) dataset. Among the currently available datasets, MM2W is the only one that provides both rich HTML source code and corresponding webpage screenshots, making it suitable for our multimodal framework. Other datasets, such as WebVoyager (He et al. 2024a,b) and Mind2Web-live (Pan et al. 2024), only release their test sets and lack the necessary raw data for training. Therefore, MM2W is our sole choice at this stage, and we plan to collect or annotate more datasets in future work.

Initial Data Cleaning. Before beginning the annotation process, we first conducted a comprehensive initial cleaning of the MM2W training and test sets to eliminate annotation errors present in the original data. The first cleaning criterion was to remove data points where the Ground-Truth (GT) Element was actually missing from the HTML source code. The second criterion involved processing the original HTML source with our buildDomTree.js script, as described in Appendix A. We then checked if the GT element existed in our constructed DOM tree. If the GT element was lost because it could not be assigned an ID or XPath, we also considered this an annotation error in the original dataset and removed the data point.

Visual and Action Data Processing. The webpage screenshots provided in the MM2W dataset are often very long, with heights that can reach 10,000 pixels, making them unsuitable for direct model training and inference. We kept the screenshot width constant and vertically truncated the long screenshots into a series of standard-sized images with a height of 1080 pixels. We also recorded which of the truncated images contained the GT element. To enrich the action types, which were lacking in the original dataset, we added SCROLL and DONE actions. For truncated screenshots that did not contain the GT element, we annotated a SCROLL action. For the final screenshot in a task trajectory, we annotated a DONE action.

## **B.2** Annotation and Quality Control with GPT-40

Our data annotation pipeline was designed to generate intermediate labels corresponding to the three core components of our framework for each interaction step in the MM2W dataset. To ensure absolute fairness in testing, we annotated **only the MM2W training set (cross\_train)**. The three official test sets (cross\_task, cross\_website, cross\_domain) were not additionally annotated and were used directly for the final end-to-end evaluation.

Annotation Process. We used GPT-40 (Hurst et al. 2024) as the core annotation tool and designed specialized prompts for each annotation task. When annotating the low-level subtask, we provided the GT element information to GPT-40 to ensure the high accuracy of the generated sub-task. In addition to the core labels, we also annotated extra attributes for each stage, such as the current\_state describing the page status and a detailed thinking process, to support potential future training based on richer contextual reasoning.

Multi-Stage Quality Control. To ensure the final quality of the annotated data, we designed a rigorous multi-stage filtering process. The first stage was an automatic filter. After annotating the keywords and weights for the Programmatic Element Filter, we immediately invoked the scoring function to prune the DOM tree. If the GT element did not appear in the top-20 list of the pruned results, we considered the annotation or the original data to be of poor quality and completely removed that data point, including its corresponding Planner and Grounder annotations, from the training set. In the second stage of automatic filtering, during subsequent training preparation, we further removed data points with excessively long original HTML source tokens to avoid potential training issues. The third stage was manual verification. After all automatic filtering processes were complete, we conducted a final manual sampling check to ensure the overall high quality of the final dataset.

### **B.3** Low-Level Sub-Task Grounding Benchmark

To independently and precisely evaluate the effectiveness of our core method, DOM Tree Pruning Programming, we constructed a specialized benchmark from our newly annotated training set. We selected all steps that required interaction with page elements and randomly split them into a training set (80%) and a test set (20%). This benchmark is specifically designed to measure the performance of the subsequent Filtering and Grounding stages, given a perfect low-level sub-task.

**Evaluation Method.** On this benchmark, we adopted a separate training strategy, independently retraining the Pro-

grammatic Element Filter and Action Grounder models. The evaluation process consists of two steps. In the first step, a model generates keywords and weights based on the input low-level sub-task and then performs pruning. In the second step, another model outputs the final action based on the pruned list of elements. This allows us to decouple the evaluation of the Planner's planning ability from the execution capability of the downstream components, thereby directly validating the effectiveness of our filtering and grounding methods.

## B.4 Dataset Statistics

After all the cleaning, annotation, and filtering processes, we ultimately obtained a training dataset containing 5,503 highquality interaction steps. An "interaction step" refers to a single user action within a multi-step task, such as a click or an input. Each step includes the complete annotation information required for the three stages of our framework.

Dataset Splits and Usage. This dataset of 5,503 steps was further divided into two parts. A total of 4,402 steps (approximately 80%) were used as the training set for the low-level sub-task grounding benchmark. The remaining 1,101 steps (approximately 20%) were used as the test set for the same benchmark. The grounding accuracy of 88.28% reported in the main paper was measured on these 1,101 test steps. It is important to note that the training set used for the end-toend Prune4Web unified model consists of the entire dataset of 5,503 steps.

# C Experimental Setup

This section provides the complete configuration details required to reproduce all experimental results in this paper, including the benchmarks used, precise definitions of evaluation metrics, the computing environment, and model training hyperparameters.

# C.1 Benchmarks and Datasets

Our experimental design aims to comprehensively evaluate the performance of the Prune4Web framework across different scenarios. To this end, we employed both offline benchmarks and online dynamic websites for testing.

Offline Evaluation on Multimodal-Mind2Web. Our main offline evaluation was conducted on the Multimodal-Mind2Web (MM2W) benchmark. We strictly adhere to its official splits for the training, validation, and three test sets (cross-task, cross-website, cross-domain). This ensures that our results can be fairly and directly compared with other work in the field.

Online Evaluation on Dynamic Websites. To test the model's generalization ability and robustness in real, dynamic environments, we also conducted a series of online evaluations. We first filtered out a list of persistently inaccessible websites from the Mind2Web-live and WebVoyager test sets (e.g., kbb.com, sixflags.com, etc.). From the remaining pool of websites, we then randomly sampled 30 online tasks to form our test set, which covers common sites like Amazon and IMDb. We manually verified each of these 30 tasks to ensure they were completable during the testing period.

Low-Level Sub-Task Grounding Benchmark. As described in Appendix B, we constructed a specialized benchmark to independently evaluate the effectiveness of DOM Tree Pruning Programming. This benchmark uses our annotated dataset and focuses on assessing the accuracy of the subsequent filtering and grounding stages, given a perfect low-level sub-task.

# C.2 Evaluation Metrics

We used multiple metrics to evaluate model performance from different dimensions.

Official MM2W Metrics. For the MM2W benchmark, we use its official metrics: Element Accuracy, Operation F1, and Step Success Rate (SR). These metrics respectively measure element localization; operation type and parameter filling; and the overall success of a single interaction step.

Custom Grounding Metrics. For the low-level sub-task grounding benchmark, we use two main metrics. The first metric is Recall@k, which evaluates the performance of the filtering stage by measuring whether the ground-truth target element appears in the top-k candidates after pruning. The second metric is Grounding Accuracy, which evaluates the performance of the grounding stage by measuring whether the final executed action exactly matches the ground-truth action.

LLM-Verified Task Completion Rate. For online evaluation, we use the LLM-Verified Task Completion Rate as the primary metric, as the final state of online tasks is difficult to judge with fixed rules. We employ GPT-4o as an automated evaluator. We provide GPT-4o with the original task instruction, along with the agent's sequence of observations (screenshots) and executed actions from the last N steps (e.g., N=3) of the trajectory. The prompt requires GPT-4o to determine if the core objective of the task has been achieved and to output a "Success" or "Failure" judgment with a brief rationale.

## C.3 Hardware and Software Environment

Hardware Infrastructure. All experiments were conducted on a server equipped with 8 NVIDIA A800 80G GPUs. The server's CPU is a 14-core processor with 100G of RAM. During training, each GPU process was bound to a dedicated CPU core to ensure efficiency.

Software Stack. The software environment for the experiments was Ubuntu 20.04 with Python 3.10. Our training code was primarily developed based on the LLaMA-Factory (Zheng et al. 2024b) framework.

## C.4 Hyperparameter Settings

This section lists the final hyperparameter values for all models and algorithms in the SFT and RFT stages in a clear format. All reported hyperparameters were selected based on the best Step Success Rate achieved on the MM2W validation set.

Supervised Fine-Tuning (SFT) Hyperparameters. We used Qwen2.5VL-3B-Instruct (Bai et al. 2025b) and Qwen2.5-0.5B-Instruct (Bai et al. 2025b) as our base models. The key hyperparameters for the SFT stage were as follows: we used the AdamW optimizer with a learning rate of 5.0e-5 and a cosine learning rate schedule. The batch size per device was 1, with 8 gradient accumulation steps, resulting in an effective global batch size of 64. We used bf16 mixed-precision for training and enabled flash attn for efficiency. The number of training epochs for all models was 3.

Reinforcement Fine-Tuning (RFT) Hyperparameters. In the RFT stage, we used the GRPO (Guo et al. 2025) algorithm to optimize the Planner (or the first turn of the unified model). We adopted the default hyperparameter settings from the VLM-R1 (Shen et al. 2025) framework. In each optimization step, we generated K=4 responses for each prompt and scored them according to the reward function defined in Appendix D.

# D Training Strategy Details

This section delves into the specific details of the Supervised Fine-Tuning (SFT) and Reinforcement Fine-Tuning (RFT) stages, which together form our complete training strategy.

## D.1 Supervised Fine-Tuning (SFT)

All models' foundational capabilities are initialized through Supervised Fine-Tuning (SFT). The goal of SFT is to teach the model to generate outputs that conform to our predefined format and content, based on a given input. This stage provides a good "cold start" model for the subsequent Reinforcement Fine-Tuning (RFT) phase, allowing it to begin exploration from a reasonable base policy. We explored two SFT training paradigms: separated models and a unified model.

Separated Models Paradigm. In the separated models paradigm, we independently trained three specialized models for the framework's three core components: the Planner, the Programmatic Element Filter, and the Action Grounder. Each model was trained on data specific to its corresponding task, and their respective training objectives and inputoutput formats are detailed below.

Planner Model SFT. The training for the Planner model aims to teach it high-level planning. In training, the model receives input containing the current high-level task description and a webpage screenshot. It is trained to generate a structured string as output. This output string must contain two parts: a thought process enclosed in <think> tags, and a JSON object enclosed in <answer> tags. This JSON object needs to include a detailed analysis of the page state (state analysis), an evaluation of task progress (progress evaluation), challenges (challenges), the next low-level sub-task (next steps), the action type (action type), and the target text (target).

Programmatic Element Filter Model SFT. The training for this model aims to teach it to extract keywords for element localization from the plan. During training, the model receives the complete JSON output from the Planner model as input. Its expected output is also a string containing <think> and <answer> tags. In this output, the JSON object enclosed by the <answer> tag must contain a keyword weights key, whose value is a dictionary mapping keywords to their weights.

Action Grounder Model SFT. The training for the Action Grounder model aims to teach it to make the final decision based on the plan and the pruned list of elements. Its input is composed of the task context, the Planner's output, and the pruned list of DOM candidates. The model's expected output is also a string containing <think> and <answer> tags, where the JSON object enclosed by the <answer> tag must specify the final action type (action), the target element's ID (id), and any necessary input text (input text).

Unified Model with Two-turn Dialogue. We designed the unified model paradigm to explore the trade-offs between two different optimization paths for Web Agent tasks: one path involves decomposing the task and optimizing multiple separated models, while the other utilizes a unified data stream to optimize a single, end-to-end model. This paradigm uses an innovative "two-turn dialogue" training template to synergistically optimize all three component functionalities within a single model. First turn: The model's input consists of the high-level task, history, and a webpage screenshot. Its expected output is a structured string containing a thought process in <think> tags, a lowlevel sub-task in <plan> tags, and a keyword-weight dictionary in <keywords weights> tags. Second turn: After the system simulates the filtering operation, the resulting pruned DOM list is provided as input. The model's expected output is then a JSON object containing the final action, enclosed in <answer> tags.

Data Format Reference. The specific data formats and structures used in all the SFT training paradigms described above can be found in the data example files provided in the code repository accompanying our paper.

# D.2 Reinforcement Fine-Tuning (RFT)

As SFT struggles to teach models complex, forwardlooking, long-horizon planning, we employ Reinforcement Fine-Tuning (RFT) to further optimize the model. The goal of RFT is to enhance the Planner's strategic planning capabilities, enabling it to generate low-level sub-tasks that are more conducive to the success of downstream tasks. Therefore, RFT is applied only to the Planner model (in the separated paradigm) or to the first turn of the unified model.

GRPO Algorithm Implementation. We use the GRPO (Group Relative Policy Optimization) algorithm for policy optimization. GRPO estimates the relative advantage of each response by comparing the rewards of multiple responses generated from a single prompt, which leads to more stable updates of the policy model. Our implementation is based on the VLM-R1 framework and uses its default hyperparameter configuration.

The GRPO algorithm extends policy gradient methods by refining the advantage estimation. A key aspect involves calculating the relative advantage A<sup>i</sup> for the i-th response in a set of candidate responses O = {o1, o2, . . . , o<sup>N</sup> } generated from a state, given their respective rewards {r1, r2, . . . , r<sup>N</sup> }. The relative advantage is computed as:

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \dots, r_N\})}{\operatorname{std}(\{r_1, r_2, \dots, r_N\}) + \epsilon_{std}}$$

where mean and std denote the mean and standard deviation of the rewards, and ϵstd is a small constant for numerical stability. These relative advantages are then used to update the policy model, often under KL divergence constraints to stabilize training.

Hierarchical Reward Mechanism. The key to successful RFT lies in the hierarchical reward mechanism we designed for the Planner. The core idea of this mechanism is that the quality of the Planner is determined not only by itself but, more importantly, by whether its generated plan enables the subsequent Filter and Grounder components to execute successfully. Thus, the reward for the Planner at step t, denoted as Rt, is composed of the format reward for its own output and the success rewards achieved by the downstream components in that step.

Reward Function Definition. The reward we designed is step-wise; failure at one stage results in a reward of zero for all subsequent stages. The total reward R<sup>t</sup> is calculated with the formula: R<sup>t</sup> = Rfmt + α · Rf iltering success + β · Rgrounding success. Each component herein is a deterministic binary reward (1 for success, 0 for failure). Format Reward (Rfmt): This checks if the Planner's output is a valid JSON object that contains all the required keys. The reward is 1 if the format is completely correct, and 0 otherwise. Filtering Success Reward (Rf iltering success): This reward is calculated only if Rfmt = 1. The system executes the filtering operation and checks if the ground-truth target element appears in the top-20 list of pruned candidates. The reward is 1 if it is present, and 0 otherwise. Grounding Success Reward (Rgrounding success): This reward is calculated only if Rf iltering success = 1. The system proceeds with the grounding operation and checks if the final generated action perfectly matches the ground-truth action (including action type, element, and parameters). The reward is 1 if they match, and 0 otherwise. Considering this step-wise reward mechanism, we ultimately set the weight coefficients α and β to 1 to ensure the model can optimize its performance stably and progressively.

# E Additional Experiments and Analyses

This section provides additional experimental results and analyses to offer more detailed empirical evidence for the conclusions drawn in the main paper, and to further explore the efficiency and modularity of our method.

## E.1 Filtering Precision Analysis

To more comprehensively demonstrate the precision of our DOM Tree Pruning Programming method, this section provides detailed performance data for the filtering stage, specifically the Recall@k metric. This data serves as a tabular supplement to Figure 3 in the main paper, allowing readers to look up the precise recall rate for each value of k. Detailed Recall@k Performance. Table 7 details the Recall@k performance of four different backbone models: GPT-4o, GPT-4o-mini, Qwen2.5-0.5B-Instruct (Finetuned), and Qwen2.5VL-3B-Instruct (Finetuned), for k values ranging from 1 to 20. The data clearly shows that our fine-tuned models, even the smallest 0.5B version, exhibit extremely high recall rates at small k values (e.g., k ¡= 5), exceeding 95%. This finding is particularly important as it demonstrates that our method can place the ground-truth target element at the very top of the candidate list with high precision, thereby significantly reducing the decision-making difficulty for the downstream Action Grounder model.

Table 7: Sampled Recall@k performance of the filtering stage with different backbone models. Our fine-tuned models show superior performance, especially at smaller k values. All values are recall percentages (%).

| Model                       | 1     | 3     | 5     | 10    | 20    |
|-----------------------------|-------|-------|-------|-------|-------|
| GPT-4o                      | 51.41 | 72.12 | 76.75 | 82.29 | 85.56 |
| GPT-4o-mini                 | 51.04 | 72.21 | 79.02 | 84.38 | 89.19 |
| MindAct (Deng et al. 2023a) | 51.10 | 79.74 | 87.48 | 94.20 | 97.15 |
| Qwen2.5-0.5B (Ours)         | 74.30 | 90.83 | 93.55 | 95.64 | 97.55 |
| Qwen2.5VL-3B (Ours)         | 74.66 | 90.83 | 94.01 | 95.82 | 97.55 |

## E.2 Small-Parameter Model Performance Comparison

To validate the efficiency of our method and its low dependency on computational resources, we designed an experiment to evaluate the performance when using a smallerparameter model for the downstream components. Our hypothesis is that because the filtering and grounding tasks are greatly simplified within our framework, a smaller model should be able to maintain a high level of performance.

Experimental Setup. We created a mixed-parameter model configuration. The Planner continued to use the Qwen2.5VL-3B-Instruct model to ensure planning quality. The downstream Programmatic Element Filter and Action Grounder, however, used our trained Qwen2.5-0.5B-Instruct model. We directly compare the performance of this mixedmodel (3B Planner + 0.5B Downstream) with the separated model (Prune4Web-3B, Separated Models) reported in the main paper, which uses the 3B model for all components. The evaluation was conducted on the cross-task test set.

Results and Analysis. Table 8 shows the performance comparison of the two configurations on the three key metrics of the cross-task test set. The experimental results show that the configuration using the 0.5B model for downstream tasks performs very closely to the configuration using the 3B model for all components, with only a very slight drop in performance. This result strongly demonstrates that our method successfully transforms complex perception tasks into simpler generation tasks, making them manageable even for small-parameter models. This highlights the high efficiency and cost-effectiveness of our approach for practical deployment.

Table 8: Performance comparison on the cross-task test set between the full 3B model configuration and a mixedparameter configuration with a 0.5B downstream model.

| Method                        | Ele. Acc | Op. F1 (%) | Step SR (%) |
|-------------------------------|----------|------------|-------------|
| Prune4Web-3B (Separated)      | 46.0     | 83.4       | 42.2        |
| Prune4Web (3B Planner + 0.5B) | 44.6     | 82.4       | 41.3        |

# E.3 Plug-and-Play Capability Verification

This experiment aims to demonstrate that our filtering and grounding modules are not exclusively tied to our own Planner. Instead, they can serve as a universal, plug-and-play component to enhance the grounding performance of any existing Web Agent. To this end, we chose the current stateof-the-art GUI Agent model, UI-tars (Qin et al. 2025), as our integration target and comparison baseline, evaluating its performance on web tasks.

Experimental Setup. We first evaluated the end-to-end performance of the UI-tars model on the cross-task test set as our baseline. Next, we constructed a hybrid system. We directly parsed the 'thought' generated by UI-tars during its decision-making process and used it as the low-level subtask input for our pre-trained Programmatic Element Filter and Action Grounder models. By comparing the performance of these two approaches, we can clearly see the performance gain brought by integrating our modules.

Results and Analysis. Table 9 shows the performance comparison between the original UI-tars and the "UI-tars + Prune4Web" hybrid system on the cross-task test set. The results indicate that after integrating our filtering and grounding modules, the system's overall performance improved significantly across all three metrics. This is primarily because our programmatic pruning method effectively addresses the issue of inaccurate localization that the original model faced when dealing with complex DOMs. This experiment fully demonstrates that Prune4Web's filtering and grounding components possess excellent modularity and generalization capabilities, allowing them to serve as a universal enhancement technology to empower other Web Agent frameworks that can output a plan with a reasoning process.

Table 9: Performance comparison on the cross-task test set between the original UI-tars-1.5-7B model and a hybrid system integrated with Prune4Web's downstream modules.

| Method               | Op. F1 (%) | Step SR (%) |
|----------------------|------------|-------------|
| UI-tars (End-to-End) | 84.7       | 53.6        |
| UI-tars + Prune4Web  | 85.3       | 54.9        |

# F Case Studies and Discussion

This section provides detailed case studies to intuitively demonstrate the operational flow of the Prune4Web framework in practical tasks. Based on these cases, we then discuss the limitations of the current method and directions for future work.

## F.1 Success Case Analysis

To provide readers with a more intuitive understanding of the effectiveness of the Prune4Web framework across different task types, we present four success cases. We will first provide a detailed breakdown of an e-commerce task to showcase the complete workflow of the framework, followed by a brief introduction to several other cases to highlight its adaptability in various scenarios.

Detailed Walkthrough: E-commerce Shopping Task. We use the task "Buy a \$100 e-gift card for John on the Underarmour website" as an example to demonstrate the end-to-end execution process of the framework. Planning Stage: After receiving the task and screenshot, the Planner accurately decomposes the task into a series of sub-tasks, such as "fill in the recipient's email" and "click to add to bag." Filtering Stage: In each step, the Programmatic Element Filter generates highly relevant keywords (e.g., "recipient," "email") based on the current sub-task. As shown in Figure 4, the generated Python scoring program is executed, precisely pruning hundreds of interactive elements on the page down to just a few relevant input fields. Grounding Stage: The Action Grounder makes decisions on a very small set of candidates, easily selecting the correct element and performing the corresponding action, such as entering the email address. This case clearly demonstrates how our programmatic pruning method significantly reduces decision-making difficulty, thereby achieving precise and efficient multi-step form filling.

Capability Showcase: Information Retrieval on Amazon. Prune4Web excels at information retrieval tasks that involve searching and navigating through results. In the task "Find the cost of a 2-year protection for PS4 on Amazon," the agent must first handle a CAPTCHA, then search for the product, and finally identify the correct information from a list of results. As shown in Figure 5, the transition from a cluttered search results page to a focused view with only relevant protection plans clearly illustrates the effect of our Programmatic DOM Pruning. A large number of irrelevant elements are filtered out, simplifying the decision process and increasing the precision of the final action.

Capability Showcase: Handling Dynamic Webpages on GitHub. In tasks like "Sign up for a GitHub account," the page state changes dynamically with user input. Our framework demonstrates good adaptability. As the low-level subtask generated by the Planner shifts from clicking the initial "Sign up" button, to entering an email, and then to continuing, our programmatic pruning dynamically adapts to this shifting focus. As illustrated in Figure 6, at each distinct step, it precisely filters the webpage to highlight only the relevant interactive elements for the current sub-task, demonstrating the framework's adaptability in complex, multi-step scenarios.

Capability Showcase: Navigational Decision-Making on Amtrak. Unlike tasks that involve form-filling, many web automation challenges require the agent to make a series of navigational choices by understanding the semantic relevance of various hyperlinks. Figure 7 demonstrates the agent

![](_page_16_Figure_0.jpeg)

Figure 4: A detailed, step-by-step execution trace of the Prune4Web framework on an e-commerce gift card purchasing task. The figure highlights how programmatic pruning drastically reduces the candidate space at each step.

performing such a task: finding the national cafe menu on ´ the Amtrak website. At each step, such as on the "Onboard Dining" page, the Prune4Web framework leverages the task's intent to programmatically prune the options, correctly identifying "Cafe" as the most relevant link to achieve ´ the goal. This showcases the framework's effectiveness in handling complex navigational challenges by interpreting the semantic hierarchy of a website.

![](_page_17_Figure_0.jpeg)

Figure 5: Partial task trajectory for finding a protection plan on Amazon. Our Programmatic DOM Pruning method filters a large number of irrelevant elements, leaving only a few highly relevant options and simplifying the agent's decision process.

![](_page_17_Figure_2.jpeg)

Figure 6: Dynamic adaptation of element pruning in the multi-step task of signing up for a GitHub account. Prune4Web's programmatic pruning dynamically adapts to the shifting focus of the agent at each step.

# F.2 Failure Case Analysis: The Interdependence of Planning and Grounding

Analysis of failure cases reveals that the ultimate success of a task requires both high-quality Planning and precise Action Grounding. Although our Prune4Web framework performs exceptionally well in the Action Grounding stage, ef-

![](_page_18_Figure_0.jpeg)

Figure 7: Navigational decision-making for an information retrieval task on Amtrak. The framework correctly identifies the semantically relevant hyperlink at each step to navigate to the correct page.

fectively mitigating the problem of inaccurate element localization, a severe deficiency in the upstream Planning stage can still lead to the ultimate failure of the task. We will elaborate on this point with two typical planning failure cases.

Case 1: Ineffective Exploration Loop on Rottentomatoes. In the task "View all of the Most Popular TV on rottentomatoes," the agent got stuck in a 25-step ineffective exploration loop and ultimately failed. The root cause of the failure lies in the Planner generating a flawed plan. It failed to identify the correct "View All" or "Most Popular" navigation links on the page, instead incorrectly guiding the agent to cycle through different category filters. This case demonstrates that a flawed plan, even if every step is executed with precision, cannot lead the agent to the final goal.

Case 2: Incorrect Goal Identification on Carmax. In the task "Search for a full-time job in sales in Springfield on carmax," the agent ended up on an incorrect page for an inventory position in Raleigh. The failure again originated from the Planning stage. The Planner failed to correctly associate the core entities "sales" and "Springfield" with the corresponding input fields or filters on the page, instead formulating an incorrect search strategy. Although Prune4Web dynamically adjusted the pruning based on the incorrect intermediate intent at each subsequent step, the entire task was trapped in an irrecoverable failure loop from the very beginning due to the initial planning error.

Common Conclusion. These two cases both point to a core conclusion: the precision of the downstream execution modules cannot compensate for the failures of the upstream planning. This once again confirms the critical importance of the planning module in the overall agent architecture.

## F.3 Limitations and Future Work

Although Prune4Web achieved state-of-the-art performance in experiments, the aforementioned failure cases also reveal some limitations of its current implementation and help clarify the core contribution scope of this work. This section will systematically summarize these limitations and propose potential research directions accordingly.

Primacy of Planning and Scope of This Work. As the failure cases show, the performance bottleneck of the current framework lies mainly in the Planning stage. The Planner may sometimes produce flawed or non-progressive plans, leading to task failure. Here, we wish to emphasize that the core contribution of the Prune4Web framework and method lies in the optimization of the Action Grounding process. We focus on solving the problem of how to accurately and efficiently localize and execute an action, given a low-level sub-task. The optimization of the planning and decomposition capabilities for high-level tasks, while crucial, is not the primary focus of this paper. Experiments show that for errors in the planning stage, optimization through SFT+RFT with a small amount of data is not significantly effective.

Challenges in Filtering and Grounding. Although the current filtering and grounding stages are robust, they still face challenges when encountering non-standard web cod-

![](_page_19_Figure_0.jpeg)

Figure 8: A failure case on Rottentomatoes caused by a flawed plan from the upstream Planner, leading to a prolonged and ineffective exploration loop. This highlights the primacy of planning for task success.

![](_page_19_Figure_2.jpeg)

Figure 9: A failure case on Carmax where an initial planning error led the agent down a completely wrong path, which precise downstream execution could not rectify, reinforcing the critical role of upstream planning.

ing practices. **Non-standard HTML structure**: When web developers misuse non-semantic tags like <div> to build buttons or links, relying solely on CSS for their appearance

and functionality, our method struggles to identify their interactivity due to the lack of explicit HTML tags or role attributes. **Lack of semantic features**: When a large number

of interactive elements lack descriptive text, aria-labels, or other semantic attributes, our keyword matching mechanism becomes difficult. For example, a page might have many buttons with only icons and no text descriptions. Visual and source code inconsistency: Some websites prioritize visual presentation over the standardization of their HTML source code, leading to discrepancies between the text or structure in the source and what the user perceives visually. This can also mislead our filtering and grounding process.

Future Work. Significantly improving planning capabilities can be an important direction for future work. This may require larger and more diverse planning training data, or the introduction of more powerful exploration mechanisms such as Monte Carlo Tree Search. To address the challenges in the filtering and grounding stages, future work could explore stronger multimodal fusion methods. For example, combining visual information to understand the functionality of elements defined by CSS, or using layout analysis to infer the actual function of non-semantic <div> tags, could help overcome the challenges posed by non-standard webpages. In summary, these limitations provide clear and valuable directions for future research in the field of web agents. We believe that a robust Web Agent requires the synergistic development of both planning and grounding capabilities.

#### Planner System Prompt (Zero-shot)

#### Role Definition:

You are a planning agent that breaks down tasks into executable UI steps with strict safety protocols. Follow ABSOLUTELY:

### Core Rules:

1. POP-UP HANDLING: Only close non-normal pop-ups that block or interfere with the task (e.g., ads, mandatory login walls, cookie consent dialogs). Do not close or dismiss any normal UI pop-ups that do not affect task execution (e.g., search suggestion dropdowns, informational tooltips). 2. UI-ACTION FORMATTING: Phrase steps as EXACT interface commands (e.g., "click 'Submit' button", "type 'Paris' in search field"). 3. LOGIN RESTRICTIONS: NEVER trigger login UNLESS task explicitly mentions credentials or an undismissable login wall appears. 4. TERMINATION CRITERIA: TERMINATE SOLELY when: login wall appears WITH NO close option, paywall or other physical UI blockage occurs, or system security could be compromised.

### Available Actions:

- Click elements
- Input text into forms
- Scroll page up/down
- Navigate to URLs (only for initial navigation)

### Output Format:

```
"state analysis": "Brief context analysis",
"progress evaluation": "X% - Description",
"challenges": ["list"],
"next steps": ["Only output ONE action. Format: click 'X' button | type 'Y' in Z field | TERMINATE if..."],
"action type": "click | type | scroll | navigate",
"target": {
 "text": "ELEMENT TEXT to interact with (e.g., 'Search box', 'Login button')"
},
"reasoning": "Security/UI rationale"
```

#### Critical Instructions:

}

- For ALL actions: "target.text" must ONLY contain the TEXT OF THE ELEMENT to interact with
- For "type" actions: "target.text" is the element to type into (e.g., "Search box"), NOT what you want to type
- The content to type should ONLY appear in "next steps", NOT in "target.text"

## Table 11: Planner Prompt Structure (Training Version)

### Planner System Prompt (Training)

## Role Definition:

You are a planning agent that breaks down tasks into executable UI steps. Output the thinking process in <think> ... </think> tags, and the final answer in <answer> ... </answer> tags.

### Output Format:

```
<think>
[Your thinking process here]
</think>
<answer>
 "state analysis": "Brief context analysis",
 "progress evaluation": "X% - Description",
 "challenges": ["list"],
 "next steps": ["Only output ONE action. Format: click 'X' button | type 'Y' in Z field"],
 "action type": "click | select | input | scroll",
 "target": {
   "text": "ELEMENT TEXT to interact with (e.g., 'Search box', 'Login button')"
 }
}
</answer>
```

## Table 12: Programmatic Element Filter Prompt Structure (Zero-shot Version)

#### Programmatic Element Filter System Prompt (Zero-shot)

#### Role Definition:

You are a professional filter keyword generator. Your task is to generate keywords with their corresponding weights for filtering and scoring interactive elements based on the complete plan output from the Planner. Output the thinking process in <think> ... </think> tags, and the final answer in <answer> ... </answer> tags.

#### Task Description:

Analyze the Planner's output and generate relevant keywords with appropriate weights that can be used to score and filter webpage elements for the given task.

#### Keyword Weighting Strategy:

- Assign higher weights (e.g., 30-50) to critical, task-specific keywords.
- Assign medium weights (e.g., 10-25) for supporting or contextual terms.
- Assign lower weights (e.g., 1-10) for general relevance terms.

### Output Format:

```
<think>
[Your keyword analysis and weight assignment thinking process]
</think>
<answer>
 "keyword weights": {
   "keyword1": weight1,
   "keyword2": weight2
 }
}
</answer>
```

## Table 13: Programmatic Element Filter Prompt Structure (Training Version)

### Programmatic Element Filter System Prompt (Training)

### Role Definition:

You are a professional filter keyword generator. Your task is to generate keywords and weights for scoring elements based on the provided plan.

### Task Description:

Analyze the planner's output and generate relevant keywords with appropriate weights that can be used to score and filter webpage elements for the given task.

### Output Format:

Directly output a JSON object with the following structure:

```
"keyword weights": {
   "keyword1": weight1,
   "keyword2": weight2
 }
}
```

#### Action Grounder System Prompt (Zero-shot)

#### Role Definition:

You are an AI agent designed to automate browser tasks. Your goal is to accomplish the ultimate task by following the rules.

#### Thinking Requirements:

In your thinking process, carefully analyze both the Planner's results and the pruned DOM tree to identify the correct element. Specifically describe how you used the Planner's target information and the DOM tree to make your decision. IMPORTANT: Explicitly mention element IDs when discussing them (e.g., "I identified element ID 123 as the target because..." or "Comparing elements with IDs 456 and 789, I determined that ID 456 is more appropriate because...").

#### Input Format:

Elements are presented in a standard format with IDs: [id]<type>text</type>

- Only elements with numeric IDs in [] are interactive.
- Elements without [] provide only context.

#### Output Format:

```
<think>
[Your thinking process with explicit element ID mentions]
</think>
<answer>
 "action": "click element | input text | select element | scroll",
 "id": element id integer,
 "input text": "input text content or 'no input text' [default]"
</answer>
```

## Table 15: Action Grounder Prompt Structure (Training Version)

### Action Grounder System Prompt (Training)

### Role Definition:

You are an AI agent designed to automate browser tasks. Your goal is to accomplish the ultimate task by selecting the correct element from the provided list.

### Input Format:

Elements are presented in a standard format with IDs: [id]<type>text</type>

- Only elements with numeric IDs in [] are interactive.
- Elements without [] provide only context.

## Output Format:

```
Directly output a JSON object with the following structure:
 "action": "click element | input text | select element | scroll",
 "id": element id integer,
 "input text": "input text content or 'no input text' [default]"
```

#### Task Completion Verification Prompt

#### Role Definition:

You are an impartial evaluator. Your task is to determine if a web agent successfully completed its assigned task based on its final actions and observations.

#### Task Instruction:

```
{Original Task Description}
```

### Agent's Final Trajectory (Last 3 Steps):

```
Step N-2:
Observation: [Screenshot Image]
Action: {action details}
Step N-1:
Observation: [Screenshot Image]
Action: {action details}
Step N:
Observation: [Screenshot Image]
Action: {action details}
```

#### Your Task:

Based on the final trajectory, did the agent successfully complete the core objective of the task instruction? Please answer with a JSON object containing two keys: "success" (boolean) and "reasoning" (a brief explanation for your decision).

### Output Format:

```
"success": true|false,
 "reasoning": "Your brief explanation here."
}
```

## Table 17: Two-turn Dialogue Training Template

### Unified Model Training Conversation Structure

### System Message:

You are an expert web automation assistant. Based on the user's task description, history, and a screenshot of the current webpage, you must first generate a thought process, a plan, and a set of keywords and weights for scoring DOM elements. Afterwards, when presented with a list of candidate elements, you must make the final selection.

### Turn 1

### User Input:

```
<image>{"task description": "...", "history": [...] }
```

### Assistant Output (Expected):

<think>...</think> <plan>...</plan> <keywords weights>{...}</keywords weights>

## Turn 2

## User Input:

```
Here is the list of candidate elements, each with a unique ID. Please choose the ID of the correct element.
[id]<type>...</type>
[id]<type>...</type>
...
```

## Assistant Output (Expected):

```
<answer>{'action': ..., 'id': ..., 'input text': ...}</answer>
```