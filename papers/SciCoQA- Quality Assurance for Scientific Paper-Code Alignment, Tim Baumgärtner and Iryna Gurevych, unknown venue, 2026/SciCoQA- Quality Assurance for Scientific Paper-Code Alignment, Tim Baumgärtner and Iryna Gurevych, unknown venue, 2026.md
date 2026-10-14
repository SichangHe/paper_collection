                                                 S CI C O QA: Quality Assurance for Scientific Paper–Code Alignment

                                                                    Tim Baumgärtner and Iryna Gurevych
                                                 Ubiquitous Knowledge Processing Lab (UKP Lab), Department of Computer Science,
                                                  TU Darmstadt and National Research Center for Applied Cybersecurity ATHENE

                                                                            Code: https://github.com/ukplab/scicoqa
                                                                            Data: https://hf.co/datasets/ukplab/scicoqa
                                                                            Blog: https://ukplab.github.io/scicoqa


                                                                                                     Paper                                                      def forward(self, x):    Code
                                                                   Abstract                                   We feed λ to two MLPs Mσ and Mμ to generate
                                                                                                              two, σ and μ, of dimensionality C each. We then     m = self.mu(x)
                                                                                                              multiply the feature map channel-wise by σ          s = self.sigma(x)
                                                                                                                                                                  return F.sigmoid(m),
                                                                                                                                                                                          =

                                                                                                              and add μ to get the transformed feature map:
                                                 Discrepancies between scientific papers and
                                                                                                                                                                                              =
arXiv:2601.12910v3 [cs.CL] 22 Apr 2026




                                                                                                                    fijk
                                                                                                                      ̃ = σkfijk + μk, σ = Mσ(λ), μ = Mμ(λ)         F.sigmoid(s)              =   +




                                                 their code undermine reproducibility, a con-
                                                 cern that grows as automated research agents         Discrepancy: The paper conditions layers using FiLM by mapping
                                                                                                      the loss-parameter vector λ through two MLPs to obtain σ and μ and
                                                 scale scientific output beyond human review          then applying the afﬁne transform f ̃ = σ ⊙ f + μ; [...]. In the repo-
                                                 capacity. Whether LLMs can reliably detect           sitory, the FiLMBlock applies a sigmoid activation to both μ and σ
                                                 such discrepancies has not been systematically       before using them, thereby constraining both to the (0,1) range. […]
                                                 measured. To this end, we present S CI C O QA,
                                                 a dataset of 635 paper-code discrepancies (92       Figure 1: Example from S CI C O QA, showing a specific
                                                 real, 543 synthetic) for this cross-modal verifi-   model implementation in the paper and its implementa-
                                                 cation task. Across 22 evaluated models, even       tion in the code (simplified for readability). The paper’s
                                                 the best-performing LLMs, Gemini 3.1 Pro and        description and the code’s implementation mismatch,
                                                 GPT-5 Mini, detect only 46.7% of real-world         creating a paper-code discrepancy.
                                                 discrepancies, revealing a critical gap in au-
                                                 tomated scientific quality assurance. We con-
                                                 struct S CI C O QA from GitHub issues and repro-    discrepancies manifest in troubling ways: from
                                                 ducibility papers, and propose a synthetic gen-     “mathiness,” where equations simulate technical
                                                 eration pipeline to scale beyond AI to Physics,     depth while actual gains stem from undocumented
                                                 Quantitative Biology, and other computational       tricks (Lipton and Steinhardt, 2019), to evaluation
                                                 sciences. We further introduce a taxonomy of
                                                                                                     metrics that differ in implementation (Post, 2018;
                                                 discrepancy types and categories to character-
                                                 ize the occurring mismatches. Our analysis          Marie et al., 2021), rendering scientific compar-
                                                 shows that models particularly struggle with        isons invalid.
                                                 omitted paper details, long-context inputs, and        Reproducibility issues and paper-code inconsis-
                                                 papers outside their pre-training corpus. 1         tencies are typically only detected during repro-
                                                                                                     duction efforts and post-publication, resulting in
                                         1       Introduction
                                                                                                     a waste of resources and eroding trust in science.
                                         The “reproducibility crisis” in AI and across sci-          While checklists during peer review can encourage
                                         ence casts doubt on the reliability of research             authors to provide more reproducible code (Pineau
                                         (Baker, 2016; Hutson, 2018). To address this, the           et al., 2021; Dodge et al., 2019), ideally, reviewers
                                         computational sciences have long recognized that a          check the correctness of the implementation and
                                         paper alone is insufficient and that publishing code,       ensure reproducibility. However, with the rapid
                                         data, and instructions is a prerequisite to ensure          growth of submission numbers, reviewers are al-
                                         experimental findings are reproducible (Buckheit            ready under severe time pressure (Rogers and Au-
                                         and Donoho, 1995; Peng, 2011; Raff, 2019; Pineau            genstein, 2020) and conducting intricate code re-
                                         et al., 2021). However, the availability of code guar-      views is time-consuming (Collberg and Proebsting,
                                         antees neither reproducibility nor consistency with         2016).
                                         the scientific text (as showcased in Fig. 1). In prac-         Furthermore, the reliance on manual review is
                                         tice, implementation details can diverge from their         becoming increasingly impractical as science be-
                                         descriptions, introducing performance variations            gins to scale via agentic systems that develop ideas,
                                         that go unreported (Henderson et al., 2018). These          generate and execute code, and produce scientific
                                             1
                                            Data also available at: https://tudatalib.ulb.           articles autonomously (Boiko et al., 2023; Lu et al.,
                                         tu-darmstadt.de/handle/tudatalib/4994                       2024; Tang et al., 2025; Weng et al., 2026; Lu
et al., 2026), a trend recently exemplified by peer-     Xi et al. (2025) propose dedicated pipelines that
reviewed acceptance to an ICLR workshop (Ya-             generate modifications to papers, invalidating their
mada et al., 2025). While this direction has the         key claims. They evaluate whether the soundness
potential to accelerate scientific discovery, it makes   score of generated reviews decreases or whether
oversight increasingly challenging as humans can-        LLMs can spot these errors. Both find that LLMs
not verify the rapidly expanding volume of output        struggle to detect most introduced errors. Besides
(Bowman et al., 2022). Moreover, the faithfulness        constructing erroneous papers, recent research fo-
of these systems is not guaranteed as LLMs suffer        cuses on identifying real-world issues. Specifically,
from limited context (Liu et al., 2024b), experience     Son et al. (2025) and Zhang and Abernethy (2025)
compounding errors (Dziri et al., 2023; Mirzadeh         use the authors’ retraction notes from WithdrarXiv
et al., 2025), and struggle with independent self-       (Rao et al., 2024) and PubPeer to obtain faulty
correction (Tyen et al., 2024; Wu et al., 2024). Con-    papers. While realistic, these notes are often un-
sequently, ensuring the reliability of science at this   specific (e.g., “Theorem 2 is incorrect”). Recently,
scale demands automated tools capable of verify-         Bianchi et al. (2025) developed a system to detect
ing that the code faithfully implements the methods      inconsistencies within the text of AI papers (e.g.,
reported in the scientific paper.                        incorrect calculations in tables or errors in equa-
   To this end, we introduce S CI C O QA, the first      tions) and then manually verified the detections.
benchmark for detecting discrepancies between sci-       They found their system to be relatively precise
entific papers and their code as a cross-modal ver-      but to struggle with recall, i.e., detecting all issues
ification task. Benchmarking LLMs on this task           in a paper. They also noted an increasing trend
allows us to measure their potential for automated       of errors in scientific publications over the years,
quality assurance workflows in science. To con-          highlighting the importance of quality assurance in
struct our dataset, we leverage issues reported in       science.
code repositories and papers dedicated to repro-            While these works share a similar spirit to ours,
ducing existing work, such as those from repro-          i.e., identifying errors in science, they are limited
ducibility challenges and conference tracks. While       by solely analyzing the paper. S CI C O QA extends
these sources are realistic and of high quality, they    beyond the scientific text and considers the code as
are sparse and limited to CS and AI. Therefore,          well, enabling the detection of cross-modal error
we scale the data to various computational science       types, such as implementations that deviate from
domains (e.g., Physics and Quantitative Biology)         the paper description or omissions in the paper
by generating modifications in codebases, creating       or the code that are crucial for understanding and
discrepancies between the paper and its implemen-        reproducibility. Conceptually, our task can be
tation. Finally, we benchmark open-weight and            viewed as a form of cross-modal claim verification
proprietary LLMs to determine whether current            (Thorne et al., 2018; Wadden et al., 2020), where
systems can be deployed for detecting paper-code         the evidence source is a codebase rather than
discrepancies. Our evaluation reveals that the best-     text. Furthermore, S CI C O QA utilizes constructed
performing models, while precise in identifying          errors to scale the quantity and diversity in
discrepancies, suffer from insufficient recall. The      the computational science domain, while also
best models in our evaluation detect only 46.7% of       providing challenging real-world discrepancies
real-world cases, highlighting the need to develop       between paper and code.
more effective models and systems for this critical
task.                                                    Code-Comment Inconsistency Our task is also
                                                         related to Code-Comment Inconsistency (CCI) de-
2   Related Work                                         tection, where natural language comments that no
                                                         longer match a piece of code need to be identified,
Error Detection in Science Recently, LLMs                e.g., after adding a feature to a function. Early CCI
have been employed to detect errors in scientific        research relied on rule-based systems to identify
papers. Early work created short CS papers with          outdated comments (Ratol and Robillard, 2017).
logical errors and prompted LLMs to identify the         Subsequently, bi-encoders and cross-encoders have
issues (Liu and Shah, 2023). However, their re-          been employed (Rabbi and Siddik, 2020; Steiner
liance on manually crafted papers limits scalabil-       and Zhang, 2022). Panthaplackel et al. (2021) fur-
ity. Therefore, Dycke and Gurevych (2026) and            ther extended CCI to dynamic settings, learning
       Extract reported                             Filter invalid                   Verify discrepancy with original
       paper-code discrepancies                     discrepancies                    paper + code and rephrase


                     GPT-5                              Human                                        Gemini 3.1
                                                                                                      + GPT 5
                                                                 “... while the original
                      “We found the imple-                      “We found the imple-
Reproducibility       mentation of the eval is
                                                                 paper says X, the code
                                                                mentation of the eval is                 “The paper states using
    Papers                                                       actually implements Y”
                      different in their code”                  different in their code”                 macro f1, but the code
                                                                                                         actually implements …”


                     Issue #12
                     “The code implements
 Identify issues    an additional loss…”
                                                      GPT-5
 reporting paper-                                                 “Equation 1 uses L2 norm, but
 code discrepancies                                               the code implements L1 norm”                     Real
                                                                  >>>>>>> ORIGINAL
                                              Generate code       def normalize(v):
                                            changes creating        return v/np.sqrt(np.sum(v**2))              Synthetic
                     Qwen3                                        =======
                                      synthetic discrepancies     def normalize(v):                             ML, CV, NLP
                                                                    return v/np.sum(np.abs(v))
   Scientific                                                     <<<<<<< MODIFIED                        Ph, Math, Q-Bio, Stat, EE
  Repositories

Figure 2: Overview of the data collection process of S CI C O QA. We source real-world data from reproducibility
papers and GitHub issues. For the former, paper-code discrepancies are extracted from the paper with GPT-5, for
the latter, issues are pre-filtered using Qwen3. Next, all candidates are manually filtered to remove any that do not
fit our discrepancy definition. Finally, all paper-code discrepancies are verified with Gemini 3.1 and GPT-5. For
synthetic data, we generate discrepancies using GPT-5 for AI and other computational domains.


to detect inconsistency arising from code updates.               runs (Weng et al., 2026; Xiang et al., 2025), or as-
Recently, LLMs have been deployed for both de-                   sign reproducibility scores based on execution out-
tection and rectification (Dau et al., 2024; Rong                comes (Siegel et al., 2024; Hu et al., 2025; Ye et al.,
et al., 2025). These methods deal with local and                 2025). Critically, these metrics can be mislead-
small inputs, typically taking a single function and             ing; a generated codebase may execute perfectly
an inline comment or docstring as input to detect                and achieve high performance while implementing
the CCI. S CI C O QA is substantially more ambi-                 a method that differs fundamentally from the pa-
tious: it requires performing a global alignment by              per’s scientific description (Beel et al., 2025). S CI -
reasoning over a dense scientific paper and a long,              C O QA addresses this gap by providing a ground
multi-file code repository to find inconsistencies.              truth dataset of paper-code discrepancies, enabling
                                                                 the development of robust quality assurance models
Science Automation Automation in science is                      that can verify the faithfulness of (generated) pa-
rapidly accelerating (Zheng et al., 2025). Early                 pers to (generated) code. More broadly, while code
work targeted specific components of the research                benchmarks in both software engineering (Jimenez
cycle, including ideation (Si et al., 2025; Baek et al.,         et al., 2024) and science (Tian et al., 2024) pre-
2025), literature review (Wang et al., 2024; Liang               dominantly evaluate code generation, S CI C O QA
et al., 2025), coding (Tian et al., 2024; Gandhi et al.,         evaluates the complementary task of code compre-
2025), and writing (Liang et al., 2024; Weng et al.,             hension and verification against a scientific spec-
2025). A recent trend involves generating entire                 ification. Thus, S CI C O QA takes a step toward
code repositories from a paper (Starace et al., 2025;            verification and reproducibility tooling essential
Seo et al., 2026; Xiang et al., 2025) or automat-                for sustaining peer review integrity and science at
ing the scientific method end-to-end, giving rise                scale (Wei et al., 2025b; Woodruff et al., 2026; You
to “AI Scientists.” However, for both these tasks,               et al., 2026).
validating whether the generated code faithfully re-
flects the paper is challenging. For example, Paper-
Bench (Starace et al., 2025) relies on high-quality,             3     S CI C O QA
but expensive, manual rubrics specific to each pa-
per to verify implementation nuances. Others use                 The objective of the S CI C O QA task is to identify
generic LLM-judges without ground truth valida-                  discrepancies between a paper and its code. We
tion (Tang et al., 2025), evaluate whether the code              first define what constitutes a discrepancy:
Paper-Code Discrepancy We define a paper-                         cess this large volume efficiently, we automatically
code discrepancy as a semantic conflict between                   classify issues with Qwen3 4B Thinking (Yang
the scientific method described in the publication                et al., 2025), prompting the model to determine
and its actual implementation in the codebase, such               whether an issue reports a paper-code discrepancy
that the code does not faithfully reproduce the re-               or not, resulting in 232 candidates (prompt in §F.1).
ported method. This mismatch must be meaningful,                  All candidates are subsequently manually filtered
implying a fundamental alteration to the scientific               to ensure they meet our definition of a paper-code
logic, experimental protocol, or mathematical for-                discrepancy, yielding 59 discrepancies.
mulation described in the text. These discrepancies
manifest as three distinct types: Differences, where              Reproducibility Papers We collect reproducibil-
the code implements a logic distinct from the pa-                 ity reports from the ML Reproducibility Chal-
per’s description (e.g., L1 vs. L2 normalization),                lenge (Pineau et al., 2019; Sinha et al., 2020,
Paper Omissions, where the code includes critical                 2022, 2023), which invites participants to repro-
components missing from the text, or Code Omis-                   duce papers from leading ML, CV, and NLP confer-
sions, where a step described in the paper is absent              ences (e.g., NeurIPS, ICML, ICLR, CVPR, ICCV,
from the repository. We distinguish these discrep-                ACL, EMNLP) and papers from the reproducibility
ancies from engineering artifacts: We exclude bugs,               tracks of SIGIR and ECIR from 2020–2025. We
as these are independent of the paper’s scientific                retain only reports that reproduce a single, open-
description. Similarly, mismatches in default hy-                 access paper with an open-source implementation,
perparameters are not considered discrepancies if                 resulting in 171 reproducibility papers. From each
the code supports the paper’s settings via configu-               report, we extract mentions of paper-code discrep-
ration files or CLI arguments. Finally, we exclude                ancies using GPT-5, resulting in 132 candidates
trivial implementation details that are standard en-              (prompt in §F.3). All extracted discrepancies are
gineering practices typically omitted from scientific             manually verified to confirm adherence to our defi-
descriptions (e.g., adding noise to a denominator                 nition, yielding 65 discrepancies.
for numerical stability).
   The paper-code discrepancies, according to                     Validation and Phrasing Finally, all manually
our definition, can arise from distinct authorship                filtered discrepancies are validated by Gemini 3.1
(where the paper writer differs from the engineer                 Pro and GPT-5, checking the discrepancy’s exis-
implementing the code), simplifications made in                   tence given the original paper, codebase, and the
the text for readability, or code updates or experi-              GitHub issue or the description extracted from the
ments that were not propagated to the manuscript.                 reproducibility paper. For the cases where the
                                                                  LLMs disagreed, we manually verified the discrep-
3.1    Data Collection                                            ancy. During this step, the LLMs are further tasked
Fig. 2 provides an overview of our data collection.               with generating a standardized discrepancy descrip-
To obtain real-world instances of paper-code dis-                 tion. We prompt the models to output 3-8 sentences
crepancies, we draw from GitHub issues and repro-                 and to state what the paper describes, what the code
ducibility papers. Furthermore, synthetic discrep-                implements, and where the difference is. We use
ancies are generated in real scientific codebases.                these generated descriptions as the ground truth to
                                                                  ensure the same format and level of verbosity for
GitHub Issues We first identify repositories that                 paper-code discrepancies (prompt in §F.2 and §F.4).
reference a research paper in their homepage or                   We use two state-of-the-art LLMs to perform the
description field on GitHub, restricted to projects               validation and rephrasing to prevent potential bias
published between 2020 and 2025 and repositories                  in the selection and phrasing (see §C.5 for an analy-
with at least one issue (see §A.1 for details).2 For              sis). The verification step ensures adherence to the
each, we crawl all associated issues, yielding 1,890              discrepancy definition, acting as a high-precision
repositories with a total of 10,636 issues. To pro-               filter. Therefore, we retain only discrepancies that
   2
    The crawled repositories are not always the official imple-   can be verified given the explicit evidence, and pri-
mentation by the authors, but sometimes reproductions. They       oritize the precision and objectivity of the ground
were published, for example, when there is no official imple-     truth. In total, we obtain 92 discrepancies from
mentation or the reimplementation uses a different framework.
We still consider these repositories, as researchers might use    72 papers, where 42 discrepancies originate from
them to base their experiments on.                                GitHub issues and 50 from reproducibility papers.
                                                Discrepancy             Discrepancy             Publication                Cumulative
                    Arxiv Subject                  Type                  Category                  Year                   Token Counts
             1.0                          1.0                                                                  1.0
                          Origin                               0.3                      0.3
             0.8          Real            0.8                                                                  0.8
                          Synthetic
                          Real + Synth.
