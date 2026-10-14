                                             math-PVS: A Large Language Model Framework to
                                                Map Scientific Publications to PVS Theories


                                                           Hassen Saidi                                   Susmit Jha
                                                     Computer Science Laboratory                   Computer Science Laboratory
                                                         SRI International,                            SRI International,
                                                       Menlo Park, CA 94025                          Menlo Park, CA 94025
arXiv:2310.17064v1 [cs.AI] 25 Oct 2023




                                                      hassen.saidi@sri.com                           susmit.jha@sri.com

                                                                                    Tuhin Sahai
                                                                             Applied Sciences Laboratory
                                                                                  SRI International
                                                                               Menlo Park, CA 94025.
                                                                              tuhin.sahai@sri.com



                                                                                      Abstract

                                                  As artificial intelligence (AI) gains greater adoption in a wide variety of applica-
                                                  tions, it has immense potential to contribute to mathematical discovery, by guiding
                                                  conjecture generation, constructing counterexamples, assisting in formalizing math-
                                                  ematics, and discovering connections between different mathematical areas, to
                                                  name a few. While prior work has leveraged computers for exhaustive mathemat-
                                                  ical proof search, recent efforts based on large language models (LLMs) aspire
                                                  to position computing platforms as co-contributors in the mathematical research
                                                  process. Despite their current limitations in logic and mathematical tasks, there is
                                                  growing interest in melding theorem proving systems with foundation models. This
                                                  work investigates the applicability of LLMs in formalizing advanced mathematical
                                                  concepts and proposes a framework that can critically review and check mathemati-
                                                  cal reasoning in research papers. Given the noted reasoning shortcomings of LLMs,
                                                  our approach synergizes the capabilities of proof assistants, specifically PVS, with
                                                  LLMs, enabling a bridge between textual descriptions in academic papers and
                                                  formal specifications in PVS. By harnessing the PVS environment, coupled with
                                                  data ingestion and conversion mechanisms, we envision an automated process,
                                                  called math-PVS, to extract and formalize mathematical theorems from research
                                                  papers, offering an innovative tool for academic review and discovery.


                                         1    Introduction

                                         The growth (both in model size and size of training datasets) of transformer-based foundation
                                         models is quickly revolutionizing a large number of applications such as natural language processing,
                                         image generation and modification, and multi-modal inference. Recently, the National Academy of
                                         Sciences, Engineering, and Medicine released a workshop report [1] that emphasizes the importance
                                         of constructing and deploying AI agents that aid in mathematical endeavors. The advances in machine
                                         learning (ML) and AI methods has already aided in generating theorems for outstanding conjectures
                                         and discovering new connections between disparate concepts [2].
                                         Note that using computers to assist in generating proofs does have historical precedence. Examples
                                         include the four color theorem [3] and the proof of the existence of a chaotic attractor in the Lorenz
                                         system using interval arithmetic [4]. These efforts used computers to exhaustively search a large
Figure 1: Overall workflow called math-PVS for data generation from scientific publications, LLM-
based PVS code generation, and interactive theorem proving.


