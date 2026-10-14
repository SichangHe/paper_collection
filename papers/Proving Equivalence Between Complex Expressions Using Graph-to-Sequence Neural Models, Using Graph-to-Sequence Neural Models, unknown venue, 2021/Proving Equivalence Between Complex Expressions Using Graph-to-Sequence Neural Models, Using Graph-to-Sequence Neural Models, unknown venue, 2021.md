                                            Proving Equivalence Between Complex Expressions
                                                 Using Graph-to-Sequence Neural Models
                                                                            Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet
                                        Abstract                                                                matrices, scalars, and a vector: (𝐴 +𝐵)𝐼 ((𝑎 + (𝑏 −𝑏))/𝑎)®𝑣 −𝐴® 𝑣
                                        We target the problem of provably computing the equiva-                 can be proven equivalent to 𝐵®    𝑣 by applying 10 axioms in
                                        lence between two complex expression trees. To this end, we             sequence; our work generates the proof steps between these
                                        formalize the problem of equivalence between two such pro-              expressions.
                                        grams as finding a set of semantics-preserving rewrite rules                While prior work has shown promises for deep networks
                                        from one into the other, such that after the rewrite the two            to compute some forms of program equivalence [5, 62], the
arXiv:2106.02452v2 [cs.PL] 9 Jun 2021




                                        programs are structurally identical, and therefore trivially            system typically outputs only a probability of equivalence,
                                        equivalent. We then develop a graph-to-sequence neural net-             without any reasoning or insight that can be verified easily:
                                        work system for program equivalence, trained to produce                 false positive can be produced. Programs can be represented
                                        such rewrite sequences from a carefully crafted automatic               as a tree (or graph) of symbols, and deep networks for sym-
                                        example generation algorithm. We extensively evaluate our               bolic reasoning have been studied, e.g. to compute the deriv-
                                        system on a rich multi-type linear algebra expression lan-              ative of a symbolic expression [38]. In this work, we take a
                                        guage, using arbitrary combinations of 100+ graph-rewriting             significantly different approach to the problem of symbolic
                                        axioms of equivalence. Our machine learning system guar-                program reasoning with deep networks: we make the sys-
                                        antees correctness for all true negatives, and ensures 0 false          tem produce the sequence of steps that lead to rewriting one
                                        positive by design. It outputs via inference a valid proof of           program into another, that is the reasoning for (or proof of)
                                        equivalence for 93% of the 10,000 equivalent expression pairs           equivalence between the two programs, instead of produc-
                                        isolated for testing, using up to 50-term expressions. In all           ing directly the result of this reasoning (e.g., a probability of
                                        cases, the validity of the sequence produced and therefore              equivalence, without explanation about the reasoning). In a
                                        the provable assertion of program equivalence is always                 nutshell, we approach expression equivalence as a theorem
                                        computable, in negligible time.                                         proving problem, in which all the axioms as well as tactics
                                                                                                                to compute a proof are all learned by example in a deep
                                                                                                                learning system, without any human insight.
                                        1    Introduction
                                                                                                                    We propose a method for generating training samples
                                        Deep neural network systems have excelled at a variety of               using probabilistic applications of production rules within
                                        classification and reinforcement learning tasks [26]. How-              a formal grammar, and then develop a graph-to-sequence
                                        ever, their stochastic nature tends to hinder their deployment          [13, 40] neural network system for program equivalence,
                                        for automated program analysis: ensuring the correctness                trained to learn and combine rewrite rules to rewrite one
                                        of the solution produced is often required, e.g., when deter-           program into another. It can deterministically prove equiva-
                                        mining the semantics equivalence between two programs                   lence, entirely avoids false positives, and quickly invalidates
                                        (or symbolic expressions).                                              incorrect answers produced by the network (no determin-
                                           In this work we target the problem of automatically com-             istic answer is provided in this case, only a probability of
                                        puting whether two input symbolic expressions are semanti-              non-equivalence). In a nutshell, we develop the first graph-
                                        cally equivalent [31], under a well-defined axiomatic system            to-sequence neural network system to accelerate the search
                                        for equivalence using semantics-preserving rewrite rules                in the space of possible combinations of transformation rules
                                        [21]. Program equivalence is summarized as determining                  (i.e., axioms of equivalence in the input language) to make
                                        whether two programs would always produce the same out-                 two graphs representing symbolic expressions structurally
                                        puts for all possible inputs, and is a central problem in com-          identical without violating their original semantics. We pro-
                                        puting [23, 31, 55]. The problem ranges from undecidable, e.g.          pose a machine learning system for program equivalence
                                        [25], to trivial in cases of testing the equivalence of a program       which ensures correctness for all non-equivalent programs
                                        with itself. Our work directly studies the subset of programs           input (specificity = 100%) , and a deterministically checkable
                                        represented by symbolic linear algebra expressions which                output for equivalent programs (no false positives). We make
                                        include scalar, vector, and matrix types for both constants             the following contributions:
                                        and variables, and 16 different operators with 147 distinct
                                        axioms of equivalence. For example, the expression using                   1. We design, implement and evaluate two competing
                                                                                                                      approaches using graph-to-sequence neural network
                                        pe-graph2axiom, June, 2021, ArXiV
                                        2021.
                                                                                                                      systems to generate proofs of equivalence. We provide
                                                                                                            1
pe-graph2axiom, June, 2021, ArXiV                                         Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet


                   ∗                                ∗                                    +                                 +
           𝑎               +
                   ∗               ∗            𝑎       +                        ∗               ∗                 ∗               ∗
               1       𝑏       1       𝑐            𝑏       𝑐                𝑎       𝑏       𝑎       𝑐         𝑎       𝑐       𝑎       𝑏
      (a) 𝑎 ∗ (1 ∗ 𝑏 + 1 ∗ 𝑐)               (b) 𝑎 ∗ (𝑏 + 𝑐)                  (c) 𝑎 ∗ 𝑏 + 𝑎 ∗ 𝑐                 (d) 𝑎 ∗ 𝑐 + 𝑎 ∗ 𝑏

                                                Figure 1. Examples of Computations

       the first implementation of such graph-to-sequence                    To assess the validity of a transformation sequence 𝑆
       systems in the popular OpenNMT-py framework [34].                  where 𝑃2 = 𝑆 (𝑃1), one simply needs to check for 𝑆, in se-
    2. We present a complete implementation of our system                 quence, that each axiom is applicable at that program point,
       operating on a rich language for multi-type linear alge-           apply it to obtain a new temporary program, and repeat
       bra expressions. Our system provides a correct rewrite             the process for each axiom in the complete sequence. If the
       rule sequence between two equivalent programs for                  sequence is verified to be valid, and 𝑆 (𝑃1) is structurally
       93% of the 10,000 test cases. The correctness of the               equivalent to 𝑃2, then we have proved 𝑃1 ≡ 𝑃2, and 𝑆 forms
       rewrite rule is deterministically checkable in all cases           the complete proof of equivalence between the two pro-
       in negligible time.                                                grams. Using 𝐴2 : 𝑥 ∗ (𝑦 + 𝑧) = 𝑥 ∗ 𝑦 + 𝑥 ∗ 𝑧, ∀𝑥, 𝑦, 𝑧 ∈ N
   The rest of the paper is organized as follows. Sec. 2 out-             and 𝐴3 : 𝑥 + 𝑦 = 𝑦 + 𝑥, ∀𝑥, 𝑦 ∈ N, we have 𝑃1 ≡ 𝑃4 ≡
lines the program equivalence problem we address, and mo-                 𝐴3(+, 𝐴2(∗, 𝐴1(𝑐, 𝐴1(𝑏, 𝑃1)))), a verifiable proof of equiva-
tivates our proposed approach. Sec. 3 formalizes the equiv-               lence under our axioms between the programs 𝑎(1𝑏 +1𝑐) and
alence problem addressed. Automatic sample generation is                  𝑎𝑐 + 𝑎𝑏, which involved structural changes including node
discussed in Sec. 4 before Sec. 5 which introduces our DNN                deletion, creation and edge modification. Note the bidirec-
system, its overall design principles and key components. A               tional nature of the process: one can rewrite from 𝑎(1𝑏 + 1𝑐)
complete experimental evaluation of our system is detailed in             to 𝑎𝑐 + 𝑎𝑏, or the converse using the same (but reverted) se-
Sec. 6. We present related work in Sec. 7 before concluding.              quence. Note also the non-unicity of a sequence: by possibly
                                                                          many ways a program can be rewritten into another one,