Proportion



             0.6                          0.6                  0.2                      0.2                    0.6
             0.4                          0.4                                                                  0.4
                                                               0.1                      0.1                                            Paper
             0.2                          0.2                                                                  0.2                     Code
                                                                                                                                       P+C
             0.0                          0.0                  0.0                      0.0                    0.0
                                                                                                                     5 10 25 50 100200400
                   Phy S




                                                                                g
                       CS


                     Sta s
                        io
                        ts

                        th




                                                 Cod m.




                                                                          Mo m
                                                        m.



                                                                              del
                                                                                s
                                                                              ion
                                                           .




                                                                       Tra a



                                                                                                  0
                                                                                                  1
                                                                                                  2
                                                                                                  3
                                                                                                  4
                                                                                                  5
                                                                                                                     log Token Count (1,000s)
                                                       Diff
                      sic




                                                                            Los

                                                                            Dat
                                                                           inin


                                                                                              202
                                                                                              202
                                                                                              202
                                                                                              202
                                                                                              202
                                                                                              202
                    EES


                    Q-B




                                                                              h
                     Ma




                                                    er O
                                                     eO




                                                                         luat
                                                                         orit
                                                                Alg
                                                Pap




                                                                     Eva
Figure 3: Analysis of the real (blue), synthetic (orange), and combined (green) discrepancy data. The y-axis
shows the proportion of the data. The arXiv subjects stand for Computer Science (CS), Electrical Engineering and
Systems Science (EESS), Physics, Statistics (Stats), Quantitative Biology (Q-Bio), and Mathematics (Math). The
Discrepancy Category chart shows only the distribution over computer science papers.


Synthetic Data To scale the data in size and                                      3.2   Data Analysis
beyond the CS/AI domain, we employ synthetic
                                                                                  Domain Fig. 3 analyzes several dimensions of
data generation. Specifically, based on our GitHub
                                                                                  S CI C O QA. While our real-world data is mostly
crawl, we sample repositories linked to arXiv pa-
                                                                                  from computer science (specifically from AI and
pers and those with permissive code licenses (i.e.,
                                                                                  its subdomains such as ML, CV, and NLP), the
MIT, Apache 2.0, CC-BY, BSD), as we will be
                                                                                  synthetic data contains papers and code from Elec-
redistributing their code partially. We randomly
                                                                                  trical Engineering and Systems Science, Physics,
select 102 repositories where the paper’s arXiv sub-
                                                                                  Statistics, Quantitative Biology, and Mathematics,
ject is CS (balanced over Machine Learning (ML,
                                                                                  making the data diverse across computational sci-
cs.LG), Computer Vision (CV, cs.CV), and Natural
                                                                                  ences.
Language Processing (NLP, cs.CL)), and 102 for
non-CS papers.3 Next, we prompt GPT-5 with the
                                                                                  Taxonomy We further analyze the discrepancy
paper and code to generate five code diffs accord-
                                                                                  type (as defined in §3) by annotating each discrep-
ing to our discrepancy definition (prompt in §F.5).
                                                                                  ancy in the real set as Difference, Paper Omission,
We then sample up to three of these changes, ensur-
                                                                                  or Code Omission. For the synthetic data, we pro-
ing that they do not manipulate the same file and
                                                                                  vide type definitions in the prompt and generate the
that the generated diff can be found by exact match
                                                                                  label along with the discrepancy. We find that 55%
in the original code. Finally, we add 13 additional
                                                                                  of discrepancies in the real data are Differences,
discrepancies that are labeled as Paper Omissions
                                                                                  which is also the majority class in the synthetic data,
as we later find these to be most critical (see §3.2
                                                                                  accounting for 78% of the data. Beyond the dis-
and §5). This yields a total of 543 discrepancies
                                                                                  crepancy type, we analyze the affected component
across the 204 papers, of which 286 discrepancies
                                                                                  within the research pipeline. We introduce a taxon-
are from the CS domain, and 257 are from other
                                                                                  omy of six discrepancy categories, namely: Algo-
computational domains, such as Electrical Engi-
                                                                                  rithm, Model, Loss, Evaluation, Data, and Training.
neering and Systems Science (114), Physics (51),
                                                                                  Table 1 provides an overview of our proposed tax-
or Statistics (40).
                                                                                  onomy. We apply this taxonomy to real-world data
   Example data, including discrepancy type and                                   and the CS subset of synthetic data, excluding the
category annotations, are shown in Table 12. Ex-                                  other domains where these ML-specific concepts
amples from the synthetic subset, including the                                   may not always apply cleanly. Similar to the dis-
code changes, are shown in Table 13. We release                                   crepancy type annotation, we manually label the
S CI C O QA publicly under CC-BY-4.0.                                             real instances and automatically generate labels
                                                                                  for the synthetic ones. In the real data, discrepan-
                                                                                  cies in the Algorithm and Loss categories dominate
    3
                                                                                  (25% and 24%), whereas in the synthetic data Al-
      We manually checked the repositories and removed code-
bases from our sample that were not suitable, such as reposi-                     gorithm is the largest category (26%) and Model is
tories for survey papers or with very few files.                                  the second-largest (21%).
           Label            Definition                               ically GPT-OSS 20B (OpenAI, 2025b) (prompt
           Difference       The code implements logic distinct       in §F.7), because it is open-weight, enabling
                            from the paper’s description             reproducibility, and offers a favorable speed-
           Paper Omission   The code includes critical compo-
Type




                            nents not described in the paper
                                                                     performance trade-off. For the real data where
           Code Omission    A step described in the paper is ab-     two ground truth descriptions exist (generated by
                            sent from the code                       Gemini 3.1 Pro and GPT-5), we consider matches
           Algorithm        Changes to step order, operations, or    against either as correct. To verify the evaluation
                            core logic                               setup, we annotate the predictions from 20 dis-
           Model            Architectural or weight initialization
                            deviations                               crepancies, where 10 originate from GitHub and
Category




           Loss             Alterations to loss definitions or       10 from reproducibility papers. To streamline our
                            terms
           Evaluation       Modifications to evaluation logic,
                                                                     evaluation, we compute the top three most similar
                            metrics, or scripts                      predicted discrepancies per model using Embed-
           Data             Dataset usage, preprocessing, aug-       dingGemma (Vera et al., 2025). We then manually
                            mentation, or filtering
           Training         Changes to the learning process,         assess whether each prediction matches the refer-
                            schedule, or optimization                ence discrepancy. In total, this yields 1,039 annota-
                                                                     tions, of which 143 predictions match the reference.
Table 1: The S CI C O QA discrepancy taxonomy. Types                 On this data, the LLM judge achieves an F1 score
describe the structural nature of the mismatch; Cat-                 of 87.5% ± 1.1, showing strong alignment with
egories describe which component of the research
                                                                     our annotations.4 We further validate the setup by
pipeline is affected.
                                                                     running Qwen3 32B as an alternative judge. We
                                                                     find a Cohen’s Kappa of κ = 0.838 between them
Input Length Finally, we visualize the token                         and an F1 score of 91.9%. However, since the F1
count distributions of the papers and codebases.                     score of Qwen3 32B against our human evaluation
The medians are 14,200 tokens for papers, 39,272                     is only 70.0%, we retain GPT-OSS 20B as a judge.
for codebases, and 56,903 when concatenated. Fur-                    While the evaluation is a binary classification (ref-
ther, 73 out of 276 papers have more than 100k                       erence and predicted discrepancies match or do not
tokens combined with their codebase, making S CI -                   match), we refer to the performance as recall, as
C O QA a challenging task for measuring the mod-                     the predictions may contain unannotated, but valid,
els’ long-context abilities. In the appendix, we                     discrepancies, and we only evaluate whether the
analyze the dataset by programming languages and                     annotated ones are detected.
the synthetic code diffs (§B.3 and §B.2).
                                                                     Models We evaluate several state-of-the-art
4          Experiments                                               model families, including commercial and open-
                                                                     weight models, as well as reasoning, instruction-
Given a paper and its code, we prompt the model                      tuned, and code-specific variants, specifically:
to generate a list of discrepancies between the two                  GPT-5, Gemini, GPT-OSS, Qwen3, DeepSeek R1,
(prompt in §F.6). We then parse the model out-                       Nemotron, and Mistral (exact model variants in
put into individual discrepancies. The generation                    Table 3).
prompt contains the same instructions as those used
to construct the ground-truth discrepancies. For im-                 5    Results
plementation details, we refer to §A. We further
ablate the discrepancy prediction experiment by                      Fig. 4 reports the recall of the top-performing mod-
providing only the code as input. This allows us to                  els (full results in Table 10). Overall, Gemini 3.1
quantify the contribution of the paper, distinguish-                 Pro and GPT-5 Mini perform best, achieving a re-
ing between discrepancies that require cross-modal                   call of 46.7%, leaving considerable room for im-
reasoning and those that can be inferred from the                    provement. On the synthetic data, GPT-5 detects
code (e.g., through comments or readmes) or from                     70.0% of discrepancies. Crucially, we observe a
the model’s parametric knowledge of the paper.                       strong correlation (r = 0.94) between recall on real
                                                                     and synthetic data, validating the synthetic subset
Evaluation We employ LLM-as-a-Judge (Zheng                           as a reliable proxy for ranking models (see §C.4).
et al., 2023) to evaluate whether the predicted dis-                    4
                                                                          We observe a slight variance in predictions despite a fixed
crepancy matches the reference. Inspired by Wei                      seed in vLLM; we therefore report the mean and standard
et al. (2025a), we use a reasoning model, specif-                    deviation over five runs.
                                                         Origin                                                                        Discrepancy Type            Prompt Tokens                                  Publication Year
          1.0
                                                         Real                                      Synthetic                                 Code Omission            <=31k     69k-130k                                                             2020                                    2023
                                                         R/GitHub                                  S/CS                                      Difference               31k-49k   >=130k                                                               2021                                    2024
          0.8                                            R/Repro.                                  S/Other                                   Paper Omission           49k-69k                                                                        2022                                    2025

          0.6
 Recall




          0.4

          0.2

          0.0
                                                      GPT-OSS 20B



                                                                                                   GPT-OSS 120B




                                                                                                                                        GPT-OSS 20B


                                                                                                                                       GPT-OSS 120B




                                                                                                                                                                 GPT-OSS 20B


                                                                                                                                                                GPT-OSS 120B




                                                                                                                                                                                                                                 GPT-OSS 20B



                                                                                                                                                                                                                                                                              GPT-OSS 120B
                                                                    Gemini 2.5 Pro



                                                                                                                  Gemini 2.5 Flash




                                                                                                                                      Gemini 2.5 Pro


                                                                                                                                     Gemini 2.5 Flash



                                                                                                                                                               Gemini 3.1 Pro

                                                                                                                                                               Gemini 2.5 Pro


                                                                                                                                                              Gemini 2.5 Flash




                                                                                                                                                                                                                                                                                             Gemini 2.5 Flash
                GPT-5
                        GPT-5 Mini
                                     Gemini 3.1 Pro




                                                                                                                                               GPT-5
                                                                                                                                          GPT-5 Mini
                                                                                                                                      Gemini 3.1 Pro




                                                                                                                                                                                                   GPT-5 Mini
                                                                                                                                                                                                                Gemini 3.1 Pro


                                                                                                                                                                                                                                               Gemini 2.5 Pro
                                                                                                                                                                        GPT-5
                                                                                                                                                                   GPT-5 Mini




                                                                                                                                                                                           GPT-5
                                                                                     GPT-5 Codex




                                                                                                                                        GPT-5 Codex




                                                                                                                                                                 GPT-5 Codex




                                                                                                                                                                                                                                                                GPT-5 Codex
Figure 4: Results of the top 8 best-performing models (sorted by average recall on the real and synthetic data) on
the discrepancy dataset by different analyses. From left to right: we analyze the origin of the discrepancy, the type
of discrepancy, the number of tokens in the prompt, and the publication year of the paper.


While general scaling laws can be observed (i.e.,                                                                                                             tion, where all described components must exist in
models trained with more compute and data per-                                                                                                                the code. Code Omissions and Differences benefit
form better), GPT-5 Mini and GPT-OSS 20B are                                                                                                                  from this explicit grounding. Conversely, the code
exceptions in our task, slightly outperforming their                                                                                                          contains many implementation details not required
larger variants. We attribute this partly to the self-                                                                                                        in the paper; thus, detecting Paper Omissions re-
preference bias of the judge for GPT-OSS, rating                                                                                                              quires the harder task of distinguishing deviations
its own outputs better (Panickssery et al., 2024),                                                                                                            from permissible engineering artifacts without a
and partly to the model’s verbosity. GPT-5 Mini                                                                                                               reference in the paper.
and GPT-OSS 20B on average make 5.3 and 5.8
                                                                                                                                                              Input Length We further analyze the perfor-
predictions per paper, while GPT-5 and GPT-OSS
                                                                                                                                                              mance by the number of input tokens.5 We split the
120B make only 4.6 and 5.0 predictions, giving the
                                                                                                                                                              dataset by prompt length into five approximately
smaller variants a higher chance to match the dis-
                                                                                                                                                              equally sized bins. We find a consistent pattern
crepancy at the expense of precision. Additionally,
                                                                                                                                                              where the longer the input, the lower the perfor-
we find GPT-5 Codex to be inferior, despite being a
                                                                                                                                                              mance becomes, consistent with findings in prior
larger model than GPT-5 Mini (Codex is based on
                                                                                                                                                              work (Zhang et al., 2024; Levy et al., 2024). This
GPT-5). While Codex is generally superior in code
                                                                                                                                                              sensitivity to input length also suggests an explana-
generation, for S CI C O QA, code and natural lan-
                                                                                                                                                              tion for the performance gap between domains in
guage understanding are both crucial, and we con-
                                                                                                                                                              the synthetic data: models struggle more with CS
jecture that the general instruction-following and
                                                                                                                                                              papers, which is likely driven by the larger repos-
reasoning abilities of GPT-5 and GPT-5 Mini are
                                                                                                                                                              itory size of CS vs. non-CS repositories (median:
more helpful than specialized coding knowledge.
                                                                                                                                                              53k vs. 31k tokens). This increased volume creates
                                                                                                                                                              a larger search space, making the task more chal-
Origin and Type Analyzing detection rates re-
                                                                                                                                                              lenging. Unlike long-context evaluations that pri-
veals a clear hierarchy: Code Omissions are the
                                                                                                                                                              marily test retrieval of isolated facts from extended
easiest to detect, followed by Differences, while
                                                                                                                                                              contexts (Kamradt, 2023; Hsieh et al., 2024), S CI -
Paper Omissions are the most challenging. This or-
                                                                                                                                                              C O QA requires cross-document reasoning over
der also explains the performance gap between data
                                                                                                                                                              real scientific papers and multi-file codebases to
sources. Discrepancies from GitHub are easier to
                                                                                                                                                              identify semantic mismatches, making it a natu-
detect because they primarily consist of Differences
                                                                                                                                                              ral testbed for long-context abilities (similar to the
(71.4%) and Code Omissions (19.0%). In contrast,
                                                                                                                                                              question answering task of Liu et al. (2024a)).6
discrepancies from reproducibility papers are more
                                                                                                                                                                  5
challenging as they are often dominated by Paper                                                                                                                    §C.3 conducts a further performance analysis by the posi-
Omissions (50%). The challenging nature of Pa-                                                                                                                tion of the relevant code file in the prompt.
                                                                                                                                                                  6
                                                                                                                                                                    The synthetic data generation can further be used to inject
per Omissions likely stems from the asymmetry                                                                                                                 discrepancies at controlled positions in the codebase, enabling
between modalities: the paper acts as a specifica-                                                                                                            targeted analysis of context-length effects.
         1.0
                       R: Paper+Code                    S: Paper+Code                           R+S: Paper+Code                       5.1   Code-Only Ablation
         0.8           R: Code Only                     S: Code Only                            R+S: Code Only
                                                                                                                                      To test the multimodality of our data, we remove
         0.6
Recall


                                                                                                                                      the paper from the input, leaving only the code.
         0.4                                                                                                                          This makes it more difficult to identify discrepan-
         0.2                                                                                                                          cies, but not impossible, since the repositories also
         0.0                                                                                                                          frequently contain abstracts, summaries, or details
                                                                                                                                      of the paper in their readme files. Furthermore, sci-
                                                       GPT-OSS 20B




                                                                                                    GPT-OSS 120B
                                      Gemini 3.1 Pro



                                                                     Gemini 2.5 Pro




                                                                                                                   Gemini 2.5 Flash
               GPT-5

                         GPT-5 Mini




                                                                                      GPT-5 Codex
                                                                                                                                      entific papers are typically part of the pre-training
                                                                                                                                      data; therefore, while the model does not directly
                                                                                                                                      receive the paper as input, it may be able to recall
                                                                                                                                      it from its pre-training. We show the results of the
Figure 5: Performance of top 8 models when given                                                                                      top models in this experiment in Fig. 5 (full results
paper and code, and only the code, split by data origin:                                                                              in Table 11). When removing the paper from the
Real (R), Synthetic (S), and combined (R+S).
                                                                                                                                      input, all models perform worse, confirming that
                                                                                                                                      the paper is necessary to perform the task. We ob-
                                                                                                                                      serve an average drop of 19.2 percentage points, a
Publication Year Lastly, we split the data by pub-                                                                                    relative drop of 48.3% on the real data. For the syn-
lication year. Among the top models, the one with                                                                                     thetic data, the drop is less pronounced; on average,
the most recent knowledge cutoff is the Gemini                                                                                        the models’ performance drops by 16.3 percentage
family, which was trained using data up to January                                                                                    points (relative drop of 30.8%).
2025 (other models have cutoffs in 2024). There-
fore, the 2025 split of our data is largely outside                                                                                   5.2   Validation of Unlabeled Discrepancies
the pre-training data, although Gemini models have                                                                                    To better understand the precision of the models,
partial coverage. Most models (except Gemini 2.5                                                                                      we analyze GPT-5’s, Gemini 2.5 Pro’s, and GPT-
Flash) perform worst on the most recent data. This                                                                                    OSS 20B’s generations. We select predictions from
suggests that models benefit from the inclusion of                                                                                    20 papers in NLP and CV that were not matched to
specific papers and codebases in their pre-training                                                                                   a ground truth, yielding a total of 224 evaluations.
sets, lending support to concerns regarding data                                                                                      We select these papers to leverage our own domain
contamination discussed in the literature (OpenAI,                                                                                    expertise, as validating discrepancies is challenging
2023; Zhou et al., 2023; Sainz et al., 2023). This                                                                                    and requires a detailed understanding of the paper
further emphasizes the importance of our synthetic                                                                                    and its implementation. We report results of this
data generation pipeline, which enables us to con-                                                                                    precision analysis in Table 4.
tinuously update our dataset with uncontaminated
                                                                                                                                         Overall, we find that Gemini 2.5 Pro does not
