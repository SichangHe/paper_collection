# A General Framework For Robust Interactive Learning

Ehsan Emamjomeh-Zadeh∗ David Kempe†
October 17, 2017

## Abstract

We propose a general framework for interactively learning models, such as (binary or nonbinary) classifiers, orderings/rankings of items, or clusterings of **data points. Our framework is**
based on a generalization of Angluin's equivalence query model and Littlestone's online learning model: in each iteration, the algorithm proposes a model, and the user either accepts it or reveals a specific mistake in the proposal. The feedback is correct only with probability p > 12

(and adversarially incorrect with probability 1 − p**), i.e., the algorithm must be able to learn in**
the presence of arbitrary noise. The algorithm's goal is to learn the **ground truth model using** few iterations.

Our general framework is based on a graph representation of the **models and user feedback.**
To be able to learn efficiently, it is sufficient that there be a graph G **whose nodes are the**
models and (weighted) edges capture the user feedback, with the property that if s, s∗ **are the**
proposed and target models, respectively, then any (correct) user feedback s
′ **must lie on a**
shortest s-s
∗ path in G**. Under this one assumption, there is a natural algorithm reminiscent of**
the Multiplicative Weights Update algorithm, which will efficiently learn s
∗
**even in the presence**
of noise in the user's feedback.

From this general result, we rederive with barely any extra effort classic results on learning of classifiers and a recent result on interactive clustering; in addition, we easily obtain new interactive learning algorithms for ordering/ranking.

## 1 Introduction

With the pervasive reliance on machine learning systems across myriad application domains in the real world, these systems frequently need to be deployed **before they are fully trained. This**
is particularly true when the systems are supposed to learn a **specific user's (or a small group of**
users') personal and idiosyncratic preferences. As a result, we are seeing an increased practical interest in online and interactive learning across a variety of domains.

A second feature of the deployment of such systems "in the wild" is that the feedback the system receives is likely to be noisy. Not only may individual users give incorrect feedback, but even if they do not, the preferences - and hence feedback - across different users may vary. Thus, interactive learning algorithms deployed in real-world systems must be resilient to noisy feedback.

Since the seminal work of Angluin [2] and Littlestone [15], the paradigmatic application of (noisy)
interactive learning has been online learning of a binary classifier when the algorithm is provided with feedback on samples it had previously classified incorrectly. However, beyond (binary or other)
classifiers, there are many other models that must be frequently learned in an interactive manner.

Two particularly relevant examples are the following:
∗**Department of Computer Science, University of Southern California, emamjome@usc.edu**
†**Department of Computer Science, University of Southern California, dkempe@usc.edu**

1
- **Learning an ordering/ranking of items is a key part of personalized Web search or other**
information-retrieval systems (e.g., [12, 19]). The user is typically presented with an ordering of items, and from her clicks or lack thereof, an algorithm can infer items that are in the wrong order.

- **Interactively learning a clustering [6, 5, 4] is important in many application domains, such as**
interactively identifying communities in social networks **or partitioning an image into distinct** objects. The user will be shown a candidate clustering, and can express that two clusters should be merged, or a cluster should be split into two.

In all three examples - classification, ranking, and clustering - the interactive algorithm will propose a model 1**(a classifier, ranking, or clustering) as a solution. The user then provides —**
explicitly or implicitly - feedback on whether the model is correct or needs to be fixed/improved.

This feedback may be incorrect with some probability. Based **on the feedback, the algorithm will**
propose a new and possibly very different model, and the process repeats. This type of interaction is the natural generalization of Angluin's equivalence query model [2, 3]. It is worth noting that in contrast to active learning, in interactive learning (which is the focus of this work), the algorithm cannot "ask" direct questions; it can only propose a model and receive feedback in return. The algorithm should minimize the number of user interactions, **i.e., the number of times that the user** needs to propose fixes. A secondary goal is to make the algorithm's internal computations efficient as well.

The main contribution of this article is a general framework **for efficient interactive learning of**
models (even with noisy feedback), presented in detail in Section 2. We consider the set of all N
models as nodes of a positively weighted undirected or directed graph G**. The one key property** that G must satisfy is the following: (*) If s **is a proposed model, and the user (correctly) suggests**
changing it to s
′, then the graph must contain the edge (s, s′); furthermore, (s, s′**) must lie on a**
shortest path from s **to the target model** s
∗**(which is unknown to the algorithm).**
We show that this single property is enough to learn the target model s
∗ **using at most log** N
queries2to the user, in the absence of noise. When the feedback is correct with probability p > 12
,
the required number of queries gracefully deteriorates to O(log N); the constant depends on p**. We** emphasize that the assumption (*) is not an assumption on the **user. We do not assume that** the user somehow "knows" the graph G **and computes shortest paths in order to find a response.**
Rather, (*) states that G was correctly chosen to model the underlying domain, so that **correct**
answers by the user must in fact have the property (*). To illustrate the generality of our framework, we apply it to ordering, clustering, and classification:
1. For ordering/ranking, each permutation is a node in G**; one permutation is the unknown**
target. If the user can point out only adjacent **elements that are out of order, then** G is an adjacent transposition "Bubble Sort**" graph, which naturally has the property (*). If** the user can pick any element and suggest that it should precede an entire block of elements it currently follows, then we can instead use an "Insersion Sort**" graph; interestingly, to** ensure the property (*), this graph must be weighted. On the other hand, as we show in Section 3, if the user can propose two arbitrary elements that should be swapped, there is no graph G **with the property (*).**
1We avoid the use of the term "concept," as it typically refers **to a binary function, and is thus associated**
specifically with a classifier.

2 **Unless specified otherwise, all logarithms are base 2.**
Our framework directly leads to an interactive algorithm that will learn the correct ordering of n items in O(log(n!)) = O(n log n**) queries; we show that this bound is optimal under the**
equivalence query model.

2. For learning a clustering of n **items, the user can either propose merging two clusters, or**
splitting one cluster. In the interactive clustering model of [6, 5, 4], the user can specify **that** a particular cluster C **should be split, but does not give a specific split. We show in Section 4** that there is a weighted directed graph with the property (*); then, if each cluster is from a "small" concept class of size at most M **(such as having low VC-dimension), there is an** algorithm finding the true clustering in O(k log M) queries, where k **is number of the clusters**
(known ahead of time).

3. For binary classification, G is simply an n-dimensional hypercube (where n **is the number of**
sample points that are to be classified). As shown in Section 5, one immediately recovers a close variant of standard online learning algorithms within this framework. An extension to classification with more than two classes is very straightforward.

## 2 Learning Framework

We define a framework for query-efficient interactive learning of different types of models**. Some**
prototypical examples of models to be learned are rankings/orderings of items, (unlabeled) clusterings of graphs or data points, and (binary or non-binary) **classifiers. We denote the set of all**
candidate models (permutations, partitions, or functions from the hypercube to {0, 1}**) by Σ, and**
individual models3 by s, s′, s∗, etc. We write N = |Σ| **for the number of candidate models.**
We study interactive learning of such models in a natural generalization of the equivalence query model of Angluin [2, 3]. This model is equivalent to the more widely known online learning model of Littlestone [15], but more naturally fits the description **of user interactions we follow here. It** has also served as the foundation for the interactive clustering model of Balcan and Blum [6] and Awasthi et al. [5, 4].

In the interactive learning framework**, there is an unknown ground truth model** s
∗**to be learned.**
In each round, the learning algorithm proposes a model s **to the user. In response, with probability**
p > 12
, the user provides correct feedback. In the remaining case (i.e., with probability 1 − p**), the**
feedback is arbitrary**; in particular, it could be arbitrarily and deliberately misleading.**
Correct feedback is of the following form: if s = s
∗**, then the algorithm is told this fact in the**
form of a user response of s**. Otherwise, the user reveals a model** s
′ 6= s **that is "more similar"**
to s
∗than s **was. The exact nature of "more similar," as well as the possibly restricted set of**
suggestions s
′that the user can propose, depend on the application domain. **Indeed, the strength**
of our proposed framework is that it provides strong query complexity guarantees under minimal assumptions about the nature of the feedback; to employ the framework, one merely has to verify that the the following assumption holds.

Definition 2.1 (Graph Model for Feedback) Define a weighted graph G (directed or undirected) that contains one node for each model s ∈ Σ, and an edge (s, s′) **with arbitrary positive**
edge length ω(s,s′) > 0 **if the user is allowed to propose** s
′in response to s**. (Choosing the lengths**
of edges is an important part of using the framework.) G may contain additional edges not corresponding to any user feedback. The key property that G **must satisfy is the following: (*) If the**

3**When considering specific applications, we will switch to notation more in line with that used for the specific**
application.
algorithm proposes s **and the ground truth is** s
∗ 6= s**, then every correct user feedback** s
′**lies on a**
shortest path from s to s
∗in G with respect to the lengths ωe**. If there are multiple candidate nodes**
s
′, then there is no guarantee on which one the algorithm will be **given by the user.**

## 2.1 Algorithm And Guarantees

Our algorithms are direct reformulations and slight generalizations of algorithms recently proposed by Emamjomeh-Zadeh et al. [10], which itself was a significant generalization of the natural "Halving Algorithm" for learning a classifier (e.g., [15]). They studied the search problem as an abstract problem they termed "Binary Search in Graphs," without discussing any applications. Our main contribution here is the application of the abstract search **problem to a large variety of interactive** learning problems, and a framework that makes such applications easy. We begin with the simplest case p **= 1, i.e., when the algorithm only receives correct feedback.**
Algorithm 1 gives essentially best-possible general guarantees [10]. To state the algorithm and its guarantees, we need the notion of an approximate median node of the graph G**. First, we denote** by

$$N(s,s^{\prime}):=\begin{cases}\{s\}&\text{if}s^{\prime}=s\\ \{\hat{s}\mid s^{\prime}\text{lies on a shortest path from}s\text{to}\hat{s}\}&\text{if}s^{\prime}\neq s\end{cases}$$

the set of all models ˆs **that are consistent with a user feedback of** s
′to a model s**. In anticipation**
of the noisy case, we allow models to be weighted4, and denote the node weights or **likelihoods** by µ(s) ≥ 0. If feedback is not noisy (i.e., p **= 1), all the non-zero node weights are equal. For every**
subset of models S, we write µ(S) := Ps∈S µ(s) for the total node weight of the models in S**. Now,**
for every model s**, define**

$$\Phi_{\mu}(s):=\frac{1}{\mu(\Sigma)}\cdot\operatorname*{max}_{s^{\prime}\neq s,(s,s^{\prime})\in G}\mu(N(s,s^{\prime}))$$

