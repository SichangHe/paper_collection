                                         Vibe Coding in Software Development: A Multivocal Literature
                                         Review⋆
                                         Shahbaz Siddeeqa , Muhammad Waseema , Kai-Kristian Kemella , Mika Saaria , Jussi Raskua and
                                         Pekka Abrahamssona
                                         a Faculty of Information Technology and Communication Sciences, Tampere University, Finland



                                         ARTICLE INFO                                           ABSTRACT
                                         Keywords:                                              Vibe coding is a software development practice in which developers state intent in natural language
                                         Vibe coding                                            and large language models generate code. It is often framed as one-shot prompting, but the evidence
                                         AI-assisted software development                       describes an intent-driven, iterative workflow whose outcomes depend on how generated code is
                                         Large language models                                  evaluated and governed. Knowledge of how vibe coding is defined, practiced, and governed is
                                         Human-AI collaboration                                 scattered across academic and practitioner sources, and, to our knowledge, existing reviews have not
                                         Code generation                                        yet integrated both evidence streams. We conducted a multivocal literature review of peer-reviewed
                                         Multivocal literature review                           and grey literature following established guidelines. Searches spanned 2022 to October 2025. After
                                                                                                screening, credibility assessment, and snowballing, 47 sources were retained (28 peer-reviewed and
                                                                                                19 grey) and analyzed through descriptive mapping and thematic synthesis across eight research
                                                                                                questions. Vibe coding is consistently described as an iterative generation-evaluation-revision loop
                                                                                                rather than a one-shot activity, and developer work shifts from writing code towards specification,
                                                                                                supervision, and validation. Short-term productivity and time-to-prototype gains are reported in 21 of
arXiv:2607.21652v1 [cs.SE] 22 Jul 2026




                                                                                                47 sources (45%), while evidence on maintainability, long-term quality, and safeguard effectiveness
                                                                                                remains limited. Evidence is strongest for prototyping and user-interface work and weakest for
                                                                                                production, data-intensive, and safety-critical use, and tool visibility does not imply effectiveness.
                                                                                                This is one of the first reviews to integrate peer-reviewed and grey literature on vibe coding under
                                                                                                a single documented protocol. Future work should evaluate safeguard effectiveness, study session-
                                                                                                level dynamics and long-term maintainability, and test vibe coding in production, data-intensive, and
                                                                                                safety-critical settings.



                                         1. Introduction                                                                  guidance is given through prompts, feedback, constraints,
                                                                                                                          and validation rather than through direct editing. In this
                                             Large Language Models (LLMs) are increasingly re-                            setting the developer’s role shifts. The focus moves from
                                         shaping software development practices by changing how                           writing code toward specifying what is needed, supervising
                                         developers specify, generate, evaluate, and maintain soft-                       the model, evaluating its output, and validating the result.
                                         ware artifacts. Early coding tools worked at the level of
                                                                                                                              Vibe coding follows a short loop, shown in Figure 1. The
                                         single lines or blocks, completing code that the developer
                                                                                                                          developer states the intent in natural language. The model
                                         had already begun. Newer tools work through conversation:
                                                                                                                          generates or revises the code. The developer then evalu-
                                         the developer describes a need in natural language, and the                      ates the result by running, inspecting, testing, or otherwise
                                         model returns code, tests, or fixes [1, 2]. Some tools go                        checking the generated artifact. Using what they observe,
                                         further and act as agents that plan a task, run commands,                        such as an error message or a failed test, the developer
                                         and change several files with little human input. Software
                                                                                                                          refines the next prompt. This loop of intent, generation,
                                         development is in this way moving from code completion
                                                                                                                          evaluation, and refinement repeats until the result meets the
                                         toward conversational, intent-driven, and agentic work [3].                      goal. The outcome therefore depends not only on the model’s
                                         Vibe coding is one emerging form of this shift.                                  generation capability, but also on how systematically the
                                             In vibe coding, the developer expresses intent in natural                    developer evaluates and controls each iteration.
                                         language, and one or more LLMs generate, revise, and refine                          Vibe coding matters because it may reduce the effort
                                         the code in response [4]. Andrej Karpathy introduced the
                                                                                                                          required to create working software artifacts. A working
                                         term in early 2025 to describe this way of working, in which
                                                                                                                          version can be produced from a short description, which
                                         the developer often does not read the generated code line                        supports rapid prototyping and early validation of ideas. Be-
                                         by line [4]. The developer still guides the work, but the                        cause the interface is natural language, software creation be-
                                             ⋆
                                                 Submitted to the Journal of Systems and Software (JSS).                  comes more open to people who are not expert programmers.
                                             ∗ Corresponding author: Shahbaz Siddeeq <shahbaz.siddeeq@tuni.fi>
                                                                                                                          Early evidence from AI-assisted programming also points to
                                                  shahbaz.siddeeq@tuni.fi (S. Siddeeq); muhammad.waseem@tuni.fi           gains in productivity [5], and experienced developers can use
                                         (M. Waseem); kai-kristian.kemell@tuni.fi (K. Kemell);
                                                                                                                          the same approach to move faster on routine implementation
                                         mika.saari@tuni.fi (M. Saari); jussi.rasku@tuni.fi (J. Rasku);
                                         pekka.abrahamsson@tuni.fi (P. Abrahamsson)                                       tasks. These possible benefits help explain why vibe coding
                                               ORCID (s): 0009-0003-9030-8841 (S. Siddeeq); 0000-0001-7488-2577           has drawn attention in both practitioner communities and
                                         (M. Waseem); 0000-0002-0225-4560 (K. Kemell); 0000-0001-7677-2355 (M.            research.
                                         Saari); 0000-0002-4401-8013 (J. Rasku); 0000-0002-4360-2226 (P.
                                         Abrahamsson)


                                         S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                             Page 1 of 35
                                                   Multivocal Review of Vibe Coding

                                                                     document its search. Fawzy et al. [15] follow a documented
                                                                     process but look at grey literature only. To the best of our
                                                                     knowledge, no single review yet systematically integrates
                                                                     peer-reviewed and grey literature under a single protocol
                                                                     while jointly synthesizing definitions, workflows, developer-
                                                                     role changes, reported outcomes, risks, safeguards, tool
                                                                     ecosystems, and open research challenges.
                                                                         The aim of this study is to bring these two streams of
                                                                     evidence together. We synthesize academic and practitioner
                                                                     sources on vibe coding and give an evidence-weighted ac-
                                                                     count of how it is conceptualized, practiced, evaluated, and
                                                                     governed in software development. This evidence-weighted
                                                                     synthesis allows us to distinguish findings that are strongly
                                                                     supported from those that remain tentative, emerging, or
                                                                     weakly evidenced.
Figure 1: The vibe coding loop. The developer states the                 To do this, we conducted a multivocal literature review
intent in natural language; one or more LLMs generate the            (MLR). This kind of review extends a systematic review by
code; the developer evaluates it by running and inspecting the       including grey literature alongside peer-reviewed work. It
result; and the developer refines the next prompt based on           suits a topic where much of the activity is reported outside
what they observe. The loop repeats until the goal is met.
                                                                     academic venues [16]. We applied selection and credibility
Review of the generated code line by line is often reduced or
                                                                     criteria to both streams. We then synthesized 47 sources, 28
skipped, which sets vibe coding apart from ordinary AI-assisted
programming [4]. The full process view is shown in Figure 4a.        peer-reviewed and 19 grey, published from 2022 to October
                                                                     2025, using descriptive mapping and thematic synthesis.
                                                                     The detailed research questions, GQM mapping, extraction
                                                                     measures, search strategy, selection criteria, quality assess-
     Vibe coding also raises important software engineering
                                                                     ment, and data-extraction procedures are reported in the
risks. Because code is often accepted from how it behaves
                                                                     Methodology section. The main contributions of this study
rather than from a full reading, mistakes can pass unno-
                                                                     are as follows:
ticed. Models can return output that looks plausible but
is incorrect, incomplete, insecure, or inconsistent with the            • We provide a documented MLR protocol that inte-
intended requirements [6, 7]. Verification is often weak,                 grates peer-reviewed and grey literature on vibe cod-
which can lead to maintainability problems, security weak-                ing, making the search, selection, quality assessment,
nesses, and defects that surface later in the development                 and synthesis process transparent and reproducible.
lifecycle. Over a long session the context can drift, and
the developer may come to trust the output more than the                • We synthesize the evidence on definitions, workflows,
evidence supports. The origin of the generated code is often              developer roles, outcomes, risks, safeguards, contexts,
unclear, which raises concerns about provenance, licensing,               and tools, which brings the scattered material into one
and reproducibility. Taken together, these risks suggest that             structured account.
vibe coding is not only a new way of working but also an
important software engineering research problem.                        • We carry out an evidence-strength analysis that marks
     Evidence on vibe coding is currently spread across                   each finding as strong, moderate, weak, or emerging,
many kinds of sources. It appears in peer-reviewed studies,               which helps the reader judge how far each claim can
preprints, industry reports, blogs, vendor documentation,                 be trusted.
videos, and practitioner discussions [8, 9, 10, 11, 12]. These          • We propose a conceptual framework and a research
sources differ in depth and in methodological rigor, purpose,             agenda, which point to the areas where further empir-
and credibility. For a practitioner, this fragmentation makes             ical work is most needed.
it hard to know how to use vibe coding safely and effectively.
For a researcher, it makes it hard to see what is already                The rest of the paper is organized as follows. Section 2
known, which claims are supported by stronger evidence,              describes the MLR methodology, including the research
and what is still open. A structured synthesis is therefore          questions, search strategy, study selection, quality assess-
needed to consolidate academic and practitioner knowledge            ment, and data synthesis. Section 3 reports the results for
on vibe coding.                                                      each research question. Section 4 draws the findings together
     Existing reviews provide useful starting points, but they       and presents the conceptual framework. Section 5 discusses
remain limited in scope, evidence coverage, or methodologi-          threats to validity. Section 6 compares this review with
cal transparency. Some are narrative and do not report a doc-        earlier work. Section 7 concludes the paper and outlines
umented search or quality-assessment process, so their cov-          directions for future research.
erage is hard to check. Ge et al. [13] draw on peer-reviewed
sources only, and Ray [14] gives an overview but does not

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                      Page 2 of 35
                                                   Multivocal Review of Vibe Coding

2. Methodology                                                       2.2.1. Search strategy and query development
                                                                         Because “vibe coding” is a recent practitioner term and
    This study was conducted as a Multivocal Literature Re-
                                                                     may not appear consistently in academic indexing, we used
view (MLR), following the guidelines of Garousi et al. [16].
                                                                     an iterative query development strategy.
These guidelines build on established systematic review
principles [17] and add procedures for grey-literature search,       Stage A: Seed and scoping search We first searched
credibility assessment, and combined synthesis. Vibe coding          for the exact phrase “vibe coding” to identify seed sources
is a recent and practitioner-driven practice, so much of the         and observe how the term was used across academic and
reported evidence appears outside peer-reviewed venues,              grey venues. This search returned 31 sources and informed
in blogs, industry reports, guides, videos, and practitioner         refinement of the search vocabulary. Examining the termi-
discussions. An MLR suits this setting because it brings             nology used across these seed sources revealed recurring
grey literature together with peer-reviewed studies under one        synonyms and related concepts (including prompt-based de-
protocol, and so captures the state of practice as well as the       velopment, natural language programming, conversational
state of research. The method was designed to identify rele-         programming, and AI-assisted development), which were
vant peer-reviewed and grey sources on vibe coding, apply            incorporated into the Stage B search string. Seed sources that
transparent selection procedures, and conduct a reproducible         satisfied all inclusion criteria were also retained in the final
synthesis aligned with the research questions.                       corpus.
2.1. Goal and Research Questions                                     Search timeline. An initial seed search using the exact
    The goal of this MLR is to synthesize current evidence           phrase “vibe coding” was conducted in August 2025 to
on vibe coding, a recent software development practice               identify relevant terminology and seed sources. Following
mediated by LLMs. The review examines how vibe cod-                  feedback on the initial search vocabulary and research-
ing is defined, how it is practiced, how developer work              question framing, we iteratively refined the search string
changes during interaction with LLM systems, and what                during September 2025. The formal systematic search using
outcomes, risks, and safeguards are reported in the literature.      the final refined query (Stage B) was executed across all
We formulated eight Research Questions (RQs) as outlined             databases and grey-literature channels in October 2025. This
in Table 1. The table provides a structured view of the              timeline ensured that the corpus captured the most recent
RQs with their corresponding rationale and categorization.           literature available at the time of review, given that the term
We organized the review using the Goal–Question–Metric               “vibe coding” was coined only in early 2025 [4].
paradigm [18], as recommended for multivocal reviews by
Garousi et al. [16]. The goal is to synthesize current evidence      Stage B: Refined systematic search string After review-
on vibe coding. The questions are the eight RQs in Table 1.          ing the seed sources, we expanded the query to include
The metrics are descriptive indicators recorded for each RQ:         related terms used in academic and practitioner discourse,
the number and share of contributing sources, the source             such as AI-assisted development and natural language pro-
type, the quality and credibility scores, and an evidence-           gramming. The final search string was:
strength label. We report these qualitatively rather than as
combined statistics.                                                     Search String

Scope boundaries between related RQs: Some RQs                           ( “vibe coding” OR “prompt-based development*”
examine adjacent dimensions, so we drew their boundaries                      OR “natural language programming” OR
deliberately. RQ2 covers workflows and tactics, while RQ7                 “conversational programming” OR “AI-assisted
covers named tools. RQ4 covers product-level outcomes,
                                                                                            development*” )
while RQ5 covers process-level risks and safeguards. RQ3.3
covers differences by user and task, while RQ6 covers adop-                                       AND
tion context and constraints. Each code is tagged to exactly
                                                                          ( “software development” OR “code generation”
one RQ, so a source that contributes to several RQs does
so through different codes. This avoids double-counting and                            OR “software creation” )
keeps the per-RQ counts in Section 3 interpretable. Worked
examples of these boundaries are given in the codebook.                 This strategy follows systematic review guidance for
                                                                     emergent and inconsistently labeled concepts [17] and aligns
2.2. Review design                                                   with MLR guidance on grey literature coverage [16].
    Consistent with MLR guidance, we treated peer-
reviewed and grey literature as two evidence streams and ap-         Search terms considered but not included During scop-
plied stream-specific selection criteria and credibility checks      ing we also considered broader AI-assisted programming
[16]. Figure 2 summarizes the review process: (1) query              terms, such as “LLM-assisted programming,” “AI pair pro-
development, (2) systematic searching, (3) screening and             gramming,” “AI coding assistant,” and “agentic coding.”
selection, (4) snowballing, (5) data extraction, and (6) syn-        We did not include them in the final query, because they
thesis.                                                              retrieve a much wider literature that is not directly focused

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                       Page 3 of 35
                                                           Multivocal Review of Vibe Coding

Table 1
Research questions and their rationale
         Research Questions                                  Rationale
                                                        Concept and Practices
 RQ1     How is “vibe coding” defined and conceptualized in Vibe coding is a recent term that is not consistently defined across
         academic and industry literature?                   sources. This RQ synthesizes how the concept is described in the literature,
                                                             including interpretations such as prompt-based development, AI-assisted
                                                             programming, agentic programming, or a development practice.
 RQ2     What workflows characterize vibe coding and what This RQ examines how vibe coding is practiced. It identifies recurring
         tactics/tools are reported?                         workflow patterns, including iterative generation and testing loops, context
                                                             provisioning, error-driven prompting, and retrieval grounding, and docu-
                                                             ments associated tactics and tools.
                                                   Developer Role and Outcomes
 RQ3     How does the developer role shift?                  RQ3 examines how developer work changes during interaction with LLM
              • RQ3.1: Changes in trust, flow, agency, cog- systems. It focuses on cognitive and behavioral aspects of development,
                nitive load, and cognitive debt              including trust calibration, perceived agency, cognitive load, and session-
                                                             level interaction dynamics. Differences across user groups and task types
              • RQ3.2: Session-level dynamics such as mo- are also examined.
                mentum and context loss
             • RQ3.3: Differences by audience and task type
 RQ4     What is reported about productivity, time-to-        RQ4 synthesizes reported outcomes associated with vibe coding. Outcomes
         prototype, code/UI quality, defects, maintainability,include short-term effects such as productivity and prototyping speed, as
         and reproducibility?                                 well as longer-term considerations including defects, maintainability, and
                                                              reproducibility.
                                                   Risks, Safeguards, and Context
 RQ5     What risks and safeguards are reported for vibe- RQ5 examines reported risks and mitigation strategies. Failure modes
         coded software?                                      include incorrect code generation, context-related errors, minimal review
              • RQ5.1: Failure modes                          practices, and licensing or provenance concerns. Safeguards include review
                                                              practices, validation pipelines, sandboxing, and provenance tracking.
              • RQ5.2: Governance and guardrails
 RQ6     Where is vibe coding used, by whom, and with what RQ6 examines contexts of adoption, including prototyping versus produc-
         constraints?                                         tion settings, user groups, and constraints such as privacy, cost, and domain
                                                              sensitivity.
                                                      Tools and Open Challenges
 RQ7     What tools and platforms support vibe coding?        RQ7 analyzes the tool ecosystem associated with vibe coding, including
                                                              coding assistants, agentic development environments, and supporting
                                                              infrastructure such as evaluation tools and testing integrations.
 RQ8     What open challenges and future research directions RQ8 synthesizes open challenges reported in the literature, including
         are identified?                                      limitations in empirical evidence, evaluation practices, and representation
                                                              of user groups or task domains.



Table 2                                                                        Digital Library, Scopus, SpringerLink, and Google Scholar.
Query development.                                                             Because Google Scholar returns both peer-reviewed and
 Stage        Purpose               Query                                      non-peer-reviewed material, a Google Scholar record was
 Stage    A   Identify    initial   “vibe coding”                              kept in the peer-reviewed stream only when its venue was
 (seed and    terminology and                                                  a confirmed peer-reviewed journal, conference, workshop,
 scoping)     seed sources                                                     or symposium. Other Google Scholar records were treated
 Stage    B   Increase recall by
                                                                               as grey literature or excluded, and where a work appeared as
                                    ("vibe    coding"     OR   "prompt-based
 (refined     adding     related    development*" OR "natural language
 systematic   terms                 programming"      OR     "conversational   both a preprint and a published paper we kept the published
 query)                             programming"        OR      "AI-assisted   version. The grey-literature stream was searched separately
                                    development*")       AND      ("software
                                                                               across practitioner-oriented channels, following MLR guid-
                                    development" OR "code generation"
                                    OR "software creation")                    ance on using multiple grey channels [16]; the platforms,
                                                                               search terms, dates, and candidate counts are reported in the
                                                                               grey-literature search below (Table 7).
on vibe coding as an intent-driven, conversational practice.
We chose the final string to balance recall and precision and                  Inclusion and exclusion criteria for the peer-reviewed
to keep the corpus focused on vibe coding. The fuller recall                   literature To support consistent selection of peer-reviewed
trade-off is discussed in Section 5 (Internal validity).                       studies, we defined inclusion and exclusion criteria for the
    The search was limited to publications from 2022 on-                       peer-reviewed literature stream. For each criterion, we spec-
ward, consistent with inclusion criterion I3.                                  ified the stage of application: title and abstract screening
                                                                               (T/A), full-text screening (F), or all stages (All). The criteria
Search Sources We applied the refined search string to five                    are listed in Table 3.
databases for the peer-reviewed stream: IEEE Xplore, ACM

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                  Page 4 of 35
                                                                                                   Multivocal Review of Vibe Coding


      Phase 1                                                                                                                                                                                                                                                           Phase 3

                                          MLR Goal                                                           Query Development                                                                                                                                             Performing Data Analysis
                                                                                                                                                                                                                                                                             and Documentation
                                    Research Questions                                     Stage A: Seed Search "Vibe Coding"                                                              Peer-reviewed
                                                                                                                                                                                                                                                                                      Data Extraction       Raw Data

                                                                                           Stage B: Refined Search String
                                                      Concept and practices
                     Workflow characteristics                                                                                                                                                                                                                           Results     Data Synthesis
                                                                                                 "vibe coding'' OR "prompt-based development*'' OR
                                                     Developer role shift                        "natural language programming'' OR "conversational
                                     Outcomes                                                       programming'' OR "AI-assisted development*''
                                                     Risks and safeguards                                                      AND                                                                                                                                                Data Interpretation
                               Adoption context                                                   "software development'' OR "code generation'' OR
                                                                                                                                                                                                     Grey
                                                                                                                                                                                                                                                                                                            Validity
                                                     Ecosystem                                                    "software creation''                                                                                                                                   Research
                                    Challenges                                                                                                                                                                                                                                                              Threats
                                                                                                                                                                                                                                                                        Demography       Answer to the
                                                                                                                                                                                                                                                                                       Research Questions




                                                                                                                    Forward




                                                                                                                                         Peer-reviewed Literature
                                                                                                                                                                                                    Full Reading
       Conducting Multivocal




                                                                                 White Screening                                                                                                                                                                         Relevance & Credibility Screening
                                                                                                                                                                             Screening Title & Abstract




                                                                                                                                                                                                                                                      Grey Literature
         Literature Search




                                                                                                                                                                                                                                 Quality Assessment
                                                                              Title   Abstract   Full Text                                                                    Initially Extracted                                                                                  Initially Extracted




                                                                                                                                                                                                                   Snowballing




                                                                                                                                                                                                                                                                                                                 Snowballing
                                                                                                                                                                    IEEE Xplore            148         21    11                                                         Web Search                14        09
                               Primary Search                                                            Snowballing                                                ACM Digital Library      81        14    08                                                         Google Scholar            07        04
                                                                                                                                                                    Scopus                 191         25    06                                                         Youtube                   01        01
                                                  Extraction of
                                                                                                                                                                    Google Scholar         102         24    01                                                         LinkedIn                  01        01
                                                                                                                    Backward

                                                    studies                      Grey Screening
                                                                                                                                                                    Springer Link            18        06    01                                                         X (Twitter)               01        01
                                                                              Relevance and Credibility

                                                                                                                                                                     28 Studies            540         90    27 02 -1                                                     19 Studies              24        16       03


      Phase 2



                                                                                      Figure 2: Overview of the MLR review process.



