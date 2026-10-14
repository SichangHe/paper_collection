                                                                           Graph Representations for Higher-Order
                                                                                Logic and Theorem Proving
                                                        Aditya Paliwal∗                                Sarah Loos                          Markus Rabe
                                                        Google Research                             Google Research                       Google Research
                                                     adipal@google.com                           smloos@google.com                      mrabe@google.com

                                                                       Kshitij Bansal                                     Christian Szegedy
                                                                       Google Research                                     Google Research
                                                                      kbk@google.com                                    szegedy@google.com
arXiv:1905.10006v2 [cs.LG] 13 Sep 2019




                                                                     Abstract                                 for model architectures that show non-trivial understanding
                                                                                                              of higher-order logic is thus wide-open.
                                           This paper presents the first use of graph neural networks
                                           (GNNs) for higher-order proof search and demonstrates that            In this work, we explore the use of the tree struc-
                                           GNNs can improve upon state-of-the-art results in this do-         ture (e.g. the abstract syntax tree) of logic expressions for
                                           main. Interactive, higher-order theorem provers allow for          learning representations. Most earlier works in this area
                                           the formalization of most mathematical theories and have           used TreeRNNs with the idea that the embedding of each
                                           been shown to pose a significant challenge for deep learning.      node needs to summarize the semantics of the subexpres-
                                           Higher-order logic is highly expressive and, even though it is     sion. However, TreeRNNs (and likewise sequence mod-
                                           well-structured with a clearly defined grammar and seman-          els such as LSTMs) have not shown strong performance
                                           tics, there still remains no well-established method to con-
                                           vert formulas into graph-based representations. In this paper,
                                                                                                              gains over baselines on logical reasoning tasks. We believe
                                           we consider several graphical representations of higher-order      this is because TreeRNNs fail to consider the context of
                                           logic and evaluate them against the HOList benchmark for           subexpressions—when computing the embedding of an in-
                                           higher-order theorem proving.                                      ternal node in the syntax tree, TreeRNNs only consider the
                                                                                                              embeddings of its child-nodes, but never the parent.
                                                               1     Introduction                                In this paper, we consider the syntax trees of formulas
                                                                                                              as graphs, where each node has edges to its children and
                                         Mathematics poses a particularly attractive learning chal-           also to its parent(s), and apply message-passing graph neu-
                                         lenge, as it can be seen as a test-bed for general-purpose rea-      ral networks (GNNs) (Scarselli et al. 2009; Li et al. 2015;
                                         soning. HOList (Bansal et al. 2019) is a recently published          Gilmer et al. 2017; Wu et al. 2019) instead of TreeRNNs.
                                         learning environment for mathematics consisting of a state-          We focus on imitation learning, i.e. learning from human
                                         less theorem proving API, a benchmark consisting of over             proofs. The proofs we learn from in the HOList dataset
                                         twenty thousand mathematical theorems and their proofs,              were written by human mathematicians interacting with a
                                         and a neural theorem prover called DeepHOL. It builds on             computer-based theorem prover. To ensure that we make
                                         HOL Light (Harrison 1996), an interactive theorem prover             meaningful progress, we evaluate all our models by mea-
                                         that has been used to formalize several mathematical theo-           suring how many theorems they manage to prove when in-
                                         ries, including topology, multivariate calculus, real and com-       tegrated with the DeepHOL neural theorem prover. In Sec-
                                         plex analysis, geometric algebra, measure theory and the Ke-         tion 5 we find that GNNs significantly improve performance,
                                         pler conjecture (Hales et al. 2017). The HOList environment          and achieve state-of-the-art performance for higher-order
                                         and benchmark allows us to measure progress in automated             logic proof search by a wide margin. Our best model au-
                                         mathematical reasoning, in particular for machine learning           tomatically proves nearly 50% of theorems in the validation
                                         techniques.                                                          set.
                                            The percentage of theorems that can be proven automat-
                                         ically by the neural theorem prover DeepHOL presented                   We present and compare several graph representations
                                         by Bansal et al. (2019) appears to be comparable with state-         for higher-order logic (Section 3) and suggest a sim-
                                         of-the-art algorithms in higher-order reasoning, which typi-         ple, message-passing, GNN architecture (Section 4.1). We
                                         cally build on advanced backtracking search algorithms and           demonstrate that minor changes in graph representations
                                         special-purpose proof calculi (Kaliszyk and Urban 2014;              can have significant effects on the performance of message
                                         Bentkamp et al. 2018). While these results were very                 passing GNNs. We additionally confirm our hypothesis that
                                         promising, the reference models presented by (Bansal et al.          the context of subexpressions is crucial, by first restricting
                                         2019) are still relatively naive—in fact we show that we can         GNNs to pass messages only upwards in the syntax tree
                                         beat their best models with a bag-of-words model. The quest          (similar to TreeRNNs), and, second, to pass messages only
                                                                                                              downwards in the syntax tree. The experiment clearly shows
                                            ∗
                                                Google AI Resident                                            that the second approach, which emphasizes the context of