to be the largest fraction (with respect to node weights) of models that could still be consistent with a worst-case response s
′to a proposed model of s. For every subset of models S**, we denote by**
µS the likelihood function that assigns weight 1 to every node s ∈ S **and 0 elsewhere. For simplicity**
of notation, we use ΦS(s**) when the node weights are** µS.

The simple key insight of [10] can be summarized and reformulated as the following proposition:
Proposition 2.1 ([10], Proofs of Theorems 3 and 14) Let G **be a (weighted) directed graph**
in which each edge e with length ωe is part of a cycle of total edge length at most c · ωe**. Then, for**
every node weight function µ, there exists a model s **such that** Φµ(s) ≤
c−1 c
.

When G is undirected (and hence c = 2), for every node weight function µ**, there exists an** s such that Φµ(s) ≤
1 2
.

Proof. For any pair s, s′ of models, let d(s, s′) denote their distance in G **with respect to the edge**
lengths ω. Fix a node weight function µ. Define Ψµ(s**) :=** Ps
′∈Σ
d(**s, s**′)µ(s
′**) as the total weighted**
distance from s **to every model** s
′. Let ˆs be a model that minimizes Ψµ(s). We prove that ˆs **satisfies**
the claim of Proposition 2.1.

Let e = (ˆs, s) be an edge in G. By definition, s lies on a shortest path from ˆs **to every model**
s
′ ∈ N(ˆs, s**). Therefore, for every** s
′ ∈ N(ˆs, s), we have d(s, s′) = d(ˆs, s′) − ωe**. On the other hand,**

4**Edge lengths are part of the definition of the graph, but node weights will be assigned by our algorithm; they**
basically correspond to likelihoods.
e belongs to a cycle of total length at most c · ωe**, so there is a path of total length no more than**
(c − 1) · ωe from s to ˆs**. Thus, for every** s
′ ∈/ N(ˆs, s), we have d(s, s′) ≤ d(ˆs, s′) + (c − 1) · ωe**. We**
can now bound Ψµ(s**) from above:**

$$\Psi_{\mu}(s)=\sum_{s^{\prime}\in\Sigma}\mu(s^{\prime})\cdot d(s,s^{\prime})$$ $$\leq\sum_{s^{\prime}\in N(\hat{s},s)}\mu(s^{\prime})\cdot(d(\hat{s},s^{\prime})-\omega_{e})+\sum_{s^{\prime}\notin N(\hat{s},s)}\mu(s^{\prime})\cdot(d(s,s^{\prime})+(c-1)\cdot\omega_{e})$$ $$=\Psi_{\mu}(\hat{s})-\omega_{e}\cdot\left(\sum_{s^{\prime}\in N(\hat{s},s)}\mu(s^{\prime})-(c-1)\cdot\sum_{s^{\prime}\notin N(\hat{s},s)}\mu(s^{\prime})\right).$$

By definition of ˆs, we have Ψµ(s) ≥ Ψµ(ˆs), so after dividing by ωe > **0, we get that** Ps
′∈N(ˆs,s) µ(s
′)−
(c−1)·Ps
′∈/N(ˆs,s) µ(s
′**) must be non-positive, implying that** Ps
′∈N(ˆs,s) µ(s
′) ≤ (c−1)·Ps
′∈/N(ˆs,s) µ(s
′).

This completes the proof.

In Algorithm 1, we always have uniform node weight for all the **models which are consistent**
with all the feedback received so far, and node weight 0 for models that are inconsistent with at least one response. Prior knowledge about candidates for s
∗**can be incorporated by providing the**
algorithm with the input Sinit ∋ s
∗**to focus its search on; in the absence of prior knowledge, the**
algorithm can be given Sinit **= Σ.**
Algorithm 1 **Learning a model without Feedback Errors** (Sinit)
1: S ← Sinit.

2: **while** |S| > 1 do 3: Let s **be a model with a "small" value of Φ**S(s).

4: Let s
′ **be the user's feedback model.**
5: Set S ← S ∩ N(**s, s**′).

6: return **the only remaining model in** S.

Line 3 is underspecified as "small." Typically, an algorithm would choose the s **with smallest**
ΦS(s**). But computational efficiency constraints or other restrictions (see Sections 2.2 and 5) may**
preclude this choice and force the algorithm to choose a suboptimal s**. The guarantee of Algorithm 1** is summarized by the following Theorem 2.2. It is a straightforward generalization of Theorems 3 and 14 from [10], but for completeness, we give a self-contained proof.

Theorem 2.2 Let N0 = |Sinit| be the number of initial candidate models. If each model s **chosen**
in Line 3 of Algorithm 1 has ΦS(s) ≤ β**, then Algorithm 1 finds** s
∗ using at most log1/β N0 **queries.**
Corollary 2.3 When G is undirected and the optimal s **is used in each iteration,** β =
1 2 and Algorithm 1 finds s
∗ using at most log2 N0 **queries.**
Proof of Theorem 2.2. Let S **be the set of models that are consistent with all the query responses so far. (Initially,** S = Sinit.) Let s be a model with ΦS(s) ≤ β**. If the algorithm proposes**
s to the user, the user's feedback will be consistent with at most a β **fraction of the models in** S**. Note that in Algorithm 1,** µ(s
′**) = 1 for every** s
′ ∈ S**. Given that the set of consistent models**
shrinks by at least a factor of β **in each round, it takes no more than log**1/β |Sinit| **rounds to get it**
down to a single model (which must then be the target).

Next, we present the algorithm in the case of probabilistically incorrect feedback. It is a close adaptation of an algorithm by Emamjomeh-Zadeh et al. [10], which resembles a multiplicativeweights update algorithm. It keeps track of node weights µ(s**) for each model, which now exactly**
correspond to likelihoods of the observed responses, given that s **is the target. Hence, instead of**
the generic name "node weight," we will refer to them as likelihoods.

In order to achieve an information-theoretically optimal dependence on p**, [10] run the algorithm**
in several stages, removing very likely **nodes from consideration for later inspection. Here, however,**
we slightly modify (in fact, simplify) the algorithm by not removing the likely nodes during the execution. This modification is crucial to make the algorithm efficiently implementable using a sampling oracle, as discussed in Section 2.2. The key "multiplicative weights" loop is reformulated and slightly generalized by Algorithm 2.

Algorithm 2 **Multiplicative-Weights (**Sinit, K)
1: Set µ(v) ← **1 for all models** s ∈ Sinit and µ(s) ← 0 for all models s /∈ Sinit.

2: Set M ← ∅.

3: for K **+ 1 iterations** do 4: if there exists a model s **with** µ(s) ≥
1 2 µ(Sinit) **then**
5: Mark s, by setting M ← M ∪ {s}.

6: Let s **be a model with "small" Φ**µ(s).

7: Query model s**, receiving feedback** s
′.

8: for all **models ˆ**s ∈ Sinit do 9: if sˆ ∈ N(s, s′) **then**
10: µ(ˆs) ← p · µ(ˆs).

11: **else** 12: µ(ˆs) ← (1 − p) · µ(ˆs). 13: **return** M
Algorithm 2 is invoked several times in Algorithm 3. Algorithm 3 is given an initial candidate model set Sinit, and also a threshold 0 < τ < **1 (to be specified later), as well as a target error**
probability δ**. The algorithm must output** s
∗**(the target model) with probability at least 1** − δ, assuming that s
∗ ∈ Sinit**. The exact constants used are chosen to achieve an optimal dependency of**
the number of queries on p in the worst case over graphs [10]. Here and below, H(p) = −p log p −
(1 − p) log(1 − p**) denotes the entropy.**
The performance of Algorithm 3 is summarized in Theorem 2.4, **which generalizes the results**
of [10] to arbitrary values of β.

Theorem 2.4 Let β ∈ [
1 2
, 1), define τ = βp + (1 − β)(1 − p), and let N0 = |Sinit|**. Assume that**
log(1/τ ) > H(p) where H(p) = −p log p − (1 − p) log(1 − p) **denotes the entropy. (When** β =
1 2
,
this holds for every p > 12
.)
If each model s chosen in Line 6 of Algorithm 2 has Φµ(s) ≤ β**, then with probability at least**
1 − δ**, Algorithm 3 finds** s
∗ **using at most** (1−δ)
log(1/τ)−H(p)
log N0 + o(log N0) + O(log2(1/δ)) **queries in**
expectation.

Corollary 2.5 When the graph G is undirected and the optimal s **is used in each iteration, then**
with probability at least 1 − δ**, Algorithm 3 finds** s
∗ **using at most** (1−δ)
1−H(p)
log2 N0 + o(log N0) +
O(log2(1/δ)) **queries in expectation.**
Algorithm 3 **Online Learning of a model with Imperfect Feedback** (Sinit**, τ, δ**)
1: δ
′ ← δ/5.

2: Fix λ1 **= max**{
q 1 log log |S**init**|
,
log(1/τ)−H(p)
2 log(p/(1−p)) }.

3: K1 ← max{log |S**init**| log(1/τ)−H(p)−λ1 log(p/(1−p)) +
log(1/τ)
log(1/δ′)
,
ln(1/δ′)
λ 2 1
} **+ 1.**
4: S1 ← Multiplicative-Weights(**V, K**1). 5: Fix λ2 =
log(1/τ)−H(p)
2 log(p/(1−p)) .

6: K2 ← max{log(|S1|)
log(1/τ)−H(p)−λ2 log(p/(1−p)) +
log(1/τ)
log(1/δ′)
,
ln(1/δ′)
λ 2 2
} **+ 1.**
7: S2 ← Multiplicative-Weights(S1, K2).

8: **for all** s ∈ S2 do 9: Query s **repeatedly** 2 ln(|S2|/δ′)
(2p−1)2 **times.**
10: if s is returned as the correct model for at least half of these queries **then** 11: **return** s.

12: return **failure.**
Proof of Theorem 2.4. **The proof of this theorem is fairly similar to the proof of Lemma 7 in**
[10]. Here, we give a high-level outline of that proof, and specify the changes that need to be made for our slightly more general setting, as well as the modification we made in Algorithm 2.

Let s **be the model in Line 6 of Algorithm 2. If it has** µ(s) ≤
1 2 µ(Sinit**), whatever the query**
response is, at most a β fraction of the total likelihood is multiplied by p**, while the rest is multiplied** by 1 − p. Therefore, the total likelihood decreases by at least a factor of τ = βp + (1 − β)(1 − p).