Table 3                                                                                                                                           Table 4
Inclusion and exclusion criteria for the peer-reviewed literature.                                                                                Grey literature eligibility criteria.
 ID                 Criterion                                                                                 Stage                                           ID              Criterion                 Rule
                                         Inclusion criteria                                                                                                   GL-I1           Topical relevance         Must address vibe coding or AI-assisted
 I1                 Studies focus on vibe coding, intent-driven program-                                      All                                                                                       software development, including work-
                    ming, or AI-assisted development in the context of                                                                                                                                  flows, tools, or practices relevant to the
                    software development.                                                                                                                                                               RQs.
 I2                 Studies evaluate or review tools or platforms for AI-                                     T/A                                             GL-I2           Substantive technical Must include concrete discussion of work-
                    driven software creation.                                                                                                                                 content                   flows, tools, risks, mitigations, or imple-
 I3                 Studies are published in 2022 or later.                                                   T/A                                                                                       mentation detail rather than high-level
                                                                                                                                                                                                        opinion.
 I4                 Studies are published in peer-reviewed journals or con-                                   T/A
                    ferences relevant to software engineering.                                                                                                GL-I3           Credibility threshold     Must score above the minimum quality
                                                                                                                                                                                                        threshold on the Garousi et al. [16] 15-
 I5                 Studies provide evidence-based contributions relevant                                     T/A
                                                                                                                                                                                                        item credibility checklist (score >4 out of
                    to vibe coding, including empirical evaluations, design
                                                                                                                                                                                                        15; see Table 9).
                    proposals, theoretical arguments, or position state-
                                                                                                                                                                                                   Exclusion criteria
                    ments directly addressing vibe coding practices or
                    outcomes.                                                                                                                                 GL-E1           Opinion-only or low Exclude sources dominated by commen-
                                                                                                                                                                              substance                 tary without substantive technical or
 I6                 Studies discuss developer experience or human–AI col-                                     T/A
                                                                                                                                                                                                        methodological detail.
                    laboration in coding.
                                                                                                                                                              GL-E2           Duplicate or replicative Exclude near-duplicate sources or sources
                                         Exclusion criteria
                                                                                                                                                                              content                   that primarily restate previously included
 E1                 Not written in English.                                                                   T/A                                                                                       material.
 E2                 Duplicate study or extension of an already included                                       T/A
                    work.
 E3                 Irrelevant to AI or software development.                                                 All
 E4                 Non-peer-reviewed source.                                                                 F                                   primarily opinion-based with limited technical content or
 E5                 Not accessible via institutional access or public reposi-
                    tories.
                                                                                                              T/A                                 when they substantially duplicated already included mate-
 E6                 Focuses on AI applications outside software develop-                                      F                                   rial. The eligibility criteria are shown in Table 4.
                    ment.
 E7                 Published before 2022.                                                                    F                                   2.2.2. Search and selection process for the
                                                                                                                                                         peer-reviewed literature
                                                                                                                                                      The peer-reviewed literature search was conducted in
Grey literature eligibility (credibility and relevance)
                                                                                                                                                  October 2025 and covered publications from 2022 onward.
Grey sources were included when they (i) addressed vibe
                                                                                                                                                  Applying the refined search string to the selected sources
coding or AI-assisted programming practices relevant to the
                                                                                                                                                  returned 540 records, as shown in Figure 3.
RQs and (ii) provided sufficient technical substance and
source credibility. Sources were excluded when they were


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                                                                                                                                                                   Page 5 of 35
                                                   Multivocal Review of Vibe Coding

    • Title and abstract screening: We screened titles using         Table 5
      the criteria in Table 3, reducing the set from 540 to 246      Quality assessment checklist for peer-reviewed papers, adapted
      records. We then screened abstracts of the remaining           from Dybå and Dingsøyr [20] and organized into the four
      records and retained 90 papers as candidates for dedu-         CASP-derived evaluation stages used in that checklist. Scoring:
      plication and full-text assessment.                            Yes = 1, Partly = 0.5, No = 0; inapplicable items are recorded
                                                                     as N/A and removed from that paper’s denominator.
    • Deduplication: Following title and abstract screen-             Stage         QA𝑠    Quality assessment question
      ing, records retained from all five databases were                            QA1    Is the paper based on research (not merely a “lessons
      merged into a combined candidate list. Cross-database           Reporting            learned” or expert-opinion report)?
                                                                                    QA2    Is there a clear statement of the aims of the research?
      duplicate records (papers indexed in more than one                            QA3    Is there an adequate description of the context in which
      database) were identified by comparing titles, au-                                   the research was carried out?

      thors, and publication venues, consistent with the                            QA4    Was the research design appropriate to address the aims
                                                                                           of the research?
      PRISMA 2020 deduplication step recommended be-                  Rigor         QA5    Was the recruitment or sampling strategy appropriate
      fore full-text assessment. Sixteen such duplicate                                    to the aims of the research?
                                                                                    QA6    Was there a control group or comparison baseline with
      records were removed (primarily papers co-indexed                                    which to compare the approach (where appropriate)?
      by Scopus and IEEE Xplore, or by ACM Digital                                  QA7    Was the data collected in a way that addressed the
                                                                                           research issue?
      Library and Scopus), leaving 74 unique papers for                             QA8    Was the data analysis sufficiently rigorous?
      full-text reading.                                              Credibility   QA9    Has the relationship between researcher and partici-
                                                                                           pants been considered adequately?
    • Full-text assessment: We read the full text of the 74           Relevance
                                                                                    QA10   Is there a clear statement of findings?
                                                                                    QA11   Is the study of value for research or practice?
      deduplicated papers and applied the same criteria.
      This step yielded 27 potentially relevant papers.
                                                                     Table 6
    • Snowballing: We performed backward and forward                 Quality bands for the 28 included peer-reviewed papers, from
      snowballing [19] on the reference lists and citing             the 11-item Dybå and Dingsøyr checklist: High (≥0.75, 𝑛 =
      works of the 27 unique peer-reviewed studies. This             18), Medium (0.60–0.74, 𝑛 = 7), Low (0.50–0.59, 𝑛 = 3).
      process yielded 47 candidate references for inspec-            Item-level scores are provided in the supplementary material.
      tion. Of these, 31 were duplicates of studies already           ID       Short title                                             Quality
      captured by the primary search, 9 addressed AI-                 WL1      IDE Augmented with NL Programming                       High
                                                                      WL2      FormalEval: LLM Code Generation Evaluation              High
      assisted software development broadly but did not               WL3      Review on LLM-Based Code Generation                     Low
      meet our vibe-coding-specific inclusion criteria (I1,           WL4      Survey: Usability of AI Programming Assistants          High
      I6), 3 were published before 2022 (excluded by I3/E7),          WL5      Trust Dynamics in AI-Assisted Development               High
                                                                      WL6      Industrial Experience on AI-Assisted Coding             Medium
      and 2 failed the accessibility criterion (E5). The re-          WL7      Evaluating Advantage of AI-Native IDE Cursor            Medium
      maining 2 candidates satisfied all criteria and were            WL8      Developer–AI Interaction Taxonomy                       Medium
      added to the corpus, resulting in 29 papers before              WL9      Transformative Influence of LLMs on SW Dev              Low
                                                                      WL10     Security of GitHub Copilot-Generated Code               High
      quality assessment. The low yield is expected, because          WL11     CoPrompt: Collaborative NL Programming                  High
      vibe coding is a new term and its citation network is           WL12     In-IDE Code Generation from Natural Language            High
      still immature.                                                 WL13     The Programmer’s Assistant (Conversational)             High
                                                                      WL14     Games Programming Pedagogy                              Medium
    • Quality assessment: The first author assessed the 29            WL15     Position: Vibe Coding Needs Vibe Reasoning              High
                                                                      WL16     AI Assistants in SW Dev: Qualitative Study              High
      retained peer-reviewed papers with the eleven-item              WL17     MultiMind: AI Development Plugin                        Medium
      checklist of Dybå and Dingsøyr [20] (Table 5), which            WL18     Facilitating Trust in AI-Assisted SW Tools              High
      is widely used in software engineering reviews [17,             WL19     GenAI Coding for Visually Impaired Developers           High
                                                                      WL20     Vibe Coding for Biomedical SW Development               High
      16]. Each item was scored Yes = 1, Partly = 0.5, or             WL21     Automatic Programming: LLMs and Beyond                  High
      No = 0. An item was marked Not Applicable only                  WL22     AI-Based Coding Assistants in Practice                  High
      when it could not apply to the study type, for example          WL23     Online Communities and AI Tool Trust                    High
      participant recruitment in a non-empirical paper. N/A           WL24
                                                                      WL25
                                                                               LLM Agent for Efficient Low-Code Development
                                                                               GenAI Vibe Coding for Industrial Prototyping
                                                                                                                                       Medium
                                                                                                                                       Medium
      items were removed from that paper’s denominator,               WL26     NLOP: Natural Language-Oriented Programming             High
      and the score is reported as the proportion of appli-           WL27     Vibe Coding as Intent Mediation in SW Dev               High
      cable items. Papers scoring below 0.5 were excluded             WL28     Democratizing SE through GenAI and Vibe Coding          Low

      from data extraction. Of the 29 papers, 28 met this
      threshold and were included. These 28 papers were
                                                                     Corpus size in context. The final corpus of 47 primary
      then grouped into three quality bands: High (propor-
                                                                     studies (28 peer-reviewed and 19 grey) is smaller than recent
      tion ≥0.75), Medium (0.60–0.74), and Low (0.50–
                                                                     narrative reviews of vibe coding. This follows from applying
      0.59). The bands are used only for evidence weighting
                                                                     explicit inclusion and exclusion criteria, duplicate removal,
      during synthesis; inclusion is governed solely by the
                                                                     and quality and credibility assessment to a broad initial
      0.50 threshold. The band and score for each included
                                                                     retrieval. A detailed comparison with prior reviews is given
      paper are given in Table 6, and all item-level scores
                                                                     in Section 6.
      are provided in the supplementary material.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                   Page 6 of 35
                                                            Multivocal Review of Vibe Coding




Figure 3: Database-level reduction of the peer-reviewed corpus across screening stages. The record count falls from the 540 initial
records through title and abstract screening, deduplication, and full-text assessment. This figure complements the overall review
process in Figure 2, which shows the review stages rather than the per-stage record counts.



Table 7                                                                             technical content, opinion-dominant framing, or du-
Grey-literature search by platform.                                                 plication.
Platform               Search terms                    Date       Candidates
Google Web Search      vibe coding; AI-assisted pro-   Oct 2025   14
                                                                                 • Snowballing: We applied backward and forward
                       gramming; LLM-based devel-                                  snowballing where applicable, tracing hyperlinks,
                       opment; natural language pro-
                       gramming                                                    named references, and cited resources within the 16
Google Scholar         vibe coding; AI-assisted pro-   Oct 2025   07               retained grey sources. This produced 12 candidate
                       gramming; LLM-based devel-
                       opment; natural language pro-
                                                                                   sources for inspection. Of these, 5 were duplicates
                       gramming                                                    or near-duplicates of already-included material and
YouTube                vibe coding; AI-assisted pro-
                       gramming
                                                       Oct 2025   01
                                                                                   2 lacked substantive technical content (excluded by
LinkedIn               vibe coding                     Oct 2025   01               GL-E1), leaving 5 candidates for quality assessment.
X (formerly Twitter)   vibe coding                     Oct 2025   01               These 5, together with the 16 primary sources, were
                                                          Total   24
                                                                                   scored against the Garousi et al. [16] 15-item QA
                                                                                   checklist. Of the 5 snowballing candidates, 2 scored
    Figure 3 summarizes the peer-reviewed search and se-                           ≤4 out of 15, failing the minimum credibility thresh-
lection process.                                                                   old (GL-I3), and were excluded. The remaining 3
                                                                                   satisfied all eligibility and quality criteria and were
2.2.3. Search and Selection Process for the Grey                                   added, yielding a final grey corpus of 19 sources.
        Literature
                                                                                 • Credibility assessment: All retained grey sources were
    The grey literature search was conducted in October
                                                                                   evaluated using the 15-item quality assessment check-
2025 using Google Scholar, Google web search, YouTube,
                                                                                   list for grey literature proposed by Garousi et al. [16],
LinkedIn, and X (formerly Twitter). These channels were
                                                                                   reproduced verbatim in Table 9. The checklist covers
selected to capture practitioner-oriented content across for-
                                                                                   seven criteria: authority of the producer, methodol-
mats including technical blog posts, industry guides, video
                                                                                   ogy, objectivity, date, position with respect to re-
tutorials, and professional commentary. The primary search
                                                                                   lated sources, novelty, and outlet type, operational-
terms used were “vibe coding”, “AI-assisted programming”,
                                                                                   ized through fifteen sub-questions each scored on an
“LLM-based development”, and “natural language program-
                                                                                   ordinal scale (0, 0.5, or 1). Sub-question scores are
ming”. Searches were stopped when three consecutive result
                                                                                   summed to a total credibility score in the range 0–
pages across all active channels yielded no new topically rel-
                                                                                   15. Each grey source was coded by the first author
evant sources, following the saturation-based stopping rule
                                                                                   against this checklist. Consistent with MLR guidance
recommended by Garousi et al. [16]. The search returned 24
                                                                                   to include only sources with sufficient credibility to
candidate grey sources in total. The platforms, search terms,
                                                                                   contribute meaningfully to the synthesis [16], sources
dates, and per-platform candidate counts are summarized in
                                                                                   scoring ≤4 out of 15 were excluded from data extrac-
Table 7.
                                                                                   tion (criterion GL-I3). All 19 retained sources scored
    • Relevance screening: We screened candidate sources                           above this threshold. For evidence-weighting pur-
      for topical relevance, credibility, and technical sub-                       poses during synthesis, retained sources were grouped
      stance using the criteria in Table 4. This retained                          into three credibility bands based on their aggregate
      16 sources; eight were excluded because of limited                           score (Table 10): GL Tier 1 (high credibility, ≥12),

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                              Page 7 of 35
                                                           Multivocal Review of Vibe Coding

Table 8                                                                          Coding followed a hybrid scheme [21]. An initial set of
Credibility scores and tiers for the 19 included grey sources,               codes was derived deductively from the eight research ques-
from the 15-item Garousi et al. [16] checklist (range 0–15).                 tions. Further codes were added inductively while reading
Tiers: GL Tier 1 (≥12, 𝑛 = 1), GL Tier 2 (9 ≤ 𝑠 < 12, 𝑛 = 12),               the sources. Each code was linked to exactly one research
GL Tier 3 (5 ≤ 𝑠 < 9, 𝑛 = 6). Item-level scores are provided in              question, so that a source contributing to several questions
the supplementary material.                                                  does so through different codes and is not counted twice. The
ID       Short description                         Score     GL Tier         final codebook contains 56 codes. The complete extraction
GL1      Review: Vibe Coding Fundamentals
         (Ray)
                                                   11.5      GL Tier 2
                                                                             data for all 47 sources (24 data fields per source) and the
GL2      Gotchas of AI and Vibe Coding (Maes)      9.5       GL Tier 2       full codebook (code definitions, keywords, and include and
GL3      What is Vibe Coding and When to Use
         It? (Horvat)
                                                   11.5      GL Tier 2       exclude rules) are provided in the supplementary material.
GL4      Karpathy’s Original Vibe Coding Post      6.0       GL Tier 3
GL5      State of Vibe Coding Tools (Gaspar,       7.5       GL Tier 3       2.3. Data synthesis
GL6
         LinkedIn)
         Vibe Coding Fundamentals in 33 Min-       8.0       GL Tier 3
                                                                                We applied a two-stage synthesis approach consisting of
         utes (YouTube)                                                      descriptive mapping followed by thematic synthesis.
GL7      Programming through Conversation          12.0      GL Tier 1
         with AI (Sarkar)
GL8      Vibe Coding vs. Agentic Coding (Sap-      11.5      GL Tier 2
                                                                             Descriptive mapping We first performed descriptive
         kota et al.)                                                        mapping of the included corpus to characterize the evi-
GL9      Twilight of SW Engineering in Vibe Cod-
         ing Age
                                                   8.5       GL Tier 3
                                                                             dence base. Studies were summarized by publication year,
GL10     Vibe Coding in Practice (Fawzy et al.)    11.5      GL Tier 2       venue or source type, publication category (peer-reviewed
GL11     Vibe Coding Explained: Tools and          11.0      GL Tier 2       vs. grey literature), and research question (RQ) coverage.
         Guides (Google Cloud)
GL12     Vibe Coding and AI-Led Conversational     11.5      GL Tier 2       These summaries provide an overview of the distribution of
         Programming                                                         studies across topics and evidence streams and establish the
GL13     Will the Future of SW Dev Run on
         Vibes? (Ars Technica)
                                                   11.5      GL Tier 2
                                                                             evidence context for the subsequent thematic synthesis.
GL14     Student–AI Interactions in Vibe Coding    11.5      GL Tier 2
         (Geng et al.)                                                       Thematic synthesis We then conducted a thematic syn-
GL15     Technical Debt-Aware Prompting for        8.0       GL Tier 3
         Vibe Coding                                                         thesis aligned with the research questions (RQ1–RQ8). The
GL16     Academic Vibe Coding: Research Oppor-     10.5      GL Tier 2       synthesis proceeded in steps. We read each source and
GL17
         tunities
         Intent-Driven Code Synthesis: Redefin-    11.0      GL Tier 2
                                                                             extracted the text relevant to each RQ, together with a
         ing SW Dev                                                          supporting excerpt. We applied the codes to these extracts
GL18     What is Vibe Coding? (IBM)                7.0       GL Tier 3       and grouped the codes under their RQs. For each RQ we
GL19     Silicon Valley’s Next Act: Vibe Coding    11.5      GL Tier 2
                                                                             compared peer-reviewed and grey evidence. We then con-
                                                                             solidated related codes into higher-level themes. Each theme
       GL Tier 2 (moderate credibility, 9 ≤ 𝑠 < 12), and GL                  was linked back to the contributing source identifiers and
       Tier 3 (low credibility, 5 ≤ 𝑠 < 9). Of the 19 included               representative excerpts, so that every finding reported in the
       grey sources, one (GL7, Sarkar, arXiv/PPIG 2025)                      Results section is traceable to its sources.
       reached GL Tier 1, 12 were classified as GL Tier 2,
       and 6 as GL Tier 3. Findings resting substantively on                 Evidence strength For each finding we recorded an
       Tier 2 or Tier 3 sources were interpreted cautiously                  evidence-strength label, so that readers can see how well
       and, where peer-reviewed evidence reported the same                   a claim is supported. The label combines three factors: the
       phenomenon, reported alongside the corresponding                      number of contributing sources, their quality and credibility
       peer-reviewed citations so the reader can assess con-                 (the peer-reviewed quality band in Table 6 and the grey-
       vergence between evidence streams (see Section 3).                    literature credibility tier in Table 10), and the consistency
       The credibility band and total checklist score for each               of the finding across the two evidence streams. We used
       of the 19 grey sources is shown in Table 8; full item-                four levels. A finding is strong when many sources support
       level scores for all 15 sub-questions are provided in                 it, including several high-quality (High-band) peer-reviewed
       the supplementary material.                                           studies, and it is consistent across the peer-reviewed and grey
                                                                             streams. It is moderate when it rests on a substantial mix
                                                                             of peer-reviewed and higher-tier grey sources (GL Tier 1
2.2.4. Data extraction                                                       or Tier 2), with only minor inconsistency across streams. It
    Following the search and selection process, 47 primary                   is weak when it rests on few sources, or mainly on lower-
studies were included for data extraction (28 peer-reviewed                  tier grey literature (GL Tier 3), or the sources disagree. It is
and 19 grey). The first author extracted the data using a struc-             emerging when it rests on very few sources or a single early
tured form aligned with the research questions (Table 11).                   signal, most often from grey literature, indicating an under-
Each field records a short analytical summary and, where                     studied phenomenon. The first author assigned the labels.
possible, a supporting excerpt or section reference, so that
each extracted item is traceable to its source. Missing or un-               Researcher roles The first author performed the main
clear information was marked as Not reported or Unknown                      methodological steps: title and abstract screening, full-
rather than inferred.                                                        text screening, quality assessment, credibility assessment,

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                               Page 8 of 35
                                                   Multivocal Review of Vibe Coding

Table 9
Quality assessment criteria for grey literature, adopted verbatim from Garousi et al. [16]. Each source is scored on fifteen
sub-questions (0–1 per sub-question); sub-scores are summed to a credibility total in 0–15 and mapped to tiers in Table 10.
   Criterion                   Question                                               Score description
                                                                                      1: Reputable and well-known organization
                               Is the publishing organization reputable?              0.5: Existing but not well-known organization
                                                                                      0: Unknown or low-reputation organization
                               Is an individual author associated with a reputable    1: Yes
                               organization?                                          0: No
   Authority of the producer
                                                                                      1: More than three works
                               Has the author published other work in the field?      0.5: 1–2 works
                                                                                      0: No other works
                                                                                      1: Relevant professional role
                               Does the author have expertise in the area?
                                                                                      0: Not relevant
                                                                                      1: Yes
                               Does the source have a clearly stated aim?
                                                                                      0: No
                                                                                      1: Reputable sources
   Methodology                 Is the source supported by authoritative references?   0.5: Non-highly reputable sources
                                                                                      0: No references
                                                                                      1: Yes
                               Does the work cover a specific question?               0.5: Not explicit
                                                                                      0: No
                                                                                      1: Yes
                               Does the work seem to be balanced in
                                                                                      0.5: Partially
                               presentation?
                                                                                      0: No
                                                                                      1: Objective
                               Is the statement objective or subjective?              0.5: Partially objective
                                                                                      0: Subjective
   Objectivity
                                                                                      1: No vested interest
                               Are the conclusions free of bias?                      0.5: Partial interest
                                                                                      0: Strong interest
                                                                                      1: Yes
                               Are the conclusions supported by the data?             0.5: Partially
                                                                                      0: No
                                                                                      1: Yes
   Date                        Does the item have a clearly stated date?
                                                                                      0: No
   Position w.r.t. related                                                            1: Yes
                               Have related sources been discussed?
   sources                                                                            0: No
                                                                                      1: Yes
   Novelty                     Does it add something unique?                          0.5: Partially
                                                                                      0: No
                                                                                      1: High credibility (books, reports, white papers)
   Outlet type                 Outlet control                                         0.5: Moderate credibility (news, videos, Stack Over-
                                                                                      flow)
                                                                                      0: Low credibility (blogs, tweets, emails)



data extraction, coding, and thematic synthesis. Senior re-                checklists in Tables 5 and 9, and a fixed codebook in which
searchers then reviewed a sample of the screening and se-                  each code is linked to one research question. Every extracted
lection decisions, the quality and credibility scores, and the             item and every reported finding is linked to a source identi-
coding outputs and final themes, and disagreements were                    fier and a supporting excerpt, so a reader can trace a finding
resolved through discussion. To further reduce subjectivity,               back to its sources. The supporting artifacts, including the
we used documented inclusion and exclusion criteria, a fixed               data-extraction matrix, the codebook, and the item-level
codebook in which each code is linked to one RQ, and a                     quality and credibility scores, are released as supplementary
traceability record that links every extracted item and every              material; their contents and the deposit location are given in
finding to a source identifier and a supporting excerpt.                   the Data availability statement.

2.4. Reproducibility
    The review was designed so that others can follow
and check each step. We used a written protocol based on
Garousi et al. [16], with documented inclusion and exclusion
criteria for both evidence streams, the quality and credibility


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                               Page 9 of 35
                                                                Multivocal Review of Vibe Coding

