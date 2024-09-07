# A General Framework for Robust Interactive Learning

Ehsan Emamjomeh-Zadeh

Department of Computer Science, University of Southern California, emamjome@usc.edu

David Kempe

Department of Computer Science, University of Southern California, dkmepe@usc.edu

###### Abstract

We propose a general framework for interactively learning models, such as (binary or non-binary) classifiers, orderings/rankings of items, or clusterings of data points. Our framework is based on a generalization of Angluin's equivalence query model and Littlestone's online learning model: in each iteration, the algorithm proposes a model, and the user either accepts it or reveals a specific mistake in the proposal. The feedback is correct only with probability \(p>\frac{1}{2}\) (and adversarially incorrect with probability \(1-p\)), i.e., the algorithm must be able to learn in the presence of arbitrary noise. The algorithm's goal is to learn the ground truth model using few iterations.

Our general framework is based on a graph representation of the models and user feedback. To be able to learn efficiently, it is sufficient that there be a graph \(G\) whose nodes are the models and (weighted) edges capture the user feedback, with the property that if \(s,s^{*}\) are the proposed and target models, respectively, then any (correct) user feedback \(s^{\prime}\) must lie on a shortest \(s\)-\(s^{*}\) path in \(G\). Under this one assumption, there is a natural algorithm reminiscent of the Multiplicative Weights Update algorithm, which will efficiently learn \(s^{*}\) even in the presence of noise in the user's feedback.

From this general result, we rederive with barely any extra effort classic results on learning of classifiers and a recent result on interactive clustering; in addition, we easily obtain new interactive learning algorithms for ordering/ranking.

## 1 Introduction

With the pervasive reliance on machine learning systems across myriad application domains in the real world, these systems frequently need to be deployed before they are fully trained. This is particularly true when the systems are supposed to learn a specific user's (or a small group of users') personal and idiosyncratic preferences. As a result, we are seeing an increased practical interest in online and interactive learning across a variety of domains.

A second feature of the deployment of such systems "in the wild" is that the feedback the system receives is likely to be noisy. Not only may individual users give incorrect feedback, but even if they do not, the preferences -- and hence feedback -- across different users may vary. Thus, interactive learning algorithms deployed in real-world systems must be resilient to noisy feedback.

Since the seminal work of Angluin [2] and Littlestone [15], the paradigmatic application of (noisy) interactive learning has been online learning of a binary classifier when the algorithm is provided with feedback on samples it had previously classified incorrectly. However, beyond (binary or other) classifiers, there are many other models that must be frequently learned in an interactive manner. Two particularly relevant examples are the following:* Learning an ordering/ranking of items is a key part of personalized Web search or other information-retrieval systems (e.g., [12, 19]). The user is typically presented with an ordering of items, and from her clicks or lack thereof, an algorithm can infer items that are in the wrong order.
* Interactively learning a clustering [6, 5, 4] is important in many application domains, such as interactively identifying communities in social networks or partitioning an image into distinct objects. The user will be shown a candidate clustering, and can express that two clusters should be merged, or a cluster should be split into two.

In all three examples -- classification, ranking, and clustering -- the interactive algorithm will propose a _model1_ (a classifier, ranking, or clustering) as a solution. The user then provides -- explicitly or implicitly -- feedback on whether the model is correct or needs to be fixed/improved. This feedback may be incorrect with some probability. Based on the feedback, the algorithm will propose a new and possibly very different model, and the process repeats. This type of interaction is the natural generalization of Angluin's equivalence query model [2, 3]. It is worth noting that in contrast to active learning, in interactive learning (which is the focus of this work), the algorithm cannot "ask" direct questions; it can only propose a model and receive feedback in return. The algorithm should minimize the number of user interactions, i.e., the number of times that the user needs to propose fixes. A secondary goal is to make the algorithm's internal computations efficient as well.

Footnote 1: We avoid the use of the term “concept,” as it typically refers to a binary function, and is thus associated specifically with a classifier.

The main contribution of this article is a general framework for efficient interactive learning of models (even with noisy feedback), presented in detail in Section 2. We consider the set of all \(N\) models as nodes of a positively weighted undirected or directed graph \(G\). The one key property that \(G\) must satisfy is the following: (*) If \(s\) is a proposed model, and the user (correctly) suggests changing it to \(s^{\prime}\), then the graph must contain the edge \((s,s^{\prime})\); furthermore, \((s,s^{\prime})\) must lie on a shortest path from \(s\) to the target model \(s^{*}\) (which is unknown to the algorithm).

We show that this single property is enough to learn the target model \(s^{*}\) using at most \(\log N\) queries2 to the user, in the absence of noise. When the feedback is correct with probability \(p>\frac{1}{2}\), the required number of queries gracefully deteriorates to \(O(\log N)\); the constant depends on \(p\). We emphasize that the assumption (*) is not an assumption on the user. We do not assume that the user somehow "knows" the graph \(G\) and computes shortest paths in order to find a response. Rather, (*) states that \(G\) was correctly chosen to model the underlying domain, so that correct answers by the user must in fact have the property (*). To illustrate the generality of our framework, we apply it to ordering, clustering, and classification:

Footnote 2: Unless specified otherwise, all logarithms are base 2.

1. For ordering/ranking, each permutation is a node in \(G\); one permutation is the unknown target. If the user can point out only _adjacent_ elements that are out of order, then \(G\) is an adjacent transposition "Bubble Sort" graph, which naturally has the property (*). If the user can pick any element and suggest that it should precede an entire block of elements it currently follows, then we can instead use an "Inserison Sort" graph; interestingly, to ensure the property (*), this graph must be weighted. On the other hand, as we show in Section 3, if the user can propose two arbitrary elements that should be swapped, there is _no_ graph \(G\) with the property (*).

Our framework directly leads to an interactive algorithm that will learn the correct ordering of \(n\) items in \(O(\log(n!))=O(n\log n)\) queries; we show that this bound is optimal under the equivalence query model.
2. For learning a clustering of \(n\) items, the user can either propose merging two clusters, or splitting one cluster. In the interactive clustering model of [6, 5, 4], the user can specify _that_ a particular cluster \(C\) should be split, but does not give a specific split. We show in Section 4 that there is a weighted directed graph with the property (*); then, if each cluster is from a "small" concept class of size at most \(M\) (such as having low VC-dimension), there is an algorithm finding the true clustering in \(O(k\log M)\) queries, where \(k\) is number of the clusters (known ahead of time).
3. For binary classification, \(G\) is simply an \(n\)-dimensional hypercube (where \(n\) is the number of sample points that are to be classified). As shown in Section 5, one immediately recovers a close variant of standard online learning algorithms within this framework. An extension to classification with more than two classes is very straightforward.

## 2 Learning Framework

We define a framework for query-efficient interactive learning of different types of _models_. Some prototypical examples of models to be learned are rankings/orderings of items, (unlabeled) clusterings of graphs or data points, and (binary or non-binary) classifiers. We denote the set of all candidate models (permutations, partitions, or functions from the hypercube to \(\{0,1\}\)) by \(\Sigma\), and individual models3 by \(s,s^{\prime},s^{*}\), etc. We write \(N=|\Sigma|\) for the number of candidate models.

Footnote 3: When considering specific applications, we will switch to notation more in line with that used for the specific application.

We study interactive learning of such models in a natural generalization of the equivalence query model of Angluin [2, 3]. This model is equivalent to the more widely known online learning model of Littlestone [15], but more naturally fits the description of user interactions we follow here. It has also served as the foundation for the interactive clustering model of Balcan and Blum [6] and Awasthi et al. [5, 4].

In the _interactive learning framework_, there is an unknown ground truth model \(s^{*}\) to be learned. In each round, the learning algorithm proposes a model \(s\) to the user. In response, with probability \(p>\frac{1}{2}\), the user provides correct feedback. In the remaining case (i.e., with probability \(1-p\)), the feedback is _arbitrary_; in particular, it could be arbitrarily and deliberately misleading.

Correct feedback is of the following form: if \(s=s^{*}\), then the algorithm is told this fact in the form of a user response of \(s\). Otherwise, the user reveals a model \(s^{\prime}\neq s\) that is "more similar" to \(s^{*}\) than \(s\) was. The exact nature of "more similar," as well as the possibly restricted set of suggestions \(s^{\prime}\) that the user can propose, depend on the application domain. Indeed, the strength of our proposed framework is that it provides strong query complexity guarantees under minimal assumptions about the nature of the feedback; to employ the framework, one merely has to verify that the the following assumption holds.

**Definition 2.1** (Graph Model for Feedback): _Define a weighted graph \(G\) (directed or undirected) that contains one node for each model \(s\in\Sigma\), and an edge \((s,s^{\prime})\) with arbitrary positive edge length \(\omega_{(s,s^{\prime})}>0\) if the user is allowed to propose \(s^{\prime}\) in response to \(s\). (Choosing the lengths of edges is an important part of using the framework.) \(G\) may contain additional edges not corresponding to any user feedback. The key property that \(G\) must satisfy is the following: (*) If the algorithm proposes \(s\) and the ground truth is \(s^{*}\neq s\), then every correct user feedback \(s^{\prime}\) lies on a shortest path from \(s\) to \(s^{*}\) in \(G\) with respect to the lengths \(\omega_{e}\). If there are multiple candidate nodes \(s^{\prime}\), then there is no guarantee on which one the algorithm will be given by the user._

### Algorithm and Guarantees

Our algorithms are direct reformulations and slight generalizations of algorithms recently proposed by Emamjomeh-Zadeh et al. [10], which itself was a significant generalization of the natural "Halving Algorithm" for learning a classifier (e.g., [15]). They studied the search problem as an abstract problem they termed "Binary Search in Graphs," without discussing any applications. Our main contribution here is the application of the abstract search problem to a large variety of interactive learning problems, and a framework that makes such applications easy. We begin with the simplest case \(p=1\), i.e., when the algorithm only receives correct feedback.

Algorithm 1 gives essentially best-possible general guarantees [10]. To state the algorithm and its guarantees, we need the notion of an approximate median node of the graph \(G\). First, we denote by

\[N(s,s^{\prime}):=\begin{cases}\{s\}&\text{if }s^{\prime}=s\\ \{\hat{s}\mid\text{$s^{\prime}$ lies on a shortest path from $s$ to $\hat{s}$}\}& \text{if }s^{\prime}\neq s\end{cases}\]

the set of all models \(\hat{s}\) that are consistent with a user feedback of \(s^{\prime}\) to a model \(s\). In anticipation of the noisy case, we allow models to be weighted4, and denote the node weights or _likelihoods_ by \(\mu(s)\geq 0\). If feedback is not noisy (i.e., \(p=1\)), all the non-zero node weights are equal. For every subset of models \(S\), we write \(\mu(S):=\sum_{s\in S}\mu(s)\) for the total node weight of the models in \(S\). Now, for every model \(s\), define

Footnote 4: Edge lengths are part of the definition of the graph, but node weights will be assigned by our algorithm; they basically correspond to likelihoods.

\[\Phi_{\mu}(s):=\frac{1}{\mu(\Sigma)}\cdot\max_{s^{\prime}\neq s,(s,s^{\prime}) \in G}\mu(N(s,s^{\prime}))\]

to be the largest fraction (with respect to node weights) of models that could still be consistent with a worst-case response \(s^{\prime}\) to a proposed model of \(s\). For every subset of models \(S\), we denote by \(\mu_{S}\) the likelihood function that assigns weight \(1\) to every node \(s\in S\) and \(0\) elsewhere. For simplicity of notation, we use \(\Phi_{S}(s)\) when the node weights are \(\mu_{S}\).

The simple key insight of [10] can be summarized and reformulated as the following proposition:

**Proposition 2.1** ([10], Proofs of Theorems 3 and 14): _Let \(G\) be a (weighted) directed graph in which each edge \(e\) with length \(\omega_{e}\) is part of a cycle of total edge length at most \(c\cdot\omega_{e}\). Then, for every node weight function \(\mu\), there exists a model \(s\) such that \(\Phi_{\mu}(s)\leq\frac{c-1}{c}\)._

_When \(G\) is undirected (and hence \(c=2\)), for every node weight function \(\mu\), there exists an \(s\) such that \(\Phi_{\mu}(s)\leq\frac{1}{2}\)._

Proof.For any pair \(s,s^{\prime}\) of models, let \(d(s,s^{\prime})\) denote their distance in \(G\) with respect to the edge lengths \(\omega\). Fix a node weight function \(\mu\). Define \(\Psi_{\mu}(s):=\sum_{s^{\prime}\in\Sigma}d(s,s^{\prime})\mu(s^{\prime})\) as the total weighted distance from \(s\) to every model \(s^{\prime}\). Let \(\hat{s}\) be a model that minimizes \(\Psi_{\mu}(s)\). We prove that \(\hat{s}\) satisfies the claim of Proposition 2.1.

