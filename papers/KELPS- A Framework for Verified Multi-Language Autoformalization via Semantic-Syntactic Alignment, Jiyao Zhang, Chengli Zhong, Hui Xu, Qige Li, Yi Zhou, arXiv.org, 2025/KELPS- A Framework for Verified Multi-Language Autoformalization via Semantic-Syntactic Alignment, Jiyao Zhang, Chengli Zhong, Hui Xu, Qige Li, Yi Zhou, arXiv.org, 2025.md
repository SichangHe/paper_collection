                                               KELPS: A Framework for Verified Multi-Language Autoformalization via
                                                                Semantic-Syntactic Alignment


                                                                    Jiyao Zhang 1 2 Chengli Zhong 1 2 Hui Xu 1 Qige Li 1 Yi Zhou 1 2


                                                                  Abstract
                                               Modern large language models (LLMs) show
                                               promising progress in formalizing informal math-
arXiv:2507.08665v1 [cs.CL] 11 Jul 2025




                                               ematics into machine-verifiable theorems. How-
                                               ever, these methods still face bottlenecks due to
                                               the limited quantity and quality of multilingual
                                               parallel corpora. In this paper, we propose a novel
                                               neuro-symbolic framework KELPS (Knowledge-
                                               Equation based Logical Processing System) to
                                               address these problems. KELPS is an iterative
                                               framework for translating, synthesizing, and filter-
                                               ing informal data into multiple formal languages
                                               (Lean, Coq, and Isabelle). First, we translate nat-              Figure 1. An overview of the relationships between natural lan-
                                               ural language into Knowledge Equations (KEs),                    guage (NL), Knowledge Equations (KEs), and formal languages
                                               a novel language that we designed, theoretically                 (FLs). KEs are extracted from NL through semantic parsing, then
                                               grounded in assertional logic. Next, we convert                  transformed into various FLs via specific syntactic rules.
                                               them to target languages through rigorously de-
                                               fined rules that preserve both syntactic structure               while such verification cannot eliminate minor errors or
                                               and semantic meaning. This process yielded a par-                critical flaws.
                                               allel corpus of over 60,000 problems. Our frame-
                                                                                                                A rigorous formal system is therefore essential for unam-
                                               work achieves 88.9% syntactic accuracy (pass@1)
                                                                                                                biguous mathematical representation. Modern proof assis-
                                               on MiniF2F, outperforming SOTA models such as
                                                                                                                tants have shown significant potential through landmark
                                               Deepseek-V3 (81%) and Herald (81.3%) across
                                                                                                                achievements such as the formalization of the Four-Color
                                               multiple datasets. All datasets and codes are avail-
                                                                                                                Theorem in Coq (Gonthier et al., 2008) and the Liquid Ten-
                                               able in the supplementary materials.
                                                                                                                sor Experiment (Scholze, 2022) in Lean4. However, writing
                                                                                                                formal proofs is laborious and often challenging, highlight-
                                                                                                                ing the importance of autoformalization. This paper focuses
                                         1. Introduction                                                        specifically on statement autoformalization, a necessary pre-
                                                                                                                requisite for proof autoformalization.
                                         Formalizing mathematical semantics as machine-verifiable
                                         codes has been a fundamental pursuit since Leibniz to Wu               Early attempts regarded this problem as a machine trans-
                                         Wen-Tsun (Wu, 2001), as informal statements’ ambiguity                 lation problem (Wang et al., 2018). They trained neural
                                         impedes proof verification, particularly in advanced mathe-            models to translate LaTex-written text into the formal Mizar
                                         matics. Many sophisticated mathematical proofs span hun-               language. Recent studies (Wu et al., 2022) focus on utilizing
                                         dreds of pages and require extensive verification by experts,          the in-context learning ability of LLMs.
                                           *
                                             Equal contribution 1 School of Information Science and Tech-       While fine-tuning models on large-scale parallel natural NL-
                                         nology, University of Science and Technology of China, Hefei,          FL datasets has achieved remarkable success, this approach
                                         China 2 USTC Knowledge Computing Lab. Correspondence                   remains constrained by the limited quantity and diversity
                                         to: Jiyao Zhang <ambitious 777@mail.ustc.edu.cn>, Yi Zhou              of available NL-FL (natural language to formal language)
                                         <yi zhou@ustc.edu.cn>.                                                 pairs. Prior work has explored strategies such as translating
                                         Proceedings of the 42 nd International Conference on Machine           natural language problems into formal language expressions
                                         Learning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025            (Ying et al., 2024) or back-translating formal language cor-
                                         by the author(s).                                                      pora into natural language statements (Gao et al., 2025).

                                                                                                            1
          KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Nevertheless, the quality of synthetically generated data,                ments over existing baselines on mainstream evaluation
along with maintaining semantic alignment between FL and                  benchmarks (MiniF2F, FormalMATH).
NL remains challenging.
In this paper, We introduce KELPS (Knowledge Equation                2. Related Work
Linguistic Parsing System), a rule-based framework de-
                                                                     2.1. Formal System
signed to translate natural language mathematical statements
into multiple formal languages, including Lean4 (Moura &             Natural languages exhibit inherent ambiguity in both textual
Ullrich, 2021), Coq (Barras et al., 1999), and Isabelle (Paul-       and symbolic forms (Ganesalingam, 2013), complicating
son, 1994). As illustrated in Figure 2, KELPS consists of            syntactic analysis and semantic extraction. This has moti-
three core components.                                               vated systematic efforts to formalize mathematical expres-
                                                                     sions through logical frameworks (Trybulec, 1989; Gordon,
(1) Semantic Parsing. The input natural language is first
                                                                     2000; Carneiro, 2024). Existing approaches fall into two
translated into an intermediate formal representation—the
                                                                     main distinct categories: controlled natural languages and
Knowledge Equation. The formal definition and implemen-
                                                                     formal language systems.
tation details are in Section 3.1.
                                                                     Controlled Natural Language (CNL) systems employ re-
(2) Syntactic Alignment. The results in stage 1 are then
                                                                     stricted natural language subsets with predefined grammars,
parsed and converted into various formal languages via
                                                                     as exemplified by Mizar (Grabowski et al., 2010) and Math-
parallel complex rules. Compilers will help to check its
                                                                     Nat (Humayoun & Raffalli, 2010). Recent advances in-
correctness.
                                                                     clude grammatical frameworks like GF (Ranta, 2004), with
(3) Semantic Verification. Formal statements generated               GFLean (Pathak, 2024) demonstrating direct text-to-Lean
in Stage 2, even though compiled successfully, still need            parsing.
semantic checks to be correct. We adopt the approach pro-
                                                                     Formal language systems (Lean, Coq) uniformly repre-
posed in (Xin et al., 2025), leveraging a LLM-as-a-Judge
                                                                     sent theorems through three core elements (Declaration,
framework.
                                                                     Fact, Query) despite differing in styles. To our knowl-
We propose a data augmentation and expert iteration frame-           edge, this work presents the first automated framework sup-
work for progressive model enhancement. Our approach                 porting multi-formal-language translation. Compared to
combines two key strategies: (1) A data synthesis module             existing formal languages, our knowledge equation frame-
that efficiently generates various formalization data through        work achieves superior expressiveness and natural language
randomized combinations of concepts and operators; (2) An            alignment while maintaining simpler structure and better
expert iteration process where our model successfully parsed         extensibility.
>60,000 formalized problems. The synthesized data set was
used to train our KELPS translator model. Comprehensive              2.2. Autoformalization
evaluations demonstrate its superior performance, achieving
88.9% (pass@1) syntactic accuracy in the MiniF2F test,               Autoformalization constitutes a specialized machine trans-
outperforming baseline models including Herald (81.3%),              lation task that transforms natural language statements into
DeepSeek-v3 (81%) and Llama (61.4%).                                 formal representations while preserving semantic content
                                                                     and complying with target syntax requirements. Initial inves-
