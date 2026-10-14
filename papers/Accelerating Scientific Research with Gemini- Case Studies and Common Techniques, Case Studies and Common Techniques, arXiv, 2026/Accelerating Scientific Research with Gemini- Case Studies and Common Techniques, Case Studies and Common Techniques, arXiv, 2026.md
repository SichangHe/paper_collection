                                                          Accelerating Scientific Research with Gemini:
                                                             Case Studies and Common Techniques
                                          David P. Woodruff*, †, ‡1,2 , Vincent Cohen-Addad†, ‡1 , Lalit Jain‡1 , Jieming Mao‡1 , Song
                                        Zuo†, ‡1 , MohammadHossein Bateni†1 , Simina Brânzei†3,1 , Michael P. Brenner†1,5 , Lin Chen†1 ,
                                        Ying Feng†6 , Lance Fortnow†7 , Gang Fu†1 , Ziyi Guan†13 , Zahra Hadizadeh†10 , Mohammad T.
                                           Hajiaghayi†1,14 , Mahdi JafariRaviz†14 , Adel Javanmard†1,4 , Karthik C. S.†8 , Ken-ichi
                                           Kawarabayashi†12 , Ravi Kumar†1 , Silvio Lattanzi†1 , Euiwoong Lee†9 , Yi Li†15 , Ioannis
arXiv:2602.03837v3 [cs.CL] 6 Mar 2026




                                          Panageas†10 , Dimitris Paparas†1 , Benjamin Przybocki†2 , Bernardo Subercaseaux†2 , Ola
                                        Svensson†13 , Shayan Taherijam†10 , Xuan Wu†15 , Eylon Yogev †16 , Morteza Zadimoghaddam†1 ,
                                                  Samson Zhou†11 , Yossi Matias1 , James Manyika1 , and Vahab Mirrokni*, †, ‡1
                                                                                        1
                                                                                          Google Research
                                                                                 2
                                                                                 Carnegie Mellon University
                                                                                       3
                                                                                         Purdue University
                                                                          4
                                                                            University of Southern California
                                                                                       5
                                                                                         Harvard University
                                                                                               6
                                                                                                 MIT
                                                                             7
                                                                               Illinois Institute of Technology
                                                                                       8
                                                                                         Rutgers University
                                                                                    9
                                                                                      University of Michigan
                                                                            10
                                                                               University of California, Irvine
                                                                                   11
                                                                                      Texas A&M University
                                                    12
                                                       National Institute of Informatics, Tokyo and The University of Tokyo
                                                                                              13
                                                                                                 EPFL
                                                                      14
                                                                         University of Maryland, College Park
                                                                         15
                                                                            Nanyang Technological University
                                                                                      16
                                                                                         Bar-Ilan University

                                                                                              Abstract
                                                   Recent advances in large language models (LLMs) have opened new avenues for accelerating
                                               scientific research. While models are increasingly capable of assisting with routine tasks, their
                                               ability to contribute to novel, expert-level mathematical discovery is less understood. We present
                                               a collection of case studies demonstrating how researchers have successfully collaborated with
                                               advanced AI models, specifically Google’s Gemini-based models (in particular Gemini Deep
                                               Think and its advanced variants), to solve open problems, refute conjectures, and generate
                                               new proofs across diverse areas in theoretical computer science, as well as other areas such as
                                               economics, optimization, and physics. Based on these experiences, we extract common techniques
                                               for effective human-AI collaboration in theoretical research, such as iterative refinement, problem
                                               decomposition, and cross-disciplinary knowledge transfer. While the majority of our results stem
                                           *
                                             Corresponding authors: woodruffd@google.com, mirrokni@google.com
                                           †
                                             Individual section contributor. Authors of individual sections are only responsible for correctness of their section.
                                           ‡
                                             Contributed to advanced variants of Google models used in this paper.



                                                                                                   1
     from this interactive, conversational methodology, we also highlight specific instances that push
     beyond standard chat interfaces. These include deploying the model as a rigorous adversarial
     reviewer to detect subtle flaws in existing proofs, and embedding it within a "neuro-symbolic"
     loop that autonomously writes and executes code to verify complex derivations. Together, these
     examples highlight the potential of AI not just as a tool for automation, but as a versatile,
     genuine partner in the creative process of scientific discovery.


Contents
1 Introduction                                                                                           4
  1.1 Model Description . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        5
  1.2 Related Work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       5

2 Techniques for AI-Assisted Research                                                                     8
  2.1 Iterative Prompting and Refinement . . . . . . . . . . . . . . . . . . . . . . . . . . .            8
  2.2 Cross-Pollination of Ideas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        8
  2.3 Simulation and Counterexample Search . . . . . . . . . . . . . . . . . . . . . . . . . .            8
  2.4 Formalization and Rigor Checks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          9
  2.5 Interactive Proof Construction with External Validation . . . . . . . . . . . . . . . .             9
  2.6 Agentic Tool-Use and Automated Feedback . . . . . . . . . . . . . . . . . . . . . . .              10
  2.7 Human-AI Collaboration Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . .            10
  2.8 Summary: The AI-Assisted Research Playbook . . . . . . . . . . . . . . . . . . . . .               11

3 Deep Technical Review and Counterexamples                                                   11
  3.1 Online Algorithms: Submodular Welfare . . . . . . . . . . . . . . . . . . . . . . . . . 11
  3.2 Cryptography: AI-Assisted Bug Detection in SNARGs . . . . . . . . . . . . . . . . . 17

4 Cross-Pollination of Ideas                                                                  20
  4.1 Approximation Algorithms: Max-Cut . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
  4.2 Computational Geometry: Steiner Trees . . . . . . . . . . . . . . . . . . . . . . . . . 28
  4.3 Graph Theory: Computing Perfect Matchings in Regular Bipartite Graphs . . . . . . 32

5 Using an AI-integrated IDE to “vibe-code”                                                        41
  5.1 Search vs. Decision in S2P . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41

6 Autonomous Verification and Neuro-Symbolic Loops                                               47
  6.1 Physics: Cosmic String Spectra . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 47

7 Algorithms and Bounds                                                                           52
  7.1 Graph Theory: Biclique Partitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
  7.2 Query Complexity: Local Search on General Graphs . . . . . . . . . . . . . . . . . . 56
  7.3 Robust Coresets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65
  7.4 Submodular Function Maximization in a Stream . . . . . . . . . . . . . . . . . . . . 70
  7.5 Streaming Algorithms: Entropy, Low Rank Approximation, and Chamfer Distance . 83
      7.5.1 Internal State Changes for Streaming Entropy . . . . . . . . . . . . . . . . . . 84
      7.5.2 Consistent Low-Rank Approximation . . . . . . . . . . . . . . . . . . . . . . . 86
      7.5.3 Global Efficient Encoding for Low-Rank Approximation . . . . . . . . . . . . 88
      7.5.4 Even Faster Algorithm for the Chamfer Distance . . . . . . . . . . . . . . . . 92



                                                    2
8 Resolving Conjectures and Complex Derivations                                              97
  8.1 Information Theory: The Courtade-Kumar Conjecture . . . . . . . . . . . . . . . . . 97
      8.1.1 Part I: Generalization to Unbalanced Functions . . . . . . . . . . . . . . . . . 97
      8.1.2 Part II: The Unsymmetrized Conjecture and the Li-Médard’s Conjecture . . . 111
  8.2 NP-hardness: Ratio Difference Maximization (RDM) . . . . . . . . . . . . . . . . . . 120
  8.3 Machine Learning Optimization: Self-regularized Gumbel Sigmoid . . . . . . . . . . 125
  8.4 Mechanism Design: Revelation Principle Reduction Domain Extension . . . . . . . . 130
  8.5 Networked Information Aggregation for Binary Classification . . . . . . . . . . . . . 140

9 Conclusion and Future Directions                                                                 146
  9.1 Common Themes and Problem Suitability . . . . . . . . . . . . . . . . . . . . . . . . 146
  9.2 Understanding Current Limitations and Failure Modes . . . . . . . . . . . . . . . . . 147
  9.3 Future Directions: From Code Execution to Formal Verification . . . . . . . . . . . . 147
  9.4 The Shifting Bottleneck: An Impending Crisis in Peer Review . . . . . . . . . . . . . 148
  9.5 Final Thoughts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 148




                                                  3
1     Introduction
The integration of artificial intelligence into the scientific workflow has traditionally focused on data
analysis, simulation, and routine automation. However, the emergence of frontier large language
models (LLMs) with enhanced reasoning capabilities suggests a shift towards AI systems that can
act as an effective research collaborator, and contribute to the core intellectual tasks of research:
formulating hypotheses, designing algorithms, developing novel techniques to tackle an open problem,
and proving theorems.
    This paper documents a series of independent experiments where researchers utilized advanced
AI models to tackle specific, often long-standing, open problems in their respective fields. The results
range from resolving conjectures in information theory and submodular maximization to deriving
exact analytical spectra for cosmic strings and improving bounds for graph algorithms.
    Key Contributions: Given the breadth of the fields and case studies covered, we highlight
three primary contributions of this paper:

    1. Demonstrating the power of hybrid models: We show the potential of a hybrid human-AI
       model in tackling real, highly complex open problems across a diverse set of scientific and
       mathematical domains.

    2. Advancing state-of-the-art science: We make concrete, notable contributions to real
       problems in science, yielding novel results such as resolving conjectures, improving algorithmic
       bounds, and identifying critical flaws in literature.

    3. Showcasing the future of scientific discovery: We illustrate what the future of research
       looks like in practice. By detailing novel workflows, human-AI collaboration techniques, and
       interactive problem-solving strategies, we highlight the real implications for how science is
       likely to be conducted in the coming years.

    Crucially, these are not hypothetical scenarios but real-world instances where AI played a
pivotal role in advancing state-of-the-art research. By analyzing these diverse case studies, we
identify recurring patterns and effective strategies for leveraging AI in such theoretical research. The
significance of these results is the generality of these techniques and existence of common recipes
that can be applied by probing publicly available Gemini models. These include:

    • Agentic Execution Loops: Moving beyond manual chat interfaces, models can be embedded
      in automated “neuro-symbolic" pipelines. In these setups, the AI proposes a mathematical
      solution, writes code to numerically verify it, and automatically ingests execution errors (e.g.,
      Python tracebacks) to self-correct and autonomously prune invalid mathematical branches
      (see Section 6.1).

    • Deep Technical Review and Bug Detection: Beyond constructive tasks, AI models
      can act as adversarial reviewers. We present a case where an LLM, guided by an iterative
      self-correction protocol, identified a fatal flaw in a recent cryptography preprint claiming a
      major breakthrough (SNARGs from LWE) [53], a subtle inconsistency between a definition
      and a construction that had escaped initial human review.

    • Deep Literature Synthesis and Connection: AI models can identify obscure connections
      between disparate fields (e.g., linking Steiner trees to the Kirszbraun Extension Theorem) that
      human experts might overlook.



                                                   4
   • Counterexample Generation: Models are adept at constructing counterexamples to refute
     plausible conjectures, saving researchers from pursuing dead ends.

   • Algorithmic Insight and Optimization: In algorithmic research, AI can propose novel
     data structures or analysis techniques (e.g., adapting quadtrees for different norms) to improve
     time complexity bounds.

   • Automated Proof Generation and Verification: For well-defined subproblems, AI can
     generate rigorous proofs, sometimes requiring minimal human intervention, or verify complex
     manual derivations.

   • Interactive Refinement: A recurring theme is the iterative "conversation" where the
     researcher guides the model, correcting errors and refining the problem statement, which often
     leads to the final solution.

   • Theoretical Justification of Heuristics: AI models can bridge the gap between empirical
     success and theory by deriving rigorous justifications for heuristic methods, such as characteriz-
     ing the implicit regularization induced by specific architectural choices like the Self-regularized
     Gumbel Sigmoid.

1.1   Model Description
Unless otherwise specified in the testimonials, the model used in this work is a Google-internal
advanced version of Gemini Deep Think [74] – an enhanced reasoning model for complex problems
that incorporates some of our latest research techniques, including parallel thinking, i.e., exploring
multiple proof branches simultaneously. Similar models were also used recently in the International
Mathematics Olympiad, achieving gold-medal standard performance [74]. This setup enables the
model to simultaneously explore and combine multiple possible solutions before giving a final answer,
rather than pursuing a single, linear chain of thought. This approach aligns with prior research
demonstrating the efficacy of tree-based search methods in mathematical reasoning [45].
    To make the most of the reasoning capabilities of Deep Think, we additionally trained this
version of Gemini on novel reinforcement learning techniques that can leverage more multi-step
reasoning, problem-solving and theorem-proving data. We also provided Gemini with access to a
curated corpus of high-quality solutions to mathematics problems [74]. We also added a long linear
chain of interactive verification calls at the output to increase reasoning depth and provide a lot of
iterative verification, which was augmented by human expert verification.

1.2   Related Work
Recent advances in Large Language Models (LLMs) have spurred significant interest in their potential
to accelerate scientific discovery. Several concurrent works explore the capabilities of AI in assisting
mathematical and theoretical research. Here, we situate our contributions in the context of two
particularly relevant studies: OpenAI’s investigation into GPT-5’s scientific capabilities [17] and the
work of Nagda et al. on using AlphaEvolve for hardness of approximation [77].

Comparison with OpenAI’s GPT-5 Experiments. Concurrent work by OpenAI [17] doc-
uments a series of case studies demonstrating GPT-5’s ability to contribute to research in fields
ranging from biology and physics to mathematics. While both our work and theirs highlight the
potential of frontier models as research assistants, there are differences in scope and focus. Our work
places a heavier emphasis on Theoretical Computer Science (TCS), covering a wide array of subfields

                                                   5
Figure 1: Overview of the reasoning architecture used in many testimonials: an extensive exploration
of the solution space combined with deep reasoning and a long tail of automated and human
verification and in several cases, guidance and iterative feedback.




                                                 6
including algorithmic game theory, approximation algorithms, complexity theory, cryptography,
graph theory, information theory, optimization, online algorithms, streaming algorithms, and query
complexity.
    Furthermore, recent activity on the Erdős Problem database has showcased the growing role of
AI in resolving open mathematical conjectures. Notably, Erdős Problem #728, concerning factorial
divisibility, was solved autonomously by an AI system (Aristotle), with GPT-5 playing a crucial
role in generating the proof strategy and subsequent expositions [17]. This achievement, verified by
Terence Tao and the broader community, underscores the capacity of these models not only to solve
problems but also to rapidly iterate on and improve mathematical writing. Other problems, such as
#729, #401, #205, #333, #281, and #460 have also seen AI-assisted progress or full resolutions,
further validating the trend of AI-accelerated mathematical discovery. Our work complements
these findings by providing a detailed methodology and a broader set of examples across TCS,
demonstrating that these capabilities are not isolated incidents but part of a larger shift in research
practices.

Comparison with AlphaEvolve for Hardness of Approximation. Nagda, Raghavan, and
Thakurta [77] present significant results in hardness of approximation for MAX-CUT, MAX-k-CUT,
and TSP. Their primary methodology relies on AlphaEvolve [79], a specialized evolutionary algorithm
that uses an LLM as a mutation operator to search for combinatorial structures (gadgets) that
optimize a specific objective function (inapproximability ratios).
    In contrast, our work focuses on the utility of general-purpose LLMs (specifically Gemini and its
reasoning-enhanced variants like Deep Think) as conversational research partners. While AlphaEvolve
is a powerful tool for search problems where a clear objective function exists (e.g., finding a gadget
with specific properties), our case studies demonstrate that general-purpose models can be effective
across a broader range of intellectual tasks where the "objective" is less well-defined, such as
generating a proof idea, identifying a relevant theorem from a different field, or interactively refining
a definition.
    For instance, our derivation of the analytical spectrum for cosmic strings (Section 6.1) involved a
tree-search over derivation strategies and mathematical concepts, rather than a direct optimization
of a numerical value. Similarly, the resolution of the "Simplex is the Best for Graph Embeddings"
conjecture (Section 4.2) relied on conceptual bridging (linking Steiner trees to Lipschitz extensions)
rather than combinatorial search. Thus, our work complements [77] by showing that standard
frontier models, without specialized evolutionary wrappers, can drive progress in theoretical research
through dialogue and reasoning.

Concurrent Work. A recent work [49] does mathematical discovery at scale using AI-assisted
methodologies. Our work aligns with it in demonstrating the potential of AI as a collaborative
partner in theoretical research, but we offer a distinct set of case studies and a focus on specific TCS
domains. Additionally, we note independent works [90, 92] that further contribute to the growing
body of literature on AI in mathematics and science.
   In concurrent and independent work of Feng et al. [37, 38], they study similar Gemini-based
models using similar techniques, though their focus is on pure math problems whereas ours is mostly
on other disciplines, such as many areas of theoretical computer science, as well as economics and
physics.

Roadmap The remainder of this paper is organized as follows. Section 2 synthesizes the common
techniques and methodologies derived from these case studies. The sections after that give detailed


                                                   7
and extensive testimonials from each collaboration, roughly categorized by the main role of the AI in
the collaboration. Finally, Section 2.8 discusses the broader implications for the future of theoretical
research.


2     Techniques for AI-Assisted Research
Across the various successful collaborations documented here, several common techniques emerged.
These strategies represent a "playbook" for researchers looking to integrate AI into their theoretical
work.

2.1    Iterative Prompting and Refinement
Rarely does a model solve a deep open problem in a single shot. Success often comes from an
iterative dialogue.

    • Initial Broad Query: Start by asking the model to digest a relevant paper or problem
      statement to gauge its understanding.

    • Specific Sub-tasks: Break down the main problem into smaller, verifiable lemmas or
      calculations.

    • Error Correction: When the model makes a mistake (e.g., a wrong constant or invalid
      assumption), pointing it out specifically often leads to a correct and sometimes more elegant
      solution in the next turn.

    • Scaffolding: Providing the model with a high-level proof strategy or "scaffold" allows it to
      fill in the technical details effectively.

    • Adversarial Self-Correction for Review: When tasked with reviewing complex proofs,
      standard prompts often yield superficial results. A rigorous protocol instructing the model to
      (1) generate an initial review, (2) critique its own findings for hallucinations, and (3) iteratively
      refine the logic, enables deep technical critique. This was critical in identifying the flaw in the
      SNARGs paper (Section 3.2), where the model distinguished between a definition of perfect
      consistency and a construction of statistical consistency.

2.2    Cross-Pollination of Ideas
Models have ingested vast amounts of literature across all fields. They excel at:

    • Finding Analogies: Identifying similar problems in different domains (e.g., applying tech-
      niques from computational geometry to graph theory).

    • Retrieving obscure theorems: Bringing relevant but less-known theorems to the researcher’s
      attention (e.g., Stone-Weierstrass or Kirszbraun Extension Theorem) to bridge gaps in a proof.


2.3    Simulation and Counterexample Search
For conjectures, models can be tasked to:

    • Construct Counterexamples: Generating specific instances (graphs, matrices, set systems)
      that violate a proposed conjecture.

                                                    8
                                                           (b) From Graph Embeddings to Hilbert
(a) From Discrete Combinatorics to Con-                    Space Geometry: To resolve the "Simplex is
tinuous Measure Theory: To resolve an open                 Best" conjecture for Euclidean Steiner Trees, the
question about bounded-rank SDP solutions for              AI constructed a mapping from the Euclidean em-
Max-Cut, the AI reframed a discrete combinato-             bedding of an arbitrary graph (orange network,
rial problem involving unit vectors into an energy         left) to the embedding of a star graph, which
minimization problem over continuous probabil-             forms a regular geometric simplex (green tetra-
ity measures on the unit sphere (S d−1 , illustrated       hedron, right). By recognizing this as a distance-
above). This cross-pollination allowed the AI to           compressing (1-Lipschitz) map, the AI realized
bypass traditional approximation tool-kits and in-         it could apply the obscure Kirszbraun Extension
stead apply the Stone-Weierstrass Theorem from             Theorem to formally guarantee that transform-
geometric functional analysis to establish the nec-        ing the graph into a simplex never increases the
essary variance bounds. See Section 4.1.                   Steiner tree cost. See Section 4.2.

Figure 2: Visualizing Cross-Pollination: The AI model successfully resolved open problems by
reframing them in entirely different mathematical domains, bringing advanced topological and
geometric theorems to bear on algorithmic and combinatorial problems.


    • Verify Small Cases: Writing code to computationally verify a conjecture for small n,
      providing empirical evidence before attempting a general proof.

2.4    Formalization and Rigor Checks
While models can hallucinate, they are increasingly capable of formal reasoning when prompted
correctly.

    • Proof Sketch to Formal Proof: Asking the model to expand a high-level sketch into a
      rigorous LATEX proof.

    • Sanity Checking: Using the model to check consistent usage of notation or to verify that all
      conditions of a theorem are met.

    • Mathematical Derivation: Researchers can offload the mechanical heavy lifting of complex
      derivations to the model, such as simplifying expressions, computing limits, or solving integrals,
      allowing them to focus on the high-level logic.

2.5    Interactive Proof Construction with External Validation
A powerful technique involves using the model to identify necessary external theorems and then
validating those theorems with external sources.

    • Identifying Dependencies: Asking the model to list all external theorems required for a
      proof.

                                                       9
   • External Verification: The researcher finds the formal statements of these theorems (e.g.,
     via Google Search or textbooks) and feeds them back to the model.

   • Self-Contained Proof Generation: The model then incorporates these verified statements
     to generate a rigorous, self-contained proof.

2.6   Agentic Tool-Use and Automated Feedback
While most of the collaborations documented here rely on manual, iterative dialogue, frontier models
can also be deployed as agents within automated programmatic loops. For problems requiring heavy
algebraic manipulation or where symbolic math must be rigorously grounded in numerical reality
(e.g., the physics case study in Section 6.4), researchers can construct a “neuro-symbolic" pipeline
consisting of the following steps:

   • Symbolic Proposal: The LLM generates a mathematical hypothesis or intermediate expres-
     sion.

   • Code Generation: The LLM autonomously writes an executable script (e.g., in Python) to
     evaluate its proposed math against a known numerical baseline.

   • Automated Feedback: The system executes the code. If the code fails, hits a runtime error,
     or reveals numerical instability (such as catastrophic cancellation), the automated harness
     captures the exact execution traceback and injects it back into the LLM’s context window.

This programmatic loop allows the AI to systematically explore a tree of mathematical solutions,
autonomously pruning dead-ends and self-correcting its algebra without requiring a human-in-the-loop
for every intermediate step.

2.7   Human-AI Collaboration Dynamics
It is important to note that AI models like Gemini function best as powerful collaborators rather
than autonomous researchers. In the successful case studies presented here, the partnership between
the model and the human expert was key to the results.

   • Selection and Refinement: Models are capable of generating a high volume of diverse
     mathematical statements. Human expertise is valuable for filtering these outputs and identifying
     the most promising directions for further investigation.

   • Iterative Guidance: While models can solve some problems in a single shot, tackling deep
     open problems is often most successful through an iterative process. The researcher guides the
     model, refining the problem statement and narrowing the focus to achieve the desired result.

   • Standard Verification: As with any research collaboration, the AI can make mistakes,
     and AI-generated proofs and counterexamples benefit from rigorous verification. The model
     serves as an excellent accelerator for ideation and drafting, while the researcher validates the
     mathematical correctness.

   • Optimizing Context: Performance is often optimized by providing clear, self-contained
     definitions, particularly when using highly specialized notation that may deviate from standard
     literature.



                                                 10
    • Leveraging Literature: We found that incorporating relevant papers directly into the context
      significantly enhanced the model’s ability to construct correct proofs for specialized domains.

    • Context De-Identification: The model sometimes avoids non-trivial machinery (for example,
      the Kirszbraun extension theorem as in Section 4.2), treating such proofs as non-elementary, or
      it may do so because the prompt steers it toward conservatism to avoid hallucinations, causing
      it to abandon an otherwise viable approach. Separately, on occasion, when shown the paper as
      context in the prompt, it recognizes the statement to prove as a conjecture in the paper and
      refuses to attempt it on the grounds that it is an open problem. One way to bypass both issues
      is via context de-identification (remove the paper and provide only the problem statement
      and definitions), after which the model typically engages (and, in cases like Section 4.2, may
      ultimately draw on deeper results to resolve a conjecture).

    We view the AI as a tireless, knowledgeable, and creative bright junior collaborator. Its value lies
in its ability to synthesize vast amounts of information and generate novel hypotheses that human
researchers can then validate and build upon.

2.8    Summary: The AI-Assisted Research Playbook
Taken together, the techniques outlined above represent a fundamental shift in how theoretical
research can be conducted. The LLM is no longer acting merely as a search engine or a syntax
formatter; it is functioning as a combinatorial reasoning engine and a sounding board for abstract
ideation.
    However, the most successful collaborations documented in the following case studies all share
a common denominator: strong human orchestration. Although several of our successes came
from a single “zero-shot" prompt, many required scaffolded reasoning, i.e., breaking down deep
open problems into verifiable parts, testing hypotheses through adversarial prompting, and actively
steering the model. Informally this interactive workflow has been called “vibe-proving".
    By mastering the techniques outlined above—particularly iterative refinement and adversarial
self-correction—researchers can effectively elevate the AI from a passive tool into an active, high-
leverage research partner. The following sections document these dynamics in practice across a wide
array of disciplines.

Color-coding: In the remainder of the paper, chat interactions are presented using a light,
color-coded design. When present, the overall chat box uses a sand-colored background to group
messages within a conversation. In cases where only a single message appears—such as an isolated
user message or an isolated AI response—the surrounding chat box may be omitted, and only the
message styling is shown. Messages authored by the user are displayed on a light blue background
and AI-generated messages are shown on a light red background.


3     Deep Technical Review and Counterexamples
In this section, we see how AI can act as a critical adversary, finding subtle bugs in human proofs,
refuting plausible hypotheses, and hunting for counterexamples.

3.1    Online Algorithms: Submodular Welfare
Written by Morteza Zadimoghaddam and Vahab Mirrokni.


                                                  11
Problem Context
In online submodular welfare maximization, the Greedy algorithm achieves a competitive ratio of
0.5. A conjecture by Korula et al. (2015) suggested that the gain from "copying" an item to the end
of the stream is bounded by the gain of "moving" it. Proving this would imply a competitive ratio
of 0.567.

AI Contribution
    The researcher provided the research paper that included the formal definitions as well as a
conjecture statement, and tasked the model zero-shot with just identifying any open question in the
paper and solving it. Throughout this paper we add a prompt that asks the model to be rigorous in
its mathematical proofs and to thoroughly check its answers - we do not specify the details of this
prompt.

   Please try to improve the paper by identifying and solving an open question from it.

   <Math rigor prompt>



    Remarkably, the model chose the following counterexample and refuted it autonomously. The
subsequent verification calculations were also generated by the model without extra interaction
or supervision. This demonstrates its ability to construct valid, non-trivial instances that violate
human-proposed conjectures. The human researchers defined the initial search parameters and
independently verified the model’s arithmetic.

   • Refutation Strategy: The model independently selected the minimal non-trivial dimensions
     (n = 3 items, m = 2 agents).

   • Autonomous Construction: In a single output, the model successfully defined the specific,
     valid submodular valuation functions (presented in Table 1) and the ε-perturbation required
     to strictly break the bound.

   • Automated Verification: Without human intervention, the model correctly performed the
     tedious calculations of expected marginal gains across all 3! = 6 permutations to formally
     verify the violation.

Technical Details
In the problem of Online Submodular Welfare Maximization (Online SWM), items arrive one by
one in a random order and must be irrevocably assigned to agents with submodular valuation
functions. The goal is to maximize the total social welfare. It is well-established that the simple
Greedy algorithm achieves a competitive ratio of 1/2 in the adversarial setting. In the random order
model, Korula et al. proved that Greedy achieves a ratio of at least 0.5052, strictly beating 1/2 [68].
    To obtain a stronger bound, the authors proposed a natural conjecture (Conjecture 15) relating
the expected marginal gain of the Greedy algorithm when an item is moved to the end of the
sequence versus when it is duplicated at the end. If true, this conjecture would imply a competitive
ratio of at least 0.567.
    In this note, we refute this conjecture. We construct a counter-example involving a specific
submodular valuation function and a set of items where the conjectured inequality fails to hold.


                                                   12
The Open Question
We focus on the definitions and conjecture provided in Section 5 of [68]. Let π = (π1 , π2 , π3 , . . . , πn )
be a permutation of n items.

Definition 3.1 (Permutation Variants [68]). Fix a permutation π.

   • Let π M ove,i be the permutation achieved by moving the item πi to the end of the sequence:

                                    π M ove,i = (π1 , . . . , πi−1 , πi+1 , . . . , πn , πi )

   • Let π Copy,i be the sequence of n + 1 items achieved by copying πi to the end without removing
     the original πi :
                                π Copy,i = (π1 , . . . , πi−1 , πi , πi+1 , . . . , πn , πi )

    Let MG(k, σ) denote the marginal gain that the Greedy algorithm obtains by allocating the k-th
arriving item in a sequence σ. Let Sn be the set of all n! permutations. The conjecture proposed by
Korula et al. is as follows:

Conjecture 3.2 (Conjecture 15 of [68]). For any instance of the online submodular welfare maxi-
mization problem,
                        " n                     #        " n                    #
                         X                                X
                  Eπ∼Sn     MG(n + 1, π Copy,i
                                               ) ≤ Eπ∼Sn      MG(n, π M ove,i
                                                                              )             (1)
                            i=1                                             i=1

    The Right Hand Side (RHS) of the inequality is equivalent to n · Eπ∼Sn [MG(n, π)], as π M ove,i
and π share the same distribution. The conjecture essentially posits that the gain from a duplicated
item at the end of the stream is, in expectation, bounded by the gain of the last item in a standard
random permutation.

Refutation of the Conjecture
We answer the open question negatively. We show that there exist submodular valuation functions
and instances where the expected marginal gain from the copied item exceeds the bound proposed
in Conjecture 3.2.

Theorem 3.3. Conjecture 3.2 is false. There exists an instance of Online SWM such that:
                     " n                       #         " n                     #
                      X                                    X
                                       Copy,i                          M ove,i
              Eπ∼Sn       MG(n + 1, π         ) > Eπ∼Sn       MG(n, π          )
                            i=1                                             i=1


Counterexample Construction
We construct an instance with n = 3 items N = {e, x1 , x2 } and m = 2 agents {A1 , A2 }. We define
the valuation functions v1 and v2 . Let ε = 0.1. We define v1 (S) = v10 (S) + ε|S|, where v10 (S) and
v2 (S) are defined in Table 1.
    Verification of Validity We must verify that v1 and v2 are monotone and submodular.

   1. Monotonicity: It is clear from Table 1 that both v1 and v2 are monotone (i.e., v(S) ≤ v(T )
      if S ⊆ T ).


                                                          13
                                     Table 1: Valuation Functions

                                       S          v10 (S)   v2 (S)   v1 (S)
                                       ∅            0        0        0
                                      {e}           10       10      10.1
                                     {x1 }          10       7       10.1
                                     {x2 }          10       11      10.1
                                    {e, x1 }        15       17      15.2
                                    {e, x2 }        20       16      20.2
                                   {x1 , x2 }       20       16      20.2
                                  {e, x1 , x2 }     25       21      25.3


  2. Submodularity of v2 : We check the marginal gains (MG).

        • MG2 (e): ∅(10), {x1 }(10), {x2 }(5), {x1 , x2 }(5).
        • MG2 (x1 ): ∅(7), {e}(7), {x2 }(5), {e, x2 }(5).
        • MG2 (x2 ): ∅(11), {e}(6), {x1 }(9), {e, x1 }(4).

     In all cases, the marginal gains are non-increasing as the conditioning set grows. Thus, v2 is
     submodular.

  3. Submodularity of v1 : We first check v10 .

        • MG01 (e): ∅(10), {x1 }(5), {x2 }(10), {x1 , x2 }(5).
        • MG01 (x1 ): ∅(10), {e}(5), {x2 }(10), {e, x2 }(5).
        • MG01 (x2 ): ∅(10), {e}(10), {x1 }(10), {e, x1 }(10).

     v10 is submodular. Since v1 (S) = v10 (S) + ε|S| is the sum of a submodular function and a
     modular function, v1 (S) is submodular.

Calculation of the RHS
The RHS is the sum of the expected gains of each item when it arrives last. Let W (j) denote this
expectation for item j.

  1. W (e) (e arrives last). We consider the permutations of {x1 , x2 }.

        • (x1 , x2 ). x1 : A1 (10.1) vs A2 (7). x1 → A1 .
          x2 : MG1 (x2 |x1 ) = 10.1. MG2 (x2 ) = 11. x2 → A2 .
          Gain of e: MG1 (e|x1 ) = 5.1. MG2 (e|x2 ) = 5. Gain is 5.1.
        • (x2 , x1 ). x2 : A1 (10.1) vs A2 (11). x2 → A2 .
          x1 : MG1 (x1 ) = 10.1. MG2 (x1 |x2 ) = 5. x1 → A1 .
          Gain of e: 5.1.

     Result: W (e) = 5.1.

  2. W (x1 ) (x1 arrives last). We consider the permutations of {e, x2 }.

                                                      14
        • (e, x2 ). e: A1 (10.1) vs A2 (10). e → A1 .
          x2 : MG1 (x2 |e) = 10.1. MG2 (x2 ) = 11. x2 → A2 .
          Gain of x1 : MG1 (x1 |e) = 5.1. MG2 (x1 |x2 ) = 5. Gain is 5.1.
        • (x2 , e). x2 → A2 . e → A1 . Gain of x1 is 5.1.

     Result: W (x1 ) = 5.1.

  3. W (x2 ) (x2 arrives last). We consider the permutations of {e, x1 }.

        • (e, x1 ). e → A1 .
          x1 : MG1 (x1 |e) = 5.1. MG2 (x1 ) = 7. x1 → A2 .
          Gain of x2 : MG1 (x2 |e) = 10.1. MG2 (x2 |x1 ) = 9. Gain is 10.1.
        • (x1 , e). x1 → A1 .
          e: MG1 (e|x1 ) = 5.1. MG2 (e) = 10. e → A2 .
          Gain of x2 : MG1 (x2 |x1 ) = 10.1. MG2 (x2 |e) = 6. Gain is 10.1.

     Result: W (x2 ) = 10.1.


                   RHS = W (e) + W (x1 ) + W (x2 ) = 5.1 + 5.1 + 10.1 = 20.3.

Calculation of the LHS
The LHS is the expected total residual welfare. We calculate the total residual R(π) for all 3! = 6
permutations. The residual of item j, Rj (π), is the maximum marginal gain of j for any agent given
the final allocation by Greedy on π. (The agent who received j has 0 marginal gain for a copy).

  1. π1 = (e, x1 , x2 ).
     e → A1 . x1 → A2 (7 vs 5.1). x2 → A1 (10.1 vs 9).
     Allocation: A1 = {e, x2 }, A2 = {x1 }.
     Re = MG2 (e|x1 ) = 10. Rx1 = MG1 (x1 |e, x2 ) = 5.1. Rx2 = MG2 (x2 |x1 ) = 9.
     R(π1 ) = 24.1.

  2. π2 = (e, x2 , x1 ).
     e → A1 . x2 → A2 (11 vs 10.1). x1 → A1 (5.1 vs 5).
     Allocation: A1 = {e, x1 }, A2 = {x2 }.
     Re = MG2 (e|x2 ) = 5. Rx1 = MG2 (x1 |x2 ) = 5. Rx2 = MG1 (x2 |e, x1 ) = 10.1.
     R(π2 ) = 20.1.

  3. π3 = (x1 , e, x2 ).
     x1 → A1 . e → A2 (10 vs 5.1). x2 → A1 (10.1 vs 6).
     Allocation: A1 = {x1 , x2 }, A2 = {e}.
     Re = MG1 (e|x1 , x2 ) = 5.1. Rx1 = MG2 (x1 |e) = 7. Rx2 = MG2 (x2 |e) = 6.
     R(π3 ) = 18.1.

  4. π4 = (x2 , e, x1 ).
     x2 → A2 . e → A1 . x1 → A1 .
     Allocation: A1 = {e, x1 }, A2 = {x2 }.
     R(π4 ) = R(π2 ) = 20.1.



                                                 15
  5. π5 = (x1 , x2 , e).
     x1 → A1 . x2 → A2 . e → A1 .
     Allocation: A1 = {x1 , e}, A2 = {x2 }.
     R(π5 ) = 20.1.

  6. π6 = (x2 , x1 , e).
     x2 → A2 . x1 → A1 . e → A1 .
     Allocation: A1 = {x1 , e}, A2 = {x2 }.
     R(π6 ) = 20.1.

   The sum of the total residuals is 24.1 + 20.1 + 18.1 + 20.1 + 20.1 + 20.1 = 122.6.
                                                           122.6
                                     LHS = E[R(π)] =             .
                                                             6

Conclusion
We compare the LHS and the RHS.
                                                         121.8
                                       RHS = 20.3 =            .
                                                           6
                                               122.6
                                       LHS =         .
                                                 6
Since 122.6
        6        6 , we have LHS > RHS. This violates the inequality stated in Conjecture 15.
            > 121.8
Therefore, Conjecture 15 is false.
    The failure of Conjecture 15 implies that the specific path to proving a 0.567 competitive ratio
proposed by [68] is invalid. While the Greedy algorithm is known to beat 1/2 in the random order
model, establishing the tightest possible bound remains an open challenge. Our result indicates that
the interaction between duplicated items and previous greedy allocations is more complex than the
“Move” vs “Copy” intuition suggests.




                                                16
3.2   Cryptography: AI-Assisted Bug Detection in SNARGs
Written by Ziyi Guan, David P. Woodruff, and Eylon Yogev

Problem Context
Succinct non-interactive arguments (SNARGs) are among the most important and actively studied
primitives in modern cryptography. A SNARG enables a prover to convince a verifier of some
computational statement (such as knowledge of a solution to a complex equation or the validity
of a transaction according to network rules) using a proof that is extremely short and efficient to
verify. Remarkably, the proof size and verification time can be exponentially smaller than the time
required to check the statement directly. The succinct proof and verification is critical for real-world
applications. For instance:

   • Verifiable Outsourced Computation: A weak client (like a smartphone) can offload a heavy
     computation to a cloud server and receive a short proof that the result is correct, without
     trusting the server.

   • Blockchain Scalability: Blockchains can use SNARGs (often in the form of zk-SNARKs) to
     compress the verification of thousands of transactions into a single tiny proof, enabling massive
     throughput improvements (e.g., ZK-Rollups).

    Constructions of SNARGs are notoriously difficult despite the active research. For decades, re-
searchers have sought to build them based on standard cryptographic assumptions—assumptions
that are widely believed to be true and have withstood years of cryptanalytic attacks. The “holy grail”
in this area is to build a SNARG from the learning with errors (LWE) assumption. LWE is the
foundation of modern lattice-based cryptography; it is believed to be secure even against quantum
computers (post-quantum security) and allows for powerful functionalities like fully homomorphic
encryptions.
    Existing SNARG constructions typically fall short of this ideal in the following ways:

   1. Idealized Models: The most efficient SNARGs are usually constructed in the random oracle
      model (ROM), where hash functions are modeled as perfect random functions. However,
      random oracles cannot be instantiated in the real world and thus only provide heuristic
      security.

   2. Non-Standard Assumptions: Another common way to build SNARGs (with knowledge) relies
      on assumptions like “Knowledge of Exponent,” which are non-falsifiable and sometimes imply
      conclusions too strong to be true.

   3. Indistinguishability Obfuscation (iO): While iO can build almost anything, including SNARGs,
      current constructions of iO are extremely complex, inefficient, and rely on very heavy mathe-
      matical machinery.

    The paper “SNARGs for NP from LWE” by Ziyi Guan and Eylon Yogev [53] claimed to
achieve the breakthrough: a SNARG for all of NP based solely on the sub-exponential hardness
of LWE. Their proposed construction involved two novel components: “PCP shadows” (a way to
compress probabilistically checkable proofs) and “function vector commitments” (a lattice-based
vector commitment scheme).




                                                  17
AI Contribution via Advanced Prompting
As part of an experiment to evaluate the capability of AI models in theoretical computer science
research, we analyzed the preprint of the paper using a Google-internal LLM. Crucially, we did not
simply ask the model to “check the proof,” as standard prompts often lead to superficial reviews or
hallucinations when dealing with complex mathematical logic.
    Instead, we employed a rigorous iterative self-correction prompt. The prompt was designed
to force the model to act as a meticulous and adversarial reviewer. The explicit instructions are in
Figure 3.

      1. Generate an initial review that was strictly objective, focusing only on identifying
         errors and suggesting improvements.
      2. Self-correct its first review by rigorously critiquing its own findings. The model was
         told to verify every derivation, check for hallucinations, and ensure that any claim of an
         error was substantive.
      3. Generate a revised review incorporating these corrections.
      4. Perform a second round of self-correction to further refine the logic and ensure
         comprehensive coverage of the paper, including appendices.
      5. Produce a final, verified review adhering to strict mathematical standards.

   For your proof, adhere to: ⟨rigor text⟩.


                               Figure 3: Iterative self-correction prompt.

    Furthermore, the prompt included a specific protocol for mathematical rigor. It required the
model to distinguish between a “Complete Proof” (only if every step was verified) and “Structured
Partial Progress” (if any gaps were found). It also required the model to explicitly flag gaps or
unproven assumptions using a specific tag. This approach was used by Google recently for providing
preliminary feedback to authors of STOC submissions, see [24].

The Finding and Verification
Using this method, the model’s final review flagged a critical, fatal flaw in the paper’s construction
of “PCP with shadow soundness” (Section 4).
    The issue lay in the discrepancy between the definition of the scheme and its actual construction:

   • The Definition: Definition 4.1 (Property 3) of the paper required perfect consistency. This
     meant that for any two valid proofs that shared a local view, the generated “shadows” (succinct
     digests of the proof) must be identical for every single choice of randomness used in the shadow
     generation process.

   • The Construction: The construction presented in Section 4.3, however, only achieved
     imperfect consistency. This meant that the shadows would match with high probability over
     the choice of randomness, but there could exist bad randomness values where they differed.

    The model argued that this was not a minor technicality. The security proof for the SNARG
(specifically the soundness argument) relied heavily on the strong, perfect consistency definition. It
assumed that once a commitment was opened, the underlying shadow was unique and well-defined.


                                                    18
By only achieving statistical consistency, the construction opened the door to an adversary who could
find specific bad randomness values to break the binding between the proof and its shadow. This
would allow an adversary to forge a valid argument for a false statement, completely undermining
the security of the SNARG.

Expert Verification and Outcome
To validate the model’s finding, we shared the detailed critique with cryptography experts Aayush
Jain and Zhengzhong Jin. They performed an independent review of the paper and the model’s
output.
    Their assessment was definitive: the model was correct. They confirmed that the gap between
the definition and construction of perfect consistency was a fatal flaw in the logic. They noted that
while the model produced some noise (flagging other, less relevant issues), this specific insight was
accurate and hit the core of the problem. Without perfect consistency, the reduction used in the
security proof fails, and the main theorem does not hold.
    We subsequently communicated these findings to the paper’s authors, Ziyi Guan and Eylon
Yogev. They acknowledged the validity of the issue raised by the model. They agreed that the gap
between the definition and construction of consistency was a significant error. Following this, they
updated their paper on the Cryptology ePrint Archive. The updated manuscript includes a note in
red text explicitly stating that a gap in the proof of the main theorem had been found.
    This episode serves as a powerful testament to the evolving capabilities of large language models
in scientific research. While LLMs are often criticized for their inability to reason or their tendency
to hallucinate, this case shows that with the right prompting strategy—specifically one that enforces
iterative self-correction and rigorous verification—they can identify subtle, deep technical flaws in
state-of-the-art research.




                                                  19
4     Cross-Pollination of Ideas
In this section we see AI acting as an interdisciplinary bridge, retrieving obscure theorems from
entirely different mathematical domains to overcome roadblocks.

4.1    Approximation Algorithms: Max-Cut
Written by Euiwoong Lee.

Problem Context
The Goemans-Williamson (GW) algorithm uses Semidefinite Programming (SDP) to achieve an
optimal 0.878-approximation for Max-Cut. A long-standing open question asks whether rounding
SDP solutions of bounded rank d can yield a better approximation ratio. While known for d = 2, 3,
the case for general d remained open.
    I realized that this could be resolved if the following
                                                          Psimple and natural geometric property held:
Does the variance of a sum of random variables X =          sgn(⟨g, vi ⟩) (where vi are unit vectors with
bounded pairwise inner products) have a lower bound C(d)n2 ?

AI Contribution
The model solved this geometric variance question.

    • Synthesizing Advanced Math: The model recognized this as a problem solvable via
      geometric functional analysis, a field outside the typical approximation algorithms toolkit.

    • Proof via Measure Theory: It constructed a proof using the compactness of the space of
      probability measures on the sphere.

    • Iterative Rigor: When we questioned the validity of using “relaxed" measure spaces, the
      model justified its steps by citing and applying the Stone-Weierstrass Theorem, the Riesz
      Representation Theorem, and properties of spherical harmonics.

Max-Cut on Bounded-dimension SDP Solutions
Max-Cut is one of the most fundamental problems in combinatorial optimization and approximation
algorithms. Given an undirected graph G = (V, E), the goal is to partition V into V + and V −
to maximize the number of edges between V + and V − ; equivalently, compute x : V → {±1} to
maximize (u,v)∈E 1−x(u)x(v)    .
           P
                         2
    While combinatorial or linear programming (LP)-based methods only yielded a 1/2-approximation
(e.g., the returned solution’s value is at least half of the optimal value) in polynomial time, the
celebrated result of Goemans and Williamson [52] used a semidefinite programming (SDP) relaxation
to obtain an approximation ratio of αGW := mina∈[−1,+1] arccos(a)/π
                                                             (1−a)/2 ≈ 0.878, which was later proved
to be optimal for all polynomial-time algorithms assuming the Unique Games Conjecture [66]. This
tight relationship between algorithms, complexity, and SDPs was later extended to numerous other
combinatorial optimization tasks, most notably all Constraint Satisfaction Problems (CSPs) [82].
    Given the importance of this result, it is natural to ask which additional assumptions allow
polynomial-time algorithms to achieve an approximation ratio αGW + C for some constant C > 0.
Structural properties of the input graph G = (V, E) have been the most popular assumptions, which



                                                   20
include when G is dense (i.e., |E| = Ω(n2 ) [4]), G is bounded-degree [36, 59], or G has a certain
expansion property [9].
    In order to motivate assumptions depending on the structure of SDP solutions, let us briefly
recall Goemans-Williamson’s SDP relaxation. Given G = ({1, . . . , n}, E), their SDP relaxation, with
a symmetric matrix M ∈ Rn×n as the variable, is as follows:
                                             X 1 − Mi,j
                              maximize
                                                      2
                                             (i,j)∈E

                               subject to    Mi,i = 1          ∀i ∈ [n].
                                             M ⪰ 0.

The fact that this SDP is a relaxation for Max-Cut (i.e., the SDP optimal value is at least the
Max-Cut optimal value) is based on the fact that for any solution x : V → {±1} for Max-Cut,
M = xxT is a feasible solution for the SDP. For the αGW -approximation, the algorithm is the
following:
   1. Compute the optimal SDP solution M .
   2. Compute its Gram decomposition M = V V T for some V ∈ Rn×d . Let vi be the ith row of V .
   3. Sample a random Gaussian vector g ∼ N (0, Id ).
   4. For each i ∈ [n], let xi ← sgn(⟨vi , g⟩). (I.e., xi ← +1 if ⟨vi , g⟩ ≥ 0 and xi ← −1 otherwise.)
The αGW -approximation can be proved by a simple edge-by-edge analysis where each edge (i, j)
              1−⟨vi ,vj ⟩
contributes      2        to the SDP objective, and arccos(⟨vi , vj ⟩)/π to the Max-Cut objective in
expectation (because it is the probability that sgn(vi , g) ̸= sgn(vj , g)).
    So, how about the structural properties of the optimal SDP solution M ? Perhaps one of the
most natural assumptions on M is its rank; the gist of the Max-Cut problem itself is to force the
rank of M to be 1. Then the question is, if M is a feasible solution to the SDP with rank d, can we
round M to a Max-Cut solution of value at least (αGW + C(d)) times the SDP value of M , where
C(d) > 0 is a constant depending only on d?
    This is a natural question asked since the Goemans-Williamson algorithm, and Goemans gave a
positive answer when d = 2. Avidor and Zwick [5] refined it and gave a positive answer for d = 3 as
well, but to the best of my knowledge, even the case d = 4 is open. It is surprising, especially given
that analogous questions have already been answered for more general Grothendieck problems [15, 16];
however, they are not directly comparable, as the optimal ratios for Grothendieck problems are
worse than αGW .
    While studying the recent result of Hsieh and Kothari [59], which simplifies and extends the
result of Feige, Karpinski, and Langberg [36] for Max-Cut on bounded-degree graphs, I realized that
their algorithmic framework could be applied to the bounded-dimension case as well, modulo one
very natural geometric question, which is stated below.
    The rest of the section details how the model “solved it.” Now, there exists a polynomial-time
algorithm that, given an SDP solution M of rank d, produces a Max-Cut solution whose value is at
least (αGW + C(d)) times the value of M , for some C(d) > 0. But, before detailing the answer, let
us mention that the answer is not completely satisfactory in the sense that it does not produce any
explicit expression for C as a function of d; in contrast, when G’s degree is at most d, the best-known
approximation ratio is (αGW + Ω(   e 2 1 )) [59].
                                     d log d
    On the other hand, the proof is based on results from geometric analysis, including the compactness
of a certain space of probability measures, which have not been used much in the design of

                                                  21
approximation algorithms. Will it be among the first of many examples where such analytic tools
are used in approximation algorithms (and inspire more “constructive proofs” with “more explicit
bounds”)? In any case, this experience reinforces common beliefs that large language models can
help researchers in areas where they are not experts.

Geometric Question
The original question I asked the model is depicted in Figure 4.

   Problem 4.1. Let v1 , . . . , vn be unit vectors in Rd suchP
                                                              that ⟨vi , vj ⟩ ≥ −β for every i =
                                                                                               ̸ j, where
                                                                n
   β = 0.9. Let g ∼ N (0, Id ), Xi = sgn(⟨g, vi ⟩), and X = i=1 Xi . Is it always true that |X| ≥ εn
   with probability at least δ, for some ε > 0 and δ > 0 depending only on the dimension d?


                                   Figure 4: Original prompt for model

    Using the standard second-moment methods and the fact that E[Xi ] = 0, the model reduced it
to the following equivalent question about the variance of X, which is indeed the version one needs
for the Max-Cut application.

Problem 4.2. The variance of X is E[X 2 ] = ni=1 nj=1 h(⟨vi , vj ⟩), where h(t) = π2 arcsin(t). Is
                                                P P

E[X 2 ] ≥ C(d, β)n2 for some constant C(d, β) > 0?

    Due to space constraints, let me not fully elaborate on how a positive answer to Problem 4.2
leads to an improved algorithm for Max-Cut in the bounded-dimension case. It is simple to check
formally, because one can just replace Lemma 7 of [59] with the answer to Problem 4.2, and the
rest of their (elegant) seven-page paper works as is. Intuitively, their algorithm, which is originally
suggested by [36], performs the standard rounding algorithm mentioned above, followed by the
natural local improvement step; if there is a way to flip the assignment to a vertex that strictly
improves the value, execute it. (The actual algorithm implements it in a more conservative way.)
In this context, Problem 4.2 seems natural, because from the perspective of a vertex v, the more
variance its neighbors have, the bigger chance there is that the standard rounding algorithm (which
already guarantees an αGW -approximation) made a wrong decision for v and the local improvement
step further improves upon it by flipping v. In particular, the answer to Problem 4.2 is applied to
the neighborhood of every vertex.

First Response
The response in this section is fully generated by the model, except for removing standard applications
of second-order methods.


  Let µ = n1 ni=1 δvi be the empirical probability measure on the unit sphere S d−1 . The normalized
             P
  variance is:                              ZZ
                                1       2
                       Q(µ) = 2 E[X ] =                     h(⟨x, y⟩)dµ(x)dµ(y).
                               n               S d−1 ×S d−1

  The constraint on the vectors implies that the support Sµ of µ satisfies ⟨x, y⟩ ≥ −β for all
  x, y ∈ Sµ . Let Mβ (d) be the set of all probability measures on S d−1 satisfying this support



                                                       22
constraint. We define:
                                     C(d, β) =     inf      Q(µ).
                                                 µ∈Mβ (d)

Lemma 4.3. For finite d ≥ 1 and 0 ≤ β < 1, C(d, β) > 0.

Proof. We proceed in three steps:

1. Compactness and Continuity: Since d is finite, S d−1 is compact. The space of probability
measures P(S d−1 ) is compact in the weak topology. We show that Mβ (d) is a closed subset.
Let µk ∈ Mβ (d) converge weakly to µ.
Let Sk and S be their respective supports. Let x, y ∈ S. For any ε > 0, the balls B(x, ε/2) and
B(y, ε/2) have positive measure under µ. By the Portmanteau theorem, for sufficiently large
k, µk (B(x, ε/2)) > 0. Thus, there exist xk ∈ Sk and yk ∈ Sk such that ∥x − xk ∥ < ε/2 and
∥y − yk ∥ < ε/2.
We have ⟨xk , yk ⟩ ≥ −β. Also,

               |⟨x, y⟩ − ⟨xk , yk ⟩| ≤ ∥x − xk ∥∥y∥ + ∥xk ∥∥y − yk ∥ < ε/2 + ε/2 = ε.

Thus, ⟨x, y⟩ ≥ ⟨xk , yk ⟩ − ε ≥ −β − ε. Since ε is arbitrary, ⟨x, y⟩ ≥ −β. Therefore, µ ∈ Mβ (d).
Thus, Mβ (d) is compact.
Since h(⟨x, y⟩) is continuous, Q(µ) is continuous in the weak topology. Therefore, the infimum
C(d, β) is attained by some measure µ∗ ∈ Mβ (d).

2. Moment Expansion: The Taylor series of h(t) is h(t) = m odd,m≥1 am tm , where am > 0
                                                         P

for all odd m. Let Tm (µ) = x dµ(x) be the m-th moment tensor. We can write:
                           R ⊗m

                          X     ZZ                      X
                 Q(µ) =      am    ⟨x, y⟩m dµ(x)dµ(y) =    am ∥Tm (µ)∥2 .
                          m odd                                 m odd


3. Symmetry and Contradiction: Suppose C(d,             R β) = 0.∗ Then Q(µ ) = 0. Since am > 0,
                                                                            ∗

this implies Tm (µ ) = 0 for all odd m. This means P (x)dµ (x) = 0 for any odd polynomial
                   ∗

P (x). By the Stone-Weierstrass theorem, odd polynomials are dense in the space of continuous
odd functions  on S d−1 (in the uniform norm).
Thus, g(x)dµ∗ (x) = 0 for any continuous odd function g. This implies that µ∗ is a symmetric
       R

measure (i.e., µ∗ (A) = µ∗ (−A)).
Let S ∗ be the support of µ∗ . If µ∗ is symmetric, S ∗ must be symmetric. (If x ∈ S ∗ but −x ∈
                                                                                             / S∗,
there is an open ball B(−x, r) such that µ (B(−x, r)) = 0. By symmetry, µ (B(x, r)) =
                                                ∗                                     ∗

µ∗ (−B(−x, r)) = 0, contradicting x ∈ S ∗ ).
Since S ∗ is non-empty and symmetric, there exists x ∈ S ∗ such that −x ∈ S ∗ . The support
constraint requires ⟨x, −x⟩ ≥ −β. But ⟨x, −x⟩ = −∥x∥2 = −1. So −1 ≥ −β or β ≥ 1. This
contradicts the assumption β = 0.9 < 1.
Therefore, C(d, β) > 0.

This establishes that E[X 2 ] ≥ C(d, β)n2 .




                                                 23
Interactions
The first response, though it looked like a natural and sound approach using geometric functional
analysis, had some gaps in the proof and was not fully verifiable, partially due to my inexpertise on
the topic. Two major hurdles were (1) the foundations of measure theory to establish the compactness
of Mβ (d)R and (2)∗ working knowledge of spherical harmonics to see how Tm (µ ) = 0 for all odd m
                                                                                 ∗

implies P (x)dµ (x) = 0 for any odd polynomial P (x). Note that (2) was somewhat expected as
the previous results for d = 2, 3 [5] and Grothendieck problems [15, 16] used spherical harmonics
and related Gegenbauer polynomials, but the use of (1), via relaxing n-point discrete measures to
Mβ (d), is a type of an argument rarely used in the approximation algorithms literature. In order
to formally understand it, one needs to review the foundations of measure theory. For example,
what  is the weak topology? How is the Stone-Weierstrass theorem formally applied here? How does
  g(x)dµ∗ (x) = 0 for every odd g imply µ∗ is a symmetric measure?
R

    After several iterations of asking for the reference behind each nontrivial step and manually
searching each reference and feeding it back to the model, it produced the output in the next section.
Now it is understandable to me, whose only formal exposure to analysis was an undergraduate course
almost twenty years ago.

Second Response
This response is fully generated by the model, except for (1) removing standard applications of
second-order methods, (2) adding two footnotes further justifying some steps, and (3) minor cosmetic
changes.

  Foundational Theorems We rely on the following established theorems, sourced externally
  (e.g., via Google Search, Wikipedia, or standard textbooks).
  External Result 1 (Stone-Weierstrass Theorem (Real Version)). Suppose X is a
  compact Hausdorff space and A is a subalgebra of C(X, R) which contains a non-zero constant
  function. Then A is dense in C(X, R) (under the uniform norm) if and only if it separates
  points.
  External Result 2 (Riesz Representation Theorem). Let Ω be a compact Hausdorff
  space. The dual space C(Ω)∗ is isomorphic to the space of finite regular signed measures on Ω.
  External Result 3 (Banach-Alaoglu Theorem). The closed unit ball of the dual space of
  a normed vector space is compact in the weak* topology.
  External Result 4 (Definition and Properties of Spherical Harmonics).
     1. (Definition): Spherical harmonics of degree k on S d−1 are the restrictions to the sphere
         of homogeneous harmonic polynomials of degree k in Rd . Let Hk denote this space.

     2. (Completeness):
           L∞           The spaces Hk are mutually orthogonal in L2 (S d−1 ). The algebraic
        sum k=0 Hk is dense in C(S d−1 ) and L2 (S d−1 ).

     3. (Parity): A spherical harmonic Yk ∈ Hk has parity (−1)k . That is, Yk (−x) = (−1)k Yk (x)
        for x ∈ S d−1 .

  External Result 5 (Addition Theorem for Spherical Harmonics). Let d ≥ 2 and
  λ = (d − 2)/2. The Gegenbauer polynomial Ckλ (⟨x, y⟩) is a positive semi-definite kernel. The




                                                 24
energy integral                              ZZ
                                  Ik (µ) =        Ckλ (⟨x, y⟩)dµ(x)dµ(y)

is non-negative. Ik (µ) = 0 if and only if µ is orthogonal to Hk .

Energy Minimization Framework           If d = 1, the constraint forces all vi to be identical, so
|X| = n. Assume d ≥ 2. Let µn = n δvi . The normalized variance is:
                                 1 P


                                E[X 2 ]
                                           ZZ
                      F (µn ) =         =      K(⟨x, y⟩)dµn (x)dµn (y),
                                 n2
where K(t) = π2 arcsin(t). Let M′β (S d−1 ) be the set of probability measures µ on S d−1 such that
for any distinct x, y in the support Sµ , ⟨x, y⟩ ≥ −β. We want to show C(d) = inf µ∈M′β F (µ) > 0.

Compactness and Continuity We consider M(S d−1 ) with the weak-* topology. S d−1 is a
compact metric space.
Lemma 4.4 (Compactness of M(S d−1 )). M(S d−1 ) is compact in the weak-* topology.
Proof. By External Results 2 and 3, M(S d−1 ) is identified as a weak-* closed subset of the unit
ball in C(S d−1 )∗ , which is compact by Banach-Alaoglu.

Lemma 4.5 (Portmanteau Lemma (Partial)). If µk → µ weakly in a metric space X, then for
every open set G ⊂ X, lim inf k µk (G) ≥ µ(G).
Proof. Let G be open, F = Gc . Define the continuous function fm (x) = min(1, m · dist(x, F )).
As m → ∞, fm (x) ↗ 1G (x).
                                                Z         Z
                        lim inf µk (G) ≥ lim inf fm dµk = fm dµ.
                              k                    k

By the Monotone Convergence Theorem, as m → ∞, the RHS converges to µ(G).

Lemma 4.6. M′β (S d−1 ) is a closed subset of M(S d−1 ) and thus compact.
Proof. Let µk ∈ M′β → µ. Suppose µ ∈       / M′β . There exist distinct x, y ∈ Sµ such that
⟨x, y⟩ < −β. We find disjoint open balls Bx , By where the inner product remains < −β. Since
x, y ∈ Sµ , µ(Bx ) > 0. By Lemma 4.5, lim inf k µk (Bx ) > 0. For large k, there exist xk , yk in the
support of µk within Bx and By . Thus xk =
                                         ̸ yk . As µk ∈ M′β , ⟨xk , yk ⟩ ≥ −β. Contradiction.

Lemma 4.7 (Product Convergence). If µk → µ weakly on a compact space X, then µk × µk →
µ × µ weakly on X × X.
Proof.  Let H ∈ C(X × X). By External Result 1, separable functions Happrox (x, y) =
   fi (x)gi (y) are dense. For Happrox , the convergence holds by definition of µk → µ. The
P
result extends to H by density.

Lemma 4.8. F (µ) is continuous on M(S d−1 ).
Proof. H(x, y) = K(⟨x, y⟩) is continuous. If µk → µ, by Lemma 4.7, µk × µk → µ × µ. By
definition of weak convergence, F (µk ) → F (µ).

Since F is continuous and M′β is compact, the infimum C(d) is attained.



                                                       25
Strict Positivity via Harmonic Analysis P     We show C(d) > 0. Let λ = (d − 2)/2. We write
K(t) = ∞         λ (t). The energy is F (µ) =  ∞
                                               k=0 bk Ik (µ). By External Result 5, Ik (µ) ≥ 0.
       P
             b C
         k=0 k k

Lemma 4.9 (Monomial Expansion Positivity). Let d ≥ 2 (so λ ≥ 0). The expansion of tn in
the basis of Gegenbauer polynomials Ckλ (t) has strictly positive coefficients.
Proof. Case λ > 0 (d > 2). The inversion formula is known to be:a
                                       ⌊n/2⌋
                                    n! X    (n − 2k + λ)
                             tn =                           C λ (t)
                                    2n   λ · k! · (λ + 1)n−k n−2k
                                       k=0

where (a)m is the rising factorial. Since λ > 0, n − 2k ≥ 0, and the factorials and Pochhammer
symbols are positive, the coefficients are strictly positive.
Case λ = 0 (d = 2). The basis are Chebyshev polynomials Tk (t). The inversion formula is:
                                               ⌊n/2⌋   
                                        1      X      n
                                tn =                      εn−2k Tn−2k (t)
                                       2n−1           k
                                               k=0

where εj is 1/2 if j = 0 and 1 if j > 0. The coefficients are positive.

We analyze the coefficients bk for K(t) = π2 arcsin(t).
   1. Parity: K(t) is odd. Ckλ (t) has the parity of k. Thus, bk = 0 for even k.

   2. Positivity of bk : arcsin(t) =     cm t2m+1 with cm > 0. By Lemma 4.9, t2m+1 is a sum of
                                      P
       λ
      C2j+1 (t) with strictly positive coefficients. Therefore, bk > 0 for all odd k.
Suppose F (µ) = 0. Since bk > 0 (odd k) and Ik (µ) ≥ 0, we must have Ik (µ) = 0 for all odd k.
By External Result 5, µ is orthogonal to Hk for all odd k.
Lemma 4.10 (Parity of Polynomials and Spherical Harmonics). A polynomial P (x) restricted
to S d−1 is an odd function if and only if its expansion in the basis of spherical harmonics consists
solely of spherical harmonics of odd degree.
Proof. By External Result 4 (Completeness
                                      L and Definition), P   the space of polynomials restricted
                                                               N
to S d−1 is the algebraic direct sum     Hk . Let P (x) =          Y (x), where Yk ∈ Hk . By
                                                                 PNk
                                                               k=0
External Result 4 (Parity), Yk (−x) = (−1) Yk (x). So P (−x) = k=0 (−1)k Yk (x). If P is odd,
                                            k

P (−x) = −P (x). Then N    k=0 ((−1) + 1)Yk (x) = 0. Since the spaces Hk are orthogonal, they
                                    k
                        P
are linearly independent. Thus ((−1)k + 1)Yk (x) = 0 for all k. If k is even, 2Yk (x) = 0, so
Yk = 0. Thus, P (x) consists only of odd degree harmonics. The converse is immediate.

We show F (µ) = 0 implies µ is symmetric (i.e., f dµ = 0 for any continuous odd function
                                                   R

f ). Let f be continuous and odd. By External Result 1, let polynomials Pn → f uniformly.
The odd part Qn (x) = (Pn (x) − Pn (−x))/2 is an odd polynomial, and Qn → f uniformly. By
Lemma 4.10,
          R Qn is composed solely of spherical harmonics   of odd degree. Since µ is orthogonal
to these, Qn (x)dµ(x) = 0. By uniform convergence, f (x)dµ(x) = 0. Thus, µ is symmetric.b
                                                      R

Now we use the constraint µ ∈ M′β . Suppose C(d) = 0. The minimizer µ∗ has F (µ∗ ) = 0, so µ∗
is symmetric. Let S be the support of µ∗ . Let x ∈ S. Since µ∗ is symmetric, −x ∈ S. Since
∥x∥ = 1, x ̸= −x. By the definition of M′β , ⟨x, −x⟩ ≥ −β. This means −1 ≥ −β, or β ≥ 1.



                                                     26
This contradicts β = 0.9. Therefore, C(d) > 0.
   a
    The section author’s note: It can be proved by induction using the recurrence relation given in https:
// en. wikipedia. org/ wiki/ Gegenbauer_ polynomials .
   b
                                    R formal Rjustification of this step, note that the pushforward A∗ µ for the
    The section author’s note: For the
antipodal map A(x) = −x satisfies f dµ = Rf dA∗ µ for every continuous f . As the Riesz Representation
Theorem shows that µ is fully characterized by ( f dµ)f ∈C(S d−1 ) , we can conclude that µ = A∗ µ.




                                                      27
4.2   Computational Geometry: Steiner Trees
Written by Karthik C. S.

Problem Context
The "Simplex is the Best for Graph Embeddings" conjecture states that among all graphs with m
edges embedded into Euclidean space as characteristic vectors, the star graph configuration yields
the minimum Steiner tree cost. Proving this is a key step towards establishing APX-hardness for
high-dimensional Steiner Tree problems.

AI Contribution
The model’s involvement was decisive.

   • The Crucial Link: The model suggested an approach based on the Kirszbraun Extension
     Theorem, which guarantees the existence of Lipschitz-preserving extensions of maps between
     Hilbert spaces.

   • Overcoming "Elementary" Bias: Initially, the model dismissed this approach as "non-
     elementary". However, when the researcher clarified that an elementary proof was not required,
     the model successfully formalized the argument.

   • Formal Proof: The model constructed a mapping from any graph embedding to the star
     graph embedding and used Kirszbraun’s theorem to show that a Steiner tree for the former
     can be transformed into a valid tree for the latter without increasing cost.

Technical Details: Steiner Trees and Graph Embeddings
In the Euclidean Steiner Tree problem, we are given as input a set of points (called terminals) in the
ℓ2 -metric space, and the goal is to find the minimum-cost tree connecting them. Additional points
from the space (called Steiner points) can be introduced as nodes in the solution.
    The seminal works of Arora [3] and Mitchell [76] provide a Polynomial Time Approximation
Scheme (PTAS) for solving the Euclidean Steiner Tree problem in fixed dimensions. However, the
problem remains poorly understood in higher dimensions (such as when the dimension is logarithmic
in the number of terminals). Ruling out a PTAS for the problem in high dimensions is a notoriously
long-standing open problem (for example, see Trevisan [93]).
    In [41], the authors proposed various conjectures related to Steiner trees in order to make progress
on understanding the inapproximability of the high-dimensional Euclidean Steiner Tree problem.
Assuming these, they could prove APX-hardness of the Euclidean Steiner Tree problem in dimensions
polynomial in the input size.
    The simplest such conjecture, called the Simplex is the Best for Graph Embeddings Conjecture in
[41], was a special case of the widely open generalized Gilbert-Pollak conjecture [51, 61, 30]. In this
report, we detail the resolution of this conjecture by Gemini, including the process.
    First, we state the conjecture and provide the necessary context. Next, we describe our interaction
with Gemini that led to its resolution. Finally, we present the proof produced by Gemini.

Research Context
A natural approach to prove the APX-hardness of the Euclidean Steiner Tree problem is via a
reduction from the Vertex Cover problem on bounded degree graphs (for example, see [42]). A

                                                  28
candidate reduction proposed in [41] is to embed a vertex cover instance graph G = (V, E) into R|V |
by mapping each edge {u, v} ∈ E to eu + ev , where eu is the standard basis vector with 1 in the
coordinate indexed by u and 0 elsewhere. Thus, each edge is embedded as its characteristic vector.
The embedding  √ of the set of edges incident to a single node forms the vertices of a regular simplex
of side length 2. The point configuration as a whole consists of the vertices of a regular simplicial
complex (where we take the union of the simplices associated with each node).
    Proving that the above reduction is gap-preserving, by analyzing the completeness and soundness
cases, requires proving the following conjecture:

Conjecture 4.11 (Euclidean Steiner Tree for Regular Simplicial Complexes [41]). For all constants
r ∈ (0, 1) and α ∈ (0, 1/r − 1), there exist constants s, β > 0 and M ∈ Z+ sufficiently large so that,
for all m ≥ M , given a regular, unit, simplicial complex on m vertices:

   1. Completeness: If the vertices can be partitioned into the vertices of at most rm unit regular
      simplices, then the point configuration of the m vertices admits a Euclidean Steiner tree of cost
      at most sm.

   2. Soundness: If the vertices cannot be partitioned into the vertices of fewer than (1 + α)rm unit
      regular simplices, then the point configuration of the m vertices does not admit a Euclidean
      Steiner tree of cost less than (1 + β)sm.

   As a first step toward proving the above conjecture, [41] proposed the following much simpler
conjecture about Steiner ratios of specialized point-sets.

Conjecture 4.12 (Simplex is the Best for Graph Embeddings [41]). Over all simple graphs with m
edges, the embedding1 of the star graph on m edges has the minimum cost Steiner tree.

    Observe that restricted to connected graphs with the same number of edges, the minimum
spanning tree costs are identical. Consequently, Conjecture 4.12 over connected graphs is equivalent
to finding the point configuration with the minimum Steiner ratio. In [41], the authors verified the
conjecture computationally up to m = 10 using the exact algorithm of Smith [91] and established
the following structural property.

Lemma 4.13 (Fleischmann et al. [41]). For any fixed m ≥ 1, the graph of size m whose embedding
(as above) has the minimum cost Steiner tree has diameter at most 2.

Methodology
I requested David Woodruff to formulate a prompt to solve Conjecture 4.12 using the Google internal
model, providing only the paper [41] as context.
    The model proposed two approaches but did not offer a conclusive answer. The second approach
involved starting from an arbitrary graph G and applying local transformations that do not increase
the optimal Steiner tree cost, eventually converging to the star graph. As we had already attempted
this strategy, it offered no new insights.
    The first approach, however, was based on the Kirszbraun Extension Theorem [67, 94]. I must
confess that while I was aware of various extension theorems from my work on the computation
of fixed-points (see, for example, [46]), I had not immediately seen the connection to Steiner trees.
To my frustration, instead of exploring this direction further, the model noted that the proof of
   1
    Here we allude to embedding each edge by its characteristic vector, as detailed in the aforementioned reduction
from the Vertex Cover problem.



                                                        29
Kirszbraun Extension Theorem is non-elementary, and concluded that this approach would not yield
an elementary proof of Conjecture 4.12.
    As I was not seeking an elementary proof and indeed, had not requested one, this comment left
me slightly frustrated, yet intrigued. Consequently, I decided to run my own experiments using
Gemini Ultra (utilizing the standard “thinking” mode rather than “deep think”).
    Initially, I provided the exact prompt used for the internal model, but Gemini consistently
declined to attempt the problem, insisting that it was an open problem that could not be solved.
    Next, I removed the paper from the context and provided only the problem statement along with
the relevant definitions. At first, the model suggested a hand-waving argument; however, when I
pointed out the parts that required formalization, it successfully provided them. It first derived the
same lemma suggested by the internal model, though this time with a proof. As the proof remained
somewhat informal, I provided Gemini with the summary of the internal model’s output and with its
explanation of why it had abandoned the approach. At that point, Gemini successfully formalized
the lemma using the Kirszbraun Extension Theorem (the tool it had been missing earlier).
    Through this process, I have learned about the power of the Kirszbraun Extension Theorem
for Steiner tree computation and analysis. To the best of my knowledge, this is a new connection
(yet one that feels very natural!). This discovery makes me more optimistic about the prospects of
establishing the APX-hardness of computing the Euclidean Steiner Tree in high dimensions.

Gemini’s Proof of Conjecture 4.12

  Theorem 4.14. Let f be an embedding of a graph into Euclidean space such that for any edge
  {u, v} ∈ E(G), f ({u, v}) = eu + ev , where {eu : u ∈ V (G)} are standard basis vectors. Let Starm
  denote the star graph with m edges, and let G be any arbitrary graph with m edges. Let SMT(P )
  denote the length of the Euclidean Steiner Minimal Tree of a point set P . Then:

                                    SMT(f (Starm )) ≤ SMT(f (G)).

  Proof. Let G = (VG , EG ) be a graph with |EG | = m edges and |VG | = k vertices. The embedding
  f maps edges to points in Rk . Let PG = {x1 , . . . , xm } ⊂ Rk be the set of m points generated by
  the edges of G. Similarly, let Starm have vertex set VStar with |VStar | = m + 1. Its embedding
  lies in Rm+1 . Let PStar = {y1 , . . . , ym } ⊂ Rm+1 be the corresponding point set generated by the
  edges of the star graph.
  The star graph edges share a center. For any distinct pair yi , yj ∈ PStar , the distance is:
                                                            √
                                                ∥yi − yj ∥ = 2.

  Thus, PStar forms the vertices of a regular simplex in Rm+1 .
  For PG ⊂ Rk , the distance between       √ points depends on edge adjacency, where we have for
  adjacent edges that ∥xi − xj ∥ =       √ 2 and for disjoint edges we have ∥xi − xj ∥ = 2. Thus,
  ∀xi , xj ∈ PG , i ̸= j : ∥xi − xj ∥ ≥ 2.
  We construct a bijection ϕ : PG → PStar . Let ϕ(xi ) = yi for i = 1, . . . , m. We verify the Lipschitz
  condition for ϕ on the domain PG . Consider any xi , xj ∈ PG :
                                                               √
                               ∥ϕ(xi ) − ϕ(xj )∥ = ∥yi − yj ∥ = 2 ≤ ∥xi − xj ∥.

  The map ϕ is 1-Lipschitz on the set of terminal points PG .



                                                    30
Let TG be the Euclidean Steiner Minimal Tree for PG . TG is a subset of the ambient space
Rk . We must map this tree to the ambient space of the star graph, Rm+1 . We now use the
Kirszbraun Extension Theorem [67, 94] in the following formulation.
Theorem 4.15 (Theorem 1.31 in [89]). Let H1 and H2 be Hilbert spaces. If U ⊂ H1 and
ϕ : U → H2 is a 1-Lipschitz map, there exists an extension Φ : H1 → H2 such that Φ|U = ϕ and
Φ is 1-Lipschitz on all of H1 .
We apply this theorem with H1 = Rk and H2 = Rm+1 . The extension Φ : Rk → Rm+1 satisfies:

                             ∥Φ(u) − Φ(v)∥ ≤ ∥u − v∥ ∀u, v ∈ Rk .

Let TG denote the Euclidean Steiner Minimal Tree for the point set PG . We treat TG as a graph
defined by a set of vertices VT and a set of edges ET :

   • VT = PG ∪ SG , where PG are the terminal points and SG are the Steiner points introduced
     to minimize the total length.

   • The total cost is the sum of the lengths of the edges:
                                                              X
                             SMT(f (G)) = Length(TG ) =                ∥u − v∥.
                                                            {u,v}∈ET


We construct a candidate tree T ′ for the star graph configuration PStar by applying the extended
map Φ to every vertex in VT . Let VT′ = {Φ(z) | z ∈ VT }. Since Φ is an extension of ϕ, we have
Φ(PG ) = PStar . Thus, VT′ contains the required terminals PStar . For every edge {u, v} ∈ ET , we
form a corresponding edge {Φ(u), Φ(v)} in T ′ . Since TG is connected, the image graph T ′ is
also connected and spans PStar . Thus, T ′ is a valid Steiner tree for PStar .
We now compare the lengths using the 1-Lipschitz property of Φ:
                                               X
                              Length(T ′ ) =         ∥Φ(u) − Φ(v)∥.
                                             {u,v}∈ET

Since ∥Φ(u) − Φ(v)∥ ≤ ∥u − v∥ for every pair u, v:
                                       X
                       Length(T ′ ) ≤         ∥u − v∥ = Length(TG ).
                                         {u,v}∈ET

Finally, since SMT(PStar ) is the infimum of lengths of all valid trees connecting PStar , it must be
less than or equal to the length of our candidate tree T ′ :

                                    SMT(PStar ) ≤ Length(T ′ ).

Combining these inequalities:

           SMT(f (Starm )) = SMT(PStar ) ≤ Length(T ′ ) ≤ Length(TG ) = SMT(f (G)).




                                                 31
4.3   Graph Theory: Computing Perfect Matchings in Regular Bipartite Graphs
Written by Ken-ichi Kawarabayashi
    The main contribution of the AI here is to provide a solution to a problem in Graph Theory by
pulling in tools from:

   1. Statistical Physics (Bethe Approximation),

   2. Number Theory (Coprime integers and integrality gaps)

   3. Spectral Analysis (Ihara-Bass identity)

Remark after the first version is posted After we posted the first version on ArXiv, Leonid
Gurvits made a few remarks, including (i) the AI and I missed several vital citations, including
improvement over Schrijver’s bound below, and (ii) the AI’s suggestion based on spectral graph
theory is, indeed, an important factor for the solution of Kadison-Singer problem by Adam Marcus,
Daniel Spielman and Nikhil Srivastava, which is one of the most fascinating and, perhaps one of the
most important breakthroughs in mathematics of 21-st century.
   Below, we add these remarks (as mentioned in “Post Remark”). We sincerely thank Leonid
Gurvits for these suggestions, which make this section even more interesting.

Problem Context
The goal was to improve bounds on the number of perfect matchings (permanents) in regular
bipartite graphs. In 1998, Schrijver provided a lower bound with a superior base [87].

Theorem 4.16 (Schrijver, 1998). Any k-regular bipartite graph with 2n vertices has at least
                                                                     n
                                                        (k − 1)k−1
                                                    
                                     BS (k, n) =
                                                           k k−2

perfect matchings.

   The base in Schrijver’s bound is best possible, as shown in [88], and the equality for all k is
shown by Schrijver [87]. The goal is to improve not the base, but a multiplicative factor.

Post Remark. Both the AI and I missed the following important results [54, 56]. Gurvits has
shown that the number of perfect matchings in k-regular bipartite graphs with 2n vertices is at least
                                          k − 1 k−1 n−k k!
                                 k n ((        ) )         > BS (k, n).
                                            k           kk
Let us point out that the AI proved a slightly stronger form (in terms of the Bethe approximation,
and this form may be of independent interest, slightly different from the improvement of Schrijver’s
bound).

AI Contributions
We fed the Schrijver’s paper [87] to the model and asked it to improve the bound.




                                                     32
   • Iterative Proof Discovery via Integrality Gaps: The AI’s initial proof attempt had errors
     (misunderstanding of the proof in [87] and citing some wrong papers/theorems), but through
     an iterative prompting process, the AI successfully connected Schrijver’s bound to the Bethe
     permanent [55]. By identifying a number-theoretic integrality gap, the AI established a strictly
     stronger lower bound (a marginal improvement, but it shows a stronger form).
     I should mention that the AI demonstrated a strong capacity for self-correction. Acting as its
     own adversarial peer reviewer (like “STOC” review), it critiqued its own intermediate proofs,
     identifying and correcting not only typographical errors but substantive logical flaws.

   • Generalization via Exact Bounds: The AI analyzed cubic bipartite graphs to extract
     exact boundary constants. By recovering Voorhoeve’s exact differential formula, it successfully
     extracted a strict asymptotic improvement factor.

   • A New Perspective: Finally, the AI suggested a strategy based on spectral graph theory to
     improve further. This insight was not obvious to the researchers as it was a consequence of the
     “worst” case analysis (i.e., by considering Ramanujan/expander graphs, the AI brought the
     Alon-Boppana theorem [78] and Kesten-McKay laws [65, 75])). Although the AI’s improvement
     is marginal (though it shows a slightly stronger form), this part is perhaps interesting.
     In addition, this collaboration could serve as a prime example of AI-driven cross-pollination:
     to make progress on a pure graph-theoretic question, the AI autonomously synthesized tools
     from statistical physics, number theory, and spectral analysis.

   • Post Remark: It turns out that the AI’s suggestion for a strategy based on spectral graph
     theory to improve further was an essential factor for the solution of the Kadison-Singer problem
     by Marcus, Spielman, and Srivastava [73].
     Thus, this suggestion appears highly promising, given the prior success. Indeed, it is surprising
     that, although their work is not directly connected to counting perfect matchings in regular
     bipartite graphs, the AI has already identified one of the most successful approaches in
     21st-century mathematics.

Technical Details
For an n × n matrix A, let ai,j be the entry at the ith row and jth column. The permanent of A is
defined as
                                                  XY   n
                                     perm(A) =            ai,σ(i)                             (2)
                                                   σ∈P i=1

where P is the set of all permutations of {1, 2, . . . , n}. Computing the permanent is known to be
#P-complete [95].
    We are interested in the case when A is the bi-adjacency matrix of a k-regular bipartite graph
G with 2n vertices. In this case, perm(A) equals the number of perfect matchings in G (such a
bipartite graph always has a perfect matching by Hall’s theorem (see [71]).
    A famous result concerning the lower bound is the resolution of the Van der Waerden conjecture,
proved by Falikman [34] and Egorychev [33], which asserts that the number of perfect matchings for
a k-regular bipartite graph H with 2n vertices is at least
                                                k n n!
                                                       .
                                                 nn
                              √
This bound is approximately       2πn(k/e)n .

                                                  33
    In 1998, Schrijver provided a different lower bound with a superior base [87], as in Theorem 4.16.
Two new proofs are given in [26, 54]. The base in Schrijver’s bound is best possible, as shown in
[88], and the equality for all k is shown by Schrijver [87]. Let p(k, n) be the minimum number of
perfect matchings in any k-regular bipartite graph with 2n vertices. As mentioned above, we cannot
improve the base, but Schrijver mentioned:

     [Question 1] It might be possible to derive a sharper lower bound for p(k, n) with the
     methods of the present paper.

    This is the question the model is asked. Below, we basically present the AI’s answers and
writeups.

Post Remark. The AI proved a slightly stronger form (in terms of the Bethe approximation, and
this form may be of independent interest (a bit different progress from improvement of Shrijver’s
bound)), but, as mentioned above, this question was already answered by Gurvits [54, 56].

A slightly better bound on (Q1)
The model answers Q1 affirmatively for k ≥ 2 (but small improvement) by utilizing the connection
between Schrijver’s bound and the Bethe approximation, relying on results by Gurvits [55] and
Vontobel [96] (so the AI gives a stronger form). The proof and writeup below is given by the AI and
its “revision” suggested by the AI when reviewing its proof and writeup (at the end, we (KK) will
make remarks on the proof and writeup).


  Theorem 4.17. For k ≥ 2 and n ≥ 1, p(k, n) > BS (k, n). In fact, we show a stronger
  form: p(k, n) = perm(AG ) > permB (AG ) = BS (k, n), where AG is the bi-adjacency matrix of a
  k-regular bipartite graph G with 2n vertices, and permB (AG ) = PermBethe (G) is defined below.

  Proof. The proof relies on establishing the relationship between the true permanent, the Bethe
  permanent, and Schrijver’s bound.
  Step 1: Schrijver’s Bound is the Bethe Approximation. The connection is fundamental.
  As derived by Gurvits [55] (specifically in Section 5.3), for any k-regular bipartite graph G,
  Schrijver’s bound BS (k, n) corresponds exactly to the Bethe approximation of its permanent,
  denoted PermBethe (G) (for the precise definition, see below). Gurvits calculates the functional
  corresponding to the Bethe free energy at the uniform point and shows that it evaluates exactly
  to BS (k, n) for regular graphs (see below for a proof).
  Below, we prove the following to show Step 1.
  Lemma 4.18. For any k-regular bipartite graph G, Schrijver’s bound BS (k, n) corresponds
  exactly to the Bethe approximation of its permanent, PermBethe (G).

  Proof. We aim to show that BS (k, n) = PermBethe (G).
  Step 1: Define the Matrix and Bounds. Let G be a k-regular bipartite graph. We consider
  the associated n × n normalized bi-adjacency matrix P . Since G is k-regular, P (i, j) = 1/k if
  an edge exists between i and j, and 0 otherwise. The matrix P is doubly stochastic (P ∈ Ωn ,
  i.e., Birkhoff polytope of doubly stochastic matrices).
  Since matrix P is normalized by k, Schrijver’s bound for the permanent of such a matrix P is




                                                 34
given by:
                                                                 (k−1)n
                                                          k−1
                                       BS (k, n) =
                                                           k
Note that the bound here is different from the one in Theorem 4.16 because of the scaling.
The Bethe approximation of the permanent, PermBethe (P ), is defined in the context of Gurvits’
paper as exp(maxQ∈Ωn CW (P, Q)) (see below for details).
Step 2: Simplifying the Bethe Approximation for Doubly Stochastic P. The functional
CW (P, Q) is defined as:
                         X                                               
                                                                            Q(i, j)
                                                                                     
           CW (P, Q) =       (1 − Q(i, j)) log(1 − Q(i, j)) − Q(i, j) log
                                                                            P (i, j)
                           i,j

When the matrix P is itself doubly stochastic (which is true for the normalized bi-adjacency
matrix of a k-regular graph), the maximum of CW (P, Q) is attained when Q = P .
Let’s evaluate CW (P, P ):
                         X                                                      
                                                                                   P (i, j)
                                                                                            
            CW (P, P ) =         (1 − P (i, j)) log(1 − P (i, j)) − P (i, j) log
                                                                                   P (i, j)
                           i,j
                         X
                       =       [(1 − P (i, j)) log(1 − P (i, j)) − P (i, j) log(1)]
                           i,j
                           X
                       =         (1 − P (i, j)) log(1 − P (i, j))
                           i,j

Therefore, the Bethe approximation is:
                                                                      Y
                  PermBethe (P ) = exp(CW (P, P )) =                        (1 − P (i, j))1−P (i,j)
                                                                      i,j

This quantity is denoted as F (P ) in the paper [55] (Equation 14).
Step 3: Evaluating F(P) for the k-regular Case. We calculate F (P ) for the specific matrix
P derived from the k-regular graph. Let us remind that the entries of P are P (i, j) ∈ {0, 1/k}.
We evaluate the product term by term:

  1. If P (i, j) = 0, the contribution is (1 − 0)1−0 = 1.

  2. If P (i, j) = 1/k, the contribution is:
                                                   1− 1                     k−1
                                                1         k           k−1         k
                                             1−               =
                                                k                      k

Since the graph is k-regular, every row (and column) of P has exactly k non-zero entries. Thus,
the total number of non-zero entries in the n × n matrix P is kn.
Step 4: Final Calculation. The total value of F (P ) is the product of the contributions of the
kn non-zero entries:                        "      k−1 #kn
                                               k−1 k
                                   F (P ) =
                                                 k



                                                      35
We simplify the exponent:
                                     k−1
                                         · kn = (k − 1)n
                                      k
Therefore,
                                                                 (k−1)n
                                                            k−1
                            PermBethe (P ) = F (P ) =
                                                             k
This exactly matches Schrijver’s bound BS (k, n).

Step 2: The Inequality. Gurvits ([55], Theorem 2.2 or 2 in Section 3 (Corollaries)) established
that the true permanent is lower-bounded by the Bethe approximation:

                                  perm(AG ) ≥ PermBethe (G).

Lemma 4.19 (Gurvits [55]). The true permanent is lower-bounded by the Bethe approximation.
Combining this with Step 1, we confirm that perm(AG ) ≥ BS (k, n).
Below, we use PermBethe (G) as permB (AG ), where AG is the bi-adjacency matrix of G.
Step 3: Strict Inequality (Condition for Equality). To prove the theorem, we must show
the inequality is strict (>). This requires characterizing the condition for equality. We rely on
the analysis provided by Vontobel [96].

1. Exactness on Forests (Sufficient Condition). The Bethe permanent is defined via the
minimization of the Bethe free energy, which corresponds to the fixed points of the Sum-Product
Algorithm (SPA). In Section VI-F (p. 17) of [96], under the heading “Relevance of Finite
Graph Covers,” Vontobel explicitly establishes the exactness of the SPA on cycle-free graphs:

     “If the NFG [Normal Factor Graph] N(θ) had no cycles, then the SPA could be used to
     exactly compute the partition function... the partition function ZG (N(θ)) = perm(θ)
     could be computed...”

By Definition 11 in [96], permB (θ) is defined as this partition function at the SPA fixed point.
Thus, if G is a forest, perm(θ) = perm(AG ) = permB (θ) = permB (AG ), where AG is the
bi-adjacency matrix of G.

2. Strict Inequality for Regular Graphs (k ≥ 2). Let G be a k-regular bipartite graph
with 2n vertices (n ≥ 1). We show that perm(AG ) > permB (AG ). First, we recall Theorem
49 in [96] (attributed to Gurvits, see the above lemma), which establishes the lower bound:
perm(θ) ≥ permB (θ). Indeed, in this case perm(θ) = perm(AG ) ≥ permB (θ) = permB (AG )a .
To prove strictness, we distinguish two cases based on the degree k.
Case 1: k = 2 (Disjoint Cycles). A 2-regular bipartite graph is a union of disjoint cycles.

   • Bethe Value: Using Example 41 (p. 14) and Lemma 40 in [96], Vontobel proves that
     for a cycle, permB (θ) = permB (AG ) calculates the maximum weight of a local matching.
     For a standard 2-regular graph (0-1 entries), this value is 1.

   • True Value: A cycle of length 2n has exactly two perfect matchings. Thus perm(AG ) ≥ 2.




                                               36
  Since 2 > 1, the strict inequality holds.
  Case 2: k ≥ 3 (Integrality Gap). We utilize a number-theoretic argument. The true
  permanent perm(AG ) counts the number of perfect matchings in G, so it must be an integer.
  In contrast, Vontobel [96] derives the explicit value of the Bethe permanent for a homogeneous
  k-regular matrix in Section VII-E (p. 21, Eq. 13):
                                                                      n
                                                         (k − 1)k−1
                                                     
                                      permB (θ) =                          .                             (3)
                                                            k k−2

  Again, in this case permB (θ) = permB (AG ), as a homogeneous k-regular matrix is indeed the
  bi-adjacency matrix AG of a k-regular bipartite graph G with 2n vertices. We observe that for
  any integer k ≥ 3, this value is not an integer:
                                         k−1
     1. The base fraction is b = (k−1)
                                   kk−2
                                        .

     2. Since k ≥ 3, the denominator k k−2 > 1. Let p be any prime factor of k.

     3. gcd(k, k − 1) = 1, so p does not divide k − 1. Thus, p cannot divide the numerator
        (k − 1)k−1 .

     4. Therefore, the fraction b is irreducible and non-integer. It follows that bn is never an
        integer for any n ≥ 1.

  Since perm(θ) = perm(AG ) is an integer and permB (θ) = permB (AG ) is strictly non-integer,
  they cannot be equal. Combining this with the lower bound perm(AG ) ≥ permB (AG ), we
  conclude:
                                  perm(AG ) > permB (AG ).


     a
      When G is a k-regular bipartite graph with 2n vertices, we can assume N (θ) = G. Hence, we only need to
  look at the bi-adjacency matrix AG of G.


Remark 4.20. While the AI generated a complete proof of this strict inequality (detailed above),
human review revealed that the core logic could be streamlined: because k and k − 1 are consecutive,
they are strictly coprime. This makes the Bethe approximation an irreducible, non-integer rational
for k ≥ 3. Since the true permanent must be an integer, it must be strictly greater than this rational.
                                                                                           √ n
Post Remark. Regarding Bethe approximation, the best achievement in this context is 2
deterministic polynomial time approximation of the permanent of nonnegative matrices [2]. More-
over, the solution of the asymptotic version of Friedland’s monomer-dimer conjecture, which is a
generalization of Schrijver’s bound on matching of size pn for 0 < p < 1 [57].

Further Discussion on Improvement (Q1)
While Theorem 4.17 proves that Schrijver’s bound is never tight for k ≥ 2, a deeper interpretation
of Q1 asks whether the asymptotic improvement factor Ck∞ (i.e., p(k, n)/BS (k, n)) is strictly greater
than 1.
    Case k = 2



                                                      37
   For k = 2, BS (2, n) = 1. A 2-regular bipartite graph is a disjoint union of even cycles. The
minimum number of perfect matchings occurs for a connected graph (a single cycle C2n ), which has
2 perfect matchings. Thus p(2, n) = 2.
                                           C2∞ = 2.
   Case k = 3
Theorem 4.21. For cubic graphs, the asymptotic improvement factor is strictly bounded below by
C3∞ ≥ 81
      32 ≈ 2.53125 > 1.

Proof.     1. Schrijver’s
                 n        Bound: Schrijver’s lower bound for k = 3 [87] is defined as BS (3, n) =
          (3−1)3−1     4 n
                    = 3 .
                        
            33−2

   2. The Exact Voorhoeve Lower Bound [97] (1979): It is a foundational result that the
      absolute minimum number of perfect matchings in any 3-regular bipartite graph with 2n
      vertices (n ≥ 3) is strictly bounded below by the exact differential formula:
                                                        n−3
                                                         4
                                           perm(G) ≥ 6
                                                         3
     (Note: Schrijver [87] utilized Voorhoeve’s [97] local differential tree-pruning arguments to
     generalize the base to all k, but absorbed the boundary conditions into O(1) terms for asymptotic
     simplicity. By retrieving the exact boundary constants from Voorhoeve’s original differential
     equation, we recover the explicit asymptotic surplus).

   3. Evaluating the Asymptotic Ratio: Evaluating the infimum ratio between the true deter-
      ministic limit and Schrijver’s bound as n → ∞:
                                                    n−3      3
                              perm(G)          6 43
                                                                       
             ∞                                                3        27   81
           C3 = lim inf min             ≥ lim     4 n
                                                        = 6      = 6     =    = 2.53125
                    n→∞ G BS (3, n)       n→∞                 4        64   32
                                                  3




Remark 4.22. The human researcher noted that the crucial insight in the AI’s derivation was the
rigorous extraction of the O(1) boundary constants. While Schrijver’s general asymptotic formulation
omitted these for simplicity, the AI recognized that retrieving Voorhoeve’s exact bound allows for the
recovery of the explicit asymptotic surplus.

Post Remark. The k = 3 bound corresponds to Gurvits’ bound above [54].

An AI-Proposed Spectral Roadmap
Below, the AI provides some attempts; To tackle the general k ≥ 4 case, the AI autonomously
recognized the limitations of local combinatorial methods, identifying a ’Harmonic Divergence’.
Remarkably, it proposed shifting the paradigm entirely to spectral graph theory. By invoking the
Ihara-Bass identity and the Kesten-McKay spectral measure for Ramanujan graphs, the AI reframed
the combinatorial roadblock as an analytic singularity, outlining a highly non-trivial roadmap for
future research (That said, if spectral graph theory (by considering Ramanujan/expander graphs)
plays a role, this is interesting).
    Proving Ck∞ > 1 remains a significant open problem. The graphs that minimize the number of
perfect matchings are expected to be those with the largest possible girth (i.e., Ramanujan/expander

                                                 38
graphs), as they locally resemble the infinite k-regular tree Tk , for which the Bethe approximation
(Schrijver’s bound) is exact (see below too).
    Heuristic arguments based on correlation decay suggest that the convergence of the normalized
log-permanent of a graph G to the tree value depends exponentially on the girth g(G). Since the
maximum girth grows logarithmically with n, this suggests that the ratio Perm(G)/BS (k, n) might
tend to a constant greater than 1. However, rigorously identifying the structure of the minimizing
graphs and proving these convergence rates are challenging open questions.


  The Attempt: By the Bethe Loop Calculus (Vontobel [96]), the ratio of the true permanent to
  Schrijver’s bound is a cycle gas partition function:
                                  perm(G)       X
                                            =1+   (k − 1)−|E(S)|
                                  BS (k, n)
                                                   S∈E

  where E is the set of vertex-disjoint cycle unions.
  The difficulty: In Ramanujan graphs, g(n) ≈ 2 logk−1 (n) → ∞. Thus, the weight of any indi-
  vidual shortest cycle becomes (k − 1)−2 logk−1 n = n12 . As n → ∞, individual cycle contributions
  vanish to zero. If one naively sums all cycles, the number of cycles of length ℓ in a regular graph
                                 ℓ
  grows asymptotically as (k−1)
                              ℓ    . When we sum the expected weights of all cycles to find the gap,
  we get:
                      X∞                            X (k − 1)ℓ               X1
                           Count(ℓ) · Weight(ℓ) ≈               (k − 1)−ℓ =
                                                            ℓ                    ℓ
                    ℓ=g(n)                          ℓ                         ℓ

  This yields the divergent Harmonic Series ( ℓ → ∞). Thus, local combinatorial correlation
                                                  P1
  decay fails to bound the n → ∞ limit, trapping researchers in an analytic divergence.
  The remaining open question is the exact asymptotic value of Ck∞ for k ≥ 4. Overcoming
  the Harmonic Divergence requires moving from standard Combinatorics to Spectral Graph
  Theory and the geometry of Zeta Functions.

  The Crux: The Ihara Zeta Singularity By the Ihara-Bass identity, the infinite cycle sum
  for the Permanent on regular graphs can be analytically continued as the reciprocal determinant
  of the Non-Backtracking Matrix B:
                                                             −1/2
                              perm(G)
                                              
                                                        1
                                        ∝ det I −          B
                              BS (k, n)              k−1
  The gap preventing the completion of the general proof is a spectral singularity. For any k-regular
  graph, the matrix B possesses a trivial Perron-Frobenius eigenvalue of λ = k − 1 corresponding
  to traversing all edges. Substituting this fundamental eigenvalue into the determinant yields:

                                           det(I − I) = 0

  The theoretical limit Ck∞ resides exactly at this 0/0 spectral singularity. Attempting to pass the
  limit locally without deflating this pole results in a harmonic explosion.
  Because resolving this singularity requires theorems on the spectrum of the Non-Backtracking
  matrix (e.g., the Alon-Boppana theorem, see [78], and the Kesten-McKay laws [65, 75]), which
  are non-elementary, this portion of the conjecture must remain an identified gap, ready for
  future spectral exploration.



                                                  39
  Note that the Ihara-Bass identity relates the non-backtracking matrix B to the adjacency matrix
  A via det(I − uB) = (1 − u2 )(k−2)n det(I − uA + u2 (k − 1)I). Evaluating the second determinant
  at the Bethe pole u = k−1
                          1
                             yields det(I − k−1
                                              1      1
                                                A + k−1            k−1 ). The factors corresponding
                                                        I) = det( kI−A
  to the eigenvalues λ of A are thus k−1 .
                                      k−λ

  The remaining limit will be determined by integrating the non-trivial eigenvalues over the
  Kesten-McKay spectral measure [65, 75], µKM (λ) of the infinite k-regular tree:
                                             Z 2√k−1               
                                         1                    k−λ
                            ln(Ck∞ ) ∝ −        √    ln                 dµKM (λ)
                                         2    −2 k−1          k−1

  By the Alon-Boppana
                 √        theorem,
                                 √ the non-trivial eigenvalues of high-girth graphs are strictly
  bounded by 2 k − 1. Since 2 k − 1 < k for all k ≥ 3, this absolute spectral gap ensures the
  remaining integral is strictly positive. However, this method merely confirms that Schrijver’s
  bound is exact on the infinite tree. Therefore, we need to write the discrete spectral sum for
  finite graphs (indeed, Ramanujan/expander graphs) with 2n vertices more accurately. This is a
  challenging problem for future work.


Post Remark. It turns out that the AI’s suggestion for a strategy to shift the paradigm to spectral
graph theory was an important factor for the solution of the Kadison-Singer problem by Marcus,
Spielman, and Srivastava (MSS) [73], which is, perhaps, one of the most important breakthroughs in
21st-century mathematics.
    Indeed, there is a similar flavor in the first paper of MSS’s work on Ramunajan graphs [72]. It
is worth noting that, rather than spectral graph theory and linear operators, MSS took a different
direction: real stability, which eventually led to a solution of the Kadison-Singer problem [73].
    It is surprising that, given that their work is not directly connected to counting perfect matchings
in regular bipartite graphs, the AI has already identified one of the most successful approaches in
mathematics of the 21st century. That is, the last question: we need to write the discrete spectral
sum for finite graphs (indeed, Ramanujan/expander graphs) with 2n vertices more accurately.
    Thus, this suggestion appears highly promising, given the prior success.




                                                   40
5     Using an AI-integrated IDE to “vibe-code”
In this section, we explore a different modality of interaction: embedding an LLM directly into a
LaTeX integrated development environment (IDE). This setup allows the researcher to act as a
high-level orchestrator while the AI autonomously drafts and refines technical proofs, effectively
"vibe-coding" a research paper from scratch.

5.1    Search vs. Decision in S2P
Written by Lance Fortnow.

Problem Context
The complexity class S2P represents problems solvable by a game between two competing provers. A
fundamental question is the relationship between the decision version (does a strategy exist?) and
the search version (find the strategy). It was known that decision is in ZPPNP (Cai 2001), but the
status of search was unclear.

AI Contribution
The researcher used an AI-powered IDE to write a paper on this topic from scratch.

    • "Vibe-Coding" a Paper: The researcher provided high-level prompts (e.g., "Plan a paper
      showing finding an S2P witness is equivalent to TFNPNP ").

    • Autonomous Proof Discovery: The AI independently generated the proof of the main
      equivalence.

    • Self-Correction: When the AI made an incorrect assumption in a corollary (assuming a
      containment that is open), the researcher pointed it out, and the AI immediately corrected the
      proof to use a reduction instead.

Experiment Narrative
The story starts with a talk by Purdue philosophy of science professor Eamon Duede [31]. Duede
argued that if artificial intelligence makes writing papers much easier, researchers will publish less
important research results. He worried about an explosion of AI-generated mediocre research papers,
but I saw the chance to get research out there that wouldn’t be there otherwise. AI itself can help
sort through the papers.
    But how about the premise itself, can AI simplify writing a quality paper, especially one that
has a result that might not have otherwise been published? So I picked one of my theorems that I
never wrote up and decided to try it out myself.
    In short, the process worked even better than I expected. I created the paper [43] with eight
prompts, not counting requests to compile. Surprisingly, it came up with the proof of the main
result on its own though it did assume something it shouldn’t have for the corollary, which went
away when I pointed it out.
    I give the detailed discussions below followed by a few lessons. At the end, I give an informal
description of the paper itself for those so inclined.




                                                 41
Details of the Process
I used Google Antigravity, an AI integrated development environment, with Gemini 3 Pro as the AI
model. I had successfully used Antigravity to fix some old links on my blog, so why not try it for
this paper? I used an IDE instead of a chatbot as I see LATEX as code that produces a paper.
    Below is a transcript between myself and Antigravity, lightly edited for clarity. The plan.md
and paper.tex files mentioned below are available in a GitHub repository [44].



     Let’s plan a paper showing that finding a S2P witness is equivalent to TFNPNP . The paper’s
     author is Lance Fortnow (me) and should be written in my style.


          I’ve drafted a plan for the paper, outlining the argument that finding an S2P witness is
          equivalent to TFNPNP . The plan is saved in plan.md.
          The core argument rests on two directions:

             1. S2P -Search ∈ TFNPNP : This is the straightforward direction. Verifying a witness
                (strategy) requires checking a universal quantifier (∀z P (x, y, z)), which is a coNP
                query. Since S2P guarantees a witness always exists, the problem is total.
             2. TFNPNP ⊆ S2P -Search: This is the main technical contribution. We need to show
                that any total search problem with an NP-oracle verifier can be reduced to the game-
                theoretic setting of S2P . This likely involves encoding the PNP verification circuit into
                the symmetric alternation structure.

          Next Steps
              • Review the Plan: Does the structure in plan.md look right to you?
              • Start the Draft: I can initialize a paper.tex file with this structure and your standard
                preamble.
              • Flesh out the Proofs: We can start sketching the reduction for the hard direction
                (TFNPNP ⊆ S2P -Search) in more detail.




    Not a bad start and it has the right ideas for the proof. But it doesn’t mention Cai’s work or the
search versus decision angle.




                                                     42
     Don’t forget to cite Cai’s paper that S2P is in ZPPNP . Add as a corollary that reducing
     search to decision for S2P would put ΣP
                                           2 ∩ Π2 in ZPP
                                                 P       NP
                                                            .


          I’ve updated the plan to include the corollary and the citation for Jin-Yi Cai’s paper.

          Updates
                • Section 4: Added the corollary: “If search reduces to decision for S2P , then ΣP    P
                                                                                                 2 ∩ Π2 ⊆
                  ZPP .”
                      NP


                • References: Added “Cai, J.-Y. (2001). S2P ⊆ ZPPNP .”

          The plan is now updated in plan.md. Ready to proceed with drafting the content whenever
          you are.


     Mention the corollary in the abstract, and note the stark difference between search and
     decision.


          I’ve updated the abstract in plan.md to include the corollary and emphasize the stark
          difference between the search and decision complexities of S2P , specifically referencing Cai’s
          result. The plan is now fully updated with your requirements. Would you like to proceed
          with creating the LaTeX file for the paper?


     Proceed.


          I’ve created the paper.tex file with the content we discussed. It includes the abstract,
          introduction, preliminaries, the equivalence proof sketch, the corollary regarding search-to-
          decision, and the references. You can now compile this LaTeX file to generate the PDF.
          Would you like me to try and compile it for you (if a LaTeX environment is available), or is
          there anything else you’d like to add to the paper first?




    I had expected to have to walk through the proof with the IDE, but it came up with the proof
on its own. That surprised me. It isn’t a technically difficult theorem but it has never been written
up before. But there was a mistaken assumption in the corollary.




                                                      43
     It’s open whether ΣP
                        2 ∩ Π2 ⊆ S2 . The point is that Σ2 ∩ Π2 can be reduced to TFNP
                             P    P                      P    P                       NP
                                                                                         .


          I’ve corrected the proof in paper.tex. It now correctly states that the search problem
          for ΣP2 ∩ Π2 is in TFNP
                      P             NP
                                       , which (via our main result) connects it to S2P -Search and
          subsequently ZPP . Is there anything else you’d like to refine in the paper?
                            NP




   That’s all it took to fix the proof of the corollary. Still Gemini got a little lazy in the write up.


     Avoid statements like “it is known” and put in details instead.


          I’ve expanded the proof in paper.tex to explicitly detail why the search problem for ΣP2 ∩Π2
                                                                                                      P

          falls into TFNP , replacing the “it is known” statement. The proof now walks through the
                          NP

          definitions of membership in ΣP2 and Π2 , the existence of witnesses for either case, and the
                                                 P

          verification complexity using an NP oracle. Is there anything else you’d like to modify or
          add?


     Similarly give the details of predicate Q.


          I’ve updated the paper with the detailed construction of the predicate Q and the logic for
          the reduction. This should make the proof much more rigorous.
          The paper now contains:
             1. Equivalence of S2P -Search and TFNPNP .
             2. Detailed reduction construction.
             3. Corollary connecting search-to-decision for S2P with ΣP    P
                                                                      2 ∩ Π2 ⊆ ZPP
                                                                                  NP
                                                                                     .
             4. Corrected proof for the corollary.
          Is there anything else you’d like to refine?




    The paper at this point was pretty well written but I wanted to change the emphasis to search
versus decision.




                                                     44
 Change the title to “Search versus Decision for S2P ” and adjust the abstract and introduction
 appropriately.


      I have read paper.tex and understood the necessary changes. Now I am creating the
      implementation plan. I have created an implementation plan to update the paper’s title,
      abstract, and introduction. Please review it. I have verified the changes in paper.tex.
      The title, abstract, and introduction have been correctly updated. Now I am creating
      the walkthrough artifact. I have updated the paper’s title, abstract, and introduction as
      requested. You can review the changes in paper.tex.




I had been using a separate LATEX editor to compile paper. Maybe I didn’t need to.


 Can you convert the tex file to pdf?


      I have successfully compiled paper.tex to paper.pdf. You can find the output at paper.pdf.




The citations weren’t going to the latest journal versions.


 Check Google Scholar that we have the latest versions of the papers in the citation.


      I have checked the citations on Google Scholar. I found updated journal versions for Canetti
      (IPL 1996) and Cai (JCSS 2007). Russell–Sundaram (1998) and Megiddo–Papadimitriou
      (1991) are already correct. I found updated journal versions for Canetti and Cai. I have
      created a plan to update the citations. Please review it. I have verified the updated citations
      in paper.tex. They are correct. I have updated the citations for Canetti and Cai to their
      journal versions and recompiled the paper. You can check paper.pdf for the latest version.




Finally I should come clean that I had AI write this paper.


 Add an acknowledgment section: “While the results are fully due to the author, this paper
 was generated using the large language model Gemini 3 Pro with prompting from the author.
 The author takes full responsibility for its contents.”


      I have added the acknowledgment section and recompiled the paper. You can check paper.pdf
      for the final version.




                                                 45
   And that’s how I "vibe-coded" a research paper in eight prompts, not counting the two used to
compile. I did some light editing afterwards to get it ready for the arXiv submission but I didn’t
need to.

Lessons
I did this as an experiment on a result that may never have seen the light of day otherwise, and
I was fully open about how I had AI write the paper. Nevertheless, it felt wrong, like I cheated
somehow. I felt a similar way when I first used LATEX in the 1980s, a paper that looked far better
than it deserved. After that all papers looked the same, and maybe with AI all papers will read the
same.
     The experience felt similar to working with a graduate student writing their first research paper.
I would just make suggestions until they got it right.
     In AI coding you can get better behavior when you give detailed instructions using markdown
files like the plan.md that Gemini created for me. I could have taken the approach by creating
a markdown file myself, instead of having AI create one for me. I could have a separate file that
describes how I personally like papers written. This might lead to a system where you write
mathematical papers in LATEX without ever looking at the LATEX produced and the markdown files
become the true paper source.
     Is low-friction research paper writing good for science? It’s a question that philosophers like
Duede contemplate. But I see no one suggesting we go back to quill and scroll.

Informal Theorem Description
The complexity class SP2 [19, 83] can be thought of as an exponential-sized 0-1 matrix with the
promise that either (a) there is a row of all ones or (b) a column of all zeros (you can’t have both).
The decision problem for SP2 is to tell whether (a) or (b) holds, and the search problem is to find the
appropriate row or column. An NP oracle is an extra capability to ask about existential questions,
like does a specified row have a zero. Jin-Yi Cai [18] showed that the decision problem can be solved
by a randomized algorithm with access to an NP oracle. But his proof did not necessarily find
the row or column. The new result shows that the search problem is equivalent to a likely harder
problem, total search problems verifiable with access to an NP oracle, a class called TFNPNP .




                                                  46
6     Autonomous Verification and Neuro-Symbolic Loops
Standard text-based chat interfaces are fundamentally limited by the AI’s tendency to hallucinate
during long symbolic derivations. This section highlights a methodological leap: embedding the AI in
an automated "neuro-symbolic" loop where it autonomously writes and executes code to numerically
verify its own mathematical hypotheses, effectively pruning its own invalid reasoning branches.

6.1    Physics: Cosmic String Spectra
Written by Michael P. Brenner, Vincent Cohen-Addad, and David P. Woodruff.

Problem Context
    Predicting the gravitational radiation emitted by cosmic strings requires solving a specific,
notoriously difficult integral over the sphere. Cosmic strings are hypothetical one-dimensional
topological defects that may have formed during symmetry-breaking phase transitions in the early
universe. The study of these strings as sources of gravitational radiation has seen renewed interest
following recent observations of a stochastic gravitational wave background by Pulsar Timing Arrays.
    A critical quantity in predicting this radiation is the power spectrum PN of the N -th harmonic
emitted by a cosmic string loop. For the well-studied class of Garfinkle-Vachaspati strings, the
power emitted at frequency ωN = 4πN/L (where L is the loop length) is governed by a core integral
I(N, α) evaluated over the unit sphere S 2 :

                                                 32Gµ2
                                          PN =         I(N, α)                                           (4)
                                                 π3N 2
where µ is the mass per unit length. The core integral I(N, α) is defined as:

                                    [1 − (−1)N cos(N πe1 )][1 − (−1)N cos(N πe2 )]
                            Z
                 I(N, α) =       dΩ                                                                      (5)
                              S2                  (1 − e21 )(1 − e22 )

where e1 = r̂ · â and e2 = r̂ · b̂ are projection factors. The vectors â and b̂ are three-dimensional unit
vectors characterizing the string trajectory, and the problem is defined entirely by the loop opening
angle α between them.
    Evaluating this integral has been a roadblock in theoretical astrophysics. The integrand features
severe singularities at the poles (e1,2 = ±1). Furthermore, as N grows large, the integrand in
angular coordinates becomes highly oscillatory, rendering standard numerical integration grids highly
unstable and computationally prohibitive. Analytical expansions (e.g., using standard Legendre
polynomials) are exceedingly difficult due to the non-matching weight functions (1 − e2 )−1 in the
denominator. Previous human and AI-assisted efforts yielded only partial solutions for odd N or
asymptotic approximations for large N . Finding a unified, exact, closed-form analytical solution for
arbitrary loop geometries remained a significant open problem. We do give an exact closed form
analytical solution (with an infinite number of terms), though we do not give a simple expression for
the asymptotics at large N for any α. While the formulae discovered are all in the form of infinite
expansions of known functions, this can be used to derive effective asymptotic formulae.
    We have further developed the initial results here in followup work [14].

AI Contribution
    To tackle this integral, we deployed a hybrid neuro-symbolic system combining the Gemini Deep
Think reasoning engine with a systematic Tree Search (TS) algorithm. This interaction highlighted
three interesting capabilities of modern AI as an active research partner:

                                                    47
   • Automated Pruning and Grounded Verification: To bridge the gap between symbolic
     mathematical manipulation and ground-truth verification, we utilized an automated numerical
     feedback loop. At each node in the search space, the model proposed an intermediate
     mathematical expression in LATEX and autonomously generated an executable Python function
     to evaluate it. The TS algorithm scored the node against a high-precision numerical baseline.
     If the proposed expression exhibited numerical instability (e.g., catastrophic cancellation) or
     divergence, the evaluation harness caught the exception and injected the Python traceback
     directly back into Gemini’s context window. This successfully pruned over 80% of the
     approximately 600 candidate branches early, keeping the LLM strictly grounded in mathematical
     reality.

   • Methodological Diversity via Negative Prompting: The system was highly adept at
     finding alternative mathematical routes. Once the model successfully found a valid solution
     path, we utilized negative prompting to force broader methodological exploration. By explicitly
     instructing the model, “One way of solving this problem is to use the following method... DO
     NOT use this method. Reflect on your plan and try a different plan,” the AI autonomously
     discovered six distinct analytical methods to solve the integral.

   • Hierarchical Refinement and Self-Correction: The most interesting moment came during
     the final verification stage. The TS framework initially produced an exact solution for our
     preferred method (Method 6) expressed as an infinite tail sum of coefficients. We then passed
     this intermediate result to a larger, unconstrained version of Gemini Deep Think, asking it
     to rigorously verify the proofs and search for further simplifications. This advanced model
     independently spotted an algebraic oversight in a related recurrence (Method 5, where a
     denominator dependency had been missed). By correcting this, it established a mathematical
     equivalence between the two methods, and recognized that a localized recurrence structure
     allowed the infinite tail sum to telescope into a finite, closed-form expression.

Technical Details: The AI’s Discovery Process
    To demonstrate the depth of the AI’s mathematical exploration, we detail the progression of the
six methods it discovered. The AI first recast the integral into the following general form over the
unit sphere S 2 :                       Z
                              I(N, α) =                dΩ(u) fN (u · z) fN (u · a)               (6)
                                                  S2
where z and a are unit vectors with z · a = cos α. The function fN (t) is defined as:

                                         1 − (−1)N cos(N πt)
                            fN (t) =                         ,               t ∈ [−1, 1].        (7)
                                               1 − t2
For convergence at the poles t = ±1, N must be an integer, and we define A = N π.

Class I: Monomial Basis Approaches (The Unstable Solutions)
    The AI first explored expanding fN (t) in a Taylor series monomial basis {t2k }. It found the
coefficients d2k by expanding the right-hand side using the cosine power series:
                                   ∞                                   ∞
                                   X                                   X (−1)m (At)2m
                              2
                        (1 − t )         d2k t   2k
                                                      = 1 − (−1)   N
                                                                                            .    (8)
                                                                                 (2m)!
                                   k=0                                 m=0




                                                           48
                                                                                      k   2k
Matching coefficients of t2k yields the recurrence d2k − d2k−2 = −(−1)N (−1) A
                                                                          (2k)! , implying:

                                                 k
                                                 X (−1)j A2j
                             d2k = −(−1)N                      + (1 − (−1)N ).                              (9)
                                                       (2j)!
                                                 j=1

Substituting this expansion into the integral yields a double sum:
                         ∞ X
                         X ∞                                             Z
             I(N, α) =             d2k d2j J2k,2j (α) where Jk,l (α) =        (u · z)k (u · a)l dΩ.       (10)
                         k=0 j=0                                         S2


To evaluate the angular moments Jk,l (α), the AI discovered three separate sub-methods:
R Method      1: Generating Function Approach. The AI defined a generating function G(λ, µ) =
 S2 e
     λu·z+µu·a dΩ. Letting K = λz + µa and aligning the polar axis with K, the AI integrated to find:

                                                  eK − e−K      sinh K
                                   G(λ, µ) = 2π            = 4π        ,                                  (11)
                                                     K             K
where K 2 = λ2 + µ2 + 2λµ cos α. The AI then expanded sinh K/K:
                                      ∞
                                  X K 2s                ∞
                                               X (λ2 + µ2 + 2λµ cos α)s
                         sinh K
                                =            =                          .                                 (12)
                            K      (2s + 1)!            (2s + 1)!
                                     s=0               s=0
                                                         h            i
This allowed the AI to compute J2k,2j via differentiation ∂λ2k ∂µ2j G                , resulting in an explicit
                                                                             λ=µ=0
sum involving factorials and powers of cos α.
    Method 2: Gaussian Integral Lifting. Alternatively, the AI lifted the basic equation into R3
by introducing a Gaussian weight:
                                      Z
                                              2
                                M=        e−r (r · z)2k (r · a)2j d3 r.                      (13)
                                            R3

By switching to spherical coordinates r = ru, the radial integral separates and evaluates to
2 Γ(k + j + 3/2), implying M = 2 Γ(k + j + 3/2)J2k,2j . Simultaneously, applying the differential
1                                  1

operator identity (r · z) = ∂λ |λ=0 eλr·z directly to the standard Gaussian integral allowed the AI
                         2k   2k

to evaluate M analytically:
                                                        2
                                                        λ + µ2 + 2λµ cos α
                                                                           
                         M = π 3/2 ∂λ2k ∂µ2j       exp                       .                  (14)
                                             λ=µ=0              4

Equating the two representations of M isolates J2k,2j .
    Method 3: Hybrid Coordinate Transformation. TheP                AI’s third approach projected the
power series onto a Legendre basis P2m (t), expanding t2k = km=0 Tk,m P2m (t), where Tk,m are
known
P∞ analytical
         P∞         coefficients. Substituting this back into the Taylor expansion yielded fN (t) =
   m=0  (  k=m  d2k T k,m ) P2m (t).
    AI Self-Correction: While mathematically correct, the AI’s automated Python verification
routines revealed that all three Monomial methods were highly unstable. The calculation of the
Taylor coefficients d2k involves alternating sums of very large numbers. For large N , this triggers large
O(eN π ) cancellation, rendering the methods computationally intractable without arbitrary-precision
libraries. Recognizing this, the AI autonomously pivoted to Spectral methods.


                                                       49
Class II: Spectral Basis Approaches (The Pivot to Stability)
P The AI recognized that because I(N, α) is a spherical self-convolution, expanding fN (t) =
  C2j P2j (t) (where P are standard Legendre polynomials) allows the direct application of the
Funk-Hecke Convolution Theorem to diagonalize the integral:
                                                  ∞    2
                                                  X  C2j
                                  I(N, α) = 4π             P2j (cos α).                               (15)
                                                    4j + 1
                                                  j=0

The problem now reduced to finding the Legendre coefficients C2j efficiently without relying on the
unstable Taylor series. The AI found two stable O(N ) methods to do this:
    Method 4: Spectral Galerkin (Matrix Method). The AI formulated                  a linear system by
defining g(t) = (1 − t2 )fN (t) = 1 − (−1)N cos(At). Substituting fN = j C2j P2j and projecting
                                                                                P
onto a test function P2i yielded:
                         X       Z 1                             Z 1
                             C2j     (1 − t2 )P2i (t)P2j (t)dt =     P2i (t)g(t)dt.                (16)
                          j       −1                                 −1

This forms a matrix equation GC = b. Using the recurrence identity t2 Pl = Al Pl+2 + Bl Pl + Cl Pl−2 ,
the AI deduced an explicit formula for the matrix elements Gij and proved that G is a symmetric
positive-definite tridiagonal matrix. The RHS vector b was evaluated using the Bauer plane wave
expansion to yield bi = 2δi0 − 2(−1)N +i j2i (A), allowing the coefficients to be solved with high
stability.
    Method 5: Spectral Volterra (RecurrenceR Method). Pushing further, the AI derived a
                                                        1
forward recurrence for C2j . Starting from Cl = 2l+1
                                                  2    −1 fN (t)Pl (t)dt = 2 γl , the AI multiplied the
                                                                            2l+1

Legendre differential equation by fN (t) and integrated by parts:
                                             Z 1
                                                  ′
                                l(l + 1)γl =     fN (t)(1 − t2 )Pl′ (t) dt.                        (17)
                                               −1

Differentiating (1 − t2 )fN (t) = 1 − (−1)N cos(At) gives (1 − t2 )fN  ′ (t) = (−1)N A sin(At) + 2tf (t).
                                                                                                      N
Substituting this back into the integral brilliantly split the result into two tractable terms, T1 (l) and
T2 (l):
                                 Z 1                             Z 1
                                                        ′
                    l(l + 1)γl =          N
                                      (−1) A sin(At)Pl (t)dt +        2tfN (t)Pl′ (t)dt .              (18)
                                   −1                             −1
                                 |             {z            } |           {z         }
                                             T1 (l)                       T2 (l)

The AI evaluated T1 (2j) via spherical Bessel functions as −2A2 (−1)N +j j2j (A). It expanded T2 (2j)
into a telescoping sum structure, yielding a clean O(N ) forward recurrence:
                                   4(2j 2 − j)
                                               C2j = T1 (2j) + SR (j),                                (19)
                                     4j + 1
                 Pj−1
where SR (j) =     m=0 (8m + 2)γ2m is a running sum of lower-order coefficients.

Class III: The Exact Analytic Solution (Method 6)
    While Methods 4 and 5 provided stable algorithmic resolutions, the crowning achievement was
finding an exact analytic closed-form solution via the Gegenbauer Method.
    The AI insightfully chose to expand fN (t) not in standard Legendre polynomials, but in the
                                    (3/2)
basis of Gegenbauer polynomials C2m (t):
                                                  ∞
                                                             (3/2)
                                                  X
                                       fN (t) =         b2m C2m (t).                                  (20)
                                                  m=0


                                                      50
It realized that Gegenbauer polynomials are orthogonal with respect to the specific weight w(t) = 1−t2 .
This specific weight miraculously cancels the problematic singular denominator in fN (t) when
determining the coefficients by orthogonality:
                                Z 1
                                      1 − (−1)N cos(N πt)
                                                           
                             1                                (3/2)
                     b2m =                        2
                                                             C2m (t) (1 − t2 ) dt,                 (21)
                            h2m −1            1−t                     | {z }
                                    |          {z          }            weight
                                               fN (t)

                                                                                  (3/2)
where h2m is the standard normalization constant. By using the identity Ck (t) = Pk+1     ′  (t) and
integrating by parts, the boundary terms vanish (because the numerator 1−(−1) cos(N πt) evaluates
                                                                                 N

to 0 at t = ±1), and the integral elegantly reduces to the Fourier transform of Legendre polynomials:
                                                                 4m + 3
                           b2m = −A(−1)N +m j2m+1 (A)                         .                     (22)
                                                             (2m + 1)(2m + 2)
                        (3/2)
   Using the expansion C2m (t) = m  j=0 (4j + 1)P2j (t), the AI then relates the Legendre coefficients
                                  P
C2j (from Equation 15) to these Gegenbauer coefficients via a tail sum:
                                                           ∞
                                                           X
                                        C2j = (4j + 1)             b2m ,                            (23)
                                                           m=j

noting a critical property: when j = 0, the sum of all Gegenbauer coefficients simply equals C0 :
                                                     ∞
                                                     X
                                            C0 =           b2m .                                    (24)
                                                     m=0

    Finally, during the hierarchical refinement
                                                  phase,
                                                          the advanced Gemini model exploited a partial
fraction decomposition of 1−t2 = 2 1−t + 1+t to telescope the series and find an exact analytical
                              1     1    1       1

expression for C0 :

                           1 1 1 − (−1)N cos(N πt)              1 2N π 1 − cos(x)
                             Z                                   Z
                     C0 =                                 dt =                    dx.              (25)
                           2 −1           1 − t2                2 0        x

   Recognizing
        Rz     this final integral as the standard definition of the generalized cosine integral function
Cin(z) ≡ 0 1−cos(t)
               t    dt, the AI produced the final, exact closed-form solution:

                                              1
                                          C0 = Cin(2N π).                                           (26)
                                              2
Combining, we obtain
                                               j−1
                                                                                          !
                                               X                         4m + 3
              C2j = (4j + 1) C0 + A(−1)N             (−1)m j2m+1 (A)                          .     (27)
                                                                     (2m + 1)(2m + 2)
                                               m=0




Summary of Discovered Methods
   The table below summarizes the AI’s discoveries and their computational tradeoffs. This AI-driven
work provides a stable, closed-form analytic solution for the spectral coefficients.
   We refer the reader to [14] for our more recent developments.

                                                     51
Method        Core Technique                  Complexity       Numerical Stability
1, 2, 3       Monomial Expansions             O(N 2 )          Unstable (Catastrophic Cancellation)
4             Spectral Galerkin Matrix        O(N )            Stable (Tridiagonal SPD Matrix)
5             Spectral Volterra Recurrence    O(N )            Stable (Forward Step Recurrence)
6             Gegenbauer Expansion            O(1)             Stable (Exact Analytic Closed-Form)

Table 2: Comparison of AI-discovered methods for evaluating the cosmic string radiation integral
I(N, α).

7     Algorithms and Bounds
In this section we see the AI acting as an algorithmic optimizer—tightening mathematical bounds,
removing logarithmic factors, and discovering exact optimal constants.

7.1       Graph Theory: Biclique Partitions
Written by Benjamin Przybocki and Bernardo Subercaseaux.

Problem Context
Biclique partitions are a well-studied topic in graph theory with applications to secret sharing, circuit
design, and graph compression. Together with Andrew Krapivin and Nicolás Sanhueza-Matamala,
we recently proved that every n-vertex graph admits an integral biclique partition of weight at most
( 12 + o(1))n2 / lg(n), matching an information-theoretic lower bound [69]. However, in the context of
cryptographic secret sharing, fractional solutions to the biclique partition problem are also studied.
Previous work by Csirmaz, Ligeti, and Tardos [27] had shown a fractional upper bound with a
constant of 12 , and a fractional lower bound of 0.265. Since we were able to match their fractional
upper bound with integral solutions, a natural question was whether we could use our techniques to
push the fractional upper bound strictly below 12 .

AI Contribution
We had our paper fed to the model and asked it to resolve the open problem. While its initial proof

    Please try to improve the paper by identifying and solving the open problem from it.

    <Math rigor prompt>


attempt had errors, it ultimately led us to solve the problem by providing a crucial insight on how
one of our lemmas could be repurposed in a way we had not seen.
    • Proof Strategy: The AI suggested a strategy based on partitioning vertices into “good”
      (degree close to n/2) and “bad”. We had considered this before, so we had some understanding
      of the technical hurdle the AI would need to overcome to make it work.
    • Overcoming the Hurdle: In the AI’s proof attempt, it pointed out a crucial idea that
      allowed us to get better control on the proportion of bad vertices. This insight was not obvious
      to us as it was a consequence of a construction we had used for a different purpose.

                                                    52
   • From Insight to Proof: The AI’s initial proof attempt had errors (incorrect constants
     and Taylor approximations), but the core idea—that “bad” vertices actually help reduce the
     partition weight—was correct.

Technical Details: Fractional and Integral Biclique Partitions
Definition 7.1. Given a graph G, a fractional biclique partition is a function B : B → [0, 1], where
B is the set of all complete bipartite subgraphs of G, such that for all e ∈ E(G), we have
                                         X
                                             1[e∈B] · B(B) = 1.
                                            B∈B

The weight w(B) of such a partition is w(B) :=
                                                    P
                                                      B∈B B(B) · |V (B)|. A fractional biclique partition
B is integral if B(B) ∈ {0, 1} for all B ∈ B.

The following notation will be useful for discussing the problem at hand.

Definition 7.2. Given a graph G, let BP(G) (resp., BP∗ (G)) be the minimum weight of an integral
(resp., fractional) biclique partition of G. Then, given n ≥ 1, let

                  BP(n) :=      max         BP(G)   and   BP∗ (n) :=      max         BP∗ (G).
                             G, |V (G)|=n                              G, |V (G)|=n

We had recently proven the following theorem regarding optimal integral biclique partitions:
                                                                                                           2
Theorem 7.3 (Krapivin, Przybocki, Subercaseaux, and Sanhueza-Matamala [69]). BP (n) ∼ 12 · lgn n .

In turn, the best bounds for fractional biclique partitions were:
                                                                           2                           2
Theorem 7.4 (Csirmaz, Ligeti, and Tardos [27]). (0.265 − o(1)) lgn n ≤ BP ∗ (n) ≤ ( 12 + o(1)) · lgn n .

   Importantly, Csirmaz, Ligeti, and Tardos also proved that on graphs of large minimum degree, a
better upper bound can be obtained:

Theorem 7.5 (C.L.T. [27]). Let p ∈ [0, 1] be a fixed constant, and let G be a graph on n vertices
such that deg(v) ≥ p · n for every v ∈ V (G). Then,

                                                                        n2
                                 BP∗ (G) ≤ (0.725 · (1 − p) + o(1))         .
                                                                       lg n

   In particular, for any graph G with minimum degree at least 0.32n (such as a G(n, 12 ) graph,
w.h.p.), this gives an upper bound strictly better than Theorem 7.4. On the other hand, for graphs
whose edge density is far from 0.5, we also have an improved upper bound, even for integral biclique
partitions:

Theorem 7.6 (K.P.S.S.-M. [69]). Let γ ∈ (0, 1) be such that max{γ −1 , (1 − γ)−1 } = no(1) . Then,
                                                                        2
given a graph G of density γ, we have BP (G) ≤ ( 12 + o(1)) · h2 (γ) lgn n , where h2 (x) := −x lg x − (1 −
x) lg(1 − x) is the binary entropy function.

   Moreover, we also proved a similar result that applies when the degree of every vertex is bounded
away from 0.5, even if the global density is close to 0.5:

Theorem 7.7 (K.P.S.S-M. [69]). Let γ̇ ∈ (0, 1) be such that γ̇ −1 = no(1) . Then, given a graph G
                                                                                   2
such that min{d(v)/n, 1 − d(v)/n} ≤ γ̇, we have BP (G) ≤ ( 21 + o(1)) · h2 (γ̇) lgn n .

                                                     53
    Therefore, in light of Theorems 7.5 to 7.7, if it is not possible to improve the 12 constant from
Theorem 7.4, then the problematic graphs must have a particular structure: (i) a constant fraction
of vertices of degree at most 0.32n, (ii) edge density 0.5, and (iii) a constant fraction of vertices
whose degree is approximately n2 .
    Naturally, we thought of decomposing problematic graphs into different pieces that could be
separately handled by the three aforementioned results. Roughly, the idea was to partition the
vertices of a given graph into those whose degree is close to n2 (call these Vgood ) and those whose
degree is far from n2 (call these Vbad ). Our hope was to use Csirmaz, Ligeti, and Tardos’s result
to construct a biclique partition for G[Vgood ] and then try to construct a biclique partition for the
remaining edges using a different method. But, in order for this to work, we needed Vbad to be a
small proportion of the vertices, and it did not seem possible to ensure this with our strategy. We
therefore left this as an open problem.
    The AI model was fed our paper, and at our suggestion, was asked to resolve this open problem.2
The proof attempt generated by the AI was similar to the strategy outlined in the previous paragraph,
which was impressive given that we did not share our ideas with the AI. But there was one crucial
difference. The AI noticed that the construction we used for Theorem 7.7 actually implies that we
can improve the 12 constant from Theorem 7.4 whenever the average of | deg(v)/n − 21 | is bounded
away from 0. We neglected to consider this ourselves, since Theorem 7.7, as stated here, is in fact a
corollary of a stronger theorem in our paper bounding the maximum number of bicliques any given
vertex belongs to; for this stronger result, it was necessary to assume that | deg(v)/n − 12 | is bounded
away from 0 for every vertex rather than merely on average.
    However, despite the promising high-level strategy, the AI’s proof attempt contained several
mistakes, which did not seem to be fixable by local modifications of the proof attempt at least
as written. For example, the AI asserted that some expression is ≈ 0.31966 when it is actually
≈ 0.13933, and it had a nonsensical asymptotic expression Ax + x3 /2 + O(x2 ), where x is a constant.
Nevertheless, the AI’s observation in the previous paragraph turned out to be exactly what we
needed to overcome the difficulties we had encountered in our first attempt, and we proved that
every n-vertex graph admits a fractional biclique partition of weight at most (0.4999 + o(1))n2 / lg(n).
We made no attempt to optimize the constant 0.4999; in fact, it seems to us that where the AI
went wrong is trying too aggressively to optimize the constant in its proof, which resulted in overly
complicated algebraic calculations that the AI struggled to accurately manipulate.

Final Proof For technical reasons, Theorems 7.6 and 7.7 require γ or γ̇ to not be too close to 0 or
1. For similar reasons, it is convenient to define a “clipped” version of the binary entropy function,
which allows us to state Lemma 7.9, a lemma corresponding to the AI’s central insight mentioned
above. The AI originally stated the lemma using the non-clipped binary entropy function, although
the lemma is incorrect when stated that way. Interestingly, when the AI was asked the provide a
rigorous proof of the lemma, it realized it could not be true as stated, although it did not discover
that the clipped binary entropy function provides a simple way to salvage it that suffices for its
application.

Definition 7.8. Let h2 (x) := −x lg x − (1 − x) lg(1 − x) be the binary entropy function, and let
h†2 : [0, 1] → [0, 1] be defined by
                                            (
                                    †        h2 (x)    if x ∈ [0.01, 0.99]
                                   h2 (x) =
                                             h2 (0.01) if x ̸∈ [0.01, 0.99].
   2
    Initially, the AI model tried a different open problem from our paper, but its response did not seem very promising
to us, and we were more interested in this problem anyway.


                                                          54
                                                                                    †
Lemma 7.9. Let G be an n-vertex graph, and let h̄ = h̄(G) := n1
                                                                              P
                                                                               v∈V h2 (deg(v)/n). Then,

                                                                      n2
                                                                
                                         ∗           h̄
                                     BP (G) ≤           + o(1)            .
                                                     2               lg n

   The proof of Lemma 7.9 is a relatively straightforward modification of the proof for Theorem 7.7,
which corresponds to [69, Theorem 26]. With it, the proof of the final result is surprisingly simple.
                                                 2
Theorem 7.10. BP∗ (n) ≤ (0.4999 + o(1)) · lgn n .

Proof. Let G be an arbitrary n-vertex graph. Let Vgood = {v ∈ V (G) | d(v) ≥ 0.37n} and
Vbad = V (G) \ Vgood . Then, note that
                                                                               
                  1                      1
                         h†2 (deg(v)/n) =     h†2 (deg(v)/n) +   h†2 (deg(v)/n)
                     X                       X                  X
          h̄(G) =
                  n                      n
                     v∈V                       v∈Vbad                         v∈Vgood
                                         1
                                        ≤ (|Vbad | · h2 (0.37) + |Vgood | · 1) .
                                         n
Thus, if |Vbad | ≥ n/100, then by Lemma 7.9,
                                                             2
                                                                                     n2
                           
                   ∗         0.02 · h2 (0.37) + 0.98          n
                 BP (G) ≤                            + o(1)       ≤ (0.4999 + o(1))      .
                                         2                   lg n                   lg n

    Therefore, we may assume that |Vbad | < n/100. Then, every vertex of G[Vgood ] has degree at
least 0.36|Vgood |, whence Theorem 7.5 implies

                                                                  n2                    n2
                BP∗ (G[Vgood ]) ≤ (0.725 · (1 − 0.36) + o(1))         = (0.464 + o(1))      .
                                                                 lg n                  lg n

Let H be the graph with V (H) = V (G) and E(H) = {e ∈ E(G) | e ∩ Vbad ̸= ∅}. It remains to
construct a fractional biclique partition for H. Note that |E(H)| ≤ |Vbad | · 0.37n ≤ 0.0037n2 , from
where the edge density of H is at most 0.0074 + o(1). Hence, by Theorem 7.6,
                                                      2
                                                                              n2
                                
                       ∗          h2 (0.0074)          n
                    BP (H) ≤                  + o(1)       ≤ (0.0316 + o(1))      .
                                       2              lg n                   lg n

Since, E(G) := E(H) ⊔ E(G[Vgood ]), we have

                                                                                         n2
                      BP∗ (G) ≤ BP∗ (G[Vgood ]) + BP∗ (H) ≤ (0.496 + o(1))                   .
                                                                                        lg n




                                                     55
7.2   Query Complexity: Local Search on General Graphs
Written by Simina Brânzei, Ioannis Panageas, Dimitris Paparas [13].

Problem Context
We analyze the query complexity of the abstract problem of finding a local minimum of a function
defined on a general graph using t rounds of interaction with the oracle. This theoretical model
captures optimization tasks such as training neural networks, where the goal is to minimize a loss
function, each “query” is an expensive loss evaluation, and batching queries is crucial for efficiency.
    Prior work [12] resolved the query complexity of local search in rounds for the d-dimensional
grid. However, the problem remained open for general graphs, which are essential for modeling
non-Euclidean geometries such as manifold discretizations.

AI Contribution
The AI was instrumental in obtaining the following results on the query complexity of local search
on arbitrary graphs:

   • A deterministic upper bound as a function of the number of vertices n, the number of rounds
     t, and the separation number s of the graph.

   • A randomized lower bound dependent on n and t.

    These results constitute a research paper [13], developed entirely by iterating with the AI via a
“scaffolded reasoning” process. Rather than asking the model to generate the paper from scratch,
we treated it as a junior research assistant: we defined the lemmas and tasked the AI with writing
the proofs, which we then rigorously verified and refined. We directed the model to expand unclear
sections and flagged issues where applicable. This approach can be characterized as a form of “vibe
proving”.

   • Algorithm Design: We tasked the AI with deriving an upper bound for two-round local
     search parameterized
                      √ by the graph’s separation number. The model synthesized a two-round
     algorithm with O( ns∆) queries and stated a supporting “Shattering Lemma” about separator
     decompositions.

   • Iterative Improvements: For all the upper and lower bounds, we guided the model to
     gradually generalize (e.g., obtain a lower bound for a tree in 2 rounds and then generalize to
     any graph in 2 rounds). We gave several relevant papers as context in all iterations.

   • Adversarial Hypothesis Testing: When we hypothesized a linear lower bound for local
     search in two rounds on constant-degree expanders, the AI refuted it by proposing a counter-
     algorithm (Randomized Parallel Steepest Descent) and demonstrating an upper bound of
     O(n/ log n) for it.

    Problem choice. We chose this problem for several reasons. One of the authors has expertise
on the topic of local search (with a prior paper that focuses on grids [12]). Investigating the query
complexity for general geometries was written in an NSF grant by this author. Moreover, one of
the journal reviewers of the paper on local search in rounds on grids [12] independently raised this
question. Pedagogically, the problem seemed ideal for a collaboration with a student, as it allowed
for a natural progression from simple cases—such as two-round search on trees—to general results.

                                                  56
    Strengths. The AI model demonstrated distinct strengths during our collaboration. One of
the key contributions was the model’s tailoring of the classical staircase construction to the round
setting. While the staircase technique is well-known, the model’s instantiation ensured that in the
hard distribution, every vertex is the (only) local minimum with equal probability. This created a
recursive structure where, at the end of each round, the set of viable candidates forms a smaller
instance of the original problem, enabling a clean inductive argument to go through. The elegance
of this structure was a very nice surprise.
     Weaknesses. The model also exhibited weaknesses, such as sometimes producing incorrect
proofs or conveniently mis-interpreting the question so that it could answer it. For instance, when
we first asked for a lower bound, it would often switch to proving an existential one. Specifically,
when queried about a lower bound for local search on graphs with n vertices and separation number
s, it created a “hard graph” for these parameters (such as a line where each vertex is connected to
a clique of size s). We also encountered occasional hallucinations of non-existent results. Finally,
when we prompted without suggesting graph features, the AI model gave upper bounds that were
less interpretable.

Model and Results
Let G = (V, E) be a connected undirected graph with vertex set V = [n] = {1, . . . , n}. Let f : V → R.
We call a vertex v ∈ V a local minimum if f (v) ≤ f (u) for every neighbor u of v. In the local search
problem, we are given G and oracle access to the values of f . The goal is to locate a local minimum
using a minimum number of queries, where a query at vertex v reveals f (v).
    Suppose the interaction with the oracle has t rounds. In each round j, the algorithm selects a
set of queries based on the outcomes of rounds 1, . . . , j − 1, submits them, and receives the answers.
The algorithm terminates after round t with a proposed solution.

Query Complexity. The deterministic query complexity is the minimum number of queries
required for an optimal deterministic algorithm to find a local minimum on a worst case instance.
   The randomized query complexity is the minimum worst-case number of queries required by a
randomized algorithm to compute the function with probability at least 9/10 for every input3 .

Graph Features. Let ∆ be the maximum degree of G, and let dist(u, v) denote the shortest-path
distance between u, v ∈ V . Given a parameter 1/2 ≤ α < 1 and an integer s ∈ N, a subset S ⊆ V
is an (s, α)-separator of G if there is a partition of V into disjoint sets A, B, S satisfying: (a)
V = A ∪ B ∪ S; (b) |S| ≤ s and |A|, |B| ≤ α|V |; (c) No edges connect A and B (i.e., E(A, B) = ∅).
     The separation number s(G) is the minimum s such that every subgraph of G admits an
(s, 2/3)-separator. The separation number s(G) is within a constant factor of the graph’s treewidth.

Experiment Narrative
We started the investigation with trying to understand the query complexity for two rounds. One of
the prompts used in the early stages of writing the paper is in Figure 5.




  3
      The constant 9/10 can be replaced by any other constant strictly more than 1/2.


                                                         57
   “Given a connected undirected graph G = (V, E), there is an unknown function f : V → R,
   which assigns a value to every vertex v (say the values are distinct). We have oracle access
   to the function (i.e. an algorithm can learn the value of the function at a vertex by probing
   that vertex). A vertex v is a local minimum if f (v) ≤ f (u) for all neighbors u of v. What is
   the query complexity of finding a local minimum in t rounds of interaction with the oracle?”


   Suppose we focus on two rounds. Can you design algorithms as a function of graph
   features/properties like minimum vertex cover, chromatic number, treewidth?



    Figure 5: Early prompt for trying to understand the query complexity for two rounds.


 The full response to this prompt is included below.

Response: This is an excellent problem that explores the trade-offs between the number of
interaction rounds and the total query complexity for finding a local minimum in a graph. When
restricted to two rounds, algorithms must strategically balance the exploration in the first round
with an adaptive, focused search in the second round. We can indeed design effective algorithms
by leveraging graph structural properties.
General Framework: Decomposition-Based Approach. The core strategy for a two-
round algorithm involves partitioning the vertices V into a separator set S and the remainder
V \ S. The first round queries S. The key is that G[V \ S] must be decomposed into small
connected components, allowing the second round to adaptively explore the neighborhood of
the most promising candidate.
Let K be the maximum size of any connected component in G[V \ S].
Generalized Decomposition Algorithm:
  1. Decomposition: Identify a separator set S.

   2. Round 1: Query all vertices in S (Q1 = S).

   3. Adaptivity: Identify the minimum value found: vmin = arg minv∈S f (v).

   4. Round 2: Identify all connected components of G[V \ S] that are adjacent to vmin . Let
      Q2 be the union of vertices in these components. Query Q2 .

   5. Output: Output v ∗ = arg minv∈S∪Q2 f (v).

Correctness: The algorithm guarantees finding a local minimum. If v ∗ ∈ S (so v ∗ = vmin ), all
its neighbors are queried. If v ∗ ∈ Q2 , then f (v ∗ ) < f (vmin ). Its neighbors in S are larger than
f (vmin ), and its neighbors within its component (which is entirely in Q2 ) are larger than f (v ∗ )
by definition.
Query Complexity: Let ∆ be the maximum degree of G. Vertex vmin can be adjacent to at
most ∆ components, each of size at most K. Thus, |Q2 | ≤ K · ∆. The total query complexity is
bounded by |S| + K · ∆. We aim to minimize this quantity by optimizing the trade-off between
|S| and K.



                                                   58
  1. Algorithm based on Minimum Vertex Cover (VC). A Vertex Cover C is a separator
  such that V \ C is an independent set (components of size K = 1).
  Algorithm (VC-Adaptive): Use the minimum vertex cover (size τ (G)) as the separator S.
  Query Complexity: QCV C = τ (G) + 1 · ∆ = τ (G) + ∆. This is efficient if both τ (G) and ∆ are
  small. However, for many graphs (e.g., a path graph where τ (G) ≈ N/2), this complexity is
  O(N ).

  2. Algorithm based on Chromatic Number (χ(G)). The chromatic number relates to the
  size of the maximum independent set α(G), with α(G) ≥ N/χ(G). We can use the complement
  of the largest independent set as the separator S (a vertex cover). This is also the K = 1 case.
  Query Complexity: QCχ = (N − α(G)) + ∆ ≤ N (1 − 1/χ(G)) + ∆. This is effective for
  graphs with small chromatic numbers and bounded degrees, such as bipartite graphs, where the
  complexity is ≤ N/2 + ∆.

  3. Algorithm based on Treewidth (tw(G)). Treewidth (w = tw(G)) measures the
  separability of a graph. We can optimize the generalized framework by choosing K > 1. Let
  sK (G) be the minimum size of a separator S such that all components of G[V \ S] have size at
  most K. The complexity is: QC = minK (sK (G) + K · ∆).
  Graphs with low treewidth can be efficiently shattered. Specifically, many graph classes with
  bounded treewidth satisfy the property sK (G) = O(N · w/K) (known as having 1/K-separators).
  Optimized Complexity: We minimize O(N w/K) + K∆. The balance is achieved whenpthe two
  terms are roughly equal: N w/K ≈ K∆. This yields
                                               p an optimal component size K ≈ N w/∆.
  The resulting query complexity is: QCT W = O( N · tw(G) · ∆).
  Implications: This demonstrates that sublinear query complexity is achievable in two rounds for
  structured graphs.                                                                       √
  • Paths and Trees: For paths (w = 1, ∆ = 2) or bounded-degree trees, the complexity is O(√N ).
  • Bounded Treewidth/Degree Graphs: If tw(G) = O(1) and ∆ = O(1), the complexity is O( N ).

      √ Planar Graphs. Planar
  Example:                 √    graphs utilize stronger separator theorems (sK (G) =
  O(N/ K)). Optimizing O(N/ K) + K∆ yields a complexity of O(N 2/3 ∆1/3 ).

  Summary. By exploiting graph structures, we can design efficient two-round algorithms. The
  Vertex Cover and Chromatic Number approaches provide parameterized complexity based on the
  K = 1 decomposition. The Treewidth approach leverages generalized decomposition (optimized
  K) and allows for sublinear query complexity in various important graph classes.


    The separation number and treewidth are related by a constant factor; thus, approach (3) from
the response is essentially the two-round algorithm presented in our full paper.
   In subsequent interactions, we prompted the model to generalize this two-round strategy to t ≥ 2
rounds. The model successfully synthesized a t-round algorithm anchored by a “Shattering Lemma”.
The lemma is: “For any parameter K ∈ [1, n], there exists a separator S ⊆ V such that every
connected component of G[V \ S] has size at most K, with |S| < 3sn/K. This lemma is folklore and
was central to constructing the general strategy. We also included the vertex cover-based algorithm
suggested by the model into the paper’s introduction as an example.


                                                59
   We obtained this way the following theorem.
Theorem 7.11 (Theorem 1 in [13]). Let G = (V, E) be a connected undirected graph with n vertices.
The deterministic query
           1        1     complexity of finding a local minimum on G in t ≥ 2 rounds is at most
min 4t · n t (s∆)1− t , n , where ∆ is the maximum degree and s is the separation number of G.
    The development of the lower bounds was more iterative. Initially, the model insisted on
constructing hard graphs (e.g., line graphs with cliques of size s attached to each node) rather than
finding a hard distribution of functions for a fixed graph. Some of the lower bounds derived in
this stage were not correct, or relied on looking at the longest path in the graph or using Menger’s
theorem.
   Eventually we created a prompt that had the following elements:
   • explicitly clarifying it must keep the given graph fixed and find a hard input distribution (of
     functions) for that graph;

   • including as context prior papers on lower bounds for local search (specifically, [12] and [85]);

   • asking it to focus on local search in two rounds on a tree and try to prove a lower bound of
       √
     Ω( n).
   The prompt, given in Figure 6, also contained the version of the paper up to that point, which
contained only algorithmic results (Theorem 7.11).


     I am working on the following manuscript.
                                         √     Can you read it (ignoring the todos/notes) and
     then help me prove a lower bound of n on the randomized query complexity of finding a
     local minimum in two rounds on a tree? The statement should be of the form:

     Theorem. Let G = (V, E) be an undirected connected tree with n vertices. Then  √    the
     randomized query complexity of finding a local minimum in two rounds on G is Ω( n).

     Note the lower bound should hold for the given tree G, so don’t create a hard family of
     trees. Rather, you need to create a hard family of functions for the given tree G. Make it
     so that for each function in the family, there is a unique local minimum. Also don’t hide
     the constants under big Omega until the very end of the proof. Attaching two papers from
     this literature together with my current draft; see especially the paper on local search in
     rounds on grids for examples of how to use Yao’s lemma in such proofs (i.e. finding a hard
     distribution of functions and analyzing the performance of a deterministic algorithm).



                     Figure 6: Prompt for lower bound on trees in two rounds


   The model’s response to the prompt is included below:


  Theorem. Let G = (V, E) be an undirected connected tree with n > 1 vertices. Then the
  randomized query complexity of finding a local minimum in two rounds on G, with success
                                      √                                    √
  probability at least c = 9/10, is Ω( n). Specifically, it is at least 1.8 n − 2.

  Proof. We use Yao’s Minimax Principle. We define a distribution D over input functions such



                                                   60
that each function has a unique local minimum. We then analyze the expected query complexity
of any deterministic two-round algorithm A that succeeds with probability at least c over D.
1. The Hard Distribution D. Fix an arbitrary vertex r ∈ V as the root. Let d(v) be the
depth of v (distance from r). Let Anc(v) be the set of ancestors of v (the unique path from r to
v, inclusive). We write u ⪯ v if u ∈ Anc(v).
For each v ∗ ∈ V , we define the function fv∗ : V → Z:
                                             (
                                              −d(x) if x ⪯ v ∗
                                   fv∗ (x) =
                                                d(x) if x ̸⪯ v ∗

fv∗ has a unique local minimum at v ∗ .
Let D be the uniform distribution over {fv∗ }v∗ ∈V . The input is fV ∗ , where V ∗ is chosen
uniformly at random from V .
2. Analysis of a Deterministic Two-Round Algorithm A.
Round 1. A queries a fixed set Q1 ⊂ V . Let q1 = |Q1 |. Since the structure of G is known, d(x)
is known. A query to fV ∗ (x) reveals whether x ⪯ V ∗ . The outcome of Round 1 is the signature
SV ∗ = Anc(V ∗ ) ∩ Q1 .
Let S be the set of possible signatures. The outcomes partition V into K = |S| blocks C1 , . . . , CK ,
where Ci is the set of v ∗ corresponding to the i-th signature.
Lemma 7.12. The number of distinct outcomes K is at most q1 + 1.

Proof. For any non-empty signature S ∈ S, let m(S) be the unique element in S farthest from
the root r. Note m(S) ∈ Q1 . We show the map m : S \ {∅} → Q1 is injective.
Suppose m(S1 ) = m(S2 ) = x. Let S1 = Anc(v1 ) ∩ Q1 . Since x ∈ S1 , we have x ⪯ v1 . We claim
S1 = Anc(x) ∩ Q1 . (⊆): If y ∈ S1 , then y ∈ Q1 and y ⪯ v1 . Since x is the deepest element in S1 ,
y must be an ancestor of x (as all elements in Anc(v1 ) are comparable). Thus y ∈ Anc(x) ∩ Q1 .
(⊇): If y ∈ Anc(x) ∩ Q1 . Since x ⪯ v1 , Anc(x) ⊆ Anc(v1 ). Thus y ∈ Anc(v1 ) ∩ Q1 = S1 .
Therefore, S1 = Anc(x) ∩ Q1 . Similarly, S2 = Anc(x) ∩ Q1 . Thus S1 = S2 . Since m is injective,
there are at most |Q1 | = q1 non-empty signatures. Including the possibility of the empty
signature, K ≤ q1 + 1.

Round 2. If the outcome implies V ∗ ∈ Ci , A queries Q2,i of size qi . This further partitions Ci
into Ki sub-blocks. By the same logic as Lemma 7.12, Ki ≤ qi + 1.
3. Success Probability and Expected Cost. Let Pi be the conditional success probability
given V ∗ ∈ Ci . Since the distribution within Ci is uniform, and the algorithm makes a
deterministic guess for each sub-block Ci,j , it succeeds on at most one vertex per sub-block.
                Ki                                                   Ki
                X
                          ∗         ∗                   ∗
                                                                     X  |Ci,j |    1        Ki
         Pi =         P (V ∈ Ci,j |V ∈ Ci )P (Success|V ∈ Ci,j ) ≤                       =       .
                                                                           |Ci | |Ci,j |   |Ci |
                j=1                                                  j=1

(The inequality becomes equality if the algorithm guesses optimally within each sub-block).
Since Ki ≤ qi + 1, we have |Ci |Pi ≤ qi + 1, so qi ≥ |Ci |Pi −
                                                             P1. Also, ∗Pi ≤ 1 since 1KP
                                                                                       i ≤ |Ci |.
We require the overall success probability PS ≥ c. PS = K      i=1 P (V  ∈ C  )P
                                                                             i i  =  n
                                                                                         K
                                                                                         i=1 |Ci |Pi .
                        PK
Let S = cn. We require i=1 |Ci |Pi ≥ S.



                                                  61
  The expected query complexity Qexp of A under D is:
                       K                                K                                   K                             K
                                                                                                                !
                1X                1X                           1                            X
                                                                                                            2         1X
    Qexp = q1 +    |Ci |qi ≥ q1 +    |Ci |(|Ci |Pi − 1) = q1 +                                       Pi |Ci |       −    |Ci |
                n                 n                            n                                                      n
                      i=1                           i=1                                        i=1                        i=1
                            K
                        1   X
         = q1 − 1 +               Pi |Ci |2 .
                        n
                            i=1

  4. Optimization. We use the Cauchy-Schwarz inequality to lower bound the summation:

              K
                                 !   K
                                                !           K p
                                                                                 !2       K
                                                                                                           !2
              X                      X                      X            p                X
                     Pi |Ci |2             Pi       ≥         ( Pi |Ci |) Pi          =         Pi |Ci |        ≥ S2.
               i=1                   i=1                    i=1                           i=1

  Therefore, K
            P            2   2
                                PK
             i=1 Pi |Ci | ≥ S /( i=1 Pi ). P
  We bound the denominator. Since Pi ≤ 1,    Pi ≤ K. By Lemma 7.12, K ≤ q1 + 1.
                                                    K
                                                    X                       S2
                                                            Pi |Ci |2 ≥          .
                                                                          q1 + 1
                                                    i=1

                                                                                           2                          2
  Substituting this back into the expected cost: Qexp ≥ q1 − 1 + n(qS1 +1) = q1 − 1 + qc1 +1
                                                                                          n
                                                                                             .
  This lower bound holds for any deterministic algorithm A, characterized by its choice of q1 .
  To find the overall lower bound via Yao’s principle, we minimize this expression over q1 ≥ 0.
                                                               2
  Let x = q1 + 1 (x ≥ 1). We minimize g(x) = x − 2 + c xn . By the AM-GM inequality,
                √          √                              √                   √
  x + c2 n/x ≥ 2 c2 n = 2c n. Equality holds when x = c n. (Assuming c n ≥ 1, which holds
  for c = 9/10 and n > 1).                        √
                                        Qexp ≥ 2c n − 2.
                                          √             √
  Substituting c = 9/10: Qexp ≥ 2(0.9) n − 2 = 1.8 n − 2. Thus, the randomized query
                   √
  complexity is Ω( n).


    Building on the lower bound for trees in two rounds, we asked the model to generalize the result
to any graph G in two rounds. The proposed approach defines an arbitrary spanning tree T of G
rooted at some vertex r and a family of functions F = {fv | v ∈ V } parameterized by each vertex
v ∈ V that also depends on T . In particular, for every v ∈ V , let fv : V → Z be such that for all
x∈V,
                                         (
                                           −distT (r, x) if x ⪯T v
                                fv (x) =                                                        (28)
                                             distT (r, x) otherwise

where distT (r, x) represents the distance between r and x in the spanning tree T .
    Moreover, we denote by D the uniform distribution over F. The distribution D is the one used
to obtain the lower bound for any graph and number t of rounds. Unlike the two-round case where
the round-1 queries are fixed, the t ≥ 3 round case requires analyzing adaptive histories. To handle
the adaptivity, the model suggested the notion of candidate set. Suppose H is a history reachable
after i rounds. The candidate set, denoted C(H), represents the vertices of G that could still be
local minima given the history H.


                                                                  62
                                                       (b) Spanning tree with the candidate sets attain-
        (a) Graph with n = 16 vertices                 able at the end of round 1.

Figure 7: The left figure (a) shows a graph G. The input function is drawn from F. The right figure
(b) shows a spanning tree of G rooted at 1. The set of queries Q1 = {2, 3, 10} submitted in round 1
are circled in red. The partition of candidate sets attainable at the end of round 1 (depending on
the answers to the queries) is illustrated using yellow frames.


   The model observed several properties of the candidate sets, which we consolidated into a key
lemma stating that at the end of each round i:

   • (a) each attainable candidate set is a sub-tree of the original spanning tree T of G; and

   • (b) the candidate sets partition the graph, and there is a bijection from the set of histories
     reachable at the end of round i and the set of candidate sets attainable at the end of round i.

    While the model’s intuition was correct, obtaining a rigorous proof for part (b) was more
challenging. It initially treated the result as self-evident; when pressed for details, it produced a
circular argument (very briefly, to prove the bijection, it assumed that the candidate sets already
form a partition of the set of vertices). We tried guiding it toward an inductive proof, and later
toward a direct non-inductive one, but the circular argument persisted in both. The turning point
came when we gave it a hint: assume by contradiction that a vertex lies in two candidate sets, and
use part (a) to analyze the roots of the trees underlying the two sets. With this hint, the model
generated a correct proof that is now found in the paper.
   The remainder of the t-round lower bound argument was correct. Thus we obtained:

Theorem 7.13 (Theorem 2 in [13]). Let G = (V, E) be a connected undirected graph with n vertices.
The randomized query complexity of finding a local minimum on G in t ∈ N∗ rounds is Ω(tn1/t − t).

    We also asked the model to prove a linear lower bound for local search in two rounds on constant-
degree expanders. Instead, it responded by proposing a Parallel Steepest Descent with a Warm Start
algorithm. This algorithm has a query complexity slightly better than linear even for two rounds
on any graph with constant maximum degree: O(n/ log n). The bound given by this algorithm is
stated next for any number of rounds.

Proposition 7.14 (Proposition 1 in [13]). Let G = (V, E) be a graph with n vertices and maximum
                                                                                          √
degree ∆. The randomized query complexity of finding a local minimum in t ≥ 2 rounds is O( n + t)
                                √
when ∆ ≤ 2 and O t·logn n + t∆2 n when ∆ ≥ 3.
                                  
                        ∆




                                                 63
Concluding Remarks. Our experiment demonstrates that the model can expedite theoretical
research when treated as a research assistant. For instance, when guided toward separation numbers,
the model developed the divide-and-conquer algorithm and its proof, leveraging the ‘Shattering
Lemma’ as a key component for the analysis. This process required vigilance; we had to rigorously
audit the model’s claims, as illustrated by a circular argument we uncovered in one of the lower
bound lemmas. Despite the need for verification, the interaction was very fruitful, yielding a lower
bound construction with a surprisingly elegant recursive structure.

Acknowledgements. Simina Brânzei was supported by US National Science Foundation grant
CCF-2238372. Ioannis Panageas was supported by US National Science Foundation grant CCF-
2454115.




                                                64
7.3   Robust Coresets
Written by Yi Li, David P. Woodruff, and Xuan Wu.

Problem Context
In the standard coreset framework, one is given a finite weighted collection of functions F = {(f, wf )},
where each function fP: Rd → R≥0 is associated with a weight wf ≥ 0. The loss function for F is
defined as L(F; x) = f ∈F wf f (x). An ε-coreset is a weighted subset F̃ ⊂ F such that

                             (1 − ε)L(F ; x) ≤ L(F̃; x) ≤ (1 + ε)L(F; x)

holds simultaneously for all possible values of x. Classical problems such as ℓp -regression and
clustering naturally fit into this framework. A typical approach to construct a coreset is sensitivity
sampling, where each function f ∈ F is sampled with probability proportional to its sensitivity,
defined as
                                                      wf f (x)
                                        σF (f ) = sup          .
                                                   x L(F; x)

For example, in ℓ2 -subspace embedding and regression, these sensitivities coincide with leverage
scores. In the more general ℓp -subspace embedding and regression, exact sensitivities are harder to
compute and Lewis weights are commonly used as an effective proxy. Similarly, in clustering, recent
work [8] has shown that sensitivity sampling canPachieve near-optimal coreset sizes. We also define
the sensitivity of the function set F as σ(F) = f ∈F σF (f ).
    Robust coresets can be studied within the same framework by replacing the standard loss with a
trimmed loss. Specifically, for an integer m ≥ 0, the trimmed loss is defined as
                                                              n
                                                              X
                               L(m) (F; x) =      min
                                                  ′
                                                                         wf f (x),
                                                 F ⊂F                ′
                                               |F \F ′ |≤m (f,wf )∈F

which discards (at most) m largest contributions to the loss. Correspondingly, an (ε, m)-robust
coreset is a weighted subset F̃ ⊂ F such that

                        (1 − ε)L(m) (F; x) ≤ L(m) (F̃; x) ≤ (1 + ε)L(m) (F; x)

for all x. When m = 0, this definition reduces to the standard ε-coreset. Prior work [60] has shown
that if the total sensitivity of F is bounded by T (i.e. σ(F ′ ) ≤ T for any non-empty subset F ′ ⊂ F),
then there exists an (ε, m)-robust coreset of size O(T m/ε · log(T m/ε)) + Q, where Q denotes the
size of a standard ε-coreset.

AI Contribution
AI provided a sharper analysis that eliminates the logarithmic factor, improving the robust coreset
size bound to O(T m/ε) + Q, which is known to be tight.

Technical Details
We first review the algorithms from [60] and the associated guarantees before presenting the tighter
analysis produced by AI.



                                                     65
   Algorithm 1 Uniform(A, ε, m)                       Algorithm 2 Refine(D, ε, m)
   Require: A set A of functions, parameters ε Require: A coreset D, parameters ε and m
       and m                                      Ensure: A refined subset D̃ adapted for the
   Ensure: A subset D ⊆ A                             robust optimization problem
    1: B ← ∅                                       1: D̃ ← ∅
    2: for each f ∈ A, with probability m
                                        1
                                          , add f  2: for (f, ωf ) ∈ D do
       to B                                        3:    compute the sensitivity σD (f )
    3: for each f ∈ B, compute the sensitivity     4:    nf ← ⌈ m  ε · σD (f )⌉
                                                                                ω
       σB (f )                                     5:    Add nf copies of (f, nff ) to D̃
                              ε
    4: D ← {f ∈ B : σB (f ) ≥ 4 }                  6: end for
    5: return D                                    7: return D̃


   Algorithm 3 Coreset(A, ε, m)                       Algorithm 4 ModifiedCoreset(A, ε, m)
   Require: A set A of functions, parameters ε Require: A set A of functions, parameters ε
       and m, and an algorithm Vanilla(A) to con-     and m, and an algorithm Vanilla(A) to con-
       struct an ε-coreset for A                      struct an ε-coreset for A
   Ensure: An (ε, m)-robust coreset for A         Ensure: An (ε, m)-robust coreset for A
    1: S ← ∅                                       1: R ← 40m ln(2000T m/ε)
                         Tm
    2: R ← Θ(m log ε )                             2: for i = 1, 2, · · · , R do
    3: for i = 1, 2, · · · , R do                  3:     Di ← Uniform(A, ε, m)
    4:     D ← Uniform(A, ε, m)                    4:     for f ∈ Di do
    5:     S ←S∪D                                  5:        cf ← cf + 1
    6: end for                                     6:     end for
    7: V ← Vanilla(A \ S)                          7: end for
                                                                               R
    8: S̃ ← {(f, 1) : f ∈ S}                       8: S ← {f ∈ A : cf ≥ 10m      }
    9: Return S̃ ∪ Refine(V, ε, m).                9: V ← Vanilla(A \ S)
                                                  10: S̃ ← {(f, 1) : f ∈ S}
                                                  11: Return S̃ ∪ Refine(V, ε, m).
    The algorithms from [60] are reproduced in Algorithms 1 to 3, where Algorithm 3 outputs
the final robust coreset. A function f ∈ A is called contributing if there exists x ∈ Rd such that
        ε
f (x) ≥ m  · L(m) (A; x). The following guarantee of Algorithm 1 was established in Lemma 4.3 of [60].

                                                                           1
Lemma 7.15. Assume that f is contributing, then with probability at least 5m , the set returned by
Uniform(A, ε, m) contains f .

   It was then argued in [60] that the number of contributing functions in A is O( Tεm · log Tεm ).
Consequently, Algorithm 3 executes Θ(m log(T m/ε)) rounds of Algorithm 1 in order to capture all
contributing functions with high probability, thereby forming the basis of the robust coreset that
can handle outliers.
   Now we describe our interactions with AI. We first entered the following prompt.




                                                 66
     Prompt 1. Can you resolve the logarithmic factor gap in the coreset construction in the
     attached paper? Feel free to give both a tighter analysis as well as to change the algorithmic
     framework in the paper in order to achieve this improved bound.
     <generic instructions on being mathematically rigorous>


          Gemini. Yes, the logarithmic factor gap in the coreset construction size can be resolved.
          The paper presents a coreset of size O(K log K) + Q, where K = T m/ε. We demonstrate
          that this can be improved to O(K) + Q in expectation and with constant probability.
              This improvement is achieved in two steps: first, by providing a tighter analysis of
          the number of contributing functions, and second, by modifying Algorithm 3 to filter out
          non-contributing functions more effectively using frequency estimation.
             ...


   The AI produces the following bound on the number of contributing functions, which already
improves the argument in [60].

Lemma 7.16. The number of contributing functions in A is 20 Tεm .

Proof. Let C be the set of contributing functions, N = |C|. Let D be the output of a single execution
of Algorithm 1. Algorithm 1 returns D = {f ∈ B : σB (f ) ≥Pε/4}. By the assumption of strong
total sensitivity T , we have σB ≤ T . Therefore, |D| · (ε/4) ≤ f ∈D σB (f ) ≤ σB ≤ T . This implies
|D| ≤ 4T /ε deterministically. Let W = 4T /ε. Consequently, the expected size of D is bounded:
E[|D|] ≤ W .
    Let pf = Pr(f ∈ D). By 7.15, if f ∈ C, then pf ≥ 1/(5m). By linearity of expectation:
                                             X             X                  1
                                  E[|D|] =          pf ≥          pf ≥ N ·      .
                                                                             5m
                                             f ∈A          f ∈C

Combining the inequalities:
                             N                      4T   20T m
                                ≤ W =⇒ N ≤ 5mW = 5m    =       .
                             5m                      ε     ε
   The AI then proceeds with a modified version of Algorithm 3 by tracking the frequency of each
function in S and discarding the ones with low frequencies. It then presents a theorem as follows.

Theorem 7.17 (Improved Coreset Construction). Algorithm 3-Modified constructs an (ε, m)-robust
coreset for A of expected size O(K) + Q. The construction succeeds with high probability (at least
1 − O(1/n)).

    The proof is correct, though we omit it here, since the theorem states an expected size of the
coreset, which is not desirable. We further make the following prompt.


     Prompt 2. It looks correct, but the Theorem only gives the size in expectation. The
     earlier version had a high-probability bound, which shouldn’t be hard to get. Maybe you
     can prompt it to produce an upper bound that holds with high probability? Actually we
     need only probability ≥ 0.99 instead of 1 − 1/n.




                                                       67
          Gemini. We demonstrate that the logarithmic factor in the coreset size bound of Theorem
          4.1 in the paper "Robust Sparsification via Sensitivity" can be removed. The original paper
          presents a coreset of size O(K log K) + Q, where K = T m/ε. We show that a modification
          of the algorithm yields a coreset of size O(K) + Q with high probability (at least 0.99).
              ...
          Key Properties of Algorithm 1:
             1. Deterministic    Size Bound: The output D always satisfies |D| ≤ W . This is because
                                 σB ≤ T . Since σB (f ) ≥ ε/4 for f ∈ D, we have |D| · (ε/4) ≤ T , so
                P
                      σ
                  f ∈D B  (f ) ≤
                |D| ≤ W .
             2. Expected Size Bound: E[|D|] ≤ W .
             3. Capture Probability (Lemma 4.3): If f ∈ C, the probability pf = P (f ∈ D)
                satisfies pf ≥ 1/(5m).
             ...


   AI returns a correct version of the theorem.
Theorem 7.18. The Modified Algorithm constructs an (ε, m)-robust coreset for A of size O(K) + Q
with probability at least 0.99.
    The proof is correct, though somewhat suboptimal. It uses Markov’s inequality to bound the
total number of sampled functions over R rounds, which is unnecessary. This suboptimality arises
from a weaker property generated by the AI, as presented in its response above. In particular,
Point 1 already provides a deterministic bound |D| ≤ W , rendering the expected bound in Point 2
unnecessary.
    Therefore, we further prompt the AI to improve the argument.


     Prompt 3. This looks correct though it is a bit suboptimal when bounding the size.
     Specifically, it says <quote of the properties>.
     In the first bullet point, it already obtains that |D| ≤ W , so the second bullet point is
     unnecessary. In the subsequent proof of Part 2 of the theorem, it could directly use the
     deterministic bound |D| ≤ W instead of the expectation bound. This will further tighten
     the analysis a bit.


          Gemini. <latex source>


   The results are correct and are reproduced below with minor modifications to fit the present
context. The algorithm generated by the AI is presented in Algorithm 4, with slight simplifications.
Theorem 7.19. Let ε ∈ (0, 21 ) and F be a unit-weight function set with total sensitivity T . Suppose
that there exists an algorithm that computes a vanilla ε-coreset for F of size Q. Then, Algorithm 4
computes an (ε, m)-robust coreset for F of size O( Tεm ) + Q, with probability at least 0.99.
Proof. Size bound. We analyze the size of the set S returned by the algorithm. Let Ctotal be the
total count of all functions captured across all R iterations.
                                                      R
                                                      X
                                           Ctotal =         |Di |.
                                                      i=1


                                                   68
By the deterministic size bound property of Algorithm 1, we know |Di | ≤ W := 4T /ε for all i.
Therefore, Ctotal is deterministically bounded:
                                                      R
                                                      X
                                        Ctotal ≤            W = RW.
                                                      i=1

   Now we relate the size of S to Ctotal . By definition, f ∈ S if and only if cf ≥ Rθ for θ = 1/(10m).
                                     X             X             X
                          Ctotal =          cf ≥          cf ≥          (Rθ) = |S| · Rθ.
                                     f ∈A          f ∈S          f ∈S

Therefore, we have a deterministic bound on |S|:

                                        Ctotal   RW   W   40T m
                                |S| ≤          ≤    =   =       .
                                         Rθ      Rθ   θ     ε
Thus, |S| ≤ 40K, where K = T m/ε. The size bound |S| = O(K) holds deterministically.
     Correctness. We want to bound the probability that a contributing function f ∈ C is missed
(f ∈/ S). The count cf is a sum of R independent indicators. If f ∈ C, we have E[cf ] ≥ R/(5m). If
f ̸∈ S, it means that cf < R/(10m). Use the Chernoff lower tail bound P (X ≤ µ/2) ≤ exp(−µ/8):
                                                       
                                   1               R/(5m)
  Pr(f ∈
       / S) = Pr(cf < Rθ) = Pr cf ≤ E[cf ] ≤ exp −
                                   2                  8
                                                                       
                                                          40m ln(2000K)       1
                                                  = exp −                 =       .
                                                               40m          2000K

   We apply a union bound over C. By Lemma 7.16, |C| ≤ 20K.
                                                    X                                1      1
        Pr(C ̸⊆ S) = Pr(∃f ∈ C : f ∈
                                   / S) ≤                 Pr(f ∈
                                                               / S) ≤ 20K ·              =     = 0.01.
                                                                                   2000K   100
                                                   f ∈C

    The algorithm deterministically produces a set S of size |S| ≤ 40K. With probability at least
1 − 0.01 = 0.99, the algorithm ensures C ⊆ S. The remainder of the correctness proof follows exactly
as in Theorem 4.1 of [60].




                                                          69
7.4   Submodular Function Maximization in a Stream
Written by Ola Svensson.

Problem context
We consider monotone submodular maximization under a cardinality constraint in the adversarial
injection streaming model introduced in the paper “Robust Algorithms under Adversarial Injec-
tions” [47]. In this model, the stream consists of an (unknown) set Egood of “genuine” elements
arriving in uniformly random order, interleaved with an arbitrary set Enoise of injected elements
placed by an adversary. The motivation of this semi-random model is to design algorithms in a
beyond-worst-case model while not overfitting to the assumption (such as all elements arrive in a
uniformly at random order). The goal is to output a set S ⊆ Egood ∪ Enoise of size at most k with
value close to
                                    OPT :=      max      f (T ),
                                             |T |≤k, T ⊆Egood

where f is a nonnegative monotone submodular function given by value-oracle access. We remark
that it is important that OPT is defined with respect to the optimal solution of elements in Egood .
Indeed, if OPT were also allowed to contain elements of Enoise then the model would be equivalent
to a fully adversarial one.
    The above paper proposes a streaming algorithm for this setting (the tree algorithm for monotone
submodular maximization), achieving an approximation factor around 0.55 while storing a number
of elements independent of |Egood | (but exponential in k). Two concrete questions were left open
for submodular maximization in this model: (i) whether one can reach the offline-optimal constant
(1 − 1/e), and (ii) whether one can reduce memory to poly(k) elements.

The tree algorithm and where the analysis bottleneck appears
At a high level, the tree algorithm maintains a rooted tree of depth k whose root-to-leaf paths
represent candidate size-≤ k solutions. When a new element e arrives, the algorithm considers
attaching e beneath existing nodes based on its marginal contribution. The tree is kept from
exploding by merging equal-marginal states: within each level, only one representative for each
marginal-gain value is retained. This keeps the algorithm stream-length independent, but in the
worst case still requires exponentially many stored elements as a function of k.
    The original approximation analysis proceeds by tracking a carefully chosen leaf as the k
(unknown) optimal elements from Egood appear in the stream. A central technical device is a
threshold parameter t used in a case split comparing (i) the best “available” marginal gain since the
last optimal element appeared, versus (ii) the marginal gain of the next unseen optimal element.
This case split yields a recurrence R(k, h) that lower bounds the fraction of OPT captured after
“progress” through h optimal elements with budget k, with the final guarantee given by R(k, k). In
the paper, t is chosen globally (independent of the state (k, h)); numerically, setting t ≈ 0.8 yields
R(k, k) ≈ 0.55067.
    A key insight by Gemini—which ultimately enabled our improvement—is that t is not an algo-
rithm parameter. It only appears in the analysis, meaning we are free to choose a different threshold
in different states as long as the inequalities used in the proof remain valid.

AI Contribution
The AI identified a latent degree of freedom in the existing algorithmic analysis. By replacing a
global threshold with a state-dependent threshold, the model autonomously derived and proved an


                                                  70
optimized
    √      recurrence relation, strictly improving the algorithm’s approximation ratio from ≈ 0.55 to
2 − 2.
    We used Gemini to explore whether the analysis could be sharpened.
    Gemini did not produce a new algorithm achieving (1 − 1/e), nor did it find a way to reduce
the memory requirement to poly(k) elements in this adversarial injection setting. However, it did
identify a clean way to improve the existing analysis of the tree algorithm: replace the single global
threshold t by a state-dependent threshold tk,h in the recurrence.
    Concretely, Gemini suggested using
                                                            k
                                           tk,h := √              ,
                                                         k 2 + h2
and first predicted and then formally proved that the corresponding optimized recurrence achieves
the exact constant                              √
                                 R(k, k) = 2 − 2 ≈ 0.585786,
thereby improving the analyzed approximation ratio of the same underlying algorithm from ≈ 0.55067
to ≈ 0.58579.
    The remainder of this testimonial highlights the four prompts that led from “idea” to a complete,
algorithm-level guarantee.

Prompt 1: exploratory questions, and the key analysis insight



     Prompt 1. Please investigate if you can improve the submodular part of the attached paper.
     Specifically:
     • Can we get (1 − 1/e) for submodular maximization?
     • Can we only store poly(k) elements instead of exponentially many in k?
     Be mathematically rigorous.


          Gemini (summary). The model did not produce a new algorithm achieving (1 − 1/e),
          and it did not resolve how to store only poly(k) elements. However, it identified that the
          analysis recurrence in the paper can be strengthened by letting the threshold depend on the
          state: instead of a global t, introduce tk,h . It further
                                                                  √ hypothesized that the best constant
          achievable within this recurrence framework is 2 − 2, and that a natural candidate is a
          closed-form threshold of the form tk,h = t(h/k).



Figure 8: The first prompt where Gemini identified the direction for improvement and the improved
guarantee.


    In the first interaction with Gemini (fig. 8), we gave a fairly general prompt with two open
questions. Even though the response did not resolve the two open algorithmic questions, it pinpointed
a previously unexplored degree of freedom in the analysis and proposed (correctly) that exploiting it
improves the approximation factor.

Prompt 2: a rigorous (but asymptotic) derivation via continuous limits


                                                    71
                                                                     √
     Prompt 2. Can you rigorously improve it to obtain a 2 −             2 approximation, as suggested?

     <math rigor boilerplate>


          Gemini (summary). Gemini produced a rigorous argument in a continuous/asymptotic
          regime (as k → ∞) by recasting the recurrence optimization as a minimax problem that
          leads to differential inequalities/ODE-type conditions. While this was not yet the discrete
          proof we needed, it strongly indicated the correct functional form of the optimal thresholds,
          and guided us to the explicit choice
                                                            k
                                               tk,h = √              .
                                                          k 2 + h2
          This directly set up Prompt 3, where we asked for a fully discrete proof.



    Figure 9: In the second prompt, we asked for a rigorous proof of the improved guarantee.


   In the second prompt, fig. 9, we asked for a rigorous proof and Gemini responded with an
argument in the asymptotic regime. Even though the ODE argument was “not exactly what we
asked for”, it served as a highly effective derivation tool : it revealed the right closed-form threshold
and the right constant before we invested time in a discrete induction.

Prompt 3: a complete discrete proof of the optimized recurrence
We next asked Gemini to prove the optimized recurrence formally, with the thresholds fixed to the
candidate form, see fig. 10 for the third prompt.




                                                    72
     Prompt 3 (condensed). Define tk,h = √k2k+h2 and the recurrence

                                    R(k, h) = min{Ak,h , Bk,h , Ck,h }

     with
                                    tk,h        tk,h 
                              Ak,h :=     + 1−          R(k, h − 1),
                                      k           k
                                    1         1 + tk,h 
                            Bk,h := + 1 −                 R(k − 1, h − 1),
                                    k             k
                                        1
                            Ck,h :=          ,
                                    1 + tk,h
                                                     √
     and base R(k, 0) = 0. Prove that R(k, k) = 2 − 2 for all integers k ≥ 1.


            Gemini (summary). Gemini proposed an explicit closed-form candidate P (k, h) (as a
            function of h/k) and showed
                                  √       it satisfies the recurrence by induction, yielding the exact
            identity R(k, k) = 2 − 2 for all k ≥ 1.



Figure 10: In our third prompt, we asked for and received a complete proof of the discrete recurrence.



    At this point, Gemini had delivered an almost complete proof of the mathematical core: the
optimal solution of the improved recurrence. This was the key missing technical ingredient needed
to upgrade the approximation factor.

Prompt 4: connecting the recurrence back to the tree algorithm (and a hidden mono-
tonicity issue)
Finally, we asked Gemini to connect the recurrence to the original algorithm analysis, see Figure 11.
This step is subtle because the original paper uses a global t in an inequality of the form R(k −
1, h − 1) ≤ 1/(1 + t), whereas our thresholds vary with (k, h).




                                                      73
     Prompt 4 (condensed). Please relate the recurrence with state-dependent thresholds
     t = tk,h to the analysis of the tree algorithm. In particular, in the analogue of Lemma 4 from
     the paper, the proof used R(k − 1, h − 1) ≤ 1/(1 + t) for a global t. Now t depends on (k, h),
     so this step requires care. Please write step-by-step how R(k, h) bounds the approximation
     guarantee, and identify what additional property is needed.


          Gemini (summary). Gemini provided a step-by-step mapping from the algorithm’s case
          analysis to the three terms Ak,h , Bk,h , and Ck,h , showing how R(k, h) lower bounds the
          value of a carefully chosen leaf as the optimal elements appear. Crucially, it identified that
          the “global-t” inequality is replaced by a requirement of the form
                                                                  1
                                          R(k − 1, h − 1) ≤             ,
                                                               1 + tk,h

          which does not automatically hold for arbitrary state-dependent thresholds. Gemini then
          pinpointed a sufficient condition: a monotonicity relation along the diagonal,

                                                tk,h ≤ tk−1,h−1 ,

          which implies 1+tk−1,h−1
                            1
                                   ≤ 1+t1k,h and allows the induction to go through. It also proved
          this monotonicity for the chosen optimal thresholds tk,h = √k2k+h2 .



Figure 11: In the fourth prompt, we asked Gemini to correctly relate the improved analysis of the
recurrence to the improved analysis of the algorithm.


    This last step was important for correctness: it is easy to “solve” an abstract recurrence while
accidentally breaking an inequality needed to justify the recurrence from the algorithm. Gemini
not only identified the missing monotonicity condition but also proved it for the optimal threshold
schedule, thereby completing the logical chain from the recurrence back to the streaming algorithm.

Outcome and takeaway
The outcome of this interaction was a strictly improved approximation guarantee for the same tree
algorithm in the adversarial injection streaming model:
                                                                    √
               approximation ratio improved from ≈ 0.55067 to 2 − 2 ≈ 0.58579,
achieved by refining the analysis (via a sharper, state-dependent choice of thresholds).
     From a “how to use Gemini” perspective, this case study highlights a valuable contribution: even
when a model does not solve the headline open problems (here, (1 − 1/e) or poly(k) memory), it can
still make a decisive contribution by (i) identifying a latent degree of freedom in an existing proof,
(ii) guessing the right closed form for an optimum constant/parameter schedule, and (iii) producing
formal proofs with minimal guidance.

The Formal Improved Analysis by Gemini

The following is the complete proof that was automatically generated by Gemini. We have kept the
writing exactly as automatically produced.

                                                     74
Preliminaries and Notation
Submodularity. A function f is submodular if for all S ⊆ T ⊂ E and e ∈ E \ T , the marginal
gain f (e|S) := f (S ∪ {e}) − f (S) satisfies f (e|S) ≥ f (e|T ). It is monotone if f (S) ≤ f (T ) for S ⊆ T .

Lemma 7.20 (Average Marginal Bound). Let O be a set of size k and S be any partial solution. For
a monotone submodular function f , the expected marginal gain of a random element o ∈ O satisfies:

                                                        f (O ∪ S) − f (S)
                                   Eo∼O [f (o | S)] ≥
                                                                k
If S = ∅ and O = Eopt , then Eo∼Eopt [f (o)] ≥ OPk T .

Proof. This follows from the definition of submodularity. The sum of the marginals of elements in O
added to S is at least the total gain f (O ∪ S) − f (S). Taking the average yields the result.

Stream Notation Let σ be the input stream. Eopt = {o1 , . . . , ok }. Let π be the random
permutation of Eopt . oπi is the i-th element of Eopt to arrive in the stream. Oiπ = {oπ1 , . . . , oπi }.
OP T = f (Eopt ).

The Tree Algorithm
We briefly review the Tree Algorithm from [47]. For simplicity, we assume the algorithm knows
OP T and that the set of possible marginal gains I is small (these assumptions can be removed using
standard techniques involving discretization and guessing, as detailed in the appendix of [47]).
    The algorithm maintains a rooted tree T of height at most k. Each node represents a partial
solution (the set of elements on the path from the root to the node).

Algorithm 5 Tree Algorithm
 1: Initialize tree T   with only the root (representing S = ∅).
 2: for each element e arriving in the stream σ do
 3:    for each node v in T do
 4:       Let Sv be the solution corresponding to v.
 5:       if |Sv | < k then
 6:           Calculate the marginal gain g = f (e|Sv ).
 7:           if v has no child c such that f (c|Sv ) = g then
 8:                Add a new child node corresponding to Sv ∪ {e}.
 9:           end if
10:       end if
11:    end for
12: end for
13: Return the solution SALG corresponding to the leaf with maximum value f (SALG ).




Analysis via Generalized Recurrence
The core of the analysis involves defining a specific path in the execution tree and lower bounding
its expected value. We generalize the approach by introducing a state-dependent threshold.




                                                     75
The Generalized Recurrence Relation We define the domain D := {(k, h) ∈ Z2≥0 : 0 ≤ h ≤ k}.
We introduce a generalized recurrence R(k, h) which aims to lower bound the approximation ratio
when the optimal solution has size k and the algorithm’s budget is h.
Definition 7.21 (Threshold Function). We define a threshold function T : D \ {(0, 0)} → (0, 1].
Definition 7.22 (Generalized Recurrence). Let R : D → R≥0 be defined as follows: R(k, 0) := 0 for
all k ≥ 0. For (k, h) ∈ D with k ≥ 1, h ≥ 1, let t = T (k, h).

                                      R(k, h) := min{Ak,h , Bk,h , Ck,h }

where
                                               
                                        t     t
                                 Ak,h = + 1 −     R(k, h − 1),
                                        k     k
                                                  
                                        1     1+t
                                 Bk,h = + 1 −        R(k − 1, h − 1),
                                        k       k
                                          1
                                 Ck,h =     .
                                        1+t

Adapted Path Selection Strategy To utilize this recurrence, the analysis employs a path
selection strategy that dynamically uses the threshold corresponding to the current subproblem.
This strategy defines a path in the tree whose expected value we analyze.
    We define the path Shπ = {sπ1 , . . . , sπh } inductively. We track the state (ki , hi , ni ): remaining OPT
size, remaining budget, and index of the current OPT element. Initialize (k1 , h1 , n1 ) = (k, h, 1).
    At step i (for i = 1, . . . , h): 1. Set the threshold ti = T (ki , hi ). 2. Define uπi (the best non-OPT
element seen so far) and viπ (the better of uπi and the current OPT element oπni ) relative to Si−1        π  (as
defined in [47]). 3. Apply the decision rule:
    • Case 1 (Greedy Choice): If Eπ [f (uπi |Si−1 π )] ≥ t · E [f (oπ |S π )]. Set sπ = uπ . Update:
                                                          i   π     ni i−1          i    i
      (ki+1 , hi+1 ) = (ki , hi − 1), ni+1 = ni .

    • Case 2 (Wait for OPT): Otherwise. Set sπi = viπ . Update: (ki+1 , hi+1 ) = (ki − 1, hi − 1),
      ni+1 = ni + 1.

Connecting the Recurrence to the Algorithm We now prove that R(k, h) bounds the
performance of this strategy, provided the threshold function satisfies a monotonicity property.
Definition 7.23 (Monotonic Threshold Condition (MTC)). A threshold function T (k, h) satisfies
the Monotonic Threshold Condition (MTC) if for all k ≥ 2, h ≥ 1:

                                         T (k, h) ≤ T (k − 1, h − 1).

Lemma 7.24. If T (k, h) satisfies the MTC, then for all k ≥ 1, h ≥ 1, letting t = T (k, h):
                                                                1
                                          R(k − 1, h − 1) ≤        .
                                                               1+t
Proof. If k = 1, then h = 1. R(0, 0) = 0. Since t > 0, the inequality holds. Assume k ≥ 2. By
definition of the recurrence:
                                                                       1
                           R(k − 1, h − 1) ≤ Ck−1,h−1 =                            .
                                                              1 + T (k − 1, h − 1)

                                                      76
By the MTC, T (k, h) ≤ T (k − 1, h − 1). Thus 1 + T (k, h) ≤ 1 + T (k − 1, h − 1).
                                                   1                  1          1
                   R(k − 1, h − 1) ≤                           ≤              =     .
                                          1 + T (k − 1, h − 1)   1 + T (k, h)   1+t


   We can now prove the main connection theorem.
Theorem 7.25. If the threshold function T (k, h) satisfies the MTC, then for all instances of the
problem and (k, h) ∈ D, the solution Shπ defined by the adapted strategy satisfies:

                                        Eπ [f (Shπ )] ≥ R(k, h) · OP T.

Proof. We proceed by induction on h.
     Base Case (h=0): R(k, 0) = 0. Eπ [f (S0π )] = f (∅) = 0. The theorem holds.
     Inductive Step: Assume the theorem holds for h − 1. We prove it for (k, h), where k ≥ 1, h ≥ 1.
Let t = T (k, h). We analyze the first step (i = 1). By Lemma 7.20, due to the random permutation,
Eπ [f (oπ1 )] ≥ OP T /k.
     Case 1: Eπ [f (uπ1 )] ≥ t · Eπ [f (oπ1 )]. We set sπ1 = uπ1 .
    As argued in [47], uπ1 is determined by the elements arriving before the first OPT element. Since
the adversary injects noise without knowledge of the permutation π, the set of elements in this prefix
is independent of π. Therefore, uπ1 is independent of π. Let s1 = uπ1 .
    We consider the remaining subproblem I ′ . It has k ′ = k OPT elements and budget h′ = h − 1.
The function is f ′ (T ) = f (T |s1 ). The optimum of the subproblem is OP T ′ = f (Eopt |s1 ). By
submodularity and monotonicity, OP T ′ ≥ OP T − f (s1 ).
    The remainder of the path Shπ \ {s1 } corresponds exactly to the path constructed by our strategy
applied to I ′ . By the Inductive Hypothesis (IH): Eπ [f (Shπ |s1 )] ≥ R(k, h − 1) · OP T ′ .


                      Eπ [f (Shπ )] = f (s1 ) + Eπ [f (Shπ |s1 )]
                                    ≥ f (s1 ) + R(k, h − 1)(OP T − f (s1 ))
                                    = f (s1 )(1 − R(k, h − 1)) + R(k, h − 1) · OP T.

    We verify that R(k, h − 1) < 1. Since h ≥ 1, R(k, h − 1) ≤ Ck,h−1 = 1+T (k,h−1)        1
                                                                                             . Since
T (k, h − 1) > 0, R(k, h − 1) < 1. Thus, 1 − R(k, h − 1) > 0.
    By the condition for Case 1 and Lemma 7.20, f (s1 ) ≥ t · Eπ [f (oπ1 )] ≥ t · OP T /k.

                                 t · OP T
                  Eπ [f (Shπ )] ≥         (1 − R(k, h − 1)) + R(k, h − 1) · OP T
                                     k                           
                                          t          t
                               = OP T ·     + 1−         R(k, h − 1) = Ak,h · OP T.
                                          k         k

     Case 2: Eπ [f (uπ1 )] < t · Eπ [f (oπ1 )]. We set sπ1 = v1π .
     We consider the remaining subproblem I ′ (π). It depends on π because both sπ1 and the remaining
OPT elements Eopt   ′ (π) = E
                               opt \ {o1 } depend on π. The parameters are (k − 1, h − 1). The function
                                        π

is fπ (T ) = f (T |s1 ).
     ′              π

     We analyze the expected value over π. Eπ [f (Shπ )] = Eπ [f (sπ1 )] + Eπ [f (Shπ |sπ1 )].
     By the IH applied to the subproblem (noting that conditional on oπ1 , the remaining elements are
still uniformly permuted): Eπ [f (Shπ |sπ1 )] ≥ R(k − 1, h − 1) · Eπ [OP T ′ (π)].

                                                        77
      The expected optimum of the subproblem is Eπ [OP T ′ (π)] = Eπ [f (Eopt     ′ (π)|sπ )]. By submodular-
                                                                                         1
ity: Eπ [OP T ′ (π)] ≥ OP T − Eπ [f (sπ1 ∪ oπ1 )].
      Combining these: Eπ [f (Shπ )] ≥ Eπ [f (sπ1 )] + R(k − 1, h − 1) · (OP T − Eπ [f (sπ1 ∪ oπ1 )]).
      We bound the loss term Eπ [f (sπ1 ∪ oπ1 )]. Note that if sπ1 ̸= oπ1 , then sπ1 must have arrived before
oπ1 , and since sπ1 = v1π is the best element up to oπ1 , it must be that sπ1 = uπ1 .
      We can obtain a bound using the Case 2 condition.

  Eπ [f (sπ1 ∪ oπ1 )] = Eπ [f (oπ1 )] + Eπ [f (sπ1 |oπ1 )]
                     = Eπ [f (oπ1 )] + P (sπ1 = oπ1 )E[f (sπ1 |oπ1 )|sπ1 = oπ1 ] + P (sπ1 ̸= oπ1 )E[f (sπ1 |oπ1 )|sπ1 ̸= oπ1 ].

If sπ1 = oπ1 , the marginal gain is 0. If sπ1 ̸= oπ1 , then sπ1 = uπ1 .

          Eπ [f (sπ1 ∪ oπ1 )] = Eπ [f (oπ1 )] + P (sπ1 ̸= oπ1 )E[f (uπ1 |oπ1 )|sπ1 ̸= oπ1 ]
                              ≤ Eπ [f (oπ1 )] + Eπ [f (uπ1 )]. (By submodularity and non-negativity)

    Using the Case 2 condition Eπ [f (uπ1 )] < t · Eπ [f (oπ1 )]: Eπ [f (sπ1 ∪ oπ1 )] < (1 + t)Eπ [f (oπ1 )].
    Substituting back into the main inequality: Eπ [f (Shπ )] > Eπ [f (sπ1 )] + R(k − 1, h − 1) · (OP T −
(1 + t)Eπ [f (oπ1 )]).
    By definition of v1π , f (sπ1 ) ≥ f (oπ1 ) for all π. Thus Eπ [f (sπ1 )] ≥ Eπ [f (oπ1 )]. Eπ [f (Shπ )] >
Eπ [f (oπ1 )](1 − (1 + t)R(k − 1, h − 1)) + R(k − 1, h − 1) · OP T .
    Crucially, by Lemma 7.24 (which relies on the MTC), the coefficient 1 − (1 + t)R(k − 1, h − 1) is
non-negative. We substitute Eπ [f (oπ1 )] ≥ OP T /k (Lemma 7.20).


                                  OP T
                  Eπ [f (Shπ )] >      (1 − (1 + t)R(k − 1, h − 1)) + R(k − 1, h − 1) · OP T
                                   k                                   
                                           1        1+t
                                = OP T ·     + 1−          R(k − 1, h − 1) = Bk,h · OP T.
                                           k         k

    In both cases, Eπ [f (Shπ )] ≥ min(Ak,h , Bk,h )·OP T ≥ R(k, h)·OP T . The induction is complete.

Analysis of the Specific Recurrence
We now analyze the recurrence using a specific threshold function that optimizes the fluid limit.

The Optimal Threshold Function We define the threshold function T ∗ (k, h) = √k2k+h2 .

Lemma 7.26. The threshold function T ∗ (k, h) satisfies the Monotonic Threshold Condition (MTC).

Proof. We need to show T ∗ (k, h) ≤ T ∗ (k − 1, h − 1) for k ≥ 2, h ≥ 1. Let g(x) = (1 + x2 )−1/2 . g(x)
is strictly decreasing for x ≥ 0. T ∗ (k, h) = g(h/k). T ∗ (k − 1, h − 1) = g((h − 1)/(k − 1)). We
compare x1 = h/k and x0 = (h − 1)/(k − 1). Since (k, h) ∈ D, k ≥ h. k ≥ h =⇒ −k ≤ −h =⇒
hk − k ≤ hk − h. k(h − 1) ≤ h(k − 1). Since k ≥ 2, k > 0 and k − 1 > 0. (h − 1)/(k − 1) ≤ h/k. So
x0 ≤ x1 . Since g(x) is decreasing, g(x1 ) ≤ g(x0 ). Thus T ∗ (k, h) ≤ T ∗ (k − 1, h − 1).

   Since T ∗ (k, h) satisfies the MTC, Theorem 7.25 applies. The approximation ratio of the Tree
Algorithm is lower bounded by R(k, k) derived using this threshold function.




                                                              78
Solving
   √    the Recurrence We now prove that the recurrence defined with T ∗ (k, h) evaluates to
2 − 2 when h = k.
Theorem
   √    7.27. Let R(k, h) be the recurrence defined using T ∗ (k, h). Then for all k ≥ 1, R(k, k) =
2 − 2.
    To prove this, we introduce continuous helper functions that represent the fluid limit of the
recurrence and use them to establish bounds.
    The Continuous Helper Functions Let ρ : [0, 1] → [0, 1] and t : [0, 1] → (0, 1] be defined as:
                                                    p
                                    ρ(x) = 1 + x − x2 + 1,
                                                1
                                     t(x) = √       .
                                               2
                                              x +1
Note that T ∗ (k, h) = t(h/k). We define the comparison function P (k, h) = ρ(h/k) for k ≥ 1.
   We establish key properties of these functions.
                                                                                          √
Lemma 7.28 (Properties of ρ(x) and t(x)).       1. Boundary values: ρ(0) = 0, ρ(1) = 2 − 2.
   2. Concavity: ρ(x) is strictly concave on [0, 1].
                                           1
                                                           √
   3. Convex Auxiliary Function: W (x) = 1−ρ(x) =              x2 + 1 + x is strictly convex on [0, 1].

   4. Rate 1 Identity: ρ′ (x) = t(x)(1 − ρ(x)). (Equivalently, W ′ (x) = W (x)t(x)).
   5. Rate 2 Identity: ρ′ (x)(1 − x) = 1 − (1 + t(x))ρ(x).
                                   1
   6. Threshold Relation: ρ(x) ≤ 1+t(x) .

  7. Monotonicity of t: t(x) is strictly decreasing on [0, 1].
                        √                          √           √
Proof. 1. ρ(0) = 1 + 0 − 1 = 0. ρ(1) √
                                        =1+1−    √
                                                     2 = 2 − 2.
                                          2            2              2     2
   2. ρ′ (x) = 1 − √xx2 +1 . ρ′′ (x) = − x +1−x(x/
                                               x2 +1
                                                      x +1)
                                                            = − (x  +1)−x
                                                                 (x2 +1)3/2
                                                                                     1
                                                                            = − (x2 +1)3/2 . Since ρ (x) < 0,
                                                                                                    ′′

ρ(x) is strictly concave.
   3. W ′ (x) = √xx2 +1 + 1. W ′′ (x) = (x2 +1)
                                             1
                                               3/2 . Since W (x) > 0, W (x) is strictly convex.
                                                             ′′
                                                √                     √
   4. t(x)(1 − ρ(x)) = √x12 +1 (1 − (1 + x − x2 + 1)) = √x12 +1 ( x2 + 1 − x) = 1 − √xx2 +1 = ρ′ (x).
                √
   5. Let S = x2 + 1. t(x) = 1/S, ρ(x) = 1+x−S, ρ′ (x) = 1−x/S. LHS = (1−x/S)(1−x) = 1−
                           2
x−x/S+x2 /S = 1−x+ x S−x . RHS = 1−(1+1/S)(1+x−S) = 1−(1+x−S+ 1+x                   S −1) = 1−x+S− S .
                                                                                                         1+x
                   2                      2
RHS = 1 − x + S −(1+x)
                                                                     2
                        S    = 1 − x + (x +1)−1−x
                                            S      = 1 − x + x S−x . LHS = RHS. (There was a slight
algebraic error in the previous draft’s proof of this point, which is corrected here).
    6. We want ρ(x)(1 + t(x)) ≤ 1. By the Rate 2 identity,
                                                         √     this is equivalent to 1 −√(1 − x)ρ′ (x) ≤ 1,
or (1 − x)ρ (x) ≥ 0. Since x ∈ [0, 1], 1 − x ≥ 0. Since x + 1 > x, ρ′ (x) = 1 − x/ x2 + 1 > 0. The
             ′                                              2

inequality holds. Equality holds only if x = 1.
    7. t′ (x) = − 21 (x2 + 1)−3/2 (2x) = −x(x2 + 1)−3/2 . This is negative for x > 0.

   We next give the proof of Theorem 7.27.

Proof. We use a "Diagonal Sandwich" argument. We first prove a global lower bound R(k, h) ≥
P (k, h), and then prove a tight upper bound at the diagonal h = k.
    Step 1: Global Lower Bound. We prove by strong induction that R(k, h) ≥ P (k, h) = ρ(h/k)
for all (k, h) ∈ D, k ≥ 1.
    Base Conditions:

                                                    79
   • h = 0, k ≥ 1: R(k, 0) = 0. P (k, 0) = ρ(0) = 0. Holds.
                                             √                                      √
   • k = 1. R(1, 1). t1,1 = T ∗ (1, 1) = 1/ 2. A1,1√= t1,1 + (1 − t1,1 )R(1, 0) = 1/ 2. B1,1 =
                                                              √                    √      √
     1+(1−(1+t1,1 ))R(0, 0) = 1. C1,1 = 1+1/ 1√
                                                  =  √ 2 = 2− 2. R(1, 1) = min(1/ 2, 1, 2− 2).
               √                   √            2     2+1   √                        √
     Since 2 − 2 ≈ 0.586 and 1/ 2 ≈ 0.707, R(1, 1) = 2 − 2. P (1, 1) = ρ(1) = 2 − 2. Holds.
    Inductive Step: Fix (k, h) with k ≥ 2, h ≥ 1. Assume R(k ′ , h′ ) ≥ P (k ′ , h′ ) for all (k ′ , h′ ) < (k, h)
lexicographically. Let x = h/k. Let t = T ∗ (k, h) = t(x). We must show Ak,h , Bk,h , Ck,h ≥ P (k, h) =
ρ(x).
                                 1
    Analysis of Ck,h : Ck,h = 1+t(x) . By Lemma 7.28.6, ρ(x) ≤ 1+t(x) 1
                                                                         . So Ck,h ≥ P (k, h).
    Analysis of Ak,h : Let ∆x = 1/k. The previous state is (k, h − 1). The ratio is x′ = (h − 1)/k =
x − ∆x. By IH, R(k, h − 1) ≥ P (k, h − 1) = ρ(x − ∆x).

                                 Ak,h ≥ t(x)∆x + (1 − t(x)∆x)ρ(x − ∆x).

We want to show this is ≥ ρ(x).

                               t(x)∆x(1 − ρ(x − ∆x)) ≥ ρ(x) − ρ(x − ∆x).

Let W (x) = 1/(1 − ρ(x)).
                                    t(x)∆x           1      1
                                              ≥           −      .
                                   W (x − ∆x)   W (x − ∆x) W (x)
Multiplying by W (x)W (x − ∆x) (which is positive):

                                   t(x)∆xW (x) ≥ W (x) − W (x − ∆x).

                                   W (x − ∆x) ≥ W (x) − W (x)t(x)∆x.
By Lemma 7.28.4 (Rate 1 Identity), W ′ (x) = W (x)t(x).

                                     W (x − ∆x) ≥ W (x) − W ′ (x)∆x.

This inequality holds because W (x) is strictly convex (Lemma 7.28.3). A convex function lies
above its tangent line: W (y) ≥ W (x) + W ′ (x)(y − x). Setting y = x − ∆x yields the result. Thus
Ak,h ≥ P (k, h).
   Analysis of Bk,h : The previous state is (k − 1, h − 1). Let x1 = h/k and x0 = (h − 1)/(k − 1).
By IH, R(k − 1, h − 1) ≥ P (k − 1, h − 1) = ρ(x0 ).
                                                             
                                        1          1 + t(x1 )
                                Bk,h ≥ + 1 −                    ρ(x0 ).
                                        k              k
We want to show this is ≥ ρ(x1 ).
                                 1
                                   (1 − (1 + t(x1 ))ρ(x0 )) ≥ ρ(x1 ) − ρ(x0 ).
                                 k
                                                                                 h(k−1)−k(h−1)
    We analyze the relationship between 1/k and the ratios. x1 − x0 = hk − h−1
                                                                           k−1 =     k(k−1)    =
                                 k−1−(h−1)
k(k−1) .                                       k−1 . Therefore, x1 − x0 = k (1 − x0 ). So 1/k =
 k−h
          1 − x0 = 1 − h−1k−1 =     k−1     = k−h                          1

(x1 − x0 )/(1 − x0 ). (This assumes h < k, so x0 < 1).
    Case 1: 1 ≤ h < k. In this case x0 < x1 < 1. 1 − x0 > 0 and x1 − x0 > 0. Substituting 1/k:
                              x1 − x 0
                                       (1 − (1 + t(x1 ))ρ(x0 )) ≥ ρ(x1 ) − ρ(x0 ).
                              1 − x0

                                                       80
                                      1 − (1 + t(x1 ))ρ(x0 )   ρ(x1 ) − ρ(x0 )
                                                             ≥                 .
                                             1 − x0               x1 − x 0
The RHS is the slope of the secant line of ρ(x) from x0 to x1 . Since ρ(x) is concave (Lemma 7.28.2),
the slope of the secant is less than the slope of the tangent at x0 :

                                               ρ(x1 ) − ρ(x0 )
                                                               < ρ′ (x0 ).
                                                  x1 − x 0
It is sufficient to prove:
                                          1 − (1 + t(x1 ))ρ(x0 )
                                                                 ≥ ρ′ (x0 ).
                                                 1 − x0
By Lemma 7.28.5 (Rate 2 Identity) applied at x0 : ρ′ (x0 ) = 1−(1+t(x0 ))ρ(x0 )
                                                                  1−x0          . We need to show:

                                 1 − (1 + t(x1 ))ρ(x0 ) ≥ 1 − (1 + t(x0 ))ρ(x0 ).

                                       (1 + t(x0 ))ρ(x0 ) ≥ (1 + t(x1 ))ρ(x0 ).
Since h ≥ 1, x0 = (h − 1)/(k − 1) ≥ 0. ρ(x0 ) ≥ 0. We need t(x0 ) ≥ t(x1 ). Since t(x) is decreasing
(Lemma 7.28.7) and x0 < x1 , this holds. Thus Bk,h ≥ P (k, h) when√h < k.                           √
   Case 2: h = k. (k ≥ 2). We want to show Bk,k ≥ P (k, k) = 2 − 2. Here x1 = 1. t(x1 ) = 1/√2.
The previous state is (k − 1, k − 1). x0 = 1. By IH, R(k − 1, k − 1) ≥ P (k − 1, k − 1) = ρ(1) = 2 − 2.
                                                        √ !
                                        1         1 + 1/ 2          √
                                Bk,k ≥ + 1 −                   (2 − 2).
                                        k             k
                             √
We check if this is ≥ 2 −        2.
                                                                 √ !
                                 1       √                 1 + 1/ 2      √
                                   ≥ (2 − 2) −          1−           (2 − 2)
                                 k                             k
                                                          √ !!                           √ !
                  1       √                         1 + 1/ 2          √            1 + 1/ 2
                    ≥ (2 − 2) 1 −               1−              = (2 − 2)                    .
                  k                                     k                              k
                                                        √        √
                                               1 ≥ (2 − 2)(1 + 1/ 2).
              √ √               √ √            √        √       √
                              (2− 2)( 2+1)
RHS = (2 − 2) √2+1    2
                          =         √
                                      2
                                              = 2 2+2−2−
                                                     √
                                                       2
                                                            2
                                                              =   √2 = 1. The inequality 1 ≥ 1 holds.
                                                                    2
Thus Bk,k ≥ P (k, k).
    Conclusion of Step 1: We have shown Ak,h ≥ P (k, h), Bk,h ≥ P (k, h), and Ck,h ≥ P (k, h).
Therefore, R(k, h) = √min(Ak,h , Bk,h , Ck,h ) ≥ P (k, h) for all (k, h) ∈ D. In particular, R(k, k) ≥
P (k, k) = ρ(1) = 2 − 2.
    Step 2: Diagonal Upper Bound. We consider          √ the upper bound
                                                                       √     at h √
                                                                                  = k. By definition of
the recurrence, R(k, k) ≤ Ck,k . tk,k = T (k, k) = k/ k + k = k/ 2k = 1/ 2.
                                          ∗               2     2          2


                                                  1           1        √
                                      Ck,k =            =       √ = 2 − 2.
                                               1 + tk,k   1 + 1/ 2
                 √
So, R(k, k) ≤ 2 − 2.                                               √
    Conclusion√ of the Proof (Diagonal Sandwich):   √ Since 2 − 2 ≤ R(k, k) (Step 1) and
R(k, k) ≤ 2 − 2 (Step 2), we must have R(k, k) = 2 − 2 for all k ≥ 1.


                                                           81
Conclusion
We have rigorously established the connection between the Tree Algorithm for submodular maximiza-
tion under adversarial injections and a generalized recurrence relation featuring a state-dependent
threshold T (k, h).

  1. We proved that if the threshold function satisfies the Monotonic Threshold Condition (MTC),
     the recurrence R(k, h) provides a lower bound on the expected approximation ratio of the
     algorithm (Theorem 7.25), correctly utilizing the inequalities inherent to submodular functions.
                                                              √
  2. We defined a specific threshold function T ∗ (k, h) = k/ k 2 + h2 and verified it satisfies the
     MTC (Lemma 7.26).

  3. We analyzed the
                  √ resulting recurrence using a "Diagonal Sandwich" argument and proved that
     R(k, k) = 2 − 2 (Theorem 7.27).
                                                                                        √
    This implies that the Tree Algorithm achieves an approximation ratio of at least 2 − 2 ≈ 0.5857
in the adversarial injections model. This improves upon the 0.55 approximation derived in [47] using
a fixed threshold analysis.




                                                82
7.5   Streaming Algorithms: Entropy, Low Rank Approximation, and Chamfer
      Distance
Written by Ying Feng, David P. Woodruff, and Samson Zhou.

Problem Context
This case study examines several fundamental problems in streaming algorithms, but where the
focus is on settings where space efficiency alone is not the only resource constraint. In addition to
minimizing memory usage, modern systems often operate under limitations on write bandwidth,
communication, or the frequency with which internal state can be modified. We consider four
representative problems:

  1. Entropy Estimation: Can the Shannon entropy of a data stream be estimated with signifi-
                                                             √
     cantly fewer internal state changes than the current Õ( n) bound?

  2. Consistent LRA: Is the optimal low-rank approximation subspace stable under row updates?

  3. Efficient Encoding for LRA: Can low-rank sketches computed on different parts of the
     data be globally compressed without losing accuracy?

  4. Chamfer Distance: Can the fast ℓ1 Chamfer distance algorithm be extended to the ℓ2
     metric?

Together, these problems highlight a common theme: understanding how algorithmic guarantees
interact with more refined complexity measures beyond space, such as stability, recourse, and internal
state changes.

AI Contribution
Across these problems, the model played a role in identifying structural properties that were not
explicit in prior analyses and in turning those observations into concrete algorithmic improvements.

   • Entropy: The model observed that the standard algorithm only queries moments Fp for p ≈ 1,
     avoiding the high-variance regime (p = 2) entirely. This immediately implied a polylogarithmic
     bound on the number of internal state changes.

   • LRA Stability: The model produced a proof showing that the optimal rank-k subspace
     changes by at most a constant amount under a single row insertion, using eigenvalue interlacing
     and dimension arguments.

   • LRA Encoding: The model suggested decomposing local sketches into a global “head” and
     quantized “tail,” and proved that this representation preserves projection costs with small
     additive error.

   • Chamfer Distance: The model adapted the quadtree-based algorithm from ℓ1 to ℓ2 , intro-
     ducing a dimensionality reduction step (Johnson-Lindenstrauss) to handle high dimensions
     efficiently.




                                                 83
7.5.1   Internal State Changes for Streaming Entropy
In streaming algorithms, the foremost priority is typically to minimize the amount of memory
(space) required to process a stream, since data streams can be massive and cannot be stored in full.
Recently, [63] noted that minimizing the number of internal state changes, which counts how often
the algorithm updates its memory representation, is also a reasonable secondary priority, particularly
in settings with limited write bandwidth or distributed monitoring systems.
    In the streaming model considered here, the stream consists of a sequence of elements from
[n] = {1, 2, . . . , n}, and the algorithm maintains a frequency vector f ∈ Zn≥0 , where fi denotes
the number of times item i has appeared in the data stream, so that each update to the stream
increments the corresponding coordinate of f by one. The number of internal state changes is the
number of times the algorithm modifies its memory state over the duration of the data stream.
    The Fp moment     Pnestimation problem asks to approximate the p-th frequency moment of the stream,
                             p
defined as Fp = i=1 fi . Accurate Fp estimation is fundamental because many other statistics
can be expressed in terms of frequency moments. In particular, Fp moments are central tools in
streaming algorithms for estimating norms, identifying heavy hitters, and, as in this discussion,
approximating Shannon entropy.


     Please try to improve the paper by identifying and solving an open question from it.
     For your proof, adhere to: ⟨rigor text⟩.


          We identify and resolve an open question arising from the analysis of the entropy estimation
          algorithm presented in Section 3.3 of the paper.
          Open Question:
          The paper establishes in Theorem 3.8 that the Shannon
                                                             √      entropy of an insertion-only stream
          can be estimated with an ε-additive error using Õ( n/ε
                                                               √
                                                                  O(1)
                                                                       ) internal state changes (assuming
          m = poly(n)) and polylogarithmic space. This Õ( n) bound stems from the worst-case
          complexity of Fp moment estimation for p ∈ (0, 2], which is Õ(n1−1/p ), maximized as p → 2.
                                               √
          The open question is: Can this Õ( n) upper bound on the number of state changes for
          streaming entropy estimation be improved?
          We answer this question affirmatively. By analyzing the specific moments required by the
          underlying [HNO08] framework used in the paper, we show that they are sufficiently close to
          1 such that the polynomial dependence on n vanishes.



              Figure 12: Model identification of open problem and progress direction


    Shannon entropy, defined as H = − ni=1 pi log pi with pi = fi /∥f ∥1 , measures the uncertainty
                                             P
or information content in a dataset. Estimating Shannon entropy is a fundamental problem with
numerous applications, including network traffic analysis (to detect anomalies or DDoS attacks),
database summarization (to quantify diversity), natural language processing (to measure information
content of text corpora), and data compression (to determine optimal coding schemes). Because
entropy is sensitive to the entire distribution of frequencies, accurately approximating it in a streaming
setting is challenging and typically relies on sophisticated techniques, such as Chebyshev interpolation
of multiple Fp moment estimates, as observed by [58].
    [63] analyzed the internal-state complexity required for approximating Fp in one-pass insertion-

                                                     84
only streams. Their main theorem distinguishes two regimes: forp ∈ (0, 1], a (1 + ε)-approximation
can be achieved with high probability using only poly 1ε , log n internal state changes, while for
p ≥ 1, estimating Fp requires O(n e 1−1/p ) internal state changes, which can be as large as Õ (√n)
when p = 2. In their discussion of Shannon entropy, they interpreted the Chebyshev interpolation
observation by [58] and noted that it requires evaluating multiple Fp moment estimates. They
assumed the exponents lie in the range p ∈ (0, 2), which implies that estimating F2 could be necessary.
                                         √
Because F2 sketches can incur up to n internal state changes, this led to the conclusion that
                                              √
Shannon entropy estimation inherits an O( n) state-change cost.
     However, upon closer examination, the model noticed that all evaluation points in the interpolation
procedure are of the form 1 + yi , where yi = f (cos(iπ/k)), and showed that 1 + yi ∈ (0, 1) for all i,
c.f., Lemma 7.31. This implies that the entropy algorithm never requires Fp estimates for p ≥ 1, and
all required
            frequency moments lie strictly within the low-p regime. Consequently, the worst-case
Õ n1−1/p state-change barrier from the p ≥ 1 region     is avoided. It then follows that the necessary
Fp estimates for p ∈ (0, 1) use only poly ε , log n internal state changes, c.f., Theorem 7.29. As a
                                            1
                                                   

result, the Shannon entropy algorithm   can compute  an additive                   using      1
                                                                                                       
                                                                  ε-approximation        Õ  ε2 + log n
bits of space and poly 1ε , log n internal state changes, significantly improving upon the previously
                                 
             √
believed Õ ( n) bound.
Theorem 7.29. [63] Let ε ∈ (0, 1) be an approximation parameter, δ ∈ (0, 1/3) be a failure proba-
bility, and n be the domain size. There exists a one-pass insertion-only streaming algorithm
for the p-th frequency moment Fp :
                                             a (1+ε)-approximation (w.h.p.) using poly log n, 1ε , log 1δ
                                                                                                                
   1. For p ∈ (0, 1]: The algorithm achieves
                                    
      internal state changes and Õ     1
                                        ε2
                                           (log log n + log 1ε ) + loglog(1/ε)
                                                                        log(1/ε) log n
                                                                               bits of space.
                                                             h                 i
                                                               cp − Fp ≤ ε · Fp ≥ 2 , with Õ n1−1/p
                                                                                                     
   2. For p ≥ 1: The algorithm outputs F    cp such that Pr F
                                                                                    3
      internal state changes. The space complexity depends on p:
         • If p ∈ [1, 2]: Space is Õ ε4+4p
                                        1
                                            
                                              · polylog(mn).
         • If p > 2: Space is Õ ε4+4p n
                                     1    1−2/p
                                                
                                                  .


Algorithm 6 Additive approximation of empirical Shannon entropy
Require: Error parameter ε̃, points {y0 , . . . , yk }
 1: for i = 0, . . . , k do
 2:    Compute F̃1+y     i , a (1 + ε̃)-approx.
                                              of F1+yi
                                   1+yi
 3:    H̃(yi ) ← − log F̃1+yi /∥A∥1+y    /yi
                                     i
                                 1+yi
 4:    T̃ (yi ) ← 1 − F̃1+yi /∥A∥1+yi /yi
 5: end for
 6: return estimate of H(0) or T (0) by interpolating {H̃(yi )} or {T̃ (yi )}


Lemma 7.30. [58] To achieve an additive ε-approximation of the Shannon entropy, it suffices to
implement Algorithm 6 with ε̃ = 12(k+1)ε 3 log m using points y0 , . . . , yk with k = log 1ε + log log m and
                                  2        2
yi = f (cos(iπ/k)) for f (y) = (k ℓ)·y−ℓ·(k
                                     2k2 +1
                                            +1)                  1
                                                , where ℓ = (2(k+1) log m .
                                                               2         2
Lemma 7.31. Let yi = f (cos(iπ/k)) for f (y) = (k ℓ)·y−ℓ·(k
                                                     2k2 +1
                                                            +1)                 1
                                                                , with ℓ = (2(k+1) log m . Then
1 + yi ∈ (0, 1) for all i ≥ 0.

                                                      85
Proof. Observe that 1 + yi < 1 if and only if f (cos(iπ/k)) < 0 or equivalently,

                                  (k 2 ℓ) · cos(iπ/k) − ℓ · (k 2 + 1) < 0.

Since ℓ > 0, this is equivalent to k 2 · cos(iπ/k) < (k 2 + 1), which holds for all i, since cos(iπ/k) ≤ 1
for all i.
    Similarly, observe that 1 + yi > 0 if and only if f (cos(iπ/k)) > −1 or equivalently,

                             (k 2 ℓ) · cos(iπ/k) − ℓ · (k 2 + 1) > −(2k 2 + 1).

Since | cos(iπ/k)| ≤ 1 for all i, then

                            (k 2 ℓ) · cos(iπ/k) − ℓ · (k 2 + 1) > −ℓ(2k 2 + 1).

Then, the desired claim follows because ℓ ∈ (0, 1).

From Theorem 7.29 and Lemma 7.31, we have:

Corollary 7.32. Given an accuracy parameter ε ∈ (0, 1) and a stream of length m = poly(n) over a
universe of size n, there exists a one-pass insertion-only streaming algorithm that outputs an additive
ε-approximation H  b to the entropy H of the data stream with high probability, using Õ 12 + log n
                                                                                            ε
bits of space and poly 1ε , log n internal state changes.
                                 


7.5.2   Consistent Low-Rank Approximation
Low-rank approximation is a central tool in data analysis and machine learning. Given a matrix
A ∈ Rn×d , the goal is to find a rank-k subspace, i.e., orthogonal matrix V ∈ Rk×d , that minimizes the
approximation error ∥A − AV ⊤ V ∥2F , measured in Frobenius norm. In static settings, this problem
is well understood: the optimal solution is given by the top k singular vectors of A, and efficient
algorithms with strong guarantees are known.
    Many modern applications, however, are inherently dynamic. Data arrive sequentially, are
corrected, or are removed, and low-rank approximations are recomputed repeatedly as part of larger
pipelines. In these settings, approximation quality alone is not sufficient. Each time the output
subspace changes, downstream systems may need to retrain models, update features, or revalidate
decisions, all of which can be expensive. This motivates a second objective beyond accuracy, namely
consistency.
    Consistent low-rank approximation is a relatively new problem formulation that makes this
tradeoff explicit. Instead of computing a single low-rank approximation to a fixed dataset, the
algorithm is asked to maintain a sequence of near-optimal subspaces as the data evolve, while keeping
the changes between successive outputs small. Formally, we fix an accuracy parameter ε > 0 and a
target rank k. The input is a matrix A ∈ Rn×d that changes over time, e.g., rows of A are revealed
incrementally, or there is a sequence of updates to entries of A. At each time step t, the algorithm
observes the current matrix A(t) and outputs a rank-k orthogonal matrix V (t) ∈ Rk×d .
    The first requirement is accuracy. For every t, the subspace V (t) should give a near-optimal
rank-k approximation to A(t) , in the sense that

                             ∥A(t) − A(t) (V (t) )⊤ V (t) ∥2F ≤ (1 + ε) · OPTt ,

where
                                  OPTt = min ∥A(t) − A(t) V ⊤ V ∥2F
                                           V ∈Rk×d


                                                     86
is the optimal rank-k approximation error at time t.
    The second requirement is stability. As the matrix A evolves, the sequence of outputs V (1) , . . . , V (n)
should change minimally. We formalize this desideratum through the notion of recourse, de-
fined as the squared Frobenius distance between consecutive subspaces. For two rank-k matrices
R, T ∈ Rk×d , let PR and PT be the orthogonal projection matrices onto their row spans, and define
Recourse(R, T ) = ∥PR − PT ∥2F . The goal is to minimize the total recourse
                                         n
                                         X
                                               Recourse(V (t) , V (t−1) ),
                                         t=2

while still meeting the approximation guarantee at every time step. This formulation reflects the
practical intuition behind consistent low-rank approximation. The algorithm is allowed to adapt as
the input evolves, but large or frequent rotations of the maintained subspace are discouraged, since
they correspond to costly changes in downstream representations.
    This notion of consistency is not addressed by standard streaming algorithms such as Frequent
Directions [50], which may change their output subspaces frequently in order to achieve strong
approximation guarantees, e.g., even small perturbations in the data can cause a complete change in
the reported subspace and leading to large recourse. However, the model noticed that the optimal
rank-k subspace is inherently stable under row insertions. In other words, the recourse between the
optimal subspaces before and after a row insertion is bounded by a fixed constant.


     Analyze whether the optimal rank-k subspace is stable under rank-one updates when the
     stream has polynomially bounded condition number.
     Provide a rigorous proof establishing the resulting recourse bound.


           We show that when a single row is appended to a matrix, the optimal rank-k right singular
           subspace changes by at most a constant amount. Specifically, if Vt−1    ∗
                                                                                       and Vt∗ denote the
           top-k subspaces before and after the row insertion, then the squared Frobenius distance
           between their projection matrices satisfies Recourse(Vt−1
                                                                  ∗
                                                                     , Vt∗ ) ≤ 8. This establishes that the
           optimal subspace is inherently stable under row insertions, providing a concrete bound on
           recourse in the row-arrival model.


Figure 13: Model-generated resolution of a stability question in consistent low-rank approximation


   In particular, the model produced a complete and correct proof showing:
Theorem 7.33. Suppose A(t) is obtained from A(t−1) by adding one new row. Let Vt−1    ∗  and Vt∗
denote the optimal rank-k subspaces of the matrices before and after the update. Then the change
                                                  ∗ , V ∗ ) ≤ 8.
between these two subspaces is at most Recourse(Vt−1   t

Proof. Consider the covariance matrices

                             Bt−1 = (A(t−1) )⊤ A(t−1) ,          Bt = (A(t) )⊤ A(t) .

Since A(t) is just A(t−1) with the new row At appended, we have

                                               Bt = Bt−1 + A⊤
                                                            t At ,


                                                        87
so Bt is a rank-one positive semidefinite update of Bt−1 . By the Eckart-Young theorem, the optimal
rank-k subspaces Vt−1
                    ∗ and V ∗ are spanned by the top k eigenvectors of B
                              t                                            t−1 and Bt , respectively.
   Next, we consider how much these subspaces can change. Define the subspace orthogonal to the
new row as
                                      Sa = {v ∈ Rd : At v = 0},
which has dimension d − 1, assuming v is nonzero. Let W = Vt−1      ∗ ∩ S be the part of the old
                                                                            a
subspace that is unaffected by the new row. Using basic dimension counting, it follows that
dim(W ) ≥ dim(Vt−1∗ ) − (d − (d − 1)) = k − 1.

    For any vector w ∈ W , we have Bt w = Bt−1 w, so w is an eigenvector for both covariance matrices
with the same eigenvalue. Let λ1 ≥ . . . ≥ λd be the eigenvalues of Bt−1 and µ1 ≥ . . . ≥ µd those of
Bt . By the Cauchy interlacing theorem,

                          µ1 ≥ λ1 ≥ µ2 ≥ λ2 ≥ . . . ≥ µk ≥ λk ≥ µk+1 ≥ . . .

Since W ⊆ Vt−1∗ , its vectors correspond to eigenvalues among the top k of B
                                                                              t−1 , and by interlacing
they lie within the top k + 1 eigenvectors of Bt . From this, we conclude that the intersection of the
old and new subspaces has dimension at least k − 2.
    Finally, consider the projection matrices Pt−1 and Pt onto Vt−1∗ and V ∗ . Let W = V ∗ ∩ V ∗ ,
                                                                            t          ∩     t−1    t
and let P∩ be the projection matrix onto W∩ .
    If dim(W∩ ) = k, the subspaces are identical and recourse is zero. If dim(W∩ ) = k − 1, then

                              Pt−1 = P∩ + u1 u⊤
                                              1,        Pt = P∩ + u2 u⊤
                                                                      2,

where u1 and u2 are unit vectors orthogonal to the shared subspace. Then Pt − Pt−1 = u2 u⊤
                                                                                         2 − u1 u1 ,
                                                                                                 ⊤

so by the triangle inequality

                         Recourse(Pt , Pt−1 ) ≤ 2∥u1 u⊤  2         ⊤ 2
                                                      1 ∥F + 2∥u2 u2 ∥F = 4.

Similarly, if dim(W∩ ) = k−2, the difference involves four rank-one terms, giving Recourse(Pt , Pt−1 ) ≤
8.

    This result has immediate algorithmic implications and has been incorporated into a work
accepted for publication at ICLR 2026 [98]. Although the theorem is stated for row insertions, the
result also applies to row deletions by symmetry. Moreover, changes to a single entry of a matrix can
be expressed as a row deletion followed by a row insertion. Thus, the result directly implies a constant
upper bound on recourse for these operations, thereby establishing a O(1) amortized recourse bound
for the dynamic model, where the matrix is updated by a sequence of entry modifications, row
insertions, or row deletions.

7.5.3   Global Efficient Encoding for Low-Rank Approximation
In many applications, we work with a large matrix A ∈ Rn×d , where both dimensions n and d may be
very large. Directly storing or processing such matrices can be computationally expensive, especially
when we only care about their action on low-dimensional subspaces or rank-k approximations.
Low-rank approximations (LRA) provide a natural tool to reduce storage and computation by
approximating A with a matrix of rank at most k ≪ min(n, d), while preserving important properties
such as the Frobenius or spectral norm. A more powerful guarantee is achieving a projection-cost
preservation. In our specific context, the rows of an input matrix A ∈ Rn×d arrive sequentially and



                                                   88
the goal is to compute a matrix B ∈ Rm×d such that for all rank-k orthogonal projection matrices
P ∈ Rd×d , we have

                      (1 − ε)∥A − AP ∥2F ≤ ∥B − BP ∥2F ≤ (1 + ε)∥A − AP ∥2F ,

where ∥ · ∥F denotes the Frobenius norm.
   A common setting arises when A can be decomposed as a concatenation of blocks,

                                        A = Q1 ◦ Q2 ◦ · · · ◦ Qm ,

where each block Qi ∈ Rni ×d represents a submatrix of A. This block structure naturally appears in
streaming or distributed scenarios, where each Qi corresponds to a portion of the data arriving at
different times or stored across multiple nodes. For each block, one can compute a local low-rank
approximation Wi that summarizes Qi while approximately preserving its projection costs, i.e., the
squared Frobenius norm under all rank-k orthogonal projections. In particular, it is known that it
suffices for Wi to just have r := Õ εk2 subsampled and reweighted rows of Qi [23]. However, naïvely
storing all local approximations Wi may still be expensive, especially if m or the number of rows in
each local approximation Wi is large. The goal of the global efficient encoding is to compress these
local sketches into a representation that:

   1. Uses significantly fewer bits of storage compared to storing all entries of Wi explicitly.

   2. Allows efficient reconstruction of Wi′ such that the concatenated matrix W ′ = W1′ ◦· · ·◦Wm
                                                                                                 ′ still

      forms a good approximation to the original matrix A in the sense of low-rank approximation
      and projection-cost preservation.

   3. Preserves provable guarantees on the Frobenius norm and spectral norm errors, as well as
      the Loewner ordering of Gram matrices, which are important in downstream tasks such as
      regression, PCA, and clustering.

    The model suggested the global efficient encoding for low-rank approximation depicted in
Algorithm 7.
    The main idea behind the global encoding is to separate each block Wi into a “head” component
and a “tail” residual with respect to a global low-rank subspace determined by the top-k singular
vectors of a global sketch B of A. Specifically, for a matrix B that is a (1 + ε)-PCP of A, we compute
its top-k right singular vectors Vk and define the projections

                                   PB = Vk Vk⊤ ,         PB⊥ = Id − PB .

The head coefficients Hi = Wi Vk capture the component of Wi in the top-k global subspace, while
the tail residual Ti = Wi PB⊥ contains the remaining information orthogonal to this subspace. The
tail residuals are then quantized entry-wise to a precision ε′ , providing a compressed representation
while controlling the additive projection-cost error. Reconstruction simply sums the head and tail
contributions:
                                         Wi′ = Hi Vk⊤ + Ti′ .
    This approach ensures that the concatenated reconstructed matrix W ′ satisfies a (1 ± O(mε))
projection-cost preservation guarantee with respect to A, while using significantly less storage than
the naive concatenation of the Wi . Moreover, the method preserves Loewner orderings of the Gram
matrices up to small additive errors, which is crucial for applications that rely on positive semi-definite


                                                    89
Algorithm 7 Global efficient encoding for low-rank approximation
Require: Accuracy parameter ε < 12 , matrix A = Q1 ◦ . . . ◦ Qm , matrix B ∈ Rr×d that is a
    (1 + ε)-PCP of A, matrices W1 , . . . , Wm ∈ Rr×d where each Wi is a (1 + ε)-PCP of Qi , rank k
Ensure: Encoded matrices W1′ , . . . , Wm ′

 1: Set quantization precision ε′ ≤ √ε , where Cε = 1−ε1+ε
                                     4 C ε
 2: Compute the SVD of B and let Vk ∈ Rd×k be the top-k right singular vectors
 3: Define projection matrices PB = Vk Vk⊤ and PB
                                                ⊥ =I −P
                                                    d   B
 4: Store Vk with high precision (e.g., O(log n) bits per entry)
 5: for i = 1 to m do
 6:    Compute head coefficients Hi = Wi Vk and store with high precision
 7:    Compute tail residual Ti = Wi PB⊥
 8:    Quantize Ti entry-wise to relative precision ε′ to obtain Ti′ and store
 9: end for
10: for i = 1 to m do
11:    Reconstruct Wi′ = Hi Vk⊤ + Ti′
12: end for
13: return W ′ = W1′ ◦ . . . ◦ Wm
                                ′




approximations. The algorithm is thus globally efficient in both space and reconstruction time, while
providing strong theoretical guarantees on approximation quality.
    Toward establishing correctness of the proposed efficient encoding, the model first suggested the
following auxiliary lemma that bounds the Frobenius norm of a projected matrix.

Lemma 7.34. For any projection matrix Q, it holds that

                                        ∥Wi Q∥2F ≤ Cε ∥BQ∥2F ,
           1+ε
where Cε = 1−ε .

Proof. Since Wi is a (1 + ε)-PCP of Qi , we have

                                      ∥Wi Q∥2F ≤ (1 + ε)∥Qi Q∥2F .

Because A is the concatenation of the matrices Qj , it follows that
                                             m
                                             X
                                ∥AQ∥2F =           ∥Qj Q∥2F ≥ ∥Qi Q∥2F .
                                             j=1

Moreover, as B is a (1 + ε)-PCP of A, we obtain

                                      ∥BQ∥2F ≥ (1 − ε)∥AQ∥2F .

Combining these inequalities yields
                                             1+ε
                              ∥Wi Q∥2F ≤         ∥BQ∥2F = Cε ∥BQ∥2F .
                                             1−ε




                                                    90
Using this result, the model then showed that the global efficient encoding results in a PCP with small
additive error, which for our downstream applications can ultimately be absorbed into multiplicative
error.
Lemma 7.35. For every rank-k orthogonal projection matrix P ∈ Rd×d and each i ∈ [m],

         ∥Wi − Wi P ∥2F − ε∥B − BP ∥2F ≤ ∥Wi′ − Wi′ P ∥2F ≤ ∥Wi − Wi P ∥2F + ε∥B − BP ∥2F .

Proof. Let Q = Id − P and fix an arbitrary i ∈ [m]. It suffices to show that

                                     ∥Wi′ Q∥2F − ∥Wi Q∥2F ≤ ε∥BQ∥2F .

Define Ei = Wi′ − Wi = Ti′ − Ti . Then,

                 ∥Wi′ Q∥2F = ∥(Wi + Ei )Q∥2F = ∥Wi Q∥2F + 2⟨Wi Q, Ei Q⟩F + ∥Ei Q∥2F .

Consequently,

         ∥Wi′ Q∥2F − ∥Wi Q∥2F = 2⟨Wi Q, Ei Q⟩F + ∥Ei Q∥2F ≤ 2∥Wi Q∥F ∥Ei Q∥F + ∥Ei Q∥2F ,

where the inequality follows from the Cauchy-Schwarz inequality. Since Q is a projection matrix, we
have ∥Ei Q∥F ≤ ∥Ei ∥F ≤ ε′ ∥Ti ∥F , which implies

                          ∥Wi′ Q∥2F − ∥Wi Q∥2F ≤ 2ε′ ∥Wi Q∥F ∥Ti ∥F + (ε′ )2 ∥Ti ∥2F .

By Lemma 7.34, ∥Wi Q∥2F ≤ Cε ∥BQ∥2F . Furthermore, since PB denotes the projection onto the
top-k singular vectors of B,

                             ∥Ti ∥2F = ∥Wi PB⊥ ∥2F ≤ Cε ∥BPB⊥ ∥2F ≤ Cε ∥BQ∥2F .

Substituting these bounds yields

                              ∥Wi′ Q∥2F − ∥Wi Q∥2F ≤ Cε 2ε′ + (ε′ )2 ∥BQ∥2F .
                                                                    

Choosing ε′ ≤ 4√εC completes the proof.
                    ε

    Finally, we analyze the space complexity of the global efficient encoding.
Lemma 7.36. The global encoding scheme can be represented using
                                                                
                                                       1
                   O kd log n + mrk log n + mrd log ′ + log log n
                                                      ε
bits of space in total.
Proof. The storage cost consists of three components. First, the matrix Vk ∈ Rd×k is stored at high
precision, requiring O(kd log n) bits. Second, each head coefficient matrix Hi ∈ Rr×k is stored at
high precision, contributing a total of O(mrk log n) bits across all i ∈ [m]. Finally, each tail residual
Ti′ is stored using entry-wise quantization with precision parameter ε′ . This quantization requires
O log ε1′ + log log n bits per entry, giving a total of
                     

                                                             
                                                   1
                                    O mrd log ′ + log log n
                                                  ε
bits for all residuals. Summing these three contributions gives the stated space bound.

                                                      91
   The existence of a global efficient encoding has immediate implications for low-rank approximation.
In particular, it enables the construction of projection-cost preservation sketches in a single pass
over the data, using
                                 k2
                                                                  
                                                 1                  dk
                                   2
                                     · polylog     , log(ndκ) + Õ
                                 ε               ε                  ε2
words of space and input-sparsity runtime. Here, κ is a term related to the “condition number” of the
data stream, which essentially captures the worst-case arrival of the matrix over the data stream, e.g.,
if “small” rows arrive first and the “larger” rows arrive later. This quantitatively matches the best
known offline coreset constructions while improving over previous streaming algorithms by removing
extra logarithmic factors, making the space essentially independent of n for low-rank projections.
Consequently, high-accuracy low-rank approximations are achievable efficiently in streaming settings,
closing the gap between streaming and offline performance and enabling fast, memory-efficient
dimensionality reduction and randomized matrix computations.

7.5.4    Even Faster Algorithm for the Chamfer Distance
The Chamfer distance is a popular quantification of the dissimilarity between point clouds. For any
two d-dimensional point sets A, B of sizes up to n, the Chamfer distance from A to B is defined as
                                                X
                                   CH(A, B) =        min ∥a − b∥
                                                           b∈B
                                                     a∈A

where ∥ · ∥ is the underlying norm defining the distance between two points, such as the Euclidean
or Manhattan distance.
     While the naive algorithm for the Chamfer distance takes O(dn2 ) time, recently, [7] proposed
the first near-linear-time algorithm to approximate the Chamfer distance. Their algorithm works for
the underlying norm being ℓ1 or ℓ2 , and outputs an (1 ± ε)-approximation in time O(dn log(n)/ε2 ).
When ε is a constant, this leaves a gap of O(log n) between the upper bound and the trivial Ω(dn)
lower bound.
     Towards closing this gap, [39] proposed a faster algorithm for the ℓ1 norm. This leads to the
natural question of whether the improvement generalizes to the ℓ2 norm. The model answers this
question in affirmative.
     Initial Improvement in the Low-Dimensional Regime
     As summarized in Figure 14, with a generic initial prompt, the model identifies the open problem
and the key ingredient to focus on. It then gives            √ a proof in the ℓ2 norm, which improves over the
runtime of [7] in the low-dimensional regime ( d ≪ log n/ log log n).
     The proof focuses on a data structure called quadtree. A quadtree of depth t is defined by a
random offset vector z ∼ [0, 2t ]d . It assigns every point in Rd with a sequence of t hash values, using
t nested grids shifted by z. Concretely, for any a ∈ Rd and any integer k such that 0 ≤ k ≤ t, it
hashes hk (a) := (⌈ a12+z
                        k
                          1
                            ⌉, ⌈ a22+z
                                    k
                                      2
                                        ⌉, · · · , ⌈ ad2+z
                                                        k
                                                           d
                                                             ⌉).
     [39] used two independent quadtrees to estimate the nearest neighbor distance for all a ∈ A in
ℓ1 , i.e. estimating minb∈A ∥a − b∥1 for all a ∈ A. The model follows a similar proof structure and
analyzes the behavior of quadtrees in ℓ2 as follows:
                                                                                                √
Lemma 7.37. For all a, b ∈ Rd and 0 ≤ k ≤ t, if hk (a) = hk (b), then ∥a − b∥2 ≤ 2k d.

Proof. If hk (a) = hk (b), then√ a, b lie in the same d-dimensional cube of side-length 2k . The ℓ2
diameter of such a cube is 2k d.



                                                     92
Lemma 7.38. With probability 1 − O(1/n), the following holds simultaneously for all a, b, k: If
hk (a) = hk (b), then ∥a − b∥2 ≤ 2k · 3 log n.

Proof. Lemma 3.4 of [39] shows that ∀a, b, k : ∥a − b∥1 ≤ 2k · 3 log n with probability 1 − O(1/n).
Combining this with the fact that ∥a − b∥1 ≥ ∥a − b∥2 concludes the proof.

    With the above lemmas, the model shows that in expectation, two quadtrees output good
estimation to opta := minb∈A ∥a − b∥2 for all a ∈ A. The estimator Da is defined as:

   1. Identifying the smallest k̃ such that hk̃ (a) = hk̃ (b) for some b ∈ B across the two quadtrees.4

   2. Assigning Da := ∥a − b∥2 for arbitrary b such that hk̃ (a) = hk̃ (b).

Lemma 7.39. With probability 1 − O(1/n), it holds for all a ∈ A that EDa ≤ F · opt(a), where
F = O(min(d3/2 , d log n)).

Proof. We need the following fact:
Fact 7.40 ([7]). Pr[hk (a) ̸= hk (b)] ≤ ∥a−b∥
                                          2k
                                             1
                                               .
    Similar to Theorem 3.5 in [39], we condition on Lemma 7.38 and fix a ∈ A. Let k ∗ := ⌈log(opta )⌉.
And let Ek be the event that k̃ = k (recall that we identified a unique √
                                                                        k̃ when defining the estimator).
If Ek occurs, the estimator Da is bounded by 2k · F̃ for F̃ = O(min( d, log n)). Thus
                                              X
                                     EDa ≤         Pr[Ek ] · 2k · F̃ .
                                                        0≤k≤t

We split the sum based on k ≤ k ∗ and k > k ∗ . The first part is bounded by
                                           X
                                   F̃ opta      Pr[Ek ] ≤ F̃ opta .
                                                       k≤k∗

For the second part (k > k ∗ ), we fix b∗ := arg minb∈B ∥a − b∥2 . Event Ek implies that hk−1 (a) ̸=
hk−1 (b∗ ) in two independent quadtrees. Therefore,
                                                     √
                                    ∥a − b∗ ∥1 2       d∥a − b∗ ∥2 2 d(opta )2
                        Pr[Ek ] ≤ (           )  ≤ (              ) = 2k−2
                                      2k−1               2k−1         2
                      √
because ∥a − b∗ ∥1 ≤ d∥a − b∗ ∥2 . Now we can bound the summation for k > k ∗ :
              X                               X d(opt )2                            X opt
                                                         a                                      a
                     Pr[Ek ] · 2k · F̃ ≤ F̃                   · 2k ≤ 4F̃ d · opta                   = O(F̃ dopta ).
                                                     22k−2                                 2k
              k>k∗                            k>k∗                                  k>k∗

Thus, EDa = O(F̃ d) · opta , i.e. the approximation factor is F = O(min(d3/2 , d log n)).

    As outlined in Figure 14, the rest of the algorithm in [39] works the same regardless of the
underlying norm. And the total runtime can be derived from the bound on the approximation factor
F . This leads to the conclusion (Theorem 7.41).




  4
      For simplicity, assume that we chose t so that there always exists such k̃ ≤ t.


                                                              93
     Please try to improve the paper by identifying and solving an open question from it.
     For your proof, adhere to: ⟨rigor text⟩.


          [39] presents an improved algorithm for approximating the Chamfer distance in the ℓ1 metric,
          achieving a runtime of O(dn(log log(n) + log 1ε )/ε2 ). However, they note that extending
          this improvement to the ℓ2 metric is challenging. The standard approach, used in prior
          work [7] , involves embedding the points from ℓ2 to ℓ1 , which takes O(dn log(n)/ε2 ) time,
          thereby eliminating the speedup. The authors leave finding a faster embedding algorithm, or
          consequently a faster ℓ2 Chamfer distance algorithm, as an open problem.
          We address this open problem by analyzing the performance of the proposed algorithmic
          framework when adapted directly to the ℓ2 metric. We show that the new techniques can
          yield a faster algorithm for the ℓ2 Chamfer distance when the dimension d is relatively small.
          Overview of the Approach: The algorithm presented in the paper consists of three main
          components:
             1. QuadTree: A fast procedure using quadtrees to compute crude estimates Da of
                opta := minb∈B ∥a − b∥. This runs in O(dn log log n) time.
             2. Tournament: An algorithm to efficiently compute O(1)-approximations of opta for a
                batch of sampled points.
             3. Rejection Sampling: A framework that uses the estimates from QuadTree and Tourna-
                ment to perform importance sampling and estimate the Chamfer distance.
          The efficiency of the overall algorithm depends on the approximation factor achieved by
          the QuadTree step. If QuadTree provides an F -approximation in expectation (i.e., EDa ≤
          F · opta ), the overall runtime is dominated by the QuadTree and Tournament steps. The
          Tournament runs in time roughly O(n(d + F/ε2 ) log(F/ε2 )).
          For the ℓ1 metric, the authors prove F = O(min(d, log n)). This leads to the improved
          O(dn log log n/ε2 ) runtime. We analyze the approximation factor F when the framework is
          applied to the ℓ2 metric.
          [Proofs to Lemma 7.37, 7.38, 7.39]
          Conclusion: We have shown that the techniques introduced in the paper can be adapted
          directly to the ℓ2 metric to yield a faster algorithm for the Chamfer distance, provided the
          dimension d is small.

          Theorem 7.41. There is an algorithm that computes a (1 + ε)-approximation to the
          Chamfer distance under the ℓ2 metric in time O(n(F/ε2 )(log(F/ε2 ) + log log n)), where
          F = O(min(d3/2 , d log n)).

          This runtime constitutes an improvement over the previous O(dn log(n)/ε2 ) when d1/2 (log d+
          log(1/ε) + log log n) = o(log n).



                   Figure 14: Model identification of problem and initial solution.


   Refined Improvement for Any Dimension. Following the initial response of the model, we
asked the model to focus on improving the high-dimensional case. the model refines the previous
Lemma 7.39 and combines it with a fast Johnson-Lindenstrauss Transform. This gives an algorithm

                                                    94
for ℓ2 that matches the runtime of ℓ1 in [39] for any dimension d, thus improving the previous best
runtime from [7].

Lemma 7.42 (Refinement of Lemma 7.39).
                                    √ With probability 1 − O(1/n), it holds for all a ∈ A that
EDa ≤ F · opt(a), where F = O(min(d, d log n)).

     Compared
        √     to Lemma 7.39, this proof switches from √ℓ1 to ℓ2 in a later stage. This switch applies
∥ · ∥1 ≤ d∥ · ∥2 , thus introducing an extra factor of d. Intuitively, we want this to happen after
multiplying the probabilities of two independent quadtrees. This is precisely what the model changes.

Proof. As before, we P fix b := arg min
                             ∗
                                           b∈B ∥a − b∥2 . But now we define k := ⌈log(∥a − b ∥1 )⌉. We
                                                                             ∗              ∗

again split EDa ≤ 0≤k≤t Pr[Ek ] · 2 · F̃ based on k ≤ k and k > k , and bound the first part by
                                        k                     ∗          ∗
      ∗ P
         k≤k∗ Pr[Ek ] ≤ F̃ ∥a − b ∥1 . For the second part,
F̃ 2k                            ∗


  X                               X ∥a − b∗ ∥1                              X ∥a − b∗ ∥1
                                                                      ∗
         Pr[Ek ] · 2k · F̃ ≤ F̃      (   k−1
                                               )2
                                                  · 2 k
                                                        ≤ 4F̃ · ∥a − b  ∥ 1        k
                                                                                         = O(F̃ ∥a − b∗ ∥1 ).
                                       2                                         2
  k>k∗                             ∗
                                  k>k                                    k>k ∗

                                  √                                                  √
Thus, EDa = O(F̃ )·∥a−b∗ ∥1 ≤ O(F̃ d)·opta . The approximation factor is F = O(min(d, d log n)).


    As mentioned in Figure 15, this gives a O(dn(log d + log log n + log 1ε )/ε2 ). For d ≪ poly(n)-
time algorithm, this improves the best known runtime of ℓ2 . Moreover, for d ≤ poly(log n), this
already matches the best known runtime of ℓ1 . Finally, to handle larger d, the model applies fast
Johnson-Lindenstrauss transform to reduce the dimension, and then estimate the Chamfer distance.
    Note that while the model claims the existence of an (unconditional) O(dn)-time JL transform,
which we are not aware of, there indeed exists an O(dn log m)-time JL transform that reduces the
dimension to m = O(log2 n/ε2 ) [35], which suffices for the final conclusion (Theorem 7.43).




                                                         95
     Focus on improving the high dimensional regime. Concretely, try (1) using an ℓ2 -native
     scheme, and (2) modifying later stages of the algorithm.


         We begin by rigorously analyzing the performance of the QuadTree estimator when adapted
         to the ℓ2 metric. This analysis provides a tighter bound than the one presented in the
         preamble and establishes the baseline performance.
         [Proof to Lemma 7.42]
         This leads to O(dn(log d + log log n + log 1ε )/ε2 ) total runtime. If d is large (e.g., d = poly(n)),
         the runtime matches the previous state-of-the-art O(dn log n/ε2 ), offering no substantial
         improvement.
         Strategy (1) proposes using an ℓ2 -native approach. We can achieve this by employing
         dimensionality reduction via the Johnson-Lindenstrauss (JL) transform before applying the
         framework. This reduces the dimension from d to m = O(log n/ε2 ), thereby reducing the
         impact of the dimension on the approximation factor F .
         Fast Johnson-Lindenstrauss (JL) Transform: Given n points in Rd and ε > 0. Let
         m = O(log n/ε2 ). There exists a randomized linear map S : Rd → Rm such that with high
         probability, it preserves all pairwise ℓ2 distances within (1 ± ε). Furthermore, the map S can
         be applied to all n points in total time O(dn).

         Theorem 7.43. Assuming the fast Johnson-Lindenstrauss (JL) transform, there is an
         algorithm that computes a (1 + ε)-approximation to the Chamfer distance under the ℓ2 metric
         in time O(dn(log log n + log 1ε )/ε2 ).

         [For large d, this is justified by plugging in m into the previous time bound.]



                  Figure 15: Model refinement of the analysis and final solution.


    We have incorporated this result, together with other results on ℓp versions of Chamfer and in
streaming models, into a submission [40]. The model was also very helpful for verifying correctness
of different parts of the submission.




                                                       96
8       Resolving Conjectures and Complex Derivations
Distinct from the algorithmic optimizations in the previous section, here the AI acts as a heavy-
lifting theoretical mathematician. These case studies showcase the AI’s ability to build theory from
scratch—executing complex continuous derivations, extending theorems via measure theory, and
constructing novel computational reductions.

8.1      Information Theory: The Courtade-Kumar Conjecture
Written by Adel Javanmard.

AI Contribution The AI made two distinct contributions to the Courtade-Kumar conjecture.
First, it successfully generalized a known theorem to unbalanced functions and improved entropy
bounds in the high-noise regime using hypercontractivity and Taylor expansions (Section 8.1.1).
Second, it made structural progress on the “unsymmetrized” version of the conjecture by analyzing
continuous relaxations and proving local optimality (Section 8.1.2).

8.1.1     Part I: Generalization to Unbalanced Functions
The Courtade-Kumar Conjecture An intriguing question in information theory, formalized by
Courtade and Kumar [25] in 2014, asks how to optimally compress a noisy signal into a single bit
to preserve information about the original source. Specifically, let X n be i.i.d Bernoulli(1/2) and
let Y n be a noisy observation of X n , generated by passing the input through a memoryless binary
symmetric channel with a crossover probability 0 < α < 12 . The core optimization challenge is to
identify a Boolean function b : {0, 1}n → {0, 1} that maximizes the mutual information I(b(X n ); Y n ),
or equivalently I(b(Y n ); X n ). Courtade and Kumar conjectured that this quantity is bounded by

                                             I(b(X n ); Y n ) ≤ 1 − H(α) ,                                                    (29)

where H(α) = −α log α − (1 − α) log(1 − α) represents the binary entropy function. This upper
bound is achieved when b is a “dictatorship” function, defined as b(X1 , . . . , Xn ) = Xi for any fixed
index i ∈ {1, . . . , n}. Essentially, the conjecture posits that no Boolean function is more informative
than simply selecting the value of a single coordinate.

Recent Progress and Partial Results In their original paper [25], the authors established the
following result, which is a weaker version5 of the conjecture:

        Theorem 1[25]: If b(X n ) is equiprobable, then
                                           n
                                           X
                                                 I(b(X n ); Yi ) ≤ 1 − H(α) .                                          (30)
                                           i=1

This is still a significant result given that the left hand side is the sum of n mutual information
terms, while the right-hand side does not depend on n. Also, note that Theorem 1 above is only
proved in the case of equiprobable boolean functions. In Section IV of [25], the authors ask the
following question:
    5                                                                                             Pn
    It is a weaker form of the main conjecture because (29) is equivalent to I(b(X n ); Y n ) =    i=1 I(Y
                                                                                                             i−1
                                                                                                                   , b(X n ); Yi ) ≤
1 − H(α) by independence of Yi ’s.



                                                            97
     Does Theorem 1 continue to hold when b(X n ) is not equiprobable? Unfortunately, our
     Fourier-analytic proof of Theorem 1 appears to fail in this setting. Nonetheless, we feel
     that establishing this generalization of Theorem 1 should be considerably easier than
     establishing the main conjecture.

   Since its introduction, the conjecture (29) has generated substantial interest, leading to several
partial results. Chandar and Tchamkerten [20] established the bound:

                                      I(b(X n ); Y n ) ≤ (1 − 2α)2 .                                   (31)

Building on this,
              q Ordentlich, Shayevitz, and Weinstein [80] derived the following bound for the
interval 12 (1 −   3) ≤ α ≤ 2:
                   1        1

                                                                  
                                    log(e)                  log(e)
                           n     n
                     I(b(X ); Y ) ≤                2
                                           (1 − 2α) + 9 1 −          (1 − 2α)4                         (32)
                                      2                       2

This result provides a tighter bound than (31) within the range 13 ≤ α ≤ 12 . Leveraging this
improved bound, Samorodnitsky [84] successfully proved that the conjecture holds for all α ≥ 12 − δ,
where δ > 0 is an absolute constant. While these results represent significant milestones, the main
conjecture (29) remains open in its full generality.

Partial Resolution of the Courtade-Kumar Conjecture by Gemini We asked Gemini to
try to solve the Courtade-Kumar conjecture and provided their paper as input.


     Can you prove Conjecture 1 stated in this paper or make progress on it (“Which Boolean
     Functions Maximize Mutual Information on Noisy Inputs”)?


           We analyze the conjectures and open questions presented in the paper “Which Boolean
           Functions Maximize Mutual Information on Noisy Inputs?” by Courtade and Kumar. The
           main conjecture (Conjecture 1) remains open. However, we provide a complete resolution
           to the first open question posed in Section IV, generalizing Theorem 1 to arbitrary (non-
           balanced) Boolean functions.



               Figure 16: Model identification of open problem and progress direction


    As illustrated in Figure 16, while the model could not solve the main conjecture, it identified the
open problem from Section IV of the paper and provided a complete resolution. Specifically it proves
the following theorem, which confirms that Theorem 1 holds even when b(X n ) is not equiprobable.

Theorem 8.1 (Generalized Theorem 1). Let X n be i.i.d. uniform on {−1, 1}n , and let Y n be the
output of a BSC(α) with input X n . For any Boolean function b : {−1, 1}n → {−1, 1},
                                     n
                                     X
                                           I(b(X n ); Yi ) ≤ 1 − H(α).
                                     i=1




                                                     98
    Gemini’s proof employs Fourier-analytic techniques analogous to those in [25] to establish
Theorem 1, yet Gemini independently refined the derivation of Theorem 1 to address scenarios where
the distribution of b(X n ) is non-uniform. For this problem, while we maintained minimal oversight
throughout the process, many intermediate steps were cryptically generated, requiring us to query
the system multiple times for clarification.
    The formal proof of Theorem 8.1 is presented below. The proof outline involves an analysis of
the optimization landscape, where we demonstrate that the objective function—viewed as a function
of the squared level-1 Fourier coefficients—is convex. We then characterize the extreme points of the
feasible region defined by Parseval’s identity and spectral bounds. Finally, the proof establishes a
non-trivial inequality involving derivatives of the mutual information expression with respect to ρ.
A key distinction from the proof strategy in [25, Theorem 1] is our demonstration that the objective
function is maximized by Boolean functions that are monotone in each coordinate (defined via a 1-d
compression operator). Using this structure we can impose tighter constraints on the feasible set
which allows us to generalize the result of [25, Theorem 1] to all Boolean functions.

Strengthening the High-Noise Regime Results We further explored potential improvements
to the results established by Samorodnitsky [84], which proved that the Courtade-Kumar conjecture
holds in the high-noise regime—specifically, when the noise parameter α is sufficiently close to 1/2
(i.e., λ = 1 − 2α < δc for an absolute constant δc > 0). Initially, when provided with [84] as input,
the system produced a concise summary of the methodology in [84] without offering immediate novel
insights.


     Can you make further progress on the conjecture using this work?


          We analyze the maximization of a convex functional related to entropy under the noise oper-
          ator, focusing on the conjecture that the Dictatorship function is the optimizer. We provide
          a rigorous proof for the high noise regime, following the methodology of A. Samorodnitsky
          in “On the entropy of a noisy function”.



              Figure 17: Model identification of open problem and progress direction


    However, this summary served as a useful primer for distilling the core proof techniques. Through
iterative prompting and self-correction cycles, we tasked the system with refining Samorodnitsky’s
result. After several rounds of checking its own logic, the model claimed to have established an
improvement on the threshold δc .
Technical Verification and Error Correction. While the initial output appeared structurally
sound and cited relevant literature correctly, a manual review revealed subtle technical inaccuracies.
Specifically, the system invoked the Bonami-Beckner hypercontractivity inequality with an incorrect
assumption:
                                                                              √
      “For a function h supported on Fourier levels ≥ k, and q ≥ 2, ∥h∥q ≤ ( q − 1)k ∥h∥2 .”

    Our attempts to verify this claim led us to realize that the inequality holds for functions supported
on Fourier levels ≤ k, rather than ≥ k. Upon being prompted to resolve this discrepancy, the system
initially defended its original statement. However, after several rounds of probing, it provided a proof


                                                    99
that allowed us to pinpoint a specific line where an inequality direction had been flipped. Once this
error was identified, the system conceded the mistake—illustrating its tendency to present subtle
errors with high confidence.
Final Result and Methodology. The system eventually derived an alternative proof that bypassed
these initial errors. By incorporating our feedback regarding a seemingly trivial (but actually false)
claim, the model produced a rigorous proof that improved upon the result of [84]. This final proof
technique synthesizes the methodology of [84] with higher-moment analysis to establish optimal
Fourier concentration for highly informative Boolean functions. We summarize the main result
below.

Theorem 8.2 (Extended Range for the Conjecture). There exists an absolute constant δopt > 0
such that if the noise parameter λ ≤ δopt , the Courtade-Kumar conjecture holds. Furthermore, δopt
is strictly larger than the thresholds previously established in [84].

Observations on AI-Assisted Research. Our interactions with the system on these theoretical
problems yielded several key insights into its utility as a research partner:

   • Effective “Jumpstarting”: The model is exceptionally adept at identifying relevant ideas
     across disparate fields and literature, making it an excellent tool for generating an initial line
     of thought.

   • The “Mid-PhD” Analogy: Its performance is comparable to a mid-level PhD student; it is
     most effective when the researcher provides a high-level proof strategy and tasks the system
     with making the steps rigorous or connecting logical gaps. The results of this part were used
     to write a full paper [62] using a “vibe proving” methodology. In this workflow, we defined the
     lemmas and tasked the AI with drafting the proofs, which were then rigorously verified and
     refined by us.

   • Scale and Complexity Limits: While the system excels at solving isolated, small-scale
     problems (akin to IMO-style challenges), it still struggles with the expansive, multi-stage
     reasoning required for long-term research projects. Researchers must remain vigilant, as the
     system can be confidently incorrect regarding subtle technical details.

Proof of Theorem 8.1                 Due to the complexity of this derivation, the AI struggled to
generate a complete, flawless proof in a single shot. The formal proof below is the result of our
“vibe-proving” methodology: it was drafted and rigorously verified by the human researchers, who
stitched together the correct intermediate lemmas, structural insights, and Fourier-analytic techniques
discovered iteratively by the AI.

Proof. Recall the crossover probability 0 < α < 12 and define ρ = 1 − 2α.
   Any Boolean function b : {−1, +1}n → {−1, 1} can be written in terms of its Fourier coefficients
as                                            X
                                     b(xn ) =     b̂(S)ΠS (xn ) ,
                                              S⊆[n]

where ΠS (xn ) = Πi∈S xi are the orthonormal basis for the Fourier transform and {b̂(S)}S⊆[n] are the
Fourier coefficient defined by
                                      b̂(S) = Eb(X n )ΠS (X n ) .
For S = ∅, we define ΠS (xn ) = 1.

                                                 100
   Let µ = E[b] = b̂(∅) be the bias, and zi = b̂({i}) be the level-1 Fourier coefficients. The objective
function is:
                                              n
                                              X                   n
                                                                  X
                                     L(b) =         I(b; Yi ) =     (H(b) − H(b|Yi )).               (33)
                                              i=1                 i=1

Since the range of b is {−1, +1}, the entropy H(b) is determined by the bias Pr[b = 1] = 1+E[b]
                                                                                           2    = 1+µ
                                                                                                   2 ,
                                 1+µ
hence we can write H(b) = H( 2 ). Using relation (34) from [25], we have

                                                                    1 + µ + ρyi zi
                                        Pr[b = 1|Yi = yi ] =                       ,
                                                                          2
and since the marginal distribution of Yi is uniform on {−1, +1}, we get
                                       1
                        H(b|Yi ) =       [H(Pr[b = 1|Yi = 1]) + H(Pr[b = 1|Yi = −1]) .]              (34)
                                       2
Therefore we obtain H(b|Yi ) = hµ (zi ), where
                                                                     
                                   1     1 + µ + ρz    1    1 + µ − ρz
                          hµ (z) := H                 + H                 .
                                   2          2        2         2

Let gµ (z) = H(b) − hµ (z). By (33), we want to maximize ni=1 gµ (zi ) subject to the constraints on
                                                         P
the Fourier coefficients of a Boolean function.

Step 1: Reduction to Monotone Functions. Let f : {−1, 1}n → {−1, 1} be a Boolean function.
The 1-d compression operator along coordinate i, denoted as Ci , rearranges the values of the function
along the i-th dimension to make it “monotone” while preserving the total number of 1s. Specifically,
for any input x ∈ {−1, 1}n , let x = (x∼i , xi ), where x∼i are all bits except i. The operator acts on
the pair of values (f (x∼i , −1), f (x∼i , 1)):

                                             if xi = 1 and f (x∼i , −1) + f (x∼i , 1) ≥ 0
                                    
                                    1
                                    
                  Ci f (x∼i , xi ) = 1       if xi = −1 and f (x∼i , −1) + f (x∼i , 1) = 2         (35)
                                      −1 otherwise
                                    
                                    

We show that 1-d compression increases the objective function L(b).
Lemma 8.3. Let b̃ be the compression of b along coordinate j, making it non-decreasing in xj . The
Fourier coefficients satisfy:

   1. zi (b̃) = zi (b) for i ̸= j.

   2. |zj (b̃)| ≥ |zj (b)|.

    Note that hµ (z) = hµ (−z) and the function hµ (z) is decreasing in |z|, hence by Lemma 8.3
hµ (zj (b̃)) ≤
             Phµ (zj (b)).
    Thus, i H(b|Yi ) decreases under compression and L(b) = i I(b; Yi ) increases. This implies
                                                                   P
that the maximum must be attained by a function b that is monotone along each coordinate. We
assume b is non-decreasing, so zi (b) ≥ 0, for i ∈ [n], by the next lemma.
Lemma 8.4. Suppose that b is a non-decreasing Boolean function, i.e., for any input x, changing the
i-th bit from −1 to 1 either increases the function value or keeps it the same: b(x∼i , −1) ≤ b(x∼i , +1).
Then zi (b) := b̂({i}) ≥ 0.

                                                             101
   We will also use the following lemma in the next step.
Lemma 8.5. For any Boolean function b : {−1, 1}n → {−1, 1}, with µ = E[b] and zi = b̂({i}) the
level-1 Fourier coefficients, we have zi ≤ 1 − |µ|.

Step 2: Optimization over Monotone Functions. We analyze the structure of the optimization
                                            √
problem. Let wi = zi2 . Define ψµ (w) = gµ ( w). It can be shown that ψµ (w) is strictly convex for
                         √
w > 0 (Equivalently, hµ ( w) is strictly concaveP
                                                in w).
   We want to maximize the convex function ni=1 ψµ (wi ) subject to constraints on the Fourier
coefficients.
   The constraints are:
  1. wi ≥ 0
     Pn
  2.   i=1 wi ≤ 1 − µ = R (Parseval’s theorem).
                     2   2


  3. wi ≤ (1 − |µ|)2 = C 2 (Since 0 ≤ zi ≤ 1 − |µ| by Lemmas 8.4 and 8.5).
The maximum of a convex function over this polytope is attained at an extreme point. Let
K = R2 /C 2 = (1 − µ2 )/(1 − |µ|)2 = (1 + |µ|)/(1 − |µ|). We analyze two cases based on the
relationship between n and K. Without loss of generality, assume µ ≥ 0.

Step 3: Bounding the Maximum (Case 1: n ≥ K). If n ≥ K, the constraint             wi ≤ R2 is the
                                                                                 P
dominant constraint. The extreme points (up to permutation) have k = ⌊K⌋ coordinates equal to
C 2 , one coordinate equal to θC 2 (where θ = K − k), and the rest are 0. The maximum value is:

                                    M (µ) = kψµ (C 2 ) + ψµ (θC 2 ).

We verify that ψµ (0) = 0. Note that ψµ (0) = gµ (0) = H(b) − hµ (0). Since hµ (0) = H( 1+µ
                                                                                         2 ) = H(b),
we have ψµ (0) = 0. Using the convexity of ψµ (w) and ψµ (0) = 0:

              ψµ (θC 2 ) = ψµ (θC 2 + (1 − θ)0) ≤ θψµ (C 2 ) + (1 − θ)ψµ (0) = θψµ (C 2 ).

Thus, the maximum is bounded by:

              M (µ) ≤ kψµ (C 2 ) + θψµ (C 2 ) = (k + θ)ψµ (C 2 ) = Kψµ (C 2 ) = Kgµ (C).

Recall that C = 1 − µ and K = (1 + µ)/(1 − µ), and so µ and C are determined by K as follows:
                                          K −1              2
                                     µ=        ,     C=        .
                                          K +1            K +1
Let MK (ρ) := Kgµ (C), where we made the dependence on ρ = 1 − 2α explicit in the notation. We
aim to show MK (ρ) ≤ 1 − H(α).
   Writing MK (ρ) more explicitly, we have
                                                                        
                                     K     1 + µ + ρC     K     1 + µ − ρC
                MK (ρ) = KH(b) − H                      − H
                                     2          2         2          2
                                                                    
                                   K        K      K +ρ     K      K −ρ
                        = KH             − H              − H              ,
                                 K +1       2      K +1     2      K +1

where we used that H(b) = H( 1+µ                                        1+ρ
                               2 ) = H( K+1 ). Note that M1 (ρ) = 1 − H( 2 ) = 1 − H(α). We
                                         K

want to show MK (ρ) ≤ M1 (ρ) for K ≥ 1.

                                                  102
    Observe that MK (0) = 0 for all K, so it suffices to show that the derivative with respect to ρ
satisfies MK
           ′ (ρ) ≤ M ′ (ρ).
                     1
    The derivative is calculated as:
                                                                      
                              ′          K              (1 + ρ)(K + ρ)
                            MK (ρ) =               ln                    .
                                     2(K + 1) ln 2      (1 − ρ)(K − ρ)
        1+ρ
Let A = 1−ρ . Then M1′ (ρ) = 2 ln
                                1
                                  2 ln(A). The inequality MK (ρ) ≤ M1 (ρ) is equivalent to:
                                                            ′       ′

                                                       
                                       K         K +ρ
                                           ln A           ≤ ln A.
                                     K +1        K −ρ
Rearranging this inequality yields:
                                                                    
                           K +ρ                     1 + ρ/K          1+ρ
                    K ln            ≤ ln A ⇔ K ln             ≤ ln         .
                           K −ρ                     1 − ρ/K          1−ρ
Let f (x) = x1 ln( 1+x ). The inequality is equivalent to f (ρ/K) ≤ f (ρ). The Taylor series is
          P∞ x2j1−x
f (x) = 2 j=0 2j+1 , which is strictly increasing for x > 0. Since K ≥ 1, we have ρ/K ≤ ρ, thus
f (ρ/K) ≤ f (ρ).
    The inequality MK′ (ρ) ≤ M ′ (ρ) holds. Integrating from ρ = 0 yields M (ρ) ≤ M (ρ) = 1 − H(α).
                              1                                            K       1

Step 4: Bounding       the Maximum (Case 2: n < K). If n < K, then        P nC < R . The Parseval
                                                                                 2     2

constraint      wi ≤ R is inactive. We maximize the convex function
                       2                                                    ψµ (wi ) subject to the box
             P
constraints 0 ≤ wi ≤ C 2 . Therefore the maximum is attained at an extreme point. In addition,
ψµ (C 2 ) = gµ (C) ≥ 0 (as it represents mutual information). Also, ψµ (0) = 0, and so ψµ (C 2 ) ≥ ψµ (0).
Therefore, the maximum is attained when wi = C 2 for all i ∈ [n].
    The objective value is:
                        n
                        X
                              ψµ (wi ) = nψµ (C 2 ) = ngµ (C) < Kgµ (C) = MK (ρ),
                        i=1

Since gµ (C) ≥ 0 (as it represents mutual information) and n < K. From Step 3, we established
MK (ρ) ≤ 1 − H(α).
   In both cases, the total mutual information is bounded by 1 − H(α).

Proof of Lemma 8.3 We first prove that xi (b̃) = xi (b) for i ̸= j.
    Recall the definition of the Fourier coefficient zi (b) = E[b(X n )Xi ]. Since i =
                                                                                     ̸ j, Xi is independent
of Xj . Let X∼j denote the bits of X n excluding index j. We write
                                                                             
                                              Xi
                              zi (b) = EX∼j       (b(X∼j , −1) + b(X∼j , 1))
                                              2

    Now consider the compressed function b̃. By definition, compression locally rearranges the pair
(b(x∼j , −1), b(x∼j , 1)) into (b̃(x∼j , −1), b̃(x∼j , 1)) such that the sum is preserved :
                              b(x∼j , −1) + b(x∼j , 1) = b̃(x∼j , −1) + b̃(x∼j , 1)
   Substituting this back into the expectation:
                                                                         
                                           Xi 
                           zi (b) = EX∼j        b̃(X∼j , −1) + b̃(X∼j , 1)
                                           2
                                    = E[b̃(X n )Xi ] = zi (b̃)

                                                      103
Thus, zi (b̃) = zi (b) for i ̸= j.
   We next show that |zj (b̃)| ≥ |zj (b)|. Expand the Fourier coefficient for index j by conditioning
on X∼j :
                                           1
                                   zj (b) = EX∼j [b(X∼j , 1) − b(X∼j , −1)]
                                           2
By definition, compression locally rearranges the pair (b(x∼j , −1), b(x∼j , 1)) into (b̃(x∼j , −1), b̃(x∼j , 1)).
Therefore, |b(x∼j , 1) − b(x∼j , −1)| = b̃(x∼j , 1) − b̃(x∼j , −1) for any value of x∼j . Hence,

                                    1
                           |zj (b)| = EX∼j [b(X∼j , 1) − b(X∼j , −1)]
                                    2
                                    1
                                   ≤ EX∼j [|b(X∼j , 1) − b(X∼j , −1)|]
                                    2
                                    1     h                           i
                                   = EX∼j |b̃(X∼j , 1) − b̃(X∼j , −1)|
                                    2
                                    1     h                         i
                                   = EX∼j b̃(X∼j , 1) − b̃(X∼j , −1) = zj (b̃) ,
                                    2
where in the first step we used the convexity of absolute value (|E[Y ]| ≤ E[|Y |]). In the third equality,
we used the assumption that b̃ is non-decreasing in the j-th bit. Note that this also implies that
zj (b̃) ≥ 0, which completes the proof.

Proof of Lemma 8.4 We can expand the expectation by conditioning on the value of the random
variable Xi . Since X is uniform, Xi takes values −1 and +1 with probability 1/2 each.
                                      1                        1
              zi (b) = E[b(X n )Xi ] = E[b(X n )Xi | Xi = −1] + E[b(X n )Xi | Xi = 1]                       (36)
                                      2                        2
Substitute the value of Xi into the expression:
                                   1                           1
                           zi (b) = E[b(X∼i , −1) · (−1)] + E[b(X∼i , 1) · (1)]
                                   2                           2                                            (37)
                                   1
                                  = Ex∼i [b(x∼i , 1) − b(x∼i , −1)]
                                   2
    We are given that b is non-decreasing bit-wise. Therefore, for every possible setting of the other
bits x∼i , we have b(x∼i , 1) ≥ b(x∼i , −1). Thus, zi (b) ≥ 0.

Proof of Lemma 8.5 Let E+ = E[b(X) | Xi = +1] and E− = E[b(X n ) | Xi = −1] respectively
denote the average value of the function when the i-th bit is fixed to +1 and −1. Since b outputs
values in {−1, 1}, we have −1 ≤ E+ , E− ≤ 1. In addition, we have
                             1    1
                          µ = E+ + E−
                             2    2
                                           1        1            E+ − E−
                          zi = E[b(X)Xi ] = E+ · 1 + E− · (−1) =
                                           2        2               2
Hence µ + zi = E+ and µ − zi = E− and the claim follows from the fact that E+ ≤ 1 and E− ≥ −1.




                                                      104
Proof of Theorem 8.2
Preliminaries and Notation We analyze functions on the Boolean hypercube {−1, 1}n . We
follow the setup used in [84]. Let f : {−1, 1}n → R be a bounded, non-negative function, normalized
such that E[f ] = 1. We assume ∥f ∥∞ ≤ M . (When analyzing a Boolean function b, we typically
look at the indicator function of the event b(x) = 1).
    Let α ∈ [0, 1/2] be the noise parameter. The noise operator Tα acts on f as (Tα f )(x) = Ey [f (y)],
where y is obtained from x by flipping coordinates with probability α. Let ρ = 1 − 2α. In the Fourier
domain, Tα acts as a multiplier:
                                                      |S| ˆ
                                         Tdα f (S) = ρ f (S).

We define the noise parameter λ = ρ2 = (1 − 2α)2 . We consider the high noise regime, where λ is
small.
   We decompose f into its even part f0 and odd part f 1:
                                     f (x) + f (−x)                f (x) − f (−x)
                          f0 (x) =                  ,   f1 (x) =                  .
                                            2                             2
Note that E[f0 ] = 1.
   We define the noisy versions:
                                         F = Tα f0 ,    Z = Tα f1 .
Note that Tα f = F + Z. We define Y = F − 1. Since E[F ] = 1, we have E[Y ] = 0.
   The Fourier coefficients satisfy F̂ (S) = λ|S|/2 fˆ0 (S) and Ẑ(S) = λ|S|/2 fˆ1 (S). F (and Y ) are
supported on even Fourier levels, while Z is supported on odd levels.
   The level 1 Fourier weight is L1 (f ) = L1 (f1 ).
   We utilize the entropy decomposition established in [84] (Lemma 6.2):
Lemma 8.6 (Entropy Decomposition).
                                                         2     4 
                                                  1      Z        Z
                        Ent(Tα f ) ≤ Ent(F ) +        E      +O E       .
                                               2 ln 2    F        F3

   It is known that Ent(F ) = O(λ2 ) (Lemma 5.4 in [84]).
   We also rely on a crucial dominance property.
Lemma 8.7 (Dominance). F ≥ 0 and |Z| ≤ F .
Proof. Note that by definition of the even and odd parts of f , we have

                                         f0 (x) + f1 (x) = 2f (x)
                                         f0 (x) − f1 (x) = 2f (−x)

Since f ≥ 0, we have |f1 (x)| ≤ f0 (x). The noise operator Tα is a positive operator, preserving
non-negativity and dominance. Thus |Z| = |Tα f1 | ≤ Tα |f1 | ≤ Tα f0 = F .

Hypercontractivity and Moment Bounds We rely on the Bonami-Beckner Hypercontractivity
Theorem. A standard application is for homogeneous polynomials.
Corollary 8.8 (Hypercontractivity for Homogeneous Polynomials). Let hk be a homogeneous
polynomial of degree k. For q ≥ 2,

                                   ∥hk ∥q ≤ ( q − 1)k ∥hk ∥2 .
                                             p


                                                    105
   We must be careful when applying this to functions supported on multiple levels. We use the
Minkowski inequality combined with Corollary 8.8 to establish rigorous moment bounds.
Lemma 8.9 (Moment Bounds). Assuming f is bounded by M , the following bounds hold as λ → 0:
  1. E[Y 2 ] = O(λ2 ).
  2. E[|Y |3 ] = O(λ3 ).
  3. E[Z 2 ] = λL1 (f ) + O(λ3 ).
  4. E[Z 4 ] = O(λ2 ).
  5. E[Z 2 Y ] = O(λ2 ).
Proof. We assume λ is small enough (e.g., 3λ < 1). Since f is bounded, its L2 norm is also bounded
(∥f ∥2 ≤ M ).
Part 1: E[Y 2 ] = O(λ2 ). Y is supported on even levels ≥ 2.
                                      X       X
                           E[Y 2 ] =       λk      fˆ0 (S)2
                                       k≥2,even        |S|=k
                                            X
                                     ≤ λ2          fˆ0 (S)2 = λ2 Var(f0 ) = O(λ2 ).
                                            S̸=∅


Part 2: E[|Y |3 ] = O(λ3 ). We analyze Y = Y2 + Y≥4 using the L3 norm.
   1. Bounding ∥Y2 ∥3 . Use q = 3, k = 2. The constant is 2.

                                                    ∥Y2 ∥3 ≤ 2∥Y2 ∥2 .

     ∥Y2 ∥22 = O(λ2 ). Thus, ∥Y2 ∥3 = O(λ).
   2. Bounding ∥Y≥4 ∥3 .
                               X                               X                 √
                   ∥Y≥4 ∥3 ≤        k ≥ 4, even∥Yk ∥3 ≤            k ≥ 4, evenM ( 2λ)k = O(λ2 ).

   3. Combining the bounds. ∥Y ∥3 = O(λ). Therefore, E[|Y |3 ] = O(λ3 ).

Part 3: E[Z 2 ] = λL1 (f ) + O(λ3 ). Z is supported on odd levels ≥ 1.
                                                    X      X
                              E[Z 2 ] = λL1 (f1 ) +     λk      fˆ1 (S)2
                                                         k≥3,odd     |S|=k
                                                               3
                                       = λL1 (f ) + O(λ ).


Part 4: E[Z 4 ] = O(λ2 ). We decompose Z = Z1 + Z≥3 . We use the Minkowski inequality for the L4
norm: ∥Z∥4 ≤ ∥Z1 ∥4 + ∥Z≥ 3∥4 .
   1. Bounding ∥Z1 ∥4 . Z1 is degree 1. Use Corollary 8.8 (q = 4, k = 1).
                                                    √
                                           ∥Z1 ∥4 ≤ 3∥Z1 ∥2 .

     ∥Z1 ∥22 = O(λ). Thus, ∥Z1 ∥4 = O(λ1/2 ).

                                                        106
  2. Bounding ∥Z≥3 ∥4 . Use Minkowski inequality on Z≥3 = k≥3,odd Zk .
                                                          P
                                            X
                                  ∥Z≥3 ∥4 ≤     k ≥ 3, odd∥Zk ∥4 .
     Applying hypercontractivity to each Zk :
                                                       √
                                             ∥Zk ∥4 ≤ ( 3)k ∥Zk ∥2 .
     Since ∥fˆk ∥2 ≤ M , ∥Zk ∥2 ≤ M λk/2 .
                                                           √
                                               ∥Zk ∥4 ≤ M ( 3λ)k .
     We sum this geometric series:
                                                               √
                                      X                √      ( 3λ)3
                       ∥Z≥3 ∥4 ≤ M        k ≥ 3, odd( 3λ) = M
                                                            k
                                                                     = O(λ3/2 ).
                                                              1 − 3λ
  3. Combining the bounds.
                                   ∥Z∥4 ≤ O(λ1/2 ) + O(λ3/2 ) = O(λ1/2 ).
     Therefore, E[Z 4 ] = ∥Z∥44 = O(λ2 ).

Part 5: E[Z 2 Y ] = O(λ2 ). We use the Cauchy-Schwarz inequality:
                                                 p
                                    |E[Z 2 Y ]| ≤ E[Z 4 ]E[Y 2 ].
Using Part 4 and Part 1:                       p
                               |E[Z 2 Y ]| ≤    O(λ2 ) · O(λ2 ) = O(λ2 ).



Higher Order Term We now bound the higher order term in the entropy decomposition (Lemma
8.6).
Lemma 8.10 (Higher Order Term). E[Z 4 /F 3 ] = O(λ2 ).
Proof. We use a constant threshold ∆ = 1/2 to split the expectation.
                           4       4                 4          
                           Z         Z                    Z
                        E       =E      IF ≤ 1/2 + E         IF > 1/2 .
                           F3        F3                   F3
   Term 2 (F is large): When F > 1/2, 1/F 3 < 8.
                                  4         
                                  Z
                               E      I        ≤ 8E[Z 4 ].
                                  F 3 F >1/2
By Lemma 8.9(4), E[Z 4 ] = O(λ2 ). So Term 2 is O(λ2 ).
   Term 1 (F is small): By Lemma 8.7, |Z| ≤ F . So Z 4 /F 3 ≤ F .
                                   4          
                                   Z
                               E      IF ≤ 1/2 ≤ E[F IF ≤ 1/2].
                                   F3
Since F ≤ 1/2 on this indicator,
                                               1
                                E[F IF ≤1/2 ] ≤ P (F ≤ 1/2).
                                               2
P (F ≤ 1/2) = P (Y ≤ −1/2). By Chebyshev’s inequality and Lemma 8.9(1):
                                   P (|Y | ≥ 1/2) ≤ 4E[Y 2 ] = O(λ2 ).
So Term 1 is O(λ2 ).

                                                    107
Optimal Asymptotic Entropy Bound We now prove the main technical result of this section,
achieving the optimal O(λ2 ) error bound by employing a direct Taylor expansion.
Theorem 8.11 (Optimal Asymptotic Entropy Bound). For any bounded nonnegative non-zero
function f with E[f ] = 1:
                                                       
                                             1
                           Ent(Tα f ) ≤          L1 (f ) · λ + O(λ2 ).
                                          2 ln 2
    The proof, detailed below, relies on a direct Taylor expansion approach combined with rigorous
moment bounds derived using hypercontractivity. Crucially, we employ a careful application of
the Minkowski inequality over the Fourier decomposition to establish the necessary higher-moment
bounds. The optimality of this bound is demonstrated by the fact that the O(λ2 ) error rate is tight
for Boolean dictatorship functions.

Proof. We start from the entropy decomposition (Lemma 8.6):
                                                       2     4 
                                                1      Z        Z
                      Ent(Tα f ) ≤ Ent(F ) +        E      +O E       .
                                             2 ln 2    F        F3

We know Ent(F ) = O(λ2 ) and by Lemma 8.10, the error term is O(λ2 ). We analyze B = E[Z 2 /F ].
   We use the Taylor expansion of 1/F = 1/(1 + Y ) around Y = 0 with the exact remainder:

                                        1          Y2
                                           =1−Y +     .
                                       1+Y        1+Y
This holds when F = 1 + Y > 0. Let S+ = {x : F (x) > 0}.
                              2
                                                         Y2
                                                             
                               Z               2
                       B=E       IS+ = E Z 1 − Y +            IS+ .
                               F                         F
   Term 1 (Expansion): ET = E[Z 2 (1 − Y )IS+]. By Lemma 8.7, if F (x) = 0, then Z(x) = 0.
The indicator is redundant.
                              ET = E[Z 2 ] − E[Z 2 Y ].
By Lemma 8.9(3) and (5):

                  ET = (λL1 (f ) + O(λ3 )) − O(λ2 ) = λL1 (f ) + O(λ2 ).
                                h 2 2      i
   Term 2 (Remainder): RT = E Z FY IS+ . Using dominance |Z| ≤ F , Z 2 /F ≤ F .

                                     RT ≤ E[F Y 2 IS+] ≤ E[F Y 2 ].

                            E[F Y 2 ] = E[(1 + Y )Y 2 ] = E[Y 2 ] + E[Y 3 ].
By Lemma 8.9(1) and (2), RT = O(λ2 ) + O(λ3 ) = O(λ2 ).
   Combining the terms for B:
                                   B = λL1 (f ) + O(λ2 ).
   Substituting this back into the entropy decomposition:
                                                  1
                       Ent(Tα f ) ≤ O(λ2 ) +          (λL1 (f ) + O(λ2 )) + O(λ2 )
                                               2 ln 2
                                     L1 (f )
                                 =           λ + O(λ2 ).
                                     2 ln 2

                                                  108
We next show that the O(λ2 ) error term is asymptotically tight. We demonstrate this by analyzing
the dictatorship functions which are believed to maximize the entropy (and mutual information).
    Consider the Boolean dictatorship function f (x) = x1 . The mutual information is exactly the
channel capacity, I(f (X); Y ) = 1 − H(α), where H(α) is the binary entropy function (in bits). We
analyze the Taylor expansion of the capacity around α = 1/2 (where ρ = 0).
    Recall ρ = 1 − 2α and λ = ρ2 . The expansion of the binary entropy function H(α) around
α = 1/2 yields
                                             1 2       1
                              H(α) = 1 −         ρ −         ρ4 + O(ρ6 ).
                                          2 ln 2     12 ln 2
Therefore, the capacity is:
                                             1        1
                             1 − H(α) =          λ+         λ2 + O(λ3 ).
                                          2 ln 2    12 ln 2
For the dictatorship function, L1 (f ) = 1. Thus, the expansion matches the form in the theorem
statement:                                             
                                                L1 (f )
                               I(f (X); Y ) =             λ + Θ(λ2 ).
                                                2 ln 2
Since the expansion for the maximizing function includes a Θ(λ2 ) term, the general upper bound
established in the theorem statement cannot be asymptotically improved beyond O(λ2 ).

Implications and Applications The optimal error bound established in the previous section has
significant consequences for the structural properties of highly informative functions and the range
of validity of the Courtade-Kumar conjecture.

Linear Fourier Concentration The O(λ2 ) error bound allows us to derive the strongest possible
Fourier concentration result within this asymptotic framework.
Theorem 8.12 (Linear Fourier Concentration). Let f be a Boolean function satisfying c ≤ Ef ≤ 1/2
(for some absolute constant c > 0). If I(f (X); Y ) ≥ 1 − H(α), then
                                         X
                                             fˆ(S)2 = O(λ).
                                        |S|≥2

Proof. Let p = Ef . We utilize the connection: I(f (X); Y ) = Ent(Tα f ) + Ent(Tα (1 − f )).
    We apply Theorem 8.11 by normalizing f . Using Ent(h) = E[h]·Ent(h/E[h]), we have Ent(Tα f ) =
p · Ent(Tα (f /p)). Applying the theorem to f /p:
                                                                    
                                                 L1 (f /p)         2
                                Ent(Tα f ) ≤ p             λ + O(λ )
                                                   2 ln 2
                                               L1 (f )
                                           =           λ + O(λ2 ).
                                             p(2 ln 2)

The O(λ2 ) constant remains controlled because p is bounded away from 0 by c. Applying the same
logic to 1 − f , and noting L1 (f ) = L1 (1 − f ):
                                                        
                                               1     1       L1 (f )
                            I(f (X); Y ) ≤       +                   λ + O(λ2 )
                                               p 1 − p 2 ln 2
                                                 1    L1 (f )
                                          =                   λ + O(λ2 ).
                                             p(1 − p) 2 ln 2

                                                109
   We use the Taylor expansion of the channel capacity: 1 − H(α) = 2 ln
                                                                     λ
                                                                        2 − O(λ ). Combining this
                                                                               2

with the assumption I(f (X); Y ) ≥ 1 − H(α):

                                     λ                   1    L1 (f )
                                          + O(λ2 ) ≤                  λ + O(λ2 ).
                                   2 ln 2            p(1 − p) 2 ln 2

      Dividing by λ/(2 ln 2):
                                                            L1 (f )
                                              1 + O(λ) ≤            + O(λ).
                                                           p(1 − p)
Rearranging:
                                                p(1 − p) − O(λ) ≤ L1 (f ).
   By Parseval’s identity,                ˆ 2
                                     S̸=∅ f (S) = p(1 − p). Therefore, the Fourier weight on levels 2 and
                                  P
higher is:                            X
                                              fˆ(S)2 = p(1 − p) − L1 (f ) ≤ O(λ).
                                      |S|≥2



      This linear concentration is a significant improvement over the O(λ1/3 ) bound established in [84].

Extended Range for the Conjecture The improved Fourier concentration directly translates
to proving the Courtade-Kumar conjecture for a wider range of the noise parameter λ.
    We are now ready to prove Theorem 8.2. We recall the theorem below.
Theorem 8.13 (Main Result - Extended Range). There exists an absolute constant δopt > 0 such
that if the noise parameter λ ≤ δopt , the Courtade-Kumar conjecture holds. Furthermore, δopt is
strictly larger than the threshold established using the O(λ4/3 ) error bound in [84].
Proof. The proof strategy follows the established path in [84], relying on the combination of Fourier
concentration and structural theorems for Boolean functions.
    Theorem 8.12P implies that a highly informative function f has most of its Fourier mass on level
                        ˆ
1. Define ξ := |S|≥2 f (S)2 . Theorem 5.5 in [84] at high level states that such a function must be
close to a dictatorship. Concretely, by this theorem we have

                                                                                                 (38)
                                                  p
                                     |E[f ]| = O(ξ ln(1/ξ)),
                                  fˆ({k})2 ≥ 1 − ξ − O(ξ 2 ln(1/ξ))                              (39)

for some k ∈ [n].6 The next step involves analyzing the mutual information of near-dictatorship
functions (Theorem 1.14 in [84]), by which Conjecture 29 holds provided that

                                                                                           (40)
                                          p
                                         ξ ln(1/ξ) ≤ c0 ,

for a small absolute constant c0 .
    There is also another constraint that needs to be satisfied and is implicit in the proof of Theorem
1.14 [84], which we discuss next. Define α, β ≥ 0 as follows: β = −(1/2)fˆ(∅) = −(1/2)E[f ] and
fˆ({k}) = (1 − α)(1 − 2β). Also set γ := α + β. Then, another condition used in Proof of [84,
Theorem 1.14 (page 30)] is that

                                                   λ + γ ln(1/γ) ≤ c1                                        (41)
  6
      Note that in our notation f takes its values in {−1, 1} which corresponds to the g notation in [84].


                                                           110
for some small absolute constant c1 > 0. Invoking (38) and (39), γ = O(ξ ln(1/ξ)). In Theorem 8.12,
                                                                        p

we proved that ξ = O(λ) and so γ = O(λ ln(1/λ)). Since ln(1/γ) = O(ln(1/λ)), we have:
                                           p


                                    γ ln(1/γ) = O(λ(ln(1/λ))3/2 ).

   Hence, condition (41) becomes

                                        λ + λ(ln(1/λ))3/2 ≤ c′1                                      (42)

for some absolute constant c′1 > 0. Furthermore, using that ξ = O(λ), condition (40) is equivalent to

                                                                                                 (43)
                                           p
                                          λ ln(1/λ) ≤ c0 .

Condition (42) already implies Condition (43). In summary, Condition (42) defines the threshold
δopt .
     In contrast, the analysis in [84], based on the O(λ4/3 p) error bound, yielded a Fourier concen-
tration of O(λ ). This led to the bound γ = O(λ
                1/3                                     1/3   ln(1/λ)) and a condition dominated by
O(λ1/3 (ln(1/λ))3/2 ).
     Since 1 > 1/3, the function x(ln(1/x))3/2 approaches zero significantly faster than x1/3 (ln(1/x))3/2
as x → 0. Therefore, the threshold δopt satisfying the new, tighter inequality is strictly larger than
the threshold derived from the O(λ4/3 ) analysis.

8.1.2   Part II: The Unsymmetrized Conjecture and the Li-Médard’s Conjecture
Problem Context Beyond the main conjecture, Li and Médard [70] proposed related conjectures
on the Lα -norm of the noise-stability operator Tp f (x) = P (f (Y ) =P1 | X = x). They conjectured
that for balanced functions, the “unsymmetrized” norm Nα (f ) = (Tp f (x))α is maximized by a
dictatorship. This “Unsymmetrized Conjecture” implies the Courtade-Kumar conjecture.

AI Contribution We provided the AI system with the research paper [10] as primary input, and
prompted it to prove the Unsymmetrized Conjecture (Conjecture 1) or the Li-Médard Conjecture
(Conjecture 3) therein.
   • Analyzing
             P Relaxations: The AI analyzed a relaxation of the problem to maximizing
     J (q) = qx log qx under moment constraints. It identified that the dictatorship is a saddle
     point (not a global max) for this specific relaxation, revealing why standard approaches fail.

   • Structural Insights: It proved that any maximizer of the relaxed problem must be a
     distribution supported on at most two points (Lemma 8.15).

   • Local Optimality: It proved that the dictatorship function is a local maximum for the
     optimization problem over the Boolean Hull (Lemma 8.18).

   • Monotonicity: It established that the maximizer must be a monotone function (Lemma
     8.17).

Technical Details: Unsymmetrized Courtade-Kumar Conjecture and the Li-Médard
Conjecture We begin by recalling the Courtade-Kumar conjecture [25]. Let X be a random
variable uniformly distributed over the n-dimensional Hamming cube {0, 1}n . We define Y as a
noisy observation of X obtained by passing each coordinate of X through a memoryless Binary
Symmetric Channel (BSC) with crossover probability p ∈ (0, 1/2).

                                                  111
    Courtade and Kumar conjectured that for any Boolean function f : {0, 1}n → {0, 1}, the mutual
information between the function output f (Y ) and the original input X is bounded by:

                                            I(f (Y ); X) ≤ 1 − h(p)

where h(p) = −p log2 p − (1 − p) log2 (1 − p) denotes the binary entropy function.
   The conjecture posits that this maximum mutual information is achieved when f is a dictatorship
function—that is, a function that depends solely on a single input coordinate, such as f (Y ) = Yi for
any i ∈ {1, . . . , n}.

Related Conjectures on Functionals of f . Beyond the primary Courtade-Kumar conjecture,
several related conjectures have been proposed in [70, 1]. These works generally posit that dictatorship
functions are the maximizers for various functionals of Boolean functions. Of particular relevance is
the work of Li and Médard [70], which focuses on balanced Boolean functions (where E[f ] = 1/2).
    They investigate the Lα -norm of the noise-stability operator, defined as:

                                     Tp f (x) = P (f (Y ) = 1 | X = x)                                         (44)

   Li and Médard conjecture that among all balanced functions f , the quantity Nα (f ) is maximized
by a dictatorship function f0 for 1 ≤ α ≤ 2. Specifically, they consider the unsymmetrized and
symmetrized versions of these norms:

   • Unsymmetrized Norm: Nα (f ) = x∈{0,1}n (Tp f (x))α
                                         P

   • Symmetrized Norm: Nαsym (f ) = x∈{0,1}n [(Tp f (x))α + (1 − Tp f (x))α ]
                                        P


The Entropy Connection. For a balanced function f , the mutual information I(f (Y ); X) can be
expressed in terms of the noise operator. Since H(f (Y )) = 1 for balanced functions, we have:

         I(f (Y ); X) = 1 − H(f (Y ) | X)
                             1 X
                      =1− n             h(Tp f (x))
                            2         n
                                 x∈{0,1}
                             1     X
                     =1+                    [Tp f (x) log2 Tp f (x) + (1 − Tp f (x)) log2 (1 − Tp f (x))]      (45)
                            2n
                                 x∈{0,1}n

This decomposition motivates
                           P an “unsymmetrized” version of the Courtade-Kumar conjecture, which
focuses solely on the term   Tp f (x) log2 Tp f (x).
Comparison of Conjectures. Let f be a balanced Boolean function and f0 be a dictatorship
function. The various conjectures are summarized in Table 3.

             Table 3: Summary of related conjectures for balanced Boolean functions.

      Conjecture      Name                             Formal Statement
      Conjecture 1    Unsymmetrized C-K
                                                       P                          P
                                                          Tp f (x) log Tp f (x) ≤    Tp f0 (x) log Tp f0 (x)
      Conjecture 2    Courtade-Kumar                   I(f (Y ); X) ≤ 1 − h(p)
      Conjecture 3    Li-Médard (Lα )                  Nα (f ) ≤ Nα (f0 ) for 1 ≤ α ≤ 2
      Conjecture 4    Symmetrized Li-Médard            Nαsym (f ) ≤ Nαsym (f0 ) for 1 ≤ α ≤ 2




                                                       112
   Prior work in [10] has established the following logical relationships between these conjectures:

                                  Conjecture 1      ⇐⇒      Conjecture 3
                                       ⇓                         ⇓                                           (46)
                                  Conjecture 2      ⇐⇒      Conjecture 4

Specifically, if the Lα -norm conjectures hold, the corresponding Courtade-Kumar conjectures (sym-
metrized and unsymmetrized) follow for all balanced functions.
   We prompted the Gemini AI system to prove either Conjecture 1 or Conjecture 3.


     Can you prove Conjecture 1 or Conjecture 3 (in the provided paper)?


          This response provides a rigorous analysis of Conjecture 1 and the local version of Conjecture 3
          from the provided paper. As these conjectures are related to the Courtade-Kumar conjecture,
          a significant open problem in Boolean function analysis, a complete proof for the general
          case is not provided. Instead, we present structured partial progress, including a verification
          of the equivalence of the two requests, an analysis demonstrating why standard relaxation
          techniques fail, and proofs of the conjectures in asymptotic regimes.



              Figure 18: Model identification of open problem and progress direction


   The system specifically analyzed a relaxed version of the optimization problem given by:
                                                    X
                               Maximize J (q) :=           qx log qx                                         (47)
                                                         x∈{0,1}n


subject to the constraints    qx = N1 (f0 ) and    qx ≤ N2 (f0 ). The model’s analysis identified that
                           P                    P 2
the dictatorship distribution constitutes a saddle point for this relaxed problem. Consequently,
this suggested that the current relaxation is insufficient to prove the primary conjecture, as the
dictatorship function does not emerge as a definitive global maximizer under these constraints.
Following an iterative review of the system’s detailed technical reports, we derived the following
result (which we later noted is consistent with findings in [10, 20, 70]):

Lemma 8.14. For any balanced Boolean function f , N2 (f ) ≤ N2 (f0 ) and N2sym (f ) ≤ N2sym (f0 ),
where equality holds if and only if f is a dictatorship function.

   Leveraging this result, we provided the system with a specific strategy to pursue further refine-
ments of the proof.




                                                     113
     Note that the relaxed problem is maximizing a convex function over a set. So the optimal
     solution should be achieved at the boundary. Given Lemma 8.14, can you argue that an
     extreme point should be a dictatorship function?


         This is an exceptionally insightful and elegant approach to proving Conjecture 1. The
         strategy of relaxing the optimization problem from the discrete space of realizable vectors
         (from Boolean functions) to a continuous convex space defined by the L1 and L2 constraints
         is very powerful. Your analysis of the optimization landscape—maximizing a strictly convex
         function over a compact convex set—is correct. This indeed implies that the maximum must
         occur at an extreme point, meaning the L2 inequality constraint must be active (satisfied
         with equality). However, there is a subtle but crucial gap in the final step of the logic. Your
         argument finds the optimizer q ∗ over the relaxed set K. While we know q ∗ satisfies the
         equality constraint, we have not yet established that q ∗ is actually realizable by balanced
         Boolean functions.


              Figure 19: Model identification of open problem and progress direction


   It revealed a subtle logical gap in the initial argument. To address this, the system investigated
the relaxed optimization problems, demonstrating that the optimal solution is characterized by a
two-point distribution. By leveraging this structural property, the system provided an analytical
upper bound for the maximum objective value achievable by any balanced Boolean function.

Lemma 8.15. Consider maximizing J (q) given by (47) over the set K1 = {q : E[q] = 1/2, Var(q) ≤
ρ2 /4}. Then the maximizingdistribution
                                        is supported on two points {0, (1 + ρ2 )/2}, achieving the
                             1+ρ 2
objective value: V = 2n−1 ln   2     .

    Note that the ρ2 /4 bound on the variance comes from Lemma 8.14 as N2 (f0 ) = (1 + ρ2 )/4. We
also asked the AI system to plot the upper bound established by Lemma 8.15 along with the value
achieved by the dictatorship functions (see Figure 20.)




                                                   114
Figure 20: Comparison of the objective functional values for the two-point distribution relaxation
(upper bound), given by Lemma 8.15, and the dictatorship function as the correlation parameter ρ
varies from 0 to 1.


    We next sought to tighten the relaxation by establishing an L∞ bound for the functions q
realizable by balanced Boolean functions. However, the system identified a technical flaw in our
proposed bound and provided a concrete counter-example, leading us to pivot our strategy.
    Our subsequent approach focused on leveraging the inverse of the noise operator. Given a corre-
lation parameter ρ, if q = Tρ f , the original function can be recovered via the inverse transformation
f = T1/ρ q. Recall that the noise operator is linear and can be expressed as:
                                                  X
                                      Tρ f (x) =        P (x, y)f (y)
                                              y∈{0,1}n

where the transition kernel is determined by the Hamming distance d(x, y). To refine the optimization
space, we relaxed the strict Boolean constraint f (x) ∈ {0, 1} to a pointwise box constraint, requiring
0 ≤ (T1/ρ q)x ≤ 1 for all x. Combining this with the established constraints on the first and second
moments of q, we defined the following relaxed constraint set K:
                                                        ρ2
                                                                              
                                         1
                      K := q : E[q] = , Var(q) ≤ , 0 ≤ (T1/ρ q)x ≤ 1
                                         2              4
    Interestingly it showed that the variance constraint is already implied by the other two. In
addition, it showed that this relaxation is indeed tight, as discussed next.
    Let FB be the P  set of balanced Boolean functions f : {0, 1}n → {0, 1} and define the entropy
functional Φ(f ) = x∈{0,1}n h((Tρ f )(x)) with h(t) = t ln t. Let G be the Boolean Hull (functions
g : {0, 1}n → [0, 1] with E[g] = 1/2). Let K = Tρ (G) be the feasible set for q, which can then be
characterized by the mean constraint E[q] = 1/2 and the pointwise box constraints 0 ≤ T1/ρ q ≤ 1.
Lemma 8.16. (Convex Relaxation and Tightness). Maximizing Φ(f ) over FB is equivalent to
maximizing J (q) over K.
   This equivalence is an important milestone as it transforms the initial optimization over discrete
Boolean functions into a continuous convex optimization.
   In addition, it proves two other structural properties of the solution.

                                                 115
     Consider the following relaxation of the problem [...]. What do you think about it? Can you
     use it to prove the unsymmetrized C-K conjecture?


          This is a challenging problem concerning the maximization of a convex functional related to
          entropy under the noise operator. Based on the instructions, we analyze the two proposed
          approaches. We provide rigorous proofs for several key properties of the optimizer, including
          monotonicity and the local optimality of the Dictatorship function. However, proving the
          global optimality requires advanced techniques that cannot be derived elementarily from the
          provided context. [....]



               Figure 21: Model identification of open problem and progress direction



Lemma 8.17. (Monotonicity). If f ∈ FB maximizes Φ(f ), then f can be assumed to be monotone.

Lemma 8.18. (Local optimality). A dictatorship function is a local maximum of the problem of
maximizing J (q) over K.

    The AI system also attempted to prove global optimality of the dictatorship functions by an
inductive proof and identifies the remaining gaps. Concretely, consider the restrictions of the function
f to the (n − 1)-dimensional sub-cubes. Let f0 , f1 : {0, 1}n−1 → {0, 1} be defined by f0 (x′ ) = f (x′ , 0)
and f1 (x′ ) = f (x′ , 1). Furthermore, let Tρ′ denote the noise operator acting on n − 1 variables, and
let gi = Tρ′ fi represent the noise-evolved versions of these sub-functions. The functional Φ(f ) admits
the following decomposition:
                                                 X
                                    Φ(f ) =             J(g0 (x′ ), g1 (x′ ))
                                           x′ ∈{0,1}n−1

where the kernel J(a, b) is defined as J(a, b) = h(pa + εb) + h(εa + pb), with h(t) = t ln(t), and the
parameters p and ε are given by p = 1+ρ             1−ρ
                                        2 and ε = 2 .
   The system then continues with the following response given the above notation.




                                                    116
          We have reduced the problem to maximizing Φ(f ) among balanced monotone Boolean
          functions and verified that Dictatorship is a local maximum. However, maximizing a convex
          function can lead to multiple local maxima. (For instance, for n = 2, the XOR function is
          also a local maximum, but yields a smaller value).
          To prove global optimality, we attempted an inductive approach using the decomposition:

                                           Φ(f ) = 2n−1 E[J(g0 , g1 )].

          We need to show E[J(g0 , g1 )] ≤ C(ρ) := h((1 + ρ)/2) + h((1 − ρ)/2).
          We proved the standard contraction inequality using the convexity of J and the doubly
          stochastic nature of Tρ′ :

                                E[J(g0 , g1 )] ≤ E[J(f0 , f1 )] = P (f0 ̸= f1 )C(ρ).

          Let P = P (f0 =  ̸ f1 ). Since C(ρ) < 0, we know P C(ρ) ≥ C(ρ). This inequality Φ(f ) ≤
          P 2n−1 C(ρ) is not strong enough to prove Φ(f ) ≤ 2n−1 C(ρ).
          This is a strong data processing inequality, equivalent to Mrs. Gerber’s Lemma. This is the
          central difficulty of the problem.




    We next conducted several further iterations of prompting to explore the inductive path. Specifi-
cally, we attempted to solidify the connection with Mrs. Gerber’s Lemma—which was also previously
used in [84] to prove C-K conjecture in the high-noise regime. However, while the system could
identify the relevance of the lemma, it ultimately failed to complete the formal analytical steps
required for the proof.
Observations on AI-Assisted Research. Our interactions with the system on these theoretical
problems yielded several key insights into its utility as a research partner:

   • Confirmation Bias in Prompting: The system exhibits a tendency to support the position
     or hypothesis presented in the prompt. When tasked with proving open-ended conjectures that
     are not necessarily true, it often attempts to bridge logical gaps with “hand-wavy” arguments
     that do not withstand rigorous scrutiny. We found that performance improves significantly
     when using neutral prompts (e.g., “prove or refute”), which encourages the system to evaluate
     multiple directions in parallel.
   • Effectiveness in Refutation: The system is remarkably adept at identifying counterexamples
     and pinpointing the “crux” of a problem. When provided with a precise but flawed idea, it can
     often explain exactly why a particular strategy fails, making it a valuable tool for early-stage
     proof debugging.

Proof of Lemma 8.15 To formally prove that the optimal distribution qx is supported on
at most two points, we analyze the Karush-Kuhn-Tucker (KKT) conditions. This structural
approachPreveals how the moment constraints necessitate aPsparse distribution. We seek to maximize
f (q) = x qx ln qx , which is equivalent to minimizing − x qx ln qx . Defining M = 2n as the size
of the Hamming cube, we construct the Lagrangian L with multipliers λ and µ for the mean and
variance constraints:
                                 M
                                                            !                   !
                                 X               X        M          X
                                                                          2
                  L(q, λ, µ) = −    qx ln qx + λ     qx −      +µ        qx − C
                                                  x
                                                          2            x
                                  x=1


                                                    117
                                               2
where the quadratic constraint C = M (1+ρ
                                       4
                                          )
                                            assumes the variance constraint Var(q) ≤ ρ2 /4 is active
at the maximum. Setting the partial derivative with respect to each qx to zero gives:
                                    ∂L
                                        = −(ln qx + 1) + λ + 2µqx = 0
                                    ∂qx

Rearranging this yields the transcendental equation ln qx − 2µqx = λ − 1. Let g(q) = ln q − 2µq. Any
optimal value of qx must lie at the intersection of g(q) and the constant λ − 1. Since g ′′ (q) = −1/q 2 ,
which is strictly negative for all q > 0, g(q) is strictly concave. A strictly concave function can
intersect a horizontal line at most at two distinct points, proving that the optimal qx can take at
most two values, a and b. Let k be the multiplicity of the value a, such that M − k indices take the
value b. The linear and quadratic constraints provide the following system:

                                        ka + (M − k)b = M/2,
                                                             M (1 + ρ2 )
                                      ka2 + (M − k)b2 =                  .
                                                                 4
Solving for a(k) and b(k) in terms of k, we find:
                                      r                                  r
                                1 ρ M −k                       1 ρ             k
                        a(k) = +                ,        b(k) = −                 .
                                2 2         k                  2 2           M −k
The objective function can then be expressed as F (k) = kϕ(a(k))+(M −k)ϕ(b(k)), where ϕ(t) = t ln t.
To determine the behavior of F (k), we examine its derivative F ′ (k) via implicit differentiation of the
constraints:
                                                               ϕ′ (a) + ϕ′ (b)
                            F ′ (k) = (ϕ(a) − ϕ(b)) − (a − b)
                                                                       2
                                                                               Ra
Assuming a > b, we utilize the integral representation ϕ(a) − ϕ(b) = b ϕ′ (t)dt to rewrite the
derivative:
                                                              ϕ′ (a) + ϕ′ (b)
                                       Z a
                                 ′
                             F (k) =       ϕ′ (t)dt − (a − b)
                                        b                            2
This expression represents the difference between the integral of ϕ′ (t) and the trapezoidal area under
the chord connecting (b, ϕ′ (b)) and (a, ϕ′ (a)). Calculating the derivatives of ϕ(t) = t ln t, we find
ϕ′ (t) = ln t + 1, ϕ′′ (t) = 1/t, and ϕ′′′ (t) = −1/t2 . Since ϕ′′′ (t) < 0 for all t > 0, the function ϕ′ (t) is
strictly concave. For a strictly concave function, the area under the curve is strictly greater than the
area of the trapezoid defined by the chord. Consequently, F ′ (k) > 0, meaning the objective function
F (k) is strictly increasing over its feasible domain. The maximum is therefore achieved at the largest
possible value of k. Given the non-negativity constraint b(k) ≥ 0, the maximum k occurs when b = 0.
                                                                                            1+ρ2
Solving for k in this boundary condition yields k = 1+ρ       M
                                                                2 , which results in a =         . Substituting
                                                                                      2 2                   
these values back into the objective yields the maximum value V = M               ln   1+ρ
                                                                                             =  2 n−1 ln 1+ρ2 .
                                                                               2         2                 2


Proof of Lemma 8.16 Since Tρ is linear, K is a convex polytope. Since J (q) is strictly convex,
its maximum over K is attained at an extreme point. The extreme points of K are the images of
the extreme points of G, which are FB (the set of balanced Boolean functions). Thus, maximizing
Φ(f ) over FB is equivalent to maximizing J (q) over K.




                                                      118
Proof of Lemma 8.17 We use decomposition along the n-th coordinate. Let f0 (x′ ) = f (x′ , 0)
and f1 (x′ ) = f (x′ , 1). Let Tρ′ be the noise operator on n − 1 variables. Let gi = Tρ′ fi . The functional
decomposes as:                                   X
                                      Φ(f ) =            J(g0 (x′ ), g1 (x′ )),
                                           x′ ∈{0,1}n−1

where J(a, b) = h(pa + εb) + h(εa + pb), with p = (1 + ρ)/2 and ε = (1 − ρ)/2. Let m = (a + b)/2
and d = (b − a)/2. Then J(a, b) = h(m − ρd) + h(m + ρd). Since h is strictly convex, J is strictly
increasing in |d| for fixed m.
    Consider the polarization f ∗ defined by f0∗ = min(f0 , f1 ) and f1∗ = max(f0 , f1 ). Note that f ∗ is
balanced since f0∗ +f1∗ = f0 +f1 . Let gi∗ = Tρ′ fi∗ . The means are preserved pointwise: m∗ (x′ ) = m(x′ ).
The differences are d(x′ ) = Tρ′ ((f1 − f0 )/2) and d∗ (x′ ) = Tρ′ (|f1 − f0 |/2).
    Since Tρ′ is a positive operator (its kernel is non-negative as it represents probabilities), we have
the inequality |Tρ′ (u)| ≤ Tρ′ (|u|). Thus, |d(x′ )| ≤ d∗ (x′ ). Since J increases with |d|, Φ(f ) ≤ Φ(f ∗ ).
By repeatedly applying this polarization, we conclude that the maximum must be attained by a
monotone function.

Proof of Lemma 8.18 We verify that the Dictatorship is a local maximum by checking the
KKT conditions for P maximizing J (q) over the polytope K. The set K is defined by the constraints
0 ≤ (M q)x ≤ 1 and      qx = N/2, where M = T1/ρ .
   We formulate the KKT conditions for maximization subject to g1 (q) := −M q ≤ 0 and g2 (q) :=
M q − 1 ≤ 0. The gradient condition is ∇J (q) = M (µ − λ), where λ, µ ≥ 0 are the multipliers for g1
and g2 respectively (ignoring the equality constraint which adds a constant shift ν1). Let γ = µ − λ
and g := M q. Complementary slackness implies:

   • If gx = 0, then µx = 0, which implies γx ≤ 0.

   • If gx = 1, then λx = 0, which implies γx ≥ 0.

    Let q ∗ be the noise operator applied to the dictatorship function fD (x) = x1 , i.e., q ∗ = Tρ (fD ).
Consequently, g ∗ = M q ∗ = T1/ρ (q ∗ ) = fD . Let A = {x | x1 = 1} and B = {x | x1 = 0}. We have
g ∗ = 1 on A and g ∗ = 0 on B. We therefore require γ ≥ 0 on A and γ ≤ 0 on B.
    The gradient condition is given by h′ (qy∗ ) = (M γ)y + ν. Let v = M γ. Since q ∗ takes values a on
B and b on A, v must be constant on A and B:

                                           v(x) = c0 + c1 χ1 (x),                                       (48)

where χ1 (x) = (−1)x1 . Calculating c1 , we obtain
                                 h′ (a) − h′ (b)  1
                          c1 =                   = ln(a/b) = − artanh(ρ) < 0,                           (49)
                                        2         2
where we used that a = 1−ρ                 1+ρ
                             2 and b = 2 , by definition of the noise operator. We also have
γ = Tρ v = c0 + ρc1 χ1 (x). The resulting constraints on γ are:
   • On A (χ1 = −1): c0 − ρc1 ≥ 0 =⇒ c0 ≥ ρc1 .

   • On B (χ1 = 1): c0 + ρc1 ≤ 0 =⇒ c0 ≤ −ρc1 .
    We require ρc1 ≤ c0 ≤ −ρc1 . Given that c1 < 0 and ρ > 0, we have ρc1 < 0 < −ρc1 . This
interval is non-empty (e.g., c0 = 0 is a valid solution). Thus, the Dictatorship satisfies the KKT
conditions and is a local maximum.

                                                    119
8.2    NP-hardness: Ratio Difference Maximization (RDM)
Written by Ravi Kumar and Silvio Lattanzi (on behalf of coauthors).

Problem Context
In a recent work [22], together with Flavio Chierichetti, Mirko Giacchini, Alessandro Panconesi,
Erasmo Tani, and Andrew Tomkins, we were studying Multinomial Logits (MNLs), also known
as Plackett–Luce models, that describe user preferences by assigning a weight to each item in a
universe. When a user is presented a subset of items, they select one with probability proportional
to its weight. In the paper, we consider the problem of learning an MNL by sampling from the
conditional distributions induced on subsets of the universe.
    Interestingly, even computing the worst-case error on arbitrary size subsets of the universe turns
out to be a non-trivial problem. In [22] we introduce several approximation algorithms for this tasks.
We also had the intuition that the problem was related to SUBSET-SUM and most likely NP-hard
but we felt that the reduction was not immediate and hence we decided to test Gemini with such a
question. We were happily surprised by receiving a zero-shot correct proof within a few minutes.
    We then asked also to prove NP-hardness for a variation of the problem.

AI Contribution
    Given only the formal definition of the Ratio Difference Maximization (RDM) problem, the AI
zero-shot generated a flawless, polynomial-time NP-hardness reduction from the SUBSET-SUM
problem. Upon a subsequent prompt, it successfully proved the NP-hardness of a related variation
(MAX-DIFF-RATIO) using a similarly rigorous reduction.
    More specifically, we used a math rigor prompt and we asked the model to show that the Ratio
Difference Maximization (RDM) problem is NP-hard. This is the prompt that we used:

   <Math Rigor Prompt>
   Prove that the following problem is NP-hard. Given two lists V = (v1 , ..., vn ) and W = (w1 , ..., wn )
   of positive integers, find subsets S ⊆ T ⊆ [n] that maximize the objective function

                                                      V (S)   W (S)
                                        f (S, T ) =         −       ,
                                                      V (T ) W (T )

   where V (X) =      i∈X vi and W (X) =
                    P                       P
                                               i∈X wi




   This is the output provided by Gemini that we verified to be correct:


  Theorem 8.19. The Ratio Difference Maximization (RDM) problem is NP-hard.
  Proof. We prove NP-hardness by a reduction from the SUBSET-SUM problem. The SUBSET-
  SUM problem is: Given a set A = {a1 , ..., an } ofP
                                                    positive integers and a target positive integer
  K, does there exist a subset I ⊆ [n] such that i∈I ai = K? We can assume K ≥ 2, as this
  restriction remains NP-complete.
  We define the decision version of RDM (D-RDM): Given (V, W ) and a rational number Z, does
  there exist S ⊆ T ⊆ [n] such that f (S, T ) ≥ Z?
  We now construct the reduction from an instance (A, K) of SUBSET-SUM (with K ≥ 2) to an
  instance of D-RDM.



                                                         120
Let L = K 2 . Since K ≥ 2, we have L > 1. We construct an RDM instance with n + 1 items:

   • For i = 1, ..., n, set vi = ai and wi = ai .

   • For i = n + 1, set vn+1 = 1 and wn+1 = L.

We set the target value for D-RDM to Z = K−1     K+1 . This construction is polynomial in the size of
the input (A, K).
We analyze the maximum value of the objective function f (S, T ) for this instance, where
S ⊆ T ⊆ [n + 1].
Case 1: n + 1 ∈  / T . Then T ⊆ [n]. For all i ∈ T , vi = wi = ai . Thus V (T ) = W (T ) and
V (S) = W (S). f (S, T ) = VV (T
                              (S)    W (S)    V (S)     V (S)
                                 ) − W (T ) = V (T ) − V (T    = 0.
                                                          P)
Case 2: n + 1 ∈ T . Let TA = T ∩ [n]. Let x = i∈TA ai . V (T ) = V (TA ) + vn+1 = x + 1.
W (T ) = W (TA ) + wn+1 = x + L.
We seek S ⊆ T that maximizes f (S, T ) = Vx+1        (S)
                                                         −W    (S)
                                                              x+L . This is equivalent to maximizing
G(S) = (x + L)V (S) − (x + 1)W (S).
We analyze the contribution of each element i ∈ T to G(S). For i ∈ TA , vi = wi = ai . The
contribution if i ∈ S is (x + L)ai − (x + 1)ai = ai (L − 1). Since ai > 0 and L > 1, this is positive.
Thus, the optimal S must include all i ∈ TA .
For i = n + 1, vn+1 = 1, wn+1 = L. The contribution if n + 1 ∈ S is (x + L)(1) − (x + 1)(L) =
x + L − xL − L = x(1 − L).
If x > 0 (i.e., TA =
                   ̸ ∅), since L > 1, the contribution x(1 − L) is negative. Thus, the optimal S
must exclude n + 1. In this case, the optimal S is S ∗ = TA .
If x = 0 (i.e., TA = ∅, T = {n + 1}), the contribution is 0. f (S, T ) = 0 whether S = ∅ or
S = {n + 1}.
We focus on the case x > 0. The maximum value for a fixed T (defined by x) is:

                                 x   x    x(x + L) − x(x + 1)      x(L − 1)
         h(x) = f (TA , T ) =      −    =                     =                .
                                x+1 x+L     (x + 1)(x + L)      (x + 1)(x + L)

We want to maximize h(x) over the set of achievable SUBSET-SUMs XA = {A(I) | I ⊆ [n], I ≠
∅}.
We analyze the function h(x) for x > 0. h(x) = (L − 1) x2 +(L+1)x+L
                                                             x
                                                                    . The derivative is:

                                         (x2 + (L + 1)x + L) − x(2x + L + 1)
                      h′ (x) = (L − 1)                                       .
                                                  ((x + 1)(x + L))2

The sign of h′ (x) is determined√by the numerator: N (x) = x2 + (L
                                                                 √ + 1)x + L − 2x2 − (L + 1)x
                                                                                            √=
L − x . h (x) = 0 when x = L. h(x) increases for 0√< x < L and decreases for x > L.
      2   ′

Thus, h(x) attains its unique global maximum at x = L.
Since L = K 2 , the unique maximum is attained at x = K. The maximum value is:

                             K(K 2 − 1)     K(K − 1)(K + 1)   K −1
                 h(K) =                 2
                                          =                 =      = Z.
                          (K + 1)(K + K )   (K + 1)K(K + 1)   K +1

Let OP T be the maximum value of the objective function for the constructed RDM instance.
Since K ≥ 2, Z > 0. Thus OP T = maxx∈XA h(x) (assuming A contains at least one element,
otherwise SUBSET-SUM is trivial).



                                                    121
 We now show the equivalence between the SUBSET-SUM instance and the D-RDM instance.
 (⇒) Suppose the SUBSET-SUM instance is a YES instance. Then there exists I ⊆ [n] such
 that A(I) = K. So K ∈ XA . Then OP T ≥ h(K) = Z. Since Z is the global maximum of h(x),
 OP T = Z. Thus the D-RDM instance is a YES instance.
 (⇐) Suppose the D-RDM instance is a YES instance. Then OP T ≥ Z. Since Z is the global
 maximum of h(x), this implies OP T = Z. Let x∗ ∈ XA be such that h(x∗ ) = Z. Since x = K is
 the unique global maximizer of h(x), it must be that x∗ = K. Therefore, K ∈ XA , which means
 the SUBSET-SUM instance is a YES instance.
 We have provided a polynomial-time reduction from SUBSET-SUM to D-RDM. Therefore,
 D-RDM is NP-hard, and consequently, the optimization problem RDM is NP-hard.

   Given the success of the first attempt, using the same prompt structure, we also asked to show
that a variation of the problem is NP-hard. This is the second proof that we obtained in this way.
   Consider the MAX-DIFF-RATIO (MDR) optimization problem: Given two lists V = (v1 , . . . , vn )
and W = (w1 , . . . , wn ) of positive integers, find j ∈ T ⊆ [n] that maximizes
                                                    vj            wj
                                    f (j, T ) = P            −P            .
                                                    i∈T vi        i∈T wi



  Theorem 8.20. The MDR problem is NP-hard.

 Proof. To prove NP-hardness, we consider the corresponding decision problem, D-MDR: Given
 (V, W ) and a rational threshold Q, does there exist a pair (j, T ) with j ∈ T ⊆ [n] such that
 f (j, T ) ≥ Q? We will show that D-MDR is NP-hard by a reduction from the SUBSET-SUM
 problem, which is known to be NP-complete.

  The Reduction. Given an instance (A, B) of SUBSET-SUM, we construct an instance of
  D-MDR with N = n + 1 items, indexed from 0 to n. We define the lists V = (v0 , . . . , vn ) and
  W = (w0 , . . . , wn ) and the threshold Q.
  The construction is defined as follows:

    1. For i = 1, . . . , n: vi = 4ai and wi = 4ai .

    2. For the special item i = 0: v0 = 8B and w0 = 2B.

    3. The threshold is Q = 1/3.

  Since ai and B are positive integers, all vi and wi are positive integers. This construction is
  clearly computable in polynomial time.

  Analysis of the Objective Function. Let V (T ) = i∈T vi and W (T ) = i∈T wi . We
                                                                 P                        P
  analyze the objective function f (j, T ) for the constructed instance.
  Case 1: j ∈ {1, . . . , n}. Let j = k ≥ 1. We have vk = wk .
  Case 1a: 0 ∈
             / T . Then T ⊆ {1, . . . , n}. For all i ∈ T , vi = wi , so V (T ) = W (T ).
                                          vk     wk       vk     vk
                           f (k, T ) =         −       =       −       = 0.
                                         V (T ) W (T )   V (T ) V (T )



                                                       122
Case 1b: 0 ∈ T . Let T = {0} ∪ S where S ⊆ {1, . . . , n} and k ∈ S. Let X =       i∈S 4ai . Then
                                                                                 P
V (S) = W (S) = X. V (T ) = v0 + X = 8B + X. W (T ) = w0 + X = 2B + X.
                                                 vk       wk
                                 f (k, T ) =          −        .
                                               8B + X   2B + X
Since vk = wk and B > 0, we have 8B + X > 2B + X. Thus, f (k, T ) < 0.
In Case 1, the maximum value of f (j, T ) is 0.
Case 2: j = 0. We P  must have 0 ∈ T . Let T = {0} ∪ S for some S ⊆ {1, . . . , n}. Let
X = V (S) = W (S) = i∈S 4ai .

                                      v0     w0        8B       2B
                       f (0, T ) =         −       =        −        .
                                     V (T ) W (T )   8B + X   2B + X

Let h(X) = 8B+X
            8B     2B
                − 2B+X . We analyze h(X) for X ≥ 0.

                         8B(2B + X) − 2B(8B + X)
                 h(X) =
                            (8B + X)(2B + X)
                         16B + 8BX − 16B 2 − 2BX
                            2                            6BX
                       =                         =                  .
                             (8B + X)(2B + X)      (8B + X)(2B + X)

We examine the derivative of h(X) with respect to X. The sign of h′ (X) is determined by the
sign of the numerator when using the quotient rule:

              N (X) = (6B)(8B + X)(2B + X) − (6BX)((8B + X) + (2B + X)).

Dividing by 6B (since B > 0), the sign is determined by:

                 N (X)
                       = (16B 2 + 10BX + X 2 ) − X(10B + 2X)
                  6B
                       = 16B 2 + 10BX + X 2 − 10BX − 2X 2 = 16B 2 − X 2 .

Thus, h′ (X) = 0 if and only if X 2 = 16B 2 . Since X ≥ 0 and B > 0, this occurs at X = 4B. The
function h(X) increases for X < 4B and decreases for X > 4B. The unique global maximum of
h(X) occurs at X = 4B.
The maximum value is:
                                  6B(4B)            24B 2    24B 2  1
                  h(4B) =                      =           =       = .
                            (8B + 4B)(2B + 4B)   (12B)(6B)   72B 2  3

Proof of Equivalence. We show that the SUBSET-SUM instance (A, B) is a Yes instance if
and only if the maximum value of f (j, T ) is at least Q = 1/3.
( =⇒ ) Suppose   the SUBSET-SUM instance is Yes.   P Then there exists a subset S ⊆ {1, . . . , n}
such that i∈S ai = B. This implies that X = i∈S 4ai = 4B is achievable. Let j = 0 and
          P
T = {0} ∪ S. Then f (0, T ) = h(4B) = 1/3. Thus, the D-MDR instance is Yes.
( ⇐= ) Suppose the D-MDR instance is Yes. The maximum value of f (j, T ) is ≥ 1/3. From
our analysis, if j ≥ 1, f (j, T ) ≤ 0. Therefore, the maximum must be achieved when j = 0.
The objective function is h(X), where X is an achievable SUBSET-SUM of {4ai }. Since the
maximum possible value of h(X) is 1/3, and this maximum is achieved uniquely at X = 4B,



                                                 123
the maximum value being ≥ 1/3 implies it must be exactly 1/3.       P This means X = 4B must
be  achievable. That  is, there exists S ⊆ {1, . . . , n} such that  i∈S 4ai = 4B, which implies
   i∈S ai = B. Thus, the SUBSET-SUM instance is Yes.
P
Since we have a polynomial-time reduction from the NP-complete problem SUBSET-SUM to
D-MDR, the latter is NP-hard. Consequently, the MDR optimization problem is NP-hard.




                                              124
8.3   Machine Learning Optimization: Self-regularized Gumbel Sigmoid
Written by Lin Chen, Gang Fu, and David P. Woodruff.

Problem Context
Subset selection is a core problem in machine learning, relevant to tasks like feature selection and
embedding dimension optimization. Current methods like Dropout Feature Ranking (DFR) rely on
explicit penalty terms (e.g., ℓ1 regularization) to control the number of selected features. However,
tuning the regularization strength λ is difficult and sensitive, often hindering practical application.
A new method, Self-regularized Gumbel Sigmoid (SrGS), was proposed to eliminate this
hyperparameter by using an implicit regularization mechanism involving Softmax competition and
budget-aware clipping. The theoretical question was to understand exactly why and how this
parameterization enforces sparsity without an explicit penalty.

AI Contribution
The researchers provided the model with the mathematical definition of SrGS and asked for a
theoretical analysis of its implicit regularization and behavior in the low-temperature limit.

   • Implicit ℓ0 Penalty: The model derived that in the low-temperature limit (T → 0), the
     variance of the Gumbel-Sigmoid distribution acts as an exact relaxation of the ℓ0 constraint,
     effectively penalizing non-binary solutions.

   • Adaptive Hybrid Regularization: It analyzed the deterministic limit (using expectations)
     and proved that the method induces a unique "hybrid" regularization: strong signals are
     subject to ℓ2 shrinkage (preserving magnitude), while weak signals competing for the remaining
     budget are suppressed by a non-convex ℓ2/3 penalty.

   • Theoretical Validation: These derivations provided the rigorous theoretical justification for
     the method’s empirical success, confirming it solves a relaxed subset selection problem without
     manual tuning.

Technical Details: Theoretical Analysis of SrGS
We employed the model to identify and resolve a key theoretical gap regarding the implicit mechanisms
of the Self-regularized Gumbel Sigmoid (SrGS) method.

Problem Formulation Subset selection is a core problem central to multiple optimization tasks
in machine learning. Existing methods, such as Dropout Feature Ranking (DFR) (Chang et al.,
2017), approach this by optimizing a variational dropout mask z on the input layer. However, DFR
relies on an explicit penalty term in the loss function to constrain the number of active features.
The objective function is formulated as:
                                      M                                M   D
                                1 X                                λ XX
                       L(θ) = −       log p(yi |f (xi ⊙ zi ; θ)) +           zij
                                M                                  M
                                  i=1                                i=1 j=1
                              |            {z                  }
                              Task Loss (e.g., Cross-Entropy or MSE)

where the first term represents the task-specific prediction error (negative log-likelihood), M is
the batch size, D is the number of features, and zij is the stochastic gate for the j-th feature.

                                                   125
Determining the optimal regularization strength λ requires extensive cross-validation and often
becomes a blocker for successful application due to its sensitivity.
   The SrGS method was proposed to overcome this limitation by eliminating the explicit penalty
term λ. Instead, it introduces a structural “self-regularization” mechanism defined by the following
process:

  1. Competition: For each feature j, a learnable logit tj is normalized via Softmax to produce
     an attention score Sj , enforcing global competition:

                                                  exp(tj )
                                           Sj = PD
                                                 k=1 exp(tk )


  2. Budgeting: The scores are scaled by the target budget K and clipped to form selection
     probabilities zj , ensuring the expected number of selected features approximates K:

                                          zj = Clip(Sj · K, ε, 1)

  3. Stochastic Selection: The final binary masks wj are generated via the differentiable Gumbel-
     Sigmoid reparameterization:
                                                                                
                                1
                      wj = σ      (log zj − log(1 − zj ) + log uj − log(1 − uj ))
                                T

    While SrGS empirically demonstrates superior solution quality without hyperparameter tuning,
the theoretical basis for this parameterization remains an open question. Specifically:

  1. Does this specific parameterization rigorously enforce sparsity in the low-temperature limit
     (T → 0)?

  2. What is the exact mathematical form of the implicit regularization induced by this mechanism
     when combined with standard weight decay?




                                                126
We identify and resolve a key theoretical gap regarding the implicit mechanisms of the
Self-regularized Gumbel Sigmoid (SrGS) method.

Question: Subset selection is a core problem central to multiple optimization tasks in
machine learning. Existing methods, such as Dropout Feature Ranking (DFR), approach
this by optimizing a variational dropout mask z on the input layer. However, DFR relies on
an explicit penalty term in the loss function to constrain the number of active features. The
objective function is formulated as:
                                M                                  M D
                             1 X                                λ XX
                  L(θ) = −         log p(yi |f (xi ⊙ zi ; θ)) +           zij             (50)
                             M i=1                              M i=1 j=1
                           |            {z                  }
                          Task Loss (e.g., Cross-Entropy or MSE)

where the first term represents the task-specific prediction error (negative log-likelihood),
M is the batch size, D is the number of features, and zij is the stochastic gate for the j-th
feature. Determining the optimal regularization strength λ requires extensive cross-validation
and often becomes a blocker for successful application due to its sensitivity.
The SrGS method was proposed to overcome this limitation by eliminating the explicit
penalty term λ. Instead, it introduces a structural “self-regularization” mechanism defined
by the following process:
   1. Competition: For each feature j, a learnable logit tj is normalized via Softmax to
      produce an attention score Sj , enforcing global competition:

                                                exp(tj )
                                         Sj = PD
                                               k=1 exp(tk )

   2. Budgeting: The scores are scaled by the target budget K and clipped to form selection
      probabilities zj , ensuring the expected number of selected features approximates K:

                                        zj = Clip(Sj · K, ϵ, 1)

   3. Stochastic Selection: The final binary masks wj are generated via the differentiable
      Gumbel-Sigmoid reparameterization:
                                                                             
                            1
                   wj = σ     (log zj − log(1 − zj ) + log uj − log(1 − uj ))
                            T

While SrGS empirically demonstrates superior solution quality without hyperparameter
tuning, the theoretical basis for this parameterization remains an open question. Specifically:
   1. Does this specific parameterization rigorously enforce sparsity in the low-temperature
      limit (T → 0)?
   2. What is the exact mathematical form of the implicit regularization induced by this
      mechanism when combined with standard weight decay?




                                                  127
         We answer these questions affirmatively. We analyze the method from two perspectives:
         the behavior of the stochastic objective in the low-temperature limit, and the implicit
         regularization induced by its parameterization.


         1. Stochastic Analysis: Exact ℓ0 Relaxation
         We first analyze the objective in the limit T → 0. In this limit, the expected loss decomposes
         into a deterministic loss and a variance penalty term Rvar (z, θ). The optimization problem
         effectively minimizes:
                                           min Ldet (z, θ) + Rvar (z, θ)
                                            θ,z

         The model derived that the variance penalty takes the form Rvar (z, θ) = j ||Xj ||22 θj2 zj (1 −
                                                                                  P
         zj ). Minimizing this concave function over the hypersimplex encourages solutions at the
         vertices (binary selection).
         Theorem 2 (Implicit ℓ0 Penalty). The implicit regularization induced by the variance
         penalty, defined as R∗ (β) = inf{Rvar (z, θ) | z ∈ H(D, K), z ◦ θ = β}, is an exact penalty
         function for the ℓ0 constraint. Specifically:

                                          R∗ (β) = 0 ⇐⇒ ||β||0 ≤ K

         This result mathematically validates that SrGS provides a continuous, exact relaxation of
         the combinatorial Best Subset Selection problem.


         2. Deterministic Analysis: Adaptive Hybrid Regularization
         We further analyzed the implicit regularization in the deterministic regime where the mask
         w is replaced by its expectation z, combined with ℓ2 regularization  (weight decay) on θ.
         The model discovered that under the budget constraint zj = K and the physical constraint
                                                                P
         0 ≤ zj ≤ 1, the optimization landscape induces a unique Adaptive Hybrid Regularization.
         Theorem 4 (Hybrid Regularization). The implicit regularizer RDR        ∗
                                                                                   (β) partitions the
         features into two sets based on a data-dependent threshold τ :
             • A Saturated Set (A): Features with strong signals (|βj |2/3 ≥ τ ) are assigned full
               probability zj = 1. These features are subject to standard ℓ2 regularization (λ||βA ||22 ),
               which preserves signal magnitude.
             • A Fractional Set (F ): Features with weak signals compete for the remaining budget
               KF = K − |A|. These features are subject to an aggressive ℓ2/3 penalty:

                                        ∗                        λ
                                       RDR (β) = λ||βA ||22 +       ||βF ||22/3
                                                                KF2
         This derivation reveals the mechanism behind SrGS’s superior performance: it automatically
         applies ℓ2 protection to key features while subjecting noise features to non-convex ℓ2/3
         compression.



                           Figure 22: Model resolution of the new theory


Theoretical Findings We answer these questions affirmatively. We utilized the model to analyze
the method from two perspectives: the behavior of the stochastic objective in the low-temperature
limit, and the implicit regularization induced by its parameterization.


                                                    128
Stochastic Analysis: Exact ℓ0 Relaxation. We first analyze the objective in the limit T → 0.
In this limit, the expected loss decomposes into a deterministic loss and a variance penalty term
Rvar (z, θ). The optimization problem effectively minimizes:

                                     min Ldet (z, θ) + Rvar (z, θ)
                                      θ,z

The model derived that the variance penalty takes the form Rvar (z, θ) = j ||Xj ||22 θj2 zj (1 − zj ).
                                                                           P
Minimizing this concave function over the hypersimplex encourages solutions at the vertices (binary
selection).

Theorem 8.21 (Implicit ℓ0 Penalty). The implicit regularization induced by the variance penalty,
defined as R∗ (β) = inf{Rvar (z, θ) | z ∈ H(D, K), z ◦ θ = β}, is an exact penalty function for the ℓ0
constraint. Specifically:
                                       R∗ (β) = 0 ⇐⇒ ||β||0 ≤ K

This result mathematically validates that SrGS provides a continuous, exact relaxation of the
combinatorial Best Subset Selection problem.
Deterministic Analysis: Adaptive Hybrid Regularization. We further analyzed the implicit
regularization in the deterministic regime where the mask w is replaced by its expectation z, combined
with ℓ2 regularization (weight decay) on θ.
The model discovered that under the budget constraint           zj = K and the physical constraint
                                                             P
0 ≤ zj ≤ 1, the optimization landscape induces a unique Adaptive Hybrid Regularization.

Theorem 8.22 (Hybrid Regularization). The implicit regularizer RDR
                                                                ∗ (β) partitions the features

into two sets based on a data-dependent threshold τ :

   • A Saturated Set (A): Features with strong signals (|βj |2/3 ≥ τ ) are assigned full probability
     zj = 1. These features are subject to standard ℓ2 regularization (λ||βA ||22 ), which preserves
     signal magnitude.

   • A Fractional Set (F ): Features with weak signals compete for the remaining budget KF =
     K − |A|. These features are subject to an aggressive ℓ2/3 penalty:

                                  ∗                        λ
                                 RDR (β) = λ||βA ||22 +       ||βF ||22/3
                                                          KF2
This derivation reveals the mechanism behind SrGS’s superior performance: it automatically applies
ℓ2 protection to key features while subjecting noise features to non-convex ℓ2/3 compression.




                                                 129
8.4   Mechanism Design: Revelation Principle Reduction Domain Extension
Written by Song Zuo and David P. Woodruff.

Problem Context
The main task for the model was to extend the key theoretical results of the paper “Mechanism Design
for Large Language Models” [32] from rational bids (Qn+ ) to real bids (Rn+ ). The original paper’s
Revelation Principle (Theorem 3.5) relied on the countability of the bid space. The generalization
was expected to heavily rely on order theory and topological arguments as the assumptions are much
weaker than standard auction theory setups. To avoid the additional mathematical complexity, the
authors restricted bids to be rational.

AI Contributions
We fed the original paper [32] to the model and asked it to bridge the rational to real bids gap for
Theorem 3.5.

   • Proof Attempts and Improvement Reviews: The model initially came up with some
     coarse proofs from the initial ask. Then we also asked the model to review the draft and
     provide improvement suggestions. We iterated through this process with human selection as
     well as additional guidance, and finally reached the complete and rigorous results.

   • Free Bonus on Extension of Theorem 3.12: The model volunteered to also extend
     Theorem 3.12 to general settings.

   • Full Writing with Strategic Guideline and Suggestions from Human: The entire
     material in the next Technical Details section is fully written by the model with human
     suggestions (and some minor corrections).

Human Interventions
Throughout the iteration process, human interventions mainly happen at correcting the model
generated review feedback. Sometimes, the model suggests something distracting, misleading, or
even mathematically suspicious. Human interventions then can help the model get out of potential
dead-loops.

Technical Details
The original paper [32] introduces a Token Auction Model where agents, represented by Large
Language Models (LLMs), submit scalar bids to influence the generation of content. The mechanism
M = ⟨q, z⟩ consists of an aggregation function q that combines agents’ preferred distributions p
based on their bids b, and a payment function z.
The paper establishes a Revelation Principle ([32, Theorem 3.5]), stating that any mechanism satis-
fying Payment Monotonicity and Consistent Aggregation is strategically equivalent to a mechanism
with a Monotone Aggregation Function. The proof relies on the assumption that the bid space
is Qn+ , utilizing the countability of the bids to construct utility representations. Furthermore, the
paper proves the existence of Stable Sampling ([32, Theorem 3.12]). The original proof implicitly
requires the aggregation function to be absolutely continuous by relying on Lebesgue’s Differentiation
Theorem and the Fundamental Theorem of Calculus.


                                                 130
Open Problem: Extend the Revelation Principle and the existence of Stable Sampling to the more
natural domain of real-valued bids, Rn+ , while minimizing additional assumptions and providing
rigorous proofs that do not rely on countability or absolute continuity. We will show this is possible
by assuming the token set T is finite, which is standard in practice.

Key Definitions We restate the key definitions from [32] for completeness. Let ∆(T ) be the set
of distributions over tokens T . Let ⪰i be the preference relation of agent i over ∆(T ).

Definition 8.23 (Robust Preferences). Given preferred distribution pi , q ⪰i q ′ if ∀t ∈ T, |q(t) −
pi (t)| ≤ |q ′ (t) − pi (t)| and (q(t) − pi (t))(q ′ (t) − pi (t)) ≥ 0.

Definition 8.24 (Payment Monotonicity). Mechanism M = ⟨q, z⟩ satisfies payment monotonicity
if for all p, b−i , bi , b′i : zi (bi , b−i , p) ≥ zi (b′i , b−i , p) ⇐⇒ q(bi , b−i , p) ⪰i q(b′i , b−i , p).

Definition 8.25 (Consistent Aggregation). q(b, p) is consistent if: if q(bi , b−i , p) ≻i q(b′i , b−i , p)
for some b−i , then for all b′−i , q(bi , b′−i , p) ⪰i q(b′i , b′−i , p).

Definition 8.26 (Monotone Aggregation Function). q(b, p) is monotone if for all p, b−i and bi ≥ b′i :
q(bi , b−i , p) ⪰i q(b′i , b−i , p).

Methodology and Assumptions
We extend the bid space to Rn+ . We assume the token set T is finite. This ensures the space of
distributions ∆(T ) is a finite-dimensional simplex, which is a compact, metrizable, and second-
countable space.

Extending the Revelation Principle The main challenge in extending Theorem 3.5 is the failure
of the countability argument used in [32]. Approach: We replace the countability arguments with
topological and order-theoretic methods. We establish a utility representation using the topological
properties of the codomain. Then, we prove a general Monotone Extension Lemma that allows
extending the transformed monotone aggregation function from the image of the utility representation
to the entire bid space Rn+ . This approach relies only on the continuity of the underlying preferences
and the compactness of ∆(T ), removing the need for continuity assumptions on the aggregation
function q. This approach requires the following assumptions:

Assumption 8.27 (A1: Continuous Preferences). The partial order ⪰i on ∆(T ) is continuous (i.e.,
its graph is closed in ∆(T ) × ∆(T )).

We also formalize an assumption that was inherent in the original framework:

Assumption 8.28 (A2: Anti-symmetry of Preferences). The order ⪰i is anti-symmetric (i.e.,
(q ⪰i q ′ and q ′ ⪰i q) =⇒ q = q ′ ). Here ∼i denotes the symmetric component of ⪰i . This means ⪰i
is a true partial order, not just a preorder.

Robust Preferences satisfy A1 and A2. However, we state A2 explicitly as the Revelation Principle
applies to general partial orders. A2 is crucial to ensure that the transformed aggregation function q̃
is well-defined. Combined with Payment Monotonicity, it ensures that payments are invariant if
the allocation remains the same, which is necessary for the transformed payment function z̃ to be
well-defined.
It is worth noting that A2 is restrictive in the context of LLMs, where preferences are typically
defined via continuous loss functions (e.g., KL-divergence) which naturally have non-trivial level

                                                    131
sets (i.e., distinct distributions can be equally preferred). If A2 is relaxed, the Revelation Principle
can still theoretically hold for preorders if the mechanism specifies a consistent tie-breaking rule
across indifference classes (see the Discussion and Limitation section for the topological limitations
of tie-breaking).
To ensure that payment functions and strategy mappings remain well-defined in the measure-theoretic
sense (which will be essential for integration in later sections), we explicitly state the following
measurability assumption:

Assumption 8.29 (A3: Measurability). The initial aggregation function q(b, p) is Borel-measurable
with respect to the bids b.

By removing any continuity assumption on the aggregation function q, our Extended Revelation
Principle applies to a broad class of mechanisms, including those with discontinuous allocation rules
(e.g., step functions) common in mechanism design.

Extending Stable Sampling. The challenge in extending Theorem 3.12 is the reliance on
differentiation in the original proof. Approach: We use a measure-theoretic approach. We associate
Lebesgue-Stieltjes (LS) measures with the monotone components of the aggregation function and
use the Radon-Nikodym theorem to characterize the transport of probability mass. We carefully
define the measures on (0, ∞) to rigorously handle the boundary at b = 0.
Importantly, the general Revelation Principle (Theorem 3.5) established in the next section guarantees
the existence of an equivalent monotone mechanism, but it does not necessarily guarantee right-
continuity without loss of generality. However, this technical assumption is standard for defining
Lebesgue-Stieltjes measures associated with increasing functions. Thus, for the Stable Sampling
construction, we explicitly require:

Assumption 8.30 (A4: Right-Continuity). The aggregation function q(b, p) is right-continuous in
b.

Extended Revelation Principle
We now formally prove the extension of the Revelation Principle to Rn+ , assuming A1, A2, and A3
hold.

Utility Representation

Lemma 8.31 (Extended Lemma 3.6). Assume A1. Let the bid space be Rn+ . For any distribution
aggregation function q, there exists a payment function z such that mechanism M = ⟨q, z⟩ is payment-
monotone if and only if ⪰i establishes a total order over Q(b−i , p) = {q(bi , b−i , p) : bi ∈ R+ } for
any fixed b−i and p.

Proof. The “only if” direction follows directly from the definition of Payment Monotonicity. We
prove the “if” direction. Fix i, b−i , p. Let Q = Q(b−i , p). By hypothesis, ⪰i is a total order on Q.
Let Q be the closure of Q in ∆(T ). Since T is finite, the probability simplex ∆(T ) is a compact
metric space, making Q a compact metric space, which is second-countable under the subspace
topology. By A1, ⪰i is continuous, so the total order extends to a continuous total preorder on Q.
Debreu’s Theorem [29] guarantees that there exists a continuous utility representation ui : Q → R
for the preference relation ⪰i restricted to Q. We can always choose a bounded representation
(e.g., by composing with a strictly increasing, bounded function). Defining the payment function
zi (bi , b−i , p) = ui (q(bi , b−i , p)) yields a payment-monotone mechanism.

                                                  132
Monotone Extension Lemmas To extend the aggregation function from the image of the strategy
mappings to the entire space Rn+ , we need the following lemmas. We provide a supremum-based
extension that naturally guarantees monotonicity.
Lemma 8.32 (1D Monotone Extension). Let I ⊆ R+ . Let X be a compact metric space (e.g., ∆(T ))
with a continuous partial order ⪰ (A1). Let g : I → X be a monotone function (non-decreasing) such
that its image g(I) is totally ordered by ⪰. Let A denote the topological closure of a subset A ⊆ X.
Let xmin = min g(I). Let Yt = {g(y) : y ∈ I, y ≤ t}. Then the function G : R+ → X defined by
                                             (
                                              max Yt if Yt ̸= ∅
                                      G(t) =
                                              xmin     if Yt = ∅
is a monotone extension of g.
Proof. We first show G(t) is well-defined. Since X is compact and ⪰ is continuous, the closure of
any totally ordered subset of X is compact and totally ordered. Thus, for any t where Yt ̸= ∅, its
closure Yt ⊆ g(I) possesses a maximum element in X. Similarly, since X is a compact metric space
and g(I) is a closed subset, xmin = min g(I) is guaranteed to exist. Note that this construction does
not require the domain I to be compact.
Monotonicity: If t′ ≥ t. Case 1: Yt ̸= ∅. Then Yt′ ⊇ Yt , which implies Yt′ ⊇ Yt . Thus
max Yt′ ⪰ max Yt , so G(t′ ) ⪰ G(t). Case 2: Yt = ∅. G(t) = xmin . For any t′ , since Yt′ ⊆ g(I), it
follows that Yt′ ⊆ g(I), so by definition of xmin , G(t′ ) ⪰ xmin = G(t).
Extension property: If t ∈ I. Then Yt ̸= ∅. Since g is monotone, g(t) is the maximum element of
Yt . Since Yt ⊆ Yt and g(t) ∈ Yt , G(t) = max Yt = g(t).

Lemma 8.33 (Monotonicity Preservation). Under the assumptions of Lemma 8.32, let g ′ : I → X
be another monotone function such that g ′ (I) is totally ordered by ⪰. Let ⪰′ be another continuous
partial order on X. If g ′ (y) ⪰′ g(y) for all y ∈ I, then their monotone extensions G′ and G satisfy
G′ (t) ⪰′ G(t) for all t ∈ R+ .
Proof. Fix t ∈ R+ . Case 0: Yt = ∅ (t < inf I). G(t) = xmin and G′ (t) = x′min . Since g and g ′ are
monotone w.r.t. ⪰, xmin and x′min are realized as the limits of g(yk ) and g ′ (yk ) respectively, for any
sequence yk ∈ I such that yk → inf I. We are given g ′ (yk ) ⪰′ g(yk ). By continuity of ⪰′ , taking the
limit yields x′min ⪰′ xmin . Thus G′ (t) ⪰′ G(t).
Case 1: Yt ̸= ∅. Let y ∗ = sup(I ∩ [0, t]). Case 1a: y ∗ ∈ I. By the extension property in Lemma 8.32,
G(t) = g(y ∗ ) and G′ (t) = g ′ (y ∗ ). Since g ′ (y ∗ ) ⪰′ g(y ∗ ), we have G′ (t) ⪰′ G(t). Case 1b: y ∗ ∈
                                                                                                          / I.
Since y is the supremum of I ∩ [0, t] and does not belong to the set, it must be a limit point of the
          ∗

set I ∩ [0, t]. Therefore, there exists an increasing sequence yk ∈ I ∩ [0, t] such that yk → y ∗ . Since g
is monotone w.r.t. ⪰, g(yk ) is non-decreasing. As G(t) is the maximum of Yt , G(t) = limk→∞ g(yk ).
In a compact metric space with a continuous total order, bounded monotone sequences converge
to their suprema (in the order topology, which coincides with the subspace metric topology here
since the image is totally ordered and closed). Similarly, G′ (t) = limk→∞ g ′ (yk ). We are given
g ′ (yk ) ⪰′ g(yk ) for all k. By the continuity of the order ⪰′ (A1), the order is preserved in the limit.
Thus, G′ (t) ⪰′ G(t).

Strategic Equivalence
Lemma 8.34 (Extended Lemma 3.7). Assume A1, A2, and A3. Let the bid space be Rn+ . Consider
any consistent aggregation function q. Suppose ⪰i defines a total order over the aggregation set
Q(b−i , p) for any fixed b−i and p. Then there exists a profile π of strategy mappings such that
q(b, p) = q̃(π(b), p) for some monotone aggregation function q̃(·, ·).

                                                    133
Proof. We proceed in several steps.
Step 1: Induced Preference. Define the induced preference ⪰i,p on R+ : bi ⪰i,p b′i if q(bi , b−i , p) ⪰i
q(b′i , b−i , p) for all b−i . Consistency ensures this is a total preorder on R+ .
Step 2: Strategy Mapping via Pull-back. We seek a utility representation πi : R+ → R+ for
the induced preorder ⪰i,p . Let Q∗ be the image of q(·, b∗−i , p) for an arbitrary fixed reference profile
b∗−i . By the premise, ⪰i is a total order on Q∗ . Let Q∗ be its closure in ∆(T ). Since the token
set T is finite, Q∗ is a second-countable, compact metric space. By A1, the preference relation ⪰i
is continuous. The continuity of ⪰i ensures that the total order property of Q∗ transfers to its
closure Q∗ . Thus, ⪰i is a continuous total preorder on Q∗ . By Debreu’s theorem [29], the continuous
preference relation ⪰i on Q∗ admits a continuous utility representation ui : Q∗ → R. We can assume
without loss of generality that the image of ui is in R+ (by composing with a strictly increasing,
positive-valued function if necessary). We define the strategy mapping by pulling back the utility
from the codomain: πi (bi ) := ui (q(bi , b∗−i , p)). By Assumption A3, q is Borel-measurable. Since ui is
continuous, the composition πi is measurable. The Consistent Aggregation property (Definition 8.25)
ensures that the preference ordering induced by this mapping is independent of the choice of the
reference profile b∗−i . By definition of ⪰i,p , bi ⪰i,p b′i ⇐⇒ q(bi , b∗−i , p) ⪰i q(b′i , b∗−i , p) ⇐⇒
ui (q(bi , b∗−i , p)) ≥ ui (q(b′i , b∗−i , p)) ⇐⇒ πi (bi ) ≥ πi (b′i ). Thus, πi is a valid utility representation for
⪰i,p . This rigorous construction bypasses the need for an order-density assumption on the bid space
R+ under the potentially disconnected topology induced by ⪰i,p .
Step 3: Defining q̃ on the Image. Let Ii be the image of πi , and I = I1 × · · · × In . Define
q̃(π(b), p) = q(b, p). We must show this is well-defined. If π(b) = π(b′ ), then bi ∼i,p b′i for all i. This
means q(bi , b−i , p) ∼i q(b′i , b−i , p) for all b−i . By A2 (Anti-symmetry), this implies equality of the
distributions. We show q(b) = q(b′ ) by changing bids one by one. Let b(k) = (b′1 , . . . , b′k , bk+1 , . . . , bn )
be the bid profile with the first k bids from b′ and the rest from b. Since bk+1 ∼k+1,p b′k+1 , we
have q(b(k) ) ∼k+1 q(b(k+1) ). By A2, q(b(k) ) = q(b(k+1) ). Thus, q(b) = q(b′ ). The function q̃ is
monotone on I by construction of π. Furthermore, the 1D images of q̃ are totally ordered since the
1D images of q are assumed to be totally ordered.
Step 4: Monotone Extension. We extend q̃ from I to Rn+ iteratively. In step k, we extend the
domain from Dk−1 = Rk−1        + × Ik × · · · × In to Dk = R+ × Ik+1 × · · · × In . We use Lemma 8.32 to
                                                                      k

extend along the k-th dimension using the standard numerical order ≥ on the k-th coordinate. This
is possible because the required conditions (A1, compactness of ∆(T ), total order on 1D images) are
met. We must ensure that this extension preserves the monotonicity w.r.t. other orders ⪰j . For
j > k, this follows from Lemma 8.33 (with ⪰=⪰k and ⪰′ =⪰j ). For j < k, the domain is already
R+ in the j-th dimension, and the extension in the k-th dimension also preserves monotonicity in
the j-th dimension by Lemma 8.33 (by viewing the j-th coordinate as the parameter defining g
vs g ′ , and the k-th coordinate as the domain being extended). This iterative process yields the
monotone extension q̃ on Rn+ . Furthermore, since the extended aggregation function q̃ is monotone
in each coordinate by construction, it is continuous almost everywhere with respect to the Lebesgue
measure, and thus preserves joint Borel-measurability on the entire domain Rn+ (e.g., by Lebesgue’s
theorem for monotone functions), thus satisfying the measurability requirement of the mechanism
(Assumption A3).

The Main Theorem

Theorem 8.35 (Extended Theorem 3.5). Let the bid space be Rn+ . Assume A1, A2, and A3. Any
mechanism M = ⟨q, z⟩ with a consistent aggregation function q and a monotone payment function z
is strategically equivalent to a mechanism M̃ = ⟨q̃, z̃⟩ which has a monotone aggregation function q̃
and a monotone payment function z̃.

                                                        134
Proof. By Payment Monotonicity of M and Lemma 8.31, the prerequisites for Lemma 8.34 are met.
Lemma 8.34 yields the mappings π and the monotone function q̃. We define z̃ on the image I by
z̃(π(b), p) = z(b, p). If π(b) = π(b′ ), then bi ∼i,p b′i for all i. As shown in the proof of Lemma 8.34
(Step 3), under A2 this implies q(b, p) = q(b′ , p). Since the outcomes are identical, by Payment
Monotonicity, zi (b, p) = zi (b′ , p) for all i. Thus, z̃ is well-defined. M satisfies Payment Monotonicity
because M does and q̃, z̃ are defined via the preference representation π.
Finally, we extend z̃ from I to Rn+ . Note that the original mechanism M is fixed, so its payment
function z is predetermined and may be unbounded. To accommodate this, we take the codomain
X for the extension to be the extended real line R = [−∞, ∞], which is a compact metric space
under the standard order topology. The image of z̃i on I is a subset of R. Since z̃i is monotone in
each component (with the standard order on R), we can apply the Monotone Extension Lemma
(Lemmas 8.32 and 8.33 applied to the standard order on R) iteratively to extend z̃ to Rn+ .
Note that the iterative dimension-by-dimension extension in Step 4 of Lemma 8.34 means that the
final extended mechanism depends on the order in which the dimensions are processed. This renders
the constructed equivalent mechanism non-unique. However, since the equivalence holds on the
image of the strategy mappings, these choices correspond to off-path bids and do not affect the
on-path behaviors, strategic properties, or equilibrium payments.

Extended Stable Sampling
We now generalize Theorem 3.12 to R+ using measure theory, relying on assumption A4 (Right-
Continuity) for the monotone aggregation function. We utilize the definitions of T + and T − from
Lemma 3.10 in [32]. For notational precision, we define limits at infinity as qo (∞) := limb→∞ qo (b)
and Q− (∞) := limb→∞ Q− (b).

Theorem 8.36 (Extended Theorem 3.12). Given a monotone distribution aggregation function
q satisfying A4, for any agent i with robust preferences (and fixed b−i , p), there exists a stable
implementation σ of q(bi ).

Proof. Let q(b) = q(bi , b−i , p). Following [32], define T + = {t ∈ T : qt (0) ≤ (pi )t } (weakly
undersampled) and T − = {t ∈ T : qt (0) > (pi )t } (strictly oversampled). These sets form a partition
of T . By Lemma 3.10 in [32], qt (b) is non-decreasing for t ∈ T + and non-increasing for t ∈ T − . By
A4, these functions are right-continuous.
Step 0: Setup and Trivial Case. We define associated Lebesgue-Stieltjes (LS) measures on
(0, ∞). For u ∈ T + , let νu be the LS measure of the non-decreasing function qu (b), defined such
that νu ((a, b]) = qu (b) − qu (a) for 0 ≤ a < b. For o ∈ T − , let νo be the LS measure of the
nondecreasing
            P function qo (0) − qo (b), defined such that νo ((a, b]) = qo (a) − qo (b) for 0 ≤ a < b. Let
Q+ (b) = u∈T + qu (b). Let ν be the LS measure of Q+ (b) on (0, ∞). By the Right-Continuity
assumption (A4), Q+ (0) = Q+ (0+ ), which guarantees that the measure places no point mass at 0, i.e.,
ν({0}) = 0. This ensures the integration   domain
                                               P is strictly (0, bi ] as used in subsequent integrations.
By conservation of probability, u νu = ν = o νo . Let M = ν((0, ∞)) = Q+ (∞) − Q+ (0+ ) be the
                                  P
total mass moved. If M = 0, then q(b) = q(0) for all b. Let q ∗ = q(0). We define the implementation
σ(b, r) for the trivial case M = 0 directly on R by mapping all r to a sample from q ∗ . This is
trivially stable. Assume M > 0.
Step 1: Measure Theoretic Setup. Since ν((0, ∞)) = M ≤ 1, ν is a finite measure, which strictly
fulfills the σ-finite condition for the Radon-Nikodym theorem. Since νt (A) ≤ ν(A) on (0, ∞), νt is
absolutely continuous w.r.t. ν. Let ft (θ) = dν
                                              dν (θ) be the Radon-Nikodym derivative for θ ∈ (0, ∞).
                                                t

Note that these derivatives are unique only up to a set of ν-measure zero. Consequently, the sampling
implementation σ(b, r) constructed below is determined ν-almost everywhere. Using u ∈ T + and

                                                   135
o ∈ T − as index variables for the respective subsets, we have u∈T + fu (θ) = 1 and o∈T − fo (θ) = 1
                                                              P                    P
(ν-a.e.). We define a joint measure µ on T − × T + × (0, ∞) representing the mass transport. For
any measurable set A ⊆ T − , B ⊆ T + , and E ⊆ (0, ∞), the measure is defined via its action on
measurable product sets:
                                           Z              !          !
                                                X            X
                        µ(A × B × E) =              fo (θ)     fu (θ) dν(θ).
                                               E    o∈A                  u∈B

Step 2: Construction of Stable Sampling σ. We define             P the randomness space R and the
implementation σ(b, r). Let S + = Q+ (0) and S − = Q− (∞) = o∈T − qo (∞). Note S + + S − + M =
Q+ (0) + Q− (∞) + (Q+ (∞) − Q+ (0+ )). By the Right-Continuity assumption (A4), Q+ (0) =
Q+ (0+ ). Additionally, by the definition of the partition, we have the identity Q− (∞) = 1 − Q+ (∞).
Substituting these, the expression simplifies algebraically to (1 − Q+ (∞)) + Q+ (∞) = 1. We define
the randomness space R as the disjoint union RS + ∪ RS − ∪ RM , where RS + = T + , RS − = T − , and
RM = T − × T + × (0, ∞). We equip R with the σ-algebra ΣR formed by the disjoint union of the
discrete σ-algebras on the finite sets T + and T − , and the Borel σ-algebra on RM (with the discrete
topology on T − and T + ). We define the probability measure P on (R, ΣR ) as follows:
   • On RS + : For u ∈ RS + , P (u) = qu (0).
   • On RS − : For o ∈ RS − , P (o) = qo (∞).
   • On RM : The restriction of the probability measure P to RM is the joint measure on the Borel
     σ-algebra given by µ defined in Step 1.
We define the implementation σ(b, r) for r ∈ R as follows: 1. If r ∈ RS + (Static T + ), r = u. Set
σ(b, r) = u. 2. If r ∈ RS − (Static T − ), r = o. Set σ(b, r) = o. 3. If r ∈ RM (Moving Mass),
r = (o, u, θ). Since θ > 0, we set σ(b, r) = u if b ≥ θ, and σ(b, r) = o if b < θ.
Step 3: Verification. Stability: By construction, for any realization r, the output σ(b, r) as a
function of b is either constant (cases 1 and 2) or switches exactly once from o ∈ T − to u ∈ T + at
b = θ (case 3).
Measurability: By construction, the components of σ(b, r) are either constant or simple indicator
functions of the form I(b ≥ θ) for θ ∈ (0, ∞), which are Borel measurable. Thus, σ(b, r) is a valid
random variable with respect to ΣR .
Correctness: We verify the marginal probability for u ∈ T + . P (σ(b) = u) = P (r = u) + P (r ∈
RM , σ(b, r) = u). The first term is qu (0).
                                               Z
                           P (Moving part) =         I(σ(b, r) = u)dP (r)
                                                 RM
                                                X Z
                                             =              I(b ≥ θ)dµ(o, u, θ)
                                                             (0,∞)
                                                   o∈T −
                                                   Z         X
                                               =                     fo (θ)fu (θ)dν(θ).
                                                    (0,b]
                                                            o∈T −

Since   o∈T − fo (θ) = 1 (ν-a.e.), this equals:
        P
                                Z                       Z
                            =           fu (θ)dν(θ) =               dνu (θ) = νu ((0, b]).
                                (0,b]                       (0,b]

By right-continuity (A4), the LS measure satisfies νu ((0, b]) = qu (b) − qu (0). Thus, P (σ(b) = u) =
qu (0) + (qu (b) − qu (0)) = qu (b). The verification for o ∈ T − is similar.

                                                        136
Remark 8.37 (Algorithmic Constructiveness). The proof of Theorem 8.36 provides an existence result
for stable sampling based on a measure-theoretic construction involving Radon-Nikodym derivatives
ft (θ). While theoretically sound, this construction does not immediately yield an efficient sampling
algorithm. Note that while the standard inverse-CDF method (F −1 (u) = inf{x : F (x) ≥ u}) is
universally applicable to any 1D cumulative distribution function (requiring only right-continuity
and non-decreasing properties), the difficulty in the multidimensional LLM implementation arises
from the measure-theoretic coupling of probabilities across different tokens, rather than a lack of
absolute continuity. In practical computational settings, the Radon-Nikodym derivatives ft (θ) can
be approximated. For example, the bid space can be discretized into a fine grid to estimate the
derivatives using finite differences on the empirical cumulative distributions, or one can parameterize
the measures using continuously differentiable generative models where the densities are explicitly
tractable.
Consequently, Proposition 3.13 (Myerson-style payment formula) also generalizes to R+ . We note
                                                                     Rb
that the formula presented in the reference paper [32], zi (bi ) = 12 0 i (||q(bi ) − pi ||1 − ||q(b′ ) − pi ||1 )db′ ,
contained a sign error, leading to non-positive payments as the L1 distance is decreasing in b. We
provide the corrected formula and its derivation.
Proposition 8.38 (Corrected Payment Formula). Under robust preferences and a monotone ag-
gregation function q satisfying A4, the expected payment zi (bi ) induced by the second price rule via
stable sampling satisfies:
                                Z
                              1
                   zi (bi ) =           (||q(θ) − pi ||1 − ||q(bi ) − pi ||1 )dθ, ∀bi ∈ R+ .
                              2 (0,bi ]
Proof. We derive the payment formula using the stable implementation σ constructed in Theorem 8.36.
Let Zi (bi , r) be the random variable representing the ex-post payment for agent i given a bid bi
and a realization r ∈ R. Under the second-price rule, the payment is the critical bid at which the
outcome changes. For a realization r ∈ RM , where r = (o, u, θ), the outcome changes from o to u at
bid θ. Thus, Zi (bi , r) = θ if bi ≥ θ, and 0 otherwise. For r ∈ RS + ∪ RS − , the outcome is constant,
so the critical bid is 0, meaning Zi (bi , r) = 0. The expected payment is:
                                              Z                     X X Z
                zi (bi ) = Er [Zi (bi , r)] =   Zi (bi , r)dP (r) =            θdµ(o, u, θ).
                                                  RM                                (0,bi ]
                                                                     o∈T − u∈T +

Using the definition of µ and the fact that o∈T − fo (θ) = 1 and u∈T + fu (θ) = 1 (ν-a.e.):
                                             P                   P

                                                         
                           Z       X              X                  Z
                zi (bi ) =     θ       fo (θ)      fu (θ) dν(θ) =
                                                                         θdν(θ).
                              (0,bi ]                                                 (0,bi ]
                                         o∈T −            u∈T +

Recall that ν is the LS measure associated with the increasing, right-continuous function Q+ (b) on
(0, ∞). Using
          R the standard integration by parts Rformula for Lebesgue-Stieltjes integrals on half-open
intervals, (a,b] U dV = U (b)V (b) − U (a)V (a) − (a,b] V (x−)dU (x). By setting a = 0, U (x) = x, and
V (x) = Q+ (x), the boundary term at a = 0 evaluates directly as 0 · Q+ (0) = 0. Furthermore, noting
that Q+ (x−) = Q+ (x) almost everywhere with respect to the Lebesgue measure dU (x) = dx, we
obtain:                            Z                             Z
                        zi (bi ) =      θdQ+ (θ) = bi Q+ (bi ) −      Q+ (θ)dθ.
                                        (0,bi ]                           (0,bi ]
This yields the final integral directly without the need for the intermediate limit notation. This
is the standard Myerson payment formula with allocation probability Q+ (b). Now we relate this

                                                         137
to theP
      L1 distance. Let D(b) = ||q(b) − pi ||1 . P
                                                Under robust preferences (Lemma 3.10 in [32]), let
P+ = u∈T + (pi )u and explicitly define P− = o∈T − (pi )o . We analyze the distance:
                X                       X
       D(b) =       ((pi )u − qu (b)) +   (qo (b) − (pi )o ) = (P+ − Q+ (b)) + (Q− (b) − P− ).
                u∈T +                  o∈T −

Since Q− (b) = 1 − Q+ (b) and P− = 1 − P+ , we have D(b) = 2(P+ − Q+ (b)). We now evaluate the
integral I in the proposition statement:
                                   Z
                                 1
                            I=              (D(θ) − D(bi ))dθ
                                 2 (0,bi ]
                                Z
                              =           ((P+ − Q+ (θ)) − (P+ − Q+ (bi )))dθ
                                  (0,bi ]
                                               Z
                              = bi Q+ (bi ) −        Q+ (θ)dθ.
                                               (0,bi ]

Thus, zi (bi ) = I. This confirms the corrected formula and ensures non-negative payments, as D(b) is
non-increasing in b.

Discussion and Limitations
This note successfully extends the core theoretical results of the reference paper from rational to
real-valued bids by employing topological and measure-theoretic tools, under the practical assumption
of a finite token vocabulary. However, these generalizations reveal important limitations and suggest
directions for future research.
Restrictiveness of the Anti-Symmetry Assumption (A2) in the LLM Context. The reliance
on anti-symmetry (A2) for the Revelation Principle excludes scenarios where agents are indifferent
between distinct distributions. This is a significant limitation in the context of LLMs, where
preferences are typically defined via continuous loss functions (e.g., KL-divergence). Continuous loss
functions naturally have non-trivial level sets (indifference classes), meaning distinct distributions
can be equally preferred, which violates A2.
Topological Incompatibility of Tie-Breaking Rules. A natural attempt to satisfy the Anti-
Symmetry assumption (A2) in the presence of indifference classes is to introduce a deterministic
tie-breaking rule, such as a lexicographic ordering over the token probabilities. However, it is a
well-established result in mathematical utility theory (e.g., [29], [86]) that lexicographic orders on
spaces of dimension greater than one (such as ∆(T ) for |T | ≥ 3) do not admit continuous utility
representations. Specifically, such tie-breaking rules violate the Continuity Assumption (A1) by
creating non-closed preference graphs (open sets of strictly preferred outcomes). Since the Extended
Revelation Principle critically relies on Debreu’s Representation Theorem to construct the strategy
mappings πi , violating A1 invalidates the utility representation step in Lemma 8.31 and Lemma 8.34.
Therefore, A1 and A2 cannot be simultaneously satisfied by simply overlaying a standard tie-breaking
rule on continuous loss functions. Relaxing A2 by designing appropriate tie-breaking mechanisms
that preserve continuity remains an open problem.
The Continuity Gap in the Revelation Principle. There is a fundamental tension between
the generality of the Extended Revelation Principle (Theorem 8.35) and the requirements for
Stable Sampling (Theorem 8.36). The Revelation Principle applies broadly, even to discontinuous
mechanisms, by constructing an equivalent monotone mechanism. However, this constructed
mechanism is not guaranteed to be right-continuous (A4). Since the strategy mappings π and the
underlying aggregation function q are not required to be continuous, the image space I can be

                                                     138
disconnected, and the utility values can have jumps. Consequently, any extension scheme—whether
based on the supremum or the infimum—cannot universally guarantee right-continuity. Specifically,
an infimum-based extension from the right would fail to be right-continuous at the boundary points
of the gaps in I.
While this leaves a theoretical gap between the mechanisms covered by the Revelation Principle and
those implementable via Stable Sampling, it is important to emphasize that the Revelation Principle
successfully establishes that we can, without loss of generality, focus on monotone mechanisms. This
aligns with standard auction theory, where monotonicity is the cornerstone of incentive compatibility.
Given the weak assumptions required, this is a positive foundational result. Bridging this gap—either
by identifying conditions under which right-continuity can be preserved, extending Stable Sampling
to left-continuous mechanisms, or proving that non-right-continuous mechanisms offer no strategic
advantage—is an interesting direction for future research that goes beyond the scope of this note.




                                                 139
8.5    Networked Information Aggregation for Binary Classification
Written by MohammadHossein Bateni, Zahra Hadizadeh, MohammadTaghi Hajiaghayi, Mahdi
JafariRaviz, and Shayan Taherijam.

Problem Context
Recent work by Kearns et al. [64] shows basic limits on information aggregation in distributed
learning. In their framework, agents in a Directed Acyclic Graph (DAG) act in sequence and
minimize Mean Squared Error (MSE), while each agent only sees a subset of the input features and
the predictions made by earlier agents.
Moving from regression to binary classification, using a non-linear link function such as logistic
regression, raises new challenges. MSE can still be used, but Binary Cross Entropy (BCE) is the
standard loss for classification. BCE is harder to study because it is not quadratic. It is open
whether the aggregation limits seen with MSE also show up in this classification setting.

AI Contribution
The AI acted as a theoretical collaborator to extend distributed learning limits from linear regression
(MSE loss) to binary classification (Binary Cross Entropy loss). By breaking the proof into modular
lemmas, the model successfully utilized KL-divergence and Pinsker’s inequality to rigorously bound
the excess risk of the final agent in the network.
Overall, the structured prompt in Figure 23 below was instrumental in generating rigorous proofs at
several stages of our experience to prove the full theorem.


      Task: Based on the attached PDF, prove conjecture/theorem X below. You must provide a
      rigorous, bug-free proof decomposed into elementary lemmas.
      Strict Standards:
      Rigor > Completion: A rigorous partial analysis (Outcome 2) is vastly superior to a flawed
      complete proof.
      No Hallucinations: Every lemma must be proven from elementary principles.
      Verification: Explicitly verify every step. If you find a gap, stop and report it.
      Required Output Format (Choose One):
      Outcome 1: COMPLETE PROOF (Use ONLY if every step is 100% rigorous and all cases
      are covered. Provide a formal, stand-alone proof.)
      Outcome 2: STRUCTURED PARTIAL PROGRESS (Use if ANY logical gaps or unproven
      assumptions exist.)
      Proven Lemmas: Rigorously prove what you can.
      The Crux: Pinpoint exactly where the proof stalls.
      Next Steps: Propose strategies to bridge the gap.



Figure 23: The structured prompt above has led to rigorous proofs, well-organized proof structures,
and clear technical insights. The attached PDF represents the current proof structure developed
with the assistance of Gemini and further refined by our own reasoning.




                                                   140
Details of the Process
Aaron Roth, one of the authors of the original framework [64], shared how his team integrated AI
into their research. He described treating the AI as a colleague, providing high-level mathematical
intuition which the model expanded into formal proofs. He noted that while this accelerated their
work, it required careful verification to catch “human-like” errors.
Adopting this approach, we considered replacing the loss in their framework with BCE using logistic
regression. We asked Gemini 3 Pro to derive a theorem like the one in the linear regression setting.
It produced a short chain of lemmas and a final theorem that bounds the excess loss of the last node
in the DAG, compared to a logistic regression learner that has access to all input features.
While checking the output, we found one key first lemma (Lemma 8.41) and verified that Gemini
proved it correctly. The lemma states that the minimizer of the BCE loss outputs predictions
p∗ (x) such that the residual p∗ (x) − y (where y is the binary label) is orthogonal to the input x in
expectation. Formally, E[x(p∗ (x) − y)] = 0. We knew this would matter because it is also the first
building block in the MSE setting. The next lemma (Lemma 8.42) compared the loss of the optimal
predictor to the loss of any other logistic predictor. Gemini correctly identified that the loss gap can
be written using the Kullback–Leibler divergence between the predictors’ output distributions. The
lemma itself was needed for the rest of the argument, but Gemini made a mistake near the end of
the proof, and we fixed it.
The next step was the final theorem bounding the excess loss. The bound it gave was stronger than
                                                                                                2
in the linear regression setting: there the bound was √MD , while here Gemini claimed MD , which
is smaller when √MD < 1. This is where Gemini started to go off track. Instead of breaking the
proof into short lemmas, it wrote one long proof that was not correct. It also added a major new
assumption: Assume the loss is µ-strongly convex.
We kept the theorem statement, including the assumption and the stronger bound, and asked Gemini
to regenerate a proof in a fresh context. Here the prompt in Figure 23 was especially helpful and
this time the proof was correct. However, the µ-strong convexity assumption felt indirect.
Next, we asked Gemini to remove the µ-strong convexity assumption and replace it with something
closer to the boundedness assumptions used by Kearns et al. It produced a correct proof, with the
weaker bound of √MD , under a new assumption: the coefficient vectors of every agent’s predictor, and
of the optimal predictor, have bounded L1 norm. This was still a stronger assumption than what
was needed in the linear regression setting, where the bound only applies to the optimal predictor.
We did not think this was a major issue, so we accepted the theorem statement. At that point, we
believed the theorem and proof were correct. Still, we prompted Gemini to look for flaws in the
proof or statement.
It found an error we had missed: you can compare convexity bounds for a parameter θ to the optimal
parameter θ∗ only when the loss is defined over the same set of indices. Gemini also suggested the
fix: since θ∗ lives on the full set of indices, we can pad θ with zeros to get θ′ , and also pad and
add the predecessors’ parameter vectors in the same coordinate system. The problem was that we
assumed θ has bounded L1 norm, and now we would also need θ′ to have bounded norm. But θ′
depends on predecessors’ parameters through this padding-and-summing step, so the norm can grow
quickly with depth, and it did not seem reasonable to assume it stays bounded.
We then took a different path. We noticed that the orthogonality lemma was mainly used for a
predictor against its own subset of input indices, and orthogonality to predecessors’ logit outputs
was not really used.
We changed the assumptions to only require boundedness of the optimal predictor, and asked Gemini
to prove the theorem under this smaller assumption, hinting that it should use the orthogonality
lemma. Again the prompt in Figure 23 was very helpful. As a result, Gemini did so by breaking

                                                  141
the proof into lemmas, reusing the correct parts under the new assumption, and adding new helper
lemmas to reach the final bound.
We then cleaned up the writing and the lemma flow, again using Gemini for rewriting and proofreading.

The theorem
We consider a distributed learning system where agents are arranged in a Directed Acyclic Graph
(DAG). Let P a(i) denote the set of predecessors of agent Ai . Agents are indexed 1, . . . , N consistent
with a topological sort of the graph. Each agent Ai observes a local subset of features xSi from the
input x ∈ Rd and the logits {zj }j∈P a(i) from its predecessors. The agent computes its own logit zi
and prediction pi = σ(zi ) (where σ is the sigmoid function 1/(1 + e−x )) using learnable parameters
wi and vij :                                          X
                                     zi = wi⊤ xSi +        vij zj .
                                                       j∈P a(i)

Agents sequentially update their parameters to minimize the expected Binary Cross Entropy (BCE)
loss with respect to the target y ∈ {0, 1}:

                               L(pi ) = −E [y log pi + (1 − y) log(1 − pi )] .

We also use the notation zθ = θT x, pθ = σ(zθ ), and L(θ) = −E [y log pθ + (1 − y) log(1 − pθ )].
We now give the following definition.
Definition 8.39 (M -Coverage Condition, from Kearns et al.[64]). A path satisfies the M -coverage
condition if every contiguous subsequence of M agents collectively observes all d features x1 , . . . , xd .
We aim to prove the following theorem.
Theorem 8.40 (Global Convergence Rate). Consider a DAG G containing a path of length D of
agents A1 , . . . , AD satisfying the M -coverage condition. Let p∗ be the global optimal logistic predictor
over all d features. Assume:
   1. Bounded second moments: E[x2l ] ≤ BX  2 for all l ∈ {1, . . . , d}.


   2. Bounded coefficients: for the optimal logits z ∗ (x) = l αl xl where ∥α∥1 ≤ Bp∗ .
                                                            P

Then the excess risk of the final agent pD is bounded by
                                                                             
                                            ∗         M                 M
                              L(pD ) − L(p ) ≤ Bp∗ BX √ = O             √         .
                                                       D                  D
We begin with the following lemma.
Lemma 8.41 (Orthogonality of Residuals). Let p∗ be the optimal logistic predictor on a feature
space X . The residual error (p∗ (x) − y) is orthogonal to the feature vector x in expectation:

                                           E [x(p∗ (x) − y)] = 0.

Proof. The gradient of the logistic output is ∇θ pθ (x) = pθ (x)(1 − pθ (x))x. So we get
                                                                  
                               y        1−y
          ∇θ L(θ) = −E              −             pθ (x)(1 − pθ (x))x = E [(pθ (x) − y)x] .
                             pθ (x) 1 − pθ (x)
The optimal parameters θ∗ must satisfy the condition ∇θ L(θ∗ ) = 0. Thus,

                                     ∇θ L(θ) = E [x(p∗ (x) − y)] = 0.

                                                    142
This orthogonality allows us to decompose the error of any suboptimal model. We will relate
the excess loss of a logistic predictor q by the optimal logistic predictor p, using the expected
Kullback-Leibler divergence of the Bernoulli distributions with parameters q(x) and p(x). We denote
this measure as D(p∥q) defined by

                       D(p∥q) = E [DKL (Bernoulli(p(x))∥Bernoulli(q(x))]
                                                                         
                                           p(x)                  1 − p(x)
                              = E p(x) log      + (1 − p(x)) log            .
                                           q(x)                  1 − q(x)

Lemma 8.42 (Decomposing Loss). Let p∗ be the optimal logistic predictor on a feature set S, and
let q be any logistic predictor in S. The loss decomposes as

                                        L(q) = L(p∗ ) + D(p∗ ∥q).

Proof. Using the identity log σ(z) = z − log(1 + ez ), we write the loss with z = θ⊤ x as

                                     L(θ) = −E [yz − log(1 + ez )] .

Expanding the difference L(θ) − L(θ∗ ), we obtain
                               h           ⊤               ∗ ⊤
                                                                                   i
             L(θ) − L(θ∗ ) = E log(1 + eθ x ) − log(1 + e(θ ) x ) − y((θ − θ∗ )⊤ x) .

Adding and subtracting p∗ (x)(θ − θ∗ )⊤ x inside the expectation yields
                                h           ⊤                ∗ ⊤
                                                                                       i
             L(θ) − L(θ∗ ) = E log(1 + eθ x ) − log(1 + e(θ ) x ) − p∗ (x)(θ − θ∗ )⊤ x
                                  h                         i
                             + E (p∗ (x) − y)((θ − θ∗ )⊤ x) .                                      (51)

The second term is zero due to the orthogonality condition derived in Lemma 8.41. For the first
term, we expand the definition of D(p∗ ∥q) with z = θ⊤ x and z ∗ = (θ∗ )⊤ x:
                             h                       ∗
                                                                      i
               D(p∗ ∥q) = E p∗ (z ∗ − z) − log(1 + ez ) + log(1 + ez )
                             h          ⊤                ∗ ⊤
                                                                                   i
                        = E log(1 + eθ x ) − log(1 + e(θ ) x ) − p∗ (x)(θ − θ∗ )⊤ x .

This matches the first term in Equation 51, completing the proof.

To relate the KL divergence to the parameter error, we employ the following bound, which is a
specific case of Pinsker’s inequality [81]. We include the proof for completeness.

Lemma 8.43. For the expected KL divergence D(p∥q), the following inequality holds:

                              D(p∥q) ≥ 2E (p(x) − q(x))2 .
                                                         


Proof. We verify the inequality pointwise for any x ∈ X . We aim to show

                                p(x)                  1 − p(x)
                     p(x) log        + (1 − p(x)) log          ≥ 2(p(x) − q(x))2 .                 (52)
                                q(x)                  1 − q(x)

Define the function f (p) = p log pq + (1 − p) log 1−p
                                                   1−q − 2(p − q) . The first derivative with respect to
                                                                 2

p is f ′ (p) = log pq − log 1−p
                            1−q − 4(p − q). The second derivative is f (p) = p + 1−p − 4 = p(1−p) − 4.
                                                                      ′′     1    1           1



                                                   143
For p ∈ [0, 1], the term p(1 − p) has a maximum value of 0.25. Consequently, p(1−p) 1
                                                                                          ≥ 4, which
implies f (p) ≥ 0. Since f is convex and satisfies f (q) = 0, the point p = q is a global minimum.
          ′′                                         ′

Observing that f (q) = 0, we conclude that f (p) ≥ 0 for all p. Taking the expectation of both sides
in (52) yields the result:
                                                                
                                  p(x)                  1 − p(x)
             D(p∥q) = E p(x) log       + (1 − p(x)) log            ≥ 2E[(p(x) − q(x))2 ].
                                  q(x)                  1 − q(x)
We define the pointwise loss function:

                                      l(z, y) = log(1 + ez ) − yz.

Thus, we can write L(p) = E[l(z(x), y)].
Lemma 8.44. Let g(x) = σ(zg (x)) be any logistic predictor. Let S be a subspace of features and
p(x) = σ(zp (x)) be the predictor that minimizes L(p) over S. Then, we have

                                    L(p) ≤ L(g) + |E[(p − y)zg ]|.                                 (53)

Proof. Let ϕ(z) = log(1 + ez ). The derivatives are ϕ′ (z) = σ(z) and ϕ′′ (z) = σ(z)(1 − σ(z)). Since
σ(z) ∈ (0, 1), we have ϕ′′ (z) ≥ 0, implying ϕ is convex. Convexity implies that for any u, v ∈ R,
ϕ(v) ≥ ϕ(u) + ϕ′ (u)(v − u). Rearranging implies the following:

                                      ϕ(u) ≤ ϕ(v) + σ(u)(u − v).                                   (54)

We define the relationship between the losses l(u, y) and l(v, y). Substituting l(z, y) = ϕ(z) − yz, we
assume the following inequality:

                                 l(u, y) ≤ l(v, y) + (σ(u) − y)(u − v).                            (55)

Expanding terms confirms this holds given the convexity of ϕ in Equation 54:

                           ϕ(u) − yu ≤ ϕ(v) − yv + σ(u)(u − v) − yu + yv
                           ⇐⇒ ϕ(u) ≤ ϕ(v) + σ(u)(u − v).

Now, for a point x, let u = zp (x) and v = zg (x). Applying Equation 55, we get

                              l(zp , y) ≤ l(zg , y) + (σ(zp ) − y)(zp − zg ).

Taking the expectation over x gives

              L(p) ≤ L(g) + E[(p − y)(zp − zg )] = L(g) + E[(p − y)zp ] − E[(p − y)zg ].

From Lemma 8.41 (Orthogonality), we know that for any feature xl in the support of p, E[xl (p−y)] = 0.
Since zp is a linear combination of such features, E[(p − y)zp ] = 0. Substituting this yields

                         L(p) ≤ L(g) − E[(p − y)zg ] ≤ L(g) + |E[(p − y)zg ]|.

We consider a path of agents A1 , . . . , AD . Each agent i receives the logit zi−1 from its predecessor
and trains a logistic predictor model using locally observed features xSi , zi−1 , and possibly some
other predecessors’ logits. Since one option for the agent Ai is to pass the logits zi−1 through, we
have that L(pi−1 ) ≥ L(pi ). We also get that Lemma 8.42 holds for pi−1 and pi , since pi−1 is in the
stricter subspace of pi .
We use the notation ∥f (x)∥2 = E [f (x)2 ] for any function f .
                                p


                                                   144
Lemma 8.45 (Residual Bound via Path Coverage). Let A1 , . . . , Ak be a pathPd of agents where every
feature xl is observed at least once. Let g(x) = σ(zg (x)) where zg (x) = l=1 αl xl be any logistic
predictor over the whole space. Assume the coefficients of zg satisfy dl=1 |αl | ≤ Bg , and the features
                                                                     P
satisfy E[x2l ] ≤ BX
                   2 , for some B and B . Let ε ≥ L(p ) − L(p ). Then, we have
                                 g       X               1        k
                                                             r
                                                               kε
                                    |E[(pk − y)zg ]| ≤ Bg BX       .
                                                                2

Proof. Let zg (x) = dl=1 αl xl . We bound the error term:
                      P

                                         " d                       #       d
                                          X                                X
                  |E[(pk − y)zg ]| = E            αl xl (pk − y)       ≤         |αl | |E[xl (pk − y)]|.
                                            l=1                            l=1

Consider a feature xl . Due to each feature being observed, this feature appears in the index set of
some agent Aj in the path. By orthogonality, E[xl (pj − y)] = 0. We decompose the expectation
using the triangle inequality:

                |E[xl (pk − y)]| ≤ |E[xl (pk − pj )]| + |E[xl (pj − y)]| = |E[xl (pk − pj )]|.

Applying the Cauchy-Schwarz inequality gives
                                      q       q
                  |E[xl (pk − pj )]| ≤ E[x2l ] E[(pk − pj )2 ] = ∥xl ∥2 ∥pk − pj ∥2 .

Given ∥xl ∥2 ≤ BX , we bound ∥pk − pj ∥2 using the loss difference ε. Applying Lemma 8.43, we get
for any s ∈ {1, . . . , k − 1}:
                                                     1
                                   E (ps − ps+1 )2 ≤ D(ps+1 ∥ps ).
                                     
                                                       2
By the triangle inequality and Cauchy-Schwarz,
                                                       s
                                 k−1
                                     r
                                                         k k−1
                                                          P                    r
                                 X     D(ps+1 ∥ps )        s=1 D(ps+1 ∥p s )     kε
                   ∥pj − pk ∥2 ≤                     ≤                       ≤      .
                                           2                    2                2
                                  s=j

Combining these bounds with the constraint on αl gives
                                            d                                              r
                                            X                                                  kε
                       |E[(pk − y)zg ]| ≤         |αl | · |E[xl (pk − y)]| ≤ Bg BX                .
                                                                                               2
                                            l=1

We are finally ready to prove Theoremp   8.40. Combining Lemma 8.44 and Lemma 8.45, we obtain
the relationship L(pk ) ≤ L(g) + Bg BX kε/2 for a path of length k. Extending this analysis over
the full path satisfying the M -coverage condition leads to our main convergence result.

Proof of Theorem 8.40. We partition the path into K = ⌊D/M ⌋ disjoint blocks of length M . By
the Pigeonhole Principle, since the total loss reduction is bounded by the loss of the first agent L(p1 ),
there exists at least one stable block k ∗ where the reduction is at most the total reduction divided
by K. Suppose this block k ∗ is on indices s, s + 1, . . . , t. Then, we have
                           t
                           X                               L(p1 )   2M L(p1 )
                                  (L(pi−1 ) − L(pi )) ≤           ≤           := ε.
                                                            K          D
                          i=s+1


                                                        145
Applying Lemma 8.44 and Lemma 8.45, we get that over this path L(pt ) ≤ L(p∗ ) + Bp∗ BX M ε/2.
                                                                                              p

Next, note that L(p1 ) ≤ log 2 since using θ1 = 0 achieves a loss of log 2, and because the first agent
optimizes within its domain then L(p1 ) ≤ log 2 < 1. Combined with the non-increasing losses, we get
                                                             M
                                    L(pD ) − L(p∗ ) ≤ Bp∗ BX √ .
                                                              D
Our theoretical analysis builds on the framework established by Kearns et al. [64] for linear regression.
We extend their methods to the classification setting. Unlike their work, which relies on the geometry
of Mean Squared Error (MSE), our analysis addresses the non-linearities of the sigmoid function
and Binary Cross Entropy (BCE) loss. This necessitates the use of information-theoretic tools to
bound the excess risk.
The proof strategy for Theorem 8.40 mirrors the methods of Kearns et al. [64]. Lemma 8.41
(Orthogonality) and Lemma 8.42 (Decomposition) establish the logistic equivalents of their linear
regression results. However, since the logistic loss does not admit a simple Euclidean decomposition,
we rely on KL-divergence and a Pinsker-type bound (Lemma 8.43) to relate the risk reduction to
parameter error.


9     Conclusion and Future Directions
The diverse array of case studies presented in this manuscript demonstrates unequivocally that
frontier AI models—specifically Gemini Deep Think and its advanced variants—have crossed a
critical threshold. They are no longer merely tools for routine automation, data processing, or syntax
formatting; they are now capable of acting as genuine, expert-level collaborators in mathematical
and algorithmic discovery. Across theoretical computer science, economics, physics, and optimization,
we have shown that LLMs can actively resolve open conjectures, tighten long-standing mathematical
bounds, and identify obscure, cross-disciplinary theorems to bypass human roadblocks.
The value of the AI in these collaborations manifested in several distinct paradigms. In some
instances, it acted as a cross-disciplinary bridge, retrieving theorems from distant mathematical
domains (such as the Kirszbraun Extension Theorem) to resolve computational geometry roadblocks.
In others, it served as a relentless adversarial reviewer, successfully identifying a fatal, deeply buried
flaw regarding perfect versus statistical consistency in a state-of-the-art cryptography preprint.
Crucially, however, these successes were not achieved autonomously. They required a tightly
coupled human-AI workflow characterized by iterative refinement, strategic scaffolding, and rigorous
verification—a process some authors have colloquially termed “vibe-proving.”

9.1    Common Themes and Problem Suitability
Across these diverse case studies, clear themes emerge regarding the types of problems where this
human-AI collaborative approach excels, and where it currently struggles.

Highly Suited Problem Classes: The model is exceptionally effective on problems that
can be decomposed into verifiable steps, require cross-disciplinary knowledge retrieval (e.g., bridging
graph theory with continuous measure theory), or involve generating counterexamples to bounded
conjectures. It also thrives in settings where the human can provide a strategic “scaffold” while
the AI fills in tactical derivations, or where automated execution loops can rapidly test and prune
algebraic hypotheses against numerical ground-truths (as in the cosmic strings derivation).

Less Suited Problem Classes: One goal is to improve the model on problems requiring

                                                  146
completely unconstrained, multi-page derivations, where intermediate steps cannot be easily verified
or grounded. Problems that require establishing entirely novel mathematical frameworks from
scratch, or those with extremely long, sparse reward horizons without intermediate feedback, exceed
the autonomous capabilities of current models and require some amount of human orchestration.

Capabilities Needed for Expansion: To further expand the range of scientific prob-
lems that can be tackled, future AI capabilities likely should evolve beyond natural language and
standard code execution. Models will need enhanced capacities for long-horizon logical planning to
maintain context over lengthy proofs. Furthermore, seamless, native integration with interactive
theorem provers (discussed in Section 9.3) are important to autonomously verify the logical
soundness of deep reasoning steps and mitigate hallucination bottlenecks.

9.2   Understanding Current Limitations and Failure Modes
Left unchecked, current models exhibit distinct failure modes that researchers must actively manage.
Across our experiments, several recurring limitations emerged:

   • Confirmation Bias: As noted in the information theory case studies (Section 8.1), models
     exhibit a strong tendency to support the hypothesis presented in a prompt. If tasked with
     proving a false conjecture, the AI will often attempt to bridge logical gaps with confident
     but “hand-wavy” arguments that do not withstand rigorous scrutiny. Neutral prompting (e.g.,
     “prove or refute”) is essential.

   • Confident Technical Hallucinations: While models excel at high-level structural insights,
     they can occasionally make subtle algebraic errors, drop constraints, or confidently misapply
     theorems (e.g., flipping inequality signs in hypercontractivity bounds).

   • Alignment Friction: Standard safety and alignment guardrails can sometimes hinder scientific
     exploration. As noted in Section 2, the model may initially refuse to attempt a problem if it
     recognizes it as an “unsolved open problem” (requiring Context De-Identification to bypass).

Because of these limitations, the human researcher’s role is elevated rather than replaced. The
scientist shifts from executing mechanical derivations to acting as an orchestrator, auditor, and
strategic director of the AI’s combinatorial reasoning.

9.3   Future Directions: From Code Execution to Formal Verification
To overcome the limitations of LLM hallucinations, researchers must integrate pure language models
with external verification environments. As outlined in Section 2.6 and demonstrated in our cosmic
strings experiments (Section 6.4), we are already seeing success by embedding AI in “neuro-symbolic”
loops—where the model autonomously writes code to numerically verify its proposed mathematical
steps and uses traceback errors to prune invalid branches.
However, while numerical execution is a powerful grounding mechanism for applied mathematics and
physics, it is fundamentally limited when dealing with abstract proofs. For pure mathematics and
theoretical computer science, the natural evolution of this workflow is Formal Verification. As AI
systems generate increasingly complex, multi-page mathematical proofs, human verification becomes
an exhausting bottleneck. Future research must focus on building autoformalization pipelines that
automatically translate LLM-generated informal mathematics into formal verification languages (such
as Lean, Coq, or Isabelle). By pairing the creative, associative leaps of an LLM with the absolute


                                                147
rigorous certainty of an interactive theorem prover, the research community can systematically
eliminate the hallucination problem in mathematical discovery.

9.4   The Shifting Bottleneck: An Impending Crisis in Peer Review
As AI drastically lowers the friction of generating highly technical, mathematically dense research
papers—evidenced by the AI-integrated IDE workflow utilized in Section 5 — the scientific community
faces an impending systemic challenge. If researchers can “vibe-code” comprehensive papers in a
fraction of the traditional time, the fundamental bottleneck of science will shift entirely from the
generation of ideas to the verification of those ideas.
The traditional human peer-review system is already strained and fundamentally unequipped to
handle a massive influx of AI-accelerated literature. Consequently, the very same tools used to
generate these papers must be adapted to evaluate them. The cryptography case study (Section 3.2)
proves that AI models, when guided by rigorous, adversarial self-correction protocols, are already
capable of finding subtle flaws in advanced proofs. Developing robust, AI-assisted peer-review
systems will be vital to triaging submissions and maintaining the integrity of the scientific literature
in the coming years.

9.5   Final Thoughts
Just as the advent of calculators and computational algebra systems revolutionized applied math-
ematics in previous decades, the ability to rapidly iterate on abstract reasoning with a tireless,
knowledgeable AI collaborator promises to dramatically reduce the friction of theoretical execution.
Ultimately, the premise of this work is not just that AI can help solve specific, isolated research
problems, but that it transforms how we do research. The implications for scientists are important:
the day-to-day workflow of theoretical research will likely shift away from mechanical derivations and
exhaustive literature hunting, moving instead toward high-level orchestration, hypothesis generation,
and rigorous verification. By acting as a collaborative sounding board, AI lowers the barrier to entry
for exploring complex, interdisciplinary ideas. This shift promises to empower a broader diversity of
researchers, allowing them to tackle bigger, more ambitious problems than they could alone. By
embracing this collaborative paradigm, understanding its failure modes, and building new automated
verification pipelines, researchers can explore broader hypothesis spaces and ultimately accelerate
the pace of scientific discovery.


Acknowledgments
The authors thank the Gemini team for access to early models and technical support. We also
thank the support of Corinna Cortes, Jeff Dean, Demis Hassabis, and Koray Kavukcuoglu. We
also acknowledge members of the Deep Think team that are not authors: Garrett Bingham, Irene
Cai, Heng-Tze Cheng, Yong Cheng, Kristen Chiafullo, Paul Covington, Golnaz Ghiasi, Chenjie Gu,
Huan Gui, Ana Hosseini, Dawsen Hwang, Vihan Jain, Ragha Kotikalapudi, Chenkai Kuang, Maciej
Kula, Nate Kushman, Jane Labanowski, Quoc Le, Jonathan Lee, Zhaoqi Leng, Steve Li, YaGuang
Li, Hanzhao (Maggie) Lin, Evan Liu, Yuan Liu, Thang Luong, Pol Moreno, Nigamaa Nayakanti,
Aroonalok Pyne, Shubha Raghvendra, Sashank Reddi, Nikunj Saunshi, Siamak Shakeri, Archit
Sharma, Xinying Song, Qijun Tan, Yi Tay, Trieu Trinh, Theophane Weber, Winnie Xu, Zicheng Xu,
Shunyu Yao, Lijun Yu, Hao Zhou, and Honglei Zhuang.




                                                  148
References
 [1] Anantharam, V., Bogdanov, A., Chakrabarti, A., Jayram, T. S., and Nair, C. (2017). A
     conjecture regarding optimality of the dictator function under Hellinger distance. In Information
     Theory and Applications Workshop.

 [2] Anari, N., and Rezaei, A., A tight analysis of Bethe approximation for permanent. SIAM
     Journal on Computing 54 (4), 81–101

 [3] Arora, Sanjeev. Polynomial time approximation schemes for Euclidean traveling salesman and
     other geometric problems. Journal of the ACM, 45(5):753–782, 1998.

 [4] Arora, Sanjeev and Karger, David and Karpinski, Marek. Polynomial time approximation
     schemes for dense instances of NP-hard problems. Proceedings of the twenty-seventh annual
     ACM symposium on Theory of computing, pages 284–293, 1995.

 [5] Avidor, Adi and Zwick, Uri. Rounding two and three dimensional solutions of the SDP relax-
     ation of MAX CUT. International Workshop on Approximation Algorithms for Combinatorial
     Optimization, pages 14–25, 2005.

 [6] Aygün, Eser et al. An AI system to help scientists write expert-level empirical software. arXiv
     preprint arXiv:2509.06503, 2025.

 [7] Bakshi, A., Indyk, P., Jayaram, R., Silwal, S., Waingarten, E. (2023). A near-linear time
     algorithm for the chamfer distance. NeurIPS 2023.

 [8] Bansal, Nikhil and Cohen-Addad, Vincent and Prabhu, Milind and Saulpic, David and
     Schwiegelshohn, Chris Sensitivity Sampling for k-Means: Worst Case and Stability Opti-
     mal Coreset Bounds. Proceedings of the 65th IEEE Annual Symposium on Foundations of
     Computer Science (FOCS 2024), pages 1707–1723, 2024.

 [9] Barak, Boaz and Raghavendra, Prasad and Steurer, David. Rounding semidefinite programming
     hierarchies via global correlation. 2011 ieee 52nd annual symposium on foundations of computer
     science, pages 472–481, 2011.

[10] Barnes, L. P., and Özgür, A. (2020, June). The Courtade-Kumar most informative Boolean
     function conjecture and a symmetrized Li-Médard conjecture are equivalent. IEEE International
     Symposium on Information Theory (ISIT), 2205-2209.

[11] Bottcher, Julia and Pruessmann, Klaas P. and Taraz, Anusch and Würfl, Andreas. Bandwidth,
     expansion, treewidth, separators and universality for bounded-degree graphs. European Journal
     of Combinatorics, 31(5):1217–1227, 2010.

[12] Brânzei, Simina and Li, Jiawei. The Query Complexity of Local Search and Brouwer in Rounds.
     COLT, 2022. In Mathematical Statistics and Learning, forthcoming.

[13] Simina Brânzei, Ioannis Panageas, and Dimitris Paparas. The Query Complexity of Local
     Search in Rounds on General Graphs. arXiv:2601.13266 [cs.CC], 2026. https://arxiv.org/
     abs/2601.13266.

[14] M. P. Brenner, V. Cohen-Addad, and D. Woodruff, “Solving an Open Problem in Theoretical
     Physics using AI-Assisted Discovery,” 2026, arXiv:2603.04735 [cs.AI]. https://arxiv.org/abs/
     2603.04735

                                                 149
[15] Briet, Jop and de Oliveira Filho, Fernando Mário and Vallentin, Frank. The positive semidefinite
     Grothendieck problem with rank constraint. International Colloquium on Automata, Languages,
     and Programming, pages 31–42, 2010.

[16] Briet, Jop and de Oliveira Filho, Fernando Mário and Vallentin, Frank. Grothendieck Inequalities
     for Semidefinite Programs with Rank Constraint. Theory of Computing, 10(1):77–105, 2014.

[17] Bubeck, Sébastien and Coester, Christian and Eldan, Ronen and Gowers, Timothy and Lee,
     Yin Tat and Lupsasca, Alexandru and Sawhney, Mehtaab and Scherrer, Robert and Sellke,
     Mark and Spears, Brian K et al. Early science acceleration experiments with GPT-5. arXiv
     preprint arXiv:2511.16072, 2025.

[18] Cai, J.-Y. S2P ⊆ ZPPNP . Journal of Computer and System Sciences, 73(1):25–35, 2007.

[19] Canetti, R. More on BPP and the polynomial-time hierarchy. Information Processing Letters,
     57(5):237–241, 1996.

[20] Chandar, Venkat and Tchamkerten, Aslan. Most informative quantization functions. Proc. ITA
     Workshop, San Diego, CA, USA, 2014.

[21] Chang, Chun-Hao and Rampasek, Ladislav and Goldenberg, Anna. Dropout feature ranking
     for deep learning models. arXiv preprint arXiv:1712.08645, 2017.

[22] F. Chierichetti, M. Giacchini, R. Kumar, S. Lattanzi, A. Panconesi, E. Tani, A. Tomkins.
     Beyond the Full Slate: Evaluating MNL Algorithms on All Slates. Private Communication.

[23] M. B. Cohen, C. Musco, and C. Musco, Input sparsity time low-rank approximation via ridge
     leverage score sampling, Proceedings of the Twenty-Eighth Annual ACM-SIAM Symposium on
     Discrete Algorithms (SODA), pp. 1758–1777, 2017.

[24] Cohen-Addad, V. and Woodruff, David P. Google Research Blog post, 2025. https:
     //research.google/blog/gemini-provides-automated-feedback-for-theoretical-
     computer-scientists-at-stoc-2026/

[25] Courtade, T. A., Kumar, G. R. (2014). Which Boolean functions maximize mutual information
     on noisy inputs? IEEE Transactions on Information Theory, 60(8), 4515–4525.

[26] P. Csikvári. Lower matching conjecture, and a new proof of Schrijver’s and Gurvits’s theorems.
     Journal of the European Mathematical Society (EMS Publishing) 19 (6), 2017.

[27] Csirmaz, L., Ligeti, P., Tardos, G. (2015). Erdős-Pyber theorem for hypergraphs and secret
     sharing. Graphs Combin., 31(5):1335–1346.

[28] Cygan, M. and Fomin, F. V. and Kowalik, L. and Lokshtanov, D. and Marx, D. and Pilipczuk,
     M. and Pilipczuk, M. and Saurabh, S. Parameterized Algorithms. Springer, 2015.

[29] Gerard Debreu. “Representation of a Preference Ordering by a Numerical Function”. Decision
     processes 3 (1954): 159-165.

[30] Du, Ding-Zhu and Smith, Warren D. Disproofs of Generalized Gilbert Pollak Conjecture on
     the Steiner Ratio in Three or More Dimensions. Journal of Combinatorial Theory, Series A,
     74(1):115–130, 1996.



                                                150
[31] Duede, E. Tail Novelty, Knowledge Collapse, and Useful Frictions in Science. Computer Science
     Seminar, Illinois Institute of Technology, November 17, 2025. https://bit.ly/iit-cs-seminar-duede

[32] Paul Dütting, Vahab Mirrokni, Renato Paes Leme, Haifeng Xu, and Song Zuo. “Mechanism
     Design for Large Language Models”. In Proceedings of the ACM Web Conference 2024 (pp.
     144-155).

[33] G.P. Egorychev. Proof of the van der Waerden conjecture for permanents [in Russian]. Sibirskii
     Matematicheskii Zhurnal, 22:6, 65–71, 1981.

[34] D.I. Falikman. Proof of the van der Waerden conjecture regarding the permanent of a doubly
     stochastic matrix [in Russian]. Matematicheskie Zametki, 29:931–938, 1981.

[35] Fand, M. (2021). Fast Johnson-Lindenstrauss Transform. arXiv preprint arXiv:2104.05695.

[36] Feige, Uriel and Karpinski, Marek and Langberg, Michael. Improved approximation of Max-Cut
     on graphs of bounded degree. Journal of Algorithms, 43(2):201–219, 2002.

[37] T. Feng, T. Trinh, G. Bingham, J. Kang, S. Zhang, et al., Semi-Autonomous Mathematics
     Discovery with Gemini: A Case Study on the Erdős Problems, arXiv preprint arXiv:2601.22401
     (2026). Available at: https://arxiv.org/abs/2601.22401.

[38] T. Feng, T. H. Trinh, G. Bingham, D. Hwang, Y. Chervonyi, et al., Towards
     Autonomous Mathematics Research, arXiv preprint arXiv:2408.00000 (2026). Avail-
     able at: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/towards-
     autonomous-mathematics-research/Towards_Autonomous_Mathematics_Research.pdf

[39] Feng, Y., Indyk, P. (2025). Even Faster Algorithm for the Chamfer Distance. ICALP 2025.

[40] Feng, Y., Woodruff, David P. (2026). Fast Approximate Lp Chamfer Distance via Lopsided
     Embeddings and Structured JL. In submission 2026.

[41] Fleischmann, H., Gamboa Quintero, G., Karthik C. S., Matějka, J., Petr, J. (2025). On Steiner
     Trees of the regular simplex. Journal of Computational Geometry, 16(1), 1–34.

[42] Fleischmann, Henry and Gavva, Surya Teja and Karthik C. S.. On Approximability of Steiner
     Tree in ℓp -metrics. TheoretiCS, 4, 2025.

[43] Fortnow, L. Search versus Decision for S2P . arXiv preprint arXiv:2512.02808, 2025. https:
     //arxiv.org/abs/2512.02808

[44] L. Fortnow. fortnow/s2psearch: Files related to vibe-coding the “Search vs Decision for S2P”
     paper. GitHub repository, 2025. https://github.com/fortnow/s2psearch

[45] Yao Fu, et al. Tree of Thoughts: Deliberate Problem Solving with Large Language Models.
     arXiv preprint arXiv:2305.10601, 2023.

[46] Ganor, Anat and Karthik C. S. and Pálvölgyi, Dömötör. On Communication Complexity of
     Fixed Point Computation. ACM Trans. Economics and Comput., 9(4):25:1–25:27, 2021.

[47] Paritosh Garg, Sagar Kale, Lars Rohwedder, and Ola Svensson. Robust Algorithms Under
     Adversarial Injections. Proceedings of the 47th International Colloquium on Automata, Languages,
     and Programming (ICALP), 2020, pages 56:1–56:15.


                                                 151
[48] Gemini Deep Think. https://blog.google/products/gemini/gemini-2-5-deep-think/.

[49] B. Georgiev, J. Gómez-Serrano, T. Tao, and A. Z. Wagner, Mathematical exploration and
     discovery at scale, arXiv preprint arXiv:2511.02864, 2025.

[50] Ghashami, M., Liberty, E., Phillips, J. M., Woodruff, D. P. (2016). Frequent directions: Simple
     and deterministic matrix sketching. SIAM Journal on Computing, 45(5), 1762–1792.

[51] Gilbert, Edgar N. and Pollak, Henry O. Steiner Minimal Trees. SIAM Journal on Applied
     Mathematics, 16(1):1–29, 1968.

[52] Goemans, Michel X and Williamson, David P. Improved approximation algorithms for maximum
     cut and satisfiability problems using semidefinite programming. Journal of the ACM (JACM),
     42(6):1115–1145, 1995.

[53] Ziyi Guan and Eylon Yogev. SNARGs for NP from LWE. Cryptology ePrint Archive, Paper
     2025/2328, 2025.

[54] L. Gurvits. Van der Waerden/Schrijver-Valiant like conjectures and stable (aka hyperbolic)
     homogeneous polynomials: one theorem for all. Electron. J. Combin., 15(1), Research Paper 66,
     2008.

[55] L. Gurvits. Unleashing the power of Schrijver’s permanental inequality with the help of the
     Bethe Approximation. ArXiv preprint 1106.2844v11, 2011.

[56] L. Gurvits. Boolean matrices with prescribed row/column sums and stable homogeneous
     polynomials: Combinatorial and algorithmic applications. Inf. Comput. 240 42-55 (2015)

[57] L. Gurvits, A. Samorodnitsky: Bounds on the Permanent and Some Applications. FOCS 2014:
     90-99

[58] Harvey, Nicholas J. A. and Nelson, Jelani and Onak, Krzysztof. Sketching and streaming
     entropy via approximation theory. FOCS 2008, 489–498.

[59] Hsieh, Jun Ting and Kothari, Pravesh K. Approximating Max-Cut on Bounded Degree Graphs:
     Tighter Analysis of the FKL Algorithm. 50th International Colloquium on Automata, Languages,
     and Programming, ICALP 2023, page 77, 2023.

[60] In, Chansophea Wathanak and Li, Yi and Woodruff, David and Wu, Xuan. Robust Sparsification
     via Sensitivity. Proceedings of ICML 2025, pages 26446–26463, 2025.

[61] Ivanov, Alexander O. and Tuzhilin, Alexey A. The Steiner Ratio Gilbert Pollak Conjecture Is
     Still Open: Clarification Statement. Algorithmica, 62(1-2):630–632, 2012.

[62] Javanmard, A., and Woodruff, D. P. (2026). Progress on the Courtade-Kumar Conjecture:
     Optimal High-Noise Entropy Bounds and Generalized Coordinate-wise Mutual Information.
     arXiv preprint arXiv:2601.09679.

[63] Jayaram, R., Woodruff, D. P., Zhou, S. (2024). Streaming Algorithms with Few State Changes.
     Proc. ACM Manag. Data, 2(2), 82.

[64] M. Kearns, A. Roth, and E. Ryu. Networked information aggregation via machine learning.
     Proceedings of the Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 2026,
     4799–4845.

                                                152
[65] H. Kesten. Symmetric random walks on groups, Trans. Am. Math. Soc. 92 (1959), 336–354.

[66] Khot, Subhash and Kindler, Guy and Mossel, Elchanan and O’Donnell, Ryan. Optimal
     inapproximability results for MAX-CUT and other 2-variable CSPs? SIAM Journal on
     Computing, 37(1):319–357, 2007.

[67] Kirszbraun, M. "Uber die zusammenziehende und Lipschitzsche Transformationen. Fundamenta
     Mathematicae, 22(1):77–108, 1934.

[68] Korula, N., Mirrokni, V., Zadimoghaddam, M. (2015). Online submodular welfare maximization:
     Greedy beats 1/2 in random order. STOC 2015.

[69] Krapivin, A., Przybocki, B., Sanhueza-Matamala, N., Subercaseaux, B. (2025). Optimal and
     efficient partite decompositions of hypergraphs. arXiv preprint arXiv:2511.11855.

[70] Li, J., and Médard, M. (2020). Boolean functions: noise stability, non-interactive correlation
     distillation, and mutual information. IEEE Transactions on Information Theory, 67(2), 778-789.

[71] L. Lovász, M. Plummer. Matching Theory. AMS Chelsea Publishing Series, 2009.

[72] A. W. Marcus, D. A. Spielman and N. Srivastava, Interlacing families I: Bipartite Ramanujan
     graphs of all degrees, Annals of Mathematics 182 (2015), 307–325.

[73] A. W. Marcus, D. A. Spielman and N. Srivastava, Interlacing families II: Mixed characteristic
     polynomials and the Kadison—Singer problem, Annals of Mathematics 182 (2015), 327–350.

[74] Thang Luong and Edward Lockhart. Advanced version of Gemini with Deep Think officially
     achieves gold-medal standard at the International Mathematical Olympiad. Google DeepMind
     Blog, July 21, 2025.

[75] B. D. McKay. The expected eigenvalue distribution of a large regular graph, Linear Algebra
     Appl. 40 (1981), 203–216.

[76] Mitchell, Joseph S. B. Guillotine Subdivisions Approximate Polygonal Subdivisions: A Simple
     Polynomial-Time Approximation Scheme for Geometric TSP, k-MST, and Related Problems.
     SIAM Journal on Computing, 28(4):1298–1309, 1999.

[77] Nagda, Ansh and Raghavan, Prabhakar and Thakurta, Abhradeep. Reinforced Generation of
     Combinatorial Structures: Hardness of Approximation. arXiv preprint arXiv:2509.18057, 2025.

[78] A. Nilli. On the second eigenvalue of a graph, Discrete Mathematics, 91 (1991), 207–210.

[79] Novikov, Alexander, Vũ, Ngân and Eisenberger, Marvin and Dupont, Emilien and Huang,
     Po-Sen and Wagner, Adam Zsolt and Shirobokov, Sergey and Kozlovskii, Borislav and Ruiz,
     Francisco JR and Mehrabian, Abbas et al. AlphaEvolve: A coding agent for scientific and
     algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.

[80] Ordentlich, Or and Shayevitz, Ofer and Weinstein, Omri. An improved upper bound for the most
     informative Boolean function conjecture. 2016 IEEE International Symposium on Information
     Theory (ISIT), pages 500–504, 2016.

[81] M. S. Pinsker. Information and Information Stability of Random Variables and Processes.
     Holden–Day, 1964.


                                               153
[82] Raghavendra, Prasad. Optimal algorithms and inapproximability results for every CSP?
     Proceedings of the fortieth annual ACM symposium on Theory of computing, pages 245–254,
     2008.

[83] Russell, A. and Sundaram, R. Symmetric alternation captures BPP. Computational Complexity,
     7(2):152–162, 1998.

[84] Samorodnitsky, A. (2016). On the entropy of a noisy function. IEEE Transactions on Information
     Theory, 62(10), 5446-5464.

[85] Santha, Miklos and Szegedy, Mario. Quantum and classical query complexities of local search
     are polynomially related. Proceedings of the thirty-sixth annual ACM symposium on Theory of
     computing, pages 494–501, 2004.

[86] David Schmeidler. “A Condition for the Completeness of Partial Preference Relations”. In:
     Econometrica: Journal of the Econometric Society (1971), pp. 403–404.

[87] A. Schrijver. Counting 1-Factors in Regular Bipartite Graphs. Journal of Combinatorial Theory,
     Series B, 72:122–135, 1998.

[88] A. Schrijver, W.G. Valiant. On lower bounds for permanents. Indagationes Mathematicae,
     42:425–427, 1980.

[89] Schwartz, Jacob T. Nonlinear Functional Analysis. Gordon and Breach Science Publishers,
     New York, 1969.

[90] M. Sellke and S. Yin, On Learning-Curve Monotonicity for Maximum Likelihood Estimators,
     arXiv preprint arXiv:2512.10220, 2025.

[91] Smith, Warren D. How to find Steiner minimal trees in Euclidean d-space. Algorithmica,
     7:137–177, 1992.

[92] N. Sothanaphan, Resolution of Erdős Problem #728: a writeup of Aristotle’s Lean proof, arXiv
     preprint arXiv:2601.07421, 2026.

[93] Trevisan, Luca. When Hamming Meets Euclid: The Approximability of Geometric TSP and
     Steiner Tree. SIAM J. Comput., 30(2):475–485, 2000.

[94] Valentine, F. A. A Lipschitz condition preserving extension for a vector function. American
     Journal of Mathematics, 67:83–93, 1945.

[95] L. Valiant. The complexity of computing the permanent. Theoretical Computer Science,
     8(2):189–201, 1979.

[96] P. O. Vontobel. “The Bethe Permanent of a Non-Negative Matrix,” IEEE Transactions on
     Information Theory, vol. 59, no. 3, pp. 1866-1901, 2013. (Also arXiv:1107.4196).

[97] M. Voorhoeve. A lower bound for the permanents of certain (0, 1)-matrices. Nederl. Akad.
     Wetensch. Indag. Math., 41(1):83–86, 1979.

[98] Woodruff, David P. and Zhou, Samson. Consistent Low-Rank Approximation. The Fourteenth
     International Conference on Learning Representations (ICLR) 2026.



                                               154