expressions, outperforms the first.                                Hales et al. 2017) were performed using interactive proof
                                                                   assistants like Coq and HOL Light (Harrison 1996), which
                    2   Related Work                               are based on higher order logic (in which quantification
Graph Neural Network (GNN) is an umbrella term for                 over arbitrary propositions is allowed). However, the au-
several kinds of neural networks that operate on graph-            tomation of higher-order theorem proving, especially at the
structured data (Wu et al. 2019; Gilmer et al. 2017; Xu et         tactic level, is a more recent research area. Deep learning
al. 2019). This family of neural networks has been success-        has made inroads into various types of logic reasoning, for
fully applied in several domains ranging from computer vi-         example to guide SAT solvers (Selsam and Bjørner 2019),
sion (Raposo et al. 2017; Santoro et al. 2017), to predict-        QBF solvers (Lederman, Rabe, and Seshia 2018), and for
ing properties of molecules (Gilmer et al. 2017), to traffic       inductive reasoning (Dong et al. 2019).
prediction (Li et al. 2017). (Battaglia et al. 2018) show that        Many authors have used TreeRNN (or TreeLSTM) archi-
GNNs are capable of manipulating structured knowledge in           tectures to encode logical statements based on their abstract
the data and hence are a natural choice to learn meaningful        syntax tree representations (Evans et al. 2018; Huang et al.
representations for higher-order logic.                            2018; Loos et al. 2017). While this seems like a natural way
   Similar to our work, Wang et al. (2017) apply GNNs to           to encode tree-structured data, this approach greatly restricts
higher-order logic; they use graph representations of higher-      the flow of information across the tree, especially between
order logic formulas for premise selection, resulting in a         siblings. TreeRNNs enforce the property that a subexpres-
significant improvement in prediction accuracy. Our work           sion will always have the same embedding, regardless of the
extends their contributions by using GNNs not only for             context in which the expression appears. While this has com-
premise selection, but for predicting tactics and tactic argu-     putational advantages, as it allows embeddings of subex-
ments at every step of the proof. While the difference seems       pressions to be cached, it may also limit the ability of the
minor, it has a big effect on our contributions: it allows us to   network to effectively encode semantic information across
evaluate our models on a theorem proving benchmark where           (structurally) long distances.
we demonstrate that our models actually prove more theo-              Conversely, message-passing graph neural networks do
rems. Because Wang et al. (2017) only predict the premises         not have a single, static embedding for each subexpression,
at the theorem level, they can not generate each individual        but rather evolve embeddings for every node based on both
proof step, and are therefore not able to use their models to      its children and parents. Perhaps more importantly, when
generate proofs; instead they use a proxy metric that mea-         the graph representation allows subexpression sharing, these
sures against existing human proofs. We are able to provide        embeddings can draw on context from multiple occurrences.
end-to-end metrics on the percentage of theorems from the          Our experimental results clearly demonstrate the importance
validation set that can be proved using our models. This en-       of subexpression sharing.
sures that our models are learning something useful about
mathematics instead of learning to exploit syntactic tricks               3    Graph Representations of HOL
on the data.
   Our findings also differ from the results of Wang et            In this section we describe our graph representations of
al. (2017) in a crucial aspect: we found that representa-          higher-order logic (HOL) terms. The HOList benchmark
tions that share sub-expressions are significantly stronger        provides its data in the form of S-expressions. For example,
than representations that use tree representations. Our graph      the term f (x), which applies a variable f to another variable
representation allows for more sharing between expressions,        x, is represented as the following string: (a (v (fun A
as we merge variable nodes, even if they belong to different       B) f) (v A x))). The S-expression breaks the func-
binders. Also, our representation includes all type informa-       tion application down into fundamental elements, which we
tion and has a special node for function applications, which       explain in the following: The token a indicates a function
allows us to treat variables, abstractions, and quantifiers in a   application, which always has two children; the function to
uniform way.                                                       be applied and the argument. The token v indicates that the
   Similar to this work, GamePad (Huang et al. 2018),              function to be applied is a variable. This variable is then de-
TacticToe (Gauthier, Kaliszyk, and Urban 2017), Coq-               scribed as having type fun A B (i.e. a function mapping
Gym (Yang and Deng 2019), and Proverbot9001 (Sanchez-              from some type A to some potentially different type B) and
Stern et al. 2019) use imitation learning on human proofs          having the name f. Similarly, the expression (v A x) de-
collected from the tactics-based higher-order provers Coq          scribes the argument of the function application as a variable
and HOL4.                                                          x with type A.
   We elected to use the HOList benchmark as opposed to               There are only a small number of these fundamental
the GamePad or CoqGym datasets as it spans a large variety         building blocks of HOList’s S-expressions: a for function
of mathematics. We additionally wanted to ensure that our          applications, v for variables, l for lambda expressions (also
models performed well when used to guide proof search,             called abstractions), c for constants, and some additional
which is made simple in HOList.                                    ones for type constructors such as fun. All other tokens are
   Traditionally, automated theorem provers were developed         names of either variables, constants, or types, of which there