(combinatorial) search space and demonstrate the robustness of chaotic attractors respectively. Recent
efforts, however, aim to elevate the use of computing platforms to that of an assistant or a peer-
participant in the creative process of mathematical research. Given that large language models
(LLMs) do not directly perform well on problems in logic and mathematics [5], there are multiple
efforts to integrate theorem proving systems with foundation models, see [1, 6, 7] and references
therein.
The majority of these efforts are focused on formalization of mathematics from the ground up,
wherein the LLM proof assistants are customized to prove theorems in particular domains. A number
of these efforts use datasets such as MATH, GSM8K, and datasets in [8, 9, 10] that are limited to
high school grade mathematics and mathematics Olympiad questions. Our goal is to explore the use
of LLMs on formalizing mathematics used at the frontier of research, and to examine the possibility
of developing an LLM-based research assistant that can review mathematical reasoning in a research
paper. It is widely accepted that LLMs lack even basic reasoning capability and fail at even spatial
reasoning [11]. Consequently, we posit that any serious AI mathematics research assistant capable
of reviewing research papers and assisting in proving theorems needs to be a combination of proof
assistants such as prototype verification system (PVS) [12] and LLMs that can interface between the
textual description in research papers and the formal specification in PVS.
PVS [12] is a mechanized environment for formal specification and verification and consists of a
specification language based on classical, typed higher-order logic, a large number of predefined
theories, a type checker, and an interactive theorem prover. PVS type system supports sub-typing
and dependent types. Moreover, the PVS prelude offers foundational theories. NasaLib [13] is a
large collection of PVS libraries maintained by NASA. Currently, NasaLib consists of 63 top-level
libraries, containing about 38K proven formulas in total. They encode basic mathematical theories
such as topology, graph theory, group theory, and probability theory to name a few, as well as useful
theories for reasoning about critical systems.
Our framework (see Fig. 1) is able ingest the vast amounts of scientific literature in the form of PDF
files. The ingested data is directly converted to PVS code by a LLM as follows: (a) we generate
the mathematical data by processing a large corpus of scientific mathematical publications using
Facebook’s Nougat [14] framework to convert the information from PDF to LATEXformat, (b) the
LATEXcode is converted to PVS theories using LLMs, and (c) the user interacts with the LLM and
PVS systems and iterates with them to refine the theories and proofs with the aim of discovering new
proofs, define conjectures, check existing proofs, and uncover hidden connections between disparate
works. This integration of the PVS with LLMs opens up the possibility of automatically extracting
PVS formalization of mathematical theorems and proofs in existing research papers into PVS which
can be useful paper reviews and the aforementioned tasks.


2   A Prompting Framework for Generating PVS Theories

We demonstrate our framework by reproducing the core arguments for a proposition and its associated
proof from an existing paper [15] that relates the evolution of Turing machines to symbolic dynamics.
Note that symbolic dynamics are a standard tool in study of temporally evolving nonlinear systems.
Additionally, the authors develop a generalized definition of computational universality that extends


                                                  2
beyond Turing machines, counter machines, and tag systems. This work generalizes the notion
of computational universality to cellular automata and subshifts. The authors define an effective
symbolic space (ESS) and exploit it as described below.
Definition 1. An effective symbolic space is a pair (X, P ), where X is a symbolic space and
P : N → 2X is an injective function whose range is the set of all clopen sets of X, such that
the intersection and complementation of clopen sets are computable operations. This means that
there exist computable functions f : N → N and g : N × N → N such that X \ Pn = Pf (n) and
Pn ∩ Pm = Pg(n,m) .
They show that cellular automata and Turing machines (ignoring the blank symbol) are examples of
effective symbolic systems and then go on to prove universality theorems using this construct.
We ingest the above paper (in PDF format) using the Nougat software [14] and feed the resulting
LATEXcode to OpenAI’s GPT-4 for automatic generation of PVS theories. In particular, we used the
definition of effective symbolic spaces above along with the following definition to prove a simplified
version of the first proposition in [15] (presented below for completeness).
Definition 2. Let (X, P ) and (Y, Q) be two effective symbolic spaces. An effective continuous
map is a continuous map h : X → Y such that h−1 (Qn ) = Pk(n) , for some computable map
k : N → N. If h is bijective then it is an effective homeomorphism, and (X, P ) is said to be
effectively homeomorphic to (Y, Q).
Theorem 1. Every effective symbolic space is effectively homeomorphic to an effective subset of
the Cantor space. Every perfect effective symbolic space is effectively homeomorphic to the Cantor
space.
We note that we use definitions of Cantor spaces [16], homeomorphisms [17], and other mathematical
terminology from publicly available lectures notes and Wikipedia/Scholarpedia articles. In the case
that these documents are available in PDF format, we again use the Nougat software to convert key
portions to LATEXformat that is then converted to PVS theories using GPT-4.
We note that, as shown in Fig. 1, both the transformer-based PVS theory generation and its use in
PVS presently requires human intervention. The user was also involved in simplifying the theories
for PVS parsing, typechecking, and applying the grind tactic, a catch-all strategy that is frequently
used to automatically complete a proof in PVS. Moreover, we note that these interactions were very
similar to those that one may have with collaborators or advanced student researchers.

