                                                    From Scientific Texts to Verifiable Code:
                                                    Automating the Process with Transformers
                                                       Changjie Wang                           Mariano Scazzariello                            Marco Chiesa
                                             KTH Royal Institute of Technology           KTH Royal Institute of Technology          KTH Royal Institute of Technology

                                           Abstract—Despite the vast body of research literature propos-      and long, covering several pages of an article or book. The
                                        ing algorithms with formal guarantees, the amount of verifiable       complexity of the structure of the proof and properties of data
                                        code in today’s systems remains minimal. This discrepancy stems       types quickly escalates, making it difficult for humans to grasp
                                        from the inherent difficulty of verifying code, particularly due to
                                        the time-consuming nature and strict formalism of proof details       the complexity. Existing solutions that try to automate formal
arXiv:2501.05252v1 [cs.SE] 9 Jan 2025




                                        that formal verification tools require. However, the emergence of     verification have significant limitations, such as the inability
                                        transformers in Large Language Models presents a promising            to read text and scale to simple proofs or code bases [6].
                                        solution to this challenge. In this position paper, we believe that
                                        transformers have the potential to read research papers that          Transformers to the rescue? Transformers are a type of neu-
                                        propose algorithms with formal proofs and translate these proofs      ral network architecture designed to quickly process and gen-
                                        into verifiable code. We leverage transformers to first build a       erate sequences (e.g., text) [7], excelling at understanding and
                                        formal structure of the proof using the original text from the        manipulating human language, which makes them well-suited
                                        paper, and then to handle the tedious, low-level aspects of proofs    for tasks like translating textual descriptions into code [8].
                                        that are often omitted by humans. We argue that this approach
                                        can significantly reduce the barrier to formal verification. The      Tools like OpenAI’s Codex [9] and GitHub Copilot [10]
                                        above idea of reading papers to write verifiable code opens new       leverage these models to suggest code — with some levels
                                        avenues for automating the verification of complex systems, en-       of accuracy — but they do not perform formal verification
                                        abling a future where formally verified algorithms from academic      of the produced code, leaving correctness not guaranteed. As
                                        research can more seamlessly transition into real-world software      our experiments further reveal, naively applying a transformer-
                                        systems, thereby improving code reliability and security.
                                                                                                              based LLM to the formal verification problem fails to produce
                                                               I. I NTRODUCTION                               any verifiable proofs, due to the low-level complexities. Fur-
                                           Throughout history, humans have continually developed              thermore, even existing transformer-based systems for writing
                                        more sophisticated algorithms to solve complex problems,              verifiable code barely scale to simple programs that, for
                                        uncovering and forging connections between concepts in inno-          example, contain a single loop [11]–[13].
                                        vative and complex ways, and used this knowledge to build the         Our vision: from textual descriptions to verifiable code
                                        software that runs in modern-day systems. The culmination of          using transformers and separation of responsibilities. We
                                        all this research knowledge is captured in human language             argue that transformers are still a natural candidate for tackling
                                        and recorded in countless papers, books, or other written             the challenge of converting algorithms and proofs from human
                                        works. Despite this vast body of algorithmic knowledge, only          language into verification code. We, however, need to use them
                                        a negligible fraction of today’s code in systems has been             for the right task. Our key intuition is that we can break down
                                        formally verified using computers [1]. The reasons for this           the verification task into two main stages:
                                        lie in the inherent complexity and challenges involved in the         1) Translate a textual proof from human language to high-
                                        formal verification process [2].                                         level verification code. Transformers excel at translations
                                        Formal verification is time-consuming and complicated.                   that are roughly one-to-one (e.g., between spoken lan-
                                        This complexity arises from several factors. First, it requires          guages), making them well-suited for converting a textual
                                        familiarity with specialized formal languages, which have their          proof into a high-level skeleton of code for the verifier. At
                                        own syntax and semantics that require an enormous amount of              this stage, the goal is not to complete the entire proof but
                                        time to master adequately [3]. Second, the formal verification           to outline its structure, with many low-level details inten-
                                        process operates at an extremely low level; every step, even             tionally left out. The key insight here is that verifiers can
                                        those that are intuitively obvious to humans, must be explicitly         prove that the high-level proof works assuming (without
                                        verified — a tedious and often frustrating task [4]. Third,              proving) that the details of the low-level proofs are correct.
                                        verifiers attempt to aid this process by using heuristics to link        This allows us to use the best aspect of transformers for
                                        logical relationships, but the reliance on heuristics introduces         building the skeleton of the formal proof while deferring
                                        something known as brittleness [5]. Even a minor change,                 the detailed, low-level proofs to a second stage.
                                        like renaming a variable or removing seemingly irrelevant             2) Generate the missing low-level verifiable proofs. For the
                                        assertions, can cause previously verified proofs to fail. Finally,       second stage, we claim that transformers are still the right
                                        even if one could skip proving low-level lemmas, translating             tool. We use them to autonomously generate low-level
                                        proofs from human language into high-level verifiable code               proofs that lack textual equivalents, typically because their
                                        remains time-consuming. This is because proofs may be vague              solutions are intuitively obvious to humans. Our key ob-
    servation is that such low-level proofs do not require deep                           II. E XAMPLE : T HE HANDSHAKE LEMMA
    intellectual effort. Were they more complex, they would                       We explain the main challenges in writing verification code
    need explicit descriptions in text to ensure understanding                 using a simple network topological property that we derive
    from human readers. This observation allows us to leverage                 from graph theory [16]:
    the strengths of current transformers, which, while limited
    in complex reasoning [14], are perfectly suited for this                         P lemma. For every graph G = (V, E) we have
                                                                               Handshake
    type of task. Additionally, since many of these proofs                     2|E| = v∈V d(v), where d(v) is the degree of vertex v.
    exhibit recurring patterns, one can envision training or fine-                This lemma states that the sum of the degrees of all vertices
    tuning specialized, smaller transformers on these specific                 is equal to twice the number of edges in the graph. Even
    types of proofs. This pre-training enables the transformer                 without looking at the proof, a human immediately guesses
    to efficiently produce these necessary but straightforward                 the correctness of the statement with the following reasoning:
    verifications, streamlining and complementing the high-
    level formal verification from the previous stage.                         Human intuition. Each edge connects two vertices, increasing
                                                                               the overall sum of the degrees of all the graph vertices by two.