for first order logic, as it is easier to create complete and      are around 1200 in the dataset. Even quantifiers have no spe-
sound provers for it. However, most of the serious human           cial treatment and are simply represented as functions, using
formalization efforts (Gonthier 2008; Gonthier et al. 2013;        the definition (∀) , λf. (f = λx. True).
                                            a
                                                                                                          a
                               c                        l                                       c                     l

                         fun           ∀        v                   a                                                 a
                                                                                           ∀        fun

                      fun    bool A                 x       a               v                                     a
                                                    c               v A         x                             c           v
                  A     bool
                                           fun          =       A       x                                 fun =               x

                                       fun          A                                               fun

                                   A       bool                                                bool               A

Figure 1: Comparison of two graph representations of ∀x : x = x. Types (e.g. fun, bool, and type variable A) are printed
in orange. Left: AST representation. Right: AST with subexpression sharing (edge labels ensure the left/right order of children
is preserved, but are omitted for readability in this figure). Sharing reduces the graph size from 27 nodes to 15; the amount of
sharing increases as the terms grow larger.


   That is, S-expressions essentially represent the abstract                           Leaf sharing is a middle ground between the very verbose
syntax tree of higher-order logic expressions. We consider                          AST representation and the aggressive graph reduction that
the abstract syntax tree (AST) as a graph with directional                          is subexpression sharing. Instead of merging nodes that rep-
edges, where each node has edges to its children and also to                        resent equal subexpressions, we only merge leaves with the
its parent(s). Edges are labeled with the index of the child,                       same token, such as A, bool, or x.
which makes the original string representation recoverable                             Variable blinding replaces all variable names by x. This
from the graph.                                                                     transformation is applied only after the graph is constructed
   In addition to the plain AST, we consider several mod-                           and does not modify the graph structure. Hence, different
ifications to the graph representations, which we study in                          variables still have different graph nodes and are thus distin-
Section 5:                                                                          guishable - just their names are the same. This allows us to
• We share nodes of syntactically equal subexpressions                              study how much our networks rely on variable names.
  (subexpression sharing).                                                             Restricting our graphs to only have top down edges or
                                                                                    only have bottom up edges allows us to study the question
• We share equal leaves of the AST (leaf sharing).                                  of how important the context of subexpressions is for their
• We replace all variable names by x (variable blinding).                           embeddings. Bottom up loosely resembles TreeRNNs, as it
                                                                                    computes its embeddings only from the embeddings of its
• We add random edges (random).                                                     children. Top down, on the other hand, disallows nodes to
• We remove all edges from nodes to their parents and only                          see their children, but allows them to see their context.
  keep those to their children (top down).                                             Adding random edges to the graph representation allows
                                                                                    us to study if additional connectivity helps the neural net-
• We remove all edges from nodes to their children and only
                                                                                    works to propagate information through the graphs. We
  keep those to their parents (bottom up).
                                                                                    chose to add 3 outgoing edges per node to random targets,
   Subexpression sharing merges all nodes in the AST that                           as this approximates the construction of expander graphs,
represent the same expression. In Figure 1 we illustrate the                        which provides excellent connectivity properties of the re-
difference between the abstract syntax tree representation                          sulting graph with little overhead. We label the random
with (right) and without (left) subexpression sharing. The                          edges to make them distinguishable from regular edges in
variable x of type A, which occurs three times in the ab-                           the graph.
stract syntax tree, now occurs only once. It is represented by
the S-expression (v x A), and the root node of this expres-                                          4    Model Architecture
sion now has three parents that keep track of the locations
of each of its original occurrences. Note that sub-expression                       In this section we present our neural network architec-
sharing also happens over types. In this example, variable x                        ture, starting with basics of message-passing GNNs in Sec-
has type A, so every other expression with type or sub-type                         tion 4.1, which we use for embedding statements in higher-
A is now connected through this node. For detailed statis-                          order logic. We then detail the prediction tasks necessary for
tics of how subexpression sharing compresses the data, see                          guiding proof search and our imitation learning approach,
Appendix A.1.                                                                       which trains on human proofs, in Section 4.2.
4.1   Graph Neural Networks                                      p using identical GNNs; GNN-1 and GNN-2 do not share
Graph neural networks (GNNs) compute embeddings for              weights. To make the architecture computationally tractable,
nodes in a graph via consecutive rounds (also called hops)       the depth of each node embedding is relatively small (128).
of end-to-end differentiable message passing. The input to       We do two 1x1 convolutions to expand the depth (to 512
a GNN is a labeled graph G = (V, E, lV , lE ) where V is a       and then to 1,024) immediately before max pooling, result-
set of nodes, E is a set of directed edges, lV maps nodes to     ing in a goal embedding and premise embedding, each of
a fixed vocabulary of tokens, and lE maps each edge e to a       size 1,024.
single scalar indicating if the edge is to (or from) the first      The tactic classifier selects from a fixed set of 41 tactics. It
or the second child, encoded as 0 and 1. Each token t in the     uses two fully connected layers, followed by a linear layer to
vocabulary is associated with a trainable feature vector xt .    produce logits for a softmax tactic classifier. The combiner
   The GNN computes node embeddings hv for each node             network concatenates the goal and premise embeddings,
v ∈ V via an iterative message passing process of T rounds:      as well as their element-wise multiplication, followed by
   1. Embed nodes n and edges e into high dimensional            three fully connected layers. The model uses sigmoid cross-
space using multi-layer perceptrons:                             entropy to score how useful an individual premise is for the
                                                                 given goal. It was important to apply dropout throughout the
                   h1v = MLPV (xlV (v) )                         network.
                    he = MLPE (lE (e))                              This architecture was trained on the proofs written by hu-
                                                                 mans and released in the HOList dataset. For evaluation, we
  2. For each round t ∈ {2, . . . , T }, and for each edge       plug the models into the breadth-first proof search provided
(u, v) = e ∈ E, pass the node embeddings from the pre-           by the HOList environment. We first start with the top level
vious step ht−1
             u  and ht−1
                      v   and the edge embedding he into         goal which is the top level theorem to be proved. To pro-
an MLP to generate messages. When computing the mes-             cess a goal (or “subgoals” for newly created goals), we ap-
sages for a node v, we distinguish between messages from         ply one of the tactics that may take a list of already proven
parent nodes su,v and from child nodes ŝu,v :                   theorems as parameters.1 Once a goal is set to be processed,
            stu,v = MLPtedge ([ht−1  t−1                         we pick the top-k1 highest scoring tactics from the softmax
                                u , hv , he ])
                                                                 tactic classifier (see Figure 3). Then the combiner network
                     ˆ t                                         is evaluated for each (g, pi ) pairs of the current goal g and
           ŝtu,v = MLP          t−1  t−1
                         edge ([hu , hv , he ])                  possible tactic parameter pi (which includes all the defini-
  3. To summarize the messages for node v ∈ V , we sum           tions and theorems preceding the top level goal in the theo-
over the messages from parents and from children separately      rem database). Note that this computation is accelerated sig-
before passing them through an MLP and adding them to the        nificantly by pre-computing the premise-embeddings P (pi ),
previous embedding:                                              and therefore only the combiner network has to be evaluated
                                                                 for each pair of embeddings G(g), P (pi )), where G(g) de-
                                 X stu,v X ŝtu,v            notes the goal embedding of the currently processed goal. In
   t      t−1                 t−1
  hv = hv + MLPaggr hv ,                    ,                    total, there are 19,262 theorems and definitions in the theo-
                                       p(v)       c(v)
                                                                 rem database. Only the top-k2 highest scoring premises are
   MLPV , MLPE , MLPtedge , MLP    ˆ t                           chosen as tactic arguments. In our setting, we used k1 = 5,
                                       edge and MLPaggr are
                                                                 k2 = 20.
