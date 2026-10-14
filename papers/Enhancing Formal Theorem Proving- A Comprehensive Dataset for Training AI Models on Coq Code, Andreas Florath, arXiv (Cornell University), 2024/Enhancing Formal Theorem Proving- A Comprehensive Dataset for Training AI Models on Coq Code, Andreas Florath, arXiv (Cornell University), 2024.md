                                                                                                                                                                              V2




                                        Enhancing Formal Theorem Proving: A
                                        Comprehensive Dataset for Training AI Models on
                                        Coq Code
                                        Andreas Florath1 *

                                            Abstract
                                            In the realm of formal theorem proving, the Coq proof assistant stands out for its rigorous approach to verifying
                                            mathematical assertions and software correctness. Despite the advances in artificial intelligence and machine
arXiv:2403.12627v2 [cs.AI] 2 Apr 2024




                                            learning, the specialized nature of Coq syntax and semantics poses unique challenges for Large Language
                                            Models (LLMs). Addressing this gap, we present a comprehensive dataset specifically designed to enhance
                                            LLMs’ proficiency in interpreting and generating Coq code. This dataset, derived from a collection of over 10,000
                                            Coq source files, encompasses a wide array of propositions, proofs, and definitions, enriched with metadata
                                            including source references and licensing information. Our primary aim is to facilitate the development of LLMs
                                            capable of generating syntactically correct and semantically meaningful Coq constructs, thereby advancing the
                                            frontier of automated theorem proving.
                                            Initial experiments with this dataset have showcased its significant potential; models trained on this data exhibited
                                            enhanced accuracy in Coq code generation. Notably, a particular experiment revealed that a fine-tuned LLM
                                            was capable of generating 141 valid proofs for a basic lemma, highlighting the dataset’s utility in facilitating the
                                            discovery of diverse and valid proof strategies. This paper discusses the dataset’s composition, the methodology
                                            behind its creation, and the implications of our findings for the future of machine learning in formal verification.
                                            The dataset is accessible for further research and exploration:
                                            https://huggingface.co/datasets/florath/coq-facts-props-proofs-gen0-v1
                                            Keywords
                                            Mathematics Formal Proof — Coq — dataset — ML — LLM
                                        1 flonatel GmbH & Co. KG, Aachen, Germany

                                        *Corresponding author: andreas@florath.net




                                                                    Contents                                       8.3 Experiment 3: S (m * n) = m * n + n. . . . . . . . . . 6
                                                                                                                       Prompt and Challenge • Discussion
                                        1     Introduction                                                    1
                                                                                                                   9   Results                                                  6
                                        2     Objectives                                                      2
                                                                                                                   10 Outlook                                                   7
                                        3     Prior Art                                                       2
                                                                                                                   11 Acknowledgment                                            7
                                        4     Data Sources                                                    3
                                                                                                                   12 Appendix                                                  8
                                        5     Licenses                                                        3
                                                                                                                   12.1141 Ways to Proof the Lemma . . . . . . . . . . . . . 8
                                        6     Dataset “coq-facts-props-proofs”                                4
                                        7     Statistics                                                      4
                                        7.1 info.parquet . . . . . . . . . . . . . . . . . . . . . . . . . . . 4                       1. Introduction
                                        7.2 facts.parquet . . . . . . . . . . . . . . . . . . . . . . . . . . 4    In the exploration of Large Language Models (LLMs) for code
                                        7.3 props-proof.parquet . . . . . . . . . . . . . . . . . . . . . 4        optimization [1], two significant limitations were identified:
                                        8     Experiments                                                     5         • The dependency on human interaction impedes the
                                        8.1 Experiment 1: n = n + 0 . . . . . . . . . . . . . . . . . . 5                 model’s ability to function autonomously, limiting its
                                              Prompt and Reference Proof • Model Responses • Comparative                  applicability to extensive source code collections and
                                              Model Responses • Discussion                                                automation processes.
                                        8.2 Experiment 2: 7 + 3 = 10 . . . . . . . . . . . . . . . . . 6                • The indefinite nature of optimization completion, where
                                              Prompt and Theoretical Proof • Model’s Response • Comparison                a considerable portion of time is allocated to verifica-
                                              with Other Models • Discussion                                              tion rather than the optimization process itself. The
          Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 2/11



       measurement of optimization efficacy remains a chal-        for source code retrieval from S3 storage rather than includ-
       lenge.                                                      ing the code directly. Unprocessed raw data constitutes the
    The adoption of formal mathematical proofs presents a          dataset’s format, presenting each file in a single row. No-
logical advancement for overcoming the second limitation.          tably, precise and detailed license documentation is provided
Through formal proof assistants like Coq [2], Lean [3], or         for each file, an approach mirrored in the dataset discussed
Isabelle [4], the verification of propositions (such as lemmas     herein.
or theorems) becomes definitive. Once verified, the proposi-            On Huggingface [6], four additional datasets containing
tion is conclusively validated, eliminating the need for further   Coq source code were found. Two of these datasets comprised
evaluation.                                                        entire Coq files within single rows, leading to impractical
    This approach advocates for focusing on domains akin to        usability due to excessively large row sizes, with the largest
programming, yet characterized by determinate termination          containing over 6 million characters [7, 8]. Although these col-
states. The development of a system, potentially using agent-      lections were sizable, the licensing terms were inadequately
based models, is proposed. Such a system could subsequently        addressed, mixing data from various repositories under dif-
be applied to the autonomous optimization of source code,          ferent licenses without proper license adherence. Queries
thereby resolving the identified challenges.                       regarding licensing prompted the removal of both datasets.
                                                                        CoqGym [9] presents another notable attempt, offering
                      2. Objectives                                a substantial collection under the Creative Commons Attri-
                                                                   bution 2.0 Generic License [10], which is incompatible with