Let \(e=(\hat{s},s)\) be an edge in \(G\). By definition, \(s\) lies on a shortest path from \(\hat{s}\) to every model \(s^{\prime}\in N(\hat{s},s)\). Therefore, for every \(s^{\prime}\in N(\hat{s},s)\), we have \(d(s,s^{\prime})=d(\hat{s},s^{\prime})-\omega_{e}\). On the other hand,\(e\) belongs to a cycle of total length at most \(c\cdot\omega_{e}\), so there is a path of total length no more than \((c-1)\cdot\omega_{e}\) from \(s\) to \(\hat{s}\). Thus, for every \(s^{\prime}\notin N(\hat{s},s)\), we have \(d(s,s^{\prime})\leq d(\hat{s},s^{\prime})+(c-1)\cdot\omega_{e}\). We can now bound \(\Psi_{\mu}(s)\) from above:

\[\Psi_{\mu}(s) =\sum_{s^{\prime}\in\Sigma}\mu(s^{\prime})\cdot d(s,s^{\prime})\] \[\leq\sum_{s^{\prime}\in N(\hat{s},s)}\mu(s^{\prime})\cdot(d(\hat{s },s^{\prime})-\omega_{e})+\sum_{s^{\prime}\notin N(\hat{s},s)}\mu(s^{\prime}) \cdot(d(s,s^{\prime})+(c-1)\cdot\omega_{e})\] \[=\Psi_{\mu}(\hat{s})-\omega_{e}\cdot\left(\sum_{s^{\prime}\in N( \hat{s},s)}\mu(s^{\prime})-(c-1)\cdot\sum_{s^{\prime}\notin N(\hat{s},s)}\mu( s^{\prime})\right).\]

By definition of \(\hat{s}\), we have \(\Psi_{\mu}(s)\geq\Psi_{\mu}(\hat{s})\), so after dividing by \(\omega_{e}>0\), we get that \(\sum_{s^{\prime}\in N(\hat{s},s)}\mu(s^{\prime})-(c-1)\cdot\sum_{s^{\prime} \notin N(\hat{s},s)}\mu(s^{\prime})\) must be non-positive, implying that \(\sum_{s^{\prime}\in N(\hat{s},s)}\mu(s^{\prime})\leq(c-1)\cdot\sum_{s^{\prime} \notin N(\hat{s},s)}\mu(s^{\prime})\). This completes the proof.

In Algorithm 1, we always have uniform node weight for all the models which are consistent with all the feedback received so far, and node weight \(0\) for models that are inconsistent with at least one response. Prior knowledge about candidates for \(s^{*}\) can be incorporated by providing the algorithm with the input \(S_{\text{init}}\ni s^{*}\) to focus its search on; in the absence of prior knowledge, the algorithm can be given \(S_{\text{init}}=\Sigma\).

```
1:\(S\gets S_{\text{init}}\).
2:while\(|S|>1\)do
3: Let \(s\) be a model with a "small" value of \(\Phi_{S}(s)\).
4: Let \(s^{\prime}\) be the user's feedback model.
5: Set \(S\gets S\cap N(s,s^{\prime})\).
6:return the only remaining model in \(S\).
```

**Algorithm 1** Learning a model without Feedback Errors (\(S_{\text{init}}\))

Line 3 is underspecified as "small." Typically, an algorithm would choose the \(s\) with smallest \(\Phi_{S}(s)\). But computational efficiency constraints or other restrictions (see Sections 2.2 and 5) may preclude this choice and force the algorithm to choose a suboptimal \(s\). The guarantee of Algorithm 1 is summarized by the following Theorem 2.2. It is a straightforward generalization of Theorems 3 and 14 from [10], but for completeness, we give a self-contained proof.

**Theorem 2.2**: _Let \(N_{0}=|S_{\text{init}}|\) be the number of initial candidate models. If each model \(s\) chosen in Line 3 of Algorithm 1 has \(\Phi_{S}(s)\leq\beta\), then Algorithm 1 finds \(s^{*}\) using at most \(\log_{1/\beta}N_{0}\) queries._

**Corollary 2.3**: _When \(G\) is undirected and the optimal \(s\) is used in each iteration, \(\beta=\frac{1}{2}\) and Algorithm 1 finds \(s^{*}\) using at most \(\log_{2}N_{0}\) queries._

**Proof of Theorem 2.2.** Let \(S\) be the set of models that are consistent with all the query responses so far. (Initially, \(S=S_{\text{init}}\).) Let \(s\) be a model with \(\Phi_{S}(s)\leq\beta\). If the algorithm proposes \(s\) to the user, the user's feedback will be consistent with at most a \(\beta\) fraction of the models in \(S\). Note that in Algorithm 1, \(\mu(s^{\prime})=1\) for every \(s^{\prime}\in S\). Given that the set of consistent models shrinks by at least a factor of \(\beta\) in each round, it takes no more than \(\log_{1/\beta}|S_{\text{init}}|\) rounds to get it down to a single model (which must then be the target).

Next, we present the algorithm in the case of probabilistically incorrect feedback. It is a close adaptation of an algorithm by Emamjomeh-Zadeh et al. [10], which resembles a multiplicative-weights update algorithm. It keeps track of node weights \(\mu(s)\) for each model, which now exactly correspond to likelihoods of the observed responses, given that \(s\) is the target. Hence, instead of the generic name "node weight," we will refer to them as likelihoods.

In order to achieve an information-theoretically optimal dependence on \(p\), [10] run the algorithm in several stages, removing _very likely_ nodes from consideration for later inspection. Here, however, we slightly modify (in fact, simplify) the algorithm by not removing the likely nodes during the execution. This modification is crucial to make the algorithm efficiently implementable using a sampling oracle, as discussed in Section 2.2. The key "multiplicative weights" loop is reformulated and slightly generalized by Algorithm 2.

```
1:Set \(\mu(v)\gets 1\) for all models \(s\in S_{\mathrm{init}}\) and \(\mu(s)\gets 0\) for all models \(s\notin S_{\mathrm{init}}\).
2:Set \(M\leftarrow\emptyset\).
3:for\(K+1\) iterations do
4:if there exists a model \(s\) with \(\mu(s)\geq\frac{1}{2}\mu(S_{\mathrm{init}})\)then
5: Mark \(s\), by setting \(M\gets M\cup\{s\}\).
6: Let \(s\) be a model with "small" \(\Phi_{\mu}(s)\).
7: Query model \(s\), receiving feedback \(s^{\prime}\).
8:for all models \(\hat{s}\in S_{\mathrm{init}}\)do
9:if\(\hat{s}\in N(s,s^{\prime})\)then
10:\(\mu(\hat{s})\gets p\cdot\mu(\hat{s})\).
11:else
12:\(\mu(\hat{s})\leftarrow(1-p)\cdot\mu(\hat{s})\).
13:return\(M\)
```

**Algorithm 2**Multiplicative-Weights (\(S_{\mathrm{init}},K\))

Algorithm 2 is invoked several times in Algorithm 3. Algorithm 3 is given an initial candidate model set \(S_{\mathrm{init}}\), and also a _threshold_\(0<\tau<1\) (to be specified later), as well as a target error probability \(\delta\). The algorithm must output \(s^{*}\) (the target model) with probability at least \(1-\delta\), assuming that \(s^{*}\in S_{\mathrm{init}}\). The exact constants used are chosen to achieve an optimal dependency of the number of queries on \(p\) in the worst case over graphs [10]. Here and below, \(H(p)=-p\log p-(1-p)\log(1-p)\) denotes the entropy.

The performance of Algorithm 3 is summarized in Theorem 2.4, which generalizes the results of [10] to arbitrary values of \(\beta\).

**Theorem 2.4**: _Let \(\beta\in[\frac{1}{2},1)\), define \(\tau=\beta p+(1-\beta)(1-p)\), and let \(N_{0}=|S_{\mathrm{\emph{init}}}|\). Assume that \(\log(1/\tau)>H(p)\) where \(H(p)=-p\log p-(1-p)\log(1-p)\) denotes the entropy. (When \(\beta=\frac{1}{2}\), this holds for every \(p>\frac{1}{2}\).)_

_If each model \(s\) chosen in Line 6 of Algorithm 2 has \(\Phi_{\mu}(s)\leq\beta\), then with probability at least \(1-\delta\), Algorithm 3 finds \(s^{*}\) using at most \(\frac{(1-\delta)}{\log(1/\tau)-H(p)}\log N_{0}+o(\log N_{0})+O(\log^{2}(1/ \delta))\) queries in expectation._

**Corollary 2.5**: _When the graph \(G\) is undirected and the optimal \(s\) is used in each iteration, then with probability at least \(1-\delta\), Algorithm 3 finds \(s^{*}\) using at most \(\frac{(1-\delta)}{1-H(p)}\log_{2}N_{0}+o(\log N_{0})+O(\log^{2}(1/\delta))\) queries in expectation._

**Proof of Theorem 2.4.** The proof of this theorem is fairly similar to the proof of Lemma 7 in [10]. Here, we give a high-level outline of that proof, and specify the changes that need to be made for our slightly more general setting, as well as the modification we made in Algorithm 2.

Let \(s\) be the model in Line 6 of Algorithm 2. If it has \(\mu(s)\leq\frac{1}{2}\mu(S_{\text{init}})\), whatever the query response is, at most a \(\beta\) fraction of the total likelihood is multiplied by \(p\), while the rest is multiplied by \(1-p\). Therefore, the total likelihood decreases by at least a factor of \(\tau=\beta p+(1-\beta)(1-p)\). Furthermore, if \(\mu(s)>\frac{1}{2}\mu(S_{\text{init}})\) and \(s\) is not the target, we show that in expectation, the total likelihood decreases by at least a factor \(\frac{1}{2}\). This is because with probability at most \(1-p\), the query response claims that \(s\) is the target in which case \(\mu(s)\) is multiplied by \(p\), while all other nodes' likelihoods are multiplied by \(1-p\). In the remaining cases, i.e., if the response is correct, or it is incorrect but pointing to a neighbor of \(s\), \(\mu(s)\) is multiplied by \(1-p\). Hence, in expectation, the total likelihood decreases by a factor of

\[(1-p)\cdot\Big{(}p\cdot\mu(s)+(1-p)\cdot(\mu(S_{\text{init}})-\mu (s))\Big{)}+p\cdot\Big{(}(1-p)\mu(s)+p\cdot(\mu(S_{\text{init}})-\mu(s))\Big{)}\] \[\leq\frac{1}{2}\mu(S_{\text{init}})\leq\tau\mu(S_{\text{init}}).\]

To summarize, in expectation, the total likelihood decreases by at least a factor \(\tau\) in both cases. Initially, in Algorithm 2, the total likelihood of all models is \(|S_{\text{init}}|\), and in each iteration, the total likelihood decreases at least by a factor of \(\tau\), in expectation. By induction, after \(K\) rounds, the expected total likelihood is bounded by \(|S_{\text{init}}|\cdot\tau^{K}\). On the other hand, in expectation, a \(p\) fraction of the query responses is correct. Using tail bounds, for a carefully chosen value of \(\lambda\) (as in Algorithm 3, Lines 2 and 5), with "high enough" probability, a \(p-\lambda\) fraction of the responses are correct. Whenever a \(p-\lambda\) fraction of the responses is correct, the likelihood \(\mu(s^{*})\) of the target model \(s^{*}\) is at least \((p^{p-\lambda}\cdot(1-p)^{1-p+\lambda})^{K}\).

Because the statement of the theorem assumed that \(\log(1/\tau)\ >\ H(p)=-p\log p-(1-p)\log(1-p)\), or, equivalently, \(\tau<p^{p}(1-p)^{1-p}\), \(\mu(s^{*})\) decreases exponentially slower than the total likelihood of all the models; hence, \(s^{*}\) must eventually get marked by Algorithm 2 with high probability.

In fact, \(K_{1}\) and \(K_{2}\) are chosen such that this marking of \(s^{*}\) happens with sufficiently high probability within that many rounds. The precise calculations are quite similar to those in [10], butslightly more messy. [10] showed that if the first time that Algorithm 2 is invoked by Algorithm 3, it is executed for (roughly) \(\frac{\log N}{1-H(p)}\) iterations, then with high probability, \(s^{*}\) is marked. This analysis can be straightforwardly generalized to our setting, when running for \(\frac{\log N}{\log(1/\tau)-H(p)}\) rounds. The proof for the other stages of Algorithm 3 remains almost the same. \(\blacksquare\)

### Computational Considerations and Sampling

Corollaries 2.3 and 2.5 require the algorithm to find a model \(s\) with small \(\Phi_{\mu}(s)\) in each iteration. In most learning applications, the number \(N\) of candidate models is exponential in a natural problem parameter \(n\), such as the number of sample points (classification), or the number of items to rank or cluster. If computational efficiency is a concern, this precludes explicitly keeping track of the set \(S\) or the weights \(\mu(s)\). It also rules out determining the model \(s\) to query by exhaustive search over all models that have not yet been eliminated.