multi-layer perceptrons, p(v) is the number of parents of
node v, c(v) is the number of children of node v [, ] is the        A tactic application might fail or may be successful.
vector concatenation operator, and htv represents the embed-     Failed applications are logged, but ignored for proof search.
ding of node v after t rounds of message passing. A multi-       If the tactic application is successful, it might close (that
layer perceptron (MLP), is a function MLP : Ra → Rb , that       is: prove) the goal or generate a new list of subgoals (or
maps vectors in the input space to the output space via suc-     proof obligations). The original goal is closed if each of its
cessive applications of linear transformations and non-linear    subgoals is closed. During proof search, the HOList proof-
activations.                                                     search graph maintains several alternative branches of sub-
   The final set of node embeddings returned by the Graph        goals to be closed. Proof search stops if the top-level goal
Neural Network is given by hv = hTv where T is the number        closes, that is if at least one of the alternative branches
of message passing rounds. These node embeddings repre-          closes.
sent information from the T -hop neighborhood of each node          Note that in contrast to earlier premise selection works,
in the graph. A single step of message passing over a single     we generate new tactic parameter lists for each subgoal dur-
node of a graph is shown in Figure 2.                            ing proof-search, not just a single list of premises for the
                                                                 top-level goal.
4.2   Complete Model Architecture
The full architecture is depicted in Figure 3. The network          1
                                                                      The interpretation of the tactic parameters depends on the type
takes the current goal (an intermediate state in a proof         of the tactic. For MESON TAC, these are premises that the tactic can
search) and a candidate premise.                                 use for proving the statement in HOL Light’s built-in first-order
   It then generates node embeddings G(g) and P (p) for          reasoning algorithm. For REWRITE TAC, these should be equa-
the graph representations of both the goal g and premise         tions that are applied for rewriting the goal statement.
             A                         C                                      A
                                                                              ’

                                                                              B

                                                                                                                         B
                                                                              C
                                                             MLP                             𝚺          ReLU
                                                                              D
                 B




                                   D




Figure 2: A single Graph Neural Network neighborhood aggregation step for node B. The features over the neighborhood are
passed through an MLP, followed by a summation and a non-linearity. The output that follows is the hidden feature for node B
for the next step.

                        Goal                       Premise
                                                                                  Table 1: Our best model, compared against previous state of
                                                                                  the art and bag of words model as baselines.
                       GNN-1                       GNN-2
                                                                                     Network Architecture                % Proofs Closed
                      Conv
                                                                                                                          (Validation Set)
                      Conv1x1
                           1x1                  Conv
                                                Conv1x1
                                                     1x1
                                                                                     Baseline: S-expression as a string
                     Max Pooling               Max Pooling
                                                                                     WaveNet (Bansal et al. 2019)                 32.65%
                 Goal Embedding             Premise Embedding                        Baseline: Bag of words
                                                                                     Max pooling only                             37.98%
                                                                                     Subexpression sharing
   Tactic Classifier            Combiner Network             Premise Scorer
                                                                                     12-hop GNN                                   49.95%