Our main contributions are as follows.                               tigations explored neural approaches like (Wang et al., 2018;
                                                                     Cunningham et al., 2023), demonstrating the feasibility of
   • We propose a novel semantic parsing strategy that first         this paradigm.
     transforms natural language into a simple intermediate
     representation. This representation enables flexible            Current research on LLM-based autoformalization primar-
     translation into multiple formal languages through pre-         ily follows two dominant approaches: (1) few-shot in-
     defined rules while preserving semantic fidelity.               context learning (Wu et al., 2022; Patel et al., 2023; Zhou
                                                                     et al., 2024), and (2) fine-tuning LLMs on NL-FL pairs
   • We propose a novel data synthesis strategy that enables         (Lu et al., 2024a;b; Gao et al., 2025). While the latter has
     precise atomic-level control over generated problems.           shown promising results with 96% (pass@128) accuracy
     We further provide an ontology that encompasses 40              in MiniF2F (Zheng et al., 2021), performance drops to just
     core concepts and 180 operators.                                16% (pass@128) on the College CoT benchmark, revealing
                                                                     the critical limitation of NL-FL data scarcity.
   • We introduce a dataset comprising 60,000 real-
     world and synthetic problems spanning K-12 and                  A parallel research direction addresses the more challenging
     undergraduate-level mathematics. Our KELPS transla-             task of formal proof generation, where natural language
     tor, trained on this dataset, shows substantial improve-        proofs often diverge substantially from their formal counter-

                                                                 2
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment




Figure 2. Overview of Our Method. (a) Data Collection. We gather problems from various sources, including online resources and
exercise sets, and construct an ontology library of relevant concepts and theorems. Through filtering and data synthesis strategies, we
obtain a natural language (NL) corpus. (b) Semantic Parsing. We employ the KELPS model to perform semantic parsing, translating
natural language problems into knowledge equations. The initial iteration of data is obtained through annotation. (c) Syntax Validation.
The knowledge equations generated in (b) are validated by the AL Parser. Problems that pass validation are then converted into other
formal languages via rule-based transformation. (d) Semantic Validation. Data that passes the compiler validation in the previous stage
undergoes semantic review by both LLMs and human experts. Finally, the verified data is incorporated into the dataset, which is then used
to continuously train the baseline model.


parts. Current approaches include: (1) proof decomposition              The alternative paradigm (Wu et al., 2024; Gao et al., 2025)
into draft skeletons with subsequent completion (Jiang et al.,          initiates from formal language corpora, employing LLMs
2022; Wang et al., 2023), and (2) direct neural translation of          for backward translation to natural language. While valu-
informal proofs (Wang et al., 2024; Shao et al., 2024). The             able, this approach remains fundamentally constrained by
first approach uses language models to complete proof steps             the scope and completeness of existing formal libraries.
within a structured framework, whereas the second aims for
                                                                        Building upon existing work (Huang et al., 2024; Liu et al.,
complete automated translation.
                                                                        2025) that generates diverse problems through random-
                                                                        ized concept selection from a predefined concept library,
2.3. NL-FL Dataset Generation                                           we introduce a more controlled synthesis approach. Our
The scarcity of high-quality, large-scale natural language-             method employs structured Concept-Operator templates
formal language (NL-FL) parallel datasets remains a funda-              to achieve three key advances: (1) ensuring comprehensive
mental challenge in autoformalization research. Since hiring            theorem coverage through a Concept-Operator library, (2)
domain experts for annotation is expensive and inefficient,             enabling easy-to-hard theorem synthesis via predefined tem-
recent work has investigated leveraging large language mod-             plates, and (3) generating theorem diversity through various
els for scalable dataset generation. Existing approaches                Concept-Operator combinations.
include two main categories:
The first line of work (Jiang et al., 2023; Li et al., 2024; Ying       3. Methodology
et al., 2024) exploits the wide availability of informal mathe-         In this section, we present our core methodologies for state-
matical texts, using LLMs to translate NL statements into FL            ment autoformalization and dataset construction. Section 3.1
statements. Although this pipeline has yielded some large-              establishes our theoretical foundations (Assertional Logic
scale datasets, it remains hampered by several limitations:             and Knowledge Equations). Section 3.2 presents the com-
the translation pipeline requires extensive post-processing,            plete system architecture, and Section 3.3 details our syn-
often produces low-quality statements, and faces challenges             thetic data generation strategy.
due to the scarcity of cutting-edge domain data.


                                                                    3
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

3.1. Assertional Logic and Knowledge Equation                         where “var” represents a free variable (belongs to Individual
                                                                      in AL) and “ConceptType” is a defined concept. Its seman-
We introduce Assertional Logic (AL), a knowledge repre-
                                                                      tic meaning is similar to “Assume x is an integer ...” and the
sentation system with formally specified syntax.
                                                                      syntactic part of “fixes n :: int” in Isabelle or “(n : Z)” in
                                                                      Lean4.
3.1.1. A N I NTRODUCTION TO A SSERTIONAL L OGIC
                                                                      Definition 3.4. Fact part of a knowledge equation has the
Assertional Logic (AL) (Zhou, 2017), is an extension of first-        form of
order logic with enhanced power as expressive as higher-
order logic, while these representations are usually human-                     [Assertion1; Assertion2; Assertion3...]         (3)
friendly.
Definition 3.1. The Syntactic structure of a given domain             During the translation process, KELPS model will system-
in AL is a tripe ⟨I, C, O⟩. I is the collection of individuals,       atically capture all known information, (including inferable
corresponding to objects in the domain. C is the collection           propositions such as “Set S is finite”), and formalize them
of concepts, representing all sets of objects that have some          as assertions. By leveraging the equivalence of a proposi-
properties in common. O is the collection of all operators,           tion A ≡ (A = True), this representation ensures seamless
which acts among concepts and individuals like a function.            translation to various formal languages.
                                                                      Definition 3.5. Query part shares the syntactic structure
This structure has a natural correspondence with set theory,          with facts, but differs in their semantic meaning.
where individuals map to elements, concepts to sets, and
operators to functions.                                                                        Assertion                        (4)
Definition 3.2. An assertion is the of form
                                                                      The assertions in the Query typically represent propositions
                          a=b                              (1)        requiring proof (for closed-form problems) or propositions
                                                                      we aim to investigate (for open-ended questions). For the
where a and b are two terms. From a semantic perspective,             later situation, we use “ ? ” as syntax sugar to replace the
it claims that the left and the right side refer to the same          real item. This is just like “ sorry ” in Lean 4.
thing. A term is an individual, either an atomic individual
                                                                      We designed the Backus-Naur Form (BNF) of Knowledge
a ∈ I or the compound individuals O(a1 , ..., an ). Where
                                                                      Equations based on the formal definitions above. And by
O represents an operator on some individuals a1 , ..., an .
                                                                      using ANTLR4, we implemented an extensible parser frame-
Building upon AL, we presented Knowledge Equations (KE)               work that automatically transforms Knowledge Equations
to represent all knowledge with the same form. There is an            into equivalent representations in target formal languages.
example in Fig 1.                                                     The correctness is guaranteed by translation rules designed
                                                                      by human experts:
3.1.2. T RANSLATE KE INTO MULTIPLE LANGUAGE
                                                                                      CKE 7→ CTL ,    OKE 7→ OTL                (5)