This research endeavors to advance the integration of machine      the licenses of the included Coq source code [11]. The issue
learning and artificial intelligence within the realm of formal    of license compatibility remains unresolved [12]. Further-
theorem proving, emphasizing the Coq Proof Assistant. By           more, CoqGym duplicated content from other projects into its
developing a dedicated dataset, this work aims to refine ML        repository, resulting in a dataset that is now outdated by five
models, notably enhancing LLMs’ capabilities in processing         years.
and generating Coq code. The objectives are meticulously                The dataset ”coq code” [13] on Huggingface, though ad-
outlined to encompass:                                             hering to a step-by-step format (including hypothesis, goal,
                                                                   and tactic), is limited, containing fewer than 25,000 entries.
Enhance Syntax and Semantic Comprehension: Enhanc-                 Its formatting is suboptimal, with data merged into a single
ing LLMs’ proficiency in interpreting and generating Coq           text column and separated by special tags.
code by providing a comprehensive dataset, thereby facilitat-
                                                                        In parallel efforts to utilize machine learning for enhanc-
ing a deeper comprehension of Coq’s syntax, mathematical
                                                                   ing formal proving in Coq, research has been conducted on the
logic, and proof strategies.
                                                                   automation of lemma name generation, leveraging a dataset
Enable Autonomous Content Generation: Empowering                   constructed from approximately 450 Coq source files from
LLMs to autonomously formulate mathematical definitions,           the math-comp project. This dataset, aimed at producing AST
lemmas, examples, and exercises, adjusting the complexity to       and token files through preprocessing, encountered challenges
bolster formal mathematics contributions.                          in data bloat and clarity, raising questions on its efficacy for
Optimize Coq Files for Machine Interaction: Refining Coq           LLM training or fine-tuning. To date, there’s no documented
codebases for improved machine interaction through simpli-         success in employing this specific dataset for LLM enhance-
fication and standardization, aiming for broader application       ment [14, 15]. Another effort was formatting Coq code using
and usage.                                                         language models. [16]
                                                                        No datasets containing Coq source code were found on
Facilitate Proof Generation: Equipping LLMs with the nec-
                                                                   Kaggle at the time of this writing. [17]
essary tools for autonomous proof generation, laying a foun-
                                                                        Against the backdrop of these endeavors, the dataset pre-
dation for innovative advancements in formal proofs.
                                                                   sented in this paper distinguishes itself through a unique com-
    The pursuit of these objectives is anticipated to elevate      bination of scale, organization, and focus on formal theorem
LLMs’ efficiency with Coq code, marking significant progress       proving. Unlike previously mentioned datasets, which either
in automated theorem proving and broadening the horizons           offer raw, unprocessed files or are constrained by licensing
for formal mathematics and computer science research.              and formatting issues, this dataset provides a curated and
                                                                   processed collection of Coq code.
                                                                        Two recent publications, although not directly related to
                       3. Prior Art                                the dataset focus of this paper, share similar approaches or
A singular comprehensive dataset, The Stack v2, has been           motivations:
identified amidst extensive research efforts as encompassing            An approach is described where a large-scale, graph-based
a diverse and extensive collection of Coq source code [5].         dataset and a graph neural network are employed to dynami-
Hosting over 150,000 files, with nearly 80,000 under a per-        cally integrate and leverage the hierarchical structure of def-
missive license, the dataset stands out by providing identifiers   initions, theorems, and proofs within Coq. This method sig-
          Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 3/11



nificantly enhances AI agents’ capability to adapt to new                                 5. Licenses
mathematical concepts and lemmas not encountered during
training, presenting a critical advancement in the automation      Addressing the complexities of licensing within the context
of theorem proving [18].                                           of aggregating datasets from various sources is a non-trivial
                                                                   challenge. [5] The datasets compiled for enhancing Large
    A novel methodology employing Monte Carlo Tree Search
                                                                   Language Models’ (LLMs) comprehension and generation of
(MCTS) to guide LLMs for the generation of verified pro-
                                                                   Coq code embody this challenge, as they amalgamate content
grams in Dafny, Lean, and Coq, named VMCTS, enhances
                                                                   from a multitude of repositories, each governed by its unique
synthesis capabilities by incorporating verifier feedback di-
                                                                   license. Given the diverse origins of the Coq source files,
rectly into the search algorithm, showcasing its efficiency
                                                                   the datasets do not subscribe to a singular license. Instead,
by solving complex verification problems in notably shorter
                                                                   each row in the facts and proposition / proofs table link to the
times compared to base models and even rivaling ChatGPT4’s
                                                                   license table where for each row the needed information can
augmented capabilities [19].
                                                                   be found.
                                                                       To comply with the stipulations of these licenses, espe-
                   4. Data Sources                                 cially those like MIT which mandate the inclusion of original
                                                                   licensing and authorship information, the dataset incorpo-
The Coq source files for the datasets were meticulously col-       rates copies of the original license files and, where available,
lected from a diverse array of sources across the internet,        the author files. This practice ensures adherence to the le-
focusing on repositories that are pivotal within the Coq com-      gal requirements of software redistribution, particularly for
munity and cover a broad spectrum of mathematical and com-         open-source licenses that permit such activities.
putational theories. These sources encompass a range of
                                                                       The compilation strictly omits libraries or files that lack
categories, including foundational libraries, formalized math-
                                                                   an explicit open-source license or are under a commercial
ematical theorems, computer science concepts, and algorithm
                                                                   license, thereby ensuring that the dataset comprises only data
implementations.
                                                                   that is legally redistributable. This careful selection process
    Foundational Libraries and Frameworks form the bedrock,        is pivotal for maintaining the integrity and legality of the