data that is not part of the pre-training data of future
                                                                                                                                      make significant errors, achieving a precision of
models.
                                                                                                                                      94.1%. Its three errors were due to preprocessing
                                                                                                                                      (an omitted term in a formula during OCR), an
                                                                                                                                      ambiguity within the paper (a nuance even noted
Open-Weight Models Beyond the top-                                                                                                    in the model’s generation), and the incorrect re-
performing models, we find the other open-weight                                                                                      call of another paper’s formula. GPT-5 follows
models (Qwen3, Nemotron, DeepSeek R1, Mistral)                                                                                        (85.7%), primarily failing due to paper ambigui-
severely limited. Nemotron 49B and Qwen3 30B                                                                                          ties or misinterpretations, or incorrect assumptions
Coder perform best, but only achieve an average                                                                                       about library functions. Finally, GPT-OSS 20B
recall on the combined data of 23.9% and 23.5%,                                                                                       struggles most (67.0%), frequently misunderstand-
respectively.                                                                                                                         ing the code logic (e.g., failing to align variables
   In summary, S CI C O QA provides a significant                                                                                     named differently in the paper and code or misin-
challenge for state-of-the-art LLMs. We find the re-                                                                                  terpreting conditional execution paths).
call of all models to be limited; the best-performing                                                                                    Taking inspiration from information retrieval
models can only detect 46.7% of all discrepancies                                                                                     benchmarks where incomplete relevance judg-
in the real-world data. Consequently, these systems                                                                                   ments are common (Buckley and Voorhees, 2004),
cannot yet be relied upon to ensure the faithfulness                                                                                  we construct a pooled ground truth from the 20
of scientific publications to their codebases.                                                                                        papers. We aggregate the discrepancies originally
     Model             GPT-5   Gemini   GPT-OSS         yond this primary use case, S CI C O QA can serve
     True Positives    66       53       72             multiple roles: as a natural long-context reason-
     False Positives    9        3       31             ing benchmark complementing synthetic retrieval
     Precision         88.0     94.6     69.9           probes, as a testbed for cross-modal claim verifica-
     Recall            51.2     41.1     55.8           tion between text and code, and as an evaluation
     F1                64.7     57.3     62.1
                                                        suite for code comprehension in scientific domains.
Table 2: Performance of GPT-5, Gemini 2.5 Pro, and      We release the dataset, model generations, eval-
GPT-OSS 20B on 129 pooled discrepancies from the        uation pipeline, and synthetic generation code to
annotation of unlabeled predictions and discrepancies   support these applications. To further advance this
from S CI C O QA from 20 NLP and CV papers.             field, we encourage the broader adoption of repro-
                                                        ducibility tracks to systematically capture these
                                                        discrepancies and expand future data collection.
annotated in S CI C O QA with the verified ones iden-
tified by the models (excluding minor ones, which
                                                        7   Limitations
are mostly discrepancies related to mismatching
settings that can typically be resolved via config-     Domains Our real-world data is predominantly
uration or the CLI). This results in a comprehen-       skewed towards Computer Science and Artificial
sive set of 129 distinct paper-code discrepancies,      Intelligence. Applying our real-world pipeline to
and we report the results in Table 2. We find that      non-CS domains, searching GitHub repositories for
the number of discrepancies uniquely identified         URLs linking to PubMed, bioRxiv, and medRxiv,
by the models is high (see also Table 4), yet re-       yielded very few issues reporting paper-code dis-
call remains low (41–56%), confirming our main          crepancies, and we did not identify comparable
experiment’s findings that model recall is limited.     reproducibility tracks outside of CS with paper-
GPT-5 achieves the best precision-recall tradeoff,      code discrepancy reports that we could use. The in-
obtaining an F1 score of 64.7%. We evaluate all         frastructure for surfacing paper-code discrepancies
22 models against this pooled ground truth in §C.6,     thus appears to be largely absent outside CS/AI.
confirming that recall remains the primary bottle-      Our synthetic pipeline is a short-term response,
neck. We make the annotations from the precision        which we believe provides more value than exclud-
analysis public, so future work can leverage them       ing these domains entirely. Long-term, we call for
as well for detailed analysis.                          broader adoption of reproducibility tracks, journals,
                                                        and projects, such as ReScience C (Rougier et al.,
6   Conclusion                                          2017) and the new Replication Research journal
                                                        (Röseler et al., 2025). Consequently, the distri-
We introduced S CI C O QA, a dataset of 635 discrep-
                                                        bution of errors outside CS/AI may differ from
ancies designed to evaluate the alignment between
                                                        our synthetic approximations, and performance on
a scientific paper and its code. Our analysis reveals
                                                        non-CS domains should be interpreted with this
a critical gap: while models like GPT-5 and Gem-
                                                        synthetic nature in mind.
ini demonstrate high precision, they suffer from
insufficient recall, detecting only 46.7% of real-      Discrepancy Definition Our discrepancy defi-
world discrepancies. For a verification use case,       nition focuses on “meaningful mismatches” that
low recall is a particularly consequential failure      impact reproducibility, explicitly excluding simple
mode: missed discrepancies silently provide false       bugs, hyperparameter configuration mismatches,
assurance, while false positives can be filtered by     or documentation nits. While this focuses the task
a human reviewer. We further find that models           on scientific validity, it means S CI C O QA does not
struggle with Paper Omissions, where code logic         cover the full spectrum of software engineering
is absent from the paper text, and fail to maintain     defects that may exist in research code.
performance on recent, uncontaminated publica-
tions. Consequently, while current LLMs show            Dataset Size With 635 discrepancies, our dataset
promise as assistants, they cannot yet serve as au-     is relatively small compared to large-scale pre-
tonomous verifiers of paper-code faithfulness. As       training corpora. This size is a deliberate trade-off
research scales toward “AI Scientists,” S CI C O QA     to ensure high quality: real-world discrepancies are
provides the essential ground truth to ensure these     naturally sparsely documented, and we employed
agents remain faithful to the scientific method. Be-    a rigorous manual verification process to guarantee
that every entry constitutes a meaningful mismatch      call rates demonstrated in our experiments (46.7%
rather than a trivial error or noise.                   for Gemini 3.1 Pro and GPT-5 Mini), automated
                                                        tools should not yet be used as the sole arbiter of a