2    Motivation and Overview                                              for example the sequence 𝑃4 ≡ 𝐴3(+, 𝐴1(𝑐, 𝐴1(𝑏, 𝐴2(∗, 𝑃1))
Rewrite rules as axioms of equivalence In this work we                    also correctly rewrites 𝑃1 into 𝑃4. Conversely, a sequence
represent programs with symbolic expressions made of vari-                may not exist: for example no sequence of the 3 above axioms
ables (e.g., 𝑎, 𝑏, 𝑐), operators (e.g., +, *) and neutral/absorbing       allow to rewrite 𝑎 +𝑏 into 𝑎 ∗𝑏. We call these non-equivalent
elements (e.g., 1). We consider a rich linear algebra expression          in our system, that is precisely if there is no sequence of
language, supporting three variable types (scalars as shown               axioms that can be applied to rewrite one program into the
in P1-P4, vectors, and matrices) and 5 different variables                other. Our approach aims to compute some 𝑆 for a pair of
per type; 16 operators including operators mixing different               programs 𝑃1, 𝑃2, so that 𝑆 is verified correct when 𝑃1 ≡ 𝑃2.
variable types such as vector-matrix product. We represent                Consequently, if 𝑃1 . 𝑃2, no sequence 𝑆 produced can be
these programs as dataflow graphs [16] with a single root                 verified correct: true negatives are trivially detected.
node, that is to compute a single value.
    P1 is equivalent to P2 if we consider the axiom 𝐴1 : 1N ∗𝑥 =          Pathfinding program equivalence proofs Intuitively, we
𝑥, ∀𝑥 ∈ N. This axiom is also a clear rewrite rule: the LHS               can view the solution space as a graph, where every possi-
expression 1N ∗ 𝑥 (with 𝑥 ∈ N) can be matched and replaced                ble syntactically different program in the language is rep-
by the RHS expression 𝑥 anywhere in the program with-                     resented by its own vertex 𝑣𝑖 . And ∃ 𝑒 (𝐴𝑘 ,𝑥) : 𝑣𝑖 → 𝑣 𝑗 iff
out altering its semantics. An axiom, or equivalently here a              ∃𝐴𝑘 an axiom and 𝑥 a node in 𝑣𝑖 such that 𝑣 𝑗 = 𝐴𝑘 (𝑥, 𝑣𝑖 ).
graph rewrite rule, may be applied repeatedly to different                Any two programs connected by a path in this graph are
subtrees. When applying 𝐴1 on a specific location, the node               therefore semantically equivalent. Building 𝑆 for 𝑃1 ≡ 𝑆 (𝑃2)
𝑏 of 𝑃1, we obtain an equivalent and yet syntactically differ-            amounts to exposing one path between 𝑃1 and 𝑃2 in this
ent program, we note 𝑃1 ≡ 𝐴1(𝑏, 𝑃1). These equivalences                   graph when it exists, the path forming the proof of equiva-
can be composed, incrementally, to form a complex transfor-               lence. We build a deep learning graph-to-sequence system to
mation: we have 𝑃1 ≡ 𝐴1(𝑐, 𝐴1(𝑏, 𝑃1)). The result of these                learn a stochastic approximation of an iterative algorithm to
semantics-preserving transformations can be computed in                   construct such feasible path when possible, trained only by
sequence: first implement 𝐴1(𝑏, 𝑃1) to obtain a new program               randomly sampling pairs of programs and one carefully la-
𝑃 ′, then 𝐴1(𝑐, 𝑃 ′) to obtain 𝑃 ′′. To prove 𝑃1 ≡ 𝑃2, we simply          beled path between them. This avoids the need to craft smart
check 𝑃 ′′ is structurally identical to 𝑃2, a linear time process.
                                                                      2
Proving Equivalence Between Complex Expressions                                               pe-graph2axiom, June, 2021, ArXiV




                                       Figure 2. pe-graph2axiom System Overview
exploration heuristics to make this path-finding problem              and location on which it is applied. As developed below, we
practical.                                                            specifically study the robustness of our approach to generate
                                                                      proofs of increasingly complex length, contrasting models
Graph-to-sequence network for pathfinding This is in-                 to output the entire path at once with pe-graph2axiom
stead what we let the neural network learn automatically;             which incrementally builds the sequence one step at a time,
and specifically why we implemented graph neural networks             as shown in Sec. 6.
to solve this problem [51, 62]. We rely on the network to
suggest a transformation path by inference, and then verify           3     Framework for Program Equivalence
its validity in linear time. To implement our approach, we            We now present the formalism we use in this work to repre-
enumerate randomly valid sentences in a language, and a set           sent symbolic expressions and their equivalences. We care-
of axioms of equivalence expressible as semantics-preserving          fully co-designed this problem representation and the (graph)
rewrite rules from one to the other. The system in Fig. 2 takes       neural network approach to make the best use of machine
as input two programs represented as symbolic trees, and              learning via deep networks, as discussed in Sec. 5.
produces a sequence of axioms along with their position of
application (or node) that can be used to rewrite sequentially        3.1   Input Representation
one input program into the other input program. To train              A key design aspect is to match the capability of the neu-
the system, we generate pairs of equivalent programs by it-           ral network to model the input as a walkable graph with
erating the axioms with random probability on one program,            the actual input program representation to be handled. We
thereby generating both a path to equivalence and the target          therefore model “programs” in a dataflow-like representa-
program. Random programs are generated so as to respect               tion (i.e., a directed graph), using a single root/output node.
the grammar defined. The training set is then appropriately           Symbolic expressions computing a single result typically fit
selected from these random samples, as detailed in Sec. 6.            this representation. The following definitions are applica-
Node initialization initializes the graph neural network, con-        ble to programs represented as dataflow graphs, albeit we
verting the input programs text (e.g., (𝑎 + (𝑏 + 𝑐)) into nodes       specialize them to symbolic expressions.
and edges in the Graph Neural Network [51, 62]. The details
of the network are covered in Sec. 5. In a nutshell, the key          Definition 3.1 (Expression graph node). A node 𝑛 ∈ 𝑁
principle is to combine a memory-based neural network ap-             in the expression graph models n-ary operations and input
proach, e.g., using Long-Short Term Memory (LSTM) [28]                operands. A node produces a value which can be consumed
neurons and a graph neural network design (which uses                 by any of its immediate successors in the graph. When a node
Gated Recurrent Units (GRUs) internally) [13] that matches            has no predecessor, it models an input value. The output
our program graph representation. Token embedding is a                value for the computation is produced by the unique root
neural network layer in which tokens are assigned a learn-            node 𝑛𝑟𝑜𝑜𝑡 of the graph, the only node without successor.
able multidimensional embedding vector [44]. Each layer
                                                                      Definition 3.2 (Expression graph directed edge). A directed
in LSTM 2 layers has 256 neurons, which support sequence
                                                                      edge 𝑒𝑛1,𝑛2 : 𝑛 1 → 𝑛 2 with 𝑛 1, 𝑛 2 ∈ 𝑁 in the expression graph
generation. Token generator is the final output portion of the
                                                                      connects the producer of a value (𝑛 1 ) to a node consuming
network. It learns to output the tokens based on the current
                                                                      this value in the computation.
LSTM hidden states and the Global Attention from the graph
neural network. As each token is output, it feeds back into           Definition 3.3 (Expression graph). A expression graph 𝐺 is
the LSTM layer through the embedding layer to affect its              a directed dataflow graph modeling the computation, made
next state. We use a sequence generation principle, using a           of nodes 𝑛𝑖 ∈ 𝑁 and edges 𝑒𝑛𝑖 ,𝑛 𝑗 ∈ 𝐸 as defined in Def. 3.1
global attention mechanism [42] to allow observation of pro-          and Def. 3.2. That is, 𝐺 = ⟨𝑛𝑟𝑜𝑜𝑡 , 𝑁 , 𝐸⟩. There is no dandling
gram graph node information while generating the axiom                edge nor unconnected node in 𝐺.
                                                                  3
pe-graph2axiom, June, 2021, ArXiV                                         Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

Language of linear algebra expressions We developed a                     complex graph modifications, such as node deletion or cre-
complex-enough language to evaluate carefully our work,                   ation, subtree manipulation, multi-node graph changes, etc.
that captures rich linear algebra expressions. Specifically, we              A graph pattern can be viewed as a pattern-matching
support 3 types of data/variables in the expression: scalars,             rule on graphs and its precise applicability criteria. It can
vectors and matrices. We use the standard notation 𝑎, 𝑎,      ®𝐴          also be viewed as a sentential form of the language grammar,
for scalars, vectors and matrices. We evaluate using different            e.g. ScalarVal PlusOp ScalarVal is a pattern, if the
variable names for each of the 3 types above, along with                  grammar is well formed.
their identity and absorbing elements.
                                                                          Definition 3.4 (Graph pattern). A graph pattern 𝑃 is an un-
   We also model a rich set of operators, mixing different
                                                                          ambiguous structural description of a (sub-)graph 𝐺 𝑃 , which
unary and binary operations for each type. Specifically, we
                                                                          can be deterministically matched in any expression graph 𝐺.
support ∗𝑠 , +𝑠 , −𝑠 , /𝑠 between scalar operands, and +𝑣 , −𝑣 , ∗𝑣
                                                                          We have 𝑃 = ⟨𝐺 𝑃 , 𝑀𝑛 , 𝑀𝑒 ⟩ where for each node 𝑛𝑖 ∈ 𝑁 𝐺𝑃 ,
between vectors and +𝑚 , −𝑚 , ∗𝑚 for matrices. For −, / we
                                                                          {𝑛𝑚𝑎𝑡𝑐ℎ } = 𝑀𝑛 (𝑛𝑖 ) returns the set of node values 𝑛𝑚𝑎𝑡𝑐ℎ
also support their unary version for all types, e.g. −1𝑠 for
                                                                          accepted to match 𝑛𝑖 on a graph 𝐺. For 𝑛𝑖 , 𝑛 𝑗 ∈ 𝑁 𝐺𝑃 , 𝑒𝑖 =
unary scalar inversion and −𝑢𝑚 for unary matrix negation.
                                                                          𝑀𝑒 (𝑛𝑖 , 𝑛 𝑗 ) returns the set of edges between 𝑀 (𝑛𝑖 ) and 𝑀 (𝑛 𝑗 )
For example 𝑎 −1𝑠 computes to 1/𝑎. We also support multi-
                                                                          to be matched in 𝐺. A pattern 𝐺 𝑃 is matched in 𝐺 if (a) ∀𝑛𝑖 ∈
type operations, such as vector and matrix scaling by a scalar
                                                                          𝐺 𝑝 , ∃ 𝑛𝑚 = 𝑀 (𝑛𝑖 ) ∈ 𝑁 𝐺 ; (b) ∀𝑒𝑖 ∈ 𝐸𝐺𝑃 , ∃ 𝑒𝑀𝑛 (𝑛𝑖 ),𝑀𝑛 (𝑛 𝑗 ) =
∗𝑠𝑣 , ∗𝑠𝑚 . We support two specific unary matrix operations,
transpose 𝑡𝑚 and matrix inversion as −1𝑚 . Note every opera-              𝑀𝑒 (𝑛𝑖 , 𝑛 𝑗 ) ∈ 𝐸𝐺 ; and (c) 𝑒𝑀𝑛 (𝑛𝑖 ),𝑀𝑛 (𝑛 𝑗 ) ∈ 𝐸𝐺 ≠ 𝑀𝑒 (𝑛𝑖 , 𝑛 𝑗 ).
tor has a unique name in our language, driven by the type of                Note when a graph pattern models a rewrite, 𝑀𝑛 and 𝑀𝑒
its operand. This will facilitate the learning of the expression          are adjusted accordingly to output the rewrite of a node
embedding, avoiding the need to learn type propagation.                   𝑛 ∈ 𝑁 𝐺 into its desired value, instead of the set of acceptable
                                                                          nodes from 𝑛 ∈ 𝑁 𝐺𝑃 .
Examples Expressions of the form 𝐴(𝐵𝐶 𝑡 𝐷)𝐸 −1 , 𝑎® +𝑏®  𝑐 −1 −
 𝑒 , (𝑎 +𝑏) + (𝑐 (𝑑/𝑒)), (𝑎𝐴 +𝑏𝐵)𝐶 etc. can be parsed trivially
0®                                𝑡                                       Definition 3.5 (Axiom of equivalence). An axiom 𝐴 is a
to our representation, one simply needs to be able to provide             semantics-preserving rewrite rule 𝐺 ′ = 𝐴(𝑛, 𝐺) that can ar-
a unique name for each operand and operator type (possibly                bitrarily modify a expression graph 𝐺, and produces another
via some analysis, or simple language design principles),                 expression graph 𝐺 ′ respecting Def. 3.3 with identical se-
that is avoiding to overload the semantics of operators and               mantics to 𝐺. We note 𝐴 : ⟨𝑃𝑚𝑎𝑡𝑐ℎ , 𝑃𝑟𝑒𝑝𝑙𝑎𝑐𝑒 ⟩ an axiom, where
operands. Note the semantics is never explicitly provided to              𝑃𝑚𝑎𝑡𝑐ℎ , 𝑃𝑟𝑒𝑝𝑙𝑎𝑐𝑒 are graph patterns as per Def. 3.4. The appli-
our DNN approach, it is learned by examples. There will be                cation of axiom 𝐴 to node 𝑛 in 𝐺 is written 𝐴(𝑛, 𝐺).
no example of the form e.g. 𝑎 + 𝐴, an invalid expression in
                                                                            We can compose axioms to form a complex rewrite se-
our language.
                                                                          quence.
    We believe a sensible approach is to develop a clean, reg-
ular grammar for the language to be handled, as implicitly                Definition 3.6 (Semantics-preserving axiom composition).
these are concepts the DNN will need to learn. We did so,                 Given a sequence 𝑆 : 𝐴1 (𝑛 1, 𝐴2 (𝑛 2, ..., 𝐴𝑚 (𝑛𝑚 , 𝐺))) of 𝑚 ax-
using a classical LL(1) grammar description of our linear al-             ioms applications. It is a semantics-preserving composition
                                                                                                                𝐴𝑖
gebra language. This is not a requirement of our approach, as             if for each 𝐺 𝑗 = 𝐴𝑖 (𝑛𝑖 , 𝐺𝑖 ) ∈ 𝑆, 𝑃𝑚𝑎𝑡𝑐ℎ succeeds on the sub-
one can arrive to the desired input expression graph by any               graph with root 𝑛𝑖 in 𝐺𝑖 , and 𝐺 𝑗 is obtained by applying
means necessary, but we believe making the reasoning on                     𝐴𝑖
                                                                          𝑃𝑟𝑒𝑝𝑙𝑎𝑐𝑒 to 𝑛𝑖 .
the language structure “easy” is an important design aspect.
                                                                          Theorem 3.7 (Expression graph equivalence). Given a ex-
3.2   Axioms of Equivalence                                               pression 𝐺. If 𝐺 ′ = 𝑆 (𝐺) such that 𝑆 is a semantics-preserving
                                                                          sequence as per Def. 3.6, then 𝐺 ≡ 𝐺 ′, they are equivalent
A central aspect of our approach is to view the problem of ex-
                                                                          under the axiom system used in 𝑆.
pression equivalence as finding a sequence of locally-correct
rewrite rules that each preserve the semantics, thereby mak-                 This is a direct consequence of using only semantics-
ing incremental reasoning possible. We explicitly do not con-             preserving axioms, each rewrite cannot individually alter
sider non-semantics-preserving axioms. A rich structure of                the semantics, so such incremental composition does not. It
alternate but equivalent ways to rewrite one expression to an-            leads to the formal problem we are addressing:
other makes the problem easier to sample and more amenable
to machine learning. Semantics-preserving axioms enable                   Corollary 3.8 (Expression graphs equivalence matching).
incremental per-axiom reasoning, and enforce semantics                    Given two expressions 𝐺, 𝐺 ′. If there exist a semantics-preserving
preservation without overly complicated semantics analysis;               sequence 𝑆 such that 𝐺 ′ = 𝑆 (𝐺), then 𝐺 ≡ 𝐺 ′.
while still manipulating a very rich space of transformations.              Note here = means complete structural equivalence be-
To illustrate this we specifically design axioms that perform             tween the two graphs: they are identical in structure and
                                                                      4
Proving Equivalence Between Complex Expressions                                                      pe-graph2axiom, June, 2021, ArXiV

label/node values. Determining 𝐺 = 𝐺 ′ amounts to visiting                       The proof is a direct consequence of Def. 3.9. In this work,
both graphs simultaneously e.g. in depth-first search from                    we randomly sample this exact graph to learn how to build
the root to ensure structural equivalence, and also verifying                 paths between arbitrary expressions. As it is a multigraph,
the same node labels appear in both at the same time. This                    there will be possibly many different sequences modeled to
is trivally implemented in linear time in the graph size.                     prove the equivalence between two expressions. It is suffi-
                                                                              cient to expose one to prove equivalence.
Language of linear algebra expressions We have imple-
memented a total of 102 different axioms for our language,
made of the multi-type versions of the 13 core restructur-                    Corollary 3.11 (Semantics-preserving rewrite sequence).
ing axioms described later in Table 1. They all follow estab-                 Any directed path in 𝐺 𝑒𝑞𝑢𝑖𝑣 is a semantics-preserving rewrite
lished linear algebra properties. Note different data types                   sequence between the expressions, described by the sequence of
have different axioms following typical linear algebra rules,                 axioms and expression position labeling the edges in this path.
e.g., matrix-multiplication does not commute, but scalar                      This sequence forms the proof of equivalence.
and vector multiplications do. Examples of axioms include
𝑥 (𝑦𝑧) → (𝑥𝑦)𝑧, 𝑋 − 𝑋 → 𝑂, −(𝑥® − 𝑦)   ® → 𝑦® − 𝑥,
                                                        𝑡
                                                ® or 𝑋 𝑡 → 𝑋 ,                   We believe that ensuring there are possibly (usually) many
an exhaustive list is displayed in the Supplementary Material.                ways to compute a proof of equivalence in our specific frame-
   In our experiments, we presume matrix and vector dimen-                    work is key to enable the DNN approach to learn automat-
sions are appropriate for the given operation. Such dimen-                    ically the pathfinding algorithm for building such proofs.
sion compatibility checks are simple to implement by e.g.                     Other more compact representations of this space of equiva-
introducing additional nodes in the prgram representation,                    lences are clearly possible, including by folding nodes in the
but are not considered in our test language.                                  equivalence graph for structurally-similar expressions and
                                                                              folding equivalent paths between nodes. When building e.g.
Examples We illustrate axiom-based rewrites using ax-                         a deterministic algorithm for pathfinding, such space size
ioms presented in later Table 1. Note axiom names follow                      reduction would bring complexity benefits [11, 31]. We be-
the structural changes applied. For example, we have 𝑎 + 𝑏 ≡                  lieve that for the efficient deployment of graph-to-sequence
𝑏 + 𝑎 : {𝑎 + 𝑏} = 𝐶𝑜𝑚𝑚𝑢𝑡𝑒 ({+}, {𝑏 + 𝑎}). 𝑎 + 𝑏 + 𝑐 ≡ 𝑏 + 𝑐 +                 systems, exposing significant redundancy in the space fa-
𝑎 : {𝑎 +𝑏 +𝑐} = 𝐶𝑜𝑚𝑚𝑢𝑡𝑒 ({+1 }, 𝐶𝑜𝑚𝑚𝑢𝑡𝑒 ({+2 }, {𝑏 +𝑐 +𝑎}).                   cilitates the learning process. We also alleviate the need to
Note we refer to different nodes with the same symbol (e.g.,                  reason on the properties of this space to find an efficient
+2 ) subscripting them by their order in a DFS traversal of the               traversal heuristic.
expression graph, starting from the unique root. We have
0 ≡ 𝑎 − 𝑎 : {0} = 𝐶𝑎𝑛𝑐𝑒𝑙 ({−}, {𝑎 − 𝑎}). These can be com-
bined in complex paths, e.g., 𝑏 +𝑐 ≡ 𝑐 +𝑏 + (𝑎 −𝑎) : {𝑏 +𝑐} =
                                                                              4   Samples Generation
𝐶𝑜𝑚𝑚𝑢𝑡𝑒 ({+}, 𝑁𝑜𝑜𝑝 ({+}, 𝐶𝑎𝑛𝑐𝑒𝑙 ({−}, {𝑐 + 𝑏 + (𝑎 − 𝑎)}))).                   The careful creation of our training dataset is key: as we let
Such axioms are developed for scalars, matrices and vectors,                  the DNN learn by example only what the axioms are and
and include complex rewrites such as distributivity rules and                 when they are applicable in the structure of a program, we
transpositions. A total of 102 axioms are used in our system.                 must carefully sample the space of equivalences to ensure
                                                                              appropriate distributions of the examples. We produce a final
3.3   Space of Equivalences                                                   dataset of tuples (𝑃1, 𝑃2, 𝑆), a pair of input programs and a
We now define the search space being explored in this work,                   possible rewrite rule sequence that proves the pair equiva-
i.e., the exact space of solutions on which the DNN system                    lent. Duplicates are removed such that all samples have a
formally operates, and that we sample for training.                           unique 𝑃1. From this dataset, we create 1,000,000 training
                                                                              samples, 10,000 validation samples, and 10,000 test samples.
Definition 3.9 (Graph of the space of equivalences). Given
                                                                              We outline below its generation principles; extensive details
a language L. The directed graph of equivalences between
                                                                              and the algorithms used are presented in section B.1.
expressions is 𝐺 𝑒𝑞𝑢𝑖𝑣 = ⟨𝑁 𝑒𝑞𝑢𝑖𝑣 , 𝐸𝑒𝑞𝑢𝑖𝑣 ⟩ such that ∀𝑙 ∈ L, 𝑛𝑙 ∈
𝑁 𝑒𝑞𝑢𝑖𝑣 , and 𝑒𝑛𝐴𝑖𝑖,𝑛,𝑥𝑗 : 𝑛𝑖 → 𝑛 𝑗 ∈ 𝐸𝑒𝑞𝑢𝑖𝑣 iff 𝑛 𝑗 ≡ 𝐴𝑖 (𝑥, 𝑛𝑖 ), ∀𝐴𝑖       Random sample generation Deep learning typically re-
in the axiom system and 𝑥 a position in 𝑛𝑖 where 𝐴𝑖 is appli-                 quires large training sets to be effectively deployed, hence
cable.                                                                        we developed a process to automate sample generation. We
   In other words, the graph has one node per possible expres-                specifically use randomized program generation algorithms
sion in the language L, and a single axiom application leads                  that are inspired by a given language grammar. By randomly
to connecting two nodes. We immediately note that 𝐺 𝑒𝑞𝑢𝑖𝑣                     choosing between production rulse, one can build random
is a (possibly infinite) multigraph, and contains circuits.                   parse trees by simply iterating the grammar. The leaves ob-
Theorem 3.10 (Expression equivalence with pathfinding).                       tained will form a sentence accepted by the language, i.e.,
Given two expressions 𝑛𝑖 , 𝑛 𝑗 ∈ 𝑁 𝑒𝑞𝑢𝑖𝑣 . If there is any path from          a program [15]. We limit to programs of 50 nodes in the
𝑛𝑖 to 𝑛 𝑗 in 𝐺 𝑒𝑞𝑢𝑖𝑣 , then 𝑛𝑖 ≡ 𝑛 𝑗 .                                        program tree (or AST), with a maximal tree depth of 7. We
                                                                          5
pe-graph2axiom, June, 2021, ArXiV                                      Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

assert that our random production rule procedure has a non-            They are not "iterative": a single inference is expected to
zero probability of producing any program allowed by the               produce the complete proof; in contrast to AxiomStep10 for
grammar for our datasets.                                              which a single axiom of the sequence is produced at each
  We produce equivalent program samples by pseudo-randomly             inference step. Training long output sequences can benefit
applying axioms on one randomly generated program to                   from complex training approaches such as Professor forcing
produce a rewrite sequence and the associated equivalent               [37], but we will show that our AxiomStep10 model general-
program. Given a randomly selected node in the program                 izes well with our sequence model training approach.
graph, our process checks which axiom(s) can be applied.
E.g., the +𝑚 operator may have the Commute axiom cate-                     Table 2. Datasets used for studies in experiments.
gory applied, or it may have the Transpose axiom category              Dataset         AST depth   AST #nodes    Proof length   Iterative
applied, which affects the operator’s children.
                                                                       AxiomStep10        2-7          2-50          1-10       Yes
Final experimental dataset: AxiomStep10 To train our                   AxiomStep5         2-6          2-25           1-5       Yes
network to produce one axiom step at a time, as described              WholeProof10       2-7          2-50          1-10       No
in Sec. 2, AxiomStep10 has a single axiom in each output se-           WholeProof5        2-6          2-25           1-5       No
quence 𝑆. For a complete proof 𝑆 : 𝐴1 (𝐴2 (...) in a (𝑃1, 𝑃2, 𝑆)
we generated made of N axioms, we then create N training
examples for the network: (𝑃1, 𝑃2, 𝐴𝑁 ) the first intermediate         Complexity of equivalence space Figure 3 provides a view
step by applying the first axiom, then (𝐴𝑁 (𝑃1), 𝑃2, 𝐴𝑁 −1 ),          of the complexity of the equivalence problem we tackle. The
etc. We limit proof length to 10 axioms in our experiments             distribution of the dataset per proof length is displayed in
(hence AxiomStep10). Test samples only have the original               the right chart; the left chart shows by size of bubble the
and target program and the network proposes axioms which               number of test samples with a given number of semantics-
create intermediate programs towards the proof, fed back to            preserving axioms that may be implemented as the first step
the system.                                                            of the proof and the proof length needed.

Table 1. Distribution for the 14 axiom categories in Axiom-
Step10 test set. Considering scalars (a, b, ...), vectors (®  ®
                                                           𝑣 ,𝑤,
...) and matrices (A, B, ...) types combinations, 147 distinct
axioms are represented.
      Axiom Category Example axiom(s)       Samples with
      Cancel           (A-A)→O,(b/b)→1             13.8%
      NeutralOp        (®   ® → 𝑣®
                        𝑣 - 𝑜)                     40.0%
                          𝑡
      DoubleOp         𝐴𝑡 → 𝐴, 1/1/x→x              7.3%
      AbsorbOp         (A*O)→O, (b*0)→0            30.3%
      Commute          (a + b) → (b + a)           48.6%
      DistributeLeft   (a + b)c → ac + bc          36.3%
      DistributeRight a(b + c) → ab + ac           27.8%
      FactorLeft       ab + ac → a(b+c)             6.1%
      FactorRight      ac + bc → (a+b)c             9.0%
      AssociativeLeft a(bc) → (ab)c                46.3%
      AssociativeRight (ab)c → a(bc)               43.1%
      FlipLeft         -(®   ® → 𝑤® − 𝑣®
                         𝑣 - 𝑤)                     8.4%
      FlipRight        a/(b/c) → a(c/b)            26.1%               Figure 3. Distribution of axiom possibilities and proof com-
      Transpose        (𝐴𝐵)𝑡 → 𝐵𝑡 𝐴𝑡 ,             11.1%               plexity for test datasets.
                                                                          There is a large number of proofs possible in our system,
Datasets to study generalizability and robustness In                   as detailed in Appendix B.3. For example, for proofs of length
order to study our model’s ability to generalize, we have              5, about 340,000 proofs made only of legal applications of ax-
created alternate datasets on which to train and test models           ioms can be performed on the average sample in our dataset.
which are summarized in table 2. WholeProof10 will help us             Since many programs have multiple possible proofs, about
contrast learning approaches. This dataset has the complete            10,000 different programs can be produced, only one of which
proof sequence 𝑆 made of 𝑁 ≥ 1 axioms as reference output              is the target to prove, i.e., randomly drawing a valid 5 axiom
for a program pair, while for AxiomStep10, 𝑁 = 1. Models               proof on a program known to be 5 axiom steps from the
trained on WholeProofX must maintain internal state rep-               target has roughly a 1 in 10,000 chance of being a correct
resenting the graph transformations that the axioms create.            proof of equivalence between the two programs.
                                                                   6
Proving Equivalence Between Complex Expressions                                                                pe-graph2axiom, June, 2021, ArXiV

5     Deep Neural Networks for Program                                                  Because pe-graph2axiom has a robust output verifica-
      Equivalence                                                                       tion, we make use of beam search to track up to 10 likely
Fig. 2 overviews the entire system architecture including                               candidates for proofs of equivalence.
sample generation, the pe-graph2axiom network, and                                         By using the root node only for seeding the initial hid-
the rewrite checker. Key design decisions are presented be-                             den state ℎ𝑑0 of the decoder, the weights associated with its
low.                                                                                    connections to the program graphs for 𝑃1 and 𝑃2 learn to
                                                                                        represent the information necessary for the rewrite rule se-
Graph neural network The sample generation discussed                                    quence. In parallel, after the graph neural network iterations
in section 4 provides input to the Node Initialization module                           complete, the final embedding for all the nodes in the graphs
in Fig. 2 to create the initial state of our graph neural network                       for 𝑃1 and 𝑃2 are only used by the attention network, so
[13]. For each node in the program graph, a node will be                                their final embedding represents information useful during
initialized in our graph neural network with a value that                               rewrite rule generation.
encodes the AST level and language token of the program
node. To interconnect the edges we support 9 edge types and                             Intermediate program generation pe-graph2axiom
their reverse edges which allows information to move in any                             applies the axiom and program node chosen by the neural
direction necessary: 1) left child of binary op, 2) right child                         network token generator to the input program to create an
of binary op, 3) child of unary op, 4) root node to program                             intermediate program 𝑃 ′ on the path from 𝑃1 to 𝑃2. If this
1, 5) root node to program 2, 6-9) there are 4 edge types for                           program is equal to 𝑃2, then our axiom path is complete,
the node grandchildren (LL, LR, RL, RR). The node states                                otherwise the new pair 𝑃 ′, 𝑃2 is inferred to determine the
and edge adjacency matrix represent the initial graph neural                            next axiom step.
network state.
   After initialization, the graph neural network iterates 10                           Incremental versus non-incremental sequence produc-
