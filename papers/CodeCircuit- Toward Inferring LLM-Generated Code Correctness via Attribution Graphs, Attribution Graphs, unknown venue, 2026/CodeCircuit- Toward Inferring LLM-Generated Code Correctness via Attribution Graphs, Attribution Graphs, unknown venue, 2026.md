                                                CodeCircuit: Toward Inferring LLM-Generated Code Correctness via
                                                                        Attribution Graphs


                                                         Yicheng He * 1 Zheng Zhao * 2 Kaiyu Zhou 3 Bryan Dai 4 Jie Fu 4 Yonghui Yang 5


                                                                  Abstract                                      2023). As these models integrate into mission-critical work-
                                                                                                                flows, the demand for functionally correct and maintainable
                                             Current paradigms for code verification rely heav-
                                                                                                                code has intensified (Liu et al., 2023; 2024b). However,
                                             ily on external mechanisms—such as execution-
arXiv:2602.07080v1 [cs.SE] 6 Feb 2026




                                                                                                                the stochastic nature of LLMs makes reliable assessment
                                             based unit tests or auxiliary LLM judges—which
                                                                                                                a persistent bottleneck. While execution-based verifica-
                                             are often labor-intensive or limited by the judging
                                                                                                                tion via unit tests remains the standard (Khan et al., 2024;
                                             model’s own capabilities. This raises a funda-
                                                                                                                Dong et al., 2025; Wang et al., 2023b; Chen et al., 2021;
                                             mental, yet unexplored question: Can an LLM’s
                                                                                                                Austin et al., 2021; Hendrycks et al., 2021), it is limited
                                             functional correctness be assessed purely from
                                                                                                                by labor-intensive test design and sparse edge-case cover-
                                             its internal computational structure? Our primary
                                                                                                                age. Emergent LLM-as-a-Judge frameworks offer scalable
                                             objective is to investigate whether the model’s
                                                                                                                automation (He et al., 2025a; Jiang et al., 2025), yet they
                                             neural dynamics encode internally decodable sig-
                                                                                                                introduce inference overhead and suffer from recursive de-
                                             nals that are predictive of logical validity dur-
                                                                                                                pendencies where reliability is bounded by the evaluator’s
                                             ing code generation. Inspired by mechanistic
                                                                                                                own reasoning priors.
                                             interpretability, we propose to treat code verifi-
                                             cation as a mechanistic diagnostic task, mapping                   Given these limitations of external mechanisms, a natural
                                             the model’s explicit algorithmic trajectory into                   question arises: Can code correctness be assessed intrin-
                                             line-level attribution graphs. By decomposing                      sically, by examining the LLM’s internal computational
                                             complex residual flows, we aim to identify the                     structure? Prior work has probed neuron activations and
                                             structural signatures that distinguish sound rea-                  representation dynamics during generation (Bui et al., 2025;
                                             soning from logical failure within the model’s                     Huang et al., 2025; Patel et al., 2025), yet these analyses
                                             internal circuits. Analysis across Python, C++,                    have not been directly linked to the correctness of the gen-
                                             and Java confirms that intrinsic correctness sig-                  erated code. In parallel, recent advances in mechanistic
                                             nals are robust across diverse syntaxes. Topolog-                  interpretability (Michaud et al., 2024; Sharkey et al., 2025;
                                             ical features from these internal graphs predict                   Rai et al., 2024a; Gao et al., 2025; Templeton et al., 2024),
                                             correctness more reliably than surface heuristics                  specifically the use of attribution graphs to trace reasoning
                                             and enable targeted causal interventions to fix er-                pathways (Dunefsky et al., 2024; Ameisen et al., 2025; Zhao
                                             roneous logic. These findings establish internal                   et al., 2025), have shown promise in reasoning domains. We
                                             introspection as a decodable property for verify-                  believe that bridging this gap requires a deeper look at how
                                             ing generated code. Our code is at https://                        code-specific structures are manifested within the model’s
                                             github.com/bruno686/CodeCircuit.                                   latent space during the generation process.
                                                                                                                Unlike natural language or abstract math, code possesses a
                                                                                                                rigid, objective topology, such as control flow and variable
                                        1. Introduction
                                                                                                                binding. Recent research (Zhang et al., 2025) demonstrates
                                        Large language models (LLMs; Liu et al., 2024a; He et al.,              that LLMs could form internal finite automata rather than
                                        2025b; Rozière et al., 2023; Guo et al., 2024) have trans-              relying on superficial statistical shortcuts. Thus, we hypoth-
                                        formed code generation from simple solvers to complex                   esize that reliable code generation requires the model to
                                        agents (Wang et al., 2024a; Shinn et al., 2023; Madaan et al.,          instantiate specific neural circuits that mirror this topology,
                                           *
                                                                                                                and that errors manifest as detectable structural collapses
                                             Equal contribution 1 University of Illinois Urbana-Champaign       within these circuits. By decoding the intrinsic circuits that
                                        2
                                          University of Edinburgh 3 Nanyang Technological University
                                        4
                                          IQuest Research 5 National University of Singapore. Correspon-        drive code generation, we gain a window into the model’s
                                        dence to: Yicheng He <yh84@uiuc.edu>.                                   internally consistent computational trajectories—bypassing
                                                                                                                both the opacity of black-box methods and the incomplete-
                                        Preprint. February 10, 2026.

                                                                                                            1
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

ness of external verification frameworks, ultimately provid-         putation for a specific input prompt, enabling the tracing of
ing a more robust foundation for assessing model reliability.        information flow through interpretable features. The con-
                                                                     struction of an AG is predicated on the local replacement
To operationalize this, we introduce CodeCircuit, a white-
                                                                     model, which substitutes the standard Multi-Layer Percep-
box verification framework that analyzes the line-level at-
                                                                     trons (MLPs) with a set of Per-Layer Transcoders (PLTs).
tribution graph of the generated code. We adopt the in-
                                                                     A PLT creates a sparse feature vector f (l) at layer l from the
strumentation of sparse autoencoders (transcoders) to de-                                                   (l)
compose complex residual flows into a causal graph of                residual stream x(l) via an encoder Wenc and a non-linearity
interpretable features. Using CodeCircuit, we conduct an             σ (e.g., TopK or ReLU):
extensive analysis across diverse programming languages                              f (l) = σ(Wenc
                                                                                                (l) (l)
                                                                                                    x + b(l)
                                                                                                         enc ).                 (1)
(Python, C++, Java). Although line-level attribution graphs
are computationally demanding, this detail is crucial for            Crucially, these features are trained to reconstruct the lo-
exposing failure mechanisms. CodeCircuit thus serves as              cal MLP output (or residual update) via decoder weights
a scientific instrument for precise auditing and debugging,             (l)
                                                                     Wdec . Unlike standard Autoencoders, PLTs disentangle the
providing mechanistic insights into code generation beyond           superposition of features in the dense activation space:
what coarser methods can reveal. Our results reveal that,
within a fixed model, internal attribution structures corre-                                      (l)         (l)
                                                                                       m̂(l) = Wdec f (l) + bdec .              (2)
late with code correctness across multiple programming
languages. We find that correct and incorrect code exhibit           The local replacement model is constructed by replacing
systematic topological differences in their attribution graphs       the true MLP output m(l) with an error-corrected PLT out-
                                                                            (l)
(Figure 1). Consequently, CodeCircuit consistently out-              put m̂adj = m̂(l) + (m(l) − m̂(l) ), where the error term
performs both black-box methods (e.g., Temperature Scal-             (m(l) − m̂(l) ) is computed on the forward pass and effec-
ing; Shih et al., 2023) and gray-box methods (e.g., Chain-of-        tively acts as a bias node. This yields a locally linearized
Embedding; Wang et al., 2024b) in verification performance.          computation in which downstream quantities are linear func-
Notably, we demonstrate that these signals are not merely            tions of feature activations and residual stream components,
correlational: by performing targeted interventions on the           with attention outputs and normalization statistics treated as
graph’s nodes (Meng et al., 2022; 2023), we can causally             fixed. Linearity therefore holds with respect to the substi-
correct erroneous code, proving that the attribution graph           tuted MLP pathways under the frozen forward pass.
captures the functional mechanism of generation. Our con-
tributions are summarized as follows:                                The AG is a directed acyclic graph G = (V, E) where
                                                                     nodes V include active PLT features, token embeddings,
• Assessing Generated Code via Internal Computational                error terms, and output logits. An edge wij ∈ E from a
  Structure. We investigate the feasibility of evaluating            source node i (at layer l) to a target node j (at layer l′ > l)
  LLM-generated code by examining the model’s internal               represents the linear contribution of node i’s activation to
  neural dynamics rather than its surface-level output. By           the pre-activation of node j under the locally linearized
  extracting line-level attribution graphs, we demonstrate           computation. Let ai denote the activation of node i, and
  that code correctness appears to be reflected in structured        let vout,i and vin,j denote the residual stream directions
  patterns of internal computation, enabling reliability as-         associated with the output of node i and the input of node j,
  sessment without external supervision or execution.                respectively. The contribution is defined as:
                                                                                                 ⊤
• Shared Signals and Causal Debugging. We provide                                      wij = ai vin,j Jij vout,i ,              (3)
  empirical evidence that these structural correctness sig-
                                                                     where Jij is the Jacobian of the frozen residual stream trans-
  nals are robust across multiple programming languages,
                                                                     formation mapping the output of node i to the input of node
  suggesting that LLMs learn shared computational circuits
                                                                     j, with stop-gradients applied to all nonlinearities. This
  independent of surface syntax. Furthermore, we establish
                                                                     formulation attributes influence through the residual stream
  the causal nature of these features: by intervening on spe-
                                                                     rather than via direct feature-to-feature dependencies.
  cific nodes within the attribution graph, we demonstrate
  the ability to patch the model’s internal logic, moving            To enhance interpretability, the graph undergoes a pruning
  from passive verification to active mechanistic debugging.         process. Rather than matrix inversion (which is intractable
                                                                     for large feature spaces), nodes are pruned based on their
2. Preliminary                                                       attribution to the final model output. We compute the attri-
                                                                     bution of every feature node to the correct logit (or a target
Mechanistic Interpretability via Attribution Graph. At-              metric) via a single backward pass. Nodes are retained only
tribution Graphs (AGs; Ameisen et al., 2025) provide a               if they contribute a significant portion of the total influence
causal, linear decomposition of a transformer model’s com-           relative to a threshold τ . Edges with negligible weights

                                                                 2
                    CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs




Figure 1. Topological fingerprints of code generation errors. Distributions of five graph features extracted from attribution graphs show
differences between correct (blue) and incorrect (orange) code construction steps. These results demonstrate that the attribution topology
provides a structural signal for monitoring the integrity of the code generation process.


are similarly pruned, resulting in a sparse, mechanistically             where L is a standard cross-entropy loss function. This for-
faithful circuit responsible for the model’s behavior.                   mulation enables the detection of logical fallacies at a granu-
                                                                         lar, step-by-step level, grounded in the structural pathologies
Problem Formulation. We consider the task of verifying
                                                                         of the model’s internal reasoning pathways.
the correctness of a code snippet C generated by a large
language model in response to a natural language specifi-
cation S. Formally, the code snippet is decomposed into a                3. CodeCircuit: Mechanistic Code Verification
sequence of N discrete logical steps (e.g., lines of code),
                                                                         The fundamental premise of our framework CodeCircuit
denoted as C = {s1 , s2 , . . . , sN }. Our objective is to pre-
                                                                         (Figure 2) is that the correctness of a generated code se-
dict the correctness label yi ∈ {0, 1} for each step si , where
                                                                         quence is intrinsically encoded within the latent algorith-
yi = 1 indicates that the i-th step is logically sound and
                                                                         mic trajectory of the language model. Traditional verifi-
consistent with the specification S, and yi = 0 otherwise.
                                                                         cation paradigms treat the model as an opaque function,
Unlike traditional verification methods that rely on the ex-             focusing on extrinsic execution outcomes that often fail to
ecution output of the entire snippet C, we formulate code                capture the underlying causal mechanisms of logical falla-
verification as a mechanistic sequence labeling problem. For             cies. In contrast, building upon the mechanistic verification
each step si , the LLM’s internal computation is represented             paradigm established by Zhao et al. (2025), we propose
by a high-dimensional activation trace. We map this trace                a white-box framework that audits the structural integrity
onto an interpretable basis to construct a step-level attribu-           of the model’s internal reasoning pathways. By projecting
tion graph Gi = (Vi , Ei ), which serves as a formal proxy               high-dimensional neural activations onto an interpretable
for the model’s latent algorithmic execution. The prob-                  basis, we extend their approach to identify the specific struc-
lem is thus transformed into learning a diagnostic mapping               tural fingerprints of algorithmic success or failure in code,
F : Gi → yi .                                                            shifting the diagnostic focus from output observation to
                                                                         internal process auditing.
This mapping F is decomposed into two successive oper-
ations. First, a structural encoding function Φ distills the
complex, variable-sized topology of the attribution graph                3.1. Latent Algorithmic Tracing via Attribution Graphs
into a fixed-size feature vector xi ∈ Rd :                               To expose the hidden computational logic of code gen-
                           xi = Φ(Gi ),                        (4)       eration, we construct a step-level attribution graph Gi =
                                                                         (Vi , Ei ) for each discrete logical step i. This graph serves as
where xi captures the structural fingerprints of the computa-            a formal causal map of the model’s mechanistic reasoning
tional trajectory, including node composition, information               pathway. As established in the preliminaries, we utilize a
flow density, and topological bottlenecks. Second, a discrim-            local replacement model where standard MLP layers are
inative classifier hϕ , parameterized by ϕ, maps the structural          substituted by PLTs. This transformation projects the resid-
encoding to a correctness probability:                                   ual stream into a sparse, interpretable feature space f (l) ,
              ŷi = hϕ (xi ) = P (yi = 1 | Gi ; ϕ).            (5)       where individual dimensions correspond to discrete algorith-
                                                                         mic primitives. The resulting graph Gi captures the linear
The learning objective is to find the optimal parameters ϕ∗              flow of information from input embeddings Vemb through
that minimize the empirical risk over a dataset of M labeled             these latent features Vf eat to the final logit output. To ac-
code steps:                                                              count for the portion of the computation not captured by
                               M                                         the interpretable features, we explicitly include error nodes
                           1 X
          ϕ∗ = arg min           L(hϕ (Φ(Gj )), yj ),          (6)       Verr , defined as the residual difference between the true
                       ϕ   M j=1

                                                                     3
                     CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

            Generate Code                                    Attribution Graph                                Verification
  Given a sorted array of distinct integers
  and a target value, return the index if the                                         NL
  target is found. If not, return the index     Layer N
                                                                                                       Global States
  where it would be if it were inserted in




                                                  …
  order.
                                                                                                                   Topological States
  def search_insert(nums, target):
      low = 0                                   Layer 2
      high = len(nums) - 1
      while low <= high:                                                                                  Node States
          mid = (low + high) // 2
          if nums[mid] == target:               Layer 1
              return mid
          elif nums[mid] < target:
              low = mid + 1
          else:
              high = mid
      return low                                          high         =             mid

Figure 2. Overview of the CodeCircuit framework. CodeCircuit maps an LLM’s internal dynamics into a line-level Attribution Graph to
detect errors. By extracting structural features, including global, topological, and node states, the framework identifies latent structural
fingerprints of validity. NL represents the next line.


MLP output and its local PLT reconstruction:                               Furthermore, we analyze the global structure of the rea-
                                      (l)       (l)                        soning pathway. We compute the graph density ρi =
               e(l) = m(l) − (Wdec f (l) + bdec ).               (7)       |Ei |/(|Vi |(|Vi | − 1)) and the number of connected compo-
Including Verr allows for a quantitative assessment of the                 nents to evaluate whether the latent algorithm is executing a
mechanical faithfulness of the reasoning pathway, where the                unified or fragmented process. To capture the hierarchical
total influence of error nodes serves as a proxy for the epis-             and modular nature of the computation, we calculate the av-
temic uncertainty inherent in the model’s latent algorithm.                erage clustering coefficient Ci , which measures the degree
                                                                           to which nodes in the graph tend to cluster together:
3.2. Structural Feature Extraction and Pathological                                                          
                                                                                                               (u,w)∈Ei
                                                                                                                        
     Analysis                                                                                              2 u,w∈N (v)
                                                                                                   1 X         (u,w)∈Ei
                                                                                          Ci =                            ,          (9)
Inspired by Zhao et al. (2025), we hypothesize that logi-                                        |Vi |       kv (kv − 1)
                                                                                                   v∈Vi
cal errors in code generation manifest as structural anoma-
lies within the attribution graph’s topology. To capture
                                                                           where N (v) is the neighborhood of node v and kv is its
these, we define a comprehensive feature extraction map-
                                                                           degree. In the context of code generation, high modularity
ping Φ : Gi → xi that distills the complex topology of
                                                                           often corresponds to the execution of independent sub-tasks,
Gi into a fixed-size diagnostic vector xi . A complete enu-
                                                                           while the presence of disjoint components may indicate
meration of the statistics-, activation-, and topology-based
                                                                           fragmented reasoning where the model fails to integrate
features included in xi is provided in Appendix A.3. This
                                                                           necessary context into the program state.
mapping systematically analyzes the circuit across multiple
hierarchical dimensions of the computational trajectory.                   To identify critical information bottlenecks and logical hubs
                                                                           within the trajectory, we analyze the distribution of between-
The first dimension concerns the mechanical composition
                                                                           ness centrality CB (v) and degree centrality. For a node
and faithfulness of the circuit. Beyond simple cardinality
                                                                           v ∈ Vi , the betweenness centrality represents the fraction
measures of the node set Vi and edge set Ei , we define the
                                                                           of all shortest paths between node pairs that pass through v,
error-to-feature influence ratio ηi to quantify the model’s
                                                                           formulated as:
reliance on unexplained components. Let wuv denote the
attribution weight of the edge from node u to node v; the                                                 X σst (v)
                                                                                            CB (v) =                    ,            (10)
cumulative error influence is formulated as:                                                                       σst
                     P          P                                                                     s̸=v̸=t∈Vi
                       u∈Verr          |wuv |
              ηi = P            Pv∈Vi         .         (8)                where σst is the total number of shortest paths from s to t
                       u∈Vf eat   v∈Vi |wuv |
                                                                           and σst (v) is the number of those paths passing through v.
A high value of ηi indicates a computation driven by opaque                We aggregate these values into statistical moments, includ-
heuristics rather than interpretable algorithmic steps, sug-               ing the mean µ(CB ), standard deviation σ(CB ), and maxi-
gesting a higher probability of logical fragility.                         mum value max(CB ), to characterize the concentration of

                                                                       4
                   CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

information flow. A robust algorithmic execution typically               signals generalize across different programming syntax?
exhibits stable, high-centrality features that coordinate state-       • RQ3 (Scalability):Does predictive power of internal sig-
tracking, whereas an error-prone step may manifest as a                  nals remain robust as algorithmic complexity increases?
fragmented bottleneck with no clear coordination hub.
                                                                       • RQ4 (Visualization): Are there visually distinct topo-
Finally, we characterize attribution dynamics using a total              logical patterns in the internal circuits of correct versus
logit attribution score. Instead of relying on shallow con-              incorrect code?
nectivity, we aggregate the gradient-based attribution along
                                                                       • RQ5 (Causal Intervention): Can targeted interventions
all paths from a feature node to the final output logits. We
                                                                         on internal failure modes rectify errors in code generation?
extract the statistical profile of these total influence scores
S, where Sv represents the integrated gradient of the target
probability with respect to feature v. This allows us to dis-          4.1. Evaluation Setup
tinguish between features that merely activate and those that          Datasets and Problem Domains. To ensure cross-lingual
functionally drive the deep algorithmic processing essential           robustness, we evaluate CodeCircuit across Python, Java,
for correct code generation.                                           and C++. We utilize the MBPP dataset (Austin et al.,
                                                                       2021) as the benchmark for Python and curate semanti-
3.3. Diagnostic Classification and Structural Bug                      cally equivalent task sets for Java and C++ by translating
     Diagnosis                                                         MBPP specifications and generating solutions via Gemma-
                                                                       2-2B-it (Team et al., 2024). We use transcoder trained
The final stage of our framework involves the training of
                                                                       by (Lieberum et al., 2024). This alignment ensures that
a diagnostic classifier hϕ that maps the structural vector
                                                                       the model operates on identical algorithmic logic across
xi to a correctness probability ŷi = hϕ (xi ). We utilize a
                                                                       disparate syntaxes. Ground truth labels are derived from
Gradient Boosting Decision Tree (GBDT; Ke et al., 2017)
                                                                       GPT-4o (OpenAI et al., 2024), where a step is defined as a
architecture, which is particularly effective for handling the
                                                                       correct code line. We emphasize that external supervision
heterogeneous, tabular nature of the extracted topological
                                                                       is used only to obtain evaluation labels and is not required
features. The objective is to minimize the cross-entropy
                                                                       by CodeCircuit during inference. Any functional or logical
loss over a labeled dataset of correct and incorrect code
                                                                       deviation within a line is treated as a positive instance of
generations:
                                                                       failure. Detailed dataset statistics and label distributions
              X
  L(ϕ) = −       [yi log(ŷi ) + (1 − yi ) log(1 − ŷi )] . (11)       are provided in Appendix A.1. The exact prompt templates
               i                                                       used for code generation and line-wise labeling, as well as
                                                                       the attribution-graph extraction configuration, are shown in
Beyond simple binary classification, the GBDT model pro-               Appendix B and A.2.
vides feature importance rankings that enable structural bug
diagnosis. By identifying which topological properties are             Baselines. We compare CodeCircuit against a suite of es-
most predictive of failure, we can pinpoint the mechanical             tablished black-box and gray-box metrics. These include
cause of a logical error. For instance, a high importance              Temperature Scaling (Shih et al., 2023), Maximum Soft-
score for the error-to-feature ratio ηi combined with low              max Probability (MaxProb), Perplexity (PPL), Energy (Liu
betweenness centrality for state-tracking features suggests            et al., 2020), and Entropy derived from final token log-
that the model’s failure stems from a lack of interpretable            its as measures of surface-level confidence. We also in-
state maintenance. This transforms code verification from a            clude Chain-of-Embedding (CoE), such as real-space CoE-
post-hoc execution test into a proactive, mechanistic audit            R, complex-space CoE-C variants (Wang et al., 2024b) and
of the model’s latent computational integrity.                         CoT-Kinetics (Bi et al., 2025), as a competitive gray-box
                                                                       baseline to evaluate the consistency of the reasoning process
                                                                       throughout the generation trajectory.
4. Experiments
                                                                       Evaluation Metrics. Following Zhao et al. (2025), we
In this section, we empirically validate our central hypothe-          evaluate verifier performance using AUROC, FPR@95, and
sis: that code correctness is intrinsic to the model’s latent          AUPR. Since the task focuses on identifying coding errors,
computational topology and can be diagnosed without ex-                incorrect steps are treated as the positive class throughout.
ternal execution. We structure our evaluation around five              Taken together, these metrics characterize ranking quality,
primary research questions:                                            error detection strength, and false alarm behavior.
• RQ1 (Effectiveness): Can CodeCircuit accurately distin-
  guish between correct and incorrect code across diverse              4.2. Main Performance
  programming languages?                                               Effectiveness. We first evaluate the fundamental efficacy
• RQ2 (Generalization): Do the identified discriminative               of CodeCircuit in identifying code errors. This analysis ad-

                                                                   5
                        CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

                    Table 1. Performance comparison of methods across different programming languages and baselines.

                                                Python                             Java                             C++
  Paradigm       Method
                                     AUROC ↑    AUPR ↑     FPR@95 ↓   AUROC ↑    AUPR ↑    FPR@95 ↓    AUROC ↑    AUPR ↑    FPR@95 ↓
                 MaxProb              51.25     29.08       97.20      56.29      46.00      91.20       54.06     27.95      93.39
                 PPL                  51.24     29.08       97.20      56.29      46.00      91.20       54.06     27.94      93.39
  Black-Box      Entropy              51.42     29.04       96.88      56.56      46.34      89.96       53.16     27.98      93.39
                 Temp. Scaling        50.86     28.85       97.20      55.65      45.44      92.08       55.79     28.44      91.49
                 Energy               49.45     25.63       89.10      57.52      45.38      88.38       42.78     23.42      97.71
                 CoE-R                50.75     25.22       93.52      49.68      40.07      94.46       59.07     40.17      92.49
                 CoE-C                51.10     42.91       93.52      52.46      44.76      94.64       56.40     37.72      92.61
  Gray-Box
                 CoT-Kinetics         51.41     29.04       96.88      56.57      46.34      89.96       53.16     27.98      93.39
  White-Box      Ours                 79.89     54.77       77.84      68.06      56.83      79.66       72.21     64.55      80.51


Table 2. Performance comparison of different methods across               (RQ2). As shown in Table 2, our method exhibits robust
Python, C++, and Java test sets. Results are evaluated using AU-
ROC, AUPR, and FPR@95 metrics.
                                                                          zero-shot generalization capabilities, consistently outper-
                                                                          forming the surface-level baseline (MaxProb) even when
 Test Set     Method (Train Set)                 Metrics                  the probe is trained on a different programming language.
                                      AUROC ↑    AUPR ↑    FPR@95 ↓       For instance, when testing on the Java set, the probe trained
              Baseline (MaxProb)        51.25     29.08      97.20        on Python achieves an AUROC of 62.15, marking a 5.86%
 Python
              CodeCircuit (Java)        55.42     34.15      94.10        absolute improvement over the Java-specific MaxProb base-
              CodeCircuit (C++)         53.18     31.50      95.82        line (56.29). We observe a nuanced transferability across the
              CodeCircuit (Python)      79.89     54.77      77.84        three languages; notably, the Java-trained probe generalizes
              Baseline (MaxProb)        56.29     46.00      91.20        effectively to both C++ (59.33 AUROC) and Python (55.42
              CodeCircuit (Python)      62.15     48.33      88.45
 Java
              CodeCircuit (C++)         58.74     47.12      90.15
                                                                          AUROC), suggesting that the structural patterns captured
                                                                          from Java may encapsulate more fundamental logic com-
              CodeCircuit (Java)       68.06      56.83      79.66
                                                                          mon to imperative languages. While a performance gap nat-
              Baseline (MaxProb)        54.06     27.95      93.39
              CodeCircuit (Java)        59.33     36.80      88.24        urally exists between cross-domain transfer and in-domain
 C++                                                                      training, the consistent superiority of our method over the
              CodeCircuit (Python)      57.10     32.55      91.12
              CodeCircuit (C++)         72.21     64.55      80.51        baseline confirms that code errors manifest through a set of
                                                                          universal structural pathologies. These results suggest that
                                                                          our white-box approach captures fundamental reasoning
dresses whether internal circuit pathologies provide a more               inconsistencies that transcend language-specific syntax.
reliable signal for correctness than surface-level heuristics
                                                                          Scalability. To test the robustness of these signals, we an-
(RQ1). As shown in Table 1, CodeCircuit outperforms all
                                                                          alyze how predictive power scales as code complexity and
baseline paradigms across Python, Java, and C++, demon-
                                                                          physical length (number of lines N ∈ {10, 20, 30}) increase
strating the superior reliability of internal circuit patholo-
                                                                          (RQ3). As shown in the Figure 3, the performance advan-
gies over surface-level heuristics. Specifically, our approach
                                                                          tage of CodeCircuit becomes significantly more pronounced
achieves an AUROC of 79.89 in Python, representing a sub-
                                                                          as task difficulty grows, with AUROC rising from approxi-
stantial improvement over the best-performing black-box
                                                                          mately 80 to nearly 92. While surface-level baselines like
and gray-box methods, which hover around 51.42. This
                                                                          MaxProb remain stagnant, our method capitalizes on the
trend is consistent across other metrics and languages; for
                                                                          richer internal activations provided by longer sequences to
instance, we achieve an AUPR of 54.77 in Python and 56.83
                                                                          more accurately identify circuit pathologies. This suggests
in Java, nearly doubling the performance of traditional meth-
                                                                          that unlike gray-box methods that struggle with consistency,
ods like MaxProb or CoT-Kinetics in many cases. Further-
                                                                          our white-box approach becomes increasingly reliable in
more, our method markedly reduces the FPR@95, main-
                                                                          more demanding and complex computational contexts.
taining values as low as 80.51 in C++, whereas baselines
frequently exceed 90. These results highlight that by lever-
                                                                          4.3. Visual Analysis (RQ4)
aging internal model states, we can distinguish correct from
erroneous code with far greater precision than methods rely-              To move beyond binary prediction, we conduct a qualitative
ing on output probabilities or chain-of-thought consistency.              and fine-grained analysis of the attribution graphs to un-
Generalization. We investigate the cross-programming                      cover the “structural fingerprints” of specific failure modes.
language invariance of these structural signatures by con-                Following Zhao et al. (2025), we visualize the separation
ducting transfer experiments across Python, Java, and C++                 between correct and erroneous computational trajectories

                                                                      6
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs




      Figure 3. Predictor performance on Python tasks by difficulty, showing CodeCircuit’s advantage as complexity increases.




 Figure 4. Feature distributions after PCA for correct (blue) and incorrect (red) code generation in different programming languages.


using manifold projection techniques and case studies of              vestigating the attribution graph revealed that the error was
individual circuits in Figure 4. The plots reveal that correct        driven by a specific transcoder feature in the middle layers,
steps often form a dense subset within the broader distribu-          which semantically corresponded to a “greedy matching”
tion of incorrect steps. This spatial overlap suggests many           heuristic that overrode the precise arithmetic state mainte-
failures are structural near misses, maintaining similar graph        nance required for the loop invariant.
topologies to valid code. Nevertheless, a distinct zone of
                                                                      To test causality, we performed a targeted intervention using
computational integrity exists where only correct samples
                                                                      activation clamping. We re-ran the generation and verified
reside. This observation is consistent with the findings
                                                                      that by placing a forward hook to suppress (zero out) this
of Zhao et al. (2025) for reasoning tasks. This consistency
                                                                      maladaptive feature, the model’s trajectory was immediately
across languages confirms that our graph features capture
                                                                      corrected. As shown in Table 3, the intervention successfully
universal signatures of correctness that transcend specific
                                                                      steered the model to generate high = mid - 1 and pro-
programming language.
                                                                      ceed to a functionally correct solution. We also observed
                                                                      successful corrections via feature amplification, specifically
4.4. Causal Intervention (RQ5)                                        by boosting under-active features associated with variable
Finally, we move beyond passive verification to test the              binding context.
causal nature of the identified structural features. Consistent       These results corroborate the causal link between latent
with recent findings by Zhao et al. (2025) in the domain              circuit activation and reasoning correctness established by
of reasoning, we hypothesize that the anomalies detected              Zhao et al. (2025), while extending the phenomenon to the
by CodeCircuit are not merely correlational byproducts but            strict syntactic and logical constraints of programming. This
active drivers of the model’s generation. To validate this, we        serves as a proof-of-concept for latent debugging: the ability
perform a “mechanistic patching” experiment—intervening               to fix software bugs not by editing the source code, but by
on specific nodes in the attribution graph to correct algorith-       modulating the neural circuitry that generates it.
mic logic in real-time.
We illustrate this via a case study on a classic boundary             5. Related Work
condition failure. Given a prompt to implement a binary
search algorithm, the model generated the incorrect update            5.1. Mechanistic Interpretability
logic high = mid, a common bug that leads to infinite                 Mechanistic interpretability (Gao et al., 2025; Michaud
loops, instead of the correct high = mid - 1 (Table 3).               et al., 2024; Rai et al., 2024b) aims to reverse-engineer
CodeCircuit flagged this step as structurally anomalous. In-

                                                                  7
                   CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

 Before Intervention (Incorrect)                                        After Intervention (Correct)
 def search_insert(nums, target):                                       def search_insert(nums, target):
    low, high = 0, len(nums) - 1                                           low, high = 0, len(nums) - 1
    while low <= high:                                                     while low <= high:
        mid = (low + high) // 2                                                mid = (low + high) // 2
        if nums[mid] == target:                                                if nums[mid] == target:
           return mid                                                             return mid
        elif nums[mid] < target:                                               elif nums[mid] < target:
           low = mid + 1                                                          low = mid + 1
        else:                                                                  else:
            high = mid                                                             high = mid - 1
    return low                                                             return low
 Trace: The model fails to decrement high, leading to a potential       Trace: Suppressing the “greedy” feature allows the model to
 infinite loop or incorrect insertion index.                            correctly update the boundary.
Table 3. Side-by-side comparison of a code reasoning trace before and after causal intervention. The highlight indicates the point of
divergence where suppressing a single greedy-matching transcoder feature corrects the model’s internal computational path and restores
logical validity.



neural networks into their underlying computational algo-               the functional correctness of generated code, moving be-
rithms. The field was largely formalized by the “circuits"              yond conventional open-loop generation. This involves the
framework (Olah et al., 2020), which posits that features are           integration of execution-based feedback and self-debugging
the fundamental units of representation and are connected               mechanisms (Chen et al., 2024; Jiang et al., 2024), where the
by weights to form circuits. In the context of Transformers,            model iteratively refines its proposed solution based on sig-
Elhage et al. (2021) introduced a mathematical framework                nals derived from compilers, linters, or test case execution.
that identified “induction heads” as the mechanism for in-              More recently, the scope of LLM-based code generation
context learning. This paradigm has enabled the discovery               has expanded from isolated code snippets to full project-
of specific circuits for tasks such as indirect object identifi-        level development. The emergence of agentic frameworks,
cation (Wang et al., 2022) and modular arithmetic (Nanda                capable of autonomously addressing real-world software
et al., 2023). To address the challenge of polysemanticity,             issues, has been a significant development. The capabilities
where single neurons represent multiple unrelated concepts              of these agents are rigorously evaluated using benchmarks
(Olah et al., 2017), recent research has leveraged the Linear           like SWE-bench (Jimenez et al., 2023) and platforms such
Representation Hypothesis (Elhage et al., 2022) and Sparse              as OpenDevin (Wang et al., 2024a).
Autoencoders to decompose activations into monosemantic
features (Bricken et al., 2023; Cunningham et al., 2023).               6. Conclusion
Furthermore, to bridge the gap between manual inspection
and large-scale models, automated discovery methods such                This work asks a single question: whether the correctness
as ACDC (Conmy et al., 2023) and LLM-based explanations                 of LLM-generated code can be inferred from the model’s
(Bills et al., 2023) have been proposed.                                internal computation, without relying on execution, tests,
                                                                        or external judges. This question is motivated by the grow-
5.2. LLM-based Code Generation                                          ing use of LLMs in settings where external evaluation is
                                                                        costly or incomplete, and where reliability must be assessed
LLMs have rapidly advanced from basic code completion                   from the generation process itself rather than from down-
utilities to sophisticated systems for automated software en-           stream outcomes. Through a systematic analysis based on
gineering (Liu et al., 2024a; He et al., 2025b; Li et al., 2023;        line-level attribution graphs, we show that this is indeed
Wang et al., 2023a; Hui et al., 2024). The initial phase of             possible. Correct and incorrect code exhibit consistent and
this evolution was marked by the development of founda-                 distinguishable internal structures across programming lan-
tional models, such as CodeLlama (Rozière et al., 2023) and             guages, indicating that code correctness is encoded in the
DeepSeek-Coder (Guo et al., 2024), which established new                model’s internal representations. These results suggest that
performance baselines. These models were typically trained              internal analysis provides a viable and general approach to
on massive, high-quality code corpora and leveraged long-               assessing code correctness, and open the door to reliability
context windows to capture extensive code dependencies.                 evaluation methods grounded directly in model behavior
A subsequent research direction has focused on enhancing                rather than external supervision.

                                                                    8
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

Impact Statement                                                    Bui, T.-D., Vu, T. T., Nguyen, T.-T., Nguyen, S., and Vo,
                                                                      H. D. Correctness assessment of code generated by large
This work contributes to the advancement of reliable and              language models using internal representations. arXiv
interpretable machine learning, specifically in the domain of         preprint arXiv:2501.12934, 2025.
automated software engineering. As LLMs are increasingly
deployed to generate code for critical infrastructure and ap-       Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O.,
plications, ensuring their correctness is of paramount soci-          Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman,
etal importance. Our proposed framework, CodeCircuit, ad-             G., et al. Evaluating large language models trained on
vances this goal by shifting verification from opaque, black-         code. arXiv preprint arXiv:2107.03374, 2021.
box outcomes to transparent, mechanistic processes. By ex-
posing the internal “circuits” of code generation, this work        Chen, X., Lin, M., Schärli, N., and Zhou, D. Teaching
aids in the early detection of logical failures and software          large language models to self-debug. In International
vulnerabilities that standard execution-based testing might           Conference on Learning Representations (ICLR), 2024.
miss. Furthermore, our focus on interpretability aligns with        Conmy, A., Mavor-Parker, A., Lynch, A., Heimersheim, S.,
the broader goal of developing trustworthy AI systems that            and Garriga-Alonso, A. Towards automated circuit dis-
are understandable by humans. However, we note that while             covery for mechanistic interpretability. Advances in Neu-
mechanistic verification improves reliability, it should cur-         ral Information Processing Systems, 36:16318–16352,
rently serve as an aid to, rather than a replacement for,             2023.
human review and rigorous software testing protocols.
                                                                    Cunningham, H., Ewart, A., Riggs, L., Huben, R., and
References                                                            Sharkey, L. Sparse autoencoders find highly inter-
                                                                      pretable features in language models. arXiv preprint
Ameisen, E., Lindsey, J., Pearce, A., Gurnee, W., Turner,             arXiv:2309.08600, 2023.
 N. L., Chen, B., Citro, C., Abrahams, D., Carter, S., Hos-
 mer, B., Marcus, J., Sklar, M., Templeton, A., Bricken, T.,        Dong, Y., Ding, J., Jiang, X., Li, G., Li, Z., and Jin, Z.
 McDougall, C., Cunningham, H., Henighan, T., Jermyn,                 Codescore: Evaluating code generation by learning code
 A., Jones, A., Persic, A., Qi, Z., Ben Thompson, T., Zim-            execution. ACM Transactions on Software Engineering
 merman, S., Rivoire, K., Conerly, T., Olah, C., and Bat-             and Methodology, 34(3):1–22, 2025.
 son, J. Circuit tracing: Revealing computational graphs
                                                                    Dunefsky, J., Chlenski, P., and Nanda, N. Transcoders find
 in language models. Transformer Circuits Thread, 2025.
                                                                      interpretable LLM feature circuits. In The Thirty-eighth
 URL https://transformer-circuits.pub/
                                                                     Annual Conference on Neural Information Processing
 2025/attribution-graphs/methods.html.
                                                                      Systems, 2024. URL https://openreview.net/
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,               forum?id=J6zHcScAo0.
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q. V.,
                                                                    Elhage, N., Nanda, N., Olsson, C., Henighan, T., Joseph,
  et al. Program synthesis with large language models.
                                                                      N., Mann, B., Askell, A., Bai, Y., Chen, A., Conerly, T.,
  arXiv preprint arXiv:2108.07732, 2021.
                                                                      et al. A mathematical framework for transformer circuits.
Bi, J., Yan, D., Wang, Y., Huang, W., Chen, H., Wan, G., Ye,          Transformer Circuits Thread, 1(1):12, 2021.
  M., Xiao, X., Schuetze, H., Tresp, V., et al. Cot-kinetics:
                                                                    Elhage, N., Hume, T., Olsson, C., Nanda, N., Henighan,
  A theoretical modeling assessing lrm reasoning process.
                                                                      T., Johnston, S., ElShowk, S., Joseph, N., DasSarma, N.,
  arXiv preprint arXiv:2505.13408, 2025.
                                                                      Mann, B., et al. Softmax linear units. transformer circuits
Bills, S., Cammarata, N., Mossing, D., Tillman, H.,                   thread, 2022.
  Gao, L., Goh, G., Sutskever, I., Leike, J., Wu,                   Gao, L., Rajaram, A., Coxon, J., Govande, S. V., Baker,
  J., and Saunders, W.      Language models can                       B., and Mossing, D. Weight-sparse transformers have
  explain neurons in language models.       https:                    interpretable circuits, 2025. URL https://arxiv.
  //openaipublic.blob.core.windows.net/                               org/abs/2511.13653.
  neuron-explainer/paper/index.html,
  2023.                                                             Guo, D., Zhu, Q., Yang, D., Xie, Z., Dong, K., Zhang, W.,
                                                                      et al. Deepseek-coder: When the large language model
Bricken, T., Templeton, A., Batson, J., Chen, B., Jermyn, A.,         meets programming–the rise of code intelligence. arXiv
  Conerly, T., Turner, N., Anil, C., Denison, C., Askell, A.,         preprint arXiv:2401.14196, 2024.
  et al. Towards monosemanticity: Decomposing language
  models with dictionary learning. Transformer Circuits             Hanna, M., Piotrowski, M., Lindsey, J., and Ameisen,
  Thread, 2, 2023.                                                    E.    circuit-tracer.    https://github.com/

                                                                9
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

  safety-research/circuit-tracer,                   2025.             Li, R., Allal, L. B., Zi, Y., Muennighoff, N., Kocetkov, D.,
  The first two authors contributed equally and are listed              Mou, C., Marone, M., Akiki, C., Li, J., Chim, J., et al.
  alphabetically.                                                       Starcoder: May the source be with you! arXiv preprint
                                                                        arXiv:2305.06161, 2023.
He, J., Shi, J., Zhuo, T. Y., Treude, C., Sun, J., Xing, Z.,
  Du, X., and Lo, D. Llm-as-a-judge for software engineer-            Lieberum, T., Rajamanoharan, S., Conmy, A., Smith, L.,
  ing: Literature review, vision, and the road ahead. arXiv             Sonnerat, N., Varma, V., Kramar, J., Dragan, A., Shah,
  preprint arXiv:2510.24367, 2025a.                                     R., and Nanda, N. Gemma scope: Open sparse au-
                                                                        toencoders everywhere all at once on gemma 2. In Be-
He, Y., Huang, C., Li, Z., Huang, J., and Yang, Y. Visplay:             linkov, Y., Kim, N., Jumelet, J., Mohebbi, H., Mueller,
  Self-evolving vision-language models from images. arXiv               A., and Chen, H. (eds.), Proceedings of the 7th Black-
  preprint arXiv:2511.15661, 2025b.                                     boxNLP Workshop: Analyzing and Interpreting Neu-
                                                                        ral Networks for NLP, pp. 278–300, Miami, Florida,
Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M., Arora,            US, November 2024. Association for Computational
  A., Guo, E., Burns, C., Puranik, S., He, H., Song, D.,                Linguistics. doi: 10.18653/v1/2024.blackboxnlp-1.
  et al. Measuring coding challenge competence with APPS.               19. URL https://aclanthology.org/2024.
  In Advances in Neural Information Processing Systems                  blackboxnlp-1.19/.
  (NeurIPS) Datasets and Benchmarks Track, 2021.
                                                                      Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,
Huang, Y., Ma, L., Nishikino, K., and Akazaki, T. Risk                  C., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-
  assessment framework for code llms via leveraging inter-              v3 technical report. arXiv preprint arXiv:2412.19437,
  nal states. In Proceedings of the 33rd ACM International              2024a.
 Conference on the Foundations of Software Engineering,
  pp. 432–443, 2025.                                                  Liu, J., Xia, C. S., Wang, Y., and Zhang, L. Is your code
                                                                        generated by chatgpt really correct? rigorous evaluation
Hui, B., Yang, J., Cui, Z., Yang, J., Liu, D., Zhang, L., Liu,          of large language models for code generation. Advances
 T., Zhang, J., Yu, B., Dang, K., et al. Qwen2.5-coder                  in Neural Information Processing Systems, 36:21558–
  technical report. arXiv preprint arXiv:2409.12186, 2024.              21572, 2023.
Jiang, H., Chen, Y., Cao, Y., Lee, H.-y., and Tan, R. T. Code-        Liu, J., Xie, S., Wang, J., Wei, Y., Ding, Y., and Zhang, L.
   judgebench: Benchmarking llm-as-a-judge for coding                   Evaluating language models for efficient code generation.
   tasks. arXiv preprint arXiv:2507.10535, 2025.                        arXiv preprint arXiv:2408.06450, 2024b.
Jiang, X., Dong, J., Wang, Y., Zheng, Y., Shang, L., Li, G.,          Liu, W., Wang, X., Owens, J., and Li, Y. Energy-based out-
   Jin, Z., and Jiao, L. Self-planning code generation with             of-distribution detection. Advances in neural information
   large language models. ACM Transactions on Software                  processing systems, 33:21464–21475, 2020.
   Engineering and Methodology, 33(7), 2024. doi: 10.
   1145/3672456.                                                      Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao,
                                                                       L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S.,
Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K.,                Yang, S., et al. Self-refine: Iterative refinement with self-
  Niranjan, O., et al. Swe-bench: Can language mod-                    feedback. In Advances in Neural Information Processing
  els resolve real-world github issues? arXiv preprint                 Systems (NeurIPS), 2023.
  arXiv:2310.06770, 2023.
                                                                      Meng, K., Bau, D., Andonian, A., and Belinkov, Y. Locating
Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma,                  and editing factual associations in GPT. In Advances in
  W., Ye, Q., and Liu, T.-Y. Lightgbm: A highly efficient              Neural Information Processing Systems (NeurIPS), 2022.
  gradient boosting decision tree. Advances in neural infor-
  mation processing systems, 30, 2017.                                Meng, K., Bau, D., Andonian, A., and Belinkov, Y. Mass-
                                                                       editing memory in a transformer. In International Con-
Khan, M. A. M., Bari, M. S., Do, X. L., Wang, W., Parvez,              ference on Learning Representations (ICLR), 2023.
  M. R., and Joty, S. Xcodeeval: An execution-based large
  scale multilingual multitask benchmark for code under-              Michaud, E. J., Liao, I., Lad, V., Liu, Z., Mudide, A.,
  standing, generation, translation and retrieval. In Pro-             Loughridge, C., Guo, Z. C., Kheirkhah, T. R., Vukelić,
  ceedings of the 62nd Annual Meeting of the Association               M., and Tegmark, M. Opening the ai black box: program
  for Computational Linguistics (Volume 1: Long Papers),               synthesis via mechanistic interpretability. arXiv preprint
  pp. 6766–6805, 2024.                                                 arXiv:2402.05110, 2024.

                                                                 10
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

Nanda, N., Chan, L., Lieberum, T., Smith, J., and Stein-               MacDiarmid, M., Freeman, C. D., Sumers, T. R.,
  hardt, J. Progress measures for grokking via mechanistic             Rees, E., Batson, J., Jermyn, A., Carter, S., Olah,
  interpretability. arXiv preprint arXiv:2301.05217, 2023.             C., and Henighan, T. Scaling monosemanticity: Ex-
                                                                       tracting interpretable features from claude 3 sonnet.
Olah, C., Mordvintsev, A., and Schubert, L. Feature visual-            Transformer Circuits Thread, 2024. URL https:
  ization. Distill, 2(11):e7, 2017.                                    //transformer-circuits.pub/2024/
Olah, C., Cammarata, N., Schubert, L., Goh, G., Petrov,                scaling-monosemanticity/index.html.
  M., and Carter, S. Zoom in: An introduction to circuits.           Wang, K., Variengien, A., Conmy, A., Shlegeris, B., and
  Distill, 5(3):e00024–001, 2020.                                     Steinhardt, J. Interpretability in the wild: a circuit for
                                                                      indirect object identification in gpt-2 small. arXiv preprint
OpenAI et al. Gpt-4o system card, 2024. URL https:
                                                                      arXiv:2211.00593, 2022.
 //arxiv.org/abs/2410.21276.
                                                                     Wang, X., Li, B., and Neubig, G. Opendevin: An open
Patel, S., Yadavally, A., Dhulipala, H., and Nguyen, T.
                                                                      platform for ai software developers as generalist agents.
  Planning a large language model for static detection
                                                                      arXiv preprint arXiv:2407.16741, 2024a.
  of runtime errors in code snippets. In Proceedings of
  the IEEE/ACM 47th International Conference on Soft-                Wang, Y., Le, H., Gotmare, A. D., Bui, N. D., Li, J., and
  ware Engineering (ICSE 2025), pp. 872–884, 2025. doi:               Hoi, S. C. Codet5+: Open code large language models
  10.1109/ICSE55347.2025.00102.                                       for code understanding and generation. In Proceedings
                                                                      of the 2023 Conference on Empirical Methods in Natural
Rai, D., Zhou, Y., Feng, S., Saparov, A., and Yao, Z.
                                                                      Language Processing, pp. 1069–1088, 2023a.
  A practical review of mechanistic interpretability for
  transformer-based language models. arXiv preprint                  Wang, Y., Zhang, P., Yang, B., Wong, D. F., and Wang, R.
  arXiv:2407.02646, 2024a.                                            Latent space chain-of-embedding enables output-free llm
                                                                      self-evaluation. arXiv preprint arXiv:2410.13640, 2024b.
Rai, D., Zhou, Y., Feng, S., Saparov, A., and Yao, Z.
  A practical review of mechanistic interpretability for             Wang, Z., Zhou, S., Fried, D., and Neubig, G. Execution-
  transformer-based language models. arXiv preprint                   based evaluation for open-domain code generation. In
  arXiv:2407.02646, 2024b.                                            Findings of the Association for Computational Linguis-
                                                                      tics: EMNLP 2023, pp. 1271–1290, 2023b.
Rozière, B., Gehring, J., Gloeckle, F., Sootla, S., Gat, I.,
  Tan, X. E., et al. Code llama: Open foundation models              Zhang, Y., Du, W., Jin, D., Fu, J., and Jin, Z. Finite state
  for code. arXiv preprint arXiv:2308.12950, 2023.                     automata inside transformers with chain-of-thought: A
                                                                       mechanistic study on state tracking. In Proceedings of
Sharkey, L., Chughtai, B., Batson, J., Lindsey, J., Wu, J.,
                                                                       the 63rd Annual Meeting of the Association for Computa-
  Bushnaq, L., Goldowsky-Dill, N., Heimersheim, S., Or-
                                                                       tional Linguistics (ACL), 2025.
  tega, A., Bloom, J., et al. Open problems in mechanistic
  interpretability. arXiv preprint arXiv:2501.16496, 2025.           Zhao, Z., Koishekenov, Y., Yang, X., Murray, N., and Can-
                                                                       cedda, N. Verifying chain-of-thought reasoning via its
Shih, A., Sadigh, D., and Ermon, S. Long horizon temper-               computational graph. arXiv preprint arXiv:2510.09312,
  ature scaling. In International conference on machine                2025.
  learning, pp. 31422–31434. PMLR, 2023.

Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and
  Yao, S. Reflexion: Language agents with verbal rein-
  forcement learning. In Advances in Neural Information
  Processing Systems (NeurIPS), 2023.

Team, G., Riviere, M., Pathak, S., Sessa, P. G., Hardin,
  C., Bhupatiraju, S., Hussenot, L., Mesnard, T., Shaber,
  B., Haber, A., et al. Gemma 2: Improving open
  language models at a practical size. arXiv preprint
  arXiv:2408.00118, 2024.

Templeton, A., Conerly, T., Marcus, J., Lindsey, J., Bricken,
  T., Chen, B., Pearce, A., Citro, C., Ameisen, E., Jones,
  A., Cunningham, H., Turner, N. L., McDougall, C.,

                                                                11
                    CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

A. Experimental Settings
A.1. Dataset Statistic
We report the final statistics of our curated multilingual MBPP incremental datasets in Table 4. Following our evaluation
setup in Section 4.1, we use MBPP as the Python benchmark and construct semantically equivalent C++ and Java task
sets by translating the same specifications, ensuring that the three datasets share comparable underlying algorithmic logic
while differing only in surface syntax. Each JSONL instance corresponds to one labeled generation record with a binary
correctness label (answer∈ {0, 1}), where 1 denotes correct and 0 denotes wrong. In total, our corpus contains 1,447 Python
instances, 3,423 C++ instances, and 3,126 Java instances. The label distribution exhibits noticeable language-dependent
skew: Python has the highest correctness ratio (81.6% correct vs. 18.4% incorrect), while C++ and Java are more challenging
with substantially higher error rates (C++: 66.8%/33.2%; Java: 61.7%/38.3%). This imbalance motivates us to evaluate
CodeCircuit across languages and to study whether attribution-graph structural signatures remain predictive under varying
error prevalence and programming syntax.

                                       Dataset      Total Steps      % Correct        % Incorrect
                                       C++              3,423             66.8%           33.2%
                                       Python           1,447             81.6%           18.4%
                                       Java             3,126             61.7%           38.3%
Table 4. Final statistics of our curated MBPP incremental datasets, showing the number of instances and the distribution of correct/incorrect
labels.



A.2. Experimental Hyperparameter
For attribution-graph extraction, we use the ReplacementModel instantiated from the base LLM, Google Gemma-2-2B-IT1 ,
together with the corresponding GemmaScope transcoder2 , and run all tracing in bfloat16 precision on a single GPU. We
use the Circuit-Tracer (Hanna et al., 2025) library for attribution graph computation. For each input prompt, we construct an
attribution graph with the following settings: we attribute at most 10 output logits and target a cumulative logit probability
mass of 0.95. To control graph size and memory footprint, we cap the number of retained feature nodes to 8,192 and compute
attributions in mini-batches of size 64. We disable parameter offloading and verbose debugging output. Following the
preprocessing in our pipeline, we skip prompts longer than 550 characters to avoid excessively long contexts during tracing.
Each resulting attribution graph is serialized in PyTorch format (.pt), and we additionally append a per-instance metadata
record in JSONL format, including the task identifier, step index, graph path, and the corresponding binary correctness label.

A.3. Detailed Features
For each line-level attribution graph, we extract a fixed-length feature vector from the pruned subgraph to characterize both
node composition and circuit topology. Concretely, we first prune the full attribution graph using an influence-based masking
rule with a node-threshold of 0.8, which retains only the most influential nodes according to the cumulative influence scores
returned by the pruning routine. Let the pruned node set contain (i) transcoder feature nodes, (ii) error nodes (one error node
per layer-position pair), as well as (optionally) token and logit nodes if they survive pruning. We then compute three groups
of features.
(1) High-level statistics. We record (a) the total number of active features in the original graph (the length of the activation-
value vector), (b) the number of pruned feature nodes, and (c) the number of pruned error nodes. To summarize output
uncertainty, we additionally compute (d) the top-1 logit probability and (e) the entropy of the traced logit probability vector.
These quantities capture the overall circuit scale and the model’s output confidence for the step.
(2) Aggregated node and activation statistics. Using the cumulative influence scores restricted to the pruned nodes, we
compute (a) the mean influence over all pruned nodes as a global saliency summary. For error nodes, we compute (b) the
total error influence (sum over pruned error nodes) and (c) the mean error influence, serving as a proxy for how much of
the computation is routed through unexplained residual components. For pruned feature nodes, we gather their activation
   1
       https://huggingface.co/google/gemma-2-2b-it
   2
       https://huggingface.co/mntss/gemma-scope-transcoders

                                                                     12
                    CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

  Gemma-2-2B-IT Code Generation Prompt Template
  You are a code assistant.
  You must output ONLY valid code.
  Do not include comments, markdown, explanations, or extra text.
  Output only code.

  Task prompt:
  {TASK_PROMPT}
Table 5. Prompt template used for code generation. The final input is the concatenation of the fixed instruction block above and the task
prompt, separated by two newline characters.




  Line-wise Code Correctness Checker Prompt Template
  You are a code correctness checker.
  Review the provided code line by line. For each line, output a score of 1 or 0 according to the following rules:

  1. If the line has a syntax error, output 0.
  2. If the line is syntactically correct but violates the coding requirements described in the task, output 0 for that line and all subsequent
  lines. Once a line violates the requirements, all following lines must also be 0.
  3. If the line is syntactically correct and meets the coding requirements so far, output 1.

  The code has exactly {N_LINES} lines. Output only a list of exactly {N_LINES} integers, e.g., [1, 1, 0, 1]. Do not include any
  explanation or extra text.

  4. Focus solely on whether the substantive code contains issues, ignoring parameter variable names, function names, and so on.

  Task Description:
  —
  {TASK_DESCRIPTION}
  —

  Code to Check:
  —
  {CODE_TO_CHECK}
  —
Table 6. Prompt template used for line-wise correctness scoring. {N_LINES} is computed as the number of lines in {CODE_TO_CHECK};
the model is instructed to output a list of exactly {N_LINES} binary integers.




values and compute (d) mean activation, (e) maximum activation, and (f) activation standard deviation. Finally, to capture
where computation concentrates across depth, we construct a (g) layer-wise histogram of pruned feature counts: for each
transformer layer, we count how many retained feature nodes originate from that layer. This produces a length-L vector,
where L is the number of transformer layers.
(3) Topological and edge-based features of the pruned subgraph. We form a directed weighted graph from the pruned
adjacency matrix, where directed edges represent attributed influence and edge weights are inherited from the adjacency
matrix. From edge weights, we compute (a) the sum, (b) mean, and (c) standard deviation of all edge weights, together
with (d) the number of edges in the pruned subgraph and (e) the graph density. To capture structural fragmentation, we
compute (f) the number of weakly connected components. We then compute centrality-based summaries: (g) mean degree
centrality, (h) maximum degree centrality, (i) mean betweenness centrality (computed with edge weights), and (j) maximum
betweenness centrality. To quantify global connectivity, we compute (k) the average shortest path length within the largest
weakly connected component (set to −1 if undefined). Finally, we add a task-relevant routing signal: (l) the shortest-path
distance from any retained input-token node to any retained logit node (set to −1 if no path exists), which measures how
directly input evidence can flow to the output decision within the pruned circuit. For degenerate cases where the pruned
graph has fewer than two nodes, we return a default feature vector with zeros and sentinel values (e.g., −1 for undefined
shortest-path statistics) to preserve a consistent feature dimensionality across all examples.

                                                                      13
                  CodeCircuit: Toward Inferring LLM-Generated Code Correctness via Attribution Graphs

B. Prompt Template
For code generation, we use a fixed instruction block that strictly constrains the model to output only valid code; this block
is concatenated with the task prompt (two newline characters in between) to form the final input, as shown in Table 5. For
correctness checking, we use a single user prompt that instructs a judge model to perform line-wise validation and return an
integer list of length {N_LINES}, where any violation at a given line forces that line and all subsequent lines to be scored as
0; we then parse the returned list as per-line correctness signals, as shown in Table 6.

C. Limitation
The primary limitation of this approach is the computational overhead required to construct attribution graphs. Unlike
black-box methods, our framework involves gradient-based backpropagation and feature projections, which increase time
and memory complexity relative to standard inference. For extensive code generation tasks, these requirements may
limit real-time deployment. Nevertheless, this bottleneck presents a significant opportunity for algorithmic optimization.
Future research could focus on sparse attribution techniques that target only critical logical junctions or utilize low-rank
approximations to reduce the cost of Jacobian computations. By transitioning from exhaustive circuit tracing to selective
structural diagnostics, the computational burden can be substantially mitigated, paving the way for efficient, white-box
verification in production environments.




                                                              14