Synthetic GPT-5 Performance Our synthetic               paper’s validity. Relying blindly on these systems
discrepancies are generated by GPT-5, which is          could lead to a false sense of security regarding
also evaluated on the benchmark. We find that           the reproducibility and validity of a paper. We em-
GPT-5 achieves disproportionately higher recall on      phasize that model outputs should support human
synthetic data. This suggests that, on this subset,     review and reproducibility efforts, not serve as au-
GPT-5 may benefit from its involvement in the data      tomatic reject signals or as evidence of bad faith.
generation. However, the strong correlation be-         Automated detections, particularly given the false
tween real and synthetic recall across all 22 models    positive rates observed in our experiments, require
(r = 0.94, Fig. 9) confirms that relative model com-    expert verification before any conclusions about
parisons remain valid. Notably, excluding the GPT-      research quality are drawn.
5 family from the correlation analysis increases
the correlation to r = 0.98, confirming that the        Acknowledgments
overall trend is not driven by GPT-5’s generation
advantage; rather, the GPT-5 family sits slightly       We thank Jan Buchmann, Bhavyajeet Singh, and
off the shared trend line that the other models fol-    Vatsal Venkatkrishna for their helpful comments
low closely. To mitigate this limitation, absolute      throughout the paper-writing process, as well as
model performance should be assessed on the real        the anonymous reviewers and area chair for their
subset, while the synthetic subset reliably supports    constructive feedback.
relative model comparison and allows for targeted          This work has been funded by the LOEWE Dis-
generation of new, uncontaminated data.                 tinguished Chair “Ubiquitous Knowledge Process-
                                                        ing,” LOEWE initiative, Hesse, Germany (Grant
8   Ethical Considerations                              Number: LOEWE/4a//519/05/00.002(0002)/81)
                                                        and by the German Federal Ministry of Research,
Data Release We constructed the synthetic por-
                                                        Technology and Space and the Hessian Ministry of
tion of S CI C O QA using repositories with permis-
                                                        Higher Education, Research, Science and the Arts
sive licenses (MIT, Apache 2.0, BSD, CC-BY)
                                                        within their joint support of the National Research
to ensure respectful redistribution of code. For
                                                        Center for Applied Cybersecurity ATHENE.
real-world discrepancies derived from GitHub is-
sues and reproducibility reports, we leverage the
publicly available data to create our ground truth      References
data by contextualizing and rephrasing the origi-
nal issues. None of our data contains any personal      Jinheon Baek, Sujay Kumar Jauhar, Silviu Cucerzan,
                                                           and Sung Ju Hwang. 2025. ResearchAgent: Iterative
information; however, since we work with scien-            research idea generation over scientific literature with
tific publications, they are closely associated with       large language models. In Proceedings of the 2025
the authors of the respective papers. We acknowl-          Conference of the Nations of the Americas Chap-
edge that highlighting discrepancies in a specific         ter of the Association for Computational Linguistics:
                                                           Human Language Technologies (Volume 1: Long Pa-
author’s work may be perceived negatively. We              pers), pages 6709–6738, Albuquerque, New Mexico.
emphasize that these discrepancies are treated as          Association for Computational Linguistics.
scientific artifacts for improving community repro-
ducibility standards, rather than criticisms of indi-   Monya Baker. 2016. 1,500 Scientists Lift the Lid on
vidual researchers. Discrepancies frequently arise       Reproducibility. Nature, 533(7604):452–454.
from benign causes, including concurrent code up-
                                                        Aarti Basant, Abhijit Khairnar, Abhijit Paithankar, Ab-
dates, simplifications for readability, or distinct       hinav Khattar, Adithya Renduchintala, Aditya Malte,
authorship of paper and code, and their presence          Akhiad Bercovich, Akshay Hazare, Alejandra Rico,
does not imply negligence or misconduct.                  Aleksander Ficek, Alex Kondratenko, Alex Sha-
                                                          poshnikov, Alexander Bukharin, Ali Taghibakhshi,
Automation Risks The benchmarked models in                Amelia Barton, Ameya Sunil Mahabaleshwarkar,
                                                          Amy Shen, Andrew Tao, Ann Guan, and 80 oth-
this work are intended to assist in quality assurance     ers. 2025. NVIDIA Nemotron Nano 2: An Accurate
of scientific papers and their codebases. However,        and Efficient Hybrid Mamba-Transformer Reasoning
there is a risk of over-reliance; given the low re-       Model. CoRR, abs/2508.14444.
Joeran Beel, Min-Yen Kan, and Moritz Baumgart.              Methods in Natural Language Processing and the
  2025. Evaluating Sakana’s AI Scientist: Bold Claims,      9th International Joint Conference on Natural Lan-
  Mixed Results, and a Promising Future? SIGIR Fo-          guage Processing (EMNLP-IJCNLP), pages 2185–
  rum, 59(1):1–20.                                          2194, Hong Kong, China. Association for Computa-
                                                            tional Linguistics.
Federico Bianchi, Yongchan Kwon, Zachary Izzo, Lin-
  jun Zhang, and James Zou. 2025. To Err Is Human:        Nils Dycke and Iryna Gurevych. 2026. Automatic Re-
  Systematic Quantification of Errors in Published AI       viewers Fail to Detect Faulty Reasoning in Research
  Papers via LLM Analysis. CoRR, abs/2512.05925.            Papers: A New Counterfactual Evaluation Frame-
                                                            work. Transactions of the Association for Computa-
Daniil A. Boiko, Robert MacKnight, Ben Kline, and           tional Linguistics. To appear.
  Gabe Gomes. 2023. Autonomous Chemical Re-
  search with Large Language Models. Nature,              Nouha Dziri, Ximing Lu, Melanie Sclar, Xiang Lorraine
  624(7992):570–578.                                        Li, Liwei Jiang, Bill Yuchen Lin, Sean Welleck, Peter
                                                            West, Chandra Bhagavatula, Ronan Le Bras, Jena D.
Samuel R. Bowman, Jeeyoon Hyun, Ethan Perez, Ed-            Hwang, Soumya Sanyal, Xiang Ren, Allyson Et-
  win Chen, Craig Pettit, Scott Heiner, Kamile Luko-        tinger, Zaïd Harchaoui, and Yejin Choi. 2023. Faith
  siute, Amanda Askell, Andy Jones, Anna Chen,              and Fate: Limits of Transformers on Compositional-
  Anna Goldie, Azalia Mirhoseini, Cameron McK-              ity. In Advances in Neural Information Processing
  innon, Christopher Olah, Daniela Amodei, Dario            Systems 36: Annual Conference on Neural Informa-
  Amodei, Dawn Drain, Dustin Li, Eli Tran-Johnson,          tion Processing Systems 2023, NeurIPS 2023, New
  and 27 others. 2022. Measuring Progress on Scal-          Orleans, LA, USA, December 10 - 16, 2023.
  able Oversight for Large Language Models. CoRR,
  abs/2211.03540.                                         Shubham Gandhi, Dhruv Shah, Manasi Patwardhan,
                                                            Lovekesh Vig, and Gautam Shroff. 2025. Research-
Jonathan B. Buckheit and David L. Donoho. 1995.
                                                            CodeAgent: An LLM Multi-agent System for Au-
  WaveLab and Reproducible Research, pages 55–81.
                                                            tomated Codification of Research Methodologies.
  Springer New York, New York, NY.
                                                            In AI for Research and Scalable, Efficient Systems,
Chris Buckley and Ellen M. Voorhees. 2004. Retrieval        pages 3–37, Singapore. Springer Nature Singapore.
  Evaluation with Incomplete Information. In Proceed-
  ings of the 27th Annual International ACM SIGIR         Gemini Team. 2025. Gemini 2.5: Pushing the Fron-
  Conference on Research and Development in Infor-          tier with Advanced Reasoning, Multimodality, Long
  mation Retrieval, SIGIR ’04, page 25–32, New York,        Context, and Next Generation Agentic Capabilities.
  NY, USA. Association for Computing Machinery.             CoRR, abs/2507.06261.

Christian Collberg and Todd A. Proebsting. 2016. Re-      Google DeepMind. 2025. Gemini 3.1 Pro Model Card.
  peatability in Computer Systems Research. Commu-          Technical report, Google DeepMind.
  nications of the ACM, 59(3):62–69.
                                                          Peter Henderson, Riashat Islam, Philip Bachman, Joelle
Anh Dau, Jin L.c. Guo, and Nghi Bui. 2024. Doc-             Pineau, Doina Precup, and David Meger. 2018. Deep
  Checker: Bootstrapping code large language model          Reinforcement Learning That Matters. In Proceed-
  for detecting and resolving code-comment inconsis-        ings of the Thirty-Second AAAI Conference on Ar-
  tencies. In Proceedings of the 18th Conference of         tificial Intelligence, (AAAI-18), the 30th innovative
  the European Chapter of the Association for Compu-        Applications of Artificial Intelligence (IAAI-18), and
  tational Linguistics: System Demonstrations, pages        the 8th AAAI Symposium on Educational Advances
  187–194, St. Julians, Malta. Association for Compu-       in Artificial Intelligence (EAAI-18), New Orleans,
  tational Linguistics.                                     Louisiana, USA, February 2-7, 2018, pages 3207–
                                                            3214. AAAI Press.
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing Rea-
  soning Capability in LLMs via Reinforcement Learn-      Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shan-
  ing. CoRR, abs/2501.12948.                                tanu Acharya, Dima Rekesh, Fei Jia, and Boris Gins-
                                                            burg. 2024. RULER: What’s the Real Context Size
DeepSeek-AI, Qihao Zhu, Daya Guo, Zhihong Shao,             of Your Long-Context Language Models? In First
  Dejian Yang, Peiyi Wang, Runxin Xu, Y. Wu, Yukun          Conference on Language Modeling.
  Li, Huazuo Gao, Shirong Ma, Wangding Zeng,
  Xiao Bi, Zihui Gu, Hanwei Xu, Damai Dai, Kai            Chuxuan Hu, Liyun Zhang, Yeji Lim, Aum Wadhwani,
  Dong, Liyue Zhang, Yishi Piao, and 21 others.             Austin Peters, and Daniel Kang. 2025. REPRO-
  2024. DeepSeek-Coder-V2: Breaking the Barrier of          bench: Can agentic AI systems assess the repro-
  Closed-Source Models in Code Intelligence. CoRR,          ducibility of social science research? In Findings of
  abs/2406.11931.                                           the Association for Computational Linguistics: ACL
                                                            2025, pages 23616–23626, Vienna, Austria. Associa-
Jesse Dodge, Suchin Gururangan, Dallas Card, Roy            tion for Computational Linguistics.
   Schwartz, and Noah A. Smith. 2019. Show your
   work: Improved reporting of experimental results. In   Matthew Hutson. 2018. Artificial Intelligence Faces
   Proceedings of the 2019 Conference on Empirical         Reproducibility Crisis. Science, 359(6377):725–726.
Carlos E. Jimenez, John Yang, Alexander Wettig,         Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob N.
  Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R.       Foerster, Jeff Clune, and David Ha. 2024. The AI
  Narasimhan. 2024. SWE-bench: Can Language               Scientist: Towards Fully Automated Open-Ended
  Models Resolve Real-world Github Issues? In The         Scientific Discovery. CoRR, abs/2408.06292.
  Twelfth International Conference on Learning Rep-
  resentations, ICLR 2024, Vienna, Austria, May 7-11,   Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Ya-
  2024. OpenReview.net.                                   mada, Shengran Hu, Jakob Foerster, David Ha, and
                                                          Jeff Clune. 2026. Towards end-to-end automation of
Greg Kamradt. 2023. Needle In A Haystack - Pres-          AI research. Nature, 651(8107):914–919.
  sure Testing LLMs. https://github.com/
  gkamradt/LLMTest_NeedleInAHaystack.                   Benjamin Marie, Atsushi Fujita, and Raphael Rubino.
  GitHub repository.                                      2021. Scientific credibility of machine translation re-
                                                          search: A meta-evaluation of 769 papers. In Proceed-
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying              ings of the 59th Annual Meeting of the Association for
 Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gon-           Computational Linguistics and the 11th International
 zalez, Hao Zhang, and Ion Stoica. 2023. Efficient        Joint Conference on Natural Language Processing
 Memory Management for Large Language Model               (Volume 1: Long Papers), pages 7297–7306, Online.
 Serving with PagedAttention. In Proceedings of the       Association for Computational Linguistics.
 29th Symposium on Operating Systems Principles,
 SOSP 2023, Koblenz, Germany, October 23-26, 2023,      Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi,
 pages 611–626. ACM.                                      Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar.
Mosh Levy, Alon Jacoby, and Yoav Goldberg. 2024.          2025. GSM-Symbolic: Understanding the Limita-
 Same task, more tokens: the impact of input length       tions of Mathematical Reasoning in Large Language
 on the reasoning performance of large language mod-      Models. In The Thirteenth International Conference
 els. In Proceedings of the 62nd Annual Meeting of        on Learning Representations, ICLR 2025, Singapore,
 the Association for Computational Linguistics (Vol-      April 24-28, 2025. OpenReview.net.
 ume 1: Long Papers), pages 15339–15353, Bangkok,
 Thailand. Association for Computational Linguistics.   Mistral AI & All Hands AI. 2025. Devstral: Fine-tuning
                                                          Language Models for Coding Agent Applications.
Weixin Liang, Yuhui Zhang, Hancheng Cao, Binglu           CoRR, abs/2509.25193.
 Wang, Daisy Yi Ding, Xinyu Yang, Kailas Vodra-
 halli, Siyu He, Daniel Scott Smith, Yian Yin, and 1    Mistral AI Team. 2025. Mistral OCR. https://
 others. 2024. Can Large Language Models Provide          mistral.ai/news/mistral-ocr. Blog.
 Useful Feedback on Research Papers? A Large-Scale
 Empirical Analysis. NEJM AI, 1(8):AIoa2400196.         OpenAI. 2023. GPT-4 Technical Report.            CoRR,
                                                          abs/2303.08774.
Xun Liang, Jiawei Yang, Yezhaohui Wang, Chen Tang,
  Zifan Zheng, Shichao Song, Zehao Lin, Yebin Yang,     OpenAI. 2025a. GPT-5 System Card. System card,
  Simin Niu, Hanyu Wang, Bo Tang, Feiyu Xiong,            OpenAI.
  Keming Mao, and Zhiyu Li. 2025. SurveyX: Aca-
  demic Survey Automation via Large Language Mod-       OpenAI. 2025b. GPT-OSS-120B & GPT-OSS-20B
  els. CoRR, abs/2502.14776.                              Model Card. CoRR, abs/2508.10925.
Zachary C. Lipton and Jacob Steinhardt. 2019. Trou-     Arjun Panickssery, Samuel R. Bowman, and Shi Feng.
  bling Trends in Machine Learning Scholarship. ACM       2024. LLM Evaluators Recognize and Favor Their
  Queue, 17(1):80.                                        Own Generations. In Advances in Neural Infor-
                                                          mation Processing Systems 38: Annual Conference
Jiawei Liu, Jia Le Tian, Vijay Daita, Yuxiang Wei,        on Neural Information Processing Systems 2024,
   Yifeng Ding, Yuhan Katherine Wang, Jun Yang,           NeurIPS 2024, Vancouver, BC, Canada, December
   and Lingming Zhang. 2024a. RepoQA: Evaluat-            10 - 15, 2024.
   ing Long Context Code Understanding. CoRR,
   abs/2406.06025.                                      Sheena Panthaplackel, Junyi Jessy Li, Milos Gligoric,
Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paran-      and Raymond J. Mooney. 2021. Deep Just-In-Time
  jape, Michele Bevilacqua, Fabio Petroni, and Percy      Inconsistency Detection Between Comments and
  Liang. 2024b. Lost in the middle: How language          Source Code. In Thirty-Fifth AAAI Conference on
  models use long contexts. Transactions of the Asso-     Artificial Intelligence, AAAI 2021, Thirty-Third Con-
  ciation for Computational Linguistics, 12:157–173.      ference on Innovative Applications of Artificial In-
                                                          telligence, IAAI 2021, The Eleventh Symposium on
Ryan Liu and Nihar B. Shah. 2023. ReviewerGPT? An         Educational Advances in Artificial Intelligence, EAAI
  Exploratory Study on Using Large Language Models        2021, Virtual Event, February 2-9, 2021, pages 427–
  for Paper Reviewing. CoRR, abs/2306.00622.              435. AAAI Press.

Llama-Nemotron Team. 2025. Llama-Nemotron: Effi-        Roger D. Peng. 2011. Reproducible Research in Com-
  cient Reasoning Models. CoRR, abs/2505.00949.           putational Science. Science, 334(6060):1226–1227.
Joelle Pineau, Koustuv Sinha, Genevieve Fried, Rose-       Nicolas P. Rougier, Konrad Hinsen, Frédéric Alexan-
  mary Nan Ke, and Hugo Larochelle. 2019. ICLR Re-           dre, Thomas Arildsen, Lorena A. Barba, Fabien
  producibility Challenge 2019. ReScience C, 5(2):5.         C. Y. Benureau, C. Titus Brown, Pierre de Buyl,
                                                             Ozan Caglayan, Andrew P. Davison, Marc-André
Joelle Pineau, Philippe Vincent-Lamarre, Koustuv             Delsuc, Georgios Detorakis, Alexandra K. Diem,
  Sinha, Vincent Lariviere, Alina Beygelzimer, Flo-          Damien Drix, Pierre Enel, Benoît Girard, Olivia
  rence d’Alche Buc, Emily Fox, and Hugo Larochelle.         Guest, Matt G. Hall, Rafael Neto Henriques, and
  2021. Improving Reproducibility in Machine Learn-          26 others. 2017. Sustainable Computational Science:
  ing Research (A Report from the NeurIPS 2019 Re-           the ReScience Initiative. PeerJ - Computer Science
  producibility Program). Journal of Machine Learn-          Journal, 3:e142.
  ing Research, 22(164):1–20.
                                                           Lukas Röseler, Lukas Wallrich, Susanne Adler, Prince
Matt Post. 2018. A call for clarity in reporting BLEU        Oppong Boakye, Thomas Rhys Evans, Janik Golter-
 scores. In Proceedings of the Third Conference on           mann, Tamarinde Haven, Jan Horstmann, Max Ko-
 Machine Translation: Research Papers, pages 186–            rbmacher, Miriam Müller, and et al. 2025. A Com-
 191, Brussels, Belgium. Association for Computa-            munity Model for Rigorous and Inclusive Scholar-
 tional Linguistics.                                         ship: Inaugural Editorial of Replication Research
                                                             (R2). Replication Research, 1.
Fazle Rabbi and Md. Saeed Siddik. 2020. Detecting
  Code Comment Inconsistency using Siamese Recur-          Oscar Sainz, Jon Campos, Iker García-Ferrero, Julen
  rent Network. In ICPC ’20: 28th International Con-         Etxaniz, Oier Lopez de Lacalle, and Eneko Agirre.
  ference on Program Comprehension, Seoul, Republic          2023. NLP evaluation in trouble: On the need to mea-
  of Korea, July 13-15, 2020, pages 371–375. ACM.            sure LLM data contamination for each benchmark.
Edward Raff. 2019. A Step Toward Quantifying Inde-           In Findings of the Association for Computational
  pendently Reproducible Machine Learning Research.          Linguistics: EMNLP 2023, pages 10776–10787, Sin-
  In Advances in Neural Information Processing Sys-          gapore. Association for Computational Linguistics.
  tems 32: Annual Conference on Neural Information
  Processing Systems 2019, NeurIPS 2019, December          Minju Seo, Jinheon Baek, Seongyun Lee, and Sung Ju
  8-14, 2019, Vancouver, BC, Canada, pages 5486–             Hwang. 2026. Paper2code: Automating code gener-
  5496.                                                      ation from scientific papers in machine learning. In
                                                            The Fourteenth International Conference on Learn-
Delip Rao, Jonathan Young, Thomas Dietterich, and            ing Representations, ICLR 2026, Rio de Janeiro,
  Chris Callison-Burch. 2024. WithdrarXiv: A                April 23-27, 2026. OpenReview.net.
  Large-Scale Dataset for Retraction Study. CoRR,
  abs/2412.03775.                                          Chenglei Si, Diyi Yang, and Tatsunori Hashimoto. 2025.
                                                             Can LLMs Generate Novel Research Ideas? A Large-
Abhinav Rastogi, Albert Q. Jiang, Andy Lo, Gabrielle         Scale Human Study with 100+ NLP Researchers. In
  Berrada, Guillaume Lample, Jason Rute, Joep Bar-           The Thirteenth International Conference on Learning
  mentlo, Karmesh Yadav, Kartik Khandelwal, Khy-             Representations, ICLR 2025, Singapore, April 24-28,
  athi Raghavi Chandu, Léonard Blier, Lucile Saulnier,       2025. OpenReview.net.
  Matthieu Dinot, Maxime Darrin, Neha Gupta, Ro-
  man Soletskyi, Sagar Vaze, Teven Le Scao, Yihan          Zachary S. Siegel, Sayash Kapoor, Nitya Nadgir,
  Wang, and 80 others. 2025. Magistral. CoRR,                Benedikt Stroebl, and Arvind Narayanan. 2024.
  abs/2506.10910.                                            CORE-Bench: Fostering the Credibility of Published
                                                             Research Through a Computational Reproducibility
Inderjot Kaur Ratol and Martin P. Robillard. 2017. De-       Agent Benchmark. Transactions on Machine Learn-
   tecting fragile comments. In Proceedings of the 32nd      ing Research, 2024.
  IEEE/ACM International Conference on Automated
  Software Engineering, ASE 2017, Urbana, IL, USA,         Koustuv Sinha, Maurits Bleeker, Samarth Bhargav, Jes-
  October 30 - November 03, 2017, pages 112–122.             sica Zosa Forde, Sharath Chandra Raparthy, Jesse
   IEEE Computer Society.                                    Dodge, Joelle Pineau, and Robert Stojnic. 2023. ML
                                                             Reproducibility Challenge 2022. ReScience C, 9(2).
Anna Rogers and Isabelle Augenstein. 2020. What
  can we do to improve peer review in NLP? In Find-        Koustuv Sinha, Jesse Dodge, Sasha Luccioni, Jes-
  ings of the Association for Computational Linguistics:     sica Zosa Forde, Sharath Chandra Raparthy, Joelle
  EMNLP 2020, pages 1256–1262, Online. Association           Pineau, and Robert Stojnic. 2022. ML Reproducibil-
  for Computational Linguistics.                             ity Challenge 2021. ReScience C, 8(2).
Guoping Rong, Yongda Yu, Song Liu, Xin Tan, Tianyi         Koustuv Sinha, Joelle Pineau, Jessica Forde, Rose-
  Zhang, Haifeng Shen, and Jidong Hu. 2025. Code             mary Nan Ke, and Hugo Larochelle. 2020. NeurIPS
  Comment Inconsistency Detection and Rectification          2019 Reproducibility Challenge. ReScience C,
  Using a Large Language Model. In 47th IEEE/ACM             6(2):11.
  International Conference on Software Engineering,
  ICSE 2025, Ottawa, ON, Canada, April 26 - May 6,         Guijin Son, Jiwoo Hong, Honglu Fan, Heejeong Nam,
  2025, pages 1832–1843. IEEE.                               Hyunwoo Ko, Seungwon Lim, Jinyeop Song, Jinha
  Choi, Gonçalo Paulo, Youngjae Yu, and Stella Bi-          Processing (EMNLP), pages 7534–7550, Online. As-
  derman. 2025. When AI Co-Scientists Fail: SPOT-a          sociation for Computational Linguistics.
  Benchmark for Automated Verification of Scientific
  Research. CoRR, abs/2505.11855.                         Yidong Wang, Qi Guo, Wenjin Yao, Hongbo Zhang,
                                                            Xin Zhang, Zhen Wu, Meishan Zhang, Xinyu Dai,
Giulio Starace, Oliver Jaffe, Dane Sherburn, James          Min Zhang, Qingsong Wen, Wei Ye, Shikun Zhang,
  Aung, Jun Shern Chan, Leon Maksin, Rachel Dias,           and Yue Zhang. 2024. AutoSurvey: Large Language
  Evan Mays, Benjamin Kinsella, Wyatt Thompson,             Models Can Automatically Write Surveys. In Ad-
  Johannes Heidecke, Amelia Glaese, and Tejal Pat-          vances in Neural Information Processing Systems
  wardhan. 2025. PaperBench: Evaluating AI’s Ability        38: Annual Conference on Neural Information Pro-
  to Replicate AI Research. In Forty-second Interna-        cessing Systems 2024, NeurIPS 2024, Vancouver, BC,
  tional Conference on Machine Learning, ICML 2025,         Canada, December 10 - 15, 2024.
  Vancouver, BC, Canada, July 13-19, 2025. OpenRe-
  view.net.                                               Anjiang Wei, Jiannan Cao, Ran Li, Hongyu Chen, Yuhui
                                                            Zhang, Ziheng Wang, Yuan Liu, Thiago S. F. X. Teix-
Theo Steiner and Rui Zhang. 2022. Code Comment              eira, Diyi Yang, Ke Wang, and Alex Aiken. 2025a.
  Inconsistency Detection with BERT and Longformer.         EquiBench: Benchmarking large language models’
  CoRR, abs/2207.14444.                                     reasoning about program semantics via equivalence
                                                            checking. In Proceedings of the 2025 Conference on
Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao
                                                            Empirical Methods in Natural Language Processing,
   Huang. 2025. AI-Researcher: Autonomous Scien-
                                                            pages 33868–33881, Suzhou, China. Association for
   tific Innovation. CoRR, abs/2505.18705.
                                                            Computational Linguistics.
James Thorne,       Andreas Vlachos,         Christos
  Christodoulopoulos, and Arpit Mittal. 2018.             Qiyao Wei, Samuel Holt, Jing Yang, Markus Wulfmeier,
  FEVER: a large-scale dataset for fact extraction          and Mihaela van der Schaar. 2025b. The AI Impera-
  and VERification. In Proceedings of the 2018              tive: Scaling High-Quality Peer Review in Machine
  Conference of the North American Chapter of               Learning. CoRR, abs/2506.08134.
  the Association for Computational Linguistics:
                                                          Yixuan Weng, Minjun Zhu, Guangsheng Bao, Hongbo
  Human Language Technologies, Volume 1 (Long
                                                            Zhang, Jindong Wang, Yue Zhang, and Linyi Yang.
  Papers), pages 809–819, New Orleans, Louisiana.
                                                            2025. CycleResearcher: Improving Automated Re-
  Association for Computational Linguistics.
                                                            search via Automated Review. In The Thirteenth In-
Minyang Tian, Luyu Gao, Shizhuo Dylan Zhang, Xinan          ternational Conference on Learning Representations,
  Chen, Cunwei Fan, Xuefei Guo, Roland Haas, Pan Ji,        ICLR 2025, Singapore, April 24-28, 2025. OpenRe-
  Kittithat Krongchon, Yao Li, Shengyan Liu, Di Luo,        view.net.
  Yutao Ma, Hao Tong, Kha Trinh, Chenyu Tian, Zihan
  Wang, Bohao Wu, Shengzhu Yin, and 10 others. 2024.      Yixuan Weng, Minjun Zhu, Qiujie Xie, QiYao Sun,
  SciCode: A Research Coding Benchmark Curated by           Zhen Lin, Sifan Liu, and Yue Zhang. 2026. Deepsci-
  Scientists. In Advances in Neural Information Pro-        entist: Advancing frontier-pushing scientific findings
  cessing Systems 38: Annual Conference on Neural           progressively. In The Fourteenth International Con-
  Information Processing Systems 2024, NeurIPS 2024,        ference on Learning Representations, ICLR 2026,
  Vancouver, BC, Canada, December 10 - 15, 2024.            Rio de Janeiro, April 23-27, 2026. OpenReview.net.

Gladys Tyen, Hassan Mansoor, Victor Carbune, Peter        David P. Woodruff, Vincent Cohen-Addad, Lalit Jain,
  Chen, and Tony Mak. 2024. LLMs cannot find rea-           Jieming Mao, Song Zuo, MohammadHossein Bateni,
  soning errors, but can correct them given the error       Simina Brânzei, Michael P. Brenner, Lin Chen, Ying
  location. In Findings of the Association for Compu-       Feng, Lance Fortnow, Gang Fu, Ziyi Guan, Zahra
  tational Linguistics: ACL 2024, pages 13894–13908,        Hadizadeh, Mohammad T. Hajiaghayi, Mahdi Ja-
  Bangkok, Thailand. Association for Computational          fariRaviz, Adel Javanmard, Karthik C. S., Ken-ichi
  Linguistics.                                              Kawarabayashi, and 17 others. 2026. Accelerating
                                                            Scientific Research with Gemini: Case Studies and
Henrique Schechter Vera, Sahil Dua, Biao Zhang,             Common Techniques. CoRR, abs/2602.03837.
  Daniel Salz, Ryan Mullins, Sindhu Raghuram Pa-
  nyam, Sara Smoot, Iftekhar Naim, Joe Zou, Feiyang       Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan
  Chen, Daniel Cer, Alice Lisak, Min Choi, Lucas Gon-       Tan, Chao Shen, and Meng Jiang. 2024. Large lan-
  zalez, Omar Sanseviero, Glenn Cameron, Ian Ballan-        guage models can self-correct with key condition ver-
  tyne, Kat Black, Kaifeng Chen, and 70 others. 2025.       ification. In Proceedings of the 2024 Conference on
  EmbeddingGemma: Powerful and Lightweight Text             Empirical Methods in Natural Language Processing,
  Representations. CoRR, abs/2509.20354.                    pages 12846–12867, Miami, Florida, USA. Associa-
                                                            tion for Computational Linguistics.
David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu
  Wang, Madeleine van Zuylen, Arman Cohan, and            Sarina Xi, Vishisht Rao, Justin Payan, and Nihar B.
  Hannaneh Hajishirzi. 2020. Fact or fiction: Verifying     Shah. 2025. FLAWS: A Benchmark for Error Identi-
  scientific claims. In Proceedings of the 2020 Con-        fication and Localization in Scientific Papers. CoRR,
  ference on Empirical Methods in Natural Language          abs/2511.21843.
Yanzheng Xiang, Hanqi Yan, Shuyin Ouyang, Lin Gui,        Kun Zhou, Yutao Zhu, Zhipeng Chen, Wentong Chen,
  and Yulan He. 2025. SciReplicate-Bench: Bench-            Wayne Xin Zhao, Xu Chen, Yankai Lin, Ji-Rong
  marking LLMs in Agent-driven Algorithmic Repro-           Wen, and Jiawei Han. 2023. Don’t Make Your
  duction from Research Papers. In Second Conference        LLM an Evaluation Benchmark Cheater. CoRR,
  on Language Modeling.                                     abs/2311.01964.

Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shen-        A       Implementation Details
  gran Hu, Chris Lu, Jakob N. Foerster, Jeff Clune, and
  David Ha. 2025. The AI Scientist-v2: Workshop-          A.1      GitHub Crawl Details
  Level Automated Scientific Discovery via Agentic
  Tree Search. CoRR, abs/2504.08066.                      We use the GitHub API7 to search for code
                                                          repositories that provide code for a research paper.
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
  Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao,             To obtain only repositories for a single paper,
  Chengen Huang, Chenxu Lv, Chujie Zheng, Day-            we search the description and homepage fields
  iheng Liu, Fan Zhou, Fei Huang, Feng Hu, Hao            of the repositories, which are commonly used
  Ge, Haoran Wei, Huan Lin, Jialong Tang, and 39          to indicate which paper the code is intended to
  others. 2025. Qwen3 Technical Report. CoRR,
  abs/2505.09388.
                                                          implement. Specifically, we search for the follow-
                                                          ing URLs: arxiv.org, openreview.net,
Christine Ye, Sihan Yuan, Suchetha Cooray, Steven Dill-   aclanthology.org, doi.org/10.1145.
  mann, Ian L. V. Roque, Dalya Baron, Philipp Frank,      We further limit our search to only include code
  Sergio Martin-Alvarez, Nolan Koblischke, Frank J.
                                                          repositories that have been published since 2020.
  Qu, Diyi Yang, Risa Wechsler, and Ioana Ciuca. 2025.
  ReplicationBench: Can AI Agents Replicate Astro-
  physics Research Papers? CoRR, abs/2510.24591.          A.2      Issue Processing
                                                          For the initial GitHub issue classification with
Lei You, Lele Cao, and Iryna Gurevych. 2026. Pre-
  venting the Collapse of Peer Review Requires            Qwen3 4B Thinking, we used a low temperature
  Verification-First AI. CoRR, abs/2601.16909.            of 0.2 to minimize generation variance and pro-
                                                          mote strict adherence to the classification schema.
Tianmai M. Zhang and Neil F. Abernethy. 2025. Re-         For the verification of discrepancies from GitHub
  viewing Scientific Papers for Critical Problems With
  Reasoning LLMs: Baseline Approaches and Auto-           issues with GPT-5, we checked whether an issue
  matic Evaluation. In NeurIPS 2025 AI for Science        description contained screenshots of the paper or
  Workshop.                                               code. If so, we replaced these with their text equiv-
                                                          alents.
Xinrong Zhang, Yingfa Chen, Shengding Hu, Zihang
  Xu, Junhao Chen, Moo Hao, Xu Han, Zhen Thai,
                                                          A.3      Versioning
  Shuo Wang, Zhiyuan Liu, and Maosong Sun. 2024.
  ∞Bench: Extending long context evaluation beyond        To ensure that the paper and code still contain the
  100K tokens. In Proceedings of the 62nd Annual          discrepancy, we provide links to versioned pub-
  Meeting of the Association for Computational Lin-
  guistics (Volume 1: Long Papers), pages 15262–          lications for arXiv, using the version at the time
  15277, Bangkok, Thailand. Association for Compu-        of the reporting of the discrepancy, i.e., publica-
  tational Linguistics.                                   tion of the reproducibility report or creation of the
                                                          GitHub issue. Similarly, for the codebases, we
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,            use the commit history to obtain the version of the
  Zhuohan Li, Dacheng Li, Eric Xing, Hao Zhang,           code at the time of the reporting of the discrepancy.
  Joseph E Gonzalez, and Ion Stoica. 2023. Judg-          Our dataset contains the versioned links to both
  ing LLM-as-a-Judge with MT-Bench and Chatbot            the paper (for arXiv) and the codebase. For the
  Arena. In Advances in Neural Information Process-
  ing Systems, volume 36, pages 46595–46623. Curran
                                                          synthetic data, we take a version of the codebase
  Associates, Inc.                                        as of 31-10-2025.

Tianshi Zheng, Zheye Deng, Hong Ting Tsang, Weiqi         A.4      Paper Processing
  Wang, Jiaxin Bai, Zihao Wang, and Yangqiu Song.
  2025. From automation to autonomy: A survey on          We provide the paper text in markdown as input.
  large language models in scientific discovery. In       We use Mistral’s OCR (Mistral AI Team, 2025) to
  Proceedings of the 2025 Conference on Empirical         convert the PDF to markdown. We exclude figures,
  Methods in Natural Language Processing, pages
  17733–17750, Suzhou, China. Association for Com-            7
                                                             https://docs.github.com/en/rest?
  putational Linguistics.                                 apiVersion=2022-11-28
                                                                                                            Context   Knowledge   Release
 Model                     Paper                              Model Card
                                                                                                            Window      Cutoff     Date
 DeepSeek Coder 16B v2     DeepSeek-AI (2024)                 deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct      131k   Nov 2023    Jun 2024
 DeepSeek R1 32B           DeepSeek-AI (2025)                 deepseek-ai/DeepSeek-R1-Distill-Qwen-32B         131k    Jul 2024    Jan 2025
 DeepSeek R1 8B            DeepSeek-AI (2025)                 deepseek-ai/DeepSeek-R1-Distill-Llama-8B         131k    Jul 2024    Jan 2025
 Gemini 2.5 Flash          Gemini Team (2025)                 gemini-2.5-flash                               1,047k    Jan 2025   Aug 2025
 Gemini 2.5 Flash Lite     Gemini Team (2025)                 gemini-2.5-flash-lite                          1,047k    Jan 2025   Aug 2025
 Gemini 2.5 Pro            Gemini Team (2025)                 gemini-2.5-pro                                 1,047k    Jan 2025   Aug 2025
 Gemini 3.1 Pro            Google DeepMind (2025)             gemini-3.1-pro-preview                         1,047k    Jan 2025   Feb 2026
 GPT-OSS 120B              OpenAI (2025b)                     openai/gpt-oss-120b                              131k   Jun 2024    Aug 2025
 GPT-OSS 20B               OpenAI (2025b)                     openai/gpt-oss-20b                               131k   Jun 2024    Aug 2025
 GPT-5                     OpenAI (2025a)                     gpt-5-2025-08-07                                 272k   Sep 2024    Aug 2025
 GPT-5 Codex               OpenAI (2025a)                     gpt-5-codex                                      272k   Sep 2024    Aug 2025
 GPT-5 Mini                OpenAI (2025a)                     gpt-5-mini-2025-08-07                            272k   May 2024    Aug 2025
 GPT-5 Nano                OpenAI (2025a)                     gpt-5-nano-2025-08-07                            272k   May 2024    Aug 2025
 Devstral 24B Small        Mistral AI & All Hands AI (2025)   mistralai/Devstral-Small-2507                    131k   Mar 2025     Jul 2025
 Magistral 24B Small       Rastogi et al. (2025)              mistralai/Magistral-Small-2509                   131k   Jun 2025    Sep 2025
 Nemotron Nano 9B v2       Basant et al. (2025)               nvidia/NVIDIA-Nemotron-Nano-9B-v2                131k   Apr 2025    Aug 2025
 Nemotron Super 49B v1.5   Llama-Nemotron Team (2025)         nvidia/Llama-3_3-Nemotron-Super-49B-v1_5         131k   Dec 2023     Jul 2025
 Qwen3 30B Coder           Yang et al. (2025)                 Qwen/Qwen3-Coder-30B-A3B-Instruct                262k   Mar 2025     Jul 2025
 Qwen3 30B Instruct        Yang et al. (2025)                 Qwen/Qwen3-30B-A3B-Instruct-2507                 262k   Mar 2025     Jul 2025
 Qwen3 30B Thinking        Yang et al. (2025)                 Qwen/Qwen3-30B-A3B-Thinking-2507                 262k   Mar 2025     Jul 2025
 Qwen3 4B Instruct         Yang et al. (2025)                 Qwen/Qwen3-4B-Instruct-2507                      262k   Mar 2025     Jul 2025
 Qwen3 4B Thinking         Yang et al. (2025)                 Qwen/Qwen3-4B-Thinking-2507                      262k   Mar 2025     Jul 2025


Table 3: Model versions including their context window, knowledge cutoff (date of most recent pre-training data),
and release date.


although the captions are included. We further                             A.6   Context Processing
remove the references section from all papers.

A.5      Code Processing                                                   The markdown paper and processed code reposi-
To provide the code in the prompt, we obtain all                           tory are inserted into the prompt. We fill the prompt
files from the GitHub repository at a target date                          up to 90% of the context size to leave space for the
using the commit history, which we set to the date                         reasoning (if supported by the model) and output.
when the original GitHub issue was raised or the                           If the paper and code would exceed the context
reproducibility paper was published. For the syn-                          window, we truncate entire files from the end of the
thetic data, we set the cutoff to 31-10-2025. Having                       code prompt until it fits into the context window.
a versioned and static code repository is crucial to
ensure reproducibility of our experiments and to
make sure paper-code discrepancies have not been
fixed in our dataset.                                                      A.7   Model and Decoding Configuration
   We retain only files that contain relevant
content, mainly excluding dataset files. Specif-
ically, we exclude files that are larger than                           We deploy the open-weight models with FP16, ex-
1MB and include files with the following                                cept for the GPT-OSS models, which were only
extensions:       .c, .cc, .cpp, .cu, .h,                               published in MXFP4. We utilize the Ollama and
.hpp, .java, .jl, .m, .matlab,                                          vLLM libraries (Kwon et al., 2023) on 1-4 A100
Makefile, .md, .pl, .ps1,                                               80GB GPUs, depending on the model’s VRAM
.py, .r, .sh, config.txt, .rs,                                          requirements; the commercial models are queried
readme.txt, requirements_dev.txt,                                       via their respective APIs. We generally set the
requirements-dev.txt,                                                   temperature to 1.0, and for the GPT-5, GPT-OSS,
requirements.dev.txt,                                                   and Gemini models, set a high reasoning effort or
requirements.txt, .scala, .yaml,                                        budget to maximize performance. For the Gemini
.yml. We obtain this list by manually inspecting                        models, we set a high reasoning budget of 24k to-
the file extensions in the repositories of our dataset.                 kens; for the GPT-5 models and GPT-OSS, we set a
We further convert all Jupyter notebooks to Python                      “high” reasoning budget. Further details about each
files by removing their outputs. For the prompt, we                     model can be obtained from the respective model
further include a list of all files in the repository.                  card linked in Table 3.
                                 Tokens                                         Lexical Similarity                                           Semantic Similarity                               Eval Agreement ( =0.83)
                     GPT mean: 181                                             Mean: 0.52                                                    Mean: 0.83
             300     Gemini mean: 135                            15.0                                                       15.0




                                                                                                                                                                                    Match
                                                                                                                                                                                                  541               104
             250                                                 12.5                                                       12.5                                                                 (5.9%)            (1.1%)
             200                                                 10.0                                                       10.0
Gemini




                                                         Count




                                                                                                                    Count




                                                                                                                                                                                 GPT
             150                                                  7.5                                                        7.5




                                                                                                                                                                                    No Match
             100                                                  5.0                                                        5.0                                                                  104               8,493
                                                                                                                                                                                                 (1.1%)            (91.9%)
              50                                                  2.5                                                        2.5
               0                                                  0.0                                                        0.0                                                                 Match          No Match
                   0 50 100 150 200 250 300                               0.2          0.4          0.6       0.8                      0.7            0.8          0.9
                                     GPT                                  TF-IDF Cosine Similarity                                     Semantic Cosine Similarity                                         Gemini

              Figure 6: Comparisons between the two ground truth descriptions generated by Gemini 3.1 Pro and GPT-5.

                   # Changed Files                       # Diff Snippets                                      # Added and Removed Lines                                               Code Jaccard Similarity
             1.0                           1.0                                               0.25                                                                  0.15
                                                                                                                                                   Added Lines                Full Snippet
                                                                                                                                                   Removed Lines              Added/Removed Lines
             0.8                           0.8                                               0.20                                                                  0.12

             0.6                           0.6                                               0.15                                                                  0.09
Proportion




             0.4                           0.4                                               0.10                                                                  0.06

             0.2                           0.2                                               0.05                                                                  0.03

             0.0                           0.0                                               0.00                                                                  0.00
                    1     2      3               1   2       3      4      5       6                 1    2   3     4       5      6    7      8     9    10 10+          0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
                    Changed Files                         Diff Snippets                                                         Lines                                                      Jaccard Similarity


Figure 7: Quantitative analysis of synthetic code modifications. We show the distribution of number of changed
files, number of generated diff snippets, added (green) vs. removed (orange) lines in those snippets, and Jaccard
similarity between the original and modified code.


B                  Extended Analysis                                                                                    Code Changes We find the generated discrepan-
                                                                                                                        cies in the code to be highly targeted. The vast
B.1                 Gemini and GPT Ground Truth                                                                         majority affect only a single file (1.08 ± 0.29 on
                    Comparison                                                                                          average), with a maximum of three files. Similarly,
For the real data, we rephrased the ground truth                                                                        the number of distinct generated diffs is low, with
discrepancy descriptions with Gemini 3.1 Pro and                                                                        a mean of 1.24 ± 0.61 snippets per discrepancy.
GPT-5 (see §3.1). We analyze the similarity be-                                                                         This confirms that the generated errors are specific
tween these two descriptions in Fig. 6. We find the                                                                     deviations in logic rather than large-scale refactors.
GPT descriptions to be slightly longer (181 ± 40                                                                        The number of line edits (i.e., added or removed
vs. 135 ± 34 tokens). We further find moderate                                                                          lines) further supports the subtlety of the dataset.
lexical overlap between the two ground truths (av-                                                                      The distribution of line counts is heavily skewed
erage TF-IDF cosine similarity is 0.52), but high                                                                       towards small edits: On average, 2.41 ± 3.25 lines
semantic similarity (average 0.83 computed using                                                                        are added and 3.13 ± 4.47 lines are removed. The
EmbeddingGemma), indicating that the models use                                                                         slightly higher count for removed lines suggests the
different wording to describe the same discrepancy.                                                                     discrepancies often simplify logic (e.g., removing
Finally, we analyze how often the GPT-OSS 20B                                                                           a normalization step) rather than adding complex
judge matches a prediction against none, either,                                                                        boilerplate.
or both ground truths. We find that in 97.7% of
cases, the judge comes to the same verdict given                                                                        Code Similarity To quantify the similarity be-
the two different discrepancy descriptions, yielding                                                                    tween the original and modified code, we calculate
a Cohen’s Kappa of κ = 0.83.                                                                                            the Jaccard similarity. We measure the similar-
                                                                                                                        ity at two levels: over the entire generated code
B.2                 Synthetic Code Analysis                                                                             block (which often contains a few unchanged lines)
We conduct a quantitative analysis of the synthetic                                                                     and over only the code lines that were modified.
data to validate that our generation pipeline pro-                                                                      Comparing the entire code block generated by the
duces minimal changes, leaving the main code in-                                                                        model against the original yields a high mean sim-
tact. Fig. 7 presents the analysis of the generated                                                                     ilarity of 0.74 ± 0.20. This indicates that the sur-
diffs.                                                                                                                  rounding context and structure remain largely iden-
Model                      GPT-5   Gemini   GPT-OSS               Code File
                                                                                       # Samples
False Positives            10        3         34                 Prompt Position
  Code Misunderstanding     1        0         20
  Paper Misunderstanding    2        0          9                 ≤ 32k                253 (39.8%)
  Paper Ambiguity           2        1          0
  OCR Error                 1        1          1
                                                                  ≤ 64k                463 (72.9%)
  3rd Party Code            2        0          1                 ≤ 131k               568 (89.4%)
  No Discrepancy            1        0          1                 ≤ 262k               631 (99.4%)
  Minor (Config)            1        0          2
  Other                     0        1          0                 ≤ 524k               635 (100.0%)
True Positives             60       48         69
  Unique                   23       19         34        Table 5: Number of data samples by position of the last
  Minor                     7        7         12        relevant code file in the prompt.
Total                      70       51        103
Precision                  85.7     94.1       67.0
                                                         the small sample size. Therefore, we group all
Table 4: Analysis of unlabeled discrepancy predictions   non-Python instances into a unified subset of 46
of GPT-5, Gemini 2.5 Pro, and GPT-OSS 20B on 20
                                                         samples for analysis (“Not Python”). The resulting
NLP and CV papers from the real subset of S CI C O QA.
                                                         recall scores are presented in Table 6. Most models
                                                         show only small, inconsistent differences between
tical. Comparing only the specific lines that differ     Python and non-Python recall (within ±5 pp). The
(added vs. removed) yields a mean similarity of          notable exceptions are Devstral 24B Small, which
0.50 ± 0.29. This moderate overlap suggests the          collapses from 15.1% on Python to 0% on non-
changes are often modifications of existing state-       Python, and Gemini 2.5 Flash (+9.7 pp); con-
ments (e.g., changing an operator or variable) rather    versely, GPT-5 Mini (−5.9 pp), GPT-OSS 20B
than complete replacements. Overall, the data con-       (−5.4 pp), and Nemotron Nano 9B v2 (−7.8 pp)
firms that the synthetic discrepancies are precise       actually perform slightly better on non-Python.
and minimal, strictly adhering to the “small” and        Beyond these aggregate trends, two specific lan-
“conceptually meaningful” constraints of the syn-        guages stand out. MATLAB is a positive outlier:
thetic data generation prompt (§F.5).                    GPT-5 and GPT-5 Mini both achieve 90.0% re-
                                                         call, substantially above their Python performance.
B.3     Programming Language Distribution                With n = 10 this is tentative, but we hypothesize
Fig. 8 shows the distribution of programming lan-        that MATLAB’s mathematical syntax aligns more
guages in the S CI C O QA dataset. Since the real        closely with the equations presented in scientific
data originates from the CS/AI domain, we ob-            papers, facilitating easier logical alignment for the
serve Python as the dominant language, along with        models. Conversely, CUDA is a near-universal
a small portion of C/C++, MATLAB, and CUDA               weak spot: 17 of 22 models score 0% recall on
files. Besides Python, other languages are present       CUDA (n = 4), including GPT-5, Gemini 3.1
in the synthetic data, including Java, Scala, Julia,     Pro, and GPT-OSS 120B. Small sample sizes limit
and R, although their overall presence is relatively     definitive conclusions for both languages.
small.
                                                         C.3   Truncation Analysis
C     Extended Results                                   In §5 we analyzed the model performance by input
                                                         length, finding that longer inputs degrade perfor-
C.1     Error Analysis
                                                         mance. We extend this analysis by investigating
Table 4 provides the detailed breakdown of our           the performance as a function of the position of the
human analysis from §5.2 on the predictions of           last relevant code file in the prompt. The relevant
GPT-5, Gemini 2.5 Pro, and GPT-OSS 20B.                  code files are obtained in the validation/rephrasing
                                                         step for the real data, and during discrepancy gen-
C.2     Performance by Programming Language              eration for the synthetic data. Table 5 shows the
In the synthetic dataset, the known injection points     distribution of the position of the last relevant code
allow us to analyze detection performance across         file in the prompt. We find that 89.4% of samples
different programming languages. Since the dataset       in our data contain all relevant code files within a
is skewed towards Python, drawing conclusions for        context window of 131k tokens, and 99.4% within
specific low-resource languages is difficult due to      a 262k context window.
                               Repos                                  Files                           Lines                            Tokens
                                                                                                                        107
                 102                                                                   105
                                                   103                                                                  105
                                                   102
Real




                 101                                                                   103
                                                                                                                        103
                                                   101
                                                                                       101                              101
                 100                               100


                       PowerShell




                                                         PowerShell




                                                                                             PowerShell




                                                                                                                              PowerShell
                           YAML
                            Shell


                         MATLAB




                                                           MATLAB




                                                                                               MATLAB
                          Python



                           CUDA
                             Text
                            Scala
                             Julia
                                 R
                              Perl



                                                            Python
                                                             YAML
                                                              Shell



                                                               Text

                                                               Julia
                                                               Java
                                                              Scala
                                                                   R
                                                                Perl



                                                                                                Python
                                                                                                 YAML
                                                                                                  Shell



                                                                                                   Text

                                                                                                   Julia
                                                                                                    Perl



                                                                                                                                 Python
                                                                                                                                  YAML
                                                                                                                                   Shell


                                                                                                                                MATLAB
                                                                                                                                  CUDA
                                                                                                                                    Text
                                                                                                                                   Scala
                                                                                                                                    Julia
                                                                                                                                        R
                                                                                                                                     Perl
                       Markdown
                          C/C++


                             Java




                                                         Markdown
                                                            C/C++
                                                             CUDA




                                                                                             Markdown
                                                                                                C/C++
                                                                                                 CUDA

                                                                                                   Java
                                                                                                  Scala
                                                                                                       R




                                                                                                                              Markdown
                                                                                                                                 C/C++


                                                                                                                                    Java
                               Repos                                  Files                           Lines                            Tokens
                                                   104                                                                  107
                 102                                                                   105
                                                   103                                                                  105
Synthetic




                                                   102                                 103                              103
                 101
                                                   101
                                                                                       101                              101
                 100                               100
                       PowerShell




                                                         PowerShell




                                                                                             PowerShell




                                                                                                                              PowerShell
                         MATLAB
                          Python
                           YAML
                            Shell



                             Text

                             Julia
                          C/C++
                           CUDA

                             Java
                            Scala
                                 R
                              Perl



                                                            Python
                                                             YAML
                                                              Shell


                                                           MATLAB
                                                               Text

                                                               Julia
                                                                   R
                                                                Perl



                                                                                                Python
                                                                                                 YAML
                                                                                                  Shell


                                                                                               MATLAB
                                                                                                   Text

                                                                                                   Julia
                                                                                                       R
                                                                                                    Perl



                                                                                                                                 Python
                                                                                                                                  YAML
                                                                                                                                   Shell


                                                                                                                                MATLAB
                                                                                                                                  CUDA
                                                                                                                                    Text
                                                                                                                                   Scala
                                                                                                                                    Julia
                                                                                                                                        R
                                                                                                                                     Perl
                       Markdown




                                                         Markdown
                                                            C/C++
                                                             CUDA

                                                               Java
                                                              Scala




                                                                                             Markdown
                                                                                                C/C++
                                                                                                 CUDA

                                                                                                   Java
                                                                                                  Scala




                                                                                                                              Markdown
                                                                                                                                 C/C++


                                                                                                                                    Java
                               Repos                                  Files                           Lines                            Tokens
                                                   104                                                                  107
Real+Synthetic




                 102                                                                   105
                                                   103                                                                  105
                                                   102                                 103                              103
                 101
                                                   101
                                                                                       101                              101
                 100                               100
                       PowerShell




                                                         PowerShell




                                                                                             PowerShell




                                                                                                                              PowerShell
                         MATLAB




                                                           MATLAB
                          Python
                           YAML
                            Shell

                           CUDA
                             Text




                                                            Python
                                                             YAML
                                                              Shell

                                                             CUDA
                                                               Text




                                                                                                Python
                                                                                                 YAML
                                                                                                  Shell


                                                                                               MATLAB




                                                                                                                                MATLAB
                                                                                                 CUDA
                                                                                                   Text
                                                                                                  Scala
                                                                                                   Julia
                                                                                                       R
                                                                                                    Perl



                                                                                                                                 Python
                                                                                                                                  YAML
                                                                                                                                   Shell

                                                                                                                                  CUDA
                                                                                                                                    Text
                       Markdown
                          C/C++


                             Java
                            Scala
                             Julia
                                 R
                              Perl




                                                         Markdown
                                                            C/C++


                                                               Java
                                                              Scala
                                                               Julia
                                                                   R
                                                                Perl




                                                                                             Markdown
                                                                                                C/C++


                                                                                                   Java




                                                                                                                              Markdown
                                                                                                                                 C/C++


                                                                                                                                    Java
                                                                                                                                   Scala
                                                                                                                                    Julia
                                                                                                                                        R
                                                                                                                                     Perl
Figure 8: Distribution of programming languages in S CI C O QA. The columns of the plot show the distribution
by number of Repos, Files, Lines, and Tokens for each respective programming language. The rows show the
distribution for the real, synthetic, and combined data.




          Model                            Python        Not Python    Julia   MATLAB        YAML   C/C++     CUDA     R      Shell   Py+YAML   AVG
                         # Discrepancies    496             46          12       10           9       5        4       3       3         1      543
          GPT-5                             70.4            65.2       66.7     90.0         75.0   60.0       0.0   100.0    33.3     100.0    70.0
          GPT-5 Mini                        63.7            69.6       75.0     90.0         66.7   60.0      25.0   100.0    33.3     100.0    64.3
          Gemini 3.1 Pro                    56.9            50.0       50.0     80.0         50.0   60.0       0.0    66.7     0.0     100.0    56.4
          GPT-OSS 20B                       46.8            52.2       50.0     60.0         66.7   60.0      50.0    33.3     0.0       0.0    47.1
          Gemini 2.5 Pro                    48.8            45.7       41.7     60.0         50.0   40.0      50.0    33.3    33.3       0.0    48.4
          GPT-5 Codex                       48.8            45.7       33.3     70.0         50.0   40.0      25.0    66.7    33.3     100.0    48.6
          GPT-OSS 120B                      44.6            39.1       33.3     80.0         41.7   40.0       0.0    33.3     0.0       0.0    44.0
          Gemini 2.5 Flash                  42.3            32.6       33.3     40.0         33.3   40.0       0.0    66.7    33.3       0.0    41.4
          GPT-5 Nano                        27.2            30.4       33.3     30.0         41.7   40.0       0.0    33.3     0.0       0.0    27.4
          Nemotron Super 49B v1.5           24.0            23.9       16.7     20.0         16.7   40.0      50.0    33.3    33.3       0.0    23.9
          Qwen3 30B Coder                   24.0            21.7       25.0     30.0         41.7    0.0       0.0    33.3     0.0       0.0    23.8
          Gemini 2.5 Flash Lite             24.0            19.6       16.7     20.0         50.0   20.0       0.0     0.0     0.0     100.0    23.8
          Nemotron Nano 9B v2               16.1            23.9       25.0     40.0         50.0    0.0       0.0     0.0     0.0       0.0    16.8
          Qwen3 30B Inst.                   22.0            19.6       25.0     20.0         33.3    0.0       0.0    33.3     0.0       0.0    21.7
          DeepSeek R1 32B                   16.7            13.0        8.3     20.0          8.3    0.0       0.0    66.7     0.0       0.0    16.4
          DeepSeek Coder 16B V2             10.1             4.3        8.3     10.0          0.0    0.0       0.0     0.0     0.0       0.0     9.6
          Qwen3 4B Inst.                    16.7             8.7       16.7     10.0          0.0    0.0       0.0    33.3     0.0       0.0    16.0
          Magistral 24B Small               14.5            10.9       25.0      0.0         25.0    0.0       0.0     0.0     0.0       0.0    14.2
          Devstral 24B Small                15.1             0.0        0.0      0.0          0.0    0.0       0.0     0.0     0.0     100.0    14.0
          Qwen3 30B Think.                  15.5            15.2        8.3     30.0          8.3   20.0       0.0    33.3     0.0       0.0    15.5
          Qwen3 4B Think.                   11.3             8.7        8.3      0.0         41.7    0.0       0.0     0.0     0.0       0.0    11.0
          DeepSeek R1 8B                     5.6             0.0        0.0      0.0          0.0    0.0       0.0     0.0     0.0       0.0     5.2

                            Table 6: Discrepancy recall by programming language on the synthetic S CI C O QA data.
                                      Real vs Synthetic Recall                                                       Gemini
              0.5                                                                            Model                   +GPT Gemini      GPT       ∆
                                                                                             GPT-5                    45.0     45.0    43.8    −1.3
              0.4
                                                                                             GPT-5 Mini               48.8     47.5    43.8    −3.7
                                                                                             Gemini 3.1 Pro           50.0     50.0    48.8    −1.3
              0.3
Recall Real




                                                                                             GPT-OSS 20B              47.5     45.0    42.5    −2.5
                                                                                             Gemini 2.5 Pro           41.2     40.0    40.0     0.0
              0.2                                                 GPT-OSS                    GPT-5 Codex              27.5     27.5    27.5     0.0
                                                                  GPT-5
                                                                  Gemini                     GPT-OSS 120B             42.5     37.5    40.0     2.5
                                                                  Nemotron
              0.1                                                 Qwen                       Gemini 2.5 Flash         36.2     32.5    33.8     1.3
                                                                  Mistral                    GPT-5 Nano               21.2     18.8    18.8     0.0
                                                                  DeepSeek
                                                                  r = 0.94 (all)             Nemotron 49B v1.5        26.2     23.8    21.2    −2.5
              0.0                                                 r = 0.98 (ex GPT-5 Fam.)
                                                                                             Qwen3 30B Coder          23.8     17.5    20.0     2.5
                    0.0   0.1   0.2       0.3     0.4       0.5      0.6         0.7         Gemini 2.5 Flash Lite    18.8     16.2    16.2     0.0
                                         Recall Synthetic
                                                                                             Nemotron Nano 9B v2      13.8      8.8    11.2     2.5
                                                                                             Qwen3 30B Inst.          20.0     13.8    17.5     3.7
Figure 9: Correlation between model recall on the syn-                                       DeepSeek R1 32B          21.2     17.5    17.5     0.0
thetic (x-axis) and real (y-axis) subsets of S CI C O QA.                                    DeepSeek Coder 16B V2     2.5      2.5     1.2    −1.2
Each point represents one of the 22 evaluated models.                                        Qwen3 4B Inst.           10.0      7.5     8.8     1.2
The dashed lines show linear fits across all models (blue)                                   Magistral 24B Small      16.2     15.0    13.8    −1.2
                                                                                             Devstral 24B Small       12.5      8.8    11.2     2.5
or excluding the GPT-5 family (orange). The r values
                                                                                             Qwen3 30B Think.         13.8     12.5    13.8     1.3
denote Pearson correlation coefficients.                                                     Qwen3 4B Think.           8.8      7.5     8.8     1.2
                                                                                             DeepSeek R1 8B            3.8      3.8     2.5    −1.2

   We further analyze recall by the position of the                                          Table 7: Model performance on the real-world S CI -
last relevant code file in the prompt, binning the                                           C O QA data for the 80 instances where both a GPT-5 and
samples and reporting results in Table 9. We ob-                                             Gemini 3.1 Pro ground truth discrepancy description
serve substantial recall degradation even for models                                         is available. The columns show the recall performance
that experience virtually zero truncation. GPT-5                                             when assessed against both (Gemini+GPT), Gemini-
drops from 77.5% to 50.7% and Gemini 3.1 Pro                                                 only, or GPT-only ground truth. A negative ∆ shows a
                                                                                             preference for Gemini’s ground truth descriptions, while
from 64.4% to 37.3% as the relevant file appears
                                                                                             a positive ∆ shows a preference for GPT’s.
later in the prompt.
   Both the code file position distribution and the
performance degradation demonstrate that the dom-                                            be influenced by the general capabilities of the
inant factor is long-context reasoning, not trunca-                                          models, the strong correlation confirms that the
tion, consistent with our analysis in Fig. 4 and prior                                       synthetic data preserves relative model rankings.
findings on long-context degradation (Liu et al.,                                            Consequently, absolute performance should be as-
2024b; Hsieh et al., 2024; Levy et al., 2024).                                               sessed on the real subset, while the synthetic subset
                                                                                             serves as a reliable proxy for relative model com-
C.4                 Real vs. Synthetic Recall                                                parison, justifying its use for scaling the benchmark
To assess the validity of our synthetic data genera-                                         to scientific domains where real-world examples
tion pipeline, we analyze the relationship between                                           are scarce.
model performance on real-world discrepancies
versus synthetic discrepancies. Fig. 9 visualizes                                            C.5     Gemini vs. GPT Ground Truth Recall
the recall and the relationship between the subsets.                                         A potential concern with the LLM-rephrased
We observe a high positive Pearson correlation                                               ground truth discrepancy descriptions is that a
of r = 0.94. When excluding the GPT-5 family                                                 model from the same family might have an ad-
(i.e., GPT-5, GPT-5 Mini, GPT-5 Nano, and GPT-5                                              vantage when evaluated against the ground truth
Codex) from the correlation analysis, the Pearson                                            (GT) that was generated by the same model or
correlation rises to r = 0.98, indicating that the                                           from the same family. To test this, we compare
GPT-5 family sits slightly off the shared trend line                                         per-model recall when evaluating against only the
that the other models follow closely. Apart from                                             GPT-generated versus Gemini-generated ground
this caveat, the relative ranking of models remains                                          truth descriptions across the 80 discrepancies for
consistent regardless of the data origin; models                                             which both are available. We report results in Ta-
that demonstrate strong capabilities on our syn-                                             ble 7. We find no evidence of systematic provider
thetic injections are reliably better at identifying                                         bias. In fact, the closed OpenAI models perform
real-world discrepancies. While this trend might                                             the same or better against the Gemini-generated
 Model                            P       R      F1       dicted discrepancies from GPT-5, Gemini 2.5 Pro,
                                                          and GPT-OSS 20B. Together with the existing dis-
 GPT-5                          84.1    63.6    72.4
                                                          crepancies from the real-world data in S CI C O QA
 GPT-5 Mini                     70.7    62.8    66.5
                                                          on these papers, this yields 129 verified paper-code
 GPT-OSS 20B                    68.9    63.6    66.1
                                                          discrepancies. Following the pooling methodology
 Gemini 2.5 Pro                 85.7    48.8    62.2
                                                          from information retrieval (Buckley and Voorhees,
 Gemini 3.1 Pro                 76.1    50.4    60.6
                                                          2004), where relevance judgments are aggregated
 GPT-OSS 120B                   61.1    52.7    56.6
                                                          from multiple systems to approximate a more com-
 Gemini 2.5 Flash               63.2    41.1    49.8
                                                          plete ground truth, we evaluate all models against
 GPT-5 Codex                    79.1    34.9    48.4
                                                          the pooled set. In case multiple ground truths exist
 Gemini 2.5 Flash Lite          57.1    30.2    39.5
                                                          for the same discrepancy, e.g., when both GPT-5
 Nemotron Super 49B v1.5        56.1    30.2    39.3
                                                          and Gemini 2.5 Pro surfaced the same unannotated
 GPT-5 Nano                     44.3    34.1    38.5
                                                          discrepancy, we consider it detected if the predic-
 Devstral 24B Small             45.6    27.9    34.6
                                                          tion matches at least one description. Table 8 re-
 Qwen3 30B Inst.                42.6    27.1    33.2
                                                          ports the results.
 Qwen3 30B Coder                39.1    27.9    32.6
                                                             GPT-5 achieves the highest F1 (72.4%), bal-
 Qwen3 30B Think.               62.5    18.6    28.7
                                                          ancing precision (84.1%) and recall (63.6%) the
 Qwen3 4B Inst.                 38.9    22.5    28.5
                                                          best, followed by GPT-5 Mini and GPT-OSS 20B
 DeepSeek R1 32B                32.8    22.5    26.7
                                                          (66.5% and 66.1%). As established in the pooling
 Magistral 24B Small            28.7    24.0    26.2
                                                          literature, systems contributing to the pool have
 Qwen3 4B Think.                61.5    14.7    23.8
                                                          a structural advantage, so the evaluations of GPT-
 Nemotron Nano 9B v2            23.5    17.8    20.3
                                                          5, Gemini 2.5 Pro, and GPT-OSS 20B should be
 DeepSeek Coder 16B V2          11.1     6.2     8.0
                                                          viewed as upper bounds (Buckley and Voorhees,
 DeepSeek R1 8B                 14.3     1.6     2.8
                                                          2004). Nonetheless, clear patterns emerge: a
                                                          precision–recall tradeoff is evident across models,
Table 8: Precision (P), Recall (R), and F1 scores on 20
NLP and CV papers with 129 discrepancies. Ground          with Gemini 2.5 Pro reaching the highest precision
truths have been pooled from the predictions of GPT-      (85.7%) at the cost of recall (48.8%). GPT-OSS
5, Gemini 2.5 Pro, and GPT-OSS 20B. Additionally,         20B and 120B are the strongest open-weight mod-
discrepancies from the real-world data of S CI C O QA     els, while the remaining open-weight models lag
have been added.                                          behind considerably (next best: Nemotron 49B, F1
                                                          of 39.3%). Despite the pool bias favoring contribut-
                                                          ing systems, recall remains the primary bottleneck:
ground truth. Gemini 3.1 Pro performs slightly
                                                          even under favorable conditions, the best model
better against its own generations (∆ = −1.3),
                                                          detects at most 63.6% of verified discrepancies.
but the other Gemini models do not exhibit any
bias towards these descriptions. Among third-
party model families, which serve as unbiased con-
trols since they are not affiliated with either GT
provider, results are similarly balanced: DeepSeek
and NVIDIA models show no consistent prefer-
ence, while the Qwen models slightly favor GPT
GT (mean ∆ = +2.0pp). Across all 22 models,
the overall mean ∆ is +0.2pp with a maximum
absolute difference of just 3.7pp, and 9 models fa-
vor GPT GT versus 8 favoring Gemini GT (5 tied).
These small, inconsistent differences suggest that
the choice of ground truth source does not intro-
duce meaningful evaluation bias.

C.6   Pooled Ground Truth Results
In §5.2 we created a pooled ground truth for 20
NLP and CV papers by manually verifying the pre-
                                       Bin         All       0-32k      32-64k     64-131k ≥ 131k
                Model             # Samples        635        253        210        105      67
                GPT-5                              65.8        77.5       62.9       53.3       50.7
                GPT-5 Mini                         61.7        75.1       59.5       44.8       44.8
                Gemini 3.1 Pro                     55.0        64.4       55.7       41.9       37.3
                GPT-OSS 20B                        46.5        60.1       41.9       35.2       26.9
                Gemini 2.5 Pro                     47.1        58.1       43.8       37.1       31.3
                GPT-5 Codex                        45.5        57.7       41.9       36.2       25.4
                GPT-OSS 120B                       43.6        59.3       38.6       28.6       23.9
                Gemini 2.5 Flash                   40.5        51.4       40.5       24.8       23.9
                GPT-5 Nano                         26.3        34.8       22.4       21.9       13.4
                Nemotron Super 49B v1.5            23.9        29.6       20.5       20.0       19.4
                Qwen3 30B Coder                    23.5        27.3       20.0       24.8       17.9
                Gemini 2.5 Flash Lite              22.8        33.6       18.1       14.3       10.4
                Nemotron Nano 9B v2                16.2        21.7       13.8       14.3        6.0
                Qwen3 30B Inst.                    21.3        26.5       20.5       12.4       17.9
                DeepSeek R1 32B                    16.9        25.7       16.7        4.8        3.0
                DeepSeek Coder 16B V2               8.7        13.8        4.3        5.7        7.5
                Qwen3 4B Inst.                     15.1        21.7       12.9        8.6        7.5
                Magistral 24B Small                14.5        20.9       14.3        6.7        3.0
                Devstral 24B Small                 13.7        19.0       11.9        5.7       11.9
                Qwen3 30B Think.                   15.0        19.4       14.3        7.6       11.9
                Qwen3 4B Think.                    10.6        15.4       11.4        3.8        0.0
                DeepSeek R1 8B                      4.9         5.5        4.8        2.9        6.0

Table 9: Model performance by position of the last relevant code file in the prompt. The All column considers the
full S CI C O QA dataset, the following columns partition the data based on the position of the last relevant code file
in the prompt.
C.7     Detailed Results per Model

                                Real+Synthetic                  Real                           Synthetic                          Type
Model                          # Preds.   Recall      All        GH        RP         All         CS       Other      CO          PO           Diff.
        # Real | # Synthetic   92 | 543   92 | 543   92 | 0     42 | 0    50 | 0     0 | 543    0 | 286    0 | 257   12 | 55     29 | 64   51 | 424
GPT-5                             4.6       65.8      41.3       54.8      30.0       70.0       65.7       74.7      70.1        51.6         68.0
GPT-5 Mini                        5.3       61.7      46.7       59.5      36.0       64.3       58.7       70.4      70.1        45.2         63.8
Gemini 3.1 Pro                    3.8       55.0      46.7       59.5      36.0       56.4       54.9       58.0      62.7        41.9         56.4
GPT-OSS 20B                       5.8       46.5      42.4       47.6      38.0       47.1       41.6       53.3      61.2        40.9         45.5
Gemini 2.5 Pro                    3.5       47.1      39.1       54.8      26.0       48.4       43.0       54.5      46.3        34.4         49.7
GPT-5 Codex                       2.2       45.5      27.2       31.0      24.0       48.6       45.5       52.1      59.7        28.0         46.9
GPT-OSS 120B                      5.0       43.6      41.3       50.0      34.0       44.0       40.6       47.9      52.2        40.9         42.9
Gemini 2.5 Flash                  4.0       40.5      34.8       47.6      24.0       41.4       36.0       47.5      47.8        33.3         40.8
GPT-5 Nano                        3.8       26.3      19.6       26.2      14.0       27.4       22.7       32.7      40.3        17.2         26.1
Nemotron Super 49B v1.5           5.1       23.9      23.9       28.6      20.0       23.9       23.8       24.1      37.3        15.1         23.8
Qwen3 30B Coder                   4.3       23.5      21.7       26.2      18.0       23.8       23.4       24.1      38.8        11.8         23.6
Gemini 2.5 Flash Lite             2.8       22.8      17.4       31.0       6.0       23.8       19.2       28.8      32.8        11.8         23.6
Nemotron Nano 9B v2               6.7       16.2      13.0       14.3      12.0       16.8       15.0       18.7      13.4        16.1         16.6
Qwen3 30B Inst.                   3.8       21.3      18.5       21.4      16.0       21.7       17.8       26.1      32.8        15.1         20.8
DeepSeek R1 32B                   4.7       16.9      19.6       31.0      10.0       16.4       14.3       18.7      23.9        14.0         16.4
DeepSeek Coder 16B V2             3.5        8.7       3.3        2.4       4.0        9.6        9.1       10.1      19.4         3.2          8.2
Qwen3 4B Inst.                    2.8       15.1       9.8       14.3       6.0       16.0       12.9       19.5      22.4        11.8         14.7
Magistral 24B Small               4.3       14.5      16.3       21.4      12.0       14.2       13.3       15.2      19.4        14.0         13.9
Devstral 24B Small                4.8       13.7      12.0       16.7       8.0       14.0       11.2       17.1      25.4        15.1         11.8
Qwen3 30B Think.                  1.7       15.0      12.0       19.0       6.0       15.5       15.0       16.0      23.9         4.3         15.8
Qwen3 4B Think.                   1.6       10.6       7.6        7.1       8.0       11.0        9.1       13.2      11.9         7.5         10.9
DeepSeek R1 8B                    4.2        4.9       3.3        7.1       0.0        5.2        6.6        3.5       9.0         1.1          5.1

Table 10: Detailed recall performance of all evaluated models in the S CI C O QA dataset. # Preds. refers to the
average number of predictions the model makes per paper, GH stands for discrepancies originating from GitHub,
RP originating from reproducibility papers. The synthetic data is split by the Computer Science (CS) domain and
Others. The discrepancies are further split by Type, specifically Code Omissions (CO), Paper Omissions (PO), and
Differences (Diff ). The # Real/Synthetic row indicates how many samples per column are from the real or synthetic
data.

C.8     Code Only Ablation Results

                                             Real                                  Synthetic                     Real+Synthetic
      Model                       P+C          C            ∆            P+C           C           ∆          P+C            C             ∆
      GPT-5                        41.3       29.3     −12.0             70.0         51.0      −19.0          65.8        47.9      −18.0
      GPT-5 Mini                   46.7       23.9     −22.8             64.3         39.6      −24.7          61.7        37.3      −24.4
      Gemini 3.1 Pro               46.7       25.0     −21.7             56.4         42.0      −14.4          55.0        39.5      −15.4
      GPT-OSS 20B                  42.4       17.4     −25.0             47.1         33.3      −13.8          46.5        31.0      −15.4
      Gemini 2.5 Pro               39.1       18.5     −20.7             48.4         33.1      −15.3          47.1        31.0      −16.1
      GPT-5 Codex                  27.2       12.0     −15.2             48.6         28.0      −20.6          45.5        25.7      −19.8
      GPT-OSS 120B                 41.3       22.8     −18.5             44.0         34.6       −9.4          43.6        32.9      −10.7
      Gemini 2.5 Flash             34.8       17.4     −17.4             41.4         28.5      −12.9          40.5        26.9      −13.5
      Average                      39.9       20.8 −19.2                 52.5         36.3 −16.3               50.7        34.0 −16.7

Table 11: Discrepancy recall of the top 8 performing models depending on the input: The P+C column refers to the
performance when providing paper and code, C for only providing the code, and ∆ shows the absolute difference
between the two.
D    Example Discrepancies in S CI C O QA




 Type       Category    Description
 Paper      Algorithm Gemini 3.1
 Omission             The paper discusses utilizing Feature-wise Linear Modulation (FiLM) to adjust convolutional
                      model features based on the loss weights. For this modulation, it describes using multi-layer
                      perceptrons to compute unconstrained scaling (σ) and shifting (µ) parameter bounds which are
                      applied as affine transformations to the features. In contrast, the code implements a ‘FiLMBlock‘
                      that processes the shift (‘mu‘) and scale (‘sigma‘) through a sigmoid activation function prior to
                      applying them to the features. The difference is the undocumented use of an output sigmoid layer
                      on the FiLM parameters in the implementation which restricts the scaling factor to solely shrink the
                      features and the shift translation strictly to positive values compared to the unrestricted parameter
                      bounds discussed in the text.

                        GPT-5
                        The paper conditions layers using FiLM by mapping the loss-parameter vector λ through two
                        MLPs to obtain σ and µ and then applying the affine transform f˜ = σ ⊙ f + µ; there is no mention
                        of any output activation on σ or µ, and in the style transfer details it explicitly states that σ and
                        µ are computed via affine maps. In the repository, the FiLMBlock applies a sigmoid activation
                        to both µ and σ before using them, thereby constraining both to the (0,1) range. Thus, the code
                        restricts the FiLM coefficients to be positive and bounded, whereas the paper’s description implies
                        unconstrained affine coefficients produced by linear layers. This is a clear deviation between the
                        implementation and the method described in the paper.
 Paper      Model       Gemini 3.1
 Omission               The paper states that a three-layer GNN is trained for the node-classification tasks before generating
                        explanations, but omits any description of batch normalization layers being used as part of
                        the architecture. However, the code implementation for node classification models includes
                        batch normalization by default (‘args.bn = True‘). Specifically, in the GCN model code, batch
                        normalization is applied after the first and second GCN layers during the forward pass. This
                        introduces an undocumented architectural choice present in the code but not mentioned in the
                        paper.

                        GPT-5
                        The paper states that, following GNNExplainer’s setup, a three-layer GNN is first trained and then
                        explained, but it does not mention any batch normalization in this backbone network. In the public
                        code for node-classification tasks (synthetic datasets), the GCN model enables batch normalization
                        by default (args.bn=True) and applies tf.keras.layers.BatchNormalization after all GCN layers
                        except the last, i.e., after the first and second layers in a 3-layer GCN. This BatchNorm usage is not
                        described in the paper’s model description or experimental setup, making it an undocumented
                        architectural difference between the paper and the released code.
 Code       Data         Gemini 3.1
 Omission               The paper states that for the MNIST experiments, the "Original + CGN" baseline is trained on
                        a combination of real and counterfactual images. However, the implemented code for training
                        the MNIST classifiers does not combine these datasets. The data loading logic defined in
                        ‘get_tensor_dataloaders‘ exclusively loads the counterfactual tensor dataset when a counterfactual
                        dataset name is evaluated, without appending or mixing in the original training dataset. Therefore,
                        the code implementation trains solely on counterfactual data, lacking the original data indicated by
                        the paper.

                        GPT-5
                        The paper describes training classifiers using a combination of original MNIST data and
                        CGN-generated counterfactual images. This is explicitly stated in Section 3.2 and reinforced by
                        the MNIST ablation (Appendix A.3) and Table 2 which presents an “Original + CGN” setting.
                        In contrast, the released MNIST training code (mnists/train_classifier.py) only supports training
                        on a single dataset per run; the provided datasets and README usage instruct training on the
                        counterfactual dataset alone (e.g., wildlife_MNIST_counterfactual) without combining with
                        original data. Thus, the code implements CF-only training for MNIST classifiers rather than the
                        paper’s combined original+CF setup, constituting a mismatch in the MNIST training protocol.

Table 12: Discrepancy ground truth examples from the S CI C O QA dataset generated by both Gemini 3.1 Pro and
GPT-5, including discrepancy type and category annotations. All samples are from real data.
    Type         Category   Description
    Code         Training   Gemini 3.1
    Omission                The paper algorithm outlines that within each global aggregation round, each worker performs τ
                            local update steps on different minibatches and accumulates the computed gradients to represent
                            the overall worker gradient. However, in the code, the ‘federated_worker_process‘ loops over the
                            dataloader, performs a single forward and backward pass, and then immediately unconditionally
                            breaks out of the loop. Additionally, the lines of code previously intended for accumulating
                            gradients (‘accum_grads = add_param_list(accum_grads, worker_grads)‘) are commented out,
                            which means the code effectively enforces τ = 1.

                            GPT-5
                            The paper’s FL formulation and Algorithm 1 state that each worker performs τ local updates
                            per round and accumulates
                                             P            the resulting gradients g_k^(t,b) into an accumulated stochastic
                            gradient g_k^(t)= _{b=0}^{τ −1} g_k(θ_k^{(t,b)}), which is then used by LBGM for projection
                            and communication. In the code, the federated worker loop processes only one minibatch and
                            immediately breaks, with the lines that would accumulate gradients across batches commented out;
                            an assertion on τ is present but no actual multi-step accumulation is performed. Consequently,
                            the implemented training uses only a single local update per round (effectively τ =1) rather than
                            accumulating τ local updates as described in the paper.
    Difference   Eval       Gemini 3.1
                            The paper describes the accuracy-based confidence score as the mean accuracy of the candidate
                            responses, computed by taking the average of the indicator functions that check if each
                            sampled response matches the ground-truth answer. In the provided code, the confidence score
                            calculation is implemented by returning the maximum value of the sampled correctness scores
                            (‘max(probabilities)‘) instead of their average. This creates a discrepancy where the code leverages
                            a binary indicator reflecting whether at least one correct response was generated (1 if yes, 0
                            otherwise), rather than the continuous proportion of correct responses specified by the formula in
                            the paper.

                            GPT-5
                            The paper specifies “accuracy-based confidence” for a question as the mean accuracy across K
                            sampled responses, i.e., the fraction of correct generations among the K samples. In the code,
                            however, the function calculate_confidence takes the list of per-sample correctness indicators
                            (greedy_scores) and returns max(greedy_scores), which reduces confidence to a binary value: 1 if
                            any sample is correct, 0 otherwise. Moreover, while the code also computes greedy_scores_avg
                            (the intended mean), it does not use that for the confidence fed into the downstream datasets;
                            instead, the binary max value is stored as "confidence" and used for reward/align data. Thus, the
                            implemented confidence deviates from the paper’s definition by using maximization rather than
                            averaging.
    Difference   Loss       Gemini 3.1
                            The paper defines the P2 penalty term as the sum of min(ξ(x, y), 0)2 , which applies a squared
                            penalty strictly to negative evaluations of ξ(x, y) in order to enforce the provided optimal
                            transport constraints. However, the code implements this term using ‘torch.clamp(full_xi_vals,
                            min=0)**2‘. The PyTorch function with ‘min=0‘ imposes a lower bound of 0, mathematically
                            returning max(ξ(x, y), 0)2 , which zeroes out the negative values and squares the positive ones.
                            Consequently, the codebase incorrectly penalizes positive values of ξ(x, y) instead of negative
                            values as stated in the methodology.

                            GPT-5
                            The paper defines the second penalty P2 to enforce the admissibility constraints (ϕ, ϕ^c) ∈ ADM(c)
                            by penalizing only negative values of ξ(x,y) = c(x,y) − ϕ(x) − ϕ^c(y), specifically using min(ξ(x,y),
                            0)^2. In the code, P2 is implemented in admissable_penalty as torch.mean(torch.clamp(full_xi_vals,
                            min=0)**2), which penalizes positive ξ values (since negative values are clamped to zero).
                            Therefore, the implementation reverses the intended sign: the paper penalizes violations where ξ <
                            0, while the code penalizes cases where ξ > 0. This directly contradicts the paper’s definition for
                            P2.

Table 12: Discrepancy ground truth examples from the S CI C O QA dataset generated by both Gemini 3.1 Pro and
GPT-5, including discrepancy type and category annotations. All samples are from real data. (Continued)
E    Example Synthetic Discrepancies in S CI C O QA




Discrepancy                                               Code Change
Paper:      https://arxiv.org/abs/1906.                   Code: https://github.com/concavegit/kfda
09436
Domain: Machine Learning (stat.ML)                        File: kfda/kfda.py
The paper emphasizes that classification in FDA is        centroids_ = m_classes @ self.weights_
performed using Euclidean distances in the Fisher         + centroids_ = centroids_ / (np.linalg.norm(
subspace (and shows its equivalence to LDA under                centroids_, axis=1, keepdims=True) + 1e-12)
Euclidean metrics). The code normalizes both pro-         self.clf_ = NearestCentroid().fit(centroids_, self
jected samples and class centroids to unit norm                 .classes_)
prior to classification. This switches the effec-         # ...
tive decision metric from Euclidean distance to an        - return pairwise_kernels(X, self.X_, metric=self.
angular/cosine-like similarity, diverging from the              kernel, **self.kwds) @ self.weights_
Euclidean geometry prescribed in the paper.               + Z = pairwise_kernels(X, self.X_, metric=self.
                                                                kernel, **self.kwds) @ self.weights_
                                                          + Z_norm = np.linalg.norm(Z, axis=1, keepdims=True
                                                                ) + 1e-12
                                                          + return Z / Z_norm
                                                          # ...
                                                          new_centroids = y_onehot.T @ projections /
                                                                y_onehot.T.sum(1)
                                                          + new_centroids = new_centroids / (np.linalg.norm(
                                                                new_centroids, axis=1, keepdims=True) + 1e-12)
                                                          concatenated_classes = np.concatenate([self.
                                                                classes_, new_classes])
                                                          concatenated_centroids = np.concatenate([self.clf_
                                                                .centroids_, new_centroids])
Paper:     https://arxiv.org/abs/2409.                    Code: https://github.com/nz-gravity/sgvb_psd
13224
Domain: General Relativity and Quantum Cosmol-            File: src/sgvb_psd/postproc/plot_coherence.py
ogy (gr-qc)                                               def compute_coherence(pxx, pyy, pxy):
The paper defines squared coherence as the                -      coh_q = np.real(np.abs(pxy) ** 2) / np.real(
magnitude-squared of the complex cross-spectrum                 pxx) / np.real(pyy)
normalized by the product of the auto-spectra. In         +      coh_q = (np.real(pxy) ** 2) / (np.real(pxx) *
the code, coherence is computed using only the                  np.real(pyy))
square of the real part of the cross-spectrum (co-               coh_uniform = None
spectrum) divided by the product of the auto-spectra.
                                                          File: src/sgvb_psd/postproc/plot_triangle_psd_coherence.py
Thus, while the paper’s definition uses |Sxy |2 ,
                                                          def compute_coherence(pxx, pyy, pxy):
the implementation effectively uses Re(Sxy )2 ,
                                                          -      coh_q = np.real(np.abs(pxy) ** 2) / np.real(
ignoring the quadrature (imaginary) component.
                                                                pxx) / np.real(pyy)
This changes the coherence measure away from
                                                          +      coh_q = (np.real(pxy) ** 2) / (np.real(pxx) *
magnitude-squared coherence to co-coherence,
                                                                np.real(pyy))
which is not described in the paper.
                                                                 coh_uniform = None
Paper:      https://arxiv.org/abs/1911.                   Code: https://github.com/bowenc0221/panoptic-deeplab
10194
Domain: Computer Vision (cs.CV)                           File: segmentation/model/meta_arch/panoptic_deeplab.py
The paper defines the offset vector in pixel space        result = OrderedDict()
and groups pixels by moving each pixel by its pre-        for key in pred.keys():
dicted offset and assigning it to the nearest predicted          out = F.interpolate(pred[key], size=
center. The code upscales predictions to the input              input_shape, mode=’bilinear’, align_corners=
resolution but does not scale the offsets accordingly           True)
during this upsampling, meaning the offsets are           -      if ’offset’ in key:
left in a lower-resolution coordinate system when         -          scale = (input_shape[0] - 1) // (pred[key
grouped at full resolution. This contradicts the pa-            ].shape[2] - 1)
per’s grouping formulation that assumes offsets and       -          out *= scale
coordinates are in the same resolution.                          result[key] = out
                                                          return result