with repositories like the official Coq repository [20], math-     datasets, facilitating their use in research and development
comp (Mathematical Components) [21], and Coq’s standard            without infringing upon copyright laws or license conditions.
library extensions [22]. These are essential for anyone work-
ing with Coq, offering basic definitions, theorems, and tactics        The dataset encompasses a wide range of licenses, re-
widely used in further Coq developments.                           flecting the diversity of the Coq community and the broader
                                                                   open-source ecosystem. Among these are:
    Formalized Mathematics and Theorem Proofs are repre-
sented through collections such as GeoCoq (geometry) [23],              • Apache License 2.0 (Apache-2.0)
the formal proofs of the Four Color Theorem [24], and var-              • BSD 2-Clause ”Simplified” License (BSD-2-Clause)
ious projects under the Coq-community umbrella focusing                 • BSD 3-Clause ”New” or ”Revised” License (BSD-3-
on specific mathematical domains like algebra [25], number                Clause)
theory [26], and logic [27]. These projects not only provide            • CEA CNRS Inria Logiciel Libre License, versions 1.0,
proofs of known theorems but also extend the library of for-              2.1 (CECILL-1.0, CECILL-2.1), including its variants
malized mathematics accessible for Coq users.                             CECILL-B and CECILL-C for library and plugin dis-
                                                                          tributions, respectively
    Computer Science Theories and Algorithms feature promi-
                                                                        • GNU General Public License versions 2.0 only (GPL-
nently, with projects like Verdi (for distributed systems ver-
                                                                          2.0-only), 3.0 only (GPL-3.0-only), and 3.0 or later
ification) [28], the Iris project for concurrent systems [29],
                                                                          (GPL-3.0-or-later)
and various algorithm collections including sorting, graph
                                                                        • GNU Lesser General Public License versions 2.1 only
theory, and data structures. These repositories are crucial for
                                                                          (LGPL-2.1-only), 2.1 or later (LGPL-2.1-or-later), 3.0
researchers and practitioners interested in the formal verifica-
                                                                          only (LGPL-3.0-only), and 3.0 or later (LGPL-3.0-or-
tion of software and algorithms.
                                                                          later)
    The repositories were chosen for their quality, relevance to
                                                                        • MIT License (MIT)
the Coq community, and contribution to the ecosystem. The
                                                                        • Mozilla Public License 2.0 (MPL-2.0)
collected datasets aim to provide comprehensive coverage of
                                                                        • UniMath License (specific to the UniMath library)
the syntax and semantics employed in Coq development, sup-
porting the project’s goal of enhancing LLMs’ understanding            This approach ensures that the datasets not only respect the
and generation capabilities with respect to Coq code. The          legal and ethical considerations of software redistribution but
datasets ensure a wide representation of the Coq language’s        also provide a rich, legally compliant resource for advancing
potential applications, from pure mathematics to computer          the capabilities of LLMs in processing and generating Coq
science.                                                           code.
           Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 4/11



     6. Dataset “coq-facts-props-proofs”                            spdx-id detailing the license under which the repository’s
                                                                          content is distributed, in alignment with the Software
This dataset is comprised of three distinct tables:                       Package Data Exchange (SPDX) identifiers.
   1. Definitions or notations categorized as facts.                   The dataset is accessible on huggingface: [30].
   2. Theorems and lemmas, alongside their proofs, classified
      as propositions.
                                                                                          7. Statistics
   3. Licensing and repository information for each entry
      within the facts and propositions tables.                     7.1 info.parquet
                                                                    The info.parquet table comprises 142 rows, each repre-
     License identification was conducted manually: a license       senting a repository. The distribution of licenses across these
hint within the Readme file was prioritized, followed by the        repositories is outlined below:
contents of any LICENSE file. Only repositories under open-
source licenses permitting redistribution were included.
     The dataset exclusively features Coq source code files (.v      License                Count     License               Count
files), which were pre-processed using a customized OCaml            MIT                       43     Apache-2.0                3
parser to separate Coq sentences, remove comments, and elim-         LGPL-2.1-only             29     MPL-2.0                   3
inate directives like #global. This process also involved            LGPL-2.1-or-later         12     GPL-3.0-only              3
condensing multiple consecutive whitespaces into a single            CECILL-B                   9     GPL-3.0-or-later          3
space and deduplicating based on facts and proposition/proof         CECILL-1.0                 7     BSD-3-Clause              2
content rather than file origin. The preprocessing was purely        LGPL-3.0-only              7     CECILL-2.1                2
done on parsing level, no evluation of the Coq source code           LGPL-3.0-or-later          6     GPL-2.0-only              1
was done. Consequently, some parts of the Coq code may not           CECILL-C                   6     CECILL-2.0                1
evaluate or may not be compatible with the latest version of         BSD-2-Clause               4     UniMath                   1
Coq.
     The facts table is one cornerstone of the dataset, encom-      7.2 facts.parquet
passing definitions or notations. Each row within this table        Data pertaining to the facts.parquet table is provided below,
represents a unique fact, identified by a Coq definition or no-     with measurements based on character count:
tation. These facts are detailed through several key columns:
                                                                                    Columns                     4
fact the fact itself, presented in Coq syntax
                                                                                    Rows                  103,446
imports a list of imports, specifying the Coq modules and                           Shortest fact              12
     libraries required for the fact’s context                                      Longest fact           37,630
filename the filename, indicating the source file from which                        Mean length            132.26
      the fact was extracted                                                        Standard deviation     359.47
symbolic name the symbolic name, providing a reference
    handle for the fact to the repository and license infor-        7.3 props-proof.parquet
    mation.                                                         Details regarding the props-proof.parquet table are summa-
                                                                    rized below, with lengths measured in characters:
    The table props-proofs is the other key component
of the dataset. The structure is very similar to the facts table,            Columns                                    5
but instead of using the facts column there are two columns                  Rows                                166,035
proposition and proof.                                                       Shortest proposition                      13
    The ”info” table within our dataset acts as a vital link                 Longest proposition                    7400