Challenges and a feasibility prototype. Beyond laying out                        This reasoning is generally enough to convince the reader
a vision, this paper explores the challenges associated with                   about the correctness of the lemma. Some books may provide
generating formal proof of correctness for both experts and                    some additional proof text as in the following example:
transformer-based LLMs. We discuss some of these challenges
through selective examples that are relevant for network                                   P Let X = {(e, x) P
                                                                               Book proof [16].              : e ∈ E, x ∈ V, x ∈ e}.
                                                                               Then |X| = v∈V d(v) and |X| = e∈E 2 = 2|E|.
system verification, whereas a comprehensive list would be
beyond the scope of this work. We provide hints that a                           This proof more formally defines human intuition using an
transformed-based LLM would be a suitable tool for producing                   auxiliary set X, which enumerates all the edge-vertex pairs of
a complete formal proof, limiting human intervention to only                   the graph. It then claims that the cardinality of this set (i.e.,
verifying the correctness of the formal specifications (not                    X) is equal to both (i) the sum of the degrees of the vertices,
the proofs). To support our position paper, we show how                        and (ii) the sum of the edges times two.
to verify three selected network topological properties using                    In this example, for the sake of simplicity, we only focus
a simple LLM-based prototype called P ROMETHEUS.1 Our                          on generating verification code (i.e., the proof), rather than the
prototype primarily focuses on network properties derived                      code of an algorithm. But, the principles behind P ROMETHEUS
from graph theory. 2 Specifically, through our analysis, we                    could be extended to enable joint generation of both algorithms
highlight how even a seemingly straightforward lemma, such                     and their corresponding proofs.
as the “handshake lemma” from graph theory, would require                      Why is it so hard to verify the lemma for a non-expert?
substantial verification efforts for those not specialized in the              Neither the human intuition nor the above book proof can be
field, but can be proved using our prototype. Our results show                 easily formally verified. Consider the more formal proof from
that P ROMETHEUS outperforms existing LLM-based verifiers                      the book. Even if we write the complete formal specification of
thanks to its ability in separating the proof verification into                the problem, including the property to be proved and a specifi-
a high-level and low-level verification synthesis process. We                  cation of a graph data structure, a verifier like DafnyP [17] will
focus on code verification and tools more widely used by                       not be able to verify these two assertions |X| = v∈V d(x)
developers (e.g., Dafny), thus we do not discuss related work                  and |X| = 2|E|. Indeed, formal verifiers operate without
on the pure math verification or other verifiers (e.g., [15]).                 understanding the semantics or meaning of the mathematical
                                                                               problem that they analyze. Instead, they apply a series of pre-