One of the biggest benefits of AL is that it could uniformly
formalize every knowledge into assertions of the form a = b.          where CKE and OKE represents concepts and operators in
Consequently, all mathematical assertions can be systemati-           KE, CTL and OTL represents the same semantic object in
cally translated into other formal languages, including but           the target language.
not limited to Lean and Coq.
Unlike GFLean (Pathak, 2024) which handles natural lan-               3.2. KELPS Framework
guage in its entirety, our method specifically targets asser-         In this subsection, we present the KELPS framework (illus-
tions, concepts, and operators. The simplified syntax works           trated in Figure 2), which comprises three core components:
with just a handful of core elements, enabling efficient trans-       Semantic Parsing, Syntactic Validation, and Semantic Vali-
lation to various formal languages.                                   dation. We will now describe each component in sequence.
In summary, a mathematical question can be divide into
three parts: Declartion, Fact and Query. And we give each             3.2.1. S EMANTIC PARSING
of their formal definitions.                                          Large-scale data annotation remains highly laborious. We
Definition 3.3. Declaration part of a knowledge equation              develop an iterative pipeline that first fine-tunes DeepSeek-
has the form of                                                       Math-7B-Base on 1,200 manually annotated examples (Fig.
                                                                      2), then automatically processes unannotated data. The
                     var : ConceptType                     (2)        model’s outputs undergo syntactic and semantic checks,

                                                                  4
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

with validated results expanding the training set through            template-based synthesis of NL-AL pairs through a com-
multiple refinement cycles. After seven iterations, our              bination of templates. Implementation details follow in
model processed > 50K validated samples.                             subsequent sections.

3.2.2. S YNTAX VALIDATION                                            3.3.1. B UILDING THE M ATHEMATICAL O NTOLOGY
To ensure the syntactic correctness of the semantic parsing          We manually constructed a mathematics ontology covering
results obtained from Section 3.2.1, we implement a two-             most K12 and selected undergraduate-level mathematical
stage validation process.                                            topics, which comprises 6 major topics, 40 core concepts,
                                                                     and 180 operators. This ontology development effort re-
We first perform grammar verification using our ANTLR4-
                                                                     quired approximately three weeks of work by two mathe-
based knowledge equation parser that guarantees strict com-
                                                                     matical graduate students.
pliance with formal specifications. Subsequently, we em-
ploy the target language’s compiler to verify its final cor-         The complete specifications and structural details of the
rectness.                                                            ontology are provided in Appendix A.
For statements processed by the knowledge equation parser,
                                                                     3.3.2. C OLLECTION AND P ROCESSING DATA
approximately 80-90% successfully pass validation through
the target language compiler typically. The remaining cases          This module discusses two main steps in building our dataset
primarily involve minor type conversion errors, which we             from NL problems —- problem collection, filtering, and
analyze comprehensively in Appendix C.                               translation.
                                                                     NL Problems Collection
3.2.3. S EMANTIC VALIDATION
                                                                     The Numina (Li et al., 2024) dataset represents the largest
To ensure the semantic correctness of the semantic parsing
                                                                     and most comprehensive open-source collection of K12
results obtained from Section 3.2.2, our evaluation frame-
                                                                     mathematics materials, incorporating diverse sources rang-
work incorporates insights from mainstream methods (Wu
                                                                     ing from AIME competition problems to Chinese K12 cur-
et al., 2022; Gao et al., 2025). However, we observe that
                                                                     riculum content. In this study, we selected Numina as our
back-translation from formal to natural language fails to
                                                                     primary reference dataset due to its unique coverage that sub-
preserve semantic fidelity, thereby introducing extra mea-
                                                                     sumes content from numerous other mathematical datasets.
surement errors. Furthermore, the binary True/False classi-
fication criterion is insufficient for the precise measurement       Filtering and Translation
of semantic alignment in formalized expressions.
                                                                     We first filtered out unsupported problems from the Nu-
We evaluate formalized statements through a graded align-            mina dataset, including out-of-ontology mathematical ques-
ment assessment framework (0-5 scale) with corresponding             tions, retaining approximately 100,000 items. Subsequently,
natural language expressions. Uncompilable statements are            we removed problems unsuitable for formalization, such
automatically assigned a score of 0. The evaluation is per-          as questions with graphical representations. Finally, we
formed using DeepSeek-V3 (version 250324) with default               yielded a corpus of 70,000 problems for translation.
parameters.
                                                                     We adopted an expert-iterative approach for continuous
To enhance robustness, we adopt a sample@3 strategy in               problem parsing and successfully translated 50,000 prob-
the second stage: for each evaluation example, we collect            lems after seven iterations.
three independent judgments from DeepSeek-v3. The final
verdict is determined via majority voting, where semantic            3.3.3. S YNTHESIS S TRATEGIES
success is only confirmed if at least two 5 scores on semantic
                                                                     This subsection presents our synthetic data generation frame-
evaluation. All reported semantic evaluation results adhere
                                                                     work, which consists of two key components: template cre-
to this protocol.
                                                                     ation based on our mathematical ontology, and a systematic
                                                                     template combination strategy.
3.3. AL-FL Data Generation
                                                                     Templates Creation
This section presents the KELPS dataset construction
methodology - a corpus of 60,000+ NL-FL and AL-FL                    Using the strong in-context learning capabilities of LLM,
pairs supporting major formal languages.                             we found that providing just 3-shot examples was sufficient
                                                                     for the model to correctly learn patterns of target concepts
Our pipeline first establishes a mathematics ontology, then          and operators. For our template-based generation tasks,
employs dual generation strategies: (1) translation of nat-          DeepSeek-v3 (Liu et al., 2024) achieved a 90% syntactic
ural language problems into AL representations, and (2)

                                                                 5
            KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


Table 1. Evaluating Performance Across Different Models and Datasets. We highlight the top-performing results for syntactic accuracy in
red and those for semantic accuracy in green. Syntactic accuracy is determined by whether the code passes compiler verification, while
semantic accuracy scores are obtained through LLM majority voting. The version of Deepseek-V3 used is DeepSeek-V3-0324. Given the
substantial volume of problems, we selectively sampled 200 questions from FormalMATH and 300 from Numina-Hard for experiments.

                                         MiniF2F           MiniF2F-Isabelle        Numina-Hard            FormalMATH
                  Model
                                    Syntax    Semantic    Syntax       Semantic   Syntax   Semantic     Syntax    Semantic
            DeepSeek-V3 (671B)       81%        4.00      56.5%          2.74      82%        4.02      58.3%        2.90
                Herald (7B)         81.3%       3.58        –              –      85.5%       3.30      73.8%        3.11
               LlaMa-3 (8B)         61.4%       2.63      54.3%          2.27     62.3%       2.58      37.7%        1.56
               KELPS (7B)           88.9%       4.05      82.2%          3.56     94.3%       4.49      74.3%        3.29


accuracy.                                                              we conduct comparative benchmarks across three math-
                                                                       ematical datasets: MiniF2F, FormalMATH, and Numina-
In addition to templates derived from individual concepts,
                                                                       Hard. These established benchmarks comprehensively cover
we extract specialized templates from concrete problem
                                                                       olympiad/undergraduate mathematics through diverse prob-
instances. For example, the problem “Find all integers such
                                                                       lem types, ideal for formalization testing.
that [a is a prime and a < 15]” is abstracted into a template
where the condition “[a is a prime and a < 15]” is replaced
                                                                          • MiniF2F. (Zheng et al., 2021) A widely adopted mul-
with a generic “[property]” placeholder. This approach
                                                                            tilingual benchmark for auto-formalization tasks, com-
enhances the model’s capacity to generate diverse problem
                                                                            prising K12-level mathematical problems. In this work,
variations.
                                                                            we only evaluate its test set.
Templates Combination
                                                                          • FormalMATH. (Yu et al., 2025) A formalized mathe-