between the symbolic name and its corresponding repository,                  Mean length proposition              104.05
enriched with precise licensing information. It is comprised                 Standard deviation proposition         97.65
of four columns:                                                             Shortest proof                            11
symbolic name serving as a unique identifier correlating to                  Longest proof                        177585
    entries within the ”facts” and ”props-proofs” tables                     Mean length proof                    347.88
                                                                             Standard deviation proof            1290.80
url providing the repository’s location which hosts the source
      Coq files                                                         Observations indicate high standard deviations, attributed
hexsha representing the Git SHA of the last commit at the           to the presence of a few exceptionally long facts, propositions,
     time the repository was checked out, offering a snapshot       and proofs. The deviation pattern when excluding the top 5%
     for reproducibility and version tracking                       of length can be seen in figure 1.
          Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 5/11



                                                                   complete dataset described in this paper, specifically designed
                                                                   to enhance its proficiency in interpreting and generating Coq
                                                                   code and serves as the experiment to show the usefulness of
                                                                   the dataset.
                                                                   Mistral-7b-Instruct-0.2 Based on the Mistral-7b architec-
                                                                   ture, this model leverages instructional data to guide its re-
                                                                   sponses and programming language understanding. [31]
                                                                   Starcoder2-15b Starcoder2-15b has been trained on over 600
                                                                   different programming languages, including Coq, providing
                                                                   it with a broad syntax and semantic understanding across a
                                                                   wide array of languages. [5]
Figure 1. Deviation of length of proofs for the 0.95 percentile    Google Gemini This publicly available chat model from
                                                                   Google demonstrates capabilities in natural language pro-
                                                                   cessing and understanding, applied across various contexts,
                    8. Experiments                                 including programming. [33]
In this section, we explore one of many possible applica- OpenAI ChatGPT 4 As OpenAI’s publicly available chat
tions of the dataset through the fine-tuning of an existing base   model, ChatGPT 4 showcases advancements in language mod-
model, Mistral-7b [31]. This exercise is meant to serve as         els’ ability to engage in detailed conversations and generate
an illustration of the dataset’s potential rather than a com- code snippets. [34]
prehensive or central focus of the paper. Our intention is
to demonstrate, via selected examples, how the dataset can         8.1 Experiment 1: n = n + 0
be utilized to potentially enhance LLM’s understanding and         8.1.1 Prompt and Reference Proof
generation of Coq code.                                            For this experiment, the lemma tested was as follows:
    The fine-tuning process, performed on an NVidia A30
GPU across approximately seven days, involved adapting the 1 Lemma plus_n_O : forall n:nat, n = n + 0.
model to better handle Coq syntax and logic as represented             The reference proof contained within the training data is
in the dataset. Every three hours a snapshot of the model was      straightforward [23]:
generated. It’s important to note that while the model’s per-
formance post fine-tuning provides insights into the dataset’s 1 Proof.
                                                                 2    induction n; trivial.
utility, it represents only one of many possible evaluation 3 Defined.
metrics.
    The model’s output underwent evaluation at a tempera-
ture setting of 0.4 across different snapshots using coqc or       8.1.2 Model Responses
coqide. We curated the output for readability, truncating          Among    the 563 responses generated that began with Proof.,
responses at logical endpoints such as Qed., to focus on the       141  were  identified as valid (see section 12.1), demonstrating
model’s capability to produce syntactically and logically co-      the model’s   adeptness not only in understanding Coq syntax
herent Coq constructs. These choices were guided by the goal       but also  in navigating   its semantic landscape to reach valid
of assessing the model’s ability to generate syntactically and     conclusions   through  various  methods.
logically correct Coq code, underlining the qualitative rather         Notably, the variety of proofs highlights the LLM’s ca-
than quantitative nature of this experiment. A version of the      pacity to utilize a broad spectrum of Coq’s proof strategies,
model which was trained only using Coq code with permissive        ranging from direct application of arithmetic simplification
licenses is publicity available [32].                              (auto with arith.) to structural induction and recur-
    Additionally, we made prompt adjustments to encourage          sive definitions (induction n as [| n IHn].). This
Coq-specific responses from the different models, indicating       diversity not only showcases the potential of LLMs in theo-
the necessity of tailored inputs for optimal output in domain- rem proving but also suggests a nuanced understanding of the
specific tasks. The comparison of the fine-tuned model against     Coq proof assistant’s capabilities, opening new avenues for
several prominent LLMs provides a broader context for eval- exploring automated theorem proving.
uating the dataset’s impact on enhancing Coq code genera-              These findings are particularly significant as they suggest
tion capabilities, albeit this comparison is illustrative of the   that LLMs, when equipped with a well-curated dataset, can
dataset’s potential rather than an exhaustive evaluation of its    extend beyond mere syntactic correctness to exhibit a deep
efficacy.                                                          comprehension of mathematical logic and proof strategies.
    The models under observation and for comparison:               This depth enables the generation of multiple, distinctively
                                                                   valid approaches to proving a single proposition, thereby en-