Impact. We believe our study has several far-reaching im-
                                                                               defined heuristics and logical techniques to check whether
plications. First, it opens the possibility of automatically
                                                                               a given post-condition or specification holds. These tools
verifying the correctness of decades of academic research,
                                                                               function purely at the syntactic level, using rules and strategies
an ambitious undertaking in itself. Second, by integrating our
                                                                               to attempt proofs, but without any intrinsic comprehension
system, researchers will have the ability to formalize proofs
                                                                               of the underlying, potentially trivial, mathematical concepts
in an easier way, with an automated transformer providing
                                                                               or their purpose. We showcasePthese limitations from formal
verification. This process would enhance transparency, al-
                                                                               verifiers using the |X(G)| = v∈V d(v) assertion from the
lowing both authors and reviewers to verify the correctness
                                                                               handshake lemma and use the Dafny verification system3 :
of claims more effectively. Third, based on the extensive
formal knowledge generated by our approach, we can envision                      1) Definitions are side-effect-free. Any definition of a prop-
developing systems that not only verify but also create novel                        erty expressed in Dafny must be described without using
algorithms with proofs.                                                              side-effect operations [19], i.e., the definition should not
                                                                                     modify the state of the involved variables in the definition.
                                                                                     Practically speaking, this constraint forbids a programmer
  1 Prometheus is a figure in Greek mythology who stole “fire” from the gods         from using “for” loops in the definition of properties. As
