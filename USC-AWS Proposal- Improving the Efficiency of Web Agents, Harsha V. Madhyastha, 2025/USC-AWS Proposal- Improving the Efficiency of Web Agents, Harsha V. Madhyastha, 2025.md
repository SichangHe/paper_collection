# **Improving the Efficiency of Web Agents**

**PI:** Harsha V. Madhyastha, Professor, Department of Computer Science, University of Southern California

### **Cash funding needed:** \$70,000

### **AWS Promotional Credits needed:** \$50,000

## **Abstract**

The vision of agentic AI is already coming to fruition on the web. State-of-the-art web agents can automate the execution of many diverse tasks which are cumbersome for users. However, in their current form, offering web agents as a service is impractical at scale. They incur high cost both due to the significant amount of computation they perform when executing a typical task and their large input to the foundation models they consult.

We observe that the inefficiency of existing web agents stems from them treating the web browser as a blackbox. Web browsers are designed to load any page in its entirety, as any of the content/functionality on the page may be of interest to the user. In contrast, when a web agent visits a page, it needs the browser to only fetch and process that subset of the page's source which is relevant to the task at hand. This will significantly reduce both the work that an agent needs to do when loading web pages as well as the amount of information about each page that it will need share in order to seek input from a foundation model. Based on this insight, we propose to design, implement, and evaluate Swiftor (short for Swift Executor), a new web agent which can be used cost-effectively at scale.

**Keywords:** Web agents, Agent as a Service, Scalability, Efficiency

## **Introduction**

**Context.** Modern human society relies on the web for a wide range of information and services: news, shopping, weather, travel, etc. However, many of the tasks we seek to accomplish on the web are laborious and require us to navigate complex user interfaces. As an example, consider the task of finding the cheapest computer monitor which has a desired set of features. One has to visit many pages on many sites, figure out how to filter and sort the search results on each site, and inspect the details of every search result.