In some cases, these difficulties can be circumvented by exploiting problem-specific structure. A more general approach relies on Monte Carlo techniques. We show that the ability to sample models \(s\) with probability (approximately) proportional to \(\mu(s)\) (or approximately uniformly from \(S\) in the case of Algorithm 1) is sufficient to essentially achieve the results of Corollaries 2.3 and 2.5 with a computationally efficient algorithm. Notice that in both Algorithms 1 and 2, \(\mu(s)\) is completely determined by all the query responses the algorithm has seen so far and the probability \(p\).

**Theorem 2.6**: _Let \(n\) be a natural measure of the input size and assume that \(\log N\) is polynomial in \(n\). Assume that \(G=(V,E)\) is undirected5, all edge lengths are integers, and the maximum degree and diameter (both with respect to the edge lengths) are bounded by poly\((n)\). Also assume w.l.o.g. that \(\mu\) is normalized to be a distribution over the nodes6 (i.e., \(\mu(\Sigma)\) = 1)._

Footnote 5: It is actually sufficient that for every node weight function \(\mu:V\rightarrow\mathbb{R}^{+}\), there exists a model \(s\) with \(\Phi_{\mu}(s)\leq\frac{1}{2}\).

Footnote 6: For Algorithm 1, \(\mu\) is uniform over all models consistent with all feedback up to that point.

_Let \(0\leq\Delta<\frac{1}{4}\) be a constant, and assume that there is an oracle that -- given a set of query responses -- runs in polynomial time in \(n\) and returns a model \(s\) drawn from a distribution \(\mu^{\prime}\) with \(d_{\mathrm{TV}}(\mu,\mu^{\prime})\leq\Delta\). Also assume that there is a polynomial-time algorithm that, given a model \(s\), decides whether or not \(s\) is consistent with every given query response or not._

_Then, for every \(\epsilon>0\), in time poly\((n,\frac{1}{\epsilon})\), an algorithm can find a model \(s\) with \(\Phi_{\mu}(s)\leq\frac{1}{2}+2\Delta+\epsilon\), with high probability. Therefore, Algorithms 1 and 3 with \(\beta=\frac{1}{2}+2\Delta+\epsilon\) (for a sufficiently small \(\epsilon\)) can be implemented to run in time poly\((n,\frac{1}{\epsilon})\)._

Proof.The high-level idea is to use a simple local search algorithm to find a model \(s\) with small \(\Phi_{\mu}(s)\). In order to execute the updating step, we need to estimate \(\mu(N(s,s^{\prime}))\) for all neighbors \(s^{\prime}\) of \(s\) in \(G\). The key insight here is that \(\mu(N(s,s^{\prime}))\) is exactly the probability that a node drawn from \(\mu\) is consistent with the feedback \(s^{\prime}\) when \(s\) is queried. To get a sharp enough estimate of \(\mu(N(s,s^{\prime}))\), in each iteration, enough samples are drawn to ensure that tail bounds kick in and provide high-probability guarantees. The high-level algorithm is given as Algorithm 4; details -- in particular on Line 5 -- are provided below.

In Line 5 of Algorithm 4, \(P_{s,s^{\prime}}\) is estimated as the fraction of samples \(\hat{s}\) drawn from \(\mu^{\prime}\) that are in \(N(s,s^{\prime})\). Below, for a particular desired high-probability guarantee, we choose the number of samples to guarantee that

\[|P_{s,s^{\prime}}-\mu(N(s,s^{\prime}))|\leq\Delta+\epsilon^{\prime} \tag{1}\]

with high probability. For most of the proof, we will assume that all of these high-probability events occurred; at the end, we will calculate the probability of this happening.

```
1: Let \(\epsilon^{\prime}=\epsilon/3\).
2: Let \(s\) be an arbitrary model.
3:loop
4:for each edge \(e=(s,s^{\prime})\)do
5: Let \(P_{s,s^{\prime}}\) be the empirical estimation of \(\mu(N(s,s^{\prime}))\).
6:if\(P_{s,s^{\prime}}\leq\frac{1}{2}+\Delta+2\epsilon^{\prime}\) for every edge \(e=(s,s^{\prime})\)then
7:return\(s\).
8:else
9: Let \(e=(s,s^{\prime})\) be an edge out of \(s\) with \(P_{s,s^{\prime}}>\frac{1}{2}+\Delta+2\epsilon^{\prime}\).
10: Set \(s\gets s^{\prime}\).
```

**Algorithm 4** Finding a good approximate median \((\Delta,\epsilon)\)

Whenever an edge \(e=(s,s^{\prime})\) has \(P_{s,s^{\prime}}\leq\frac{1}{2}+\Delta+2\epsilon^{\prime}\), we can bound \(\mu(N(s,s^{\prime}))\leq\frac{1}{2}+2\Delta+3\epsilon^{\prime}=\frac{1}{2}+2 \Delta+\epsilon\). Thus, whenever Algorithm 4 returns a model \(s\), the model satisfies \(\Phi_{\mu}(s)\leq\frac{1}{2}+2\Delta+\epsilon\).

It remains to show that the algorithm terminates, and in a polynomial number of iterations. Define \(\Psi_{\mu}(s)=\sum_{s^{\prime}}\mu(s^{\prime})d(s,s^{\prime})\) to be the weighted distance (with respect to the edge lengths \(\omega_{e}\)) from \(s\) to all other models. When Algorithm 4 switches from \(s\) to \(s^{\prime}\) in Line 10, by Inequality (1), we have \(\mu(N(s,s^{\prime}))\geq\frac{1}{2}+\Delta+2\epsilon^{\prime}-(\Delta+\epsilon ^{\prime})=\frac{1}{2}+\epsilon^{\prime}\), so \(\Psi_{\mu}(s^{\prime})\leq\Psi_{\mu}(s)-2\epsilon^{\prime}\cdot\omega_{e}\). Because the value of \(\Psi_{\mu}(s)\) for all \(s\) is bounded by the diameter of \(G\), which was assumed to be bounded by \(\mathrm{poly}(n)\), and the edge lengths are all positive integers, Algorithm 4 terminates after \(\mathrm{poly}(n,1/\epsilon)\) steps.

The only remaining part is to compute how many samples from the oracle are required to guarantee Inequality (1) with high enough probability. Drawing \(r\) samples, by standard tail bounds, Inequality (1) fails with probability no more than \(e^{-\Omega(\epsilon^{2}r)}\). Because all degrees are bounded by \(\mathrm{poly}(n)\), Line 5 of Algorithm 4 is executed only \(\mathrm{poly}(n,1/\epsilon)\) times, so it suffices to draw \(r=\mathrm{poly}(\frac{1}{\epsilon},\log n)\) samples in each iteration in order to apply a union bound over all iterations of the algorithm. \(\blacksquare\)

## 3 Application I: Learning a Ranking

As a first application, we consider the task of learning the correct order of \(n\) elements with supervision in the form of equivalence queries. This task is directly motivated by learning a user's preference over web search results (e.g., [12, 19]), restaurant or movie orders (e.g., [9]), or many other types of entities. Using pairwise _active_ queries ("Do you think that A should be ranked ahead of B?"), a learning algorithm could of course simulate standard \(O(n\log n)\) sorting algorithms; this number of queries is necessary and sufficient. However, when using equivalence queries, the user must be presented with a complete ordering (i.e., a permutation \(\pi\) of the \(n\) elements), and the feedback will be a _mistake_ in the proposed permutation. Here, we propose interactive algorithms for learning the correct ranking without additional information or assumptions.7 We first describe results for a setting with simple feedback in the form of adjacent transpositions; we then show a generalization to more realistic feedback as one is wont to receive in applications such as search engines.

Footnote 7: For example, [12, 19, 9] map items to feature vectors and assume linearity of the target function(s).

### Adjacent Transpositions

We first consider "Bubble Sort" feedback of the following form: the user specifies that elements \(i\) and \(i+1\) in the proposed permutation \(\pi\) are in the wrong relative order. An obvious correction for an algorithm would be to swap the two elements, and leave the rest of \(\pi\) intact. This algorithm would exactly implement Bubble Sort, and thus require \(\Theta(n^{2})\) equivalence queries. Our general framework allows us to easily obtain an algorithm with \(O(n\log n)\) equivalence queries instead. We define the undirected and unweighted graph \(G_{\mathrm{BS}}\) as follows:

* \(G_{\mathrm{BS}}\) contains \(N=n!\) nodes, one for each permutation \(\pi\) of the \(n\) elements;
* it contains an edge between \(\pi\) and \(\pi^{\prime}\) if and only if \(\pi^{\prime}\) can be obtained from \(\pi\) by swapping two adjacent elements.

**Lemma 3.1**: \(G_{\mathrm{BS}}\) _satisfies Definition 2.1 with respect to Bubble Sort feedback._

**Proof.** By definition, there is one node for each permutation, and the edges of \(G_{\mathrm{BS}}\) exactly capture the possible feedback provided in response to the query. For two permutations \(\pi,\pi^{*}\), let \(\tau(\pi,\pi^{*})=|\{(i,j)\mid i\) precedes \(j\) in \(\pi\) and follows \(j\) in \(\pi^{*}\}|\) denote the Kendall \(\tau\) distance. Since an adjacent transposition can fix the ordering of exactly one pair \((i,j)\), the distance between \(\pi,\pi^{*}\) in \(G_{\mathrm{BS}}\) is exactly equal to \(\tau(\pi,\pi^{*})\). If the user proposes \(\pi^{\prime}\) in response to \(\pi\), then \(\pi^{\prime}\) must fix exactly one inversion between \(\pi\) and \(\pi^{*}\), so the distance between \(\pi^{\prime}\) and \(\pi^{*}\) is \(\tau(\pi^{\prime},\pi^{*})=\tau(\pi,\pi^{*})-1\). Thus, \(\pi^{\prime}\) lies on a shortest path from \(\pi\) to \(\pi^{*}\).

Hence, applying Corollary 2.3 and Theorem 2.4, we immediately obtain the existence of learning algorithms with the following properties:

**Corollary 3.2**: _Assume that in response to each equivalence query on a permutation \(\pi\), the user responds with an adjacent transposition (or states that the proposed permutation \(\pi\) is correct)._

1. _If all query responses are correct, then the target ordering can be learned by an interactive algorithm using at most_ \(\log N=\log n!\leq n\log n\) _equivalence queries._
2. _If query responses are correct with probability_ \(p>\frac{1}{2}\)_, the target ordering can be learned by an interactive algorithm with probability at least_ \(1-\delta\) _using at most_ \(\frac{(1-\delta)}{1-H(p)}n\log n+o(n\log n)+O(\log^{2}(1/\delta))\) _equivalence queries in expectation._

Up to constants, the bound of Corollary 3.2 is optimal: Theorem 3.3 shows that \(\Omega(n\log n)\) equivalence queries are necessary in the worst case. Notice that Theorem 3.3 does not immediately follow from the classical lower bound for sorting with pairwise comparisons: while the result of a pairwise comparison always reveals one bit, there are \(n-1\) different possible responses to an equivalence query, so up to \(O(\log n)\) bits might be revealed. For this reason, the proof of Theorem 3.3 explicitly constructs an adaptive adversary, and does not rely on a simple counting argument.

**Theorem 3.3**: _With adversarial responses, any interactive ranking algorithm can be forced to ask \(\Omega(n\log n)\) equivalence queries. This is true even if the true ordering is chosen uniformly at random, and only the query responses are adversarial._

**Proof.** Let \({\cal A}\) be an arbitrary interactive algorithm which learns the underlying order. In each round, \({\cal A}\) proposes a permutation \(\pi\) and receives feedback in the form of an adjacent transposition. We start with the case when both the correct ordering and the responses are adversarial. We define an adaptive adversary \({\cal B}\) which forces \({\cal A}\) to take \(\Omega(n\log n)\) rounds before it finds the correct ordering \(\pi^{*}\).

The adversary \({\cal B}\) gradually marks elements as '\(+\)' or '\(-\)', trying to delay labeling for as long as possible. Initially, all \(n\) elements are unmarked. When \({\cal A}\) proposes a permutation \(\pi\), \({\cal B}\) looks for two consecutive elements \(i=\pi_{k},j=\pi_{k+1}\) in \(\pi\) which are both unmarked. If such a pair exists, \({\cal B}\) returns \((k,k+1)\) as feedback, i.e., it tells the algorithm that \(i\) and \(j\) are in the wrong order. Then, it marks \(i\) with '\(+\)' and \(j\) with '\(-\)'. Because \({\cal B}\) marks exactly two new elements in each round, and any permutation with fewer than \(\lfloor n/2\rfloor\) marked elements must have two consecutive marked elements, \({\cal B}\) can keep following this strategy for at least \(\left\lfloor\frac{n}{4}\right\rfloor\) rounds.

At this point, the algorithm starts its second stage. It partitions the elements into two sets: \(L_{-}\) and \(L_{+}\). The partition satisfies the following conditions:

* All elements marked with '\(-\)' are in \(L_{-}\), and all elements marked with '\(+\)' are in \(L_{+}\).
* Elements are partitioned as evenly as possible: \(|L_{-}|\geq\left\lfloor\frac{n}{2}\right\rfloor\) and \(|L_{+}|\geq\left\lfloor\frac{n}{2}\right\rfloor\).

Notice that such a partition always exists, because the number of elements marked '\(+\)' and '\(-\)' are the same. \({\cal B}\) commits to the fact that in \(\pi^{*}\), all elements of \(L_{-}\) will precede all elements of \(L_{+}\), but leaves \(\pi^{*}\) unspecified beyond that. Notice that \({\cal A}\) has not received any feedback on the relative ordering of any pair of elements in \(L_{-}\) or any pair in \(L_{+}\). In the subsequent rounds, \({\cal B}\) responds as follows:

* If \({\cal A}\) proposes a permutation \(\pi\) in which an element \(j\in L_{-}\) appears after an element \(i\in L_{+}\), then \(\pi\) must contain an _adjacent_ such pair \((i,j)\). In that case, \({\cal B}\) provides the feedback that \((i,j)\) are out of order. In fact, this provides \({\cal A}\) with no new information beyond \(L_{-}\) and \(L_{+}\), which it was assumed to already know.
* Otherwise, in \(\pi\), all elements of \(L_{-}\) must precede all elements of \(L_{+}\). In that case, \({\cal B}\) will first recursively follow the same strategy on \(L_{-}\), and then recursively follow the same strategy on \(L_{+}\).

Let \(Q(n)\) be the minimum number of rounds that \({\cal A}\) requires against this adversarial strategy \({\cal B}\). The description of the adversary strategy implies the following recurrence: \(Q(n)\geq\left\lfloor\frac{n}{4}\right\rfloor+2\cdot Q(\left\lfloor\frac{n}{2} \right\rfloor)\). Thus, by the master theorem, \(Q(n)=\Omega(n\log n)\), proving the theorem.

In the given proof, \({\cal B}\) provides adversarial feedback and gradually commits to an adversarial permutation. However, even if the true permutation \(\pi^{*}\) is chosen uniformly at random ahead of time, \({\cal B}\) can still follow essentially the same approach to provide adversarial feedback with respect to \(\pi^{*}\).

Fix \(\pi^{*}\), and consider the first stage of \({\cal B}\), where it assigns '\(-\)' and '\(+\)' to the items. When \({\cal A}\) proposes a permutation \(\pi\), every pair \((i,j)\) of adjacent unmarked items in \(\pi\) is, with probability exactly \(\frac{1}{2}\), in the wrong order with respect to \(\pi^{*}\). If \(n^{\prime}\) elements are already marked, there are at least \(\frac{n-2n^{\prime}-1}{2}\)_disjoint_ pairs of adjacent unmarked items, each of which is in the wrong order independently with probability exactly \(\frac{1}{2}\). Thus, for each of the first \(\frac{n}{8}-1\) rounds, the probability that \({\cal B}\) fails to find an unmarked adjacent pair in the wrong order is less than \(2^{-\frac{n}{4}}\). After \(\frac{n}{8}-1\) rounds, it starts its second stage, and a similar argument applies. Because the failure probability is exponentially low, we can take a union bound over all rounds until \(n\) is sufficiently small, and obtain that with high probability, \({\cal A}\) requires \(\Omega(n\log n)\) queries on a random permutation.

### Implicit Feedback from Clicks

In the context of search engines, it has been argued (e.g., by [12, 19, 1]) that a user's clicking behavior provides implicit feedback of a specific form on the ranking. Specifically, since users will typically read the search results from first to last, when a user skips some links that appear earlier in the ranking, and instead clicks on a link that appears later, her action suggests that the later link was more informative or relevant.

Formally, when a user clicks on the element at index \(i\), but did not previously click on any elements at indices \(j,j+1,\ldots,i-1\), this is interpreted as feedback that element \(i\) should precede all of elements \(j,j+1,\ldots,i-1\). Thus, the feedback is akin to an "Inserion Sort" move. (The Bubble Sort feedback model is the special case in which \(j=i-1\) always.)

To model this more informative feedback, the new graph \(G_{\mathrm{IS}}\) has more edges, and the edge lengths are non-uniform. It contains the same \(N\) nodes (one for each permutation). For a permutation \(\pi\) and indices \(1\leq j<i\leq n\), \(\pi_{j\gets i}\) denotes the permutation that is obtained by moving the \(i^{\mathrm{th}}\) element in \(\pi\) before the \(j^{\mathrm{th}}\) element (and thus shifting elements \(j,j+1,\ldots,i-1\) one position to the right). In \(G_{\mathrm{IS}}\), for every permutation \(\pi\) and every \(1\leq j<i\leq n\), there is an undirected edge from \(\pi\) to \(\pi_{j\gets i}\) with length \(i-j\). Notice that for \(i>j+1\), there is actually no user feedback corresponding to the edge from \(\pi_{j\gets i}\) to \(\pi\); however, additional edges are permitted, and Lemma 3.4 establishes that \(G_{\mathrm{IS}}\) does in fact satisfy the "shortest paths" property.

**Lemma 3.4**: \(G_{\mathrm{IS}}\) _satisfies Definition 2.1 with respect to Inversion Sort feedback._

**Proof.** As in the proof of Lemma 3.1, there is one node for each permutation, and for each possible Insertion Sort feedback given in response to \(\pi\), there is an edge in \(G_{\mathrm{IS}}\) by definition (though \(G_{\mathrm{IS}}\) contains additional edges).

As with \(G_{\mathrm{BS}}\), the distance between two permutations \(\pi,\pi^{*}\) in \(G_{\mathrm{IS}}\) (now with respect to the given edge lengths) is still equal to the Kendall \(\tau(\pi,\pi^{*})\). This is because going from \(\pi\) to \(\pi_{j\gets i}\) transposes exactly \(i-j\) pairs of elements, which is the length of the corresponding edge, so no edge with \(i>j+1\) is essential for any shortest path.

When the user feedback \(\pi^{\prime}=\pi_{j\gets i}\) indicates that the \(i^{\mathrm{th}}\) element should be placed ahead of all the elements in positions \(j,j+1,\ldots,i-1\), then the \(i^{\mathrm{th}}\) element does indeed precede all of these elements in \(\pi^{*}\). Thus, \(\tau(\pi^{\prime},\pi^{*})=\tau(\pi,\pi^{*})-(i-j)\), and the edge \((\pi,\pi^{\prime})\) lies on a shortest path from \(\pi\) to \(\pi^{*}\). Notice that the "extraneous" edges of the form \((\pi_{j\gets i},\pi)\) for \(i>j+1\) (of cost \(i-j\)) do not affect any shortest paths between pairs \(\pi,\pi^{*}\), as they can be replaced with the corresponding \(i-j\) adjacent transpositions, without increasing the total length of the path.

As in the case of \(G_{\mathrm{BS}}\), by applying Corollary 2.3 and Theorem 2.4, we immediately obtain the existence of interactive learning algorithms with the same guarantees as those of Corollary 3.2.

**Corollary 3.5**: _Assume that in response to each equivalence query, the user responds with a pair of indices \(j<i\) such that element \(i\) should precede all elements \(j,j+1,\ldots,i-1\)._

1. _If all query responses are correct, then the target ordering can be learned by an interactive algorithm using at most_ \(\log N=\log n!\leq n\log n\) _equivalence queries._
2. _If query responses are correct with probability_ \(p>\frac{1}{2}\)_, the target ordering can be learned by an interactive algorithm with probability at least_ \(1-\delta\) _using at most_ \(\frac{(1-\delta)}{1-H(p)}n\log n+o(n\log n)+O(\log^{2}(1/\delta))\) _equivalence queries in expectation._

### Computational Considerations

While Corollaries 3.2 and 3.5 imply interactive algorithms using only \(O(n\log n)\) equivalence queries, they do not guarantee that the internal computations of the algorithms are efficient. The naive implementation requires explicitly keeping track of and comparing likelihoods on all \(N=n!\) nodes.

When \(p=1\), i.e., the algorithm only receives correct feedback, it can be made computationally efficient using Theorem 2.6. To apply Theorem 2.6, it suffices to show that one can efficiently sample a (nearly) uniformly random permutation \(\pi\) consistent with all feedback received so far. Since the feedback is assumed to be correct, the set of all pairs \((i,j)\) such that the user implied that element \(i\) must precede element \(j\) must be acyclic, and thus must form a partial order. The sampling problem is thus exactly the problem of sampling a _linear extension_ of a given partial order.

This is a well-known problem, and a beautiful result of Bubley and Dyer [8, 7] shows that the Karzanov-Khachiyan Markov Chain [14] mixes rapidly. Huber [11] shows how to modify the Markov Chain sampling technique to obtain an exactly (instead of approximately) uniformly random linear extension of the given partial order. For the purpose of our interactive learning algorithm, the sampling results can be summarized as follows:

**Theorem 3.6** (Huber [11]): _Given a partial order over \(n\) elements, let \(\mathcal{L}\) be the set of all linear extensions, i.e., the set of all permutations consistent with the partial order. There is an algorithm that runs in expected time \(O(n^{3}\log n)\) and returns a uniformly random sample from \(\mathcal{L}\)._

The maximum node degree in \(G_{\mathrm{BS}}\) is \(n-1\), while the maximum node degree in \(G_{\mathrm{IS}}\) is \(O(n^{2})\). The diameter of both \(G_{\mathrm{BS}}\) and \(G_{\mathrm{IS}}\) is \(O(n^{2})\). Substituting these bounds and the bound from Theorem 3.6 into Theorem 2.6, we obtain the following corollary:

**Corollary 3.7**: _Both under Bubble Sort feedback and Insersion Sort feedback, if all feedback is correct, there is an efficient interactive learning algorithm using at most \(\log n!\leq n\log n\) equivalence queries to find the target ordering._

The situation is significantly more challenging when feedback could be incorrect, i.e., when \(p<1\). In this case, the user's feedback is not always consistent and may not form a partial order. In fact, we prove the following hardness result.

**Theorem 3.8**: _There exists a \(p\) (depending on \(n\)) for which the following holds. Given a set of user responses, let \(\mu(\pi)\) be the likelihood of \(\pi\) given the responses, and normalized so that \(\sum_{\pi}\mu(\pi)=1\). Let \(0<\Delta<1\) be any constant. There is no polynomial-time algorithm to draw a sample from a distribution \(\mu^{\prime}\) with \(d_{\mathrm{TV}}(\mu,\mu^{\prime})\leq 1-\Delta\) unless \(\mbox{RP}=\mbox{NP}\)._

**Proof.** We prove this theorem using a reduction from Minimum Feedback Arc Set, a well-known NP-complete problem [13]. Given a directed graph \(G\) and number \(k\), the Minimum Feedback Arc Set problem asks if there is a set of at most \(k\) arcs of \(G\) whose removal will leave the remaining graph acyclic. This is equivalent to asking if there is a permutation \(\pi\) of the nodes of \(G\) such that at most \(k\) arcs go from higher-numbered nodes in \(\pi\) to lower-numbered ones.

Given \(\Delta\), a graph \(G\) with \(n\) nodes and \(m\) edges, and \(k\), we define the following sampling problem. Consider sampling from permutations of \(n\) elements, let \(p=1-\frac{1}{2(n+1)!}\), and let the \(m\) user responses be exactly the (directed) edges of \(G\).

For any permutation \(\pi\), let \(x_{\pi}\) be the number of queries that \(\pi\) agrees with, and \(y_{\pi}\) the number of queries that \(\pi\) disagrees with. Then, for all \(\pi\), \(x_{\pi}+y_{\pi}=m\), and the (unnormalized) likelihoodfor \(\pi\) is \(L(\pi)=p^{x_{\pi}}\cdot(1-p)^{y_{\pi}}\). Let \(y^{*}=\min_{\pi}y_{\pi}\), and let \(\Pi^{*}=\{\pi\mid y_{\pi}=y^{*}\}\) be the set of all permutations minimizing \(y_{\pi}\). Then, for any permutation \(\pi\in\Pi^{*}\), we have

\[L(\pi)\;=\;\left(1-\frac{1}{2(n+1)!}\right)^{m-y^{*}}\cdot\left(\frac{1}{2(n+1 )!}\right)^{y^{*}}\;=:\;L^{*}.\]

On the other hand, for any permutation \(\pi^{\prime}\notin\Pi^{*}\), we get that

\[L(\pi^{\prime}) \leq\;\left(1-\frac{1}{2(n+1)!}\right)^{m-y^{*}-1}\cdot\left( \frac{1}{2(n+1)!}\right)^{y^{*}+1}\] \[=L^{*}\cdot\frac{1}{2(n+1)!}/\left(1-\frac{1}{2(n+1)!}\right)\] \[\leq\;\frac{L^{*}}{(n+1)!}.\]