times in order to convert the initial node state into the                               tion The models we train on the AxiomStep5, WholeProof10,
embeddings needed for rewrite rule generation. Given an                                 and WholeProof5 datasets have the same neural network
initial hidden state for node 𝑛 of 𝑥𝑛 (0), 𝑥𝑛 (𝑡 + 1) is com-                           hyperparemeters as the AxiomStep10 data model. However,
puted with a learnable function 𝑓 which combines the cur-                               the models for WholeProof10 and WholeProof5 are trained
rent hidden state 𝑥𝑛 (0), the edge types 𝑙𝑖𝑛 [𝑛] of edges en-                           to output the entire sequence of axioms needed to prove the
tering node 𝑛, the edge types 𝑙𝑜𝑢𝑡 [𝑛] of edges exiting node                            2 programs identical, hence these models do not make use
𝑛, and the hidden states 𝑥𝑛𝑒 [𝑛] of the neighbors of node 𝑛:                            of the intermediate program generation and instead have a
𝑥𝑛 (𝑡 + 1) = 𝑓 (𝑥𝑛 (𝑡), 𝑙𝑖𝑛 [𝑛] , 𝑥𝑛𝑒 [𝑛] (𝑡), 𝑙𝑜𝑢𝑡 [𝑛] ).                              component which checks whether the full sequence of ax-
   Each edge type has a different weight matrix for learning,                           ioms legally transforms 𝑃1 into 𝑃2. We encode the path to the
allowing aggregation of information into a given node re-                               AST node an which to apply an axiom using ’left’ and ’right’
lated to its function in the full graph of the program. The root                        tokens which specify the path from the current program
node’s initial state along with the edge types connecting it                            root node. This encoding is sufficient for the iterative model
to the program graph trees allow it to aggregate and transfer                           and necessary to allow the non-iterative model to identify
specific information regarding rewrite rules as demonstrated                            nodes which may not have been in the initial AST for 𝑃1.
by our experimental results. This is a novel feature of our                             The non-iterative models must learn a representation in the
network not used in prior work with GNNs on program                                     LSTM network to allow them to track AST transformations
analysis [4, 62].                                                                       as they are generated.

Graph neural network output to decoder After stepping
the GGNN, the final node values are used by the decoder in                              6   Experimental Results
two ways to create rewrite rules. First, the final root node                            We now present extensive experimental results, and compare
value 𝑥𝑟𝑜𝑜𝑡 (10) is fed through a learnable bridge function to                          the quality of several neural network approaches to address
initialize the LSTMs of the decoder. In this way, the aggre-                            the problem of program equivalence. We have proceeded
gated information of the 2 programs seeds the generation                                incrementally for fine-tuning the final system design, and
of rewrite rules. The LSTMs update as each output token 𝑦 𝑗                             report on several of these design points below.
is generated with a learnable function based on the current                                We focus our experiments below on 4 key questions: 1) Is
decoder hidden state ℎ𝑑𝑗 at decoder step 𝑗 and the previous                             performance related to input program size? 2) Is performance
output token 𝑦 𝑗−1 [18]. Second, all nodes in the graph can be                          related to proof length? 3) Is the incremental, per-axiom ap-
used by an attention layer [8]. The attention layer creates a                           proach more generalizable than producing the full sequence
context vector 𝑐 𝑗 which can be used by a learnable function                            in a single inference step? And 4) Is performance consis-
𝑔 when computing the probability for generating the 𝑗th out-                            tent across a range of datasets, including human-written
put token 𝑃 (𝑦 𝑗 ): 𝑃 (𝑦 𝑗 | 𝑦 𝑗−1, 𝑦 𝑗−2, ..., 𝑦0, 𝑐 𝑗 ) = 𝑔(ℎ𝑑𝑗 , 𝑦 𝑗−1, 𝑐 𝑗 ).       examples?
                                                                                    7
pe-graph2axiom, June, 2021, ArXiV                                      Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet
                                                                       Table 4. Performance vs. AST size: counts and percentage
Implementation setup We developed the neural network                   pass rates.
system presented in the OpenNMT-py system [34], adding
                                                                                         Testset       Model trained    Model trained
on a new encoder based on a prior implementation of gated                             Sample Count    on AxiomStep5    on AxiomStep10
graph neural networks [40]. For our training and evalua-                AST depth      AS5   AS10     AS5      AS10    AS5        AS10
tion experiments, we use systems with Intel Xeon 3.6GHz                       2-6    10000    6865     99        93     99          94
CPUs and 6GB GeForce GTX 1060 GPUs. During training,                            7        0    3135    n/a        86    n/a          92
                                                                              All    10000   10000     99        90     99          93
we save a model snapshot every 50,000 iterations and score
the accuracy the model achieved on the validation dataset.
Graphs showing that validation accuracy plateaus at 200,000            to the input program complexity is illustrated with the 86%
to 300,000 iterations are provided in section E. We run each           pass rate on AST depth 7, for the model trained on Axiom-
model twice and evaluate the test set using the saved model            Step5 which never saw programs of depth 7 during training.
which achieved the highest validation score.                              Table 5 compares the results of our 4 models, each trained
                                                                       on one of our 4 datasets, and evaluated with the test set of all
Evaluation procedure and neural network alternatives                   4 datasets. The models all have identical hypermeter settings.
The benefits of key components of our neural network model             We observe the inability of models trained to output the
are studied in table 3. The bidirectional RNN model is similar         whole proof to generalize to proofs of higher length (WP5
to state-of-the-art sequence-to-sequence models used for               model on AS10/WP10), with near zero success rate. However,
program repair [18]. The results for the graph-to-sequence             per-axiom models (AS5 and AS10) show potential for gen-
model without attention show the benefit of providing the              eralization to proof length: AS5 model performs well when
node information during the axiom generation process.                  evaluated on AS10, showing the ability to produce proofs of
     Table 3. pe-graph2axiom mini ablation study.                      length/complexity unseen in training. Overall, the success
                                                 Beam width            rate degrades gracefully with proof length, bottoming at 66%
Model description                               1   2   5 10           for AS10 for proofs of length 10.
Bidirectional RNN seq-to-seq with attention    48   62   71   75       6.1   WholeProof Models: Language Complexity and
Graph-to-sequence w/o attention                73   81   87   90             Performance
pe-graph2axiom model                           76   84   90   93
                                                                       Table 6 shows the result of 12 different experiments and
                                                                       designs specifically for the WholeProof5 models. In particu-
   Our final design was influenced by explorations we per-
                                                                       lar, we incrementally increase the problem complexity from
formed on varied models, datasets, and hyperparameters
                                                                       rows 1 to 10, increasing the number of Operators that can be
such as LSTM layers and graph neural network parameters.
                                                                       used in any input program, of Axioms used in the rewrite se-
In relation to the model’s ability to learn a representation of
                                                                       quence, of Operands in any input program, of the maximal
the proof sequence, we note that our GGNN initialization us-
                                                                       number of nodes in an input program graph (the Program
ing the root node connection to the decoder outperforms the
                                                                       length, directly influencing the size of the graph network),
embedding learned by a bidirectional RNN model. Also, we
                                                                       and the Rewrite rule length, which contains the description
found that averaging the embedding of all graph nodes had
                                                                       of paths from the root node to reach the position of appli-
about 10% lower accuracy than using the more specific root
                                                                       cation of an axiom, this is directly related to the maximal
node information. Numerous additional results are reported
                                                                       graph height, itself determined by the maximal program size.
in Suppl. material E.
                                                                       Details on each row are provided in Supplementary Material.
Generalizing across different datasets We specifically                    We specifically compare against a sequence-to-sequence
look at the generalization potential for our models by study-          (S2S) approach, to quantify the gains brought by employing
ing their success rate as a function of the input program              graph-to-sequence (G2S). When the space is small enough,
complexity, represented as the AST depth, in Table 4, and as           S2S still performs well, especially using aggressive beam
a function of the output complexity, represented by the proof          search. We recall that by design of our system testing the
length in Table 5, all using a beam size of 10. We designed            correctness of one sequence is trivial and deterministic, so
our datasets in Sec. 4 to study how well pe-graph2axiom                one can easily use large beam sizes without any correctness
generalizes and to assess we are not overfitting on training           impact nor major performance penalty during inference. For
data. Extensive in-depth additional experimental results are           example, inference of beam 1 is about 15ms for our most
presented in Suppl. Material E, we summarize key results               complex networks, but beam 10 only takes 16ms. Checking
only below.                                                            correctness is << 1ms.
   Table 4 illustrates the ability of a model trained on Ax-              Contrasting rows 2 and 3 displays the merits of the G2S
iomStep5 (i.e., limited to proofs of length 5) to perform well         approach for our problem: on this simple problem, in fact G2S
when evaluated on the more complex AxiomStep10, which                  gets near-perfect accuracy already. Progressively increasing
includes proofs of unseen length of up to 10. The robustness           the complexity of the search space, till row 9 and 10, displays
                                                                   8
