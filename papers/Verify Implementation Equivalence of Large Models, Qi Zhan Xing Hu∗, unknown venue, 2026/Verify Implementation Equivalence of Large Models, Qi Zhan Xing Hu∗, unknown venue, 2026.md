                                                        Verify Implementation Equivalence of Large Models
                                                                         Qi Zhan                                                                Xing Hu∗
                                             The State Key Laboratory of Blockchain and Data Security,               The State Key Laboratory of Blockchain and Data Security,
                                                               Zhejiang University                                                     Zhejiang University
                                                                Hangzhou, China                                                         Hangzhou, China
                                                               qizhan@zju.edu.cn                                                       xinghu@zju.edu.cn

                                                                         Xin Xia                                                              Shanping Li
                                             The State Key Laboratory of Blockchain and Data Security,               The State Key Laboratory of Blockchain and Data Security,
                                                               Zhejiang University                                                     Zhejiang University
                                                                Hangzhou, China                                                         Hangzhou, China
arXiv:2603.21851v1 [cs.SE] 23 Mar 2026




                                                                xin.xia@acm.org                                                         shan@zju.edu.cn

                                         Abstract                                                                     of determining whether such implementations realize the same
                                         Verifying whether two implementations of the same large model                mathematical function as Implementation Equivalence.
                                         are equivalent across frameworks is difficult in practice. Even when             When implementation equivalence does not hold, it often leads
                                         they realize the same computation, their graphs may differ substan-          to silent bugs: they do not trigger crashes or exceptions, but instead
                                         tially in operator decomposition, tensor layout, and the use of fused        produce incorrect intermediate tensors or outputs during normal
                                         or opaque kernels, making manual rewrite rules hard to build and             execution [13]. Such failures have been observed in production ML
                                         maintain. We present Emerge, a framework for checking Implemen-              frameworks, including incorrect loss scaling in Megatron-LM and
                                         tation Equivalence over computation graphs of large-model imple-             output mismatches in vLLM caused by implementation bugs in
                                         mentations. Instead of writing rules manually, Emerge represents             components such as split-QKV handling and RoPE [4, 19, 29, 30].
                                         the two implementations in an e-graph, infers candidate relations                Existing research has focused on equivalence checking for deep
                                         from execution values, and synthesizes rewrite rules on demand               learning systems, particularly in the setting of Parallel Equiva-
                                         when existing rules are insufficient. Each synthesized rule is vali-         lence [12, 16, 31, 39]. In this setting, the goal is to verify that dis-
                                         dated using the strongest applicable method, including SMT-based             tributed execution strategies, such as tensor sharding or data par-
                                         checking for symbolically tractable cases and constraint-aware ran-          allelism, preserve the semantics of a reference implementation.
                                         domized testing for opaque kernels, and then propagated through              However, verifying implementation equivalence beyond the paral-
                                         e-graph rebuilding to establish larger equivalences. Our current im-         lel setting remains under-explored. For instance, the HuggingFace
                                         plementation targets inference computation graphs captured from              Transformers library [33] provides reference implementations of
                                         HuggingFace Transformers and vLLM. Our evaluation shows that                 state-of-the-art models, while vLLM [14] offers highly optimized im-
                                         Emerge establishes equivalence for correct implementation pairs              plementations. Although these frameworks target the same model
                                         at practical cost, while also providing useful by-products for de-           architectures, their implementations can differ substantially in com-
                                         bugging: it detects 10 of 13 known implementation bugs, uncovers             putation graphs, tensor layouts, and kernel-level execution.
                                         8 previously unknown implementation issues that were later con-                  Recent work has explored equality saturation and e-graphs for
                                         firmed by developers. In addition, Emerge synthesizes high-level             proving equivalence in deep learning systems [31, 38, 39]. These ap-
                                         rules that compare favorably with manually authored ones.                    proaches construct a unified representation of computation graphs
                                                                                                                      and iteratively apply human-defined rewrite rules to establish equiv-
                                                                                                                      alence. However, such manually authored rewrite rules are typi-
                                         1    Introduction
                                                                                                                      cally tailored to parallel-equivalence transformations and do not
                                         Deep learning deployment today relies on a diverse ecosystem of              transfer easily to cross-framework model implementations. Unlike
                                         reference frameworks, compiler stacks, and high-performance serv-            parallel-equivalence settings, where equivalence often follows from
                                         ing systems, such as HuggingFace Transformers, XLA, TVM/Ansor,               a relatively structured set of partitioning and aggregation transfor-
                                         and vLLM [5, 14, 18, 33, 35, 37]. As a result, the same model archi-         mations, cross-framework model implementations introduce two
                                         tecture is often realized by multiple implementations, optimized             additional challenges:
                                         for serving efficiency or specific hardware targets. However, these              Challenge 1: Divergent Implementation Paths. Even when
                                         implementations are not guaranteed to be equivalent. Even when               mathematically equivalent, two implementations may use differ-
                                         derived from the same high-level model specification, they may               ent operator decompositions, execution plan, and tensor layouts [10,
                                         differ substantially in computation graphs, operator decomposi-              34]. For example, GPT-2 [21]’s linear projection is realized as addmm
                                         tions, tensor layouts, and low-level kernels. We refer to the problem        in the Transformers but as linear in vLLM, with the weight tensor
                                         ∗ Corresponding Author
                                                                                                                      stored in a transposed layout and the surrounding execution plan
                                                                                                                      organized differently. As a result, the corresponding computation
                                                                                                                      graphs can differ substantially in structure, making it impractical
                                         Conference’17, Washington, DC, USA
                                         2026. ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM                                     to manually encode rewrite rules for every such divergence.
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                 1
Conference’17, July 2017, Washington, DC, USA                                                                 Qi Zhan, Xing Hu, Xin Xia, and Shanping Li


    Challenge 2: Opaque Semantics of Custom Kernels. Cus-                     to validity and limitations in Section 6, review related work in
tom kernels make equivalence checking difficult because their se-             Section 7, and conclude in Section 8.
mantics are often not explicit at the computation-graph level. To
maximize inference-time performance, modern frameworks rely                   2   Emerge in a Nutshell
heavily on such operators, often implemented as fused CUDA ker-
                                                                              In this section, we provide a high-level overview of Emerge through
nels or hardware-specific primitives [6, 23, 27]. These operators are
                                                                              an illustrative example, shown in Figure 1. We consider two imple-
difficult to model precisely with existing verification techniques.
                                                                              mentations of the same GPT-2 subcomponent: one from Hugging-
In addition, they can introduce small numerical differences that
                                                                              Face Transformers, the other from vLLM. Although mathematically
accumulate along the computation graph [8], making direct output-
                                                                              equivalent, they differ substantially in operator choices, computa-
based testing unreliable for establishing model equivalence. Manu-
                                                                              tion graph structure, and tensor layouts.
ally writing rules for such operators requires significant domain
expertise and does not generalize well across frameworks.                        Input Relation. We begin by establishing equivalences between
    To address these challenges, we propose Emerge, a framework               the leaf nodes (inputs and parameters) of the two computation
for checking Implementation Equivalence over computation graphs               graphs. Since both implementations take the same token IDs and
of large-model implementations. The key idea is to verify equiva-             share embedding weights, most input nodes can be matched di-
lence without relying on hand-written rewrite rules: instead, Emerge          rectly. A more interesting case arises for the weight tensors 𝑤 1
discovers the relations needed to connect different implementations
                                                                              and 𝑤 2 . These represent the same logical matrix but are stored
directly from their executions and synthesizes rewrite rules on the
                                                                              in transposed layouts by the two frameworks. By comparing the
fly.
                                                                              loaded weight values, Emerge automatically infers the relation
    Our approach represents both implementations in a joint e-
                                                                              𝑤 1 ⇐⇒ transpose(𝑤 2 ).
graph [32] and incrementally establishes equivalence between their
nodes. For each candidate relation, Emerge first attempts to estab-              Congruence and Graph Rebuilding. After aligning input nodes,
lish it using available rules; only when this fails does it synthesize        Emerge propagates these relations to downstream operators through
a new rule by abstracting over shared dependencies and validate               congruence: if 𝑎 ≡ 𝑏, then 𝑓 (𝑎) ≡ 𝑓 (𝑏) whenever the same oper-
it with SMT solving or constraint-aware randomized testing. Each              ator 𝑓 is applied in the same position. In this example, the two
newly established equivalence is then propagated through e-graph              implementations share the same prefix computations, including
rebuilding. This design allows Emerge to handle divergent imple-              the embedding, addition, and layer normalization blocks. Once
mentation paths, framework-specific operator fusions, and opaque              their inputs are aligned, congruence automatically merges the cor-
kernels within a unified verification framework.                              responding intermediate nodes without requiring any rules. The
    We implement Emerge on computation graphs extracted by                     layernorm and layernorm nodes in two implementations are
TorchDynamo [22] and evaluate it on model pairs drawn from                    merged directly through congruence. After each successful merge,
Transformers and vLLM. Our evaluation shows that Emerge is ef-                Emerge rebuilds the e-graph to propagate the new equivalence; the
fective along three dimensions. First, it detects real implementation         precise procedure is described in §3.6.
bugs, including 10 of 13 known cases and 8 previously unknown
implementation issues, while providing useful fault localization                 Rule Synthesis and Application. After rebuilding, Emerge searches
signals. Second, it establishes equivalence for correct model pairs           for node pairs that remain in different equivalence classes but have
at practical cost. Third, it synthesizes block-level rewrite rules that       matching concrete values. Such pairs suggest candidate relations
compare favorably with manually authored ones.                                not yet captured by the current rule set. For the pair addmm and
Contributions. Our main contributions are as follows:                          linear , Emerge synthesizes a candidate rewrite rule by abstract-
                                                                              ing over the concrete arguments:
• Problem Formalization. We formulate Implementation Equiva-
  lence as a distinct verification problem for multiple implementa-                    linear(𝑎, transpose(𝑐), 𝑏) ⇐⇒ addmm(𝑏, 𝑎, 𝑐).
  tions of the same model, together with a formal framework over
  joint graphs, e-classes, and validated rewrite rules.                       The rule is then validated via randomized testing (§3.4). Once vali-
• Dynamic Rule Synthesis. We propose Emerge, which auto-                      dated, it is added to the rule set and immediately applied to merge
  matically discovers and validates rewrite rules on the fly, without         the two nodes into the same equivalence class. This merge is then
  manual rule writing.                                                        propagated to downstream operators through rebuilding, allowing
• Evaluation. We evaluate Emerge on model pairs drawn from                    Emerge to lift the newly established equivalence through the rest
  Transformers and vLLM, showing that it detects 10 of 13 known               of the graph (§3.6).
  bugs, identifies 8 previously unknown implementation issues,                    Following the same procedure, Emerge infers a rule relating
  provides useful fault localization, and establishes equivalence for          split and chunk : split(𝑎, 512, dim = 2) ⇐⇒ chunk(𝑎, chunks =
  correct implementation pairs at practical cost.                             3, dim = −1), which holds only when the shape of 𝑎 satisfies
                                                                              [𝑖, 3 × 512], where 𝑖 denotes the number of input tokens. This
  The rest of the paper is organized as follows. In § 2, we provide           precondition is necessary because the correspondence between
an overview of Emerge through an illustrative example. Section 3              split and chunk depends on evenly divisible dimensions. Emerge
presents the approach, and Section 4 describes implementation                 validates the rule formally via SMT solving under the shape con-
details. We present evaluation results in Section 5, discuss threats          straints (§3.4).
                                                                          2
Verify Implementation Equivalence of Large Models                                                                              Conference’17, July 2017, Washington, DC, USA


                                 wte                              b1      w1
                                                                                                         transpose(1, 2)
                                                                                                     Q
                    input_id      embedding
    Transformers                               add   layer_norm    addmm       split(512, dim = 2)   K   transpose(1, 2)       scaled_dot_product_attention    transpose(1, 2)
                   position_id    embedding                                                          V
                                                                                                         transpose(1, 2)
                                 wpe     wte         Congruence        Rule           Rule                                                                          Rule

                    input_id      embedding                                    chunk(chunks = 3,
       Vllm                                    add   layer_norm    linear                                            Q, K, V                    unified_attention_with_output
                                                                                   dim = -1)
                   position_id    embedding

                                         wpe                      b2      w2



Figure 1: A part of GPT-2 Model used to illustrate equivalence verification between two implementations. Simplified and
adjusted for clarity.


    Opaque Kernels. Finally, we consider the attention computa-                        def compare(P, Q):
tion [28], where the two implementations differ most substantially.                      G = initialize_egraph(P, Q) # build joint e-graph
Transformers decomposes attention into separate operators via                            R = ∅
scaled dot-product attention and output projection, whereas vLLM                         for i in range(MAX_ITERATIONS):
fuses the same computation into a single unified_attention ker-                            # may augment G with auxiliary nodes
nel. Emerge infers the following equivalence between                                       for (u, v) in find_possible_relations(G): # §3.2
  scaled_dot_product_attention and unified_attention :                                       proved = apply_rules(R, u, v) # §3.5
                                                                                             if not proved: # otherwise, synthesize new rule
unified_attention(𝑄, 𝐾, 𝑉 ) ⇐⇒                                                                 rule = synthesize_rule(G, u, v) # §3.3
                                                                                               if rule and validate(rule): # §3.4
                                          transpose(𝑄),
                                                                                                 R = R ∪ {rule}
transpose ­scaled_dot_product_attention ­ transpose(𝐾), ®® .
          ©                             ©               ªª
                                                                                                 proved = True
          «                             « transpose(𝑉 ) ¬¬                                   if proved:
                                                                                               G.merge(u, v)
Here we abbreviate transpose(𝑎, 1, 2) as transpose(𝑎) for clarity.
                                                                                               G.rebuild() # §3.6
Since this kernel is opaque to symbolic reasoning, Emerge validates
                                                                                           if outputs_equivalent(G):
the rule via randomized testing (§3.4). The complete rule set and
                                                                                             return EQUIVALENT
validation verdicts are made available for manual inspection.
                                                                                         return FAILED, localize(G) # §3.7
   At this point, the output nodes belong to the same equivalence
class, establishing the implementation equivalence of the two graphs.
Although this walkthrough covers only a fragment of GPT-2, the                                   Algorithm 1: High-level Algorithm of Emerge.
synthesized rules are immediately reusable across later layers, amor-
tizing the synthesis cost across the entire model. This example il-
lustrates the core intuition behind Emerge, but leaves out several
important design details, including candidate generation, rule syn-                    3.1       Formalization
thesis and validation, and e-graph maintenance. We now present
                                                                                       We begin by formalizing the key components of our approach.
the full framework.
                                                                                           Computation Graph. A computation graph is represented as a
                                                                                       directed acyclic graph (DAG) 𝐺 = (𝑉 , 𝐸), where each node 𝑣 ∈ 𝑉
3      Approach                                                                        represents either an operation (e.g., addition, multiplication, convo-
Emerge verifies the functional equivalence of two computation                          lution) or an input tensor and each edge (𝑢, 𝑣) ∈ 𝐸 indicates that
graphs through an iterative procedure on a joint e-graph. The over-                    the output of node 𝑢 is an input to node 𝑣. Given two graphs 𝐺 1 =
all workflow is illustrated in Algorithm 1. Given two computation                      (𝑉1, 𝐸 1 ) and 𝐺 2 = (𝑉2, 𝐸 2 ), we construct a joint graph 𝐺 = (𝑉 , 𝐸)
graphs, Emerge repeatedly proposes candidate relations between                         where 𝑉 = 𝑉1 ∪ 𝑉2 and 𝐸 = 𝐸 1 ∪ 𝐸 2 .
nodes (§3.2) and attempts to establish them using existing rules                           Equivalence Relation and E-Classes. Implementation Equivalence
(§3.5). When no existing rule applies, it synthesizes a candidate rule                 is a graph-level semantic notion: it asks whether two implemen-
from the current e-graph state (§3.3) and validates the rule (§3.4) be-                tations realize the same function. During verification, however,
fore merging the corresponding nodes. After each successful merge,                     Emerge maintains a node-level equivalence relation ≡ over the
the e-graph is rebuilt to maintain congruence and refresh attached                     nodes of the joint graph 𝐺. This relation induces a partition of 𝑉
execution data (§3.6). At the end of each iteration, Emerge checks                     into equivalence classes, or e-classes; for a node 𝑛 ∈ 𝑉 , we write 𝑛
whether the output nodes 𝑜 1 and 𝑜 2 belong to the same equivalence                    for the e-class containing 𝑛. Intuitively, nodes in the same e-class
class. If so, the two graphs are declared equivalent. Otherwise, if a                  are treated as equivalent by the e-graph. Each e-class is associated
predefined iteration limit is reached first, the verification attempt                  with concrete execution data obtained from dynamic execution; we
fails and Emerge invokes failure localization to identify the first pair               denote this attachment by a partial function 𝑓 : 𝑉 → 𝐷, where 𝐷
of mismatched nodes that best explains the remaining divergence.                       is the domain of runtime tensor values. Throughout the paper, we
                                                                                 3
Conference’17, July 2017, Washington, DC, USA                                                                                     Qi Zhan, Xing Hu, Xin Xia, and Shanping Li


use plain symbols such as 𝑛, 𝑢, 𝑣 for nodes and overlined symbols                                                  e-class                    node
such as 𝑛, 𝑢, 𝑣 for their corresponding e-classes.
   Rewrite Rules. A rewrite rule is an equivalence of the form 𝑙 ⇐⇒                                    add                   2
                                                                                                                    1                   add             linear
𝑟, where 𝑙 and 𝑟 are operator terms built from the same operator
vocabulary as the computation graph. An operator term is either a                                 b1          mm                                   mm        w2
variable, a literal constant or an operator applied to a finite num-
ber of sub-terms. We write FV(𝑡) for the free variables of a term                                        i1        w1        b1    b2         i1   i2   w1       transpose
𝑡. A substitution 𝜎 maps the free variables of a rule to e-classes.
Intuitively, a rewrite rule describes two parameterized computa-
tion subgraphs that produce the same result under all consistent
substitutions of their free variables. In our system, rewrite rules are                                                      3          add             linear
treated symmetrically, so either side may be matched and used to                                       linear
establish equivalence.                                                                                                                             mm        w2
   Maintained Structures. During verification, Emerge maintains                              b2          i2        w2
the joint graph 𝐺, the current equivalence relation ≡, the attached                                                          b1    b2         i1   i2   w1       transpose
execution data 𝑓 , and the set R of validated rewrite rules. The
rule set R may be initialized either as empty or with a seed set of
manually authored rules. These components are updated iteratively                          Figure 2: Rule synthesis from execution traces. ① Initial re-
as new relations are inferred, rules are synthesized and validated,                        lation ② Relation inferred from input values ③ Relation
and e-classes are merged and rebuilt. The procedure succeeds when                          inferred from rule synthesis.
the designated output nodes 𝑜 1 ∈ 𝑉1 and 𝑜 2 ∈ 𝑉2 are placed in the
same e-class.1
   The following sections use the running example in Figure 2. In
                                                                                           synthesis over this grammar to search for an expression that trans-