CoqLLM-FineTuned This model was fine-tuned with the                riching the repertoire of automated theorem proving.
              Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 6/11



        These implications reinforce the utility of specialized            the CoqLLM-FineTuned, alongside other prominent models
    datasets in enhancing the performance of LLMs within domain-           like ChatGPT 4, Google Gemini, and Starcoder2-15b, demon-
    specific tasks such as theorem proving.                                strated proficiency in Coq syntax and logical reasoning.
    8.1.3 Comparative Model Responses
                                                                           8.3 Experiment 3: S (m * n) = m * n + n.
    Mistral-7b-Instruct Responded in a non-Coq language and
    failed to generate a valid proof even after prompt adaptation.         8.3.1 Prompt and Challenge
                                                                           The lemma explored in this experiment was as follows:
    ChatGPT 4 Although replying in Coq, the proof offered was
    incorrect.                                                         1   Lemma mult_S : forall m n : nat, S (m * n) = m * n
                                                                                + n.
    Google Gemini Required prompt modification before pro-
    ducing a correct proof.                                                     Intentionally erroneous, this lemma serves to test the
    Starcoder2-15b Did not provide any proof, despite being                LLMs’ ability to recognize or question the validity of a propo-
    prompted.                                                              sition, essentially assigning them an impossible task.

    8.1.4 Discussion                                                       8.3.2 Discussion
    This experiment highlights the CoqLLM-FineTuned model’s                Despite the intrinsic fallacy in the lemma, all tested models,
    superior capability in producing correct Coq proofs that were          including Mistral-7b-Instruct, ChatGPT 4, Google Gemini,
    not part of its training set, distinguishing it from other mod-        Starcoder2, and CoqLLM-FineTuned, endeavored to construct
    els, including those of similar size and significantly larger          a proof without indicating any recognition of the proposition’s
    ones like ChatGPT 4 or Google Gemini. The model not only               incorrectness. This uniform approach across diverse models
    demonstrated its understanding of Coq syntax and logic but             reveals a critical area for future enhancement in LLMs’ ca-
    also its ability to creatively solve problems without directly         pabilities: the detection of inherently flawed or unsolvable
    reproducing training data.                                             problems.

    8.2 Experiment 2: 7 + 3 = 10
    8.2.1 Prompt and Theoretical Proof                                                             9. Results
    The prompt for this experiment was:                                    The fine-tuning of a Large Language Model (LLM) with
1   Lemma ex1: 7 + 3 = 10.                                                 the Coq dataset demonstrated promising outcomes, with the
                                                                           model generating outputs with a high probability exclusively
        Notably, this specific lemma did not exist within the train-
                                                                           in Coq syntax. This specificity in output underscores the
    ing dataset. However, a theoretically valid proof employing
                                                                           dataset’s effectiveness in aligning the trained model with the
    basic reflexivity is suggested:
                                                                           requirements of both agent systems and Coq runtime environ-
1 Proof.                                                                   ments, making it a preferred choice for these applications.
2   reflexivity.
3 Qed.
                                                                               The endeavor also revealed the feasibility of achieving
                                                                           significant advancements in model performance with lim-
                                                                           ited resources and within a constrained timeframe. The re-
    8.2.2 Model’s Response
                                                                           fined model showcased an ability to produce insightful, Coq-
    Remarkably, the CoqLLM-FineTuned model independently
                                                                           compatible remarks, underscoring the potential for further
    arrived with most responses at the same proof as the one
                                                                           enhancing the efficiency of theorem proving in Coq.
    proposed, successfully utilizing the reflexivity tactic.
                                                                               Moreover, the careful curation, cleanup, and licensing of
    8.2.3 Comparison with Other Models                                     the dataset not only facilitated this study but also ensure its
    Mistral-7b-Instruct Failed to provide a valid Coq proof,               utility for the broader research community. This resource is
    responding inappropriately and deviating significantly from            poised to contribute to the ongoing development of agents,
    the prompt.                                                            marking a crucial step in the journey towards more sophisti-
    ChatGPT 4, Google Gemini, and Starcoder2-15b Each of                   cated and autonomous theorem proving systems.
    these models managed to produce valid proofs, indicating a                 Building upon these achievements, the notable success in
    general competence in handling straightforward arithmetic              Experiment 1 (see section 8.1), where the fine-tuned LLMs
    propositions in Coq.                                                   generated 141 valid proofs for the proposition n = n + 0 opens
                                                                           a new vista for the application of LLMs in generating valuable
    8.2.4 Discussion                                                       Coq source code. This accomplishment illustrates the models’
    This experiment underscores the performance of the CoqLLM-             capacity not only to adhere to syntactic correctness but also to
    FineTuned model in generating a valid proof for a propo-               engage in creative problem-solving within the Coq framework.
    sition not present in its training set, further exemplifying           The presence of valid, varied proofs further underscores the
    its advanced reasoning capabilities. Unlike the Mistral-7b-            potential utility of LLMs as tools for enriching and expanding
    Instruct model, which failed to generate a correct response,           Coq datasets with new, verified source code.
          Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 7/11



                       10. Outlook
The successful fine-tuning of the Large Language Model
(LLM) using the Coq dataset opens up several promising
avenues for future research and application enhancements:

Agent-based Application: The dataset can serve as a training
data for models for developing agents capable of interacting
with, and reasoning about, Coq code. This could significantly
streamline processes in formal methods and theorem proving
by providing automated assistance.
Refining Prompts with the Dataset: Utilizing the dataset to
fine-tune prompts can enhance the generation of higher quality
and more relevant content. This improvement can bolster
the model’s capacity to tackle intricate problem-solving and
reasoning within formal verification’s scope.
Hypothesis, Goal, Tactic Approach: Implementing a struc-
tured approach that defines hypotheses, sets goals, and em-
ploys tactics could further sophisticate the model’s interaction
with formal proofs. This strategy could facilitate the devel-
opment of more advanced models capable of autonomously
devising and verifying proofs, thus pushing the boundaries of
what’s possible in automated theorem proving.
Curating, Enhancing, and Enlarging the Coq Source Code
Base Using LLMs: The demonstrated capacity of LLMs
to generate valid and diverse Coq proofs opens the door to
utilizing these models for the curation, enhancement, and
expansion of the Coq source code base. By integrating LLM-
generated code into the dataset, we can continuously improve
the quality and breadth of Coq resources available to the
research community, fostering a more dynamic and robust
ecosystem for theorem proving and formal verification.

    These directions not only underscore the potential for the
dataset to catalyze significant advancements in the field but
also highlight the broader implications for enhancing AI’s
role in formal methods and beyond.

                11. Acknowledgment