3   Using LLM for Abstraction
The human input required for our math-PVS framework as illustrated in Figure 1 is to use LLMs to
simplify and construct abstractions of the original input that capture the underlying core concepts.
Similar to the formalization of a complex system or algorithm in a theorem prover, the abstraction step
is required here to map mathematical concepts described in the paper of interest, to concepts grounded
in basic mathematical constructs such as set theory. While the formalization of the original input
in PVS can be automated using LLMs, the resulting PVS theorems might require extensive proof
details and background mathematical knowledge that are typically omitted in most mathematical
papers. By using LLMs to automatically generate abstractions of the input, the resulting concepts can
be mapped directly to PVS theories and subsequently proved by theorem proving techniques without
the need for ingestion and processing of copious amounts of background mathematical knowledge
and theories. As the corpus of mathematical knowledge grows in math-PVS, we expect this need for
abstraction to reduce.




Figure 2: Prompting ChatGPT4 to provide abstraction of the original mathematical definitions and
theorem

Figure 2 illustrates the prompt used to abstract the mathematical definitions extracted from the
paper [15]. The prompt explicitly requests the LLM to generate an abstraction that captures the main


                                                  3
concepts without the inclusion of specific details, thereby enabling the foundation model to generate
a self-contained and consistent PVS code.

4   Evaluation
We now describe how our approach can be applied to review the paper [15] described in the previous
section. The first step in our process is to use Meta’s Nougat [14] to generate TEXfrom the original
PDF file. Nougat is a Visual Transformer model that performs an Optical Character Recognition
(OCR) task for processing scientific documents into a markup language such as LATEX. This makes
the mathematical knowledge accessible and enables us to use LLMs for autoformalization into PVS.




 Figure 3: Prompting ChatGPT4 with a bijective mapping definition, and the resulting PVS theory

The next step is to extract and summarize the definitions and theorems from the recovered Latex. The
core theory described in the paper under study [15] can be summarized as follows:
Definition 3. Given two sets X and Y , a mapping h is a one-to-one mapping between its elements
(h(x) = y) such that x ∈ X and y ∈ Y and the inverse mapping exists h−1 (y) = x.
Definition 4. A Cantor space is the set of infinite numbers on the interval [0, 1] that can be represented
as a sequence a0 , a1 , . . . such that ai ∈ {0, 1}
Definition 5. A symbolic space is a set such that there exists a one-to-one map to some subset of
integers greater than 0.
Definition 6. An effective symbolic space is a pair (X, P ) where X is a symbolic space and P is a
one-to-one mapping P : X → 2X . Here 2X is the power set of all possible combinations of subsets
of X.
Theorem. Every effective symbolic space has a homeomorphic mapping to some subset of a cantor
space.


                                                    4
We note that the above definitions are not entirely complete, however, they capture the central
concepts associated with the proof that enable one to create the mappings between the spaces. This is
consistent with a mathematical collaborator that is participating in the theorem proving activity. We
proceed by simply pasting definitions and theorems from the summary as prompts without giving any
context. Figure 3 show how a definition of a bijective mapping is used as a prompt, and the output of
ChatGPT4 when prompted to generate a PVS theory implementing the definition. For further details
we point the reader to the appendix.
Limitations. The generated PVS theory is very close to a valid PVS theory that is syntactically
correct (can be parsed) and semantically correct (can be typechecked). But the autoformalization
by LLMs is not perfect and without errors. For instance, theory Mappings should be Mappings:
THEORY. The importing statement should be after begin. Also, set_theory in PVS is simply sets
defined in the prelude. These syntactic errors are easily fixed by providing ChatGPT4 with a few
examples of PVS syntax. In future work, we plan to address these issues by fine tuning ChatGPT4
using the PVS prelude and the PVS NASA library [13] which have large quantities of PVS code. We
will also explore combining this work with CoProver [18] to automatically generate lemmas from the
extracted theories, and automate proofs generation.