the figure, dashed boxes denote e-classes and solid boxes denote
                                                                                           forms one tensor value into the other. When such an expression
nodes. One subgraph computes a linear projection through the
                                                                                           is found, the corresponding auxiliary nodes are added to the joint
decomposed pattern add(mm(𝑖 1, 𝑤 1 ), 𝑏 1 ), while the other uses the
                                                                                           graph. Moreover, these transformations admit natural inverses un-
fused operator linear(𝑖 2, 𝑤 2, 𝑏 2 ). Although the two forms differ in
                                                                                           der compatible parameters (e.g., concat and split along the same
operator structure and weight layout, they correspond to the same
                                                                                           axis), so discovering a transformation from 𝑎 to 𝑏 also yields the
logical computation. We use this example to show how Emerge
                                                                                           reverse relation from 𝑏 to 𝑎, and it suffices to search in one direction.
aligns inputs, synthesizes rewrite rules, and eventually merges the
                                                                                               Once such a transformation is found, Emerge adds the corre-
two outputs into the same e-class.
                                                                                           sponding auxiliary nodes to the joint graph and uses them to relate
                                                                                           the original nodes. If both original nodes are leaves, such as model
3.2       Relation Inference
                                                                                           inputs or parameters, the transformed node can be merged directly
Emerge infers candidate relations by comparing the concrete tensor                         with its counterpart to establish an initial equivalence. In Figure 2,
values attached to e-classes. For two e-classes 𝑢 and 𝑣, if 𝑓 (𝑢) and                      for example, Emerge introduces the auxiliary node transpose on
𝑓 (𝑣) match up to a configurable numerical tolerance 𝜖, then (𝑢, 𝑣) is
                                                                                           top of 𝑤 2 and merges it with 𝑤 1 in ②. If the matched nodes are
treated as a candidate relation. This direct comparison is effective in
                                                                                           non-leaf nodes, however, the added auxiliary structure only exposes
many cases, but it is not sufficient on its own because semantically
                                                                                           a candidate equivalence. Emerge must still justify it through rule
equivalent tensors may differ in layout, partitioning, or structural
                                                                                           application (§3.5) or, when no existing rule applies, through rule
organization; for example, one may be the transpose of the other
                                                                                           synthesis (§3.3).
or a concatenation of its components. In our implementation, value
matching uses an absolute/relative tolerance of 10−2 by default. As
illustrated in Figure 2, the weight matrices 𝑤 1 and 𝑤 2 are stored
                                                                                           3.3     Rule Synthesis
in different layouts. We therefore need to introduce an auxiliary                          When Emerge identifies a candidate relation between e-classes
node to relate them.                                                                       𝑢 and 𝑣, it first attempts to establish it using existing rules in R.
    To handle such cases, Emerge uses a small transformation gram-                         If no existing rule applies, Emerge then synthesizes a rule using
mar to describe value-level operations that relate semantically                            representative nodes 𝑢 ∈ 𝑢 and 𝑣 ∈ 𝑣. Concretely, rule synthesis
equivalent tensors with different layouts or structures. The search                        seeks an equivalence 𝑙 ⇐⇒ 𝑟 such that 𝑙 matches 𝑢 and 𝑟 matches
space is given by the following context-free grammar:                                      𝑣 in the current e-graph. However, not every pair of target e-classes
                                                                                           admits such a rule. We therefore first determine whether the two
      𝐸    → transpose(𝐸, axis1, axis2 ) | concat(𝐸, . . . , 𝐸, axis)
                                                                                           sides can be abstracted over a common frontier.
                | reshape(𝐸, shapes) | split(𝐸, size, axis)
                                                                                              To this end, we introduce the notion of an abstraction frontier of
This grammar captures common layout and structural transforma-                             an equivalence class. Intuitively, a frontier is a set of e-classes whose
tions in deep learning frameworks, including reordering, reshaping,                        values jointly determine the value of the target e-class. Coarser
and partitioning. Emerge then performs bottom-up enumerative                               frontiers stop earlier and yield more general abstractions, while
1Without loss of generality, we assume single output nodes; in practice, both graphs       finer frontiers expand deeper and preserve more internal structure.
may have multiple outputs, and we require pairwise equivalence.                            Formally, for an equivalence class 𝑛, we write C(𝑛) ⊆ P (𝑉 ) for the
                                                                                       4
Verify Implementation Equivalence of Large Models                                                                    Conference’17, July 2017, Washington, DC, USA


set of candidate abstraction frontiers of 𝑛. For a representative node                   1    def synthesize_rule(egraph, 𝑢, 𝑣):
𝑛 ∈ 𝑛, let C(𝑛) denote the frontier family obtained by expanding                         2      𝑃𝑢 = enumerate_frontier_patterns(egraph, 𝑢)
through 𝑛. Then C(𝑛) and C(𝑛) can be computed recursively as                             3      𝑃 𝑣 = enumerate_frontier_patterns(egraph, 𝑣)
                                                                                        4      for ((𝑆𝑢 , 𝑝𝑢 ), (𝑆 𝑣 , 𝑝 𝑣 )) in Π(𝑃𝑢 , 𝑃 𝑣 ):
            {𝑛} ,                                     𝑛 is a leaf,
           
                                                                                         5         if 𝑆𝑢 == 𝑆 𝑣 : # depend on the same frontier
           
           
  C(𝑛) =                                                           (1)
            {𝑛} ∪
                      Ð𝑘
                                 𝑆® ∈ 𝑘𝑖=1 C(𝑙𝑖 ) , otherwise,
                                      Î                                                  6             return Rule(𝑝𝑢 , 𝑝 𝑣 )
                          𝑖=1 𝑆𝑖
                                                                                        7
           Ð
  C(𝑛) = 𝑚∈𝑛 C(𝑚),                                                  (2)                  8    def enumerate_frontier_patterns(egraph, 𝑛):
                                                                                         9      yield ({𝑛}, Atom(𝑛))
where 𝑙 1, . . . , 𝑙𝑘 are the children of 𝑛 and 𝑆® = (𝑆 1, . . . , 𝑆𝑘 ). Intuitively,   10      # Expand through operators in the same e-class
frontier enumeration may either stop at the current e-class or con-                     11      for n in 𝑛:
tinue expanding through its children; taking the union over all                         12          if n.op == "input":
representatives allows enumeration to proceed through any equiv-                        13              continue
alent form already present in the e-graph. For example, in Figure 2,                    14          child_patterns = [
{add} ∈ C(add), {mm, 𝑏 1 } ∈ C(add), and {𝑏 1, 𝑤 1, 𝑖 1 } ∈ C(add).                     15              enumerate_frontier_patterns(egraph, arg)
    Two equivalence classes 𝑢 and 𝑣 can admit a rewrite rule only                       16              for arg in n.args
if they share a common frontier, i.e., C(𝑢) ∩ C(𝑣) ≠ ∅. If their                        17          ]
frontier families are disjoint, then no meaningful symbolic relation                    18          # Cartesian product over children
can be synthesized between them. In the running example, after                          19          for combo in Π(*child_patterns):
input alignment we have 𝑏 1 = 𝑏 2 and 𝑖 1 = 𝑖 2 , so the add and                        20              𝑆 = set()
  linear nodes share the common frontier {𝑏 1, 𝑖 1, 𝑤 2 }. By contrast,                 21              args = []
the mm node and the linear node do not share any common                                 22              for (𝑆𝑖 , 𝑝𝑖 ) in combo:
frontier, and hence no rule is synthesized between them.                                23                  𝑆 = 𝑆 ∪ 𝑆𝑖
    A key design goal is not merely to synthesize a valid rule, but to                  24                  args.append(𝑝𝑖 )
synthesize the most general one. When multiple common frontiers                         25              𝑝 = Node(n.op, args)
are available, they induce symbolic patterns at different abstraction                   26              yield (𝑆, 𝑝)
levels. If frontier enumeration stops too early, the resulting rule
preserves unnecessary internal structure and becomes overly spe-
cific. For example, a naive synthesis procedure might stop at the e-                    Algorithm 2: Rule synthesis by shared frontier enumeration.
class containing layernorm(𝑎) and produce the overly specific rule
linear(layernorm(𝑎), transpose(𝑐), 𝑏) ⇔ addmm(𝑏, layernorm(𝑎), 𝑐),
which unnecessarily constrains the first argument to be a layernorm                        In the running example, the extracted symbolic pattern summa-
output. By continuing the abstraction one step further and treating                     rizes the decomposed subgraph add(mm(𝑖 1, 𝑤 1 ), 𝑏 1 ) as the com-
its input as a symbolic variable, Emerge instead synthesizes the                        pound term addmm(𝑏, 𝑎, 𝑐). In the end, Emerge synthesizes the
more general rule linear(𝑎, transpose(𝑐), 𝑏) ⇔ addmm(𝑏, 𝑎, 𝑐).                          equivalence linear(𝑎, transpose(𝑐), 𝑏) ⇐⇒ addmm(𝑏, 𝑎, 𝑐), thereby
    Equipped with the above definitions, we now present the algo-                       merging the add root and the linear root in ③ of Figure 2.