Proving Equivalence Between Complex Expressions                                                                                                                                  pe-graph2axiom, June, 2021, ArXiV
                                       Table 5. Performance vs. proof length: percentage pass rates.
                         Axiom         Model trained on         Model trained on                                          Model trained on                                        Model trained on
                        Count in      WholeProof5 (WP5)        WholeProof10 (WP10)                                        AxiomStep5 (AS5)                                       AxiomStep10 (AS10)
                            Proof   WP5 WP10 AS5 AS10         WP5 WP10 AS5 AS10                              WP5 WP10 AS5 AS10                                                  WP5 WP10 AS5 AS10
                              1-5     95     89    44    44     94       93             44          44                99                 97    99                          98    99                  98              99       98
                                6            14           4              72                          5                                   81                                88                        90                       93
                                7             0           1              63                          2                                   67                                81                        83                       87
                                8             0           0              54                          1                                   54                                75                        73                       82
                                9             0           0              47                          0                                   35                                64                        63                       74
                               10             0           0              34                          0                                   24                                57                        46                       66
                              All     95     66    44    27     94       84             44          27                99                 87    99                          90    99                  93              99       93




                                                                                                                                                    Rewrite rules length




                                                                                                                                                                                                                                                       with beam width 10
                                                                                                                                                                                                                                   with beam width 1
                                                                                                                                                                                                                                   Percent matching



                                                                                                                                                                                                                                                       Percent matching
                                                                                                                                                                                  Graph2seq (G2S)



                                                                                                                                                                                                          Training set size
                                                                                                                                                                                  or seq2seq (S2S)
                                                                                                                              Program length
                                                                          # Operators




                                                                                                             # Operands
                                                                                             # Axioms
      ID    Description
      1     Rewrite sequence is only single Commute, uses sequence-to-    2                  1               10               3-19                  1-5                           S2S                     80,000                   90.0%               96.2%
            sequence model
      2     Rewrite sequence is exactly 2 Commutes, uses sequence-to-     2                  1               10               5-24                  3-10                          S2S                     80,000                   80.3%               96.5%
            sequence model
      3     Rewrite sequence exactly 2 Commutes                           2                  1               10               5-24                  3-10                          G2S                     80,000                   98.9%               99.8%
      4     Rewrite sequence exactly 3 Commutes                           2                  1               10               7-45                  5-15                          G2S                     80,000                   91.4%               99.0%
      5     Rewrite sequence 1 to 3 Commutes                              2                  1               10               3-45                  1-15                          G2S                     180,000                  97.1%               99.2%
      7     Commute, Noop, Cancel, Distribute Left, Distribute Right      4                  5               12               3-45                  1-15                          G2S                     180,000                  93.1%               97.4%
      8     Scalars, Vectors, and Matrixes                                16                 5               20               3-30                  1-25                          G2S                     250,000                  88.3%               95.6%
      9     13 Axioms                                                     16                 13              20               3-30                  1-25                          G2S                     400,000                  85.5%               95.5%
      10    Rewrite sequence or Not_equal                                 16                 13              20               3-30                  1-25                          G2S                     500,000                  79.8%               93.8%
      11    Test sequence-to-sequence                                     16                 13              20               3-30                  1-25                          S2S                     400,000                  59.8%               81.1%
      12    Add loop axioms                                               18                 15              20               3-30                  1-25                          G2S                     400,000                  83.8%               94.7%
           Table 6. Results for various language complexities studied, on non-incremental models (WholeProof).
a slow but steady decrease in quality, while still maintaining                                          provide small but human-written datasets. We solve all of
excellent scores near or above 95% with beam 10. To reassess                                            the matrix expression equivalence programs from 2 relevant
the limits of a sequence-to-sequence approach, row 9 and 11                                             Khan academy modules designed to test student’s knowl-
can be constrasted: they operate on the same search space,                                              edge of matrix algebra [33]. Our AxiomStep10 model is able
but S2S peaks at 81% accuracy, while G2S reaches 95%.                                                   to correctly prove all 15 equivalent pairs from the modules
   Row 10 displays the result when learning using also sam-                                             with beam width 1 and wider. With a beam width of 10, the
ples of non-equivalent programs, using the “empty path”                                                 WholeProof10 model proved 12. An example problem solv-
symbol Not_equal. We evaluated this system to measure                                                   able by AxiomStep10 but not WholeProof10 is: 𝑐 (1𝐴 + 𝐵) =
the impact of training on only equivalent programs vs. also                                             𝑐𝐵 + 𝑐𝐴 which can be proven by applying the rewrite rules
sampling pairs of unconnected nodes in the equivalences                                                 NeutralOp, DistributeRight, and Commute to the proper
graph. We recall that by design, if no rewrite rule produced                                            nodes. The WholeProof10 model mostly fails because it was
is verified as correct, our system outputs the programs are                                             not trained on how to apply repeated transformations at
not equivalent. In other words, whichever the sequence(s)                                               the same point in the AST. This suggests AxiomStep10 has
produced by the network, if the two input programs are                                                  generalized well to these hand-written problems.
non-equivalent, the system will always output they are not
equivalent: no equivalence sequence produced can be veri-
fied as correct. So training on only equivalent programs is                                              7                Related Work
clearly sensible for such system; furthermore as shown in                                                Theorem provers The problem of equivalence as we for-
row 10 vs. 9, even increasing the training set size, training us-                                        mulated may be solved by other (smart) brute-force ap-
ing non-equivalent programs seem to lower the performance                                                proaches, where a problem is solved by pathfinding. This
slightly.                                                                                                ranges from theoreom proving systems like Coq [14] which
                                                                                                         supports the formal framework for equivalence we describe
Human written test expressions from Khan academy
                                                                                                         in this paper, to (Approximate Probabilistic) Model Check-
exercises Unfortunately there is a dearth of existing large
                                                                                                         ing [17, 20, 27], where a program equivalence system can
reference datasets for equivalence of linear algebra expres-
                                                                                                         also be built, e.g. [19, 46, 52, 58]. Our contribution is not in
sions, which justified our careful dataset creation approach
                                                                                                         the formal definition of program equivalence we presented,
in Sec. 4 and their upcoming public release. However nu-
                                                                                                         semantics-preserving rewrite systems have been studied,
merous math exercises involve exactly this problem, and can
                                                                                             9
pe-graph2axiom, June, 2021, ArXiV                                       Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

e.g. [41, 50, 57]. But understanding why this particular for-           network weights are processed to create a verifiable deter-
malism was well suited to deep learning graph-to-sequence               ministic finite automata (DFA) representation of the learned
systems was key. The merits of stochastic search to accel-              grammar. This work demonstrates that deterministic gram-
erate such systems has been demonstrated, e.g. [24, 27, 45].            mars can be learned with RNNs, which we rely on.
The novelty of our approach is to develop carefully crafted
graph-to-sequence neural networks to automatically learn                Graph Neural Networks Graph neural networks [51, 61]
an efficient pathfinding heuristic for this problem. Our ap-            use machine learning to analyze a set of nodes and edges
proach is potentially applicable in these areas too, however            for patterns related to a target problem. Using a graph-to-
training scalability can become a challenge if increasing the           sequence network with attention has been analyzed for nat-
input representation size excessively. Theorem provers us-              ural language processing [13]. Allamanis et al. use graph
ing deep learning have recently started to be investigated,             neural networks to analyze code sequences and add edge
Aygun et al. [7] developed a graph neural network system                types representing LastUse, ComputedFrom, and LastWrite
for automatic proof generation. Wu et al. [60] explores the             to improve the system’s ability to reason about the code
ability of theorem provers using GNNs, TreeLSTMs, and                   [4]. Their work achieves 84% accuracy on correcting vari-
BagOfWords architectures to generalize and solve proofs                 able misuse cases and provides insights to useful edge types.
with lengths up to 7 axioms and found that GNNs performed               Structure2vec [62] uses a graph neural network to detect
the best of the architectures studied when more complex                 binary code similarity. Structure2vec uses a graph neural net-
proofs were required. While our model works in a slightly               work to learn an embedding from a annotated control flow
different problem space, we study the ability of our mod-               graph (ACFG) of a program. This learning process targets the
els to generalize on proofs with lengths up to 10, with 14              embedding so that equivalent programs will have equivalent
different rewrite rules acting on 147 distinct axioms. These            embeddings, reporting precision scores of 84% and 85% on
frameworks could also be used to prove equivalence between              various test datasets for correctly predicting program equiv-
symbolic expressions, as theorem provers.                               alence. It only outputs a probability of equivalence, and not
                                                                        a verifiable proof, which is sufficient in their context.
Static program equivalence Algorithms for static pro-                      The G2SKGE model [39] has a similar graph network struc-
gram equivalence have been developed, e.g. [2, 11, 29, 56].             ture which uses a node embedding (which they refer to as
These approaches typically restrict to demonstrating the                an information fusion mechanism) in order to predict rela-
equivalence of different schedules of the operations, possibly          tionships between nodes. This technique of using a neural
dynamically [10]. In this work we target graph-modifying                network to understand and predict node interelationships is
rewrites (and therefore which alter the operation count).               common to our approach.
Barthou et al. [2, 11] have developed techniques to recog-
nize algorithm templates in programs. These approaches                  8    Conclusion
are restricted to static/affine transformed programs. Karfa et          In this work, we presented pe-graph2axiom, the first
al. also designed a method that works for a subset of affine            graph-to-sequence neural network system to generate verifi-
programs using array data dependence graphs (ADDGs) to                  able axiomatic proofs (via rewrite rules) for equivalence for
represent input and transforming behaviors. Operator-level              a class of symbolic programs. Evaluated on a rich language
equivalence checking provides the capability to normalize               for linear algebra expressions, this system produces correct
expressions and establish matching relations under algebraic            proofs of up to 10 axioms in length in 93% of the 10,000 equiv-
transformations [32]. Mansky and Gunter used the TRANS                  alent cases evaluated. We believe the performance of our
language [30] to represent transformations. The correctness             approach comes in part from using graph neural networks
proof implemented in the verification framework [43] is ver-            for what they aim to excel at: learning efficient heuristics
ified by the Isabelle [48] proof assistant. Other works also            to quickly find paths in a graph; and the observation that
include translation validation [35, 47].                                program equivalence can be cast as a path-based solution
                                                                        that is efficiently found by such networks.
Program analysis with machine learning Numerous
prior work has employed (deep) machine learning for pro-                Acknowledgments
gram analysis, e.g. [3, 5, 12, 36, 49, 54]. code2vec [5] teaches
                                                                        This work was supported in part by the U.S. National Science
a method for creating a useful embedding vector that sum-
                                                                        Foundation award CCF-1750399.
marizes the semantic meaning of a snippet of code. Program
repair approaches, e.g. [18, 54] are deployed to automatically
repair bugs in a program. Output accuracies of up to 20%
                                                                        References
                                                                         [1] Umair Z Ahmed, Pawan Kumar, Amey Karkare, Purushottam Kar,
on the test set is reported, using sequence-to-sequence mod-
                                                                             and Sumit Gulwani. 2018. Compilation error repair: for the student
els. Wang et al. [59] learns to extract the rules for Tomita                 programs, from the student programs. In Proceedings of the 40th In-
grammars [53] with recurrent neural networks. The learned                    ternational Conference on Software Engineering: Software Engineering
                                                                   10
Proving Equivalence Between Complex Expressions                                                                   pe-graph2axiom, June, 2021, ArXiV

     Education and Training. ACM, 78–87.                                              [16] Joseph Tobin Buck and Edward A Lee. 1993. Scheduling dynamic
 [2] Christophe Alias and Denis Barthou. 2004. On the recognition of                       dataflow graphs with bounded memory using the token flow model.
     algorithm templates. Electronic Notes in Theoretical Computer Science                 In 1993 IEEE international conference on acoustics, speech, and signal
     82, 2 (2004), 395–409.                                                                processing, Vol. 1. IEEE, 429–432.
 [3] Miltiadis Allamanis, Earl T. Barr, Premkumar Devanbu, and Charles                [17] Jerry R Burch, Edmund M Clarke, Kenneth L McMillan, David L Dill,
     Sutton. 2018. A Survey of Machine Learning for Big Code and Nat-                      and Lain-Jinn Hwang. 1992. Symbolic model checking: 1020 states
     uralness. ACM Comput. Surv. 51, 4, Article 81 (July 2018), 37 pages.                  and beyond. Information and computation 98, 2 (1992), 142–170.
     https://doi.org/10.1145/3212695                                                  [18] Zimin Chen, Steve Kommrusch, Michele Tufano, Louis-Noël Pouchet,
 [4] Miltiadis Allamanis, Marc Brockschmidt, and Mahmoud Khademi.                          Denys Poshyvanyk, and Martin Monperrus. 2019. SequenceR:
     2018. Learning to Represent Programs with Graphs. In 6th Inter-                       Sequence-to-Sequence Learning for End-to-End Program Repair. IEEE
     national Conference on Learning Representations, ICLR 2018, Vancou-                   Transactions on Software Engineering (2019). https://doi.org/10.1109/
     ver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings.                TSE.2019.2940179
     https://openreview.net/forum?id=BJOFETxR-                                        [19] Edmund Clarke, Daniel Kroening, and Karen Yorav. 2003. Behavioral
 [5] Uri Alon, Meital Zilberstein, Omer Levy, and Eran Yahav. 2019.                        consistency of C and Verilog programs using bounded model check-
     Code2Vec: Learning Distributed Representations of Code. Proc. ACM                     ing. In Proceedings 2003. Design Automation Conference (IEEE Cat. No.
     Program. Lang. 3, POPL, Article 40 (Jan. 2019), 29 pages. https:                      03CH37451). IEEE, 368–371.
     //doi.org/10.1145/3290353                                                        [20] Edmund M Clarke, Orna Grumberg, and David E Long. 1994. Model
 [6] Marcin Andrychowicz, Filip Wolski, Alex Ray, Jonas Schneider, Rachel                  checking and abstraction. ACM transactions on Programming Lan-
     Fong, Peter Welinder, Bob McGrew, Josh Tobin, OpenAI Pieter Abbeel,                   guages and Systems (TOPLAS) 16, 5 (1994), 1512–1542.
     and Wojciech Zaremba. 2017. Hindsight Experience Replay. In Ad-                  [21] Nachum Dershowitz. 1985. Computing with rewrite systems. Infor-
     vances in Neural Information Processing Systems 30, I. Guyon, U. V.                   mation and Control 65, 2-3 (1985), 122–157.
     Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Gar-          [22] Alhussein Fawzi, Mateusz Malinowski, Hamza Fawzi, and Omar Fawzi.
     nett (Eds.). Curran Associates, Inc., 5048–5058. http://papers.nips.cc/               2019. Learning dynamic polynomial proofs. In Advances in Neu-
     paper/7090-hindsight-experience-replay.pdf                                            ral Information Processing Systems 32, H. Wallach, H. Larochelle,
 [7] Eser Aygün, Zafarali Ahmed, Ankit Anand, Vlad Firoiu, Xavier                          A. Beygelzimer, F. d’Alché Buc, E. Fox, and R. Garnett (Eds.).
     Glorot, Laurent Orseau, Doina Precup, and Shibl Mourad. 2020.                         Curran Associates, Inc., 4179–4188. http://papers.nips.cc/paper/
     Learning to Prove from Synthetic Theorems.               arXiv e-prints,              8671-learning-dynamic-polynomial-proofs.pdf
     Article arXiv:2006.11259 (June 2020), arXiv:2006.11259 pages.                    [23] Benny Godlin and Ofer Strichman. 2008. Inference rules for proving
     arXiv:2006.11259 [cs.LO]                                                              the equivalence of recursive procedures. Acta Informatica 45, 6 (2008),
 [8] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2014. Neural                      403–439.
     machine translation by jointly learning to align and translate. arXiv            [24] Vibhav Gogate and Pedro Domingos. 2012. Probabilistic theorem
     preprint arXiv:1409.0473 (2014).                                                      proving. arXiv preprint arXiv:1202.3724 (2012).
 [9] Kshitij Bansal, Sarah Loos, Markus Rabe, Christian Szegedy, and Stew-            [25] Robert Goldblatt and Marcel Jackson. 2012. Well-structured program
     art Wilcox. 2019. HOList: An Environment for Machine Learning                         equivalence is highly undecidable. ACM Transactions on Computational
     of Higher Order Logic Theorem Proving. In Proceedings of the 36th                     Logic (TOCL) 13, 3 (2012), 26.
     International Conference on Machine Learning (Proceedings of Ma-                 [26] Ian J. Goodfellow, Yoshua Bengio, and Aaron Courville. 2016. Deep
     chine Learning Research, Vol. 97), Kamalika Chaudhuri and Ruslan                      Learning.     MIT Press, Cambridge, MA, USA.               http://www.
     Salakhutdinov (Eds.). PMLR, Long Beach, California, USA, 454–463.                     deeplearningbook.org.
     http://proceedings.mlr.press/v97/bansal19a.html                                  [27] Thomas Hérault, Richard Lassaigne, Frédéric Magniette, and Sylvain