Table 13: Examples from the synthetic S CI C O QA data. The Code Change column shows the code snippet that has
been modified to create a paper-code discrepancy.
  Discrepancy                                               Code Change
  Paper:       https://arxiv.org/abs/2302.                  Code: https://github.com/saitta-s/INRs-4DFlowMRI
  12835
  Domain: Image and Video Processing (eess.IV)              File: fit_inr.py
  The paper specifies that training uses only a data        def closure():
  fidelity term plus enforcement of the no-slip condi-             optimizer.zero_grad()
  tion on the wall, explicitly noting no physics resid-     +      X.requires_grad_(True)
  uals. In the code, an additional divergence-free                 outputs = model(X)
  penalty term is added by computing spatial deriva-               obs_loss = loss_fn(outputs[:-n_wall, :], Y0)
  tives of the velocity outputs with respect to the input          wall_loss = loss_fn(outputs[-n_wall:, :],
  coordinates and penalizing their sum (divergence),              wall_vel[wall_idx, :])
  scaled by a configurable weight. This introduces an       +      if cfg.div_weight > 0:
  explicit incompressibility prior not described in the     +             u = outputs[:, 0]
  paper.                                                    +             v = outputs[:, 1]
                                                            +             w = outputs[:, 2]
                                                            +             grads_u = torch.autograd.grad(u.sum(), X,
                                                                  create_graph=True, retain_graph=True)[0]
                                                            +             grads_v = torch.autograd.grad(v.sum(), X,
                                                                  create_graph=True, retain_graph=True)[0]
                                                            +             grads_w = torch.autograd.grad(w.sum(), X,
                                                                  create_graph=True, retain_graph=True)[0]
                                                            +             div = grads_u[:, 0] + grads_v[:, 1] +
                                                                  grads_w[:, 2]
                                                            +             div_loss = (div ** 2).mean()
                                                            +             loss = obs_loss + wall_loss + cfg.
                                                                  div_weight * div_loss
                                                            +      else:
                                                                          loss = obs_loss + wall_loss
                                                                   loss.backward()
                                                                   return loss
  Paper:      https://arxiv.org/abs/2412.                   Code: https://github.com/HPMolSim/FastSpecSoG.jl
  04595
  Domain: Numerical Analysis (math.NA)                      File: src/FFCT/interpolate.jl
  The paper derives a single Fourier–Chebyshev rep-         for j in 1:size(H_r, 2)
  resentation for the long-range part and does not                 k_yj = k_y[j]
  duplicate the zero wavenumber contribution. In the               for i in 1:size(H_r, 1)
  code, the zero in-plane Fourier mode is already com-                  k_xi = k_x[i]
  puted via a dedicated “zeroth-order” 1D path, but                     k2 = k_xi^2 + k_yj^2
  the spectral path is also modified to include the kx =    -          if !(k2 $\approx$ zero(T))
  ky = 0 contribution. This leads to a double counting      -                 phase = phase_x[i] * phase_y[j]
  of the zeroth Fourier mode in the long-range part,        -                 cheb_ij = cheb_mat[i, j]
  which the paper’s formulation does not include.           -                 for k in 1:size(H_r, 3)
                                                            -                       r_zk = r_z[k]
                                                            -                       H_r[i, j, k] += q * phase *
                                                                  cheb_ij(abs(z - r_zk))
                                                            -                 end
                                                            +           phase = phase_x[i] * phase_y[j]
                                                            +           cheb_ij = cheb_mat[i, j]
                                                            +           for k in 1:size(H_r, 3)
                                                            +                 r_zk = r_z[k]
                                                            +                 H_r[i, j, k] += q * phase * cheb_ij(
                                                                  abs(z - r_zk))
  Paper:     https://arxiv.org/abs/2402.                    Code:                   https://github.com/LDeng0205/
  18396                                                     confidence-bootstrapping
  Domain: Biomolecules (q-bio.BM)                           File: utils/utils.py
  The paper describes that the confidence model             def crop_beyond(complex_graph, cutoff, all_atoms):
  reasons about local interactions by feeding only                ligand_pos = complex_graph[’ligand’].pos
  residues whose Cα lies within 20 Å of any pre-            +     center = ligand_pos.mean(dim=0, keepdim=True)
  dicted ligand atom. The code instead crops the                  receptor_pos = complex_graph[’receptor’].pos
  receptor using a centroid-based distance (distance        -     residues_to_keep = torch.any(torch.sum((
  from Cα to the ligand centroid), not the minimum                ligand_pos.unsqueeze(0) - receptor_pos.
  distance to any ligand atom. This changes which                 unsqueeze(1)) ** 2, -1) < cutoff ** 2, dim=1)
  residues are kept and contradicts the paper’s “any        +     residues_to_keep = torch.sum((receptor_pos -
  atom” criterion.                                                center) ** 2, -1) < cutoff ** 2