Table 10                                                                                   By study type (Table 13), method proposals are the most
Credibility band classification for grey literature sources, based                    frequent category (15; 31%). Exploratory studies account for
on the aggregate Garousi et al. [16] 15-item QA checklist score                       10 sources (21%) and proof-of-concept contributions for 9
(range 0–15; see Table 9). The three bands are used solely for                        (18%). Experiments are present in 7 sources (15%). Tool
evidence weighting during synthesis. Sources scoring ≤4 fail                          reviews appear in 6 sources (12%) and are concentrated in
the minimum credibility threshold (GL-I3) and are excluded                            the grey literature. Case studies (4; 8%) and surveys (5; 10%)
before band assignment; no source in this corpus reached that                         are the least frequent types. Since sources may be coded
threshold.
                                                                                      under more than one study type, the counts in Table 13 sum
 Tier        Score           Interpretation      Use in synthesis
 GL Tier 1   ≥ 12 (≥ 80%)    High credibility    May support major themes; still
                                                                                      to 56 rather than 47.
                             grey                labeled as grey evidence.                 By study category (Table 14), full papers account for
 GL Tier 2 9 ≤ 𝑠 < 12
             (60–79%)
                             Moderate credi-
                             bility grey
                                                 Supports themes with caution;
                                                 triangulate with peer-reviewed
                                                                                      the largest share (29; 62%). Blog posts represent 5 sources
                                                 literature where possible.           (11%). The remaining sources are distributed across position
 GL Tier 3 5 ≤ 𝑠 < 9 Low credibility Include only if uniquely relevant;
             (33–59%)        grey                do not use for strong conclusions.
                                                                                      papers (4; 9%), short papers (2; 4%), industry reports (2;
 Exclusion floor (not a substantive tier): sources scoring ≤4 (<27%) were             4%), guides (2; 4%), vision papers (2; 4%), and one YouTube
 excluded from data extraction before tier assignment, consistent with                video (1; 2%).
 MLR credibility guidance [16]. No source in this corpus reached this
 threshold.                                                                                Taken together, these distributions suggest that vibe cod-
                                                                                      ing is still an emerging and unevenly studied topic. The cor-
                                                                                      pus is recent and concentrated around 2025 (Figure 5), and a
3. Results                                                                            large share is grey literature (40%), which indicates that prac-
                                                                                      titioner discussion currently runs ahead of peer-reviewed
    This section reports the results obtained to address our
                                                                                      research. Method proposals, exploratory studies, and proof-
RQs. From here onward, we distinguish results from peer-
                                                                                      of-concept work outweigh controlled experiments, surveys,
reviewed literature (denoted WL) and grey literature (GL)
                                                                                      and case studies, which points to an early, proposal-driven
using both visual cues and textual means.
                                                                                      stage in which ideas are put forward faster than they are
    Denominator conventions. Not every source in the cor-
                                                                                      tested empirically. Coverage across research questions is
pus contributed codeable data to every research question. For
                                                                                      also uneven (Table 15): workflows (RQ2) and tools (RQ7)
each RQ subsection, we report the number of sources that
                                                                                      are comparatively well covered, whereas session-level dy-
provided relevant data. Percentages within an RQ section
                                                                                      namics (RQ3.2) and usage contexts (RQ6) rest on fewer than
are calculated relative to that RQ’s contributing source count
                                                                                      ten sources each. These patterns are best read as a maturity
as denominator, except for RQ3.3, RQ4, RQ5.1, and RQ8,
                                                                                      signal: the evidence base is broad in some areas but thin and
where findings represent the prevalence of an audience or
                                                                                      preliminary in others, so the findings in this review are better
task profile, outcome, risk, or challenge across the full cor-
                                                                                      treated as early indications than as settled results.
pus of 47 sources and the denominator is therefore 47. Each
                                                                                           Figure 5 shows how the sources are distributed by pub-
results table carries a footnote or caption note specifying the
                                                                                      lication year, type, and category. Almost all sources fall in
exact denominator used. The percentage denominators by
                                                                                      2025, which confirms that the topic is very recent and that
RQ are: RQ1 = 36, RQ2 = 43, RQ3.1 = 34, RQ5.2 = 33; and
                                                                                      the current evidence base has formed within a short window.
the full corpus of 47 for RQ3.3, RQ4, RQ5.1, and RQ8. For
the two smallest research questions, RQ3.2 (9 contributing
                                                                                      3.2. Vibe Coding Definition (RQ1)
sources) and RQ6 (8 contributing sources), we report counts
                                                                                           Table 16 presents representative definitions and descrip-
rather than percentages, since percentages are unstable at
                                                                                      tions of vibe coding as stated in the primary sources, ordered
such low source counts.
                                                                                      chronologically from the original coinage by Karpathy to
    Evidence strength. Because frequency alone does not
                                                                                      subsequent academic and practitioner framings. The def-
capture how well supported a finding is, we also assign
                                                                                      initions range from informal practitioner characterizations
each research question a qualitative evidence-strength rating,
                                                                                      to structured academic formulations, but several recurring
reported in the RQ summary boxes. The rating uses the four
                                                                                      elements are visible across them: (i) the use of natural lan-
levels (strong, moderate, weak, and emerging) defined in
                                                                                      guage as the primary development interface, (ii) an iterative
Section 2 under “Evidence strength”, which combine the
                                                                                      conversational interaction loop between developer and AI,
number of contributing sources, their quality and credibility,
                                                                                      (iii) reduced emphasis on line-by-line code authoring or
and their consistency across the two evidence streams.
                                                                                      comprehension, and (iv) the delegation of code implementa-
3.1. Study Context                                                                    tion to a generative model under varying degrees of human
                                                                                      oversight.
    We provide an overview of the study contexts in the
                                                                                           A total of 36 out of 47 sources contributed to RQ1
reviewed research, including the types of studies conducted,
                                                                                      (17 peer-reviewed and 19 grey). All percentages in this
the balance between peer-reviewed and grey literature, and
                                                                                      subsection are relative to these 36 contributing sources.
the categories of published works.
                                                                                           Table 17 organizes the conceptualizations of vibe coding
    The corpus consists of 28 peer-reviewed studies
                                                                                      reported across the literature into five categories. The two
(59.57%) and 19 grey-literature sources (40.43%), as re-
ported in Table 12.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                       Page 10 of 35
                                                                                                                                 Multivocal Review of Vibe Coding

Table 11
Data extraction form: data items, descriptions, and linked research question. This is a grouped view; the full matrix of 24 data
fields per source is provided in the supplementary material.
 Data item                                                                             Description                                                                                                                                                                                     Linked RQ
 Study metadata                                                                        Title, authors, year, venue or outlet, source type (peer-reviewed or Demographic
                                                                                       grey), and publication type
 Study method                                                                          Research method or type of contribution                                                                                                                                                         Demographic
 Conceptualization                                                                     How the source defines and frames vibe coding                                                                                                                                                   RQ1
 Workflow and tactics                                                                  Interaction patterns, task distribution, and automation boundaries                                                                                                                              RQ2
 Developer role                                                                        Trust, flow, agency, cognitive load, and cognitive debt                                                                                                                                         RQ3.1
 Session dynamics                                                                      Momentum, context loss, and disengagement during a session                                                                                                                                      RQ3.2
 Audience and task                                                                     Differences by user group and task type                                                                                                                                                         RQ3.3
 Outcomes                                                                              Productivity, prototyping speed, code and UI quality, defects, main- RQ4
                                                                                       tainability, and reproducibility
 Failure modes                                                                         Ways in which the human–AI process breaks down                                                                                                                                                  RQ5.1
 Safeguards                                                                            Governance and guardrails                                                                                                                                                                       RQ5.2
 Adoption context                                                                      Where, by whom, and under what constraints vibe coding is used                                                                                                                                  RQ6
 Tools and platforms                                                                   Named tools and supporting infrastructure                                                                                                                                                       RQ7
 Open challenges                                                                       Reported open challenges and future directions                                                                                                                                                  RQ8



                                                                                                                                                                                                  Structural View: Vibe Coding in Software Development
                                                                                                                                                                                    Moderators (RQ6 - RQ7)


                                        Process View: Vibe Coding Workflow Loop                                                                                                      Context/users (RQ6): novice vs expert; student vs pro; prototype
                                                                                                                                                                                     vs production; UI vs data/ML; privacy/cost constraints
                                                                                                                                                                                                                                                        Tools/platforms (RQ7): Copilot-style completion; chat assistants;
                                                                                                                                                                                                                                                        feedback mechanisms
                                                                                                                                  Outcomes: productivity,
                                                       Risks: hallucinations,                                                      quality/maintainability
                                                           context drift                                                          uncertain (conditional)
                                                                                                                                                                                    Workflow Layer (RQ2)                 Role & Experience Layer         Outcome Layer (RQ4)                   Risk & Governance Layer
                                                                                                                                                                                                                         (RQ3)                                                                 (RQ5)
                                                                                                                                                                                     W1 Chat loop / multi-turn                                            O1 Productivity / time-to-
                                                                                                                                                                                                                          R1 Trust calibration                                                  G1 Failure modes:
                                                                                                                                                                                     prompting                                                            time prototype
                                                                                                                                                                                                                                                                                                hallucinations, brittle
                                                                                                                                                                                                                                                                                                prompts, context errors,
                Intent &                       LLM/Agent                        Execution &                   Human                                                                  W2 Prompt-patch iteration            R2 Agency shift:                O2 Code/UI quality &
                                                                                                                                                    Outputs                                                                                                                                     licensing/provenance gaps
                Context                        Generation                        Feedback                   Supervision                                                              (error-paste-back)                   author supervisor               defects

                                                                                                                                                                                     W3 Context provisioning              R3 Cognitive load
                                                                                                                                                                                     (requirements, constraints,          (verification + context         O3 Maintainability                    G2 Guardrails: HITL
        User
        User     Constraint Artifacts                                       Tests       Runtime
       Prompt
                                                Code/UI Change
                                                                                                          Review     Trust     Decision          Prototype/   Risk State             artifacts)                           repair)                                                               review, sandboxes,
                                                                                UI Preview        Logs             Calibration                    Product                                                                                                                                       validation/QA pipelines,
                                                                                                                                                                                                                                                                                                provenance tracking,
     Defining the 'what' & 'why'           AI translates intent into     Immediate validation in a       The 'vibe' check: does             Deployable software and
                                                                                                                                                                                     W4 Retrieval grounding               R4 Cognitive debt                                                     disclosure & avoid-when
      in the natural language.                 functional code.             live environment.                 it feel right?                     known issues.                                                                                            O4 Reproducibility
                                                                                                                                                                                     (docs/RAG)                           (deferred understanding)                                              rules

                                                                                                                                Safeguards: tests/QA,
                                                                                                                               HITL review, sandboxing,                              W5 Evaluation pipeline               R5 Session momentum &
                                                          Iterative Refinement Loop                                              provenance tracking                                 (tests, lint, runtime checks)        context drift
                                                  Refine prompts, constraints, or context




(a) Process view: the iterative intent–generation–evaluation–refinement                                                                                                       (b) Structural view: a multi-layered conceptual model mapping
loop that characterizes a single vibe coding session.                                                                                                                         the dimensions of vibe coding to the review’s research questions.
                                                                                                                                                                              Four layers (workflow, RQ2; role and experience, RQ3; outcomes,
                                                                                                                                                                              RQ4; and risk and governance, RQ5) are moderated by contex-
                                                                                                                                                                              tual factors (RQ6) and tool ecosystem characteristics (RQ7).

Figure 4: Conceptual framework for vibe coding in software development, synthesized from the thematic analysis of 47 primary
sources. (a) The process view captures the temporal dynamics of a development session, specifically how the iterative loop
operates. (b) The structural view decomposes the phenomenon into interconnected layers that shape and are shaped by the loop,
with each layer grounded in the corresponding research questions.



most frequently reported conceptualizations are the socio-                                                                                                                     The socio-technical framing describes vibe coding as
technical practice framing, appearing in 69% (25) of the                                                                                                                   a development practice rather than only a prompting tech-
sources, and the natural-language-to-code or prompt-based                                                                                                                  nique. In this framing, vibe coding is understood as an
development framing, appearing in 67% (24). The natural-                                                                                                                   interaction pattern of intent articulation, rapid iteration, and
language-to-code perspective treats natural language as the                                                                                                                human steering of generated outputs rather than line-by-
primary interface for specifying functionality and guiding                                                                                                                 line authoring. This reading appears most prominent in
code generation, and prompting as the mechanism for itera-                                                                                                                 practitioner-oriented accounts, and is echoed in some peer-
tive refinement.                                                                                                                                                           reviewed sources.



S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                                                                                                                                                             Page 11 of 35
                                                                                                      Multivocal Review of Vibe Coding


                                                                                         Peer-Reviewed and Grey Literatures: Demographic Details

                                                                                                                                                                                                                                              (67.9%)
                                                                                                         Peer-reviewed Literature                                                                     20
                                                                                               y
                                                                                          Gre ure




                                                                                                                                                 Peer-reviewed Literature
                          25




                                                                                                                                                                            Number of Publications
                                                                                              rat         4
                                                                                         Lite              Journal Article                                                                                                 (28.6%)
                                                                                         100%                                                                                                         10
                                                                                                          Conference Proceedings
                          20                                                               1                                                                                                                                                     18
                                                                                   r-                     4Workshop Paper
                                                                               Pee wed
                                                                                                                                                                                                             (7.2%)
                                                                                           2                                                                                                          5                         8
                                                                                 vie       1
                                                                              Re
 Number of Publications




                                                                                           1                                                                                                                   2
                                                                              57.14%              4
                          15                                                               1
                                                                                 1                            Grey Literature                                                                                Workshop       Journal           Conference
                                                                                           2                                                                                                                  Paper         Articles           Articles
                                                                r-
                                                            Pee wed
                                                              vie                6         2               Research Articles
                          10                               Re
                                                           28.57%                                          Technical Reports
                                                                                                                                                                                                      20




                                                                                                                                                                             Number of Publications
                                     r-         r-              1                                          News
                                 Pee wed    Pee wed                                                                                                                                                          (52.6%)
                                   vie        vie               1




                                                                                                                                                  Grey Literature
                                           Re                                                              Guide                                                                                      10
                                Re                                                        10
                           5                                                     9
                               7.14%        7.14                                                           Video
                                                                6                                                                                                                                              10        (10.5%) (10.5%)                            (10.5%)
                                 1                                                                                                                                                                    5
                                              2                                                            Post                                                                                                                                 (5.2%)     (5.2%)             (5.2%)
                                01     0              0                   0
                                                                                                           Blogs                                                                                                            2           2          1         1        2         1
                           0
                                   2   2    3          3                           5          5
                                202 202 202        202      2024      2024     202        202                                                                                                                Research    Technical
                                                                                                                                                                                                                                       News      Guide      Video    Post     Blog
                                                                                                                                                                                                              Articles    Report




                                     a) Years of Publications                                                                                                                                                 b) Frequency and Types of Papers




Figure 5: Demographic distribution of peer-reviewed and grey-literature sources by publication year, publication type, and source
category.



Table 12                                                                                                                            Table 14
Peer-Reviewed and Grey Literature Distribution                                                                                      Study Category
Code                                 PaperID                                     #  %                                               Code                                                                   PaperID                                      # %
Peer-                                [WL1], [WL2], [WL3], [WL4], [WL5], [WL6], 28 59.57%                                            Full Paper                                                             [WL2], [WL3], [WL4], [WL5], [WL7], [WL9], 29 62%
reviewed                             [WL7], [WL8], [WL9], [WL10], [WL11],                                                                                                                                  [WL10], [WL11], [WL12], [WL13], [WL14],
                                                                                                                                                                                                           [WL16], [WL17], [WL18], [WL19], [WL21],
                                     [WL12], [WL13], [WL14], [WL15], [WL16],
                                                                                                                                                                                                           [WL22], [WL23], [WL24], [WL25], [WL27],
                                     [WL17], [WL18], [WL19], [WL20], [WL21],
                                                                                                                                                                                                           [WL28], [GL1], [GL7], [GL8], [GL10], [GL12],
                                     [WL22], [WL23], [WL24], [WL25], [WL26],                                                                                                                               [GL14], [GL17]
                                     [WL27], [WL28]                                                                                 Blog Post                                                              [GL4], [GL5], [GL13], [GL18], [GL19]         5 11%
Grey                                 [GL1], [GL2], [GL3], [GL4], [GL5], [GL6], 19 40.43%                                            Short Paper                                                            [WL1], [WL8]                                 2 4%
                                     [GL7], [GL8], [GL9], [GL10],[GL11], [GL12],                                                    Industry Report                                                        [WL6], [GL2]                                 2 4%
                                     [GL13], [GL14], [GL15], [GL16], [GL17],                                                        Vision Paper                                                           [WL26], [GL15]                               2 4%
                                     [GL18], [GL19]                                                                                 Position Paper                                                         [WL15], [WL20], [GL3], [GL9]                 4 9%
                                                                                                                                    YouTube Video                                                          [GL6]                                        1 2%
                                                                                                                                    Guide                                                                  [GL11], [GL16]                               2 4%
Table 13
Study Type.
Code                                              PaperID                                     #∗                    %               agents or tool-augmented assistants that carry out multi-
Method Proposal                                   [WL8], [WL14], [WL15], [WL20], [WL21], 15                        31%
                                                  [WL25], [WL27], [GL2], [GL3], [GL8], [GL9],                                       step reasoning, tool invocation, and code modification under
                                                  [GL10], [GL11], [GL15], [GL17]                                                    human supervision.
Experiment                                        [WL1], [WL2], [WL10], [WL11], [WL13], 7
                                                  [WL19], [WL24]
                                                                                                                   15%
                                                                                                                                        Less frequently, vibe coding is framed as AI-assisted
Tool Review                                       [GL1], [GL5], [GL6], [GL11], [GL16], [GL18] 6                    12%              development aligned with the copilot or pair-programming
Exploratory Study                                 [WL3], [WL6], [WL26], [GL4], [GL6], [GL12], 10                   21%              model, appearing in 19% (7) of the sources. In these cases,
                                                  [GL13], [GL14], [GL18], [GL19]
Proof of Concept                                  [WL9], [WL16], [WL17], [WL19], [WL23], 9                         18%
                                                                                                                                    the LLM is positioned primarily as a development assistant
                                                  [WL13], [WL24], [WL28], [GL7]                                                     embedded in the programming workflow rather than as an
Case Study                                        [WL6], [WL7], [WL16], [WL23]                4                    8%               autonomous system. Finally, a small number of sources (6%,
Survey                                            [WL4], [WL5], [WL12], [WL18], [WL22]        5                    10%
                               ∗ = one source may be coded under multiple types
                                                                                                                                    2 sources) conceptualize vibe coding in terms of AI-native
                                                                                                                                    development environments in which the integrated develop-
                                                                                                                                    ment environment and the AI assistant together constitute
    Another recurring perspective conceptualizes vibe cod-                                                                          the primary programming interface.
ing as agentic or semi-autonomous development, appearing                                                                                Across the two evidence streams, peer-reviewed studies
in 50% (18) of the sources. These sources emphasize AI                                                                              more often anchor definitions in established research ter-
                                                                                                                                    minology such as natural-language programming or agent-
                                                                                                                                    mediated development. In contrast, grey sources more fre-
                                                                                                                                    quently articulate vibe coding as a practice identity or

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                                                                                                                                       Page 12 of 35
                                                      Multivocal Review of Vibe Coding

Table 15
RQ coverage by evidence stream
 RQ Field                                  Academic    Grey   Total                                                          Thinking
 RQ1 Definition                               17        19     36                                                            Strategic problem formulation
 RQ2 Workflows / tactics                      24        19     43
                                                                                             Framework
 RQ3.1 Trust / flow / agency / cognitive      22        12     34
                                                                                Architectural Awareness




                                                                                                               Vibe Coding
 load
 RQ3.2 Session momentum                       5         4      9                                                             Checkpoints
 RQ3.3 Audience / task differences            19        15     34
                                                                                                                                   Version Control
 RQ4 Outcomes                                 20        15     35
 RQ5.1 Failure modes                          13         7     20                             Debugging
 RQ5.2 Safeguards / guardrails                19        14     33             Collaborative Error Resolution
 RQ6 Contexts / users                         2          6      8
                                                                                                                             Context
 RQ7 Tools / platforms                        23        16     39
 RQ8 Challenges / future research             13         7     20                                                                Information Provision




workflow style emphasizing rapid iteration, experimenta-                Figure 6: Fundamental skills for effective vibe coding,
tion, and developer steering. Operational definitions vary              as described by two practitioner grey-literature sources
across sources; a synthesized working definition is presented           (Huang [GL6] and Sapkota et al. [GL8]). This is a practitioner-
at the end of this subsection.                                          derived lens rather than a central framework of this review, and
                                                                        it is only partially supported by the wider evidence base.
3.2.1. Fundamental skills for effective vibe coding
    A subset of sources conceptualizes vibe coding in
terms of the developer competencies needed to collabo-
rate with LLMs. Two practitioner-oriented grey-literature
sources (Huang [GL6] and Sapkota et al. [GL8]) describe
the same five skills, Thinking, Framework, Checkpoints,
Debugging, and Context (Figure 6), and present them as
a shift from syntax-focused implementation toward higher-
level guidance and iterative collaboration. Their agreement
offers some corroboration, though both are grey literature
and their independence cannot be verified. Each skill is
broadly consistent with peer-reviewed evidence reported
elsewhere in this review: Thinking with problem formu-                  Figure 7: Thinking layers, based on the practitioner accounts of
lation and prompt engineering (Section 3.3), Framework                  Huang [GL6] and Sapkota et al. [GL8]. Shown as a practitioner-
with retrieval grounding and design-constraint provisioning,            derived illustration, not as a validated framework.
Checkpoints with version-control discipline and validation
(Section 3.6.2), Debugging with the iterate–prompt–patch
loop, and Context with explicit context provisioning. We                Such knowledge helps constrain the solution space and guide
therefore report it as a practitioner-derived lens that is con-         technology choices, and it supports using LLMs to compare
sistent with, rather than derived from, the peer-reviewed               framework alternatives against project requirements.
evidence base.
                                                                        Checkpoints (version control discipline) Checkpoints
Thinking (strategic problem formulation) Thinking is                    are described as a safeguard against the unpredictability of
described as a staged approach to defining a problem for an             generated code. Frequent commits act as recovery points for
LLM. It moves from a logical specification of core intent,              reverting to stable states, and branching supports experimen-
through an analytical description of user interactions and              tation while protecting the main codebase, so iteration can
system components, to a computational decomposition into                proceed while recoverability and traceability are preserved.
modules, rules, and data flows, and finally to procedural
detail such as best practices and feature behaviors (Figure 7).         Debugging (collaborative error resolution) Debugging
The result is often a structured requirements artifact, such as         is described as a collaborative process. The developer sup-
a product requirements document, that serves as a reference             plies diagnostic context, such as error messages, code frag-
for subsequent prompts.                                                 ments, expected versus observed behavior, and logs or
                                                                        screenshots, and the LLM proposes diagnoses and candidate