rithm for rule synthesis, shown in Algorithm 2. For each target
e-class, the algorithm enumerates a sequence of frontier-pattern                        3.4    Rule Validation
pairs. Each pair (𝑆, 𝑝) consists of a frontier 𝑆 and a symbolic pat-                    Synthesized rules are not admitted into R immediately. Before a
tern 𝑝 obtained by abstracting the target over 𝑆. Here Π denotes                        rule can participate in equality saturation, Emerge validates it using
Cartesian-product enumeration. The enumeration proceeds in a top-                       the strongest applicable method. The validation pipeline serves two
down manner, from the coarsest abstraction to progressively finer                       purposes: to reject ill-formed or semantically unsound rules, and
ones. Starting from a target e-class 𝑛, the algorithm first yields the                  to attach an evidence level to each accepted rule. Pre-checking
frontier {𝑛} (line 9), treating the entire e-class as a single symbolic                 and Rule Classification. Validation begins with a lightweight
atom. It then recursively expands representative nodes toward their                     structural pre-check. In this phase, Emerge rejects malformed or
inputs (lines 12–26), refining the current frontier and construct-                      unsupported rules, such as rules with inconsistent operator at-
ing correspondingly more specific symbolic patterns. In this way,                       tributes. Only rules that pass this pre-check proceed to semantic
frontier-pattern pairs are generated in decreasing order of gen-                        validation.
erality. Given the two enumerated sets 𝑃𝑢 and 𝑃 𝑣 , the procedure                           The remaining rules are then classified according to their seman-
searches over Π(𝑃𝑢 , 𝑃 𝑣 ) for a pair (𝑆𝑢 , 𝑝𝑢 ) ∈ 𝑃𝑢 and (𝑆 𝑣 , 𝑝 𝑣 ) ∈ 𝑃 𝑣            tic structure in order to select the strongest applicable validation
such that 𝑆𝑢 = 𝑆 𝑣 (lines 4–7). Because frontier enumeration emits                      strategy. At a high level, we distinguish three classes: (i) Scalar-
frontier-pattern pairs from coarser to finer frontiers, the first such                  Logic, containing only arithmetic, boolean, or bitwise operators;
match corresponds to the coarsest shared abstraction frontier be-                       (ii) Tensor-Rearrangement, consisting of structural tensor transfor-
tween 𝑢 and 𝑣, and therefore yields the most general candidate rule                     mations such as view, transpose, reshape, and split; and (iii)
under the current e-graph: 𝑝𝑢 ⇐⇒ 𝑝 𝑣 . If no such pair exists, the                      Opaque-Heavy, containing fused kernels, black-box operators, or
algorithm concludes that no rule can be synthesized for 𝑢 and 𝑣                         numerically complex tensor operators such as embedding, softmax,
under the current graph state.                                                          and linear.
                                                                                    5
Conference’17, July 2017, Washington, DC, USA                                                                 Qi Zhan, Xing Hu, Xin Xia, and Shanping Li


   Symbolic Verification via SMT. For rules whose semantics                  are treated symmetrically in our system, we also accept matches in
can be modeled precisely, Emerge invokes an SMT solver to prove              the reverse direction, i.e., matching 𝑟 at 𝑢 and 𝑙 at 𝑣.
equivalence under the inferred constraints.                                     Each matched pair (𝑢, 𝑣) provides a concrete witness that the
• Scalar Arithmetic. Expressions are lowered to SMT real and                 rule relates the two e-classes under the current bindings. Emerge
  boolean terms. The solver checks the negation of the candidate             merges the corresponding e-classes and invokes the rebuilding
  equivalence; if the negation is unsatisfiable, the rule is proved          procedure (§3.6) to restore congruence. If a rule carries additional
  correct and marked formally verified.                                      preconditions (e.g., shape divisibility constraints inferred during
• Tensor Rearrangement. For structural tensor rules, Emerge                  synthesis), the match is accepted only when these constraints are
  models each tensor as a symbolic array whose elements are dis-             satisfied by the current substitution.
  tinct symbolic variables. Operators such as transpose, reshape,
  and split/concat are lowered to index transformations. Un-                 3.6    E-Class Merge and Graph Rebuild
  der satisfiable shape constraints, the solver proves element-wise          When two e-classes 𝑛 1 and 𝑛 2 are merged, the new equivalence
  equality between the two sides.                                            may induce further merges among their parent nodes through
   Constraint-Aware Randomized Testing. For rules involving                  congruence. To restore this invariant, Emerge performs a worklist-
fused kernels, numerically complex operators, or operators outside           driven rebuilding phase until a fixpoint is reached.
the supported SMT, Emerge falls back to empirical validation. To
make randomized testing meaningful, the validator first solves the           (1) Canonicalize Parent References. For every parent node 𝑝
rule’s preconditions and then samples inputs that satisfy them.                  that uses 𝑛 1 or 𝑛 2 as an argument, Emerge replaces that argu-
                                                                                 ment with the canonical representative of the newly merged
• Shape-Aware Generation. Emerge solves systems of shape con-
                                                                                 e-class.
  straints, such as shape_dim_eq and numel_eq, to generate valid
                                                                             (2) Detect New Congruences. After canonicalization, Emerge
  tensor shapes satisfying operator requirements such as matrix-
                                                                                 checks whether any parent nodes have become structurally
  multiplication alignment, reshape consistency, or divisibility for
                                                                                 congruent, i.e., they have the same operator and their corre-
  chunking and splitting.
                                                                                 sponding arguments now refer to the same e-classes. If so, they
• Domain-Aware Sampling. For operators with restricted input
                                                                                 are merged and added to the worklist for further rebuilding.
  domains, such as embedding, the validator infers the semantic
                                                                             (3) Refresh Execution Data. The merged e-class retains one at-
  role of each tensor (e.g., index tensor versus weight tensor) and
                                                                                 tached value as its representative concrete value. Then, for
  samples values from the corresponding admissible domain. This
                                                                                 each parent node whose input e-classes have changed, Emerge
  avoids invalid executions such as out-of- bounds indexing and
                                                                                 re-executes the corresponding operator on the updated repre-
  improves the effectiveness of randomized testing.
                                                                                 sentative inputs to obtain a refreshed output value.
   In addition to shape and domain constraints, the validator also
checks operator-specific side conditions, such as index bounds for
                                                                             3.7    Fault Localization
embedding or divisibility requirements for chunk. Rules whose
inferred preconditions are unsatisfiable are rejected directly, rather       When verification terminates without merging the output e-classes,
than being vacuously accepted.                                               Emerge performs failure localization to identify the earliest sub-
   Finally, Emerge assigns each accepted rule a validation level.            stantive divergence between the two implementations. Rather than
Rules proved by SMT are labeled formally verified, while rules that          reporting only the final unmatched outputs, Emerge traces the mis-
pass constraint- aware randomized testing are labeled empirically            match backward through the e-graph and returns a pair of frontier
validated. Only rules with one of these accepted validation levels           nodes that best explains why equivalence could not be established.
are inserted into R and used during subsequent equality saturation.             The localization procedure is heuristic-guided. Starting from
                                                                             the outputs, it traverses backward along data dependencies while
3.5     Rule Application                                                     abstracting away nodes treated as semantically transparent by the
                                                                             heuristic. It then continues through the primary data-carrying in-
A validated rewrite rule is applied only after relation inference has
                                                                             puts of each operator until it reaches the first frontier whose e-class
identified a candidate pair of nodes. Rule application in Emerge
                                                                             has no cross-graph counterpart. Among all such frontiers, Emerge
is therefore candidate-driven: Emerge first proposes a candidate
                                                                             reports the earliest unexplained mismatch.
relation and then checks whether an existing rule can justify it.
Unlike conventional term rewriting, matching in Emerge is e-class
aware: because an e-class may contain multiple nodes, a rule need            4     Implementation
not match a single fixed node form. Instead, it may match through            Emerge is implemented on top of TorchDynamo [22], following
any representative already contained in the e-classes.                       prior work [31], to capture computation graphs from production
    Formally, given a rule 𝑙 ⇐⇒ 𝑟 , Emerge searches for a substitu-          code (e.g., vLLM and HuggingFace) without manual instrumenta-
tion 𝜎 : FV(𝑙) ∪ FV(𝑟 ) → 𝑉 from rule variables to e-classes. Literal        tion. To compactly represent and reason about many equivalent
constants and operator parameters are matched syntactically as               expressions, we use an e-graph with Union-Find [25], implemented
part of the term structure, rather than through 𝜎. We say that the           via egg [32]. Rule validation combines SMT-based checking with
rule matches a pair of e-classes (𝑢, 𝑣) if there exist representatives       Z3 [7] and constraint-aware randomized testing, as described in
𝑢 ∈ 𝑢 and 𝑣 ∈ 𝑣 such that the left-hand side 𝑙 matches 𝑢 under 𝜎             §3.4. This section focuses on two practical aspects of the implemen-
and the right-hand side 𝑟 matches 𝑣 under the same 𝜎. Since rules            tation: specialized input matching and efficiency optimizations.
                                                                         6
Verify Implementation Equivalence of Large Models                                                                       Conference’17, July 2017, Washington, DC, USA


                    Table 1: Known bug cases used in our evaluation and detection results compared with TTrace.

   ID    Emerge        TTrace     Description                                                                                              Issue     Fix
    1                    ✗        InternLM2: wrong split_qkv execution semantics in tensor parallel                                        8017      pull/8055
    2                    ✗        OLMo: wrong shard/full weight-loading semantics in tensor parallel                                       3775      pull/3869
    3                             Gemma: MLP GELU approximation mismatch (tanh vs exact)                                                   3411      pull/3653
    4                             GPT-J: incorrect RoPE rotation scheme                                                                    590       pull/941
    5                             GLM: rotary / attention path mismatch                                                                    16904     pull/16912
    6                             Command-R: wrong RoPE base parameter priority                                                            3892      pull/3919
    7                             Gemma2: context/window boundary exposed as rotary/cache inconsistency                                    6220      pull/10584
    8                             Qwen2-VL: weights mapper / parameter-path mismatch                                                       18976     pull/19054
    9                    ✗        Phi: declared max position exceeds materialized rotary cache size                                        9502      pull/9503
   10                             Llama4-Vision: wrong vision rotary cache representation / dtype path                                     25888     pull/25889
   11        ✗           ✗        Mistral long prompt / sliding-window behavior; semantics are hidden                                      2059      pull/2088
   12        ✗           ✗        Phi-3.5: LongRoPE branch / KV-cache semantics hidden by data-dependent branching                         27414     pull/27431
   13        ✗           ✗        GGUF: TP embedding/materialization bug not isolated under current method                                 7880      pull/7954
  Legend (Detected):    exact bug root;   same functional block;   farther from the root; ✗ missed.