5   Conclusion and Future Work
In this work, we explored the transformative potential of integrating LLMs and proof assistants such
as PVS. By automating the extraction and formalization of mathematical content from research papers,
we provide a promising approach for academic review and knowledge discovery. This fusion of AI
and formal mathematical methods paves the way for more robust, collaborative research practices for
scientific discovery. We envision the following uses for our LLM-based math-PVS theorem proving
framework.
      1. Automated reviewing of papers by journals and reviewers for theorems and their proofs.
      2. Discovery of connections between unrelated subareas of mathematics enabling the extensions
         of existing theories to new settings.
      3. Construction of an assistant that removes the mechanical portions of theorem proving,
         thereby enabling the mathematician researcher to focus on the creative aspects of the work
         and the “bigger picture”.
In future work, we believe that several steps in the process will be automated, reducing the workload
on the scientific user of the math-PVS framework. Using the extensive PVS NASA library, we plan
to fine-tune a foundation model using existing PVS theories to reduce the number of errors in PVS
theory code generation.
Moreover, we plan to process a large corpus of mathematical literature using Nougat and generate
extensive math-PVS theories that will reduce the workload of the user.

References
 [1] National Academies of Sciences, Engineering, and Medicine. Artificial Intelligence to As-
     sist Mathematical Reasoning: Proceedings of a Workshop. The National Academies Press,
     Washington, DC, 2023.
 [2] Alex Davies, Petar Veličković, Lars Buesing, Sam Blackwell, Daniel Zheng, Nenad Tomašev,
     Richard Tanburn, Peter Battaglia, Charles Blundell, András Juhász, et al. Advancing mathemat-
     ics by guiding human intuition with AI. Nature, 600(7887):70–74, 2021.
 [3] Kenneth I Appel and Wolfgang Haken. Every planar map is four colorable, volume 98.
     American Mathematical Soc., 1989.
 [4] Warwick Tucker. The Lorenz attractor exists. Comptes Rendus de l’Académie des Sciences-
     Series I-Mathematics, 328(12):1197–1202, 1999.
 [5] Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan
     Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step, 2023.
 [6] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation
     and repair with large language models, 2023.


                                                 5
 [7] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-
     augmented language models, 2023.

 [8] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
     Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
     Schulman. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168,
     2021.

 [9] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset.
     NeurIPS, 2021.

[10] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: a cross-system benchmark
     for formal Olympiad-level mathematics, 2022.

[11] Sumit Kumar Jha, Rickard Ewetz, Alvaro Velasquez, and Susmit Jha. Responsible reasoning
     with large language models and the impact of proper nouns. In Workshop on Trustworthy and
     Socially Responsible Machine Learning, NeurIPS 2022, 2022.

[12] Sam Owre, John M Rushby, and Natarajan Shankar. Pvs: A prototype verification system. In
     International Conference on Automated Deduction, pages 748–752. Springer, 1992.

[13] NASA Langley Research Center. PVS NASA library. https://github.com/nasa/pvslib,
     2020. Accessed: October 27, 2023.

[14] Lukas Blecher, Guillem Cucurull, Thomas Scialom, and Robert Stojnic. Nougat: Neural optical
     understanding for academic documents, 2023.

[15] Jean-Charles Delvenne, Petr Kurka, and Vincent Blondel. Decidability and universality in
     symbolic dynamical systems. Fundamenta Informaticae, 74(4):463–490, 2006.

[16] Walter Rudin. Principles of mathematical analysis. McGraw Hill, 1953.

[17] John Guckenheimer and Philip Holmes. Nonlinear oscillations, dynamical systems, and
     bifurcations of vector fields, volume 42. Springer Science & Business Media, 2013.

[18] Eric Yeh, Briland Hitaj, Sam Owre, Maena Quemener, and Natarajan Shankar. CoProver: A
     recommender system for proof construction, 2023.


A    Appendix: ChatGPT4 Prompts, PVS theory, and PVS Proof