Furthermore, if µ(s) >
1 2 µ(Sinit) and s **is not the target, we show that in expectation, the total**
likelihood decreases by at least a factor 12
. This is because with probability at most 1−p**, the query**
response claims that s is the target in which case µ(s) is multiplied by p**, while all other nodes'**
likelihoods are multiplied by 1 − p. In the remaining cases, i.e., if the response is correct, or **it is**
incorrect but pointing to a neighbor of s, µ(s) is multiplied by 1 − p**. Hence, in expectation, the** total likelihood decreases by a factor of

$$(1-p)\cdot\left(p\cdot\mu(s)+(1-p)\cdot(\mu(S_{\rm init})-\mu(s))\right)+p\cdot\left((1-p)\mu(s)+p\cdot(\mu(S_{\rm init})-\mu(s))\right)$$ $$\leq\frac{1}{2}\mu(S_{\rm init})\leq\tau\mu(S_{\rm init}).$$

To summarize, in expectation, the total likelihood decreases by at least a factor τ **in both cases.**
Initially, in Algorithm 2, the total likelihood of all models is |Sinit|**, and in each iteration, the**
total likelihood decreases at least by a factor of τ , in expectation. By induction, after K **rounds,**
the expected total likelihood is bounded by |Sinit| · τ K**. On the other hand, in expectation, a** p fraction of the query responses is correct. Using tail bounds, for a carefully chosen value of λ (as in Algorithm 3, Lines 2 and 5), with "high enough" probability, a p − λ **fraction of the responses**
are correct. Whenever a p − λ **fraction of the responses is correct, the likelihood** µ(s
∗**) of the target**
model s
∗**is at least (**p p−λ· (1 − p)
1−p+λ)
K.

Because the statement of the theorem assumed that log(1/τ ) > H(p) = −p log p − (1 −
p) log(1 − p), or, equivalently, **τ < p**p(1 − p)
1−p, µ(s
∗**) decreases exponentially slower than the**
total likelihood of all the models; hence, s
∗ **must eventually get marked by Algorithm 2 with high**
probability.

In fact, K1 and K2 **are chosen such that this marking of** s
∗ **happens with sufficiently high**
probability within that many rounds. The precise calculations are quite similar to those in [10], but slightly more messy. [10] showed that if the first time that Algorithm 2 is invoked by Algorithm 3, it is executed for (roughly) log N
1−H(p)
iterations, then with high probability, s
∗**is marked. This analysis**
can be straightforwardly generalized to our setting, when running for log N
log(1/τ)−H(p)
rounds. The proof for the other stages of Algorithm 3 remains almost the same.

## 2.2 Computational Considerations And Sampling

Corollaries 2.3 and 2.5 require the algorithm to find a model s with small Φµ(s**) in each iteration. In**
most learning applications, the number N **of candidate models is exponential in a natural problem** parameter n, such as the number of sample points (classification), or the **number of items to rank**
or cluster. If computational efficiency is a concern, this precludes explicitly keeping track of the set S or the weights µ(s). It also rules out determining the model s **to query by exhaustive search** over all models that have not yet been eliminated.

In some cases, these difficulties can be circumvented by exploiting problem-specific structure.

A more general approach relies on Monte Carlo techniques. We **show that the ability to sample**
models s with probability (approximately) proportional to µ(s**) (or approximately uniformly from** S **in the case of Algorithm 1) is sufficient to essentially achieve the results of Corollaries 2.3 and**
2.5 with a computationally efficient algorithm. Notice that in both Algorithms 1 and 2, µ(s**) is**
completely determined by all the query responses the algorithm has seen so far and the probability p. Theorem 2.6 Let n be a natural measure of the input size and assume that log N **is polynomial**
in n. Assume that G = (V, E) is undirected5**, all edge lengths are integers, and the maximum**
degree and diameter (both with respect to the edge lengths) are bounded by poly(n)**. Also assume**
w.l.o.g. that µ is normalized to be a distribution over the nodes6(i.e., µ(Σ) **= 1).**
Let 0 ≤ ∆ < 14 be a constant, and assume that there is an oracle that - given a **set of query**
responses - runs in polynomial time in n and returns a model s **drawn from a distribution** µ
′
with dTV(µ, µ′) ≤ ∆**. Also assume that there is a polynomial-time algorithm that, given a model** s, decides whether or not s **is consistent with every given query response or not.**
Then, for every ǫ > 0**, in time poly**(n, 1 ǫ
), an algorithm can find a model s **with** Φµ(s) ≤
1 2**+2∆+**ǫ, with high probability. Therefore, Algorithms 1 and 3 with β =
1 2 + 2∆ + ǫ **(for a sufficiently small**
ǫ**) can be implemented to run in time poly**(n, 1 ǫ
).

Proof. The high-level idea is to use a simple local search algorithm to find a model s **with small**
Φµ(s). In order to execute the updating step, we need to estimate µ(N(s, s′**)) for all neighbors** s
′
of s in G. The key insight here is that µ(N(s, s′**)) is exactly the probability that a node drawn**
from µ **is consistent with the feedback** s
′ when s **is queried. To get a sharp enough estimate of**
µ(N(s, s′**)), in each iteration, enough samples are drawn to ensure that tail bounds kick in and**
provide high-probability guarantees. The high-level algorithm is given as Algorithm 4; details - in particular on Line 5 - are provided below.
In Line 5 of Algorithm 4, Ps,s′ is estimated as the fraction of samples ˆs **drawn from** µ
′**that are**
in N(s, s′**). Below, for a particular desired high-probability guarantee, we choose the number of**
samples to guarantee that
$$|P_{s,s^{\prime}}-\mu(N(s,s^{\prime}))|\leq\Delta+\epsilon^{\prime}$$
′(1)
with high probability. For most of the proof, we will assume that all of these high-probability events occurred; at the end, we will calculate the probability of this happening.

5**It is actually sufficient that for every node weight function** µ : V → R
+, there exists a model s **with Φ**µ(s) ≤
1 2
.

6For Algorithm 1, µ is uniform over all models consistent with all feedback up to **that point.**

$\left(1\right)$. 
Algorithm 4 Finding a good approximate median (∆, ǫ)
1: Let ǫ
′ = ǫ/3.

2: Let s **be an arbitrary model.** 3: **loop**
4: for each edge e = (**s, s**′) do 5: Let Ps,s′ be the empirical estimation of µ(N(s, s′)).

6: if Ps,s′ ≤
1 2 **+ ∆ + 2**ǫ
′for every edge e = (s, s′) **then**
7: **return** s. 8: **else**
9: Let e = (s, s′) be an edge out of s with Ps,s′ >
1 2 **+ ∆ + 2**ǫ
′.

10: Set s ← s
′.

Whenever an edge e = (s, s′) has Ps,s′ ≤ 12 **+∆+ 2**ǫ
′, we can bound µ(N(s, s′)) ≤ 12 **+ 2∆+ 3**ǫ
′ =
1 2 + 2∆ + ǫ. Thus, whenever Algorithm 4 returns a model s, the model satisfies Φµ(s) ≤ 12 **+ 2∆ +** ǫ.

It remains to show that the algorithm terminates, and in a polynomial number of iterations.

Define Ψµ(s) = Ps
′ µ(s
′)d(s, s′**) to be the weighted distance (with respect to the edge lengths** ωe)
from s **to all other models. When Algorithm 4 switches from** s to s
′**in Line 10, by Inequality (1),**
we have µ(N(**s, s**′)) ≥
1 2 **+∆ + 2**ǫ
′−**(∆ +**ǫ
′) = 12 +ǫ
′**, so Ψ**µ(s
′) ≤ Ψµ(s)−2ǫ
′·ωe**. Because the value**
of Ψµ(s) for all s is bounded by the diameter of G**, which was assumed to be bounded by poly(**n),
and the edge lengths are all positive integers, Algorithm 4 terminates after poly(n, 1/ǫ**) steps.**
The only remaining part is to compute how many samples from the oracle are required to guarantee Inequality (1) with high enough probability. Drawing r **samples, by standard tail bounds,**
Inequality (1) fails with probability no more than e
−Ω(ǫ 2r)**. Because all degrees are bounded by**
poly(n), Line 5 of Algorithm 4 is executed only poly(n, 1/ǫ**) times, so it suffices to draw** r =
poly( 1 ǫ
, log n**) samples in each iteration in order to apply a union bound over all iterations of the**
algorithm.

## 3 Application I: Learning A Ranking

As a first application, we consider the task of learning the correct order of n **elements with supervision in the form of equivalence queries. This task is directly motivated by learning a user's**
preference over web search results (e.g., [12, 19]), restaurant or movie orders (e.g., [9]), or many other types of entities. Using pairwise active **queries ("Do you think that A should be ranked ahead** of B?"), a learning algorithm could of course simulate standard O(n log n**) sorting algorithms; this**
number of queries is necessary and sufficient. However, when using equivalence queries, the user must be presented with a complete ordering (i.e., a permutation π of the n **elements), and the** feedback will be a mistake **in the proposed permutation. Here, we propose interactive algorithms**
for learning the correct ranking without additional information or assumptions.7 **We first describe**
results for a setting with simple feedback in the form of adjacent transpositions; we then show a generalization to more realistic feedback as one is wont to receive in applications such as search engines.

7**For example, [12, 19, 9] map items to feature vectors and assume linearity of the target function(s).**

## 3.1 Adjacent Transpositions

We first consider "Bubble Sort**" feedback of the following form: the user specifies that elements**
i and i + 1 in the proposed permutation π **are in the wrong relative order. An obvious correction**
for an algorithm would be to swap the two elements, and leave the rest of π **intact. This algorithm**
would exactly implement Bubble Sort**, and thus require Θ(**n 2**) equivalence queries. Our general**
framework allows us to easily obtain an algorithm with O(n log n**) equivalence queries instead. We**
define the undirected and unweighted graph GBS **as follows:**
- GBS contains N = n! nodes, one for each permutation π of the n **elements;**
- it contains an edge between π and π
′**if and only if** π
′can be obtained from π **by swapping**
two adjacent elements.

Lemma 3.1 GBS satisfies Definition 2.1 with respect to Bubble Sort **feedback.**
Proof. By definition, there is one node for each permutation, and the edges of GBS **exactly**
capture the possible feedback provided in response to the query. For two permutations π, π∗**, let**
τ (π, π∗) = |{(i, j) | i precedes j in π **and follows** j in π
∗}| denote the Kendall τ **distance. Since an**
adjacent transposition can fix the ordering of exactly one pair (i, j), the distance between **π, π**∗in GBS is exactly equal to τ (π, π∗**). If the user proposes** π
′in response to π**, then** π
′ **must fix exactly**
one inversion between π and π
∗**, so the distance between** π
′ and π
∗is τ (π
′, π∗) = τ (π, π∗)−**1. Thus,**
π
′**lies on a shortest path from** π to π
∗.