4.1     Practical Input Matching                                                           to this intersection, pruning branches that cannot yield a shared
Although input relations can in principle be inferred by the gen-                          frontier. Second, Cartesian products in frontier enumeration (Algo-
eral relation inference procedure in §3.2, using that machinery                            rithm 2, line 20) are generated lazily with Python generators and
directly on all input pairs is unnecessarily expensive in practice.                        traversed in diagonal order, so that coarser, more general candidates
We therefore implement a specialized candidate-generation pipeline                         are explored earlier. Together, these optimizations avoid materi-
for input matching. Given input sets 𝐼 1 and 𝐼 2 from graphs 𝐺 1 and                       alizing exponentially many combinations and allow synthesis to
𝐺 2 , the goal is to construct a small candidate set 𝐸 input ⊆ 𝐼 1 × 𝐼 2 that              terminate as soon as the first shared frontier is found.
is highly likely to contain the true correspondences.
    Purely syntactic alignment by name or argument position is                             5     Evaluation
brittle in real systems due to inconsistent naming, layout differ-                         We evaluate Emerge on the following research questions (RQs):
ences (e.g., channels-first vs. channels-last), and input fusion (e.g.,                    • RQ1 (Bug Detection): Can Emerge effectively detect and local-
concatenated Q/K/V weights). We therefore treat input matching as                            ize real-world implementation bugs?
candidate generation over concrete values: lightweight heuristics                          • RQ2 (Equivalence & Scalability): Can Emerge establish equiv-
(e.g., shape-compatible weight matching and embedding-table iden-                            alence for correct implementation pairs at practical cost?
tity) propose a small set of high-probability pairs. These heuristics                      • RQ3 (Rule Characterization): What kinds of rules does Emerge
are used only to narrow the search space; final acceptance still                             synthesize, and how do they compare with manually authored
comes from the core relation inference procedure.                                            rules?
    This matching layer is used only for candidate generation. It
does not alter the soundness of the verification procedure: every                          5.1        Experimental Setup
proposed input relation must still be accepted by the core equiva-                         Baselines. A direct end-to-end baseline is not available for our
lence engine through value-based relation inference. In this way,                          full setting: existing techniques mainly target tensor-parallel trans-
the input-matching heuristics improve robustness to inconsistent                           formations within a shared framework and operator semantics,
naming and fused representations while preserving the verification                         whereas our setting involves cross-framework implementations.
guarantees of the main algorithm.                                                          We therefore use task-specific comparisons: TTrace [12] serves as
                                                                                           the baseline for bug detection in RQ1, and Entangle [31] serves as
4.2     Efficiency Optimizations                                                           the baseline for rule characterization in RQ3.
We implement several optimizations to improve efficiency:                                  Environment. All experiments are conducted on our local server
   Dependency-Based Blocking. Two e-classes can be equiva-                                 with an Intel Xeon Platinum 8358P CPU, 2 TB of memory, and one
lent only if they depend on the same logical inputs. We therefore                          NVIDIA A800 80GB PCIe GPU, running Ubuntu 20.04.6 LTS. All
compute a dependency signature for each e-class (the set of reach-                         experiments use a maximum of 2 main verification iterations.
able input leaf e-classes) and compare candidate relations only
when they have identical signatures. This blocks many impossible                           5.2        RQ1: Bug Detection
comparisons early and reduces the search space in practice.                                We answer RQ1 through two studies: reproducing known imple-
   Efficient Frontier Enumeration. Rule synthesis is driven by                             mentation bugs and discovering previously unknown bugs in cur-
shared-frontier discovery, so we optimize frontier enumeration in                          rent releases. Besides whether Emerge detects non-equivalence,
two ways. First, for a candidate relation (𝑢, 𝑣), we precompute the                        we also evaluate localization quality at three levels: , where the
e-classes reachable from both endpoints and restrict enumeration                           reported node is the root-cause operator; , where it falls in the
                                                                                      7
Conference’17, July 2017, Washington, DC, USA                                                               Qi Zhan, Xing Hu, Xin Xia, and Shanping Li


same functional block; and , where it lies further downstream.              merges through rebuilding. As a result, already explained differ-
Here, a functional block denotes the smallest model component im-           ences are removed from subsequent analysis, which improves both
plementing a coherent sub-computation, such as rotary embedding,            detection coverage and localization precision by focusing on the
attention, or MLP, as identified from the captured computation              first frontier that remains unmatched.
graph and the corresponding implementation code.
                                                                            5.2.2 Discovering New Bugs. Beyond reproducing historical bugs,