Figure 3: Diagram of the model architecture. At every step
of the proof, the current goal is embedded using GNN-1.                           5.1   Evaluation Metrics
Based on the goal embedding, the model predicts the next                          The primary way that we evaluate our models is by using
tactic to apply from a fixed set of 41 tactics. The goal embed-                   them to guide the proof search in the HOL Light theorem
dings are also used to score every preceding theorem, called                      prover, and then counting how many theorems each trained
premises. Premises are also embedded using a graph neural                         model can prove. However, it takes several hours to run the
network (GNN-2). Higher scores indicate the given premise                         prover on the validation set, even in a distributed manner.
is predicted to be useful for proving the current goal. Full                      If we were to use this metric during training, it would slow
details presented in Section 4.2.                                                 down training of our models by several orders of magnitude,
                                                                                  so we instead train using two proxy metrics:
                                                                                  • We look at the accuracy of the tactic prediction output,
                                                                                     which decides which one of the 41 possible tactics is to
                            5      Experiments                                       be applied for a given goal. It is often the case that more
                                                                                     than one choice of tactic would work, but to determine if
Here we present our experimental results on the HOList                               a tactic is correct, we would need to try it in the prover.
benchmark (Bansal et al. 2019), which is based on the com-                           Instead, for the proxy metric, we only count a tactic cor-
plex analysis corpus of HOL Light (Harrison 1996). The                               rect if it was the exact tactic applied in the human proof,
training set is derived from the proofs of 10,200 top-level                          as our data contains only a single proof per theorem.
theorems and has around 375,000 proof steps (subgoals) to                         • We monitor the relative prediction accuracy for the tactic
learn from. We have evaluated the end-to-end prover per-                             parameter selection, which is the ratio of cases in which a
formance on the standard validation split of HOList which                            true tactic parameter is scored higher than some randomly
consists of 3,225 held out theorems of the complex analysis                          sampled parameter. Again, there is often more than one
corpus.                                                                              “true parameter”, but we only consider the set of premises
   In total, there are 19,262 theorems and definitions in the                        that were used as tactic parameters in the human proof.
HOList corpus. These theorems are proved in a sequential                             We then perform the computationally expensive evalua-
order. So, for any given goal, all preceding theorems and                         tion only on the best checkpoint (according to the proxy
definitions in the corpus are eligible premises. For each tac-                    metrics): running the prover once over the validation set us-
tic application, we select the top 20 premises after ranking                      ing the parameterized tactics predicted by the checkpoint
the eligible premises with the premise scorer.                                    to guide proof search. This percentage of proofs closed in
Table 2: Percentage of proofs closed on the validation set. Representations are defined in Section 3. Two AST results indicated
with an asterisk (*) required a smaller batch size due to memory constraints.
              Representation                                0 Hops 2 Hops 4 Hops             8 Hops     12 Hops
              Abstract syntax trees (AST)                   40.18% 43.84% 44.58% 46.66%∗ 45.67%∗
              Leaf sharing                                  41.76% 33.89% 29.24% 29.51%                  30.51%
              Leaf sharing + variable blinding              31.78% 32.18% 32.80% 30.04%                  31.00%
              Subexpression sharing                         40.86% 42.94% 46.94% 47.22%                 49.95%
              Subexpression sharing + variable blinding 31.75% 34.44% 35.96% 34.07%                      37.36%
              Subexpression sharing + random                41.24% 43.68% 43.84% 42.63%                  42.94%
              Subexpression sharing + top down              40.55% 43.59% 45.51% 48.24%                  48.40%
              Subexpression sharing + bottom up             39.72% 40.58% 41.16% 41.86%                  40.99%


the validation set is the primary metric that we use to es-       acyclic graph, so we can experiment with restricting mes-
tablish the proving power of a given checkpoint. It evaluates     sage passing to flow only from children to parents (bottom
whether a trained model is effective at automatically proving     up), or from parents to children (top down). While allowing
newly encountered theorems.                                       information to flow in both directions results in the best per-
                                                                  formance, Table 2 shows that top down message passing sig-
5.2   Results and Analysis                                        nificantly outperforms bottom up. This experiment demon-
We train several models using the architecture described in       strates that the context of all the places a subexpression oc-
Section 4.2, varying the number of message passing rounds         curs in the larger formula may be more important than the
in the GNN and the representation of the higher-order logic       value of the subexpression itself. It’s worth noting that this is
formulas as graphs as described in Section 3.                     opposite the bottom up direction of information flow used in
   We compare our best-performing model against baselines         TreeRNNs, where information starts at the leaves and then is
in Table 1. Our 12-hop shared subexpression GNN achieves          propagated to the root. However, our neural networks have
the state-of-the-art result on the HOList benchmark, clos-        the benefit of aggregating over all nodes in the graph after
ing 49.95% of the proofs. This is a major improvement on          message passing is complete, a step not taken in TreeRNNs.
the baseline models in the HOList paper (32.65%) and even            While leaf sharing had the effect of compressing the tree
outperforms the reported 38.9% of their best reinforcement        representations by approximately 40%, this representation
learning experiment. We also observe that a simple bag-of-        also incurred a large drop in performance. Most notably, leaf
words model with large word embedding sizes also manages          sharing models which used message passing were well be-
to close 37.98% of all proofs. The GNN models with zero           low the 0-hop baseline in all cases. This result demonstrates
message passing steps (0 Hops) are roughly equivalent to          the huge impact the representation has on the GNN perfor-
the bag of words max pooling model, except that the 0 Hops        mance.
models also have additional MLPs between the word em-                Analyzing only the best-performing representation
bedding lookup step and the max pooling step.                     (subexpression sharing, indicated in bold), we find that
   In Table 2 we can see that the number of proofs closed         models with more hops not only close more proofs, but