and gave it to humanity in the form of technology and knowledge.
  2 Our insights would apply to potentially different domains.                   3 We focus on the Dafny verifier as it is widely used in the industry [18].
                  P
   an example,      v∈V d(v) cannot be defined with a for               case, we are asking a question about the sizes of the
   loop. Dafny only allows programmers to use recursive                 sets that are actually the same but expressed differently.
   definitions to define properties and the recursive function          We need to help Dafny in proving this assertion by first
   cannot modify any state, only return values. The sum of              asking to check if the sets are identical, i.e., we must first
   the degrees of the vertices Sd would be defined as:                  prove {(e, x)|e ∈ (N (v) − {k}), x = v} + {k, v} ==
                                                                        {(e, x)|e ∈ N (v), x = v} so that the Dafny verifier uses
                  (
                    0                           if V = ∅,
       Sd (G) =                                                         its heuristics to prove this assertion and only then, it can
                    d(v) + Sd ((V \ {v}), E) else
                                                                        prove the cardinality one. This example illustrates the
   It is key to understand that verifiers reason in this                importance of allowing humans to add intermediate asser-
   “recursive space” and all proofs must align with these               tions to guide the solver and its heuristics toward correct
   definitions. As developers rarely rely on recursion to               lemma verification. Here, these guiding assertions relate
   develop code, this constraint represents a barrier for most          to extension equalities and assist Dafny in recognizing
   developers wishing to formally verify their code.                    that two objects are, in fact, identical.
2) Inductions are pervasive: the summation example. Since         Would an LLM help in proving the handshake lemma?
   most definitions are recursive, it is often required to        We answer this question by feeding the lemma statement and
   prove even simple properties using inductive proofs.           its textual proof from the book [16] to the Claude Sonnet 3.5
   Let’s consider the same example as above, i.e., |X| =
   P                                                              LLM and asking it to produce Dafny code. Most of the time,
      v∈V d(v) = Sd (G). To prove this property, we would         Claude will produce the following code:
   write a proof by induction on the set of vertices. In the
                                                                   1: lemma H ANDSHAKE L EMMA(g: Graph)
   inductive step, one needs to prove that adding a vertex
                                                                   2: requires I S VALID G RAPH(g)
   increases both the sum of degrees and |X| by d(v). While        3: ensures S UM O F D EGREES(g) == 2· |E|
   obvious, this inductive step is non-trivial to prove in a            {
   verifier as we discuss in the next step.                        4:       var V, E := g.V, g.E;
3) Inductions are pervasive: the set augmentation example.         5:       var X := set e, v | e in E & v in V & A DJ(e,v) :: (e, v);
                                                                   6:       assert |X|== S UM O F D EGREES(g);
   When we add a vertex in the above inductive step, its
                                                                   7:       assert |X|== 2· |E|;
   degree is defined as the sum of its adjacent edges, i.e.,            }
   d(v) = |N (v)|, where N (v) represents the neighbors of
   v and is defined as {e|e ∈ E, v ∈ e}. At the same time,           The translation of the proof is accurate as it covers every
   by the definition of X, vertex v contributes with elements     logical step, i.e., the definition of set X (where A DJ is an
   X(v) = {(e, x)|e ∈ N (v), x = v}. Clearly, the two sets        adjacency predicate) and the two assertions claiming |X| is
   have the same number of elements, i.e., |d(v)| == |X(v)|       equal to both the sum of degrees and twice the number of
   since both sets enumerate the edges adjacent at v, but         edges. Dafny cannot independently verify these two assertions.
   X(v) stores the edges as pairs always repeating v as           Yet, one main contribution of an LLM is that it can lay out
   the second element in the pair. For example, consider          the outline of a proof so that one only needs to focus on the
   a vertex v adjacent to edges e1 and e2 . We have that          low-level technical parts. LLMs are extremely efficient in this
   d(v) = |{e1 , e2 }| while |X(v)| = |{(e1 , v), (e2 , v)}|. A   type of translation from natural language to Dafny code as
   verifier like Dafny does not easily understand that the        they are almost one-to-one, a perfect task for transformers.
   cardinalities of the two sets are equivalent by the above         What it remains to do is writing the low-level proofs
   definitions. It requires another proof by induction over the   showing that the two assertions hold. This is where an LLM
   sets of edges in N (v) and X(v), showing that adding an        needs to find its own ways of proving sub lemmas. We
   edge preserves |N (v)| = |X(v)|. Even if we write this         argue that these low-level lemmas do not require complex
   induction, a human still needs to address another low-         intellectual reasoning, which would otherwise be expressed
   level challenge, which we discuss next.                        in human language for the reader to trust the proof. Instead,