5.2.1 Reproducing Known Bugs. We collected 13 confirmed, inde-              we ran Emerge on recent releases of all evaluated model families
pendently fixed bugs from the issue trackers of vLLM [14] and               under both default and non-default configurations such as alter-
HuggingFace Transformers [33]. For each bug, we reproduce the               native attention backends. This process uncovered 8 previously
faulty behavior and construct a model pair that exercises the af-           unknown implementation issues (Table 2). Among these 8 issues,
fected code path. We then run Emerge and record (i) whether it              2 have already been confirmed and patched, while the other cases
reports non-equivalence, and (ii) the first reported mismatch re-           have been confirmed by developers and now have follow-up fixes
turned by the localization procedure. For baseline comparison, we           under review. We highlight two representative cases below.
run TTrace on the same model pairs under the same configurations               GPT-2 scale_attn_weights (Bugs #14–#16). Emerge found that
and record whether it reports a mismatch and, when available, its           the scale_factor parameter is silently ignored under the SDPA
localization result. We report these results in Table 1.                    and FlashAttention backends in both Transformers and vLLM. In
                                                                            our framework, the candidate rule for the corresponding attention
        Table 2: Unknown issues identified by Emerge.
                                                                            computation fails validation because the scaling factor is absent
                                                                            from one side. This bug is configuration-sensitive and would not
ID Our Description                               Issue Fix                  surface under the default backend. Fixes have been merged in Trans-
 14         GPT-2: scale_attn_weights ig- 44380 pull/44397                  formers (PR#44397) and are under review in vLLM (PR#35436).
            nored in SDPA path                                                 Qwen1 logn_attn (Bug #17). Qwen1 applies a log-𝑛 attention
 15         GPT-2                         family: 35402 pull/35436          scaling during long-context inference, but this logic was entirely
            scale_attn_weights mismatch in                                  missing in vLLM. Emerge reported non-equivalence along the at-
            vLLM                                                            tention path and localized the discrepancy to the missing scaling
 16         GPT-BigCode                   family: 36565 pull/36637          behavior. Unlike configuration-specific bugs that only surface un-
            scale_attn_weights mismatch in                                  der non-default settings, this bug can already be triggered under
            vLLM                                                            the default configuration once the input length exceeds the base
 17         Qwen1: long-context logn_attn 36880 pull/37089                  context window.
            missing in vLLM
 18         PhiMoE: router_jitter_noise 35494 pull/35499                    5.3    RQ2: Equivalence Proving and Scalability
            hardcoded                                                       In this section, we evaluate Emerge’s ability to establish full equiva-
 19         OLMoE: clip_qkv ignored               35513 pull/35523          lence for correct implementation pairs and analyze how verification
 20         JAIS: learned positional embeddings 37400 pull/37820            time scales with model size.
            still trigger ALiBi in vLLM attention                              Our benchmark covers five representative model families: GPT2 [21],
 21         Phi: qk_layernorm missing in vLLM 37852 pull/37870              Qwen [3], Llama [9], Mistral [11], and Phi [1], which are among the
                                                                            most widely adopted open-weight language models in the research
   Emerge detects 10 of the 13 known bugs. Among the detected               community. Figure 3a reports the end-to-end verification time for
cases, 6 are localized exactly ( ), 3 are localized to the same func-       each model family, together with the corresponding model size in
tional block ( ), and 1 is localized further downstream ( ). For            parameters. Across these model families, the measured verification
example, Bug #4 (GPT-J incorrect RoPE) is localized directly to             time ranges from 11.03 seconds for GPT-2 70M to 350.09 seconds
the rotary_embedding operator, while Bug #3 (Gemma GELU mis-                for Mistral 12B. For every model in the benchmark, Emerge estab-
match) is pinpointed at the gelu node. In these cases, Emerge re-           lishes that the output nodes of the two implementations belong
duces debugging effort from inspecting the entire model execution           to the same equivalence class, confirming full functional equiva-
to inspecting a single operator and its immediate context. Three            lence. Disabling any one of the key optimizations described in §4.2
bugs are missed. Two require data-dependent branches that are not           caused verification to exceed one hour on the complete benchmark.
exercised by our current inputs, and one depends on weight-loading          This indicates that these optimizations are essential to making the
semantics outside the current graph-extraction boundary.                    approach practical, rather than merely improving constant factors.
   Compared with TTrace, Emerge achieves both higher detec-                    Figure 3b shows the scalability trends on three representative
tion coverage and more precise localization on the known-bug                model families: Qwen, Llama, and Mistral. As shown in the fig-
benchmark. As shown in Table 1, Emerge detects 10 of 13 bugs,               ure, verification time increases with model depth and overall ar-
whereas TTrace detects 7. Moreover, Emerge localizes 6 bugs ex-             chitectural complexity. Qwen grows relatively steadily over the
actly ( ), while TTrace does not achieve exact localization on              evaluated range, whereas Llama and Mistral increase much more
any case. TTrace localizes bugs by comparing execution traces               sharply at larger depths, with Mistral exceeding 100 seconds at
against a trusted reference under carefully designed numerical              22 layers. An explanation is the growth of the candidate search
tolerances, whereas Emerge incrementally establishes local equiva-          space: after dependency- and value-based filtering, Emerge still
lences, merges the corresponding e-classes, and propagates these            needs to consider many possible relations among surviving nodes,
                                                                        8
Verify Implementation Equivalence of Large Models                                                                                     Conference’17, July 2017, Washington, DC, USA


                                                                                                            Figure 4 shows that Emerge synthesizes block-level rules (R1–R2)




                                       Verification Time (s)
                                                                            Qwen
                                                           100
 Model       Params      Time (s)                                           Llama                        that directly capture the semantic decomposition of feed-forward
                                                                            Mistral                      and head-partitioned attention blocks across tensor-parallel parti-
 GPT-2       70m            11.03
 Qwen        0.5b           22.59                              50                                        tions. For readability, R1–R2 present normalized block-level sum-
 Phi         3.8b          147.99                                                                        maries of the actual learned rules, which in the implementation
 Llama3      8b            148.33                                                                        also contain lower-level operators such as view, chunk, fused atten-
 Mistral     12b           350.09                              0                                         tion kernels, and all_reduce. By contrast, Entangle uses manually
                                                                    2   6     10      14   18   22
                                                                                                         authored component rules (E1–E4) for affine decomposition, acti-
(a) End-to-end verification.                                    (b) Scalability trends.                  vation distribution, reduction, and attention partitioning. The same
                                                                                                         block-level equivalences can be recovered by composing these com-
      Figure 3: RQ2 results on correctness and scalability.                                              ponent rules together with standard operator normalization and
                                                                                                         implementation-specific reasoning, whereas Emerge synthesizes
                                                                                                         the composed equivalence directly.
and the number of such candidate pairs can grow quadratically in
the worst case. As a result, deeper and more structurally diverse                                        6     Discussion
models require more verification work as depth increases. Despite                                        In this section, we discuss the threats to validity and limitations of
this increase, Emerge remains practical on the evaluated models.                                         our approach.

5.4     RQ3: Rule Characterization                                                                       6.1    Threats to Validity
We characterize the rules synthesized by Emerge from two perspec-                                        Internal Validity. Our results depend on the correctness and com-
tives: the distinct rule patterns that emerge across all experiments,                                    pleteness of the captured computation graphs. Since the current
and the granularity of these synthesized rules relative to manually                                      implementation relies on TorchDynamo [22], bugs or omissions
authored rules.                                                                                          in graph capture may hide behavior outside the extracted graph
                                                                                                         and thereby affect both bug detection and equivalence checking. A
5.4.1 Synthesized Rule Catalogue. Across the five full-model pos-                                        second threat comes from rule validation. While some synthesized
itive examples in our benchmark, Emerge synthesizes 86 rule in-                                          rules are formally proved by SMT, others are accepted through
stances, corresponding to only 54 unique rules. Each model requires                                      constraint-aware randomized testing. Such empirically validated
a small learned rule set, ranging from 14 to 21 rules. This indicates                                    rules may still be unsound, potentially leading to false equivalence.
that the checking process relies not on a large model-specific rule                                      Some results may also be sensitive to hyper-parameters such as
library, but on a compact reusable core plus a few model-specific                                        numerical tolerances, iteration limits, and validation budgets.
rules. The learned rules exhibit a clear reuse pattern. 12 of the 54                                        External Validity. Our evaluation focuses on transformer-based
distinct rules appear in at least two models, and several recur in all                                   language models implemented in HuggingFace Transformers and
models, including wrapper elimination, dtype normalization, and                                          vLLM [14, 33]. The results may not directly generalize to other serv-
simple algebraic normalization. The most common rule families                                            ing or compilation ecosystems such as TensorRT, XLA, or ONNX
are layout/wrapper normalization, normalization-path canonical-                                          Runtime [2, 15, 35], where operator lowering and execution behav-
ization, and partition/slicing rules. In contrast, model- specific dif-                                  ior can differ. Although the underlying formulation is not specific
ferences are concentrated in a small number of higher-value bridge                                       to these two frameworks, our current implementation relies on
rules, especially for attention kernels, embedding, and fused MLP.                                       TorchDynamo [22] for computational graph capture, which may
   Of the 86 rule instances, 64 are formally verified and 22 are                                         not be available or equally effective in other deployment settings.
empirically validated. Most rules over explicit tensor transforma-
tions, such as layout, slicing, and normalization rewrites, can be
                                                                                                         6.2    Limitations
discharged by SMT. By contrast, rules involving opaque or fused
operators, especially attention-related ones, are validated through                                      Coverage and Dynamic Control Flow. Our approach is execution-
randomized testing. This division reflects the design of Emerge:                                         driven: equivalence relations and rewrite rules are synthesized only
use formal proof whenever the operator semantics are explicit, and                                       for computation paths exercised by the input set. If a data- depen-
fall back to empirical validation for semantically opaque kernels.                                       dent branch is never triggered, the corresponding semantics remain
In our benchmark, we did not observe any empirically validated                                           unexplored. This limitation is especially pronounced for Mixture-of-
rule that later led to an incorrect merge or an incorrect equivalence                                    Experts architectures [24], where expert routing depends on input
result. Nevertheless, these rules remain testing-backed rather than                                      values, and for long-context mechanisms such as LongRoPE, which
formally proved.                                                                                         are activated only beyond certain sequence-length thresholds.
                                                                                                            Validation Strength. When both sides of a rule consist of sym-
5.4.2 Comparison with Manually Authored Rules. To assess rule                                            bolically tractable operators, Emerge can discharge equivalence
quality, we compare the rules synthesized by Emerge with manually                                        through SMT solving. However, opaque or fused kernels often lack
authored rules from Entangle [31] on tensor-parallel equivalence                                         accessible symbolic semantics and therefore fall back to constraint-
patterns. Although Emerge is designed for cross-framework equiv-                                         aware randomized testing. In such cases, confidence depends on
alence, this setting provides a direct way to contrast automatically                                     the quality of inferred preconditions and the testing budget, rather
inferred rules with hand-engineered ones.                                                                than on a formal proof.
                                                                                                     9
Conference’17, July 2017, Washington, DC, USA                                                                           Qi Zhan, Xing Hu, Xin Xia, and Shanping Li



 Emerge (Ours): Automatically Synthesized Rules
                                                                             
        (R1) linear(gelu linear(𝑥, concat(𝑏 1, 𝑏 2, 0), concat(𝑐 1, 𝑐 2, 0)) , concat(𝑓1, 𝑓2, 1), 𝑒)
                                                                                                              
         ⇐⇒ reduce_add(linear gelu(linear(𝑥, 𝑏 1, 𝑐 1 )), 𝑓1, 𝑒 , linear gelu(linear(𝑥, 𝑏 2, 𝑐 2 )), 𝑓2, 0 )
        (R2) linear attentionhead (𝑞, 𝑘, 𝑣), concat(𝑤𝑜(1) , 𝑤𝑜(2) , 1), 𝑏
                                                                          

         ⇐⇒ reduce_add(linear attentionhead (𝑞 1, 𝑘 1, 𝑣 1 ), 𝑤𝑜(1) , 𝑏 , linear attentionhead (𝑞 2, 𝑘 2, 𝑣 2 ), 𝑤𝑜(2) , 0 )
                                                                                                                         


 Entangle (Baseline): Manually Defined Rules
                                                                                                                             
        (E1) addmm concat(𝑏 1, 𝑏 2, 0), 𝑥, concat(𝑊1,𝑊2, 1), 𝛽, 𝛼 ⇐⇒ concat addmm(𝑏 1, 𝑥,𝑊1, 𝛽, 𝛼), addmm(𝑏 2, 𝑥,𝑊2, 𝛽, 𝛼), 1
                                                                                   
        (E2) gelu concat(𝑡 1, 𝑡 2, 𝑑) ⇐⇒ concat gelu(𝑡 1 ), gelu(𝑡 2 ), 𝑑
                                                                                                                    
        (E3) matmul concat(𝑥 1, 𝑥 2, 1), concat(𝑊1,𝑊2, 0) ⇐⇒ reduce_add matmul(𝑥 1,𝑊1 ), matmul(𝑥 2,𝑊2 )
                                                                                                                 
        (E4) attentionhead concat(𝑞 1, . . . , 𝑞𝑝 , 1), concat(𝑘 1, . . . , 𝑘𝑚 , 1), concat(𝑣 1, . . . , 𝑣𝑚 , 1)
                                                                                                                   
             ⇐⇒ concat attentionhead (𝑞 1, 𝑘𝜋 (1) , 𝑣 𝜋 (1) ), . . . , attentionhead (𝑞𝑝 , 𝑘𝜋 (𝑝 ) , 𝑣 𝜋 (𝑝 ) ), 1


Figure 4: Comparison of tensor-parallel equivalence rules. Top: normalized block-level rules synthesized by Emerge from
execution traces. Bottom: manually authored component rules used by Entangle. All rules assume compatible tensor shapes
and partition layouts. R2 and E4 additionally assume that query, key, and value tensors are partitioned into disjoint head
groups under a fixed query-to-KV head mapping 𝜋.


   Scalability. Repeated graph execution, e-graph rebuilding, and                  often involve different operator vocabularies, graph structures, lay-
rule enumeration introduce overhead that grows with model size.                    out transformations, and opaque kernels.
Although we employ pruning and bounded enumeration, synthesis                         Rewrite-based Equivalence Checking. Recent work [31, 38,
can still become costly on very large graphs with high branching                   39] has explored the use of equality saturation and e-graphs to
factors. We have not yet evaluated Emerge at the 200B-parameter                    check equivalence between computation graphs. Aerify [39], Entan-
scale, and reducing this overhead remains an important direction                   gle [31], and Scalify [38] are representative systems in this direction.
for future engineering work.                                                       In particular, Scalify uses bijection inference to reason about layout
                                                                                   transformations, while our work also targets equivalences arising
                                                                                   from different operator implementations and execution structures.
7 Related Work                                                                        Compared with these approaches, our work focuses on discover-
7.1 Equivalence Checking for DL Systems                                            ing rules dynamically during verification. This makes the approach
The closest line of work studies equivalence checking for distributed              better suited to modern large-model implementations, where the
training and parallel implementations of deep learning systems [12,                relevant transformations are often framework-specific and difficult
16, 31, 38, 39], which can be broadly grouped into three categories.               to enumerate in advance.
   Differential Testing and Diagnosis. Testing-based approaches
validate correctness by comparing executions against a trusted ref-
erence [12]. Rather than comparing only final outputs, TTrace                      7.2     Equality Saturation and Rule Synthesis
aligns intermediate tensors from a distributed execution with those                Our approach builds directly on e-graphs and equality satura-
from a reference implementation and uses tolerance analysis to                     tion [26], which provide a compact representation of many equiva-
distinguish bug-induced deviations from numerical error. However,                  lent expressions and support efficient congruence maintenance dur-
such methods still provide empirical rather than formal evidence                   ing rewriting. Egg [32] introduces an efficient equality-saturation
of equivalence. They are also sensitive to implementation differ-                  engine together with the rebuild procedure that restores congru-
ences that make numerical alignment difficult, even when the two                   ence after merges; our rebuilding procedure is inspired by this
implementations are semantically equivalent.                                       design. Our attachment of concrete execution values to e-classes
   Formal Verification of Parallel Training. TrainVerify [16]                      can be viewed as an e-graph analysis in the sense of Egg [32]. Eg-
targets formal verification of distributed LLM training. Given a                   glog [36] further combines equality saturation with Datalog-style
logical model specification as the ground truth, it verifies that a dis-           reasoning to improve rule application efficiency. Beyond applying a
tributed parallel execution plan is mathematically equivalent to that              fixed rewrite set, several prior works study the automatic inference
specification. To scale to frontier models, TrainVerify introduces                 of rewrite rules. Ruler [17] and Enumo [20], for example, synthesize
a stage-wise verification algorithm together with shape-reduction                  rules from a grammar and an interpreter by enumerating candidate
techniques. Compared with our setting, TrainVerify focuses on                      expressions and validating semantic equivalence. TASO [10] and
parallelization equivalence within distributed training, whereas we                Mirage [34] are also related in that they enumerate graph substitu-
target cross-framework model implementations whose divergences                     tions and verify their correctness under known operator semantics,
                                                                              10
Verify Implementation Equivalence of Large Models                                                                                Conference’17, July 2017, Washington, DC, USA


but their goal is graph optimization rather than implementation                                  Operating Systems Design and Implementation (Carlsbad, CA, USA) (OSDI’18).
equivalence.                                                                                     USENIX Association, USA, 579–594.
                                                                                             [6] Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
   Our work differs in two important ways. First, we synthesize                                  2022. FLASHATTENTION: fast and memory-efficient exact attention with IO-
rules in the context of large deep learning computation graphs                                   awareness. In Proceedings of the 36th International Conference on Neural Informa-
                                                                                                 tion Processing Systems (New Orleans, LA, USA) (NIPS ’22). Curran Associates
rather than in a standalone algebraic domain. Second, our synthesis                              Inc., Red Hook, NY, USA, Article 1189, 16 pages.
procedure is guided by the shared-frontier structure induced by                              [7] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In
the current e-graph, which constrains the search space and enables                               Tools and Algorithms for the Construction and Analysis of Systems, C. R. Ramakr-
                                                                                                 ishnan and Jakob Rehof (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
practical rule discovery on real models.                                                         337–340.
                                                                                             [8] David Goldberg. 1991. What every computer scientist should know about floating-
                                                                                                 point arithmetic. ACM Comput. Surv. 23, 1 (March 1991), 5–48. doi:10.1145/103162.
8    Conclusion                                                                                  103163
                                                                                             [9] Aaron Grattafiori et al. 2024.                The Llama 3 Herd of Models.
In this paper, we presented Emerge, a verification engine for Im-                                arXiv:2407.21783 [cs.AI] https://arxiv.org/abs/2407.21783
plementation Equivalence. Instead of relying on manually written                            [10] Zhihao Jia, Oded Padon, James Thomas, Todd Warszawski, Matei Zaharia, and
                                                                                                 Alex Aiken. 2019. TASO: optimizing deep learning computation with automatic
rewrite rules, Emerge infers candidate relations from execution val-                             generation of graph substitutions. In Proceedings of the 27th ACM Symposium on
ues, synthesizes rules on demand, validates them, and propagates                                 Operating Systems Principles (Huntsville, Ontario, Canada) (SOSP ’19). Association
through a joint e-graph. Our current implementation and evalua-                                  for Computing Machinery, New York, NY, USA, 47–62. doi:10.1145/3341301.
                                                                                                 3359630
tion focus on inference computation graphs, and the results show                            [11] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, De-
that this execution-driven design is effective in practice: Emerge                               vendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel,
detects and localizes real implementation bugs, establishes equiva-                              Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux,
                                                                                                 Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix,
lence for correct model pairs at practical cost, and synthesizes rules                           and William El Sayed. 2023. Mistral 7B. arXiv:2310.06825 [cs.CL] https:
that compare with manually authored ones.                                                        //arxiv.org/abs/2310.06825
                                                                                            [12] Haitian Jiang, Shaowei Zhu, Zhen Zhang, Zhenyu Song, Xinwei Fu, Zhen Jia, Yida
                                                                                                 Wang, and Jinyang Li. 2026. TTrace: Lightweight Error Checking and Diagnosis
                                                                                                 for Distributed Training. arXiv:2506.09280 [cs.DC] https://arxiv.org/abs/2506.
References                                                                                       09280
 [1] Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad                  [13] Yuxuan Jiang, Ziming Zhou, Boyu Xu, Beijie Liu, Runhui Xu, and Peng Huang.
     Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl,                2025. Training with Confidence: Catching Silent Errors in Deep Learning Training
     Alon Benhaim, Misha Bilenko, Johan Bjorck, Sébastien Bubeck, Martin Cai, Qin                with Automated Proactive Checks. arXiv:2506.14813 [cs.LG] https://arxiv.org/
     Cai, Vishrav Chaudhary, Dong Chen, Dongdong Chen, Weizhu Chen, Yen-Chun                     abs/2506.14813
     Chen, Yi-Ling Chen, Hao Cheng, Parul Chopra, Xiyang Dai, Matthew Dixon, Ro-            [14] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,
     nen Eldan, Victor Fragoso, Jianfeng Gao, Mei Gao, Min Gao, Amit Garg, Allie Del             Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient
     Giorno, Abhishek Goswami, Suriya Gunasekar, Emman Haider, Junheng Hao,                      Memory Management for Large Language Model Serving with PagedAttention.
     Russell J. Hewett, Wenxiang Hu, Jamie Huynh, Dan Iter, Sam Ade Jacobs, Mojan                In Proceedings of the 29th Symposium on Operating Systems Principles (Koblenz,
     Javaheripi, Xin Jin, Nikos Karampatziakis, Piero Kauffmann, Mahoud Khademi,                 Germany) (SOSP ’23). Association for Computing Machinery, New York, NY, USA,
     Dongwoo Kim, Young Jin Kim, Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi               611–626. doi:10.1145/3600006.3613165
     Li, Yunsheng Li, Chen Liang, Lars Liden, Xihui Lin, Zeqi Lin, Ce Liu, Liyuan           [15] Chris Lattner, Mehdi Amini, Uday Bondhugula, Albert Cohen, Andy Davis,
     Liu, Mengchen Liu, Weishung Liu, Xiaodong Liu, Chong Luo, Piyush Madan, Ali                 Jacques Pienaar, River Riddle, Tatiana Shpeisman, Nicolas Vasilache, and Olek-
     Mahmoudzadeh, David Majercak, Matt Mazzola, Caio César Teodoro Mendes,                      sandr Zinenko. 2021. MLIR: Scaling Compiler Infrastructure for Domain Specific
     Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick, Barun Patra, Daniel                 Computation. In 2021 IEEE/ACM International Symposium on Code Generation
     Perez-Becker, Thomas Portet, Reid Pryzant, Heyang Qin, Marko Radmilac, Lil-                 and Optimization (CGO). 2–14. doi:10.1109/CGO51591.2021.9370308
     iang Ren, Gustavo de Rosa, Corby Rosset, Sambudha Roy, Olatunji Ruwase, Olli           [16] Yunchi Lu, Youshan Miao, Cheng Tan, Peng Huang, Yi Zhu, Xian Zhang, and
     Saarikivi, Amin Saied, Adil Salim, Michael Santacroce, Shital Shah, Ning Shang,             Fan Yang. 2025. TrainVerify: Equivalence-Based Verification for Distributed LLM
     Hiteshi Sharma, Yelong Shen, Swadheen Shukla, Xia Song, Masahiro Tanaka,                    Training. In Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems
     Andrea Tupini, Praneetha Vaddamanu, Chunyu Wang, Guanhua Wang, Lijuan                       Principles (Lotte Hotel World, Seoul, Republic of Korea) (SOSP ’25). Association
     Wang, Shuohang Wang, Xin Wang, Yu Wang, Rachel Ward, Wen Wen, Philipp                       for Computing Machinery, New York, NY, USA, 237–253. doi:10.1145/3731569.
     Witte, Haiping Wu, Xiaoxia Wu, Michael Wyatt, Bin Xiao, Can Xu, Jiahang Xu,                 3764850
     Weijian Xu, Jilong Xue, Sonali Yadav, Fan Yang, Jianwei Yang, Yifan Yang, Ziyi         [17] Chandrakana Nandi, Max Willsey, Amy Zhu, Yisu Remy Wang, Brett Saiki, Adam
     Yang, Donghan Yu, Lu Yuan, Chenruidong Zhang, Cyril Zhang, Jianwen Zhang,                   Anderson, Adriana Schulz, Dan Grossman, and Zachary Tatlock. 2021. Rewrite
     Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan Zhang, and Xiren Zhou. 2024. Phi-3                rule inference using equality saturation. Proc. ACM Program. Lang. 5, OOPSLA,
     Technical Report: A Highly Capable Language Model Locally on Your Phone.                    Article 119 (Oct. 2021), 28 pages. doi:10.1145/3485496
     arXiv:2404.14219 [cs.CL] https://arxiv.org/abs/2404.14219                              [18] NVIDIA Corporation. 2025. Megatron Core. https://developer.nvidia.com/
 [2] Shakkeel Ahmed, Prakash Bisht, Ravi Mula, and Soma S Dhavala. 2021. A Deep                  megatron-core.
     Learning framework for Interoperable Machine Learning. In Proceedings of the           [19] NVIDIA Megatron-LM Contributors. 2024. Incorrect loss scaling in context par-
     First International Conference on AI-ML Systems (Bangalore, India) (AIMLSystems             allel code logic. https://github.com/NVIDIA/Megatron-LM/issues/673. GitHub
     ’21). Association for Computing Machinery, New York, NY, USA, Article 23,                   Issue #673.
     7 pages. doi:10.1145/3486001.3486243                                                   [20] Anjali Pal, Brett Saiki, Ryan Tjoa, Cynthia Richey, Amy Zhu, Oliver Flatt, Max
 [3] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan,              Willsey, Zachary Tatlock, and Chandrakana Nandi. 2023. Equality Saturation
     Wenbin Ge, Yu Han, Fei Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Runji               Theory Exploration à la Carte. Proc. ACM Program. Lang. 7, OOPSLA2, Article
     Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin Ma, Rui Men,                  258 (Oct. 2023), 29 pages. doi:10.1145/3622834
     Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng                [21] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
     Wang, Shijie Wang, Wei Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang,                    Sutskever. 2019. Language Models are Unsupervised Multitask Learners. OpenAI
     Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi Yuan, Zheng                  Blog (2019). https://cdn.openai.com/better-language-models/language_models_
     Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang                     are_unsupervised_multitask_learners.pdf
     Zhou, Jingren Zhou, Xiaohuan Zhou, and Tianhang Zhu. 2023. Qwen Technical              [22] James Reed, Zachary DeVito, Horace He, Ansley Ussery, and Jason Ansel. 2022.
     Report. arXiv:2309.16609 [cs.CL] https://arxiv.org/abs/2309.16609                           torch. fx: Practical program capture and transformation for deep learning in
 [4] Stas Bekman. 2022. BLOOM: Megatron-DeepSpeed. https://huggingface.co/                       python. Proceedings of Machine Learning and Systems 4 (2022), 638–651.
     blog/bloom-megatron-deepspeed                                                          [23] Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri
 [5] Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Meghan                 Dao. 2024. FlashAttention-3: fast and accurate attention with asynchrony and low-
     Cowan, Haichen Shen, Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin,                     precision. In Proceedings of the 38th International Conference on Neural Information
     and Arvind Krishnamurthy. 2018. TVM: an automated end-to-end optimizing                     Processing Systems (Vancouver, BC, Canada) (NIPS ’24). Curran Associates Inc.,
     compiler for deep learning. In Proceedings of the 13th USENIX Conference on                 Red Hook, NY, USA, Article 2193, 28 pages.
                                                                                       11
Conference’17, July 2017, Washington, DC, USA                                                                                          Qi Zhan, Xing Hu, Xin Xia, and Shanping Li


[24] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le,                      Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu,
     Geoffrey Hinton, and Jeff Dean. 2017. Outrageously Large Neural Networks:                     Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest,
     The Sparsely-Gated Mixture-of-Experts Layer. arXiv:1701.06538 [cs.LG] https:                  and Alexander Rush. 2020. Transformers: State-of-the-Art Natural Language
     //arxiv.org/abs/1701.06538                                                                    Processing. In Proceedings of the 2020 Conference on Empirical Methods in Natural
[25] Robert Endre Tarjan. 1975. Efficiency of a Good But Not Linear Set Union                      Language Processing: System Demonstrations, Qun Liu and David Schlangen (Eds.).
     Algorithm. J. ACM 22, 2 (April 1975), 215–225. doi:10.1145/321879.321884                      Association for Computational Linguistics, Online, 38–45. doi:10.18653/v1/2020.
[26] Ross Tate, Michael Stepp, Zachary Tatlock, and Sorin Lerner. 2009. Equality                   emnlp-demos.6
     saturation: a new approach to optimization. SIGPLAN Not. 44, 1 (Jan. 2009),              [34] Mengdi Wu, Xinhao Cheng, Shengyu Liu, Chunan Shi, Jianan Ji, Man Kit Ao,
     264–276. doi:10.1145/1594834.1480915                                                          Praveen Velliengiri, Xupeng Miao, Oded Padon, and Zhihao Jia. 2025. Mirage: a
[27] Philippe Tillet, H. T. Kung, and David Cox. 2019. Triton: an intermediate lan-                multi-level superoptimizer for tensor programs. In Proceedings of the 19th USENIX
     guage and compiler for tiled neural network computations. In Proceedings of the               Conference on Operating Systems Design and Implementation (Boston, MA, USA)
     3rd ACM SIGPLAN International Workshop on Machine Learning and Program-                       (OSDI ’25). USENIX Association, USA, Article 13, 18 pages.
     ming Languages (Phoenix, AZ, USA) (MAPL 2019). Association for Computing                 [35] XLA and TensorFlow Teams. 2017. XLA—TensorFlow, Compiled. https:
     Machinery, New York, NY, USA, 10–19. doi:10.1145/3315508.3329973                              //developers.googleblog.com/2017/03/xla-tensorflow-compiled.html.
[28] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,                 [36] Yihong Zhang, Yisu Remy Wang, Oliver Flatt, David Cao, Philip Zucker, Eli
     Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you               Rosenthal, Zachary Tatlock, and Max Willsey. 2023. Better Together: Unifying
     need. In Proceedings of the 31st International Conference on Neural Information               Datalog and Equality Saturation. Proc. ACM Program. Lang. 7, PLDI, Article 125
     Processing Systems (Long Beach, California, USA) (NIPS’17). Curran Associates                 (June 2023), 25 pages. doi:10.1145/3591239
     Inc., Red Hook, NY, USA, 6000–6010.                                                      [37] Lianmin Zheng, Chengfan Jia, Minmin Sun, Zhao Wu, Cody Hao Yu, Ameer
[29] vLLM Contributors. 2023. GPT-J: Incorrect RoPE rotation scheme. https://github.               Haj-Ali, Yida Wang, Jun Yang, Danyang Zhuo, Koushik Sen, Joseph E. Gonzalez,
     com/vllm-project/vllm/issues/590. GitHub Issue #590.                                          and Ion Stoica. 2020. Ansor: generating high-performance tensor programs
[30] vLLM Contributors. 2024. Wrong split_qkv execution semantics in tensor                        for deep learning. In Proceedings of the 14th USENIX Conference on Operating
     parallel (InternLM2). https://github.com/vllm-project/vllm/issues/8017. GitHub                Systems Design and Implementation (OSDI’20). USENIX Association, USA, Article
     Issue #8017.                                                                                  49, 17 pages.
[31] Zhanghan Wang, Ding Ding, Hang Zhu, Haibin Lin, and Aurojit Panda. 2026. It              [38] Kahfi S. Zulkifli, Wenbo Qian, Shaowei Zhu, Yuan Zhou, Zhen Zhang, and Chang
     Takes Two to Entangle. In Proceedings of the 31st ACM International Conference on             Lou. 2025. Verifying Computational Graphs in Production-Grade Distributed
     Architectural Support for Programming Languages and Operating Systems, Volume                 Machine Learning Frameworks. arXiv:2509.10694 [cs.LG] https://arxiv.org/abs/
     2 (USA) (ASPLOS ’26). Association for Computing Machinery, New York, NY,                      2509.10694
     USA, 1022–1039. doi:10.1145/3779212.3790178                                              [39] Kahfi S. Zulkifli, Wenbo Qian, Shaowei Zhu, Yuan Zhou, Zhen Zhang, and Chang
[32] Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock,                Lou. 2025. Verifying Semantic Equivalence of Large Models with Equality Sat-
     and Pavel Panchekha. 2021. egg: Fast and extensible equality saturation. Proc.                uration. In Proceedings of the 5th Workshop on Machine Learning and Systems
     ACM Program. Lang. 5, POPL, Article 23 (Jan. 2021), 29 pages. doi:10.1145/3434304             (World Trade Center, Rotterdam, Netherlands) (EuroMLSys ’25). Association for
[33] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue,                  Computing Machinery, New York, NY, USA, 82–89. doi:10.1145/3721146.3721943
     Anthony Moi, Pierric Cistac, Tim Rault, Remi Louf, Morgan Funtowicz, Joe




                                                                                         12