increases with additional hops (message passing steps) for        also find slightly longer proofs on average (1.93 steps for
ASTs with and without subexpression sharing. This in-             12-hops vs 1.86 for 0-hops). Another indicator that the
dicates that additional information about the structure of        quality of the choices made by GNNs increases with with
higher-order logic formulas provides the model with the ca-       the number of hops is that the percentage of successful
pacity to learn better embeddings.                                tactic applications increased from 33.8% for 0-hops, to
   Variable blinding, which initializes every token represent-    38.6% for 12-hops.
ing a variable name to the same (trained) embedding, al-
lows us to evaluate the importance of human-assigned vari-        5.3    Implementation Details
able names. Even though constant values are not altered and       In this section, we describe our implementation and hard-
the expressions remain semantically equivalent after vari-        ware setup, including hyper-parameter settings and a more
able blinding, removing variable names causes a significant       detailed description of the losses we used. These hyper-
drop in performance. This suggests that human-chosen vari-        parameters did not vary between experiments unless other-
able names are important and should not be discarded, even        wise noted, and are presented here to aid reproducibility.
when the resulting formula is semantically equivalent.
   The graph representation with random edges improves the
performance of the 2-hop network, but not for networks with       Choosing Negative Examples. For each theorem in the
four or more hops. This suggests that the addition of random      HOList training set, there is only one human proof. We gen-
edges increases the field-of-view into the graph for the net-     erate positive training examples from each step of the human
works, but the benefits diminish and ultimately are harmful       proof with three values: the goal that is being proved at that
for networks with more hops.                                      step, the tactic applied to it, and a list of theorem parameters
   Subexpression sharing on ASTs results in a directed            passed to the tactic (or a special token if no parameters were
used). To generate positive (goal, premise) pairs, we sam-          Section 4.1. MLPedge , MLP  ˆ
                                                                                                  edge and MLPaggr have an
ple a premise from this list of theorem parameters. In each         identical configuration with two layers, with hidden sizes
batch, we sample 16 positive (goal, premise) pairs from our         256 and 128 and ReLU activations. The MLPs do not share
training data.                                                      weights across message passing steps. The final node em-
   Because we only have successful human proofs, we se-             bedding has size 128. A dropout of 0.5 is applied to all
lect our negative training examples by sampling uniformly           MLPs.
from the set of all theorems that were used at least once as           The node embeddings hv returned by the graph neu-
positive training examples. Every goal in the batch is then         ral network are then aggregated into a single vector that
paired with 15 randomly sampled theorems and labeled as             represents the embedding of the entire graph. Using two
negative examples (adding 15x16=240 negative examples to            Conv 1 × 1 layers, we expand the 128 dimensional node em-
the batch).                                                         beddings to 512, and then 1024, with ReLU activations and
   Since the combiner network is quite small relative to            a dropout rate of 0.5. Then we perform max pooling over all
the GNN embedding networks, we reuse all 256 embed-                 node embeddings to create a single vector of size 1024.
ded premises (positive and negative) as negative premise
examples for the remaining goals in the batch (adding
15x256=3,840 negative examples to the batch), giving a to-          Hardware. We used eight NVIDIA Tesla V100 GPUs for
tal batch size of 4,096.                                            distributed training, an additional GPU was used purely for
                                                                    evaluation, and we maintained a separate parameter server
                                                                    on a CPU machine.
Loss Functions. In addition to the cross-entropy loss for
both tactics and pairwise scores as described in Section 4,
we also use the AUCROC loss (Burges et al. 2005; Eban                        6    Conclusions and Future Work
et al. 2017) to directly relate positive and negative premise       We present the first use of graph neural networks to guide
examples within a batch. The AUCROC loss minimizes the              higher-order theorem proving. We experiment with sev-
area under the ROC curve and is implemented as follows.             eral graph representations of higher-order logic expressions
                         XX                                         and demonstrate that graph neural networks can signifi-
        AU CROCb =               loss(logiti − logitj )             cantly improve over non-structured representations, espe-
                          i   j                                     cially when the structure of the graph allows for sharing of
                                                                    sub-expressions. We observed that increasing the number of
                    loss(l) = ln(1 + e−l )                          message passing steps resulted in improved accuracy on the
Where i ranges over the positive premises in batch b, and           training and evaluation sets, and also led to a larger percent-
j ranges over the negatives in b. Because our final predic-         age of closed proofs. Using GNNs, we are able to signifi-
tion task is to rank premises for just one given goal, we           cantly improve previous state-of-the-art results for imitation
double the loss for logits that compare positive and negative       learning on the HOList theorem set and proof search envi-
premises for the same goal.                                         ronment.
   For the total loss, we take a weighted sum of the cross-            In the experiments presented in this paper, we predict tac-
entropy loss on the tactic classifier (weight = 1.0), the cross-    tics and their arguments by looking only at the conclusion of
entropy loss on the pairwise scorer (weight = 0.2), and the         the current sub-goal and ignoring any local assumptions that
AUCROC loss (weight = 4.0).                                         could be crucial to the proof. This is a serious limitation for
                                                                    our system, and in future work we would like to include the