The author extend his sincere gratitude to Andrei Agapi for his
invaluable ideas and for conducting the initial review, which
significantly contributed to the enhancement of this paper.
    “Stylish Article” template [35] was used.
              Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 8/11



                                                         12. Appendix
    12.1 141 Ways to Proof the Lemma
    The validation was performed using coqc version 8.19.1. In addition to the proposition, the validated coq source file contained
    some Require Imports as well as some notations like plus 0 l or plus comm.
1  Proof. auto with arith. Qed.
2  Proof. destruct n; simpl; auto. Qed.
 3 Proof. induction n; simpl; auto. Qed.
 4 Proof. intro n; apply eq_add_S; auto with arith. Qed.
 5 Proof. intro n; destruct n as [|p]. - reflexivity. - simpl; auto. Qed.
 6 Proof. intro n; elim n ; auto with arith. Qed.
 7 Proof. intro n; elim n ; simpl; auto. Qed.
 8 Proof. intro n; elim n using nat_rect. - reflexivity. - intros m Hrec; simpl; auto. Qed.
 9 Proof. intro n; elim n using nat_rect. - reflexivity. - intros m Hrec; simpl; rewrite <- Hrec; auto with
        arith. Qed.
10 Proof. intro n; elim n using nat_rect. - reflexivity. - simpl. auto with arith. Qed.
11 Proof. intro n; elim n using nat_rect; auto. Qed.
12 Proof. intro n; elim n. - reflexivity. - intros m IHm. simpl. rewrite <- IHm. reflexivity. Qed.
13 Proof. intro n; elim n. - reflexivity. - intros p IHp; simpl; rewrite <- IHp; reflexivity. Qed.
14 Proof. intro n; elim n; auto with arith. Qed.
15 Proof. intro n; elim n; auto. Qed.
16 Proof. intro n; elim n; simpl. - reflexivity. - intros m IHm; rewrite <- IHm; reflexivity. Qed.
17 Proof. intro n; elim n; simpl. reflexivity. intros m IH. rewrite <- IH. auto with arith. Qed.
18 Proof. intro n; elim n; simpl. reflexivity. intros m IHm. rewrite <- IHm. reflexivity. Qed.
19 Proof. intro n; elim n; simpl; auto with arith. Qed.
20 Proof. intro n; elim n; simpl; auto. Qed.
21 Proof. intro n; induction n as [ | n IHn]. - reflexivity. - simpl; rewrite <- IHn; auto. Qed.
22 Proof. intro n; induction n as [ | p IHp]. - reflexivity. - simpl; rewrite <- IHp; reflexivity. Qed.
23 Proof. intro n; induction n as [| m IHm]; auto with arith. Qed.
24 Proof. intro n; induction n as [| n Hrecn]. - reflexivity. - simpl; rewrite <- Hrecn; reflexivity. Qed.
25 Proof. intro n; induction n as [| n IH]. - reflexivity. - simpl. apply f_equal. assumption. Qed.
26 Proof. intro n; induction n as [| n IH]. - reflexivity. - simpl. rewrite <- IH. reflexivity. Qed.
27 Proof. intro n; induction n as [| n IH]. - reflexivity. - simpl; auto. Qed.
28 Proof. intro n; induction n as [| n IH]. - reflexivity. - simpl; rewrite <- IH; reflexivity. Qed.
29 Proof. intro n; induction n as [| n IH]; auto. Qed.
30 Proof. intro n; induction n as [| n IH]; simpl. - reflexivity. - rewrite <- IH; ring. Qed.
31 Proof. intro n; induction n as [| n IH]; simpl; auto. Qed.
32 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl. rewrite <- IHn. reflexivity. Qed.
33 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; auto. Qed.
34 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; now rewrite <- IHn. Qed.
35 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- (IHn); auto. Qed.
36 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- (plus_n_O n); reflexivity.
       Qed.
37 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- IHn at 1; reflexivity. Qed.
38 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- IHn; auto. Qed.
39 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- IHn; reflexivity. Qed.
40 Proof. intro n; induction n as [| n IHn]. - reflexivity. - simpl; rewrite IHn at 1; reflexivity. Qed.
41 Proof. intro n; induction n as [| p Hp]. - reflexivity. - simpl; rewrite <- Hp; reflexivity. Qed.
42 Proof. intro n; induction n as [| p Hp]. - simpl; auto with arith. - simpl; rewrite <- Hp; reflexivity.
       Qed.
43 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl. rewrite <- (IHp). reflexivity. Qed.
44 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl. rewrite <- IHp. reflexivity. Qed.
45 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; auto with arith. Qed.
46 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; auto. Qed.
47 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; rewrite -> IHp at 1; reflexivity. Qed.
48 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; rewrite <- IHp at 1; reflexivity. Qed.
49 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; rewrite <- IHp; auto with arith. Qed.
50 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; rewrite <- IHp; auto. Qed.
51 Proof. intro n; induction n as [| p IHp]. - reflexivity. - simpl; rewrite <- IHp; reflexivity. Qed.
52 Proof. intro n; induction n as [|n IH]. - reflexivity. - simpl; rewrite <- IH. reflexivity. Qed.
53 Proof. intro n; induction n as [|n IHn]. - reflexivity. - simpl; auto. Qed.
54 Proof. intro n; induction n as [|n IHn]. - reflexivity. - simpl; rewrite <- IHn; reflexivity. Qed.
55 Proof. intro n; induction n as [|n IHn]; simpl; auto. Qed.
56 Proof. intro n; induction n as [|n’ IHn’]. - reflexivity. - simpl; rewrite <- IHn’; reflexivity. Qed.
57 Proof. intro n; replace 0 with (S 0 - 1); auto. Qed.
58 Proof. intro n; rewrite (plus_comm n 0); auto with *. Qed.
59 Proof. intro n; rewrite (plus_comm n 0); auto with arith. Qed.
60 Proof. intro n; rewrite (plus_comm n 0); auto. Qed.
           Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 9/11