Framework (architectural awareness) Framework em-                       fixes. Human oversight is still needed to interpret the sugges-
phasizes that, even when an LLM generates much of the                   tions and validate the result.
implementation, developers benefit from familiarity with
relevant frameworks, libraries, and architectural patterns.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                     Page 13 of 35
                                                   Multivocal Review of Vibe Coding

Table 16
Representative definitions and descriptions of vibe coding from the reviewed literature. Quotes are reproduced verbatim from
the primary sources. Sources are ordered chronologically; the table spans both evidence streams and all five conceptualization
categories identified in this review.
     Source      Type          Definition / description (verbatim)
     [GL4]       Grey          “There’s a new kind of coding I call ‘vibe coding’, where you fully give in to the vibes, embrace
                               exponentials, and forget that the code even exists.”
     [WL15]      Peer-         - “ ‘Vibe coding’—the practice of developing software through iteratively conversing with a large
                 reviewed      language model (LLM)—has exploded in popularity within the last year. ”
                               - “Modern LLMs have made vibe coding—writing software by conversing with an LLM—an appealing
                               new workflow, granting developers the ability to rapidly prototype and refine code by prompting an
                               LLM.”
     [WL24]      Peer-         - “Vibe coding, a concept introduced by Andrej Karpathy in February 2025 through X (former Twitter),
                 reviewed      where software is developed by interacting with LLMs using natural language prompts instead of writing
                               code manually.”
                               - “LLM-based vibe coding, where developers interact with Large Language Models using natural
                               language, allowing for rapid prototyping and code generation through conversations.”
     [WL27]      Peer-         “Vibe coding is a software development paradigm where humans and Generative AI engage in
                 reviewed      collaborative flow to co-create software artifacts through natural language dialogue, shifting the
                               mediation of developer intent from deterministic instruction to probabilistic inference.”
     [WL20]      Peer-         “We introduce here the emerging concept of vibe coding, in which artificial intelligence (AI) accelerates
                 reviewed      the coding process by converting natural language or abstract research intent (a ‘vibe’) into functioning
                               software modules, dramatically shortening development cycles.”
     [WL25]      Peer-         “Vibe coding is a recent Generative AI innovation where a human operator provides conversational
                 reviewed      natural language description of a problem and an AI assistant writes the code to develop a solution.
                               [. . . ] It can also be described as an emerging approach to software development where users interact
                               with AI to create code.”
     [GL8]       Grey          “ ‘Vibe coding’ refers to a novel, emergent mode of software development in which the human
                               programmer operates less as a direct implementer of code and more as a high-level coordinator
                               who collaborates with LLMs through iterative prompting and strategic direction. [. . . ] Developers
                               communicate desired outcomes—the ‘vibe’—via natural language instructions, conceptual overviews,
                               and progressive refinements, rather than by specifying logic in syntactic detail.”
     [GL7]       Grey          “An emerging programming paradigm where developers primarily write code by interacting with code-
                               generating large language models rather than writing code directly.”
     [GL10]      Grey          “Vibe coding is a new programming approach where users employ AI code generation tools to write code
                               by describing their desired outcome (in natural language) without fully understanding the AI-generated
                               code. [. . . ] Vibe coding prioritizes speed and experimentation over understanding.”
     [GL11]      Grey          “Vibe coding is an emerging software development practice that uses artificial intelligence (AI) to
                               generate functional code from natural language prompts, accelerating development, and making app
                               building more accessible, especially for those with limited programming experience.”
     [GL3]       Grey          “A new paradigm of software development in which developers use natural language to state their
                               high-level intent [. . . ]; the developer acts as a ‘high-level coordinator’, guiding the AI agent [. . . ]; vibe
                               coding implies ‘generating code with AI without understanding the code that is produced.’ [. . . ] The
                               process is inherently probabilistic and non-deterministic.”
     [GL14]      Grey          “The term ‘vibe coding’ describes creating software with minimal oversight—users focus on the end
                               product rather than systematically reviewing or testing code. [. . . ] Vibe coding involves asking a GenAI
                               tool for code, but not reading that code. To debug, one can paste error messages into the AI, or ask
                               for random changes until it’s fixed.”



Context (information provision) Context highlights the                     problem formulation, constraint specification, disciplined
value of providing enough background to guide the model’s                  iteration, and systematic verification.
outputs, including requirements artifacts, examples, existing
code, API documentation, and explicit constraints such as                  3.2.2. Synthesized working definition.
preferred libraries, coding conventions, or security require-                  Overall, the evidence suggests that vibe coding is not
ments. Fuller context reduces ambiguity and improves the                   only code generation from prompts, but a broader socio-
relevance of generated artifacts.                                          technical practice in which natural language mediates de-
    Taken together, these five skills frame vibe coding as                 veloper intent, model generation, and human validation.
a form of intent articulation and interaction management                   Drawing on the definitions reported across the 47 reviewed
rather than direct line-by-line authoring. They reinforce re-              sources (Table 16), we synthesize the following working
curring conceptualizations of vibe coding identified in RQ1,               definition:
where development is structured as an iterative, human-                        Vibe coding is an intent-driven software development
steered process in which outcomes depend on effective                      practice in which a developer specifies desired functionality,


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                     Page 14 of 35
                                                               Multivocal Review of Vibe Coding

Table 17                                                                              Takeaway 1
RQ1: Conceptualizations of “vibe coding” across sources.
Percentages are relative to the 36 sources contributing to RQ1.                       Across the 36 contributing sources, vibe coding
 Code                         PaperID                              Count*    %        is described most often as an intent-driven socio-
 Socio-technical practice     [WL14], [WL15], [WL20], [WL24],        25     69%
                              [WL25], [WL27], [WL28], [GL1],                          technical practice of human–AI collaboration (69%)
                              [GL2], [GL3], [GL4], [GL5], [GL6],
                              [GL7], [GL8], [GL9], [GL10],                            and as natural-language-to-code or prompt-based
                              [GL11], [GL12], [GL13], [GL14],
                              [GL15], [GL16], [GL18], [GL19]                          development (67%). Agentic or semi-autonomous
 Natural-language-to-code /   [WL1], [WL3], [WL7], [WL10],           24     67%
 Prompt-based development     [WL11], [WL20], [WL24], [WL25],                         framings also appear widely (50%), while copilot-
                              [WL26], [WL27], [WL28], [GL1],
                              [GL2], [GL3], [GL5], [GL7], [GL8],                      style and AI-native IDE framings are rarer. Taken to-
                              [GL9], [GL10], [GL11], [GL12],
                              [GL15], [GL16], [GL17]                                  gether, the evidence indicates that vibe coding is best
 Agentic or semi-autonomous
 development
                              [WL8], [WL13], [WL15], [WL17],
                              [WL20], [WL24], [WL25], [WL27],
                                                                     18     50%
                                                                                      understood as an intent-driven socio-technical prac-
                              [WL28], [GL1], [GL3], [GL7],
                              [GL8], [GL11], [GL12], [GL15],                          tice, in which the developer expresses intent, steers,
 AI-assisted development
                              [GL16], [GL18]
                              [WL4], [WL13], [WL17], [WL25],         7      19%
                                                                                      and validates, rather than only as a way of turn-
 AI-native IDE
                              [GL11], [GL13], [GL17]
                              [WL7], [GL14]                          2      6%
                                                                                      ing natural language into code. Evidence strength
                 ∗ = sources may appear in multiple rows.                             is strong (36 sources across both streams, including
                                                                                      multiple high-quality peer-reviewed studies).
constraints, and context primarily through natural-language
prompts, and one or more large language models generate,                          3.3. Workflows and Tactics (RQ2)
refine, and iteratively revise code artifacts in response. The                        A total of 43 out of 47 sources contributed to RQ2 (24
developer’s role shifts from direct code authoring toward                         peer-reviewed and 19 grey). The contributing peer-reviewed
expressing intent, evaluating generated outputs, providing                        studies were predominantly high or medium quality (the 28-
corrective feedback, and steering successive iterations. In its                   paper peer-reviewed corpus comprises 18 high-, 7 medium-,
strongest form, as originally framed by Karpathy, the devel-                      and 3 low-quality papers; see Table 6), while grey sources
oper foregoes reading or understanding the generated code                         were classified as GL Tier 1–3 (1 at Tier 1, the remainder at
entirely, accepting AI outputs based on observed behavior                         Tier 2 or Tier 3).
rather than code inspection. In practice, the degree of devel-                        Table 18 summarizes the workflow patterns reported
oper oversight varies along a spectrum from minimal review                        for vibe coding across the literature. The most frequently
(“pure” vibe coding) to structured validation incorporating                       reported workflow is the use of validation and evaluation
testing, linting, and human-in-the-loop review. The practice                      pipelines as a core development loop, appearing in 72% (31)
is characterized by rapid prototyping cycles, conversational                      of the sources. These workflows combine generation with
interaction with AI systems, and an inherently probabilistic                      systematic verification activities such as testing, linting, and
generation process whose outcomes depend on prompt for-                           runtime inspection. Across these sources, evaluation is fre-
mulation, model capabilities, and contextual grounding.                           quently positioned as a necessary safeguard for maintaining
This definition synthesizes the five conceptualization cat-                       quality when using AI-generated outputs.
egories identified in Table 17: it encompasses natural-                               The second most common pattern is a chat-based itera-
language-to-code generation (Category 1), the socio-                              tive development loop, reported in 63% (27) of the sources.
technical interaction paradigm of iterative human–AI col-                         This workflow involves conversational interaction between
laboration (Category 2), the agentic dimension in which AI                        developers and LLMs, where successive prompts refine or
systems operate with varying autonomy (Category 3), the                           correct generated artifacts. Several studies describe this con-
copilot-style AI-assisted mode (Category 4), and the AI-                          versational interaction as the primary mechanism through
native IDE environments that embed these capabilities (Cat-                       which developers steer model behavior. For instance, one
egory 5). By acknowledging the spectrum from minimal-                             practitioner-oriented source describes the workflow as one
oversight to structured-validation modes, this formulation                        where “developers interact with AI through natural language
captures both the original Karpathy framing and operational-                      rather than writing or editing code directly,” characterizing
izations emerging in academic literature.                                         vibe coding as a “behavior-driven, conversational style of
                                                                                  programming” [GL12].
                                                                                      In retrieval-augmented workflows, the agent “constructs
                                                                                  prompts using DSL-specific knowledge stored in a vector
                                                                                  database, communicates with the employed LLM, and stores
                                                                                  the full conversation context in a memory module for conti-
                                                                                  nuity in subsequent interactions” [WL24].
                                                                                      Explicit context provisioning represents another fre-
                                                                                  quently reported tactic, appearing in 40% (17) of the sources.
                                                                                  In these workflows, developers provide contextual artifacts

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                   Page 15 of 35
                                                                                                                   Multivocal Review of Vibe Coding

                                                                                                                                                        verification activity, such as automated tests, continuous-
                                                                                                                                                        integration checks, linting, and runtime inspection applied
                     Alerts                      Incident
                                                                                                                                                        to generated code. The iterate–prompt–patch loop refers to
                 Monitoring                   User Feedback                                                                                             the conversational debugging cycle, in which runtime errors
                       Feedback and Observability
                                                                                                                                                        or logs are fed back into successive prompts to repair the




                                                               interprets signals
                    Metrics                     Updated
                                                                                                                    Tool Layer
                                                                                                                 Browser-Based, CLI,
                                                                                                                                                        output across turns. The patch and repair workflow refers
                 App Usage                    Prompt Debug                                                         IDEs and Editors,
                                                                                                                         Plugin                         to localized edits to an existing fragment, rather than full
                                                                                                                                                        regeneration or a verification step. Because these categories
     Deployment and                                                                                                      Prompt-Engineering
                                                                                                                                                        describe different aspects of a workflow, a single source may
     Operations Layer
  Hosting, Rollbacks, Monitoring
                                                       Vibe Coding
                                                                                                                             Layer
                                                                                                                                Prompt Library,         be coded under more than one. The counts therefore report
                                                                                                                                                        how many sources mention each pattern and do not form
                                                                                                                          Versioning, Debugger




                                                                                                                                                        mutually exclusive groups. Taken together, these patterns
    LLM Provider Layer                                                              crafts & refines                   Interaction Layer
                                                                                                                                                        describe vibe coding as an iterative generation–evaluation–
     OpenAI, Anthropic, Ollama                                                                                  CI/CD, Database Access, Authorization
                                                                                                                                                        refinement loop rather than a one-shot code-generation ac-
                                                                                                                                                        tivity. Validation and testing sit inside this loop rather than
                           MCP Layer
                                                                                                                                                        as optional additions: generated code is evaluated, repaired,
                                                                                                Stack Engine Layer
                      MCP Gost, MCP Client,
                              MCP Server
                                                                                                Next.js, Astro, Angular, Qwik                           and refined before it is relied upon.
                                                                                                                                                             Across evidence streams, peer-reviewed studies more
                                                                                                                                                        frequently describe structured workflows that integrate re-
Figure 8: Layered vibe-coding workflow architecture, adapted                                                                                            trieval mechanisms and systematic verification pipelines,
from Ray [14]. The developer (left) composes a natural-                                                                                                 whereas grey sources tend to emphasize rapid iteration, con-
language prompt in the Prompt Box. The request passes                                                                                                   versational prompting, and exploratory trial-and-error inter-
through the Tool, Prompt-Engineering, and Integration layers                                                                                            action. Although workflow patterns are widely described,
before reaching the LLM Provider. Generated code is assem-                                                                                              empirical comparisons of workflow effectiveness remain
bled by the Stack Engine, deployed through the Deployment                                                                                               limited. Figure 8 situates the workflow patterns identified
& Operations layer, and monitored via the Feedback &                                                                                                    in this review within a layered vibe-coding architecture.
Observability layer. Observability signals (metrics, alerts, logs)                                                                                      The layered structure is adapted from Ray [14], while the
are returned to the developer, who interprets them, refines
                                                                                                                                                        placement of prompting, tooling, validation, deployment,
the prompt, and re-enters the cycle. The layered structure is
                                                                                                                                                        and feedback within it, and their arrangement as an iterative
adapted from Ray [14]; the placement of validation, feedback,
and the iterate–prompt–patch loop within it reflects the                                                                                                loop, reflects the patterns synthesized in this review (Ta-
workflow patterns synthesized in this review (RQ2).                                                                                                     ble 18). The figure shows how these stages form an iterate–
                                                                                                                                                        prompt–patch loop in which observability signals return to
                                                                                                                                                        the developer, who refines the prompt and re-enters the
                                                                                                                                                        cycle.
such as requirements, constraints, documentation, or ex-
isting code snippets to guide model responses and reduce                                                                                                   Takeaway 2
ambiguity in generated outputs.
     An additional pattern described in 35% (15) of the                                                                                                    Across the 43 contributing sources, the leading
sources is the iterate–prompt–patch loop. In this workflow,                                                                                                workflow patterns are validation and evaluation
developers repeatedly refine prompts, incorporate runtime
                                                                                                                                                           pipelines (72%) and chat-based iterative loops (63%),
errors or logs into the interaction, and iteratively repair gen-
erated code. Practitioner-oriented sources such as [GL8] and                                                                                               often combined with context provisioning and
[GL12] frequently describe this loop as a practical strategy                                                                                               prompt–repair cycles. This indicates that vibe cod-
for debugging and refining AI-generated artifacts.                                                                                                         ing operates as an iterative generation–evaluation–
     Retrieval and documentation grounding is reported in
                                                                                                                                                           refinement loop rather than a one-shot code gener-
30% (13) of the sources. These workflows integrate re-
trieval mechanisms that allow models to access external                                                                                                    ation activity. Validation and testing appear to be
documentation, repositories, or project artifacts, for instance                                                                                            central to that loop rather than optional additions,
by referencing documentation during generation or using                                                                                                    because generated code is evaluated, repaired, and
repository search to ground prompts.
                                                                                                                                                           refined before it is trusted. The quality of the result
     Less frequently reported workflow patterns include patch
and repair workflows (14%, 6 sources), inline IDE-assisted                                                                                                 therefore seems to depend on the strength of the eval-
completion (9%, 4 sources), and collaborative prompt prac-                                                                                                 uation loop around the AI-generated code. Evidence
tices (2%, 1 source).                                                                                                                                      strength is strong (43 sources; both leading patterns
     Three of these categories are closely related, so we state
                                                                                                                                                           appear across both evidence streams).
their boundaries to make clear that the same evidence is not
counted twice. Validation and evaluation pipelines refers to


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                                                                        Page 16 of 35
                                                                  Multivocal Review of Vibe Coding

Table 18                                                                              Table 19
RQ2: Dominant workflow patterns reported for vibe coding.                             RQ3.1: Developer role and cognitive/behavioral shifts. Per-
Percentages are relative to the 43 sources contributing to RQ2.                       centages are relative to the 34 sources contributing to RQ3.1.
 Code                             PaperID                              Count*    %     Code                              PaperID                           Count*    %
 Validation and evaluation        [WL1], [WL2], [WL3], [WL4],            31     72%    Trust calibration and adaptive    [WL3], [WL4], [WL6], [WL8],         23     68%
 pipelines as a core loop         [WL6], [WL7], [WL8], [WL9],                          reliance                          [WL9], [WL13], [WL16], [WL20],
                                  [WL14], [WL15], [WL16], [WL17],                                                        [WL21], [WL22], [WL23], [WL25],
                                  [WL18], [WL19], [WL20], [WL21],                                                        [WL27], [GL1], [GL2], [GL6],
                                  [WL22], [WL24], [WL25], [GL1],                                                         [GL7], [GL9], [GL10], [GL11],
                                  [GL3], [GL5], [GL7], [GL8], [GL9],                                                     [GL12], [GL13], [GL17]
                                  [GL10], [GL11], [GL14], [GL15],                      Changes in cognitive load         [WL7], [WL8], [WL9], [WL11],        13     38%
                                  [GL16], [GL17]                                                                         [WL14], [WL17], [WL19], [WL21],
 Chat-based iterative develop-    [WL2], [WL3], [WL4], [WL7],            27     63%                                      [WL25], [WL27], [WL28], [GL2],
 ment loop                        [WL8], [WL9], [WL13], [WL14],                                                          [GL3]
                                  [WL15], [WL17], [WL18], [WL19],                      Cognitive debt due to deferred    [WL4], [WL5], [WL8], [WL15],        8      24%
                                  [WL21], [WL24], [WL25], [WL27],                      understanding                     [WL25], [GL10], [GL13], [GL19]
                                  [WL28], [GL1], [GL2], [GL3],                         Flow effects                      [WL2], [WL4], [WL8], [WL27],        7      20%
                                  [GL4], [GL10], [GL11], [GL12],                                                         [WL28], [GL1], [GL6]
                                  [GL14], [GL16], [GL18]
                                                                                       Shift from direct authoring to-   [WL6], [WL25], [GL13]               3      9%
 Explicit context provisioning    [WL3], [WL4], [WL7], [WL9],            17     40%    ward supervision and steering
                                  [WL13], [WL20], [WL21], [WL24],                      roles
                                  [WL28], [GL1], [GL4], [GL6],
                                  [GL10], [GL14], [GL15], [GL16],                             ∗ = one source may contribute to multiple categories
                                  [GL19]
 Iterate–prompt–patch loop        [WL4], [WL6], [WL24], [WL27],          15     35%
                                  [WL28], [GL1], [GL3], [GL8],
                                  [GL10], [GL11], [GL12], [GL13],                          Cognitive debt is reported in 24% (8) of the sources
                                  [GL15], [GL18], [GL19]
 Retrieval and documentation      [WL2], [WL4], [WL7], [WL12],           13     30%   and refers to the accumulation of shallow or deferred un-
 grounding                        [WL20], [WL21], [WL22], [WL24],
                                  [WL28], [GL1], [GL2], [GL15],
                                                                                      derstanding when developers accept generated code without
                                  [GL16]                                              fully comprehending its structure or behavior. As one source
 Patch and repair workflow        [WL3], [WL17], [WL20], [WL21],
                                  [GL4], [GL16]
                                                                         6      14%
                                                                                      observes, vibe coding “flips some of these assumptions:
 Inline IDE-assisted completion   [WL3], [WL19], [WL21], [GL5]           4      9%    the need for active participation of the human expert, the
 Collaborative prompt practices   [WL11]                                 1      2%
                                                                                      importance of knowing and understanding every line of
                ∗ = sources may appear in multiple rows.
                                                                                      code, and the human operator’s ability to accurately describe
                                                                                      what is required” [WL25].
3.4. Developer Role Shift (RQ3)                                                            A more critical perspective warns that the practice
    This RQ reports one developer-role shift seen from three                          “normalizes randomness, encouraging a culture of low-
angles: the cognitive and behavioral constructs that accom-                           accountability development” whose “costs are rarely visible
pany it (RQ3.1), the within-session interaction dynamics                              in the short term—but they accrue in the long-term debt of
(RQ3.2), and the differences by audience and task (RQ3.3).                            unmaintainable systems, fragile architectures, and undocu-
Across all three, the developer moves from writing code di-                           mented logic” [GL9].
rectly toward supervising, validating, and steering AI output.                             For example, [WL5] and [WL15] highlight the risk that
                                                                                      rapid AI-assisted iteration may postpone deeper reasoning
3.4.1. Trust, Cognitive Load, and Cognitive Debt                                      about design decisions, potentially increasing debugging
    This subsection reports the cognitive and behavioral con-                         and maintenance effort later in the development lifecycle.
structs that accompany the role shift (Table 19). The central                         Practitioner-oriented sources such as [GL10] similarly cau-
pattern is that vibe coding moves the developer from writing                          tion that fast iteration can lead to brittle code when develop-
code directly toward supervising the model, validating its                            ers rely heavily on generated outputs.
output, calibrating trust in it, and managing the context it                               Flow-related effects are discussed in 20% (7) of the
is given. The most frequently discussed construct is trust                            sources. These studies describe how conversational inter-
calibration and adaptive reliance, appearing in 68% (23)                              action with AI systems can sometimes improve develop-
of the sources: developers adjust their reliance on model                             ment flow by accelerating routine implementation tasks.
outputs based on observed errors, task complexity, and ver-                           For example, [WL2] reports smoother iteration during ex-
ification outcomes, and typically apply stricter verification                         ploratory development tasks, while [GL1] describes rapid
for unfamiliar functionality than for routine tasks.                                  conversational prototyping that reduces implementation
    Changes in cognitive load represent another widely dis-                           friction. However, several studies also report interruptions
cussed shift, appearing in 38% (13) of the sources. Sev-                              in flow when developers must repair incorrect outputs or re-
eral peer-reviewed studies examine how interaction with AI                            establish lost context during long interaction sessions.
systems introduces new forms of cognitive effort related                                   Finally, a smaller set of studies (9%, 3 sources) explicitly
to prompt formulation, verification, and context switching.                           discusses a shift from direct code authoring toward supervi-
For instance, [WL7] and [WL19] discuss the additional                                 sion and steering roles. In these cases, developers primarily
effort required to evaluate uncertain outputs and maintain                            frame constraints, evaluate generated solutions, and guide
awareness of system behavior during iterative prompting.                              subsequent iterations rather than writing implementation de-
In contrast, grey sources such as [GL2] and [GL3] more                                tails directly. For instance, [WL6] describes developers act-
frequently describe cognitive load in terms of practical work-                        ing as supervisors of AI-generated solutions, while [WL25]
flow friction during development.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                       Page 17 of 35
                                                                   Multivocal Review of Vibe Coding