Thus, under the normalized likelihood distribution \(\mu\), the total sampling probability of all permutations \(\pi\in\Pi^{*}\) must be

\[\sum_{\pi\in\Pi^{*}}\mu(\pi) =\;\frac{\sum_{\pi\in\Pi^{*}}L(\pi)}{\sum_{\pi^{\prime}}L(\pi^{ \prime})}\] \[=\;\frac{L^{*}\cdot|\Pi^{*}|}{L^{*}\cdot|\Pi^{*}|+\sum_{\pi^{ \prime}\notin\Pi^{*}}L(\pi^{\prime})}\] \[\geq\;\frac{L^{*}\cdot|\Pi^{*}|}{L^{*}\cdot|\Pi^{*}|+n!\cdot L^{* }\cdot\frac{1}{(n+1)!}}\] \[=\;\frac{|\Pi^{*}|}{|\Pi^{*}|+1/(n+1)}\] \[\geq\;1-1/(n+1).\]

If \(\mu^{\prime}\) has total variation distance at most \(1-\Delta\) from \(\mu\), it must satisfy \(\sum_{\pi\in\Pi^{*}}\mu^{\prime}(\pi)\geq\sum_{\pi\in\Pi^{*}}\mu(\pi)-(1- \Delta)\geq\Delta-1/(n+1)\). In particular, it must sample a permutation \(\pi\in\Pi^{*}\) with constant probability \(\Delta-1/(n+1)\).

A randomized algorithm can now simply sample \(O(\log n)\) permutations \(\pi\) according to \(\mu^{\prime}\). If one of these permutations, applied to the nodes of \(G\), has at most \(k\) edges going from higher-numbered to lower-numbered nodes, it constitutes a feedback arc set of at most \(k\) edges, and the algorithm can correctly answer "Yes" to the Minimum Feedback Arc Set instance. When the algorithm sees no \(\pi\) with fewer than \(k+1\) edges going from higher-numbered to lower-numbered nodes, it answers "No." This answer may be incorrect. But notice that if it is incorrect, the Minimum Feedback Arc Set instance must have had a feedback arc set of at most \(k\) edges, and the randomized algorithm would sample at least one corresponding permutation \(\pi\) with high probability. Thus, when the algorithm answers "No," it is correct with high probability. Thus, we have an RP algorithm for Minimum Feedback Arc Set under the assumption of an efficient approximate sampling oracle. \(\blacksquare\)

It should be noted that the value of \(p\) in the reduction is exponentially close to \(1\). In this range, incorrect feedback is so unlikely that with high probability, the algorithm will always see a partial order. It might then still be able to sample efficiently. On the other hand, for smaller values of \(p\) (e.g., constant \(p\)), sampling approximately from the likelihood distribution might be possible via a metropolized Karzanov-Khachiyan chain or a different approach. This problem is still open.

### Arbitrary Swap Model

In order to demonstrate that the condition of Definition 2.1 is not trivial to satisfy, we consider another natural feedback model for ranking. In the Arbitrary Swap model, a user can exhibit two _arbitrary_ elements \(i,j\) that are in the wrong order; doing so does not imply anything about the relation between \(i,j\) and the elements that are between them. We will show that in contrast to the Insersion Sort and Bubble Sort models, there is _no_ almost-undirected graph \(G\) satisfying Definition 2.1; hence, our general framework cannot lead to an \(o(n^{2})\) interactive algorithm for learning a ranking in the Arbitrary Swap model.

**Theorem 3.9**: _For the Arbitrary Swap model, there is no directed graph \(G\) which is almost undirected with \(c<n\) and satisfies Definition 2.1._

**Proof.** Assume that there is a graph \(G\) which satisfies the definition. For every \(1\leq i\leq n\), define the permutation \(\pi_{i}=\langle i,i+1,\ldots,n,1,\ldots,i-1\rangle\) and let \(S=\{\pi_{i}\mid 1\leq i\leq n\}\). Let \(\mu\) be the node weight function that assigns uniform weight to every \(\pi_{i}\) and \(0\) to all other permutations.

Consider an arbitrary permutation \(\pi\) proposed to the user. We show that there exists a response that it is consistent with every permutation in \(S\) but one. Distinguish the following two cases for the proposed \(\pi\):

* If there exists \(1\leq i<n\) such that \(\pi(i+1)<\pi(i)\) (i.e., \(i+1\) precedes \(i\) in \(\pi\)), then the response "\(i\)_and \(i+1\) are in the wrong order_" is consistent with every permutation in \(S\) except \(\pi_{i+1}\).
* If \(\pi(i)<\pi(i+1)\) for every \(1\leq i<n\), then \(\pi=\langle 1,2,\ldots,n\rangle\). In this case, "\(n\)_and \(1\) are in the wrong order_" is a response that is consistent with every permutation in \(S\) except \(\pi_{1}\).

Hence, \(\Phi_{\mu}(\pi)\geq\frac{n-1}{n}\) for every permutation \(\pi\). This implies that \(G\) cannot be almost undirected with \(c<n\); otherwise, Proposition 2.1 would imply the existence of a permutation \(\pi\) with \(\Phi_{\mu}(\pi)<\frac{n-1}{n}\). \(\blacksquare\)

While Theorem 3.9 rules out an algorithm based on the graph framework we propose, it is worth noting that there is an algorithm (not based on our framework) that, in the absence of noise, can learn the correct permutation under the Arbitrary Swap model using \(O(n\log n)\) queries. It is an interesting question for future work to generalize our model so that it contains this algorithm as a natural special case.

## 4 Application II: Learning a Clustering

Many traditional approaches for clustering optimize an (explicit) objective function or rely on assumptions about the data generation process. In interactive clustering, the algorithm repeatedly proposes a clustering, and obtains feedback that two proposed clusters should be merged, or a proposed cluster should be split into two. There are \(n\) items, and a _clustering_\(\mathcal{C}\) is a partition of the items into disjoint sets (_clusters_) \(C_{1},C_{2},\ldots\). It is known that the target clustering has \(k\) clusters, but in order to learn it, the algorithm can query clusterings with more or fewer clusters as well. The user feedback has the following semantics, as proposed by Balcan and Blum [6] and Awasthi et al. [5, 4].

1. Merge\((C_{i},C_{j})\): Specifies that all items in \(C_{i}\) and \(C_{j}\) belong to the same cluster.
2. Split\((C_{i})\): Specifies that cluster \(C_{i}\) needs to be split, but not into which subclusters.

Notice that feedback that two clusters be merged, or that a cluster be split (when the split is known), can be considered as adding constraints on the clustering (see, e.g., [22]); depending on whether feedback may be incorrect, these constraints are hard or soft.

We define a weighted and _directed_ graph \(G_{\text{UC}}\) on all clusterings \(\mathcal{C}\). Thus, \(N=B_{n}\leq n^{n}\) is the \(n^{\text{th}}\) Bell number. When \(\mathcal{C}^{\prime}\) is obtained by a Merge of two clusters in \(\mathcal{C}\), \(G_{\text{UC}}\) contains a directed edge \((\mathcal{C},\mathcal{C}^{\prime})\) of length \(2\). If \(\mathcal{C}=\{C_{1},C_{2},\ldots\}\) is a clustering, then for each \(C_{i}\in\mathcal{C}\), the graph \(G_{\text{UC}}\) contains a directed edge of length \(1\) from \(\mathcal{C}\) to \(\mathcal{C}\setminus\{C_{i}\}\cup\{\{v\}\mid v\in C_{i}\}\). That is, \(G_{\text{UC}}\) contains an edge from \(\mathcal{C}\) to the clustering obtained from breaking \(C_{i}\) into singleton clusters of all its elements. While this may not be the "intended" split of the user, we can still associate this edge with the feedback.

**Lemma 4.1**: \(G_{\text{UC}}\) _satisfies Definition 2.1 with respect to Merge and Split feedback._

**Proof.** \(G_{\text{UC}}\) has a node for every clustering, and its edges capture every possible user feedback.8

Footnote 8: As mentioned before, we _translate_ user feedback of the form Split into a request for breaking the cluster into singletons. From the user’s perspective, nothing changes.

Let \(\mathcal{C}=\{C_{1},\ldots,C_{k}\}\) and \(\mathcal{C}^{\prime}=\{C^{\prime}_{1},\ldots,C^{\prime}_{k^{\prime}}\}\) be two clusterings with \(k\) and \(k^{\prime}\) clusters, respectively. We call a cluster \(C\in\mathcal{C}\)_mixed_ (with respect to \(\mathcal{C}^{\prime}\)) if it contains elements from at least two different clusters in \(\mathcal{C}^{\prime}\). Let \(x_{\mathcal{C},\mathcal{C}^{\prime}}\) (\(x\) for short) be the number of mixed clusters \(C\in\mathcal{C}\) with respect to \(\mathcal{C}^{\prime}\), and \(y_{\mathcal{C},\mathcal{C}^{\prime}}\) (\(y\) for short) the total number of elements in mixed clusters. Notice that it is possible that \(x_{\mathcal{C},\mathcal{C}^{\prime}}\neq x_{\mathcal{C}^{\prime},\mathcal{C}}\), and similarly for \(y\). Define the (asymmetric) distance \(d(\mathcal{C},\mathcal{C}^{\prime})=2y_{\mathcal{C},\mathcal{C}^{\prime}}-x_{ \mathcal{C},\mathcal{C}^{\prime}}+2(k-k^{\prime})\). We claim that the length of every shortest path from \(\mathcal{C}\) to \(\mathcal{C}^{\prime}\) with respect to the edge lengths \(\omega_{e}\) is \(d(\mathcal{C},\mathcal{C}^{\prime})\).

First, we show that there exists a path of length \(d(\mathcal{C},\mathcal{C}^{\prime})\) from \(\mathcal{C}\) to \(\mathcal{C}^{\prime}\). Start the path by breaking the \(x\) mixed clusters in \(\mathcal{C}\), using Split edges of length \(1\) each. At this point, we have a clustering \(\mathcal{C}^{\prime\prime}\) with \(y+k-x\) clusters, each of which is a subset of one of the clusters in \(\mathcal{C}^{\prime}\). Then, using \(y+k-x-k^{\prime}\) cluster merges (each of edge length \(2\)), we obtain \(\mathcal{C}^{\prime}\). The total length of this path is \(x+2(y+k-x-k^{\prime})=d(\mathcal{C},\mathcal{C}^{\prime})\).

Next, we show that there is no path in \(G_{\text{UC}}\) from \(\mathcal{C}\) to \(\mathcal{C}^{\prime}\) shorter than the claimed bound of \(d(\mathcal{C},\mathcal{C}^{\prime})\). We do so by induction on the number of edges in the path. In the base case of \(0\) edges, \(\mathcal{C}=\mathcal{C}^{\prime}\), so the claimed bound of \(d(\mathcal{C},\mathcal{C}^{\prime})=0\) is a lower bound. Now consider an edge \((\mathcal{C},\bar{\mathcal{C}})\) which is the first edge on a path from \(\mathcal{C}\) to \(\mathcal{C}^{\prime}\). Let \(\bar{k}\) be the number of clusters in \(\bar{\mathcal{C}}\), and \(x=x_{\mathcal{C},\mathcal{C}^{\prime}}\), \(y=y_{\mathcal{C},\mathcal{C}^{\prime}}\), \(\bar{x}=x_{\bar{\mathcal{C}},\mathcal{C}^{\prime}}\), \(\bar{y}=y_{\bar{\mathcal{C}},\mathcal{C}^{\prime}}\). We distinguish two cases based on the type of edge from \(\mathcal{C}\) to \(\bar{\mathcal{C}}\).