Hence, applying Corollary 2.3 and Theorem 2.4, we immediately obtain the existence of learning algorithms with the following properties: Corollary 3.2 Assume that in response to each equivalence query on a permutation π**, the user**
responds with an adjacent transposition (or states that the proposed permutation π **is correct).**
1. If all query responses are correct, then the target ordering can be learned by an interactive algorithm using at most log N = log n! ≤ n log n **equivalence queries.**
2. If query responses are correct with probability p > 12
, the target ordering can be learned by an interactive algorithm with probability at least 1 − δ **using at most** (1−δ)
1−H(p)
n log n + o(n log n) +
O(log2(1/δ)) **equivalence queries in expectation.**
Up to constants, the bound of Corollary 3.2 is optimal: Theorem 3.3 shows that Ω(n log n)
equivalence queries are necessary in the worst case. Notice **that Theorem 3.3 does not immediately**
follow from the classical lower bound for sorting with pairwise comparisons: while the result of a pairwise comparison always reveals one bit, there are n − **1 different possible responses to an** equivalence query, so up to O(log n**) bits might be revealed. For this reason, the proof of Theorem 3.3** explicitly constructs an adaptive adversary, and does not rely on a simple counting argument. Theorem 3.3 **With adversarial responses, any interactive ranking algorithm can be forced to ask** Ω(n log n) equivalence queries. This is true even if the true ordering is **chosen uniformly at random,**
and only the query responses are adversarial.

Proof. Let A **be an arbitrary interactive algorithm which learns the underlying order. In each**
round, A proposes a permutation π **and receives feedback in the form of an adjacent transposition.**
We start with the case when both the correct ordering and the responses are adversarial. We define an adaptive adversary B which forces A to take Ω(n log n**) rounds before it finds the correct**
ordering π
∗.

The adversary B gradually marks elements as '+' or '−**', trying to delay labeling for as long as**
possible. Initially, all n elements are unmarked. When A proposes a permutation π, B **looks for**
two consecutive elements i = πk, j = πk+1 in π **which are both unmarked. If such a pair exists,** B
returns (k, k + 1) as feedback, i.e., it tells the algorithm that i and j **are in the wrong order. Then,**
it marks i with '+' and j with '−'. Because B **marks exactly two new elements in each round,**
and any permutation with fewer than ⌊n/2⌋ **marked elements must have two consecutive marked**
elements, B **can keep following this strategy for at least** n 4
**rounds.**
At this point, the algorithm starts its second stage. It partitions the elements into two sets: L−
and L+**. The partition satisfies the following conditions:**
- All elements marked with '−' are in L−**, and all elements marked with '+' are in** L+.

- Elements are partitioned as evenly as possible: |L−| ≥ n 2 and |L+| ≥ n 2
.

Notice that such a partition always exists, because the number of elements marked '+' and '−**' are**
the same. B **commits to the fact that in** π
∗, all elements of L− **will precede all elements of** L+,
but leaves π
∗ unspecified beyond that. Notice that A **has not received any feedback on the relative**
ordering of any pair of elements in L− or any pair in L+. In the subsequent rounds, B **responds as**
follows:
- If A proposes a permutation π in which an element j ∈ L− **appears after an element** i ∈ L+,
then π must contain an adjacent such pair (i, j). In that case, B **provides the feedback that**
(i, j) are out of order. In fact, this provides A with no new information beyond L− and L+,
which it was assumed to already know.

- Otherwise, in π, all elements of L− must precede all elements of L+. In that case, B **will first**
recursively follow the same strategy on L−**, and then recursively follow the same strategy on**
L+.

Let Q(n) be the minimum number of rounds that A **requires against this adversarial strategy** B.

The description of the adversary strategy implies the following recurrence: Q(n) ≥n 4
+ 2·Q(n 2
).

Thus, by the master theorem, Q(n) = Ω(n log n**), proving the theorem.**
In the given proof, B **provides adversarial feedback and gradually commits to an adversarial**
permutation. However, even if the true permutation π
∗**is chosen uniformly at random ahead of**
time, B **can still follow essentially the same approach to provide adversarial feedback with respect**
to π
∗.

Fix π
∗, and consider the first stage of B, where it assigns '−**' and '+' to the items. When** A
proposes a permutation π, every pair (i, j) of adjacent unmarked items in π **is, with probability**
exactly 12
, in the wrong order with respect to π
∗**. If** n
′**elements are already marked, there are**
at least n−2n
′−1 2disjoint **pairs of adjacent unmarked items, each of which is in the wrong order**
independently with probability exactly 12
. Thus, for each of the first n 8 − **1 rounds, the probability**
that B **fails to find an unmarked adjacent pair in the wrong order is less than 2**− n 4 **. After** n 8 − 1 rounds, it starts its second stage, and a similar argument applies. Because the failure probability is exponentially low, we can take a union bound over all rounds until n **is sufficiently small, and** obtain that with high probability, A requires Ω(n log n**) queries on a random permutation.**

## 3.2 Implicit Feedback From Clicks

In the context of search engines, it has been argued (e.g., by **[12, 19, 1]) that a user's clicking** behavior provides implicit feedback of a specific form on the **ranking. Specifically, since users will**
typically read the search results from first to last, when a user skips some links that appear earlier in the ranking, and instead clicks on a link that appears later, her action suggests that the later link was more informative or relevant.

Formally, when a user clicks on the element at index i**, but did not previously click on any**
elements at indices j, j + 1, . . . , i − 1, this is interpreted as feedback that element i **should precede**
all of elements j, j + 1, . . . , i − 1. Thus, the feedback is akin to an "Insersion Sort**" move. (The**
Bubble Sort feedback model is the special case in which j = i − **1 always.)**
To model this more informative feedback, the new graph GIS **has more edges, and the edge**
lengths are non-uniform. It contains the same N nodes (one for each permutation). For a permutation π and indices 1 ≤ j < i ≤ n, πj←i **denotes the permutation that is obtained by moving the**
i th element in π **before the** j th element (and thus shifting elements j, j + 1, . . . , i − **1 one position**
to the right). In GIS, for every permutation π and every 1 ≤ j < i ≤ n**, there is an undirected**
edge from π to πj←i with length i − j. Notice that for i > j **+ 1, there is actually no user feedback**
corresponding to the edge from πj←i to π**; however, additional edges are permitted, and Lemma 3.4**
establishes that GIS **does in fact satisfy the "shortest paths" property.**
Lemma 3.4 GIS satisfies Definition 2.1 with respect to Insersion Sort **feedback.** Proof. **As in the proof of Lemma 3.1, there is one node for each permutation, and for each possible**
Insertion Sort feedback given in response to π, there is an edge in GIS **by definition (though** GIS
contains additional edges).

As with GBS, the distance between two permutations π, π∗in GIS **(now with respect to the**
given edge lengths) is still equal to the Kendall τ (π, π∗**). This is because going from** π to πj←i transposes exactly i−j **pairs of elements, which is the length of the corresponding edge, so no edge**
with i > j **+ 1 is essential for any shortest path.**
When the user feedback π
′ = πj←i**indicates that the** i th **element should be placed ahead of all**
the elements in positions j, j + 1, . . . , i − **1, then the** i th **element does indeed precede all of these**
elements in π
∗**. Thus,** τ (π
′, π∗) = τ (π, π∗)−(i−j), and the edge (π, π′**) lies on a shortest path from**
π to π
∗. Notice that the "extraneous" edges of the form (πj←i, π) for i > j + 1 (of cost i − j**) do**
not affect any shortest paths between pairs π, π∗**, as they can be replaced with the corresponding**
i − j **adjacent transpositions, without increasing the total length of the path.**
As in the case of GBS**, by applying Corollary 2.3 and Theorem 2.4, we immediately obtain the**
existence of interactive learning algorithms with the same **guarantees as those of Corollary 3.2.** Corollary 3.5 **Assume that in response to each equivalence query, the user responds with a pair**
of indices j < i such that element i should precede all elements j, j + 1**, . . . , i** − 1.

1. If all query responses are correct, then the target ordering can be learned by an interactive algorithm using at most log N = log n! ≤ n log n **equivalence queries.**
2. If query responses are correct with probability p > 12
, the target ordering can be learned by an interactive algorithm with probability at least 1 − δ **using at most** (1−δ)
1−H(p)
n log n + o(n log n) +
O(log2(1/δ)) **equivalence queries in expectation.**

## 3.3 Computational Considerations

While Corollaries 3.2 and 3.5 imply interactive algorithms using only O(n log n**) equivalence queries,**
they do not guarantee that the internal computations of the algorithms are efficient. The na¨ıve implementation requires explicitly keeping track of and comparing likelihoods on all N = n**! nodes.**
When p **= 1, i.e., the algorithm only receives correct feedback, it can be made computationally**
efficient using Theorem 2.6. To apply Theorem 2.6, it suffices to **show that one can efficiently** sample a (nearly) uniformly random permutation π **consistent with all feedback received so far.** Since the feedback is assumed to be correct, the set of all pairs (i, j**) such that the user implied** that element i must precede element j **must be acyclic, and thus must form a partial order. The** sampling problem is thus exactly the problem of sampling a linear extension **of a given partial**
order.

This is a well-known problem, and a beautiful result of Bubley and Dyer [8, 7] shows that the Karzanov-Khachiyan Markov Chain [14] mixes rapidly. Huber **[11] shows how to modify the Markov**
Chain sampling technique to obtain an exactly (instead of approximately) uniformly random linear extension of the given partial order. For the purpose of our interactive learning algorithm, the sampling results can be summarized as follows: Theorem 3.6 (Huber [11]) Given a partial order over n elements, let L **be the set of all linear**
extensions, i.e., the set of all permutations consistent with the partial order. There is an algorithm that runs in expected time O(n 3log n) **and returns a uniformly random sample from** L.

The maximum node degree in GBS is n − **1, while the maximum node degree in** GIS is O(n 2).

The diameter of both GBS and GIS is O(n 2**). Substituting these bounds and the bound from**
Theorem 3.6 into Theorem 2.6, we obtain the following corollary:
Corollary 3.7 Both under Bubble Sort feedback and Insersion Sort **feedback, if all feedback is**
correct, there is an efficient interactive learning algorithm using at most log n! ≤ n log n **equivalence**
queries to find the target ordering.

The situation is significantly more challenging when feedback could be incorrect, i.e., when p < 1. In this case, the user's feedback is not always consistent **and may not form a partial order.**
In fact, we prove the following hardness result. Theorem 3.8 There exists a p (depending on n**) for which the following holds. Given a set of user**
responses, let µ(π) be the likelihood of π given the responses, and normalized so that Pπ µ(π**) = 1**.