Table 20                                                                                 Another observed pattern involves context window or
RQ3.2: Session-level dynamics. Counts are reported out of the                        state-retention failures. These failures occur when earlier
full corpus of 47 sources; percentages are omitted because the                       context is truncated or insufficiently retained across multi-
contributing source count is small.                                                  turn interactions, causing the model to lose important infor-
 Code                                      PaperID                        Count*     mation required for consistent generation. A smaller num-
 Session momentum breaks due to failure,
 misalignment, or tool friction
                                           [WL4], [WL23], [GL7], [GL14]     4
                                                                                     ber of studies describe looping behaviors. In these cases,
 Repetitive prompt–patch cycles without    [WL6], [GL13], [GL19]            3        developers become trapped in repetitive prompt–patch cy-
 convergence
 Context window or state-retention fail-   [WL7], [WL16]                    2
                                                                                     cles where generated outputs repeatedly fail to resolve the
 ures                                                                                underlying issue.
        ∗ = one source may contribute to multiple categories                             Across evidence streams, peer-reviewed studies tend to
                                                                                     describe these phenomena at a technical level, particularly
                                                                                     with respect to context limitations and system constraints,
characterizes the role shift as moving from “writing code”                           whereas grey sources more frequently describe session mo-
toward “orchestrating generation and validation.”                                    mentum and interaction friction from a practitioner work-
    Across evidence streams, peer-reviewed studies more                              flow perspective.
frequently operationalize constructs such as trust calibra-
tion and cognitive load as measurable phenomena, whereas                                Takeaway 4
grey sources tend to emphasize experiential descriptions of
agency shifts and developer steering practices.                                         Session-level dynamics such as momentum breaks,
                                                                                        repeated prompt–patch cycles, and context loss are
    Takeaway 3
                                                                                        reported in only a small subset of sources. These
    The evidence points to a shift in the developer role,                               patterns appear real but remain underexplored, so
    from writing code directly toward supervising, val-                                 they are better read as an open research direction
    idating, and steering AI output and managing the                                    than as an established finding. Evidence strength is
    context given to it. Trust calibration and adaptive                                 emerging (9 contributing sources; each phenomenon
    reliance is the most reported construct (68%), fol-                                 reported by 2 to 4 sources).
    lowed by changes in cognitive load (38%), cognitive
    debt (24%), and flow effects (20%). These constructs                             3.4.3. Differences by Audience and Task
    appear to describe different aspects of the same role                                 A total of 34 out of 47 sources contributed to RQ3.3
    shift. Peer-reviewed sources tend to treat them as                               (19 peer-reviewed and 15 grey). All percentages in this
                                                                                     subsection are expressed relative to the full corpus of 47
    measurable constructs, while grey sources describe                               sources to reflect the overall prevalence of each audience and
    them as workflow experience. Evidence strength is                                task type across the literature.
    moderate (34 sources spanning peer-reviewed and                                       This subsection reports how vibe coding use differs by
    grey work; trust calibration is well supported and                               audience and by task domain. Two audience profiles emerge
                                                                                     (Table 21). Novice or non-programmer-oriented usage ap-
    consistent across both streams, while cognitive debt                             pears in 45% (21) of the sources, where vibe coding lowers
    and the explicit role shift rest on fewer sources).                              entry barriers to software creation. Expert-oriented usage
                                                                                     appears in 43% (20) of the sources, where experienced
3.4.2. Session Dynamics and Context Momentum                                         developers accelerate routine implementation tasks while
    Table 20 summarizes the session-level interaction dy-                            retaining responsibility for architectural reasoning and veri-
namics reported across the literature. Compared with other                           fication. Vibe coding therefore appears to serve two different
role-related constructs, these dynamics are discussed in rel-                        roles at once, accessibility for novices and acceleration for
atively few sources, indicating that session-level interaction                       experts, which mirrors the role shift in RQ3.1: novices gain
patterns remain underexplored in the current evidence base.                          a route into software creation, while experts move toward
    The most frequently reported phenomenon is session                               steering and validation.
momentum breaks, reported in 4 of the 47 sources. These                                   Table 22 presents a separate dimension: the application
breaks occur when iterative development flow is interrupted                          domains in which vibe coding is reported. UI and front-end
due to generation failures, misalignment between developer                           prototyping is the most frequently mentioned task context,
intent and model output, or friction in the development tools                        appearing in 28% (13) of the sources, consistent with the
themselves. For example, [WL4] describes interruptions                               literature’s emphasis on rapid interface prototyping and it-
caused by repeated generation errors that require developers                         erative design workflows. Data and machine-learning tasks
to reformulate prompts, while [GL7] reports practical work-                          appear in only 4% (2) of the sources. Other task domains
flow disruptions when generated code diverges significantly                          such as back-end development, API design, or infrastructure
from expected functionality.                                                         automation were not explicitly coded as distinct categories


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                    Page 18 of 35
                                                            Multivocal Review of Vibe Coding

Table 21                                                                          Takeaway 5
RQ3.3: Target audience differentiation. Percentages are rela-
tive to the full corpus of 47 sources.                                            Vibe coding appears to serve two distinct roles:
Audience                       PaperID                           Count* %         accessibility for novices (45%) and acceleration for
Novice or non-programmer       [WL3], [WL4], [WL5], [WL7],       21     45%
orientation                    [WL8], [WL9], [WL11], [WL12],                      experts (43%). Novice-oriented accounts stress lower
                               [WL25], [WL27], [GL2], [GL3],
                               [GL7], [GL10], [GL12], [GL13],                     entry barriers, while expert-oriented accounts stress
                               [GL14], [GL16], [GL17], [GL18],
                               [GL19]                                             faster routine implementation with continued over-
Expert acceleration            [WL1], [WL5], [WL7], [WL8],
                               [WL9], [WL11], [WL12], [WL14],
                                                                 20    43%        sight. Task-domain evidence is narrow and concen-
                               [WL18], [WL19], [WL22], [WL23],                    trated on UI and front-end prototyping (28%), with
                               [WL25], [GL1], [GL3], [GL5],
                               [GL7], [GL10], [GL12], [GL13]                      data and machine-learning tasks in only two sources,
       ∗ = one source may contribute to multiple categories
                                                                                  so these findings may not generalize to other soft-
                                                                                  ware tasks. Evidence strength is moderate for the
Table 22
RQ3.3: Task domain differentiation. Percentages are relative                      audience split and weak for task-domain coverage.
to the full corpus of 47 sources.
Task domain                     PaperID                          Count* %
UI and front-end prototyping    [WL1], [WL5], [WL8], [WL9],      13     28%
                                                                              3.5. Productivity, Quality, and Maintainability
                                [WL18], [WL20], [WL28], [GL3],                     (RQ4)
                                [GL5], [GL8], [GL11], [GL13],
                                [GL18]                                             This subsection reports the outcomes attributed to vibe
Data and machine learning       [WL13], [WL20]                   2      4%    coding, across productivity, quality, maintainability, defects,
tasks
       ∗ = one source may contribute to multiple categories
                                                                              and reproducibility. The main pattern is that the evidence
                                                                              is strongest for short-term gains and much weaker for long-
                                                                              term software quality. The most frequently reported outcome
in the reviewed literature; these activities are occasionally                 is improved productivity and reduced time-to-prototype, ap-
mentioned but are typically subsumed under general “code                      pearing in 45% (21) of the sources (Table 23). These sources
generation” rather than being analyzed as separate applica-                   describe acceleration in early-stage activities such as code
tion contexts. This gap suggests that empirical evidence on                   generation, UI prototyping, and rapid feature iteration.
vibe coding remains concentrated on front-end and UI tasks,                        Quality-related outcomes are discussed in 36% (17) of
and future work should investigate its effectiveness across a                 the sources. These findings include both perceived improve-
broader range of software-engineering activities.                             ments in generated code or UI artifacts and concerns re-
    Google Cloud’s practitioner guide distinguishes two                       garding correctness and robustness. For instance, [WL6]
modes: “ ‘pure’ vibe coding,” in which “a user might fully                    report that AI-generated solutions can produce acceptable or
trust the AI’s output to work as intended,” and “responsi-                    even high-quality outputs for certain tasks, whereas [GL18]
ble AI-assisted development,” in which “AI tools act as a                     highlight instances where generated code requires additional
powerful accelerator, with the developer maintaining over-                    verification due to potential inaccuracies or incomplete im-
sight” [GL11].                                                                plementations. Maintainability implications appear in 23%
    Grey sources such as [GL1] and [GL10] describe expe-                      (11) of the sources. One study notes that “code generated
rienced developers using vibe coding to accelerate routine                    through conversational flows often lacks cohesive structure,
development tasks while retaining control over design deci-                   consistent patterns, and proper documentation, greatly com-
sions and validation processes.                                               plicating future maintenance” [WL27].
    Across evidence streams, grey sources more frequently                          Similarly, a grey-literature source cautions that the “costs
describe vibe coding as a technology that lowers barriers to                  of this transformation are rarely visible in the short term—
software creation, often emphasizing accessibility for novice                 but they accrue in the long-term debt of unmaintainable sys-
users. Peer-reviewed studies, by contrast, more frequently                    tems, fragile architectures, and undocumented logic” [GL9].
analyze differences between novice and expert developer                            These studies often link maintainability challenges to
behavior, particularly with respect to verification practices                 shallow understanding of generated code, incremental patch-
and interaction strategies.                                                   ing practices, and limited documentation of design intent.
                                                                              For example, [WL5] and [WL15] discuss how rapid AI-
                                                                              assisted iteration can introduce structural complexity that
                                                                              complicates later maintenance, while [GL10] notes that
                                                                              developers sometimes accept generated code without fully
                                                                              understanding its long-term implications.
                                                                                   Defect risks and error patterns are also reported in 21%
                                                                              (10) of the sources. These studies frequently discuss de-
                                                                              fects alongside productivity gains, suggesting that increased
                                                                              development speed may introduce additional verification


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                Page 19 of 35
                                                                                    Multivocal Review of Vibe Coding


                                           (a) Audience vs Reported Outcomes                                                                                                   (b) Task Domain vs Reported Outcomes
                                                                                                                                                                                                                                      7




                                                                                                                             Task Domain (RQ3.3)
                                                                                                     10
Audience (RQ3.3)


                                12              9              8               6           2                                                                              4           7              2               2       2




                                                                                                         Number of Sources




                                                                                                                                                                                                                                      Number of Sources
                   Novice                                                                                                                          UI / Front-end                                                                     5

                                                                                                     5                                                                                                                                3
                   Expert        7              7              4               4           1                                                           Data / ML          1           2              0               0       1
                                                                                                     0                                                                                                                                0
                            Productivity      Quality       Maintain-     Defects      Reproduci-                                                                    Productivity   Quality       Maintain-    Defects   Reproduci-
                                                             ability                     bility                                                                                                    ability                 bility
                                                    Outcome Dimensions (RQ4)                                                                                                              Outcome Dimensions (RQ4)
                            (a) Audience categories vs. reported outcomes.                                                                                          (b) Task domain vs. reported outcomes.

Figure 9: Relationship between RQ3.3 categories and reported development outcomes (RQ4). Cell values represent the number
of sources reporting each outcome for the corresponding category. (a) Audience dimension: novice-oriented sources emphasize
productivity, while expert-oriented sources show a more balanced distribution across outcome types. (b) Task-domain dimension:
UI and front-end tasks dominate the evidence base, with data/ML tasks appearing in only two sources.



Table 23                                                                                                                          Figure 9a shows the audience dimension: productivity im-
RQ4: Reported outcomes of vibe coding. Percentages are                                                                            provements are most frequently associated with novice-
relative to the full corpus of 47 sources.                                                                                        oriented contexts (12 sources), reflecting the recurring claim
  Code                                                  PaperID                         Count*       %                            that vibe coding lowers barriers to entry and enables rapid
  Productivity                                          [WL3],     [WL4],     [WL6],      21        45%                           prototyping for less experienced developers. Expert-oriented
                                                        [WL8],    [WL9],    [WL12],
                                                        [WL13], [WL16], [WL17],                                                   usage shows a more balanced distribution across productiv-
                                                        [WL19], [WL21], [WL25],
                                                        [WL27], [GL2], [GL7], [GL8],
                                                                                                                                  ity (7), quality (7), and defect outcomes (4), suggesting that
                                                        [GL11],   [GL12],    [GL15],                                              experienced developers use vibe coding as an acceleration
                                                        [GL16], [GL17]
  Code or UI quality                                    [WL3],     [WL5],     [WL6],        17      36%
                                                                                                                                  mechanism while maintaining verification practices. Fig-
                                                        [WL7],    [WL8],    [WL13],                                               ure 9b presents the task-domain dimension independently.
                                                        [WL20], [WL21], [WL22],
                                                        [WL25], [GL2], [GL5], [GL8],                                              UI and front-end development tasks are frequently linked to
                                                        [GL13],   [GL15],    [GL16],                                              quality improvements (7 sources) and productivity gains (4),
                                                        [GL18]
  Maintainability implications                          [WL3],    [WL5],    [WL15],         11      23%                           consistent with the emphasis on rapid interface prototyping.
                                                        [WL21], [WL27], [GL2],
                                                        [GL10],   [GL12],    [GL13],
                                                                                                                                  Data and machine-learning tasks appear in only two sources,
                                                        [GL15], [GL19]                                                            providing insufficient evidence for reliable cross-tabulation.
  Defect risks and error patterns                       [WL2],
                                                        [WL6],
                                                                   [WL4],
                                                                  [WL7],
                                                                              [WL5],
                                                                            [WL24],
                                                                                            10      21%
                                                                                                                                  Overall, the separation of these two dimensions highlights
                                                        [GL3], [GL4], [GL10], [GL19]                                              that outcome claims vary substantially by both user expertise
  Reproducibility and consistency                       [WL20], [WL27], [GL3]               3       6%
                                                                                                                                  and task context, and should be interpreted in relation to the
                       ∗ = one source may contribute to multiple categories
                                                                                                                                  specific development setting.

                                                                                                                                                     Takeaway 6
burdens. Finally, reproducibility and consistency concerns
are reported in only 6% (3) of the sources. These studies                                                                                            The evidence is strongest for short-term gains in
highlight that outputs may vary across prompt formulations,                                                                                          productivity and time-to-prototype (45%) and much
model versions, or interaction contexts. Taken together,
                                                                                                                                                     weaker for long-term quality (36%), maintainabil-
these outcomes point to a trade-off rather than a general
improvement: vibe coding may speed up prototyping, but                                                                                               ity (23%), defects (21%), and reproducibility (6%).
quality, maintainability, and reproducibility appear condi-                                                                                          This points to a trade-off rather than a general im-
tional on developer expertise, task complexity, and verifica-                                                                                        provement: vibe coding may speed up prototyping,
tion practices, rather than being reliable gains.
                                                                                                                                                     but that benefit appears to depend on developer ex-
    Across evidence streams, peer-reviewed studies more
frequently report measurable task performance outcomes                                                                                               pertise, task complexity, and verification practices.
or controlled evaluations and explicitly discuss trade-offs                                                                                          Quality and maintainability are therefore better read
between productivity and verification effort. Grey sources, in                                                                                       as conditional outcomes than as reliable gains. Ev-
contrast, more commonly emphasize perceived productivity
                                                                                                                                                     idence strength is moderate (productivity is sup-
gains and rapid prototyping success, although the level of
empirical substantiation varies.                                                                                                                     ported across 21 sources from both the peer-reviewed
    Figure 9 illustrates how reported outcomes (RQ4) vary                                                                                            and grey streams, while reproducibility rests on only
across the two RQ3.3 dimensions separately. Whereas Ta-                                                                                              3).
ble 23 reports outcomes for the whole corpus, this figure
splits them by audience and task: it shows that productiv-
ity dominates the novice column, while the expert column
is more balanced across productivity, quality, and defects.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                                                                                                         Page 20 of 35
                                                   Multivocal Review of Vibe Coding

3.6. Risks and Safeguards (RQ5)                                      Table 24
3.6.1. Failure Modes                                                 RQ5.1: Reported failure modes of vibe coding. Percentages are
    Of the 47 sources, 20 provided data coded under RQ5.1            relative to the full corpus of 47 sources; 20 sources provided
(13 peer-reviewed and 7 grey); however, percentages in               specific data on failure modes.
this section represent prevalence across the full corpus of           Code                           PaperID                           Count*    %
47 sources, so that readers can assess how commonly each              Hallucinations and incorrect
                                                                      generations
                                                                                                     [WL1], [WL5], [WL6], [WL7],
                                                                                                     [WL8], [WL16], [WL18], [WL20],
                                                                                                                                         13     28%

failure mode appears in the vibe coding literature overall                                           [WL24], [WL25], [GL1], [GL2],
                                                                                                     [GL10]
(see denominator note at the start of Section 3). Six of the          Licensing and provenance       [WL14], [WL28], [GL17]               3     6%
seven contributing grey sources were classified as GL Tier 2;         uncertainty

one (GL7) was GL Tier 1. Table 24 summarizes the failure              Cumulative context errors
                                                                      and iteration drift
                                                                                                     [WL15], [GL19]                       2     4%

modes associated with vibe coding reported across the liter-          Minimal-review      commits    [GL7], [GL13]                        2     4%
                                                                      and insufficient inspection
ature. The most frequently reported risk concerns hallucina-          practices
tions and incorrect generations, appearing in 28% (13 out of                 ∗ = one source may contribute to multiple categories

47) of the sources. These failures include confident but incor-
rect code outputs, logical inconsistencies, or generated solu-
tions that appear plausible but contain subtle errors. As one            Overall, the evidence suggests that vibe coding risks
peer-reviewed study warns, LLMs “frequently generate er-             are not only technical errors in generated code, but also
roneous code segments or hallucinate, presenting seemingly           workflow risks created by rapid iteration, reduced review,
correct answers that are actually wrong” [WL24], while a             and overreliance on model outputs.
practitioner account observes that “the risks of overtrust
                                                                         Takeaway 7
emerge when users fail to critically evaluate AI outputs or
lack the expertise to identify problematic code” [GL7].                  The most frequently reported failure mode in vibe
    The remaining failure modes rest on few sources and are
                                                                         coding is hallucinated or incorrect code genera-
better read as lower-frequency or emerging risks. Licensing
and provenance uncertainty appears in 6% (3) of the sources,             tion. Additional risks include licensing uncertainty,
which raise concerns about the origin and legal status of                cumulative context drift across iterations, and re-
generated code fragments. Cumulative context errors and                  duced review discipline when integrating gener-
iteration drift appear in 4% (2) of the sources. In these cases,
                                                                         ated outputs. While peer-reviewed studies empha-
misunderstandings introduced in earlier prompts propagate
through subsequent iterations, leading to increasingly mis-              size correctness-related risks, practitioner sources
aligned outputs. [WL15], for example, reports interaction                highlight workflow-related vulnerabilities associated
scenarios where successive prompts amplify earlier errors                with rapid AI-assisted development. This suggests
rather than correcting them. Minimal-review commits and
                                                                         that managing vibe coding risk depends not only on
insufficient inspection practices are also reported in 4% (2)
of the sources and appear predominantly in grey litera-                  catching generation errors but also on the review and
ture. These accounts describe situations where developers                iteration practices around the tool. Evidence strength
integrate AI-generated code into repositories with limited               is moderate (hallucination/incorrect-generation risk
review due to the speed of automated generation.
                                                                         is corroborated across both streams and includes
    Across evidence streams, peer-reviewed studies more
frequently document correctness-related risks such as hal-               peer-reviewed sources; the remaining failure modes
lucinations and context-related errors, often analyzing them             rest on few, mainly practitioner sources).
at a technical level. In contrast, grey sources more fre-
quently highlight workflow-related risks, particularly those
                                                                     3.6.2. Governance and Guardrails
associated with reduced review discipline or overreliance on
                                                                         A total of 33 out of 47 sources contributed to RQ5.2
generated outputs.
                                                                     (19 peer-reviewed and 14 grey). Of the 14 contributing
Cross-stream corroboration. The contributing grey                    grey sources, 12 were classified as GL Tier 2 and two
sources are mostly GL Tier 2, with one GL Tier 1 (GL7),              (GL15, GL18) as GL Tier 3. Because the grey evidence
so we checked whether their reported failure modes are               base for safeguards is almost entirely Tier 2, we explic-
corroborated by peer-reviewed evidence. Hallucinated or              itly checked each major safeguard category against peer-
incorrect generation [GL1] is independently documented               reviewed evidence. Validation and testing pipelines (the
in peer-reviewed studies [WL6][WL7], and context drift               most frequent grey recommendation) are independently sup-
converges with peer-reviewed accounts of iteration-induced           ported by multiple peer-reviewed studies [WL1][WL7] de-
error propagation [WL15]. These modes appear convergent              scribing continuous-integration and runtime validation as
across both streams. Workflow risks such as minimal-review           core practices. Human-in-the-loop review likewise appears
commits lack peer-reviewed corroboration and are reported            in peer-reviewed sources [WL6] as in Tier 2 practitioner
as practitioner-sourced and weaker.                                  accounts. By contrast, behavioral guardrails emphasized by
                                                                     grey sources (e.g., disciplined review routines) have weaker

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                      Page 21 of 35
                                                   Multivocal Review of Vibe Coding

peer-reviewed backing, and we therefore report them as               Table 25
primarily practitioner-derived rather than cross-validated.          RQ5.2: Reported safeguards and governance mechanisms in
Table 25 summarizes governance mechanisms and safe-                  vibe coding. Percentages are relative to the 33 sources con-
guards reported for vibe coding workflows. The most fre-             tributing to RQ5.2.
quently reported safeguard is the use of validation and testing       Code                           PaperID                           Count*    %
pipelines, appearing in 88% (29) of the sources. These mech-          Validation
                                                                      pipelines
                                                                                   and     testing   [WL2], [WL4], [WL5], [WL6],
                                                                                                     [WL7], [WL8], [WL11], [WL15],
                                                                                                                                         29     88%

anisms include automated testing, continuous integration                                             [WL16], [WL17], [WL18], [WL20],
                                                                                                     [WL21], [WL23], [WL24], [WL26],
checks, linting, and runtime validation designed to detect                                           [WL28], [GL1], [GL2], [GL3],
errors introduced by AI-generated code.                                                              [GL8], [GL10], [GL11], [GL12],
                                                                                                     [GL13], [GL14], [GL15], [GL16],
     Human-in-the-loop review represents another widely re-                                          [GL17]

ported safeguard, appearing in 48% (16) of the sources.               Human-in-the-loop              [WL4], [WL6], [WL8], [WL15],
                                                                                                     [WL24], [WL25], [GL2], [GL8],
                                                                                                                                         16     48%