* If \((\mathcal{C},\bar{\mathcal{C}})\) is a Merge edge, then \(\omega_{(\mathcal{C},\bar{\mathcal{C}})}=2\), and \(\bar{k}=k-1\). We distinguish two subcases, based on the two clusters \(C_{1},C_{2}\in\mathcal{C}\) that were merged: 1. If \(C_{1}\) or \(C_{2}\) was mixed, or \(C_{1}\cup C_{2}\) is not mixed, then \(\bar{x}\leq x\) and \(\bar{y}\geq y\) (because merging two clusters cannot remove any elements from mixed clusters). In particular, \(2\bar{y}-\bar{x}\geq 2y-x\). 2. If neither \(C_{1}\) not \(C_{2}\) was mixed, but the new cluster \(C_{1}\cup C_{2}\) is mixed, then \(\bar{x}=x+1\) and \(\bar{y}=y+|C_{1}|+|C_{2}|\geq y+2\). Therefore, again \(2\bar{y}-\bar{x}\geq 2y+4-(x+1)\geq 2y-x\). In either case, \(2\bar{y}-\bar{x}\geq 2y-x\), so \[d(\bar{\mathcal{C}},\mathcal{C}^{\prime}) =2\bar{y}-\bar{x}+2(\bar{k}-k^{\prime})\] \[\geq 2y-x+2((k-1)-k^{\prime})\] \[=d(\mathcal{C},\mathcal{C}^{\prime})-2\] \[=d(\mathcal{C},\mathcal{C}^{\prime})-\omega_{(\mathcal{C},\bar{ \mathcal{C}})}.\]* If \(({\cal C},\bar{\cal C})\) is a Split\((C)\) edge, then \(\omega_{({\cal C},\bar{\cal C})}=1\), and \(\bar{k}=k+|C|-1\). Again, there can be at most one fewer mixed cluster (namely, \(C\)). If \(C\) was mixed, then \(\bar{x}=x-1\) and \(\bar{y}=y-|C|\). Otherwise, \(\bar{x}=x\) and \(\bar{y}=y\). In both cases, we have that \(2\bar{y}-\bar{x}\geq 2y-x-2|C|+1\). Thus, \[d(\bar{\cal C},{\cal C}^{\prime}) =2\bar{y}-\bar{x}+2(\bar{k}-k^{\prime})\] \[\geq 2y-x-2|C|+1+2(k+|C|-1-k^{\prime})\] \[=2y-x+2(k-k^{\prime})-1\] \[=d({\cal C},{\cal C}^{\prime})-1\] \[=d({\cal C},{\cal C}^{\prime})-\omega_{({\cal C},\bar{\cal C})}.\]

In both cases, we can apply induction to \({\cal C}^{\prime}\), and conclude that there is no path of total length less than \(d({\cal C},{\cal C}^{\prime})\) from \({\cal C}\) to \({\cal C}^{\prime}\).

Finally, we verify that every correct feedback \(\bar{\cal C}\) to a queried clustering \({\cal C}\) lies on a path of length \(d({\cal C},{\cal C}^{*})\) from \({\cal C}\) to the target clustering \({\cal C}^{*}\).

* If \(({\cal C},\bar{\cal C})\) is a correct user response in the form of Merge, then \(x_{\bar{\cal C},{\cal C}^{*}}=x_{{\cal C},{\cal C}^{*}}\) and \(y_{\bar{\cal C},{\cal C}^{*}}=y_{{\cal C},{\cal C}^{*}}\). However, \(\bar{\cal C}\) has one fewer cluster than \({\cal C}\), so \[d(\bar{\cal C},{\cal C}^{*})\;=\;d({\cal C},{\cal C}^{*})-2\;=\;d({\cal C},{ \cal C}^{*})-\omega_{({\cal C},\bar{\cal C})}.\]
* If \(({\cal C},{\cal C}^{\prime})\) is a correct response in the form of Split and \(C\) is the cluster that needs to be split/broken, then \(x_{\bar{\cal C},{\cal C}^{*}}=x_{{\cal C},{\cal C}^{*}}-1\) and \(y_{\bar{\cal C},{\cal C}^{*}}=y_{{\cal C},{\cal C}^{*}}-|C|\). Moreover, \(\bar{\cal C}\) has \(|C|-1\) more clusters than \({\cal C}\). By applying all these equations, similar to the earlier calculations, we get that \[d(\bar{\cal C},{\cal C}^{*})\;=\;d({\cal C},{\cal C}^{*})-1\;=\;d({\cal C},{ \cal C}^{*})-\omega_{({\cal C},\bar{\cal C})}.\]

In both cases, by induction on \(d({\cal C},{\cal C}^{*})\), we show that every correct user feedback from \({\cal C}\) lies on a path of length \(d({\cal C},{\cal C}^{*})\) to \({\cal C}^{*}\).

Finally, we show that each edge is part of "short" cycle. Consider any two clusterings \({\cal C}\), \({\cal C}^{\prime}\) with \(k,k^{\prime}\) clusters, respectively. By using \(k-1\)Split operations (of length \(1\) each), we can first break \({\cal C}\) into all singletons. Then, by using \(n-k^{\prime}\)Merge operations (the edges having length \(2\) each), we can obtain \({\cal C}^{\prime}\). The total length of this path is at most \(k-1+2(n-k^{\prime})\leq 3n-3\). In particular, for any edge \(({\cal C},{\cal C}^{\prime})\), there is a "returning" path from \({\cal C}^{\prime}\) to \({\cal C}\) of total length at most \(3n-3\), which together with the edge \(({\cal C},{\cal C}^{\prime})\) gives a cycle of total length at most \(3n-1\leq 3n\). Because \(({\cal C},{\cal C}^{\prime})\) has length at least \(1\), it makes up a \(\frac{1}{3n}\) fraction of the cycle's length. (With a little more care, this bound can be easily improved to \(\frac{1}{2n}\).) \(\blacksquare\)

\(G_{\rm UC}\) is directed, and (as mentioned in the proof of Lemma 4.1) every edge makes up at least a \(\frac{1}{3n}\) fraction of the total length of at least one cycle it participates in. Hence, Proposition 2.1 gives an upper bound of \(\frac{3n-1}{3n}\) on the value of \(\beta\) in each iteration. A more careful analysis exploiting the specific structure of \(G_{\rm UC}\) gives us the following:

**Lemma 4.2**: _In \(G_{\mbox{\it UC}}\), for every non-negative node weight function \(\mu\), there exists a clustering \({\cal C}\) with \(\Phi_{\mu}({\cal C})\leq\frac{1}{2}\)._

**Proof.** Without loss of generality, assume that \(\mu\) is normalized, so that \(\sum\limits_{s}\mu(s)=1\). We describe an explicit greedy procedure for finding a clustering \({\cal C}\), similar to a procedure employed by Awasthi and Zadeh [5]. Start with a clustering into singleton sets, i.e., \({\cal C}=\{\{v\}\mid v\mbox{ is an item}\}\). Repeatedlylook for two clusters \(C,C^{\prime}\in{\cal C}\) such that the total likelihood of all the clusterings that group all of \(C\cup C^{\prime}\) in one cluster is strictly more than \(\frac{1}{2}\). As long as such \(C,C^{\prime}\) exist, merge them into a new cluster, and continue with the new clustering. The procedure terminates with some clustering \({\cal C}\) for which no pair of clusters can be further merged. We will show that \(\Phi_{\mu}({\cal C})\leq\frac{1}{2}\), by considering all clusterings \({\cal C}^{\prime}\) adjacent to \({\cal C}\):

* If \({\cal C}^{\prime}\) is obtained by merging two clusters \(C,C^{\prime}\in{\cal C}\), then by the termination condition, \(\mu(N({\cal C},{\cal C}^{\prime}))\leq\frac{1}{2}\); otherwise, \(C\) and \(C^{\prime}\) would have been merged.
* If \({\cal C}^{\prime}\) is obtained by splitting a cluster \(C\in{\cal C}\), then we first notice that \(C\) cannot be a singleton cluster. Therefore, it was created by merging two other clusters at some point earlier in the greedy process. By the merge condition, the total weight of the clusterings \({\cal C}^{\prime\prime}\) that have all of \(C\) in the same cluster is strictly more than \(\frac{1}{2}\). Therefore, the total weight of all clusterings \({\cal C}^{\prime\prime}\) that prefer _any_ partitioning of \(C\) is less than \(\frac{1}{2}\). This implies \(\mu(N({\cal C},{\cal C}^{\prime}))\leq\frac{1}{2}\) in the Split case as well. \(\blacksquare\)

In the absence of noise in the feedback, Lemmas 4.1 and 4.2 and Theorem 2.2 imply an algorithm that finds the true clustering using \(\log N=\log B(n)=\Theta(n\log n)\) queries. Notice that this is worse than the "trivial" algorithm, which starts with each node as a singleton cluster and always executes the merge proposed by the user, until it has found the correct clustering; hence, this bound is itself rather trivial.

Non-trivial bounds can be obtained when clusters belong to a restricted set, an approach also followed by Awasthi and Zadeh [5]. If there are at most \(M\) candidate clusters, then the number of clusterings is \(N_{0}\leq M^{k}\). For example, if there is a set system \({\cal F}\) of VC dimension at most \(d\) such that each cluster is in the range space of \({\cal F}\), then \(M=O(n^{d})\) by the Sauer-Shelah Lemma [20, 21]. Combining Lemmas 4.1 and 4.2 with Theorems 2.2 and 2.4, we obtain the existence of learning algorithms with the following properties:

**Corollary 4.3**: _Assume that in response to each equivalence query, the user responds with Merge or Split. Also, assume that there are at most \(M\) different candidate clusters, and the clustering has (at most) \(k\) clusters._

1. _If all query responses are correct, then the target clustering can be learned by an interactive algorithm using at most_ \(\log N=O(k\log M)\) _equivalence queries. Specifically when_ \(M=O(n^{d})\)_, this bound is_ \(O(kd\log n)\)_. This result recovers the main result of_ _[_5_]__._9__ Footnote 9: In fact, the algorithm in [5] is implicitly computing and querying a node with small \(\Phi\) in this directed graph.
2. _If query responses are correct with probability_ \(p>\frac{1}{2}\)_, the target clustering can be learned with probability at least_ \(1-\delta\) _by an interactive algorithm using at most_ \(\frac{(1-\delta)k\log M}{1-H(p)}+o(k\log M)+O(\log^{2}(1/\delta))\) _equivalence queries in expectation. Our framework provides the noise tolerance "for free;"_ _[_5_]_ _instead obtain results for a different type of noise in the feedback._

### Interactive Clustering with Given Cluster Splits

We now also consider a model in which the user specifies exactly _how_ to split a cluster when proposing a split. The operation Split\((C_{i},C^{\prime},C^{\prime\prime})\) specifies that the cluster \(C_{i}\) should be split into \(C^{\prime}\) and \(C^{\prime\prime}\), and thereby implies that none of the items in \(C^{\prime}\) should be clustered with any item in \(C^{\prime\prime}\). (Naturally, \(C^{\prime}\) and \(C^{\prime\prime}\) must be disjoint, and their union must be \(C_{i}\).) We require the same assumptions as for the model of "unspecified splits," and the bounds we obtain are the same.

Hence, the results in this model are weaker than those for the "unspecified splits" model. We are including them because we believe them to be a clean and natural application of the interactive learning framework.

We define an undirected weighted graph \(G_{\text{GC}}\), again containing a node for each clustering \(\mathcal{C}\). There is an (undirected) edge between two clusterings \(\mathcal{C},\mathcal{C}^{\prime}\) if and only if there exist clusters \(C_{i}\in\mathcal{C},C^{\prime}_{j},C^{\prime}_{j^{\prime}}\in\mathcal{C}^{\prime}\) with \(\mathcal{C}^{\prime}=\mathcal{C}\setminus\{C_{i}\}\cup\{C^{\prime}_{j},C^{ \prime}_{j^{\prime}}\}\), i.e., \(\mathcal{C}^{\prime}\) is obtained from \(\mathcal{C}\) by splitting \(C_{i}\) into \(C^{\prime}_{j}\) and \(C^{\prime}_{j^{\prime}}\). The length of the edge \((\mathcal{C},\mathcal{C}^{\prime})\) is \(\omega_{(\mathcal{C},\mathcal{C}^{\prime})}=2|C^{\prime}_{j}|\cdot|C^{\prime}_ {j}|\).

**Lemma 4.4**: \(G_{\text{GC}}\) _satisfies Definition 2.1 with respect to Merge and Split\((C_{i},C^{\prime},C^{\prime\prime})\) feedback._

Proof.Corresponding to each clustering \(\mathcal{C}\), we define an \(n\times n\) adjacency matrix \(\mathcal{A}^{(\mathcal{C})}\) with \(\mathcal{A}^{(\mathcal{C})}_{i,j}=1\) if items \(i\) and \(j\) are in the same cluster in \(\mathcal{C}\), and \(\mathcal{A}^{(\mathcal{C})}_{i,j}=0\), otherwise. (By definition, \(\mathcal{A}^{(\mathcal{C})}_{i,i}=1\) for every item \(i\).) For two clusterings \(\mathcal{C}\) and \(\mathcal{C}^{\prime}\), define their distance \(d(\mathcal{C},\mathcal{C}^{\prime})\) to be the Hamming distance of their adjacency matrices \(\mathcal{A}^{(\mathcal{C})}\) and \(\mathcal{A}^{(\mathcal{C}^{\prime})}\), i.e., the total number of bits in which their adjacency matrices differ.

If there is an edge in \(G_{\text{GC}}\) between \(\mathcal{C}\) and \(\mathcal{C}^{\prime}\), then \(\mathcal{C}\) and \(\mathcal{C}^{\prime}\) will differ by exactly one cluster being split into two (or two clusters being merged into one). Let \(C,C^{\prime}\) be the two merged clusters (or the clusters resulting from the split). The merge/split changes exactly \(2|C|\cdot|C^{\prime}|\) bits in the adjacency matrix, and the length assigned to the edge \((\mathcal{C},\mathcal{C}^{\prime})\) is exactly \(\omega_{(\mathcal{C},\mathcal{C}^{\prime})}=2|C|\cdot|C^{\prime}|=d(\mathcal{ C},\mathcal{C}^{\prime})\).