61  Proof. intro n; rewrite (plus_comm n 0); reflexivity. Qed.
62  Proof. intro n; rewrite (plus_comm n 0); simpl; auto. Qed.
 63 Proof. intro n; rewrite (plus_comm n 0); trivial. Qed.
 64 Proof. intro n; rewrite <- (plus_n_O n); reflexivity. Qed.
 65 Proof. intro n; rewrite <- Nat.add_0_r at 1. reflexivity. Qed.
 66 Proof. intro n; rewrite Nat.add_0_r; reflexivity. Qed.
 67 Proof. intro n; rewrite Nat.add_comm; auto. Qed.
 68 Proof. intro n; rewrite Nat.add_comm; reflexivity. Qed.
 69 Proof. intro n; rewrite add_comm. reflexivity. Qed.
 70 Proof. intro n; rewrite add_comm; auto with arith. Qed.
 71 Proof. intro n; rewrite add_comm; reflexivity. Qed.
 72 Proof. intro n; rewrite plus_O_r; reflexivity. Qed.
 73 Proof. intro n; rewrite plus_comm with (m := 0); auto. Qed.
 74 Proof. intro n; rewrite plus_comm; apply plus_O_n. Qed.
 75 Proof. intro n; rewrite plus_comm; auto. Qed.
 76 Proof. intro n; rewrite plus_comm; exact (plus_O_n n). Qed.
 77 Proof. intro n; rewrite plus_comm; reflexivity. Qed.
 78 Proof. intro n; simpl. auto with arith. Qed.
 79 Proof. intro n; simpl; auto with arith. Qed.
 80 Proof. intro n; simpl; auto. Qed.
 81 Proof. intro; apply eq_add_S ; auto with arith. Qed.
 82 Proof. intro; apply eq_add_S; auto. Qed.
 83 Proof. intro; apply nat_ind with (P := fun n => n = n + O). - reflexivity. - intros; simpl; auto. Qed.
 84 Proof. intro; apply sym_eq; apply Nat.add_0_r. Qed.
 85 Proof. intro; elim n using nat_rect. - reflexivity. - intros m Hrec; simpl in |- *; rewrite Hrec; auto
        with arith. Qed.
 86 Proof. intro; elim n. - reflexivity. - intros; simpl; auto with arith. Qed.
 87 Proof. intro; elim n; simpl; auto. Qed.
 88 Proof. intro; induction n as [| n IH]; simpl; auto. Qed.
 89 Proof. intro; induction n as [| n IHn]. - reflexivity. - simpl; rewrite <- IHn; reflexivity. Qed.
 90 Proof. intro; induction n as [| p IHp]; simpl; auto with arith. Qed.
 91 Proof. intro; induction n as [| p IHp]; simpl; auto. Qed.
 92 Proof. intro; induction n as [|n IH]; simpl; auto. Qed.
 93 Proof. intro; induction n; simpl; auto. Qed.
 94 Proof. intro; rewrite <- (Nat.add_comm 0); reflexivity. Qed.
 95 Proof. intro; rewrite <- (add_comm 0); apply plus_O_n. Qed.
 96 Proof. intro; rewrite <- (plus_n_O n); reflexivity. Qed.
 97 Proof. intro; rewrite <- add_comm; auto with arith. Qed.
 98 Proof. intro; rewrite <- add_comm; auto. Qed.
 99 Proof. intro; rewrite <-plus_n_O. reflexivity. Qed.
100 Proof. intro; rewrite Nat.add_0_r; reflexivity. Qed.
101 Proof. intro; rewrite Nat.add_comm; auto with arith. Qed.
102 Proof. intro; rewrite Nat.add_comm; auto. Qed.
103 Proof. intro; rewrite Nat.add_comm; reflexivity. Qed.
104 Proof. intro; rewrite Nat.add_comm; trivial. Qed.
105 Proof. intro; rewrite add_comm; auto with *. Qed.
106 Proof. intro; rewrite add_comm; auto with arith. Qed.
107 Proof. intro; rewrite add_comm; auto. Qed.
108 Proof. intro; rewrite add_comm; reflexivity. Qed.
109 Proof. intro; rewrite add_comm; simpl; auto. Qed.
110 Proof. intro; rewrite add_comm; simpl; reflexivity. Qed.
111 Proof. intro; rewrite plus_comm; apply plus_O_n. Qed.
112 Proof. intro; rewrite plus_comm; auto with arith. Qed.
113 Proof. intro; rewrite plus_comm; auto. Qed.
114 Proof. intro; rewrite plus_comm; reflexivity. Qed.
115 Proof. intro; rewrite plus_comm; simpl; reflexivity. Qed.
116 Proof. intro; ring. Qed.
117 Proof. intro; ring_simplify; reflexivity. Qed.
118 Proof. intro; ring_simplify; trivial. Qed.
119 Proof. intro; simpl; auto with arith. Qed.
120 Proof. intros n; now rewrite <- Nat.add_comm. Qed.
121 Proof. intros. rewrite <- Nat.add_comm. apply eq_refl. Qed.
122 Proof. intros. rewrite <- plus_comm. reflexivity. Qed.
123 Proof. intros. rewrite Nat.add_comm; reflexivity. Qed.
124 Proof. intros; now rewrite Nat.add_0_r. Qed.
125 Proof. intros; now rewrite Nat.add_comm. Qed.
126 Proof. intros; rewrite <- (plus_n_O n); reflexivity. Qed.
127 Proof. intros; rewrite <- Nat.add_comm; reflexivity. Qed.
128 Proof. intros; rewrite <- add_comm; reflexivity. Qed.
129 Proof. intros; rewrite <- plus_n_O; reflexivity. Qed.
               Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 10/11