These studies emphasize explicit developer oversight during                                          [GL11], [GL12], [GL13], [GL14],
                                                                                                     [GL16], [GL17], [GL18], [GL19]
generation, evaluation, and integration of AI-generated ar-           Sandboxing and constrained     [WL9], [WL20], [WL23], [WL25],      5      15%
tifacts. For instance, [WL6] highlights review practices in           execution environments
                                                                      Explicit guidance on when to
                                                                                                     [GL1]
                                                                                                     [GL19]                              1      3%
which developers inspect generated code before committing             avoid vibe coding
it to repositories, while grey sources such as [GL12] and             Provenance     tracking
                                                                      traceability mechanisms
                                                                                               and   [WL20]                              1      3%

[GL17] describe disciplined review routines as essential for                 ∗ = one source may contribute to multiple categories
maintaining quality during rapid AI-assisted development.
     Sandboxing and constrained execution environments ap-
pear in 15% (5) of the sources. One source describes a                    Takeaway 8
“multi-tiered sandbox” in which “Apple’s Seatbelt confines
all operations to a read-only jail” and “Docker-based iso-                Validation and review practices are the most fre-
lation combined with iptables firewall rules” enforces con-               quently recommended safeguards in vibe coding
finement on Linux [GL1]. These mechanisms are intended                    workflows. Few studies, however, provide empirical
to limit potential risks by isolating generated code within
                                                                          evidence on whether these safeguards reduce risk
controlled environments. Two safeguards appear in single
sources and are better read as emerging. [GL19] suggests                  in real development settings, so the field converges
avoiding AI-assisted generation in safety-critical contexts               more on what to recommend than on what has been
where verification requirements are particularly strict, and              shown to work. This suggests that current safeguards
provenance tracking and traceability mechanisms are also
                                                                          are best read as commonly recommended gover-
reported [WL20].
     Across evidence streams, both peer-reviewed and grey                 nance mechanisms rather than proven solutions. Ev-
sources consistently emphasize validation activities as the               idence strength is moderate (33 sources across both
primary safeguard mechanism. However, grey literature                     streams recommend safeguards and largely agree,
more frequently foregrounds behavioral guardrails such as
                                                                          but most are Tier 2 grey or propose safeguards rather
disciplined review practices, whereas peer-reviewed studies
tend to reference structured governance mechanisms such                   than evaluate their effectiveness).
as sandboxing or provenance tracking. The evidence base
is stronger in recommending safeguards than in evaluating            3.7. Usage Contexts and Constraints (RQ6)
their effectiveness. Validation pipelines and human review               The evidence suggests that vibe coding is most often
are frequently proposed, but their actual impact in real             discussed in prototyping and early-stage development, while
development settings remains under-tested.                           production use and operational constraints remain weakly
                                                                     evidenced. A total of 8 out of 47 sources contributed explicit
                                                                     evidence to RQ6 (2 peer-reviewed and 6 grey). This com-
                                                                     paratively low number indicates that many sources describe
                                                                     workflows and outcomes without systematically specifying
                                                                     contextual conditions or operational constraints.
                                                                         Table 26 summarizes reported usage contexts and
                                                                     constraints. Prototyping and early-stage development (6
                                                                     sources) is the most frequently reported context of use in
                                                                     this small evidence base and is primarily described in grey
                                                                     sources. Production use (2 sources; grey-only) appears less
                                                                     frequently and is typically framed with caution.
                                                                         Privacy-related constraints (2 sources; peer-reviewed
                                                                     only) are discussed in terms of data or code exposure risks




S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                   Page 22 of 35
                                                           Multivocal Review of Vibe Coding

Table 26                                                                      Table 27
RQ6: Usage contexts and operational constraints in vibe                       RQ7: Tools and platforms supporting vibe coding. Counts are
coding. Counts are reported out of the 8 sources contributing                 the number of sources referencing each coded tool category;
to RQ6; percentages are omitted because the contributing                      one source may contribute to multiple categories. ChatGPT
source count is small.                                                        includes OpenAI/GPT models and the agentic-frameworks cat-
 Code                                PaperID                         Count*   egory includes tools such as Devin and SWE-agent, following
 Use in prototyping or early-stage   [WL17], [GL1], [GL3], [GL10],     6      the codebook.
 development contexts                [GL11], [GL19]
 Use in production or operational    [GL10], [GL13]                    2       Tool / Platform (normalized)                  Academic   Grey   Total
 deployment contexts                                                           GitHub Copilot                                   17       9      26
 Privacy or data/code exposure       [WL17], [WL27]                    2       ChatGPT (incl. OpenAI/GPT models)                11       7      18
 constraints                                                                   Cursor                                            3       11     14
 Cost or usage-limit constraints     [WL17]                            1       Agentic frameworks (incl. Devin, SWE-agent)       6       4      10
       ∗ = one source may contribute to multiple categories                    Claude                                            3       4       7
                                                                               Evaluation tooling                               1         0      1


when interacting with external services. Cost-related con-
straints (1 source; peer-reviewed only) refer to usage limits                 and refine code,” distinguishing it from traditional IDEs
or operational expense considerations.                                        that “may offer AI as an auxiliary feature” [WL7]. Agent-
    Grey sources more frequently provide narrative accounts                   based and agent-framework tooling (10 sources; 6 peer-
of prototype versus production contexts, whereas peer-                        reviewed, 4 grey), including tools such as Devin and SWE-
reviewed studies that mention constraints tend to focus on                    agent, is referenced in both streams, typically in the context
privacy and cost considerations.                                              of multi-step or semi-autonomous workflows. Claude (7
    RQ6 draws disproportionately on grey literature (6 grey,                  sources; 3 peer-reviewed, 4 grey) and dedicated evaluation
2 peer-reviewed), with all grey sources at Tier 2. Because                    tooling (1 source) are less frequently mentioned. The tool
the peer-reviewed base is small, we do not claim cross-                       evidence suggests that vibe coding currently sits between
stream triangulation for context-level findings; instead, they                three tool traditions: general-purpose coding assistants, AI-
are reported as practitioner-situated observations whose                      native IDEs, and emerging agentic development environ-
generalizability should be tested in future empirical work.                   ments. These counts indicate visibility in the literature rather
This asymmetry is itself a substantive finding: production-                   than comparative effectiveness, since most sources mention
deployment and operational- constraint contexts remain em-                    tools without controlled evaluation.
pirically under-studied in the peer-reviewed stream.                              Across the reviewed sources, the tool ecosystem sup-
                                                                              porting vibe coding can be organized into four recurring
    Takeaway 9                                                                categories. First, no-code or low-code application builders
                                                                              allow users to specify desired functionality in natural lan-
    Vibe coding is most often discussed in prototyp-                          guage and generate applications with minimal direct pro-
    ing and early-stage development, while production                         gramming. Second, design-to-code tools translate design
    use and operational constraints remain weakly evi-                        artifacts (e.g., UI mockups) into executable interface code,
    denced. This indicates that current accounts describe                     supporting rapid UI prototyping and iteration. Third, AI-
                                                                              integrated development environments (AI IDEs) provide in-
    where the practice tends to start rather than how                         editor assistance for code generation, refactoring, and itera-
    it behaves under deployment conditions. Evidence                          tive improvement within conventional software engineering
    strength is weak: only 8 sources contribute, mostly                       workflows. Fourth, autonomous agentic systems aim to exe-
    Tier 2 grey literature, with little peer-reviewed cor-                    cute higher-level tasks with reduced human intervention by
                                                                              planning, implementing, and iteratively validating changes.
    roboration.                                                                   This categorization complements the RQ7 tool inventory
                                                                              by providing an ecosystem-level view of how tools differ
3.8. Tools and Platforms (RQ7)                                                in (i) the expected user expertise, (ii) the level of control
    Table 27 summarizes the tools and platforms referenced                    retained by the human, and (iii) the degree of automation.
across the reviewed sources. GitHub Copilot (26 sources;                      In the reviewed evidence base, AI IDEs and chat-based
17 peer-reviewed, 9 grey) is the most frequently referenced                   assistants are the most frequently referenced tool categories,
tool and appears in both evidence streams. Chat-based as-                     while agentic systems and no-code builders are discussed
sistants such as ChatGPT, including OpenAI/GPT models                         primarily in grey sources and with less systematic evalua-
(18 sources; 11 peer-reviewed, 7 grey), are also widely                       tion. Figure 10 summarizes this tool ecosystem and situates
discussed. Cursor (14 sources; 11 grey, 3 peer-reviewed) is                   representative platforms within these four categories.
referenced primarily in grey literature, often described as an                    Peer-reviewed studies more frequently reference widely
AI-native IDE environment. One peer-reviewed evaluation                       studied assistants such as Copilot, whereas grey sources
describes Cursor as an “AI-native integrated development                      more often describe AI-native IDEs and agent-oriented tool-
environment (IDE)” that “is designed to interpret Natu-                       ing.
ral Language Coding (NLC) prompts to generate, debug,

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                    Page 23 of 35
                                                   Multivocal Review of Vibe Coding




                       Figure 10: Tool ecosystem categories for vibe coding, with representative platforms.



    Takeaway 10                                                      rather than isolated generation tasks. These gaps relate to the
                                                                     productivity, quality, and reproducibility measures reviewed
    Copilot and chat-based assistants are the most vis-              in RQ4 (3.5). Context management limitations represent an-
    ible tools across both evidence streams. AI-native               other widely reported challenge, appearing in 30% (6) of the
    IDEs and agentic tools appear more prominently in                sources. These limitations relate to difficulties in handling
                                                                     long interaction histories, maintaining coherent state across
    grey literature but still lack strong peer-reviewed
                                                                     prompts, and preventing context drift during extended devel-
    evaluation. These patterns reflect visibility in the             opment sessions. They connect to the workflows described
    literature rather than demonstrated effectiveness. Ev-           in RQ2 (3.3) and to the session-level dynamics discussed in
    idence strength is moderate (39 sources reference                RQ3.2. For instance, [WL12] and [WL22] describe technical
                                                                     challenges associated with managing long prompt histories,
    tools, though largely as mentions rather than con-
                                                                     while [GL15] reports practical difficulties maintaining con-
    trolled evaluations).                                            sistent context across multi-step development interactions.
                                                                          Governance-related challenges are reported in 20% (4)
3.9. Open Challenges and Future Directions                           of the sources. As one source summarizes, “the limitations
                                                                     surrounding data privacy, code correctness, operational cost,
     (RQ8)
                                                                     and intellectual property demand robust governance frame-
    This section frames the reported challenges as directions
                                                                     works” [GL16]. These challenges concern organizational
for future research and connects each one to the earlier
                                                                     guardrails, disclosure requirements, and the integration of
research questions where the topic first appears. The most
                                                                     AI-assisted workflows into existing development processes.
frequently discussed challenge concerns security risks as-
                                                                     This mirrors the governance and guardrails discussed in
sociated with AI-generated code, appearing in 50% (10)
                                                                     RQ5.2 (3.6.2). Trust calibration and appropriate reliance
of the sources shown in Table 28. These risks include the
                                                                     are also reported as open challenges in 20% (4) of the
introduction of unsafe code, vulnerabilities, and potential
                                                                     sources. These studies highlight unresolved questions re-
misuse of generated artifacts. Peer-reviewed and practitioner
                                                                     garding when developers should trust AI-generated outputs
sources agree that generated code may contain weaknesses
                                                                     and how appropriate reliance can be achieved in practice. For
when developers rely on automated generation without rig-
                                                                     example, [WL6] discusses the difficulty of calibrating trust
orous verification ([WL6], [WL21], [GL12], [GL15]). This
                                                                     in systems that can produce both high-quality and erroneous
challenge builds on the risks and safeguards reported in RQ5
                                                                     outputs within the same workflow. This question connects to
(3.6).
                                                                     the shift in the developer role discussed in RQ3 (3.4).
    A similar proportion of studies (30%, 6 sources) high-
                                                                          Beyond explicitly reported challenges, certain areas ap-
lights gaps in evaluation and measurement practices. These
                                                                     pear underrepresented in extractable evidence. In particu-
sources emphasize the absence of standardized benchmarks
                                                                     lar, session-level interaction dynamics (RQ3.2) and repro-
capable of assessing realistic development workflows and
                                                                     ducibility concerns (RQ4) appear only in a small number
long-horizon tasks. For example, [WL3] calls for evaluation
                                                                     of studies, suggesting important opportunities for future
frameworks that capture multi-step development processes

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                     Page 24 of 35
                                                                        Multivocal Review of Vibe Coding

Table 28                                                                                  4.1. Vibe Coding as an Iterative Control System
RQ8: Open challenges and future research directions. Percent-                                 A central interpretive contribution of this review is to
ages are relative to the 20 sources contributing to RQ8.                                  frame vibe coding as an iterative control system: a feedback-
 Challenge                              PaperID                            Count*    %    driven development process in which the developer repeat-
 Security concerns including unsafe
 code, vulnerabilities, and misuse
                                        [WL6], [WL10], [WL16], [WL21],
                                        [WL28], [GL1], [GL12], [GL15],
                                                                             10     50%
                                                                                          edly specifies intent, evaluates AI-generated output, and
 risks                                  [GL16], [GL19]                                    refines the next prompt based on observed behavior. We use
 Context management limitations         [WL12], [WL13], [WL16], [WL22],      6      30%
                                        [GL13], [GL15]                                    the term control system conceptually rather than as a formal
 Lack of standardized evaluation
 frameworks      and     long-horizon
                                        [WL3], [WL5], [WL17], [GL1],
                                        [GL14], [GL15]
                                                                             6      30%
                                                                                          control-theoretic model; it highlights the role of feedback,
 benchmarks                                                                               monitoring, correction, and repeated adjustment in vibe
 Governance, disclosure, and organi-    [WL15], [GL1], [GL15], [GL16]        4      20%
 zational integration challenges                                                          coding workflows. This framing emerges consistently across
 Trust calibration and appropriate
 reliance challenges
                                        [WL3], [WL5], [WL6], [WL9]           4      20%
                                                                                          the research questions. The definitions synthesized in RQ1
         ∗ = one source may contribute to multiple categories                             converge on natural-language intent as the primary interface.
                                                                                          Evaluation pipelines (72%) and chat-based iteration loops
                                                                                          (63%) are the most frequently reported workflow patterns
empirical investigation. These challenges mirror the weaker                               in RQ2. The role shifts documented in RQ3 show develop-
areas identified in earlier RQs: session-level dynamics,                                  ers moving from direct code authoring toward supervision,
reproducibility, safeguard effectiveness, and long-horizon                                constraint-setting, and verification. The developer does not
evaluation. Overall, the open challenges suggest that vibe                                merely request code; the developer steers a generation–
coding research has moved faster in describing workflows                                  evaluation cycle.
and tools than in evaluating long-term outcomes, governance                                   This interpretation explains why evaluation activities
mechanisms, and context-sensitive adoption.                                               feature so prominently in the evidence base. Generated out-
                                                                                          puts are treated as provisional proposals that require inspec-
     Takeaway 11                                                                          tion, testing, or runtime validation before integration into a
     The open challenges suggest that vibe coding re-                                     working system. Many studies across both evidence streams
                                                                                          emphasize automated tests, linting, continuous integration
     search has so far described workflows and tools                                      checks, and manual code review as workflow components.
     more than it has evaluated their long-term effects.                                  Vibe coding does not remove verification work; it redis-
     Security risks, context management limitations, and                                  tributes it, shifting effort from writing code to reviewing and
     the absence of realistic evaluation frameworks are                                   validating generated outputs.
                                                                                              The control loop is described differently across evidence
     the most frequently reported open challenges, while                                  streams. Academic studies more often describe the process
     governance integration and trust calibration remain                                  as a structured workflow incorporating formal verification
     unresolved. Future work should prioritize security                                   mechanisms such as quality-assurance procedures, retrieval-
     evaluation, improved context management, realistic                                   based grounding, or automated test suites. Grey literature
                                                                                          tends to emphasize rapid iteration and exploratory prompt-
     long-horizon benchmarks, governance integration,                                     ing, with less formalized discussion of verification prac-
     trust calibration, and long-term empirical studies of                                tices. These differences shape the reported outcomes. The
     adoption. Evidence strength is moderate (20 con-                                     structured workflows described in peer-reviewed studies are
     tributing sources across a mix of peer-reviewed and                                  more frequently associated with quality and defect aware-
                                                                                          ness, whereas the rapid-iteration accounts in grey literature
     grey literature; security is the most consistently re-                               emphasize perceived productivity gains (cf. Section 3.5).
     ported challenge, while the other categories rest on                                     Prior reviews of vibe coding each adopt a narrower lens.
     thinner evidence).                                                                   Ray [14] centers on the tool landscape. Fawzy et al. [15]
                                                                                          center on practitioner experience drawn from grey literature.
                                                                                          Ge et al. [13] center on formal modeling of human–AI
                                                                                          collaboration. Each lens captures one facet of the process
4. Discussion                                                                             but does not connect them. What is new in this review is the
     This section integrates the findings across the research                             framing of vibe coding as a broader socio-technical control
questions. For each major theme it states the main finding,                               loop that spans intent, generation, validation, trust calibra-
relates it to previous work, notes what this review adds, and                             tion, and governance. This loop becomes visible only when
draws out what it means for researchers and practitioners.                                the peer-reviewed and grey evidence streams are synthesized
It then sets out the recurring tensions in the evidence base,                             together, since neither stream on its own reports every stage.
a conceptual framework that links the findings, and the                                       These findings indicate that the effectiveness of vibe
implications for practice and research.                                                   coding depends less on the speed of code generation than
                                                                                          on the rigor of the evaluation loop surrounding it. Faster
                                                                                          generation can accelerate early prototyping, but the sus-
                                                                                          tainability of those gains depends on the verification and


S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                          Page 25 of 35
                                                   Multivocal Review of Vibe Coding

governance mechanisms embedded in the workflow. When                 4.3. Conditional Outcomes and the Verification
the evaluation loop is systematic, with defined acceptance                Gap
criteria, automated testing, and structured prompt refine-                Across the reviewed sources, productivity improvements
ment, vibe coding functions as a productive feedback-driven          are among the most frequently reported outcomes of vibe
development process. When evaluation is superficial, with            coding workflows (RQ4). Many studies describe faster time-
limited review, unchecked outputs, and ad-hoc prompting,             to-prototype, reduced implementation effort for initial fea-
the same speed that enables rapid prototyping can also               tures, and accelerated iteration cycles. The synthesis indi-
introduce hallucinations, technical debt, and the cognitive          cates that such gains are highly conditional. They depend on
debt documented in RQ3.1. For researchers, the loop offers a         task characteristics, developer expertise, and the strength of
common structure for comparing studies. For practitioners,           verification practices embedded in the workflow.
adopting vibe coding without investing in evaluation infras-              Quality outcomes are therefore often framed as trade-
tructure may increase long-term maintenance risks, although          offs rather than consistent improvements. Rapid generation
longitudinal evidence on such effects remains limited.               and iteration can improve perceived development progress,
                                                                     particularly during early prototyping. Several sources note
4.2. Developer Role Shift and Cognitive Burden                       that such gains may come at the expense of long-term
    The synthesis suggests a shift in developer work from            maintainability when developers defer deeper understanding
direct code authoring toward specification, supervision, and         of generated artifacts. This pattern aligns with the cognitive
validation (RQ3). Across many sources, developers con-               debt phenomenon discussed in RQ3.1. A further observation
tribute primarily by framing constraints, providing contex-          concerns the limited attention to long-horizon outcomes.
tual information, selecting among generated alternatives,            Many reported benefits relate to short-term measures such as
and verifying outputs. This observation aligns with the fre-         task completion time or prototype creation speed. Outcomes
quent appearance of trust calibration and verification effort        such as maintainability, reproducibility, and defect accumu-
constructs in RQ3.1.                                                 lation are less frequently examined and often emerge only in
    The role shift is not uniformly beneficial. While AI as-         longer development cycles.
sistance may reduce implementation effort in some tasks, it               Findings from RQ5 indicate that the central risk asso-
can increase cognitive load through prompt refinement, con-          ciated with vibe coding is a verification gap: a mismatch
text repair, and systematic verification of uncertain outputs.       between the speed at which AI-assisted workflows can gen-
These dynamics are reflected in the cognitive debt themes            erate code and the practical capacity of developers and
identified in the synthesis. Deferring detailed understanding        processes to verify correctness, security, and provenance.
during rapid iteration may raise downstream debugging or             Within RQ5.1, this gap appears in recurring failure modes
maintenance costs when generated artifacts are accepted              such as incorrect or hallucinated outputs, context drift across
with limited inspection.                                             multi-turn interactions, and workflow practices where gener-
    Studies of AI-assisted programming and human-AI col-             ated changes are integrated with limited review. Correspond-
laboration report related effects. Controlled evaluations of         ingly, RQ5.2 shows that safeguards across both evidence
GitHub Copilot record productivity gains [5], while other            streams emphasize validation mechanisms and human-in-
work frames the same assistant as both an asset and a                the-loop review as the primary controls for reducing risk. At
liability [22]. A parallel line of work describes the model          present, the empirical basis for evaluating safeguard effec-
as a conversational assistant to the programmer [2, 7], and          tiveness remains limited. Many safeguards are presented as
broader accounts examine how teams navigate generative-              recommended practices rather than evaluated interventions.
AI adoption [1]. What appears specific to vibe coding is             The evidence base is therefore stronger in identifying risks
the degree of the shift. The developer is not only using AI          than in quantifying which mitigation strategies are most
as a coding assistant but increasingly acts as a supervisor,         effective under realistic development conditions.
validator, and prompt-based controller of the development                 These outcomes echo earlier evidence on AI-assisted
process. The unit of work moves from the line of code toward         programming. Controlled studies report measurable produc-
the specification and the acceptance decision.                       tivity gains from Copilot [5], while other work raises ro-
    For practitioners, this reframing suggests that skill in         bustness and quality concerns about generated code [6, 22].
verification, constraint specification, and review may matter        Fawzy et al. [15] report a related speed–quality trade-off in
as much as authoring skill. For researchers, the weakest             grey literature. What is new here is the link between these
area of evidence concerns session-level interaction dynam-           conditional outcomes and the strength of the evaluation loop
ics (RQ3.2), including momentum shifts, context drift, and           introduced in Section 4.1. Rather than treating productivity
repeated prompting cycles. Although such phenomena are               and quality as separate results, this review reframes the core
frequently mentioned in practitioner narratives, they are            problem as a single verification gap that runs across both
rarely operationalized or measured in empirical studies. This        evidence streams. The conditions under which productivity
gap points to an opportunity for future research examining           gains hold are, in large part, the conditions under which the
full-session interaction traces and long-horizon workflows           verification gap is closed.
rather than isolated task outcomes.                                       For practitioners, this suggests that reported productivity
                                                                     benefits are most credible when code generation is coupled

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                      Page 26 of 35
                                                   Multivocal Review of Vibe Coding