Let 0 < ∆ < 1 **be any constant. There is no polynomial-time algorithm to draw a sample from a**
distribution µ
′ with dTV(µ, µ′) ≤ 1 − ∆ unless RP = NP.

Proof. We prove this theorem using a reduction from Minimum Feedback Arc Set, a wellknown NP-complete problem [13]. Given a directed graph G and number k, the Minimum Feedback Arc Set problem asks if there is a set of at most k arcs of G **whose removal will leave the**
remaining graph acyclic. This is equivalent to asking if there is a permutation π **of the nodes of** G
such that at most k arcs go from higher-numbered nodes in π **to lower-numbered ones.**
Given ∆, a graph G with n nodes and m edges, and k**, we define the following sampling problem.**
Consider sampling from permutations of n elements, let p = 1− 1 2(n+1)! , and let the m **user responses**
be exactly the (directed) edges of G.

For any permutation π, let xπ be the number of queries that π agrees with, and yπ **the number**
of queries that π disagrees with. Then, for all π, xπ + yπ = m**, and the (unnormalized) likelihood**
for π is L(π) = p xπ · (1 − p)
yπ **. Let** y
∗ = minπ yπ**, and let Π**∗ = {π | yπ = y
∗} **be the set of all**
permutations minimizing yπ. Then, for any permutation π ∈ Π∗**, we have**

$$L(\pi)\ =\ \left(1-\frac{1}{2(n+1)!}\right)^{m-y^{*}}\cdot\left(\frac{1}{2(n+1)!}\right)^{y^{*}}\ =:\ L^{*}.$$  for any permutation $\pi^{\prime}\notin\Pi^{*}$, we get that 
On the other hand, for any permutation π
′ ∈/ Π∗**, we get that**

If any permutation $\pi\not\in\Pi$ , we get that  $\begin{array}{ll}L(\pi')&\leq\ \left(1-\dfrac{1}{2(n+1)!}\right)^{m-y^{*}-1}\cdot\left(\dfrac{1}{2(n+1)!}\right)^{y^{*}+1}\\ &=L^{*}\cdot\dfrac{1}{2(n+1)!}/\left(1-\dfrac{1}{2(n+1)!}\right)\\ &\leq\ \dfrac{L^{*}}{(n+1)!}.\end{array}$  I'm absolutely sure what it looks wrong. 
Thus, under the normalized likelihood distribution µ**, the total sampling probability of all**
permutations π ∈ Π∗ **must be**

$\sum_{\pi\in\Pi^{*}}\mu(\pi)=\frac{\sum_{\pi\in\Pi^{*}}L(\pi)}{\sum_{\pi^{\prime}}L(\pi^{\prime})}$  $\begin{array}{c}\hskip14.226378pt=\hskip14.226378pt\frac{L^{*}\cdot|\Pi^{*}|}{L^{*}\cdot|\Pi^{*}|+\sum_{\pi^{\prime}\notin\Pi^{*}}L(\pi^{\prime})}\\ \hskip14.226378pt\geq\hskip14.226378pt\frac{L^{*}\cdot|\Pi^{*}|}{L^{*}\cdot|\Pi^{*}|+n!\cdot L^{*}\cdot\frac{1}{(n+1)!}}\\ \hskip14.226378pt=\hskip14.226378pt\frac{|\Pi^{*}|}{|\Pi^{*}|+1/(n+1)}\\ \hskip14.226378pt\geq\hskip14.226378pt1-1/(n+1).\end{array}$  It is a consequence of the fact that 
If µ
′ has total variation distance at most 1 − ∆ from µ**, it must satisfy** Pπ∈Π∗ µ
′
P
(π) ≥
π∈Π∗ µ(π) − (1 − ∆) ≥ ∆ − 1/(n **+ 1). In particular, it must sample a permutation** π ∈ Π∗
with constant probability ∆ − 1/(n **+ 1).**
A randomized algorithm can now simply sample O(log n) permutations π **according to** µ
′**. If**
one of these permutations, applied to the nodes of G, has at most k edges going from highernumbered to lower-numbered nodes, it constitutes a feedback arc set of at most k **edges, and the**
algorithm can correctly answer "Yes" to the Minimum Feedback Arc Set **instance. When the** algorithm sees no π with fewer than k **+ 1 edges going from higher-numbered to lower-numbered** nodes, it answers "No." This answer may be incorrect. But notice that if it is incorrect, the Minimum Feedback Arc Set instance must have had a feedback arc set of at most k **edges,** and the randomized algorithm would sample at least one corresponding permutation π **with high**
probability. Thus, when the algorithm answers "No," it is correct with high probability. Thus, we have an RP algorithm for Minimum Feedback Arc Set **under the assumption of an efficient**
approximate sampling oracle.

It should be noted that the value of p **in the reduction is exponentially close to 1. In this range,**
incorrect feedback is so unlikely that with high probability, the algorithm will always see a partial order. It might then still be able to sample efficiently. On the **other hand, for smaller values of** p
(e.g., constant p**), sampling approximately from the likelihood distribution might be possible via a**
metropolized Karzanov-Khachiyan chain or a different approach. This problem is still open.

## 3.4 Arbitrary Swap Model

In order to demonstrate that the condition of Definition 2.1 is not trivial to satisfy, we consider another natural feedback model for ranking. In the Arbitrary Swap **model, a user can exhibit**
two arbitrary elements i, j **that are in the wrong order; doing so does not imply anything about** the relation between i, j **and the elements that are between them. We will show that in contrast to** the Insersion Sort and Bubble Sort models, there is no almost-undirected graph G **satisfying** Definition 2.1; hence, our general framework cannot lead to an o(n 2**) interactive algorithm for**
learning a ranking in the Arbitrary Swap **model.** Theorem 3.9 For the Arbitrary Swap model, there is no directed graph G **which is almost**
undirected with c < n **and satisfies Definition 2.1.**
Proof. Assume that there is a graph G which satisfies the definition. For every 1 ≤ i ≤ n**, define**
the permutation πi = hi, i + 1, . . . , n, 1, . . . , i − 1i and let S = {πi| 1 ≤ i ≤ n}. Let µ **be the node**
weight function that assigns uniform weight to every πi **and 0 to all other permutations.**
Consider an arbitrary permutation π **proposed to the user. We show that there exists a response**
that it is consistent with every permutation in S **but one. Distinguish the following two cases for**
the proposed π:
- If there exists 1 ≤ i < n such that π(i+1) < π(i) (i.e., i+1 precedes i in π**), then the response**
"i and i + 1 are in the wrong order" is consistent with every permutation in S **except** πi+1.

- If π(i) < π(i + 1) for every 1 ≤ i < n, then π = h1, 2, . . . , ni. In this case, "n and 1 **are in the**
wrong order" is a response that is consistent with every permutation in S **except** π1.

Hence, Φµ(π) ≥
n−1 nfor every permutation π. This implies that G **cannot be almost undirected**
with c < n; otherwise, Proposition 2.1 would imply the existence of a permutation π **with Φ**µ(π) <
n−1 n
.

While Theorem 3.9 rules out an algorithm based on the graph framework we propose, it is worth noting that there is an algorithm (not based on our framework) that, in the absence of noise, can learn the correct permutation under the Arbitrary Swap model using O(n log n**) queries. It is**
an interesting question for future work to generalize our model so that it contains this algorithm as a natural special case.

## 4 Application Ii: Learning A Clustering

Many traditional approaches for clustering optimize an (explicit) objective function or rely on assumptions about the data generation process. In interactive clustering, the algorithm repeatedly proposes a clustering, and obtains feedback that two proposed clusters should be merged, or a proposed cluster should be split into two. There are n items, and a clustering C **is a partition of the**
items into disjoint sets (clusters) C1, C2, . . .. It is known that the target clustering has k **clusters,**
but in order to learn it, the algorithm can query clusterings **with more or fewer clusters as well.**
The user feedback has the following semantics, as proposed by Balcan and Blum [6] and Awasthi et al. [5, 4].

1. Merge(Ci, Cj ): Specifies that all items in Ci and Cj **belong to the same cluster.**
2. Split(Ci): Specifies that cluster Ci **needs to be split, but not into which subclusters.**
Notice that feedback that two clusters be merged, or that a cluster be split (when the split is known), can be considered as adding constraints on the clustering (see, e.g., [22]); depending on whether feedback may be incorrect, these constraints are hard or soft.

We define a weighted and directed graph GUC on all clusterings C**. Thus,** N = Bn ≤ n n**is the**
n th **Bell number. When** C
′is obtained by a Merge of two clusters in C, GUC **contains a directed**
edge (C, C
′) of length 2. If C = {C1, C2, . . .} is a clustering, then for each Ci ∈ C**, the graph** GUC
contains a directed edge of length 1 from C to C \ {Ci} ∪ {{v} | v ∈ Ci}. That is, GUC **contains an**
edge from C to the clustering obtained from breaking Ci**into singleton clusters of all its elements.**
While this may not be the "intended" split of the user, we can still associate this edge with the feedback.

Lemma 4.1 GUC satisfies Definition 2.1 with respect to Merge and Split **feedback.**
Proof. GUC **has a node for every clustering, and its edges capture every possible user feedback.**8 Let C = {C1, . . . , Ck} and C
′ = {C
′1
, . . . , C′k
′} be two clusterings with k and k
′clusters, respectively. We call a cluster C ∈ C mixed **(with respect to** C
′**) if it contains elements from at**
least two different clusters in C
′**. Let** xC,C
′ (x for short) be the number of mixed clusters C ∈ C
with respect to C
′**, and** yC,C
′ (y **for short) the total number of elements in mixed clusters. Notice that it is possible that** xC,C
′ 6= xC
′,C, and similarly for y**. Define the (asymmetric) distance**
d(C, C
′**) = 2**yC,C
′ − xC,C
′ **+ 2(**k − k
′**). We claim that the length of every shortest path from** C to C
′
with respect to the edge lengths ωe is d(C, C
′).

First, we show that there exists a path of length d(C, C
′**) from** C to C
′**. Start the path by**
breaking the x mixed clusters in C, using Split **edges of length 1 each. At this point, we have a** clustering C
′′ with y + k − x **clusters, each of which is a subset of one of the clusters in** C
′**. Then,**
using y + k − x − k
′**cluster merges (each of edge length 2), we obtain** C
′**. The total length of this**
path is x **+ 2(**y + k − x − k
′) = d(C, C
′).

Next, we show that there is no path in GUC **from** C to C
′**shorter than the claimed bound of**
d(C, C
′**). We do so by induction on the number of edges in the path. In the base case of 0 edges,**
C = C
′**, so the claimed bound of** d(C, C
′) = 0 is a lower bound. Now consider an edge (C, C**¯) which is**
the first edge on a path from C to C
′. Let ¯k be the number of clusters in C**¯, and** x = xC,C
′, y = yC,C
′,
x¯ = xC¯,C
′, ¯y = yC¯,C
′**. We distinguish two cases based on the type of edge from** C to C¯.

- If (C, C¯) is a Merge edge, then ω(C,C¯) = 2, and ¯k = k −**1. We distinguish two subcases, based**
on the two clusters C1, C2 ∈ C **that were merged:**
1. If C1 or C2 was mixed, or C1 ∪ C2 is not mixed, then ¯x ≤ x and ¯y ≥ y **(because**
merging two clusters cannot remove any elements from mixed clusters). In particular, 2¯y − x¯ ≥ 2y − x.

2. If neither C1 not C2 was mixed, but the new cluster C1 ∪ C2 is mixed, then ¯x = x + 1 and ¯y = y + |C1| + |C2| ≥ y + 2. Therefore, again 2¯y − x¯ ≥ 2y + 4 − (x **+ 1)** ≥ 2y − x.

In either case, 2¯y − x¯ ≥ 2y − x**, so**

$$\begin{array}{r l}{d({\bar{C}},{\mathcal{C}}^{\prime})=2{\bar{y}}-{\bar{x}}+2({\bar{k}}-k^{\prime})}\\ {\geq2y-x+2((k-1)-k^{\prime})}\\ {=d({\mathcal{C}},{\mathcal{C}}^{\prime})-2}\\ {=d({\mathcal{C}},{\mathcal{C}}^{\prime})-\omega_{({\mathcal{C}},{\bar{C}})}.}\end{array}$$
8**As mentioned before, we** translate user feedback of the form Split **into a request for breaking the cluster into**
singletons. From the user's perspective, nothing changes.
- If (C, C¯) is a Split(C) edge, then ω(C,C¯) = 1, and ¯k = k + |C| − **1. Again, there can be at**
most one fewer mixed cluster (namely, C). If C was mixed, then ¯x = x − 1 and ¯y = y − |C|. Otherwise, ¯x = x and ¯y = y. In both cases, we have that 2¯y − x¯ ≥ 2y − x − 2|C| **+ 1. Thus,**

$$d(\bar{\mathcal{C}},\mathcal{C}^{\prime})=2\bar{y}-\bar{x}+2(\bar{k}-k^{\prime})$$ $$\geq2y-x-2|C|+1+2(k+|C|-1-k^{\prime})$$ $$=2y-x+2(k-k^{\prime})-1$$ $$=d(\mathcal{C},\mathcal{C}^{\prime})-1$$ $$=d(\mathcal{C},\mathcal{C}^{\prime})-\omega_{(\mathcal{C},\bar{\mathcal{C}})}.$$

In both cases, we can apply induction to C
′**, and conclude that there is no path of total length less**
than d(C, C
′**) from** C to C
′.

Finally, we verify that every correct feedback C¯ to a queried clustering C **lies on a path of length**
d(C, C
∗) from C **to the target clustering** C
∗.

- If (C, C¯) is a correct user response in the form of Merge**, then** xC¯,C
∗ = xC,C
∗ and yC¯,C
∗ = yC,C
∗.

However, C¯ has one fewer cluster than C**, so**
d(C¯, C
∗) = d(C, C
∗) − 2 = d(C, C
∗) − ω(C,C¯)
.

- **If (**C, C
′) is a correct response in the form of Split and C **is the cluster that needs to be**
split/broken, then xC¯,C∗ = xC,C
∗ − **1 and** yC¯,C∗ = yC,C
∗ − |C|. Moreover, C¯ has |C| − **1 more**
clusters than C**. By applying all these equations, similar to the earlier calculations, we get**
that d(C¯, C
∗) = d(C, C
∗) − 1 = d(C, C
∗) − ω(C,C¯)
.

In both cases, by induction on d(C, C
∗), we show that every correct user feedback from C **lies on a**
path of length d(C, C
∗**) to** C
∗.

Finally, we show that each edge is part of "short" cycle. Consider any two clusterings C, C
′ **with**
k, k′clusters, respectively. By using k − 1 Split **operations (of length 1 each), we can first break** C
into all singletons. Then, by using n − k
′ Merge **operations (the edges having length 2 each), we**
can obtain C
′. The total length of this path is at most k − **1 + 2(**n − k
′) ≤ 3n − **3. In particular,**
for any edge (C, C
′**), there is a "returning" path from** C
′to C of total length at most 3n − **3, which**
together with the edge (C, C
′) gives a cycle of total length at most 3n − 1 ≤ 3n**. Because (**C, C
′)
has length at least 1, it makes up a 1 3n fraction of the cycle's length. (With a little more care, this bound can be easily improved to 1 2n
.)
GUC **is directed, and (as mentioned in the proof of Lemma 4.1) every edge makes up at least a**
1 3n fraction of the total length of at least one cycle it participates in. Hence, Proposition 2.1 gives an upper bound of 3n−1 3non the value of β **in each iteration. A more careful analysis exploiting the**
specific structure of GUC **gives us the following:**
Lemma 4.2 In GUC, for every non-negative node weight function µ**, there exists a clustering** C
with Φµ(C) ≤ 12
.