However, this approach tended to produce problems with                      matical benchmark that spans Olympic competitions
limited diversity, and the model occasionally made errors                   and undergraduate-level problems in multiple domains.
due to incomplete conceptual understanding. To address                      We randomly select 200 problems across various math-
these limitations, we developed a composite template strat-                 ematical domains for evaluation.
egy that systematically combines templates of varying com-
plexity - from basic concept applications to advanced prob-               • Numina-Hard. The Numina-Hard dataset comprises
lem types. We ultimately constructed a corpus of 50+ high-                  300 challenging problems randomly selected from the
quality templates, significantly improving both the diversity               KELPS dataset.
and complexity of generated problems.
                                                                       Due to the comprehensiveness and practicality of Mathlib
The complete set of prompting templates employed to gen-               (Blokpoel, 2024), we adopt Lean4 as our primary formaliza-
erate synthetic data is provided in Appendix B.2.                      tion language. All experiments are conducted in Lean4 by
                                                                       default. In addition, we evaluate the NL to Isabelle transla-
4. Experiments                                                         tion on the MiniF2F benchmark. Herald’s results (Gao et al.,
                                                                       2025) were excluded as their experimental setup diverged
We conduct a comprehensive series of experiments to evalu-             from our task requirements.
ate both the performance of the KELPS translator and the
quality of the KELPS dataset. Section 4.1 details the exper-           Experimental Process. To validate our model’s capabil-
imental setup and configurations. Section 4.2 presents the             ities, we employ the experimental pipeline illustrated in
main results of multiple benchmarks. Section 4.3 provides              Fig 2. It comprises three core steps: semantic parsing,
an ablation study to analyze the effect of different compo-            syntax validation, and semantic validation, with detailed
nents. Finally, Section 4.4 offers a further analysis of the           descriptions provided in Section 3.3. For the Herald model,
influencing factors behind the results.                                we rigorously maintain the original configuration reported
                                                                       in (Gao et al., 2025). The implementation details and hy-
4.1. Experimental Setup                                                perparameter settings for all other models are provided in
                                                                       Appendix B.1.
Fine-tuning. We employ DeepSeek-Math-7B-Base as our
base model and conduct supervised fine-tuning on the                   All KELPS experiments used NL-Lean4 fine-tuning and
KELPS dataset using a full-parameter training approach.                translated directly into Lean4 in this chapter, except for
                                                                       MiniF2F-Isabelle, which employed NL-AL training fol-
Dataset.     To evaluate the performance of our system,                lowed by rule-based Isabelle translation.

                                                                   6
          KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Our experimental environment utilizes Lean v4.19.0 (with            (2) the mixing ratio between synthetic and authentic data
Mathlib4 of the same version), and Isabelle 2025 (March             samples.
2025). The header files and executable code used in our
                                                                    As shown in Table 2, the experimental results demonstrate
experiments are included in our supplementary materials.
                                                                    that our synthetic data augmentation approach significantly
                                                                    improves model performance. We observe a nonlinear rela-
4.2. Main Results                                                   tionship between training data scale and model performance.
In this section, we present a systematic comparison between         When the dataset is small (< 20K samples), increasing its
the KELPS model and other baseline models across vari-              size significantly improves both semantic understanding and
ous benchmark datasets. Our evaluation framework assesses           grammatical accuracy. However, beyond a certain threshold,
two critical dimensions of model performance: (1) syntactic         further scaling yields diminishing returns. This implies that
accuracy, measuring formal correctness, and (2) semantic            prioritizing high-quality, diverse training data may be
accuracy, evaluating meaningful correspondence to mathe-            more effective than simply pursuing larger quantities.
matical truth.                                                      Due to the limited variety of operators and homogeneous
Syntactic Accuracy quantifies the formal correctness of             combinations in the training data, the model often fails to
model outputs by measuring their ability to pass automated          handle infrequent or structurally complex problems. To
compiler verification. The overall pass rate is equal to the        address this limitation, we employed three undergraduate
ratio of compiler-valid statements to all problems.                 students to systematically analyze mathematical templates
                                                                    from competition problems and online K12 mathematical
Semantic Accuracy assesses the mathematical equivalence             resources. These templates focus on specific forms and
between formally verified statements and their original natu-       categories of problems, significantly alleviating the scarcity
ral language formulations, following the evaluation protocol        of relevant data.
established in 3.2.3. The semantic scores reported in Table
1 represent the average performance across all problems.            Compared to the limited data variety in Numina, synthetic
Problems that fail to compile are assigned a score of zero.         data significantly enriches training diversity—yielding no-
                                                                    table performance gains by incorporating only 7,000 addi-
As summarized in Table 1, our experimental results demon-           tional problems. However, constrained by template rigid-
strate that the KELPS translator maintains robust perfor-           ity and limited conceptual combinations, further scaling
mance across all evaluation metrics and datasets. Notably,          fails to produce substantial breakthroughs. This limitation
while other models exhibit significant accuracy gaps be-            is particularly evident on competition-level datasets (e.g.,
tween Lean and Isabelle formalizations, the KELPS trans-            FormalMATH), where synthetic data complexity remains in-
lator’s consistent performance confirms its capability for          adequate, resulting in lower performance relative to simpler
cross-formal-language translation.                                  benchmarks. Therefore, future research should prioritize
We also note the outstanding performance of the Herald              enhancing data quality over mere quantity. To achieve this
model on the FormalMATH dataset, which may be attributed            objective, establishing an effective evaluation metric for
to its training on extensive advanced Lean4 statements. We          problem complexity is both essential and urgent.
will delve deeper into this phenomenon in Section 4.4.
                                                                    4.4. Analysis
The results demonstrate that the KELPS translator excels at
formalizing natural language sentences into various formal          In this subsection, we provide an in-depth analysis of the ex-
representations. A case study of the formalization results of       perimental outcomes and identify key factors that influence
the KELPS translator is shown in Appendix C.                        model performance. These factors represent the primary
                                                                    targets for improvement in our subsequent research.
4.3. Ablation Study                                                 Effectiveness of KE Translation: We will discuss the im-
In this subsection, we conduct ablation studies on the syn-         pact of introducing Knowledge Equations. Specifically, the
thetic data approach, primarily investigating the impact of         task of autoformalization can be regarded as an alignment
synthetic data quantity and quality on model performance.           between natural language and formal language.
We compare the results under different configurations. All          Corollary 4.1. This alignment can be further categorized
models were trained using a subset of the KELPS dataset             along the following two dimensions:
containing approximately 15,000 Numina-Basic NL-AL
pairs parsed from Numina combined with various categories                AG(NL, FL) = AGsyn (NL, FL) + AGsem (NL, FL)
of synthetic data. To systematically evaluate the effects, we
controlled two key factors: (1) dataset diversity and quality
                                                                    where AG denotes the overall alignment gap between the
by varying the templates used for synthetic data generation,
                                                                    informal statement (NL) and the formal statement (FL).

                                                                7
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


Table 2. We compare the performance of KELPS trained on datasets of varying scales and composition ratios across different benchmark
datasets, where the ’Dataset ratio’ denotes the proportion of informal data from natural language problems to model-generated synthetic
data in the training corpus.

                                                        MiniF2F              Numina-Hard            FormalMATH
                Dataset Ratio     Dataset Size
                                                  Syntax     Semantic     Syntax    Semantic      Syntax    Semantic
                     1:0              14k         81.6%        3.75       91.7%        4.33       60.1%        2.54
                    1 : 0.5           21k         87.6%        4.08       94.5%        4.51       70.3%        3.14
                     1:1              28k         88.4%        4.08       93.4%        4.49       70.9%        3.25
                    1 : 1.5           35k         88.9%        4.05       94.3%        4.49       74.3%        3.29


AGsyn represents the syntactic alignment gap, while AGsem             5. Conclusion
denotes the semantic alignment gap.
                                                                      In this work, we propose KELPS, a novel three-stage frame-