130 Proof. intros; rewrite Nat.add_comm; apply Nat.add_0_l. Qed.
131 Proof. intros; rewrite Nat.add_comm; apply add_O_l. Qed.
132 Proof. intros; rewrite Nat.add_comm; apply plus_O_n. Qed.
133 Proof. intros; rewrite Nat.add_comm; reflexivity. Qed.
134 Proof. intros; rewrite plus_comm; exact (plus_O_n n). Qed.
135 Proof. intros; ring. Qed.
136 Proof. intros; simpl; auto with arith. Qed.
137 Proof. simpl. auto with arith. Qed.
138 Proof. simple induction n; auto. Qed.
139 Proof. simple induction n; simpl in |- *; auto with arith. Qed.
140 Proof. simple induction n; simpl; auto with arith. Qed.
141 Proof. simple induction n; simpl; auto. Qed.




                                                          References
       [1]   Andreas Florath. LLM Interactive Optimization of Open Source Python Libraries – Case Studies and Generalization.
             2024. arXiv: 2312.14949 [cs.SE].
       [2]   The Coq Development Team. The Coq Proof Assistant. accessed 2024-02-29. URL: https://coq.inria.fr/.
       [3]   Lean. accessed 2024-03-18. URL: https://lean-lang.org.
       [4]   Isabelle. accessed 2024-03-18. URL: https://isabelle.in.tum.de.
       [5]   Anton Lozhkov et al. StarCoder 2 and The Stack v2: The Next Generation. 2024. arXiv: 2402.19173 [cs.SE].
       [6]   Huggingface Datasets. accessed 2024-03-01. URL: https://huggingface.co/datasets.
       [7]   Huggingface Dataset: coq-github-scrape. accessed 2024-02-27. URL: https://huggingface.co/datasets/
             cassanof/coq-github-scrape.
       [8]   Huggingface Dataset: coq-train. accessed 2024-02-27. URL: https://huggingface.co/datasets/metareflection/
             coq-train.
       [9]   Kaiyu Yang and Jia Deng. “Learning to Prove Theorems via Interacting with Proof Assistants”. In: International
             Conference on Machine Learning (ICML). 2019.
      [10] CC BY 2.0 LEGAL CODE Attribution 2.0 Generic. accessed 2024-03-01. URL: https://creativecommons.
           org/licenses/by/2.0/legalcode.en.
      [11] ShareAlike compatibility: GPLv3. accessed 2024-03-01. URL: https://wiki.creativecommons.org/wiki/
           ShareAlike_compatibility:_GPLv3.
      [12] License Compatibility Review Suggested for Dataset. accessed 2024-03-18. URL: https : / / github . com /
           princeton-vl/CoqGym/issues/87.
      [13] Dataset jbb/coq code. accessed 2024-03-01. URL: https://huggingface.co/datasets/jbb/coq_code.
      [14] Pengyu Nie et al. “Deep Generation of Coq Lemma Names Using Elaborated Terms”. In: International Joint Conference
           on Automated Reasoning. 2020, pp. 97–118. DOI: 10.1007/978-3-030-51054-1_6.
      [15] MathComp Corpus. accessed 2024-03-08. URL: https://github.com/EngineeringSoftware/math-
           comp-corpus.
      [16]   Pengyu Nie et al. Learning to Format Coq Code Using Language Models. 2020. arXiv: 2006.16743 [cs.HC].
      [17] Kaggle datasets. accessed 2024-03-01. URL: https://www.kaggle.com/datasets.
      [18] Jason Rute et al. Graph2Tac: Learning Hierarchical Representations of Math Concepts in Theorem proving. 2024. arXiv:
           2401.02949 [cs.LG].
      [19] David Brandfonbrener et al. Verified Multi-Step Synthesis using Large Language Models and Monte Carlo Tree Search.
           2024. arXiv: 2402.08147 [cs.SE].
      [20] Coq. accessed 2024-03-01. URL: https://github.com/coq/coq.
      [21] Mathematical Components. accessed 2024-03-01. URL: https://github.com/math-comp.
      [22] coq-ext-lib. accessed 2024-03-01. URL: https://github.com/coq-community/coq-ext-lib.git.
      [23] GeoCoq. accessed 2024-03-01. URL: https://github.com/GeoCoq/GeoCoq.
         Enhancing Formal Theorem Proving: A Comprehensive Dataset for Training AI Models on Coq Code — 11/11



[24] The Four Color Theorem. accessed 2024-03-01. URL: https://github.com/coq-community/fourcolor.
     git.
[25] algebra-tactics. accessed 2024-03-01. URL: https://github.com/math-comp/algebra-tactics.git.
[26] coqprime. accessed 2024-03-01. URL: https://github.com/thery/coqprime.
[27] 100 famous theorems proved using Coq. accessed 2024-03-01. URL: https://github.com/coq-community/
     coq-100-theorems.git.
[28] verdi. accessed 2024-03-01. URL: https://github.com/uwplse/verdi.
[29] stdpp. accessed 2024-03-07. URL: https://gitlab.mpi-sws.org/iris/stdpp.git.
[30] Coq Facts, Propositions and Proofs. accessed 2024-03-18. URL: https : / / huggingface . co / datasets /
     florath/coq-facts-props-proofs-gen0-v1.
[31]   Albert Q. Jiang et al. Mistral 7B. 2023. arXiv: 2310.06825 [cs.CL].
[32] CoqLLM-FineTuned-Experiment-Gen0. accessed 2024-03-18. URL: https://huggingface.co/florath/
     CoqLLM-FineTuned-Experiment-Gen0.
[33]   Gemini Team et al. Gemini: A Family of Highly Capable Multimodal Models. 2023. arXiv: 2312.11805 [cs.CL].
[34]   OpenAI et al. GPT-4 Technical Report. 2024. arXiv: 2303.08774 [cs.CL].
[35] Stylish Article. https://www.latextemplates.com/template/stylish-article. Accessed: 2023-11-
     01.