We now show that for each pair \(\mathcal{C}\), \(\mathcal{C}^{\prime}\), there is a path in \(G_{\text{GC}}\) of total edge length exactly equal to \(d(\mathcal{C},\mathcal{C}^{\prime})\). We show this by induction on \(d(\mathcal{C},\mathcal{C}^{\prime})\), the base case \(d(\mathcal{C},\mathcal{C}^{\prime})=0\) being trivial because \(\mathcal{C}=\mathcal{C}^{\prime}\). Suppose that \(\mathcal{C}\neq\mathcal{C}^{\prime}\). Then, there exist10\(C\in\mathcal{C},C^{\prime}_{1},C^{\prime}_{2}\in\mathcal{C}^{\prime}\) such that \(C\cap C^{\prime}_{1}\neq\emptyset\) and \(C\cap C^{\prime}_{2}\neq\emptyset\). Consider the move Split\((C,C\cap C^{\prime}_{1},C\setminus C^{\prime}_{1})\). Call the resulting clustering \(\mathcal{C}^{\prime\prime}\). Its adjacency matrix has \(\mathcal{A}^{(\mathcal{C}^{\prime\prime})}_{i,j}=0=\mathcal{A}^{(\mathcal{C}^ {\prime})}_{i,j}\) for all \(i\in C\cap C^{\prime}_{1},j\in C\setminus C^{\prime}_{1}\) and \(i\in C\setminus C^{\prime}_{1},j\in C\cap C^{\prime}_{1}\), while \(\mathcal{A}^{(\mathcal{C})}_{i,j}=1\) for all \(i,j\in C\). Thus,

Footnote 10: Technically, one might have to switch the roles of \(\mathcal{C}\) and \(\mathcal{C}^{\prime}\) for this to be true.

\[d(\mathcal{C},\mathcal{C}^{\prime})=\ d(\mathcal{C}^{\prime\prime},\mathcal{C }^{\prime})+2|C\cap C^{\prime}_{1}|\cdot|C\cap C^{\prime}_{2}|\ =\ d(\mathcal{C}^{ \prime\prime},\mathcal{C}^{\prime})+\omega_{(\mathcal{C},\mathcal{C}^{\prime \prime})}.\]

By induction hypothesis, there is a path of total length \(d(\mathcal{C}^{\prime\prime},\mathcal{C}^{\prime})\) from \(\mathcal{C}^{\prime\prime}\) to \(\mathcal{C}^{\prime}\) in \(G_{\text{GC}}\), which combined with the edge \((\mathcal{C},\mathcal{C}^{\prime\prime})\) gives the desired path from \(\mathcal{C}\) to \(\mathcal{C}^{\prime}\), completing the inductive proof.

We can now show that when a user correctly proposes a move corresponding to an edge \((\mathcal{C},\mathcal{C}^{\prime})\), it indeed lies on a shortest path from \(\mathcal{C}\) to \(\mathcal{C}^{*}\). We consider two cases:

* The user proposes Merge\((C,C^{\prime})\). This means that all of \(C\) and \(C^{\prime}\) belong to one cluster in \(\mathcal{C}^{*}\); in particular, all matrix entries for \(i,j\in C\cup C^{\prime}\) are \(1\). In \(\mathcal{A}^{(\mathcal{C})}\), all entries for \(i,j\in C\) are \(1\), as are all entries for \(i,j\in C^{\prime}\); on the other hand, all entries \(\mathcal{A}^{(\mathcal{C})}_{i,j}\) for \(i\in C,j\in C^{\prime}\) or for \(i\in C^{\prime},j\in C\) are \(0\). After the Merge, all these entries are \(1\) as well, decreasing the Hamming distance by \(2|C|\cdot|C^{\prime}|\). Since this is the length of the edge \((\mathcal{C},\mathcal{C}^{\prime})\) as well, and there is a path from \(\mathcal{C}^{\prime}\) to \(\mathcal{C}^{*}\) with total length equal to their Hamming distance (the argument of the previous paragraph), \(\mathcal{C}^{\prime}\) indeed lies on a shortest path from \(\mathcal{C}\) to \(\mathcal{C}^{*}\).
* The user proposes Split\((C,C^{\prime},C^{\prime\prime})\). This means that no pair \(i\in C^{\prime},j\in C^{\prime\prime}\) belongs to the same cluster in \(\mathcal{C}^{*}\), whereas they are all grouped together in \(\mathcal{C}\), meaning that \(\mathcal{A}^{(\mathcal{C})}_{i,j}=1\) for all \(i,j\in C\). Thus, \(d(\mathcal{C}^{\prime},\mathcal{C}^{*})=d(\mathcal{C},\mathcal{C}^{*})-2|C^{ \prime}|\cdot|C^{\prime\prime}|=d(\mathcal{C},\mathcal{C}^{*})-\omega_{( \mathcal{C},\mathcal{C}^{\prime})}\). Again by the argument from the previous paragraph, there is a path of total length \(d(\mathcal{C}^{\prime},\mathcal{C}^{*})\) from \(\mathcal{C}^{\prime}\) to \(\mathcal{C}^{*}\), so \((\mathcal{C},\mathcal{C}^{\prime})\) indeed lies on a shortest path from \(\mathcal{C}\) to \(\mathcal{C}^{*}\).

As in the clustering model in Section 4, the obvious \(\log N=\log B(n)=\Theta(n\log n)\) bound on the number of queries can be improved when clusters belong to a restricted set of size at most \(M\), giving us the following result:

**Corollary 4.5**: _Assume that in response to each equivalence query, the user responds with Merge or \(\textsc{Split}(C_{i},C^{\prime},C^{\prime\prime})\). Also, assume that there are at most \(M\) different candidate clusters, and the clustering has \(k\) clusters._

1. _If all query responses are correct, then the target clustering can be learned by an interactive algorithm using at most_ \(O(k\log M)\) _equivalence queries. Specifically when_ \(M=O(n^{d})\)_, this bound is_ \(O(kd\log n)\)_._
2. _If query responses are correct with probability_ \(p>\frac{1}{2}\)_, the target clustering can be learned with probability at least_ \(1-\delta\) _by an interactive algorithm using at most_ \(\frac{(1-\delta)k\log M}{1-H(p)}+o(k\log M)+O(\log^{2}(1/\delta))\) _equivalence queries in expectation._

We saw earlier that a trivial algorithm in the weaker model achieved a bound of \(n-k\) queries. The situation is even more extreme with more informative feedback: if there are no errors in the feedback, a bound of \(k-1\) can actually be obtained by another trivial algorithm. The algorithm starts from a clustering of all items in one cluster, and repeatedly obtains feedback, which must provide a correct split of one cluster into two. While this algorithm uses significantly fewer queries, it is not clear how to generalize it to the case of incorrect feedback: in particular, repeating the same query multiple times to obtain higher assurance will not work, as there are many correct answers the algorithm could receive. Thus, the algorithm cannot rely on a majority vote.

## 5 Application III: Learning a Classifier

Learning a binary classifier is the original and prototypical application of the equivalence query model of Angluin [2], which has seen a large amount of follow-up work since (see, e.g., [17, 18]). Naturally, if no assumptions are made on the classifier, then \(n\) queries are necessary in the worst case. In general, applications therefore restrict the concept classes to smaller sets, such as assuming that they have bounded VC dimension. We use \(\mathcal{F}\) to denote the set of all possible concepts, and write \(M=|\mathcal{F}|\); when \(\mathcal{F}\) has VC dimension \(d\), the Sauer-Shelah Lemma [20, 21] implies that \(M=O(n^{d})\).

Learning a binary classifier for \(n\) points is an almost trivial application of our framework11. When the algorithm proposes a candidate classifier, the feedback it receives is a point with a corrected label (or the fact that the classifier was correct on all points).

Footnote 11: The results extend readily to learning a classifier with \(k\geq 2\) labels.

We define the graph \(G_{\mathrm{CL}}\) to be the \(n\)-dimensional hypercube12 with unweighted and undirected edges between every pair of nodes at Hamming distance \(1\). Because the distance between two classifiers \(C\), \(C^{\prime}\) is exactly the number of points on which they disagree, \(G_{\mathrm{CL}}\) satisfies Definition 2.1. Hence, we can apply Corollary 2.3 and Theorem 2.4 with \(S_{\mathrm{init}}\) equal to the set of all \(M\) candidate classifiers to obtain the following:

Footnote 12: When there are \(k\) labels, \(G_{\mathrm{CL}}\) is a graph with \(k^{n}\) nodes.

**Corollary 5.1**:
* _With perfect feedback, the target classifier is learned using_ \(\log M\) _queries_13_._ Footnote 13: With \(k\) labels, this bound becomes \((k-1)\log M\)._

* _When each query response is correct with probability_ \(p>\frac{1}{2}\)_, there is an algorithm learning the true binary classifier with probability at least_ \(1-\delta\) _using at most_ \(\frac{(1-\delta)\log M}{1-H(p)}+o(\log M)+O(\log^{2}(1/\delta))\) _queries in expectation._

Thus, we recover the classic result on learning a classifier in the equivalence query model when feedback is perfect and extend it to the noisy setting.

### Proper Learning of Hyperplanes

While the learning algorithm we described will always terminate with the correct classifier, and in particular one from \(\mathcal{F}\), as part of the learning process, it may propose classifiers outside of \(\mathcal{F}\), somewhat akin to improper learning. Angluin's original paper [2] already observed that when each query has to be in \(\mathcal{F}\), a large number of queries may be necessary even when \(\mathcal{F}\) has very small VC dimension: a particularly stark example is when \(\mathcal{F}\) consists of all singleton sets.

Since bounded VC dimension is not sufficient to ensure query-efficient proper learning in the equivalence query model, a large body of subsequent work (see, e.g., [18] for an overview) has focused on specific geometric classes such as hyperplanes or axis-aligned boxes. Here, we show that the results on learning hyperplanes in \(\mathbb{R}^{d}\) can be obtained directly in our framework. Let \(\mathcal{H}\) be the family of all subsets of the \(n\) points that are separable using a \(d\)-dimensional hyperplane. The key insight is:

**Lemma 5.2**: _For every weight function \(\mu:\mathcal{H}\rightarrow\mathbb{R}_{\geq 0}\) on linear classifiers, there exists a linear classifier \(C\in\mathcal{H}\) with \(\Phi_{\mu}(C)\leq\frac{d+1}{d+2}\)._

The key to the proof of Lemma 5.2 is the following generalization of Caratheodory's Theorem. We suspect that Lemma 5.3 must be known, but since we could not find a statement of it despite a long search, we provide a self-contained proof here.

**Lemma 5.3**: _Let \(P,Q\) be sets in \(\mathbb{R}^{d}\) whose convex hulls intersect. Then, there exist sets \(P^{\prime}\subseteq P,Q^{\prime}\subseteq Q\) with \(|P^{\prime}|+|Q^{\prime}|\leq d+2\) such that their convex hulls intersect._

Notice that Caratheodory's Theorem is the special case when \(|P|=1\). The lemma can also be easily generalized to points in the intersection of \(k\) sets, rather than just the special case \(k=2\).

Proof.The proof is quite similar to one of the standard proofs for Caratheodory's Theorem, and based on properties of basic feasible solutions of an LP.

First, to avoid notational inconvenience, we may assume w.l.o.g. that \(P\) and \(Q\) are finite; in fact, that \(|P|,|Q|\leq d+1\). This is due to Caratheodory's Theorem. Let \(x\in\operatorname{conv}(P)\cap\operatorname{conv}(Q)\). Then, because \(x\in\operatorname{conv}(P)\), there exists \(P^{\prime}\subseteq P\) of cardinality at most \(d+1\) such that \(x\in\operatorname{conv}(P^{\prime})\); similarly for \(Q\). Hence, we have exhibited subsets \(P^{\prime}\subseteq P,Q^{\prime}\subseteq Q\) of size at most \(d+1\) each, whose convex hulls intersect. For the remainder of the proof, we can therefore focus on \(P^{\prime},Q^{\prime}\), and will rename them to \(P,Q\).

Write \(P=\{p_{1},p_{2},\ldots,p_{d+1}\}\) and \(Q=\{q_{1},q_{2},\ldots,q_{d+1}\}\). A point \(x\) is in \(\operatorname{conv}(P)\) iff there exist \(\lambda_{1},\ldots,\lambda_{d+1}\geq 0\) with \(\sum_{i}\lambda_{i}=1\) such that \(x=\sum_{i}\lambda_{i}p_{i}\). Similarly, \(x\in\operatorname{conv}(Q)\) iff there exist \(\mu_{1},\ldots,\mu_{d+1}\geq 0\) with \(\sum_{j}\mu_{j}=1\) such that \(x=\sum_{j}\mu_{j}q_{j}\). We can therefore characterize the intersection \(\operatorname{conv}(P)\cap\operatorname{conv}(Q)\) using the following linear program with variables \(\lambda_{i},\mu_{j}\):\[\sum_{i}\lambda_{i}p_{i} =\sum_{j}\mu_{j}q_{j}\] \[\sum_{i}\lambda_{i} =1\] \[\sum_{j}\mu_{j} =1\] \[\lambda_{i} \geq 0\quad\text{ for all }i\] \[\mu_{j} \geq 0\quad\text{ for all }j.\]