Proof. Without loss of generality, assume that µ **is normalized, so that** P
s µ(s**) = 1. We describe**
an explicit greedy procedure for finding a clustering C**, similar to a procedure employed by Awasthi**
and Zadeh [5]. Start with a clustering into singleton sets, i.e., C = {{v} | v is an item}**. Repeatedly**
look for two clusters C, C′ ∈ C **such that the total likelihood of all the clusterings that group all of**
C ∪ C
′**in one cluster is strictly more than** 12
. As long as such C, C′**exist, merge them into a new**
cluster, and continue with the new clustering. The procedure terminates with some clustering C
for which no pair of clusters can be further merged. We will show that Φµ(C) ≤
1 2
, by considering all clusterings C
′ **adjacent to** C:
- If C
′is obtained by merging two clusters C, C′ ∈ C**, then by the termination condition,**
µ(N(C, C
′)) ≤
1 2
; otherwise, C and C
′ **would have been merged.**
- If C
′is obtained by splitting a cluster C ∈ C, then we first notice that C **cannot be a singleton**
cluster. Therefore, it was created by merging two other clusters at some point earlier in the greedy process. By the merge condition, the total weight of the clusterings C
′′ **that have all**
of C **in the same cluster is strictly more than** 12
. Therefore, the total weight of all clusterings C
′′ that prefer any partitioning of C **is less than** 12
. This implies µ(N(C, C
′)) ≤
1 2 in the **Split**
case as well.

In the absence of noise in the feedback, Lemmas 4.1 and 4.2 and **Theorem 2.2 imply an algorithm**
that finds the true clustering using log N = log B(n) = Θ(n log n**) queries. Notice that this is worse** than the "trivial" algorithm, which starts with each node as **a singleton cluster and always executes**
the merge proposed by the user, until it has found the correct **clustering; hence, this bound is itself** rather trivial.

Non-trivial bounds can be obtained when clusters belong to a **restricted set, an approach also**
followed by Awasthi and Zadeh [5]. If there are at most M **candidate clusters, then the number of**
clusterings is N0 ≤ Mk. For example, if there is a set system F of VC dimension at most d **such**
that each cluster is in the range space of F**, then** M = O(n d**) by the Sauer-Shelah Lemma [20, 21].**
Combining Lemmas 4.1 and 4.2 with Theorems 2.2 and 2.4, we obtain the existence of learning algorithms with the following properties:
Corollary 4.3 Assume that in response to each equivalence query, the user responds with **Merge**
or Split. Also, assume that there are at most M **different candidate clusters, and the clustering**
has (at most) k **clusters.**
1. If all query responses are correct, then the target clustering can be learned by an interactive algorithm using at most log N = O(k log M) **equivalence queries. Specifically when** M =
O(n d), this bound is O(kd log n)**. This result recovers the main result of [5].**9 2. If query responses are correct with probability p > 12
, the target clustering can be learned with probability at least 1 − δ **by an interactive algorithm using at most** (1−δ)k log M
1−H(p) + o(k log M) +
O(log2(1/δ)) **equivalence queries in expectation. Our framework provides the noise tolerance**
"for free;" [5] instead obtain results for a different type of **noise in the feedback.**

## 4.1 Interactive Clustering With Given Cluster Splits

We now also consider a model in which the user specifies exactly how **to split a cluster when**
proposing a split. The operation Split(Ci, C′, C′′) specifies that the cluster Ci **should be split**
into C
′ and C
′′**, and thereby implies that none of the items in** C
′**should be clustered with any**
item in C
′′**. (Naturally,** C
′ and C
′′ must be disjoint, and their union must be Ci**.) We require the**
same assumptions as for the model of "unspecified splits," and the bounds we obtain are the same.

9**In fact, the algorithm in [5] is implicitly computing and querying a node with small Φ in this directed graph.**
Hence, the results in this model are weaker than those for the **"unspecified splits" model. We are**
including them because we believe them to be a clean and natural application of the interactive learning framework.

We define an undirected weighted graph GGC**, again containing a node for each clustering**
C**. There is an (undirected) edge between two clusterings** C, C
′**if and only if there exist clusters**
Ci ∈ C, C′j
, C′j
′ ∈ C′ **with** C
′ = C \ {Ci**} ∪ {**C
′j
, C′j
′}**, i.e.,** C
′is obtained from C by splitting Ci**into**
C
′j and C
′
j
′**. The length of the edge (**C, C
′**) is** ω(C,C
′) = 2|C
′j | · |C
′j |.

Lemma 4.4 GGC satisfies Definition 2.1 with respect to Merge and Split(Ci, C′, C′′) **feedback.**
Proof. Corresponding to each clustering C, we define an n×n adjacency matrix A(C) **with** A
(C)
i,j = 1 if items i and j are in the same cluster in C**, and** A
(C)
i,j **= 0, otherwise. (By definition,** A
(C)
i,i = 1 for every item i.) For two clusterings C and C
′**, define their distance** d(C, C
′**) to be the Hamming**
distance of their adjacency matrices A(C) and A(C
′)**, i.e., the total number of bits in which their**
adjacency matrices differ.