Optimizers, Learning Rate, Dropout, and Polyak Aver-                local assumptions list when generating the embedding of the
aging. For training, we use an Adam Optimizer (Kingma               goal. We expect this to be a natural extension for GNNs, be-
and Ba 2014) with initial learning rate 0.0001 and decay            cause they can easily extend graph representations to include
rate 0.98. Excluding the two GNNs, dropout is added before          additional expressions.
every dense layer of the network with a “keep probability”
of 0.7. For our evaluation checkpoints, we also use moving                                   References
exponential parameter averaging with rate 0.9999 per step          [Bansal et al. 2019] Bansal, K.; Loos, S. M.; Rabe, M. N.;
(Polyak 1990; Polyak and Juditsky 1992).                            Szegedy, C.; and Wilcox, S. 2019. Holist: An environ-
                                                                    ment for machine learning of higher-order theorem proving.
GNN Hyperparameters. The token features xt are train-               ICML 2019. International Conference on Machine Learn-
able embedding vectors of size 128. The edge labels lE (e)          ing.
are non-trainable binary values {0, 1} which indicate if the       [Battaglia et al. 2018] Battaglia, P. W.; Hamrick, J. B.; Bapst,
edge connects a left child or the right child. The graph neu-       V.; Sanchez-Gonzalez, A.; Zambaldi, V. F.; Malinowski,
ral network begins by projecting the node features xlV (v)          M.; Tacchetti, A.; Raposo, D.; Santoro, A.; Faulkner, R.;
and edge features lE (e) to vectors of size 128 using an            Gülçehre, Ç.; Song, F.; Ballard, A. J.; Gilmer, J.; Dahl, G. E.;
MLP with two hidden layers of sizes 256 and 128 with                Vaswani, A.; Allen, K.; Nash, C.; Langston, V.; Dyer, C.;
ReLU activations (MLPV and MLPE ). The resulting em-                Heess, N.; Wierstra, D.; Kohli, P.; Botvinick, M.; Vinyals,
beddings are denoted by h1v and he . We then perform t              O.; Li, Y.; and Pascanu, R. 2018. Relational inductive biases,
rounds of message passing as per the equations shown in             deep learning, and graph networks. CoRR abs/1806.01261.
[Bentkamp et al. 2018] Bentkamp, A.; Blanchette, J. C.;           automated reasoning through deep reinforcement learning.
 Cruanes, S.; and Waldmann, U. 2018. Superposition for            CoRR abs/1807.08058.
 lambda-free higher-order logic. In Galmiche, D.; Schulz,        [Li et al. 2015] Li, Y.; Tarlow, D.; Brockschmidt, M.; and
 S.; and Sebastiani, R., eds., Automated Reasoning, 28–46.        Zemel, R. 2015. Gated graph sequence neural networks.
 Cham: Springer International Publishing.                         arXiv preprint arXiv:1511.05493.
[Burges et al. 2005] Burges, C.; Shaked, T.; Renshaw, E.;        [Li et al. 2017] Li, Y.; Yu, R.; Shahabi, C.; and Liu, Y. 2017.
 Lazier, A.; Deeds, M.; Hamilton, N.; and Hullender, G. N.        Graph convolutional recurrent neural network: Data-driven
 2005. Learning to rank using gradient descent. In Pro-           traffic forecasting. CoRR abs/1707.01926.
 ceedings of the 22nd International Conference on Machine
                                                                 [Loos et al. 2017] Loos, S.; Irving, G.; Szegedy, C.; and
 learning (ICML-05), 89–96.
                                                                  Kaliszyk, C. 2017. Deep network guided proof search.
[Dong et al. 2019] Dong, H.; Mao, J.; Lin, T.; Wang, C.; Li,      LPAR-21. 21st International Conference on Logic for Pro-
 L.; and Zhou, D. 2019. Neural logic machines. ICLR 2019.         gramming, Artificial Intelligence and Reasoning.
 International Conference on Learning Representations.
                                                                 [Polyak and Juditsky 1992] Polyak, B. T., and Juditsky, A. B.
[Eban et al. 2017] Eban, E. E.; Schain, M.; Mackey, A.; Gor-      1992. Acceleration of stochastic approximation by averag-
 don, A.; Saurous, R. A.; and Elidan, G. 2017. Scalable           ing. SIAM Journal on Control and Optimization 30(4):838–
 learning of non-decomposable objectives. Proceedings of          855.
 the 20th International Conference on Artificial Intelligence
 and Statistics (AISTATS).                                       [Polyak 1990] Polyak, B. T. 1990. A new method of stochas-
                                                                  tic approximation type. Avtomatika i telemekhanika 7:98–
[Evans et al. 2018] Evans, R.; Saxton, D.; Amos, D.; Kohli,       107.
 P.; and Grefenstette, E. 2018. Can neural networks under-
 stand logical entailment? ICLR 2018. International Confer-      [Raposo et al. 2017] Raposo, D.; Santoro, A.; Barrett, D.
 ence on Learning Representations.                                G. T.; Pascanu, R.; Lillicrap, T. P.; and Battaglia, P. W. 2017.
                                                                  Discovering objects and their relations from entangled scene