Table 13: Examples from the synthetic S CI C O QA data. The Code Change column shows the code snippet that has
been modified to create a paper-code discrepancy. (Continued)
F      Prompts
F.1     GitHub Issue Discrepancy Extraction

    PROMPT | GitHub Issue Discrepancy Extraction

    You are an assistant that analyzes GitHub issues of scientific codebases. Your primary goal is to determine if the code repository contains any
    inconsistency, discrepancy, or mismatch between what is described in the paper and implemented in the code. For this, you analyze a GitHub
    issue and determine whether it reports a concrete discrepancy.
    A **concrete discrepancy** means the issue clearly describes a mismatch between what is stated in the paper (e.g., formulas, algorithms,
    hyperparameters, methods, logic, or processes) and what is implemented in the repository’s code.
    Important: Only label issues as a discrepancy if they point to a _specific, concrete difference_ between paper and code. Do not label general
    reproducibility problems, missing details, or unrelated bugs as discrepancies.
    ## Not a discrepancy issue
    Label as **Not a discrepancy issue** if:
    - The issue is about anything other than a difference between the paper and the code.
    - The issue describes reproducibility problems (e.g., different results) but does **not** identify a concrete paper-code mismatch.
    - The issue is about missing information needed to reproduce results without pointing to a mismatch.
    - The issue is about bugs or errors unrelated to the paper’s described methods or experiments.
    ## Discrepancy issue
    Label as **Discrepancy issue** if:
    - The issue explicitly reports a mismatch between the paper and the code implementation.
    - The mismatch can involve hyperparameters, formulas, algorithms, logic, processes, or other settings described in the paper.
    ## Response Format
    After analyzing the issue in detail and applying the definitions above, provide your final classification in the structure defined below:
    ### Final Answer
    “‘yaml
    issue_label: <the issue label: "Not a discrepancy issue" or "Discrepancy issue">
    “‘
    ## Issue
    {issue}