with systematic review, and that verification effort should          as a research agenda, the review suggests where empirical
scale with the intended use of the artifact. For researchers,        effort would be most useful next. The main open direction
the priority is causal evidence. Controlled and field stud-          concerns the evaluation loop that sits at the center of vibe
ies that compare alternative verification and governance             coding. The review can describe this loop and its failure
mechanisms in end-to-end development workflows would                 modes, but it cannot yet say which parts of it most affect
strengthen guidance on which safeguards actually narrow the          outcomes, because the underlying phenomena are rarely
gap.                                                                 measured.
                                                                         This gap connects to the future directions already noted
4.4. Contexts, Tools, and Adoption Boundaries                        in prior reviews. Ray [14] enumerates a broad set of chal-
     The mapping of task domains and usage contexts indi-            lenge categories and future research directions but does
cates that vibe coding is adopted unevenly across settings.          so from a non-systematic base, so the directions are not
The domain evidence (RQ3.3) suggests that certain domains            weighted by evidence quality. Fawzy et al. [15] document
are more favorable for AI-assisted workflows than others. UI         a speed–quality trade-off from grey literature alone, which
and front-end prototyping contexts appear frequently in the          leaves the peer-reviewed and long-horizon side of that trade-
literature and are often associated with positive productiv-         off open. What this review adds is a cross-stream view
ity outcomes. Domains involving complex data pipelines,              that shows where the two evidence streams agree, where
machine learning infrastructure, or tightly coupled system           they diverge, and which questions neither stream currently
logic appear less frequently and are more commonly as-               answers.
sociated with correctness and verification challenges. The               Building on this, several priorities emerge for re-
usage-context evidence (RQ6) points in the same direction.           searchers. First, session-level interaction dynamics (RQ3.2),
Reported use concentrates on prototyping and exploratory             such as momentum shifts, context drift, and repeated
development, while production deployment is discussed                prompting cycles, are frequently described in practitioner
cautiously and rarely evidenced. Factors such as privacy and         narratives but seldom operationalized. Studies that capture
cost constraints further shape where and how workflows are           full-session interaction traces, rather than isolated task out-
adopted.                                                             comes, would allow these dynamics to be measured. Sec-
     The tool evidence (RQ7) shows that supporting tools             ond, safeguards are widely recommended (RQ5.2) but rarely
moderate workflow behavior. Different assistant paradigms,           evaluated. Controlled and field studies comparing alternative
including inline completion systems, chat-based assistants,          verification and governance mechanisms would show which
and agent-oriented development environments, support dif-            safeguards reduce risk under realistic conditions, rather
ferent capabilities for context management, automation, and          than which are merely advised. Third, the evidence base
verification. Across the corpus these tools group into a small       is domain-skewed, with stronger coverage of prototyping
number of ecosystem categories, which differ in how much             and UI tasks than of data-intensive or safety-critical systems
of the loop they automate and how much verification they             (RQ3.3, RQ6); studies in the under-represented domains
expose to the developer.                                             would test how far current findings generalize. Fourth,
     Ray [14] provides the most detailed prior taxonomy of           clearer operational definitions of vibe coding (RQ1) would
this tool landscape. This review builds on that description          support comparability across studies. Finally, long-horizon
but situates tools and contexts differently. Rather than cata-       outcomes such as maintainability, reproducibility, and defect
loging them as a standalone landscape, it treats them as mod-        accumulation (RQ4) are under-studied relative to short-term
erators of the whole control loop set out in Section 4.1. Read       measures like task completion time, and longer development
this way, the evidence marks clear adoption boundaries.              cycles would be needed to observe them.
Coverage concentrates on prototyping and UI or front-end
work, whereas production, data-intensive, and safety-critical        4.6. Tensions in the Evidence Base
use remain thin. Tool choice and usage context appear to                 Beyond the individual findings, the review suggests five
condition where along that boundary a given workflow sits.           recurring tensions that run across the research questions:
     These patterns are early indications rather than settled
conclusions, since the RQ6 base is small (8 sources). For               • Productivity is the most frequently reported outcome
practitioners, the practical reading is to match tool and con-            (21 sources, RQ4), yet maintainability concerns (11
text to the maturity of the surrounding verification practices,           sources) and the cognitive-debt phenomenon (RQ3.1)
and to treat production and data-intensive use as areas need-             suggest that speed gains may come at the cost of long-
ing stronger safeguards. For researchers, the concentration of            term maintainability when understanding is deferred.
evidence marks where the field is thin. Studies of production,          • Vibe coding is widely framed as lowering entry bar-
data-intensive, and safety-critical settings would help estab-            riers for novices (RQ3.3), but the same reduced-
lish whether the favorable prototyping results extend beyond              oversight mode may increase the risk of overtrust
the contexts in which they were first reported.                           in incorrect or hallucinated output (RQ3.1, RQ5.1),
                                                                          which novice users may be least equipped to detect.
4.5. Open Challenges and Research Agenda
   The findings point less to a settled body of knowledge               • Agentic or semi-autonomous framings (RQ1) point
and more to an early evidence base with clear gaps. Read                  toward delegation, whereas the safeguards reported

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                     Page 27 of 35
                                                   Multivocal Review of Vibe Coding

      most often, such as human-in-the-loop review and val-          How the layers interact The value of the framework
      idation pipelines (RQ5.2), point back toward human             lies in how these layers act on one another rather than in
      control. A workable balance appears to lie between the         the layers taken separately. How the workflow is designed
      two.                                                           appears to affect developer cognitive load, since the choice
                                                                     of interaction pattern in the workflow layer (RQ2) shapes
    • Reported use concentrates on prototyping and early-            how much prompt refinement, context repair, and verifica-
      stage development (RQ6), while production deploy-              tion the developer must carry in the role and experience
      ment is discussed cautiously and rarely evidenced,             layer (RQ3). Developer validation in turn appears to affect
      which suggests that the move from prototype to pro-            outcomes, because how closely the developer supervises and
      duction remains underexplored.                                 validates the loop (RQ3) influences the productivity and
    • Explicit context provisioning is a frequently reported         quality results recorded in the outcome layer (RQ4). Weak
      workflow tactic (RQ2), yet context-window and state-           evaluation appears to increase risk, in that limited review
      retention failures and iteration drift (RQ3.2, RQ5.1)          and superficial verification in the workflow and role layers
      suggest that the same multi-turn interaction that sup-         raise the likelihood of the failure modes cataloged in the risk
      plies context can also degrade it.                             and governance layer (RQ5). The two moderators sit across
                                                                     this chain rather than within it: the tool ecosystem (RQ7)
    These tensions appear to follow from the iterative-              and the development context and users (RQ6) moderate
control-system framing (Section 4.1): each arises where the          the whole process, so that the same workflow can produce
speed of generation can outpace the rigor of the surrounding         different cognitive load, outcomes, and risk depending on
evaluation loop. Each also relates to two or more layers of          the assistant paradigm in use and the domain, expertise, and
the conceptual framework described next.                             constraints of the setting.
                                                                         Two moderating dimensions therefore shape the rela-
4.7. Conceptual Framework                                            tionships among the layers rather than adding to them.
    To integrate the findings across the research questions,
we propose a conceptual framework comprising two com-                Context and users (RQ6) The effectiveness of vibe cod-
plementary views, presented together in Figure 4. Figure 4a          ing workflows depends strongly on development context and
presents the process view: the iterative intent–generation–          user characteristics. Factors such as developer expertise,
evaluation–refinement loop that characterizes vibe coding            organizational setting, domain characteristics, and privacy
as an interaction pattern (Section 4.1). Figure 4b presents          or cost constraints influence how workflows are adopted and
the structural view: a multi-layered model that decomposes           what outcomes emerge.
the phenomenon into four interconnected layers (workflow,
role and experience, outcomes, and risk and governance)
                                                                     Tool ecosystem (RQ7) The design of supporting tools also
                                                                     moderates workflow behavior. Different assistant paradigms,
moderated by context and tooling. Together, the two views
                                                                     such as inline completion systems, chat-based assistants, and
capture both the temporal dynamics of a single develop-
                                                                     agent-oriented development environments, support different
ment session and the cross-cutting dimensions that shape
                                                                     capabilities for context management, automation, and veri-
its outcomes. Two further threads connect the framework
                                                                     fication.
to the research questions that are not represented as layers.
                                                                         Taken together, the framework conceptualizes vibe cod-
The intent-specification step that begins each loop relates to
                                                                     ing as a socio-technical system in which interaction work-
the definitional findings of RQ1 and the workflow tactics of
                                                                     flows, developer cognition, development outcomes, and gov-
RQ2. Trust calibration and cognitive load, which influence
                                                                     ernance mechanisms are closely interrelated, and in which
how closely the loop is supervised, relate to RQ3.
                                                                     the strength of the links between them, not the layers in
    The four layers are best read not as a static stack but as a
                                                                     isolation, determines what the process produces.
chain of directional relationships. The workflow layer (RQ2)
captures the interaction patterns underlying vibe coding,
                                                                     4.8. Implications for Practice and Research
such as conversational development loops, prompt–patch
                                                                         From a practitioner perspective, the synthesis indicates
cycles, context provisioning, retrieval grounding, and evalu-
                                                                     that vibe coding should be treated as an engineering work-
ation pipelines. The role and experience layer (RQ3) reflects
                                                                     flow requiring explicit evaluation practices. Reported pro-
how these workflows reshape developer work, through trust
                                                                     ductivity benefits are most credible when code generation is
calibration, shifts from authoring to supervision, changes
                                                                     coupled with systematic review. Organizations adopting vibe
in cognitive load, and phenomena such as cognitive debt.
                                                                     coding should therefore incorporate verification routines
The outcome layer (RQ4) represents development outcomes,
                                                                     such as automated testing and structured code review, partic-
including productivity gains and quality dimensions such
                                                                     ularly when generated artifacts are intended for production
as defects, maintainability, and reproducibility. The risk
                                                                     use.
and governance layer (RQ5) captures failure modes such as
                                                                         More concretely, the synthesis points to several practices
hallucinations, context drift, and insufficient review, together
                                                                     that teams adopting vibe coding may consider:
with safeguards such as testing pipelines, human-in-the-loop
validation, sandboxing, and provenance tracking.

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                     Page 28 of 35
                                                   Multivocal Review of Vibe Coding

    • Using vibe coding mainly for prototyping and ex-               be fully addressed retrospectively, and future updates to this
      ploratory work, unless validation practices are strong         review should expand the search string.
      (RQ4, RQ6);                                                        Reproducibility of the search is also threatened by
                                                                     volatility in web search results and platform ranking
    • Running automated tests before accepting generated             changes, particularly for grey literature sources retrieved via
      code, and treating passing tests as an acceptance cri-         Google and YouTube. We mitigate this risk by documenting
      terion (RQ5.2);                                                the search date (October 2025), the search channels, and the
    • Reviewing generated code before committing it, rather          selection procedures. Re-executing the search at a later time
      than integrating unread output (RQ5.1, RQ5.2);                 may still yield a different candidate set, a known limitation
                                                                     of multivocal literature reviews [16].
    • Documenting the prompts, assumptions, and tool or
      model versions behind retained artifacts, to support           5.2. Study selection
      later maintenance and reproducibility (RQ4, RQ8);                  Study selection involves subjective judgment, particu-
                                                                     larly for grey literature. Inclusion decisions may reflect judg-
    • Sandboxing execution when generated code interacts             ments about credibility and technical substance. To mitigate
      with files, external APIs, or deployment environments          this risk, we applied explicit inclusion and exclusion criteria
      (RQ5.2).                                                       for peer-reviewed studies (Table 3), used a staged screening
                                                                     process with recorded counts, and assessed grey sources
    The findings also highlight the importance of context            using a structured credibility checklist (Table 9) [16]. Some
management. Many workflow breakdowns arise from miss-                degree of subjectivity remains inherent to credibility assess-
ing constraints or degraded context across multi-turn inter-         ment in grey literature.
actions. Teams may therefore benefit from explicitly doc-
umenting requirements and constraints, providing relevant            5.3. Data extraction
artifacts to the model, and using retrieval or grounding                 Data extraction may introduce error or bias in how
mechanisms where available.                                          evidence is recorded. To reduce this risk, we used a struc-
    From a research perspective, the same synthesis leaves           tured extraction template aligned with RQ1–RQ8 (Table 11)
several questions open rather than settled. The priorities are       and retained supporting excerpts, preserving traceability by
set out as a forward-looking agenda in Section 3.9, which            linking synthesized claims to Paper_IDs and their source
covers session-level dynamics, safeguard effectiveness, do-          identifiers. This record supports auditability of how each
main coverage, operational definitions, and long-horizon             finding was derived. Some interpretive variability may still
outcomes. Rather than repeat them here, we note that each            affect how evidence was extracted.
follows from the same pattern seen throughout the review:
the evidence base is stronger at describing vibe coding than         5.4. Coding and theme classification
at measuring which parts of the evaluation loop most affect              Assigning codes and defining themes involves interpre-
its outcomes. The main research implication is therefore             tive judgment. The first author performed the main review
that vibe coding should be studied as an end-to-end socio-           steps, while senior researchers reviewed a sample of the
technical workflow rather than as isolated prompt-based              screening and selection decisions, the quality and credibility
code generation. Future empirical studies should measure             scores, and the coding outputs and final themes, and resolved
not only output correctness or productivity, but also verifica-      disagreements through discussion. We did not carry out
tion effort, context management, trust calibration, and long-        formal independent double coding with an inter-rater agree-
term maintainability. This would help explain which parts of         ment measure. To reduce the effect of this, we maintained
the evaluation loop most strongly influence outcomes.                a documented codebook (56 codes with definitions and
                                                                     keywords, provided in the supplementary material) in which
5. Threats to validity                                               each code is linked to one research question, and preserved
                                                                     traceability from each finding to its source identifiers and
    This section discusses limitations and threats to valid-         excerpts. These practices support auditability and reduce
ity relevant to this MLR, following established guidance             ambiguity in how evidence was interpreted, though some
for software engineering secondary studies [17] and MLR              interpretive subjectivity remains inherent to qualitative cod-
methodology [16].                                                    ing.
5.1. Study search                                                    5.5. Synthesis
    The search string may not capture all relevant work. The             Synthesis across heterogeneous evidence involves inter-
Boolean query combined vibe-coding-specific terms with a             pretive decisions and limits quantitative aggregation. Re-
limited set of software-development terms and deliberately           ported outcomes are measured using diverse methods such
excluded broader AI/LLM programming terms, as docu-                  as controlled experiments, surveys, practitioner reports, and
mented in Section 2.2.1. This scoping improves precision             prescriptive guidance, which increases the risk of overinter-
but reduces recall, so relevant work that uses only broader          preting simple vote-counting across studies. To address this
terminology may have been missed. This limitation cannot             risk, the review relies on descriptive mapping and thematic

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                      Page 29 of 35
                                                   Multivocal Review of Vibe Coding

synthesis rather than statistical meta-analysis. Interpretive        or measured across primary sources and may therefore be
variability may still influence theme boundaries, particu-           interpreted differently. To reduce this risk, we reported areas
larly for constructs that are not consistently operationalized       where evidence was sparse or conceptually heterogeneous
across studies. Another research team may therefore derive           (e.g., session-level dynamics in RQ3.2).
somewhat different themes from the same corpus, although
our documented codebook and traceability records support             5.8. Conclusion validity
comparable interpretation.                                               Conclusion validity concerns whether outcome-related
                                                                     claims are well supported. Outcomes reported in RQ4, in-
5.6. External validity                                               cluding productivity, quality, and maintainability, rest on
    External validity concerns the generalizability of the           heterogeneous evidence, so we interpret outcome claims
findings beyond the analyzed sources. The included studies           cautiously by considering the evidence stream and consis-
are concentrated within a recent time window (primarily              tency across sources. Therefore, the reported counts and
2025) and frequently discuss a limited set of widely used            percentages should be interpreted as the frequency with
tools and development environments. As a result, findings            which concepts appear in the reviewed sources, not as esti-
may not generalize to future model versions, alternative tool        mates of their real-world prevalence, effect size, or practical
ecosystems, or less-represented development contexts such            impact. Publication and availability biases are additional
as safety-critical or highly regulated domains. The evidence         threats, since both peer-reviewed and grey literature may
base is also domain-skewed: UI and front-end prototyping             favor positive or novel findings while negative or unsuc-
tasks appear frequently in the literature, whereas data engi-        cessful experiences may be underreported. Grey literature
neering and machine learning workflows are comparatively             in particular may be promotional, anecdotal, or tool-driven,
underrepresented. A related temporal validity threat arises          which may overrepresent positive or early-adopter experi-
from the rapid evolution of large language model capabili-           ences. Although the use of multiple databases, grey litera-
ties, context limits, agentic toolchains, and IDE integrations.      ture channels, and snowballing reduces the risk of missing
Conclusions derived from the October 2025 evidence snap-             relevant studies, complete coverage cannot be guaranteed.
shot may therefore become partially outdated as new tools
and interaction patterns emerge. To mitigate this risk, the
                                                                     6. Related Work
review emphasizes transparency and reproducibility by pro-
viding structured extraction artifacts and by distinguishing              Three prior review studies address aspects of vibe cod-
peer-reviewed evidence from grey literature claims.                  ing, each with a distinct scope and methodology. This section
    Corpus size is a related concern. This MLR includes 47           sets out what each one covers and what it leaves open, and
sources and is therefore narrower than broader narrative re-         positions the present MLR against them.
views of AI-assisted software development. This difference                Ge et al. [13] give a formal, infrastructure-oriented treat-
reflects the focused scope and systematic selection protocol         ment of vibe coding. They model the practice as a Con-
of the review. The low snowballing yield (2 peer-reviewed            strained Markov Decision Process (CMDP) over a human–
and 3 grey additions) may also reflect the nascent and               project–agent triad, and they derive five development mod-
sparsely interconnected state of the vibe coding literature.         els: Unconstrained Automation (UAM), Iterative Conver-
Nevertheless, we cannot rule out that relevant studies were          sational Collaboration (ICCM), Planning-Driven (PDM),
missed, particularly grey-literature sources that may not be         Test-Driven (TDM), and Context-Enhanced (CEM). The
indexed by our search channels. Future updates should re-            review is technical and heavy on system detail. It covers
execute and expand the search protocol.                              code LLMs, agent architectures, execution environments,
                                                                     and feedback mechanisms in depth. It describes itself as the
5.7. Construct validity                                              first comprehensive and systematic review of the topic and
    Construct validity concerns whether the concepts stud-           reports drawing on over 1,000 papers. However, it docu-
ied are well defined. “Vibe coding” is a recent practitioner-        ments no search string, no inclusion or exclusion criteria, no
driven term whose meaning varies across sources. Some                quality appraisal, and no replication package, Based on the
studies describe it as intent-driven prompt programming,             information reported, however, its search and selection pro-
others emphasize agentic development environments, and               cess is not sufficiently documented to support independent
some use it broadly to refer to AI-assisted development.             reproduction in the sense expected of systematic secondary
This variation introduces a risk of construct drift when syn-        studies. It also does not incorporate grey literature under
thesizing heterogeneous evidence. To mitigate this risk, the         an appraisal protocol. Compared with this MLR, it gives
search strategy included related terminology (e.g., prompt-          limited structured attention to empirical outcomes such as
based development, conversational programming, and AI-               productivity, quality, defects, and maintainability. It also
assisted development), definitions and conceptual framings           gives limited attention to usage contexts, practitioner expe-
were coded under RQ1, and peer-reviewed and grey liter-              rience, and evidence-weighted developer human factors.
ature streams were analyzed separately during parts of the                Ray [14] offers the broadest narrative survey, drawing
synthesis. A related threat concerns the operationalization of       on around 245 references. It maps over twenty tools across
socio-technical constructs such as trust calibration, cognitive      five categories: browser-based environments, IDEs and ed-
load, and cognitive debt, which are not consistently defined         itors, plugins and extensions, command-line agents, and

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                       Page 30 of 35
                                                   Multivocal Review of Vibe Coding

task-management systems. It also proposes a taxonomy of              Table 29
four interaction modalities, namely full delegation, guided          Comparison of this MLR with existing vibe coding reviews.
delegation, active pairing, and expert consultation, placed on       The top two rows summarize corpus size and review type; the
a delegation–pairing continuum. It identifies twelve critical        remaining rows summarize per-area coverage. ✓ = addressed
challenges and proposes fourteen concrete research direc-            substantively; △ = partially addressed or addressed only narra-
tions. Its main strengths are the coverage of the tool ecosys-       tively; × = not addressed. “Undocumented” = no documented
tem and of definitions. However, it documents no systematic          systematic selection process: Ge et al. cites approximately
                                                                     1,000 references and Ray approximately 245, but these counts
protocol. There is no search string, no inclusion or exclusion
                                                                     are not the product of a documented selection protocol.
criteria, no quality appraisal, and no replication package, so
its conclusions are difficult to reproduce independently. It         Contributions / Themes
                                                                     Number of selected studies
                                                                                                           Ge et al. [13]   Ray [14]
                                                                                                           Undocumented Undocumented
                                                                                                                                       Fawzy et al. [15] Our MLR
                                                                                                                                            101           47
also blends peer-reviewed and grey sources without credi-            Review type                                NR            NR            GLR          MLR

bility weighting. Compared with this MLR, it gives limited           Conceptualization of vibe coding
                                                                     (Section 3.2)
                                                                                                                △             △              △             ✓

structured attention to developer role and cognitive aspects,        Workflow patterns and tactics               ✓             ✓             ✓             ✓

and it does not offer a synthesis of empirical outcomes.
                                                                     (Section 3.3)
                                                                     Developer role shift; cognitive and         ×             ×             △             ✓
     Fawzy et al. [15] conduct a systematic Grey Literature          behavioral aspects (Section 3.4)

Review (GLR) of vibe coding. They analyze 101 practitioner
                                                                     Reported outcomes: productivity,            ×            △              ✓             ✓
                                                                     quality, defects, maintainability,
sources against a 0–15 credibility rubric and extract 518            reproducibility (Section 3.5)
                                                                     Failure modes (Section 3.6.1)              △             △              △             ✓
firsthand behavioral units through thematic analysis. A repli-       Safeguards and governance (Sec-            △             △              △             ✓
cation package is publicly archived. Their findings report a         tion 3.6.2)
                                                                     Usage contexts and operational              ×            △              △             ✓
speed–quality trade-off: 62% of practitioners are motivated          constraints (Section 3.7)

by speed, 68% perceive the resulting code as fast but flawed,        Tool ecosystem and platform tax-
                                                                     onomy (Section 3.8)
                                                                                                                 ×             ✓             ×             ✓


and 36% skip quality assurance. The review covers motiva-            Open challenges and future re-             △              ✓             △             ✓
                                                                     search directions (Section 3.9)