Corollary 4.2. The term AGsyn primarily depends on the                work for autoformalization. Our method introduces an inter-
syntactic rules and stylistic conventions of the FL. And AGsyn        mediate representation—Knowledge Equation, which trans-
coule be decomposed into two subcomponents                            lates natural language into multiple formal languages. This
    AGsyn (NL, FL) = AGsyn (NL, AL) + AGsyn (AL, FL)                  representation aligns more closely with natural language,
                                                                      thus improving model accuracy, while the expert-crafted
where the AGsyn part can be automatically resolved by our             transformation rules guarantee syntactic correctness.
rule-based parser                                                     We introduce a large-scale parallel dataset comprising over
Table 1 shows AG(NL, FL) varies significantly across for-             60,000 NL-FL pairs spanning distinct mathematical sub-
mal languages, causing DeepSeek-v3’s performance to drop              fields, with multi-language support (Lean, Coq, Isabelle).
from 81% to 56.5% on MiniF2F. In contrast, our method                 Additionally, we propose an LLM-based synthetic data gen-
only requires AG(NL, AL) mapping, thus with relatively                eration strategy that controls difficulty levels and targets
consistent results (88.9% and 82.2%)                                  specific concepts/operators, effectively enhancing data di-
                                                                      versity. Fine-tuning the KELPS translator on this dataset
Quality of Alignment between NL-FL pairs: Since the                   achieved 88.9% syntactic accuracy on the MiniF2F dataset,
semantic verification module that relies on a large language          outperforming SOTA models like Deepseek-V3 81% and
model as a referee is not completely reliable, instances of           Herald 81.3% on MiniF2F.
misalignment between NL and FL persist in the training
dataset. Common misalignment patterns include misinter-               In summary, this work makes three contributions: the de-
pretation of problem semantics and omission of problem-               sign of Knowledge Equations as a novel formal language,
specific constraints.                                                 including its complete BNF specification and parser imple-
                                                                      mentation; the release of KELPS Dataset, a large-scale mul-
Our preliminary experiments revealed that semantically er-            tilingual formal language dataset; and the development of a
roneous data can mislead models to generate incorrect re-             high-performance model that achieves new SOTA accuracy.
sponses. To address this issue, We employed a rigorous                Due to their simplified formalism, Knowledge Equations
manual verification process to curate a high-quality subset           demonstrate strong potential as both an educational and
of 15,000 precisely aligned NL-FL pairs for experiments.              research-oriented formal language, despite limitations in
The Diversity and Coverage of the KELPS Ontology:                     automated type conversion between multiple concepts.
Due to limited time and resources, we only modeled core               In the future, we plan to extend and refine this methodology
mathematical concepts in natural language. While these                along two key dimensions: expanding Knowledge Equa-
atomic concepts are theoretically sufficient to represent most        tions’ coverage to advanced mathematical domains, and
mathematical knowledge, our experiments revealed that the             strengthening its theoretical foundations to address type sys-
model tends to self-construct undefined operators (shown              tem conversion errors. We posit that Knowledge Equations
in Appendix C). These operators failed syntax validation              possess the potential to emerge as a universal, machine-
because of the absence of corresponding transformation                learnable language.
rules.
Therefore, to enhance both the practical utility and expres-          6. Impact Statement
sive power of Knowledge Equations, our future research
will focus on comprehensive semantic modeling of natural              This paper presents work whose goal is to advance the field
language in its entirety.                                             of Machine Learning. There are many potential societal

                                                                  8
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

consequences of our work, none which we feel must be                   Jiang, A. Q., Li, W., and Jamnik, M. Multilingual mathemat-
specifically highlighted here.                                            ical autoformalization. arXiv preprint arXiv:2311.03755,
                                                                          2023.
References                                                             Li, J., Beeching, E., Tunstall, L., Lipkin, B., Soletskyi, R.,
Barras, B., Boutin, S., Cornes, C., Courant, J., Coscoy,                 Huang, S., Rasul, K., Yu, L., Jiang, A. Q., Shen, Z., et al.
  Y., Delahaye, D., de Rauglaudre, D., Filliâtre, J.-C.,                Numinamath: The largest public dataset in ai4maths with
  Giménez, E., Herbelin, H., et al. The coq proof assistant             860k pairs of competition math problems and solutions.
  reference manual. INRIA, version, 6(11):17–21, 1999.                   Hugging Face repository, 13:9, 2024.

Blokpoel, M. mathlib: A scala package for readable, verifi-            Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,
  able and sustainable simulations of formal theory. Journal             C., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-v3
  of Open Source Software, 9(99):6049, 2024.                             technical report. arXiv preprint arXiv:2412.19437, 2024.

Carneiro, M. Lean4lean: Towards a verified typechecker                 Liu, X., Bao, K., Zhang, J., Liu, Y., Chen, Y., Liu, Y.,
  for lean, in lean. arXiv preprint arXiv:2403.14064, 2024.              Jiao, Y., and Luo, T. Atlas: Autoformalizing theo-
                                                                         rems through lifting, augmentation, and synthesis of data.
Cunningham, G., Bunescu, R. C., and Juedes, D. Towards                   arXiv preprint arXiv:2502.05567, 2025.
  autoformalization of mathematics and code correctness:
  Experiments with elementary proofs. arXiv preprint                   Lu, J., Wan, Y., Huang, Y., Xiong, J., Liu, Z., and Guo, Z.
  arXiv:2301.02195, 2023.                                                Formalalign: Automated alignment evaluation for auto-
                                                                         formalization. arXiv preprint arXiv:2410.10135, 2024a.
Ganesalingam, M. The language of mathematics. In The
  Language of Mathematics: A Linguistic and Philosophi-                Lu, J., Wan, Y., Liu, Z., Huang, Y., Xiong, J., Liu, C., Shen,
  cal Investigation, pp. 17–38. Springer, 2013.                          J., Jin, H., Zhang, J., Wang, H., et al. Process-driven auto-
                                                                         formalization in lean 4. arXiv preprint arXiv:2406.01940,
Gao, G., Wang, Y., Jiang, J., Gao, Q., Qin, Z., Xu, T., and              2024b.
  Dong, B. Herald: A natural language annotated lean
  4 dataset. In The Thirteenth International Conference                Moura, L. d. and Ullrich, S. The lean 4 theorem prover
  on Learning Representations, 2025. URL https://                       and programming language. In Automated Deduction–
  openreview.net/forum?id=Se6MgCtRhz.                                   CADE 28: 28th International Conference on Automated
                                                                        Deduction, Virtual Event, July 12–15, 2021, Proceedings
Gonthier, G. et al. Formal proof–the four-color theorem.                28, pp. 625–635. Springer, 2021.
 Notices of the AMS, 55(11):1382–1393, 2008.
                                                                       Patel, N., Saha, R., and Flanigan, J. A new approach towards
Gordon, M. From lcf to hol: a short history. In Proof,                   autoformalization. arXiv preprint arXiv:2310.07957,
  language, and interaction, pp. 169–186. Citeseer, 2000.                2023.

Grabowski, A., Kornilowicz, A., and Naumowicz, A. Mizar                Pathak, S. Gflean: An autoformalisation framework for lean
  in a nutshell. Journal of Formalized Reasoning, 3(2):                  via gf. arXiv preprint arXiv:2404.01234, 2024.
  153–245, 2010.                                                       Paulson, L. C. Isabelle: A generic theorem prover. Springer,
                                                                         1994.
Huang, Y., Lin, X., Liu, Z., Cao, Q., Xin, H., Wang, H.,
  Li, Z., Song, L., and Liang, X. Mustard: Mastering uni-              Ranta, A. Grammatical framework. Journal of Functional
  form synthesis of theorem and proof data. arXiv preprint               Programming, 14(2):145–189, 2004.
  arXiv:2402.08957, 2024.
                                                                       Scholze, P. Liquid tensor experiment. Experimental Mathe-