[10] Wenlei Bao, Sriram Krishnamoorthy, Louis-Noël Pouchet, Fabrice                        Peyronnet. 2004. Approximate probabilistic model checking. In In-
     Rastello, and Ponnuswamy Sadayappan. 2016. Polycheck: Dynamic                         ternational Workshop on Verification, Model Checking, and Abstract
     verification of iteration space transformations on affine programs. In                Interpretation. Springer, 73–84.
     ACM SIGPLAN Notices, Vol. 51. ACM, 539–554.                                      [28] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term
[11] Denis Barthou, Paul Feautrier, and Xavier Redon. 2002. On the equiva-                 memory. Neural computation 9, 8 (1997), 1735–1780.
     lence of two systems of affine recurrence equations. In Euro-Par 2002            [29] Guillaume Iooss, Christophe Alias, and Sanjay Rajopadhye. 2014. On
     Parallel Processing.                                                                  program equivalence with reductions. In International Static Analysis
[12] Rohan Bavishi, Michael Pradel, and Koushik Sen. 2017. Context2Name:                   Symposium. Springer, 168–183.
     A Deep Learning-Based Approach to Infer Natural Variable Names                   [30] Sara Kalvala, Richard Warburton, and David Lacey. 2009. Program
     from Usage Contexts. http://tubiblio.ulb.tu-darmstadt.de/101419/                      transformations using temporal logic side conditions. ACM Trans. on
[13] Daniel Beck, Gholamreza Haffari, and Trevor Cohn. 2018. Graph-to-                     Programming Languages and Systems (TOPLAS) 31, 4 (2009), 14.
     Sequence Learning using Gated Graph Neural Networks. In Proceedings              [31] Donald M Kaplan. 1969. Regular expressions and the equivalence of
     of the 56th Annual Meeting of the Association for Computational Lin-                  programs. J. Comput. System Sci. 3, 4 (1969), 361–386.
     guistics (Volume 1: Long Papers) (Melbourne, Australia). Association             [32] Chandan Karfa, Kunal Banerjee, Dipankar Sarkar, and Chittaranjan
     for Computational Linguistics, 273–283. http://aclweb.org/anthology/                  Mandal. 2013. Verification of loop and arithmetic transformations of
     P18-1026                                                                              array-intensive behaviors. IEEE Trans. on Computer-Aided Design of
[14] Yves Bertot and Pierre Castéran. 2013. Interactive theorem proving and                Integrated Circuits and Systems 32, 11 (2013), 1787–1800.
     program development: Coq’Art: the calculus of inductive constructions.           [33] Sal Khan. 2020.        Properties of matrix multiplication.       Khan
     Springer Science & Business Media.                                                    Academy (accessed May 20, 2020) (May 2020).                       https:
[15] Pavol Bielik, Veselin Raychev, and Martin Vechev. 2016. PHOG: Proba-                  //www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:
     bilistic Model for Code. In Proceedings of The 33rd International Confer-             matrices/x9e81a4f98389efdf:properties-of-matrix-multiplication/a/
     ence on Machine Learning (Proceedings of Machine Learning Research,                   properties-of-matrix-multiplication
     Vol. 48), Maria Florina Balcan and Kilian Q. Weinberger (Eds.). PMLR,            [34] Guillaume Klein, Yoon Kim, Yuntian Deng, Jean Senellart, and Alexan-
     New York, New York, USA, 2933–2942. http://proceedings.mlr.press/                     der M. Rush. 2017. OpenNMT: Open-Source Toolkit for Neural
     v48/bielik16.pdf                                                                      Machine Translation. In Proc. ACL. https://doi.org/10.18653/v1/
                                                                                           P17-4012
                                                                                 11
pe-graph2axiom, June, 2021, ArXiV                                              Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

[35] Sudipta Kundu, Zachary Tatlock, and Sorin Lerner. 2009. Proving         [49] Veselin Raychev, Martin Vechev, and Andreas Krause. 2015. Predicting
     optimizations correct using parameterized program equivalence. ACM           Program Properties from "Big Code". In Proceedings of the 42Nd Annual
     SIGPLAN Notices 44, 6 (2009), 327–337.                                       ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
[36] Jeremy Lacomis, Pengcheng Yin, Edward J. Schwartz, Miltiadis Alla-           guages (Mumbai, India) (POPL ’15). ACM, New York, NY, USA, 111–124.
     manis, Claire Le Goues, Graham Neubig, and Bogdan Vasilescu. 2019.           https://doi.org/10.1145/2676726.2677009
     DIRE: A Neural Approach to Decompiled Identifier Naming. In Inter-      [50] Uday S Reddy. 1989. Rewriting techniques for program synthesis.
     national Conference on Automated Software Engineering (ASE ’19).             In International Conference on Rewriting Techniques and Applications.
[37] Alex M Lamb, Anirudh Goyal ALIAS PARTH GOYAL, Ying Zhang,                    Springer, 388–403.
     Saizheng Zhang, Aaron C Courville, and Yoshua Bengio. 2016.             [51] Franco Scarselli, Marco Gori, Ah Chung Tsoi, Markus Hagenbuchner,
     Professor Forcing: A New Algorithm for Training Recurrent Networks.          and Gabriele Monfardini. 2009. The Graph Neural Network Model.
     In Advances in Neural Information Processing Systems 29, D. D.               IEEE Transactions on Neural Networks 20 (2009), 61–80.
     Lee, M. Sugiyama, U. V. Luxburg, I. Guyon, and R. Garnett (Eds.).       [52] Bernhard Steffen. 1991. Data flow analysis as model checking. In
     Curran Associates, Inc., 4601–4609. http://papers.nips.cc/paper/             International Symposium on Theoretical Aspects of Computer Software.
     6099-professor-forcing-a-new-algorithm-for-training-recurrent-networks.      Springer, 346–364.
     pdf                                                                     [53] M. Tomita. 1982. Dynamic Construction of Finite Automata from
[38] Guillaume Lample and François Charton. 2020. Deep Learning For               examples using Hill-climbing. In Proceedings of the Fourth Annual
     Symbolic Mathematics. In International Conference on Learning Repre-         Conference of the Cognitive Science Society. Ann Arbor, Michigan, 105–
     sentations. https://openreview.net/forum?id=S1eZYeHFDS                       108.
[39] W. Li, X. Zhang, Y. Wang, Z. Yan, and R. Peng. 2019. Graph2Seq:         [54] Michele Tufano, Cody Watson, Gabriele Bavota, Massimiliano Di Penta,
     Fusion Embedding Learning for Knowledge Graph Completion. IEEE               Martin White, and Denys Poshyvanyk. 2019. An Empirical Study on
     Access 7 (2019), 157960–157971. https://doi.org/10.1109/ACCESS.              Learning Bug-Fixing Patches in the Wild via Neural Machine Transla-
     2019.2950230                                                                 tion. ACM Trans. Softw. Eng. Methodol. 28, 4, Article 19 (Sept. 2019),
[40] Yujia Li, Richard Zemel, Marc Brockschmidt, and Daniel Tarlow.               29 pages. https://doi.org/10.1145/3340544
     2016. Gated Graph Sequence Neural Networks. In Proceedings of           [55] Sven Verdoolaege, Gerda Janssens, and Maurice Bruynooghe. 2009.
     ICLR’16 (proceedings of iclr’16 ed.). https://www.microsoft.com/en-us/       Equivalence checking of static affine programs using widening to
     research/publication/gated-graph-sequence-neural-networks/                   handle recurrences. In Computer aided verification. Springer, 599–613.
[41] Dorel Lucanu and Vlad Rusu. 2015. Program equivalence by circular       [56] Sven Verdoolaege, Gerda Janssens, and Maurice Bruynooghe. 2012.
     reasoning. Formal Aspects of Computing 27, 4 (2015), 701–726.                Equivalence checking of static affine programs using widening to han-
[42] Thang Luong, Hieu Pham, and Christopher D. Manning. 2015. Ef-                dle recurrences. ACM Trans. on Programming Languages and Systems
     fective Approaches to Attention-based Neural Machine Translation.            (TOPLAS) 34, 3 (2012), 11.
     In Proceedings of the 2015 Conference on Empirical Methods in Natu-     [57] Eelco Visser. 2004. Program transformation with Stratego/XT. In
     ral Language Processing. Association for Computational Linguistics,          Domain-specific program generation. Springer, 216–238.
     Lisbon, Portugal, 1412–1421. https://doi.org/10.18653/v1/D15-1166       [58] Willem Visser, Klaus Havelund, Guillaume Brat, SeungJoon Park, and
[43] William Mansky and Elsa Gunter. 2010. A framework for formal                 Flavio Lerda. 2003. Model checking programs. Automated software
     verification of compiler optimizations. In Interactive Theorem Proving.      engineering 10, 2 (2003), 203–232.
     Springer.                                                               [59] Qinglong Wang, Kaixuan Zhang, Alexander G. Ororbia, II, Xinyu Xing,
[44] Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and                 Xue Liu, and C. Lee Giles. 2018. An Empirical Evaluation of Rule
     Jeff Dean. 2013.       Distributed Representations of Words and              Extraction from Recurrent Neural Networks. Neural Comput. 30, 9
     Phrases and their Compositionality.            In Advances in Neural         (Sept. 2018), 2568–2591. https://doi.org/10.1162/neco_a_01111
     Information Processing Systems 26, C. J. C. Burges, L. Bottou,          [60] Yuhuai Wu, Albert Jiang, Jimmy Ba, and Roger Grosse. 2020. INT:
     M. Welling, Z. Ghahramani, and K. Q. Weinberger (Eds.). Cur-                 An Inequality Benchmark for Evaluating Generalization in Theo-
     ran Associates, Inc., 3111–3119.           http://papers.nips.cc/paper/      rem Proving. arXiv e-prints, Article arXiv:2007.02924 (July 2020),
                                                                                  arXiv:2007.02924 pages. arXiv:2007.02924 [cs.AI]
     5021-distributed-representations-of-words-and-phrases-and-their-compositionality.
     pdf                                                                     [61] Zonghan Wu, Shirui Pan, Fengwen Chen, Guodong Long, Chengqi
[45] Andrzej S Murawski and Joël Ouaknine. 2005. On probabilistic pro-            Zhang, and Philip S. Yu. 2019. A Comprehensive Survey on Graph
     gram equivalence and refinement. In International Conference on Con-         Neural Networks. CoRR abs/1901.00596 (2019). arXiv:1901.00596
     currency Theory. Springer, 156–170.                                          http://arxiv.org/abs/1901.00596
[46] Kedar S Namjoshi and Robert P Kurshan. 2000. Syntactic program          [62] Xiaojun Xu, Chang Liu, Qian Feng, Heng Yin, Le Song, and Dawn Song.
     transformations for automatic abstraction. In International Conference       2017. Neural Network-based Graph Embedding for Cross-Platform
     on Computer Aided Verification. Springer, 435–449.                           Binary Code Similarity Detection. In Proceedings of the 2017 ACM
[47] George C Necula. 2000. Translation validation for an optimizing              SIGSAC Conference on Computer and Communications Security (Dallas,
     compiler. ACM SIGPLAN Notices 35, 5 (2000), 83–94.                           Texas, USA) (CCS ’17). ACM, New York, NY, USA, 363–376. https:
[48] Lawrence C. Paulson. [n.d.]. Isabelle Page. https://www.cl.cam.ac.uk/        //doi.org/10.1145/3133956.3134018
     research/hvg/Isabelle.




                                                                          12
Proving Equivalence Between Complex Expressions                                            pe-graph2axiom, June, 2021, ArXiV

A    Appendix                                                       • Matrix operations: +m -m *m im nm tm, where im is
               Supplementary Materials:                             matrix inversion, nm negates the matrix, and tm is matrix
         Learning Axioms to Compute Verifiable                      transpose.
                                                                    • Vector operations: +v -v *s nv, where nv is the unary
         Symbolic Expression Equivalence Proofs
                                                                    negation.
           using Graph-to-Sequence Networks                         • Scalars: a b c d e 0 1
Document Overview                                                   • Matrices: A B C D E O I, where O is the empty matrix
                                                                    and I is the identity matrix.
This document supplements the submission Proving Equiva-
                                                                    • Vectors: v w x y z o, where o is the empty vector.
lence Between Complex Expressions Using Graph-to-Sequence
                                                                    • Summary: 16 operations, 20 terminal symbols
