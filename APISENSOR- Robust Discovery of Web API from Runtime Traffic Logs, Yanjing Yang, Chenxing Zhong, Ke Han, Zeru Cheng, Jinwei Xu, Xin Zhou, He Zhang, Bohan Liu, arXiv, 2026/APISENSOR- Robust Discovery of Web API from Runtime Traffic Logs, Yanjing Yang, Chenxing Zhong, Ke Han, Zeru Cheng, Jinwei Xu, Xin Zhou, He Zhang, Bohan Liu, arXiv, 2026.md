## APISENSOR: Robust Discovery of Web API from Runtime Traffic Logs

Yanjing Yang† [,](https://orcid.org/0009-0006-8789-4589) Chenxing Zhong[†](https://orcid.org/0000-0001-7298-1926) , Ke Han† [,](https://orcid.org/0009-0001-5094-4427) Zeru Chen[g](https://orcid.org/0009-0001-5094-4427) , Jinwei X[u](https://orcid.org/0009-0004-5157-1118) , Xin Zhou[∗](https://orcid.org/0000-0002-3263-1275) , He Zhang[∗](https://orcid.org/0000-0002-9159-5331) , Bohan Li[u](https://orcid.org/0000-0002-0146-5411) ,

*Abstract*—Large Language Model (LLM)–based agents increasingly rely on APIs to operate complex web applications, but rapid evolution often leads to incomplete, unclear, or inconsistent API documentation. Existing work broadly falls into two categories: (1) static, white-box approaches based on source code or formal specifications, and (2) dynamic, black-box approaches that infer APIs from runtime network traffic. Static approaches rely on internal artifacts such as source code or API specifications, which are typically unavailable for closed-source systems. Moreover, because they analyze potential interfaces rather than runtime behavior, they often over-approximate API usage by matching patterns that may include unused or unreachable code, resulting in high false-positive rates. Although dynamic black-box API discovery applies broadly across applications, its robustness degrades in complex traffic environments where shared collection points aggregate traffic from multiple applications. To improve the robustness of API discovery under mixed runtime traffic, we propose APISENSOR, a black-box API discovery framework that reconstructs application APIs in an unsupervised setting. Instead of relying on simple clustering or analyzing requests individually, APISENSOR performs structured analysis over complex traffic, combining traffic denoising and normalization with a graph-based two-stage clustering process to recover accurate APIs. Our evaluation measures the accuracy of APISENSOR in discovering APIs and its robustness across six widely used web applications using over 10,000 runtime requests with simulated mixed-traffic noise. The results demonstrate that APISENSOR significantly improves discovery accuracy, achieving an average Group Accuracy Precision of 95.92% and an F1-score of 94.91%, outperforming state-of-the-art API discovery methods. Across different applications and noise settings, APISENSOR achieves both the lowest performance variance and at most an 8.11-point FGA drop, demonstrating the best robustness in 10 baselines. Finally, ablation studies confirm that each component of the APISENSOR is essential to its overall effectiveness. During our experiments, APISENSOR also reveals API documentation inconsistencies in a real application, which are confirmed by the developers in the community.

*Index Terms*—Software Reverse Engineering, Application Programming Interfaces, Application Service Discovery.

#### I. INTRODUCTION

The rapid growth of Large Language Models (LLM) based agent applications (e.g., Openclaw [\[3\]](#page-12-0)) has increased the

Yanjing Yang, Ke Han, Xin Zhou, Jinwei Xu, Bohan Liu, and He Zhang are with State Key Laboratory of Novel Software Technology, Software Institute, Nanjing University, Nanjing 210008, China (email: yj yang@smail.nju.edu.cn; zhouxin@nju.edu.cn; bohanliu@nju.edu.cn; hezhang@nju.edu.cn; jinwei xu@smail.nju.edu.cn;.

Chenxing Zhong is with Nanjing University of Science and Technology, Nanjing 2100094, China

requirements for reliable API discovery. Agents allow LLM to operate complex web applications by invoking APIs without requiring knowledge of UI design logic [\[34,](#page-13-0) [28\]](#page-13-1). However, many web applications still provide incomplete or missing API descriptions because API implementations evolve rapidly through frequent version updates and feature iterations, while documentation maintenance often lags behind the implementation [\[12,](#page-12-1) [24,](#page-13-2) [37\]](#page-13-3).

1

Existing API discovery techniques can be broadly divided into (1) white-box and (2) black-box approaches, which can work in synergy in practice. White-box approaches that rely on source code or static specifications have limited practical applicability because they require access to program internals. However, most production web services are proprietary and closed source. Recent industry reports estimate that more than 85% of deployed web services are not publicly available in source form, which significantly restricts the use of white-box techniques [\[10\]](#page-12-2). Moreover, many white-box approaches rely on static analysis, which typically adopts *over-approximation* to conservatively model program behavior. As a result, the analysis may report APIs that are defined in the code but not actually exposed at runtime (e.g., endpoints used only for internal service calls), leading to false positives in discovered active API assets [\[10\]](#page-12-2). In addition, prior work shows that existing documentation may not accurately reflect the actual implementation [\[31\]](#page-13-4). Therefore, understanding application functionality cannot rely solely on white-box techniques and requires black-box runtime behavior observation [\[16\]](#page-12-3).

Although black-box API discovery techniques are applicable to a wider range of scenarios, their effectiveness often degrades significantly in practice when operating on diverse runtime traffic. Existing approaches mainly follow three directions, including traffic capture methods that (1) reconstruct APIs from request–response traces [\[1,](#page-12-4) [2\]](#page-12-5), (2) request pattern analysis using clustering or learning-based techniques [\[13,](#page-12-6) [35,](#page-13-5) [7\]](#page-12-7), and (3) log template mining approaches that extract parameterized request structures [\[19,](#page-13-6) [29,](#page-13-7) [25,](#page-13-8) [5,](#page-12-8) [14,](#page-12-9) [11\]](#page-12-10). In practice, API traffic is commonly collected at shared network gateways that serve multiple applications [\[8\]](#page-12-11). As a result, requests from different services are interleaved with each other and with background traffic [\[27\]](#page-13-9). For example, a gateway may simultaneously observe requests such as /account/info/get, /accounting/info/gen, and /account/info/graph. Although these paths share highly similar lexical patterns, they may belong to user account management, financial accounting, and analyt-

<sup>†</sup> Contribute Equally

<sup>∗</sup> Corresponding author: Xin Zhou & He Zhang.

ics services, respectively. The same gateway may also carry non-API traffic such as /static/account.js or /images/account.png. Such heterogeneous traffic makes it difficult to correctly attribute observed requests to the application that actually exposes the corresponding API [\[33,](#page-13-10) [26\]](#page-13-11). *(Problem)* Consequently, existing black-box trafficbased API discovery approach are not robust and suffer substantial performance degradation in complex traffic environments involving multiple applications.

*(Approach)* To address the above challenges, we propose APISENSOR, a black-box API discovery framework that extracts structural API templates from runtime traffic and clusters them using graph-based analysis. To cope with mixed traffic from multiple applications and heavy noise in gateway environments (Challenge 1), APISENSOR first filters runtime traffic to remove non-API requests and normalizes request paths to reduce noise and variability. This step suppresses interference from background traffic and produces cleaner inputs for subsequent analysis. To overcome the limited information available from individual requests (Challenge 2), APISENSOR performs API discovery in two stages. Structural template extraction abstracts variable identifiers while preserving stable API structures, which mitigates fragmentation caused by dynamic parameters. Based on these templates, graph-based clustering captures relationships among API calls rather than treating requests independently, enabling more reliable API discovery under unlabeled and heterogeneous traffic.

*(Evaluation)* To evaluate APISENSOR, we conduct API discovery experiments on several well-known web applications, including Train-Ticket, HumHub, Memos, Overleaf, Nextcloud, and Dify. We use *Precision of Group Accuracy* (PGA), *Recall of Group Accuracy* (RGA), the *F1-score of Group Accuracy* (FGA), and Purity as evaluation metrics. Averaged across all projects, APISENSOR achieves leading performance with a PGA of 95.92%, an RGA of 94.36%, and an FGA of 94.91%, while maintaining low variance across different applications. These results demonstrate strong robustness across projects and a low false-positive rate in practical API discovery. Then, we further evaluate the robustness of APISENSOR under different noise types and injected noise levels. Across all settings, APISENSOR shows stronger robustness than all baseline methods and is minimally affected by noise introduced in simulated gateway environments. Across different noise types, the performance variation of APISENSOR remains limited, with the FGA decreasing by at most 8.11% and Purity varying within 1%. Under different noise levels, the performance variation remains within 4%. Finally, we conduct ablation studies on the key components of APISENSOR, showing that each design component is necessary for achieving the overall performance.

The contributions of this study are summarized as follows.

• Data: We construct a benchmark dataset by manually collecting over 10K runtime traffic traces from six web applications of different types, scales, and domains. Based on official documentation and validation through real execution traffic, we annotate 199 valid and callable API endpoints for evaluation. The dataset will be released as part of our replication package [].

- Approach: We propose APISENSOR, a black-box API discovery framework that reconstructs web APIs from mixed runtime traffic. The framework combines traffic denoising, structural API template extraction, and robust graph clustering to achieve accurate and stable API discovery under unsupervised and noisy settings.
- Evaluation: We comprehensively evaluate APISENSOR against existing baseline methods under the identified challenges, covering diverse applications and different noise conditions. In addition, during evaluation, APISEN-SOR uncovers previously undocumented shadow APIs in a popular application, Dify, which are later confirmed by the developer community.

The remainder of this paper is organized as follows. Section [II](#page-1-0) reviews related work and motivates our work by identifying unresolved challenges. Section [III](#page-2-0) presents our APISENSOR approach for API discovery from runtime traffic. Section [IV](#page-4-0) describes the research questions and the experimental setup. Section [V](#page-6-0) reports and analyzes the results. Section [VI](#page-10-0) discusses the value of our approach for agent-based applications and the shadow undocumented APIs discovered in Dify. Finally, we examine threats to validity in Section [VIII](#page-11-0) and conclude this paper in Section [IX.](#page-12-12)

#### II. RELATED WORK

<span id="page-1-0"></span>Prior work on API reverse engineering and discovery mainly falls into two categories: (1) white-box approaches that analyze source code and other development-time artifacts to statically extract API definitions, which provide broad coverage but are limited to open-source systems; and (2) black-box approaches that infer APIs from runtime traffic and logs, which reflect actual exposed functionality but often rely on fixed assumptions about API structures. These two lines of work are complementary, as static analysis improves completeness while traffic-based analysis enhances accuracy, together enabling more comprehensive and precise API discovery.

White-box API discovery approaches analyze artifacts available at development time, such as API specifications, source code, and developer documentation. Specificationdriven methods, for example OpenAPI, describe intended API interfaces in a structured way and support systematic analysis [\[21\]](#page-13-12). However, specifications may become outdated as systems evolve, leading to specification drift and the existence of undocumented or obsolete APIs [\[6\]](#page-12-13). In addition, inconsistent REST design practices reduce the reliability of specification-based analysis [\[18\]](#page-12-14). To reduce manual effort, some approaches extract API information directly from source code and repositories. Tools such as APIDocGen [\[20\]](#page-13-13) and RepoDocGen [\[22\]](#page-13-14) recover API endpoints and structures through static code analysis. These approaches can achieve good coverage when full source code is available, but they only reflect design-time artifacts and do not capture actual runtime API usage [\[30\]](#page-13-15). Other work focuses on improving API discovery by linking developer intent to API usage. TaskAPIRec [\[9\]](#page-12-15) and related studies [\[17\]](#page-12-16) map high-level tasks to API calls, while CodeGlossary [\[30\]](#page-13-15) extracts semantic information from

![](_page_2_Figure_1.jpeg)

<span id="page-2-1"></span>Fig. 1. Existing tools (e.g., Optic) cannot reliably distinguish these heterogeneous requests, potentially leading to incomplete and inaccurate API specifications.

code. Additional semantic knowledge has also been collected from developer forums [\[4,](#page-12-17) [23\]](#page-13-16). More recent hybrid approaches, such as gDoc, combine static analysis with limited runtime information to generate structured API documentation [\[32\]](#page-13-17).

While white-box approaches rely on development-time artifacts, API discovery can also be performed from a runtime perspective. Accordingly, black-box approaches infer API endpoints and behaviors directly from observed traffic and logs, without access to internal artifacts.

Several open-source tools support API reverse engineering from runtime traffic. Optic [\[2\]](#page-12-5) and Mitmproxy2Swagger [\[1\]](#page-12-4) generate OpenAPI specifications from HTTP request–response traces or intercepted network traffic, but they mainly rely on heuristics and shallow structure inference. Beyond such tools, prior work explicitly studies endpoint discovery and specification recovery using richer signals. APID2Spec [\[36\]](#page-13-18) extracts API specifications by crawling documentation pages and inferring base URLs, paths, and HTTP methods. APICARV [\[35\]](#page-13-5) monitors UI-driven runtime traffic and builds an interaction graph to infer endpoints. Web API Search [\[13\]](#page-12-6) supports endpoint-level discovery by matching natural language queries against API descriptions mined from online documentation. Online methods such as APIDrain3 incrementally mine URL templates from streaming API traffic for continuous discovery.

Template mining and log parsing techniques are also related and can be applied to API traffic analysis. Classical parsers such as LogCluster [\[25\]](#page-13-8) and LogNgram [\[5\]](#page-12-8), as well as more recent approaches like UniParser [\[14\]](#page-12-9) and LogPPT [\[11\]](#page-12-10), extract stable patterns by abstracting variable tokens from request paths. However, since these methods mainly rely on lexical patterns of individual requests, they often struggle to distinguish API operations with similar URL structures.

Figure [1](#page-2-1) shows a real example of Optic on gateway traffic, highlighting its limitations in accurate API identification. The intercepted traffic contains multiple variants of similar paths (e.g., /api/v1/users/login, /api/v1/users/log1n3, /api/{a.pi}/user/login) together with noisy or malformed requests. While the ground truth includes canonical endpoints such as POST /api/v1/users/login and GET /api/v1/user/me, Optic produces erroneous outputs such as invalid attributes (e.g., /api/{a.pi}/user/me), over-generalized paths, clustered noise variants, and incorrect parameterization (e.g., /api/v1/3327/login).

These errors stem from two key challenges: (1) Mixed and noisy gateway traffic, where requests from different API versions and malformed paths coexist in a single stream; and (2) Insufficient context in individual requests, as many requests share similar lexical patterns but differ semantically, leading to over-generalization and misclassification when analyzed in isolation.

#### III. APPROACH

#### <span id="page-2-0"></span>*A. Overview*

APISENSOR is a traffic-based API discovery framework composed of a denoising and normalization layer followed by a two-stage clustering layer, as illustrated in Figure [2,](#page-3-0) which incrementally abstracts raw HTTP traffic into API assets. To improve robustness against traffic diversity and noise (Challenge 1), we first preprocess runtime traffic by filtering non-API requests and normalizing request paths before clustering. To achieve better precision under fully unsupervised settings (Challenge 2), our approach avoids premature merging by first clustering requests at the interface level and applying semantic refinement only within each template group.

#### *B. Statistical Traffic Denoising and Path Normalization*

Raw HTTP traffic is noisy and heterogeneous. Besides genuine API calls, logs often contain large amounts of non-API requests such as static resources, web pages, and malformed entries, which can substantially distort downstream clustering. Moreover, even within API traffic, URLs frequently embed dynamic identifiers (e.g., user IDs, order IDs) that create high-variance paths and fragment otherwise identical interfaces. To address these issues, we preprocess traffic with (i) multi-signal noise filtering to remove non-API requests, and (ii) identifier pattern learning for path normalization, which abstracts dynamic segments into stable interface templates.

Stage 1: Multi-signal noise filtering. We filter out non-API requests using a cascaded set of low-cost checks. Concretely, a request is removed if it matches any of the following signals: (1) static extensions (e.g., .js, .css, .png, .svg, .html), (2) static path patterns (e.g., /static/, /assets/, /images/) or common CDN/static-host signatures, and (3) the presence and value of the Content-Type header. Requests without a Content-Type field are discarded, and requests whose Content-Type indicates non-API semantics (e.g., text/html, image/\*, font/\*, media, archives) are pruned. After rule-based filtering, we apply a lightweight logistic sanity check to remove extreme outliers. For each remaining request r, we compute:

$$p = \sigma(z) = \frac{1}{1 + e^{-z}},$$
 (1)

![](_page_3_Figure_1.jpeg)

<span id="page-3-0"></span>Fig. 2. The workflow of APISENSOR.

where z is a weighted combination of simple structural features, including the HTTP method, path depth, whether the normalized path contains identifier placeholders, whether URL query parameters exist, and whether the payload type is JSON-based. Requests with  $p < \tau \text{(threshold)} = 0.01$  are removed.

**Stage 2: Path Normalization.** After noise filtering, we normalize request paths into a canonical form to reduce superficial variations. Specifically, we (i) strip the scheme and host (e.g., http://, domain name), (ii) remove query strings and fragments, and (iii) standardize path formatting (e.g., collapse repeated slashes and trim trailing slashes when applicable). The resulting normalized path, together with the HTTP method, is used as the API interface representation for downstream clustering.

### C. Two-Stage Clustering with Structural Templates and Semantic Graphs.

API traffic is highly heterogeneous. Requests with identical URL structures may exhibit different operational behaviors, while directly clustering raw traffic based on semantic features is often unstable and expensive at scale. To address this, we adopt a two-stage clustering framework that incrementally refines API requests from coarse structural patterns to finegrained behavioral groups (Algorithm ??). The first stage performs structure-level abstraction to group requests by interface shape, removing variability caused by dynamic path segments. The second stage refines each structural group by separating distinct behaviors using lightweight semantic signals. The two-stage clustering approach combines the robustness and efficiency of structural parsing with the expressiveness of semantic clustering, while avoiding unnecessary computation on noisy or sparse traffic.

Stage 1: Template Mining (Structure perspective). The first stage aims to identify stable API structural templates

<span id="page-3-2"></span>TABLE I
LIGHTWEIGHT SEMANTIC FEATURES USED TO DISTINGUISH REQUESTS
UNDER THE SAME STRUCTURAL TEMPLATE.

| Feature Type       | Examples                                                    | Purpose                                       |
|--------------------|-------------------------------------------------------------|-----------------------------------------------|
| Path structure     | <pre>path depth, API keywords (e.g., api, v1)</pre>         | capture interface shape and action cues       |
| Query parameters   | <pre>parameter count, common keys (e.g., page, limit)</pre> | distinguish list-style and control behaviors  |
| Payload complexity | body size, field count, nesting depth                       | separate simple Requests from complex traffic |

that represent interface shapes while removing variable path parts. Given normalized request paths, each path is split into an ordered list of segments and inserted into a fixed-depth prefix tree using the Drain3 [15]. At each level of the tree, path segments are matched exactly whenever possible. Segment positions with many different values are replaced with wildcards. This groups concrete request paths that differ only in identifier segments, such as /api/v1/items/123 and /api/v1/items/456, into a single interface-level template /api/v1/items/\*, as shown in Figure 3.

![](_page_3_Figure_11.jpeg)

<span id="page-3-1"></span>Fig. 3. Structural template mining via Drain3. Concrete API paths are abstracted into interface-level templates by replacing dynamic identifier segments.

# Stage 2: Semantic refinement (Semantic perspective). The second stage aims to further separate requests within each structural template by considering their semantic differences. Although requests grouped under the same template share the same path structure, they may still represent different behaviors.

To distinguish requests under the same structural template, each request is represented by a lightweight semantic feature vector composed of simple path, query, and payload features in Table [I.](#page-3-2) A semantic similarity graph is built within each template group using these feature representations.

Edges are added only between request pairs with high semantic similarity, filtering out weak or noisy connections. Clustering is then framed as a refinement step that enforces consistent behavior within each graph. Request embeddings are learned by minimizing the consistency loss in Equation [\(2\)](#page-4-1), which preserves strong semantic relations in the embedding space:

<span id="page-4-1"></span>
$$\mathcal{L}_{\text{cons}} = \left\| A - \sigma(ZZ^{\top}) \right\|_F^2, \tag{2}$$

where A is the semantic similarity matrix for a template group, Z is the learned request embedding matrix, and σ(·) is the sigmoid function.

To produce discrete API behavior clusters, we add a clustering regularization term that encourages compact and stable groups in the embedding space. The final semantic clustering objective is:

$$\mathcal{L} = \mathcal{L}_{cons} + \lambda \mathcal{L}_{clus}, \tag{3}$$

where Lclus is the clustering regularization term, and λ controls the trade-off between behavior consistency and cluster separation. Graph-based semantic clustering is used only when sufficient samples and dense similarity graphs are available; otherwise, we fall back to K-means on the feature vectors to ensure robustness.

#### Algorithm 1: Two-Stage Clustering with Structural Templates and Semantic Graphs

```
Input: Normalized API paths {pˆi}, request feature vectors {xi}
  Output: Discovered API assets C
1 Stage 1: Template Mining;
2 Build prefix tree over {pˆi} using Drain3;
3 Assign each request to a template group Gk;
4 Stage 2: Semantic refinement; // separate behaviors under
    same template
5 C ← ∅;
6 foreach template group Gk do
7 if |Gk| < 3 then
8 C ← C ∪ {Gk} continue
9 Build similarity graph A from {xi}i∈Gk
                                       ; // semantic affinity
10 if DAEGC is applicable on A then
11 Train DAEGC on (A, {xi}); // split semantic
            behaviors
12 Ck ← cluster assignments from DAEGC;
13 else
14 Ck ← KMeans({xi}); // fallback
15 end
16 C ← C ∪ Ck;
17 end
18 return C;
```

#### IV. EXPERIMENT DESIGN

#### <span id="page-4-0"></span>*A. Research Questions*

To evaluate the proposed method from multiple perspectives, we formulate three research questions (RQs).

#### RQ1. How effective is APISENSOR in discovering APIs across different applications?

*Motivation.* Effectiveness is a fundamental requirement of any API discovery approach. In many practical scenarios, API traffic is collected from a single application with limited cross-project interference. Under such settings, an API discovery method should accurately identify API structures with *high precision*, avoiding incorrect endpoint merges, while maintaining robust performance across different applications. Therefore, RQ1 evaluates the effectiveness of APISENSOR on multiple representative web applications, with particular attention to its precision and cross-project robustness, and compares it against existing baseline methods.

#### RQ2. How robust is APISENSOR to noise in diverse API traffic?

*Motivation.* Robustness is critical for deploying API discovery methods in practical analysis environments. In real-world traffic, API requests often originate from multiple applications and are affected by various types and levels of noise. Under such conditions, an API discovery method should maintain stable performance despite interference. Therefore, RQ2 evaluates the robustness of APISENSOR under mixed multi-project traffic with different noise types and noise levels, and compares its performance stability against baseline approaches.

#### RQ3. How does each component contribute to the overall effectiveness of APISENSOR?

*Motivation.* Understanding the contribution of individual components is essential for validating the design of a complex API discovery system. APISENSOR adopts a multistage pipeline composed of several interacting components. Under such a design, the overall effectiveness may depend on the joint impact of these components rather than any single module. Therefore, RQ3 investigates the contribution of each component through ablation studies to assess its impact on the overall effectiveness of APISENSOR.

#### *B. Studied Applications*

To evaluate APISENSOR under realistic multi-tenant *web application* settings, we select six open-source web applications using explicit and systematic criteria. Specifically, the selected projects must (1) cover diverse functional domains to avoid application-specific bias; (2) exhibit heterogeneous architectures, including both monolithic and microservice-based designs; (3) expose a non-trivial set of structured HTTP(S) APIs that are exercised during normal user interactions; and (4) be actively maintained and practically relevant, as reflected by community adoption and recent updates.

<span id="page-4-2"></span>TABLE II BASIC CHARACTERISTICS OF THE SELECTED WEB APPLICATIONS. REQS.: NUMBER OF HTTP(S) REQUESTS COLLECTED; EPS: NUMBER OF UNIQUE API ENDPOINTS; UPD.: LAST MAJOR UPDATE YEAR.

| Project            |        |         |    | Version Req. Eps Function | Scale             | Stars Upd. |      |
|--------------------|--------|---------|----|---------------------------|-------------------|------------|------|
| Train-Ticket 1.0.0 |        | 6564 13 |    | Ticket booking            | Small             | 2k         | 2024 |
| Humhub             | 1.15.1 | 3957 18 |    | Social networking         | Medium 6.6k       |            | 2025 |
| Memos              | 0.23.0 | 508     | 25 | Note taking               | Medium 47.3k 2025 |            |      |
| Overleaf           | 5.2.1  | 162     | 32 | Collaborative editing     | Large             | 17k        | 2025 |
| Nextcloud          | 32.0.3 | 107     | 20 | Cloud storage             | Large             | 33.6k 2025 |      |
| Dify               | 1.9.0  | 1354 91 |    | LLM workflow platform     | Large             | 122k 2026  |      |

Based on these criteria, we select six representative opensource web applications, as summarized in Table [II,](#page-4-2) covering

TABLE III ATOMIC NOISE RULES USED FOR NOISY DATASET CONSTRUCTION

<span id="page-5-0"></span>

| Noise Type | Rule                        | Example                                                 |  |  |  |  |
|------------|-----------------------------|---------------------------------------------------------|--|--|--|--|
|            | Query Order Shuffle         | /api/user?id=1&role=admin → /api/user?role=admin&id=1   |  |  |  |  |
|            | Neutral Query Parameter     | /api/user?id=1 → /api/user?id=1&tmp=0                   |  |  |  |  |
|            | Duplicate Query Key         | /api/user?id=1 → /api/user?id=1&id=1                    |  |  |  |  |
|            | Underscore Injection        | /api/user/profile → /api/user_/profile                  |  |  |  |  |
|            | Hyphen Duplication          | /api/user-profile → /api/userprofile                    |  |  |  |  |
|            | Dot Injection               | /api/user → /api/us.er                                  |  |  |  |  |
|            | Repeated Slash              | /api/user/profile → /api//user/profile                  |  |  |  |  |
| Lexify     | Trailing Slash Addition     | /api/user → /api/user/                                  |  |  |  |  |
|            | Trailing Slash Removal      | /api/user/ → /api/user                                  |  |  |  |  |
|            | Uppercase Token             | /api/user → /API/user                                   |  |  |  |  |
|            | Lowercase Token             | /API/User → /api/user                                   |  |  |  |  |
|            | Space Encoding (%20)        | /api/search?q=hello world → /api/search?q=hello%20world |  |  |  |  |
|            | Plus Encoding (+)           | /api/search?q=hello world → /api/search?q=hello+world   |  |  |  |  |
|            | Hex Encoding                | /api/search?q=test → /api/search?q=%74%65%73%74         |  |  |  |  |
|            | Static Asset Request        | /static/app.js, /assets/style.css                       |  |  |  |  |
|            | Image Resource Request      | /images/logo.png, /img/banner.jpg                       |  |  |  |  |
|            | Font and Media Request      | /fonts/main.woff2, /media/intro.mp4                     |  |  |  |  |
|            | Health Check Endpoint       | /health, /status                                        |  |  |  |  |
| Interfere  | Metrics Endpoint            | /metrics, /actuator/metrics                             |  |  |  |  |
|            | Framework Handshake Request | /sockjs/info, /ws/connect                               |  |  |  |  |
|            | Hot Reload / Dev Channel    | /webpack-hmr, /vite/client                              |  |  |  |  |
|            | Third-party Analytics Call  | /analytics/collect, /track/event                        |  |  |  |  |
|            | CDN / Proxy Trace           | /cdn-cgi/trace, /proxy/ping                             |  |  |  |  |

collaborative editing, ticket booking, note taking, social networking, cloud storage, and LLM workflow orchestration. The selected systems exhibit distinct functional roles and architectural styles. Overleaf and Nextcloud represent large-scale collaborative web platforms with intensive and fine-grained API interactions; Train-Ticket is a widely used microservice-based benchmark web system featuring complex inter-service API dependencies; Memos exposes relatively clean and lightweight REST-style APIs typical of single-purpose web applications; Humhub provides modular social networking functionalities with diverse user-driven API behaviors; and Dify is a rapidly growing and actively evolving open-source web platform for LLM-based application development, introducing modern agent-oriented and workflow-driven API interaction patterns.

Each application is deployed locally and exercised through browser-driven interactions to emulate realistic user behaviors. All HTTP(S) traffic is directly captured from Burp Suite Pro configured as an interception proxy, recording complete request–response pairs. As reported in Table [II,](#page-4-2) Req. denotes the total number of captured HTTP(S) requests, while EPs indicates the number of unique API endpoints after normalization and deduplication. To obtain ground-truth semantic labels for evaluation, API endpoints are manually annotated by analyzing the application source code and publicly available API documentation. This labeling process required 32 personhours of manual effort and provides reliable reference labels for assessing the accuracy of API graph construction.

#### *C. Noisy Simulation*

To evaluate the robustness of API endpoint discovery under realistic operating conditions, we construct noisy variants of each single-project dataset by introducing controlled perturbations into the original traffic. These perturbations reflect common artifacts of real-world HTTP-based systems, where API calls coexist with heterogeneous client behaviors and non-API traffic.

We consider two complementary noise types, termed Lexify and Interfere. Lexify models lexical variability within individual API requests, while Interfere models structural interference caused by semantically irrelevant HTTP traffic. Both noise types are applied in a semantics-preserving manner and are used solely for robustness evaluation.

Lexify. Lexify introduces fine-grained syntactic variability within individual HTTP requests without altering the invoked API endpoint. It simulates inconsistencies arising from different client implementations, serialization behaviors, and framework-level preprocessing by applying syntax-preserving transformations such as query parameter reordering, neutral parameter insertion, encoding and delimiter variations, case changes, and trailing-slash modifications.

Interfere. Interfere introduces structural noise by injecting realistic but semantically irrelevant HTTP requests into the API traffic. This models mixed-traffic deployment environments where API calls are interleaved with resource loading, framework-generated background requests, and auxiliary service interactions. The injected requests introduce additional path patterns unrelated to the target API surface and are excluded from ground-truth endpoint annotations.

The complete set of noise rules used by Lexify and Interfere is summarized in Table [III.](#page-5-0) For each single-project dataset, we generate multiple evaluation variants by applying Lexify and Interfere independently. Unless otherwise specified, the injected noise does not modify the original ground-truth endpoint annotations and is used solely to assess robustness under lexical variability and structural distraction.

#### *D. Selected Baseline*

To evaluate API endpoint discovery, we compare our approach with a set of representative baselines that operate at runtime or on semi-structured artifacts. These baselines are grouped into three categories according to their primary discovery mechanism: (1) open-source tools, (2) log-based template mining methods, and (3) API traffic-based endpoint discovery methods.

- (1) Open-source tools extract API endpoint information from runtime request–response traces or network traffic and are widely used for API reverse engineering and specification generation.
  - Optic [\[2\]](#page-12-5). An open-source tool that captures real HTTP traffic to generate and validate OpenAPI specifications, enabling endpoint discovery from observed API interactions.
  - Mitmproxy2Swagger [\[1\]](#page-12-4). A reverse-engineering tool built on mitmproxy that automatically generates OpenAPI specifications from intercepted HTTP/HTTPS traffic, suitable for discovering undocumented or black-box APIs.
- (2) Log-based template mining methods discover API endpoint patterns by mining templates from runtime traffic logs. They extract invariant textual structures that represent endpoint templates, without relying on static specifications or source code.
  - LogCluster [\[25\]](#page-13-8). A data mining-based log clustering algorithm that groups similar log entries by identifying frequent token patterns and replacing variable tokens with wildcards.
  - LogNgram [\[5\]](#page-12-8). A template mining approach that uses token-level n-gram statistics to distinguish static components from dynamic variables in runtime logs.
  - UniParser [\[14\]](#page-12-9). A unified log parsing method that leverages neural encoders to learn common structural and semantic patterns across heterogeneous runtime logs.
  - LogPPT [\[11\]](#page-12-10). A prompt-based log template mining approach that employs pretrained language models to extract templates from runtime logs. We consider both the RoBERTa-based and GPT-based variants under fewshot settings.
- (3) API traffic-based endpoint discovery methods explicitly target API endpoint discovery from runtime observations, documentation, or interaction traces. They are designed to infer API endpoints, path templates, or specifications, rather than general-purpose log templates.
  - Web API Search [\[13\]](#page-12-6). A learning-based approach that supports endpoint-level API discovery by matching natural language queries against API and endpoint descriptions mined from online documentation.
  - APID2Spec [\[36\]](#page-13-18). A documentation-driven approach that extracts API specifications by crawling documentation pages and inferring base URLs, path templates, and HTTP methods.
  - APICARV [\[35\]](#page-13-5). A dynamic analysis technique that infers API endpoints by monitoring runtime API traffic generated through UI interactions and constructing an API graph from observed traces.
  - APIDrain3. An online template mining approach adapted to API traffic, which incrementally extracts URL tem-

plates from streaming API flows for continuous endpoint discovery.

#### *E. Evaluation Metrics*

We evaluate the correctness of API endpoint discovery and the structural quality of clustering using multiple quantitative metrics, covering both endpoint-level accuracy and clustering consistency.

To evaluate the accuracy of discovered API endpoints at the set level, we use Precision of Group Accuracy (PGA), Recall of Group Accuracy (RGA), and the F1-score of Group Accuracy (FGA). Precision measures the proportion of discovered endpoints that correspond to ground-truth endpoints, Recall measures the coverage of ground-truth endpoints, and F1-score provides a balanced summary of the two:

$$\mathbf{PGA} = \frac{TP}{TP + FP}, \qquad \mathbf{RGA} = \frac{TP}{TP + FN},$$

$$\mathbf{FGA} = \frac{2TP}{2TP + FP + FN}.$$
(4)

where T P denotes the number of correctly discovered endpoints, F P the number of spurious endpoints, and F N the number of ground-truth endpoints that are not recovered.

To evaluate whether each predicted cluster corresponds to a single semantic API endpoint, we measure cluster purity(Purity). Let {xi} N <sup>i</sup>=1 denote the set of API endpoint templates, where each template x<sup>i</sup> is associated with a groundtruth label y<sup>i</sup> and a predicted cluster label yˆ<sup>i</sup> . Cluster purity is defined as:

Purity = 
$$\frac{1}{N} \sum_{k} \max_{c} |\{x_i : \hat{y}_i = k \land y_i = c\}|,$$
 (5)

where k indexes predicted clusters and c indexes ground-truth endpoint labels.

Together, these metrics provide a unified evaluation of endpoint discovery accuracy and clustering structure using a consistent notation across all metrics.

#### V. RESULT ANALYSIS

#### <span id="page-6-0"></span>*A. Effectiveness (RQ1)*

To evaluate the ability of APISENSOR to handle diverse projects with different scales and functionalities, we conduct experiments on six projects. The results show that APISEN-SOR achieves strong and stable performance across all projects, demonstrating its effectiveness and robustness under diverse project settings.

APISENSOR achieves the best precision (PGA) across diverse projects. As shown in Table [V,](#page-8-0) on the simple Train-Ticket project, APISENSOR achieves a PGA of 100% and an FGA of 91.67%, while maintaining an RGA of 84.62%, thereby avoiding the over-merging behavior of baselines that reach RGA = 100% at the cost of precision. On medium-scale projects such as Humhub and Memos, APISENSOR maintains high precision, achieving PGA values of 85.71% and 96.15%, respectively, while both projects reach an RGA of 100%, effectively suppressing incorrect endpoint merges. On large and complex projects such as Overleaf and Dify, APISENSOR continues to deliver very high precision, with PGA values of

| Method           | Train-Ticket |        | Humhub |       | Memos  |       | Overleaf |        | Nextcloud |        | Dify   |       |       |        |       |       |       |       |
|------------------|--------------|--------|--------|-------|--------|-------|----------|--------|-----------|--------|--------|-------|-------|--------|-------|-------|-------|-------|
|                  | PGA          | RGA    | FGA    | PGA   | RGA    | FGA   | PGA      | RGA    | FGA       | PGA    | RGA    | FGA   | PGA   | RGA    | FGA   | PGA   | RGA   | FGA   |
| Optic            | 69.23        | 84.62  | 76.15  | 22.22 | 11.11  | 14.81 | 54.17    | 100.00 | 70.27     | 43.75  | 37.50  | 40.38 | 33.33 | 15.01  | 20.69 | 25.00 | 16.48 | 19.87 |
| Mitproxy2Swagger | 8.28         | 100.00 | 15.29  | 75.00 | 100.00 | 85.71 | 55.56    | 100.00 | 71.43     | 38.55  | 100.00 | 55.65 | 54.05 | 100.00 | 70.18 | 40.64 | 97.80 | 57.42 |
| LogCluster       | 86.67        | 100.00 | 92.86  | 90.00 | 100.00 | 94.74 | 78.57    | 88.00  | 83.02     | 34.78  | 25.00  | 29.09 | 77.78 | 35.00  | 48.28 | 71.43 | 60.44 | 65.48 |
| LogNgram         | 86.67        | 100.00 | 92.86  | 64.29 | 100.00 | 78.26 | 75.76    | 100.00 | 86.21     | 46.27  | 96.88  | 62.63 | 82.61 | 95.00  | 88.37 | 67.42 | 97.80 | 79.82 |
| UniParser        | 86.67        | 100.00 | 92.86  | 64.29 | 100.00 | 78.26 | 74.19    | 92.00  | 82.14     | 58.00  | 90.62  | 70.73 | 82.61 | 95.00  | 88.37 | 67.18 | 96.70 | 79.28 |
| LogPPT           | 86.67        | 100.00 | 92.86  | 64.29 | 100.00 | 78.26 | 75.76    | 100.00 | 86.21     | 46.27  | 96.88  | 62.63 | 82.61 | 95.00  | 88.37 | 67.42 | 97.80 | 79.82 |
| LogPPT (GPT5)    | 26.67        | 30.77  | 28.57  | 64.29 | 100.00 | 78.26 | 25.00    | 32.00  | 28.07     | 32.69  | 53.12  | 40.48 | 39.13 | 45.00  | 41.86 | 40.00 | 57.14 | 47.06 |
| WebAPISearch     | 80.00        | 30.77  | 44.44  | 69.23 | 50.00  | 58.06 | 50.00    | 16.00  | 24.24     | 55.00  | 34.38  | 42.31 | 76.92 | 50.00  | 60.61 | 27.78 | 10.99 | 15.75 |
| APID2Spec        | 86.67        | 100.00 | 92.86  | 64.29 | 100.00 | 78.26 | 72.73    | 64.00  | 68.09     | 50.00  | 90.62  | 64.44 | 81.82 | 90.00  | 85.71 | 65.69 | 73.63 | 69.43 |
| APICARV          | 86.67        | 100.00 | 92.86  | 64.29 | 100.00 | 78.26 | 75.76    | 100.00 | 86.21     | 46.27  | 96.88  | 62.63 | 82.61 | 95.00  | 88.37 | 67.42 | 97.80 | 79.82 |
| APIDrain3        | 86.67        | 100.00 | 92.86  | 81.82 | 100.00 | 90.00 | 74.19    | 92.00  | 82.14     | 62.50  | 62.50  | 62.50 | 78.95 | 75.00  | 76.92 | 67.42 | 97.80 | 79.82 |
| APISENSOR        | 100.00       | 84.62  | 91.67  | 85.71 | 100.00 | 92.31 | 96.15    | 100.00 | 98.04     | 100.00 | 93.75  | 96.77 | 94.74 | 90.00  | 92.31 | 98.89 | 97.80 | 98.34 |

TABLE IV PERFORMANCE OF API DISCOVERY ON DIFFERENT PROJECTS (PGA, RGA, FGA IN %)

![](_page_7_Figure_3.jpeg)

<span id="page-7-0"></span>Fig. 4. Performance Stability of API Endpoint Discovery Methods Across Diverse Projects (PGA, RGA, FGA in %)

100% and 98.89%, demonstrating strong robustness as project scale and API complexity increase.

APISENSOR consistently achieves the best overall performance (FGA) across projects of different scales. It achieves the highest FGA on all six projects, with particularly large improvements over the strongest baselines on Overleaf (96.77%, +26.04), Memos (98.04%, +11.83), and Dify (98.34%, +18.52). On medium-scale projects, APISENSOR achieves FGA values of 92.31% on Humhub and 98.04% on Memos, benefiting from its balanced precision and recall. On large and complex projects, it substantially outperforms all baseline methods, reaching an FGA of 96.77% on Overleaf, 92.31% on Nextcloud, and 98.34% on Dify, demonstrating strong scalability and robustness to complex API semantics.

APISENSOR demonstrates the most stable high-

performance on both PGA and FGA across diverse projects. As shown in Figure [4,](#page-7-0) the PGA and FGA values of APISENSOR are tightly clustered near the upper bound with small interquartile ranges and few outliers, indicating consistently strong performance rather than occasional peaks. Quantitatively, APISENSOR achieves an average PGA of 95.92% and an average FGA of 94.91% across six projects, with low variances of 24.63 and 8.17, respectively. This shows that the high precision and overall accuracy of APISENSOR are maintained consistently across projects of different scales and functionalities, demonstrating strong robustness to project diversity.

Answer to RQ1: APISENSOR achieves the best API endpoint discovery performance across all projects. It consistently attains the highest precision, resulting in the fewest false-positive endpoint merges, with an average PGA of 95.92%. Meanwhile, it achieves the highest overall accuracy on every project, with an average FGA of 94.91%, while remaining the most stable across diverse projects.

#### *B. Robustness (RQ2)*

To evaluate the robustness of APISENSOR under noisy and mixed API traffic, we conduct experiments with increasing levels of cross-application interference and lexical noise. The results show that APISENSOR consistently maintains superior performance under all noise settings, demonstrating strong robustness to interference in diverse and realistic API traffic.

Under the Standard setting, where API traffic from multiple projects is collected simultaneously at the gateway side, APISENSOR consistently outperforms all baselines across all evaluation metrics. As shown in Table [V,](#page-8-0) APISEN-SOR achieves a PGA of 98.25, an RGA of 84.85, and an FGA of 91.06, while also maintaining high clustering purity (91.24). In contrast, baseline methods typically exhibit a clear trade-off between precision and recall, achieving very high RGA (e.g., up to 98.48) at the cost of substantially lower PGA (around 68.18), indicating aggressive and error-prone

<span id="page-8-0"></span>Method Standard Interfere Lexify PGA RGA FGA Purity PGA RGA FGA Purity PGA RGA FGA Purity Optic 24.00 38.89 29.68 4.81 17.78(↓6.22) 38.89(−) 24.40(↓5.28) 4.81(−) 18.38(↓5.62) 39.39(↑0.50) 25.07(↓4.61) 4.81(−) Mitproxy2Swagger 24.20 19.19 21.41 3.80 7.58(↓16.62) 7.58(↓11.61) 7.58(↓13.83) 3.04(↓0.76) 6.85(↓17.35) 7.58(↓11.61) 7.19(↓14.22) 3.04(↓0.76) LogCluster 73.65 62.12 67.40 90.06 57.21(↓16.44) 62.12(−) 59.56(↓7.84) 90.56(↑0.50) 66.85(↓6.80) 62.12(−) 64.40(↓3.00) 89.06(↓1.00) LogNgram 68.18 98.48 80.58 90.68 54.47(↓13.71) 98.48(−) 70.14(↓10.44) 91.85(↑1.17) 50.92(↓17.26) 97.47(↓1.01) 66.90(↓13.68) 89.89(↓0.79) UniParser 71.43 95.94 81.90 90.45 56.51(↓14.92) 96.46(↑0.52) 71.27(↓10.63) 91.55(↑1.10) 55.29(↓16.14) 94.95(↓0.99) 69.89(↓12.01) 89.55(↓0.90) LogPPT 68.18 98.48 80.58 90.68 54.47(↓13.71) 98.48(−) 70.14(↓10.44) 91.85(↑1.17) 51.88(↓16.30) 97.47(↓1.01) 67.72(↓12.86) 89.95(↓0.73) LogPPT (GPT5) 43.40 58.08 49.68 90.34 33.14(↓10.26) 58.08(−) 42.20(↓7.48) 91.55(↑1.21) 33.24(↓10.16) 57.07(↓1.01) 42.01(↓7.67) 89.54(↓0.80) WebAPISearch 51.76 22.22 31.10 48.36 33.33(↓18.43) 22.22(−) 26.67(↓4.43) 51.93(↑3.57) 48.89(↓2.87) 22.22(−) 30.56(↓0.54) 48.99(↑0.63) APID2Spec 67.66 80.30 73.44 86.34 50.81(↓16.85) 79.29(↓1.01) 61.93(↓11.51) 88.66(↑2.32) 48.58(↓19.08) 77.78(↓2.52) 59.81(↓13.63) 85.50(↓0.84) APICARV 68.18 98.48 80.58 90.68 54.47(↓13.71) 98.48(−) 70.14(↓10.44) 91.85(↑1.17) 51.88(↓16.30) 97.47(↓1.01) 67.72(↓12.86) 89.89(↓0.79) APIDrain3 72.24 89.39 79.91 90.16 56.15(↓16.09) 89.90(↑0.51) 69.13(↓10.78) 91.00(↑0.84) 55.17(↓17.07) 88.89(↓0.50) 68.09(↓11.82) 89.25(↓0.91)

APISENSOR 98.25 84.85 91.06 91.24 97.66(↓0.59) 84.34(↓0.51) 90.51(↓0.55) 91.72(↑0.48) 83.59(↓14.66) 82.32(↓2.53) 82.95(↓8.11) 92.16(↑0.92)

TABLE V SINGLE-PROJECT API ENDPOINT DISCOVERY PERFORMANCE

endpoint merging. These results show that APISENSOR can accurately distinguish endpoints across multiple coexisting projects without relying on over-merging strategies.

![](_page_8_Figure_4.jpeg)

<span id="page-8-1"></span>Fig. 5. Robustness of API discovery under increasing noise ratios (Interfere and Lexify).

When cross-application interference is introduced, APISENSOR is affected the least and maintains the highest performance. Under the Interfere setting, baseline methods suffer noticeable degradation, with FGA dropping to 59.56– 71.27 due to confusion caused by interleaved traffic patterns. In contrast, APISENSOR maintains a PGA of 97.66 and an RGA of 84.34, resulting in an FGA of 90.51, with only a marginal decrease of 0.55 compared to the Standard setting. This demonstrates that APISENSOR remains highly robust to cross-application noise when deployed in realistic gateway environments.

Even under the most challenging Lexify setting, APISENSOR continues to deliver the strongest performance with the smallest degradation. While baseline methods degrade substantially when lexical cues are weakened, achieving at most an FGA of 69.89, APISENSOR still attains a PGA of 83.59 and an RGA of 82.32, yielding an FGA of 82.95. Despite the increased difficulty, APISENSOR preserves a clear performance margin over all baselines, indicating strong generalization ability beyond surface-level lexical similarity in highly heterogeneous, multi-application traffic.

APISENSOR remains the most robust method as noise increases. As shown in Figure [5,](#page-8-1) when the noise ratio increases under both the Interfere and Lexify settings, APISEN-SOR consistently maintains the highest FGA and Purity among all methods. While the performance of baseline approaches drops noticeably as noise intensifies, APISENSOR degrades only slightly. Specifically, its FGA decreases by less than 4% as the noise ratio increases from 5% to 95%. Even at very high noise levels (e.g., 75% and 95%), APISENSOR still preserves a clear performance margin over all baselines. These results demonstrate that APISENSOR is highly resilient to crossapplication interference and lexical corruption, maintaining stable API discovery performance under increasingly noisy traffic.

Answer to RQ2: APISENSOR consistently maintains the highest API endpoint discovery performance under all noisy settings, even in the presence of cross-application interference and weakened lexical cues. Moreover, as the noise ratio increases, APISENSOR exhibits the slowest performance degradation among all methods, demonstrating the strongest robustness to increasing noise in diverse and realistic API traffic.

#### *C. Ablation Study (RQ3)*

To quantify the contribution of each component in APISEN-SOR, we conduct a comprehensive ablation study under all three evaluation settings: *Standard*, *Interfere*, and *Lexify*. This design allows us to examine not only the standalone effec-

![](_page_9_Figure_1.jpeg)

<span id="page-9-1"></span>Fig. 6. The t-SNE visualizations of API endpoint representations under different modeling configurations and noise conditions.

tiveness of each component, but also its role under increasing levels of structural interference and lexical variability.

APISENSOR consists of three key components: (1) *NF*, which normalizes raw HTTP requests to suppress instancelevel noise; (2) *Structural Template Mining*, implemented using Drain3 to extract canonical API templates; and (3) *Graph-based Representation Learning*, implemented via the DAEGC module to jointly model structural and semantic relationships. We construct three ablated variants by removing one component at a time while keeping the rest of the pipeline unchanged.

TABLE VI ABLATION RESULTS OF APISENSOR.

<span id="page-9-0"></span>

|           | Set.      | PGA   | RGA   | FGA                                                     | Purity |
|-----------|-----------|-------|-------|---------------------------------------------------------|--------|
|           | APISENSOR | 98.28 | 86.36 | 91.94                                                   | 93.17  |
| Standard  | w/o NF    |       |       | 32.60(↓65.68) 82.32(↓4.04) 46.70(↓45.24) 89.00(↓4.17)   |        |
|           | w/o DS    |       |       | 92.11(↓6.17) 17.68(↓68.68) 29.66(↓62.28) 37.37(↓55.80)  |        |
|           | w/o GC    |       |       | 98.58(↑0.30) 70.20(↓16.16) 82.01(↓9.93) 85.66(↓7.51)    |        |
|           | APISENSOR | 97.69 | 85.35 | 91.11                                                   | 92.04  |
| Interfere | w/o NF    |       |       | 25.35(↓72.34) 63.64(↓21.71) 36.26(↓54.85) 76.60(↓15.44) |        |
|           | w/o DS    |       |       | 86.84(↓10.85) 16.67(↓68.68) 27.97(↓63.14) 37.37(↓54.67) |        |
|           | w/o GC    |       |       | 97.86(↑0.17) 69.19(↓16.16) 81.07(↓10.04) 85.39(↓6.65)   |        |
|           | APISENSOR | 83.76 | 83.33 | 83.54                                                   | 92.56  |
| Lexify    | w/o NF    |       |       | 29.59(↓54.17) 79.80(↓3.53) 43.17(↓40.37) 87.41(↓5.15)   |        |
|           | w/o DS    |       |       | 92.11(↑8.35) 17.68(↓65.65) 29.66(↓53.88) 36.78(↓55.78)  |        |
|           | w/o GC    |       |       | 80.65(↓3.11) 63.13(↓20.20) 70.82(↓12.72) 87.96(↓4.60)   |        |

*Note:* w/o NF removes URL normalization and request canonicalization; w/o Drain3 removes structural template mining; w/o Graph replaces graph-based deep clustering with K-means.

Effect of Noise Filtering (NF). As shown in Table [VI,](#page-9-0) removing NF causes substantial performance degradation across all settings, mainly affecting precision-related metrics. Under *Standard*, PGA drops from 98.28 to 32.60 (↓65.68) and FGA from 91.94 to 46.70 (↓45.24), while RGA only slightly decreases by 4.04. Similar trends are observed under *Interfere*, where PGA and FGA decrease by 72.34 and 54.85, respectively. The impact is most pronounced under *Lexify*, with PGA dropping by 54.17 and FGA by 40.37, indicating that normalization is crucial for mitigating lexical noise and preserving cluster precision.

Effect of Structural Template Mining (Drain3). Removing structural template mining leads to severe recall collapse and purity degradation across all settings. In the *Standard* setting, RGA drops sharply from 86.36 to 17.68 (↓68.68) and Purity from 93.17 to 37.37 (↓55.80). A similar pattern holds under *Interfere* and *Lexify*, where RGA consistently falls by over 65 points. The results in Table [VI](#page-9-0) show that template abstraction provides essential structural guidance for distinguishing API endpoints, especially in noisy environments.

Effect of Graph-based Representation Learning (DAEGC). As shown in Table [VI,](#page-9-0) replacing DAEGC with K-means mainly affects recall and overall clustering quality. Under *Standard*, RGA decreases from 86.36 to 70.20 (↓16.16) and FGA from 91.94 to 82.01 (↓9.93), while PGA slightly increases. Comparable degradations are observed under *Interfere* and *Lexify*, with FGA drops of 10.04 and 12.72, respectively. This indicates that graph-based joint optimization is critical for maintaining coherent clustering under interference and cross-project scenarios.

Figure [6](#page-9-1) provides a qualitative analysis of learned API endpoint representations, showing that APISENSOR consistently achieves strong endpoint-level discriminability, while representation quality degrades in a structured and interpretable manner as modeling components are removed and noise is introduced.

In standard conditions, the full pipeline produces compact and well-separated clusters, with each endpoint occupying a distinct region in the embedding space. The first row in Figure [6](#page-9-1) indicates that the learned representations can reliably distinguish endpoints even across multiple projects. When individual components are ablated, clusters become less compact and their boundaries more fragmented, suggesting that strong discriminability already relies on the joint contribution of lexical, structural, and relational modeling.

As semantic interference is introduced, the full model largely preserves inter-endpoint separation, whereas ablated configurations exhibit increasing overlap between clusters. Interfering samples blur the boundaries between endpoints in the embedding space as shown in Figure [6,](#page-9-1) indicating that higher-level structural abstraction and graphbased relational learning are essential for preventing semantic noise from collapsing global discriminability.

Under lexical perturbations, representation degradation follows a different pattern. Endpoint identities are not entirely lost; samples associated with the same endpoint still form locally compact groups in the Figure [6.](#page-9-1) However, these groups become spatially fragmented and lose consistent relative positioning, resulting in an embedding space with weak global geometric coherence. As a consequence, discriminability becomes highly localized and unstable, demonstrating that effective lexical normalization is a prerequisite for maintaining coherent and globally discriminative endpoint representations.

Answer to RQ3: The core components of APISENSOR are all indispensable. Removing any component leads to clear degradation in endpoint clustering, not only in overall performance but also in the stability and sharpness of clustering boundaries, as further evidenced by the representation visualizations. Together, these components are necessary to produce coherent, well-separated, and robust API endpoint representations under noise.

#### VI. DISCUSSION

<span id="page-10-0"></span>*A. Shadow APIs Revealed by Runtime Traffic: Evidence from the Case Study of Dify*

During the evaluation of APISENSOR, we observed a clear inconsistency between the official API documentation of Dify and the API endpoints exercised at runtime. A number of API endpoints repeatedly appeared in network traffic traces but were missing from the API Reference at the time of our study. These endpoints are callable, actively used by the system, and essential for Console-level functionalities, yet remain undocumented or only indirectly described. Such undocumented but operational interfaces constitute a class of *shadow APIs* that are invisible to documentation-centric API discovery approaches.

Representative examples of these shadow APIs span different functional modules. In the Datasets module, endpoints such as /console/api/datasets/{id}/metadata and /console/api/datasets/{id}/error-docs were frequently observed during dataset management operations but absent from the API Reference. In the Apps module, we identified undocumented endpoints including /console/api/apps/{id}/api-keys, which is essential for application integration and key management, and /console/api/apps/{id}/advanced-chat/workf low-runs, which supports workflow execution monitoring. These endpoints represent core application functionalities, yet they are not discoverable by developers or agents relying solely on the documented API surface.

To validate that these findings reflected genuine documentation gaps rather than artifacts of traffic analysis, we reported the discovered inconsistencies to the Dify developer community through an official documentation issue. A core collaborator acknowledged that, due to legacy reasons and rapid system evolution, the API reference had become out of sync with the implementation and contained notable gaps. The maintainers further indicated ongoing efforts to consolidate the API Reference as the single source of truth. This independent confirmation substantiates that the identified endpoints correspond to real and practically relevant shadow APIs.

This case study illustrates how shadow APIs naturally emerge in evolving web applications, even in actively maintained open-source projects. From a software engineering perspective, the presence of such shadow APIs complicates reuse, automation, and reliable integration. Developers and LLM-based agents relying solely on official API references may incorrectly assume that certain functionalities do not exist. The Dify case demonstrates that black-box, traffic-based API discovery is essential for reconstructing the effective API surface of real-world systems. By grounding API discovery in observed runtime behavior, APISENSOR enables systematic identification of shadow APIs and provides a more faithful representation of application functionality than documentationbased approaches alone.

#### *B. Implications for LLM-Based and Tool-Using Agents*

The emergence of sophisticated autonomous agents such as Clawbot (also known as Moltbot or OpenClaw) underscores the transformative potential of LLM-based and tool-using agents in software ecosystems and end-user workflows. Unlike traditional chatbots that primarily provide text responses, agents like Clawbot integrate deeply with existing applications and infrastructure to perform concrete actions, such as interacting with messaging platforms, executing local system commands, managing calendars, and orchestrating workflows across services. They are designed to operate persistently, retain long-term memory, and bridge natural language instruction with executable operations on behalf of human users. These capabilities represent a new class of agent behavior that transcends conventional prompt-response interactions and moves toward truly autonomous software assistants.

From the perspective of API discovery, such agents require reliable and comprehensive knowledge of the target system's API surface in order to fulfill user intents accurately. Incomplete or outdated documentation—as exemplified by the shadow APIs in Dify—poses a significant obstacle for LLM-based agents that rely on documentation to generate correct invocation sequences and compose complex behaviors. If key interfaces are undocumented, agents may either be unable to perform certain tasks or may generate incorrect API invocations, leading to failed executions or unintended side effects. Furthermore, dynamic capabilities such as workflow orchestration, permission management, and contextual decision making demand fine-grained API discovery that goes beyond static endpoint descriptions.

The Clawbot example illustrates a broader trend in which autonomous agents are increasingly expected to handle realworld tasks and integrate with existing digital ecosystems in a seamless manner. Agents that can access multiple platforms (e.g., messaging apps, local system resources, external services) and execute multi-step operations inherently depend on accurate API knowledge to translate high-level user goals into low-level actions. Therefore, methodologies like trafficbased API discovery, which can systematically uncover both documented and shadow APIs, provide a critical foundation for empowering LLM-based agents to operate reliably in complex environments.

Looking forward, comprehensive API discovery and modeling will enable several key advancements for agent-centric systems. First, it will improve the automation capabilities of agents, allowing them to perform tasks such as end-to-end workflow execution, proactive monitoring, and service configuration without manual intervention. Second, it will facilitate safer and more predictable agent behavior by reducing reliance on incomplete or inaccurate documentation. Third, accurate API discovery will support the development of higher-order reasoning and planning capabilities in agents, enabling them to sequence dependent operations, handle error conditions, and adapt to evolving application surfaces. Ultimately, integrating robust API discovery into agent frameworks will be essential for realizing the promise of autonomous software agents that operate as reliable collaborators across diverse software ecosystems.

#### VII. LIMITATIONS AND FUTURE WORK

Despite the promising results achieved by APISENSOR, our study has several limitations that point to important directions for future research. The primary limitation lies in the end-to-end completeness of runtime traffic collection. While APISENSOR is capable of accurately discovering APIs from observed traffic, the effectiveness of the discovery process is inherently bounded by the coverage of the collected runtime interactions.

In our current experimental setup, runtime traffic was generated through manual and semi-natural interactions, such as daily usage, exploratory clicking, and execution of common workflows within the target web applications. Although this approach reflects realistic usage scenarios and captures a diverse set of API interactions, it does not guarantee exhaustive coverage of all reachable API endpoints. As a result, APIs that are guarded by rare conditions, deep interaction paths, or specific user roles may remain undiscovered. Achieving fully end-to-end API discovery therefore requires not only robust traffic analysis, but also systematic and automated generation of triggering interactions that exercise the full functional surface of the application.

Automated interaction and test generation represents a promising complementary direction to address this limitation. Recent work such as APICARV [\[35\]](#page-13-5) demonstrates the feasibility of mining executable interaction paths from existing test cases to systematically explore API behaviors. Integrating such automated test-driven or behavior-driven interaction generation techniques with traffic-based API discovery could significantly improve coverage and reduce reliance on manual exploration. In particular, combining automated click-path generation with runtime traffic analysis may enable scalable, end-to-end discovery of web APIs across diverse applications with minimal human intervention.

Looking forward, we envision a unified framework in which automated interaction generation continuously stimulates application behaviors, while traffic-based analysis incrementally reconstructs and refines the API surface. Such an approach would further enhance the generality and practicality of blackbox API discovery, making it applicable to large-scale, continuously evolving web systems. Exploring the integration of automated testing, agent-based exploration, and traffic-based API inference remains an important avenue for future work.

#### VIII. THREATS TO VALIDITY

#### <span id="page-11-0"></span>*A. Construct Validity*

A threat to construct validity arises from the construction of the runtime traffic dataset. The traffic traces are manually collected through controlled executions, which may not exhaustively cover all possible API endpoints or rare execution paths. To mitigate this threat, we repeatedly exercised core functionalities of each application and validated collected traffic against official documentation and observed runtime behavior. Only endpoints that were confirmed to be callable and semantically meaningful were annotated as valid APIs. Although the dataset may be incomplete, the collected traffic and labels are accurate and sufficient for evaluating API discovery precision and robustness, which are the primary goals of this study.

#### *B. Internal Validity*

Internal validity may be affected by design choices in preprocessing and clustering, such as traffic filtering, path normalization, and parameter settings, which could influence the discovery results. To reduce this risk, all preprocessing steps are applied consistently, and baseline methods are evaluated under their commonly used configurations without datasetspecific tuning. In addition, we conduct ablation studies to examine the impact of each major component in APISEN-SOR, showing that the performance improvements cannot be attributed to a single heuristic or implementation artifact.

#### *C. External Validity*

The external validity of our results may be limited by the scope of evaluated applications and experimental environments. Although we study six real-world web applications from different domains, the findings may not generalize to all systems, such as highly customized enterprise applications or those using non-standard communication protocols. Moreover, real-world traffic collection environments may introduce more complex noise than our simulated settings. To address this concern, we evaluate robustness under multiple noise types and levels, and observe stable performance trends, suggesting that the conclusions are likely to hold under practical deployment conditions, albeit with potential minor performance variation.

#### IX. CONCLUSION

<span id="page-12-12"></span>In this paper, we propose APISENSOR, a black-box API discovery framework that reconstructs application APIs from mixed runtime traffic under unsupervised settings. By integrating traffic denoising with a two-stage clustering design based on structural templates and graph-based refinement, APISENSOR reduces false positives and improves discovery precision in heterogeneous traffic environments. Experiments on six real-world web applications show that APISENSOR achieves state-of-the-art accuracy while maintaining strong robustness under different noise conditions. Ablation studies further confirm the necessity of each design component. In addition, our evaluation reveals inconsistencies between official API documentation and actual API usage in one application, demonstrating the practical value of runtime-based API discovery. Overall, APISENSOR provides an effective solution for accurate API discovery in closed-source and mixed-traffic environments.

#### DATA AVAILABILITY

All source code and datasets used in this study are open source and anonymous. The source code and datasets are released at:<https://figshare>

#### REFERENCES

- <span id="page-12-4"></span>[1] [n. d.]. mitmproxy2swagger: Automatically Convert Mitmproxy Captures to OpenAPI. [https://github.com/](https://github.com/alufers/mitmproxy2swagger) [alufers/mitmproxy2swagger.](https://github.com/alufers/mitmproxy2swagger) Open-source tool.
- <span id="page-12-5"></span>[2] [n. d.]. Optic: API Specification Generation and Validation from Traffic. [https://github.com/opticdev/optic.](https://github.com/opticdev/optic) Open-source tool.
- <span id="page-12-0"></span>[3] Mohana Basu. 2026. OPENCLAW CHATBOTS ARE RUNNING AMOK: SCHOLARS ARE LISTENING. *Nature* 650 (2026), 533.
- <span id="page-12-17"></span>[4] Cong Chen and Kang Zhang. 2014. Who asked what: Integrating crowdsourced faqs into api documentation. In *Companion Proceedings of the 36th International Conference on Software Engineering*. ACM, 456–459.
- <span id="page-12-8"></span>[5] Haibo Dai, Heng Li, Chih-Sheng Chen, Weiyi Shang, and Tse-Hsun Chen. 2022. Logram: Efficient Log Parsing Using n-Gram Dictionaries. *IEEE Transactions on Software Engineering* 48 (2022).
- <span id="page-12-13"></span>[6] Tiago Espinha, Andy Zaidman, and Hans-Gerhard Gross. 2014. Web API growing pains: Stories from client developers and their code. In *Proceedings of the 18th European Conference on Software Maintenance and Reengineering (CSMR-WCRE)*. IEEE, 84–93.

- <span id="page-12-7"></span>[7] Xiaodong Gu, Hongyu Zhang, Dongmei Zhang, and Sunghun Kim. 2016. Deep API learning. In *Proceedings of the 2016 24th ACM SIGSOFT international symposium on foundations of software engineering*. ACM, 631– 642.
- <span id="page-12-11"></span>[8] Xinyu Han, Yuan Gao, Gabriel Parmer, and Timothy Wood. 2024. Byways: High-Performance, Isolated Network Functions for Multi-Tenant Cloud Servers. In *Proceedings of the 2024 ACM Symposium on Cloud Computing*. ACM.
- <span id="page-12-15"></span>[9] Qiao Huang, Xin Xia, Zhenchang Xing, David Lo, and Xinyu Wang. 2018. API method recommendation without worrying about the task-API knowledge gap. In *Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering*. ACM, 293–304.
- <span id="page-12-2"></span>[10] Ruidong Huang, Mohit Motwani, Isabella Martinez, and Anderson Orso. 2024. Generating REST API Specifications through Static Analysis. In *Proceedings of the 46th IEEE/ACM International Conference on Software Engineering*. ACM, 1–13.
- <span id="page-12-10"></span>[11] Van-Hoang Le and Hongyu Zhang. 2023. Log parsing with prompt-based few-shot learning. In *2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)*. IEEE, 2438–2449.
- <span id="page-12-1"></span>[12] Zhiqiang Lin, Xiangyuan Liu, Jianing Wang, and Zhenkai Liang. 2023. Detecting API Post-Handling Bugs Using Code and Inference. In *Proceedings of the 32nd USENIX Security Symposium*. USENIX Association, 1– 18.
- <span id="page-12-6"></span>[13] Li Liu, Mohammad Bahrami, Jongmin Park, and Wen-Pin Chen. 2020. Web API Search: Discover Web API and Its Endpoint with Natural Language Queries. In *Proceedings of the International Conference on Web Services (ICWS)*. IEEE.
- <span id="page-12-9"></span>[14] Yiming Liu, Xu Zhang, Shilin He, Haixun Zhang, Li Li, Yang Kang, Yifan Xu, Ming Ma, Qingwei Lin, Yingnong Dang, Saravanakumar Rajmohan, and Dongmei Zhang. 2022. UniParser: A Unified Log Parser for Heterogeneous Log Data. In *Proceedings of The ACM Web Conference 2022*. ACM, 1893–1901.
- <span id="page-12-18"></span>[15] Logpai. 2019. Drain3: A robust streaming log template miner.<https://github.com/logpai/Drain3>
- <span id="page-12-3"></span>[16] Chengpeng Luo, Yicheng Ouyang, Yanyang Zhao, Jian Zhang, Yu Jiang, and Zijiang Yang. 2024. Holistic Concolic Execution for Dynamic Web Applications via Symbolic Interpreter Analysis. In *Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security*. ACM.
- <span id="page-12-16"></span>[17] Collin McMillan, Mark Grechanik, Denys Poshyvanyk, Qing Xie, and Chen Fu. 2011. Portfolio: finding relevant functions and their usage. In *Proceedings of the 33rd International Conference on Software Engineering*. ACM, 111–120.
- <span id="page-12-14"></span>[18] Lauren Murphy, Tosin Alliyu, Andrew Macvean, Mary Beth Kery, and Brad A Myers. 2017. Preliminary analysis of REST API style guidelines. *Ann Arbor* 1001 (2017).

- <span id="page-13-6"></span>[19] Sasho Nedelkoski, Jasmin Bogatinovski, Alexander Acker, Jorge Cardoso, and Odej Kao. 2020. Selfsupervised log parsing. In *Joint European Conference on Machine Learning and Knowledge Discovery in Databases*. Springer, 122–138.
- <span id="page-13-13"></span>[20] Kristian Nybom, Adnan Ashraf, and Ivan Porres. 2018. A systematic mapping study on API documentation generation approaches. In *2018 44th euromicro conference on software engineering and advanced applications (SEAA)*. IEEE, 462–469.
- <span id="page-13-12"></span>[21] OpenAPI Initiative. 2023. OpenAPI Specification. [https:](https://www.openapis.org) [//www.openapis.org](https://www.openapis.org)
- <span id="page-13-14"></span>[22] Xin Peng, Yifan Zhao, Mingwei Liu, Fengyi Zhang, Yang Liu, Xin Wang, and Zhenchang Xing. 2018. Automatic Generation of API Documentations for Open-Source Projects. In *2018 IEEE Third International Workshop on Dynamic Software Documentation (DySDoc3)*. IEEE, 7– 8.
- <span id="page-13-16"></span>[23] Mohammad Masudur Rahman, Chanchal K Roy, and David Lo. 2016. Rack: Automatic api recommendation using crowdsourced knowledge. In *2016 IEEE 23rd International Conference on Software Analysis, Evolution, and Reengineering (SANER)*. IEEE, 349–359.
- <span id="page-13-2"></span>[24] Lin Shi, Hao Zhong, Tao Xie, and Mingshu Li. 2011. An empirical study on evolution of API documentation. In *International Conference on Fundamental Approaches To Software Engineering*. Springer, 416–431.
- <span id="page-13-8"></span>[25] Risto Vaarandi and Margus Pihelgas. 2015. LogCluster: A Data Clustering and Pattern Mining Algorithm for Event Logs. In *Proceedings of the 11th International Conference on Network and Service Management (CNSM)*. IEEE.
- <span id="page-13-11"></span>[26] Tim Van Ede, R. Bortolameotti, et al. 2020. Flow-Print: Semi-Supervised Mobile-App Fingerprinting on Encrypted Network Traffic. In *Proceedings of the 27th Annual Network and Distributed System Security Symposium*.
- <span id="page-13-9"></span>[27] Felix Wallner, Bernhard A. Aichernig, and Christian Burghard. 2024. It's Not a Feature, It's a Bug: Fault-Tolerant Model Mining from Noisy Data. In *Proceedings of the 46th IEEE/ACM International Conference on Software Engineering*. ACM, 1–12.
- <span id="page-13-1"></span>[28] Chenlong Wang, Zhaoyang Chu, Zhengxiang Cheng, Xuyi Yang, Kaiyue Qiu, Yao Wan, Zhou Zhao, Xuanhua Shi, Hai Jin, and Dongping Chen. 2025. CodeSync: Synchronizing Large Language Models with Dynamic Code Evolution at Scale. In *International Conference on Machine Learning*. PMLR, 62672–62700.
- <span id="page-13-7"></span>[29] Chun Wang, Shirui Pan, Ruiqi Hu, Guodong Long, Jing Jiang, and Chengqi Zhang. 2019. Attributed Graph Clustering: A Deep Attentional Embedding Approach. In *Proceedings of the 28th International Joint Conference on Artificial Intelligence (IJCAI)*. IJCAI, 3670–3676.
- <span id="page-13-15"></span>[30] Chong Wang, Xin Peng, Mingwei Liu, Zhenchang Xing, Xuefang Bai, Bing Xie, and Tuo Wang. 2019. A learning-based approach for automatic construction of domain glossary from source code and documentation. In *Proceedings of the 2019 27th ACM joint meeting on*

- *european software engineering conference and symposium on the foundations of software engineering*. ACM, 97–108.
- <span id="page-13-4"></span>[31] Chengpeng Wang, Jipeng Zhang, Rongxin Wu, and Charles Zhang. 2024. DAInfer: Inferring API Aliasing Specifications from Library Documentation via Neurosymbolic Optimization. *Proceedings of the ACM on Software Engineering (FSE)* 1 (2024).
- <span id="page-13-17"></span>[32] Shujun Wang, Yongqiang Tian, and Dengcheng He. 2023. gDoc: Automatic generation of structured API documentation. In *Companion Proceedings of the ACM Web Conference 2023*. ACM, 53–56.
- <span id="page-13-10"></span>[33] Zhe Wang, Huanwu Hu, Linghe Kong, et al. 2024. Diagnosing Application-network Anomalies for Millions of IPs in Production Clouds. In *Proceedings of the 2024 USENIX Annual Technical Conference*. USENIX Association.
- <span id="page-13-0"></span>[34] Georg Wolflein et al. 2025. LLM Agents Making Agent ¨ Tools. In *Proceedings of ACL*.
- <span id="page-13-5"></span>[35] Raghavendra Yandrapally, Shreya Sinha, Roni Tzoref-Brill, and Ali Mesbah. 2023. Carving UI Tests to Generate API Tests and API Specification. In *Proceedings of the International Conference on Software Engineering (ICSE)*. IEEE.
- <span id="page-13-18"></span>[36] Jiamou Yang, Erik Wittern, Andrew T. T. Ying, Julian Dolby, and Lin Tan. 2018. Towards Extracting Web API Specifications from Documentation. In *Proceedings of the 15th International Conference on Mining Software Repositories*. ACM, 454–464.
- <span id="page-13-3"></span>[37] Hao Zhong and Zhendong Su. 2013. Detecting API documentation errors. In *Proceedings of the 2013 ACM SIGPLAN international conference on Object oriented programming systems languages & applications*. 803– 816.