4) Extension equalities. Following our example, we now            these low-level lemmas often require dealing with the low-
   must prove |N (v)| = |X(v)| by induction, i.e., we prove       level time-consuming details of the Dafny language and how
   |N (v)| = |{(e, x)|e ∈ N (v), x = v}|. We do not cover         data structures are expressed. We show in the next section how
   the base case. In the inductive step, we remove any            a simple LLM-based prototype manages to write Dafny code
   edge k from N (v). By inductive hypothesis we have             to also verify the low-level aspects of a proof.
   |N (v) − {k}| = |{(e, x)|e ∈ (N (v) − {k}), x = v}|.
                                                                             III. F EASIBILITY S TUDY WITH A P ROTOTYPE
   Dafny easily understands that removing an edge from
   N (v) results in reducing its cardinality by one. However,        We perform a preliminary evaluation of our idea to assess
   Dafny cannot automatically understand the same for             the potential feasibility of the idea, leaving a full-scale eval-
   X(v). Asking Dafny to prove that |{(e, x)|e ∈ (N (v) −         uation as future work. Our prototype feeds a proof in natural
   {k}), x = v} + {k, v}| == |{(e, x)|e ∈ N (v), x = v}|          language as input to the Claude Sonnet 3.5 LLM. It then
   will fail. The reason is subtle. Dafny relies on some          interacts iteratively with the LLM by proving lemmas using a
   heuristics to find out how to prove assertions. In this        top-down approach, i.e., first prove the general lemma using
some lower-level helper lemmas that will be proved in the next    mismatch between the level of detail required by a formal
iterations. The system also verifies the code generated by the    verifier and a textual proof. In P ROMETHEUS, we try to fill this
LLM, and sends both the output of the verification process        gap in two ways: either having an LLM generating the missing
alongside some hints on how to solve these problems. These        logic or letting verifiers generate a proof using heuristics. In
hints are high-level hints to help the LLM in solving common      both cases, neither LLMs nor verifiers possess the same level
Dafny problems, i.e., proving using inductions, solving exten-    of “intelligence” that humans possess in order to understand
sion equality problems, spotting missing pre-conditions, and      relations between concepts, e.g., impact of an edge on the sum
more. We test P ROMETHEUS on three lemmas:                        of degrees of the vertices. Exploring novel ways to generate
• Handshake lemma (definition in §II).                            proofs (as in the AlphaProof or Alpha Geometry 2 systems)
• Degree bounds lemma. Given a graph G, we have that              using transformers and reinforcement learning is left outside
   min(G) ≤ avg(G) ≤ max(G), where min(G), avg(G),                the scope of this paper, which only deals with translating the
   and max(G) are the minimum, average, and maximum               existing human knowledge into verifiable code.
   degree of the vertices in G.
                                                                                          C ONCLUSIONS
• Even cycle bipartite lemma. Given a bipartite graph G =
                                                                     In this position paper, we argue that recent advancements
   ((A, B), E), we have that every cycle has an even length,
                                                                  in LLMs present unprecedented opportunities for translating
   where A and B are two partitions of the vertices such that
                                                                  decades of scientific research on algorithms and systems into
   there are no edges connecting two vertices in the same
                                                                  formally verifiable code. We propose leveraging LLMs to
   partition.
                                                                  generate high-level code outlines and corresponding verifica-
   For each lemma, we input all the formal specifications of      tion logic from natural language descriptions in the literature.
all the relevant definitions, such as the graph data structure    This approach aims to lower the barrier to verifying scientific
or the definition of a cycle. To evaluate the performance of      research and enable the creation of more resilient software
P ROMETHEUS, we use zero-shot prompting as a baseline,            systems. Significant research challenges remain, including
requesting that LLMs generate the complete proof in a single      developing systems capable of accurately translating complex
attempt. We compare the success rate of P ROMETHEUS to the        notations, algorithms, and logic, as well as innovating stronger
baseline as the number of successful runs over the total runs.    methods for verifying the low-level aspects of these proofs.
The following table presents the results for the three lemmas,
including the success rate over five runs:                                               ACKNOWLEDGMENTS
                     Handshake   Degree Bounds   Bipartite           We would like to thank the anonymous reviewers for their
        Baseline        0/5           0/5           0/5           insightful comments and suggestions on this paper. This work
     P ROMETHEUS        4/5           3/5           3/5
                                                                  has been partially supported by Vinnova (the Sweden’s In-
   We observe that with basic prompting strategies like zero-     novation Agency), the Swedish Research Council (agreement
shot prompting, the baseline fails to produce verifiable code.    No. 2021-04212), and KTH Digital Futures.
The generated code is always short and lacks low-level proofs
                                                                                              R EFERENCES