If there is an edge in GGC between C and C
′, then C and C
′ **will differ by exactly one cluster being**
split into two (or two clusters being merged into one). Let C, C′ **be the two merged clusters (or the**
clusters resulting from the split). The merge/split changes exactly 2|C**| · |**C
′| **bits in the adjacency**
matrix, and the length assigned to the edge (C, C
′**) is exactly** ω(C,C
′) = 2|C**| · |**C
′| = d(C, C
′).

We now show that for each pair C, C
′, there is a path in GGC **of total edge length exactly equal**
to d(C, C
′**). We show this by induction on** d(C, C
′**), the base case** d(C, C
′**) = 0 being trivial because**
C = C
′. Suppose that C 6= C
′. Then, there exist10 C ∈ C, C′1
, C′2 ∈ C′**such that** C ∩ C
′1 6= ∅ and C ∩ C
′2 6= ∅. Consider the move Split(**C, C** ∩ C
′1
, C \ C
′1
). Call the resulting clustering C
′′**. Its**
adjacency matrix has A
(C
′′)
i,j **= 0 =** A
(C
′)
i,j **for all** i ∈ C ∩ C′1
, j ∈ C \ C′1 and i ∈ C \ C′1
, j ∈ C ∩ C′1
,
while A
(C)
i,j = 1 for all i, j ∈ C**. Thus,**
d(C, C
′) = d(C
′′, C
′**) + 2**|C ∩ C
′
1 | · |C ∩ C
′
2 | = d(C
′′, C
′) + ω(C,C
′′).

By induction hypothesis, there is a path of total length d(C
′′, C
′**) from** C
′′ to C
′in GGC**, which**
combined with the edge (C, C
′′**) gives the desired path from** C to C
′**, completing the inductive proof.**
We can now show that when a user correctly proposes a move corresponding to an edge (C, C
′),
it indeed lies on a shortest path from C to C
∗**. We consider two cases:**
- The user proposes Merge(C, C′). This means that all of C and C
′ **belong to one cluster in**
C
∗; in particular, all matrix entries for **i, j** ∈ C ∪ C
′ are 1. In A(C), all entries for **i, j** ∈ C
are 1, as are all entries for **i, j** ∈ C
′**; on the other hand, all entries** A
(C)
i,j for i ∈ **C, j** ∈ C
′
or for i ∈ C
′, j ∈ C are 0. After the Merge**, all these entries are 1 as well, decreasing the**
Hamming distance by 2|C**| · |**C
′|**. Since this is the length of the edge (**C, C
′**) as well, and there**
is a path from C
′to C
∗ **with total length equal to their Hamming distance (the argument of**
the previous paragraph), C
′**indeed lies on a shortest path from** C to C
∗.

- The user proposes Split(C, C′, C′′**). This means that no pair** i ∈ C
′, j ∈ C
′′ **belongs to the**
same cluster in C
∗, whereas they are all grouped together in C**, meaning that** A
(C)
i,j **= 1 for all**
i, j ∈ C**. Thus,** d(C
′, C
∗) = d(C, C
∗) − 2|C
′**| · |**C
′′| = d(C, C
∗) − ω(C,C
′)**. Again by the argument**
from the previous paragraph, there is a path of total length d(C
′, C
∗**) from** C
′to C
∗**, so (**C, C
′)
indeed lies on a shortest path from C to C
∗.

10Technically, one might have to switch the roles of C and C
′**for this to be true.**
As in the clustering model in Section 4, the obvious log N = log B(n) = Θ(n log n**) bound on**
the number of queries can be improved when clusters belong to **a restricted set of size at most** M,
giving us the following result:
Corollary 4.5 Assume that in response to each equivalence query, the user responds with **Merge**
or Split(Ci, C′, C′′). Also, assume that there are at most M **different candidate clusters, and the**
clustering has k **clusters.**
1. If all query responses are correct, then the target clustering can be learned by an interactive algorithm using at most O(k log M) **equivalence queries. Specifically when** M = O(n d)**, this**
bound is O(kd log n).

2. If query responses are correct with probability p > 12
, the target clustering can be learned with probability at least 1 − δ **by an interactive algorithm using at most** (1−δ)k log M
1−H(p) + o(k log M) +
O(log2(1/δ)) **equivalence queries in expectation.**
We saw earlier that a trivial algorithm in the weaker model achieved a bound of n − k **queries.**
The situation is even more extreme with more informative feedback: if there are no errors in the feedback, a bound of k − 1 can actually be obtained by another trivial algorithm. The **algorithm**
starts from a clustering of all items in one cluster, and repeatedly obtains feedback, which must provide a correct split of one cluster into two. While this algorithm uses significantly fewer queries, it is not clear how to generalize it to the case of incorrect feedback: in particular, repeating the same query multiple times to obtain higher assurance will not work, as there are many correct answers the algorithm could receive. Thus, the algorithm cannot rely on a majority vote.

## 5 Application Iii: Learning A Classifier

Learning a binary classifier is the original and prototypical application of the equivalence query model of Angluin [2], which has seen a large amount of follow-up work since (see, e.g., [17, 18]). Naturally, if no assumptions are made on the classifier, then n **queries are necessary in the worst case.**
In general, applications therefore restrict the concept classes to smaller sets, such as assuming that they have bounded VC dimension. We use F **to denote the set of all possible concepts, and write**
M = |F|; when F has VC dimension d**, the Sauer-Shelah Lemma [20, 21] implies that** M = O(n d).

Learning a binary classifier for n **points is an almost trivial application of our framework**11.

When the algorithm proposes a candidate classifier, the feedback it receives is a point with a corrected label (or the fact that the classifier was correct on all points).

We define the graph GCL to be the n-dimensional hypercube12 **with unweighted and undirected**
edges between every pair of nodes at Hamming distance 1. Because the distance between two classifiers C, C
′is exactly the number of points on which they disagree, GCL **satisfies Definition 2.1.**
Hence, we can apply Corollary 2.3 and Theorem 2.4 with Sinit equal to the set of all M **candidate**
classifiers to obtain the following:
Corollary 5.1 - With perfect feedback, the target classifier is learned using log M **queries**13.

11The results extend readily to learning a classifier with k ≥ **2 labels.**
12When there are k labels, GCL **is a graph with** k n**nodes.**
13With k labels, this bound becomes (k − **1) log** M.
- When each query response is correct with probability p > 12
, there is an algorithm learning the true binary classifier with probability at least 1 − δ **using at most** (1−δ) log M
1−H(p) + o(log M) +
O(log2(1/δ)) **queries in expectation.**
Thus, we recover the classic result on learning a classifier in the equivalence query model when feedback is perfect and extend it to the noisy setting.

## 5.1 Proper Learning Of Hyperplanes

While the learning algorithm we described will always terminate with the correct classifier, and in particular one from F**, as part of the learning process, it may propose classifiers outside of** F,
somewhat akin to improper learning. Angluin's original paper [2] already observed that when each query has to be in F, a large number of queries may be necessary even when F **has very small VC**
dimension: a particularly stark example is when F **consists of all singleton sets.**
Since bounded VC dimension is not sufficient to ensure query-efficient proper learning in the equivalence query model, a large body of subsequent work (see, e.g., [18] for an overview) has focused on specific geometric classes such as hyperplanes or **axis-aligned boxes. Here, we show that**
the results on learning hyperplanes in R
dcan be obtained directly in our framework. Let H **be the**
family of all subsets of the n points that are separable using a d**-dimensional hyperplane. The key**
insight is:
Lemma 5.2 For every weight function µ : H → R≥0 **on linear classifiers, there exists a linear**
classifier C ∈ H **with** Φµ(C) ≤
d+1 d+2 .

The key to the proof of Lemma 5.2 is the following generalization of Carath´eodory's Theorem.

We suspect that Lemma 5.3 must be known, but since we could not **find a statement of it despite**
a long search, we provide a self-contained proof here.

Lemma 5.3 Let P, Q **be sets in** R
d **whose convex hulls intersect. Then, there exist sets** P
′ ⊆
P, Q′ ⊆ Q **with** |P
′| + |Q′| ≤ d + 2 **such that their convex hulls intersect.**
Notice that Carath´eodory's Theorem is the special case when |P| **= 1. The lemma can also be**
easily generalized to points in the intersection of k sets, rather than just the special case k **= 2.** Proof. **The proof is quite similar to one of the standard proofs for Carath´eodory's Theorem, and** based on properties of basic feasible solutions of an LP.

First, to avoid notational inconvenience, we may assume w.l.o.g. that P and Q **are finite; in fact,**
that |P|, |Q| ≤ d + 1. This is due to Carath´edory's Theorem. Let x ∈ conv(P) ∩ conv(Q**). Then,**
because x ∈ conv(P**), there exists** P
′ ⊆ P of cardinality at most d + 1 such that x ∈ **conv(**P
′);
similarly for Q**. Hence, we have exhibited subsets** P
′ ⊆ P, Q′ ⊆ Q of size at most d **+ 1 each, whose**
convex hulls intersect. For the remainder of the proof, we can therefore focus on P
′, Q′**, and will**
rename them to **P, Q**.

Write P = {p1, p2, . . . , pd+1} and Q = {q1, q2, . . . , qd+1}. A point x is in conv(P**) iff there**
exist λ1, . . . , λd+1 ≥ **0 with** Pi λi **= 1 such that** x =Pi λipi. Similarly, x ∈ conv(Q**) iff there**
exist µ1, . . . , µd+1 ≥ 0 with Pj µj = 1 such that x =Pj µjqj **. We can therefore characterize the**
intersection conv(P) ∩ conv(Q) using the following linear program with variables λi, µj :

$$\begin{array}{l}{{\sum_{i}\lambda_{i}p_{i}=\sum_{j}\mu_{j}q_{j}}}\\ {{\sum_{i}\lambda_{i}=1}}\\ {{\sum_{j}\mu_{j}=1}}\end{array}$$
$$\begin{array}{r l}{\lambda_{i}\geq0}&{{}{\mathrm{~for~all~}}i}\\ {\mu_{j}\geq0}&{{}{\mathrm{~for~all~}}j.}\end{array}$$

Notice that the first "constraint" is actually d **constraints, one for each dimension. Hence, the**
linear program has 2d + 2 variables and 3d **+ 4 constraints. By assumption, this LP has a feasible**
solution, so it must have a basic **feasible solution. A basic feasible solution is characterized by**
2d + 2 constraints that hold with equality. Therefore, at most d **+ 2 inequalities can be strict. The**
only inequalities in the LP are the non-negativity constraints, implying that at most d**+ 2 variables**
λi, µj **can be strictly positive. Hence, there is a point in the intersection that can be written as a**
convex combination of points pi and qj , using at most d **+ 2 points total.**
Using Lemma 5.3, the proof of Lemma 5.2 is fairly straightforward.