Notice that the first "constraint" is actually \(d\) constraints, one for each dimension. Hence, the linear program has \(2d+2\) variables and \(3d+4\) constraints. By assumption, this LP has a feasible solution, so it must have a _basic_ feasible solution. A basic feasible solution is characterized by \(2d+2\) constraints that hold with equality. Therefore, at most \(d+2\) inequalities can be strict. The only inequalities in the LP are the non-negativity constraints, implying that at most \(d+2\) variables \(\lambda_{i},\mu_{j}\) can be strictly positive. Hence, there is a point in the intersection that can be written as a convex combination of points \(p_{i}\) and \(q_{j}\), using at most \(d+2\) points total.

Using Lemma 5.3, the proof of Lemma 5.2 is fairly straightforward.

Proof of Lemma 5.2.We will use the terms "linear classifier" and "hyperplane" interchangeably in the proof, using whichever term better emphasizes the concept we are illustrating at the time. W.l.o.g., we assume that the weights \(\mu\) assigned to linear classifiers are normalized so that they add up to \(1\).

For each linear classifier \(C\in\mathcal{H}\) and sample point \(x\), let \(C(x)\in\{0,1\}\) be the assigned binary label. Define \(\phi(x):=\sum_{C\in\mathcal{H}}\mu(C)\cdot C(x)\) as the weighted average label assigned to \(x\) by all classifiers. Define \(P:=\{x\mid\phi(x)<\frac{1}{d+2}\}\) and \(Q:=\{x\mid\phi(x)>1-\frac{1}{d+2}\}\).

We claim that the convex hulls of \(P\) and \(Q\) do not intersect. Suppose for contradiction that they did; then, by Lemma 5.3, there exist \(P^{\prime}\subseteq P,Q^{\prime}\subseteq Q\) with \(|P^{\prime}|+|Q^{\prime}|\leq d+2\) and \(x\in\operatorname{conv}(P^{\prime})\cap\operatorname{conv}(Q^{\prime})\). Write \(P^{\prime}=\{p_{1},\ldots,p_{k}\}\) and \(Q^{\prime}=\{q_{1},\ldots,q_{\ell}\}\) with \(k+\ell\leq d+2\). For each \(p_{i}\), let \(\mathcal{H}_{i}^{p}:=\{C\in\mathcal{H}\mid C(p_{i})=0\}\) be the set of all linear classifiers that assign label \(0\) to \(p_{i}\); similarly, the definition of \(P\) and \(Q\), \(\mu(\mathcal{H}_{i}^{p})>1-\frac{1}{d+2}\) for all \(i\), and \(\mu(\mathcal{H}_{j}^{q})>1-\frac{1}{d+2}\) for all \(j\), or, taking complements, \(\mu(\overline{\mathcal{H}_{i}^{p}})<\frac{1}{d+2}\) for all \(i\), and \(\mu(\overline{\mathcal{H}_{j}^{q}})<\frac{1}{d+2}\) for all \(j\). Because

\[\mu(\bigcup_{i}\overline{\mathcal{H}_{i}^{p}}\cup\bigcup_{j}\overline{ \mathcal{H}_{j}^{q}})\leq\sum_{i}\mu(\overline{\mathcal{H}_{i}^{p}})+\sum_{j} \mu(\overline{\mathcal{H}_{j}^{q}})\;<\;k\cdot\frac{1}{d+2}+\ell\cdot\frac{1} {d+2}\;<\;1,\]

there must exist at least one linear classifier \(C\in\bigcap_{i}\mathcal{H}_{i}^{p}\cap\bigcap_{j}\mathcal{H}_{j}^{q}\). Because \(C(p_{i})=0\) for all \(p_{i}\in P^{\prime}\), and \(x\in\operatorname{conv}(P^{\prime})\), we must have \(C(x)=0\). But because \(C(q_{j})=1\) for all \(q_{j}\in Q^{\prime}\), and \(x\in\operatorname{conv}(Q^{\prime})\), we must also have \(C(x)=1\). This is a contradiction, and we have proved that the convex hulls of \(P\) and \(Q\) are disjoint.

Because \(\operatorname{conv}(P)\cap\operatorname{conv}(Q)=\emptyset\), the Hyperplane Separation Theorem implies that there is a hyperplane \(C\) separating \(P\) and \(Q\). We will show that any such \(C\) (labeling every point in \(P\) with \(0\) every point in \(Q\) with \(1\)) satisfies the claim of the lemma; thereto, fix one arbitrarily. Consider any feedback that could be given to the algorithm; because the graph \(G_{\mathrm{CL}}\) is the \(n\)-dimensional hypercube, this feedback is in the form of a point \(x\) which \(C\) mislabels. We distinguish three cases for \(x\):* If \(x\in P\), then \(C(x)=0\). By definition of \(P\), the total weight of classifiers labeling \(x\) with \(0\) is more than \(1-\frac{1}{d+2}\), and all these classifiers are inconsistent with the feedback. Therefore, the total weight of all classifiers consistent with the feedback decreased by a factor \(d+2\), which is much stronger than the claim of the lemma.
* If \(x\in Q\), then \(C(x)=1\); apart from this, the proof is identical to the case \(x\in P\).
* If \(x\notin P\cup Q\), then either \(C(x)=0\) or \(C(x)=1\) are possible. The fractional label \(\phi(x)\in[\frac{1}{d+2},1-\frac{1}{d+2}]\) was inconclusive. But because \(\phi(x)\geq\frac{1}{d+2}\), at least a \(\frac{1}{d+2}\) (weighted) fraction of classifiers labeled \(x\) with \(1\); similarly, because \(\phi(x)\leq 1-\frac{1}{d+2}\), at least a \(\frac{1}{d+2}\) (weighted) fraction of classifiers labeled \(x\) with \(0\). Thus, whichever label \(C\) assigned to \(x\) and was corrected about, at least a \(\frac{1}{d+2}\) weighted fraction of classifiers are inconsistent with the feedback.

Thus, in each case, we obtain that the total weight of classifiers consistent with the feedback is at most a \(\max(\frac{1}{d+2},1-\frac{1}{d+2})=\frac{d+1}{d+2}\) fraction of the total weight, and the lemma follows. \(\blacksquare\)

Using Lemma 5.2, Theorem 2.2 with \(\beta=\frac{d+1}{d+2}\), and the fact that \(M\leq n^{d}\), we immediately recover Theorem 5 of [16] for binary classification:

**Corollary 5.4** (Theorem 5 of [16]): _In the absence of noise, a hyperplane can be properly learned using at most \(O(d\log_{\frac{d+2}{d+1}}n)=O(d^{2}\log n)\) equivalence queries._

As with the result for improper learning, we obtain a bound in the case of imperfect feedback by using Theorem 2.4 in place of Theorem 2.2.

## 6 Discussion and Conclusions

We defined a general framework for interactive learning from imperfect responses to equivalence queries, and presented a general algorithm that achieves a small number of queries. We then showed how query-efficient interactive learning algorithms in several domains can be derived with practically no effort as special cases; these include some previously known results (classification and clustering) as well as new results on ranking/ordering.

Our work raises several natural directions for future work. Perhaps most importantly, for which domains can the algorithms be made computationally efficient (in addition to query-efficient)? We provided a positive answer for ordering with perfect query responses, but the question is open for ordering when feedback is imperfect. For classification, when the possible clusters have VC dimension \(d\), the time is \(O(n^{d})\), which is unfortunately still impractical for real-world values of \(d\). Maass and Turan [16] show how to obtain better bounds specifically when the sample points form a \(d\)-dimensional grid; to the best of our knowledge, the question is open when the sample points are arbitrary. The Monte Carlo approach of Theorem 2.6 reduces the question to the question of sampling a uniformly random hyperplane, when the uniformity is over the _partition_ induced by the hyperplane (rather than some geometric representation). For clustering, even less appears to be known.

Another natural question is motivated by the discussion in Section 5 and its application to clustering. We saw that the number of queries can increase significantly in proper interactive learning, i.e., when the set of models that can be queried is restricted to those that are themselves candidates. When concepts were specifically defined as hyperplane partitions, the increase can be bounded by \(O(\log d)\). Can similar bounds be obtained for other concept classes? What happens in the case of clustering if each proposed clustering must only have clusters from the allowed set?Finally, we are assuming a uniform noise model. An alternative would be that the probability of an incorrect response depends on the type of response. In particular, false positives could be extremely likely, for instance, because the user did not try to classify a particular incorrectly labeled data point, or did not see an incorrect ordering of items far down in the ranking. Similarly, some wrong responses may be more likely than others; for example, a user proposing a merge of two clusters (or split of one) might be "roughly" correct, but miss out on a few points (the setting that [5, 4] studied). We believe that several of these extensions should be fairly straightforward to incorporate into the framework, and would mostly lead to additional complexity in notation and in the definition of various parameters. But a complete and principled treatment would be an interesting direction for future work.

## References

* [1] E. Agichtein, E. Brill, S. Dumais, and R. Ragno. Learning user interaction models for predicting web search result preferences. In _Proc. 29th Intl. Conf. on Research and Development in Information Retrieval (SIGIR)_, pages 3-10, 2006.
* [2] D. Angluin. Queries and concept learning. _Machine Learning_, 2:319-342, 1988.
* [3] D. Angluin. Computational learning theory: Survey and selected bibliography. In _Proc. 24th ACM Symp. on Theory of Computing_, pages 351-369, 1992.
* [4] P. Awasthi, M.-F. Balcan, and K. Voevodski. Local algorithms for interactive clustering. _Journal of Machine Learning Research_, 18:1-35, 2017.
* [5] P. Awasthi and R. B. Zadeh. Supervised clustering. In _Proc. 22nd Advances in Neural Information Processing Systems_, pages 91-99. 2010.
* [6] M.-F. Balcan and A. Blum. Clustering with interactive feedback. In _Proc. 19th Intl. Conf. on Algorithmic Learning Theory_, pages 316-328, 2008.
* [7] R. Bubley. _Randomized Algorithms: Approximation, Generation, and Counting_. 2001.
* [8] R. Bubley and M. Dyer. Faster random generation of linear extensions. _Discrete mathematics_, 201(1):81-88, 1999.
* [9] K. Crammer and Y. Singer. Pranking with ranking. In _Proc. 14th Advances in Neural Information Processing Systems_, pages 641-647, 2002.
* [10] E. Emamjomeh-Zadeh, D. Kempe, and V. Singhal. Deterministic and probabilistic binary search in graphs. In _Proc. 48th ACM Symp. on Theory of Computing_, pages 519-532, 2016.
* [11] M. Huber. Fast perfect sampling from linear extensions. _Discrete Mathematics_, 306(4):420-428, 2006.
* [12] T. Joachims. Optimizing search engines using clickthrough data. In _Proc. 8th Intl. Conf. on Knowledge Discovery and Data Mining_, pages 133-142, 2002.
* [13] R. M. Karp. Reducibility among combinatorial problems. In _Complexity of Computer Computations_, pages 85-103. 1972.

* [14] A. Karzanov and L. Khachiyan. On the conductance of order Markov chains. _Order_, 8(1):7-15, 1991.
* [15] N. Littlestone. Learning quickly when irrelevant attributes abound: A new linear-threshold algorithm. _Machine Learning_, 2:285-318, 1988.
* [16] W. Maass and G. Turan. On the complexity of learning from counterexamples and membership queries. In _Proc. 31st IEEE Symp. on Foundations of Computer Science_, pages 203-210, 1990.
* [17] W. Maass and G. Turan. Lower bound methods and separation results for on-line learning models. _Machine Learning_, 9(2):107-145, 1992.
* [18] W. Maass and G. Turan. Algorithms and lower bounds for on-line learning of geometrical concepts. _Machine Learning_, 14(3):251-269, 1994.
* [19] F. Radlinski and T. Joachims. Query chains: Learning to rank from implicit feedback. In _Proc. 11th Intl. Conf. on Knowledge Discovery and Data Mining_, pages 239-248, 2005.
* [20] N. Sauer. On the density of families of sets. _Journal of Combinatorial Theory, Series A_, 13(1):145-147, 1972.
* [21] S. Shelah. A combinatorial problem; stability and order for models and theories in infinitary languages. _Pacific Journal of Mathematics_, 41(1):247-261, 1972.
* [22] K. L. Wagstaff. _Intelligent Clustering with Instance-Level Constraints_. PhD thesis, 2002. 