F.2     GitHub Issue Discrepancy Verification

    PROMPT | GitHub Issue Discrepancy Verification

    Your task is to verify a paper-code discrepancy described in a GitHub issue. Your goal is to verify whether the discrepancy is valid or not.
    Follow these steps to verify the discrepancy:
    1. Analyze the issue and ensure you understand exactly the claimed discrepancy between the paper and the code.
    2. Analyze the paper and the code and understand in detail the relevant paper sections and code files.
    3. Using your understanding of paper, code, and the discrepancy in the issue, analyze whether the discrepancy is valid or not. A discrepancy is
    valid, if the claimed discrepancy actually exists and there is a difference between the paper description and the code.
    4. Provide your final judgement whether the reported discrepancy is valid or not, and if so a summary and the relevant paper sections and
    code files in the format below:
    “‘yaml
    is_valid_discrepancy: <yes or no>
    is_valid_discrepancy_reason: <provide a short explanation for your judgement>
    discrepancy_summary: <if valid provide the following description, else this should be empty: a summary of the discrepancy between the paper
    and the code in 3-8 sentences. Your description should contain three parts focusing on the discrepancy: 1) summarize what is described in the
    paper, 2) summarize what is implemented in the code, and 3) summarize the difference. Do not speculate about the impact.>
    relevant_paper_sections:
    - <verbatim quote any parts from the paper that are relevant to the discrepancy>
    - <if there are multiple relevant parts, paste each of them.>
    relevant_code_files:
    - <name any code files that are relevant to the discrepancy by providing the file name>
    - <if there are multiple relevant code files, paste each of them.>
    “‘
    ## Issue
    {issue}
    ## Paper
    {paper}
    ## Code
    {code}
