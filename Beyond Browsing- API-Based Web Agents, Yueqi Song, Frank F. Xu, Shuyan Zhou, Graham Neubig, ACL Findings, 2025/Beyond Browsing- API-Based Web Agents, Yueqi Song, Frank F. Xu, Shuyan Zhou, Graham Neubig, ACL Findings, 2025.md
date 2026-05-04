# Beyond Browsing: API-Based Web Agents

### Yueqi Song, Frank Xu, Shuyan Zhou, Graham Neubig

{yueqis,gneubig}@cs.cmu.edu Carnegie Mellon University

<https://yueqis.github.io/API-Based-Agent/>

### Abstract

Web browsers are a portal to the internet, where much of human activity is undertaken. Thus, there has been significant research work in AI agents that interact with the internet through web browsing. However, there is also another interface designed specifically for machine interaction with online content: application programming interfaces (APIs). In this paper we ask – *what if we were to take tasks traditionally tackled by Browsing Agents, and give AI agents access to APIs*? To do so, we propose two varieties of agents: (1) an API-calling agent that attempts to perform online tasks through APIs only, similar to traditional coding agents, and (2) a Hybrid Agent that can interact with online data through both web browsing and APIs. In experiments on WebArena, a widely-used and realistic benchmark for web navigation tasks, we find that API-Based Agents outperform web Browsing Agents. Hybrid Agents outperform both others nearly uniformly across tasks, resulting in a more than 24.0% absolute improvement over web browsing alone, achieving a success rate of 38.9%, the SOTA performance among task-agnostic agents. These results strongly suggest that when APIs are available, they present an attractive alternative to relying on web browsing alone.

### 1 Introduction