Neural Models. We have provided below numerous additional
                                                                       Initially, GenP1 is called with GenP1("+s -s *s /s
information for completeness. We also provide access to
                                                                   +s -s *s /s +s -s *s /s is ns +m -m *m +m
anonymized software artifacts to replicate our results. Our
                                                                   -m *m +m -m *m im nm tm +v -v *v +v -v *v
supplementary materials are organized as follows:
                                                                   +v -v *v nv",0.94)" In this initial call binary opera-
• Appendix B of this document presents the dataset genera-
                                                                    tions are repeated so that they are more likely to be created
tion approach we developed.
                                                                    than unary operations, and the initial probability that a child
• Appendix C of this document presents exhaustively the
                                                                    of the created graph node will itself be an operation (as op-
language for complex linear algebra expressions we evalaute
                                                                    posed to a terminal symbol) is set to 94%. Since the algorithm
on, including the list of all 147 axioms of equivalence we
                                                                    subtracts a 19% probability for children at each level of the
learned.
                                                                    graph, trees are limited to 7 levels.
• Appendix D of this document presents additional details
                                                                       Algorithm 1 starts execution by randomly selecting an
about the neural network architectures we developed.
                                                                    operation from the set provided as input. When GenP1 is
• The anonymized url https://gofile.io/d/IvqAnp contains all
                                                                    called recursively, the operation set is limited such that the
trained models evaluated in this paper, including scripts to
                                                                    operation produces the correct type as output (scalar, ma-
train them directly from our datasets, using OpenNMT. It
                                                                    trix, or vector). Lines 3 through 15 of the algorithm show an
contains also our code for generating datasets and training
                                                                    example case where the *s operation is processed. This oper-
models, the testsets for our 4 key datasets, and key results
                                                                    ation requires scalar operands. If the probability of children
files from our testset evaluations.
                                                                    at this level is met, then GenP1 is called recursively with
• Appendix E of this document presents complementary ex-
                                                                    only scalar operands available, otherwise a random scalar
perimental results and additional in-depth details on results
                                                                    operand is chosen.
presented in the main paper body.
                                                                       The text for algorithm 1 does not show the process for all
                                                                    operations. Certain operations, such as *v, have a variety
B Dataset generation
                                                                    of operand types that can be chosen. The *v operand is a
B.1 Generation of Examples                                          multiplication which produces a vector. As such, 𝐴𝑣 (matrix
Machine learning benefits from large training sets, so in           times vector), 𝑏𝑣 (scalar times vector), or 𝑣𝑐 (vector times
order to produce this data, we created algorithms that would        scalar) are all valid options and will be chosen randomly.
generate programs meeting a given language grammar along               After generating a program which follows the grammar
with target programs which could be reached by applying a           rules of our language, algorithm 2 will produce a new pro-
given axiom set. By creating this process, we could create as       gram along with a set of rewrite rules which transform the
large and varied a dataset as our machine learning approach         source program to the target program.
required.                                                              Algorithm 2 receives as input the source program (or sub-
   Algorithm 1 provides an overview of the full program gen-        program) along with the path to the current root node
eration algorithm. For this generation process, we define a set     of the source program. If the source program is a terminal
of operations and operands on scalars, matrices, and vectors.       symbol, the algorithm returns with no action taken. Oth-
For our process, we presume matrix and vector dimensions            erwise, the program starts with an operation and the algo-
are appropriate for the given operation as such dimension           rithm proceeds to process options for transforming the given
checks are simple to implement and are not considered in our        operation. For our wholeproof10 and wholeproof5 datasets,
procedure. Note the token syntax here is exactly the one used       algorithm 2 is only called once, simplifying the possible node
by our system, and is strictly semantically equivalent to the       order and proof complexity. for the axiomstep10 and axiom-
mathematical notations used to describe these operations,           step5 datasets, algorithm 2 is called multiple times, allowing
e.g. 1N is 1.                                                       for the possibility that after a path is chosen for one axiom
• Scalar operations: +s -s *s /s is ns, where is the                any node can be accessed for the next axiom (including the
unary reciprical and ns is the unary negation.                      same node).
                                                                       As shown on line 10 of the algorithm, when the operation
                                                                13 and children meet the conditions necessary for a rewrite rule
pe-graph2axiom, June, 2021, ArXiV                                    Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet


 Algorithm 2: GenP2                                                  (in this case NeutralOp), the rule is applied with some
  Result: Second program and transform_sequence                      probability (in this case 50%). Note that before processing a
  Input : P1, path                                                   node, the left and right operands are further analyzed to de-
  Output : P2                                                        termine their operators and operands as well (or ⊥ if the child
                                                                     is a terminal). Processing the left and right operands allows
1  if terminal symbol then                                           for complex axioms to be applied, such as distribution or fac-
 2      return P1                                                    torization. When a rule is applied, the rewrite rule is added to
 3 end                                                               the rewrite rule sequence and a new target program is gener-
 4 op = find operator of P1                                          ated for any remaining subtrees. When creating the rewrite
 5 L = find left operand of P1                                       rules for subtrees, the path variable is updated as rewrites
 6 R = find right operand of P1                                      are done. In the case of NeutralOp, the current node is
 7 Lop,LL,LR = operator and operands of left child                   being updated, so the path is not changed. But in the case of
 8 Rop,RL,RR = operator and operands of right child                  the Commute rule, the return would be generated with (op
 9 // Randomly apply transform if allowed
                                                                     GenP2(R,path."left ") GenP2(L,path."right
10 if random < 0.5 and ((op == "+v" and (L == "o" or R ==
                                                                     ")) which creates rewrite rules for the prior right and left
                                                                     operands of the op and updates the path used to the new
     "o")) or (op == "-v" and R == "o")) then
                                                                     node positions. In order to analyze nearly equal programs,
11      append path."NeutralOp " to transform_sequence
                                                                     illegal rewrites can be optionally enabled; for example, com-
12      // Eliminate unnecessary operator and 0 vector
                                                                     muting a subtraction operation or mutating one operation
13      if L == "o" then                                             into another. In that case, the GenP2 process continues to
14           return GenP2(R,path)                                    create a target program, but transform_sequence is
15      else                                                         set to Not_equal.
16           return GenP2(L,path)                                       After these generation algorithms are run, a final data
17      end                                                          preparation process is done which prunes the data set for
18 end                                                               the learning algorithm. The pruning used on our final data
                                                                     set insures that the (𝑃1, 𝑃2) program pair total to 100 tokens
                                                                     or fewer (where a token is an operation or terminal), that
 Algorithm 1: GenP1                                                  the graph is such that every node is reachable from the root
  Result: Prefix notation of computation with                        with a path of length 6 or less, and that there are 10 or fewer
          parenthesis                                                rewrite rules applied. But within these restrictions, we assert
  Input : Ops, P                                                     that our random production rule procedure has a non-zero
  Output : (op L R) or (op L)                                        probability of producing any program allowed by the gram-
1  op = select randomly from Ops                                     mar. Also, the pruning insures that there are no lexically
2  // Create subtree for chosen op                                   equivalent programs in the process and removes some of the
 3 if op == "*s" then
                                                                     cases with fewer than 10 rewrite rules generated to bias the
 4      if random < P then                                           dataset to longer rewrite sequences. Table 1 details the dis-
 5          L = GenP1("+s -s *s /s +s -s *s /s is ns",P-0.19)        tribution of rewrite rules created by the full process. Section
                                                                     C details all axioms when variable types and operators are
 6      else
                                                                     considered.
 7          L = select random scalar operand
                                                                        We produce equivalent program samples by pseudo-randomly
 8      end
                                                                     applying axioms on one randomly generated program to
 9      if random < P then                                           produce a rewrite sequence and the associated equivalent
10          R = GenP1("+s -s *s /s +s -s *s /s is ns",P-0.19)        program. Given a randomly selected node in the program
11      else                                                         graph, our process checks which axiom(s) can be applied.
12          R = select random scalar operand                         E.g., the +𝑚 operator can have the Commute axiom applied,
13      end                                                          or depending on subtrees it may be allowed to have the Fac-
14      return (op L R)                                              torleft axiom applied, as discussed in Sec. 6. Generally we
15 end                                                               choose to apply or not an operator with 50% probability, so
16 // Other ops may have more complex options for                    that pe-graph2axiom is forced to rely on analysis of the
     children types.                                                 two programs to determine whether an operator is applied
17 // (For example, "*m" may have a matrix multiplied by             instead of learning a bias due to the local node features.
     a scalar or matrix)
18 ...


                                                                14
Proving Equivalence Between Complex Expressions                                          pe-graph2axiom, June, 2021, ArXiV
                                      Table 7. Counts for equivalence proof possibilities
                                                                          Proof length in axioms
                Proof description                    1            2         3          4         5          6         7
                All Possible nodes and axioms     5933    3.5E+07      2.1E+11   1.2E+15   7.4E+18   4.4E+22    2.6E+26
                Sample Node + Any Axiom            226      46900      1.5E+07   8.8E+09   5.0E+12   3.3E+15    2.7E+18
                Sample Node + Legal Axiom          11.2       77.8         931     15812   3.4E+05   8.2E+06    1.8E+08
                Unique Programs from Sample         9.2       47.4         264      1574     10052     65176    4.6E+05


B.2   Intermediate program generation                                   Variable types We model programs made of scalars, vec-
The intermediate program generation algorithm is very sim-              tors and matrices. We limit programs to contain no more
ilar to algorithm 2. For program generation of the target               than 5 distinct variable names of each type in a program:
program, algorithm 2 will check that a node can legally ap-             • Scalar variables are noted 𝑎, 𝑏, ..., 𝑒.
ply a given rule, apply the rule with some probability, record          • Vector variables are noted 𝑣®, 𝑤,
                                                                                                         ® ..., 𝑧®.
the action, and process the remaining program. For interme-             • Matrix variables are noted 𝐴, 𝐵, ..., 𝐸.
diate program generation, we begin with a 𝑃1 and a rewrite                Note we also explicitly distinguish the neutral and ab-
rule. We follow the path provided to identify the node, check           sorbing elements for scalars and matrices, e.g. 1 = 1N . This
that a node can legally accept a rule, apply the rule, and re-          enables the creation of simplification of expressions as a
turn the adjusted program. If a rule cannot legally be applied,         program equivalence problem, e.g. if 𝐴 + 𝐵 − (𝐵 + 𝐴) = 0K×K
𝑃1 is not successfully transformed. If a rule can be legally            Unary operators We model 6 distinct unary operators, all
applied to 𝑃1, the program is compared lexically to 𝑃2 and if           applicable to any variable of the appropriate type:
they match then equivalence has been proven.                            • is(a) = 𝑎 −1 is the unary reciprocal for scalars, im(A)
                                                                        = 𝐴−1 is matrix inverse.
B.3   Complexity of Proving Equivalence
                                                                        • ns(a) = −𝑎 is unary negation for scalars, nv(v) = −®  𝑣
Table 7 shows the complexity of the solution space for our              for vectors, nm(M) = −𝑀 for matrices.
problem for proofs from our AxiomStep10 test dataset up to              • tm(M) = 𝑀 𝑡 is matrix transposition.
length 7 (deterministically computing all possible programs
requires too many resources for longer proof lengths). The              Binary operators We model 10 distinct binary operators
’All possible nodes and axioms’ row includes the total num-             that operate on two values. 7 operators require the same
ber of proofs of a given length available to our problem space.         type for both operands, while 3 enable multi-type operands
The entry 5933 for a single axiom represents that for an AST           (e.g., scaling a matrix by a scalar). Note we do not consider
depth of 7 we have 43 axioms which can be applied to all                potential vector/matrix size compatibility criterion for these
63 possible operator nodes and 104 axioms which can be                  operators, in fact we do not represent vector or matrix sizes
applied to the 31 nodes which possibly have child operator              at all in our language, for simplicity.
nodes themselves: 63*43+31*104=5933. Subsequent columns                 • +s(a, b)= 𝑎 + 𝑏, the addition on scalars, along with
can select repeatedly from the same set growing as 59332               -s(a,b) = 𝑎 − 𝑏, *s(a,b) = 𝑎 ∗ 𝑏 and /s(a,b) = 𝑎/𝑏.
to 59337 . The ’sample node + axiom group’ row is based on              • +v( v, w) = 𝑣® + 𝑤,   ® the addition on vectors, along with
our 10,000 sample test dataset and represents the possible             -v( v , w) = 𝑣® − 𝑤,   ® *v( v, w) = 𝑣®.𝑤® the dot product
selection of any of the 14 axiom groups being applied to                between two vectors, producing a scalar.
any node in the program. The ’sample node + legal axiom’                • +m(A, B) = 𝐴 + 𝐵, the addition on matrices, along with
row represents only legal node plus legal axiom group being            -m(A, B) = 𝐴 − 𝐵, and *m(A, B) = 𝐴𝐵 the product of
applied and effectively represents the total number of pro-             matrices.
grams derivable from the start program in the test dataset.             • *m(a,A) = 𝑎𝐴¤ and *m(A,a) = 𝐴𝑎¤ are used to represent
The final row ’Sample derivable unique programs’ represents             scaling a matrix by a scalar.
the total number of programs derived from legal node and                • *m(v,A) = 𝑣®𝐴 represents a vector-matrix product.
axiom sequences which are lexically unique.                             • *v(a,v) = 𝑎®    𝑣 and *v(v,a) = 𝑣®𝑎 represent scaling a
                                                                       vector by a scalar.
C     Language and Axioms for Complex                                   List of axioms of equivalence Tables 8-9 show the full
      Linear Algebra Expressions                                        147 axioms supported by our rewrite rules. Many rewrite
We now provide the complete description of the input lan-               rules can be applied to all 3 variable types as well as multiple
guage for multi-type linear algebra expressions we use to               operator types.
evaluate our work, and the complete list of all axioms that
are used to compute equivalence between programs.
                                                                  15
pe-graph2axiom, June, 2021, ArXiV                                Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

 Rewrite Rule      ID   Example(s)                            Rewrite Rule     ID   Example(s)
 Cancel            1    (a - a) → 0                           AbsorbOp         28   (a * 0) → 0
                   2    (b/b) → 1                                              29   (0 * a) → 0
                   3    (A - A) → O                                            30   (A * 0) → O
                   4    (𝐴 ∗ 𝐴−1 ) → I                                         31   (0 * A) → O
                   5    (𝐴−1 ∗ 𝐴) → I                                          32   (A * O) → O
                   6    (v - v) → o                                            33   (O * A) → O
 NeutralOp         7    (a + 0) → a                                            34   (A * o) → o
                   8    (0 + a) → a                                            35   (a * o) → o
                   9    (a - 0) → a                                            36   (o * a) → o
                   10   (a * 1) → a                                            37   (0 * v) → o
                   11   (1 * a) → a                                            38   (v * 0) → o
                   13   (a / 1) → a                                            39   (O * v) → o
                   14   (A + O) → A                           Commute          40   (a + b) → (b + a)
                   15   (O + A) → A                                            41   (a * b) → (b * a)
                   16   (A - O) → A                                            42   (A + B) → (B + A)
                   17   (A * I) → A                                            43   (A * a) → (a * A)
                   18   (I * A) → A                                            44   (a * A) → (A * A)
                   19   (v + o) → v                                            45   (A * O) → (O * A)
                   20   (o + v) → v                                            46   (O * A) → (A * O)
                   21   (v - o) → v                                            47   (A * I) → (I * A)
 DoubleOp          22   -(-a)) → a                                             48   (I * A) → (A * I)
                   23   (𝑎 −1 ) −1 → a                                         49   (v + w) → (w + v)
                   24   −(−𝐴) → 𝐴                                              50   (v * a) → (a * v)
                   25   (𝐴−1 ) −1 → 𝐴                                          51   (a * v) → (v * a)
                   26   (𝐴𝑡 )𝑡 → 𝐴                            DistributeLeft   52   (a + b)c → ac + bc
                   27   −(−𝑣)) → 𝑣                                             53   (a - b)c → ac - bc
 DistributeRight   64   a(b + c) → ab + ac                                     54   (a + b)/c → a/c + b/c
                   65   a(b - c) → ab - ac                                     55   (a - b)/c → a/c - b/c
                   66   a(v + w) → av + av                                     56   (v + w)*a → va + wa
                   67   a(v - w) → av - av                                     57   (v - w)*a → va - wa
                   68   A(B + C) → AB + AC                                     58   (A + B)C → AC + BC
                   69   A(B - C) → AB - AC                                     59   (A - B)C → AC - BC
                   70   a(B + C) → aB + aC                                     60   (A + B)v → Av + Bv
                   71   a(B - C) → aB - aC                                     61   (A - B)v → Av - Bv
                                                                               62   (A + B)a → Aa + Ba
                                                                               63   (A - B)a → Aa - Ba
        Table 8. Full axiom count when all type options and other supported permutations are included (part 1 of 2)




                                                            16