[Gauthier, Kaliszyk, and Urban 2017] Gauthier,             T.;    representations. CoRR abs/1702.05068.
 Kaliszyk, C.; and Urban, J. 2017. Tactictoe: Learning
 to reason with hol4 tactics. In LPAR-21. 21st Interna-          [Sanchez-Stern et al. 2019] Sanchez-Stern, A.; Alhessi, Y.;
 tional Conference on Logic for Programming, Artificial           Saul, L. K.; and Lerner, S. 2019. Generating correctness
 Intelligence and Reasoning, volume 46, 125–143.                  proofs with neural networks. CoRR abs/1907.07794.
[Gilmer et al. 2017] Gilmer, J.; Schoenholz, S. S.; Riley,       [Santoro et al. 2017] Santoro, A.; Raposo, D.; Barrett, D.
 P. F.; Vinyals, O.; and Dahl, G. E. 2017. Neural message         G. T.; Malinowski, M.; Pascanu, R.; Battaglia, P.; and Lil-
 passing for quantum chemistry. CoRR abs/1704.01212.              licrap, T. P. 2017. A simple neural network module for
                                                                  relational reasoning. CoRR abs/1706.01427.
[Gonthier et al. 2013] Gonthier, G.; Asperti, A.; Avigad, J.;
 Bertot, Y.; Cohen, C.; Garillot, F.; Roux, S. L.; Mah-          [Scarselli et al. 2009] Scarselli, F.; Gori, M.; Tsoi, A. C.; Ha-
 boubi, A.; O’Connor, R.; Biha, S. O.; Pasca, I.; Rideau, L.;     genbuchner, M.; and Monfardini, G. 2009. The graph neu-
 Solovyev, A.; Tassi, E.; and Théry, L. 2013. A machine-         ral network model. IEEE Transactions on Neural Networks
 checked proof of the Odd Order Theorem. In ITP, 163–179.         20(1):61–80.
[Gonthier 2008] Gonthier, G. 2008. Formal proof–the four-        [Selsam and Bjørner 2019] Selsam, D., and Bjørner, N.
 color theorem. Notices of the AMS 55(11):1382–1393.              2019. Guiding high-performance sat solvers with unsat-core
                                                                  predictions. SAT 2019, The 22nd International Conference
[Hales et al. 2017] Hales, T.; Adams, M.; Bauer, G.; Dang,
                                                                  on Theory and Applications of Satisfiability Testing.
 T. D.; Harrison, J.; Le Truong, H.; Kaliszyk, C.; Magron,
 V.; McLaughlin, S.; Nguyen, T. T.; et al. 2017. A formal        [Wang et al. 2017] Wang, M.; Tang, Y.; Wang, J.; and Deng,
 proof of the kepler conjecture. In Forum of Mathematics,         J. 2017. Premise selection for theorem proving by deep
 Pi, volume 5. Cambridge University Press.                        graph embedding. In Advances in Neural Information Pro-
                                                                  cessing Systems, 2786–2796.
[Harrison 1996] Harrison, J. 1996. HOL Light: A tutorial
 introduction. In FMCAD, 265–269.                                [Wu et al. 2019] Wu, Z.; Pan, S.; Chen, F.; Long, G.; Zhang,
                                                                  C.; and Yu, P. S. 2019. A comprehensive survey on graph
[Huang et al. 2018] Huang, D.; Dhariwal, P.; Song, D.; and
                                                                  neural networks. CoRR abs/1901.00596.
 Sutskever, I. 2018. Gamepad: A learning environment for
 theorem proving. ICLR 2018. International Conference on         [Xu et al. 2019] Xu, K.; Hu, W.; Leskovec, J.; and Jegelka, S.
 Learning Representations.                                        2019. How powerful are graph neural networks? ICLR 2019.
                                                                  International Conference on Learning Representations.
[Kaliszyk and Urban 2014] Kaliszyk, C., and Urban, J.
 2014. Learning-assisted automated reasoning with flyspeck.      [Yang and Deng 2019] Yang, K., and Deng, J. 2019. Learn-
 Journal of Automated Reasoning 53(2):173–213.                    ing to prove theorems via interacting with proof assistants.
[Kingma and Ba 2014] Kingma, D. P., and Ba, J. 2014.              CoRR abs/1905.09381.
 Adam: A method for stochastic optimization. arXiv preprint
 arXiv:1412.6980.
[Lederman, Rabe, and Seshia 2018] Lederman, G.; Rabe,
 M. N.; and Seshia, S. A. 2018. Learning heuristics for
                               A    Appendix
A.1            Statistics over the Theorem Database
We analyzed how much the different graph representations
affect the graph size. Below we present a histogram of the
number of nodes of all the theorems in the HOList theorem
database. We can see that the shared subexpression repre-
sentation leads to a significant reduction in graph sizes. It is
noteworthy that it almost eliminates the tail of the distribu-
tion.
             3000
                                                                  shared subexp.
             2500                                                 leaf sharing
                                                                  AST
             2000
 frequency




             1500

             1000

              500

                0
                    0    100            200            300          400        500
                        nodes in different graph representations
   We also measured the maximal path length from the root
node of the graphs, which we call depth. The data indicates
that the 12 hops that our best graph neural networks do are
not really really sufficient to propagate information from all
leafs to the root node, or vice versa. Models with even more
hops might therefore help to increase the performance fur-
ther.
             1400
             1200
             1000
 frequency




              800
              600
              400
              200
                0
                    0   10         20          30            40        50          60
                                              depths