This appendix contains specific details of the example outlined in the main body of the paper. In
particular, we provide the following information:

      1. The ChatGPT4 prompts and responses for the example reported in the main body of the
         paper.

      2. The PVS theory generated by ChatGPT4 for the example in the main body of the paper.

      3. edited and final PVS theory for the example in the main body of the paper.

      4. The proof of the main theorem in PVS after it has been abstracted to the core concepts.

The first set of interactions with ChatGPT4 are used to input the original definitions and proposition
from the paper, we then use ChatGPT4 to summarize the information, abstract it, and generate a
graph that maps all the concepts introduced in the definitions along with their dependencies.
The second set of interactions with ChatGPT4 is used to generate PVS theories from the definitions
and summaries and prove the primary abstracted version of the proposition of interest.


                                                  6
7
8
9
10
11
12
From this point, we ask ChatGPT4 to generate PVS theories formalizing the various definitions and
theorems. The resulting PVS theories are manually edited to produce a single theory merging the
various generated theories. In particular, (1) fix syntax errors in the generated PVS code, and (2)
change the theorem from proving a surjective mapping to a bijective mapping, and (3) added two
lemmas that allow us to prove the main result.




                                                13
14
15
16
Mappings: theory
 begin

  importing sets

  𝑋: type

  𝑌: type

  𝐻: type = [𝑋 → 𝑌]

  injective(ℎ: 𝐻): bool =
       ∀ (𝑥1 , 𝑥2 : 𝑋): ℎ(𝑥1 ) = ℎ(𝑥2 ) implies 𝑥1 = 𝑥2

  surjective(ℎ: 𝐻): bool =
       ∀ (𝑦: 𝑌): ∃ (𝑥: 𝑋): ℎ(𝑥) = 𝑦

  bijective(ℎ: 𝐻): bool = injective(ℎ) and surjective(ℎ)

  H_INV: type = [𝑌 → 𝑋]

  inverse_mapping(ℎ: 𝐻, h_inv: H_INV): bool =
       ∀ (𝑥: 𝑋, 𝑦: 𝑌):
          (ℎ(𝑥) = 𝑦 implies h_inv(𝑦) = 𝑥) and
           (h_inv(𝑦) = 𝑥 implies ℎ(𝑥) = 𝑦)

  bijective_if_has_inverse: lemma
     ∀ (ℎ: 𝐻, h_inv: H_INV):
        injective(ℎ) and inverse_mapping(ℎ, h_inv) implies bijective(ℎ)

  ZeroOne: type = {𝑥: ℕ | 𝑥 = 0 or 𝑥 = 1}

  Binary_Sequence: type = [ℕ → sequence[ZeroOne]]

  Cantor_Space: type = setof[Binary_Sequence]

  CS: Cantor_Space

  symbolic_space_element: type

  symbolic_space: type = setof[symbolic_space_element]



                                             1
 ℕ>0 : type = {𝑥: ℕ | 𝑥 > 0}

 positive_integers: type = setof[ℕ>0 ]

 injective_map: [symbolic_space → positive_integers]

 injective_map_axiom: axiom
    ∀ (𝑥1 , 𝑥2 : symbolic_space):
      𝑥1 ≠ 𝑥2 implies injective_map(𝑥1 ) ≠ injective_map(𝑥2 )

 PSet_symbolic_space: type = setof[setof[symbolic_space]]

 𝑃: [symbolic_space → PSet_symbolic_space]

 injective_P_axiom: axiom
    ∀ (𝑥1 , 𝑥2 : symbolic_space): 𝑥1 ≠ 𝑥2 implies ℙ(𝑥1 ) ≠ ℙ(𝑥2 )

 effective_symbolic_space: type =
         [#ss_field: symbolic_space, pss_field: PSet_symbolic_space#]

 effective_symbolic_space_axiom(ss: symbolic_space): effective_symbolic_space =
      (#ss_field := ss, pss_field := ℙ(ss)#)

 subset_Cantor_Space: type = setof[Cantor_Space]

 injective(𝑓: [effective_symbolic_space → subset_Cantor_Space]): bool =
      ∀ (𝑥1 , 𝑥2 : effective_symbolic_space):
         𝑥1 ≠ 𝑥2 implies 𝑓(𝑥1 ) ≠ 𝑓(𝑥2 )

 bijective_map(𝑓: [symbolic_space → subset_Cantor_Space]): bool =
       ∀ (𝑥1 , 𝑥2 : symbolic_space): 𝑥1 = 𝑥2 implies 𝑓(𝑥1 ) = 𝑓(𝑥2 )

 MapLemma1: lemma ∃ (𝑓: [symbolic_space → ℕ]): bijective?(𝑓)

 MapLemma2: lemma ∃ (𝑓: [ℕ → Binary_Sequence]): bijective?(𝑓)

 mapping_exists_theorem: theorem
   ∀ (ss: symbolic_space):
     ∃ (𝑓: [symbolic_space → Binary_Sequence]): bijective?(𝑓)

end Mappings



                                           2
Verbose proof for mapping_exists_theorem.
mapping_exists_theorem:


    {1}   ∀ (ss: symbolic_space): ∃ (𝑓: [symbolic_space → Binary_Sequence]): bi-
          jective?(𝑓)
mapping_exists_theorem:


    [1]   ∀ (ss: symbolic_space): ∃ (𝑓: [symbolic_space → Binary_Sequence]): bi-
          jective?(𝑓)
Rule? (lemma ”MapLemma1”)
Applying MapLemma1
mapping_exists_theorem:
    {-1} ∃ (𝑓: [symbolic_space → ℕ]): bijective?(𝑓)
    [1] ∀ (ss: symbolic_space): ∃ (𝑓: [symbolic_space → Binary_Sequence]): bi-
         jective?(𝑓)
Rule? (lemma ”MapLemma2”)
Applying MapLemma2
mapping_exists_theorem:
    {-1} ∃ (𝑓: [ℕ → Binary_Sequence]): bijective?(𝑓)
    [-2] ∃ (𝑓: [symbolic_space → ℕ]): bijective?(𝑓)
     [1] ∀ (ss: symbolic_space): ∃ (𝑓: [symbolic_space → Binary_Sequence]): bi-
         jective?(𝑓)
Rule? (skeep)
Skolemizing and keeping names of the universal formula in (+ -),
mapping_exists_theorem:
    [-1] ∃ (𝑓: [ℕ → Binary_Sequence]): bijective?(𝑓)
    [-2] ∃ (𝑓: [symbolic_space → ℕ]): bijective?(𝑓)
     {1} ∃ (𝑓: [symbolic_space → Binary_Sequence]): bijective?(𝑓)
Rule? (skeep)
Skolemizing and keeping names of the universal formula in (+ -),
mapping_exists_theorem:
    {-1} bijective?(𝑓)
    [-2] ∃ (𝑓: [symbolic_space → ℕ]): bijective?(𝑓)
     [1] ∃ (𝑓: [symbolic_space → Binary_Sequence]): bijective?(𝑓)
Rule? (skeep)
Skolemizing and keeping names of the universal formula in (+ -),



                                           1
mapping_exists_theorem:
     [-1] bijective?(𝑓)
     {-2} bijective?(𝑓 ′ )
      [1] ∃ (𝑓: [symbolic_space → Binary_Sequence]): bijective?(𝑓)
Rule? (inst 1 ”f o f!1”)
Instantiating the top quantifier in 1 with the terms: 𝑓 ∘ 𝑓 ′ ,
mapping_exists_theorem:
     [-1]   bijective?(𝑓)
     [-2]   bijective?(𝑓 ′ )
      {1}   bijective?(𝑓 ∘ 𝑓 ′ )
Rule? (assert)
Simplifying, rewriting, and recording with decision procedures,
mapping_exists_theorem:
     [-1]   bijective?(𝑓)
     [-2]   bijective?(𝑓 ′ )
      [1]   bijective?(𝑓 ∘ 𝑓 ′ )
Rule? (use ”composition_bijective[symbolic_space,nat,Binary_Sequence]”)
Using lemma composition_bijective[symbolic_space, ℕ, Binary_Sequence],
This completes the proof of mapping_exists_theorem.
Q.E.D.




                                                 2