Proving Equivalence Between Complex Expressions                                         pe-graph2axiom, June, 2021, ArXiV

 Rewrite Rule      ID    Example(s)                           Rewrite Rule       ID    Example(s)
 FactorLeft        72    ab + ac → a(b+c)                     AssociativeRight   113   (a+b)+c → a+(b+c)
                   73    ab - ac → a(b-c)                                        114   (a+b)-c → a+(b-c)
                   74    AB + AC → A(B+C)                                        115   (ab)c → a(bc)
                   75    AB - AC → A(B-C)                                        116   (A+B)+C → A+(B+C)
                   76    Av + Aw → A(v+w)                                        117   (A+B)-C → A+(B-C)
                   77    Av - Aw → A(v-w)                                        118   (AB)C → A(BC)
                   78    Aa + Ab → A(a+b)                                        119   (AB)a → A(Ba)
                   79    Aa - Ab → A(a-b)                                        120   (Aa)B → A(aB)
                   80    va + vb → v(a+b)                                        121   (aA)B → a(AB)
                   81    va - vb → v(a-b)                                        122   (Av)a → A(va)
 FactorRight       82    ac + bc → (a+b)c                                        123   (Aa)v → A(av)
                   83    ac - bc → (a-b)c                                        124   (aA)v → a(Av)
                   84    a/c + b/c → (a+b)/c                                     125   (va)b → v(ab)
                   85    a/c - b/c → (a-b)/c                                     126   (av)b → a(vb)
                   86    AC + BC → (A+B)C                                        127   (ab)v → a(bv)
                   87    AC - BC → (A-B)C                                        128   (v+w)+x → v+(w+x)
                   88    Av + Bv → (A+B)v                                        129   (v+w)-x → v+(w-x)
                   89    Av - Bv → (A-B)v                     FlipLeft           130   -(a - b) → b-a
                   90    Aa + Ba → (A+B)a                                        131   (𝑎/𝑏) −1 → b/a
                   91    Aa - Ba → (A-B)a                                        132   −(𝐴 − 𝐵) → (B - A)
                   92    va + wa → (v+w)a                                        133   −(𝑣 − 𝑤) → (w - v)
                   93    va - wa → (v-w)a                     FlipRight          134   a/(b/c) → a(c/b)
 AssociativeLeft   94    a+(b+c) → (a+b)+c                                       135   𝑎/(𝑏 −1 ) → ab
                   95    a+(b-c) → (a+b)-c                                       136   a-(b-c) → a+(c-b)
                   96    a(bc) → (ab)c                                           137   a-(-b) → a+b
                   97    a(b/c) → (ab)/c                                         138   A-(B-C) → A+(C-B)
                   98    A+(B+C) → (A+B)+C                                       139   A-(-B) → A+B
                   99    A+(B-C) → (A+B)-C                                       140   v-(w-x) → v+(x-w)
                   100   A(BC) → (AB)C                                           141   v-(-w) → v+w
                   101   A(Ba) → (AB)a                        Transpose          142   (𝐴𝐵) → (𝐵𝑡 𝐴𝑡 )𝑡
                   102   A(aB) → (Aa)B                                           143   (𝐴 + 𝐵) → (𝐴𝑡 + 𝐵𝑡 )𝑡
                   103   a(AB) → (aA)B                                           144   (𝐴 − 𝐵) → (𝐴𝑡 − 𝐵𝑡 )𝑡
                   104   A(Bv) → (AB)v                                           145   (𝐴𝐵)𝑡 → 𝐵𝑡 𝐴𝑡
                   105   A(va) → (Av)a                                           146   (𝐴 + 𝐵)𝑡 → 𝐴𝑡 + 𝐵𝑡
                   106   A(av) → (Aa)v                                           147   (𝐴 − 𝐵)𝑡 → 𝐴𝑡 − 𝐵𝑡
                   107   a(Av) → (aA)v
                   108   v+(w+x) → (v+w)+x
                   109   v+(w-x) → (v+w)-x
                   110   v(ab) → (va)b
                   111   a(vb) → (av)b
                   112   a(bv) → (ab)v
        Table 9. Full axiom count when all type options and other supported permutations are included (part 2 of 2)




                                                            17
pe-graph2axiom, June, 2021, ArXiV                                       Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet




                                       Figure 4. pe-graph2axiom System Overview

D    Details on neural network model                                    are unified in a single graph using a single connecting root
Figure 4 overviews the entire pe-graph2axiom architec-                  node; and where additional edges are inserted to make the
ture including sample generation, the graph-to-sequence                 graph fully walkable.
network, the intermediate program generation, and lexical                  In our full model, we support 9 edge types and their re-
equivalence checker. In this section we will discuss the im-            verse edges. The edge types are: 1) left child of binary op, 2)
plementation details of these components.                               right child of binary op, 3) child of unary op, 4) root node
                                                                        to program 1, 5) root node to program 2, 6-9) there are 4
Graph neural network internal representation The sam-                   edge types for the four node grandchilden (LL, LR, RL, RR).
ple generation discussed in section 4 provides input to the             After the node hidden states and edge adjacency matrix are
Node Initialization module in Fig. 4 to create the initial state        initialized, the network is ready to begin processing. This
of our graph neural network. For each node in the program               initial state is indicated in figure 6 by the solid circles in the
graph, a node will be initialized in our graph neural network.          lower left of the diagram.
Each node has a hidden state represented by a vector of 256
floating point values which are used to create an embedding             Beam search A typical approach when using sequence-
for the full meaning of the given node. Initially all 256 di-           to-sequence systems is to enable beam search, the process
mensions of the hidden states of the nodes are set to zero              of asking for multiple answers to the same question to the
except for 2. Given 𝑁 tokens in our input program language,             network. It is particularly relevant when creating outputs
one of the dimensions from 1 through 𝑁 of a node will be                which can be automatically checked [1, 18]. Beam search can
set based on the token at the program position that the node            be viewed as proposing multiple possible axioms to apply.
represents. For example, if the scalar variable 𝑎 is assigned           Given the stochastic nature of generation model, a beam
to be token 3 in our language, then the 𝑎 nodes of Fig. 5               width of 𝑛 can be thought of as creating the 𝑛 most likely
recalled below would have their 3rd dimension initialized to            sequences given the training data the model as learned on.
1.0. This is a one-hot encoding similar to that used in neural          Each proposal can be checked for validity, the first valid one
machine translation models which leverage Word2vec [44].                is outputted by the system, demonstrating equivalence. Our
The second non-zero dimension in our node initialization                system builds on the neural network beam search provided
indicates the tree depth, with the root for the program being           by OpenNMT to create a ’system beam search’ of variable
at depth 1. We set the dimension 𝑁 +𝑑𝑒𝑝𝑡ℎ to 1.0; hence, the            width. In particular, we set the OpenNMT network beam
𝑎 nodes in Fig 5, which vary from level 2 or 3 in the graph,            search to 3, which constrains the token generator to produce
would set dimension 𝑁 + 2 or 𝑁 + 3 to 1. In addition to nodes           3 possible axiom/node proposals for a given pair of input
correlating to all tokens in both input programs, we initial-           programs. Using these 3 proposals, when our system beam
ize a root node for program comparison which has edges                  width is 10, we build up to 10 intermediate programs that are
connecting to the root nodes of both programs. The root                 being processed in the search for a proof. To illustrate with
node does not represent a token from the language, but it is            a system beam width of 5, after 𝑃1 and 𝑃2 are provided to
initialized with a 1.0 in a hidden state dimension reserved             the neural network, 3 possible intermediate programs may
for its identification.                                                 be created (so long as all axioms are legal and don’t produce
   For a graph neural network, the edge connections between             duplicates). After those 3 intermediates are processed, 9 pos-
nodes are a crucial part of the setup. In particular, to match          sible new intermediates are created, all of which are checked
the formulation of our problem, we must ease the ability of             for lexical equivalence with 𝑃2, but only 5 of which are fed
the network to walk the input program graphs. We therefore              back into the neural network for further axiom generation.
designed a unified graph input, where both program graphs               This process is continued for up to 12 axioms at which point
                                                                        the system concludes an equivalence proof cannot be found
                                                                   18
Proving Equivalence Between Complex Expressions                                                           pe-graph2axiom, June, 2021, ArXiV


                  ∗                               ∗                                       +                                       +
          𝑎               +
                  ∗               ∗          𝑎        +                           ∗               ∗                       ∗               ∗
              1       𝑏       1       𝑐           𝑏       𝑐                   𝑎       𝑏       𝑎       𝑐               𝑎       𝑐       𝑎       𝑏
      (a) 𝑎 ∗ (1 ∗ 𝑏 + 1 ∗ 𝑐)             (b) 𝑎 ∗ (𝑏 + 𝑐)                     (c) 𝑎 ∗ 𝑏 + 𝑎 ∗ 𝑐                      (d) 𝑎 ∗ 𝑐 + 𝑎 ∗ 𝑏

                                                 Figure 5. Examples of Computations




                                 Figure 6. Graph-to-sequence neural network data flow details.
Table 10. Hyperparameter experiments. Summary of best            examples of axioms given similar input programs. For exam-
validation token accuracy result after 2 runs for up to 100,000  ple, proving "(a+b)(c+d) = (b+a)(d+c)" requires commuting
training iterations. The golden model has 256 graph nodes        the left and right subexpressions. The training dataset could
and decoder dimensions, 2 decoder LSTM layers, starts train-     have similar programs which are sometimes transformed
ing with a learning rate of 0.8, and uses 10 steps to stabilize  first with a right Commute and then a left or vice-versa.
the GGNN encoder.                                                Given this data, the network would learn to apply one or the
                                                                 other (it would not get trained to use associativity for these
Parameter                               Value        Validation  program pairs for example), hence the actual output given
                                                token accuracy   may or may not match the validation target axiom. We will
Golden model                                              83.89  discuss this further in section E.2.
Graph node+decoder LSTM dimension         192                 83.89        Training convergence Since our model trains on axiomatic
                                          320                 83.58        proofs which may vary in order (allowing 2 or 3 options to
Decoder LSTM layers                          1                83.53
                                                                           be correct and occur in the training set), we see our training
Initial learning rate                     0.75                83.76
                                                                           and token accuracies plateau below 90% during training for
                                          0.85                83.57
GGNN stability steps                        12                83.19        AxiomStep10 as shown in Figure 7. Full testset proof accura-
                                             8                83.61        cies for beam width 10 exceed 90%, but also plateau along
                                                                           with the training and validation results. This result differs
                                                                           from our WholeProof10 training, which achieves training
and the programs are likely not equivalent. We evaluate                    and validation accuracies above 96% because the expected
in Sec. 6 beam sizes ranging from 1 to 10, showing higher                  axiom sequence is more predictable, but as we have seen less
success with larger beams.                                                 generalized.
                                                                              As another observation on generalization and overfitting,
E     Details on Experimental Results                                      we note that figure 7 shows a slight separation between
E.1   Complementary Results and Observations                               the training and validation accuracies starting at around
                                                                           iteration 180,000. While the training accuracy rises slowly,
Table 10 describes part of our neural network hyperparam-
                                                                           validation accuracy plateaus, indicating slight overfitting on
eter tuning showing that our golden model has as high a
                                                                           the training data. Yet our model continues to slowly increase
result as other variations explored. Note that the validation
                                                                           in quality, with the model snapshot that scores best on both
token accuracy is not too high (it’s not above 90%) despite
                                                                           validation and test accuracies occurring at iteration 300,000.
the ability to predict full correct proofs with over 93% accu-
                                                                           This is our golden model, with 93.1% of P1 to P2 proofs
racy. This is because the training dataset can have multiple
                                                                           accurately found using beam width 10.
                                                                      19
pe-graph2axiom, June, 2021, ArXiV                                        Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

                                                                         up to 10 rewrite rules, 𝑃1 and 𝑃2 can have up to 50 AST nodes
                                                                         each, and an AST depth of up to 7. AxiomStep5 has samples
                                                                         requiring up to 5 rewrite rules, 𝑃1 and 𝑃2 can have up to
                                                                         25 AST nodes each, and an AST depth of up to 6. Tables 12
                                                                         and 13 (repeated from main paper below) demonstrate the
                                                                         ability of a model trained on AxiomStep5 to perform well
                                                                         on the larger distribution of programs from AxiomStep10,
                                                                         implying that the model has generalized well to our program
Figure 7. Model training percentage accuracy up to 300,000               equivalence problem and that pe-graph2axiom does not
iterations on AxiomStep10. Training and Validation accura-               overfit its response to merely the training set distribution.
cies are per-token on the target axioms in the samples. Test                Table 13 illustrates the ability of a model trained on Ax-
accuracies are for full correct proofs of P1 to P2.                      iomStep5 (i.e., limited to proofs of length 5) to perform well
                                                                         when evaluated on the more complex AxiomStep10, which
                                                                         includes proofs of unseen length of up to 10. The robustness
Testing simpler models In addition to the sequence-to-                   to the input program complexity is illustrated with the 86%
sequence and graph-to-sequence models, we explored a feed-               pass rate on AST depth 7, for the model trained on Axiom-
forward equal/not equal classifier on a simple version of our            Step5 which never saw programs of depth 7 during training.
language. That model uses an autoencoder on the program                     As an indication of the breadth of equivalent programs
to find an embedding of the program and then a classifier                represented by AxiomStep10 relative to WholeProof10, table
based on the program embeddings found. It achieves a 73%                 14 shows the full detail of models trained on all 4 datasets
accuracy on identifying equivalent pairs in the test data,               when tested on test data from all 4 datasets. AxiomStep10,
which, as expected, is much lower than the full proof rate               while training on our broadest dataset in which axioms can
of 93% achieved with a graph-to-sequence proof generator                 be applied to nodes repeatedly and in variable order, achieves
on our full language. This simple experiment highlights the              a 93% average success rate. 72% of the proofs of length 6
importance of a system which prevents the false positives                from the WholeProof10 testset were solved by the model
which a classifier might have by creating a verifiable proof.            trained on WholeProof10, but only 5% of such proofs from
   We explore initial language generation using a simple lan-            AxiomStep10 were, suggesting the method of generating
guage in order to assess feasibility of different approaches.            AxiomStep pairs covers the problem space more thoroughly.
For fine tuning network parameters and architectural fea-                   The complete result for the WholeProof10 model on the
tures, we add more complexity to the language as shown in                WholeProof10 dataset was 8,388 out of 10,000 program pairs
table 11. Language IDs 1 through 3 are all based on a simple             had a correct proof found; of those, 8,350 were the exact proof
grammar which only allows the "+" or "-" operators on scalar             created during 𝑃1, 𝑃2 generation, implying that WholeProof10,
variables labeled a through j. The only axiom is Commute,                while performing well on its own testset distribution, is not
which can be applied on up to 3 nodes in language IDs 2 and              learning to generalize to alternative proof paths.
3. Language ID 4 adds the scalar constants 0 and 1, scalar
operations * and /, and 4 more axioms. We perform a fair                 Manual verifications We conducted a series of manual
amount of network development on this model in an effort                 verifications of the system used to produce all the above
to maintain high accuracy rates. Language ID also 4 expands              results. First, we are happy to confirm that most likely 𝐴𝐵 ≠
the operands to 3 types and hence the number of operators                𝐵𝐴 given no verifiable equivalence sequence was produced,
also increases. To speed up model evaluation, we reduced the             but that provably 𝑎𝑏 = 𝑏𝑎 indeed. We also verified that
                                                                           𝑡
program length for IDs 5, 6, and 7, allowing us to train larger          𝐴𝑡 (𝐵 + 𝐶 − 𝐶) = 𝐴𝐵, and that 𝐴𝐵®      𝑣 − 𝐴𝐵𝑤® = 𝐴𝐵(® 𝑣 − 𝑤)
                                                                                                                                    ®
data sets for more epochs. ID 7 is a forward looking-model               which would be a much faster implementation. The system
which makes a minor increment to the language to support                 correctly suggests that 𝐴𝐵®𝑣 − 𝐵𝐴𝑤® ≠ 𝐴𝐵(®  𝑣 − 𝑤).
                                                                                                                         ® We ensured
the analysis of loop rolling and unrolling, discussed further            that 𝐴𝑡 (𝐴𝐴𝑡 ) −1𝐴 ≠ 𝐴𝑡 (𝐴𝐴−1 )𝑡 𝐴, from a typo we once made
in section E.3. ID 8 is the WholeProof5 model in relation to             when typing the computation of an orthonormal sub-space.
these early experiments.                                                 We also verified that indeed 𝐴𝐵 + 𝐴𝐶 + 𝑎𝐷 − 𝑎𝐷 = 𝐴(𝐵 + 𝐶).
   We designed our datasets in section 4 with the goal of                Generalizing variable types We explored the ability of