Proof of Lemma 5.2. **We will use the terms "linear classifier" and "hyperplane" interchangeably in the proof, using whichever term better emphasizes the concept we are illustrating at the**
time. W.l.o.g., we assume that the weights µ **assigned to linear classifiers are normalized so that** they add up to 1.

For each linear classifier C ∈ H and sample point x, let C(x) ∈ {0, 1} **be the assigned binary**
label. Define φ(x) := PC∈H µ(C)·C(x) as the weighted average label assigned to x **by all classifiers.**
Define P := {x | φ(x) <1 d+2 } and Q := {x | φ(x) > 1 −1 d+2 }.

We claim that the convex hulls of P and Q **do not intersect. Suppose for contradiction that**
they did; then, by Lemma 5.3, there exist P
′ ⊆ P, Q′ ⊆ Q **with** |P
′| + |Q′| ≤ d **+ 2 and** x ∈
conv(P
′)∩ conv(Q′**). Write** P
′ = {p1, . . . , pk} and Q′ = {q1, . . . , qℓ} with k + ℓ ≤ d **+ 2. For each** pi, let H
p i
:= {C ∈ H | C(pi) = 0} be the set of all linear classifiers that assign label 0 to pi**; similarly,**
let H
q j
:= {C ∈ H | C(qj ) = 1} be the set of all linear classifiers that assign label 1 to qj **. By**
the definition of P and Q, µ(H
p i
) > 1 − 1 d+2 for all i**, and** µ(H
q j
) > 1 − 1 d+2 for all j**, or, taking**
complements, µ(H
p i
) <1 d+2 for all i**, and** µ(H
q j
) <1 d+2 for all j**. Because**

$$\mu(\bigcup_{i}\overline{{{\mathcal{H}}}}_{i}^{p}\cup\bigcup_{j}\overline{{{\mathcal{H}}}}_{j}^{q})\leq\sum_{i}\mu(\overline{{{\mathcal{H}}}}_{i}^{p})+\sum_{j}\mu(\overline{{{\mathcal{H}}}}_{j}^{q})\ <\ k\cdot\frac{1}{d+2}+\ell\cdot\frac{1}{d+2}\ <\ 1,$$

there must exist at least one linear classifier C ∈Ti H
p i ∩Tj H
q j
. Because C(pi**) = 0 for all** pi ∈ P
′,
and x ∈ **conv(**P
′), we must have C(x) = 0. But because C(qj ) = 1 for all qj ∈ Q′, and x ∈ **conv(**Q′),
we must also have C(x**) = 1. This is a contradiction, and we have proved that the convex hulls of**
P and Q **are disjoint.**
Because conv(P) ∩ conv(Q) = ∅**, the Hyperplane Separation Theorem implies that there is a**
hyperplane C separating P and Q. We will show that any such C (labeling every point in P **with** 0 every point in Q **with 1) satisfies the claim of the lemma; thereto, fix one arbitrarily. Consider**
any feedback that could be given to the algorithm; because the graph GCL is the n**-dimensional**
hypercube, this feedback is in the form of a point x which C **mislabels. We distinguish three cases** for x:
- If x ∈ P, then C(x) = 0. By definition of P, the total weight of classifiers labeling x **with 0 is**
more than 1−1 d+2 **, and all these classifiers are inconsistent with the feedback. Therefore, the**
total weight of all classifiers consistent with the feedback decreased by a factor d **+ 2, which** is much stronger than the claim of the lemma.

- If x ∈ Q, then C(x**) = 1; apart from this, the proof is identical to the case** x ∈ P.

- If x /∈ P ∪ Q, then either C(x) = 0 or C(x**) = 1 are possible. The fractional label** φ(x) ∈
[1 d+2 , 1−1 d+2 **] was inconclusive. But because** φ(x) ≥1 d+2 **, at least a** 1 d+2 **(weighted) fraction of**
classifiers labeled x **with 1; similarly, because** φ(x) ≤ 1−1 d+2 **, at least a** 1 d+2 **(weighted) fraction**
of classifiers labeled x with 0. Thus, whichever label C assigned to x **and was corrected about,**
at least a 1 d+2 **weighted fraction of classifiers are inconsistent with the feedback.**
Thus, in each case, we obtain that the total weight of classifiers consistent with the feedback is at most a max( 1 d+2 , 1 −1 d+2 ) = d+1 d+2 **fraction of the total weight, and the lemma follows.**
Using Lemma 5.2, Theorem 2.2 with β =
d+1 d+2 **, and the fact that** M ≤ n d**, we immediately**
recover Theorem 5 of [16] for binary classification:
Corollary 5.4 (Theorem 5 of [16]) **In the absence of noise, a hyperplane can be properly learned**
using at most O(d log d+2 d+1 n) = O(d 2log n) **equivalence queries.**
As with the result for improper learning, we obtain a bound in **the case of imperfect feedback**
by using Theorem 2.4 in place of Theorem 2.2.

## 6 Discussion And Conclusions

We defined a general framework for interactive learning from **imperfect responses to equivalence**
queries, and presented a general algorithm that achieves a small number of queries. We then showed how query-efficient interactive learning algorithms **in several domains can be derived with**
practically no effort as special cases; these include some previously known results (classification and clustering) as well as new results on ranking/ordering.

Our work raises several natural directions for future work. **Perhaps most importantly, for which**
domains can the algorithms be made computationally efficient **(in addition to query-efficient)? We** provided a positive answer for ordering with perfect query responses, but the question is open for ordering when feedback is imperfect. For classification, when the possible clusters have VC dimension d**, the time is** O(n d), which is unfortunately still impractical for real-world **values of** d.

Maass and Tur´an [16] show how to obtain better bounds specifically when the sample points form a d**-dimensional grid; to the best of our knowledge, the question is open when the sample points**
are arbitrary. The Monte Carlo approach of Theorem 2.6 reduces the question to the question of sampling a uniformly random hyperplane, when the uniformity is over the partition **induced by the** hyperplane (rather than some geometric representation). For clustering, even less appears to be known.

Another natural question is motivated by the discussion in Section 5 and its application to clustering. We saw that the number of queries can increase significantly in proper interactive learning, i.e., when the set of models that can be queried is restricted to those that are themselves candidates. When concepts were specifically defined as hyperplane partitions, the increase can be bounded by O(log d). Can similar bounds be obtained for other concept classes? **What happens in** the case of clustering if each proposed clustering must only **have clusters from the allowed set?**
Finally, we are assuming a uniform noise model. An alternative would be that the probability of an incorrect response depends on the type of response. In particular, false positives could be extremely likely, for instance, because the user did not try **to classify a particular incorrectly labeled** data point, or did not see an incorrect ordering of items far down in the ranking. Similarly, some wrong responses may be more likely than others; for example, **a user proposing a merge of two**
clusters (or split of one) might be "roughly" correct, but miss out on a few points (the setting that [5, 4] studied). We believe that several of these extensions should be fairly straightforward to incorporate into the framework, and would mostly lead to additional complexity in notation and in the definition of various parameters. But a complete and principled treatment would be an interesting direction for future work.

## References

[1] E. Agichtein, E. Brill, S. Dumais, and R. Ragno. Learning user interaction models for predicting web search result preferences. In **Proc. 29th Intl. Conf. on Research and Development in**
Information Retrieval (SIGIR)**, pages 3–10, 2006.**
[2] D. Angluin. Queries and concept learning. Machine Learning**, 2:319–342, 1988.** [3] D. Angluin. Computational learning theory: Survey and selected bibliography. In **Proc. 24th**
ACM Symp. on Theory of Computing**, pages 351–369, 1992.**
[4] P. Awasthi, M.-F. Balcan, and K. Voevodski. Local algorithms for interactive clustering.

Journal of Machine Learning Research**, 18:1–35, 2017.**
[5] P. Awasthi and R. B. Zadeh. Supervised clustering. In Proc. 22nd Advances in Neural Information Processing Systems**, pages 91–99. 2010.**
[6] M.-F. Balcan and A. Blum. Clustering with interactive feedback. In **Proc. 19th Intl. Conf. on**
Algorithmic Learning Theory**, pages 316–328, 2008.**
[7] R. Bubley. Randomized Algorithms: Approximation, Generation, and Counting**. 2001.**
[8] R. Bubley and M. Dyer. Faster random generation of linear extensions. **Discrete mathematics**,
201(1):81–88, 1999.

[9] K. Crammer and Y. Singer. Pranking with ranking. In Proc. 14th Advances in Neural Information Processing Systems**, pages 641–647, 2002.**
[10] E. Emamjomeh-Zadeh, D. Kempe, and V. Singhal. Deterministic and probabilistic binary search in graphs. In Proc. 48th ACM Symp. on Theory of Computing**, pages 519–532, 2016.**
[11] M. Huber. Fast perfect sampling from linear extensions. Discrete Mathematics**, 306(4):420–428,**
2006.

[12] T. Joachims. Optimizing search engines using clickthrough data. In **Proc. 8th Intl. Conf. on**
Knowledge Discovery and Data Mining**, pages 133–142, 2002.**
[13] R. M. Karp. Reducibility among combinatorial problems. In Complexity of Computer Computations**, pages 85–103. 1972.**
[14] A. Karzanov and L. Khachiyan. On the conductance of order Markov chains. Order**, 8(1):7–15,**
1991.

[15] N. Littlestone. Learning quickly when irrelevant attributes abound: A new linear-threshold algorithm. Machine Learning**, 2:285–318, 1988.**
[16] W. Maass and G. Tur´an. On the complexity of learning from counterexamples and membership queries. In Proc. 31st IEEE Symp. on Foundations of Computer Science**, pages 203–210, 1990.**
[17] W. Maass and G. Tur´an. Lower bound methods and separation results for on-line learning models. Machine Learning**, 9(2):107–145, 1992.**
[18] W. Maass and G. Tur´an. Algorithms and lower bounds for on-line learning of geometrical concepts. Machine Learning**, 14(3):251–269, 1994.**
[19] F. Radlinski and T. Joachims. Query chains: Learning to **rank from implicit feedback. In**
Proc. 11th Intl. Conf. on Knowledge Discovery and Data Mining**, pages 239–248, 2005.**
[20] N. Sauer. On the density of families of sets. **Journal of Combinatorial Theory, Series A**,
13(1):145–147, 1972.

[21] S. Shelah. A combinatorial problem; stability and order for models and theories in infinitary languages. Pacific Journal of Mathematics**, 41(1):247–261, 1972.**
[22] K. L. Wagstaff. Intelligent Clustering with Instance-Level Constraints**. PhD thesis, 2002.**