Web agents use browsers as an interface to facilitate humans in performing daily tasks such as online shopping, online planning, trip planning, and other work-related tasks [\(Liu et al.,](#page-10-0) [2018;](#page-10-0) [Li et al.,](#page-10-1) [2020;](#page-10-1) [Rawles et al.,](#page-11-0) [2023;](#page-11-0) [Patil et al.,](#page-11-1) [2023;](#page-11-1) [Pan et al.,](#page-11-2) [2024;](#page-11-2) [Chen et al.,](#page-9-0) [2024a;](#page-9-0) [Huang et al.,](#page-10-2) [2024;](#page-10-2) [Du](#page-10-3)[rante et al.,](#page-10-3) [2024\)](#page-10-3). Existing web agents typically operate within the space of graphical user interfaces (GUI) [\(Zhang et al.,](#page-12-0) [2023;](#page-12-0) [Zhou et al.,](#page-12-1) [2024;](#page-12-1) [Zheng et al.,](#page-12-2) [2024\)](#page-12-2), using action spaces that simulate human-like keyboard and mouse operations, such as clicking and typing. To observe webpages,

common approaches include using accessibility trees, a simplified version of the HTML DOM tree, as input to text-based models [\(Zhou et al.,](#page-12-1) [2024;](#page-12-1) [Drouin et al.,](#page-9-1) [2024a\)](#page-9-1), or multi-modal, screenshotbased models [\(Koh et al.,](#page-10-4) [2024a;](#page-10-4) [Xie et al.,](#page-11-3) [2024;](#page-11-3) [You et al.,](#page-12-3) [2024;](#page-12-3) [Hong et al.,](#page-10-5) [2023\)](#page-10-5). However, regardless of the interaction method with websites, there is no getting around the fact that these sites were originally designed for humans, and may not be the ideal interface for machines.

Notably, there is another interface designed specifically for machine interaction with the web: application programming interfaces (APIs) [\(Chan](#page-9-2) [et al.,](#page-9-2) [2024\)](#page-9-2). APIs allow machines to communicate directly with backends of web services [\(Brana](#page-9-3)[van et al.,](#page-9-3) [2009\)](#page-9-3), sending and receiving data in machine-friendly formats such as JSON or XML [\(Meng et al.,](#page-11-4) [2018;](#page-11-4) [Xu et al.,](#page-11-5) [2021;](#page-11-5) [Trivedi et al.,](#page-11-6) [2024\)](#page-11-6). Nonetheless, whether AI agents can effectively use APIs to tackle real-world online tasks, and the conditions under which this is possible, remain unstudied. In this work, we explore methods for tackling tasks normally framed as webnavigation tasks with an expanded action space to interact with APIs. To do so, we develop new *API-Based Agents* that directly interact with web services via API calls. This method bypasses the need to interact with web GUIs.

However, not all websites have extensive API support, in which case web browsing actions may still be required. To overcome this limitation, we propose a *hybrid* approach that combines API-Based Agents with Browsing Agents, as depicted in Figure [1.](#page-1-0) Rather than choosing between API calling and web browsing at the task level, our Hybrid Agent is capable of dynamically *interleaving* both actions. We found that agents benefit from the flexibility of this hybrid model. When APIs are available and well-documented, the agent can directly interact with the web services. For websites with limited API support, the agent seamlessly in-

<span id="page-1-0"></span>![](_page_1_Figure_0.jpeg)

Figure 1: The Browsing Agent performs tasks through browsing only, utilizing the accessibility tree to interact with webpages, achieving an average performance of 14.8% on WebArena. Without reliance on web browsing, the API-Based Agent performs tasks by making API calls and generating code without relying on web browsing, achieving an average accuracy of 29.2%. Dynamically interleaving web browsing and API calling, the Hybrid Agent executes either API calls or browsing actions, or combining both, achieving performance of 38.9%.

terleaves API calling and browsing, combining the power of both to complete each task.

We evaluated our API-Based and Hybrid Agents on WebArena, a benchmark for real-world web tasks [\(Zhou et al.,](#page-12-1) [2024\)](#page-12-1), and the results are shown in Figure [1.](#page-1-0) Our experiments revealed three key findings: (1) The API-Based Agent outperforms the Browsing Agent on WebArena by around 15% on average. (2) The API-Based Agent yields a higher success rate on websites with good API support (e.g., Gitlab) compared to those with limited API support (e.g., Reddit). This result underscores the importance of developing comprehensive API support for more accurate and efficient web task automation in the future. (3) The Hybrid Agent outperforms solely Browsing and solely API-Based Agents, further improving accuracy by 10% compared to the API-Based Agent. By dynamically interleaving approaches, the Hybrid Agent is able to provide more consistent and reliable outcomes.

In sum, our results suggest that allowing agents to interact with APIs, interfaces designed specifically for machines is often preferable or at least complementary to direct interaction with graphical interfaces designed for humans.

### 2 Background: Web Browsing

#### <span id="page-1-3"></span>2.1 The Web Browsing Task

Various benchmarks have been developed to evaluate web Browsing Agents. MiniWoB (Miniature World of Bits) is an early benchmark that provides simple web-based tasks such as clicking links or typing into forms, but it remains limited in complexity and realism [\(Shi et al.,](#page-11-7) [2017\)](#page-11-7). Mind2Web scales up these tasks, introducing more complex in-

teractions across websites, but it primarily focuses on basic web operations [\(Deng et al.,](#page-9-4) [2023\)](#page-9-4). WebArena [\(Zhou et al.,](#page-12-1) [2024\)](#page-12-1) advances web browsing benchmarks by creating reproducible sandboxes of various websites, such as managing repositories, posting online, performing online shopping, and planning trips using map services, while VisualWebArena extends WebArena to the vision modality [\(Koh et al.,](#page-10-4) [2024a\)](#page-10-4).

In this paper, we focus on WebArena tasks, which simulate real-world scenarios to evaluate an agent's ability to complete diverse web-based activities.[1](#page-1-1) WebArena tasks include interacting with platforms like Gitlab (to manage projects and repositories), Reddit (to browse and post content), e-commerce websites (for shopping), and mapping services (for trip planning) [\(Zhou et al.,](#page-12-1) [2024\)](#page-12-1). Task success is evaluated in three ways: (1) if the task requires producing specific outputs, agents' responses are checked for correctness; (2) for tasks involving changes to a website's state (e.g., adding items to shopping carts), success is verified by whether the state has changed as expected, such as ensuring the correct items have been added to the cart; and (3) if the task involves navigation, success is determined by whether the agent reaches the correct URL displaying the desired content.

#### <span id="page-1-2"></span>2.2 A Baseline Web Browsing Agent

While there are a wide variety of agents proposed for such web navigation tasks, in this work we build upon the WebArena baseline agent [\(Zhou](#page-12-1) [et al.,](#page-12-1) [2024\)](#page-12-1), which operates purely through web

<span id="page-1-1"></span><sup>1</sup>Notably, upon investigation of VisualWebArena we found that APIs for handling images were relatively limited, and hence we chose to experiment on text-only tasks in this paper.

```
How many commits
                                   goto `qitlab.com` (2) login with credentials
                               (3)
                                   click `allyproject` (4) click `Repository
did the user SaptakS
                                                    (6) No commits found -> scroll down
                               (5) click `Commits`
make to "allyproject"?
                               (7) No commits found -> scroll down ..... (15) No
                              commits found but no steps left,
                                                                   conclude 0 commits are
                              made by SaptakS.
                                           Web Browsing Traces. Failed after 15 steps
                               <execute ipython>
                               (1) r=requests.get('gitlab.com/api/allyproject/commits')
                               (2) commits=r.json()
                       (API
                               (3)len([c for c in commits if c['author'] == 'SaptakS'])
                               </execute_ipython>
                                              API Calling via Python requests library
```

Figure 2: The API-Based Agent often solves problems in fewer steps than the Browsing Agent. In this task, web browsing failed to solve the intent "find the number of commits the user *SaptakS* made to the repo *allyproject*" after 15 steps, while the API-Based Agent successfully completed the task with only three lines of code.

interaction by leveraging the accessibility tree<sup>2</sup>, a structure that exposes interactive elements like buttons, input fields, and hyperlinks (Yao et al., 2023; Gu et al., 2024). Each element of the accessibility tree is characterized by its functionality such as a hyperlink, its content, and specific web attributes (Liu et al., 2024b; He et al., 2024a; Lù et al., 2024). This exposes webpage elements in a hierarchical structure that is easy for agents to navigate (Samuel et al., 2024; Burns et al., 2022).

Agents based on this framework utilize an action space that simulates human browsing behavior, incorporating actions such as simulated clicks, form input, and navigation between pages (Liu et al., 2023; Song et al., 2024; Gur et al., 2024). Importantly, these agents maintain a comprehensive history of their previous actions, allowing them to contextualize their decision-making in past actions.

While agents utilizing this method can navigate arbitrary webpages and often perform well on simple layouts, challenges arise with the complexity of GUIs. Many large language models (LLMs) are not familiar with accessibility trees, which leads to difficulties in completing tasks that require numerous or complex interactions, resulting in lower accuracies (Liu et al., 2024a; Deng et al., 2023; Fu et al., 2024). These methods also struggle with content that need to be dynamically loaded or contents not immediately visible within the tree (Abramovich et al., 2024; Chen et al., 2024b; Lutz et al., 2024).

To give a motivating example, in Figure 2, we demonstrate a task where agents need to determine the number of commits made by the user *SaptakS* 

in a repository named *allyproject*. For each task, agents are given a fixed number of steps within which to complete the task. Using a traditional browsing approach, the agent follows a complex trajectory, starting with logging in, navigating to the correct project, accessing the repository, and finally attempting to view the list of commits. However, due to the large number of commits made by other users, the commits by *SaptakS* are located much further down on the webpage, requiring agents to scroll down many times. As a result, despite completing 15 steps, the Browsing Agent is unable to retrieve the required information.

#### **3 From Web Browsing to API Calling**

In contrast, API calling allows machines to directly communicate with web services, reducing operational complexity. In this section, we explore an API-based approach when performing web tasks.

#### 3.1 APIs and API Documentation

For websites that offer API support, pre-defined endpoints can be utilized to perform tasks efficiently. These APIs, following standardized protocols like REST<sup>3</sup>, allow interaction with web services through sending HTTP requests (e.g., GET, POST, PUT) and receiving structured data such as JSON objects<sup>4</sup> as responses. Websites often provide official documentation for the APIs, which can give guidance on how to utilize the APIs. Some documentation is provided as plain text, some in README <sup>5</sup> format, and some in OpenAPI

<span id="page-2-0"></span><sup>&</sup>lt;sup>2</sup>https://developer.mozilla.org/en-US/docs/Glossary/ Accessibility\_tree

<span id="page-2-2"></span>https://en.wikipedia.org/wiki/REST

<span id="page-2-3"></span><sup>4</sup>https://www.json.org/json-en.html

<span id="page-2-4"></span><sup>&</sup>lt;sup>5</sup>https://en.wikipedia.org/wiki/README

```
# Commits
           ## GET /api/{id}/commits: Get a list of commits in a project.
           | Attribute | Type | Description |
           | `id` | integer/string | The ID or path of the project. |
           | `since` | string | Only commits after or on this date. |
           | `until` | string | Only commits before or on this date.|
           Output: JSON containing all commits that meet the given criteria.
           <execute_ipython>
           requests.get('gitlab.com/api/a11yproject/commits')
           </execute_ipython>
           [ ......{
            "id": "ed37a2f2",
            "created_at": "2023-03-13T21:04:49.000-04:00",
            "title": "Update README.md",
            "message": "Update README.md",
            "author": "SaptakS",
           }]
   API 
Documentation
API Calling
JSON Output
```

Figure 3: An example of API documentation showing how to get commits of a project, the API call using a Python script to retrieve commits from a project repository, and the resulting JSON response.

YAML[6](#page-3-0) format. Figure [3](#page-3-1) shows an example of the Gitlab README documentation of GET /api/{id}/commits, documenting it's functionality, input arguments, and output types. For example, to retrieve all commits to a11yproject, one could use the Python requests library, by calling requests.get"gitlab.com/api/a11yproject/ commits"). This returns a JSON list containing all the commits to this repo, as shown in Figure [3.](#page-3-1)

### 3.2 Obtaining APIs for Agents

One important design decision is how to obtain APIs for agents to use. The way agents interact with APIs depends heavily on the availability of APIs and quality of API documentation. In this work, we acquired APIs by manually looking up official API documentation on a website, although this process could potentially be automated in the future. We classify the availability of APIs according to the following three scenarios:

Sufficient APIs and Documentation Many websites provide comprehensive API support and well-documented API documentation in YAML or README format. In this case, simply use the APIs/documentation as-is. Figure [3](#page-3-1) depicts an example of API documentation.

#### Sufficient APIs, Insufficient Documentation

There are some challenging situations where APIs exist but good documentation is not officially available. In such cases, additional steps may be required to obtain a list of accessible APIs. In this case, we inspected the frontend or backend code of

the website to extract undocumented API calls that can still be utilized by the agent. Then, based on the implementation of APIs of the website, leverage an LLM (GPT-4o[7](#page-3-2) ) to generate these YAML or README files. By prompting GPT-4o with the relevant implementation details of the APIs (for example, the implementation files of the APIs or example traces of API calls), we generate comprehensive documentation, including input parameters, expected outputs, and example API calls.

Insufficient APIs In the more challenging cases, where only minimal APIs are available, it may be necessary to create new APIs. These custom APIs allow agents to perform tasks that otherwise would require manual web browsing steps. In our case, this was necessary for 1 of 5 websites in the WebArena benchmark that we utilized, such as creating Reddit APIs discussed in Section [6.2.](#page-7-0)

#### <span id="page-3-4"></span>3.3 Using APIs in Agents

Once we have the APIs and documentation, we then need to provide methods to utilize them in agents. We utilize two different methods based on the size of the API documentation.

# One-Stage Documentation for Small API Sets

For websites with smaller numbers of APIs[8](#page-3-3) , we directly incorporate the full documentation into the prompt provided to the agent. This approach of directly feeding the full documentation worked well for websites with a limited number of API end-

<span id="page-3-0"></span><sup>6</sup> <https://yaml.org/>

<span id="page-3-3"></span><span id="page-3-2"></span><sup>7</sup> <https://openai.com/index/hello-gpt-4o/>

<sup>8</sup>We use a threshold of 100 APIs, but this could be adjusted depending on the supported language model context size.

points, as it allowed the agent to have immediate access to all the necessary information without the need for a more complex retrieval mechanism.

Two-Stage Documentation Retrieval for Large API Sets For websites with more APIs, providing the full documentation in the prompt is impractical due to size limitation of agent inputs. To address this, we use a two-stage documentation retrieval process, allowing access to only the needed information to keep the initial prompt concise.

In the first stage, the user prompt provides a task description, with a list of all available APIs along with a brief description of each. For example, {"GET /api/{id}/commits": "List commits in a project"}. This initial summary helps in understanding the scope of all the available APIs while staying within the prompt size constraints.

In the second stage, if the model determines that it needs detailed information about one or more specific API endpoints, it can use a tool named get\_api\_documentation, which maintains a dictionary that maps each API to its documentation respectively. The dictionary is generated using Python pattern match to retrieve substrings related to each endpoints. This tool is able to search the dictionary and retrieve the full README or YAML documentation for any given endpoint with the endpoint's identifier. The resulting documentation might include the input parameters, output formats, and examples of how to interact with the endpoint. For example, to retrieve the documentation for the API GET /api/id/commits, the agent would call get\_api\_documentation("GET /api/id/commits"). An example returned API documentation is the documentation in Figure [3.](#page-3-1)

This retrieval method allows the agent to make flexible and informed decisions to perform tasks. If the agent finds that an API does not meet its needs or if it encounters an error, it can easily retrieve the documentation for a different API by calling the tool again. This dynamic approach promotes adaptability and minimizes the risk of incorrect API usage when the number of APIs available is large. The prompt can be found in Appendix [A.5.](#page-15-0)

### 4 Hybrid Browsing+API Calling Agents

We have proposed API-based methods for handling web tasks, but the question arises: given the benefits of API calling, should we discard browsing altogether? The most obvious bottleneck is that not all websites offer good API support. Some

platforms offer limited or poorly documented APIs (e.g. no API for shopping on Amazon[9](#page-4-0) ), forcing agents to rely on browsing to complete tasks.

To deal with these situations, we propose a hybrid methods that integrates both browsing and API calling, and developed a Hybrid Agent capable of dynamically interleaving API calls and web browsing based on task requirements and the available resources. Specifically, for each task, the agent is given the fixed step budget within which it has to finish the task. *In each step of a task*, the agent could either (1) communicate with humans in natural language to ask for clarification, or 2) generate and executes Python code which could include performing API calling, or 3) performs web browsing actions. The Hybrid Agent could choose freely among these options, depending on the agent's confidence in which method is the best for each step.

Ideally, for websites with good API support, the Hybrid Agent can utilize well-documented APIs to perform tasks more efficiently than it could through only browsing; for websites with limited API support or poor documentation, the Hybrid Agent could rely more on browsing. We find that enabling it to interleave API calling and web browsing boosts task performance (see Section [6\)](#page-6-0).

Prompt Construction The Hybrid Agent's prompt construction extends upon the API-Based Agent by incorporating both API and webbrowsing documentation. Similar to the API-Based Agent, the Hybrid Agent is provided with a description of available API calls as discussed in Section [3.3.](#page-3-4) In addition, the Hybrid Agent receives a detailed specification of the web-browsing actions, which mirrors the information given to the Browsing Agent described in Section [2.2,](#page-1-2) including a breakdown of all potential browser interactions. It also maintains a history of all its prior steps such that the agent could make more informed actions. The prompt can be found in Appendix [A.6.](#page-16-0)

### 5 Experimental Setup

### 5.1 Dataset Description

We utilized WebArena [\(Zhou et al.,](#page-12-1) [2024\)](#page-12-1) as the primary evaluation benchmark. WebArena is a comprehensive benchmark designed for real-world web tasks, providing a diverse set of websites that simulate various online interactions, allowing comprehensive evaluation of agents' abilities to handle

<span id="page-4-0"></span><sup>9</sup> <https://www.amazon.com>

both API calling and web browsing across varied web settings. WebArena mainly includes five websites, each with various intents representing different tasks: Gitlab, Map, Shopping, Shopping Admin, Reddit, and Multi-Site tasks. A detailed descriptions of the tasks is in Appendix [A.2.](#page-13-0)

### <span id="page-5-4"></span>5.2 API Statistics for WebArena Sites

The API support for WebArena websites can be categorized into three levels: good, medium, and poor. APIs' availability, functionality, and documentation, as described in Table [1,](#page-5-0) play a crucial role in the efficiency and flexibility of our agents[10](#page-5-1) .

<span id="page-5-0"></span>

| Sites   | Gitlab | Map  | Shop | Admin | Reddit |
|---------|--------|------|------|-------|--------|
| # APIs  | 988    | 53   | 556  | 556   | 31‡    |
| Quality | Good   | Good | Fair | Fair  | Poor   |

Table 1: Number of endpoints, and quality of API and documentation for WebArena websites. ‡ See Section [6.2](#page-7-0) for more discussions.

#### 5.2.1 Good API Support

Gitlab Gitlab supports 988 endpoints, which offer extensive coverage across a wide range of functionalities, including repositories, commits, and users. This comprehensive API support allows for effective interaction in most WebArena tasks, making Gitlab one of the best-supported platforms in terms of API availability.

Map The Map website offers 53 endpoints. Despite the smaller number of endpoints, the APIs available are well-documented and cover most of the essential WebArena use cases.

#### 5.2.2 Medium API Support

Shopping and Shopping Admin The Shopping and Shopping Admin websites share a common set of 556 APIs, which provide a reasonable level of support for common shopping tasks. However, some features, such as adding items to wish lists, are absent, and thus these tasks must be handled via browsing. Despite this, the documentation is fairly detailed. Overall, API calling is a solid, though not exhaustive, solution for handling shopping tasks.

### 5.2.3 Poor API Support

Reddit The WebArena Reddit is a self-hosted limited clone of the actual Reddit[11](#page-5-2) with only 31 endpoints. It offers minimal API support and no documentation, making it the least API-friendly site in WebArena. Many critical functionalities such as searching posts are missing, significantly hampering task execution on Reddit, highlighting the need for a hybrid browsing+API approach.

### 5.3 API Implementation Details

We follow the methodologies discussed in Section [3.3](#page-3-4) to provide APIs to agents. Appendix [A.3](#page-13-1) contains the sources of the public API documentations.

# 5.3.1 One-Stage Documentation for Small API Sets

For websites with fewer than 100 API endpoints, namely the Map and Reddit websites, we directly provide the full documentation to the agent.

Map The README documentation was inputted directly from the public API documentation.

Reddit Since there was no pre-existing documentation for the APIs, we leveraged GPT-4o[12](#page-5-3) itself to generate these README files. By prompting GPT-4o with a file containing all implementations of the API endpoints, we generated a README documentation, including input parameters, expected outputs, and example API calls.

### 5.3.2 Two-Stage Documentation Retrieval for Large API Sets

For websites with more than 100 endpoints, namely GitLab, Shopping, and Shopping Admin, we employ a two-stage documentation retrieval process.

We obtained Gitlab README documentations from the official website. For Shopping and Shopping Admin, the documentation is provided as OpenAPI specification, structured in YAML format.

#### 5.4 Evaluation Framework

We employed OpenHands as our evaluation framework to facilitate the development and testing of our agents [\(Wang et al.,](#page-11-11) [2024c\)](#page-11-11). OpenHands is an open-source platform designed for creating and evaluating AI agents that interact with both software and web environments, making it an appropriate infrastructure for our proposed methods. The OpenHands architecture supports various interfaces for agents to interact with. Moreover, this framework allows agents to keep a detailed record of past actions in the prompt, enabling agents to execute actions in a way that is consistent with earlier steps. For coding tasks, it implements an agent based on CodeAct [\(Wang et al.,](#page-11-12) [2024a\)](#page-11-12) that incorporates a sandboxed bash operating system and Jupyter

<span id="page-5-1"></span><sup>10</sup>See Appendix [A.3](#page-13-1) for where to find the WebArena APIs.

<span id="page-5-2"></span><sup>11</sup>See Appendix [A.3](#page-13-1) for more explanations.

<span id="page-5-3"></span><sup>12</sup><https://openai.com/index/hello-gpt-4o/>

<span id="page-6-3"></span>

| Agents                            | Gitlab | Map  | Shopping | Admin | Reddit | Multi | AVG. |
|-----------------------------------|--------|------|----------|-------|--------|-------|------|
| WebArena Base (Zhou et al., 2024) | 15.0   | 15.6 | 13.9     | 10.4  | 6.6    | 8.3   | 12.3 |
| AutoEval (Pan et al., 2024)       | 25.0   | 27.5 | 39.6     | 20.9  | 20.8   | 16.7  | 26.9 |
| AWM (Wang et al., 2024e)          | 35.0   | 42.2 | 32.1     | 29.1  | 54.7   | 18.8  | 35.5 |
| †<br>SteP (Sodhi et al., 2024)    | 32.2   | 31.2 | 50.8     | 23.6  | 57.5   | 10.4  | 36.5 |
| Browsing Agent                    | 12.8   | 20.2 | 10.2     | 22.0  | 10.4   | 10.4  | 14.8 |
| API-Based Agent                   | 43.9   | 45.4 | 25.1     | 20.3  | 18.9‡  | 8.3   | 29.2 |
| Hybrid Agent                      | 44.4   | 45.9 | 25.7     | 41.2  | 51.9‡  | 16.7  | 38.9 |

Table 2: Agents' performances on WebArena. †Note that SteP uses prompts inspired specifically by WebArena tasks, while other agents are task-agnostic. Our Hybrid Agent achieve the highest accuracy among these agents. ‡ We report these results using a set of APIs introduced by the authors to mimic the official Reddit website, constructed task-agnostically without access to WebArena tasks. See Section [6.2](#page-7-0) for more discussions.

IPython[13](#page-6-1) environments, enabling Python code execution. Additionally, it includes a BrowsingAgent Browsing Agent that focuses solely on web navigation. This agent operates within a Chromium web browser powered by Playwright[14](#page-6-2), utilizing a comprehensive set of browser actions defined by BrowserGym [\(Drouin et al.,](#page-10-14) [2024b\)](#page-10-14). However, while the Browsing Agent can browse websites, and the CodeActAgent make API calls and execute code, there is not an agent that can natively do both. Given this base, we developed two varieties of agents for API-based solving of web tasks.

API-Based Agent Our API-Based Agent essentially uses the CodeAct architecture [\(Wang et al.,](#page-11-12) [2024a\)](#page-11-12). In addition to the basic CodeAct framework, we tailor the agent for API calling by adding specialized instructions and examples that guide its understanding and using of APIs. At each step, the agent could utilize all previous actions to make informed selection of actions. The prompt of the API-Based Agent is included in the Appendix [A.5.](#page-15-0)

Hybrid Browsing/API Calling Agent In addition to the API-Based Agent, we developed a Hybrid Agent that integrates Chromium web browsing functionalities powered by Playwright into the existing API-Based Agent framework. This Hybrid Agent is provided the prompt describing both the APIs and the browsing actions, allowing for free transitions between API calling and web browsing. At each step, the agent can utilize the current state of the browser, all previous actions taken by the agent, and the results of those actions to determine the next course of action. The prompt of the Hybrid Agent is included in the Appendix [A.6.](#page-16-0)

For the Browsing, API-Based, and Hybrid Agents, we utilized GPT-4o as the base LLM. However, this could be easily changed to other LLMs.

### <span id="page-6-0"></span>6 Results

### 6.1 Main Results

The main results of our evaluation, as summarized in Table [2,](#page-6-3) demonstrate the performance of three different agents across WebArena websites.

The API-Based Agent consistently achieved higher scores on most websites compared to the Browsing Agent. This agent's strong performance is attributed to its specialized design for API calling, enabling it to efficiently interact with websites and complete tasks with no reliance on browsing.

In contrast, the Browsing Agent, designed solely for navigating web interfaces, demonstrated significantly lower performance across most domains. It achieved its best scores on Shopping Admin and Map, but struggled more on the other websites.

The Hybrid Agent, integrating both API calling and web browsing, outperformed the Browsing and API-Based Agents on all websites. The agent's ability to interleave API calling and web browsing proved beneficial. API calling delivers high performance for web tasks when well-supported APIs are available, while web browsing serves as a backup when API endpoints are unavailable or incomplete. Even if the website provides comprehensive APIs, there might be corner cases where APIs are not supportive. Thus, relying on web browsing is still needed for tasks that would otherwise fail through API-only interactions. Table [3](#page-7-1) show the frequency of each action type of the Hybrid Agent: it chooses to do both Browsing and API in 77.7% of WebArena tasks, and it shows higher accuracy when choosing API only and API+browsing. More de-

<span id="page-6-1"></span><sup>13</sup><https://ipython.org>

<span id="page-6-2"></span><sup>14</sup><https://playwright.dev/>

tailed analysis on action types, steps and cost and case studies are in Appendix A.4 and 6.4.

<span id="page-7-1"></span>

| Actions       | Frequency (%) | Accuracy (%) |
|---------------|---------------|--------------|
| Browsing only | 14.3          | 25.0         |
| API only      | 8.0           | 40.0         |
| Browsing+API  | 77.7          | 42.0         |

Table 3: The left column specifies the type of action taken by the Hybrid Agent; the middle column shows the percentage of actions selected among all WebArena tasks; and the right column indicates the accuracy of the Hybrid Agent for each action type.

Overall, the results indicate that the Hybrid Agent is the most effective for handling diverse tasks in WebArena, particularly in environments that require a blend of API and browsing actions. The API-Based Agent excels in tasks that are primarily API-driven, while the Browsing Agent is more suitable for simple navigation tasks but lacks the versatility needed for more complex scenarios.

#### <span id="page-7-0"></span>**6.2 Does API Quality Matter?**

Yes, API quality does significantly impact the performance of agents. High quality APIs provide comprehensive and well-documented endpoints that enable agents to interact accurately and efficiently with websites. With comprehensive API support, the API-Based Agent is able to tackle more tasks through API calling, while the Hybrid Agent rely less on browsing; on the other hand, clear and detailed documentation allows agents to use APIs effectively, ensuring that requests are accurate, and minimizing potential errors in task execution. For example, Gitlab and Map, with the best API support as mentioned in Section 5.2, demonstrate highest task completion accuracies among websites by the API-Based and Hybrid Agent.

Conversely, low-quality APIs, characterized by incomplete functionality or ambiguous documentation, can significantly degrade performance. In such cases, the absence of necessary endpoints may prevent the API-Based Agent from completing tasks. Moreover, poorly documented APIs can result in misusing parameters and headers, further reducing the effectiveness of the agent. This highlights the importance for websites to maintain comprehensive and well-documented API support.

An illustrative example of this is the case of Reddit, where the initial performance of the API-Based Agent was suboptimal due to limited API availability. As depicted in Table 4, initially, Reddit

<span id="page-7-3"></span>

| Number of Endpoints | 18   | 31    |
|---------------------|------|-------|
| Accuracy on Reddit  | 9.4% | 18.9% |

Table 4: Change in performance of the API-Based Agent on Reddit upon incorporating new APIs.

offered only 18 APIs, lacking the major functionality that common online forums have, such as post voting. Recognizing this limitation, we manually introduced 13 additional APIs including one API on post voting, with our best effort trying to mimic the official Reddit website. This results in a marked improvement in the API-Based Agent's performance, underscoring the direct correlation between the availability of high-quality APIs and the average performance of the API-Based Agent.

<span id="page-7-4"></span>![](_page_7_Figure_11.jpeg)

Figure 4: Error analysis on 100 WebArena tasks.

#### 6.3 Error Analysis

We randomly sampled 100 tasks from WebArena and performed error analysis on the API-Based Agent. Figure 4 shows the distribution of error categories among these 100 tasks. We found that 33% of the tasks are correctly performed with only API calling, 50% are unsolvable with solely APIs, 6% are incorrect due to incorrect task understanding, and 11% are incorrect due to error in calling APIs such as mal-formatting and wrong input. In other words, among the 50 API solvable tasks, 66% are performed correctly by the API-Based Agent. This showcases the strong capability of the API-Based Agent when given sufficient APIs to solve the task.

Additionally, the average API calls required to solve API solvable tasks are 2.1 API calls, demonstrating how API calling could reduce operational complexity for web tasks. Although the API-Based Agent took an average of 7.8 steps to complete WebArena tasks, most of the steps were taken to retrieve API documentation, resolve errors from it's previous generations, or verify it's outputs.

#### <span id="page-7-2"></span>6.4 Case Studies

We analyze two contrasting instances as shown in Figure 5 and Figure 6, where the Hybrid Agent

```
(1) goto `admin.com` (2) login with 
credentials (3) click `store` (4) click
`products` (5) search `Sybil running 
short` (6) iteratively click products on 
search result and see if it's the product 
wanted (7) click review 1 (8) if negative, 
then delete (9) click review 2 ......
the product Sybil running short.
```

<span id="page-8-0"></span>Task: delete all negative reviews for

```
(1) GET `/api/products` to retrieve all 
products (2) get the product URL from 
`Sybil running short` product in Python 
(3) go to product URL (4)click review 1 
(5) if negative, then delete (6) click
review 2 ...... 
  Web browsing has complex traces and lower success rate
API Calling fails due to no useful API available to solve the task
 No API for checking and deleting reviews.
```

Hybrid Agent simplifies task traces and solves the task

Figure 5: The Hybrid Agent succeeds while the Browsing Agent and API-Based Agent both fail

and API-Based Agent exhibited different levels of performance on WebArena tasks. These case studies highlight the strengths and weaknesses of each agent, demonstrating scenarios where hybrid browsing outperforms API-only or browsing-only approaches, as well as cases where the API-Based Agent excels over the hybrid method.

Case 1 One example where the Hybrid Agent succeeded, while both the API-Based and Browsing Agents failed, involved a task from the Shopping Admin domain. The query was to "delete all negative reviews for Sybil running short", a product listed in the shopping admin interface. In this instance, the API-Based Agent failed because no relevant API endpoints were available for retrieving or deleting reviews. Similarly, the Browsing Agent failed, as completing this task purely through web navigation required too many steps, as depicted in Figure [5.](#page-8-0) This complexity made the task challenging for an agent relying solely on web interactions. However, the Hybrid Agent successfully completed the task by leveraging both API and browsing functionalities. An example trace of the Hybrid Agent shown in Figure [5.](#page-8-0) This case highlights the Hybrid Agent's ability to efficiently combine API calls with web interactions, allowing it to tackle complex multi-step tasks that would be difficult or impossible for solely browsing or solely API-Based Agents.

Case 2 Conversely, there are instances where the API-Based Agent outperforms the Hybrid Agent.

```
Task: tell me the email of the contributor 
who has the most commits to `ai`.
```

```
(1) goto `gitlab.com` (2) login with 
credentials (3) click `projects` (4) click
`ai` (5) click `Repository` (6) click
`Commits` (7) For each contributor, count
commit number ...... (15) did not find all 
commits in 15 steps
```

Web browsing has complex traces and lower success rate r = requests.get('/api/ai/contributors') email = r.json()[0]['email']

API Calling successfully completes the task after one API call

```
(1) goto `gitlab.com` (2) login with 
credentials (3) click `projects` (4) click
`ai` (5) click `Repository` (6) click
`Commits` (7) For each contributor, count
commit number ...... (15) did not find all 
commits in 15 steps
```

Hybrid Agent fails the task as it only attempts browsing

Figure 6: The API-Based Agent succeeds while the Browsing Agent and the Hybrid Agent fails.

One such case occurred in the GitLab website, where the task was to "tell me the email address of the contributor who has the most commits to ai." The API-Based Agent successfully completed this task by utilizing the GET /api/id/contributors API endpoint to retrieve the contributor with the highest number of commits and their associated email address. On the other hand, the Hybrid Agent attempted to solve the task through browsing but encountered significant challenges. Accessing this information through web browsing required navigating GitLab's interface, locating the correct repository and branch, and identifying the top contributor manually, a task that might be too difficult to perform through web navigation alone. As a result, both the Browsing Agent and the Hybrid Agent failed to complete the task. This case demonstrates an example where API access provides a more straightforward solution than browsing in contexts requiring structured data retrieval.

# 7 Conclusion

In this paper, we propose new web agents that use APIs instead of traditional browsers. We find that API-Based Agents outperform Browsing Agents, especially on websites with good API support. Thus we further propose Hybrid Agents capable of interleaving API calling and browsing that empirically outperforms agents that only use one of the two interfaces.

# 8 Limitations

Evaluation Benchmark In this paper, we evaluate web agents exclusively on WebArena tasks. While WebArena offers realistic and diverse challenges, the number and variety of tasks may be limited. Other benchmarks, such as Webshop [\(Yao et al.,](#page-11-15) [2022\)](#page-11-15), MiniWoB [\(Shi et al.,](#page-11-7) [2017\)](#page-11-7), Mind2Web [\(Deng et al.,](#page-9-4) [2023\)](#page-9-4), WebVoyager [\(He](#page-10-15) [et al.,](#page-10-15) [2024b\)](#page-10-15), and VisualWebArena [\(Koh et al.,](#page-10-4) [2024a\)](#page-10-4), provide alternative valuable evaluation platforms. However, as discussed in Section [2.1,](#page-1-3) WebArena aligns more closely with real-world scenarios and our use case, while other benchmarks lack support for API calling. For example, VisualWebArena is less applicable to our study because WebArena APIs lack support for interacting with images, a core component of VisualWebArena tasks.

API Availability A key limitation of API-Based Agents is the inconsistent availability and coverage of APIs across websites. Even platforms with extensive API ecosystems, such as GitLab, may lack support for specific functionalities (e.g., retrieving a user's official username from a displayed name), leading to edge cases where API-Based Agents are unable to complete tasks due to incomplete API support. However, advancements in techniques like Automatic Web API Mining (AWM) [\(Wang](#page-11-13) [et al.,](#page-11-13) [2024e\)](#page-11-13) could potentially address this limitation by automatically generating APIs for unsupported tasks, reducing reliance on manual API creation.

Incorporating APIs Unlike Browsing Agents, which can adapt to new websites without manual intervention, the API-Based Agent requires additional effort to integrate the necessary APIs documentation to the action space of the agent for each website. This manual integration process increases complexity, particularly when the agent must support a wide range of websites, limiting scalability compared to agents that rely solely on web browsing for interactions. However, future advancements could explore automatically inducing APIs using methods such as Agent Workflow Memory (AWM) [\(Wang et al.,](#page-11-13) [2024e\)](#page-11-13) and self-improving [\(Zheng](#page-12-5) [et al.,](#page-12-5) [2025\)](#page-12-5). These methods could identify and generate API calls for websites lacking formal API support, further expanding the applicability and efficiency of API-Based Agents. By automating the discovery and utilization of APIs, we envision even

more robust agents capable of handling diverse web tasks without reliance on interaction through browsing.

### References

<span id="page-9-6"></span>Talor Abramovich, Meet Udeshi, Minghao Shao, Kilian Lieret, Haoran Xi, Kimberly Milner, Sofija Jancheska, John Yang, Carlos E. Jimenez, Farshad Khorrami, Prashanth Krishnamurthy, Brendan Dolan-Gavitt, Muhammad Shafique, Karthik Narasimhan, Ramesh Karri, and Ofir Press. 2024. [Enigma: En](https://arxiv.org/abs/2409.16165)[hanced interactive generative model agent for ctf chal](https://arxiv.org/abs/2409.16165)[lenges.](https://arxiv.org/abs/2409.16165) *Preprint*, arXiv:2409.16165.

<span id="page-9-3"></span>S.R.K. Branavan, Harr Chen, Luke Zettlemoyer, and Regina Barzilay. 2009. [Reinforcement learning for](https://aclanthology.org/P09-1010) [mapping instructions to actions.](https://aclanthology.org/P09-1010) In *Proceedings of the Joint Conference of the 47th Annual Meeting of the ACL and the 4th International Joint Conference on Natural Language Processing of the AFNLP*, pages 82–90, Suntec, Singapore. Association for Computational Linguistics.

<span id="page-9-5"></span>Andrea Burns, Deniz Arsan, Sanjna Agrawal, Ranjitha Kumar, Kate Saenko, and Bryan A. Plummer. 2022. [A dataset for interactive vision-language navigation](https://doi.org/10.1007/978-3-031-20074-8_18) [with unknown command feasibility.](https://doi.org/10.1007/978-3-031-20074-8_18) In *Computer Vision – ECCV 2022: 17th European Conference, Tel Aviv, Israel, October 23–27, 2022, Proceedings, Part VIII*, page 312–328, Berlin, Heidelberg. Springer-Verlag.

<span id="page-9-2"></span>Alan Chan, Carson Ezell, Max Kaufmann, Kevin Wei, Lewis Hammond, Herbie Bradley, Emma Bluemke, Nitarshan Rajkumar, David Krueger, Noam Kolt, et al. 2024. Visibility into ai agents. In *The 2024 ACM Conference on Fairness, Accountability, and Transparency*, pages 958–973.

<span id="page-9-0"></span>Weize Chen, Ziming You, Ran Li, Yitong Guan, Chen Qian, Chenyang Zhao, Cheng Yang, Ruobing Xie, Zhiyuan Liu, and Maosong Sun. 2024a. Internet of agents: Weaving a web of heterogeneous agents for collaborative intelligence. *arXiv preprint arXiv:2407.07061*.

<span id="page-9-7"></span>Zehui Chen, Kuikun Liu, Qiuchen Wang, Wenwei Zhang, Jiangning Liu, Dahua Lin, Kai Chen, and Feng Zhao. 2024b. [Agent-FLAN: Designing data](https://doi.org/10.18653/v1/2024.findings-acl.557) [and methods of effective agent tuning for large lan](https://doi.org/10.18653/v1/2024.findings-acl.557)[guage models.](https://doi.org/10.18653/v1/2024.findings-acl.557) In *Findings of the Association for Computational Linguistics ACL 2024*, pages 9354– 9366, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.

<span id="page-9-4"></span>Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samuel Stevens, Boshi Wang, Huan Sun, and Yu Su. 2023. [Mind2web: Towards a generalist agent for the](https://arxiv.org/abs/2306.06070) [web.](https://arxiv.org/abs/2306.06070) *Preprint*, arXiv:2306.06070.

<span id="page-9-1"></span>Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H Laradji, Manuel Del Verme, Tom Marty, Léo Boisvert, Megh Thakkar, Quentin Cappart, David

- Vazquez, et al. 2024a. Workarena: How capable are web agents at solving common knowledge work tasks? *arXiv preprint arXiv:2403.07718*.
- <span id="page-10-14"></span>Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, Léo Boisvert, Megh Thakkar, Quentin Cappart, David Vazquez, Nicolas Chapados, and Alexandre Lacoste. 2024b. [Workarena: How capable are web agents at](https://arxiv.org/abs/2403.07718) [solving common knowledge work tasks?](https://arxiv.org/abs/2403.07718) *Preprint*, arXiv:2403.07718.
- <span id="page-10-18"></span>Yu Du, Fangyun Wei, and Hongyang Zhang. 2024. Anytool: Self-reflective, hierarchical agents for largescale api calls. *arXiv preprint arXiv:2402.04253*.
- <span id="page-10-3"></span>Zane Durante, Bidipta Sarkar, Ran Gong, Rohan Taori, Yusuke Noda, Paul Tang, Ehsan Adeli, Shrinidhi Kowshika Lakshmikanth, Kevin Schulman, Arnold Milstein, Demetri Terzopoulos, Ade Famoti, Noboru Kuno, Ashley Llorens, Hoi Vo, Katsu Ikeuchi, Li Fei-Fei, Jianfeng Gao, Naoki Wake, and Qiuyuan Huang. 2024. [An interactive agent foun](https://arxiv.org/abs/2402.05929)[dation model.](https://arxiv.org/abs/2402.05929) *Preprint*, arXiv:2402.05929.
- <span id="page-10-12"></span>Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. 2024. [Autoguide: Automated gener](https://openreview.net/forum?id=Zu1MihB661)[ation and selection of context-aware guidelines for](https://openreview.net/forum?id=Zu1MihB661) [large language model agents.](https://openreview.net/forum?id=Zu1MihB661) In *ICML 2024 Workshop on LLMs and Cognition*.
- <span id="page-10-6"></span>Yu Gu, Yiheng Shu, Hao Yu, Xiao Liu, Yuxiao Dong, Jie Tang, Jayanth Srinivasa, Hugo Latapie, and Yu Su. 2024. [Middleware for llms: Tools are instrumen](https://arxiv.org/abs/2402.14672)[tal for language agents in complex environments.](https://arxiv.org/abs/2402.14672) *Preprint*, arXiv:2402.14672.
- <span id="page-10-10"></span>Izzeddin Gur, Hiroki Furuta, Austin V Huang, Mustafa Safdari, Yutaka Matsuo, Douglas Eck, and Aleksandra Faust. 2024. [A real-world webagent with plan](https://openreview.net/forum?id=9JQtrumvg8)[ning, long context understanding, and program syn](https://openreview.net/forum?id=9JQtrumvg8)[thesis.](https://openreview.net/forum?id=9JQtrumvg8) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-10-8"></span>Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, and Dong Yu. 2024a. [WebVoyager: Building an end-to](https://doi.org/10.18653/v1/2024.acl-long.371)[end web agent with large multimodal models.](https://doi.org/10.18653/v1/2024.acl-long.371) In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 6864–6890, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-10-15"></span>Hongliang He, Wenlin Yao, Kaixin Ma, Wenhao Yu, Yong Dai, Hongming Zhang, Zhenzhong Lan, and Dong Yu. 2024b. Webvoyager: Building an end-toend web agent with large multimodal models. *arXiv preprint arXiv:2401.13919*.
- <span id="page-10-5"></span>Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxuan Zhang, Juanzi Li, Bin Xu, Yuxiao Dong, Ming Ding, and Jie Tang. 2023. [Cogagent:](https://arxiv.org/abs/2312.08914) [A visual language model for gui agents.](https://arxiv.org/abs/2312.08914) *Preprint*, arXiv:2312.08914.

- <span id="page-10-2"></span>Qiuyuan Huang, Naoki Wake, Bidipta Sarkar, Zane Durante, Ran Gong, Rohan Taori, Yusuke Noda, Demetri Terzopoulos, Noboru Kuno, Ade Famoti, Ashley Llorens, John Langford, Hoi Vo, Li Fei-Fei, Katsu Ikeuchi, and Jianfeng Gao. 2024. [Po](https://arxiv.org/abs/2403.00833)[sition paper: Agent ai towards a holistic intelligence.](https://arxiv.org/abs/2403.00833) *Preprint*, arXiv:2403.00833.
- <span id="page-10-4"></span>Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Russ Salakhutdinov, and Daniel Fried. 2024a. [VisualWebArena: Evaluating multimodal](https://doi.org/10.18653/v1/2024.acl-long.50) [agents on realistic visual web tasks.](https://doi.org/10.18653/v1/2024.acl-long.50) In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 881–905, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-10-17"></span>Jing Yu Koh, Stephen McAleer, Daniel Fried, and Ruslan Salakhutdinov. 2024b. Tree search for language model agents. *arXiv preprint arXiv:2407.01476*.
- <span id="page-10-16"></span>Hanyu Lai, Xiao Liu, Iat Long Iong, Shuntian Yao, Yuxuan Chen, Pengbo Shen, Hao Yu, Hanchen Zhang, Xiaohan Zhang, Yuxiao Dong, and Jie Tang. 2024. Autowebglm: A large language model-based web navigating agent. In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, pages 5295—-5306.
- <span id="page-10-1"></span>Yang Li, Jiacong He, Xin Zhou, Yuan Zhang, and Jason Baldridge. 2020. [Mapping natural language instruc](https://doi.org/10.18653/v1/2020.acl-main.729)[tions to mobile UI action sequences.](https://doi.org/10.18653/v1/2020.acl-main.729) In *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, pages 8198–8210, Online. Association for Computational Linguistics.
- <span id="page-10-0"></span>Evan Zheran Liu, Kelvin Guu, Panupong Pasupat, and Percy Liang. 2018. [Reinforcement learning on web](https://openreview.net/forum?id=ryTp3f-0-) [interfaces using workflow-guided exploration.](https://openreview.net/forum?id=ryTp3f-0-) In *International Conference on Learning Representations*.
- <span id="page-10-11"></span>Junpeng Liu, Yifan Song, Bill Yuchen Lin, Wai Lam, Graham Neubig, Yuanzhi Li, and Xiang Yue. 2024a. [Visualwebbench: How far have multimodal llms](https://arxiv.org/abs/2404.05955) [evolved in web page understanding and grounding?](https://arxiv.org/abs/2404.05955) *Preprint*, arXiv:2404.05955.
- <span id="page-10-9"></span>Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and Jie Tang. 2023. Agentbench: Evaluating llms as agents. *arXiv preprint arXiv: 2308.03688*.
- <span id="page-10-7"></span>Xiao Liu, Tianjie Zhang, Yu Gu, Iat Long Iong, Yifan Xu, Xixuan Song, Shudan Zhang, Hanyu Lai, Xinyi Liu, Hanlin Zhao, et al. 2024b. Visualagentbench: Towards large multimodal models as visual foundation agents. *arXiv preprint arXiv:2408.06327*.
- <span id="page-10-13"></span>Michael Lutz, Arth Bohra, Manvel Saroyan, Artem Harutyunyan, and Giovanni Campagna. 2024. [Wilbur: Adaptive in-context learning for robust and](https://arxiv.org/abs/2404.05902) [accurate web agents.](https://arxiv.org/abs/2404.05902) *Preprint*, arXiv:2404.05902.

- <span id="page-11-8"></span>Xing Han Lù, Zdenek Kasner, and Siva Reddy. 2024. ˇ [Weblinx: Real-world website navigation with multi](https://arxiv.org/abs/2402.05930)[turn dialogue.](https://arxiv.org/abs/2402.05930) *Preprint*, arXiv:2402.05930.
- <span id="page-11-4"></span>Michael Meng, Stephanie Steinhardt, and Andreas Schubert. 2018. Application programming interface documentation: What do software developers want? *Journal of Technical Writing and Communication*, 48(3):295–330.
- <span id="page-11-2"></span>Jiayi Pan, Yichi Zhang, Nicholas Tomlin, Yifei Zhou, Sergey Levine, and Alane Suhr. 2024. [Autonomous](https://openreview.net/forum?id=NPAQ6FKSmK) [evaluation and refinement of digital agents.](https://openreview.net/forum?id=NPAQ6FKSmK) *Conference On Language Modeling (COLM)*.
- <span id="page-11-1"></span>Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. 2023. Gorilla: Large language model connected with massive apis. *arXiv preprint arXiv:2305.15334*.
- <span id="page-11-17"></span>Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al. 2023. Toolllm: Facilitating large language models to master 16000+ real-world apis. *arXiv preprint arXiv:2307.16789*.
- <span id="page-11-0"></span>Christopher Rawles, Alice Li, Daniel Rodriguez, Oriana Riva, and Timothy P Lillicrap. 2023. [An](https://openreview.net/forum?id=j4b3l5kOil)[droidinthewild: A large-scale dataset for android de](https://openreview.net/forum?id=j4b3l5kOil)[vice control.](https://openreview.net/forum?id=j4b3l5kOil) In *Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track*.
- <span id="page-11-9"></span>Vinay Samuel, Henry Peng Zou, Yue Zhou, Shreyas Chaudhari, Ashwin Kalyan, Tanmay Rajpurohit, Ameet Deshpande, Karthik Narasimhan, and Vishvak Murahari. 2024. [Personagym: Evaluating persona](https://arxiv.org/abs/2407.18416) [agents and llms.](https://arxiv.org/abs/2407.18416) *Preprint*, arXiv:2407.18416.
- <span id="page-11-20"></span>Haiyang Shen, Yue Li, Desong Meng, Dongqi Cai, Sheng Qi, Li Zhang, Mengwei Xu, and Yun Ma. 2024. [Shortcutsbench: A large-scale real-world benchmark](https://arxiv.org/abs/2407.00132) [for api-based agents.](https://arxiv.org/abs/2407.00132) *Preprint*, arXiv:2407.00132.
- <span id="page-11-7"></span>Tianlin Shi, Andrej Karpathy, Linxi Fan, Jonathan Hernandez, and Percy Liang. 2017. [World of bits: An](https://proceedings.mlr.press/v70/shi17a.html) [open-domain platform for web-based agents.](https://proceedings.mlr.press/v70/shi17a.html) In *Proceedings of the 34th International Conference on Machine Learning*, volume 70 of *Proceedings of Machine Learning Research*, pages 3135–3144. PMLR.
- <span id="page-11-14"></span>Paloma Sodhi, SRK Branavan, Yoav Artzi, and Ryan McDonald. 2024. Step: Stacked llm policies for web actions. In *First Conference on Language Modeling*.
- <span id="page-11-10"></span>Yifan Song, Da Yin, Xiang Yue, Jie Huang, Sujian Li, and Bill Yuchen Lin. 2024. [Trial and error:](https://doi.org/10.18653/v1/2024.acl-long.409) [Exploration-based trajectory optimization of LLM](https://doi.org/10.18653/v1/2024.acl-long.409) [agents.](https://doi.org/10.18653/v1/2024.acl-long.409) In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 7584–7600, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-11-19"></span>Xunzhu Tang, Kisub Kim, Yewei Song, Cedric Lothritz, Bei Li, Saad Ezzini, Haoye Tian, Jacques Klein, and

- Tegawende F. Bissyande. 2024. [Codeagent: Au](https://arxiv.org/abs/2402.02172)[tonomous communicative agents for code review.](https://arxiv.org/abs/2402.02172) *Preprint*, arXiv:2402.02172.
- <span id="page-11-6"></span>Harsh Trivedi, Tushar Khot, Mareike Hartmann, Ruskin Manku, Vinty Dong, Edward Li, Shashank Gupta, Ashish Sabharwal, and Niranjan Balasubramanian. 2024. AppWorld: A controllable world of apps and people for benchmarking interactive coding agents. In *ACL*.
- <span id="page-11-12"></span>Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji. 2024a. Executable code actions elicit better llm agents. *arXiv preprint arXiv:2402.01030*.
- <span id="page-11-18"></span>Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, Hoang H. Tran, Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian, Yanjun Shao, Niklas Muennighoff, Yizhe Zhang, Binyuan Hui, Junyang Lin, Robert Brennan, Hao Peng, Heng Ji, and Graham Neubig. 2024b. [Open](https://arxiv.org/abs/2407.16741)[devin: An open platform for ai software developers](https://arxiv.org/abs/2407.16741) [as generalist agents.](https://arxiv.org/abs/2407.16741) *Preprint*, arXiv:2407.16741.
- <span id="page-11-11"></span>Xingyao Wang, Boxuan Li, Yufan Song, Frank F Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, et al. 2024c. Opendevin: An open platform for ai software developers as generalist agents. *arXiv preprint arXiv:2407.16741*.
- <span id="page-11-16"></span>Zhiruo Wang, Zhoujun Cheng, Hao Zhu, Daniel Fried, and Graham Neubig. 2024d. What are tools anyway? a survey from the language model perspective. *arXiv preprint arXiv:2403.15452*.
- <span id="page-11-13"></span>Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. 2024e. Agent workflow memory. *arXiv preprint arXiv:2409.07429*.
- <span id="page-11-3"></span>Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh Jing Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, and Tao Yu. 2024. [Os](https://arxiv.org/abs/2404.07972)[world: Benchmarking multimodal agents for open](https://arxiv.org/abs/2404.07972)[ended tasks in real computer environments.](https://arxiv.org/abs/2404.07972) *Preprint*, arXiv:2404.07972.
- <span id="page-11-5"></span>Nancy Xu, Sam Masling, Michael Du, Giovanni Campagna, Larry Heck, James Landay, and Monica Lam. 2021. [Grounding open-domain instructions to auto](https://doi.org/10.18653/v1/2021.naacl-main.80)[mate web support tasks.](https://doi.org/10.18653/v1/2021.naacl-main.80) In *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 1022–1032, Online. Association for Computational Linguistics.
- <span id="page-11-15"></span>Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. 2022. Webshop: Towards scalable realworld web interaction with grounded language agents. *Advances in Neural Information Processing Systems*, 35:20744–20757.

<span id="page-12-4"></span>Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. 2023. [Webshop: Towards scalable real](https://arxiv.org/abs/2207.01206)[world web interaction with grounded language agents.](https://arxiv.org/abs/2207.01206) *Preprint*, arXiv:2207.01206.

<span id="page-12-3"></span>Keen You, Haotian Zhang, Eldon Schoop, Floris Weers, Amanda Swearngin, Jeffrey Nichols, Yinfei Yang, and Zhe Gan. 2024. [Ferret-ui: Grounded mobile](https://arxiv.org/abs/2404.05719) [ui understanding with multimodal llms.](https://arxiv.org/abs/2404.05719) *Preprint*, arXiv:2404.05719.

<span id="page-12-6"></span>Siyu Yuan, Kaitao Song, Jiangjie Chen, Xu Tan, Yongliang Shen, Ren Kan, Dongsheng Li, and Deqing Yang. 2024. [Easytool: Enhancing llm-based](https://arxiv.org/abs/2401.06201) [agents with concise tool instruction.](https://arxiv.org/abs/2401.06201) *Preprint*, arXiv:2401.06201.

<span id="page-12-0"></span>Chi Zhang, Zhao Yang, Jiaxuan Liu, Yucheng Han, Xin Chen, Zebiao Huang, Bin Fu, and Gang Yu. 2023. [Appagent: Multimodal agents as smartphone users.](https://arxiv.org/abs/2312.13771) *Preprint*, arXiv:2312.13771.

<span id="page-12-7"></span>Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. 2024. [Codeagent: Enhancing code generation with](https://arxiv.org/abs/2401.07339) [tool-integrated agent systems for real-world repo](https://arxiv.org/abs/2401.07339)[level coding challenges.](https://arxiv.org/abs/2401.07339) *Preprint*, arXiv:2401.07339.

<span id="page-12-5"></span>Boyuan Zheng, Michael Y Fatemi, Xiaolong Jin, Zora Zhiruo Wang, Apurva Gandhi, Yueqi Song, Yu Gu, Jayanth Srinivasa, Gaowen Liu, Graham Neubig, et al. 2025. Skillweaver: Web agents can selfimprove by discovering and honing skills. *arXiv preprint arXiv:2504.07079*.

<span id="page-12-2"></span>Boyuan Zheng, Boyu Gou, Jihyung Kil, Huan Sun, and Yu Su. 2024. [Gpt-4v\(ision\) is a generalist web agent,](https://openreview.net/forum?id=piecKJ2DlB) [if grounded.](https://openreview.net/forum?id=piecKJ2DlB) In *Forty-first International Conference on Machine Learning*.

<span id="page-12-1"></span>Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Graham Neubig. 2024. [Webarena: A realistic web en](https://openreview.net/forum?id=oKn9c6ytLx)[vironment for building autonomous agents.](https://openreview.net/forum?id=oKn9c6ytLx) In *The Twelfth International Conference on Learning Representations*.

### A Appendix

#### A.1 Related Work

The development of AI agents that interact with the web and APIs has garnered significant research attention. Web browsers, serving as the primary interface for interacting with online content, have long been a focus for AI research. Web-based agents that can navigate websites, extract information, and perform tasks autonomously have been studied extensively, especially in the context of LLMs and agents designed to mimic human behavior online.

Web Navigation Agents Much prior work has centered around agents that perform web-based tasks using browsing actions [\(Yao et al.,](#page-11-15) [2022;](#page-11-15) [Lai et al.,](#page-10-16) [2024;](#page-10-16) [Koh et al.,](#page-10-17) [2024b;](#page-10-17) [Pan et al.,](#page-11-2) [2024\)](#page-11-2). These agents are particularly effective in environments where human-like interaction with a user interface is necessary [\(Drouin et al.,](#page-10-14) [2024b\)](#page-10-14). Frameworks such as WebArena have further refined the evaluation of such agents by providing complex and realistic web navigation tasks [\(Zhou](#page-12-1) [et al.,](#page-12-1) [2024\)](#page-12-1). Our work explores the Hybrid Agent that combines web browsing with API interactions. While prior work primarily focuses on browsingonly agents, we examine how Hybrid Agents can enhance performance by integrating structured API calls with web navigation.

Code Generation Agents and Tool Usage Another stream of research focuses on agents that interact with online content via application programming interfaces (APIs) [\(Wang et al.,](#page-11-16) [2024d;](#page-11-16) [Patil et al.,](#page-11-1) [2023;](#page-11-1) [Qin et al.,](#page-11-17) [2023;](#page-11-17) [Yuan et al.,](#page-12-6) [2024;](#page-12-6) [Wang et al.,](#page-11-18) [2024b;](#page-11-18) [Du et al.,](#page-10-18) [2024\)](#page-10-18). In this context, works such as CodeAct have pioneered the development of agents that generate and execute code, including API calls, to perform tasks typically reserved for software engineers [\(Wang et al.,](#page-11-12) [2024a;](#page-11-12) [Zhang et al.,](#page-12-7) [2024;](#page-12-7) [Tang et al.,](#page-11-19) [2024\)](#page-11-19). These API-Based Agents are optimized for tasks that involve structured data exchanges, allowing them to perform operations more efficiently than traditional web navigation agents [\(Shen et al.,](#page-11-20) [2024\)](#page-11-20). On the other hand, our work integrates both browsing and API interactions, demonstrating that Hybrid Agents can outperform API-only agents in tasks requiring web navigation. While existing research shows the efficiency of API-Based Agents, our Hybrid Agent dynamically switches between APIs and web browsing to optimize task performance.

Additionally, we are the first to explore comparative studies of API v.s. Browsing Agents on the same websites. We demonstrate that API-Based Agents are often more efficient than Browsing Agents when APIs are available, leading to significant improvements in performance. This finding is aligned with previous studies that highlight the advantages of structured interactions through APIs compared to unstructured web browsing interactions.

### <span id="page-13-0"></span>A.2 WebArena Tasks

WebArena reproduces the functionality of several commonly-used websites using open-source frameworks, with real-world data imported into the reproduced websites.

WebArena includes tasks related to the following websites:

- Gitlab[15](#page-13-2) 180 instances: This website contains tasks related to project management and version control, where agents perform tasks like opening issues, handling merge requests, or creating repositories. Example query: Submit a merge request for a11yproject.com/redesign branch to be merged into the markdown-figure-block branch, assign myself as the reviewer.
- Map[16](#page-13-3) 109 instances: For this website, tasks are centered around navigation, trip planning and queries about distances, requiring the agent to retrieve and interpret map-based data, similar to using real-world map services like Google map. Example query: Tell me the full address of all international airports that are within a driving distance of 50 km to Carnegie Mellon University.
- Shopping[17](#page-13-4) 187 instances: Tasks related to this website represents typical e-commerce tasks, such as searching for products, adding items to carts, and processing transactions. Example query: Change the delivery address for my most recent order to 77 Massachusetts Ave, Cambridge, MA.
- Shopping Admin[18](#page-13-5) 182 instances: This setting involves managing backend administrative tasks for an online store, like managing product inventories, processing orders, or viewing sales reports. Example query: Tell me the the number of reviews that our store received by far that mention term "satisfied".
- Reddit[19](#page-13-6) 106 instances: Tasks here are similar to interactions with the official Reddit,

where agents need to post comments, upvote or down-vote posts, or retrieve information from threads. Example query: Tell me the count of comments that have received more downvotes than upvotes for the user who made the latest post on the Showerthoughts forum.

• Multi-Website Tasks – 48 instances: These examples involve tasks that span across two websites, requiring the agent to interact with both websites simultaneously, adding complexity to the task. Example query: Create a folder named news in gimmiethat.space repo. Within it, create a file named urls.txt that contains the URLs of the 5 most recent posts from the news related subreddits?

#### <span id="page-13-1"></span>A.3 Obtaining APIs of WebArena Websites

- Gitlab: we leveraged the open Gitlab REST APIs[20](#page-13-7), consisting of 988 endpoints. Most of WebArena tasks are covered by these APIs, with only a small fraction of tasks, such as retrieving users' Gitlab feed token, are not covered by any existing endpoints,
- Map: The Map website offers three sets of APIs, each offering distinct functionalities, with a total of 53 endpoints. The first set of APIs, openly available at Nominatim[21](#page-13-8), offers essential endpoints for geographic searches. The second set of APIs, from Project OSRM[22](#page-13-9), focuses on routing and navigation functionalities. The third set of APIs, available at OpenStreetMap[23](#page-13-10), deals primarily with map database operations. This API is rarely used in WebArena tasks but offers capabilities for interacting with OSM data.
- Shopping: The e-commerce website uses APIs from the Adobe Commerce API[24](#page-13-11), consisting of 556 endpoints. These endpoints provide support for common shopping tasks such as purchasing products, searching categories, and managing customer accounts.

<span id="page-13-2"></span><sup>15</sup>Original Website: <https://gitlab.com>

<span id="page-13-4"></span><span id="page-13-3"></span><sup>16</sup>Original Website: <https://www.openstreetmap.org>

<sup>17</sup>Developed using Adobe Magento [\(https://github.com/](https://github.com/magento/magento2) [magento/magento2\)](https://github.com/magento/magento2)

<span id="page-13-5"></span><sup>18</sup>Developed using Adobe Magento [\(https://github.com/](https://github.com/magento/magento2) [magento/magento2\)](https://github.com/magento/magento2)

<span id="page-13-6"></span><sup>19</sup>Deployed Postmill [\(https://postmill.xyz/\)](https://postmill.xyz/), the opensourced counterpart of Reddit [\(https://www.reddit.com\)](https://www.reddit.com)

<span id="page-13-7"></span><sup>20</sup>Documentation of all Gitlab APIs could be found at [https:](https://docs.gitlab.com/ee/api/rest/) [//docs.gitlab.com/ee/api/rest/.](https://docs.gitlab.com/ee/api/rest/)

<span id="page-13-8"></span><sup>21</sup>The API documentations could be found at [https://](https://nominatim.org/release-docs/develop/api/Overview/) [nominatim.org/release-docs/develop/api/Overview/](https://nominatim.org/release-docs/develop/api/Overview/)

<span id="page-13-9"></span><sup>22</sup>Documentations of APIs available at [https://project-osrm.](https://project-osrm.org/docs/v5.5.1/api) [org/docs/v5.5.1/api](https://project-osrm.org/docs/v5.5.1/api)

<span id="page-13-10"></span><sup>23</sup>API documentations openly available at [https://wiki.](https://wiki.openstreetmap.org/wiki/API_v0.6) [openstreetmap.org/wiki/API\\_v0.6](https://wiki.openstreetmap.org/wiki/API_v0.6)

<span id="page-13-11"></span><sup>24</sup>APIs documented at [https://developer.adobe.com/](https://developer.adobe.com/commerce/webapi/rest/quick-reference/) [commerce/webapi/rest/quick-reference/](https://developer.adobe.com/commerce/webapi/rest/quick-reference/)

- Shopping Admin: This website shares a common set of APIs with the shopping website. However, this website requires a unique admin token to access the admin-only APIs such as changing the price of products and deleting products from stores.
- Reddit: The Reddit tasks in WebArena are based on a self-hosted limited clone of the Reddit website [25](#page-14-1), with limited functionalities as compared to the official site. As a result, all of the available APIs are self-implemented, with a best effort to mimic to official Reddit APIs. This website supports 31 endpoints, which include writing comments and voting posts.

#### <span id="page-14-0"></span>A.4 Additional Analysis

Table [5](#page-15-1) documents the percentage of actions of our Hybrid Agent. Across all websites, our Hybrid Agent chooses to do both Browsing and API in the same task at least half of the time.

Table [6](#page-15-2) documents the accuracy of the Hybrid Agent across websites when performing different choices of actions. It shows consistently high accuracy when choosing API only and API+browsing.

Table [7](#page-16-1) shows the breakdown of number of steps and cost by website.

<span id="page-14-2"></span>![](_page_14_Figure_6.jpeg)

Figure 7: Steps of agents on WebArena.

Steps Figure [7](#page-14-2) demonstrates a scatterplot of the average accuracy of each agent on WebArena over their average steps. The Browsing Agent takes more steps to complete tasks compared to the API-Based Agent on average, while the Hybrid Agent takes the most steps amongst the three agents. This

is likely due to the Browsing Agent's reliance on navigating web interfaces and interacting with visual elements, which involves a sequential and more time consuming processes. The API-Based Agent is the most efficient in terms of steps, as it can directly interact with structured data via APIs, bypassing many of the steps involved in traditional web navigation. The Hybrid Agent, combining both action spaces from the Browsing Agent and the API-Based Agent, takes more steps than both agents.

<span id="page-14-3"></span>![](_page_14_Figure_11.jpeg)

Figure 8: Costs of agents on WebArena.

Costs Figure [8](#page-14-3) demonstrates a scatterplot of the average accuracy of each agent on WebArena over their average costs. The cost of completing tasks shows a different trend. While the Browsing Agent requires more steps, it is much cheaper compared to the API-Based Agent and the Hybrid Agent. This is primarily because the prompts needed for Browsing Agents are much shorter. When browsing, the agent only needs instructions on how to use the web interface and the limited action space around 14 browsing actions. In contrast, API-Based and Hybrid Agents require access to a much larger set of API calls. For example, when interacting with Git-Lab, the agent is provided with 988 available APIs, leading to much longer prompts and significantly increasing the cost of execution. The cost goes down when the prompt for API calling is shorter. For example, the Reddit website has the least length of API documentation, where its cost is also less than other websites. However, as visualized in Figure [8,](#page-14-3) the accuracy of the API-Based Agent and the Hybrid Agent is much higher than the Browsing Agent, which makes the increase in cost justifiable

<span id="page-14-1"></span><sup>25</sup><https://codeberg.org/Postmill/Postmill>

<span id="page-15-1"></span>

| Actions       | Gitlab | Map  | Shopping | Admin | Reddit | Multi | AVG. |
|---------------|--------|------|----------|-------|--------|-------|------|
| Browsing only | 7.8    | 3.7  | 38.5     | 2.2   | 0      | 8.3   | 12.1 |
| API only      | 21.1   | 4.6  | 7.5      | 1.1   | 0      | 10.4  | 7.9  |
| Browsing+API  | 71.1   | 91.7 | 54.0     | 96.7  | 82.1   | 81.3  | 80.0 |

Table 5: Percentage of Actions (%) that our Hybrid Agent takes for each type of tasks. Each column sums up to 1.

<span id="page-15-2"></span>

| <b>Choices of Action</b> | Gitlab       | Map          | Shopping     | Admin        | Reddit       | Multi      | AVG.          |
|--------------------------|--------------|--------------|--------------|--------------|--------------|------------|---------------|
| Browsing only            | 7.1(1/14)    | 50.0(2/4)    | 23.6(17/72)  | 50.0(2/4)    | 0(0/0)       | 25.0(1/4)  | 23.5(23/98)   |
| API only                 | 47.4(18/38)  | 40.0(2/5)    | 21.4(3/14)   | 50.0(1/2)    | 0.0(0/0)     | 20.0(1/5)  | 39.1(25/64)   |
| Browsing+API             | 47.7(61/128) | 46.0(46/100) | 27.7(28/101) | 40.9(72/176) | 51.9(55/106) | 15.4(6/39) | 41.2(268/650) |

Table 6: The accuracy (%) of the Hybrid Agent across choices of actions for each website, with the number of correct instances / number of total instances in parentheses.

due to the significantly improved task performance. The higher cost is offset by the agents' ability to complete tasks more accurately and efficiently. In the future, this increased cost could potentially be mitigated by methods that retrieve only relevant APIs on the fly.

#### <span id="page-15-0"></span>A.5 API-Based Agent Prompt

### **Full System Prompt**

Full System Prompt = System Prefix + API
Prompt + System Suffix

#### .5 Al I-Dasca Agent I Tompo

#### **API Prompt**

To call APIs, you can use an interactive Python (Jupyter Notebook) environment, executing code with <execute\_ipython>.

<execute\_ipython>

print("Hello World")

</execute\_ipython>

This can be used to call the Python requests library, which is already installed for you. Here are some hints about effective API usage:

- It is better to actually view the API response and ensure the relevant information is correctly extracted and utilized before attempting any programmatic parsing.
- Make use of HTTP headers when making API calls, and be careful of the input parameters to each API call.
- Be careful about pagination of the API response, the response might only contain the first few instances, so make sure you look at all instances.

The user will provide you with a list of API calls that you can use.

#### **System Prefix**

You are an AI assistant that performs tasks on the websites. You should give helpful, detailed, and polite responses to the user's queries.

You have the ability to call site-specific APIs using Python, or browse the website directly.

<span id="page-16-1"></span>

| Agents    | Gitlab |      | Map   |      | Shopping |      | Shop-Admin |      | Reddit |      | Multi Sites |      | AVG.  |      |
|-----------|--------|------|-------|------|----------|------|------------|------|--------|------|-------------|------|-------|------|
|           | steps  | cost | steps | cost | steps    | cost | steps      | cost | steps  | cost | steps       | cost | steps | cost |
| Browsing  | 9.4    | 0.2  | 8.0   | 0.1  | 7.3      | 0.1  | 7.0        | 0.2  | 11.1   | 0.1  | 7.5         | 0.1  | 8.4   | 0.1  |
| API-Based | 7.0    | 1.7  | 6.6   | 1.1  | 8.2      | 1.0  | 8.4        | 1.1  | 8.8    | 0.6  | 7.7         | 1.6  | 7.8   | 1.2  |
| Hybrid    | 8.1    | 2.0  | 9.4   | 1.7  | 8.2      | 1.3  | 9.0        | 1.4  | 7.8    | 0.6  | 8.0         | 1.9  | 8.5   | 1.4  |

Table 7: Number of Steps and Cost (in U.S. dollars) of Agents across WebArena Websites

#### System Suffix

The information provided by the user might be incomplete or ambiguous. For example, if I want to search for "xyz", then "xyz" could be the name of a product, a user, or a category on the site. In these cases, you should attempt to evaluate all potential cases that the user might be indicating and be careful about nuances in the user's query. Also, do NOT ask the user for any clarification, they cannot clarify anything and you need to do it yourself.

When you think you successfully finished the task, first respond with Finish[answer] where you include *only* your answer to the question [] if the user asks for an answer, make sure you should only include the answer to the question but not any additional explanation, details, or commentary unless specifically requested.

After that, when you responded with your answer, you should respond with <finish></finish>.

Then finally, to exit, you can run

<execute\_bash>

exit()

</execute\_bash>

Your responses should be concise. The assistant should attempt fewer things at a time instead of putting too many commands OR too much code in one execute block.

Include AT MOST ONE <execute\_ipython>, <execute\_browse>, or <execute\_bash> per response.

IMPORTANT: Execute code using <execute\_ipython>, <execute\_bash>, or <execute\_browse> whenever possible.

Below are some examples:

— START OF EXAMPLE —

Examples

— END OF EXAMPLE —

Now, let's start!

#### Initial User Prompt

Think step by step to perform the following task related to gitlab. Answer the question: \*\*\*Example WebArena Intent\*\*\*

The site URL is Example Site URL, use this instead of the normal site URL.

For API calling, use this access token: Example Access Token.

My username on this website is Example Username. Below is the list of all APIs you can use and their descriptions:

Example API Documentation.

Note: Before actually using a API call, \*you should call the get\_api\_documentation function in the utils module to get detailed API documentation of the API.\* For example, if you want to use the API GET /api/v4/projects/id/repository/commits, you should first do:

<execute\_ipython>

from utils import get\_api\_documentation get\_api\_documentation("GET

/api/v4/projects/{id}/repository/commits") </execute\_ipython>

This will provide you with detailed descriptions of the input parameters and example output jsons.

#### <span id="page-16-0"></span>A.6 Hybrid Agent Prompt

#### Full System Prompt

Full System Prompt = System Prefix + API Prompt + Browsing Prompt + System Suffix

#### System Prefix

You are an AI assistant that performs tasks on the websites. You should give helpful, detailed, and polite responses to the user's queries.

You have the ability to call site-specific APIs using Python, or browse the website directly.

IMPORTANT: In general, you must always first try to use APIs to perform the task; however, you should use web browsing when there is no useful API available for the task.

IMPORTANT: After you tried out using APIs, you must use web browsing to navigate to some URL containing contents that could verify whether the results you obtained by API calling is correct.

#### API Prompt

To call APIs, you can use an interactive Python (Jupyter Notebook) environment, executing code with <execute\_ipython>.

<execute\_ipython> print("Hello World!") </execute\_ipython>

This can be used to call the Python requests library, which is already installed for you. Here are some hints about effective API usage:

- It is better to actually view the API response and ensure the relevant information is correctly extracted and utilized before attempting any programmatic parsing.
- Make use of HTTP headers when making API calls, and be careful of the input parameters to each API call.
- Be careful about pagination of the API response, the response might only contain the first few instances, so make sure you look at all instances.

The user will provide you with a list of API calls that you can use.

#### Browsing Prompt

You can browse the Internet by putting special browsing commands within <execute\_browse> and </execute\_browse> (in Python syntax).

For example to select the option blue from the dropdown menu with bid 12, and click on the submit button with bid 51:

```
<execute_browse>
select_option("12", "blue")
click("51")
</execute_browse>
```

```
The following actions are available:
def goto(url: str):
  """Navigate to the specified URL.
  Examples:
    goto("http://www.example.com")
  """
def go_back():
  """Navigate back to the previous page.
  Examples:
    go_back()
  """
def go_forward():
  """Navigate forward to the next page.
  Examples:
    go_forward()
  """
def scroll(delta_x: float, delta_y:
float):
  """Scroll the page by the specified
amount.
  Examples:
    scroll(0, 200)
    scroll(-50.2, -100.5)
  """
def fill(bid: str, value: str):
  """Fill the input field with the
specified value.
  Examples:
    fill("237", "example value")
    fill("45", "multi-line example")
    fill("a12", "example with "quotes"")
  """
def select_option(bid: str, options: str |
list[str]):
  """Select an option from a dropdown menu.
  Examples:
    select_option("48", "blue")
    select_option("48", ["red", "green",
"blue"])
  """
def focus(bid: str):
  """Focus on an element.
  Examples:
    focus("b455")
  """
```

#### Browsing Prompt - Continued

```
def click(bid: str, button: Literal["left",
"middle", "right"] = "left", modifiers:
list[typing.Literal["Alt", "Control",
"Meta", "Shift"]] = []):
  """Click on an element with the specified
button and modifiers.
  Examples:
    click("51")
    click("b22", button="right")
    click("48", button="middle",
modifiers=["Shift"])
  """
def dblclick(bid: str, button:
Literal["left", "middle",
"right"] = "left", modifiers:
list[typing.Literal["Alt", "Control",
"Meta", "Shift"]] = []):
  """Double-click on an element with the
specified button and modifiers.
  Examples:
    dblclick("12")
    dblclick("ca42", button="right")
    dblclick("178", button="middle",
modifiers=["Shift"])
  """
def hover(bid: str):
  """Hover over an element.
  Examples:
    hover("b8")
  """
def press(bid: str, key_comb: str):
  """Press a key combination on an element.
  Examples:
    press("88", "Backspace")
    press("a26", "Control+a")
    press("a61", "Meta+Shift+t")
  """
def clear(bid: str):
  """Clear the input field.
  Examples:
    clear("996")
  """
def drag_and_drop(from_bid: str, to_bid:
str):
  """Drag and drop an element to another
element.
  Examples:
    drag_and_drop("56", "498")
  """
def upload_file(bid: str, file: str |
list[str]):
  """Upload a file to the specified
element.
  Examples:
    upload_file("572", "my_receipt.pdf")
    upload_file("63",
["/home/bob/Documents/image.jpg",
"/home/bob/Documents/file.zip"])
  """
```

#### System Suffix

The information provided by the user might be incomplete or ambiguous. For example, if I want to search for "xyz", then "xyz" could be the name of a product, a user, or a category on the site. In these cases, you should attempt to evaluate all potential cases that the user might be indicating and be careful about nuances in the user's query. Also, do NOT ask the user for any clarification, they cannot clarify anything and you need to do it yourself.

When you think you successfully finished the task, first respond with Finish[answer] where you include *only* your answer to the question [] if the user asks for an answer, make sure you should only include the answer to the question but not any additional explanation, details, or commentary unless specifically requested.

After that, when you responded with your answer, you should respond with <finish></finish>.

Then finally, to exit, you can run

<execute\_bash>

exit()

</execute\_bash>

Your responses should be concise. The assistant should attempt fewer things at a time instead of putting too many commands OR too much code in one execute block.

Include AT MOST ONE <execute\_ipython>, <execute\_browse>, or <execute\_bash> per response.

IMPORTANT: Execute code using <execute\_ipython>, <execute\_bash>, or <execute\_browse> whenever possible.

Below are some examples:

— START OF EXAMPLE —

Examples

— END OF EXAMPLE —

Now, let's start!

#### Initial User Prompt

Think step by step to perform the following task related to gitlab. Answer the question: \*\*\*Example WebArena Intent\*\*\*

The site URL is Example Site URL, use this instead of the normal site URL.

For API calling, use this access token: Example Access Token.

For web browsing, You should start from the URL Example Start URL, and this webpage is already logged in and opened for you.

My username on this website is Example Username. Below is the list of all APIs you can use and their descriptions:

Example API Documentation.

Note: Before actually using a API call, \*you should call the get\_api\_documentation function in the utils module to get detailed API documentation of the API.\* For example, if you want to use the API GET /api/v4/projects/id/repository/commits, you should first do:

<execute\_ipython>

from utils import get\_api\_documentation get\_api\_documentation("GET

/api/v4/projects/{id}/repository/commits") </execute\_ipython>

This will provide you with detailed descriptions of the input parameters and example output jsons.

IMPORTANT: In general, you must always first try to use APIs to perform the task; however, you should use web browsing when there is no useful API available for the task. IMPORTANT: After you tried out using APIs, you must use web browsing to navigate to some URL containing contents that could verify whether the results you obtained by API calling is correct.