using the varied models to understand the generalizability of            the model to understand variable typing by training a model
pe-graph2axiom and to show that our model is not over-                   with the AxiomStep10 distribution but with no samples that
fitting on training data. For these next experiments, all results        included the scalar variable ’e’ and scalar multiplication
of for beam width 10, which provides for a neural-network                ∗𝑠 . This removed about 50% of the training set, as longer
directed search of up to 10 axiomatic proofs of equivalence              programs were often included both tokens. When tested
for each program pair. Recall that our most complex dataset              with the unaltered AxiomStep10 test set and beam width
is AxiomStep10 which includes (𝑃1, 𝑃2, 𝑆) samples requiring              10, test samples that included a scalar variable not ’e’ and
                                                                    20
Proving Equivalence Between Complex Expressions                                                                                                              pe-graph2axiom, June, 2021, ArXiV




                                                                                                                                      Rewrite rules length




                                                                                                                                                                                                                          with beam width 10
                                                                                                                                                                                                      with beam width 1
                                                                                                                                                                                                      Percent matching



                                                                                                                                                                                                                          Percent matching
                                                                                                                                                             Graph2seq (G2S)



                                                                                                                                                                                  Training set size
                                                                                                                                                             or seq2seq (S2S)
                                                                                                                    Program length
                                                                        # Operators




                                                                                                    # Operands
                                                                                       # Axioms
      ID   Description
      1    Rewrite sequence is only single Commute, uses sequence-to-   2               1           10              3-19              1-5                    S2S                  80,000              90.0%               96.2%
           sequence model
      2    Rewrite sequence is exactly 2 Commutes, uses sequence-to-    2               1           10              5-24              3-10                   S2S                  80,000              80.3%               96.5%
           sequence model
      3    Rewrite sequence exactly 2 Commutes                          2               1           10              5-24              3-10                   G2S                  80,000              98.9%               99.8%
      4    Rewrite sequence exactly 3 Commutes                          2               1           10              7-45              5-15                   G2S                  80,000              91.4%               99.0%
      5    Rewrite sequence 1 to 3 Commutes                             2               1           10              3-45              1-15                   G2S                  180,000             97.1%               99.2%
      7    Commute, Noop, Cancel, Distribute Left, Distribute Right     4               5           12              3-45              1-15                   G2S                  180,000             93.1%               97.4%
      8    Scalars, Vectors, and Matrixes                               16              5           20              3-30              1-25                   G2S                  250,000             88.3%               95.6%
      9    13 Axioms                                                    16              13          20              3-30              1-25                   G2S                  400,000             85.5%               95.5%
      10   Rewrite sequence or Not_equal                                16              13          20              3-30              1-25                   G2S                  500,000             79.8%               93.8%
      11   Test sequence-to-sequence                                    16              13          20              3-30              1-25                   S2S                  400,000             59.8%               81.1%
      12   Add loop axioms                                              18              15          20              3-30              1-25                   G2S                  400,000             83.8%               94.7%
           Table 11. Results for various language complexities studied, on non-incremental models (WholeProof).
Table 12. Generalizing to longer P1 inputs. Percentage pass rates for equivalence proofs with P1 having increasing program
graph nodes. The model trained with the AxiomStep5 dataset had no training examples more than 25 program graph nodes
yet it performs relatively well on these more complex problems. The furthest right column shows the pe-graph2axiom
model results on the most complex dataset.

                                                        Testset                        Model trained                                  Model trained
                                                     Sample Count                     on AxiomStep5                                  on AxiomStep10
                                   P1 nodes            AS5      AS10                  AS5                        AS10                AS5                              AS10
                                         1-5           231       109                  100                         100                100                                   100
                                        6-10          2147      1050                  100                          99                 99                                    99
                                       11-15          3980      2175                   99                          96                 99                                    96
                                       16-20          2583      2327                   98                          92                 98                                    93
                                       21-25          1059      1989                   97                          89                 98                                    92
                                       26-30             0      1229                  N/A                          83                N/A                                    90
                                       31-35             0       698                  N/A                          78                N/A                                    88
                                       36-40             0       304                  N/A                          74                N/A                                    87
                                       41-45             0       101                  N/A                          68                N/A                                    84
                                       46-50             0        27                  N/A                          67                N/A                                    85
                                         All         10000     10000                   99                          90                 99                                    93

                               Table 13. Performance vs. AST size: counts and percentage pass rates.

                                                         Testset                       Model trained                                  Model trained
                                                      Sample Count                    on AxiomStep5                                  on AxiomStep10
                                  AST depth             AS5      AS10                 AS5                        AS10                AS5                                 AS10
                                            2             5         3                  100                         100                100                                       100
                                            3           306       133                  100                         100                100                                       100
                                            4          1489       577                  100                          99                 99                                        99
                                            5          4744      1844                   99                          94                 98                                        95
                                            6          3456      4308                   98                          90                 98                                        93
                                            7             0      3135                  n/a                          86                n/a                                        92
                                           All        10000     10000                   99                          90                 99                                        93


∗𝑠 were proven equal 90% of the time; test samples that in-                                       For beam width 1 the proof success rates were 72% and 70%
cluded ’e’ and ∗𝑠 were also proven equal 90% of the time.                                         for without and with ’e’, implying that the heavily biased
                                                                                       21
pe-graph2axiom, June, 2021, ArXiV                                        Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

Table 14. Generalizing to longer proofs. Percentage pass rates for equivalence proofs of increasing axiom counts when testing
each of 4 datasets on models trained using each of 4 datasets.

                 Axiom       Model trained on      Model trained on            Model trained on       Model trained on
                Count in    WholeProof5 (WP5)     WholeProof10 (WP10)          AxiomStep5 (AS5)      AxiomStep10 (AS10)
                    Proof WP5 WP10 AS5 AS10 WP5 WP10 AS5                AS10   WP5 WP10 AS5 AS10 WP5 WP10 AS5 AS10
                        1   100 100 100      99    100 100 100          100     100 100 100 100          100 100 100 100
                        2    99 98 66        64     99 99 65             63     100 99 100 99            100 100 100 100
                        3    98 94 34        33     97 95 33             33     100 98 99 98             100 99 99 99
                        4    93 84 16        15     90 88 16             15      98 95 98 97              99 98 98 98
                        5    84 70    8       7     84 82    8            7      96 91 96 95              97 95 96 96
                       6           14         4          72               5           81        88            90          93
                       7            0         1          63               2           67        81            83          87
                       8            0         0          54               1           54        75            73          82
                       9            0         0          47               0           35        64            63          74
                      10            0         0          34               0           24        57            46          66
                      All    95    66   44   27     94   84   44         27      99   87   99   90       99   93     99   93


training set did have a small effect on the system general-               𝑃1, 𝑃2 pair and the system must learn to produce an axiom at
ization. pe-graph2axiom was still able to generalize the                  a location which performs an ’action’ on the ’state’ of 𝑃1 in
relation of ’e’ to the ∗𝑠 operator given that ’e’ was used in             a predictable way. Unlike reinforcement learning, we do not
contexts similar to other scalar variables in the training sam-           produce a reward function and our system cannot learn from
ples that were provided, implying it was forming an internal              a poor reward produced by an incorrect axiom. However, we
representation of a ’scalar’ type by learning from examples.              have demonstrated that our system, as it is presented with
                                                                          a wide distribution of (𝑃1, 𝑃2, 𝑆) tuples to train on, learns a
E.2   Learning that multiple axiom choices are                            probability distribution of possibly correct axioms to produce
      possible                                                            for a given program pair. There may be value in combining
Our AxiomStep10 model is trained on axioms which may                      our graph-neural-network within a reinforcement learning
be applied in varying order in the training set. For example,             framework that used a hindsight mechanism [6] to learn
((𝑎 + 𝑏) ∗ (𝑐 + 𝑑)) = ((𝑏 + 𝑎) ∗ (𝑑 + 𝑐)) may have the training           from every attempted axiom, but it is not immediately ob-
data to Commute the left node 𝑎+𝑏 first and then 𝑐 +𝑑 second;             vious that our approach of learning only from examples of
in the same dataset, ((𝑎+𝑒) ∗ (𝑏 +𝑐)) = ((𝑒 +𝑎) ∗ (𝑐 +𝑏)) might           successful equivalence proofs would be improved.
occur and the training data has the right node Commuted
first. In this way, we expect the model to learn that either              Table 15. Learning multiple output options. When con-
commuting the left or right node is a proper first axiom                  sidering scalar expressions that can be proven equivalent
choice. Table 15 explores the ability of the model to produce             by commuting the left and right subexpressions, such as
such axiom proposals. Given 5 scalar variables, there are                 (𝑎 + 𝑏) (𝑐 + 𝑑) = (𝑏 + 𝑎) (𝑑 + 𝑐), pe-graph2axiom learns
120 possible expressions where two 2-variable additions are               that either the left or right commute can occur first. The
multiplied together such as ((𝑎 + 𝑏) ∗ (𝑐 + 𝑑)). We consider              columns show counts for axioms and locations proposed by
here all 120 program pairs in which the left and right ad-                the token generator with beam width of 3 when given 120
ditions are commuted. The table shows which axioms and                    different scalar expression pairs.
positions are recommended by the graph-to-sequence neural
network model within the pe-graph2axiom system as                                                                   Axiom
most probably moving the 2 programs closer to equivalence                 Beam             Commute         Commute Commute          DistributeLeft
by the beam width 3 on this problem. Note that the 2 correct              position          left child    right child     root                root
axioms are always within the top 3 choices and the other                  First                    49               35         36               0
2 axioms (Commute and DistributeLeft on the root), while                  Second                   58               59          3               0
not necessary for this problem, are at least legal choices for            Third                    13               26         45              36
axioms within our expression language.                                    Any of top 3            120              120         84              36
   The results in table 15 relate to the value of our approach
in relation to reinforcement learning models for proof gen-
eration [22] [9]. To make an analogy with reinforcement                   Exploration of alternate designs In order to design the
learning, in our training, the world ’state’ is presented as a            system, we explored parts of the design space quickly and
                                                                   22
Proving Equivalence Between Complex Expressions                                               pe-graph2axiom, June, 2021, ArXiV

performed several single training run comparisons between                 For the first output case, the output sequence to produce
2 options, as shown in Table 16.                                       is either Equal or Not_equal. Given a false positive rate
   In cases where 2 options were similar, we chose the model           of 9.6%, these results demonstrate the importance of produc-
which ran faster, or run the models a second time to get               ing a verifiable proof of equivalence when using machine
a more precise evaluation, or use our experience based on              learning for automated equivalence checking. For the sec-
prior experiments to select an option.                                 ond output case, the model can produce either Not_equal
                                                                       or a rewrite rule sequence which can be checked for cor-
Table 16. Example explorations as a single feature or param-           rectness. The source programs for the first and second case
eter is changed. Each comparison is a distinct experiment,             are identical: 250,000 equivalent program pairs and 250,000
as the entire network and language used was being varied.              non-equivalent program pairs. In the second case, the false
                                                                       positive rate from the network is 9.1% (rules predicted for
                                          Match      Match             Not_equal programs), but the model only produces correct
 Options compared                         beam 1     beam 10           rewrite rules between actual equivalent programs in 70.7%
 1 layer LSTM vs                          198        1380              of the cases.
 2 layer LSTM vs                          5020       9457                 One challenge with a model that produce rules or Not_equal
 3 layer LSTM                             4358       8728              is that beam widths beyond 1 are less usable. Consider that
 No edges to grandchild nodes vs          9244       9728              with a beam width of 1, if the network predicts Not_equal
 Edges to grandchild nodes                9284       9774              then the checker would conclude the programs are not equal
 Encoder->Decoder only root node vs       8616       9472
                                                                       (which is correct for 90.9% of the actually not equal pro-
 Encoder->Decoder avg all nodes           7828       9292
                                                                       grams). With a beam width of 10, there would be more pro-
                                                                       posed rewrite rules for equal programs to test with, but if
   Experiments such as these informed our final network ar-            1 of the 10 proposals is Not_equal, should the checker
chitecture. For example, in pe-graph2axiom, we include                 conclude they are not equal? Or should the the checker only
4 edges with learnable weight matrices from a node to its              consider the most likely prediction (beam width 1) when
grandchildren because such edges were found to improve re-             checking for non-equivalence? The third and fourth net-
sults on multiple runs. Li et al. [39] discusses the importance        work output cases provide an answer. For these 2 cases, the
of selecting the optimal process for aggregating the graph in-         training set is 400,000 equivalent program pairs - none are
formation hence we explore that issue for our network. Our             non-equivalent. 250,000 of these pairs are identical to the
approach uses the root comparison node to create aggregate             equivalent programs in the first 2 cases, and 150,000 are new
the graph information for the decoder as it performs better            but were produced using the same random generation pro-
than a node averaging.                                                 cess. Note that by requiring the network to focus only on
Including Not_equal option Table 17 analyzes the chal-                 creating rewrite rules, beam width 1 is able to create cor-
lenge related to a model which only predicts Equal or Not_equal        rect rewrite rules for 87.8% of the equivalent programs. And
for program pairs along with various options which produce             now, since we’ve remove the confusion of the Not_equal
rewrite rules which can be checked for correctness. In all 4           prediction option, beam width 10 can be used to produce
output cases shown, 2 programs are provided as input. These            10 possible rewrite rule sequences and in 96.2% of the cases
programs use an earlier version of our language model with             these rules are correct. Hence, we propose the preferred use
16 operators, 13 core axioms, and 20 operands generated                model for pe-graph2axiom is to always use the model which
with a distribution similar to WholeProof5.                            is trained for rule generation with beam width 10 and rely
                                                                       on our rule checker to prevent false positives. From the 10
Table 17. Table showing alternate options for handling not             rewrite rule proposals, non-equivalent programs will never
equal programs                                                         have a correct rewrite rule sequence produced, hence we
                                                                       guarantee there are no false positives.
 Network                                 Predicted   Correct
 output                      Predicted   Rules       Rewrite           E.3   An Example of Back-Edge in the Program
 Description        Actual   NotEq       or Eq       Rules                   Graph
 Eq or NotEq,       Eq       5.4%        94.6%       N/A               Figure 8 shows an example of DoX and DoHalf. The new
 Beam width 1       NotEq    90.4%       9.6%        N/A               operators result in 2 new edges in our graph representation
 Rules or NotEq,    Eq       6.6%        93.4%       70.7%             (along with 2 new back-edges): there is a ’loopbody’ edge
 Beam width 1       NotEq    90.9%       9.1%        N/A
                                                                       type from the loop operator node to the start of the subgraph,
 Rules only,        Eq       N/A         100%        87.8%
                                                                       and there is a ’loopfeedback’ edge type from the variable
 Beam width 1       NotEq    N/A         N/A         N/A
 Rules only,        Eq       N/A         100%        96.2%
                                                                       which is written to each loop iteration. These 2 edge types
 Beam width 10      NotEq    N/A         N/A         N/A               are shown in the figure. The new 𝐷𝑜ℎ𝑎𝑙 𝑓 axiom intuitively

                                                                  23
pe-graph2axiom, June, 2021, ArXiV                                   Steve Kommrusch, Théo Barollet and Louis-Noël Pouchet

states that 𝐷𝑜𝑋 (𝑔(𝑦)) = 𝐷𝑜𝐻𝑎𝑙 𝑓 (𝑔(𝑔(𝑦))) (where 𝑦 is the                                                       DoH
variable reused each iteration), and 𝐷𝑜𝑥 states the reverse.
                                                                                                                 /

                                                                                      DoX                    +         𝑐

                                                                                      /                  𝑎       /

                                                                                  +         𝑐                +         𝑐

                                                                              𝑎       𝑏                  𝑎       𝑏
                                                                            (a) DoX(𝑏           =      (b) DoHalf(𝑏 = (𝑎 +
                                                                            (𝑎 + 𝑏)/𝑐)                 (𝑎 + 𝑏)/𝑐)/𝑐)

                                                                    Figure 8. Adding loop constructs creates cycles in the pro-
                                                                    gram graph.




                                                               24