Therefore, leveraging advances in computer vision and AI, there has recently been a rise in efforts to build software-based agents which can execute tasks on the web on behalf of users. Given a task description as input, a typical web agent consults a foundation model to identify which pages it should visit. The agent loads each of these pages using a web browser, extracts information about the elements on the page, and again queries the foundation model to determine its subsequent actions, e.g., follow a certain link or click a specific button. Today, there are a plethora of such agents [\[9,](#page-3-0) [13,](#page-3-1) [10,](#page-3-2) [11,](#page-3-3) [1\]](#page-3-4) and there also exist many benchmarks [\[12,](#page-3-5) [14,](#page-3-6) [7,](#page-3-7) [4\]](#page-3-8) to compare these agents across a wide variety of tasks.

**Problem.** We observe that all existing web agents share two common sources of inefficiency, both of which stem from the high complexity of modern web pages [\[3\]](#page-3-9). First, because of the widespread usage of JavaScript to enable dynamism and personalization, each page load incurs a significant amount of computation [\[8,](#page-3-10) [6\]](#page-3-11). Second, the many diverse elements on a typical web page – text blocks, image carousels, menu bars, etc. – and the many modes of interacting with a page – click a button, select a filter, scroll down, etc. – inflate the size of the input to a foundation model in order to identify the agent's next action. Figure [1](#page-1-0) quantifies these two problems by executing a state-of-the-art web agent – Browser Use [\[1\]](#page-3-4) – on six representative tasks.

These inefficiencies result in two significant downsides. On the one hand, the operators of web agents have to incur high costs, both to run the agents in the cloud and to query a foundational model service. On the other hand, users have to wait for long to have their tasks completed.

## **Methods**

**Key insight.** We observe that the key source of inefficiency in web agents is that, when visiting any page, they load the page exactly as a user would, i.e., the browser employed by an agent fetches all the resources on the page and renders the page in its entirety. This is unnecessary because, unlike when a user visits a

page, only a small portion of the elements on a page are relevant to a web agent: specifically, those portions relevant to its input task. Therefore, loading those portions of a page which are irrelevant to the task at hand incurs compute overhead and inflates cost without any corresponding utility.

To exploit this observation, our key insight is that a typical web page is not a monolithic entity. Instead, a web browser constructs a web page by fetching and processing many scripts. If a browser skips executing all the scripts on a page, much of the content and functionality on the page is likely to be missing. However, if the browser fetches and executes a subset of a page's scripts, then the page will still be partially functional.

Figure [2](#page-1-1) shows an example from [apple.com'](apple.com)s homepage. On the left is a screenshot captured when the page is loaded as normal, which takes 1564 ms to complete. In the middle, the same page is loaded with JavaScript execution disabled; the page load completes in 992 ms, but is missing the image carousel and all interactions (*e.g.,* menu clicks) no longer work. By carefully selecting which subset of scripts on the page are executed, the screenshot on the right shows that we are able to do away with the carousel, but preserve all interactions. For tasks where the images in the carousel offer no utility, an agent can use this method to complete loading the page in 1043 ms. Though the speedup of roughly 500 ms in this example may seem small, note that a web agent typically needs to load many pages to execute a single task. Moreover, when offered as a service, a web agent will execute tasks on behalf of many users.

<span id="page-1-0"></span>![](_page_1_Figure_3.jpeg)

**FIGURE 1:** Quantification of inefficiencies when using Browser Use to execute six example tasks: (a) The amount of CPU time when running the agent and the cost for the container in which the agent runs. (b) The size of the agent's input to Google Gemini and the corresponding cost.

**Proposed work.** To exploit the above observation for improv-

ing the efficiency of web agents, the primary question at hand is: given a specific input task, for every page that the agent loads, what is the minimum subset of the page's resources that it must fetch and execute in order to accomplish the task? For this, we exploit the fact that, when offered as a service to a large population of users, a web agent is likely to load each page many times while serving requests from different users. As it does so, we envision that it will build a profile of each page's content and constituent resources as follows.

*Classification of page content.* First, based on a web agent's repeated loads of a page over time, we aim to build a page-specific classifier which, given a specific task description as input, can partition the elements on the page into two bins: those which are likely relevant for the task, and those which are not. In any particular page load, the agent can identify the specific page elements that it must interact with only by consulting

<span id="page-1-1"></span>![](_page_1_Figure_8.jpeg)

**FIGURE 2:** Screenshots of the <apple.com> homepage: (left) normal page load, (middle) page load with all JS execution disabled, and (right) page load with only JS for loading the image carousel disabled. with JS enabling all other interactions

a foundation model. However, our lightweight classifier, which the agent can execute locally, will aim to conservatively identify all the elements which could potentially be relevant to the task at hand, thereby reducing the size of the input to the foundation model and the resulting cost. To develop this classifier, we will take advantage of the fact that, though the specific content on any page changes over time, its layout and the *kind of content* at each spot on the page is largely stable.

*Inference of resource dependencies.* Second, we seek to develop methods to infer two kinds of dependencies within every page. On the one hand, for every element on a page, we will identify which of the scripts on the page contribute to the construction of that element, including fetching its content, adding it to the page's layout, and properly initializing any interactions with the element. On the other hand, even if a script does not directly contribute to a specific page element, it may indirectly do so. For example, a script which initializes a particular page element may invoke utility functions included in another script. For inferring both kinds of dependencies, we will leverage our extensive prior work on instrumenting and analyzing JavaScript code [\[8,](#page-3-10) [5,](#page-3-12) [6\]](#page-3-11).

*System design and implementation.* Putting everything together, our proposed web agent Swiftor (short for Swift Executor) will work as follows. Like all other web agents, given a task to execute, Swiftor will consult a foundation model to identify which pages to load and how to interact with each page. However, unlike existing agents, for every page that it loads, Swiftor will a) run our lightweight classifier to identify which elements on the page could potentially be relevant to the task, and b) fetch and process only that subset of the page's content and code that influence the construction of these elements. To accomplish these modifications to page loads, we will lean on our group's experience in interacting with the Chromium web browser via the Chrome Devtools Protocol (CDP).

## **Expected results**

- **Months 1–4**: We will develop the above-mentioned methods for enabling a web agent to load only that portion of every web page which is likely relevant for its input task.
- **Months 5–6**: We will implement Swiftor by incorporating our methods into an open-source web agent such as Browser Use [\[1\]](#page-3-4) or Agent Occam [\[13\]](#page-3-1).
- **Months 7–10**: We will evaluate Swiftor on benchmarks such as WebVoyager [\[7\]](#page-3-7) and WebArena [\[14\]](#page-3-6) with respect to efficiency, cost, and accuracy. We will use our evaluation results to refine our methods.
- **Months 11–12**: We will write up a research paper describing the outcomes of our research and submit for publication at a top-tier conference. We will also open source all of our code and data.

# **Funds needed**

We request \$70,000 to support this one-year project. \$60,000 will be used to pay the salary, benefits, and tuition for one year for one graduate student researcher. The remaining funds will help support half a month of summer salary for the PI.

In addition, we request \$50,000 in AWS credits to support the development and evaluation of Swiftor. Of this, we estimate that \$30,000 will be needed to support Swiftor's use of Amazon Bedrock, which offers a diverse selection of foundation models, including Amazon Nova, DeepSeek-R1, and Meta Llama 4. For reference, one run of Browser Use on all tasks in the WebVoyager benchmark costs around \$250 [\[2\]](#page-3-13). We plan to test Swiftor across multiple benchmarks, using multiple models, and rerun each test several times as we refine our methods. We estimate that the remaining \$20,000 will go towards the storage, CPU, and memory of the container in which we will run Swiftor.

# **Additional Information**

We plan to contribute back to open-source web agents Browser Use and Agent Occam by modifying their use of the web browser to benefit from the methods we develop as part of the proposed research.

In our research thus far, we have run web agents using Google's Gemini and OpenAI's GPT-4o models. In this project, we will instead experiment with the models offered on Amazon Bedrock.

### **References**

- <span id="page-3-4"></span>[1] Browser Use – Enable AI to control your browser. [https://browser-use.com/.](https://browser-use.com/)
- <span id="page-3-13"></span>[2] WebVoyager Evaluation for Browser Use. [https://github.com/browser-use/eval,](https://github.com/browser-use/eval) 2023. Fork of the original WebVoyager repository with modifications for browser use evaluation.
- <span id="page-3-9"></span>[3] M. Butkiewicz, H. V. Madhyastha, and V. Sekar. Characterizing Web Page Complexity and Its Impact. In *Proceedings of the ACM Internet Measurement Conference (IMC)*, 2011.
- <span id="page-3-8"></span>[4] X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su. Mind2Web: Towards a Generalist Agent for the Web. In *Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track*, 2023.
- <span id="page-3-12"></span>[5] A. Goel, J. Zhu, R. Netravali, and H. V. Madhyastha. Jawa: Web Archival in the Era of JavaScript. In *OSDI*, 2022.
- <span id="page-3-11"></span>[6] A. Goel, J. Zhu, R. Netravali, and H. V. Madhyastha. Sprinter: Speeding Up High-Fidelity Crawling of the Modern Web. In *NSDI*, 2024.
- <span id="page-3-7"></span>[7] H. He, W. Yao, K. Ma, W. Yu, Y. Dai, H. Zhang, Z. Lan, and D. Yu. WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 6864–6890, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
- <span id="page-3-10"></span>[8] S. Mardani, A. Goel, R. Ko, H. Madhyastha, and R. Netravali. Horcrux: Automatic JavaScript Parallelism for Resource-Efficient Web Computation. In *OSDI*, 2021.
- <span id="page-3-0"></span>[9] S. Marreed, A. Oved, A. Yaeli, S. Shlomov, I. Levy, A. Sela, A. Adi, and N. Mashkif. Towards Enterprise-Ready Computer Using Generalist Agent. *arXiv preprint arXiv:2503.01861*, 2025.
- <span id="page-3-2"></span>[10] OpenAI. Operator System Card. [https://openai.com/index/operator-system-card/,](https://openai.com/index/operator-system-card/) January 2025. Details OpenAI's multi-layered approach for testing and deploying Operator safely, including risk areas and implemented mitigations.
- <span id="page-3-3"></span>[11] H. Su, R. Sun, J. Yoon, P. Yin, T. Yu, and S. O. Arık. Learn-by-Interact: A Data-Centric Framework for Self-Adaptive Agents in Realistic Environments. *arXiv preprint arXiv:2501.10893*, 2025.
- <span id="page-3-5"></span>[12] F. F. Xu, Y. Song, B. Li, Y. Tang, K. Jain, M. Bao, Z. Z. Wang, X. Zhou, Z. Guo, M. Cao, M. Yang, H. Y. Lu, A. Martin, Z. Su, L. Maben, R. Mehta, W. Chi, L. Jang, Y. Xie, S. Zhou, and G. Neubig. TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks. *arXiv preprint arXiv:2412.14161*, 2024.
- <span id="page-3-1"></span>[13] K. Yang, Y. Liu, S. Chaudhary, R. Fakoor, P. A. Chaudhari, G. Karypis, and H. Rangwala. AgentOccam: A Simple Yet Strong Baseline for LLM-Based Web Agents. In *Proceedings of the 13th International Conference on Learning Representations (ICLR)*, 2025. Poster presentation.
- <span id="page-3-6"></span>[14] S. Zhou. WebArena: A Realistic Web Environment for Building Autonomous Agents. In *Proceedings of the 37th Conference on Neural Information Processing Systems (NeurIPS)*, 2023. Spotlight talk at the Agent Learning in Open-Endedness Workshop.