mentioned in §II. In contrast, P ROMETHEUS successfully
generates a complete and verifiable proof in Dafny, with a         [1] F. Wiedijk, “Formal proof–getting started,” 2008.
                                                                   [2] R. P. Kurshan, “The complexity of verification,” in STOC ’94.
high success rate. P ROMETHEUS always starts with a proof          [3] “Opinions on Proof Assistants,” Link to the article, 2024.
skeleton, delves into the low-level details, and refines them      [4] H. Geuvers, “Proof assistants: History, ideas and future,” Sadhana,
iteratively. View a video of a successful run [20]. The result         vol. 34, pp. 3–25, 2009.
                                                                   [5] A. Tomb and J. Tristan, “Avoiding verification brittleness in Dafny,”
shows that P ROMETHEUS delivers a promising performance                https://dafny.org/blog/2023/12/01/avoiding-verification-brittleness/.
in verifiable code generation in Dafny.                            [6] S. Chatzikyriakidis and Z. Luo, “Proof assistants for natural language
                                                                       semantics,” in LACL’16, M. Amblard, P. de Groote et al., Eds.
       IV. F UTURE C HALLENGES AND D ISCUSSION                     [7] A. Vaswani, N. Shazeer et al., “Attention is all you need,” in NeurIPS’17.
                                                                   [8] M. Nejjar, L. Zacharias et al., “Llms for science: Usage for code
Who verifies the correctness of the input formal specifica-            generation and data analysis,” ArXiv, vol. abs/2311.16733, 2023.
tions? In our evaluation, all formal specifications—including      [9] M. Chen, J. Tworek et al., “Evaluating large language models trained
data structure and predicate definitions (e.g., how a graph            on code,” 2021. [Online]. Available: https://arxiv.org/abs/2107.03374
                                                                  [10] “Microsoft copilot,” 2024. [Online]. Available: copilot.microsoft.com
or the sum of node degrees is defined) as well as pre- and        [11] C. Sun, Y. Sheng et al., “Clover: Closed-loop verifiable code generation,”
post-conditions of the proven property—were generated using            in SAIV’24.
an LLM. However, we manually verified the correctness of          [12] M. R. H. Misu, C. V. Lopes et al., “Towards AI-assisted synthesis of
                                                                       verified Dafny methods,” in FSE’24.
these definitions before using them as input for P ROMETHEUS.     [13] E. Mugnier, E. A. Gonzalez et al., “Laurel: Generating dafny assertions
Completely automating this task is challenging, as it forms the        using large language models,” arXiv preprint arXiv:2405.16792, 2024.
foundational truth that guides the LLM in generating accurate     [14] Z. Li, Y. Cao et al., “Llms for relational reasoning: How far are we?”
                                                                       in LLM4Code ’24.
code. Further research on how to more reliably generate formal    [15] A. Q. Jiang, S. Welleck et al., “Draft, sketch, and prove: Guiding formal
specifications from natural language is needed.                        theorem provers with informal proofs,” in ICLR’23.
                                                                  [16] D. H. Mónika Csikós and T. Ueckerdt, “Graph Theory,”
How far can we go in proving theorems without a textual                https://www.math.kit.edu/iag6/lehre/graphtheory2019w/media/main short.pdf,
proof? As we discussed in this paper, there is always a                2019.
[17] K. R. M. Leino, “ Accessible Software Verification with Dafny ,” IEEE
     Software, vol. 34, no. 06, pp. 94–97, Nov. 2017. [Online]. Available:
     https://doi.ieeecomputersociety.org/10.1109/MS.2017.4121212
[18] M. Hicks, “How we built cedar with automated reasoning and differen-
     tial testing,” Link to the article, 2024.
[19] “Dafny Reference Manual,” https://dafny.org/dafny/DafnyRef/DafnyRef.html,
     2024.
[20] “Prometheus system demonstration video.” [Online]. Available:
     https://youtu.be/hw9423RrZZo