Humayoun, M. and Raffalli, C. Mathnat-mathematical text                  matics, 31(2):349–354, 2022.
  in a controlled natural language. Special issue: Natural
  Language Processing and its Applications, 46:293–307,                Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,
  2010.                                                                  H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Push-
                                                                         ing the limits of mathematical reasoning in open language
Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J., Jamnik,         models. arXiv preprint arXiv:2402.03300, 2024.
   M., Lacroix, T., Wu, Y., and Lample, G. Draft, sketch,
   and prove: Guiding formal theorem provers with informal             Trybulec, A. Tarski grothendieck set theory. Journal of
   proofs. arXiv preprint arXiv:2210.12283, 2022.                        Formalized Mathematics, 1, 1989.

                                                                   9
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q.,
 Huang, Y., Xiong, J., Shi, H., Xie, E., et al. Lego-prover:
 Neural theorem proving with growing libraries. arXiv
 preprint arXiv:2310.00656, 2023.
Wang, Q., Kaliszyk, C., and Urban, J. First experiments
 with neural translation of informal to formal mathematics.
 In Intelligent Computer Mathematics: 11th International
 Conference, CICM 2018, Hagenberg, Austria, August 13-
 17, 2018, Proceedings 11, pp. 255–270. Springer, 2018.
Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., and
 Zhang, T. Theoremllama: Transforming general-purpose
 llms into lean4 experts. arXiv preprint arXiv:2407.03203,
 2024.
Wu, W.-T. Mathematics mechanization: mechanical ge-
 ometry theorem-proving, mechanical geometry problem-
 solving, and polynomial equations-solving. Kluwer Aca-
 demic Publishers, 2001.

Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jam-
 nik, M., and Szegedy, C. Autoformalization with large
 language models. Advances in Neural Information Pro-
 cessing Systems, 35:32353–32368, 2022.
Wu, Z., Wang, J., Lin, D., and Chen, K. Lean-github:
 Compiling github lean repositories for a versatile lean
 prover. arXiv preprint arXiv:2407.17227, 2024.
Xin, H., Li, L., Jin, X., Fleuriot, J., and Li, W. Ape-bench i:
  Towards file-level automated proof engineering of formal
  math libraries. arXiv preprint arXiv:2504.19110, 2025.

Ying, H., Wu, Z., Geng, Y., Wang, J., Lin, D., and Chen,
  K. Lean workbook: A large-scale lean problem set for-
  malized from natural language math problems. arXiv
  preprint arXiv:2406.03847, 2024.
Yu, Z., Peng, R., Ding, K., Li, Y., Peng, Z., Liu, M.,
  Zhang, Y., Yuan, Z., Xin, H., Huang, W., et al. Formal-
  math: Benchmarking formal mathematical reasoning of
  large language models. arXiv preprint arXiv:2505.02735,
  2025.
Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  benchmark for formal olympiad-level mathematics. arXiv
  preprint arXiv:2109.00110, 2021.
Zhou, J. P., Staats, C., Li, W., Szegedy, C., Weinberger,
  K. Q., and Wu, Y. Don’t trust: Verify–grounding llm
  quantitative reasoning with autoformalization. arXiv
  preprint arXiv:2403.18120, 2024.
Zhou, Y. From first-order logic to assertional logic. In In-
  ternational Conference on Artificial General Intelligence,
  pp. 87–97. Springer, 2017.


                                                                  10
          KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


                                           Table 3. Representative Ontology Examples

                          Domain        Concept            Operator
                                                           Abs, Sqrt, Log, NaturalLog, Sqrt, Cos, Sin,
                                        Real
                                                           Tan, Get Number Round, Exp, Is Real
                                                           Get GCD, Is OddNumber, Get Remainder,
                          Numbers       Integers
                                                           Get InversedMod, Get LCM,
                                                           Factorial, Get Combination, Is Coprime,
                                        NaturalNumbers     Is Prime, Get Digit Number, Get DigitSum,
                                                           Get DigitProduct, Get DigitCount
                                                           Get PolyTerm, Is PolyFactor, Get Polyroots,
                          Polynomial    Polynomial
                                                           Get PolyDegree, Get Term Coefficient,
                                                           Get Function Range, Get Function Zeroes,
                          Function      Function           Get Inverse Function, Get Function Value,
                                                           Get Function Minimum, Is Bijection
                                                           Set Cardinality, Set Union, Set Difference,
                          Set           Set                Set Intersection, Build Set, Get Set Sum,
                                                           Get Set Maximum, Get Set Minimum
                                                           Is GeometricSequence, Get CommonRatio,
                          Sequence      Sequence           Is ArithmeticSequence, Get Sequence Sum,
                                                           Get CommonDifference
                                                           ForAll, Exists, Get Prod, Solve equation,
                          Special       ——–
                                                           Get Sum , Negation, Range



Appendix
A. Ontology Examples.
The complete ontology comprises only 40 concepts, 180 operators, and 6 thematic topics. In table 3, we present representative
samples of core concepts and corresponding operators across topics. The full content can be accessed in our materials.
Our method incorporates the core concepts and operations from these fields. Although some concepts are not directly
covered in the ontology library, they can essentially be derived through combinations of our existing operators. This
demonstrates the simplicity and expressive power of the knowledge equation.
In the future, we will further expand the coverage of our ontology library to support more complex mathematical reasoning.
Our plan primarily includes: (1) Completing the ontology library to support geometric and statistical visual reasoning,
and (2) Incorporating foundational undergraduate mathematics, such as abstract algebra, mathematical analysis,
and topology. We hope that KE can provide resources and novel insights for future research in autoformalization and
theorem proving.


                                        Table 4. Hyperparameters in all the experiments.

                                       Type           Parameter                     Value
                                       SFT Training   Batch Size                      512
                                                      Learning Rate              2.0e − 5
                                                      Learning Rate Scheduler      Cosine
                                                      Warm-up Ratio                  0.01
                                                      Optimizer                  AdamW
                                                      Epoch                            15
                                       Evaluation     Top-p                            0.9
                                                      Temperature                       0.7
                                                      Max tokens                       512

                                                              11
          KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

  Instruction:
  You are an expert in the Isabelle theorem prover. Your task is to translate theorems from natural language into formal
  Isabelle statements. Please follow these guidelines:

    1. Carefully analyze the given theorem in natural language.

    2. Translate it into a correct and precise Isabelle formal statement.
    3. Use the following format for your response:
       theorem tm name :
       fixes 〈variable〉
       assumes "〈hypothesis〉"
       shows "〈statement〉"
       sorry
    4. Focus solely on the translation. Do not attempt to prove the theorem or provide additional explanations.
    5. Ensure that your translation accurately captures all the mathematical concepts and relationships expressed in the
       natural language version.

    6. Use appropriate Isabelle syntax, including correct use of quantifiers, implications, and mathematical symbols.
    7. If the theorem involves specific mathematical structures (e.g., groups, rings, topological spaces), use the corre-
       sponding Isabelle definitions and notations.
    8. Do not include any proofs, use sorry as a placeholder. Do not add any explanations.

  The goal is to produce a syntactically correct and semantically accurate formalization in Isabelle. Your translation
  should faithfully reflect the meaning of the original theorem while following Isabelle conventions and best practices.


                              Figure 3. Instructions for Translating Natural Language into Isabelle


B. Experiments.
B.1. Training Details
We take a fully fine-tuning setting for training DeepSeek-Math-7B-Base as the base model. All training experiments are
conducted on 4 NVIDIA A100 GPUs with LLaMA-Factory framework. Detailed hyperparameters utilized for training and
evaluation experiments are documented in Table 4.

B.2. Prompt Details
In this section, we present all the prompts used in this work to facilitate progress. The correspondence between all prompt
examples and the tables is shown below.

  • Fig 3, Fig 4, Fig 5 and Fig 6, Fig 7, Fig 8 present the prompts used to translate natural language to Lean, Coq, and
    Isabelle respectively, with examples randomly sampled from our parallel dataset.
  • Fig 9 outlines the prompt used to verify the semantic accuracy of KE during our validation phase.
  • Fig 10 outlines the prompt used to guide the large language model to perform data synthesis, with templates randomly
    selected from our template library.




                                                              12
        KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Instruction:
You are an expert in the Lean4 theorem prover. Your task is to translate theorems from natural language into formal
Lean4 statements. Please follow these guidelines:

  1. Carefully analyze the given theorem in natural language.

  2. Translate it into a correct and precise Lean4 formal statement.
  3. Use the following format for your response:
     theorem tm name : <Lean4 formal statement> := by sorry
  4. Focus solely on the translation. Do not attempt to prove the theorem or provide any explanations.

  5. Ensure that your translation accurately captures all the mathematical concepts and relationships expressed in the
     natural language version.
  6. Use appropriate Lean4 syntax, including correct use of quantifiers, implications, and mathematical symbols.
  7. If the theorem involves specific mathematical structures (e.g., groups, rings, topological spaces), use the corre-
     sponding Lean4 definitions and notations.

  8. Do not include any proofs, use sorry as a placeholder. Do not add any explanations.

The goal is to produce a syntactically correct and semantically accurate formalization in Lean4. Your translation should
faithfully reflect the meaning of the original theorem while following Lean4 conventions and best practices.


                             Figure 4. Instructions for Translating Natural Language into Lean




Instruction:
You are an expert in the Coq theorem prover. Your task is to translate theorems from natural language into formal Coq
statements. Please follow these guidelines:

  1. Carefully analyze the given theorem in natural language.

  2. Translate it into a correct and precise Coq formal statement.
  3. Use the following format for your response:
     Theorem tm name : <Coq formal statement>.                            Proof.        Admitted.
  4. Focus solely on the translation. Do not attempt to prove the theorem or provide additional explanations.

  5. Ensure that your translation accurately captures all the mathematical concepts and relationships expressed in the
     natural language version.
  6. Use appropriate Coq syntax, including correct use of quantifiers, implications, and mathematical symbols.
  7. If the theorem involves specific mathematical structures (e.g., groups, rings, topological spaces), use the corre-
     sponding Coq definitions and notations.
  8. Do not include any proofs, use Admitted as a placeholder. Do not add any explanations.

The goal is to produce a syntactically correct and semantically accurate formalization in Coq. Your translation should
faithfully reflect the meaning of the original theorem while following Coq conventions and best practices.


                             Figure 5. Instructions for Translating Natural Language into Coq

                                                            13
        KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


id: 1

-- Problem: Find all solutions to the equation \sqrt[3]{3 - \frac{x}{3}} = -2.

--lean_theorem:
theorem Unexplored_1 :
    { (x : R ) | ( 3 - x / 3 ) ˆ ( 1 / 3 ) = -2 } = sorry
    := by sorry

--coq_theorem:
Theorem Test_1 :        { x : R} | 1 / (x - 2) < 3 / x } = sorry.
    Proof.
    Admitted.

--Isabelle_theorem:
theorem Test_1 :
    shows "{ x :: real . 1 / (x - 2) < 3 / x } = sorry" sorry

id: 2

-- Problem: Given the function f(x) = |1 - 2x| - |1 + x|. Solve the inequality f(x) ≥
    4.

--lean_theorem:
theorem Unexplored_2 :
    { x : R | |1 - 2 * x| - |1 + x| ≥ 4 } = sorry
    := by sorry

--coq_theorem:
Theorem Test_2 :
    { x : R | (Rabs (1 - 2 * x) - Rabs (1 + x)) >= 4 } = sorry.
    Proof.
    Admitted.

--Isabelle_theorem:
theorem Test_2 :
    shows "{x :: real. abs (1 - 2 * x) - abs (1 + x) ≥ 4} = {}"
    sorry

id: 3

-- Problem: If sequence A is an arithmetic sequence with A(1)=3, A(2)=6; find A(5)

--lean_theorem:
theorem Unexplored_3 (A : N → R)
    (h1 : ∃ d : R, ∀ n : N, A (n + 1) = A n + d)
    (h2 : A 1 = 3)
    (h3 : A 2 = 6) :
    A 5 = 15 := by sorry

--coq_theorem:
Theorem Test_3 (A : nat → R)
    (h1 : exists d, forall n, A (S n) = A n + d)
    (h2 : A 1%nat = 3)
    (h3 : A 2%nat = 6) :
    A 5%nat = 15.
Proof.
Admitted.



                   Figure 6. Few Shots for Translating Natural Language into Formal Language (Part I).



                                                           14
        KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


--Isabelle_theorem:
theorem Test_3 :
    fixes A :: "nat ⇒ real"
    assumes h1: "∃d. ∀n. A (n + 1) = A n + d"
        and h2: "A 1 = 3"
        and h3: "A 2 = 6"
    shows "A 5 = 15"
    sorry

id: 4

-- Problem: If Set M = {1, 3, 5}, Set N = {2, 3, 4}. Find the union of M and N.

--lean_theorem:
theorem Unexplored_4 (M N : Set R)
    (h1 : M = {1, 3, 5})
    (h2 : N = {2, 3, 4}) :
    M ∪ N = {1, 2, 3, 4, 5} := by sorry

--coq_theorem:
Theorem Test_4 (M N : Ensemble R)
    (h1 : M = [1; 3; 5])
    (h2 : N = [2; 3; 4]) :
    Union M N = [1; 2; 3; 4; 5].
Proof.
Admitted.

--Isabelle_theorem:
theorem Test_4 :
    fixes M N :: "real set"
    assumes h1: "M = {1, 3, 5}"
        and h2: "N = {2, 3, 4}"
    shows "M ∪ N = {1, 2, 3, 4, 5}"
    sorry

id: 5

-- Problem: Solve the following equation: 5(1 - cos x) = 4 sin x

--lean_theorem:
theorem Unexplored_5 :
    {x : R | 5 * (1 - Real.cos x) = 4 * Real.sin x} = sorry := by sorry

--coq_theorem:
Theorem Test_5 :
    {x : R | 5 * (1 - cos x) = 4 * sin x} = sorry.
Proof.
Admitted.

--Isabelle_theorem:
theorem Test_5 :
    shows "{x :: real. 5 * (1 - cos x) = 4 * sin x} = {}"
    sorry



                  Figure 7. Few Shots for Translating Natural Language into Formal Language (Part II).




                                                          15
        KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment


id: 6

-- Problem: Given that x, y, z are positive real numbers with product xyz = 1,
-- show that the inequality holds

--lean_theorem:
theorem Unexplored_6 (x y z : R)
    (hx : x > 0) (hy : y > 0) (hz : z > 0)
    (h1 : x * y * z = 1) :
    xˆ3 / ((1 + y) * (1 + z)) +
    yˆ3 / ((1 + z) * (1 + x)) +
    zˆ3 / ((1 + x) * (1 + y)) ≥ 3/4 := by sorry

--coq_theorem:
Theorem Test_6 (x y z : R)
    (hx : x > 0) (hy : y > 0) (hz : z > 0)
    (h1 : x * y * z = 1) :
    (xˆ3 / ((1 + y) * (1 + z)) +
     yˆ3 / ((1 + z) * (1 + x)) +
     zˆ3 / ((1 + x) * (1 + y))) >= 3/4.
Proof.
Admitted.

--Isabelle_theorem:
theorem Test_6 :
    fixes x y z :: real
    assumes hx: "x > 0" and hy: "y > 0" and hz: "z > 0"
        and h1: "x * y * z = 1"
    shows "xˆ3 / ((1 + y) * (1 + z)) +
           yˆ3 / ((1 + z) * (1 + x)) +
           zˆ3 / ((1 + x) * (1 + y)) ≥ 3/4"
    sorry



                  Figure 8. Few Shots for Translating Natural Language into Formal Language (Part III).




                                                           16
       KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Instruction:
You are an expert in Lean4 language and natural language. When given a math problem described in natural language
and a math problem described in Lean4 language, your task is to evaluate the consistency of the two math problems
and score them.
Scoring Rules:
 1. The full score is 5 points and the lowest score is 0.

 2. When the semantics of all statements of the two math problems are consistent, give full marks of 5 points.
 3. For each inconsistent statement, deduct 1 point until 0 points.
Response Format:

  • Reply with ||your points|| in the final sentence
  • Use the exact ”——” format for the score
Input Format:
math problem described in natural language:
<ORIGINAL MATH PROBLEM>

math problem described in Lean4 language:
<LEAN4 MATH PROBLEM>
Output Format:
<SEMANTIC CONSISTENCY SCORE>


                                  Figure 9. Prompt for Semantic Consistency Judgment




                                                            17
         KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

Instruction:
You are an expert at creating integrated math problems combining multiple concepts. When provided with knowledge
K of operators and concepts, and labeled examples E, your task is to return complex math problems and their labeled
results.
Rules:
 1. Never use any new concepts or operators except those in the context!

 2. Do not include any explanatory text.
 3. Strictly follow the style of the context.
 4. Combine the provided fragments effectively to create complex mathematical problems or proofs.

 5. Return exactly 10 results in the specified format.
Output Format:
Problem: <problem statement>
Declaration: <required declarations>
Facts: <supporting facts>
Query: <specific question>
Input:
knowledge K:
## Concepts ##
<EXPLANATION OF CONCEPTS IN K>

## Operators ##
<EXPLANATION OF OPERATORS IN K>

labeled examples E:
<EXAMPLES OF LABELING MATH PROBLEMS>
Output:
<10 LABELED MATH PROBLEMS>


                              Figure 10. Prompt for Data Synthesis about Sequence Questions




                                                           18
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

   MiniF2F T29. Show that there exist real numbers a and b such that a is irrational, b is irrational, and ab is rational.



   theorem Unexplored_29
       (a : R)(h_a : Irrational a)
       (b : R)(h_b : Irrational b)
       : a ˆ b ∈ Q
       := sorry



Figure 11. A formalization of MiniF2F T29 in Lean 4. ab ∈ Q follows natural language conventions, it constitutes invalid syntax in
Lean4. We note that the problem’s formalization also contains inaccuracies, though our present focus remains on syntactic errors in this
subsection.




C. Case Study.
This section analyzes common error cases in KELPS translation results, providing a detailed examination of frequent
grammatical and semantic issues. Generally, grammatical rules are relatively limited, resulting in a narrower range of error
types. In contrast, ensuring semantic consistency often proves more challenging.

C.1. Syntax Errors
Grammar Errors. This might be because the model didn’t see enough formal examples, or perhaps there is a discordance
between formal language syntax rules and typical organic natural language patterns. A representative example is illustrated
in Figure 11, where the expression q ∈ Q, though common and clear in natural language, is not valid in formal syntax. The
model may also adopt natural language shortcuts or formats in formal expressions (Figure 12). This could trace back to the
model’s exposure to abundant informal content during pre-training, while having relatively limited contact with formalized
materials.
Type Errors. These errors primarily occur because, in natural language, a number/object often belongs to multiple types
simultaneously, while the informal statement may be insufficient to determine its unique specific type. Generally, Lean4
supports automatic type inference, except for certain specific cases (see Figure 13). In contrast, more rigorous formal
systems like Coq typically require explicit type declarations in formal statements. Version differences can also trigger such
issues. Therefore, file-level (rather than theorem-level) autoformalization is essential for future research.

C.2. Semantic Errors
Misunderstanding about Informal Statement. The process of formalizing natural language math problems presents
varying levels of difficulty. Since some problems lack explicit mathematical declarations and assumptions, their formal-
ization requires first parsing the natural language semantics and then abstracting mathematical content through modeling.
Unfortunately, current mainstream large language models still exhibit limitations in natural language understanding. The
representative example in Figure 14 shows how models lose accuracy when faced with indirect statements.
Misalignment with Informal Statement. Other prevalent error patterns comprise omission of critical information (Fig 15)
and inconsistencies with the informal statement (Fig 16). These resemble human students’ typos in writing solutions, thus
being nearly unavoidable. However, these relatively minor errors are theoretically preventable through self-correction and
secondary checking.

                                                                  19
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

   FormalMath T452. Find all positive integers a, b, c such that ab + 1, bc + 1, and ca + 1 are all equal to factorials of
   some positive integers. Prove that the answer is: (k! − 1, 1, 1) (and its permutations), where k ∈ N>1 .



   Declarations: "a: PositiveIntegers; b: PositiveIntegers; c: PositiveIntegers"

   Facts: "a * b + 1 = Factorial(k); b * c + 1 = Factorial(k); c * a + 1 = Factorial(k)"

   Query: "(a, b, c) = (k! - 1, 1, 1)",



Figure 12. A formalization of FormalMath T452 in Knowledge Equations. While the notation k! clearly denotes the factorial function
in human-readable mathematics, it fails to comply with the syntactic requirements of Knowledge Equations. Therefore, it fails to be
translated into Lean4.




                                     −1
   MiniF2F T111. Solve for a: 84−1 − a−1 = 1. Show that it is -2.



   theorem Unexplored_111
       (a : R) (h1 : ( 8 : R ) ˆ ( -1 ) / ( 4 : R ) ˆ ( -1 ) - (a) ˆ (-1: R) = 1)
       : a = -2 := by sorry



Figure 13. A formalization of MiniF2F T111 in Lean4. The expression appears almost correct. However, the exponent (−1) in (8 : R)(−1)
is not explicitly declared as a real number, causing Lean4 to default its type to N during computation and resulting in a type mismatch.

                                                                  20
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

   MiniF2F T198. What digit must be placed in the blank to make the four-digit integer 20 7 a multiple of 11? Show that
   it is 5.


   theorem Unexplored_198
       (d : Z) (h1 : 2057 % 11 = 0)
       (h2 : 2067 % 11 = 0) (h3 : 2077 % 11 = 0)
       (h4 : 2087 % 11 = 0) (h5 : d = 5)
       : 2097 % 11 = 0 := by sorry



Figure 14. A formalization of MiniF2F T198 in Lean4. While the generated formal statement is syntactically correct, the model fails to
capture the authentic mathematical intent of the problem, consequently producing erroneous results.




   MiniF2F T204. Notice that 35 · 40 = 1400 Find some integer n with 0 ≤ n < 1399 such that n is the multiplicative
   inverse to 160 modulo 1399. Show that it is 1058.


   theorem Unexplored_204
       (n : Z) (h1 : 0 <= n)
       (h2 : 35 * 40 = 1400) (h3 : n < 1399)
       : n = 1058 := by sorry



Figure 15. A formalization of MiniF2F T204 in Lean4. Although the existing content is correct, the model missed the condition that n is
the multiplicative inverse to 160 modulo 1399. This renders the problem unsolvable under the given constraints.

                                                                  21
           KELPS: A Framework for Verified Multi-Language Autoformalization via Semantic-Syntactic Alignment

                                                     32
  MiniF2F T155. If a and b are real numbers, a2 b3 = 27 , and ba3 = 27                                 8
                                                                    4 , what is a + b? Show that it is 3 .




  theorem Unexplored_155
      (a : R) (b : R)
      (h1 : a / ( b ˆ 3 ) = 27 / 4) (h2 : a * ( b ˆ 3 ) = 32 / 27)
      : a + b = 8 / 3 := by sorry



Figure 16. A formalization of MiniF2F T155 in Lean4. The model incorrectly substituted a for a2 , resulting in misalignment with the
informal statement.




                                                                22