F.3   Reproducibility Paper Discrepancy Extraction

  PROMPT | Reproducibility Paper Discrepancy Extraction

  You are an assistant that analyzes reproducibility reports of scientific papers. Your primary goal is to detect whether the report identifies any
  discrepancies between the original paper and the original code repository.
  ## What counts as a discrepancy - A concrete paper–code discrepancy means the report clearly describes a mismatch between what is stated
  in the original paper (e.g., formulas, algorithms, logic, methods, processes, or other settings) and what is implemented in the original code
  repository. - Each distinct mismatch should be reported as a separate item. - Hyperparameter mismatches (e.g., learning rate, batch size,
  dropout rate) do not count as discrepancies, since these are typically configurable in code repositories. - If the report only describes differences
  between reproduced results and original results, without identifying a paper–code mismatch, do not list it. - If the report speculates about a
  possible mismatch (uncertain or ambiguous wording), still list it, but mark it with confindence: low.
  ## What does not count as a discrepancy - General reproducibility problems (e.g., “we could not match the reported results”).
  - Missing information in the paper (e.g., “the authors did not specify X”).
  - Missing implementation in the original code repository (e.g., “the authors did not provide the code for X”).
  - Bugs or errors in the code that are unrelated to what the paper describes.
  - Differences between reproduced implementation/results and the original paper.
  ## Output format
  Summarize all discrepancies found in the following structure, providing a description of the discrepancy, evidence supporting the discrepancy
  as verbatim quotes from the reproducibility report, and a confidence estimate of the authors on the reported discrepancy.
  “‘yaml
  concrete_paper_code_discrepancies:
  - description: "<3–8 sentence descriptive summary of the first discrepancy>"
  evidence:
  - "<paste any evidence (e.g. a paragraph describing the discrepancy) from the reproducibility report that support the discrepancy.>"
  - "<If there are multiple evidence, paste each of them.>"
  confidence: <Estimate of the confidence the authors have on the reported discrepancy. One of: low, medium, high>- ... “‘
  If no discrepancies are reported, return:
  “‘yaml
  concrete_paper_code_discrepancies: []
  “‘
  Reproducibility Report:
  {paper}



F.4   Reproducibility Paper Discrepancy Verification

  PROMPT | Reproducibility Paper Discrepancy Verification

  Your task is to verify a paper-code discrepancy described in a reproducibility report. You will be provided with a summary of the discrepancy
  according to the report, and potentially multiple quotes from the reproducibility report that support the discrepancy. Your goal is to verify
  whether the discrepancy is valid or not.
  Follow these steps to verify the discrepancy:
  1. Analyze the description and evidence from the reproducibility report and ensure you understand exactly the claimed discrepancy between
  the paper and the code.
  2. Analyze the paper and the code and understand in detail the relevant paper sections and code files.
  3. Using your understanding of paper, code, and the reported discrepancy, analyze whether the discrepancy is valid or not. A discrepancy is
  valid, if the claimed discrepancy actually exists, i.e. the described difference between paper and code exists.
  4. Provide your final judgement whether the reported discrepancy is valid or not, and if so a summary and the relevant paper sections and
  code files in the format below:
  “‘yaml
  is_valid_discrepancy: <yes or no>
  is_valid_discrepancy_reason: <provide a short explanation for your judgement>
  discrepancy_summary: <if valid provide the following description, else this should be empty: a summary of the discrepancy between the paper
  and the code in 3-8 sentences. Your description should contain three parts focusing on the discrepancy: 1) summarize what is described in the
  paper, 2) summarize what is implemented in the code, and 3) summarize the difference. Do not speculate about the impact.>
  relevant_paper_sections:
  - <verbatim quote any parts from the paper that are relevant to the discrepancy>
  - <if there are multiple relevant parts, paste each of them.>
  relevant_code_files:
  - <name any code files that are relevant to the discrepancy by providing the file name>
  - <if there are multiple relevant code files, paste each of them.>
  “‘
  ## Reproducibility Report with Discrepancy
  {discrepancy_in_report}
  ## Paper
  {paper}
  ## Code
  {code}
F.5   Synthetic Discrepancy Generation
Below the prompt for generating synthetic discrepancies for computer science papers. For non-CS paper,
we remove the discrepancy type definition and prediction from the prompt.

  PROMPT | Synthetic Discrepancy Generation

  Your task is to generate 5 realistic paper–code discrepancies by introducing small, conceptually meaningful modifications to the codebase of
   the provided research paper.
   Follow these steps to perform the edit:
  1. Carefully read and understand both the research paper and the entire code repository provided below. Your goal is to identify the key ideas,
   methods, and components described in the paper and how they correspond to the implementation in the code.
   2. Your changes must adhere to the following constraints:
  - **Small**: The changes must affect a few lines of code or a short function. It may affect multiple files, but only to the extent necessary to
   create a coherent and realistic discrepancy.
  - **Relevance**: The changes must relate directly to a core scientific or algorithmic idea of the paper and would likely have an impact on
   reproducibility of results and validity of claims.
  - **Significance**: The changes must introduce a conceptual discrepancy — not a simple hyperparameter, or formatting change, or a change
   that could be fixed via a simple (command line) argument.
  - **Scope**: The changes should not all rely on already implemented features of the code base, but also implement new features or introduce
   modifications. Balance between relying on existing features and implementing new features.
  - **No Comments**: Do not add comments to the changed code which would easily allow to identify the discrepancy.
  - **No Bugs**: The introduced discrepancies should not be bugs, i.e., code that could be detected as erroneous by inspecting the code itself.
  The discrepancy must be related to both the paper and the code to be identified.
  - **No Implications**: The discrepancies must not rely on anything the paper only implies or assumes, but the paper must clearly conflict with
   the code after the change, or omit an important concept that is implemented in the changed code.
   3. Your changes can be one of the following types. You can create multiple discrepancies of the same or different types.
  - **Paper Omission**: Modify the code such that it implements a concept or idea that is not described in the paper.
  - **Code Omission**: Modify the code such that it drops a specific concept or idea that is described in the paper.
  - **Difference**: Modify the code such that there is a difference between the paper and the code, i.e., the paper describes one thing and the
   code implements another, e.g., by changing the order of steps, operations, or core logic.
  4. Decide which paper-code discrepancies are most appropriate for the given paper, choosing from the following categories. Note, you can
   create multiple discrepancies of the same or different types.
  - **Loss**: changes to loss definition or terms
  - **Algorithm**: changes in the order of steps, operations, or core logic
  - **Training**: changes to the learning process, schedule, or optimization
  - **Evaluation**: changes to evaluation logic, metrics, or scripts
  - **Model**: architectural or initialization changes
  - **Data**: dataset usage, preprocessing, augmentation, or filtering
  - **Other**: other types of discrepancies that are not covered by the above categories but appropriate for the given paper.
   5. Generate 5 discrepancies in the following strict format:
  “‘md
   # Discrepancy 1
  - Type: <choose one from: Paper Omission, Code Omission, Difference>
  - Category: <choose one from: Loss, Algorithm, Training, Evaluation, Model, Data, Other>
  - Description: <a summary of the discrepancy between the paper and the code in 3-8 sentences. When referring to the code, do not mention
  ’original’ or ’modified’, but assume the code is published with the modification and discrepancy. Your description should contain three parts
   focusing on the discrepancy: 1) summarize what is described in the paper, 2) summarize what is implemented in the modified code, and 3)
   summarize the difference. Do not speculate about the impact.>
   ## Code Changes
  «««<ORIGINAL CODE: <relative/path/to/file.py>
  (paste the relevant lines of the original code exactly as they appear)
   =======
  (paste the lines of the modified code containing your change that replace the original code)
  »»»>DISCREPANCY
   If multiple files are affected, repeat the diff block for each.
   ## Relevant Paper Sections
  - <verbatim quote any parts from the paper that are relevant to the discrepancy.>
  - <if there are multiple relevant parts, paste each of them.>
   # Discrepancy 2
   ...
   # Discrepancy 3
   ...
  “‘
   ## Paper
  {paper}
   ## Code
  {code}
F.6   Discrepancy Prediction

  PROMPT | Discrepancy Prediction

  You are an expert in analyzing scientific papers and their code implementations.
  Your task is to carefully identify concrete discrepancies between what is described in a paper and what is actually implemented in the code.
   ## What counts as a discrepancy
  - A concrete paper–code discrepancy means a mismatch between what is stated in the original paper (e.g., formulas, algorithms, logic, methods,
   processes, or other settings) and what is implemented in the original code repository.
  - Each distinct mismatch should be reported as a separate item.
   ## What does not count as a discrepancy
  - Missing information in the paper like hyperparameters (e.g., “the authors did not specify X”).
  - Hyperparameter mismatches (e.g., learning rate, batch size, dropout rate), since these are typically configurable in code repository.
  - Missing implementation in the original code repository (e.g., “the authors did not provide the code for X”).
  - Bugs or errors in the code that are unrelated to what the paper describes.
   ## Output format
   Provide your findings in the following YAML structure:
  “‘yaml
   discrepancies:
  - <a summary of the discrepancy between the paper and the code in 3-8 sentences. Your description should contain three parts focusing on the
   discrepancy: 1) summarize what is described in the paper, 2) summarize what is implemented in the code, and 3) summarize the difference.
   Do not speculate about the impact.>
  - <if there are multiple discrepancies, put each of them in a separate item.>
  “‘
   ## Paper
  {paper}
   ## Code
  {code}



F.7   Discrepancy Evaluation

  PROMPT | Discrepancy Evaluation

  Your task is to evaluate whether a reference paper - code discrepancies matches a predicted paper - code discrepancy. Follow these steps:
  1. Analyze which part of the paper or code each discrepancy is describing. Extract the core claims and issues from the reference and predicted
  discrepancies.
  2. Analyze whether the core claims are about the same issue, i.e. if they describe the same or different paper-code discrepancies. The two
  discrepancies might use different wording or one might be more detailed than the other. Focus on whether the issue is the same, even if minor
  details are different. However, if they describe different issues (even about the same topic or part of the paper or code) they do not match.
  3. Provide a brief explanation of your reasoning.
  ## Reference Paper-Code Discrepancy
  {reference discrepancy}
  ## Predicted Paper-Code Discrepancy
  {predicted discrepancy}
  ## Answer Format
  Provide your answer in the following format:
  “‘yaml
  core_claim_reference: <core claim from reference discrepancy >
  core_claim_predicted: <core claim from predicted discrepancy >
  reasoning: <explanation of why the core claims concern the same issue >
  match: <yes | no >
  “‘