tions, lived experience, quality-assurance perceptions, and
the speed–quality trade-off. Compared with this MLR, it is
scoped to practitioner grey literature and includes no peer-              Table 29 provides an at-a-glance view that summarizes
reviewed technical evidence. It performs no cross-stream             corpus size, review type, and the substantive contribution
integration, does not provide a dedicated tool taxonomy              areas each review delivers. Coverage of each content area is
comparable to Ray’s or the present MLR, and offers no                denoted as ✓ (the area is addressed substantively), △ (the
formal risk, safeguard, or governance analysis. Its outcome          area is addressed only partially, narratively, or in passing), or
measurement is narrow and based on perceptions, and it               × (the area is not addressed). Each substantive row is linked
treats developer-role change only narratively. It is organized       to the section of this paper that documents the corresponding
around four research questions, whereas this MLR addresses           finding so the reader can verify the classification. The labels
eight.                                                               in the Review type row use the conventions: NR = Narrative
     Across these three reviews, the differences cluster along       Review, GLR = Grey Literature Review, MLR = Multivocal
a few dimensions. In methodology, Ge et al. provide formal           Literature Review.
modeling but document no systematic search, selection, or                 Table 29 surfaces three patterns. First, the two upper
quality-appraisal procedure; Ray covers a broad range of             rows make the corpus and methodology asymmetry visible
topics but is likewise non-systematic; and Fawzy et al. apply        at a glance: this MLR is the only review among those
a documented protocol, though only to grey literature. The           compared here whose corpus results from a documented
reviews also differ in evidence sources. Ge et al. draw on           systematic selection process applied to both peer-reviewed
peer-reviewed work, Fawzy et al. on grey literature, and Ray         and grey literature. Second, among substantive content ar-
on a mix that is not systematically selected. These choices          eas, workflow patterns and tactics is the only area substan-
affect reproducibility, among the three reviews, Fawzy et al.        tively addressed across all four reviews, and it is the most-
provide the clearest documented protocol and public replica-         covered dimension of the existing vibe coding literature.
tion package. In terms of focus, prior work centers on tools         Third, developer role shift and cognitive/behavioral aspects
and definitions (Ray), practitioner experience (Fawzy et al.),       is the least-covered area among prior work: Ge et al. and Ray
or human–AI collaboration and formal modeling (Ge et al.).           do not address it, and only Fawzy et al. touches it through
None of the three combines peer-reviewed and grey liter-             practitioner accounts. Taken together, the table indicates that
ature under one documented protocol. To the best of our              no prior review substantively covers the full set of areas
knowledge, this MLR is one of the first dedicated syntheses          this MLR synthesizes, which motivates the cross-stream
to address that gap. It integrates both evidence streams under       integration adopted here.
a single protocol with a documented search string, inclusion
and exclusion criteria, quality and grey-credibility tiers, and
a replication package, and it applies this protocol across
eight research questions so that findings can be weighted by
evidence quality.



S.Siddeeq et al.: Preprint submitted to Elsevier                                                                                             Page 31 of 35
                                                   Multivocal Review of Vibe Coding

7. Conclusion                                                        Data availability
    This paper synthesized the emerging evidence on vibe                To support replication, we released a replication package
coding through a MLR of 47 sources, including 28 peer-               and the package is publicly available [23].
reviewed and 19 grey-literature sources. The central mes-
sage of the review is that vibe coding is not only prompt-
based code generation. It is an intent-driven and iterative          Declaration of AI Assistance
development workflow, and its reported productivity gains                During the preparation of this manuscript, the authors
depend on evaluation, validation, and governance rather than         used ChatGPT to assist with grammar refinement, sentence
on generation speed alone.                                           restructuring, and formatting improvements. Following the
    The synthesis supports this interpretation across the            use of this tool, the authors carefully reviewed and revised
eight research questions. Vibe coding is most consis-                the content and assume full responsibility for the final ver-
tently described as an intent-driven and iterative mode in           sion of the publication.
which natural language steers software creation through
generation–evaluation–revision loops (RQ1–RQ2). Devel-
oper work shifts from direct code authoring towards specifi-
                                                                     Selected Peer-Reviewed Literature
cation, supervision, and validation (RQ3). Productivity and        [WL1] Young, M., Nan, Z., & Shen, X. (2022, May).
time-to-prototype improvements are frequently reported,                  IDE augmented with human-learning inspired nat-
particularly in prototyping and UI development contexts,                 ural language programming. In Proceedings of the
while evidence on long-term quality, maintainability, and                ACM/IEEE 44th International Conference on Soft-
reproducibility remains limited (RQ4). The literature also               ware Engineering: Companion Proceedings (pp. 110-
highlights risks related to incorrect generations, context               114).
errors, and governance gaps. Commonly recommended safe-
                                                                   [WL2] Yang, S., & Yang, Y. (2024, May). FormalEval: A
guards include validation pipelines and human-in-the-loop
                                                                         method for automatic evaluation of code generation
review, although empirical evaluations of safeguard effec-
                                                                         via large language models. In 2024 2nd Interna-
tiveness remain scarce (RQ5). Evidence is strongest for pro-
                                                                         tional Symposium of Electronics Design Automation
totyping and UI contexts, while production, data-intensive,
                                                                         (ISEDA) (pp. 660-665). IEEE.
and safety-critical settings remain weakly examined (RQ6).
The tooling landscape is active, but visibility of a tool does     [WL3] Wang, J., & Chen, Y. (2023, November). A review on
not imply demonstrated effectiveness, because comparative                code generation with LLMs: Application and evalua-
evaluations are still sparse (RQ7).                                      tion. In 2023 IEEE International Conference on Med-
    For practitioners, this indicates that vibe coding should            ical Artificial Intelligence (MedAI) (pp. 284-289).
not be treated as a speed-focused coding shortcut. It should             IEEE.
instead be treated as an engineering workflow that requires
testing, review, validation, context management, and gover-        [WL4] Liang, J. T., Yang, C., & Myers, B. A. (2024). A large-
nance.                                                                   scale survey on the usability of AI programming assis-
    To the best of our knowledge, this is the first dedicated            tants: Successes and challenges. In 2024 IEEE/ACM
MLR that integrates peer-reviewed and grey literature on                 46th International Conference on Software Engineer-
vibe coding under a single documented protocol. The re-                  ing (ICSE). IEEE Computer Society, Los Alamitos,
view spans eight research questions covering definitions,                CA, USA, 605-617.
workflows, human factors, outcomes, risks and safeguards,
                                                                   [WL5] Sabouri, S., Eibl, P., Zhou, X., Ziyadi, M., Med-
usage context, tool ecosystems, and open challenges. It offers
                                                                         vidovic, N., Lindemann, L., & Chattopadhyay, S.
one of the first dedicated syntheses of governance and the
                                                                         (2025, March). Trust dynamics in AI-assisted de-
developer role shift in vibe coding, and it proposes a research
                                                                         velopment: Definitions, factors, and implications. In
agenda grounded in the evidence gaps found in the review.
                                                                         2025 IEEE/ACM 47th International Conference on
Future work should follow from these gaps. Future work
                                                                         Software Engineering (ICSE) (pp. 736-736). IEEE
should examine session-level workflow dynamics, directly
                                                                         Computer Society.
evaluate safeguard mechanisms, address the domain-skewed
evidence base, develop clearer operational definitions to          [WL6] Ramler, R., Moser, M., Fischer, L., Nissl, M., &
support comparability, and study long-term maintainability,              Heinzl, R. (2024, April). Industrial experience re-
where current evidence remains limited.                                  port on AI-assisted coding in professional software
                                                                         development. In Proceedings of the 1st International
Acknowledgment                                                           Workshop on Large Language Models for Code (pp.
                                                                         1-7).
    This work has been supported by FAST, the Finnish
Software Engineering Doctoral Research Network, funded             [WL7] Kumar, Y., Akinwunmi, I., & Kruger, D. (2025,
by the Ministry of Education and Culture, Finland.                       March). Evaluating the Advantage of an AI-Native
                                                                         IDE Cursor on Programmer Performance. In 2025

S.Siddeeq et al.: Preprint submitted to Elsevier                                                                    Page 32 of 35
                                                     Multivocal Review of Vibe Coding

         IEEE Integrated STEM Education Conference (ISEC)                    SIGSAC Conference on Computer and Communica-
         (pp. 1-8). IEEE.                                                    tions Security (pp. 2726-2740).
 [WL8] Treude, C., & Gerosa, M. A. (2025, April). How [WL17] Donato, B., Mariani, L., Micucci, D., Riganelli, O., &
       developers interact with AI: A taxonomy of human-     Somaschini, M. (2025, June). Multimind: A plug-in
       AI collaboration in software engineering. In 2025     for the implementation of development tasks aided by
       IEEE/ACM Second International Conference on AI        ai assistants. In Proceedings of the 33rd ACM Inter-
       Foundation Models and Software Engineering (Forge)    national Conference on the Foundations of Software
       (pp. 236-240). IEEE.                                  Engineering (pp. 1310-1317).
 [WL9] Jalil, S. (2025, August). The transformative influence [WL18] Johnson, B., Bird, C., Ford, D., Al Haque, E., Fors-
       of LLMs on software development & developer pro-              gren, N., & Zimmermann, T (2025, October). Fa-
       ductivity. In 2025 International Conference on Artifi-        cilitating Trust in AI-assisted Software Tools. ACM
       cial Intelligence, Computer, Data Sciences and Appli-         Transactions on Software Engineering and Methodol-
       cations (ACDSA) (pp. 1-10). IEEE.                             ogy.
[WL10] Majdinasab, V., Bishop, M. J., Rasheed, S., Moradi- [WL19] Flores-Saviaga, C., Hanrahan, B. V., Imteyaz, K.,
       dakhel, A., Tahir, A., & Khomh, F. (2024, March).          Clarke, S., & Savage, S. (2025, April). The impact
       Assessing the security of GitHub Copilot’s generated       of generative AI coding assistants on developers who
       code-a targeted replication study. In 2024 IEEE Inter-     are visually impaired. In Proceedings of the 2025 CHI
       national Conference on Software Analysis, Evolution        Conference on Human Factors in Computing Systems
       and Reengineering (SANER) (pp. 435-444). IEEE.             (pp. 1-17).
[WL11] Feng, L., Yen, R., You, Y., Fan, M., Zhao, J., & [WL20] Moore, J. H., & Tatonetti, N. (2025, July). Vibe cod-
       Lu, Z. (2024, May). Coprompt: Supporting prompt                ing: a new paradigm for biomedical software develop-
       sharing and referring in collaborative natural language        ment. BioData Mining, 18(1), 46.
       programming. In Proceedings of the 2024 CHI con-
       ference on human factors in computing systems (pp. [WL21] Lyu, M. R., Ray, B., Roychoudhury, A., Tan, S. H.,
       1-21).                                                         & Thongtanunam, P. (2025, May). Automatic pro-
                                                                      gramming: Large language models and beyond. ACM
[WL12] Xu, F. F., Vasilescu, B., & Neubig, G. (2022). In-ide          Transactions on Software Engineering and Methodol-
       code generation from natural language: Promise and             ogy, 34(5), 1-33.
       challenges. ACM Transactions on Software Engineer-
       ing and Methodology (TOSEM), 31(2), 1-47.               [WL22] Sergeyuk, A., Golubev, Y., Bryksin, T., & Ahmed, I.
                                                                      (2024). Using AI-Based Coding Assistants in Prac-
[WL13] Ross, S. I., Martinez, F., Houde, S., Muller, M., &            tice: State of Affairs. Perceptions, and Ways Forward,
       Weisz, J. D. (2023, March). The programmer’s assis-            10.
       tant: Conversational interaction with a large language
       model for software development. In Proceedings of [WL23] Cheng, R., Wang, R., Zimmermann, T., & Ford, D.
       the 28th international conference on intelligent user          (2024). “It would work for me too”: How online
       interfaces (pp. 491-514).                                      communities shape software developers’ trust in AI-
                                                                      powered code generation tools. ACM Transactions on
[WL14] Cox, D., Murray, J., & Salter, A. (2025, April). Rou-          Interactive Intelligent Systems, 14(2), 1-39.
       tine, twisty, and queer: pasts and futures of games
       programming pedagogy with no and low code tools. [WL24] Malamas, N., Tsardoulias, E., Panayiotou, K., &
       In Proceedings of the 20th International Conference            Symeonidis, A. L. (2025). Toward efficient vibe cod-
       on the Foundations of Digital Games (pp. 1-8).                 ing: An LLM-based agent for low-code software de-
                                                                      velopment. Journal of Computer Languages, 101367.
[WL15] Mitchell, J., & Shaaban, Y. (2025, October). Position:
       Vibe coding needs vibe reasoning: improving vibe [WL25] De Silva, D., Mills, N., Issadeen, Z., Moraliyage, H.,
       coding with formal verification. In Proceedings of             Jennings, A., & Manic, M. (2025, June). Generative
       the 1st ACM SIGPLAN International Workshop on                  AI Vibe Coding for Prototyping Industrial Systems.
       Language Models and Programming Languages (pp.                 In 2025 IEEE 34th International Symposium on In-
       84-90).                                                        dustrial Electronics (ISIE) (pp. 1-6). IEEE.

[WL16] Klemmer, J. H., Horstmann, S. A., Patnaik, N., Lud- [WL26] Beheshti, A. (2024, July). Natural language-oriented
       den, C., Burton Jr, C., Powers, C., ... & Fahl, S.         programming (NLOP): Towards democratizing soft-
       (2024, December). Using AI assistants in software          ware creation. In 2024 IEEE International Conference
       development: A qualitative study on security practices     on Software Services Engineering (SSE) (pp. 258-
       and concerns. In Proceedings of the 2024 on ACM            267). IEEE.


  S.Siddeeq et al.: Preprint submitted to Elsevier                                                            Page 33 of 35
                                                      Multivocal Review of Vibe Coding

[WL27] Meske, C., Hermanns, T., Von der Weiden, E., Loser, [GL13] Edwards, B. (2025, March 6). Will the future of soft-
       K. U., & Berger, T. (2025). Vibe coding as a reconfig-           ware development run on vibes? Ars Technica. https:
       uration of intent mediation in software development:             //arstechnica.com/ai/2025/03/is-vibe-coding-wit
       Definition, implications, and research agenda. IEEE              h-ai-gnarly-or-reckless-maybe-some-of-both/
       Access, 13, 213242-213259.
                                                                 [GL14] Geng, F., Shah, A., Li, H., Mulla, N., Swanson,
[WL28] Gadde, A. (2025). Democratizing software engineer-               S., Raj, G. S., ... & Porter, L. (2025). Exploring
       ing through Generative AI and vibe coding: The evo-              student-AI interactions in vibe coding. arXiv preprint
       lution of no-code development. Journal of Computer               arXiv:2507.22614.
       Science and Technology Studies, 7(4), 556-572.
                                                                 [GL15] van Hurne, M. H. (2025). A Technical Debt-Aware
                                                                        Prompting Framework for Sustainable Vibe Coding:
  Selected Grey Literature                                              Addressing the Production Readiness Crisis in AI-
                                                                        Assisted Software Development. Authorea Preprints.
 [GL1] Ray, P. P. (2025). A review on vibe coding: Fundamen-
       tals, state-of-the-art, challenges and future directions. [GL16] Crowson, M. G., & Celi, L. C. A. (2025). Aca-
       Authorea Preprints.                                              demic vibe coding: Opportunities for accelerating re-
                                                                        search in an era of resource constraint. arXiv preprint
 [GL2] Maes, S. H. (2025). The gotchas of AI coding and vibe
                                                                        arXiv:2508.00952.
       coding. it’s all about support and maintenance. OSF
       Preprints.                                                [GL17] Bollikonda, T., & Kovi, M. (2025). Intent-Driven
                                                                        Code Synthesis: Redefining Software Development
 [GL3] Horvat, M. (2025). What is Vibe coding and when                  with Transformers.
       should you use it (or not)?. Authorea Preprints.
                                                                 [GL18] Harkar, S. (2025). What is vibe coding? IBM. https:
 [GL4] Karpathy, A. (2025, February). There’s a new kind of             //www.ibm.com/think/topics/vibe-coding
       coding I call “vibe coding”. . . [Post]. X. https://x.co
       m/karpathy/status/1886192184808149383?lang=en             [GL19] Chowdhury, H., & Mann, J. (2025). Silicon Valley’s
                                                                        next act: Bringing “vibe coding” to the world. Busi-
 [GL5] Gaspar, N. (2025, May 11). The state of vibe coding              ness Insider.
       tools (May 2025). LinkedIn. https://www.linkedin.c
         om/pulse/state-vibe-coding-tools-may-2025-nufar-g
         aspar-x1znf/
                                                                        References
                                                                         [1] D. Russo, Navigating the complexity of generative ai adoption in
 [GL6] Huang, T. (2025, May 19). Vibe coding fundamentals                    software engineering, ACM Transactions on Software Engineering
       in 33 minutes [Video]. YouTube. https://youtu.be/i                    and Methodology 33 (5) (2024) 1–50.
                                                                         [2] S. I. Ross, F. Martinez, S. Houde, M. Muller, J. D. Weisz, The
         LCDSY2XX7E                                                          programmer’s assistant: Conversational interaction with a large lan-
                                                                             guage model for software development, in: Proceedings of the 28th
 [GL7] Sarkar, A., & Drosos, I. (2025). Vibe coding: pro-                    International Conference on Intelligent User Interfaces, 2023, pp.
       gramming through conversation with artificial intel-                  491–514.
       ligence. arXiv preprint arXiv:2506.23253.                         [3] J. Sauvola, S. Tarkoma, M. Klemettinen, J. Riekki, D. Doermann, Fu-
                                                                             ture of software development with generative ai, Automated Software
 [GL8] Sapkota, R., Roumeliotis, K. I., & Karkee, M. (2025).                 Engineering 31 (1) (2024) 26.
       Vibe coding vs. agentic coding: Fundamentals and                  [4] A. Karpathy, There’s a new kind of coding i call ‘vibe coding’. . . ,
       practical implications of agentic AI. arXiv preprint                  (February 2025).
                                                                             URL https://x.com/karpathy/status/1886192184808149383?lang=en
       arXiv:2505.19443.                                                 [5] S. Peng, E. Kalliamvakou, P. Cihon, M. Demirer, The impact of ai on
                                                                             developer productivity: Evidence from github copilot, arXiv preprint
 [GL9] Gómez, O. S. (2025). The Twilight of Software Engi-                   arXiv:2302.06590 (2023).
       neering in the Age of Vibe Coding.                                [6] A. Mastropaolo, L. Pascarella, E. Guglielmi, M. Ciniselli, S. Scal-
                                                                             abrino, R. Oliveto, G. Bavota, On the robustness of code gener-
[GL10] Fawzy, A., Tahir, A., & Blincoe, K. (2025). Vibe Cod-                 ation techniques: An empirical study on github copilot, in: 2023
       ing in Practice: Motivations, Challenges, and a Future                IEEE/ACM 45th International Conference on Software Engineering
       Outlook–a Grey Literature Review. arXiv preprint                      (ICSE), IEEE, 2023, pp. 2149–2160.
       arXiv:2510.00328.                                                 [7] M. Akhoroz, C. Yildirim, Conversational ai as a coding assistant:
                                                                             Understanding programmers’ interactions with and expectations from
[GL11] Google Cloud. (2025, April). Vibe coding explained:                   large language models for coding, arXiv preprint arXiv:2503.16508
                                                                             (2025).
       Tools and guides. https://cloud.google.com/discove                [8] N. Gaspar, The state of vibe coding tools (may 2025), LinkedIn (May
         r/what-is-vibe-coding                                               2025).
                                                                             URL https://www.linkedin.com/pulse/state-vibe-coding-tools-may
[GL12] Samsyudin, I. (2025). Vibe Coding and AI-Led Con-                     -2025-nufar-gaspar-x1znf/
       versational Programming: Emerging Trends in Soft-                 [9] T. Huang, Vibe coding fundamentals in 33 minutes, YouTube (May
       ware Development. Available at SSRN 5469367.                          2025).
                                                                             URL https://youtu.be/iLCDSY2XX7E

   S.Siddeeq et al.: Preprint submitted to Elsevier                                                                              Page 34 of 35
                                                         Multivocal Review of Vibe Coding

[10] S. Harkar, What is vibe coding?, IBM (2025).
     URL https://www.ibm.com/think/topics/vibe-coding
[11] H. Chowdhury, J. Mann, Silicon valley’s next act: Bringing “vibe
     coding” to the world, Business Insider (2025).
[12] B. Edwards, Will the future of software development run on vibes?,
     Ars Technica (March 2025).
     URL https://arstechnica.com/ai/2025/03/is-vibe-coding-with-a
     i-gnarly-or-reckless-maybe-some-of-both/
[13] Y. Ge, L. Mei, Z. Duan, T. Li, Y. Zheng, Y. Wang, L. Wang, J. Yao,
     T. Liu, Y. Cai, et al., A survey of vibe coding with large language
     models, arXiv preprint arXiv:2510.12399 (2025).
[14] P. P. Ray, A review on vibe coding: Fundamentals, state-of-the-art,
     challenges and future directions, Authorea Preprints (2025).
[15] A. Fawzy, A. Tahir, K. Blincoe, Vibe coding in practice: Motiva-
     tions, challenges, and a future outlook–a grey literature review, arXiv
     preprint arXiv:2510.00328 (2025).
[16] V. Garousi, M. Felderer, M. V. Mäntylä, Guidelines for including grey
     literature and conducting multivocal literature reviews in software
     engineering, Information and software technology 106 (2019) 101–
     121.
[17] B. Kitchenham, S. Charters, et al., Guidelines for performing system-
     atic literature reviews in software engineering (2007).
[18] V. R. Basili, G. Caldiera, H. D. Rombach, The goal question metric
     approach, in: Encyclopedia of Software Engineering, Vol. 1, John
     Wiley & Sons, 1994, pp. 528–532.
[19] C. Wohlin, Guidelines for snowballing in systematic literature studies
     and a replication in software engineering, in: Proceedings of the 18th
     international conference on evaluation and assessment in software
     engineering, 2014, pp. 1–10.
[20] T. Dybå, T. Dingsøyr, Empirical studies of agile software devel-
     opment: A systematic review, Information and software technology
     50 (9-10) (2008) 833–859.
[21] D. S. Cruzes, T. Dybå, Recommended steps for thematic synthesis in
     software engineering, in: 2011 International Symposium on Empir-
     ical Software Engineering and Measurement (ESEM), IEEE, 2011,
     pp. 275–284.
[22] A. M. Dakhel, V. Majdinasab, A. Nikanjam, F. Khomh, M. C. Des-
     marais, Z. M. J. Jiang, Github copilot ai pair programmer: Asset or
     liability?, Journal of Systems and Software 203 (2023) 111734.
[23] S. Siddeeq, M. Waseem, K.-K. Kemell, M. Saari, J. Rasku, P. Abra-
     hamsson, Vibe coding in software development: A multivocal litera-
     ture review (Jul. 2026). doi:10.5281/zenodo.21490083.
     URL https://doi.org/10.5281/zenodo.21490083




S.Siddeeq et al.: Preprint submitted to Elsevier                                            Page 35 of 35
